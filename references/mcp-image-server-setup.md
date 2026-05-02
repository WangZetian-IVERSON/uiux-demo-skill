# MCP Image Server Setup (verified 2026-04)

Practical, China-friendly setup for calling real image-generation models from VS Code via MCP. All notes below are field-verified — they fix specific failures we have hit and recovered from.

## Recommended Server Mix

Install all three; route per use case:

```jsonc
// .vscode/mcp.json
{
  "servers": {
    "imagen": {
      "// 用途": "Imagen 4 / 4 Ultra / 4 Fast — 真实静物 / 氛围 / 海报 / 拉丁文 UI",
      "command": "cmd",
      "args": [
        "/c", "npx", "-y", "gemini-imagen-mcp-server",
        "--model", "imagen-4",
        "--output-dir", "test-output/assets",
        "--batch", "--max-batch-size", "4"
      ],
      "env": {
        "GEMINI_API_KEY": "<key>",
        "HTTP_PROXY": "http://127.0.0.1:7890",
        "HTTPS_PROXY": "http://127.0.0.1:7890",
        "ALL_PROXY": "http://127.0.0.1:7890",
        "NODE_USE_ENV_PROXY": "1"
      }
    },
    "nano-banana-pro": {
      "// 用途": "Gemini 3 Pro Image / Nano Banana Pro — 备用,中文文字稍优于 Imagen",
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@zhibinyang/nano-banana-mcp"],
      "env": {
        "GEMINI_API_KEY": "<key>",
        "MODEL": "gemini-3-pro-image",
        "ASPECT_RATIO": "16:9",
        "RESOLUTION": "2K",
        "HTTP_PROXY": "http://127.0.0.1:7890",
        "HTTPS_PROXY": "http://127.0.0.1:7890",
        "ALL_PROXY": "http://127.0.0.1:7890",
        "NODE_USE_ENV_PROXY": "1"
      }
    }
  }
}
```

## Five Failure Modes And Their Fixes (in install order)

### 1. 400 `User location is not supported for the API use`
**Cause**: Gemini API geo-blocks China mainland + HK.
**Fix**: route the MCP subprocess through an HTTP proxy with a non-CN exit. Set `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY` in the server's `env` block.

### 2. Proxy env vars set but still 400
**Cause**: Node 18+ global `fetch` (undici) does NOT honor `HTTP_PROXY` / `HTTPS_PROXY` env vars by default. Curl in the same terminal works; the MCP subprocess does not.
**Fix**: add `"NODE_USE_ENV_PROXY": "1"` to the env block (Node 24+ feature). For older Node, enable system-wide proxy / TUN mode in Clash so all TCP traffic is routed at the OS level regardless of env vars.

### 3. 404 `models/imagen-4.0-ultra-generate-preview-06-06 is not found`
**Cause**: Many published MCP packages hardcode 2025-06 preview model IDs that have been retired. As of 2026-04 the live IDs are:
- `models/imagen-4.0-generate-001`
- `models/imagen-4.0-ultra-generate-001`
- `models/imagen-4.0-fast-generate-001`
- `models/imagen-3.0-generate-002`

**Verification command**:
```powershell
curl.exe -s "https://generativelanguage.googleapis.com/v1beta/models?key=<KEY>" | ConvertFrom-Json | Select-Object -ExpandProperty models | Where-Object { $_.name -like "*imagen*" }
```

**Fix (npx-cached package)**: locate and patch in place.
```powershell
$cache = npm config get cache
$pkg = Get-ChildItem -Path "$cache\_npx" -Recurse -Filter "index.js" | Where-Object { $_.FullName -like "*<package-name>*" } | Select-Object -First 1 -ExpandProperty FullName
(Get-Content $pkg -Raw) `
  -replace 'imagen-4\.0-generate-preview-06-06', 'imagen-4.0-generate-001' `
  -replace 'imagen-4\.0-ultra-generate-preview-06-06', 'imagen-4.0-ultra-generate-001' `
  | Set-Content $pkg -NoNewline
