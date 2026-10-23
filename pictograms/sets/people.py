"""People folder: family members, teacher, and the pronouns (ja is in core).

Also holds the shared people helpers used by core, verbs and feelings:
`person()` draws one family member as a cropped bust in kit coordinates (head at 50,36, r 19),
`place()` moves and scales a drawing while keeping the outline width W,
`point_hand()` is a hand with the index finger out, `arrow_to()` an arrow with a head at its end.

Family (decided once, reuse it):
  me       the child (kit bust): brown short hair, blue shirt
  brother  older boy: dark spiky hair, yellow shirt
  sister   girl: brown pigtails with pink ties, pink shirt
  mom      long auburn hair over the shoulders, red top
  dad      short dark hair and a beard, green shirt
  grandma  grey hair with a bun, glasses, purple top
  grandpa  bald with grey sides, grey moustache, glasses, brown cardigan
  teacher  man with short hair, glasses, white shirt and red tie, in front of a blackboard
Pronoun marks: an orange arrow points at who is meant (on, ona, oni); the child points at
himself (ja, my); a hand from the viewer points at the group (vy); an arrow coming in to the
child means "me / us as the object" (mňa, nás).
"""
import math
import re

from kit import *

ARROW = '#F28C28'
HILITE = '#FFE9A8'
GREY = '#D3D7DC'

KINDS = {
    #          hair style, hair color, shirt
    'me':      ('boy', HAIR, SHIRT),
    'brother': ('spiky', '#4A2E1C', '#F6C453'),
    'sister':  ('pigtails', HAIR, '#F5A3C7'),
    'mom':     ('long', '#9A4E2A', '#E5534B'),
    'dad':     ('short', '#3E2A1E', '#5FAF7A'),
    'grandma': ('bun', GREY, '#A98BD6'),
    'grandpa': ('bald', GREY, '#B98D5F'),
    'teacher': ('short', '#5A3A24', '#FFFFFF'),
    'he':      ('boy', '#4A2E1C', '#5FAF7A'),
    'she':     ('pigtails', '#9A4E2A', '#F6C453'),
}


def place(body, x, y, k=1.0):
    """Draws `body` (kit coordinates, head center 50,36) with its head center at x,y, scaled by k.
    Stroke widths are divided by k so every outline stays W wide."""
    if k != 1:
        body = re.sub(r'stroke-width="([\d.]+)"', lambda m: f'stroke-width="{round(float(m.group(1)) / k, 2)}"', body)
    return f'<g transform="translate({x} {y}) scale({k}) translate(-50 -36)">{body}</g>'


def torso_c(shirt, top=59):
    return torso(0, top).replace(SHIRT, shirt)


def arm_c(d, shirt, width=11):
    return P(d, 'none', width + 2 * W, L) + P(d, 'none', width, shirt)


def body(kind, shirt=None):
    style, hc, sh = KINDS[kind]
    s = torso_c(shirt or sh)
    if style == 'long':
        s += P('M31 32 Q29 13 50 13 Q71 13 69 32 L72 62 Q66 67 60 61 L58 44 H42 L40 61 Q34 67 28 62 Z', hc)
    if kind == 'teacher':
        s += P('M42 60 L50 68 L58 60', '#FFFFFF') + P('M50 66 L46.5 70 L50 90 L53.5 70 Z', RED, 1.6)
    if kind == 'grandpa':
        s += P('M42 60 L50 72 L58 60', '#FFFFFF') + P('M50 72 V104', sw=1.6) + C(54, 80, 1.3, L, 0) + C(54, 90, 1.3, L, 0)
    return s


