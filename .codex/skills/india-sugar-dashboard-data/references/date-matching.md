# India Sugar Dashboard Date Matching

## Current Date

Use the source record's own data date:

- wholesale/retail: the ChiniMandi table `Date` column;
- Uttar Pradesh ex-mill: the `Ex-mill Sugar Prices as on ...` date inside the report.

Never use current webpage date, scrape time, Vercel deployment time, article modified time, or a requested target date as the data date unless it matches the source record date.

If the requested date has no valid source record, search backward until the latest valid source record is found and display that true data date.

## Previous Valid Day

Previous-day comparison uses the immediately preceding valid source record before the current data date:

- skip weekends, holidays, missing articles, and missing table rows;
- do not assume natural yesterday;
- do not infer previous values from article prose;
- store `previous_date` / `previousDataDate` and previous source URL when applicable.

Formulas:

```text
daily_change_absolute = current_value - previous_value
daily_change_percent = daily_change_absolute / previous_value * 100
```

For Uttar Pradesh ex-mill, `current_value` and `previous_value` are range midpoints.

## Year-On-Year

Prefer the same month/day in the prior year. If that source record is absent, use the nearest prior valid comparable source record.

Rules:

- the price type, unit, grade, GST basis, and city sample/range basis must match;
- never use annual average, monthly average, news summary, retail, wholesale, spot, or other-state values as substitute;
- expose the actual `yoy_comparison_date` / `previousYearDate`;
- set `yoy_exact_date_match` to `false` when the comparison date differs from the prior-year same month/day.

Formulas:

```text
yoy_change_absolute = current_value - yoy_value
yoy_change_percent = yoy_change_absolute / yoy_value * 100
```

If no comparable year-on-year source record exists, show `暂无同比数据` and leave the numeric comparison fields null.

## Precision

- Wholesale and retail display values, absolute changes, and percentages to 2 decimals.
- Uttar Pradesh range bounds use source precision; midpoint and changes display to at most 2 decimals; percentages display to 2 decimals.
- Calculate from unrounded raw values, then round only for output.
