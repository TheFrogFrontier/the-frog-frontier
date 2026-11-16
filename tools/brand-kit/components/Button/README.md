# Button
A pill button in ink with a hard pink offset behind it, like a second color printed slightly off.

- Classes: `ff-btn` (primary), add `ff-btn--ghost` for the secondary. Use on `<a>` or `<button>`.
- One primary per view. Labels are a verb and an object: "Shop the frogs", "Add to cart".
- The offset shrinks on hover and closes on press. Never blur it or swap it for a soft shadow.
- The fill is `ink`, not `teal`: paper text on teal fails contrast at 16px.
- You provide: the label and the link or click handler.
