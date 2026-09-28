# Employment offer letter

Source assets for `landing.ai/document-type/employment-offer-letter`.

## Sample document

`source/employment-offer-letter-redacted.pdf` — an offer letter from Aerial Telecom
Solutions Pvt. Ltd., an Indian telecom services company, for a Technical Manager post,
dated 20-Mar-2025, redacted. **5 pages, portrait (612×792)**, exported from Word, with a
full text layer, a logo, a watermark and a branded footer on every page. Pages 1 to 4
are the letter and its terms; page 5 is Annexure I, the salary breakdown table.

| | |
|---|---|
| Publisher | Aerial Telecom Solutions Pvt. Ltd. (employer) |
| Source | [scribd.com/document/850511200](https://www.scribd.com/document/850511200) |
| Retrieved | 2026-09-27, downloaded manually |
| Clearance | Redacted |

## Redaction

This is a real letter, uploaded to Scribd by a third party. Scribd is a user-upload site,
so the uploader is not the publisher, and the letter is treated as a personal record.
Scribd also blocks scripted requests, so the file was downloaded by hand. **The source url
is recorded in its id-only form**: Scribd's full url adds a title slug, and this one was
the candidate's full name.

Personal data was removed using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it:

| What | Replaced with | Occurrences |
|---|---|---|
| Candidate's full name | Jonny Doe | 2 (page 1, annexure) |
| First name in the salutation | Dear Jonny | 1 |
| Care-of line with a relative's name and house number | C/O Sample Relative, H.No-000, Example Colony, | 1 |
| Locality, city and PIN code | Sample Nagar, Jalandhar, Punjab-000000 | 1 |

The city is kept: Jalandhar is also the place of posting in the body of the letter.

**The signature was an image.** The authorized signatory's handwritten signature on page 4
was deleted with a new `redact.py --remove-images` option. It sat over a corner of the
full-page watermark, so blanking the area would have left a white patch on the watermark,
and deleting every overlapping image would have removed the watermark. The option deletes
only images lying entirely inside the given area.

The PDF metadata was also cleared; its `author` field named a person. The company's name,
logo, address, phone number, website and CIN are business details, and the terms and
salary figures are left as printed.

**Replacement names were chosen by width.** The letter is set in Calibri Bold, which is
narrow, and replacements are written in Helvetica Bold. "John Q Sample" had to shrink to
fit the original name's width and came out visibly small; "Jonny Doe" fits at full size.
The replaced text is still visibly a different typeface from the Calibri around it.

**Verified:** no original identifier is extractable from the committed PDF, no image
remains in the signature area, and no original identifier appears anywhere in this folder.
The original values are deliberately not recorded here or in `manifest.json`. The rules
file used by `redact.py` stays outside the repo.

## Why this document

The collection's first **Indian document**, and a letter that pairs prose with a table:

- **Terms in sentences.** The designation, posting, joining date and pay are each stated
  in a sentence ("Your Date of Joining will be 07-Apr-2025."), not in labelled fields.
- **Indian conventions.** Rupee amounts written in figures and in words ("Rs. 565008/-
  (Rupees Five Lakh Sixty Five Thousand Eight Only/-)"), and a salary structure with HRA,
  EPF, ESIC, LWF and professional tax.
- **A table with repeated line names.** The annexure lists EPF, ESIC and LWF twice, once
  under the employee's deductions and once under the employer's contributions.

## Featured fields: the terms of the offer

All on **page 1**, which the request asked for. The request named no fields, so these
were chosen:

| Field | Value |
|---|---|
| Designation | Technical Manager |
| Place of posting | Jalandhar |
| Date of joining | 07-Apr-2025 |
| Annual cost to company (Rs.) | 565008 |
| Letter date | 20-Mar-2025 |

Together they are the offer: what the job is, where, from when, for how much, and when it
was made. No person is featured. Designation and annual CTC each appear more than once
and are pinned to their page 1 occurrences. Each box covers the sentence that states the
value.

## What it surfaced

**The annexure extracts completely.** All 15 salary components come back with the right
monthly and annual amounts, and each duplicated line lands in the right section: the
employee's EPF of 1800 and the employer's EPF of 1800 are told apart by position.

**But the annexure totals have no location.** Gross salary, monthly and annual take-home,
and total cost to company all extract correctly, yet all four come back with no range,
while every component line in the same table grounds normally.

**A section name the table never prints.** The schema calls the first block of the
annexure "Earnings", but the table heads it "Particulars". Extraction assigns the six lines
to "Earnings" correctly and grounds them to the "Particulars" heading, which the
consistency check flags.

**Numbers written as words.** Probation is "Six months" and retirement is at "Fifty-eight
years". Both extract correctly as 6 and 58, and both are flagged because the digits are
not on the page.

70 of 87 extracted values are `ok`; the 13 `OFF` and 4 `SYNTH` are the cases above plus the
employer's name grounding to whole paragraphs that mention it.

## Extraction

`schema.json` was written for this letter, with **19 leaf fields**: employer, reference
number, letter date, candidate, the offer terms (designation, posting, joining date,
annual CTC, probation, notice period, retirement age) and the annexure (components with
section, monthly and annual amounts, plus totals). Everything populates, with no warnings.

## Cost

**9.20 credits** at standard tier for 5 pages: 5.30 to parse, 3.90 to extract.

## Regenerating

```bash
# Redaction, from the manual download, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/employment-offer-letter/source/employment-offer-letter-redacted.pdf \
    --rules <outside-the-repo>/rules.json --remove-images 4:45,328,136,378

.venv/bin/python document-types/scripts/run_ade.py employment-offer-letter                # 9.20 credits
.venv/bin/python document-types/scripts/run_ade.py employment-offer-letter --extract-only # 3.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py employment-offer-letter           # free
.venv/bin/python document-types/scripts/inspect_fields.py employment-offer-letter --page 1
```

`manifest.json` sets `preview_pages` to 1, 2, 3 and 5: page 5 is the annexure table, and
page 4 is the signature page with the signature removed.
