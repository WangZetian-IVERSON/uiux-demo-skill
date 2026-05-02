# Deck Defaults

One place that locks the boring-but-critical defaults so the agent doesn't re-decide them per project. Override only with a stated reason.

## Canvas

| Output | Canvas | Aspect | Notes |
|---|---|---|---|
| HTML deck (default) | 1920 × 1080 px | 16:9 | Use `vendor/huashu-design/assets/deck_stage.js` for the stage. |
| HTML deck portrait | 1080 × 1920 px | 9:16 | Only when the user explicitly asks for vertical / mobile-first review. |
| PPTX export | 1920 × 1080 px | 16:9 | Use `vendor/huashu-design/scripts/export_deck_pptx.mjs` or `html2pptx.js`. |
| Static PDF | 1920 × 1080 px → PDF | 16:9 | Use `export_deck_pdf.mjs` / `export_deck_stage_pdf.mjs`. |

Body copy minimum size:
- 1920 px canvas: body ≥ 18px, callout ≥ 14px, micro-label ≥ 12px.
- 1280 px canvas: body ≥ 14px, callout ≥ 12px, micro-label ≥ 11px.
- Inside HTML dashboards: KPI big number 32-48px, KPI unit 14px, status pill text 12-13px (NOT 11px — gets unreadable when projected).

## Typography

Pick one row per project and lock in the deck meta-PADB. Defaults below.

| Role | Chinese default | Latin default | Backup |
|---|---|---|---|
| Display (cover, section cover, hero title) | 思源黑体 Heavy / Source Han Sans Heavy | Migra / Geist Mono Bold | OPPOSans Heavy / 阿里巴巴普惠体 Heavy |
| Subtitle | 思源黑体 Medium | Geist Mono Medium | HarmonyOS Sans Medium |
| Body | HarmonyOS Sans SC Regular | Inter Regular (body only, NEVER as display) | PingFang SC |
| Mono / data | JetBrains Mono | JetBrains Mono | Geist Mono |

Project may override Display face for brand reasons. Body face is rarely overridden.

## Bilingual Strategy

Default: bilingual titles where the Chinese leads and the English is a short atmospheric subtitle. Examples:

```text
设计提案
VISUAL DIRECTION PROPOSAL · 2026

问题诊断
PROBLEM SPACE · 5 frictions

最终界面
THE PRODUCT · core flow
```

Rules:
- Chinese is the primary load-bearing copy. English is mood, not translation.
- English must be ≤ 4 words OR a single tagline ≤ 8 words.
- Body copy is Chinese only by default. Bilingual body is allowed only when the deck targets a bilingual audience (state this once in the deck meta).
- Never machine-translate Chinese to English; if you can't write a tight English line, drop it.

## Output Format Decision

| User signal | Default output |
|---|---|
| "做一份作品集 / 投递版 / 评审版" | HTML deck (vendor/huashu-design stage) + PPTX export |
| "面试要带 PDF / 邮件附件" | HTML deck + PDF export |
| "storyboard / 大纲 / 先看结构" | Markdown storyboard, no HTML/PPT yet |
| "改一改 / 拔高 / 评审现有作品集" | CRITIQUE mode, page-by-page review, no new HTML |
| "这是图片素材, 帮我组成一页" | Single HTML page (not full deck) |

If unclear: ask one question — "要 HTML 在线翻页 / PPTX 投递 / PDF 邮件，三选一？" — then proceed.

## generated-images/ Naming Convention

All generated images go into `generated-images/{project_slug}/` with the naming:

```text
{project_slug}/{seq:02d}_{page_role}_{variant}.png
```

Where:
- `seq` is generation order across the whole project, zero-padded.
- `page_role` is one of: `cover` / `section` / `prop3d` / `scene` / `concept-screen` / `dashboard-bg` / `poster` / `hero`.
- `variant` is short tag like `v1` / `final` / `master` / `s2-summer`.

Examples:
```text
fin-saas-2026/01_cover_v1.png
fin-saas-2026/01_cover_final.png
fin-saas-2026/02_section_strategy.png
fin-saas-2026/03_prop3d_glass-panel.png
fin-saas-2026/04_concept-screen_dashboard.png
jd-mall/05_poster_master.png
jd-mall/06_poster_s2-summer.png
```

This makes the project's PADB + reference-image chain reusable across runs and prevents the folder from collapsing into a flat ungroupable pile.

The PADB itself is saved at `generated-images/{project_slug}/PADB.md` so any later run can pick it up.

## Don't Re-Decide These

When this skill is invoked, the agent should NOT ask the user about: canvas size, body font size, output format defaults, file naming, bilingual default, where to put generated images. Pick from this file silently and proceed. Only ask if the user signals a non-default need.
