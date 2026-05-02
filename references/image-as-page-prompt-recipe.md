# Image-As-Page Prompt Recipe

This file is the **quality contract** for IMAGE_AS_PAGE pages. It exists because "make a magazine-quality portfolio page" is too vague — `gpt-image-2-2k` only delivers editorial-grade output when the prompt names brand identity precisely while leaving the model maximum compositional freedom.

> **Architectural shift (2026-05).** Earlier versions of this recipe pre-locked a "left 45% reserved blank" zone for HTML overlay. That collapsed image2's compositional creativity and produced visually monotonous decks (every page looked like "title-left, phone-right"). The current architecture is the opposite:
>
> 1. The image prompt locks ONLY the brand anchors and density tier, not layout positions.
> 2. image2 composes freely, BUT is forbidden from rendering the editorial text fields that HTML will overlay (title, subtitle, desc, KPI numbers, role chip, section label). Those fields live in `may_overlay_in_html` of the deck plan — see TEXT POLICY in the master template below.
> 3. image2 IS still required to render the deck header bar, footer bar, brand wordmark, and any in-device-screen UI text, because those are visual identity, not editorial copy.
> 4. `scripts/find_blank_zone.py` (multi-zone mode) post-hoc discovers all whitespace regions in the rendered image.
> 5. The Layout Fitter (rule-based, see `references/layout-fitter.md`) decides which `candidate_copy` snippet slots into which discovered zone.
> 6. `scripts/build_interactive_page.py --mode multi-zone` renders the HTML overlay.
>
> The image prompt should describe **WHAT must be true about the image** (palette, anchors, deck-header/footer bars, density) and **WHAT MUST NOT appear as text** (editorial fields), but NOT **WHERE text goes**. Text placement is decided after the image exists. Skipping the "what must not appear as text" half causes duplicated overlays — verified failure mode on lulu/case03 v1.

> **User input wins.** This recipe is a fallback for vague briefs. If the user named a style, supplied hex codes, gave a reference image, or wrote their own image prompt, see `SKILL.md` → User-Authored Input Priority. Use this recipe only to fill slots the user did NOT specify. Never overwrite user-authored values with the 4 preset Directions below.

> **Pipeline contract.** This recipe is invoked by Agent 2 (Page Designer) once per page in `deck-plan.json → pages[]`. It reads `deck` + the single page entry, drafts `candidate_copy`, then writes the image prompt described in §Master Template (Free-Composition Form) below. See `references/deck-plan-schema.md` for the full agent contract.

## The 6 Mandatory Slots (Free-Composition Form)

A page prompt that consistently hits the magazine quality bar contains exactly these 6 slots, in this order. Notice that "left typography zone" and "right mockup" are gone — composition is up to the model.

```text
1. ONE-LINE INTENT          — page role + medium + canvas + density tier
2. PALETTE (LOCKED)         — 4–5 named hex codes with semantic labels (from deck.palette)
3. DECK HEADER + FOOTER     — exact strings for the cross-page header/footer bars
                              (from deck.name / deck.section_label / deck.tagline / deck.designer)
4. ANCHORS (1–4 sentences)  — what MUST be true about the composition; brand anchors only
                              (the device, the hero element on screen, must-bake text strings)
5. PERMISSION                — what the model is encouraged to add freely
                              (floating UI fragments, dimensional tilt, supporting cards,
                               background micro-textures — without spelling out positions)
6. NEGATIVE                 — no watermark / no flare / no grain / no extra logos
                              + density caps from the table below
```

If you are tempted to add a second laptop, a second phone, a popover, a color-swatch card, or a comment bubble: **only encourage them in slot 5 if `density_hint=magazine-dense`**. The slim density tier (`balanced`) caps at 1 main device + 1 floating fragment. The spacious tier caps at 1 main device only.

## Prompt Brevity & Creative Latitude (2026-05 update)

Long prompts ≠ better images. The opposite is true above ~600 words: gpt-image-2-2k slows down (single-image inference grows past 100s, tripping the Cloudflare edge timeout, see `scripts/image_client.py` retry block) AND its compositional creativity degrades because over-specified scenes leave nothing for the model to invent. Verified failure: lulu/case03 v1 prompt at 920 words required 3 retries; the trimmed v2 at 480 words rendered first try.

