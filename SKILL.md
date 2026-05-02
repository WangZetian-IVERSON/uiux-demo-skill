---
name: uiux-portfolio-deck
description: Create, critique, or refine UI/UX portfolio decks and product design case-study presentations from project notes, app screenshots, dashboard screenshots, screen recordings, reference decks, or local visual corpora. Use for UIUX portfolio, design portfolio, case study deck, product design review deck, interaction design proposal, product redesign story, dashboard design presentation, visual system appendix, or polished dark-tech portfolio work inspired by local uxui template references.
---

# UI/UX Portfolio Deck

## Auto-Run On Every Invocation

When this skill is invoked, IMMEDIATELY run this fixed sequence without waiting for the user to ask. Do not require the user to recite rules — the skill drives the flow.

```text
0. OPENING CHECKLIST — if the brief is missing any of {project domain, target audience, real screenshots vs proposal, named style or palette, page count target, delivery format, **inline-editability of titles in browser (Y/N — see `references/editable-image-as-page.md`)**}, batch-ask ALL the missing items in ONE message and wait for the user to answer them in one round. Do not start image generation, asset scans, or PADB while questions are open. Inspired by huashu's Junior Designer workflow: ask everything once, then go heads-down. If the brief is already complete, skip to step 1 silently.
1. CAPABILITY CHECK — detect the real image-generation tool available in this session (per references/image-generation-protocol.md). State the model name in one line.
2. ASSET SCAN — quickly scan the workspace and the user's message for real screenshots, logos, brand colors, project facts. State what was found. If a real public brand / company / product / platform is named (e.g. "京东 / 美团 / 抖音 / 飞书"), ALSO run `references/asset-and-fact-protocol.md` once before any visual decision — verify name, version, current visual identity, and never invent claims about the real entity. **When a real brand is involved, MUST produce a `brand-spec.md` at the deck root via the 5-step protocol (ask → search official brand page → download SVG/HTML/screenshot → grep hex codes → freeze spec + CSS variables). Every later prompt and HTML page MUST reference brand-spec.md — never quote brand colors from memory.** If the named company is the **delivery target** of this deck (a portfolio submitted TO that company), apply the Brand Distance rule from `references/asset-and-fact-protocol.md`: deck primary color must NOT be that company's brand color, and the deck must not cosplay the company's identity.
3. SCOPE DECIDE — pick FULL_CASE_STUDY, VISUAL_PROPOSAL, or CRITIQUE based on what is available (default to VISUAL_PROPOSAL if no real screenshots).
3.5. PICK NARRATIVE ARCHETYPE — per `references/deck-narrative-architecture.md`, choose ONE archetype from {A1 argument-arc, A2 before-after-comparison, A3 option-tradeoff, A4 process-journey, A5 system-anatomy, A6 single-screen-deep-dive}. Use the decision tree in that file. Then write a per-page table `{page_id, narrative_role, page_pattern, why_this_page, needs_real_data}` and **show it to the user for one-round confirmation BEFORE writing deck-plan.json or burning any image credits**. Adjacent pages MUST NOT share the same page_pattern. KPI tiles are forbidden unless the user supplied real numbers OR archetype is A2.
4. STYLE PICK — **first check User-Authored Input Priority (see section below)**. If the user already named a style, pasted a palette, supplied a reference image, or wrote their own image prompt, do NOT propose alternatives — record their input verbatim and skip to step 5. Only when the brief is genuinely vague (no named style, no palette, no reference) propose 2–3 differentiated visual directions tied to the project domain.
5. LOCK ART DIRECTION — write the Project Art Direction Block (PADB) per references/visual-consistency.md and save it at the top of the working file. The PADB is the **design spec** (palette, fonts, device_lock, forbidden vocabulary, text_safe_zones) — it informs every visual decision. **Prompt format is chosen per page type**: UIUX pages (cover/case-study/anatomy/process/system/hero) MUST use the 5-sentence Chinese structure + 6 intent-label dictionary from `references/image-prompt-style-uiux.md` (and MUST NOT use `image-style-presets.md`). Poster/brand/editorial pages MAY use the preset-first lean mode from `references/image-generation-protocol.md`. Never paste the full PADB text block into a prompt — let the chosen format carry the instructions.
6. ASSET ROUTING — for each planned page, decide its production lane: IMAGE_AS_PAGE (covers, case-study heroes, key visuals where typography composition IS the design — image carries text, OCR overlays make titles clickable; see `references/image-first-deck-workflow.md` Variant section), **IMAGE_AS_PAGE_EDITABLE (same architecture but the left typography zone is left as a flat <BG_HEX> block in the image; HTML overlay renders the editable title/desc/KPI on top — use when the user said "yes" to inline-editability in step 0; see `references/editable-image-as-page.md`)**. **Whenever a page is routed to IMAGE_AS_PAGE the agent MUST read `references/image-as-page-prompt-recipe.md` and fill all 7 mandatory slots before sending the prompt — this is the quality contract that separates the lumen-2K editorial baseline from generic AI output. For IMAGE_AS_PAGE_EDITABLE the agent MUST also read `references/editable-image-as-page.md` and replace the LEFT TYPOGRAPHY ZONE slot per that file's rule.** IMAGE_MODEL+OVERLAY (standard layered: full-bleed bg + HTML text/links — for content-dense or navigation pages), HTML_DASHBOARD (data screens, admin, B-side, dashboards — per `references/dashboard-rendering.md`), POSTER_BATCH (campaign visuals appendix), or REAL_SCREENSHOT (user-supplied). Default image model is configurable via `BACKEND_IMAGE_MODEL` env (current default: `gpt-image-2`, verified 2026-05; CJK clean; ~1.2MB/page; ~80s render). Opt up to `gpt-image-2-2k` only when the relay is healthy — it has been intermittently overloaded with HTTP 524 in 2026-05. Fallback to HTML_UI_SCREEN per `references/html-ui-screen-lane.md` only when the available image model garbles CJK. State the routing for each page in one line.
7. SHOWCASE FIRST — generate the cover (4 candidates, pick 1), then 1 section cover, then 1 hero 3D prop, then 1 concept screen OR 1 dashboard mockup depending on the deck's dominant page type. Use the chosen cover as the reference image for all subsequent IMAGE_MODEL generations when the model supports it. STOP and run the 5-axis consistency QA from references/visual-consistency.md.
8. CONFIRM — show the showcase contact sheet to the user. If grammar/consistency is approved, proceed. If not, revise the PADB and regenerate.
9. EXPAND — batch-produce the remaining pages following the per-page routing. Apply references/analysis-depth.md to every analysis page (problem, competitive, strategy, IA, comparison, outcome). Every image prompt MUST respect the PADB's palette + fonts + forbidden vocabulary, and MUST use the correct prompt format for the page type: `image-prompt-style-uiux.md` for UIUX pages, `image-generation-protocol.md` preset-first path for poster/brand pages.
10. CLOSED-LOOP OVERLAY QA — after `build_interactive_page.py --mode multi-zone` produces the HTML for each page, the agent MUST run `scripts/build_with_qa.py` (or invoke `scripts/render_screenshot.py` + `scripts/overlay_qa.py` manually) to: (a) screenshot the rendered HTML at 2048x1152, (b) submit it + the layout.json + a one-line page intent to the vision QA model (default `gpt-4o`, configurable via `BACKEND_QA_MODEL` env; see `scripts/config.py`), (c) parse the JSON report, (d) if `pass=false` or any issue is `severity=blocker|major`, regenerate a revised layout.json from the LLM and re-render, up to `--max-iters 3`. A page with unresolved blocker/major issues MUST NOT be included in the final deck. The final QA JSON is saved next to the layout file as `<name>.qa.json`. See `references/closed-loop-overlay-qa.md` for the full contract — including the `retake_image=true` rollback rule (exit code 2 → rewind to step 6, regenerate the image, do NOT patch the overlay). Layout JSON schema lives in `references/overlay-layout-spec.md`; for a copy-pasteable end-to-end template see `references/example-fit-checkin-walkthrough.md`.
10. FINAL QA — run the 5-axis visual consistency QA on the full asset pool AND the analysis-depth self-check on every reasoning page before composing the deck.
```

