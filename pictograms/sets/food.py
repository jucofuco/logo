"""Food folder: one object, centered, filling most of the frame."""
from kit import *


@picto('glassOfWater', 'voda')
def glass_of_water():
    s = P('M30 16 L70 16 L65 86 L35 86 Z', GLASS)
    s += P('M31.6 36 Q41 32 50 36 Q59 40 68.4 36 L65.3 84 L34.7 84 Z', WATER, 0)
    s += P('M31.6 36 Q41 32 50 36 Q59 40 68.4 36', sw=1.8)
    s += P('M30 16 L70 16 L65 86 L35 86 Z')
    s += P('M38 44 L40 76', sw=2.4, stroke='#FFFFFF')
    return s


@picto('milk', 'mlieko')
def milk():
    # carton
    s = P('M38 10 H62 V17 H38 Z', '#FFFFFF')
    s += P('M30 33 L38 17 H62 L70 33 Z', '#FFFFFF')
    s += P('M30 33 H70 V88 H30 Z', '#FFFFFF')
    s += P('M30 50 H70 V72 H30 Z', '#5B8DEF')
    s += P('M50 53 Q44 61 44 64.5 A6 6 0 0 0 56 64.5 Q56 61 50 53 Z', '#FFFFFF', 1.6)
    return s


@picto('juice', 'džús')
def juice():
    s = P('M30 26 L66 26 L62 88 L34 88 Z', GLASS)
    s += P('M31.3 42 H64.7 L62.2 86 H33.8 Z', '#F7A23B', 0)
    s += P('M31.3 42 H64.7', sw=1.6)
    s += P('M52 60 L62 12 L74 10', 'none', 6.5, L) + P('M52 60 L62 12 L74 10', 'none', 3, RED)
    s += P('M30 26 L66 26 L62 88 L34 88 Z')
    s += P('M14 28 A14 14 0 0 1 42 28 Z', '#F7A23B')
    s += P('M28 28 V16 M28 28 L19 19 M28 28 L37 19', sw=1.4)
    return s


@picto('bread', 'chlieb')
def bread():
    # loaf + cut slice
    s = P('M8 72 Q8 40 40 38 Q66 40 70 58 V84 H20 Q8 84 8 72 Z', '#D9A066')
    s += P('M20 48 Q26 42 32 44 M34 43 Q40 38 46 40 M48 45 Q54 41 60 45', sw=2.2, stroke='#9A5B2E')
    s += P('M60 50 Q60 36 74 36 Q88 36 88 50 V86 H60 Z', '#B9824A')
    s += P('M63.5 51 Q63.5 40 74 40 Q84.5 40 84.5 51 V82.5 H63.5 Z', '#F6DDB0', 0)
    s += P('M68 56 h0.1 M78 52 h0.1 M72 66 h0.1 M80 70 h0.1 M68 76 h0.1', sw=2, stroke='#D9B27A')
    return s


@picto('roll', 'rožok')
def roll():
    s = P('M10 58 Q12 40 32 38 Q50 36 70 38 Q90 40 90 56 Q88 68 70 68 H30 Q10 70 10 58 Z', '#E1A45B')
    s += P('M26 40 Q21 53 26 66 M38 38 Q33 52 38 68 M50 37 Q45 52 50 68 M62 37 Q57 52 62 68 M74 39 Q69 52 74 66', sw=1.8, stroke='#A8652E')
    return s


@picto('apple', 'jablko')
def apple():
    s = P('M50 30 Q36 20 24 30 Q13 41 17 58 Q23 83 40 85 Q46 86 50 82 Q54 86 60 85 Q77 83 83 58 Q87 41 76 30 Q64 20 50 30 Z', RED)
    s += P('M50 30 Q49 20 53 12', sw=2.6)
    s += P('M53 20 Q62 11 73 15 Q64 25 53 20 Z', GREEN)
    s += E(33, 45, 4, 7, '#F6A39D', 0, rot=25)
    return s


