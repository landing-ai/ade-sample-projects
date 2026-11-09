# LandingAI ADE Build Schema API — Specification

Source: https://docs.landing.ai/api-reference/tools/ade-build-extract-schema
        https://docs.landing.ai/ade/ade-extract-schema-api
Retrieved: 2026-04-05

---

## Overview

The Build Schema API generates a JSON extraction schema from parsed markdown content
and a text prompt. The schema it produces can be passed directly to the Extract API.

Use it to:
1. **Generate** a schema from scratch — provide markdowns and/or a prompt
2. **Refine** an existing schema — provide the schema + a prompt describing what to change

This is the API that replaces manual schema writing in the pipeline.

---

## Endpoint

```
POST /v1/ade/extract/build-schema
```

| Region | Base URL |
|---|---|
| US (default) | `https://api.va.landing.ai` |
| EU | `https://api.va.eu-west-1.landing.ai` |

**Authentication**: `Authorization: Bearer $VISION_AGENT_API_KEY`

**Content type**: Multipart form data (`-F` in curl, `files=` in Python requests)

---

## Request Parameters

At least one of `markdowns`, `markdown_urls`, or `prompt` must be provided.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `model` | string | No | Model version. Use `extract-latest` for the latest. |
| `markdowns` | file or string (repeatable) | No | One or more markdown files or inline strings. Provide multiple for better schema coverage across document layouts. |
| `markdown_urls` | array of strings | No | URLs to markdown files. |
| `prompt` | string | No | Instructions for how to generate or modify the schema. |
| `schema` | string | No | Existing JSON schema to refine. Pass as a JSON string. |

---

## Response

**200 OK**

```json
{
  "extraction_schema": "<JSON schema as a string>",
  "metadata": {
    "filename": "string",
    "org_id": "string",
    "duration_ms": 0,
    "credit_usage": 0,
    "job_id": "",
    "version": "string",
    "warnings": [
      {
        "code": "nonconformant_schema",
        "msg": "string"
      }
    ]
  }
}
```

Note: `extraction_schema` is a **string** — parse it with `json.loads()` before use.

---

## Workflows

### 1. Generate from markdowns (no prompt)

The API identifies all fields present in the document and builds a schema.

```bash
curl -X POST 'https://api.va.landing.ai/v1/ade/extract/build-schema' \
  -H 'Authorization: Bearer $VISION_AGENT_API_KEY' \
  -F 'markdowns=@data/pipeline_outputs/parsed/doc_markdown.md' \
  -F 'model=extract-latest'
```

### 2. Generate from multiple markdowns (better coverage)

Pass multiple documents representing the range of layouts you expect.

```bash
curl -X POST 'https://api.va.landing.ai/v1/ade/extract/build-schema' \
  -H 'Authorization: Bearer $VISION_AGENT_API_KEY' \
  -F 'markdowns=@doc1_markdown.md' \
  -F 'markdowns=@doc2_markdown.md' \
  -F 'model=extract-latest'
```

### 3. Generate from a prompt (no markdown needed)

Useful for specifying exact field names and types.

```bash
curl -X POST 'https://api.va.landing.ai/v1/ade/extract/build-schema' \
  -H 'Authorization: Bearer $VISION_AGENT_API_KEY' \
  -F 'model=extract-latest' \
  -F 'prompt=Extract patient_name (string), age (integer), rbc_count_value (number), rbc_count_unit (string)'
```

### 4. Generate from markdowns + prompt (recommended for initial build)

Combines document structure awareness with explicit field instructions.

```bash
curl -X POST 'https://api.va.landing.ai/v1/ade/extract/build-schema' \
  -H 'Authorization: Bearer $VISION_AGENT_API_KEY' \
  -F 'markdowns=@doc1_markdown.md' \
  -F 'markdowns=@doc2_markdown.md' \
  -F 'model=extract-latest' \
  -F 'prompt=Extract the following fields using these exact names: patient_name, age, test_date ...'
```

### 5. Refine an existing schema

Pass the current schema + instructions for what to change.

```bash
curl -X POST 'https://api.va.landing.ai/v1/ade/extract/build-schema' \
  -H 'Authorization: Bearer $VISION_AGENT_API_KEY' \
  -F 'markdowns=@doc1_markdown.md' \
  -F 'model=extract-latest' \
  -F 'schema={"type":"object","properties":{"age":{"type":"string"}}}' \
  -F 'prompt=Change the age field type from string to integer'
```

---

## Python Example (requests library)

```python
import requests, json, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["VISION_AGENT_API_KEY"]

# Refinement example
with open("data/pipeline_outputs/parsed/doc_markdown.md", "rb") as f:
    response = requests.post(
        "https://api.va.landing.ai/v1/ade/extract/build-schema",
        headers={"Authorization": f"Bearer {API_KEY}"},
        files=[
            ("markdowns", ("doc_markdown.md", f, "text/plain")),
            ("model",     (None, "extract-latest")),
            ("prompt",    (None, "Change age to integer type")),
            ("schema",    (None, json.dumps(existing_schema))),
        ],
    )

data = response.json()
new_schema = json.loads(data["extraction_schema"])  # note: parse the string
```

---

## Notes

- The `extraction_schema` response field is a **JSON string**, not an object — always use `json.loads()`.
- To send string fields as multipart (required), use `(None, value)` tuple syntax in Python requests.
- Strip any `_meta` internal block from your schema before sending it to the API.
- Check the `warnings` array — a `nonconformant_schema` warning means the API adjusted your schema to meet Extract API requirements.
- This API is not yet available in the `landingai-ade` Python library — use REST directly.
