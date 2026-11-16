# Immigration Visa (Historical)

A **United States Quota Immigration Visa**, No. 840, issued by the American Consular Service at
Riga, Latvia on February 2, 1927, under the Immigration Act of 1924. The bearer is classed as a
Preference immigrant on the Russian quota, travelling on a Soviet passport issued at Kiev.

It is a printed Government Printing Office form, filled in on a typewriter. It also carries:

- the bearer's photograph, with her handwritten signature across it
- a consular fee stamp and the vice consul's signature
- a file number written at the top
- the ribbon and seal of the visa packet

The source is one portrait page, a 600×820 greyscale image.

## Provenance

| | |
|---|---|
| Issued by | U.S. Department of State, American Consular Service, Riga |
| Hosted at | RootsWeb wiki (Ancestry) |
| Source URL | https://wiki.rootsweb.com/wiki/images/e/e5/ImmigrationVisa-lores.jpg |
| Retrieved | 2026-11-16, downloaded manually |
| Clearance | `public` |

This is a record of the US federal government. It is the kind of document held in the USCIS
**Visa Files** series (July 1, 1924 – March 31, 1944), the arrival records created when the 1924
act required immigrants to obtain a visa abroad.

RootsWeb blocks scripted access, so the operator downloaded the image by hand. Its RootsWeb
file-description page refused scripted access (HTTP 403). The uploader and any further
attribution **could not be checked**. RootsWeb is therefore recorded as the host, not the
publisher. The image was wrapped in a one-page PDF with no metadata.

It is published as printed, including the bearer's name and photograph, under the
historical-record exemption. The evidence:

- **The record is old enough.** It is dated February 2nd, 1927 on its face, more than 72 years
  ago.
- **The bearer is long deceased.** She is photographed as an elderly woman at that date.
- **The vice consul signs in an official role.**

## Why this document

The visa is laid out as two columns of typed blanks in printed legal sentences, plus:

- checkboxes (Preference / Nonpreference)
- paired blanks with captions underneath ("(Quota.)" and "(Nationality.)")
- a photo and stamps overlapping the text
- a two-line passport number (31014 / 585822)

It is a low-resolution image, as many genealogy-site copies are.

## Featured fields (page 1)

| Field | Value |
|---|---|
| Visa number | 840 |
| Consular post | RIGA, LATVIA |
| Quota category | Preference |
| Quota | Russian |
| Granted under | Immigration Act of 1924 |

These show the visa as an instrument of the 1924 quota system: its number, the consulate, the
preference box that was checked, the national quota it was charged to, and the act it was
granted under. No individual is featured.

## Grounding on this document

**Every typed value grounds to its line, and the checkbox is found.** That includes the checked
**Preference** box, which comes back as "[x] Preference", and the captioned quota blank.

**Some values that are right still ground `OFF`.**

- **Dates:** the four dates are right, but the schema normalizes them to YYYY-MM-DD, and several
  wrap across two lines ("the 20th / day of December, A.D. 1926").
- **Visa type:** "QUOTA Immigration Visa" is stacked on two lines, so no single line holds the
  whole value.

**The fee grounds to the wrong place.** It is extracted correctly as **$9.00**, but it grounds to
the parse's *description of the photograph* rather than to the "Fee $9.00" line, so it was not
featured.

**The passport number is read across both lines.** It comes back as "31014 / 585822".

## Credits

2.00 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py immigration-visa-historical
.venv/bin/python document-types/scripts/inspect_fields.py immigration-visa-historical --page 1
.venv/bin/python document-types/scripts/build_images.py immigration-visa-historical
```

The schema has 19 leaf fields.
