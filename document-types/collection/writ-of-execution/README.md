# Writ of Execution

**On the website:** [landing.ai/document-type/writ-of-execution](https://landing.ai/document-type/writ-of-execution)

A writ of execution on real property issued by the Multnomah County Circuit Court in
Oregon. It orders the county sheriff to sell a foreclosed home to satisfy $450,797.72
under a General Judgment of Foreclosure and Sale. The sum, interest and return deadline
are set out in prose, under a dense caption and over a signed court seal. The
defendants' names and the property details were replaced with stand-in data.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 20 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 04:00 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 3,003 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 11.2 s |
| Per page | 5.6 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.8 credits |
| Per page | 0.90 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 04:01 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 20 |
| Non-null fields returned | 20 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 50.2 s |
| Per schema field (20) | 2.51 s |
| Per value returned | 2.18 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.6 credits |
| Per schema field (20) | 0.080 credits |
| Per value returned | 0.070 credits |

## Origin

`source/writ-of-execution-redacted.pdf` is a writ of execution on real property issued
by the Multnomah County Circuit Court. It orders the county sheriff to sell a foreclosed
home to satisfy $450,797.72 under a General Judgment of Foreclosure and Sale. It is **2
pages, portrait, scanned** on 28-line pleading paper.

| | |
|---|---|
| Publisher | Multnomah County Circuit Court record, posted by the Oregon State Sheriffs' Association sales site |
| Source | [oregonsheriffssales.org/…/384277-Writ.pdf](https://oregonsheriffssales.org/wp-content/uploads/2025/01/384277-Writ.pdf), pages 1–2 of 13 |
| Retrieved | 2026-10-02, by script |
| Clearance | **Redacted**, see below |

The writ heads a sheriff's-sale packet. The judgment it enforces, the note and the
note's allonge from the same packet are separate samples, and all four share the same
stand-ins.

It is a public court record, but the defendants are private individuals, so their names
and the property's identifying details were replaced:

| Data | Replaced with |
|---|---|
| Defendants in the caption: the borrower, his alias and three heirs | `JOHN Q SAMPLE`, `JOHN QUINCY SAMPLE`, `JAMES Q SAMPLE`, `JANE Q SAMPLE`, `JUNE Q SAMPLE` |
| Property house number and street | `100 Sample` |
| Property ZIP code | `97000` |
| Subdivision name in the legal description | `SAMPLE` |
| Case number (page header and caption) | `24CV32513` |
| Law firm's file number (footers) | `84-556087` |

Kept, because they appear in an official or professional capacity: the court and the
judgment creditor, the creditor's law firm and its attorneys of record, and the
signature across the court seal.

The replacements were made in the pixels of the scan, and the page was rebuilt from the
edited image alone. Names that wrap across caption lines were split the same way in the
stand-ins, and the filer's yellow highlighting on the address was kept. Verified by OCR
of the output, on literals and bare digits. A separate sweep of every file in this
folder found none of the original values. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A writ of execution is the court order that lets a sheriff seize and sell property to
satisfy a judgment. In a foreclosure it starts the sheriff's sale.

- **Foreclosure and creditors' rights law firms:** they request writs and track the sale
  and return deadlines.
- **Sheriffs' offices:** civil units read the writ to schedule and conduct the sale and
  file the return.
- **Mortgage servicers and lenders:** default teams follow each loan from judgment to
  sale.
- **Title insurers:** examiners review the writ and the sale record before insuring the
  property after a sheriff's sale.
- **Real estate investors:** buyers at sheriff's sales research the judgment amount and
  the property before bidding.

### What it contains

- **Money in prose:** the sum, the date it is stated as of, the post-judgment rate, the
  per-day interest and the return deadline all sit in two sentences.
- **A dense caption** with defendants' names that wrap across lines.
- **A court seal with a signature across it.**
- **28-line pleading paper** with line numbers in the margin.
- **Highlighter** over part of the text.
- **A scan,** so the text has to be read from the page image.
