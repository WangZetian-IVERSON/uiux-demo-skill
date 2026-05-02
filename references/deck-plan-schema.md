# Deck Plan Schema

The `deck-plan.json` is the **single source of truth** that bridges the three agents:

```
Agent 1 (Project Planner)  →  deck-plan.json  →  Agent 2 (Page Designer, per page)  →  image2 prompts + content drafts
                                                              ↓
                                     find_blank_zone.py multi-zone scan
                                                              ↓
                                     Agent 3 (Layout Fitter, rule-based by default)
                                                              ↓
                                     build_interactive_page.py multi-zone overlay
                                                              ↓
                                     Final HTML deck
```

This file defines that JSON contract. Any tool that reads or writes a deck plan MUST conform.

## Why a plan file at all

Earlier iterations of this skill baked layout decisions (e.g. "left 45% reserved blank") into the image prompt itself. That collapses image2's compositional creativity and produces visually monotonous decks. The fix is to let image2 compose freely, then discover whitespace post-hoc and slot text into whatever the model actually drew.

`deck-plan.json` is the upstream artifact that lets us do that without losing cross-page consistency: every page references the same `deck` block (palette, header bar text, footer bar text, designer name) so the model's free composition still feels like ONE deck.

## Top-level shape

```json
{
  "schema_version": "1",
  "deck": { ... global, identical across all pages ... },
  "pages": [
    { ... page 1 ... },
    { ... page 2 ... }
  ]
}
```

## `deck` block (cross-page anchors — never change between pages)

```json
{
  "name": "lulu 2026",
  "designer": "WANGZETIAN",
  "tagline": "把日常採買變成一件值得期待的小事",
  "section_label": "UX/UI DESIGN",
  "header_style": "dot-deckname-section",
  "footer_style": "dot-tagline-wordmark",
  "palette": {
    "bg": "#FFF6E1",
    "ink": "#1A1410",
    "accent_start": "#F5B700",
    "accent_end": "#E8851A",
    "secondary": "#2B5C40",
    "muted": "#8B7355"
  },
  "fonts": {
    "cjk_display": "PingFang SC Heavy",
    "cjk_body": "PingFang SC Regular",
    "en_display": "Cormorant Garamond Italic",
    "en_body": "Inter"
  },
  "style_direction": "warm-commercial",
  "canvas": { "w": 2048, "h": 1152 }
}
```

Field rules:

- `name` — short deck title; appears in header bar verbatim.
- `designer` — appears in footer bar verbatim, suffixed by " PORTFOLIO".
- `tagline` — appears in footer bar wrapped in `( ... )`.
- `section_label` — appears in header bar; usually `UX/UI DESIGN` or `BRAND DESIGN`.
- `header_style` / `footer_style` — pick from the 3 styles documented in `references/page-patterns.md` § Header & Footer Styles. Choose ONE and reuse on every page.
- `palette` — exactly these 6 semantic keys; see `image-as-page-prompt-recipe.md` for hex selection.
- `style_direction` — one of `dark-tech`, `warm-commercial`, `clean-product`, `magazine-editorial` (matches the 4 directions in the recipe).
- `canvas` — currently always 2048×1152 (gpt-image-2-2k 16:9). Don't change without verifying timeout budget.

## `pages[]` block (one entry per page)

```json
{
  "id": "case-03-membership",
  "page_type": "case-study",
  "page_role_label": "会员体系",
  "intent_one_line": "讲清楚 lulu 会员体系是如何把消费动作变成可见的成长。",
  "device_hint": "phone",
  "density_hint": "magazine-dense",
  "compose_freedom": "high",
  "page_pattern": "hero-device-orbit",
  "breathing_region": "left",
  "anchors": [
    "phone screen shows the lulu 会员中心 page with progress arc 'Lv3 金卡会员 68/80'",
    "four membership tier badges (Lv1 銅 / Lv2 銀 / Lv3 金 / Lv4 鑽石) shown as extracted UI cards",
    "tagline scribble underline through the word 'growth' under the english subtitle"
  ],
  "candidate_copy": {
    "section_label": "CASE 03 · 会员体系",
    "title_zh": "会员等级 成长体系",
    "subtitle_en": "Membership · growth",
    "desc": "重新设计 lulu 会员体系。每一次消费都可见地推进等级，每一级都对应可感知的回馈。",
    "kpis": [
      { "key": "active",  "label": "会员活跃", "number": "84%", "sub": "环比 +18pt" },
      { "key": "ltv",     "label": "LTV",     "number": "+2.4×", "sub": "金卡 vs 普通" },
      { "key": "rebuy",   "label": "复购率",  "number": "62%", "sub": "金卡用户" }
    ],
    "role": "Lead Designer · 2025–2026 · Figma · Principle"
  },
  "must_bake_in_image": [],
  "may_overlay_in_html": ["section_label", "title_zh", "subtitle_en", "desc", "kpis", "role"]
}
```

Field rules:

