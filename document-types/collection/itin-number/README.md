# ITIN number

Source assets for `landing.ai/document-type/itin-number`.

## Sample document

`source/itin-assignment-notice-redacted.pdf` — a letter presented as an IRS notice CP565,
assigning an Individual Taxpayer Identification Number, dated 11/05/2023, redacted.
**1 page, A4 portrait (595×842)**, with a full text layer, the IRS eagle logo and a
Treasury seal watermark.

| | |
|---|---|
| Publisher | Presented as the Internal Revenue Service (see below) |
| Source | [scribd.com/document/894287956](https://www.scribd.com/document/894287956) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

## This is probably not a genuine IRS notice

It is used at the document owner's decision, and the page should not present it as an
authentic notice. Four things point the other way:

- **It was made in a word processor.** The PDF was created in Apple Pages on a
  Russian-language macOS ("macOS Версия 13.2.1"). IRS notices come from IRS print systems.
- **It names two different people.** The header's "Recipient:" and the mailing address
  block name different people.
- **The ITIN was not a valid ITIN.** Its middle group was outside the ranges the IRS
  assigns (50–65, 70–88, 90–92, 94–99).
- **The dates disagree.** The file was created on 11 May 2023, which matches the notice
  date "11/05/2023" only when read day-first; US notices are written month-first, where
  11/05/2023 is 5 November. The format is also not the IRS's current CP565, whose official
  sample is [irs.gov/pub/notices/cp565_english.pdf](https://www.irs.gov/pub/notices/cp565_english.pdf).

The official IRS sample would be the stronger source for this page: it is public, filled
with specimen data ("JOHN SMITH"), and needs no redaction, though it prints the ITIN itself
as the placeholder "NNN-NN-NNNN".

## Redaction

The letter was uploaded to Scribd by a third party and names real-looking people, so it is
treated as a personal record. Scribd blocks scripted requests, so the file was downloaded
by hand. **The source url is recorded in its id-only form**: Scribd's full url adds a title
slug, and this one carried a person's name.

Seven text identifiers were replaced using `document-types/scripts/redact.py`, which
removes the underlying text rather than covering it. Names and the address are obviously
fake; numbers are plausible random stand-ins of the same shape:

| What | Replaced with |
|---|---|
| Recipient name in the header | Jane Q Sample |
| Name in the mailing address block | JOHN Q SAMPLE |
| Mailing address, street | 10 MAIN ST APT 1 |
| Mailing address, city, state and ZIP | ANYTOWN, NJ 00000 |
| ITIN | 981-93-3299 |
| Case reference number | 77582342621020 |
| Mail sort code line | 287327.453204.6306.386 6 MB 3.797 130 |

**The ITIN stand-in is in a range the IRS does not assign**: middle group 93, the same idea
as the SSA's advertising block for SSNs, so it looks like an ITIN but can belong to no one.

**The Intelligent Mail barcode was an image** encoding the mail's routing, and was deleted
with `redact.py --remove-images`. The PDF metadata was also cleared; its title named a
person. The IRS seal, logo and contact details are left as printed.

The replacements are in Helvetica among Calibri, so a few lines are visibly a different
size from their neighbours.

**Verified:** no original identifier is extractable from the committed PDF, no image
remains in the barcode area, and no original identifier appears anywhere in this folder.
The original values are deliberately not recorded here or in `manifest.json`. The rules
file used by `redact.py` stays outside the repo.

## Why this document

The collection's first **tax identification notice**: a short government letter whose
point is one number, printed large in the middle of the page, with the notice's
identifiers in a labelled block at the top right.

## Featured fields: the notice and the number it assigns

All on **page 1**. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| ITIN | 981-93-3299 |
| Notice number | CP565 |
| Notice date | 11/05/2023 |
| Form | W-7 |
| Case reference number | 77582342621020 |

No person is featured. The ITIN and case reference shown are plausible stand-ins, not the
originals.

## What it surfaced

**Everything extracts correctly and grounds precisely.** All 12 fields come back right,
and every single-line value boxes exactly its line, including the large ITIN over the
Treasury seal watermark.

**The two names are kept apart.** The schema asks separately for the header recipient and
the mailing-block name, and extraction returns each from its own place rather than merging
them, which is how the inconsistency in the source shows up in the data.

**Addresses ground line by line.** Both the recipient's and the IRS's mailing addresses come
back with one range per line, so the consistency check flags them.

## Extraction

`schema.json` was written for this notice, with **12 leaf fields**: the ITIN, the notice
(number, date, form, case reference), the recipient (header name, mailing name, mailing
address) and the issuer (agency, assistance and international phone numbers, mailing
address). Everything populates, with no warnings.

## Cost

**2.30 credits** at standard tier for 1 page: 1.20 to parse, 1.10 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/itin-number/source/itin-assignment-notice-redacted.pdf \
    --rules <outside-the-repo>/rules.json --remove-images 1:134,159,328,180

.venv/bin/python document-types/scripts/run_ade.py itin-number                # 2.30 credits
.venv/bin/python document-types/scripts/run_ade.py itin-number --extract-only # 1.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py itin-number           # free
.venv/bin/python document-types/scripts/inspect_fields.py itin-number --page 1
```
