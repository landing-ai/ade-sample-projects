# Elevation certificate (flood)

Source assets for `landing.ai/document-type/elevation-certificate`.

## Sample document

`source/elevation-certificate-sarasota-fire-station.pdf`: a FEMA Elevation Certificate
(Form FF-206-FY-22-152, the 2022 edition) for a Sarasota County fire station at 1930 N.
Tamiami Trail, Nokomis, Florida. A licensed surveyor at GeoSurv, LLC certified it on
March 11, 2024. **7 pages, portrait (US Letter)**, with a text layer from the fillable
form. The pages are Sections A and B (property and flood map data), C and D (surveyed
elevations and certification), E to I (blank on this certificate), and two pages of
building photographs.

| | |
|---|---|
| Publisher | Sarasota County, Florida (floodplain records); prepared by GeoSurv, LLC |
| Source | [ftp.scgov.net/GIS/ElevCerts/…Fire Station…pdf](https://ftp.scgov.net/GIS/ElevCerts/220021_EC_Fire%20Station%20FINAL_dsigned3-11-24_22%20115132%2000%20BC.pdf) |
| Retrieved | 2026-10-13 |
| Clearance | Redacted |

The file is hosted on Sarasota County's own server. It sits in a public directory of
about 7,600 permit-linked elevation certificates that the county posts as an NFIP
Community Rating System community. The county's flood-maps page, which links to the
directory, returned 403 to scripts, so that link was not confirmed by script. The file
itself is on the county's domain and was downloaded by script.

The building owner is the county, and the building is a public fire station, so there is
no private owner data. The surveyor's printed name, licence number, title and firm
contact details are professional information on a public record, and were kept.

The following were removed with `document-types/scripts/redact.py`:

- **The surveyor's seal image.** The Section D seal box is now empty.
- **The digital signature.** This covers the signature form field and its visible
  appearance: the signature itself and the signer and timestamp line beside it.
  The Signature line is blank, and no stand-in was drawn.
- **12 pages.** These are page 1 and pages 9 to 19, which are FEMA's blank instructions
  and building diagrams. The footers still read "Page N of 19".
- **Document metadata.**

No text value was replaced. The output was verified: no image or text remains inside the
removed regions, and the metadata is empty.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it. This section is the human-readable version.

## Why this document

The collection's first **elevation certificate**, and the survey-side counterpart to the
lender-side `flood-certification` (the Standard Flood Hazard Determination):

- **A dense federal form with numbered items.** Items A1 to A9, B1 to B13 and C2.a to h
  pack label and value pairs onto shared lines.
- **Numbers that only mean something together.** The flood zone and base flood elevation
  in Section B are compared with the surveyed floor and grade elevations in Section C.
- **Checkbox answers** for the datum, the BFE source, construction status and the units.
- **Photo pages.** Captioned photographs, plus an empty fourth photo slot.

## Featured fields: the flood map lookup

All on page 1, Section B. The request named no page or fields, but suggested several in
its notes. These shipped:

| Field | Value |
|---|---|
| NFIP community ID | 125144 |
| FIRM map panel | 12115C0239 |
| Flood zone | AE |
| Base flood elevation | 10 |
| BFE source | FIRM |

Together they are the flood-rating lookup: which community, which map panel, which zone,
the base flood elevation the building is measured against, and where that elevation came
from. Two of the request's suggestions did not ship:

- **FIRM index date.** It reads OFF: it is extracted as 2016-11-04 while the page prints
  11/04/2016.
- **Panel suffix.** It grounds to the same line box as the map panel, which would have
  given a duplicate crop. BFE source has its own line.

Every box is a whole form line rather than the value alone. Flood zone and BFE share one
line, so their crops are the same image.

## What it surfaced

**The numbers ground cleanly.** The community ID, map panel, zone, BFE, latitude and
longitude, and all four surveyed elevations (13.00, 12.95, 12.40, 13.00) ground `ok`.

**Blank is not the same as zero.** C2.b, C2.c and C2.d are blank on the form, but come
back as 0.0. The first run returned -99999.0. Two rewordings of the schema description
changed only the placeholder, never to null. The 0.00 square footages in A8 and A9 are
printed on the form, so those zeros are correct.

**Checkbox booleans ground to their question.** B12, B13 and Section D's lat/long
question come back correct, but they ground to the question text and read OFF.

**The photo descriptions invent details.** The parse describes the first photo's entrance
sign as reading "St. Lucie County", a different Florida county. Zoomed in on the source,
the sign plainly reads "Sarasota County". Treat figure descriptions as captions, not as
extracted data. The photo pages also carry the form's hidden "Photo One" label, which
the first extraction counted as an extra photograph. Saying "one entry per photograph
actually inserted" in the schema fixed that.

## Extraction

**45 leaf fields**:

- the form number;
- Section A property data: owner, address, legal description, building use,
  latitude/longitude and datum, building diagram, crawlspace and garage areas;
- Section B FIRM data: community, county, panel and suffix, dates, zone, BFE with its
  source and datum, CBRS/OPA and LiMWA;
- Section C elevations, datum and units;
- Section D certifier title, company, date, comments and the lat/long attestation;
- the photo captions.

The schema leaves out the certifier's name and licence number on purpose.

## Cost

**27.60 credits** at standard tier for 7 pages: 15.30 for the first parse and extract
(about 9.1 to parse), then 6.20 and 6.10 for two extract-only schema iterations.

## Regenerating

The committed PDF is the redacted one. Re-running from the original requires removing
the signature form field on original page 3, then running `redact.py` with an empty rules
file:
`--drop-pages 1 9 10 11 12 13 14 15 16 17 18 19 --remove-images 2:440,520,570,650 --remove-marks 2:76,613,335,643`.

```bash
.venv/bin/python document-types/scripts/run_ade.py elevation-certificate                # ~15 credits
.venv/bin/python document-types/scripts/run_ade.py elevation-certificate --extract-only # ~6, schema iteration
.venv/bin/python document-types/scripts/build_images.py elevation-certificate           # free
.venv/bin/python document-types/scripts/inspect_fields.py elevation-certificate --page 1
```
