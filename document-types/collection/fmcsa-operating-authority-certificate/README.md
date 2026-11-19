# FMCSA Operating Authority Certificate

**On the website:** [landing.ai/document-type/fmcsa-operating-authority-certificate](https://landing.ai/document-type/fmcsa-operating-authority-certificate)

Twenty operating authority documents the Federal Motor Carrier Safety Administration
issued on February 16, 2023. Each is a one-page certificate or permit that grants a
motor carrier interstate operating authority under an MC docket number. It names the
holder and its city, prints its U.S. DOT number and the authority granted, and carries
the signature of the FMCSA official who issued it.

| | |
|---|---|
| Pages | 20 |
| Fields in the extraction schema | 15 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 | 2026-11-19 03:04 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 26,551 | 26,587 |
| Words under 0.95 confidence | 0 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 11.9 s | 15.0 s |
| Per page | 0.6 s | 0.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.7 credits | 16.7 credits |
| Per page | 0.29 credits | 0.83 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:00 | 2026-11-19 03:04 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 15 | 15 |
| Non-null fields returned | 15 | 15 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 160.7 s | 167.6 s |
| Per schema field (15) | 10.71 s | 11.18 s |
| Per value returned | 0.71 s | 0.75 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 13.4 credits | 13.3 credits |
| Per schema field (15) | 0.893 credits | 0.887 credits |
| Per value returned | 0.059 credits | 0.060 credits |

## Origin

`source/fmcsa-authority-certificates-2023-02-16-excerpt.pdf` holds twenty operating
authority documents issued by the Federal Motor Carrier Safety Administration on one
day. Each is a one-page certificate or permit granting a motor carrier interstate
operating authority under an MC docket number and printing its U.S. DOT number. It is
**20 pages, portrait (612×792)**, with a text layer throughout (Oracle Reports output),
plus the USDOT logo and the signing official's signature as images on every page.

| | |
|---|---|
| Publisher | U.S. Department of Transportation, Federal Motor Carrier Safety Administration, Office of Registration |
| Source | [li-public.fmcsa.dot.gov/…/LI_CPL20230216.PDF](https://li-public.fmcsa.dot.gov/lihtml/rptspdf/LI_CPL20230216.PDF) |
| Title | FMCSA Licensing & Insurance daily report of issued operating authority documents, service date February 16, 2023 |
| Retrieved | 2026-10-25 |
| Clearance | Public |

FMCSA posts each day's batch of issued authority documents in its own Licensing &
Insurance public report folder, so the URL is the publisher. It is a U.S. federal
government work. It was downloaded by script.

The source is 768 pages, alternating an authority document with a mailing-envelope page.
This folder keeps 20 of them, the odd-numbered source pages 33 to 71. The even-numbered
pages in that range were dropped because they are envelope pages printing each
carrier's business street address.

Every kept page was checked by eye for personal data. Each holder is a business (an LLC,
an Inc., or a trade name), and none is a sole proprietor trading under a personal name.
The only individual named is the FMCSA Division Chief who signs every document in an
official capacity; his printed name and image signature are kept as published. Nothing
was redacted. The document metadata was cleared when the pages were split out.

The carriers are real companies, and their authority status may have changed since
February 2023. These pages show what was issued that day, not current status.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A motor carrier needs FMCSA operating authority to haul regulated freight or passengers
across state lines. The certificate is its proof, and anyone who hires or covers a
carrier asks for it.

- **Freight brokers and 3PLs:** they verify a carrier's authority and DOT number before
  tendering a load.
- **Shippers:** they confirm that the carriers they hire are authorized for the freight.
- **Commercial auto insurers:** underwriters check the authority type and docket number
  when writing a trucking policy.
- **Factoring companies and equipment lenders:** they confirm a carrier is active
  before buying its invoices or financing trucks.
- **Compliance and carrier-onboarding services:** they collect and monitor authority
  documents for large carrier networks.

### What it contains

- **One record per page, many pages.** The file is a batch of 20 separate certificates
  and permits.
- **Small variations inside a fixed template:** a household-goods certificate with extra
  tariff and arbitration requirements, a contract-carrier permit with a
  continuing-agreement condition, holders with a D/B/A line that pushes the city down a
  line, and a holder in Quebec.
- **Values set apart by layout, not labels.** The service date sits alone at top right,
  and the docket number, DOT number, holder and city form an unlabeled centered stack.
- **Key terms in bold inside a sentence,** such as the authority granted.
- **An agency logo and an image signature** on every page.
