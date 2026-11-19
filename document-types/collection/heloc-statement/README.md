# HELOC statement

**On the website:** [landing.ai/document-type/heloc-statement](https://landing.ai/document-type/heloc-statement)

Manulife Bank's sample monthly statement for a Manulife One account for April 2023, an
all-in-one account that combines a home-equity line of credit with mortgage
sub-accounts. It shows the borrowing limit, available credit and outstanding balance,
the main account's transactions, three sub-account ledgers, summaries of money in,
money out and interest, and the account's interest rates.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 26 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:08 | 2026-11-19 03:15 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 11,318 | 12,071 |
| Words under 0.95 confidence | 34 | n/a |
| Words under 0.80 confidence | 13 | n/a |
| Words under 0.50 confidence | 7 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 21.2 s | 7.1 s |
| Per page | 4.2 s | 1.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.9 credits | 5.6 credits |
| Per page | 0.38 credits | 1.12 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:08 | 2026-11-19 03:15 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 26 | 26 |
| Non-null fields returned | 26 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 158.0 s | 217.1 s |
| Per schema field (26) | 6.08 s | 8.35 s |
| Per value returned | 1.12 s | 1.55 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 6.7 credits | 6.8 credits |
| Per schema field (26) | 0.258 credits | 0.262 credits |
| Per value returned | 0.048 credits | 0.049 credits |

## Origin

`source/manulife-one-sample-statement-wm0013e.pdf` is Manulife Bank's sample monthly
statement for a Manulife One account, April 2023. It is **5 pages, portrait (US
Letter)**: an account snapshot with a borrowings chart, the main account's transactions,
three sub-account ledgers, summaries of money in, money out and interest, and the
account's interest rates.

| | |
|---|---|
| Publisher | Manulife Bank of Canada |
| Source | [manulifebank.ca/…/manulife-bank-manulife-one-sample-statement-wm0013e.pdf](https://www.manulifebank.ca/content/dam/manulife-advisor-portal/documents/en/marketing-materials/bank/manulife-one/manulife-bank-manulife-one-sample-statement-wm0013e.pdf) |
| Retrieved | 2026-04-04, downloaded manually |
| Clearance | Public |

This is the bank's own specimen, from its advisor marketing materials. Every page is
marked "(For illustrative purposes only)", and page 5 says "This is a sample statement
only". The borrowers, mailing address and account number are placeholders ("Client name
1", "Client address", 1234567), and the representative is a placeholder name. No
redaction was needed.

The site answers scripted requests with a 403, so the file is the copy the document
owner downloaded by hand on 2026-04-04. Its embedded title, author (Manulife Bank) and
form number (WM0013E) match the URL.

Manulife One is an all-in-one account secured against the borrower's home: a revolving
home-equity line of credit (the $240,000 borrowing limit) combined with fixed- and
variable-rate mortgage sub-accounts, and used for everyday banking too. The PDF's own
metadata calls it a sample mortgage statement. It is filed here as a HELOC statement
because that is the closer description for a US reader: it has no payment coupon and no
principal, interest and escrow split. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A HELOC statement records a revolving line of credit secured by a home: the limit, what
has been drawn, what is still available, and the interest charged.

- **Mortgage lending and refinancing:** lenders read the outstanding balance and limit
  to calculate combined loan-to-value and plan payoffs.
- **Consumer and credit underwriting:** underwriters count the line and its payments in
  the borrower's debt obligations.
- **Bank operations and servicing:** servicers reconcile transactions, interest and
  balances across the line and its sub-accounts.
- **Financial advisors:** advisors review all-in-one accounts like this one when
  planning a client's debt repayment.
- **Title and closing:** escrow and closing agents need the balance to arrange payoff
  when the home is sold or refinanced.

### What it contains

- **A balance that runs backwards.** The running balance is borrowings, so money in
  makes it smaller and money out makes it larger.
- **Four ledgers:** a 27-row main account table and three sub-account tables (one
  fixed-rate, two variable), with interest moving between them.
- **A borrowings chart** in the account snapshot on page 1.
- **Figures that should agree and do not quite.** Three running balances in the main
  account differ from the arithmetic by a few dollars, and the four accounts' closing
  balances sum to $406.64 less than the snapshot's total.
- **Placeholder text** in place of names, addresses and the account number.
