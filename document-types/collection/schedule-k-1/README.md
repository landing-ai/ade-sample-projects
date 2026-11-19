# Schedule K-1

**On the website:** [landing.ai/document-type/schedule-k-1](https://landing.ai/document-type/schedule-k-1)

The 2025 IRS Schedule K-1 (Form 1065), Partner's Share of Income, Deductions, Credits,
etc., filled with IRS test data. It identifies the partnership and the partner, gives
the partner's share of profit, loss, capital and liabilities and a capital-account
roll-forward, and lists the partner's share of each income, deduction and credit line,
many with code letters.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 70 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:35 | 2026-11-19 03:52 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 5,867 | 6,224 |
| Words under 0.95 confidence | 38 | n/a |
| Words under 0.80 confidence | 11 | n/a |
| Words under 0.50 confidence | 6 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.6 s | 15.3 s |
| Per page | 5.6 s | 15.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.8 credits | 2.1 credits |
| Per page | 0.80 credits | 2.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:36 | 2026-11-19 03:53 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 70 | 70 |
| Non-null fields returned | 45 | 45 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 275.3 s | 95.9 s |
| Per schema field (70) | 3.93 s | 1.37 s |
| Per value returned | 6.12 s | 2.13 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.2 credits | 3.3 credits |
| Per schema field (70) | 0.046 credits | 0.047 credits |
| Per value returned | 0.071 credits | 0.073 credits |

## Origin

`source/schedule-k-1-2025-irs-ats-1065-scenario-1.pdf` is the 2025 IRS Schedule K-1
(Form 1065), Partner's Share of Income, Deductions, Credits, etc., filled with IRS test
data. It is **1 page, portrait**.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [ty25-f1065-ats-scenario01.pdf](https://www.irs.gov/pub/irs-wi/ty25-f1065-ats-scenario01.pdf) |
| Linked from | The IRS Tax Year 2025 Form 1065 MeF ATS information page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Scenario 1 for
tax year 2025 Form 1065, which software vendors use to test their e-file output. The
original PDF is 28 pages: the full partnership return with its schedules (B, K, L, M-1,
M-2, M-3), Forms 4562, 4797, 8825 and 8882, and the partners' K-1s. This file keeps
**page 12 only**, the first Schedule K-1.

Every value is IRS test data: a fictitious partnership, SAM STARLING LLP of Reno NV,
with an EIN in the `00-` test range, and a foreign individual partner whose TIN has the
`000-00-` form the IRS uses in ATS scenarios. Nothing needed redacting. The PDF metadata
was reset to the IRS as author and a title naming the scenario, and the XMP packet was
removed. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Every partner in a partnership receives a K-1 each year, so investors, preparers and
lenders read them in bulk.

- **Tax preparation and accounting:** preparers carry each K-1's amounts and codes onto
  the partner's own return.
- **Private equity, hedge and real estate funds:** fund administrators issue K-1s to
  investors and reconcile them with the partnership return.
- **Wealth management and family offices:** they collect K-1s across a client's
  holdings each tax season.
- **Mortgage and business lending:** underwriters read K-1s to verify self-employed and
  partnership income.
- **Tax software and e-file providers:** they test their output against IRS scenarios
  like this one.

### What it contains

- **Three parts in two columns,** with the partnership and the partner on the left and
  the partner's share of each line on the right.
- **Many checkboxes,** for final or amended K-1, general or limited partner, domestic or
  foreign, and more.
- **A code-letter grid** where boxes pair a box number, a code letter and an amount, and
  some boxes hold more than one row.
- **Beginning and ending matrices** for profit, loss and capital share and for
  liabilities.
- **A capital-account roll-forward.**
- **Empty coded boxes** that must stay empty.
