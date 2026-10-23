"""Shared drawing kit for all pictograms: style constants, shape helpers, people parts, registry.

Every pictogram is drawn on a 100 x 100 canvas with one dark outline color and one line width,
flat fills, round line ends. Keep new pictograms inside these rules so the set looks like one family.
"""

import os

# ---------- style ----------
# Style 2 (PICTO_STYLE=2, built into svg-v2/ by build.py): the same drawings with a thinner line and a
# calmer, less cartoon-like face: small dot eyes, a small smile, no blush, a slightly smaller head.
STYLE = int(os.environ.get('PICTO_STYLE', '1'))
L = '#2A2A2A'          # outline
W = 2 if STYLE == 1 else 1.3   # outline width, same everywhere
BLUSH = '#F7A8A0'      # cheek color, left out in style 2
SK = '#FAD7BE'         # skin
HAIR = '#6B4226'
SHIRT = '#8DBBEA'
MOUTH = '#7E2B2B'
TONGUE = '#E88080'
TEAR = '#6EC1F0'
RED = '#E5534B'
GREEN = '#3BA55D'
FOOD = '#F4A340'
OBJ = '#ECEFF4'        # plates, cutlery, glass objects held by people
ANGRY = '#F5A99B'
WATER = '#6EC1F0'
GLASS = '#F2F6FA'


# ---------- shapes ----------
def _sw(sw):
    """Style 2 thins the detail lines too. Thick strokes (limbs, symbols) and the outline width stay."""
    if STYLE == 1 or sw == W or sw <= 0 or sw > 3.2:
        return sw
    return round(sw * 0.65, 2)


def P(d, fill='none', sw=W, stroke=L):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{_sw(sw)}"/>'


def C(cx, cy, r, fill, sw=W, stroke=L):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{_sw(sw)}"/>'


def E(cx, cy, rx, ry, fill, sw=W, stroke=L, rot=0):
    if STYLE == 2 and fill == BLUSH:
        return ''
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{_sw(sw)}"{t}/>'


def arrow(d, heads, color, sw=3):
    s = P(d, 'none', sw, color)
    for h in heads:
        s += P(h, color, 1.2, color)
    return s


# ---------- big emotion face (head fills the frame) ----------
def face(skin=SK):
    return (C(50, 54, 34, skin)
            + P('M16.6 50 Q14 18 50 17 Q86 18 83.4 50 Q82 33 75 28.5 Q70 34 62 30.5 Q56 36 48 31.5 Q40 36 33.5 30.5 Q24 32 16.6 50 Z', HAIR))


def eye_open(cx, cy, r=5.2, pupil=2.6, py=0):
    if STYLE == 2:
        return C(cx, cy + py * 0.4, r * 0.4, L, 0)   # a small dot, no highlight
    # friendly solid eye with highlight (no sclera = no stare)
    rx = r * 0.72; ry = r * 0.95
    return E(cx, cy + py * 0.4, rx, ry, L, 0) + C(cx + rx * 0.35, cy + py * 0.4 - ry * 0.4, rx * 0.36, '#FFFFFF', 0)


def happy_eye(cx, cy):
    return P(f'M{cx-6} {cy+2} Q{cx} {cy-7} {cx+6} {cy+2}', sw=3)


# ---------- cropped upper body (bleeds off bottom edge) ----------
def torso(dx=0, top=64):
    x = 50 + dx
    return P(f'M{x-36} 104 V{top+24} Q{x-36} {top+2} {x} {top} Q{x+36} {top+2} {x+36} {top+24} V104 Z', SHIRT)


def headb(dx=0, head_y=36, r=19):
    if STYLE == 2:
        r *= 0.9
    x = 50 + dx
    nb = head_y + r + 5.5
    s = P(f'M{x-5.5} {head_y+r-4} V{nb} Q{x} {nb+3.5} {x+5.5} {nb} V{head_y+r-4}', SK)
    s += C(x, head_y, r, SK)
    s += P(f'M{x-r+0.5} {head_y-1} Q{x-r} {head_y-r-1} {x} {head_y-r-1} Q{x+r} {head_y-r-1} {x+r-0.5} {head_y-1} '
           f'Q{x+r-3} {head_y-r*0.62} {x+7} {head_y-r*0.66} Q{x+1} {head_y-r*0.4} {x-5} {head_y-r*0.62} Q{x-r+3} {head_y-r*0.6} {x-r+0.5} {head_y-1} Z', HAIR)
    return s


