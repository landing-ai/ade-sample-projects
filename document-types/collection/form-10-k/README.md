# Form 10-K

## Sample document

NVIDIA Corporation's annual report on Form 10-K for the fiscal year ended January 25, 2026.
It is 93 pages, all portrait. The filing has the full standard structure: the SEC cover
page, Parts I to IV (business, risk factors, MD&A, the audited consolidated financial
statements and notes), the signatures section, and the exhibits filed with it (insider
trading policy, auditor consent, and the Section 302 and 906 certifications).

| | |
|---|---|
| Publisher | NVIDIA Corporation |
| Source URL | https://d18rn0p25nwr6d.cloudfront.net/CIK-0001045810/e361e58a-7483-44f5-bc62-a9080ae6ec72.pdf |
| Filed | 2026-02-25 (SEC accession 0001045810-26-000021) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `public` |

A 10-K is a mandatory public SEC filing. This copy is the PDF that NVIDIA's investor
relations site serves, an EDGAR Online rendering of the filing. It is committed
unmodified, including its EDGAR Online metadata and an owner-only permissions flag that
needs no password to open.

The filing names the company's executive officers and directors in their official
roles. They appear in the executive officer table on page 11, in the conformed `/s/`
signatures on pages 84–85 and in the CEO and CFO certifications on pages 90–93. The
operator decided to keep these names as published. No private individual's personal
data appears: the only phone number is the corporate main line, and there are no
emails, home addresses or personal identifiers. The featured fields are all impersonal.

## Why this document

Long-form financial reporting is not covered anywhere else in the collection. The
investor presentation is a slide deck, and Form 1120 is a tax form. A 10-K is dense
prose broken up by about 60 financial tables. The values a reader needs are scattered
across it: the cover page, the statements in Item 8 and the narrative sections. The same
figure often appears in several places, too: the cash flow totals appear both in the
MD&A summary (page 43) and in the statement itself (page 55).

At 93 pages it is also the longest document in the collection, more than twice the size
of the next largest, the 43-page investor presentation.

## Extraction

`schema.json` has 49 leaf fields in five groups:

- `cover_page`: registrant name, fiscal year end, commission file number, EIN, state of
  incorporation, address, phone, ticker, exchange, filer category, the WKSI and shell
  company check boxes, public float and shares outstanding, with their dates
- `income_statement`: an array with one entry per fiscal year column, holding revenue
  through diluted EPS and diluted share count
- `balance_sheet`: the current year-end column
- `cash_flow`: the three activity totals and capital expenditure for the current year
- `company_facts`: headcount, auditor, reportable segments

Every value came back correct, and each of the three income statement columns went to the
right array entry.

## Featured fields

Page 51 shows the Consolidated Statements of Income. The featured fields are the fiscal
2026 column, top to bottom: **Revenue**, **Gross profit**, **Operating income**, **Net
income** and **Diluted EPS**. The overlay therefore follows one year from the top line to
the bottom line. Because the table has three year columns, it also shows that the model
picked the right column. All five fields are `ok` from `inspect_fields.py`, and each box
sits exactly on its cell. The two cells printed with a `$` include it in the box.

## What the grounding did

- **Financial tables ground cleanly.** Every income statement, balance sheet and cash
  flow figure grounds to its own cell, including all three columns of the income
  statement.
- **Repeated values ground to every place they appear.** The cash flow totals ground both
  to the MD&A summary table on page 43 and to the statement on page 55.
- **Normalized dates read `OFF`.** The fiscal year ends ground to column headers such as
  `Jan 25, 2026`, which do not literally contain `2026-01-25`. The grounding is right,
  but the strict check fails, so no date is featured.
- **Cover page check boxes read `OFF`.** `well_known_seasoned_issuer` and `shell_company`
  ground to the question text and both boxes, which is right for a boolean but cannot be
  shown as a single value. `filer_category` grounds correctly to the "Large accelerated
  filer" label.
- **Some values are grounded to whole sentences.** Headcount, public float and shares
  outstanding are stated in prose, so they ground to the whole sentence. The auditor
  name grounds to a paragraph that names the firm.

## Cost

**226.80 credits** at standard tier for 93 pages, parse and extract together. This is far
more per page than the investor presentation (65.50 for 43 pages). The markdown is about
395,000 characters and contains around 60 HTML tables.

To iterate on the schema, use `run_ade.py --extract-only`, which reuses the committed
parse and runs extraction only.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py form-10-k                 # 226.80 credits
.venv/bin/python document-types/scripts/run_ade.py form-10-k --extract-only  # schema iteration
.venv/bin/python document-types/scripts/build_images.py form-10-k            # free
.venv/bin/python document-types/scripts/inspect_fields.py form-10-k --page 51
```
