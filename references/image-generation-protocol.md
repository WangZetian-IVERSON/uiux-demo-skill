# Image Generation Protocol

## Purpose

Use image generation to create support visuals for UI/UX portfolio decks while preserving product truth. Real assets define the work; generated images help package, stage, and explain it.

Every project and theme must get its own generated asset pool. Do not reuse cover props, backgrounds, mascots, poster visuals, or decorative assets across unrelated themes.

## Hard Rule (read first)

The single most common failure mode of this skill is the agent painting a UI with HTML/CSS/SVG, screenshotting it (or saving the rendered DOM as a PNG), and presenting it as a "generated image". This is forbidden.

**A "generated image" in this skill ALWAYS means: an image returned by a real image-generation model.** Acceptable producers include Nano Banana Pro / Gemini 3 Pro Image, GPT Image / gpt-image-1, Midjourney, Stable Diffusion (XL/3/Flux), Recraft, Ideogram, or a Codex-built-in image tool that calls one of these.

An HTML page rendered to PNG is NOT a generated image. CSS gradients with rounded boxes inside a phone frame are NOT a generated image. Inline SVG illustrations are NOT a generated image.

If no real image model is callable in the current session, the correct behavior is to **output prompt packs** for the user to run externally — NOT to fabricate replacements with HTML/CSS.

## Capability Detection (run before any image task)

At the start of any image-related task, perform an explicit capability check and tell the user the result:

```text
Image capability check:
- Real image-generation tool available in this session: yes | no
- If yes, model/tool name: <name>
- Test prompt result: <one sentence on quality / text rendering / resolution>
- Decision: GENERATE_DIRECT | PROMPT_PACK_ONLY
```

Decision rules:

- `GENERATE_DIRECT` only if a real image model is callable AND it can produce at least 1024px output AND it can render either accurate Latin text or clean text-free compositions. Otherwise downgrade.
- `PROMPT_PACK_ONLY` if the environment has no real image tool, the tool only renders DOM/HTML, the tool produces low-resolution thumbnails, or text rendering is garbled. In this mode, deliver model-agnostic prompt packs and tell the user which external model to run them on (Nano Banana Pro / Gemini 3 Pro Image preferred for portfolio work; GPT Image / gpt-image-1 second; Midjourney for atmospheric covers only).

**Never silently downgrade to HTML rendering.** If you cannot generate a real image, say so and ship prompts.

## Tool Preference (when GENERATE_DIRECT)

Preferred order of real image models for UI/UX portfolio work:

1. Gemini Nano Banana Pro / Gemini 3 Pro Image — best for portfolio covers, Chinese text rendering, 2K+ assets, reference-image blending.
2. OpenAI GPT Image / gpt-image-1 — best for instruction following, brand-guided assets, iterative editing.
3. Recraft V3 / Ideogram 2 — useful for typographic posters and brand-color-locked visuals.
4. Midjourney v6 / v7 — atmospheric covers and cinematic backgrounds only; do not use for text-heavy pages.
5. SDXL / Flux via configured endpoint — fallback for support props.

Do not hardcode a single model. The skill should generate strong prompts and call whatever real image capability the environment provides.

## ComfyUI Desktop Invocation (verified default for this workspace, 2026-05)

When the local **ComfyUI Desktop** server is running on `127.0.0.1:8000`, the
skill MUST prefer it over remote relays for `gpt-image-2` calls — same model,
zero network latency, full ~9-credit cost still applies but no relay rate
limiting.

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:COMFY_API_KEY    = "<COMFY_API_KEY from ComfyUI Desktop settings>"
python scripts/image_client.py generate `
  --backend       comfyui `
  --comfyui-url   http://127.0.0.1:8000 `
  --model         gpt-image-2 `
  --size          2048x1152 `
  --prompt-file   <path to prompt.txt> `
  --out           <path to out.png> `
  --comfyui-timeout 240
