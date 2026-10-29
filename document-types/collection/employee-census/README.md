# Employee Census

Source assets for `landing.ai/document-type/employee-census`.

## Sample document

`source/advanstaff-employee-census-report.pdf`: an **Employee Census Report with Status
Class "Active"** for AdvanStaff HR's demo company `*ASI DEMO - GENERAL COMPANY`, run on
23 May 2025. **1 page, landscape**, with a native text layer. It lists 34 active
employees, one row each: name, employee ID, status, birth date, age, marital status,
state, gender, last and original hire dates, term date and annual pay.

| | |
|---|---|
| Publisher | AdvanStaff HR |
| Source | [advanstaff.com/wp-content/uploads/2025/05/reporting_sales-final.pdf](https://advanstaff.com/wp-content/uploads/2025/05/reporting_sales-final.pdf), linked from [advanstaff.com/help/introduction-to-reporting/](https://advanstaff.com/help/introduction-to-reporting/) |
| Retrieved | 2026-10-28 (downloaded by script) |
| Clearance | **Public** |

The source is AdvanStaff HR's own "Reporting Options" sales PDF, which shows example
output from its HR and payroll system. The original is six pages: a cover page, a
dashboard, and four demo reports. **Only page 4, the census report, was kept**; the other
pages were dropped.

**No redaction was needed.** Every employee is a fictional demo record with an
alliterative name (Abagail Aarons, Beth Baker, Chloe Cook), and 32 of the 34 carry a
`DEMO` suffix. The two without one follow the same alliterative pattern and appear as
new hires of the same demo company in the PDF's other demo reports, beside suffixed demo
hires, so they were treated as fictional too. The PDF's document metadata, which named
the person who produced the sales PDF, was cleared. The page is otherwise unchanged.

The footer reads "Page 1 of 2". The second page of the census is not in the publisher's
PDF, so the sample stops at the 34th row.

## Why this document

An employee census is what an employer hands a benefits broker, insurer or PEO to get a
group quote: one row per employee with the attributes coverage is rated on. It is a
single wide table and nothing else, so it tests whether every row's values stay in their
own columns across 34 rows and 12 columns, with two sparse columns (marital status is
filled on 12 rows; term date on none) that could pull neighbouring values sideways. This
one is an HR/payroll-style census, without the coverage-tier or ZIP columns a
carrier's census template would carry.

## Schema

`schema.json` resolves to **18 leaf fields**: company name, report title, report filter,
run date, page label, the employee count, and for every employee row the name, ID,
status, birth date, age, marital status, state, gender, last hire date, original hire
date, term date and annual pay.

All 34 rows were extracted, and every value in every row was checked against the PDF's
text layer: all matched. Blank cells came back two ways: of the 34 blank term dates, 26
as an empty string and 8 as null; of the 22 blank marital status cells, 16 as an empty
string and 6 as null. The extraction is published as returned.

## Featured fields: one census row

All on page 1:

| Field | Value |
|---|---|
| Company | *ASI DEMO - GENERAL COMPANY |
| Employee ID | E92815 |
| Birth date | 07/30/1968 |
| Original hire date | 02/26/2024 |
| Annual pay | 41,601.60 |

The overlay shows the company and the first row of the census, the values a benefits
quote is rated on. The first row was chosen because its original hire date (02/26/2024)
differs from its last hire date (09/17/2024), a rehire, so the featured hire date is not
a repeat of the other one. The employee ID stands in for the name, which grounds equally
well, so the page features no personal name, even a fictional one.

The request suggested, as suggestions only, the company name, the report title, and one
row's ID, birth date, hire dates and annual pay. All of them ground correctly; the
report title and the last hire date were left out to keep to five fields.

## Grounding

- **The table grounds cell by cell.** Every populated cell in all 34 rows resolves to its
  own cell and checks `ok`.
- **Blank cells ground two ways.** The empty-string values (26 term dates, 16 marital
  statuses) point at their empty cells, which is correct but cannot be illustrated. The
  null values (8 term dates, 6 marital statuses) have no range at all.
- **The employee count is synthesized from the rows.** The report prints no count; the
  extracted 34 is right, and its ranges point at the employee names it was counted from.
- **The run date grounds to the footer timestamp** "23 May 2025 - 11:06", which contains
  the date in a different format, so it is flagged `OFF` and not featured.
- **Bold, overprinted amounts read cleanly.** Every other row's annual pay is printed
  twice at a small offset to fake bold; the text layer carries both copies, but the
  parse and extraction read each value once.
- **Birth date boxes are wide.** The column is right-aligned under a wide header, so the
  box spans most of the column; the value sits at its right end.

## Credits

13.30 credits at the standard tier: 2.30 for the parse and 11.00 for the extraction.

## Regenerate

```bash
# source PDF: page 4 of the sales PDF, metadata cleared with document-types/scripts/pdfmeta.py
PYTHONPATH=document-types/scripts .venv/bin/python -c "
import pymupdf, pdfmeta
d = pymupdf.open('reporting_sales-final.pdf'); d.select([3]); pdfmeta.clear(d)
d.save('document-types/collection/employee-census/source/advanstaff-employee-census-report.pdf', garbage=4, deflate=True)"

.venv/bin/python document-types/scripts/run_ade.py employee-census
.venv/bin/python document-types/scripts/build_images.py employee-census
```