The user should be able to type one short sentence ("做一份财务 SaaS 作品集") and get the right deck. They should NOT have to specify capability checks, asset gates, or showcase-first — the skill enforces those automatically.

## Configuration (scripts/config.py)

All Python scripts in `scripts/` read backend connection details from environment variables via `scripts/config.py`. No URLs, keys, or model names are hardcoded in the scripts themselves.

| Variable | Default | Purpose |
|---|---|---|
| `BACKEND_API_KEY` | (falls back to `POCKGO_KEY`) | API key for the active backend |
| `BACKEND_BASE_URL` | `https://newapi.pockgo.com/v1` | Base URL of the OpenAI-compatible relay |
| `BACKEND_IMAGE_MODEL` | `gpt-image-2` | Default image generation model |
| `BACKEND_QA_MODEL` | `gpt-4o` (falls back to `OVERLAY_QA_MODEL`) | Vision QA model for overlay review |
| `COMFY_API_KEY` | — | ComfyUI platform key (separate path) |
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI Desktop server |

**Legacy env vars** (`POCKGO_KEY`, `OVERLAY_QA_MODEL`, `COMFY_API_KEY`) continue to work — they are read as fallbacks. To switch to a different provider (e.g., direct OpenAI), set:

```powershell
$env:BACKEND_BASE_URL = "https://api.openai.com/v1"
$env:BACKEND_API_KEY  = "sk-your-openai-key"
```

