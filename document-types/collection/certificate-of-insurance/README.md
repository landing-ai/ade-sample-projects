# Certificate of insurance

**On the website:** [landing.ai/document-type/certificate-of-insurance](https://landing.ai/document-type/certificate-of-insurance)

An ACORD 25 Certificate of Liability Insurance, the standard US form a business uses to
prove it carries liability cover. This one lists the insured, the issuing broker, the
insurer, and two policies (general liability and professional liability), each with its
policy number, policy period and limits.

| | |
|---|---|
| Pages | 1 |
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
| Processed (UTC) | 2026-11-19 02:05 | 2026-11-19 02:23 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 6,531 | 6,803 |
| Words under 0.95 confidence | 70 | n/a |
| Words under 0.80 confidence | 22 | n/a |
| Words under 0.50 confidence | 13 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.7 s | 12.5 s |
| Per page | 7.7 s | 12.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.9 credits | 2.3 credits |
| Per page | 0.90 credits | 2.30 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:06 | 2026-11-19 02:23 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 24 | 25 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 85.1 s | 91.5 s |
| Per schema field (26) | 3.27 s | 3.52 s |
| Per value returned | 1.98 s | 2.08 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.8 credits | 3.9 credits |
| Per schema field (26) | 0.146 credits | 0.150 credits |
| Per value returned | 0.088 credits | 0.089 credits |

## Origin

`source/Sample_COI_2026-27.pdf` is an **ACORD 25 Certificate of Liability Insurance**
(form edition 2025/12). The American Baseball Coaches Association publishes it as proof
of coverage for its member liability program. Its broker, Sadler Insurance (a division
of Specialty Program Group), issued it on 07/29/2026. It names the ABCA as the insured
and covers the 2026-27 policy year, with Sirius American Insurance Company as insurer A.
It is **1 page, portrait (US Letter)**, created digitally with a text layer.

| | |
|---|---|
| Publisher | American Baseball Coaches Association; certificate issued by Sadler Insurance, Div of Specialty Program Group, LLC |
| Source | https://www.abca.org/common/Uploaded%20files/Membership%20Documents/Sample_COI_2026-27.pdf |
| Retrieved | 2026-10-28, downloaded by script from the publisher's site |
| Clearance | Public |

The ABCA links this certificate from its insurance page (https://www.abca.org/insurance)
as a sample of the proof of coverage members can request. It is used as published, with
no redaction. The producer box names a broker contact and gives a phone number, a fax
number and an email address, and the authorized-representative box carries a
handwritten signature. All of these were kept as the publisher filed them, by the
operator's decision. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A certificate of insurance is how one business proves to another that it carries
liability cover. The ACORD 25 is the standard form in the US, so the same layout arrives
from thousands of different brokers and insurers.

- **Commercial real estate and property management:** tenants and vendors must show
  cover before they get access to a building.
- **Construction:** general contractors collect a COI from every subcontractor before
  work starts, and again at each renewal.
- **Procurement and vendor management:** suppliers are onboarded only once their
  certificate meets the contract's minimum limits.
- **Insurance brokers and carriers:** certificates are issued, tracked and reconciled
  against the policies behind them.
- **Events, sports and education:** venues and associations, like the ABCA here, require
  certificates from members, coaches and organizers.

The task is the same everywhere: read the insurer, policy numbers, dates and limits, and
check them against a requirement.

### What it contains

- **A dense ruled grid with merged cells.** Each coverage row spans up to seven lines,
  with the policy number and dates in tall merged cells and the limits in a two-column
  label/amount ladder beside them.
- **Checkboxes that carry meaning:** occurrence or claims-made, and what the general
  aggregate limit applies per.
- **Mostly blank rows by design.** The auto, umbrella, workers compensation and
  insurer B–F rows are empty, so extraction has to skip them rather than invent values.
- **A handwritten signature** in the authorized-representative box.
- **A diagonal SAMPLE watermark** across the coverage grid.
