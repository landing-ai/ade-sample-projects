# Life Insurance Application

Source assets for `landing.ai/document-type/life-insurance-application`.

## Sample document

`source/jhny17_app.pdf`: John Hancock Life Insurance Company of New York's *Application
for Life Insurance*, form NB5000NY (version 06/2012). The carrier filled it in with
specimen data: an application by "John M. Doe", a company president, for $250,000 of JH
Universal Life on a single life. The owner is the insured and the primary beneficiary is
his son. **7 pages, portrait, scanned**: page scans at about 96 dpi with no text layer.
Pages 1 to 3 hold the insured, owner, beneficiary, coverage and funding sections. Pages 4
to 6 hold the replacement, lifestyle, medical and temporary insurance questions and the
declarations. Page 7 is the authorization and the signature block, which is unsigned.

| | |
|---|---|
| Publisher | John Hancock Life Insurance Company of New York, filed on SEC EDGAR (CIK 1043846, accession 0001193125-17-327052) |
| Source | [sec.gov/…/d481410dex99e.htm](https://www.sec.gov/Archives/edgar/data/1043846/000119312517327052/d481410dex99e.htm), Exhibit 99.(E) "Specimen policy application" ([filing index](https://www.sec.gov/Archives/edgar/data/1043846/000119312517327052/)) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted**, see below |

### How the PDF was made

EDGAR publishes this exhibit as an HTML page that embeds seven JPEG page scans,
`g481410new93.jpg` to `g481410new99.jpg`, which sit in the same filing folder. The HTML
and the seven images were downloaded with `curl`, using a User-Agent that carries a
contact address, as EDGAR requires. The images were then assembled with PyMuPDF into
one PDF, in the order the HTML embeds them. Each JPEG went onto its own page at its
native size, at 96 dpi, so the pages measure about 7.0 x 9.3 in. The JPEG bytes were
inserted without re-encoding. The PDF's metadata was cleared with
`document-types/scripts/pdfmeta.py`.

## Redaction

This is a specimen, and almost everything filled in is obviously sample data: John M.
Doe, an SSN of sequential digits, 1999 March Street in Anytown, ABC Company, and a
physician named Arther H. Smith at 123 Main Street. Those values were left as filed.

Three values were replaced, all on page 1:

| What | Replaced with | Count |
|---|---|---|
| Specimen telephone line numbers (personal and business) on a real area code | `555-0111` and `555-0144`, from the fiction-reserved 555-0100–0199 range, drawn by `plausible.py`. The area code was kept. | 2 |
| Specimen email address on a real mail domain | `johndoe@example.com` | 1 |

The originals are not recorded anywhere in this folder. The rules file stays outside the
repo.

The replacement used `document-types/scripts/redact_scan.py`. It rebuilds the page from a
300 dpi render of the edited image, so the original raster is not carried into the
output. Only page 1 was rebuilt. Pages 2 to 7 are the original JPEG scans, unchanged.

**Tesseract could not read these values.** They are blue, bold, underlined serif type at
about 96 dpi, and OCR found none of the three. So `redact_scan.py` gained a `--place
PAGE:X0,Y0,X1,Y1=TEXT` option for this document. It takes a region in PDF points, paints
it with the page's background, and redraws a rule's replacement there. It redraws
through the same path as an OCR hit, at the original's measured cap height and ink
colour. `TEXT` is a rule's replacement, or the part of one that stands at the same
offset in its original. That lets a rule cover the whole phone number while only the
line number, printed apart from its area code, is redrawn. The command line also never
carries an original. The regions stop just above the underlines, so the underlines
survive.

Because OCR could not read the originals, its verification pass proves little on this
document. The result was also checked by eye on 300 dpi renders, and every file in this
folder was swept for the originals with `ship.py check --rules`.

## Why this document

It is a real carrier form rather than a mock-up, filled in by the carrier, which is rare
for an insurance application. Applications are almost never published with data in
them. It tests:

- **Checkboxes carrying the answer.** Owner, death benefit option, qualification test,
  purpose of insurance, premium frequency and every yes/no question are checked boxes,
  not written values.
- **Comb fields.** The date of birth is written one character per box (`O C T | 0 4 |
  1 9 6 7`). Extraction returned `OCT 04 1967`.
- **Low resolution.** The scans are about 96 dpi.
- **Two-life layout.** The form has Life One and Life Two columns and sections, with Life
  Two left blank. The schema reads Life One.

`schema.json` was written for this run: **38 leaf fields**, counted from the schema. It
covers the insurer and form, the proposed insured, owner, beneficiaries, coverage,
premium funding, replacement, pending coverage, tobacco, last medical consultation and
temporary insurance. It deliberately leaves out the SSN and driver's licence fields.

## Featured fields: who owns it, who is paid, what and how much

All on page 2.

| Field | Value |
|---|---|
| Policy owner | Proposed Life Insured One (checkbox) |
| Primary beneficiary relationship | SON |
| Product name | JH UNIVERSAL LIFE |
| Base face amount | 250000 |
| Death benefit option | Option 1 (Face Amount/TFA) (checkbox) |

These follow the request's suggestions. The beneficiary's name was avoided in favour of
the relationship. The name also grounds `OFF`: it is written across three separate
underlined blanks, and each range covers only one of them. The Guideline Premium
qualification test grounds cleanly and is correct, but was left out to keep to five. The
100% beneficiary share also grounds cleanly. The medical and lifestyle pages were not
considered for featuring.

## Grounding and extraction on this document

- **Every top-level field was populated, and every value checked is right.** That
  includes the checkboxes, the income figures, net worth written as `$2.6 M`, and the
  combed date of birth.
- **A checkbox grounds to its whole row.** The owner and death benefit option boxes take
  in the question label and every option on the line, including the unchecked ones. The
  value is in the box, but the box does not single out the ticked option.
- **The relationship grounds to the cell, header included.** It boxes the "Relationship
  to Proposed Life Insured(s)" label together with `SON`. `build_images.py` warned that
  OCR could not read `SON` in the box, but the crop does contain it.
- **The base face amount box runs on** across the line into the blank "Supplemental Face
  Amount" field beside it.
- **Split values ground OFF.** A name typed across separate First, Middle and Last
  blanks grounds to one blank per range.

## Credits

17.60 credits at standard tier, through the jobs API (parse with `dpt-3-pro-latest`,
which ran as `dpt-3-pro-20260710`, plus extract).

## Regenerate

```bash
# Assemble the source (scratch directory, outside the repo)
B=https://www.sec.gov/Archives/edgar/data/1043846/000119312517327052
for i in 93 94 95 96 97 98 99; do
  curl -A "<name> <contact email>" -O $B/g481410new$i.jpg
done
# PyMuPDF: one page per JPEG at 72/96 of its pixel size, insert_image unchanged, in order;
# pdfmeta.clear(); save as jhny17_app.pdf

# Redact page 1 (rules.json outside the repo), then join it to original pages 2-7
.venv/bin/python document-types/scripts/redact_scan.py jhny17_app.pdf p1.pdf --pages 1 \
    --rules <outside-the-repo>/rules.json \
    --font "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf" \
    --place "1:114.0,169.2,145.4,174.2=555-0111" "1:200.4,169.2,231.8,174.2=555-0144" \
            "1:341.3,169.2,423.8,174.2=johndoe@example.com"

.venv/bin/python document-types/scripts/run_ade.py life-insurance-application
.venv/bin/python document-types/scripts/build_images.py life-insurance-application
```
