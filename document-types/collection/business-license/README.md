# Business license

Source assets for `landing.ai/document-type/business-license`.

## Sample document

`source/broward-county-local-business-tax-receipt-sample.pdf` — a specimen Broward County
Local Business Tax Receipt, valid October 1, 2019 through September 30, 2020. **1 page,
landscape**, a single raster image: the only text layer is the red "This is a sample of a
local business tax receipt" banner added by the publisher.

Florida has no general business licence; its counties and cities issue a Local Business
Tax Receipt instead, which is what a Florida business shows when asked for its business
license. The receipt says so itself: the tax "is non-regulatory in nature" and the receipt
"does not indicate that the business is legal".

| | |
|---|---|
| Publisher | Broward County (receipt format); published as a sample by the Florida State Minority Supplier Development Council |
| Source | [fsmsdc.org/…/8-Broward-county-Generic.pdf](https://fsmsdc.org/wp-content/uploads/2023/02/8-Broward-county-Generic.pdf) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

The Florida State Minority Supplier Development Council publishes this file in the sample
documents library on its certification pages, which carries a disclaimer for its sample
documents. It is a specimen filled with placeholder data — Generic Business LLC, owner
Juan B Generic, 123 Fourth St — not a real business, and the publisher's banner crosses
the page. No redaction was needed. The PDF metadata holds only the Acrobat creator,
producer and dates.

The business phone printed on the specimen is the well-known 867-5309 placeholder. It is
part of the publisher's image, extracted as printed, and not featured.

## Why this document

The collection's first **business license**, and a small, clean test of a different kind
from the long forms around it:

- **Raster only.** No text layer under the receipt; everything is read from the image.
- **Label and value in different typefaces.** Bold sans-serif labels, monospaced typed
  values, sometimes on a different baseline from their label.
- **A sparse count row.** Rooms, Seats, Employees, Machines, Professionals, with only
  Employees filled. Blank should mean null, not zero.
- **A fee table** with a "For Vending Business Only" header spanning five columns.
- **A document that says what it is not.** The schema asks whether it is a regulatory
  license, which has to be inferred from the disclaimer paragraph.

## Featured fields: the receipt as a record

All on page 1. The request named no fields; its notes suggested receipt number, business
type, tax amount or total paid, and employees.

| Field | Value |
|---|---|
| Issuing county | BROWARD COUNTY |
| Receipt number | 327-123456 |
| Business opened | 2020-03-27 |
| Employees | 2 |
| Total paid | 16.50 |

Who issued it, which receipt, how long the business has operated, the count it is
assessed on, and what was paid. Total paid stands for the amount, since Tax Amount and
Total Paid are both 16.50.

**Business type was not featured,** though it was suggested. The parse places the Receipt #
line and both Business Type lines in one block, so its box would be the same region as the
receipt number's and the overlay would show two fields on one highlight. The receipt
number crop takes in the business type lines below it for the same reason; it does contain
the value.

**Business name was tried and rejected after viewing the crop.** It reads `ok` in the
range check, but its box covers only the bold "Business Name:" label, not the monospaced
value printed beside and slightly above it. A crop that shows the label without the value
would read as a mistake.

## What it surfaced

**Blank counts come back as null.** Rooms, Seats, Machines and Professionals are all
`null`, Employees is `2`, read from a cell where the 2 sits under its header.

**But blank strings come back as the string "null".** State/County/Cert/Reg and Exemption
Code are typed `["string", "null"]`, and both came back as the four-letter string
`"null"` rather than JSON null. The integer-or-null counts did not do this.

**The disclaimer is read correctly.** `is_regulatory_license` is `false`, grounded to the
three lines of the disclaimer paragraph that say so.

**The DBA line is duplicated.** The specimen prints "Generic Business LLC" once, between
the DBA: and Business Name: labels; the parse writes it under both.

**Dates read OFF only by format.** The validity period is printed "OCTOBER 1, 2019 THROUGH
SEPTEMBER 30, 2020" and normalized to ISO, so the grounding check flags it; the ranges
are right.

## Extraction

**32 leaf fields**: issuing authority, document title, receipt number and validity period;
the business (name, owner, location, phone, type, date opened, state registration,
exemption code, mailing address); the five capacity counts; the seven fee columns; the
payment stamp; and whether the document is a regulatory license. All 10 top-level fields
populate.

## Cost

**2.40 credits** at standard tier for 1 page: 1.00 to parse, 1.40 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/business-license/source/broward-county-local-business-tax-receipt-sample.pdf \
  "https://fsmsdc.org/wp-content/uploads/2023/02/8-Broward-county-Generic.pdf"
.venv/bin/python document-types/scripts/run_ade.py business-license                # 2.40 credits
.venv/bin/python document-types/scripts/run_ade.py business-license --extract-only # 1.40, schema iteration
.venv/bin/python document-types/scripts/build_images.py business-license           # free
.venv/bin/python document-types/scripts/inspect_fields.py business-license --page 1
```
