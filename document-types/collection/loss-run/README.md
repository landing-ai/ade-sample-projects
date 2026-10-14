# Loss Run

Source assets for `landing.ai/document-type/loss-run`.

## Sample document

`source/cameron-county-wc-loss-runs-2015-2019.pdf`: a workers' compensation Claim/Loss
Report produced by the Texas Association of Counties Risk Management Pool for its member
Cameron County, Texas, covering five coverage years (2015 to 2019). **31 pages,
landscape.** The 1,309 individual claims span pages 1 to 31; page 31 also closes the
last period and summarises all five periods with a grand total.

| | |
|---|---|
| Publisher | Texas Association of Counties Risk Management Pool, posted by Cameron County, Texas |
| Source | [cameroncountytx.gov](https://www.cameroncountytx.gov/wp-content/uploads/2022/10/Cameron-County-WC-Loss-Runs-2015-2019.pdf) |
| Retrieved | 2026-10-04 (downloaded by script) |
| Clearance | **Public** |

Cameron County published this loss run on its own official website alongside its
Workers' Compensation RFP 1470, so that brokers bidding on the account could price it.
A loss run is exactly the document an RFP like that has to carry, which makes this a
public record of a real one rather than a mock-up.

**No page text was redacted.** The Claimant Full Name column is blank at source on every
page, so the report carries claim numbers, loss dates, status, cause-of-loss categories
and dollar amounts, but no claimant identities. The PDF's document metadata named the
pool staff member who ran the report; it was cleared before the file entered the repo,
and the source PDF now carries no metadata.

## Why this document

A loss run is the claims history an underwriter reads before quoting a renewal. This one
tests a long, uniform table that runs over 30 pages with a section break and a subtotal
row for each coverage period, then repeats every subtotal in a summary block on the last
page. Telling those two copies apart is the hard part.

Cause-of-loss text is truncated at the column width in the source ("Struck or Injured By
Fellow Worker; Patient or Oth"), and most rows are $0: both are faithful to the original.

## Schema

`schema.json` resolves to **24 leaf fields** in four groups: report details (carrier,
insured member, line of coverage, year range, run date), the policy header for each
period (coverage number and dates), the per-period summary rows, and the grand total. It
summarises by period and does **not** extract the 1,309 claim rows; a claim-level schema
for a document this size is a separate exercise.

Getting the period summaries right took three extraction passes. The first version asked
for one array combining each period's coverage number with its totals, and the model
read `$0` cells as null. Saying "a printed $0 is 0" fixed the nulls but produced nine
periods instead of five, because each period's totals appear twice. The version
committed here splits the coverage numbers (taken from the section headers) from the totals
(taken only from the last-page summary block), and returns all five periods correctly.

## Featured fields: one coverage year

All on page 31, following the 2016 row of the summary block:

| Field | Value |
|---|---|
| Coverage period | Jan 1, 2016- Jan 1, 2017 |
| Count of claims | 276 |
| Total paid | $605,268 |
| Outstanding reserve | $27,648 |
| Total incurred | $619,349 |

It is the only period with both payments and an open reserve, so the overlay shows the
paid, reserved and incurred split a loss run exists to report. The request's research
notes suggested this period's count, paid and reserve, plus the grand-total claim count
and incurred. The grand totals could not be featured (see below).

## Grounding

The per-period summary rows ground perfectly: all 40 values in the block resolve to
their own cell on page 31, including the `$0` cells and the parenthesised recoveries.

The **grand total does not ground**. Extraction returns the right values (1,309 claims,
$2,047,261 incurred after ($33,963) recoveries), but the claim count is grounded to a
page 19 header and the six dollar totals come back with no ranges at all. The grand
total is printed twice, as the "Workers' Compensation" coverage line and the "Grand
Total:" line, identical. That duplication may explain it. Grand-total deductible came back
null although the row prints `$0`.

The run date is extracted correctly as 2022-08-02 but grounds `OFF`, against "Aug 2,
2022 3:09:57 PM". Coverage period start and end dates in the section headers are mostly
`OFF` for the same reason: "Jan-01-2016" is not recognised as 2016-01-01.

## Credits

At standard tier: **150.6** for the committed parse and first extraction (about 89 parse,
62 extract), and 122.6 more for the two extraction-only reruns while fixing the schema.
**335.2 in total**. Re-creating the committed output from scratch costs about 150.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py loss-run                 # parse + extract
.venv/bin/python document-types/scripts/run_ade.py loss-run --extract-only  # extract only
.venv/bin/python document-types/scripts/inspect_fields.py loss-run --page 31
.venv/bin/python document-types/scripts/build_images.py loss-run
```
