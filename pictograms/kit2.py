"""Style 2 people: simpler, closer to European AAC symbols (ARASAAC-like), nothing anime.

Natural proportions (smaller head), dot eyes without highlights, a nose, ears, a small mouth,
no blush, plain hair shapes, arms as their own outlined shapes so they never melt into the body.
Same outline color and width as kit.py, and the same hands.
"""
from kit import *

SK2 = '#F6D5C1'
HAIR_BROWN = '#7A5230'
HAIR_BLOND = '#D9A953'
HAIR_DARK = '#3E2C22'
HAIR_GREY = '#BDBDBD'

# who looks how: hair style, hair color, shirt color, extras
PEOPLE = {
    'child':   dict(hair='short', color=HAIR_BROWN, shirt=SHIRT),
    'mom':     dict(hair='long', color=HAIR_BROWN, shirt='#E8705F'),
    'dad':     dict(hair='short', color=HAIR_DARK, shirt='#5FA36A'),
    'brother': dict(hair='short', color=HAIR_BLOND, shirt='#F2C14E'),
    'sister':  dict(hair='ponytail', color=HAIR_BLOND, shirt='#F29BB5'),
    'grandma': dict(hair='bun', color=HAIR_GREY, shirt='#A98BD0', glasses=True),
    'grandpa': dict(hair='bald', color=HAIR_GREY, shirt='#B5895A', glasses=True, moustache=True),
    'teacher': dict(hair='short', color=HAIR_BROWN, shirt='#FFFFFF', glasses=True),
}


def hair_back(x, y, r, style, color):
    """Hair that sits behind the head (long hair, bun, ponytail)."""
    if style == 'long':
        return P(f'M{x-r-2} {y} Q{x-r-3} {y-r-3} {x} {y-r-3} Q{x+r+3} {y-r-3} {x+r+2} {y} '
                 f'L{x+r+3} {y+r+6} Q{x+r} {y+r+9} {x+r-4} {y+r+7} L{x-r+4} {y+r+7} Q{x-r} {y+r+9} {x-r-3} {y+r+6} Z', color)
    if style == 'bun':
        return C(x, y - r - 2, r * 0.42, color)
    if style == 'ponytail':
        return P(f'M{x+r-2} {y-r*0.5} Q{x+r+9} {y-r*0.6} {x+r+8} {y+r*0.5} Q{x+r+6} {y+r*0.9} {x+r+3} {y+r*0.3} Q{x+r+3} {y-r*0.1} {x+r-3} {y-r*0.2} Z', color)
    return ''


def hair_front(x, y, r, style, color):
    """Hair on top of the head."""
    if style == 'bald':
        return (P(f'M{x-r-0.6} {y+2} Q{x-r-1} {y-r*0.55} {x-r*0.55} {y-r*0.8} Q{x-r*0.7} {y-r*0.3} {x-r+2.5} {y+1} Z', color)
                + P(f'M{x+r+0.6} {y+2} Q{x+r+1} {y-r*0.55} {x+r*0.55} {y-r*0.8} Q{x+r*0.7} {y-r*0.3} {x+r-2.5} {y+1} Z', color))
    # a cap of hair with a side parting fringe
    return P(f'M{x-r-0.8} {y+1} Q{x-r-1.4} {y-r-1.6} {x} {y-r-1.8} Q{x+r+1.4} {y-r-1.6} {x+r+0.8} {y+1} '
             f'Q{x+r-1} {y-r*0.45} {x+r*0.35} {y-r*0.62} Q{x-r*0.25} {y-r*0.4} {x-r*0.55} {y-r*0.55} Q{x-r+1} {y-r*0.3} {x-r-0.8} {y+1} Z', color)