@picto('banana', 'banán')
def banana():
    s = P('M20 30 Q20 76 64 82 Q84 84 90 72 Q70 74 52 64 Q32 52 28 28 Z', '#F7D154')
    s += P('M28 28 L23 21 Q19 24 20 30 Z', '#6B4226', 1.6)
    s += P('M90 72 L94 75 L93 68 Z', '#8A6D2B', 1.6)
    s += P('M26 40 Q30 64 62 76', sw=1.6, stroke='#D4A92A')
    return s


@picto('cheese', 'syr')
def cheese():
    s = P('M12 52 L62 30 L88 44 L38 66 Z', '#FBE08A')
    s += P('M12 52 L38 66 V84 L12 70 Z', '#F2C94C')
    s += P('M38 66 L88 44 V62 L38 84 Z', '#F7D46A')
    s += E(52, 50, 4.5, 2.4, '#E0B23A', 1.2) + E(68, 40, 3, 1.6, '#E0B23A', 1.2)
    s += E(56, 70, 3, 4, '#E0B23A', 1.2) + E(74, 61, 2.6, 3.4, '#E0B23A', 1.2) + E(24, 66, 2.6, 3.6, '#E0B23A', 1.2)
    return s


@picto('soup', 'polievka')
def soup():
    s = P('M42 44 Q38 38 42 32 Q46 26 42 20 M52 42 Q48 36 52 30 Q56 24 52 18 M62 44 Q58 38 62 32 Q66 26 62 20', sw=2, stroke='#9AA3AE')
    s += P('M14 58 H86 Q86 88 50 88 Q14 88 14 58 Z', '#FFFFFF')
    s += E(50, 58, 36, 8, '#F4A340')
    s += P('M60 58 L80 32', 'none', 5, L) + P('M60 58 L80 32', 'none', 2.4, '#ECEFF4')
    s += E(57, 60, 7, 3.6, '#ECEFF4', 1.8, rot=-10)
    return s


@picto('pasta', 'cestoviny')
def pasta():
    # spaghetti on a plate with a fork
    s = E(50, 70, 42, 16, '#FFFFFF') + E(50, 68, 30, 10, '#FFFFFF', 1.4)
    s += P('M20 66 Q24 50 50 48 Q76 50 80 66 Q50 74 20 66 Z', '#F7D16B')
    s += P('M24 62 Q30 54 36 62 Q42 70 48 60 Q54 52 60 62 Q66 70 72 60 Q75 56 77 62', sw=1.6, stroke='#C9962A')
    s += P('M28 56 Q36 50 42 56 Q48 62 54 54 Q60 48 68 56 Q72 60 74 56', sw=1.6, stroke='#C9962A')
    s += P('M38 52 Q46 47 52 51 Q58 55 64 50', sw=1.6, stroke='#C9962A')
    s += P('M58 58 L82 24', 'none', 5, L) + P('M58 58 L82 24', 'none', 2.4, '#ECEFF4')
    s += P('M77 30 Q80 33 87 30 L88 28 M78.5 28 L82 17 M82 29.5 L85.5 18.5 M85.5 30 L89 19', sw=2.2)
    s += E(48, 53, 7, 3.6, '#D9483B', 1.6)
    return s


@picto('yogurt', 'jogurt')
def yogurt():
    s = P('M29 36 L71 36 L66 88 L34 88 Z', '#FFFFFF')
    s += P('M30.6 54 H69.4 L67.7 72 H32.3 Z', '#F2A1B6', 0)
    s += P('M30.6 54 H69.4 M32.3 72 H67.7', sw=1.4)
    s += C(50, 63, 5, RED, 1.4) + P('M47 58.5 Q50 55 53 58.5', sw=1.4, stroke=GREEN)
    s += P('M24 29 H76 Q78 29 78 31 V35 Q78 37 76 37 H24 Q22 37 22 35 V31 Q22 29 24 29 Z', '#ECEFF4')
    s += P('M29 36 L71 36 L66 88 L34 88 Z')
    return s


