---
name: brazil-sugar-dashboard-data
description: Maintain and validate the Sugar News "巴西糖价与库存" dashboard data rules. Use when updating, fixing, validating, or explaining Brazil import premium, Brazil sugar stock, hydrous ethanol stock, daily change, half-month change, year-on-year matching, MAPA/Hisugar source selection, unit conversion, stale data handling, or Sugar News Brazil dashboard failures.
---

# Brazil Sugar Dashboard Data

Use this skill for the `D:\Desktop\ai\sugar-news` Brazil dashboard only. Keep the public dashboard dynamic: never hard-code current prices, stock values, dates, changes, source article IDs, or fallback example values.

## Fixed Dashboard Contract

The "巴西糖价与库存" dashboard has exactly three cards in this order:

1. 巴西进口升贴水
2. 巴西食糖库存
3. 巴西含水乙醇库存

Each card must expose current value, data date, absolute change, percent change, year-on-year absolute change, year-on-year percent change, source name, and source URL. Read [references/output-schema.md](references/output-schema.md) before changing payload fields.

## Required Sources

- 巴西进口升贴水: 泛糖科技 "食糖进口成本及利润估算表" list at `https://www.hisugar.com/home/newListMore?parentId=39&level=3&childId=144&menuTap1`.
- 巴西食糖库存: MAPA production page at `https://www.gov.br/agricultura/pt-br/assuntos/sustentabilidade/agroenergia/producao`, report family 009 / sugar production and stocks.
- 巴西含水乙醇库存: MAPA ethanol tracking page at `https://www.gov.br/agricultura/pt-br/assuntos/sustentabilidade/agroenergia/acompanhamento-da-producao-sucroalcooleira`, hydrous ethanol `ESTOQUE (m3)` / `E.Fisico` national total.

Do not substitute Platts, search snippets, reposted values, model estimates, ANP-only labels without report evidence, production, sales, export, regional subtotal, or page last-modified dates.

## Workflow

1. Read [references/source-rules.md](references/source-rules.md) for source-specific navigation and field rules.
2. Read [references/date-matching.md](references/date-matching.md) before computing previous-period or year-on-year values.
3. Read [references/output-schema.md](references/output-schema.md) before changing JSON fields consumed by Sugar News.
4. Read [references/validation-checklist.md](references/validation-checklist.md) before claiming completion.
5. Update or fix the scraper so it dynamically discovers the newest report by the report's internal data date, then persists history and computes changes from stored/raw values.
6. If any source or comparison period fails, preserve the last successful data, mark the failure, and never fabricate a replacement.

## Calculation Rules

- Import premium daily change: latest value minus previous valid Hisugar value.
- Import premium year-on-year: latest value minus same-source last-year comparable value.
- Stock half-month changes: latest stock minus immediately preceding report in the same season.
- Stock year-on-year changes: latest stock minus previous-season report with the same month/day.
- Percent changes use the comparison base. For import premium, divide by the absolute base value. If the base is zero or the premium crosses zero, show percent as not calculable while keeping absolute change.
- Convert tonnes to 万吨 by dividing by 10,000. Convert cubic metres to 万立方米 by dividing by 10,000. Store raw values and converted values to prevent double conversion.

## Failure Rules

When pages fail, downloads fail, fields move, units look wrong, dates do not match, or comparison periods are missing:

- do not invent data;
- do not silently use another source or another date;
- do not overwrite a successful historical value with `0`, examples, or placeholders;
- mark the failed fetch and keep the last successful value with its real data date;
- set only the missing comparison field to unavailable when the latest value is valid.

## Static Validation

Run the bundled static validator after editing this skill:

```powershell
.\.venv\Scripts\python.exe .codex\skills\brazil-sugar-dashboard-data\scripts\validate_skill_static.py .codex\skills\brazil-sugar-dashboard-data
```

Then run the standard Skill Creator validator:

```powershell
.\.venv\Scripts\python.exe C:\Users\zsqh\.codex\skills\.system\skill-creator\scripts\quick_validate.py .codex\skills\brazil-sugar-dashboard-data
```
