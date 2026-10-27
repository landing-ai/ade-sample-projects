# Auto Lease Agreement

Source assets for `landing.ai/document-type/auto-lease-agreement`.

## Sample document

`source/auto-lease-agreement-honda-florida-redacted.pdf` is a **Closed End Motor Vehicle
Lease (With Arbitration Provision)**, form HFS-UCL-FL-e-14 1/21: the Reynolds and Reynolds
LAW form that Honda Financial Services dealers in Florida use. This copy is the customer
copy of a real, executed lease of a new 2025 Honda Civic Sedan from AutoNation Honda Miami
Lakes, assigned to Honda Lease Trust, dated 3 December 2024.

**5 pages, portrait, US legal size (8.5 x 14 in), with a text layer.** Page 1 carries the
parties, the vehicle, and the federal Consumer Leasing Act disclosures: amount due at
signing, scheduled payments, other charges, total of payments, the itemization of the
amount due, and Item 7, the step-by-step calculation of the monthly payment. Page 2 has the
trade-in, the itemized gross capitalized cost, optional products, required insurance and
the lease term. Pages 3 and 4 are dense two-column terms and conditions. Page 5 has the
arbitration provision and the signature blocks. The filled values are typed in a narrow
sans-serif over light-blue field shading, and a faint "Customer Copy" watermark runs
diagonally across every page.

| | |
|---|---|
| Publisher | AutoNation Honda Miami Lakes (lessor), on the Reynolds and Reynolds LAW form for Honda Financial Services. Uploaded to Scribd by a third party |
| Source | [scribd.com/document/943516552/Contract](https://www.scribd.com/document/943516552/Contract) |
| Retrieved | 2026-10-26, downloaded manually by the operator (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

Scribd is a user-upload site, so the account that posted the lease is not its publisher.
The document was treated as a personal record from the start.

## Redaction

The lease was not redacted at source. Everything that identifies a person or the specific
vehicle was replaced with `document-types/scripts/redact.py`, which removes the underlying
text rather than drawing over it:

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
That check was done locally, not with a decoding service. The policy number is random digits
from `plausible.py`. Kept: the dealer and its address, the assignee, the insurer's name,
address and customer-service number, the lessees' city, state, ZIP and county, the signer's
job title, the lease date, and every financial term. PDF metadata was cleared.

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. Verified by redact.py's text and image checks, by eye on renders of pages 1, 2
and 5, and by `ship.py check --rules` over every file in this folder.

**A redact.py change came with this document.** The lease draws its field shading as
images inside form XObjects, which aborted the inline-image step even though nothing inline
lay in a signature region. It also places one signature image several times on a page, so
a second region tried to blank an image that was already blank. Both cases are now handled.

## Why this document

It is the consumer-finance version of a contract: a legal-size form whose most important
content is a chain of numbers.

- **The Item 7 calculation is arithmetic the page carries out in front of you.** Gross
  capitalized cost minus the capitalized cost reduction gives the adjusted capitalized cost.
  Subtracting the residual value gives depreciation. Adding the rent charge and dividing by
  the number of payments gives the base payment, and adding tax gives the total. Every
  extracted value checks out: 28,539.00 − 101.29 = 28,437.71; − 18,070.00 = 10,367.71;
  + 4,269.17 = 14,636.88; ÷ 36 = 406.58; + 28.46 = 435.04.
- **The operators sit in their own column** (`–`, `=`, `+`, `÷`) between the label and the
  value, and the labels run across the whole page width.
- **The same value appears many times.** 435.04 is the first payment, each following
  payment, the 6A3 line and the Item 7 total, so a field has to be tied to the right line.
- **Fill-in-the-blank sentences.** "Your first monthly payment of $435.04 is due on
  12/03/2024, followed by 35 monthly payments of $435.04, due on the 3rd of each month"
  holds five values in one sentence.
- **Most fields are `N/A`.** Trade-in, optional products and guarantor sections are filled
  with N/A, and the model has to leave them out rather than invent them.

## Featured fields

All on **page 1**, in Item 7:

| Field | Label | Value |
|---|---|---|
| `payment_calculation.gross_capitalized_cost` | Gross capitalized cost | 28539.00 |
| `payment_calculation.capitalized_cost_reduction` | Capitalized cost reduction | 101.29 |
| `payment_calculation.adjusted_capitalized_cost` | Adjusted capitalized cost | 28437.71 |
| `payment_calculation.residual_value` | Residual value | 18070.00 |
| `payment_calculation.total_scheduled_payment` | Total monthly payment | 435.04 |

Together they follow the path from the car's capitalized price to the monthly payment, so
the overlay reads as one calculation. No person's name is featured.

## Grounding notes

- **The schema has 55 leaf fields, and all of them were populated.** `inspect_fields.py`
  reports 59 because it counts each of the three write-in itemization rows separately.
  Every field has at least one `ok` citation on the page it belongs to.
- The Item 7 values ground to their own right-hand cells, each with its operator.
  The gross capitalized cost box covers two lines, because the value sits on the second
  line of a two-line label, but the value is inside it.
- A few citations are `OFF`. The first payment due date cites the right sentence ("on
  12/03/2024, followed by 35 monthly"), but it reads `OFF` there, and `ok` on its second
  citation, the "Lease Date: 12/03/2024" line, which supports the value without being
  where it is stated. The due day ("3rd") also cites the Lease Date line as a second
  source, and one property-damage citation lands on the following sentence. None of
  these is featured.
- The assignee has three citations: the Lessor's Acceptance block on page 5 (`ok`), the
  whole assignment sentence on page 1 (`OFF`), and the "Honda Lease Trust" blank in
  that sentence (`ok`).
- The disposition fee and total of scheduled payments ground to the whole fill-in
  paragraph, which contains the value, rather than to the amount alone.

## Credits

**33.30 credits** at standard tier (parse and extract, DPT-3 Pro, jobs API).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py auto-lease-agreement        # spends credits
.venv/bin/python document-types/scripts/run_ade.py auto-lease-agreement --extract-only
.venv/bin/python document-types/scripts/build_images.py auto-lease-agreement   # free
.venv/bin/python document-types/scripts/inspect_fields.py auto-lease-agreement
```
