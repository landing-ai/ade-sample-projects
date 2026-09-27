# SAT score report

Source assets for `landing.ai/document-type/sat-score-report`.

## Sample document

`source/sat-score-report-redacted.pdf` — a College Board SAT score report for the June 7,
2025 administration, redacted. **1 page, portrait (612×792).** Rendered from the College
Board website, with a full text layer: the header, the total and section scores, and the
Knowledge and Skills panel's eight content domains.

| | |
|---|---|
| Publisher | College Board |
| Source | [scribd.com/document/891396937/…](https://www.scribd.com/document/891396937/Sat-Score-Report-6-2025) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

## Redaction

This is a real student's report, uploaded to Scribd by a third party. Scribd is a
user-upload site, so the uploader is not the publisher, and the report is treated as a
personal record. Scribd also blocks scripted requests, so the file was downloaded by
hand and passed to the skill with `--file`.

The report carried two identifiers, and both were replaced using
`document-types/scripts/redact.py`, which removes the underlying text rather than
covering it:

| What | Replaced with |
|---|---|
| Student's name | Jane Q Sample |
| College Board record locator | 0000000000 |

The PDF metadata was also cleared. The scores are left as printed: with the name and
record locator gone, nothing on the page identifies the student. The QR code was decoded
and carries the generic link `satsuite.org/whatsnext`, not a personal one.

**Verified:** no original identifier is extractable from the committed PDF, and a sweep of
every file in this folder, on literals, name parts and bare digits, found none.

The original values are deliberately not recorded here or in `manifest.json`. The rules
file used by `redact.py` stays outside the repo.

**This sample fixed `redact.py`.** The script used to write the replacement inside the
redaction box, which is trimmed to avoid erasing the line above. On this page that left a
7pt box for 8.8pt bold text, and the name came out at 4.3pt in regular Helvetica, an
obvious edit. It now reads the size, weight and baseline of the text it replaces and
writes the replacement there after redacting.

## Why this document

The collection's first **education record**, and its densest one-page layout:

- **Scores in several visual forms.** Large numerals, percentile pills, stacked scale
  labels such as "400–" over "1600", small-print ranges and averages, and eight
  performance bands drawn as bar segments.
- **Repeated structure.** Two section panels built the same way, and eight content
  domains in two columns, so the schema has two arrays to fill and ground.
- **A clean text layer.** Like the arbitration award, so any grounding trouble comes from
  layout rather than from reading the page.

## Featured fields: one result

All on **page 1**:

| Field | Value |
|---|---|
| Total score | 1470 |
| Reading and Writing score | 680 |
| Math score | 790 |
| Test date | Jun 7, 2025 |

The two section scores sum to the total, so the overlay reads as a single result rather
than four unrelated numbers. No named individual is featured: the name and record locator
extract correctly, but the scores make the same point without them.

## What it surfaced

**Every value grounds to text containing it.** All 59 extracted leaves pass the
consistency check, including all eight content domains in both columns. That is a first
for the collection: `inspect_fields.py` flags at least some ranges on every other sample,
from 16 on the invoice to 287 on the investor presentation, and none here.

**But one box is on the wrong line, and only the crop showed it.** The total score's
"400–" / "1600" scale label is stacked on two lines beside the score, with the "96th"
percentile pill to its right. ADE split the stacked label into two atomic lines, gave
`400-1600` the upper line's box, and gave `96th*` the lower one, the "1600". The
percentile value is right and its range text reads "96th*", so the check passed, but the
crop showed the scale label. Percentiles are not featured. This is the reason Step 8 of
the skill says to open every image.

**Identical panels, different boxes.** The two section panels are laid out the same way,
but the Reading and Writing score gets a tight box around "680", while the Math score's
box spans the whole line: "790 | 200–800 | 99th*". Both contain the value.

**Small print is extractable but not showable.** The score range and 3-year average lines
are about 7pt. They extract and ground correctly, but at crop size the highlight border
covers most of the text, so they are not featured.

## Extraction

`schema.json` was written for this page, with **19 leaf fields** in five groups:
`student` (name, grade, record locator), `test` (administration, test date),
`total_score` (score, percentile, range, average), `section_scores[]` (five fields per
section) and `knowledge_and_skills[]` (five fields per domain). Everything populates, with
no warnings.

## Cost

**3.20 credits** at standard tier for 1 page: 1.10 to parse, 2.10 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/sat-score-report/source/sat-score-report-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py sat-score-report                # 3.20 credits
.venv/bin/python document-types/scripts/run_ade.py sat-score-report --extract-only # 2.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py sat-score-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py sat-score-report --page 1 --good
```
