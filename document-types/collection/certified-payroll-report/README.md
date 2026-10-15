# Certified Payroll Report

Source assets for `landing.ai/document-type/certified-payroll-report`.

## Sample document

`source/boli-wh-38-certified-payroll-sample.pdf`: a filled specimen of Oregon's form
WH-38, *Payroll/Certified Statement*, the certified payroll a contractor on a public
works project files with the public agency each pay period under Oregon's prevailing
wage law (ORS 279C.845); the form is also designed to meet the federal Davis-Bacon Act.
The Oregon Bureau of Labor and Industries (BOLI) Prevailing Wage Rate unit handed it to
the Oregon Legislature's Senate Labor and Business committee PWR work group on
October 23, 2019, and the handout is posted on oregonlegislature.gov. The same filled
sample appears on slides 9 and 10 of BOLI's 2024 certified payroll training deck.
**2 pages, landscape, text layer.**

The handout has 6 pages. Pages 1 to 4 are presentation slides and were dropped. Pages 5
and 6 are kept:

| Page | Content |
|---|---|
| 1 | The WH-38 payroll grid: contractor and project header, prime and subcontractor sections, and four worker blocks with daily OT/ST hours, rates, fringe benefits, gross, deductions and net |
| 2 | The certified statement on the reverse: signatory, contractor, project and period, deductions, and the Davis-Bacon fringe benefit section |

The certified statement was printed upside down in the handout. It was turned upright,
and both pages had their page rotation folded into the content, so the text runs left to
right on an unrotated page. Nothing on either page was otherwise moved.

