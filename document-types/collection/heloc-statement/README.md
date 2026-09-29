# HELOC statement

Source assets for `landing.ai/document-type/heloc-statement`. The page title is
**HELOC Statement**, with HELOC capitalized.

## Sample document

`source/manulife-one-sample-statement-wm0013e.pdf` — Manulife Bank's sample monthly
statement for a Manulife One account, April 2023. **5 pages, portrait (US Letter)**: an
account snapshot with a borrowings chart, the main account's transactions, three
sub-account ledgers, summaries of money in, money out and interest, and the account's
interest rates.

| | |
|---|---|
| Publisher | Manulife Bank of Canada |
| Source | [manulifebank.ca/…/manulife-bank-manulife-one-sample-statement-wm0013e.pdf](https://www.manulifebank.ca/content/dam/manulife-advisor-portal/documents/en/marketing-materials/bank/manulife-one/manulife-bank-manulife-one-sample-statement-wm0013e.pdf) |
| Retrieved | 2026-04-04, downloaded manually |
| Clearance | Public |

The bank's own specimen, from its advisor marketing materials. Every page is marked
"(For illustrative purposes only)", and page 5 says "This is a sample statement only".
The borrowers, mailing address and account number are placeholders ("Client name 1",
"Client address", 1234567), and the representative is a placeholder name. No redaction
was needed.

The site answers scripted requests with a 403, so the file is the copy the document
owner downloaded by hand on 2026-04-04. Its embedded title, author (Manulife Bank) and
form number (WM0013E) match the url.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

**What Manulife One is.** An all-in-one account secured against the borrower's home: a
revolving home-equity line of credit (the $240,000 borrowing limit) combined with
fixed- and variable-rate mortgage sub-accounts, and used for everyday banking too, so pay
goes in and bills go out of the same balance that carries the debt. The PDF's own
metadata calls it a sample mortgage statement. It is filed here as a HELOC statement
because that is the closer description for a US reader: it has no payment coupon and no
principal, interest and escrow split. It was first built as the collection's bank
statement, and was moved here at the document owner's decision because it is not a
standard one.

The collection's first **HELOC statement**:

- **A balance that runs backwards.** The
  running balance is *borrowings*, so money in makes it smaller and money out larger. A
  schema that assumes a deposit balance gets the sign wrong.
- **Four ledgers.** A 27-row main account table and three sub-account tables (one
  fixed-rate, two variable), with interest moving between them.
- **Summaries that should agree with the detail,** and do not quite (see below).

## Featured fields: what a lender verifies

All on page 1. At the document owner's request, these are the fields a lender reads from
a HELOC statement:

| Field | Value |
|---|---|
| Institution | Manulife Bank |
| Maximum borrowing limit | $240,000.00 |
| Available credit | $85,853.51 |
| Statement date | 2023-05-01 |
| Outstanding balance | $154,146.49 |

The outstanding balance is the total borrowings at the end of the month, across the main
account and all three sub-accounts. All five were already in the schema, so extraction
was not re-run.

**The statement date is flagged, and correct.** It is extracted as the ISO date
2023-05-01 and grounds to the printed "Prepared on May 1, 2023", so `build_images.py`
warns that the value is not in the boxed text. It is the same date in another format; the
crop was checked by eye. The borrowing limit and available credit boxes are taller than
their values because those table cells carry extra space above the text.

An earlier version featured the snapshot's movement for the month instead, which
reconciles: $155,268.51 plus $3,967.76 out, less $5,089.78 in, is $154,146.49, a
reduction of $1,122.02.

## What it surfaced

**The sample does not fully add up, and extraction does not pretend it does.** Three of
the 30 April rows in the main account's running balance differ from the arithmetic by a
few dollars (after "Main account interest", the balance should be 94,529.61; it is printed
as 94,488.61). The four accounts' closing balances on pages 2 and 3 sum to $153,739.85,
$406.64 less than the snapshot's $154,146.49. Extraction returns every figure exactly as
printed, which is what a downstream reconciliation check needs: the discrepancy is
visible in the extracted data, not smoothed over.

**Every row of a 27-row table comes back.** All 27 main account transactions match the
page on date, description, amount and running balance, as do the three sub-accounts'
opening and closing balances, rates and interest.

**Two small misses.** Empty Money in and Money out cells come back as 0 rather than null,
though the schema asks for null. The account holders list includes the mailing panel's
"Client name" as well as the two borrowers.

**Dates are normalized.** The statement date and period come back as 2023-05-01 and
2023-04 from "Prepared on May 1, 2023" and "Statement for April 2023", so they are flagged
as not matching their boxed text, though they are right.

## Extraction

**26 leaf fields**, written when this was the bank-statement sample and unchanged: the
bank, product and account, the statement date and period, the account holders, the
eight-value snapshot, the main account's transactions, the sub-accounts and the interest
totals. Everything extracts correctly apart from the two small misses above.

## Cost

**12.60 credits** at standard tier for 5 pages: 5.70 to parse, 6.90 to extract.

## Regenerating

```bash
# The source is a manual download from the url; the site blocks scripted requests.
.venv/bin/python document-types/scripts/run_ade.py heloc-statement                # 12.60 credits
.venv/bin/python document-types/scripts/run_ade.py heloc-statement --extract-only # 6.90, schema iteration
.venv/bin/python document-types/scripts/build_images.py heloc-statement           # free
.venv/bin/python document-types/scripts/inspect_fields.py heloc-statement --page 1
```
