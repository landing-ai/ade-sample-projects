# Court Order for Alimony

**On the website:** [landing.ai/document-type/alimony-court-order](https://landing.ai/document-type/alimony-court-order)

A California stipulated judgment of dissolution (Judicial Council form FL-180) and the
FL-343 Spousal, Partner, or Family Support Order Attachment it incorporates, filled in
with specimen parties. The order has the respondent pay the petitioner $407 a month in
spousal support after a 15-year marriage, and lists both parties' monthly income.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 31 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:25 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 11,713 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 31.6 s |
| Per page | 7.9 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 5.0 credits |
| Per page | 1.25 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 31 |
| Non-null fields returned | 20 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 89.1 s |
| Per schema field (31) | 2.88 s |
| Per value returned | 4.05 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 3.4 credits |
| Per schema field (31) | 0.110 credits |
| Per value returned | 0.155 credits |

## Origin

`source/alimony-court-order-fl-180-fl-343.pdf` is a California stipulated judgment of
dissolution (Judicial Council form **FL-180**, pages 1-2) and the **FL-343 Spousal,
Partner, or Family Support Order Attachment** it incorporates (pages 3-4). The order has
the respondent pay the petitioner $407 a month in spousal support from 8/1/2011, on the
1st of each month, after a 15-year marriage. It is **4 pages, portrait**, a scan.

| | |
|---|---|
| Publisher | Superior Court of California, County of San Luis Obispo (Self-Help Center) |
| Source | [slo.courts.ca.gov/…/disso-3-uncontested-judgment-sample.pdf](https://www.slo.courts.ca.gov/system/files/disso-3-uncontested-judgment-sample.pdf), pages 7-8 and 18-19 of 33 |
| Retrieved | 2026-10-03, by script |
| Clearance | Public |

The court's Self-Help Center links this packet as "Sample Forms": a complete
uncontested-judgment filing, filled in by the court with specimen parties (Pat Sample,
Sam Sample, their children Chad and Cindy Sample) and a placeholder address, so
self-represented litigants can see what a finished one looks like. Nothing in it is a
real person's data, and nothing was redacted. Only the judgment and the support order
are used; the rest of the packet is instructions and custody and property attachments.

In the source, these pages are 1-bit raster scans stored sideways, with `/Rotate 270` on
the page to turn them upright, and slightly skewed. To keep the committed sample free of
page rotation, each page was rendered upright at 300 dpi and placed as an image on a
fresh, unrotated letter-size page. The scan itself is unchanged, including its skew, and
the document metadata is empty. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

A support order sets who pays whom, how much and from when. Courts, agencies and
lenders all need those terms, and in California they arrive on the same Judicial Council
forms.

- **Mortgage and consumer lending:** underwriters read support orders to count alimony
  as a borrower's income, or as a debt the payor must keep paying.
- **Child and spousal support enforcement:** state agencies set up wage withholding and
  track payments against the ordered amount and start date.
- **Family law practices:** attorneys and paralegals review existing orders before a
  modification or enforcement filing.
- **Courts and self-help centers:** clerks check that the judgment and its attachments
  are complete and consistent before entry.
- **Tax preparation:** preparers check the order's date and terms when handling alimony
  paid or received.

### What it contains

- **Checkbox sentences.** Who pays whom, and whether support is spousal, family or
  partner support, are ticked boxes in one sentence that runs across three lines, with
  the amount, start date and payment day typed into blanks.
- **Two linked forms.** The FL-180 says spousal support is "as set forth in the
  attached" FL-343, and the FL-343 says it is attached to the FL-180.
- **The case number repeated** in the caption of each form.
- **An income table** with gross monthly and net disposable income for both parties,
  and mostly empty deduction columns.
- **Blank fields by design,** such as the end date of support.
- **1-bit skewed scans** with no usable text layer, so the text has to be read from the
  page image.
