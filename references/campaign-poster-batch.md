# Campaign Poster Batch

## Why This Module Exists

Premium ecommerce / brand UIUX portfolios always include a "campaign visuals" or "operations design" appendix: 5-8 posters arranged as a gallery (双 11, 五一, 99 大促, 夏日上新, 新品发布, etc.). This is one of the few page types where image generation models genuinely shine — and where consistency matters most, because the page IS a comparison grid.

This module gives the skill a single batch action that produces a coherent set of campaign posters for one project, all sharing the same brand world.

## When To Use

Use this module when the deck includes:

- An ecommerce / retail / marketplace project that needs a "campaign visuals" appendix.
- A brand / VI project that needs application examples.
- A content platform / community project that needs a "feature campaign" gallery.
- An operations / growth designer portfolio.

Do NOT use this module:

- For B-side / admin / dashboard projects (campaign posters are off-domain).
- As filler when there is nothing else to show — the posters must serve a real claim about visual range.

## Prerequisites

Before generating, confirm:

1. The project PADB exists (per `visual-consistency.md`).
2. The project type allows campaign posters (consumer-facing).
3. There is a defined poster series concept (e.g. "the 4 seasonal campaigns of 2026" / "5 anchor mid-year promotions" / "3 brand application scenarios"). Without a series concept, the gallery looks random.
4. The image-generation tool can produce 2K+ output with reference-image support (Nano Banana Pro / Gemini 3 Pro Image / GPT-Image / Midjourney). If only a weak tool is available, output a prompt pack and stop.

## Series Concept

Pick ONE of these series structures. Do not mix.

### Structure A — Seasonal Calendar (4-5 posters)
新春 / 五一 / 暑期 / 双 11 / 双 12 — calendar-driven, palette shifts seasonally but keeps the brand frame.

### Structure B — Promotion Tier (5-6 posters)
新品首发 / 限时秒杀 / 满减大促 / 会员专享 / 品牌联名 / 清仓特惠 — promotion-mechanic driven, all in current season.

### Structure C — Channel / Format (4-5 posters)
首页 banner / 详情页头图 / push 推送图 / 短信卡片 / 朋友圈广告 — same campaign across formats, demonstrates adaptive design.

### Structure D — Brand Application (3-5 visuals)
礼盒包装 / 户外大屏 / 落地展架 / 周边周年纪念 — VI application across physical touchpoints.

### Structure E — Concept Series (3 visuals)
For VISUAL_PROPOSAL mode: three concept campaigns illustrating brand voice ("活力", "温度", "信赖" — each a single hero image). Lower output count, higher art direction per piece.

## Series-Level PADB Extension

Beyond the project PADB, define a series-specific block once:

```text
=== POSTER SERIES BLOCK (extends project PADB) ===
series_concept:         (which structure A-E)
series_count:           N
master_palette:         the project PADB primary + 1 series accent that shifts per poster (e.g. seasonal hue)
master_typography:      lock display face for poster Chinese title; lock secondary face for promotion tag
master_format:          poster aspect ratio, e.g. 3:4 portrait, 1:1 square, 9:16 vertical
master_motif:           ONE recurring visual element across all posters (e.g. a glowing arc, a 3D mascot, a packaging silhouette, a gradient ribbon). This is what makes the series read as a series.
hero_object_per_poster: list each poster's distinct hero object (gift box / coupon stack / product trio / mascot pose / etc.)
title_keyword_per_poster: 2-character or 4-character Chinese promotion keyword
promotion_tag_per_poster: e.g. "限时 3 天" / "满 199 减 50" / "首单立减"
forbidden:              real brand logos, real celebrity faces, real currency symbols other than ¥, watermarks
=== END ===
```

The `master_motif` line is the single most important field — it is the visual thread that turns 5 separate images into a series.

## Generation Order

**Showcase / batch split (mandatory).** When the deck follows the showcase-first workflow, only generate poster #1 (the master) during the showcase step. Get user approval on the master + master_motif + palette accent rule. Only then batch-generate posters #2-N. Do NOT produce the full series before showcase confirmation.

Generate in this order. Each step uses the previous output as reference.

