# High school transcript

Source assets for `landing.ai/document-type/high-school-transcript`.

## Sample document

`source/nyc-doe-high-school-transcript-redacted.pdf`: a New York City Department of
Education student transcript (an "unofficial student copy") from Tottenville High School,
printed June 26, 2023, redacted. **1 page, portrait (612×796).** It is page 1 of 2; only
that page was uploaded. The source is a phone scan with **no text layer**: one JPEG,
slightly skewed, with a fold shadow down the right edge.

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

## Redaction

This is a real student's transcript, uploaded to Scribd by a third party. Scribd is a
user-upload site, so the uploader is not the publisher, and the transcript is treated as
a personal record. Scribd also blocks scripted requests, so the file was downloaded by
hand and passed to the skill as a local file.

Because the page is a raster scan, the replacements were made in the pixels with
`document-types/scripts/redact_scan.py`, which rebuilds the page from the edited image
alone, so the original raster is not carried into the committed PDF:

| What | Replaced with |
|---|---|
| Student's name | SAMPLE, JANE |
| Student ID number | 417948620 (digits drawn at random by `plausible.py`) |
| House number and street name | 100 MAIN (the word STREET kept as printed) |
| City | ANYTOWN |
| ZIP code | 12345 |
| Date of birth | 03/14/2005 (year kept) |
| Guidance counselor's name | EXAMPLE PAT |

OCR could not read most of the header on this skewed scan, so most of these were placed
by coordinates (`--place`) rather than found by matching text. The street was done in two
passes, erase first and then place: measured on the slanted original, the stand-in came
out about 40% too tall. The school name, courses, marks and averages are left as printed.
With the name, ID, address and date of birth gone, nothing on the page names the student.

Before redaction, the scan's JPEG was moved unchanged onto a 612 × 796 pt page. The
source page measured 1833 × 2385 pt, one point per pixel, and `redact_scan.py` rebuilds
at 300 dpi, so the full-size page would have come out as a 7.4 MB PDF. At letter width
the rebuild stays close to the scan's own resolution, and the file is 1.7 MB.

The PDF metadata was cleared. Nothing in the metadata identified the student; it named
only the iOS PDF producer and the date the scan was made.

**Verified:** `redact_scan.py` re-OCRs its output and found no original value, compared as
literals and as bare digits. The header was also checked by eye at 300 dpi, and every file
in this folder was swept.

The original values are deliberately not recorded here or in `manifest.json`. The rules
file stays outside the repo.

## Why this document

The collection's first **academic transcript**, and its first **two-column scan**:

- **A scan, not a rendered PDF.** Like the motor vehicle report and the foreclosure
  judgment, there is no text layer to fall back on. Everything comes from reading pixels,
  on a page photographed slightly askew.
- **A table that breaks across columns.** The 2020 Term 2 block starts at the bottom of
  the left column and finishes at the top of the right one: one course, the term's credit
  totals and its average carry over, and sit above the next term's heading.
- **Codes and flags in the margins.** Marks carry `*` (not averaged) and course codes
  carry `**` (weighted course). Both are defined only in the page footer, and the schema
  asks for each as a boolean.
- **Repeated structure.** Eight terms and 55 course rows, so the schema has a nested
  array to fill and ground.

## Featured fields: one term across two columns

All on **page 1**, all from 2020 Term 2:

| Field | Value | Where |
|---|---|---|
| Term year | 2020 | heading, bottom of the left column |
| Course carried to the next column | CHEMISTRY TERM 2 | top of the right column |
| Mark | 73 | top of the right column |
| Term credits averaged | 7.00 | right column |
| Term average | 75.43% | right column |

The overlay shows ADE putting a term back together from both columns. The heading and six
courses are on the left. The seventh course and the totals are on the right, above the
next term. Extraction put all seven courses and the totals in the same term, which is how
a person reads the page. The credit total matches the seven 1.00-credit courses, 7.00.
No named individual is featured.

## What it surfaced

**The column break was handled.** The term that spans both columns has all seven courses
and its totals in the right entry, and none of the course rows were dropped or duplicated.
All 55 rows extract, with the course titles exactly as printed, truncations included
("ST JOHNS PRE CALCUI", "BEGINNING ORCHESTF").

**Totals for the carried-over term ground OFF.** For 2020 Term 2, the credits attempted
and credits earned values (7.00 / 7.00) are correct but have empty ranges. The same
fields ground correctly for the other seven terms. Term credits averaged, from the next
line, grounds correctly and is featured instead.

**The asterisk flags are the weakest leaves.** In 2022 Term 1, both weighted courses
(pre-calculus and AP Biology, each marked `**` beside the course code) came back with
`weighted: false` and `not_averaged: true`. The flag was attached to the wrong column.
The same two courses one term later are read correctly. Booleans have no text to box in
any case, so none are featured.

**Boxes are a little high on the right column.** The scan is skewed, and the boxes on the
right column sit slightly above their text. They still contain it, and every featured crop
was checked by eye.

**Blank fields come back as empty strings.** Discharge date and graduation date are blank
on the page and extract as `""` rather than null, grounded to their labels.

## Extraction

`schema.json` was written for this page, with **30 leaf fields** in three groups:
`issuer` (issuing authority, school, transcript type, print time), `student` (eleven
header fields) and `terms[]` (year, term, four totals, and `courses[]` with nine fields
per course). Everything populates, with no warnings.

## Cost

**18.40 credits** at standard tier for 1 page: 3.10 to parse and 15.30 to extract.
Extraction is most of the cost because of the 55-row course array.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo.
# 1. Move the scan's JPEG unchanged onto a 612 pt wide page (PyMuPDF insert_image).
# 2. Pass 1: replace the name, ID, city, ZIP, date of birth and counselor, and erase
#    the street number and name.
.venv/bin/python document-types/scripts/redact_scan.py <letter>.pdf <pass1>.pdf \
    --rules <outside-the-repo>/rules.json \
    --font "/System/Library/Fonts/Supplemental/Times New Roman.ttf" \
    --bold-font "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf" \
    --bold ... --place ... --erase ...
# 3. Pass 2: place the street stand-in, at a set height, on the erased area.
.venv/bin/python document-types/scripts/redact_scan.py <pass1>.pdf \
    document-types/collection/high-school-transcript/source/nyc-doe-high-school-transcript-redacted.pdf \
    --rules <outside-the-repo>/rules.json \
    --font "/System/Library/Fonts/Supplemental/Times New Roman.ttf" --place ...

.venv/bin/python document-types/scripts/run_ade.py high-school-transcript                # 18.40 credits
.venv/bin/python document-types/scripts/run_ade.py high-school-transcript --extract-only # 15.30, schema iteration
.venv/bin/python document-types/scripts/build_images.py high-school-transcript           # free
.venv/bin/python document-types/scripts/inspect_fields.py high-school-transcript --page 1 --good
```
