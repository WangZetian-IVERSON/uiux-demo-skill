# Worked Example — fit-checkin Hero Page (light cream + M3 layout)

End-to-end record of producing a single overlay page that **passed the closed
loop on iteration 1 with score 9**. Use as a template when starting a new page.
Companion to `references/overlay-layout-spec.md` and
`references/closed-loop-overlay-qa.md`.

Final artifacts live in [generated-images/fit-checkin/](../generated-images/fit-checkin/).

---

## 1. The brief (one sentence)

> 「日课」健身打卡 App 的「今日训练」页 hero — 强调「完成 3/5 项就够」的克制立场，浅色奶油底，M3 (主屏 + 局部放大卡) 构图。

That's the only input. Everything below is derived.

## 2. Style choices (per `references/image-prompt-style-uiux.md`)

| Slot | Choice | Why |
|---|---|---|
| 意图标签 | 排版干净，留白充足 | hero 页只一个主体 |
| Prompt 模板 | M3 主屏+局部放大 | 强调一个完成态微动效 |
| BG 基调 | 暖米 `#F2EDE0` | "工具/内容浅色" 类目 |
| 主强调色 | 深绿 `#2EA36B → #1F8755` | 健身=完成=绿，避免和"打卡"产品常见的橙混淆 |
| Secondary | 橙 `#E07A2D` | 保留给火焰徽章一个用途 |

Conscious anti-default: 上一次案例 (`jike-circle/anatomy-v3`) 用的是深紫梅+黄渐变，这次故意全反——浅色 BG + 深绿渐变 + 深墨 ink，验证 schema 不偏向某个色域。

## 3. The image prompt (saved at [prompt.txt](../generated-images/fit-checkin/prompt.txt))

```
排版干净，留白充足。一台 iPhone 居中展示「日课」健身打卡 App 的「今日训练」页面 UI：
顶部一个大圆环显示「今日完成 3/5 项」，下方一列卡片是今天的训练任务（深蹲 4×12 已打勾，
俯卧撑 3×15 已打勾，平板支撑 60s 已打勾，硬拉 4×8 未完成，跳绳 5min 未完成），
右上角小图标是「连续打卡 28 天」的火焰徽章。旁边浮起 1 张玻璃质感的小卡片，是某项训练的
局部放大：一个完成态打勾的微动效特写。背景纯色 #F2EDE0。背景不要任何标题文字，
不要项目名，不要 logo。16:9。
```

5-句结构对应：

1. 意图标签
2. 设备 + 项目 + 屏内必读 UI（5 项训练 + 圆环 + 火焰徽章）
3. 浮起元素（玻璃放大卡）
4. BG hex
5. 禁止背景文字 + 比例

字数 110 中文字 — 在 40-80 推荐区间偏长但仍可接受，因为屏内 UI 元素较多需要枚举。

## 4. Generate the image (ComfyUI + gpt-image-2)

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:COMFY_API_KEY = "<key>"
python scripts/image_client.py generate `
  --backend comfyui `
  --comfyui-url http://127.0.0.1:8000 `
  --model gpt-image-2 `
  --size 2048x1152 `
  --prompt-file generated-images/fit-checkin/prompt.txt `
  --out generated-images/fit-checkin/hero.png `
  --comfyui-timeout 240
