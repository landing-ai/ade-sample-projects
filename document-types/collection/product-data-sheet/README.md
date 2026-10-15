# Product Data Sheet

Source assets for `landing.ai/document-type/product-data-sheet`.

## Sample document

`source/Wolfspeed_HAB900C33LM4_data_sheet.pdf`: Wolfspeed's preliminary data sheet for
the HAB900C33LM4, a 3300 V, 900 A silicon carbide half-bridge power module.
**9 pages, portrait (612×792)**, with a text layer (InDesign).

| | |
|---|---|
| Publisher | Wolfspeed, Inc. (Durham, NC) |
| Source | [assets.wolfspeed.com/…/Wolfspeed_HAB900C33LM4_data_sheet.pdf](https://assets.wolfspeed.com/uploads/2026/05/Wolfspeed_HAB900C33LM4_data_sheet.pdf) |
| Title | HAB900C33LM4 Preliminary Datasheet, Rev. 1, May 2026 |
| Retrieved | 2026-10-14 |
| Clearance | Public |

A manufacturer's catalog data sheet, downloaded directly from Wolfspeed's own asset
domain, where it is distributed to design engineers and the public. It is marked
*Preliminary, subject to change without notice*. The footer carries the usual
"© 2026 Wolfspeed, Inc. All rights reserved" notice, so this is publicly distributed
material rather than copyright-free material.

There is no personal data: the only contact details are the company's headquarters
address and main switchboard number, and the document is not tied to any customer or
job. Nothing was redacted, and the source PDF is unmodified.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

It is a dense engineering spec rather than a business form, and it has the layout
features that make spec sheets hard to read reliably:

- **Merged cells in characteristic tables.** The Maximum Parameters, MOSFET, Diode and
  Physical Characteristics tables share one Parameter / Symbol / Min / Typ / Max / Unit /
  Conditions / Note layout. Unit, Note and Parameter cells span two to four rows, so a
  row's unit is often printed only once, rows above or below it.
- **Subscripted symbols** (V<sub>GS(th)</sub>, R<sub>DS(on)</sub>, T<sub>VJ</sub>) in
  both the symbol column and the conditions.
- **Sixteen numbered figures**: 12 typical performance curves set two per row on pages
  4–5, and four switching-definition diagrams on page 6, plus a schematic and package
  drawing on page 7.

## What the parse did

DPT-3 kept the merged cells: the HTML tables carry `rowspan` on every merged Unit,
Note, Parameter and Symbol cell (39 merged cells across the document). It returned 20 figures, 15 as
`CHART` and 5 as `DIAGRAM`, with each curve's caption kept with its chart.

## Extraction

`schema.json` resolves to **44 leaf fields**: product identification and revision, the
page 1 headline box, named values from the maximum-ratings, MOSFET, physical and NTC
tables, plus three arrays: every row of the MOSFET table (`characteristics_table`),
every numbered figure, and the application notes.

The values are right throughout, including the table rows that depend on merged cells.
Output capacitance (2.4) inherits `nF` from the Unit cell it shares with input
capacitance, and the 175 °C rows inherit their parameter, symbol and unit from the row
above.

Two errors and one schema problem:

- **Figure 7 is listed twice** in `performance_figures`, so the array has 17 entries for
  16 figures.
- **`on_resistance_test_conditions` was rewritten** as `V_GS = 18 V, I_D = 900 A`,
  borrowing the underscore notation from the schema's descriptions, and has no
  grounding. Asking for a value "as printed" did not stop that.
- **The committed extraction carries a `nonconformant_output` warning.** The last row of
  the MOSFET table, FET thermal resistance, really does have an empty Conditions cell,
  and the schema's `conditions` field is not nullable. An earlier run hit the same
  problem on the Min/Typ/Max columns, which were then made nullable. The remaining null
  is correct, so it was accepted rather than paying for another extraction.

## Featured fields

All on **page 1**, which identifies the part, shows its headline ratings and starts the
merged-cell Maximum Parameters table:

| Field | Value | Region |
|---|---|---|
| Part number | HAB900C33LM4 | Title |
| Rated drain-source voltage | 3300 V | Summary box |
| Rated on-state resistance | 2 mΩ | Summary box |
| Continuous drain current at 25 °C | 1200 | Maximum Parameters, Max. column |
| Power dissipation | 7282 | Maximum Parameters, Typ. column |

The request suggested page 1 or 2 and listed these fields along with R<sub>DS(on)</sub>
typ/max and gate threshold min/typ/max. Those ground correctly too, but they are on
page 2 and the page overlay shows only one page. Page 1 makes a single point: which part
this is, what it is rated for, and two limits read out of a table with merged Unit and
Note cells. The 1200 A value is the top row of a four-row merged `A` unit cell.

## Grounding

**Named fields ground to the exact cell.** Every value from the tables, on pages 1–3,
boxes its own Min, Typ or Max cell. The headline-box values box the full row, symbol
included.

**The `characteristics_table` array has no ranges at all.** All 14 rows extract
correctly, but every leaf comes back with `ranges: null`, so none of them can be
illustrated. The same values requested as named fields (`gate_threshold_voltage_*`,
`on_resistance_*`) ground precisely, on the same table. Here, a value in a fixed field
was located and the same value as a row of a repeated array was not. This is a contrast
with the consolidated 1099, whose `details` array grounds row by row. Both extractions
carry a `nonconformant_output` warning, but there it is on a top-level field and here it
is inside this very array, which may be the cause. The other arrays in this extraction,
the figures and application notes, are grounded.

**Figure captions ground to the caption.** `performance_figures[n].title` boxes the
caption under each chart, except Figure 2, whose two-line caption grounds to each line
separately and reads `OFF`.

`build_images.py` flags `rated_on_resistance` because OCR could not read `2 mΩ` in its
crop. The crop is correct; OCR misread the Ω.

## Cost

**31.20 credits** at standard tier for the committed output: 16.00 to parse 9 pages and
15.20 to extract. Building the folder cost **46.20** in total, because the first
extraction (15.00) was rerun after the Min/Typ/Max columns were made nullable.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py product-data-sheet                # ~31 credits
.venv/bin/python document-types/scripts/run_ade.py product-data-sheet --extract-only # ~15, schema iteration
.venv/bin/python document-types/scripts/build_images.py product-data-sheet           # free
.venv/bin/python document-types/scripts/inspect_fields.py product-data-sheet --page 1 --good
```
