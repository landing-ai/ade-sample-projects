# ITIN number

Source assets for `landing.ai/document-type/itin-number`.

## Sample document

`source/irs-cp565-specimen.pdf` — the IRS's own published sample of Notice CP565, which
confirms an Individual Taxpayer Identification Number. **2 pages, US Letter portrait
(612×792)**, with a full text layer and the IRS eagle logo on both the letter and the
tear-off stub.

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [irs.gov/pub/notices/cp565_english.pdf](https://www.irs.gov/pub/notices/cp565_english.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

A work of the United States government, so it carries no copyright, served from irs.gov
and linked from the CP565 help page. Every value on it is specimen data the IRS printed
for illustration: the recipient is "JOHN SMITH" at "123 N HARRIS ST, HARVARD, TX 12345",
the case reference number is 99999, and **the ITIN itself is printed as the placeholder
`NNN-NN-NNNN`**. No real person's data appears, so no redaction was needed.

The PDF's metadata named the IRS employee who produced the file. That dictionary and the
XML metadata were cleared before committing. Nothing on the page was altered.

> On PyMuPDF 1.28, `doc.set_metadata({})` does not clear the `/Info` dictionary; the keys
> have to be set to empty strings explicitly. `redact.py` clears metadata correctly, and
> every redacted source in this collection was verified clean.

## This replaces an earlier sample

The previous source was a letter presented as a CP565, downloaded from a Scribd upload.
It was probably not a genuine IRS notice: the PDF was authored in Apple Pages on a
Russian-language macOS, the header recipient and the mailing-block name were two
different people, the ITIN's middle group fell outside every range the IRS assigns, and
the notice date parsed only day-first where US notices are month-first. It was also a
third party's personal record, redacted but not consented to.

A marketing page should not present a probably-forged notice as an authentic one, so the
IRS's own sample replaces it. The old file is removed here; it remains in git history.

## Why this document

The collection's first **tax identification notice**, and a letter that is mostly table:

- **99 parse blocks over two pages, of which 73 are table cells.** The header block, the
  ITIN and personal information table and the tear-off stub are all label-value grids.
- **Column headers printed below their values.** In the ITIN table, "First / Middle /
  Last" sits underneath the name it labels.
- **A tear-off stub that repeats the identifiers** and adds blank fields and a.m./p.m.
  checkboxes for the taxpayer to complete.
- **Identifiers repeat.** The notice number, notice date and case reference each print in
  the header block, again on the stub and again on the page 2 header.

## Featured fields: the notice and the number it confirms

All on **page 1**. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| ITIN | NNN-NN-NNNN |
| Notice number | CP565 |
| Notice date | January 26, 2017 |
| Case reference number | 99999 |
| Date of birth | January 20, 1990 |

No name is featured, although the specimen's name is the IRS's own illustrative data.
The ITIN's value is the placeholder the IRS prints, which is the real text on the real
page.

**The ITIN uses occurrence 1, not 0.** Occurrence 0 boxes `NNN-NN-NNN` where the headline
wraps across two lines; occurrence 1 boxes the full `NNN-NN-NNNN` on the second line.
`inspect_fields.py` marks the first `OFF` and the second `ok`.

## What it surfaced

**Everything extracts and grounds.** All 14 leaf fields populate, with no warnings and no
schema violation.

**The two printings of the name are kept apart.** The schema asks separately for the full
name in the ITIN table and the name in the mailing block, and extraction returns each
from its own place, including the difference in case.

**Addresses ground line by line.** Both mailing addresses come back with one range per
printed line, so a consistency check can compare them.

## Extraction

`schema.json` has **14 leaf fields**: the ITIN, the notice (number, date, form, case
reference, page marker), the recipient (full name, mailing name, mailing address, date of
birth) and the issuer (agency, assistance and international phone numbers, mailing
address).

## Cost

**3.80 credits** at standard tier for 2 pages: 2.30 to parse, 1.50 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py itin-number                # 3.80 credits
.venv/bin/python document-types/scripts/run_ade.py itin-number --extract-only # 1.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py itin-number           # free
.venv/bin/python document-types/scripts/inspect_fields.py itin-number --page 1
```
