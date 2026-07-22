# India Sugar Dashboard Output Schema

Store enough raw and normalized data to reproduce the dashboard and audit comparisons. Keep legacy fields consumed by the current frontend until all callers are migrated.

## Wholesale

```json
{
  "indicator": "india_wholesale_price",
  "value": null,
  "price_inr_per_quintal": null,
  "price_inr_per_kg": null,
  "unit": "卢比/公担",
  "raw_unit": "₹/quintal",
  "data_date": null,
  "previous_data_date": null,
  "previous_value": null,
  "change_value": null,
  "change_percent": null,
  "previous_year_date": null,
  "previous_year_value": null,
  "year_on_year_change": null,
  "year_on_year_change_percent": null,
  "price_basis": "ChiniMandi城市样本均价，含GST",
  "cities_used": [],
  "city_count": null,
  "city_prices": {},
  "raw_city_prices": {},
  "includes_gst": true,
  "source_name": "ChiniMandi",
  "source_url": "https://www.chinimandi.com/wholesale-sugar-prices/",
  "daily_market_update_url": "https://www.chinimandi.com/english-news/daily-sugar-market-update/",
  "fetched_at": null,
  "status": null
}
```

## Retail

```json
{
  "indicator": "india_retail_price",
  "value": null,
  "price_inr_per_kg": null,
  "unit": "卢比/公斤",
  "raw_unit": "₹/kg",
  "data_date": null,
  "previous_data_date": null,
  "previous_value": null,
  "change_value": null,
  "change_percent": null,
  "previous_year_date": null,
  "previous_year_value": null,
  "year_on_year_change": null,
  "year_on_year_change_percent": null,
  "price_basis": "ChiniMandi城市样本均价，含GST",
  "cities_used": [],
  "city_count": null,
  "city_prices": {},
  "raw_city_prices": {},
  "includes_gst": true,
  "source_name": "ChiniMandi",
  "source_url": "https://www.chinimandi.com/retail-prices/",
  "daily_market_update_url": "https://www.chinimandi.com/english-news/daily-sugar-market-update/",
  "fetched_at": null,
  "status": null
}
```

## Uttar Pradesh Ex-Mill

```json
{
  "indicator": "up_ex_mill_price",
  "display_range": null,
  "raw_range": null,
  "low": null,
  "high": null,
  "midpoint": null,
  "currency": "INR",
  "unit": "卢比/公担",
  "raw_unit": "₹/quintal",
  "grade": "M/30",
  "region": "Uttar Pradesh",
  "quote_type": "ex-mill",
  "includes_gst": false,
  "gst_status": "excluding GST",
  "data_date": null,
  "daily_change_absolute": null,
  "daily_change_percent": null,
  "previous_date": null,
  "previous_low": null,
  "previous_high": null,
  "previous_midpoint": null,
  "yoy_change_absolute": null,
  "yoy_change_percent": null,
  "yoy_comparison_date": null,
  "yoy_low": null,
  "yoy_high": null,
  "yoy_midpoint": null,
  "yoy_exact_date_match": null,
  "source_name": "ChiniMandi — Daily Sugar Market Update",
  "source_url": null,
  "previous_source_url": null,
  "yoy_source_url": null,
  "fetched_at": null,
  "status": null
}
```

## Frontend Contract

The three cards must display:

- `取值`
- `数据日期`
- `日涨跌`
- `同比`
- `绝对值`
- `（%）`

Use compact Brazil-style tables. Main card values remain dynamic. Source footer/detail should expose source name, source link, data date, previous valid date, year-on-year comparison date, fetched time, GST basis, and city sample or midpoint basis.
