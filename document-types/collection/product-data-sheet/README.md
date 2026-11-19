# Product Data Sheet

**On the website:** [landing.ai/document-type/product-data-sheet](https://landing.ai/document-type/product-data-sheet)

Wolfspeed's preliminary data sheet for the HAB900C33LM4, a 3300 V, 900 A silicon
carbide half-bridge power module. It gives the part's headline ratings, tables of
maximum ratings and MOSFET, diode and physical characteristics, sixteen numbered
performance curves and switching diagrams, a schematic and package drawing, and
application notes.

| | |
|---|---|
| Pages | 9 |
| Fields in the extraction schema | 44 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:43 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 45,878 | 44,836 |
| Words under 0.95 confidence | 263 | n/a |
| Words under 0.80 confidence | 167 | n/a |
| Words under 0.50 confidence | 36 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 16.3 s | 20.2 s |
| Per page | 1.8 s | 2.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.0 credits | 15.8 credits |
| Per page | 0.67 credits | 1.76 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:43 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 44 | 44 |
| Non-null fields returned | 44 | 44 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 250.1 s | 313.1 s |
| Per schema field (44) | 5.68 s | 7.12 s |
| Per value returned | 1.57 s | 1.97 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 15.0 credits | 14.9 credits |
| Per schema field (44) | 0.341 credits | 0.339 credits |
| Per value returned | 0.094 credits | 0.094 credits |

## Origin

`source/Wolfspeed_HAB900C33LM4_data_sheet.pdf` is Wolfspeed's preliminary data sheet for
the HAB900C33LM4, a 3300 V, 900 A silicon carbide half-bridge power module. It is **9
pages, portrait (612×792)**, with a text layer (InDesign). Its title is
"HAB900C33LM4 Preliminary Datasheet, Rev. 1, May 2026".

| | |
|---|---|
| Publisher | Wolfspeed, Inc. (Durham, NC) |
| Source | [assets.wolfspeed.com/…/Wolfspeed_HAB900C33LM4_data_sheet.pdf](https://assets.wolfspeed.com/uploads/2026/05/Wolfspeed_HAB900C33LM4_data_sheet.pdf) |
| Retrieved | 2026-10-14 |
| Clearance | Public |

A manufacturer's catalog data sheet, downloaded directly from Wolfspeed's own asset
domain, where it is distributed to design engineers and the public. It is marked
*Preliminary, subject to change without notice*. The footer carries the usual
"© 2026 Wolfspeed, Inc. All rights reserved" notice, so this is publicly distributed
material rather than copyright-free material.

There is no personal data: the only contact details are the company's headquarters
address and main switchboard number, and the document is not tied to any customer or
job. Nothing was redacted, and the source PDF is unmodified. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Every electronic component ships with a data sheet, and the figures in it decide
whether a part can be designed in, bought and qualified.

- **Hardware and power electronics engineering:** designers compare ratings and
  characteristics across candidate parts.
- **Electronics distributors and component databases:** they load parametric values
  from manufacturers' data sheets into searchable catalogs.
- **Procurement and supply chain:** buyers match alternates and second sources on key
  specifications.
- **Quality and compliance teams:** they check parts against qualification requirements
  and track revisions of preliminary data sheets.
- **Manufacturers' product and applications teams:** they maintain data across many
  data sheets and part revisions.

### What it contains

- **Characteristic tables with merged cells.** Unit, Note, Parameter and Symbol cells
  span two to four rows, so a row's unit is often printed only once, above or below it.
- **Min, Typ and Max columns** with many cells left empty.
- **Subscripted symbols** such as V<sub>GS(th)</sub>, R<sub>DS(on)</sub> and
  T<sub>VJ</sub>, in both the symbol and conditions columns.
- **Sixteen numbered figures:** typical performance curves set two per row, and
  switching-definition diagrams.
- **A schematic and a package drawing** with dimensions.
- **Engineering units and symbols** such as mΩ, nF and °C.
