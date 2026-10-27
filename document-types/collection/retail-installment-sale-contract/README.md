# Retail Installment Sale Contract

Source assets for `landing.ai/document-type/retail-installment-sale-contract`.

## Sample document

`source/retail-installment-sale-contract-redacted.pdf` is **LAW form 553-CA-ARB-eps 7/16,
Retail Installment Sale Contract – Simple Finance Charge (With Arbitration Provision)**,
published by The Reynolds and Reynolds Company. It is the contract a car dealer
signs with a buyer who finances the purchase through the dealer. The dealer is the
original creditor and usually assigns the contract to a bank or finance company
afterwards. This is the California edition.

**7 pages, portrait, with a text layer (no fillable fields).** Page 1 has the
dealer letterhead, header reference numbers, buyer, co-buyer and seller boxes, the vehicle
row, the Federal Truth-in-Lending disclosure box, a six-row payment schedule and the
Statement of Insurance. Page 2 itemizes the amount financed (lines 1 to 7, with lettered
sub-items) beside the service contract, debt cancellation and trade-in panels. Pages 3 to
7 are terms, notices, signature blocks and the arbitration provision. They are mostly
boilerplate, with the seller name repeated on page 7.

The filled sample is a used 2020 GMC Terrain with 17,765 miles. It is financed at 23.99%
APR: $27,492.56 financed, a $12,706.64 finance charge, and 59 monthly payments of $503.32
plus a final payment of the same amount. Co-buyer, stock number, trade-in and insurance
are blank or zero, as in the original.