**Hard targets per page prompt:**
- Total length: **350 – 550 words**. Hard cap 600.
- Anchors slot: **3 – 5 short bullets**, each one sentence. Never enumerate every UI element on a screen — name the top 1–2 hero elements and trust the model.
- Permission slot: **2 – 4 bullets** describing the kind of additions encouraged, not specific positions or counts.
- TEXT POLICY slot: keep ALLOWED list to 3–4 bullets, FORBIDDEN list to the actual fields in `may_overlay_in_html` (1 bullet per field). Do NOT restate full strings twice.

**Brevity heuristics (apply during draft):**
- If you write more than 2 sentences describing what's inside a single device screen, delete down to 2. Name the page title + the single hero element ("a large progress arc" / "one area chart"), drop the rest.
- If you list more than 2 floating cards, cut to 2. Density data: 1 device + 2 cards = safe (~80s render); 1 device + 4 cards = ~140s and frequently times out.
- If a sentence starts with "Decide …" or "You MAY …" — keep one such sentence in slot 5, delete repeats.
- Never repeat hex codes outside slot 2. Never repeat the header/footer literals outside slot 3.
- Negative slot is one line, not a list.

**Creative latitude — what to leave to the model:**
- Lighting direction, shadow softness, ambient highlights.
- Device tilt angle, exact card orbit positions.
- Background micro-textures (paper grain, vignette intensity).
- Decorative accents (one scribble, one underline, one tiny floating toast) — say "1 OR 2 of these are welcome", not "place a +5 toast at upper-left".
- Internal layout of a device screen beyond the named hero element.

**Still always lock:** palette hexes, deck header/footer literals, the TEXT POLICY ALLOWED/FORBIDDEN split, and the **rule that ~35% of the canvas (a single contiguous flat-color region) must be left empty for HTML overlay** — but **NOT which side** that region lives on. The model picks left, right, top, bottom, or diagonal. Variety across pages is desired; identical "title-left, mockup-right" on every page is a regression.

**Anti-pattern (do NOT write this in per-page prompts):**
- "Position the device in the RIGHT HALF of the canvas"
- "The LEFT THIRD must be left flat"
- "One card upper-right, one card lower-right"

**Pattern (DO write this):**
- "The device dominates the composition; place it where it composes best."
- "Two extracted UI cards orbit the device; pick the orbit that breathes."
- "Leave one large contiguous flat-color region (~35% of canvas) somewhere in the composition for editorial breathing room — you decide where (left, right, top, bottom, diagonal)."

Bias toward cutting. If unsure whether a sentence earns its keep, delete it — image2 fills the gap better than another adjective does.

## Master Template (Free-Composition Form)

