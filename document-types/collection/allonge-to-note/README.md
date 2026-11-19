# Allonge to Note

**On the website:** [landing.ai/document-type/allonge-to-note](https://landing.ai/document-type/allonge-to-note)

An allonge to a VA-guaranteed mortgage note, filed as an exhibit in an Oregon
foreclosure. It is a separate sheet attached to the note that endorses it from PennyMac
Corp. to PennyMac Loan Services, LLC, without recourse. It identifies the note by its
property address and principal, and carries the endorser's signature.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 13 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:25 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 817 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 17.3 s |
| Per page | 17.3 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 0.8 credits |
| Per page | 0.80 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:25 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 13 |
| Non-null fields returned | 11 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 43.4 s |
| Per schema field (13) | 3.34 s |
| Per value returned | 3.95 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 0.6 credits |
| Per schema field (13) | 0.046 credits |
| Per value returned | 0.055 credits |

## Origin

`source/allonge-to-note-redacted.pdf` is an **allonge to a VA-guaranteed mortgage
note**. It endorses the note from PennyMac Corp. to PennyMac Loan Services, LLC, without
recourse. It is **1 page, portrait**, a raster scan with no text layer.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), page 12 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

The source is a 13-page sheriff's-sale packet with four document types: the writ of
execution (pages 1–2), the general judgment of foreclosure and sale (3–8), the
promissory note (9–11) and two allonges (12–13). This folder is page 12 only, the
allonge with a **specific** endorsement. Page 13 is a second allonge with a **blank**
endorsement, and it is not used. The note, writ and judgment have their own folders,
built from the same packet with the same stand-ins.

The packet is a public court record of a foreclosure on a deceased private borrower's
home, so three values on this page were replaced:

| Data | Replaced with |
|---|---|
| Borrower's name | `JOHN Q SAMPLE` |
| Property street address | `100 SAMPLE AVE` |
| Property ZIP code | `97000` |

"Portland, OR" is kept, because the court is Multnomah County's. The principal
($360,000) is kept: with the address and name gone, it identifies no one. The loan
number was already blacked out by whoever filed it, before scanning, and that blackout
is kept. The PennyMac authorized representative's name and signature are kept, because
they sign in a corporate capacity.

The page has no text layer and no vector glyphs, so the redaction was done in the
pixels. OCR located each string, the pixels were painted over in the paper's own tone,
and each stand-in was drawn at the original's cap height and ink color. The page was
then rebuilt from the edited image alone, so the original raster is not in the output.
The source's rotation and metadata were not carried over. The stand-ins are set in
Arial against the scan's Calibri, so they look slightly crisper than the text around
them. OCR of the output, and a sweep of every file in this folder, found none of the
original values. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An allonge carries an endorsement when the note itself has no room for one. A lender
proves it holds a note through this chain of endorsements, so an allonge is one of the
documents a foreclosure turns on.

- **Mortgage servicing and loan transfers:** servicers and investors track who holds
  each note as loans are sold and transferred.
- **Foreclosure attorneys and courts:** the plaintiff must show it holds the note, and
  the court reviews the endorsement chain before entering judgment.
- **Due diligence on loan sales:** buyers of loan pools check that each note's
  endorsements run unbroken to the seller.
- **Document custodians:** custodians that hold original notes for investors
  certify that each note file has its allonges in order.
- **Title insurance:** title examiners on foreclosed properties check that the
  foreclosing party had the right to enforce the note.

### What it contains

- **A scan with no text layer,** so every word has to be read from the page image.
- **Labeled lines** with the loan, borrower, property and principal values.
- **A specific endorsement** ("Pay to the order of") that has to be told apart from a
  blank one.
- **A blacked-out loan number,** redacted by the filer before scanning.
- **A large handwritten signature** that crosses the printed title line.
- **A partly handwritten exhibit stamp** marking the page's place in the court filing.
