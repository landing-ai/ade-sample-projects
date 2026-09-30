# IRA statement

Source assets for `landing.ai/document-type/ira-statement`.

## Sample document

`source/ira-statement-redacted.pdf` — a monthly Premiere Select Rollover IRA statement
for September 1 to September 30, 2025. **10 pages, landscape (US Letter)**: a summary
with a portfolio value chart, an account overview (allocation, change in value,
retirement contributions and distributions, income, fees), a beneficiary summary and
messages, holdings, activity, bank deposit detail, footnotes and a glossary.

| | |
|---|---|
| Publisher | Commonwealth Financial Network (broker-dealer); account carried by National Financial Services LLC; advised by SageRock Wealth Partners |
| Source | [scribd.com/document/970556624](https://www.scribd.com/document/970556624) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted |

A real account holder's statement, uploaded to Scribd by a third party and downloaded by
hand, because Scribd blocks scripted requests. Scribd is not the publisher, so it is
treated as a personal record. The listing's title ends in the account number's last
digits, so the url is recorded without it.

Replaced with `document-types/scripts/redact.py`, which removes the underlying text
rather than covering it:

| What | With |
|---|---|
| Account holder's name, in every page header and the mailing block | JOHN Q SAMPLE |
| Mailing address | 100 MAIN ST, ANYTOWN MI 00000 (state kept) |
| Account number, on every page | A plausible random stand-in of the same shape |
| Mail envelope code, on every page | Random letters of the same length |
| Three designated beneficiaries | JANE Q SAMPLE, ALEX Q SAMPLE, SAM Q SAMPLE |
| Two financial advisors' names, rep code and email | A ADVISOR / B ADVISOR, a random rep code, advisor@example.com |

Kept as printed: every balance, holding, transaction and fee, the beneficiaries'
allocations, relationships and designations, and the firms' names, business addresses,
phone numbers and website. The PDF metadata was cleared. Verified: no original value is
extractable from the committed PDF, no other line of text changed, and none appears in
any file in this folder. The stand-in name is shorter than the original, so the page
header leaves a gap before "- Premiere Select Rollover IRA".

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **IRA statement**, and different from the workplace plans at
`401k-statement` and `retirement-statement`:

- **Three firms on one statement.** The broker-dealer, the clearing firm that carries the
  account and the advisory firm each appear, and a schema has to tell them apart.
- **Beneficiaries.** Designated beneficiaries with allocations, relationships and
  primary or contingent status, which neither workplace statement carries.
- **IRA-specific activity.** Contributions for the current and prior tax year, and
  distributions, reported separately from ordinary income.
- **Landscape pages and a brokerage layout,** with multi-line security descriptions and
  estimated yield and income per holding.

## Featured fields: what a lender verifies

All on page 1. The request named no page or fields; following the lending framing chosen
for the 401(k), bank and HELOC statements:

| Field | Value |
|---|---|
| Account holder | JOHN Q SAMPLE |
| Account number | B19-187999 |
| Statement date | 2025-09-30 |
| Account value | $164,145.49 |
| Provider | Commonwealth Financial Network |

The account holder and account number are the stand-ins. The account holder's box covers
the whole header line, which also carries the account type. The provider is the
broker-dealer, boxed on its name in the return-address block.

**The statement date is flagged, and correct.** It is extracted as the ISO date
2025-09-30 and boxed on the printed "STATEMENT FOR THE PERIOD SEPTEMBER 1, 2025 TO
SEPTEMBER 30, 2025", so `build_images.py` warns that the value is not in the boxed text.
The box contains the date in another format; the crop was checked by eye.

## What it surfaced

**The three firms come back right.** Broker-dealer, custodian and advisory firm are each
extracted correctly, although the advisory firm appears only as a logo and in small
print.

**Every value extracts correctly.** The nine holdings sum to the $164,145.49 total, the
change in value and retirement activity match, and the beneficiaries come back with
their allocations and designations.

**Descriptions are inconsistent across rows.** Seven of the nine holding descriptions
absorb the "Estimated Yield ... Dividend Option Cash" lines printed beneath the security
name, and two do not. The cash sweep's estimated annual income comes back as 0 where
nothing is printed.

**Dates are normalized.** The period dates come back as ISO dates, so they are flagged as
not matching the printed period, though they are right.

## Extraction

**30 leaf fields**: account holder, type and number, the three firms, the period, the
beginning and ending values, the change in value, retirement contributions and
distributions, allocation, holdings and beneficiaries. Everything extracts correctly
apart from the small inconsistencies above.

## Cost

**27.80 credits** at standard tier for 10 pages: 15.90 to parse, 11.90 to extract.

## Regenerating

```bash
# The source is a manual download from the url, redacted with redact.py and a rules
# file kept outside the repo. The committed PDF is the redacted one.
.venv/bin/python document-types/scripts/run_ade.py ira-statement                # 27.80 credits
.venv/bin/python document-types/scripts/run_ade.py ira-statement --extract-only # 11.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py ira-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py ira-statement --page 1
```
