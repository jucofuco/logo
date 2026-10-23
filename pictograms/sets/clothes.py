"""Clothes folder: one garment, flat front view."""
import re
from kit import *


def _sc(body, s, tx, ty):
    """Scales a drawing about the origin and keeps the outline width constant."""
    body = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{round(float(m.group(1)) / s, 2)}"', body)
    return f'<g transform="translate({tx} {ty}) scale({s})">{body}</g>'


BLUE = '#4A78C2'


@picto('trousers', 'nohavice')
def trousers():
    s = P('M27 8 H73 L79 92 H55 L50 42 L45 92 H21 Z', BLUE)
    s += P('M27 8 H73 V20 H27 Z', '#3A62A5')
    s += P('M50 20 V42', sw=1.8) + C(50, 24, 1.6, '#FBD34D', 1)
    s += P('M30 28 Q36 30 38 40 M70 28 Q64 30 62 40', sw=1.8)
    s += P('M22 82 H45 M55 82 H78', sw=1.8, stroke='#9BB8E6')
    return s


@picto('shorts', 'šortky')
def shorts():
    s = P('M16 20 H84 L94 74 H56 L50 50 L44 74 H6 Z', '#F4A340')
    s += P('M16 20 H84 L85 32 H15 Z', '#E08A1F')
    s += P('M46 32 Q44 44 40 48 M54 32 Q56 44 60 48', sw=2)
    s += P('M50 25 L42 20 M50 25 L58 20', sw=2) + C(50, 25, 2, L, 0)
    s += P('M8 64 H44 M56 64 H92', sw=1.8, stroke='#FFFFFF')
    return s


@picto('tshirt', 'tričko')
def tshirt():
    s = P('M34 12 Q50 24 66 12 L92 26 L82 48 L71 42 V88 H29 V42 L18 48 L8 26 Z', RED)
    s += P('M34 12 Q50 24 66 12', sw=2) + P('M37 13 Q50 27 63 13', sw=2.2, stroke='#B5413D')
    s += P('M50 48 L54 58 L65 58 L56 65 L59 76 L50 70 L41 76 L44 65 L35 58 L46 58 Z', '#FBD34D', 1.8)
    s += P('M12 38 L22 43 M88 38 L78 43', sw=1.6, stroke='#FFFFFF')
    return s


@picto('shirt', 'košeľa')
def shirt():
    s = P('M36 12 L16 20 L5 70 L21 75 L30 44 V92 H70 V44 L79 75 L95 70 L84 20 L64 12 Q50 20 36 12 Z', '#8DBBEA')
    s += P('M50 30 V92', sw=1.8)
    for y in (46, 60, 74, 88):
        s += C(50, y, 1.8, '#FFFFFF', 1.2)
    s += P('M35 12 L50 22 L48 36 L30 22 Z', '#FFFFFF') + P('M65 12 L50 22 L52 36 L70 22 Z', '#FFFFFF')
    s += P('M8 62 L23 67 M92 62 L77 67', sw=1.8)
    s += P('M56 50 H66 V60 H56 Z', '#6FA3DD', 1.6)
    return s


def _sock(ox, oy, col, stripe):
    s = P(f'M{ox+16} {oy+8} H{ox+42} V{oy+48} Q{ox+42} {oy+54} {ox+50} {oy+58} L{ox+64} {oy+66} Q{ox+74} {oy+72} {ox+70} {oy+82} Q{ox+66} {oy+88} {ox+58} {oy+86} H{ox+32} Q{ox+16} {oy+86} {ox+16} {oy+70} Z', col)
    s += P(f'M{ox+16} {oy+8} H{ox+42} V{oy+22} H{ox+16} Z', stripe)
    s += P(f'M{ox+18} {oy+34} H{ox+42}', sw=1.6, stroke=stripe)
    s += P(f'M{ox+58} {oy+86} Q{ox+64} {oy+78} {ox+64} {oy+70}', sw=1.6)
    return s


@picto('socks', 'ponožky')
def socks():
    return _sock(18, 4, '#F4A340', '#FFFFFF') + _sock(-6, 8, '#8DBBEA', '#E5534B')


def _shoe(sw):
    s = P('M8 38 Q8 30 16 30 H32 Q36 42 50 44 L64 48 Q88 52 92 66 V74 H8 Z', '#E5534B', sw)
    s += P('M8 72 H92 V80 Q92 84 88 84 H12 Q8 84 8 80 Z', '#FFFFFF', sw)
    s += P('M62 48 Q76 52 84 60 L92 66 H66 Z', '#F07A72', sw)
    s += P('M36 34 L44 44 M44 32 L52 44 M52 36 L58 46', sw=sw, stroke='#FFFFFF')
    s += P('M8 62 H92', sw=sw * 0.8, stroke='#B5413D')
    return s


