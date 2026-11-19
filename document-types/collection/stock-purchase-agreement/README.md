# Stock Purchase Agreement

**On the website:** [landing.ai/document-type/stock-purchase-agreement](https://landing.ai/document-type/stock-purchase-agreement)

A 2005 joint application to the Kentucky Public Service Commission for approval of a
transfer of stock, with the executed Stock Purchase Agreement as an exhibit. Under the
agreement, Hydro Star, LLC buys all 1,000 shares of Nuon Global Solutions USA Inc., the
parent of a water and wastewater utility holding company, for $192,500,000. It sets out
the parties, price, closing, guarantees, termination terms and signatures.

| | |
|---|---|
| Pages | 78 |
| Fields in the extraction schema | 31 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:55 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 192,660 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 43.7 s |
| Per page | 0.6 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 87.2 credits |
| Per page | 1.12 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:56 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 31 |
| Non-null fields returned | 31 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 140.0 s |
| Per schema field (31) | 4.51 s |
| Per value returned | 3.59 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 40.9 credits |
| Per schema field (31) | 1.319 credits |
| Per value returned | 1.049 credits |

## Origin

`source/stock-purchase-agreement-hydro-star-nuon.pdf` is a joint application to the
Kentucky Public Service Commission (Case No. 2005-00323) asking for approval of a
transfer of stock. Exhibit 3 is the executed **Stock Purchase Agreement** dated as of
May 14, 2005, under which Hydro Star, LLC buys all 1,000 shares of Nuon Global Solutions
USA Inc., the parent of the water and wastewater utility holding company Utilities,
Inc., from Nuon Global Solutions USA B.V. for $192,500,000. It is **78 pages,
portrait**, an Acrobat Paper Capture scan with a text layer on page 1 only.

The filing is in three parts: the cover letter, application and verifications (pages
1–30), the SPA (pages 31–75: cover, 42 numbered pages of terms, signature pages 74–75)
and later exhibits (76–78).

| | |
|---|---|
| Publisher | Kentucky Public Service Commission (filed by Nuon Global Solutions USA B.V. and Hydro Star, LLC as joint applicants) |
| Source | [psc.ky.gov, NHW_App_080205.pdf](https://psc.ky.gov/PSCSCF/2005%20cases/2005-00323/NHW_App_080205.pdf) |
| Case | Kentucky PSC Case No. 2005-00323 |
| Retrieved | 2026-10-28, by script |
| Clearance | Public |

This is a public regulatory filing, downloaded from the Commission's official case-file
server. **The operator decided explicitly to publish it as filed, without redaction.**
That departs from the collection's usual rule that personal data is replaced before
parsing. The filing names corporate officers, attorneys and company contacts, and
carries their wet signatures, phone and fax numbers, notary seals and a personnel table.
Every one of them appears in a professional or corporate capacity in a document the
Commission publishes. None of it was replaced.

The one change from the filed PDF: **the hidden /Info and XMP metadata was cleared**
(Acrobat Paper Capture creator and the 2005 creation and modification dates). Every
page's content stream is byte-identical to the filed file. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A stock purchase agreement is the contract by which a buyer acquires a company's shares.
It fixes the parties, the price, the conditions for closing and what happens if the deal
fails.

- **M&A legal:** deal lawyers draft, negotiate and later review SPAs for price,
  guarantees, termination rights and governing law.
- **Private equity and corporate development:** deal teams track the terms of
  acquisitions across a portfolio.
- **Regulators:** utility commissions and other agencies review the agreement when a
  change of control needs approval, as here.
- **Due diligence and contract management:** reviewers extract key terms from executed
  agreements into contract databases.
- **Lenders and investors:** acquisition lenders and analysts read the price, payment
  method and guarantees behind a deal.

### What it contains

- **A raster scan.** Only page 1 has any text layer, so every value has to be read from
  the image.
- **Long legal prose.** Values sit mid-sentence in defined-term paragraphs, such as
  `("Seller")` and `(the "Purchase Price")`.
- **A contract wrapped in a filing.** The SPA is an exhibit inside a 78-page
  application, which restates some of its terms in summary.
- **Values that break across lines,** such as the closing location and a parent
  guarantor's name.
- **Deadlines defined in words,** such as an outside date set as twelve months after
  the last regulatory filing.
- **Signature pages, wet signatures and notary seals,** plus a personnel table in the
  application.
