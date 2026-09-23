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
