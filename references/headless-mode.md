# Headless Mode — No Terminal, No Scripts

When the agent's environment has NO terminal access (e.g. Claude.ai web, API-only
Codex, mobile chat), the Python script pipeline (`build_with_qa.py`, `image_client.py`,
`render_screenshot.py`) is unavailable. This mode defines the degraded-but-still-useful
alternative: the agent writes everything as text artifacts and the user runs external
tools manually.

## Detection (before Auto-Run step 1)

Ask silently: "Can I execute `python scripts/…` in this session?"

| Signal | Mode |
|--------|------|
| `run_in_terminal` tool available + Python found | **FULL** (use scripts normally) |
| No terminal tool, but image generation tool available | **HEADLESS_GEN** (generate images in-session, manual QA) |
| No terminal AND no image tool | **HEADLESS_PROMPT_ONLY** (output prompt packs only) |

Tell the user which mode is active in one line at the end of step 1.

## Auto-Run Step Changes

For brevity, only the steps that CHANGE are listed. All unchanged steps
run identically to FULL mode.

| Step | FULL mode | HEADLESS mode |
|------|-----------|---------------|
| **1. Capability check** | Detect image model + scripts available | Same, but also note "scripts unavailable — HEADLESS mode" |
| **6. Asset routing** | Route to IMAGE_AS_PAGE / IMAGE_MODEL+OVERLAY / etc. | All lanes collapse to **PROMPT_PACK_ONLY**: write prompts + layout.json files; user runs image generation externally |
| **10. Closed-loop overlay QA** | `build_with_qa.py` auto loop | Agent performs **Manual QA Checklist** (below) by visually inspecting the rendered page if multimodal, or by checking layout.json against prompt rules if not |

## Manual QA Checklist (replaces `build_with_qa.py` in HEADLESS mode)

For each page, after the user has generated the background image and you have
access to the rendered result (either as an uploaded screenshot or as a multimodal
view), verify these 10 items. Mark each PASS or FAIL.

### 1. OCCLUSION — Device mockup clear?
- [ ] No overlay text (title, desc, KPI, label) sits ON TOP of the device mockup / phone screen / laptop bezel.
- [ ] The device is fully visible; its UI is not covered by HTML text boxes.
- **FAIL if**: any character of overlay text overlaps the device.

### 2. TEXT COMPLETENESS — Any truncation?
- [ ] Every text field renders its full content without `…` or cut-off words.
- [ ] Container width ≥ longest line at its font-size.
- **FAIL if**: any word is incomplete or missing.

### 3. IMAGE-TEXT CORRESPONDENCE — Does the copy match what's visible?
- [ ] Overlay copy references ONLY UI elements that are actually visible in the image.
- [ ] If desc mentions "评论", there IS a comment area in the screen.
- [ ] If desc mentions a specific number/color/label, it MATCHES the in-image UI.
- **FAIL if**: overlay invents UI elements not in the image.

### 4. ALIGNMENT — Same column = same edge?
- [ ] All elements in the same column share the same x or right-edge.
- [ ] Vertically adjacent elements have consistent gap (no ±20px drift).
- [ ] Section labels align with their title below them.
- **FAIL if**: two elements claiming the same column are ≥8px misaligned.

### 5. CONTRAST — Readable at arm's length?
- [ ] Light text on dark BG: minimum 4.5:1 ratio.
- [ ] Dark text on light BG: minimum 3:1 (display), 4.5:1 (body).
- [ ] Muted annotations (#9E94A8 on #1F1326) are still legible.
- **FAIL if**: a reasonable person would squint to read it.

### 6. PAGE PATTERN — Does the layout match the declared pattern?
- [ ] The overlay geometry (left column / right column / top strip / split / centered) matches the `page_pattern` declared in the deck plan.
- [ ] Two adjacent pages don't share the same pattern.
- **FAIL if**: pattern doesn't match or repeats adjacently.

### 7. KPI HONESTY — Numbers are real or marked?
- [ ] Every KPI tile's number either comes from user-supplied data OR is marked `[concept data]`.
- [ ] No invented percentages, user counts, or revenue figures.
- **FAIL if**: unmarked fake KPI found.

### 8. BREATHING REGION — Is the declared white space actually empty?
- [ ] The `breathing_region` declared in the prompt is free of overlay text, device chrome, and props.
- [ ] The region reads as deliberate negative space, not as "we forgot to put something there".
- **FAIL if**: overlay text or key props intrude into the breathing region.

### 9. INFORMATION COMPLEMENTARITY — Title ≠ Desc ≠ Annotations?
- [ ] The title, subtitle, description, and annotations each add NEW information.
- [ ] The description doesn't just restate the title in longer words.
- [ ] Annotations call out specific details, not generic praise.
- **FAIL if**: any two text blocks could swap positions without loss of meaning.

### 10. DENSITY TIER — Does the page feel like its declared tier?
- [ ] `spacious`: 1 device, 0 fragments, ≥50% negative space → feels airy.
- [ ] `balanced`: 1 device + 1 fragment, ~35% negative space → feels composed.
- [ ] `magazine-dense`: 1 device + 3-4 orbiting fragments, ≤25% negative space → feels rich.
- **FAIL if**: the page's visual density clearly contradicts its declared tier.

### Scoring

| PASS count | Verdict |
|------------|---------|
| 10/10 | ✅ Ship it |
| 8-9/10 | ⚠️ Fix MINORs, no re-roll needed |
| 6-7/10 | 🔴 Fix before shipping |
| ≤5/10 | 🔴 Regenerate image + layout |

Record the checklist result in a `<page>.manual-qa.json` alongside the layout:

```json
{
  "mode": "headless",
  "score": 9,
  "pass": true,
  "checks": {
    "occlusion": "pass",
    "text_completeness": "pass",
    "image_text_correspondence": "pass",
    "alignment": "pass",
    "contrast": "pass",
    "page_pattern": "pass",
    "kpi_honesty": "pass",
    "breathing_region": "pass",
    "info_complementarity": "fail",
    "density_tier": "pass"
  },
  "fail_detail": "Title '陪跑，不再独跑' and desc paragraph overlap in meaning — desc restates title rather than adding new evidence.",
  "fix": "Rewrite desc to focus on a specific interaction detail not mentioned in the title."
}
```

## PROMPT_PACK_ONLY Deliverable

When the agent can neither run scripts NOR generate images (HEADLESS_PROMPT_ONLY),
the final deliverable is a directory of text artifacts the user can feed into
external tools:

```
generated-images/<project-slug>/
├── README.md                  # How to use this prompt pack
├── padb.md                    # Project Art Direction Block (palette, fonts, rules)
├── deck-plan.md               # Per-page table with narrative_role + page_pattern
├── prompts/
│   ├── 01-cover.txt           # Prompt text only, ready to paste into image model
│   ├── 02-case-01.txt
│   └── ...
├── layouts/
│   ├── 01-cover.layout.json   # Multi-zone overlay layout
│   └── ...
└── manual-qa/
    ├── 01-cover.manual-qa.json # Filled after user generates image + sends back
    └── ...
```

The README.md must tell the user:
1. Which image model to use (from capability check or user preference)
2. Canvas size (2048x1152)
3. How to run the prompt (paste → generate → save as 01-cover.png)
4. How to apply the layout (if they have a way to render HTML overlays)
5. How to send back results for manual QA
