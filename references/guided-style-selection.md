# Guided Style Selection

## Purpose

Guide the user toward a visual direction before producing a full UI/UX portfolio deck. This follows the Huashu Design pattern: when the direction is not locked, act as a design direction advisor first, then produce.

## Trigger

Use this flow when:

- The user says "make it look good", "make a portfolio", "generate a PPT", or gives only a topic.
- The user has no screenshots or brand assets.
- The user asks for better visual quality.
- The deck has 5 or more pages and the style is not already confirmed.
- The user asks for Huashu-like quality or guided style selection.

Skip only when:

- The user explicitly gives a precise style and says to proceed.
- The task is a quick one-page image, prompt, or critique.
- The user says "do not ask, just generate".

## Phase 1: Ask Only The Minimum

Ask at most three short questions if missing answers materially affect the result:

```text
1. What is the project domain? Example: ecommerce app, hotel booking, smart power dashboard, B-side SaaS.
2. Who is the deck for? Example: job portfolio, design review, client pitch, annual review.
3. Which output do you want first? Style options, 2-page showcase, HTML deck, PPTX, or image prompt pack.
```

If the user already gave enough context, do not ask. Move directly to Phase 2.

## Phase 2: Recommend 3 Directions

Recommend exactly three directions. They must differ in structure, mood, and production path, not only color.

Each direction must include:

- Name.
- Suitable use case.
- Visual signature.
- Page rhythm.
- Asset strategy.
- Risk.
- Recommended first showcase pages.

Example format:

```text
Direction A: Warm Commercial Case Study
Best for: ecommerce, local retail, marketplace SaaS.
Visual signature: orange/cream surfaces, dense phone collages, playful 3D commercial props, business-goal cards.
Page rhythm: cover -> business goals -> problem -> UI proof -> component system -> campaign visuals.
Asset strategy: generate shopping props, coupon cards, phone staging scenes; use placeholder UI until real screenshots arrive.
Risk: can become too cute unless business value is explicit.
Showcase first: cover + core UI collage page.
```

## Phase 3: Show Visual Evidence

Do not leave directions as abstract words.

Use one of these evidence paths:

- If generated image is available: directly generate one small cover/hero sample for each direction.
- If using Huashu vendor only: show matching upstream showcase screenshots as mechanical examples, while making clear they are not final UIUX style.
- If image generation is unavailable: output one prompt per direction and ask the user to choose.

The preferred path in Codex with image generation available:

```text
Generate 3 quick direction images, one per style, low commitment.
Ask the user to choose A/B/C or mix parts.
Then create 2-page showcase for the chosen direction.
```

## Phase 4: User Choice

Ask for a concrete selection:

```text
Choose one:
A. Warm commercial
B. Dark-tech command center
C. Clean B-side SaaS
Or tell me a mix, such as "A's color + C's layout".
```

Do not batch-produce a full deck before this choice unless the user explicitly asks to skip selection.

## Phase 5: Lock Grammar

After the user chooses:

- Define deck tokens: background, type scale, accent color, grid, screenshot treatment, imagery style.
- Define asset pool: generated assets, real screenshots needed, placeholders.
- Move to `showcase-first-deck-workflow.md`.

## Quality Bar

The style selection fails if:

- All three directions look like the same template.
- The directions are only color variations.
- The user cannot tell what the final deck would feel like.
- The suggested direction ignores the project domain.
- It jumps directly to a full deck without style confirmation.
