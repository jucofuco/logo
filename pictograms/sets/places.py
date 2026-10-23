"""Places folder: a building or a scene with one telling feature."""
from kit import *

WALL = '#F7E3B5'
GLASSB = '#BFE3F7'


def _win(x, y, w, h, fill=GLASSB, cross=True):
    s = P(f'M{x} {y} h{w} v{h} h-{w} Z', fill, 1.8)
    if cross:
        s += P(f'M{x + w / 2} {y} v{h} M{x} {y + h / 2} h{w}', sw=1.4)
    return s


@picto('home', 'domov')
def home():
    s = P('M66 12 H78 V34 H66 Z', '#B5413D')
    s += P('M18 46 H82 V90 H18 Z', WALL)
    s += P('M6 50 L50 12 L94 50 Z', RED)
    s += C(50, 36, 6, GLASSB, 1.8)
    s += P('M42 62 Q42 56 50 56 Q58 56 58 62 V90 H42 Z', '#B9824A') + C(54, 76, 1.8, '#FBD34D', 1)
    s += _win(23, 58, 14, 14) + _win(63, 58, 14, 14)
    return s


@picto('school', 'škola')
def school():
    s = P('M38 24 H62 V50 H38 Z', '#F2B66D')
    s += P('M34 26 L50 10 L66 26 Z', '#4A78C2')
    s += P('M50 10 V2', sw=2) + P('M50 2 H60 L57 5 L60 8 H50', RED, 1.6)
    s += P('M43 42 V34 Q43 29 50 29 Q57 29 57 34 V42 Z', '#7A5A3A', 1.6)
    s += P('M50 31 Q45 33 45 38 L44 41 H56 L55 38 Q55 33 50 31 Z', '#FBD34D', 1.4) + C(50, 42, 1.6, L, 0)
    s += P('M8 50 H92 V90 H8 Z', '#E58B5A')
    s += _win(14, 58, 14, 14) + _win(72, 58, 14, 14)
    s += P('M40 90 V68 Q40 62 50 62 Q60 62 60 68 V90 Z', '#8DBBEA')
    s += P('M50 62 V90', sw=1.6)
    s += P('M36 90 H64 V94 H36 Z', '#D8DEE9', 1.6)
    return s


@picto('classroom', 'trieda')
def classroom():
    s = P('M8 8 H92 V60 H8 Z', '#B9824A')
    s += P('M13 13 H87 V55 H13 Z', '#2E7D4F', 1.6)
    s += P('M22 30 Q28 22 34 30 Q40 38 46 30', sw=2.4, stroke='#FFFFFF')
    s += C(70, 28, 7, 'none', 2.4, '#FFFFFF') + P('M24 44 H50', sw=2.4, stroke='#FFFFFF')
    s += P('M60 42 L76 46', sw=2.4, stroke='#FFFFFF')
    s += P('M8 60 H92 V63 H8 Z', '#8A5A3C', 1.6)
    s += P('M14 68 H54 V74 H14 Z', '#F4A340')
    s += P('M20 74 V94 M48 74 V94', sw=3)
    s += P('M18 94 H26 M42 94 H54', sw=2.4)
    s += P('M26 60 Q40 56 54 60 L50 68 H30 Z', '#FFFFFF', 0) if False else ''
    s += P('M64 68 H90 V74 H64 Z', '#F4A340') + P('M70 74 V94 M84 74 V94', sw=3)
    s += P('M64 68 L68 56 H86 L90 68', '#FFFFFF', 1.8) if False else ''
    s += C(26, 62, 0, 'none')
    s += P('M18 66 Q18 56 28 56 Q34 56 34 66 Z', RED, 1.8) + P('M26 56 Q26 52 29 50', sw=1.6)
    return s


