# Form 1120

Source assets for `landing.ai/document-type/form-1120`.

## Sample document

`source/form-1120-2024-irs-ats-alternate-scenario-1.pdf`: the 2024 IRS Form 1120, U.S.
Corporation Income Tax Return, all six pages, filled with IRS test data. **6 pages,
portrait.**

| | |
|---|---|
| Publisher | Internal Revenue Service |
| Source | [ty24-f1120-ats-scenario-1-alternate.pdf](https://www.irs.gov/pub/irs-wi/ty24-f1120-ats-scenario-1-alternate.pdf), linked from the IRS Tax Year 2024 Form 1120 MeF ATS page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (US government work, public domain) |

The source is the IRS Modernized e-File Assurance Testing System (ATS) Alternate
Scenario 1 for tax year 2024, which software vendors use to test their e-file output.
The original PDF is 32 pages: cover sheets, Form 1120, then Schedules B, D, G, M-3 and
O and Forms 1125-A, 3800, 4562, 8594, 8916-A, 8453-CORP and 8949. This folder keeps
**source pages 4–9 only**, the six pages of Form 1120 itself, split out with PyMuPDF:

| Page | Content |
|---|---|
| 1 | Form 1120 page 1: header, income, deductions, tax and payments |
| 2 | Schedule C, dividends and special deductions |
| 3 | Schedule J, tax computation and payment |
| 4–5 | Schedule K, other information |
| 6 | Schedules L, M-1 and M-2: balance sheet and retained earnings |

Every value is IRS test data: the fictitious corporation Help For Some, Inc. at 33 Any
Street, Anytown MD, and a fictitious preparer firm with a 555 phone number. No
individual is named and the officer and preparer signature lines are blank. Nothing
needed redacting. The PDF metadata was reset to the IRS as author and a title naming
the scenario.

Page 2 (Schedule C) carries an "INTERNAL USE ONLY / DRAFT AS OF May 23, 2024"
watermark. Page 1, the featured page, does not. The previews skip page 2.

## Why this document

It is the collection's first corporate return. Form 1065 covers a partnership and
Form 1040 an individual; this one has mid-size eight-digit figures ($87.6M of assets)
and a full balance sheet. It tests reading a long ladder of numbered amount lines on
page 1 and pulling figures from the schedules behind them: Schedule J's tax
computation, Schedule K's accounting method checkbox and business activity code, and
the multi-column Schedule L balance sheet.

`schema.json` covers the header, the income, deduction and tax lines of page 1, the
paid preparer block, and key lines of Schedules J, K, L and M-2. **69 leaf fields**
(counted from the schema), all populated.

## Featured fields: the return from top to bottom line

All on page 1.

| Field | Value |
|---|---|
| Total assets (item D) | 87608959 |
| Total income (line 11) | 77254243 |
| Total deductions (line 27) | 40415384 |
| Total tax (line 31) | 7719804 |
| Total payments and credits (line 33) | 9000000 |

These are the fields the request's notes suggested. Each one grounds to its own amount
cell, and the crops were checked by eye. Together they run the return from how big the
corporation is, through income and deductions, to the tax owed and paid. Lines whose
value repeats on page 1 (1a and 1c, 28 and 30, 36 and 37) were left out. No person is
featured.

## Grounding and extraction notes

- **Every populated amount line on page 1 grounds to its own cell** (all read `ok` in
  `inspect_fields.py`). So do every Schedule J, K, L and M-2 field, on their own pages.
- **The multi-column Schedule L grounds cleanly.** Beginning-of-year column (b) and
  end-of-year column (d) values each land in the right column, even where both print
  87,608,959 (the IRS test data repeats total assets across both years).
- **Blank amount lines extract as 0, not null**, despite the schema asking for null.
  Same as on Form 1040. They read `OFF` because there is nothing on the line to point
  at.
- **Line 37 is misassigned.** The 1,280,196 overpayment is printed in the **Refunded**
  column; the "Credited to 2025 estimated tax" box is empty. The parse reads that
  correctly (an empty cell, then `Refunded`, then the amount), but extraction puts the
  amount in `credited_to_next_year_estimated_tax` and gives `refunded` 0. Left visible
  rather than patched.
- **A schema description is out of date, harmlessly.** `schedule_j.income_tax` says
  "Part I line 2"; on the 2024 form income tax is line 1a (line 2 is the subtotal, blank
  here). Extraction took the right value, 7,736,160 from line 1a.
- The Schedule M-3 checkbox (`schedule_m3_attached`, true) reads `OFF` only because
  "true" is not printed, as for every boolean.

## Cost

**21.70 credits** at standard tier: 12.30 for the six-page parse and 9.40 for
extraction.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-1120
.venv/bin/python document-types/scripts/build_images.py form-1120
.venv/bin/python document-types/scripts/inspect_fields.py form-1120 --page 1
```
