# Medical imaging report

Source assets for `landing.ai/document-type/medical-imaging-report`.

## Sample document

`source/sample-mri-report.pdf`: a **sample MRI report**, published as Attachment #4 to a
New York State Department of Corrections and Community Supervision (DOCCS) procurement to
show bidders the report format the agency expects. **3 pages, portrait**, a native PDF
exported from Word with a text layer.

Each page repeats the same letterhead ("CONTRACTOR NAME") and a two-column patient header
of twelve labels: patient name, sex, DOB, accession number, medical record number,
ordering and attending doctor, and so on. Every one is blank. Page 1 carries the exam,
clinical indication, comparison and technique, followed by the first findings sections
(ligaments, tendons, muscles). Page 2 continues with joints and bones and the "other"
structures, then gives the impression, the line recording when the findings were
discussed, and the signature block. Page 3 is a sign-off page with placeholders only.

| | |
|---|---|
| Publisher | New York State Department of Corrections and Community Supervision (DOCCS) |
| Source | [doccs.ny.gov/…/attachment-4-sample-mri-report.pdf](https://doccs.ny.gov/system/files/documents/2021/04/attachment-4-sample-mri-report.pdf) |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public |

The PDF is on the agency's official domain. The parent bid or RFP page that links it was
not found. The report carries no identifiers: the patient header is blank, and the
provider, doctor, facility and signer are placeholders such as `DOCTOR NAME` and
`{insert correctional facility name}`. The clinical narrative (a right-ankle MRI in a
53-year-old male) is not tied to anyone. No page text was changed. The only edit was
clearing the PDF's document-information metadata, whose author field held a staff
member's first name.

## Why this document

The collection's first **radiology report**. Every other medical document here is a lab
report built around a results table. This one is almost all free-text narrative: a
radiologist's prose findings under anatomic headings, then an impression. It tests:

- **Facts in prose:** the diagnosis, the recommended follow-up, and the date the findings
  were communicated all sit in sentences, not labelled fields.
- **A repeated, inconsistent block:** the examination, clinical indication, comparison
  and technique appear twice on page 1, and they disagree. The first says "MRI FOOT"
  and the second says "MRI ANKLE". The schema asks for the last statement, the one the
  findings follow, and gets it.
- **Template residue:** a blank patient header and `{insert …}` placeholders that an
  extractor has to recognize as empty instead of copying.
- **Typos as printed:** "platar spring", "signification osteochondral lesion".

## Featured fields: the clinical conclusion

All on page 2.

| Field | Value |
|---|---|
| Impression | Non-displaced fracture of the medial cortex of the distal tibial metadiaphysis. |
| Joint and bone finding | moderate marrow edema in the anterior/lateral aspect of the distal tibia |
| Findings discussed | 12/15/2020 2:20 PM |

What the radiologist concluded, the imaging finding behind it, and when the result reached
the care team. The request suggested these three plus the recommended follow-up (CT of
the tibia/fibula or radiographs). The follow-up extracts correctly but could not be
featured, as explained below.

## What it surfaced

**Narrative paragraphs ground one line at a time.** Each range in a long value covers one
printed line, so no single box contains the whole value, and every multi-line field reads
`OFF`. These fields include the impression, technique, recommended follow-up and most
`findings[].finding` paragraphs. The values themselves are correct. To give the page
something it could feature, the schema has short verbatim fields that fit on one line:
`primary_diagnosis` (the impression's first sentence), `findings[].key_finding` (the
section's first abnormality) and `follow_up_studies`. The first two ground `ok`.
`follow_up_studies` ("CT of the rest of the tibia/fibula or radiographs") still reads
`OFF` because the printed text wraps between "CT" and "of the rest", which is why the
request's follow-up field did not ship.

**Template placeholders are handled correctly, mostly.** All six patient fields and the
exam date come back `null` with no grounding, which is the right answer for blank labels.
`radiologist` is `null` despite `DOCTOR NAME` and `{insert …}` placeholders, but only
after the schema told it to return JSON null. The first run returned the string
`"null"`. Inside the `findings` array, `key_finding` for normal sections still comes back
as the string `"null"` even with the same instruction. `imaging_provider` copies the
placeholder `CONTRACTOR NAME` literally.

**The impression first absorbed the next paragraph.** On the first run, `impression`
included the "findings were discussed with…" sentence. Telling it to stop at the end of
the paragraph fixed that.

**The abnormal flag is right in every section.** The flag marks ligaments, muscles and
joints/bones as abnormal (all three report edema or fracture) and the five other
sections as normal.

## Extraction

**27 leaf fields**: the provider and report status; the patient header (name, sex, date
of birth, record and accession numbers, ordering physician); exam date, examination,
modality, body part, laterality and contrast; clinical indication, comparison and
technique; each findings section (area, finding, key finding, abnormal flag); the
impression, primary diagnosis, recommended follow-up and follow-up studies; when the
findings were communicated; and the radiologist. 16 of 19 top-level fields populate. The
three empty ones (patient, exam date, radiologist) are blank or placeholders in the
source. The `findings` array has 8 sections.

## Cost

**15.10 credits** at standard tier for 3 pages: 6.50 for the parse and first extraction,
then 4.40 and 4.20 for two extract-only runs while iterating the schema.

## Regenerating

```bash
curl -sSL -o document-types/collection/medical-imaging-report/source/sample-mri-report.pdf \
  "https://doccs.ny.gov/system/files/documents/2021/04/attachment-4-sample-mri-report.pdf"
# then clear the PDF metadata (author field), e.g. PyMuPDF set_metadata({}) + del_xml_metadata()
.venv/bin/python document-types/scripts/run_ade.py medical-imaging-report                # 6.50 credits
.venv/bin/python document-types/scripts/run_ade.py medical-imaging-report --extract-only # ~4.3, schema iteration
.venv/bin/python document-types/scripts/build_images.py medical-imaging-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py medical-imaging-report --page 2
```
