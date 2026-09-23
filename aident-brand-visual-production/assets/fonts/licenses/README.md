# Font licenses

Default faces are packaged so HTML export renders the same on another machine. They stay replaceable.

## Outfit

- Primary marketing type in the Visual-design templates.
- File: `../outfit/Outfit-VariableFont_wght.ttf`
- License: [Outfit-OFL.txt](Outfit-OFL.txt) (SIL OFL 1.1)
- Upstream: https://github.com/Outfitio/Outfit-Fonts

## Smiley Sans

- Display / Chinese accent seen on some posters.
- File: `../smiley-sans/SmileySans-Oblique.ttf.woff2`
- License: [SmileySans-OFL.txt](SmileySans-OFL.txt) (SIL OFL 1.1). Reserved font names: Smiley, 得意黑.
- Upstream: https://github.com/atelier-anchor/smiley-sans

## Noto Sans SC

- Chinese body. Latin stays on Outfit because Outfit is listed first in `--font-primary`.
- File: `../noto-sans-sc/NotoSansSC-Variable.ttf`
- License: [NotoSansSC-OFL.txt](NotoSansSC-OFL.txt) (SIL OFL 1.1)
- Upstream: https://github.com/notofonts/noto-cjk

## Override path

1. Payload `fonts.primary` / `fonts.display` rewrites `--font-primary` / `--font-display`.
2. Replace `fonts.css` `@font-face` src with another licensed file and keep the license text in this folder.
3. A binary under `assets/fonts/` without a license file fails `scripts/validate_package.py`.
