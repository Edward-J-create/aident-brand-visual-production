# Packaged template kit

Sizes, type roles, and layer boxes live in this package:

- `assets/templates/size-kit.yaml`
- `assets/templates/html/`
- `assets/templates/layout-zones.md`

Design source files used while authoring the templates are **not** part of the skill. Do not link them, fetch them, upload them, or ask a user to open them. A public run never depends on access to those files.

## What the kit contains

| Family | Templates | Sizes |
|---|---|---|
| Marketing stills | Video cover, feature/social posters 00–06 (+ ZH), banner (+ ZH) | Cover **1920×1080**; posters **1242×1660**; banner **1270×760** |
| Social banners | X, YouTube, LinkedIn | X **2048×900**; YouTube **2048×1152**; LinkedIn **2048×400** |
| Logo and avatar | Profile avatar, mark, lockup | Avatar **400×400**; mark **80×80**; lockup **~257–365×80** |
| Storyboard stills | Ten 16:9 layouts in `video-frame-specs.json` | **1920×1080**. Pick the layout that matches the beat. |

## Typography

- Primary: **Outfit** 400/600, bundled at `assets/fonts/outfit/`.
- Display: **Smiley Sans**, bundled at `assets/fonts/smiley-sans/`.
- Both are OFL and overridable from the brand payload.

## Rules

- Known `tpl-*` sizes stay as written in `size-kit.yaml`.
- Poster field colors, boxes, bloom SVGs, and the grain overlay blend are the code in `assets/templates/poster-specs.json`. Do not invent a different poster palette per job.
- Sample wordmarks, product UI, and decorative art are slots. Do not bake a client's logo or copy into the shared HTML.
- The `video-frame-*` canvases are storyboard stills. They are not a finished video, and this package does not ship a private storyboard catalog. `ui`, `stat`, and `chips` sit on a flat field. `tpl-video-frame-subtitle` exports with alpha.