def bust(dx=0, head_y=36, r=19):
    return torso(dx, head_y + r + 4) + headb(dx, head_y, r)


def arm_back(d, width=11):
    return P(d, 'none', width + 2 * W, L)


def arm_fill(d, width=11):
    return P(d, 'none', width, SHIRT)


def arm(d, width=11):
    return P(d, 'none', width + 2 * W, L) + P(d, 'none', width, SHIRT)


def face_small(x, y, mood='smile', look=0):
    s = ''
    if mood == 'worried':
        s += P(f'M{x-11} {y-6} Q{x-7} {y-11} {x-2.5} {y-10}', sw=2.2) + P(f'M{x+2.5} {y-10} Q{x+7} {y-11} {x+11} {y-6}', sw=2.2)
    elif mood in ('smile', 'neutral', 'frown'):
        s += P(f'M{x-11} {y-8} Q{x-7} {y-11} {x-3} {y-9}', sw=2) + P(f'M{x+3} {y-9} Q{x+7} {y-11} {x+11} {y-8}', sw=2)
    if mood == 'pain':
        s += P(f'M{x-11} {y-2} L{x-5} {y+0.5} L{x-11} {y+3}', sw=2.4) + P(f'M{x+11} {y-2} L{x+5} {y+0.5} L{x+11} {y+3}', sw=2.4)
        s += P(f'M{x-6} {y+12} Q{x-3} {y+9} {x} {y+12} Q{x+3} {y+15} {x+6} {y+12}', sw=2)
        return s
    s += eye_open(x - 6.5 + look, y, r=3.6) + eye_open(x + 6.5 + look, y, r=3.6)
    if STYLE == 2:
        # a small mouth line instead of the big open cartoon mouth
        if mood == 'smile':
            s += P(f'M{x-4.5} {y+9} Q{x} {y+12.5} {x+4.5} {y+9}')
        elif mood in ('frown', 'worried'):
            s += P(f'M{x-4} {y+12} Q{x} {y+8.8} {x+4} {y+12}')
        elif mood == 'open':
            s += E(x, y + 10.5, 2.2, 2.6, '#B5413D')
        elif mood == 'neutral':
            s += P(f'M{x-3} {y+10.5} H{x+3}')
        return s
    if mood == 'smile':
        s += P(f'M{x-8} {y+8} Q{x} {y+9} {x+8} {y+8} Q{x+6} {y+16} {x} {y+16} Q{x-6} {y+16} {x-8} {y+8} Z', '#B5413D', 1.6)
    elif mood in ('frown', 'worried'):
        # small filled sad mouth, high on the face: a bare arch near the chin read as a moustache
        s += P(f'M{x-5.5} {y+13} Q{x} {y+6.5} {x+5.5} {y+13} Q{x} {y+10.5} {x-5.5} {y+13} Z', '#B5413D', 1.6)
    elif mood == 'open':
        s += E(x, y + 11, 3.2, 3.8, '#B5413D', 1.6)
    elif mood == 'neutral':
        s += P(f'M{x-4} {y+11} H{x+4}', sw=2)
    return s


# Hands: wrist at origin, fingers toward -y, thumb toward -x (a right hand seen from the palm).
# One smooth outline each, so they read clearly at phone size.
# open palm
HAND_OPEN = ('<path d="M-6 0 C-6.6 -2.5 -7 -4.5 -7.2 -6.6 C-9.2 -7.6 -11.6 -10 -13.4 -12.8 '
             'A2.2 2.2 0 0 1 -9.6 -15 C-8.6 -13.8 -7.9 -12.9 -7.3 -12.4 L-7.4 -20.6 A1.85 1.85 0 0 1 -3.7 -20.6 L-3.7 -14.6 '
             'L-3.7 -22.7 A1.85 1.85 0 0 1 0 -22.7 L0 -14.6 '
             'L0 -21.8 A1.85 1.85 0 0 1 3.7 -21.8 L3.7 -14.6 '
             'L3.7 -18.6 A1.8 1.8 0 0 1 7.3 -18.6 L7.3 -10 C7.3 -5.6 6.8 -2.6 6 0 Z" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M-7.2 -6.6 C-5.6 -5.8 -4.4 -6.8 -4.6 -9.2" fill="none" stroke="{L}" stroke-width="{w2}"/>')