@picto('cookie', 'keksík')
def cookie():
    s = C(50, 52, 32, '#D9A066')
    for (x, y, rx, ry, r) in [(38, 38, 4, 3, 20), (60, 36, 3.5, 2.6, -15), (66, 54, 4, 3, 30), (44, 58, 3.6, 2.8, 0), (32, 52, 3, 2.4, 40), (54, 72, 4, 3, -20), (36, 70, 3, 2.4, 10), (70, 70, 2.8, 2.2, 0)]:
        s += E(x, y, rx, ry, '#6B4226', 0, rot=r)
    return s


# ---------- more food (appended) ----------
import re as _re


def _scale(body, s, tx, ty):
    """Scales a drawing about the origin and keeps the outline width constant."""
    body = _re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{round(float(m.group(1)) / s, 2)}"', body)
    return f'<g transform="translate({tx} {ty}) scale({s})">{body}</g>'


@picto('pizza', 'pizza')
def pizza():
    s = P('M12 30 Q50 10 88 30 L50 94 Z', '#F7D154')
    s += P('M8 32 Q50 6 92 32 Q94 42 86 42 Q50 22 14 42 Q6 42 8 32 Z', '#D9A066')
    s += C(40, 52, 7, '#D6453D', 1.8) + C(60, 50, 6.5, '#D6453D', 1.8) + C(50, 70, 6, '#D6453D', 1.8)
    s += E(52, 58, 2.6, 1.8, GREEN, 1.2) + E(36, 64, 2.6, 1.8, GREEN, 1.2) + E(62, 64, 2.6, 1.8, GREEN, 1.2)
    s += P('M22 32 Q30 24 40 22', sw=2.4, stroke='#F2C98F')
    return s


@picto('cake', 'torta')
def cake():
    s = E(50, 90, 42, 6, '#ECEFF4')
    s += P('M14 54 H86 V86 Q86 90 82 90 H18 Q14 90 14 86 Z', '#E8B27B')
    s += P('M14 70 H86 V75 H14 Z', '#FFFFFF', 1.6)
    s += P('M12 56 Q12 40 28 40 H72 Q88 40 88 56 Q88 62 83 62 Q78 62 78 56 Q78 68 71 68 Q64 68 64 58 Q64 62 58 62 Q52 62 50 56 Q50 70 43 70 Q36 70 36 58 Q36 62 29 62 Q22 62 22 56 Q22 62 17 62 Q12 62 12 56 Z', '#F9C6D8')
    s += P('M45 22 H55 V40 H45 Z', '#8DBBEA') + P('M45 28 L55 26 M45 34 L55 32', sw=1.6, stroke='#FFFFFF')
    s += P('M50 6 Q58 16 50 22 Q42 16 50 6 Z', '#F4A340', 1.8)
    s += C(28, 38, 4.5, RED, 1.8) + C(72, 38, 4.5, RED, 1.8)
    return s


@picto('butter', 'maslo')
def butter():
    s = P('M8 56 L22 36 H92 L78 56 Z', '#FFF0A8')
    s += P('M78 56 L92 36 V68 L78 88 Z', '#EBC94A')
    s += P('M8 56 H78 V88 H8 Z', '#F7DC6B')
    s += P('M8 56 H44 V88 H8 Z', '#FFFFFF') + P('M8 66 H44 M8 78 H44', sw=2, stroke='#5B8DEF')
    s += P('M44 56 L58 36', sw=2)
    s += E(66, 46, 7, 2.2, '#FFF8CF', 0, rot=-35)
    s += P('M58 74 Q66 70 72 72', sw=1.6, stroke='#D4A92A')
    return s