```text
1. [SHOWCASE STEP] Generate poster #1 (the strongest seasonal / hero) — 4 candidates, pick 1. STOP. Confirm with user.
2. [BATCH STEP] Use poster #1 as reference image for poster #2. Adjust seasonal hue + hero object per the series block. 2 candidates, pick 1.
3. Continue 2 candidates per remaining poster, always passing the prior selected poster as reference, with explicit instructions to keep master_motif + master_typography + master_format identical and only vary palette accent + hero object + title keyword.
4. Run the 5-axis QA from visual-consistency.md across the full series in a contact sheet.
5. If any poster drifts >1 axis, regenerate that poster with stronger reference instructions.
```

## Prompt Template (per poster)

```text
[paste project PADB]
[paste poster series block]

--- POSTER N OF N ---
poster_role:            seasonal | promotion-tier | channel | brand-application | concept
hero_object:            [from series block]
title_keyword:          [from series block]
promotion_tag:          [from series block]
palette_shift:          this poster shifts the series accent toward [warm gold / cool blue / fresh green / festive red] while keeping master_palette base
composition:            
  - hero object occupies 55-65% of the poster, anchored at center or 2/3 vertical line
  - title safe zone: top 25% reserved for HTML title overlay (do NOT render the Chinese title in the image — it goes on top in HTML/PPT)
  - master_motif appears in the same screen quadrant as poster #1
  - small promotion tag area in the bottom-right corner (will also be overlaid in HTML)
material:               from project PADB (do not introduce new materials)
lighting:               from project PADB
camera:                 product photography, 50-85mm equivalent, slight 3/4 angle
quality_bar:            premium ecommerce campaign, magazine-cover composition, generous breathing room
negative:               no fake brand logos, no readable Chinese text inside the image, no random celebrity faces, no AI sparkles, no purple gradient bg, no watermark, no stock-poster cliche
```

## Title Layer Discipline

Render the Chinese promotion title in HTML/PPT on top of the image, NOT inside the image. Reasons:

- Image models still mis-render Chinese display type at small sizes.
- Editable titles let the deck adapt to different campaigns later.
- Layered titles let you keep the master_typography lock across all posters.

Layout convention:

```text
Title block (HTML overlay):
  Position: top-left of the poster, 8% margin
  Display face: master_typography
  Title size: 56-72px
  Title content: 4-character Chinese promotion keyword (e.g. "夏日狂欢" / "好物上新")
  Subtitle: 16-20px Latin or smaller Chinese (e.g. "SUMMER SALE 2026" / "限时 7 天")
  Promotion tag: bottom-right corner, 14-18px in master_typography secondary face, on a small accent-colored chip
```

## Gallery Page Composition

Once posters are generated, compose the gallery page:

### Layout — 5 posters
```text
Hero poster (left, 1.5x scale) + 4 supporting posters in a 2x2 grid on the right.
```

### Layout — 6 posters
```text
3 across x 2 down, all equal scale, with 24-32px gutters.
```

### Layout — 4 posters
```text
2 hero + 2 secondary (one row big, one row small), or 4 portrait posters in a single row with parallax depth.
```

### Required overlays on the gallery page:

- A short claim above the gallery: "campaign visual system for [project name]", year, channels covered.
- Per-poster caption strip: campaign name + month + channel.
- One callout describing the system rule (e.g. "every poster reuses the master arc motif and shifts seasonally on accent only").

## QA Gates Specific To Posters

Reject the series and regenerate when:

- Two posters look like they came from different brands.
- The master_motif is missing or transformed in any poster.
- The title safe zone is filled by image content (image text/logo intrudes where the HTML title sits).
- A poster has unreadable AI text or a fake real-world brand logo.
- The series feels like 5 standalone images instead of one coherent campaign system.
- Aspect ratios are inconsistent (mixing 3:4 with 1:1 unless Structure C / channel format demands it).

## Density And Rhythm In The Deck

Place the campaign poster gallery in the back third of the deck, after the case-study core (problem → analysis → strategy → UI proof). It serves as "visual range proof", not as the main case argument. One gallery page per major project at most. If multiple projects need posters, group them in a single "Other Visual Work" appendix with one row per project.

## What NOT To Do

- Do not generate posters for a B-side or industrial project to "fill the deck". They will read as off-topic.
- Do not let the image model render the Chinese promotion title — overlay in HTML.
- Do not invent a real brand or use a real celebrity / IP / mascot.
- Do not produce 10+ posters. 4-6 is the sweet spot. More dilutes the series.
- Do not break the master_motif rule "just for one poster". The motif is the series.
