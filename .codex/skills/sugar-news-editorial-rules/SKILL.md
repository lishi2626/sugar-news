---
name: sugar-news-editorial-rules
description: Maintain and validate Sugar News article summaries, country classification, sugar-industry relevance filtering, pre-publish quality checks, daily report JSON/Excel consistency, and Chinese sugar research writing style.
---

# Sugar News Editorial Rules

## Scope

Use this skill only inside the independent `sugar-news` project. Do not modify Sugar Daily.

This skill governs the news section only. Price, stock, weather dashboard data, deployment configuration, and page layout may be changed only when the user explicitly asks.

The daily GitHub Actions workflow runs `scripts/sugar_news_pipeline.py`. That pipeline must load this `SKILL.md`, validate its required rules, and record the skill path and SHA-256 hash in the run log before publishing.

## Mandatory News Summary Rules

Each news item must be rewritten into 2-3 concise Chinese sentences.

The first sentence states the core event, policy, data, weather change, production change, trade change, or company action.

The following sentence or sentences state the impact path on sugar supply, demand, inventories, cane or beet production, ethanol diversion, imports or exports, production cost, or sugar prices.

Do not merely copy the title. Do not produce a long article-style rewrite. Do not add facts, figures, dates, or judgments that are absent from the source.

Use natural Chinese sugar-industry research language. Remove promotional wording, background padding, repeated boilerplate, and low-value commentary.

## Date Expression Rules

Do not mechanically repeat ordinary publication dates in every item, including wording such as `今日发布`, `今天发布`, `本日发布`, `X月X日消息`, `X月X日报道`, or a leading `YYYY-MM-DD 来源报道：`.

If a date is only the article publication time, remove it from the summary body.

Keep dates only when the date itself changes the market judgment, such as policy effective dates, quota execution months, export ban windows, crushing periods, statistical cutoff dates, factory opening or closure dates, weather forecast coverage periods, or inventory report periods.

Distinguish article publication date, event date, and data reference date.

## Country Assignment Rules

Classify news by the core event subject, event location, policy implementation country, production area, and main affected sugar market. Never classify only by media source, website country, article language, reposting platform, company headquarters, or the country mentioned most often.

Priority-country rules:

- Brazil: Brazil government, mills, cane, ethanol, sugar output, sugar exports, or Brazil sugar/ethanol market data.
- India: India government, parliament, courts, sugar mills, cane dues, cane disease, stock policy, hoarding control, ethanol policy tied to cane/molasses/sugar syrup, and domestic sugar price policy.
- Thailand: Thailand policy, cane production, cane-area weather, and sugar mill news.
- China: China policy, production, imports, sugar syrup, futures, and price news.

Other-country rules:

- Indonesia news must be `其他国家` with country `印度尼西亚`.
- Cameroon, Philippines, Vietnam, Russia, Pakistan, Fiji, Kenya, Bangladesh, South Africa, UK, US, Australia, Poland, Mexico, and similar items must use the actual country name, not a generic `其他国家`.
- ChiniMandi or another India-based source reporting a non-India event must be classified by the event country, not India.
- Global sugar-price, crude-oil, futures, or multi-country supply-demand items without one clear national subject should use country `全球`.

For two-country trade stories, use one main country:

- Import policy, import volume, or domestic supply impact -> importing country.
- Export quota, export sale, or production allocation -> exporting country.
- If neither country is clearly primary -> `全球`.

Never publish the same story in multiple country sections.

Before publication, compare title entities, summary entities, and the chosen country column. If they conflict, reclassify automatically when the country is clear; otherwise put the item into a hold/review list and stop publication.

## Sugar-Industry Relevance Rules

Sugar News only keeps direct sugar-industry content:

- sugar, raw sugar, white sugar, beet sugar;
- cane or beet planting, yield, disease, harvest, weather, or disasters;
- mills, crushing, production, factory opening or closure, processing capacity, labor disruption;
- cane dues, cane price, sugar price, subsidies, quotas, stock limits, hoarding control, taxes, tariffs, regulation;
- inventories, wholesale/retail/ex-mill prices, futures, imports, exports, and trade flows;
- cane ethanol, molasses ethanol, sugar-syrup ethanol, sugar-to-ethanol allocation, and sugar-industry feedstock diversion;
- major cane-area weather that directly affects cane growth, harvest, transport, crushing, or sugar output.

Water-resource pressure rule:

- When a sugarcane story states that cane production faces water-resource pressure, water constraints, water scarcity, irrigation shortage, semi-arid climate pressure, or similar wording, interpret the supply path as lower yield potential, constrained cane expansion, or weaker future cane availability.
- The impact judgment should be `利多` because future sugar-material supply may decline or become less stable.
- Do not weaken this to `影响有限` merely because the article is framed as climate/water risk or does not name one of the usual core cane provinces, as long as the story is about sugarcane production.

