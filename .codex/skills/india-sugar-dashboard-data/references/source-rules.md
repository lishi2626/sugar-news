# India Sugar Dashboard Source Rules

## Domestic Wholesale Price

Use only `https://www.chinimandi.com/wholesale-sugar-prices/`.

The page uses a WordPress Supsystic table loaded through public AJAX:

- endpoint: `https://www.chinimandi.com/wp-admin/admin-ajax.php`
- action: `supsystic-tables`
- route module/action: `tables/getPageRows`
- table id: `6`
- nonce: extract `DTGS_NONCE_FRONTEND` from the page HTML
- columns: `Date`, `Delhi`, `Kanpur`, `Raipur`, `Mumbai`, `Ranchi`, `Kolkata`, `Guwahati`, `Hyderabad`, `Chennai`

Use the table's `Date` cell as `data_date`. Do not use page access date, article date, or deployment date.

Source notes:

- main grade: M-30 sugar;
- Hyderabad: S-30 sugar;
- prices include GST;
- display unit: `卢比/公担`;
- raw unit: ChiniMandi wholesale table convention, `₹/quintal`.

## Domestic Retail Price

Use only `https://www.chinimandi.com/retail-prices/`.

The page uses the same Supsystic AJAX pattern as wholesale:

- table id: `7`
- columns: `Date`, `Delhi`, `Kanpur`, `Raipur`, `Mumbai`, `Ranchi`, `Kolkata`, `Guwahati`, `Hyderabad`, `Chennai`

Source notes:

- main grade: M-30 sugar;
- Hyderabad: S-30 sugar;
- prices include GST;
- display unit: `卢比/公斤`;
- raw unit: `₹/kg`.

## Fixed City Sample

Use the city sample in this order:

`Delhi`, `Kanpur`, `Raipur`, `Mumbai`, `Ranchi`, `Kolkata`, `Guwahati`, `Hyderabad`, `Chennai`.

If the dashboard displays one national-style price, compute a fixed city-sample arithmetic average. If a city cell is a range, convert it to midpoint first. For current, previous, and year-on-year comparisons, use only the common cities available in every compared period. Store `cities_used`, `city_count`, `city_prices`, and raw cell text.

## Uttar Pradesh Ex-Mill Price

Use only ChiniMandi formal daily close reports:

- entry: `https://www.chinimandi.com/english-news/daily-sugar-market-update/`
- article title pattern: `Daily Sugar Market Update By Vizzie`
- article slug pattern: `https://www.chinimandi.com/daily-sugar-market-update-by-vizzie-DD-MM-YYYY/`
- table: `Ex-mill Sugar Prices`
- row: `Uttar Pradesh`
- column: `M/30 [Rates per Quintal]`
- unit: `Rates per Quintal`, display `卢比/公担`, raw `₹/quintal`
- GST basis: excluding GST
- source name: `ChiniMandi — Daily Sugar Market Update`

Do not use:

- `Morning Market Update`;
- `Destination-wise Spot Price`;
- Muzaffarnagar spot/destination prices;
- Delhi, Kanpur, or other city spot prices;
- `S/30` for Uttar Pradesh when empty;
- other states' ex-mill prices;
- article prose such as "up/down ₹10-20";
- wholesale, retail, futures, SAP/FRP, or minimum selling price.

## Range Parsing

For a cell like `₹4500 to 4580`, store:

- raw range text;
- low `4500`;
- high `4580`;
- midpoint `4540`;
- display range `₹4,500—₹4,580/公担`.

If the source cell has one valid number, set low = high = midpoint. Never treat range width as price change.
