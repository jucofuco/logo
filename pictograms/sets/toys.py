"""Toys folder: one object, its typical view, flat colors."""
import math
import re
from kit import *


def _sc(body, s, tx, ty):
    """Scales a drawing about the origin and keeps the outline width constant."""
    body = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{round(float(m.group(1)) / s, 2)}"', body)
    return f'<g transform="translate({tx} {ty}) scale({s})">{body}</g>'


def _tube(d, w, color):
    return P(d, 'none', w + 2 * W, L) + P(d, 'none', w, color)


def _poly(pts, fill, sw=W):
    return P('M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z', fill, sw)


def _pent(cx, cy, r, rot):
    return [(cx + r * math.cos(math.radians(rot + 72 * k)), cy + r * math.sin(math.radians(rot + 72 * k))) for k in range(5)]


@picto('ball', 'lopta')
def ball():
    s = f'<defs><clipPath id="ballclip"><circle cx="50" cy="50" r="38"/></clipPath></defs>'
    s += C(50, 50, 38, '#FFFFFF')
    inner = _pent(50, 50, 12, -90)
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        x1, y1 = 50 + 12 * math.cos(a), 50 + 12 * math.sin(a)
        x2, y2 = 50 + 28 * math.cos(a), 50 + 28 * math.sin(a)
        s += P(f'M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}')
    patches = ''
    for k in range(5):
        a = -90 + 72 * k + 36
        cx, cy = 50 + 41 * math.cos(math.radians(a)), 50 + 41 * math.sin(math.radians(a))
        patches += _poly(_pent(cx, cy, 13, a + 180 + 0), L, 0)
    s += f'<g clip-path="url(#ballclip)">{patches}</g>'
    # lines from inner pentagon vertices to patches
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        x2, y2 = 50 + 28 * math.cos(a), 50 + 28 * math.sin(a)
        for da in (-36, 36):
            b = math.radians(-90 + 72 * k + da)
            s += P(f'M{x2:.1f} {y2:.1f} L{50 + 31 * math.cos(b):.1f} {50 + 31 * math.sin(b):.1f}')
    s += _poly(inner, L)
    s += C(50, 50, 38, 'none')
    s += P('M24 28 Q30 20 40 17', sw=3, stroke='#FFFFFF')
    return s


@picto('computer', 'počítač')
def computer():
    s = P('M16 14 H84 Q88 14 88 18 V62 Q88 66 84 66 H16 Q12 66 12 62 V18 Q12 14 16 14 Z', '#5A6577')
    s += P('M19 21 H81 V59 H19 Z', '#BFE3F7')
    s += C(34, 33, 5, '#FBD34D', 1.6) + P('M19 59 L38 42 L52 54 L62 46 L81 59 Z', '#6CC08B', 1.6)
    s += P('M10 66 H90 L95 80 Q95 84 90 84 H10 Q5 84 5 80 Z', '#D5DAE3')
    s += P('M40 71 H60', sw=2.4)
    return s


