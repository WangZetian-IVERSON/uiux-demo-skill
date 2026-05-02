# Layout Fitter — Rules for slotting copy into discovered zones

The Layout Fitter is **Agent 3** in the 3-agent pipeline (see `references/deck-plan-schema.md`). It runs once per page, **after** the image has been generated and `scripts/find_blank_zone.py --multi` has emitted `<page-id>.zones.json`.

Default implementation is **rule-based**, not an LLM call. The rules below are deterministic so the same image+copy always produces the same overlay. (If a future agent wants to override with creative judgment, it can — but it must produce the same JSON shape this rules engine emits.)

## Inputs

```
deck-plan.json                               (deck.palette, deck.fonts)
deck-plan.json → pages[<i>].candidate_copy   (the writable copy fields)
<page-id>.zones.json                         (multi-zone scan output)
<page-id>.png                                (only for sampling per-zone bg color)
```

## Output

`<page-id>.layout.json`:

```json
{
  "image": "lulu/case-03-membership.png",
  "image_w": 2048, "image_h": 1152,
  "overlays": [
    {
      "zone_index": 0,
      "role": "title-block",
      "x": 96, "y": 220, "w": 740, "h": 520,
      "fields": [
        { "key": "section_label", "text": "CASE 03 · 会员体系", "font": "cjk_body",    "size_pt": 13, "color": "#8B7355", "letter_spacing": "0.18em", "align": "left" },
        { "key": "title_zh",      "text": "会员等级 成长体系",  "font": "cjk_display", "size_pt": 84, "color": "gradient(#F5B700,#E8851A)", "line_height": 1.05, "align": "left" },
        { "key": "subtitle_en",   "text": "Membership · growth", "font": "en_display", "size_pt": 42, "color": "#1A1410", "italic": true, "align": "left" }
      ]
    },
    {
      "zone_index": 1,
      "role": "desc-block",
      "x": 96, "y": 760, "w": 540, "h": 220,
      "fields": [
        { "key": "desc", "text": "重新设计 lulu 会员体系。…", "font": "cjk_body", "size_pt": 18, "color": "#1A1410", "line_height": 1.6, "align": "left" }
      ]
    },
    {
      "zone_index": 2,
      "role": "kpi-tile",
      "x": 1200, "y": 880, "w": 220, "h": 140,
      "fields": [
        { "key": "kpis[0].label",  "text": "会员活跃",      "font": "cjk_body",    "size_pt": 13, "color": "#8B7355" },
        { "key": "kpis[0].number", "text": "84%",           "font": "en_display",  "size_pt": 56, "color": "gradient(#F5B700,#E8851A)" },
        { "key": "kpis[0].sub",    "text": "环比 +18pt",    "font": "cjk_body",    "size_pt": 12, "color": "#8B7355" }
      ]
    }
  ],
  "unplaced": []
}
```

`unplaced` lists `candidate_copy` keys that the fitter could not slot anywhere. The build step warns if non-empty.

## The 7 Rules

These rules execute in order. Each rule consumes one or more zones and one or more `candidate_copy` keys, then removes them from the pool.

### Rule 1 — Sort zones by area, descending

Already done by `find_blank_zone.py --multi`. Just consume `zones[]` in order.

### Rule 2 — Largest zone gets the title block

The single largest zone is assigned `role: "title-block"` and receives, in this order if present:

1. `section_label` (small caps, `cjk_body` 13pt, color `palette.muted`, letter-spacing 0.18em)
2. `title_zh` (`cjk_display`, gradient fill `accent_start → accent_end`, size scales by zone height)
3. `subtitle_en` (`en_display` italic, color `palette.ink`, size = title_zh × 0.5)

Title size formula: `size_pt = clamp( zone.h * 0.18, 56, 120 )`.

If the largest zone is wider than 700px, the title block aligns left. If narrower, center.

### Rule 3 — Second-largest zone gets the description

If `candidate_copy.desc` exists and the next zone has `area_ratio ≥ 0.02`:

- `role: "desc-block"`
- Single field `desc`, `cjk_body` 16–22pt (scale by `zone.w`), `palette.ink`, `line_height: 1.6`.
- Width-clamp text to `zone.w - 32px` for breathing.