| | |
|---|---|
| Publisher | Oregon Bureau of Labor and Industries (BOLI), Prevailing Wage Rate unit |
| Source | [oregonlegislature.gov handout, 2019-10-23 PWR work group](https://www.oregonlegislature.gov/committees/slb/WorkgroupDocuments/Susan%20Wooley,%20BOLI%20(handout)%20-%2010-23-19%20meeting.pdf) |
| Retrieved | 2026-10-14, downloaded by script |
| Clearance | **Redacted**, see below |

## Redaction

The workers are specimen joke names with no ID numbers, and the contractor is fictional.
But the specimen borrows the presenter's own name for the contractor's owner, signatory
and business name, carries two real-looking phone numbers, and gives the workers
plausible Portland street addresses, one of them a state office building. These were
replaced before anything was parsed:

| What | Replaced with | Count |
|---|---|---|
| Presenter's name, as the contractor owner and signatory (page 2) | `Jane Sample` | 2 |
| Contractor business name, which carried the presenter's surname (pages 1 and 2) | `Sample Construction` / `SAMPLE CONSTRUCTION` | 3 |
| Contractor phone, in a BOLI telephone exchange | `(971) 555-0136` | 1 |
| Public agency phone, of unknown origin | `(503) 555-0127` | 1 |
| Contractor street address and PO box number (city, state and ZIP kept) | `500 Pine St`, `PO Box 3569` | 2 |
| Four worker street addresses (city, state and ZIP kept) | `100 Main St`, `200 Oak St`, `300 Elm St`, `400 Ash St.` | 4 |

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. Worker names, the specimen CCB registration number, the public agency, the
project name, number and location, every date and every amount were left as published.
The public agency and project are a real public project, which is acceptable here.

The replacement used `document-types/scripts/redact.py`, unmodified, which removes the
underlying text rather than covering it. Two things needed care:

- **Rotated pages.** Both pages were stored as portrait pages with a `/Rotate` entry, and
  redact.py's boxes landed on a sliver of each match, leaving the original glyphs
  visible. Folding the rotation into the content first (PyMuPDF `remove_rotation`) fixed
  it.
- **Case-insensitive matching.** redact.py's search ignores case, so a mixed-case and an
  upper-case rule for the business name both fired on every occurrence and overprinted
  two stand-ins. Each page was therefore redacted separately with its own rules, and the
  two pages were joined afterwards and their metadata cleared.

The output was verified by redact.py's own re-extraction check, by eye on renders of both
pages, and by `ship.py check --rules` over every file in this folder. The PDF's metadata
is empty.

## Why this document

A certified payroll is the compliance record every contractor on a prevailing-wage
public works job files weekly, and filled ones from real contractors are payroll records
that are never published. This is the regulator's own specimen on the state form. It
tests:

- **A dense ruled grid with stacked rows.** Each worker is a five-row block: an OT row
  and an ST row of daily hours, rates and totals, then a schedule line, all sharing the
  worker's name, classification, gross, deductions and net cells.
- **Diagonally split cells.** Column (7) holds two values in one cell, divided by a
  diagonal rule: gross on this project in the upper left, gross for all work in the
  lower right.
- **A sub-table beside each block.** Columns (10) and (11) list each worker's fringe
  benefit plans, one per row, with a different count per worker (three, three, two,
  none).
- **Two-part document.** The payroll and the certified statement on its reverse must
  agree on contractor, project and period.

## Featured fields

Page 1 features two header values and one complete worker line: the project name, the
payroll number, and for the third worker (Laborer Gp 1, the only one with overtime) the
total straight-time hours, the gross wages for all work from the lower half of the
diagonal cell, and the net wages paid. Gross less itemized deductions equals that net.

The request suggested, as suggestions only, the project name and number, the pay period
dates, the contract amount, the payroll number with the prime contractor checkbox, and
one worker's total hours, gross and net. The project number shows inside the project-name
box. The pay period dates read `OFF` because they are normalized to `YYYY-MM-DD`, and the
end date's range points at the begin line. The prime contractor checkbox is a boolean
whose range points at the printed `[x] PRIME CONTRACTOR`, so it reads `OFF` too. The
contract amount grounds cleanly but would have made six fields. The first worker was
passed over because the specimen prints his net one cent off his gross less deductions.
The worker's name was deliberately not featured.

## Grounding notes

- The layout risks did not materialize. The parse rendered every diagonal cell as
  `$128.50 / $1,163.75` within one table cell, and extraction split both halves into the
  right fields for all four workers. Each fringe benefit row paired with its own worker,
  including the empty list for the fourth.
- The daily hours landed in the right weekday columns, including the third worker's
  single overtime hour on Saturday.
- The gross box covers the whole diagonal cell, so the crop shows both halves. The value
  sits in its lower right. `build_images.py` warned that OCR could not read the value
  inside the box; the crop was checked by eye and is right.
- The project-name box spans the whole header row, taking in the project number and
  type of work beside it.
- Blank cells come back as zeros and empty strings rather than the nulls the schema asks
  for: the blank subcontract amount is `0`, the blank subcontractor name and CCB number
  are `""`, and blank daily-hour cells and OT totals are `0`. An earlier extraction
  against the same parse returned a mix of `0` and null for the same cells.
- The parse put a stray `I` in an empty cell of the first worker block, apparently a
  ruling line.
- The specimen's own quirks were extracted as printed: the one-cent net, day header
  dates (2/4 to 2/10) that do not fall on the weekdays printed above them, and a two-week
  pay period against a one-week grid.
- The schema has 51 leaf fields (173 occurrences in this document). Extraction filled
  every top-level field.

## Credits

23.30 credits at standard tier: 10.40 for the parse and first extraction, then two
schema iterations with `--extract-only` at 6.50 and 6.40 (nullable daily-hours arrays,
then plain-object prime and subcontractor sections so every leaf is counted).

## Regenerate

```bash
.venv/bin/python document-types/scripts/run_ade.py certified-payroll-report     # spends credits
.venv/bin/python document-types/scripts/build_images.py certified-payroll-report
.venv/bin/python document-types/scripts/inspect_fields.py certified-payroll-report
```

The redaction is not reproducible from this folder by design, because its rules file
holds the originals.
