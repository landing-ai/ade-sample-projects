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
was an image** and was deleted with `redact.py --remove-images`. The signatory is not named
on the page; their title and the team mailbox beneath the signature stay. The company's
letterhead, office address, phone, GST and CIN numbers stay, as do the start date and the
designation.

**Verified:** no original identifier is extractable from the committed PDF, no image
remains in the signature area, and no original identifier appears anywhere in this folder.
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

## Featured fields: what a verifier reads

All on **page 1**, which the request asked for. The request named no fields, so these
were chosen:

| Field | Value |
|---|---|
| Letter date | April 25, 2022 |
| Employer (sign-off) | Deloitte Consulting India Private Limited |
| Designation | XIN-DC SENIOR CONSULTANT |
| Purpose | current proof of employment |
| Signatory title | Executive Manager |

When the letter was issued, by whom, for what role, for what purpose, and who signed it.
No person is featured. The start date grounds to the same line as the designation and
would render an identical crop, so it is left out; the designation's crop shows both. The
employer's name is pinned to the sign-off line rather than the letterhead.

## What it surfaced

**Everything extracts correctly,** all 13 fields, including the purpose paraphrased from
the closing sentence and the employee's name without its "Mr.".

**Two values share one line.** The start date and the designation are in the same
sentence and ground to the same line, so they cannot be featured side by side.

**Addresses ground line by line.** Both the residential and the office address come back
with one range per line, and `currently_employed` grounds to the sentences that state it;
the consistency check flags all three.

## Extraction

`schema.json` was written for this letter, with **13 leaf fields**: the letter date, the
employer (name, office location, phone, signatory title, contact email), the employee
(name, ID, start date, designation, current employment, residential address) and the
purpose. Everything populates, with no warnings.

## Cost

**1.90 credits** at standard tier for 1 page: 0.90 to parse, 1.00 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo.
# --remove-images arrives with the employment-offer-letter PR; until it is merged, run
# that branch's redact.py for the image and this one for the text.
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/employment-verification-letter/source/employment-verification-letter-redacted.pdf \
    --rules <outside-the-repo>/rules.json --remove-images 1:50,535,192,598

.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter                # 1.90 credits
.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter --extract-only # 1.00, schema iteration
.venv/bin/python document-types/scripts/build_images.py employment-verification-letter           # free
.venv/bin/python document-types/scripts/inspect_fields.py employment-verification-letter --page 1
```
