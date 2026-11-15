# Investor Presentation (Korean)

Source assets for `landing.ai/document-type/investor-presentation-korean`.

## Sample document

`source/naver-3q26-earnings-kor.pdf` is NAVER's third-quarter 2026 earnings presentation
(2026년도 3분기 실적발표), dated 2026-11-12. **10 pages, landscape (4:3), Korean.**

| | |
|---|---|
| Publisher | NAVER Corporation (KRX: 035420) |
| Source | [navercorp.com/api/article/download/…](https://navercorp.com/api/article/download/5424bdee-8b0f-4f03-b38f-a308a9381eb9) |
| Retrieved | 2026-11-15, downloaded by script directly from the publisher |
| Clearance | Public |

This is investor relations material that a listed company published on its own domain
for general distribution. The source URL is a download endpoint rather than a file path.
It returned `application/pdf` with the filename `3Q26_Naver_Earnings_KOR_vF.pdf`, and the
file was checked to be a 10-page PDF, not an HTML or JSON response. It is stored here under
a descriptive name. The deck names no individuals, so nothing needed redacting.

## Why this document

- **Korean.** Labels (매출액, 영업이익, 당기순이익), units (십억 원, 조 원) and the
  percentage-point notation (`-5.2%p`) all have to be read and kept in Korean.
- **A real text layer.** Exported from PowerPoint, unlike the image-only Chinese deck, so
  this shows ADE on a born-digital slide deck in a non-Latin script.
- **Dense financial tables on slides.** The results summary, cost and net-income slides
  are ruled tables of five quarters plus Y/Y and Q/Q columns, with indented sub-segment
  rows. Other slides are stacked bar charts with value labels.

## Extraction

`schema.json` has **47 leaf fields**. They cover the company, title, date, period,
accounting basis and unit; the four headline rows of the results summary (revenue,
operating expenses, operating profit, net income), each with 3Q26, 3Q25, Y/Y and Q/Q;
3Q26 revenue for every segment; payment volume from the financial platform slide; the
cost breakdown; cash and borrowings; and the non-operating items from the appendix.
Keys are English, and each description names the Korean label it maps to.

Every field extracted with the correct value. Segment names came back in Korean as asked.

## Featured fields: page 3

| Field | Label |
|---|---|
| `results_summary.revenue.q3_2026` | Revenue (3Q26) — 매출액 3,472.4 |
| `results_summary.revenue.yoy_change` | Revenue growth YoY — 10.7% |
| `results_summary.operating_profit.q3_2026` | Operating profit (3Q26) — 영업이익 451.3 |
| `results_summary.operating_profit.yoy_change` | Operating profit change YoY — -20.9% |
| `results_summary.net_income.q3_2026` | Net income (3Q26) — 당기순이익 402.5 |

These tell the quarter's headline story, the same one the slide's two bullets tell:
revenue up 10.7% while operating profit fell 20.9%. Every value grounds to its own cell
in the highlighted 3Q26 and Y/Y columns, so the overlay shows five tight boxes on the
right rows.

## What it surfaced

**Table cells ground tightly.** The 47 schema leaves expand to 68 extracted values (the
segment array has eight entries), cited at 80 places in the parse. 77 of those 80 contain
their value, every value except one has at least one good grounding, and the cells on the summary, cost, cash and
appendix tables each got their own box. This contrasts with the Chinese deck, where an
image-only PDF and chart-built slides left values grounded to whole figures.

**Repeated figures ground in more than one place.** Operating profit, net income and their
Y/Y and Q/Q changes appear on both page 3 and page 7, and extraction cited both. The
featured fields pin occurrence 0, on page 3.

**Three groundings are off.** `operating_expenses.q3_2025` grounds to the row label
`영업비용` rather than `2,567.4`; `reporting_period` cites the cover title as well as the
`3Q26` column header; and revenue's `10.7%` also cites the footnote, which gives the
ex-acquisition figure of 9.0%. The values are all correct.

**Charts become tables.** The stacked bar charts on pages 4–6 are parsed as `figure`
blocks containing a generated description and a reconstructed data table. Payment volume
(26.2조 원) was grounded both to the bullet text that prints it and to that generated
table.

## Cost

**13.80 credits** at standard tier for the parse and extract together, covering 10 pages.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-korean                # 13.80 credits
.venv/bin/python document-types/scripts/run_ade.py investor-presentation-korean --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py investor-presentation-korean           # free
.venv/bin/python document-types/scripts/inspect_fields.py investor-presentation-korean --page 3
```
