"""
Builds the free coloring-page download from the source drawings.

    python3 tools/build-coloring-pages.py

Reads   tools/coloring-src/*.jpg       (in filename order)
Writes  public/coloring-pages-f7k2q9/
          frog-frontier-coloring-pages-letter.pdf
          frog-frontier-coloring-pages-a4.pdf
          thumbs/page-1.webp ... page-N.webp

The source drawings are 1232x1600, which is only 144 dpi on a Letter page.
Line art survives an upscale well where photos don't: doubling the size and
then snapping near-white to white and near-black to black gives smooth,
crisp outlines at ~290 dpi instead of visible stair-steps on every curve.
"""

import io, pathlib
from PIL import Image
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'tools' / 'coloring-src'
OUT = ROOT / 'public' / 'coloring-pages-f7k2q9'
FONT = ROOT / 'tools' / 'SpecialElite-Regular.ttf'

GREEN = (40 / 255, 63 / 255, 9 / 255)
GREY = (0.42, 0.42, 0.40)


def clean(im):
    """2x upscale, then a levels curve that clears JPEG haze from the paper
    and firms up the line, keeping the anti-aliased edge in between."""
    g = im.convert('L')
    g = g.resize((g.width * 2, g.height * 2), Image.LANCZOS)
    a = np.asarray(g).astype(np.float32)
    lo, hi = 40.0, 225.0
    a = np.clip((a - lo) / (hi - lo), 0, 1) * 255
    return Image.fromarray(a.astype(np.uint8), 'L')


def build_pdf(pages, size, path, label):
    W, H = size
    c = canvas.Canvas(str(path), pagesize=size)
    c.setTitle('The Frog Frontier: Coloring Pages')
    c.setAuthor('The Frog Frontier')
    side, top, bottom = 0.4 * inch, 0.4 * inch, 0.7 * inch
    boxw, boxh = W - 2 * side, H - top - bottom
    for i, im in enumerate(pages, 1):
        r = im.width / im.height
        w, h = (boxw, boxw / r) if boxw / r <= boxh else (boxh * r, boxh)
        x, y = (W - w) / 2, bottom + (boxh - h) / 2
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=90, optimize=True)
        buf.seek(0)
        c.drawImage(ImageReader(buf), x, y, w, h)
        c.setFont('SpecialElite', 10)
        c.setFillColorRGB(*GREEN)
        c.drawCentredString(W / 2, 0.42 * inch, 'The Frog Frontier  ·  thefrogfrontier.com')
        c.setFont('SpecialElite', 7.5)
        c.setFillColorRGB(*GREY)
        c.drawCentredString(W / 2, 0.26 * inch,
                            'Free for personal and classroom use. Please don’t resell or redistribute.')
        c.drawRightString(W - side, 0.26 * inch, '%d / %d' % (i, len(pages)))
        c.showPage()
    c.save()
    print('%-44s %d pages  %.1f MB  (%s)' % (path.name, len(pages), path.stat().st_size / 1e6, label))


def main():
    pdfmetrics.registerFont(TTFont('SpecialElite', str(FONT)))
    srcs = sorted(SRC.glob('*.jpg')) + sorted(SRC.glob('*.png'))
    if not srcs:
        raise SystemExit('No drawings in %s' % SRC)
    pages = [clean(Image.open(p)) for p in srcs]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'thumbs').mkdir(exist_ok=True)
    build_pdf(pages, letter, OUT / 'frog-frontier-coloring-pages-letter.pdf', 'US Letter')
    build_pdf(pages, A4, OUT / 'frog-frontier-coloring-pages-a4.pdf', 'A4')

    for i, im in enumerate(pages, 1):
        t = im.copy()
        t.thumbnail((520, 680), Image.LANCZOS)
        t.save(OUT / 'thumbs' / ('page-%d.webp' % i), quality=80, method=6)
    print('thumbnails: %d' % len(pages))


if __name__ == '__main__':
    main()