The scripts (`image_client.py`, `build_with_qa.py`, `overlay_qa.py`, `ocr_hotspots.py`) all import from `config.py` and require zero changes to work with a new backend.

## Operating Mode (FULL vs HEADLESS)

The skill auto-detects whether terminal/script access is available. At the end of step 1, state the active mode in one line.

### FULL mode (terminal + Python + scripts available)

Run the 10-step Auto-Run sequence as written. All scripts are available for image generation, overlay building, and closed-loop QA.

### HEADLESS mode (no terminal access — Claude.ai web, API-only, etc.)

**Detection**: `run_in_terminal` tool is absent OR Python is not available.

**What changes**: Read `references/headless-mode.md` for the full degradation path. In summary:
- Step 6: All asset lanes collapse to `PROMPT_PACK_ONLY` — the agent writes prompt `.txt` files + `layout.json` files; the user runs image generation externally.
- Step 10: Replace `build_with_qa.py` with the **Manual QA Checklist** (10 visual checks) from `references/headless-mode.md`. The agent performs this by inspecting the rendered page visually (if multimodal) or by comparing layout.json against prompt rules (if text-only). Record result in `<page>.manual-qa.json`.
- Deliverable: A prompt pack directory (`prompts/` + `layouts/` + `README.md`) the user feeds into their own image tool, plus manual QA for every page they send back.

**Minimum viable deliverable**: Even in the worst case (no terminal, no image tool, no multimodal vision), the agent MUST output prompt packs + layout.json files + the Manual QA Checklist for the user to self-review.

## Hard Rules (the skill enforces these silently; do not negotiate)

These rules override any "looks fine" judgement. Violating them is the #1 cause of low-quality output.

**MUST**

1. MUST run the Auto-Run sequence above on every invocation.
2. MUST deliver the deck via the **image-first HTML deck workflow** per `references/image-first-deck-workflow.md`. Each page = full-bleed image-model background + HTML text/link overlay + huashu deck_stage.js navigation. Do not write CSS portfolios as the main visual.
3. MUST detect the actual image-generation capability and prefer real image generation aggressively. Generate covers, section covers, scenes, AND in-frame concept UI screens. Never paint UI in CSS as a substitute.
4. MUST write a Project Art Direction Block (PADB) per `references/visual-consistency.md` BEFORE generating image #1, including the image-first additions (in_image_ui_style, device_lock, text_safe_zones). Prefix every later image prompt with that exact PADB. Pass the chosen cover as a reference image to subsequent prompts whenever the model supports it.
5. MUST follow `references/showcase-first-deck-workflow.md` for any deck of 5+ pages: generate cover + 1 section cover + 1 core-UI page first, run 5-axis consistency QA, get user confirmation, then expand.
6. MUST read `references/anti-ai-slop.md` before writing any HTML/CSS or image prompt.
7. MUST keep editable text out of the image. All Chinese titles, project names, contact info, and links live in the HTML text layer over the image. The image carries no editable Chinese text.
8. MUST keep evidence honest: a real shipped product UI must come from a real screenshot. Image-generated concept screens are fine in VISUAL_PROPOSAL mode and are labelled at deck level as "设计提案 / Visual Direction Proposal".

**NEVER**