```

Defaults that should NOT be changed without reason:
- `--size 2048x1152` (16:9, matches stage canvas)
- `--comfyui-quality high` (default, ~9 credits/page)
- `--comfyui-workflow vendor/comfyui/workflow-t2i.json` (the only workflow we vendor)

Failure modes:
- `ERROR: ComfyUI did not finish within 240s` → bump `--comfyui-timeout` to 360
- `404` on `/prompt` → ComfyUI Desktop is not running OR is on a different port (check the desktop app's Settings → Server)
- empty/garbled image → re-run with a different seed (auto-randomized each call)
- CJK garble in 屏内 UI 文字 → tighten the prompt per `image-prompt-style-uiux.md`, do NOT switch to a different model unless garble persists across 3 seeds

When ComfyUI Desktop is unavailable, fall back to the pockgo relay route (no
`--backend` flag, default), but expect HTTP 524 timeouts on `gpt-image-2-2k`.

## When To Generate Images

Default: generate aggressively. Reach for the image model first, fall back to other solutions only when generation cannot honestly produce the asset.

Generate images for:

- Cover hero scene.
- Section covers and atmospheric backgrounds.
- 3D mascot, shopping terminal, glass device, or abstract commercial object.
- Generic laptop/phone staging scene.
- Decorative commerce objects: shopping bags, coupon cards, gift boxes, price tags.
- Atmospheric command-center / control-room **environment shots** (the room, the lighting, the spatial mood) — for use as section covers or backdrops behind a real or HTML-rendered dashboard. The image model NEVER renders the actual dashboard surface, charts, or numbers.
- Campaign poster placeholders when clearly marked as concept examples.
- Visual mood variants for direction exploration.
- Project-specific asset pools when no screenshots exist or when the project theme differs from prior work.
- **Concept UI screens** (in VISUAL_PROPOSAL mode):
  - If interface text is Latin-only (English / Spanish / German / French …), render as a high-fidelity mockup via the image model inside a device frame.
  - If interface text is CJK / RTL / non-Latin, do NOT route to the image model. Hand-build the screen in HTML/CSS inside the deck page's device frame (`HTML_UI_SCREEN` lane). This is per the Mobile UI rule below — image models universally garble non-Latin UI text and regress to off-brief outputs.

Do not generate images for:

- A real shipped app screen presented as evidence of a real product. Use the user's actual screenshot.
- A real brand's logo. Use the user's logo file.
- Real user research, real metrics, real quotes.
- Real before/after UI proof when the project IS a real existing product.
- **Dashboards / data screens / admin consoles / charts / KPI cards / tables.** Image models cannot render numbers consistently and produce garbled labels. Render these in HTML+SVG per `references/dashboard-rendering.md`. The image model may produce the *atmospheric environment* around a dashboard, but never the dashboard surface itself.
- **Mobile / desktop UI screens whose interface text is non-Latin (Chinese / Japanese / Korean / Arabic / Cyrillic / Thai / Hindi).** Empirically verified across Imagen 4 / Imagen 4 Ultra / Nano Banana Flash / Nano Banana Pro (Gemini 3 Pro Image): all of them garble CJK characters into nonexistent glyph composites, and frequently regress to training-set memories such as iPhone home screens with fake English app names, a fashion model standing in front of seamless paper, or a developer DevTools screenshot with placeholder URLs. The failure mode is universal and not fixable by prompt engineering, negative prompts, or higher-tier models. Concept UI screens with Chinese / Japanese / Korean copy MUST be hand-built in HTML/CSS inside the device frame on the deck page (route to the new `HTML_UI_SCREEN` lane). Latin-only UI screens may still go to the image model, but treat any text inside the screenshot as best-effort and overlay critical CTA / price / data on top in HTML when possible.

If those are missing AND the project is a real shipped product, ask for the materials or use a clearly labelled placeholder. If the project is conceptual (most personal portfolios), generate the concept screens and label the deck as a visual proposal.

## Theme-Specific Asset Rule

Before generating images, define:

```text
project_slug:
theme:
audience:
asset_pool:
forbidden_reuse:
```

Examples:

- Ecommerce SaaS marketplace: shopping terminal, coupon cards, product-card collage, warm orange commercial props.
- Hotel booking app: hotel facade, booking card, map pin, room card, calm blue service props.
- Smart power dashboard: map texture, grid floor, glass dashboard panel, electric blue metric cards.
- Wellness/sleep app: moonlit landscape, soft phone pedestal, circular control motif, purple-blue calm props.

Do not use the ecommerce shopping terminal for hotel booking, smart power, wellness, or unrelated SaaS projects.

## Prompt Structure

Amateur prompts only describe "vibe". Portfolio-grade prompts describe vibe + camera + light + material + composition coordinates + negative constraints. AND for any project with more than one generated image, every prompt MUST start with the project's Project Art Direction Block (PADB) defined in `visual-consistency.md`. This is non-negotiable — it is the only thing that prevents image-to-image style drift.

Use this structure:

```text
[PADB — paste the entire Project Art Direction Block as the first half of the prompt]

