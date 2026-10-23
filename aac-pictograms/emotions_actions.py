import sys

L = '#2A2A2A'; SK = '#FAD7BE'; HAIR = '#6B4226'; SHIRT = '#8DBBEA'; MOUTH = '#7E2B2B'; TONGUE = '#E88080'
TEAR = '#6EC1F0'; RED = '#E5534B'; GREEN = '#3BA55D'; FOOD = '#F4A340'; OBJ = '#ECEFF4'; ANGRY = '#F5A99B'
W = 2  # uniform line weight

def P(d, fill='none', sw=W, stroke=L, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def C(cx, cy, r, fill, sw=W, stroke=L):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def E(cx, cy, rx, ry, fill, sw=W, stroke=L, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{t}/>'

# ---------- big emotion face (head fills the frame) ----------
def face(skin=SK):
    return (C(50, 54, 34, skin)
            + P('M16.6 50 Q14 18 50 17 Q86 18 83.4 50 Q82 33 75 28.5 Q70 34 62 30.5 Q56 36 48 31.5 Q40 36 33.5 30.5 Q24 32 16.6 50 Z', HAIR) )

def eye_open(cx, cy, r=5.2, pupil=2.6, py=0):
    # friendly solid eye with highlight (no sclera = no stare)
    rx = r * 0.72; ry = r * 0.95
    return E(cx, cy + py * 0.4, rx, ry, L, 0) + C(cx + rx * 0.35, cy + py * 0.4 - ry * 0.4, rx * 0.36, '#FFFFFF', 0)

def happy_eye(cx, cy):
    return P(f'M{cx-6} {cy+2} Q{cx} {cy-7} {cx+6} {cy+2}', sw=3)

def emo_happy():
    s = face()
    s += P('M27 39 Q35 33 43 37', sw=2.4) + P('M57 37 Q65 33 73 39', sw=2.4)
    s += happy_eye(36, 52) + happy_eye(64, 52)
    s += E(26, 64, 6, 4, '#F7A8A0', 0) + E(74, 64, 6, 4, '#F7A8A0', 0)
    s += P('M31 63 Q50 67 69 63 Q66 83 50 83 Q34 83 31 63 Z', '#B5413D')
    s += P('M40 78 Q50 72 60 78 Q55 82.5 50 82.5 Q45 82.5 40 78 Z', '#EE8C86', 0)
    s += P('M9 22 L14 27 M5 36 L11 37 M91 22 L86 27 M95 36 L89 37', sw=2.2)
    return s

def emo_sad():
    s = face()
    s += P('M26 46 Q32 36 43 36', sw=2.8) + P('M57 36 Q68 36 74 46', sw=2.8)
    for cx in (36, 64):
        s += E(cx, 54, 3.8, 4.8, L, 0) + C(cx + 1.3, 52.2, 1.4, '#FFFFFF', 0)
        s += P(f'M{cx-6} 48.5 Q{cx} 46.5 {cx+6} 49.5', sw=2)          # heavy upper lid
    s += P('M36 79 Q43 72 50 74 Q57 72 64 79', sw=2.8)              # wobbly frown
    s += P('M35 60 Q30 69 31.5 73 A5.2 5.2 0 0 0 41.5 73 Q42 69 35 60 Z', TEAR, 1.5)
    s += P('M65 60 Q62 65 63 67.5 A3.5 3.5 0 0 0 69.5 67.5 Q70 65 65 60 Z', TEAR, 1.4)
    return s

def emo_angry():
    s = face('#FBC9BE')
    s += P('M24 38 L45 47 L44 51 L23 43 Z', L, 0) + P('M76 38 L55 47 L56 51 L77 43 Z', L, 0)
    for cx in (36, 64):
        s += E(cx, 56, 3.6, 4.2, L, 0)
    s += E(25, 66, 6, 4, '#F08A7E', 0) + E(75, 66, 6, 4, '#F08A7E', 0)
    s += P('M38 79 Q39 70 50 70 Q61 70 62 79 Q50 75 38 79 Z', '#B5413D')   # shouting frown
    s += P('M14 20 Q10 14 15 10 Q20 6 18 2', sw=2.4, stroke=RED) + P('M86 20 Q90 14 85 10 Q80 6 82 2', sw=2.4, stroke=RED)
    s += P('M70 22 L76 28 M76 22 L70 28', sw=2.6, stroke=RED)              # anger mark
    return s

def emo_scared():
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

def emo_tired():
    s = '<g transform="rotate(-10 50 54)">' + face()
    s += P('M28 45 Q35 44 42 46', sw=2.2) + P('M58 46 Q65 44 72 45', sw=2.2)
    s += P('M29 53 Q35.5 58 42 53', sw=2.8) + P('M58 53 Q64.5 58 71 53', sw=2.8)
    s += P('M31 60 Q35.5 62 40 60 M60 60 Q64.5 62 69 60', sw=1.4, stroke='#B98A73')
    s += E(50, 73, 5, 7, '#B5413D') + '</g>'
    s += P('M80 16 Q84 20 80 24 M86 12 Q92 20 86 28', sw=2)  # small sigh lines
    return s

# ---------- cropped upper body (bleeds off bottom edge) ----------
def torso(dx=0, top=64):
    x = 50 + dx
    return P(f'M{x-36} 104 V{top+24} Q{x-36} {top+2} {x} {top} Q{x+36} {top+2} {x+36} {top+24} V104 Z', SHIRT)

def headb(dx=0, head_y=36, r=19):
    x = 50 + dx
    nb = head_y + r + 5.5
    s = P(f'M{x-5.5} {head_y+r-4} V{nb} Q{x} {nb+3.5} {x+5.5} {nb} V{head_y+r-4}', SK)
    s += C(x, head_y, r, SK)
    s += P(f'M{x-r+0.5} {head_y-1} Q{x-r} {head_y-r-1} {x} {head_y-r-1} Q{x+r} {head_y-r-1} {x+r-0.5} {head_y-1} '
           f'Q{x+r-3} {head_y-r*0.62} {x+7} {head_y-r*0.66} Q{x+1} {head_y-r*0.4} {x-5} {head_y-r*0.62} Q{x-r+3} {head_y-r*0.6} {x-r+0.5} {head_y-1} Z', HAIR)
    return s

def bust(dx=0, head_y=36, r=19):
    return torso(dx, head_y + r + 4) + headb(dx, head_y, r)

def arm_back(d, width=11):
    return P(d, 'none', width + 2 * W, L)
def arm_fill(d, width=11):
    return P(d, 'none', width, SHIRT)

def face_small(x, y, mood='smile', look=0):
    s = ''
    if mood == 'worried':
        s += P(f'M{x-11} {y-6} Q{x-7} {y-11} {x-2.5} {y-10}', sw=2.2) + P(f'M{x+2.5} {y-10} Q{x+7} {y-11} {x+11} {y-6}', sw=2.2)
    elif mood in ('smile', 'neutral', 'frown'):
        s += P(f'M{x-11} {y-8} Q{x-7} {y-11} {x-3} {y-9}', sw=2) + P(f'M{x+3} {y-9} Q{x+7} {y-11} {x+11} {y-8}', sw=2)
    if mood == 'pain':
        s += P(f'M{x-11} {y-2} L{x-5} {y+0.5} L{x-11} {y+3}', sw=2.4) + P(f'M{x+11} {y-2} L{x+5} {y+0.5} L{x+11} {y+3}', sw=2.4)
        s += P(f'M{x-6} {y+12} Q{x-3} {y+9} {x} {y+12} Q{x+3} {y+15} {x+6} {y+12}', sw=2)
        return s
    s += eye_open(x - 6.5 + look, y, r=3.6) + eye_open(x + 6.5 + look, y, r=3.6)
    if mood == 'smile':
        s += P(f'M{x-8} {y+8} Q{x} {y+9} {x+8} {y+8} Q{x+6} {y+16} {x} {y+16} Q{x-6} {y+16} {x-8} {y+8} Z', '#B5413D', 1.6)
    elif mood in ('frown', 'worried'):
        s += P(f'M{x-6} {y+14} Q{x} {y+7} {x+6} {y+14}', sw=2.2)
    elif mood == 'open':
        s += E(x, y + 11, 3.2, 3.8, '#B5413D', 1.6)
    elif mood == 'neutral':
        s += P(f'M{x-4} {y+11} H{x+4}', sw=2)
    return s

# detailed open hand, wrist at origin, fingers toward -y
HAND_OPEN = ('<path d="M-5 -2 L-12.8 -11.6 A2.1 2.1 0 0 1 -9.6 -14.2 L-3.5 -8 Z" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M-6 0 C-7 -4 -7.6 -8 -7.6 -11 L-7.6 -20 A1.9 1.9 0 0 1 -3.8 -20 L-3.8 -12.5 L-3.8 -22.6 A1.9 1.9 0 0 1 0 -22.6 '
             'L0 -12.5 L0 -21.6 A1.9 1.9 0 0 1 3.8 -21.6 L3.8 -12.5 L3.8 -18.4 A1.8 1.8 0 0 1 7.4 -18.4 L7.4 -9 C7.4 -5 6.8 -2 6 0 Z" '
             'fill="{SK}" stroke="{L}" stroke-width="{w}"/>')
# fist holding something, wrist at origin, object passes vertically through x≈0
HAND_GRIP = ('<rect x="-7" y="-14" width="13" height="13" rx="4" fill="{SK}" stroke="{L}" stroke-width="{w}"/>'
             '<path d="M-7 -10.8 H3 M-7 -7.6 H3 M-7 -4.4 H3" fill="none" stroke="{L}" stroke-width="{w2}"/>'
             '<rect x="2" y="-18" width="5" height="11" rx="2.5" fill="{SK}" stroke="{L}" stroke-width="{w}"/>')

def hand(kind, x, y, rot=0, sc=1.25, mirror=False):
    w = round(W / sc, 2); w2 = round(1.4 / sc, 2)
    t = HAND_OPEN if kind == 'open' else HAND_GRIP
    sx = -sc if mirror else sc
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({sx} {sc})">' + t.format(SK=SK, L=L, w=w, w2=w2) + '</g>'

def arm(d, width=11):
    return P(d, 'none', width + 2 * W, L) + P(d, 'none', width, SHIRT)

def arrow(d, heads, color, sw=3):
    s = P(d, 'none', sw, color)
    for h in heads:
        s += P(h, color, 1.2, color)
    return s

def svg(name, body):
    return (f'<svg viewBox="0 0 100 100" width="240" height="240" stroke-linecap="round" stroke-linejoin="round" '
            f'role="img" aria-label="{name}" style="border:1px solid #ccc;overflow:hidden">{body}</svg>')

out = []
out.append(svg('veselý', emo_happy()))
out.append(svg('smutný', emo_sad()))
out.append(svg('nahnevaný', emo_angry()))
out.append(svg('vystrašený', emo_scared()))
out.append(svg('unavený', emo_tired()))

# áno: big green check (thin dark outline around a thick green stroke)
ck = 'M20 52 L41 73 L80 28'
out.append(svg('áno', P(ck, 'none', 19, L) + P(ck, 'none', 15, GREEN)))

# nie: big red X
xx = 'M24 24 L76 76 M76 24 L24 76'
out.append(svg('nie', P(xx, 'none', 19, L) + P(xx, 'none', 15, RED)))

# chcem: reach toward apple
d = 'M38 80 Q50 60 62 52'
s = arm_back(d) + torso(-22, 61) + arm_fill(d) + headb(-22, 38) + face_small(28, 40, 'smile', look=2)
s += C(83, 26, 9.5, '#E5534B') + P('M83 16.5 Q83 11 88 10', sw=1.8) + P('M83 15 Q87 9 92 12 Q88 16 83 15 Z', GREEN, 1.4)
s += hand('open', 63, 51, 52, 1.15)
s += P('M70 32 L73 36 M74 40 L78 41', sw=1.8)
out.append(svg('chcem', s))

# pomoc: raised waving hand
d = 'M58 84 Q72 64 70 40'
s = arm_back(d) + torso(-10, 63) + arm_fill(d) + headb(-10, 40) + face_small(40, 42, 'worried')
s += hand('open', 70, 38, 4, 1.25)
s += P('M82 12 Q86 18 82 24 M87 9 Q93 18 87 27', sw=2)
out.append(svg('pomoc', s))

# jesť
s = bust(0, 34, 20) + face_small(50, 36, 'open')
s += arm('M80 104 Q86 76 70 66')
s += P('M69 63 L55.5 47.5', sw=3) + E(53, 44.8, 6.4, 4.2, OBJ, 1.8, rot=48)
s += hand('grip', 70, 70, -45, 1.1)
s += P('M18 82 Q36 72 50 82 Z', FOOD, 1.6) + P('M14 82 H54 Q54 96 34 96 Q14 96 14 82 Z', OBJ)
out.append(svg('jesť', s))

# piť
s = bust(-4, 34, 20) + face_small(46, 36, 'open')
s += arm('M82 104 Q88 76 72 64')
s += f'<g transform="translate(60.5 49) rotate(-48)">' + P('M-7 -11 L7 -11 L5.5 11 L-5.5 11 Z', OBJ) + P('M-5.9 -3 L5.9 -3 L4.9 9.5 L-4.9 9.5 Z', TEAR, 0) + '</g>'
s += hand('grip', 71, 66, -48, 1.1)
out.append(svg('piť', s))

# bolí: hand on forehead, red pain marks
d = 'M58 86 Q78 62 62 34'
s = arm_back(d) + torso(-8, 65) + arm_fill(d) + headb(-8, 42) + face_small(42, 46, 'pain')
s += hand('open', 59, 33, -62, 1.15)
s += P('M18 18 L23 24 L19 26 L25 32', sw=2.4, stroke=RED) + P('M8 36 L15 37', sw=2.4, stroke=RED) + P('M80 14 L76 22 L81 22 L77 30', sw=2.4, stroke=RED)
out.append(svg('bolí', s))

html = ('<!doctype html><html><body style="margin:0;background:#fff;display:grid;grid-template-columns:repeat(6,250px);gap:8px;padding:8px">'
        + ''.join(out) + '</body></html>')
open(sys.argv[1], 'w', encoding='utf-8').write(html)
