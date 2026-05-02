# Source Ingestion

## Authoring Corpus Policy

The original local screenshots used to create this skill were authoring material, not runtime dependencies. Do not automatically inspect, read, or reuse those folders during normal skill use.

At runtime, use the distilled rules in this skill's `references/` folder. Only inspect a local folder when the user explicitly provides that folder as a new task input, such as "analyze this folder and update the skill" or "use this folder as references for this specific project".

When the user explicitly provides a new local corpus:

- Extract style grammar only: page rhythm, density, typography, color roles, composition, screenshot treatment, and case-study logic.
- Do not copy or reuse images from the corpus as materials for a different project.
- Do not assume every future project should use the same visual assets.
- Create a new project-specific asset pool for every theme.

## Distilled Style Coverage

The current distilled rules cover these directions without rereading the original screenshots:

- A dark-tech UI/UX portfolio.
- A 2025 personal design collection.
- Mobile app case-study pages with device mockups.
- Enterprise dashboard or data-visualization portfolio pages.
- A cinematic HTML/PPT deck with blue-black spatial polish.
- A commercial UI/UX portfolio with warmer, lighter packaging.
- Ecommerce app review or marketplace SaaS case-study pages.
- B-side SaaS, admin console, official website, or operations platform work.
- Component/icon library presentation.
- Event poster, campaign visual, or operations design appendix.
- A portfolio that needs to connect visual design to efficiency, consistency, and business conversion.

The distilled rules are enough for:

- A personal UI/UX portfolio spanning mobile app, B-side design, official website, operations visuals, and dashboard work.
- A 20-40 page project review deck with both visual polish and case-study logic.
- A portfolio style that alternates warm commercial pages and dark-tech section covers.

They are still not enough when the requested output needs:

- A hiring/interview portfolio optimized for clarity over visual drama.
- A warm consumer/lifestyle brand style.
- A clean SaaS/product-management design case study.
- A research-heavy UX deck.
- A light editorial portfolio.
- A specific brand, company, or product identity.

When the target falls outside the distilled coverage, ask for new references or use public references when browsing is allowed. Still create new project-specific assets.

## Minimum Input Checklist

For a strong case-study deck, try to gather:

- Project name, platform, role, timeline, and responsibility.
- 3-8 screenshots of final UI.
- 1-3 screenshots or notes about old/current-state UI.
- Problem statement and target user.
- 2-5 design decisions or tradeoffs.
- Benchmark/competitor notes if available.
- Metrics or feedback if available.
- Desired output format and page count.

For a visual-only portfolio, gather:

- Project categories.
- Hero images or representative screens.
- Contact/name/year metadata.
- Preferred tone and forbidden styles.

## Working From Screenshots

When given screenshot folders:

1. Count files and identify page groups.
2. Sample cover, contents, process, UI proof, dashboard, visual system, and ending pages.
3. Extract repeated patterns: title style, spacing, page rhythm, screenshot treatment, color role, and proof logic.
4. Separate style rules from logic rules.
5. Use the screenshots as inspiration, not as a template to copy exactly.

## Working From Screen Recordings

When given videos:

1. Extract representative keyframes at scene changes or every few seconds.
2. Identify the same page groups as screenshot folders.
3. Ask for still screenshots only for pages with important small text or dense UI.
4. Summarize what is visible and what is uncertain.

## Assumption Discipline

If material is missing, write assumptions explicitly:

```text
Assumptions:
- The product is a mobile service app.
- Metrics are unavailable, so outcome pages use qualitative validation placeholders.
- Competitor analysis is represented as a structure placeholder until references are supplied.
```

Do not hide missing inputs under polished visuals.
