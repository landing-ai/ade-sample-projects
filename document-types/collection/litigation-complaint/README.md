# Litigation complaint

**On the website:** [landing.ai/document-type/litigation-complaint](https://landing.ai/document-type/litigation-complaint)

The Justice Department's complaint in United States of America v. Hewlett Packard
Enterprise Co. and Juniper Networks, Inc., filed in the Northern District of California
on January 30, 2025, to block HPE's $14 billion acquisition of Juniper. It sets out the
parties, the transaction, the markets it would affect, the legal claims and the relief
the government seeks, in numbered paragraphs on pleading paper.

| | |
|---|---|
| Pages | 21 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:16 | 2026-11-19 03:32 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 49,864 | 49,949 |
| Words under 0.95 confidence | 204 | n/a |
| Words under 0.80 confidence | 179 | n/a |
| Words under 0.50 confidence | 87 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.3 s | 14.5 s |
| Per page | 0.5 s | 0.7 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.2 credits | 23.0 credits |
| Per page | 0.39 credits | 1.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:16 | 2026-11-19 03:33 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 233.3 s | 92.3 s |
| Per schema field (23) | 10.14 s | 4.01 s |
| Per value returned | 8.33 s | 3.30 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.8 credits | 11.9 credits |
| Per schema field (23) | 0.513 credits | 0.517 credits |
| Per value returned | 0.421 credits | 0.425 credits |

## Origin

`source/us-v-hpe-juniper-complaint.pdf` is the complaint in *United States of America v.
Hewlett Packard Enterprise Co. and Juniper Networks, Inc.*, No. 3:25-cv-00951 (N.D.
Cal.), the Justice Department's suit to block HPE's $14 billion acquisition of Juniper.
It is **21 pages, portrait (612×792)**, produced from Word with a full text layer, on
28-line numbered pleading paper, with the court's ECF filing stamp across the top of
every page.

| | |
|---|---|
| Publisher | U.S. Department of Justice, Antitrust Division |
| Source | [justice.gov/atr/media/1406591/dl](https://www.justice.gov/atr/media/1406591/dl?inline) |
| Linked from | [US v. Hewlett Packard Enterprise Co. and Juniper Networks, Inc.](https://www.justice.gov/atr/case/us-v-hewlett-packard-enterprise-co-and-juniper-networks-inc), as "Complaint (January 30, 2025)" |
| Filed | 2025-01-30 |
| Retrieved | 2026-10-28, downloaded by script |
| Clearance | Public |

This is a U.S. government work, published by the DOJ on its case page. It is used
**exactly as published, all 21 pages, unredacted**, by decision of the document owner.
The only individuals it names are the government attorneys of record, in their official
capacity: counsel and their bar numbers, an office email, telephone and fax on page 1,
and the signature block with an `/s/` e-signature on page 21. The body was screened for
named company executives: they are referred to by title only ("Senior Vice President of
Worldwide Sales"), never by name. The PDF metadata is left as published. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A complaint is the document that starts a civil lawsuit. It names the court and the
parties, states the facts and legal claims, and says what relief the plaintiff wants.

- **Law firms and in-house legal:** litigators and legal teams read new complaints to
  assess claims, deadlines and exposure.
- **Litigation support and e-discovery:** teams index pleadings by court, case number,
  parties and claims.
- **Legal research and court data providers:** services collect filings to track cases,
  judges and litigation trends.
- **Insurance:** liability and D&O insurers review complaints to decide coverage and
  set reserves.
- **Compliance, M&A and investors:** deal teams and analysts follow antitrust challenges
  to pending transactions like this one.

### What it contains

- **Pleading paper.** Line numbers down the left margin, a ruled border and a footer
  title on every page, all separate from the pleading text.
- **An ECF filing stamp** across the top of every page, with the case number and filed
  date.
- **A side-by-side caption.** The parties sit in a ruled box on the left, the case
  number and title on the right. The caption's case-number box is blank, as it is on
  any complaint at filing, so the number appears only in the court's stamp.
- **Mostly prose.** After page 1 the facts are numbered paragraphs, so statutes,
  markets and relief have to be found in sentences.
- **Legal citations** with section symbols (`§`) and lettered requests for relief.
- **An electronic `/s/` signature** in the signature block.
