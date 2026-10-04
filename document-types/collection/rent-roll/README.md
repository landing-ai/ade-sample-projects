# Rent Roll

Source assets for `landing.ai/document-type/rent-roll`.

## Sample document

The rent roll for Lund Pointe Apartments, a 25-unit multifamily property in Port Orchard,
Washington, taken from the offering memorandum the listing broker, Neil Walter Company,
published to market the property in 2016.

| | |
|---|---|
| File | `source/lund-pointe-rent-roll.pdf` |
| Pages | 1 (page 11 of the 17-page offering memorandum) |
| Orientation | Landscape |
| Layer | Native text, no scanning |

One table: 25 unit rows (unit, bed/bath, status, square feet, total rent, other charges)
and a totals row, under a header line giving the property name, address range, unit list,
city, state and ZIP.

## Provenance

| | |
|---|---|
| Publisher | Neil Walter Company Commercial Real Estate |
| Source URL | https://www.neilwalter.com/wp-content/uploads/2016/02/Lund-PointeApts_OfferingMemorandum.pdf |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | `public` |

The broker publishes the offering memorandum on its own website for prospective buyers.
Only the rent roll page was kept, split out with PyMuPDF. The page carries no personal
data: no tenant names, lease dates, deposits or contact details. Nothing was redacted.
The source PDF's document metadata named the preparer's user account, so it was cleared
when the page was split out, and the committed file carries none.

## Why this document

It is a clean, complete rent roll with a totals row that reconciles: the 25 unit rents sum
to the printed $22,280 and the unit areas to the printed 23,760 square feet. A rent roll
is one long, repetitive table where every row looks like its neighbours, which tests
whether extraction keeps 25 rows aligned without dropping, duplicating or shifting one.
It also splits a combined `3/2.00` cell into bedrooms and bathrooms.

It is thin as rent rolls go: there are no tenant names, lease start and end dates,
deposits or market rents, so the schema does not ask for them.

The `Other Charges` column repeats the `Total` column on every row, which is an error in
the source. The schema extracts it as printed and it is not featured.

## Featured fields

All on page 1, the totals row, so the overlay reads as one summary of the property:

| Field | Label | Value |
|---|---|---|
| `totals.total_units` | Total units | 25 |
| `totals.occupancy_percent` | Occupancy | 100 |
| `totals.total_square_feet` | Total square feet | 23760 |
| `totals.total_monthly_rent` | Total monthly rent | 22280 |

The request file named no fields. Its research notes also suggested unit A-101's rent
($1,215); that was dropped for the reason under Grounding.

## Extraction

`schema.json` has 16 leaf fields: five for the property, seven per unit and four for the
totals row. The run returned 184 leaf values, including all 25 units.

Every one of the 175 unit cells was checked against the PDF's text layer and all match,
including the bedroom and bathroom split. The property header was split correctly into
street address range, city, state and ZIP, with the unit list left out.

## Grounding

Every value is grounded, on the right page and in the right cell. Where two columns hold
the same number, as `Total` and `Other Charges` do on every row, the ranges point at
different cells, so the model is tracking columns rather than matching the first
occurrence of a value.

`inspect_fields.py` nonetheless marks the 75 per-unit square-foot and dollar values `OFF`.
Extraction returned them as floats (`1215.0`) and the matcher does not equate that with
the boxed `$1,215`. The boxed cells are the right ones; the flag is a formatting mismatch.
The totals came back as integers and match. Only rows marked `ok` are featured, which is
why A-101's rent is not.

## Credits

**5.60 credits** at standard tier: one-page parse and extraction. Most of it is the
extraction of the 25-row array.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py rent-roll      # spends credits
.venv/bin/python document-types/scripts/build_images.py rent-roll # free
```
