# Image production

## Principles

1. Bind each deliverable to a `size-kit.yaml` template ID before any pixel paint.
2. Critical type (headline, CTA, disclaimer) lives in template/editable layers — not prompt-only bake-ins.
3. Generative fill is allowed for a scene only when authorized, and never for a packaged poster background, a logo, or the sole source of a claim.
4. Place supplied logo SVG/PNG into the footer logo slot or `tpl-logo-mark` / lockup slots; never generative-redraw.
5. Poster type is a template ID, not a freeform layout. Read `assets/templates/poster-specs.json` and fill that HTML file. Field color, bloom SVG, and grain blend mode stay as written there.
6. The middle slot is a user-supplied UI screenshot, an authorized product capture, or a supplied icon on the icon posters. If none of those exist, leave the slot empty and return `blocked`. Never place the logo, mark, or lockup in the middle.
7. Materials are SVG, or lossless transparent WebP when a photo texture is required. Do not JPEG-compress them and do not downscale them to save bytes. The grain layer composites with `mix-blend-mode: overlay`. Opacity is per template (`0.25` on posters, `0.30` on the social banners) and comes from `poster-specs.json` / `banner-specs.json`. Do not premultiply that into a flat background, and do not recolour `grain-overlay.svg`.
8. Landscape banners follow `banner-specs.json`. Storyboard stills follow `video-frame-specs.json`: one `tpl-video-frame-*` layout per beat. `ui`, `stat`, and `chips` stay on a flat field. `tpl-video-frame-subtitle` exports with alpha.
9. Export exact WxH. Filename: `{asset_id}__{W}x{H}__{locale}.{ext}`.

## Preferred paths (options, not lock-in)

1. **HTML template fill → export (default for static kits)**  
   `scripts/render_html_template.py` + brand payload → filled HTML → host PNG/JPEG. See `references/editable-slots.md`. `scripts/check_render.py` fills poster, banner, and cover and refuses to call a missing PNG delivered.
2. The user's own design-tool export → PNG/JPEG/SVG
3. Authorized image APIs for non-text regions only
4. Manual designer export guided by this skill's checklist

Hard-coded brand colors or baked client imagery inside shared `assets/templates/html/*` = FAIL; change the payload.

See `references/host-compatibility.md`.

## QA before `delivered`

- Openable; MIME matches extension
- Pixel dimensions match template/brief exactly
- Bytes + sha256 recorded when available
- Alt text present for stills
- Logo clearspace and copy accuracy checked against acceptance_checks
