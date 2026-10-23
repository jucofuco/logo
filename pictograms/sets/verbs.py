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


from sets.people import arrow_to, place, point_hand, ARROW  # noqa: E402

PANTS = '#4A6FA5'
WOOD = '#C98F55'


def kid_full(x=50, stride=False, look=0):
    """Whole child standing (front view), feet at y≈90. With stride the legs and arms swing (walking)."""
    s = ''
    if stride:
        s += P(f'M{x-5} 66 L{x-12} 84', 'none', 11 + 2 * W, L) + P(f'M{x-5} 66 L{x-12} 84', 'none', 11, PANTS)
        s += P(f'M{x+5} 66 L{x+12} 84', 'none', 11 + 2 * W, L) + P(f'M{x+5} 66 L{x+12} 84', 'none', 11, PANTS)
        s += P(f'M{x-20} 84 Q{x-20} 90 {x-14} 90 H{x-6} Q{x-6} 84 {x-12} 83 Z', L, 0)
        s += P(f'M{x+8} 84 Q{x+8} 90 {x+14} 90 H{x+22} Q{x+22} 84 {x+16} 83 Z', L, 0)
        la, ra = f'M{x-12} 46 Q{x-20} 56 {x-24} 62', f'M{x+12} 46 Q{x+20} 54 {x+26} 56'
    else:
        s += P(f'M{x-13} 64 H{x-1} V86 H{x-13} Z', PANTS) + P(f'M{x+1} 64 H{x+13} V86 H{x+1} Z', PANTS)
        s += P(f'M{x-15} 86 Q{x-15} 91 {x-10} 91 H{x-1} V86 Z', L, 0) + P(f'M{x+15} 86 Q{x+15} 91 {x+10} 91 H{x+1} V86 Z', L, 0)
        la, ra = f'M{x-12} 46 Q{x-18} 56 {x-19} 64', f'M{x+12} 46 Q{x+18} 56 {x+19} 64'
    s += P(la, 'none', 9 + 2 * W, L) + P(ra, 'none', 9 + 2 * W, L)
    s += P(f'M{x-15} 68 V50 Q{x-15} 40 {x} 40 Q{x+15} 40 {x+15} 50 V68 Z', SHIRT)
    s += P(la, 'none', 9, SHIRT) + P(ra, 'none', 9, SHIRT)
    ex = la.split()[-2:]; ey = ra.split()[-2:]
    s += C(float(ex[0]), float(ex[1]) + 3, 4.5, SK) + C(float(ey[0]) + (2 if stride else 0), float(ey[1]) + 3, 4.5, SK)
    s += place(headb(0, 36) + face_small(50, 38, 'smile', look), x, 24, 0.7)
    return s


@picto('be', 'byť')
def be():
    # the child just standing on a spot: "here I am"
    s = E(50, 90, 34, 7, '#FFE08A')
    s += kid_full(50)
    s += P('M14 30 L20 34 M10 46 H17 M86 30 L80 34 M90 46 H83', sw=2.2, stroke=ARROW)
    return s


@picto('have', 'mať')
def have():
    # holds a ball to the chest with both hands
    s = bust(0, 32, 19) + face_small(50, 34, 'smile')
    s += C(50, 76, 20, RED) + P('M31 70 Q50 80 69 70', 'none', 6, '#FFFFFF') + C(50, 76, 20, 'none')
    d1, d2 = 'M14 104 Q16 98 26 96', 'M86 104 Q84 98 74 96'
    s += arm(d1) + arm(d2)
    s += hand('open', 28, 97, 22, 1.1) + hand('open', 72, 97, -22, 1.1, mirror=True)
    return s


@picto('see', 'vidieť')
def see():
    # looks at a butterfly, dashed lines from the eyes
    s = bust(-20, 44, 19) + face_small(30, 46, 'smile', look=2.5)
    s += f'<path d="M42 44 L72 30" fill="none" stroke="{L}" stroke-width="1.8" stroke-dasharray="3 4"/>'
    s += f'<path d="M42 48 L72 38" fill="none" stroke="{L}" stroke-width="1.8" stroke-dasharray="3 4"/>'
    s += E(76, 26, 7, 9, '#F28C28', rot=-30) + E(88, 26, 7, 9, '#F28C28', rot=30)
    s += E(77, 38, 5, 6, '#F6C453', rot=-20) + E(87, 38, 5, 6, '#F6C453', rot=20)
    s += E(82, 32, 2.2, 9, L, 0) + P('M81 23 Q78 17 75 16 M83 23 Q86 17 89 16', sw=1.6)
    return s


