# Shop Drawing

**On the website:** [landing.ai/document-type/shop-drawing](https://landing.ai/document-type/shop-drawing)

A reinforcing steel (rebar) shop drawing submittal for the Turnbull School Music Room
Addition in Ottawa: sheets P1 Footing and P2 Foundation at Rev 2, returned with review
stamps. Each 36×24 in sheet has a foundation plan or wall elevations with bar callouts,
a bar list and bending schedule, bend-shape diagrams, concrete and lap tables, a title
block, and review stamps from the architect, the structural engineer and the general
contractor.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 35 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:37 | 2026-11-19 03:52 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 27,338 | 27,856 |
| Words under 0.95 confidence | 100 | n/a |
| Words under 0.80 confidence | 36 | n/a |
| Words under 0.50 confidence | 15 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 24.3 s | 26.9 s |
| Per page | 12.2 s | 13.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.1 credits | 8.0 credits |
| Per page | 1.55 credits | 4.00 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:37 | 2026-11-19 03:53 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 35 | 35 |
| Non-null fields returned | 35 | 35 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 197.1 s | 214.1 s |
| Per schema field (35) | 5.63 s | 6.12 s |
| Per value returned | 0.93 s | 1.01 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.7 credits | 11.8 credits |
| Per schema field (35) | 0.334 credits | 0.337 credits |
| Per value returned | 0.055 credits | 0.056 credits |

## Origin

`source/181113-HOBIN-Returned-P1-P2-REV2-Rebar.pdf` is a reinforcing steel (rebar) shop
drawing submittal for the Turnbull School Music Room Addition in Ottawa. It holds sheets
P1 Footing and P2 Foundation at Rev 2, returned with review stamps. It is **2 pages,
landscape, 36×24 in (2592×1728 pt)**. AGF Steel Ottawa, the rebar fabricator, drew them.
Cunliffe & Associates (structural engineer) and Hobin Architecture reviewed them, and
TalCo Building Innovations, the general contractor, both stamped and posted them. The
bar list, plan callouts and title block are stroked CAD text with no text layer; the red
review comments and two of the stamps have real text.

Each sheet carries:

- a foundation plan or wall elevations with bar callouts
- a bar list and bending schedule (quantity, size, bar mark, bend type, bending
  dimensions A–O)
- bend-shape diagrams
- concrete strength, cover and Class B lap tables
- a revision block and the fabricator's title block
- three review stamps: the architect's red stamp (REVIEWED, ticked), the engineer's
  black stamp (REVIEWED AS NOTED, checked, with initials and a date), and the
  contractor's flattened REVIEWED stamp

| | |
|---|---|
| Producer | AGF Steel Ottawa; reviewed by Cunliffe & Associates and Hobin Architecture |
| Posted by | TalCo Building Innovations Ltd. (general contractor) |
| Source | [tal-co.com/wp-content/uploads/2018/11/181113-HOBIN-Returned-P1-P2-REV2-Rebar.pdf](https://tal-co.com/wp-content/uploads/2018/11/181113-HOBIN-Returned-P1-P2-REV2-Rebar.pdf) |
| Linked from | [TalCo's DRC Shop Drawings page for the project](https://tal-co.com/project-management/turnbull-school-music-room-addition/drc-shop-drawings/), which lists 32 returned submittals |
| Retrieved | 2026-10-14, downloaded by script |
| Clearance | Redacted |

**Clearance.** TalCo posts this file in public on purpose: it is one of the 32 returned
submittals on the open project page. TalCo is a party to the project but did not produce
the drawing. AGF drew the sheets and Cunliffe and Hobin stamped them, so those firms hold
any copyright. No licence terms are stated, and no copyright notice appears on the AGF
sheets. Because the poster is not the producer, the file was treated the way this
collection treats user-upload sources: everything that identifies an individual was
replaced. The operator cleared it on that basis on 2026-10-14.

**What was changed.** Page 1 of the original was dropped. It was Hobin's transmittal
cover letter: a letterhead with the partners' names, a sender, and a recipient's name
and email. On the two remaining sheets, individuals were replaced with obvious
stand-ins:

| What | Where | Replaced with |
|---|---|---|
| Contractor reviewer's name | flattened REVIEWED stamp | `Pat Sample` |
| Architect reviewer's name | Hobin review stamp | `Jane Q Sample` |
| Engineer checker's initials | Cunliffe review stamp | `JD` |
| Detailer's initials | revision block and DETAILED BY box | `J.DOE` |
| Detailer's work email | AGF title block | `detailer@example.com` |
| Direct phone extension | AGF title block | a random 4-digit extension |

Firm names, the fabricator's office address and main phone number, the project, every
date and every engineering value are unchanged. Document metadata and the tagged-PDF
structure tree were cleared: after page 1 was deleted, its accessibility tags still held
a name and an email address, readable in the file but not on any page.

The stamps have a text layer, so they were redacted through it. The title-block text is
stroked vector glyphs, so it was located by OCR and the glyph paths were removed. Both
methods were verified, by text extraction and by OCR, and the folder was then swept for
the originals. The rules file was kept outside the repo.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A shop drawing is the fabricator's detailed plan of what it will make and install.
Before fabrication starts, it goes to the design team for review, and it comes back
stamped.

- **General contractors:** they collect, log and route submittals and track each
  review status, as TalCo does here.
- **Architects and structural engineers:** they review shop drawings against the
  design and stamp them reviewed, reviewed as noted, or revise and resubmit.
- **Rebar and steel fabricators:** they produce bar lists and bending schedules that
  drive cutting and bending in the shop.
- **Owners and project managers:** they keep returned submittals as part of the
  project record.
- **Construction software and estimating:** bar lists feed quantity takeoffs and
  material tracking.

### What it contains

- **Large-format sheets** at 36×24 in, with small text relative to the page.
- **A sparse 18-column bar list,** with narrow columns and a bending-dimension group
  whose filled cells depend on the bend type.
- **Plans and elevations** with bar callouts such as `V 23 15M A11 @400`.
- **Three review stamps side by side,** each with a different outcome ticked.
- **Mixed text layers.** Stroked CAD text with no text layer sits beside real text, and
  the engineer's stamp uses a font with no Unicode mapping.
- **Tables inside a CAD sheet:** concrete, cover and lap tables, a revision block and a
  title block.