@picto('zoo', 'zoo')
def zoo():
    Y, SP = '#F4C24E', '#B9824A'
    s = P('M32 94 Q40 56 42 32 L62 34 Q64 62 68 94 Z', Y)
    for (x, y, r) in [(48, 46, 4.5), (56, 60, 5), (46, 70, 5), (60, 80, 4.5), (50, 36, 3)]:
        s += C(x, y, r, SP, 1.2)
    s += P('M44 20 L42 8', sw=2.4) + C(42, 7, 3, SP, 1.6) + P('M56 18 L58 6', sw=2.4) + C(58, 5, 3, SP, 1.6)
    s += E(40, 22, 7, 4, Y, 1.8, rot=30)
    s += E(55, 28, 14, 11, Y, rot=-8) + E(70, 33, 8, 6.5, '#E8B060', 1.8, rot=10)
    s += E(75, 32, 1.8, 1.4, L, 0) + eye_open(58, 25, r=3.8)
    s += P('M6 78 H94 M6 90 H94', 'none', 5, L) + P('M6 78 H94 M6 90 H94', 'none', 2, '#C98B52')
    for x in (12, 36, 64, 88):
        s += P(f'M{x - 4} 70 H{x + 4} V96 H{x - 4} Z', '#C98B52', 1.8)
    return s


@picto('sea', 'more')
def sea():
    s = P('M12 6 H88 Q94 6 94 12 V88 Q94 94 88 94 H12 Q6 94 6 88 V12 Q6 6 12 6 Z', '#D8F0FB')
    s += C(72, 26, 10, '#FBD34D', 1.8)
    s += P('M72 10 V6 M86 26 H90 M82 16 L85 13 M58 26 H54 M62 16 L59 13', sw=2, stroke='#F4A340')
    s += P('M34 46 H70 L62 58 H42 Z', RED) + P('M52 12 V46', sw=2)
    s += P('M52 14 L28 44 H52 Z', '#FFFFFF') + P('M55 22 L74 44 H55 Z', '#FFFFFF')
    s += P('M6 60 Q18 52 30 60 T54 60 T78 60 T94 58 V88 Q94 94 88 94 H12 Q6 94 6 88 Z', '#6EC1F0')
    s += P('M6 74 Q18 66 30 74 T54 74 T78 74 T94 72 V88 Q94 94 88 94 H12 Q6 94 6 88 Z', '#4A9BDD')
    s += P('M20 84 Q26 80 32 84 M60 86 Q66 82 72 86', sw=1.8, stroke='#FFFFFF')
    return s


@picto('shop', 'obchod')
def shop():
    s = P('M12 40 H88 V90 H12 Z', WALL)
    s += P('M32 6 H68 V20 H32 Z', '#8DBBEA') + P('M42 17 L44 9 H56 L58 17 Z', '#F4A340', 1.4)
    s += P('M10 24 H90 L94 44 Q88 52 82 44 Q76 52 70 44 Q64 52 58 44 Q52 52 46 44 Q40 52 34 44 Q28 52 22 44 Q16 52 6 44 Z', '#FFFFFF')
    for x in (10, 30, 50, 70):
        s += P(f'M{x} 24 H{x + 10} L{x + 12} 45 Q{x + 8} 50 {x + 3} 46 Z', RED, 1.2)
    s += P('M10 24 H90 L94 44 Q88 52 82 44 Q76 52 70 44 Q64 52 58 44 Q52 52 46 44 Q40 52 34 44 Q28 52 22 44 Q16 52 6 44 Z')
    s += P('M18 58 H54 V82 H18 Z', GLASSB, 1.8) + C(30, 74, 5, RED, 1.4) + P('M40 82 V70 H50 V82', '#F4A340', 1.4)
    s += P('M62 58 H80 V90 H62 Z', '#8DBBEA', 1.8) + P('M62 74 H80', sw=1.4) + C(66, 72, 1.4, L, 0)
    return s


