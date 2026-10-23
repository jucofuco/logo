"""Draws the app icon (no dependencies): a white speech bubble with three picture cards.

Run: python3 Scripts/make_icon.py  -> logo/Assets.xcassets/AppIcon.appiconset/icon.png
"""
import struct
import zlib

SIZE = 1024
SS = 2  # supersampling per axis for smooth edges

BG = (0x6E, 0x56, 0xCF)
BUBBLE = (0xFF, 0xFF, 0xFF)
CARDS = [(0xFF, 0xB0, 0x20), (0x34, 0xC7, 0x59), (0x0A, 0x84, 0xFF)]


def in_round_rect(x, y, x0, y0, x1, y1, r):
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    cx = min(max(x, x0 + r), x1 - r)
    cy = min(max(y, y0 + r), y1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def in_tail(x, y):
    # Triangle under the bubble, bottom left.
    ax, ay, bx, by, cx, cy = 300, 740, 460, 740, 270, 880
    d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    a = ((by - cy) * (x - cx) + (cx - bx) * (y - cy)) / d
    b = ((cy - ay) * (x - cx) + (ax - cx) * (y - cy)) / d
    return a >= 0 and b >= 0 and a + b <= 1


def color_at(x, y):
    for i, c in enumerate(CARDS):
        x0 = 246 + i * 190
        if in_round_rect(x, y, x0, 400, x0 + 150, 590, 30):
            return c
    if in_round_rect(x, y, 170, 270, 854, 760, 110) or in_tail(x, y):
        return BUBBLE
    return BG


def main():
    rows = []
    for py in range(SIZE):
        row = bytearray([0])
        for px in range(SIZE):
            acc = [0, 0, 0]
            for sy in range(SS):
                for sx in range(SS):
                    c = color_at(px + (sx + 0.5) / SS, py + (sy + 0.5) / SS)
                    acc[0] += c[0]; acc[1] += c[1]; acc[2] += c[2]
            row += bytes(v // (SS * SS) for v in acc)
        rows.append(bytes(row))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", SIZE, SIZE, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
    png += chunk(b"IEND", b"")
    with open("logo/Assets.xcassets/AppIcon.appiconset/icon.png", "wb") as f:
        f.write(png)


main()
