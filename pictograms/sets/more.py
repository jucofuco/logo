"""Abstract words: conjunctions, prepositions, sizes.

Recurring objects so the words read as a family: a red ball, a blue block, a cardboard box.
"""
from kit import *

BLUE = '#5B8DEF'
BOX = '#D9A066'
BOX_IN = '#A8652E'
PALE = '#E3E6EC'      # the "other" items in the size series
GREY = '#9AA0A8'


# ---------- local helpers ----------
def ball(cx, cy, r, fill=RED, sw=W):
    s = C(cx, cy, r, fill, sw)
    s += P(f'M{cx-r} {cy} Q{cx} {cy-r*0.55} {cx+r} {cy}', sw=sw * 0.9)
    s += E(cx - r * 0.42, cy - r * 0.55, r * 0.16, r * 0.24, '#FFFFFF', 0, rot=35)
    return s


def block(x, y, a, fill=BLUE):
    # cube, front face top-left corner at (x, y), side a
    d = a * 0.28
    s = P(f'M{x} {y} L{x+d} {y-d} H{x+a+d} L{x+a} {y} Z', '#8FB2F4' if fill == BLUE else fill)
    s += P(f'M{x+a} {y} L{x+a+d} {y-d} V{y+a-d} L{x+a} {y+a} Z', '#3F6FD0' if fill == BLUE else fill)
    s += P(f'M{x} {y} H{x+a} V{y+a} H{x} Z', fill)
    return s


def box(x, y, w, h):
    # open cardboard box seen slightly from above; rim at y
    s = P(f'M{x} {y} L{x+8} {y-8} H{x+w-8} L{x+w} {y} Z', BOX_IN)
    s += P(f'M{x} {y} H{x+w} V{y+h} H{x} Z', BOX)
    s += P(f'M{x} {y} L{x-8} {y-10} M{x+w} {y} L{x+w+8} {y-10}', sw=W)
    s += P(f'M{x} {y} L{x-8} {y-10} L{x-2} {y-14} L{x+8} {y-8} Z', '#E9B77E')
    s += P(f'M{x+w} {y} L{x+w+8} {y-10} L{x+w+2} {y-14} L{x+w-8} {y-8} Z', '#E9B77E')
    s += P(f'M{x+w/2-6} {y+h*0.3} H{x+w/2+6}', sw=2.4, stroke=BOX_IN)
    return s


def thick(d, color, w=9):
    return P(d, 'none', w + 4, L) + P(d, 'none', w, color)


def plus(cx, cy, r=10, color=GREEN):
    d = f'M{cx-r} {cy} H{cx+r} M{cx} {cy-r} V{cy+r}'
    return thick(d, color, 6)


def bold_arrow(d, head, color=GREEN):
    # outlined arrow: shaft path + head polygon
    return P(d, 'none', 10, L) + P(head, color, W) + P(d, 'none', 6, color)


# ---------- pictograms ----------
@picto('colors', 'farby')
def colors():
    # painter's palette with color blobs
    s = P('M50 14 Q86 14 90 44 Q93 66 76 66 Q66 66 66 74 Q68 86 54 88 Q16 90 10 56 Q8 16 50 14 Z', '#E8C796')
    s += E(30, 62, 6.5, 6, '#FFFFFF')
    s += C(28, 40, 8, RED) + C(46, 28, 8, '#F7D154') + C(68, 30, 8, GREEN) + C(78, 48, 7.5, BLUE)
    return s


@picto('and', 'a')
def and_():
    # ball + block
    return ball(22, 52, 16) + plus(50, 52, 9) + block(64, 40, 22)


@picto('or', 'alebo')
def or_():
    # ball on the left, block on the right, a fork arrow choosing one or the other
    s = ball(22, 26, 15) + block(66, 14, 22)
    s += P('M50 90 V64 Q50 52 32 46 M50 64 Q50 52 70 46', 'none', 10, L)
    s += P('M24 36 L38 39 L30 50 Z', '#F7A23B', W) + P('M76 36 L62 39 L70 50 Z', '#F7A23B', W)
    s += P('M50 90 V64 Q50 52 32 46 M50 64 Q50 52 70 46', 'none', 6, '#F7A23B')
    return s


