# Templates

`deck-skeleton.html` and `styles.css` are the starting files for the **image-first deck workflow** (see `references/image-first-deck-workflow.md`).

## How To Use

1. Copy the contents of this folder into your project's deck folder, e.g. `decks/<project-slug>/`.
2. Adjust the relative path to `vendor/design-assets/assets/deck_stage.js` in `deck-skeleton.html` so it resolves from your deck folder.
3. Generate background images with gpt-image-2 / Nano Banana Pro per the PADB and Layer Map. Save them under `decks/<project-slug>/generated-images/` with predictable names (`01-cover.png`, `02-contents.png`, etc.).
4. Edit each `<section>` in `deck-skeleton.html`:
   - Update `src` of `<img class="bg">` to the matching generated image.
   - Edit text inside `<div class="text-layer">` freely. No image regeneration needed when only text changes.
5. Open `deck-skeleton.html` (renamed to `index.html`) in a browser. Use ←/→/Space/Home/End/Esc to navigate. Use `#slide-N` in the URL to jump.
6. To deploy: drop the deck folder onto Vercel / Netlify / Cloudflare Pages.

## What's Editable Without Regenerating Images

- All text inside `.text-layer` divs.
- All `<a href>` link targets.
- The order of `<section>` elements (page order).
- Adding or removing pages (just add or remove `<section>` blocks).
- CSS in `styles.css` for typography, color, positioning.

## What Requires Regenerating An Image

- Changing the project visual style (palette, mood, props).
- Changing what's inside a phone/laptop frame in the image.
- Changing the page background scenery.
- Moving the reserved text zone to a different part of the page.

When you regenerate, keep using the project's PADB so consistency holds.
