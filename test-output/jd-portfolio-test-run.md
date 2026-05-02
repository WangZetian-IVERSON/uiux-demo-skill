# Test Run · 京东电商运营设计师作品集

> Smoke-test of the uiux-portfolio-deck skill on topic "投京东 · 电商运营设计师作品集"
> Mode: VISUAL_PROPOSAL · Capability: PROMPT_PACK_ONLY
> Date: 2026-04

---

## DECK META-PADB (deck-level grammar)

```text
deck_typography:
  display_zh:   思源黑体 Heavy
  display_en:   Migra Italic (cover only) / Geist Mono Bold (section, callout)
  body_zh:      HarmonyOS Sans SC Regular
  body_en:      Inter Regular (subtitle only)
  mono:         JetBrains Mono (data, code label)
canvas:         1920 × 1080 px, 16:9
background_system: deep charcoal #0d0d10 base, with warm-amber atmospheric haze on covers; paper #f5f1ea on lightswitch pages (component / system / data)
accent_colors:
  primary:      #ff6a00 (warm 京东-adjacent orange, but not the exact JD red — honest distance)
  secondary:    #ffb454 (soft amber)
  cool_balance: #1f3a55 (deep navy for B-side / data pages only)
  neutral:      #f5f1ea / #1a1a1f / #6b6b73
grid:           12-column, 96px gutter, 64px outer margin
screenshot_treatment: floating in 3/4 perspective with soft contact shadow, never pasted flat
generated_asset_style: cinematic product photography 50mm, deep DoF, single key light upper-left, warm rim
data_card_treatment: matte white card on charcoal, 16px radius, 0 shadow, 1px hairline border
section_divider_style: full-bleed black with one giant Chinese number 01 / 02 / 03 in display face
footer_metadata: top-right shows section number + page counter, bottom-left shows designer name + year
bilingual_strategy: 中文 leads, 英文 ≤ 4 词作 atmospheric subtitle
concept_badge: VISUAL_PROPOSAL mode → every non-real UI page carries [概念 / Concept] in top-right corner, 12px, primary accent on 1px outlined chip
```

---

## PROJECT-LEVEL PADBs

The deck has 3 case study projects (inferred from a 电商运营设计师 portfolio shape) + 1 visual range appendix.

### PADB-1 · M-Mall (麦集) · 综合电商 App 改版

```text
project_slug:     mmall-2026
project_type:     综合电商 App, C-side, iOS-first
mode:             VISUAL_PROPOSAL
style_anchor:     Warm commercial confidence — soft amber light, glossy product still-life, charcoal stage with one ember accent.
palette:
  base:           #0d0d10
  surface:        #1a1a1f
  primary_accent: #ff6a00
  secondary_accent: #ffb454
  text_on_dark:   #f5f1ea
  warm_spark:     #ffd9a8 (rim light only)
  forbidden_colors: 京东红 #e1251b (太近真实品牌, 故意避开), purple gradient, neon pink
material_vocabulary: glossy product packaging + matte charcoal pedestal + soft fabric backdrop + frosted glass coupon card + brushed brass detail
lighting_setup:   key 45° upper-left, 3200K warm tungsten, soft fill 5000K, hard rim from upper-right, contact shadow at 25°
camera:           50mm equivalent, f/2.0, slight low-angle 3/4 view at 15°
environment:      deep charcoal floor with soft amber haze, faint perspective grid in 4% opacity
props_vocabulary: shopping bag in kraft + linen, gift box with brass clasp, coupon card in frosted glass, price tag in matte ceramic, fabric drape, single ember spark, iPhone 15 Pro titanium, MacBook Pro 16 matte
type_in_image:    NONE (all titles overlaid in HTML)
forbidden_props:  smart power dashboard, hotel buildings, sleep moons, cute mascots, emoji, AI sparkles, purple blobs, fake JD logo
device_frames:    iPhone 15 Pro titanium black for all phone shots; MacBook Pro 16 matte aluminum for all desktop shots
render_reference: Octane + Redshift, premium ecommerce product photography (think Apple x MUJI x 一条)
aspect_ratios:    16:9 at 2048×1152 for deck pages; 1:1 at 1536×1536 for isolated 3D props; 3:4 for poster series
```

