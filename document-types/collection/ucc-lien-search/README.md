# UCC lien search

**On the website:** [landing.ai/document-type/ucc-lien-search](https://landing.ai/document-type/ucc-lien-search)

MicroBilt's sample UCC Search Report, filled with specimen data. It lists five UCC
financing statements filed in Washington, each with its debtor, filing date, creditor,
document numbers and counts, and then gives the detail record for one filing: its
debtor parties, the secured party and the filing event.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 27 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:40 | 2026-11-19 03:57 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,556 | 4,034 |
| Words under 0.95 confidence | 39 | n/a |
| Words under 0.80 confidence | 10 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.7 s | 7.4 s |
| Per page | 2.8 s | 3.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.7 credits | 2.1 credits |
| Per page | 0.35 credits | 1.05 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:41 | 2026-11-19 03:57 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 27 | 27 |
| Non-null fields returned | 25 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 163.5 s | 124.9 s |
| Per schema field (27) | 6.06 s | 4.63 s |
| Per value returned | 2.21 s | 1.73 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.7 credits | 3.8 credits |
| Per schema field (27) | 0.137 credits | 0.141 credits |
| Per value returned | 0.050 credits | 0.053 credits |

## Origin

`source/microbilt-ucc-report-2024.pdf` is MicroBilt's sample UCC Search Report. It is
**2 pages, portrait (US Letter)**, born-digital with a text layer. Page 1 and the top of
page 2 hold a results table of five UCC financing statements filed in Washington, each
with its debtor, filing state and date, creditor, document numbers and filing, debtor and
secured-party counts. The rest of page 2 is the detail record for one of those filings:
original document number and date, filing state, four debtor parties, the secured party,
and the filing event with its type code.

| | |
|---|---|
| Publisher | MicroBilt Corporation |
| Source | [microbilt.com/.../UCC-Report-2024.pdf](https://www.microbilt.com/Cms_Data/Contents/Microbilt/Media/Docs/SampleReports/UCC-Report-2024.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

**A vendor's own published specimen, and nothing was redacted.** MicroBilt links this
PDF from its UCC product page, and a reseller (lsiservices.net) links it from its
samples page. It is filled with specimen data: names such as ANY COMPANY and WALLY WORLD
MEGA VISION CINEMA, ANYSTREET addresses with ZIP 12345, and document numbers masked as
XXXX. The only phone number is MicroBilt's toll-free sales line in the footer. The PDF
metadata carries only InDesign producer data. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A UCC search shows which creditors have filed liens against a business's assets, so it
is a standard step before lending to, buying or extending credit to that business.

- **Commercial lending:** lenders search before closing to confirm their lien position
  and find competing creditors.
- **Equipment finance and leasing:** lessors check for existing liens on the equipment
  and the lessee.
- **M&A and legal due diligence:** lawyers search the target for liens that must be
  released at closing.
- **Trade credit and collections:** credit managers check a customer's secured debt
  before setting terms.
- **Title, search and filing services:** they run searches across state filing offices
  and deliver reports like this one.

### What it contains

- **A results grid built from loose text.** Each result is a block of text in three
  shaded columns, with label and value pairs such as `DOC NUMBER:` and `FILING COUNT
  [ 1]`.
- **A result that breaks across the page,** so its counts sit on page 2.
- **The same filing more than once.** One document number appears as two results under
  different debtor names, and again in the detail record.
- **A labelled detail record** with key and value pairs set side by side in two
  columns.
- **Blank labels by design.** Every `COLLATERAL:` label is empty, and there are no lapse
  dates.
- **Values that wrap over two lines,** such as the type of filing and debtor addresses.
