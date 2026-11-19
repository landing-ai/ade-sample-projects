# Quality of Earnings Report

**On the website:** [landing.ai/document-type/quality-of-earnings-report](https://landing.ai/document-type/quality-of-earnings-report)

A sample Quality of Earnings report dated February 2025, prepared by the CPA firm QOE
Prep on a fictional fixed-wireless internet provider. It is a slide deck covering key
findings, the bridge from reported to adjusted EBITDA with commentary on each
adjustment, P&L and revenue trends, vendor analysis, net working capital, cash
conversion and proof-of-cash reconciliations.

| | |
|---|---|
| Pages | 25 |
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
| Processed (UTC) | 2026-11-19 03:27 | 2026-11-19 03:47 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 53,036 | 52,853 |
| Words under 0.95 confidence | 150 | n/a |
| Words under 0.80 confidence | 45 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 11.1 s | 21.8 s |
| Per page | 0.4 s | 0.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.1 credits | 25.8 credits |
| Per page | 0.36 credits | 1.03 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:27 | 2026-11-19 03:48 |
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
| Total | 317.9 s | 126.5 s |
| Per schema field (26) | 12.23 s | 4.87 s |
| Per value returned | 3.46 s | 1.38 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 14.4 credits | 14.4 credits |
| Per schema field (26) | 0.554 credits | 0.554 credits |
| Per value returned | 0.157 credits | 0.157 credits |

## Origin

`source/qoe-prep-sample-report.pdf` is a sample Quality of Earnings (QoE) report dated
February 2025, published by QOE Prep, a CPA firm. It is **25 pages, landscape
(792×612)**, a PowerPoint deck printed to PDF with a full text layer. It covers a
fictional fixed-wireless internet provider: key findings, the EBITDA bridge, P&L and
revenue trends, vendor analysis, net working capital, cash conversion and proof-of-cash
reconciliations.

| | |
|---|---|
| Publisher | QOE Prep (Caleb PA Basile, LLC) |
| Source | [img1.wsimg.com/…/Sample report - Qoe Prep 12.4.pdf](https://img1.wsimg.com/blobby/go/2975c323-0167-4a10-81f0-60981f4243c3/Sample%20report%20-%20Qoe%20Prep%2012.4.pdf) |
| Linked from | qoeprep.com/sample |
| Retrieved | 2026-10-28, by script |
| Clearance | Redacted (one page dropped) |

The publisher distributes this as a public sample, and its cover states that all figures
are fictional. The target company, its owners and staff are already anonymized in the
document (`XXXX`, "Company 2", "Vendor 1"). The only real person named in the report is
the publisher's own principal, as signatory of the cover letter and contact on the
closing page. He is named in his professional capacity, so his name is kept.

**One page was removed.** The original page 2, "Happy Customers", was a set of
screenshot Google reviews naming eight private reviewers, one with a profile photo. It is
publisher marketing, not part of the report, and the names were in images, so no text
rule could reach them. The page was dropped, and the PDF metadata was cleared. No text
was replaced. The folder was swept for the reviewers' names afterwards and none appear.
Because of the drop, every PDF page number here is one lower than the "Page N" footer
printed on the slide.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A Quality of Earnings report is the core financial-diligence deliverable in the sale of
a private company. It restates the seller's earnings into an adjusted EBITDA that the
price is negotiated on.

- **Private equity and search-fund buyers:** they use the adjusted EBITDA and its
  adjustments to set and defend their offer.
- **M&A lenders:** acquisition lenders size debt on the adjusted figures and read the
  rationale for each add-back.
- **Sellers and their advisers:** sell-side QoEs prepare a company for market and
  answer buyer questions in advance.
- **Accounting and transaction advisory firms:** they prepare QoE reports and compare
  them across engagements.
- **Representations and warranties insurers:** underwriters review the diligence before
  binding a deal policy.

### What it contains

- **A slide deck in landscape,** with an analyst's argument built on tables and the
  reasoning in prose beside them.
- **Table on the left, commentary on the right.** The EBITDA bridge pairs a dense ruled
  table with a panel explaining each adjustment.
- **The same table printed twice,** on consecutive pages with different commentary.
- **A units trap.** The table header says `In $000's`, but the figures are whole dollars.
- **Dashes for zero and parentheses for negatives** in the financial tables.
- **Figures stated in prose** as `$764K` or `($297K)` alongside the tables.
- **Totals that do not quite reconcile,** with one-dollar rounding differences in the
  source.
