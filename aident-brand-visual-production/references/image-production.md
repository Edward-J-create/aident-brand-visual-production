# Image production

## Principles

1. Bind each deliverable to a `size-kit.yaml` template ID before any pixel paint.
2. Critical type (headline, CTA, disclaimer) lives in template/editable layers — not prompt-only bake-ins.
3. Generative fill is allowed for a scene only when authorized, and never for a packaged poster background, a logo, or the sole source of a claim.
4. Place supplied logo SVG/PNG into the footer logo slot or `tpl-logo-mark` / lockup slots; never generative-redraw.
5. Poster type is a template ID, not a freeform layout. Read `assets/templates/poster-specs.json` and fill that HTML file. Field color, bloom SVG, and grain blend mode stay as written there.
6. The middle slot is a replaceable user-supplied UI screenshot, authorized product capture, or supplied icon on the icon posters. Bind UI-led feature posters through `images.ui-screenshot` (or the supported `hero` fallback). If none exists, leave the slot empty and return `blocked`. Never place the logo, mark, or lockup in the middle.
7. Feature posters require approved `text.url` for the lower-right footer. Keep its reference weight at Outfit 400 / 56px when the display domain fits; long domains may scale down within the reserved width but must not clip. Poster headlines may use at most two total lines. When line two is the approved emphasis, bind it to `text.headline-accent` so the template applies the brighter gradient. The renderer may reduce title size to its packaged minimum, then must block export rather than truncate or add a third line.
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
