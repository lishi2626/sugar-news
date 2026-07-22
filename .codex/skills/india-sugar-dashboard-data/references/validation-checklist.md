# India Sugar Dashboard Validation Checklist

Before claiming completion, verify:

## Scope

- Only India price dashboard code/data changed for the requested card(s).
- No news, Brazil dashboard, weather, deployment config, Sugar Daily, or navigation changes were introduced.
- The removed India carryover-stock card remains absent from the page.

## Wholesale

- Source is `ChiniMandi`.
- Source URL is `https://www.chinimandi.com/wholesale-sugar-prices/`.
- Data date comes from the ChiniMandi table `Date` column.
- The value is the fixed city-sample average, not FCA or another national average.
- City list and city count are saved.
- Includes GST is true.
- Previous-day and year-on-year comparisons use the same source, unit, and common city sample.

## Retail

- Source is `ChiniMandi`.
- Source URL is `https://www.chinimandi.com/retail-prices/`.
- Data date comes from the ChiniMandi table `Date` column.
- The value is the fixed city-sample average, not wholesale, ex-mill, or FCA.
- City list and city count are saved.
- Includes GST is true.
- Previous-day and year-on-year comparisons use the same source, unit, and common city sample.

## Uttar Pradesh Ex-Mill

- Source is `ChiniMandi — Daily Sugar Market Update`.
- Source URL is a `daily-sugar-market-update-by-vizzie-DD-MM-YYYY` report.
- The parsed field is `Ex-mill Sugar Prices -> Uttar Pradesh -> M/30`.
- Unit is `卢比/公担`; raw unit is `₹/quintal`.
- GST basis is excluding GST.
- The display value is the complete range, not just low/high/midpoint.
- Midpoint equals `(low + high) / 2`.
- Daily and year-on-year changes use midpoint comparisons.
- Previous and year-on-year source URLs are saved.
- The logic did not use Muzaffarnagar destination spot prices, city spot prices, article prose, or another state's quote.

## Failure Handling

- Failed fetches do not overwrite last successful values with zero or examples.
- Missing previous/yoy comparison only nulls the affected comparison fields.
- Data date and fetched time remain distinct.
- Production code has no hard-coded current prices, dates, changes, source slugs, or examples.

## Commands

Run:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\python.exe scripts\verify_sugar_news_dashboard.py --date YYYY-MM-DD
.\.venv\Scripts\python.exe .codex\skills\india-sugar-dashboard-data\scripts\validate_skill_static.py .codex\skills\india-sugar-dashboard-data
.\.venv\Scripts\python.exe C:\Users\zsqh\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\india-sugar-dashboard-data
```

If production is deployed, verify the Vercel JSON payload uses the same values, source names, dates, and links as local data.
