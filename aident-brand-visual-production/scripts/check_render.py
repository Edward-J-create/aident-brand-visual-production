#!/usr/bin/env python3
"""Fill poster, banner, and cover from the synthetic payload and check the contract.

The HTML contract must pass: slots receive the payload, shared templates stay
free of that brand, and canvas size matches the size kit.

PNG is inspected when Playwright can export it. A missing PNG is recorded as
blocked. It is never reported as delivered.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "examples" / "brand-payload.example.json"
HTML_DIR = ROOT / "assets" / "templates" / "html"

# Synthetic payload markers that must never be baked into shared templates.
FORBIDDEN_IN_SOURCE = ("#3D8BFF", "Northline", "Ship brand kits")

CASES = (
    {
        "template_id": "tpl-feature-poster",
        "file": "feature-poster.html",
        "headline": "Ship brand kits without the scramble.",
        "subcopy": "Feature poster 1242×1660 — logo, url, title and the middle slot are replaceable.",
        "width": 1242,
        "height": 1660,
        "logo": "logo-lockup.svg",
    },
    {
        "template_id": "tpl-banner",
        "file": "banner.html",
        "headline": "Marketing banner",
        "subcopy": "1270×760 — logo, title and the art band are replaceable.",
        "width": 1270,
        "height": 760,
        "logo": "logo-lockup.svg",
    },
    {
        "template_id": "tpl-video-cover",
        "file": "video-cover.html",
        "headline": "Ship brand kits without the scramble.",
        "subcopy": "Template-owned type. Replaceable slots. Packaged sizes.",
        "width": 1920,
        "height": 1080,
        "logo": "logo-lockup.svg",
    },
)


def load_renderer():
    path = ROOT / "scripts" / "render_html_template.py"
    spec = importlib.util.spec_from_file_location("render_html_template", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def png_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def main() -> int:
    errors: list[str] = []
    renderer = load_renderer()
    payload = renderer.load_payload(PAYLOAD)
    source_hashes = {name: sha256(HTML_DIR / name) for name in {c["file"] for c in CASES}}

    for case in CASES:
        source = HTML_DIR / case["file"]
        text = source.read_text(encoding="utf-8")
        for needle in FORBIDDEN_IN_SOURCE:
            if needle in text:
                errors.append(f"{case['file']} bakes payload marker {needle!r}")

    # Resolve placeholder paths from the skill root.
    import os

    previous = Path.cwd()
    os.chdir(ROOT)
    try:
        with tempfile.TemporaryDirectory(prefix="abvp-check-") as tmp:
            out_root = Path(tmp)
            for case in CASES:
                out_dir = out_root / case["template_id"]
                html_path = renderer.fill_template(case["template_id"], payload, out_dir)
                filled = html_path.read_text(encoding="utf-8")
                if case["headline"] not in filled:
                    errors.append(f"{case['template_id']} missing headline")
                if case["subcopy"] not in filled:
                    errors.append(f"{case['template_id']} missing subcopy")
                if "#3D8BFF" not in filled or 'id="brand-token-overrides"' not in filled:
                    errors.append(f"{case['template_id']} missing payload color override")
                if f'data-width="{case["width"]}"' not in filled or f'data-height="{case["height"]}"' not in filled:
                    errors.append(f"{case['template_id']} canvas size drifted")
                if case["logo"] not in filled:
                    errors.append(f"{case['template_id']} logo slot was not filled")
                if case["template_id"] == "tpl-feature-poster":
                    if "visual-kit/backgrounds/bloom-teal-indigo.svg" not in filled:
                        errors.append("tpl-feature-poster missing packaged bloom")
                    if "visual-kit/materials/grain-overlay.svg" not in filled:
                        errors.append("tpl-feature-poster missing grain material")
                    kit_css = (out_dir / "poster-kit.css").read_text(encoding="utf-8")
                    if "mix-blend-mode: overlay" not in kit_css:
                        errors.append("poster grain blend mode was dropped")
                    if "orb-a" in (HTML_DIR / "feature-poster.html").read_text(encoding="utf-8"):
                        errors.append("feature poster still uses ad-hoc orbs")

                png_path = out_dir / (html_path.stem + ".png")
                ok, message = renderer.try_png_export(
                    html_path, png_path, case["width"], case["height"]
                )
                if not ok or not png_path.is_file():
                    print(f"png {case['template_id']}: blocked — {message}")
                    continue
                size = png_size(png_path)
                if size != (case["width"], case["height"]):
                    errors.append(
                        f"{case['template_id']} png is {size}, expected {case['width']}x{case['height']}"
                    )
                else:
                    print(f"png {case['template_id']}: {case['width']}x{case['height']} inspected")

            probe = {
                "text": {"headline": "Probe", "subcopy": "Probe"},
                "images": {
                    "logo": {"src": "assets/placeholders/logo-lockup.svg", "alt": "Logo"},
                    "ui-screenshot": {"src": "assets/placeholders/logo-lockup.svg", "alt": "wrong"},
                },
            }
            probe_html = renderer.fill_template("tpl-feature-poster", probe, out_root / "probe")
            probe_text = probe_html.read_text(encoding="utf-8")
            if probe_text.count("logo-lockup.svg") != 1:
                errors.append("logo file was placed in the poster UI slot")
            if "Supplied product UI, screenshot, or SVG" not in probe_text:
                errors.append("rejected UI slot did not keep the screenshot well")
    finally:
        os.chdir(previous)

    for name, digest in source_hashes.items():
        if sha256(HTML_DIR / name) != digest:
            errors.append(f"{name} was modified by the render check")

    if errors:
        print(f"check_render FAIL ({len(errors)})")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("check_render PASS")
    print("html: slots filled, payload colors stayed in the override block, shared templates unchanged")
    print("png: inspected files match the size kit; a missing export stays blocked, not delivered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
