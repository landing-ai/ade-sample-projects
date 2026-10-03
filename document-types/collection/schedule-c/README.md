# Schedule C

Source assets for `landing.ai/document-type/schedule-c`.

## Sample document

`source/schedule-c-2025-irs-ats-scenario-12.pdf`: the 2025 IRS Schedule C (Form 1040),
Profit or Loss From Business (Sole Proprietorship), pages 1 and 2, filled with IRS test
data. **2 pages, portrait.**

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [1040-mef-ats-scenario-12-10292025.pdf](https://www.irs.gov/pub/irs-efile/1040-mef-ats-scenario-12-10292025.pdf), linked from the [Tax Year 2025 Form 1040 series MeF ATS information page](https://www.irs.gov/e-file-providers/tax-year-2025-form-1040-series-and-extensions-modernized-e-file-mef-assurance-testing-system-ats-information) |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Test Scenario
12 for tax year 2025, which software vendors use to test their e-file output. The
original PDF is 15 pages: a cover sheet, Form 1040, Schedules 1, 2, C and SE, Forms
7206 and 7217, and a W-2. This folder keeps **pages 8 and 9 only**, the two pages of
Schedule C, split out with PyMuPDF. No content was altered.

Every value is IRS test data: a fictitious sole proprietor running a design business
called ENERGY BUILD in Anytown KY, with an SSN in the 400-00 range the IRS reserves for
ATS testing. Nothing needed redacting. The PDF metadata was reset to the IRS as author
and a title naming the scenario.

The pages carry a "TREASURY/IRS AND OMB USE ONLY DRAFT" header and "DRAFT — DO NOT
FILE" side banners. The parse transcribes them as text blocks. Page 2 (Parts III to V:
cost of goods sold, vehicle information, other expenses) is blank on this return and is
kept so the folder holds the complete schedule.

## Why this document

Schedule C is how a sole proprietor reports business income, and it is the document a
lender asks for to qualify a self-employed borrower. It tests things the collection's
other tax forms do not:

- **A two-column expense grid.** Part II runs lines 8-17 down the left and 18-27b down
  the right, each with its own amount column. Every populated expense (550, 125, 1,000,
  2,500, 6,532, 200) extracts to the right line and grounds to its own cell.
- **The same value on four lines.** 35,235 is printed on lines 1, 3, 5 and 7, and each
  grounds to its own line's amount cell.
- **A header full of checkboxes and coded fields**: the accounting method, the
  material-participation and 1099 questions, and the six-digit business code printed in
  separate boxes (read correctly as 541310).

`schema.json` covers the proprietor, business details (lines A-J), all of Parts I and
II, line 31 and 32, and the main lines of Parts III-V. **60 leaf fields** (counted
from the schema).

## Featured fields: from the business to its bottom line

All on page 1.

| Field | Value |
|---|---|
| Business name (line C) | ENERGY BUILD |
| Gross receipts (line 1) | 35235 |
| Gross income (line 7) | 35235 |
| Total expenses (line 28) | 10907 |
| Net profit (line 31) | 24328 |

These are the fields the request's notes suggested, which preferred Part I and the
summary lines over the Part II grid. They read as one calculation down the right-hand
column: the business takes in 35,235, spends 10,907 and nets 24,328. No person is
featured.

The line 31 amount sits low in a short cell, so the box's top edge runs close to the
digits in the crop. The box is the right cell; the crop was checked by eye.

## Grounding and extraction notes

- **The parse reads every checkbox correctly**, including the empty boxes on lines H
  and J, the line 1 statutory-employee box, and both line 32 at-risk boxes.
- **Extraction does not, in two places.** `line_32_at_risk` comes back `all_at_risk`
  and `filed_required_1099s` (line J) comes back `false`, although both boxes on each
  line are unchecked. Line 32 only applies to a loss, and this return shows a profit.
- **Blank amount lines extract as 0, not null**, with ranges pointing at empty cells:
  every blank line in Parts I-III and line 48. The schema descriptions ask for null on
  an empty cell. One extraction-only rerun with both points worded more strongly
  changed nothing. For the arithmetic the two are equivalent, but a consumer who needs
  to tell "blank" from "zero" cannot rely on this.
- `business.ein` is correctly empty; `vehicle_placed_in_service` is correctly null.
- Every populated amount and text field on page 1 grounds to its own cell and reads `ok`.

## Cost

**11.10 credits** at standard tier: 7.30 for the parse and first extraction, 3.80 for
one extraction-only rerun with tightened descriptions.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py schedule-c
.venv/bin/python document-types/scripts/build_images.py schedule-c
.venv/bin/python document-types/scripts/inspect_fields.py schedule-c --page 1
```
