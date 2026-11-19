# Closing Disclosure

**On the website:** [landing.ai/document-type/closing-disclosure](https://landing.ai/document-type/closing-disclosure)

The Consumer Financial Protection Bureau's filled sample of the TRID Closing Disclosure
for a purchase loan, dated April 15, 2013. It sets out the loan terms, projected payments
and costs at closing, itemizes every closing cost, calculates the cash to close,
summarizes the borrower's and seller's transactions, and ends with loan disclosures and
contact information.

| | |
|---|---|
| Pages | 5 |
| Fields in the extraction schema | 59 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 | 2026-11-19 02:41 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 24,067 | 24,731 |
| Words under 0.95 confidence | 53 | n/a |
| Words under 0.80 confidence | 4 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.7 s | 16.0 s |
| Per page | 1.5 s | 3.2 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.2 credits | 8.7 credits |
| Per page | 0.64 credits | 1.74 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 | 2026-11-19 02:41 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 59 | 59 |
| Non-null fields returned | 57 | 57 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 111.9 s | 696.3 s |
| Per schema field (59) | 1.90 s | 11.80 s |
| Per value returned | 1.80 s | 11.23 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 7.0 credits | 7.2 credits |
| Per schema field (59) | 0.119 credits | 0.122 credits |
| Per value returned | 0.113 credits | 0.116 credits |

## Origin

`source/closing-disclosure.pdf` is the Consumer Financial Protection Bureau's filled
sample of the **TRID Closing Disclosure** for a purchase loan, dated April 15, 2013. It is
**5 pages, portrait (US Letter)**, created digitally with a text layer: loan terms,
projected payments and costs at closing on page 1; itemized closing cost details on page
2; the cash-to-close calculation and summaries of the borrower's and seller's
transactions on page 3; loan disclosures and the escrow account on page 4; loan
calculations, other disclosures and contact information on page 5.

| | |
|---|---|
| Publisher | Consumer Financial Protection Bureau |
| Source | [files.consumerfinance.gov/f/201311_cfpb_kbyo_closing-disclosure.pdf](https://files.consumerfinance.gov/f/201311_cfpb_kbyo_closing-disclosure.pdf) |
| Retrieved | 2026-10-03 |
| Clearance | Public |

The CFPB links this file from its Closing Disclosure explainer page and publishes it for
general use. It is the same form content as Regulation Z Appendix H-25(B), without the
cover sheet. Every party is a specimen placeholder: the borrowers, sellers, Ficus Bank,
Epsilon Title Co., "Anywhere Street" and "Somewhere Drive" addresses, phone numbers such
as 123-456-7890 and made-up email domains. The file was downloaded directly by script.
No redaction was needed.

The PDF's text layer holds a filled-in Mortgage Broker column on page 5, with a company,
address, contact and IDs, but the column prints empty on the page. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

The Closing Disclosure is the federally required summary a borrower receives three days
before closing on most US mortgages. It is the final statement of the loan's terms and
every cost of the transaction.

- **Mortgage lending:** lenders issue it, and post-closing teams check it against the
  Loan Estimate for tolerance violations.
- **Title and escrow:** settlement agents balance the funds against it at closing.
- **Mortgage quality control and compliance:** reviewers audit loan files for TRID
  timing and accuracy.
- **Secondary market and loan purchase:** investors buying closed loans check the
  terms, fees and cash to close against the loan data.
- **Real estate agents and attorneys:** they review it with buyers and sellers before
  the closing.

### What it contains

- **A dense, regulated layout** of fixed sections, lettered A to N, across five pages.
- **Multi-column cost tables** with borrower-paid, seller-paid and paid-by-others
  columns, each split into at-closing and before-closing.
- **The same number in several places.** Closing costs and cash to close appear on page
  1 and again on pages 2 and 3, and the payment appears in two tables on page 1.
- **Totals that sum across pages:** page 1's totals are sums of page 2's sections.
- **Checkboxes and YES/NO answers** inside table cells, with terms written in prose.
- **Hidden text** in the text layer that does not print on the page.
