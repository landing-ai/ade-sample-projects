# Schedule C

**On the website:** [landing.ai/document-type/schedule-c](https://landing.ai/document-type/schedule-c)

The 2025 IRS Schedule C (Form 1040), Profit or Loss From Business, filled with IRS test
data for a fictitious sole proprietor running a design business. It reports the
business details and accounting method, gross receipts, the expense lines, and the net
profit. Page 2, for cost of goods sold, vehicle information and other expenses, is blank
on this return.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 60 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:34 | 2026-11-19 03:52 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 10,809 | 10,962 |
| Words under 0.95 confidence | 52 | n/a |
| Words under 0.80 confidence | 22 | n/a |
| Words under 0.50 confidence | 8 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 51.5 s | 25.2 s |
| Per page | 25.7 s | 12.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.4 credits | 3.8 credits |
| Per page | 0.70 credits | 1.90 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:35 | 2026-11-19 03:53 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 60 | 60 |
| Non-null fields returned | 26 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 125.2 s | 126.1 s |
| Per schema field (60) | 2.09 s | 2.10 s |
| Per value returned | 4.82 s | 4.85 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 4.1 credits | 4.1 credits |
| Per schema field (60) | 0.068 credits | 0.068 credits |
| Per value returned | 0.158 credits | 0.158 credits |

## Origin

`source/schedule-c-2025-irs-ats-scenario-12.pdf` is the 2025 IRS Schedule C (Form 1040),
Profit or Loss From Business (Sole Proprietorship), pages 1 and 2, filled with IRS test
data. It is **2 pages, portrait**.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-12-10292025.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-12-10292025.pdf) |
| Linked from | [Tax Year 2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public: US government work, public domain |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Test Scenario 12
for tax year 2025, which software vendors use to test their e-file output. The original
PDF is 15 pages: a cover sheet, Form 1040, Schedules 1, 2, C and SE, Forms 7206 and
7217, and a W-2. This folder keeps **pages 8 and 9 only**, the two pages of Schedule C,
split out with PyMuPDF. No content was altered.

Every value is IRS test data: a fictitious sole proprietor running a design business
called ENERGY BUILD in Anytown KY, with an SSN in the 400-00 range the IRS reserves for
ATS testing. Nothing needed redacting. The PDF metadata was reset to the IRS as author
and a title naming the scenario.

The pages carry a "TREASURY/IRS AND OMB USE ONLY DRAFT" header and "DRAFT — DO NOT FILE"
side banners. Page 2 (Parts III to V: cost of goods sold, vehicle information, other
expenses) is blank on this return and is kept so the folder holds the complete schedule.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Schedule C is how a sole proprietor reports business income on a personal tax return.
It is the main record of a self-employed person's earnings.

- **Mortgage lending:** lenders use two years of Schedule C net profit to qualify
  self-employed borrowers.
- **Small-business and SBA lending:** loan officers read gross receipts, expenses and
  net profit to size a loan.
- **Tax preparation and accounting:** preparers carry the figures into Schedule SE and
  Form 1040 and compare them year over year.
- **Income verification and government programs:** agencies and verification services
  use net profit as the income of a self-employed applicant.
- **Tax software vendors:** they test their e-file output against IRS scenarios like
  this one.

### What it contains

- **A two-column expense grid.** Part II runs lines 8-17 down the left and 18-27b down
  the right, each with its own amount column.
- **The same value on several lines,** with gross receipts repeated on lines 1, 3, 5
  and 7.
- **A header full of checkboxes and coded fields:** the accounting method, the
  material-participation and 1099 questions, and a six-digit business code printed in
  separate boxes.
- **Blank amount lines** and a blank second page.
- **Draft banners** in the header and down the sides of each page.
