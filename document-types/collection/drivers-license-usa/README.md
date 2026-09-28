# Driver's license (US state)

Source assets for `landing.ai/document-type/drivers-license-usa`.

## Sample document

`source/texas-dl-specimen-2025.png` — the official specimen of Texas's 2025 driver license
design, the front of the card. **1 image, landscape (600×385)**, cropped from the Texas
Department of Public Safety's news release image.

| | |
|---|---|
| Publisher | Texas Department of Public Safety |
| Source | [dps.texas.gov/news/dps-rolls-out-new-driver-license-design](https://www.dps.texas.gov/news/dps-rolls-out-new-driver-license-design) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

DPS published this card in its August 18, 2025 release announcing the new design. Every
field is specimen data: "SAMPLE JANE", DL 12345678, 123 Sample Street, Sample City, TX
12345, with "SAMPLE" printed across the portrait. The portrait is DPS's specimen model,
not a license holder, and the director's printed signature is part of the card design.
No redaction was needed.

**The source is the DPS release, not the url in the request.** The request gave a Google
Images thumbnail (`encrypted-tbn0.gstatic.com`), which is Google's cached copy of an image
hosted elsewhere, not a publisher. Tracing it led to the DPS release, whose banner image
carries the identical card. The file here is that banner, `8.18.2025-New-DL-Design-PR.jpg`
(1080×742), cropped to the card, box (22, 300, 622, 685), so the banner's "LATEST NEWS"
headline is not parsed as part of the card. The card in the banner is slightly larger than
the thumbnail, and it is the publisher's own file.

**Resolution is the limit.** DPS publishes the card at about 600 pixels wide, the largest
version found. Everything reads correctly, but the field crops are small, around 30 pixels
tall. DPS's card designs page carries two other specimens ("SAMPLE JANICE SOFÍA" and an
under-21 "ZACHARY JOSÉ" card), both smaller still.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **identity document**, and its smallest and densest page:

- **A card, not a page.** Twenty-odd fields, each a small AAMVA field code ("4d DL",
  "16 Hgt", "18 Eyes") followed by its value, over a guilloche background with a seal,
  a ghost portrait and microtext.
- **Security features as distractions.** The second, smaller portrait, the laser-engraved
  star and the rotated ghost text all sit among the fields.
- **A team schema written for identity documents in general,** including passport fields
  that a US license does not carry.

## Featured fields: the card and its holder's description

All on the card's front. The request named no fields, so these were chosen:

| Field | Value |
|---|---|
| License number | 12345678 |
| Issuing state | Texas |
| Sex | F |
| Height | 5 feet 10 inches |
| Eye color | BRO |

The card's identity and the holder's physical description, each boxed on its code and
value ("4d DL 12345678", "16 Hgt 5'-10""). No name is featured, although the name is
specimen data. Height is returned as "5 feet 10 inches", normalized as the schema asks,
from the printed 5'-10".

## What it surfaced

**Values that are not printed are inferred.** `nationality` comes back as "American",
which the card does not print; it is a reasonable inference from a US license, but it has
no range. `issuing_country` comes back as "USA" with no range either: the card does print
a small "USA" beside TEXAS, but it is missing from the parse.

**The schema asks for fields a license does not have.** `place_of_birth` and `weight` are
not on a Texas license and correctly come back null. `place_of_birth` is required by the
schema, so extraction returns a `nonconformant_output` warning. The schema is the team's
and is used unchanged; the warning is a finding about the schema's fit to this document
type.

**The security features parse as noise, not as fields.** The rotated ghost text next to
the second portrait comes back as "orero", and the second portrait as a photo tag. Neither
leaks into any extracted field.

**Dates are normalized.** Issue, expiry and birth dates come back as ISO dates, so they
no longer match the printed 01/04/2025 style and are flagged, though they are right.

## Extraction

`schema.json` is the team's `doc42-driver-license-schema.json`, used unchanged: **15 leaf
fields** across `document_type`, `document_info` and `personal_info`. Everything printed
on the card extracts correctly.

## Cost

**1.10 credits** at standard tier for 1 image: 0.60 to parse, 0.50 to extract.

## Regenerating

```bash
# The source is a crop of the DPS release image:
curl -sSL -o /tmp/tx-pr.jpg "https://cdn.www3.dps.texas.gov/cdn/ff/BrbsHGfX2YEY0YqmGzl-YDiz0R2fk5b2BxyVlMprcIM/1755528566/public/news/2025-08/8.18.2025-New-DL-Design-PR.jpg"
.venv/bin/python -c "from PIL import Image; Image.open('/tmp/tx-pr.jpg').convert('RGB').crop((22,300,622,685)).save('document-types/collection/drivers-license-usa/source/texas-dl-specimen-2025.png')"

.venv/bin/python document-types/scripts/run_ade.py drivers-license-usa                # 1.10 credits
.venv/bin/python document-types/scripts/run_ade.py drivers-license-usa --extract-only # 0.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py drivers-license-usa           # free
.venv/bin/python document-types/scripts/inspect_fields.py drivers-license-usa --page 1
```
