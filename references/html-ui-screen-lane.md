# HTML UI Screen Lane

## Status: DEPRECATED as of 2026-05 (kept as fallback only)

`gpt-image-2` (verified 2026-05) renders Chinese / CJK UI labels cleanly and on-brief. The image-first deck workflow is now the default for CJK concept UI screens. Generate them inside the page background image per `references/image-first-deck-workflow.md` + `references/image-generation-protocol.md` "Image-First Deck: Page Image Recipe".

This lane is kept for two narrow fallback cases only:

1. The available image model in the current session is NOT gpt-image-2 / Nano Banana Pro / Gemini 3 Pro Image, AND a quick capability test confirms the model garbles CJK labels.
2. The user explicitly asks for hand-built HTML UI (e.g. for a live interactive prototype, not a deck page).

For all other cases, route CJK concept UI screens to `IMAGE_MODEL` lane.

---

## Original Rationale (historical, kept for context)

Older image generation models (Imagen 4 / 4 Ultra / Nano Banana Flash / Nano Banana Pro / Gemini 3 Pro Image — verified 2026-04) **universally failed at concept mobile or web UI screens whose text is non-Latin** (Chinese / Japanese / Korean / Arabic / Cyrillic / Thai / Hindi). The failures observed:

- Chinese characters became nonexistent glyph composites ("今日精选" → "令目精送" / "象居" / "购兜中")
- The model regressed to memorized training-set images: iPhone home screen with fake English app names ("Souge / Sesp / Tamps / Apalke"), a fashion model standing in front of seamless paper, a developer DevTools panel with placeholder URLs
- Negative prompts, aspect ratio, model upgrades (Flash → Pro → Ultra) did not fix it
- Latin-only UI screens (English, Spanish, German) worked tolerably; CJK did not

`gpt-image-2` (2026-05) resolves this. Use it.

## When To Use This Lane (fallback only)

Route a page to `HTML_UI_SCREEN` only when ALL of the following are true:

1. The page shows a concept mobile screen, web app screen, or web page
2. The interface text is CJK or other non-Latin
3. There is no real shipped product screenshot for this screen (otherwise route to `REAL_SCREENSHOT`)
4. The page is intended to read as "look at this UI design", not "look at this atmospheric scene with a phone in it"
5. **The session's available image model is verified to garble CJK labels** (run a 1-image capability test on a sample CJK button before committing to this lane)

If gpt-image-2 or equivalent is available, route to `IMAGE_MODEL` instead.

## Build Pattern

The deck page already provides a device frame (phone shell with notch, browser chrome, etc.). Replace the inner `.image-slot` placeholder div with a fully styled `.ui` container hand-coded to match the PADB.

### Required structure

```html
<div class="phone-shell">
  <div class="notch"></div>
  <div class="ui {screen-name}">
    <div class="status">9:41 + signal/wifi/battery</div>
    <div class="nav">left icon · title · right icon</div>
    <div class="scroll">{actual screen content}</div>
    <div class="tabbar">5 bottom tabs (if app has one)</div>
  </div>
</div>
```

### Required style anchors (must match PADB)

- Font stack: `-apple-system, BlinkMacSystemFont, "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif`
- Background: pure white `#fff` (or PADB.surface)
- Primary CTA color: PADB.primary_accent
- Border radius scheme: 10px cards / 14-22px buttons / 38px inner shell
- All text in real domain-realistic Chinese (per `image-generation-protocol.md` Sample Copy Convention) — NEVER lorem-ipsum / "商品 1" / "示例文案"

### Required content discipline

Every UI screen must include:

- A real-feeling product / data / user identity (e.g. "羊毛针织开衫 · 米杏色 ¥488", "汪先生 · 138 8888 0000 · 北京市朝阳区建国路 89 号")
- The exact UX claim from the deck's `screen-cap` paragraph below it (e.g. if the caption says "加入购物车吸底", the screen MUST show a sticky bottom button — visual must match the verbal claim)
- A working visual hierarchy: status bar → nav → primary content → CTA. Not a flat block of text and chips.

## Anti-Patterns

DO NOT do any of the following — they all look like AI-slop UI:

- Empty grey rectangles labeled "图片" or "icon"
- Emoji used as hero product image at >40px in the actual screen body (small thumbnails OK)
- Lorem ipsum / "商品 1 / 商品 2" / repetitive placeholder rows
- Outlined dashed boxes left visible inside the device frame
- A single giant chip / single button taking up half the screen with nothing else

## Composition Pairing

The HTML UI screen pairs with the deck page's caption block (typically labelled `screen-cap` or equivalent):

```
[ PHONE SHELL with handcoded UI ]
SCREEN A · HOME
首页 · 少而准
从 8 个金刚位收到 5 个,每个入口都对应一个明确的决策路径,不再做"运营展示墙"。
```

The screen and the caption are one argument. The screen MUST visibly demonstrate what the caption claims. If the caption says "5 金刚位", count them in the screen. If the caption says "最优组合自动勾选", show the highlighted card.

## Verification Checklist

Before declaring an `HTML_UI_SCREEN` page done:

- [ ] All Chinese text renders correctly in the deck's preview browser
- [ ] Product / user / data sample copy is domain-realistic, not placeholder
- [ ] PADB primary accent color appears on the CTA / highlighted state
- [ ] Status bar + nav + content + (tab bar | sticky bar) all present
- [ ] No dashed border / `image-slot` styling left visible
- [ ] Screen visually demonstrates every claim in its caption
