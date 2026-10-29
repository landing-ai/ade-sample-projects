# Audited financial statements

Source assets for `landing.ai/document-type/audited-financial-statement`.

## Sample document

`source/family-first-2024-audited-financial-statements.pdf` is the audited financial
statements of **Family First, Inc.**, a Florida nonprofit, for the year ended
December 31, 2024, with the independent auditor's report from Schafer, Tschopp, Whitcomb,
Mitchell & Sheridan, LLP. It has **27 pages, all portrait except page 9**, which is a
landscape statement of functional expenses. The PDF has a text layer: it was made from
Excel and Word.

The package follows the usual order for a nonprofit that receives government money. It
opens with the auditor's opinion, then the four basic statements (financial position,
activities, functional expenses and cash flows) and the notes. Pages 19 to 27 hold the
Single Audit material: the Schedule of Expenditures of Federal Awards and State Financial
Assistance, two compliance reports from the auditor, and the Schedule of Findings and
Questioned Costs.

| | |
|---|---|
| Publisher | Family First, Inc. and its auditor; posted by the Florida Auditor General |
| Source | [flauditor.gov/…/2024 family first.pdf](https://www.flauditor.gov/pages/nonprofit_forprofit%20rpts/2024%20family%20first.pdf) |
| Provenance page | [flauditor.gov/…/family first.htm](https://flauditor.gov/pages/nonprofit_forprofit%20pages/family%20first.htm) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

Nonprofits that receive Florida state financial assistance must file their audit reports
with the Auditor General, which posts them publicly. The text layer names no individual.
The auditor's reports are addressed to the Board of Directors. The signatures on pages 6,
23 and 26 are the firm's name written by hand, not an individual's signature. The firm's
letterhead on pages 4, 22 and 24 is an image that lists six partners by name, with the
office address and phone number. The operator chose to keep it as published. No redaction
was made. The committed PDF is the publisher's file, unaltered. It carries an
owner-password permissions restriction, which ADE handled without trouble, and its
metadata names only the audit firm.

## Why this document

This is the collection's first **audited financial statement**. It differs from the
business profit and loss statement in three ways:

- **An opinion as well as numbers.** The auditor's report, the opinion type (unmodified),
  the framework (US GAAP), the report date and the signing city all have to be read out
  of prose, across a letterhead image and a signature image.
- **Statements that tie together.** Total assets equal total liabilities and net assets.
  Net assets at the end of the year appear on both the balance sheet and the statement of
  activities. Ending cash appears on both the cash flow statement and the balance sheet.
- **A Single Audit tail.** The awards schedule nests programs under grantors and
  subtotals under states, with CFDA and CSFA numbers and contract numbers in their own
  columns. The findings summary is a numbered list of yes/no conclusions.

## Featured fields: the statement of financial position

All on page 7.

| Field | Value |
|---|---|
| Cash and cash equivalents | $14,021,341 |
| Total current assets | $15,252,147 |
| Total assets | $15,689,274 |
| Total liabilities | $1,758,660 |
| Total liabilities and net assets | $15,689,274 |

The request suggested this page and these fields, and the overlay reads as the balance
sheet balancing: the same $15,689,274 is boxed on two different lines, one on each side.
The request also suggested the statement date. It was left out because the extracted
period end date grounds to the cover page, not to the date printed on page 7. Net assets
without donor restrictions would have completed the equation, but on this page it
grounds to its row label rather than its amount.

## What it surfaced

**Every number reconciles.** The nine revenue lines, including the negative "Less direct
benefit costs to donors", sum to the $26,362,717 printed total. The three expense
functions sum to total expenses. The two federal awards sum to $818,458, and the eight
Florida state lines sum to $9,494,278. Every total on the balance sheet matches its
printed figure.

**The opinion section reads cleanly.** The model took the audit firm's name from the
letterhead image, and the report date and city from beneath the handwritten signature.
It classified the "present fairly, in all material respects" wording as `unmodified`.

**The awards table is extracted as printed, inconsistencies included.** The schedule
prints the Responsible Fatherhood CSFA number as "60.245 & 60.226" on one line and
"60.245 & 60.246" on the next, and the extraction keeps both. The Texas and Tennessee rows
print a year range ("22/24") in the CSFA column, and the extraction returns that as the
number. The grantor heading "Family Strengthening, Public Awareness and" was merged into
the first program's name, so that row reads as one long program title.

**Grounding is tight on the statements and loose on the prose.** Every balance sheet
amount boxes its own figure. On the asset side the box covers the whole amount column,
because those figures sit in wider cells. Fields read from sentences ground to the
sentence or to a neighbouring line: the accounting framework spans a line break, and the
findings booleans ground to "No matters reported". The `source` field on each award
(federal or state) has no range at all, because it comes from the section heading rather
than from the row.

## Extraction

**46 leaf fields**, covering the entity and period; the auditor's report (addressee,
firm, opinion type, framework, report date and city); the main balance sheet lines; the
revenue lines and expense totals from the statement of activities; the cash flow
subtotals; each award in the federal and state schedule (source, grantor, program,
CFDA/CSFA number, contract number, expenditures) with the totals; and the findings
summary (material weaknesses, major programs tested, the Type A/B threshold, low-risk
auditee status, findings reported). All 8 top-level fields populate. Net assets with
donor restrictions and net cash from financing activities are null, because the document
reports neither.

## Cost

**44.40 credits** at standard tier for 27 pages, parse and extract together.

## Regenerating

```bash
curl -sSL -o document-types/collection/audited-financial-statement/source/family-first-2024-audited-financial-statements.pdf \
  "https://www.flauditor.gov/pages/nonprofit_forprofit%20rpts/2024%20family%20first.pdf"
.venv/bin/python document-types/scripts/run_ade.py audited-financial-statement                # 44.40 credits
.venv/bin/python document-types/scripts/run_ade.py audited-financial-statement --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py audited-financial-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py audited-financial-statement --page 7
```
