# Retirement statement

**On the website:** [landing.ai/document-type/retirement-statement](https://landing.ai/document-type/retirement-statement)

TIAA's sample quarterly retirement savings statement for January 1 to March 31, 2021.
It opens with the balance and a projected retirement income chart, then a portfolio
summary and asset allocation. Five workplace plans follow, each with holdings, changes
in value, transactions and vesting, and the statement ends with disclosures.

| | |
|---|---|
| Pages | 15 |
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
| Processed (UTC) | 2026-11-19 03:33 | 2026-11-19 03:50 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 43,795 | 44,284 |
| Words under 0.95 confidence | 121 | n/a |
| Words under 0.80 confidence | 51 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.5 s | 21.9 s |
| Per page | 1.0 s | 1.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.7 credits | 18.6 credits |
| Per page | 0.45 credits | 1.24 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:33 | 2026-11-19 03:51 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 442.8 s | 109.9 s |
| Per schema field (24) | 18.45 s | 4.58 s |
| Per value returned | 8.05 s | 2.00 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.6 credits | 10.7 credits |
| Per schema field (24) | 0.442 credits | 0.446 credits |
| Per value returned | 0.193 credits | 0.195 credits |

## Origin

`source/tiaa-participant-statement-sample.pdf` is TIAA's sample quarterly retirement
savings portfolio statement, January 1 to March 31, 2021. It is **15 pages, portrait
(US Letter)**: a cover with the balance and a projected retirement income chart, a
portfolio summary and asset allocation, then five workplace plans (a retirement plan, a
voluntary employee plan, a matching plan, a basic plan and a Roth supplemental annuity
plan), each with holdings, changes in value, transactions and vesting, followed by
disclosures.

| | |
|---|---|
| Publisher | TIAA |
| Source | [tiaa.org/…/PDF_Participant-statement-sample2.PDF](https://www.tiaa.org/public/pdf/p/PDF_Participant-statement-sample2.PDF) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted (hidden data removed) |

This is TIAA's own sample, published on its public site, marked SAMPLE on every page,
with the account holder's name and plan numbers left blank. The site does not answer
scripted requests, so the file was downloaded by hand.

**The published sample was not fully scrubbed.** Page 1 carried invisible mail-merge
control data, hidden under the grey balance panel and near the footer, that included
what appears to be a real participant's name, personal email address and PIN, along
with delivery, package and routing IDs built from the PIN. It does not show on the page,
but any text extraction reads it. The spans were deleted outright rather than replaced,
since they are delivery data rather than statement content, so nothing visible changed.
The deletion removed the underlying text, and the PDF metadata and XMP were cleared.
Verified: none of the values is in the page text or the raw PDF bytes, no other line of
text changed, and none appears anywhere in this folder.

A document published as a sample is not evidence that it is clean. The hidden text
layer is the leak path a visual check misses. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

### Who processes it

A retirement plan statement reports a participant's balance, contributions and
investments in workplace plans each quarter.

- **Financial advisers and wealth managers:** they gather clients' plan statements to
  build a full picture of assets and allocation.
- **Mortgage and consumer lending:** lenders accept retirement statements as proof of
  reserves.
- **Divorce and estate attorneys:** they use balances and vesting to divide or value
  retirement assets.
- **Plan sponsors, recordkeepers and auditors:** they reconcile contributions and
  vesting against payroll and plan records.
- **Rollover and account transfer teams:** they read holdings and balances when moving
  assets between providers.

### What it contains

- **Employee and employer money side by side,** split per plan and in total.
- **Five plans repeating the same sections,** with different lines present in each.
- **Vesting shown as a percent or as "not displayed",** which must not be read as 0%.
- **Charts,** including a projected income bar chart on the cover and an asset
  allocation summary.
- **Holdings and transaction tables** across many pages.
- **A SAMPLE mark on every page** and pages of disclosure text.