If the description is multi-paragraph (newline-separated) and the zone has room, render each paragraph; otherwise truncate after 3 lines with no ellipsis (truncation = the desc was too long; warn at build time).

### Rule 4 — Next N zones get KPI tiles, one per zone

For each remaining `kpis[]` entry, consume one zone (smallest acceptable: 160×100 after padding):

- `role: "kpi-tile"`
- Fields: `label` (12–14pt muted), `number` (40–80pt gradient, scales by zone.h), `sub` (12pt muted).

Stop when KPIs run out OR zones run out.

If a KPI's zone width < 180, drop the `sub` field for that tile.

### Rule 5 — `role` chip goes in the smallest remaining zone touching the bottom edge

If `candidate_copy.role` exists, look for the smallest zone whose bottom edge is within 10% of `image_h`. If found:

- `role: "role-chip"`
- Single field `role`, `cjk_body` 12pt, `palette.muted`, letter-spacing 0.1em.

If no such zone, append `role` to the title block as a small line beneath `subtitle_en`.

### Rule 6 — Per-zone color contrast

For each chosen zone, sample the average background color of the source image inside the zone bounds (use `<page-id>.png`). Compute relative luminance. If luminance < 0.45, flip the field colors:

- `palette.ink` → `#FFFFFF`
- `palette.muted` → `#FFFFFF` at 70% opacity
- gradient stays as-is (it should be readable on either background; if the deck palette violates this, the deck-plan author should pick a different gradient)

### Rule 7 — Drop overlays in zones that overlap the deck header / footer bars

If `zone.y < image_h * 0.05` or `zone.y + zone.h > image_h * 0.95`, the zone is inside the cross-page header or footer bar (which is baked into the image). Skip it — never place HTML text there. This is also enforced as a defensive `padding` on the find_blank_zone side, but the fitter double-checks.

## Font size ladder (palette-derived)

The fitter never invents a size out of thin air. It picks from this ladder:

| Tier | pt | Use |
|---|---|---|
| display-XL | 96–120 | cover title only |
| display-L  | 64–96  | case title (`title_zh`) |
| display-M  | 40–64  | KPI numbers |
| display-S  | 28–40  | secondary headings, subtitle_en |
| body-L     | 18–22  | desc paragraphs |
| body       | 14–18  | inline copy |
| caption    | 11–14  | label, role chip, kpi sub |

`size_pt = clamp(target, tier_min, tier_max)` — the fitter always rounds to the nearest 2pt step.

## What the fitter does NOT do

- It does not invent copy. Every `text` field in the overlay must trace to a key in `candidate_copy`.
- It does not pick the palette. Colors come from `deck.palette`.
- It does not move zones around. It only assigns copy → existing zones (or skips).
- It does not resize the image.
- It does not re-roll the image when zones are insufficient — it emits `unplaced` and lets the caller decide whether to re-prompt the image.

## Failure modes & fallbacks

| Symptom | Likely cause | Fix |
|---|---|---|
| `unplaced` contains `title_zh` | No zone large enough for title-block (largest zone < min). | Re-roll image with `density_hint=spacious`, OR increase `--padding` then re-detect. |
| All KPIs unplaced | Image is too dense, no small pockets remain. | Reduce KPI count in `candidate_copy.kpis`, OR re-roll with `density_hint=balanced`. |
| `desc` truncated at 3 lines | Description too long for the assigned zone. | Trim `desc` in `deck-plan.json`, OR move desc to title-block as a sub-paragraph. |
| Title overlaps a baked phone screen | `find_blank_zone` mask tolerance was too loose. | Re-run with `--tolerance 8` (stricter). |

## CLI contract (for `scripts/layout_fitter.py`, TODO)

```
python scripts/layout_fitter.py \
  --deck-plan deck-plan.json \
  --page-id case-03-membership \
  --zones generated-images/lulu/case-03-membership.zones.json \
  --image generated-images/lulu/case-03-membership.png \
  --out   generated-images/lulu/case-03-membership.layout.json
```

`build_interactive_page.py --mode multi-zone --layout <page>.layout.json --image <page>.png --out <page>.html` consumes the result.
