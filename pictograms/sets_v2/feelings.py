"""Style 2 redraws of the big feeling faces that are drawn by hand in sets/feelings.py: calmer,
no big cartoon mouths or blush, dot eyes, thin lines."""
from kit import *


def eyes(y=52, r=2.6, dx=14):
    return C(50 - dx, y, r, L, 0) + C(50 + dx, y, r, L, 0)


@picto('happy', 'veselý', style=2)
def happy():
    s = face() + eyes()
    s += P('M28 42 Q35 38 42 41') + P('M58 41 Q65 38 72 42')
    s += P('M35 66 Q50 78 65 66 Q50 72 35 66 Z', '#B5413D')
    return s


@picto('angry', 'nahnevaný', style=2)
def angry():
    s = face() + eyes(54)
    s += P('M26 41 L43 47') + P('M74 41 L57 47')
    s += P('M38 74 Q50 66 62 74')
    s += P('M84 22 L80 30 M90 26 L84 32', sw=2, stroke=RED)
    return s


@picto('scared', 'vystrašený', style=2)
def scared():
    s = face('#F6DDCB') + eyes(50, 3.2)
    s += P('M27 39 Q34 33 41 36') + P('M59 36 Q66 33 73 39')
    s += E(50, 70, 4, 5, '#B5413D')
    s += P('M84 36 Q80 43 81 46 A3.6 3.6 0 0 0 88 46 Q89 43 84 36 Z', TEAR)
    s += P('M6 96 Q10 88 18 84', 'none', 8 + 2 * W) + P('M6 96 Q10 88 18 84', 'none', 8, SHIRT)
    s += P('M94 96 Q90 88 82 84', 'none', 8 + 2 * W) + P('M94 96 Q90 88 82 84', 'none', 8, SHIRT)
    s += hand('open', 22, 84, 20, 1.3) + hand('open', 78, 84, -20, 1.3, mirror=True)
    return s


def heart(cx, cy, s, fill=RED):
    return P(f'M{cx} {cy + s * 0.9} C{cx - s * 1.3} {cy - s * 0.1} {cx - s * 0.9} {cy - s * 1.1} {cx} {cy - s * 0.45} '
             f'C{cx + s * 0.9} {cy - s * 1.1} {cx + s * 1.3} {cy - s * 0.1} {cx} {cy + s * 0.9} Z', fill)


@picto('love', 'láska', style=2)
def love():
    s = bust(0, 30, 18) + face_small(50, 32, 'smile')
    s += heart(50, 76, 20)
    d1, d2 = 'M14 104 Q16 86 30 80', 'M86 104 Q84 86 70 80'
    s += arm(d1) + arm(d2)
    s += hand('open', 31, 81, 70, 1.1) + hand('open', 69, 81, -70, 1.1, mirror=True)
    s += heart(15, 22, 6, '#F28B9B') + heart(86, 18, 7, '#F28B9B')
    return s
