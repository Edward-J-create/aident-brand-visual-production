# Aident Brand Visual Production

An open, cross-agent Skill that renders marketing image kits and video production kits from a frozen [aident-brand-marketing-pack](https://github.com/Edward-J-create/aident-brand-marketing-pack) handoff or an equivalent visual/video brief.

It fills packaged HTML templates, places supplied logos, and exports inspectable PNG/JPEG/SVG. Storyboards and shot lists are production inputs. An MP4 or MOV is produced only when encode is separately authorized. This Skill does not write pack copy or the cloud marketing document.

## What is packaged

| Layer | Where | Replace how |
|---|---|---|
| Layouts | `aident-brand-visual-production/assets/templates/html/` | Fill `data-slot`s. Do not invent a new frame per job. |
| Sizes | `assets/templates/size-kit.yaml` | Known `tpl-*` sizes stay fixed. |
| Poster, banner, and storyboard materials | `poster-specs.json`, `banner-specs.json`, `video-frame-specs.json`, `assets/visual-kit/` | Recolour by swapping the SVG. Do not flatten grain or redraw a logo. |
| Type | `assets/fonts/` (OFL Outfit, Smiley Sans, Noto Sans SC) | Override `--font-primary` / `--font-display` from the payload. |
| Copy and logos | Slots documented in `references/editable-slots.md` | Brand payload only. |

Chinese poster frames (`*-zh`) share the English geometry and ship with Chinese default copy.

## Cross-agent installation

The portable package is [`aident-brand-visual-production/`](aident-brand-visual-production/). It follows the open filesystem Agent Skills layout and is not tied to Codex or one model.

```bash
npx skills add Edward-J-create/aident-brand-visual-production \
  --skill aident-brand-visual-production
```

Install for the agents this machine already uses:

```bash
npx skills add Edward-J-create/aident-brand-visual-production \
  --skill aident-brand-visual-production \
  --global \
  --agent codex claude-code cursor opencode \
  --yes
```

Manual install: copy the complete package directory to the host skill folder, for example `~/.agents/skills/`, `~/.codex/skills/`, `~/.claude/skills/`, or `.cursor/skills/` inside a project. Hosts may ignore [`agents/openai.yaml`](aident-brand-visual-production/agents/openai.yaml). It is optional discovery metadata.

## Run

From a frozen `aident-brand-marketing-pack` handoff, validate bindings and prepare the whole return package in one command:

```bash
python3 aident-brand-visual-production/scripts/prepare_pack_run.py \
  --handoff aident-brand-visual-production/examples/both-from-pack-handoff.yaml \
  --out /tmp/abvp-return \
  --png
```

This resolves approved copy and source-asset IDs into template slots, fills all requested still/storyboard frames, and emits the pack-aligned return manifest. Raster files remain `in-production` until visual/brand QA is completed.

For one-off template rendering:

```bash
python3 aident-brand-visual-production/scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload aident-brand-visual-production/examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster \
  --png
```

`--png` needs Playwright and Chromium. Without them the command still writes filled HTML and records the PNG as blocked.

```bash
python3 scripts/validate_package.py
```

## Example request

```text
Use $aident-brand-visual-production to render the image kit from this frozen
marketing-pack handoff. Fill the packaged templates, place the supplied logo,
leave product UI empty if no screenshot was provided, and return inspected
PNG files plus the storyboard. Do not encode an MP4.
```
