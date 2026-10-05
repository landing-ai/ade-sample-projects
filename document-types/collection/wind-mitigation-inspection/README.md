# Wind mitigation / 4-point inspection

Source assets for `landing.ai/document-type/wind-mitigation-inspection`.

## Sample document

`source/surehome-oir-b1-1802-wind-mitigation-sample.pdf`: a completed Florida **Uniform
Mitigation Verification Inspection Form, OIR-B1-1802 (Rev. 04/26)**, the state form
insurers accept as evidence for windstorm premium discounts. It covers a one-storey 1999
home in Brevard County, inspected July 29, 2026. **6 pages, portrait**, with a text layer.

| | |
|---|---|
| Publisher | SureHome of Brevard (licensed Florida home inspection company, Melbourne FL) |
| Source | [surehomes.org/samples/sample-wind-mitigation.pdf](https://www.surehomes.org/samples/sample-wind-mitigation.pdf) |
| Retrieved | 2026-10-04 |
| Clearance | Public |

SureHome's home page links this file as "Sample PDF - Wind Mitigation: The signed
OIR-B1-1802" and states that "Sample reports use fictional client and property details."
The owner and street address are those fictional details. The inspector's name, licence
number, company phone, initials and signature appear in a professional capacity on the
company's own marketing sample. Downloaded directly; no redaction was needed.

The published file has 11 pages. It was trimmed to pages 2–7, the six-page state form:
page 1 is a branded cover with a photo of a house, and pages 8–11 are inspection photos.
Document metadata was cleared.

Full provenance is in `manifest.json` under `source.origin`; this section is the
human-readable version.

## Why this document

The collection's first **insurance underwriting inspection**, and its most
checkbox-dense form:

- **Answers are checkmarks, not text.** Nine questions, each answered by marking one
  lettered option (Building Code A–D, Roof Deck A–H, Roof to Wall A–I, Opening
  Protection A–Z), with nested sub-options under several of them.
- **The marks are separate glyphs.** Each checkmark is an "X" drawn beside an empty box
  glyph rather than a filled box, so the parser has to decide which box each X belongs to.
- **A matrix of marks.** The Opening Protection Level Chart is a grid of opening types
  against protection levels, filled with Xs.
- **Typed values on a pre-printed form:** dates, year built, stories, roof perimeter,
  inspector licence and company.

## Featured fields: what an insurer reads first

All on page 1. The request named no page or fields; it suggested several, and these
were chosen from them:

| Field | Value |
|---|---|
| Inspection date | 2026-07-29 |
| Year of home | 1999 |
| Building code answer | D (unknown or does not meet A, B or C) |
| Wind region | Region 1 (≥ 140 mph) |
| Roof permit application date | 2019-04-04 |

When the home was inspected (the form is valid for five years), how old it is, which
building code it was built under, how exposed it is to wind, and how recent the roof is.
Number of stories and roof slope also ground correctly on the same page and were left
out to keep to five. The fictional owner name and address are on page 1 and not featured.

The wind region is pinned to its second occurrence; the first grounds to the question
heading. Its box covers the whole line of four region options, with the X beside
Region 1 visible inside it.

## What it surfaced

**Most checkmarks resolve correctly.** DPT-3 Pro rendered each X-beside-a-box as `[x]`
or `[ ]` in the markdown, and got Building Code D, Region 1, slope < 6:12, product
approval A, roof deck C, single wraps with minimal condition 2, hip roof, sealed roof
deck A, and opening protection A with sub-answer A.1 all right. The Opening Protection
chart comes back correct for all six opening types.

**Two misreads, both in places where marks are sparse.** In the 4.1 roof covering
table, Built Up, Membrane and Other were rendered `[x]` although only
Asphalt/Fiberglass Shingle is marked, so extraction returns four roof coverings instead
of one. Under 8.A, the "fully adhered polymer-modified bitumen" sub-option is marked but
was rendered `[ ]`, so `swr_method` comes back null. Neither is featured; both are worth
knowing before trusting checkbox output on this form without review.

**Chart cells ground to bare Xs.** Each Opening Protection chart value is right, but it
grounds to a cell holding only "X", so `inspect_fields.py` marks it OFF: the value is a
row label, and the evidence is a mark.

**Empty values come back as "" or 0, not null.** Insurance company, policy number,
product approval number and year installed are blank on the form and return empty
strings or 0.

## Extraction

**45 leaf fields** (counted from `schema.json`): form revision, inspection date, owner
block, year and stories, the answer to each of the nine questions with their sub-answers
and written values, the opening protection chart, the inspector block and both
signature lines.

## Cost

**16.40 credits** at standard tier for 6 pages, parse and extract together.

## Regenerating

```bash
curl -sSL -o /tmp/sample-wind-mitigation.pdf https://www.surehomes.org/samples/sample-wind-mitigation.pdf
# keep pages 2-7 and clear metadata
.venv/bin/python -c "import fitz;d=fitz.open('/tmp/sample-wind-mitigation.pdf');d.select(range(1,7));d.set_metadata({});d.del_xml_metadata();d.save('document-types/collection/wind-mitigation-inspection/source/surehome-oir-b1-1802-wind-mitigation-sample.pdf',garbage=4,deflate=True)"
.venv/bin/python document-types/scripts/run_ade.py wind-mitigation-inspection                # 16.40 credits
.venv/bin/python document-types/scripts/run_ade.py wind-mitigation-inspection --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py wind-mitigation-inspection           # free
.venv/bin/python document-types/scripts/inspect_fields.py wind-mitigation-inspection --page 1
```
