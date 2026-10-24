# Pictograms

Hand-drawn SVG pictograms for the app's words, written as Python code. They replace the emoji in
`logo/Vocabulary/structure.json` (not wired into the app yet).

```sh
python3 pictograms/build.py
```

writes `svg/<word id>.svg` (style 1), `svg-v2/` (style 2: the same drawings, thinner line, small dot eyes, small
mouth, no blush, narrower body, see `kit.STYLE`) and `svg-mulberry/` (Mulberry Symbols from `mulberry/svg`,
our style 2 where Mulberry has no symbol; `own.json` lists those), all committed, plus `preview.html` (not
committed): all pictograms on one page, plus the list of app words that still have none.
`python3 pictograms/export_png.py` then makes the PNGs the iOS app bundles (`Pictograms/`).

## Layout

| path | what |
|---|---|
| `kit.py` | Style (colors, line width), shape helpers `P` (path), `C` (circle), `E` (ellipse), people parts (`face`, `bust`, `torso`, `headb`, `face_small`, `hand`, `arm`), the `@picto` registry and the `svg` wrapper. |
| `sets/<folder>.py` | One file per app folder (`core`, `food`, `feelings`, `verbs`, ...). One function per pictogram. |
| `build.py` | Imports every set, writes the SVGs and the preview. Deletes SVGs whose pictogram no longer exists. |
| `svg/` | Generated. File name = word id from `structure.json`. |

## Adding a pictogram

1. Find the word id in `logo/Vocabulary/structure.json` (e.g. `ball`) and the folder it is in.
2. In `sets/<folder>.py` (create it if needed, start with `from kit import *`):
   ```python
   @picto('ball', 'lopta')
   def ball():
       s = C(50, 52, 34, '#E5534B')
       s += P('M16 52 Q50 30 84 52', sw=2)
       return s
   ```
   The function returns SVG elements as a string, drawn on a `0 0 100 100` canvas.
3. `python3 pictograms/build.py`, open `preview.html`, look at it, adjust, repeat.

## Style rules (so the set stays one family)

- Canvas `0 0 100 100`. The subject fills most of the frame, centered, a few units of margin.
  People in actions are a cropped bust that bleeds off the bottom edge.
- Outline: always `L` (`#2A2A2A`), width `W` (2). Thicker only on purpose (yes/no marks, brows).
  Round line ends and joins (set by the wrapper).
- Flat fills from the palette in `kit.py`. No gradients, no text, no shadows.
- Feelings: the big `face()` fills the frame; mood from brows, eyes and mouth; small extra marks
  (tears, red anger marks, sigh lines) at the edges.
- Actions: `bust()` or `torso()` + `headb()`, `face_small()` with a mood, `arm()` and `hand('open'|'grip')`;
  the object of the action held or reached for.
- Objects (food, toys, clothes): one object, its typical view, a highlight or detail line or two.
- Friendly: no stare (eyes are solid dark ovals with a white highlight), rounded shapes.

## Checking the result

`preview.html` must be looked at, the code alone does not show whether a drawing reads well.
On a machine without a browser, render to PNG and look at the image, for example with
`rsvg-convert -w 256 svg/ball.svg -o /tmp/ball.png` (package `librsvg2-bin`).
