# Property tax bill

Source assets for `landing.ai/document-type/property-tax-bill`.

## Sample document

`source/clark-county-property-tax-statement-sample.pdf` — the Clark County (Washington)
Treasurer's sample 2026 property tax statement. **1 page, portrait (612×900)**, with a full
text layer: the statement header and account number, property information, value
information with levy rates, an account summary, past-due details, a 12-line tax and
assessment detail by district, and a payment coupon.

| | |
|---|---|
| Publisher | Clark County (WA) Treasurer |
| Source | [clark.wa.gov/…/tax-statement-sample.pdf](https://clark.wa.gov/sites/default/files/media/document/2026-03/tax-statement-sample.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

## Clearance

The Treasurer's office publishes this sample itself and links it from the county's
"Understanding your tax bill" page. Every personal value on it is specimen data: the owner
is "SAMPLE TAXPAYER", the property and mailing addresses are on "MAIN ST", and the legal
description is "#13 TOWNSVILLE ADDITION". The only person named is the elected County
Treasurer, in the office letterhead in her official capacity. The phone numbers, PO boxes
and website are the office's own. **No redaction was needed.**

Two changes were made to the downloaded file:

- **Only page 1 was kept.** The source is an 11-page explainer: page 1 is the sample
  statement, pages 2–11 explain each lettered section.
- **The PDF metadata was cleared.** It named the individual who built the file in Canva.

The teal "Understanding your Tax Statement" banner and the lettered callouts (A–G) are the
publisher's own and were left in place; ADE reads the callout letters into the markdown as
stray single characters, which does not affect extraction.

## Why this document

The collection's first **property tax bill**, and a dense one-page government statement:

- **Seven lettered sections of different shapes** on one page — key-value panels, a
  value table, a past-due grid, a district list and a payment coupon.
- **Levy rates to 10 decimal places**, which a number type would round.
- **The bill reconciles.** Assessed value × levy rate equals the sum of the levy
  districts, and the districts plus assessments equal the full-year amount.
- **Two addresses that look alike**: the property at "134 MAIN STREET" and the owner's
  mailing address at "1234 MAIN ST" on the coupon.

## Featured fields: how the bill is computed

All on **page 1**. The request's notes suggested four fields; all four ship, with the levy
rate added because it is what links the value to the tax:

| Field | Value |
|---|---|
| Assessed value | $756,979 |
| Levy rate | 6.4423487853 |
| School district tax | $345.47 |
| Full year due | $5,157.93 |
| First half due | $2,579.01 |

$756,979 × 6.4423487853 / 1,000 = $4,876.72; the nine levy districts in the detail, school
district first, sum to $4,876.71. The three flat assessments (clean water, lighting,
mosquito control, $281.22) bring it to $5,157.93, payable as two halves. Every box sits
exactly on its value.

## What it surfaced

**Tables ground cell by cell.** All 12 district rows, all three past-due rows and both value
rows ground `ok`, each to its own cell. The account summary amounts box exactly their
figures rather than the label row.

**A long number survives as text.** `levy_rate` is a string in the schema, and both rates
came back with all 10 decimal places.

**The property address was grounded to the wrong address too.** `property.property_address`
extracts correctly as "134 MAIN STREET VANCOUVER WA 98660", but its ranges cover both the
property panel and the owner's mailing address on the coupon ("1234 MAIN ST", "VANCOUVER,
WA 98660"). The value is right; the grounding conflates two similar addresses.

**An empty cell came back as zero.** The 2025 row of the value table has no % change; the
schema asks for null in that case, and extraction returned 0 with no grounding.

**Multi-line values ground line by line.** The payment remittance address is three lines on
the coupon and grounds as three ranges, so the check flags it as `OFF`; the value is right.

62 of 71 rows in the grounding check are `ok`. The 9 flagged are the property address
(4 ranges), the remittance address (3), the 2025 % change, and one of the three ranges for
the taxing authority's name, which points at the letterhead line "Alishia Topper CLARK
COUNTY" rather than a line containing "Clark County Treasurer".

## Extraction

**28 leaf fields**: taxing authority, tax year and account number, property information,
value information by year, amounts due, past-due details, the district detail and the
voter-approved amount. Every field populates, with no warnings.

## Cost

**3.90 credits** at standard tier, one run (parse and extract together).

## Regenerating

```bash
# Page 1 of the downloaded source, with metadata cleared:
.venv/bin/python -c "import fitz;d=fitz.open('tax-statement-sample.pdf');d.select([0]);d.set_metadata({});d.del_xml_metadata();d.save('document-types/collection/property-tax-bill/source/clark-county-property-tax-statement-sample.pdf',garbage=4,deflate=True)"

.venv/bin/python document-types/scripts/run_ade.py property-tax-bill                # 3.90 credits
.venv/bin/python document-types/scripts/run_ade.py property-tax-bill --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py property-tax-bill           # free
.venv/bin/python document-types/scripts/inspect_fields.py property-tax-bill --page 1
```
