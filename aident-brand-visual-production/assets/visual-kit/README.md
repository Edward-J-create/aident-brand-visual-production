# Basic visual kit

Packaged structure for marketing frames. These pieces are the template, not a client brand.

| Piece | Where | How to replace |
|---|---|---|
| Poster field, footer, bloom, URL fill | `assets/templates/poster-specs.json` and each poster HTML file | Use the matching template. Recolor by replacing that type's bloom SVG. Do not paint a new palette in CSS circles. |
| Bloom | `backgrounds/poster-*-bloom.svg` | Transparent outside the blurred ellipse. Colors and blur are in the file. |
| Grain | `materials/grain-overlay.svg` | Stack it with `mix-blend-mode: overlay` and `opacity: 0.25`, as in `poster-kit.css`. Do not merge it into the field. |
| Media shell | Empty `[data-slot="ui-screenshot"]` or `[data-slot="icon"]` | A supplied screenshot, an authorized capture, or a supplied icon. The dashed shell is not a place for the logo. |
| Generic frame | `shells/media-frame.svg` | Optional starter you may place in a media slot. It is not a logo and not product UI. |
| Logo | `[data-slot="logo"]` | Supplied SVG/PNG only, in the footer or a logo template. Never draw a real logo into this kit. |

Prefer SVG. Use lossless transparent WebP only when the material is a photo texture. Do not add partner marks, product screenshots, or client photography to this folder. Those belong in the job payload.
