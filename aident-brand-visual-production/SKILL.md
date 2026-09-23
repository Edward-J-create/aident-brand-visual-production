---
name: aident-brand-visual-production
description: Produce marketing visual result files and video production kits that feed aident-brand-marketing-pack. Create posters, social avatars, banners, feature posters, OG/social cards, and video inputs (storyboards, shot lists, poster frames, motion assets) and, when authorized, final MP4/MOV exports—using the packaged size kit, typography, and HTML layout templates. Use when the user lacks brand visual/video assets, asks to render or export campaign creatives from a pack handoff or visual/video brief, mentions storyboards, shot lists, social avatar/banner, feature poster, or needs PNG/JPEG/SVG/MP4/MOV originals for the marketing pack. Do not use for writing pack copy or cloud pack documents (use aident-brand-marketing-pack); do not use for full brand-identity systems/tokens/brand books (use aident-brand-design-skill); do not use for generic long-form video toolchains unrelated to pack handoffs (use hyperframes-general-video or host video tools). Do not look up, link, or redistribute private design source files.
license: MIT
metadata:
  version: 0.3.0
  author: Edward-J-create
---

# Aident Brand Visual Production

Produce **finished marketing media** (and video production inputs) from a frozen pack handoff or equivalent brief. Typography, frame sizes, and layout structure come from the packaged templates in this skill—not freeform improvisation, and not from a private design file.

**Default final files:** PNG / JPEG / SVG and MP4 / MOV. Editable Figma/PSD/AE/Remotion sources are optional side exports only when requested. **Never** claim a storyboard or shot list is a final video.

## Relationship to other Skills

| Skill | Role |
|---|---|
| **aident-brand-marketing-pack** (upstream) | Copy, taxonomy, quality gates, frozen `visual-brief` / `video-brief`, handoff authorization, pack document + durable library ingest |
| **This Skill** | Template-driven image exports; video storyboard/shot-sheet/assets; optional authorized final video exports; return package with QA |
| **aident-brand-design-skill** (adjacent) | Brand identity system, tokens, logo lockups rules, HTML brand book—not campaign media rendering |
| **hyperframes-general-video** (adjacent, optional) | General video tooling; may be selected as a renderer after the contract is frozen—never a hard dependency |
| **aident-ppt-skill** (adjacent) | Deck / Motion Slides HTML—reference for **packaging granularity** (HTML templates + editable tokens/slots). This skill still owns pack social/poster/video originals at the packaged template sizes |

**Complementarity rule:** This Skill does **not** write pack copy, classify pack taxonomy, or create the Lark/Google/Notion marketing document. It consumes approved copy + briefs and emits inspectable media (+ storyboard/shot sheets) for pack to package.

## Non-negotiables

