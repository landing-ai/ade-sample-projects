# Arbitration award

**On the website:** [landing.ai/document-type/arbitration-award](https://landing.ai/document-type/arbitration-award)

A FINRA arbitration award in case 25-01517, a customer's claim against a
broker-dealer and three of its associated persons, heard in Providence, Rhode Island.
It sets out the parties and counsel, the causes of action, the relief requested, the
panel's award and the allocation of forum fees, and ends with the arbitrators'
signatures.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 50 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 7,736 | 8,010 |
| Words under 0.95 confidence | 1 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 9.6 s | 20.4 s |
| Per page | 1.9 s | 4.1 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.6 credits | 4.6 credits |
| Per page | 0.32 credits | 0.92 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 50 | 50 |
| Non-null fields returned | 36 | 37 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 111.0 s | 445.1 s |
| Per schema field (50) | 2.22 s | 8.90 s |
| Per value returned | 2.47 s | 9.68 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.9 credits | 5.6 credits |
| Per schema field (50) | 0.118 credits | 0.112 credits |
| Per value returned | 0.131 credits | 0.122 credits |

## Origin

`source/25-01517.pdf` is a FINRA arbitration award, case 25-01517: a customer's claim
against a broker-dealer and three of its associated persons, heard in Providence, Rhode
Island. It is **5 pages, portrait (612×792)**, produced from Word, so it has a full text
layer.

| | |
|---|---|
| Publisher | FINRA Dispute Resolution Services |
| Source | [finra.org/…/aao_documents/25-01517.pdf](https://www.finra.org/sites/default/files/aao_documents/25-01517.pdf) |
| Retrieved | 2026-09-26 |
| Clearance | Public |

FINRA publishes every arbitration award in its public Arbitration Awards Online
database. This one is used **exactly as published, unredacted**. That was a deliberate
decision by the document owner. The award names the claimant, who is a private
individual, three individual respondents, the respondent member firm, counsel and their
firms, and the three arbitrators, all as they appear in the public record. The PDF
metadata `author` field, the FINRA staff member who prepared it, is also left as
published.

It is recent: the award was served on 2026-09-25, the day before it was retrieved. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

FINRA arbitration is the forum for most disputes between investors and US brokerage
firms, and every award is published, so a large public record builds up case by case.

- **Broker-dealer compliance and legal:** firms track awards against them and their
  representatives, and report them on the registration forms they file.
- **Securities litigation firms:** claimant and defense counsel research past awards by
  firm, product and cause of action to value new cases.
- **Investor due diligence:** investors, advisers and recruiting firms check a
  representative's arbitration history before doing business with them.
- **Errors and omissions insurers:** underwriters and claims teams review awards
  against the firms and individuals they cover.
- **Regulators and researchers:** analysts study awards for patterns in claims,
  outcomes and damages.

### What it contains

- **A labelled caption** on page 1: case number, parties, hearing site and nature of
  dispute.
- **Long narrative paragraphs** for the causes of action, relief requested, the award
  and the fee allocation.
- **Many named parties** in roles that must be kept apart: claimant, individual
  respondents, the member firm, counsel and arbitrators.
- **Dates and dollar amounts inside prose,** such as damages awarded and fees assessed.
- **A panel table and electronic signature blocks** with signature dates on the last
  page.
- **A born-digital text layer** from a Word export.