--- PAGE-SPECIFIC INSTRUCTIONS ---
[aspect ratio + target resolution — inherits from PADB unless overridden]
[page role + position in deck]
[composition with explicit empty areas, e.g. "left 40% reserved for Chinese title, vertical safe zone 1080-1440px"]
[main subject: object + scale + pose + position]
[secondary props — ONLY items from PADB.props_vocabulary]
[any per-page deviation from PADB — if you need one, also update the PADB]
[negative — re-state PADB.forbidden_colors and PADB.forbidden_props plus page-specific exclusions]
```

If a page has no PADB yet (the very first image of the project), write the PADB first per `visual-consistency.md`, save it, then prompt.

## Lean Natural-Language Mode (poster / brand / editorial decks; for UIUX pages see `image-prompt-style-uiux.md`)

**Verified 2026-05 on gpt-image-2.** The PADB-stacked structured prompt above (with hex codes, NEGATIVE lists, "PERMISSION" / "TEXT POLICY" sections, header/footer bar specs, and 400+ word multi-section bodies) over-constrains modern instruction-tuned image models and visibly flattens their output: scenes look obediently filled-in rather than photographed. These models read English like an art director's brief, not like a Stable Diffusion tag soup, and they reward freedom inside a clear envelope.

Use the lean mode for poster / brand / editorial deck pages whose visual goal is "looks like a real magazine / editorial / cinematic photo of a scene". Reserve the full PADB-stacked mode for SDXL / Flux / Recraft / Ideogram, and for cases where you have measurably proven that strict control beats lean.

### Preset-first lean prompts (preferred since 2026-05-02)

> **⚠️ DOMAIN RESTRICTION: This preset system applies to POSTER / BRAND / EDITORIAL decks ONLY.**
> For **UI/UX case-study pages** (cover, case-study, anatomy, process, system, hero — any page where the visual is a product mockup on flat BG), the presets are **forbidden** and you MUST use `references/image-prompt-style-uiux.md` instead (the 5-sentence Chinese structure + 6 intent-label dictionary + 6 verified templates M1–M6). See SKILL.md Rule 15. The two systems are mutually exclusive per page; never mix a preset tag with a UIUX intent label in the same prompt.
>
> If a deck mixes UIUX pages and poster/brand pages (e.g. a portfolio that ends with a campaign visual appendix), apply the rule per page: UIUX pages → `image-prompt-style-uiux.md`, poster pages → presets below.

After running A/B tests on the JD 618 deck (4 cases), we confirmed: even a 200-word lean paragraph still drifts in style across pages, because the LLM keeps re-inventing "lighting / lens / material / palette / reference" in slightly different words for each prompt. Two adjacent pages end up looking like they were shot by different photographers.

The fix — borrowed from `frontend-slides` (curated style presets, "show-don't-tell" picker) and `huashu-design` (20 design philosophies × 5 schools, anti-AI-slop rules) — is to **move the style DNA out of the prompt and into a named preset**. The prompt itself becomes a 3-section, ~60–120-word skeleton.

The preset library lives in `references/image-style-presets.md` (12 entries: `cinematic-velvet-jewel`, `swiss-editorial-grid`, `dark-botanical-sanctum`, `editorial-paper-ink`, `brutalist-concrete`, `nocturne-festival`, `rose-minimal-studio`, `arcade-neon`, `sunbleached-archive`, `monastic-stillness`, `tactile-laboratory`, `night-market-banquet`). For poster/brand/editorial decks, pick one preset for the whole deck. If unsure, run the show-don't-tell flow: render the cover under 3 candidate presets in parallel, let the user pick, lock for the rest of the deck. **For UIUX decks, skip this entirely — use `image-prompt-style-uiux.md`.**

#### The 3-section preset-first prompt template

```text
preset: <slug-from-image-style-presets.md>