1. **Match the mode.** Image kit does not invent a finished video; video-kit-only does not claim MP4 delivery unless encode was authorized; both requires both families explicitly.
2. **Frozen contract first.** Work only from a pack handoff or a completed visual/video brief with asset IDs, exact copy text, dimensions, rights, and acceptance checks. If any P0 field is missing, return `blocked`—do not invent brand facts or copy.
3. **Templates own structure.** Fixed sizes, type roles, margins, and safe areas come from `assets/templates/`. Do not freestyle a new layout system per job. **Sizes in `size-kit.yaml` are non-negotiable** for known `tpl-*` IDs. Private design source files are not part of this package: do not link them, fetch them, or ask the user to open them.
4. **Prefer HTML template fill → export.** For static image kits, fill `assets/templates/html/*.html` via brand payload + `scripts/render_html_template.py`, then rasterize on the host (Playwright/Chromium or design-tool export). Do not invent a parallel layout system.
5. **Replaceable copy and logos; fixed poster materials.** Text and logo slots stay editable. Poster backgrounds, bloom shapes, and the grain layer come from `assets/templates/poster-specs.json` plus the SVG files under `assets/visual-kit/`. Do not repaint a poster with `colors.bg` / `colors.accent` or a few CSS circles. A brand recolor is a replaced SVG, not a flat hex. The middle of a UI poster is a supplied screenshot or an authorized capture. A logo, mark, or lockup never goes in that slot.
6. **Critical typography is template/editable-layer owned.** Prompts may drive background/scene imagery; they must not be the sole source of headlines, CTAs, disclaimers, or legal lines.
7. **Fonts are packaged and replaceable.** Default faces are OFL Outfit (primary) and Smiley Sans (display), with license files under `assets/fonts/`. `@font-face` lives in `fonts.css`. A brand payload may override `--font-primary` / `--font-display`. Do not add a font binary that has no license file.
8. **Never redraw a real logo** with a generative model. Place supplied logo SVG/PNG into logo slots; preserve intrinsic aspect ratio, clearspace, and approved variants only.
9. **Never fabricate product UI, metrics, testimonials, partnerships, or third-party marks** as evidence. Conceptual UI must be labeled.
10. **Result files ≠ projects.** Default outputs are full-quality PNG/JPEG/SVG and/or MP4/MOV (plus storyboard/shot-sheet documents for video kit). Layered Figma/PSD/AE/Remotion projects are optional side exports only when requested. Filled HTML is an editable intermediate, not a substitute for inspected PNG/JPEG masters unless the brief accepts HTML delivery.
11. **Inspect before `delivered`.** Record MIME, bytes, pixel dimensions or duration, openability, and SHA-256 when bytes are available. Exact export size must match the brief / size-kit.
12. **No unpaid/unauthorized generation.** Paid image/video APIs, stock licenses, or external publication require explicit user authorization.
13. **Honest status.** Storyboards and shot lists are never labeled as final video. Deviations from the brief are listed explicitly. Do not upscale, screenshot, or transcode a preview and call it an original.

## Modes

Infer the narrowest mode that satisfies the request:

| Mode | When | Primary outputs |
|---|---|---|
| **image-kit** | Static marketing visuals only | Per-asset PNG/JPEG/SVG (+ optional editable source), return manifest |
| **video-kit** | Video planning / production inputs; final encode optional | Storyboard, shot list, poster/frame stills, asset board; MP4/MOV only if authorized and feasible |
| **both** | Pack asked for finished media across image + video families | Union of above under one handoff ID |
| **qa-only** | User/pack returns files for inspection | QA report + pass/fail vs frozen acceptance; no new creative |

If the user says all creative decisions need confirmation, stop at an approval gate with options even when drafts exist.

## Packaged size kit

The public contract is `assets/templates/size-kit.yaml` plus the HTML frames. Design source files used while authoring these templates are **not** included and must not be linked or fetched.

