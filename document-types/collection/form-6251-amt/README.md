# Form 6251 - AMT

**On the website:** [landing.ai/document-type/form-6251-amt](https://landing.ai/document-type/form-6251-amt)

IRS Form 6251 for 2025, Alternative Minimum Tax for individuals, completed with IRS test
data for a fictitious married couple. It adjusts income to alternative minimum taxable
income, subtracts the exemption, and compares the tentative minimum tax with the regular
tax. Here no AMT is owed, and the capital gains part on page 2 is blank.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 21 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:05 | 2026-11-19 03:10 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 14,378 | 16,079 |
| Words under 0.95 confidence | 77 | n/a |
| Words under 0.80 confidence | 22 | n/a |
| Words under 0.50 confidence | 5 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.8 s | 13.8 s |
| Per page | 3.4 s | 6.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.8 credits | 5.1 credits |
| Per page | 0.90 credits | 2.55 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:05 | 2026-11-19 03:11 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 21 | 21 |
| Non-null fields returned | 14 | 14 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 367.6 s | 246.9 s |
| Per schema field (21) | 17.50 s | 11.76 s |
| Per value returned | 26.26 s | 17.64 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.5 credits | 3.8 credits |
| Per schema field (21) | 0.167 credits | 0.181 credits |
| Per value returned | 0.250 credits | 0.271 credits |

## Origin

`source/form-6251-2025-irs-ats-scenario-13.pdf` is IRS Form 6251 (2025), Alternative
Minimum Tax—Individuals, completed for an IRS e-file test scenario. It is **2 pages,
portrait**, with a text layer.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-13.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-13.pdf), pages 5-6 of 9 |
| Linked from | [TY2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | Public |

The IRS publishes these Assurance Testing System (ATS) scenarios so that e-file software
developers can test their returns against known answers. As a US government work, it is
in the public domain.

The source is a 9-page packet for Test Scenario 13. Pages 5-6, the completed Form 6251,
were split out unchanged. The same packet supplies the `form-1040` folder (pages 2-3).

Every value is IRS test data for a fictitious taxpayer. The SSN is in the 400-00-13xx
range that the ATS keeps for test scenarios. The PDF metadata names only the IRS, Acrobat
and Distiller. Nothing needed redacting.

The IRS replaces these undated files in place from time to time, so the committed copy
is the record. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Form 6251 decides whether a taxpayer owes the alternative minimum tax on top of the
regular tax. It is filed with Form 1040 whenever the AMT applies or certain adjustments
are present.

- **Tax preparation and CPA firms:** preparers review prior-year 6251s to carry forward
  AMT credits and adjustments.
- **Mortgage and consumer lending:** underwriters read the full return, including its
  schedules, when they verify self-employed or high-income borrowers.
- **Wealth management and financial planning:** advisers check AMT exposure before
  exercising incentive stock options or realizing large gains.
- **Tax software developers:** e-file vendors test their returns against IRS scenarios
  like this one.
- **IRS and state examiners:** they check the computation line by line during review.

### What it contains

- **A line-numbered computation,** where each line feeds the next and the result
  depends on earlier lines.
- **An inner amount column.** Line 1a's value sits to the left of the main amount
  column.
- **A value printed twice.** Line 5's exemption appears in a threshold table beside the
  line and again as the line's own entry.
- **Blank lines and a blank page by design.** Only about eight lines are filled, and
  Part III on page 2 is empty.
- **A zero result,** since no AMT is owed.
- **A text layer** on a two-page portrait form.
