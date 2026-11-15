# Investor Presentation (Chinese)

Source assets for `landing.ai/document-type/investor-presentation-chinese`.

## Sample document

`source/boc-2026-interim-results.pdf` is Bank of China's 2026 interim results presentation
(2026年中期业绩发布), dated 2026-08-28. **21 pages, landscape (16:9), Simplified Chinese.**

| | |
|---|---|
| Publisher | Bank of China Limited (SSE: 601988, HKEX: 3988) |
| Source | [pic.bankofchina.com/…/P020260828571239979382.pdf](https://pic.bankofchina.com/bocappd/report/202608/P020260828571239979382.pdf) |
| Retrieved | 2026-11-15, downloaded by script directly from the publisher |
| Clearance | Public |

This is investor relations material that a listed bank published on its own domain for
general distribution. It names no individuals, so nothing needed redacting.

## Why this document

- **Chinese.** Every other investor deck in the collection is English. Here the labels,
  units (百万元人民币, 十亿元人民币), and change notation (个百分点, 个基点) all have to be
  read and kept in Chinese.
- **Image only.** The PDF has no text layer: each page is one raster image produced by
  Acrobat's image-conversion plug-in. Everything ADE returns comes from reading pixels.
- **A very large page.** Each page is 5759 × 3240 pt, about eight times the size of a
  normal slide. The crops come out around 5,000 px wide as a result.
- **Light, branded design.** Pink gradients, 3D bar charts and decorative arrows, against
  the white-background tables in most of the collection.

## Extraction

`schema.json` has **38 leaf fields**. They cover the bank name, title and date; the six
headline metrics on the operating-results slide (page 5), each as a current value, prior
value and printed change; total assets and liabilities (page 6); asset quality and
capital ratios (page 7); and the proposed interim dividend (page 8). Keys are English,
and each description names the Chinese label it maps to.

All 38 fields extracted with correct values, including figures that are only printed as
chart labels.

There was one small slip in following instructions. The description asked for change
strings exactly as printed, and most came back that way (`+1个基点`, `+0.48个百分点`).
The cost-to-income change came back translated, as `-1.68 percentage points`.

## Featured fields: page 7

| Field | Label |
|---|---|
| `asset_quality.npl_ratio_percent` | NPL ratio (不良贷款率) 1.22% |
| `asset_quality.allowance_to_npl_percent` | Allowance to NPLs (不良贷款拨备覆盖率) 200.85% |
| `capital_adequacy.cet1_ratio_percent` | CET1 ratio (核心一级资本充足率) 12.04% |
| `capital_adequacy.tier1_ratio_percent` | Tier 1 ratio (一级资本充足率) 13.65% |
| `capital_adequacy.total_capital_ratio_percent` | Total capital ratio (资本充足率) 18.31% |

These five fields describe how sound the bank is: credit quality on the left and
regulatory capital on the right. Each value grounds to its own row, and each box holds
both the Chinese label and the figure. So the overlay reads as five label-value pairs,
not five numbers floating on the slide.

## What it surfaced

**Chart values ground to the whole chart.** Page 6 was the first pick for featured
fields: total assets and liabilities, two dates each. Every value extracted correctly and
text-matched, but each one grounds only to its whole `figure` block. Because there is no
finer box inside a chart, all five crops were the same half-slide. `inspect_fields.py`
reports these values as `ok`. Only opening the crops showed the problem.

**Some chart values ground to the wrong text.** On page 5, several values ground to an
axis label (`1H2026`) or a word (`Growth`) instead of the figure. Most of the printed
changes (`+8.41%`) ground to the chart's generated `<description>`, not to the printed
label. Slides built from text boxes, like page 7, ground much more cleanly than slides
built from charts.

**One OCR slip in the markdown, and extraction corrected it.** The parse renders the CET1
label as `核一级资本充足率`, dropping `心` from `核心一级`. The extracted value and its box
are still correct.

## Cost

**20.70 credits** at standard tier for the parse and extract together, covering 21 pages.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-chinese                # 20.70 credits
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-chinese --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py investor-presentation-chinese           # free
.venv/bin/python document-types/scripts/inspect_fields.py investor-presentation-chinese --page 7
```
