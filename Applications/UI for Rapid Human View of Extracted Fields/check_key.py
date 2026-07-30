"""Verify the ADE API key is present and accepted, without spending credits.

    python check_key.py

Checks, in order:
  1. VISION_AGENT_API_KEY is loaded from .env (or the environment)
  2. The client constructs
  3. The key authenticates, via a read-only list of recent parse jobs

Never prints the key itself -- only its length and prefix.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

key = os.environ.get("VISION_AGENT_API_KEY", "").strip()

if not key:
    print("FAIL  VISION_AGENT_API_KEY is not set.")
    print("      Add it to .env in this folder:  VISION_AGENT_API_KEY=your_key")
    print("      Get a key at https://va.landing.ai/settings/api-key")
    sys.exit(1)

# Show only enough to confirm the right value landed, never the secret itself.
print(f"OK    key loaded: {len(key)} chars, starts with {key[:4]!r}")

try:
    from landingai_ade import LandingAIADE
except ImportError:
    print("FAIL  landingai-ade is not installed.  pip install -r requirements.txt")
    sys.exit(1)

try:
    client = LandingAIADE()
except Exception as exc:  # noqa: BLE001
    print(f"FAIL  could not construct client: {type(exc).__name__}: {exc}")
    sys.exit(1)

print("OK    client constructed")

if not hasattr(client, "v2"):
    import landingai_ade

    version = getattr(landingai_ade, "__version__", "unknown")
    print(f"FAIL  this SDK ({version}) has no client.v2; need landingai-ade >= 1.13.0")
    sys.exit(1)

print("OK    client.v2 available (DPT-3 stack)")

# Read-only call: lists recent jobs, parses nothing, costs no credits.
try:
    jobs = client.v2.parse_jobs.list(page=0, page_size=1)
except Exception as exc:  # noqa: BLE001
    print(f"FAIL  key was rejected or the API is unreachable: {type(exc).__name__}: {exc}")
    print("      A 401/403 means the key is wrong. Check for stray spaces or quotes in .env.")
    sys.exit(1)

count = len(getattr(jobs, "data", None) or [])
print(f"OK    authenticated — parse_jobs.list returned {count} recent job(s)")
print()
print("Ready. Start the app with:  uvicorn app:app --reload --port 8000")
