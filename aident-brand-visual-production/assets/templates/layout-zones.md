# Layout zones

Zone names match HTML `data-slot` regions under `assets/templates/html/`. Boxes below are the packaged template frames. Sample logos, product UI, and decorative art are slots, not baked artwork.

Safe margin default: ~6% of the shorter side (`--safe-margin-ratio`) unless brief overrides.

## `tpl-feature-poster` and the other 1242×1660 posters

Colors, boxes, bloom files, and the grain blend mode are in `poster-specs.json`. Shared chrome is `html/poster-kit.css`. Each HTML file states that type's field, title box, and middle box.

Every poster keeps the same footer: logo at (68, 1520) 409×75, URL at the right, Outfit 56. The grain layer is `visual-kit/materials/grain-overlay.svg`, placed at (−46, −87) 1335×2418, **opacity 0.25, blend mode overlay**. Do not flatten that blend into the background.

The middle slot is a product UI screenshot or a supplied icon. It is never the footer logo.

| Template | Type | Middle |
|---|---|---|
| `tpl-feature-poster` | ui | screenshot (128, 657) 994×623, field `#111114` with top radius 80, bloom `#606AF7 → #1992DD → #11C5B0` |
| `tpl-poster-shot` | shot | screenshot (118, 649) 1015×643 on canvas `#111114` plus wash `#1DDEC8 → #25ACFF → #4D59FF` at 0.6 |
| `tpl-poster-stage` | stage | screenshot (191, 859) 860×515, bloom `#15FFEF → #7B4FFF` |
| `tpl-poster-cluster` | cluster | supplied visual (192, 678) 859×384, bloom `#7B4FFF → #15FFEF` |
| `tpl-poster-grid` | icon-side | icon (323, 669) 150×150. The 1640×1064 plate at (135, 753) is fixed decoration, not the slot |
| `tpl-poster-table` | icon-center | icon (541, 652) 150×150. The 974×1240 plate at (134, 723) is fixed decoration, not the slot |

Footer behind the logo, except on `tpl-poster-shot`, is `linear-gradient(90deg, #E7FFFE, #F2F9FF, #EFE7FF)`. URL fill on that footer is `#039987 → #0281D0 → #4B56F8`. The shot poster URL fill is `#9AFFF8 → #DAF4FF → #CAB7FF`.

```
+----------------------------------+
|  headline + subcopy              |
|                                  |
|  [screenshot or icon — not logo] |
|                                  |
|  logo                  url       |
+----------------------------------+
```

## `tpl-banner` — 1270×760 → `html/banner.html`

Logo at (504, 65) 262×48, inside the title frame. Headline at (85, 131) 1100×107. Stat row at (280, 277), shown only when the brief supplies the numbers. Art band from y=424 to the bottom edge (`data-slot=art-band`).

```
+------------------------------------------+
|              logo                        |
|            HEADLINE                      |
|         stat-a      stat-b               |
|            [art-band]                    |
+------------------------------------------+
```

## `tpl-video-cover` — 1920×1080 → `html/video-cover.html`

Logo at (683, 140) 555×80. Title at (488, 301) 945×292. UI at (416, 689) 1088×405. Icon cluster around (1511, 838).

```
+------------------------------------------+
|                 logo                     |
|               headline                   |
|            ui-screenshot                 |
+------------------------------------------+
```

## Social banners

Blur ellipses use the packaged three-orb kit, colored by tokens.

| Template | Logo | Title | UI |
|---|---|---|---|
| `tpl-x-banner` 2048×900 | (768, 143) 511×74 | (669, 246) 711×238 | (480, 551) 1088×405 |
| `tpl-youtube-banner` 2048×1152 | (830, 443) 389×56 | (738, 521) 573×188 | (480, 771) 1088×405 |
| `tpl-linkedin-banner` 2048×400 | (1487, 121) 462×67 | one row, headline + accent | none — the 400px strip has no UI slot |

## `tpl-profile-avatar` — 400×400 → `html/profile-avatar.html`

Mark slot is (90, 90) 220×220, the plain avatar in the design. The larger avatar frames include a ring or a star field, so their artwork boxes are bigger; this template has neither. Backdrop is `data-slot=decor`. 400×400 is the export canvas. Sample logo art is not copied.

## `tpl-logo-mark` / `tpl-logo-lockup`

`logo-mark.html` is an 80×80 canvas, artwork inset to 60×60 at (10, 10). It is the isolated mark for placements other than the poster footer (75×75) and the plain avatar (220×220). `logo-lockup.html` is height 80, max width 365, mark at (0, 0), `data-slot=wordmark` at (90, 16) 275×47. Place a supplied SVG/PNG in the mark slot. The wordmark is editable text. Never stretch. Never generative-redraw.

## Storyboard stills — 1920×1080

Boxes and materials are in `video-frame-specs.json`. Shared chrome is `html/video-frame-kit.css`. Pick the layout that matches the beat. `ui`, `stat`, and `chips` have no mesh. `tpl-video-frame-subtitle` is transparent and exports with alpha.

| Template | Field | What it holds |
|---|---|---|
| `tpl-video-frame-title` | mesh | Headline at (210, 380) 1500×240 |
| `tpl-video-frame-logo` | mesh | Lockup at (580, 462) 761×157 |
| `tpl-video-frame-caption` | mesh | Mark (855, 344) 210×210, caption (210, 620) 1500×96 |
| `tpl-video-frame-ui` | flat `#F0F8F1` | UI card (174, 214) 1600×1024, runs off the bottom; badge (875, 375) 170×170 |
| `tpl-video-frame-stat` | flat, faint tiles | Stat A (360, 311), stat B (1080, 436) |
| `tpl-video-frame-chips` | flat `#F0F8F1` | Mark (823, 198) 273×273, six icon slots in a rail (440, 516) 1040×210 |
| `tpl-video-frame-label-row` | wide mesh | Word, four labelled plates, word |
| `tpl-video-frame-endcard` | mesh + sparkles | Mark, lockup, optional CTA |
| `tpl-video-frame-message` | flat `#F4F6F2` | Prompt bubble + avatar |
| `tpl-video-frame-subtitle` | transparent | One subtitle line, alpha PNG |