1. NEVER render UI in HTML/CSS, screenshot it, and present it as a generated image. Generated images come from a real image model only.
2. NEVER fabricate metrics, user quotes, research findings, or business outcomes that the user did not provide.
3. NEVER reuse one project's generated assets in an unrelated project.
4. NEVER bake editable Chinese text into the background image. The image is a stage; the HTML carries the text.
5. NEVER produce the full deck in one shot when the deck is 5+ pages and the visual grammar/consistency has not been approved.
6. NEVER use the AI-slop visual vocabulary listed in `references/anti-ai-slop.md` (purple gradients, emoji icons, rounded-card-with-left-border, Inter as display, generic 4-phones-in-a-row layouts, etc.).
6. NEVER use lorem-ipsum / placeholder filler (`商品 1`, `Item 2`, `xxx`, `示例文案`) in HTML pages or in image prompts. Sample copy must be domain-realistic per the Sample Copy Convention in `references/image-generation-protocol.md`. Mark fictional data with `[估算]` / `[concept data]`, never present it as real.
7. NEVER reuse one project's reference-image chain to seed another project's images within the same deck. Each project starts a fresh chain from its own cover (per `references/visual-consistency.md`).
8. NEVER cosplay the delivery target company's brand identity in a portfolio deck submitted to that company. Brand Distance rule from `references/asset-and-fact-protocol.md` applies.
9. NEVER overwrite, "upgrade", reword, or recolor user-authored input (named style, hex palette, reference image, hand-written image prompt, brand spec). The skill's recipes and 4 directions are FALLBACKS for vague briefs — they are NOT defaults to impose on a user who already decided. See User-Authored Input Priority below.
10. NEVER quote a real brand's color, logo geometry, or wordmark from memory. When a real brand is involved, the source of truth is `brand-spec.md` produced via the 5-step Brand Asset Protocol in `references/asset-and-fact-protocol.md`. No spec, no brand visuals.
11. NEVER start generating images / writing PADB / running asset scans while there are unanswered questions in the OPENING CHECKLIST (step 0). Batch-ask first, then go heads-down.
12. NEVER write deck-plan.json without first picking a `narrative_archetype` and confirming the per-page table with the user (see step 3.5 + `references/deck-narrative-architecture.md`). Templated cover + KPI-case + process-case skeletons are banned — every page must declare a unique `narrative_role` and `why_this_page`.
13. NEVER include a `kpis` block on a page unless the user supplied real numbers OR the chosen archetype is A2 `before-after-comparison` (and even then numbers must be labeled `[concept data]` if not real). Inventing percentages to fill space is the #1 cause of decks that read as fake.
14. NEVER reuse the same `page_pattern` on two adjacent pages. Visual rhythm is part of the argument.
15. NEVER write image prompts for UIUX case-study / cover / anatomy / process / system pages using editorial-poster vocabulary (paper, pen, coffee, scribble, washi tape, binder clip, desk, textured cotton, handwritten, flat-lay, any of the 12 presets in `image-style-presets.md`). UIUX pages MUST follow `references/image-prompt-style-uiux.md` — product mockup + flat single-color BG + in-screen UI + intent label + "背景不要任何标题文字" tail.
16. NEVER over-specify pixel-level layout in image prompts (“向右倾斜 X 度” / “占画面高度 70%” / “居中偏左 200px” / “radial glow at top-left”). image2 不擅长像素级执行，处于这种 prompt 下反而会生成僵硬的图。只允许使用 `image-prompt-style-uiux.md` 里的 6 个意图标签（“排版干净，留白充足”等）。

   **16a. FREE-COMPOSITION CHECKLIST (HARD GATE before sending any IMAGE_AS_PAGE prompt to image2).** Open the prompt and verify ALL FOUR boxes — if ANY fails, REJECT and rewrite using `references/image-as-page-prompt-recipe.md` Master Template (Free-Composition Form):
   - [ ] **ANCHORS minimal**: only the must-be-true facts (which device, which UI screen, brand-mandatory icons). NO tilt angle, NO background color hex pinned to a region, NO "居中" / "纯色背景" / "X 元素在 Y 位置" / "禁止任何其他元素".
   - [ ] **PERMITTED_EXTRAS slot present**: 3+ optional creative elements image2 is encouraged to add (still-life prop, secondary device, motion trace, floating UI fragment, tilt range, light direction). If absent → REJECT.
   - [ ] **DENSITY tier explicitly named**: `spacious` (covers/dividers, 1 device, 0 fragments) / `balanced` (case study, 1 device + 1 fragment) / `magazine-dense` (anatomy/breakdown, 1 device + 3–4 orbiting fragments). Two adjacent pages MUST NOT share a tier.
   - [ ] **TEXT POLICY explicit**: lists what text image2 MAY render (in-screen UI + named brand wordmark) and what it MUST NOT render (large editorial titles, English subtitles, KPI tiles, role chips — these all live in HTML overlay, not the image).

   The single biggest failure mode of this skill is wireframe-style prompts that lock the composition: every page comes out a centered phone on flat BG and the deck reads as monotonous. `references/deck-plan-schema.md` line 21 explicitly warns against this. The fix is mechanical: enforce the checklist above on every prompt, on every page, before invoking image2.
