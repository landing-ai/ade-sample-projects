# Accounts Receivable and Payable Aging Report

**On the website:** [landing.ai/document-type/ar-ap-aging-report](https://landing.ai/document-type/ar-ap-aging-report)

A sample accounts receivable aging report from Empire State Development, published to show
applicants to its CDFI lending program what an aging schedule should look like. It lists
eight customers of a fictitious "NYS CDFI" as of June 30, 2016, with each balance split
into current, 1-30, 31-60 and over-60-days-past-due buckets, and a Total row.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 22 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:25 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 1,896 | 1,931 |
| Words under 0.95 confidence | 4 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.6 s | 14.3 s |
| Per page | 2.6 s | 14.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.0 credits |
| Per page | 0.40 credits | 1.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:25 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 22 | 22 |
| Non-null fields returned | 20 | 20 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 35.5 s | 47.4 s |
| Per schema field (22) | 1.61 s | 2.16 s |
| Per value returned | 0.66 s | 0.88 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.5 credits | 2.5 credits |
| Per schema field (22) | 0.114 credits | 0.114 credits |
| Per value returned | 0.046 credits | 0.046 credits |

## Origin

`source/CDFI-RFP-Attachment2.pdf` is "Attachment 2: Sample Accounts Receivable Aging
Report", published by Empire State Development (ESD), New York State's economic
development agency. It is **1 page, portrait**: a single ruled table for a fictitious
"NYS CDFI" as of June 30, 2016, with eight customer rows and a Total row. The columns are
an MWBE status, "ESD Funds Used", the total receivable, and four aging buckets: Current,
1-30, 31-60 and Over 60 Days Past Due. A short tip about accounting software follows the
table.

| | |
|---|---|
| Publisher | Empire State Development (New York State) |
| Source | https://esd.ny.gov/sites/default/files/rfp/CDFI-RFP-Attachment2.pdf |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

ESD publishes the PDF on its own domain as an attachment to a public RFP for its CDFI
lending program. The data is specimen data, so it names no real customers or amounts. The
page text is unchanged. The only edit was clearing the PDF's document-information
metadata, because its author field named a state staff member. No page text needed
redaction.

This sample is **receivables only**. AR and AP aging reports share the same layout, with
customers swapped for vendors. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

An aging report breaks down what customers owe a business, or what it owes its
suppliers, by how long each balance has been outstanding. Lenders and finance teams ask
for it whenever the quality of receivables or payables matters.

- **Commercial lending and CDFIs:** lenders ask borrowers for an aging schedule to judge
  how collectible the receivables are, as ESD does here.
- **Asset-based lending and factoring:** lenders set borrowing bases from eligible
  receivables, which usually excludes balances past a set age.
- **Accounting and audit:** auditors test receivables and the bad-debt allowance against
  the aging buckets.
- **Credit and collections:** credit teams use the oldest buckets to decide which
  accounts to chase or put on hold.
- **Accounts payable:** finance teams use the payables version to plan payments and
  catch overdue vendor bills.

### What it contains

- **A single ruled table** with eight customer rows and a Total row.
- **Aging buckets that reconcile.** Each row's buckets sum to its total, and the columns
  sum to the Total row.
- **A non-standard oldest bucket,** "Over 60 Days" where many reports use "Over 90".
- **Program-specific columns** for MWBE status and ESD funds used, placed before the
  aging buckets.
- **Dashes and blanks for empty cells.** Some amounts print as `----` and some cells are
  left blank.
- **A header block** with the title, entity name and as-of date set together above the
  table.
