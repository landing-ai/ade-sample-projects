# Medical Imaging Report

A real radiology report as it actually arrives at a provider's office: by fax. It is a shoulder
MRI read for an orthopedic practice and faxed to a physical therapy clinic in March 2019.

| Page | Content |
|---|---|
| 1 | The practice's fax cover sheet: letterhead, a staff roster down the left margin, To/From/Date/Subject blocks, and a confidentiality notice |
| 2 | The report: patient block, study details, history, comparison, technique, findings, impression, and signature lines |

The PDF is 2 pages, portrait, and is a raster scan with no text layer. Every page carries the fax
machine's transmission header.

This replaces the collection's earlier medical-imaging-report folder, a 3-page sample report
published by New York State DOCCS, at the operator's direction.

## Provenance

| | |
|---|---|
| Sender | Rebound Orthopedics & Neurosurgery (Northwest Surgical Specialists, P.C.), Vancouver, WA |
| Source | Contributed by the patient. Not published online, so there is no source URL |
| Received for this collection | 2026-11-15 |
| Clearance | `redacted` |

The patient this report describes contributed it and gave explicit permission to publish it, on
one condition: their name must not appear. The patient chose to remove their name only.
Everything else is as faxed:

- the clinic's staff roster
- the referring, reading and sending staff
- the medical record and accession numbers
- the dates
- the clinical content

### What was removed, and how

The scan arrived with the patient's name and date of birth covered by black marks. These were
**stamp annotations drawn over an intact scan**. Remove the annotations in any PDF editor and
the original text is still there underneath. A "redaction" like this looks complete on screen
and is not.

Three regions were burned into the page images: the patient name on both pages and the date of
birth on page 2. The image pixels in each region were blanked and a solid black box drawn in
their place, and the stamp annotations were deleted. The boxes are fitted to each text line, so
the neighbouring labels (PATIENT NAME, MRN, DOB, SEX) stay legible.

Checks on the output:

- the raw embedded image pixels under every box read pure white
- no annotations remain
- the PDF metadata is empty

The usual text sweep for the original strings was not run. The patient did not supply them, by
choice. The burn happened before the document was parsed, so the originals never reached ADE:
the parse reads the boxes as `[REDACTED]`. There is no text layer and no metadata in which they
could survive.

## Why this document

It is the real thing rather than a specimen:

- a fax of a scan
- a cover sheet that is mostly noise, including a roster of about 60 staff names
- a report body in the shouting all-caps of a radiology information system export
- burned-in redaction boxes, as real records arriving from outside usually carry

## Schema

The schema was supplied with the request and used unchanged. It has 22 leaf fields across:

- fax transmission details
- sender information
- the patient block
- study details
- report findings

One key is spelled `oragnization`, as supplied.

## Featured fields (page 2)

| Field | Value |
|---|---|
| Exam | MR UPPER EXT WO CONTRAST SHOULDER RIGHT |
| Study date | Mar 08, 2019 |
| Comparison study | X-ray January 14, 2018. |
| Technique | Coronal oblique, sagittal oblique on axial imaging. |

Together they describe the study itself: what was scanned, when, against what prior image, and
how it was imaged. The identifier fields (MRN and accession number) and the physician names
ground correctly but were deliberately not featured, because these four fields make the same
point without them.

## Grounding on this document

**One line, one value: tight boxes.** Every single-line value grounds to its own line box,
including the fax header on both pages and the sender block in the cover sheet's footer.

**Several lines, one value: `OFF`.** The most interesting text on the page is the findings and
the impression, and neither can be featured. Each spans several lines, and the range comes back
as one piece per line. None of those pieces contains the whole value, so `inspect_fields.py`
reports every one `OFF`. The history (two lines) does the same.

**The parse reads a black box as `[REDACTED]`.** DPT-3 renders the burned regions as
`[REDACTED]`, on both the subject line and the patient name. Extraction returns
`patient_name: "[REDACTED]"` rather than inventing a name, the right outcome for a redacted
record.

**One line disappeared.** The parse dropped the line that holds the date-of-birth box and the
legible "SEX: F" entirely. So `date_of_birth` and `sex` both come back null (`SYNTH`), even
though the sex is printed in clear.

**A value that needs reading.** `accession_number` wraps onto its own line below its label. It
grounds `ok` to that line, with a second, `OFF` range on the label line.

## Credits

5.30 credits at standard tier: parse plus extract, 2 pages.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py medical-imaging-report
.venv/bin/python document-types/scripts/inspect_fields.py medical-imaging-report --page 2
.venv/bin/python document-types/scripts/build_images.py medical-imaging-report
```
