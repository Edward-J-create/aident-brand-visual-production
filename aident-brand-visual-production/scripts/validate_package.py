#!/usr/bin/env python3
"""Validate aident-brand-visual-production package structure, size-kit, and HTML templates."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
FOLDER_NAME = "aident-brand-visual-production"
EXPECTED_VERSION = "0.3.0"

REQUIRED_FILES = [
    "SKILL.md",
    "LICENSE.md",
    "NOTICE.md",
    "README.md",
    "README.zh.md",
    "agents/openai.yaml",
    "assets/templates/size-kit.yaml",
    "assets/templates/production-return.yaml",
    "assets/templates/shot-list.yaml",
    "assets/templates/storyboard.md",
    "assets/templates/layout-zones.md",
    "assets/templates/html/tokens.css",
    "assets/templates/html/poster-kit.css",
    "assets/templates/poster-specs.json",
    "assets/templates/html/feature-poster.html",
    "assets/templates/html/poster-shot.html",
    "assets/templates/html/poster-stage.html",
    "assets/templates/html/poster-cluster.html",
    "assets/templates/html/poster-grid.html",
    "assets/templates/html/poster-table.html",
    "assets/templates/html/feature-poster-zh.html",
    "assets/templates/html/poster-shot-zh.html",
    "assets/templates/html/poster-stage-zh.html",
    "assets/templates/html/poster-cluster-zh.html",
    "assets/templates/html/poster-grid-zh.html",
    "assets/templates/html/poster-table-zh.html",
    "assets/visual-kit/materials/grain-overlay.svg",
    "assets/visual-kit/backgrounds/bloom-teal-indigo.svg",
    "assets/visual-kit/backgrounds/bloom-pastel.svg",
    "assets/visual-kit/backgrounds/bloom-cyan-violet.svg",
    "assets/visual-kit/backgrounds/bloom-violet-cyan.svg",
    "assets/visual-kit/backgrounds/bloom-light-top.svg",
    "assets/visual-kit/backgrounds/bloom-light-lower.svg",
    "assets/visual-kit/backgrounds/top-glow.svg",
    "assets/visual-kit/backgrounds/top-glow-wide.svg",
    "assets/visual-kit/backgrounds/top-glow-social.svg",
    "assets/visual-kit/backgrounds/mesh-bloom.svg",
    "assets/visual-kit/backgrounds/mesh-bloom-wide.svg",
    "assets/visual-kit/materials/tile-field.svg",
    "assets/visual-kit/materials/tile-field-strip.svg",
    "assets/visual-kit/materials/tile-field-wide.svg",
    "assets/visual-kit/materials/sparkles.svg",
    "assets/templates/html/landscape-kit.css",
    "assets/templates/html/video-frame-kit.css",
    "assets/templates/banner-specs.json",
    "assets/templates/video-frame-specs.json",
    "assets/templates/html/banner.html",
    "assets/templates/html/banner-prompt.html",
    "assets/templates/html/video-cover.html",
    "assets/templates/html/profile-avatar.html",
    "assets/templates/html/x-banner.html",
    "assets/templates/html/youtube-banner.html",
    "assets/templates/html/linkedin-banner.html",
    "assets/templates/html/logo-mark.html",
    "assets/templates/html/logo-lockup.html",
    "assets/templates/html/video-frame-title.html",
    "assets/templates/html/video-frame-logo.html",
    "assets/templates/html/video-frame-caption.html",
    "assets/templates/html/video-frame-ui.html",
    "assets/templates/html/video-frame-stat.html",
    "assets/templates/html/video-frame-chips.html",
    "assets/templates/html/video-frame-label-row.html",
    "assets/templates/html/video-frame-endcard.html",
    "assets/templates/html/video-frame-message.html",
    "assets/templates/html/video-frame-messages.html",
    "assets/templates/html/video-frame-input.html",
    "assets/templates/html/video-frame-steps.html",
    "assets/templates/html/video-frame-subtitle.html",
    "assets/fonts/manifest.json",
    "assets/fonts/fonts.css",
    "assets/fonts/licenses/README.md",
    "assets/fonts/licenses/Outfit-OFL.txt",
    "assets/fonts/licenses/SmileySans-OFL.txt",
    "assets/fonts/licenses/NotoSansSC-OFL.txt",
    "assets/visual-kit/README.md",
    "assets/tokens/tokens.json",
    "assets/visual-brief.schema.yaml",
    "assets/video-brief.schema.yaml",
    "references/pack-handoff.md",
    "references/figma-template-kit.md",
    "references/image-production.md",
    "references/video-production-kit.md",
    "references/quality-gates.md",
    "references/host-compatibility.md",
    "references/scope-and-modes.md",
    "references/editable-slots.md",
    "references/reference-gap-matrix.md",
    "scripts/validate_package.py",
    "scripts/render_html_template.py",
    "examples/image-kit-request.yaml",
    "examples/video-kit-request.yaml",
    "examples/both-from-pack-handoff.yaml",
    "examples/brand-payload.example.yaml",
    "examples/brand-payload.example.json",
]

KNOWN_TEMPLATE_IDS = [
    "tpl-video-cover",
    "tpl-feature-poster",
    "tpl-poster-shot",
    "tpl-poster-stage",
    "tpl-poster-cluster",
    "tpl-poster-grid",
    "tpl-poster-table",
    "tpl-feature-poster-zh",
    "tpl-poster-shot-zh",
    "tpl-poster-stage-zh",
    "tpl-poster-cluster-zh",
    "tpl-poster-grid-zh",
    "tpl-poster-table-zh",
    "tpl-banner",
    "tpl-banner-prompt",
    "tpl-x-banner",
    "tpl-youtube-banner",
    "tpl-linkedin-banner",
    "tpl-profile-avatar",
    "tpl-logo-mark",
    "tpl-logo-lockup",
    "tpl-video-frame-title",
    "tpl-video-frame-logo",
    "tpl-video-frame-caption",
    "tpl-video-frame-ui",
    "tpl-video-frame-stat",
    "tpl-video-frame-chips",
    "tpl-video-frame-label-row",
    "tpl-video-frame-endcard",
    "tpl-video-frame-message",
    "tpl-video-frame-messages",
    "tpl-video-frame-input",
    "tpl-video-frame-steps",
    "tpl-video-frame-subtitle",
]

# Static image templates that MUST have HTML frames (storyboard stays md/yaml)
HTML_REQUIRED = {
    "tpl-feature-poster": "feature-poster.html",
    "tpl-poster-shot": "poster-shot.html",
    "tpl-poster-stage": "poster-stage.html",
    "tpl-poster-cluster": "poster-cluster.html",
    "tpl-poster-grid": "poster-grid.html",
    "tpl-poster-table": "poster-table.html",
    "tpl-feature-poster-zh": "feature-poster-zh.html",
    "tpl-poster-shot-zh": "poster-shot-zh.html",
    "tpl-poster-stage-zh": "poster-stage-zh.html",
    "tpl-poster-cluster-zh": "poster-cluster-zh.html",
    "tpl-poster-grid-zh": "poster-grid-zh.html",
    "tpl-poster-table-zh": "poster-table-zh.html",
    "tpl-banner": "banner.html",
    "tpl-banner-prompt": "banner-prompt.html",
    "tpl-video-cover": "video-cover.html",
    "tpl-profile-avatar": "profile-avatar.html",
    "tpl-x-banner": "x-banner.html",
    "tpl-youtube-banner": "youtube-banner.html",
    "tpl-linkedin-banner": "linkedin-banner.html",
    "tpl-logo-mark": "logo-mark.html",
    "tpl-logo-lockup": "logo-lockup.html",
    "tpl-video-frame-title": "video-frame-title.html",
    "tpl-video-frame-logo": "video-frame-logo.html",
    "tpl-video-frame-caption": "video-frame-caption.html",
    "tpl-video-frame-ui": "video-frame-ui.html",
    "tpl-video-frame-stat": "video-frame-stat.html",
    "tpl-video-frame-chips": "video-frame-chips.html",
    "tpl-video-frame-label-row": "video-frame-label-row.html",
    "tpl-video-frame-endcard": "video-frame-endcard.html",
    "tpl-video-frame-message": "video-frame-message.html",
    "tpl-video-frame-messages": "video-frame-messages.html",
    "tpl-video-frame-input": "video-frame-input.html",
    "tpl-video-frame-steps": "video-frame-steps.html",
    "tpl-video-frame-subtitle": "video-frame-subtitle.html",
}

KNOWN_SIZES = {
    "tpl-video-cover": (1920, 1080),
    "tpl-feature-poster": (1242, 1660),
    "tpl-poster-shot": (1242, 1660),
    "tpl-poster-stage": (1242, 1660),
    "tpl-poster-cluster": (1242, 1660),
    "tpl-poster-grid": (1242, 1660),
    "tpl-poster-table": (1242, 1660),
    "tpl-feature-poster-zh": (1242, 1660),
    "tpl-poster-shot-zh": (1242, 1660),
    "tpl-poster-stage-zh": (1242, 1660),
    "tpl-poster-cluster-zh": (1242, 1660),
    "tpl-poster-grid-zh": (1242, 1660),
    "tpl-poster-table-zh": (1242, 1660),
    "tpl-banner": (1270, 760),
    "tpl-banner-prompt": (1270, 760),
    "tpl-x-banner": (2048, 900),
    "tpl-youtube-banner": (2048, 1152),
    "tpl-linkedin-banner": (2048, 400),
    "tpl-profile-avatar": (400, 400),
    "tpl-logo-mark": (80, 80),
    "tpl-video-frame-title": (1920, 1080),
    "tpl-video-frame-logo": (1920, 1080),
    "tpl-video-frame-caption": (1920, 1080),
    "tpl-video-frame-ui": (1920, 1080),
    "tpl-video-frame-stat": (1920, 1080),
    "tpl-video-frame-chips": (1920, 1080),
    "tpl-video-frame-label-row": (1920, 1080),
    "tpl-video-frame-endcard": (1920, 1080),
    "tpl-video-frame-message": (1920, 1080),
    "tpl-video-frame-messages": (1920, 1080),
    "tpl-video-frame-input": (1920, 1080),
    "tpl-video-frame-steps": (1920, 1080),
    "tpl-video-frame-subtitle": (1920, 1080),
}

REQUIRED_COLOR_ROLES = ["bg", "surface", "text", "accent", "muted"]
REQUIRED_DATA_SLOTS_MIN = ["headline"]  # each marketing HTML should expose at least headline or logo


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def parse_frontmatter(skill_text: str) -> dict[str, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_text, re.DOTALL)
    if not m:
        return {}
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def load_size_kit(path: Path, errors: list[str]) -> dict:
    text = path.read_text(encoding="utf-8")
    if re.search(r"\bTBD\b", text):
        fail("size-kit.yaml still contains TBD placeholders", errors)

    if yaml is not None:
        try:
            data = yaml.safe_load(text)
            if data:
                return data
        except Exception as e:
            fail(f"size-kit.yaml YAML parse error: {e}", errors)

    templates = []
    blocks = re.split(r"(?m)^  - id:\s*", text)
    for block in blocks[1:]:
        lines = block.splitlines()
        tid = lines[0].strip()
        entry: dict = {"id": tid}
        for line in lines[1:]:
            if re.match(r"^  - id:\s*", line):
                break
            m = re.match(r"^\s+(width|height|width_min|width_max):\s*(\d+)\s*$", line)
            if m:
                entry[m.group(1)] = int(m.group(2))
        templates.append(entry)
    if not templates:
        fail("size-kit.yaml: could not parse any templates", errors)
    return {"templates": templates}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if ROOT.name != FOLDER_NAME:
        fail(f"folder name is {ROOT.name!r}, expected {FOLDER_NAME!r}", errors)

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"missing required file: {rel}", errors)

    skill_path = ROOT / "SKILL.md"
    version = None
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        meta = parse_frontmatter(skill_text)
        # name may be only in frontmatter top; also parse nested metadata.version
        name = meta.get("name")
        if name != FOLDER_NAME:
            # frontmatter parser is flat — name should still be there
            fail(f"SKILL.md frontmatter name={name!r}, expected {FOLDER_NAME!r}", errors)
        # version lives under metadata: block — regex scan
        vm = re.search(r"(?m)^\s*version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", skill_text)
        version = vm.group(1) if vm else None
        if version != EXPECTED_VERSION:
            fail(f"SKILL.md metadata.version={version!r}, expected {EXPECTED_VERSION!r}", errors)
        for tid in KNOWN_TEMPLATE_IDS:
            if tid not in skill_text:
                fail(f"SKILL.md missing template id mention: {tid}", errors)
        if re.search(r"TBD\s*[×x]", skill_text):
            fail("SKILL.md still has TBD×TBD size placeholders", errors)
        for needle in (
            "data-slot",
            "render_html_template",
            "Hard-coded brand",
            "assets/templates/html",
        ):
            if needle not in skill_text and needle.lower() not in skill_text.lower():
                # soft: check case-insensitive variants
                if needle.lower() not in skill_text.lower():
                    warnings.append(f"SKILL.md may be missing guidance mentioning {needle!r}")

        # Stronger checks for replaceability language
        if "replaceable" not in skill_text.lower() and "data-slot" not in skill_text:
            fail("SKILL.md missing replaceability / data-slot guidance", errors)
        if "html" not in skill_text.lower():
            fail("SKILL.md missing HTML template guidance", errors)

    kit_path = ROOT / "assets/templates/size-kit.yaml"
    if kit_path.is_file():
        data = load_size_kit(kit_path, errors)
        templates = data.get("templates") or []
        ids = [t.get("id") for t in templates if isinstance(t, dict)]
        for tid in KNOWN_TEMPLATE_IDS:
            if tid not in ids:
                fail(f"size-kit missing template id: {tid}", errors)
        by_id = {t["id"]: t for t in templates if isinstance(t, dict) and "id" in t}
        for tid, (w, h) in KNOWN_SIZES.items():
            t = by_id.get(tid)
            if not t:
                continue
            if t.get("width") != w or t.get("height") != h:
                fail(
                    f"{tid} expected {w}x{h}, got {t.get('width')}x{t.get('height')}",
                    errors,
                )
        lockup = by_id.get("tpl-logo-lockup")
        if lockup:
            if lockup.get("height") != 80:
                fail("tpl-logo-lockup height must be 80", errors)
            if lockup.get("width_min") is None or lockup.get("width_max") is None:
                fail("tpl-logo-lockup must define width_min and width_max", errors)

    # HTML templates + tokens.css
    html_dir = ROOT / "assets/templates/html"
    tokens_css = html_dir / "tokens.css"
    if tokens_css.is_file():
        css = tokens_css.read_text(encoding="utf-8")
        for var in ("--color-bg", "--color-text", "--color-accent", "--font-primary", "--safe-margin-ratio"):
            if var not in css:
                fail(f"tokens.css missing {var}", errors)
    for tid, fname in HTML_REQUIRED.items():
        fpath = html_dir / fname
        if not fpath.is_file():
            fail(f"missing HTML template for {tid}: assets/templates/html/{fname}", errors)
            continue
        html = fpath.read_text(encoding="utf-8")
        if f'data-template-id="{tid}"' not in html:
            fail(f"{fname} missing data-template-id={tid!r}", errors)
        if "data-slot=" not in html:
            fail(f"{fname} has no data-slot markers", errors)
        if "tokens.css" not in html:
            fail(f"{fname} does not link tokens.css", errors)
        # Forbid TBD sizes in HTML
        if re.search(r"\bTBD\b", html):
            fail(f"{fname} contains TBD", errors)
        # Canvas size attributes
        if tid in KNOWN_SIZES:
            w, h = KNOWN_SIZES[tid]
            if f'data-width="{w}"' not in html or f'data-height="{h}"' not in html:
                # logo-lockup may use max hug width
                if tid != "tpl-logo-lockup":
                    fail(f"{fname} data-width/height must be {w}x{h}", errors)

        if "fonts.css" not in html:
            fail(f"{fname} does not link fonts.css", errors)

    # tokens.json color roles + versioned fields
    tokens_path = ROOT / "assets/tokens/tokens.json"
    if tokens_path.is_file():
        try:
            tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"tokens.json invalid JSON: {e}", errors)
            tokens = {}
        roles = ((tokens.get("color") or {}).get("roles")) or {}
        for role in REQUIRED_COLOR_ROLES:
            if role not in roles:
                fail(f"tokens.json color.roles missing {role!r}", errors)
            elif roles[role].get("value") in (None, "", "TBD"):
                fail(f"tokens.json color.roles.{role} value is empty/TBD", errors)
        families = ((tokens.get("typography") or {}).get("fontFamilies")) or {}
        if "primary" not in families:
            fail("tokens.json typography.fontFamilies.primary missing", errors)

    # Licensed font binaries are allowed. A binary without an OFL/license file is not.
    fonts_dir = ROOT / "assets/fonts"
    if fonts_dir.is_dir():
        license_dir = fonts_dir / "licenses"
        license_blob = ""
        if license_dir.is_dir():
            for lic in license_dir.glob("*"):
                if lic.suffix.lower() in {".txt", ".md"} and lic.is_file():
                    license_blob += lic.read_text(encoding="utf-8", errors="replace")
        has_ofl = "SIL OPEN FONT LICENSE" in license_blob or "Open Font License" in license_blob
        binaries = [
            p for p in fonts_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2", ".eot"}
        ]
        if binaries and not has_ofl:
            fail("font binaries exist but no SIL OFL / license text under assets/fonts/licenses/", errors)
        for required in (
            "outfit/Outfit-VariableFont_wght.ttf",
            "smiley-sans/SmileySans-Oblique.ttf.woff2",
            "noto-sans-sc/NotoSansSC-Variable.ttf",
        ):
            if not (fonts_dir / required).is_file():
                fail(f"missing packaged font: assets/fonts/{required}", errors)

    # Forbid TBD anywhere critical in package docs for sizes
    for rel in ("assets/templates/size-kit.yaml", "SKILL.md", "assets/templates/layout-zones.md"):
        p = ROOT / rel
        if p.is_file() and re.search(r"TBD\s*[×x]|width:\s*TBD|height:\s*TBD", p.read_text(encoding="utf-8")):
            fail(f"{rel} still has TBD size placeholders", errors)


    spec_path = ROOT / "assets/templates/poster-specs.json"
    if spec_path.is_file():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        kit_css = (ROOT / "assets/templates/html/poster-kit.css").read_text(encoding="utf-8")
        if "mix-blend-mode: overlay" not in kit_css or "opacity: 0.25" not in kit_css:
            fail("poster grain layer must stay overlay at opacity 0.25", errors)
        # Per-type colours live in each poster HTML and in poster-specs.json, not in
        # the shared kit, so the kit only has to carry the shared geometry.
        if "width: 1242px" not in kit_css or "height: 1660px" not in kit_css:
            fail("poster-kit.css is missing the shared 1242x1660 canvas", errors)
        for poster_type in spec.get("types") or []:
            html_rel = poster_type.get("html")
            html_path = ROOT / html_rel if html_rel else None
            if html_path is None or not html_path.is_file():
                fail(f"poster spec missing html for {poster_type.get('id')}", errors)
                continue
            html_text = html_path.read_text(encoding="utf-8")
            if f'data-poster-type="{poster_type.get("id")}"' not in html_text:
                fail(f"{html_rel} missing data-poster-type", errors)
            panel = poster_type.get("panel")
            if panel and panel not in html_text:
                fail(f"{html_rel} does not declare its panel colour {panel}", errors)
            box = poster_type.get("middleBox") or {}
            for key in ("x", "y", "w", "h"):
                if f"{box.get(key)}px" not in html_text:
                    fail(f"{html_rel} missing middle box {key}={box.get(key)}", errors)
            bloom = poster_type.get("bloom")
            if not bloom:
                continue
            bloom_path = ROOT / bloom["file"]
            if not bloom_path.is_file():
                fail(f"missing bloom asset {bloom['file']}", errors)
                continue
            # The blur now lives inside the asset, and the file is padded so the
            # Gaussian falls off before the viewport edge instead of ending on a
            # straight line. Both have to survive a re-export.
            bloom_text = bloom_path.read_text(encoding="utf-8")
            if "feGaussianBlur" not in bloom_text:
                fail(f"{bloom['file']} lost its feGaussianBlur", errors)
            if 'filterUnits="userSpaceOnUse"' not in bloom_text:
                fail(f"{bloom['file']} filter region must cover the padded viewBox", errors)
            if "Padded by" not in bloom_text:
                fail(f"{bloom['file']} is missing its padding note", errors)

    # Design source URLs and file keys must not ship. This check does not store those keys.
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".html", ".py", ".css"}:
            continue
        if path.name == "validate_package.py" or "licenses" in path.parts:
            continue
        blob = path.read_text(encoding="utf-8", errors="replace")
        if "figma.com/design/" in blob or "file_key:" in blob:
            fail(f"{path.relative_to(ROOT)} still links a private design file", errors)

    print(f"validate_package: root={ROOT}")
    print(f"version_expected={EXPECTED_VERSION} version_found={version}")
    if warnings:
        for w in warnings:
            print(f"  WARN: {w}")
    if errors:
        print(f"FAIL ({len(errors)} error(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    if not errors:
        import subprocess

        check = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_render.py")],
            cwd=ROOT,
        )
        if check.returncode != 0:
            fail("scripts/check_render.py failed", errors)

    if errors:
        print(f"FAIL ({len(errors)} error(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("PASS")
    print("template_ids:")
    for tid in KNOWN_TEMPLATE_IDS:
        print(f"  - {tid}")
    print("html_templates:")
    for tid, fn in HTML_REQUIRED.items():
        print(f"  - {tid} -> assets/templates/html/{fn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
