"""Overlay QA Agent.

Inspects a rendered deck page (PNG screenshot of the multi-zone HTML) using a
multimodal LLM to verify that text overlays are:

  1. not occluding the device mockup / UI
  2. visually aligned (same column = same edge)
  3. semantically corresponding to the in-image UI (text references real UI bits)
  4. readable (size + contrast against BG)
  5. logically complementary (title / desc / annotations don't repeat each other)
  6. matching the page intent (e.g. "排版干净留白充足" still holds)

Usage:
    python scripts/overlay_qa.py \\
        --rendered generated-images/jike-circle/anatomy-v3-rendered.png \\
        --layout   generated-images/jike-circle/anatomy-v3.layout.json \\
        --intent   "排版干净留白充足。Case 01 圈子首页：左栏文案 + iPhone mockup + 右栏注释" \\
        --out      generated-images/jike-circle/anatomy-v3.qa.json

Env: POCKGO_KEY  (same relay as image_client.py)
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import mimetypes
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

# ── Unified config (replaces hardcoded pockgo URL + model) ──
from config import BASE_URL, UA, QA_MODEL, require_api_key

MODEL = QA_MODEL  # can be overridden by BACKEND_QA_MODEL / OVERLAY_QA_MODEL

return require_api_key():
        sys.exit("ERROR: set POCKGO_KEY env var")
    return k


def _data_uri(p: Path, max_w: int = 1280) -> str:
    """Downscale large screenshots before base64'ing — relays often reject
    >2MB payloads with 503 / 413 / silent timeouts."""
    img = Image.open(p).convert("RGB")
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"


SYSTEM = """You are a senior UI/UX deck reviewer. You look at a rendered
portfolio deck page (a screenshot of a 2048x1152 canvas: a generated UIUX
hero image + HTML text overlays placed on top) and judge the overlay quality.

SEVERITY RULES (strict — misclassification breaks the closed loop):
- "blocker" = page is unshippable: overlay text fully covers a device mockup,
  page is broken / corrupt, or the overlay area is unreadable.
- "major"   = (a) overlay copy claims a UI element NOT visible in the image,
  contradicts visible UI text, or invents a concrete detail (food / video /
  specific label) absent from the screen; OR
  (b) **ANY character of overlay text is occluded by the device mockup, a
  glassmorphism callout, the phone bezel, or another overlay** — even if only
  "a few characters" are hidden. Text content lost = MAJOR, never minor; OR
  (c) text truncated / overflowing its box; OR
  (d) text contrast so low it cannot be read at arm's length.
- "minor"   = low contrast that's still legible, slightly tight spacing,
  wording could be tighter, alignment off by ≤4px.

When in doubt about whether something is "still readable" — escalate one
severity level. The closed loop's pass gate excludes blocker+major, so under-
classifying occlusion lets a broken page through.

You MUST return strict JSON with this schema, no prose, no markdown fence:
{
  "score": 0-10 integer (10 = ship it, 7 = minor fixes, <=5 = redo),
  "pass": true | false,
  "retake_image": true | false,   // true ONLY if the underlying generated image is unusable (UI illegible / wrong device / wrong theme)
  "issues": [
    {
      "severity": "blocker" | "major" | "minor",
      "area": "occlusion" | "alignment" | "image-text-correspondence" | "readability" | "logic" | "intent-match",
      "where": "short locator like 'left column desc' or 'right top annotation'",
      "what": "one sentence: what is wrong",
      "fix": "one sentence: concrete fix (e.g. move x by +40, shrink to 18pt, change copy to ...)"
    }
  ],
  "summary": "one paragraph in Chinese, max 80 chars, plain language"
}
"""


USER_TEMPLATE = """这是一张已经渲染好的 UIUX 作品集页（截图，含 HTML overlay）。
画布 2048x1152。

【页面意图】
{intent}

【overlay 布局元数据（每个 overlay 的位置 + 字段）】
{layout_summary}

