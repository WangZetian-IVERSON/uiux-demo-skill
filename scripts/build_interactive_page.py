"""Build a single self-contained HTML viewer for an image-as-page.

Two modes:
  - default (hotspots): inlines OCR hotspots JSON, overlays invisible clickable hotspots on
    big horizontal title text in the image. Read-only.
  - editable: takes a blank-zone rect (from find_blank_zone.py) + a content JSON
    (title/desc/KPI/role) and renders editable HTML text positioned inside the detected
    blank zone. Hover top-left hotzone or press E to toggle edit mode; Ctrl+S exports a
    clean self-contained HTML with edit state stripped. Auto-saves to localStorage.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TEMPLATE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8" />
<title>__TITLE__ · 可交互演示</title>
<style>
  :root { color-scheme: dark; }
  html, body {
    margin: 0; padding: 0; height: 100%; background: #05070d;
    font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
    overflow: hidden;
  }
  #viewport {
    position: fixed; inset: 0;
    display: flex; align-items: center; justify-content: center;
  }
  #stage {
    position: relative;
    width: __W__px; height: __H__px;
    transform-origin: center center;
    flex-shrink: 0;
  }
  #stage > img {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    display: block; user-select: none; pointer-events: none;
  }
  .hot {
    position: absolute;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    text-decoration: none; color: transparent;
    transition: background-color .12s ease, border-color .12s ease, box-shadow .12s ease;
    cursor: pointer;
  }
  .hot:hover {
    background: rgba(123, 107, 255, 0.18);
    border-color: rgba(123, 107, 255, 0.85);
    box-shadow: 0 0 0 1px rgba(123, 107, 255, 0.35), 0 6px 24px rgba(59, 91, 255, 0.25);
  }
  .hot::after {
    content: attr(data-text);
    position: absolute; left: 50%; top: 100%;
    transform: translate(-50%, 8px);
    white-space: nowrap; padding: 4px 8px;
    background: rgba(10, 14, 26, 0.92); color: #e7ecff;
    font-size: 12px; border: 1px solid rgba(123, 107, 255, 0.5);
    border-radius: 4px; opacity: 0; pointer-events: none;
    transition: opacity .12s ease;
  }
  .hot:hover::after { opacity: 1; }
  body.debug .hot {
    background: rgba(255, 0, 80, 0.10);
    border-color: rgba(255, 0, 80, 0.55);
  }
  #hud {
    position: fixed; left: 12px; bottom: 12px; z-index: 9;
    color: #aab3d4; font-size: 12px;
    background: rgba(10,14,26,.7); padding: 8px 12px; border-radius: 6px;
    border: 1px solid rgba(123,107,255,.3);
  }
  #hud kbd {
    background: #1a2040; padding: 1px 5px; border-radius: 3px;
    border: 1px solid #3a3f6a; color: #e7ecff;
  }
</style>
</head>
<body>
  <div id="viewport">
    <div id="stage">
      <img id="bg" src="__IMAGE__" alt="" />
    </div>
  </div>
  <div id="hud">悬停大标题试试 · 按 <kbd>D</kbd> 切换 debug 框 · <span id="count">0</span></div>

<script>
const DATA = __DATA__;
const MIN_HEIGHT_PX = 60;
const MIN_ASPECT    = 1.1;

function fitStage() {
  const stage = document.getElementById("stage");
  const w = stage.offsetWidth, h = stage.offsetHeight;
  if (!w || !h) return;
  const s = Math.min(window.innerWidth / w, window.innerHeight / h);
  stage.style.transform = `scale(${s})`;
}
window.addEventListener("resize", fitStage);
window.addEventListener("load", fitStage);
fitStage();

const stage = document.getElementById("stage");
const isBigHorizontal = (h) => {
  const [x1, y1, x2, y2] = h.bbox;
  const w = x2 - x1, hpx = y2 - y1;
  return hpx >= MIN_HEIGHT_PX && (w / Math.max(hpx, 1)) >= MIN_ASPECT;
};
const routeFor = (h) => h.suggested_href || ("#" + encodeURIComponent(h.text.trim()));

let count = 0, skipped = 0;
for (const h of DATA.hotspots) {
  if (!isBigHorizontal(h)) { skipped++; continue; }
  const href = routeFor(h);
  const [x1, y1, x2, y2] = h.bbox;
  const a = document.createElement("a");
  a.className = "hot";
  a.href = href;
  a.style.left   = x1 + "px";
  a.style.top    = y1 + "px";
  a.style.width  = (x2 - x1) + "px";
  a.style.height = (y2 - y1) + "px";
  a.dataset.text = h.text;
  a.dataset.kind = h.kind;
  if (/^(mailto:|tel:|https?:)/.test(href)) { a.target = "_blank"; a.rel = "noopener"; }
  stage.appendChild(a);
  count++;
}
document.getElementById("count").textContent =
  `${count} 个大标题热区（已忽略 ${skipped} 个小字/斜字）`;

window.addEventListener("keydown", (e) => {
  if (e.key === "d" || e.key === "D") document.body.classList.toggle("debug");
});
</script>
</body>
</html>
"""


