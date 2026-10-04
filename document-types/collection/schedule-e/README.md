# Schedule E

Source assets for `landing.ai/document-type/schedule-e`.

## Sample document

`source/ScheduleE.Form.2020.pdf`: a completed tax-year 2020 IRS Schedule E (Form 1040),
Supplemental Income and Loss, page 1 (Part I, rental real estate and royalties).
**1 page, portrait.** A single-family rental with a full year of fair rental days, rents,
mortgage interest, taxes, insurance, repairs, HOA dues and depreciation.

| | |
|---|---|
| Publisher | Enact Mortgage Insurance (formerly Genworth Mortgage Insurance) |
| Source | [content.enactmi.com/documents/training/course/ScheduleE.Form.2020.pdf](https://content.enactmi.com/documents/training/course/ScheduleE.Form.2020.pdf) |
| Retrieved | 2026-10-03, downloaded manually by the operator |
| Clearance | **Public** |

## Provenance and clearance

A training handout from a mortgage insurer's lender course. Enact's own deck
*Calculating Rental Income* titles its page 35 "Schedule E Handout", matching this file
on Enact's course-materials host, and the PDF metadata names Genworth Mortgage Insurance,
Enact's former name, as author.

The host answers scripted downloads with a bot check, so the operator downloaded the
file by hand on 2026-10-03. The URL above is still the source of record. The committed
file is byte-for-byte what was downloaded, metadata included.

It is a specimen: the filer is "Larry Landlord", the SSN is printed as `XXX-XX-XXXX`, and
the property is "8 Renters Way", a teaching address. No redaction was needed.

## Why this document

The collection already has a Schedule C (sole proprietorship) and a Form 1040. Schedule E
is the form mortgage underwriters actually work from to qualify rental income, and this
copy comes from exactly that setting. Its layout is unlike Schedule C: the amounts sit in
property columns A to C beside a shared list of line labels, so grounding has to land on
the right column as well as the right row, and four of the per-property amounts are
repeated in the line 23 to 26 summary block below.

The amounts are printed in the tax-software style with a trailing period (`73,900.`).

## Schema

`schema.json` covers page 1 in full: tax year, filer, the 1099 questions on lines A and B,
an array of properties (address, property type, rental and personal days, QJV, rents,
royalties, all 15 expense lines, total expenses, net income or loss, deductible loss) and
the summary lines 23a to 26. **40 leaf fields.** All six top-level fields populate.

## Featured fields: the rental-income calculation

All on page 1, all in property column A:

| Field | Value |
|---|---|
| Rents received (line 3) | 73,900 |
| Mortgage interest (line 12) | 19,332 |
| Taxes (line 16) | 10,344 |
| Depreciation (line 18) | 3,661 |
| Net rental income (line 21) | 31,185 |

These are the lines an underwriter reads: gross rents, the large expenses, depreciation
to add back, and the bottom line. They were the request's suggestions and all five ground
`ok`. No person is featured.

## Grounding

Clean, and worth recording because of the repeated values. 73,900, 19,332, 3,661 and
31,185 each appear twice or three times on the page (column A and lines 23a, 23c, 23d,
24 and 26), and every per-property path grounds to its own column-A cell while every
`totals` path grounds to its own summary cell. Nothing was crossed. The trailing-period
amounts matched without trouble.

Weaker spots, none featured:

- Blank amount lines extract as `0` rather than `null`, though the schema asks for null.
  This is the same behaviour seen on Schedule C and Form 1040.
- Line B (filed required 1099s) extracts as `false` although neither box is checked; the
  parse reads both correctly as `[ ]`. Line A (`No` checked) extracts correctly.
- Lines A and B ground to the whole Part I header block rather than their checkbox rows.
- The QJV checkbox grounds correctly to its empty box.

## Cost

**4.60 credits** at standard tier: 1 page, parse plus extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py schedule-e
.venv/bin/python document-types/scripts/build_images.py schedule-e
.venv/bin/python document-types/scripts/inspect_fields.py schedule-e --page 1
```
