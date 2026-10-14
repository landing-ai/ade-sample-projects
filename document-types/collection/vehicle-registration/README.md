# Vehicle Registration

Source assets for `landing.ai/document-type/vehicle-registration`.

## Sample document

`source/flhsmv-vehicle-registration-test-print.pdf`: a Florida vehicle registration
printed by the Florida Department of Highway Safety and Motor Vehicles (FLHSMV) as a
system test. The header reads **TEST DOCUMENT**. The registrant is "SAMPLE SAMPLE, SAMMY D
SAMPLE JR" at 2900 Neil Kirkman Building, which is the agency's own Tallahassee address.
The vehicle is a blue 2005 Chevrolet four-door with the VIN `1POLKTESTPRINT123`. The card
carries the plate, decal, expiry, title number and an itemized fee block (registration
tax 68.15 plus a 3.00 county fee, for a grand total of 71.15). **1 page, landscape,
scanned.** It is a low-resolution raster (about 140 dpi as placed in the handout) with no
text layer.

| | |
|---|---|
| Publisher | FLHSMV (test print), republished by the City of Bloomington, Indiana, Parking Services |
| Source | [bloomington.in.gov/…/Sample Vehicle Registrations_0.pdf](https://bloomington.in.gov/sites/default/files/2022-07/Sample%20Vehicle%20Registrations_0.pdf), linked as "Sample of vehicle registrations" from the city's [neighborhood parking page](https://bloomington.in.gov/transportation/parking/neighborhood-parking) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted**: cropped from a larger handout, and one value replaced. See below. |

Provenance is secondary. The city's handout is a compilation, and the original FLHSMV
page this test print came from was not found.

### How the PDF was made: the crop

The city's handout has 4 pages and shows registrations from several states. Apart from
this Florida test print, the cards appear to be real people's registrations. **None of
them were ever written to this repo.** Only the Florida card was taken, like this:

1. The Florida card is a single embedded JPEG on handout page 3 (914 x 479 px), placed at
   `72,72 – 540,317.28` pt on that page.
2. The JPEG bytes were extracted with PyMuPDF and placed unchanged on a new page of
   468 x 245.28 pt, the size the image had on the handout page.
3. Everything else in the handout was dropped: pages 1, 2 and 4, the second card image
   lower on page 3, and page 3's caption text.
4. The PDF's metadata was cleared with `document-types/scripts/pdfmeta.py`.

## Redaction

Almost every value on the card is obvious test data: the "SAMPLE" registrant, the
agency's own address and a VIN that spells out "TEST PRINT". Those were left as printed.

One value was replaced:

| What | Replaced with | Count |
|---|---|---|
| DL/FEID (driver licence or federal employer ID) value: a letter and 12 digits, in a real Florida licence-number format | `S101074959542`. The letter and every digit were drawn at random by `plausible.py`, so nothing was kept from the original. | 1 |

The original is not recorded anywhere in this folder, and the rules file stays outside
the repo.

The replacement used `document-types/scripts/redact_scan.py`. Tesseract could not match
the value on this low-resolution scan, so it was placed by region with `--place` and set
in Arial Bold. The script rebuilds the page from a 300 dpi render of the edited image, so
the cropped JPEG itself is not carried into the committed PDF. Its OCR verification pass
found no original surviving, as literals or as digits. The result was also checked by eye
on 200 and 600 dpi renders, and every file in this folder was swept for the original with
`ship.py check --rules`. The stand-in renders a little lighter than the neighbouring bold
values.

## Why this document

Registrations are usually printed by a state system onto a fixed form, and this one shows
why that is harder to read than it looks:

- **A borderless grid.** Labels and values sit in loose columns with no rules, and the
  parser has to rebuild the table from position alone.
- **A value that overflows its column.** The VIN is wider than its column and runs under
  the BODY label (see below).
- **Blank fee lines.** Init. Reg., Mail Fee, Sales Tax and Voluntary Fees are printed
  with no amount, and the amounts that are printed must reconcile to the grand total.
- **Low resolution**, with a decorative logo in one corner.

`schema.json` was written for this run: **26 leaf fields**, counted from the schema. It
covers the issuing state, the registrant, the vehicle, the plate and registration
period, the itemized fees and a test-document flag. It deliberately leaves out the
DL/FEID and the CO/AGY, T# and B# office and transaction numbers.

## Featured fields: which plate, which vehicle, what was paid

All on page 1.

| Field | Value |
|---|---|
| Plate number | 429MAI |
| Title number | 100020689 |
| Model year | 2005 |
| Registration tax | 68.15 |
| Grand total | 71.15 |

The request did not name a feature page or any fields. These follow its suggestions,
except for the expiration date. That grounds `OFF`: it comes from the merged cell
"DECAL 00019601 Expires Midnight Thu 1/1/2015" and was normalised to `01/01/2015`. The
county fee shares its box with the registration tax, so only one of the two is featured.
The registrant name was avoided in favour of impersonal fields.

## Grounding and extraction on this document

- **The VIN was truncated.** The parser split the over-wide VIN across two table cells.
  `1POLKTESTPR` went into the value column, and `NT123` went into the BODY label cell. The
  `I` between them was lost. Extraction returned `1POLKTESTPR`, and the right answer
  cannot be rebuilt from the markdown. This is the one wrong value.
- **Stacked cells ground together.** The parser merged YR/MK, VIN and Plate Type into one
  cell, Reg. Tax, Init. Reg. and County Fee into another, and COLOR and TITLE into a
  third. A field in one of them boxes the whole stack, so the model year crop also takes
  in the VIN and plate type lines, and the registration tax box also covers the county
  fee.
- **Blank fees came back as 0.0, not null**, although the schema asks for null. Those
  rows ground `OFF` to empty cells.
- **Normalised dates ground `OFF`.** `11/5/2013` was returned as `11/05/2013`, and so on.
  The values are right, but the text does not match character for character.
- `build_images.py` warned that OCR could not read `71.15` inside its box. The crop does
  contain it.
- The fees reconcile in the extraction: 68.15 + 3.00 = 71.15.

## Credits

2.20 credits at standard tier, through the jobs API (parse with `dpt-3-pro-latest`,
which ran as `dpt-3-pro-20260710`, plus extract).

## Regenerate

```bash
# In a scratch directory outside the repo
curl -o handout.pdf "https://bloomington.in.gov/sites/default/files/2022-07/Sample%20Vehicle%20Registrations_0.pdf"
# PyMuPDF: take page 3's first embedded image (the Florida card, bbox 72,72,540,317.28),
# insert its JPEG bytes unchanged on a new 468 x 245.28 pt page, pdfmeta.clear(), save
# as cropped.pdf

# Replace the DL/FEID (rules.json outside the repo)
.venv/bin/python document-types/scripts/redact_scan.py cropped.pdf \
    flhsmv-vehicle-registration-test-print.pdf --rules <outside-the-repo>/rules.json \
    --font "/System/Library/Fonts/Supplemental/Arial Bold.ttf" \
    --place "1:39.8,90.5,88.3,95.9=S101074959542"

.venv/bin/python document-types/scripts/run_ade.py vehicle-registration
.venv/bin/python document-types/scripts/build_images.py vehicle-registration
```