- `id` — kebab-case, used as filename stem (`case-03-membership.png`, `.html`, `.zone.json`).
- `page_type` — one of `cover`, `toc`, `case-study`, `process`, `design-system`, `before-after`, `closing`. Drives default device/extracts; see `references/page-type-routing.md`.
- `page_role_label` — short Chinese label that appears in header bar's right side (e.g. `会员体系`, `首页改版`).
- `intent_one_line` — ONE sentence. The Page Designer agent uses this as the north star.
- `device_hint` — `phone` / `laptop` / `desktop-browser` / `tablet` / `still-life` / `none`. Page Designer may override if a different device serves the intent better.
- `density_hint` — `spacious` (cover-style, lots of breathing) / `balanced` (1 device + 1 floating) / `magazine-dense` (Pattern A/B/C from the recipe).
- `page_pattern` — visual composition pattern, **must be different from the previous page's pattern in the same deck** (variety is enforced). Pick one of: `hero-device-orbit` (one main device + 2 floating UI cards), `stacked-extracts` (no main device, just 4–6 layered extracted UI fragments at varying tilts/depths), `diagram-led` (a clean information diagram or process flow as the hero, no device chrome), `type-led` (massive editorial type as the hero, plus a single small supporting visual), `full-bleed-photo` (one large photographic hero, with a thin device or paper edge fragment overlapping it), `process-strip` (a horizontal multi-step strip showing 3–5 sequential states), `before-after-split` (two contrasting compositions in one frame, divided by a clean line). See `references/page-patterns.md` § Visual Composition Patterns.
- `breathing_region` — where on the canvas the large flat-color HTML overlay region must sit, picked by Agent 1 to vary across the deck. One of: `left` / `right` / `top` / `bottom` / `diagonal-tl` (top-left wedge) / `diagonal-br` (bottom-right wedge) / `center-block` (central rectangle, devices push to edges). Aim for variety across pages — do not put the breathing region on the same side for two consecutive pages.
- `compose_freedom` — `low` (specify every UI element) / `medium` (anchors + permission template) / `high` (only brand identity locked). DEFAULT is `high`.
- `anchors` — array of 1–4 short sentences. These are the ONLY things the image MUST include. Everything else is up to image2.
- `candidate_copy` — text drafts the Page Designer wrote. Some may be baked into the image, some overlaid by HTML. The split is decided AFTER the image is generated, by looking at where the whitespace ended up.
- `must_bake_in_image` — copy fields that MUST appear in the image pixels (e.g. brand wordmark on a phone screen). Page Designer should add the corresponding strings to the image prompt.
- `may_overlay_in_html` — copy fields the Layout Fitter is allowed to slot into discovered whitespace. Anything in this list must NOT be baked into the image.

## Workflow contract

1. **Agent 1 (Project Planner)** writes `deck-plan.json` from the user brief. It produces `deck` + `pages[]` with `intent_one_line` + `page_type` + `page_role_label` populated. It SHOULD leave `anchors`, `candidate_copy`, `device_hint`, `density_hint` empty for Agent 2 to fill (or pre-populate as sketches that Agent 2 may revise).
2. **Agent 2 (Page Designer)** runs once per page. It reads `deck` + the single page entry, drafts `candidate_copy`, picks `device_hint` / `density_hint` / `compose_freedom`, writes `anchors`, computes the `must_bake_in_image` vs `may_overlay_in_html` split, then emits a free-composition image prompt to disk and invokes image2.
3. **`scripts/find_blank_zone.py`** scans the generated image and emits `<page-id>.zones.json` (multiple zones; see schema in that script).
4. **Agent 3 (Layout Fitter)** reads `candidate_copy` + `zones.json` and decides which copy fields go into which zones, with what font sizes / colors / alignment. Default implementation is rule-based (largest zone → title, second-largest → desc, smallest non-touching zones → KPI tiles).
5. **`scripts/build_interactive_page.py --mode multi-zone`** consumes the fitter output and renders HTML overlay.

## Validation

Use `scripts/validate_deck_plan.py deck-plan.json` (TODO) to verify:

- All required `deck` fields present.
- Each page has `id`, `page_type`, `intent_one_line`.
- All `id`s unique and kebab-case.
- `page_type` ∈ allowed enum.
- All `style_direction` palettes use the 6 semantic keys.
- `must_bake_in_image` and `may_overlay_in_html` are disjoint subsets of `candidate_copy` keys.

## Example: minimal 3-page deck plan

```json
{
  "schema_version": "1",
  "deck": {
    "name": "lulu 2026",
    "designer": "WANGZETIAN",
    "tagline": "把日常採買變成一件值得期待的小事",
    "section_label": "UX/UI DESIGN",
    "header_style": "dot-deckname-section",
    "footer_style": "dot-tagline-wordmark",
    "palette": {
      "bg": "#FFF6E1", "ink": "#1A1410",
      "accent_start": "#F5B700", "accent_end": "#E8851A",
      "secondary": "#2B5C40", "muted": "#8B7355"
    },
    "fonts": {
      "cjk_display": "PingFang SC Heavy", "cjk_body": "PingFang SC Regular",
      "en_display": "Cormorant Garamond Italic", "en_body": "Inter"
    },
    "style_direction": "warm-commercial",
    "canvas": { "w": 2048, "h": 1152 }
  },
  "pages": [
    { "id": "cover",            "page_type": "cover",       "page_role_label": "封面",     "intent_one_line": "用一张暖色静物建立 lulu 的语气：日常、新鲜、值得期待。" },
    { "id": "case-01-detail",   "page_type": "case-study",  "page_role_label": "商品详情", "intent_one_line": "把一件商品讲清楚——价格、产地、保鲜信息一次到位。" },
    { "id": "case-02-home",     "page_type": "case-study",  "page_role_label": "首页改版", "intent_one_line": "重新规划 lulu 首页，让用户在 3 秒内看到今天的重点。" }
  ]
}
```
