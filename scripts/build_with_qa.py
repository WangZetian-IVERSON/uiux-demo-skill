"""Build a multi-zone overlay page with closed-loop QA.

Pipeline:
    1. build_interactive_page.py --mode multi-zone   (HTML)
    2. render_screenshot.py                           (PNG)
    3. overlay_qa.py                                  (QA report JSON)
    4. if pass=false OR has major/blocker:
         ask LLM for a revised layout.json patch (full file)
         save layout, GOTO 1
       else:
         exit
    Max iterations: --max-iters (default 3)

Each iteration's artifacts are versioned: layout.iter1.json, page.iter1.html,
page.iter1-rendered.png, qa.iter1.json. The final passing version is also
written to the original layout/html/png paths.

Env: POCKGO_KEY  (vision/text relay key)
     OVERLAY_QA_MODEL (default claude-sonnet-4.5)

Usage:
    python scripts/build_with_qa.py \\
        --image    generated-images/jike-circle/anatomy-v3.png \\
        --layout   generated-images/jike-circle/anatomy-v3.layout.json \\
        --html     generated-images/jike-circle/anatomy-v3.html \\
        --rendered generated-images/jike-circle/anatomy-v3-rendered.png \\
        --intent   "Case 01 圈子首页：左栏文案 / 中央 iPhone mockup / 右栏注释。深紫梅 #1F1326 背景。排版意图：干净留白充足。" \\
        --title    "Case 01 v3" \\
        --max-iters 3
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

# ── Unified config (replaces hardcoded pockgo URL + model) ──
from config import BASE_URL, UA, QA_MODEL, require_api_key

DEFAULT_MODEL = QA_MODEL
SCRIPTS = Path(__file__).resolve().parent


def _key() -> str:
    return require_api_key()


def _data_uri(p: Path, max_w: int = 1280) -> str:
    img = Image.open(p).convert("RGB")
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=88)
    return f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"


def _post(payload: dict, timeout: int = 240) -> dict:
    headers = {
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": UA,
    }
    body = json.dumps(payload).encode("utf-8")
    last = None
    for attempt in range(4):
        try:
            req = urllib.request.Request(f"{BASE_URL}/chat/completions",
                                         data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            if e.code in (408, 425, 429, 500, 502, 503, 504, 524):
                last = f"HTTP {e.code}: {text[:200]}"
            else:
                sys.exit(f"HTTP {e.code}: {text[:600]}")
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        delay = (3 * (2 ** attempt)) * (0.7 + 0.6 * random.random())
        print(f"  retry {attempt+1}/4 in {delay:.1f}s ({last})", file=sys.stderr)
        time.sleep(delay)
    sys.exit(f"FAILED after 4 retries: {last}")


def _extract_json(text: str) -> dict:
    s = text.strip()
    if s.startswith("```"):
        s = s.strip("`")
        if s.startswith("json"):
            s = s[4:]
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j < 0:
        raise ValueError(f"no JSON in reply: {text[:300]}")
    return json.loads(s[i : j + 1])


# ---------------- pipeline steps ----------------

def step_build(image: Path, layout: Path, html: Path, title: str) -> None:
    cmd = [sys.executable, str(SCRIPTS / "build_interactive_page.py"),
           "--mode", "multi-zone",
           "--image", str(image), "--layout", str(layout),
           "--out", str(html), "--title", title]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"build_interactive_page failed:\n{r.stderr}")
    print(r.stdout.strip())


def step_screenshot(html: Path, out_png: Path) -> None:
    cmd = [sys.executable, str(SCRIPTS / "render_screenshot.py"),
           "--html", str(html), "--out", str(out_png)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"render_screenshot failed:\n{r.stderr}")
    print(r.stdout.strip())


# ---------------- LLM calls ----------------

QA_SYSTEM = """You are a senior UI/UX deck reviewer. You see a rendered portfolio
page (2048x1152: a generated UIUX hero image + HTML text overlays).

