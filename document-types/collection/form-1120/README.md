# Form 1120

**On the website:** [landing.ai/document-type/form-1120](https://landing.ai/document-type/form-1120)

The 2024 IRS Form 1120, U.S. Corporation Income Tax Return, all six pages, filled with
IRS test data for a fictitious corporation. It reports the company's income,
deductions, taxable income, tax and payments, with the schedules behind them:
dividends, tax computation, other information, a balance sheet and retained earnings.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 69 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:03 | 2026-11-19 03:09 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 39,878 | 40,765 |
| Words under 0.95 confidence | 238 | n/a |
| Words under 0.80 confidence | 94 | n/a |
| Words under 0.50 confidence | 44 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 14.6 s | 13.3 s |
| Per page | 2.4 s | 2.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.9 credits | 13.2 credits |
| Per page | 0.82 credits | 2.20 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:03 | 2026-11-19 03:09 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 69 | 69 |
| Non-null fields returned | 59 | 59 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 430.0 s | 154.5 s |
| Per schema field (69) | 6.23 s | 2.24 s |
| Per value returned | 7.29 s | 2.62 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.0 credits | 10.2 credits |
| Per schema field (69) | 0.145 credits | 0.148 credits |
| Per value returned | 0.169 credits | 0.173 credits |

## Origin

`source/form-1120-2024-irs-ats-alternate-scenario-1.pdf` is the 2024 IRS Form 1120,
U.S. Corporation Income Tax Return, filled with IRS test data. It is **6 pages,
portrait**:

| Page | Content |
|---|---|
| 1 | Form 1120 page 1: header, income, deductions, tax and payments |
| 2 | Schedule C, dividends and special deductions |
| 3 | Schedule J, tax computation and payment |
| 4–5 | Schedule K, other information |
| 6 | Schedules L, M-1 and M-2: balance sheet and retained earnings |

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [ty24-f1120-ats-scenario-1-alternate.pdf](https://www.irs.gov/pub/irs-wi/ty24-f1120-ats-scenario-1-alternate.pdf) |
| Linked from | IRS Tax Year 2024 Form 1120 MeF ATS page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Alternate
Scenario 1 for tax year 2024, which software vendors use to test their e-file output.
The original PDF is 32 pages: cover sheets, Form 1120, then Schedules B, D, G, M-3 and O
and Forms 1125-A, 3800, 4562, 8594, 8916-A, 8453-CORP and 8949. This file keeps
**source pages 4 to 9 only**, the six pages of Form 1120 itself, split out with PyMuPDF.

Every value is IRS test data: the fictitious corporation Help For Some, Inc. at 33 Any
Street, Anytown MD, and a fictitious preparer firm with a 555 phone number. No
individual is named, and the officer and preparer signature lines are blank. Nothing
needed redacting. The PDF metadata was reset to the IRS as author and a title naming the
scenario. Page 2 (Schedule C) carries an "INTERNAL USE ONLY / DRAFT AS OF May 23, 2024"
watermark. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Form 1120 is the annual income tax return of a US C corporation. It is the standard
record of a corporation's revenue, profit and balance sheet as reported to the IRS.

- **Commercial lending:** lenders read two or three years of returns to analyze cash
  flow and confirm the financials a borrower submits.
- **Accounting and tax preparation:** CPAs prepare and review the return and reconcile
  book income to taxable income on Schedule M-1.
- **Tax software vendors:** e-file providers test their output against IRS scenarios
  like this one.
- **M&A and private equity due diligence:** buyers review historical returns for tax
  exposure and to check reported earnings.
- **Government programs and auditors:** grant and loan programs and auditors use returns
  to verify a company's revenue and size.

### What it contains

- **A long ladder of numbered amount lines** on page 1, from gross receipts to the
  amount owed or overpaid.
- **Schedules behind the main page,** each with its own numbered lines that feed page 1.
- **Checkboxes** in Schedule K, such as the accounting method, and yes/no questions.
- **A multi-column balance sheet** on Schedule L, with beginning and end of year amounts
  in paired columns.
- **Large figures,** up to eight digits, in narrow right-aligned amount columns.
- **Blank signature lines** and a paid preparer block.
- **A DRAFT watermark** across page 2.
