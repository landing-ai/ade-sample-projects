# Vehicle Schedule

Source assets for `landing.ai/document-type/vehicle-schedule`.

## Sample document

`source/louisa-county-fire-ems-vehicle-schedule-2021.pdf`: Addendum 1 to Louisa County,
Virginia's RFP ES-21-04, *Property and Casualty Insurance Services for Louisa County Fire
and EMS* (April 29, 2021). **4 pages, portrait.** Pages 1 and 2 are the addendum's
questions and answers, including a current-premium-by-coverage table on page 1. Pages 3
and 4 are the attached vehicle schedule "as of April 2021": 86 fire and EMS units in a
nine-column table (Veh #, Year, Make, Model, Body Type, VIN, Agreed Value, Unique Id,
Loc), grouped under twelve section headers, one per fire company, rescue squad or the
county itself.

| | |
|---|---|
| Publisher | County of Louisa, Virginia, Finance Department |
| Source | [louisacounty.gov](https://louisacounty.gov/DocumentCenter/View/6988/RFP-ES-21-04-Property-and-Casualty-Addendum-1?bidId=) |
| Retrieved | 2026-10-25 (downloaded by script) |
| Clearance | **Public** |

The county published this addendum on its own website so that insurers bidding on the
fire and EMS programme could price the fleet. A vehicle schedule is exactly what an
auto liability and physical damage quote is priced from, so this is a public record of
a real one rather than a mock-up.

**No page content was changed.** The schedule lists government fleet vehicles, VINs and
station identifiers, and names no private individual. The PDF's document metadata
carried the Word user name of the county employee who prepared it; it was cleared
before the file entered the repo, and the source PDF now carries no metadata.

It is an entity-prepared fleet list, not an ACORD 129 vehicle schedule form. The
operator accepted that when choosing this sample: most commercial fleets submit their
schedule as a spreadsheet export just like this one.

## Why this document

It tests a dense, ruled table of about 55 rows per page that is split into sections by
centred header rows, with one section (Zion Crossroads Vol. Fire Dept.) running across
the page break. The cells are as irregular as real fleet lists get: models left blank,
vehicle numbers blank or starred, a VIN with an embedded space, a value printed as
`280 ,000`, text instead of amounts in the value column ("Portable Equip", "Inland
Marine"), and a boat and outboard motor whose values are written into the VIN column.

## Schema

`schema.json` resolves to **20 leaf fields**: nine about the submission (entity,
department, RFP and addendum numbers, date, title, schedule as-of date, and the current
auto liability and auto physical damage premiums from page 1), the section name, and ten
per vehicle under each section. Agreed value is a number, with a separate
`agreed_value_note` that takes the cell's text when it is not an amount.

Extraction returned all twelve sections in order with the right number of units in each
(86 in total), kept the Zion Crossroads section as one entry across the page break, kept
the asterisks on vehicle numbers, and put "Portable Equip" and "Inland Marine" in the note
with a null value. Blank model cells came back inconsistently, sometimes as `""` and
sometimes as null; the schema asks for null.

## Featured fields: one fleet line

All on page 3, following Veh # 1, the first unit under the first section header:

| Field | Value |
|---|---|
| Department section | Louisa Vol. Fire Dept. |
| Body type | Pumper |
| VIN | 4PICV01E5BA011783 |
| Agreed value | 580,000 |
| Station ID | FS1 |

The request suggested page 3, the first section header, and Veh # 1's year, make, body
type, VIN, agreed value, unique ID and location. All of them grounded `ok` on page 3. A
page features at most five fields, so year, make and the Loc column were left out; the
station ID says where the unit is garaged just as the Loc column does.

The PDF's text layer spells this VIN with the letter `l` where the printed glyph reads as
`I`; ADE returns `I`, which matches what is on the page.

## Grounding

Of 881 extracted leaf values, 722 ground `ok`. The 123 `SYNTH` values are all nulls for
blank cells, which have nothing to point at. Of the 37 `OFF` values, 28 are blank model
cells returned as `""`.

The other nine are worth knowing about:

- **Seven cells grounded one column or one row adrift.** On page 3, Veh # 73's number
  and year are swapped (`73` grounded to `2008` and back). On page 4, the makes of three
  units ground to the year cell beside them and one model grounds to the make; Veh # 56's
  body type grounds to its model, `E-450`. The values themselves are all correct.
- **Two are formatting.** `34*` grounds to the parse's `34<sup>*`, and the addendum date
  `2021-04-29` grounds to "April 29, 2021".

The values in the overlay row are clean, and the section header grounds as a full-width
row of its own, which is what lets the overlay show the unit and the company it belongs
to together.

`build_images.py` warned that OCR could not read `Pumper` and `FS1` inside their boxes.
Both crops were opened and both boxes sit on the right cell; the text is small at this
table density.

## Credits

At standard tier: **28.20** for the parse and extraction. No extraction reruns.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py vehicle-schedule                 # parse + extract
.venv/bin/python document-types/scripts/run_ade.py vehicle-schedule --extract-only  # extract only
.venv/bin/python document-types/scripts/inspect_fields.py vehicle-schedule --page 3
.venv/bin/python document-types/scripts/build_images.py vehicle-schedule
```
