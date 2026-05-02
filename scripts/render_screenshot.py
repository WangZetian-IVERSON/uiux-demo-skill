"""Render an HTML deck page to PNG via Playwright (headless Chromium).

Usage:
    python scripts/render_screenshot.py --html path/page.html --out path/page-rendered.png \\
        [--w 2048] [--h 1152] [--wait 1200]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def render(html: Path, out: Path, w: int, h: int, wait_ms: int) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    uri = html.resolve().as_uri()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto(uri)
        pg.wait_for_timeout(wait_ms)
        pg.screenshot(path=str(out))
        b.close()
    print(f"OK shot -> {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--w", type=int, default=2048)
    ap.add_argument("--h", type=int, default=1152)
    ap.add_argument("--wait", type=int, default=1200)
    args = ap.parse_args()
    html = Path(args.html)
    if not html.exists():
        sys.exit(f"ERROR: html not found: {html}")
    render(html, Path(args.out), args.w, args.h, args.wait)


if __name__ == "__main__":
    main()