@picto('phone', 'mobilný telefón')
def phone():
    s = P('M38 6 H62 Q72 6 72 16 V84 Q72 94 62 94 H38 Q28 94 28 84 V16 Q28 6 38 6 Z', '#3B4252')
    s += P('M33 17 H67 V80 H33 Z', '#9BD3F2', 1.6)
    cols = [RED, '#FBD34D', GREEN, '#5B8DEF', '#F29AB8', '#F4A340']
    for n, c in enumerate(cols):
        x = 36 + (n % 3) * 11
        y = 21 + (n // 3) * 11
        s += P(f'M{x} {y} h8 v8 h-8 Z', c, 1.4)
    s += C(50, 68, 6, GREEN, 1.6)
    s += P('M45 11 H55', sw=2, stroke='#9AA3B5')
    return s


@picto('teddy', 'medvedík')
def teddy():
    B, Lt = '#C98B52', '#F0CFA0'
    s = C(30, 18, 9, B) + C(70, 18, 9, B) + C(30, 18, 5, Lt, 0) + C(70, 18, 5, Lt, 0)
    s += E(24, 66, 8, 13, B, rot=28) + E(76, 66, 8, 13, B, rot=-28)
    s += E(50, 70, 23, 23, B)
    s += E(36, 90, 12, 8, B) + E(64, 90, 12, 8, B) + E(36, 91, 6, 4, Lt, 0) + E(64, 91, 6, 4, Lt, 0)
    s += E(50, 72, 14, 15, Lt, 1.6)
    s += C(50, 36, 24, B)
    s += E(50, 44, 11, 9, Lt, 1.8) + E(50, 40, 4.5, 3.2, L, 0)
    s += P('M50 43 V47 M44 49 Q50 53 56 49', sw=1.8)
    s += eye_open(40, 33, r=4.4) + eye_open(60, 33, r=4.4)
    s += P('M50 57 L36 52 L36 62 Z', RED, 1.8) + P('M50 57 L64 52 L64 62 Z', RED, 1.8) + C(50, 57, 3.6, RED, 1.8)
    return s


@picto('doll', 'bábika')
def doll():
    HAIRC = '#F2C14E'
    s = C(22, 36, 9, HAIRC) + C(78, 36, 9, HAIRC)
    s += P('M40 54 L16 66', 'none', 8, L) + P('M40 54 L16 66', 'none', 4, SK) + P('M60 54 L84 66', 'none', 8, L) + P('M60 54 L84 66', 'none', 4, SK)
    s += P('M42 80 V92 M58 80 V92', 'none', 8, L) + P('M42 80 V92 M58 80 V92', 'none', 4, SK)
    s += E(42, 94, 7, 3.4, RED) + E(58, 94, 7, 3.4, RED)
    s += P('M38 48 H62 L82 86 Q50 92 18 86 Z', '#F29AB8')
    s += P('M36 54 H64', sw=3, stroke='#E5534B') + P('M30 74 Q50 80 70 74', sw=1.6)
    s += P('M27 36 Q27 10 50 10 Q73 10 73 36 Q73 44 68 46 L32 46 Q27 44 27 36 Z', HAIRC)
    s += C(50, 34, 17, SK)
    s += P('M33 33 Q32 17 50 16 Q68 17 67 33 Q58 30 50 22 Q42 30 33 33 Z', HAIRC)
    s += eye_open(43, 36, r=3.8) + eye_open(57, 36, r=3.8)
    s += E(37, 42, 3.4, 2.2, ANGRY, 0) + E(63, 42, 3.4, 2.2, ANGRY, 0)
    s += P('M45 43 Q50 48 55 43', sw=1.8)
    s += P('M20 28 L26 34 L16 38 Z', RED, 1.4) + P('M80 28 L74 34 L84 38 Z', RED, 1.4)
    return s


@picto('blocks', 'kocky')
def blocks():
    s = P('M14 64 H48 V96 H14 Z', RED)
    s += P('M52 64 H86 V96 H52 Z', '#5B8DEF')
    s += '<g transform="rotate(-8 50 44)">' + P('M33 28 H67 V62 H33 Z', '#F7D154') + '</g>'
    s += P('M31 90 L31 70 L41 90 Z', '#FFFFFF', 1.6)
    s += C(69, 80, 7, '#FFFFFF', 1.6)
    s += '<g transform="rotate(-8 50 44)">' + P('M44 58 L50 48 L56 58 Z', '#E5534B', 1.6) + P('M40 38 H60', sw=0) + '</g>'
    return s


@picto('hoop', 'obruč')
def hoop():
    s = '<circle cx="50" cy="50" r="34" fill="none" stroke="#2A2A2A" stroke-width="15"/>'
    s += '<circle cx="50" cy="50" r="34" fill="none" stroke="#E75480" stroke-width="11"/>'
    s += '<circle cx="50" cy="50" r="34" fill="none" stroke="#FBD34D" stroke-width="11" stroke-dasharray="13.3 26.7" stroke-dashoffset="-6"/>'
    s += P('M22 34 Q30 20 44 16', sw=2.6, stroke='#FFFFFF')
    return s


@picto('boardGame', 'spoločenská hra')
def board_game():
    s = P('M10 12 H84 V84 H10 Z', '#F2D9A0')
    s += P('M34 12 H60 V84 H34 Z', '#FFF6DD', 1.6) + P('M10 34 H84 V60 H10 Z', '#FFF6DD', 1.6)
    s += P('M34 34 H60 V60 H34 Z', '#FBD34D', 1.6) + P('M47 38 L49.5 44.5 L56 45 L51 49 L52.5 56 L47 52.5 L41.5 56 L43 49 L38 45 L44.5 44.5 Z', '#E5534B', 1)
    for (x, y, c) in [(14, 16, RED), (64, 16, '#5B8DEF'), (14, 64, GREEN), (64, 64, '#F4A340')]:
        s += P(f'M{x} {y} h16 v16 h-16 Z', c, 1.6)
        s += C(x + 8, y + 8, 4, '#FFFFFF', 1.6)
    for y in (22, 72):
        for x in (42, 52):
            pass
    s += '<g transform="rotate(12 76 76)">' + P('M64 64 H88 V88 H64 Z', '#FFFFFF')
    for (x, y) in [(70, 70), (82, 70), (76, 76), (70, 82), (82, 82)]:
        s += C(x, y, 2.4, L, 0)
    s += '</g>'
    return s


@picto('cards', 'karty')
def cards():
    heart = 'M50 62 Q32 50 34 40 Q36 31 44 33 Q48 34 50 39 Q52 34 56 33 Q64 31 66 40 Q68 50 50 62 Z'
    spade = 'M50 33 Q30 48 34 56 Q38 62 46 56 Q46 62 42 67 H58 Q54 62 54 56 Q62 62 66 56 Q70 48 50 33 Z'
    dia = 'M50 34 L65 50 L50 66 L35 50 Z'
    s = ''
    for rot, sym, col in [(-30, heart, RED), (0, spade, L), (30, dia, RED)]:
        s += (f'<g transform="rotate({rot} 50 96)">' + P('M31 30 H69 V86 H31 Z', '#FFFFFF')
              + f'<g transform="translate(50 36) scale(0.78) translate(-50 -48)">' + P(sym, col, 2) + '</g></g>')
    return s


@picto('lego', 'lego')
def lego():
    R, RL = '#E5534B', '#F07A72'
    s = P('M8 52 L22 32 H94 L80 52 Z', RL)
    s += P('M80 52 L94 32 V66 L80 86 Z', '#C73E37')
    s += P('M8 52 H80 V86 H8 Z', R)
    for (y, shift) in [(37, 10.5), (45, 4.9)]:
        left = 8 + shift
        for k in range(4):
            x = left + 9 + 18 * k
            s += P(f'M{x-6} {y-4} V{y} A6 3 0 0 0 {x+6} {y} V{y-4} Z', R, 1.6) + E(x, y - 4, 6, 3, RL, 1.6)
    s += P('M14 78 H74', sw=1.6, stroke='#C73E37')
    return s


@picto('toyCar', 'autíčko')
def toy_car():
    s = P('M6 66 Q6 56 16 54 L28 52 Q34 32 52 32 H64 Q74 32 80 52 L90 55 Q96 58 96 66 V74 H6 Z', RED)
    s += P('M33 52 Q37 40 49 40 H52 V52 Z', '#BFE3F7', 1.8) + P('M57 40 H63 Q68 40 73 52 H57 Z', '#BFE3F7', 1.8)
    s += P('M54 52 V70', sw=1.6) + P('M46 60 H50', sw=2.4)
    s += E(92, 62, 3, 4, '#FBD34D', 1.6) + E(10, 62, 2.4, 4, '#F4A340', 1.6)
    for x in (28, 76):
        s += C(x, 74, 12, '#4C566A') + C(x, 74, 5, '#D8DEE9', 1.6)
    return s


@picto('balloon', 'balón')
def balloon():
    s = P('M50 6 Q80 6 80 38 Q80 62 52 72 Q20 62 20 38 Q20 6 50 6 Z', RED)
    s += P('M52 72 L45 80 Q52 78 59 80 Z', RED, 1.8)
    s += P('M52 80 Q44 86 52 91 Q60 96 52 99', sw=1.8)
    s += E(34, 30, 4.5, 9, '#F6A39D', 0, rot=25)
    return s


@picto('puzzle', 'puzzle')
def puzzle():
    s = P('M56 22 H92 V78 H56 V57 A8 8 0 1 0 56 43 Z', '#F4A340')
    s += P('M8 22 H44 V43 A8 8 0 1 1 44 57 V78 H8 Z', '#5B8DEF')
    s += E(18, 34, 4, 2.4, '#8FB0F4', 0, rot=-20)
    s += E(80, 34, 4, 2.4, '#F8C27C', 0, rot=-20)
    return s


@picto('bicycle', 'bicykel')
def bicycle():
    s = ''
    for x in (22, 78):
        s += C(x, 66, 17, 'none', 4.5)
        s += P(f'M{x-17} 66 H{x+17} M{x} 49 V83 M{x-12} 54 L{x+12} 78 M{x+12} 54 L{x-12} 78', sw=0.9, stroke='#9AA3B5')
        s += C(x, 66, 3, '#D8DEE9', 1.6)
    s += _tube('M22 66 L44 66 L38 38 Z', 3.5, RED)
    s += _tube('M44 66 L66 36 L38 38', 3.5, RED)
    s += _tube('M66 36 L78 66', 3.5, RED)
    s += _tube('M66 36 L62 26 H72', 3.5, '#4C566A')
    s += P('M31 35 H46 Q48 35 48 37 Q48 39 46 39 H31 Q29 39 29 37 Q29 35 31 35 Z', '#4C566A', 1.8)
    s += C(44, 66, 4, '#FBD34D', 1.8) + P('M44 66 L40 77 H34', sw=2.4)
    return s


@picto('tetris', 'tetris')
def tetris():
    s = P('M8 8 H92 V92 H8 Z', '#2F3A52')
    cell = 16
    ox, oy = 10, 10

    def blk(col, row, color, light):
        x, y = ox + col * cell, oy + row * cell
        return P(f'M{x} {y} h{cell} v{cell} h-{cell} Z', color, 1.6) + P(f'M{x+3} {y+3} h{cell-6} v3', sw=1.4, stroke=light)
    for c in range(4):
        s += blk(c, 4, '#4FC3E8', '#BFEFFB')
    for (c, r) in [(4, 4), (4, 3), (4, 2), (3, 2)]:
        s += blk(c, r, '#F4A340', '#FBD9A6')
    for (c, r) in [(0, 2), (1, 2), (0, 3), (1, 3)]:
        s += blk(c, r, '#F7D154', '#FFF1B0')
    for (c, r) in [(1, 0), (2, 0), (3, 0), (2, 1)]:
        s += blk(c, r, '#B36AD9', '#E3C2F3')
    return s
