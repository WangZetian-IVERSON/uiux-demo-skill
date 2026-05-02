"""PaddleOCR-based hotspot extractor.

Replaces the LLM-based ocr_hotspots.py. PaddleOCR returns precise pixel bboxes
for text regions in the rendered portfolio image. We classify each text by
simple regex (email / phone / url / wechat) and emit the same hotspots.json
schema consumed by the interactive HTML overlay.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
URL_RE = re.compile(r"\b(?:https?://|www\.)[\w./%#?&=-]+", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s-]{6,18}\d)(?!\d)")
WECHAT_RE = re.compile(r"wechat|微信", re.I)
COPYRIGHT_RE = re.compile(r"©|copyright|cease", re.I)


def classify(text: str) -> tuple[str, str | None]:
    t = text.strip()
    m = EMAIL_RE.search(t)
    if m:
        return "email", f"mailto:{m.group(0)}"
    m = URL_RE.search(t)
    if m:
        u = m.group(0)
        if not u.lower().startswith("http"):
            u = "https://" + u
        return "url", u
    if WECHAT_RE.search(t):
        m = PHONE_RE.search(t)
        return "wechat", None
    m = PHONE_RE.search(t)
    if m and len(re.sub(r"\D", "", m.group(0))) >= 7:
        cleaned = re.sub(r"[\s-]", "", m.group(0))
        return "phone", "tel:" + cleaned
    if COPYRIGHT_RE.search(t):
        return "copyright", None
    if re.fullmatch(r"[A-Z][A-Z0-9 +@.\-]{2,}", t) and len(t) >= 4:
        return "decorative-english", None
    if re.fullmatch(r"[\u4e00-\u9fff·、。·\s]{2,8}", t):
        return "title", None
    return "body", None


def _quad_to_bbox(quad) -> list[int]:
    xs = [p[0] for p in quad]
    ys = [p[1] for p in quad]
    return [int(round(min(xs))), int(round(min(ys))),
            int(round(max(xs))), int(round(max(ys)))]


def extract(image_path: Path, lang: str) -> dict:
    from paddleocr import PaddleOCR
    from PIL import Image

    ocr = PaddleOCR(
        use_textline_orientation=False,
        lang=lang,
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="PP-OCRv5_mobile_rec",
        enable_mkldnn=False,
    )

    im = Image.open(image_path)
    w, h = im.size

    res = ocr.predict(str(image_path))
    # PaddleOCR 3.x returns list of OCRResult dicts. Each has keys 'rec_texts',
    # 'rec_scores', 'rec_polys' (or 'dt_polys').
    hotspots = []
    for page in res:
        d = page if isinstance(page, dict) else page.json
        texts = d.get("rec_texts") or []
        scores = d.get("rec_scores") or []
        polys = d.get("rec_polys") or d.get("dt_polys") or []
        for text, score, poly in zip(texts, scores, polys):
            text = (text or "").strip()
            if not text:
                continue
            quad = [(float(p[0]), float(p[1])) for p in poly]
            bbox = _quad_to_bbox(quad)
            kind, href = classify(text)
            item = {
                "text": text,
                "score": float(score) if score is not None else None,
                "bbox": bbox,
                "bbox_norm": [
                    round(bbox[0] / w * 1000),
                    round(bbox[1] / h * 1000),
                    round(bbox[2] / w * 1000),
                    round(bbox[3] / h * 1000),
                ],
                "kind": kind,
            }
            if href:
                item["suggested_href"] = href
            hotspots.append(item)

    return {
        "image": image_path.name,
        "width": w,
        "height": h,
        "engine": f"paddleocr/{lang}",
        "hotspots": hotspots,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", default="ch", help="ch | en | japan | korean ...")
    a = ap.parse_args()

    image = Path(a.image)
    if not image.exists():
        sys.exit(f"image not found: {image}")

    data = extract(image, a.lang)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK  {len(data['hotspots'])} hotspots  -> {out}")
    for h in data["hotspots"][:12]:
        print(f"    [{h['kind']:>18}] {h['text'][:40]:<40} bbox={h['bbox']}")


if __name__ == "__main__":
    main()
