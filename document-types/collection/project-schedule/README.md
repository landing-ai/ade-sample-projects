# Project Schedule

Source assets for `landing.ai/document-type/project-schedule`.

## Sample document

`source/exhibit-b-3b-opitz-boulevard-ramp-baseline-schedule.pdf` is the **initial
baseline schedule** for the 95 Express Lanes Opitz Boulevard project in Virginia. The
contractor, Shirley Contracting Company, LLC, built it in Oracle Primavera P6, and it is
filed as Exhibit B-3B of the executed I-95/I-395 (Fredex) public-private partnership
agreement. **18 pages, mixed orientation**, with a text layer throughout:

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
| Retrieved | 2026-10-14, downloaded directly by script |
| Clearance | Public |

Virginia's P3 office posts executed agreements and their exhibits on its public
agreements page (p3.virginia.gov/p3-agreements/), which links this file directly. The
schedule names organizations only (the contractor, Transurban, VDOT, DEQ). It contains
no individual's name, signature, phone number or address, so nothing was redacted and
the whole exhibit is kept as published. The PDF metadata holds only the InDesign creator,
producer and dates.

## Why this document

This is the collection's first **project schedule**, and its first Gantt chart:

- **A real P6 export.** This is a contract baseline with real dates, durations,
  budgeted costs and float, not a template.
- **A nested WBS shown by colour.** The project rolls up through coloured band rows,
  from project to phase to sub-phase to stage, each with its own cost, duration, dates and
  float. The indentation and band colour show the level. Neither survives into text.
- **Gantt bars beside the table.** Every activity name is printed a second time as a bar
  label to its right, cut off where the page ends. The extraction must take the table's
  version.
- **Blank cells that mean something.** A milestone has a start or a finish, never both,
  and an asterisk marks a constrained date (`05-31-22*`).
- **Three views that must agree.** The narrative's milestone table, the Gantt milestones
  and the payment schedule describe the same contract. The payment schedule's grand total,
  $59,127,675.84, is the Gantt's top-level budget.
- **Very small type** on tabloid sheets, and a project name spelled both "Opitz" and
  "Optiz" in the source.

## Featured fields: the budget, the start and two milestones

All five are on page 10, the first Gantt page.

| Field | Value |
|---|---|
| Project budgeted total cost | $59,127,675.84 |
| Notice to Proceed (MS-1200) start | 08-15-22 |
| Open New Slip Ramp (MS-1500) finish | 12-05-23 |
| Open New Slip Ramp total float (critical) | 0 |
| Open Pedestrian Facility (MS-1450) total float | 367 |

These show what a scheduler reads first: the size of the job, the day work starts, and
how much slack the key dates have. The slip ramp opening is on the critical path, with no
float. The pedestrian facility, two rows above it, has more than a year to spare.

The request suggested seven values on this page, and all seven ground cleanly. A page
can feature only five, so the project duration (595 days) and the MS-1450 finish date
(07-14-23) were left out.

## What it surfaced

**The Gantt table extracts accurately.** All 19 milestones match the page, in order, with
their IDs, names, costs, durations, dates and float. Activity names come from the table,
not from the bar labels beside it. MS-1700's name ends in an unclosed parenthesis
because P6 cut it off there, and the extraction keeps it that way. All 26 rows of the
monthly payment schedule match the PDF digit for digit.

**WBS levels are lost in the markdown.** The parse turns each Gantt page into an HTML
table where every band row looks the same: a two-column name cell followed by the
figures. Only colour and indentation show the level, and both are lost. On the first
extraction, `wbs_summaries` left out the empty STAKEHOLDER / ADJACENT PROJECT
COORDINATION band and listed PROJECT CLOSEOUT at level 2, although it is a level-3 band
inside CONSTRUCTION. The schema then pointed the field at the narrative's Table 02, which
gives each level-2 element a one-letter code (RRC.A to RRC.G). Re-running extraction
alone (`--extract-only`) fixed it, and the seven bands now sum exactly to the project's
$59,127,675.84.

**Blank cells come back as empty strings.** The schema asks for null when a milestone has
no start or no finish. The committed extraction returns `""` for all 17
of them, each grounded to the empty cell itself. The first run returned a mix of `""`
and null. The `date_constrained` flag is right for both asterisked dates (MS-1000 and
MS-1900). It is a yes-or-no judgement about the row rather than printed text, so none
of its 19 values can be featured: 9 ground to a date cell, which does not contain the
word true or false, and 10 have no ranges.

**The narrative's milestone table grounds on one run and not the next.** On the first
extraction, Table 01's ten milestones grounded to their cells on page 2. On the
re-extraction, the values were the same but every item came back with no ranges. Nothing
on that table changed between the two runs. The schema edit touched only
`wbs_summaries`.

**The cost crop is harder to read.** The project budget sits in a dark-blue band row, and
the translucent yellow highlight looks muddier over dark blue than over white. The box is
in the right place.

## Extraction

**29 leaf fields**: the title block (schedule title, project, contractor, data date); the
project summary row (budgeted cost, duration, start, finish, total float); every project
milestone (ID, name, cost, duration, start, finish, constrained flag, total float); the
seven level-2 WBS bands; Table 01's contract milestones; and every row of the monthly
payment schedule plus its total. Dates are kept as printed (MM-DD-YY), so they match the
cells they ground to. All 7 top-level fields are populated.

## Cost

**104.50 credits** at standard tier: 71.70 for parsing and extracting the 18 pages, plus
32.80 for one extraction-only re-run after the schema change.

## Regenerating

```bash
curl -sSL -o document-types/collection/project-schedule/source/exhibit-b-3b-opitz-boulevard-ramp-baseline-schedule.pdf \
  "https://p3.virginia.gov/media/p3/documents/p3-agreements/i-95i-395fredex/Exhibit_B-3B_-_Initial_Opitz_Boulevard_Ramp_Baseline_Schedule.pdf"
.venv/bin/python document-types/scripts/run_ade.py project-schedule                # ~72 credits
.venv/bin/python document-types/scripts/run_ade.py project-schedule --extract-only # ~33 credits, schema iteration
.venv/bin/python document-types/scripts/build_images.py project-schedule           # free
.venv/bin/python document-types/scripts/inspect_fields.py project-schedule --page 10
```
