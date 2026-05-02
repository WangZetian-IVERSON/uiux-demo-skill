# Editable Image-As-Page Variant

Borrowed pattern from `zarazhangrui/frontend-slides` (16k★) inline-editing mode + adapted for our IMAGE_AS_PAGE pipeline. Use this variant when the user wants to **edit titles / descriptions / KPI numbers in the browser after generation** — for example, reusing one template across multiple job applications and only swapping company names + metrics.

## When To Use This Variant Instead Of Plain IMAGE_AS_PAGE

Ask the user once during the OPENING CHECKLIST:

> "成品交付后，你需要在浏览器里直接改标题/描述/数据吗？(Y) 改 → 选 EDITABLE 变体（左字版区是 HTML 文字，可编辑、可导出新 HTML）；(N) 只看/只导 PDF → 选标准 IMAGE_AS_PAGE（杂志级排版，文字烫死在图里更好看）"

| Use plain IMAGE_AS_PAGE | Use IMAGE_AS_PAGE_EDITABLE |
|---|---|
| One-shot deliverable (作品集 PDF / 路演) | Template the user will reuse with different copy |
| Visual ceiling matters most | User must edit titles in browser without re-running image-gen |
| User won't touch HTML | User wants to swap company name / KPI numbers / dates per-deck |
| Print / PDF export is end format | Live web link is end format (Vercel etc.) |

## The Architecture Conflict (the bug the user spotted)

```
[BAD]  image has 「悟」+「Lumen」 baked in pixels
        + HTML overlay also renders 「悟」+「Lumen」 on top
       → user sees DOUBLE text, image-text bleeds around the HTML edges
```

**Root cause:** `gpt-image-2-2k` produces editorial typography by drawing text DIRECTLY into the image. That's exactly why the lumen 2K demo looks magazine-grade. But once text is rasterized into pixels, it cannot be edited without re-generating the image. If you put HTML text on top, the underlying pixels still show.

**Two solutions, pick one per deck (cannot have both):**

### Solution A — Plain IMAGE_AS_PAGE (current default)

- Image carries ALL text (left big title + right in-frame UI + corners).
- HTML overlay is **invisible clickable hotspots only** (PaddleOCR → bbox → transparent `<a>`).
- Editable: ❌ Visual ceiling: ✅✅
- This is what `references/image-as-page-prompt-recipe.md` produces today.

### Solution B — IMAGE_AS_PAGE_EDITABLE (this file)

- Image **explicitly leaves the left typography zone as a solid BG_HEX block** — no characters, no logo, no label.
- Right mockup keeps its in-frame UI text (sidebar nav / canvas content / popovers — those are "product screenshot" content, not meant to be edited per-deck).
- HTML overlay renders the editable big title / English subtitle / 3 description lines / 3 KPI tiles in the left zone using web fonts.
- Visual ceiling: ✅ (left zone is HTML typography, slightly less editorial than baked-pixel but very close with good fonts).
- Editable: ✅✅ (any text in left zone + corners is `contenteditable` in edit mode).

## Two Methods For Reserving The Editable Zone

### Method A — Pre-Reserved Zone (rigid, simpler HTML)

Tell the prompt up-front "left 45% is solid <BG_HEX>". HTML overlay always positions text at fixed coords (0..922px × full height). Pros: deterministic. Cons: every page has the same composition.

### Method B — Inferred Blank Zone (recommended, more flexible) ★

