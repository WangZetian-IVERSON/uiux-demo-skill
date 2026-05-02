# Closed-Loop Overlay QA

The final mandatory step before any multi-zone overlay page is delivered.

## Why

`layout_fitter.py` only knows geometry + contrast. It cannot tell you that:

- the overlay copy claims "评论" but the rendered UI shows no comment area
- the description references "美食视频" but the UI image has only static photos
- a label is technically inside its box but visually hidden behind a device bezel
- two columns appear aligned in numbers but look uneven after font rendering
- a small annotation has insufficient contrast against the BG color

These are the issues that make a deck feel "almost right but somehow off."
A vision LLM can spot them in one shot.

## Pipeline (3 scripts)

```
build_interactive_page.py  ─┐
   --mode multi-zone        │   builds   page.html      (overlay HTML)
                            │
render_screenshot.py    ────┤   shoots   page-rendered.png   (Chromium 2048x1152)
                            │
overlay_qa.py / build_with_qa.py  reviews  →  page.qa.json   (vision LLM verdict)
                            │              ↻ if issues → patch layout, re-run
                            ▼
                        FINAL: page.html + page.qa.json (pass=true)
```

## Scripts

### `scripts/render_screenshot.py`
Headless-Chromium screenshot of any HTML page at 2048x1152.

```powershell
python scripts/render_screenshot.py `
  --html  generated-images/<deck>/<page>.html `
  --out   generated-images/<deck>/<page>-rendered.png
```

### `scripts/overlay_qa.py`
Single-shot vision QA. Submits the screenshot + layout.json + page intent to the
configured vision model. Outputs strict JSON: score / pass / retake_image /
issues[] / summary.

```powershell
$env:POCKGO_KEY        = "<key>"
$env:OVERLAY_QA_MODEL  = "claude-sonnet-4.5"   # default; gemini-2.5-flash too lenient
python scripts/overlay_qa.py `
  --rendered generated-images/<deck>/<page>-rendered.png `
  --layout   generated-images/<deck>/<page>.layout.json `
  --intent   "Case 01 圈子首页 case-study：左栏文案 / 中央 iPhone / 右栏注释" `
  --out      generated-images/<deck>/<page>.qa.json
```

### `scripts/build_with_qa.py` (recommended — full closed loop)
Wraps build → shot → QA → (LLM-suggested layout fix) → rebuild → re-QA.
Stops when `pass=true` AND no `blocker|major` issues, or after `--max-iters`.

```powershell
$env:PYTHONIOENCODING  = "utf-8"
$env:POCKGO_KEY        = "<key>"
$env:OVERLAY_QA_MODEL  = "claude-sonnet-4.5"
python scripts/build_with_qa.py `
  --image    generated-images/<deck>/<page>.png `
  --layout   generated-images/<deck>/<page>.layout.json `
  --html     generated-images/<deck>/<page>.html `
  --rendered generated-images/<deck>/<page>-rendered.png `
  --intent   "<one-line page intent — what's in the layout, what BG, what intent label>" `
  --title    "<page title>" `
  --max-iters 3