### PADB-2 · Hometaste (家味) · 生鲜社区团购小程序

```text
project_slug:     hometaste-2026
project_type:     生鲜社区团购, mini-program, C-side + B-side (团长后台)
mode:             VISUAL_PROPOSAL
style_anchor:     Fresh-market warmth — terracotta + sage, natural wood pedestal, morning sunlight.
palette:
  base:           #f5f1ea (paper)
  surface:        #ffffff
  primary_accent: #c14b2a (terracotta)
  secondary_accent: #6b8e5a (sage)
  text_on_light:  #2a2018
  warm_spark:     #f4c97f (sun gold)
  forbidden_colors: 京东红, 拼多多红, neon, purple
material_vocabulary: natural oak pedestal + woven basket + linen cloth + fresh produce + ceramic bowl + handwritten paper tag
lighting_setup:   key from upper-left, 5600K morning daylight, soft fill, organic dappled shadow
camera:           50mm, f/2.8, eye-level slight tilt
environment:      paper-textured backdrop with soft natural shadow, subtle vignette
props_vocabulary: oak crate, linen tote, vegetable bunch, ceramic bowl, brown paper bag, handwritten price tag, iPhone 15 Pro silver, MacBook Air 13 silver (lighter device for lighter palette)
type_in_image:    NONE
forbidden_props:  charcoal/dark-tech props, gloss product photography, cool blue, cute character mascots
device_frames:    iPhone 15 Pro silver, MacBook Air 13 silver
render_reference: editorial food + lifestyle photography, soft documentary
aspect_ratios:    16:9 at 2048×1152 for deck pages; 1:1 at 1536×1536 for isolated 3D props
```

### PADB-3 · ToolStudio (匠工) · B-side 工单 SaaS 数据后台

```text
project_slug:     toolstudio-2026
project_type:     B-side SaaS, 工单/订单管理后台, web admin
mode:             VISUAL_PROPOSAL
style_anchor:     Operational command-center — deep navy, electric cobalt, frosted glass panels, single ember alert.
palette:
  base:           #050a12
  surface:        #0c1622
  primary_accent: #34d6ff (electric cyan)
  secondary_accent: #2563eb (cobalt)
  text_on_dark:   #f6fbff
  warm_spark:     #ffb454 (alert / spark)
  forbidden_colors: warm orange (would conflict with PADB-1), purple, pink
material_vocabulary: frosted glass panel + brushed dark metal + matte concrete + anti-reflective screen glass
lighting_setup:   key 45° upper-left, 5600K cool, soft fill, hard cyan rim
camera:           50mm, f/2.0, slight low-angle for hero, eye-level for product
environment:      deep navy spatial environment with perspective hex grid floor, faint volumetric haze
props_vocabulary: glass dashboard panel, floating chart cards, holographic map texture, dark metal pedestal, single ember spark, MacBook Pro 16 matte black
type_in_image:    NONE (dashboard surface itself = HTML+SVG, this PADB only governs covers/scenes/3D props around it)
forbidden_props:  warm shopping props from PADB-1, food/produce props from PADB-2, mascots, emoji
device_frames:    MacBook Pro 16 matte black (this project is desktop B-side only, no phone)
render_reference: cinematic command-center product photography
aspect_ratios:    16:9 at 2048×1152
```

---

## STEP 6 · ASSET ROUTING (per page)

22-page deck (typical 京东投递版 长度).

