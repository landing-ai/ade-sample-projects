# Investor presentation

Source assets for `landing.ai/document-type/investor-presentation`.

## Sample document

`source/Q4-2025-Investor-Slides.pdf` — Park National Corporation's Q4 2025 investor
slides. **43 pages, landscape (720×540).**

| | |
|---|---|
| Publisher | Park National Corporation (NYSE American: PRK) |
| Source | [s201.q4cdn.com/960710146/…/Q4-2025-Investor-Slides.pdf](https://s201.q4cdn.com/960710146/files/doc_presentations/2026/Feb/09/Q4-2025-Investor-Slides.pdf) |
| Retrieved | 2026-09-25 |
| Clearance | Public |

Investor relations material published by a listed company for general distribution, so
it is publishable without further clearance. It names executives, but only in their
professional capacity, which is the point of the document.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

It is the pilot's hard case, and it is in the pilot to break things early:

- **Landscape**, where every other sample is portrait. Crop and render logic tuned on
  portrait pages would produce bad output here.
- **43 pages**, so featured fields land on different pages and the page-render path is
  exercised properly. The five featured fields fall on pages 1, 4 and 6.
- **A dark cover slide.** The highlight style was designed against white documents, and
  this was the first real test of it on a dark background.
- **Parsing matters more than extraction.** The schema is deliberately thin — seven flat
  fields. The value in a deck is what parsing recovers from slide layouts, charts and
  tables, not a rich field set.

## What it surfaced

**The highlight works on a dark slide, but looks different.** Translucent yellow over
dark navy reads as a greenish tint rather than a warm highlight. It is legible, and the
amber border carries it, but it is visibly not the same treatment as on a white page. If
the library ends up with many dark documents this may need a background-aware fill.

**Grounding can support a value without showing it.** `total_assets` extracted as
`$9.8 billion` and its first range grounds to a table cell reading `$ 9,805`. Both are
correct — 9,805 million is 9.8 billion — but a crop whose text does not match the value
printed beside it reads as an error. `build_images.py` now warns on this and names an
occurrence that does contain the value; the manifest pins `total_assets` to occurrence 1.

**Common values have many occurrences.** `company_name` appears 49 times in the deck and
`as_of_date` 57 times, so the default first-occurrence choice is close to arbitrary. All
five featured fields are pinned.

## Extraction

`schema.json` has seven company-level fields plus a `fee_income` object built around
**page 20, "Diverse Fee Income"** — a slide from the main presentation rather than the
appendix. That page carries all four element types in one place, which is why it was
chosen:

| Region | Featured field |
|---|---|
| Overview bullet | The 21.5% non-interest income ratio, in prose |
| Bar chart | The same ratio, as a chart label |
| Pie chart | Fiduciary Activities, the largest income source |
| Footnotes | The $6.1MM pension settlement gain |

The ratio is featured twice deliberately: the same figure grounded in a sentence and in
a chart is a better demonstration than two unrelated values.

Everything extracts correctly — all five years of the bar chart, all six pie slices with
their percentages, the bullet figures, and the footnote detail.

## Featured fields must share a page

A web page can realistically embed one page overlay, so every featured field has to live
on the same page. `manifest.json` declares `"feature_page": 20` and `build_images.py`
warns if any field resolves elsewhere. An earlier manifest featured fields from pages 1,
4 and 6, which no single image could show.

## Choosing what to feature

Reading `extract-*.json` is not enough to pick fields. Three failure modes are invisible
until you look, and `inspect_fields.py` exists to surface all three:

```bash
python document-types/scripts/inspect_fields.py investor-presentation --page 20 --good
```

**Synthesized values.** `net_interest_income_latest_year` is correct at 437.3 but has no
ranges at all — ADE read it from the chart without being able to point at it. It cannot
be illustrated.

**Grounding off by one.** Array elements in dense tables and charts ground one cell
adrift: in `revenue_by_year`, `year` grounds to the net interest income figure, which
grounds to the non-interest income figure, and so on. The values are right; the ranges
are shifted. Not universal — the pie chart array on this same page grounds correctly, as
does `line_items` on the invoice.

**Grounded on another page.** The bar chart's series values ground to page 18, not 20.

Two further traps this page hit: a field can ground to a whole `figure` block rather than
to the value inside it, so featuring both the pie's `source` and its `share_percent`
produced *identical* images; and a value printed in several places needs its occurrence
pinned, or the box wanders between runs.

`build_images.py` compares every extracted value against the text it boxed and warns on a
mismatch, which is what caught the off-by-one. Never feature a field without reading its
crop.

## Cost

**65.50 credits** at standard tier for 43 pages, parse and extract together. By
comparison the one-page invoice cost 3.10.

Iterating on the schema does not cost that again: `run_ade.py --extract-only` reuses the
committed parse and re-runs extraction alone, at **21.30 credits**. Parsing is the
expensive half and the markdown does not change.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation                # 65.50 credits
.venv/bin/python document-types/scripts/run_ade.py investor-presentation --extract-only # 21.30, schema iteration
.venv/bin/python document-types/scripts/build_images.py investor-presentation           # free
.venv/bin/python document-types/scripts/inspect_fields.py investor-presentation --page 20 --good
```
