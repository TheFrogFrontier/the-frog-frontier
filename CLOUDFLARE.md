# Putting the site on Cloudflare Pages

You have Git and a domain, so use the **Git integration** rather than uploading
files. Push a change, Cloudflare rebuilds and deploys it. No zipping, and every
deploy is tied to a commit you can roll back to.

---

## How the repo is laid out

```
public/          <- everything Cloudflare serves. This is the site.
  index.html
  site.css
  assets/
  fonts/
  check-your-inbox/
  _headers
  _redirects
tools/           <- never published: scripts, source drawings, the brand kit
index-standalone.html    <- the portable single-file copy
README.md
CLOUDFLARE.md
```

The split matters. Cloudflare is pointed at `public/`, so the scripts, the README
and the brand kit stay in version control without being served to the public.

---

## 1. Push it

If you're starting a fresh repo, create an empty one on GitHub (no README, no
.gitignore, this folder already has both), then:

```
cd the-frog-frontier
git remote add origin git@github.com:YOUR-USERNAME/the-frog-frontier.git
git push -u origin main
```

If you'd rather use an existing repo, copy these files in and commit as usual.

GitLab works identically. Cloudflare supports both.

---

## 2. Connect Cloudflare

**dash.cloudflare.com** -> **Workers & Pages** -> **Create application** ->
**Pages** -> **Connect to Git**.

Authorise GitHub, pick the repository, then set:

| Setting | Value |
|---|---|
| Framework preset | **None** |
| Build command | *leave empty* |
| Build output directory | **`public`** |
| Production branch | `main` |

That's the whole configuration. There is no build step. The files are already
what gets served, and Cloudflare just publishes the `public` folder.

Press **Save and Deploy**. You'll be live at `the-frog-frontier.pages.dev`
within a minute or so.

**Getting the output directory wrong is the one thing that will bite you.** Leave
it blank and Cloudflare serves the repo root, finds no `index.html` at the top
level, and you get a 404 on a deploy that otherwise reports success.

---

## 3. Point your domain at it

Pages project -> **Custom domains** -> **Set up a domain**.

**If the domain's nameservers are already on Cloudflare**, type it in and
Cloudflare creates the DNS record itself. Under a minute.

**If it's still at your registrar**, Cloudflare gives you a CNAME to add there.
Either add it, or move the nameservers to Cloudflare and let it manage the whole
zone, which is worth doing if you'll use Cloudflare for anything else.

Add both `thefrogfrontier.com` and `www.thefrogfrontier.com`, then redirect one
to the other so you aren't splitting search ranking across two addresses.
Certificates are automatic and free.

---

## Day to day

```
# edit public/index.html
git add -A
git commit -m "Update handbook price"
git push
```

Live in about a minute. Every push to `main` deploys.

Every push to any *other* branch gets its own preview URL, which is a good way
to try something before it goes public: branch, push, open the preview link
Cloudflare posts, merge when you're happy.

If a deploy goes wrong: **Deployments** -> find the previous one ->
**Rollback**. Two clicks, no Git surgery.

---

## Keeping the standalone copy in step

`index-standalone.html` is the everything-inlined version, useful for emailing
or opening off a USB stick. It does not update itself. After editing
`public/index.html`:

```
python3 tools/build-single-file.py
```

It isn't served by the site, so a stale one breaks nothing, but it's confusing
later if it disagrees with the live page.

---

## About `_headers`

Cloudflare reads `public/_headers` automatically. Images and fonts get a week of
browser caching; the pages and `site.css` are always revalidated, so text, price
and design edits appear immediately.

The trade-off: **replacing an image means returning visitors may see the old one
for up to a week.** Rename it (`frog-teal-2.webp`, updating the reference in
`index.html`) to push it through straight away.

There is no Content-Security-Policy header. It's the usual next step, but
written casually it blocks the YouTube embeds. Worth doing properly later.

---

## What a static host can't do

**The email form** still opens the visitor's mail app. Cloudflare serves files;
it doesn't process form posts. Point it at Kit or Buttondown as described in the
main README. Cloudflare Pages Functions could handle it, but
that's a lot of machinery for something a mailing-list provider does free.

**Checkout** happens on Etsy. The site only links to the listings, so it needs
nothing from the host.
