# Deck Narrative Architecture

> The reason most AI-generated portfolio decks feel templated: every project gets the same skeleton (cover → KPI case → process case → KPI case). This file forces a deliberate narrative choice **before** any page is written.

---

## Hard Rules (enforced silently by the skill)

**R1 — Pick an archetype before writing deck-plan.json.**
Every deck must declare exactly one `narrative_archetype` from the catalog below. Write it into the deck-plan root.

**R2 — No two adjacent pages may share the same `page_pattern`.**
Visual rhythm is part of the argument. If the archetype demands two consecutive pages of the same role, they MUST take different visual patterns.

**R3 — KPI tiles are gated.**
A page may carry a `kpis` block only if **the user supplied real numbers** OR the archetype is explicitly `outcome-driven`. Otherwise drop the KPI block — replace with an honest qualitative claim, a comparison, or a single insight quote. **Never invent percentages to fill space.**

**R4 — Every page must declare `narrative_role` and `why_this_page`.**
- `narrative_role` ∈ {hook, context, problem, insight, principle, exploration, decision, anatomy, flow, detail, system, outcome, reflection, transition}
- `why_this_page` is one sentence answering "if I delete this page, what claim collapses?"
If you can't write `why_this_page`, the page is decoration — cut it.

**R5 — Show the architecture to the user before generating images.**
After step 3.5 of Auto-Run, post the table `{page_id, narrative_role, page_pattern, why_this_page, needs_real_data}` and wait for confirmation. This is cheaper to revise than 9 credits of imagery.

---

## Archetype Catalog

Each archetype below lists: when to use, the page-role spine, and a default 3 / 5 / 8-page mapping. The page_pattern column references the visual patterns in `page-patterns.md` "Visual Composition Patterns".

### A1 · `argument-arc` — "I saw a problem nobody named, and here's my fix"

When: the project's value is a sharp insight (small UX truth, naming a friction nobody articulated). Best for personal redesigns, opinionated case studies, interview decks.

Spine: **hook → problem → insight → principle → anatomy → outcome-or-reflection**

| 3-page | role | pattern | needs_real_data |
|---|---|---|---|
| P1 | hook (manifesto cover) | `type-led` or `full-bleed-photo` | no |
| P2 | problem→insight (one-page diagnosis with annotated artifact) | `stacked-extracts` or `diagram-led` | no |
| P3 | anatomy (the proposed UI with 3 callouts explaining the principle) | `hero-device-orbit` | no |

| 5-page | role | pattern |
|---|---|---|
| P1 | hook | `type-led` |
| P2 | problem | `stacked-extracts` (annotated current-state) |
| P3 | insight | `diagram-led` (the lever, drawn as a 2-axis or causal arrow) |
| P4 | anatomy | `hero-device-orbit` (the redesigned screen) |
| P5 | reflection | `full-bleed-photo` w/ short paragraph |

### A2 · `before-after-comparison` — "I made it measurably better"

When: there is a real shipped redesign with real metrics. Honest A/B story.

Spine: **context → before-state → after-state → mechanism → outcome**

| 3-page | role | pattern | needs_real_data |
|---|---|---|---|
| P1 | context cover | `full-bleed-photo` | no |
| P2 | comparison (split-canvas before/after) | `stacked-extracts` (left=before, right=after) | yes |
| P3 | outcome with KPIs | `diagram-led` (a 2-bar chart + 2 callouts) | **YES** |

KPI gate: this archetype is the ONLY 3-page archetype where invented KPIs are tolerable as `[concept data]` — but they MUST be labeled.

### A3 · `option-tradeoff` — "I considered three paths and chose this one because"

When: the value is the judgment, not the polish. Senior IC interview decks, strategy reviews.

Spine: **context → option-A → option-B → option-C → decision-with-reasoning → result**

| 3-page (compressed) | role | pattern |
|---|---|---|
| P1 | context + question | `type-led` (the question as graphic) |
| P2 | three options on one canvas | `process-strip` (3 frames = 3 options, with checkmark on chosen) |
| P3 | the chosen design | `hero-device-orbit` |

