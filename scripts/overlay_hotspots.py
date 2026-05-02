"""Overlay hotspot bboxes onto the source image to visually verify OCR alignment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def overlay(image: str, hotspots: str, out: str) -> None:
    data = json.loads(Path(hotspots).read_text(encoding="utf-8"))
    items = data["hotspots"]
    im = Image.open(image).convert("RGBA")
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 14)
    except Exception:
        font = ImageFont.load_default()
    for it in items:
        x1, y1, x2, y2 = it["bbox"]
        d.rectangle([x1, y1, x2, y2], outline=(255, 0, 80, 220), width=2)
        d.rectangle([x1, y1, x2, y2], fill=(255, 0, 80, 40))
        label = it["text"][:24]
        d.text((x1 + 3, y1 + 2), label, fill=(255, 255, 255, 255), font=font,
               stroke_width=2, stroke_fill=(0, 0, 0, 255))
    Image.alpha_composite(im, over).save(out)
    print(f"OK  -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--hotspots", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    overlay(a.image, a.hotspots, a.out)
