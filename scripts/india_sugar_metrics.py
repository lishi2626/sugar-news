from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = PROJECT_ROOT / "public" / "sugar-news"
METRICS_ROOT = PUBLIC_ROOT / "data" / "india_metrics"
HISTORY_PATH = METRICS_ROOT / "history.json"
try:
    SHANGHAI = ZoneInfo("Asia/Shanghai")
except Exception:
    SHANGHAI = timezone(timedelta(hours=8), name="Asia/Shanghai")

CHINIMANDI_SEARCH = "https://www.chinimandi.com/?s="
CHINIMANDI_DAILY_MARKET_UPDATE_URL = "https://www.chinimandi.com/english-news/daily-sugar-market-update/"
CHINIMANDI_WHOLESALE_URL = "https://www.chinimandi.com/wholesale-sugar-prices/"
CHINIMANDI_RETAIL_URL = "https://www.chinimandi.com/retail-prices/"
CHINIMANDI_AJAX_URL = "https://www.chinimandi.com/wp-admin/admin-ajax.php"
CHINIMANDI_CITIES = ("Delhi", "Kanpur", "Raipur", "Mumbai", "Ranchi", "Kolkata", "Guwahati", "Hyderabad", "Chennai")
INVENTORY_SEARCH_QUERIES = (
    "Department of Food and Public Distribution sugar stock",
    "Department of Food & Public Distribution sugar stock",
    "India sugar balance sheet",
    "India sugar closing stock",
    "India sugar opening stock",
    "sugar stock position India",
    "site:dfpd.gov.in sugar stock",
    "site:gov.in India sugar closing stock",
    "ISMA sugar closing stock",
    "ISMA sugar balance sheet",
    "ISMA sugar production estimate",
    "ISMA opening stock and closing stock",
    "site:ismaindia.com closing stock sugar",
    "NFCSF India sugar closing stock",
    "NFCSF sugar balance sheet",
    "NFCSF sugar production estimate",
    "National Federation Cooperative Sugar Factories closing stock",
    "site:coopsugar.org closing stock",
)
MARKET_FORECAST_SEARCH_QUERIES = (
    "ICRA India sugar closing inventory",
    "India sugar carryover stock market forecast",
    "India sugar ending stocks agency forecast",
    "India sugar balance sheet closing stocks rating agency",
)
AUTHORIZED_STOCK_SOURCES = ("Government of India", "Department of Food and Public Distribution", "ISMA", "NFCSF")
AUTHORIZED_STOCK_PRIORITY = {
    "Government of India": 0,
    "Department of Food and Public Distribution": 0,
    "ISMA": 1,
    "NFCSF": 2,
}


def beijing_now() -> datetime:
    fixed = os.getenv("SUGAR_NEWS_NOW")
    if fixed:
        return datetime.fromisoformat(fixed).astimezone(SHANGHAI)
    return datetime.now(SHANGHAI)


def fetch_url(url: str, timeout: int = 25) -> tuple[str, int]:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 SugarNewsBot/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "ignore")
        return body, resp.status


def post_form(url: str, data: dict, timeout: int = 25) -> tuple[str, int]:
    encoded = urlencode(data).encode("utf-8")
    req = Request(
        url,
        data=encoded,
        headers={
            "User-Agent": "Mozilla/5.0 SugarNewsBot/1.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
        method="POST",
    )
    with urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", "ignore")
        return body, resp.status


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[dict] = []
        self._table_stack: list[dict] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._capture_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            self._table_stack.append({"id": attrs_dict.get("id", ""), "caption": "", "rows": []})
        elif tag == "caption" and self._table_stack:
            self._capture_depth = 1
            self._cell = []
        elif tag == "tr" and self._table_stack:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag):
        if tag in {"td", "th"} and self._row is not None and self._cell is not None:
            text = re.sub(r"\s+", " ", html.unescape("".join(self._cell))).strip()
            self._row.append(text)
            self._cell = None
        elif tag == "caption" and self._table_stack and self._cell is not None:
            self._table_stack[-1]["caption"] = re.sub(r"\s+", " ", "".join(self._cell)).strip()
            self._cell = None
        elif tag == "tr" and self._table_stack and self._row is not None:
            if any(self._row):
                self._table_stack[-1]["rows"].append(self._row)
            self._row = None
        elif tag == "table" and self._table_stack:
            self.tables.append(self._table_stack.pop())


