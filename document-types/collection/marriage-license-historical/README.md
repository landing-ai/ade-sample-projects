# Marriage License (Historical)

The 1886 Hamilton County, Ohio marriage license of **William Howard Taft and Helen Louise Herron**,
issued June 19, 1886 and returned the same day. It has two parts:

- a printed probate-court affidavit, completed in ink
- the marriage return at the foot, with the officiant's certification

The image is a Bain News Service glass-plate photograph of the license, taken around 1910–15
while Taft was President. It is one landscape page in greyscale: a photo of a ledger page, with
the negative's handwritten caption ("TAFT MARRIAGE LICENSE") running up the left margin.

## Provenance

| | |
|---|---|
| Publisher | Library of Congress, Prints and Photographs Division (Bain News Service collection), via Wikimedia Commons |
| Source URL | https://upload.wikimedia.org/wikipedia/commons/b/bd/Taft_Marriage_License%2C_Ohio_LOC_2162683291.jpg |
| Retrieved | 2026-11-15 |
| Clearance | `public` |

The Library of Congress lists the image with "no known restrictions on publication" (Flickr ID
2162683291). It was downloaded by script from Commons as a 1024×751 greyscale JPEG and wrapped in
a one-page PDF with no metadata.

It is published as printed, with no redaction, under the historical-record and public-figure
exemptions:

- **The record is more than 72 years old.** It is dated June 19, 1886 on its face.
- **Both people named in it are deceased public figures.** William Howard Taft, 27th President
  of the United States, died March 8, 1930. Helen Herron Taft died May 22, 1943. Source:
  Encyclopaedia Britannica's biographies of each.
- **The other names appear in official roles.** These are the probate judge, the deputy clerk
  and the officiant.

## Why this document

Most of the collection is printed or typed. Here every value is **19th-century handwriting**,
some faded and some smudged. The page is a photograph of a bound ledger rather than a scan. The
form's fill-in lines put each handwritten value mid-sentence inside printed legal prose ("And
that ___ is more than eighteen years of age …").

## Featured fields (page 1)

| Field | Value |
|---|---|
| License number | 165 |
| Applicant | William H Taft |
| Intended spouse | Helen L Herron |
| Probate judge | Herman Hoebel |
| Officiant | Minister of the Gospel |

The overlay follows the license from issue to return: its number, the two people named in the
affidavit, the judge who granted it, and the officiant's line in the return. Named individuals
are featured here because they are the substance of a marriage license, and these are a
president and first lady, both long deceased.

## Grounding on this document

**The handwriting grounds line by line.** Each handwritten value grounds to the line it sits on,
even where it is embedded in printed prose. The box for the applicant takes in the whole line,
"and for the County of Hamilton … who being", so the crop shows the value in context rather than
alone.

**OCR cannot check cursive.** `build_images.py` warns on all five fields, because Tesseract
cannot read cursive. Every crop was opened and contains its value.

**Readings that need care:**

- **The probate judge's surname** is read as "Hoebel". The flourished capital could also be
  read "Froebel".
- **The officiant's name** under "Minister of the Gospel" is smudged. It extracts as "A. Hogg",
  and was not featured.
- **The licence number** is "165" in a hand-ruled box. The model read it correctly.

**Dates come back `OFF`, and they are right.** The schema asks for YYYY-MM-DD, so "1886-06-19"
does not appear literally in "19 day of June 1886". Both dates are correct and ground to their
lines.

## Credits

1.50 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py marriage-license-historical
.venv/bin/python document-types/scripts/inspect_fields.py marriage-license-historical --page 1
.venv/bin/python document-types/scripts/build_images.py marriage-license-historical
```

The schema has 14 leaf fields.
