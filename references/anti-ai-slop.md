# Anti AI Slop

Read this before writing ANY HTML/CSS or image prompt. The biggest reason UI/UX portfolio decks come out looking "AI-generated" is not the model — it is the visual vocabulary the agent reaches for by default. Block that vocabulary up front.

## Forbidden Visual Vocabulary

These patterns are banned across HTML, CSS, slides, and image generation. If you catch yourself producing one, stop and rework.

### Color & Gradient

- NEVER use generic purple-to-pink or purple-to-blue gradient backgrounds as the deck base.
- NEVER use neon rainbow gradients on text or buttons.
- NEVER fall back to `#7c3aed` / `#a855f7` / `#ec4899` family as accent without a brand reason.
- NEVER stack three or more gradients in one composition.
- Prefer flat-with-texture or single-direction subtle gradients tied to the project domain.

### Type

- NEVER use Inter / Helvetica / Arial as a hero/display face. They are body fonts.
- NEVER use system-ui sans for large titles. Use a real display face (Chinese: 思源黑体 Heavy / 阿里巴巴普惠体 Heavy / Misans Heavy / OPPOSans Heavy / 鸿蒙黑体 Heavy. Latin: a real display serif or wide grotesk).
- NEVER use emoji as functional icons in a portfolio deck. Use line icons or 3D rendered icons.
- NEVER set body copy below 14px at 1280px canvas, or below 18px at 1920px canvas.

### Layout

- NEVER use the "card with rounded corners + 4px left border accent + icon + title + body" pattern. It is the most overused AI layout.
- NEVER place 4 phone mockups in a single horizontal row as the only proof page. It reads as a template.
- NEVER center every element on the page. Use asymmetric grids.
- NEVER use evenly spaced 3-column "feature card" grids as a hero section.
- NEVER decorate a page with floating gradient blobs / blurry circles / random sparkles to fill empty space.

### UI Mockups

- NEVER paint fake UI inside a phone/laptop frame using HTML/CSS gray bars and colored rectangles, then save the rendered DOM as a `.png`, then present it as either a real screenshot or a generated image. This HTML-screenshot fake is the single biggest tell of AI slop in a portfolio.
- For real shipped products: use the user's actual screenshot, or a clearly labelled `[真实产品截图待补充]` placeholder. Do not draw fake UI in CSS.
- For visual proposals (concept work): generate concept UI screens with the IMAGE MODEL inside the device frame. This is acceptable and labelled as concept. Never produce concept screens by drawing CSS gray-bar layouts.
- Image-model-generated concept screens must look like a real designer's mockup (clean grid, real typography, plausible product copy), not like a wireframe of gray bars.

### Iconography

- NEVER mix flat outline icons + filled icons + emoji + 3D icons in one deck.
- NEVER use generic stock icon sets (Heroicons / Feather) as the visual highlight of a portfolio page. They are utility-grade, not portfolio-grade.
- NEVER draw faces, mascots, or characters in raw inline SVG. Either render in 3D via the image model or omit.

### Effects

- NEVER apply glassmorphism (blur + translucent + thin border) to more than one layer at a time.
- NEVER use the same drop shadow on every card.
- NEVER apply outer glow to text — it almost always reads as cheap.
- NEVER animate everything. Pick at most 2 motion roles per deck.

### Data Visualization

- NEVER use the default look of an off-the-shelf chart library (Chart.js orange-blue, ECharts demo theme, default Recharts). They scream "demo". Restyle to the project palette.
- NEVER use rainbow series colors (>3 distinct hues) on one chart.
- NEVER show charts without a story — a flat line, random noise, or values that contradict the case-study narrative.
- NEVER place a single chart on a huge empty canvas as a "data page". Pair every chart with KPI cards / a list / a status indicator (see references/dashboard-rendering.md density targets).
- NEVER let an image model render a numeric dashboard. Numbers will be garbled. Use HTML/SVG per references/dashboard-rendering.md.
- NEVER claim chart numbers are measured business outcomes when the user did not provide them. They are designed sample data inside a UI mockup.

### Copy

- NEVER write generic marketing copy as a substitute for design reasoning. "Beautiful, intuitive, modern" tells the reader nothing.
- NEVER pad pages with lorem ipsum or "AI-style" filler ("In today's fast-paced world…").
- NEVER fabricate metrics. If the user did not give numbers, use a placeholder block: `[Metric: <name> — to be confirmed]`.

## Required Replacements

When you would have reached for a banned pattern, use these instead:

| Banned default | Required replacement |
|---|---|
| Purple gradient bg | Domain-tied palette: dark-tech (deep navy + electric cyan), warm commercial (charcoal + amber), B-side SaaS (paper + cobalt), wellness (ink + soft purple-blue). One palette per project. |
| Inter display title | A specified display face. State the exact font in the page header comment. |
| 4-phones-in-a-row | One hero phone at scale + 2-3 callouts pointing to specific UI decisions. |
| Card-with-left-border | Numbered analysis block, dashed-method container, or split column with a clear label rail. |
| CSS-drawn gray-bar fake UI | For real product: real screenshot or labelled `[真实产品截图待补充]`. For concept project: image-model-generated UI mockup inside the frame. |
| Generic Heroicons | Project-specific 3D rendered icons via the image model, or a custom line-icon micro-set. |
| Glassmorphism everywhere | One glass surface per page, with a real reason (active state, focus panel). |

## Self-Check Before Output

Before saving any HTML page or image prompt, answer:

1. Could this exact page have been produced for any other project? If yes, it is too generic — add domain specificity.
2. Is there a single page where I drew fake UI inside a phone? If yes, replace with placeholder or real screenshot.
3. Is the accent color tied to the project domain or just a default purple/blue? If default, switch.
4. Does every "card" use the same shape and shadow? If yes, vary at least three card roles.
5. Is the display face actually a display face, or did I default to Inter/system-ui?
6. Are there at least three distinct page-type layouts in the deck, or did everything collapse to title + cards?

If any answer fails the bar, rework before delivering.
