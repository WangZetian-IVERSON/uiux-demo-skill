# Annotated Callouts — Image-as-Content Render Mode

> The image is not a background. It is **the artifact being analyzed**. Text is not a caption — it's a series of design notes pinned to specific pixels in the image, connected by thin lines.

This mode replaces the "image fills canvas + title floats in breathing zone" pattern with the editorial annotation layout used by Pentagram / IDEO / Frog case studies.

---

## When to use

- **Anatomy pages** — explaining the parts of a single screen / mockup.
- **Process detail pages** — pointing at moments in a flow image.
- **Before/after pages** — annotating which pixels changed and why.
- **Photography / installation pages** — pointing at material decisions in a real photo.

When NOT to use:
- **Cover / manifesto pages** — the image *is* the statement; no notes.
- **Diagram-led pages** — the diagram already labels itself.
- **Pure data/dashboard pages** — those are HTML/SVG, not photos.

---

## Mental model

```
┌────────┬──────────────────────┬────────┐
│ left   │                      │ right  │
│ gutter │   the artifact       │ gutter │
│ (440)  │   (image_w x         │ (440)  │
│        │    image_h)          │        │
│ ┌────┐ │                      │ ┌────┐ │
│ │card│←┄┄┄┄●(anchor)          │ │card│ │
│ └────┘ │                      │ └────┘ │
│        │              ●┄┄┄┄┄→ │ ┌────┐ │
│        │                      │ │card│ │
└────────┴──────────────────────┴────────┘
   stage_w = image_w + 2 * gutter
```

- The image is centered in a wider stage. Default gutter = 440 px each side.
- Each callout has an **anchor point** (a yellow dot pinned to a specific pixel in the image), and a **card** (in one of the two gutters).
- A thin SVG line connects the anchor to the card edge.
- Cards stack vertically on either side. Designer chooses `side` and `card_y` per callout.

This means image_model has **full freedom** to compose the artifact however it wants — there is no "must leave breathing room here" constraint. The annotations live OUTSIDE the image.

---

## Workflow

1. **Write the prompt** so the image has 4-6 visually distinct, identifiable elements (a header strip, a card, a button, a badge, etc.). Don't reserve breathing space — fill the image. Just make sure each element you plan to annotate is recognizable.
2. **Generate the image** via ComfyUI as usual.
3. **Visually inspect** the rendered image and write down `(x, y)` for each anchor (image coords, not stage coords).
4. **Write the annotations.json** (see schema below). Each callout = one design decision, with a `detail` of 80–180 Chinese characters explaining the **reasoning**, not just describing what's there.
5. **Render**: `python scripts\build_interactive_page.py --mode annotated-callouts --image X.png --annotations X.annotations.json --out X-annotated.html`
6. Open the HTML. If a card overlaps another or an anchor is wrong, adjust `card_y`, `side`, or `anchor` — re-render takes <1s.

---

## annotations.json schema

```jsonc
{
  "image_w": 2048,
  "image_h": 1152,
  "deck_palette": {
    "bg": "#FAFAF7", "ink": "#1B1B1B", "muted": "#5A5A5A",
    "accent_start": "#FFE411", "accent_end": "#FFC400"
  },
  "page_num": "03",                        // optional, top-left badge
  "page_title": "圈子首页改版 · 看到熟人 再看动态",   // optional, top center
  "page_subtitle": "Anatomy of a Small-Circle Home", // optional, top right italic
  "footer": "WANGZETIAN · 2026 · ANATOMY", // optional, bottom muted strip

  "gutter": 440,        // default 440, increase if cards need more room
  "card_w": 380,        // card width
  "img_y_offset": 90,   // vertical offset of image from stage top (leaves room for page-head)
  "foot_h": 70,         // height reserved at stage bottom for footer

  "callouts": [
    {
      "anchor": [620, 360],    // (x, y) in IMAGE coords (0..image_w, 0..image_h)
      "side": "right",         // "left" or "right" — which gutter the card sits in
      "card_y": 90,            // top of card in IMAGE coords (0..image_h)
      "num": "01",             // optional, defaults to position number
      "headline": "顶部 · 今天 12 人在",
      "detail": "把在线圈友放在第一屏顶部……"   // 80–180 CJK chars; explain WHY, not WHAT
    }
  ]
}
```

---

## Writing rules for `detail`

This is where the designer's thinking lives. Treat each card as a 1-paragraph design memo.

**MUST:**
- State the **decision** in one clause ("把 X 放在 Y").
- State the **reason** in one clause ("因为 / 是为了 ...").
- State the **tradeoff** acknowledged ("代价 / 取舍 / 放弃 ...").
- 80–180 Chinese characters. Tighter is better.

**MUST NOT:**
- Re-describe the image ("这里有一个按钮"). The viewer already sees that.
- Use vague claims ("更好用 / 更友好 / 提升体验"). Forbidden by `analysis-depth.md`.
- Invent metrics. If a number is hypothesized, mark `[假设：xx，需 A/B 验证]`.

**Good detail:**
> 把在线圈友放在第一屏顶部，而不是侧边或抽屉里。50 人圈子里，「今天有谁来了」比「今天发了什么」更稀缺——头像出现的频率，比内容更新更值得让你打开 App。代价是首屏少塞两条动态，换归属感的可见信号。

**Bad detail:**
> 这里展示了在线用户头像，让用户体验更友好。

---

## Layout rules

- 4 callouts is the sweet spot. 6 is the maximum. More than 6 = the page is too dense; split into two pages.
- Roughly balance left/right. All-on-one-side reads as imbalanced unless the image visually demands it.
- `card_y` values should be at least 240 px apart (card height ≈ 200 px).
- Cards in the left gutter visually pair with anchors on the left half of the image; same for right. Crossing lines are okay if intentional, but more than 2 crossings becomes unreadable.
- The hero image's **left and right edges** are where lines terminate (visually). The yellow anchor dot inside the image is where the eye starts.

---

## Worked example

See [generated-images/jike-circle/case01.annotations.json](../generated-images/jike-circle/case01.annotations.json) and [case01-annotated.html](../generated-images/jike-circle/case01-annotated.html). Same source PNG as the v1 multi-zone version, but with 4 design memos pinned to specific pixels.

---

## Integration with deck-narrative-architecture.md

Each archetype's pattern table can specify `render_mode: "annotated-callouts"` for any anatomy / detail / before-after page. Example for A1 argument-arc, P3:

| page | role | pattern | render_mode |
|---|---|---|---|
| P3 | anatomy | hero-device-orbit | **annotated-callouts** ← image is content, 4 design memos pinned to it |

This decouples **what the page argues** (narrative_role) from **how the image carries content** (render_mode). They compose freely.
