"""Production image client for the pockgo OpenAI-compatible relay.

Verified 2026-05 against:
  - gpt-image-2 / gpt-image-2-2k / gpt-image-2-4k          (OpenAI-style /images/generations)
  - nano-banana-pro / -2k / -4k                            (chat-completions multimodal)
  - gemini-3-pro-image-preview / -2k / -4k                 (chat-completions multimodal)

Why this exists:
  - The relay sits behind Cloudflare and rejects requests without a browser User-Agent
    with "403 error code: 1010". Python's default UA is blocked.
  - Two endpoint shapes (OpenAI images-generations vs Gemini chat-completions
    multimodal) need different request bodies and response parsers.
  - Reference-image chaining (per references/visual-consistency.md) needs base64
    encoding of a previously generated PNG.
  - PADB-prefixed prompts (per references/image-generation-protocol.md) tend to be
    long; reading from a file is more reliable than CLI quoting.

Usage:
  $env:BACKEND_API_KEY = "sk-..."    # or legacy POCKGO_KEY
  python scripts/image_client.py generate \
      --model gpt-image-2 \
      --prompt-file prompts/cover.txt \
      --size 1792x1024 \
      --out generated-images/finance-saas/cover.png

  # Direct OpenAI / Gemini (set BACKEND_BASE_URL + BACKEND_API_KEY):
  python scripts/image_client.py generate \
      --backend openai \
      --model gpt-image-2 \
      ...

  python scripts/image_client.py models           # list image-capable models
  python scripts/image_client.py health           # one cheap test image
"""
from __future__ import annotations

import argparse
import base64
import copy
import json
import mimetypes
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

# ── Unified config (replaces hardcoded pockgo URL) ──
from config import BASE_URL, UA, COMFY_API_KEY, COMFYUI_URL, require_api_key

OPENAI_IMAGE_MODELS = {
    "gpt-image-1.5",
    "gpt-image-2",
    "gpt-image-2-2k",
    "gpt-image-2-4k",
}

# Models routed through chat-completions multimodal (Gemini-style)
CHAT_IMAGE_MODELS_PREFIX = ("nano-banana", "gemini-", "qwen-image", "flux-", "grok-")


def _key() -> str:
    return require_api_key()


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_key()}",
        "Content-Type": "application/json",
        "User-Agent": UA,
        "Accept": "application/json",
    }


def _post(path: str, payload: dict, timeout: int = 240) -> dict:
    """POST with robust retries.

    pockgo sits behind Cloudflare; image2 at 2k often takes 80-150s to render,
    which routinely trips CF's ~100s edge timeout. We see two failure modes:
      - HTTPError 502/503/504/524: visible 5xx from CF
      - URLError / RemoteDisconnected / "Remote end closed connection without response":
        CF closed the socket mid-flight while the upstream is still rendering
    Both are transient. Retry up to MAX_RETRIES with exponential backoff + jitter.
    """
    import random
    MAX_RETRIES = 5
    url = f"{BASE_URL}{path}"
    body = json.dumps(payload).encode("utf-8")
    last_err: object = None
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, data=body, headers=_headers(), method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")
            # Cloudflare 1010 is a UA problem; do not retry, just fail loudly.
            if "1010" in text or e.code == 403:
                sys.exit(f"HTTP {e.code} (Cloudflare): {text[:300]}")
            if e.code in (408, 425, 429, 500, 502, 503, 504, 524):
                last_err = f"HTTP {e.code}: {text[:200]}"
            else:
                sys.exit(f"HTTP {e.code}: {text[:600]}")
        except Exception as e:
            # urllib.error.URLError, http.client.RemoteDisconnected,
            # ConnectionResetError, socket.timeout — all transient for us.
            last_err = f"{type(e).__name__}: {e}"
        # backoff: 3, 6, 12, 24, 48 seconds (+/- 30% jitter)
        delay = (3 * (2 ** attempt)) * (0.7 + 0.6 * random.random())
        print(f"  retry {attempt+1}/{MAX_RETRIES} in {delay:.1f}s  ({last_err})",
              file=sys.stderr, flush=True)
        time.sleep(delay)
    sys.exit(f"FAILED after {MAX_RETRIES} retries: {last_err}")


def _get(path: str, timeout: int = 30) -> dict:
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers=_headers(), method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _read_prompt(prompt: str | None, prompt_file: str | None) -> str:
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8").strip()
    if prompt:
        return prompt
    sys.exit("ERROR: provide --prompt or --prompt-file")