```

成本：约 9 ComfyUI credits，~80 秒。一次成功，无重抽。

## 5. Hand-write the layout (skip zones.json)

For a single hero page we don't bother with `find_blank_zone.py` + `layout_fitter.py`.
We hand-write 6 overlays directly. See [hero.layout.json](../generated-images/fit-checkin/hero.layout.json) full file.

Decisions made manually:

| Overlay | Position | Why |
|---|---|---|
| `section_label` | x=90 y=170 w=580 h=50 | top-left, above the title block, leaves header safe-zone clear |
| `title-block` (3 fields) | x=90 y=240 w=580 h=280 | Title 1 = ink black, Title 2 = green gradient — split into two fields so colors differ |
| `desc-block` (desc) | x=90 y=560 w=580 h=260 | Aligned to title block left edge |
| `desc-block` (role chip) | x=90 y=1010 w=580 h=50 | Footer safe — y+h=1060 < 1152*0.95=1094 |
| `desc-block` (anno top) | x=1340 y=360 w=480 h=80 | Right side, points at the glass card area |
| `desc-block` (anno bottom) | x=1340 y=880 w=480 h=80 | Right side, points at the bottom of the phone |

Palette in layout.json mirrors the BG hex used in the prompt (#F2EDE0). When
they drift, the closed-loop QA will mark text as low-contrast.

## 6. Run the closed loop

```powershell
$env:PYTHONIOENCODING = "utf-8"
$env:POCKGO_KEY = "<key>"
$env:OVERLAY_QA_MODEL = "claude-sonnet-4.5"
python scripts/build_with_qa.py `
  --image    generated-images/fit-checkin/hero.png `
  --layout   generated-images/fit-checkin/hero.layout.json `
  --html     generated-images/fit-checkin/hero.html `
  --rendered generated-images/fit-checkin/hero-rendered.png `
  --intent   "Case 02 日课 fitness check-in: left-column typography, centered iPhone, right glass card + 2 annotations" `
  --title    "fit-checkin" `
  --max-iters 3
```

## 7. The QA verdict

```
========= iter 1 =========
OK multi-zone -> hero.html  overlays=6
OK shot -> hero-rendered.png
--- QA iter 1 · score=9 pass=True retake_image=False ---
summary: 布局清晰，UI-文案对应准确，仅动效描述和文本截断为小瑕疵
  [1] MINOR · intent-match @ overlay[4] right glass card annotation
      what: 描述提到「绿色光点扩散」微动效，但静态截图无法验证动效存在
      fix : 改为「完成态的绿色打勾图标」等可验证的静态描述
  [2] MINOR · readability @ overlay[2] desc-block line break
      what: 描述文本在「3/5」后被截断，末尾缺少完整句子
      fix : 补全文本或调整 size 高度至完整显示所有内容

PASSED at iter 1
```

`pass=True` + 0 blocker + 0 major → ship it.

The 2 minors are real but **acceptable**:
- M1 ("describing motion in static screenshot") is a wording sharpening
  opportunity, not a defect. We could rewrite "绿色光点扩散一次即收" → "完成态的
  绿色打勾图标"; both convey the same design intent.
- M2 (text truncation) is a false positive — the QA model misread the line
  wrap. The actual rendered text is complete. This is a known limitation:
  when desc copy contains digits like "3/5" mid-sentence, vision models
  sometimes interpret the line break as a truncation.

## 8. What this validated about the SKILL

- ✅ NEVER 17 (closed loop is mandatory) holds for light-palette pages, not just dark
- ✅ `claude-sonnet-4.5` keeps high precision on tool-app screenshots
- ✅ M3 layout (main shot + glass callout) renders correctly without zones.json
- ✅ Two-color split title (`#1B1B1B` ink + `gradient(#2EA36B,#1F8755)` accent) survives the build's gradient text trick
- ✅ Right-aligned annotations at `align: right` with `x = 1340, w = 480` land naturally to the right of the device

## 9. Reuse instructions

To start a new page from this template:

1. Copy [hero.layout.json](../generated-images/fit-checkin/hero.layout.json) to your `<deck>/<page>.layout.json`
2. Replace `image`, `page_id`, `deck_palette` (especially `bg` to match new prompt)
3. Replace each field's `text`
4. Adjust overlay `x/y/w/h` if your image's mockup is in a different position
5. Run `build_with_qa.py` exactly as in section 6

The schema details that govern step 3-4 live in
[overlay-layout-spec.md](overlay-layout-spec.md).

## 10. Counter-example record — when this doesn't work

If the brief asks for **multiple devices** (M4 device array, M5 process strip),
hand-writing 6+ precise rectangles becomes brittle. Switch to the full
zones-based pipeline:

1. `find_blank_zone.py --multi --ocr` → zones.json
2. `layout_fitter.py --deck-plan ... --page-id ... --zones ...` → layout.json
3. Then `build_with_qa.py` as usual

For single-device hero pages like this one, hand-written layout is faster and
the closed loop catches mistakes anyway.
