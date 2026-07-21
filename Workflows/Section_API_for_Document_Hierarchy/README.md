# Section API for Document Hierarchy

A Python implementation for turning a parsed document into a structured,
hierarchical table of contents using LandingAI's ADE (Agentic Document
Extraction) **Section** API.

## Overview

Parsing a document gives you clean markdown, but that markdown is still *flat* —
one long stream of headings, paragraphs, and tables with no explicit sense of
where one section ends and the next begins. The **Section** endpoint reads that
parsed markdown and reconstructs the document's logical hierarchy: chapters,
sections, sub-sections, and the parent/child relationships between them.

Because the Section model works from **reference anchors** (`<a id='...'></a>`)
that the parser embeds in the markdown, every entry in the returned table of
contents is pinned back to a precise location in the source document.

This example runs the full two-step flow on the sample `ibm_annual_report.pdf`:

1. **Parse** the PDF into markdown (with reference anchors).
2. **Section** that markdown into a hierarchical table of contents.

### Key Features

- 🌳 **Hierarchical Structure**: Reconstructs chapters → sections → sub-sections
- 🔗 **Anchored Entries**: Every TOC entry maps back to a location in the source
- 🧭 **Guidelines Support**: Steer the hierarchy in plain English (e.g. "Group by topic")
- 💾 **Dual Output**: Saves both a machine-readable JSON hierarchy and a human-readable TOC
- 🧩 **RAG-Ready**: Produces the section boundaries that make retrieval chunking accurate

## Prerequisites

