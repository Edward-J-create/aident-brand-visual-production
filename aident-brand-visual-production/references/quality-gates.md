# Quality gates

## P0 (must pass for `delivered`)

- Exact export WxH (or duration/resolution/fps for video) matches brief + size-kit
- File opens; MIME/bytes recorded; sha256 when available
- Copy matches approved exact text / copy IDs
- Logo is supplied file placement — not generative redraw
- No fabricated UI/metrics/testimonials/partner marks
- Video: every shot has `source_type`; storyboard not labeled as final video
- Rights_status and approval_owner resolved or status stays `blocked`
- Deviations listed explicitly (empty list if none)

## P1 (fix or document)

- Safe-area clearance vs schematic zones
- Contrast / readability for critical type
- Captions present when brief requires
- Alt text for stills
- Filename convention followed

## Evidence

Record under `return/.../qa/` and in `return-manifest.yaml` per asset.
