# Investor Presentation (Japanese)

Source assets for `landing.ai/document-type/investor-presentation-japanese`.

## Sample document

`source/nintendo-fy27-q2-earnings-presentation.pdf`: Nintendo's 決算説明資料 (earnings
explanatory material) for the second quarter of the fiscal year ending March 2027.
**18 pages, portrait (A4).**

| | |
|---|---|
| Publisher | Nintendo Co., Ltd. (任天堂株式会社, TSE: 7974) |
| Source | [nintendo.co.jp/ir/pdf/2026/261105_3.pdf](https://www.nintendo.co.jp/ir/pdf/2026/261105_3.pdf) |
| Retrieved | 2026-11-15 |
| Clearance | Public |

Investor relations material that a listed company publishes on its own IR site for
general distribution. It was downloaded directly from the URL, not by hand. No
individual is named anywhere in the deck, so nothing was redacted. The file is
byte-for-byte the publisher's copy, including its owner-password permissions flag
(there is no open password), and ADE parsed it without complaint.

## Why this document

The collection's other investor presentation (`investor-presentation`) is an English,
landscape, slides-only deck. This one differs on every axis that matters for parsing:

- **Japanese throughout**, with financial units the reader has to interpret: amounts in
  億円 (hundred millions of yen), 百万円 on the reference pages, unit sales in 万台 and
  万本 (tens of thousands). The schema asks for numbers in the units printed, and every
  value came back in those units.
- **A handout layout.** Pages 2 to 11 are A4 portrait sheets with a slide in the top
  third and the presenter's commentary as prose underneath, so most headline figures are
  printed twice: once in the slide, once in a sentence.
- **Reference tables.** Pages 13 to 17 are dense ruled data tables (regional sales,
  quarterly KPIs, unit sales by region, million-seller titles, release schedule), closer
  to a financial supplement than a slide.

## Featured fields

All five are on **page 3**, the 連結業績（実績） consolidated results slide, and read as one
story: the period column and the four headline profit lines in it.

| Field | Label | Value |
|---|---|---|
| `reporting_period` | Reporting period | FY27/Q1-Q2 |
| `consolidated_results.net_sales` | Net sales (売上高) | 9,660 億円 |
| `consolidated_results.operating_profit` | Operating profit (営業利益) | 2,165 億円 |
| `consolidated_results.ordinary_profit` | Ordinary profit (経常利益) | 3,006 億円 |
| `consolidated_results.net_profit` | Net profit (中間純利益) | 2,209 億円 |

The request named no page or fields, so these were chosen. Each is pinned to
occurrence 0, the table cell; the same figures recur in the commentary below the slide
and again on pages 4, 8 and 9.

## What the grounding did

**Ruled slide tables grounded per cell.** Page 3's slide parsed as a `table` block with
one `table_cell` per value, so every featured field has its own tight box: each crop
shows exactly one cell, and no two crops are alike. Pages 7 to 11 parse the same way.

**Two slides parsed as one whole-slide figure.** Pages 4 and 6 combine a results table
with a chart, and ADE treated each entire slide as a single `CHART` figure (about 86% of
the page width and a third of its height). Values from those slides still read `ok` in
`inspect_fields.py`, but any crop of them would be the whole slide. Chart labels on
slides commonly ground to the whole figure; here it extends to a results table that
shares a slide with a chart. Page 6 was avoided as the feature page for this reason, although
its digital sales figures extracted correctly.

**The whole-slide figure was transcribed in English, with a unit error.** The figure
description on page 6 renders 2,496億円 as "2,496 billion yen". 億 is a hundred
million, so the correct English is 249.6 billion yen; the description is off by a
factor of ten. The extraction is unaffected, because the schema asked for 億円 and
`digital_sales.digital_sales` came back as 2496, and its second occurrence grounds to
the Japanese commentary sentence that prints 2,496億円. But a pipeline that reads chart
descriptions for amounts would get it wrong.

**Japanese text grounds as cleanly as English.** All seven million-seller titles on
page 16 ground to their own cells with the title text intact, and no full-width digits
appeared in the markdown: the text layer uses ASCII digits throughout.

**Values that read OFF.** `presentation_date` (2026-11-05 from 2026年11月5日) and the
second occurrence of `reporting_period` (FY27/Q1-Q2, grounded to the cover's
2027年3月期第2四半期) are correct but normalized, so their boxed text does not contain
the value. The `unit_sales[].category` values are English words (hardware, software)
grounded to ハードウェア and ソフトウェア. None of these is featured.

**A value grounded on another page.** `full_year_forecast.usd_jpy_assumption` (150)
grounds to the 前提為替レート column of the page 13 reference table, not to the forecast
slide on page 10 that states it in a footnote.

## Extraction

`schema.json` has **26 leaf fields**: cover details, the consolidated results, digital
sales, unit sales by platform, the full-year forecast, and the million-seller table.
Everything extracted, with every amount in the units printed (億円, 万台, 万本).

## Cost

**23.20 credits** at standard tier for 18 pages: 16.00 to parse with
`dpt-3-pro-20260710` and 7.20 to extract with `extract-20260903`.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-japanese                # 23.20 credits
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-japanese --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py investor-presentation-japanese           # free
.venv/bin/python document-types/scripts/inspect_fields.py investor-presentation-japanese --page 3
```
