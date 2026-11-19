# IRS CP 575

**On the website:** [landing.ai/document-type/irs-cp-575](https://landing.ai/document-type/irs-cp-575)

A specimen CP 575 A notice, the letter the IRS sends when it assigns an Employer
Identification Number, with placeholder values throughout. It gives the new EIN, the
business's legal name, address and name control, and the forms the business must file,
with reminders on page 2 and a tear-off stub on page 3. The publisher marked it up as a
credentialing example.

| | |
|---|---|
| Pages | 3 |
| Fields in the extraction schema | 13 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:11 | 2026-11-19 03:23 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 6,169 | 6,272 |
| Words under 0.95 confidence | 22 | n/a |
| Words under 0.80 confidence | 9 | n/a |
| Words under 0.50 confidence | 3 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.5 s | 10.3 s |
| Per page | 1.2 s | 3.4 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.1 credits | 3.1 credits |
| Per page | 0.37 credits | 1.03 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 03:11 | 2026-11-19 03:24 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 13 | 13 |
| Non-null fields returned | 13 | 13 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 289.3 s | 257.2 s |
| Per schema field (13) | 22.25 s | 19.78 s |
| Per value returned | 22.25 s | 19.78 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 1.7 credits | 1.8 credits |
| Per schema field (13) | 0.131 credits | 0.138 credits |
| Per value returned | 0.131 credits | 0.138 credits |

## Origin

`source/irs-cp-575-sample.pdf` is a specimen CP 575 A notice, the letter the IRS sends
when it assigns an Employer Identification Number. It is **3 pages, US Letter portrait
(612×792)**, with a full text layer: the letter on page 1, reminders on page 2, and a
mostly blank page 3 ending in the tear-off stub.

| | |
|---|---|
| Publisher | MetroPlusHealth |
| Source | [metroplus.org/…/Sample-IRS-Letter.pdf](https://metroplus.org/wp-content/uploads/2024/09/Sample-IRS-Letter.pdf) |
| Retrieved | 2026-10-03, downloaded by script |
| Clearance | Public |

MetroPlusHealth publishes it on its provider forms page as a credentialing example, to
show providers which IRS letter to submit. Every value is placeholder data: EIN
88-8888888, the entity "ABC Behavioral LCSW PC" at "123 OLD Road TPKE, ANY VALLEY, NY
10111", name control ABCD, an IRS-use reference of 9999999999, and dates in the year
2525. No real person's or business's data appears, so nothing was redacted. The PDF
metadata names only "IRS" as author, and the file is committed exactly as downloaded.

**The publisher marked it up.** A red "EXAMPLE ONLY" header, two yellow callout boxes
("Name must match contracted entity and the W9", "EIN must match W9") with arrows, and
yellow highlights over the name and EIN. They are in the text layer.

**The dates are deliberately invalid.** Page 1 dates the notice 01-35-2525; the stub on
page 3 and the IRS-use line on pages 2 and 3 print 01-25-2525. Full provenance is in
`manifest.json` under `source.origin`.

## Why this document

### Who processes it

The CP 575 is the IRS's proof that a business owns its EIN, so organizations that pay,
contract with or bank a business ask for a copy.

- **Healthcare payers and provider credentialing:** health plans, like the publisher
  here, check that the provider's legal name and EIN match the contract and the W-9.
- **Banking and payments:** know-your-business checks use the notice to confirm a new
  entity's EIN when an account is opened.
- **Lending:** SBA and commercial lenders ask for it to verify the borrower's tax ID.
- **Vendor onboarding and accounts payable:** buyers confirm the EIN before issuing
  payments and 1099s.
- **Accounting and payroll providers:** they set up new clients' tax accounts from it.

### What it contains

- **Prose with no tables.** Key values sit in sentences, such as the required filing and
  its due date, and the name control in a page 2 sentence.
- **A header block** of `label: value` lines.
- **Third-party markup over an official form:** a red header, yellow callout boxes with
  arrows, and highlights over the name and EIN.
- **Identifiers that repeat** across the header, the body, the IRS-use line and the
  stub.
- **A tear-off stub** that repeats the name and address at the bottom of page 3.
- **Inconsistent dates,** with an invalid notice date on page 1 and a different date on
  later pages.
