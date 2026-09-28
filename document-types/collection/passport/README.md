# Passport

Source assets for `landing.ai/document-type/passport`.

## Sample document

`source/japan-passport-specimen-2025.jpg` — the official specimen of the identity page of
Japan's 2025 passport. **1 image, landscape (600×449)**, bilingual Japanese and English,
with a two-line machine-readable zone (MRZ) along the bottom.

| | |
|---|---|
| Publisher | Ministry of Foreign Affairs of Japan (specimen), as published by The Japan News (Yomiuri Shimbun) |
| Source | [japannews.yomiuri.co.jp/…/new-passport-design.jpg](https://japannews.yomiuri.co.jp/wp-content/uploads/2025/01/new-passport-design.jpg) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Every field is specimen data: the holder is "GAIMU SAKURA" (*gaimu* means "foreign
affairs"), passport no. ZZ0000826, with "SPECIMEN" printed across the page. The portrait
is the ministry's specimen model, not a passport holder. No redaction was needed.

**Provenance is weaker than it should be.** The request's url is The Japan News image of
the specimen. That site answers scripted requests with an empty page, and the ministry's
own pages refuse them outright, so neither could be downloaded or checked. At the document
owner's decision, the file used is `doc43-passport_japan.jpeg` from the ADE Documents
shared drive. **It could not be verified to be the same file as the url.** It is 600×449
and shows a page curl along the top edge, as if photographed rather than exported. The
stronger source would be the ministry's own specimen, on
[「2025年旅券」導入開始](https://www.mofa.go.jp/mofaj/ca/pss/pagew_000001_01518.html) or
[旅券（パスポート）の変更について](https://www.mofa.go.jp/mofaj/toko/passport/pagew_000001_01253.html),
downloaded by hand.

Full provenance is in `manifest.json` under `source.origin`, where the authoring tooling
can read it — this section is the human-readable version.

## Why this document

The collection's first **passport**, and its first document in two scripts:

- **Bilingual labels.** Every field is labelled in Japanese and English ("姓 / Surname"),
  and the page carries a Registered Domicile (本籍) that a Western passport does not.
- **A handwritten signature in Japanese.** The bearer's signature, 外務 さくら, is written
  by hand in kanji and hiragana.
- **A machine-readable zone.** Two lines of OCR-B text, the same data again in a fixed
  format, with check digits.
- **The same schema as the driver's license.** `schema.json` is the team's government-ID
  schema, identical to the one used for `drivers-license-usa`, so the two pages show one
  schema across two very different documents.

## Featured fields: the document and when it was issued

All on the identity page. The request named no fields; nationality was in the first
choice and was swapped for the date of issue at the document owner's request:

| Field | Value |
|---|---|
| Document type | Passport |
| Passport number | ZZ0000826 |
| Issuing country | JAPAN |
| Sex | F |
| Date of issue | 2025-03-24 |

No name is featured, although the name is specimen data.

**The date of issue is flagged, and correct.** Extraction returns it as the ISO date
2025-03-24 and grounds it to the printed "24 MAR 2025", so `build_images.py` warns that the
value is not in the boxed text. It is the same date in another format, and the box sits on
the issue date rather than the expiry date printed directly beneath it; the crop was
checked by eye.

## What it surfaced

**One value, two places.** Issuing country and nationality are both "JAPAN", and they
ground to different text: issuing country to the country name in the page header, and
nationality to the Nationality field. The page's own Issuing country field prints the
three-letter code "JPN"; extraction took the header's "JAPAN" instead, which is also right.

**The parse reads both scripts and the handwriting.** Every bilingual label comes back
intact, as do the Registered Domicile, "TOKYO", and the handwritten signature, returned as
the text 外務 さくら. Both MRZ lines come back character for character.

**A general schema meets a specific document.** The schema covers passports and driver's
licenses alike, so it asks for fields a passport does not carry: issuing state, eye
colour, height, weight and place of birth all correctly come back null. `state_issuing` is
required, which produces a `nonconformant_output` warning. On the Texas license it was
`place_of_birth` that failed, and here it is `state_issuing`: the same schema has a
different gap for each document type. The schema is the team's and is used unchanged.

**Dates are normalized.** Birth, issue and expiry dates come back as ISO dates, so they no
longer match the printed "24 MAR 2025" and are flagged, though they are right.

## Extraction

**15 leaf fields**, the same `doc43-government-id-schema.json` as the driver's license,
used unchanged. Everything printed on the page that the schema asks for extracts
correctly.

## Cost

**1.20 credits** at standard tier for 1 image: 0.70 to parse, 0.50 to extract.

## Regenerating

```bash
# The source is doc43-passport_japan.jpeg from the ADE Documents shared drive.
.venv/bin/python document-types/scripts/run_ade.py passport                # 1.20 credits
.venv/bin/python document-types/scripts/run_ade.py passport --extract-only # 0.50, schema iteration
.venv/bin/python document-types/scripts/build_images.py passport           # free
.venv/bin/python document-types/scripts/inspect_fields.py passport --page 1
```