```
Restart the MCP server in VS Code (Command Palette → `MCP: Restart Server`).

### 4. 429 `Your project has exceeded its monthly spending cap`
**Cause**: Imagen 4 / Ultra / Fast are NOT in the free tier. The project's spend cap on AI Studio is at the default $0.
**Fix**: open https://ai.studio/spend → confirm the project name in the top dropdown matches the project that owns the API key (check at https://aistudio.google.com/app/apikey) → bind a credit card if needed → raise the spend cap (USD $5 covers a full portfolio deck). Wait ~1–2 minutes for propagation.
**Cost ballpark (2026-04)**: imagen-4 ≈ $0.04/img, imagen-4-ultra ≈ $0.06/img, imagen-4-fast ≈ $0.02/img, Nano Banana Flash ≈ $0.04/img.

### 5. Tool returns `must NOT have additional properties`
**Cause**: Many MCP image servers expose only `{ prompt }` (or `{ prompts: string[] }`) as the tool schema. Model / aspect ratio / negative prompt are configured via CLI flags at server startup, not per-call.
**Fix**: pass model / aspect ratio / batch settings as `args` when registering the server in `.vscode/mcp.json`. To switch models mid-deck, register multiple server instances with different flags (one for `imagen-4`, one for `imagen-4-ultra`, etc.).

## Lane Routing Cheat Sheet

| Use case | Server | Why |
|----------|--------|-----|
| Cover hero (Chinese title overlaid in HTML) | `imagen` (imagen-4 or ultra) | Best photoreal product still-life, clean negative-space composition |
| Section cover, atmospheric backdrop | `imagen` | Same as above |
| 3D prop / staged object | `imagen` or `nano-banana-pro` | Both work; Pro slightly better for complex multi-object scenes |
| Editorial campaign poster (no text in image) | `imagen-4-ultra` | Strongest prompt adherence on intricate compositions |
| **Mobile UI screen with Chinese / CJK text** | `pockgo` (`gpt-image-2`) | Verified 2026-05: gpt-image-2 renders CJK labels cleanly. Hand-built HTML UI in `references/html-ui-screen-lane.md` is now a fallback only. |
| **Dashboard / chart / KPI grid** | **NONE — hand-build HTML/SVG** | Image models cannot render numbers and labels reliably |
| Logo, real shipped UI screenshot | **NONE — use real asset** | Honesty rule |

## Verification Routine After Any Change

Run this once after installing/restarting any image MCP, before the actual deck work:

```text
1. health_check → expect ✅ + correct default model + correct output dir
2. list_models → expect Imagen 4 family or Nano Banana family present
3. Generate one cheap test image (simple still life, no text) → expect PNG saved to output dir
4. Open the PNG, eyeball: real photoreal output (not a placeholder, not garbled)
```

Only after all four pass should batch generation begin.

---

## Provider B: pockgo HTTP Relay (verified 2026-05, China-friendly, no proxy needed)

A China-accessible OpenAI-compatible relay that exposes `gpt-image-2`, `gpt-image-2-2k`, `gpt-image-2-4k`, `nano-banana-pro` (+ `2k` / `4k`), `gemini-3-pro-image-preview` (+ `2k` / `4k`), `flux-2-pro`, `grok-imagine-image`, and ~221 chat models. Use this when the AI Studio path is blocked, when you do not want to run a proxy, or when you need gpt-image-2 specifically.

### Endpoint

```text
Base URL:   https://newapi.pockgo.com/v1
Image gen:  POST /images/generations    (OpenAI-compatible)
Chat+image: POST /chat/completions      (Gemini-style multimodal, see below)
List models: GET  /models
Auth:       Authorization: Bearer <key>
```

### Hard requirement: User-Agent

The relay sits behind Cloudflare. **Requests without a browser-like `User-Agent` header return `403 error code: 1010`.** Python's default `Python-urllib/x.y` is blocked. Always send:

```text
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36
Accept: application/json
```

### Minimal text-to-image (gpt-image-2)

```bash
curl.exe -s -X POST "https://newapi.pockgo.com/v1/images/generations" \
  -H "Authorization: Bearer $POCKGO_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0 ..." \
  -d '{
    "model": "gpt-image-2",
    "prompt": "...",
    "size": "1024x1024",
    "n": 1
  }'
```

Response: `{ created, data: [ { b64_json, revised_prompt } ] }`. No `url`, only base64 — decode and write to `generated-images/{project_slug}/...png`.

### Aspect ratio for image-first deck pages (16:9 at 2048x1152)

`gpt-image-2` accepts `size`. For our 2048x1152 canvas, request `"size": "1792x1024"` (closest 16:9 supported) and upscale via `gpt-image-2-2k` if needed. Or call `gpt-image-2-4k` once and downscale.

For `nano-banana-pro` / `gemini-3-pro-image-preview` use the chat-completions endpoint with the `extra_body.imageConfig.aspectRatio` trick:

```jsonc
{
  "extra_body": { "imageConfig": { "aspectRatio": "16:9" } },
  "model": "gemini-3-pro-image-preview-2k",
  "messages": [
    { "role": "system", "content": "{\"imageConfig\": {\"aspectRatio\": \"16:9\"}}" },
    { "role": "user", "content": [
        { "type": "text", "text": "<PADB + page recipe>" }
    ]}
  ]
}
```

For image-to-image (reference chaining for consistency per `references/visual-consistency.md`), pass the previously generated cover as `image_url` (either `https://` URL or `data:image/png;base64,<b64>`):

```jsonc
{
  "role": "user",
  "content": [
    { "type": "text", "text": "<PADB + page recipe>" },
    { "type": "image_url", "image_url": { "url": "data:image/png;base64,..." } }
  ]
}
```

### Production client

Use `scripts/image_client.py` (in this repo). It encapsulates: UA header, key from env (`POCKGO_KEY`), retry on Cloudflare 1010, b64 decode + save, optional reference-image chaining, PADB injection. CLI:

```powershell
$env:POCKGO_KEY = "sk-..."
python scripts/image_client.py generate `
  --model gpt-image-2 `
  --prompt-file prompts/cover.txt `
  --size 1792x1024 `
  --out generated-images/finance-saas/cover.png

python scripts/image_client.py generate `
  --model gemini-3-pro-image-preview-2k `
  --aspect 16:9 `
  --prompt-file prompts/section-01.txt `
  --reference generated-images/finance-saas/cover.png `
  --out generated-images/finance-saas/section-01.png
```

### Capability sanity test

```powershell
$env:POCKGO_KEY = "sk-..."
python scripts/test_gpt_image_2.py
```

Expected: `HAS_B64: True`, file ~1MB+ saved, image opens as a real photo. If `HTTP 403 error code: 1010`, your UA header is missing.

### Pockgo failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `403 error code: 1010` | Missing/blocked User-Agent | Send a browser UA |
| `model not found` | Typo or wrong tier suffix | `GET /v1/models` to list; suffix must be `-2k` / `-4k` exactly |
| `data` is empty, no error | Prompt rejected by upstream safety filter | Soften prompt or switch model |
| Times out / hangs | Upstream Gemini / OpenAI region instability | Retry with same key; the relay does not require user proxy |
| `usage: null` | Relay does not surface token counts | Ignore; charge is per-image on the relay's own meter |