def number(text: str | int | float | None) -> float | None:
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return float(text)
    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", str(text))
    if not match:
        return None
    return float(match.group(0).replace(",", ""))


def round2(value: float | None) -> float | None:
    return None if value is None else round(value, 2)


def inr_per_quintal_to_kg(value: float | None) -> float | None:
    return None if value is None else round(value / 100, 4)


def percent_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or previous == 0:
        return None
    return (current - previous) / previous * 100


def history_indicators(indicator: str) -> set[str]:
    return {indicator}


def history_value(record: dict | None, indicator: str, value_kind: str) -> float | None:
    if not record:
        return None
    if indicator == "india_wholesale_price":
        if value_kind == "price":
            return number(record.get("price_inr_per_quintal") or record.get("wholesale_price_inr_per_quintal"))
    if indicator == "india_retail_price":
        if value_kind == "price":
            return number(record.get("price_inr_per_kg") or record.get("retail_price_inr_per_kg"))
    return number(record.get(value_kind))


def latest_record_before(history: dict, indicator: str, data_date: str | None) -> dict | None:
    allowed = history_indicators(indicator)
    rows = [
        r for r in history.get("records", [])
        if r.get("indicator") in allowed and r.get("status") == "ok"
    ]
    if data_date:
        rows = [r for r in rows if (r.get("data_date") or r.get("forecast_date") or "") < data_date]
    rows.sort(key=lambda r: (r.get("data_date") or r.get("forecast_date") or "", r.get("fetched_at") or ""), reverse=True)
    return rows[0] if rows else None


def comparable_yoy_record(history: dict, indicator: str, data_date: str | None, max_days: int = 3) -> dict | None:
    if not data_date:
        return None
    try:
        target = datetime.fromisoformat(data_date).date().replace(year=int(data_date[:4]) - 1)
    except Exception:
        return None
    allowed = history_indicators(indicator)
    rows = [
        r for r in history.get("records", [])
        if r.get("indicator") in allowed and r.get("status") == "ok" and r.get("data_date")
    ]
    best = None
    best_delta = None
    for row in rows:
        try:
            row_date = datetime.fromisoformat(row["data_date"]).date()
        except Exception:
            continue
        delta = abs((row_date - target).days)
        if delta <= max_days and (best_delta is None or delta < best_delta):
            best = row
            best_delta = delta
    return best