17. NEVER deliver a multi-zone overlay page that hasn't been through `scripts/build_with_qa.py` (FULL mode) OR the Manual QA Checklist from `references/headless-mode.md` (HEADLESS mode). The closed-loop QA (or its manual equivalent) is the only mechanism that catches image-text mismatches, occlusion, and overflow before they ship. A `<page>.qa.json` or `<page>.manual-qa.json` with `pass=true` and zero `blocker|major` issues is the gate. If in HEADLESS mode and the rendered page cannot be visually inspected (no multimodal), the agent MUST still write the checklist with best-effort judgments from prompt-to-layout cross-checking, and mark every item as `CONFIRM_WHEN_VISIBLE` instead of `pass`/`fail`.

18. NEVER copy a layout.json from a previous deck and just swap the text. Each new deck MUST get its own `page_pattern` + `breathing_region` assignment per `references/page-patterns.md`, and the overlay-zone geometry (zone x positions) MUST visibly differ across pages within the deck AND across decks. **Layout-Variety Hard Gate (run before writing the first layout.json of any new deck):**
   - [ ] Picked at least 3 different `page_pattern` values across the deck (from: `hero-device-orbit` / `stacked-extracts` / `diagram-led` / `type-led` / `full-bleed-photo` / `process-strip` / `before-after-split`). NEVER use `hero-device-orbit` on more than ~30% of pages.
   - [ ] Picked at least 2 different `breathing_region` sides across the deck (left / right / top / bottom / diagonal). NO two consecutive pages share the same side.
   - [ ] Looked at the most-recent prior deck's overlay x-pattern and CONFIRMED the new deck does NOT clone it. If the previous deck used `[90,90,90,90,1340,1340]` (left column + right annotations), this deck MUST start somewhere else (e.g. right-column hero `x=1260`, split `[80,1320]`, top-strip `[96,96,1500]`, centered `[1033,...]`, headline `[50,342]`).
   - [ ] Each page's title-block x-anchor varies across the deck — do NOT pin every page's title to `x=90`.

   The 2026-05 monotony trap: I kept reusing fit-checkin's `[90,90,90,90,1340,1340]` template for every new deck, and every project looked like the last. The fix is to consult `page-patterns.md` for each new deck and pick a NEW combination — the patterns library is the antidote, not optional.

## User-Authored Input Priority

The skill's job is to make a vague brief land at lumen-2K quality. When the brief is NOT vague — when the user has already authored part of the design — the skill defers, never overrides. Same spirit as huashu's brand-asset protocol: user-supplied is ground truth, skill never invents over it.

| What the user supplied | Skill MUST do | Skill MUST NOT do |
|---|---|---|
| Named style ("温暖商业杂志风" / "赛博朋克" / "到家 App风格") | Adopt verbatim. Map onto recipe slots; if it doesn't match any of the 4 Directions, ADD a new direction filling for this project rather than force-fit. | Replace with the closest preset Direction. Suggest "a better style". |
| Hex palette (any of BG / INK / ACCENT) | Use those exact hex values in PADB and every prompt. | Round, "harmonize", or substitute with recipe presets. |
| Reference image / mood board | Treat as the canonical visual target. Pass as reference image to the model when supported. Match its palette + composition. | Generate a different look because "recipe says X". |
| Hand-written image prompt | Send the user's prompt as-is to the image model. Optionally APPEND PADB consistency suffix (palette lock + negatives) at the END, clearly marked. Show the merged prompt to the user before sending. | Rewrite, restructure, or replace user wording. Strip user details. |
| Hand-written copy / KPI numbers / case-study text | Use verbatim. | "Polish" or paraphrase. Invent surrounding metrics. |
| Real screenshot of their product | Use as REAL_SCREENSHOT lane. | Regenerate as "a better-looking version". |

When user input is partial (e.g. only a palette), use the recipe to fill ONLY the unspecified slots. Always show the merged result back before image generation: "你给的： #D9531E + #2E6F4E + 烘焙 App。 我补的：字体 阿里巴巴普惠体 / KPI 文案 / 负面提示词。确认后发送?"

