# Trademark registration certificate

**On the website:** [landing.ai/document-type/trademark-registration-certificate](https://landing.ai/document-type/trademark-registration-certificate)

The USPTO registration certificate for U.S. Reg. No. 5,886,375, the AMERICAN NINJA
WARRIOR shield design mark, registered October 15, 2019 in International Class 21. It
gives the registration and serial numbers, the owner, the goods, first-use dates, the
description of the mark and its drawing, and a second page on the filings needed to keep
the registration in force.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 25 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:39 | 2026-11-19 03:56 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 4,428 | 4,860 |
| Words under 0.95 confidence | 16 | n/a |
| Words under 0.80 confidence | 10 | n/a |
| Words under 0.50 confidence | 8 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.1 s | 8.2 s |
| Per page | 2.5 s | 4.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.8 credits | 2.3 credits |
| Per page | 0.40 credits | 1.15 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:39 | 2026-11-19 03:56 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 25 | 25 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 198.0 s | 54.2 s |
| Per schema field (25) | 7.92 s | 2.17 s |
| Per value returned | 8.25 s | 2.26 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.5 credits | 2.6 credits |
| Per schema field (25) | 0.100 credits | 0.104 credits |
| Per value returned | 0.104 credits | 0.108 credits |

## Origin

`source/uspto-reg-5886375-registration-certificate.pdf` is the USPTO registration
certificate for U.S. Reg. No. 5,886,375, the AMERICAN NINJA WARRIOR shield design mark,
registered October 15, 2019 in International Class 21. It is **2 pages, portrait, A4**.
Page 1 is the certificate, and page 2 is the USPTO's standard statement of the filings
needed to keep the registration alive. Both are kept, as the request asked.

The pages are mixed-layer. The text is a real text layer, while the blackletter "United
States of America" banner, the mark itself, the USPTO seal and the Director's signature
are images.

| | |
|---|---|
| Publisher | United States Patent and Trademark Office |
| Source | [tmng-al.uspto.gov/…/5886375_87981735_101519_ORC.pdf](https://tmng-al.uspto.gov/resting2/api/casedoc/cms/case/87981735/registration-certificate/5886375_87981735_101519_ORC.pdf) |
| File record | [TSDR, serial 87981735](https://tsdr.uspto.gov/#caseNumber=87981735&caseType=SERIAL_NO&searchType=documentSearch) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

Trademark registrations and their file histories are public records, published by the
USPTO in TSDR. This is the "Registration Certificate" document in that file. The owner
is a corporation, Tokyo Broadcasting System Television, Inc. The only personal element
is the facsimile signature of the USPTO Director, a public official, which appears on
every certificate of the period. It is kept, and no redaction was made. The PDF metadata
holds only the PD4ML creator and producer and a creation date. The mark is a well-known
third-party television brand logo, shown here as part of the public record. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A registration certificate is the official proof that a trademark is registered, who
owns it and for which goods or services. It travels with the brand through licensing,
sales and disputes.

- **Trademark attorneys and IP firms:** they docket registration dates and maintenance
  deadlines and file the certificates as evidence of rights.
- **Brand owners and licensing teams:** they track their portfolio by registration
  number, class and goods.
- **E-commerce marketplaces:** brand registry programs ask sellers for a registration to
  prove they own a brand.
- **M&A and IP due diligence:** buyers verify ownership, status and coverage of the
  trademarks they acquire.
- **Customs and anti-counterfeiting:** rights holders record registrations so that
  infringing goods can be stopped.

### What it contains

- **Two columns that are not a table.** Bold left-column labels ("Reg. No.", "Int. Cl.",
  "Principal Register") sit beside a right column of prose, with no rules between them.
- **Values inside prose.** The serial number and filing date share one line, the
  first-use dates share another, and the disclaimer is a quoted word at the end of a
  sentence.
- **The mark as an image,** described in words in a separate paragraph.
- **A blackletter banner, a seal and a facsimile signature** as images.
- **A second page of boilerplate** whose deadlines are relative to a date on page 1.
