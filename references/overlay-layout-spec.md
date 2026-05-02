# Overlay Layout Spec — `<page>.layout.json`

The single source of truth for the **layout JSON** consumed by
`scripts/build_interactive_page.py --mode multi-zone` and patched by
`scripts/build_with_qa.py`. If a field isn't in this spec, the build script
ignores it (or worse, breaks). Update this file when you change the schema.

---

## Where it sits in the pipeline

```
deck-plan.json  (palette + fonts + per-page candidate_copy)
    │
    ▼
zones.json      (rectangular blank-zone scan of <page>.png — manual or via find_blank_zone.py)
    │
    ▼
layout_fitter.py  (matches copy fields → zones, picks colors, drops header/footer-unsafe zones)
    │
    ▼
<page>.layout.json   ←── this file's spec
    │
    ▼
build_interactive_page.py --mode multi-zone   →   <page>.html
    │
    ▼
render_screenshot.py + overlay_qa.py (closed loop in build_with_qa.py)
```

You can hand-write a `layout.json` directly when:
- there's no `zones.json` (you eyeballed the safe regions yourself)
- you want full control over copy / coordinates
- you're patching what the LLM produced

The QA closed loop's auto-fix only mutates this file — never zones.json or deck-plan.json.

---

## Top-level shape

```json
{
  "image": "hero.png",
  "image_w": 2048,
  "image_h": 1152,
  "page_id": "fit-checkin-hero",
  "deck_palette": { ... },
  "deck_fonts":   { ... },
  "overlays": [ ... ]
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `image` | string | ✅ | Filename relative to the `.html` output directory. Build copies as-is into `<img src>`. |
| `image_w` | int | ✅ | Logical canvas width in CSS px. Must match the rendered HTML stage. Default deck = `2048`. |
| `image_h` | int | ✅ | Same, height. Default deck = `1152`. |
| `page_id` | string | ✅ | Echoed into QA reports + filenames. Use kebab-case: `case-01-circle-home-v3`. |
| `deck_palette` | object | ✅ | See **Palette** below. Drives CSS variables `--bg --ink --muted --acc1 --acc2`. |
| `deck_fonts` | object | optional | See **Fonts** below. Falls back to built-in Noto stacks if missing. |
| `overlays` | array | ✅ | Each overlay = one positioned text block. See **Overlays** below. |
| `unplaced` | array of string | optional | Echoed by `layout_fitter.py` when a copy field couldn't be slotted. Build prints a warning. |

---

## Palette (`deck_palette`)

```json
{
  "bg":            "#1F1326",
  "ink":           "#F4F0E8",
  "accent_start":  "#FFE411",
  "accent_end":    "#FFC400",
  "secondary":     "#D74E26",
  "muted":         "#9E94A8"
}
```

| Key | Required | Used by build | Used by closed-loop QA fix |
|---|---|---|---|
| `bg` | ✅ | CSS `--bg` (stage background behind the image, visible if image alpha) | locked — fix LLM cannot change |
| `ink` | ✅ | CSS `--ink` + default text color | locked |
| `muted` | ✅ | CSS `--muted` | locked |
| `accent_start` | ✅ | CSS `--acc1` (first stop of `gradient()`) | locked |
| `accent_end` | ✅ | CSS `--acc2` (second stop of `gradient()`) | locked |
| `secondary` | optional | not used in build CSS today; reserved for future role styling | locked |

**Convention**: the palette MUST match the BG color baked into the image
(`bg` ≈ the flat single-color BG you put in the prompt per
`image-prompt-style-uiux.md`). When they drift, overlay text disappears.

---

## Fonts (`deck_fonts`)

Four logical font keys. Each maps to a `font-family` stack with built-in
fallbacks, so individual values can be omitted.

```json
{
  "cjk_display": "Noto Serif SC",
  "cjk_body":    "Noto Sans SC",
  "en_display":  "Cormorant Garamond Italic",
  "en_body":     "Inter"
}
```

| Key | Default fallback | Auto-applied weight |
|---|---|---|
| `cjk_display` | `'Noto Serif SC', 'PingFang SC', serif` | `font-weight: 900` |
| `cjk_body` | `'Noto Sans SC', 'PingFang SC', sans-serif` | (no override) |
| `en_display` | `'Cormorant Garamond', 'Noto Serif SC', serif` | `font-weight: 700` |
| `en_body` | `'Inter', 'Noto Sans SC', sans-serif` | (no override) |

---

## Overlays (`overlays[]`)

Each overlay is an absolutely-positioned `<div class="ov role-...">` containing
one or more vertically-stacked fields.

```json
{
  "role": "title-block",
  "x": 110, "y": 250, "w": 600, "h": 280,
  "fields": [ ... ]
}
```

| Key | Type | Required | Notes |
|---|---|---|---|
| `role` | enum | ✅ | One of `title-block` \| `desc-block` \| `kpi-tile` \| `role-chip`. Drives flex-gap and intent classification in QA. |
| `x` | int | ✅ | Top-left X in canvas px (origin = top-left of stage). |
| `y` | int | ✅ | Top-left Y in canvas px. |
| `w` | int | ✅ | Width. Padding 12px each side is internal — content area = `w - 24`. |
| `h` | int | ✅ | Height. Padding 8px each end — content area = `h - 16`. |
| `fields` | array | ✅ | Order = vertical render order. Min 1, no enforced max. |

**Role → flex gap (vertical spacing between fields)**

| `role` | gap (px) | Typical use |
|---|---|---|
| `title-block` | 14 | section_label + title + subtitle |
| `desc-block` | 6 | description / annotations / role line |
| `kpi-tile` | 4 | one KPI: number + label + sub |
| `role-chip` | 6 | designer / year / tools chip |

**Auto-shrink**: `build_interactive_page.py` calls `_autoshrink_overlay()` per
overlay. If estimated stacked field height > `h - 16`, all `size_pt` are scaled
proportionally down to a min of `9pt`. **The closed-loop QA's auto-patch must
never set `size_pt` < 10** — leave the safety margin to the build step.

---

## Fields (`overlays[].fields[]`)

```json
{
  "key": "title_zh_1",
  "text": "看到熟人",
  "font": "cjk_display",
  "size_pt": 64,
  "color": "gradient(#FFE411,#FFC400)",
  "line_height": 1.1,
  "align": "left",
  "italic": false,
  "letter_spacing": "0.22em"
}
```

| Key | Type | Required | Default | Notes |
|---|---|---|---|---|
| `key` | string | ✅ | — | Logical name (`section_label`, `title_zh`, `desc`, `kpi_number`, `role`, ...). Used by QA reports to point at issues. Suffix `_1`/`_2` when split. |
| `text` | string | ✅ | — | Raw string. Build escapes `& < >`. CJK + emoji OK. Use `\n` only inside JSON-strings — newlines render as space, not `<br>`. To force a line break, split into two fields. |
| `font` | enum | ✅ | — | One of `cjk_display` \| `cjk_body` \| `en_display` \| `en_body`. |
| `size_pt` | number | ✅ | — | Font size in **pt**. Build converts via `pt × 4/3 = px`. Common: 11 (role), 13 (label), 14–18 (anno), 22 (desc), 28–32 (subtitle), 56–72 (title). |
| `color` | string | optional | `palette.ink` | Either a CSS hex `#FFE411` OR the special `gradient(<hex_a>,<hex_b>)` token. Gradient renders via `-webkit-background-clip: text` using the same `acc1/acc2` if you use the actual palette stops, or the explicit hex pair if different. |
| `line_height` | number | optional | `1.2` | CSS unitless. |
| `align` | enum | optional | `left` | `left` \| `right` \| `center` \| `justify`. |
| `italic` | bool | optional | `false` | Adds `font-style: italic`. |
| `letter_spacing` | string | optional | normal | CSS letter-spacing, e.g. `"0.22em"`. Used for ALL-CAPS section labels. |

