"""Feelings folder: big faces that fill the frame, plus bolí (person holding the forehead)."""
from kit import *


@picto('happy', 'veselý')
def happy():
    s = face()
    s += P('M27 39 Q35 33 43 37', sw=2.4) + P('M57 37 Q65 33 73 39', sw=2.4)
    s += happy_eye(36, 52) + happy_eye(64, 52)
    s += E(26, 64, 6, 4, '#F7A8A0', 0) + E(74, 64, 6, 4, '#F7A8A0', 0)
    s += P('M31 63 Q50 67 69 63 Q66 83 50 83 Q34 83 31 63 Z', '#B5413D')
    s += P('M40 78 Q50 72 60 78 Q55 82.5 50 82.5 Q45 82.5 40 78 Z', '#EE8C86', 0)
    s += P('M9 22 L14 27 M5 36 L11 37 M91 22 L86 27 M95 36 L89 37', sw=2.2)
    return s


@picto('sad', 'smutný')
def sad():
    s = face()
    s += P('M26 46 Q32 36 43 36', sw=2.8) + P('M57 36 Q68 36 74 46', sw=2.8)
    for cx in (36, 64):
        s += E(cx, 54, 3.8, 4.8, L, 0) + C(cx + 1.3, 52.2, 1.4, '#FFFFFF', 0)
        s += P(f'M{cx-6} 48.5 Q{cx} 46.5 {cx+6} 49.5', sw=2)          # heavy upper lid
    s += P('M36 79 Q43 72 50 74 Q57 72 64 79', sw=2.8)              # wobbly frown
    s += P('M35 60 Q30 69 31.5 73 A5.2 5.2 0 0 0 41.5 73 Q42 69 35 60 Z', TEAR, 1.5)
    s += P('M65 60 Q62 65 63 67.5 A3.5 3.5 0 0 0 69.5 67.5 Q70 65 65 60 Z', TEAR, 1.4)
    return s


@picto('angry', 'nahnevaný')
def angry():
    s = face('#FBC9BE')
    s += P('M24 38 L45 47 L44 51 L23 43 Z', L, 0) + P('M76 38 L55 47 L56 51 L77 43 Z', L, 0)
    for cx in (36, 64):
        s += E(cx, 56, 3.6, 4.2, L, 0)
    s += E(25, 66, 6, 4, '#F08A7E', 0) + E(75, 66, 6, 4, '#F08A7E', 0)
    s += P('M38 79 Q39 70 50 70 Q61 70 62 79 Q50 75 38 79 Z', '#B5413D')   # shouting frown
    s += P('M14 20 Q10 14 15 10 Q20 6 18 2', sw=2.4, stroke=RED) + P('M86 20 Q90 14 85 10 Q80 6 82 2', sw=2.4, stroke=RED)
    s += P('M70 22 L76 28 M76 22 L70 28', sw=2.6, stroke=RED)              # anger mark
    return s


@picto('scared', 'vystrašený')
def scared():
    s = face('#F6DDCB')
    s += P('M50 17 L46 6 M40 18 L33 8 M60 18 L67 8 M31 22 L22 14 M69 22 L78 14', sw=2.2)
    s += P('M27 36 Q33 29 41 32', sw=2.6) + P('M59 32 Q67 29 73 36', sw=2.6)
    for cx in (36, 64):
        s += E(cx, 48, 5.2, 6.6, L, 0) + C(cx + 1.8, 45.4, 1.9, '#FFFFFF', 0)
    s += E(50, 70, 5, 6.5, '#B5413D')
    s += P('M84 36 Q80 43 81 46 A3.6 3.6 0 0 0 88 46 Q89 43 84 36 Z', TEAR, 1.4)
    s += hand('open', 22, 92, 12, 1.3) + hand('open', 78, 92, -12, 1.3, mirror=True)
    s += P('M5 50 Q8 54 5 58 M95 50 Q92 54 95 58', sw=2)
    return s


@picto('tired', 'unavený')
def tired():
    s = '<g transform="rotate(-10 50 54)">' + face()
    s += P('M28 45 Q35 44 42 46', sw=2.2) + P('M58 46 Q65 44 72 45', sw=2.2)
    s += P('M29 53 Q35.5 58 42 53', sw=2.8) + P('M58 53 Q64.5 58 71 53', sw=2.8)
    s += P('M31 60 Q35.5 62 40 60 M60 60 Q64.5 62 69 60', sw=1.4, stroke='#B98A73')
    s += E(50, 73, 5, 7, '#B5413D') + '</g>'
    s += P('M80 16 Q84 20 80 24 M86 12 Q92 20 86 28', sw=2)  # small sigh lines
    return s


@picto('hurts', 'bolí')
def hurts():
    # hand on forehead, red pain marks
    d = 'M58 86 Q78 62 62 34'
    s = arm_back(d) + torso(-8, 65) + arm_fill(d) + headb(-8, 42) + face_small(42, 46, 'pain')
    s += hand('open', 59, 33, -62, 1.15)
    s += P('M18 18 L23 24 L19 26 L25 32', sw=2.4, stroke=RED) + P('M8 36 L15 37', sw=2.4, stroke=RED) + P('M80 14 L76 22 L81 22 L77 30', sw=2.4, stroke=RED)
    return s
