"""
Turn a scanned or generated pencil drawing into the site background.

What it does, and why each step matters:

  1. Measures the drawing's own paper level, then rebuilds the image as
     "amount of ink" rather than "colour". This is what lets the artwork's
     paper be swapped for the site's paper exactly, so the background has
     no visible edge against the page.
  2. Applies a deadband, because JPEG noise sits at about 1-2% and would
     otherwise turn the empty middle into faint grey mottling.
  3. Composites that ink onto the page colour at a fraction of full
     strength. Backgrounds behind text need to be much lighter than they
     look right in isolation.
  4. Saves opaque WebP. Transparency would be the honest way to do this,
     but an alpha channel on a drawing this detailed costs roughly ten
     times the file size for a picture that looks identical on a page
     whose background colour is already known.

    python3 tools/process-background.py
    python3 tools/process-background.py --strength 0.30
    python3 tools/process-background.py some-other-drawing.jpg

Writes public/assets/foliage.webp.
"""

import argparse, pathlib, sys

try:
    from PIL import Image
    import numpy as np
except ImportError:
    sys.exit("Needs pillow and numpy:  pip install pillow numpy")

PAPER = (239, 238, 233)   # --paper, sampled from the logo drawing
INK = (74, 73, 68)        # the logo's graphite

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'public'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', nargs='?', default=str(pathlib.Path(__file__).resolve().parent / 'source-drawing.jpg'),
                    help='the drawing: jpg, png or webp (defaults to tools/source-drawing.jpg)')
    ap.add_argument('--strength', type=float, default=0.38,
                    help='0.2 is barely there, 0.5 starts competing with text (default 0.38)')
    ap.add_argument('--width', type=int, default=1800,
                    help='output width; below ~1600 looks soft on a desktop monitor')
    ap.add_argument('--quality', type=int, default=64)
    ap.add_argument('--out', default='assets/foliage.webp',
                    help='written inside public/')
    a = ap.parse_args()

    src = Image.open(a.source).convert('RGB')
    if src.width != a.width:
        src = src.resize((a.width, round(src.height * a.width / src.width)), Image.LANCZOS)

    arr = np.asarray(src).astype(np.float32)
    lum = arr.mean(2)

    # the 97th percentile, not the max: one stray white pixel would skew it
    paper_level = np.percentile(lum, 97)
    ink = np.clip((paper_level - lum) / paper_level, 0, 1)
    ink = np.clip((ink - 0.045) / (1 - 0.045), 0, 1)     # deadband out the noise

    k = (ink * a.strength)[..., None]
    out = np.array(PAPER, np.float32) * (1 - k) + np.array(INK, np.float32) * k

    dest = SITE / a.out
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out.round().astype(np.uint8)).save(dest, quality=a.quality, method=6)

    print('%s  %dx%d  %.0f KB  (strength %.2f)'
          % (a.out, src.width, src.height, dest.stat().st_size / 1024, a.strength))
    print('Now run:  python3 tools/build-single-file.py')


if __name__ == '__main__':
    main()