Return strict JSON only, no prose:
{
  "score": 0-10,
  "pass": true|false,
  "retake_image": true|false,
  "issues": [
    {"severity":"blocker|major|minor",
     "area":"occlusion|alignment|image-text-correspondence|readability|logic|intent-match",
     "where":"locator",
     "what":"one sentence",
     "fix":"one sentence concrete fix"}
  ],
  "summary": "<=80 char Chinese"
}

Severity rules — be strict:
- BLOCKER: overlay text physically covers the device mockup or hides UI; canvas broken.
- MAJOR: overlay copy claims a UI element that is NOT visible in the image
        (e.g. text says "评论" but the UI shows no comment area), OR copy
        contradicts visible UI text, OR copy mentions concrete details
        (food / video / specific labels) that aren't in the screen.
        Also MAJOR: text truncated / overflowing its box.
- MINOR: contrast slightly low, spacing could be tighter, wording could be tighter.

pass=true requires NO blocker AND NO major. minor issues OK.
retake_image=true ONLY if the underlying generated image (UI/device/theme) is unusable.
"""


def _qa(rendered: Path, layout: dict, intent: str) -> dict:
    summary = "\n".join(
        f"  [{i}] role={ov['role']} pos=({ov['x']},{ov['y']}) "
        f"size=({ov['w']}x{ov['h']}) text=\""
        f"{' | '.join(f.get('text','')[:40] for f in ov.get('fields', []))}\""
        for i, ov in enumerate(layout.get("overlays", []))
    )
    user = (
        f"【页面意图】\n{intent}\n\n"
        f"【overlay 布局元数据】\n{summary}\n\n"
        "请按 system 中的规则审阅这张图的 overlay 质量并返回 JSON。"
    )
    payload = {
        "model": DEFAULT_MODEL,
        "temperature": 0.2,
        "max_tokens": 1500,
        "messages": [
            {"role": "system", "content": QA_SYSTEM},
            {"role": "user", "content": [
                {"type": "text", "text": user},
                {"type": "image_url", "image_url": {"url": _data_uri(rendered)}},
            ]},
        ],
    }
    resp = _post(payload)
    return _extract_json(resp["choices"][0]["message"]["content"])


FIX_SYSTEM = """You are a layout repair agent. You receive:
- a rendered deck page screenshot (2048x1152)
- the current layout.json (text overlays placed on the image)
- a QA report listing issues (severity, area, where, what, fix)

Your job: output a REVISED full layout.json that addresses every blocker/major
issue and as many minors as feasible WITHOUT breaking other parts.

Rules:
1. Output ONLY the JSON object, no prose, no fence.
2. Keep the same top-level keys: image, image_w, image_h, page_id, deck_palette,
   deck_fonts, overlays.
3. Keep overlay count and order unless an issue explicitly requires removal.
4. You MAY change: x, y, w, h (overlay box), field.text (copy), field.size_pt,
   field.color, field.align, field.line_height. Stay inside 0..image_w/image_h.