def build(hotspots_path: Path, out_path: Path, title: str | None = None) -> None:
    data = json.loads(hotspots_path.read_text(encoding="utf-8"))
    image = data["image"]
    w = data["width"]
    h = data["height"]
    html = (
        TEMPLATE
        .replace("__TITLE__", title or Path(image).stem)
        .replace("__W__", str(w))
        .replace("__H__", str(h))
        .replace("__IMAGE__", image)
        .replace("__DATA__", json.dumps(data, ensure_ascii=False))
    )
    out_path.write_text(html, encoding="utf-8")
    print(f"OK  -> {out_path}  ({w}x{h}, {len(data['hotspots'])} hotspots)")


# ============================================================================
# EDITABLE MODE
# ============================================================================
# Pattern borrowed from zarazhangrui/frontend-slides inline editing:
#   - JS-based hover hotzone with 400ms grace timeout (CSS ~ sibling breaks under
#     pointer-events:none on the toggle button).
#   - exportFile() must strip contenteditable + body.edit-active + .active/.show
#     classes before serializing outerHTML, otherwise saved file opens permanently
#     stuck in edit mode.
#   - localStorage key includes image filename so multiple pages don't collide.

EDITABLE_TEMPLATE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8" />
<title>__TITLE__ · 可编辑作品集页</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700;900&family=Noto+Sans+SC:wght@400;500;700;900&family=Cormorant+Garamond:ital,wght@1,500;1,600&display=swap" />
<style>
  :root {
    --bg: __BG_HEX__;
    --ink: __INK_HEX__;
    --accent-start: __ACCENT_START__;
    --accent-end: __ACCENT_END__;
    --secondary: __SECONDARY__;
    --muted: __MUTED__;
    color-scheme: dark;
  }
  html, body {
    margin: 0; padding: 0; height: 100%;
    background: #050709;
    font-family: "Noto Sans SC", -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    overflow: hidden;
  }
  #viewport {
    position: fixed; inset: 0;
    display: flex; align-items: center; justify-content: center;
  }
  #stage {
    position: relative;
    width: __W__px; height: __H__px;
    transform-origin: center center;
    flex-shrink: 0;
    background: var(--bg);
  }
  #stage > img.bg-image {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    display: block; user-select: none; pointer-events: none;
  }

  /* Editable zone — absolute-positioned over the detected blank rectangle */
  #zone {
    position: absolute;
    left: __ZONE_X__px; top: __ZONE_Y__px;
    width: __ZONE_W__px; height: __ZONE_H__px;
    display: flex; flex-direction: column; justify-content: center;
    gap: 28px; padding: 0;
    color: var(--ink);
  }
  .label {
    font-family: "Noto Sans SC", sans-serif;
    font-size: 20px; font-weight: 500;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--muted);
  }
  .title-zh {
    font-family: "Noto Sans SC", "PingFang SC", sans-serif;
    font-weight: 900;
    font-size: clamp(72px, 9vw, 132px);
    line-height: 1.0;
    background: linear-gradient(120deg, var(--accent-start) 0%, var(--accent-end) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin: 0;
  }
  .subtitle-en {
    font-family: "Cormorant Garamond", "Noto Serif SC", serif;
    font-style: italic; font-weight: 600;
    font-size: 56px; line-height: 1.05;
    color: var(--ink);
  }
  .desc {
    font-family: "Noto Sans SC", sans-serif;
    font-size: 22px; line-height: 1.65; font-weight: 400;
    color: var(--ink); opacity: 0.92;
    max-width: 760px;
  }
  .kpi-row {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 18px; max-width: 720px;
  }
  .kpi {
    border: 1px solid color-mix(in srgb, var(--ink) 22%, transparent);
    border-radius: 6px;
    padding: 18px 20px;
    display: flex; flex-direction: column; gap: 4px;
  }
  .kpi-label {
    font-size: 12px; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--muted);
  }
  .kpi-number {
    font-family: "Noto Sans SC", sans-serif;
    font-size: 38px; font-weight: 900;
    background: linear-gradient(120deg, var(--accent-start) 0%, var(--accent-end) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    line-height: 1;
  }
  .kpi-sub {
    font-size: 13px; color: var(--muted);
  }
  .role {
    font-size: 14px; letter-spacing: 0.12em;
    color: var(--muted); text-transform: uppercase;
  }

  /* Edit mode UI — frontend-slides pattern */
  .edit-hotzone {
    position: fixed; top: 0; left: 0;
    width: 80px; height: 80px; z-index: 10000; cursor: pointer;
  }
  .edit-toggle {
    position: fixed; top: 16px; left: 16px; z-index: 10001;
    width: 44px; height: 44px; border-radius: 50%;
    background: rgba(20, 26, 54, 0.95); color: #e7ecff;
    border: 1px solid rgba(123, 107, 255, 0.6);
    font-size: 20px; cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    opacity: 0; pointer-events: none;
    transition: opacity 0.3s ease, transform 0.2s ease;
  }
  .edit-toggle:hover { transform: scale(1.08); }
  .edit-toggle.show, .edit-toggle.active {
    opacity: 1; pointer-events: auto;
  }
  .edit-toggle.active {
    background: linear-gradient(135deg, #3B5BFF, #7B6BFF);
    border-color: #38E1FF;
  }
  .edit-banner {
    position: fixed; top: 16px; left: 50%; transform: translateX(-50%);
    z-index: 10001; padding: 8px 16px;
    background: rgba(20, 26, 54, 0.95); color: #e7ecff;
    border: 1px solid rgba(123, 107, 255, 0.6);
    border-radius: 999px; font-size: 13px;
    opacity: 0; pointer-events: none;
    transition: opacity 0.25s ease;
  }
  .edit-banner.active { opacity: 1; }
  .edit-banner kbd {
    background: #1a2040; padding: 1px 6px; border-radius: 3px;
    border: 1px solid #3a3f6a; font-size: 11px; margin: 0 4px;
  }
  body.edit-active [data-editable] {
    outline: 1px dashed rgba(123, 107, 255, 0.6);
    outline-offset: 6px;
    transition: outline-color 0.2s ease;
  }
  body.edit-active [data-editable]:hover {
    outline-color: rgba(123, 107, 255, 1);
  }
  body.edit-active [data-editable]:focus {
    outline: 2px solid #38E1FF;
    outline-offset: 6px;
  }
</style>
</head>
<body>
  <div id="viewport">
    <div id="stage">
      <img class="bg-image" src="__IMAGE__" alt="" />
      <div id="zone">
        <div class="label" data-editable data-key="label">__LABEL__</div>
        <h1 class="title-zh" data-editable data-key="title_zh">__TITLE_ZH__</h1>
        <div class="subtitle-en" data-editable data-key="subtitle_en">__SUBTITLE_EN__</div>
        <div class="desc" data-editable data-key="desc">__DESC__</div>
        <div class="kpi-row">__KPIS__</div>
        <div class="role" data-editable data-key="role">__ROLE__</div>
      </div>
    </div>
  </div>

  <div class="edit-hotzone" id="editHotzone" title="编辑模式入口"></div>
  <button class="edit-toggle" id="editToggle" title="切换编辑模式 (E)">✏️</button>
  <div class="edit-banner" id="editBanner">编辑模式 · 点击文字直接改 · <kbd>Ctrl+S</kbd> 导出 · <kbd>E</kbd> 退出</div>

<script>
const STORAGE_KEY = "uiux-editable::" + "__IMAGE__";

function fitStage() {
  const stage = document.getElementById("stage");
  const w = stage.offsetWidth, h = stage.offsetHeight;
  if (!w || !h) return;
  const s = Math.min(window.innerWidth / w, window.innerHeight / h);
  stage.style.transform = `scale(${s})`;
}
window.addEventListener("resize", fitStage);
window.addEventListener("load", fitStage);
fitStage();

// Restore saved edits
try {
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
  document.querySelectorAll("[data-editable]").forEach(el => {
    const k = el.dataset.key;
    if (k && saved[k] !== undefined) el.innerHTML = saved[k];
  });
} catch (e) { /* ignore */ }

const editor = {
  isActive: false,
  toggle() {
    this.isActive = !this.isActive;
    document.body.classList.toggle("edit-active", this.isActive);
    document.querySelectorAll("[data-editable]").forEach(el => {
      if (this.isActive) el.setAttribute("contenteditable", "true");
      else el.removeAttribute("contenteditable");
    });
    document.getElementById("editToggle").classList.toggle("active", this.isActive);
    document.getElementById("editBanner").classList.toggle("active", this.isActive);
    if (this.isActive) {
      const first = document.querySelector("[data-editable]");
      if (first) first.focus();
    } else {
      this.save();
    }
  },
  save() {
    const data = {};
    document.querySelectorAll("[data-editable]").forEach(el => {
      data[el.dataset.key] = el.innerHTML;
    });
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); } catch (e) {}
  },
  exportFile() {
    // CRITICAL: strip edit state before capturing outerHTML so the saved file
    // doesn't open permanently stuck in edit mode (frontend-slides footgun).
    const editableEls = Array.from(document.querySelectorAll('[contenteditable]'));
    editableEls.forEach(el => el.removeAttribute('contenteditable'));
    document.body.classList.remove('edit-active');
    const editToggle = document.getElementById('editToggle');
    const editBanner = document.getElementById('editBanner');
    editToggle?.classList.remove('active', 'show');
    editBanner?.classList.remove('active', 'show');

    const html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

    // Restore so user can keep editing the open tab.
    document.body.classList.add('edit-active');
    editableEls.forEach(el => el.setAttribute('contenteditable', 'true'));
    editToggle?.classList.add('active');
    editBanner?.classList.add('active');

    const blob = new Blob([html], { type: 'text/html' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '__OUT_BASENAME__.edited.html';
    a.click();
    URL.revokeObjectURL(a.href);
  }
};

// Hover hotzone with 400ms grace (JS-based; CSS ~ sibling breaks).
const hotzone = document.getElementById("editHotzone");
const editToggle = document.getElementById("editToggle");
let hideTimeout = null;
hotzone.addEventListener("mouseenter", () => {
  clearTimeout(hideTimeout);
  editToggle.classList.add("show");
});
hotzone.addEventListener("mouseleave", () => {
  hideTimeout = setTimeout(() => {
    if (!editor.isActive) editToggle.classList.remove("show");
  }, 400);
});
editToggle.addEventListener("mouseenter", () => clearTimeout(hideTimeout));
editToggle.addEventListener("mouseleave", () => {
  hideTimeout = setTimeout(() => {
    if (!editor.isActive) editToggle.classList.remove("show");
  }, 400);
});
hotzone.addEventListener("click", () => editor.toggle());
editToggle.addEventListener("click", () => editor.toggle());

// E key toggle (skip when typing into editable text); Ctrl+S export.
document.addEventListener("keydown", (e) => {
  if ((e.key === "e" || e.key === "E") && !e.target.getAttribute("contenteditable")) {
    e.preventDefault();
    editor.toggle();
    return;
  }
  if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S")) {
    e.preventDefault();
    editor.save();
    editor.exportFile();
  }
});

// Auto-save on every input.
document.querySelectorAll("[data-editable]").forEach(el => {
  el.addEventListener("input", () => editor.save());
});
</script>
</body>
</html>
"""


def build_editable(image: Path, zone_json: Path, content_json: Path,
                   out_path: Path, title: str | None = None) -> None:
    zone = json.loads(zone_json.read_text(encoding="utf-8"))
    content = json.loads(content_json.read_text(encoding="utf-8"))
    palette = content.get("palette", {})
    z = zone["zone"]

    kpis_html_parts = []
    for k in content.get("kpis", []):
        kpis_html_parts.append(
            f'<div class="kpi" data-editable data-key="kpi_{k["key"]}_label_num">'
            f'<div class="kpi-label">{k["label"]}</div>'
            f'<div class="kpi-number">{k["number"]}</div>'
            f'<div class="kpi-sub">{k["sub"]}</div>'
            f'</div>'
        )
    kpis_html = "".join(kpis_html_parts)

    out_basename = out_path.stem.replace(".", "_")
    # Image src must be relative to the HTML file location, not the cwd.
    try:
        image_rel_path = Path(image).resolve().relative_to(out_path.resolve().parent)
        image_rel = str(image_rel_path).replace("\\", "/")
    except ValueError:
        # Different drive / not under HTML's parent → fall back to absolute file URI.
        image_rel = Path(image).resolve().as_uri()

    html = (
        EDITABLE_TEMPLATE
        .replace("__TITLE__", title or image.stem)
        .replace("__W__", str(zone["image_w"]))
        .replace("__H__", str(zone["image_h"]))
        .replace("__IMAGE__", image_rel)
        .replace("__BG_HEX__", zone.get("bg_hex", "#0A0E1A"))
        .replace("__INK_HEX__", palette.get("ink", "#F5F6FA"))
        .replace("__ACCENT_START__", palette.get("accent_start", "#3B5BFF"))
        .replace("__ACCENT_END__", palette.get("accent_end", "#7B6BFF"))
        .replace("__SECONDARY__", palette.get("secondary", "#38E1FF"))
        .replace("__MUTED__", palette.get("muted", "#8A93B8"))
        .replace("__ZONE_X__", str(z["x"]))
        .replace("__ZONE_Y__", str(z["y"]))
        .replace("__ZONE_W__", str(z["w"]))
        .replace("__ZONE_H__", str(z["h"]))
        .replace("__LABEL__", content.get("label", ""))
        .replace("__TITLE_ZH__", content.get("title_zh", ""))
        .replace("__SUBTITLE_EN__", content.get("subtitle_en", ""))
        .replace("__DESC__", content.get("desc", ""))
        .replace("__KPIS__", kpis_html)
        .replace("__ROLE__", content.get("role", ""))
        .replace("__OUT_BASENAME__", out_basename)
    )
    out_path.write_text(html, encoding="utf-8")
    print(f"OK editable -> {out_path}  zone={z['x']},{z['y']} {z['w']}x{z['h']}")


# ============ multi-zone mode (Layout-Fitter pipeline) ============

MULTI_ZONE_TEMPLATE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8" />
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500;1,700&family=Inter:wght@400;600;700&family=Noto+Sans+SC:wght@400;700;900&family=Noto+Serif+SC:wght@600;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: __BG__;
    --ink: __INK__;
    --muted: __MUTED__;
    --acc1: __ACC1__;
    --acc2: __ACC2__;
  }
  html, body { margin: 0; padding: 0; height: 100%; background: #0b0d12; overflow: hidden;
    font-family: "Noto Sans SC", "PingFang SC", -apple-system, sans-serif; }
  #viewport { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; }
  #stage { position: relative; width: __W__px; height: __H__px; flex-shrink: 0;
           background: var(--bg); }
  #stage > img { position: absolute; inset: 0; width: 100%; height: 100%; display: block;
                 user-select: none; pointer-events: none; }
  .ov { position: absolute; box-sizing: border-box; padding: 8px 12px;
        display: flex; flex-direction: column; gap: 6px; justify-content: center;
        overflow: hidden; }
  .ov.role-title-block { gap: 14px; }
  .ov.role-kpi-tile { gap: 4px; justify-content: center; }
  .ov .f { line-height: 1.2; }
  .grad { background: linear-gradient(120deg, var(--acc1) 0%, var(--acc2) 100%);
          -webkit-background-clip: text; background-clip: text; color: transparent; }
  body.debug .ov { outline: 1px dashed rgba(255,0,80,.6);
                   background: rgba(255,0,80,.06); }
  #hud { position: fixed; left: 12px; bottom: 12px; z-index: 9;
         color: #aab3d4; font-size: 12px;
         background: rgba(10,14,26,.7); padding: 6px 10px; border-radius: 6px;
         border: 1px solid rgba(123,107,255,.3); }
  #hud kbd { background: #1a2040; padding: 1px 5px; border-radius: 3px; }
</style>
</head>
<body>
<div id="viewport"><div id="stage">
  <img src="__IMAGE__" alt="">
__OVERLAYS__
</div></div>
<div id="hud"><kbd>D</kbd> debug · <kbd>R</kbd> reset zoom</div>
<script>
  const stage = document.getElementById('stage');
  function fit() {
    const W = __W__, H = __H__;
    const sx = window.innerWidth / W, sy = window.innerHeight / H;
    const s = Math.min(sx, sy) * 0.96;
    stage.style.transform = `scale(${s})`;
    stage.style.transformOrigin = 'center center';
  }
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('keydown', e => {
    if (e.key === 'd' || e.key === 'D') document.body.classList.toggle('debug');
    if (e.key === 'r' || e.key === 'R') fit();
  });
</script>
</body></html>
"""


def _font_stack(font_key: str, deck_fonts: dict) -> str:
    # NOTE: must use single quotes around family names — these strings are
    # emitted into HTML inline style attributes (style="..."), and double
    # quotes inside would terminate the attribute and silently break
    # font-size / line-height / etc.
    fallbacks = {
        "cjk_display": "'Noto Serif SC', 'PingFang SC', 'Microsoft YaHei', serif",
        "cjk_body":    "'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif",
        "en_display":  "'Cormorant Garamond', 'Noto Serif SC', serif",
        "en_body":     "'Inter', 'Noto Sans SC', sans-serif",
    }
    if font_key in deck_fonts:
        return f"'{deck_fonts[font_key]}', {fallbacks.get(font_key, 'sans-serif')}"
    return fallbacks.get(font_key, "sans-serif")


def _resolve_color(color: str, palette: dict) -> str:
    """gradient(...) → CSS gradient text trick is applied via class; here return plain CSS color
    or sentinel for gradient handling."""
    if color.startswith("gradient("):
        return "__GRAD__"
    return color


def _render_field(f: dict, deck_fonts: dict, palette: dict) -> str:
    color_val = _resolve_color(f.get("color", palette["ink"]), palette)
    is_grad = color_val == "__GRAD__"
    style_parts = [
        f'font-family: {_font_stack(f["font"], deck_fonts)}',
        f'font-size: {f["size_pt"]}pt',
    ]
    if "line_height" in f:
        style_parts.append(f'line-height: {f["line_height"]}')
    if f.get("italic"):
        style_parts.append("font-style: italic")
    if "letter_spacing" in f:
        style_parts.append(f'letter-spacing: {f["letter_spacing"]}')
    if "align" in f:
        style_parts.append(f'text-align: {f["align"]}')
    if not is_grad:
        style_parts.append(f'color: {color_val}')
    if f["font"] == "cjk_display":
        style_parts.append("font-weight: 900")
    elif f["font"] == "en_display":
        style_parts.append("font-weight: 700")
    cls = "f grad" if is_grad else "f"
    text = (f["text"]
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f'<div class="{cls}" style="{"; ".join(style_parts)}">{text}</div>'


import math

# Per-role flex gap (matches CSS in MULTI_ZONE_TEMPLATE).
_ROLE_GAP = {"title-block": 14, "kpi-tile": 4, "desc-block": 6, "role-chip": 6}
# Padding inside .ov (CSS: padding: 8px 12px).
_OV_PAD_X = 24
_OV_PAD_Y = 16
# CSS pt -> px ratio.
_PT2PX = 4.0 / 3.0


def _est_field_height(f: dict, avail_w_px: float) -> float:
    """Estimate rendered height in CSS px for one field at its current size_pt.
    Uses simple per-glyph width heuristic: CJK ≈ 1em, latin ≈ 0.55em."""
    size_px = f["size_pt"] * _PT2PX
    text = f.get("text", "")
    is_latin_font = f.get("font", "").startswith("en_")
    glyph_w = size_px * (0.55 if is_latin_font else 1.0)
    char_count = max(1, len(text))
    text_w = char_count * glyph_w
    lines = max(1, math.ceil(text_w / max(1.0, avail_w_px)))
    line_h = size_px * float(f.get("line_height", 1.2))
    return lines * line_h


def _autoshrink_overlay(ov: dict) -> None:
    """Mutate ov['fields'][*]['size_pt'] so that the overlay's rendered content
    fits inside the zone (avail_w x avail_h after padding). Iteratively scales
    all field sizes by the same factor until total height fits or min size hit.
    Idempotent: small overlays already fitting are left alone.
    """
    avail_w = max(1.0, ov["w"] - _OV_PAD_X)
    avail_h = max(1.0, ov["h"] - _OV_PAD_Y)
    gap = _ROLE_GAP.get(ov["role"], 6)
    fields = ov["fields"]
    if not fields:
        return
    MIN_PT = 9.0
    for _ in range(8):
        total_h = sum(_est_field_height(f, avail_w) for f in fields) \
                  + gap * (len(fields) - 1)
        if total_h <= avail_h:
            return
        scale = avail_h / total_h
        # Clamp scale so we don't go below MIN_PT for the largest field.
        max_pt = max(f["size_pt"] for f in fields)
        if max_pt * scale < MIN_PT:
            scale = MIN_PT / max_pt
        # If no progress can be made, bail.
        if scale >= 0.999:
            return
        for f in fields:
            new_pt = max(MIN_PT, f["size_pt"] * scale)
            # round to whole pt, but keep >=MIN_PT
            f["size_pt"] = max(MIN_PT, round(new_pt))


def build_multi_zone(image_path: Path, layout_path: Path, out_path: Path, title: str | None) -> None:
    layout = json.loads(layout_path.read_text(encoding="utf-8"))
    palette = layout["deck_palette"]
    deck_fonts = layout.get("deck_fonts", {})

    overlay_html_parts = []
    for ov in layout["overlays"]:
        _autoshrink_overlay(ov)
        style = (
            f'left: {ov["x"]}px; top: {ov["y"]}px; '
            f'width: {ov["w"]}px; height: {ov["h"]}px;'
        )
        fields_html = "\n".join(_render_field(f, deck_fonts, palette) for f in ov["fields"])
        overlay_html_parts.append(
            f'<div class="ov role-{ov["role"]}" style="{style}">\n{fields_html}\n</div>'
        )

    # Image src is relative to the HTML output file's directory.
    img_rel = Path(image_path).name if Path(image_path).parent == out_path.parent else str(image_path).replace("\\", "/")

    html = (
        MULTI_ZONE_TEMPLATE
        .replace("__TITLE__", title or out_path.stem)
        .replace("__W__", str(layout["image_w"]))
        .replace("__H__", str(layout["image_h"]))
        .replace("__BG__", palette["bg"])
        .replace("__INK__", palette["ink"])
        .replace("__MUTED__", palette["muted"])
        .replace("__ACC1__", palette["accent_start"])
        .replace("__ACC2__", palette["accent_end"])
        .replace("__IMAGE__", img_rel)
        .replace("__OVERLAYS__", "\n".join(overlay_html_parts))
    )
    out_path.write_text(html, encoding="utf-8")
    unplaced = layout.get("unplaced", [])
    extra = f"  WARN unplaced={unplaced}" if unplaced else ""
    print(f"OK multi-zone -> {out_path}  overlays={len(layout['overlays'])}{extra}")


# ---------------------------------------------------------------------------
# annotated-callouts mode
# ---------------------------------------------------------------------------

ANNOTATED_TEMPLATE = """<!doctype html>
<html lang="zh">
<head>
<meta charset="utf-8" />
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500;1,700&family=Inter:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;700;900&family=Noto+Serif+SC:wght@600;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: __BG__;
    --ink: __INK__;
    --muted: __MUTED__;
    --acc1: __ACC1__;
    --acc2: __ACC2__;
  }
  html, body { margin: 0; padding: 0; height: 100%; background: var(--bg); overflow: hidden;
    font-family: "Noto Sans SC", "PingFang SC", -apple-system, sans-serif; color: var(--ink); }
  #viewport { position: fixed; inset: 0; display: flex; align-items: center; justify-content: center; }
  #stage { position: relative; width: __SW__px; height: __SH__px; flex-shrink: 0;
           background: var(--bg); }
  #stage > img.hero { position: absolute; left: __IMG_X__px; top: __IMG_Y__px;
                      width: __IW__px; height: __IH__px; display: block;
                      user-select: none; pointer-events: none;
                      box-shadow: 0 24px 60px rgba(0,0,0,.18), 0 2px 6px rgba(0,0,0,.06); }
  svg.lines { position: absolute; left: 0; top: 0; width: __SW__px; height: __SH__px;
              pointer-events: none; }
  svg.lines line { stroke: var(--ink); stroke-width: 1.2; stroke-linecap: round;
                   opacity: 0.62; }
  .anchor-dot { position: absolute; width: 14px; height: 14px; border-radius: 50%;
                background: var(--acc1); border: 2px solid var(--ink);
                transform: translate(-50%, -50%); box-shadow: 0 0 0 4px rgba(255,228,17,.20); }
  .callout { position: absolute; width: 360px; padding: 18px 20px 20px;
             background: rgba(255,255,255,0.96); border: 1px solid rgba(27,27,27,0.10);
             border-radius: 4px; box-shadow: 0 12px 30px rgba(0,0,0,.06);
             box-sizing: border-box; }
  .callout .num { display: inline-block; font-family: 'Cormorant Garamond', serif;
                  font-style: italic; font-size: 14pt; color: var(--ink);
                  border-bottom: 2px solid var(--acc1); padding: 0 4px 1px;
                  margin-bottom: 10px; letter-spacing: 0.04em; }
  .callout .head { font-family: 'Noto Sans SC', sans-serif; font-weight: 700;
                   font-size: 14pt; line-height: 1.35; color: var(--ink);
                   margin: 0 0 8px; letter-spacing: 0.01em; }
  .callout .body { font-family: 'Noto Sans SC', sans-serif; font-weight: 400;
                   font-size: 11pt; line-height: 1.65; color: var(--muted); margin: 0; }
  .page-head { position: absolute; left: __IMG_X__px; top: 30px; width: __IW__px;
               display: flex; align-items: baseline; gap: 18px; }
  .page-head .pn { font-family: 'Cormorant Garamond', serif; font-style: italic;
                   font-size: 18pt; color: var(--ink); border-bottom: 2px solid var(--acc1);
                   padding: 0 6px 2px; }
  .page-head .pt { font-family: 'Noto Sans SC', sans-serif; font-weight: 700;
                   font-size: 16pt; color: var(--ink); }
  .page-head .ps { font-family: 'Cormorant Garamond', serif; font-style: italic;
                   font-size: 13pt; color: var(--muted); margin-left: auto; }
  .page-foot { position: absolute; left: __IMG_X__px; bottom: 22px; width: __IW__px;
               font-family: 'Inter', sans-serif; font-size: 10pt; color: var(--muted);
               letter-spacing: 0.18em; text-transform: uppercase; }
  body.debug .anchor-dot { box-shadow: 0 0 0 8px rgba(255,0,80,.35); }
  #hud { position: fixed; left: 12px; bottom: 12px; z-index: 9; color: var(--muted);
         font-size: 11px; background: rgba(255,255,255,.7); padding: 6px 10px;
         border-radius: 4px; border: 1px solid rgba(27,27,27,.08); }
  #hud kbd { background: var(--acc1); padding: 1px 5px; border-radius: 3px; color: var(--ink); }
</style>
</head>
<body>
<div id="viewport"><div id="stage">
  <img class="hero" src="__IMAGE__" alt="">
  <svg class="lines" viewBox="0 0 __SW__ __SH__">__LINES__</svg>
__DOTS__
__CALLOUTS__
__HEAD__
__FOOT__
</div></div>
<div id="hud"><kbd>D</kbd> debug · <kbd>R</kbd> reset zoom</div>
<script>
  const stage = document.getElementById('stage');
  function fit() {
    const W = __SW__, H = __SH__;
    const sx = window.innerWidth / W, sy = window.innerHeight / H;
    const s = Math.min(sx, sy) * 0.96;
    stage.style.transform = `scale(${s})`;
    stage.style.transformOrigin = 'center center';
  }
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('keydown', e => {
    if (e.key === 'd' || e.key === 'D') document.body.classList.toggle('debug');
    if (e.key === 'r' || e.key === 'R') fit();
  });
</script>
</body></html>
"""


def build_annotated(image_path: Path, ann_path: Path, out_path: Path, title: str | None) -> None:
    ann = json.loads(ann_path.read_text(encoding="utf-8"))
    iw = int(ann["image_w"])
    ih = int(ann["image_h"])
    palette = ann.get("deck_palette", {
        "bg": "#FAFAF7", "ink": "#1B1B1B", "muted": "#6B6B6B",
        "accent_start": "#FFE411", "accent_end": "#FFC400",
    })
    gutter = int(ann.get("gutter", 420))
    card_w = int(ann.get("card_w", 360))
    card_pad_outer = (gutter - card_w) // 2  # margin between image edge and card
    img_x = gutter
    img_y = int(ann.get("img_y_offset", 80))
    sw = iw + 2 * gutter
    sh = ih + img_y + int(ann.get("foot_h", 80))

    callouts = ann.get("callouts", [])

    line_svg_parts = []
    dot_html_parts = []
    card_html_parts = []
    for i, c in enumerate(callouts, start=1):
        ax, ay = c["anchor"]
        # anchor pixel in stage coords
        sx = img_x + int(ax)
        sy = img_y + int(ay)
        side = c.get("side", "right")
        card_y = img_y + int(c.get("card_y", ay - 60))
        if side == "left":
            card_x = card_pad_outer
            card_anchor_x = card_x + card_w  # right edge of card
        else:
            card_x = img_x + iw + card_pad_outer
            card_anchor_x = card_x  # left edge of card
        # Line endpoints: from anchor dot to card edge at card_y + ~30 (top band area)
        line_end_y = card_y + 30
        line_svg_parts.append(
            f'<line x1="{sx}" y1="{sy}" x2="{card_anchor_x}" y2="{line_end_y}" />'
        )
        dot_html_parts.append(
            f'<div class="anchor-dot" style="left:{sx}px;top:{sy}px;"></div>'
        )
        head = c.get("headline", "").strip()
        body = c.get("detail", "").strip().replace("\n", "<br>")
        num = c.get("num") or f"{i:02d}"
        card_html_parts.append(
            f'<div class="callout" style="left:{card_x}px;top:{card_y}px;width:{card_w}px;">'
            f'<span class="num">{num}</span>'
            f'<div class="head">{head}</div>'
            f'<p class="body">{body}</p>'
            f'</div>'
        )

    page_num = ann.get("page_num", "")
    page_title = ann.get("page_title", title or "")
    page_subtitle = ann.get("page_subtitle", "")
    head_html = ""
    if page_num or page_title or page_subtitle:
        head_html = (
            '<div class="page-head">'
            + (f'<span class="pn">{page_num}</span>' if page_num else "")
            + (f'<span class="pt">{page_title}</span>' if page_title else "")
            + (f'<span class="ps">{page_subtitle}</span>' if page_subtitle else "")
            + '</div>'
        )
    footer = ann.get("footer", "")
    foot_html = f'<div class="page-foot">{footer}</div>' if footer else ""

    img_rel = Path(image_path).name if Path(image_path).parent == out_path.parent else str(image_path).replace("\\", "/")

    html = (
        ANNOTATED_TEMPLATE
        .replace("__TITLE__", title or out_path.stem)
        .replace("__SW__", str(sw))
        .replace("__SH__", str(sh))
        .replace("__IW__", str(iw))
        .replace("__IH__", str(ih))
        .replace("__IMG_X__", str(img_x))
        .replace("__IMG_Y__", str(img_y))
        .replace("__BG__", palette["bg"])
        .replace("__INK__", palette["ink"])
        .replace("__MUTED__", palette["muted"])
        .replace("__ACC1__", palette["accent_start"])
        .replace("__ACC2__", palette["accent_end"])
        .replace("__IMAGE__", img_rel)
        .replace("__LINES__", "\n".join(line_svg_parts))
        .replace("__DOTS__", "\n".join(dot_html_parts))
        .replace("__CALLOUTS__", "\n".join(card_html_parts))
        .replace("__HEAD__", head_html)
        .replace("__FOOT__", foot_html)
    )
    out_path.write_text(html, encoding="utf-8")
    print(f"OK annotated -> {out_path}  callouts={len(callouts)}  stage={sw}x{sh}")



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["hotspots", "editable", "multi-zone", "annotated-callouts"], default="hotspots")
    ap.add_argument("--hotspots", help="(hotspots mode) OCR hotspots JSON path")
    ap.add_argument("--image", help="(editable/multi-zone/annotated mode) image path")
    ap.add_argument("--zone-json", help="(editable mode) blank zone JSON from find_blank_zone.py")
    ap.add_argument("--content-json", help="(editable mode) editorial content JSON")
    ap.add_argument("--layout", help="(multi-zone mode) layout.json from layout_fitter.py")
    ap.add_argument("--annotations", help="(annotated-callouts mode) annotations.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    if a.mode == "hotspots":
        if not a.hotspots:
            ap.error("--hotspots is required for mode=hotspots")
        build(Path(a.hotspots), Path(a.out), a.title)
    elif a.mode == "editable":
        for req in ("image", "zone_json", "content_json"):
            if not getattr(a, req):
                ap.error(f"--{req.replace('_', '-')} is required for mode=editable")
        build_editable(Path(a.image), Path(a.zone_json), Path(a.content_json),
                       Path(a.out), a.title)
    elif a.mode == "annotated-callouts":
        for req in ("image", "annotations"):
            if not getattr(a, req):
                ap.error(f"--{req.replace('_', '-')} is required for mode=annotated-callouts")
        build_annotated(Path(a.image), Path(a.annotations), Path(a.out), a.title)
    else:  # multi-zone
        for req in ("image", "layout"):
            if not getattr(a, req):
                ap.error(f"--{req.replace('_', '-')} is required for mode=multi-zone")
        build_multi_zone(Path(a.image), Path(a.layout), Path(a.out), a.title)

