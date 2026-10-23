"""The alphabet: uppercase print letters a-z and the ABC folder icon."""
from kit import *

LW, FW = 13, 9          # outline stroke width, colored stroke width
COLORS = [RED, '#5B8DEF', GREEN, '#F7A23B', '#9B6FD6']

O = 'M50 20 Q74 20 74 50 Q74 80 50 80 Q26 80 26 50 Q26 20 50 20 Z'
_C = 'M72 32 Q65 20 50 20 Q28 20 28 50 Q28 80 50 80 Q65 80 72 68'
_P = 'M30 80 V20 H50 Q70 20 70 37 Q70 54 50 54 H30'

PATHS = {
    'a': 'M26 80 L50 20 L74 80 M36 58 H64',
    'b': 'M30 20 V80 M30 20 H50 Q68 20 68 35 Q68 50 50 50 H30 M50 50 Q72 50 72 65 Q72 80 50 80 H30',
    'c': _C,
    'd': 'M30 20 V80 H46 Q74 80 74 50 Q74 20 46 20 Z',
    'e': 'M70 20 H30 V80 H70 M30 50 H62',
    'f': 'M70 20 H30 V80 M30 50 H62',
    'g': 'M72 32 Q65 20 50 20 Q28 20 28 50 Q28 80 50 80 Q66 80 72 66 V52 H54',
    'h': 'M30 20 V80 M70 20 V80 M30 50 H70',
    'i': 'M38 20 H62 M50 20 V80 M38 80 H62',
    'j': 'M46 20 H70 M62 20 V60 Q62 80 46 80 Q32 80 29 66',
    'k': 'M30 20 V80 M70 20 L30 56 M44 44 L72 80',
    'l': 'M30 20 V80 H70',
    'm': 'M26 80 V20 L50 54 L74 20 V80',
    'n': 'M30 80 V20 L70 80 V20',
    'o': O,
    'p': _P,
    'q': O + ' M58 62 L74 81',
    'r': _P + ' M48 54 L70 80',
    's': 'M70 30 Q64 20 50 20 Q30 20 30 35 Q30 48 50 50 Q70 52 70 66 Q70 80 50 80 Q35 80 28 70',
    't': 'M26 20 H74 M50 20 V80',
    'u': 'M30 20 V58 Q30 80 50 80 Q70 80 70 58 V20',
    'v': 'M26 20 L50 80 L74 20',
    'w': 'M22 20 L36 80 L50 40 L64 80 L78 20',
    'x': 'M28 20 L72 80 M72 20 L28 80',
    'y': 'M26 20 L50 52 L74 20 M50 52 V80',
    'z': 'M28 20 H72 L28 80 H72',
}


def glyph(d, color, lw=LW, fw=FW):
    return P(d, 'none', lw, L) + P(d, 'none', fw, color)


def make(ch, color):
    @picto(f'letter.{ch}', ch)
    def f():
        return glyph(PATHS[ch], color)
    return f


for i, ch in enumerate('abcdefghijklmnopqrstuvwxyz'):
    make(ch, COLORS[i % len(COLORS)])


def tile(d, color, cx, cy, rot, gcx=50, gcy=50, k=1.0, s=0.5):
    """A rounded block with a glyph, centered at (cx, cy), drawn at scale s."""
    t = f'<g transform="translate({cx} {cy}) rotate({rot}) scale({s}) translate(-50 -50)">'
    t += f'<rect x="14" y="10" width="72" height="80" rx="14" fill="#FFFFFF" stroke="{L}" stroke-width="{W / s:.2f}"/>'
    t += f'<g transform="translate(50 50) scale({k}) translate({-gcx} {-gcy})">{glyph(d, color, LW, FW)}</g></g>'
    return t


@picto('abc', 'ABC')
def abc():
    return (tile(PATHS['a'], RED, 24, 54, -9, s=0.45) + tile(PATHS['c'], GREEN, 76, 54, 9, s=0.45)
            + tile(PATHS['b'], '#5B8DEF', 50, 48, 0, s=0.45))
