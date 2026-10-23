import sys
L = '#2A2A2A'; W = 2
RED = '#E5534B'; GREEN = '#3BA55D'; WATER = '#6EC1F0'; GLASS = '#F2F6FA'

def P(d, fill='none', sw=W, stroke=L):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def E(cx, cy, rx, ry, fill, sw=W, stroke=L, rot=0):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{t}/>'
def C(cx, cy, r, fill, sw=W, stroke=L):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def svg(name, body):
    return (f'<svg viewBox="0 0 100 100" width="240" height="240" stroke-linecap="round" stroke-linejoin="round" '
            f'role="img" aria-label="{name}" style="border:1px solid #ccc;overflow:hidden">{body}</svg>')

out = []

# voda
s = P('M30 16 L70 16 L65 86 L35 86 Z', GLASS)
s += P('M31.6 36 Q41 32 50 36 Q59 40 68.4 36 L65.3 84 L34.7 84 Z', WATER, 0)
s += P('M31.6 36 Q41 32 50 36 Q59 40 68.4 36', sw=1.8)
s += P('M30 16 L70 16 L65 86 L35 86 Z')
s += P('M38 44 L40 76', sw=2.4, stroke='#FFFFFF')
out.append(svg('voda', s))

# mlieko (krabica)
s = P('M38 10 H62 V17 H38 Z', '#FFFFFF')
s += P('M30 33 L38 17 H62 L70 33 Z', '#FFFFFF')
s += P('M30 33 H70 V88 H30 Z', '#FFFFFF')
s += P('M30 50 H70 V72 H30 Z', '#5B8DEF')
s += P('M50 53 Q44 61 44 64.5 A6 6 0 0 0 56 64.5 Q56 61 50 53 Z', '#FFFFFF', 1.6)
out.append(svg('mlieko', s))

# džús
s = P('M30 26 L66 26 L62 88 L34 88 Z', GLASS)
s += P('M31.3 42 H64.7 L62.2 86 H33.8 Z', '#F7A23B', 0)
s += P('M31.3 42 H64.7', sw=1.6)
s += P('M52 60 L62 12 L74 10', 'none', 6.5, L) + P('M52 60 L62 12 L74 10', 'none', 3, RED)
s += P('M30 26 L66 26 L62 88 L34 88 Z')
s += P('M14 28 A14 14 0 0 1 42 28 Z', '#F7A23B')
s += P('M28 28 V16 M28 28 L19 19 M28 28 L37 19', sw=1.4)
out.append(svg('džús', s))

# chlieb: bochník + odkrojený krajec
s = P('M8 72 Q8 40 40 38 Q66 40 70 58 V84 H20 Q8 84 8 72 Z', '#D9A066')
s += P('M20 48 Q26 42 32 44 M34 43 Q40 38 46 40 M48 45 Q54 41 60 45', sw=2.2, stroke='#9A5B2E')
s += P('M60 50 Q60 36 74 36 Q88 36 88 50 V86 H60 Z', '#B9824A')
s += P('M63.5 51 Q63.5 40 74 40 Q84.5 40 84.5 51 V82.5 H63.5 Z', '#F6DDB0', 0)
s += P('M68 56 h0.1 M78 52 h0.1 M72 66 h0.1 M80 70 h0.1 M68 76 h0.1', sw=2, stroke='#D9B27A')
out.append(svg('chlieb', s))

# rožok
s = P('M10 58 Q12 40 32 38 Q50 36 70 38 Q90 40 90 56 Q88 68 70 68 H30 Q10 70 10 58 Z', '#E1A45B')
s += P('M26 40 Q21 53 26 66 M38 38 Q33 52 38 68 M50 37 Q45 52 50 68 M62 37 Q57 52 62 68 M74 39 Q69 52 74 66', sw=1.8, stroke='#A8652E')
out.append(svg('rožok', s))

# jablko
s = P('M50 30 Q36 20 24 30 Q13 41 17 58 Q23 83 40 85 Q46 86 50 82 Q54 86 60 85 Q77 83 83 58 Q87 41 76 30 Q64 20 50 30 Z', RED)
s += P('M50 30 Q49 20 53 12', sw=2.6)
s += P('M53 20 Q62 11 73 15 Q64 25 53 20 Z', GREEN)
s += E(33, 45, 4, 7, '#F6A39D', 0, rot=25)
out.append(svg('jablko', s))

