# Dashboard Rendering

## Why This Module Exists

Image generation models cannot produce credible dashboard screenshots: numbers come out garbled, charts look approximate, Chinese labels mis-render, and the same dashboard regenerated never matches.

But "designing a dashboard mockup with plausible structure and styled fake data" is exactly what UI designers do every day. It is **not fabrication of evidence** — it is **design work, rendered as a designed mockup**, the same way Figma mockups go into a portfolio.

This module gives the skill a way to render dashboard / data-visualization / admin-console mockups using HTML/CSS/SVG, then use those renders as legitimate "designed UI" inside the deck. The result reads as "the designer designed this interface", not as "the designer screenshotted a real product".

## When To Use This Module

Use HTML-rendered dashboard mockups when the deck needs:

- Enterprise data dashboards (smart power, smart city, IoT, manufacturing, fleet, finance).
- Admin console / B-side SaaS list pages, detail pages, table-heavy pages.
- Operations / monitoring screens with charts, KPI cards, maps, status panels.
- Mobile app data screens with charts, metric cards, progress rings.
- Component library / design system showcase pages.
- Onboarding / settings / configuration screens.

Do NOT use this module to fake screenshots of a real shipped product. If the project IS a real existing product, use the user's real screenshots.

## Honesty Boundary

HTML-rendered mockups are honest under these conditions:

