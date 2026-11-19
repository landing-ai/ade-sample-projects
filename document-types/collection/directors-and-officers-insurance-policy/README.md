# D&O Insurance Policy

**On the website:** [landing.ai/document-type/directors-and-officers-insurance-policy](https://landing.ai/document-type/directors-and-officers-insurance-policy)

A complete, issued Travelers SelectOne+ policy with Mutual Fund Liability coverage for
Monteagle Funds, a registered investment company, for March 2022 to March 2023. The
declarations give the policy number, insured, policy period, limit of liability,
retention, premium and extended reporting terms. The rest is the general terms,
the coverage part and the endorsements.

| | |
|---|---|
| Pages | 26 |
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
| Processed (UTC) | 2026-11-19 02:48 | 2026-11-19 02:55 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 84,418 | 90,118 |
| Words under 0.95 confidence | 57 | n/a |
| Words under 0.80 confidence | 31 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 16.7 s | 24.6 s |
| Per page | 0.6 s | 0.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 12.4 credits | 35.6 credits |
| Per page | 0.48 credits | 1.37 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:49 | 2026-11-19 02:56 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 45 | 45 |
| Non-null fields returned | 44 | 44 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 91.8 s | 153.3 s |
| Per schema field (45) | 2.04 s | 3.41 s |
| Per value returned | 1.37 s | 2.29 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 19.4 credits | 20.5 credits |
| Per schema field (45) | 0.431 credits | 0.456 credits |
| Per value returned | 0.290 credits | 0.306 credits |

## Origin

`source/directors-and-officers-insurance-policy-travelers.pdf` is a complete, issued
**Travelers SelectOne+ Investment Advisers and Funds** policy with **Mutual Fund
Liability** coverage, for the policy year March 16, 2022 to March 16, 2023. It is **26
pages, portrait**, with a text layer.

The named insured is Monteagle Funds, a registered investment company (a fund trust with
seven series). The policy is laid out the way most management liability policies are:

- **Declarations** (pages 1-3): policy number, insurer, named insured, policy period,
  claim notice addresses, coverages, limit of liability, retention, prior or pending
  proceeding date, premium, extended reporting period, shared limit, forms attached,
  producer, and the insurer's facsimile officer signatures.
- **Terrorism endorsements** (pages 4-5).
- **General Terms and Conditions** (pages 6-16), the common definitions and conditions.
- **Endorsements** (pages 17-18 and 25-26): specified entities (the seven funds), global
  coverage compliance, defense expenses for investigating and monitoring claims, and
  mock regulatory examination.
- **Mutual Fund Liability Coverage part** (pages 19-24): insuring agreements,
  definitions and exclusions.

This is a mutual-fund management liability policy, not a classic corporate D&O policy.
It covers the fund trust and its directors, trustees and officers rather than the board
of an operating company. The structure and the key terms (claims-made basis, defense
inside limits, retention, prior or pending proceeding date, extended reporting period)
are the same as a corporate D&O policy, which is why it serves as the sample.

| | |
|---|---|
| Publisher | Monteagle Funds, as filed with the SEC; policy issued by Travelers Casualty and Surety Company of America |
| Source | [SEC EDGAR, monteagle4017g.pdf](https://www.sec.gov/Archives/edgar/data/1045701/000116204422000446/monteagle4017g.pdf) |
| Filing | Form 40-17G (fidelity bond and insurance filing by a registered investment company), accession 0001162044-22-000446, CIK 1045701 |
| Retrieved | 2026-10-04, by script |
| Clearance | Public |

Registered investment companies file their bonds and insurance policies on EDGAR under
Rule 17g-1, so this policy is a public record. The kept pages name only organizations:
the fund trust and its series, the insurer, and the broker, plus the insurer's corporate
claims email, fax and phone lines. Nothing was replaced.

Two changes from the filed PDF:

- **Pages 1-3 were dropped.** They are the fund's cover letter, a secretary's
  certificate and the board resolutions approving the coverage, which are not part of
  the policy and name individuals and a direct phone line. Page numbers here are the
  filing's minus three. The cover letter also describes a different policy from the one
  attached, a filing error; dropping it removes that inconsistency too.
- **PDF metadata was cleared** (the filer's Word document title, author initials,
  producer and dates). The policy pages are otherwise unchanged.

The declarations carry the insurer's two pre-printed facsimile officer signatures
(President and Corporate Secretary), with no printed names. They are part of every
Travelers policy of this form and were left in place. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A management liability policy protects an organization's directors and officers against
claims over their decisions. The declarations set the price and limits, and the
conditions decide how claims are paid.

- **Insurance brokers:** they compare limits, retentions, premiums and endorsements
  across carriers at each renewal.
- **Carriers and underwriters:** they check issued policies against the bound terms and
  review prior coverage on submissions.
- **Corporate legal and risk management:** they track policy periods, notice addresses
  and claims-made deadlines.
- **Fund boards and compliance:** registered investment companies file these policies
  with the SEC and review the coverage each year.
- **M&A and financing due diligence:** counsel confirm D&O coverage and its extended
  reporting terms before a deal closes.

### What it contains

- **A long policy** whose key values sit on two declarations pages among 26 pages of
  dense, two-level legal prose.
- **Terms that repeat throughout the conditions,** such as "Limit of Liability" and
  "Retention", so the declarations values have to be found among them.
- **Policy terms stated in prose, not fields:** the claims-made basis, defense costs
  inside the limit and no duty to defend appear in a capitalized warning and in the
  conditions.
- **Numbered ITEMs** on the declarations, with a semicolon-separated run of form numbers
  in one line.
- **Endorsement titles that wrap across two lines.**
- **Facsimile officer signatures** on the declarations.
