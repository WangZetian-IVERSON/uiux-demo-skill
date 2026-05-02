# Page Patterns

## Cover

Purpose:
Establish designer identity and visual ambition.

Composition:
Large title on the left, 3D product/deck mockup on the right, dark grid or depth field, small contact/year marks on edges.

Required content:
Year, portfolio/design collection title, designer name or role, contact, optional theme phrase.

## Contents / Project Map

Purpose:
Show scope and make the deck feel curated.

Composition:
Floating cards or spatial blocks arranged on a dark perspective grid. Use one card per project category.

Content:
Project name, category, 1-line scope, optional date marker.

## Profile / Positioning

Purpose:
Tell reviewers what kind of designer they are seeing.

Composition:
Short self-positioning statement, skill tags, project categories, role emphasis, and a compact career or capability map.

Content:
Role, strengths, domain focus, tools, selected project list.

## Project Section Cover

Purpose:
Reset attention and give each project its own world.

Composition:
Large part number, project name, one hero device/screen/mockup, atmospheric background related to the domain.

Content:
Project name, product type, one-line value proposition.

## Project Background

Purpose:
Answer why this project exists.

Composition:
Left title and explanation; right product hero, map, dashboard, or device mockup.

Content:
Background, target users, scenario, problem seed, designer responsibility.

## Problem Diagnosis

Purpose:
Make the design challenge specific.

Composition:
Annotated screenshots, numbered issue cards, pain-point matrix, or a flow with friction markers.

Content:
3-5 concrete issues and their impact.

## Competitive Analysis

Purpose:
Show external learning and opportunity.

Composition:
Competitor screens on the left; test/process strip or insight boxes on the right. Use a dashed container or flow arrow for method.

Content:
Comparison dimension, finding, design opportunity.

## Design Strategy

Purpose:
Convert analysis into principles.

Composition:
Three or four principle cards, an experience map, or a layered pyramid.

Content:
Principle, rationale, design implication.

## Flow / IA

Purpose:
Prove interaction thinking.

Composition:
Task flow, screen relationship, user journey, service blueprint, or information architecture map.

Content:
Entry point, user decision, system feedback, error/edge path, success state.

## Scheme Comparison / A-B Iteration

Purpose:
Prove judgment.

Composition:
Before/after or option A/B split. Make the chosen option larger and visually cleaner.

Content:
What changed, why the selected version is better, tradeoffs.

## Core Page Front

Purpose:
Present the main UI outcome.

Composition:
One full phone/web/dashboard mockup as hero; side callouts explain hierarchy, modules, interaction, and content priority.

Content:
Screen name, module breakdown, top 3 design decisions.

## Interaction Detail

Purpose:
Show craft beyond static UI.

Composition:
Step sequence, state grid, component anatomy, micro-interaction strip, or user flow.

Content:
Trigger, feedback, state change, edge case.

## Data / Dashboard Value Page

Purpose:
Show operational or decision value.

Composition:
Large dashboard crop, metric cards floating in depth, charts with glow accents, map or digital twin if relevant.

Content:
Metric name, insight, decision supported, data hierarchy.

**Render via `references/dashboard-rendering.md`** — always HTML+SVG, never image-model output. Numbers come from a single Dashboard Sample Data block.

## Business Goal Page

Purpose:
Connect product design work to business results.

Composition:
Background paragraph, 3 circular or card-like business goals, and one product/business image. Use concise claims such as user experience, sales innovation, brand communication, or payment conversion.

Content:
Project background, business goals, target scenario, expected value.

## Component Library Page

Purpose:
Prove system thinking and scalable execution.

Composition:
Left side contains rationale and efficiency metric; right side shows angled component boards, icon sheets, color tables, or UI kit fragments.

Content:
Reusable component scope, consistency rule, development efficiency, maintenance benefit.

**Render via `references/dashboard-rendering.md` Pattern D** (HTML/SVG component boards, never image-model output).

## Icon System Page

Purpose:
Show detail craft and category consistency.

Composition:
Clean light surface, repeated icon tiles, category headings, generous spacing, soft shadow, optional colorful 3D-style icons.

Content:
Icon categories, usage context, style rules, replacement/customization logic.

## Operations Visual / Campaign Page

Purpose:
Show visual design range beyond product UI.

Composition:
Dark gallery page or light poster grid. Use 3-5 campaign posters with varied aspect ratios.

Content:
Campaign theme, channel, visual hook, promotion hierarchy, brand continuity.

**Produce via `references/campaign-poster-batch.md`** — batch-generate 4-6 posters sharing one master_motif via image model with reference-image chaining.

## SaaS Website Review Page

Purpose:
Show official website or SaaS landing/product page design.

Composition:
Large laptop/desktop mockup on a pedestal or spatial background, with tags such as technology, lightweight, professional.

Content:
Website goal, product value proposition, information structure, conversion path.

## Visual System

Purpose:
Show consistency and taste.

Composition:
Typography scale, color tokens, icon style, components, logo or illustration system. Use the same deck mood but keep this page more systematic.

Content:
Font, sizes, palette, component rules, usage examples.

## Outcome / Reflection

Purpose:
Close the argument.

Composition:
Metrics, qualitative feedback, before/after summary, launch/handoff result, or next-step reflection.

Content:
What improved, what was learned, what remains unresolved.

## Other Design

Purpose:
Show range without weakening the main cases.

Composition:
Gallery grid or two-column display of logos, VI, posters, brand applications, and side projects.

Content:
Project type and very short label.

## Thanks / Contact