@picto('need', 'potrebovať')
def need():
    # worried child reaches with both hands for a glass of water, red "!" mark
    d = 'M34 104 Q42 84 52 76'
    s = arm_back(d) + torso(-24, 61) + arm_fill(d) + headb(-24, 38) + face_small(26, 40, 'worried', look=2)
    s += P('M70 50 L92 50 L89 92 L73 92 Z', GLASS) + P('M70.9 62 H91.1 L89 90 H73 Z', WATER, 0) + P('M70 62 H92', sw=1.6)
    s += P('M70 50 L92 50 L89 92 L73 92 Z')
    s += hand('open', 53, 76, 68, 1.1)
    s += P('M78 8 L80 30 H86 L88 8 Z', RED) + C(83, 38, 4, RED)
    return s


@picto('make', 'robiť')
def make():
    # hammers a nail into a wooden block
    d = 'M76 104 Q84 80 72 62'
    s = arm_back(d) + torso(-14, 63) + arm_fill(d) + headb(-14, 40) + face_small(36, 42, 'smile', look=2)
    s += P('M50 82 H96 V104 H50 Z', WOOD) + P('M54 90 H66 M74 96 H90', sw=1.4, stroke='#8A5A2B')
    s += P('M80 82 V74', sw=2.6) + P('M76.5 73.5 H83.5', sw=2.6)
    s += '<g transform="rotate(30 72 60)">' + P('M70 64 H74 V34 H70 Z', WOOD) + P('M62 24 H86 V36 H62 Z', '#8D99A6') + '</g>'
    s += hand('grip', 73, 64, 30, 1.15)
    s += P('M88 64 L92 58 M92 72 L98 70 M84 60 L84 54', sw=2.2, stroke=ARROW)
    return s


@picto('ask', 'požiadať')
def ask():
    # holds out an open palm (please, give me) with a question bubble
    d = 'M58 104 Q62 84 72 78'
    s = arm_back(d) + torso(-20, 63) + arm_fill(d) + headb(-20, 42) + face_small(30, 44, 'smile', look=2)
    s += hand('open', 72, 79, 100, 1.25)
    s += P('M60 8 H92 Q96 8 96 12 V38 Q96 42 92 42 H72 L64 50 L66 42 H60 Q56 42 56 38 V12 Q56 8 60 8 Z', '#FFFFFF')
    s += P('M69 18 Q69 13 76 13 Q83 13 83 19 Q83 24 76 26 V30', 'none', 3.4) + C(76, 35.5, 2, L, 0)
    return s


@picto('dress', 'obliekať sa')
def dress():
    # pulls a T-shirt down over the head: head is through, the shirt still bunched on the chest
    TS = '#F6C453'
    s = P('M14 104 V87 Q14 65 50 63 Q86 65 86 87 V104 Z', '#FFFFFF')
    s += P('M44.5 46 V64 Q50 67.5 55.5 64 V46', SK)
    s += P('M16 84 Q14 66 30 62 L42 60 Q50 66 58 60 L70 62 Q86 66 84 84 Q78 80 72 84 Q66 80 60 84 Q54 80 50 84 Q46 80 40 84 Q34 80 28 84 Q22 80 16 84 Z', TS)
    s += P('M30 62 Q24 66 22 74 M70 62 Q76 66 78 74', sw=1.6)
    s += headb(0, 34) + face_small(50, 36, 'smile')
    s += hand('grip', 18, 92, 0, 1.15) + hand('grip', 82, 92, 0, 1.15)
    s += arrow_to('M6 56 V72', 6, 74, 90, sw=4, size=5) + arrow_to('M94 56 V72', 94, 74, 90, sw=4, size=5)
    return s


@picto('go', 'ísť')
def go():
    s = kid_full(44, stride=True, look=2)
    s += P('M8 94 H92', sw=2)
    s += arrow_to('M66 70 H84', 86, 70, 0)
    s += P('M10 40 H20 M6 52 H18 M10 64 H20', sw=2.2)
    return s


