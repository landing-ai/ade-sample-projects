# Prescription history report

**On the website:** [landing.ai/document-type/prescription-history-report](https://landing.ai/document-type/prescription-history-report)

A generic prescription drug monitoring program (PDMP) patient report with fictitious
data, as printed in PDMP TTAC's overview of how PDMPs operate. Four indicator boxes give
the patient's morphine milligram equivalent average, multiple provider episodes,
overlapping prescriptions and overall risk score. Below them are the patient's details
and a table of seven dispensed prescriptions with prescriber, pharmacy, dates, drug,
strength, quantity, days supply and refills.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 30 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:42 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 2,838 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 14.1 s |
| Per page | 14.1 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.3 credits |
| Per page | 1.30 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:42 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 30 |
| Non-null fields returned | 30 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 93.1 s |
| Per schema field (30) | 3.10 s |
| Per value returned | 0.78 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 4.2 credits |
| Per schema field (30) | 0.140 credits |
| Per value returned | 0.035 credits |

## Origin

`source/pdmp-sample-patient-report.png` is a **prescription drug monitoring program
(PDMP) patient report**, the generic sample with fictitious data that PDMP TTAC prints
on page 9 of its overview of how PDMPs operate. It is **1 page, landscape**, a 2365 x
1312 PNG image with no text layer. Four summary indicator boxes (MME assessment,
multiple provider episodes, overlapping prescriptions, overall risk score) sit over a
patient identification row and a dispensation table of seven prescriptions.

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

**How the page was cropped.** The 11-page PDF is not committed; only the sample report
is. Page 9 holds it as two embedded raster images (the indicator boxes, and the patient
and dispensation tables), with prose above and below. The page was rendered at 300 dpi
and clipped to the union of the two images' bounding boxes plus a 5-point margin, which
excludes the surrounding prose and the page number. Rendering the page, rather than
extracting the embedded images, composites their transparency masks over white as the
PDF displays them. Nothing else was altered.

Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A prescription history report lists the medications a person has filled over time.
PDMP reports cover controlled substances for clinical and regulatory use, and insurer
Rx history reports cover pharmacy benefit data for underwriting.

- **Prescribers and pharmacists:** they check a patient's PDMP report before prescribing
  or dispensing controlled substances.
- **State PDMP administrators:** they produce reports and review risk indicators across
  patients.
- **Life and disability insurers:** underwriters read Rx history reports to check an
  applicant's medical disclosures.
- **Health systems and care managers:** they review fill histories when reconciling a
  patient's medications.
- **Regulators and law enforcement:** under the conditions state law sets, they use PDMP
  data in investigations of diversion.

### What it contains

- **Indicator tiles:** colored boxes in which a bare number ("66.04", "8 Dr / 5 Rx", "4",
  "5") takes its meaning from a caption beside it.
- **A dispensation table** of seven rows with prescriber, pharmacy, three dates, Rx
  number, drug, strength, quantity, days supply and refills.
- **Multi-line table cells** that pack a name, an address and a DEA number into one cell.
- **Repeated rows** (the same prescriber, pharmacy and drug a month apart) that must stay
  separate.
- **A raster image,** cropped from a larger page, with no text layer.