@picto('shoppingMall', 'nákupné centrum')
def shopping_mall():
    s = P('M4 36 H96 V90 H4 Z', '#D5D9F0')
    s += P('M4 36 H96 V42 H4 Z', '#9AA3D6')
    for (x, y, kind) in [(6, 48, 'bottle'), (19, 48, 'shoe'), (70, 48, 'shirt'), (83, 48, 'ring')]:
        s += P(f'M{x} {y} h11 v18 h-11 Z', '#F2F6FA', 1.6)
        if kind == 'bottle':
            s += P(f'M{x + 4} {y + 15} V{y + 8} Q{x + 4} {y + 5} {x + 7} {y + 5} Q{x + 10} {y + 5} {x + 10} {y + 8} V{y + 15} Z', '#F4A340', 1.4)
        elif kind == 'shoe':
            s += P(f'M{x + 2} {y + 6} H{x + 7} L{x + 8} {y + 10} L{x + 12} {y + 11} V{y + 14} H{x + 2} Z', RED, 1.4)
        elif kind == 'shirt':
            s += P(f'M{x + 3} {y + 3} L{x} {y + 6} L{x + 3} {y + 9} L{x + 4} {y + 8} V{y + 15} H{x + 10} V{y + 8} L{x + 11} {y + 9} L{x + 13} {y + 6} L{x + 10} {y + 3} Z', '#5B8DEF', 1.4)
        else:
            s += C(x + 7, y + 11, 4, 'none', 1.8, '#E8B520') + C(x + 7, y + 6, 1.6, '#8DBBEA', 1)
    s += P('M32 20 H68 V90 H32 Z', '#FFFFFF')
    s += P('M32 20 H68 V26 H32 Z', '#9AA3D6')
    s += C(50, 41, 12, '#FBD34D', 1.8)
    s += P('M44 37 H56 L57 48 H43 Z', RED, 1.6) + P('M47 37 Q47 32 50 32 Q53 32 53 37', sw=1.6)
    s += P('M38 90 V62 H50 V90 M50 62 H62 V90', GLASSB, 1.8) + P('M50 62 V90', sw=1.6)
    s += P('M34 60 H66', sw=2.4)
    s += P('M50 20 V12 M50 12 H58 V16 H50', RED, 1.6)
    return s


@picto('park', 'park')
def park():
    s = C(80, 14, 7, '#FBD34D', 1.6)
    s += P('M24 52 H34 V82 H24 Z', '#8A5A3C') + P('M70 56 H78 V82 H70 Z', '#8A5A3C')
    s += C(29, 32, 22, '#3BA55D') + C(44, 40, 12, '#52B96F', 1.8)
    s += C(74, 42, 16, '#52B96F') + C(24, 28, 4, '#6FCB88', 0)
    s += P('M6 86 Q30 80 50 84 Q74 88 94 82 V94 H6 Z', '#9BD27A')
    s += P('M32 62 H70 V68 H32 Z', '#C98B52') + P('M34 72 H68 V77 H34 Z', '#C98B52')
    s += P('M36 68 V86 M66 68 V86', 'none', 5, L) + P('M36 68 V86 M66 68 V86', 'none', 2, '#8A5A3C')
    s += P('M30 60 V74 M72 60 V74', sw=2.4)
    return s


@picto('bathroom', 'kúpeľňa')
def bathroom():
    s = P('M88 4 H76 Q69 4 68 14', 'none', 7, L) + P('M88 4 H76 Q69 4 68 14', 'none', 3, '#C5CCD8')
    s += E(58, 20, 14, 5, '#C5CCD8', 1.8, rot=-18)
    s += P('M50 28 L48 38 M58 28 L58 40 M66 24 L68 36', sw=2.4, stroke=WATER)
    for (x, y, r) in [(20, 52, 8), (32, 44, 11), (48, 46, 10), (62, 50, 9), (76, 52, 7)]:
        s += C(x, y, r, '#FFFFFF')
    s += C(34, 41, 2.4, GLASSB, 0) + C(46, 43, 2, GLASSB, 0)
    s += P('M6 56 H94 V62 Q94 84 74 84 H26 Q6 84 6 62 Z', '#F2F6FA')
    s += P('M6 62 H94', sw=1.6, stroke='#9BD3F2')
    s += P('M20 84 L16 92 H28 L28 84 M80 84 L84 92 H72 L72 84', '#C5CCD8', 1.8)
    s += P('M14 70 Q16 78 24 78', sw=2, stroke='#FFFFFF')
    return s


