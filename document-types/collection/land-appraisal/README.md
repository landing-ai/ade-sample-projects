# Land Appraisal

**On the website:** [landing.ai/document-type/land-appraisal](https://landing.ai/document-type/land-appraisal)

Five pages of a Uniform Agricultural Appraisal Report valuing a 10,777.89-acre grazing
ranch in Powder River County, Montana, effective January 22, 2015. They hold the
summary of facts and conclusions, a sales comparison grid of ten comparable sales, the
income approach, and the reconciliation into a final opinion of value.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 43 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:14 | 2026-11-19 03:29 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 22,637 | 24,902 |
| Words under 0.95 confidence | 157 | n/a |
| Words under 0.80 confidence | 94 | n/a |
| Words under 0.50 confidence | 43 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 12.7 s | 13.5 s |
| Per page | 2.5 s | 2.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.1 credits | 8.8 credits |
| Per page | 0.62 credits | 1.76 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:15 | 2026-11-19 03:29 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 43 | 43 |
| Non-null fields returned | 43 | 43 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 177.2 s | 183.8 s |
| Per schema field (43) | 4.12 s | 4.27 s |
| Per value returned | 1.43 s | 1.48 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 7.9 credits | 8.3 credits |
| Per schema field (43) | 0.184 credits | 0.193 credits |
| Per value returned | 0.064 credits | 0.067 credits |

## Origin

`source/land-appraisal-uaar-warren-land-redacted.pdf` is five pages of a real **Uniform
Agricultural Appraisal Report (UAAR)**, the AgWare form used for farm and ranch lending.
It values a 10,777.89-acre grazing ranch in Powder River County, Montana for estate
planning, effective January 22, 2015. It is **5 pages, portrait (US Letter)**, cut from
a 74-page report.

| | |
|---|---|
| Publisher | Warren Land & Livestock, Inc., an agricultural appraisal firm in Billings, Montana |
| Source | [Redacted-Appraisal-Report.pdf](https://warrenlandinc.com/wp-content/uploads/2018/12/Redacted-Appraisal-Report.pdf) |
| Linked from | [warrenlandinc.com/samples](https://warrenlandinc.com/samples/) ("Redacted Appraisal Report") |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted** (by the publisher, before release) |

The full report is 74 pages, so this file keeps the five pages that carry the valuation,
split out with PyMuPDF:

| Here | Source page | Report page | Content |
|---|---|---|---|
| 1 | 6 | 2 of 70 | Property identification and summary of facts and conclusions |
| 2 | 40 | 36 of 70 | Sales Comparison Approach grid, sales 1-5 |
| 3 | 41 | 37 of 70 | Sales Comparison Approach grid, sales 6-10 |
| 4 | 43 | 39 of 70 | Income Approach |
| 5 | 44 | 40 of 70 | Reconciliation and opinion of value |

Everything else was left out: the cover and transmittal letter, table of contents,
signed certification, limiting conditions, area narrative, photographs, maps, the cost
approach worksheets, the per-sale land adjustment pages, deeds and the appraisers'
resumes.

The firm publishes this report as a work sample, and had already replaced the personal
data with a visible `***REDACTED***` placeholder: the owner, client, ranch name,
property address and location, legal description (section, township and range, shown as
`***`), the file number in every page header, and the grantor and grantee of every
comparable sale. The placeholder is real replacement text, not a box drawn over the
original, and the original strings are not in the file. Those placeholders stay visible
on the pages here.

The five kept pages were checked for anything the publisher missed, and nothing was
found: no name, signature, phone number, email or account number; no hidden or off-page
text (the only white text is the section headings on the blue bars); no annotations,
form fields, links or embedded files. The appraisers' names appear only on dropped
pages, in a professional capacity. No text was replaced and no page content was changed.

Two things that do not render were removed while splitting out the pages:

- **The PDF metadata**, which named one of the appraisers as author, and the bookmarks.
- **The original's shared image resources.** Every page of the original references the
  same twelve images (the photographs, maps and resume scans drawn on other pages). None
  is drawn on the kept pages, so they were removed from the resource dictionary.

The five pages render pixel-identical to the source pages and their text is unchanged.
The file has no metadata and no image objects, and neither appraiser's name is
extractable from the PDF or present anywhere in this folder. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

An agricultural appraisal values farmland and ranches by comparing recent land sales,
the income the land can earn and the cost of its improvements. It supports most large
farm and ranch transactions.

- **Agricultural lenders:** Farm Credit institutions, ag banks and life insurance
  lenders underwrite real estate loans against the appraised value.
- **Estate planning and estate tax:** attorneys and executors use appraisals to value
  ranches for gifts and estates, as with this report.
- **Farm and ranch real estate brokers and buyers:** they study comparable sales and
  per-acre prices when they price and bid on land.
- **Government programs:** conservation easement programs and federal agencies rely on
  appraisals to set purchase and easement values.
- **Appraisal reviewers:** lenders' review appraisers check each comparable's
  adjustments and the reconciliation.

### What it contains

- **A sales comparison grid of ten comparables** over two pages, each column a chain of
  per-acre arithmetic: price, land and improvement adjustments, time adjustment, net
  adjustment and adjusted price.
- **Three approaches to value** reconciled into one opinion, with the same dollar
  figures repeated across the summary and reconciliation pages.
- **Dense small-type form fields** with dotted leaders.
- **Visible redaction placeholders** (`***REDACTED***` and `***`) sitting inside the
  form and the grid.
- **Section headings in white text on blue bars.**
