"""Style 2 people, modelled on the European AAC standard (ARASAAC-like), nothing anime.

Whole figures seen from the front with natural proportions (small head), thin dark outlines,
flat saturated colors, very light skin, a minimal face (dot eyes, a small mouth, a small nose for
adults), long sleeves with the arms hanging beside the body, trousers or a dress, shoes.
Feelings are a plain white face circle with dot eyes and a simple mouth.
"""
from kit import *

W2 = 1.3                 # thin outline (style 1 uses 2)
SK2 = '#FCEBDF'          # very light skin
HAIR_BROWN = '#9A5B2E'
HAIR_BLOND = '#E8C04A'
HAIR_DARK = '#4A3324'
HAIR_GREY = '#D8D8D8'
SHOE = '#3A3A3A'


def P2(d, fill='none', sw=W2, stroke=L):
    return P(d, fill, sw, stroke)


def C2(cx, cy, r, fill, sw=W2):
    return C(cx, cy, r, fill, sw)


# who looks how. h = body height in canvas units (adults taller), top = shirt color, bottom = trousers,
# dress = dress color instead of top + trousers, skirt = skirt color under the top.
PEOPLE = {
    'child':   dict(hair='short', color=HAIR_BROWN, top='#D9643A', bottom='#4A78B5', kid=True),
    'boy':     dict(hair='short', color=HAIR_BROWN, top='#D9643A', bottom='#4A78B5', kid=True),
    'brother': dict(hair='short', color=HAIR_DARK, top='#5E9A4A', bottom='#3D5A8C', kid=True),
    'sister':  dict(hair='pigtails', color=HAIR_BLOND, top='#D2506B', bottom='#E0A93A', kid=True),
    'girl':    dict(hair='pigtails', color=HAIR_BLOND, top='#D2506B', bottom='#E0A93A', kid=True),
    'mom':     dict(hair='curly', color=HAIR_BROWN, dress='#5C8F4E'),
    'dad':     dict(hair='short', color=HAIR_DARK, top='#B5413A', bottom='#3F5F7A'),
    'grandma': dict(hair='curly_short', color=HAIR_GREY, top='#C49AC0', skirt='#7A7A7A', glasses=True),
    'grandpa': dict(hair='bald', color=HAIR_GREY, top='#6F8FC0', bottom='#A88A4A', glasses=True, moustache=True),
    'teacher': dict(hair='short', color=HAIR_BROWN, top='#FFFFFF', bottom='#4A4A4A', glasses=True, tie=True),
}

def hair2(x, y, r, style, color, part):
    """part 'back' is drawn before the head, 'front' after the face."""
    if part == 'back':
        if style == 'curly':
            bumps = ''.join(f'{x + r * dx} {y + r * dy} ' for dx, dy in ())
            return P2(f'M{x - r * 1.05} {y + r * 1.5} Q{x - r * 1.7} {y + r * 0.9} {x - r * 1.35} {y + r * 0.1} '
                      f'Q{x - r * 1.75} {y - r * 0.8} {x - r * 0.8} {y - r * 1.2} Q{x - r * 0.3} {y - r * 1.75} {x + r * 0.35} {y - r * 1.25} '
                      f'Q{x + r * 1.2} {y - r * 1.5} {x + r * 1.35} {y - r * 0.5} Q{x + r * 1.8} {y + r * 0.2} {x + r * 1.35} {y + r * 0.8} '
                      f'Q{x + r * 1.6} {y + r * 1.4} {x + r * 1.05} {y + r * 1.5} Z', color)
        if style == 'pigtails':
            return (P2(f'M{x - r * 0.9} {y - r * 0.5} Q{x - r * 2.2} {y - r * 0.9} {x - r * 2} {y + r * 0.7} Q{x - r * 1.4} {y + r * 0.1} {x - r * 0.8} {y + r * 0.2} Z', color)
                    + P2(f'M{x + r * 0.9} {y - r * 0.5} Q{x + r * 2.2} {y - r * 0.9} {x + r * 2} {y + r * 0.7} Q{x + r * 1.4} {y + r * 0.1} {x + r * 0.8} {y + r * 0.2} Z', color))
        return ''
    if style == 'bald':
        return (P2(f'M{x - r * 1.0} {y + r * 0.2} Q{x - r * 1.05} {y - r * 0.5} {x - r * 0.65} {y - r * 0.75} Q{x - r * 0.75} {y - r * 0.2} {x - r * 0.8} {y + r * 0.25} Z', color, W2)
                + P2(f'M{x + r * 1.0} {y + r * 0.2} Q{x + r * 1.05} {y - r * 0.5} {x + r * 0.65} {y - r * 0.75} Q{x + r * 0.75} {y - r * 0.2} {x + r * 0.8} {y + r * 0.25} Z', color, W2))
    if style == 'curly_short':
        return P2(f'M{x - r * 1.05} {y - r * 0.05} Q{x - r * 1.35} {y - r * 0.9} {x - r * 0.6} {y - r * 1.15} Q{x - r * 0.2} {y - r * 1.5} {x + r * 0.3} {y - r * 1.2} '
                  f'Q{x + r * 1.3} {y - r * 1.25} {x + r * 1.05} {y - r * 0.05} Q{x + r * 0.7} {y - r * 0.55} {x} {y - r * 0.6} Q{x - r * 0.7} {y - r * 0.55} {x - r * 1.05} {y - r * 0.05} Z', color, W2)
    if style == 'curly':
        return P2(f'M{x - r * 1.0} {y - r * 0.1} Q{x - r * 0.9} {y - r * 1.05} {x} {y - r * 1.08} Q{x + r * 0.9} {y - r * 1.05} {x + r * 1.0} {y - r * 0.1} '
                  f'Q{x + r * 0.5} {y - r * 0.7} {x - r * 0.1} {y - r * 0.55} Q{x - r * 0.6} {y - r * 0.5} {x - r * 1.0} {y - r * 0.1} Z', color, 0)
    # short hair: a cap with a fringe
    return P2(f'M{x - r * 1.04} {y - r * 0.05} Q{x - r * 1.12} {y - r * 1.1} {x} {y - r * 1.12} Q{x + r * 1.12} {y - r * 1.1} {x + r * 1.04} {y - r * 0.05} '
              f'Q{x + r * 0.8} {y - r * 0.55} {x + r * 0.25} {y - r * 0.5} Q{x - r * 0.3} {y - r * 0.62} {x - r * 0.6} {y - r * 0.4} Q{x - r * 0.9} {y - r * 0.3} {x - r * 1.04} {y - r * 0.05} Z', color)


