# Criminal background check

**On the website:** [landing.ai/document-type/criminal-background-check](https://landing.ai/document-type/criminal-background-check)

The first three pages of Accurate Background's sample US employment screening report.
They carry the overall result, the candidate information, a summary table of eleven
searches with their status, an SSN trace, and a county criminal search with one case
file, two felony charges, their dispositions and sentencing.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 34 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:46 | 2026-11-19 02:53 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 5,450 | 5,607 |
| Words under 0.95 confidence | 23 | n/a |
| Words under 0.80 confidence | 6 | n/a |
| Words under 0.50 confidence | 4 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 21.4 s | 7.3 s |
| Per page | 7.1 s | 2.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.0 credits | 3.0 credits |
| Per page | 0.33 credits | 1.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:46 | 2026-11-19 02:53 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 34 | 34 |
| Non-null fields returned | 34 | 34 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 70.2 s | 249.6 s |
| Per schema field (34) | 2.06 s | 7.34 s |
| Per value returned | 1.13 s | 4.03 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 3.2 credits | 3.2 credits |
| Per schema field (34) | 0.094 credits | 0.094 credits |
| Per value returned | 0.052 credits | 0.052 credits |

## Origin

`source/accurate-sample-background-check-report-redacted.pdf` is an employment
**background screening report** from Accurate Background, a consumer reporting agency.
It is the publisher's own US sample report, cut to **3 pages, portrait**: a native PDF
with a text layer, rendered from HTML. Page 1 has the FCRA and California disclosure
text in English and Spanish, a header band with the overall result ("Does Not Meet
Requirements") and order dates, and the candidate information block. Page 2 has the
requested-by block, client and reviewer notes, the summary table of all 11 searches with
their status badges, and the SSN trace. Page 3 has the **county criminal search for
Placer County, CA**: one case file with two felony charges, each with a disposition and
a sentencing block (jail, prison, fines, fees, costs, restitution, classes).

| | |
|---|---|
| Publisher | Accurate Background |
| Source | [content.cdntwrk.com/…](https://content.cdntwrk.com/files/aT0xNTIyMDYzJnY9MSZpc3N1ZU5hbWU9c2FtcGxlLWJhY2tncm91bmRjaGVja3JlcG9ydC11cyZjbWQ9ZCZzaWc9ZGQzOWQxZWVlOTdhMTNjOGE3NTc4MjBiNGZkNWM1NDg%253D) |
| Linked from | [accurate.com/resources/abm/sample-backgroundcheckreport-us](https://www.accurate.com/resources/abm/sample-backgroundcheckreport-us) ("Download PDF") |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Redacted |

This is the publisher's own sample, not a customer document. The subject is fictitious,
but shares a real actor's name, and the address used a real Chicago street and ZIP code.
Both were replaced with obvious stand-ins before parsing:

- The subject's name, in all four places it is printed, became **Doe, Jane** (uppercase
  where the original was uppercase).
- The street became **100 Main St**, the city **Anytown**, and the ZIP code a randomly
  drawn 5-digit stand-in.
- The requestor reference, which may be a staff surname, became **SAMPLE**.

The replacement used `document-types/scripts/redact.py`, which removes the underlying
text rather than covering it. The pages were redacted one at a time so each name kept
its capitalization, then merged. On the dark header band, the name was cleared and a
white Helvetica stand-in was written on the band. Document metadata was cleared.

Only **pages 1 to 3** are kept. Pages 4 to 16 cover employment, education, references, a
motor vehicle report (which returns a different, real-looking driver's identity), a drug
test, credit and global watch. They add personal data without adding anything to the
criminal record.

The SSN shown is the well-known specimen 123-45-6789 and is kept. The email and phone
were already masked at source, and the date of birth is fictitious, so they are kept too.
No replaced string is extractable from the committed PDF, and none appears anywhere in
this folder. The redaction rules file stays outside the repo. Accurate's site footer says
All Rights Reserved and states no reuse terms for the sample. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

A background check report is what a consumer reporting agency returns after it searches
court, identity and other records on a candidate. The criminal search is usually the
part that decides the outcome.

- **Employers and HR teams:** they review reports before a hire and run the adverse
  action process under the FCRA when a report does not meet requirements.
- **Staffing agencies:** they screen large numbers of candidates and track each search's
  status.
- **Property managers and landlords:** tenant screening includes criminal searches with
  the same case, charge and disposition structure.
- **Gig and transportation platforms:** drivers and contractors are screened before they
  are activated and again on a schedule.
- **Healthcare, education and finance:** regulated employers must screen staff and keep
  the reports as part of compliance records.

### What it contains

- **Nested records:** search, then case file, then charges, then sentencing, with a
  different set of sentencing items on each charge.
- **Status badges** (RECORD FOUND, COMPLETED - Discrepancy Found) set in colored pills
  rather than table text.
- **Label/value grids** built from nested HTML tables, three levels deep in the
  sentencing block.
- **A summary table** of eleven searches with their status.
- **Legal disclosure text in English and Spanish.**
- **White text on a dark header band** for the overall result and the candidate's name.
