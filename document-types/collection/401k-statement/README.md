# 401(k) statement

Source assets for `landing.ai/document-type/401k-statement`.

## Sample document

`source/401k-statement-redacted.pdf` — a quarterly statement for the Publix Super
Markets, Inc. 401(k) SMART Plan, administered by Voya Financial, January 1 to March 31,
2023. **7 pages, portrait (US Letter)**: an account summary with a balance history chart,
an estimated retirement income illustration, holdings by fund, contribution rates and
investment elections, an account activity table, fees and messages, and two scanned
plan-sponsor inserts (fund performance, and news about the company match and Publix
stock dividends).

| | |
|---|---|
| Publisher | Voya Financial, recordkeeper for the Publix Super Markets, Inc. 401(k) SMART Plan |
| Source | [scribd.com/document/816135454](https://www.scribd.com/document/816135454/Safari) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted |

A real participant's statement, saved to PDF from Safari on an iPhone and uploaded to
Scribd under the title "Safari". Scribd is not the publisher, so it is treated as a
personal record, and it was downloaded by hand because Scribd blocks scripted requests.

Replaced with `document-types/scripts/redact.py`, which removes the underlying text
rather than covering it:

| What | With |
|---|---|
| Participant's name, on every page | JANE Q SAMPLE |
| Street address | 100 MAIN ST |
| City, state and ZIP | ANYTOWN FL  00000 (state kept) |
| Employee number | A plausible random stand-in, keeping the leading zeros |

Kept as printed: the plan, sponsor and recordkeeper, every balance, fund and price, the
contribution rates and elections, the payroll location code, and the two scanned inserts.
None identifies the participant once the name, address and employee number are gone. The
PDF metadata was cleared. Verified: no original value is extractable from the committed
PDF, no other line of text changed, and none appears in any file in this folder.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **401(k) statement**, and different from the TIAA statement at
`retirement-statement`:

- **Employer stock.** Nearly half the account is Publix stock, with a cash component and
  an internal transfer between them in the activity table.
- **A recordkeeper's layout.** Voya's orange panels, icon rows and a balance history bar
  chart, where the TIAA statement is plain tables.
- **Scanned pages in a digital PDF.** Pages 6 and 7 are images of the plan sponsor's
  inserts, so the parse has to read them by OCR; the fund performance table on page 6
  comes back as a table.
- **Payroll detail.** Contribution rates by category and investment elections for future
  contributions.

## Featured fields: what a lender verifies

All on page 1. The request named no page or fields; following the lending framing used
for the bank and HELOC statements, these are the fields a lender reads to verify
retirement assets:

| Field | Value |
|---|---|
| Participant | JANE Q SAMPLE |
| Plan | 401(k) SMART Plan |
| Account value | $13,650.02 |
| Employee contributions | $542.08 |
| Employer contributions | $572.87 |

The participant is the stand-in name. The account value is the closing value in the
summary table. The summary reconciles: $11,412.38 opening, plus $542.08 and $572.87 in
contributions and $1,122.69 in gains, is $13,650.02.

## What it surfaced

**The employer's name is inside a panel that grounds as one block.** The plan sponsor,
"PUBLIX SUPER MARKETS, INC. 401(K) SMART PLAN", is printed as the banner of the orange
panel that also holds the Account Balance History chart, and extraction grounds it to the
whole panel. It extracts correctly but its box is far too loose to feature, so the
participant is featured instead.

**The headline figure grounds to its neighbour.** The large "$13,650.02" in the orange
account value banner is not where `account_value` points; its range lands on a nearby
block. The same figure in the summary table grounds exactly, and is the one featured.

**Everything extracts correctly.** All five holdings with units, prices and values, both
contribution rates, both annuity estimates, the summary, and the plan, sponsor and
recordkeeper. The employee number comes back with its leading zeros, as the schema asks.

**Dates are normalized.** The period dates come back as ISO dates, so they are flagged as
not matching the printed "January 1, 2023 - March 31, 2023", though they are right.

## Extraction

**25 leaf fields**: plan, sponsor, recordkeeper, participant and employee number, the
period, the account value and seven-line activity summary, performance, holdings,
contribution rates and the estimated monthly income. Everything extracts correctly.

## Cost

**17.10 credits** at standard tier for 7 pages: 10.30 to parse, 6.80 to extract.

## Regenerating

```bash
# The source is a manual download from the url, redacted with redact.py and a rules
# file kept outside the repo. The committed PDF is the redacted one.
.venv/bin/python document-types/scripts/run_ade.py 401k-statement                # 17.10 credits
.venv/bin/python document-types/scripts/run_ade.py 401k-statement --extract-only # 6.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py 401k-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py 401k-statement --page 1
```
