"""
Thin REST client for LandingAI ADE **v2** (DPT-3) async APIs.

This module wraps the four endpoints used by the invoice pipeline:

    Parse Jobs v2      POST /v2/parse/jobs      +  GET /v2/parse/jobs/{job_id}
    Extract Jobs v2    POST /v2/extract/jobs    +  GET /v2/extract/jobs/{job_id}

Only v2 endpoints are used, per the project instructions. All calls go to the
same host (`https://api.ade.landing.ai`) and authenticate with a Bearer token
read from the VISION_AGENT_API_KEY environment variable.

Docs:
    https://docs.landing.ai/dpt3/parse-async
    https://docs.landing.ai/dpt3/extract-async
    https://docs.landing.ai/dpt3/parse-response
    https://docs.landing.ai/dpt3/extract-response
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Callable

import requests

# The v2 APIs share one host with the synchronous Parse/Extract endpoints.
BASE_URL = "https://api.ade.landing.ai"

# DPT-3 model family default for Parse Jobs (accepts dpt-3-pro-latest,
# a dated snapshot like dpt-3-pro-20260710, or the bare dpt-3-pro alias).
DEFAULT_PARSE_MODEL = "dpt-3-pro-latest"

# Terminal job states returned by the poll endpoints.
TERMINAL_STATUSES = {"completed", "failed"}


def get_api_key() -> str:
    """Return the ADE API key from the VISION_AGENT_API_KEY environment variable."""
    key = os.environ.get("VISION_AGENT_API_KEY")
    if not key:
        raise ValueError(
            "API key not found. Set the VISION_AGENT_API_KEY environment variable "
            "(or add it to a .env file and load it before running)."
        )
    return key


def _auth_header(api_key: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


# ---------------------------------------------------------------------------
# Parse Jobs v2
# ---------------------------------------------------------------------------

def create_parse_job(
    document_path: str | Path,
    api_key: str,
    model: str = DEFAULT_PARSE_MODEL,
    service_tier: str = "standard",
    timeout: int = 120,
) -> str:
    """
    Submit a document to Parse Jobs v2 and return the job_id.

    POST /v2/parse/jobs  (multipart/form-data)
    """
    doc_path = Path(document_path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")

    url = f"{BASE_URL}/v2/parse/jobs"
    data = {"model": model, "service_tier": service_tier}

    with open(doc_path, "rb") as fh:
        files = {"document": (doc_path.name, fh, "application/pdf")}
        resp = requests.post(
            url, headers=_auth_header(api_key), data=data, files=files, timeout=timeout
        )

    _raise_for_status(resp, context=f"create parse job for {doc_path.name}")
    return resp.json()["job_id"]


def get_parse_job(job_id: str, api_key: str, timeout: int = 120) -> dict[str, Any]:
    """Poll a single parse job. GET /v2/parse/jobs/{job_id}."""
    url = f"{BASE_URL}/v2/parse/jobs/{job_id}"
    resp = requests.get(url, headers=_auth_header(api_key), timeout=timeout)
    _raise_for_status(resp, context=f"get parse job {job_id}")
    return resp.json()


# ---------------------------------------------------------------------------
# Extract Jobs v2
# ---------------------------------------------------------------------------

def create_extract_job(
    markdown: str,
    schema_json: str,
    api_key: str,
    model: str | None = None,
    service_tier: str = "standard",
    filename: str = "markdown.md",
    timeout: int = 120,
) -> str:
    """
    Submit Markdown + a JSON schema to Extract Jobs v2 and return the job_id.

    POST /v2/extract/jobs  (multipart/form-data)

    Args:
        markdown: The Markdown to extract from (Parse v2 output). Sent as a file
            part so large inputs are staged by the gateway.
        schema_json: The extraction schema as a JSON *string*.
        model: Optional extract model version (defaults to the API's latest).
        service_tier: "standard" (default) or "priority".
    """
    url = f"{BASE_URL}/v2/extract/jobs"

    data: dict[str, str] = {"schema": schema_json, "service_tier": service_tier}
    if model:
        data["model"] = model

    files = {"markdown": (filename, markdown.encode("utf-8"), "text/markdown")}
    resp = requests.post(
        url, headers=_auth_header(api_key), data=data, files=files, timeout=timeout
    )
    _raise_for_status(resp, context="create extract job")
    return resp.json()["job_id"]


def get_extract_job(job_id: str, api_key: str, timeout: int = 120) -> dict[str, Any]:
    """Poll a single extract job. GET /v2/extract/jobs/{job_id}."""
    url = f"{BASE_URL}/v2/extract/jobs/{job_id}"
    resp = requests.get(url, headers=_auth_header(api_key), timeout=timeout)
    _raise_for_status(resp, context=f"get extract job {job_id}")
    return resp.json()


# ---------------------------------------------------------------------------
# Polling
# ---------------------------------------------------------------------------

def poll_job(
    get_fn: Callable[[str, str], dict[str, Any]],
    job_id: str,
    api_key: str,
    poll_interval: float = 5.0,
    max_wait: float = 900.0,
) -> dict[str, Any]:
    """
    Poll a job until it reaches a terminal state (completed / failed).

    Args:
        get_fn: get_parse_job or get_extract_job.
        job_id: The job to poll.
        poll_interval: Seconds between polls (standard tier is slower).
        max_wait: Give up after this many seconds.

    Returns:
        The final job response dict (status == "completed" or "failed").

    Raises:
        TimeoutError: If the job does not finish within max_wait.
    """
    deadline = time.monotonic() + max_wait
    while True:
        job = get_fn(job_id, api_key)
        status = job.get("status")
        if status in TERMINAL_STATUSES:
            return job
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Job {job_id} did not finish within {max_wait:.0f}s "
                f"(last status: {status})."
            )
        time.sleep(poll_interval)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _raise_for_status(resp: requests.Response, context: str) -> None:
    """Raise a readable error, surfacing the v2 {code, message} error body."""
    if resp.ok:
        return
    detail = ""
    try:
        body = resp.json()
        # v2 errors use {"code": "...", "message": "..."}
        detail = f' — {body.get("code")}: {body.get("message")}' if isinstance(body, dict) else f" — {body}"
    except ValueError:
        detail = f" — {resp.text[:500]}"
    raise RuntimeError(f"ADE v2 API error ({context}): HTTP {resp.status_code}{detail}")
