# Auto loan statement

**On the website:** [landing.ai/document-type/auto-loan-statement](https://landing.ai/document-type/auto-loan-statement)

GM Financial's sample monthly statement for a retail auto loan on a 2021 GMC Acadia
Denali, dated September 15, 2022. It shows the amount due, the payment due date, recent
transactions, the current principal balance and loan term, a tear-off payment coupon,
and on the back how the last payment was split between principal and interest.

| | |
|---|---|
| Pages | 2 |
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
| Processed (UTC) | 2026-11-19 02:29 | 2026-11-19 02:29 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 8,260 | 8,968 |
| Words under 0.95 confidence | 28 | n/a |
| Words under 0.80 confidence | 5 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.8 s | 18.9 s |
| Per page | 3.4 s | 9.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.2 credits | 3.3 credits |
| Per page | 0.60 credits | 1.65 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:30 | 2026-11-19 02:29 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 23 | 23 |
| Non-null fields returned | 23 | 23 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 326.9 s | 91.4 s |
| Per schema field (23) | 14.21 s | 3.98 s |
| Per value returned | 14.21 s | 3.98 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.4 credits | 2.5 credits |
| Per schema field (23) | 0.104 credits | 0.109 credits |
| Per value returned | 0.104 credits | 0.109 credits |

## Origin

`source/gm-financial-sample-auto-loan-statement.pdf` is GM Financial's sample monthly
account statement for a retail auto loan on a 2021 GMC Acadia Denali, dated September
15, 2022. It is **2 pages, portrait, US Legal (8.5 × 14 in)**: page 1 is the statement
with a tear-off payment coupon, and page 2 is the reverse side with the payment
allocation, payment options, general disclosures and a contact-update coupon.

| | |
|---|---|
| Publisher | GM Financial |
| Source | [gmfinancial.com/…/Sample-Statement.pdf](https://www.gmfinancial.com/content/dam/gmf/myaccount/documents/Sample-Statement.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

This is the lender's own specimen, served from its own domain. It is plainly a template:
a large SAMPLE watermark, a dealer block of "Dealership name / Address line 1 / City,
State 01234 / 555-555-5555", business hours of "H a.m. to H p.m.", a lorem ipsum Account
Details block, and the placeholder borrower JOHN Q SMITH. The coupon's mailing address
is a commercial office address, not a residence. No redaction was needed.

The page content is used exactly as published. The PDF metadata's author field carried a
GM Financial employee's user ID, so the metadata (Info dictionary and XMP) was cleared.

The template does not agree with itself on dates. The header and transactions are dated
2022, the coupon's due date is October 15, 2020, and the payment allocation on page 2 is
dated 8/21/20 against 8/21/22 on page 1. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

An auto loan statement is the monthly record of what a borrower owes on a vehicle loan.
Borrowers hand it to third parties whenever the loan or the car changes hands.

- **Auto lending and refinancing:** a new lender reads the current balance and payment
  to price a refinance and arrange the payoff.
- **Mortgage and consumer underwriting:** underwriters count the monthly car payment in
  the borrower's debt-to-income ratio.
- **Dealerships:** when a financed car is traded in, the dealer needs the lender and the
  balance to pay off the old loan.
- **Loan servicing and collections:** servicers and their vendors reconcile payments,
  due dates and balances across accounts.
- **Personal finance and bankruptcy:** counselors, attorneys and trustees list the loan
  and its payment among the borrower's obligations.

### What it contains

- **A designed, marketing-style layout,** with the key loan facts set as a large-type
  header and a graphical Account Details panel with a payment progress bar, not in
  ruled tables.
- **A payment coupon that repeats the header values,** so the same amount appears more
  than once on the page.
- **A transaction table** and, on page 2, a payment allocation that splits the last
  payment into principal and interest.
- **Dates that disagree across the template,** printed in different formats.
- **Side-by-side text blocks,** such as a dealer name and address set in parallel lines.
- **A diagonal SAMPLE watermark** and placeholder template text.
