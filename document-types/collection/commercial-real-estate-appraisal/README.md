# Commercial Real Estate Appraisal

A narrative commercial appraisal by Integra Realty Resources - DFW, LLP. It values the
"GSA Office", a 39,329 SF single-tenant Class B office building at 4211 Cedar Springs Drive,
Dallas, leased to the U.S. General Services Administration. The premise is **Fair Value As
Is**, compliant with FAS 157 and effective March 2, 2011, at **$4,600,000**. The client was
Kent International Holdings, Inc., which filed the full report with the SEC as an exhibit
to its going-private Schedule 13E-3.

This folder keeps **8 of the report's 166 pages**. All are portrait, US Letter.

| Page here | Source page | Content |
|---|---|---|
| 1 | 1 | Cover |
| 2-3 | 3-4 | Transmittal letter, value conclusion, signature block |
| 4-5 | 6-7 | Summary of Salient Facts and Conclusions, parts one and two |
| 6 | 8 | Identification of Subject (tax ID, legal description, ownership history) |
| 7-8 | 83-84 | Reconciliation and Conclusion of Value |

The other 158 pages were left out to keep the parse cost proportionate to the page this
folder feeds. They cover the market and area analysis, land and improvements, the sales
comparison and income approach detail, the certification, limiting conditions,
qualifications and addenda. The kept pages still read as a complete summary of the
assignment.

## Provenance

| | |
|---|---|
| Publisher | Integra Realty Resources - DFW, LLP (appraiser); filed by Kent International Holdings, Inc. |
| Source URL | https://www.sec.gov/Archives/edgar/data/728478/000109690611002287/ex16e.pdf |
| Filing | Schedule SC 13E3/A (Amendment No. 2), filed 2011-09-29, accession 0001096906-11-002287, Exhibit 16(e) |
| Retrieved | 2026-10-13, downloaded by script |
| Clearance | `redacted` |

The report is a public SEC filing. The EDGAR filing index describes this exhibit as the
Integra Realty Resources appraisal of the Dallas, Texas GSA office property. The firm's
copyright footer limits reliance on the report; it does not ban reproduction.

**What was changed.** I used `document-types/scripts/redact.py`, which removes content
rather than covering it:

- **Signature images: 3 removed** from the transmittal letter (page 3). These are the three
  appraisers' signatures. Each was replaced with a blank 1x1 image, and no stand-in
  signature was drawn, so the signature lines are empty.
- **Addressee street line: 1 string, replaced in 2 places** (cover and letter) with
  `100 Main Street`. It is not the company's EDGAR business address and could be a
  residence. City, state and ZIP are unchanged.
- **Document metadata cleared.**

**What was kept, deliberately.** The appraisers' names, titles and Texas certificate
numbers, and the client CFO's name and title. These are professional details printed in a
public filing. The firm's office addresses and phone numbers were also kept.

The output was verified: redact.py re-extracted the text and found no original string, and
no image remains in the removed regions. The rules file lives outside the repo.

## Why this document

The collection already has a residential appraisal (`appraisal-report`), which is a
GSE-standard URAR form with ruled grids. This one is the other kind of appraisal: a
narrative report written in a word processor, where the facts sit in tables and prose and
nothing is a form field. It also has a quirk real underwriting pipelines run into. The
**same Value Conclusions table is printed three times**: in the transmittal letter, in the
Salient Facts and in the reconciliation.

## Featured fields

All five are on **page 4**, the Summary of Salient Facts:

| Field | Label | Value |
|---|---|---|
| `property.tax_id` | Tax ID | 001616000901A0000 |
| `property.gross_building_area_sf` | Gross building area | 39,329 SF |
| `property.percent_leased` | Percent leased | 100% |
| `property.year_built` | Year built | 1985 |
| `value_conclusions[1].value_conclusion` | Fair value as is | $4,600,000 |

Read top to bottom, they cover the parcel, its size, occupancy and age, and the value the
appraisers concluded. The request suggested eight values from this page. All of them ground
correctly, but a page carries at most five, so I left out property type (printed as
"Office - Office") and the premise, interest and date columns of the value conclusion row.
The label carries the premise. No person is featured.

## Grounding notes

- **The Salient Facts table grounds cleanly.** Each value boxes exactly its own cell on the
  right row, including the alphanumeric tax ID.
- **Dates must be extracted as printed to be featurable.** In the first run, the schema
  asked for ISO dates and both `date_of_value` and `report_date` grounded OFF: the value
  2011-03-02 does not appear in the cell, which reads "March 2, 2011". Asking for the date
  as printed fixed it.
- **The repeated table makes array extraction unstable.** Over four extract-only runs with
  slightly different descriptions for `value_conclusions`:
  - Two runs returned three identical rows, one per printed copy, all grounded.
  - A run asked to de-duplicate returned one row with **no ranges at all** (synthesized).
  - A run pinned to the Salient Facts copy returned two synthesized rows.
  - The committed run returned three rows, and only the middle one (page 4) carries ranges.

  That is why the featured path is `value_conclusions[1]`. On documents that repeat a
  summary table, asking the model to merge the copies costs grounding.
- **The extraordinary assumption is repeated three times as well**, and grounds OFF because
  its range is split across the two lines of the wrapped sentence.
- **"Not Used" became 0.** `valuation_approaches.cost_approach_value` came back 0 for a cost
  approach printed as "Not Used", although the description asks for null. Treat it as a
  known extraction error.
- `year_built` grounded OFF in the first run, boxing the "Year Built" label. Once the
  description named the Year Built row it grounded to the 1985 cell.

The schema has **50 leaf fields**.

## Credits

Standard tier, jobs API, DPT-3 Pro:

| Run | Credits |
|---|---|
| Parse and first extract | 13.80 |
| Four extract-only reruns while refining the schema | 6.20 + 5.90 + 6.10 + 6.20 |
| **Total** | **38.20** |

A fresh parse plus extract of these 8 pages costs about 14 credits.

## Regenerate

```bash
# Trim and redact (the rules file is kept outside the repo)
.venv/bin/python -c "import fitz; d=fitz.open('ex16e.pdf'); d.select([0,2,3,5,6,7,82,83]); d.save('trimmed.pdf', garbage=4, deflate=True)"
.venv/bin/python document-types/scripts/redact.py trimmed.pdf \
    document-types/collection/commercial-real-estate-appraisal/source/commercial-real-estate-appraisal-irr-gsa-office-dallas.pdf \
    --rules <outside-the-repo>/rules.json \
    --remove-images 3:85,410,440,475 3:88,534,280,593

.venv/bin/python document-types/scripts/run_ade.py commercial-real-estate-appraisal
.venv/bin/python document-types/scripts/build_images.py commercial-real-estate-appraisal
```

Re-running extraction may return a different number of `value_conclusions` rows; see the
grounding notes above.
