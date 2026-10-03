# Business Profit and Loss Statement

Source assets for `landing.ai/document-type/business-profit-and-loss-statement`.

## Sample document

`source/business-profit-and-loss-statement-score-quickbooks-sample.pdf`: two QuickBooks
profit and loss reports for Craig's Design and Landscaping Services, a month-over-month
**Profit and Loss Comparison** (August 2017 against July 2017) and a year-to-date
**Profit and Loss** (January to August 2017). **2 pages, portrait.**

| | |
|---|---|
| Publisher | Champlain Valley SCORE, with Davis & Hodgdon Associates CPAs |
| Source | [2017-11 Need Answers About Accounting.pdf](https://s3.amazonaws.com/mentoring.redesign/s3fs-public/2017-11%20Need%20Answers%20About%20Accounting.pdf) |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (nonprofit workshop handout; the company is Intuit's fictional sample company) |

The source is the handout for "Need Answers About Accounting?", a 2017-2018 education
series workshop run by the Champlain Valley chapter of SCORE, the SBA-affiliated
small-business mentoring nonprofit, with Davis & Hodgdon Associates CPAs presenting.
It is served from SCORE's own file store (the `mentoring.redesign` bucket behind
score.org), and every page carries both the Champlain Valley SCORE and Davis & Hodgdon
logos. The score.org page that links the file could not be confirmed, because the
chapter site refuses scripted requests, so provenance rests on the file store and the
branding.

The original PDF is 16 pages: a balance sheet comparison, the two profit and loss
reports, cash-flow statement templates, the workshop slides and a reprinted accounting
software review. This folder keeps **pages 2 and 3 only**, split out with PyMuPDF.

Craig's Design and Landscaping Services is the fictional sample company that ships with
QuickBooks Online, so every figure is demonstration data, and small: hundreds of
dollars a month. No person is named. Nothing needed redacting. The PDF metadata was
reset to the publisher and a title naming the report.

## Why this document

These are genuine accounting-software exports rather than a hand-built template, which
is what a lender or bookkeeper actually receives from a small business. They test:

- **A nested chart of accounts.** Accounts sit two and three levels deep (Landscaping
  Services, then Job Materials, then Fountains and Garden Lighting), and the same
  account name (Job Materials, Plants and Soil) appears under both income and expenses.
- **Comparison columns with gaps.** The comparison report has a current-period and a
  prior-period column, and many lines are blank in one of them. Each value must land in
  the right column.
- **Negative amounts in QuickBooks style.** August's loss is printed `$ -19.68`, with
  the sign separated from the currency symbol.
- **Two reports in one file**, each with its own title, period and column layout.

## Featured fields

All on page 1, the Profit and Loss Comparison:

| Field | Label | Value |
|---|---|---|
| `company_name` | Company | Craig's Design and Landscaping Services |
| `reports[0].columns[0].total_income` | Total income (Aug 2017) | 942.00 |
| `reports[0].columns[0].total_expenses` | Total expenses (Aug 2017) | 961.68 |
| `reports[0].columns[0].net_income` | Net income (Aug 2017) | -19.68 |
| `reports[0].columns[1].net_income` | Net income (Jul 2017) | 112.92 |

The request suggested the company, August total income, August total expenses and July
net income. All four shipped. August net income was added so the overlay reads as one
story: income of $942.00 against expenses of $961.68 gives a $19.68 loss, beside July's
$112.92 profit in the prior-period column. The two net income values sit side by side
on the same row, so the overlay also shows the extraction keeping the columns apart.

## Grounding

- **The headline totals ground exactly.** Every report-level total (income, gross
  profit, expenses, net operating income, net income) grounds `ok` to its own cell in
  both columns of the comparison and in the year-to-date report. The negative
  `$ -19.68` extracts as -19.68.
- **August-column boxes are wide.** In the comparison table the August column's cells
  stretch left across the blank space between the account names and the figures, so
  the August boxes are wider than the July ones. They contain the right value and
  nothing else.
- **Each comparison-page field carries a second, empty range.** For most fields on page
  1, the extraction metadata includes a second range that resolves to no block. The
  first range is correct, so every featured field is pinned to occurrence 0.
  `company_name`'s second range lands on the SCORE logo text at the page break.
- **Line items mostly ground, a few adrift.** Of the account and amount leaves in the
  `line_items` arrays, 103 ground `ok` and 29 do not. Apart from the empty second
  ranges above, the misses are one row off: Plants and Soil's account name grounds to
  its amount cell, and on page 2 the Fuel amount grounds to the Total Automobile line
  below it (both read 116.56). `section`, `is_subtotal` and most `parent_account`
  values are inferred from layout, so they carry no range, as expected.
- **Extraction is fully correct.** All 49 line items across three columns, every
  subtotal and every total match the printed reports, including the nesting
  (`parent_account`) and the blank-in-one-column lines being omitted.

## Schema

`schema.json` has 16 leaf fields: company name and accounting basis, then an array of
reports, each with its title, period, run timestamp and an array of amount columns.
Each column carries the five headline totals and an array of line items (section,
account, parent account, subtotal flag, amount). A single-period report has one column;
a comparison report has one per period.

## Credits

9.60 credits at standard tier (Parse with DPT-3 Pro plus Extract, jobs API).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py business-profit-and-loss-statement
.venv/bin/python document-types/scripts/build_images.py business-profit-and-loss-statement
.venv/bin/python document-types/scripts/inspect_fields.py business-profit-and-loss-statement --page 1
```
