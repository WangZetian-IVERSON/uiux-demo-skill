"""Find the largest axis-aligned rectangle of (near-)background-color pixels in an image.

Used by the IMAGE_AS_PAGE_EDITABLE pipeline (Method B): the prompt tells gpt-image-2 NOT
to draw any horizontal editorial text and to leave most of the canvas as flat BG color.
This script then locates the blank rectangle so that build_interactive_page.py can place
HTML title/desc/KPI elements precisely inside it.

Algorithm:
    1. Sample the four corners of the image to learn BG_HEX (modal pixel).
    2. Build a binary mask: pixel is "blank" iff |R-bg.r|+|G-bg.g|+|B-bg.b| <= tolerance*3.
    3. Optional erosion (1-2 px) to ignore device shadow halos.
    4. Find the maximum-area all-1 axis-aligned rectangle via histogram + monotonic stack.
    5. Emit JSON {bg_hex, image_w, image_h, zone:{x,y,w,h}, zone_norm:{x,y,w,h}}.

Run:
    python scripts/find_blank_zone.py --image path/to/page.png \
        --out path/to/page.zone.json [--tolerance 14] [--min-w 600] [--min-h 800]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image


def sample_bg_hex(arr: np.ndarray) -> tuple[int, int, int]:
    """Pick the BG color from the LIGHTEST corner patch.

    Earlier versions used the modal color across all 4 corners, but that broke on images
    with a vignette: the dark vignette dominates the corners while the actual open canvas
    region is lighter. Using the lightest corner's modal color recovers the true open-area
    background.
    """
    h, w = arr.shape[:2]
    patch = 24
    corners = [
        arr[0:patch, 0:patch],
        arr[0:patch, w - patch:w],
        arr[h - patch:h, 0:patch],
        arr[h - patch:h, w - patch:w],
    ]
    # Pick the brightest corner by mean luminance.
    def luma(c: np.ndarray) -> float:
        m = c.reshape(-1, 3).mean(axis=0)
        return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2]
    brightest = max(corners, key=luma)
    quantized = (brightest.reshape(-1, 3) // 4) * 4
    counts = Counter(map(tuple, quantized.tolist()))
    bg = counts.most_common(1)[0][0]
    return int(bg[0]), int(bg[1]), int(bg[2])


def build_mask(arr: np.ndarray, bg: tuple[int, int, int], tolerance: int) -> np.ndarray:
    diff = np.abs(arr.astype(np.int16) - np.array(bg, dtype=np.int16))
    return (diff.sum(axis=2) <= tolerance * 3).astype(np.uint8)


def erode(mask: np.ndarray, iters: int = 1) -> np.ndarray:
    if iters <= 0:
        return mask
    out = mask
    for _ in range(iters):
        shifted = (
            out[1:-1, 1:-1]
            & out[0:-2, 1:-1]
            & out[2:, 1:-1]
            & out[1:-1, 0:-2]
            & out[1:-1, 2:]
        )
        new = np.zeros_like(out)
        new[1:-1, 1:-1] = shifted
        out = new
    return out


def max_rect_in_histogram(heights: np.ndarray) -> tuple[int, int, int]:
    """Return (max_area, left_index_in_row, width)."""
    stack: list[int] = []
    best = (0, 0, 0)
    n = len(heights)
    i = 0
    while i <= n:
        cur = heights[i] if i < n else 0
        if not stack or cur >= heights[stack[-1]]:
            stack.append(i)
            i += 1
            continue
        top = stack.pop()
        left = stack[-1] + 1 if stack else 0
        width = i - left
        area = heights[top] * width
        if area > best[0]:
            best = (int(area), int(left), int(width))
    return best


def largest_rectangle(mask: np.ndarray) -> tuple[int, int, int, int]:
    """Return (x, y, w, h) of the largest axis-aligned all-1 rectangle."""
    rows, cols = mask.shape
    heights = np.zeros(cols, dtype=np.int32)
    best = (0, 0, 0, 0, 0)  # area, x, y, w, h
    for r in range(rows):
        heights = np.where(mask[r] == 1, heights + 1, 0)
        area, x, w = max_rect_in_histogram(heights)
        if area > best[0]:
            h = area // max(w, 1)
            y = r - h + 1
            best = (area, x, y, w, h)
    _, x, y, w, h = best
    return x, y, w, h


def ocr_text_mask(image_path: Path, h: int, w: int, lang: str = "ch", pad: int = 6) -> np.ndarray:
    """Return an HxW uint8 mask: 1 where the image has NO detected text, 0 inside text bboxes.

    Multiplied with the color-blank mask before zone search so detected text is never
    classified as blank — protects against text whose color happens to be near the background.
    """
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        print("WARN: paddleocr not installed; --ocr ignored. "
              "pip install paddleocr paddlepaddle", file=sys.stderr)
        return np.ones((h, w), dtype=np.uint8)
    ocr = PaddleOCR(
        use_textline_orientation=False,
        lang=lang,
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="PP-OCRv5_mobile_rec",
        enable_mkldnn=False,
    )
    res = ocr.predict(str(image_path))
    mask = np.ones((h, w), dtype=np.uint8)
    n_boxes = 0
    for page in res:
        d = page if isinstance(page, dict) else page.json
        polys = d.get("rec_polys") or d.get("dt_polys") or []
        for poly in polys:
            xs = [float(p[0]) for p in poly]
            ys = [float(p[1]) for p in poly]
            x0 = max(0, int(min(xs)) - pad)
            y0 = max(0, int(min(ys)) - pad)
            x1 = min(w, int(max(xs)) + pad)
            y1 = min(h, int(max(ys)) + pad)
            if x1 > x0 and y1 > y0:
                mask[y0:y1, x0:x1] = 0
                n_boxes += 1
    print(f"  ocr: masked {n_boxes} text bboxes", file=sys.stderr)
    return mask


def find_all_zones(
    mask: np.ndarray,
    *,
    max_zones: int,
    min_w: int,
    min_h: int,
    padding: int,
) -> list[tuple[int, int, int, int]]:
    """Iteratively peel off the largest unused all-1 rectangle until no zone meets minimums.

    Returns list of (x, y, w, h) in already-padded coordinates, sorted by area desc.
    """
    work = mask.copy()
    zones: list[tuple[int, int, int, int]] = []
    for _ in range(max_zones):
        x, y, w, h = largest_rectangle(work)
        if w == 0 or h == 0:
            break
        # Pad inward.
        px = x + padding
        py = y + padding
        pw = w - 2 * padding
        ph = h - 2 * padding
        # Zero out the RAW (un-padded) region so subsequent searches don't overlap.
        work[max(0, y):y + h, max(0, x):x + w] = 0
        if pw < min_w or ph < min_h:
            # Too small after padding — stop, since any further zone will also be smaller.
            if not zones:
                # Still record one undersized result so the caller can decide.
                zones.append((max(0, px), max(0, py), max(0, pw), max(0, ph)))
            break
        zones.append((px, py, pw, ph))
    return zones


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--tolerance", type=int, default=36,
                        help="Per-channel mean tolerance from BG color (default 36). Raised "
                             "from 14 to handle warm-vignette and paper-noise backgrounds. "
                             "Lower (e.g. 16) for flat solid-color backgrounds.")
    parser.add_argument("--erode", type=int, default=2,
                        help="Erosion iterations to ignore device shadow halos (default 2).")
    parser.add_argument("--min-w", type=int, default=600,
                        help="Reject zone narrower than this in pixels (default 600).")
    parser.add_argument("--min-h", type=int, default=800,
                        help="Reject zone shorter than this in pixels (default 800).")
    parser.add_argument("--padding", type=int, default=48,
                        help="Inset the detected rect by N px on each side (default 48).")
    parser.add_argument("--multi", action="store_true",
                        help="Emit a sorted list of multiple non-overlapping zones (zones[]) "
                             "instead of a single largest zone. Required by the layout-fitter "
                             "pipeline.")
    parser.add_argument("--max-zones", type=int, default=6,
                        help="Cap on number of zones returned in --multi mode (default 6).")
    parser.add_argument("--multi-min-w", type=int, default=180,
                        help="In --multi mode, secondary zones are accepted down to this width "
                             "(default 180). The primary zone still must satisfy --min-w.")
    parser.add_argument("--multi-min-h", type=int, default=120,
                        help="In --multi mode, secondary zones are accepted down to this height "
                             "(default 120).")
    parser.add_argument("--ocr", action="store_true",
                        help="Run PaddleOCR on the image and exclude detected text bboxes from "
                             "the blank-zone search. Prevents overlay collisions with text that "
                             "image2 already baked into the canvas (header/footer bars, in-screen "
                             "UI labels, tier-card copy, etc.). Requires paddleocr + paddlepaddle.")
    parser.add_argument("--ocr-lang", default="ch",
                        help="PaddleOCR lang code (default ch). en | japan | korean ...")
    parser.add_argument("--ocr-pad", type=int, default=8,
                        help="Pad each OCR bbox by N px on each side before masking (default 8).")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"image not found: {args.image}", file=sys.stderr)
        return 1

    img = Image.open(args.image).convert("RGB")
    arr = np.asarray(img)
    bg = sample_bg_hex(arr)
    mask = build_mask(arr, bg, args.tolerance)
    mask = erode(mask, args.erode)
    bg_hex = "#{:02X}{:02X}{:02X}".format(*bg)
    H, W = arr.shape[:2]

    if args.ocr:
        text_mask = ocr_text_mask(args.image, H, W, lang=args.ocr_lang, pad=args.ocr_pad)
        mask = mask & text_mask

    if args.multi:
        # First zone uses the strict (--min-w, --min-h); subsequent zones use the
        # looser (--multi-min-w, --multi-min-h) so we capture KPI-tile-sized pockets.
        primary = find_all_zones(
            mask,
            max_zones=1,
            min_w=args.min_w,
            min_h=args.min_h,
            padding=args.padding,
        )
        # Re-run the multi peel from the start so the primary zone is included exactly once.
        all_zones = find_all_zones(
            mask,
            max_zones=args.max_zones,
            min_w=args.multi_min_w,
            min_h=args.multi_min_h,
            padding=args.padding,
        )
        if not all_zones:
            print("REJECT: no zone of any size detected.", file=sys.stderr)
            return 2
        # Sort by area desc.
        all_zones.sort(key=lambda z: z[2] * z[3], reverse=True)
        zones_payload = [
            {
                "x": int(x), "y": int(y), "w": int(w), "h": int(h),
                "area": int(w * h),
                "area_ratio": round((w * h) / (W * H), 4),
                "norm": {
                    "x": round(x / W, 4), "y": round(y / H, 4),
                    "w": round(w / W, 4), "h": round(h / H, 4),
                },
            }
            for (x, y, w, h) in all_zones
        ]
        # Determine which zone is the "primary" (the strict-minimum one), if any.
        primary_idx = -1
        if primary:
            px, py, pw, ph = primary[0]
            for i, z in enumerate(zones_payload):
                if z["x"] == px and z["y"] == py and z["w"] == pw and z["h"] == ph:
                    primary_idx = i
                    break
        payload = {
            "image": str(args.image),
            "image_w": W,
            "image_h": H,
            "bg_hex": bg_hex,
            "tolerance": args.tolerance,
            "erode": args.erode,
            "padding": args.padding,
            "mode": "multi",
            "primary_zone_index": primary_idx,
            "zones": zones_payload,
        }
        args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(
            f"OK multi zones={len(zones_payload)} primary_idx={primary_idx} -> {args.out}",
            file=sys.stderr,
        )
        return 0

    # ---- Single-zone (legacy) path ----
    x, y, w, h = largest_rectangle(mask)
    print(f"bg_hex={bg_hex} raw_zone=x={x},y={y},w={w},h={h}", file=sys.stderr)

    px = max(0, x + args.padding)
    py = max(0, y + args.padding)
    pw = max(0, w - 2 * args.padding)
    ph = max(0, h - 2 * args.padding)

    if pw < args.min_w or ph < args.min_h:
        print(
            f"REJECT: detected zone {pw}x{ph} smaller than min {args.min_w}x{args.min_h}. "
            "Re-roll the image with a slimmer prompt or fall back to Method A.",
            file=sys.stderr,
        )
        return 2

    payload = {
        "image": str(args.image),
        "image_w": W,
        "image_h": H,
        "bg_hex": bg_hex,
        "tolerance": args.tolerance,
        "erode": args.erode,
        "padding": args.padding,
        "zone": {"x": int(px), "y": int(py), "w": int(pw), "h": int(ph)},
        "zone_norm": {
            "x": round(px / W, 4),
            "y": round(py / H, 4),
            "w": round(pw / W, 4),
            "h": round(ph / H, 4),
        },
    }
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK zone={px},{py} {pw}x{ph} -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