```

Side effects each iteration:
- `<page>.layout.json.iter1`, `.iter2`, … (history)
- `<page>.html.iter1`, …
- `<page>-rendered.png.iter1`, …
- `<page>.layout.qa.iter1.json`, …
- `<page>.layout.json.seed.bak` (one-time backup of original)
- final QA written to `<page>.qa.json`
- exit code 0 = passed, 1 = exhausted iters, 2 = retake_image=true (regenerate the underlying ComfyUI image, not the overlay)

## QA contract (severity rules)

The vision model is instructed:

| severity | trigger | example |
|---|---|---|
| **blocker** | overlay text covers the device mockup / hides UI; canvas broken | desc box overlaps phone screen |
| **major**   | overlay copy claims a UI element that's NOT visible in the image, contradicts visible UI text, mentions concrete details (food / video / specific labels) absent from the screen, **or any character of overlay text is occluded by the device mockup / a glassmorphism callout / another overlay (text content lost or hard to read = MAJOR, never minor)**, or text is truncated / overflowing the box | "点赞了哪条美食视频" but UI shows static photos; left desc text covered by phone bezel |
| **minor**   | low contrast, slightly tight spacing, wording could be tighter | annotation at #9E94A8 on #1F1326 |

**Critical**: occlusion-of-text is **always MAJOR**, even if "only a few characters" are hidden.
The closed loop's pass gate excludes major, so misclassifying occlusion as minor lets a broken page through.
When in doubt about "is this readable?" — escalate one severity level.

**Pass gate**: `pass=true` AND zero `blocker|major`. Minor issues are acceptable.

`retake_image=true` ONLY when the underlying generated image is unusable
(garbled UI, wrong device, wrong theme, no readable text). In that case the
loop exits with code 2 and the agent must regenerate the image via ComfyUI
following `image-prompt-style-uiux.md`.

## Default model

`claude-sonnet-4.5` via pockgo relay. Verified 2026-05:
- gpt-4o → 503 model_not_found on most pockgo keys
- gemini-2.5-flash → too lenient, hallucinates phantom truncation
- claude-sonnet-4.5 → 6/6 hit rate on real issues, 0 hallucinations in our test

Override with `$env:OVERLAY_QA_MODEL`.

## When to use which script

| Situation | Use |
|---|---|
| One-off check on an existing rendered page | `overlay_qa.py` |
| Build a new page from layout.json (production path) | `build_with_qa.py` (gives closed loop for free) |
| Already iterated manually, want a final verdict | `overlay_qa.py` |
| Deck-wide batch | shell loop over `build_with_qa.py`, each page in turn |

## Failure modes & remedies

- **HTTP 503 model_not_found** → switch `OVERLAY_QA_MODEL` to a model your key has access to (list via `curl /v1/models`).
- **HTTP 403 / Cloudflare 1010** → the pockgo relay rejects bare urllib UA; both scripts already inject Chrome UA.
- **GBK encode error on Windows console** → set `$env:PYTHONIOENCODING = "utf-8"` before running.
- **Loop never converges (3 iters all fail)** → the LLM-patched layout introduced new issues. Inspect `<page>.layout.qa.iter*.json`, restore `<page>.layout.json.seed.bak`, fix the seed manually.
- **`retake_image=true`** → don't keep iterating overlays. Rewrite the prompt in `prompts/<page>.txt` per `image-prompt-style-uiux.md`, regenerate via ComfyUI, then re-enter the loop.

## `retake_image=true` rollback rule (exit code 2)

When `build_with_qa.py` exits with code 2 (`retake_image=true`), the underlying
generated image is unfixable by overlay tweaks. The agent MUST:

1. **Stop** — do NOT re-run `build_with_qa.py` on the same image.
2. **Rewind to step 6 (ASSET ROUTING) of the Auto-Run sequence** — not step 7
   (showcase-first). The image prompt itself is the failure point, not the
   downstream overlay.
3. **Diagnose the failure mode** from the QA JSON's `issues[].what`:
   - "屏内 UI garbled CJK" / "wrong device shown" / "no readable text" → image-model failure → keep prompt, change `seed` (auto-random in `image_client.py`, just rerun)
   - "BG color does not match deck_palette.bg" / "wrong intent label vibe" / "extra props (paper/coffee/desk) appeared" → prompt failure → rewrite prompt per [image-prompt-style-uiux.md](image-prompt-style-uiux.md), THEN regenerate
   - "image-model returned a 4-phone array but layout expects 1 device" → routing failure → switch to a different M-template (M1↔M3↔M6) and regenerate
4. **Regenerate the image** via the same ComfyUI invocation block from
   [image-generation-protocol.md](image-generation-protocol.md#comfyui-desktop-invocation-verified-default-for-this-workspace-2026-05).
   Up to 3 fresh seeds before escalating to a model change.
5. **Re-enter the closed loop** — re-run `build_with_qa.py` on the new image
   with the same `layout.json` (no manual overlay edits needed; layout was
   already correct).
6. **Hard cap**: if 3 image regenerations + 3 overlay loops each still fail,
   STOP and tell the user. Do not silently keep burning credits.

The agent MUST NOT:
- patch the layout to "work around" a bad image (e.g. enlarge an overlay to
  cover a garbled UI region — this hides evidence the user needs to see)
- mark the page as delivered when exit code = 2
- switch the QA model to a more lenient one to make `retake_image` go away

## Relation to other QA layers

| Layer | What it checks | When it runs |
|---|---|---|
| `references/visual-consistency.md` 5-axis QA | cross-page palette / device / typography drift | after showcase 3 pages |
| `layout_fitter.py` rules | per-zone geometry, header/footer safe zones, contrast flip | between zones.json and layout.json |
| **closed-loop overlay QA (this doc)** | image-text correspondence, occlusion, readability of the *final rendered page* | after build_interactive_page, BEFORE delivery |
| `references/quality-review.md` | deck-level narrative, copy quality, KPI honesty | before final handoff to user |

The closed-loop QA sits at the seam between layout and delivery. It is the only
layer that sees the final pixels.
