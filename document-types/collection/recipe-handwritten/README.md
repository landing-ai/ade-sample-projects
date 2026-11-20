# Recipe (Handwritten)

A family recipe card for Date Bars, written in cursive on a ruled index card and
photographed lying on a fabric surface. One landscape image, 1600 × 1200.

| | |
|---|---|
| Publisher | JayDee Mahs, [jaydeemahs.com](https://www.jaydeemahs.com/the-importance-of-handwritten-recipes-preserving-memories/), in the post *The Importance of Handwritten Recipes – Preserving Memories* |
| Source URL | https://i0.wp.com/www.jaydeemahs.com/wp-content/uploads/2023/11/1-Moms-Recipes-3.jpg?resize=768%2C576&ssl=1 |
| File | The full-resolution original behind that URL, which serves a 768 × 576 resize. EXIF metadata stripped |
| Retrieved | 2026-11-16 |
| Clearance | `public` |

## Clearance

The blog shows the card in a post about its author's mother's recipe box. The site is
marked "All Rights Reserved" and offers no reuse licence. The operator accepted that and
chose to publish it.

The name in the top-right corner is the blogger's own. The post says their mother wrote
it on the card, and it is the name the blog is published under. It is left as written.
Nothing else on the card identifies anyone.

## Why this document

The collection's other handwritten samples are forms, where the handwriting sits in
labelled boxes. This one has no structure at all: cursive on ruled lines, stacked
fractions (1½, 1¼, ¾), abbreviations (tsp., oleo) and an ingredient line that
carries a second ingredient after a dash. Every structured value has to come from
reading the handwriting.

## Schema

This is the team's existing doc44 recipe schema, used unchanged: a dish name, an array of
ingredients (name, unit, quantity, other details) and a free-text instructions field.
That is 6 leaf fields.

The extraction read every word on the card correctly, including the stacked fractions,
"scant 3/4" and "tsp.". One structural miss: the oleo line ends "- 1 tsp soda", and
the extraction put "1 tsp soda" into oleo's `other_details` instead of listing baking
soda as a sixth ingredient. The schema requires `other_details` on every ingredient,
which may encourage the model to fill it. The other four ingredients return it as an
empty string.

## Featured fields, page 1

| Field | Label | Value |
|---|---|---|
| `dish_name` | Dish name | Date Bars |
| `ingredients[0].quantity` | Oatmeal quantity | 1 1/2 |
| `ingredients[2].unit_of_measure` | Salt unit | tsp. |
| `ingredients[3].quantity` | Flour quantity | 1 1/4 |
| `ingredients[4].quantity` | Oleo quantity | scant 3/4 |

The handwritten fractions and abbreviations are what make this card hard to read, so the
featured fields are those values.

## Grounding

- **Handwriting grounds to the line.** Each ingredient's quantity, unit and name all
  share one box, the whole written line. So the overlay boxes lines, not individual
  values, and the boxes for neighbouring lines overlap slightly, because the cursive
  runs above and below the ruling.
- **`instructions` cannot be featured.** It is written over four lines, and gets one
  range per line. No single range contains the joined value.
- **Empty `other_details` values ground to the whole card.** Nothing is there to point
  at.
- **The OCR check is no use here.** Tesseract reads none of the cursive, so
  `build_images.py` warns on every field. Each crop was opened and checked by eye.

## Credits

1.40 credits at standard tier (parse and extract).

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py recipe-handwritten
.venv/bin/python document-types/scripts/inspect_fields.py recipe-handwritten --page 1
.venv/bin/python document-types/scripts/build_images.py recipe-handwritten
```
