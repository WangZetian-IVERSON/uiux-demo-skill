# Asset And Fact Protocol

## When To Use

Use this protocol whenever the deck involves a real product, brand, company, app, platform, public launch, product version, metric, or public event.

## Fact Verification

Before making factual claims:

1. Search current public sources when the fact may be recent or uncertain.
2. Confirm existence, official naming, release state, version, and key facts.
3. Mark unverified items as assumptions.
4. Do not present inferred metrics, user counts, conversion changes, or launch results as facts.

## Core Asset Priority

Use real assets whenever possible. Priority:

1. Logo.
2. Product/UI screenshots.
3. Product renderings or official imagery.
4. Brand colors.
5. Fonts.
6. Voice/tone and visual references.

Color and typography are not enough for recognizable brand work. A deck about a product needs the product to appear.

## Asset First, Image Generation Second

Follow this order:

1. Use user-provided screenshots, UI exports, and real project materials.
2. Use official/public assets when the project is a real brand or product and public sourcing is allowed.
3. Use generated images only for missing support assets: cover scene, 3D decoration, abstract background, generic commercial object, neutral device scene, or illustration.
4. Do not replace real UI screenshots, logos, product screens, or factual dashboards with generated approximations unless the user explicitly asks for a concept/fake demo.

This borrows the Huashu Design principle: assets are the identity. Image generation is a supplement, not a substitute for the product.

## Asset Intake Prompt

Ask for assets in one compact list:

```text
Please send any assets you already have:
1. Logo, preferably SVG or high-res PNG.
2. Product screenshots or app/dashboard UI.
3. Old/current-state UI if this is a redesign.
4. Brand colors or design system links.
5. Metrics, research notes, or stakeholder feedback.
6. Preferred reference decks or styles.
```

If the user has no assets, gather public official assets when allowed and clearly note sources.

## Asset Quality Gate

For hero assets, use a 5-10-2 style gate:

- Search or inspect at least 5 source directions when public assets are needed.
- Gather around 10 candidate visuals when possible.
- Select 2-4 strong assets.
- Reject assets below roughly 8/10 quality.

Score assets on:

- Resolution.
- Officialness/source reliability.
- Brand fit.
- Composition and lighting.
- Whether the asset can carry a page by itself.

## Brand Distance (when the deck is delivered TO a real company)

If the deck is a portfolio / proposal **delivered to a specific real company** (e.g. a JD application portfolio, a Tencent proposal deck), the deck must NOT cosplay that company's brand identity. The deck is the candidate's work, not the target company's collateral.

When a target-company is identified, lock these rules into the deck meta-PADB:

```text
target_company:           e.g. JD.com
target_brand_color:       e.g. #e1251b (JD red)
forbidden_in_deck:        target_brand_color used as deck primary; target_company logo on cover; target_company product UI screenshots presented as the candidate's own work; target_company slogan or tagline
allowed:                  small respectful mention on the closing/contact page ("投递目标 / Target: JD"); target-company-aligned tone in writing
deck_primary_color:       must be visibly distinct from target_brand_color (different hue family, not just lighter/darker)
```

Why: a deck that uses JD red, JD logo, and JD product mockups looks like internal JD design output, not like a candidate's portfolio. It also confuses the reviewer about what the candidate actually shipped vs. what's aspirational.

The candidate's case studies inside the deck SHOULD however target the company's domain (e.g. ecommerce operations, member growth) so the work is relevant. Domain alignment yes, brand cosplay no.

## Brand Spec — 5-Step Hard Process

When a real brand is involved, follow these 5 steps in order. Each step has a fallback. Do not skip and do not quote brand colors / logo geometry / wordmark from memory — that is the #1 failure mode of branded portfolio work.

| # | Step | Action | Fallback if blocked |
|---|---|---|---|
| 1 | **ASK** | Ask the user once: do you have brand guidelines / a brand kit / an internal style guide? | If no, continue to step 2 |
| 2 | **SEARCH official brand page** | Try in order: `<brand>.com/brand`, `brand.<brand>.com`, `<brand>.com/press`, `<brand>.com/about/logo`, `<brand>.com/newsroom` | If none reachable, search "<brand> brand guidelines" / "<brand> press kit" / "<brand> visual identity" |
| 3 | **DOWNLOAD assets** | Three fallbacks in order: (a) official SVG / EPS / brand kit ZIP; (b) full HTML of the official site (will contain inlined SVG and CSS variables); (c) high-res product screenshots from official channels | If all three fail, mark logo as `[unavailable]` and ask the user to upload one |
| 4 | **GREP hex codes** | From downloaded assets, regex `#[0-9A-Fa-f]{6}` and `rgb\([^)]+\)`, sort by frequency, drop pure white / black / mid-greys. Top 3-5 are the brand palette. Cross-check by eyedropping the official logo PNG. | Never guess. If grep yields nothing usable, treat the brand as `[palette-unverified]` and ask the user |
| 5 | **FREEZE spec** | Write `brand-spec.md` at the deck root (template below). Define CSS variables (`--brand-primary`, `--brand-ink`, etc.). All later HTML pages reference `var(--brand-*)`. All later image prompts quote the hex from this file, not from memory. | n/a — this is the deliverable of the protocol |

After step 5, treat `brand-spec.md` as immutable for the rest of the deck. If something feels "off color", verify against the spec — do not adjust the spec to match a hunch.

### Brand Spec Template

For substantial branded work, create or maintain a compact `brand-spec.md` near the output:

```markdown
# Brand Spec

## Facts
- Product/company:
- Verification date:
- Sources:

## Assets
- Logo:
- UI screenshots:
- Product imagery:

## Visual System
- Primary colors:
- Secondary colors:
- Type:
- Signature details:

## Assumptions
- 

## Forbidden
- 
```

Use the spec while designing. Do not redraw logos or products from memory.

## When Assets Are Missing

- Missing UI screenshots: ask the user for screenshots, use placeholders, or build simple wireframe placeholders. Do not hallucinate a real app UI as if it existed.
- Missing logo: ask the user or use a clearly labeled placeholder.
- Missing cover decoration: generate a neutral visual asset with `references/image-generation-protocol.md`.
- Missing campaign poster examples: generate clearly illustrative poster placeholders only if the user accepts concept examples.
