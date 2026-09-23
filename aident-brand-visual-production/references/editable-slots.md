# Editable slots contract

HTML templates under `assets/templates/html/` are **structures**, not baked brand assets. All brand-variable content enters through slots + token overrides.

Granularity mirrors Edward's `aident-ppt-skill` (HTML layout + editable tokens + replaceable imagery/copy). Visual geometry comes from this skill's packaged size kit.

## Slot types

| Kind | How marked | Payload field | Rules |
|---|---|---|---|
| **Text** | `[data-slot="headline\|subcopy\|cta\|disclaimer\|title-tag"]` (often `contenteditable`) | `text.*` or `templates.<id>.text.*` | Exact approved copy from pack/brief. Never bake into background images. |
| **Image** | container or `<img data-slot="…">` | `images.*` or `templates.<id>.images.*` | `src` / `path` to supplied file. Logo slots place SVG/PNG only — **never** generative redraw. Preserve aspect ratio (`object-fit: contain`). |
| **Color** | CSS variables on `:root` | `colors.*` | Roles: `bg`, `surface`, `text`, `textSecondary`, `muted`, `accent`, `accentSoft`, `border` (+ aliases `background`/`foreground`). Injected as `#brand-token-overrides`. |
| **Font** | `--font-primary`, `--font-display` | `fonts.primary`, `fonts.display` | Default stacks name Outfit / optional Smiley Sans. Override with family name or full CSS stack. Optional local `@font-face` only with license — see `assets/fonts/licenses/README.md`. |

## Standard image slot names

| `data-slot` | Typical use |
|---|---|
| `logo` | Lockup or mark in marketing frames |
| `logo-mark` | 80×80 mark (avatar / mark template) |
| `logo-lockup` | Hug-width lockup (~257–365×80) |
| `hero` | Hero photo / product visual |
| `ui-screenshot` | Product UI capture |
| `product-art` | Product illustration / art |
| `icon` | Small iconography slot |
| `art-band` | Icon or integration art that bleeds off the light banner's bottom edge |
| `avatar` | Speaker or agent avatar beside a storyboard prompt bubble |
| `icon-a` … `icon-f` | One slot per tile in the chip rail (`tpl-video-frame-chips`, six) and the label row (`tpl-video-frame-label-row`, four). Each tile is its own slot so a brand fills the connectors it actually has. |

## Standard text slot names

| `data-slot` | Typical use |
|---|---|
| `headline` | Primary title |
| `subcopy` | Supporting body |
| `cta` | Call to action |
| `disclaimer` | Legal / fine print |
| `title-tag` | Document `<title>` |
| `url` | Footer URL on the feature poster |
| `wordmark` | Editable name beside the mark in `tpl-logo-lockup` |
| `kicker` | Small label on a storyboard frame |
| `metric-a` / `metric-a-label` | First banner metric, only when the brief supplies the number |
| `metric-b` / `metric-b-label` | Second banner metric, only when the brief supplies the number |
| `headline-accent` / `title-accent` | Second run of a two-tone headline. Leave empty for a single-tone title. |
| `stat-value-a` / `stat-label-a` | First stat pair on the light banner and `tpl-video-frame-stat`, only when the brief supplies the number |
| `stat-value-b` / `stat-label-b` | Second stat pair, same condition |
| `icon-label-a` … `icon-label-d` | Caption under each tile in `tpl-video-frame-label-row` |
| `subtitle` | Single subtitle line in `tpl-video-frame-subtitle` |

## Fail conditions

- Hard-coded client brand hex values inside shared template HTML/CSS (outside the poster kit colors in `poster-specs.json` / `poster-kit.css` and labeled defaults in `tokens.css` / `tokens.json`) → **FAIL**
- Generative redraw of a real logo into a logo slot → **FAIL**
- Logo, mark, or lockup placed in `ui-screenshot`, `hero`, `product-art`, or an icon plate → **FAIL**
- Poster background replaced by a flat `colors.bg` or ad-hoc circles → **FAIL**
- Grain layer flattened, or its blend mode changed away from `overlay` → **FAIL**. The opacity is per template (`0.25` on posters, `0.30` on the social banners); take it from `poster-specs.json` / `banner-specs.json`, and do not recolour `grain-overlay.svg` — its noise is centred on mid grey so `overlay` leaves the field untouched.
- A third-party product mark dropped into `icon-a` … `icon-f`, the chip rail, or `art-band` to imply an integration the brand has not shipped → **FAIL**. These tiles carry the brand's own connectors only.
- A mesh bloom added to `tpl-video-frame-ui`, `tpl-video-frame-stat`, or `tpl-video-frame-chips` → **FAIL**. Those three sit on a flat field in the design; only the frames listed with a `mesh` in `video-frame-specs.json` get one.
- `tpl-video-frame-subtitle` exported without an alpha channel → **FAIL**. It is an overlay meant to composite over another frame, not a finished still.
- Critical type only inside a raster with no editable text slot → **FAIL**
- Changing WxH for a known `tpl-*` ID away from `size-kit.yaml` → **FAIL**

## Fill + render

```bash
python scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster
# optional PNG when Playwright/Chromium exists:
python scripts/render_html_template.py \
  --template tpl-feature-poster \
  --payload examples/brand-payload.example.json \
  --out /tmp/abvp-out/feature-poster \
  --png
```

Changing the payload colors/text/images must not require editing the HTML structure files.
