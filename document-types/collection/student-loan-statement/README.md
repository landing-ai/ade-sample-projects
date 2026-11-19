# Student loan statement

**On the website:** [landing.ai/document-type/student-loan-statement](https://landing.ai/document-type/student-loan-statement)

A New Zealand Student Loan Statement from Inland Revenue (Te Tari Taake), showing the
balance as at 23 April 2023 in New Zealand dollars. It gives the borrower's identifiers,
tables of increases and decreases to the loan, the current balance, recent loan details
and the interest rates. The borrower's details were replaced with stand-in data.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 20 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 | 2026-11-19 03:55 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 5,263 | 5,405 |
| Words under 0.95 confidence | 6 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 4.7 s | 25.0 s |
| Per page | 1.6 s | 8.3 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.0 credits | 2.9 credits |
| Per page | 0.33 credits | 0.97 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:38 | 2026-11-19 03:55 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 20 | 20 |
| Non-null fields returned | 20 | 20 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 230.0 s | 61.0 s |
| Per schema field (20) | 11.50 s | 3.05 s |
| Per value returned | 6.77 s | 1.79 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.1 credits | 2.2 credits |
| Per schema field (20) | 0.105 credits | 0.110 credits |
| Per value returned | 0.062 credits | 0.065 credits |

## Origin

`source/student-loan-statement.pdf` is a **New Zealand government statement, not a US
servicer's.** Inland Revenue (Te Tari Taake), the New Zealand tax department, collects
student loans that StudyLink lends, and it sends borrowers a Student Loan Statement. The
statement here shows the balance as at 23 April 2023. It is **3 pages, portrait A4**,
with a text layer:

1. The borrower's identifiers and a loan summary: an "Increases to your loan" table, a
   "Decreases to your loan" table, and the resulting current balance.
2. Recent loan details: the balance on the previous statement and the new amounts since
   then (a single administration fee).
3. General information, including the current interest rate and the late-payment
   interest rate.

Amounts are in New Zealand dollars. The borrower identifier is an IRD number, New
Zealand's tax number, not an SSN or a servicer account number.

| | |
|---|---|
| Publisher | Inland Revenue (Te Tari Taake), New Zealand |
| Source | scribd.com/document/693402713/ViewFile-12 |
| Retrieved | 2026-10-03, downloaded manually by the operator because Scribd blocks scripted downloads |
| Clearance | Redacted |

Scribd is a user-upload site, not the publisher. This is a real borrower's statement, so
it was treated as a personal record. Personal data was removed **before anything was
parsed**. Everything was on page 1:

- **Borrower name** (1 line): replaced with the obviously fake `MISS JANE Q SAMPLE`.
- **Postal address** (2 lines): replaced with the obviously fake `100 MAIN ROAD` /
  `ANYTOWN AUCKLAND 1000`, keeping the New Zealand shape of suburb, city and four-digit
  postcode.
- **IRD number** (1): replaced with a stand-in of the same `NNN-NNN-NNN` shape, drawn at
  random. Its digits were chosen so that it fails the IRD check-digit algorithm on both
  the primary and secondary weights. It looks like an IRD number but cannot be a valid
  one.
- **Statement reference** (1): replaced with a random stand-in of the same shape (`L`
  followed by 10 digits).
- **Mailing barcode** (1): removed, with nothing drawn in its place. It sat above the
  address and was drawn as vector paths, not as text or an image.

The text replacements remove the underlying text rather than covering it, and the PDF
metadata was cleared. The replacements are set in Helvetica, while the original uses
Verdana, so they look slightly narrower than the text around them.

Kept exactly as printed: Inland Revenue's name and logo, its toll-free numbers,
StudyLink, every date, every amount and the interest rates. Pages 2 and 3 have no running
heads and no identifiers, so they are unchanged.

The output was verified in four ways: no original string or run of the original digits
can be extracted from the text layer, the raw PDF objects and streams, or the metadata;
no vector paths remain in the barcode area; the only image left is the Inland Revenue
logo; and the redacted pages were rendered and checked by eye before parsing. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A student loan statement shows what a borrower owes and how the balance has changed.
Government lenders and private servicers send them on a regular schedule.

- **Mortgage and consumer lending:** lenders count student loan balances and repayments
  when they assess a borrower's debts.
- **Tax agencies and loan servicers:** they issue statements and reconcile balances,
  fees and interest.
- **Financial advisers and budgeting services:** they gather loan balances to plan
  repayment.
- **Employers and payroll:** in New Zealand, employers deduct student loan repayments
  from wages, and payroll teams answer borrower queries.
- **Immigration and relocation:** borrowers moving overseas need their balance and
  interest terms for planning and applications.

### What it contains

- **A non-US government layout,** with NZ-format dates ("23 April 2023") and an IRD
  number in place of an SSN.
- **Two signed tables that must reconcile,** with increases printed positive and
  decreases negative.
- **The same balance in two places,** in a teal callout at the top and in a teal bar
  under the tables.
- **Interest rates stated in prose** on the information page.
- **A logo** and a born-digital text layer.
