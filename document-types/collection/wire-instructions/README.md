# Wire Instructions

**On the website:** [landing.ai/document-type/wire-instructions](https://landing.ai/document-type/wire-instructions)

A title company's wire instructions for sending closing funds on a California real
estate transaction, a single page taken from a title commitment. It names the receiving
bank and its address, the routing and account numbers, the account name and type, the
order number to quote, and the rules for how funds must be sent.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 15 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:43 | 2026-11-19 04:00 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 946 | 1,070 |
| Words under 0.95 confidence | 2 | n/a |
| Words under 0.80 confidence | 2 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.0 s | 11.9 s |
| Per page | 4.0 s | 11.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.3 credits | 0.8 credits |
| Per page | 0.30 credits | 0.80 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 | 2026-11-19 04:00 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 15 | 15 |
| Non-null fields returned | 15 | 15 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 248.4 s | 45.6 s |
| Per schema field (15) | 16.56 s | 3.04 s |
| Per value returned | 16.56 s | 3.04 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 0.9 credits | 0.9 credits |
| Per schema field (15) | 0.060 credits | 0.060 credits |
| Per value returned | 0.060 credits | 0.060 credits |

## Origin

`source/wire-instructions-redacted.pdf` is First Integrity Title Company's wire
instructions for closing funds. It is **1 page, portrait**, with no text layer: every
glyph is a vector path.

It is page 11 of the title commitment in
[`../commitment-for-title-insurance/`](../commitment-for-title-insurance/), split out to
stand on its own. That folder dropped the page, and this one is only that page.

| | |
|---|---|
| Publisher | First Integrity Title Company |
| Source | [adc-tenbox-prod.imgix.net/…/PRELIMINARY_TITLE_REPORT/…pdf](https://adc-tenbox-prod.imgix.net/resi/propertyDocuments/1300098/PRELIMINARY_TITLE_REPORT/40C02EC5FCCE4D3BBF40A5C6B9BEF65F.v1.pdf), page 11 |
| Retrieved | 2026-10-02, by script |
| Clearance | Redacted |

The page was posted with a preliminary title report on a residential property-auction
listing, and it held a live title-company trust account. Wire instructions are what
wire-fraud schemes forge, so a sample that names a real company, a real bank and a
working account number would be a template for the fraud.

| Data | Replaced with |
|---|---|
| Beneficiary bank account number | Random stand-in, same length |
| ABA routing number | Random 9-digit stand-in that **fails the ABA checksum**, so it cannot route a wire |
| Reference order number | `FIN-78796415`, the commitment folder's stand-in |
| Property address | `100 SAMPLE RD`, `Anytown`, `CA 90000`, as in the commitment folder |
| PDF metadata | cleared |

Reusing the commitment's stand-ins keeps the two samples consistent: the order number on
this page is the commitment's order number.

The title company's and the receiving bank's names, addresses and published phone
numbers are kept. They are businesses, and with the account and routing numbers
replaced the page cannot send money anywhere real.

Because the page has no text layer, it was redacted with
`document-types/scripts/redact_outlined.py`, which deletes the glyph paths and draws the
replacements, using the same rules as the commitment plus the two bank numbers. OCR on
literals and bare digits confirmed that no original value survives in the PDF or
anywhere in this folder. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Wire instructions tell a buyer or lender where to send money for a real estate closing.
A changed account number on wire instructions is the classic closing fraud, so every
party checks them against a known-good copy.

- **Title and escrow companies:** they issue the instructions and verify incoming wires
  against them.
- **Mortgage lenders:** funding teams confirm the bank, routing and account details
  before wiring loan proceeds.
- **Real estate agents and attorneys:** they pass instructions to buyers and confirm
  them by phone before funds move.
- **Banks and payment operations:** fraud and payment teams screen outgoing wires for
  changed beneficiary details.
- **Corporate treasury and accounts payable:** finance teams verify vendor wire details
  before paying.

### What it contains

- **A one-page key-value form,** with each `Label: value` pair on its own line.
- **Bank identifiers** in fixed formats: an ABA routing number and an account number.
- **A logo** with a short form of the company name that differs from the full name in
  the text.
- **Two-line addresses** for the receiving bank.
- **Payment rules stated in sentences,** such as wire-only and no ACH.
- **Outlined text with no text layer,** so every value has to be read from the page
  image.
