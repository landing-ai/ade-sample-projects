# Laboratory Protocol Guide

ibidi's application guide *Immunofluorescence Assays* (FL_AG_039, V 1.0, September 2019). It
walks through an indirect immunofluorescence staining protocol, one step at a time:

- fixation, permeabilization and blocking
- primary and secondary antibody incubation
- counterstain and mounting, then microscopy

It then gives two troubleshooting tables, a comparison table of ibidi's culture vessels, and
example micrographs. The PDF is 16 pages, portrait A4, with a text layer and a heavily designed
layout: two-column prose, cell diagrams beside the text, a photo cover, and ruled tables.

## Provenance

| | |
|---|---|
| Publisher | ibidi GmbH |
| Source URL | https://ibidi.com/img/cms/resources/AG/FL_AG_039_Immunofluorescence_150dpi.pdf |
| Retrieved | 2026-11-15 |
| Clearance | `public` |

This is a vendor's own application guide, published free on its website. It was downloaded by
script directly from the publisher's domain, and the PDF metadata was cleared.

The example pages credit the scientists who supplied each micrograph, by name and institution.
Those are professional attributions in the publisher's own document. They are kept as printed
and are not featured. The back page carries ibidi's corporate addresses and phone lines.

## Why this document

A protocol guide is procedural prose: what to use, for how long, at what temperature, and what
to do when it goes wrong. The parameters a lab needs, such as "4% formalin", "10 minutes" and
"3x for 5 minutes", sit inside sentences rather than in labelled fields. The guide pairs that
with ruled reference tables. It tests extraction from running text and from tables in the same
document.

## Featured fields (page 8, Troubleshooting)

| Field | Value |
|---|---|
| Problem | High Background |
| Reason (row 2) | Insufficient blocking |
| Solution (row 2) | Prolong the incubation time, consider using a different blocking solution (we recommend using serum from the secondary antibody host) |
| Reason (row 6) | Not enough washing |
| Solution (row 6) | Verify that all washing steps are carried out properly; if necessary, prolong the washing steps |

The overlay shows one table: the symptom, then two complete cause-and-remedy rows. Both rows
point back to steps the protocol describes earlier, blocking and the washes.

## Grounding on this document

**The tables ground cell by cell.** Both troubleshooting tables parse as tables. All 16 rows are
extracted, and every reason and solution resolves to its own cell. Each value also has a second
range on its table's heading, reported as `OFF`, so occurrence 0 is pinned.

**The protocol pages are harder.**

- **Prose parsed as figures.** On page 4, the fixation and permeabilization text sits beside a
  cell diagram, and both blocks parsed as figures. Values from them are correct ("10 minutes",
  "room temperature", "4% formalin solution (in PBS, pH 7.4)"), but they box a whole column of
  text.
- **Steps out of order.** `protocol_steps` came back out of document order. Blocking is listed
  first and Sample Fixation sixth, and "Experiment Planning and Sample Preparation" is missing as
  a step.
- **An invented value.** Secondary Antibody Incubation came back with a temperature of "room
  temperature". Page 6 states no temperature; it says only to follow the manufacturer's
  protocol. That value grounds `OFF`, to an unrelated sentence. It is an extraction error, and
  the grounding check is what exposes it.
- **Paraphrased cautions.** Most `key_caution` values ground `OFF`, because they paraphrase
  rather than quote.

The vessel comparison table on page 9 extracted correctly, all three columns.

## Credits

37.70 credits at standard tier: parse plus extract, 16 pages.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py laboratory-protocol-guide
.venv/bin/python document-types/scripts/inspect_fields.py laboratory-protocol-guide --page 8
.venv/bin/python document-types/scripts/build_images.py laboratory-protocol-guide
```

The schema has 19 leaf fields.
