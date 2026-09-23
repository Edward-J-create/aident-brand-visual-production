# Pack handoff (inbound + outbound)

Condensed from marketing-pack `production-handoff.md`, `original-media-delivery.md`, and brief schemas.

## Responsibility split

| Owner | Owns | Does not own |
|---|---|---|
| aident-brand-marketing-pack | Copy, taxonomy, frozen briefs, handoff authorization, return inspection, durable library + cloud doc | Rendering imagery, inventing footage, claiming script=video |
| This skill | Image exports, video kit docs, optional authorized encode, local QA, return package | Pack copy, cloud pack document, redrawing real logos |
| User | Approvals, rights, paid-execution authorization | — |

## Inbound (pack → production)

Require:

1. Handoff ID, date, brand, campaign, owner, approval owner
2. Frozen brief version + selected deliverable IDs
3. Approved copy IDs and **exact text**
4. Source asset paths/links, rights, required real captures
5. Master and variant specifications (bind to `size-kit.yaml` template IDs)
6. Editable-source and export requirements
7. Acceptance checklist + prohibited changes
8. Open blockers, optional creative latitude, return format

If approvals/rights/sources missing → return `blocked`; do not invent a frozen contract.

Mirror field shapes: `assets/visual-brief.schema.yaml`, `assets/video-brief.schema.yaml`.

## Outbound (production → pack)

Per asset return: output path, optional editable path, method/version, sources+rights, deviations, QA (MIME, bytes, sha256, dimensions or duration), status `in-production` | `blocked` | `delivered`.

Filename convention:

```text
{asset_id}__{WxH-or-dur}__{locale}.{ext}
```

Accepted result MIME: `image/png`, `image/jpeg`, `image/svg+xml`, `video/mp4`, `video/quicktime`.

Do **not** claim pack label `Original file — ready`. Only set `full_quality_verified` after local inspection.