| # | Page Role | Routing | Why |
|---|---|---|---|
| 01 | Cover | IMAGE_MODEL (PADB-1 cover hero) | 暖光商品堆叠 + 大标题 |
| 02 | Profile / 自我定位 | HTML only (text + 一张 PADB-1 衍生小图) | 文字主导 |
| 03 | Contents / 项目地图 | HTML only | 三项目卡片 |
| 04 | 项目 1 Section Cover · M-Mall | IMAGE_MODEL (PADB-1 section) | reset attention |
| 05 | M-Mall · Background | IMAGE_MODEL hero + HTML callout | 商品场景 |
| 06 | M-Mall · Problem Diagnosis | HTML only (analysis-depth template) | 5 个具体问题卡片 |
| 07 | M-Mall · 竞品分析 | HTML only (analysis-depth 矩阵) | 4 竞品 × 5 维度 |
| 08 | M-Mall · Design Strategy | HTML only (3 principle cards) | 文字 + 小图标 |
| 09 | M-Mall · 信息架构 / Flow | HTML SVG flow diagram | 流程结构 |
| 10 | M-Mall · 核心界面 | IMAGE_MODEL concept-screen × 3 (in iPhone frame) | **这页最关键的视觉证明** |
| 11 | M-Mall · 交互细节 | HTML composite (concept-screen crops + callouts) | 细节注释 |
| 12 | M-Mall · 复盘 | HTML only (3 列：shipped / improved / remains) | analysis-depth outcome |
| 13 | 项目 2 Section Cover · Hometaste | IMAGE_MODEL (PADB-2 section) | 切换暖纸调性 |
| 14 | Hometaste · Background + 用户场景 | IMAGE_MODEL hero (生鲜场景) | scene |
| 15 | Hometaste · 团长 vs 用户双角色分析 | HTML two-column (analysis-depth persona) | 角色对照 |
| 16 | Hometaste · 核心界面（用户端 + 团长端） | IMAGE_MODEL concept-screen × 4 | 双端 UI |
| 17 | Hometaste · 数据看板 (团长端) | **HTML_DASHBOARD** (dashboard-rendering Pattern A 简化版) | 数字, 不能让图像模型画 |
| 18 | 项目 3 Section Cover · ToolStudio | IMAGE_MODEL (PADB-3 section) | 切换深蓝 |
| 19 | ToolStudio · 主控台 | **HTML_DASHBOARD** (Pattern A · 完整 hero dashboard) | 核心证据 |
| 20 | ToolStudio · 工单详情 + 组件库 | **HTML_DASHBOARD** (Pattern E + Pattern D) | 多 pane + 组件墙 |
| 21 | 视觉作品 Appendix · 海报系列 | **POSTER_BATCH** (PADB-1 系列, master_motif = 暖光弧线) | 5 张 campaign poster |
| 22 | Thanks / Contact | HTML only | 收尾 |

**Lane 分布**：IMAGE_MODEL 7 页 / HTML_DASHBOARD 4 页 / POSTER_BATCH 1 页 / HTML-only 10 页 = 22 页。

---

## STEP 7 · SHOWCASE FIRST

Showcase 对（生成顺序）：

```text
1. Page 01 Cover (4 candidates) — PADB-1 验证暖光商业调
2. Page 19 ToolStudio 主控台 (HTML+SVG render) — 验证 dashboard-rendering 落地
3. Page 21 海报 Master #1 (4 candidates, then 仅生成 #1) — 验证海报系列起点
```

3 张 showcase 涵盖三种产线（IMAGE_MODEL / HTML_DASHBOARD / POSTER_BATCH），任何一种翻车都早暴露。

---

## STEP 7 · IMAGE PROMPT PACK (showcase candidates)

> 推荐外部跑 **Nano Banana Pro** 或 **Gemini 3 Pro Image**（中文 / 参考图链路最稳）。
> 每个 prompt 已经把整个 PADB 拼在前面，**直接复制粘贴即可，不要手动改**。

### PROMPT-01 · Page 01 Cover (PADB-1 · M-Mall) · 4 candidates

