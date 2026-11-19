# W-2 form

**On the website:** [landing.ai/document-type/w2-form](https://landing.ai/document-type/w2-form)

An example Form W-2, Copy A, for tax year 2024, filled with test data. It shows the
employee and employer, the wages and the federal, social security and Medicare tax
withheld in numbered boxes, the box 12 codes and amounts, the box 13 checkboxes, and
the state and local tax row along the bottom.

| | |
|---|---|
| Pages | 1 |
| Fields in the extraction schema | 33 |

DPT-3 Pro ran at standard tier through the jobs API, and the extraction used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Pro |
|---|---|
| Snapshot | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 03:59 |
| Region | US |

### Parse accuracy

| | DPT-3 Pro |
|---|---|
| Characters returned | 2,353 |
| Accuracy | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Pro |
|---|---|
| Total | 10.5 s |
| Per page | 10.5 s |

### Parse cost

| | DPT-3 Pro |
|---|---|
| Total | 1.1 credits |
| Per page | 1.10 credits |

## Extract performance

The Pro markdown was extracted with the schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Pro markdown |
|---|---|
| Snapshot | `extract-20261111` |
| Output | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 04:00 |
| Region | US |

### Extract accuracy

| | Pro markdown |
|---|---|
| Fields requested | 33 |
| Non-null fields returned | 31 |
| Accuracy | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Pro markdown |
|---|---|
| Total | 45.3 s |
| Per schema field (33) | 1.37 s |
| Per value returned | 1.13 s |

### Extract cost

| | Pro markdown |
|---|---|
| Total | 1.6 credits |
| Per schema field (33) | 0.048 credits |
| Per value returned | 0.040 credits |

## Origin

`source/w2-form-2048x1388.jpg` is an example **Form W-2** for tax year 2024, Copy A,
filled with test data. It is **1 page, a 2048×1388 landscape JPEG**: a digital image of
the IRS form, not a scan or photo, with no text layer.

| | |
|---|---|
| Publisher | Remote People (blog) |
| Source | [remotepeople.com/…/w2-form-2048x1388.avif](https://remotepeople.com/wp-content/uploads/2025/01/w2-form-2048x1388.avif) |
| Retrieved | 2026-09-27 |
| Clearance | Public |

The Marketing Document Summary sheet lists this as the W-2 source. The form layout is
the IRS's, and every value is obvious test data: employee "John Doe", employer "Company
Inc", an employee SSN of "4453453" and an EIN of "23454535" (7 and 8 digits, neither a
valid format), and a locality named "Test".

Two caveats about clearance:

- **A blog is not a specimen publisher.** Remote People made this image to illustrate a
  post. It is not a payroll vendor or the IRS distributing a sample for reuse, which is
  the stronger kind of public source. An IRS or payroll-vendor specimen would replace it
  cleanly.
- **The addresses use real road names.** Both have arbitrary house numbers. The
  employee's pairs a North Carolina road with a California ZIP, so it is not a coherent
  real address. The employer's Saratoga address could not be ruled out as matching a
  real building, and it was not redacted.

The source URL ends in `.avif`, but the server returns a JPEG, so the file is saved as
`.jpg` and needed no conversion. Full provenance is in `manifest.json` under
`source.origin`.

## Why this document

### Who processes it

Every US employer issues a W-2 to each employee every year, so it is the most common
proof of wage income in the country.

- **Mortgage and consumer lending:** lenders verify income from the last two years of
  W-2s.
- **Tax preparation:** preparers and tax software copy the boxes onto the individual
  return.
- **Payroll providers and employers:** they produce W-2s and reconcile them against
  quarterly payroll filings.
- **Tenant screening and background checks:** landlords and agencies use W-2s to
  confirm stated income.
- **Financial aid and benefits:** colleges and agencies use W-2s to verify household
  income for aid and eligibility.

### What it contains

- **An image with no text layer,** so every value is read from pixels.
- **A dense boxed form** of thirty-odd numbered boxes, each with a printed label and a
  value, in red ink.
- **Box 12 letter codes** beside a tiny vertical "Code" label, each paired with an
  amount.
- **Checkboxes** in box 13.
- **A free-text write-in** in box 14.
- **A state and local tax row** along the bottom of the form.
- **Blank boxes** that should come back empty.
