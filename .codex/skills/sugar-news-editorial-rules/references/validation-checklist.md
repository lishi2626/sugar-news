# Validation Checklist

Use this checklist after editing Sugar News news content or editorial rules.

## Content

- Every retained news item is 2-3 concise Chinese sentences.
- No item starts with mechanical publication-date wording such as `今日发布`, `今天消息`, or `X月X日报道`.
- Critical dates are retained only when relevant to policy, quotas, seasons, factory operations, statistics, or weather coverage.
- Key figures, units, policy terms, source names, and source links are preserved.
- Impact labels and logic are consistent with the item facts.

## Classification

- Brazil, India, Thailand, and China sections contain only core-country items.
- Other countries are labeled with the concrete country or `全球`, never a generic `其他国家`.
- No story is duplicated across country sections.
- Import/export stories are assigned by the main policy subject and affected market.

## Thailand Weather

- Thailand news processing includes a separate main cane-area rainfall check after ordinary Thailand sugar-news discovery.
- The check covers recent rainfall, current weather, next 7 days of forecasts, rain increase, heavy rain warnings, and low-rain/high-temperature/drought risk when sources provide them.
- Thai Meteorological Department daily forecast is checked first: https://tmd.go.th/en/forecast/daily.
- If valid rainfall exists in Udon Thani, Khon Kaen, Nakhon Ratchasima, Chaiyaphum, Kalasin, Loei, Nakhon Sawan, Kamphaeng Phet, Sukhothai, Phitsanulok, Kanchanaburi, Lopburi, Suphanburi, Chai Nat, Sa Kaeo, or Chonburi, Thailand has one weather item.
- Rainfall probability or rainfall volume is shown only when the source clearly provides it.
- The same weather process is not duplicated.

## Filtering

- No blood sugar, glucose, diabetes, insulin, glycemic, medical, nutrition, or health-consumer item remains.
- No game, novel, entertainment, recipe, dessert, restaurant, or ordinary consumer story remains because of a `sugar` word.
- Ethanol stories have a direct cane/molasses/sugar-syrup/sugar-allocation link.

## Data Integrity

- `public/sugar-news/data/reports/YYYY/MM/YYYY-MM-DD.json`, `data/verified_news/...json`, Excel, `index.json`, and `status.json` counts match.
- `brazilMetrics`, `indiaMetrics`, weather, price, stock, and other dashboard data blocks are unchanged unless explicitly requested.
- Run:

```powershell
.\.venv\Scripts\python.exe scripts\verify_sugar_news_dashboard.py --date YYYY-MM-DD
```

- If rules or code changed, also run:

```powershell
.\.venv\Scripts\python.exe scripts\test_sugar_news_regressions.py
```
