# The Frog Frontier

A small shop for frog people. It started with printable frog-care sheets and is adding stitch markers shaped like frogs. This system is the shop's look as of November 2026: a risograph print style in four inks on cream paper.

> Small goods for frog people, printed in four loud inks.

To load the fonts:

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;600;700&family=Sriracha&family=Neucha&display=swap">
```

## The idea in one paragraph

Everything looks printed on a risograph: a few flat, translucent inks laid one over another on uncoated cream paper. Where two inks overlap they mix into a third color. Shapes are soft and round. There is a little grain and the layers sit very slightly out of line. Nothing has a gradient, a glow or a soft shadow.

## Voice

- Plain, warm and a little dry. A field guide written by someone who likes a joke.
- Short sentences. American spelling. Sentence case for headings; only the shop name is uppercase.
- One playful line per page is enough: "Caution: live stitch markers", "Less frogging. More knitting."
- Name frogs properly: common name first, Latin name after in the script face.
- "Frogging" is knitters' slang for ripping out work. The pun is welcome on knitting pages and nowhere else.

## Color

Four inks plus paper. Proportions on a typical page: paper about 60%, yellow 15%, teal and ink 15%, green 7%, pink 3%.

| Token | Role |
|---|---|
| `paper` | The page. Never pure white. |
| `paper-deep` | Cards and panels. |
| `ink` | All text under 24px, buttons, borders. |
| `teal` | Headings 24px and up, the frog, line art. |
| `yellow` | Big discs. The brand's largest color after paper. |
| `green` | Leaves. |
| `pink` | The accent, used small. |

Rules:

- Text is `ink` or `teal` only. `teal` on `paper` is about 4:1, so it is for 24px and larger; `ink` on `paper` is about 6.7:1 and is safe at any size.
- `yellow`, `green` and `pink` are never text colors and never carry meaning by themselves.
- Overlaps are made by blending, not by picking a new color: set `mix-blend-mode: multiply` on each ink shape inside a wrapper with `isolation: isolate`. The `over-orange`, `over-green` and `over-navy` tokens exist only as flat fallbacks.
- There is one theme. A dark mode would break the printed-on-paper idea; do not add one.

## Type

- **Fredoka** for almost everything. Bold for the name and headings, Regular or Medium for text.
- **Sriracha** for short asides: "Est. 2026", Latin names, a note under a product name.
- **Neucha** for figure labels and anything that should look hand-lettered. A few words at most.
- The styles are `display`, `h1`, `h2`, `h3`, `body`, `small`, `label`, `script` and `hand`. Keep running text to about 65 characters a line.

## Shapes and layout

- Discs are the main shape (`RisoDisc`). Pills for buttons and bars. Cards use `radius-md`.
- The logo is always the teal frog on a large yellow disc with a smaller pink disc overlapping the lower right.
- Balance compositions left and right, as the `Hero` does: frog on one side, leaves on the other, the name between.
- Depth comes only from `offset-pink` or `offset-yellow`: a hard, unblurred offset. No soft shadows.
- Leaves come in from the edges and may be cropped by them. Keep them off body text.
- Spacing steps are `space-1` to `space-16`. Sections are `space-16` apart on desktop and `space-12` on phones.

## The print effect

```css
.ff-riso { isolation: isolate; }
.ff-riso > * { mix-blend-mode: multiply; }   /* inks mix where they overlap */
.ff-grain::after { background: url(assets/Texture/riso-grain-256.png) 0 0 / 128px 128px; }
```

Offset one ink layer by 2 to 3px from the others if you want the out-of-register look. Keep text perfectly registered.

## Components

`Hero`, `SectionTitle`, `Button`, `ProductCard`, `RisoDisc` and `Stamp`. They are plain HTML and CSS; the classes are in `components/bundle.css` and start with `ff-`. Each has a README saying what you provide.

## Assets

- `assets/Logo/`: the teal frog and the original pencil drawing.
- `assets/Leaves/`: monstera, frond, banana leaf and a pink heart leaf.
- `assets/Texture/`: the grain tile.
- `assets/Reference/`: the Etsy banner and icon, and the product packet, as flat images.

## Rebuilding the site with this

1. Set the page ground to `paper` and all text to `ink`. Load the three fonts.
2. Put the `Hero` at the top of the home page.
3. Give each section a `SectionTitle`, and list products with `ProductCard`.
4. Use `Button` for every action. One primary per view.
5. Add discs and leaves last, as decoration behind and beside content, never under text.
6. Check every page on a phone: discs and leaves shrink or drop away before text does.

## Do not

- No gradients, glows, soft shadows or glassy effects.
- No pure white backgrounds and no dark mode.
- No new colors. If something needs emphasis, use size, a pink bar or a `Stamp`.
- No pink or green text. No text on pink.
- Do not redraw or recolor the frog.

## Open points

- The product line is not settled. The examples use stitch markers, but nothing in the system depends on them.
- Product photography does not exist yet; `ProductCard` shows a leaf as a stand-in.
- The earlier pencil-and-typewriter look (Special Elite, graphite frog) is retired from the site. It survives only as the source drawing for the logo.
