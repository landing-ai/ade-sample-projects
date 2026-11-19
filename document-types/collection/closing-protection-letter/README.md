# Closing Protection Letter

**On the website:** [landing.ai/document-type/closing-protection-letter](https://landing.ai/document-type/closing-protection-letter)

A sample closing protection letter from Fidelity National Title Insurance Company to a
lender, for a Virginia closing handled by Covenant Real Estate Services. It names the
lender, the settlement agent, the borrowers, the property, and the file and loan
numbers, then sets out the conditions under which the insurer covers the lender's
losses caused by the closing agent.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 22 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 | 2026-11-19 02:42 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 12,704 | 12,962 |
| Words under 0.95 confidence | 8 | n/a |
| Words under 0.80 confidence | 3 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.8 s | 20.6 s |
| Per page | 3.4 s | 10.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.6 credits | 4.3 credits |
| Per page | 0.80 credits | 2.15 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:40 | 2026-11-19 02:43 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 22 | 22 |
| Non-null fields returned | 22 | 22 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 174.7 s | 53.6 s |
| Per schema field (22) | 7.94 s | 2.43 s |
| Per value returned | 7.60 s | 2.33 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.5 credits | 3.5 credits |
| Per schema field (22) | 0.159 credits | 0.159 credits |
| Per value returned | 0.152 credits | 0.152 credits |

## Origin

`source/sample-cpl.pdf` is a sample closing protection letter (CPL) issued by Fidelity
National Title Insurance Company to a lender, for a Virginia closing conducted by
Covenant Real Estate Services. It is on Fidelity's form CPL80446 (12/2018). It is **2
pages, portrait**, with a normal text layer.

| | |
|---|---|
| Publisher | Covenant Real Estate Services LLC |
| Source | [covenantreal.com/…/Sample-CPL.pdf](https://covenantreal.com/wp-content/uploads/2023/03/Sample-CPL.pdf) |
| Retrieved | 2026-10-02, by script |
| Clearance | Public |

The settlement agent publishes this sample on its own website for lenders, with a red
`SAMPLE` watermark. The transaction data is specimen: borrowers "John Doe and Jane Doe",
addressee "Lending Bank, LLC", property "1212 ABC Drive". The settlement agent named on
it is the publisher itself. The one real person is the insurer's chief underwriting
counsel, as a facsimile corporate signature. Nothing needed redacting. Full provenance
is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A CPL is the title insurer's promise to a lender that it will cover losses caused by the
closing agent: not following the lender's closing instructions, or fraud and theft of
the lender's funds. Lenders ask for one on every closing, so it sits beside the title
commitment and the wire instructions in the closing package.

- **Mortgage lending:** closing departments collect a CPL for each loan and check that
  it names the right lender, agent and transaction.
- **Title insurance underwriters:** they issue CPLs through their agents and track them
  against the policies they back.
- **Title and settlement agents:** they request a CPL for each closing and send it to the
  lender.
- **Loan quality control and post-closing:** reviewers confirm the CPL is in the file
  and matches the loan number and property.

### What it contains

- **Transaction values packed into a letterhead block:** lender, settlement agent,
  borrowers, property, file number and loan number.
- **Pages of numbered conditions** around those few values.
- **A coverage cap stated inside a numbered requirement** rather than in a labelled
  field.
- **The settlement agent's name printed twice,** under its heading and in a second
  address block.
- **A dense, tightly kerned footer** with the letter ID, agent number and correspondence
  address.
- **A facsimile signature** and a red diagonal `SAMPLE` watermark.
