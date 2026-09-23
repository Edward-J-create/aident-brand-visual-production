# HTML layout templates

Fixed-canvas HTML templates matching `../size-kit.yaml`.

| File | Template ID | Size |
|---|---|---|
| `feature-poster.html` | `tpl-feature-poster` | 1242×1660 |
| `poster-shot.html` | `tpl-poster-shot` | 1242×1660 |
| `poster-stage.html` | `tpl-poster-stage` | 1242×1660 |
| `poster-cluster.html` | `tpl-poster-cluster` | 1242×1660 |
| `poster-grid.html` | `tpl-poster-grid` | 1242×1660 |
| `poster-table.html` | `tpl-poster-table` | 1242×1660 |
| `banner.html` | `tpl-banner` | 1270×760 |
| `video-cover.html` | `tpl-video-cover` | 1920×1080 |
| `profile-avatar.html` | `tpl-profile-avatar` | 400×400 |
| `x-banner.html` | `tpl-x-banner` | 2048×900 |
| `youtube-banner.html` | `tpl-youtube-banner` | 2048×1152 |
| `linkedin-banner.html` | `tpl-linkedin-banner` | 2048×400 |
| `logo-mark.html` | `tpl-logo-mark` | 80×80 |
| `logo-lockup.html` | `tpl-logo-lockup` | hug×80 (~257–365) |
| `video-frame-title.html` | `tpl-video-frame-title` | 1920×1080 |
| `video-frame-logo.html` | `tpl-video-frame-logo` | 1920×1080 |
| `video-frame-caption.html` | `tpl-video-frame-caption` | 1920×1080 |
| `video-frame-ui.html` | `tpl-video-frame-ui` | 1920×1080 |
| `video-frame-stat.html` | `tpl-video-frame-stat` | 1920×1080 |
| `video-frame-chips.html` | `tpl-video-frame-chips` | 1920×1080 |
| `video-frame-label-row.html` | `tpl-video-frame-label-row` | 1920×1080 |
| `video-frame-endcard.html` | `tpl-video-frame-endcard` | 1920×1080 |
| `video-frame-message.html` | `tpl-video-frame-message` | 1920×1080 |
| `video-frame-subtitle.html` | `tpl-video-frame-subtitle` | 1920×1080 |

Shared styles: `tokens.css`, `poster-kit.css`, `landscape-kit.css`, `video-frame-kit.css`. Tokens: `tokens.css` ↔ `../../tokens/tokens.json`.

Fill via `scripts/render_html_template.py` + a brand payload (see `examples/brand-payload.example.yaml`). Slot contract: `references/editable-slots.md`.

The ten `video-frame-*` files are storyboard stills, one layout per beat. `tpl-video-frame-16x9` is an alias of `tpl-video-frame-title`. Pair them with `../storyboard.md`. A still is not an MP4. `video-frame-subtitle.html` exports with alpha.
