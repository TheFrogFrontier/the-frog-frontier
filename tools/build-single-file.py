"""
Inline every font and image into index.html, producing one portable file.

Why bother: a single file opens correctly from a desktop, an email
attachment, a USB stick or a preview pane. A folder only works when the
whole folder travels together and is served over http, which is the thing
that went wrong the first time.

    python3 build-single-file.py

Reads  public/index.html (+ public/assets, public/fonts)
Writes index-standalone.html at the top of the repo.

Run it from anywhere:  python3 tools/build-single-file.py
"""

import base64, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'public'          # the folder Cloudflare serves
MIME = {'.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.ico': 'image/x-icon',
        '.svg': 'image/svg+xml'}


def data_uri(rel):
    f = SITE / rel
    if not f.exists():
        print('  missing, left as-is: %s' % rel, file=sys.stderr)
        return None
    b64 = base64.b64encode(f.read_bytes()).decode()
    return 'data:%s;base64,%s' % (MIME.get(f.suffix.lower(), 'application/octet-stream'), b64)


def main():
    html = (SITE / 'index.html').read_text()

    # preload links point at files that will no longer exist as files
    html = re.sub(r'\n\s*<link rel="preload"[^>]*>', '', html)

    refs = set(re.findall(r"""(?:src=|href=|url\()['"]?((?:assets|fonts)/[^'")\s>]+)""", html))
    swapped = 0
    for rel in sorted(refs, key=len, reverse=True):
        uri = data_uri(rel)
        if uri:
            html = html.replace(rel, uri)
            swapped += 1

    out = ROOT / 'index-standalone.html'
    out.write_text(html)
    print('inlined %d files -> %s (%.0f KB)' % (swapped, out.name, out.stat().st_size / 1024))


if __name__ == '__main__':
    main()
