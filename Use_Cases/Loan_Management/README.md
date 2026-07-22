# LandingAI ADE — Loan Management (Classify → Parse → Extract)

An end-to-end use case built on the [LandingAI Agentic Document Extraction (ADE)](https://docs.landing.ai/ade/ade-python)
Python SDK. Given a residential mortgage file, it **classifies** every document,
**parses** only the document types you care about, and **extracts** structured
income & employment fields from them.

Classifying up front lets you triage a large, mixed packet cheaply and spend the
more expensive Parse + Extract steps only on the documents of interest.

- **Script:** [`ade_loan_management_pipeline.py`](ade_loan_management_pipeline.py)
- **Classes:** [`classes.json`](classes.json)
- **Extraction schema:** [`extract_schema.json`](extract_schema.json)
- **Demo documents:** [`loan_demo_documents/`](loan_demo_documents/)

---

## Pipeline

For each input file:

1. **Classify** (`client.classify`) into one of the categories defined in
   [`classes.json`](classes.json), reporting page, predicted class, and reason.
2. **Filter** — if the predicted class is in `PARSE_CLASSES`, continue; otherwise
   the document is classified and skipped.
3. **Parse** (`client.parse`) the kept documents into Markdown + chunks.
4. **Extract** (`client.extract`) structured fields from the parsed Markdown
   using the JSON schema in [`extract_schema.json`](extract_schema.json).

The pipeline processes a whole folder (or an explicit file list), continues past
any single file that errors, and writes results to `results_folder/`.

---

## The classes file

[`classes.json`](classes.json) is a flat `{class_name: description}` object
describing the residential mortgage document types (loan application, pay stub,
W-2, bank statement, appraisal, etc.). It is loaded at runtime and passed to
`client.classify`, so the class set can be edited without touching the script.

## The parse/extract filter

The `PARSE_CLASSES` set in the script controls what proceeds past classification.
Only documents whose predicted class is in this set are parsed and extracted. The
default keeps **income & employment** documents:

```python
PARSE_CLASSES = {
    "pay_stub",
    "w2",
    "tax_return",
    "employment_verification",
}
```

## The extraction schema

[`extract_schema.json`](extract_schema.json) is a standard **JSON Schema**
(`{"type": "object", "properties": {...}}`) passed directly to `client.extract`
— no Pydantic model required. It targets a comprehensive set of income &
employment fields; any field not present in a given document comes back null:

| Field | Type | Notes |
|---|---|---|
| `document_type` | string | Pay stub / W-2 / tax return / employment letter |
| `employee_name` | string | Employee / borrower |
| `employer_name` | string | Issuing employer |
| `employer_address` | string | Employer mailing address |
| `mailing_address` | string | Employee mailing/home address |
| `job_title` | string | Position / title |
| `employment_status` | string | full-time, part-time, contractor, active, … |
| `employment_start_date` | string | YYYY-MM-DD if available |
| `pay_period_start` / `pay_period_end` | string | Pay stub period |
| `pay_date` | string | Date wages were paid |
| `gross_pay_current` | number | Current-period gross |
| `net_pay_current` | number | Current-period net |
| `gross_pay_ytd` | number | Year-to-date gross |
| `total_deductions` | number | Current-period deductions |
| `annual_wages_w2` | number | W-2 Box 1 |
| `tax_year` | integer | e.g. 2025 |

Edit the schema to add, remove, or re-describe fields.

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
filter and is parsed & extracted.

> **Note:** the demo documents are synthetic samples — no real customer data.

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

## Run

```bash
python ade_loan_management_pipeline.py
```

Expected console output (abbreviated) — everything is classified, but only the
income & employment documents are parsed and extracted:

```
Found 20 file(s) to process.
Parse/extract filter (classes of interest): ['employment_verification', 'pay_stub', 'tax_return', 'w2']

=== 01_loan_application_1003.pdf ===
Step 1: Classifying...
  page 1: loan_application  (Contains Form 1003 borrower and loan sections)
Step 2: Skipping parse/extract — class ['loan_application'] not in filter.

=== 05_pay_stub.pdf ===
Step 1: Classifying...
  page 1: pay_stub  (Shows gross/net pay, earnings, and deductions)
Step 2: Parsing (matched ['pay_stub'])...
  parsed 11 chunks
Step 3: Extracting...
  extracted 9 field(s): ['employee_name', 'employer_name', 'gross_pay_current', ...]
...
Done. Classified 20/20 file(s); extracted 5, skipped 15 by filter.
Results written to results_folder/ (parse_*.json, extract_*.json, extractions.json).
```

## Output

Everything lands in `results_folder/` (gitignored):

- `parse_<name>.json` — full Parse response per document.
- `extract_<name>.json` — full Extract response per document.
- `extractions.json` — combined list, one entry of extracted fields per document.

---

## Next steps / extensions

- **Per-class schemas** — apply a different `extract_schema.json` per predicted
  class instead of one shared schema.
- **Validation** — cross-check extracted income across pay stub, W-2, and tax
  return for consistency.
- **Concurrency** — for large batches, switch to `AsyncLandingAIADE` or ADE
  parse/extract jobs to process files in parallel.