# fist holding something that passes vertically through x = 0 (spoon, glass, hammer handle)
HAND_GRIP = ('<path d="M-6 0 C-7.6 -1 -8.2 -3.5 -8.2 -6.5 L-8.2 -10.5 C-8.2 -14 -6 -15.6 -2.5 -15.6 L3 -15.6 '
             'C6.4 -15.6 7.8 -13.6 7.8 -10.8 L7.8 -4.4 C7.8 -1.4 6 0 3 0 Z" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M2.2 -15.4 C5 -15 5.4 -11.4 2.4 -11.2 M2.4 -11.2 C5.4 -10.9 5.6 -7.2 2.6 -7.1 M2.6 -7.1 C5.4 -6.8 5.4 -3.2 2.8 -3" '
             'fill="none" stroke="{L}" stroke-width="{w2}"/>'
             '<path d="M-8 -9.5 C-6 -12.8 -2.5 -13.6 0.8 -12.6 C2.2 -12.2 2 -10.4 0.4 -10.4 C-2.6 -10.6 -5.4 -9.4 -7.4 -7.2" '
             'fill="{SK}" stroke="{L}" stroke-width="{w}"/>')

# pointing: index finger out toward -y, the other fingers curled, thumb across them
HAND_POINT = ('<path d="M-6.2 0 C-7.6 -1.6 -8.1 -4.2 -8.1 -7 L-8 -11.4 L-7.7 -23.6 A2.35 2.35 0 0 1 -3 -23.6 '
              'L-2.8 -15.6 C-1.2 -16.8 1.6 -16.8 3 -15.4 C5.6 -15.8 7.8 -14 7.7 -11 '
              'C7.9 -6.4 7.6 -2.8 5.8 -1 C4.8 -0.2 4 0 3 0 Z" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
              '<path d="M3 -15.4 C3.4 -13.8 3.2 -12.4 2.2 -11.6 M1.6 -11.4 C4 -11.8 6.2 -11.4 7.8 -10.4 '
              'M2 -7.2 C4.2 -7.6 6.2 -7.2 7.7 -6.2" fill="none" stroke="{L}" stroke-width="{w2}"/>'
              '<path d="M-8 -8.6 C-5.4 -11.8 -1.2 -12.8 2.4 -11.4 C3.8 -10.8 3.4 -8.8 1.8 -9 C-1.2 -9.4 -4.6 -7.8 -7.4 -5.2" '
              'fill="{SK}" stroke="{L}" stroke-width="{w}"/>')


def hand(kind, x, y, rot=0, sc=1.25, mirror=False):
    """kind: 'open', 'grip' or 'point'. `mirror` makes it a left hand."""
    w = round(W / sc, 2); w2 = round(1.4 / sc, 2)
    t = {'open': HAND_OPEN, 'grip': HAND_GRIP, 'point': HAND_POINT}[kind]
    sx = -sc if mirror else sc
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {sc})">' + t.format(SK=SK, L=L, w=w, w2=w2) + '</g>'


# ---------- registry ----------
# word id (as in logo/Vocabulary/structure.json) -> (Slovak label, function returning the SVG body)
PICTOS = {}
# Style 2 (simpler people, sets_v2/): only the pictograms that differ; the rest is taken from PICTOS.
PICTOS_V2 = {}


def picto(word_id, label, style=1):
    """Registers a pictogram. `word_id` is the app's word id, `label` the Slovak word (for the preview).
    style=2 registers the style 2 version of a word (see sets_v2/)."""
    registry = PICTOS_V2 if style == 2 else PICTOS
    def register(fn):
        if word_id in registry:
            raise ValueError(f'pictogram {word_id} (style {style}) is defined twice')
        registry[word_id] = (label, fn)
        return fn
    return register


def svg(label, body, size=512):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{size}" height="{size}" '
            f'stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{label}">{body}</svg>')
