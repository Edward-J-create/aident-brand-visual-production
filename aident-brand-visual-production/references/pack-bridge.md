# Marketing-pack bridge

Use this path when `aident-brand-marketing-pack` has frozen copy, source assets, and deliverable IDs and the user wants production to start immediately.

## Canonical handoff

The accepted shape is `assets/pack-handoff.schema.yaml`. It is intentionally additive to the upstream production-handoff contract:

- `approved_copy` stores exact text by stable copy ID;
- `source_assets` stores actual source path/URL, kind, and rights;
- every image deliverable binds a packaged `template_id` to `data-slot`s through `slot_bindings`;
- every video deliverable may carry renderable 1920×1080 storyboard `frames` plus a shot list;
- final MP4/MOV encode remains separately authorized.

`slot_bindings.text` values are copy IDs. `slot_bindings.images` values are source asset IDs. This keeps production deterministic and prevents the renderer from inventing copy, logos, screenshots, or claims.

For `tpl-feature-poster` and `tpl-feature-poster-zh`, bind approved `text.url` and a supplied `images.ui-screenshot` (or `hero`) middle visual. When the second headline line is an approved emphasis, give it a separate copy ID and bind it to `text.headline-accent`; this slot owns the brighter gradient. The bridge blocks the asset when the URL or middle visual is absent. Poster headline export is also blocked if approved copy cannot fit within two lines at the packaged minimum type size.

For compatibility with older handoffs, `primary_copy_id`, `supporting_copy_ids`, `logo_asset_ids`, and `product_ui_asset_ids` are accepted as narrow fallbacks. Prefer explicit slot bindings for all new handoffs.

## Fast path

Validate and scaffold without launching a browser:

```bash
python scripts/prepare_pack_run.py \
  --handoff examples/both-from-pack-handoff.yaml \
  --out /tmp/brand-production
```

Attempt batch PNG export when Playwright/Chromium is available:

```bash
python scripts/prepare_pack_run.py \
  --handoff examples/both-from-pack-handoff.yaml \
  --out /tmp/brand-production \
  --png
```

The script creates payloads, filled HTML, storyboard/shot-list documents, a return manifest, and optional PNGs. Automated inspection checks file identity and dimensions; it deliberately leaves exported assets `in-production` until an agent or reviewer opens the result and completes visual/brand QA. It never marks a video frame as a final video.

## Pack ingest

Return the whole generated handoff folder to `aident-brand-marketing-pack`. The pack workflow must:

1. compare outputs to the frozen acceptance checks;
2. obtain named-owner approval for subjective brand decisions;
3. register inspected originals in durable storage;
4. update the pack manifest and document;
5. set `Original file — ready` only after audience access is verified.

Do not store private Figma URLs or file keys in the public skill. Use Figma only as an authorized reference during template maintenance; package reusable geometry and original public assets instead.
