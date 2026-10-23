"""Verbs folder: a cropped person doing the action."""
from kit import *


@picto('eat', 'jesť')
def eat():
    s = bust(0, 34, 20) + face_small(50, 36, 'open')
    s += arm('M80 104 Q86 76 70 66')
    s += P('M69 63 L55.5 47.5', sw=3) + E(53, 44.8, 6.4, 4.2, OBJ, 1.8, rot=48)
    s += hand('grip', 70, 70, -45, 1.1)
    s += P('M18 82 Q36 72 50 82 Z', FOOD, 1.6) + P('M14 82 H54 Q54 96 34 96 Q14 96 14 82 Z', OBJ)
    return s


@picto('drink', 'piť')
def drink():
    s = bust(-4, 34, 20) + face_small(46, 36, 'open')
    s += arm('M82 104 Q88 76 72 64')
    s += f'<g transform="translate(60.5 49) rotate(-48)">' + P('M-7 -11 L7 -11 L5.5 11 L-5.5 11 Z', OBJ) + P('M-5.9 -3 L5.9 -3 L4.9 9.5 L-4.9 9.5 Z', TEAR, 0) + '</g>'
    s += hand('grip', 71, 66, -48, 1.1)
    return s
