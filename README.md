# daughterofdirtandstars.com

Plain static site, hosted on GitHub Pages. No WordPress, no build step: what's in this repo is exactly what's served.

## Layout

- `index.html`: home page
- `<page-name>/index.html`: every other page and post (for example `about/index.html` is daughterofdirtandstars.com/about/)
- `images/`: all photos and logos
- `assets/css/styles.css`: the site's design (colors, fonts, layout)
- `assets/css/blocks.css`: base styles for page building blocks (columns, buttons, images)
- `assets/js/site.js`: mobile menu, writing filters, footer year
- `CNAME`: tells GitHub Pages to serve the site at daughterofdirtandstars.com

## Header photos

Each page sets its header photo near the top of its HTML:

```html
<style>:root{--gg-head:url("/images/mesa.webp")}</style>
```

Swap the file name to change the photo. The home page hero uses `--gg-hero`.

## Newsletter

Subscribe forms post straight to Mailchimp.
