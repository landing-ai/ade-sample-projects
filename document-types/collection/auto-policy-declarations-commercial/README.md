# Auto Policy Declarations (Commercial)

Source assets for `landing.ai/document-type/auto-policy-declarations-commercial`.

## Sample document

`source/owners-insurance-commercial-auto-declarations-redacted.pdf` — the Automobile
Policy Declarations of an Owners Insurance Company (Auto-Owners Insurance Group)
commercial auto renewal for a small excavation contractor, term 12-29-2015 to
12-29-2016. **6 pages, portrait.** Born-digital, with a text layer.

| | |
|---|---|
| Publisher | Owners Insurance Company (Auto-Owners Insurance Group) |
| Source | [scribd.com/doc/297561971](https://www.scribd.com/doc/297561971/commercial-auto-policy-12-29-2015-5-3) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted** — see below |

## This document was redacted before it entered the repo

Scribd is a user-upload site, so the account that posted this file is not its publisher.
It is a real policy for a real business, and it was treated as a private record.

**Pages kept.** The original file is 58 pages. Only the six declarations pages (original
pages 2–7) were kept:

- Page 1, the agency's cover letter, was dropped. It carried the policy number and an
  online-account enrollment code.
- Page 8, the Scheduled Drivers List, was dropped. It lists eight individual drivers
  with their full names and dates of birth, and adds nothing the vehicle schedule does
  not already show.
- Pages 9–58 are the policy form, endorsements and the insurer's signature page. They
  are not the declarations and were dropped.

**Values replaced** on the six kept pages:

| What | Occurrences | Replaced with |
|---|---|---|
| Insured business name | 6 | `SAMPLE EXCAVATION INC` |
| Insured mailing address (PO box, city, ZIP+4) | 3 | `PO BOX 10`, `ANYTOWN`, `84790-1394` |
| Agency name | 6 | `EXAMPLE AGENCY` |
| Agency code | 6 | `32-2356-69` |
| Agency phone | 1 | `(435) 555-0176` |
| Policy number | 6 | `95-342-160-75` |
| Company-use account number | 6 | `46-31-UT-3494` |
| VINs, one per vehicle | 10 | random VINs of the same shape |
| Individual named in care of a lienholder | 2 | `PAT EXAMPLE` |

Names and the address are obviously fake. Numeric identifiers are randomly drawn by
`document-types/scripts/plausible.py`, so the page still reads as a real policy rather
than a page of zeros. Kept as printed: the insurer and its address, the two lienholder
institutions, the territory county, the vehicle descriptions, and every limit and
premium.

Done with `document-types/scripts/redact.py`, which removes the underlying text rather
than drawing a box over it, and clears the PDF metadata. It re-extracts afterwards and
verified that no original string survives; `ship.py check` swept every file in this
folder, on literals and on runs of digits. The rules file stays outside the repo.

## Why this document

The collection already has `auto-policy-declarations-page`: one page, a coverage
schedule keyed by covered-auto symbols, and no vehicles listed. This is the other shape
of commercial auto declarations, the **fleet schedule**. Each of ten vehicles and
trailers has its own block, with a VIN, territory, coverage rows, limits, premiums, a
total, interested parties and rating details, spread over five pages. Page 6 rolls them
up into totals by coverage, a paid-in-full discount and the term premium.

It tests a repeating structure across page breaks, and arrays nested two deep
(vehicles → coverages). The numbers also check themselves: the eight coverage totals sum
to the $11,558.40 policy premium, which is the ten vehicle totals ($11,508.15) plus a
$50.25 designated-insured endorsement.

## Featured fields

Page 1, one scheduled vehicle and what it costs:

| Field | Label | Value |
|---|---|---|
| `policy_number` | Policy number | 95-342-160-75 |
| `vehicles[0].description` | Scheduled vehicle | 2001 DODG RAM 3500 ST/SLT/SPT |
| `vehicles[0].coverages[0].limit` | Combined liability limit | $1Million ea occ |
| `vehicles[0].coverages[0].premium` | Combined liability premium | 718.69 |
| `vehicles[0].total_premium` | Vehicle total premium | 860.51 |

Together they read as one row of the fleet schedule. Page 6, the premium totals, was the
alternative; every field there grounds cleanly too.

## Grounding

Clean throughout. All ten vehicles, all 58 coverage rows and all eight coverage totals
extract correctly, and every printed value grounds to its own line, across the page
breaks.

- Vehicle description and VIN are one parse block, so both crops show the same two
  lines.
- Blanks come back as empty strings rather than JSON null, despite the schema allowing
  null. That applies to `lienholder` where Interested Parties reads `None`, and to the
  limit of every Terrorism Coverage row, which has no limit printed. Twice the value was
  the literal string `null`. The two real lienholders extract in full.
- The two trailers' Terrorism Coverage premiums print as `.61` and extract as 0.61;
  `inspect_fields.py` marks them OFF only because the formats differ.
- The insured's address is printed on two lines and grounds as two ranges, one per line.
- `insurer` comes back as the abbreviated running header `OWNERS INS. CO.` from a later
  page, not the logo and `INSURANCE COMPANY` line on page 1.
- `gross_vehicle_weight` is null for the trailers, which state none.

The schema has 25 leaf fields.

## Credits

19.20 credits at the standard tier (parse and extract, 6 pages).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py auto-policy-declarations-commercial
.venv/bin/python document-types/scripts/build_images.py auto-policy-declarations-commercial
```

`run_ade.py --extract-only` re-runs extraction against the committed parse when only
`schema.json` changes.
