# Form 1040

Source assets for `landing.ai/document-type/form-1040`.

## Sample document

`source/form-1040-2025-irs-ats-scenario-13.pdf`: the 2025 IRS Form 1040, U.S.
Individual Income Tax Return, pages 1 and 2, filled with IRS test data. **2 pages,
portrait.**

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-13.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-13.pdf), listed on the [Tax Year 2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Test Scenario
13 for tax year 2025, which software vendors use to test their e-file output. The
original PDF is 9 pages: a cover sheet, Form 1040, Schedule 3, Form 6251, Form 8911 and
its Schedule A, and a W-2. This folder keeps **pages 2 and 3 only**, the two pages of
Form 1040, split out with PyMuPDF. The Form 6251 pages ship separately as
`form-6251-amt`.

Every value is IRS test data: a fictitious married-filing-jointly couple at 13 Elm
Street, Anytown TX, with SSNs in the 400-00 range the IRS reserves for ATS testing.
Nothing needed redacting. The PDF metadata was reset to the IRS as author and a title
naming the scenario.

The pages carry a "TREASURY/IRS AND OMB USE ONLY DRAFT" header and "DRAFT — DO NOT
FILE" side banners. The parse transcribes them as text blocks.

## Why this document

It is the most common US tax form, and the collection's first individual return. The
Form 1065 sample tests a business return; this one tests the two things a 1040 adds to a
lender's or preparer's workflow: the filing-status and digital-assets checkboxes, and a
long ladder of numbered amount lines, most of them blank, where the same value
(31,620) appears on four lines of page 1 and must be grounded to the right one each
time.

`schema.json` covers identity, address, filing status, the digital-assets answer and
the main amount lines of both pages. **50 leaf fields** (counted from the schema).

## Featured fields: the checkboxes beside the income lines

All on page 1.

| Field | Value |
|---|---|
| Filing status (checkbox) | married_filing_jointly |
| Digital assets question (checkbox) | no |
| W-2 wages (line 1a) | 31620 |
| Total income (line 9) | 31620 |
| Adjusted gross income (line 11a) | 31620 |

This is the selection the request suggested. Line 1a, line 9 and line 11a all print
31,620, and each grounds to its own line's amount cell, which is the point of featuring
three lines with one value. No person is featured.

`filing_status` reads `OFF` in `inspect_fields.py` only because its enum value is not
printed verbatim. Its range is exactly the checked `[x] Married filing jointly` line,
and the crop was checked by eye.

## Grounding and extraction notes

- **The parse reads every checkbox correctly**, including both empty direct-deposit
  boxes on line 35c (`[ ] Checking`, `[ ] Savings`).
- **Extraction does not.** `refund.account_type` comes back `checking` although neither
  box is checked. Re-running extraction with a description saying "null if both boxes
  are unchecked" did not change it. Its range points at `[ ] Checking`, so the box would
  highlight an empty checkbox.
- **Blank amount lines extract as 0, not null.** Lines 2a through 10, 13a, 19, 25b, 26,
  27a, 36 and 37 are empty on the form but extract as 0, with ranges pointing at empty
  cells or line numbers. The schema descriptions ask for null on an empty line, in a
  second pass worded more strongly; the result was the same. For a 1040 the two are
  equivalent arithmetically, but a consumer who needs to tell "blank" from "zero"
  cannot rely on this.
- `address.apartment` and `refund.routing_number` are correctly empty and have no
  ranges.
- Every populated amount on both pages grounds to its own amount cell and reads `ok`.

## Cost

**15.60 credits** at standard tier: 10.60 for the first parse and extraction, 5.00 for
one extraction-only rerun with tightened descriptions.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-1040
.venv/bin/python document-types/scripts/build_images.py form-1040
.venv/bin/python document-types/scripts/inspect_fields.py form-1040 --page 1
```
