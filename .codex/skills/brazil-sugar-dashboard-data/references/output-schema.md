# Output Schema

Use this canonical shape for scraper-level output. Sugar News frontend or pipeline adapters may map names into existing dashboard payload fields, but must preserve source, dates, raw values, converted values, status, and comparison dates.

```json
{
  "brazil_import_premium": {
    "value": null,
    "unit": "美分/磅",
    "data_date": null,
    "daily_change_absolute": null,
    "daily_change_percent": null,
    "yoy_change_absolute": null,
    "yoy_change_percent": null,
    "comparison_dates": {
      "previous": null,
      "last_year": null
    },
    "source_name": "泛糖科技",
    "source_url": null,
    "latest_report_url": null,
    "previous_report_url": null,
    "last_year_report_url": null,
    "raw_value": null,
    "raw_unit": null,
    "conversion": null,
    "fetched_at": null,
    "fetch_status": null,
    "error": null
  },
  "brazil_sugar_stock": {
    "value": null,
    "unit": "万吨",
    "data_date": null,
    "half_month_change_absolute": null,
    "half_month_change_percent": null,
    "yoy_change_absolute": null,
    "yoy_change_percent": null,
    "comparison_dates": {
      "previous": null,
      "last_year": null
    },
    "source_name": "巴西农业和畜牧业部（MAPA）",
    "source_url": null,
    "latest_report_url": null,
    "previous_report_url": null,
    "last_year_report_url": null,
    "raw_value": null,
    "raw_unit": null,
    "conversion": null,
    "fetched_at": null,
    "fetch_status": null,
    "error": null
  },
  "brazil_hydrous_ethanol_stock": {
    "value": null,
    "unit": "万立方米",
    "data_date": null,
    "half_month_change_absolute": null,
    "half_month_change_percent": null,
    "yoy_change_absolute": null,
    "yoy_change_percent": null,
    "comparison_dates": {
      "previous": null,
      "last_year": null
    },
    "source_name": "巴西农业和畜牧业部（MAPA）官方乙醇报表",
    "source_url": null,
    "latest_report_url": null,
    "previous_report_url": null,
    "last_year_report_url": null,
    "raw_value": null,
    "raw_unit": null,
    "conversion": null,
    "fetched_at": null,
    "fetch_status": null,
    "error": null
  }
}
```

## Adapter Requirements

The Sugar News dashboard may expose existing field names such as:

- `sugarPremium.premiumDiscountCentsPerLb`
- `sugarPremium.dailyChange`
- `sugarStock.stockValue`
- `sugarStock.halfMonthChange`
- `ethanolStock.totalEthanolStock`
- `ethanolStock.stockTenThousandCubicMetres`

Adapters must still preserve:

- true data date, not deployment date;
- previous comparison date;
- last-year comparison date;
- source name and clickable source URL;
- raw source value and unit;
- conversion note;
- fetch status and error message.
