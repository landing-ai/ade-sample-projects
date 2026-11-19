# MCS-90 endorsement

**On the website:** [landing.ai/document-type/mcs-90-endorsement](https://landing.ai/document-type/mcs-90-endorsement)

A completed FMCSA Form MCS-90, the endorsement that adds federally required public
liability cover to a motor carrier's insurance policy. Northland Insurance Company
issued it to BCT, Inc. in November 2024. It names the carrier, the insurer and the
policy it amends, states whether the cover is primary or excess and its limit, and ends
with the Schedule of Limits.

| | |
|---|---|
| Pages | 3 |
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
| Processed (UTC) | 2026-11-19 03:19 | 2026-11-19 03:36 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 9,690 | 10,404 |
| Words under 0.95 confidence | 11 | n/a |
| Words under 0.80 confidence | 5 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.5 s | 13.9 s |
| Per page | 3.5 s | 4.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.5 credits | 4.2 credits |
| Per page | 0.50 credits | 1.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:19 | 2026-11-19 03:36 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 22 | 22 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 109.3 s | 110.5 s |
| Per schema field (26) | 4.21 s | 4.25 s |
| Per value returned | 3.53 s | 3.56 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 4.5 credits | 4.6 credits |
| Per schema field (26) | 0.173 credits | 0.177 credits |
| Per value returned | 0.145 credits | 0.148 credits |

## Origin

`source/mcs-90-endorsement.pdf` is a completed FMCSA **Form MCS-90**, *Endorsement for
Motor Carrier Policies of Insurance for Public Liability under Sections 29 and 30 of the
Motor Carrier Act of 1980* (Rev 5/26/2023). Northland Insurance Company issued it to BCT,
Inc., the for-hire motor carrier subsidiary of Boise Paper (Packaging Corporation of
America), dated 21 November 2024 with an effective date of 11/01/2024. It is **3 pages,
portrait (US Letter)**, with a text layer:

1. The endorsement: carrier and state, where and when it was dated, the amending policy
   number and effective date, the insurer, the countersignature, the primary/excess
   checkbox with its limit, and the FMCSA verification phone number.
2. Definitions and the operative wording of the endorsement.
3. The Schedule of Limits for public liability, by type of carriage.

| | |
|---|---|
| Publisher | Boise Paper (Packaging Corporation of America), for BCT, Inc.; issued by Northland Insurance Company |
| Source | https://www.boisepaper.com/wp-content/uploads/2025/09/BCT-Owner-Oper-MCS-90.pdf |
| Linked from | [boisepaper.com/our-company/bct-inc-2/](https://www.boisepaper.com/our-company/bct-inc-2/) |
| Retrieved | 2026-10-25, downloaded by script from the publisher's site |
| Clearance | Public |

Boise Paper links this PDF as "MCS-90" on its BCT, Inc. company page, beside BCT's
operating authority, W-9 and SmartWay certificate: a carrier packet published for
shippers and brokers. It is used as published, with no redaction. It carries business
data only: the carrier, the insurer, a policy number and the insurer's verification
line. The countersignature is a handwritten mark by an unnamed insurer representative and
was kept, by the operator's decision. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

The MCS-90 guarantees that a for-hire motor carrier's insurer will pay public liability
claims up to the federal minimum, so it travels with the carrier's operating authority.

- **Freight brokers and shippers:** they check a carrier's MCS-90 during onboarding to
  confirm the insurer, policy and limit before tendering loads.
- **Commercial auto insurers:** underwriters issue the endorsement and track it against
  the policy it amends.
- **Insurance agents and brokers:** they file and renew MCS-90s for trucking clients.
- **Carrier compliance and fleet management:** carriers keep it in the packet they send
  to customers, as BCT does here.
- **Claims and litigation:** after a crash, claimants and attorneys use it to find the
  insurer obligated to pay.

### What it contains

- **A federal form whose values are typed onto underlines,** inline in running text
  rather than in ruled boxes.
- **Two label/value pairs sharing one line,** twice: the "Dated at" line and the
  "Amending Policy Number ... Effective Date" line.
- **A checkbox choice between two sentences,** primary or excess, each with its own
  amount blanks.
- **Empty boxes at source:** the USDOT Number and Date Received boxes are blank.
- **A handwritten countersignature.**
- **A ruled Schedule of Limits** with four rows by type of carriage.