Always exclude medical, nutrition, and health content:

- blood sugar, blood glucose, glucose, diabetes, diabetic, insulin, glycemic, hyperglycemia, hypoglycemia, glucose monitoring, diabetes treatment;
- 血糖、血糖控制、糖尿病、胰岛素、降糖药、高血糖、低血糖、血糖仪、连续血糖监测、升糖指数、控糖饮食、医疗健康、营养保健、减肥和疾病风险.

Also exclude non-industry uses of `sugar`: games, novels, books, films, music, recipes, desserts, restaurant marketing, lifestyle, nutrition, weight loss, or ordinary consumer health stories.

Do not accept an item only because the title contains `sugar`. Judge from context whether the story is about the sugar industry or human blood sugar/consumer sugar.

## Thailand Weather Rule

After ordinary Thailand sugar-news discovery, run a separate Thailand main cane-area rainfall check. This check is required even when no media outlet publishes a sugar-weather story.

The daily pipeline must execute the Thailand rainfall check after verified news is loaded or RSS autogeneration is complete, and before normalization, Excel writing, dashboard JSON writing, and deployment. This is mandatory even when a curated `data/verified_news/.../sugar_news_YYYY-MM-DD.json` file already exists. Do not limit the check to the missing-verified-news autogeneration branch.

If the target report has no Thailand ordinary news item, a valid Thailand cane-area rainfall forecast must still create one Thailand weather item. If a Thailand weather item already exists, keep it and do not duplicate it.

Major Thai cane areas include Udon Thani, Khon Kaen, Nakhon Ratchasima, Chaiyaphum, Kalasin, Loei, Nakhon Sawan, Kamphaeng Phet, Sukhothai, Phitsanulok, Kanchanaburi, Lopburi, Suphanburi, Chai Nat, Sa Kaeo, and Chonburi.

Use the Thai Meteorological Department daily forecast first: https://tmd.go.th/en/forecast/daily. If the official forecast only gives regional information, map it to the Thailand cane belt instead of dropping the item: Northeastern maps to Udon Thani, Khon Kaen, Nakhon Ratchasima, Chaiyaphum, Kalasin, and Loei; Northern maps to Nakhon Sawan, Kamphaeng Phet, Sukhothai, and Phitsanulok; Central maps to Kanchanaburi, Lopburi, Suphanburi, and Chai Nat; Eastern maps to Sa Kaeo and Chonburi. Public weather forecasts may supplement specific cane provinces, but source links must be kept and rainfall probability or volume must not be invented.

If TMD access fails during the daily run, use the public Open-Meteo forecast API as a no-key fallback for the configured Thai cane-area monitoring points. The Open-Meteo fallback may state forecast period, available forecast days, rainy cane regions, and forecast precipitation totals from the API response; it must not invent rainfall probability or rainfall volume.

If both TMD and Open-Meteo access fail, the pipeline may recover a previously verified Thailand weather item from recent Sugar News verified files only when that item's `published_date_local` exactly equals the target report date and the item is still a Thailand cane-area rainfall forecast. Never reuse stale Thailand weather from a different report date.

During the cane growing stage, strong rain, heavy rain, thunderstorms, showers, forecast heavy rain, forecast strong rain, forecast thunderstorms, wider rainfall coverage, higher rainfall probability, future rainfall increase, continuous rain, drought relief, or soil-moisture improvement in any major cane province must be judged as `利空`.

Do not weaken this judgment with wording such as `幅度有限`, `影响有限`, `小幅利空`, or `中性` merely because rain is local, short-lived, forecast-only, or covers only part of the cane belt.

Use this standard logic: 甘蔗生长阶段的降雨有利于补充土壤水分、改善墒情并促进甘蔗生长和单产形成，从而增加未来甘蔗及食糖供应预期，因此利空糖价。

Only confirmed flood, lodging, waterlogging, crop damage, or expected cane loss may change the judgment to bullish.

## 中国糖业新闻每日重点监测

The daily task must actively search China sugar-industry news as its own priority country. Do not rely on other-country searches to passively discover China items.

Daily China monitoring must cover:

- domestic sugar production, sales, sales ratio, and industrial inventory;
- cane and beet planted area, crop condition, yield, sugar content, and planting intention;
- Guangxi, Yunnan, Guangdong, and Hainan cane regions;
- Inner Mongolia, Xinjiang, Heilongjiang, and other beet regions;
- sugar, raw sugar, syrup, and white-sugar premix imports;
- import origin, arrival volume, import cost, and refinery operating rates;
- domestic white-sugar spot prices, Zhengzhou sugar futures, basis, and regional quotations;
- state reserve sugar, import quotas, tariffs, regulation, supervision, and industry policy;
- mill opening, closing, maintenance, capacity, and operating changes;
- cane purchase prices, planting subsidies, and farmer planting willingness;
- main sugar-crop region rainfall, heavy rain, drought, flooding, typhoon, heat, and frost;
- international events that directly affect China sugar supply, imports, inventories, or prices.

