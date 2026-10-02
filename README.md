# The Frog Frontier — website

One page, no build step, no framework. Open `index.html` in a browser to preview.
Everything you need to edit is marked with a comment in the file.

```
the-frog-frontier/
├── public/                 everything Cloudflare serves
│   ├── index.html          the editable source
│   ├── assets/             logo, frog-head mark, foliage, favicons
│   ├── fonts/              Special Elite, Poppins, Caveat (+ licenses)
│   └── _headers            caching rules, read by Cloudflare
├── tools/                  never published
│   ├── build-single-file.py    regenerates index-standalone.html
│   ├── process-background.py   converts a drawing into the background
│   └── source-drawing.jpg      the original artwork
├── index-standalone.html   one file, everything inlined
├── CLOUDFLARE.md           deploying and the custom domain
└── README.md
```

## Which file do I use?

**`index-standalone.html`** has every font and image inlined, so it is genuinely
one file. Double-click it and it works — no server, no folder, nothing to lose
in a download. This is the one to upload, email to yourself, or hand to anyone.

**`public/index.html`** is the same page, but pulling images and fonts from the folders
next to it. It's easier to edit. Browsers block font files loaded over `file://`,
so opening this one straight off your desktop shows the right layout in the wrong
typefaces — that's the browser being strict, not a broken file.

**Edit `public/index.html`, then run `python3 tools/build-single-file.py`** to regenerate the
standalone copy. Or just edit the standalone directly; the markup is identical,
there are simply long base64 strings where the images are.

The palette is sampled directly from your logo drawing — the paper, the graphite,
and the green of the typed wordmark. If you ever change the drawing, resample
rather than guessing.

## The background

`public/assets/foliage.webp` is the tropical pencil drawing, converted to sit behind
text. The source is kept alongside it as `tools/source-drawing.jpg` so you can
reprocess at a different strength without regenerating anything.

```
python3 tools/process-background.py
python3 tools/process-background.py --strength 0.30
```

Then `python3 tools/build-single-file.py` to rebuild the standalone copy.

The script does three things the drawing needs before it can be a background:

**Swaps the paper.** It rebuilds the image as "amount of ink" rather than
colour, then lays that ink onto the page colour. That's why there's no visible
seam where the artwork meets the page, and it's the same trick that makes the
logo float.

**Cuts the noise.** JPEG compression leaves a 1-2% haze that would turn the
empty middle into faint grey mottling. A deadband removes it.

**Lightens it a lot.** `--strength` defaults to 0.38. Below 0.25 it stops
reading; above 0.45 it starts competing with the text. If you change it, note
that the footer's contrast fix is tuned to the current value.

It's fixed in place, anchored to the bottom of the window at full width, which
holds up at 320px and at 2560px where `cover` would zoom into the empty middle
on a phone.

### One thing to watch

Nothing muted enough to read as secondary text survives the darkest leaves.
Over those, mid-grey lands around 2.6:1 where 4.5:1 is the readable floor. Two
places were affected and both are fixed: the footer sits on a 78% paper wash,
and the short notes in the hero use full-strength ink instead of grey.

If you swap in a different drawing, that's the thing to recheck. A busier one,
or one with denser shading in the upper half, may need the footer treatment
extended to other sections.
## 1. Shopify Starter

Starter is $5/month and does not include an online store or themes. What it gives you
is the Buy Button channel and Shopify's hosted checkout, which is exactly what this
site uses: your product cards are written here, and Shopify only supplies the button
and the checkout window.

The trade-off to know going in: **Starter charges 5% + 30¢ on each online sale** on top
of card processing. On an $8.50 handbook that's about 73¢. Basic (currently $39/mo)
drops that surcharge, so somewhere north of roughly 100 sales a month the higher plan
gets cheaper. Run your own numbers before assuming.

### Setting it up

1. In Shopify admin, add each product. Set it to **digital** — untick "This is a
   physical product" so no shipping is requested at checkout.
