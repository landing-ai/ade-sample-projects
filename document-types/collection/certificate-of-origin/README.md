# Certificate of origin

**On the website:** [landing.ai/document-type/certificate-of-origin](https://landing.ai/document-type/certificate-of-origin)

A preferential Certificate of Origin, Form L, issued in Guangzhou on 3 November 2011
under the China–Costa Rica Free Trade Agreement for two lines of footwear shipped from
Xiamen to San José. It names the exporter, producer and importer, the vessel and ports,
the goods with their HS codes and origin criteria, and the invoice. It carries the
exporter's declaration and the certifying authority's stamp and signature.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 42 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 3,490 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 13.4 s |
| Per page | 13.4 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.4 credits |
| Per page | 1.40 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:39 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 42 |
| Non-null fields returned | 41 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 163.6 s |
| Per schema field (42) | 3.90 s |
| Per value returned | 3.56 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 2.6 credits |
| Per schema field (42) | 0.062 credits |
| Per value returned | 0.057 credits |

## Origin

`source/certificate-of-origin.pdf` is a preferential **Certificate of Origin, Form L**,
issued in Guangzhou on 3 November 2011 under the China–Costa Rica Free Trade Agreement
for two lines of footwear shipped from Xiamen to San José. It is **1 page, portrait**, a
single 150 dpi colour scan of the issued certificate on its pale-blue security paper:
typed values, the exporter's red company chop, the certifying authority's red seal, two
handwritten signatures and a barcode.

| | |
|---|---|
| Publisher | Cargo From China (freight forwarder), as its "Form L sample" |
| Source | [cargofromchina.com/…/Form-L-China-Costa-Rica.jpg](https://cargofromchina.com/wp-content/uploads/Form-L-China-Costa-Rica.jpg) |
| Retrieved | 2026-10-03, downloaded directly by script |
| Clearance | Public |

Cargo From China publishes the image on its
[China Certificate of Origin](https://cargofromchina.com/certificate-of-origin/) page as
the "Form L sample" for Costa Rica, alongside samples of the other Chinese FTA forms. The
JPEG was wrapped, unaltered, in a one-page PDF at its native resolution, with no metadata.

The image carries a `jdol.com.cn` watermark in its corner, so the forwarder republished
it from an earlier Chinese source; the forwarder's page is the provenance of record. It
is an issued certificate, not a blank or a specimen. Every party it names (exporter,
producer, importer and the shipping marks) is a company. The two handwritten signatures,
the exporter's signatory in box 13 and the certifying official in box 14, carry no
printed names. It is kept as published by decision of the operator. Full provenance is
in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A certificate of origin states where goods were made. A preferential one, like this
Form L, lets the importer claim the reduced duty rate under a free trade agreement.

- **Customs brokers:** they check the HS codes, origin criteria and shipment details
  before claiming the preferential rate on an import entry.
- **Customs authorities:** officers verify the certificate against the invoice and the
  goods, and audit preference claims after release.
- **Exporters and freight forwarders:** they prepare and submit certificates to the
  certifying body and send them on with the shipping documents.
- **Banks and trade finance:** letters of credit often require a certificate of origin
  among the documents presented for payment.
- **Trade compliance teams:** importers keep certificates on file to support duty
  savings and answer verification requests.

### What it contains

- **Values typed across the printed captions,** overprinting them in several boxes.
- **A security-paper watermark** of faint Chinese text across the whole page.
- **Two red stamps over printed text,** one of them crossing the certifying body's date
  line.
- **Two handwritten signatures** with no printed names.
- **A goods table** with a merged marks column, origin codes and HS codes printed with a
  space after the dot.
- **A barcode** and a printed form serial.
- **A single colour scan,** so every value has to be read from the page image.
