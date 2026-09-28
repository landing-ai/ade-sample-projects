# Employment verification letter

Source assets for `landing.ai/document-type/employment-verification-letter`.

## Sample document

`source/employment-verification-letter-redacted.pdf` — a letter from a small contracting
business confirming an employee's job, start date, pay and duties, dated 07/03/2025,
redacted. **1 page, portrait (612×792)**, written in LibreOffice, with a full text layer
and the company logo as an image.

| | |
|---|---|
| Publisher | Premier Contracting Service, LLC (employer) |
| Source | [scribd.com/document/884065116](https://www.scribd.com/document/884065116) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

## Redaction

This is a real letter, uploaded to Scribd by a third party. Scribd is a user-upload site,
so the uploader is not the publisher, and the letter is treated as a personal record.
Scribd also blocks scripted requests, so the file was downloaded by hand.

The employee's name was replaced using `document-types/scripts/redact.py`, which removes
the underlying text rather than covering it:

| What | Replaced with | Occurrences |
|---|---|---|
| Employee's full name | Johnathan Quincy Sampleton | 3 |
| Employee's first name, on its own | John | 1 |

The PDF metadata was also cleared; its `author` field named a person. **The source url is
recorded in its id-only form**, `scribd.com/document/884065116`: Scribd's full url adds a
title slug, and this one carried the employee's first name and last initial. The employer's
name, logo, address, phone numbers and email are business details, and the job title,
dates, pay and duties are left as printed.

**The replacement name was chosen by width.** Three of the four occurrences sit
mid-sentence, and the first replacement, "John Q Sample", left a visible gap before
", who is" because it was shorter than the name it replaced. "Johnathan Quincy Sampleton"
is 157.4pt wide in Helvetica against 157.8pt for the original, so the sentences close up.
The letter uses "he" and "his", so the stand-in is a male name.

**The typeface still differs.** The letter is set in DejaVu Sans, and `redact.py` writes
replacements in the standard PDF fonts, so the replaced name is visibly Helvetica, with a
smaller x-height. It reads as a different font, not a gap.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder. The original values are deliberately not recorded here
or in `manifest.json`. The rules file used by `redact.py` stays outside the repo.

## Why this document

The collection's first **letter**: the facts are written as prose and as a short list of
"Label: value" bullets, not laid out in a form or table. It shows extraction working from
running text, including values a reader has to interpret, such as a pay range
("$750.00-$800.00 weekly") split into a minimum, a maximum and a period, and "2023 to
Present" read as a start date and a current employee.

## Featured fields: what a verifier checks

All on **page 1**. The request named no feature page or fields, so these were chosen:

| Field | Value |
|---|---|
| Letter date | 07/03/2025 |
| Job title | Carpet Clean Tech |
| Employed since | 2023 |
| Weekly pay (lower end of range) | 750.00 |
| Duties | Carpet cleaning and repairs; compensated for jobs completed |

These are what a lender or landlord reads in such a letter. No person is featured. The
pay minimum, maximum and period all ground to the one Salary line and would render
identical crops, so only the lower end is featured.

## What it surfaced

**The bullets ground line by line.** Each list value boxes its whole bullet, label and
value together ("Salary: $750.00-$800.00 weekly"), which reads well beside the value.

**Statements ground to their sentences.** `currently_employed` and `in_good_standing`
extract correctly as true, and each grounds to the sentence that says so ("…who is
currently employed with…", "He is in good standing…"). That is good traceability, but a
sentence beside the word "True" is flagged, so neither is featured.

**Values given twice ground twice.** The phone number and email appear in the body and
again in the footer, and each comes back with both ranges. The employer address grounds
to its two footer lines separately.

**Everything is correct.** All 14 extracted values match the letter.

## Extraction

`schema.json` was written for this letter, with **14 leaf fields**: the letter date, the
employer (name, address, phone, email) and the employee (name, job title, start,
current employment, pay minimum, maximum and period, duties, good standing). Everything
populates, with no warnings.

## Cost

**1.70 credits** at standard tier for 1 page: 0.90 to parse, 0.80 to extract. The
cheapest sample in the collection.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/employment-verification-letter/source/employment-verification-letter-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter                # 1.70 credits
.venv/bin/python document-types/scripts/run_ade.py employment-verification-letter --extract-only # 0.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py employment-verification-letter           # free
.venv/bin/python document-types/scripts/inspect_fields.py employment-verification-letter --page 1
```
