# Special Inspection Report

**On the website:** [landing.ai/document-type/special-inspection-report](https://landing.ai/document-type/special-inspection-report)

A building-pad certification package from a special inspections and materials testing
firm for Phase 1A of a subdivision in Oro Valley, Arizona, in 2019. The engineer's
sealed letter certifies that the pads were compacted to specification and assigns a
bearing value. A field density table of 18 compaction tests and four Soils Summary
sheets with lab results and compaction curves follow it.

| | |
|---|---|
| Pages | 6 |
| Fields in the extraction schema | 54 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:53 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 17,021 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 17.9 s |
| Per page | 3.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 7.3 credits |
| Per page | 1.22 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:54 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 54 |
| Non-null fields returned | 54 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 165.7 s |
| Per schema field (54) | 3.07 s |
| Per value returned | 0.48 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 12.7 credits |
| Per schema field (54) | 0.235 credits |
| Per value returned | 0.037 credits |

## Origin

`source/special-inspection-report.pdf` is a building-pad certification package from
**ProTeX - the PT Xperts, L.L.C.**, a special inspections, geotechnical and materials
testing firm, for the developer Pulte Tucson Land. It covers the mass grading of Phase 1A
of the Rancho Vistoso Valley Vista subdivision in Oro Valley, Arizona, in 2019. The
engineer certifies that the building pads were cleared, over-excavated, moisture
conditioned and compacted to specification, and assigns a bearing value of 1250 psf for
post-tensioned foundations. The field and laboratory test sheets behind that statement
follow it.

It is **6 pages, mixed orientation and mixed layer:**

- Page 1 (portrait, text layer): the certification letter, with the engineer's seal and
  signature.
- Page 2 (landscape, raster): a **Field Density Summary Report**, 18 nuclear-gauge
  compaction tests in a 14-column table. Each test gives the date, street, lot, depth,
  field dry density and moisture, the Proctor maximum dry density and optimum moisture it
  is compared against, % compaction, the density and moisture specs, the Proctor lab
  number and Pass/Fail.
- Pages 3-6 (portrait, raster): four **Soils Summary** sheets, one per Proctor lab
  number cited in that table (191957, 191995, 191996, 191999). Each has nested boxed
  panels for plasticity, expansion index, swell, pH and resistivity and the ASTM D698-A
  moisture-density (Proctor) results, plus a moisture-versus-density compaction curve.

The raster pages are page images of about 150 dpi in the original, rebuilt at 300 dpi by
the redaction step.

| | |
|---|---|
| Publisher | ProTeX - the PT Xperts, L.L.C., for Pulte Tucson Land; posted by the Town of Oro Valley, Arizona |
| Source | [gis.orovalleyaz.gov/storyimages/Planning/Valley Vista/3.pdf](https://gis.orovalleyaz.gov/storyimages/Planning/Valley%20Vista/3.pdf) |
| Retrieved | 2026-10-14, by script |
| Clearance | Redacted, see below |

The Town of Oro Valley publishes this file on its own GIS server, in a Planning/Valley
Vista folder beside sibling geotechnical reports, as part of the public record on the
subdivision. The subdivision is the subject of a public subsidence dispute. This folder
is about the document type and takes no position on that.

The original is 58 pages: three phase packets (1A, 1B and 1C), each a cover letter,
field density tables and Soils Summary sheets. This sample keeps six pages of the Phase
1A packet, in their original order: the cover letter (original page 1), the first Field
Density Summary Report table (page 2), and the Soils Summary sheets for the four Proctor
lab numbers that table cites (pages 13, 16, 17 and 19). The other Phase 1A tables cite
more lab numbers and repeat the same layout.

The engineer, field technician and laboratory reviewer are public professionals named
on a public record. Their names and signatures were replaced anyway, because the values
would be republished on a marketing page. Lot numbers, street names, the client, the
project and the firm's office addresses are kept: there are no homeowner names in the
document.

| What | Replaced with | Count |
|---|---|---|
| Professional engineer's name typed under the signature | `Jane Sample` | 1 |
| Engineer's name inside the P.E. seal | `JANE SAMPLE` | 1 |
| Engineer's certificate (registration) number inside the seal | A random 5-digit stand-in | 1 |
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
  file. The typed name was then replaced, removing the underlying text, and the stand-in
  signature drawn. Some letters of "ARIZONA" on the seal's lower edge were thinned where
  the signature crossed them, and the stand-in signature sits over that area as the
  original did.
- **Pages 2-6 are raster.** The names were found with OCR, painted over and redrawn at
  the original cap height, and each page was rebuilt from the edited 300 dpi image
  alone. The reviewer's signature was erased over a region that stops short of the
  signature rule. A sliver of the original stroke where it touched the rule remains,
  without the rest of it.

The redaction was verified by a text check, an OCR check, a separate OCR sweep of all
six output pages on literals and digits, by eye on renders, and by a rules check over
every file in this folder. PDF metadata is cleared. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

Special inspection and materials testing reports are the evidence that construction
work met its specification, and building departments, owners and builders all rely on
them.

- **Municipal building and planning departments:** officials review pad certifications
  and compaction tests before issuing permits and accepting subdivisions.
- **Homebuilders and land developers:** they collect certifications for every lot
  before foundations are poured.
- **Geotechnical and materials testing firms:** they produce the reports and compile
  field and lab results into certification packages.
- **Structural and foundation engineers:** they design foundations around the certified
  bearing value and soil properties.
- **Construction lawyers and insurers:** they review test records when settlement or
  defect claims arise.

### What it contains

- **A very wide table on a scan,** with 14 columns and two- to three-line headers on a
  landscape page.
- **Cross-page references.** Each test row cites a Proctor lab number whose Soils
  Summary sheet is in the sample, and not every row matches its sheet's corrected
  values.
- **Nested boxed panels** of small labelled tables inside a grid, with NA and NV
  placeholders.
- **Moisture-density charts** with plotted points and a curve.
- **A professional engineer's seal and signatures,** plus reviewer signatures on each
  lab sheet.
- **Mixed layers and orientation:** a text-layer letter followed by raster pages, one of
  them landscape.
