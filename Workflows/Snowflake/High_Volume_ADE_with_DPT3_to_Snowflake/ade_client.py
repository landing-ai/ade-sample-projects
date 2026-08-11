"""
ade_client.py
-------------
Thin wrapper over the ``landingai-ade`` DPT-3 endpoints.

DPT-3 splits parsing and extraction into two calls:

    parse_result   = client.v2.parse(document=..., model=...)      -> V2ParseResponse
    extract_result = client.v2.extract(schema=..., markdown=...)    -> V2ExtractResult

``client.v2.parse`` returns markdown plus a ``structure`` tree (document -> page
-> block) with per-block grounding; ``client.v2.extract`` takes a Pydantic model
directly and returns ``extraction`` / ``extraction_metadata`` dicts.

The client reads ``VISION_AGENT_API_KEY`` from the environment; we pass it
explicitly so a key sourced via ``.env`` is always honored.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple

from landingai_ade import LandingAIADE

from config import Settings


def build_client(settings: Settings) -> LandingAIADE:
    kwargs: dict[str, Any] = {"apikey": settings.VISION_AGENT_API_KEY}
    if settings.ADE_ENVIRONMENT and settings.ADE_ENVIRONMENT.lower() == "eu":
        kwargs["environment"] = "eu"
    return LandingAIADE(**kwargs)


def parse_and_extract(
    client: LandingAIADE,
    file_path: str,
    schema_cls: Any,
    settings: Settings,
) -> Tuple[Any, Any]:
    """Parse a document then extract structured fields. Returns
    ``(parse_result, extract_result)`` (V2ParseResponse, V2ExtractResult)."""
    parse_result = client.v2.parse(
        document=Path(file_path),
        model=settings.PARSE_MODEL,
    )
    extract_result = client.v2.extract(
        schema=schema_cls,
        markdown=parse_result.markdown,
        model=settings.EXTRACT_MODEL,
    )
    return parse_result, extract_result
