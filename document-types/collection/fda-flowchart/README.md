# FDA Flowcharts

Five pages from the U.S. Food and Drug Administration's guidance *Deciding When to Submit a
510(k) for a Change to an Existing Device* (October 25, 2017). The pages are the cover and the
four decision flowcharts a manufacturer follows to decide whether a device change needs a new
510(k) premarket notification:

- the main chart
- Chart A, labeling changes
- Chart B, technology, engineering and performance changes
- Chart C, materials changes

The PDF is 5 pages, portrait, and has a text layer.

## Provenance

| | |
|---|---|
| Publisher | U.S. Food and Drug Administration (CDRH and CBER) |
| Source URL | https://www.fda.gov/media/99812/download |
| Retrieved | 2026-11-15 |
| Clearance | `public` |

This is a US federal government work, published on fda.gov for general use. The original runs
to 78 pages. The operator extracted pages 2, 13, 17, 25 and 34 into a local file, and that file
is the source here. Each page's text was checked against the same page of a fresh download from
the URL above, and all five match. The PDF metadata was cleared.

There is no personal data in it. The only contact details are FDA office phone lines.

## Why this document

Every other document in the collection carries its data in text, tables or forms. Here the data
is the *structure* of a diagram: which question leads to which, and on which answer. Extracting
it means reading arrows, not just labels. The schema asks for each decision diamond's ID and
question, and for where its Yes and No arrows lead.

## Featured fields (page 5, Flowchart C: Materials Changes)

| Field | Value |
|---|---|
| Figure caption | Figure 4 - Flowchart C: Materials Changes |
| Decision C4 | Does a risk assessment identify any new or increased biocompatibility concerns? |
| Decision C4.1 | Has the manufacturer used the same material in a similar legally marketed device (…)? |
| C4.1 No outcome | New 510(k) |

These fields trace the chart's only route to a new 510(k): C4 Yes, then C4.1 No. Chart C was
chosen because it is the one chart whose logic ADE extracted with no errors (see below).

## Grounding on this document

**Each flowchart is a single block.** DPT-3 classifies each chart as a `FLOWCHART` figure. It
writes the chart into the markdown as a node directory plus a list of connections, such as
`[C4.1] --No--> [TERMINAL_NEW_510K]`. That text gives extraction exact ranges, and
`inspect_fields.py` reports `ok` for nearly every field. But each figure has one grounding box,
around the whole chart. Every value read from inside a chart therefore crops to the same image,
the entire flowchart. The figure captions on pages 4 and 5 parse as separate text blocks, so they
are the only tight crops. Page 3's caption parses inside the figure.

So this page can show that a value came from this chart. It cannot show which diamond it came
from.

**The edges are mostly right, but not all.** Checked against the drawn arrows:

| Chart | Result |
|---|---|
| Main | All 4 decisions correct |
| A | A3 Yes and A4 Yes are given as "New 510(k)". Both arrows run to the A1.1 path. The other 7 decisions are correct |
| B | B3.1 Yes and No are swapped. The drawn Yes goes to New 510(k), and No goes to B3.2. The other 11 decisions are correct |
| C | All 6 decisions correct |

The decision text has one transcription slip. C2 reads "formulation, composition", but the chart
says "formulation, chemical composition". The main chart's diamonds have no printed IDs, and its
`node_id` and `chart_letter` come back null, which is correct.

## Credits

12.60 credits at standard tier: parse plus extract, 5 pages.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py fda-flowchart
.venv/bin/python document-types/scripts/inspect_fields.py fda-flowchart --page 5
.venv/bin/python document-types/scripts/build_images.py fda-flowchart
```

The schema has 10 leaf fields.
