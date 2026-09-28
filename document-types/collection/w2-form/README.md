# W-2 form

Source assets for `landing.ai/document-type/w2-form`.

## Sample document

`source/w2-form-2048x1388.jpg` — an example Form W-2 for tax year 2024, Copy A, filled
with test data. **1 page, a 2048×1388 landscape JPEG**: a digital image of the IRS form,
not a scan or photo, with no text layer.

| | |
|---|---|
| Publisher | Remote People (blog) |
| Source | [remotepeople.com/…/w2-form-2048x1388.avif](https://remotepeople.com/wp-content/uploads/2025/01/w2-form-2048x1388.avif) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

The Marketing Document Summary sheet lists this as the W-2 source. The form layout is the
IRS's, and every value is obvious test data: employee "John Doe", employer "Company Inc",
an employee SSN of "4453453" and an EIN of "23454535" (7 and 8 digits, neither a valid
format), and a locality named "Test".

Two caveats about clearance:

- **A blog is not a specimen publisher.** Remote People made this image to illustrate a
  post. It is not a payroll vendor or the IRS distributing a sample for reuse, which is
  the stronger kind of `public`. An IRS or payroll-vendor specimen would replace it cleanly.
- **The addresses use real road names.** Both have arbitrary house numbers. The
  employee's pairs a North Carolina road with a California ZIP, so it is not a coherent
  real address. The employer's Saratoga address could not be ruled out as matching a real
  building, and the redaction tooling works on PDF text, not images.

**The file is a JPEG, not AVIF.** The url ends in `.avif`, but the server returns
`image/jpeg`, so it is saved as `.jpg` and needed no conversion.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **image input** and first **government tax form**:

- **An image, not a PDF.** No text layer at all, so every value is read from pixels.
- **A dense boxed form.** Thirty-odd numbered boxes, each with a printed label and a
  value, in red ink.
- **Small, awkward details.** Box 12's letter codes sit beside a tiny vertical "Code"
  label, and box 13 is three checkboxes.

## Featured fields: wages and what was withheld

All on **page 1**. The request named no feature page or fields, so these were chosen:

| Field | Value |
|---|---|
| Wages (box 1) | 2,323.00 |
| Federal income tax withheld (box 2) | 232.30 |
| Social Security tax withheld (box 4) | 144.02 |
| Medicare tax withheld (box 6) | 33.68 |

They tell one story: the wages, and each tax taken from them at its rate. Federal is 10%
of $2,323.00, Social Security is 6.2% ($144.026, printed truncated to $144.02) and Medicare
is 1.45% ($33.6835, printed $33.68). No person is featured.

Each box covers the whole form box, label and value together, so a crop reads as "Social
security tax withheld 144.02" rather than a bare number.

## What it surfaced

**The box 12 codes were lost in parsing.** Boxes 12a to 12d print codes A, A, D and A,
each beside a tiny "Code" label set vertically. The parse keeps only the box number and
amount ("12a | 220.00"), so extraction correctly returns all four amounts but null for
every code. A box 12 amount without its code is not usable: the code says what the money
is.

**One value came back without a location.** Box 16, state wages ($120.00), is in the parse
as "16 State wages, tips, etc. 120.00", and extraction returns the right value, but with no
range. Every neighbouring box in the same row grounds normally.

**Checkboxes read correctly but box as a group.** All three box 13 checkboxes extract as
true, which matches the page, but they ground to the whole of box 13 and are not featured.

**Everything else grounds to its own box.** 32 of the 42 extracted values are `ok`,
including both addresses, the control number and the whole state and local row apart
from box 16. The other ten are the four missing codes, the two blank boxes (10 and 11,
correctly null), box 16 and the three checkboxes.

## Extraction

`schema.json` was written for this form, with **33 leaf fields**: tax year, employee and
employer details, control number, federal boxes 1 to 11, box 12 entries (box, code,
amount), the three box 13 checkboxes, box 14, and the state and local row. Everything
populates apart from the box 12 codes, with no warnings.

## Cost

**2.70 credits** at standard tier for 1 page: 1.10 to parse, 1.60 to extract.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py w2-form                # 2.70 credits
.venv/bin/python document-types/scripts/run_ade.py w2-form --extract-only # 1.60, schema iteration
.venv/bin/python document-types/scripts/build_images.py w2-form           # free
.venv/bin/python document-types/scripts/inspect_fields.py w2-form --page 1
```
