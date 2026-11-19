# Promissory Note

**On the website:** [landing.ai/document-type/promissory-note](https://landing.ai/document-type/promissory-note)

A residential mortgage note on the Fannie Mae / Freddie Mac Multistate Fixed Rate Note
(Form 3200), VA-guaranteed, recording a $360,000 loan at 3.875% over 30 years owed to
Mortgage Express, LLC. It sets out the principal, interest rate, monthly payment,
maturity, late charges and default terms, with the borrower's signature and initials on
every page.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 24 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:44 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 10,326 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 21.4 s |
| Per page | 7.1 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 4.1 credits |
| Per page | 1.37 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:45 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 24 |
| Non-null fields returned | 23 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 155.1 s |
| Per schema field (24) | 6.46 s |
| Per value returned | 6.74 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.9 credits |
| Per schema field (24) | 0.121 credits |
| Per value returned | 0.126 credits |

## Origin

`source/promissory-note-redacted.pdf` is a residential mortgage note on the Fannie Mae /
Freddie Mac Multistate Fixed Rate Note (Form 3200), VA-guaranteed. It records $360,000
at 3.875% over 30 years, owed to Mortgage Express, LLC. It is **3 pages, portrait,
scanned** at low resolution.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 9–11 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | Redacted |

It was filed as Exhibit 1 (pages 1–3 of 5) to a foreclosure judgment, in a
sheriff's-sale packet. Its allonge, the writ and the judgment from the same packet are
separate samples, and all four share the same stand-ins.

| Data | Replaced with |
|---|---|
| Borrower's printed name | `JOHN Q SAMPLE` |
| Borrower's handwritten signature | "John Q Sample" in a handwriting font |
| Borrower's handwritten initials, on every page | "JQS" in a handwriting font |
| Property house number and street | `100 Sample` (the printed "Ave" is kept) |
| Property ZIP code | `97000` |

The loan number, case number and MIN were blacked out by whoever filed it, before
scanning, and those blackouts are kept. The lender's office address and the loan
originator's name and NMLS ID are kept. They appear in a professional capacity, and NMLS
IDs are public registrations.

All of it was done in the pixels with `document-types/scripts/redact_scan.py`:

- **Signature and initials.** Each region was painted out and a stand-in redrawn in
  Indie Flower, an openly licensed handwriting font, in the region's own ink. The note
  still shows it was signed and initialled. Where the original strokes crossed a
  signature line or an initials line, that segment of line was redrawn. The redrawn
  signature line is a little heavier than the original segment beside it.
- **Bold.** The property address is printed in bold, so it was replaced in bold.
- **OCR variants.** The scan's small type reads "Ave" as "Avo" and "Jr." as "Yr.", so
  the replacement rules match the house number and street only and cover the misread
  variant of the name.

The redaction was verified by OCR of the output, on literals and bare digits. A separate
sweep of every file in this folder found none of the original values. Full provenance is
in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A promissory note is the borrower's promise to repay a loan and the core document of
every mortgage. It is read at origination, when the loan is sold and when it goes into
default.

- **Mortgage lending and servicing:** servicers board the principal, rate, payment and
  maturity date from the note.
- **Secondary market and loan acquisitions:** buyers and custodians check each note
  against the loan tape during due diligence.
- **Document custodians:** they certify that the original note and its endorsements are
  in the file.
- **Foreclosure and default law:** attorneys file the note as an exhibit to prove the
  debt and the right to enforce it, as here.
- **Title and court-record services:** they read notes filed in court and county
  records.

### What it contains

- **A standard uniform instrument in dense prose,** with the loan terms embedded in
  numbered sections.
- **A low-resolution scan with small type,** so some words are hard to read.
- **Handwritten signature and initials** on every page (here, stand-ins in a handwriting
  font).
- **Black boxes** over the loan number, case number and MIN, applied before scanning.
- **Bold text** in the property address and date line.
- **Handwritten exhibit labels** ("EXHIBIT 1, PAGE 1 OF 5") added for the court filing,
  plus scan specks and punch-hole marks.