### `gradient()` syntax in detail

- Form: `gradient(<hex_a>,<hex_b>)` — exactly two hex colors, comma, no spaces.
- The build step swaps `color` for the gradient-text CSS trick (`background-clip: text; color: transparent`) and adds class `grad`. The CSS gradient direction is `120deg` (locked).
- Use it sparingly — a gradient title is a strong visual; pairing with a flat-color subtitle reads cleanest.
- ❌ Don't use gradient on `desc-block` body copy or annotations — they become unreadable at 14pt.

---

## Conventions enforced silently by the build/QA loop

1. **Padding**: every overlay has internal `padding: 8px 12px`. So usable area = `(w-24) × (h-16)`. Plan field height accordingly.
2. **Flexbox vertical center**: contents of `.ov` are `display: flex; flex-direction: column; justify-content: center`. A 60px-tall field in a 280px box ends up vertically centered. Use this — don't add empty filler fields.
3. **Header/footer safe zone**: avoid `y < image_h * 0.05` and `y + h > image_h * 0.95`. The fitter drops zones in those bands, so hand-written layouts should too.
4. **Mockup occlusion**: never place an overlay that overlaps the device mockup in the image. The QA loop will mark this as `severity: blocker`.
5. **Right-aligned annotations**: when `align: right`, anchor `x` so that `x + w` lands ~50–80 px from the right canvas edge. Otherwise text feels like it's floating.
6. **role chips at the bottom**: convention is `y = image_h - 130 ± 10`, `size_pt = 11`, `letter_spacing: 0.15em`.