**Don't tell the prompt about the editorial text at all.** Only ask the model to draw:
- the device mockup (with its in-frame UI text preserved — that's "screenshot content", not edit-target)
- top-right wordmark + bottom-right copyright (or omit corners too if those should also be editable)
- background color + texture

Then run `scripts/find_blank_zone.py` on the generated image: it samples corner pixels to learn `BG_HEX`, builds a binary mask of "is-this-pixel-within-±8-of-BG_HEX", and finds the **largest axis-aligned rectangle of pure background**. That rectangle's bbox is passed to `build_interactive_page.py --editable-zone x,y,w,h` which positions all HTML title/desc/KPI inside it.

Pros:
- Model picks composition (mockup left vs right vs centered) → variety across pages.
- Shorter prompt → less likely to hit 2K HTTP 524 timeout.
- Zero risk of underlying-text bleed (the model was never asked to draw any editorial text).
- Same architecture as user's mental model: "image carries the *device*, HTML carries the *editorial*".

Cons:
- HTML font size + line layout must adapt to detected zone aspect ratio. Use `clamp()` and `auto`-fit grid for KPI tiles.
- Occasionally the model leaves a too-small blank → script reports "no zone ≥ 600×800 found" and we re-roll the image.

**Default to Method B for IMAGE_AS_PAGE_EDITABLE.** Method A is the fallback when Method B fails twice in a row (e.g. the model insists on filling the whole canvas).

## Modified Prompt — Left Typography Zone

### For Method B (recommended) — DELETE the editorial text from the prompt

Take the master template from `references/image-as-page-prompt-recipe.md` and **simply OMIT the entire `LEFT TYPOGRAPHY ZONE` slot**. Do not mention title, subtitle, description, KPI tiles, role chip, or any horizontal editorial text. Tell the model only about:

- background color + texture
- the device mockup with its in-frame UI fully described (sidebar / canvas / popover / command bar — all the in-screen text the model SHOULD draw, because it's product screenshot content)
- top-right wordmark + bottom-right copyright (optional — omit if those should also be HTML-editable)
- the existing CRITICAL + NEGATIVE blocks

Add ONE extra negative line at the bottom of the prompt:

```text
NEGATIVE additions for editable variant:
- Do NOT draw any large title text, subtitle, paragraph, KPI number, statistic card, or chip outside the device frame.
- Leave at least 45% of the canvas as flat <BG_HEX> with the device mockup occupying the rest.
- Background area outside the device must be perfectly flat <BG_HEX> — no decorative text, no logo, no scattered UI elements, no floating cards.
```

After generation, run `scripts/find_blank_zone.py` to detect where the model actually left blank, then HTML overlay fills that detected rectangle.

### For Method A (fallback) — pre-reserve the left zone

Take the master template from `references/image-as-page-prompt-recipe.md` and replace the entire `LEFT TYPOGRAPHY ZONE` slot with this single instruction:

```text
LEFT TYPOGRAPHY ZONE (45% width):
- COMPLETELY EMPTY. Fill this entire 45% column with solid <BG_HEX> color.
- Do NOT draw any text, label, logo, chip, KPI card, or decorative element here.
- Do NOT add a subtle gradient, dot grid, or noise here either — perfectly flat <BG_HEX>.
- Treat this as a reserved zone that will be filled by HTML later. Pixel-perfect blank.
```

Everything else (right mockup, top-right wordmark, bottom-right copyright, palette, density limits) stays identical. The right mockup's in-frame UI text remains fully drawn by the model.

> **Why "perfectly flat"**: any gradient / texture in the left zone bleeds visible color through the HTML text background, especially around CJK strokes. The flat solid color makes it indistinguishable whether the title is HTML or image.

> **Why corners can stay in image**: top-right "PORTFOLIO" wordmark + bottom-right copyright rarely change per-deck. If the user wants those editable too, also remove them from the prompt and add to HTML overlay.

## HTML Overlay — Editable Mode

Generate the page with `scripts/build_interactive_page.py` BUT with `--mode editable`. This adds:

1. **Foreground typography in the left zone**: real HTML `<h1>` / `<p>` / `<div class="kpi">` positioned at the same coordinates the recipe specifies, using web fonts (Source Han Sans / PingFang / GT Super, loaded from CDN).
2. **Inline-edit machinery (borrowed from frontend-slides)**:
   - Hidden 80×80px hotzone in top-left corner
   - Hover 400ms → ✏️ button appears
   - Click ✏️ or press `E` → toggle `body.edit-active`, set `contenteditable="true"` on every `[data-editable]` element, dashed outline appears
   - Ctrl+S → export new HTML file (with edit-state stripped, see footgun below)
   - All edits auto-save to `localStorage` keyed by image filename, so refresh doesn't lose work

### exportFile() footgun (DO NOT skip)

When the user presses Ctrl+S, `document.documentElement.outerHTML` captures the LIVE DOM — including `body.edit-active`, `contenteditable="true"` on every text element, and `.active` / `.show` classes on the toggle button. If you don't strip those before serialization, **anyone opening the saved file sees dashed outlines and a checkmark button as if permanently stuck in edit mode**.

```javascript
exportFile() {
    // Strip edit state so the saved file opens cleanly
    const editableEls = Array.from(document.querySelectorAll('[contenteditable]'));
    editableEls.forEach(el => el.removeAttribute('contenteditable'));
    document.body.classList.remove('edit-active');
    const editToggle = document.getElementById('editToggle');
    const editBanner = document.querySelector('.edit-banner');
    editToggle?.classList.remove('active', 'show');
    editBanner?.classList.remove('active', 'show');

    const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;

    // Restore edit state so the user can keep editing the open tab
    document.body.classList.add('edit-active');
    editableEls.forEach(el => el.setAttribute('contenteditable', 'true'));
    editToggle?.classList.add('active');
    editBanner?.classList.add('active');

    const blob = new Blob([html], { type: 'text/html' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'page.edited.html';
    a.click();
    URL.revokeObjectURL(a.href);
}
```

### Hover hotzone footgun

Do NOT use the CSS `~` sibling selector for hover-show of the edit button. With `pointer-events: none` on the toggle button, the user's mouse leaves the hotzone before reaching the button → button disappears before clickable. Use **JS-based hover with 400ms grace timeout** as in `frontend-slides/html-template.md`.

## Coordinate Mapping (image → HTML)

The recipe's master template specifies the left zone occupies 45% width × full height. For 2048×1152:
- Zone left edge: `0px`
- Zone right edge: `~922px`
- Zone padding: 80px on all sides → content box `80,80 → 842,1072`
- Title baseline (96pt CJK): around `y=350`
- Description block: `y=550 → y=720`
- KPI tile row: `y=820 → y=940` (3 tiles, each 180×120, 24px gap)
- Role chip line: `y=1000`

`build_interactive_page.py --mode editable` should accept a `--zone left-45` argument and emit absolute-positioned editable elements at these coordinates, scaled with the same `transform:scale()` as the rest of the viewport.

## Self-Check

- [ ] Image left zone is **perfectly flat <BG_HEX>** — no text, no gradient, no noise (eyedrop-test 5 pixels).
- [ ] HTML overlay big title is in correct font (Source Han Sans Heavy / PingFang Semibold etc.) at the recipe-specified pt size.
- [ ] Pressing `E` toggles edit mode; clicking title makes it editable; typing changes it.
- [ ] Ctrl+S downloads `page.edited.html` and opening that file shows no dashed outlines / no edit button.
- [ ] localStorage key includes image filename so two pages don't collide.
- [ ] Right mockup in-frame UI text is unchanged (it's product content, not edit-target).

## When NOT To Use This Variant

- The deck is a one-shot: extra editable plumbing is dead weight.
- The user prefers PDF as final delivery: PDF screenshot doesn't preserve edit state anyway.
- The page is a **cover** with hand-drawn typography effect (variable stroke, gradient-fills-glyph, masked photography inside character) — those effects only work as image pixels. Cover pages should stay plain IMAGE_AS_PAGE.
