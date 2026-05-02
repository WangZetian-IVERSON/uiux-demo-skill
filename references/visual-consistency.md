# Visual Consistency

The single biggest reason a multi-image portfolio looks "schizophrenic" is that each image was prompted independently. Different palette, different camera, different material, different mascot — even when the project is the same. This file fixes that.

The mechanism is simple: **before generating image #1, write a Project Art Direction Block (PADB). Every subsequent prompt MUST start with the same PADB. After generation, run a 5-axis consistency QA across all images side by side.**

## Step 1 — Write The Project Art Direction Block (PADB)

Do this ONCE per project, BEFORE the first image. Save it at the top of the working notes / deck file so every later prompt can copy-paste from it.

```text
=== PROJECT ART DIRECTION BLOCK (PADB) ===
project_slug:           e.g. fin-saas-2026
project_type:           e.g. B-side financial SaaS dashboard
mode:                   FULL_CASE_STUDY | VISUAL_PROPOSAL | CRITIQUE
style_anchor:           ONE sentence, e.g. "Cinematic dark-tech command center with cobalt accents and frosted glass panels."
palette:
  base:                 e.g. #050a12
  surface:              e.g. #0c1622
  primary_accent:       e.g. #34d6ff (electric cyan)
  secondary_accent:     e.g. #2563eb (cobalt)
  text_on_dark:         #f6fbff
  warm_spark:           e.g. #ffb454 (single ember accent, used sparingly)
  forbidden_colors:     purple gradient, neon pink, generic AI rainbow
material_vocabulary:    frosted glass + brushed dark metal + matte concrete + anti-reflective screen glass
lighting_setup:         key 45° upper-left, cool 5600K, soft fill, hard rim, contact shadow at 25°
camera:                 50mm equivalent, f/2.0, eye-level or slight low-angle 3/4 view
environment:            deep navy spatial environment + perspective grid floor + faint volumetric haze
props_vocabulary:       6-12 items max — e.g. glass dashboard panel, floating chart cards, holographic map texture, single ember spark, cobalt edge glow, dark metal pedestal. Nothing outside this list.
type_in_image:          NONE (titles added later in HTML/PPT). If unavoidable, English only, 1 short label, sans display.
forbidden_props:        warm shopping mascots, hotel buildings, sleep moons, cute characters, emoji icons, sparkles, AI clouds, purple blobs.
device_frames:          MacBook Pro 16 (matte aluminum), iPhone 15 Pro (titanium black) — pick one and stick to it for all device shots.
render_reference:       Octane + Redshift, command-center cinematic product photography
aspect_ratios:          16:9 at 2048x1152 for deck pages; 1:1 at 1536x1536 for isolated 3D props
=== END PADB ===
```

The PADB is the contract. Every later image prompt is `PADB + page-specific instructions`. Nothing else.

## Step 2 — Prompt Construction Rule

Every image prompt for this project MUST follow this template:

```text
[paste the entire PADB block as the first half of the prompt]

--- PAGE-SPECIFIC INSTRUCTIONS ---
page_role:              cover | section cover | 3D prop | concept screen | scene
composition:            explicit pixel/percentage layout, where the title safe zone lives
subject:                what's in the foreground, scale, position, pose
secondary_props:        ONLY items from PADB.props_vocabulary
page-specific notes:    e.g. "this cover sits at deck position 1, tone is overture: sparser, more negative space than later pages"
negative:               re-state PADB.forbidden_colors and PADB.forbidden_props, plus page-specific exclusions
```

