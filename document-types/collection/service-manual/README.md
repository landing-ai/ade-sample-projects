# Service Manual

Source assets for `landing.ai/document-type/service-manual`.

## Sample document

`source/goodman-gpg14-service-manual-excerpt.pdf`: five pages from Goodman's service
instructions for its APG/GPG 14 SEER gas/electric package units with R-410A refrigerant
(publication RS6300012r4, July 2017). **5 pages, portrait (612×792)**, with a text layer
throughout (Acrobat Distiller); the cover drawing and the chart grids are vector paths.

| | |
|---|---|
| Publisher | Goodman Manufacturing Company, L.P. (hosted by HVACDirect) |
| Source | [hvacdirect.com/…/GPG14-Service.pdf](https://hvacdirect.com/media/hvac/pdf/GPG14-Service.pdf) |
| Title | Service Instructions: APG/GPG 14 SEER Gas Electric Package Units with R-410A Refrigerant & Accessories (RS6300012r4, July 2017) |
| Retrieved | 2026-10-14 |
| Clearance | Public |

A manufacturer's service manual, written for HVAC technicians and distributed freely for
use with Goodman equipment. This copy is hosted by HVACDirect, an online HVAC retailer
that posts manufacturers' manuals for the products it sells; other dealers and
distributors carry Goodman's manuals for this unit the same way (an earlier RS6300012
revision is on Alpine Home Air's document server). No page on goodmanmfg.com was found
linking this exact revision, so the retailer's URL is the source of record. The manual
carries "Copyright © 2014-2017 Goodman Manufacturing Company, L.P.", so it is publicly
distributed material rather than copyright-free material. Downloaded by script.

The full manual is 67 pages. This folder keeps five of them, in this order, split out
with PyMuPDF at the operator's choice:

| Page here | Manual page | Content |
|---|---|---|
| 1 | 1 | Cover |
| 2 | 32 | Cooling Analysis Chart |
| 3 | 33 | Gas Heating Analysis Chart |
| 4 | 34 | Servicing table of contents (S-1 to S-314) |
| 5 | 35 | S-1 Checking Voltage |

There is no personal data on the kept pages: no names, phone numbers or email addresses.
Nothing was redacted. The document metadata was cleared when the pages were split out.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

The two analysis charts are troubleshooting matrices, a layout common in technical
manuals and rare in business documents:

- **Rotated column headers.** Sixteen symptom columns on page 2 (nine on page 3) are
  labelled with text turned 90 degrees, under merged group headers (No Cooling,
  Unsatisfactory Cooling, System Operating Pressures).
- **Dot-only cells.** The data is a bullet in a cell, so which symptom a dot belongs to
  can only be read from its x-position under a rotated label.
- **Sparse reference column.** Many rows have no service procedure reference, which tests
  how blanks come back.

The rest of the excerpt adds a two-column table of contents and a short procedure with a
small limits table.

## What the parse did

DPT-3 read the cooling chart as one HTML table, with all 16 rotated labels as horizontal
header text in the right order and one `<td>` per symptom column carrying `•` or `●`.
The group header row is slightly off: Unsatisfactory Cooling and System Operating
Pressures were merged into one `colspan="9"` cell instead of five and four columns. The
two-column table of contents became a six-column table, read row by row, and the parse
dropped the B from `S-105B`. The PDF's broken word spacing (`Pow er Failure`,
`Blow n Fuse`) came through as printed.

## Extraction

`schema.json` resolves to **25 leaf fields**: the cover's identification, both analysis
charts as arrays of cause rows (cause, dotted symptoms, remedy, procedure reference), the
table of contents, and the S-1 voltage limits and imbalance threshold.

**The dot matrix extracts almost perfectly.** Checked against the dot positions in the
PDF's own text layer, 40 of the 41 cooling-chart rows have exactly the right set of
symptom columns (117 of 118 dots). The one miss is the Condenser fan will not start dot
on Shorted or Grounded Fan Motor. It is present in the parse, so extraction dropped it.

Other findings:

- **Blank reference cells came back as `""`, not `null`**, on 14 rows, even though the
  schema description asks for null when the cell is blank.
- **The table of contents is in row order, not reading order**: S-1, S-105, S-2, S-106,
  and so on, following the parse's six-column table. All 54 entries are there, and
  `S-105B` is `S-105`, inherited from the parse.
- The cover, voltage-limits table (460 V: 437 to 506; 208/230 V: 198 to 253) and the
  3% imbalance threshold are all correct.

## Featured fields

All on **page 2** (manual page 32), the Cooling Analysis Chart, as the request asked. They
are one complete lookup in the chart: the cause, what to do and where the procedure is.

| Field | Value | Region |
|---|---|---|
| Chart title | COOLING ANALYSIS CHART | Title |
| Possible cause | Shortage of Refrigerant | Row 19, cause column |
| Test method / remedy | Test For Leaks, Add Refrigerant | Row 19, Test Method / Remedy |
| Service procedure reference | S-103 | Row 19, See Service Procedure Ref. |

The request suggested, as suggestions only, a cause row's remedy, its procedure
reference and which symptom columns carry a dot, plus the chart title. The row's four
symptoms (Compressor cycles on overload, System runs continuously - little cooling, Low
suction pressure, Low head pressure) extract correctly but cannot be featured, because
they do not ground to their column labels (see below).

## Grounding

**Text cells ground to the exact cell.** Cause, remedy and reference values box their own
cell row by row down all 41 rows, with no drift. `build_images.py` flags `S-103` because
OCR could not read it in its crop; the crop is correct.

**Dotted symptoms ground to the dot, not the label.** For 113 of the 117 symptom values
on page 2, the range points at the `•` in the row's cell. That is arguably the right
place: it is the mark on the page that supports the value. But the boxed text does not
contain the value, so it reads `OFF` and the crop would show a dot beside a label like
"Low suction pressure". Only the first two rows' symptoms were grounded to the header
text instead and read `ok`. The bounding boxes do show which column each dot is in, so
an application can recover the column from the box even when the value cannot be
illustrated.

**Blank references ground to an empty string** and read `OFF`, so they cannot be shown
either.

## Cost

**34.10 credits** at standard tier: 9.10 to parse 5 pages and 25.00 to extract. One run;
no extraction was repeated.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py service-manual                # ~34 credits
.venv/bin/python document-types/scripts/run_ade.py service-manual --extract-only # ~25, schema iteration
.venv/bin/python document-types/scripts/build_images.py service-manual           # free
.venv/bin/python document-types/scripts/inspect_fields.py service-manual --page 2 --good
```

To rebuild the source from the full manual, keep pages 1, 32, 33, 34 and 35 in that
order with PyMuPDF and clear the metadata.
