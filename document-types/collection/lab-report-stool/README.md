# Stool test report

**On the website:** [landing.ai/document-type/lab-report-stool](https://landing.ai/document-type/lab-report-stool)

Mosaic Diagnostics' published sample of its Stool Chemistries panel, filled with
specimen data. Page 1 has the order, patient and sample collection details over a
results table of 18 analytes in six sections, each with its result, unit, reference
interval and a range bar. Page 2 explains each analyte, and page 3 is the lab's
written commentary.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:14 | 2026-11-19 03:27 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 13,303 | 12,503 |
| Words under 0.95 confidence | 24 | n/a |
| Words under 0.80 confidence | 13 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.2 s | 17.8 s |
| Per page | 2.4 s | 5.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.8 credits | 4.7 credits |
| Per page | 0.60 credits | 1.57 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:14 | 2026-11-19 03:28 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 158.8 s | 120.4 s |
| Per schema field (23) | 6.91 s | 5.23 s |
| Per value returned | 1.32 s | 1.00 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.9 credits | 5.7 credits |
| Per schema field (23) | 0.257 credits | 0.248 credits |
| Per value returned | 0.049 credits | 0.048 credits |

## Origin

`source/mosaic-stool-chemistries-sample.pdf` is a **Stool Chemistries** report, Mosaic
Diagnostics' published sample of its stool chemistry panel. It is **3 pages, portrait**,
a native PDF with a text layer. Page 1 has a three-box header (order, patient, sample
collection) over one results table of 18 analytes in six sections: digestion and
absorption, inflammation, immunology, short-chain fatty acids, intestinal health markers
and macroscopic appearance. Each row has its result, unit and reference interval, plus a
colored Low / Within / High range bar with a triangle marking the result. Page 2 explains
each analyte; page 3 is the lab's written commentary.

| | |
|---|---|
| Publisher | Mosaic Diagnostics (formerly Great Plains Laboratory); analyzed by Doctor's Data, Inc. |
| Source | [mosaicdx.com/…/MDX_Report_StoolChemistries_ENG.pdf](https://mosaicdx.com/wp-content/uploads/2026/07/MDX_Report_StoolChemistries_ENG.pdf) |
| Linked from | [Sample Test Reports](https://mosaicdx.com/resource/stool-chemistry-test-sample-report/) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

Mosaic links the PDF from its Sample Test Reports resource page, alongside Japanese,
Portuguese and Spanish versions. It is specimen data throughout: "Sample Patient",
"Sample Doctor, MD", IDs of 999999 and "123 Main St." The PDF carries no copyright or
reuse notice, and Mosaic's site states no reuse restriction. It is used unaltered.

**One caveat on terms, accepted by the operator.** The report is analyzed by Doctor's
Data, Inc., and its footer names that lab and its director. Doctor's Data's own website
terms restrict that site's content to non-commercial use. This copy is hosted and
published by Mosaic, not by Doctor's Data, and the operator accepted it on that basis.

**This replaces the request's original source.** The request first pointed at Nordic
Laboratories' GI-MAP sample report, whose footer limits reproduction to personal use and
prohibits commercial reproduction; the operator rejected it. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A stool test report gives the results of a laboratory panel on a stool sample, used to
assess digestion, inflammation and gut health. It moves between the lab, the ordering
clinician and anyone who pays for or reviews the test.

- **Clinical practices:** gastroenterologists, primary care and functional medicine
  practitioners read the results and enter them into the patient's chart.
- **Clinical laboratories:** labs issue these reports and send the results to ordering
  providers and their systems.
- **Health insurance and claims review:** payers check the tests ordered and the results
  when reviewing claims.
- **Clinical research:** researchers collect gut-health markers across patients for
  studies.
- **Electronic health record integration:** health IT teams map PDF lab results into
  structured data when no electronic feed exists.

### What it contains

- **A range-bar graphic in every row,** between the unit and the reference interval,
  with the result marked by a triangle whose color carries the interpretation. No `L`
  or `H` letter is printed.
- **A results table split into six sections,** each with its own header row.
- **Comparators in results and intervals,** such as `>500`, `<10`, `> 200` and `≤ 500`.
- **Qualitative and quantitative results side by side:** "Negative", "None", "Brown" and
  "Soft" next to numbers with units.
- **Footnote markers** (`*`, `†`, `‡`) attached to analyte names, and Greek letters such
  as β-glucuronidase.
- **A three-box header** with order, patient and sample collection details.
- **Prose pages** explaining each analyte and giving the lab's commentary.
