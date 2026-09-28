# Utility bill

Source assets for `landing.ai/document-type/utility-bill`.

## Sample document

`source/pseg-electric-gas-bill-redacted.pdf` — a PSE&G residential electric and gas bill
for May 19 to June 17, 2020, redacted. **4 pages, portrait (612×792)**, with a full text
layer: a summary with a payment stub on page 1, a charges overview on page 2, gas details
on page 3 and electric details on page 4, each detail page with a usage chart.

| | |
|---|---|
| Publisher | PSE&G (Public Service Electric and Gas Company) |
| Source | [scribd.com/document/500641462/PSEG-Sample-Electric-Bill](https://www.scribd.com/document/500641462/PSEG-Sample-Electric-Bill) |
| Retrieved | 2026-09-27 |
| Clearance | Redacted |

## Redaction

Despite "Sample" in its Scribd title, this is a real customer's bill, uploaded to Scribd by
a third party. Scribd is a user-upload site, so the uploader is not the publisher, and the
bill is treated as a personal record. The local copy used is
`Use_Cases/Utility_Bills/input_folder/electric2.pdf`, **where the same bill is already
committed to this repo unredacted.** That copy is outside this folder and is not changed
here.

Nine identifiers were replaced using `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it, 21 replacements across the four pages:

| What | Replaced with | Occurrences |
|---|---|---|
| Customer's name | JANE SAMPLE | 5 |
| Service address, street | 100 MAIN ST APT A | 2 |
| Service address, town, state and ZIP | ANYTOWN NJ 00000-0000 | 2 |
| Account number, spaced | 68 736 306 51 | 1 |
| Account number | 6873630651 | 5 |
| Invoice number | 183722332744 | 3 |
| Point-of-delivery ID | PE975560397498155489 | 1 |
| Electric meter number | 245603755 | 1 |
| Gas meter number | 7651211 | 1 |

**The numbers are plausible stand-ins, not zeros.** The name and address are obviously
fake, but the account, invoice, point-of-delivery and meter numbers are random numbers of
the same shape from `document-types/scripts/plausible.py`, so the bill still reads as a
bill. The account number is one stand-in printed in both its forms, spaced and unspaced.
None is derived from the original. This sample was first redacted with all-zero
stand-ins and redone this way, which is now the default for every redaction.

The PDF metadata was also cleared. PSE&G's name, logo, phone numbers and PO box, and the
bill's amounts, dates and usage, are left as printed.

Some replacements are visibly edited: the name in the page headers came out in regular
weight rather than bold, and the account number in the payment stub's scan line is
Helvetica rather than the original OCR font.

**Verified:** no original identifier is extractable from the committed PDF, and none
appears anywhere in this folder. The original values are deliberately not recorded here
or in `manifest.json`. The rules file used by `redact.py` stays outside the repo.

## Why this document

The collection's first **utility bill**, and the first sample built on a team schema that
had to be extended:

- **Two services on one bill.** Electric and gas each have a detail page with a meter,
  readings, usage, delivery and supply charges, and a total.
- **The same identifier everywhere.** The account number is printed six times in two
  formats, across all four pages.
- **Charges in a dotted leader list.** Each charge sits at the right end of a dotted line,
  with subtotals in bold.

## Featured fields: the electric charges

All on **page 4**, as the request asked, with the request's own field names as labels:

| Field | Value |
|---|---|
| Account number | 6873630651 |
| Meter number | 245603755 |
| Delivery charges | $16.71 |
| Service charges | $4.95 |
| Total electric charges | $46.42 |

The account and meter numbers shown are plausible stand-ins, not the originals. The
account number is pinned to its page 4 occurrence, in the page header, and the total to
its page 4 occurrence, the bar; the total is also printed on page 2's summary.

## The schema was extended

`schema.json` is `Use_Cases/Utility_Bills/utility_bill.json`, the team's schema, with
**two fields added** and nothing else changed:

- `electric_charges.monthly_service_charge`
- `electric_charges.total_delivery_charges`

The request asked for delivery charges and service charges, and the team schema has no
field for either: it covers totals per service, meters, usage and account details, not
the charge lines. The skill's rule is to use a supplied schema unchanged, so the run
stopped and asked, and the document owner chose to extend it. Extraction was then re-run
on the same parse. Both new fields extract correctly and box exactly their amounts. The
original file in `Use_Cases/` is unchanged.

## What it surfaced

**A total folded into a chart.** "Total electric charges $46.42" is printed on a shaded
bar directly above the electric usage chart, and the parse includes the bar in the chart's
figure block. The value extracts correctly, but its box covers the bar and the whole chart
beneath it. It is featured because it was requested; the crop shows the total at the top.

**A plain list grounds precisely.** The monthly service charge and the delivery total, at
the right end of dotted leader lines, box exactly their amounts, as do the meter number
and the kWh usage line.

**Normalized dates are flagged.** The schema asks for dates it then gets as ISO
(`2020-06-19`), or as `06-17-2020` for the service period, which no longer match the
printed "June 19, 2020". The values are right.

**A yes-or-no about charts.** `usage_bar_chart` extracts as true and grounds to the three
chart figures, which the consistency check flags.

32 of 45 rows in the grounding check are `ok`; the 13 flagged are the dates, the chart
boolean, and the service address, which this run grounds line by line.

## Extraction

**24 leaf fields**: the team schema's 22 plus the two added. Provider, account and service
address, billing summary, electric charges and gas charges all populate, with no warnings.
Gas extracts from page 3: $20.67 for 17.806 therms.

## Cost

**25.30 credits** at standard tier in total, across four runs: the first run with the team
schema (9.00), a re-extraction with the two added fields (3.60), a full re-run after the
numbers were re-redacted with plausible stand-ins (9.10), and one more re-extraction
(3.60). That last one was needed because the full re-run returned the account number with
page 1 ranges only; range selection varies between runs, and the repeat restored the page 4
range. Regenerating from scratch costs 9.10 (5.50 to parse, 3.60 to extract).

## Regenerating

```bash
# Redaction, from the local copy, with the rules file kept outside the repo:
.venv/bin/python document-types/scripts/redact.py Use_Cases/Utility_Bills/input_folder/electric2.pdf \
    document-types/collection/utility-bill/source/pseg-electric-gas-bill-redacted.pdf \
    --rules <outside-the-repo>/rules.json

.venv/bin/python document-types/scripts/run_ade.py utility-bill                # 9.10 credits
.venv/bin/python document-types/scripts/run_ade.py utility-bill --extract-only # 3.60, schema iteration
.venv/bin/python document-types/scripts/build_images.py utility-bill           # free
.venv/bin/python document-types/scripts/inspect_fields.py utility-bill --page 4
```