def _books(x0, yb, specs):
    s = ''
    x = x0
    for (w, h, col) in specs:
        s += P(f'M{x} {yb - h} h{w} V{yb} h-{w} Z', col, 1.6) + P(f'M{x} {yb - h + 4} h{w}', sw=1.2, stroke='#FFFFFF')
        x += w
    return s


@picto('library', 'knižnica')
def library():
    s = P('M8 6 H92 V94 H8 Z', '#C98B52')
    s += P('M13 11 H87 V89 H13 Z', '#9C6A3C', 1.6)
    for yb in (36, 62, 88):
        s += P(f'M13 {yb} H87 V{yb + 3} H13 Z', '#C98B52', 1.6) if yb < 88 else ''
    s += _books(15, 36, [(8, 22, RED), (7, 18, '#5B8DEF'), (9, 24, '#F7D154'), (7, 20, GREEN), (8, 16, '#F29AB8'), (9, 22, '#8A5CC4')])
    s += '<g transform="rotate(14 80 36)">' + P('M70 14 h8 V36 h-8 Z', '#F4A340', 1.6) + '</g>'
    s += _books(15, 62, [(7, 18, '#F29AB8'), (9, 22, '#4A78C2'), (8, 24, '#F4A340'), (7, 20, RED), (9, 16, '#52B96F'), (8, 22, '#F7D154'), (8, 19, '#5B8DEF')])
    s += _books(15, 87, [(9, 20, GREEN), (8, 23, RED), (7, 16, '#F7D154'), (9, 21, '#8A5CC4'), (8, 24, '#5B8DEF'), (8, 18, '#F4A340')])
    s += P('M62 87 L56 66 L72 62 L74 87 Z', '#FFFFFF', 0) if False else ''
    s += P('M64 87 V68 Q64 66 66 66 H82 Q84 66 84 68 V87 Z', '#FFFFFF', 1.6) + P('M74 66 V87', sw=1.6) + P('M67 72 H72 M67 77 H72 M76 72 H81 M76 77 H81', sw=1.2, stroke='#9AA3B5')
    return s


@picto('cinema', 'kino')
def cinema():
    s = P('M20 14 H80 V58 H20 Z', '#F2F6FA', 3.5)
    s += P('M22 16 H78 V56 H22 Z', '#2F3A52', 0)
    s += P('M44 26 L62 36 L44 46 Z', '#FBD34D', 2)
    s += P('M4 6 H96 V16 H4 Z', '#B5413D')
    s += P('M6 16 H22 Q16 40 22 62 H6 Z', RED) + P('M78 16 H94 V62 H78 Q84 40 78 16 Z', RED)
    s += P('M12 18 Q10 40 14 60 M86 18 Q88 40 84 60', sw=1.4, stroke='#B5413D')
    for x in (10, 38, 66):
        s += P(f'M{x} 94 V78 Q{x} 68 {x + 6} 68 H{x + 18} Q{x + 24} 68 {x + 24} 78 V94 Z', '#8A5CC4')
        s += P(f'M{x - 4} 94 V80 H{x + 2} V94 M{x + 22} 94 V80 H{x + 28} V94', '#6B3FA0', 1.6) if False else ''
    s += P('M8 94 H92', sw=1.8)
    return s


@picto('museum', 'múzeum')
def museum():
    ST = '#E8DDC9'
    s = P('M6 30 L50 8 L94 30 Z', ST)
    s += P('M8 30 H92 V38 H8 Z', '#D8CBB0')
    s += P('M16 38 H84 V82 H16 Z', '#F6EFE0', 1.8)
    # framed picture and statue between the columns
    s += P('M28 46 H48 V68 H28 Z', '#F7D154', 2.4) + P('M28 68 L36 56 L42 62 L48 54 V68 Z', '#E5534B', 1.6) + C(36, 52, 2.6, '#FFFFFF', 0)
    s += P('M60 82 V72 H76 V82 Z', '#9AA3B5', 1.8)
    s += P('M68 72 Q60 66 66 58 Q68 54 66 50 Q72 48 72 56 Q72 62 74 66 Q75 70 72 72 Z', '#B8BFCC', 1.8)
    s += P('M16 38 V82 M84 38 V82', sw=2.4)
    s += P('M12 38 H20 V82 H12 Z M80 38 H88 V82 H80 Z', ST, 1.8)
    s += P('M8 82 H92 V88 H8 Z', '#D8CBB0') + P('M4 88 H96 V94 H4 Z', ST)
    s += P('M50 14 Q42 14 44 22 L46 28 H54 L56 22 Q58 14 50 14 Z', '#F4A340', 1.4) if False else ''
    s += C(50, 22, 4, '#F4A340', 1.6)
    return s