def parse_chinimandi_date(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", value)
    if not match:
        return None
    day, month, year = map(int, match.groups())
    try:
        return datetime(year, month, day).date().isoformat()
    except ValueError:
        return None


def price_cell_value(value: str | None) -> tuple[float | None, str | None]:
    if value is None:
        return None, None
    raw = re.sub(r"\s+", " ", html.unescape(str(value))).strip()
    nums = [number(item) for item in re.findall(r"\d[\d,]*(?:\.\d+)?", raw)]
    nums = [item for item in nums if item is not None]
    if not nums:
        return None, raw or None
    if len(nums) >= 2 and re.search(r"[-–—]", raw):
        return (nums[0] + nums[1]) / 2, raw
    return nums[0], raw


def parse_supsystic_rows(rows_html: str) -> list[dict]:
    records: list[dict] = []
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", rows_html, re.I | re.S):
        cells = re.findall(r"<td\b[^>]*data-original-value=\"([^\"]*)\"[^>]*>(.*?)</td>", tr, re.I | re.S)
        if len(cells) < 2:
            continue
        raw_values = [html.unescape(cell[0]).strip() for cell in cells]
        data_date = parse_chinimandi_date(raw_values[0])
        if not data_date:
            continue
        city_prices: dict[str, float] = {}
        raw_city_prices: dict[str, str] = {}
        for city, raw in zip(CHINIMANDI_CITIES, raw_values[1:]):
            price, raw_text = price_cell_value(raw)
            if price is not None:
                city_prices[city] = price
                raw_city_prices[city] = raw_text or str(price)
        if city_prices:
            records.append({"data_date": data_date, "city_prices": city_prices, "raw_city_prices": raw_city_prices})
    return records


def chinimandi_table_request(table_id: int, source_url: str, search: str, log: dict) -> list[dict]:
    page_cache = log.setdefault("_pageCache", {})
    if source_url in page_cache:
        body, status = page_cache[source_url]
    else:
        body, status = fetch_url(source_url)
        page_cache[source_url] = (body, status)
        log.setdefault("sourcePages", []).append({"url": source_url, "httpStatus": status})
    nonce_match = re.search(r'DTGS_NONCE_FRONTEND\s*=\s*"([^"]+)"', body)
    if not nonce_match:
        raise RuntimeError("ChiniMandi Supsystic nonce not found")
    ajax_cache = log.setdefault("_ajaxCache", {})
    cache_key = f"{table_id}:{search}"
    if cache_key in ajax_cache:
        return ajax_cache[cache_key]
    request_body = {
        "action": "supsystic-tables",
        "route[action]": "getPageRows",
        "route[module]": "tables",
        "route[nonce]": nonce_match.group(1),
        "id": str(table_id),
        "searchParams[columnSearchPosition]": "bottom",
        "searchParams[minChars]": "0",
        "searchValue": search,
        "header": "1",
        "footer": "0",
        "draw": "1",
        "order[0][column]": "0",
        "order[0][dir]": "desc",
        "start": "0",
        "length": "120",
        "search[value]": search,
        "search[regex]": "false",
    }
    for idx in range(10):
        request_body[f"columns[{idx}][data]"] = str(idx)
        request_body[f"columns[{idx}][name]"] = ""
        request_body[f"columns[{idx}][searchable]"] = "true"
        request_body[f"columns[{idx}][orderable]"] = "true"
        request_body[f"columns[{idx}][search][value]"] = ""
        request_body[f"columns[{idx}][search][regex]"] = "false"
    response_body, ajax_status = post_form(CHINIMANDI_AJAX_URL, request_body)
    payload = json.loads(response_body)
    log.setdefault("ajaxRequests", []).append({
        "url": CHINIMANDI_AJAX_URL,
        "tableId": table_id,
        "search": search,
        "httpStatus": ajax_status,
        "recordsFiltered": payload.get("recordsFiltered"),
    })
    rows = parse_supsystic_rows(payload.get("rows", ""))
    ajax_cache[cache_key] = rows
    return rows


def month_searches(start_date: datetime.date, months_back: int) -> list[str]:
    searches = []
    year = start_date.year
    month = start_date.month
    for _ in range(months_back):
        searches.append(f"{month:02d}/{year}")
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return searches


def collect_chinimandi_rows(table_id: int, source_url: str, anchor_date: str, months_back: int, log: dict) -> list[dict]:
    anchor = datetime.fromisoformat(anchor_date).date()
    rows_by_date: dict[str, dict] = {}
    for search in month_searches(anchor, months_back):
        for row in chinimandi_table_request(table_id, source_url, search, log):
            rows_by_date[row["data_date"]] = row
    return sorted(rows_by_date.values(), key=lambda row: row["data_date"], reverse=True)


def row_on_or_before(rows: list[dict], date_text: str, strict: bool = False) -> dict | None:
    candidates = [row for row in rows if row["data_date"] < date_text] if strict else [row for row in rows if row["data_date"] <= date_text]
    candidates.sort(key=lambda row: row["data_date"], reverse=True)
    return candidates[0] if candidates else None


def average_for_common_cities(rows: list[dict]) -> tuple[float | None, list[str]]:
    valid_rows = [row for row in rows if row]
    if not valid_rows:
        return None, []
    common = set(valid_rows[0]["city_prices"])
    for row in valid_rows[1:]:
        common &= set(row["city_prices"])
    cities = [city for city in CHINIMANDI_CITIES if city in common]
    if not cities:
        return None, []
    value = sum(valid_rows[0]["city_prices"][city] for city in cities) / len(cities)
    return value, cities


def build_chinimandi_domestic_record(config: dict, target_date: str, log: dict) -> dict | None:
    rows = collect_chinimandi_rows(config["table_id"], config["source_url"], target_date, 3, log)
    current = row_on_or_before(rows, target_date)
    if not current:
        return None
    if current["data_date"] == target_date:
        previous_rows = rows
    else:
        previous_rows = collect_chinimandi_rows(config["table_id"], config["source_url"], current["data_date"], 3, log)
    previous = row_on_or_before(previous_rows, current["data_date"], strict=True)
    yoy_target = datetime.fromisoformat(current["data_date"]).date().replace(year=int(current["data_date"][:4]) - 1).isoformat()
    yoy_rows = collect_chinimandi_rows(config["table_id"], config["source_url"], yoy_target, 2, log)
    yoy = row_on_or_before(yoy_rows, yoy_target)
    comparison_rows = [current]
    if previous:
        comparison_rows.append(previous)
    if yoy:
        comparison_rows.append(yoy)
    current_value, cities = average_for_common_cities(comparison_rows)
    if current_value is None:
        return None
    previous_value = sum(previous["city_prices"][city] for city in cities) / len(cities) if previous else None
    yoy_value = sum(yoy["city_prices"][city] for city in cities) / len(cities) if yoy else None
    record = {
        "indicator": config["indicator"],
        "data_date": current["data_date"],
        "price_basis": "ChiniMandi城市样本均价，含GST",
        "grade": "M-30；Hyderabad为S-30",
        "includes_gst": True,
        "cities_used": cities,
        "city_count": len(cities),
        "city_prices": {city: round2(current["city_prices"][city]) for city in cities},
        "raw_city_prices": {city: current["raw_city_prices"].get(city) for city in cities},
        "unit": config["unit"],
        "previous_data_date": previous.get("data_date") if previous else None,
        "previous_value": round2(previous_value),
        "change_value": round2(current_value - previous_value) if previous_value is not None else None,
        "change_percent": round2(percent_change(current_value, previous_value)),
        "previous_year_date": yoy.get("data_date") if yoy else None,
        "previous_year_value": round2(yoy_value),
        "year_on_year_change": round2(current_value - yoy_value) if yoy_value is not None else None,
        "year_on_year_change_percent": round2(percent_change(current_value, yoy_value)),
        "source_name": "ChiniMandi",
        "source_url": config["source_url"],
        "daily_market_update_url": CHINIMANDI_DAILY_MARKET_UPDATE_URL,
        "fetched_at": beijing_now().isoformat(timespec="seconds"),
        "status": "ok",
    }
    if config["indicator"] == "india_wholesale_price":
        record["price_inr_per_quintal"] = round2(current_value)
        record["price_inr_per_kg"] = inr_per_quintal_to_kg(current_value)
    else:
        record["price_inr_per_kg"] = round2(current_value)
    return record


def parse_chinimandi_domestic_prices(target_date: str, history: dict) -> tuple[list[dict], dict]:
    log = {"source": "ChiniMandi domestic price tables", "requestedAt": beijing_now().isoformat(timespec="seconds")}
    records: list[dict] = []
    configs = (
        {"indicator": "india_wholesale_price", "table_id": 6, "source_url": CHINIMANDI_WHOLESALE_URL, "unit": "卢比/公担"},
        {"indicator": "india_retail_price", "table_id": 7, "source_url": CHINIMANDI_RETAIL_URL, "unit": "卢比/公斤"},
    )
    for config in configs:
        try:
            record = build_chinimandi_domestic_record(config, target_date, log)
            if record:
                records.append(record)
        except Exception as exc:
            log.setdefault("errors", []).append({"indicator": config["indicator"], "error": str(exc), "sourceUrl": config["source_url"]})
    log["parsed"] = bool(records)
    log["recordCount"] = len(records)
    log.pop("_pageCache", None)
    log.pop("_ajaxCache", None)
    return records, log


def chinimandi_candidate_urls(target_date: str) -> list[str]:
    dt = datetime.strptime(target_date, "%Y-%m-%d")
    ddmmyyyy = dt.strftime("%d/%m/%Y")
    search_terms = (
        f"Daily Sugar Market Update {ddmmyyyy}",
        "Uttar Pradesh sugar ex-mill price today",
        "UP M/30 sugar ex-mill rate",
        "Muzaffarnagar M-grade sugar price",
        "site:chinimandi.com Daily Sugar Market Update",
    )
    urls = []
    slug_date = dt.strftime("%d-%m-%Y")
    urls.append(f"https://www.chinimandi.com/daily-sugar-market-update-by-vizzie-{slug_date}/")
    urls.extend(CHINIMANDI_SEARCH + quote_plus(term) for term in search_terms)
    return urls


def chinimandi_daily_update_url(date_text: str) -> str:
    dt = datetime.strptime(date_text, "%Y-%m-%d")
    return f"https://www.chinimandi.com/daily-sugar-market-update-by-vizzie-{dt.strftime('%d-%m-%Y')}/"


def parse_price_range(text: str) -> tuple[float | None, float | None]:
    cleaned = html.unescape(text).replace("₹", "").replace("Rs.", "").replace("Rs", "")
    nums = [number(x) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", cleaned)]
    nums = [x for x in nums if x is not None]
    if not nums:
        return None, None
    if len(nums) == 1:
        return nums[0], nums[0]
    return nums[0], nums[1]


def parse_chinimandi_exmill_date(body: str) -> str | None:
    match = re.search(r"Ex-mill Sugar Prices as on\s*([A-Za-z]+),?\s*(\d{1,2})\s+(\d{4})", body, re.I)
    if not match:
        return None
    month, day, year = match.groups()
    try:
        return datetime.strptime(f"{month} {day} {year}", "%B %d %Y").date().isoformat()
    except ValueError:
        return None


def parse_up_exmill_article(date_text: str) -> tuple[dict | None, dict]:
    url = chinimandi_daily_update_url(date_text)
    log = {
        "source": "ChiniMandi — Daily Sugar Market Update",
        "url": url,
        "requestedAt": beijing_now().isoformat(timespec="seconds"),
    }
    try:
        body, status = fetch_url(url)
        log["httpStatus"] = status
    except Exception as exc:
        log["error"] = str(exc)
        return None, log
    if "Daily Sugar Market Update By Vizzie" not in body:
        log["parsed"] = False
        log["reason"] = "not a Daily Sugar Market Update By Vizzie report"
        return None, log
    if "Morning Market Update" in re.sub(r"Daily Sugar Market Update By Vizzie", "", body, flags=re.I) and "Ex-mill Sugar Prices" not in body:
        log["parsed"] = False
        log["reason"] = "not a formal daily close ex-mill report"
        return None, log
    data_date = parse_chinimandi_exmill_date(body)
    if not data_date:
        log["parsed"] = False
        log["reason"] = "Ex-mill Sugar Prices date not found"
        return None, log
    parser = TableParser()
    parser.feed(body)
    for table in parser.tables:
        rows = table.get("rows", [])
        if not rows or not any("Ex-mill Sugar Prices" in row_text for row in rows for row_text in row):
            # The ChiniMandi HTML table has no caption; identify by the header.
            header = rows[0] if rows else []
            if not (len(header) >= 3 and "State" in header[0] and "S/30" in header[1] and "M/30" in header[2]):
                continue
        for row in rows:
            if not row or row[0].strip().lower() != "uttar pradesh":
                continue
            m30_cell = row[2] if len(row) >= 3 else ""
            low, high = parse_price_range(m30_cell)
            if low is None or high is None:
                log["parsed"] = False
                log["reason"] = "Uttar Pradesh M/30 price missing"
                return None, log
            midpoint = (low + high) / 2
            raw_range = html.unescape(m30_cell).strip()
            record = {
                "indicator": "up_ex_mill_price",
                "display_range": f"₹{low:,.0f}—₹{high:,.0f}/公担",
                "raw_range": raw_range,
                "low": round2(low),
                "high": round2(high),
                "midpoint": round2(midpoint),
                "currency": "INR",
                "unit": "卢比/公担",
                "raw_unit": "₹/quintal",
                "data_date": data_date,
                "grade": "M/30",
                "region": "Uttar Pradesh",
                "quote_type": "ex-mill",
                "includes_gst": False,
                "gst_status": "excluding GST",
                "up_ex_mill_min_inr_per_quintal": round2(low),
                "up_ex_mill_max_inr_per_quintal": round2(high),
                "up_ex_mill_mid_inr_per_quintal": round2(midpoint),
                "up_ex_mill_min_inr_per_kg": inr_per_quintal_to_kg(low),
                "up_ex_mill_max_inr_per_kg": inr_per_quintal_to_kg(high),
                "up_ex_mill_mid_inr_per_kg": inr_per_quintal_to_kg(midpoint),
                "source_name": "ChiniMandi — Daily Sugar Market Update",
                "source_url": url,
                "fetched_at": beijing_now().isoformat(timespec="seconds"),
                "status": "ok",
            }
            log.update({"parsed": True, "dataDate": data_date, "min": low, "max": high, "rawRange": raw_range})
            return record, log
    log["parsed"] = False
    log["reason"] = "Ex-mill Sugar Prices Uttar Pradesh M/30 row not parsed"
    return None, log


def find_up_exmill_on_or_before(anchor_date: str, logs: list[dict], strict: bool = False, max_days: int = 21) -> dict | None:
    dt = datetime.strptime(anchor_date, "%Y-%m-%d").date()
    if strict:
        dt -= timedelta(days=1)
    for offset in range(max_days):
        date_text = (dt - timedelta(days=offset)).isoformat()
        record, log = parse_up_exmill_article(date_text)
        logs.append(log)
        if record:
            return record
    return None


def parse_chinimandi_up_exmill(target_date: str, history: dict) -> tuple[dict | None, list[dict]]:
    logs = []
    current = find_up_exmill_on_or_before(target_date, logs)
    if not current:
        return None, logs
    previous = find_up_exmill_on_or_before(current["data_date"], logs, strict=True)
    current_mid = current.get("midpoint")
    previous_mid = previous.get("midpoint") if previous else None
    change_value = float(current_mid) - float(previous_mid) if current_mid is not None and previous_mid is not None else None
    try:
        yoy_target = datetime.fromisoformat(current["data_date"]).date().replace(year=int(current["data_date"][:4]) - 1).isoformat()
    except ValueError:
        yoy_target = (datetime.fromisoformat(current["data_date"]).date() - timedelta(days=365)).isoformat()
    yoy = find_up_exmill_on_or_before(yoy_target, logs, max_days=31)
    yoy_mid = yoy.get("midpoint") if yoy else None
    current.update({
        "daily_change_absolute": round2(change_value),
        "daily_change_percent": round2(percent_change(current_mid, previous_mid)),
        "previous_date": previous.get("data_date") if previous else None,
        "previous_data_date": previous.get("data_date") if previous else None,
        "previous_low": previous.get("low") if previous else None,
        "previous_high": previous.get("high") if previous else None,
        "previous_midpoint": previous_mid,
        "previous_min": previous.get("low") if previous else None,
        "previous_max": previous.get("high") if previous else None,
        "previous_mid": previous_mid,
        "previous_source_url": previous.get("source_url") if previous else None,
        "yoy_change_absolute": round2(float(current_mid) - float(yoy_mid)) if current_mid is not None and yoy_mid is not None else None,
        "yoy_change_percent": round2(percent_change(current_mid, yoy_mid)),
        "yoy_comparison_date": yoy.get("data_date") if yoy else None,
        "previous_year_date": yoy.get("data_date") if yoy else None,
        "yoy_low": yoy.get("low") if yoy else None,
        "yoy_high": yoy.get("high") if yoy else None,
        "yoy_midpoint": yoy_mid,
        "previous_year_min": yoy.get("low") if yoy else None,
        "previous_year_max": yoy.get("high") if yoy else None,
        "previous_year_mid": yoy_mid,
        "yoy_source_url": yoy.get("source_url") if yoy else None,
        "yoy_exact_date_match": bool(yoy and yoy.get("data_date") == yoy_target),
        "year_on_year_change": round2(float(current_mid) - float(yoy_mid)) if current_mid is not None and yoy_mid is not None else None,
        "year_on_year_change_percent": round2(percent_change(current_mid, yoy_mid)),
        "change_value": round2(change_value),
        "change_percent": round2(percent_change(current_mid, previous_mid)),
        "change_direction": "up" if change_value and change_value > 0 else "down" if change_value and change_value < 0 else "flat" if change_value == 0 else "unknown",
    })
    return current, logs


def google_news_rss(query: str) -> str:
    return "https://news.google.com/rss/search?q=" + quote_plus(query) + "&hl=en-US&gl=US&ceid=US:en"


def parse_inventory_from_search(target_date: str, history: dict) -> tuple[list[dict], list[dict]]:
    logs = []
    # Inventory forecasts require explicit season and stock wording; this
    # search stage records candidates, but does not publish unverified numbers.
    for query in INVENTORY_SEARCH_QUERIES:
        url = google_news_rss(f"{query} {target_date}")
        log = {"source": "Google News RSS inventory discovery", "query": query, "url": url, "requestedAt": beijing_now().isoformat(timespec="seconds")}
        try:
            body, status = fetch_url(url)
            log["httpStatus"] = status
            log["candidateCount"] = len(re.findall(r"<item>", body))
            log["parsed"] = False
            log["sourceTier"] = "authoritative_main_value_only"
            log["allowedMainSources"] = list(AUTHORIZED_STOCK_SOURCES)
            log["reason"] = "Inventory candidates require source-page season, organization and closing-stock verification before publication."
        except Exception as exc:
            log["error"] = str(exc)
        logs.append(log)
    for query in MARKET_FORECAST_SEARCH_QUERIES:
        url = google_news_rss(f"{query} {target_date}")
        log = {"source": "Google News RSS market forecast discovery", "query": query, "url": url, "requestedAt": beijing_now().isoformat(timespec="seconds")}
        try:
            body, status = fetch_url(url)
            log["httpStatus"] = status
            log["candidateCount"] = len(re.findall(r"<item>", body))
            log["parsed"] = False
            log["sourceTier"] = "market_forecast_comparison_only"
            log["reason"] = "Market forecasts are comparison-only and require original report date, season and closing-stock verification before publication."
        except Exception as exc:
            log["error"] = str(exc)
        logs.append(log)
    return [], logs


def load_history() -> dict:
    if HISTORY_PATH.exists():
        with HISTORY_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "records": [], "lastUpdatedAt": None}


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(path.parent), suffix=".tmp") as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=2)
        temp_name = tmp.name
    Path(temp_name).replace(path)