| | |
|---|---|
| Publisher | The Reynolds and Reynolds Company (the form). The filled-in values come from an unknown party. |
| Source | [scribd.com/document/969411605](https://www.scribd.com/document/969411605/553-ca-arb-eps-7-16-fnicentral-com-editable) |
| Retrieved | 2026-10-26, **downloaded manually** (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

The page should credit the form to Reynolds and Reynolds. It should not present the
filled-in contract as theirs. Scribd is a user-upload site, so the uploader is not the
publisher, and nothing establishes where the filled-in values came from. The document is
therefore treated as a personal record.

## Redaction

The contract carried a buyer's full name and home address, a VIN, and a named, real
dealership with its street address and logo. It also carried dealer, contract and R.O.S.
numbers. The dealership was anonymized as well as the buyer. A contract whose origin is
unknown should not be published as a named dealer's deal. Every value was replaced with
`document-types/scripts/redact.py`, which removes the underlying text rather than covering
it:

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

The dealership logo image in the page 1 header was removed. The Reynolds and Reynolds LAW
logo was kept, because it identifies the form. The stand-in VIN fails its check-digit test
(position 9), so it cannot belong to a real vehicle. Reference numbers were drawn by
`scripts/plausible.py`.

The dealer number had to be replaced in a separate step before `redact.py` ran. In that
span, PyMuPDF's text search returns two overlapping rectangles for one number, and the
standard pass drew the stand-in twice. The pre-pass replaced the span in place and left the
form's underline untouched. `redact.py` then ran the full rule set, and the dealer-number
rule found no remaining matches.

The PDF metadata was cleared. The originals are not recorded anywhere in this folder, and
the rules file stays outside the repo. Verified by redact.py's text check, by eye on a
render, and by `ship.py check --rules` over every file in this folder.

## Why this document

Auto lenders read these contracts in volume when they fund dealer paper. This sample has
several features that make it hard to read:

- **The same amount appears twice in different formats.** The Amount Financed is
  `27,492.56` in the page 1 disclosure and `27492.56` on line 7 of the page 2 itemization.
  Extraction grounded it to both.
- **Disclosure values are wrapped in form furniture.** A `$` sits to the left, an `(e)`
  estimate marker to the right, and the value rests on an underline. Three of them were
  typed with a second `$` inside the blank (`$ $12,706.64`).
- **A sparse payment schedule.** Only two of six rows are filled. The rest read `N/A`, and
  one filled row has its count (`59`) and its due description in different cells from the
  amount.
- **Dense itemization arithmetic.** Page 2 has about 40 lettered sub-lines feeding seven
  totals. Most extracted totals reconcile. Lines 1A to 1K sum to the Total Cash Price of
  19,969.56. Adding official fees and the emissions fee gives the Subtotal of 19,992.56.
  Sixty payments of 503.32 make the Total of Payments of 30,199.20.
- **The document does not agree with itself.** The printed Amount Financed (27,492.56,
  on page 1 and on line 7) is exactly 10,000.00 more than the document's own arithmetic
  supports. Line 5 less line 6 is 17,492.56, and so is the Total of Payments less the
  Finance Charge. Extraction reports what is printed, which is correct. A lender would want
  a cross-field check to catch this, and the extracted values are enough to run one. It
  also suggests that someone edited the filled-in values before uploading, which is one
  more reason to treat the file as an unknown record.
- **A placeholder in a value slot.** The Seller-Creditor box reads `DEALERSHIP NAME`.
  Extraction correctly took the seller's name from the letterhead instead, as the schema
  directs.

## Featured fields

All on **page 1**:

| Field | Label | Value |
|---|---|---|
| `truth_in_lending.annual_percentage_rate` | Annual percentage rate | 23.99 |
| `truth_in_lending.finance_charge` | Finance charge | 12706.64 |
| `truth_in_lending.total_of_payments` | Total of payments | 30199.20 |
| `truth_in_lending.total_sale_price` | Total sale price | 32699.20 |
| `payment_schedule[0].amount_of_payment` | Monthly payment | 503.32 |

Together they are the Truth-in-Lending box and the payment it produces. The overlay shows
one financing decision: the rate, what the credit costs, the total repaid, the total sale
price, and the monthly payment. All five are impersonal amounts. The buyer's name was not
featured. The five values also agree with each other: 60 × 503.32 = 30,199.20, and adding
the 2,500.00 down payment gives 32,699.20.

**Amount Financed was deliberately left out.** It grounds correctly, but its printed value
is the inconsistent one described above. Featuring it would put a figure on the page that
visibly contradicts the values beside it.

## Grounding notes

- **Every featured value grounds tightly.** Each box sits on the value's own disclosure
  cell, and the monthly payment sits on its schedule cell.
- **Page 2 itemization grounds cleanly.** All 16 itemization fields come back `ok`, each
  on its own `$ ___ (letter)` line.
- **Multi-line addresses ground to one line per occurrence.** `buyer.address` grounds
  as separate street and city lines. Two of its four occurrences wrongly land on the
  dealer's letterhead address, so the address fields are not featured.
- **Some values can only ground to nearby text.** The checkbox-derived
  `vehicle.business_use`, the inferred `number_of_payments = 1` for the "One final payment"
  row, and the blank `co_buyer_name` and `stock_number` ground to the label beside them.
  That is expected for a checkbox or an empty blank, but none of them can be illustrated.
- `truth_in_lending.down_payment` grounds to the Total Sale Price column header. The
  `2,500.00` sits inside that column's text, so the crop would show the whole header.

## Schema

`schema.json` has **45 leaf fields**. They cover the header reference numbers, seller,
buyer, co-buyer, the vehicle, the Truth-in-Lending disclosures, the payment schedule as an
array, the late charge terms, 16 lines of the page 2 itemization, and the governing-law
state. Every field extracted as printed (48 values, counting the two payment-schedule rows).

## Cost

23.30 credits at the standard tier (parse and extract, DPT-3 Pro, 7 pages).

## Regenerate

```bash
# redaction (rules file kept outside the repo)
.venv/bin/python document-types/scripts/redact.py <original>.pdf \
    document-types/collection/retail-installment-sale-contract/source/retail-installment-sale-contract-redacted.pdf \
    --rules <outside-the-repo>/rules.json --remove-images "1:470,0,535,60"

.venv/bin/python document-types/scripts/run_ade.py retail-installment-sale-contract
.venv/bin/python document-types/scripts/build_images.py retail-installment-sale-contract
```

The dealer-number pre-pass described above has to run before `redact.py`.