@picto('listen', 'počúvať')
def listen():
    # hand cupped behind the ear, music comes in
    d = 'M74 104 Q82 74 68 56'
    s = arm_back(d) + torso(-18, 63) + arm_fill(d) + headb(-18, 40) + face_small(30, 42, 'smile', look=2)
    s += hand('open', 67, 56, -20, 1.15)
    s += P('M80 36 Q84 42 80 48 M86 31 Q92 42 86 53', sw=2.2)
    s += P('M88 8 V24', sw=2.2) + E(85, 25, 3.6, 2.8, L, 0, rot=-20) + P('M88 8 Q92 10 94 14', sw=2.2)
    s += P('M72 4 V16 L80 13 V2 Z', L, 0) + P('M72 16 V18', sw=0) + E(69.5, 17.5, 3, 2.4, L, 0, rot=-20) + E(77.5, 15, 3, 2.4, L, 0, rot=-20)
    return s


@picto('play', 'hrať')
def play():
    # plays with a toy car, a ball next to it
    d = 'M70 104 Q74 92 70 82'
    s = arm_back(d) + bust(-14, 34, 19) + arm_fill(d) + face_small(36, 36, 'smile', look=2)
    s += P('M54 76 Q56 66 64 66 H78 Q84 66 88 74 L94 76 Q97 77 97 81 V86 H54 Z', RED)
    s += P('M62 74 Q63 69 67 69 H72 V74 Z M75 69 H78 Q81 69 84 74 H75 Z', '#BFE3F7', 1.6)
    s += C(63, 87, 5.5, L, 0) + C(63, 87, 2, '#BBBBBB', 0) + C(87, 87, 5.5, L, 0) + C(87, 87, 2, '#BBBBBB', 0)
    s += hand('grip', 72, 80, 0, 1.0)
    s += C(16, 88, 11, '#5B8DEF') + P('M5.5 86 Q16 80 26.5 86 M8 95 Q16 90 24 95', 'none', 1.6) + C(16, 88, 11, 'none')
    return s


@picto('sleep', 'spať')
def sleep():
    # lies in bed under a blanket, moon and stars
    s = P('M4 64 H96 V92 H4 Z', '#B98D5F')
    s += E(30, 58, 22, 10, '#FFFFFF')
    s += '<g transform="rotate(-8 34 48)">' + C(34, 48, 15, SK)
    s += P('M19.5 47 Q19 32 34 32 Q49 32 48.5 47 Q46 38 40 38 Q35 41 30 38 Q22 39 19.5 47 Z', HAIR)
    s += P('M25 51 Q28.5 54 32 51 M37 51 Q40.5 54 44 51', sw=2.2) + P('M31 58 Q34 60 37 58', sw=1.8) + '</g>'
    s += P('M42 60 Q46 54 58 54 H96 V82 H40 Q36 70 42 60 Z', '#8DBBEA')
    s += P('M52 58 V80 M66 56 V80 M80 56 V80', sw=1.2, stroke='#5E8FC2')
    s += P('M78 8 A14 14 0 1 0 92 30 A11 11 0 1 1 78 8 Z', '#F6D35B')
    s += P('M56 14 L58 19 L63 19 L59 22 L60.5 27 L56 24 L51.5 27 L53 22 L49 19 L54 19 Z', '#F6D35B', 1.4)
    s += P('M20 10 L21.5 14 L25.5 14 L22.5 16.5 L23.5 20 L20 18 L16.5 20 L17.5 16.5 L14.5 14 L18.5 14 Z', '#F6D35B', 1.4)
    return s


@picto('speak', 'hovoriť')
def speak():
    s = bust(-20, 44, 19) + face_small(30, 46, 'open', look=2)
    s += P('M56 10 H90 Q96 10 96 16 V36 Q96 42 90 42 H70 L60 52 L62 42 H58 Q52 42 52 36 V16 Q52 10 56 10 Z', '#FFFFFF')
    s += C(63, 26, 3, L, 0) + C(74, 26, 3, L, 0) + C(85, 26, 3, L, 0)
    s += P('M48 54 L54 56 M47 62 L53 66', sw=2)
    return s


