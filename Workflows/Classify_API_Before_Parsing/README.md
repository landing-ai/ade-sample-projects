# LandingAI ADE — Classify (API) Before Parsing

A demo pipeline that uses the [LandingAI Agentic Document Extraction (ADE)](https://docs.landing.ai/ade/ade-python)
Python SDK to **classify a mixed batch of documents first**, then **parse only
the document types you care about**.

Running the Classify API up front lets you triage a large packet cheaply and
spend the more expensive parse step only on documents "of interest".

- **Script:** [`ade_classify_before_parse_pipeline.py`](ade_classify_before_parse_pipeline.py)
- **Classes:** [`classes.json`](classes.json)
- **Demo documents:** [`loan_demo_documents/`](loan_demo_documents/)

---

## Watch the demo

<div align="center">
  <a href="https://youtu.be/oGJhA2Ydza4" target="_blank">
    <img src="https://img.youtube.com/vi/oGJhA2Ydza4/maxresdefault.jpg" alt="Watch the ADE Classify API demo" width="100%" style="max-width:600px;">
  </a>
</div>

---

## How it works

For each input file the pipeline:

1. **Classifies** (`client.classify`) the document into one of the categories
   defined in [`classes.json`](classes.json), reporting the page, predicted
   class, and reason.
2. **Filters** — if the predicted class is in the `PARSE_CLASSES` set, the
   document is parsed; otherwise it is skipped (still classified, just not
   parsed).
3. **Parses** (`client.parse`) the kept documents into clean **Markdown** plus
   structured **chunks** (with grounding/location data).

It processes a whole folder (or an explicit list of files), continues past any
single file that errors, and prints a summary of how many files were parsed vs.
skipped by the filter.

---

## The classes file

The classification categories live in [`classes.json`](classes.json) — a flat
JSON object of `{class_name: description}` — so you can edit the class set
without touching the script. The script loads it at runtime and passes it to
`client.classify`. For this demo the file describes the residential mortgage
document types (loan application, pay stub, W-2, bank statement, appraisal, etc.).

## The parse filter

The `PARSE_CLASSES` set in the script controls what gets parsed. Only documents
whose predicted class is in this set proceed to parse; everything else is
classified and skipped. The default keeps **income & employment** documents:

```python
PARSE_CLASSES = {
    "pay_stub",
    "w2",
    "tax_return",
    "employment_verification",
}
```

Edit this set to keep whatever document types you care about.

---

## The loan documents

The demo set (`loan_demo_documents/`) represents a full residential mortgage
file — the kinds of documents a lender collects and reviews for a loan:

| # | File | Document type |
|---|------|---------------|
| 01 | `01_loan_application_1003.pdf` | Uniform Residential Loan Application (Form 1003) |
| 02 | `02_loan_estimate.pdf` | Loan Estimate |
| 03 | `03_closing_disclosure.pdf` | Closing Disclosure |
| 04 | `04_government_id_drivers_license.pdf` | Government ID / driver's license |
| 05 | `05_pay_stub.pdf` | Pay stub |
| 06 | `06_w2_wage_statement.pdf` | W-2 wage statement |
| 07 | `07_tax_return_1040.pdf` | Tax return (Form 1040) |
| 08 | `08_employment_verification_letter.pdf` | Employment verification letter |
| 09 | `09_bank_statement.pdf` | Bank statement |
| 10 | `10_investment_account_statement.pdf` | Investment account statement |
| 11 | `11_gift_letter.pdf` | Gift letter |
| 12 | `12_credit_report.pdf` | Credit report |
| 13 | `13_purchase_agreement.pdf` | Purchase agreement |
| 14 | `14_property_appraisal.pdf` | Property appraisal |
| 15 | `15_title_report.pdf` | Title report |
| 16 | `16_homeowners_insurance_declaration.pdf` | Homeowners insurance declaration |
| 17 | `17_property_tax_statement.pdf` | Property tax statement |
| 18 | `18_mortgage_payoff_statement.pdf` | Mortgage payoff statement |
| 19 | `19_letter_of_explanation.pdf` | Letter of explanation (LOX) |

There is also `Loan_demo_documents_Merged.pdf` — all of the above combined into a
single multi-page PDF. Because it contains income pages, it matches the default
filter and is parsed; it's a good illustration of classification across a mixed
packet.

---

## Setup

```bash
pip install -r requirements.txt

# Authenticate — get an API key from your LandingAI account:
export VISION_AGENT_API_KEY=<your-api-key>
```

> **Note:** Do not hard-code real API keys in the script or commit them to
> source control. The `VISION_AGENT_API_KEY` environment variable is the
> recommended approach.

---

## Run the demo

```bash
python ade_classify_before_parse_pipeline.py
```

Expected console output (abbreviated) — everything is classified, but only the
income & employment documents are parsed:

```
Found 20 file(s) to process.
Parse filter (classes of interest): ['employment_verification', 'pay_stub', 'tax_return', 'w2']

=== 01_loan_application_1003.pdf ===
Step 1: Classifying...
  page 1: loan_application  (Contains Form 1003 borrower and loan sections)
Step 2: Skipping parse — class ['loan_application'] not in filter.

=== 05_pay_stub.pdf ===
Step 1: Classifying...
  page 1: pay_stub  (Shows gross/net pay, earnings, and deductions)
Step 2: Parsing (matched ['pay_stub'])...
  parsed 11 chunks
...
Done. Classified 20/20 file(s); parsed 5, skipped 15 by filter.
```

> The merged packet (`Loan_demo_documents_Merged.pdf`) also parses because it
> contains income pages — hence 5 parsed rather than 4.

Parsed Markdown/JSON for each kept document is written to `OUTPUT_DIR`
(`./ade_output`).

---

## Next steps / extensions

- **Extract** — add `client.extract(schema=..., markdown=...)` with a Pydantic
  schema to pull structured fields from the parsed documents.
- **Route by class** — send each class to a different downstream handler instead
  of a single keep/skip filter.
- **Concurrency** — for large batches, switch to `AsyncLandingAIADE` or ADE
  parse jobs to process files in parallel.
