# Invoice

**On the website:** [landing.ai/document-type/invoice](https://landing.ai/document-type/invoice)

A one-page bilingual French/English sales invoice from A.E. Blake Sales Ltd., a Canadian
industrial supplier, dated January 2022. It lists the seller, the sold-to and ship-to
addresses, order and shipping terms, a three-row line-item table, and the subtotal, HST
and total in Canadian dollars.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-23 21:24 | 2026-11-19 03:22 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 2,208 | 2,354 |
| Words under 0.95 confidence | 28 | n/a |
| Words under 0.80 confidence | 7 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.1 s | 18.3 s |
| Per page | 5.1 s | 18.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.4 credits | 1.1 credits |
| Per page | 0.40 credits | 1.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-23 21:24 | 2026-11-19 03:23 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 30 | 30 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 61.3 s | 56.4 s |
| Per schema field (35) | 1.75 s | 1.61 s |
| Per value returned | 1.39 s | 1.28 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.0 credits | 2.0 credits |
| Per schema field (35) | 0.057 credits | 0.057 credits |
| Per value returned | 0.045 credits | 0.045 credits |

## Origin

`source/invoice_4.pdf` is a single-page A.E. Blake Sales invoice, bilingual
French/English, with a three-row line-item table. It is **1 page, portrait**.

It was copied from `Use_Cases/Invoices/input_folder/`, where it has been committed to
this public repository for some time, so using it here publishes nothing new. It was
cleared for use on the LandingAI website by the marketing team on 2026-11-23, as
published, with no redaction.

| | |
|---|---|
| Publisher | A.E. Blake Sales Ltd. |
| Source | [`Use_Cases/Invoices/input_folder/invoice_4.pdf`](https://github.com/landing-ai/ade-sample-projects/blob/main/Use_Cases/Invoices/input_folder/invoice_4.pdf) in this repository (committed 2026-01-22) |
| Retrieved | 2026-09-25 (copied into this folder) |
| Clearance | Public. Cleared for website use on 2026-11-23 |

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An invoice is the bill a seller sends for goods or services delivered. It is the most
common business document in accounts payable, and every supplier lays it out
differently.

- **Accounts payable:** AP teams enter invoices, match them to purchase orders and
  receipts, and schedule payment.
- **Procurement and spend analytics:** buyers track prices, quantities and suppliers
  across line items.
- **Accounting firms and bookkeepers:** they post invoices to the ledger and reconcile
  them at period end.
- **Tax and audit:** auditors and tax teams check invoices for sales tax, such as HST
  here, and for supporting evidence.
- **Trade finance and factoring:** lenders verify invoices before they advance cash
  against receivables.

### What it contains

- **Bilingual labels,** each field captioned in French and English.
- **A line-item table** with item number, description, quantity, unit price, unit of
  measure and extension.
- **Small header tables** for account, purchase order, order dates, terms and shipping.
- **Separate sold-to and ship-to address blocks.**
- **A totals block** with subtotal, sales tax and total, with the currency printed under
  the total.
- **A company logo** and a contact block in bold italic type.
