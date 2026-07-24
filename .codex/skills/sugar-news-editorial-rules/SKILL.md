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

Always exclude medical, nutrition, and health content:

- blood sugar, blood glucose, glucose, diabetes, diabetic, insulin, glycemic, hyperglycemia, hypoglycemia, glucose monitoring, diabetes treatment;
- 血糖、血糖控制、糖尿病、胰岛素、降糖药、高血糖、低血糖、血糖仪、连续血糖监测、升糖指数、控糖饮食、医疗健康、营养保健、减肥和疾病风险.

Also exclude non-industry uses of `sugar`: games, novels, books, films, music, recipes, desserts, restaurant marketing, lifestyle, nutrition, weight loss, or ordinary consumer health stories.

Do not accept an item only because the title contains `sugar`. Judge from context whether the story is about the sugar industry or human blood sugar/consumer sugar.

## Thailand Weather Rule

After ordinary Thailand sugar-news discovery, run a separate Thailand main cane-area rainfall check. This check is required even when no media outlet publishes a sugar-weather story.

Major Thai cane areas include Udon Thani, Khon Kaen, Nakhon Ratchasima, Chaiyaphum, Kalasin, Loei, Nakhon Sawan, Kamphaeng Phet, Sukhothai, Phitsanulok, Kanchanaburi, Lopburi, Suphanburi, Chai Nat, Sa Kaeo, and Chonburi.

Use the Thai Meteorological Department daily forecast first: https://tmd.go.th/en/forecast/daily. If it only gives regional information, public weather forecasts may supplement specific cane provinces, but source links must be kept and rainfall probability or volume must not be invented.

During the cane growing stage, strong rain, heavy rain, thunderstorms, showers, forecast heavy rain, forecast strong rain, forecast thunderstorms, wider rainfall coverage, higher rainfall probability, future rainfall increase, continuous rain, drought relief, or soil-moisture improvement in any major cane province must be judged as `利空`.

Do not weaken this judgment with wording such as `幅度有限`, `影响有限`, `小幅利空`, or `中性` merely because rain is local, short-lived, forecast-only, or covers only part of the cane belt.

Use this standard logic: 甘蔗生长阶段的降雨有利于补充土壤水分、改善墒情并促进甘蔗生长和单产形成，从而增加未来甘蔗及食糖供应预期，因此利空糖价。

Only confirmed flood, lodging, waterlogging, crop damage, or expected cane loss may change the judgment to bullish.

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