| Template ID | Use | Size (px) | Aspect |
|---|---|---|---|
| `tpl-video-cover` | Video cover / horizontal poster | **1920×1080** | 16:9 |
| `tpl-feature-poster` | Product UI poster (layout 00) | **1242×1660** | ~3:4 |
| `tpl-poster-shot` | Screenshot poster, dark wash (layout 01) | **1242×1660** | ~3:4 |
| `tpl-poster-stage` | Lower glass stage (layout 02) | **1242×1660** | ~3:4 |
| `tpl-poster-cluster` | Wide middle plate (layout 03) | **1242×1660** | ~3:4 |
| `tpl-poster-grid` | Side icon plate (layout 04) | **1242×1660** | ~3:4 |
| `tpl-poster-table` | Center icon plate (layout 05) | **1242×1660** | ~3:4 |
| `tpl-feature-poster-zh` | Product UI poster, 中文 | **1242×1660** | ~3:4 |
| `tpl-poster-shot-zh` | Screenshot poster, 中文 | **1242×1660** | ~3:4 |
| `tpl-poster-stage-zh` | Lower glass stage, 中文 | **1242×1660** | ~3:4 |
| `tpl-poster-cluster-zh` | Wide middle plate, 中文 | **1242×1660** | ~3:4 |
| `tpl-poster-grid-zh` | Side icon plate, 中文 | **1242×1660** | ~3:4 |
| `tpl-poster-table-zh` | Center icon plate, 中文 | **1242×1660** | ~3:4 |
| `tpl-banner` | Light marketing banner, stats (+ ZH) | **1270×760** | ~1.67:1 |
| `tpl-banner-prompt` | Light marketing banner, prompt pill (+ ZH) | **1270×760** | ~1.67:1 |
| `tpl-x-banner` | X profile banner | **2048×900** | ~2.28:1 |
| `tpl-youtube-banner` | YouTube channel banner | **2048×1152** | 16:9 |
| `tpl-linkedin-banner` | LinkedIn cover banner | **2048×400** | ~5.12:1 |
| `tpl-profile-avatar` | Profile avatar | **400×400** | 1:1 |
| `tpl-logo-mark` | Logo/mark slot (place real logo) | **80×80** | 1:1 |
| `tpl-logo-lockup` | Logo lockup (hug width) | **~257–365×80** | hug×80 |
| `tpl-video-frame-title` | Storyboard title card (mesh field) | **1920×1080** | 16:9 |
| `tpl-video-frame-logo` | Storyboard logo lockup beat | **1920×1080** | 16:9 |
| `tpl-video-frame-caption` | Storyboard mark + caption beat | **1920×1080** | 16:9 |
| `tpl-video-frame-ui` | Storyboard product UI card (flat field) | **1920×1080** | 16:9 |
| `tpl-video-frame-stat` | Storyboard stat pair (flat field) | **1920×1080** | 16:9 |
| `tpl-video-frame-chips` | Storyboard mark + 6-icon rail | **1920×1080** | 16:9 |
| `tpl-video-frame-label-row` | Storyboard word / icon row / word | **1920×1080** | 16:9 |
| `tpl-video-frame-endcard` | Storyboard end card + CTA | **1920×1080** | 16:9 |
| `tpl-video-frame-message` | Storyboard prompt-bubble beat | **1920×1080** | 16:9 |
| `tpl-video-frame-messages` | Storyboard stacked bubbles | **1920×1080** | 16:9 |
| `tpl-video-frame-input` | Storyboard input pill, hugs the text | **1920×1080** | 16:9 |
| `tpl-video-frame-steps` | Storyboard step list, each pill hugs its label | **1920×1080** | 16:9 |
| `tpl-video-frame-subtitle` | Storyboard subtitle overlay (alpha PNG) | **1920×1080** | 16:9 |

Typography: primary **Outfit** 400/600; accent/display sometimes **Smiley Sans**. Both ship as OFL files and stay overridable. See `assets/fonts/` and `references/figma-template-kit.md`.

### HTML template family (v0.3)

Editable HTML canvases (CSS variables + `data-slot`s) live in `assets/templates/html/`. Granularity matches `aident-ppt-skill` (layout templates + tokens + replaceable content). Geometry is the packaged size kit.

