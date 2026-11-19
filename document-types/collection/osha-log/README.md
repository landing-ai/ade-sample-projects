# OSHA log

**On the website:** [landing.ai/document-type/osha-log](https://landing.ai/document-type/osha-log)

The University of Wisconsin-Madison's completed OSHA Form 300A, the annual summary of
work-related injuries and illnesses, for calendar year 2025. It gives the number of
cases by outcome and by type, the total days away and on restriction, the annual average
number of employees and total hours worked, and an official's certification.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 29 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:20 | 2026-11-19 03:39 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 3,569 | 3,822 |
| Words under 0.95 confidence | 57 | n/a |
| Words under 0.80 confidence | 33 | n/a |
| Words under 0.50 confidence | 12 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 6.2 s | 8.4 s |
| Per page | 6.2 s | 8.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.6 credits | 1.5 credits |
| Per page | 0.60 credits | 1.50 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:20 | 2026-11-19 03:39 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 29 | 29 |
| Non-null fields returned | 26 | 26 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 117.3 s | 158.1 s |
| Per schema field (29) | 4.04 s | 5.45 s |
| Per value returned | 4.51 s | 6.08 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.5 credits | 1.6 credits |
| Per schema field (29) | 0.052 credits | 0.055 credits |
| Per value returned | 0.058 credits | 0.062 credits |

## Origin

`source/uw-madison-2025-osha-300a.pdf` is the University of Wisconsin-Madison's completed
**OSHA Form 300A, Summary of Work-Related Injuries and Illnesses** for calendar year
2025. It is **1 page, landscape**, with a text layer: it is generated from the
university's safety records system by Crystal Reports, with a signature image in the
certification block.

| | |
|---|---|
| Publisher | University of Wisconsin-Madison, Office of Human Resources |
| Source | [hr.wisc.edu/…/2025-OSHA-300A.pdf](https://hr.wisc.edu/docs/workplace-posters/state/2025-OSHA-300A.pdf) |
| Linked from | [hr.wisc.edu/required-postings/workplace-posters](https://hr.wisc.edu/required-postings/workplace-posters/) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

UW-Madison HR publishes the yearly 300A on its Workplace Posters page, as the posting
requirement intends. The form is an aggregate: counts of cases, days and injury types,
with no employee names or case details. It is certified by a university official in an
official capacity, with a signature image, the job title and an office phone number. No
redaction was needed. The PDF metadata holds only the Crystal Reports creator, producer
and dates. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Form 300A is the annual summary of an employer's OSHA 300 injury and illness log. Every
covered establishment completes one, even with no cases, certifies it, and posts it for
employees from February 1 to April 30 of the following year.

- **Workers' compensation insurers:** underwriters compute injury rates such as DART
  from the case counts and hours worked.
- **OSHA and state safety agencies:** OSHA's Injury Tracking Application collects the
  300A data from covered employers.
- **Safety and EHS teams:** they track injury rates year over year and across sites.
- **Procurement and contractor prequalification:** owners and general contractors ask
  bidders for their 300A to screen safety records.
- **Safety auditors and consultants:** they review the summary against the underlying
  300 log.

### What it contains

- **Lettered columns.** Values sit over the letters (G) to (M) that OSHA uses to refer
  to them, below multi-line headers that read differently from the field names.
- **Totals that must agree.** Cases by outcome (G+H+I+J) and cases by type (M1-M6) are
  two partitions of the same cases.
- **Blank establishment codes** with printed example text ("e.g., SIC 3715") beside
  them.
- **Large comma-grouped numbers,** such as 46,120,878 hours worked.
- **A certification block** with a signature image, title, phone and date.
- **A landscape form** with a text layer.