def face_small2(x, y, r, mood='smile', adult=False):
    k = r / 8
    s = E(x - 4.3 * k, y + 2.6 * k, 1.5 * k, 1 * k, '#F4B9A6', 0) + E(x + 4.3 * k, y + 2.6 * k, 1.5 * k, 1 * k, '#F4B9A6', 0)
    s += C2(x - 3 * k, y + 0.2 * k, 0.9 * k, L, 0) + C2(x + 3 * k, y + 0.2 * k, 0.9 * k, L, 0)
    if adult:
        s += P2(f'M{x} {y + 1.4 * k} Q{x + 0.9 * k} {y + 2.6 * k} {x - 0.3 * k} {y + 2.9 * k}', sw=1.2 * k)
    my = y + 4.3 * k
    if mood == 'smile':
        s += P2(f'M{x - 2.2 * k} {my} Q{x} {my + 1.8 * k} {x + 2.2 * k} {my}', sw=1.3 * k)
    elif mood == 'sad':
        s += P2(f'M{x - 2.2 * k} {my + 1.2 * k} Q{x} {my - 0.6 * k} {x + 2.2 * k} {my + 1.2 * k}', sw=1.3 * k)
    elif mood == 'open':
        s += E(x, my + 0.4 * k, 1.3 * k, 1.6 * k, '#B03A3A', 1.0 * k)
    else:
        s += P2(f'M{x - 1.6 * k} {my + 0.5 * k} H{x + 1.6 * k}', sw=1.3 * k)
    return s


def head_full(x, y, r, who, mood='smile'):
    p = PEOPLE[who]
    s = hair2(x, y, r, p['hair'], p['color'], 'back')
    s += E(x, y, r, r * 1.08, SK2, W2)
    s += face_small2(x, y, r, mood, adult=not p.get('kid'))
    s += hair2(x, y, r, p['hair'], p['color'], 'front')
    if p.get('glasses'):
        k = r / 8
        s += C2(x - 3 * k, y + 0.2 * k, 2.1 * k, 'none', 1.1 * k) + C2(x + 3 * k, y + 0.2 * k, 2.1 * k, 'none', 1.1 * k)
        s += P2(f'M{x - 0.9 * k} {y} H{x + 0.9 * k}', sw=1.1 * k)
    if p.get('moustache'):
        k = r / 8
        s += P2(f'M{x - 2.6 * k} {y + 3.6 * k} Q{x} {y + 2 * k} {x + 2.6 * k} {y + 3.6 * k} Q{x} {y + 3.2 * k} {x - 2.6 * k} {y + 3.6 * k} Z', HAIR_GREY, 1 * k)
    return s


