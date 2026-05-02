"""Detect text + bounding boxes in a generated portfolio image, output hotspots.json.

Strategy: send the image to a multimodal LLM (Gemini 2.5 / Claude) via the
pockgo relay. Ask for normalized bounding boxes (0-1000 range, Gemini convention)
plus a guessed semantic kind (link/email/contact/title/body/etc).

Why a vision LLM instead of PaddleOCR / Tesseract:
  - Zero local install; works behind a corporate firewall.
  - Reads CJK + Latin in mixed layouts, including stylized big titles, with
    no special config.
  - Returns intent inference for free (knows that "wangzetian@example.com"
    is mailto:, "查看作品" is a slide-jump candidate, "138-8888-8888" is tel:).
  - Uses the same key + relay we already verified.

Output JSON schema:
  [
    { "text": "wangzetian@example.com",
      "bbox": [x1, y1, x2, y2],          # pixel coords in the source image
      "kind": "email",
      "suggested_href": "mailto:wangzetian@example.com" },
    ...
  ]
"""
from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import urllib.request
from pathlib import Path

# ── Unified config (replaces hardcoded pockgo URL) ──
from config import BASE_URL, UA, require_api_key

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM = (
    "You are a precise OCR + UX classifier for portfolio deck pages. "
    "Return ONLY a JSON array, no prose, no markdown fences. "
    "Each item: {\"text\": str, \"bbox_norm\": [x1,y1,x2,y2], \"kind\": str}. "
    "bbox_norm uses the Gemini convention: integers in [0..1000], "
    "where [0,0] is top-left and [1000,1000] is bottom-right of the image. "
    "kind is one of: title, body, email, phone, wechat, url, button, "
    "nav-item, badge, code-color, copyright, decorative-english, "
    "metric-number, project-name, other. "
    "Detect EVERY visible text region, including big stylized titles, "
    "small captions, in-frame UI labels, and corner credits. "
    "Group multi-line titles into one item only if they are visually one "
    "block. Do not invent text. Do not translate. Preserve original "
    "punctuation and case."
)

USER_INSTRUCTION = (
    "List every text region in this portfolio page image. "
    "Return a JSON array per the schema. No commentary."
)


def _key() -> str:
    return require_api_key()


def _post(payload: dict, timeout: int = 240) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {_key()}",
            "Content-Type": "application/json",
            "User-Agent": UA,
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:600]}")


def _encode(path: Path) -> tuple[str, int, int]:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    raw = path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    # Get image dimensions cheaply (PNG header)
    w, h = _png_size(raw) if mime == "image/png" else (None, None)
    return f"data:{mime};base64,{b64}", w, h


def _png_size(raw: bytes) -> tuple[int, int]:
    # PNG IHDR chunk: bytes 16-23 are width, height (big-endian uint32)
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    import struct
    w, h = struct.unpack(">II", raw[16:24])
    return w, h


_JSON_BLOCK = re.compile(r"\[\s*{.*}\s*\]", re.S)


def _strip_json(text: str) -> str:
    # remove ```json fences if any
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = text.replace("```", "").strip()
    m = _JSON_BLOCK.search(text)
    return m.group(0) if m else text


def _parse_json_lenient(raw: str) -> list | None:
    """Parse a JSON array; if truncated, salvage as many complete objects as possible."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Salvage: find each top-level {...} object inside the array.
    items: list = []
    depth = 0
    start = -1
    in_str = False
    esc = False
    for i, ch in enumerate(raw):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
            continue
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                chunk = raw[start:i + 1]
                try:
                    items.append(json.loads(chunk))
                except json.JSONDecodeError:
                    pass
                start = -1
    return items if items else None


def _infer_href(item: dict) -> str | None:
    t = (item.get("text") or "").strip()
    kind = (item.get("kind") or "").lower()
    if kind == "email" or "@" in t and " " not in t:
        # extract email
        m = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", t)
        if m:
            return f"mailto:{m.group(0)}"
    if kind == "phone":
        digits = re.sub(r"\D", "", t)
        if 7 <= len(digits) <= 15:
            return f"tel:{digits}"
    if kind == "url" and "." in t:
        return t if t.startswith("http") else f"https://{t}"
    return None


def detect(image_path: str, model: str, out_path: str) -> None:
    p = Path(image_path)
    if not p.exists():
        sys.exit(f"ERROR: image not found: {image_path}")
    data_url, w, h = _encode(p)
    if not w or not h:
        # fall back: try PIL
        try:
            from PIL import Image  # type: ignore
            with Image.open(p) as im:
                w, h = im.size
        except Exception:
            sys.exit("ERROR: cannot determine image size; install Pillow or use PNG")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": USER_INSTRUCTION},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        "temperature": 0.0,
        "max_tokens": 32000,
    }
    resp = _post(payload)
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    content = msg.get("content")
    if isinstance(content, list):
        content = "".join(b.get("text", "") for b in content if b.get("type") == "text")
    if not isinstance(content, str):
        sys.exit(f"NO text in response: {json.dumps(resp)[:500]}")

    raw = _strip_json(content)
    items = _parse_json_lenient(raw)
    if items is None:
        sys.exit(f"BAD JSON from model.\n--- raw (last 800) ---\n{raw[-800:]}")

    if not isinstance(items, list):
        sys.exit(f"Expected JSON array, got: {type(items).__name__}")

    # Convert bbox_norm (0..1000) -> bbox pixel
    cleaned: list[dict] = []
    for it in items:
        bbox_n = it.get("bbox_norm") or it.get("bbox")
        if not bbox_n or len(bbox_n) != 4:
            continue
        x1, y1, x2, y2 = bbox_n
        # Some models swap to [y1, x1, y2, x2] (Gemini's actual convention!)
        # Heuristic: if model is gemini, assume [y1, x1, y2, x2]
        if model.startswith("gemini"):
            y1, x1, y2, x2 = bbox_n
        bbox_px = [
            int(round(x1 / 1000 * w)),
            int(round(y1 / 1000 * h)),
            int(round(x2 / 1000 * w)),
            int(round(y2 / 1000 * h)),
        ]
        out_item = {
            "text": (it.get("text") or "").strip(),
            "bbox": bbox_px,
            "bbox_norm": [x1, y1, x2, y2],
            "kind": it.get("kind") or "other",
        }
        href = _infer_href(out_item)
        if href:
            out_item["suggested_href"] = href
        cleaned.append(out_item)

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "image": p.name,
                "width": w,
                "height": h,
                "model": model,
                "hotspots": cleaned,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"OK  {len(cleaned)} hotspots  -> {out_path}")
    for it in cleaned[:8]:
        print(f"    [{it['kind']:>16}] {it['text'][:50]}  bbox={it['bbox']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="OCR + UX classification for portfolio images")
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"vision model (default: {DEFAULT_MODEL}); "
                         f"alternatives: claude-sonnet-4-5-20250929, gpt-4o-mini")
    args = ap.parse_args()
    detect(args.image, args.model, args.out)


if __name__ == "__main__":
    main()
