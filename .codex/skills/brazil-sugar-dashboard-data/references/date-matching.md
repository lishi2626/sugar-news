# Date Matching and Calculations

## Global Date Rules

- The latest period must be selected by the report's internal statistical date.
- Do not select latest data from filename, page order, crawl time, deployment time, or page last-modified time alone.
- Persist dates as ISO `YYYY-MM-DD`.
- The UI may render dates as `YYYY年M月D日`.

## Previous Period

For Brazil sugar stock and hydrous ethanol stock, previous period means the immediately preceding report in the same season.

Examples:

- Latest sugar stock `2026-06-30` -> previous `2026-06-15`.
- Latest sugar stock `2026-07-15` -> previous `2026-06-30`.
- Latest hydrous ethanol `2026-07-01` -> previous `2026-06-16`.
- Latest hydrous ethanol `2026-07-16` -> previous `2026-07-01`.

Do not skip over a same-season report unless it is invalid and the failure is recorded.

## Year-on-Year

Year-on-year comparison should use previous-season data with the same month/day.

Examples:

- Latest sugar stock `2026-06-30` -> year-on-year `2025-06-30`.
- Latest sugar stock `2026-07-15` -> year-on-year `2025-07-15`.
- Latest hydrous ethanol `2026-07-01` -> year-on-year `2025-07-01`.
- Latest hydrous ethanol `2026-07-16` -> year-on-year `2025-07-16`.

If the exact same month/day does not exist:

- do not silently use another date;
- prefer marking year-on-year unavailable;
- if using a closest comparable date is explicitly approved, store and display the actual comparison date and mark it `非完全同期`.

## Formulas

Import premium:

```text
日涨跌绝对值 = 最新值 - 上一有效数据日值
日涨跌百分比 = (最新值 - 上一有效数据日值) / abs(上一有效数据日值) * 100%

同比绝对值 = 最新值 - 上年同期值
同比百分比 = (最新值 - 上年同期值) / abs(上年同期值) * 100%
```

If the comparison base is zero or the premium crosses zero, percent is `不可计算`; keep the absolute change.

Sugar stock:

```text
半月变化绝对值 = 最新库存 - 上一期库存
半月变化百分比 = (最新库存 - 上一期库存) / 上一期库存 * 100%

同比绝对值 = 最新库存 - 去年同期库存
同比百分比 = (最新库存 - 去年同期库存) / 去年同期库存 * 100%
```

Hydrous ethanol stock:

```text
半月变化绝对值 = 最新库存 - 上一期库存
半月变化百分比 = (最新库存 - 上一期库存) / 上一期库存 * 100%

同比绝对值 = 最新库存 - 去年同期库存
同比百分比 = (最新库存 - 去年同期库存) / 去年同期库存 * 100%
```

## Missing Comparison Data

If a comparison period is missing, leave only that comparison's absolute and percent fields unavailable. Do not suppress a valid current value.
