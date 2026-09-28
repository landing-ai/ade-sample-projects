# Employment verification letter

Source assets for `landing.ai/document-type/employment-verification-letter`.

## Sample document

`source/employment-verification-letter-redacted.pdf` — an employment certificate issued by
Deloitte Consulting India on April 25, 2022, confirming an employee's start date,
designation and residential address "as per our records", redacted. **1 page, portrait
(612×792)**, produced from Adobe LiveCycle, with a full text layer and the Deloitte logo.

| | |
|---|---|
| Publisher | Deloitte Consulting India Private Limited (employer) |
| Source | [scribd.com/document/571883179/Employment-Letter](https://www.scribd.com/document/571883179/Employment-Letter) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

This sample replaces an earlier one for the same slug, a small contractor's letter.

## Redaction

This is a real certificate, uploaded to Scribd by a third party. Scribd is a user-upload
site, so the uploader is not the publisher, and the letter is treated as a personal
record. Scribd also blocks scripted requests, so the file was downloaded by hand.

Personal data was removed using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it:

| What | Replaced with |
|---|---|
| Employee's full name | Johnathon Q Samplewood |
| Employee ID | 00000000 |
| Residential address, first line | Plot no:000, Sample Green Park, |
| Residential address, locality | Anytown, |
| Residential address, city and PIN code | Hyderabad, Telangana, 000000, IN |

The city is kept: the office is in Hyderabad too. **The signatory's handwritten signature
is kept**, at the document owner's request, so the page can show signature detection. It
is illegible, and the signatory is not named anywhere on the page; their title and the team
mailbox beneath the signature stay. The company's
letterhead, office address, phone, GST and CIN numbers stay, as do the start date and the
designation.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder.
The original values are deliberately not recorded here or in `manifest.json`. The rules
file used by `redact.py` stays outside the repo.

**This sample fixed two bugs in `redact.py`.** The name is bold, in a justified line, over
a tightly set second line:

- **Replacements drawn three times.** On a justified line the spaces are wider than the
  font's own, and PyMuPDF returns one rectangle per word. Each got its own copy of the
  replacement, drawn on top of one another. The script now merges a match's rectangles on
  the same line into one.
- **The line below erased.** PyMuPDF removes every character whose box touches the
  redaction rectangle, and a character's box is the font's full height. The second line's
  characters overlapped the name's rectangle, and "2017 and is currently designa" was
  erased from under it. The script now redacts a band through the middle of the matched
  letters, which still takes every character of the match and nothing on the lines above
  or below.

The replacement name was chosen by width, "Johnathon Q Samplewood" at 126.1pt against the
original's 126.2pt in the same Helvetica Bold, so the justified sentence still reads
without a gap.

## Why this document

A letter from a large employer, set as a certificate: the facts are in two justified
sentences ("…is employed with our organization since June 05, 2017 and is currently
designated as XIN-DC SENIOR CONSULTANT.") and in address blocks, not in labelled fields.
It shows extraction reading values out of running prose, and the redaction problems that
justified, tightly set text causes.

## Featured fields: the letter and its attestation

All on **page 1**, which the request asked for. The request named no fields, so these
were chosen:

| Field | Value |
|---|---|
| Letter date | April 25, 2022 |
| Employer (letterhead) | Deloitte Consulting India Private Limited |
| Designation | XIN-DC SENIOR CONSULTANT |
| Signed | true |
| Signature date | 04.25.2022; 19:22:46 IST |

When the letter was issued, by whom, for what role, and whether and when it was signed. No
person is featured.

**Signed** is the attestation. It grounds to the parse's `[SIGNED]` label, whose box is
exactly the signature image, so the crop shows the signature itself beside "true".
`build_images.py` flags it because the word "true" is not on the page, which is expected
for a yes-or-no value; the crop was checked by eye.

The start date grounds to the same line as the designation and would render an identical
crop, so it is left out; the designation's crop shows both. The employer's name grounds
only to the letterhead in this run, so it is pinned there.

## What it surfaced

**The parse labels the signature.** DPT-3 marks the signature block `[SIGNED]` and
`[ILLEGIBLE_SIGNATURE]` in the markdown, so extraction can answer "is this signed?" with a
location: the signature image. It does not guess a name from an unreadable signature:
`signed_by` is null, which is correct, since no name is printed.

**The signature date is a separate stamp.** "Date: 04.25.2022; 19:22:46 IST", in small type
under the signature, extracts and grounds exactly. It is the signing time, distinct from the
letter date at the top.

**Titles spread over lines are joined.** The signer's title is printed on three lines
("Executive Manager", "Employee Life Cycle Events", "Core Talent Services"), and
`signer_title` returns them as one value with one range per line, so it is flagged.

**Two values share one line.** The start date and the designation are in the same sentence
and ground to the same line, so they cannot be featured side by side.

**Everything extracts correctly,** all 16 fields, including the purpose paraphrased from
the closing sentence and the employee's name without its "Mr.". Addresses ground line by
line and `currently_employed` grounds to the sentences that state it, so the consistency
check flags them; 10 of the 23 rows in the grounding check are `ok`.

## Extraction

`schema.json` was written for this letter, with **16 leaf fields**: the letter date, the
employer (name, office location, phone, contact email), the employee (name, ID, start
date, designation, current employment, residential address), the purpose, and a
`signatures` array with `is_signed`, `signature_date`, `signed_by` and `signer_title` for
each signature block. The array was added at the document owner's request, to show
attestation. Everything populates, with no warnings.

## Cost

**2.00 credits** at standard tier for 1 page: 0.90 to parse, 1.10 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo.
# The signature image is kept, so no --remove-images.
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/employment-verification-letter/source/employment-verification-letter-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter                # 2.00 credits
.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter --extract-only # 1.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py employment-verification-letter           # free
.venv/bin/python document-types/scripts/inspect_fields.py employment-verification-letter --page 1
```