Daily China search keywords must combine at least these themes, not just one generic `中国糖业新闻` query:

- 中国 + 白糖;
- 中国 + 食糖;
- 中国 + 甘蔗;
- 中国 + 甜菜糖;
- 广西 + 糖业 / 甘蔗;
- 云南 + 糖业 / 甘蔗;
- 食糖进口 / 原糖进口;
- 糖浆进口 / 预混粉进口;
- 食糖库存 / 产销率;
- 糖厂开榨 / 收榨;
- 甘蔗收购价;
- 郑糖 / 白糖现货;
- 糖料产区 + 降雨 / 暴雨 / 干旱 / 台风.

Priority China sources:

1. China Sugar Association;
2. Ministry of Agriculture and Rural Affairs and CASDE China sugar supply-demand reports;
3. General Administration of Customs;
4. National Bureau of Statistics;
5. NDRC, Ministry of Commerce, and relevant government departments;
6. Guangxi, Yunnan, and other producing-region agriculture, weather, and sugar-industry authorities;
7. YNTW, msweet, and other professional sugar-industry media;
8. Zhengzhou Commodity Exchange;
9. reputable futures companies, research institutions, and sugar-mill announcements.

Deduplicate professional-media reposts of the same China story. Prefer the original authority or the source closest to the original data.

For China weather news, do not apply the Thailand growing-stage rainfall rule mechanically. If heavy rain, flooding, hail, strong wind, waterlogging, lodging, or field-management disruption is forecast or confirmed in a China cane region, judge by the damage path; when future cane availability may decline or become less stable, the impact should be bullish.

Pre-publication logs must show that China search was completed, including query terms, sources, and candidate counts. If no important China item is found, record `China sugar monitoring completed; no publishable item found` in the backend log instead of silently omitting China. Before publishing, verify that any retained China item exists in verified JSON, Excel/dashboard output, and production artifacts.

## 巴西糖价与库存每日刷新

The daily Sugar News task must refresh the `巴西糖价与库存` dashboard before writing the dashboard JSON and before Vercel production deployment. The normal 06:00 Beijing-time GitHub Actions run must call `scripts/sugar_news_pipeline.py` without `--skip-metric-refresh`, so `refresh_brazil_metrics(date_text)` executes every day.

The Brazil dashboard refresh covers the existing dynamic modules only:

- Brazil sugar import premium/discount;
- Brazil sugar stock;
- Brazil hydrous ethanol stock.

The refresh must keep using the existing fixed sources, parsing rules, data-date rules, and calculation logic. Do not use deployment time, crawl time, or Vercel build time as the data date. If a source has not published a newer report, keep the latest successful data and preserve its true data date.

After Brazil metrics refresh, the generated dashboard JSON, Excel/report artifacts, Git commit, GitHub push, and Vercel production deployment must all use the same refreshed Brazil metric snapshot. The task log must record `brazil_metrics_refresh` status. If the normal daily run skips Brazil metrics, treat it as a pipeline error; `--skip-metric-refresh` is allowed only for explicit news-only repairs requested by the user.

## Pre-Publish Quality Checks

Before writing Excel or dashboard JSON, the pipeline must:

1. Check that each summary has 2-3 Chinese sentences.
2. Reject summaries beginning with ordinary publication-date/source formulas.
3. Remove meaningless repeated publication-date wording.
4. Detect medical/health sugar terms and exclude those items.
5. Detect non-industry uses of `sugar` and exclude those items.
6. Infer title and body country entities and compare them with `country_group` and `country`.
7. Automatically reclassify clear country mismatches.
8. Require concrete country labels for `其他国家` items.
9. Detect duplicate URLs, titles, or dedupe keys.
10. Stop publication when a violation cannot be automatically fixed, preserving the previous correct production page.

Regression tests must cover Indonesia not going to Brazil, India media reporting Cameroon going to Cameroon, medical blood-sugar exclusion, valid Brazil cane/sugar/ethanol acceptance, publication-date removal with key date retention, 2-3 sentence summaries, and Brazil/India metric value placement under the `绝对值` column.

## Output Consistency

Excel, structured verified JSON, dashboard report JSON, local preview, and Vercel production must be generated from the same validated item list.

Use:

```powershell
python scripts\sugar_news_pipeline.py --date YYYY-MM-DD --offline-only
```

For news-only repair without refreshing price and stock metrics:

```powershell
python scripts\sugar_news_pipeline.py --date YYYY-MM-DD --offline-only --skip-metric-refresh
```

Do not publish when validation fails.
