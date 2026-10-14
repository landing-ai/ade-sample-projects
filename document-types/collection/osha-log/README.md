# OSHA log

Source assets for `landing.ai/document-type/osha-log`.

## Sample document

`source/uw-madison-2025-osha-300a.pdf` — the University of Wisconsin-Madison's completed
**OSHA Form 300A, Summary of Work-Related Injuries and Illnesses** for calendar year 2025.
**1 page, landscape**, with a text layer: it is generated from the university's safety
records system by Crystal Reports, with a signature image in the certification block.

Form 300A is the annual summary of an employer's OSHA 300 injury and illness log. Every
covered establishment completes one, even with no cases, certifies it, and posts it for
employees from February 1 to April 30 of the following year. It is also what OSHA's
Injury Tracking Application collects, and what insurers and safety auditors ask for when
they want an employer's injury record.

| | |
|---|---|
| Publisher | University of Wisconsin-Madison, Office of Human Resources |
| Source | [hr.wisc.edu/…/2025-OSHA-300A.pdf](https://hr.wisc.edu/docs/workplace-posters/state/2025-OSHA-300A.pdf) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

UW-Madison HR publishes the yearly 300A on its Workplace Posters page
(hr.wisc.edu/required-postings/workplace-posters/), as the posting requirement intends.
The form is an aggregate: counts of cases, days and injury types, with no employee names
or case details. It is certified by a university official in an official capacity — a
signature image, the job title and an office phone number. None of these is featured. No
redaction was needed. The PDF metadata holds only the Crystal Reports creator, producer
and dates.

## Why this document

The collection's first **OSHA log**, and its first workplace-safety record:

- **A government form filled by a real employer**, not a specimen. Every number is a
  real count for a large workforce.
- **Lettered columns.** The values sit over the letters (G) to (M) that OSHA uses to
  refer to them, below multi-line headers that read differently from the field names.
- **Totals that must agree.** Cases by outcome (G+H+I+J) and cases by type (M1–M6) are
  two partitions of the same cases; both sum to 337 here.
- **Blank establishment codes.** Industry description, SIC and NAICS are empty, with
  printed example text ("e.g., SIC 3715") beside them that must not be extracted as a
  value.
- **Large comma-grouped numbers** — 46,120,878 hours — to be returned as integers.

## Featured fields: the inputs to an incidence rate

All on page 1. The request named no fields; its notes suggested these five, and all five
ground cleanly.

| Field | Value |
|---|---|
| Cases with days away from work (H) | 60 |
| Cases with job transfer or restriction (I) | 25 |
| Total days away from work (K) | 938 |
| Annual average employees | 34,321 |
| Total hours worked | 46,120,878 |

These are what an underwriter or safety reviewer computes from a 300A: the DART rate is
(H + I) × 200,000 ÷ hours worked, and K says how severe those cases were. The overlay
crosses both halves of the form, from the case boxes on the left to the employment box
on the right, and reads as one calculation.

## What it surfaced

**Every value is right.** All 29 extracted values match the form, including both
partitions of the 337 cases and the comma-grouped employment figures returned as
integers.

**Blank codes come back as empty strings, not null.** Industry description, SIC and
NAICS are typed string-or-null and are blank on the form; extraction returned `""` for
each. It correctly ignored the printed examples. These three read OFF in the grounding
check only because there is no value to find.

**The signature is transcribed.** The parse reads the signature image as the signer's
name and writes it in front of the title, so `certification.title` grounds to a line that
begins with the name. The value extracted is the title alone.

**Grounding on the count boxes is tight.** Each count sits in its own block, so the
crops show the number with its column letter beneath it. The two employment figures sit in
adjacent blocks, and each box covers only its own line.

## Extraction

**29 leaf fields**: form number, revision and year; the establishment's name, address and
industry codes; the four case counts (G–J); the two day totals (K, L); the six injury and
illness types (M1–M6); annual average employees and hours worked; and the certification
(signed, title, phone, date). All 9 top-level fields populate.

## Cost

**3.10 credits** at standard tier for 1 page, parse and extract together.

## Regenerating

```bash
curl -sSL -o document-types/collection/osha-log/source/uw-madison-2025-osha-300a.pdf \
  "https://hr.wisc.edu/docs/workplace-posters/state/2025-OSHA-300A.pdf"
.venv/bin/python document-types/scripts/run_ade.py osha-log                # 3.10 credits
.venv/bin/python document-types/scripts/run_ade.py osha-log --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py osha-log           # free
.venv/bin/python document-types/scripts/inspect_fields.py osha-log --page 1
```
