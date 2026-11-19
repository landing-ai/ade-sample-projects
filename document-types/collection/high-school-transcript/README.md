# High school transcript

**On the website:** [landing.ai/document-type/high-school-transcript](https://landing.ai/document-type/high-school-transcript)

An unofficial student copy of a New York City Department of Education transcript from
Tottenville High School, printed June 26, 2023. It holds a student record block and
eight terms of coursework, 2019 to 2022, laid out in two columns. Each term lists its
courses with marks and credits, then the term's credit totals and average. The student's
identifying details were replaced with stand-in data.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 30 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:15 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 10,395 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 12.6 s |
| Per page | 12.6 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 3.1 credits |
| Per page | 3.10 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:15 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 30 |
| Non-null fields returned | 28 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 220.1 s |
| Per schema field (30) | 7.34 s |
| Per value returned | 0.40 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 15.3 credits |
| Per schema field (30) | 0.510 credits |
| Per value returned | 0.028 credits |

## Origin

`source/nyc-doe-high-school-transcript-redacted.pdf` is a New York City Department of
Education student transcript (an "unofficial student copy") from Tottenville High School,
printed June 26, 2023, redacted. It is **1 page, portrait (612×796)**. It is page 1 of 2;
only that page was uploaded. The source is a phone scan with **no text layer**: one
JPEG, slightly skewed, with a fold shadow down the right edge.

The page holds a student record block, a message area, and eight terms of coursework,
2019 Term 1 to 2022 Term 2, laid out newest first in two columns. Each term lists its
courses (school code, course code, title, actual mark, numeric equivalent, credits
attempted / earned), then the term's credit totals and its average.

| | |
|---|---|
| Publisher | New York City Department of Education |
| Source | [scribd.com/document/838946806/…](https://www.scribd.com/document/838946806/High-School-Transcript) |
| Retrieved | 2026-10-26, downloaded manually |
| Clearance | Redacted |

This is a real student's transcript, uploaded to Scribd by a third party. Scribd is a
user-upload site, so the uploader is not the publisher, and the transcript is treated as
a personal record. Scribd also blocks scripted requests, so the file was downloaded by
hand.

Because the page is a raster scan, the replacements were made in the pixels, and the
page was rebuilt from the edited image alone, so the original raster is not carried into
the committed PDF:

| What | Replaced with |
|---|---|
| Student's name | SAMPLE, JANE |
| Student ID number | 417948620 (digits drawn at random) |
| House number and street name | 100 MAIN (the word STREET kept as printed) |
| City | ANYTOWN |
| ZIP code | 12345 |
| Date of birth | 03/14/2005 (year kept) |
| Guidance counselor's name | EXAMPLE PAT |

OCR could not read most of the header on this skewed scan, so most of these were placed
by coordinates rather than found by matching text. The school name, courses, marks and
averages are left as printed. With the name, ID, address and date of birth gone, nothing
on the page names the student.

Before redaction, the scan's JPEG was moved unchanged onto a 612 × 796 pt page, so the
rebuilt page stays close to the scan's own resolution. The PDF metadata was cleared.
Nothing in the metadata identified the student; it named only the iOS PDF producer and
the date the scan was made.

**Verified:** an OCR pass over the output found no original value, compared as literals
and as bare digits. The header was also checked by eye at 300 dpi, and every file in this
folder was swept. The original values are deliberately not recorded here or in
`manifest.json`. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A high school transcript is the record of a student's courses, grades and credits. It is
read whenever a student moves on to college, a job or another school.

- **College admissions:** admissions offices read courses, marks and averages to
  evaluate applicants, often recalculating a GPA on their own scale.
- **Scholarship and financial aid programs:** reviewers check grades and credits against
  eligibility rules.
- **School districts and registrars:** they evaluate transfer students' credits toward
  graduation requirements.
- **Credential evaluation services:** they convert transcripts into equivalent grades
  and credits for other institutions.
- **Employers and the military:** some require proof of graduation or completed
  coursework.

### What it contains

- **A phone scan with no text layer,** slightly skewed, with a fold shadow.
- **A two-column layout,** with terms laid out newest first.
- **A term that breaks across columns,** starting at the bottom of the left column and
  finishing at the top of the right one.
- **Repeated tables:** eight terms and 55 course rows, each with codes, marks and
  credits.
- **Flags defined only in the footer,** such as `*` on marks that are not averaged and
  `**` on weighted course codes.
- **A student record block** with labelled header fields.
