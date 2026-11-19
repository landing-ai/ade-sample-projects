# Life Insurance Application

**On the website:** [landing.ai/document-type/life-insurance-application](https://landing.ai/document-type/life-insurance-application)

John Hancock Life Insurance Company of New York's Application for Life Insurance, form
NB5000NY, filled in by the carrier with specimen data. It applies for $250,000 of
universal life cover on a single life, and covers the insured, owner and beneficiary,
the coverage and funding, replacement and medical questions, and the declarations and
authorization.

| | |
|---|---|
| Pages | 7 |
| Fields in the extraction schema | 38 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:31 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 29,218 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 25.9 s |
| Per page | 3.7 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 10.9 credits |
| Per page | 1.56 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:32 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 38 |
| Non-null fields returned | 37 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 150.3 s |
| Per schema field (38) | 3.96 s |
| Per value returned | 4.06 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 7.2 credits |
| Per schema field (38) | 0.189 credits |
| Per value returned | 0.195 credits |

## Origin

`source/jhny17_app.pdf` is John Hancock Life Insurance Company of New York's
**Application for Life Insurance**, form NB5000NY (version 06/2012). The carrier filled
it in with specimen data: an application by "John M. Doe", a company president, for
$250,000 of JH Universal Life on a single life. The owner is the insured and the primary
beneficiary is his son. It is **7 pages, portrait**, page scans at about 96 dpi with no
text layer. Pages 1 to 3 hold the insured, owner, beneficiary, coverage and funding
sections. Pages 4 to 6 hold the replacement, lifestyle, medical and temporary insurance
questions and the declarations. Page 7 is the authorization and the signature block,
which is unsigned.

| | |
|---|---|
| Publisher | John Hancock Life Insurance Company of New York, filed on SEC EDGAR (CIK 1043846, accession 0001193125-17-327052) |
| Source | [sec.gov/…/d481410dex99e.htm](https://www.sec.gov/Archives/edgar/data/1043846/000119312517327052/d481410dex99e.htm), Exhibit 99.(E) "Specimen policy application" ([filing index](https://www.sec.gov/Archives/edgar/data/1043846/000119312517327052/)) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted**, see below |

EDGAR publishes this exhibit as an HTML page that embeds seven JPEG page scans, which sit
in the same filing folder. The images were downloaded by script and assembled into one
PDF in the order the HTML embeds them. Each JPEG went onto its own page at its native
size, at 96 dpi, so the pages measure about 7.0 x 9.3 in. The JPEG bytes were inserted
without re-encoding, and the PDF's metadata was cleared.

This is a specimen, and almost everything filled in is obviously sample data: John M.
Doe, an SSN of sequential digits, 1999 March Street in Anytown, ABC Company, and a
physician named Arther H. Smith at 123 Main Street. Those values were left as filed.
Three values on page 1 were replaced:

| What | Replaced with | Count |
|---|---|---|
| Specimen telephone line numbers (personal and business) on a real area code | `555-0111` and `555-0144`, from the fiction-reserved 555-0100–0199 range. The area code was kept. | 2 |
| Specimen email address on a real mail domain | `johndoe@example.com` | 1 |

The originals are not recorded anywhere in this folder. Page 1 was rebuilt from a 300
dpi render of the edited image, so the original raster is not carried into the output.
Pages 2 to 7 are the original JPEG scans, unchanged. The values are blue, bold,
underlined serif type that OCR could not read, so each region was placed by hand and the
stand-in redrawn at the original's cap height and ink color, leaving the underlines in
place. The result was checked by eye on 300 dpi renders, and every file in this folder
was swept for the originals. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

The application is the insured's signed statement of who is covered, for how much and
for whose benefit, and it becomes part of the policy. Carrier forms are rarely
published with data in them.

- **Life insurers:** new business and underwriting teams check each application for
  completeness and assess the medical and lifestyle answers.
- **Brokers, agents and BGAs:** agencies submit applications and track what is missing
  before a case can be placed.
- **Claims:** at a death claim, insurers compare the application's answers with medical
  records during the contestability period.
- **Reinsurers:** reinsurers review application data on large or facultative cases.
- **Compliance and replacement review:** the replacement questions trigger state-
  required review when an existing policy is being replaced.

### What it contains

- **Checkboxes carrying the answer.** Owner, death benefit option, qualification test,
  purpose of insurance, premium frequency and every yes/no question are checked boxes.
- **Comb fields.** The date of birth is written one character per box.
- **Low-resolution scans,** at about 96 dpi, with no text layer.
- **A two-life layout,** with Life One and Life Two columns and sections, and Life Two
  left blank.
- **Values split across separate blanks,** such as names typed into First, Middle and
  Last fields.
- **Long question-and-answer pages** for medical, lifestyle and replacement questions.
- **An unsigned signature block** on the last page.