```text
High-end editorial portfolio <PAGE_ROLE> page, 16:9 landscape (2048×1152), <DENSITY_TIER>. Same visual system as the rest of the <DECK_NAME> deck.

PALETTE (locked, from deck.palette):
- Background: <BG_HEX> with <BG_TEXTURE>
- Ink: <INK_HEX>
- Accent gradient: <ACCENT_START_HEX> -> <ACCENT_END_HEX>
- Secondary: <SECONDARY_HEX> (sparing — used on <SECONDARY_USE>)
- Muted: <MUTED_HEX>

TOP DECK HEADER BAR (full canvas width, ~36px tall, IDENTICAL on every page of this deck):
<HEADER_BAR_LITERAL_FROM_DECK>

BOTTOM DECK FOOTER BAR (full canvas width, ~28px tall, IDENTICAL on every page of this deck):
<FOOTER_BAR_LITERAL_FROM_DECK>

ANCHORS — these MUST be true about the composition:
- <ANCHOR_1>
- <ANCHOR_2>
- (optionally <ANCHOR_3>, <ANCHOR_4>)

COMPOSITION — beyond the anchors, you have full creative freedom:
- Pick the most flattering tilt, lighting, shadow direction, and arrangement.
- You MAY add <PERMITTED_EXTRAS> if it strengthens the editorial composition.
- Leave organic whitespace where it serves the eye — text overlay will be added later, so do NOT pre-flatten any region for it.
- Compose like a real designer, not a wireframe.

TEXT POLICY — what text the image MAY render vs MUST NOT render:
- ALLOWED inside the image:
    * The deck header bar (slot 3) — VERBATIM.
    * The deck footer bar (slot 3) — VERBATIM.
    * Any text inside device screens (UI labels, button labels, body content of the app).
    * Brand wordmark on a device chassis (e.g. small "lulu" logo on the phone shell), if listed in must-bake anchors.
    * Strings explicitly listed in <MUST_BAKE_STRINGS>.
- FORBIDDEN — these will be added by HTML overlay AFTER generation, so the image MUST NOT render them anywhere:
    * Large horizontal Chinese editorial titles (e.g. "会员等级 成长体系").
    * English display subtitles (e.g. "Membership · growth").
    * Multi-line description paragraphs in the editorial canvas (UI body text inside a device is fine).
    * KPI tile rows ("84% / 62% / +2.4×" style number tiles).
    * Role chips (e.g. "Lead Designer · 2025–2026 · Figma · Principle").
    * Section labels (e.g. "CASE 03 · 会员体系") outside the deck header bar.
- The image must therefore leave generous, FLAT-COLOR breathing space where these editorial elements will land. Do not fill every pixel with devices or decorative cards.

CRITICAL:
- All Chinese characters render crisply (PingFang / Source Han Sans), no missing strokes.
- The deck header bar and footer bar must appear EXACTLY as specified, on every page.
- <DENSITY_LIMIT_NEGATIVES based on the chosen density tier>
- No watermark, no flare, no grain artifacts, no extra logos.
- Re-read the TEXT POLICY above. If you are tempted to render a big Chinese title or English subtitle anywhere outside a device screen — DO NOT.
```

Every `<…>` slot must be a concrete string before sending. No leftover placeholders. No "lorem ipsum" / `示例文案` / `xxx`.

## Header / Footer Bar Literals (3 styles)

The deck plan field `header_style` / `footer_style` resolves to one of these literal strings. Use VERBATIM in slot 3.

| `header_style` | Header bar literal (substitute `<DECK_NAME>`, `<SECTION_LABEL>`, `<PAGE_ROLE_LABEL>`) |
|---|---|
| `dot-deckname-section` | `Left: small filled-then-empty dot pair "● ○" + "<DECK_NAME>" in <INK_HEX> 13pt PingFang Semibold. Right: "<SECTION_LABEL>  /  <PAGE_ROLE_LABEL>" in <MUTED_HEX> 12pt. 1px hairline rule directly below the bar, <MUTED_HEX> opacity 30%.` |
| `email-nav` | `Left: "<DESIGNER_NAME>@example.com" in <MUTED_HEX> 12pt. Right: "WORK · ABOUT · CONTACT" in <INK_HEX> 12pt letter-spaced 0.1em, the active section "<PAGE_ROLE_LABEL>" underlined in <ACCENT_START_HEX>. 1px hairline rule below, <MUTED_HEX> opacity 25%.` |
| `serial-tagline` | `Left: serial number "P. <PAGE_NUM> / <TOTAL>" in <MUTED_HEX> 11pt monospaced. Right: "<DECK_NAME> · <SECTION_LABEL>" in <INK_HEX> 12pt. 1px hairline rule below, <MUTED_HEX> opacity 30%.` |

| `footer_style` | Footer bar literal (substitute `<DECK_TAGLINE>`, `<DESIGNER_NAME>`) |
|---|---|
| `dot-tagline-wordmark` | `Left: "● ( <DECK_TAGLINE> )" in <MUTED_HEX> 11pt. Right: "<DESIGNER_NAME> PORTFOLIO" in <INK_HEX> 12pt letter-spaced 0.15em. 1px hairline rule directly above, <MUTED_HEX> opacity 30%.` |
| `copyright-stamp` | `Centered: "© <YEAR> <DESIGNER_NAME>. ALL RIGHTS RESERVED." in <MUTED_HEX> 11pt letter-spaced 0.2em. No rule.` |
| `pagenum-only` | `Right: serial number "<PAGE_NUM> / <TOTAL>" in <MUTED_HEX> 11pt monospaced. No rule.` |

