# Special Inspection Report

Source assets for `landing.ai/document-type/special-inspection-report`.

## Sample document

`source/special-inspection-report.pdf` is a building-pad certification package from
**ProTeX - the PT Xperts, L.L.C.**, a special inspections, geotechnical and materials
testing firm, for the developer Pulte Tucson Land. It covers the mass grading of Phase 1A
of the Rancho Vistoso Valley Vista subdivision in Oro Valley, Arizona, in 2019. The
engineer certifies that the building pads were cleared, over-excavated, moisture
conditioned and compacted to specification, and assigns a bearing value of 1250 psf for
post-tensioned foundations. The field and laboratory test sheets behind that statement
follow it.

**6 pages, mixed orientation and mixed layer:**

- Page 1 (portrait, text layer): the certification letter, with the engineer's seal and
  signature.
- Page 2 (landscape, raster): a **Field Density Summary Report**, 18 nuclear-gauge
  compaction tests in a 14-column table. Each test gives the date, street, lot, depth,
  field dry density and moisture, the Proctor maximum dry density and optimum moisture it
  is compared against, % compaction, the density and moisture specs, the Proctor lab
  number and Pass/Fail.
- Pages 3-6 (portrait, raster): four **Soils Summary** sheets, one per Proctor lab number
  cited in that table (191957, 191995, 191996, 191999). Each has nested boxed panels for
  plasticity, expansion index, swell, pH and resistivity and the ASTM D698-A
  moisture-density (Proctor) results, plus a moisture-versus-density compaction curve.

The raster pages are page images of about 150 dpi in the original, rebuilt at 300 dpi by
the redaction step.