def _encode_reference(path: str) -> str:
    p = Path(path)
    if not p.exists():
        sys.exit(f"ERROR: reference image not found: {path}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _save_b64(out_path: str, b64: str) -> int:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = base64.b64decode(b64)
    p.write_bytes(raw)
    return len(raw)


def _route(model: str) -> str:
    # 2k/4k variants on this relay are served via /chat/completions and return
    # an https URL inside the assistant message, NOT base64.
    if model in {"gpt-image-2-2k", "gpt-image-2-4k"}:
        return "chat-multimodal"
    if model in OPENAI_IMAGE_MODELS:
        return "openai-images"
    if any(model.startswith(pfx) for pfx in CHAT_IMAGE_MODELS_PREFIX):
        return "chat-multimodal"
    # default: try OpenAI shape first
    return "openai-images"


# ---------------- ComfyUI backend ----------------
#
# ComfyUI exposes:
#   POST /prompt          -> queues a workflow, returns {"prompt_id": "..."}
#   GET  /history/{id}    -> returns {"<id>": {"outputs": {<node_id>: {"images": [{filename,subfolder,type}]}}}}
#   GET  /view?filename=&subfolder=&type=output  -> raw PNG bytes
#
# We load a workflow template (API format, exported via "Save (API Format)"),
# find the OpenAIGPTImage1 node, inject prompt + size + random seed + model,
# submit, poll until done, then download the SaveImage output.

def _comfyui_post(url: str, path: str, payload: dict, timeout: int = 60) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url.rstrip("/") + path,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": UA},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _comfyui_get(url: str, path: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url.rstrip("/") + path, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _comfyui_download(url: str, filename: str, subfolder: str, type_: str,
                      timeout: int = 60) -> bytes:
    qs = urllib.parse.urlencode({"filename": filename, "subfolder": subfolder, "type": type_})
    req = urllib.request.Request(
        url.rstrip("/") + "/view?" + qs, headers={"User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _generate_via_comfyui(args: argparse.Namespace, prompt: str) -> None:
    workflow_path = Path(args.comfyui_workflow)
    if not workflow_path.exists():
        sys.exit(f"ERROR: ComfyUI workflow template not found: {workflow_path}")
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))

    # Locate the OpenAIGPTImage1 node and inject our params.
    image_node_id = None
    for node_id, node in workflow.items():
        if node.get("class_type") == "OpenAIGPTImage1":
            image_node_id = node_id
            break
    if image_node_id is None:
        sys.exit("ERROR: workflow has no OpenAIGPTImage1 node")

    wf = copy.deepcopy(workflow)
    inputs = wf[image_node_id]["inputs"]
    inputs["prompt"] = prompt
    inputs["size"] = args.size
    inputs["model"] = args.model
    inputs["seed"] = random.randint(1, 2**31 - 1)
    inputs["n"] = args.n
    if args.comfyui_quality:
        inputs["quality"] = args.comfyui_quality

    client_id = uuid.uuid4().hex
    body = {"prompt": wf, "client_id": client_id}
    api_key = args.comfyui_api_key or COMFY_API_KEY
    if api_key:
        body["extra_data"] = {"api_key_comfy_org": api_key}
    submit = _comfyui_post(args.comfyui_url, "/prompt", body)
    prompt_id = submit.get("prompt_id")
    if not prompt_id:
        sys.exit(f"ERROR: ComfyUI did not return prompt_id: {json.dumps(submit)[:400]}")
    print(f"  comfyui: queued prompt_id={prompt_id} (node={image_node_id}, seed={inputs['seed']})",
          file=sys.stderr)

    # Poll /history/{prompt_id} until outputs appear or status indicates error.
    deadline = time.time() + args.comfyui_timeout
    history = None
    while time.time() < deadline:
        try:
            hist = _comfyui_get(args.comfyui_url, f"/history/{prompt_id}")
        except urllib.error.URLError as e:
            print(f"  comfyui: poll error {e}, retrying...", file=sys.stderr)
            time.sleep(2)
            continue
        entry = hist.get(prompt_id)
        if entry:
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                msgs = status.get("messages", [])
                sys.exit(f"ERROR: ComfyUI run failed: {json.dumps(msgs)[:600]}")
            outputs = entry.get("outputs", {})
            if outputs:
                history = entry
                break
        time.sleep(2)
    if history is None:
        sys.exit(f"ERROR: ComfyUI run did not finish within {args.comfyui_timeout}s")

    # Find the first SaveImage-style node with an "images" array.
    images_meta = None
    for node_id, out in history.get("outputs", {}).items():
        imgs = out.get("images") or []
        if imgs:
            images_meta = imgs[0]
            break
    if not images_meta:
        sys.exit(f"ERROR: ComfyUI history has no images: {json.dumps(history)[:600]}")

    raw = _comfyui_download(
        args.comfyui_url,
        filename=images_meta["filename"],
        subfolder=images_meta.get("subfolder", ""),
        type_=images_meta.get("type", "output"),
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    print(f"OK  {args.out}  {len(raw):,} bytes  backend=comfyui  model={args.model}")


def cmd_generate(args: argparse.Namespace) -> None:
    prompt = _read_prompt(args.prompt, args.prompt_file)

    if args.backend == "comfyui":
        return _generate_via_comfyui(args, prompt)

    route = _route(args.model)

    if route == "openai-images":
        if args.reference:
            sys.exit(
                "ERROR: --reference (image-to-image) is only supported via chat-multimodal "
                "models (nano-banana / gemini-3-pro-image / etc). gpt-image-2 ref editing "
                "uses /images/edits which this client does not wrap yet."
            )
        payload = {
            "model": args.model,
            "prompt": prompt,
            "size": args.size,
            "n": args.n,
        }
        resp = _post("/images/generations", payload)
        items = resp.get("data") or []
        if not items:
            sys.exit(f"EMPTY response: {json.dumps(resp)[:400]}")
        b64 = items[0].get("b64_json")
        if not b64:
            sys.exit(f"NO b64_json in: {json.dumps(items[0])[:400]}")
        nbytes = _save_b64(args.out, b64)
        revised = items[0].get("revised_prompt", "")
        print(f"OK  {args.out}  {nbytes:,} bytes  model={args.model}")
        if revised:
            print(f"    revised_prompt: {revised[:200]}")
        return

    # chat-multimodal
    content: list[dict] = [{"type": "text", "text": prompt}]
    if args.reference:
        content.append(
            {"type": "image_url", "image_url": {"url": _encode_reference(args.reference)}}
        )
    payload = {
        "extra_body": {"imageConfig": {"aspectRatio": args.aspect}},
        "model": args.model,
        "messages": [
            {
                "role": "system",
                "content": json.dumps({"imageConfig": {"aspectRatio": args.aspect}}),
            },
            {"role": "user", "content": content},
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
    }
    resp = _post("/chat/completions", payload)
    msg = (resp.get("choices") or [{}])[0].get("message", {})
    # Look for b64 in any of: message.images[0].image_url.url, content blocks, or markdown
    b64 = _extract_b64_from_chat(msg)
    if not b64:
        # Fall back to plain https URL inside the assistant content
        url = _extract_url_from_chat(msg)
        if url:
            raw = _download(url)
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_bytes(raw)
            print(f"OK  {args.out}  {len(raw):,} bytes  model={args.model}  via=url")
            return
        sys.exit(f"NO image in response. Snippet: {json.dumps(resp)[:600]}")
    nbytes = _save_b64(args.out, b64)
    print(f"OK  {args.out}  {nbytes:,} bytes  model={args.model}  aspect={args.aspect}")


_DATA_URL_RE = re.compile(r"data:image/[a-zA-Z]+;base64,([A-Za-z0-9+/=]+)")
_HTTPS_IMG_RE = re.compile(r"https?://[^\s)>\]\"']+\.(?:png|jpg|jpeg|webp)[^\s)>\]\"']*", re.I)


def _download(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _extract_url_from_chat(message: dict) -> str | None:
    content = message.get("content")
    if isinstance(content, str):
        m = _HTTPS_IMG_RE.search(content)
        if m:
            return m.group(0)
    if isinstance(content, list):
        for block in content:
            text = block.get("text", "") if isinstance(block, dict) else ""
            m = _HTTPS_IMG_RE.search(text)
            if m:
                return m.group(0)
            if isinstance(block, dict) and block.get("type") == "image_url":
                url = block.get("image_url", {}).get("url", "")
                m = _HTTPS_IMG_RE.search(url)
                if m:
                    return m.group(0)
    imgs = message.get("images") or []
    for it in imgs:
        url = it.get("image_url", {}).get("url") or it.get("url") or ""
        m = _HTTPS_IMG_RE.search(url)
        if m:
            return m.group(0)
    return None


def _extract_b64_from_chat(message: dict) -> str | None:
    # Pattern 1: images array (some relays put it at top-level of message)
    imgs = message.get("images") or []
    if imgs:
        url = imgs[0].get("image_url", {}).get("url") or imgs[0].get("url")
        if url:
            m = _DATA_URL_RE.search(url)
            if m:
                return m.group(1)
            # url may be https; we don't download here, treat as miss
    # Pattern 2: content is a list of blocks
    content = message.get("content")
    if isinstance(content, list):
        for block in content:
            if block.get("type") == "image_url":
                url = block.get("image_url", {}).get("url", "")
                m = _DATA_URL_RE.search(url)
                if m:
                    return m.group(1)
            text = block.get("text", "")
            m = _DATA_URL_RE.search(text)
            if m:
                return m.group(1)
    # Pattern 3: content is a string with embedded markdown / data url
    if isinstance(content, str):
        m = _DATA_URL_RE.search(content)
        if m:
            return m.group(1)
    return None


def cmd_models(args: argparse.Namespace) -> None:
    data = _get("/models")
    ids = [m["id"] for m in data.get("data", [])]
    pat = re.compile(r"image|dall|imagen|nano|flux|midjourney|sora|grok-imagine|qwen-image", re.I)
    matches = sorted(i for i in ids if pat.search(i))
    print(f"TOTAL: {len(ids)}  IMAGE-CAPABLE: {len(matches)}")
    for i in matches:
        print(" -", i)


def cmd_health(args: argparse.Namespace) -> None:
    out = Path("generated-images/_health_check.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model": "gpt-image-2",
        "prompt": "a tiny red apple on a clean white background, studio product photo",
        "size": "1024x1024",
        "n": 1,
    }
    resp = _post("/images/generations", payload)
    items = resp.get("data") or []
    if not items or not items[0].get("b64_json"):
        sys.exit(f"FAIL: {json.dumps(resp)[:400]}")
    n = _save_b64(str(out), items[0]["b64_json"])
    print(f"OK gpt-image-2 reachable. saved {out} ({n:,} bytes).")


def main() -> None:
    p = argparse.ArgumentParser(description="pockgo image client")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="generate one image")
    g.add_argument("--model", default="gpt-image-2",
                   help="image model (default: gpt-image-2 — verified 2026-05 on pockgo, accepts 2048x1152, ~80s render, more reliable than -2k which is currently overloaded; pass --model gpt-image-2-2k to opt in)")
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    g.add_argument("--out", required=True, help="output png path")
    g.add_argument("--size", default="1792x1024", help="OpenAI-style size, e.g. 1792x1024 (16:9)")
    g.add_argument("--aspect", default="16:9", help="aspect ratio for chat-multimodal models")
    g.add_argument("--reference", help="path to a reference PNG (image-to-image; chat models only)")
    g.add_argument("--n", type=int, default=1)
    g.add_argument("--backend", choices=["pockgo", "openai", "gemini", "comfyui"], default="pockgo",
                   help="image generation backend (default: pockgo relay)")
    g.add_argument("--comfyui-url", default=COMFYUI_URL,
                   help="ComfyUI server URL (when --backend comfyui)")
    g.add_argument("--comfyui-workflow", default="vendor/comfyui/workflow-t2i.json",
                   help="path to ComfyUI workflow JSON (API format)")
    g.add_argument("--comfyui-quality", default="high",
                   help="quality input for OpenAIGPTImage1 node: low / medium / high / auto")
    g.add_argument("--comfyui-timeout", type=int, default=300,
                   help="max seconds to wait for ComfyUI to finish a job")
    g.add_argument("--comfyui-api-key", default="",
                   help="ComfyUI platform API key (or set env COMFY_API_KEY); required for cloud nodes like OpenAIGPTImage1")
    g.set_defaults(func=cmd_generate)

    m = sub.add_parser("models", help="list image-capable models")
    m.set_defaults(func=cmd_models)

    h = sub.add_parser("health", help="cheap end-to-end test image")
    h.set_defaults(func=cmd_health)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