Pick ONE header style + ONE footer style at the deck level (`deck.header_style`, `deck.footer_style`) and reuse on every page. Mismatched bars across pages = the #1 reason the output stops feeling like "one deck".

## Density Tier → Permitted Composition

| `density_hint` | Main devices | Floating fragments | Background extras | Best for |
|---|---|---|---|---|
| `spacious` | 1 (or 1 still-life) | 0 | calm, very subtle texture only | covers, section dividers, closing pages |
| `balanced` | 1 | 1 (toast, badge, swatch chip) | 1 supporting still-life element OK | most case-study hero pages |
| `magazine-dense` | 1 + 3–4 extracted UI cards orbiting it | 1 (only if it strengthens) | scribble accents, hand-drawn arrows, sub-feature bullet row | feature breakdown / membership tiers / data dashboard pages |

The Page Designer agent picks the tier from `deck-plan.json → pages[].density_hint`. Defaults: cover→spacious, case-study→balanced, design-system/process→magazine-dense.

## Style-Direction Fillings

Each direction below gives a concrete palette + tone-of-voice. The deck plan's `deck.palette` should derive from one of these (or be user-supplied verbatim).

### Direction 1 — Dark-Tech Editorial

```text
BG_HEX:                #0A0E1A
BG_TEXTURE:            faint blueprint dot grid (1px dots, ~24px spacing, opacity 6%)
INK_HEX:               #F5F6FA
ACCENT_START_HEX:      #3B5BFF
ACCENT_END_HEX:        #7B6BFF
SECONDARY_HEX:         #38E1FF
SECONDARY_USE:         AI-suggestion popover left border, focus chip border
MUTED_HEX:             #8A93B8
SIDEBAR_BG_HEX:        #0F1428
CANVAS_BG_HEX:         #0E1426
KPI_BORDER_HEX:        #2A3358
BAR_BG_HEX:            #141A36
ENGLISH_SUBTITLE_FONT: italic display serif (think Tiempos / GT Sectra)
CJK_TITLE_FONT:        Source Han Sans Heavy / PingFang SC Semibold
DEVICE_MATERIAL:       silver #C8CDDA
```

Tone for description lines: factual, present tense, one observed outcome with a real number. Example:
"为内容创作者重新设计的 AI 编辑器，把指令、补全、引用整合到同一个写作流。上线 6 个月活跃用户增长 3.4×。"

Best for: AI products, dev tools, B-side SaaS, command-center, fintech.

### Direction 2 — Warm Commercial Editorial

```text
BG_HEX:                #FAF4E8 (warm cream)
BG_TEXTURE:            very fine paper noise + faint horizontal serif rules at section breaks
INK_HEX:               #1B1A17 (warm near-black)
ACCENT_START_HEX:      #D9531E (terracotta)
ACCENT_END_HEX:        #E8A23C (amber)
SECONDARY_HEX:         #2E6F4E (muted forest)
SECONDARY_USE:         price tag / verified badge / on-sale chip
MUTED_HEX:             #7A7468
SIDEBAR_BG_HEX:        #FFFFFF
CANVAS_BG_HEX:         #FBF7EE
KPI_BORDER_HEX:        #E2D9C6
BAR_BG_HEX:            #FFFFFF
ENGLISH_SUBTITLE_FONT: italic editorial serif (Caslon / Freight Big Pro)
CJK_TITLE_FONT:        阿里巴巴普惠体 Heavy / OPPOSans Heavy
DEVICE_MATERIAL:       champagne aluminum #D6CDB8 / matte cream
```

Tone: narrative, lifestyle-led, end with a concrete consumer impact. Example:
"为本地烘焙店设计的会员小程序，把订单、卡券、配送整合到同一屏。试运营 3 个月复购率从 18% 升到 41%。"

Best for: ecommerce, lifestyle apps, F&B, retail SaaS, content platforms.

### Direction 3 — Clean Product Case (Light B-side SaaS)

