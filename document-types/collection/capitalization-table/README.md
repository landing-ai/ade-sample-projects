# Capitalization Table

**On the website:** [landing.ai/document-type/capitalization-table](https://landing.ai/document-type/capitalization-table)

The pro forma capitalization table of a fictional company, Acme, Inc., after a Series B
financing. It lists each holder's Common, Series A and Series B shares with per-class and
fully diluted percentages, for five existing investors, a new investor, two founders and
three option pool rows, with a footnote on the preferred-to-common conversion ratio.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 16 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:37 | 2026-11-19 02:36 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,378 | 3,397 |
| Words under 0.95 confidence | 8 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.6 s | 5.8 s |
| Per page | 2.6 s | 5.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.4 credits |
| Per page | 0.50 credits | 1.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:37 | 2026-11-19 02:36 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 16 | 16 |
| Non-null fields returned | 16 | 16 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 156.4 s | 166.2 s |
| Per schema field (16) | 9.77 s | 10.39 s |
| Per value returned | 1.78 s | 1.89 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.1 credits | 3.1 credits |
| Per schema field (16) | 0.194 credits | 0.194 credits |
| Per value returned | 0.035 credits | 0.035 credits |

## Origin

`source/cooley-sample-pro-forma-cap-table.pdf` is the **pro forma capitalization table**
of a fictional Acme, Inc., after a Series B financing, from Cooley LLP's startup resource
site Cooley GO. It is **1 page, landscape**, created digitally with a text layer.

| | |
|---|---|
| Publisher | Cooley LLP (Cooley GO) |
| Source | [Sample-Pre-and-Post-Cap-Table-w-Pricing-Worksheet.pdf](https://www.cooleygo.com/wp-content/uploads/2014/06/Sample-Pre-and-Post-Cap-Table-w-Pricing-Worksheet.pdf) |
| Linked from | [Sample Cap Table (Pro Forma)](https://www.cooleygo.com/documents/sample-cap-table-pro-forma/) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Public**: a sample a law firm publishes for general use |

Every holder is a placeholder (Investor #1–#5, Founder #1–#2, New Investor), so no
content was redacted. The PDF's metadata (the firm's name as author, Excel as creator, a
creation date) and its tagged-PDF structure tree were cleared. None of it was personal
data.

Cooley also publishes the workbook this page was printed from, as a legacy `.xls` with
two more sheets: the pre-money cap table and an up-round pricing model. The PDF is
Cooley's own print of the Post-$ Pro Forma sheet only. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A cap table records who owns what in a private company, by share class, and how a new
financing changes it.

- **Venture capital and private equity:** investors model each round's dilution and
  check their fully diluted ownership before they close.
- **Startup legal counsel:** law firms prepare and check pro forma tables for every
  financing and keep them with the closing documents.
- **M&A due diligence:** buyers reconcile the cap table against stock ledgers and
  option grants to work out who gets paid what.
- **Equity management platforms:** cap tables from spreadsheets and PDFs are loaded
  into systems that track holdings over time.
- **409A valuation firms:** valuers use the share classes and option pool to value
  common stock.

### What it contains

- **A dense numeric grid, 11 columns wide,** with share counts and percentages in
  alternating columns.
- **Headers that wrap over two lines.**
- **Zero holdings printed as dashes,** so most cells in many rows carry no number.
- **Grouped rows** for investors, founders and the option pool, with a totals row.
- **A footnote** on the preferred-to-common conversion ratio.