def head(kind, mood='smile', look=0):
    style, hc, _ = KINDS[kind]
    s = ''
    if style == 'pigtails':
        s += E(28, 41, 6.5, 10, hc, rot=25) + E(72, 41, 6.5, 10, hc, rot=-25)
    if style == 'bun':
        s += C(50, 15, 8, hc)
    s += P('M44.5 51 V60.5 Q50 64 55.5 60.5 V51', SK) + C(50, 36, 19, SK)
    if style == 'boy':
        s += P('M31.5 35 Q31 17 50 17 Q69 17 68.5 35 Q66 24.5 57 23.5 Q51 28.5 45 24.2 Q34 24.6 31.5 35 Z', hc)
    elif style == 'spiky':
        s += P('M31.5 35 Q30 22 36 19 L35 13 L42 17 L45 10 L50 16 L56 10 L58 17 L65 13 L64 20 Q70 24 68.5 35 '
               'Q66 25 58 24 Q50 28 42 24 Q34 25 31.5 35 Z', hc)
    elif style == 'pigtails':
        s += P('M31.5 37 Q30 17 50 17 Q70 17 68.5 37 Q66 26 56 24 Q50 28 44 24 Q34 26 31.5 37 Z', hc)
        s += C(32, 31, 3.2, '#E5534B', 1.6) + C(68, 31, 3.2, '#E5534B', 1.6)
    elif style == 'long':
        s += P('M31 37 Q30 16 50 16 Q70 16 69 37 Q66 25 55 22 Q46 29 31 37 Z', hc)
    elif style == 'short':
        s += P('M31.5 33 Q31 16 50 16 Q69 16 68.5 33 Q67 24 60 22.5 Q50 26 40 22.5 Q33 24 31.5 33 Z', hc)
    elif style == 'bun':
        s += P('M31.5 37 Q30 17 50 17 Q70 17 68.5 37 Q67 26 58 23.5 Q50 27 42 23.5 Q33 26 31.5 37 Z', hc)
    elif style == 'bald':
        s += P('M31.2 40 Q30 30 34 25 Q36 30 36.5 40 Z', hc) + P('M68.8 40 Q70 30 66 25 Q64 30 63.5 40 Z', hc)
        s += P('M42 21 Q46 19 50 19.5', sw=1.4)
    if kind == 'dad':
        s += P('M31.5 38 Q32 56 50 56 Q68 56 68.5 38 Q66 47 59 47 Q50 44 41 47 Q34 47 31.5 38 Z', hc)
    s += face_small(50, 38, mood, look)
    if style in ('bun', 'bald') or kind == 'teacher':
        s += C(43.5 + look, 38, 5.3, 'none', 1.8) + C(56.5 + look, 38, 5.3, 'none', 1.8)
        s += P(f'M{48.8 + look} 37.5 H{51.2 + look} M{38.2 + look} 37 L32 35 M{61.8 + look} 37 L68 35', sw=1.8)
    if kind == 'grandpa':
        s += P('M41 46.5 Q45.5 43 50 45.5 Q54.5 43 59 46.5 Q55 50 50 48 Q45 50 41 46.5 Z', hc, 1.6)
    return s


def person(kind, mood='smile', look=0, shirt=None):
    return body(kind, shirt) + head(kind, mood, look)


# hand with the index finger out, wrist at origin, finger toward -y
HAND_POINT = ('<rect x="-6.8" y="-30" width="5" height="19" rx="2.5" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
              '<path d="M-7 -3 Q-8 -8 -7.5 -12 Q-7 -15.5 -3 -15.5 H4 Q8 -15.5 8 -11.5 V-5 Q8 0 3 0 H-3 Q-6.5 0 -7 -3 Z" '
              'fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
              '<path d="M-1.5 -11.3 H6 M-1.5 -7.4 H6" fill="none" stroke="{L}" stroke-width="{w2}"/>'
              '<path d="M-7.3 -8 Q-3 -5.5 1.5 -6.6" fill="none" stroke="{L}" stroke-width="{w2}"/>')


def point_hand(x, y, rot=0, sc=1.25, mirror=False):
    w = round(W / sc, 2); w2 = round(1.4 / sc, 2)
    sx = -sc if mirror else sc
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {sc})">' + HAND_POINT.format(SK=SK, L=L, w=w, w2=w2) + '</g>'


