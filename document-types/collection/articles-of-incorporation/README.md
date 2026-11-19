# Articles of Incorporation

**On the website:** [landing.ai/document-type/articles-of-incorporation](https://landing.ai/document-type/articles-of-incorporation)

Profit Corporation Articles of Incorporation for Top Tier Sports (USA) Inc., filed with
the Wyoming Secretary of State on November 5, 2024. It sets out the corporation's name,
registered agent, office addresses, authorized common and preferred shares with their
par values, and incorporator, and ends with the state's Certificate of Incorporation.

| | |
|---|---|
| Pages | 4 |
| Fields in the extraction schema | 24 |

Both models ran at standard tier through the jobs API, and both extractions used
`extract-20261111`.
Times are the processing time the API reports (`metadata.duration_ms`), not counting
time queued. Costs are the credits billed (`metadata.billing.total_credits`).

## Parse performance

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Snapshot | `dpt-3-verity-20261111` | `dpt-3-pro-20261111` |
| Output | [`runs/dpt-3-verity-20261111/`](runs/dpt-3-verity-20261111/) | [`runs/dpt-3-pro-20261111/`](runs/dpt-3-pro-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Parse accuracy

Word confidence is the `confidence` DPT-3 Verity reports on each word box.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Characters returned | 6,722 | 5,827 |
| Words under 0.95 confidence | 5 | n/a |
| Words under 0.80 confidence | 1 | n/a |
| Words under 0.50 confidence | 0 | n/a |
| Accuracy | To come | To come |

### Parse speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 15.8 s | 18.5 s |
| Per page | 4.0 s | 4.6 s |

### Parse cost

| | DPT-3 Verity | DPT-3 Pro |
|---|---|---|
| Total | 1.3 credits | 3.5 credits |
| Per page | 0.33 credits | 0.88 credits |

## Extract performance

Each model's markdown was extracted separately with the same schema. "Per value
returned" divides by every non-empty value extracted, so an array of six items counts
six.

| | Verity markdown | Pro markdown |
|---|---|---|
| Snapshot | `extract-20261111` | `extract-20261111` |
| Output | [`runs/dpt-3-verity-20261111/extract-20261111/`](runs/dpt-3-verity-20261111/extract-20261111/) | [`runs/dpt-3-pro-20261111/extract-20261111/`](runs/dpt-3-pro-20261111/extract-20261111/) |
| Processed (UTC) | 2026-11-19 02:26 | 2026-11-19 02:26 |
| Region | US | US |

### Extract accuracy

| | Verity markdown | Pro markdown |
|---|---|---|
| Fields requested | 24 | 24 |
| Non-null fields returned | 24 | 24 |
| Accuracy | To come | To come |

### Extract speed

Times are from a single run of each model. They vary from run to run with
server load, so treat small differences between models as noise.

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 254.8 s | 113.8 s |
| Per schema field (24) | 10.61 s | 4.74 s |
| Per value returned | 9.44 s | 4.22 s |

### Extract cost

| | Verity markdown | Pro markdown |
|---|---|---|
| Total | 2.5 credits | 2.3 credits |
| Per schema field (24) | 0.104 credits | 0.096 credits |
| Per value returned | 0.093 credits | 0.085 credits |

## Origin

`source/articles-of-incorporation-wyoming-top-tier-sports.pdf` is a set of **Profit
Corporation Articles of Incorporation** for Top Tier Sports (USA) Inc., generated and
filed by the **Wyoming Secretary of State** on November 5, 2024. It is **4 pages,
portrait**, a native PDF with a text layer:

1. The articles: the office-use filing stamp and Original ID, then Articles I to VI
   (name, registered agent, mailing and principal office addresses, authorized shares
   and par values, incorporator) and a typed e-signature block.
2. The filer's checkbox attestations, the statutory penalty notice, and the signature
   block again.
3. The registered agent's consent to appointment.
4. The Secretary of State's Certificate of Incorporation, with the Great Seal and the
   Secretary's signature.

| | |
|---|---|
| Publisher | Wyoming Secretary of State; filed on SEC EDGAR by Top Tier Sports (USA) Inc. as Exhibit D to its Form C |
| Source | [sec.gov/Archives/edgar/data/2045455/000204545524000001/exhibit_d.pdf](https://www.sec.gov/Archives/edgar/data/2045455/000204545524000001/exhibit_d.pdf) |
| Filing index | [0002045455-24-000001](https://www.sec.gov/Archives/edgar/data/2045455/000204545524000001/0002045455-24-000001-index.html) |
| Retrieved | 2026-10-28, downloaded directly by script |
| Clearance | Public |

The company filed these articles with the SEC as an exhibit to a Regulation
Crowdfunding offering statement, so the document sits in a public government
repository. EDGAR served it as a PDF.

The document is used as published, unredacted, by explicit decision of the operator. The
filing names one incorporator, an attorney at the registered-agent law firm acting in a
professional capacity, with a typed e-signature, a business email and a business phone
on pages 1 to 3. Page 4 names the Secretary of State, a public official, with his
signature and the state seal. The PDF metadata holds only the producing software (PDFium)
and a creation timestamp. Full provenance is in `manifest.json` under `source.origin`.

## Why this document

### Who processes it

Articles of incorporation are the founding record of a corporation. They prove that the
company exists, who its registered agent is, and what shares it may issue.

- **Banking and KYB onboarding:** banks and payment providers collect the articles to
  verify a business's legal name, formation date and registered address.
- **Commercial lending:** lenders confirm that the borrower is a validly formed
  corporation before they sign loan documents.
- **Investors and securities filings:** crowdfunding portals, venture investors and
  their counsel check the authorized share classes and par values, as in the SEC filing
  this copy comes from.
- **Corporate law and registered agent services:** firms file, track and reconcile
  formation documents across states.
- **Due diligence in M&A:** acquirers review the charter documents of each entity they
  buy.

### What it contains

- **Numbered articles** with labels and values mixed into a state-generated form.
- **Two-column label/value pairs.** Article V prints the share counts and par values side
  by side on two lines.
- **A non-numeric quantity.** Common shares are authorized as "Unlimited".
- **Repeated addresses.** The mailing and principal office addresses are identical, and
  the registered agent's address reappears on page 3 in running prose.
- **A page of checkbox attestations** and a statutory penalty notice.
- **Typed e-signatures, a handwritten signature and the state seal** on the certificate
  page.
