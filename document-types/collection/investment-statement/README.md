# Investment statement

Source assets for `landing.ai/document-type/investment-statement`.

## Sample document

`source/sample-new-fidelity-acnt-stmt.pdf` — Fidelity's sample monthly investment report
for July 2015, covering three accounts: an individual brokerage account, a traditional
IRA and a 529 education account. **28 pages, landscape (756×612)**, with a full text
layer. The last three pages are disclosures printed on 792×612 pages rotated 90°.

| | |
|---|---|
| Publisher | Fidelity Investments |
| Source | [fidelity.com/…/sample-new-fidelity-acnt-stmt.pdf](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/sample-new-fidelity-acnt-stmt.pdf) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Fidelity publishes this sample on fidelity.com to show customers what a statement looks
like, and every page is marked "*** SAMPLE STATEMENT *** For informational purposes
only". All the personal data is specimen: the account holder is "John W. Doe, 100 Main
St.", the account numbers are 111-111111, 222-222222 and 333-333333, and the phone
numbers are Fidelity's and SIPC's published lines. No redaction was needed.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **multi-account financial statement**, and its first vendor
specimen, which is the cleanest provenance a sample can have:

- **Long and varied.** 28 pages of summaries, allocation pie charts, holdings tables for
  stocks, bonds, mutual funds and ETFs, activity ledgers, an estimated cash flow table,
  and dense disclosures.
- **The same structure repeated per account.** Each account has its own summary, holdings
  and activity, so a value such as a stock's name or an account number appears in many
  places.
- **Rotated pages.** The three closing disclosure pages are stored rotated 90°. The
  consolidated 1099's rotated mailing panel was dropped, so these are the first rotated
  pages the collection keeps.

## Featured fields: one reconciliation

All on **page 1**, from the portfolio summary's This Period column:

| Field | Value |
|---|---|
| Beginning portfolio value | $253,221.83 |
| Additions | 59,269.64 |
| Subtractions | -45,430.74 |
| Change in investment value | 7,161.47 |
| Ending portfolio value | $274,222.20 |

The five values reconcile: $253,221.83 + $59,269.64 − $45,430.74 + $7,161.47 =
$274,222.20, so the overlay reads as one calculation. Transaction costs (−$139.77) are
extracted but not featured, because they are a sub-line already included in
subtractions.

Page 1 prints $274,222.20 three times: as the headline portfolio value, and in both the
This Period and Year-to-Date columns. `ending_value` boxes the This Period cell, the one
the schema asks for.

## What it surfaced

**Tables ground cell by cell.** Every featured value boxes exactly its table cell, and
across the whole document only seven ranges are flagged. Three are formatting: a line
break inside a description cell, or a section heading ("Common Stocks") merged into the
first holding's description. Two are the period dates, normalized to ISO. The other two
are the error below.

**"unknown" became 0.** General Motors in the IRA has its cost basis and unrealized gain
printed as "unknown". Extraction returned `0` for both, although the schema says to
return null when the basis is not available. A zero cost basis is a wrong number, not a
missing one, and would overstate the gain in any downstream calculation.

**The sample has a typo, and ADE read it faithfully.** Page 2 lists the individual
account's beginning value as "$88,0853.95". Extraction returned 880853.95. The column
arithmetic and page 4 both give $88,053.95, so the error is in Fidelity's PDF, not in the
parse. The value is not featured. It is a useful reminder that extraction reports what a
page says, and checking figures against each other is a separate step.

**Rotated pages parse as ordinary text.** The three disclosure pages come back upright,
with markdown lengths close to the PDF's own text: 4,550 against 4,635 characters,
2,495 against 2,496, and 12,892 against 12,652.

**Holdings are complete.** All 12 stock positions come back, 5 in the individual account
and 7 in the IRA, each with the right account number from its page header.

## Extraction

`schema.json` was written for this document, with **23 leaf fields** in four groups:
`statement` (institution, account holder, period), `portfolio_summary` (the page 1
reconciliation), `accounts[]` (from the Accounts Included table) and `stock_holdings[]`
(eight fields per position). Everything populates, with no warnings. The period dates
are normalized to ISO, so they no longer match the printed "July 1 – July 31, 2015" and
are flagged, though they are right.

## Cost

**55.80 credits** at standard tier for 28 pages: 35.30 to parse, 20.50 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investment-statement                # 55.80 credits
.venv/bin/python document-types/scripts/run_ade.py investment-statement --extract-only # 20.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py investment-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py investment-statement --page 1 --good
```

`manifest.json` sets `preview_pages` to 1, 4, 7 and 18: the summary, an account summary
with its allocation chart, a holdings table and the estimated cash flow table.
