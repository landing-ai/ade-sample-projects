# Instant Verification of User-Supplied Documents Demo — Landing AI

A split-screen Streamlit app that demonstrates real-time document verification using [Landing AI's Agentic Document Extraction (ADE)](https://landing.ai/agentic-document-extraction) API. Documents are parsed and key fields extracted automatically; business rules are applied instantly and results are streamed to the screen as they happen.

This demo verifies two common mortgage lending documents — a **W-2** and a **Paystub** — against borrower-supplied information.

---

## What It Does

The app has two panels side by side:

**Left — User experience**
1. Enter borrower name, SSN, and loan application date
2. Upload a W-2 (PDF) → system verifies name, SSN, and tax year
3. Upload a Paystub (PDF) → system verifies name, SSN, and that the pay date is within 30 days of the loan application date
4. View a summary screen with extracted fields and processing times

**Right — Processing view**
- Streams live timestamps as each step completes: upload → parse → extract → business rule checks
- Displays all extracted key-value pairs
- Shows a PASS / FAIL verdict per document with per-check detail

---

## Watch the Video

[![Alt text](https://img.youtube.com/vi/1xq2YuVIo-g/0.jpg)](https://www.youtube.com/watch?v=1xq2YuVIo-g)

---

## Prerequisites

- Python 3.9 or higher
- A Landing AI API key — get one at [va.landing.ai/settings/api-key](https://va.landing.ai/settings/api-key)

---

## Setup

```bash
# 1. Clone the repo and navigate to this directory
git clone <repo-url>
cd <repo-directory>

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
echo "VISION_AGENT_API_KEY=your_key_here" > .env
```

---

## Run

```bash
streamlit run app.py
```

The app opens automatically in your browser at `http://localhost:8501`.

---

## Business Rules

| Document | Field | Rule |
|---|---|---|
| W-2 | Employee name | Case-insensitive exact match against entered borrower name |
| W-2 | Employee SSN | Normalized match (ignores dashes/spaces) |
| W-2 | Tax year | Must be one of the two most recent calendar years |
| Paystub | Employee name | Case-insensitive exact match against entered borrower name |
| Paystub | Employee SSN | Normalized match (ignores dashes/spaces) |
| Paystub | Pay date | Must be within 30 days of the loan application date |

If a field cannot be extracted, the check is skipped and the document is flagged for manual review. All other checks must still pass for the document to be accepted.

---

## API Reference

This app calls two Landing AI ADE endpoints:

- **Parse** — converts a PDF to structured markdown: [`POST /v1/ade/parse`](https://docs.landing.ai/api-reference/tools/ade-parse)
- **Extract** — pulls key-value pairs from the parsed markdown using a JSON schema: [`POST /v1/ade/extract`](https://docs.landing.ai/api-reference/tools/ade-extract)
