# Customer Concentration Schedule

Source assets for `landing.ai/document-type/customer-concentration-schedule`.

## Sample document

Two exhibits from the statistical section of the FY2025 Annual Comprehensive Financial
Report of the District of Columbia Water and Sewer Authority (DC Water): Exhibit 6, *Ten
Largest Commercial Customers, Last Ten Fiscal Years*, and Exhibit 7, *Ten Largest
Government Customers, Last Ten Fiscal Years*, both in thousands of dollars.

| | |
|---|---|
| File | `source/dc-water-fy2025-largest-customers.pdf` |
| Pages | 2 (pages 11 and 12 of the 34-page statistical section; printed pages 88 and 89) |
| Orientation | Landscape |
| Layer | Native text, no scanning |

Each page is one ten-year grid: a customer column, ten fiscal-year columns (2025 back to
2016), a Total row and a `% of Total Operating Revenues` row. The commercial grid lists 16
customers and the government grid 11, because a customer that left the top ten still has
a row, with `-` in the years it did not qualify.

A public utility stands in for a diligence schedule here. A private company's customer
concentration schedule, with revenue and share by customer, is not something anyone
publishes; a utility's ACFR is the public document that carries the same table.

## Provenance

| | |
|---|---|
| Publisher | District of Columbia Water and Sewer Authority (DC Water) |
| Source URL | https://www.dcwater.com/sites/default/files/finance/ACFR/2025/FY25%20ACFR%20Statistical%20Section.pdf |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `public` |

DC Water publishes its ACFR on its own website for bondholders and the public. The two
pages the operator chose were split out with PyMuPDF and the rest of the section dropped.
There is no personal data: every customer is a university, hospital, company or government
agency. Nothing was redacted. The split file's document metadata was cleared, and the
committed PDF carries none.

## Why this document

The layout is the test. Each amount row puts a `$` sign in its own column on the first
and Total rows only, and most of the grid is `-` cells, so a parser that drops a `-` or
treats a `$` as a value shifts every number after it one year to the left. Extraction has
to keep sixteen rows by ten columns aligned, and say which customers were *not* in the top
ten in a given year rather than inventing a zero.

The schema asks for what a reader of a concentration schedule wants: each customer's two
most recent years, and the full ten-year run of the total and its share of revenue.

## Featured fields

All on page 1, in the FY2025 column of Exhibit 6, so the overlay reads as one answer to
"how concentrated is commercial revenue?":

| Field | Label | Value |
|---|---|---|
| `schedules[0].most_recent_fiscal_year` | Fiscal year | 2025 |
| `schedules[0].customers[0].customer_name` | Largest commercial customer | Georgetown University |
| `schedules[0].customers[0].most_recent_year_amount` | Largest customer revenue ($000) | 7184 |
| `schedules[0].yearly_totals[0].total_amount` | Top-ten total ($000) | 37071 |
| `schedules[0].yearly_totals[0].percent_of_total_operating_revenues` | Share of operating revenues | 3.69 |

The request file named no fields; its notes suggested the top customer and amount, the
top-ten total, the percentage and the schedule title. The title was dropped for the reason
under Grounding, and the fiscal-year header added so the overlay shows which column the
values come from.

## Extraction

`schema.json` has 13 leaf fields: one for the reporting entity, six per schedule, three per
customer row and three per yearly total. The run returned 154 leaf values: both schedules,
all 27 customer rows and all 20 yearly totals.

Every value matches the PDF, including all 54 two-year customer amounts and every total
and percentage across both ten-year runs. The columns did not shift. The government
FY2025 amounts sum exactly to the printed total of $69,930 thousand; the commercial ones
sum to $37,072 thousand against a printed $37,071, a rounding difference in the source.

The first extraction, with the customer amounts typed as plain `number`, returned `0` for
every `-` cell, although the description asked for null. Making those two fields nullable
(`["number", "null"]`) fixed it: the second extraction returned null for every `-` and
left the real amounts unchanged.

## Grounding

Every featured value grounds to its own cell, including the `$ 7,184` and `$ 37,071`
cells whose dollar sign sits in a separate column. The `-` cells ground to the `-` in the
right column too, so even a null can be pointed at.

`inspect_fields.py` marks three values `OFF`. `schedule_title` on both pages joins the
title's lines, while its range covers the whole title block (`EXHIBIT 6<br>TEN LARGEST
...`); the value is right but the crop would not match it, so the suggested title field is
not featured. `William C Smith & Co` is marked `OFF` only because the markdown escapes the
ampersand.

Extraction also returned a second, zero-length range for most fields, which resolves to no
page and shows as occurrence 1 with page `None`. Every featured field is pinned to
occurrence 0, the real cell.

## Credits

**15.40 credits** at standard tier: 8.90 for the two-page parse and first extraction, and
6.50 for the re-extraction after the schema change.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py customer-concentration-schedule      # spends credits
.venv/bin/python document-types/scripts/build_images.py customer-concentration-schedule # free
```
