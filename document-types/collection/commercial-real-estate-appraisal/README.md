# Commercial Real Estate Appraisal

**On the website:** [landing.ai/document-type/commercial-real-estate-appraisal](https://landing.ai/document-type/commercial-real-estate-appraisal)

Eight pages from a narrative commercial appraisal by Integra Realty Resources - DFW, LLP
of the "GSA Office", a 39,329 SF Class B office building in Dallas leased to the U.S.
General Services Administration. They hold the cover, the transmittal letter, the
summary of salient facts, the identification of the property and the reconciliation,
which concludes a Fair Value As Is of $4,600,000 as of March 2, 2011.

| | |
|---|---|
| Pages | 8 |
| Fields in the extraction schema | 50 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:42 | 2026-11-19 02:44 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 14,067 | 14,407 |
| Words under 0.95 confidence | 26 | n/a |
| Words under 0.80 confidence | 4 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 11.5 s | 12.8 s |
| Per page | 1.4 s | 1.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.7 credits | 7.7 credits |
| Per page | 0.34 credits | 0.96 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:42 | 2026-11-19 02:44 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 50 | 50 |
| Non-null fields returned | 49 | 49 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 138.4 s | 129.5 s |
| Per schema field (50) | 2.77 s | 2.59 s |
| Per value returned | 2.39 s | 2.23 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.2 credits | 5.3 credits |
| Per schema field (50) | 0.104 credits | 0.106 credits |
| Per value returned | 0.090 credits | 0.091 credits |

## Origin

`source/commercial-real-estate-appraisal-irr-gsa-office-dallas.pdf` is part of a
narrative commercial appraisal by Integra Realty Resources - DFW, LLP. It values the "GSA
Office", a 39,329 SF single-tenant Class B office building at 4211 Cedar Springs Drive,
Dallas, leased to the U.S. General Services Administration. The premise is Fair Value As
Is, compliant with FAS 157 and effective March 2, 2011, at $4,600,000. The client was
Kent International Holdings, Inc., which filed the full report with the SEC as an exhibit
to its going-private Schedule 13E-3.

The file keeps **8 of the report's 166 pages**, all **portrait (US Letter)**:

| Page here | Source page | Content |
|---|---|---|
| 1 | 1 | Cover |
| 2-3 | 3-4 | Transmittal letter, value conclusion, signature block |
| 4-5 | 6-7 | Summary of Salient Facts and Conclusions, parts one and two |
| 6 | 8 | Identification of Subject (tax ID, legal description, ownership history) |
| 7-8 | 83-84 | Reconciliation and Conclusion of Value |

The other 158 pages were left out to keep the parse cost proportionate. They cover the
market and area analysis, land and improvements, the sales comparison and income
approach detail, the certification, limiting conditions, qualifications and addenda. The
kept pages still read as a complete summary of the assignment.

| | |
|---|---|
| Publisher | Integra Realty Resources - DFW, LLP (appraiser); filed by Kent International Holdings, Inc. |
| Source | [sec.gov/Archives/edgar/data/728478/000109690611002287/ex16e.pdf](https://www.sec.gov/Archives/edgar/data/728478/000109690611002287/ex16e.pdf) |
| Filing | Schedule SC 13E3/A (Amendment No. 2), filed 2011-09-29, accession 0001096906-11-002287, Exhibit 16(e) |
| Retrieved | 2026-10-13, downloaded by script |
| Clearance | Redacted |

The report is a public SEC filing. The EDGAR filing index describes this exhibit as the
Integra Realty Resources appraisal of the Dallas, Texas GSA office property. The firm's
copyright footer limits reliance on the report. It does not ban reproduction.

Two changes were made with `document-types/scripts/redact.py`, which removes content
rather than covering it:

- **Signature images: 3 removed** from the transmittal letter (page 3). These are the
  three appraisers' signatures. Each was replaced with a blank image and no stand-in
  signature was drawn, so the signature lines are empty.
- **Addressee street line: 1 string, replaced in 2 places** (cover and letter) with
  `100 Main Street`. It is not the company's EDGAR business address and could be a
  residence. City, state and ZIP are unchanged.

The document metadata was cleared. The appraisers' names, titles and Texas certificate
numbers, and the client CFO's name and title, were kept on purpose. They are professional
details printed in a public filing. The firm's office addresses and phone numbers were
also kept. A re-extraction found no original string, and no image remains in the removed
regions. The rules file lives outside the repo. Full provenance is in `manifest.json`
under `source.origin`.

## Why this document

### Who processes it

A commercial appraisal states what a property is worth and how the appraiser got there.
Lenders, investors and auditors rely on it for transactions and for the books.

- **Commercial real estate lending:** banks and CMBS lenders underwrite loans against
  the appraised value and check it against the loan amount.
- **Investors and fund managers:** buyers and REITs read appraisals during acquisitions
  and to value portfolios.
- **Accounting and audit:** fair value appraisals like this one support financial
  statement values under FAS 157.
- **Corporate transactions:** companies file appraisals with the SEC to support the price
  in going-private and other transactions, as Kent International did here.
- **Property tax consultants and assessors:** they use appraisals to argue or set
  assessed values.

### What it contains

- **A narrative report, not a form.** The facts sit in tables, labeled lists and prose
  paragraphs, written in a word processor.
- **The same value conclusions table printed three times:** in the transmittal letter,
  in the salient facts and in the reconciliation.
- **Two-column summary tables** of salient facts that run across two pages.
- **A legal description and ownership history** in running text.
- **A letter with a signature block,** with the signature images removed.
- **A cover page** with the addressee block and the appraiser's logo.
