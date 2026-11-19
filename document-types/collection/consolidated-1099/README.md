# Consolidated 1099

**On the website:** [landing.ai/document-type/consolidated-1099](https://landing.ai/document-type/consolidated-1099)

A 2024 Edward Jones Consolidated 1099 Statement, the year-end tax package a brokerage
sends each account holder. It combines Forms 1099-INT, 1099-DIV, 1099-B, 1099-OID and
1099-MISC in one statement, with the 1099-B detail listing each security sold, its
dates, proceeds, cost basis and gain or loss.

| | |
|---|---|
| Pages | 13 |
| Fields in the extraction schema | 66 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:45 | 2026-11-19 02:49 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 50,968 | 55,047 |
| Words under 0.95 confidence | 93 | n/a |
| Words under 0.80 confidence | 34 | n/a |
| Words under 0.50 confidence | 9 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 16.5 s | 24.2 s |
| Per page | 1.3 s | 1.9 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.1 credits | 20.3 credits |
| Per page | 0.55 credits | 1.56 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:45 | 2026-11-19 02:49 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 66 | 66 |
| Non-null fields returned | 55 | 56 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 185.7 s | 243.3 s |
| Per schema field (66) | 2.81 s | 3.69 s |
| Per value returned | 0.79 s | 0.95 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 17.3 credits | 18.7 credits |
| Per schema field (66) | 0.262 credits | 0.283 credits |
| Per value returned | 0.074 credits | 0.073 credits |

## Origin

`source/consolidated-1099-edward-jones-redacted.pdf` is a 2024 Edward Jones
Consolidated 1099 Statement. It is **13 pages, landscape**.

| | |
|---|---|
| Publisher | Edward Jones |
| Source | [scribd.com/document/868128892](https://www.scribd.com/document/868128892/XXXX8634-Consolidated-1099-Statement-Figures-Are-Final-01-23-2025) |
| Retrieved | 2026-09-25 |
| Clearance | Redacted |

**The original was not redacted at source, despite the Scribd listing being titled
`XXXX8634`.** It carried a named individual's complete tax records. It was redacted
before it entered the repo:

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Recipient's full name | 11 | `JANE DOE` |
| Full brokerage account number | 10 | `000-00000-0-0` |
| Financial advisor's name | 1 | `PAT EXAMPLE` |
| Advisor's direct line | 2 | `(000) 000-0000` |
| Real last four of the TIN | 1 | `***-**-0000` |
| Home address | page 1 | page dropped |

This was done with `document-types/scripts/redact.py`, which uses PyMuPDF redaction
annotations. These **remove the underlying text** rather than drawing a box over it.
The script re-extracts afterwards and fails if any original string survives. It verified
clean, and a separate sweep over every file in this folder confirmed that none of the
original identifiers appear anywhere.

**The account number was also in the PDF metadata,** stored with its separators
stripped, so searches for the hyphenated form missed it. `redact.py` now clears the
metadata dictionary and XMP outright, and its verification compares digits as well as
literal strings.

**Page 1 was dropped rather than redacted.** It is a mailing panel with its text rotated
90°, so replacement text did not render cleanly, and it carried the home address.
Removing it deletes that data outright. With the cover gone, PDF page numbers match the
printed ones: page 4 of the file is "Page 4 of 10" on the page. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A consolidated 1099 is the year-end tax statement a brokerage sends every account
holder. It gathers several IRS information returns into one package, so it is a primary
record of investment income.

- **Tax preparation and accounting:** preparers carry dividends, interest and each sale
  from the 1099-B into the client's return.
- **Mortgage and consumer lending:** underwriters read it to verify investment income
  and assets.
- **Wealth management and financial planning:** advisors use it to review realized gains
  and income for the year.
- **Tax software and data aggregators:** they import the forms and transaction detail
  into returns and financial profiles.
- **Audit and tax resolution:** reviewers reconcile reported proceeds and cost basis
  against the return filed.

### What it contains

- **Several IRS forms in one statement:** 1099-INT, 1099-DIV, 1099-B, 1099-OID and
  1099-MISC, each with numbered boxes.
- **Ruled transaction tables** in the 1099-B detail, one row per sale, each with the
  security's description, CUSIP and symbol, dates, proceeds, cost basis and gain.
- **Section headers that carry values,** such as the holding period and covered status
  stated once above a group of rows.
- **Landscape pages** with small type and many columns.
- **Summary totals** that repeat figures from the detail pages.
