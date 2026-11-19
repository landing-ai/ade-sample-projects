# Schedule E

**On the website:** [landing.ai/document-type/schedule-e](https://landing.ai/document-type/schedule-e)

Page 1 of a completed tax-year 2020 IRS Schedule E (Form 1040), Supplemental Income
and Loss, from a mortgage insurer's lender training course. It reports one
single-family rental for a full year: rents received, each expense line from mortgage
interest and taxes to HOA dues and depreciation, and the net rental income.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 40 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:35 | 2026-11-19 03:52 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 6,977 | 7,219 |
| Words under 0.95 confidence | 33 | n/a |
| Words under 0.80 confidence | 9 | n/a |
| Words under 0.50 confidence | 4 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 20.2 s | 20.4 s |
| Per page | 20.2 s | 20.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.9 credits | 2.4 credits |
| Per page | 0.90 credits | 2.40 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:35 | 2026-11-19 03:52 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 40 | 40 |
| Non-null fields returned | 27 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 74.2 s | 83.3 s |
| Per schema field (40) | 1.86 s | 2.08 s |
| Per value returned | 2.75 s | 3.20 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.5 credits | 2.6 credits |
| Per schema field (40) | 0.062 credits | 0.065 credits |
| Per value returned | 0.093 credits | 0.100 credits |

## Origin

`source/ScheduleE.Form.2020.pdf` is a completed tax-year 2020 IRS Schedule E (Form 1040),
Supplemental Income and Loss, page 1 (Part I, rental real estate and royalties). It is
**1 page, portrait**: a single-family rental with a full year of fair rental days, rents,
mortgage interest, taxes, insurance, repairs, HOA dues and depreciation.

| | |
|---|---|
| Publisher | Enact Mortgage Insurance (formerly Genworth Mortgage Insurance) |
| Source | [content.enactmi.com/documents/training/course/ScheduleE.Form.2020.pdf](https://content.enactmi.com/documents/training/course/ScheduleE.Form.2020.pdf) |
| Retrieved | 2026-10-03, downloaded manually by the operator |
| Clearance | Public |

This is a training handout from a mortgage insurer's lender course. Enact's own deck
*Calculating Rental Income* titles its page 35 "Schedule E Handout", matching this file
on Enact's course-materials host, and the PDF metadata names Genworth Mortgage
Insurance, Enact's former name, as author.

The host answers scripted downloads with a bot check, so the operator downloaded the
file by hand on 2026-10-03. The URL above is still the source of record. The committed
file is byte-for-byte what was downloaded, metadata included.

It is a specimen: the filer is "Larry Landlord", the SSN is printed as `XXX-XX-XXXX`,
and the property is "8 Renters Way", a teaching address. No redaction was needed. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Schedule E is where US taxpayers report income from rental property, royalties and
pass-through entities. Part I, shown here, is the record of a rental property's income
and expenses.

- **Mortgage underwriting:** underwriters use Schedule E to qualify rental income,
  adding back depreciation and other non-cash items, as the course this copy comes from
  teaches.
- **Mortgage insurance:** insurers review the same income calculation when they insure
  the loan.
- **Tax preparation and accounting:** preparers carry each property's figures from year
  to year and reconcile them with the owner's records.
- **Real estate investing and property management:** investors and lenders compare
  rental performance across properties.
- **Commercial and DSCR lending:** lenders use reported rents and expenses to judge a
  property's cash flow.

### What it contains

- **Property columns.** Amounts sit in columns A to C beside a shared list of line
  labels, so each value belongs to both a row and a column.
- **A summary block** on lines 23 to 26 that repeats several of the per-property
  amounts.
- **Repeated values,** with the same figure printed up to three times on the page.
- **Amounts in tax-software style** with a trailing period (`73,900.`).
- **Yes/No checkboxes** for the 1099 questions on lines A and B, and a QJV checkbox.
- **Blank amount lines** for expenses the filer did not have.