# banán
s = P('M20 30 Q20 76 64 82 Q84 84 90 72 Q70 74 52 64 Q32 52 28 28 Z', '#F7D154')
s += P('M28 28 L23 21 Q19 24 20 30 Z', '#6B4226', 1.6)
s += P('M90 72 L94 75 L93 68 Z', '#8A6D2B', 1.6)
s += P('M26 40 Q30 64 62 76', sw=1.6, stroke='#D4A92A')
out.append(svg('banán', s))

# syr
s = P('M12 52 L62 30 L88 44 L38 66 Z', '#FBE08A')
s += P('M12 52 L38 66 V84 L12 70 Z', '#F2C94C')
s += P('M38 66 L88 44 V62 L38 84 Z', '#F7D46A')
s += E(52, 50, 4.5, 2.4, '#E0B23A', 1.2) + E(68, 40, 3, 1.6, '#E0B23A', 1.2)
s += E(56, 70, 3, 4, '#E0B23A', 1.2) + E(74, 61, 2.6, 3.4, '#E0B23A', 1.2) + E(24, 66, 2.6, 3.6, '#E0B23A', 1.2)
out.append(svg('syr', s))

# polievka
s = P('M42 44 Q38 38 42 32 Q46 26 42 20 M52 42 Q48 36 52 30 Q56 24 52 18 M62 44 Q58 38 62 32 Q66 26 62 20', sw=2, stroke='#9AA3AE')
s += P('M14 58 H86 Q86 88 50 88 Q14 88 14 58 Z', '#FFFFFF')
s += E(50, 58, 36, 8, '#F4A340')
s += P('M60 58 L80 32', 'none', 5, L) + P('M60 58 L80 32', 'none', 2.4, '#ECEFF4')
s += E(57, 60, 7, 3.6, '#ECEFF4', 1.8, rot=-10)
out.append(svg('polievka', s))

# cestoviny: špagety na tanieri s vidličkou
s = E(50, 70, 42, 16, '#FFFFFF') + E(50, 68, 30, 10, '#FFFFFF', 1.4)
s += P('M20 66 Q24 50 50 48 Q76 50 80 66 Q50 74 20 66 Z', '#F7D16B')
s += P('M24 62 Q30 54 36 62 Q42 70 48 60 Q54 52 60 62 Q66 70 72 60 Q75 56 77 62', sw=1.6, stroke='#C9962A')
s += P('M28 56 Q36 50 42 56 Q48 62 54 54 Q60 48 68 56 Q72 60 74 56', sw=1.6, stroke='#C9962A')
s += P('M38 52 Q46 47 52 51 Q58 55 64 50', sw=1.6, stroke='#C9962A')
s += P('M58 58 L82 24', 'none', 5, L) + P('M58 58 L82 24', 'none', 2.4, '#ECEFF4')
s += P('M77 30 Q80 33 87 30 L88 28 M78.5 28 L82 17 M82 29.5 L85.5 18.5 M85.5 30 L89 19', sw=2.2)
s += E(48, 53, 7, 3.6, '#D9483B', 1.6)
out.append(svg('cestoviny', s))

# jogurt
s = P('M29 36 L71 36 L66 88 L34 88 Z', '#FFFFFF')
s += P('M30.6 54 H69.4 L67.7 72 H32.3 Z', '#F2A1B6', 0)
s += P('M30.6 54 H69.4 M32.3 72 H67.7', sw=1.4)
s += C(50, 63, 5, RED, 1.4) + P('M47 58.5 Q50 55 53 58.5', sw=1.4, stroke=GREEN)
s += P('M24 29 H76 Q78 29 78 31 V35 Q78 37 76 37 H24 Q22 37 22 35 V31 Q22 29 24 29 Z', '#ECEFF4')
s += P('M29 36 L71 36 L66 88 L34 88 Z')
out.append(svg('jogurt', s))

# keksík
s = C(50, 52, 32, '#D9A066')
for (x, y, rx, ry, r) in [(38, 38, 4, 3, 20), (60, 36, 3.5, 2.6, -15), (66, 54, 4, 3, 30), (44, 58, 3.6, 2.8, 0), (32, 52, 3, 2.4, 40), (54, 72, 4, 3, -20), (36, 70, 3, 2.4, 10), (70, 70, 2.8, 2.2, 0)]:
    s += E(x, y, rx, ry, '#6B4226', 0, rot=r)
out.append(svg('keksík', s))

html = ('<!doctype html><html><body style="margin:0;background:#fff;display:grid;grid-template-columns:repeat(6,250px);gap:8px;padding:8px">'
        + ''.join(out) + '</body></html>')
open(sys.argv[1], 'w', encoding='utf-8').write(html)