def record_key(record: dict) -> tuple:
    if record["indicator"] in {"carryover_stock", "market_carryover_forecast"}:
        return (record["indicator"], record.get("season"), record.get("forecast_organization"), record.get("forecast_date"))
    if record["indicator"] == "up_ex_mill_price":
        return (record["indicator"], record.get("grade"), record.get("region"), record.get("data_date"), record.get("source_name"))
    return (record["indicator"], record.get("data_date"), record.get("source_name"))


def latest_record(history: dict, indicator: str, exclude_date: str | None = None) -> dict | None:
    rows = [r for r in history.get("records", []) if r.get("indicator") == indicator and r.get("status") == "ok"]
    if exclude_date:
        rows = [r for r in rows if r.get("data_date") != exclude_date and r.get("forecast_date") != exclude_date]
    rows.sort(key=lambda r: (r.get("data_date") or r.get("forecast_date") or "", r.get("fetched_at") or ""), reverse=True)
    return rows[0] if rows else None


def upsert_records(history: dict, records: list[dict]) -> dict:
    existing = {record_key(r): r for r in history.get("records", [])}
    for record in records:
        if not record:
            continue
        existing[record_key(record)] = record
    history["records"] = sorted(existing.values(), key=lambda r: (r.get("indicator", ""), r.get("data_date") or r.get("forecast_date") or "", r.get("fetched_at") or ""))
    history["lastUpdatedAt"] = beijing_now().isoformat(timespec="seconds")
    return history