@picto('rice', 'ryža')
def rice():
    s = P('M16 54 Q16 20 50 18 Q84 20 84 54 Z', '#FFFFFF')
    for (x, y, r) in [(34, 36, 20), (50, 28, -30), (66, 36, -20), (42, 46, 60), (58, 46, 10), (28, 48, -50), (72, 48, 40)]:
        s += E(x, y, 4.5, 1.8, '#DADFE8', 0, rot=r)
    s += P('M60 30 L88 6', 'none', 6, L) + P('M60 30 L88 6', 'none', 2.6, '#D9A066')
    s += P('M68 36 L94 14', 'none', 6, L) + P('M68 36 L94 14', 'none', 2.6, '#D9A066')
    s += P('M10 52 H90 Q90 88 50 90 Q10 88 10 52 Z', '#4A78C2')
    s += P('M26 62 Q50 72 74 62', sw=1.8, stroke='#FFFFFF') + C(50, 78, 4, '#FFFFFF', 0)
    return s


def _apple_s():
    s = P('M0 -14 Q-12 -22 -20 -12 Q-27 -2 -22 12 Q-16 26 -6 26 Q0 27 0 24 Q0 27 6 26 Q16 26 22 12 Q27 -2 20 -12 Q12 -22 0 -14 Z', RED)
    s += P('M0 -14 Q0 -22 3 -27', sw=2.4) + P('M3 -22 Q12 -30 20 -26 Q14 -17 3 -22 Z', GREEN, 1.8)
    s += E(-12, -2, 3, 6, '#F6A39D', 0, rot=20)
    return s


@picto('fruit', 'ovocie')
def fruit():
    s = ''
    # grapes at the back
    for (x, y) in [(42, 20), (56, 20), (35, 32), (49, 32), (63, 32), (42, 44), (56, 44)]:
        s += C(x, y, 7.5, '#8A5CC4', 1.8) + C(x - 2, y - 2.4, 1.8, '#C5A8E8', 0)
    s += P('M49 12 Q49 6 56 3', sw=2.4) + P('M52 10 Q60 2 68 8 Q62 16 52 10 Z', GREEN, 1.8)
    s += _scale(_apple_s(), 0.95, 28, 66)
    s += C(70, 68, 19, '#F59E2E') + E(63, 60, 3.4, 6, '#F9C376', 0, rot=30)
    s += P('M70 50 Q70 46 74 44', sw=2) + P('M72 48 Q80 42 86 46 Q80 52 72 48 Z', GREEN, 1.6)
    s += C(76, 74, 1, '#D9801C', 1) + C(66, 78, 1, '#D9801C', 1) + C(79, 66, 1, '#D9801C', 1)
    return s


@picto('vegetables', 'zelenina')
def vegetables():
    s = ''
    # broccoli, back left
    s += P('M20 44 H38 L40 80 H18 Z', '#9BD27A')
    for (x, y, r) in [(16, 30, 12), (30, 20, 13), (44, 30, 12), (30, 38, 12)]:
        s += C(x, y, r, '#3BA55D')
    s += P('M22 50 Q30 54 38 50', sw=1.8, stroke='#6FB14F')
    # carrot, right, tilted
    s += P('M74 34 L84 36 L64 94 Q62 96 60 92 Z', '#F4801F')
    s += P('M70 46 L76 47 M68 58 L74 59 M65 72 L70 73', sw=1.6, stroke='#B85A0E')
    s += P('M79 36 Q70 20 62 10 Q70 12 78 24 Q80 6 84 4 Q86 16 82 34 Q94 20 96 24 Q92 32 82 38 Z', '#3BA55D', 1.8)
    # tomato, front
    s += C(40, 74, 19, RED) + E(32, 66, 3.4, 5, '#F6A39D', 0, rot=30)
    s += P('M40 58 L35 53 L38 61 L30 60 L37 65 L44 65 L50 60 L43 61 L45 53 Z', GREEN, 1.6)
    return s


