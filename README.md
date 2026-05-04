# ADE Sample Projects

Sample workflows, schemas, documents, and integrations for [LandingAI's Agentic Document Extraction (ADE)](https://landing.ai/agentic-document-extraction) — a service that parses and extracts structured data from any document, with no templates required.

Try the visual playground: [va.landing.ai/](https://va.landing.ai/)

---

## What's in this repo

Each subdirectory is a standalone sample project. They are organized into four categories:

| Category | What you'll find |
|---|---|
| **Workflows** | Reusable integration patterns — quickstart, RAG, serverless, Snowflake, word-level grounding |
| **Use Cases** | Domain-specific extraction demos — invoices, food labels, utility bills, certificates |
| **Events** | Demos and tutorials built for specific conferences and courses |
| **Other** | Standalone utilities, such as the SEC EDGAR pipeline |

---

## Getting started

All ADE samples need a LandingAI API key. Get one at [va.landing.ai/settings/api-key](https://va.landing.ai/settings/api-key).

Set it as an environment variable or in a `.env` file in the project directory:

```bash
export VISION_AGENT_API_KEY=your_api_key_here
```

Most projects use the `landingai-ade` Python library:

```bash
pip install landingai-ade
```

Each project has its own README with setup and usage instructions.

---

## Workflows

### [Parse + Extract Python Quickstart](Workflows/Parse_Extract_Python_QUICKSTART/)
The minimal starting point. Follows the [ADE Quickstart Guide](https://docs.landing.ai/ade/ade-quickstart): parse a document, then extract structured fields using a Pydantic schema.

### [Parse, Classify, Extract, and Visualize](Workflows/Parse_Classify_Extract_Visualize/)
Handles mixed document types in a single batch. Automatically classifies each document (e.g., pay stub, bank statement, investment statement), then applies the correct extraction schema. Includes bounding-box visualizations for every extracted field.

### [Parse Multiple Documents for RAG](Workflows/Parse_Multiple_Documents_for_RAG/)
Async batch parser that processes many documents concurrently and writes chunks with bounding-box coordinates to CSV — ready to load into a vector database like ChromaDB.

### [Parse Jobs API for Large Files](Workflows/Parse_Jobs_API_for_Large_Files/)
Asynchronous job submission for large PDFs (up to 1 GB / 1,000 pages) that exceed the standard synchronous API limits. Includes polling, progress tracking, and automatic handling of inline vs. URL-based results.

### [Serverless Document Processing with Lambda + S3](Workflows/Serverless_Document_Processing_ADE_Lambda_S3/)
Deploys ADE as a Docker-based AWS Lambda function triggered by S3 uploads. Supports both parse-only and structured extraction modes. Includes `build.sh` and `deploy.sh` scripts.

### [ADE Lambda S3](Workflows/ADE_Lambda_S3/)
Deploys ADE as a serverless Docker-based Lambda function to automatically process documents from S3 buckets at scale. Supports parse and structured extraction modes with batch processing, auto-triggers on S3 uploads, and customizable Pydantic schemas.

### [Snowflake Intelligence Agent End-to-End](Workflows/Snowflake_Intelligence_Agent_End_to_End/)
Full Snowflake-native pipeline: upload documents to a Snowflake stage, apply ADE to parse and extract, enable RAG with Cortex Search, query structured fields with Cortex Analyst, and surface everything through a Cortex Agent. Uses FDA medical device documents as the example.

### [Document Intelligence in Snowflake](Workflows/Snowflake/Document_Intelligence_in_Snowflake/)
Transforms unstructured FDA documents into AI-ready assets inside Snowflake using ADE and Snowflake Cortex. Covers parse, structured extraction, Cortex Search for RAG, Cortex Analyst for text-to-SQL, PubMed Knowledge Extension enrichment, and a Cortex Agent with Snowflake Intelligence UI.

### [High Volume ADE with Snowflake Insertion](Workflows/Snowflake/High_Volume_ADE_with_Snowflake_Insertion/)
End-to-end pipeline that parses documents with ADE and inserts structured rows into Snowflake tables. Uses invoices as the example, but the pattern — Pydantic schema, row builder, buffered uploader — is modular and adapts to any document type.

### [ADE LLM Retrieval](Workflows/ADE_LLM_Retrieval/)
Integrates ADE with OpenAI LLMs for intelligent document processing: parse with visual grounding, extract fields via GPT, build a FAISS-backed RAG pipeline with LangChain, and evaluate answer quality with automated LLM grading.

### [Retrieval-Augmented Generation](Workflows/Retrieval_Augmented_Generation/)
Two complementary RAG samples:
- **[ADE Local RAG with OpenAI + ChromaDB](Workflows/Retrieval_Augmented_Generation/ADE_Local_RAG_OpenAI_ChromaDB/)** — Parses SEC 10-K filings with ADE, stores chunks with OpenAI embeddings in a local Chroma vector database, and enables semantic search with grounding crops.
- **[Chunking for RAG Applications](Workflows/Retrieval_Augmented_Generation/Chunking_for_RAG_Applications/)** — Async batch parser that processes documents in parallel and writes chunks with bounding-box coordinates to CSV, ready to load into any vector database.

### [Word-Level Grounding](Workflows/Word-Level_Grounding/)
Goes beyond chunk-level grounding to pinpoint the exact words in a document that correspond to extracted field values. Uses Tesseract OCR and fuzzy matching to highlight matched words with confidence-scored color coding — useful for audit trails, compliance, and explainable AI.

---

## Use Cases

### [Food Labels](Use_Cases/Food_Labels/)
Extracts 27 structured fields from food label images — product name, brand, weight, serving size, certifications (organic, non-GMO, kosher), and dietary claims. Demonstrates parse-once, extract-multiple-times for different schemas.

### [Invoices](Use_Cases/Invoices/)
Extracts header fields and line items from invoices using a nested Pydantic schema with six sub-models.

### [Utility Bills](Use_Cases/Utility_Bills/)
Extracts account information, billing period, charges, and usage data from utility bills using a JSON schema.

### [Continuing Education Certificates](Use_Cases/Continuing_Education_Certificates/)
Extracts CME certificate fields — provider, activity title, credit hours, completion date — from continuing education certificates.

---

## Events

### [Deep Learning AI Dev Day 2025](Events/Deep_Learning_AI_Dev_Day_2025/)
Conference demo: classify and extract from mixed financial documents (pay stubs, bank statements, investment statements) with bounding-box visualizations. Includes a caching layer to speed up re-runs.

### [Deep Learning Course: ADE on AWS](Events/Deep_Learning_Course_ADE_on_AWS/)
Course lesson: deploy ADE as a Lambda function, store results in S3, build a Bedrock knowledge base from parsed markdown, and create a medical document chatbot with conversation memory.

### [Data Science Dojo 2026](Events/Data_Science_Dojo_2026/)
End-to-end tutorial: extract structured data from PDFs, evaluate accuracy against a golden set, and iteratively refine the extraction schema until all fields reach ≥ 95% accuracy. Demonstrates the full Parse → Build Schema → Extract → Evaluate loop using the REST APIs directly (no Python SDK required for the Build Schema step).

### [Snowflake Intelligence Webinar 2026](Events/Snowflake_Intelligence_Webinar_2026/)
Webinar demo: SQL setup script and schema for parsing FINRA award documents inside the Snowflake ADE native application.

### [Deep Learning AI Dev Day 2026](Events/Deep_Learning_AI_Dev_Day_2026/)
Conference demo: production-ready multi-agent loan origination system powered by LandingAI ADE and Google ADK. Parses a mixed financial document packet, classifies and extracts structured fields, then runs loan scenarios through a Claude LoanDecisionAgent reviewed by a Claude ManagerReviewAgent. Features visual grounding, per-field confidence scores, live progress, results history, and a chat interface for running unlimited scenarios without re-uploading the PDF.

---

## Other

### [EDGAR API Pipeline](Other/EDGAR_API_Pipeline/)
Standalone utility for fetching SEC EDGAR 10-K and 8-K filings by ticker symbol and converting them to PDF. Does not use ADE — useful as a document source for ADE extraction pipelines.

---

## Resources

- [ADE Documentation](https://docs.landing.ai/ade/)
- [ADE Python Library (PyPI)](https://pypi.org/project/landingai-ade/)
- [API Key Setup](https://docs.landing.ai/ade/agentic-api-key)
- [ADE on Snowflake](https://docs.landing.ai/ade/ade-sf-overview)
