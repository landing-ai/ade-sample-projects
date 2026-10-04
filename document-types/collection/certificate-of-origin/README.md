# Certificate of origin

Source assets for `landing.ai/document-type/certificate-of-origin`.

## Sample document

`source/certificate-of-origin.pdf` — a preferential **Certificate of Origin, Form L**,
issued in Guangzhou on 3 November 2011 under the China–Costa Rica Free Trade Agreement
for two lines of footwear shipped from Xiamen to San José. **1 page, portrait**, a single
150 dpi colour scan of the issued certificate on its pale-blue security paper: typed
values, the exporter's red company chop, the certifying authority's red seal, two
handwritten signatures and a barcode.

| | |
|---|---|
| Publisher | Cargo From China (freight forwarder), as its "Form L sample" |
| Source | [cargofromchina.com/…/Form-L-China-Costa-Rica.jpg](https://cargofromchina.com/wp-content/uploads/Form-L-China-Costa-Rica.jpg) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

Cargo From China publishes the image on its
[China Certificate of Origin](https://cargofromchina.com/certificate-of-origin/) page as
the "Form L sample" for Costa Rica, alongside samples of the other Chinese FTA forms. The
JPEG was wrapped, unaltered, in a one-page PDF at its native resolution, with no metadata.

The image carries a `jdol.com.cn` watermark in its corner, so the forwarder republished
it from an earlier Chinese source; the forwarder's page is the provenance of record. It
is an issued certificate, not a blank or a specimen. Every party it names (exporter,
producer, importer and the shipping marks) is a company. The two handwritten signatures,
the exporter's signatory in box 13 and the certifying official in box 14, carry no printed
names. It is kept as published by decision of the operator.

## Why this document

The collection's first **certificate of origin**, and a trade document that is hard in
ways the financial forms are not:

- **Values typed across the printed captions.** The typewriter values in boxes 1–3 start
  on the same line as the caption and overprint it.
- **A watermark under everything.** The certificate's security paper carries faint
  Chinese text across the whole page.
- **Two red stamps over printed text,** one of them crossing the certifying body's date
  line.
- **A goods table** with a merged marks column, quoted origin codes ("WO") and HS codes
  printed with a space after the dot.

## Featured fields: one shipment line

All on page 1. The request named no fields.

| Field | Value |
|---|---|
| Vessel and voyage | XIANG XING V. BN02W |
| Port of loading | XIAMEN, CHINA |
| Goods (item 1) | FOOTWEAR |
| HS code (item 1) | 6403.99 |
| Origin criterion (item 1) | WO |

What a customs broker checks on a preferential certificate: the shipment it covers, what
the goods are, their tariff classification, and the origin criterion that qualifies them
for the agreement's rate ("WO", wholly obtained). The HS code is read as 6403.99 from a
scan that prints "6403. 99".

**Two fields were tried and rejected after viewing the overlay.** The certificate number
and the invoice value both read `ok`, but the certificate number's box covers the whole
top-right header cell, title and "Issued in" line included, and the invoice value's box
covers the empty lower part of box 12, only grazing the value. Neither crop would read
as pointing at its value.

`build_images.py` warns that OCR could not read the three goods-line values inside their
boxes. Those crops were opened: each box sits on its value, and tesseract fails on the
typewriter face over the watermark.

## What it surfaced

**The invoice date loses its last digit.** Box 12's "NOV. 03, 2011" runs to the right edge
of the scan, and the parse transcribes it as "NOV. 03, 201". The other three instances of
the same date on the page are read in full.

**One quantity is missed.** Item 1 and item 2 both read "216PRS" in box 11. Item 2's is
extracted; item 1's comes back as an empty string, its range pointing at the column
caption.

**The certifying body's phone and fax come back empty,** although both are printed in box
14 under the authority's stamp.

**Empty remarks come back as the string "null".** Box 5 holds only asterisks; the schema
allows null, and the extraction returns the four-letter string instead.

**Box 4's route line is merged with the port of discharge.** The scan overprints "FROM
XIAMEN, CHINA TO SAN JOSE, COSTA RICA BY SEA" on the "Port of discharge" caption. The
port of discharge itself reads correctly; the route grounds `OFF`.

**Stamps and signatures are recognised, not located.** The four stamp and signature
booleans are all `true` and right, but they ground to the parse's `[STAMPED]` and
`[SIGNED]` labels rather than to the marks themselves.

## Extraction

**42 leaf fields**: certificate number, form title and issuing country; exporter (with
"on behalf of"), producer and importer; transport (date, vessel, ports, route); remarks;
the goods lines (item, marks, description, HS code, origin criterion, quantity); the
packages statement; the invoice (number, date, trade term, value); the exporter's
declaration and the certification (place and date, stamp, signature, contact details);
the barcode number and the form serial. All 15 top-level fields populate.

## Cost

**3.90 credits** at standard tier for 1 page: 1.40 to parse, 2.50 to extract.

## Regenerating

```bash
curl -sSL -o /tmp/form-l.jpg "https://cargofromchina.com/wp-content/uploads/Form-L-China-Costa-Rica.jpg"
# wrap the JPEG in a one-page PDF at 150 dpi (1272x1752 px -> 610.56x840.96 pt) with PyMuPDF,
# clearing metadata, as source/certificate-of-origin.pdf
.venv/bin/python document-types/scripts/run_ade.py certificate-of-origin                # 3.90 credits
.venv/bin/python document-types/scripts/run_ade.py certificate-of-origin --extract-only # 2.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py certificate-of-origin           # free
.venv/bin/python document-types/scripts/inspect_fields.py certificate-of-origin --page 1
```
