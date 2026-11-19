# Residential lease

**On the website:** [landing.ai/document-type/residential-lease](https://landing.ai/document-type/residential-lease)

A residential lease on the Arkansas REALTORS® Association's standard Residential
Lease/Rental Agreement form, completed and e-signed through a Century 21 brokerage in
November 2023. Page 1 holds the filled-in terms: the parties, the property, the lease
term, rent, late charges and security deposit. Standard clauses follow, and the last
page carries the management and tenant e-signatures.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 18 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:29 | 2026-11-19 03:49 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 27,422 | 27,927 |
| Words under 0.95 confidence | 50 | n/a |
| Words under 0.80 confidence | 29 | n/a |
| Words under 0.50 confidence | 13 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.5 s | 17.5 s |
| Per page | 1.4 s | 2.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.7 credits | 10.0 credits |
| Per page | 0.62 credits | 1.67 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:29 | 2026-11-19 03:50 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 18 | 18 |
| Non-null fields returned | 17 | 17 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 256.3 s | 90.6 s |
| Per schema field (18) | 14.24 s | 5.03 s |
| Per value returned | 8.84 s | 3.36 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.5 credits | 6.5 credits |
| Per schema field (18) | 0.361 credits | 0.361 credits |
| Per value returned | 0.224 credits | 0.241 credits |

## Origin

`source/residential-lease-redacted.pdf` is a residential lease on the Arkansas
REALTORS® Association's standard Residential Lease/Rental Agreement form, completed and
e-signed through a Century 21 brokerage on November 17, 2023, redacted. It is **6 pages,
portrait (612×792)**: the filled-in terms on page 1, standard clauses on pages 2 to 5,
and the signature page.

| | |
|---|---|
| Publisher | Arkansas REALTORS® Association (form), completed by a Century 21 Prestige Realty agent |
| Source | [scribd.com/document/746241294/Residential-Lease-Rental-Agreement](https://www.scribd.com/document/746241294/Residential-Lease-Rental-Agreement) |
| Retrieved | 2026-09-28, downloaded manually |
| Clearance | Redacted |

This is a real lease, uploaded to Scribd by a third party and downloaded by hand,
because Scribd blocks scripted requests. **At the document owner's decision only the
tenant's name is replaced.** Every other detail is kept as printed: the rental
property's address, the agent's and principal broker's names, e-signatures and contact
details, the form serial number and the e-signature session ID.

| What | Replaced with | Occurrences |
|---|---|---|
| Tenant's name, printed and as the typed e-signature | Jane Q Sample | 3 |

The replacement was made with `document-types/scripts/redact.py`, which removes the
underlying text rather than covering it, and the PDF metadata was cleared.

**The tenant's signature still reads as a signature.** It was a typed e-signature in a
handwriting font, so the stand-in is set in Indie Flower, an openly licensed (SIL OFL)
handwriting font, in the same navy as the two real signatures beside it. The printed
name keeps its bold italic. The redaction also covered a near-invisible "Prepared by"
line in 2-point type on each page, and the underscore fill lines beneath the replaced
values were drawn back, so the lease keeps its original 2,301.

The tenant's name is not extractable from the committed PDF and appears nowhere in this
folder. The rules file used by `redact.py` stays outside the repo. An earlier version of
this folder replaced every name, contact detail and identifier in the lease. The owner
asked for only the tenant's name to be replaced, and for the signatures to stay. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A residential lease sets the rent, term and deposit for a home, and it is often used as
proof of where a person lives.

- **Property management:** managers record lease terms, rent due dates, late charges
  and deposits for each unit.
- **Mortgage lending:** underwriters use leases to count rental income on investment
  properties.
- **Proof of address and identity verification:** banks, schools and agencies accept a
  signed lease as proof of residence.
- **Real estate brokerages:** agents who arrange rentals keep the executed lease and
  track renewals.
- **Rental housing assistance programs:** caseworkers verify rent amounts and the lease
  term before paying benefits.

### What it contains

- **A filled-in form with values typed over underscore blanks,** in bold italic, inside
  long clauses.
- **Values embedded in sentences,** such as several rent terms in one paragraph.
- **Dates split across blanks,** as "(month) November (day) 17 (year) 2023".
- **A checkbox** for the type of term.
- **A two-column signature page,** with management signatures down the left and tenant
  signatures down the right.
- **E-signatures in handwriting fonts** and a near-invisible 2-point "Prepared by" line
  on each page.
