# Financial Model

A real estate development pro forma: the **Aloha Development Model** by Jones Lang
LaSalle (JLL). It was published as Exhibit C to the *Aloha Stadium Conceptual
Redevelopment Report* (February 23, 2017), which Foley & Lardner LLP prepared for the
State of Hawaii Department of Accounting and General Services and Stadium Authority. The
model values a 1.21 million square foot mixed-use district around a new stadium. It
covers office, retail, residential and hotel, and runs a 13-year development-and-hold
timeline for each.

This folder keeps **16 of the report's 181 pages**, the whole of Exhibit C as printed
("Page 1 of 16" to "Page 16 of 16"). The pages are landscape spreadsheet printouts at
eleven different page sizes, from 792x612 pt up to 1685x1302 pt.

| Page here | Content |
|---|---|
| 1 | Returns summary: two scenarios (sale on stabilization, long-term hold) |
| 2 | Mixed-use assumptions: program, land valuation, parking |
| 3 | Budget assumptions by product type |
| 4 | Mixed-use cash flows, 13 years |
| 5-7 | Office: assumptions, then two own-operate cash flow sheets |
| 8-10 | Retail: assumptions, then two own-operate cash flow sheets |
| 11-13 | Residential: assumptions, then two own-operate cash flow sheets |
| 14-16 | Hotel: assumptions, own-operate cash flows, own-operate sale cash flows |

## Provenance

| | |
|---|---|
| Publisher | Jones Lang LaSalle (model), within a Foley & Lardner LLP report for the State of Hawaii DAGS / Stadium Authority |
| Source URL | https://alohastadium.hawaii.gov/wp-content/uploads/2026/03/alohastadiumconceptualredevelopmentreport.pdf |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | `public` |

The State publishes the full report on its own alohastadium.hawaii.gov domain. The
report cover is marked "Privileged and Confidential / Attorney-Client Communication", and
every model page has a "Confidential" footer. Those markings predate the State's own
publication of the report, and they are left as printed. Source pages 160-175 were split
out with PyMuPDF. The Exhibit D cash flow projections (source pages 177-181) were left out
by operator decision: they are a separate renovate-versus-rebuild comparison by a
different author. The Exhibit D slip sheet, which names an individual preparer, was also
left out.

**Personal data.** The kept pages name no individuals and carry no contact details, so
nothing was redacted. The PDF's metadata named an individual author, and it was cleared.

## Why this document

Most financial documents in the collection are statements: one period, labelled rows,
values in one or two columns. A pro forma is a grid. On the cash flow sheets, every row
is a line item, and the columns are a Total followed by 13 years, each with a calendar
year, a development year and a hold year in a three-row header. The construction-period
cells are empty, negatives are red and in parentheses, and the type is small.
Answering "what is the DSCR" means finding a highlighted row, then the first non-empty
column. The model also repeats one structure for four product types, so an extractor has
to keep the office sheet's values apart from the retail sheet's values, though the labels
are identical.

The schema has 40 leaf fields in three groups: the returns summary per scenario, the
assumptions per product type (land, GSF, construction and permanent loan terms, rent,
cap rate, total costs), and the headline results per cash flow sheet.

## Featured fields

All five are on **page 6**, the office own-operate cash flow sheet (source page 165):

| Field | Label | Value |
|---|---|---|
| `cash_flow_scenarios[0].total_costs` | Total costs | $64,299,010 |
| `cash_flow_scenarios[0].permanent_loan_beginning_balance` | Permanent loan beginning balance | ($50,971,154) |
| `cash_flow_scenarios[0].first_year_dscr` | First-year DSCR | 1.25 |
| `cash_flow_scenarios[0].residual_value` | Residual value | $83,029,620 |
| `cash_flow_scenarios[0].aloha_irr` | Owner IRR | 14.25% |

Read top to bottom, they follow one development from cost through debt to exit: what it
costs, what the take-out loan opens at, how well year one covers the debt, what the
building sells for, and what return the owner earns. These are the five values the
request suggested, and all five ground correctly.

## Grounding notes

- **The featured grid grounds to the right cell.** The permanent loan balance and the
  DSCR are both in the first operating year (2021), after three empty construction
  columns. Both box that one cell, not the Total column or the row label. The DSCR is
  correct even though its row is highlighted and set in grey italics.
- **The source has a labelling quirk, which ADE read through.** On the office sheet, the
  permanent loan block is labelled "Retail" and the first cost line reads "Construction
  Costs - Retail". The template was evidently copied from the retail sheet. Extraction
  still took the values from the office sheet.
- **Footer page labels went to the wrong sheet.** The parse puts each "Page N of 16"
  footer on its correct page. Extraction, however, often gave a cash flow sheet the label
  of the sheet before it: the first retail sheet (page 9) came back as "Page 8 of 16",
  and the first office sheet's label came back null. `page_label` should not be trusted
  on this document.
- **Second sheets per product ground worse.** Each product type has a second cash flow
  sheet with a different hold and exit. The values extracted from these sheets are mostly
  right, but several of their ranges point at the sheet's title or footer rather than at
  the cell (`OFF`). On the second office sheet, the permanent loan rows are all $0 and there
  is no DSCR row. The DSCR came back null on every second sheet. The beginning balance
  came back null on the office sheet but 0 on the retail, residential and hotel sheets.
- **One assumptions sheet came back with no coordinates.** On the residential sheet
  (page 11), all 13 values are correct but have no ranges (`SYNTH`). On the hotel sheet
  (page 14), each value grounds `ok` once and then again, `OFF`, onto the "Development
  Assumptions" heading.
- **Fields the source does not have.** The hotel has no net rent or vacancy: it uses
  room-night assumptions instead. Extraction returned null and an empty string for these,
  as the schema allows.

## Credits

102.2 credits at the standard tier: 71.0 for the first parse and extract of the 16
pages, then 31.2 for one extract-only re-run. The re-run made hotel net rent nullable and
clarified the cash flow sheet fields.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py financial-model            # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py financial-model --extract-only
.venv/bin/python document-types/scripts/build_images.py financial-model      # images, no API calls
```

The source PDF was produced from the full report with PyMuPDF (`insert_pdf` of source
pages 160-175, 0-based 159-174). Its metadata was then cleared with
`document-types/scripts/pdfmeta.py`.