1. The deck mode is `VISUAL_PROPOSAL`, OR the deck mode is `FULL_CASE_STUDY` for a project the user actually designed (the dashboard mockup is the user's design work).
2. Numbers, labels, and dataset names are **plausible-but-styled fake** data — i.e. they look like real product data but are clearly designer-chosen sample values, not claimed measurements.
3. The mockup is presented as "designed UI", never as "live product screen of company X".
4. The dashboard does not display fabricated business outcomes ("用户增长 28%") as if they were measured results in the case-study narrative. Numbers can live inside the UI mockup as design content; they cannot live in the case-study reasoning text as evidence.

## Sample Data Convention

Pick coherent fake data once per dashboard, save it at the top of the page file, then reuse. Do not invent fresh numbers per chart.

```text
=== DASHBOARD SAMPLE DATA (deck-internal) ===
domain:                 smart-power | smart-retail | finance-saas | fleet | manufacturing | wellness
time_range:             2025-Q1 ~ 2025-Q4 (or one specific month)
primary_metric:         总能耗 / 总订单 / 总会话 / 总车次  → value range: e.g. 12,400 ~ 18,600
secondary_metrics:      3-5 KPI names + value ranges
unit_convention:        kWh | 万元 | 次 | 辆 | 台 | %
chart_series:           name + 12-month plausible curve (use a smooth curve, not random noise)
geographic_scope:       e.g. "贵州 9 个市州" / "全国 24 个城市" / "华东 6 省"
status_buckets:         e.g. 正常 / 预警 / 故障 (with realistic ratio like 78% / 18% / 4%)
=== END ===
```

All numbers in the rendered dashboard MUST come from this block. Never sprinkle random numbers across charts.

## Rendering Stack

Use a small, controlled tech stack. Do not import a real chart library wholesale — those produce generic Chart.js / ECharts looks that scream "demo".

Allowed:

- **SVG written by hand** for charts (line, bar, donut, area, gauge, radial). This is the highest-control option and gives the most "designed" look.
- **CSS Grid + flex** for KPI card grids, table rows, status pills.
- **Inline SVG icons** from a controlled micro-set (Lucide outline OR custom). Pick one set per project; do not mix.
- **Static map SVG** (China province outline, world simple, or a domain-specific map outline) as background; overlay status dots / pulse rings / connection lines on top.

Forbidden:

- Off-the-shelf default chart styles (Chart.js orange-blue defaults, ECharts demo themes). Always restyle to the project palette.
- Random data that doesn't tell a story. Pick a plausible curve.
- Tooltips, hover states, animations as showcased UI evidence (these are interaction details, render them only on dedicated interaction pages).

## Page Patterns

### Pattern A — Single Hero Dashboard

One full dashboard fills the canvas. Used as the deck's "core proof" page for a B-side / admin / data project.

```text
Layout:
  [Top bar: product name + breadcrumb + user + status pill] — 8% height
  [Left rail: 6-8 nav icons + labels] — 8% width
  [Main canvas: 12-grid]
    rows 1-2: 4 KPI cards (number + tiny sparkline + delta arrow)
    rows 3-6: hero map (left 7 cols) + ranked list (right 5 cols)
    rows 7-9: line chart (left 6 cols) + donut + status table (right 6 cols)
  [Optional right rail: alert feed]
```

### Pattern B — Map Digital Twin Cover

Used for smart-city / smart-power / IoT projects. Map fills the canvas; KPI floats over it.

```text
Layout:
  Background: dark navy with faint hex grid + simplified geographic SVG outline (province / city)
  Status dots: 30-80 dots placed on real geographic positions, three sizes, three colors per status
  Pulse rings: 4-6 dots with animated pulse to indicate activity (static keyframe in PPT export)
  Floating KPI cards: 3-4 glass cards anchored top-right and bottom-left, with the sample data
  Connection lines: 2-4 glowing arcs between major dots
  Title block: top-left with bilingual heading
```

### Pattern C — Mobile App Data Screen

iPhone frame with a designed data screen inside. The screen is HTML-rendered, then composited inside the iOS frame component.

```text
Inside the phone:
  [Status bar]
  [Greeting + date + segment switcher]
  [Hero metric: large number + unit + delta + 7-day sparkline]
  [Secondary KPI grid: 2x2]
  [Bar/donut chart with title]
  [List of items with tiny indicator + value]
  [Bottom tab bar]
```

### Pattern D — Component Library / System Page

Right side shows angled component boards (cards, buttons, inputs, table rows, chart variants), left side explains the system rationale.

### Pattern E — Operations Console Multi-Pane

Three-pane: list + detail + side panel. Used for ticket systems, order management, content moderation.

## Visual Style Discipline

The dashboard mockup must reuse the project's PADB:

- Background, surface, primary/secondary accent **inherit from PADB**.
- Typography inherits from the deck meta-PADB.
- Card material (frosted glass / matte panel / clean white) inherits from PADB.
- Icon set is locked once per project.

If you find the dashboard wanting a color or material outside the PADB, update the PADB first.

## Chart Style Discipline

Each chart type renders in ONE locked style across the whole deck:

| Chart | Locked style |
|---|---|
| Line | 1.5px stroke in primary accent, 8% area fill below, dot at last point only |
| Bar | rounded-top 4px radius, primary accent for "now" series, 30% opacity for "previous" series |
| Donut | 8px stroke width, three colors max from palette, center label with big number + small unit |
| Sparkline | 1px stroke, no axis, no labels, 24-32px tall |
| Status pill | 2px radius, 11px label, four bucket colors max (success / warning / danger / neutral) |
| KPI card | flat surface, big number 32-48px, unit 14px, delta arrow + percentage |

Lock these in the deck meta-PADB once and never deviate.

## Density Targets

Match the visual density of premium portfolio templates:

- A hero dashboard page should show: 4 KPI + 1 hero chart + 1 secondary chart + 1 list/table + 1 status indicator. Never a single chart on a huge empty canvas.
- A mobile data screen should show: hero metric + 2-4 secondary cards + 1 chart + 1 list. Never a single chart.
- Negative space exists, but every visible region carries information.

## Map Treatment

For map-based dashboards (Pattern B):

- Use a simplified province/city outline SVG. Do not use a generic world map.
- Geographic positions of status dots should be approximately correct (Guizhou cities should be in Guizhou). Do not scatter randomly.
- The map color is a darker shade of the PADB surface, with a 1px primary-accent border.
- Hex grid background: 24px hexagon, 4% opacity.
- No real-world satellite imagery. No copyrighted map tiles.

## Output Pipeline

1. Pick the page pattern.
2. Define / reuse the dashboard sample data block.
3. Render the dashboard HTML/SVG inside the deck page (or as a standalone component composited into a device frame).
4. Place callouts and explanation copy around it.
5. Visually QA against the PADB and against the chart-style lock table.

## What NOT To Do

- Do not feed dashboard mockup prompts to an image model. Image models cannot render numbers consistently.
- Do not screenshot the rendered dashboard and call it a "generated image". It is HTML — present it as the designed UI it is.
- Do not pretend the rendered numbers are measured business outcomes in the narrative text.
- Do not let dashboards drift in style from page to page. The chart lock table is the contract.
- Do not include real company names / real product names / real customer names inside the dashboard sample data unless the user provided them.