请按 system 中的规则审阅这张图的 overlay 质量并返回 JSON。重点检查：
- 文字是否压到 device mockup（手机/屏幕）
- 同一栏文字左/右对齐是否一致
- overlay 文字描述的 UI 元素（如「圈友」「动态」「+赞 23」）是否真的能在图里看到
- 字号 / 对比度是否清晰
- 标题 / 副标 / desc / 注释 之间是否信息互补不是重复
- 整页是否仍符合「排版意图」标签
"""


def _summarize_layout(layout: dict) -> str:
    lines = []
    for i, ov in enumerate(layout.get("overlays", [])):
        texts = " | ".join(f.get("text", "")[:40] for f in ov.get("fields", []))
        lines.append(
            f"  [{i}] role={ov['role']} pos=({ov['x']},{ov['y']}) "
            f"size=({ov['w']}x{ov['h']}) text=\"{texts}\""
        )
    return "\n".join(lines)


def _post(payload: dict, timeout: int = 180) -> dict:
    headers = {
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        ),UAerr = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(
                f"{BASE_URL}/chat/completions", data=body, headers=headers, method="POST"
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            if e.code in (408, 425, 429, 500, 502, 503, 504, 524):
                last_err = f"HTTP {e.code}: {text[:200]}"
            else:
                sys.exit(f"HTTP {e.code}: {text[:600]}")
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        delay = (3 * (2 ** attempt)) * (0.7 + 0.6 * random.random())
        print(f"  retry {attempt+1}/4 in {delay:.1f}s  ({last_err})", file=sys.stderr, flush=True)
        time.sleep(delay)
    sys.exit(f"FAILED after 4 retries: {last_err}")


def _extract_json(text: str) -> dict:
    s = text.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.startswith("json"):
            s = s[4:]
    # find first { ... last }
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j < 0:
        raise ValueError(f"no JSON in model reply: {text[:300]}")
    return json.loads(s[i : j + 1])


def review(rendered: Path, layout_path: Path, intent: str) -> dict:
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    summary = _summarize_layout(layout)
    user_text = USER_TEMPLATE.format(intent=intent, layout_summary=summary)

    payload = {
        "model": MODEL,
        "temperature": 0.2,
        "max_tokens": 1500,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {"type": "image_url", "image_url": {"url": _data_uri(rendered)}},
                ],
            },
        ],
    }
    resp = _post(payload)
    try:
        text = resp["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        sys.exit(f"ERROR: bad response: {json.dumps(resp)[:400]}")
    return _extract_json(text)


def _print_report(qa: dict) -> None:
    print(f"\n=== Overlay QA · score={qa.get('score')} pass={qa.get('pass')} "
          f"retake_image={qa.get('retake_image')} ===")
    print(f"summary: {qa.get('summary', '')}\n")
    issues = qa.get("issues") or []
    if not issues:
        print("  (no issues)")
    for i, it in enumerate(issues, 1):
        sev = it.get("severity", "?").upper()
        print(f"  [{i}] {sev} · {it.get('area')} @ {it.get('where')}")
        print(f"      what: {it.get('what')}")
        print(f"      fix : {it.get('fix')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rendered", required=True, help="Path to rendered PNG screenshot")
    ap.add_argument("--layout", required=True, help="Path to layout.json")
    ap.add_argument("--intent", required=True, help="One-line page intent description")
    ap.add_argument("--out", required=True, help="Output JSON report path")
    args = ap.parse_args()

    rendered = Path(args.rendered)
    layout_path = Path(args.layout)
    if not rendered.exists():
        sys.exit(f"ERROR: rendered image not found: {rendered}")
    if not layout_path.exists():
        sys.exit(f"ERROR: layout not found: {layout_path}")

    qa = review(rendered, layout_path, args.intent)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
    _print_report(qa)
    print(f"\nOK -> {out}")


if __name__ == "__main__":
    main()
