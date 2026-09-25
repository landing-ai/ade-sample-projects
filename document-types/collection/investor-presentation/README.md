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

`schema.json` defines seven flat fields; all seven populate. There are no nested objects
or arrays, unlike the invoice — that is deliberate, not an oversight.

## Cost

**65.50 credits** at standard tier for 43 pages, parse and extract together. By
comparison the one-page invoice cost 3.10. Worth knowing before adding more long
documents to the collection.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation      # 65.50 credits
.venv/bin/python document-types/scripts/build_images.py investor-presentation # free
```
