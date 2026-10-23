"""Core words on the main screen: áno, nie, chcem, plus pomoc."""
from kit import *


@picto('yes', 'áno')
def yes():
    # big green check (thin dark outline around a thick green stroke)
    ck = 'M20 52 L41 73 L80 28'
    return P(ck, 'none', 19, L) + P(ck, 'none', 15, GREEN)


@picto('no', 'nie')
def no():
    # big red X
    xx = 'M24 24 L76 76 M76 24 L24 76'
    return P(xx, 'none', 19, L) + P(xx, 'none', 15, RED)


@picto('want', 'chcem')
def want():
    # reach toward apple
    d = 'M38 80 Q50 60 62 52'
    s = arm_back(d) + torso(-22, 61) + arm_fill(d) + headb(-22, 38) + face_small(28, 40, 'smile', look=2)
    s += C(83, 26, 9.5, '#E5534B') + P('M83 16.5 Q83 11 88 10', sw=1.8) + P('M83 15 Q87 9 92 12 Q88 16 83 15 Z', GREEN, 1.4)
    s += hand('open', 63, 51, 52, 1.15)
    s += P('M70 32 L73 36 M74 40 L78 41', sw=1.8)
    return s


@picto('help', 'pomoc')
def help_():
    # raised waving hand
    d = 'M58 84 Q72 64 70 40'
    s = arm_back(d) + torso(-10, 63) + arm_fill(d) + headb(-10, 40) + face_small(40, 42, 'worried')
    s += hand('open', 70, 38, 4, 1.25)
    s += P('M82 12 Q86 18 82 24 M87 9 Q93 18 87 27', sw=2)
    return s
