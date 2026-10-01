# Rate lock

Source assets for `landing.ai/document-type/rate-lock`.

## Sample document

`source/wheda-sample-rate-lock-confirmation.pdf` — WHEDA's sample mortgage rate lock
confirmation for its correspondent lending channel, dated February 24, 2014. **1 page,
portrait (legal, 8.5 × 14 in)**: the lock itself, pricing adjustments, the loan officer,
and a loan summary of borrower, property, loan, automated underwriting and mortgage
insurance details.

| | |
|---|---|
| Publisher | Wisconsin Housing and Economic Development Authority (WHEDA) |
| Source | [wheda.com/…/sample-rate-lock-confirmation---correspondent-channel.pdf](https://www.wheda.com/globalassets/documents/mortgage-lending/sample-rate-lock-confirmation---correspondent-channel.pdf) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

WHEDA, Wisconsin's housing finance agency, publishes this as a sample in its mortgage
lending materials. The borrower and property are placeholders ("John S Correspondent",
123 Main Street, Waukesha). The loan officer contact is a named WHEDA staff member with
a work phone and email, which WHEDA itself publishes as a business contact in the sample;
it is kept as printed, and not featured. No redaction was needed.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **mortgage origination document**, from the middle of a loan's
life rather than its end:

- **The terms that matter fit in one table row.** Program, payment type, amount, rate,
  price, lock date, lock period and expiry, in eight narrow columns.
- **A dense two-column summary** of borrower, property and loan attributes, mostly
  label and value pairs, many of them yes or no.
- **Pricing inputs next to the price.** Credit score, LTV and occupancy sit alongside
  the rate they produced.

## Featured fields: the lock

All on the page. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| Reference number | 800203 |
| Loan program | HFA Preferred with MI Correspondent 30 year |
| Locked rate | 4.625% |
| Lock expiration date | 2014-04-10 |
| Middle credit score | 715 |

What a loan processor checks: which lock, on which program, at what rate, until when,
and the credit score the pricing assumed.

**The locked rate's box is the whole row.** See below. **The expiration date is flagged,
and correct:** it is extracted as the ISO date 2014-04-10 and boxed on the printed
"4/10/2014", so `build_images.py` warns that the value is not in the boxed text; the
crop was checked by eye.

## What it surfaced

**The key row did not split into columns.** The Rate Lock table's data row parses as one
run of text in a single cell, "$95,000.00 4.625% 102.000 2/24/2014 45 days 4/10/2014",
from Loan Amount to Lock Period. Every value is still extracted correctly, but loan
amount, rate, price, lock date and lock period all ground to that one box, so only one of
them can be featured; the rate is, and its box shows the whole run. The expiry date
parses as its own cell.

**Labels instead of values, one cell adrift.** In the property column, property type and
occupancy ground to their labels ("Property Type", "Property Purpose") rather than to
"SFR" and "Primary Residence". The property address grounds across two lines.

**Yes and no become booleans.** First-time home buyer and self-employed come back as
false from the printed "No", so they are flagged as not matching their boxed text.

**Everything extracts correctly,** including the pricing adjustment totals, LTV and CLTV
from the combined "95.000% / 95.000%", and the term from "360 / 360".

## Extraction

**34 leaf fields**: lender, confirmation time, reference and borrower; the lock's
program, payment type, amount, rate, price, dates and period; the pricing adjustment
totals; the loan officer; and borrower, property and loan attributes.

## Cost

**3.10 credits** at standard tier for 1 page: 1.40 to parse, 1.70 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/rate-lock/source/wheda-sample-rate-lock-confirmation.pdf \
  "https://www.wheda.com/globalassets/documents/mortgage-lending/sample-rate-lock-confirmation---correspondent-channel.pdf"
.venv/bin/python document-types/scripts/run_ade.py rate-lock                # 3.10 credits
.venv/bin/python document-types/scripts/run_ade.py rate-lock --extract-only # 1.70, schema iteration
.venv/bin/python document-types/scripts/build_images.py rate-lock           # free
.venv/bin/python document-types/scripts/inspect_fields.py rate-lock --page 1
```
