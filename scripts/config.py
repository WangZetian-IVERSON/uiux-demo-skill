"""
Unified backend configuration for all scripts in this skill.

All scripts import BackendConfig from here instead of hardcoding URLs, keys,
and model names. Environment variables control everything; defaults maintain
backward-compatibility with the original pockgo-only setup.

Quick start (zero config — works exactly as before):
    $env:POCKGO_KEY = "sk-..."
    python scripts/image_client.py generate --model gpt-image-2 ...

Switch to a different relay / provider:
    $env:BACKEND_BASE_URL = "https://api.openai.com/v1"
    $env:BACKEND_API_KEY  = "sk-..."
    python scripts/image_client.py generate --model gpt-image-2 ...

Environment variables:
  ── Required ──
  BACKEND_API_KEY             API key for the active backend (falls back to POCKGO_KEY)

  ── Backend selection ──
  BACKEND                     "pockgo" | "openai" | "gemini" | "custom" (default: "pockgo")
  BACKEND_BASE_URL            Base URL including /v1 (default: https://newapi.pockgo.com/v1)

  ── Default models (used when scripts don't specify --model) ──
  BACKEND_IMAGE_MODEL         Default: gpt-image-2
  BACKEND_QA_MODEL            Default: gpt-4o (overlay_qa.py + build_with_qa.py)

  ── ComfyUI (separate path, not affected by BACKEND_*) ──
  COMFY_API_KEY               ComfyUI platform API key
  COMFYUI_URL                 ComfyUI Desktop server URL (default: http://127.0.0.1:8188)

  ── Legacy (still read as fallbacks) ──
  POCKGO_KEY                  → BACKEND_API_KEY
  OVERLAY_QA_MODEL            → BACKEND_QA_MODEL
"""

from __future__ import annotations

import os
import sys

# ---------------------------------------------------------------------------
# Resolve the active backend
# ---------------------------------------------------------------------------

_backend = os.environ.get("BACKEND", "pockgo").strip().lower()

# Base URL — defaults differ per backend
_BASE_URL_DEFAULTS: dict[str, str] = {
    "pockgo": "https://newapi.pockgo.com/v1",
    "openai": "https://api.openai.com/v1",
    "gemini": "https://generativelanguage.googleapis.com/v1beta",
    "custom": "",
}

BASE_URL: str = os.environ.get(
    "BACKEND_BASE_URL", _BASE_URL_DEFAULTS.get(_backend, _BASE_URL_DEFAULTS["pockgo"])
).rstrip("/")

# API key — BACKEND_API_KEY first, then legacy POCKGO_KEY
API_KEY: str = (
    os.environ.get("BACKEND_API_KEY", "")
    or os.environ.get("POCKGO_KEY", "")
    or os.environ.get("OPENAI_API_KEY", "")
    or os.environ.get("GEMINI_API_KEY", "")
).strip()

# Default models (used when scripts don't receive --model or equivalent)
IMAGE_MODEL: str = os.environ.get("BACKEND_IMAGE_MODEL", "gpt-image-2").strip()
QA_MODEL: str = (
    os.environ.get("BACKEND_QA_MODEL")
    or os.environ.get("OVERLAY_QA_MODEL")
    or "gpt-4o"
).strip()

# ComfyUI — separate subsystem unaffected by BACKEND
COMFY_API_KEY: str = os.environ.get("COMFY_API_KEY", "").strip()
COMFYUI_URL: str = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188").strip()

# ---------------------------------------------------------------------------
# Browser User-Agent (used by all HTTP calls)
# ---------------------------------------------------------------------------

UA: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------

def require_api_key() -> str:
    """Return API_KEY or exit with a helpful message."""
    if not API_KEY:
        sys.exit(
            "ERROR: No API key set.\n"
            "  Set BACKEND_API_KEY (or legacy POCKGO_KEY) environment variable.\n"
            f"  Active backend: {_backend}  →  BASE_URL: {BASE_URL}"
        )
    return API_KEY


# ---------------------------------------------------------------------------
# Human-readable summary (useful for debug)
# ---------------------------------------------------------------------------

def summary() -> str:
    return (
        f"backend={_backend}  base_url={BASE_URL}\n"
        f"  image_model={IMAGE_MODEL}  qa_model={QA_MODEL}\n"
        f"  api_key={'✓' if API_KEY else '✗ (missing)'}"
    )
