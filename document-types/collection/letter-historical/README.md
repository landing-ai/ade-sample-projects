# Letter (Historical)

A 19th-century lithographed facsimile of **William Penn's letter to the Lenape**. Penn wrote it
in England in 1682, before sailing to Pennsylvania, and it was delivered and read aloud by his
surveyor general, Thomas Holme. It begins "The Great God who is the power and wisdom that made
you and me…". Penn promises fair dealing and that none of his people will wrong them, and signs
"Your Loving Freind, Wm Penn". Holme's delivery note sits below, beside the Pennsylvania seal.

Above the letter is an engraving after Benjamin West's painting *Penn's Treaty with the
Indians*. The source is one portrait page, a 704×1024 image.

## Provenance

| | |
|---|---|
| Publisher | Library of Congress, Prints and Photographs Division (`pga.08522`) |
| Source URL | https://tile.loc.gov/storage-services/service/pnp/pga/08500/08522v.jpg |
| Retrieved | 2026-11-16 (downloaded manually; the file is dated 2026-11-15) |
| Clearance | `public` |

loc.gov refuses scripted access, so the operator downloaded the JPEG by hand. The LOC handle
`hdl.loc.gov/loc.pnp/pga.08522` is embedded in the file's comment field. The item's catalogue
record and rights statement **could not be read by script**. Library of Congress Prints and
Photographs items of this age are normally "no known restrictions on publication". The image
was wrapped in a one-page PDF with no metadata.

It is published as printed under the historical-record exemption:

- **The record is far past the 72-year line.** The letter is dated 1682, and the print is
  19th century.
- **William Penn**, the founder of Pennsylvania, died in 1718.
- **Thomas Holme**, who signs the delivery note, died in 1695. Source: Irma Corcoran,
  *Thomas Holme, 1624–1695: Surveyor General of Pennsylvania*, American Philosophical Society,
  1992.

**Requested as "Treaty (Historical)".** The document is not a treaty: it has no parties agreeing
terms, no articles and no ratification. The treaty is only the subject of the engraving above
the letter. The operator renamed the type to Letter (Historical).

## Why this document

It is **17th-century secretary-influenced handwriting**, reproduced as a lithograph:

- long s, "ye" and "yt" abbreviations, and spellings such as "freind" and "Rumme" (rum)
- an old-style dateline ("25: 2: 1682", meaning 25th of the second month)
- a flourished signature
- a second hand writing the delivery note

All of it sits under a large engraving.

## Featured fields (page 1)

| Field | Value |
|---|---|
| Opening line | The Great God, who is the power and wisdom that made you and |
| Dateline | 25: 2: 1682 |
| Closing | Your loving freind |
| Signature | Wm Penn |
| Delivered by | Tho: Holme |

These follow the letter as a letter: how it opens, when it was written, how it closes, who
signed it, and who delivered it. The dateline's place, England, shares its box and is not
featured separately.

## Grounding on this document

**The handwriting grounds line by line.** Each handwritten value grounds to its own line,
including the flourished "Wm Penn" signature and Holme's note in a different hand.
`build_images.py` flags all five, because OCR cannot read 17th-century script. Every crop was
opened and contains its value.

**Transcription is good, not literal.** The model keeps "freind" and the old-style date as
written, but modernizes the punctuation of the opening line.

**Interpreted fields ground `OFF`.** The schema asks for the promises, paraphrased into modern
English, and for a caption for the engraving. Both ground `OFF`, as they should, because the
words are not on the page.

**The printer's imprint is unchecked.** The imprint under the letter is tiny at this resolution.
It extracts as "Sold by J. C. Whitney & Co., Baltimore", but that reading could not be confirmed
from the image, and it was not featured.

## Credits

2.30 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py letter-historical
.venv/bin/python document-types/scripts/inspect_fields.py letter-historical --page 1
.venv/bin/python document-types/scripts/build_images.py letter-historical
```

The schema has 12 leaf fields.
