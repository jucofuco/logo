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


def heart(cx, cy, s, fill=RED, sw=W):
    """Heart centered at cx,cy, about 2*s wide."""
    return P(f'M{cx} {cy + s * 0.9} C{cx - s * 1.3} {cy - s * 0.1} {cx - s * 0.9} {cy - s * 1.1} {cx} {cy - s * 0.45} '
             f'C{cx + s * 0.9} {cy - s * 1.1} {cx + s * 1.3} {cy - s * 0.1} {cx} {cy + s * 0.9} Z', fill, sw)


def snowflake(cx, cy, r, color='#6EA8D8'):
    s = ''
    for a in (0, 60, 120):
        s += f'<path d="M{cx} {cy - r} V{cy + r}" transform="rotate({a} {cx} {cy})" fill="none" stroke="{color}" stroke-width="2"/>'
    return s


@picto('love', 'láska')
def love():
    # hugs a big heart, small hearts float up (idea: ARASAAC 37721, hand on the heart)
    s = bust(0, 30, 18)
    s += happy_eye(43.5, 32) + happy_eye(56.5, 32) + P('M44 39 Q50 44 56 39', sw=2.2)
    s += E(39, 38, 3.5, 2.4, '#F7A8A0', 0) + E(61, 38, 3.5, 2.4, '#F7A8A0', 0)
    s += heart(50, 76, 24)
    s += arm('M12 104 Q14 98 24 96') + arm('M88 104 Q86 98 76 96')
    s += hand('open', 26, 97, 28, 1.1) + hand('open', 74, 97, -28, 1.1, mirror=True)
    s += heart(14, 22, 7, '#F28B9B', 1.6) + heart(86, 16, 8, '#F28B9B', 1.6) + heart(84, 40, 5, '#F28B9B', 1.4)
    return s


@picto('surprised', 'prekvapený')
def surprised():
    # brows up high, round eyes, small round mouth (idea: ARASAAC 35529)
    s = face()
    s += P('M27 36 Q35 28 43 34', sw=2.6) + P('M57 34 Q65 28 73 36', sw=2.6)
    for cx in (36, 64):
        s += C(cx, 50, 7.5, '#FFFFFF') + C(cx, 50, 3.6, L, 0) + C(cx + 1.2, 48.6, 1.2, '#FFFFFF', 0)
    s += E(50, 72, 6, 7.5, '#B5413D')
    s += P('M8 14 L15 21 M3 30 L11 32 M92 14 L85 21 M97 30 L89 32', sw=2.4, stroke=ARROW_C)
    return s


ARROW_C = '#F28C28'


@picto('curious', 'zvedavý')
def curious():
    # one brow up, looks through a magnifying glass (big eye behind the lens)
    s = face()
    s += P('M27 40 Q35 37 43 41', sw=2.6) + P('M57 34 Q65 28 73 34', sw=2.6)
    s += eye_open(36, 52, 5.2, py=0)
    s += P('M42 72 Q50 76 58 70', sw=2.4)
    s += P('M74 64 L92 94', 'none', 8 + 2 * W, L) + P('M74 64 L92 94', 'none', 8, '#8A5A2B')
    s += C(64, 50, 15, '#DDF0FB', 3.5) + C(64, 50, 15, 'none', 1, '#FFFFFF')
    s += E(64, 50, 6.5, 8.5, L, 0) + C(66.5, 46.5, 2.5, '#FFFFFF', 0)
    s += P('M56 41 Q58 39 61 38.5', sw=1.8, stroke='#FFFFFF')
    return s


@picto('embarrassed', 'v rozpakoch')
def embarrassed():
    # looks down and aside, big red cheeks, small wobbly smile (idea: ARASAAC 6922, blush)
    s = face()
    s += P('M27 42 Q34 39 42 43', sw=2.4) + P('M58 43 Q66 39 73 42', sw=2.4)
    s += P('M30 55 Q36 59 42 55', sw=2.6) + P('M58 55 Q64 59 70 55', sw=2.6)
    s += E(30, 66, 9, 6, '#F48C84', 0) + E(70, 66, 9, 6, '#F48C84', 0)
    s += P('M24 64 L27 69 M29 63 L32 68 M34 63 L37 68 M64 63 L67 68 M69 63 L72 68 M74 64 L77 69', sw=1.4, stroke='#C9504A')
    s += P('M42 75 Q46 72 50 75 Q54 78 58 75', sw=2.2)
    s += P('M84 30 Q80 37 81 40 A3.6 3.6 0 0 0 88 40 Q89 37 84 30 Z', TEAR, 1.4)
    return s


