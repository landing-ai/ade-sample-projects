# Auto Loss Run

Source assets for `landing.ai/document-type/auto-loss-run`.

## Sample document

`source/cameron-county-apd-loss-runs-2011-2016.pdf`: the Automobile Physical Damage
section of a Claim/Loss Report produced by the Texas Association of Counties Risk
Management Pool for its member Cameron County, Texas, covering five policy years
(July 2011 to July 2016). **4 pages, landscape.** Pages 1 to 3 list 112 claims under
five policy headers, each closed by a Totals row; page 3 ends and page 4 continues a
summary block that repeats the five Totals rows.

| | |
|---|---|
| Publisher | Texas Association of Counties Risk Management Pool, posted by Cameron County, Texas |
| Source | [cameroncountytx.gov](https://cameroncountytx.gov/wp-content/uploads/Purchasing/Exhibit-X-F-TAC-GL-AL-APD-Loss-Runs-2011-2016.pdf) |
| Retrieved | 2026-10-25 (downloaded by script) |
| Clearance | **Public** |

Cameron County published this loss run on its own official website, under its
Purchasing uploads, as Exhibit X-F to an insurance RFP, so that bidders could price the
account. The solicitation page that links the exhibit was not found, so provenance rests
on the official county domain. The same pool and county produced the workers'
compensation run behind the [`loss-run`](../loss-run/) page; this one is the auto line.

**Nine pages were dropped and no page text was changed.** The original is 13 pages
across three lines of coverage. Only original pages 5 to 8, Automobile Physical Damage,
are kept, unaltered. On those pages every claimant is the county itself. The Automobile
Liability pages (1 to 4) and General Liability pages (9 to 13) name private claimants;
they were removed whole with `redact.py --drop-pages` before the file entered the repo
or was parsed. The output was verified to carry none of the dropped pages' claimant
strings, and the PDF's document metadata was cleared.

## Why this document

The `loss-run` page is a long workers' compensation run summarised by period. This one
is a commercial auto run read at claim level: a 10-column table where most rows are $0,
with a policy header and a Totals row bracketing each year, and two years that break
across a page. Recoveries can exceed what was paid, so Total Incurred ($48) is sometimes
far below Pool Paid ($4,970); the columns cannot be reconstructed from one another and
have to be read by position.

## Schema

`schema.json` resolves to **24 leaf fields**: report details (title, report date,
carrier, insured member, year range), and for each policy year its line of coverage,
policy ID and effective date range, every claim row (ten columns), and the Totals row.
It does not extract the cross-year summary block on pages 3 and 4, which repeats the
Totals rows.

The first extraction read the 2015-16 year one column to the left: each claim's Pool
Paid landed in Total Incurred, Recoveries in Pool Paid, and so on, while the other four
years were right. The parse was correct. Spelling out the ten-column order in the
`claims` description fixed it; the committed extraction has every year's claim rows
summing to its printed Totals row, within the source's own $1 rounding.

## Featured fields: one claim in its policy year

All on page 1 (original page 5):

| Field | Value |
|---|---|
| Policy ID | RMP-00370-201107 |
| Claim number | APD201102084-1 |
| Cause of loss | STRUCK AN ANIMAL |
| Claim total incurred | $13,043 |
| Policy-year total incurred | $17,240 |

The overlay reads from the policy header down through the year's largest claim to the
Totals row it rolls into. The request's notes suggested page 5 and, as suggestions only,
the line of coverage and policy ID, effective date range, this claim's number, loss date,
total incurred, pool paid and cause, the year's claim count and total incurred, and the
report date. All of them ground `ok` on this page; five were picked to tell one story
within the overlay limit.

## Grounding

Clean on the featured page: every claim cell, policy header and Totals cell on page 1
resolves to its own cell at its first occurrence. Report-level fields ground to the page
header, and the carrier name to the logo's figure description.

## Credits

At standard tier: **40.9** for the parse and first extraction, and 32.8 for one
extraction-only rerun to fix the column shift. **73.7 in total**. Re-creating the
committed output from scratch costs about 41.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py auto-loss-run                 # parse + extract
.venv/bin/python document-types/scripts/run_ade.py auto-loss-run --extract-only  # extract only
.venv/bin/python document-types/scripts/inspect_fields.py auto-loss-run --page 1
.venv/bin/python document-types/scripts/build_images.py auto-loss-run
```
