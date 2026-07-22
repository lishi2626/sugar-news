# Validation Checklist

Before claiming the Brazil dashboard data workflow is complete, verify all items that apply.

## Static Source Rules

- 巴西进口升贴水 uses Hisugar "食糖进口成本及利润估算表".
- 巴西食糖库存 uses MAPA sugar production and stocks / report family `009`.
- 巴西含水乙醇库存 uses MAPA ethanol report, hydrous ethanol `ESTOQUE (m3)` / `E.Fisico` national total.
- Current values, report dates, article IDs, source links, and changes are not hard-coded as defaults.
- Example values are marked validation-only and cannot be returned as fallback data.

## Dynamic Date Discovery

- Latest data is chosen by internal report data date.
- Sugar stock previous period is the immediately preceding same-season report.
- Hydrous ethanol previous period is the immediately preceding same-season report.
- Year-on-year uses previous-season same month/day where available.
- Non-exact year-on-year dates are never silently substituted.

## Field and Unit Checks

- Import premium is in `美分/磅`.
- Sugar stock is stock, not production, sales, exports, or another field.
- Sugar stock tonnes are divided by 10,000 exactly once and displayed as `万吨`.
- Hydrous ethanol is hydrous, not anhydrous.
- Hydrous ethanol uses national total, not regional subtotal.
- Hydrous ethanol cubic metres are divided by 10,000 exactly once and displayed as `万立方米`.

## Failure Handling

- Source page failure does not fabricate data.
- Report download failure does not fabricate data.
- Missing previous period leaves only half-month change unavailable.
- Missing last-year period leaves only year-on-year unavailable.
- Stale fallback values are marked with true last successful data date and failure reason.
- New data overwrites old dashboard data only after source, date, unit, and field checks pass.

## Suggested Runtime Tests

When scraper code is changed, test at least:

- normal update;
- missing previous period;
- missing last-year period;
- comparison base equal to zero;
- negative import premium;
- unit conversion;
- page structure change or missing field.
