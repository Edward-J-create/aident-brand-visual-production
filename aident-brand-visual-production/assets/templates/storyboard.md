# Storyboard — {{handoff_id}} / {{master_asset_id}}

> **Status:** production input only. This document is **not** a final video (MP4/MOV).

| Field | Value |
|---|---|
| Handoff ID | |
| Brief version | |
| Duration | |
| Resolution | 1920×1080 (default master) |
| Aspect | 16:9 |
| Locale | |
| Poster frame | |

## Beats

| # | Timecode | Communication job | Frame template | Visual | On-screen copy IDs | Source type | Notes |
|---|---|---|---|---|---|---|
| 1 | 00:00– | | `tpl-video-frame-title` | | | | |
| 2 | | | | | | | |

Pick one `tpl-video-frame-*` id per beat from `video-frame-specs.json`. `tpl-video-frame-16x9` means the title card.

## Poster / cover stills

- [ ] Poster still exported at brief `poster_frame` (template `tpl-video-cover` or matching)
- [ ] Filename follows `{asset_id}__{WxH}__{locale}.ext`

## Encode gate

Final MP4/MOV only when: authorized by user, brief complete, capture-required shots resolved or waived, QA passed.

Encode status: `not-requested` | `blocked` | `in-production` | `delivered`
