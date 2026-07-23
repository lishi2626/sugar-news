---
name: sugar-news-editorial-rules
description: Maintain and validate Sugar News article editing rules. Use when revising, generating, validating, or debugging Sugar News news summaries, country classification, other-country labeling, source preservation, medical/non-industry sugar filtering, Thai cane-area rainfall checks, daily report JSON/Excel consistency, or newsroom-style Chinese sugar industry summaries.
---

# Sugar News Editorial Rules

## Scope

Use this skill only for the Sugar News news section. Do not modify price, stock, metric history, deployment configuration, dashboard layout, or Sugar Daily unless the user explicitly asks.

Primary files usually involved:

- `data/verified_news/YYYY/MM/sugar_news_YYYY-MM-DD.json`
- `public/sugar-news/data/reports/YYYY/MM/YYYY-MM-DD.json`
- `reports/YYYY/MM/Sugar News YYYY-MM-DD.xlsx`
- `public/sugar-news/data/index.json`
- `public/sugar-news/data/status.json`
- `scripts/sugar_news_pipeline.py`
- `prompts/sugar_news_prompt.md`
- `AGENTS.md`

## Workflow

1. Identify the target report date from `public/sugar-news/data/index.json` or the user request.
2. Read the target report JSON and the previous day's report for style reference.
3. Work from already generated items and existing source links unless the user asks for new retrieval. If country, relevance, or weather validity is uncertain, open only the existing source link or the explicitly requested official weather source.
4. For each item, determine whether it is direct sugar-industry news, assign the core country, rewrite the summary, and preserve source metadata.
5. For Thailand, after ordinary sugar-news review, separately check the Thai main cane-area weather rule. If valid rainfall exists in major cane provinces, keep one Thailand weather item.
6. Update dashboard JSON, verified news JSON, Excel output, `index.json`, and `status.json` counts together.
7. Validate with `scripts/verify_sugar_news_dashboard.py --date YYYY-MM-DD`; run `scripts/test_sugar_news_regressions.py` when rules or code changed.
8. Compare metric blocks before/after when editing an existing report: `brazilMetrics`, `indiaMetrics`, weather, and other dashboard data blocks must remain unchanged unless explicitly requested.

## Summary Style

Write each news summary in 2-3 concise Chinese sentences using sugar-industry research language.

Each item must cover:

- what happened;
- key policy, data, capacity, production, trade, weather, or cost information;
- the impact path on cane/beet, sugar production, inventories, imports/exports, ethanol diversion, costs, or sugar prices.

Do not mechanically translate English titles. Do not add facts or numbers not present in the source. Remove promotional phrasing, generic background, repeated publication dates, and filler.

Avoid repeated lead-ins such as `今日发布`, `今天消息`, `X月X日报道`, `截至今天`, or ordinary publication dates. Keep dates only when they are market-relevant: policy windows, quota months, crushing periods, statistical cutoff dates, factory opening/closure timing, export-ban periods, or forecast coverage.

Dashboard impact labels should normally be `利多`, `利空`, or `中性`. For Thailand main cane-area rainfall during the growing stage, use `利空`; do not weaken the judgment because rainfall is local, short-lived, forecast-only, or covers only part of the cane belt.

## Country Assignment

Assign by the core event location and main affected sugar market, not by media source, language, article host, title keyword frequency, or company headquarters alone.

Rules:

- India government, parliament, sugar mills, cane dues, cane disease, stock policy, hoarding control, and domestic sugar price policy belong to `印度`.
- Brazil government, mills, cane, ethanol, sugar output, or Brazil sugar/ethanol market data belong to `巴西`.
- Thailand policy, cane production, cane-area weather, and mill news belong to `泰国`.
- China policy, production, imports, and price news belong to `中国`.
- Indonesia, Pakistan, Philippines, Vietnam, Russia, Cameroon, Fiji, UK, US, Australia, Poland, Kenya, and similar items belong under their actual country name, not a generic `其他国家`.
- Global sugar-price, crude-oil, futures, or multi-country supply-demand items without one clear national subject belong to `全球`.