@picto('iceCream', 'zmrzlina')
def ice_cream():
    s = P('M30 50 L50 96 L70 50 Z', '#E1A45B')
    s += P('M36 62 L64 62 M41 74 L59 74 M33 52 L58 90 M43 52 L66 80 M67 52 L42 90 M57 52 L34 80', sw=1.6, stroke='#A8652E')
    s += C(50, 28, 17, '#8A5A3C') + E(43, 22, 3.4, 6, '#B58360', 0, rot=30)
    s += P('M28 52 Q24 38 38 36 Q50 32 62 36 Q76 38 72 52 Q70 58 65 55 Q62 62 56 56 Q51 63 46 56 Q40 62 36 55 Q30 58 28 52 Z', '#F6A5C0')
    s += C(50, 10, 4.6, RED, 1.8) + P('M50 6 Q52 2 56 2', sw=1.6, stroke=GREEN)
    return s


@picto('chocolate', 'čokoláda')
def chocolate():
    s = '<g transform="rotate(-12 50 50)">'
    s += P('M26 6 H74 V94 H26 Z', '#8A5A3C')
    for r in range(3):
        for c in range(2):
            x, y = 29 + c * 22.5, 9 + r * 15
            s += P(f'M{x} {y} h19.5 v12.5 h-19.5 Z', '#A86F4A', 1.4)
    s += P('M22 52 L50 58 L78 52 V96 H22 Z', '#8DBBEA')
    s += P('M22 52 L32 58 L42 52 L52 58 L62 52 L72 58 L78 52 L78 46 L22 46 Z', '#C9D3E0', 1.6)
    s += P('M22 52 L50 58 L78 52 V96 H22 Z', '#5B8DEF')
    s += C(50, 76, 9, '#FFFFFF', 1.6) + P('M50 70 L52 75 L57 75 L53 78 L55 83 L50 80 L45 83 L47 78 L43 75 L48 75 Z', '#F4A340', 0.8)
    s += '</g>'
    return s


def _egg(cx, cy, k, col, hi):
    s = P('M0 -22 C14 -22 20 0 20 10 C20 24 12 30 0 30 C-12 30 -20 24 -20 10 C-20 0 -14 -22 0 -22 Z', col)
    s += E(-9, 2, 3, 7, hi, 0, rot=12)
    return _scale(s, k, cx, cy)


@picto('eggs', 'vajcia')
def eggs():
    return _egg(30, 36, 1.1, '#D8A872', '#EBCFA8') + _egg(70, 36, 1.1, '#FBF6EC', '#FFFFFF') + _egg(50, 62, 1.1, '#F0DCC0', '#FFF8EA')


@picto('chicken', 'kurča')
def chicken():
    # like ARASAAC (pollo asado): roast chicken seen from the side on a plate, legs up with white
    # bone ends; no lines in the middle of the body, so it does not read as a face
    s = E(50, 84, 46, 9, '#ECEFF4') + E(50, 82, 34, 5, 'none', 1.4, '#C5CCD8')
    s += P('M12 62 Q10 38 34 32 Q58 26 76 40 Q90 52 86 70 Q82 82 60 82 H28 Q14 80 12 62 Z', '#E1953F')
    s += P('M20 52 Q24 40 38 37', sw=2.6, stroke='#F2B974')
    for (x0, y0, x1, y1) in [(64, 46, 80, 18), (50, 46, 58, 14)]:
        s += P(f'M{x0} {y0} L{x1} {y1}', 'none', 8, L) + P(f'M{x0} {y0} L{x1} {y1}', 'none', 4, '#FFFFFF')
        s += C(x1 - 2.6, y1 - 1, 3.4, '#FFFFFF') + C(x1 + 2.6, y1 + 1.4, 3.4, '#FFFFFF')
        s += P(f'M{x0 - 8} {y0 + 16} Q{x0 - 10} {y0 - 2} {x0 + (x1 - x0) * 0.35} {y0 + (y1 - y0) * 0.35} '
               f'Q{x0 + 12} {y0 + 2} {x0 + 8} {y0 + 16} Q{x0} {y0 + 22} {x0 - 8} {y0 + 16} Z', '#C97A2B')
    return s
