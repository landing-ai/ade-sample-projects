# Student loan statement

A **New Zealand government statement, not a US servicer's.** Inland Revenue (Te Tari
Taake), the New Zealand tax department, collects student loans that StudyLink lends, and
it sends borrowers a Student Loan Statement. The statement here shows the balance as at
23 April 2023. It has three portrait A4 pages:

1. The borrower's identifiers and a loan summary: an "Increases to your loan" table, a
   "Decreases to your loan" table, and the resulting current balance.
2. Recent loan details: the balance on the previous statement and the new amounts since
   then (a single administration fee).
3. General information, including the current interest rate and the late-payment
   interest rate.

Amounts are in New Zealand dollars. The borrower identifier is an IRD number, New
Zealand's tax number, not an SSN or a servicer account number.

## Sample document

| | |
|---|---|
| Publisher | Inland Revenue (Te Tari Taake), New Zealand |
| Source URL | https://www.scribd.com/document/693402713/ViewFile-12 (Scribd listing; show it as plain text, not as a link) |
| Retrieved | 2026-10-03, downloaded manually by the operator because Scribd blocks scripted downloads |
| Clearance | `redacted` |
| File | `source/student-loan-statement.pdf`, 3 pages, portrait, text layer |

Scribd is a user-upload site, not the publisher. This is a real borrower's statement, so
it was treated as a personal record.

### Redaction

Personal data was removed **before anything was parsed**. Everything was on page 1:

- **Borrower name** (1 line): replaced with the obviously fake `MISS JANE Q SAMPLE`.
- **Postal address** (2 lines): replaced with the obviously fake `100 MAIN ROAD` /
  `ANYTOWN AUCKLAND 1000`, keeping the New Zealand shape of suburb, city and four-digit
  postcode.
- **IRD number** (1): replaced with a stand-in of the same `NNN-NNN-NNN` shape, drawn at
  random. Its digits were chosen so that it **fails the IRD check-digit algorithm on
  both the primary weights (3,2,7,6,5,4,3,2) and the secondary weights
  (7,4,3,2,5,2,7,6)**. It looks like an IRD number but cannot be a valid one.
- **Statement reference** (1): replaced with a random stand-in of the same shape (`L`
  followed by 10 digits).
- **Mailing barcode** (1): removed, with nothing drawn in its place. It sat above the
  address and was drawn as 44 vector paths, not as text or an image. A redaction that
  affected only line art deleted it.

Text replacements went through `scripts/redact.py`, which removes the underlying text
rather than covering it. The barcode was removed with a one-off PyMuPDF script kept
outside the repo. The PDF metadata was cleared.

Kept exactly as printed: Inland Revenue's name and logo, its toll-free numbers, StudyLink,
every date, every amount and the interest rates. Pages 2 and 3 have no running heads and
no identifiers, so they are unchanged.

The output was verified in four ways:

- No original string, and no run of the original digits, can be extracted from the text
  layer, the raw PDF objects and streams, or the metadata.
- No vector paths remain in the barcode area.
- The only image left is the Inland Revenue logo.
- The redacted pages were rendered and checked by eye before parsing.

The replacements are set in Helvetica, while the original uses Verdana, so they look
slightly narrower than the text around them.

## Why this document

- **Not American.** The collection's loan statements so far are US servicer and lender
  documents. This one tests a non-US government layout, NZ-format dates ("23 April
  2023"), and a tax identifier with a different shape.
- **Two signed tables that must reconcile.** Increases are printed positive and
  decreases negative. The balance equals the increases total plus the decreases total.
  An extractor has to keep the signs and keep the two totals apart.
- **The same balance in two places.** The current balance appears in a teal callout at
  the top and in a teal bar under the tables.

## Featured fields: how the balance was reached

All on page 1:

| Field | Label |
|---|---|
| `increases[0].amount` | Compulsory course fees |
| `increases[2].amount` | Living costs |
| `decreases[1].amount` | Interest |
| `decreases[2].amount` | Salary and wage deductions |
| `current_loan_balance` (occurrence 1) | Current loan balance |

Together they read as one story: what was added to the loan, what came off it, and the
balance that results. Every featured field is an amount. The borrower name, IRD number
and reference are stand-ins and are not featured.

`current_loan_balance` is pinned to occurrence 1, the "Your current loan balance" bar
under the tables. Occurrence 0 is the same figure in the callout at the top, which the
parse treats as a graphic and describes in a figure block.

## Grounding on this document

- **Table rows ground cleanly.** All 12 row cells of the increases and decreases tables
  (label and amount) and both totals come back `ok` on page 1. The boxes cover the
  amount cell, which spans from the label column to the right margin, so the crops
  are wide but correct.
- **The totals needed a schema fix.** On the first extraction, `total_decreases` came
  back as the increases total ($29,131.69). After the schema descriptions said which
  bold total sits under which table, a re-extraction (`--extract-only`, no re-parse)
  returned -$2,678.73, grounded `ok`.
- **Dates ground `OFF`.** The issue date, the balance as-at date, the previous
  statement date and the transaction date all extract correctly. The schema normalises
  them to ISO (`2023-04-23`) while the page prints `23 April 2023`, so the boxed text
  does not contain the value. None is featured.
- **The late-payment interest rate grounds `OFF`.** Its range covers the sentence that
  introduces the rate but not the line where "6.9%" is printed. The value itself is
  correct.
- **IRD number and reference** ground `ok` as key-value pairs in the header.

Overall, 30 of the 36 extracted occurrences are `ok`. The schema has 20 leaf fields.

## Credits

7.40 credits at standard tier: 5.20 for the first parse and extract, and 2.20 for one
re-extraction after the schema fix.

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py student-loan-statement                  # parse + extract (spends credits)
.venv/bin/python document-types/scripts/run_ade.py student-loan-statement --extract-only   # re-extract against the committed parse
.venv/bin/python document-types/scripts/inspect_fields.py student-loan-statement
.venv/bin/python document-types/scripts/build_images.py student-loan-statement             # images, no API calls
```

The redaction cannot be regenerated from this repo by design. Its rules file maps the
original values to their stand-ins, so it is kept outside the repo.
