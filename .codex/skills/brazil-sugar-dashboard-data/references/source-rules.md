# Source Rules

## 1. 巴西进口升贴水

Fixed source: 泛糖科技 "食糖进口成本及利润估算表" list.

List URL:

```text
https://www.hisugar.com/home/newListMore?parentId=39&level=3&childId=144&menuTap1
```

Required process:

1. Open the list and discover candidate articles titled like "食糖进口成本及利润估算表".
2. Open candidate articles and parse the report's internal data date. Select the latest by data date, not by page order alone and not by crawl time.
3. Extract the `进口升贴水` value and unit from the selected report.
4. Normalize the displayed unit to `美分/磅`.
5. Find the previous valid data day from the same Hisugar source for daily change.
6. Find the previous-year comparable valid data from the same Hisugar source for year-on-year change.

Forbidden substitutes:

- Platts non-public quotes.
- News inference, third-party reposts, search snippets, or model-estimated values.
- Fixed article IDs or fixed example values.

Validation-only example, never a fallback:

- `https://www.hisugar.com/home/articleContent?id=2026072108403722853250`
- Contains 2026-07-20 data.
- Example import premium: `-0.3 美分/磅`.

## 2. 巴西食糖库存

Fixed source: MAPA official production page.

Entry URL:

```text
https://www.gov.br/agricultura/pt-br/assuntos/sustentabilidade/agroenergia/producao
```

Source label: `巴西农业和畜牧业部（MAPA）`.

Required process:

1. Open the MAPA production data page.
2. Locate sugar production and stocks materials, especially report family `009`.
3. In the current season, choose the latest report by internal `Acumulado ate` date.
4. Extract total Brazil sugar stock. Do not use cumulative production, sales, exports, or other fields.
5. Find the immediately previous `Acumulado ate` report in the same season for half-month change.
6. Open previous-season materials, `Sugar Production and Stocks by Type - Previous Seasons`.
7. Locate `ESTOQUES DE ACUCAR POR TIPO` with the same month/day for year-on-year comparison.
8. Keep current and year-on-year fields on the same stock scope and statistical basis.

Validation-only examples, never defaults:

- 2026-06-30: `345.0164 万吨`.
- 2026-06-15: `364.5203 万吨`.
- 2025-06-30: `401.6657 万吨`.

Unit rule:

- If raw value is tonnes, divide by 10,000 and display `万吨`.
- Preserve raw value, raw unit, converted value, and conversion note.
- Display 4 decimal places.

## 3. 巴西含水乙醇库存

Fixed source: MAPA ethanol tracking page.

Entry URL:

```text
https://www.gov.br/agricultura/pt-br/assuntos/sustentabilidade/agroenergia/acompanhamento-da-producao-sucroalcooleira
```

Source label: `巴西农业和畜牧业部（MAPA）官方乙醇报表`.

If the report explicitly identifies ANP as the underlying source, display `巴西农业和畜牧业部（MAPA），原始数据：ANP`. Do not infer ANP without report evidence.

Required process:

1. Open the MAPA ethanol production tracking page.
2. Enter the current latest season, such as `2026/2027`.
3. Select the latest report by internal `Volumes Acumulados ate` date. Do not use page `Last modified`.
4. Open the latest report.
5. Locate the Brazil national total row.
6. Extract hydrous ethanol stock from `ESTOQUE (m3)` / `E.Fisico`.
7. Do not use anhydrous ethanol, production, sales, or regional subtotals.
8. Find the immediately previous report in the same season for half-month change.
9. Find the previous-season same month/day report for year-on-year comparison.

Validation-only example, never a fallback:

- `Volumes Acumulados ate: 2026-07-01`.
- Field: hydrous ethanol `ESTOQUE (m3)` / `E.Fisico`.
- Converted example: `291.3832 万立方米`.

Unit rule:

- Raw stock is cubic metres.
- Divide by 10,000 and display `万立方米`.
- Preserve raw value, raw unit, converted value, and conversion note.
- Display 4 decimal places.
