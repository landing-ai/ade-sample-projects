# Appraisal Report

Source assets for `landing.ai/document-type/appraisal-report`.

## Sample document

`source/appraisal-report-uad-urar-sf1.pdf`: a complete **Uniform Residential Appraisal
Report (URAR)** in the redesigned Uniform Appraisal Dataset (UAD) format, the form that
replaces Fannie Mae Form 1004 / Freddie Mac Form 70. Single Family Scenario 1: a
detached three-level colonial with a walk-out basement, appraised subject to repair.
**21 pages, portrait, US legal size (8.5 x 14 in).**

| | |
|---|---|
| Publisher | Freddie Mac and Fannie Mae (UAD redesign) |
| Source | [uad-sample-scenarios-combined.pdf](https://sf.freddiemac.com/docs/pdf/uad-sample-scenarios-combined.pdf), linked from Freddie Mac's UAD page |
| Retrieved | 2026-10-03, by script |
| Clearance | **Public** (GSE specimen published for the industry) |

The source PDF is 302 pages of sample scenarios. This folder keeps **pages 180-200
only**, the full 21-page URAR for Single Family Scenario 1, split out with PyMuPDF.
Page 179, the scenario's introduction cover, is marked "not part of the URAR" and was
left out.

Every value is illustrative specimen data: Betty and Bob Borrower, Agatha Appraiser,
123 Falling Tree Ct, Treeville VA 12345, DEF Bank, ABC Appraisal Co. Nothing needed
redacting. The photo, sketch and chart areas are grey placeholders in the original
("This is where the Subject Property photo would display"). The PDF metadata was reset to
Freddie Mac as author and a title naming the scenario.

## Why this document

An appraisal is the lender's evidence for collateral value, and the redesigned URAR is
what every GSE-delivered appraisal will look like. It is long (21 legal-size pages),
mostly label/value pairs and ruled tables, and its heart is the **sales comparison
grid**: four columns (subject plus three comparables), each comparable carrying a value
and an adjustment cell side by side, spread over two pages. The same dollar amounts
recur across the grid (the subject's $489,000 list and contract price, comp 1's
$460,000 list and sale price, the $491,000 value on three pages), so a value is only
useful if it is grounded to the right row and column.

`schema.json` covers the report identifiers, the Summary, the parties and appraiser
credential, the subject property, every comparable's grid summary, the indicated value,
and the defects table. **57 leaf fields** (counted from the schema).

## Featured fields: one comparable's column in the Summary rows

All on page 15 (report page 15 of 21).

| Field | Value |
|---|---|
| Comp 1 sale price | 460000 |
| Comp 1 net adjustment | 30760 |
| Comp 1 adjusted price | 490760 |
| Comp 1 weight | Most |

Read top to bottom they are the arithmetic of one comparable: sale price plus net
adjustment gives the adjusted price ($460,000 + $30,760 = $490,760), and the weight says
how much the appraiser relied on it. Each box lands on its own cell in the Comparable #1
column, not the neighbouring comps' cells on the same rows. No person is featured.

`sale_price` is pinned to occurrence 1, the Summary row on page 15. Occurrence 0 is the
Sale Price row near the top of the grid on page 14, also correctly grounded.

The request suggested these four plus the **Indicated Value ($491,000)**, which was
dropped: the extracted `indicated_value_sales_comparison` grounds to the Opinion of
Market Value on page 1 (`ok`) and to a Listing Status table on page 13 (`OFF`), never to
the Indicated Value cell on page 15, so it cannot be shown on this overlay.

## Grounding and extraction notes

- **The comparables grid extracts perfectly.** All three comparables' addresses,
  proximity, sale price, sale date, net adjustment, adjusted price and weight are right,
  and every one grounds to its own column on page 14 or 15. A two-page, four-column grid
  with value and adjustment sub-columns is where this was expected to go wrong; it did
  not.
- **Values that repeat across the report ground to their first or summary appearance.**
  `indicated_value_sales_comparison` and `opinion_of_market_value` share $491,000.
  The opinion grounds to page 1 and page 17 (the Reconciliation); the indicated value
  grounds to page 1 and, off-target, to page 13. Neither points at page 15's Indicated
  Value cell.
- **Some Summary ratings ground off.** `overall_quality` (Q4) and `overall_condition`
  (C4) are correct but their ranges point at the grey photo placeholder's description on
  page 5; `effective_date` and `market_value_condition` have a second, off-target range
  on page 6. `subject_property.bedrooms` (5) grounds to the "Total Bedrooms" label rather
  than the value.
- **Booleans and blanks.** The defects table's Yes/No column extracts correctly as
  true/false (inspect_fields reads these `OFF` only because "Yes" is not "True"). The
  second defect's blank Estimated Cost to Repair extracts as 0 rather than null.
- **Placeholders are described, not hidden.** DPT-3 transcribes each grey photo box as a
  figure with a description of the placeholder text, which is accurate but adds noise to
  the parse markdown of a sample like this one.

## Credits

44.60 credits at the standard tier (21-page parse plus extraction), via the jobs API.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py appraisal-report        # spends credits
.venv/bin/python document-types/scripts/build_images.py appraisal-report   # free
.venv/bin/python document-types/scripts/inspect_fields.py appraisal-report --page 15
```
