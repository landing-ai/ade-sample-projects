# Investor Presentation (Arabic)

Source assets for `landing.ai/document-type/investor-presentation-arabic`.

## Sample document

`source/barwa-investor-presentation-q1-2026-ar.pdf`: Barwa Real Estate's Arabic-language
investor presentation for the first quarter of 2026, dated April 2026. **34 pages, landscape
(792×612)**, exported from PowerPoint.

| | |
|---|---|
| Publisher | Barwa Real Estate Company Q.P.S.C. (Qatar Stock Exchange) |
| Source | [barwa.com.qa/documents/investor-presentations/2026/…الربع الاول2026.pdf](https://www.barwa.com.qa/documents/investor-presentations/2026/%D8%A7%D9%84%D8%B9%D8%B1%D8%B6%20%D8%A7%D9%84%D8%AA%D9%82%D8%AF%D9%8A%D9%85%D9%8A%20%D9%84%D9%84%D9%85%D8%B3%D8%AA%D8%AB%D9%85%D8%B1%D9%8A%D9%86-%D8%A7%D9%84%D8%B1%D8%A8%D8%B9%20%D8%A7%D9%84%D8%A7%D9%88%D9%842026.pdf) |
| Retrieved | 2026-11-15, downloaded by script |
| Clearance | Public |

Investor relations material published by a listed company for general distribution. The
slides carry no personal data. The only contact details are the investor relations team's
corporate mailbox and switchboard number on the last slide.

The PDF's document metadata named the employee who exported the file, so all metadata was
cleared with `document-types/scripts/pdfmeta.py` before parsing. No page content was changed.

## Why this document

It is the collection's first right-to-left document. Investor decks are already covered by the
English `investor-presentation` (Park National) sample. This one tests what changes when the
script runs right to left:

- **Arabic text, right to left.** Tables put the label column on the right and the value on
  the left, and parsed cells are numbered in visual order (column 0 is the left-hand value).
- **Two digit systems in one deck.** Some slides print Western digits (`12,976`) and others
  print Arabic-Indic digits (`٤٨٦`). The PDF's own text layer stores Western digits even where
  the font draws Arabic-Indic ones. ADE mostly transcribes the digits as drawn, but not
  consistently. Every card on page 22 is drawn in Arabic-Indic digits, yet the parse wrote the
  dividend card (`١٨%`, `٦.٦%`, `٢٠٢٥`) in Western digits and the other cards in Arabic-Indic.
- **A full deck layout**: KPI cards, ruled tables, bar and stacked charts, a map, and photographs.

## Extraction

`schema.json` has **27 leaf fields**. Five are company-level, ten are the Q1 highlights
from page 22, twelve cover capital structure (including a five-bar debt maturity array) from
page 13, and three cover portfolio scale. Schema descriptions ask for numbers in Western
digits, so `٤٨٦` extracts as `486`. The digit conversion itself never failed. The one wrong
value, below, comes from the parse.

## Featured fields

All on **page 13**, "سيولة مالية لضمان توزيع رأس المال بحكمة" (financial liquidity):

| Field | Value | Why |
|---|---|---|
| Debt (QAR m) | 12,976 | Ruled table row |
| Bank balances (QAR m) | 1,244 | The next row |
| Net debt (QAR m) | 11,732 | Debt minus bank balances |
| Net debt to assets | 0.32 | The ratio the table builds to |

Together they tell one story: debt, less cash, gives net debt, which gives the leverage ratio.
Each value grounds to its own table cell, and every crop was checked by eye.

## What it surfaced

**Arabic-Indic digits defeat the value check, not the grounding.** On page 22 the operating
revenue extracts as `486` and grounds to the card reading `٤٨٦ مليون ريال قطري`, which is
correct. `inspect_fields.py` and `build_images.py` compare digit strings literally, so they
report `OFF` for every Arabic-Indic value. That is why page 22, the most visual slide in the
deck, is not the feature page. Normalizing Arabic-Indic digits in those scripts would let it
be featured.

**The Arabic-Indic zero can be read as a decimal point.** The operating margin card reads
`٧٠%` (70%). The parse transcribed it as `٧.٠%`, so the final extraction gives
`operating_margin_percent: 7.0`. The zero `٠` is a small raised dot. An earlier extraction
against the same parse returned 70, drawn from a sentence on page 11, so the value changes
from run to run. This is an Arabic-specific parse error to watch for.

**Right-to-left tables can ground to the label cell.** In the page 13 table, `total_equity`
and `net_debt_to_equity` ground to the Arabic label cell beside the value (`اجمالي حقوق
الملكية`) rather than the number. The neighbouring rows ground correctly. In the first
extraction `total_assets` did the same, and in the second it grounded correctly.

**Chart labels do not ground tightly.** The debt maturity bars on page 13 (838, 2,255, 1,296,
1,169, 7,418) extract correctly every time. In the first extraction they all grounded to the
whole chart figure, so every crop would have been the same large region. In the second
extraction they had no grounding at all.

**Cell-level grounding on the ruled table is excellent.** Each value cell has its own box,
and the boxes line up with the printed rule lines.

## Cost

**51.40 credits** at standard tier: 40.40 for parse and extract of 34 pages, and 11.00 for one
extract-only re-run after fixing the description of `cash_dividend_percent`, which had
returned null.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-arabic                # parse + extract
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-arabic --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py investor-presentation-arabic           # free
.venv/bin/python document-types/scripts/inspect_fields.py investor-presentation-arabic --page 13
```