Purpose:
End memorably.

Composition:
Large angled thanks title, small deck mockup/contact panel, QR/contact info.

Content:
Name, email or social/contact, optional QR code.

---


---

## Visual Composition Patterns (2026-05)

The patterns above describe **content roles**. This section describes **visual composition shapes** — the literal arrangement of pixels on the canvas. The two are orthogonal: a case-study page can take any of the visual patterns below.

The deck-plan field page_pattern resolves to one of these. **Variety across the deck is enforced** — Agent 1 must not assign the same page_pattern to two consecutive pages, otherwise the deck reads as one repeated visual gesture.

Each pattern below specifies (a) the prompt fragment Agent 2 should drop into ANCHORS, and (b) compatible reathing_region values.

### `hero-device-orbit`
- One main device (phone / laptop / desktop browser) is the primary anchor. 2 floating extracted UI cards orbit it at slight tilts.
- ANCHORS fragment: *"ONE photo-realistic <device> dominates the frame at ~60% canvas height. Two extracted UI fragment cards (~280×180px each, slight 3–6° tilt) orbit the device — pick the orbit that breathes."*
- Compatible breathing_region: any (left, right, top, bottom, diagonal).
- This is the workhorse — but do not use it for more than 30% of a deck.

### `stacked-extracts`
- NO main device chrome. Instead, 4–6 extracted UI fragments at varying scales and tilts, layered like physical print samples on a desk.
- ANCHORS fragment: *"4 to 6 extracted UI fragment cards at varying scales (largest ~480×320px, smallest ~220×140px) and varying tilts (-12° to +12°), layered like physical print samples on a desk. NO full device chrome appears. The hero card is the largest one — call out which screen it shows. The other cards are supporting fragments."*
- Compatible breathing_region: left, right, top, bottom (NOT diagonal — stacked extracts already create diagonal energy).
- Best for: design-system pages, before-after, process pages.

### `diagram-led`
- The hero is a clean information diagram: a flow chart, a system map, a layered architecture, an information hierarchy, or a decision tree. NO device chrome at all.
- ANCHORS fragment: *"The hero is a hand-drawn-feeling information diagram occupying ~55% of the canvas: <describe the diagram nodes and arrows in 1–2 sentences>. Render with thin <accent_start> strokes, small label text, and 2 or 3 bronze/gold accent dots at key nodes. NO device mockup."*
- Compatible breathing_region: left, right, top, bottom.
- Best for: process pages, system pages, role/positioning pages.

### `type-led`
- Massive editorial type IS the hero (rendered into the image, e.g. a single huge Chinese character or a large foreign-language word as a graphic element). One small supporting visual (a tiny phone, a paper fragment, a tiny diagram) sits in a corner.
- ANCHORS fragment: *"The hero is a massive single graphic typographic element — render the literal characters '<MUST_BAKE_TYPE_STRING>' at ~60% canvas height in <accent_start> -> <accent_end> gradient, treated as a graphic shape (not editorial copy). One small supporting visual (a tiny <device> at ~25% canvas height OR a small extracted UI fragment) sits in a corner."*
- IMPORTANT: the literal characters MUST be added to `must_bake_in_image` of the deck-plan, otherwise TEXT POLICY will forbid them.
- Compatible breathing_region: any.
- Best for: section-cover pages, manifesto pages.

### `full-bleed-photo`
- One photographic hero fills nearly the whole frame, with a thin device or paper edge fragment overlapping one edge.
- ANCHORS fragment: *"A full-bleed photographic hero fills the entire canvas with <photo subject>. A thin slice of a <device> chassis (only ~20% of the device visible, the rest cropped off canvas) overlaps one edge of the photo, showing one in-app screen as a content sample."*
- Compatible breathing_region: bottom (caption strip), top (header strip), left, right (slim column).
- Best for: brand-design pages, photography pages, mood pages.

### `process-strip`
- A horizontal strip showing 3–5 sequential frames of a single transformation (e.g. a button hovering through 5 states, an empty-state to filled state, a low-fidelity sketch evolving to high-fidelity UI).
- ANCHORS fragment: *"A horizontal strip of 4 sequential frames at equal size (~340×500px each), arranged left-to-right with a thin <muted> connecting arrow between adjacent frames. Each frame shows: <frame 1 desc>, <frame 2 desc>, <frame 3 desc>, <frame 4 desc>. The strip occupies the central horizontal band of the canvas; the band above and below is breathing room."*
- Compatible breathing_region: top, bottom (the strip leaves a top OR bottom band), or center-block (strip is the center, breathing wraps around).
- Best for: process pages, animation/interaction pages.

### `before-after-split`
- Two contrasting compositions in one frame, divided by a clean diagonal or vertical line.
- ANCHORS fragment: *"The canvas is split into TWO contrasting halves by <a clean vertical line / a 30° diagonal line>. Left/upper half: '<before>' state — <describe>. Right/lower half: '<after>' state — <describe>. Each half contains one device or one extracted UI fragment, NOT both. The contrast in the two halves is the story."*
- Compatible breathing_region: top (caption above), bottom (caption below).
- Best for: redesign / improvement pages.

### Anti-pattern (avoid)
- Do NOT use `hero-device-orbit` with `breathing_region: left` for two consecutive pages. That formula was the 2026-05 lulu trap.
- Do NOT make every page have 1 device + 2 cards. Mix in `stacked-extracts`, `type-led`, `diagram-led`.
- Do NOT keep the breathing region on the same side for more than 2 consecutive pages.
