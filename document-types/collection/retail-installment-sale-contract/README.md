# Retail Installment Sale Contract

**On the website:** [landing.ai/document-type/retail-installment-sale-contract](https://landing.ai/document-type/retail-installment-sale-contract)

A California retail installment sale contract on the Reynolds and Reynolds LAW form,
the contract a car dealer signs with a buyer who finances the purchase through the
dealer. This filled copy finances a used 2020 GMC Terrain at 23.99% APR. It holds the
parties and vehicle, the Truth-in-Lending disclosures, the payment schedule, an
itemization of the amount financed, and pages of terms and an arbitration provision.

| | |
|---|---|
| Pages | 7 |
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
| Processed (UTC) | 2026-11-19 03:31 | 2026-11-19 03:50 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 38,790 | 41,026 |
| Words under 0.95 confidence | 186 | n/a |
| Words under 0.80 confidence | 112 | n/a |
| Words under 0.50 confidence | 16 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.4 s | 19.4 s |
| Per page | 1.2 s | 2.8 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.0 credits | 13.8 credits |
| Per page | 0.71 credits | 1.97 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:31 | 2026-11-19 03:50 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 45 | 45 |
| Non-null fields returned | 43 | 43 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 198.0 s | 87.6 s |
| Per schema field (45) | 4.40 s | 1.95 s |
| Per value returned | 4.30 s | 1.90 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 9.2 credits | 9.6 credits |
| Per schema field (45) | 0.204 credits | 0.213 credits |
| Per value returned | 0.200 credits | 0.209 credits |

## Origin

`source/retail-installment-sale-contract-redacted.pdf` is **LAW form 553-CA-ARB-eps 7/16,
Retail Installment Sale Contract – Simple Finance Charge (With Arbitration Provision)**,
published by The Reynolds and Reynolds Company. It is the contract a car dealer signs
with a buyer who finances the purchase through the dealer. The dealer is the original
creditor and usually assigns the contract to a bank or finance company afterwards. This
is the California edition.

It is **7 pages, portrait, with a text layer (no fillable fields)**. Page 1 has the
dealer letterhead, header reference numbers, buyer, co-buyer and seller boxes, the
vehicle row, the Federal Truth-in-Lending disclosure box, a six-row payment schedule and
the Statement of Insurance. Page 2 itemizes the amount financed (lines 1 to 7, with
lettered sub-items) beside the service contract, debt cancellation and trade-in panels.
Pages 3 to 7 are terms, notices, signature blocks and the arbitration provision.

The filled sample is a used 2020 GMC Terrain with 17,765 miles. It is financed at 23.99%
APR: $27,492.56 financed, a $12,706.64 finance charge, and 59 monthly payments of
$503.32 plus a final payment of the same amount. Co-buyer, stock number, trade-in and
insurance are blank or zero, as in the original.

| | |
|---|---|
| Publisher | The Reynolds and Reynolds Company (the form). The filled-in values come from an unknown party. |
| Source | [scribd.com/document/969411605](https://www.scribd.com/document/969411605/553-ca-arb-eps-7-16-fnicentral-com-editable) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | Redacted |

The form is credited to Reynolds and Reynolds, but the filled-in contract is not
theirs. Scribd is a user-upload site, so the uploader is not the publisher, and nothing
establishes where the filled-in values came from. The document is therefore treated as a
personal record. The printed Amount Financed is also exactly $10,000.00 more than the
contract's own arithmetic supports, which suggests someone edited the values before
uploading.

The contract carried a buyer's full name and home address, a VIN, and a named, real
dealership with its street address and logo. It also carried dealer, contract and R.O.S.
numbers. The dealership was anonymized as well as the buyer, because a contract of
unknown origin should not be published as a named dealer's deal. Every value was
replaced with `document-types/scripts/redact.py`, which removes the underlying text
rather than covering it:

| What | Replaced with | Count |
|---|---|---|
| Buyer's full name | `JANE Q SAMPLE` | 1 |
| Buyer's street address | `100 MAIN ST` | 1 |
| Buyer's city, state and ZIP | `ANYTOWN, NV 89100` | 1 |
| Vehicle identification number | random digits, same shape | 1 |
| Dealership name (letterhead) | `SAMPLE BUICK GMC` | 1 |
| Dealership street address | `100 MAIN AVE` | 1 |
| Dealership city, state and ZIP | `ANYTOWN, TX` | 1 |
| Dealer number | random digits, same shape | 1 |
| Contract number | random digits, same shape | 1 |
| R.O.S. number | random digits, same shape | 1 |

The dealership logo image in the page 1 header was removed. The Reynolds and Reynolds
LAW logo was kept, because it identifies the form. The stand-in VIN fails its
check-digit test (position 9), so it cannot belong to a real vehicle. The dealer number
was replaced in a separate pre-pass, because the standard pass would have drawn its
stand-in twice.

The PDF metadata was cleared. The original values are not recorded anywhere in this
folder, and the rules file stays outside the repo. The redaction was verified by the
script's text check, by eye on a render, and by a rules check over every file in this
folder. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A retail installment sale contract documents a car purchase that the buyer finances
through the dealer. The dealer then sells the contract to a lender, which checks it
before funding.

- **Auto lenders and finance companies:** funding teams review contracts in volume
  before buying them from dealers.
- **Car dealerships:** finance and insurance offices prepare the contracts and fix
  errors that lenders send back.
- **Loan servicing:** servicers board the rate, payment schedule and vehicle details
  into their systems.
- **Compliance and audit:** reviewers check Truth-in-Lending disclosures and add-on
  products against the itemization.
- **Securitization and due diligence:** auditors sample contracts behind auto loan
  asset-backed securities.

### What it contains

- **The same amount in two formats.** The Amount Financed is `27,492.56` in the page 1
  disclosure and `27492.56` on line 7 of the page 2 itemization.
- **Disclosure values wrapped in form furniture.** A `$` sits to the left, an `(e)`
  estimate marker to the right, and the value rests on an underline. Three were typed
  with a second `$` inside the blank (`$ $12,706.64`).
- **A sparse payment schedule.** Only two of six rows are filled, the rest read `N/A`,
  and one row has its count and due description in different cells from the amount.
- **Dense itemization arithmetic,** with about 40 lettered sub-lines feeding seven
  totals on page 2.
- **Figures that do not agree,** since the printed Amount Financed does not match the
  itemization or the disclosure arithmetic.
- **A placeholder in a value slot.** The Seller-Creditor box reads `DEALERSHIP NAME`, so
  the seller's name has to come from the letterhead.
- **Pages of small-print terms,** checkboxes and signature blocks.
