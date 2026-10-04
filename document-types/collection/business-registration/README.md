# Business registration

Source assets for `landing.ai/document-type/business-registration`.

## Sample document

`source/business-registration.pdf` — an Idaho **Certificate of Organization, Limited
Liability Company**, filed with the Idaho Secretary of State in April 2018. **1 page,
portrait**, a single raster scan with no text layer: the state's preprinted form filled in
by typewriter-style type, two handwritten signatures, the Secretary of State's
"FILED EFFECTIVE" rubber stamp, the cashier's register imprint, and a handwritten filing
number.

| | |
|---|---|
| Publisher | Idaho Secretary of State |
| Source | [sosbiz.idaho.gov/api/report/GetImageByNum/…](https://sosbiz.idaho.gov/api/report/GetImageByNum/097182066095252009134168051025113046056061167000) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

The Secretary of State serves this filing from its public business-entity search. The
scanned image is byte-identical to the copy the marketing team kept in the ADE Documents
shared drive (doc36), so the drive copy and the public record are the same document.

**Used as published, unredacted, by explicit decision of the operator.** The filing
carries what Idaho's public register carries: the names of the LLC's two organizers (who
are also its governors, one of them its registered agent), the street address they gave,
a PO box, and their handwritten signatures. This collection's usual practice for public
records that name private people has been to redact them (the Multnomah County
foreclosure pages); this document follows the FINRA arbitration award instead, where the
operator chose to keep the record as published. None of the individuals, their address or
their signatures is featured. The PDF metadata holds only the state's imaging software
(GdPicture) and a timestamp.

## Why this document

The collection's first **state business-entity filing**, and a scan with four distinct
kinds of writing on one page:

- **Typed values on a preprinted form,** each on a rule under its numbered question.
- **A rubber stamp** ("FILED EFFECTIVE … SECRETARY OF STATE, STATE OF IDAHO"), faint and
  partly broken.
- **A cashier's register imprint** in a dot-matrix face: date and time, check, batch and
  fee lines.
- **Handwriting:** two signatures and the filing number written in the state-use box.

## Featured fields: what the state registered

All on page 1. The request named no fields.

| Field | Value |
|---|---|
| Business name | CAPITAL ASSET REALTY, LLC |
| Entity type | Limited Liability Company |
| Filing state (stamp) | Idaho |
| Filing number | W199421 |

What was formed, as what kind of entity, under which state's seal, and the number the state
gave it. The state is grounded to the rubber stamp, and the filing number to the
handwriting in the state-use box, so the overlay shows the model reading both of the
page's least legible elements.

`build_images.py` warns that OCR could not read the stamp or the filing number inside their
boxes. Both crops were opened: each box sits squarely on its value, and the warning comes
from tesseract failing on a faded stamp and on handwriting, which is the point of
featuring them.

**Dates could not be featured.** Every date on the page reads `OFF`: the stamp's
"2018 APR-9 PM 2:51" and the register's "04/09/2018 05:00" both extract correctly but are
normalised to ISO (2018-04-09), so the printed text no longer contains the value.

## What it surfaced

**The team's schema does not fit this form exactly.** The schema is the team's existing
`business_registration_schema.json`, used unchanged. It makes every top-level field
required, including `contact` (email, fax, phone), which a Certificate of Organization does
not carry. Extraction returned null for `contact.email` with a `nonconformant_output`
warning. That is a finding about the schema, recorded here rather than patched.

**Date of incorporation is null.** The schema distinguishes the incorporation date from the
filing date. An LLC organised in Idaho exists from filing, and the form prints only the
filing stamp, so the model filled `filing_date` and left `date_of_incorporation` null
rather than copying one into the other.

**A typo is extracted as printed.** The registered agent's ZIP code is written with six
digits on the form. The extraction returns the six digits rather than correcting them to
the five-digit ZIP printed elsewhere on the page.

**The stamp is read as the Secretary of State's signature.**
`secretary_of_state_signature_present` comes back `true`, grounded to the stamp; there is no
signature by the Secretary of State on the page, only the office's stamp.

**Inferred fields read OFF by design.** `document_type` (`domestic_registration`),
`country_of_jurisdiction` (`USA`) and `registered_agent.type` (`Individual`) are not printed
on the page in those words, so their ranges point at the text that supports them.

## Extraction

**36 leaf fields** in the schema: document type, business name and type, jurisdiction,
incorporation and filing dates, filing number, the state's filing details, managers, the
principal office address, contact details, the signer and the registered agent. 13 of 14
top-level fields populate; `contact` is entirely null.

## Cost

**2.80 credits** at standard tier for 1 page: 1.00 to parse, 1.80 to extract.

## Regenerating

```bash
curl -sSL -o document-types/collection/business-registration/source/business-registration.pdf \
  "https://sosbiz.idaho.gov/api/report/GetImageByNum/097182066095252009134168051025113046056061167000"
.venv/bin/python document-types/scripts/run_ade.py business-registration                # 2.80 credits
.venv/bin/python document-types/scripts/run_ade.py business-registration --extract-only # 1.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py business-registration           # free
.venv/bin/python document-types/scripts/inspect_fields.py business-registration --page 1
```
