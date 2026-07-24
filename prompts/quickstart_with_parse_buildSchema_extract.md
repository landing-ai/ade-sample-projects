# Prompt — minimal Parse → Build Schema → Extract sequence (single doc)

The smallest useful ADE flow: three chained calls on one document — parse it to
Markdown, build a schema for it, then extract against that schema. A good first
step to learn the APIs before scaling to a batch.

Copy the prompt below. Have a `sample.pdf` and a `.env` (with your endpoint and
`VISION_AGENT_API_KEY`) in the working directory.

---

Use the ADE document processing skill — we will call some APIs. Use the endpoint and API key from the `.env` file. Make a sequence of 3 calls:

1. Call **parse** with `sample.pdf` to get the markdown.
2. Call **build-schema** to build a schema for the doc.
3. Call **extract** with the markdown and the schema from the previous steps.

At the end, show me a sample response from each call.

---

**Notes**
- The ADE document processing skill gives the agent the API details, schemas, and
  best practices it needs to make these calls (see the setup in
  [`README.md`](README.md)). The `ade-docs` MCP is an alternative source of the
  same reference material.
- Feeding the markdown from step 1 and the schema from step 2 into step 3 is the
  core pattern behind every larger pipeline in this folder.
- Once this works on one file, scale it to a folder with
  [`batchToCsv_with_parse_buildSchema_extract.md`](batchToCsv_with_parse_buildSchema_extract.md).