@picto('cook', 'variť')
def cook():
    # pot on a stove with flames and steam, the child holds the handle
    d = 'M24 104 Q30 86 38 80'
    s = arm_back(d) + bust(-26, 36, 18) + arm_fill(d) + face_small(24, 38, 'smile', look=2.5)
    s += P('M44 96 H98 V104 H44 Z', '#5A5F66')
    for fx in (58, 71, 84):
        s += P(f'M{fx} 96 Q{fx-5} 90 {fx-2} 85 Q{fx} 89 {fx+1} 87 Q{fx+4} 90 {fx} 96 Z', '#F28C28', 1.4)
    s += P('M50 62 H94 V78 Q94 86 86 86 H58 Q50 86 50 78 Z', '#8D99A6')
    s += P('M47 62 H97', 'none', 5 + 2 * W, L) + P('M47 62 H97', 'none', 5, '#AAB4BF')
    s += P('M50 70 H38', 'none', 5 + 2 * W, L) + P('M50 70 H38', 'none', 5, '#5A5F66')
    s += hand('grip', 40, 79, 90, 1.05)
    s += P('M60 52 Q56 46 60 40 Q64 34 60 28 M72 52 Q68 46 72 40 Q76 34 72 28 M84 52 Q80 46 84 40 Q88 34 84 28', sw=2.2, stroke='#9AA3AD')
    return s


@picto('enter', 'zadať')
def enter():
    # a finger presses a key on a keypad
    s = P('M12 10 H76 Q82 10 82 16 V90 Q82 96 76 96 H12 Q6 96 6 90 V16 Q6 10 12 10 Z', '#5A5F66')
    for r in range(3):
        for c in range(3):
            x, y = 13 + c * 22, 17 + r * 26
            fill = '#F6C453' if (r, c) == (1, 1) else '#ECEFF4'
            s += P(f'M{x+3} {y} H{x+15} Q{x+18} {y} {x+18} {y+3} V{y+17} Q{x+18} {y+20} {x+15} {y+20} H{x+3} Q{x} {y+20} {x} {y+17} V{y+3} Q{x} {y} {x+3} {y} Z', fill)
    s += P('M98 104 Q86 92 74 86', 'none', 15 + 2 * W, L) + P('M98 104 Q86 92 74 86', 'none', 15, SHIRT)
    s += point_hand(72, 84, -50, 1.4, mirror=True)
    s += P('M30 44 L25 39 M28 58 L22 60 M44 36 V30', sw=2.2, stroke=ARROW)
    return s


@picto('stir', 'miešať')
def stir():
    # a hand stirs in a bowl, round arrow shows the motion
    s = P('M60 63 L78 30', 'none', 5 + 2 * W, L) + P('M60 63 L78 30', 'none', 5, WOOD)
    s += P('M12 62 H88 Q88 92 50 92 Q12 92 12 62 Z', '#8DBBEA')
    s += E(50, 62, 38, 7, '#F7EBD3')
    s += P('M40 62 Q46 58 52 62 M26 64 Q30 61 34 64', sw=1.6, stroke='#C9A97A')
    s += P('M56 62 L60 63 L64 62', sw=1.6)
    s += arrow_to('M66 40 A26 10 0 1 0 30 52', 30, 52, 100, sw=4, size=6)
    s += P('M92 104 Q90 60 80 40', 'none', 13 + 2 * W, L) + P('M92 104 Q90 60 80 40', 'none', 13, SHIRT)
    s += hand('grip', 80, 41, -25, 1.2)
    return s


@picto('throw', 'hádzať')
def throw():
    # arm flung forward, the ball flies away
    d = 'M56 104 Q62 80 70 60'
    s = arm_back(d) + torso(-22, 63) + arm_fill(d) + headb(-22, 40) + face_small(28, 42, 'smile', look=2.5)
    s += hand('open', 70, 60, 40, 1.2)
    s += C(84, 22, 10, '#5B8DEF') + P('M74.5 20 Q84 15 93.5 20 M76 28 Q84 24 92 28', 'none', 1.6) + C(84, 22, 10, 'none')
    s += P('M62 32 L72 28 M60 42 L70 36 M70 46 L76 40', sw=2.2)
    return s
