# Prescription history report

Source assets for `landing.ai/document-type/prescription-history-report`.

## Sample document

`source/pdmp-sample-patient-report.png` — a **prescription drug monitoring program (PDMP)
patient report**, the generic sample with fictitious data that PDMP TTAC prints on page 9
of its overview of how PDMPs operate. **1 page, landscape**, a 2365 x 1312 PNG. Four
summary indicator boxes (MME assessment, multiple provider episodes, overlapping
prescriptions, overall risk score) sit over a patient identification row and a
dispensation table of seven prescriptions, each with prescriber, dispensing pharmacy,
three dates, Rx number, drug, strength, quantity, days supply and refills.

**This is a PDMP report, not an insurer's prescription history report.** State PDMPs
collect controlled-substance dispensing data and report it to prescribers, pharmacists
and, under conditions, law enforcement. Insurers' Rx history reports (Milliman
IntelliScript, ExamOne ScriptCheck) are built from pharmacy benefit data for
underwriting. The two share their shape (a patient header, summary scores and a
chronological fill list) but differ in purpose, data source and recipients.

| | |
|---|---|
| Publisher | PDMP Training and Technical Assistance Center (PDMP TTAC), Institute for Intergovernmental Research; funded by the Bureau of Justice Assistance, Grant No. 2019-PM-BX-K003 |
| Source | [pdmpassist.org/pdf/resources/PDMPs_Overview_2023.pdf](https://www.pdmpassist.org/pdf/resources/PDMPs_Overview_2023.pdf), page 9 |
| Retrieved | 2026-10-04, downloaded directly by script |
| Clearance | Public, with a caveat on terms (below) |

The URL is on the publisher's own domain and redirects to its Azure blob store. Page 8 of
the PDF introduces the sample as "a generic sample report with fictitious data". It is
fictitious throughout: the patient is John Robert Doe of 123 Main Street, Anytown; the
prescribers are named after fictional TV doctors; the pharmacies include "Test Pharmacy"
and "Made-up Drug Store"; and the DEA-style registration numbers are repeated digit
patterns. The towns are fictional, but the ZIP codes (90210 to 90213) are real Beverly
Hills-area ZIPs. No redaction was needed.

**Caveat on terms, accepted by the operator.** The PDF states no reuse terms, and the
pdmpassist.org footer reads "All Rights Reserved". It is a federally funded publication
but not a work of the federal government itself. The operator chose this candidate with
its clearance marked unclear.

### How the page was cropped

The 11-page PDF is not committed; only the sample report is. Page 9 holds it as two
embedded raster images (the indicator boxes, and the patient and dispensation tables),
with prose above and below. The page was rendered with PyMuPDF at 300 dpi, clipped to
the rectangle (22, 67) to (589.25, 381.64) in PDF points. That rectangle is the union of
the two images' bounding boxes, (27, 72) to (584.25, 376.64), plus a 5-point margin. It
excludes the surrounding prose and the page number. Rendering the page, rather than
extracting the embedded images, composites their transparency masks over white as the
PDF displays them. Nothing else was altered.

```python
import fitz
page = fitz.open("PDMPs_Overview_2023.pdf")[8]
page.get_pixmap(dpi=300, clip=fitz.Rect(22, 67, 589.25, 381.64), alpha=False) \
    .save("source/pdmp-sample-patient-report.png")
```

## Why this document

The collection's first prescription or pharmacy record, and its first document led by
**indicator tiles**: coloured boxes in which a bare number ("66.04", "8 Dr / 5 Rx", "4",
"5") takes its meaning from a caption beside it. It also tests:

- **Multi-line table cells** that pack name, address and DEA number into one cell, split
  here into three schema fields each for prescriber and dispenser.
- **Repeated rows** (the same prescriber, pharmacy and drug a month apart), which must not
  be merged or deduplicated.
- **A raster source**, cropped from a larger page.

## Featured fields: the risk summary

| Field | Value |
|---|---|
| MME (30-day average) | 66.04 |
| Prescribers in 6 months | 8 |
| Overlapping prescriptions | 4 |
| Risk score | 5 |
| Dispensed drug | Hydrocodone |

The four indicators are what a reviewer reads first, and the request suggested them. The
fifth field is the drug on the second dispensation row, Hydrocodone 7.5 MG x 180, the
opioid behind the MME figure, so the overlay links the summary to the fill list. The
patient's name and address are left out, as impersonal fields make the same point.

## What it surfaced

**Every field grounds `ok`, all 30 leaves on all 7 rows.** The parse renders the
dispensation table as an HTML table with `<br>` inside cells, and extraction splits each
prescriber and dispenser cell into name, address and DEA number correctly, keeping the
printed space in "AP 44488891" and "AC 45454545".

**The indicator boxes ground as whole tiles.** The parse reads each tile as a single line
("66.04 MME Assessment * 30-day average"), so the four indicator values, their periods and
their maxima all ground to that tile's whole box, not to the number alone. The crops
contain the right values but are tile-sized. `build_images.py` warned that OCR could not
read 66.04, 8 and 5 inside their boxes; on inspection all three are present, and the
misses come from dark text on the red and yellow tiles under the highlight.

**The split counts are read correctly.** "8 Dr" and "5 Rx" in one tile became 8
prescribers and 5 pharmacies, and "Max Score=7" became a separate maximum of 7.

## Extraction

**30 leaf fields**: nine risk indicators (MME value and period; prescriber and pharmacy
counts and period for multiple provider episodes; overlapping count and period; risk score
and its maximum); six patient fields; and fifteen per dispensation row (prescriber name,
address and DEA number; dispenser name, address and DEA number; dates issued, filled and
sold; Rx number; drug; strength; quantity; days supply; refills). All 3 top-level fields
populate, with all 7 rows.

## Cost

**5.50 credits** at standard tier for 1 page, parse and extract together.

## Regenerating

```bash
curl -sSL -o PDMPs_Overview_2023.pdf \
  "https://www.pdmpassist.org/pdf/resources/PDMPs_Overview_2023.pdf"
# crop page 9 with the PyMuPDF snippet above, into source/
.venv/bin/python document-types/scripts/run_ade.py prescription-history-report                # 5.50 credits
.venv/bin/python document-types/scripts/run_ade.py prescription-history-report --extract-only # schema iteration
.venv/bin/python document-types/scripts/build_images.py prescription-history-report           # free
.venv/bin/python document-types/scripts/inspect_fields.py prescription-history-report --page 1
```
