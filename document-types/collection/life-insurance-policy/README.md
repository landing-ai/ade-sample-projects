# Life insurance policy

**On the website:** [landing.ai/document-type/life-insurance-policy](https://landing.ai/document-type/life-insurance-policy)

Pacific Life's specimen of an issued annual renewable term life insurance policy:
$500,000 of cover to age 95, convertible, with a premium waiver rider. The cover gives
the policy data, the specification pages carry the guaranteed premium tables for each
policy year, and the rest sets out the contract provisions, such as the grace period,
reinstatement and incontestability.

| | |
|---|---|
| Pages | 14 |
| Fields in the extraction schema | 39 |

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
| Characters returned | 26,093 | 27,189 |
| Words under 0.95 confidence | 91 | n/a |
| Words under 0.80 confidence | 56 | n/a |
| Words under 0.50 confidence | 28 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.9 s | 12.4 s |
| Per page | 0.6 s | 0.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.8 credits | 13.8 credits |
| Per page | 0.34 credits | 0.99 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:16 | 2026-11-19 03:32 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 39 | 39 |
| Non-null fields returned | 39 | 39 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 304.9 s | 138.0 s |
| Per schema field (39) | 7.82 s | 3.54 s |
| Per value returned | 1.42 s | 0.64 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 10.3 credits | 10.6 credits |
| Per schema field (39) | 0.264 credits | 0.272 credits |
| Per value returned | 0.048 credits | 0.049 credits |

## Origin

`source/pacific-life-term-art-sample-policy.pdf` is Pacific Life's specimen of an issued
**annual renewable term life insurance policy** (product PAC ART, policy form P08TRM):
$500,000 of cover to age 95, convertible, non-participating, with a premium waiver
rider. It is **14 pages, portrait**, born-digital with a text layer. Page 1 is the cover
with the policy data block, pages 3–7 are the policy specifications and the guaranteed
premium tables, pages 8–13 are the contract provisions and index, and page 14 is the
back cover. Page 2 is intentionally blank. Every data page carries a red SAMPLE stamp.

| | |
|---|---|
| Publisher | Pacific Life Insurance Company |
| Source | [pacificlife.com/…/Sample Policy_Term ART.pdf](https://www.pacificlife.com/content/dam/paclife/lid/public/sample-policies/Sample%20Policy_Term%20ART.pdf) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

The carrier publishes this file on its own domain, in a `public` sample-policies asset
folder that also holds its other sample policies. No HTML page linking it was found; the
carrier-owned URL is the provenance of record.

It is the carrier's own specimen, not a customer's policy. The insured and owner are a
19th-century historical figure used as a placeholder, and the policy number is a dummy.
The two officer signatures on page 1 are the corporate signatures printed on the
carrier's policy forms. No redaction was needed. All 14 pages are kept as published;
only the PDF's document metadata was cleared, because it carried an author username.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A life insurance policy is the contract that defines the cover, its cost over time and
the conditions for paying a claim. It is read long after it is issued.

- **Life insurance carriers:** policy administration and claims teams check face amount,
  riders, premiums and provision periods.
- **Insurance agents and brokers:** they review in-force policies when advising on
  replacement or conversion.
- **Lenders:** banks taking a collateral assignment of a policy confirm the face amount,
  owner and policy number.
- **Life settlement and policy review services:** they read premium schedules and
  conversion dates to value a policy.
- **Estate planning and financial advisory:** advisors and attorneys check the cover,
  ownership and term when planning an estate.

### What it contains

- **A two-column data block** on the cover, with label-value pairs side by side.
- **Long premium tables that continue across pages:** 60 policy years over two pages
  plus a 30-year rider table on a third, with right-aligned figures and a dollar sign on
  the first row only.
- **Terms stated once in running prose,** such as the grace period, reinstatement window
  and incontestability and suicide exclusion periods, across six pages of provisions.
- **Figures that reconcile,** such as the monthly premium computed from the annual
  premiums and a modal factor.
- **Bracketed variable text** such as "[20]" days and "[MONTHLY]".
- **A red SAMPLE stamp** on every data page and two printed officer signatures.