```text
=== PROJECT ART DIRECTION BLOCK ===
project: mmall-2026 (warm commercial portfolio cover)
style: Cinematic warm-commercial product photography. Soft amber tungsten key light upper-left at 45°,
       cool 5000K fill, hard rim from upper-right. Charcoal stage #0d0d10 with subtle amber atmospheric haze.
       Faint perspective grid floor at 4% opacity. Octane + Redshift render quality.
materials only from this list: glossy product packaging in kraft + linen, matte charcoal pedestal,
       soft fabric backdrop, frosted glass coupon card, brushed brass detail, ceramic price tag.
camera: 50mm equivalent, f/2.0, slight low-angle 3/4 view at 15° elevation.
palette HEX: base #0d0d10, surface #1a1a1f, primary accent #ff6a00, secondary #ffb454, rim #ffd9a8.
type_in_image: NONE.
forbidden: 京东红 #e1251b, JD logo, real brand logos, purple gradient, neon pink, cute mascot, emoji,
           AI sparkles, watermark, garbled Chinese text, smart power dashboard, hotel buildings.
=== END PADB ===

--- PAGE-SPECIFIC ---
page_role:    deck cover
aspect:       16:9, 2048×1152
composition:  hero stack of 3-4 commercial objects on a charcoal pedestal, occupying right 55% of frame.
              Left 40% reserved as negative space for HTML title overlay (do NOT render any text).
              Pedestal sits at lower-third line. Upper third has soft amber haze.
subject:      stacked composition — kraft shopping bag (medium), gift box with brass clasp (small, on top),
              frosted-glass coupon card floating at 30° angle (small accent), single ember spark (tiny accent).
              Brushed brass detail on the gift box catches the rim light.
mood:         premium ecommerce confidence, magazine-cover restraint, breathing room.
quality_bar:  Apple x MUJI x 一条 product photography. Magazine cover.
negative:     no text rendered in image, no logos, no JD red, no purple, no AI gradient blobs,
              no busy background, no shopping cart icon, no people.
generate:     4 candidates, square ratio test then upscale to 2048×1152.
```

### PROMPT-02 · Page 04 Section Cover (PADB-1 · M-Mall · 项目封面)

```text
[same PADB as PROMPT-01, paste in full]

--- PAGE-SPECIFIC ---
page_role:    project section cover (resets attention before case study #1)
aspect:       16:9, 2048×1152
composition:  full-bleed scene, single hero phone (iPhone 15 Pro titanium black) standing vertical
              on charcoal pedestal, slight 3/4 angle, occupying CENTER 30% of frame.
              Surrounding props: kraft shopping bag (left, larger, blurred slight foreground bokeh),
              floating coupon card (upper-right, behind phone, slightly out of focus).
              Phone screen is BLANK / off (will be composited with concept screen later in HTML).
              Generous negative space for HTML overlay of "01 · M-Mall" giant section number.
subject:      iPhone 15 Pro titanium with screen OFF, on charcoal pedestal.
mood:         hero introduction, slower pacing than cover.
generate:     2 candidates.
negative:     no UI on phone screen (screen must be black/off), no text, no logos.
```

### PROMPT-03 · Page 10 M-Mall 核心界面 (concept screens × 3 in phone)

```text
[same PADB as PROMPT-01]

--- PAGE-SPECIFIC ---
page_role:    concept UI mockup screens (will be composited into 3 iPhone frames on the deck page)
aspect:       9:19.5, 1170×2532 (iPhone 15 Pro screen native)
composition:  produce ONE iOS app screen per generation. Generate 3 screens total:
  screen A — homepage feed: top hero banner (warm-amber product hero, NO real brand),
              category grid 4×2 with simple line icons (line, NOT emoji),
              two product cards in a row showing kraft-styled product imagery, price in primary accent.
  screen B — product detail: large product image top, sticky "加入购物车" button in primary accent #ff6a00,
              spec list, recommended bundle in soft amber tint card.
  screen C — checkout: order summary with frosted glass coupon card, payment method list,
              prominent CTA button.
typography_in_screen: 思源黑体 for Chinese, all sample copy in Chinese only,
              prices in CNY ¥ symbol, NO real brand names, use placeholder product names like
              "羊毛针织开衫 · 米杏色 / 手冲咖啡 250g / 香薰蜡烛 · 无花果".
ui_style:     iOS 17 native, generous whitespace, primary accent reserved for one CTA per screen,
              cards with 16px radius, hairline 1px dividers, NO glassmorphism stacking,
              status bar at top (carrier · 9:41 · 100%).
mood:         premium-but-warm ecommerce app, like a curated lifestyle store.
generate:     3 separate generations, ONE per screen. Use screen A as reference image for B and C
              to lock typography + color + spacing.
negative:     no fake JD logo, no real brand logo, no garbled Chinese, no cartoon mascot,
              no fake user-avatar photos, no sparkles, no purple, no neon.
```

