# Premium Image Model Routing

## Purpose

Use stronger image-generation models and a multi-candidate workflow when the user expects output close to the local reference folders. The reference folders are image-dense, composed, and polished; a single generic image prompt is not enough.

## Model Preference

Use this routing when the environment or user has access. **Read the capability rule first**: only count a model as available if it is a real image-generation model, not an HTML/DOM renderer. If the only "image tool" available rasterizes HTML, treat that as **no image tool** and route to `PROMPT_PACK_ONLY` per `image-generation-protocol.md`.

1. Nano Banana Pro / Gemini 3 Pro Image:
   Best for high-fidelity design visuals, accurate text rendering, multilingual text, 2K/4K assets, reference-image blending, and controlled camera/lighting/composition. Prefer it for portfolio covers, campaign posters, commercial 3D objects, and Chinese-title assets.

2. GPT Image / gpt-image-1:
   Best for instruction-following, API integration, professional-grade image generation, brand-guided assets, and iterative editing workflows. Prefer it when the skill is connected to OpenAI API tooling.

3. Recraft V3 / Ideogram 2:
   Best for typographic posters, brand-color-locked compositions, and vector-style assets.

4. Codex built-in image generation:
   Use only after confirming it calls a real image model and produces 1024px+ output with non-garbled text. Otherwise treat as unavailable.

5. Midjourney v6 / v7:
   Useful for atmospheric covers and cinematic backgrounds, but avoid for text-heavy UIUX pages unless text is added later in HTML/PPT.

6. SDXL / Flux via configured endpoint:
   Fallback for support props and exploration, not for final cover-quality assets.

If none of the above are callable in the session, do not invent a substitute. Output a prompt pack and tell the user which model to run it on.

## Required Generation Strategy

For polished UIUX portfolio generation:

- Generate 3-4 visual directions when the style is unclear.
- Generate a separate asset pool for each project theme.
- Generate 4 candidates for cover pages.
- Generate 2 candidates for each section background.
- Generate 4-8 support objects: 3D mascot, shopping terminal, glass card, coupon, phone pedestal, laptop scene.
- Generate 3-6 operations/campaign poster placeholders for commercial portfolios.
- Keep real UI screenshots or placeholders separate from generated images.
- Composite final pages in HTML/PPT using the generated assets, not directly from the image model.
- Do not reuse generated materials from a previous project unless the user says it is the same brand/system.

## Reference-Driven Prompting

When user-provided screenshots exist:

1. Extract style traits from the folder.
2. Use the folder as style direction only for that task.
3. Do not copy exact layouts or recreate screenshots one-for-one.
4. Ask image models for reusable assets: backgrounds, 3D props, device scenes, visual motifs.
5. Add actual deck title, UI screenshots, metrics, and body copy in HTML/PPT.

## No-Screenshot Premium Workflow

If the user has no UI screenshots:

1. Generate a complete visual asset pool.
2. Use placeholder UI panels inside phone/laptop frames.
3. Label product UI areas as placeholders.
4. Generate cover/background/3D/campaign visuals with premium models.
5. Make the visual asset pool specific to the project theme, not copied from a previous deck.
6. Build final pages with strong layout density so they resemble a portfolio deck rather than a single AI poster.

## Prompt Quality Bar

Prompts must specify:

- Aspect ratio and target resolution.
- Page role and domain.
- Reference direction: dark-tech portfolio or warm commercial portfolio.
- Composition with exact empty areas for title/UI insertion.
- Material, lighting, color grading, and camera angle.
- Asset density: foreground object, secondary props, background texture, small details.
- Negative constraints: no fake UI, no random logo, no watermark, no unreadable text.

## Quality Gate

Reject outputs under this bar:

- One-object center composition with empty generic background.
- Fake UI pretending to be real screenshots.
- Garbled Chinese/English text.
- Stock-poster feeling without UIUX case-study logic.
- Too few assets to build a dense page.
- Visual style not matching either local reference folder.

## Recommended External Tools

If the current Codex environment cannot call premium image generation directly, output a prompt pack for:

- Gemini Nano Banana Pro / Gemini 3 Pro Image.
- OpenAI GPT Image / gpt-image-1.
- The user's `image2` endpoint if configured.

Always include generation counts and selection criteria so the user can batch-generate and choose the strongest candidates.
