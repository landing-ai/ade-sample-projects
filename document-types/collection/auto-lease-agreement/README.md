# Auto Lease Agreement

**On the website:** [landing.ai/document-type/auto-lease-agreement](https://landing.ai/document-type/auto-lease-agreement)

A Florida closed-end motor vehicle lease for a new 2025 Honda Civic Sedan, on the
Reynolds and Reynolds form that Honda Financial Services dealers use. It names the
lessees, the dealer and the assignee, and carries the federal Consumer Leasing Act
disclosures, the step-by-step calculation of the monthly payment, the itemized
capitalized cost, the terms and conditions, an arbitration provision and signatures.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 55 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:28 | 2026-11-19 02:29 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 64,014 | 63,642 |
| Words under 0.95 confidence | 430 | n/a |
| Words under 0.80 confidence | 227 | n/a |
| Words under 0.50 confidence | 78 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 13.0 s | 27.6 s |
| Per page | 2.6 s | 5.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.2 credits | 18.5 credits |
| Per page | 1.44 credits | 3.70 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:29 | 2026-11-19 02:29 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 55 | 55 |
| Non-null fields returned | 55 | 55 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 114.6 s | 149.1 s |
| Per schema field (55) | 2.08 s | 2.71 s |
| Per value returned | 1.94 s | 2.53 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 14.8 credits | 14.7 credits |
| Per schema field (55) | 0.269 credits | 0.267 credits |
| Per value returned | 0.251 credits | 0.249 credits |

## Origin

`source/auto-lease-agreement-honda-florida-redacted.pdf` is a **Closed End Motor
Vehicle Lease (With Arbitration Provision)**, form HFS-UCL-FL-e-14 1/21: the Reynolds
and Reynolds LAW form that Honda Financial Services dealers in Florida use. This copy is
the customer copy of a real, executed lease of a new 2025 Honda Civic Sedan from
AutoNation Honda Miami Lakes, assigned to Honda Lease Trust, dated 3 December 2024. It
is **5 pages, portrait, US legal size (8.5 x 14 in), with a text layer**.

Page 1 carries the parties, the vehicle, and the federal Consumer Leasing Act
disclosures: amount due at signing, scheduled payments, other charges, total of
payments, the itemization of the amount due, and Item 7, the step-by-step calculation of
the monthly payment. Page 2 has the trade-in, the itemized gross capitalized cost,
optional products, required insurance and the lease term. Pages 3 and 4 are dense
two-column terms and conditions. Page 5 has the arbitration provision and the signature
blocks.

| | |
|---|---|
| Publisher | AutoNation Honda Miami Lakes (lessor), on the Reynolds and Reynolds LAW form for Honda Financial Services. Uploaded to Scribd by a third party |
| Source | [scribd.com/document/943516552/Contract](https://www.scribd.com/document/943516552/Contract) |
| Retrieved | 2026-10-26, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | Redacted |

Scribd is a user-upload site, so the account that posted the lease is not its
publisher. The document was treated as a personal record from the start.

The lease was not redacted at source. Everything that identifies a person or the
specific vehicle was replaced with `document-types/scripts/redact.py`, which removes the
underlying text rather than drawing over it:

| What | Replaced with | Count |
|---|---|---|
| Lessee's full name | `JOHN Q SAMPLE` | 2 |
| Co-lessee's full name | `JANE Q SAMPLE` | 2 |
| Lessee's street address | `100 MAIN ST` | 1 |
| Co-lessee's street address | `200 OAK ST` | 1 |
| Vehicle identification number | `2HGFE2F59SH687480` | 1 |
| Lessee's insurance policy number | `210048921` | 1 |
| Dealer employee who signed for the lessor | `Pat Example` | 1 |
| Captured e-signature images (7, on pages 2 and 5) | handwriting-font stand-ins (`J Sample`, `Jane Sample`, `P Example`) | 7 |

The replacement VIN keeps Honda's `2HGFE2F5` prefix so it still reads as a Civic, with a
random serial and a deliberately invalid check digit, so it cannot match a real vehicle.
That check was done locally, not with a decoding service. The policy number is random
digits from `plausible.py`. Kept: the dealer and its address, the assignee, the
insurer's name, address and customer-service number, the lessees' city, state, ZIP and
county, the signer's job title, the lease date, and every financial term. PDF metadata
was cleared.

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. The redaction was verified by redact.py's text and image checks, by eye on
renders of pages 1, 2 and 5, and by `ship.py check --rules` over every file in this
folder. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A vehicle lease is a consumer-finance contract whose most important content is a chain
of numbers, set out in disclosures that federal law requires.

- **Captive finance companies and banks:** lessors book each lease from the capitalized
  cost, residual value, rent charge and payment schedule.
- **Auto dealers:** F&I offices and back-office staff check the deal against the
  contract before funding.
- **Lease-backed securitization:** issuers and auditors verify contract terms when
  leases are pooled into asset-backed securities.
- **Consumer lending and underwriting:** lenders read a borrower's lease to confirm an
  existing monthly obligation.
- **Compliance and consumer protection:** reviewers check the Consumer Leasing Act
  disclosures and the arbitration terms.

### What it contains

- **A payment calculation laid out as arithmetic,** with the operators (`–`, `=`, `+`,
  `÷`) in their own column between the label and the value.
- **The same value repeated,** such as the monthly payment on several lines, so each
  field has to be tied to the right line.
- **Fill-in-the-blank sentences** that hold several values in one sentence.
- **Many `N/A` fields** in the trade-in, optional products and guarantor sections.
- **Dense two-column terms and conditions** on legal-size pages.
- **Light-blue field shading** behind the typed values and a faint diagonal "Customer
  Copy" watermark on every page.
- **E-signatures** (here, handwriting-font stand-ins) on pages 2 and 5.
