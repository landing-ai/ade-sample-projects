# Stock Certificate (Historical)

**Stock Certificate No. 95** of The Ford Motor Company of Canada, Limited, for ten $100 shares,
issued at Walkerville, Ontario in November 1908. The holder is James Couzens, of Detroit. It is
signed by G. M. McGregor as Secretary and by **Henry Ford as President**.

The certificate is an engraved form completed by hand, with a guilloche border, blackletter
headings and a red foil seal. A red-ink "Cancelled" is scrawled diagonally across the middle,
and the back shows through faintly. The source is one landscape page, a high-resolution
photograph.

## Provenance

| | |
|---|---|
| Publisher | Wikimedia Commons; photograph by Julie Ceccaldi, certificate from the Sammlung Commodore (Rüdiger K. Weng) |
| Source URL | https://upload.wikimedia.org/wikipedia/commons/1/1c/Ford_Motor_Company_of_Canada_1908.jpg |
| Retrieved | 2026-11-15 |
| Clearance | `public` |

The photograph is released under **CC0**. It was downloaded by script as a 4080×3308 JPEG and
wrapped in a one-page PDF with no metadata.

It is published as printed under the historical-record exemption. The evidence:

- **The record's date.** It is dated 1908 on its face, and the Commons record gives
  1908-11-10.
- **Everyone named is a deceased public figure acting in a corporate role.**
  - James Couzens, Ford co-founder and later US Senator, died in 1936.
  - Henry Ford died in 1947.
  - Gordon M. McGregor, founder of Ford of Canada, died in 1922.

  Sources: the Detroit Historical Society's *Encyclopedia of Detroit* entry for Couzens, the
  Windsor Public Library's history of McGregor, and Henry Ford's biographies.

The Commons description names the holder as "Henry Couzens". The certificate clearly reads
**James** Couzens.

**This is not the document the request named.** The request named a photograph of Henry Ford's
own 1903 Ford Motor Company certificate, hosted by Investopedia. That image is a licensed Getty
Images photo (GettyImages-515176734), not released for reuse. The operator chose this CC0
certificate instead.

## Why this document

A stock certificate is a printed legal sentence with blanks filled in by hand. The holder, the
residence, the share count in words and the date all sit mid-sentence, in Edwardian
copperplate, among engraved type and ornament. On top of that, a cancellation is scrawled
across the text, and the reverse shows through the paper.

## Featured fields (page 1)

| Field | Value |
|---|---|
| Certificate number | 95 |
| Shareholder | James Couzens |
| Shares | Ten |
| Place of issue | Walkerville, Ontario |
| President | Henry Ford |

These follow the issue of certificate No. 95: its number, who holds it, how many shares, where
it was issued, and who signed it. Named individuals are featured because they are the substance
of a stock certificate, and here they are Ford's founders, all long deceased.

## Grounding on this document

**Every handwritten value grounds to its line.** The holder, the shares, the place and Henry
Ford's signature each get their own line box. Because the values are written into printed
sentences, each box takes in the whole line ("This Certifies that James Couzens"). OCR cannot
read the copperplate, so `build_images.py` flagged four of the five crops. Every crop was opened
and contains its value.

**Two extraction errors:**

- **The issue date is wrong.** It comes back as **1908-12-06** ("Sixth … December"). The
  handwriting, and the Commons record, give the **tenth of November**. The flourished "Tenth"
  and "November" were misread, and the field grounds `OFF`.
- **The cancellation is missed.** `cancelled` returns false with no grounding (`SYNTH`). The
  red "Cancelled" across the body is not seen.

**`number_of_shares` is right but grounds `OFF`.** It extracts as 10, but it grounds to the
handwritten "Ten" line rather than the "10" in the Shares box.

## Credits

1.70 credits at standard tier: parse plus extract, 1 page.

## Regenerate

```
.venv/bin/python document-types/scripts/run_ade.py stock-certificate-historical
.venv/bin/python document-types/scripts/inspect_fields.py stock-certificate-historical --page 1
.venv/bin/python document-types/scripts/build_images.py stock-certificate-historical
```

The schema has 13 leaf fields.
