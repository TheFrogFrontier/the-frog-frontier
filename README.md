# The Frog Frontier website

A small static site: no build step and no framework. Cloudflare Pages serves the
`public` folder as it is.

```
the-frog-frontier/
├── public/                      everything Cloudflare serves
│   ├── index.html               the home page
│   ├── site.css                 the whole design: brand tokens, components, layout
│   ├── check-your-inbox/        page shown right after someone signs up
│   ├── assets/                  frog, leaves, grain texture, icons, social image
│   ├── fonts/                   Fredoka, Sriracha, Neucha (+ their licenses)
│   ├── _headers                 caching and search-engine rules, read by Cloudflare
│   └── _redirects               sends the old coloring-pages link to the home page
├── tools/                       never published
│   ├── brand-kit/               the November 2026 brand kit, kept as the reference
│   └── build-single-file.py     regenerates index-standalone.html
├── index-standalone.html        the home page as one file, everything inlined
├── CLOUDFLARE.md                deploying and the custom domain
└── README.md
```

## The design

The site follows the brand kit in `tools/brand-kit/` (read its `README.md` first):
a risograph print look in four inks on cream paper.

- `public/site.css` starts with the kit's `tokens.css` and `components/bundle.css`,
  copied in unchanged, then adds the page layout. Change a brand color or font in
  the tokens at the top and it changes everywhere.
- Text is only ever `ink` or `teal`. Teal is for 24px and larger. Yellow, green and
  pink are never text colors, apart from the one pink Stamp.
- Overlapping inks mix because each shape uses `mix-blend-mode: multiply`. Don't
  swap that for a hand-picked color.
- No gradients, soft shadows, pure white or dark mode. Depth is the hard pink or
  yellow offset only.
- One Stamp per page at most. The home page uses its one on the signup panel.
- Fonts are served from `/fonts`, not Google's CDN, so the page doesn't depend on a
  third party. They are subsetted to Latin characters; accented or non-Latin text
  would need them regenerated.

### Product pictures

Each printable card shows its Etsy listing photo, saved square in `public/assets/`
as `printable-handbook.webp`, `-log`, `-labels`, `-kit` and `-bundle` (800 px). The
ornament card uses `ornaments-trio.webp`. Larger copies are in `tools/`. To change a
picture, replace the file under a new name and update the `<img>` in `index.html`,
because images are cached for a week.

## Editing content

Everything is in `public/index.html`.

**Printables.** Each printable is one `<li>` in the Printables section, with its name,
script note, description, price and Etsy link. Prices are typed into the page, so
when you change a price on Etsy, change it here too. The "instead of $15" and
"Save $3" lines on the two bundles are worked out from the single-item prices.

**3D files.** Both are marked "In the works". When one is ready, add a price and
swap its "Notify me" button for a "Buy on Etsy" button; a comment in the card shows
where.

**Handmade.** The Christmas Tree Frogs ornament set has its own section near the top,
with its price and Etsy link. When the season is over or the set sells out, delete
that `<section id="handmade">` and the "Handmade" link in the top bar, or swap in the
next handmade piece.

**Videos.** Each video is one `<li>` in the Videos section. To add one, copy the
existing block and put the 11-character YouTube ID (the part after `watch?v=`) in
both `data-yt` and the thumbnail address, then update the `aria-label`, heading and
blurb. The player only loads when someone presses play.

**Signup form.** Find `FORM_ACTION` and paste your mailing list's form address into
`data-list-action`. It works with Kit or Buttondown and detects which from the
address. Until then the form opens the visitor's mail app. In the mailing service,
set "after subscribing" to `https://thefrogfrontier.com/check-your-inbox/` and
"after confirming" to the home page, `https://thefrogfrontier.com/`.

**Email address.** `hello@thefrogfrontier.com` appears three times in
`index.html`; replace it if that isn't a real inbox.

## The standalone copy

`index-standalone.html` is the home page with the stylesheet, fonts and images
inlined, for emailing or opening straight off a computer. It does not update
itself. After editing the home page or `site.css`:

```
python3 tools/build-single-file.py
```
