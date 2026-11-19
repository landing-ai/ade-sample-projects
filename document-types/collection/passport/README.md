# Passport

**On the website:** [landing.ai/document-type/passport](https://landing.ai/document-type/passport)

The official specimen of the identity page of Japan's 2025 passport, with labels in
Japanese and English. It shows the passport type and number, the issuing country, the
holder's name, nationality, sex, dates of birth, issue and expiry, a portrait, a
handwritten signature, and a two-line machine-readable zone. Every value is specimen
data.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 15 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:41 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 686 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 4.0 s |
| Per page | 4.0 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 0.7 credits |
| Per page | 0.70 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:41 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 15 |
| Non-null fields returned | 10 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 92.5 s |
| Per schema field (15) | 6.17 s |
| Per value returned | 9.25 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 0.6 credits |
| Per schema field (15) | 0.040 credits |
| Per value returned | 0.060 credits |

## Origin

`source/japan-passport-specimen-2025.jpg` is the official specimen of the **identity
page of Japan's 2025 passport**. It is **1 image, landscape (600×449)**, bilingual
Japanese and English, with a two-line machine-readable zone (MRZ) along the bottom.

| | |
|---|---|
| Publisher | Ministry of Foreign Affairs of Japan (specimen), as published by The Japan News (Yomiuri Shimbun) |
| Source | [japannews.yomiuri.co.jp/…/new-passport-design.jpg](https://japannews.yomiuri.co.jp/wp-content/uploads/2025/01/new-passport-design.jpg) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

Every field is specimen data: the holder is "GAIMU SAKURA" (*gaimu* means "foreign
affairs"), passport no. ZZ0000826, with "SPECIMEN" printed across the page. The portrait
is the ministry's specimen model, not a passport holder. No redaction was needed.

**Provenance is weaker than it should be.** The source URL above is The Japan News image
of the specimen. That site answers scripted requests with an empty page, and the
ministry's own pages refuse them outright, so neither could be downloaded or checked. At
the document owner's decision, the file used is `doc43-passport_japan.jpeg` from the ADE
Documents shared drive. **It could not be verified to be the same file as the source
URL.** It is 600×449 and shows a page curl along the top edge, as if photographed rather
than exported. The stronger source would be the ministry's own specimen, on
[「2025年旅券」導入開始](https://www.mofa.go.jp/mofaj/ca/pss/pagew_000001_01518.html) or
[旅券（パスポート）の変更について](https://www.mofa.go.jp/mofaj/toko/passport/pagew_000001_01253.html),
downloaded by hand. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A passport is the standard proof of identity and nationality across borders, and many
businesses must read one before they can serve a customer.

- **Banking and fintech:** know-your-customer checks read the passport's identity page
  and MRZ when a customer opens an account.
- **Airlines and travel:** carriers capture passport details for advance passenger
  information before departure.
- **Hotels and car rental:** many countries require hotels to record foreign guests'
  passport details at check-in.
- **Employers and HR:** right-to-work checks and onboarding record the passport number,
  nationality and expiry date.
- **Immigration and visa services:** consulates, law firms and visa processors take the
  identity page data into applications.

### What it contains

- **Bilingual labels.** Every field is labeled in Japanese and English ("姓 / Surname"),
  and the page carries a Registered Domicile (本籍) that a Western passport does not.
- **A handwritten signature in Japanese,** written by hand in kanji and hiragana.
- **A machine-readable zone:** two lines of OCR-B text repeating the data in a fixed
  format, with check digits.
- **The same value in two places,** such as the issuing country in the page header and
  as a three-letter code in its own field.
- **A photograph** of the holder and security background patterns.
- **A photographed image** rather than a PDF, with a page curl along the top edge.
