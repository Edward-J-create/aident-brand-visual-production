# Reference coverage

Checked against the installed package. Baselines are capability references, not layouts to copy.

| Source | What it contributes | This skill | Status |
|---|---|---|---|
| Internal design pass (not shipped) | Sizes and layer positions for cover, posters, banner, social banners, avatar, logo | Packaged HTML in `assets/templates/html/`. Source files are not in this skill. | met |
| Storyboard stills | 16:9 frame for beats named by a brief | Ten layouts in `video-frame-specs.json`. No private frame catalog is published. | met as templates |
| [aident-ppt-skill](https://github.com/Edward-J-create/aident-ppt-skill) | HTML templates, token overrides, replaceable copy/logo/images, bundled OFL fonts | Same granularity: HTML + `tokens.css` + brand payload slots. Outfit and Smiley Sans are bundled and overridable. Geometry stays this skill's size kit, not the PPT 1920×1080 deck. | met |
| [marketingskills image](https://github.com/coreyhaines31/marketingskills/tree/main/skills/image) | Choose generation vs template vs screenshot; keep type out of rasters; exact platform sizes | Template fill is the default. Generation is allowed only for non-text regions and only when authorized. | met for pack stills |
| [marketingskills video](https://github.com/coreyhaines31/marketingskills/tree/main/skills/video) | Programmatic HTML frames (Hyperframes), AI footage, avatars | Storyboard, shot list, and HTML frame stills ship by default. MP4 only after a separate encode authorization. No vendor lock. | met as a kit; encode stays host-owned |
| [marketingskills ad-creative](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative) | Ad copy variations and format taxonomy | Out of scope. Copy stays in aident-brand-marketing-pack. | out of scope |
| [anthropics/skills skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) | Progressive disclosure, scripts for deterministic steps, trigger description | `SKILL.md` workflow plus `scripts/render_html_template.py` and `scripts/validate_package.py`. | met |
| [anthropics/skills theme-factory](https://github.com/anthropics/skills/tree/main/skills/theme-factory) | Swappable color and font themes | One payload overrides colors and font stacks. No second theme gallery. | met as a mechanism |
| [anthropics/skills canvas-design](https://github.com/anthropics/skills/tree/main/skills/canvas-design) | Freeform poster philosophy | Not used. Frames come from the packaged size kit. | out of scope |
| [anthropics/skills brand-guidelines](https://github.com/anthropics/skills/tree/main/skills/brand-guidelines) | One frozen brand palette | Colors here are token defaults, not a client identity. | deliberately different |

## Still open

1. Fill the matching `video-frame-*` still once per beat named in a frozen video brief. Do not publish a private storyboard catalog.
2. Final MP4/MOV still needs an authorized renderer. A storyboard or HTML frame is not that file.
3. WebP compression and ad-size derivatives are not part of this pack. Masters stay at the packaged pixel sizes.
