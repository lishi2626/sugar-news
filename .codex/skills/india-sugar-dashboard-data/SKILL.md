---
name: india-sugar-dashboard-data
description: Maintain and validate the Sugar News "印度糖价" dashboard data rules. Use when updating, fixing, validating, or explaining India domestic wholesale price, India domestic retail price, Uttar Pradesh M/30 ex-mill sugar price, ChiniMandi source selection, Supsystic table scraping, Daily Sugar Market Update parsing, previous valid day matching, year-on-year matching, GST basis, unit handling, stale data handling, or Sugar News India price dashboard failures.
---

# India Sugar Dashboard Data

Use this skill for the `D:\Desktop\ai\sugar-news` India price dashboard only. Keep the public dashboard dynamic: never hard-code current prices, ranges, dates, changes, source article IDs, fallback examples, or comparison values.

## Fixed Dashboard Contract

The "印度糖价" dashboard has exactly three price cards in this order:

1. 印度国内批发价
2. 印度国内零售价
3. 北方邦糖厂出厂价

The removed India carryover-stock card must not be restored. Do not modify news, Brazil dashboard data, weather, navigation, deployment config, or Sugar Daily while working on this dashboard.

## Required Sources

- 印度国内批发价: ChiniMandi wholesale sugar price table at `https://www.chinimandi.com/wholesale-sugar-prices/`.
- 印度国内零售价: ChiniMandi retail sugar price table at `https://www.chinimandi.com/retail-prices/`.
- 北方邦糖厂出厂价: ChiniMandi `Daily Sugar Market Update By Vizzie` formal daily report from `https://www.chinimandi.com/english-news/daily-sugar-market-update/`, article slug `daily-sugar-market-update-by-vizzie-DD-MM-YYYY`, table `Ex-mill Sugar Prices`, row `Uttar Pradesh`, column `M/30 [Rates per Quintal]`.

Do not substitute FCA, Google snippets, morning updates, destination-wise spot prices, city spot prices, retail prices, wholesale prices, cane SAP/FRP, minimum selling price, futures, other-state ex-mill quotes, or article prose about rises/falls.

## Workflow

1. Read [references/source-rules.md](references/source-rules.md) before changing scraper source selection or field parsing.
2. Read [references/date-matching.md](references/date-matching.md) before computing previous-day or year-on-year values.
3. Read [references/output-schema.md](references/output-schema.md) before changing JSON fields consumed by Sugar News.
4. Read [references/validation-checklist.md](references/validation-checklist.md) before claiming completion.
5. Update or fix the scraper so it dynamically discovers valid source records by the source table/report's own data date, persists history, and computes changes from raw stored values.
6. If any source or comparison period fails, preserve the last successful data, mark the failure, and never fabricate a replacement.

## Calculation Rules

- Wholesale and retail current values use the fixed ChiniMandi city sample. If a city value is a range, use the range midpoint before averaging.
- Wholesale and retail current/previous/year-on-year values must use the same city set: the common cities present in all compared periods.
- Uttar Pradesh ex-mill changes use the M/30 quote-range midpoint: `(low + high) / 2`. Never compare only lows, only highs, or the range width.
- Previous-day comparison means the immediately preceding valid source record before the current data date, not natural yesterday.
- Year-on-year comparison prefers the same month/day in the prior year; if absent, use the nearest prior valid comparable source record and expose the actual date.
- Percent changes divide by the comparison base. If the base is missing or zero, keep the absolute value if known and mark the percent unavailable.

## Failure Rules

When pages fail, table AJAX changes, reports are missing, units look wrong, dates do not match, or comparison periods are missing:

- do not invent data;
- do not silently use another source or another date;
- do not overwrite a successful historical value with `0`, examples, or placeholders;
- mark the failed fetch and keep the last successful value with its real data date;
- set only the missing comparison field to unavailable when the latest value is valid.

## Static Validation

Run the bundled static validator after editing this skill:

```powershell
.\.venv\Scripts\python.exe .codex\skills\india-sugar-dashboard-data\scripts\validate_skill_static.py .codex\skills\india-sugar-dashboard-data
```

Then run the standard Skill Creator validator:

```powershell
.\.venv\Scripts\python.exe C:\Users\zsqh\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\india-sugar-dashboard-data
```
