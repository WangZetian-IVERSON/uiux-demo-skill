# Image Style Presets

> ⚠️ **SCOPE — 2026-05-02 更新**
> 这个文件里的 12 个 preset **仅适用于海报、品牌视觉、editorial 静物、campaign 主视觉** —— 它们都是杂志/海报范式的视觉 DNA。
>
> **禁止用于** UIUX 作品集的封面 / 案例 / anatomy / process / system 页面 —— 那些走 `image-prompt-style-uiux.md`（产品 mockup + flat BG 范式）。
>
> 误用症状：图里出现钢笔、咖啡渍、手写笔记、便签、纸张材质。一旦看到，立刻切到 `image-prompt-style-uiux.md` 重写 prompt。

Curated preset library for the **Lean Natural-Language Mode** (see `image-generation-protocol.md`).

## Why presets

Letting the LLM re-invent "lighting + lens + material + palette + reference" inside every per-page prompt is the single biggest source of style drift across a deck. Two adjacent pages end up looking like they were shot by different photographers because the model saw two slightly different paragraphs. Presets fix this by **moving the style DNA out of the prompt and into a name**.

Inspired by `frontend-slides` (zarazhangrui — 12 curated style presets, "show-don't-tell" picker) and `huashu-design` (alchaincyf — 20 design philosophies × 5 schools, anti-AI-slop rules).

## How to use

1. Pick **one** preset for the whole deck (or run 3 covers in parallel under 3 presets and let the user pick — the "show-don't-tell" workflow).
2. In every page prompt, the **first line** is `preset: <slug>`. Do NOT re-describe the preset's lighting/lens/material/palette inside the prompt body.
3. The body becomes radically shorter — see `image-generation-protocol.md` § "Lean prompt anatomy with preset" for the 3-section template (~60–120 words).
4. The closing line is the fixed anti-slop tail (also defined in protocol).

## Anti-AI-slop blacklist (applied to every preset)

These are forbidden across the entire skill regardless of preset choice. Both `huashu-design` and `frontend-slides` independently converged on this exact list:

- purple gradients (any), neon-purple-on-white
- emoji-style icons, sticker-art elements
- generic glow / radial-blur halos around products
- rounded card with left accent border (the "AI dashboard tile" cliché)
- SVG-painted human faces / mascots
- Inter / Helvetica used as display font for big headings (these are body fonts)
- plastic-shiny over-rendered product visuals (the Midjourney-default look)
- generic "futuristic dashboard with floating UI panels in space" composition
- corporate gradient stock-photo people in white shirts
- food / drink with steam volumetrically rendered for no narrative reason

This list is enforced via the **fixed negative tail** appended to every lean prompt — agents do not need to re-list these.

---

## Preset library (12 entries)

Each preset is intentionally short (≤ 8 lines) so it can be consumed by the LLM without crowding the prompt.

### `cinematic-velvet-jewel`

- light: single warm key from upper-left, deep falloff, no fill light
- lens: 85mm-equivalent, f/1.8, shallow depth of field
- material: brushed brass, oxblood velvet, oil-rubbed walnut, dark glass
- palette: oxblood + ember + champagne gold + deep brown
- reference: Wong Kar-wai still / Pentagram product photography / Aesop in-store shoot
- mood: a small luxury at midnight
- best_for: e-commerce festival cover, premium brand cover, food-and-drink hero
- avoid_for: enterprise SaaS, data dashboards, dev tools

### `swiss-editorial-grid`

- light: soft north-facing daylight, even, no shadow drama
- lens: 50mm flat perspective, no DOF tricks
- material: matte paper, ink, raw plywood, brushed aluminum
- palette: paper white + ink black + one single accent (project-defined, single hue)
- reference: Bauhaus / Massimo Vignelli / Lars Müller editorial books
- mood: confident silence
- best_for: information design, infographic, B2B SaaS case, dev tooling
- avoid_for: festival, fashion, food, anything emotional

### `dark-botanical-sanctum`

- light: warm museum spotlight from upper-right, soft secondary fill
- lens: 100mm macro, medium DOF, slight tilt-shift
- material: rich green velvet, aged brass, dried botanicals, beveled glass
- palette: deep forest + moss + aged brass + bone white
- reference: Aesop catalog / Apartamento magazine / V&A still life
- mood: a librarian's secret garden
- best_for: lifestyle app, wellness, content product, slow-luxury brand
- avoid_for: speed/performance products, financial tools, gamified UX

### `editorial-paper-ink`

- light: flat overcast daylight, no rim
- lens: 35mm, slight overhead tilt
- material: textured cotton paper, India ink, letterpress imprint, riso print
- palette: bone white + warm grey + one ink color (deck-defined)
- reference: The New York Times Magazine / Apartamento / Phaidon photo books
- mood: a long-form essay's opening spread
- best_for: case-study covers, narrative section openers, long-read decks
- avoid_for: kinetic product reveals, festival energy

### `brutalist-concrete`

