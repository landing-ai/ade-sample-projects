# Bankruptcy Discharge

**On the website:** [landing.ai/document-type/bankruptcy-discharge](https://landing.ai/document-type/bankruptcy-discharge)

A US Bankruptcy Court order in a Chapter 7 case from the District of South Carolina. One
order discharges the debtor, discharges the trustee and closes the case. It names the
court, the case and the debtor, carries the judge's signature, and ends with the
standard explanation of which debts a Chapter 7 discharge does not cover.

| | |
|---|---|
| Pages | 2 |
| Fields in the extraction schema | 22 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:35 | 2026-11-19 02:32 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 4,572 | 4,729 |
| Words under 0.95 confidence | 9 | n/a |
| Words under 0.80 confidence | 4 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 5.0 s | 13.0 s |
| Per page | 2.5 s | 6.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 0.8 credits | 2.2 credits |
| Per page | 0.40 credits | 1.10 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:35 | 2026-11-19 02:33 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 22 | 22 |
| Non-null fields returned | 22 | 22 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 767.9 s | 82.5 s |
| Per schema field (22) | 34.90 s | 3.75 s |
| Per value returned | 22.58 s | 2.36 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.7 credits | 2.7 credits |
| Per schema field (22) | 0.123 credits | 0.123 credits |
| Per value returned | 0.079 credits | 0.077 credits |

## Origin

`source/bankruptcy-discharge.pdf` is a US Bankruptcy Court order in a Chapter 7 case
from the District of South Carolina: court form 166BNC, issued through the court's
electronic filing system and signed by the bankruptcy judge. It discharges the debtor,
discharges the trustee and closes the case. It is **2 pages, portrait (595×792)**. Page
1 is the order. Page 2 is the standard back page, "Explanation of Bankruptcy Discharge
in a Chapter 7 Case", which is generic text with no personal data apart from the case
number in the filing header.

| | |
|---|---|
| Publisher | United States Bankruptcy Court, District of South Carolina (a court record, posted to Scribd by a third party) |
| Source | scribd.com/document/489929789/Discharging-Debtor-7-Trustee-Closing-Case-Auto-Part-1 (the website shows this URL as plain text, not as a link) |
| Retrieved | 2026-10-03, downloaded manually |
| Clearance | Redacted |

Scribd blocks scripted requests, so the operator downloaded the file by hand. Scribd is
a user-upload site, not a publisher, so this order is treated as a private person's
record. The court is kept. The debtor is replaced.

| What | Replaced with | Occurrences |
|---|---|---|
| Debtor's name | Jane Q Sample | 1 |
| Other names used by the debtor (aka and fka) | Jane Sample, John Q Sample | 2 |
| Debtor's street address | 100 Main St | 1 |
| Debtor's city and ZIP code (state kept) | Anytown, SC 29000 | 1 |
| Last four digits of the SSN | xxx-xx-4321 | 1 |
| Case number | 09-30789-dd | 3 |
| Judge's handwritten signature | a stand-in signature in Indie Flower | 1 |

The case number is printed twice on page 1, in the body and in the electronic case
filing (ECF) header line, and once more in page 2's header. All three places use **one
stand-in** from `plausible.py`. The year prefix and the judge-initials suffix are kept.
Text was replaced with `document-types/scripts/redact.py`, which removes the underlying
text rather than covering it, and the PDF metadata was cleared.

**Two differences from the original can be seen on the page:**

- **The judge's signature was an inline image** in the page's content stream, which
  redact.py cannot reach. The inline-image block was cut out of the content stream
  directly and checked to be gone. A stand-in signature, "J Q Sample", was drawn in its
  place in Indie Flower, an openly licensed (SIL OFL) handwriting font. The order still
  shows that it was signed. No judge's name is printed on the order, so no name was kept
  or replaced.
- **Minus signs became hyphens in the body.** The body sets the dashes in the case
  number and in the masked SSN as U+2212 minus signs. The replacement font (Helvetica)
  cannot draw that character, so the stand-ins use ASCII hyphens, as the ECF header
  already did. Every other minus sign on the page is unchanged.

Kept as printed: the court and its address, the clerk of court's printed name (official
capacity), the dates, the docket number and the ECF timestamp. No original value can be
extracted from the committed PDF, checked both as literal strings and as bare digits,
and no original value appears anywhere in this folder. The rules file stays outside the
repo. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

A discharge order is the court's proof that a debtor's personal liability for most debts
has ended, and the date and chapter on it decide how a creditor treats those debts.

- **Mortgage and consumer lending:** underwriters check the chapter and the discharge
  date against waiting periods before approving a new loan.
- **Loan servicing and collections:** servicers stop collection on discharged debts and
  update account status.
- **Credit reporting:** bureaus and furnishers mark accounts as included in bankruptcy.
- **Bankruptcy and consumer law practices:** attorneys keep the order as the record that
  the case closed with a discharge.
- **Trustees and court-record services:** they track case status, trustee discharge and
  case closing across many filings.

### What it contains

- **A filing header in small type** with the case number, docket number and ECF
  timestamp.
- **A heading block with three stacked order titles** and bordered "Entered" and "Filed"
  stamps.
- **Numbered ordering paragraphs** that discharge the debtor, discharge the trustee and
  close the case.
- **A debtor block** that lists other names used ("aka", "fka") on one line.
- **A signature** (here, a stand-in in a handwriting font).
- **A lettered list** on the back page of the debts that are not discharged, with some
  items wrapping onto a second line.
