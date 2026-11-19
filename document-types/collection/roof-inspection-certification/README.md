# Roof Inspection or Certification

**On the website:** [landing.ai/document-type/roof-inspection-certification](https://landing.ai/document-type/roof-inspection-certification)

A completed Florida Roof Inspection Form, the roof certification that Florida property
insurers ask a licensed inspector to complete before they bind a policy. It records the
roof covering, age, remaining life and permit, an overall condition rating, damage and
leak checkboxes, the inspector's comments and certification, and a page of roof photos.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 24 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:50 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 5,985 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 18.6 s |
| Per page | 6.2 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 3.0 credits |
| Per page | 1.00 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:51 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 24 |
| Non-null fields returned | 23 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 81.9 s |
| Per schema field (24) | 3.41 s |
| Per value returned | 3.56 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.0 credits |
| Per schema field (24) | 0.083 credits |
| Per value returned | 0.087 credits |

## Origin

`source/roof-inspection-form.pdf` is a completed Florida **Roof Inspection Form**, the
four-point-style roof certification that Florida property insurers ask a licensed
inspector to complete before they bind a policy. It shows the output of the Citizens
Roof Inspection library in the Spectacular Inspection System. The inspector recorded an
asphalt shingle roof, 30 years old with 4 years of remaining life and a last permit in
2011, rated Satisfactory, with visible hail damage and a leak shown on an interior
ceiling.

It is **3 pages, portrait, raster**: page images at 300 dpi with no text layer.

- Page 1: the property header and the Roof section (Predominant and Secondary roof
  columns).
- Page 2: comments, the inspector's certification block and the underwriting
  instructions.
- Page 3: the photo page, with four roof photographs.

The source report has four pages, but its page 3 is not published, so the PDF's third
page is printed "Page 4 of 4".

| | |
|---|---|
| Publisher | Spectacular Inspection System (AaceSystems), inspection-software vendor |
| Source | [spectacularapp.com/images/FLRoof1.jpg](https://www.spectacularapp.com/images/FLRoof1.jpg), with FLRoof2.jpg and FLRoof3.jpg |
| Linked from | [Roof Inspection Form product page](https://www.spectacularapp.com/Roof-Inspection-Form.aspx) ("Sample Report") |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted** |

The vendor publishes the sample as three separate JPEG page images, each 2550 x 3300 px
at 300 dpi, which is US Letter. They were downloaded by script and put into one PDF with
PyMuPDF, one per page, in the order FLRoof1, FLRoof2, FLRoof3, and the metadata was
cleared. The redaction step below then rebuilt every page.

The sample is vendor marketing material, but nothing shows that its people, property
and firms are fictitious. They were therefore all replaced before anything was parsed:

| What | Replaced with | Count |
|---|---|---|
| Applicant/insured name | `Jane Q Sample` | 1 |
| Inspected street address and city (state kept) | `100 Main St Anytown, Florida` | 1 |
| Application/policy number (header and page footer) | A random stand-in of the same length | 2 |
| Inspection company name (certification block and footer; ", LLC" kept) | `Anytown Roof Services` | 2 |
| A second firm named in the page footer | `Doe & Partners` | 1 |
| Inspector license number (`#` kept) | A random 5-digit stand-in | 1 |
| Work phone line number (area code kept) | `555-0131`, from the fiction-reserved 555-0100–0199 range | 1 |
| Inspector's handwritten signature | The handwriting stand-in "J Sample", set in IndieFlower | 1 |

The originals are not recorded anywhere in this folder, and the rules file stays outside
the repo. The vendor's own copyright line (SPECTACULAR), the dates, the license type
(`CCC`) and every roof value and checkbox were left as printed.

The replacement used `document-types/scripts/redact_scan.py`. It renders each page at
300 dpi, finds the values with OCR, paints over them and redraws each stand-in at the
original's size and ink, then rebuilds the page from the edited image alone. The
signature was erased and replaced. An OCR check found no original value on any output
page, the pages were checked by eye at 300 dpi, and every file in this folder was swept
for the originals. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

In Florida, insurers will not bind or renew many homeowners policies without a recent
roof inspection, so the form passes between inspectors, agents and underwriters on a
large share of home sales and renewals.

- **Property insurers and underwriters:** they decide eligibility and premium from the
  roof's covering, age, remaining life and condition.
- **Insurance agents:** they collect the form from the homeowner's inspector and submit
  it with the application.
- **Home inspectors:** they complete and certify the form, often in inspection software
  like the vendor's here.
- **Mortgage lenders and closing agents:** a purchase cannot close until the buyer has
  insurance, which can depend on this form.
- **Roofing contractors:** they use the findings to quote repairs or replacement.

### What it contains

- **A scanned-style raster** with no text layer.
- **Checkboxes as data.** Overall condition, the damage list and the leak questions are
  all X-marked boxes.
- **A two-column form with one column blank.** The Secondary Roof column has labels and
  empty blanks only.
- **Values that contradict each other.** The form says the roof is 30 years old but
  records a 2011 roofing permit, marks the roof Satisfactory while checking visible hail
  damage, and answers No to visible leaks while checking Yes for interior ceilings.
- **A photo page** with four roof photographs.
- **A certification block** with a handwritten signature, license type and number.
