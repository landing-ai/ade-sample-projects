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

`schema.json` has seven company-level fields plus an `installment_lending` object built
around **page 35**, the Installment Lending Portfolio slide. That page carries a pie
chart, three bullet figures, and a 5×7 data table under a stacked bar chart, so it
exercises far more of ADE than a flat schema would.

All of it extracts correctly:

- **Pie chart** — six credit tiers with their shares (Premier 52.35% down to D 0.40%),
  and each tier's FICO range pulled from the *legend*, which is a separate region of the
  slide.
- **Data table** — all 5 rows × 7 origination years, matching the printed values.
- **Bullets** — $1.6B indirect, $186MM direct, weighted average FICO over 780.

## Featured fields must share a page

A web page can realistically embed one page overlay, so every featured field has to live
on the same page. `manifest.json` declares `"feature_page": 35` and `build_images.py`
warns if any field resolves elsewhere. An earlier version of this manifest featured
fields from pages 1, 4 and 6 and could not be illustrated with a single image.

## Grounding is off by one in this document's arrays

Worth knowing before trusting any array field on a chart-heavy document.

The **values** extracted from page 35 are all correct. The **grounding ranges** for array
elements are shifted by exactly one position:

| Field | Value | Grounded to |
|---|---|---|
| `balances_by_origination_year[0].credit_tier` | `Premier (FICO 780+)` | `18,429,225` |
| `balances_by_origination_year[0].pre_2020` | `18429225` | `38,573,958` |
| `balances_by_origination_year[0].year_2025` | `322236185` | `A+ (FICO 740 - 779)` |
| `portfolio_by_credit_tier[0].tier` | `Premier` | `52.35%` |
| `portfolio_by_credit_tier[0].share_of_portfolio_percent` | `52.35` | `A+` |

Each field grounds to the *next* cell in reading order, and the last column of a row
grounds to the following row's label. It is systematic, not random.

`fico_range` is the exception and grounds correctly, because it comes from the legend
rather than from the pie or the table.

This is not a script bug — the ranges come back this way from Extract. It is also not
universal: `line_items[1].description` on the invoice sample grounds correctly. It
appears to affect dense tabular and chart regions.

**What this means for the pages:** featured fields are chosen for grounding accuracy, not
just for interest. `build_images.py` compares every extracted value against the text it
boxed and warns on a mismatch, which is what caught this. Never feature a field without
reading its crop.

## Cost

**65.50 credits** at standard tier for 43 pages, parse and extract together. By
comparison the one-page invoice cost 3.10. Worth knowing before adding more long
documents to the collection.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation      # 65.50 credits
.venv/bin/python document-types/scripts/build_images.py investor-presentation # free
```
