# Deed

Source assets for `landing.ai/document-type/deed`.

## Sample document

`source/deed.pdf` — a California **grant deed** by which the City of Los Angeles sold a
surplus parcel at 15241 De Pauw Street, Pacific Palisades (APN 4412-028-906), to White
Picket Fence, Inc. for $1,100,000, executed September 23, 2011. **5 pages, portrait (US
Letter)**, a scan with a weak OCR layer: the deed, its Exhibit A legal description with
the surveyor's stamp, the signature cover with the departmental approvals, the execution
page signed by the Mayor and attested by the City Clerk, and the notary acknowledgment.

| | |
|---|---|
| Publisher | City of Los Angeles, Office of the City Clerk (Council File 10-2450), for the Department of General Services, Asset Management Division |
| Source | [cityclerk.lacity.org/onlinedocs/2010/10-2450_misc_9-23-11.pdf](https://cityclerk.lacity.org/onlinedocs/2010/10-2450_misc_9-23-11.pdf) |
| Retrieved | 2026-10-04 |
| Clearance | Public |

The file is the City Clerk's own copy in the Council File Management System, the
official public record of Council File 10-2450. It was downloaded by script. The filing
runs to 13 pages; only pages 1-5, the first deed, are kept. Pages 6-10 are a second deed
and 11-13 transmittal letters. Document metadata was cleared.

The parties are a city and a corporation. Everyone named appears in an official or
professional capacity: the Mayor, the City Clerk, a deputy city attorney, the General
Services general manager, the licensed surveyor who signed Exhibit A, and the notary. The
grantee's "When recorded mail to" block names a contact at the corporation's business
address; it was left in place as a corporate-capacity name. No redaction was needed.

This is the executed original filed with the City Clerk, not the recorded copy, so there
is no recorder's stamp.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **deed**, and the instrument that every title, escrow and
mortgage file turns on:

- **Prose, not a form.** The parties, the price and the conveyance are all in one
  granting sentence that runs across lines, so the parse has to pick the grantor, the
  grantee and the consideration out of running text.
- **The price is written in words and figures,** with the figures in bold mid-sentence.
- **A transfer tax declaration in the margin,** with two jurisdictions on two lines.
- **Handwritten dates.** The execution day and month, and the notary's date and
  commission expiry, are filled in by hand.
- **An exhibit.** The legal description (lot, block, tract, map book) is on a separate
  page under a surveyor's stamp.

## Featured fields: the conveyance

All on page 1. The request named no page or fields, only suggestions; all of them ground
cleanly on page 1, and the city transfer tax line is the one left out to stay within five.

| Field | Value |
|---|---|
| Grantor | THE CITY OF LOS ANGELES |
| Grantee | WHITE PICKET FENCE, INC. |
| Consideration | 1100000 |
| County transfer tax | 1210.0 |
| APN | 4412-028-906 |

What a title or lending reviewer checks first: who conveys to whom, for how much, the
transfer tax declared on it, and which parcel. The grantee is pinned to its first
occurrence, the granting clause, rather than the mail-to block.

## What it surfaced

**The granting sentence splits cleanly.** Grantor and grantee come back without their
entity descriptions ("a municipal corporation", "a California Corporation"), which land
in their own fields, and the consideration is read from the bold figures. The grantor and
consideration boxes are whole lines of the granting sentence, since that is the unit the
parse grounds to.

**Handwriting reads correctly.** The execution date (2011-09-23), the notary's
acknowledgment date and the commission expiry (2015-08-04) are all handwritten and all
right.

**Both transfer tax lines and their basis extract,** each with its jurisdiction, and
"computed on full value of the property" comes back as the basis.

**The exhibit's legal description is parsed into parts:** lot 14, block 19, tract 9300,
Book 125 pages 55 to 78 of Maps, plus the full text. Its mineral-rights exception is also
picked up as a second reservation.

**Paraphrased and multi-line fields read OFF.** The subject-to conditions are summarized
as the schema asks, and the reservation and the mail-to address span several lines, so
none of them can be featured.

## Extraction

**35 leaf fields**: deed type; grantor and grantee with entity descriptions;
consideration; each transfer tax line and its basis; APN, address and county; the legal
description in parts; reservations and conditions; recording request, mail-to and
recording information; the authorizing ordinance and council file; execution date and
signatories; and the notary acknowledgment.

## Cost

**7.90 credits** at standard tier for 5 pages: 3.80 to parse, 4.10 to extract.

## Regenerating

```bash
curl -sSL -o /tmp/deed-full.pdf "https://cityclerk.lacity.org/onlinedocs/2010/10-2450_misc_9-23-11.pdf"
# keep pages 1-5 with PyMuPDF and clear metadata (document-types/scripts/pdfmeta.py)
.venv/bin/python document-types/scripts/run_ade.py deed                # 7.90 credits
.venv/bin/python document-types/scripts/run_ade.py deed --extract-only # 4.10, schema iteration
.venv/bin/python document-types/scripts/build_images.py deed           # free
.venv/bin/python document-types/scripts/inspect_fields.py deed --page 1
```