def figure(who, x=50, mood='smile', foot=96):
    """A whole person standing, seen from the front, feet at `foot`. Children are smaller than adults."""
    p = PEOPLE[who]
    kid = p.get('kid')
    h = 70 if kid else 88                     # height from the top of the head to the feet
    top = foot - h
    r = h * (0.12 if kid else 0.095)          # head radius: children have bigger heads
    hy = top + r * 1.1
    sh = hy + r * 1.05 + 2                    # shoulder line
    hip = sh + h * 0.36
    bw = h * (0.16 if kid else 0.15)          # half width of the body
    s = ''
    # legs and shoes
    if p.get('dress'):
        s += P2(f'M{x - bw * 0.5} {hip + 6} V{foot - 3} M{x + bw * 0.5} {hip + 6} V{foot - 3}', 'none', 5 + 2 * W2) + P2(f'M{x - bw * 0.5} {hip + 6} V{foot - 3} M{x + bw * 0.5} {hip + 6} V{foot - 3}', 'none', 5, SK2)
    else:
        legs = f'M{x - bw} {hip} H{x + bw} L{x + bw * 0.92} {foot - 3} H{x + 1.4} L{x + 0.6} {hip + 7} H{x - 0.6} L{x - 1.4} {foot - 3} H{x - bw * 0.92} Z'
        s += P2(legs, p.get('bottom', p.get('skirt', '#555555')))
    s += E(x - bw * 0.55, foot - 1.5, bw * 0.55, 2.6, SHOE, W2) + E(x + bw * 0.55, foot - 1.5, bw * 0.55, 2.6, SHOE, W2)
    # skirt or dress over the legs
    if p.get('skirt'):
        s += P2(f'M{x - bw} {hip - 2} L{x - bw * 1.35} {foot - 10} H{x + bw * 1.35} L{x + bw} {hip - 2} Z', p['skirt'])
    if p.get('dress'):
        s += P2(f'M{x - bw * 0.95} {sh} Q{x} {sh - 2} {x + bw * 0.95} {sh} L{x + bw * 1.5} {hip + 10} H{x - bw * 1.5} Z', p['dress'])
    # arms hanging beside the body, sleeve to the wrist, small hands
    color = p.get('dress') or p.get('top')
    aw = bw * 0.42
    for side in (-1, 1):
        d = f'M{x + side * bw * 0.92} {sh + 2.5} Q{x + side * bw * 1.3} {sh + 9} {x + side * bw * 1.3} {hip}'
        s += P2(d, 'none', aw + 2 * W2) + P2(d, 'none', aw, color)
        s += C2(x + side * bw * 1.3, hip + 2.2, aw * 0.62, SK2)
    # top
    if not p.get('dress'):
        s += P2(f'M{x - bw} {hip + 1} V{sh + 4} Q{x - bw} {sh} {x - bw * 0.55} {sh} H{x + bw * 0.55} Q{x + bw} {sh} {x + bw} {sh + 4} V{hip + 1} Z', p['top'])
        s += P2(f'M{x - 2.6} {sh} Q{x} {sh + 2.6} {x + 2.6} {sh}', sw=1.1)
    if p.get('tie'):
        s += P2(f'M{x} {sh + 1} L{x - 1.8} {sh + 4} L{x} {sh + 14} L{x + 1.8} {sh + 4} Z', '#D9254A', W2)
    # neck and head
    s += P2(f'M{x - 2.2} {hy + r * 0.9} V{sh + 0.5} H{x + 2.2} V{hy + r * 0.9}', SK2)
    s += head_full(x, hy, r, who, mood)
    return s


def emotion_face(mood):
    """Feelings: a plain face with a thin outline, dot eyes, brows for some moods, a simple mouth."""
    s = P2('M45 88 V96 H55 V88', SK2) + C(50, 50, 38, SK2, 2)
    eyes = {'surprised': 5.6, 'scared': 5.6}.get(mood, 4.8)
    if mood == 'tired':
        s += P2('M30 46 Q36 50 42 46 M58 46 Q64 50 70 46', sw=2.6)
    else:
        s += C(36, 46, eyes, L, 0) + C(64, 46, eyes, L, 0)
    brows = {'sad': 'M26 38 Q33 32 41 34 M59 34 Q67 32 74 38', 'angry': 'M27 33 L43 40 M73 33 L57 40',
             'scared': 'M28 34 Q35 28 42 31 M58 31 Q65 28 72 34', 'surprised': 'M28 33 Q35 26 42 30 M58 30 Q65 26 72 33'}
    if mood in brows:
        s += P2(brows[mood], sw=2.6)
    mouths = {'smile': 'M34 64 Q50 78 66 64', 'sad': 'M36 72 Q50 60 64 72', 'angry': 'M36 71 Q50 63 64 71',
              'neutral': 'M38 68 H62', 'tired': 'M42 68 H58'}
    if mood in ('surprised', 'scared'):
        s += E(50, 68, 7, 9, L, 0)
    else:
        s += P2(mouths.get(mood, mouths['neutral']), sw=3)
    return s
