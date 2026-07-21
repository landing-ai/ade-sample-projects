# LandingAI ADE — Loan Document Classify & Parse Demo

A demo pipeline that uses the [LandingAI Agentic Document Extraction (ADE)](https://docs.landing.ai/ade/ade-python)
Python SDK to **classify** and **parse** a set of mortgage/loan documents.

- **Script:** [`ade_classify_parse_pipeline.py`](ade_classify_parse_pipeline.py)
- **Demo documents:** [`loan_demo_documents/`](loan_demo_documents/)

---

## What the script does

For each input file, the pipeline runs two ADE operations:

1. **Classify** (`client.classify`) — assigns the document to one of your defined
   categories (e.g. `pay_stub`, `bank_statement`) with a page number and a
   reason for the decision.
2. **Parse** (`client.parse`) — converts the document into clean **Markdown**
   plus structured **chunks** (with grounding/location data), suitable for
   downstream extraction, search, or routing.

It supports **batch processing** — point it at a whole folder or an explicit
list of files, and it loops over every document, continuing past any single
file that errors and printing a summary at the end.

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
single multi-page PDF. This is useful for demonstrating classification across a
mixed packet (and, optionally, the SDK's `split()` operation to break a merged
packet back into its component documents).

---

## Setup

```bash
pip install landingai-ade python-dotenv

# Authenticate — get an API key from your LandingAI account:
export VISION_AGENT_API_KEY=<your-api-key>
```

> **Note:** Do not hard-code real API keys in the script or commit them to
> source control. The `VISION_AGENT_API_KEY` environment variable is the
> recommended approach.

---

## Configure

Open [`ade_classify_parse_pipeline.py`](ade_classify_parse_pipeline.py) and set,
in the CONFIG section:

1. **Input** — either:
   - **Option A (folder):** set `INPUT_DIR` to the demo folder, e.g.
     ```python
     INPUT_DIR = Path("loan_demo_documents")
     ```
   - **Option B (explicit list):** fill `DOCUMENT_PATHS` with specific files.
2. **Classes** — the `CLASSES` dict defines the categories `classify()` chooses
   from. For this demo, describe the loan document types above (see the snippet
   below).
3. **Output** — `OUTPUT_DIR` (default `./ade_output`) is where parse JSON is saved.

Suggested `CLASSES` for the loan set:

```python
CLASSES = json.dumps({
    "loan_application":        "Uniform Residential Loan Application, Form 1003",
    "loan_estimate":           "Lender's estimate of loan terms and closing costs",
    "closing_disclosure":      "Final loan terms and closing costs before signing",
    "government_id":           "Driver's license or other government-issued photo ID",
    "pay_stub":                "Employee pay stub showing wages and deductions",
    "w2":                      "W-2 annual wage and tax statement",
    "tax_return":              "IRS Form 1040 individual income tax return",
    "employment_verification": "Letter verifying employment and income",
    "bank_statement":          "Bank account statement showing balances and transactions",
    "investment_statement":    "Brokerage or investment account statement",
    "gift_letter":             "Letter documenting a monetary gift for the down payment",
    "credit_report":           "Consumer credit report with scores and tradelines",
    "purchase_agreement":      "Real estate purchase and sale contract",
    "appraisal":               "Property appraisal report with valuation",
    "title_report":            "Title search / report on the property",
    "insurance_declaration":   "Homeowners insurance declaration page",
    "property_tax":            "Property tax statement or bill",
    "mortgage_payoff":         "Payoff statement for an existing mortgage",
    "letter_of_explanation":   "Borrower's written explanation of an item in the file",
})
```

---

## Run the demo

```bash
python ade_classify_parse_pipeline.py
```

Expected console output (abbreviated):

```
Found 19 file(s) to process.

=== 01_loan_application_1003.pdf ===
Step 1: Classifying...
  page 1: loan_application  (Contains Form 1003 borrower and loan sections)
Step 2: Parsing...
  parsed 42 chunks

=== 05_pay_stub.pdf ===
Step 1: Classifying...
  page 1: pay_stub  (Shows gross/net pay, earnings, and deductions)
Step 2: Parsing...
  parsed 11 chunks
...
Done. Processed 19/19 file(s) successfully.
```

Parsed Markdown/JSON for each document is written to `OUTPUT_DIR` (`./ade_output`).

### Try the merged packet

Point the script at `Loan_demo_documents_Merged.pdf` (via `DOCUMENT_PATHS`) to
see classification run across a single multi-document PDF — a good illustration
of sorting a mixed loan packet.

---

## Next steps / extensions

- **Extract** — add `client.extract(schema=..., markdown=...)` with a Pydantic
  schema to pull structured fields (borrower name, loan amount, income, etc.).
- **Split** — use `client.split(...)` on the merged PDF to separate a packet
  into its component documents automatically.
- **Concurrency** — for large batches, switch to `AsyncLandingAIADE` or ADE
  parse jobs to process files in parallel.