@picto('shoes', 'topánky')
def shoes():
    k = 0.66
    return _sc(_shoe(W / k), k, 30, 6) + _sc(_shoe(W / k), k, 6, 38)


@picto('cap', 'šiltovka')
def cap():
    s = P('M12 64 Q12 22 50 22 Q84 22 88 64 Z', RED)
    s += P('M50 22 Q36 40 36 64 M50 22 Q62 40 66 64', sw=1.8)
    s += C(50, 22, 3.6, '#B5413D', 1.8)
    s += P('M60 62 Q80 58 98 70 Q100 78 92 78 Q76 72 58 72 Z', '#B5413D')
    s += P('M12 64 H88', sw=1.8)
    s += P('M20 52 Q24 38 36 32', sw=2.4, stroke='#F6A39D')
    return s


@picto('coat', 'kabát')
def coat():
    s = P('M36 10 L16 20 L6 76 L22 80 L28 44 L26 94 H74 L72 44 L78 80 L94 76 L84 20 L64 10 Q50 18 36 10 Z', '#D9822B')
    s += P('M50 22 V94', sw=1.8)
    s += P('M36 10 L50 38 L38 40 L30 22 Z', '#B86A1E') + P('M64 10 L50 38 L62 40 L70 22 Z', '#B86A1E')
    for y in (54, 68, 82):
        s += C(46, y, 2.6, '#FBD34D', 1.6) + C(54, y, 2.6, '#FBD34D', 1.6)
    s += P('M30 70 H40 M60 70 H70', sw=1.8)
    s += P('M9 66 L24 71 M91 66 L76 71', sw=1.8)
    return s


@picto('underpants', 'nohavičky')
def underpants():
    s = P('M14 24 H86 L83 44 Q70 56 62 78 Q50 84 38 78 Q30 56 17 44 Z', '#8DBBEA')
    s += P('M14 24 H86 V34 H15 Z', '#5B8DEF')
    s += P('M17 44 Q32 50 38 78 M83 44 Q68 50 62 78', sw=1.6, stroke='#5B8DEF')
    s += P('M50 64 Q42 58 44 53 Q47 50 50 54 Q53 50 56 53 Q58 58 50 64 Z', '#FFFFFF', 1.6)
    return s


@picto('glasses', 'okuliare')
def glasses():
    s = P('M12 46 L4 38 M88 46 L96 38', sw=3.5)
    s += C(28, 54, 18, GLASS, 3.5) + C(72, 54, 18, GLASS, 3.5)
    s += P('M46 50 Q50 44 54 50', sw=3.5)
    s += P('M18 48 Q22 42 28 41 M62 48 Q66 42 72 41', sw=2, stroke='#9BD3F2')
    return s


@picto('sunglasses', 'slnečné okuliare')
def sunglasses():
    s = P('M8 40 L2 32 M92 40 L98 32', sw=3.5)
    for flip in (False, True):
        d = 'M6 38 H46 V54 Q46 72 28 72 Q8 72 6 54 Z'
        if flip:
            d = 'M94 38 H54 V54 Q54 72 72 72 Q92 72 94 54 Z'
        s += P(d, '#2F3A52', 3.5)
    s += P('M46 44 Q50 40 54 44', sw=3.5)
    s += P('M14 48 L24 44 M14 56 L30 50 M62 48 L72 44 M62 56 L78 50', sw=2.2, stroke='#9BD3F2')
    return s


@picto('scarf', 'šatka')
def scarf():
    s = C(50, 56, 27, SK)
    s += eye_open(41, 58, r=3.8) + eye_open(59, 58, r=3.8)
    s += E(34, 66, 3.4, 2.2, ANGRY, 0) + E(66, 66, 3.4, 2.2, ANGRY, 0)
    s += P('M44 68 Q50 74 56 68', sw=1.8)
    s += P('M18 66 Q10 16 50 12 Q90 16 82 66 Q82 74 76 78 Q74 50 50 40 Q26 50 24 78 Q18 74 18 66 Z', RED)
    for (x, y) in [(30, 24), (50, 18), (70, 24), (22, 42), (78, 42), (40, 30), (60, 30)]:
        s += C(x, y, 2.6, '#FFFFFF', 0)
    s += P('M26 80 Q50 92 74 80 L84 96 Q50 90 16 96 Z', RED)
    s += C(50, 84, 5, '#B5413D', 1.8)
    return s
