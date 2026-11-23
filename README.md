# palouselabs.com

Corporate website for Palouse Labs LLC.

Static HTML site, deployed via Cloudflare Pages with direct GitHub integration (auto-deploy on push to `main`). No build step.

## Files

- `index.html` — homepage (hero, about, contact)
- `privacy.html` — privacy policy (served at `/privacy`)
- `terms.html` — terms of service (served at `/terms`)
- `styles.css` — all styling
- `fonts/InterVariable.woff2` — self-hosted Inter variable font
- `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` — favicons
- `og.png` — Open Graph card image (1200&times;630)
- `robots.txt`, `sitemap.xml`

## Local preview

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Regenerating images

```sh
python3 scripts/generate_images.py
```

Regenerates `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, and `og.png` from the Inter font. Requires Pillow (`pip install pillow`).
