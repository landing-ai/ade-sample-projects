# Sanctions screening

**On the website:** [landing.ai/document-type/sanctions-screening](https://landing.ai/document-type/sanctions-screening)

A sanctions-record report from Lursoft's sanctions search for OFAC SDN entry 8279,
Viktor Anatolijevitch BOUT, a convicted arms dealer on the US sanctions list. It gives
the listing's list, program, date of publication and remark, six names and aliases with
their quality, birth data, and the lists the service checks with the date each was last
updated.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 18 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:33 | 2026-11-19 03:51 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,561 | 2,636 |
| Words under 0.95 confidence | 6 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.1 s | 6.2 s |
| Per page | 2.5 s | 3.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.6 credits | 1.7 credits |
| Per page | 0.30 credits | 0.85 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:33 | 2026-11-19 03:51 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 18 | 18 |
| Non-null fields returned | 18 | 18 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 314.7 s | 97.8 s |
| Per schema field (18) | 17.49 s | 5.43 s |
| Per value returned | 6.99 s | 2.17 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.1 credits | 2.2 credits |
| Per schema field (18) | 0.117 credits | 0.122 credits |
| Per value returned | 0.047 credits | 0.049 credits |

## Origin

`source/sanctions-screening-bout-sdn-8279.pdf` is a sanctions-record report from
Lursoft's sanctions search for OFAC SDN entry 8279, Viktor Anatolijevitch BOUT. It is
**2 pages, portrait (A4)**, generated on 2026-09-29: the listing (list, programme, date
of publication, remark), six names and aliases with their quality, birth data, and the
lists the service checks with the date each was last updated.

| | |
|---|---|
| Publisher | Lursoft IT (report); listing data from the US Treasury's Office of Foreign Assets Control (OFAC) |
| Source | [sanctions.lursoft.lv/person/boutov/SDN-8279](https://sanctions.lursoft.lv/person/boutov/SDN-8279?pdf=1) |
| Retrieved | 2026-09-29, downloaded manually |
| Clearance | Redacted (one value, not the subject's) |

Viktor Bout is a convicted arms dealer on the US sanctions list. Every listed value is
public US government data, also published by OFAC as
[SDN entry 8279](https://sanctionssearch.ofac.treas.gov/Details.aspx?id=8279), and
several sanctions-screening vendors use this same listing as their example report. The
listing is kept as printed, at the document owner's decision. The site answers scripted
requests with a Cloudflare challenge, so the PDF was downloaded by hand.

**One value was replaced, and it was not the subject's.** Lursoft prints the requester's
IP address in the header of every generated report, so the downloaded file identified
whoever downloaded it. It was replaced with `198.51.100.245`, from the RFC 5737 range
reserved for documentation, the same length as the original so the right-aligned header
still lines up, and in the header's grey. The underlying text was removed rather than
covered, and the PDF metadata was cleared. Verified: the original IP is not extractable
from the committed PDF and appears nowhere in this folder.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Sanctions screening checks customers, counterparties and payments against government
watch lists. A match produces a record like this one, which an analyst then reviews.

- **Banks and payment providers:** compliance teams screen customers and transactions
  and document how each potential match was resolved.
- **Fintech and crypto platforms:** onboarding and KYC teams screen new users against
  sanctions lists.
- **Trade, logistics and export compliance:** shippers and freight forwarders screen
  buyers, consignees and end users.
- **Insurers:** they screen policyholders and claimants before paying.
- **Law firms and due-diligence providers:** they screen counterparties in deals and
  investigations.

### What it contains

- **Label and value tables, repeated.** Six name blocks share the same labels with a
  different set of rows in each.
- **A record split by a page break.** The last alias's quality is printed alone at the
  top of page 2.
- **Status in prose.** The lists the service checks, and when each last changed, are one
  run-on paragraph.
- **Dates in a European style** (`22.09.2026.`).
- **A truncated remark** that ends mid-name, as the report prints it.
