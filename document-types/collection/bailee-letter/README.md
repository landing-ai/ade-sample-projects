# Bailee Letter

**On the website:** [landing.ai/document-type/bailee-letter](https://landing.ai/document-type/bailee-letter)

A synthetic bailee letter for a mortgage loan sale. A warehouse lender sends the note to
the investor buying the loan, which holds it as the lender's bailee until it wires the
purchase price. The letter names the parties, the loan and the funding window, and ends
with a signed acknowledgment and a one-loan Schedule A.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 23 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:32 | 2026-11-19 02:31 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 5,471 | 5,540 |
| Words under 0.95 confidence | 1 | n/a |
| Words under 0.80 confidence | 0 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.6 s | 8.7 s |
| Per page | 1.2 s | 2.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.2 credits | 3.4 credits |
| Per page | 0.30 credits | 0.85 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:32 | 2026-11-19 02:31 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 358.6 s | 79.8 s |
| Per schema field (23) | 15.59 s | 3.47 s |
| Per value returned | 13.79 s | 3.19 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.9 credits | 1.9 credits |
| Per schema field (23) | 0.083 credits | 0.083 credits |
| Per value returned | 0.073 credits | 0.076 credits |

## Origin

`source/bailee-letter-ocrolus-sample.pdf` is a synthetic bailee letter. It is **4
pages, portrait**: the letter (pages 1-2), the signed acknowledgment (page 3) and a
one-loan Schedule A (page 4). It was made in Google Docs.

In a bailee letter, a warehouse lender that funded a mortgage sends the note to the
investor buying the loan. The investor holds the note as the lender's *bailee*, and
ownership passes only once the investor wires the purchase price. If it does not fund
within the window, it must send the note back.

| | |
|---|---|
| Publisher | Ocrolus (document-AI vendor sample) |
| Source | [Google Drive](https://drive.google.com/file/d/1UF9p9L2zcjz8UlyrZucuDTAqiT4lIAg_/edit) |
| Linked from | [docs.ocrolus.com/docs/bailee-letter](https://docs.ocrolus.com/docs/bailee-letter) |
| Retrieved | 2026-10-02, by script (Drive's standard download link) |
| Clearance | Public |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this document type links this exact file as its sample, which establishes the
publisher. Every value is synthetic: "Fake Home Mortgage", "ABC Sample Inc.", "XYZ
Bank", borrower "John Sample" at "123 Fake Street", signers "Jack Sample" and "James
Fake", and loan `123456789`. The signatures are drawn to match those invented names. The
PDF metadata holds only the Google Docs renderer and "Untitled document". Nothing needed
redacting. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Bailee letters move with the collateral file every time a funded mortgage is sold out
of a warehouse line, so the same terms are read by each party to the trade.

- **Warehouse lenders:** they track which notes are out with which investor, and when
  each must be paid for or returned.
- **Mortgage investors and aggregators:** they log the loan, the purchase price and the
  funding deadline before they release the wire.
- **Document custodians:** they check the note and the letter on receipt and sign the
  acknowledgment.
- **Mortgage originators and post-closing teams:** they assemble the letter, the note
  and the schedule for each loan sale.
- **Secondary-market operations and audit:** reviewers match the letter to the
  schedule and to the wire.

### What it contains

- **Labelled lines at the top** for the payee, the loan and the lender.
- **Dense legal paragraphs** where the parties' roles have to be read from the prose,
  with the warehouse lender named many times across three pages.
- **Numbers in words and figures,** such as "ten (10) business days".
- **Two signature blocks side by side,** each with a company, a signature, a printed
  name and a title. The pairing of signer and company depends on the column.
- **A one-row schedule table** with the loan amount, which differs from the purchase
  price in the letter body.
- **Handwritten signatures.**