scene: <one-sentence description of WHAT physical scene appears: subjects, rough composition, aspect ratio>.

breathing region: <one sentence naming the rectangle that must stay clean for HTML overlay, in plain English (e.g. "leave the bottom third below y≈770 as flat shadow plane").>

in-scene labels: <≤6 short verbatim strings the image MUST physically contain, each in single quotes (e.g. 'JD 618', '¥2,299', '已省 ¥500'). Omit this line if the page has no required labels.>

avoid: purple gradients, neon stroke text, emoji-style icons, rounded card with left accent border, AI-rendered human faces, plastic-shiny over-rendering, generic glow halos, Inter as display heading, generic dashboard with floating panels.
```

That's the entire prompt. Total length should be **60–120 words**, never more. Do NOT re-describe the preset's lighting / lens / material / palette in the prompt body — the model is expected to look up the preset by name and follow it as the style envelope. Do NOT rewrite the `avoid:` line — it is the fixed anti-slop tail and is identical across every prompt in the skill.

#### Worked example (JD 618 cover)

```text
preset: nocturne-festival

scene: a single rose-gold espresso machine on dark walnut, with a tall glass of red wine slightly behind it, two paper lanterns out of focus deep in the background. 16:9 landscape (2048x1152). The hero ensemble sits in the upper-center; the lower third of the frame is left as deliberate empty floor.

breathing region: the bottom third of the canvas (below roughly y=770) must stay as a clean flat shadow plane of the same crimson black, with no products, devices or text — pure negative space for HTML overlay.

in-scene labels: a small red rounded badge on the espresso machine's screen reads literally 'JD 618' in clean white Chinese sans-serif, must be legible.

avoid: purple gradients, neon stroke text, emoji-style icons, rounded card with left accent border, AI-rendered human faces, plastic-shiny over-rendering, generic glow halos, Inter as display heading, generic dashboard with floating panels.
```

#### When to fall back to the legacy ~200-word lean paragraph

Only when the project explicitly opts out of the preset library (for example, a fully custom brand world where none of the 12 presets fit and the team chooses not to add a 13th). In that case follow the original anatomy below — but still always end with the fixed `avoid:` tail above.

### Lean prompt anatomy (target 150–250 words) — legacy, preset-first preferred

```text
[1 sentence — what this image IS, including aspect ratio and editorial register]
e.g. "A cinematic, magazine-cover-grade still life shot for a Chinese e-commerce
festival ('JD 电器节 2026'), 16:9 landscape (2048x1152)."

[1 short paragraph — mood / palette in feeling words, NOT hex codes]
e.g. "Mood: deep crimson midnight, mahogany surface, dramatic warm rim light from
upper right, festival gold embers in the air. Editorial photography for
Wallpaper* / Kinfolk, not catalog. Film grain, gentle vignette, shallow DOF."

[1 short paragraph — what objects/subjects appear, with composition freedom]
e.g. "Arrange a small ensemble of premium home electronics on dark wood — a sleek
black smart TV, a rose-gold espresso machine, a tall glass of red wine. Compose
them as you see fit; the goal is a luxurious 'festival begins after dark' feel."

