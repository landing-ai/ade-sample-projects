# Wind mitigation inspection

**On the website:** [landing.ai/document-type/wind-mitigation-inspection](https://landing.ai/document-type/wind-mitigation-inspection)

A completed Florida Uniform Mitigation Verification Inspection Form, OIR-B1-1802, the
state form insurers accept as evidence for windstorm premium discounts. It covers a
one-storey 1999 home in Brevard County, inspected in July 2026. It records the building
code, roof covering, roof deck and roof-to-wall attachments, roof geometry, secondary
water resistance and opening protection, with the inspector's details and signatures.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 45 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 03:59 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 24,307 | 25,539 |
| Words under 0.95 confidence | 83 | n/a |
| Words under 0.80 confidence | 43 | n/a |
| Words under 0.50 confidence | 17 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.1 s | 23.7 s |
| Per page | 1.0 s | 4.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.4 credits | 9.4 credits |
| Per page | 0.57 credits | 1.57 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 04:00 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 45 | 45 |
| Non-null fields returned | 41 | 40 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 220.5 s | 126.4 s |
| Per schema field (45) | 4.90 s | 2.81 s |
| Per value returned | 5.38 s | 3.16 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.3 credits | 6.8 credits |
| Per schema field (45) | 0.140 credits | 0.151 credits |
| Per value returned | 0.154 credits | 0.170 credits |

## Origin

`source/surehome-oir-b1-1802-wind-mitigation-sample.pdf` is a completed Florida **Uniform
Mitigation Verification Inspection Form, OIR-B1-1802 (Rev. 04/26)**, the state form
insurers accept as evidence for windstorm premium discounts. It covers a one-storey 1999
home in Brevard County, inspected July 29, 2026. It is **6 pages, portrait**, with a text
layer.

| | |
|---|---|
| Publisher | SureHome of Brevard (licensed Florida home inspection company, Melbourne FL) |
| Source | [surehomes.org/samples/sample-wind-mitigation.pdf](https://www.surehomes.org/samples/sample-wind-mitigation.pdf) |
| Retrieved | 2026-10-04 |
| Clearance | Public |

SureHome's home page links this file as "Sample PDF - Wind Mitigation: The signed
OIR-B1-1802" and states that "Sample reports use fictional client and property details."
The owner and street address are those fictional details. The inspector's name, licence
number, company phone, initials and signature appear in a professional capacity on the
company's own marketing sample. Downloaded directly; no redaction was needed.

The published file has 11 pages. It was trimmed to pages 2–7, the six-page state form:
page 1 is a branded cover with a photo of a house, and pages 8–11 are inspection photos.
Document metadata was cleared. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Florida insurers must offer windstorm premium discounts for homes with qualifying
construction features, and this form is the evidence for them.

- **Homeowners insurance carriers:** underwriters apply wind mitigation credits to the
  premium from the answers on the form.
- **Insurance agents:** they collect the form from the homeowner or inspector and submit
  it with the application or renewal.
- **Home inspection companies:** inspectors complete and sign the form, often alongside
  a four-point inspection.
- **Reinsurance and catastrophe modeling:** analysts use the construction attributes to
  assess a portfolio's exposure to hurricanes.
- **Real estate transactions:** buyers order the inspection to estimate insurance costs
  before closing.

### What it contains

- **Answers given as checkmarks, not text.** Nine questions, each answered by marking
  one lettered option, with nested sub-options under several of them.
- **Marks drawn as separate glyphs:** each "X" sits beside an empty box glyph rather than
  filling it.
- **A matrix of marks:** the Opening Protection Level Chart is a grid of opening types
  against protection levels, filled with Xs.
- **Sparse checkbox tables,** such as the roof covering table with one row marked.
- **Typed values on a pre-printed form:** dates, year built, stories, roof perimeter,
  inspector licence and company.
- **Blank fields,** such as insurance company and policy number.
- **Inspector initials and signatures.**
