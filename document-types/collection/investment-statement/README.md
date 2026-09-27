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

## Featured fields: one short position

All on **page 7**, one complete row of the individual account's stock holdings table:

| Field | Value |
|---|---|
| Security (short position) | ENSTAR GROUP LIMITED COM STK USD 1.00 (ESGR) |
| Quantity | -100.00 |
| Ending market value | -13,710.00 |
| Total cost basis | -14,510.99ᶜ |
| Unrealized gain | 800.99 |

This is the hardest row on the page, chosen for that reason:

- **Signs matter.** A short position has a negative quantity, market value and cost basis,
  and a positive gain. Dropping a minus sign anywhere turns the gain into a loss.
- **A footnote marker sits on the number.** The cost basis is printed "-14,510.99" with a
  superscript "c" for its cost basis footnote, and extracts as -14510.99.
- **The description wraps.** The ticker, "(ESGR)", is on a second line under the name.

The row reconciles: −$13,710.00 − (−$14,510.99) = $800.99, so the overlay reads as one
position rather than five unrelated numbers. Price is extracted but not featured, to keep
to five fields.

Page 1 was the first choice. Its portfolio reconciliation grounds perfectly, but a clean
summary table is the easy case, and a holdings table is where statements get difficult.

## What it surfaced

**Tables ground cell by cell.** Every value on page 7 boxes its own cell, including the
short position's negatives and the three-decimal preferred stock price, and
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
.venv/bin/python document-types/scripts/inspect_fields.py investment-statement --page 7 --good
```

`manifest.json` sets `preview_pages` to 1, 4, 7 and 18: the summary, an account summary
with its allocation chart, the featured holdings page and the estimated cash flow table.