@picto('but', 'ale')
def but():
    # U-turn: goes one way, then comes back the other way
    d = 'M12 30 H64 Q86 30 86 50 Q86 70 64 70 H34'
    return bold_arrow(d, 'M36 58 L14 70 L36 82 Z', '#F7A23B')


@picto('although', 'hoci')
def although():
    # winding road: a detour, but it still gets there
    d = 'M12 18 H64 Q82 18 82 34 Q82 50 64 50 H36 Q18 50 18 66 Q18 82 36 82 H62'
    return bold_arrow(d, 'M62 70 L86 82 L62 94 Z', '#F7A23B')


@picto('with', 's')
def with_():
    # ball and block together, held in one green ring
    s = E(50, 52, 44, 30, '#E3F4E8', 3, GREEN)
    s += ball(32, 54, 15) + block(52, 44, 21)
    return s


@picto('without', 'bez')
def without():
    # block alone, the ball crossed out
    s = ball(30, 54, 16)
    s += thick('M12 36 L48 72 M48 36 L12 72', RED, 6)
    s += block(58, 42, 22)
    return s


@picto('another', 'ďalší')
def another():
    # the used ones, then an arrow to the next one
    s = C(13, 52, 9, PALE, 1.6, GREY) + C(34, 52, 9, PALE, 1.6, GREY)
    s += bold_arrow('M48 52 H58', 'M56 44 L68 52 L56 60 Z', GREEN)
    s += ball(83, 52, 14)
    return s


@picto('on', 'na')
def on():
    # ball sits on top of the closed box
    s = P('M20 58 L28 50 H80 L72 58 Z', '#E9B77E')
    s += P('M72 58 L80 50 V80 L72 88 Z', BOX_IN)
    s += P('M20 58 H72 V88 H20 Z', BOX)
    s += P('M40 58 L48 50 M46 58 V66', sw=1.6, stroke=BOX_IN)
    s += ball(50, 40, 15)
    s += arrow('M50 6 V16', ['M44 14 L50 22 L56 14 Z'], GREEN, 4)
    return s


@picto('from', 'z')
def from_():
    # ball comes up out of the box
    s = ball(54, 22, 14)
    s += box(18, 64, 52, 28)
    s += arrow('M30 58 Q30 30 38 26', ['M34 20 L44 23 L37 31 Z'], GREEN, 4)
    return s


@picto('if', 'ak')
def if_():
    # decision point on a path: a diamond with a question mark, the path goes on
    s = P('M6 50 H22 M78 50 H86', 'none', 6, L)
    s += P('M50 18 L82 50 L50 82 L18 50 Z', '#FFF1C9', 3)
    s += P('M42 42 Q42 33 50 33 Q58 33 58 41 Q58 47 50 50 V55', 'none', 5, L)
    s += C(50, 64, 3, L, 0)
    s += P('M84 41 L97 50 L84 59 Z', GREEN, W)
    return s


def sizes(which):
    rs = {'small': 8, 'medium': 14, 'big': 21}
    xs = {'small': 12, 'medium': 37, 'big': 74}
    base = 78
    s = P('M4 79.5 H96', sw=2, stroke=GREY)
    for k in ('small', 'medium', 'big'):
        r = rs[k]
        if k == which:
            s += ball(xs[k], base - r, r)
        else:
            s += C(xs[k], base - r, r, PALE, 1.6, GREY)
    r = rs[which]
    s += arrow(f'M{xs[which]} {base - 2*r - 16} V{base - 2*r - 6}',
               [f'M{xs[which]-6} {base-2*r-8} L{xs[which]} {base-2*r-1} L{xs[which]+6} {base-2*r-8} Z'], GREEN, 4)
    return s


@picto('big', 'veľký')
def big():
    return sizes('big')


@picto('medium', 'stredný')
def medium():
    return sizes('medium')


@picto('small', 'malý')
def small():
    return sizes('small')


@picto('like', 'ako')
def like():
    # similar, not the same: a dashed ball next to a real ball
    s = ball(26, 52, 19)
    s += C(74, 52, 19, '#F3B1AC', 0)
    s += f'<circle cx="74" cy="52" r="19" fill="none" stroke="{L}" stroke-width="3" stroke-dasharray="5 4.5"/>'
    s += P('M55 52 Q74 41.5 93 52', sw=2, stroke='#C7625B')
    return s