5. Do NOT change image / image_w / image_h / deck_palette / deck_fonts.
6. Don't move overlays onto the device mockup region (occlusion).
7. Prefer concrete numeric tweaks suggested in QA `fix` fields.
"""


def _fix_layout(rendered: Path, layout: dict, qa: dict, intent: str) -> dict:
    user = (
        f"【页面意图】\n{intent}\n\n"
        f"【当前 layout.json】\n```json\n{json.dumps(layout, ensure_ascii=False, indent=2)}\n```\n\n"
        f"【QA 报告】\n```json\n{json.dumps(qa, ensure_ascii=False, indent=2)}\n```\n\n"
        "请输出修订后的完整 layout.json（仅 JSON，无围栏，无解释）。"
    )
    payload = {
        "model": DEFAULT_MODEL,
        "temperature": 0.15,
        "max_tokens": 4000,
        "messages": [
            {"role": "system", "content": FIX_SYSTEM},
            {"role": "user", "content": [
                {"type": "text", "text": user},
                {"type": "image_url", "image_url": {"url": _data_uri(rendered)}},
            ]},
        ],
    }
    resp = _post(payload)
    return _extract_json(resp["choices"][0]["message"]["content"])


# ---------------- orchestration ----------------

def _has_blocking(qa: dict) -> bool:
    if not qa.get("pass", False):
        return True
    for it in qa.get("issues", []):
        if it.get("severity") in ("blocker", "major"):
            return True
    return False


def _print_qa(qa: dict, iter_n: int) -> None:
    print(f"\n--- QA iter {iter_n} · score={qa.get('score')} pass={qa.get('pass')} "
          f"retake_image={qa.get('retake_image')} ---")
    print(f"summary: {qa.get('summary','')}")
    for i, it in enumerate(qa.get("issues") or [], 1):
        print(f"  [{i}] {it.get('severity','?').upper()} · {it.get('area')} @ {it.get('where')}")
        print(f"      what: {it.get('what')}")
        print(f"      fix : {it.get('fix')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--layout", required=True)
    ap.add_argument("--html", required=True)
    ap.add_argument("--rendered", required=True)
    ap.add_argument("--intent", required=True)
    ap.add_argument("--title", default="page")
    ap.add_argument("--max-iters", type=int, default=3)
    args = ap.parse_args()

    image = Path(args.image)
    layout_path = Path(args.layout)
    html_path = Path(args.html)
    rendered_path = Path(args.rendered)

    # Backup the seed layout once.
    seed_backup = layout_path.with_suffix(layout_path.suffix + ".seed.bak")
    if not seed_backup.exists():
        shutil.copy2(layout_path, seed_backup)
        print(f"  seed backup -> {seed_backup}")

    qa_history: list[dict] = []
    last_pass = False
    for it in range(1, args.max_iters + 1):
        print(f"\n========= iter {it} =========")
        step_build(image, layout_path, html_path, args.title)
        step_screenshot(html_path, rendered_path)
        layout = json.loads(layout_path.read_text(encoding="utf-8"))
        qa = _qa(rendered_path, layout, args.intent)
        qa_history.append(qa)

        # Persist per-iter artifacts.
        ver = f".iter{it}"
        shutil.copy2(layout_path, layout_path.with_suffix(layout_path.suffix + ver))
        shutil.copy2(html_path,   html_path.with_suffix(html_path.suffix + ver))
        shutil.copy2(rendered_path, rendered_path.with_suffix(rendered_path.suffix + ver))
        qa_dump = layout_path.with_name(layout_path.stem + f".qa.iter{it}.json")
        qa_dump.write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")

        _print_qa(qa, it)

        if qa.get("retake_image"):
            print("\n!! retake_image=true — underlying image needs regeneration.")
            print("   Re-run ComfyUI with image-prompt-style-uiux.md, then retry build_with_qa.")
            sys.exit(2)

        if not _has_blocking(qa):
            last_pass = True
            print(f"\nPASSED at iter {it}")
            break

        if it == args.max_iters:
            print(f"\n!! max iters reached, still has blocking issues")
            break

        # Ask LLM for revised layout.
        print("\n  → requesting layout fix from LLM...")
        new_layout = _fix_layout(rendered_path, layout, qa, args.intent)
        # Sanity guards.
        if new_layout.get("image_w") != layout["image_w"] or new_layout.get("image_h") != layout["image_h"]:
            print("  WARN model changed canvas size, restoring.")
            new_layout["image_w"] = layout["image_w"]
            new_layout["image_h"] = layout["image_h"]
        new_layout["deck_palette"] = layout["deck_palette"]
        new_layout["deck_fonts"] = layout["deck_fonts"]
        layout_path.write_text(json.dumps(new_layout, ensure_ascii=False, indent=2),
                               encoding="utf-8")
        print(f"  layout patched -> {layout_path}")

    final_qa = qa_history[-1]
    final_qa_path = layout_path.with_suffix(".qa.json")
    final_qa_path.write_text(json.dumps(final_qa, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    print(f"\nFINAL: pass={last_pass} score={final_qa.get('score')} iters={len(qa_history)}")
    print(f"  layout : {layout_path}")
    print(f"  html   : {html_path}")
    print(f"  shot   : {rendered_path}")
    print(f"  qa     : {final_qa_path}")
    sys.exit(0 if last_pass else 1)


if __name__ == "__main__":
    main()
