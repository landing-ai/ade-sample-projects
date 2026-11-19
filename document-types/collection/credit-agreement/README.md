# Credit Agreement

**On the website:** [landing.ai/document-type/credit-agreement](https://landing.ai/document-type/credit-agreement)

A revolving credit agreement under which Truist Bank and STI Institutional &
Government, Inc. lend up to $100,000,000 to the Hillsborough County Aviation Authority,
which runs Tampa International Airport, with Truist Bank as agent. It is the execution
copy, dated as of April 20, 2020, and runs from definitions and the commitment through
covenants and events of default to a signature page and exhibits.

| | |
|---|---|
| Pages | 76 |
| Fields in the extraction schema | 26 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:45 | 2026-11-19 02:50 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 219,661 | 218,577 |
| Words under 0.95 confidence | 179 | n/a |
| Words under 0.80 confidence | 90 | n/a |
| Words under 0.50 confidence | 36 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 59.4 s | 53.9 s |
| Per page | 0.8 s | 0.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 33.4 credits | 92.7 credits |
| Per page | 0.44 credits | 1.22 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:46 | 2026-11-19 02:52 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 26 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 345.0 s | 240.6 s |
| Per schema field (26) | 13.27 s | 9.25 s |
| Per value returned | 11.13 s | 7.76 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 45.4 credits | 45.2 credits |
| Per schema field (26) | 1.746 credits | 1.738 credits |
| Per value returned | 1.465 credits | 1.458 credits |

## Origin

`source/hcaa-revolving-credit-agreement-2020.pdf` is the execution copy of a revolving
credit agreement, dated as of April 20, 2020, among the Hillsborough County Aviation
Authority, Truist Bank and STI Institutional & Government, Inc., with Truist Bank as
agent. The facility is up to $100,000,000 and is drawn through two subordinated revenue
notes, Series 2020A (tax-exempt) and Series 2020B (taxable). It is **76 pages, portrait
(612×792)**: cover and table of contents, then the agreement (pages 6–50: definitions,
the commitment, interest and fees, conditions, covenants, events of default and
miscellaneous provisions), a scanned signature page with the Authority's seal (page 51),
and exhibits (pages 52–76): the two forms of note, advance requests, certificates and
the form of authorizing resolution.

| | |
|---|---|
| Publisher | Hillsborough County Aviation Authority (Tampa International Airport) |
| Source | [tampaairport.com, document 2020-67](https://tampaairport.com/sites/default/master/files/2020-67%20-%20HCAA%20Revolving%20Credit%20Agreement%20-%20April%2020,%202020.pdf) |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

The Authority, a Florida special district, is the borrower. It publishes the executed
agreement on its own website as document 2020-67, a public record of a public body. The
same site also posts the later Amendment Two and the board minutes that discuss the
facility.

The agreement names some people: Authority officers and a staff member, and a bank
officer. They appear in the signature blocks, on the signature page (wet-ink signatures,
on a scan) and in the notice addresses on page 13 (work email addresses and phone
numbers). **The operator chose to keep these names, signatures and contact details
exactly as the Authority published them.** No visible content was changed. The only
change was clearing the hidden PDF metadata, which held the Word file name and a
document author username. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A credit agreement sets the terms of a loan facility: who lends, how much, at what rate,
and what the borrower must do to keep it. Each economic term usually sits in its own
definition, far from the others.

- **Commercial and public-finance banking:** credit officers and agents track
  commitments, margins, fees and covenants across their loan book.
- **Municipal and public-sector finance:** issuers, financial advisors and bond counsel
  manage bank facilities alongside outstanding bonds.
- **Legal:** lawyers review defined terms, conditions, events of default and governing
  law during negotiation, amendment and disputes.
- **Credit rating and investment analysis:** analysts read bank facilities to assess a
  borrower's liquidity and debt obligations.
- **Loan administration and operations:** teams set up the facility's rates, fees and
  notice details in servicing systems.

### What it contains

- **Long-form legal prose** with defined terms and cross-referenced sections, so a
  term's value can sit many pages from where it is used.
- **Economic terms spread across the document,** such as the facility size on page 12,
  the margin on page 7, and the unused fee and minimum advance on page 32.
- **A table of contents** and numbered articles and sections.
- **A scanned signature page** inside a text-layer document, at low resolution, with
  wet-ink signatures crossing printed names.
- **The Authority's seal** on the signature page.
- **Exhibits with blank forms** of notes, requests and certificates.
