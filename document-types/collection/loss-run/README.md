# Loss Run

**On the website:** [landing.ai/document-type/loss-run](https://landing.ai/document-type/loss-run)

A workers' compensation Claim/Loss Report that the Texas Association of Counties Risk
Management Pool produced for Cameron County, Texas, covering coverage years 2015 to
2019. It lists 1,309 claims with their claim numbers, loss dates, status, cause of loss,
paid amounts, outstanding reserves and recoveries, with a subtotal for each year and a
grand total.

| | |
|---|---|
| Pages | 31 |
| Fields in the extraction schema | 24 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:17 | 2026-11-19 03:34 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 275,187 | 288,782 |
| Words under 0.95 confidence | 2,556 | n/a |
| Words under 0.80 confidence | 344 | n/a |
| Words under 0.50 confidence | 9 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 54.9 s | 56.6 s |
| Per page | 1.8 s | 1.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 32.2 credits | 87.7 credits |
| Per page | 1.04 credits | 2.83 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:18 | 2026-11-19 03:35 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 213.4 s | 187.0 s |
| Per schema field (24) | 8.89 s | 7.79 s |
| Per value returned | 3.14 s | 2.75 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 57.0 credits | 59.7 credits |
| Per schema field (24) | 2.375 credits | 2.488 credits |
| Per value returned | 0.838 credits | 0.878 credits |

## Origin

`source/cameron-county-wc-loss-runs-2015-2019.pdf` is a workers' compensation Claim/Loss
Report produced by the Texas Association of Counties Risk Management Pool for its member
Cameron County, Texas, covering five coverage years (2015 to 2019). It is **31 pages,
landscape**. The 1,309 individual claims span pages 1 to 31, and page 31 also closes the
last period and summarizes all five periods with a grand total.

| | |
|---|---|
| Publisher | Texas Association of Counties Risk Management Pool, posted by Cameron County, Texas |
| Source | [cameroncountytx.gov](https://www.cameroncountytx.gov/wp-content/uploads/2022/10/Cameron-County-WC-Loss-Runs-2015-2019.pdf) |
| Retrieved | 2026-10-04 (downloaded by script) |
| Clearance | **Public** |

Cameron County published this loss run on its own official website alongside its
Workers' Compensation RFP 1470, so that brokers bidding on the account could price it. A
loss run is exactly the document an RFP like that has to carry, so this is a public
record of a real one.

No page text was redacted. The Claimant Full Name column is blank at source on every
page, so the report carries claim numbers, loss dates, status, cause-of-loss categories
and dollar amounts, but no claimant identities. The PDF's document metadata named the
pool staff member who ran the report. It was cleared before the file entered the repo,
and the source PDF now carries no metadata. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A loss run is an insurer's or pool's history of the claims on an account. It is the
first thing an underwriter asks for before quoting a new policy or a renewal.

- **Commercial insurance brokers:** they collect loss runs from the current carrier to
  market an account to other insurers.
- **Underwriters:** they read claim counts, paid and reserved amounts and loss trends to
  price the risk.
- **Risk managers and public entities:** counties, cities and companies track claim
  frequency and cost by year and cause.
- **Self-insurance pools and TPAs:** they produce and reconcile loss runs for their
  members.
- **Actuaries:** they use claim histories to project losses and set reserves.

### What it contains

- **A long, uniform claims table** that runs across 31 landscape pages.
- **A section break and a subtotal row** for each coverage period.
- **A summary block on the last page** that repeats every period's subtotals with a
  grand total, so the same figures appear twice.
- **Truncated text.** Cause-of-loss descriptions are cut off at the column width in the
  source.
- **Many $0 cells.** Most rows are $0 across the amount columns.
- **Eleven columns,** from claim number through paid, reserve, deductible, recoveries
  and total.
- **A blank column** for claimant names on every page.
