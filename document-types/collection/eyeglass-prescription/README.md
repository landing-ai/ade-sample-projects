# Eyeglass Prescription

A filled-in eyeglass prescription: a printed form with handwritten values. Sphere,
cylinder and axis for each eye, at distance and near, a pupillary distance per row, then
the patient's name and age, the date and the prescriber's signature. One landscape image,
700 × 527.

| | |
|---|---|
| Publisher | Perfect Eyeglasses Guide (perfect-eyeglasses-guide.com) |
| Published on | [Eyeglass Prescription – Understand All the Parameters](https://www.perfect-eyeglasses-guide.com/eyeglass-prescription.html) |
| Source URL | https://www.perfect-eyeglasses-guide.com/images/xglasses-prescription.jpg.pagespeed.ic.nPjIzjC8WB.webp |
| File | The same 700 × 527 image, from the publisher's JPEG at `/images/glasses-prescription.jpg`, re-saved without metadata |
| Retrieved | 2026-11-16 |
| Clearance | `public` |

## Clearance

The publisher made this prescription to show readers how one reads, and introduces it as
"an example to see how it should look". The prescriber printed at the top is the site's
co-author, named in that role. The patient's name and age are specimen values on the
publisher's own example. The site is marked "All rights reserved" and grants no reuse
licence.

## Why this document

It is a small, dense grid of handwritten optical values: signed decimals written with
European decimal commas (−2,00, −0,75), degree signs on the axes, and two header rows
(OD/OS above SPH/CYL/AXIS). Getting the right eye's values from the right row and column
is the whole task.

## Schema

This is the team's existing doc45 schema, used unchanged. It has 16 leaf fields:
prescriber, clinic, exam date, patient name, and sphere, cylinder, axis, addition and
two prism values for each eye.

The extraction read every value correctly. It kept the decimal commas as printed and
dropped the degree signs from the axes. It normalized the date from 13.01.2015 to
2015-01-13.

The schema and this form do not quite fit, and that is worth knowing:

- **There is no near-vision row.** The form gives a full Near prescription. The
  schema's closest field is `addition`, so the extraction put each eye's near sphere
  there (+1,00 and +1,50). On a real prescription, the addition is the difference
  between near and distance power, which here would be +3,00. Downstream code that
  reads `addition` as an add power would be wrong.
- **No pupillary distance or age.** The form prints PD (64 and 62) and the patient's
  age. The schema has no field for either.
- **Prism is required but absent.** The form has no prism columns. OD prism came back as
  empty strings, and OS prism as `null` with a `nonconformant_output` warning. The two
  eyes are inconsistent for the same absence.

## Featured fields, page 1

| Field | Label | Value |
|---|---|---|
| `date_of_exam` | Exam date | 2015-01-13 |
| `prescription.OD.sphere` | Right eye sphere (OD SPH) | -2,00 |
| `prescription.OD.cylinder` | Right eye cylinder (OD CYL) | -1,00 |
| `prescription.OD.axis` | Right eye axis (OD AXIS) | 30 |
| `optometrist_name` | Prescriber | Dr. Szasz Arpad |

Together they show one complete distance prescription for the right eye, with when it was
written and by whom. The patient's name grounds cleanly too, but the impersonal values
make the same point.

## Grounding

- **Table cells ground tightly.** Each value is boxed to its own cell. The right eye's
  cylinder (−1,00) is written in both the Distance and Near rows, and occurrence 0 is
  the Distance row, as the overlay confirms.
- **Every prescription value also has a second, wrong range** pointing at the
  "EYEGLASS PRESCRIPTION" title, marked `OFF`. The empty prism strings ground only
  there. Occurrence 0 is the right one throughout.
- **The OCR check is no use here.** Tesseract misses the handwritten digits, so
  `build_images.py` warns on four fields. Each crop was opened and checked by eye.

## Credits

1.20 credits at standard tier (parse and extract).

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py eyeglass-prescription
.venv/bin/python document-types/scripts/inspect_fields.py eyeglass-prescription --page 1
.venv/bin/python document-types/scripts/build_images.py eyeglass-prescription
```