If the user's choice would obviously break a hard rule (e.g. they ask for the delivery target company's brand color, violating Brand Distance), **flag the conflict ONCE and ask** — do not silently override.

## Default Bias: Generate, Don't Placeholder

This skill prefers a complete, image-rich deliverable over a sparse one full of placeholder boxes. When in doubt:

- Generate the visual instead of leaving a gap.
- For VISUAL_PROPOSAL scope (no real product screenshots), generate concept UI screens via the image model and label the deck clearly as a visual direction proposal. This is honest and complete.
- For dashboard / admin / data screens that no image model can render credibly, render them as designed UI mockups in HTML/SVG per `references/dashboard-rendering.md`. These count as the designer's design work, not as fake screenshots.
- For ecommerce / brand projects that need a campaign visuals appendix, batch-generate a coherent poster series per `references/campaign-poster-batch.md`.
- Use placeholders ONLY for things that genuinely cannot be generated honestly: real shipped product screens, real brand logos that don't exist yet, real user quotes, real metrics.
- Never deliver a deck where every device frame is an empty placeholder. That is failure, not caution.

## Analysis Depth Bar (the recruiter's first 30 seconds)

Visual polish gets attention; analysis depth keeps it. The skill MUST apply `references/analysis-depth.md` to every analysis page (problem diagnosis, competitive analysis, strategy, IA, scheme comparison, outcome, reflection). The bar in one line: **every claim must be specific to a named segment, a named scenario, and a counted observation.** Generic copy ("提升用户体验", "优化操作流程") is forbidden — it tells the reviewer nothing.

## Overview

Build UI/UX portfolio decks that prove design thinking and craft. Treat each deck as a narrative evidence chain:

```text
context -> problem -> analysis -> strategy -> exploration -> final UI -> interaction/detail proof -> outcome
```

This skill was distilled from private/local UI/UX portfolio references during authoring, but installed runtime usage must not depend on those local folders. Treat the distilled rules in `references/` as the reusable knowledge. Do not inspect or reuse the original authoring screenshots unless the user explicitly provides a new folder for a new analysis task.

## Operating Principles

1. Verify facts before design when a real product, brand, company, platform, version, metric, or public event is involved.
2. Prefer generating visuals to leaving gaps. Use placeholders only for things that genuinely cannot be honestly generated (real shipped screens, real brand logos, real user quotes, real metrics).
3. Build the reasoning spine before visual pages. A beautiful page without a design claim is decoration.
4. Show assumptions early, then iterate. A portfolio deck should be shaped with the user, not delivered as an opaque final answer.
5. Generate variations when the direction is unclear. Offer 2-3 meaningfully different directions before committing to one.
6. Validate the output as a presentation artifact: readable, aligned, visually coherent, and logically persuasive.

## Workflow Detail (expansion of the Auto-Run sequence above)

The 10-step Auto-Run sequence at the top of this file is the canonical flow. The references below are the detailed how-to for each step. When in doubt, the Auto-Run sequence wins.

| Auto-Run step | Reference to consult |
|---|---|
| 1. Capability check | `references/image-generation-protocol.md` (capability detection section) + `references/premium-image-model-routing.md` + `references/mcp-image-server-setup.md` (verified install / proxy / model-name / billing fixes for China) |
| 2. Asset scan | `references/source-ingestion.md`. If a real public brand / product / company is mentioned, ALSO run `references/asset-and-fact-protocol.md` once. |
| 3. Scope decide | `references/asset-gate.md` (FULL_CASE_STUDY / VISUAL_PROPOSAL / CRITIQUE) |
| 3.5. Pick narrative archetype | `references/deck-narrative-architecture.md` — archetype catalog + decision tree + KPI gate + adjacent-pattern-variety rule. Output the per-page table and confirm before deck-plan.json. |
| 4. Style pick | `references/guided-style-selection.md` + `references/style-directions.md`. Inherit canvas / typography / bilingual defaults from `references/deck-defaults.md` unless overridden. |
| 5. Lock art direction (PADB) | `references/visual-consistency.md` + `references/theme-asset-isolation.md` |
| 6. Asset routing per page | `references/page-patterns.md` to choose page type, then route: dashboards/data → `references/dashboard-rendering.md`; campaign posters → `references/campaign-poster-batch.md`; covers / 3D / scenes / concept UI screens (CJK or English) → `references/image-generation-protocol.md` (image-first recipe). Fallback to `references/html-ui-screen-lane.md` only when the available image model is verified to garble CJK. |
| 7. Showcase first | `references/showcase-first-deck-workflow.md`. For poster series, generate only the master poster #1 here; batch-produce #2-N at step 9. |
| 8. Confirm | Show contact sheet to user. Apply `references/visual-language.md` for the deck-level visual rules. |
| 9. Expand | `references/portfolio-logic.md` for case-study spine. `references/analysis-depth.md` MUST be applied to every analysis page. `references/anti-ai-slop.md` MUST be re-read before each new HTML/CSS or image prompt. For multi-agent environments, `references/multi-agent-workflow.md`. |
| 10. Final QA | `references/quality-review.md` + 5-axis consistency QA from `references/visual-consistency.md` + analysis-depth self-check from `references/analysis-depth.md`. Verify the `[概念 / Concept]` badge appears on every non-real UI page in VISUAL_PROPOSAL mode. |

