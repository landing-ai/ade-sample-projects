# Disclosure Schedules

**On the website:** [landing.ai/document-type/disclosure-schedule](https://landing.ai/document-type/disclosure-schedule)

The Disclosure Schedules to the Asset Purchase Agreement between the four Finch
Therapeutics sellers and Ferring Asset Holding LLC, filed in the Finch Therapeutics
chapter 11 cases. It holds a cover page and preamble and a run of numbered schedules:
assigned agreements, patents, trademarks and software, excluded insurance policies and
causes of action, and the sellers' representations.

| | |
|---|---|
| Pages | 13 |
| Fields in the extraction schema | 57 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:50 | 2026-11-19 02:56 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 10,870 | 11,340 |
| Words under 0.95 confidence | 27 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 8.0 s | 32.0 s |
| Per page | 0.6 s | 2.5 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 3.1 credits | 9.4 credits |
| Per page | 0.24 credits | 0.72 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:50 | 2026-11-19 02:57 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 57 | 57 |
| Non-null fields returned | 57 | 57 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 246.5 s | 245.9 s |
| Per schema field (57) | 4.32 s | 4.31 s |
| Per value returned | 1.39 s | 1.39 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 11.5 credits | 11.5 credits |
| Per schema field (57) | 0.202 credits | 0.202 credits |
| Per value returned | 0.065 credits | 0.065 credits |

## Origin

`source/finch-ferring-apa-disclosure-schedules-redacted.pdf` is the Disclosure Schedules
(Execution Version) to the Asset Purchase Agreement between the four Finch Therapeutics
sellers and Ferring Asset Holding LLC, as filed in the Finch Therapeutics chapter 11
cases. It is **13 pages, portrait**, trimmed from a 66-page filing.

| | |
|---|---|
| Publisher | Omni Agent Solutions, the court-appointed claims agent, for the debtors in *In re Finch Therapeutics Group, Inc., et al.*, Case No. 26-10409 (LSS) (Bankr. D. Del.) |
| Source | [D.I. 296](https://casedocs.omniagentsolutions.com/cmsvol2/pub_47593/93712212-0d24-4754-86aa-56f478514c33_296.pdf), Notice of Filing of Schedules to Asset Purchase Agreement, filed July 24, 2026; case page [omniagentsolutions.com/FinchTherapeutics](https://omniagentsolutions.com/FinchTherapeutics) |
| Retrieved | 2026-10-28, by script |
| Clearance | **Redacted**: a public court filing, trimmed, with three individuals' names replaced |

| Page | Content |
|---|---|
| 1 | Cover page |
| 2 | Preamble (agreement, parties, interpretation) |
| 3 | Schedule 1.1(b) Assigned Agreements |
| 4–5 | Schedule 1.1(e) Intellectual Property: first page of the pending patent applications table; trademarks, domain names, software |
| 6 | Schedule 1.2(c) Excluded Insurance Policies |
| 7–8 | Schedules 1.2(f) Excluded Causes of Action, 1.2(m) Additional Excluded Assets |
| 9–13 | Schedules 4.1(a), (f), (g), (h), (i): seller jurisdictions, IP, litigation, no violation, assigned agreements |

**What was removed.** The filing's first two pages are the court notice, which carries
the debtors' attorneys' names, emails, bar numbers and an `/s/` signature; they were
dropped. Original pages 7–57 continue the Schedule 1.1(e) patent table, whose narrow
columns wrap words mid-token; they were dropped to keep the sample short, leaving the
table's first page (four complete rows). The court-stamped header still shows the
original page numbers (`Page N of 64`).

**What was replaced.** Schedule 1.1(b) names three individual contacts in its notice
addresses. Each was replaced with an obviously fake name: **Jane Sample** (an Attn line
in a University of Minnesota address), **John Sample** and **Alex Q. Sample** (in the
Skysong Innovations address); the job titles beside them were kept. The replacements
remove the original text rather than covering it, and are set in Helvetica, so they look
slightly different from the surrounding Times. Every other party (sellers, purchaser,
universities, insurers) is an organization and was kept, as were the debtors' partial
federal tax-ID digits, which are corporate. The PDF's metadata was cleared. Verified by
text search on the committed PDF and this folder: no original name survives. Full
provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Disclosure schedules sit alongside a purchase agreement and list the contracts, assets
and exceptions behind the seller's representations. They are where much of a deal's
detail lives.

- **M&A and corporate law firms:** lawyers draft, negotiate and review schedules
  against the representations in the agreement.
- **Buyers and due diligence teams:** they check which contracts, IP and liabilities
  transfer and which are excluded.
- **Bankruptcy courts, trustees and claims agents:** in a section 363 sale like this
  one, the schedules define what the buyer acquires from the estate.
- **Representations and warranties insurers:** underwriters review disclosed exceptions
  when pricing a policy for the deal.
- **Contract management and integration teams:** after closing, they take over the
  assigned agreements and their notice addresses.

### What it contains

- **Many short schedules,** each with its own number, heading and shape.
- **Tables** of assigned contracts with multi-address notice blocks, patents,
  trademarks and a 19-row insurance schedule.
- **Narrow table columns that wrap words mid-token** in the patent table.
- **Numbered lists and one-word schedules** that read only "None."
- **A court-stamped header** on every page carrying the original filing's page numbers.
- **A born-digital text layer,** with three replacement names set in a different font.
