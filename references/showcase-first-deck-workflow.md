# Showcase-First Deck Workflow

## Purpose

Prevent simple, generic PPT output by forcing visual grammar validation before full deck production. For decks with 5+ pages, build 2 showcase pages first, then expand.

This is borrowed from Huashu Design's deck workflow: a full deck should not be produced page 1 to page N before the visual grammar is proven.

## Hard Rule

For any UI/UX portfolio deck with 5 or more pages:

1. Do not immediately build the full deck.
2. Write the Project Art Direction Block (PADB) per `visual-consistency.md` BEFORE generating any image.
3. Pick two visually different page types.
4. Create those two pages as showcases, generating images via the real image model with prompts that begin with the PADB.
5. Run the 5-axis consistency QA from `visual-consistency.md` across the showcase images.
6. Let the user approve or revise the grammar AND consistency.
7. Batch-produce the remaining pages only after grammar AND consistency are locked. Every later prompt = PADB + page-specific instructions.

## Recommended Showcase Pairs

Personal UI/UX portfolio:
Cover + project core UI proof page.

Ecommerce app case study:
Cover + app screenshot collage / core flow page.

B-side SaaS or admin:
Business goal page + dashboard/admin core page.

Dashboard/data visualization:
Section cover + data/dashboard value page.

Component/icon library:
Component library page + icon system page.

Operations visual appendix:
Campaign poster gallery + visual system page.

## Showcase Output Contract

Each showcase must include:

- Page role.
- Core message.
- Visual grammar.
- Asset list.
- Generated images used.
- Placeholder areas.
- HTML/PPT layout notes.
- Risks.

If generating actual images, produce the cover/hero image first, then compose the page.

## Grammar Lock

After showcase pages, define and save (this is the deck-level grammar that complements the project-level PADB):

```text
Deck grammar:
- Canvas:
- Background system:
- Typography:
- Accent colors:
- Grid/margins:
- Screenshot treatment:
- Generated asset style:  ← must reference the PADB; never contradict it
- Data/card treatment:
- Section divider style:
- Footer/header metadata:
```

The remaining pages must reuse this grammar AND the PADB while varying layout density and visual role. If a later page needs a new prop or color not in the PADB, update the PADB first — do not silently introduce it in one prompt.

## Batch Production Rules

After grammar approval:

- Build remaining pages using established tokens.
- Alternate dense reasoning pages with visual proof pages.
- Use project-specific assets only.
- Preserve real UI areas as screenshots/placeholders.
- Keep Chinese text editable in HTML/PPT when possible.

## Anti-Simple-PPT Checklist

Reject or revise if:

- Every page is title + bullets.
- Every page uses the same two-column structure.
- Generated images sit as background wallpaper without page logic.
- There are fewer than three distinct visual page types.
- The deck lacks device frames, screenshot collage, component boards, data cards, or visual proof.
- The deck goes from storyboard to final without any visual showcase.
- **Generated images drift in palette, lighting, material, camera, or props vocabulary across pages.** Run the 5-axis consistency QA before delivery.
