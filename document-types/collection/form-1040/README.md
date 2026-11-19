# Form 1040

**On the website:** [landing.ai/document-type/form-1040](https://landing.ai/document-type/form-1040)

The two pages of the 2025 IRS Form 1040, U.S. Individual Income Tax Return, filled with
IRS test data for a fictitious married couple filing jointly. It records the filers'
identity and address, filing status, the digital-assets answer, income, adjusted gross
income, deductions, tax, credits, payments and the refund.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 50 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:02 | 2026-11-19 03:07 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 18,230 | 19,113 |
| Words under 0.95 confidence | 149 | n/a |
| Words under 0.80 confidence | 51 | n/a |
| Words under 0.50 confidence | 33 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.6 s | 23.8 s |
| Per page | 3.8 s | 11.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.2 credits | 5.8 credits |
| Per page | 1.10 credits | 2.90 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:02 | 2026-11-19 03:08 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 50 | 50 |
| Non-null fields returned | 28 | 30 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 261.2 s | 97.4 s |
| Per schema field (50) | 5.22 s | 1.95 s |
| Per value returned | 9.33 s | 3.25 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.0 credits | 5.2 credits |
| Per schema field (50) | 0.100 credits | 0.104 credits |
| Per value returned | 0.179 credits | 0.173 credits |

## Origin

`source/form-1040-2025-irs-ats-scenario-13.pdf` is the 2025 IRS Form 1040, U.S.
Individual Income Tax Return, pages 1 and 2, filled with IRS test data. It is **2 pages,
portrait**.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-13.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-13.pdf) |
| Linked from | [Tax Year 2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Test Scenario 13
for tax year 2025, which software vendors use to test their e-file output. The original
PDF is 9 pages: a cover sheet, Form 1040, Schedule 3, Form 6251, Form 8911 and its
Schedule A, and a W-2. This folder keeps **pages 2 and 3 only**, the two pages of Form
1040, split out with PyMuPDF. The Form 6251 pages ship separately as `form-6251-amt`.

Every value is IRS test data: a fictitious married-filing-jointly couple at 13 Elm
Street, Anytown TX, with SSNs in the 400-00 range the IRS reserves for ATS testing.
Nothing needed redacting. The PDF metadata was reset to the IRS as author and a title
naming the scenario.

The pages carry a "TREASURY/IRS AND OMB USE ONLY DRAFT" header and "DRAFT — DO NOT FILE"
side banners. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Form 1040 is the US individual income tax return and the most common US tax form. It is
the standard record of a household's income.

- **Mortgage and consumer lending:** underwriters use recent returns to verify income,
  especially for self-employed borrowers.
- **Tax preparation and accounting:** preparers and CPAs carry figures from prior-year
  returns and reconcile them against W-2s and schedules.
- **Financial aid:** colleges and aid offices verify family income reported on aid
  applications.
- **Wealth management and financial planning:** advisors read AGI, taxable income and
  tax due to plan for clients.
- **Tax software vendors:** vendors test their e-file output against IRS scenarios like
  this one.

### What it contains

- **Filing-status and digital-assets checkboxes,** plus empty direct-deposit
  checkboxes.
- **A long ladder of numbered amount lines,** most of them blank, across two pages.
- **Repeated values on different lines.** The same amount (31,620) appears on four lines
  of page 1, so each value has to be tied to its own line.
- **Identity and address fields** in a boxed header, including SSN boxes.
- **DRAFT headers and side banners** printed across the pages.