```text
BG_HEX:                #F4F6FB
BG_TEXTURE:            8px dot grid in #E1E6F2, opacity 50%
INK_HEX:               #0F172A
ACCENT_START_HEX:      #2962FF
ACCENT_END_HEX:        #5C7CFA
SECONDARY_HEX:         #00B894
SECONDARY_USE:         success state, status pill
MUTED_HEX:             #64748B
SIDEBAR_BG_HEX:        #FFFFFF
CANVAS_BG_HEX:         #FFFFFF
KPI_BORDER_HEX:        #D6DEEC
BAR_BG_HEX:            #F1F5FB
ENGLISH_SUBTITLE_FONT: clean grotesk italic (Söhne / Inter Display Italic)
CJK_TITLE_FONT:        HarmonyOS Sans SC Bold / MiSans Bold
DEVICE_MATERIAL:       space-grey aluminum #43474D
```

Tone: analytical, comparative, names a baseline before the improvement. Example:
"为客服后台重新设计的工作台，把话术、订单、知识库整合到同一屏。AHT 从 6.2 分钟降到 3.7 分钟（-41%）。"

Best for: enterprise SaaS, admin consoles, internal tools, hiring portfolios for B-side teams.

### Direction 4 — Magazine-Editorial (Consumer / Story-led)

```text
BG_HEX:                #F2EEE7 (newsprint warm grey)
BG_TEXTURE:            very subtle vertical newsprint columns (light dividers at 1/3, 2/3)
INK_HEX:               #14110D
ACCENT_START_HEX:      #B0231C (signal red)
ACCENT_END_HEX:        #14110D (lets red stand alone — gradient is mostly the red)
SECONDARY_HEX:         #2A4D9C (link blue)
SECONDARY_USE:         pull-quote underline, footnote markers
MUTED_HEX:             #7B7468
SIDEBAR_BG_HEX:        #14110D (inverted dark sidebar)
CANVAS_BG_HEX:         #FFFFFF
KPI_BORDER_HEX:        #C9C2B5
BAR_BG_HEX:            #14110D (inverted)
ENGLISH_SUBTITLE_FONT: large display serif (GT Super / Domaine Display)
CJK_TITLE_FONT:        思源宋体 Heavy (use a SERIF for CJK title in this direction)
DEVICE_MATERIAL:       matte black with bright bezel reflection
```

Tone: narrative, voice-led, second-person allowed, ends on a sensory detail.

Best for: lifestyle apps, creator tools, brand identity case studies, consumer storytelling.

## Composition Direction — Direct the scene, not the screws

This is the rule that separates a "magazine cover" from a "Figma frame export". The lulu test (2026-05) made it obvious: when the prompt enumerates every status-bar icon, every spec row, every button label inside the device, two bad things happen at once:

1. **Density blows up** → 524 timeout (we already cap this in the table below).
2. **The model loses creative agency** → the output looks flat, like a wireframe ported to PNG. No 12° tilt, no floating UI fragment, no dimensional shadow play, no editorial composition. Just a phone screenshot pasted onto cream paper.

The reference is the Dec 2025 purple-deck cover (3D tilted MacBook + floating comment popup + "UIUX" 3D chip + color-swatch chip + designer-info card). It works because the prompt named the **anchors**, not the **rows**.

### What to LOCK (must specify)

These pin brand identity and prevent the model from drifting:

- Palette hexes (4–5, with semantic role)
- App / brand name as a real string in the mockup
- The ONE hero anchor inside the screen (the photo of grapes, the dashboard chart, the chat thread title) — described in 1 sentence
- 1–2 must-have UI landmarks that prove "this is the right product" (price chip with currency + amount, primary CTA label, sidebar nav set) — each in 1 sentence
- Top-right corner block + bottom-right corner block (these are deck-consistency anchors)

### What to LEAVE OPEN (let the model compose)

- Exact icon set in the status bar / nav bar / tab bar
- Whether to render 12° isometric / face-on / floating-perspective
- Whether to add a **secondary floating fragment** (a popover detached from the device, a 3D chip, a color-swatch card) — encourage with "may include 1 floating UI fragment in the same palette" and let the model pick
- Exact shadow direction, exact lighting temperature
- Supporting hairline rules, sub-labels, secondary text inside the device — describe the *kind* of content, not the literal strings (`"three short product spec rows in the same hairline style"` beats `"产地 / 云南; 规格 / 1kg; 保鲜 / 当日达"`)
- Background micro-textures (paper noise / dot grid / vignette gradient) — give a budget like "very subtle", not a pixel spec

