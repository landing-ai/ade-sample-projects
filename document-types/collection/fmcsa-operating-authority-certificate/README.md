# FMCSA Operating Authority Certificate

Source assets for `landing.ai/document-type/fmcsa-operating-authority-certificate`.

## Sample document

`source/fmcsa-authority-certificates-2023-02-16-excerpt.pdf`: twenty operating authority
documents issued by the Federal Motor Carrier Safety Administration on one day, each a
one-page certificate or permit granting a motor carrier interstate operating authority
under an MC docket number and printing its U.S. DOT number. **20 pages, portrait
(612×792)**, with a text layer throughout (Oracle Reports output), plus the USDOT logo
and the signing official's signature as images on every page.

| | |
|---|---|
| Publisher | U.S. Department of Transportation, Federal Motor Carrier Safety Administration, Office of Registration |
| Source | [li-public.fmcsa.dot.gov/…/LI_CPL20230216.PDF](https://li-public.fmcsa.dot.gov/lihtml/rptspdf/LI_CPL20230216.PDF) |
| Title | FMCSA Licensing & Insurance daily report of issued operating authority documents, service date February 16, 2023 |
| Retrieved | 2026-10-25 |
| Clearance | Public |

FMCSA posts each day's batch of issued authority documents in its own Licensing &
Insurance public report folder, so the URL is the publisher. It is a U.S. federal
government work. Downloaded by script.

The source is 768 pages, alternating an authority document with a mailing-envelope page.
This folder keeps 20 of them, the odd-numbered source pages 33 to 71, split out with
PyMuPDF. The even-numbered pages in that range were dropped because they are envelope
pages printing each carrier's business street address.

Every kept page was checked by eye for personal data. Each holder is a business (an LLC,
an Inc., or a trade name), and none is a sole proprietor trading under a personal name.
The only individual named is the FMCSA Division Chief who signs every document in an
official capacity; his printed name and image signature are kept as published. Nothing
was redacted. The document metadata was cleared when the pages were split out.

The carriers are real companies, and their authority status may have changed since
February 2023. These pages show what was issued that day, not current status.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

A batch of near-identical one-page government documents, which is how these arrive in
practice: a broker or insurer onboarding carriers sees many of them. It tests

- **One record per page, many pages.** Extraction has to return 20 separate records in
  order, not merge or skip any.
- **Small variations inside a fixed template.** Among the 20 are a household-goods
  certificate (page 5, form code CHO, with extra tariff and arbitration requirements), a
  contract-carrier permit (page 8, with a continuing-agreement condition), three holders
  with a D/B/A line that pushes the city down a line (pages 13, 14 and 18), and a Quebec
  holder (page 18).
- **Values set apart by layout rather than labels.** The service date sits alone at top
  right; the docket number, DOT number, holder and city are an unlabelled centred stack;
  the authority granted is bold text inside a sentence.

## Featured fields

Page 1, a common-carrier certificate, the document type in the title:

| Label | Value |
|---|---|
| Service date | February 16, 2023 |
| MC docket number | MC-1179808-C |
| U.S. DOT number | 3537401 |
| Carrier name | PINK SPARROW SCENIC LLC |
| Authority granted | common carrier |

Together they read as one complete certificate: when it was served, the two federal
identifiers, who holds it and what it authorizes. City and state ground correctly too,
but share the holder's address line, so they were left off to keep the overlay
uncluttered. The carrier name is a business, not an individual.

## Extraction

`schema.json` resolves to **15 leaf fields**: the issuing agency and office, and an
`authority_documents` array with 13 fields per document (service date, document type,
docket number, DOT number, holder name, D/B/A, city, state, carrier type, commodity scope,
service condition, signing official, form code).

**Every one of the 20 documents extracted correctly.** All docket numbers, DOT numbers,
holder names, cities and states match the PDF's text layer, including the household-goods
scope on page 5, the contract-carrier type and its condition on page 8, the three D/B/A
names, and the cities that sit a line lower on those pages.

**Absent optional fields come back inconsistently.** Where a document has no D/B/A line
or no extra service condition, `dba_name` and `service_condition` came back as an empty
string, the string `"null"`, the string `"none"`, or a real null on different pages,
although the schema asks for null. Those empty values ground OFF onto nearby text, which
accounts for 40 of the 44 rows `inspect_fields.py` does not mark `ok`.

The Quebec holder's line reads `LAVAL, QC, CA`; extraction returned the state as `QC`
and dropped the country, which the schema has no field for.

## Grounding

Clean. Every featured value grounds to its own line, and the crops were checked by eye.
`carrier_type` grounds to the first line of the sentence that contains it, which is the
right place: the bold phrase sits at the end of that line. A few `commodity_scope` values
ground to a neighbouring block where the bold phrase wraps across lines, and one
`signing_official` carries a second range on the paragraph above.

## Credits

30.30 credits at the standard tier (parse and extract), DPT-3 Pro.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py fmcsa-operating-authority-certificate
.venv/bin/python document-types/scripts/build_images.py fmcsa-operating-authority-certificate
.venv/bin/python document-types/scripts/inspect_fields.py fmcsa-operating-authority-certificate --page 1
```

To rebuild the excerpt from the source, keep source pages 33, 35, … 71 (0-indexed 32,
34, … 70) with PyMuPDF and clear the metadata.
