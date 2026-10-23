"""Numbers 0-9 (digit plus that many dots) and the numbers folder icon."""
from kit import *
from sets.abc import glyph, tile, COLORS

DIGITS = {
    0: 'M50 12 Q68 12 68 35 Q68 58 50 58 Q32 58 32 35 Q32 12 50 12 Z',
    1: 'M40 22 L52 12 V58 M38 58 H66',
    2: 'M34 24 Q36 12 50 12 Q66 12 66 26 Q66 36 34 58 H68',
    3: 'M35 18 Q42 12 50 12 Q65 12 65 24 Q65 34 48 35 Q68 36 68 47 Q68 58 50 58 Q38 58 32 50',
    4: 'M58 58 V12 L32 44 H70',
    5: 'M65 12 H38 L36 33 Q42 29 50 29 Q67 29 67 43 Q67 58 50 58 Q38 58 33 50',
    6: 'M62 17 Q56 12 48 12 Q33 14 33 40 Q33 58 50 58 Q67 58 67 43 Q67 28 50 28 Q36 28 33 42',
    7: 'M32 12 H68 L46 58',
    8: 'M50 33 Q36 33 36 22 Q36 12 50 12 Q64 12 64 22 Q64 33 50 33 Q33 34 33 46 Q33 58 50 58 Q67 58 67 46 Q67 34 50 33 Z',
}
NAMES = ['nula', 'jeden', 'dva', 'tri', 'štyri', 'päť', 'šesť', 'sedem', 'osem', 'deväť']
DOT = 4.6


def dots(n):
    if n == 0:
        return C(50, 83, DOT, 'none', 2)
    if n <= 5:
        rows = [n]; ys = [83]
    else:
        rows = [(n + 1) // 2, n // 2]; ys = [76, 89]
    s = ''
    for cnt, y in zip(rows, ys):
        for j in range(cnt):
            x = 50 + (j - (cnt - 1) / 2) * 12.5
            s += C(round(x, 1), y, DOT, COLORS[(n) % 5], 2)
    return s


def digit(n, color, lw=11, fw=7.5):
    if n == 9:
        return f'<g transform="rotate(180 50 35)">{glyph(DIGITS[6], color, lw, fw)}</g>'
    return glyph(DIGITS[n], color, lw, fw)


def make(n):
    @picto(f'number.{n}', NAMES[n])
    def f():
        return digit(n, COLORS[n % 5]) + dots(n)
    return f


for n in range(10):
    make(n)


@picto('numbers', 'čísla')
def numbers():
    def t(n, color, cx, cy, rot):
        inner = digit(n, color, 13 / 1.3, 9 / 1.3)
        return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale(0.45) translate(-50 -50)">'
                f'<rect x="14" y="10" width="72" height="80" rx="14" fill="#FFFFFF" stroke="{L}" stroke-width="4.4"/>'
                f'<g transform="translate(50 50) scale(1.3) translate(-50 -35)">{inner}</g></g>')
    return t(1, RED, 24, 54, -9) + t(3, GREEN, 76, 54, 9) + t(2, '#5B8DEF', 50, 48, 0)
