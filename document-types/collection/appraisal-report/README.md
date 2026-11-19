# Appraisal Report

**On the website:** [landing.ai/document-type/appraisal-report](https://landing.ai/document-type/appraisal-report)

A complete Uniform Residential Appraisal Report (URAR) in the redesigned Uniform Appraisal
Dataset format, filled with Freddie Mac and Fannie Mae specimen data. It appraises a
detached three-level colonial with a walk-out basement, subject to repair. It covers the
subject property, three comparable sales in an adjustment grid, the reconciled opinion
of market value, a defects table and the appraiser's credentials.

| | |
|---|---|
| Pages | 21 |
| Fields in the extraction schema | 57 |

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
| Characters returned | 65,683 | 72,539 |
| Words under 0.95 confidence | 197 | n/a |
| Words under 0.80 confidence | 70 | n/a |
| Words under 0.50 confidence | 21 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 34.7 s | 58.2 s |
| Per page | 1.7 s | 2.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.8 credits | 28.7 credits |
| Per page | 0.47 credits | 1.37 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:27 | 2026-11-19 02:26 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 57 | 57 |
| Non-null fields returned | 57 | 57 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 101.9 s | 158.0 s |
| Per schema field (57) | 1.79 s | 2.77 s |
| Per value returned | 1.29 s | 2.00 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 15.7 credits | 17.1 credits |
| Per schema field (57) | 0.275 credits | 0.300 credits |
| Per value returned | 0.199 credits | 0.216 credits |

## Origin

`source/appraisal-report-uad-urar-sf1.pdf` is a complete **Uniform Residential
Appraisal Report (URAR)** in the redesigned Uniform Appraisal Dataset (UAD) format, the
form that replaces Fannie Mae Form 1004 / Freddie Mac Form 70. It is Single Family
Scenario 1: a detached three-level colonial with a walk-out basement, appraised subject
to repair. It is **21 pages, portrait, US legal size (8.5 x 14 in)**.

| | |
|---|---|
| Publisher | Freddie Mac and Fannie Mae (UAD redesign) |
| Source | [uad-sample-scenarios-combined.pdf](https://sf.freddiemac.com/docs/pdf/uad-sample-scenarios-combined.pdf) |
| Linked from | Freddie Mac's UAD page |
| Retrieved | 2026-10-03, by script |
| Clearance | Public: GSE specimen published for the industry |

The source PDF is 302 pages of sample scenarios. This folder keeps **pages 180-200
only**, the full 21-page URAR for Single Family Scenario 1, split out with PyMuPDF. Page
179, the scenario's introduction cover, is marked "not part of the URAR" and was left
out.

Every value is illustrative specimen data: Betty and Bob Borrower, Agatha Appraiser, 123
Falling Tree Ct, Treeville VA 12345, DEF Bank, ABC Appraisal Co. Nothing needed
redacting. The photo, sketch and chart areas are grey placeholders in the original
("This is where the Subject Property photo would display"). The PDF metadata was reset
to Freddie Mac as author and a title naming the scenario. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

An appraisal is the lender's evidence for the value of the property that secures a
mortgage. The redesigned URAR is the form every appraisal delivered to Fannie Mae and
Freddie Mac will use.

- **Mortgage lending:** underwriters read the opinion of value, the condition ratings
  and the comparables to set the loan-to-value ratio.
- **Appraisal management companies:** they review each report for completeness and
  consistency before it goes to the lender.
- **Secondary market and loan purchasers:** the GSEs and investors check delivered
  appraisals against their data standards.
- **Quality control and compliance:** reviewers test whether the comparables and
  adjustments support the final value.
- **Mortgage technology vendors:** software that produces or ingests appraisals is built
  and tested against these published sample scenarios.

### What it contains

- **A long, dense form:** 21 legal-size pages of label/value pairs and ruled tables.
- **A sales comparison grid split across two pages,** with four columns (subject plus
  three comparables), each comparable carrying a value and an adjustment cell side by
  side.
- **The same dollar amounts in many places,** such as the list price, sale price and
  final value, so each value has to be tied to the right row and column.
- **Rating codes** for quality and condition (for example Q4 and C4).
- **A defects table** with a Yes/No column and repair cost estimates, some left blank.
- **Grey placeholder boxes** where the photos, sketch and charts would appear.
