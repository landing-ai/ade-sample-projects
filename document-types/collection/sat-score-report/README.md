# SAT score report

**On the website:** [landing.ai/document-type/sat-score-report](https://landing.ai/document-type/sat-score-report)

A College Board SAT score report for the June 7, 2025 administration, with the student's
name and record locator replaced. It gives the total score and the Reading and Writing
and Math section scores, each with its percentile, score range and averages, and a
Knowledge and Skills panel with performance bands for eight content domains.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 19 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:33 | 2026-11-19 03:51 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,531 | 1,944 |
| Words under 0.95 confidence | 1 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.2 s | 11.7 s |
| Per page | 7.2 s | 11.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.0 credits |
| Per page | 0.50 credits | 1.00 credits |

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
| Fields requested | 19 | 19 |
| Non-null fields returned | 18 | 19 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 113.8 s | 54.5 s |
| Per schema field (19) | 5.99 s | 2.87 s |
| Per value returned | 1.96 s | 0.92 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.2 credits | 2.1 credits |
| Per schema field (19) | 0.116 credits | 0.111 credits |
| Per value returned | 0.038 credits | 0.036 credits |

## Origin

`source/sat-score-report-redacted.pdf` is a College Board SAT score report for the June
7, 2025 administration, redacted. It is **1 page, portrait (612×792)**, rendered from
the College Board website, with a full text layer: the header, the total and section
scores, and the Knowledge and Skills panel's eight content domains.

| | |
|---|---|
| Publisher | College Board |
| Source | [scribd.com/document/891396937/…](https://www.scribd.com/document/891396937/Sat-Score-Report-6-2025) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

This is a real student's report, uploaded to Scribd by a third party. Scribd is a
user-upload site, so the uploader is not the publisher, and the report is treated as a
personal record. Scribd also blocks scripted requests, so the file was downloaded by
hand.

The report carried two identifiers, and both were replaced with a redaction that removes
the underlying text rather than covering it:

| What | Replaced with |
|---|---|
| Student's name | Jane Q Sample |
| College Board record locator | 0000000000 |

The PDF metadata was also cleared. The scores are left as printed: with the name and
record locator gone, nothing on the page identifies the student. The QR code was decoded
and carries the generic link `satsuite.org/whatsnext`, not a personal one.

**Verified:** no original identifier is extractable from the committed PDF, and a sweep
of every file in this folder, on literals, name parts and bare digits, found none. The
original values are deliberately not recorded here or in `manifest.json`, and the
redaction rules file stays outside the repo. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

SAT score reports move between students, schools and the organizations that award
places and money on the basis of them.

- **College admissions offices:** staff record total and section scores, often from
  student-submitted copies of the report.
- **Scholarship and financial aid programs:** reviewers check scores against merit
  award thresholds.
- **High school counselors:** they track results to advise on applications and retakes.
- **Test prep and tutoring companies:** they compare section and domain results across
  attempts to plan instruction.
- **Education researchers and districts:** they analyze results across many students.

### What it contains

- **Scores in several visual forms:** large numerals, percentile pills, stacked scale
  labels such as "400–" over "1600", and small-print ranges and averages.
- **Performance bands drawn as bar segments** for each content domain.
- **Repeated structure.** Two section panels are built the same way, and eight content
  domains sit in two columns.
- **Values that must agree.** The two section scores sum to the total.
- **Small print** of about 7pt for score ranges and averages.
- **A QR code** and a full text layer.
