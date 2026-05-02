# Multi-Agent Workflow

## Purpose

Use multiple agents when the portfolio task benefits from parallel work: missing screenshots, unclear project story, many pages, image generation, HTML/PPT production, or quality review.

This is an orchestration pattern, not a hard dependency. If the current environment cannot spawn agents or call image tools, run the same roles sequentially in one agent.

## When To Use

Use this workflow when:

- The user has no screenshots and asks the skill to create a portfolio direction from scratch.
- The deck needs generated cover/background/3D support visuals.
- The deck has more than 8 pages.
- The project spans multiple domains, such as mobile app, B-side SaaS, operations visuals, and component library.
- The user asks for multiple directions or variations.
- The final output needs a second-pass critique.

Do not use it for small requests such as a single storyboard, one prompt, or a quick critique unless the user explicitly asks for parallel agents.

## Agent Roles

Lead Agent:
Own the final answer, user assumptions, task framing, and integration. Never hand off the immediate blocking decision if it is needed to keep progress moving.

Strategy Agent:
Build the case-study spine: context, problem, goals, strategy, page order, and missing inputs. Use `portfolio-logic.md` and `page-patterns.md`.

Style Advisor Agent:
Run guided style selection. Recommend 3 differentiated directions, generate or prepare evidence for each, and help the user choose. Use `guided-style-selection.md`.

Visual Direction Agent:
Choose style direction and visual rules. Use `style-directions.md`, `visual-language.md`, and the distilled rules in this skill.

Image Prompt Agent:
Create page-specific image prompts, choose premium model routing, and decide which assets can be generated. Use `image-generation-protocol.md` and `premium-image-model-routing.md`. Protect real UI/logo/product truth.

Builder Agent:
Produce the artifact: storyboard, 2-page showcase, HTML deck, PPTX, image prompt pack, or page copy. Use the integrated plan and visual prompts.

Reviewer Agent:
Score the output using `quality-review.md`, identify weak logic, fake evidence risk, visual hierarchy issues, and missing pages.

## No-Screenshot Workflow

When no screenshots are provided, default to **VISUAL_PROPOSAL** mode (see `asset-gate.md`). This is a complete, image-rich deliverable — NOT a placeholder deck.

1. State assumptions and classify the project type.
2. Pick the mode (almost always VISUAL_PROPOSAL when no screenshots) and label the deck "设计提案 / Visual Direction Proposal".
3. Create a portfolio story spine via `portfolio-logic.md`.
4. Route each page (per Auto-Run step 6) to its production lane: IMAGE_MODEL for covers / section covers / 3D props / atmospheric scenes / **concept UI screens**; HTML_DASHBOARD for any data-screen / admin / B-side page (per `dashboard-rendering.md`); POSTER_BATCH for campaign appendix (per `campaign-poster-batch.md`).
5. Generate concept UI screens with the image model inside the chosen device frame. Each non-real UI page in the deck must carry a `[概念 / Concept]` micro-badge so reviewers cannot mistake it for shipped product. Do NOT draw fake UI in HTML/CSS gray bars and call it a screenshot or a generated image.
6. Use placeholders ONLY for things that genuinely cannot be honestly generated: real shipped screens (when the project IS a real shipped product), real brand logos that don't exist yet, real user quotes, real metrics.
7. Apply `analysis-depth.md` to every analysis page so the deck reads substantive even without real research data.

Recommended parallel split:

```text
Lead: define assumptions and page count.
Strategy Agent: produce 8-12 page case-study spine.
Style Advisor Agent: produce 3 directions and evidence.
Visual Direction Agent: lock grammar after user choice.
Image Prompt Agent: produce a multi-image asset pool plan and prompts for cover/support visuals.
Builder Agent: assemble 2-page showcase first, then full HTML deck after approval.
Reviewer Agent: critique final output.
```

## With Image Tool Available

If an image tool such as `image2`, GPT Image, or Nano Banana Pro is available:

1. Generate prompts first.
2. If current Codex built-in image generation is available and the user asks for direct generation, call it first for quick visual validation.
3. Route to the strongest available model using `premium-image-model-routing.md`.
4. Generate multiple candidates, not one image, for high-polish deck work.
5. Review generated images for fake UI, fake logo, garbled text, and lack of content space.
6. Composite real screenshots later rather than asking the image model to invent them.

## With No Image Tool Available

If no image tool is available:

1. Output a prompt pack with one prompt per needed generated asset.
2. Include negative constraints and composition notes.
3. Mark where real UI screenshots should be inserted later.

## Handoff Format

Each agent should return concise structured output:

```text
Role:
Assumptions:
Key decisions:
Output:
Risks:
Next handoff:
```

## Integration Rules

- The lead agent resolves conflicts between strategy and visuals.
- Real assets always override generated visuals.
- Review findings should trigger targeted revisions, not a full restart.
- In VISUAL_PROPOSAL mode, never reduce imagery to make the deck "more truthful" — the right move is to label concept pages clearly, not to delete them.