- Python 3.7+
- LandingAI ADE API key ([Get your key here](https://docs.landing.ai/ade/agentic-api-key))

## Installation

1. From the repository root, move into this folder:
```bash
cd Workflows/Section_API_for_Document_Hierarchy
```

2. Install required dependencies:
```bash
pip install -U requests python-dotenv
```

3. Set up your API key:
   - Create a `.env` file in this directory
   - Add your API key:
```env
VISION_AGENT_API_KEY=your_api_key_here
```

## Usage

### Quick Start

Run the module directly to process the bundled sample PDF:
```bash
python section_api.py
```

This parses `input_folder/ibm_annual_report.pdf`, sections it, and writes the
results to `output_folder/`.

### Basic Workflow

```python
from section_api import process_document

results = process_document('input_folder/ibm_annual_report.pdf', API_KEY)

parsed_markdown = results['markdown']
sections = results['sections']            # full Section response
toc = sections['table_of_contents']       # list of hierarchy entries
```

### Steering the Hierarchy

Use natural-language `guidelines` to control how the document is divided:
```python
results = process_document(
    'input_folder/ibm_annual_report.pdf',
    API_KEY,
    guidelines="Group by topic and treat each numbered item as its own section",
)
```

### Step-by-Step Process

1. **Parse Document** (produces markdown with reference anchors):
```python
markdown = parse_document('input_folder/ibm_annual_report.pdf', API_KEY)
```

2. **Build the Hierarchy**:
```python
sections = section_markdown(markdown, API_KEY, guidelines="Group by topic")
```

3. **Save the Results**:
```python
save_results(sections, 'output_folder', 'ibm_annual_report')
```

## Project Structure

```
Section_API_for_Document_Hierarchy/
│
├── section_api.py               # Python module with all functions
├── input_folder/                # Sample input PDF files
│   └── ibm_annual_report.pdf    # Sample document to section
├── output_folder/               # Generated hierarchy outputs
│   ├── *_sections.json         # Full hierarchy (raw Section response)
│   └── *_toc.md                # Human-readable table of contents
└── README.md                    # This file
```

## API Reference

**Endpoint**: `POST /v1/ade/section`
([docs](https://docs.landing.ai/api-reference/tools/ade-section))

- **US Base URL**: `https://api.va.landing.ai`
- **EU Base URL**: `https://api.va.eu-west-1.landing.ai`
- **Auth**: `Authorization: Bearer YOUR_API_KEY`
- **Content-Type**: `multipart/form-data`

### Request Parameters

| Parameter     | Type   | Required | Description |
|---------------|--------|----------|-------------|
| `markdown`    | file   | No*      | Parsed markdown with reference anchors (`<a id='...'></a>`) from the parse response |
| `markdown_url`| string | No*      | URL to fetch the markdown from instead of uploading it |
| `guidelines`  | string | No       | Natural-language instructions to control the hierarchy (e.g. `"Group by topic"`) |
| `model`       | string | No       | Section model version; defaults to the latest |

\* Provide either `markdown` or `markdown_url`.

### Response Schema

| Field                   | Type   | Description |
|-------------------------|--------|-------------|
| `table_of_contents`     | array  | Entries with `title`, `level`, `section_number`, `start_reference` |
| `table_of_contents_md`  | string | Markdown-formatted table of contents |
| `metadata`              | object | `filename`, `org_id`, `duration_ms`, `credit_usage`, `job_id`, `version` |

## Key Functions

### `parse_document(file_path, api_key)`
Parses a document into markdown containing the reference anchors the Section
endpoint needs.

### `section_markdown(markdown, api_key, guidelines=None, model=None)`
Sends parsed markdown to `/v1/ade/section` and returns the hierarchical table of
contents.

### `save_results(result, output_dir, stem)`
Writes the Section response as both a JSON hierarchy and a markdown TOC.

### `process_document(file_path, api_key, ...)`
Complete end-to-end workflow: parse → section → save.

### `preview_toc(result, max_entries=25)`
Prints the table of contents with indentation by hierarchy level.

## Why Sectioning Improves RAG Performance

Retrieval-Augmented Generation lives and dies by **chunk quality**. If the
chunks you embed and retrieve are arbitrary, your retriever returns noise and
the LLM answers from noise. Sectioning fixes this at the source:

- **Semantically coherent chunks, not blind splits.** Naive RAG pipelines split
  on a fixed character/token count, which routinely cuts a table in half, orphans
  a heading from its body, or merges two unrelated topics into one chunk.
  Chunking on real section boundaries keeps each chunk about *one thing*, so its
  embedding is a clean signal and retrieval precision goes up.

- **Hierarchy-aware context.** Each chunk can carry its ancestor path
  (e.g. *"Part II › Risk Factors › Liquidity Risk"*). Injecting that breadcrumb
  into the chunk — or using it to filter — disambiguates otherwise similar text
  and lets the LLM answer with the right scope instead of blending sections.

- **Better recall on long documents.** In a 300-page filing, the same phrase can
  appear in a dozen places. Sections let you retrieve the *right* occurrence and
  expand to neighboring sibling/parent chunks, rather than returning a random
  fragment that happens to match keywords.

- **Precise citations and grounding.** Because every section is anchored back to
  a location in the source, retrieved answers can cite the exact section (and
  page) they came from — which is what makes RAG answers auditable and
  trustworthy.

- **Cheaper, faster retrieval.** Coherent, right-sized chunks mean you can send
  fewer, more relevant chunks to the model — lowering token cost and latency
  while *improving* answer quality.

In short: parsing gives the model clean text, and **sectioning gives it
structure**. Structure is what turns "search over a pile of text" into
"retrieval over a well-organized knowledge base" — the single biggest lever on
RAG accuracy. See the [`Parse_Multiple_Documents_for_RAG`](../Parse_Multiple_Documents_for_RAG)
and [`Retrieval_Augmented_Generation`](../Retrieval_Augmented_Generation) workflows
for how these chunks feed a full RAG pipeline.

## Resources

- [ADE Section API Reference](https://docs.landing.ai/api-reference/tools/ade-section)
- [LandingAI ADE Documentation](https://docs.landing.ai/ade)
- [API Key Management](https://va.landing.ai/settings/api-key)
- [Support & Issues](https://docs.landing.ai/support)

## License

This project is provided as an educational resource for working with the
LandingAI ADE Section API.
