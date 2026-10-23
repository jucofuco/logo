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


def reach_apple():
    """A big arm in the child's blue sleeve reaching up toward an apple (idea: ARASAAC 31141)."""
    sleeve = 'M-8 108 Q16 88 42 70'
    s = hand('open', 45, 68, 53, 1.65)
    s += P(sleeve, 'none', 22 + 2 * W, L) + P(sleeve, 'none', 22, SHIRT)
    s += P('M35.6 60.6 L48.4 79.4', 'none', 2.4, L)                      # cuff
    s += C(82, 20, 12, '#E5534B') + P('M82 8 Q82 3 87 1.5', sw=2.2) + P('M82 6.5 Q88 -0.5 95 3 Q89 10 82 6.5 Z', GREEN, 1.6)
    s += E(76, 16, 2.8, 4.6, '#F6A39D', 0, rot=30)
    return s


@picto('want', 'chcem')
def want():
    s = reach_apple()
    s += P('M58 22 L63 27 M53 33 L60 35 M66 12 L68 18', sw=2.2)         # eager marks
    return s


@picto('dontWant', 'nechcem')
def dont_want():
    # the same reach, crossed out (idea: ARASAAC 6156)
    xx = 'M18 18 L82 82 M82 18 L18 82'
    return reach_apple() + P(xx, 'none', 13, L) + P(xx, 'none', 9, RED)


@picto('help', 'pomoc')
def help_():
    # raised waving hand
    d = 'M58 84 Q72 64 70 40'
    s = arm_back(d) + torso(-10, 63) + arm_fill(d) + headb(-10, 40) + face_small(40, 42, 'worried')
    s += hand('open', 70, 38, 4, 1.25)
    s += P('M82 12 Q86 18 82 24 M87 9 Q93 18 87 27', sw=2)
    return s


from sets.people import me_pointing, place, point_hand  # noqa: E402


@picto('me', 'ja')
def me():
    # the child points at his own chest
    return place(me_pointing(), 50, 40, 1.1)