### PROMPT-04 · Page 21 Poster Master (PADB-1 · 海报系列 #1 — 夏日上新)

```text
[same PADB as PROMPT-01]

--- POSTER SERIES BLOCK ---
series_concept:    Structure A — seasonal calendar (4 posters: 春上新 / 夏日 / 秋礼 / 双11)
series_count:      4 (this prompt = master poster #1, 夏日上新)
master_motif:      a glowing warm-amber arc sweeping from upper-right to lower-left across the composition.
                   This arc MUST appear in identical position and curvature in all 4 posters.
master_format:     3:4 portrait, 1536×2048
master_typography: HTML overlay only (do NOT render Chinese in image)

--- PAGE-SPECIFIC ---
page_role:        master poster (will be reference for posters #2-4 batch generation in next round)
hero_object:      a single linen tote bag, half-open, with one fresh sea-salt soda can and one folded
                  cotton t-shirt visible inside. Tote sits on charcoal pedestal, bathed in summer
                  amber-gold light, with the master_motif glowing arc behind it.
composition:      hero object centered, 60% of frame height. Top 25% of canvas left empty for HTML
                  title overlay ("夏日狂欢" 4-character title will go here, do NOT render in image).
                  Bottom-right 15% area also reserved for HTML promotion tag overlay.
                  Master_motif arc passes behind the hero object at 30° angle.
mood:             clean summer commercial, premium but accessible, magazine-cover.
generate:         4 candidates.
negative:         no text in image, no logos, no people, no fake brand, no JD red, no neon,
                  no purple blob, no busy decoration in title safe zone, no watermark.
```

---

## STEP 7 · HTML SHOWCASE: Page 19 ToolStudio Main Console

> Per dashboard-rendering.md Pattern A. Image-model NEVER renders dashboard surface.
> Below is a self-contained HTML+SVG render. Drop into the deck stage at slide 19.

(See `test-output/page-19-toolstudio-dashboard.html` — created next.)

---

## STEP 8 · CONFIRM CHECKPOINT

After running PROMPT-01..04 externally + viewing the dashboard render:

- 5-axis QA on PROMPT-01..03 outputs (palette / lighting / material / camera / props).
- PROMPT-04 master poster confirmed before batching #2-4.
- Dashboard render confirmed for chart-style lock.

If confirmed → proceed to STEP 9 batch.

---

## STEP 9 · EXPAND (queued, not produced in showcase round)

After confirmation, batch:

- 4 more IMAGE_MODEL prompts (PADB-2 cover, scene, concept screens; PADB-3 section + scene).
- 3 more POSTER prompts (#2-4, each using #1 as reference).
- 3 more HTML dashboards (Hometaste 团长后台 mini, ToolStudio 工单详情多窗格, ToolStudio 组件库).
- 10 HTML-only analysis pages applying analysis-depth.md templates (problem / 竞品 / strategy / IA / outcome / persona / etc).

---

## STEP 10 · FINAL QA gates (applied at delivery, not now)

- 5-axis visual consistency QA across all generated images per project.
- analysis-depth.md self-check on every analysis page.
- `[概念 / Concept]` badge present on pages 05, 10, 11, 14, 16, 17, 19, 20, 21.
- No JD logo / 京东红 anywhere.
- No HTML-rendered fake UI saved as PNG.
- Numbers in dashboards labelled as designed sample data, not claimed business outcomes.

---

## Honesty notes (would appear at the end of the deck)

```text
本作品集所有案例项目（M-Mall / Hometaste / ToolStudio）均为虚构概念项目，
非任何真实公司或产品。界面截图为图像模型生成的设计提案概念图，仪表盘为
HTML 渲染的设计稿（含设计师选定的示例数据）。任何"指标"为预估值或示例值，
非实测业务结果。
```
