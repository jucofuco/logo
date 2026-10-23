"""Shared drawing kit for all pictograms: style constants, shape helpers, people parts, registry.

Every pictogram is drawn on a 100 x 100 canvas with one dark outline color and one line width,
flat fills, round line ends. Keep new pictograms inside these rules so the set looks like one family.
"""

# ---------- style ----------
L = '#2A2A2A'          # outline
W = 2                  # outline width, same everywhere
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
def P(d, fill='none', sw=W, stroke=L):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def C(cx, cy, r, fill, sw=W, stroke=L):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def E(cx, cy, rx, ry, fill, sw=W, stroke=L, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{t}/>'


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


# detailed open hand, wrist at origin, fingers toward -y
HAND_OPEN = ('<path d="M-5 -2 L-12.8 -11.6 A2.1 2.1 0 0 1 -9.6 -14.2 L-3.5 -8 Z" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M-6 0 C-7 -4 -7.6 -8 -7.6 -11 L-7.6 -20 A1.9 1.9 0 0 1 -3.8 -20 L-3.8 -12.5 L-3.8 -22.6 A1.9 1.9 0 0 1 0 -22.6 '
             'L0 -12.5 L0 -21.6 A1.9 1.9 0 0 1 3.8 -21.6 L3.8 -12.5 L3.8 -18.4 A1.8 1.8 0 0 1 7.4 -18.4 L7.4 -9 C7.4 -5 6.8 -2 6 0 Z" '
             'fill="{SK}" stroke="{L}" stroke-width="{w}"/>')
# fist holding something, wrist at origin, object passes vertically through x≈0
HAND_GRIP = ('<rect x="-7" y="-14" width="13" height="13" rx="4" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M-7 -10.8 H3 M-7 -7.6 H3 M-7 -4.4 H3" fill="none" stroke="{L}" stroke-width="{w2}"/>'
             '<rect x="2" y="-18" width="5" height="11" rx="2.5" fill="{SK}" stroke="{L}" stroke-width="{w}"/>')


def hand(kind, x, y, rot=0, sc=1.25, mirror=False):
    w = round(W / sc, 2); w2 = round(1.4 / sc, 2)
    t = HAND_OPEN if kind == 'open' else HAND_GRIP
    sx = -sc if mirror else sc
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {sc})">' + t.format(SK=SK, L=L, w=w, w2=w2) + '</g>'


# ---------- registry ----------
# word id (as in logo/Vocabulary/structure.json) -> (Slovak label, function returning the SVG body)
PICTOS = {}


def picto(word_id, label):
    """Registers a pictogram. `word_id` is the app's word id, `label` the Slovak word (for the preview)."""
    def register(fn):
        if word_id in PICTOS:
            raise ValueError(f'pictogram {word_id} is defined twice')
        PICTOS[word_id] = (label, fn)
        return fn
    return register


def svg(label, body, size=512):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{size}" height="{size}" '
            f'stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{label}">{body}</svg>')