def face2(x, y, r, mood='smile'):
    """Eyes, brows, nose, mouth for a head of radius r centered at x, y."""
    k = r / 15
    ex, ey = 5.4 * k, 0.6 * k
    s = ''
    brow = {'smile': (-1, 0), 'neutral': (0, 0), 'sad': (1.6, -1.2), 'angry': (-1.4, 1.6), 'surprised': (-2.6, 0)}.get(mood, (0, 0))
    for side in (-1, 1):
        bx = x + side * ex
        inner, outer = brow[1] * side, brow[0]
        s += P(f'M{bx - 3 * k} {y - 5 * k + (outer if side < 0 else inner)} Q{bx} {y - 6.6 * k + brow[0]} {bx + 3 * k} {y - 5 * k + (inner if side < 0 else outer)}', sw=1.6 * k)
        if mood == 'tired':
            s += P(f'M{bx - 2 * k} {y + ey} Q{bx} {y + ey + 1.6 * k} {bx + 2 * k} {y + ey}', sw=1.5 * k)
        else:
            s += C(bx, y + ey, (1.9 if mood == 'surprised' else 1.6) * k, L, 0)
    s += P(f'M{x - 0.4 * k} {y + 2.6 * k} Q{x + 1.4 * k} {y + 4.6 * k} {x - 0.6 * k} {y + 5.2 * k}', sw=1.4 * k)   # nose
    my = y + 8.6 * k
    if mood == 'smile':
        s += P(f'M{x - 4.2 * k} {my} Q{x} {my + 3.4 * k} {x + 4.2 * k} {my}', sw=1.6 * k)
    elif mood in ('sad', 'angry'):
        s += P(f'M{x - 3.8 * k} {my + 2 * k} Q{x} {my - 1.2 * k} {x + 3.8 * k} {my + 2 * k}', sw=1.6 * k)
    elif mood in ('open', 'surprised'):
        s += E(x, my + 0.6 * k, 2.4 * k, 2.8 * k, '#A8443F', 1.4 * k)
    else:
        s += P(f'M{x - 3 * k} {my + 0.6 * k} H{x + 3 * k}', sw=1.6 * k)
    return s


def head2(x, y, r=15, who='child', mood='smile'):
    """A whole head: hair behind, ears, face, hair on top, glasses or moustache."""
    p = PEOPLE[who]
    k = r / 15
    s = hair_back(x, y, r, p['hair'], p['color'])
    s += P(f'M{x - 4 * k} {y + r - 2 * k} V{y + r + 5 * k} H{x + 4 * k} V{y + r - 2 * k}', SK2)               # neck
    s += C(x - r, y + 1.5 * k, 3.2 * k, SK2) + C(x + r, y + 1.5 * k, 3.2 * k, SK2)                          # ears
    s += E(x, y, r, r * 1.06, SK2)
    s += face2(x, y, r, mood)
    s += hair_front(x, y, r, p['hair'], p['color'])
    if p.get('glasses'):
        for side in (-1, 1):
            s += C(x + side * 5.4 * k, y + 0.6 * k, 3.6 * k, 'none', 1.4 * k)
        s += P(f'M{x - 1.8 * k} {y + 0.2 * k} Q{x} {y - 0.8 * k} {x + 1.8 * k} {y + 0.2 * k}', sw=1.4 * k)
    if p.get('moustache'):
        s += P(f'M{x - 4.5 * k} {y + 7.6 * k} Q{x - 2 * k} {y + 4.6 * k} {x} {y + 6.4 * k} Q{x + 2 * k} {y + 4.6 * k} {x + 4.5 * k} {y + 7.6 * k} Q{x} {y + 7 * k} {x - 4.5 * k} {y + 7.6 * k} Z', HAIR_GREY, 1.2 * k)
    return s


def body2(x, top, who='child', width=25):
    """Upper body cropped by the bottom edge: shirt with a collar, arms hanging beside it as their own shapes."""
    p = PEOPLE[who]
    w = width
    s = ''
    for side in (-1, 1):
        d = f'M{x + side * (w - 3)} {top + 7} Q{x + side * (w + 7)} {top + 16} {x + side * (w + 8)} 104'
        s += P(d, 'none', 13 + 2 * W, L) + P(d, 'none', 13, p['shirt'])
    s += P(f'M{x - w} 104 V{top + 14} Q{x - w} {top} {x - w * 0.4} {top} H{x + w * 0.4} Q{x + w} {top} {x + w} {top + 14} V104 Z', p['shirt'])
    s += P(f'M{x - 5} {top} Q{x} {top + 6} {x + 5} {top}', sw=1.6)                                         # collar
    if who == 'teacher':
        s += P(f'M{x} {top + 2} L{x - 2.4} {top + 8} L{x} {top + 26} L{x + 2.4} {top + 8} Z', '#E5534B', 1.4)
    return s


def portrait(who, mood='smile'):
    """Head and shoulders of one person, the standard people pictogram."""
    return body2(50, 64, who) + head2(50, 36, 19, who, mood)


def big_face(mood, who='child'):
    """Feelings: the head fills the frame."""
    return head2(50, 50, 30, who, mood)
