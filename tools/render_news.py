#!/usr/bin/env python3
"""Render the front page image for make.fun bounty news-image-20261122.

Sums up the world news of Sunday 22 November 2026 in one 1024x1024 PNG.
Pure Python standard library only (zlib, struct, os). No network, no files
read, no timestamps, no randomness: two runs produce byte-identical output.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 render_news.py
    # writes out/entry.png (default ./out/entry.png when unset)
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 231)
INK = (28, 28, 28)
NAVY = (22, 41, 77)
NAVY_DARK = (14, 28, 54)
GOLD = (201, 162, 39)
RED = (179, 39, 30)
WHITE = (255, 253, 246)
PANEL = (255, 253, 246)
PANEL_LINE = (203, 192, 172)
MUTED = (90, 84, 72)
BLUE = (38, 90, 140)
GREEN = (46, 125, 72)
ORANGE = (224, 122, 26)
GREY = (120, 118, 112)
LIGHT_GREY = (205, 203, 196)
SKY = (168, 200, 224)
SEA = (52, 110, 158)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 characters, '#' = ink, '.' = empty.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10001", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "11110", "10001", "10001", "11110", "10000", "10000"),
    'q': ("00000", "01111", "10001", "10001", "01111", "00001", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11110", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10001", "01111"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10001", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "10001", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.rect(0, 0, w, h, bg)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c, t=1):
        for k in range(t):
            self.rect(x, y + k, w, 1, c)

    def vline(self, x, y, h, c, t=1):
        for k in range(t):
            self.rect(x + k, y, 1, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        if fill:
            for yy in range(cy - r, cy + r + 1):
                dx = int((r * r - (yy - cy) * (yy - cy)) ** 0.5) if abs(yy - cy) <= r else 0
                self.rect(cx - dx, yy, 2 * dx + 1, 1, c)
        else:
            import math
            for deg in range(0, 360):
                a = deg * 3.141592653589793 / 180.0
                self.set(cx + int(r * math.cos(a)), cy + int(r * math.sin(a)), c)

    def ellipse(self, cx, cy, rx, ry, c, fill=True):
        if fill:
            for yy in range(cy - ry, cy + ry + 1):
                t = 1.0 - ((yy - cy) / ry) ** 2
                dx = int(rx * (t ** 0.5)) if t > 0 else 0
                self.rect(cx - dx, yy, 2 * dx + 1, 1, c)

    def poly(self, pts, c):
        # scanline fill of a simple polygon
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.rect(int(xs[k]), y, max(1, int(xs[k + 1]) - int(xs[k])), 1, c)

    def text(self, x, y, s, scale, c):
        cx = x
        for ch in s:
            g = FONT.get(ch)
            if g is None:
                g = FONT[' ']
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_center(self, y, s, scale, c):
        x = (self.w - self.text_w(s, scale)) // 2
        self.text(x, y, s, scale, c)
        return x


def wrap(text, max_w, scale):
    """Word-wrap to lines no wider than max_w px (scale-sized font)."""
    words = text.split(' ')
    lines = []
    cur = ''
    for wd in words:
        trial = wd if not cur else cur + ' ' + wd
        if len(trial) * 6 * scale - scale <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # hard-split overlong words
            while len(wd) * 6 * scale - scale > max_w:
                n = max_w // (6 * scale)
                lines.append(wd[:n])
                wd = wd[n:]
            cur = wd
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# Verified against at least two independent sources each (see README):
#  1 COP31 collapse, Antalya — CNN, UN News, WRI
#  2 Kyiv-region drone strike, Dymer — Reuters, Kyiv Independent
#  3 Iran strikes Bahrain + tankers near Hormuz — AP, CNN
#  4 BepiColombo in Mercury orbit — AP/Phys.org, Fana News (QNA)
#  5 Indonesia candy-factory fire search — Reuters, AP
#  6 South Korea education minister resigns — Korea JoongAng Daily, KBS
#  7 Shuri Castle hall restored — AP, Asia Daily
LEAD = {
    'tag': 'ANTALYA, TURKIYE  -  CLIMATE',
    'headline': ['COP31 COLLAPSES:', 'NO DEAL ON', 'FOSSIL FUELS'],
    'caption': ('After two weeks of talks and record overtime, the UN climate '
                'summit ends with no pact. The EU refused a deal that never '
                'named fossil fuels.'),
    'art': 'cop31',
}

PANELS = [
    {
        'tag': 'UKRAINE  -  WAR',
        'color': RED,
        'headline': 'DRONE HITS FLAT NEAR KYIV; 14 MISSING',
        'caption': ('A Russian drone partly collapsed a five-storey block in '
                    'Dymer. Nine were evacuated.'),
        'art': 'kyiv',
    },
    {
        'tag': 'THE GULF  -  ESCALATION',
        'color': RED,
        'headline': 'IRAN STRIKES AT BAHRAIN AND TANKERS',
        'caption': ('Tehran hits a US radar site in Bahrain, its third strike '
                    'in five days.'),
        'art': 'gulf',
    },
    {
        'tag': 'SPACE  -  MERCURY',
        'color': BLUE,
        'headline': 'BEPICOLOMBO REACHES MERCURY ORBIT',
        'caption': ('After an eight-year cruise, the ESA-JAXA probe is caught '
                    'by Mercury’s gravity.'),
        'art': 'mercury',
    },
    {
        'tag': 'INDONESIA  -  DISASTER',
        'color': ORANGE,
        'headline': 'SEARCH FOR DOZENS AFTER FACTORY FIRE',
        'caption': ('Rescuers hunt for 36 missing after a blaze at a candy '
                    'plant near Jakarta. Three workers are dead.'),
        'art': 'factory',
    },
    {
        'tag': 'SOUTH KOREA  -  EDUCATION',
        'color': BLUE,
        'headline': 'MINISTER QUITS OVER AI CHEATING ROW',
        'caption': ('Choi Kyo-jin resigns after last-minute anti-cheating '
                    'rules sowed chaos before the exam.'),
        'art': 'korea',
    },
    {
        'tag': 'OKINAWA  -  HERITAGE',
        'color': RED,
        'headline': 'SHURI CASTLE BACK AFTER 7 YEARS',
        'caption': ('Okinawa celebrates the rebuilt main hall of Shuri Castle, '
                    'lost to fire in 2019. It opens Monday.'),
        'art': 'shuri',
    },
]


# ---------------------------------------------------------------- art
def art_cop31(cv, x, y, w, h):
    # globe + broken pact document + smoke
    cx, cy, r = x + 78, y + h // 2 + 8, 62
    cv.circle(cx, cy, r, BLUE)
    cv.circle(cx, cy, r - 6, (86, 158, 196))
    cv.ellipse(cx - 22, cy - 14, 26, 12, GREEN)
    cv.ellipse(cx + 24, cy + 18, 22, 10, GREEN)
    cv.ellipse(cx + 8, cy - 30, 14, 8, GREEN)
    for k in range(-2, 3):
        cv.line(cx + k * 22, cy - r + 4, cx + k * 22, cy + r - 4, (140, 190, 220), 1)
    cv.circle(cx, cy, r, NAVY, fill=False)
    # document, torn, with red X
    dx, dy = x + 168, y + 30
    cv.rect(dx, dy, 96, 128, WHITE)
    cv.rect(dx, dy, 96, 128, INK)
    for i in range(5):
        cv.hline(dx + 10, dy + 18 + i * 18, 76, MUTED, 2)
    cv.line(dx + 14, dy + 14, dx + 82, dy + 114, RED, 5)
    cv.line(dx + 82, dy + 14, dx + 14, dy + 114, RED, 5)
    # smoke puffs
    for (sx, sy, sr) in ((x + 200, y + 12, 12), (x + 226, y + 4, 15), (x + 250, y + 14, 10)):
        cv.circle(sx, sy, sr, GREY)


def art_kyiv(cv, x, y, w, h):
    # apartment block, right side collapsed, drone above, smoke
    bx, by = x + 30, y + 10
    cv.rect(bx, by, 150, 64, (150, 146, 158))
    cv.rect(bx, by, 150, 64, INK)
    for r in range(4):
        for c in range(5):
            wx = bx + 12 + c * 28
            wy = by + 8 + r * 14
            cv.rect(wx, wy, 14, 10, (255, 214, 130) if (r + c) % 3 else SKY)
    # collapsed jagged right edge
    cv.poly([(bx + 150, by), (bx + 196, by + 14), (bx + 186, by + 34),
             (bx + 200, by + 50), (bx + 182, by + 64), (bx + 150, by + 64)],
            (96, 94, 96))
    # rubble
    for (rx, ry, rw, rh) in ((bx + 150, by + 64, 20, 7), (bx + 174, by + 64, 16, 9),
                             (bx + 194, by + 64, 14, 6)):
        cv.rect(rx, ry, rw, rh, (96, 94, 96))
    # drone
    dx, dy = x + w - 90, y + 6
    cv.rect(dx, dy, 26, 10, INK)
    cv.hline(dx - 10, dy - 4, 46, INK, 2)
    cv.hline(dx - 10, dy + 12, 46, INK, 2)
    # smoke
    cv.circle(bx + 176, y + 4, 10, GREY)
    cv.circle(bx + 194, y + 2, 12, LIGHT_GREY)


def art_gulf(cv, x, y, w, h):
    # tanker on waves, explosion star, missile arc
    wy = y + 64
    cv.rect(x, wy, w, 26, SEA)
    for k in range(6):
        cv.line(x + k * 78, wy + 8, x + k * 78 + 34, wy + 8, WHITE, 2)
        cv.line(x + k * 78 + 20, wy + 17, x + k * 78 + 54, wy + 17, WHITE, 2)
    hx, hy = x + 60, wy - 26
    cv.rect(hx, hy, 260, 26, (44, 44, 48))
    cv.rect(hx + 200, hy - 16, 46, 16, (200, 60, 40))
    for c in range(5):
        cv.rect(hx + 14 + c * 34, hy - 12, 28, 12, (201, 162, 39) if c % 2 else (38, 90, 140))
    # explosion star
    ex, ey = x + w - 70, y + 24
    for ang in range(0, 360, 30):
        import math
        a = ang * 3.141592653589793 / 180.0
        cv.line(ex, ey, ex + int(18 * math.cos(a)), ey + int(18 * math.sin(a)), ORANGE, 3)
    cv.circle(ex, ey, 9, (255, 214, 90))
    cv.circle(ex, ey, 5, RED)
    # missile arc
    cv.line(x + 20, y + 10, x + 110, y + 34, INK, 2)
    cv.circle(x + 112, y + 35, 4, INK)


def art_mercury(cv, x, y, w, h):
    # cratered Mercury + spacecraft on orbit ellipse
    cx, cy, r = x + 80, y + 46, 38
    cv.circle(cx, cy, r, (168, 160, 148))
    cv.circle(cx, cy, r, INK, fill=False)
    for (kx, ky, kr) in ((cx - 15, cy - 10, 7), (cx + 12, cy + 6, 9),
                         (cx + 19, cy - 18, 5), (cx - 4, cy + 19, 6),
                         (cx + 2, cy - 1, 4)):
        cv.circle(kx, ky, kr, (140, 132, 120))
        cv.circle(kx, ky, kr, (120, 112, 100), fill=False)
    # orbit ellipse (drawn as ring of dots)
    import math
    for deg in range(0, 360, 4):
        a = deg * 3.141592653589793 / 180.0
        px = x + 210 + int(140 * math.cos(a))
        py = y + 46 + int(34 * math.sin(a))
        cv.rect(px, py, 3, 3, MUTED)
    # spacecraft
    sx, sy = x + 320, y + 22
    cv.rect(sx, sy, 30, 18, (200, 200, 200))
    cv.rect(sx, sy, 30, 18, INK)
    cv.rect(sx - 40, sy + 3, 36, 11, BLUE)
    cv.rect(sx + 34, sy + 3, 36, 11, BLUE)
    cv.rect(sx + 10, sy - 9, 9, 9, GOLD)


def art_factory(cv, x, y, w, h):
    # factory with sawtooth roof, flames, smoke, ladder
    bx, by = x + 40, y + 52
    cv.rect(bx, by, 220, 38, (176, 160, 138))
    cv.rect(bx, by, 220, 38, INK)
    for k in range(4):
        cv.poly([(bx + k * 55, by), (bx + k * 55 + 27, by - 14),
                 (bx + k * 55 + 55, by)], (120, 110, 92))
    for k in range(4):
        cv.rect(bx + 16 + k * 52, by + 12, 26, 14, (255, 214, 130))
    # chimney
    cv.rect(bx + 228, by - 28, 18, 66, (140, 132, 120))
    cv.rect(bx + 228, by - 28, 18, 66, INK)
    # flames
    for (fx, fy, fs) in ((bx + 30, by - 2, 16), (bx + 90, by - 4, 20),
                         (bx + 150, by - 2, 14)):
        cv.poly([(fx - fs, fy), (fx, fy - fs * 2), (fx + fs, fy)], ORANGE)
        cv.poly([(fx - fs // 2, fy), (fx, fy - fs), (fx + fs // 2, fy)], (255, 214, 90))
    # smoke
    cv.circle(bx + 237, y + 12, 10, GREY)
    cv.circle(bx + 254, y + 4, 12, LIGHT_GREY)
    # ladder leaning
    cv.line(bx + 280, by + 38, bx + 316, by - 8, RED, 3)
    cv.line(bx + 296, by + 38, bx + 332, by - 8, RED, 3)


def art_korea(cv, x, y, w, h):
    # exam desk: paper with questions + checks, graduation cap, AI chip
    px, py = x + 50, y + 8
    cv.rect(px, py, 140, 80, WHITE)
    cv.rect(px, py, 140, 80, INK)
    cv.hline(px + 12, py + 12, 116, INK, 3)
    for i in range(4):
        cv.hline(px + 12, py + 28 + i * 14, 84, MUTED, 2)
        cv.rect(px + 104, py + 23 + i * 14, 11, 11, WHITE)
        cv.rect(px + 104, py + 23 + i * 14, 11, 11, GREEN)
        cv.line(px + 106, py + 28 + i * 14, px + 109, py + 32 + i * 14, WHITE, 2)
        cv.line(px + 109, py + 32 + i * 14, px + 114, py + 25 + i * 14, WHITE, 2)
    # graduation cap
    cx, cy = x + 290, y + 34
    cv.poly([(cx - 48, cy), (cx, cy - 20), (cx + 48, cy), (cx, cy + 20)], INK)
    cv.rect(cx - 24, cy + 2, 48, 14, INK)
    cv.line(cx + 48, cy, cx + 48, cy + 30, GOLD, 3)
    cv.circle(cx + 48, cy + 34, 5, GOLD)
    # AI chip
    chipx, chipy = x + 290, y + 68
    cv.rect(chipx - 28, chipy - 10, 56, 24, NAVY)
    cv.text(chipx - 12, chipy - 4, 'AI', 2, WHITE)
    for k in range(3):
        cv.hline(chipx - 36, chipy - 6 + k * 8, 8, NAVY, 2)
        cv.hline(chipx + 28, chipy - 6 + k * 8, 8, NAVY, 2)


def art_shuri(cv, x, y, w, h):
    # red castle with tiered roofs, sun, stone steps
    cx = x + w // 2
    cv.circle(x + w - 52, y + 18, 16, (255, 196, 90))
    cv.circle(x + w - 52, y + 18, 16, ORANGE, fill=False)
    base_y = y + 88
    # steps
    for k in range(3):
        cv.rect(cx - 84 + k * 11, base_y - 8 - k * 8, 168 - k * 22, 8, (150, 146, 138))
    # lower tier
    cv.rect(cx - 70, base_y - 34, 140, 26, (178, 32, 28))
    cv.rect(cx - 70, base_y - 34, 140, 26, INK)
    cv.poly([(cx - 82, base_y - 34), (cx, base_y - 54), (cx + 82, base_y - 34)], (122, 18, 16))
    # upper tier
    cv.rect(cx - 46, base_y - 72, 92, 20, (178, 32, 28))
    cv.rect(cx - 46, base_y - 72, 92, 20, INK)
    cv.poly([(cx - 56, base_y - 72), (cx, base_y - 88), (cx + 56, base_y - 72)], (122, 18, 16))
    cv.circle(cx, base_y - 88, 4, GOLD)
    # windows
    for wx in (cx - 52, cx - 7, cx + 38):
        cv.rect(wx, base_y - 28, 14, 14, (255, 214, 130))


ART = {
    'cop31': art_cop31, 'kyiv': art_kyiv, 'gulf': art_gulf,
    'mercury': art_mercury, 'factory': art_factory,
    'korea': art_korea, 'shuri': art_shuri,
}


# ---------------------------------------------------------------- page
def build():
    cv = Canvas(W, H, PAPER)

    # masthead
    cv.rect(0, 0, W, 128, NAVY)
    cv.rect(0, 0, W, 6, GOLD)
    cv.text_center(16, 'THE WORLD TODAY', 7, WHITE)
    cv.hline(212, 84, 600, GOLD, 2)
    cv.text_center(94, 'SUNDAY, 22 NOVEMBER 2026', 3, (232, 214, 160))

    # lead story: COP31
    lx, ly, lw, lh = 24, 144, 976, 228
    cv.rect(lx, ly, lw, lh, PANEL)
    cv.rect(lx, ly, lw, lh, PANEL_LINE)
    cv.rect(lx, ly, 6, lh, RED)
    cv.text(lx + 24, ly + 16, LEAD['tag'], 2, RED)
    hy = ly + 44
    for line in LEAD['headline']:
        cv.text(lx + 24, hy, line, 4, INK)
        hy += 36
    cap_lines = wrap(LEAD['caption'], 620, 2)
    cy = ly + 160
    for line in cap_lines:
        cv.text(lx + 24, cy, line, 2, MUTED)
        cy += 18
    ART[LEAD['art']](cv, lx + 660, ly + 16, 300, lh - 32)

    # six panels, 2 columns x 3 rows
    px0, py0 = 24, 388
    pw, ph, gx, gy = 476, 192, 24, 14
    for idx, p in enumerate(PANELS):
        x = px0 + (idx % 2) * (pw + gx)
        y = py0 + (idx // 2) * (ph + gy)
        cv.rect(x, y, pw, ph, PANEL)
        cv.rect(x, y, pw, ph, PANEL_LINE)
        cv.rect(x, y, pw, 5, p['color'])
        # illustration strip (90 px tall, art drawn to fit it)
        ART[p['art']](cv, x + 12, y + 10, pw - 24, 90)
        cv.hline(x + 12, y + 104, pw - 24, PANEL_LINE, 1)
        cv.text(x + 12, y + 112, p['tag'], 2, p['color'])
        hl = wrap(p['headline'], pw - 24, 2)
        hy = y + 130
        for line in hl[:2]:
            cv.text(x + 12, hy, line, 2, INK)
            hy += 18
        cl = wrap(p['caption'], pw - 24, 2)
        cy = hy
        for line in cl[:3]:
            if cy + 14 > y + ph - 2:
                break
            cv.text(x + 12, cy, line, 2, MUTED)
            cy += 14

    # footer
    cv.hline(24, 1000, 976, PANEL_LINE, 2)
    cv.text_center(1008, 'THE WORLD TODAY  -  SUNDAY 22 NOVEMBER 2026', 2, MUTED)
    return cv


# ---------------------------------------------------------------- png
def write_png(cv, path):
    raw = bytearray()
    for yy in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[yy * cv.w * 3:(yy + 1) * cv.w * 3]

    def chunk(typ, data):
        c = struct.pack('>I', len(data)) + typ + data
        c += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
        return c

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', './out')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'entry.png')
    cv = build()
    size = write_png(cv, path)
    print('wrote %s (%d bytes)' % (path, size))


if __name__ == '__main__':
    main()
