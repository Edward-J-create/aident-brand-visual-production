# Video production kit

## What v0.1 delivers by default

| Artifact | Required for video-kit/both? | Is final video? |
|---|---|---|
| `docs/storyboard.md` | Yes | **No** |
| `docs/shot-list.yaml` | Yes | **No** |
| Poster / cover still (`tpl-video-cover` or brief poster_frame) | Yes when brief asks | Still image only |
| Frame stills from the `tpl-video-frame-*` layouts in `video-frame-specs.json` | One still per beat that needs a frame | **No** |
| MP4/MOV master/cutdowns | Only if user authorized + feasible | Yes, after QA |

## Shot source_type labels (required)

`supplied` | `capture-required` | `licensed-stock` | `generated-concept` | `motion-design`

Unresolved `capture-required` → asset status `blocked`, not fake footage.

## Encode gate

Authorize separately. Prefer host tools (Hyperframes, Remotion, editor handoff, Fal video, etc.) **after** contract freeze — no vendor lock. Storyboard ≠ MP4.