- light: harsh single direction, raking shadows
- lens: 24mm wide, slight architectural distortion
- material: raw concrete, exposed steel, sandblasted glass, naked LED tubes
- palette: bare concrete + steel grey + one toxic accent (lime / hot pink / safety orange)
- reference: Balenciaga campaign / Pentagram for music labels / OFFF poster
- mood: anti-fashion, fashion
- best_for: design-tool product, creative-platform, edgy startup
- avoid_for: finance, healthcare, family products

### `nocturne-festival`

- light: multi-source warm street lights, lantern bokeh in deep background
- lens: 50mm, medium DOF, strong color saturation in highlights
- material: silk, lacquer, polished metal, paper lanterns
- palette: deep indigo + crimson + festival gold + smoke
- reference: In the Mood for Love (closing scene) / Wong Kar-wai night street / 张叔平 still
- mood: the city is celebrating something quietly
- best_for: Chinese e-commerce festivals (618 / 双11 / 年货节), Lunar / Mid-Autumn campaign
- avoid_for: minimal product covers, B2B

### `rose-minimal-studio`

- light: large soft box from front, trace shadow only
- lens: 90mm, flat compression, sharp throughout
- material: ceramic, soft fabric, blush paper, satin metal
- palette: blush + warm white + soft taupe + a single deep contrast (charcoal or bordeaux)
- reference: Glossier campaign / Aesop minimal shot / Kinfolk product page
- mood: quiet feminine confidence
- best_for: beauty, lifestyle, wellness, soft-luxury, DTC
- avoid_for: fintech, dev tools, anything aggressive

### `arcade-neon`

- light: hard cyan key + magenta rim + practical neon signs in scene
- lens: 28mm wide, slight anamorphic flare
- material: acrylic, polished plastic, fogged glass, wet asphalt reflections
- palette: cyan + magenta + acid yellow on near-black
- reference: Blade Runner 2049 / Refik Anadol / 80s arcade signage
- mood: tomorrow's nostalgia
- best_for: gaming product, music app, late-night content, web3 / crypto
- avoid_for: enterprise, healthcare, education

### `sunbleached-archive`

- light: bright midday sun, slight overexposure, lens flare allowed
- lens: 35mm film, visible grain, faded contrast
- material: faded paper, sun-bleached plastic, vintage metal, masking tape
- palette: bone + faded khaki + sun-yellow + dusty teal
- reference: William Eggleston / Stephen Shore / 90s zine archive
- mood: a polaroid you forgot in a drawer
- best_for: archive products, journaling apps, slow-tech, indie tools
- avoid_for: festivals, premium luxury, anything "new"

### `monastic-stillness`

- light: single high window, long shaft of light, deep negative space
- lens: 50mm, very deep shadows, almost monochrome
- material: raw linen, unfinished wood, hand-thrown ceramic, rough stone
- palette: bone + warm grey + one earth tone (clay / ochre / deep moss)
- reference: Axel Vervoordt interiors / Joseph Dirand / Rick Owens furniture
- mood: a chapel of one product
- best_for: meditation app, reading product, single-feature hero, philosophy-driven brand
- avoid_for: dense feature reveals, festivals, enterprise dashboards

### `tactile-laboratory`

- light: even cool overhead with one warm accent
- lens: 60mm macro, surgical sharpness, no DOF
- material: brushed steel, frosted glass, calibration grids, technical paper
- palette: cool grey + bone + one signal color (caution yellow / blueprint cyan / lab green)
- reference: Dieter Rams Braun catalog / IDEO method cards / NASA technical photo
- mood: serious craft, no decoration
- best_for: developer tool, design-system docs, scientific instrument, B2B precision
- avoid_for: emotional / lifestyle / fashion

### `night-market-banquet`

- light: practical hanging warm bulbs, multi-shadow, food-stall heat shimmer
- lens: 35mm, eye-level, slight crowd compression
- material: enamel, cast iron, paper menu, condensed glass, hand-written cardboard
- palette: deep night + pork-fat amber + chili red + chive green
- reference: 是枝裕和 / Tampopo / Asian night-market documentary photography
- mood: the city eats together at 11pm
- best_for: food-delivery campaign, restaurant product, neighborhood-app cover, festival food vertical
- avoid_for: minimal product, fintech, enterprise

---

## Picking a preset (when you don't know)

Run the **show-don't-tell** workflow (borrowed from `frontend-slides`):

1. Pick 3 presets that span the project's plausible range (e.g. `cinematic-velvet-jewel` + `nocturne-festival` + `swiss-editorial-grid` for a JD 618 deck — premium / festival / editorial).
2. Generate the **cover only** under each preset, in parallel.
3. Show the user the 3 covers side-by-side and let them pick one.
4. Lock that preset for the rest of the deck.

Cost: 3 cover generations (~9 credits each at gpt-image-2 high) ≈ 27 credits. Worth it to avoid 6 case-page reshoots later.

## Adding a new preset

A preset belongs in this file only if it can be described in **≤ 8 lines** and it covers a project shape not already served by an existing preset. If it overlaps an existing preset by > 60 %, extend the existing one with a `variant` line instead of adding a new preset.