[1 sentence — the small in-scene labels that MUST appear verbatim, if any]
e.g. "Tucked into the bottom-right corner, a black smartphone slice peeks in
(only ~20% visible). Its screen edge shows a small red rounded badge that reads
literally 'JD 电器节' in clean white Chinese sans-serif — this string must be
legible and correctly written."

[1 sentence — the breathing region for HTML overlay text]
e.g. "The lower third of the canvas (below roughly y=770) must stay as a clean
flat shadow plane of the same crimson black, with no products, devices, or text
— leave it as deliberate negative space for later text overlay."

[1 closing sentence — the only blanket negative needed]
e.g. "No other text anywhere in the image."
```

### What stays in the prompt

1. **Aspect + register** (16:9 magazine cover, editorial photography, etc.)
2. **Mood in feeling words** (crimson midnight, festival gold rim, film grain) — no hex.
3. **Subject roster + freedom** ("arrange these 3 objects as you see fit").
4. **Tiny in-scene labels** that the deck *requires* to be photographed (a price chip, a UI screen string, a logo wordmark on a billboard). Quote them verbatim in single quotes.
5. **The breathing region** in plain English coordinates — this is the contract with `find_blank_zone` / `layout_fitter`.
6. **One short closing line** that forbids unwanted text everywhere else.

### What gets removed (vs the PADB-stacked mode)

- ❌ Big editorial Chinese title baked inside the image. → Lives in HTML overlay.
- ❌ English display subtitle baked inside the image. → HTML overlay.
- ❌ Description paragraph baked inside the image. → HTML overlay.
- ❌ KPI cards / role chips / "section label" baked inside the image. → HTML overlay.
- ❌ Header bar / footer bar with verbatim text strings. → If you really want a deck chrome, render it in HTML on top of the image (cheaper, editable, sharper). Bake into the image only when the chrome must be perspective-warped onto a surface.
- ❌ Lists of forbidden hex codes, lists of forbidden props, "PERMISSION" sections, "TEXT POLICY" sections. Modern models honor a single closing "no other text" sentence; the long lists are noise that crowds out the mood description.
- ❌ Fake structured headers like `PALETTE (locked):` / `ANCHORS:` / `NEGATIVE:`. Write English paragraphs.

### The text/overlay split (this is the key rule)

The image carries the **picture** (scene, mood, props, lighting) and at most a few **tiny in-scene labels** that are physically part of the picture (a badge, a price chip on a tag, the words on a poster pinned to a wall, a UI string on a phone screen). The HTML layer carries the **deck typography**: editorial title, display subtitle, body paragraph, KPI cards, role chip, page number, deck chrome.

Why split this way:
- Editable later: the LLM can re-tune copy without re-spending image credits.
- Crisp at any zoom: HTML text is vector, image text is raster.
- No CJK garble risk on long strings: the image only has to nail short labels (≤8 chars), which gpt-image-2 / nano-banana-pro handle reliably; long Chinese titles are exactly where models start hallucinating glyphs.
- Cleaner blank-zone scan: `find_blank_zone` can reliably find the reserved region because no large in-image text competes with it.

### When NOT to use lean mode

- Posters where typography IS the design (campaign poster batch, KV with hand-set Chinese title): the title must be photographed onto the surface. Use the structured POSTER recipe.
- Dashboards / data screens: per protocol, NEVER image-model these. Render in HTML.
- Sections whose meaning depends on exact pixel-level color matching to a brand book: use the structured PADB mode with hex codes.
- SDXL / Flux / older SD models: they are tag-soup readers, not instruction followers. Use the structured PADB mode.

Always specify in the page-specific section:

- Page role: cover, section cover, background, 3D support object, poster placeholder, concept UI screen.
- Where the title/UI insertion zone lives, in concrete pixel or percentage coordinates.
- For image-first deck pages, mark reserved text zones as "must remain a soft, low-contrast area — no subjects, no props, no hard edges that would clash with overlaid HTML text".
- Negative constraints — always include "no garbled text" for image-first deck pages. In-image labels (CJK or otherwise) must be specified as exact verbatim strings in `in_image_ui`; editable Chinese title/body text still lives in the HTML overlay, not the image.

## Image-First Deck: Page Image Recipe

For pages produced under `references/image-first-deck-workflow.md`, use this exact recipe (in addition to PADB):

```text
[PADB block — full]

