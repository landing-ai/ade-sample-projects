# ADE Python Quickstart

This notebook follows the quickstart code snippets available at the [ADE Quickstart Guide](https://docs.landing.ai/ade/ade-quickstart).

## Getting Started

The notebook demonstrates how to:
- Parse documents using the ADE Parse API
- Extract structured data using the ADE Extract API
- Work with Pydantic schemas for data extraction

## Setup

1. Create a virtual environment:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

2. Install required packages:
```bash
pip install ipykernel jupyter landingai_ade
```

3. Register the kernel:
```bash
python -m ipykernel install --user --name=ade-sample-projects
```

4. Open the notebook and select the `ade-sample-projects` kernel.

5. Set your API key in the notebook (see the first code cell for instructions).

## Resources

- [ADE Documentation](https://docs.landing.ai/ade/)
- [ADE Quickstart Guide](https://docs.landing.ai/ade/ade-quickstart)
- [ADE Python Library](https://docs.landing.ai/ade/ade-python)