| HTML file | Template ID | Size |
|---|---|---|
| `feature-poster.html` | `tpl-feature-poster` | 1242×1660 |
| `poster-shot.html` | `tpl-poster-shot` | 1242×1660 |
| `poster-stage.html` | `tpl-poster-stage` | 1242×1660 |
| `poster-cluster.html` | `tpl-poster-cluster` | 1242×1660 |
| `poster-grid.html` | `tpl-poster-grid` | 1242×1660 |
| `poster-table.html` | `tpl-poster-table` | 1242×1660 |
| `feature-poster-zh.html` | `tpl-feature-poster-zh` | 1242×1660 |
| `poster-shot-zh.html` | `tpl-poster-shot-zh` | 1242×1660 |
| `poster-stage-zh.html` | `tpl-poster-stage-zh` | 1242×1660 |
| `poster-cluster-zh.html` | `tpl-poster-cluster-zh` | 1242×1660 |
| `poster-grid-zh.html` | `tpl-poster-grid-zh` | 1242×1660 |
| `poster-table-zh.html` | `tpl-poster-table-zh` | 1242×1660 |
| `banner.html` | `tpl-banner` | 1270×760 |
| `banner-prompt.html` | `tpl-banner-prompt` | 1270×760 |
| `video-cover.html` | `tpl-video-cover` | 1920×1080 |
| `profile-avatar.html` | `tpl-profile-avatar` | 400×400 |
| `x-banner.html` | `tpl-x-banner` | 2048×900 |
| `youtube-banner.html` | `tpl-youtube-banner` | 2048×1152 |
| `linkedin-banner.html` | `tpl-linkedin-banner` | 2048×400 |
| `logo-mark.html` | `tpl-logo-mark` | 80×80 |
| `logo-lockup.html` | `tpl-logo-lockup` | hug×80 |
| `video-frame-title.html` | `tpl-video-frame-title` | 1920×1080 |
| `video-frame-logo.html` | `tpl-video-frame-logo` | 1920×1080 |
| `video-frame-caption.html` | `tpl-video-frame-caption` | 1920×1080 |
| `video-frame-ui.html` | `tpl-video-frame-ui` | 1920×1080 |
| `video-frame-stat.html` | `tpl-video-frame-stat` | 1920×1080 |
| `video-frame-chips.html` | `tpl-video-frame-chips` | 1920×1080 |
| `video-frame-label-row.html` | `tpl-video-frame-label-row` | 1920×1080 |
| `video-frame-endcard.html` | `tpl-video-frame-endcard` | 1920×1080 |
| `video-frame-message.html` | `tpl-video-frame-message` | 1920×1080 |
| `video-frame-messages.html` | `tpl-video-frame-messages` | 1920×1080 |
| `video-frame-input.html` | `tpl-video-frame-input` | 1920×1080 |
| `video-frame-steps.html` | `tpl-video-frame-steps` | 1920×1080 |
| `video-frame-subtitle.html` | `tpl-video-frame-subtitle` | 1920×1080 |

Poster layouts, field colors, bloom stops, and the grain blend mode are fixed in `assets/templates/poster-specs.json`. Chinese variants use the same template as their matching layout. Sample wordmarks, product UI, and decorative art stay out of the templates; those regions are slots. The ten `video-frame-*` stills are the storyboard layouts, one per beat shape; their fixed materials are in `assets/templates/video-frame-specs.json`, and the landscape banners are in `assets/templates/banner-specs.json`. Only the frames the design gives a mesh get one; `ui`, `stat`, and `chips` sit on a flat field. `tpl-video-frame-subtitle` exports with alpha so it composites over a still. A storyboard still is not an MP4. Slot contract: `references/editable-slots.md`.

## Required workflow

### 1. Intake and mode

- Accept either: (a) pack production handoff package, or (b) filled `visual-brief` / `video-brief` YAML + copy deck + source assets.
- Initialize run record from `assets/templates/production-return.yaml`.
- Confirm mode (`image-kit` | `video-kit` | `both` | `qa-only`), locales, authorization for paid tools, and whether editable sources are requested.
- Ask only if missing answers would change size family, rights, logo treatment, or whether final video encode is in scope.

### 2. Validate frozen inputs

- Read `references/pack-handoff.md`.
- Verify every selected deliverable has: asset ID, dimensions/aspect (and duration/fps for video), exact approved copy text, logo/source IDs or explicit conceptual waiver, rights_status, approval_owner, acceptance_checks.
- Fail closed → status `blocked` with blocker list.

### 3. Bind templates

- Map each deliverable to a template ID from the size kit.
- Load layout zones from `assets/templates/layout-zones.md`, type/color roles from `assets/tokens/tokens.json`, and HTML frames from `assets/templates/html/` (see `references/editable-slots.md`).
- Build or reuse a brand payload (colors, fonts, text, image paths) — example: `examples/brand-payload.example.yaml`.
- Place supplied logos/UI/photos into designated `data-slot`s; do not stretch logos.

### 4. Produce image kit (modes: image-kit | both)

- Read `references/image-production.md`.
- **Preferred path:** fill HTML template with `scripts/render_html_template.py` → export PNG/JPEG at exact WxH (Playwright/Chromium or host design export). Filled HTML + `EXPORT.md` are always emitted. If the PNG bytes are missing, that asset stays `blocked`. Do not mark HTML as `delivered`.
- Alternate: the user's own design-tool export, or authorized generative fill for **non-text** regions only.
- Hard-coded brand colors/images inside shared templates = FAIL; change the payload instead.
- Export masters + required variants at exact pixels.
- Write sidecars: alt text (from brief), filename per convention, sha256.

