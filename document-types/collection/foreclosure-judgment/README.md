# Foreclosure Judgment

**On the website:** [landing.ai/document-type/foreclosure-judgment](https://landing.ai/document-type/foreclosure-judgment)

A General Judgment of Foreclosure and Sale from the Multnomah County Circuit Court in
Oregon, with its Certificate of Readiness. It orders a foreclosed home sold and awards
the lender $443,537.60 plus fees and costs. The award is set out in a table of
principal, interest, charges and fees, surrounded by numbered findings and orders.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 30 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:06 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 10,682 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 15.6 s |
| Per page | 2.6 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 5.7 credits |
| Per page | 0.95 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:06 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 30 |
| Non-null fields returned | 30 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 128.3 s |
| Per schema field (30) | 4.28 s |
| Per value returned | 3.89 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.4 credits |
| Per schema field (30) | 0.113 credits |
| Per value returned | 0.103 credits |

## Origin

`source/foreclosure-judgment-redacted.pdf` is a **General Judgment of Foreclosure and
Sale** from the Multnomah County Circuit Court, with its Certificate of Readiness under
UTCR 5.100. It orders a foreclosed home sold and awards the lender $443,537.60 plus fees
and costs. It is **6 pages, portrait**, a scan on 28-line pleading paper.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 3–8 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

It sits in a 13-page sheriff's-sale packet with the writ that enforces it, the note and
the note's allonge. Only the judgment and its certificate of readiness are used here.
All four documents are separate samples sharing the same stand-ins.

The judgment is a public court record, but the defendants are a deceased private
borrower's heirs, so these values were replaced:

| Data | Replaced with |
|---|---|
| The borrower's and defendants' names: caption, default recital, paragraphs 2 and 3 | `JOHN Q SAMPLE`, `JOHN QUINCY SAMPLE`, `JAMES Q SAMPLE`, `JANE Q SAMPLE`, `JUNE Q SAMPLE` (title case in body text) |
| Property house number and street | `100 Sample` |
| Property ZIP code | `97000` |
| Subdivision name in the legal description | `SAMPLE` |
| Deed of trust recording number | `2019-201618` |
| Case number | `24CV32513` |
| Law firm's file number (every footer) | `84-556087` |

Kept, because they appear in an official or professional capacity:

- the court, the judge and the plaintiff
- the plaintiff's law firm and its attorneys of record
- their signatures

The money award is kept too: with the parties and the property replaced, it identifies
no one.

The pages are scans, so the redaction was done in the pixels. OCR located each value,
the stand-in was drawn in its place, and the pages were rebuilt from the edited images
alone. OCR of the output, on literals and bare digits, and a separate sweep of every
file in this folder found none of the original values. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A judgment of foreclosure is where the court sets out the money owed on a defaulted
mortgage and orders the property sold to pay it.

- **Mortgage servicing and default management:** servicers track the judgment amount,
  interest rates and sale terms for each foreclosed loan.
- **Foreclosure law firms:** attorneys draft the judgment and use its figures to prepare
  the writ and the sale.
- **Sheriffs and sale officers:** the sale is conducted under the judgment, and its
  amounts set the credit bid and the payoff.
- **Title insurance:** examiners confirm the judgment, the parties and the legal
  description before insuring a post-foreclosure sale.
- **Distressed-property investors:** buyers at sheriff's sales read the judgment to
  understand what is being sold and what liens are cut off.

### What it contains

- **A ruled award table** of principal, interest, charges and fees, with nested
  sub-items and a negative amount in parentheses.
- **A table that continues across a page break,** with its subtotal and total on the
  next page.
- **A second table** listing fees and costs.
- **Five pages of numbered findings and orders** in legal prose, with dates, rates and
  amounts inside sentences.
- **A caption** whose party names wrap across lines.
- **A scan on pleading paper** with numbered margin lines and no text layer.
- **A proxy signature and timestamp** for the judge, and attorney signatures.