| | |
|---|---|
| Publisher | ProTeX - the PT Xperts, L.L.C., for Pulte Tucson Land; posted by the Town of Oro Valley, Arizona |
| Source | [gis.orovalleyaz.gov/storyimages/Planning/Valley Vista/3.pdf](https://gis.orovalleyaz.gov/storyimages/Planning/Valley%20Vista/3.pdf) |
| Retrieved | 2026-10-14, by script |
| Clearance | **Redacted**, see below |

The Town of Oro Valley publishes this file on its own GIS server, in a Planning/Valley
Vista folder beside sibling geotechnical reports, as part of the public record on the
subdivision. The subdivision is the subject of a public subsidence dispute. This folder is
about the document type and takes no position on that.

### How the PDF was made

The original is 58 pages: three phase packets (1A, 1B and 1C), each a cover letter, field
density tables and Soils Summary sheets. This sample keeps six pages of the Phase 1A
packet, in their original order: the cover letter (original page 1), the first Field
Density Summary Report table (page 2), and the Soils Summary sheets for the four Proctor
lab numbers that table cites (pages 13, 16, 17 and 19). The other Phase 1A tables cite
more lab numbers and repeat the same layout.

## Redaction

The engineer, field technician and laboratory reviewer are public professionals named on
a public record. Their names and signatures were replaced anyway, because the values
would be republished on a marketing page. Lot numbers, street names, the client, the
project and the firm's office addresses are kept: there are no homeowner names in the
document.

| What | Replaced with | Count |
|---|---|---|
| Professional engineer's name typed under the signature | `Jane Sample` | 1 |
| Engineer's name inside the P.E. seal | `JANE SAMPLE` | 1 |
| Engineer's certificate (registration) number inside the seal | A random 5-digit stand-in from `plausible.py` | 1 |
| Engineer's handwritten signature over the seal | The handwriting stand-in "J Sample", set in IndieFlower | 1 |
| Field technician's name (Sampled By and Submitted By) | `John Doe` | 8 |
| Laboratory reviewer's printed name (Reviewed By) | `Richard Roe` | 4 |
| Laboratory reviewer's handwritten signature | The handwriting stand-in "R Roe", set in IndieFlower | 4 |

The originals are not recorded anywhere in this folder, and the rules files stay outside
the repo. The registration expiry date and the date signed on the seal were kept.

Two routes were needed, one per layer:

- **Page 1 keeps its text layer.** The seal and the signature are one RGB image on that
  page. The image was edited in place first: the blue signature ink was removed by
  colour, the seal's four rings were redrawn where the signature had crossed them, and
  the seal's centre lines (number and name) were painted out and redrawn in Arial. The
  edited image replaced the original in the PDF, so the original pixels are not in the
  file. `document-types/scripts/redact.py` then replaced the typed name and drew the
  stand-in signature with `--draw-signature`. Some letters of "ARIZONA" on the seal's
  lower edge were thinned where the signature crossed them, and the stand-in signature
  sits over that area as the original did.
- **Pages 2-6 are raster.** `document-types/scripts/redact_scan.py` found the names with
  Tesseract OCR, painted over them and redrew the stand-ins at the original cap height,
  and rebuilt each page from the edited 300 dpi image alone. The reviewer's signature was
  removed with `--erase` over a region that stops short of the signature rule. A sliver of
  the original stroke where it touched the rule remains, without the rest of it.

Verified by `redact.py`'s text check, `redact_scan.py`'s OCR check, a separate OCR
sweep of all six output pages on literals and digits, by eye on renders, and by
`ship.py check --rules` over every file in this folder. PDF metadata is cleared.

## Why this document

Construction quality-control paperwork is table-heavy and mixes a typed letter with
scanned lab output. This sample tests:

- **A very wide table on a scan.** 14 columns with 2-3-line headers, landscape, at about
  150 dpi. The parse reads all 18 rows into an HTML table with every value right.
- **Cross-page references that reconcile.** Each test row cites a Proctor lab number,
  and that lab's Soils Summary sheet is in the sample. Lab 191957's corrected maximum dry
  density (121.2) is the value the Romsdalen Road rows that cite it use. The featured
  Lot 39 row uses lab 191996's corrected values (104.1 and 8.2), while the Lot 43 row
  cites the same lab but matches its uncorrected values (102.2 and 8.6). Extraction
  reports what is printed on each page and does not reconcile them. That is the right
  behaviour, and it leaves the check to a rule downstream.
- **Nested boxed panels.** The Soils Summary layout puts small labelled tables inside
  boxes inside a grid. Every panel value extracts, including the NA and NV placeholders.
- **A chart read as data.** Each moisture-density curve parses as a `CHART` figure with
  an estimated data table. On the first sheet the four plotted points come back as about
  (7.4, 114.1), (9.6, 117.6), (11.8, 117.7) and (13.8, 114.7), which matches the plot.
- **Attestations.** The seal and the signatures come back as `[STAMPED]` and `[SIGNED]`
  labels in the markdown.

`schema.json` was written for this run: **54 leaf fields**, counted from the schema. It
covers the certification letter (including the seal's registration number, expiry and
date signed), the field density report header and every test row, and one entry per
Soils Summary sheet. It leaves out the technician and reviewer names.

## Featured fields: one compaction test, page 2

| Field | Value |
|---|---|
| Lot tested | Lot 39 |
| Field dry density (lb/ft3) | 101.9 |
| Max dry density (lb/ft3) | 104.1 |
| Percent compaction | 98 |
| Test result | Pass |

The request suggested page 2 and a longer list: job ID, project name, test type, the
first row's date, lot and field dry density, max dry density, % compaction against spec,
and the result. All of them ground `ok` on page 2. Five were kept, all from the first
row, so the overlay reads as a single calculation: 101.9 / 104.1 = 97.9%, printed as 98
against a 98 min. spec, and so Pass. The date, job ID, project name and test type were
dropped only to keep to five. No individual is featured.

## Grounding and extraction on this document

- **Every value checked is right.** All 18 table rows and all four Soils Summary sheets
  extracted correctly, along with the 16 letter fields.
- **The table's cells ground tightly**, one box per cell, on a raster page. The OCR check
  in `build_images.py` could not read three of the five crops (Lot 39, 98, Pass), but
  each was opened and each box sits on its value.
- **The last six table rows are SYNTH.** Rows 13-18 extract with correct values, and the
  parse has every one of them, but extraction returned no ranges for them. Only the first
  twelve rows can be illustrated. The parse is not the cause.
- **Attestation booleans ground OFF.** `is_sealed` grounds to the letter's `[STAMPED]`
  label, and `is_signed` to a `[SIGNED]` label on page 5, a Soils Summary sheet, rather
  than the letter.
- **Seal values ground to the whole seal.** The registration number and date signed
  ground `ok`, but the box is the seal image, not the line.
- **Proctor panel values ground twice.** Each sheet's panel values ground `ok` to their
  cells, and a second occurrence lands on the chart figure that follows.

## Credits

20.20 credits at standard tier, through the jobs API, for one parse and one extract of
the 6 pages. Parse used `dpt-3-pro-latest`, which ran as `dpt-3-pro-20260710`; extract
ran as `extract-20260819`.

## Regenerate

```bash
# Scratch directory, outside the repo
curl -sSL -o orig.pdf "https://gis.orovalleyaz.gov/storyimages/Planning/Valley%20Vista/3.pdf"

# Raster pages (rules-scan.json outside the repo: technician and reviewer names)
.venv/bin/python document-types/scripts/redact_scan.py orig.pdf scan.pdf \
    --rules <outside-the-repo>/rules-scan.json --pages 2 13 16 17 19 \
    --erase "13:462,712,584,738.5=R Roe" "16:462,712,584,738.5=R Roe" \
            "17:462,712,584,738.5=R Roe" "19:462,712,584,738.5=R Roe" \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf

# Page 1: extract the seal image (513 x 569 px), remove the blue signature ink, redraw
# the four rings where it crossed them (centre 257,240 px; radii about 160, 171, 212,
# 224), paint out the centre lines and redraw the stand-in number and name in Arial
# 36 px; then page.replace_image(<xref>, filename=<edited png>) on a one-page copy.
.venv/bin/python document-types/scripts/redact.py p1.pdf p1r.pdf \
    --rules <outside-the-repo>/rules-p1.json \
    --draw-signature "1:104,642,196,676=J Sample" \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf

# PyMuPDF: p1r.pdf then scan.pdf with insert_pdf(); pdfmeta.clear(); save as
# source/special-inspection-report.pdf

.venv/bin/python document-types/scripts/run_ade.py special-inspection-report
.venv/bin/python document-types/scripts/build_images.py special-inspection-report
```
