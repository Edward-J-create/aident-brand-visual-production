# Quality gates

## P0 (must pass for `delivered`)

- Exact export WxH (or duration/resolution/fps for video) matches brief + size-kit
- File opens; MIME/bytes recorded; sha256 when available
- Copy matches approved exact text / copy IDs
- Every requested slot exists in the selected template; no binding is silently ignored
- Feature poster includes the approved lower-right URL and a supplied, replaceable middle visual
- Poster headline renders in no more than two total lines; no truncation, ellipsis, or third line
- When a second line is approved as the emphasis, it is bound to `headline-accent` and uses the template's brighter gradient instead of inheriting the first-line treatment
- Footer URL remains Outfit 400; short domains retain 56px and long display domains fit the reserved width without clipping or competing with the headline
- Logo is supplied file placement — not generative redraw
- Approved light/dark logo variant is readable on its actual surface; no ad-hoc recolor
- No broken-image glyphs, missing local image references, or instructional slot labels in result media
- No fabricated UI/metrics/testimonials/partner marks
- Video: every shot has `source_type`; storyboard not labeled as final video
- Rights_status and approval_owner resolved or status stays `blocked`
- Deviations listed explicitly (empty list if none)

## P1 (fix or document)

- Safe-area clearance vs schematic zones
- Contrast / readability for critical type
- One dominant communication job and focal point per still/storyboard frame
- Screenshot/icon-led templates contain the approved focal asset at useful visual scale; empty scaffolds remain `blocked`
- Captions present when brief requires
- Alt text for stills
- Filename convention followed

## Evidence

Record under `return/.../qa/` and in `return-manifest.yaml` per asset.
