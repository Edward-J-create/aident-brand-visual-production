# Agent operating contract

This repository is a portable Agent Skill. Any host that can read `SKILL.md` and run Python 3 can use it. Cursor, Claude Code, Codex, and OpenCode should load the package directory `aident-brand-visual-production/`, not this file alone.

## Read first

1. `aident-brand-visual-production/SKILL.md`
2. `references/pack-handoff.md` when the input is a marketing-pack handoff
3. `references/editable-slots.md` before filling a template
4. `assets/templates/size-kit.yaml` for the template id and pixel size

## Rules that do not change per host

- Do not write marketing-pack copy or claim the cloud pack document is complete.
- Do not link, fetch, or redistribute a private design file.
- Do not redraw a supplied logo, and do not put a logo in a product-UI slot.
- Do not invent metrics, testimonials, partner marks, or product UI.
- A storyboard still is not an MP4. Encode only when the user authorizes it.
- If Playwright is missing, deliver filled HTML and mark the PNG `blocked`. Do not call that HTML delivered media.

## Validate

From the repository root:

```bash
python3 scripts/validate_package.py
```
