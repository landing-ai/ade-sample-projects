# Shop Drawing

Source assets for `landing.ai/document-type/shop-drawing`.

## Sample document

`source/181113-HOBIN-Returned-P1-P2-REV2-Rebar.pdf`: a reinforcing steel (rebar) shop
drawing submittal for the Turnbull School Music Room Addition in Ottawa. It holds sheets
P1 Footing and P2 Foundation at Rev 2, returned with review stamps. **2 pages, landscape,
36×24 in (2592×1728 pt).** AGF Steel Ottawa, the rebar fabricator, drew them.
Cunliffe & Associates (structural engineer) and Hobin Architecture reviewed them, and
TalCo Building Innovations, the general contractor, both stamped and posted them.

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

### Clearance

TalCo posts this file in public on purpose: it is one of the 32 returned submittals on
the open project page. TalCo is a party to the project but did not produce the drawing.
AGF drew the sheets and Cunliffe and Hobin stamped them, so those firms hold any
copyright. No licence terms are stated, and no copyright notice appears on the AGF
sheets. Because the poster is not the producer, the file was treated the way this
collection treats user-upload sources: everything that identifies an individual was
replaced. The operator cleared it on that basis on 2026-10-14.

### What was changed

- **Page 1 of the original was dropped.** It was Hobin's transmittal cover letter: a
  letterhead with the partners' names, a sender, and a recipient's name and email. It
  adds nothing a shop drawing needs.
- **On the two remaining sheets, individuals were replaced with obvious stand-ins:**

  | What | Where | Replaced with |
  |---|---|---|
  | Contractor reviewer's name | flattened REVIEWED stamp | `Pat Sample` |
  | Architect reviewer's name | Hobin review stamp | `Jane Q Sample` |
  | Engineer checker's initials | Cunliffe review stamp | `JD` |
  | Detailer's initials | revision block and DETAILED BY box | `J.DOE` |
  | Detailer's work email | AGF title block | `detailer@example.com` |
  | Direct phone extension | AGF title block | a random 4-digit extension |

- **Unchanged:** firm names, the fabricator's office address and main phone number,
  the project, every date, and every engineering value.
- **Document metadata and the tagged-PDF structure tree were cleared.** After page 1
  was deleted, its accessibility tags survived. They still held a name and an email
  address as `/ActualText`, readable in the file but not on any page. `ship.py check`
  caught this, and `pdfmeta.py` now strips the structure tree in every redaction
  script.

The stamps have a text layer, so they were redacted with `redact.py`. The title-block
text is stroked vector glyphs with no text layer, so it went through
`redact_outlined.py`. Both tools verified that no original survives: `redact.py` by text
extraction, `redact_outlined.py` by OCR. The folder was then swept with `ship.py check`.
The rules file was kept outside the repo.

On the first pass, OCR read the extension on sheet P2 but missed it in the matching
step. A second rule that included the `Ext.` label caught it.

## Why this document

The collection already has `engineering-drawing`: a set of municipal standard details,
one drawing per letter-size sheet. This document differs from it in three ways:

- **It is a fabrication document.** The bar list is a real 18-column schedule, mostly
  empty, with narrow columns and a bending-dimension group whose filled cells depend on
  the bend type.
- **It is large format.** The sheets are 36×24 in, and the text is small relative to
  the page.
- **It carries review state.** Three firms stamped it, side by side, with a different
  outcome ticked on each.

It also mixes layers. The bar list, plan callouts and title block are stroked CAD text
with no text layer. The red review comments and two of the stamps are real text. The
engineer's stamp uses a font with no Unicode mapping, so even its text layer is
unreadable.

## Extraction

`schema.json` has 35 leaf fields:

- project, contractor and fabricator (name, address, contract number)
- per sheet: number, drawing title, scale, latest revision, the engineer's and the
  architect's review (firm, status, date), and every bar list row (quantity, size, bar
  mark, bend type, dimensions A–K)
- the concrete strength and cover tables
- the steel grade

Everything came back right:

- **Bar list.** All 33 rows across both sheets (19 on P1, 14 on P2), including the
  sparse ones. The bend type 6 row on P1 has values only under B, C, D, H and K, and
  they land in exactly those columns. The two T2 ties fill A through G. The straight
  bars have no mark and a length in A.
- **Stamps.** Both review statuses read correctly on both sheets: REVIEWED for the
  architect, REVIEWED AS NOTED for the engineer. The checkbox states came through as
  `[x]` / `[ ]` in the engineer stamp's table.
- **Blank cells** extract as nulls with no ranges. That is why so many rows in
  `inspect_fields.py` read `SYNTH`: they are empty cells, not failures.

## Featured fields

All are on **page 1, sheet P1 Footing**:

| Field | Value | Region |
|---|---|---|
| Project | TURNBULL SCHOOL MUSIC ROOM ADDITION | Title block, PROJECT |
| Fabricator contract number | CP9667F | Title block, CONTRACT NO. |
| Engineer review status | REVIEWED AS NOTED | Cunliffe review stamp |
| Bar quantity (first bar list row) | 32 | Bar list, QTY |
| Bar mark (first bar list row) | A5 | Bar list, BAR MARK |

Together they say which job this is, whose drawing it is, whether it was approved and
what is to be fabricated. No featured field names a person.

The request suggested these fields in its notes but named none of them formally.
Several suggestions were left out:

- **Drawing title.** `FOOTING` extracted correctly but came back with no ranges on P1
  (`SYNTH`). This happened even though it sits in a title-block table cell, and the
  same field grounds fine on P2.
- **Engineer review date and latest revision date.** They are normalized to YYYY-MM-DD,
  so their crops (`11/13/18`, `6-NOV-18`) would appear to disagree with the value.
- **Sheet number and revision number.** Both ground fine but were cut to keep to five
  fields.

## What the grounding did

- **Tables are found inside a CAD sheet.** Each sheet parsed into 9 tables: the bar
  list, the concrete tables, the legend, the revision block and the title-block cells.
  Their cells ground precisely, even on stroked glyphs at this scale.
- **Drawings are figures.** All 9 plans and elevations came back as
  `<figure type="DIAGRAM">`, and their bar callouts (`V 23 15M A11 @400`) appear only in
  the generated description. As with `engineering-drawing`, a callout value can be
  extracted but can only be boxed as the whole drawing. None is featured.
- **Stamps become attestations.** Two `attestation` blocks per sheet.
- **OCR false alarm.** `build_images.py` warned that OCR could not read `32` and `A5`
  inside their boxes. The crops were opened, and each boxes exactly the right cell; the
  small CAD digits are what defeat the OCR check.

## Cost

**19.70 credits** at standard tier for 2 pages: 7.90 to parse and 11.80 to extract. The
extraction costs more than the parse because the schema returns 33 bar list rows of 13
fields each.

## Regenerating

```bash
.venv/bin/python document-types/scripts/run_ade.py shop-drawing                # 19.70 credits
.venv/bin/python document-types/scripts/run_ade.py shop-drawing --extract-only # 11.80, schema iteration
.venv/bin/python document-types/scripts/build_images.py shop-drawing           # free
.venv/bin/python document-types/scripts/inspect_fields.py shop-drawing --page 1 --good
```