### Anchor + Permission template (replace verbose UI enumeration)

```text
RIGHT 55% — ONE hero <DEVICE> mockup, free composition:
- A photo-realistic <DEVICE> in <MATERIAL>, free to tilt 0°–15°, casting a soft natural shadow.
- The screen shows <APP_NAME> <PAGE_TYPE>, with these locked anchors:
    · <HERO_ELEMENT_ONE_SENTENCE>
    · <PRIMARY_CTA_OR_PRICE_CHIP>
    · <ONE_BRAND_LANDMARK>
- Beyond these anchors, compose the rest of the screen freely in the palette: a believable <PAGE_TYPE>, with the kind of supporting content a real <APP_NAME> page would carry.
- You MAY add up to ONE floating UI fragment outside the device (a detached popover, a 3D color-swatch chip, a small notification card) in the same palette, if it strengthens the composition. Skip it if it crowds.
```

### Lulu case-01 — verbose vs free

```text
[VERBOSE — kills both density and creativity]
- iOS status bar (9:41, signal, battery)
- Top nav row: back chevron · share · cart icon
- Hero photo filling 55% of screen height: grapes on wooden board
- Title row: "云南阳光玫瑰 · 1kg" 17pt bold #1A1410
- Price row: "¥38" amber + struck-through "¥58" small muted
- Three short spec rows separated by 1px hairlines: "产地 / 云南", "规格 / 1kg", "保鲜 / 当日达"
- Sticky bottom: outlined "加入购物车" button + filled gradient "立即购买" button
- iOS home indicator

[FREE — same brand identity, breathing room, model gets to design]
- A photo-realistic iPhone 15 Pro in matte titanium, free to tilt 0°–15°, soft natural shadow on cream surface.
- Screen shows the lulu product detail page for "云南阳光玫瑰 · 1kg", with these locked anchors:
    · A bright daylight hero photo of one cluster of plump green grapes on a wooden board (top half of screen).
    · A large amber "¥38" price chip with a struck-through "¥58" beside it.
    · A primary gradient "立即购买" CTA at the bottom in the marigold→amber gradient.
- Compose the rest of the screen freely as a believable lulu detail page in the warm cream palette.
- You MAY include ONE floating UI fragment outside the phone — a detached "加入购物车成功" toast or a 3D "FRESH" badge — in the same palette, only if it strengthens the editorial composition.
```

The free version has roughly the same token count as the verbose one, but spends those tokens on **what must be true** instead of **what every pixel looks like**. That gives gpt-image-2-2k the dimensional, editorial output we actually want.

## Magazine-Dense Layout Patterns — Earn the "real portfolio" feel

Verified against two production Chinese UI/UX portfolio decks (HAOHAN 2025, Cease 2025) ingested 2026-05-01. Both decks consistently outperform our earlier "title-left + ONE phone-right" output, and the gap is **not** image quality — it is composition density.

### What the reference decks have that our pages don't