def arrow_to(d, x, y, ang, color=ARROW, sw=5, size=7):
    """Path `d` ending at x,y plus a head there pointing along `ang` degrees (0 = right, 90 = down).
    Drawn with a dark outline so it reads on any background."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    bx, by = x - ux * size * 1.3, y - uy * size * 1.3
    px, py = -uy * size, ux * size
    tip = (x + ux * 2, y + uy * 2)
    head = f'M{tip[0]:.1f} {tip[1]:.1f} L{bx + px:.1f} {by + py:.1f} L{bx - px:.1f} {by - py:.1f} Z'
    return (P(d, 'none', sw + 2 * W, L) + P(head, color, W) + P(d, 'none', sw, color)
            + P(head, color, 0))


# ---------- family ----------

def single(kind):
    return place(person(kind), 50, 40, 1.12)


@picto('mom', 'mama')
def mom():
    return single('mom')


@picto('dad', 'otec')
def dad():
    return single('dad')


@picto('brother', 'brat')
def brother():
    return place(person('brother'), 50, 44, 1.05)


@picto('sister', 'sestra')
def sister():
    return place(person('sister'), 50, 44, 1.05)


@picto('grandma', 'babička')
def grandma():
    return single('grandma')


@picto('grandpa', 'dedko')
def grandpa():
    return single('grandpa')


@picto('teacher', 'učiteľ')
def teacher():
    s = P('M4 8 H96 V66 H4 Z', '#3F6E55', W) + P('M8 12 H92 V62 H8 Z', '#2F5A44', 1.2)
    s += P('M14 22 Q20 16 26 22 T38 22', sw=1.8, stroke='#FFFFFF') + P('M14 34 H34 M14 44 H28', sw=1.8, stroke='#FFFFFF')
    s += P('M72 20 L80 34 H64 Z', sw=1.8, stroke='#FFFFFF')
    s += place(person('teacher'), 50, 50, 0.95)
    return s


# ---------- pronouns ----------

def me_pointing(dx=0, mood='smile'):
    """The child pointing at his own chest (kit coordinates)."""
    d = 'M78 104 Q80 92 69 88'
    s = arm_back(d) + torso(0, 59) + arm_fill(d) + headb(0, 36) + face_small(50, 38, mood)
    s += point_hand(68, 89, -50, 1.15)
    return s


@picto('he', 'on')
def he():
    s = place(person('he'), 56, 52, 0.95)
    s += arrow_to('M10 10 Q14 30 30 38', 30, 38, 30)
    return s


@picto('she', 'ona')
def she():
    s = place(person('she'), 56, 52, 0.95)
    s += arrow_to('M10 10 Q14 30 30 38', 30, 38, 30)
    return s


def group(y=58, k=0.72):
    s = place(person('dad', shirt='#8DCFC1'), 50, y - 8, k)
    s += place(person('sister', shirt='#F6C453'), 24, y, k * 0.9)
    s += place(person('brother', shirt='#F5A3C7'), 76, y, k * 0.9)
    return s


@picto('they', 'oni')
def they():
    s = group(64, 0.7)
    s += arrow_to('M50 4 V30', 50, 30, 90)
    return s


@picto('you', 'vy')
def you():
    s = group(42, 0.64)
    d = 'M98 108 Q86 94 78 86'
    s += P(d, 'none', 15 + 2 * W, L) + P(d, 'none', 15, '#8D8DA8')
    s += point_hand(77, 86, -40, 1.4, mirror=True)
    return s


@picto('we', 'my')
def we():
    s = C(50, 62, 46, HILITE, 0)
    s += place(person('sister', shirt='#F6C453'), 20, 54, 0.66)
    s += place(person('dad', shirt='#8DCFC1'), 80, 50, 0.72)
    s += place(me_pointing(), 50, 56, 0.8)
    return s


@picto('meAcc', 'mňa')
def me_acc():
    s = place(me_pointing(), 42, 42, 0.95)
    s += arrow_to('M98 30 Q86 46 74 56', 74, 56, 140)
    return s


@picto('us', 'nás')
def us():
    s = C(46, 64, 42, HILITE, 0)
    s += place(person('sister', shirt='#F6C453'), 20, 58, 0.62)
    s += place(person('dad', shirt='#8DCFC1'), 72, 54, 0.66)
    s += place(me_pointing(), 46, 60, 0.74)
    s += arrow_to('M98 6 Q90 22 80 26', 80, 26, 150)
    return s