### A4 · `process-journey` — "Here's the user's path, here's where I intervened"

When: workflow / multi-step task / onboarding / checkout / triage. Service-blueprint thinking.

Spine: **persona → current-journey → friction-map → redesigned-journey → key-moment-zoom**

| 3-page | role | pattern |
|---|---|---|
| P1 | persona+context cover | `full-bleed-photo` (the user's environment) |
| P2 | journey map (current vs new, marked friction) | `diagram-led` |
| P3 | one key moment screen, zoomed | `hero-device-orbit` |

### A5 · `system-anatomy` — "I built a system, here are its parts"

When: design system / component library / multi-surface product / IA-heavy work.

Spine: **system overview → primitives → composition rules → application 1 → application 2**

| 3-page | role | pattern |
|---|---|---|
| P1 | system overview | `diagram-led` (the system map) |
| P2 | primitives | `stacked-extracts` (component sheet) |
| P3 | application | `hero-device-orbit` (one shipping surface) |

### A6 · `single-screen-deep-dive` — "I will spend the whole deck on one screen, and earn it"

When: the value is in micro-craft. Show one feature with maximum depth.

Spine: **the screen → why this screen matters → 3 details → edge cases**

| 3-page | role | pattern |
|---|---|---|
| P1 | the screen, full-bleed | `full-bleed-photo` |
| P2 | 3 detail crops | `stacked-extracts` (all 3 from same screen, ringed) |
| P3 | edge cases / states | `process-strip` (4 states of one component) |

---

## Picking an archetype (decision tree)

```
Does the user have real shipped metrics?
├── YES → A2 (before-after-comparison)
└── NO
    ├── Is it a multi-surface system / IA / library?
    │   └── YES → A5 (system-anatomy)
    ├── Is it a workflow / checkout / onboarding / triage?
    │   └── YES → A4 (process-journey)
    ├── Is the value the judgment between options?
    │   └── YES → A3 (option-tradeoff)
    ├── Is the value craft on one feature/screen?
    │   └── YES → A6 (single-screen-deep-dive)
    └── Default → A1 (argument-arc)
```

When in doubt for a 3-page demo without real data, **A1** is the safest — it lets the designer's perspective be the artifact.

---

## Worked Example — 即刻 · 圈子改版 (3 pages)

This was originally written as a templated cover + KPI case + process case. Re-architected:

- **Archetype**: A1 (argument-arc). No real metrics; the value is the insight "把小圈子做小一点".
- **KPI gate**: dropped all "+52% / +38%" — they were invented.
- **Pattern variety**: `type-led` → `diagram-led` → `hero-device-orbit` (no repeats).

| page_id | narrative_role | page_pattern | why_this_page |
|---|---|---|---|
| `manifesto` | hook | `type-led` | 让评委 3 秒记住我的立场："小圈子要做小"——反潮流的设计主张 |
| `diagnosis` | problem→insight | `diagram-led` | 用一张「广场化曲线」证明圈子变大反而流失归属感，把抽象不适感落到一张可读的图 |
| `anatomy` | anatomy | `hero-device-orbit` | 给出主张的具体落点：圈子首页两栏（人/事），让"看到熟人"成为可见交互 |

Each page now has a non-redundant claim. P1 says what I think. P2 proves I'm right. P3 shows what I'd build.

---

## Anti-patterns this file is designed to kill

- **The Three-Card Trick**: cover + "case with 3 KPIs" + "case with 4-phone process strip". Every project ends up looking the same.
- **Invented metrics**: "+52% retention" with no source, no methodology, no data.
- **Decorative pages**: a page exists because the deck "needs more pages", not because it carries an argument.
- **Pattern reuse**: two adjacent stacked-extracts pages — the eye sees one page, not two.
- **Missing the question**: no page in the deck states what the design is *answering*.
