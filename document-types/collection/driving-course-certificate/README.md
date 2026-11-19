# Driving Course Certificate

**On the website:** [landing.ai/document-type/driving-course-certificate](https://landing.ai/document-type/driving-course-certificate)

A State of Texas Driving Safety Course Uniform Certificate of Completion, issued after
a six-hour defensive driving course approved by the Texas Department of Licensing and
Regulation. The page prints the certificate twice, a court copy above an insurance copy.
Each gives the certificate number, the student, the course provider, the completion and
issue dates and the reason for the course, and the court copy adds the court it is filed
with.

| | |
|---|---|
| Pages | 1 |
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
| Processed (UTC) | 2026-11-19 02:50 | 2026-11-19 02:57 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,081 | 3,545 |
| Words under 0.95 confidence | 16 | n/a |
| Words under 0.80 confidence | 8 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.4 s | 13.5 s |
| Per page | 3.4 s | 13.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.5 credits | 1.4 credits |
| Per page | 0.50 credits | 1.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:50 | 2026-11-19 02:58 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 21 | 21 |
| Non-null fields returned | 21 | 21 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 275.4 s | 83.5 s |
| Per schema field (21) | 13.11 s | 3.98 s |
| Per value returned | 12.52 s | 3.80 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.4 credits | 1.5 credits |
| Per schema field (21) | 0.067 credits | 0.071 credits |
| Per value returned | 0.064 credits | 0.068 credits |

## Origin

`source/texas-driving-safety-course-certificate-redacted.pdf` is a **State of Texas
Driving Safety Course Uniform Certificate of Completion**. A Texas driver gets one after
a six-hour driving safety (defensive driving) course approved by the Texas Department of
Licensing and Regulation (TDLR). The course provider issues it, and the driver files it
with a court to dismiss a traffic ticket or sends it to an insurer for a discount. It is
**1 page, portrait**, a fillable form with a text layer.

The sample was issued for a traffic ticket in an Ellis County municipal court. The course
was completed and the certificate issued on 24 January 2022. Both signature lines are
blank.

| | |
|---|---|
| Publisher | TDLR uniform certificate form, issued by a TDLR-approved course provider. Uploaded to Scribd by a third party |
| Source | [scribd.com/document/998399674](https://www.scribd.com/document/998399674) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | Redacted |

The Scribd account that uploaded it is not the issuer. This is a real student's record,
not a publisher's sample. The Scribd listing URL ends in a slug that was the student's
driver licence number, so the URL recorded here is the bare document ID with the slug
removed.

**Redaction.** The certificate carried the student's real identity. The values live in
fillable form fields, so each was replaced in the field value and in how it displays:

| What | Replaced with | Count |
|---|---|---|
| Student's name (Last, First), panel and mailing block of both copies | `Sample, Jane` | 4 |
| Student's street address | `100 Main St.` | 2 |
| Certificate number (TDLR can look it up) | `CP275-63203533`, randomly drawn | 2 |
| Student's Texas driver licence number | `89449885`, randomly drawn | 2 |
| Student's date of birth | `08/23/1984` | 2 |

Kept: city, state and ZIP; the court; the course provider's trade name, school-classroom
code and instructor licence number; the dates; and the reason. The PDF metadata carried
the form designer's name and was cleared. The file's owner-password encryption was
dropped. The originals are not recorded anywhere in this folder, and the rules file stays
outside the repo. The result was verified by a text check, by eye on a render, and by a
sweep of every file in this folder.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Texas drivers take a driving safety course to have a traffic ticket dismissed or to
lower their insurance premium, and this uniform certificate is the proof they hand in.

- **Municipal and justice courts:** clerks check the certificate against the citation
  before dismissing the ticket.
- **Auto insurers:** they apply a defensive-driving discount once the insurance copy
  arrives.
- **Driving safety course providers:** they issue and track certificates for each
  student who completes a course.
- **State regulators:** TDLR sets the form and runs a service to verify certificate
  numbers.
- **Employers with driving roles:** fleet operators may ask drivers for proof of a
  completed course.

### What it contains

- **Every value printed twice.** The court and insurance copies repeat the same
  certificate, divided by a dashed cut line. A Court Information block appears only on
  the court copy.
- **A large grey watermark** of the TDLR logo behind both copies, cutting through the
  warning footer and the middle of each copy.
- **Letter-spaced text that wraps:** the provider name reads `F R E E - C E R` /
  `T I F I C A T E`.
- **Fillable form fields** in a right-hand panel, each with an empty "Changed from:" line
  under it.
- **Blank signature lines,** one with an orange SIGN tab beside it.