def build_snapshot(history: dict, target_date: str, logs: list[dict]) -> dict:
    wholesale = latest_record(history, "india_wholesale_price")
    retail = latest_record(history, "india_retail_price")
    up_ex = latest_record(history, "up_ex_mill_price")
    stock_records = [
        r for r in history.get("records", [])
        if r.get("indicator") == "carryover_stock"
        and r.get("status") == "ok"
        and (r.get("forecast_organization") or r.get("source_name")) in AUTHORIZED_STOCK_PRIORITY
    ]
    stock_records.sort(key=lambda r: (AUTHORIZED_STOCK_PRIORITY.get(r.get("forecast_organization") or r.get("source_name"), 99), -(int((r.get("forecast_date") or "0000-00-00").replace("-", "")) if re.match(r"\d{4}-\d{2}-\d{2}", r.get("forecast_date") or "") else 0)))
    main_stock = stock_records[0] if stock_records else None
    market_forecasts = [r for r in history.get("records", []) if r.get("indicator") == "market_carryover_forecast" and r.get("status") == "ok"]
    market_forecasts.sort(key=lambda r: (r.get("forecast_date") or "", r.get("fetched_at") or ""), reverse=True)
    return {
        "targetDate": target_date,
        "updatedAt": beijing_now().isoformat(timespec="seconds"),
        "domesticWholesalePrice": wholesale,
        "domesticRetailPrice": retail,
        "domesticSugarPrice": wholesale,
        "upExMillPrice": up_ex,
        "carryoverStock": main_stock,
        "authorizedCarryoverStockAlternatives": stock_records[1:10],
        "carryoverStockForecasts": market_forecasts[:10],
        "fetchLog": logs,
    }


def collect(target_date: str) -> dict:
    history = load_history()
    logs: list[dict] = []
    records: list[dict] = []
    domestic_records, log = parse_chinimandi_domestic_prices(target_date, history)
    logs.append(log)
    records.extend(domestic_records)
    up_ex, up_logs = parse_chinimandi_up_exmill(target_date, history)
    logs.extend(up_logs)
    if up_ex:
        records.append(up_ex)
    inventory_records, inventory_logs = parse_inventory_from_search(target_date, history)
    logs.extend(inventory_logs)
    records.extend(inventory_records)
    if records:
        history = upsert_records(history, records)
        atomic_write_json(HISTORY_PATH, history)
    snapshot = build_snapshot(history, target_date, logs)
    atomic_write_json(METRICS_ROOT / "latest.json", snapshot)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch India sugar price and stock metrics.")
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    snapshot = collect(args.date)
    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