--- IMAGE-FIRST PAGE INSTRUCTIONS ---
canvas:                 16:9 at 2048x1152
page_role:              [from page-patterns.md]
deck_position:          page X of Y
reserved_text_zones:    [paste exact zones from the Layer Map in image-first-deck-workflow.md]
                        These zones MUST be soft background gradient or low-contrast texture only.
                        NO subjects, NO props, NO hard text-competing edges in the zones.
in_image_subject:       [main hero scene/object that fills the rest of the frame]
in_image_ui:            [if a phone/laptop frame appears, describe the in-frame concept UI:
                         layout, density, real domain-realistic labels in the deck's target
                         language (Chinese is fine — gpt-image-2 verified 2026-05 renders CJK
                         labels cleanly), chart types (line/bar/area), accent color from PADB.
                         Quote 4-8 exact label strings the model must place verbatim.]
device_frame:           [inherit from PADB.device_lock]
links_planned:          [list of clickable hot zones that will become <a> in HTML — keep them
                         clean of background distraction]

negative:               no garbled text
                        no fake brand logos
                        no watermark
                        no AI sparkles
                        the reserved text zones must remain visually clean and low-contrast
                        [PADB.forbidden_colors]
                        [PADB.forbidden_props]
```

## Prompt Templates

These are baseline templates. Always specialize them with project-specific details before generating.

### Warm Commercial Cover

```text
16:9 at 2048x1152, UI/UX portfolio cover, warm commercial ecommerce SaaS app design review.
Composition: left 42% reserved as title safe zone (vertical center axis at x=430), 3D hero object placed in right 50% with center at x=1450 y=580.
Subject: friendly 3D shopping terminal mascot, scale ~700px tall, slight 3/4 turn toward camera, screen-face neutral with soft glow.
Secondary props: 2 floating shopping bags (low density), 1 coupon card, 3 small floating stars at low opacity. No clutter.
Material: soft-touch matte plastic body, anodized aluminum trim, frosted acrylic screen, subtle subsurface scattering on rounded corners.
Lighting: key light 45 degrees from upper-right (warm 4200K), soft fill from left, hard contact shadow at 30 degrees, gentle rim light on top edge.
Camera: 85mm equivalent, f/2.8, eye-level, slight upward tilt 5 degrees.
Palette: deep charcoal #16110d background with radial warmth toward center, primary accent amber #f5a524, secondary cream #f6f1e6, tiny cobalt detail accent.
Render reference: Cinema4D + Octane, studio product photography quality.
Quality bar: magazine cover composition, generous negative space on the left for Chinese hero title to be added later in HTML.
Negative: no fake UI text on the screen, no garbled characters, no real brand logos, no watermark, no purple gradient background, no AI sparkles, no stock-poster feel.
```

### Dark-Tech Dashboard Section Cover

```text
16:9 at 2048x1152, UI/UX portfolio section cover, enterprise dashboard and data visualization project.
Composition: large empty title area on the left 45% (vertical center at x=460), hero object cluster on the right 50%.
Subject: floating glass dashboard panel at the right, slightly tilted, with abstract glowing chart shapes (no readable numbers, no fake UI text). 2 secondary glass cards drifting behind at lower opacity.
Environment: deep navy spatial environment with a perspective grid floor receding to vanishing point, faint volumetric haze, distant glowing map texture as backdrop.
Material: frosted glass with thin cyan edge glow, brushed dark metal frames, subtle internal reflection.
Lighting: cinematic studio with cyan key from upper-left (5600K cool), warm rim accent from lower-right, hard floor reflection at 25% opacity.
Camera: 50mm equivalent, f/2.0, low eye-level looking slightly up, 3/4 view.
Palette: #050a12 base, electric cyan #34d6ff accent, deep navy mid-tones, no warm colors except a single ember spark.
Render reference: Octane + Redshift command-center cinematic, dark sci-fi product photography.
Quality bar: command center mood, premium enterprise feel, clean negative space for title.
Negative: no readable numbers on charts, no fake KPI text, no random logos, no watermark, no purple gradient, no neon rainbow, no glowing stars or sparkles, no Tron grid cliche.
```

### B-Side SaaS Website Hero Scene

```text
16:9 at 2048x1152, UI/UX case study section cover, B-side SaaS official website review.
Composition: large laptop mockup centered slightly right (center at x=1200 y=620), pedestal occupies bottom 30%. Title safe zone occupies top 25% across the full width.
Subject: 16-inch open laptop, lid back at ~110 degrees, screen surface neutral dark or softly abstracted (no fake website UI). Concrete pedestal underneath.
Environment: dark charcoal studio with a subtle cobalt blue gradient wash from upper-left, fine grain texture on background.
Material: brushed aluminum laptop body, matte concrete pedestal with micro-pitting, screen as anti-reflective glass.
Lighting: soft key light from upper-left (5200K), tight rim on the laptop edge, gentle ambient fill, contact shadow under pedestal at 25 degrees.
Camera: 70mm equivalent, f/4, slight low-angle 3/4 view to give the laptop presence.
Palette: #0c1118 base, cobalt #2563eb accent, neutral cool grays for body.
Render reference: high-end product launch photography (Apple keynote style, restrained).
Negative: no fake brand logo on the laptop, no readable fake UI text, no purple gradient, no floating sparkles, no AI watermark.
```

### 3D Support Object (project-specific)

```text
1:1 at 1536x1536, isolated 3D support object for a [project domain] portfolio page.
Subject: [single specific object tied to the project domain — e.g. coupon card, room key card, electric meter, sleep mask, hard hat, etc.]. Slight 3/4 angle, scale fills 70% of canvas.
Material: [specify per project].
Lighting: studio key 45 degrees upper-right, soft fill, contact shadow at 30 degrees.
Camera: 100mm macro equivalent, f/4, eye-level.
Background: transparent or solid #f5f1ea / #0b1118 (state which).
Palette: tied to the project domain.
Render reference: Cinema4D + Redshift product photography.
Negative: no text on the object, no logos, no watermark, no extra props, no AI artifacts.
```

## Sample Copy Convention (inside prompts and inside HTML pages)

When prompts or HTML pages need filler text — store names, KPI labels, news items, product titles, user nicknames — write **realistic, domain-coherent samples**, not lorem-ipsum and not placeholder counters.

Forbidden filler:

- `商品 1 / 商品 2 / 商品 3`, `Item 1 / Item 2`, `Lorem ipsum`, `xxx`, `示例文案`, `placeholder`, `测试数据`, `1234567`.
- Generic English KPI labels like `Metric 1 / Value`, `Chart Title`, `Label here`.
- Random hex-string usernames (`user_a8f3`).

Required filler style:

- Names match the domain. Ecommerce dashboard → real-sounding store/SKU names (`华东 · 浦东金桥旗舰店`, `保暖羊毛衫 V 领基础款`). Logistics console → real-sounding city + lane (`深圳 → 武汉 · 干线 047`). Wellness app → real-feeling user nicknames (`晚安鹿_2024`).
- Numbers match plausibility. Use ranges that fit the business (an SKU page-view of `12,438` not `999,999,999`).
- KPI labels are in the deck's primary language (Chinese-led decks: Chinese leads, English ≤4 words as small caption).
- Time labels follow real cadence (`今日 09:00 - 现在`, `近 7 日`, `2025-Q4`).
- Mark estimated / fictional data with `[估算]` or `[concept data]` per `analysis-depth.md`. Realistic does NOT mean fake-as-real.

Why: a dashboard with `商品 1 / 商品 2` reads as a wireframe demo. A dashboard with `保暖羊毛衫 V 领基础款 · 浦东金桥店 · 1,847 单` reads as a designer who understands the business. The visual is the same; the credibility is not.

## Reference Image Usage

When the model supports reference images (Nano Banana Pro / Gemini 3 Pro Image, GPT Image, Midjourney `--cref`, etc.), USE THEM. This is the second strongest tool against style drift, after the PADB.

1. After generating image #1 (cover) and selecting the best candidate, pass it as a reference image to every subsequent prompt with the instruction "match the lighting, palette, material vocabulary, and camera feel of the reference image".
2. For 3D props that should belong to one set, pass the first prop image as reference for all later props.
3. For concept UI screens that share the same device frame, pass the first screen as reference for the rest.
4. Use real UI screenshots as composition references only when the user permits.
5. Use local portfolio screenshots as style references, not as content to copy.
6. Do not ask the model to recreate a screenshot exactly.
7. If generating a product-scene variant, keep the original product/UI recognizable and do not alter factual interface content.

If the model does NOT support reference images, compensate by being more explicit in the PADB: exact hex codes, exact lighting angles, exact material names, exact device model, exact lens/focal-length feel.

## Output Contract

When asked to generate images, output one of these (decided by the capability check above):

- `GENERATE_DIRECT`: a directly generated image returned by a real image model, plus the prompt used and which model produced it.
- `PROMPT_PACK_ONLY`: a model-agnostic prompt pack, with explicit instructions on which external model to run it on, target resolution, and how many candidates to generate per asset role.

Never output a third option of "HTML/CSS/SVG mockup saved as PNG". If you find yourself about to render a page in code and screenshot it as a substitute for a generated image, stop — switch to `PROMPT_PACK_ONLY` and deliver prompts instead.

For a single page image request:

1. Run the capability check.
2. If `GENERATE_DIRECT`: generate the image, state the model used, state the image role (support asset vs final page visual), revise prompt and regenerate if needed.
3. If `PROMPT_PACK_ONLY`: deliver the prompt with target model + candidate count + selection criteria. Do not produce a fake substitute.

For multi-page decks, generate prompts per page first unless the user explicitly asks for immediate batch generation. For high-polish portfolio output, create an asset pool instead of a single image:

```text
cover: 4 candidates
section backgrounds: 2 candidates per project
3D support objects: 4-8 candidates
poster/campaign placeholders: 3-6 candidates
component-board backgrounds: 2-4 candidates
phone/laptop staging scenes: 2-4 candidates
```

Select the best assets, then compose real screenshots/placeholders and text in HTML/PPT. Do not expect one model output to become the final page without layout work.

## Quality Review For Generated Images

Reject or revise generated images when:

- They contain fake app screenshots that look like real evidence.
- They include random brand logos.
- Text is garbled or pretending to be meaningful UI copy.
- The visual direction does not match the selected portfolio style.
- The image is too decorative and leaves no usable title/content space.
- It looks like a generic AI poster rather than a UI/UX portfolio asset.
- **It drifts from the PADB on any of the 5 axes (palette, lighting, material, camera, props).** Run the 5-axis consistency QA from `visual-consistency.md` after every batch.

## High-Fidelity Asset Pool Workflow

When the user expects quality similar to the local reference folders:

1. Use the distilled rules in `visual-language.md`, `page-patterns.md`, and `style-directions.md`; do not reread authoring screenshot folders.
2. Write a project-specific visual art direction in 5-8 bullets before prompting.
3. Define forbidden reuse: assets from other projects/themes that must not appear.
4. Generate multiple prompts per page role, not one generic prompt.
5. Generate multiple candidates per key asset.
6. Pick assets by composition, density, lighting, style match, theme specificity, and usable empty space.
7. Place real screenshots or placeholder UI in HTML/PPT after image generation.
8. Keep Chinese title text in HTML/PPT whenever possible. If text must be inside the image, use Nano Banana Pro or a text-strong model.
