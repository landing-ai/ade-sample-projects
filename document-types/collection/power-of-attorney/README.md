# Power of Attorney

**On the website:** [landing.ai/document-type/power-of-attorney](https://landing.ai/document-type/power-of-attorney)

A one-page specimen corporate power of attorney in which a mortgage lender appoints
another company to execute, endorse, assign and deliver its promissory notes, the
mortgages securing them and the related loan documents. It states that the power is
irrevocable, and ends with the execution date, the signature blocks of both companies
and a notarial acknowledgment.

| | |
|---|---|
| Pages | 1 |
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
| Processed (UTC) | 2026-11-19 03:21 | 2026-11-19 03:42 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,621 | 3,747 |
| Words under 0.95 confidence | 10 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 22.3 s | 22.6 s |
| Per page | 22.3 s | 22.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.6 credits | 1.5 credits |
| Per page | 0.60 credits | 1.50 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:43 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 22 | 22 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 386.1 s | 193.0 s |
| Per schema field (23) | 16.79 s | 8.39 s |
| Per value returned | 16.09 s | 8.04 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.8 credits | 2.0 credits |
| Per schema field (23) | 0.078 credits | 0.087 credits |
| Per value returned | 0.075 credits | 0.083 credits |

## Origin

`source/power-of-attorney-ocrolus-sample.pdf` is a specimen corporate power of attorney.
It is **1 page, portrait**. The printed form is about 3,300 vector paths with no text
layer, and only the typed-in values are text.

A mortgage lender (the principal) appoints another company (the agent) to execute,
endorse, assign and deliver its promissory notes, the mortgage rights securing them, and
the related loan documents. The power is irrevocable and survives the principal's
bankruptcy, dissolution or incapacity. Below the operative text are the execution line,
two signature blocks side by side (principal left, agent right) and a notarial
acknowledgment.

| | |
|---|---|
| Publisher | Ocrolus (document-AI vendor sample) |
| Source | [Google Drive](https://drive.google.com/file/d/1HBbJsyyhp90pAaS4sYdq-nokH1f25BeW/view) |
| Linked from | [docs.ocrolus.com/docs/power-of-attorney](https://docs.ocrolus.com/docs/power-of-attorney) |
| Retrieved | 2026-10-03, by script (Drive's standard download link) |
| Clearance | **Public** |

The Drive link alone does not say who made the file. The Ocrolus documentation page for
this document type links this exact file as its sample, which establishes the publisher.
Every value is specimen: principal "Fake Mortgage Company" at "123 Main Fake Street,
Anycity", agent "Sample Financial Services, Inc." at "123 Fake Grant Avenue", signer
"James Doe" and notary "John Doe", with script signatures drawn to go with those
invented names. The page is used exactly as published.

The one change: the PDF's metadata author field held the name of the person who
prepared the file, so the metadata (Info dictionary and XMP) was cleared. The rendered
page is pixel-identical to the original and the text layer is unchanged. Full provenance
is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A power of attorney lets one party act and sign for another. In mortgage lending,
corporate powers of attorney like this one let a servicer or document custodian sign
assignments and endorsements for the lender.

- **Mortgage servicers and loan purchasers:** they check that the agent signing
  assignments and endorsements had the authority to do so.
- **Title companies and closing agents:** they confirm the power is valid and recorded
  before they accept documents signed under it.
- **County recorders:** powers of attorney are recorded so later assignments can be
  traced to them.
- **Banks and brokerages:** they review a power of attorney before they let an agent act
  on an account.
- **Law firms and compliance teams:** they confirm the scope of the powers and whether
  the power survives incapacity or bankruptcy.

### What it contains

- **A mixed-layer PDF.** The printed form has no text layer, and only the typed-in values
  are text.
- **Fill-in blanks threaded through legal prose.**
- **Dates split across separate blanks** ("01 day of 01, 20 25"; "01, 15, 2025") that
  have to be assembled.
- **Two signature blocks side by side,** principal and agent, with script signatures.
- **A notarial acknowledgment** with state, county, date and commission expiry.