### 5. Produce video kit (modes: video-kit | both)

- Read `references/video-production-kit.md`.
- Emit:
  - storyboard sheet (one beat / communication job per scene);
  - shot list with `source_type` labels (`supplied` | `capture-required` | `licensed-stock` | `generated-concept` | `motion-design`);
  - poster frame still(s) matching brief `poster_frame`;
  - asset board of stills/graphics needed for edit.
- If final video is authorized and feasible, encode master/cutdowns to brief resolution/fps/duration; else leave video status `blocked` or `in-production` with next action—**never** pass a storyboard off as MP4.

### 6. QA gate

- Read `references/quality-gates.md`.
- For each file: open, measure, hash, compare to acceptance_checks (safe area, contrast, copy accuracy, logo clearspace, duration, captions if required).
- List deviations. P0 failures → cannot mark `delivered`.

### 7. Return package for pack ingest

Emit a folder:

```text
return/<handoff_id>/
  RETURN.md                 # human summary
  return-manifest.yaml      # machine contract (mirrors pack return fields)
  media/                    # PNG/JPEG/SVG/MP4/MOV
  docs/                     # storyboard, shot-list, asset-board
  editable/                 # optional sources only if requested
  qa/                       # inspection notes, dimension logs
```

Filenames:

```text
{asset_id}__{WxH-or-dur}__{locale}.{ext}
```

Per-asset status: `in-production` | `blocked` | `delivered`.

Hand the return package back to **aident-brand-marketing-pack** for original-file registration, durable upload, and document placement. Do not claim the cloud pack is complete from this Skill alone. Do not set pack labels `Original file — ready` yourself (pack verifies durable audience access). Production may only assert local QA: `full_quality_verified: true|false`.

## Output contract (must match pack)

### Always

- `return-manifest.yaml` with handoff_id, brief_version, per-asset records (filename, mime, bytes, sha256, dimensions_or_duration, sources used, deviations, qa, status)
- Media files for every asset marked `delivered`
- Explicit blocker list for anything not delivered

### Image-kit extras

- One master export per master_asset_id + each required variant
- Alt text string per still

### Video-kit extras

- `docs/storyboard.md` (or PDF/PNG contact sheet)
- `docs/shot-list.yaml` (ids, timecodes, source_type, copy_ids, product_accuracy_notes)
- Poster still(s) as raster originals
- Final MP4/MOV only when authorized and QA-passed

## Reference loading map

| Task | Read |
|---|---|
| Every run | `references/pack-handoff.md`, `references/quality-gates.md`, `references/scope-and-modes.md` |
| Template sizes / zones | `references/figma-template-kit.md`, `assets/templates/size-kit.yaml`, `assets/templates/layout-zones.md` |
| Still production | `references/image-production.md`, `references/editable-slots.md`, `assets/templates/html/` |
| HTML fill / tokens | `scripts/render_html_template.py`, `assets/templates/html/tokens.css`, `examples/brand-payload.example.yaml` |
| Video kit / encode | `references/video-production-kit.md` |
| Host / renderer options | `references/host-compatibility.md` |
| What is still open | `references/reference-gap-matrix.md` |

## Completion contract

A run is **complete for pack handoff** only when:

1. Every requested deliverable is either `delivered` with inspected result files or explicitly `blocked` with a named blocker;
2. `return-manifest.yaml` is consistent with files on disk;
3. No invented logos, UI, claims, or “fake originals”;
4. Video storyboard/shot sheets are present when video-kit/both was requested;
5. The Skill has not silently written pack copy or a cloud marketing document;
6. Storyboard/shot-list artifacts are never marked as final MP4/MOV.

Validate the installed package with `python scripts/validate_package.py`. That command also runs `scripts/check_render.py`: it fills the poster, banner, and cover from the synthetic payload, checks that slots and color overrides landed without editing the shared templates, and inspects PNG dimensions when export works. A missing PNG is reported as blocked.