1. **Deck-level header bar** across the top of every page (~3% canvas height):
    `● ○  Cease 2025` left  ·  `UX/UI DESIGN  /  项目复盘` right (or designer's email + section nav)
    This is the single biggest "this is a deck, not a poster" signal. EVERY page in the deck must carry it, identical position and styling.
2. **Deck-level footer bar** across the bottom (~2.5% canvas height):
    `● ( 唯熱愛可抵歲月漫長 )` left tagline  ·  `HAOHAN PORTFOLIO` right wordmark
3. **Multi-element grid composition** instead of "one big mockup":
    A center phone surrounded by 4 product extracts, OR 3 description columns + center phone + 3 annotation cards, OR 2 phones staggered with magnified KPI glass-cards floating beside them.
4. **Floating supporting cards are EXTRACTS of the same product**, not marketing trinkets:
    Magnified level badges, magnified KPI numbers ("3829 人次"), magnified component samples — never coupons / mascots / 3D logos.
5. **Hand-drawn or scribbled accent under the English subtitle**:
    A messy underline / strike-through / arrow drawn through "Core Features Display" or "design" — gives the page a designer-not-AI signature.
6. **Bullet sub-features with arrow connectors**:
    `○ 金刚区  根据商家需求…` — small filled circle marker + 2-line description, arranged as a column of 2–3 items.
7. **The page uses the FULL canvas** — no reserved blank zone for HTML overlay. Editable mode actively works against this density. Use editable mode only when the user explicitly asks for in-browser editing; otherwise let the image carry all the text.

### Three named layout patterns

Pick ONE per page. Reuse across the deck for rhythm, but rotate so adjacent pages aren't identical.

#### Pattern A — Hero device + 4 corner extracts (商家等级 / 卡片矩阵)

```text
Top deck header bar (full width, thin)
LEFT 30%:
    Bold CJK title (96pt) + small italic English subtitle with hand-drawn underline
    1-line role/section caption underneath
CENTER 30%:
    ONE photo-realistic phone (or browser frame) showing the main screen,
    standing upright, ~60% canvas height, soft floor shadow
FOUR CORNERS around the phone (NE, NW, SE, SW):
    Four extracted UI cards from the same app — each a real-data card
    (a level badge, a KPI tile, a banner thumbnail, a status chip)
    sized ~18% canvas width, soft drop shadow, slight 3° tilt for life
BOTTOM 8%: bullet-row of 3 sub-feature labels
Footer bar (full width, thin)
```

#### Pattern B — Description column + center phone + annotation column (核心功能展示)

```text
Top deck header bar
LEFT 36% (description column, white-on-dark or ink-on-cream):
    Bold CJK section title + italic English subtitle (with scribble accent)
    Two paragraph blocks (each: small section header + 3-line body)
    Bullet KPI line at bottom
CENTER 28% (phone, full readable UI screenshot)
RIGHT 36% (annotation column):
    3 sub-feature cards stacked: small filled circle marker + bold sub-title +
    2-line description, with a faint arrow pointing from each card toward
    the relevant area on the phone screen
Footer bar
```

#### Pattern C — Two staggered phones + floating glass KPI cards (数据看板分析)

```text
Top deck header bar
LEFT 35%:
    Bold CJK title + italic English subtitle (hand-drawn underline)
    1-paragraph project intro (4 lines, 18pt)
RIGHT 65%:
    Two photo-realistic phones, staggered with overlap, slight 5°–10° tilt,
    one in front (full screen visible) one behind (partial)
    Beside/above the phones: TWO floating dark-glass KPI cards, each magnifying
    one number from the on-screen UI ("3829 人次 ↑", "98.9% 用户满意度 ↑"),
    rounded 16px, blurred drop shadow, glass blur ~12px
Footer bar
```

### What to LOCK + what to LEAVE OPEN (for any pattern)

LOCK: deck-header text exact strings, deck-footer text exact strings, palette hexes, app/brand name, the chosen pattern letter (A / B / C), the ONE main screen the phone displays, and the 1-sentence hero anchor inside that screen.

LEAVE OPEN: exact tilt angles, exact card positions inside the chosen grid, exact icons on extracted cards, exact glass-blur strength, exact shadow direction, the supporting micro-copy on extracted cards (let the model write plausible domain copy in the locked palette).

### Density vs timeout — Magazine-dense is still safe

Multi-element compositions sound like they violate the Density Limits table. They don't, because each "extracted card" is a small, low-detail panel (one number + one label + one icon), not a second full device. The 2K timeout budget tracks **rendered surface complexity**, not element count. Empirically:

| Composition | Surface complexity | 2K outcome |
|---|---|---|
| 1 main device + 4 mini extract cards (each 18% width, single KPI) | LOW | passes |
| 1 main device + 1 second floating coupon | LOW | passes |
| 1 main device with verbose enumerated UI inside (every row spelled out) | HIGH | times out |
| 2 main devices each with full UI | HIGH | times out |

Rule of thumb: a "card" worth one number + one label is 1/10 the cost of a "device" with a full UI. Spend the budget on **many small cards around one well-described device**, not on stuffing the device or adding a second one.

### Recipe addendum — required cross-page anchors

For any deck of ≥3 pages, every IMAGE_AS_PAGE prompt MUST include these two lines verbatim (substituting the project's deck-name / designer-name once and reusing across all pages):

```text
Top deck header bar (full canvas width, ~36px tall): "● ○  <DECK_NAME>" left in <INK_HEX> 13pt, "<SECTION_LABEL>  /  <PAGE_TYPE_LABEL>" right in <MUTED_HEX> 12pt. 1px hairline rule below in <MUTED_HEX> opacity 30%.
Bottom deck footer bar (full canvas width, ~28px tall): "● ( <DECK_TAGLINE> )" left in <MUTED_HEX> 11pt, "<DESIGNER_NAME> PORTFOLIO" right in <INK_HEX> 12pt letter-spaced. 1px hairline rule above in <MUTED_HEX> opacity 30%.
```

These bars are what convert "an image with a phone in it" into "page 4 of a portfolio deck".

## Density Limits (origin-timeout safety)

`gpt-image-2-2k` on the pockgo relay times out (HTTP 524) when prompt complexity pushes generation past ~120s. Empirically verified element budget per page:

| Element | Allowed | Notes |
|---|---|---|
| Main device (laptop OR desktop browser OR phone) | 1 | Required |
| In-frame UI elements (sidebar + canvas + 1 popover/card/bar) | up to 3 named | Each adds ~10–20s |
| KPI tiles | 3 | Sweet spot |
| Role chip line | 1 row | Single line of 3–5 chips |
| Floating secondary devices (phone next to laptop, etc.) | **0 in 2K mode** | Add only at 1x model |
| Floating annotation cards / color tokens | **0 in 2K mode** | Add only at 1x model |
| Comment bubbles / popovers OUTSIDE the main device | 0 | Always cut |
| Corners (PORTFOLIO mark + copyright) | 2 | Required |

If a page concept needs more than this, **split into two pages** (case-study hero + a second "detail" page that zooms into the cut elements). Do not stuff one prompt past the budget.

## Self-Check Before Sending The Prompt

Before calling `image_client.py generate`, verify:

- [ ] All `<…>` slots filled with concrete strings (no placeholders, no lorem).
- [ ] Palette has exactly 4–5 hex codes with semantic labels.
- [ ] CJK title and English subtitle are BOTH provided (the gradient title is always CJK; the italic serif line is always English).
- [ ] All 3 description lines are real domain copy with at least one concrete number or proper noun.
- [ ] Every KPI tile has label + number + sub-label (not "KPI1 / TBD / TBD").
- [ ] Sidebar nav lists 4 real menu items in CJK (not "Menu1 / Menu2").
- [ ] Main canvas content is one specific real-looking content block (a doc title + 3 paragraphs, OR a chat with 2 named bubbles, OR an order card with 5 named fields, etc.) — not "some content".
- [ ] Bottom command bar has a real placeholder + a real keyboard hint.
- [ ] Element count is within the Density Limits table for 2K mode.
- [ ] Negative section explicitly forbids: watermark, flare, grain, extra logos, AND any element not named in the prompt.

If any box is unchecked, fill it before sending. The model fills empty slots with template defaults, and template defaults look like AI slop.

## Failure Recipes (do NOT use)

These are real anti-patterns observed during the 2026-05 verification run.

```text
[BAD] "Make a beautiful AI writing app portfolio page, dark theme, with mockups"
       → Generic dark-purple slop, fake English UI, garbled CJK.

[BAD] "Use the lumen style"
       → Model has no memory of "lumen". Always re-paste the full template.

[BAD] "Same as previous page but different project"
       → For a NEW project, re-pick the Style Direction, re-fill all 7 slots.
         Cross-project reuse is forbidden by visual-consistency.md anyway.

[BAD] Adding "popover + phone + color-swatch card + comment bubble" to one prompt
       → 3× HTTP 524 timeout at 2K. Cut to one main device + one in-frame popover max.

[BAD] Enumerating every UI row inside the device screen
       (status bar icons + nav icons + 4 spec rows + 2 buttons + tab bar + home indicator)
       → Doubles density AND collapses the model's composition agency.
         Output looks like a wireframe export, not a magazine page.
         Use the Anchor + Permission template above instead — name 2–3 anchors,
         then "compose freely in the palette".
```
