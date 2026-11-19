# Auto Insurance Application

**On the website:** [landing.ai/document-type/auto-insurance-application](https://landing.ai/document-type/auto-insurance-application)

A completed Progressive Application for Massachusetts Motor Vehicle Insurance, written
through an independent agency. It lists the applicant, the drivers and the vehicle, the
coverages and premiums by policy part, the driving history, and the fees and payment
terms, and ends with the applicant's signed agreement.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 60 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:28 | 2026-11-19 02:27 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 14,492 | 15,158 |
| Words under 0.95 confidence | 32 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 1 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 7.5 s | 11.9 s |
| Per page | 1.2 s | 2.0 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 2.4 credits | 6.8 credits |
| Per page | 0.40 credits | 1.13 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:28 | 2026-11-19 02:27 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 60 | 60 |
| Non-null fields returned | 60 | 59 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 439.6 s | 131.0 s |
| Per schema field (60) | 7.33 s | 2.18 s |
| Per value returned | 5.50 s | 1.66 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 5.7 credits | 5.8 credits |
| Per schema field (60) | 0.095 credits | 0.097 credits |
| Per value returned | 0.071 credits | 0.073 credits |

## Origin

`source/progressive-ma-auto-application-redacted.pdf` is a completed Progressive
**Application for Massachusetts Motor Vehicle Insurance** (Form 7982 MA, 12/24 edition),
written through an independent agency. It is **6 pages, portrait**, a native PDF with a
text layer.

| | |
|---|---|
| Publisher | Progressive Casualty Insurance Co |
| Source | [scribd.com/document/1038741316](https://www.scribd.com/document/1038741316/AUTO-DOCS) |
| Retrieved | 2026-10-26, downloaded manually (Scribd blocks scripted downloads) |
| Clearance | **Redacted**, see below |

Scribd is not the publisher. An unknown user uploaded a 10-page "AUTO DOCS" packet that
was a real person's application, so it was treated as a personal record and redacted
before it entered the repo. What it contained, and what replaced it:

| Personal data | Occurrences | Replaced with |
|---|---|---|
| Applicant's full name | 9 | `JOHN Q SAMPLE` |
| Applicant's street address | 1 | `100 Main St` |
| Applicant's city, state and ZIP | 1 | `Mytown, MA 01890` |
| Garaging ZIP code | 2 | `01890` |
| Applicant's date of birth | 1 | `Jun 14, 1990` |
| Policy number | 8 | `325288425` (random, same shape) |
| VIN | 2 | `3FA6P0HD2FR401300` (make and model positions kept; check digit and serial random) |
| Registration plate | 1 | `2FSM98` (random, same shape) |
| Date of the at-fault accident | 1 | `Mar 6, 2025` |
| Agent's name | 1 | `PAT EXAMPLE` |
| Agency name, street, city/ZIP | 1 each | `ACME AGENCY`, `200 MAIN ST #100`, `ANYTOWN, MA 01880` |
| Agent code | 1 | `75S1F` (random, same shape) |
| Agency phone | 1 | `1-781-555-0112` (fiction-reserved range) |

The redaction removed the underlying text rather than drawing a box over it, then
re-extracted the PDF and checked that no original survived. A sweep of every file in
this folder, on literals and on runs of digits, found none of the originals.

Three more things were removed:

- **Hidden tracking text.** Every page carried a 1pt line in a white font holding the
  policy number, the agent code and Progressive's form-routing ids. It was invisible on
  the page but fully extractable, so it was removed outright.
- **DataGlyph codes.** Pages 5 and 6 carried a 2D code in the left margin, set as text
  in a DataGlyph font. It probably encoded the same routing data, so it was removed too.
- **Pages 7-10.** These were separate forms appended in the uploaded packet: an EFT
  authorization naming the bank account holder with partial routing and account
  numbers, an automatic payment schedule, a payment receipt with the card's last four,
  and the ID card. None is part of the 6-page application.

PDF metadata was cleared. Replacement text is set in Helvetica, slightly wider than the
form's condensed face, so a careful eye can spot the edited values on pages 1 and 3.
Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

An auto insurance application is where the applicant states who drives, what is driven
and how it is used, and signs to it before a policy is bound.

- **Personal lines insurers:** underwriters check the drivers, vehicles, driving
  history and prior insurance before they bind and price the policy.
- **Independent agencies:** agents complete applications for several carriers and keep
  them on file as the signed record of what the applicant stated.
- **Premium audit and fraud investigation:** investigators compare what was declared at
  application, such as garaging address and vehicle use, against a later claim.
- **Claims:** adjusters check a claim against the drivers and vehicles listed when the
  policy was written.
- **Premium finance and billing:** fee amounts and installment terms in the agreement
  set what the policyholder is charged.

### What it contains

- **A header block of label/value pairs** for the applicant, policy period and agency.
- **Per-driver and per-vehicle blocks** that repeat the same fields for each entry.
- **A coverage table** using Massachusetts' numbered policy parts, with limits,
  deductibles and premiums by line.
- **A driving-history table,** with sources split over two lines in one column.
- **Fee amounts inside agreement prose** on pages 5 and 6, not in a table.
- **A thin condensed typeface** throughout, set in a native text layer.
