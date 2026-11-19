# Project Schedule

**On the website:** [landing.ai/document-type/project-schedule](https://landing.ai/document-type/project-schedule)

The initial baseline schedule for the 95 Express Lanes Opitz Boulevard project in
Virginia, filed as an exhibit to a public-private partnership agreement. It combines a
schedule narrative with milestone and work breakdown tables, a six-page Primavera P6
Gantt chart, a monthly payment schedule and a projected cash curve.

| | |
|---|---|
| Pages | 18 |
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
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:44 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 109,071 | 111,054 |
| Words under 0.95 confidence | 641 | n/a |
| Words under 0.80 confidence | 363 | n/a |
| Words under 0.50 confidence | 175 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 36.9 s | 28.1 s |
| Per page | 2.0 s | 1.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 13.7 credits | 36.8 credits |
| Per page | 0.76 credits | 2.04 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:22 | 2026-11-19 03:45 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 29 | 29 |
| Non-null fields returned | 29 | 29 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 478.3 s | 389.6 s |
| Per schema field (29) | 16.49 s | 13.43 s |
| Per value returned | 1.69 s | 1.38 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 30.8 credits | 31.2 credits |
| Per schema field (29) | 1.062 credits | 1.076 credits |
| Per value returned | 0.109 credits | 0.110 credits |

## Origin

`source/exhibit-b-3b-opitz-boulevard-ramp-baseline-schedule.pdf` is the **initial
baseline schedule** for the 95 Express Lanes Opitz Boulevard project in Virginia. The
contractor, Shirley Contracting Company, LLC, built it in Oracle Primavera P6, and it is
filed as Exhibit B-3B of the executed I-95/I-395 (Fredex) public-private partnership
agreement. It is **18 pages, mixed orientation**, with a text layer throughout:

| Pages | Content | Layout |
|---|---|---|
| 1–8 | Schedule narrative: Table 01 (contract and schedule milestones), Table 02 (the WBS), staging, key assumptions | Portrait letter |
| 9 | Divider | Portrait letter |
| 10–15 | The P6 Gantt chart, "Page 1 of 6" to "6 of 6" | Landscape tabloid |
| 16–17 | Divider, then the monthly payment schedule | Portrait letter |
| 18 | Projected revenue (cash) curve | Rotated landscape |

| | |
|---|---|
| Publisher | Virginia Office of Transportation Public-Private Partnerships (schedule by Shirley Contracting Company, LLC) |
| Source | [p3.virginia.gov/…/Exhibit_B-3B_-_Initial_Opitz_Boulevard_Ramp_Baseline_Schedule.pdf](https://p3.virginia.gov/media/p3/documents/p3-agreements/i-95i-395fredex/Exhibit_B-3B_-_Initial_Opitz_Boulevard_Ramp_Baseline_Schedule.pdf) |
| Linked from | [p3.virginia.gov/p3-agreements/](https://p3.virginia.gov/p3-agreements/) |
| Retrieved | 2026-10-14, downloaded directly by script |
| Clearance | Public |

Virginia's P3 office posts executed agreements and their exhibits on its public
agreements page, which links this file directly. The schedule names organizations only
(the contractor, Transurban, VDOT, DEQ). It contains no individual's name, signature,
phone number or address, so nothing was redacted and the whole exhibit is kept as
published. The PDF metadata holds only the InDesign creator, producer and dates. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A baseline schedule is the contractor's committed plan for a project: what gets done,
in what order, when, and at what cost. Owners measure progress and payments against it.

- **Construction contractors:** schedulers build and update the baseline, and project
  managers track progress against it.
- **Public agencies and infrastructure owners:** owners review the baseline for
  approval and check monthly updates for delay.
- **Construction lenders and P3 investors:** they tie draws and payments to schedule
  milestones and the payment schedule.
- **Construction claims and dispute consultants:** delay analysts compare the baseline
  with as-built schedules to assign responsibility for late completion.
- **Project controls and PMOs:** teams pull milestones, float and costs into reporting
  tools.

### What it contains

- **A Primavera P6 Gantt chart** across six tabloid sheets, with a table of activities
  beside the bars.
- **A nested work breakdown shown by color and indentation,** from project to phase to
  stage, with each band carrying its own cost, duration, dates and float.
- **Bar labels that repeat each activity name,** cut off where the page ends.
- **Blank cells that mean something:** a milestone has a start or a finish, never both,
  and an asterisk marks a constrained date (`05-31-22*`).
- **Three views of the same contract:** the narrative's milestone table, the Gantt
  milestones and the payment schedule.
- **Mixed page sizes and orientations,** very small type on the tabloid sheets, and a
  rotated cash curve chart.
- **A project name spelled two ways** ("Opitz" and "Optiz") in the source.