---

## Minimum viable layout (smallest valid file)

```json
{
  "image": "x.png",
  "image_w": 2048,
  "image_h": 1152,
  "page_id": "x",
  "deck_palette": {
    "bg": "#0F1729", "ink": "#F4F0E8",
    "accent_start": "#FFE411", "accent_end": "#FFC400",
    "secondary": "#D74E26", "muted": "#6B6B6B"
  },
  "overlays": [
    {
      "role": "title-block",
      "x": 110, "y": 250, "w": 600, "h": 200,
      "fields": [
        { "key": "title_zh", "text": "标题", "font": "cjk_display", "size_pt": 60 }
      ]
    }
  ]
}
```

This will build, screenshot, and QA-loop end-to-end. Add more overlays as needed.

---

## What the closed-loop QA may rewrite

When the QA model returns `pass=false`, the fix LLM produces a **revised full
layout.json** with the following constraints (from `FIX_SYSTEM` in `build_with_qa.py`):

| Field | Fix LLM may change? |
|---|---|
| `image`, `image_w`, `image_h` | ❌ frozen |
| `deck_palette`, `deck_fonts` | ❌ frozen |
| `overlays[]` count + order | ❌ frozen |
| `overlays[i].role` | ❌ frozen |
| `overlays[i].x/y/w/h` | ✅ — but cannot move onto the device mockup |
| `fields[].text` | ✅ — wording, fix factual mismatch with image |
| `fields[].size_pt` | ✅ — only DOWN, never below 10 |
| `fields[].color` | ✅ — for contrast flips |
| `fields[].align`, `line_height`, `letter_spacing`, `italic` | ✅ |
| `fields[].key`, `fields[].font` | ❌ frozen |

If you spot the fix LLM violating any of these, tighten `FIX_SYSTEM` in
`build_with_qa.py`.

---

## Worked examples

- [generated-images/jike-circle/anatomy-v3.layout.json](../generated-images/jike-circle/anatomy-v3.layout.json) — dark-social, 7 overlays, 2 gradient titles, single-image M1 layout.
- [generated-images/fit-checkin/hero.layout.json](../generated-images/fit-checkin/hero.layout.json) — light-cream tool, 6 overlays, 1 gradient title, M3 mainshot+callout layout.

Both files passed the closed loop on iter 1 with score 9. Use them as templates.
