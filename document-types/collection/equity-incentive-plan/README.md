# Equity Incentive Plan

**On the website:** [landing.ai/document-type/equity-incentive-plan](https://landing.ai/document-type/equity-incentive-plan)

The Alcoa Corporation Stock and Incentive Compensation Plan, as amended and restated on
May 6, 2026. It is the plan document every equity grant is made under: definitions,
administration, the share reserve and share-counting rules, eligibility, the terms of
each award type, change-in-control treatment, amendment and the plan term.

| | |
|---|---|
| Pages | 18 |
| Fields in the extraction schema | 27 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:55 | 2026-11-19 03:01 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 74,153 | 74,892 |
| Words under 0.95 confidence | 15 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 2 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 13.2 s | 61.1 s |
| Per page | 0.7 s | 3.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 10.2 credits | 27.8 credits |
| Per page | 0.57 credits | 1.54 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:55 | 2026-11-19 03:02 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 27 | 27 |
| Non-null fields returned | 27 | 27 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 242.0 s | 126.6 s |
| Per schema field (27) | 8.96 s | 4.69 s |
| Per value returned | 6.20 s | 3.33 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 16.4 credits | 16.5 credits |
| Per schema field (27) | 0.607 credits | 0.611 credits |
| Per value returned | 0.421 credits | 0.434 credits |

## Origin

`source/alcoa-stock-and-incentive-compensation-plan-2026.pdf` is the **Alcoa
Corporation Stock and Incentive Compensation Plan (as Amended and Restated)**, dated
May 6, 2026. It is **18 pages, portrait**, native text in a single column.

This is the plan document itself, the instrument stockholders approve and every equity
grant is made under: purpose and definitions, administration, the share reserve and
share-counting rules, eligibility, the terms of each award type (options, stock
appreciation rights, restricted shares, restricted share units, performance and cash
incentive awards), change-in-control treatment, performance goals, amendment, general
provisions and the plan term.

| | |
|---|---|
| Publisher | Alcoa Corporation |
| Source | [alcoa.com, plan PDF](https://www.alcoa.com/equity-plan/pdfs/alcoa-corporation-stock-and-incentive-compensation-plan-as-amended-and-restated-06-May-2026.pdf) |
| Linked from | [alcoa.com/equity-plan](https://www.alcoa.com/equity-plan/) |
| Retrieved | 2026-10-28, by script |
| Clearance | Public |

Alcoa publishes the plan on its own equity-plan page for stockholders and participants.
It names no individual, carries no signatures, and its PDF metadata holds only Word's
placeholder author. Nothing was replaced and the file is unchanged from the download.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An equity incentive plan sets the rules for every stock award a company grants, so the
same terms are read by the people who vote on it, administer it and value it.

- **Proxy advisers and institutional investors:** they read the share reserve, counting
  ratios and director caps before recommending a vote on the plan.
- **Compensation consultants and HR:** they check proposed grants against the plan's
  limits and vesting rules.
- **Stock plan administrators and transfer agents:** they track the share pool and
  apply the counting rules to each grant.
- **Corporate and securities lawyers:** they draft amendments and review the plan in
  financings and acquisitions.
- **Auditors and finance teams:** they read award terms to account for stock-based
  compensation.

### What it contains

- **Dense legal prose with no blanks or tables.** Every figure sits inside a sentence,
  often several to a sentence, and is qualified by the clauses around it.
- **Packed numeric rules.** The share-counting rule alone holds three ratios and six
  dates in four lines.
- **Numbers written as words,** such as "one year" and "ten years".
- **Numbered sections and lettered subsections** that cross-reference each other.
- **Open-ended periods** that run "from May 6, 2026 and thereafter", with no end date.
- **A native text layer** in a single column.