For two-country trade stories, use one main country:

- import policy, import volume, and domestic supply impact -> importing country;
- export quota, export sale, or production allocation -> exporting country;
- if no single country is primary -> `全球`.

Never duplicate the same story in two country sections.

## Relevance Filtering

Keep only direct sugar-industry items:

- cane or beet planting, yields, disease, harvest, weather, or disasters;
- sugar production, crushing, factory opening/closure, processing capacity, or labor disruptions;
- cane dues, cane prices, sugar policy, quotas, stock limits, hoarding controls, subsidies, taxes, or regulation;
- sugar inventories, wholesale/retail/ex-mill prices, futures, imports, exports, tariffs, or trade flows;
- cane/molasses/sugar-syrup ethanol and sugar-ethanol allocation.

Always exclude medical/health content:

- blood sugar, blood glucose, glucose, diabetes, diabetic, insulin, glycemic, hyperglycemia, hypoglycemia, glucose monitoring, diabetes treatment;
- Chinese equivalents such as `血糖`, `糖尿病`, `胰岛素`, `降糖`, `低血糖`, `高血糖`, `血糖监测`.

Also exclude non-industry uses of `sugar`: games, novels, books, films, music, recipes, desserts, restaurant/consumer marketing, lifestyle, nutrition, weight loss, and ordinary food-health content.

Ethanol news is allowed only when tied to cane, molasses, sugar syrup, sugar self-sufficiency, distilleries using sugar feedstock, or sugar-ethanol allocation. General fuel, corn ethanol, automobile, or energy-only stories are not enough.

## Thailand Weather

Thailand news must include a fixed main cane-area rainfall check after ordinary Thailand sugar-news discovery. This check is part of daily Thailand news processing and must not depend on whether a media outlet published a sugar/weather article.

Major cane areas:

- Northeast: Udon Thani, Khon Kaen, Nakhon Ratchasima, Chaiyaphum, Kalasin, Loei.
- North: Nakhon Sawan, Kamphaeng Phet, Sukhothai, Phitsanulok.
- Central/West: Kanchanaburi, Lopburi, Suphanburi, Chai Nat.
- East: Sa Kaeo, Chonburi.

Daily checks must cover:

- the most recent complete natural-day rainfall where available;
- current-day weather;
- the next 7 days of rainfall forecasts;
- rain increase, heavy rain or storm warnings;
- continued low rainfall, high temperature, or drought risk.

Use the Thai Meteorological Department daily forecast first: https://tmd.go.th/en/forecast/daily. If it only gives regional conditions, use public weather forecasts to supplement specific cane provinces, but keep source links and never invent rainfall probability or rainfall volume.

When valid rainfall exists in major cane provinces, add one concise Thailand weather item. Summarize affected provinces, forecast coverage time, rainfall type, probability or rainfall amount only if the source provides it, and the impact on cane growth and sugar prices. Merge the same weather process into one item.

Impact rules during the cane growing stage:

- strong rain, heavy rain, thunderstorms, showers, forecast heavy rain, forecast strong rain, forecast thunderstorms, wider rainfall coverage, higher rainfall probability, future rainfall increase, continuous rain, drought relief, or soil-moisture improvement in any major cane province -> `利空`;
- drought, continued low rainfall, or worsening heat stress -> `利多` or `偏多糖价`;
- confirmed flood, lodging, waterlogging, crop damage, or expected cane loss -> judge from actual damage, often `利多`;
- rain outside major cane provinces -> `影响有限` or omit.

Do not add weakening language for Thailand main cane-area rain during the growing stage.

Standard logic: 甘蔗生长阶段的降雨有利于补充土壤水分、改善墒情并促进甘蔗生长和单产形成，从而增加未来甘蔗及食糖供应预期，因此利空糖价。

## Validation

Read [references/validation-checklist.md](references/validation-checklist.md) before final reporting or deployment.