For personal learning experiments that need reusable HTML deck infrastructure, use `references/huashu-vendor-usage.md`. For background on what the distilled rules cover and where they fall short, see `references/public-corpus-notes.md`.

## Required Case-Study Logic

For every major case study, include at least five of these proof blocks:

- Project background: business/user context, target user, platform, scope, role.
- Problem diagnosis: pain points, current-state issues, user behavior, stakeholder constraints.
- Competitive or benchmark analysis: what was studied and what design opportunities were found.
- Design strategy: principles, information architecture, key interaction choices, or experience goals.
- Iteration evidence: before/after, option A/B, wireframe to final, or tradeoff comparison.
- Core screen presentation: final UI screens with callouts explaining hierarchy and interaction.
- Detail proof: components, states, edge cases, micro-interactions, data display rules, visual system.
- Outcome: metrics, qualitative feedback, handoff result, operational value, or honest limitation.

If the deck is a visual portfolio rather than a full case study, keep proof blocks shorter but still show intent. A portfolio page should not be only "large screenshot + big title" unless it is a transition, hero, or gallery page.

## Page Rhythm

Use cinematic pacing:

- Open with one strong cover that establishes identity, year, role, and visual tone.
- Follow with a contents page or project map.
- Use section covers to reset attention between projects.
- Alternate dense reasoning pages with large visual proof pages.
- End with other works, visual identity/brand pieces if relevant, then a memorable thanks/contact page.

For a 15-25 page portfolio deck, a reliable rhythm is:

```text
Cover -> Contents -> Profile/Positioning -> Project 1 Cover -> Context -> Problem/Analysis -> Strategy -> Iterations -> Final Screens -> Details/Data -> Outcome -> Project 2 Cover -> ... -> Other Design -> Thanks
```

## Quality Bar

Reject outputs that look generic, template-like, or purely decorative. The target feel is "designer with product reasoning and high visual polish":

- The viewer should understand the case without a verbal explanation.
- Page hierarchy should be clear in three seconds.
- Text must be concise enough for a presentation but specific enough to prove thinking.
- Visual effects must support depth, focus, or product realism.
- Screenshots must be framed, scaled, and integrated into the composition.
- Every beautiful page must carry a design claim, an artifact, or a transition purpose.

## References

