# Client Risk Profile (Handwritten)

**On the website:** [landing.ai/document-type/client-risk-profile-handwritten](https://landing.ai/document-type/client-risk-profile-handwritten)

Wells Fargo Advisors' Client Profile/Risk Assessment questionnaire, filled in by hand
with invented data and scanned. It has the client's contact details and twelve
risk-tolerance questions, from age band and time horizon to total assets and income
stability. Most answers are ticked checkboxes, with handwritten write-ins beside a few.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 26 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 9,017 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 16.1 s |
| Per page | 4.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 4.3 credits |
| Per page | 1.07 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 26 |
| Non-null fields returned | 25 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 176.9 s |
| Per schema field (26) | 6.80 s |
| Per value returned | 7.07 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.5 credits |
| Per schema field (26) | 0.096 credits |
| Per value returned | 0.100 credits |

## Origin

`source/wells-fargo-client-profile-risk-assessment-handwritten.pdf` is Wells Fargo
Advisors' **Client Profile/Risk Assessment** questionnaire, **filled in by hand** and
scanned. It has two parts: the client's contact details (name, phone, address and
email), and twelve risk-tolerance questions covering age band, time horizon, investment
purpose, risk acceptance, preferred portfolio, tolerable drawdown, a hypothetical return
table, income needs, experience, share of assets, total assets and income stability. It
is **4 pages, portrait**, raster scans with no text layer.

| | |
|---|---|
| Publisher | LandingAI; the form itself is Wells Fargo Advisors' questionnaire |
| Source | Not published online. A specimen filled in by hand by LandingAI staff, from LandingAI's internal marketing document library (doc38) |
| Retrieved | 2026-11-16 |
| Clearance | Public |

A LandingAI staff member filled in the blank questionnaire by hand with **invented
data**, in blue pen, and scanned it. The client's name, address, phone number (the 555
range), email address and every answer are fictitious. No real client's data is present,
so nothing was redacted. The PDF metadata was cleared. The Wells Fargo Advisors name and
logo appear because they are printed on the form; Wells Fargo did not produce or endorse
this specimen. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Brokerages and advisers have to record a client's risk tolerance and investment
objectives before recommending investments, and many still collect the answers on
paper.

- **Wealth management and brokerage:** advisers use the answers to place a client in a
  risk category and choose a model portfolio.
- **Compliance and supervision:** reviewers check that each recommendation fits the
  profile the client signed off on.
- **Account opening and operations:** teams key the answers and contact details into the
  firm's client records.
- **Retirement plan and insurance advisers:** they use similar questionnaires to set
  allocations for annuities and plan accounts.
- **Exam and audit:** firms produce completed profiles when regulators ask how a
  recommendation was justified.

### What it contains

- **Long runs of checkboxes,** with each answer a pen tick against one of four or five
  printed options.
- **Handwritten write-ins** beside some answers, such as a secondary purpose, years of
  experience and total assets.
- **A table answered by a tick,** where question 7 is answered by marking one row of a
  table of hypothetical returns.
- **Handwritten contact details** on printed lines.
- **Values that need normalizing,** such as a state name and an asset total written as
  "3.5M".
- **Raster scans with no text layer,** so every answer has to be read from the page
  image.
