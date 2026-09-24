# aident-brand-visual-production

Agent Skill that **produces** marketing image kits and video production kits for brands that lack finished visuals. It feeds **[aident-brand-marketing-pack](../aident-brand-marketing-pack)** (copy, taxonomy, quality, cloud document + durable library).

| | Marketing pack | This skill |
|---|---|---|
| Owns | Copy, briefs, handoff freeze, pack document, original-file ingest | Rendering/compositing, storyboards/shot lists, export QA, return package |
| Default outputs | Editable cloud doc + durable media library | PNG/JPEG/SVG and (when authorized) MP4/MOV + docs |
| Does not | Draw logos or invent footage | Write pack copy or claim cloud pack complete |

Packaging granularity (HTML layout templates + editable tokens/slots) is aligned with Edward's **aident-ppt-skill**. Sizes and layout live in this skill's packaged templates. Design source files are not part of the package.

## Install

The portable package is this directory (`SKILL.md` plus `assets/`, `references/`, `scripts/`, and `examples/`). It is not tied to one agent. Copy the whole directory, not only `SKILL.md`.

```bash
npx skills add Edward-J-create/aident-brand-visual-production \
  --skill aident-brand-visual-production \
  --global \
  --agent codex claude-code cursor opencode \
  --yes
```

Python 3.9+ runs `scripts/render_html_template.py` and `scripts/validate_package.py`. PNG export needs Playwright and Chromium on the host (`python3 -m pip install playwright && python3 -m playwright install chromium`). A missing browser blocks the PNG and still leaves filled HTML. It does not block the skill from loading.

## Marketing-pack fast path

Turn the frozen pack handoff into per-asset payloads, filled HTML, storyboard/shot-list documents, and a return manifest:

```bash
python scripts/prepare_pack_run.py \
  --handoff examples/both-from-pack-handoff.yaml \
  --out /tmp/abvp-return \
  --png
```

The bridge resolves stable approved-copy and source-asset IDs into explicit template slots. It does not invent missing copy or media, and it keeps generated files `in-production` until visual/brand QA is complete. See `references/pack-bridge.md`.

## Replaceability model

Shared templates are **structures**, not baked brand kits:

| Layer | Mechanism | Swap how |
|---|---|---|
| Colors | CSS custom properties + `assets/tokens/tokens.json` roles | Brand payload `colors.*` (never edit shared HTML hex for a client) |
| Text | `[data-slot="headline|subcopy|cta|disclaimer"]` | Brand payload `text.*` |
| Imagery | `[data-slot="logo|hero|ui-screenshot|…"]` | Brand payload `images.*` paths to **supplied** files |
| Fonts | `--font-primary` / `--font-display` | Payload `fonts.*`; optional licensed local files — see `assets/fonts/licenses/README.md` |
| Sizes | `assets/templates/size-kit.yaml` | Non-negotiable for known `tpl-*` IDs |

Details: `references/editable-slots.md`.

Missing local image files are ignored with a warning instead of rendering broken-image glyphs. Delivered PNGs must contain neither broken images nor instructional slot labels. Supply approved light/dark logo variants for contrasting surfaces; the renderer never recolors a real logo.

Feature posters require an approved lower-right `text.url` and a supplied `images.ui-screenshot` (or `hero`) for the replaceable middle visual. Bind an emphasized second headline line separately as `text.headline-accent` so it receives the brighter gradient. Headlines fit to at most two total lines. The footer URL stays Outfit 400 / 56px for short domains and scales only when a longer display domain exceeds its reserved width.

## Preferred still pipeline

```bash
python scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster
# optional, when Playwright/Chromium is available:
python scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster \
  --png
```

## Modes

`image-kit` · `video-kit` · `both` · `qa-only`

## Size kit

See `assets/templates/size-kit.yaml` and `SKILL.md`. Known templates include video cover 1920×1080, feature posters 1242×1660, banners 1270×760, X/YouTube/LinkedIn banners, avatar 400×400, logo slots, and 1920×1080 video storyboard frames. HTML frames for all static image IDs live under `assets/templates/html/`.

## Validate

```bash
python scripts/validate_package.py
```

## License

MIT — see `LICENSE.md`. Marks and client work: `NOTICE.md`.