2. Add the **Buy Button** sales channel.
3. Go to **Settings → Apps and sales channels → Develop apps**, create an app, and
   enable the **Storefront API**. Copy the storefront access token.
4. Get each product's ID from its admin URL — the long number at the end of
   `.../products/8123456789012`.

### Filling it in

Near the bottom of `index.html`:

```js
var SHOPIFY_CONFIG = {
  domain: 'your-store.myshopify.com',
  storefrontAccessToken: 'paste-the-token-here',
  moneyFormat: '${{amount}}'
};
```

Then replace each `data-shopify-id="PRODUCT_ID_..."` with the real number. Until you
do, those slots show a dashed "Checkout not connected yet" box and nothing loads from
Shopify.

The storefront token is **read-only and designed to sit in public page code** — it's
fine that anyone can view it. Never put an Admin API key here; that one is not safe in
a browser.

### Two things that will bite you

**Don't use variants for Letter vs A4.** The buttons are configured to show no option
selector, because a two-line dropdown wrecks the card layout. Put every format in one
zip and sell it as a single product, which is what buyers want anyway.

**Delivery needs an app.** Shopify does not email files on its own. The free
**Digital Downloads** app by Shopify is the obvious choice, and Fileflare or Filemonk
are the usual paid alternatives with better deliverability and no file-size ceiling —
worth considering for STLs, which are chunky.

Shopify's own support has said apps install fine on Starter *except* ones that require
the online store channel. Digital Downloads delivers by email rather than through a
storefront page, so it should install — but I can't verify that from here, and it
decides whether this whole setup works. **Test it with a real $1 product and your own
card before you list anything.** If it won't install, the fallback is a delivery app
that works off order emails, or upgrading to Basic.

---

## 2. Videos

Find each `data-yt="VIDEO_ID_1"` and replace it with the 11-character YouTube ID — the
part after `watch?v=`. Update the `aria-label`, the heading and the blurb to match.

Nothing is requested from Google until someone presses play, and playback then uses
`youtube-nocookie.com`. That keeps the page fast and means a visitor who scrolls past
isn't tracked. The thumbnail is pulled from YouTube once you've put a real ID in; with
a placeholder ID it quietly falls back to a plain panel with a play button.

To add a fourth video, copy one `<li class="film">` block. The grid reflows on its own.

---

## 3. Email form

Find `FORM_ACTION`. Right now the form opens the visitor's mail app, which works but is
clumsy. Point the `action` at Kit, Buttondown or Mailchimp instead — all three give you
a form URL to paste in and have a free tier at your list size.

Also replace `hello@thefrogfrontier.com` (3 places) with a real address.

---

## 4. Social preview

Find `OG_IMAGE` and replace `YOUR-DOMAIN.com` with your real domain. Link
previews on Facebook, iMessage and Slack need an absolute URL — a relative path
silently shows nothing.

---

## 5. Hosting

It's static, so hosting is free. Netlify Drop (drag the folder onto the page),
Cloudflare Pages, or GitHub Pages all work, then point your domain at whichever you pick.

Upload the whole folder. If you'd rather not think about it, upload
`index-standalone.html` on its own and rename it `index.html` — it has no
dependencies at all. The folder version is marginally better for repeat visitors
because the browser can cache the fonts separately, but at this size it's a
rounding error.

---

## Notes

- Prices are typed into the HTML. When you change one in Shopify, change it here too —
  a stale number is worse than no number.
- To move a product from "In the works" to live: swap the tag for
  `<span class="tag tag--now">Available</span>`, add a `<span class="price">`, and
  replace the "Notify me" link with a `<div class="buy" data-shopify-id="...">`.
- Colors, type and spacing live in the `:root` block at the top of the stylesheet.
- Fonts are subsetted to Latin characters, so the whole set is about 100 KB instead
  of 1 MB. Caveat is cut down further, to the handful of characters the two
  handwritten sample lines use. If you ever need accented or non-Latin text, they'll
  need regenerating.
- Contrast meets WCAG AA throughout, the layout holds down to 320px, keyboard focus is
  visible, and motion is limited to what responds to a click.