@picto('bored', 'znudený')
def bored():
    # head leans on a hand, half-shut eyes look up, flat mouth (idea: ARASAAC 6873)
    s = '<g transform="rotate(12 50 54)">' + face()
    s += P('M28 44 H42', sw=2.4) + P('M58 44 H72', sw=2.4)
    for cx in (35, 65):
        s += E(cx, 53, 4.2, 4.6, L, 0) + P(f'M{cx - 6} 51.5 H{cx + 6} V46 H{cx - 6} Z', SK, 0) + P(f'M{cx - 6} 51.5 H{cx + 6}', sw=2.4)
    s += P('M42 74 H58', sw=2.6) + '</g>'
    s += P('M6 108 Q8 104 13 104', 'none', 13 + 2 * W, L) + P('M6 108 Q8 104 13 104', 'none', 13, SHIRT)
    s += hand('open', 15, 105, 38, 1.3)
    s += P('M82 12 Q86 16 82 20 Q78 24 82 28', sw=2) + P('M90 20 Q94 24 90 28', sw=2)
    return s


@picto('sick', 'chorý')
def sick():
    # pale green face, sad brows, droopy eyes, thermometer in the mouth (idea: ARASAAC 7040)
    s = face('#DCE9C5')
    s += P('M27 44 Q34 38 42 40', sw=2.4) + P('M58 40 Q66 38 73 44', sw=2.4)
    s += P('M29 52 Q35.5 57 42 52', sw=2.6) + P('M58 52 Q64.5 57 71 52', sw=2.6)
    s += P('M40 74 Q50 68 60 74', sw=2.4)
    s += P('M52 71 L88 86', 'none', 5 + 2 * W, L) + P('M52 71 L88 86', 'none', 5, '#FFFFFF')
    s += P('M52 71 L62 75', 'none', 3, RED) + C(52, 71, 3.2, RED, 1.6)
    s += P('M80 20 Q76 27 77 30 A3.6 3.6 0 0 0 84 30 Q85 27 80 20 Z', TEAR, 1.4)
    s += P('M17 66 L22 66 M14 74 L20 72', sw=1.8, stroke='#7FA35B')
    return s


@picto('hot', 'horúco')
def hot():
    # red face, sweat drops, the sun burns (idea: ARASAAC 2300)
    s = face('#F9BDA6')
    s += P('M28 42 Q35 39 42 42', sw=2.4) + P('M58 42 Q65 39 72 42', sw=2.4)
    s += P('M29 50 Q35.5 54 42 50', sw=2.6) + P('M58 50 Q64.5 54 71 50', sw=2.6)
    s += E(29, 64, 7, 4.5, '#EE7B6E', 0) + E(71, 64, 7, 4.5, '#EE7B6E', 0)
    s += P('M38 70 Q50 66 62 70 Q62 80 50 80 Q38 80 38 70 Z', '#B5413D')
    s += P('M44 76 Q50 74 56 76 L55 86 Q50 90 45 86 Z', TONGUE, 1.8)
    for x, y, r in ((22, 44, 3.4), (80, 52, 3.4), (16, 58, 2.6)):
        s += P(f'M{x} {y - 2.6 * r} Q{x - r} {y - r} {x - r} {y} A{r} {r} 0 0 0 {x + r} {y} Q{x + r} {y - r} {x} {y - 2.6 * r} Z', TEAR, 1.4)
    s += C(86, 14, 9, '#F6D35B')
    s += P('M86 0 V2 M72 14 H70 M76 4 L74 2 M76 24 L74 26 M96 24 L98 26', sw=2.4, stroke='#E8A21A')
    return s


@picto('cold', 'zima')
def cold():
    # blue face, wool hat and scarf, chattering teeth, snowflakes
    s = C(50, 56, 32, '#D3E4F4')
    s += P('M16 50 Q16 14 50 14 Q84 14 84 50 Z', '#E5534B')
    s += P('M14 46 H86 V56 H14 Z', '#F5F5F5') + C(50, 11, 6.5, '#F5F5F5')
    s += P('M30 22 V44 M42 18 V44 M58 18 V44 M70 22 V44', sw=1.4, stroke='#B8403A')
    s += P('M28 62 Q34 61 41 58', sw=2.4) + P('M59 58 Q66 61 72 62', sw=2.4)
    for cx in (35, 65):
        s += eye_open(cx, 68, 4.2)
    s += P('M38 77 H62 V84 H38 Z', '#FFFFFF') + P('M38 80.5 H62 M44 77 V84 M50 77 V84 M56 77 V84', sw=1.4)
    s += P('M16 86 Q50 96 84 86 L86 100 H14 Z', '#3BA55D') + P('M66 92 L72 104 L80 102 L74 90 Z', '#3BA55D')
    s += P('M8 60 Q5 64 8 68 Q11 72 8 76 M92 60 Q95 64 92 68 Q89 72 92 76', sw=2)
    s += snowflake(10, 14, 6) + snowflake(90, 12, 6) + snowflake(94, 40, 4)
    return s
