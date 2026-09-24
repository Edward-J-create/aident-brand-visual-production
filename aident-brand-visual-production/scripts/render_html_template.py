#!/usr/bin/env python3
"""Fill an HTML marketing template from a brand payload (JSON or YAML).

Emits filled HTML. Optional PNG export via Playwright/Chromium when available
(host-dependent; never hard-required). No paid API dependency.

Usage:
  python scripts/render_html_template.py \\
    --template tpl-feature-poster \\
    --payload examples/brand-payload.example.yaml \\
    --out /tmp/out/feature-poster

  python scripts/render_html_template.py --list-templates
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HTML_DIR = ROOT / "assets" / "templates" / "html"
TOKENS_JSON = ROOT / "assets" / "tokens" / "tokens.json"

TEMPLATE_FILES = {
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

# Alias short names → template ids
ALIASES = {
    "feature-poster": "tpl-feature-poster",
    "poster-shot": "tpl-poster-shot",
    "poster-stage": "tpl-poster-stage",
    "poster-cluster": "tpl-poster-cluster",
    "poster-grid": "tpl-poster-grid",
    "poster-table": "tpl-poster-table",
    "banner": "tpl-banner",
    "banner-prompt": "tpl-banner-prompt",
    "video-cover": "tpl-video-cover",
    "profile-avatar": "tpl-profile-avatar",
    "x-banner": "tpl-x-banner",
    "youtube-banner": "tpl-youtube-banner",
    "linkedin-banner": "tpl-linkedin-banner",
    "logo-mark": "tpl-logo-mark",
    "logo-lockup": "tpl-logo-lockup",
    "video-frame-title": "tpl-video-frame-title",
    "video-frame-logo": "tpl-video-frame-logo",
    "video-frame-caption": "tpl-video-frame-caption",
    "video-frame-ui": "tpl-video-frame-ui",
    "video-frame-stat": "tpl-video-frame-stat",
    "video-frame-chips": "tpl-video-frame-chips",
    "video-frame-label-row": "tpl-video-frame-label-row",
    "video-frame-endcard": "tpl-video-frame-endcard",
    "video-frame-message": "tpl-video-frame-message",
    "video-frame-subtitle": "tpl-video-frame-subtitle",
    # Retired single storyboard frame. Kept so older briefs still resolve.
    "video-frame": "tpl-video-frame-title",
    "tpl-video-frame-16x9": "tpl-video-frame-title",
}

COLOR_CSS = {
    "bg": "--color-bg",
    "surface": "--color-surface",
    "surfaceElevated": "--color-surface-elevated",
    "text": "--color-text",
    "textSecondary": "--color-text-secondary",
    "muted": "--color-muted",
    "accent": "--color-accent",
    "accentSoft": "--color-accent-soft",
    "border": "--color-border",
    # common aliases
    "background": "--color-bg",
    "foreground": "--color-text",
}

FONT_CSS = {
    "primary": "--font-primary",
    "display": "--font-display",
}

TEXT_SLOTS = (
    "headline", "headline-accent", "title-accent", "subcopy", "cta", "disclaimer",
    "title-tag", "url", "kicker", "wordmark", "subtitle",
    "metric-a", "metric-a-label", "metric-b", "metric-b-label",
    "stat-value-a", "stat-label-a", "stat-value-b", "stat-label-b",
    "icon-label-a", "icon-label-b", "icon-label-c", "icon-label-d",
)
IMAGE_SLOTS = (
    "logo", "logo-mark", "logo-lockup", "hero", "ui-screenshot", "product-art",
    "icon", "decor", "art-band", "avatar",
    # One slot per tile in the chip rail and the label row. These carry the brand's
    # own connector icons, so they stay empty until someone supplies them.
    "icon-a", "icon-b", "icon-c", "icon-d", "icon-e", "icon-f",
)


POSTER_HEADLINE_FIT_SCRIPT = r'''<script id="poster-headline-fit">
(() => {
  const START_SIZE = 120;
  const MIN_SIZE = 72;
  const STEP = 2;
  const URL_START_SIZE = 56;
  const URL_MIN_SIZE = 36;

  function lineCount(element) {
    if (!element || !element.textContent.trim()) return 0;
    const range = document.createRange();
    range.selectNodeContents(element);
    const tops = [];
    for (const rect of range.getClientRects()) {
      if (rect.width <= 0 || rect.height <= 0) continue;
      if (!tops.some((top) => Math.abs(top - rect.top) < 2)) tops.push(rect.top);
    }
    return tops.length;
  }

  function fitPosterHeadline() {
    const title = document.querySelector('.poster-title');
    const headline = title && title.querySelector('[data-slot="headline"]');
    const accent = title && title.querySelector('[data-slot="headline-accent"]');
    if (!title || !headline) return true;

    const hasAccent = Boolean(accent && accent.textContent.trim());
    headline.style.whiteSpace = hasAccent ? 'nowrap' : 'normal';
    if (accent) accent.style.whiteSpace = hasAccent ? 'nowrap' : 'normal';

    const fits = () => {
      const primaryLines = lineCount(headline);
      const accentLines = lineCount(accent);
      const primaryWidthFits = headline.scrollWidth <= headline.clientWidth + 1;
      const accentWidthFits = !hasAccent || accent.scrollWidth <= accent.clientWidth + 1;
      return hasAccent
        ? primaryLines <= 1 && accentLines <= 1 && primaryWidthFits && accentWidthFits
        : primaryLines <= 2 && primaryWidthFits;
    };

    let size = START_SIZE;
    for (; size >= MIN_SIZE; size -= STEP) {
      title.style.setProperty('--poster-headline-size', `${size}px`);
      if (fits()) break;
    }

    const ok = fits();
    title.dataset.headlineFit = ok ? 'ok' : 'overflow';
    title.dataset.headlineLines = String(lineCount(headline) + lineCount(accent));
    title.dataset.headlineSize = `${Math.max(size, MIN_SIZE)}px`;
    return ok;
  }

  function fitPosterUrl() {
    const url = document.querySelector('.poster-url[data-slot="url"]');
    if (!url || !url.textContent.trim()) return true;
    let size = URL_START_SIZE;
    for (; size >= URL_MIN_SIZE; size -= 1) {
      url.style.setProperty('--poster-url-size', `${size}px`);
      if (url.scrollWidth <= url.clientWidth + 1) break;
    }
    const ok = url.scrollWidth <= url.clientWidth + 1;
    url.dataset.urlFit = ok ? 'ok' : 'overflow';
    url.dataset.urlSize = `${Math.max(size, URL_MIN_SIZE)}px`;
    return ok;
  }

  function fitPosterTypography() {
    const headlineOk = fitPosterHeadline();
    const urlOk = fitPosterUrl();
    return headlineOk && urlOk;
  }

  window.__fitPosterHeadline = fitPosterHeadline;
  window.__fitPosterUrl = fitPosterUrl;
  window.__fitPosterTypography = fitPosterTypography;
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(fitPosterTypography);
  } else {
    fitPosterTypography();
  }
})();
</script>'''


def load_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except ImportError:
        pass
    return _simple_yaml(text)


def _simple_yaml(text: str) -> dict[str, Any]:
    """Minimal nested YAML subset (mappings + lists of scalars) for examples."""
    # Prefer JSON if the file is actually JSON
    stripped = text.lstrip()
    if stripped.startswith("{"):
        return json.loads(text)

    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    pending_list_key: str | None = None
    pending_list_indent = -1

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if line.startswith("- "):
            val = _parse_scalar(line[2:].strip())
            if isinstance(parent, list):
                parent.append(val)
            elif pending_list_key and isinstance(parent, dict):
                lst = parent.setdefault(pending_list_key, [])
                if not isinstance(lst, list):
                    lst = []
                    parent[pending_list_key] = lst
                lst.append(val)
            continue

        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        pending_list_key = None

        if rest == "" or rest == "|" or rest == ">":
            # Look ahead: could be nested map or list — create dict by default
            child: dict[str, Any] = {}
            if isinstance(parent, dict):
                parent[key] = child
            stack.append((indent, child))
            pending_list_key = key
            pending_list_indent = indent
            continue

        val = _parse_scalar(rest)
        if isinstance(parent, dict):
            # If we previously created empty dict for this key and now... shouldn't happen
            parent[key] = val

    # Fix empty dicts that should have been lists: not needed for our example
    # Convert mistaken nest: when a dict only got list items via pending — handled above
    return _fix_yaml_lists(root)


def _fix_yaml_lists(obj: Any) -> Any:
    """Convert dicts that only contain integer-like sequential values — no-op for our payloads."""
    if isinstance(obj, dict):
        # If a value is empty dict but we intended list — leave as {}
        return {k: _fix_yaml_lists(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_fix_yaml_lists(v) for v in obj]
    return obj


def _parse_scalar(s: str) -> Any:
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    if s.lower() in {"true", "false"}:
        return s.lower() == "true"
    if s.lower() in {"null", "~"}:
        return None
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


def resolve_template_id(name: str) -> str:
    if name in TEMPLATE_FILES:
        return name
    if name in ALIASES:
        return ALIASES[name]
    # allow filename without .html
    stem = name.replace(".html", "")
    if stem in ALIASES:
        return ALIASES[stem]
    raise SystemExit(f"Unknown template: {name}. Use --list-templates.")


def load_default_tokens() -> dict[str, Any]:
    if TOKENS_JSON.is_file():
        return json.loads(TOKENS_JSON.read_text(encoding="utf-8"))
    return {}


def build_override_css(payload: dict[str, Any]) -> str:
    colors = payload.get("colors") or payload.get("color") or {}
    fonts = payload.get("fonts") or payload.get("font") or {}
    lines = [":root {"]
    if isinstance(colors, dict):
        for k, v in colors.items():
            css_var = COLOR_CSS.get(k) or (k if str(k).startswith("--") else None)
            if css_var and v is not None:
                lines.append(f"  {css_var}: {v};")
    if isinstance(fonts, dict):
        for k, v in fonts.items():
            css_var = FONT_CSS.get(k) or (k if str(k).startswith("--") else None)
            if css_var and v is not None:
                # allow bare family name or full stack
                val = v if "," in str(v) or str(v).startswith('"') else f'"{v}", system-ui, sans-serif'
                lines.append(f"  {css_var}: {val};")
    lines.append("}")
    if len(lines) <= 2:
        return ""
    return "\n".join(lines)


def set_text_slot(html: str, slot: str, value: str | None) -> str:
    if value is None:
        return html
    safe = escape(str(value)).replace("\n", "<br>\n")
    # Replace inner HTML of elements with data-slot="slot"
    pattern = re.compile(
        rf'(<(?P<tag>\w+)([^>]*\sdata-slot="{re.escape(slot)}"[^>]*)>)(.*?)(</(?P=tag)>)',
        re.DOTALL | re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        return f"{m.group(1)}{safe}{m.group(5)}"

    new_html, n = pattern.subn(repl, html, count=1)
    if n == 0 and slot == "title-tag":
        new_html = re.sub(r"(<title[^>]*>)(.*?)(</title>)", rf"\1{safe}\3", html, count=1, flags=re.I | re.S)
    return new_html


def set_image_slot(html: str, slot: str, src: str | None, alt: str = "") -> str:
    if not src:
        return html
    # Resolve relative paths to file:// for standalone HTML viewing
    src_path = Path(src)
    if src_path.is_file():
        href = Path(src_path.resolve()).as_uri()
    elif src.startswith(("http://", "https://", "data:", "file:")):
        href = src
    else:
        # keep relative as-is (caller may place assets beside output)
        href = src
    alt_e = escape(alt or slot)
    img = f'<img data-slot="{escape(slot)}" src="{escape(href, quote=True)}" alt="{alt_e}" />'

    # Prefer replacing contents of a container with data-slot
    pattern = re.compile(
        rf'(<(?P<tag>\w+)([^>]*\sdata-slot="{re.escape(slot)}"[^>]*)>)(.*?)(</(?P=tag)>)',
        re.DOTALL | re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        tag = m.group("tag").lower()
        if tag == "img":
            # replace the whole img tag
            return img
        return f"{m.group(1)}{img}{m.group(5)}"

    new_html, n = pattern.subn(repl, html, count=1)
    if n:
        return new_html
    # Or replace bare <img data-slot="...">
    img_pat = re.compile(rf'<img[^>]*\sdata-slot="{re.escape(slot)}"[^>]*/?>', re.I)
    new_html, n = img_pat.subn(img, html, count=1)
    return new_html if n else html


def inject_override_css(html: str, css: str) -> str:
    if not css:
        return html
    block = f"<style id=\"brand-token-overrides\">\n{css}\n</style>\n"
    if re.search(r"</head>", html, re.I):
        return re.sub(r"</head>", block + "</head>", html, count=1, flags=re.I)
    return block + html


def inject_poster_headline_fit(html: str) -> str:
    """Keep poster headlines to two visible lines without silently truncating copy."""
    if 'class="poster"' not in html or 'id="poster-headline-fit"' in html:
        return html
    if re.search(r"</body>", html, re.I):
        return re.sub(
            r"</body>",
            POSTER_HEADLINE_FIT_SCRIPT + "\n</body>",
            html,
            count=1,
            flags=re.I,
        )
    return html + "\n" + POSTER_HEADLINE_FIT_SCRIPT + "\n"


def rewrite_tokens_css_href(html: str, out_dir: Path) -> str:
    """Copy tokens.css, fonts.css, and licensed font files beside the export."""
    src = HTML_DIR / "tokens.css"
    dest = out_dir / "tokens.css"
    if src.is_file():
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    fonts_root = ROOT / "assets" / "fonts"
    fonts_css = fonts_root / "fonts.css"
    if fonts_css.is_file():
        (out_dir / "fonts.css").write_text(fonts_css.read_text(encoding="utf-8"), encoding="utf-8")
    for rel in (
        "outfit/Outfit-VariableFont_wght.ttf",
        "smiley-sans/SmileySans-Oblique.ttf.woff2",
        "noto-sans-sc/NotoSansSC-Variable.ttf",
    ):
        font_src = fonts_root / rel
        if font_src.is_file():
            font_dest = out_dir / rel
            font_dest.parent.mkdir(parents=True, exist_ok=True)
            font_dest.write_bytes(font_src.read_bytes())
    for kit in ("poster-kit.css", "landscape-kit.css", "video-frame-kit.css"):
        kit_src = HTML_DIR / kit
        if kit_src.is_file() and f'href="{kit}"' in html:
            (out_dir / kit).write_text(kit_src.read_text(encoding="utf-8"), encoding="utf-8")
    html = html.replace('href="../../fonts/fonts.css"', 'href="fonts.css"')
    html = copy_visual_kit(html, out_dir)
    return html


def copy_visual_kit(html: str, out_dir: Path) -> str:
    """Copy packaged SVG materials next to the export and rewrite their URLs."""
    refs = re.findall(r'(?:\.\./)+visual-kit/[^\s"\']+', html)
    for ref in refs:
        rel = ref.split("visual-kit/", 1)[1]
        src = ROOT / "assets" / "visual-kit" / rel
        if not src.is_file():
            continue
        dest = out_dir / "visual-kit" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())
        html = html.replace(ref, f"visual-kit/{rel}")
    return html


SCREEN_SLOTS = {"ui-screenshot", "hero", "product-art", "icon", "art-band"}
LOGO_NAME_MARKERS = ("logo", "lockup", "wordmark", "logomark")


def image_src(val: Any) -> str:
    if isinstance(val, dict):
        return str(val.get("src") or val.get("path") or "")
    return str(val or "")


def resolve_image_src(src: str) -> str:
    """Resolve local payload paths and refuse broken local image references."""
    if not src:
        return ""
    if src.startswith(("http://", "https://", "data:", "file:")):
        return src

    candidate = Path(src).expanduser()
    candidates = [candidate] if candidate.is_absolute() else [Path.cwd() / candidate, ROOT / candidate]
    for path in candidates:
        if path.is_file():
            return str(path.resolve())

    print(f"warning: image source ignored because it does not exist: {src}", file=sys.stderr)
    return ""


def normalize_src(src: str) -> str:
    return src.replace("\\", "/").split("?", 1)[0].rstrip("/").lower()


def is_logo_standin(src: str, logo_srcs: set[str]) -> bool:
    norm = normalize_src(src)
    if not norm:
        return False
    if norm in logo_srcs:
        return True
    name = norm.rsplit("/", 1)[-1]
    return any(marker in name for marker in LOGO_NAME_MARKERS)


def fill_template(template_id: str, payload: dict[str, Any], out_dir: Path) -> Path:
    fname = TEMPLATE_FILES[template_id]
    src = HTML_DIR / fname
    if not src.is_file():
        raise SystemExit(f"Missing template file: {src}")

    html = src.read_text(encoding="utf-8")
    out_dir.mkdir(parents=True, exist_ok=True)
    html = rewrite_tokens_css_href(html, out_dir)

    # Per-template content may live under payload.templates[id] or payload.content
    templates = payload.get("templates") or {}
    local = templates.get(template_id) or templates.get(ALIASES.get(template_id, "")) or {}
    if not local and isinstance(payload.get("content"), dict):
        # single-template payload
        local = payload["content"]

    # Merge top-level text/images as fallbacks
    text = dict(payload.get("text") or {})
    images = dict(payload.get("images") or {})
    if isinstance(local, dict):
        text.update(local.get("text") or {})
        images.update(local.get("images") or {})
        # allow flat keys on local
        for k in TEXT_SLOTS:
            if k in local and k not in text:
                text[k] = local[k]
        for k in IMAGE_SLOTS:
            if k in local and k not in images:
                images[k] = local[k]

    for slot in TEXT_SLOTS:
        if slot in text:
            html = set_text_slot(html, slot, text[slot])

    logo_srcs = {normalize_src(image_src(images.get(key))) for key in ("logo", "logo-mark", "logo-lockup")}
    logo_srcs.discard("")
    if "ui-screenshot" not in images and images.get("hero"):
        hero_src = image_src(images["hero"])
        if is_logo_standin(hero_src, logo_srcs):
            print("warning: hero ignored for ui-screenshot — a logo is not a product UI screenshot", file=sys.stderr)
        else:
            images["ui-screenshot"] = images["hero"]

    for slot in IMAGE_SLOTS:
        if slot in images:
            val = images[slot]
            src = resolve_image_src(image_src(val))
            if not src:
                continue
            alt = val.get("alt") or "" if isinstance(val, dict) else ""
            if slot in SCREEN_SLOTS and is_logo_standin(src, logo_srcs):
                print(
                    f"warning: {slot} ignored — a logo is not a product UI screenshot or icon plate",
                    file=sys.stderr,
                )
                continue
            if isinstance(val, dict):
                html = set_image_slot(html, slot, src, alt)
            else:
                html = set_image_slot(html, slot, src)

    # Logo convenience: images.logo applies to logo / logo-mark / logo-lockup if those unset
    if "logo" in images:
        for extra in ("logo-mark", "logo-lockup"):
            if extra not in images:
                val = images["logo"]
                src_v = resolve_image_src(image_src(val))
                if not src_v:
                    continue
                alt_v = val.get("alt", "") if isinstance(val, dict) else ""
                html = set_image_slot(html, extra, src_v, alt_v)

    css = build_override_css(payload)
    # allow local color overrides
    if isinstance(local, dict) and (local.get("colors") or local.get("fonts")):
        merged = dict(payload)
        if local.get("colors"):
            merged["colors"] = {**(payload.get("colors") or {}), **local["colors"]}
        if local.get("fonts"):
            merged["fonts"] = {**(payload.get("fonts") or {}), **local["fonts"]}
        css = build_override_css(merged)
    html = inject_override_css(html, css)
    html = inject_poster_headline_fit(html)

    # Locale
    locale = (local.get("locale") if isinstance(local, dict) else None) or payload.get("locale") or "en"
    html = re.sub(r'(<html[^>]*\slang=")[^"]*"', rf'\1{escape(str(locale))}"', html, count=1, flags=re.I)

    out_html = out_dir / fname
    out_html.write_text(html, encoding="utf-8")
    return out_html


def try_png_export(html_path: Path, png_path: Path, width: int, height: int) -> tuple[bool, str]:
    """Optional Playwright screenshot. Returns (ok, message)."""
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception as e:
        return False, (
            "PNG export skipped — Playwright not installed. "
            f"Filled HTML is at {html_path}. "
            "Host export: npx playwright install chromium, then re-run with --png. "
            f"({e.__class__.__name__})"
        )

    url = html_path.resolve().as_uri()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page.goto(url, wait_until="networkidle")
            page.evaluate(
                """async () => {
                  if (document.fonts && document.fonts.ready) await document.fonts.ready;
                  if (window.__fitPosterTypography) window.__fitPosterTypography();
                }"""
            )
            overflow = page.query_selector('.poster-title[data-headline-fit="overflow"]')
            if overflow:
                browser.close()
                return False, (
                    "PNG export blocked — poster headline cannot fit within two lines "
                    "at the minimum approved size. Shorten the approved headline."
                )
            url_overflow = page.query_selector('.poster-url[data-url-fit="overflow"]')
            if url_overflow:
                browser.close()
                return False, (
                    "PNG export blocked — poster URL cannot fit the reserved footer width "
                    "at the minimum approved size. Use a shorter display URL."
                )
            # Screenshot the canvas article if present
            handle = page.query_selector("article.canvas, article.poster, article.ls, article.vf")
            # An overlay frame is meant to be composited over a video still, so its
            # PNG has to keep the alpha channel instead of baking in a backdrop.
            overlay = bool(page.query_selector("article.vf--overlay"))
            if handle:
                handle.screenshot(path=str(png_path), type="png", omit_background=overlay)
            else:
                page.screenshot(path=str(png_path), type="png", omit_background=overlay,
                                clip={"x": 0, "y": 0, "width": width, "height": height})
            browser.close()
        return True, f"Wrote PNG {png_path}"
    except Exception as e:
        return False, f"PNG export failed: {e}. HTML remains at {html_path}."


def canvas_size(template_id: str) -> tuple[int, int]:
    sizes = {
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
        "tpl-video-cover": (1920, 1080),
        "tpl-profile-avatar": (400, 400),
        "tpl-x-banner": (2048, 900),
        "tpl-youtube-banner": (2048, 1152),
        "tpl-linkedin-banner": (2048, 400),
        "tpl-logo-mark": (80, 80),
        "tpl-logo-lockup": (365, 80),
    }
    if template_id.startswith("tpl-video-frame-"):
        return (1920, 1080)
    return sizes[template_id]


def main() -> int:
    ap = argparse.ArgumentParser(description="Fill HTML marketing templates from a brand payload.")
    ap.add_argument("--template", "-t", help="Template id or short name (e.g. tpl-feature-poster)")
    ap.add_argument("--payload", "-p", type=Path, help="Brand payload JSON or YAML")
    ap.add_argument("--out", "-o", type=Path, help="Output directory")
    ap.add_argument("--png", action="store_true", help="Attempt Playwright PNG export if available")
    ap.add_argument("--list-templates", action="store_true")
    args = ap.parse_args()

    if args.list_templates:
        print("HTML templates:")
        for tid, fn in TEMPLATE_FILES.items():
            w, h = canvas_size(tid)
            print(f"  {tid:24} {fn:24} {w}x{h}")
        print("Storyboard frames are stills, not MP4: the tpl-video-frame-* family.")
        return 0

    if not args.template or not args.payload or not args.out:
        ap.error("--template, --payload, and --out are required (or use --list-templates)")

    tid = resolve_template_id(args.template)
    payload = load_payload(args.payload)
    out_dir = args.out
    html_path = fill_template(tid, payload, out_dir)
    print(f"Wrote HTML {html_path}")

    # Sidecar note
    note = out_dir / "EXPORT.md"
    w, h = canvas_size(tid)
    note.write_text(
        "\n".join(
            [
                f"# Export notes — {tid}",
                "",
                f"- Canvas: **{w}×{h}** (packaged size kit; non-negotiable).",
                f"- Filled HTML: `{html_path.name}`",
                "- Colors/fonts overridden via injected `#brand-token-overrides` from payload.",
                "- PNG export is host-dependent (Playwright/Chromium). Re-run with `--png` when available.",
                "- Do not hard-code brand colors/images into the shared template files; use payloads.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    if args.png:
        png_path = out_dir / (html_path.stem + ".png")
        ok, msg = try_png_export(html_path, png_path, w, h)
        print(("OK: " if ok else "NOTE: ") + msg)
        if not ok:
            note.write_text(note.read_text(encoding="utf-8") + f"\nPNG: {msg}\n", encoding="utf-8")
    else:
        print("NOTE: PNG not requested. Open HTML in a browser or re-run with --png when Playwright is available.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
