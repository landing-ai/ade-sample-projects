# Prompts — build ADE projects by describing what you want

A library of **copy-paste, natural-language prompts** you can hand to an AI coding
agent (Claude Code, Cursor, etc.) to build document-processing scripts and apps on
LandingAI's **Agentic Document Extraction (ADE)** — Parse, Extract, Build Schema,
Classify, and the async Jobs APIs.

Instead of writing the integration yourself, you describe the pipeline in plain
English and the agent writes the code. Each `.md` file here is one such
instruction — the same kind of prompt used to produce several of the sample
projects in this repo (see [`Use_Cases/Invoices`](../Use_Cases/Invoices)).

## What's in here

| Prompt | Purpose | Builds |
|---|---|---|
| [`quickstart_with_parse_buildSchema_extract.md`](quickstart_with_parse_buildSchema_extract.md) | Learn the APIs | A minimal 3-call sequence (Parse → Build Schema → Extract) on a single document |
| [`batchToCsv_with_parse_buildSchema_extract.md`](batchToCsv_with_parse_buildSchema_extract.md) | Any documents → CSV | A batch script: Parse → Build Schema → Extract → one combined CSV (Python SDK) |
| [`invoice_with_parseJobs_extractJobs.md`](invoice_with_parseJobs_extractJobs.md) | Invoices | An async v2 pipeline: Parse Jobs → Extract Jobs → field / line-item / metadata CSV summaries |
| [`groundingViewerApp_with_parse_extract.md`](groundingViewerApp_with_parse_extract.md) | Visualize grounding | A full-stack app with a side-by-side doc + response viewer and hover-to-highlight grounding |

Copy the contents of any file into your agent, adjust the folder/file names to
match your project, and run.

## Give your agent ADE expertise first

These prompts assume the agent knows how ADE's APIs and SDK work. There are two
(complementary) ways to give it that knowledge — set up **either or both** before
running a prompt.

### 1. The ADE document-processing skill (Claude Code plugin)

A Claude Code plugin that teaches the agent ADE's parse/extract/classify/split
workflows, schemas, and best practices, and adds ready-to-use skills.

```
/plugin marketplace add landing-ai/ade-document-processing-skills
/plugin install ade-document-processing@ade-document-processing-skills
/reload-plugins
```

### 2. The `ade-docs` documentation MCP

An MCP server that lets the agent search the live ADE documentation and access
the ADE skills while it works.

```
claude mcp add --transport http ade-docs https://docs.landing.ai/mcp
```

> ### ⚠️ `ade-docs` is a **documentation** MCP — not a product/API MCP
>
> This is worth being explicit about. The `ade-docs` server connects the agent to
> **ADE's documentation and skills** so it writes *correct* code. It does **not**
> process your documents:
>
> - It does **not** call Parse, Extract, Classify, or any ADE endpoint on your behalf.
> - It does **not** upload, read, or return your files or extracted data.
> - It does **not** need or use your `VISION_AGENT_API_KEY`.
>
> The actual document processing is done by **the script the agent writes for
> you**, which calls the ADE APIs / Python SDK directly using *your*
> `VISION_AGENT_API_KEY`. Think of `ade-docs` as the reference manual the agent
> reads, not the machine that does the work.

## Prerequisites for the generated code

Whatever the agent builds will need:

- A LandingAI ADE API key in your environment — `export VISION_AGENT_API_KEY=<your-api-key>`
  (get one at <https://va.landing.ai/settings/api-key>). Keep it in a git-ignored
  `.env`; never commit real keys.
- The ADE Python SDK where a prompt asks for it — `pip install landingai-ade python-dotenv`.

## Tips for writing your own prompt

- **Name folders explicitly** (`input_folder`, `results_folder/parse`, …) so output
  lands where you expect.
- **State the API version and tier** — e.g. "use only v2 endpoints" or
  "Parse Jobs v2 with `standard` service_tier."
- **Say which interface you prefer** — Python SDK vs. direct REST calls.
- **Describe the output shape** — "one row per document," "avoid nested levels in
  the schema so it flattens to CSV."
- **Point the agent at the docs** — "Use the `ade-docs` MCP server for the v2 API
  details," as in the invoice sample below.

## Related

- [`Use_Cases/Invoices`](../Use_Cases/Invoices) — a full sample project produced from a prompt like these
- [ADE docs: Build with AI agents](https://docs.landing.ai/ade/build-with-ai-agents)
- [ADE Python SDK](https://docs.landing.ai/ade/ade-python)
