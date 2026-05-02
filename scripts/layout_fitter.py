"""Layout Fitter — slot candidate_copy fields into discovered zones.

Implements the rule-based agent described in references/layout-fitter.md.
Reads:
    --deck-plan deck-plan.json   (provides deck.palette + deck.fonts)
    --page-id   <id>             (selects pages[].candidate_copy by id)
    --zones     <page>.zones.json (multi-zone scan output)
    --image     <page>.png       (used to sample per-zone bg color for contrast flip)

Writes:
    --out       <page>.layout.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image


# ---------------- helpers ----------------

def luminance(rgb: tuple[int, int, int]) -> float:
    """Relative luminance in [0,1] (sRGB simple approximation)."""
    r, g, b = (c / 255.0 for c in rgb)
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def sample_zone_bg(arr: np.ndarray, z: dict) -> tuple[int, int, int]:
    x, y, w, h = z["x"], z["y"], z["w"], z["h"]
    H, W = arr.shape[:2]
    x0 = max(0, x); y0 = max(0, y)
    x1 = min(W, x + w); y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return (255, 255, 255)
    patch = arr[y0:y1, x0:x1]
    mean = patch.reshape(-1, 3).mean(axis=0)
    return (int(mean[0]), int(mean[1]), int(mean[2]))


def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def round_step(v: float, step: int = 2) -> int:
    return int(round(v / step) * step)


# ---------------- rules ----------------

def fit(
    deck: dict,
    copy: dict,
    zones: list[dict],
    image_arr: np.ndarray,
    image_w: int,
    image_h: int,
) -> dict:
    palette = deck["palette"]
    ink = palette["ink"]
    muted = palette["muted"]
    grad = f'gradient({palette["accent_start"]},{palette["accent_end"]})'

    overlays: list[dict] = []
    consumed_keys: set[str] = set()

    # Rule 7 (defensive pre-filter): drop zones inside header/footer bar bands.
    safe_zones = [
        z for z in zones
        if z["y"] >= image_h * 0.05 and (z["y"] + z["h"]) <= image_h * 0.95
    ]
    safe_zones.sort(key=lambda z: z["w"] * z["h"], reverse=True)

    pool = list(enumerate(safe_zones))  # (original_index_in_safe_zones, zone)

    def pop_largest() -> tuple[int, dict] | None:
        return pool.pop(0) if pool else None

    def pop_smallest_bottom() -> tuple[int, dict] | None:
        candidates = [
            (i, z) for (i, z) in pool
            if (z["y"] + z["h"]) >= image_h * 0.85
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda iz: iz[1]["w"] * iz[1]["h"])
        pick = candidates[0]
        pool.remove(pick)
        return pick

    # Rule 6 helper: compute per-zone color overrides
    def colors_for(z: dict) -> dict:
        bg = sample_zone_bg(image_arr, z)
        if luminance(bg) < 0.45:
            return {"ink": "#FFFFFF", "muted": "rgba(255,255,255,0.7)"}
        return {"ink": ink, "muted": muted}

    # ---- Rule 2: largest zone -> title block ----
    title_zone_entry = pop_largest()
    if title_zone_entry and ("title_zh" in copy or "subtitle_en" in copy or "section_label" in copy):
        _, z = title_zone_entry
        c = colors_for(z)
        # Width-driven sizing: count chars in the longest line of the title and fit ~85% of zone width.
        title_text = copy.get("title_zh", "")
        title_lines = title_text.split() if title_text else [""]
        max_chars = max((len(line) for line in title_lines), default=1) or 1
        # CJK glyph at N pt occupies roughly N px wide.
        width_driven = (z["w"] * 0.85) / max_chars
        # Height-driven cap: leave room for label (top) + subtitle (bottom) + breathing.
        # Reserve ~30% of zone height for non-title fields.
        n_lines = max(1, len(title_lines))
        height_cap = (z["h"] * 0.7) / (n_lines * 1.15)
        title_size = round_step(clamp(min(width_driven, height_cap), 56, 280))
        sub_size = round_step(clamp(title_size * 0.45, 28, 96))
        align = "left" if z["w"] > 700 else "center"
        fields = []
        if copy.get("section_label"):
            fields.append({
                "key": "section_label", "text": copy["section_label"],
                "font": "cjk_body", "size_pt": 13, "color": c["muted"],
                "letter_spacing": "0.18em", "align": align,
            })
            consumed_keys.add("section_label")
        if copy.get("title_zh"):
            fields.append({
                "key": "title_zh", "text": copy["title_zh"],
                "font": "cjk_display", "size_pt": title_size, "color": grad,
                "line_height": 1.05, "align": align,
            })
            consumed_keys.add("title_zh")
        if copy.get("subtitle_en"):
            fields.append({
                "key": "subtitle_en", "text": copy["subtitle_en"],
                "font": "en_display", "size_pt": sub_size, "color": c["ink"],
                "italic": True, "align": align,
            })
            consumed_keys.add("subtitle_en")
        if fields:
            overlays.append({
                "zone_index": title_zone_entry[0],
                "role": "title-block",
                "x": z["x"], "y": z["y"], "w": z["w"], "h": z["h"],
                "fields": fields,
            })
        else:
            pool.insert(0, title_zone_entry)  # nothing placed, return zone

    # ---- Rule 3: second-largest -> desc ----
    if copy.get("desc") and pool:
        idx, z = pool[0]
        if (z["w"] * z["h"]) / (image_w * image_h) >= 0.02:
            pool.pop(0)
            c = colors_for(z)
            # Scale desc with zone width: small zone → 16pt, large zone → up to 32pt.
            desc_size = round_step(clamp(z["w"] * 0.04, 16, 32))
            overlays.append({
                "zone_index": idx,
                "role": "desc-block",
                "x": z["x"], "y": z["y"], "w": z["w"], "h": z["h"],
                "fields": [{
                    "key": "desc", "text": copy["desc"],
                    "font": "cjk_body", "size_pt": desc_size, "color": c["ink"],
                    "line_height": 1.6, "align": "left",
                }],
            })
            consumed_keys.add("desc")

    # ---- Rule 4: KPI tiles, one per zone ----
    kpis = copy.get("kpis") or []
    for k_i, kpi in enumerate(kpis):
        if not pool:
            break
        idx, z = pool.pop(0)
        if z["w"] < 160 or z["h"] < 100:
            break  # too small for any KPI
        c = colors_for(z)
        num_size = round_step(clamp(z["h"] * 0.42, 40, 80))
        fields = []
        if kpi.get("label"):
            fields.append({
                "key": f"kpis[{k_i}].label", "text": kpi["label"],
                "font": "cjk_body", "size_pt": 13, "color": c["muted"],
            })
        if kpi.get("number"):
            fields.append({
                "key": f"kpis[{k_i}].number", "text": kpi["number"],
                "font": "en_display", "size_pt": num_size, "color": grad,
            })
        if z["w"] >= 180 and kpi.get("sub"):
            fields.append({
                "key": f"kpis[{k_i}].sub", "text": kpi["sub"],
                "font": "cjk_body", "size_pt": 12, "color": c["muted"],
            })
        if fields:
            overlays.append({
                "zone_index": idx,
                "role": "kpi-tile",
                "x": z["x"], "y": z["y"], "w": z["w"], "h": z["h"],
                "fields": fields,
            })
            consumed_keys.add(f"kpis[{k_i}]")

    # ---- Rule 5: role chip ----
    if copy.get("role"):
        bottom = pop_smallest_bottom()
        if bottom:
            idx, z = bottom
            c = colors_for(z)
            overlays.append({
                "zone_index": idx,
                "role": "role-chip",
                "x": z["x"], "y": z["y"], "w": z["w"], "h": z["h"],
                "fields": [{
                    "key": "role", "text": copy["role"],
                    "font": "cjk_body", "size_pt": 12, "color": c["muted"],
                    "letter_spacing": "0.1em",
                }],
            })
            consumed_keys.add("role")
        else:
            # Fallback: append onto the title-block as a bottom line.
            for ov in overlays:
                if ov["role"] == "title-block":
                    ov["fields"].append({
                        "key": "role", "text": copy["role"],
                        "font": "cjk_body", "size_pt": 12, "color": muted,
                        "letter_spacing": "0.1em", "align": "left",
                    })
                    consumed_keys.add("role")
                    break

    # ---- compute unplaced ----
    unplaced: list[str] = []
    for k in ("section_label", "title_zh", "subtitle_en", "desc", "role"):
        if k in copy and copy[k] and k not in consumed_keys:
            unplaced.append(k)
    for k_i in range(len(kpis)):
        if f"kpis[{k_i}]" not in consumed_keys:
            unplaced.append(f"kpis[{k_i}]")

    return {"overlays": overlays, "unplaced": unplaced}


# ---------------- CLI ----------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck-plan", required=True, type=Path)
    ap.add_argument("--page-id", required=True)
    ap.add_argument("--zones", required=True, type=Path)
    ap.add_argument("--image", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    plan = json.loads(args.deck_plan.read_text(encoding="utf-8"))
    deck = plan["deck"]
    page = next((p for p in plan["pages"] if p["id"] == args.page_id), None)
    if page is None:
        print(f"page id not found in deck plan: {args.page_id}", file=sys.stderr)
        return 2
    copy = page.get("candidate_copy", {})

    z_payload = json.loads(args.zones.read_text(encoding="utf-8"))
    if z_payload.get("mode") != "multi":
        print("zones JSON is not in --multi mode; re-run find_blank_zone.py with --multi",
              file=sys.stderr)
        return 2
    zones = z_payload["zones"]
    image_w = z_payload["image_w"]
    image_h = z_payload["image_h"]

    arr = np.asarray(Image.open(args.image).convert("RGB"))

    result = fit(deck, copy, zones, arr, image_w, image_h)

    out_payload = {
        "image": str(args.image),
        "image_w": image_w,
        "image_h": image_h,
        "page_id": args.page_id,
        "deck_palette": deck["palette"],
        "deck_fonts": deck.get("fonts", {}),
        "overlays": result["overlays"],
        "unplaced": result["unplaced"],
    }
    args.out.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"OK overlays={len(result['overlays'])} unplaced={result['unplaced']} -> {args.out}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
