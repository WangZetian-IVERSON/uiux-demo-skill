# Theme Asset Isolation

## Purpose

Prevent every UI/UX portfolio deck from looking like the same project with different titles. Each project theme must get its own visual asset pool.

## Hard Rule

Do not reuse images, generated props, backgrounds, mascots, posters, UI mockups, or decorative objects from one theme in another theme unless the user explicitly says the projects belong to the same brand/system.

The local screenshots originally used to author this skill are not runtime dependencies. The installed skill should use distilled rules, Huashu vendor mechanics, and project-specific generated/user assets. A local folder becomes usable only when the user explicitly provides it as a new input for analysis or update.

## Asset Pool Spec

Before generating images or building pages, define:

```text
project_slug:
project_type:
theme_keywords:
audience:
primary_visual_metaphor:
allowed_assets:
forbidden_assets:
generated_asset_count:
real_assets_required:
placeholder_areas:
```

## Theme Examples

Ecommerce SaaS marketplace:
Allowed assets: shopping terminal, coupon cards, product tags, shopping bags, warm orange commerce props, product-card collage backgrounds.
Forbidden assets: power grids, hotel buildings, sleep moon landscapes, unrelated dashboard maps.

Hotel booking app:
Allowed assets: hotel exterior, room cards, booking calendar, map pin, membership card, blue service gradients.
Forbidden assets: shopping terminal, ecommerce coupon piles, power command center, sleep mascots.

Smart power dashboard:
Allowed assets: map texture, grid floor, glass dashboard panels, electric blue metric cards, energy flow lines.
Forbidden assets: warm shopping props, cute retail mascots, hotel lifestyle photos.

Sleep/wellness app:
Allowed assets: moonlit landscape, soft gradients, circular controls, calm phone pedestal, dreamy atmospheric illustration.
Forbidden assets: ecommerce promotion objects, industrial maps, aggressive dashboard lights.

B-side SaaS admin:
Allowed assets: laptop scene, desktop dashboard shell, component boards, cobalt accents, workflow cards, KPI panels.
Forbidden assets: cute shopping mascots unless the product is commerce-related.

## Workflow

1. Identify project type and theme.
2. Define the asset pool spec.
3. Generate support images directly with the current Codex image tool when available.
4. Generate multiple candidates for hero assets.
5. Select by theme fit, density, lighting, and composition.
6. Place text, UI placeholders, and real screenshots in HTML/PPT rather than inside generated images where possible.
7. Save generated assets under a project-specific folder when creating files.

## Quality Bar

A generated asset fails if:

- It could belong to any project after changing only the title.
- It reuses props from an unrelated theme.
- It looks like a generic AI cover.
- It invents fake UI evidence.
- It prevents later insertion of real screenshots and title text.