@picto('restaurant', 'reštaurácia')
def restaurant():
    s = P('M26 62 Q26 26 50 26 Q74 26 74 62 Z', '#D8DEE9')
    s += C(50, 22, 4.6, '#AEB6C4') + P('M34 50 Q36 38 44 34', sw=2.4, stroke='#FFFFFF')
    s += P('M20 62 H80 Q80 70 74 70 H26 Q20 70 20 62 Z', '#C5CCD8')
    # fork and knife
    s += P('M10 30 V46 Q10 52 14 52 Q18 52 18 46 V30 M14 30 V52 M14 52 V84', 'none', 5, L) if False else ''
    s += P('M8 28 V44 Q8 50 13 50 Q18 50 18 44 V28 M13 28 V50', sw=2) + P('M13 50 V82', 'none', 6, L) + P('M13 50 V82', 'none', 2.6, '#ECEFF4')
    s += P('M88 28 Q96 34 90 54 H88 Z', '#ECEFF4', 2) + P('M88 54 V82', 'none', 6, L) + P('M88 54 V82', 'none', 2.6, '#ECEFF4')
    s += P('M4 82 H96 V94 H4 Z', RED)
    for x in (4, 28, 52, 76):
        s += P(f'M{x + 12} 82 h12 v6 h-12 Z M{x} 88 h12 v6 h-12 Z', '#FFFFFF', 0)
    s += P('M4 82 H96 V94 H4 Z', 'none')
    return s


@picto('pool', 'bazén')
def pool():
    s = P('M4 40 H96 V48 H4 Z', '#E3E7EE')
    s += P('M8 48 H92 V86 Q92 92 86 92 H14 Q8 92 8 86 Z', '#6EC1F0')
    s += P('M8 62 H92 M8 76 H92 M30 48 V92 M50 48 V92 M70 48 V92', sw=1, stroke='#9BD3F2')
    s += P('M8 48 Q16 44 24 48 T40 48 T56 48 T72 48 T92 48', sw=2, stroke='#FFFFFF')
    s += P('M16 74 V28 Q16 12 32 12', 'none', 7, L) + P('M16 74 V28 Q16 12 32 12', 'none', 3, '#D8DEE9')
    s += P('M32 12 Q40 12 40 28 V40', 'none', 7, L) + P('M32 12 Q40 12 40 28 V40', 'none', 3, '#D8DEE9')
    s += P('M16 58 H34 M16 68 H34', sw=2, stroke='#FFFFFF')
    s += '<ellipse cx="70" cy="52" rx="17" ry="7" fill="none" stroke="#2A2A2A" stroke-width="12"/>'
    s += '<ellipse cx="70" cy="52" rx="17" ry="7" fill="none" stroke="#E5534B" stroke-width="8"/>'
    s += '<ellipse cx="70" cy="52" rx="17" ry="7" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-dasharray="8.6 8.6"/>'
    return s


@picto('clinic', 'ambulancia')
def clinic():
    s = P('M10 34 H90 V90 H10 Z', '#EAF3F9')
    s += P('M10 34 H90 V42 H10 Z', '#5BB8B3')
    s += _win(16, 54, 16, 16) + _win(68, 54, 16, 16)
    s += P('M38 90 V62 H62 V90 Z', GLASSB, 1.8) + P('M50 62 V90', sw=1.6)
    s += C(50, 28, 20, '#FFFFFF')
    s += P('M44 14 H56 V22 H64 V34 H56 V42 H44 V34 H36 V22 H44 Z', RED, 2)
    return s
