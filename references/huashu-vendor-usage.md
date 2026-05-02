# Huashu Vendor Usage

## Purpose

Use the vendored Huashu Design files as a personal-learning template engine for UI/UX portfolio experiments. These files provide reusable HTML deck infrastructure, device frames, showcases, and export scripts.

## License Boundary

The vendored files come from:

```text
https://github.com/alchaincyf/huashu-design
```

They are under Huashu Design Personal Use License. The local copy is for personal learning and non-commercial experimentation only. Preserve `vendor/huashu-design/LICENSE` and do not present these files as original work.

Do not use the vendored Huashu files for company/team tools, paid client delivery, commercial products, paid templates, or commercial training without permission from the original author.

## Vendored Files

Core assets:

- `vendor/huashu-design/assets/deck_stage.js`: 1920x1080 deck stage, scaling, keyboard navigation, hash navigation, print/export support.
- `vendor/huashu-design/assets/deck_index.html`: index shell for multi-file slide decks.
- `vendor/huashu-design/assets/design_canvas.jsx`: design variation canvas for showing multiple concepts.
- `vendor/huashu-design/assets/ios_frame.jsx`: iPhone frame component.
- `vendor/huashu-design/assets/android_frame.jsx`: Android frame component.
- `vendor/huashu-design/assets/browser_window.jsx`: browser window component.
- `vendor/huashu-design/assets/macos_window.jsx`: macOS window component.
- `vendor/huashu-design/assets/animations.jsx`: animation helpers for video-like outputs.
- `vendor/huashu-design/assets/showcases`: upstream sample HTML/PNG references.

Core scripts:

- `vendor/huashu-design/scripts/export_deck_pdf.mjs`: export deck to PDF.
- `vendor/huashu-design/scripts/export_deck_pptx.mjs`: export deck to PPTX.
- `vendor/huashu-design/scripts/export_deck_stage_pdf.mjs`: export deck-stage output to PDF.
- `vendor/huashu-design/scripts/html2pptx.js`: HTML to PPTX conversion helper.
- `vendor/huashu-design/scripts/render-video.js`: render HTML animation to video.
- `vendor/huashu-design/scripts/verify.py`: output verification helper.

## How To Use For UI/UX Portfolio Work

Use Huashu infrastructure for the shell and export path, then apply this skill's UI/UX portfolio logic:

```text
Huashu deck stage / frames / export scripts
+ uiux-portfolio-deck page logic
+ distilled UI/UX portfolio rules from this skill
+ project-specific user assets or generated support visuals
```

Do not use Huashu showcases as the final visual target for UI/UX portfolio work. Use them to understand component mechanics and deck rendering behavior.

## Recommended Production Path

1. Build storyboard using `portfolio-logic.md` and `page-patterns.md`.
2. Run `guided-style-selection.md` when the style is not locked.
3. For decks with 5+ pages, create 2 showcase pages using `showcase-first-deck-workflow.md`.
4. Decide which pages need real screenshots, generated support images, or placeholders.
5. Create an HTML deck using Huashu `deck_stage.js` or `deck_index.html` as the stage shell.
6. Use `ios_frame.jsx`, `android_frame.jsx`, `browser_window.jsx`, or `macos_window.jsx` for screenshot framing where useful.
7. Apply our own UI/UX portfolio CSS and page patterns.
8. Export with Huashu scripts only after visual QA.
9. Run `quality-review.md` checks before delivery.

## No-Screenshot Use

If the user has no screenshots:

- Use Huashu deck stage for layout.
- Use `theme-asset-isolation.md` to define a fresh asset pool for the project theme.
- Use `image-generation-protocol.md` to directly generate project-specific cover/background/support visuals when the current Codex image tool is available.
- Use clear placeholder UI cards for real app screens.
- Mark screenshot gaps explicitly.
- Avoid generating fake product UI as portfolio evidence.

## Better-Than-Upstream Strategy

To outperform generic design generation, specialize instead of copying:

- Use Huashu for mechanics.
- Use local UI/UX portfolio references for style.
- Use this skill for case-study logic.
- Use image2 only for support visuals.
- Build custom UIUX showcases over time.

The long-term target is to create native `assets/uiux-showcases` and `assets/uiux-deck-template` so Huashu becomes a learning scaffold rather than the final dependency.
