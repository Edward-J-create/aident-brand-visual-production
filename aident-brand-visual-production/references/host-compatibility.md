# Host compatibility (renderers optional)

No hard vendor lock. Select a renderer **after** the handoff/brief is frozen and the user authorizes execution.

| Capability | Optional routes | Invariant |
|---|---|---|
| Still layout export | **HTML fill** (`render_html_template.py`) → Playwright/Chromium PNG, or the user's own design-tool export | Exact WxH from size-kit; filled HTML always emitted |
| Generative background | Fal or other authorized image APIs | Never sole source of critical type/logos |
| Video encode | Hyperframes, Remotion, NLE handoff, Fal video, Loadout-adjacent tools | Storyboard ≠ final; authorize paid runs |
| Fonts | Bundled Outfit and Smiley Sans, or a payload override | No unlicensed binary redistribution |
| Pack return | Local folder + YAML | Pack owns durable cloud ingest |

## Degradation

1. If no renderer is available → deliver complete briefs, storyboard/shot templates filled, and mark media `blocked` or `in-production` with next action.
2. Sizes always come from the packaged size kit. Do not invent alternate dimensions, and do not fetch a private design file to recover them.
3. If paid API unauthorized → do not call it; return blocker.

## HTML → PNG note

PNG export is **host-dependent**. If Playwright/Chromium is missing, the renderer still writes filled HTML + `EXPORT.md` and documents the export step. Do not hard-require a paid raster API.
