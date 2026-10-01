# Certificate of occupancy

Source assets for `landing.ai/document-type/certificate-of-occupancy`.

## Sample document

`source/certificate-of-occupancy.pdf` — a New York City Department of Buildings
Temporary Certificate of Occupancy, No. 220152652T005, for the school building at 192
East 151st Street in the Bronx, effective April 16, 2019. **4 pages, portrait (US
Letter)**, a scan with no text layer: the certificate itself, two pages of the
Permissible Use and Occupancy table, and a closing page.

| | |
|---|---|
| Publisher | NYC Department of Buildings; posted by Public Prep, the charter school network occupying the building |
| Source | [resources.finalsite.net/…/CertificateOfOccupancy.pdf](https://resources.finalsite.net/images/v1582305033/publicprep/w9uf0livvpbwada6gzn2/CertificateOfOccupancy.pdf) |
| Retrieved | 2026-10-01 |
| Clearance | Public |

Certificates of occupancy are public records, available through the Department of
Buildings' BIS system, and this one is posted on the website of the school network that
occupies the building (hosted on Finalsite, a school website platform). It names no
private individual: it describes the building, its permitted uses and capacities, and
carries the signatures of the Borough Commissioner and the Commissioner in their official
capacity. No redaction was needed.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **certificate of occupancy**, and its first municipal building
record:

- **A scan.** No text layer at all; everything is read from the image.
- **A dense ruled form.** Lettered sections A to E, with label and value pairs packed
  into cells.
- **A use table whose columns run together.** In the scan the Floor To value sits
  against Maximum persons permitted ("001 234" is floor 001, 234 persons), so the parse
  has to separate them by position.
- **A table across two pages,** with the header repeated.

## Featured fields: the certificate's status

All on page 1. The request named no page or fields, so these were chosen:

| Field | Value |
|---|---|
| Property address | 192 EAST 151ST STREET |
| CO number | 220152652T005 |
| Certificate type | Temporary |
| Effective date | 2019-04-16 |
| Expiration date | 2019-07-15 |

What a real-estate, lending or insurance reviewer checks first: which property, which
certificate, and whether it is temporary and when it lapses. This one is a 90-day
temporary certificate with 18 outstanding requirements before a final one can issue. The
expiration date's box runs down into the empty part of its cell, so it is taller than the
line it contains.

## What it surfaced

**The run-together columns are separated correctly.** All 26 rows of the use table, over
two pages, come back with the right maximum persons, live loads, occupancy groups and
descriptions.

**Blank is not the same as zero.** Three blank Maximum persons cells come back as 0, and
the blank Floor To on the cellar and roof rows is filled in from Floor From, although the
schema asks for null in both cases.

**The dates ground cleanly.** Unlike most documents in the collection, the effective and
expiration dates are printed in a form the grounding check accepts, so they are not
flagged despite being normalized to ISO dates.

**The logo is read as the issuer.** `issuing_authority` comes back as "NYC Buildings",
grounded to the logo's text, and is flagged.

## Extraction

**27 leaf fields**: issuer, number, type and dates; the property (borough, address, BIN,
block, lot, building type); the building's classification, stories, height and dwelling
units; fire protection; legal limitations; outstanding requirements; borough comments;
and every row of the use table.

## Cost

**10.30 credits** at standard tier for 4 pages: 3.80 to parse, 6.50 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/certificate-of-occupancy/source/certificate-of-occupancy.pdf \
  "https://resources.finalsite.net/images/v1582305033/publicprep/w9uf0livvpbwada6gzn2/CertificateOfOccupancy.pdf"
.venv/bin/python document-types/scripts/run_ade.py certificate-of-occupancy                # 10.30 credits
.venv/bin/python document-types/scripts/run_ade.py certificate-of-occupancy --extract-only # 6.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py certificate-of-occupancy           # free
.venv/bin/python document-types/scripts/inspect_fields.py certificate-of-occupancy --page 1
```
