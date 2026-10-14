# Roof Inspection or Certification

Source assets for `landing.ai/document-type/roof-inspection-certification`.

## Sample document

`source/roof-inspection-form.pdf` is a completed Florida **Roof Inspection Form**, the
four-point-style roof certification that Florida property insurers ask a licensed
inspector to complete before they bind a policy. It shows the output of the Citizens Roof
Inspection library in the Spectacular Inspection System. The inspector recorded an
asphalt shingle roof, 30 years old with 4 years of remaining life and a last permit in
2011, rated Satisfactory, with visible hail damage and a leak shown on an interior
ceiling.

**3 pages, portrait, raster.** These are page images at 300 dpi with no text layer:

- Page 1: the property header and the Roof section (Predominant and Secondary roof
  columns).
- Page 2: comments, the inspector's certification block and the underwriting
  instructions.
- Page 3: the photo page, with four roof photographs.

The source report has four pages, but page 3 is not published, so the PDF's third page
is printed "Page 4 of 4".

| | |
|---|---|
| Publisher | Spectacular Inspection System (AaceSystems), inspection-software vendor |
| Source | [spectacularapp.com/images/FLRoof1.jpg](https://www.spectacularapp.com/images/FLRoof1.jpg), with FLRoof2.jpg and FLRoof3.jpg, linked under "Sample Report" on the vendor's [Roof Inspection Form product page](https://www.spectacularapp.com/Roof-Inspection-Form.aspx) |
| Retrieved | 2026-10-13, by script |
| Clearance | **Redacted**, see below |

### How the PDF was made

The vendor publishes the sample as three separate JPEG page images, and they were
downloaded with `curl`. Each is 2550 x 3300 px at 300 dpi, which is US Letter. PyMuPDF
put them into one PDF, one per 612 x 792 pt page, in the order FLRoof1, FLRoof2,
FLRoof3. The JPEG bytes were inserted without re-encoding and the metadata was cleared
with `document-types/scripts/pdfmeta.py`. The redaction step below then rebuilt every
page.

## Redaction

The sample is vendor marketing material, but nothing shows that its people, property
and firms are fictitious. They were therefore all replaced before anything was parsed.

| What | Replaced with | Count |
|---|---|---|
| Applicant/insured name | `Jane Q Sample` | 1 |
| Inspected street address and city (state kept) | `100 Main St Anytown, Florida` | 1 |
| Application/policy number (header and page footer) | A random stand-in of the same length from `plausible.py` | 2 |
| Inspection company name (certification block and footer; ", LLC" kept) | `Anytown Roof Services` | 2 |
| A second firm named in the page footer | `Doe & Partners` | 1 |
| Inspector licence number (`#` kept) | A random 5-digit stand-in from `plausible.py` | 1 |
| Work phone line number (area code kept) | `555-0131`, from the fiction-reserved 555-0100–0199 range | 1 |
| Inspector's handwritten signature | The handwriting stand-in "J Sample", set in IndieFlower | 1 |

The originals are not recorded anywhere in this folder. The rules file stays outside the
repo. The vendor's own copyright line (SPECTACULAR), the dates, the licence type (`CCC`)
and every roof value and checkbox were left as printed.

The replacement used `document-types/scripts/redact_scan.py`. It renders each page at
300 dpi, finds the values with Tesseract OCR, paints over them and redraws the stand-in
at the original's cap height and ink. It then rebuilds the page from the edited image
alone. OCR read every value, so no `--place` regions were needed. The header and
certification values are bold and were redrawn in Arial Bold (`--bold`); the footer is
regular weight. The signature was removed with `--erase` over a region that stops short
of the box border, the italic line above and the signature rule. The script's own OCR
check found no original on any output page, on literals or on digits. The pages were
also checked by eye on 300 dpi renders, and every file in this folder was swept with
`ship.py check --rules`.

## Why this document

Roof inspections are a gate in Florida property underwriting, and this one is a real
software vendor's output rather than a blank template. It tests:

- **Checkboxes as data.** Overall condition, the damage list and the leak questions are
  all X-marked boxes. ADE renders them as `[x]` and `[ ]`, and extraction reads them
  correctly, including the "If updated" boxes, which are both empty.
- **A two-column form with one column blank.** The Secondary Roof column has labels and
  empty blanks only. Extraction reads the Predominant column and correctly reports no
  secondary roof.
- **Values that contradict each other.** The form says the roof is 30 years old but
  records a 2011 roofing permit. It marks the roof Satisfactory while checking Visible
  hail damage, and it answers No to visible leaks while checking Yes for interior
  ceilings. Extraction reports what is written and does not reconcile any of it. That is
  the right behaviour, and it leaves the conflicts for an underwriting rule to catch.
- **A photo page.** Page 3 parses as a `PHOTOGRAPH` figure with a written description
  of the four photos, including the mismatched replacement shingles. Extraction counted
  4 photos.

`schema.json` was written for this run: **24 leaf fields**, counted from the schema. It
covers the property header, the Predominant Roof column, whether a secondary roof is
present, the comments, the inspector block and the photo count.

## Featured fields: the predominant roof, page 1

| Field | Value |
|---|---|
| Roof covering material | Asphalt shingles |
| Roof age in years | 30 |
| Date of last roofing permit | 2011 |
| Overall condition | Satisfactory (checkbox) |
| Visible damage checked | Visible hail damage (checkbox) |

The request suggested six fields, all on page 1, and all six ground `ok`. The limit is
five, so one was dropped: remaining useful life (4 years, also `ok`). The other five keep
both of the sample's inconsistencies on one overlay, the age against the permit date and
the condition against the hail damage. No person's name is featured.

## Grounding and extraction on this document

- **Every value checked is right.** Extraction returned all 24 leaves correctly.
- **Checked boxes ground tightly.** `Satisfactory` and `Visible hail damage` each box
  only the checked option's row, not the whole group.
- **Yes/No pairs ground OFF.** The leak answers are booleans, and their ranges cover the
  whole `[ ] Yes [x] No` line. That supports the value but cannot be shown as it, so
  they were not featured.
- **An answer from two empty boxes is SYNTH.** "Not updated" has no range at all, since
  nothing on the page says it. A blank "Date of last update" grounds OFF to the empty
  line.
- **Two values share one range.** The policy number grounds to the whole header line,
  together with the applicant name. That is `ok`, but the box is wide.
- **The first schema needed tightening.** With nullable enums, extraction filled the
  blank update date with the string `"null"`. It also picked "Full replacement" when
  neither update box was checked. Explicit "Not updated" and "Not marked" values, and an
  empty string for a blank date, fixed both. The fix needed one re-run of extraction
  with `--extract-only`, not a re-parse.

## Credits

7.00 credits at standard tier, through the jobs API: 5.00 for the first parse and
extract, and 2.00 for the one extract-only re-run after the schema fix. Parse used
`dpt-3-pro-latest`, which ran as `dpt-3-pro-20260710`; extract ran as
`extract-20260819`.

## Regenerate

```bash
# Assemble the source (scratch directory, outside the repo)
for i in 1 2 3; do curl -sSLO https://www.spectacularapp.com/images/FLRoof$i.jpg; done
# PyMuPDF: new_page(612x792) per JPEG, insert_image(page.rect, stream=<jpeg bytes>),
# in order FLRoof1, FLRoof2, FLRoof3; pdfmeta.clear(); save as assembled.pdf

# Redact (rules.json outside the repo)
.venv/bin/python document-types/scripts/redact_scan.py assembled.pdf roof-inspection-form.pdf \
    --rules <outside-the-repo>/rules.json \
    --bold "1:<name rule>" "1:<address rule>" "1:<policy rule>" \
           "2:<company rule>" "2:<licence rule>" "2:<phone rule>" \
    --erase "2:60,230.5,146,264.2" "2:64,236,140,258=J Sample" \
    --handwriting-font document-types/scripts/fonts/IndieFlower-Regular.ttf

.venv/bin/python document-types/scripts/run_ade.py roof-inspection-certification
.venv/bin/python document-types/scripts/build_images.py roof-inspection-certification
```