- `references/image-first-deck-workflow.md`: **the primary delivery path** — image-model background + HTML text overlay + deck_stage.js navigation. Read first. Default lane for concept UI screens (CJK or English) since gpt-image-2 (verified 2026-05) renders Chinese labels cleanly.
- `references/asset-gate.md`: hard gate that blocks deck/image production until real brand assets are gathered or scope is downgraded. Also defines the `[概念 / Concept]` page-level badge rule.
- `references/deck-defaults.md`: canvas, typography, bilingual strategy, output format decision, and `generated-images/` naming convention. Pick silently, do not re-ask the user.
- `references/anti-ai-slop.md`: forbidden visual vocabulary. Read before any HTML/CSS or image prompt.
- `references/analysis-depth.md`: forced specificity rules + per-page-type templates. Apply to every analysis page.
- `references/visual-consistency.md`: Project Art Direction Block (PADB) and 5-axis consistency QA. Required for any deck with more than one generated image.
- `references/dashboard-rendering.md`: render dashboard / admin / data-screen mockups in HTML/SVG when image models cannot produce credible numbers. Use for B-side, IoT, smart-city, finance, fleet, manufacturing data screens.
- `references/html-ui-screen-lane.md`: **deprecated as of 2026-05, fallback only**. Hand-build concept mobile / web UI screens in HTML/CSS inside the deck page's device frame ONLY when the available image model is verified to garble CJK labels. gpt-image-2 (2026-05) renders CJK labels cleanly — prefer the image-first lane.
- `references/mcp-image-server-setup.md`: verified working `.vscode/mcp.json` setup for Imagen 4 + Nano Banana Pro from China. Covers proxy plumbing (`NODE_USE_ENV_PROXY`), model-name patches for retired preview IDs, AI Studio spend-cap requirement, and `must NOT have additional properties` schema gotcha.
- `references/campaign-poster-batch.md`: produce a coherent series of 4-6 campaign posters with one master motif. Use for ecommerce / brand / operations portfolios.
- `references/source-ingestion.md`: decide whether local screenshots, videos, or notes are enough.
- `references/asset-and-fact-protocol.md`: verify facts and collect assets for real products/brands.
- `references/theme-asset-isolation.md`: prevent cross-theme material reuse and require project-specific generated assets.
- `references/guided-style-selection.md`: guide users through 3 differentiated style directions before final production.
- `references/style-directions.md`: choose fallback styles and variants.
- `references/multi-agent-workflow.md`: coordinate planner, image, builder, and reviewer roles when the environment supports parallel agents.
- `references/showcase-first-deck-workflow.md`: require 2-page visual grammar showcases before producing decks with 5+ pages.
- `references/portfolio-logic.md`: structure case-study reasoning.
- `references/deck-narrative-architecture.md`: pick the deck's narrative archetype + per-page roles before writing deck-plan.json. Enforces pattern variety, KPI honesty, and "why this page exists".
- `references/annotated-callouts.md`: render mode where the image IS content (not background). Yellow anchor dots pinned to specific pixels + thin lines + side-gutter cards carrying 80–180 char design memos. Use for anatomy / detail / before-after / process pages.
- `references/image-prompt-style-uiux.md`: **默认 UIUX 图片 prompt 范式**. Product mockup + flat single-color BG + in-screen UI + 6 个排版意图标签 + 禁词清单。所有 case-study / cover / anatomy / process / system / hero 页必须走这个。
- `references/closed-loop-overlay-qa.md`: 页面交付前必跑的闭环 QA。`scripts/build_with_qa.py` build → screenshot → vision QA (模型由 `BACKEND_QA_MODEL` 配置，默认 `gpt-4o`) → 有 blocker/major 则 LLM 输出修订后的 layout.json 重跑，最多 3 轮。对应 NEVER 17。`retake_image=true` (exit 2) 必须回退到 step 6 重做 prompt + 重生成图，不要在 overlay 上打补丁。
- `references/headless-mode.md`: **HEADLESS 模式退化路径**。当环境无终端/无脚本时，Auto-Run 各步骤如何降级、Manual QA Checklist（10 条目视检查替代 `build_with_qa.py`）、PROMPT_PACK_ONLY 交付格式。对应 Operating Mode 章节和 NEVER 17 的 fallback 条款。
- `references/overlay-layout-spec.md`: `<page>.layout.json` 的 schema 唯一信源。字段定义（image / image_w / deck_palette / deck_fonts / overlays[].role / fields[].font / size_pt / color / `gradient(...)` 语法 / letter_spacing / italic）+ 闭环 QA 修复 LLM 可改 / 不可改的字段表。手写或 LLM 生成 layout.json 前必读。
- `references/example-fit-checkin-walkthrough.md`: 端到端的可复用范例 — 从 brief → prompt → ComfyUI 生成 → 手写 6 overlay layout → 闭环 QA iter 1 通过。新页面起步直接 copy hero.layout.json 改 6 处即可。
- `references/page-patterns.md`: choose page types and layouts.
- `references/visual-language.md`: match the dark-tech UI/UX portfolio aesthetic.
- `references/image-generation-protocol.md`: decide when and how to generate visual assets with image2 or another image tool.
- `references/premium-image-model-routing.md`: choose stronger image models and multi-candidate generation workflows.
- `references/huashu-vendor-usage.md`: use vendored Huashu Design templates/scripts for personal learning experiments.
- `references/quality-review.md`: score and fix the deck before delivery.
- `references/public-corpus-notes.md`: current public reference sources and what to borrow from them.