**Never write a prompt that contradicts the PADB.** If a page genuinely needs a new prop, update the PADB first, then propagate to all earlier images that should also have it (or accept that earlier ones won't match — re-generate them if it matters).

## Step 3 — Reference-Image Chaining (when the model supports it)

Models like Nano Banana Pro / Gemini 3 Pro Image, GPT Image, and Midjourney `--cref` accept reference images. Use them.

- After generating image #1 (the cover), pass it as a reference image to every subsequent prompt with the instruction "match the lighting, palette, material, and camera of the reference image".
- For 3D props that should belong to the same set, pass the first prop image as reference for all later props.
- For concept UI screens that share the same device frame, pass the first screen as reference for the rest.

If the model does not support reference images, compensate by being more explicit in the PADB (exact hex codes, exact lighting angles, exact material names).

### Reference chains are PER-PROJECT, never cross-project

A deck with multiple project case studies has multiple PADBs (per `theme-asset-isolation.md`). Each project runs its OWN reference-image chain:

- Project A's cover seeds the chain for ALL Project A images only.
- Project B starts a NEW chain from Project B's own cover. Do NOT pass Project A's cover as a reference into any Project B prompt.
- Cross-project reference chaining is the #1 cause of "the whole deck looks like one project" — palette, lighting, and props bleed across cases that are supposed to feel different.

If you genuinely want deck-wide visual unity (typography, frame style, photographic feel), enforce that through the **deck meta-PADB**, not through cross-project reference images.

## Step 4 — Generation Order Matters

Generate in this order so the strongest visual sets the tone for the rest:

```text
1. Cover hero (4 candidates, pick 1)  ← this image becomes the visual reference for everything below
2. One section cover (2 candidates, pick 1)  ← validates the PADB at a different page role
3. Hero 3D prop (3 candidates, pick 1)  ← validates props vocabulary
4. Concept UI screen #1 (in VISUAL_PROPOSAL mode)  ← validates the device frame + UI mockup style
5. STOP. Run the consistency QA below.
6. Only after QA passes, batch-generate the rest of the deck's assets reusing PADB + reference image.
```

This is also the showcase-first workflow's hidden purpose: the 2 showcase pages are **the consistency test for the whole deck**.

## Step 5 — 5-Axis Consistency QA

Place every generated image for the project side by side (literally, in a contact sheet). Score each axis 1–5. Anything below 4 must be regenerated before batch production.

| Axis | What to check |
|---|---|
| **Palette** | Same base, surface, primary accent across all images? Any rogue colors that aren't in the PADB? |
| **Lighting** | Same key direction, same color temperature, same shadow hardness? |
| **Material** | Same material vocabulary? No image suddenly using unrelated materials (e.g. one image uses warm wood while the rest are cool metal)? |
| **Camera & Scale** | Same focal-length feel, same eye level, same depth-of-field treatment? Subjects at coherent scale? |
| **Props & Mood** | Do all images feel like they belong to one coherent universe? Could a viewer believe they were shot in the same studio session? |

If two or more axes fail on any image, regenerate that image (don't try to fix the others). If all images fail the same axis, the PADB is wrong — revise the PADB and regenerate all images.

## Step 6 — Forbidden Inconsistency Patterns

These are the most common drift modes. Catch them in QA.

- **Palette drift**: cover uses cobalt #2563eb, section cover uses generic blue #3b82f6, prop uses teal — looks like 3 different brands.
- **Lighting drift**: cover is rim-lit cinematic, prop is flat studio, scene is overcast natural — feels like a stock-photo collage.
- **Mascot drift**: cover has a cute round 3D character, later page has a different abstract object as the "mascot". Pick one and reuse.
- **Material drift**: half the images use frosted glass, the other half use plastic. Pick one.
- **Device drift**: MacBook in one shot, generic gray laptop in another, Surface in a third. Lock the device model in PADB.
- **Type drift in images**: some images have English labels, others Chinese, others none. Default: NO text in image, all titles in HTML.
- **Background drift**: cover has a grid floor, section cover has a flat gradient, scene has clouds. Lock the environment in PADB.

## Step 7 — When Adding A New Project To The Deck

Each project gets its OWN PADB (per `theme-asset-isolation.md`). But within one deck, the *meta-grammar* — type, layout, callout style, frame style, photographic feel — should still feel like one designer made the whole deck.

Define a deck-level meta-PADB once:

```text
=== DECK META-PADB ===
deck_typography:        Chinese display: 思源黑体 Heavy. Latin display: Geist Mono / Migra. Body: HarmonyOS Sans SC.
callout_style:          thin cyan line + uppercase Latin label + Chinese explanation
frame_style:            iPhone 15 Pro titanium for all phone shots; MacBook Pro 16 matte for all laptop shots
photographic_feel:      cinematic 50mm look with controlled depth of field
section_divider:        solid color page with Roman numeral + Chinese section title
=== END ===
```

Project-level PADBs override the deck meta-PADB only on palette, props, and environment — never on typography, frame style, or photographic feel.

## TL;DR

1. Write PADB once per project.
2. Every prompt = PADB + page-specific instructions.
3. Generate the cover first, use it as reference for the rest.
4. After 4 key images, run 5-axis QA before batching.
5. Update PADB and regenerate, never let prompts contradict it.
