from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

from brazil_sugar_metrics import stock_rows_from_pdf
from sugar_news_pipeline import (
    COUNTRY_SEARCH_TEMPLATES,
    infer_core_country,
    is_india_indirect_sugar_relevant,
    is_medical_sugar_context,
    normalize_items,
    rss_sugar_relevant,
    tmd_thai_weather_item_from_text,
    validate_editorial_quality,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASK_ROOT = PROJECT_ROOT
TARGET_DATE = "2026-07-20"
REQUIRED_DEDUPE_KEYS = {
    "india_aista_sugar_supply_shortage_unwarranted_20260720",
    "india_no_plan_ethanol_blend_above_e20_20260720",
    "india_cane_states_monsoon_heavy_rain_forecast_20260720",
}


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def test_india_relevance_helpers() -> None:
    assert is_india_indirect_sugar_relevant(
        "India says no plan now to raise ethanol mix in gasoline above 20%; "
        "maize accounts for 37% of ethanol feedstock while molasses and sugar syrup remain cane-based inputs."
    )
    assert is_india_indirect_sugar_relevant(
        "OMC ethanol procurement tender includes B-heavy molasses, C-heavy molasses and sugar syrup supplies."
    )


def test_india_search_templates_cover_e20_reuters() -> None:
    queries = "\n".join(template for _language, template in COUNTRY_SEARCH_TEMPLATES["印度"])
    for expected in (
        "India E20 petrol",
        "India ethanol above 20 percent",
        "India grain ethanol",
        "India maize ethanol",
        "India OMC ethanol tender",
        "site:reuters.com India E20",
        "site:reuters.com India ethanol",
        "site:reuters.com India molasses",
    ):
        assert expected in queries


def test_thailand_weather_templates_and_tmd_item_generation() -> None:
    queries = "\n".join(template for _language, template in COUNTRY_SEARCH_TEMPLATES["泰国"])
    for expected in (
        "Thailand sugarcane rainfall forecast",
        "Udon Thani Khon Kaen Nakhon Ratchasima",
        "Nakhon Sawan Kanchanaburi Lopburi Chai Nat",
    ):
        assert expected in queries

    sample = (
        "Forecast Date: July 23, 2026 Daily Weather Forecast Issued at 5.00 a.m. "
        "During 23 - 24 Jul, the strong southwest monsoon prevails over Thailand. "
        "Northeastern: Scattered thundershowers and isolated heavy rains mostly in "
        "Loei, Udon Thani and Khon Kaen. Central: Fairly widespread thundershowers "
        "and isolated heavy rains in Kanchanaburi. Eastern: thundershowers in Sa Kaeo and Chon Buri."
    )
    item = tmd_thai_weather_item_from_text(sample, "2026-07-23")
    assert item is not None
    assert item["country_group"] == "泰国"
    assert item["impact"].startswith("利空：")
    assert "幅度有限" not in item["impact"]
    assert "乌隆他尼" in item["news"]
    assert "孔敬" in item["news"]
    assert "北碧" in item["news"]


def test_no_fixed_country_cap_in_autogen() -> None:
    source = (PROJECT_ROOT / "scripts" / "sugar_news_pipeline.py").read_text(encoding="utf-8")
    assert "retained_for_country >= 2" not in source


def test_non_industry_sugar_titles_are_filtered() -> None:
    assert not rss_sugar_relevant("其他国家", "Palm Sugar: A Village Story launches on Windows PC")
    assert not rss_sugar_relevant("印度", "Bengaluru author debuts novel The Burnt Sugar Club")


def test_editorial_country_reclassification_rules() -> None:
    indonesia_country, indonesia_group = infer_core_country(
        "ChiniMandi reports Indonesia sugar import policy and domestic sugar supply",
        "巴西",
    )
    assert indonesia_country == "印度尼西亚"
    assert indonesia_group == "其他国家"

    cameroon_country, cameroon_group = infer_core_country(
        "ChiniMandi reports Cameroon sugar production and import policy",
        "印度",
    )
    assert cameroon_country == "喀麦隆"
    assert cameroon_group == "其他国家"


def test_medical_sugar_news_is_excluded() -> None:
    sample = "Blood sugar monitoring improves diabetes treatment with insulin guidance"
    assert is_medical_sugar_context(sample)
    assert not rss_sugar_relevant("其他国家", sample)


def test_valid_brazil_cane_sugar_ethanol_news_is_allowed() -> None:
    sample = "Brazil sugarcane crushing and sugar production rise while mills adjust ethanol output"
    assert rss_sugar_relevant("巴西", sample)
    country, group = infer_core_country(sample, "巴西")
    assert country == "巴西"
    assert group == "巴西"


def test_india_water_resource_pressure_is_bullish() -> None:
    data = {
        "target_date": "2026-07-23",
        "items": [
            {
                "country_group": "印度",
                "country": "印度",
                "title": "印度半干旱地区甘蔗单产提升伴随水资源风险",
                "news": "Mongabay India称，印度半干旱地区甘蔗单产提升的同时，仍面临气候和水资源压力。水分约束可能限制甘蔗可持续扩产，并增加未来糖料供应波动风险。来源：Mongabay India（https://example.test/water）",
                "impact": "利多：水资源压力和水分约束可能限制甘蔗扩产和单产稳定性，未来糖料供应存在下降风险。",
                "source_name": "Mongabay India",
                "source_url": "https://example.test/water",
                "published_date_local": "2026-07-23",
                "dedupe_key": "india_water_resource_pressure",
            }
        ],
    }
    assert len(normalize_items(data)) == 1
    data["items"][0]["impact"] = "影响有限：报道未明确对应印度核心甘蔗主产区。"
    try:
        normalize_items(data)
    except ValueError as exc:
        assert "water-resource pressure" in str(exc)
    else:
        raise AssertionError("water-resource pressure should require bullish impact")


def test_editorial_quality_rejects_publication_date_formula_and_accepts_key_dates() -> None:
    bad = {
        "country_group": "印度",
        "country": "印度",
        "title": "India sugar policy",
        "news": "2026-07-23 ChiniMandi报道：印度糖厂甘蔗款支付改善。甘蔗款支付改善有助于稳定未来糖料供应。来源：ChiniMandi（https://example.test/a）",
        "impact": "利空：甘蔗款支付改善有助于稳定未来糖料供应。",
    }
    try:
        validate_editorial_quality(bad, 1)
    except ValueError as exc:
        assert "publication-date" in str(exc) or "reporting formula" in str(exc)
    else:
        raise AssertionError("publication date formula should be rejected")

    good = {
        "country_group": "印度",
        "country": "印度",
        "title": "India sugar policy",
        "news": "印度政府公布2026/27榨季甘蔗款支付安排，政策执行期关系到糖厂现金流和蔗农交售节奏。若付款秩序改善，蔗农种植积极性和后续糖料供应预期将得到支撑。来源：ChiniMandi（https://example.test/a）",
        "impact": "利空：甘蔗款支付改善有助于稳定未来糖料供应。",
    }
    validate_editorial_quality(good, 2)


def test_summary_must_be_two_or_three_chinese_sentences() -> None:
    data = {
        "target_date": "2026-07-23",
        "items": [
            {
                "country_group": "巴西",
                "country": "巴西",
                "title": "Brazil sugarcane",
                "news": "巴西中南部甘蔗压榨进度改善，糖产量释放速度加快。供应增加可能提高国际市场可用糖源，对原糖价格形成压力。来源：Test（https://example.test/b）",
                "impact": "利空：糖产量释放增加可能压制国际糖价。",
                "source_name": "Test",
                "source_url": "https://example.test/b",
                "published_date_local": "2026-07-23",
                "dedupe_key": "test_brazil_cane",
            }
        ],
    }
    assert len(normalize_items(data)) == 1

    data["items"][0]["news"] = "巴西中南部甘蔗压榨进度改善。来源：Test（https://example.test/b）"
    try:
        normalize_items(data)
    except ValueError as exc:
        assert "2-3" in str(exc)
    else:
        raise AssertionError("one-sentence summary should be rejected")


def test_brazil_india_metric_value_is_under_absolute_column() -> None:
    html = (PROJECT_ROOT / "public" / "sugar-news" / "index.html").read_text(encoding="utf-8")
    assert '["字段", "绝对值", "（%）"]' in html
    assert 'appendValueRow("取值", config.value());' in html
    assert 'const td = document.createElement("td");' in html
    assert 'const pctTd = document.createElement("td");' in html
    assert html.index('td.className = "brazil-metric-main";') < html.index('pctTd.className = "metric-change na";')


def test_ist_utc_beijing_date_handling() -> None:
    try:
        ist = ZoneInfo("Asia/Kolkata")
    except Exception:
        ist = timezone(timedelta(hours=5, minutes=30), name="Asia/Kolkata")
    try:
        shanghai = ZoneInfo("Asia/Shanghai")
    except Exception:
        shanghai = timezone(timedelta(hours=8), name="Asia/Shanghai")
    local_article_time = datetime(2026, 7, 20, 0, 30, tzinfo=ist)
    assert local_article_time.date().isoformat() == TARGET_DATE
    assert local_article_time.astimezone(timezone.utc).date().isoformat() == "2026-07-19"
    assert datetime(2026, 7, 21, 6, 0, tzinfo=shanghai).date().isoformat() == "2026-07-21"


def test_verified_news_contains_required_india_items() -> None:
    data = read_json(TASK_ROOT / "data" / "verified_news" / "2026" / "07" / f"sugar_news_{TARGET_DATE}.json")
    keys = {item.get("dedupe_key") for item in data["items"]}
    assert REQUIRED_DEDUPE_KEYS <= keys
    country_counts = Counter(item.get("country_group") for item in data["items"])
    assert country_counts["印度"] >= 4


def test_excel_dashboard_consistency() -> None:
    report = read_json(PROJECT_ROOT / "public" / "sugar-news" / "data" / "reports" / "2026" / "07" / f"{TARGET_DATE}.json")
    excel_path = TASK_ROOT / "reports" / "2026" / "07" / f"Sugar News {TARGET_DATE}.xlsx"
    workbook = load_workbook(excel_path)
    sheet = workbook.active
    excel_rows = [
        (row[0], row[1], row[2])
        for row in sheet.iter_rows(min_row=2, values_only=True)
        if row[0] and row[1]
    ]
    dashboard_rows = [
        (country["country"], item["news"], f'{item["impactType"]}：{item["impact"]}')
        for country in report["countries"]
        for item in country["items"]
    ]
    assert len(excel_rows) == len(dashboard_rows)
    assert Counter(row[0] for row in excel_rows)["印度"] >= 4
    dashboard_text = "\n".join(news for _country, news, _impact in dashboard_rows)
    for phrase in ("AISTA", "E20以上", "Hardoi和Unnao"):
        assert phrase in dashboard_text


def test_india_metrics_price_changes_and_stock_source_rules() -> None:
    report = read_json(PROJECT_ROOT / "public" / "sugar-news" / "data" / "reports" / "2026" / "07" / f"{TARGET_DATE}.json")
    metrics = report["indiaMetrics"]
    expected_chinimandi_urls = {
        "domesticWholesalePrice": "https://www.chinimandi.com/wholesale-sugar-prices/",
        "domesticRetailPrice": "https://www.chinimandi.com/retail-prices/",
    }
    for field in ("domesticWholesalePrice", "domesticRetailPrice", "upExMillPrice"):
        metric = metrics[field]
        assert metric["status"] == "ok"
        assert metric["previousDataDate"]
        assert metric["changePct"] is not None
        if field in expected_chinimandi_urls:
            assert metric["sourceName"] == "ChiniMandi"
            assert metric["sourceUrl"] == expected_chinimandi_urls[field]
            assert metric["includesGst"] is True
            assert metric["citiesUsed"]
            assert metric["cityCount"] == len(metric["citiesUsed"])
        if field == "domesticRetailPrice":
            assert metric["changeInrPerKg"] is not None
        else:
            assert metric["changeInrPerQuintal"] is not None
        if field == "upExMillPrice":
            low = metric["rangeInrPerQuintal"]["low"]
            high = metric["rangeInrPerQuintal"]["high"]
            assert metric["midpointInrPerQuintal"] == (low + high) / 2
            assert metric["sourceName"] == "ChiniMandi — Daily Sugar Market Update"
            assert metric["market"] == "Uttar Pradesh"
            assert metric["grade"] == "M/30"
            assert metric["includesGst"] is False
            assert "daily-sugar-market-update-by-vizzie" in metric["sourceUrl"]
            assert metric["previousSourceUrl"]
            assert metric["yoySourceUrl"]

    stock = metrics["carryoverStock"]
    if stock["status"] == "ok":
        source = stock.get("organization") or stock.get("sourceName") or ""
        assert any(token in source for token in ("Government of India", "Department of Food", "ISMA", "NFCSF", "印度政府"))
    for forecast in metrics.get("carryoverStockForecasts", []):
        assert forecast.get("sourceTier") == "market_forecast_comparison_only"


def test_brazil_sugar_stock_date_comes_from_acumulado_ate() -> None:
    sample_text = "BRASIL 1.000 2.000 3.450.164 Acumulado ate: 30/06/2026"
    rows = stock_rows_from_pdf(
        sample_text,
        "2026/2027",
        {
            "title": "ESTOQUES DE AÇÚCAR POR TIPO - SAFRA 2026-27",
            "url": "https://example.test/009ESTOQUESDEACARPORTIPOSAFRA20262027_20072026.pdf",
            "document_number": "009",
            "published_at": "2026-07-20",
        },
        "test-hash",
    )
    assert len(rows) == 1
    assert rows[0]["reference_date"] == "2026-06-30"
    assert rows[0]["reference_date_raw"] == "30/06/2026"
    assert rows[0]["reference_date_source"] == "pdf_acumulado_ate"
    assert rows[0]["document_title"] == "ESTOQUES DE AÇÚCAR POR TIPO - SAFRA 2026-27"
    assert rows[0]["stock_total_tonnes"] == 3450164


def test_brazil_dashboard_does_not_show_fetch_time_or_report_as_date() -> None:
    html = (PROJECT_ROOT / "public" / "sugar-news" / "index.html").read_text(encoding="utf-8")
    assert "发布日期/报告" not in html
    assert "last fetched" not in html.lower()
    assert "fetched_at" not in html
    assert "数据日期：" in html


def main() -> None:
    tests = [
        test_india_relevance_helpers,
        test_india_search_templates_cover_e20_reuters,
        test_thailand_weather_templates_and_tmd_item_generation,
        test_no_fixed_country_cap_in_autogen,
        test_non_industry_sugar_titles_are_filtered,
        test_editorial_country_reclassification_rules,
        test_medical_sugar_news_is_excluded,
        test_valid_brazil_cane_sugar_ethanol_news_is_allowed,
        test_india_water_resource_pressure_is_bullish,
        test_editorial_quality_rejects_publication_date_formula_and_accepts_key_dates,
        test_summary_must_be_two_or_three_chinese_sentences,
        test_brazil_india_metric_value_is_under_absolute_column,
        test_ist_utc_beijing_date_handling,
        test_verified_news_contains_required_india_items,
        test_excel_dashboard_consistency,
        test_india_metrics_price_changes_and_stock_source_rules,
        test_brazil_sugar_stock_date_comes_from_acumulado_ate,
        test_brazil_dashboard_does_not_show_fetch_time_or_report_as_date,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise
