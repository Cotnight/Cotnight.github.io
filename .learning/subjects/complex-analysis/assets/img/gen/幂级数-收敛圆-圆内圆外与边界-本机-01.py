# -*- coding: utf-8 -*-
"""产图脚本：幂级数的收敛圆——圆内绝对收敛、圆外发散、圆上单独判。

左格：以 z0 为心、R 为半径的收敛圆。圆内标「绝对收敛」，圆外标「发散」；圆内一处绿点
      z1 外面套一条虚线小圆，表示阿贝尔定理给出的那句结论：在 z1 收敛，则 |z − z0| < |z1|
      的每个点都绝对收敛。圆上的点用红点标出，结论要代进级数单独判。
右格：阿贝尔定理的两句结论、收敛半径的定义与两个极端值 R = 0、R = +∞。

输出：assets/img/pool/幂级数-收敛圆-圆内圆外与边界-本机-01.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '幂级数-收敛圆-圆内圆外与边界-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 760
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
FILL_IN = (233, 245, 236)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
RED = (176, 42, 42)
GREEN = (24, 120, 84)

CACHE = {}


def font(path, size):
    key = (path, size)
    if key not in CACHE:
        CACHE[key] = ImageFont.truetype(path, size)
    return CACHE[key]


CJK_PUNCT = set('：，、。（）·—…“”‘’《》')


def is_cjk(ch):
    o = ord(ch)
    return (0x4E00 <= o <= 0x9FFF) or (0x3000 <= o <= 0x303F) or \
           (0xFF00 <= o <= 0xFFEF) or ch in CJK_PUNCT


def runs(text):
    out = []
    for ch in text:
        c = is_cjk(ch)
        if out and out[-1][1] == c:
            out[-1][0] += ch
        else:
            out.append([ch, c])
    return [(s, c) for s, c in out]


def tokens(text):
    """切成 (串, shift)：0 正常，1 下标，-1 上标。写法 _{X} 与 ^{X}。"""
    segs = []
    buf = ''
    i = 0
    while i < len(text):
        if text.startswith('_{', i) or text.startswith('^{', i):
            if buf:
                segs.append((buf, 0))
                buf = ''
            j = text.index('}', i)
            segs.append((text[i + 2:j], 1 if text[i] == '_' else -1))
            i = j + 1
        else:
            buf += text[i]
            i += 1
    if buf:
        segs.append((buf, 0))
    return segs


def mdraw(d, xy, text, size, fill, anchor='la'):
    """按字符类型分段选字体，并把 _{X} 画成下标、^{X} 画成上标。"""
    pieces = []
    for s, shift in tokens(text):
        f_size = int(round(size * 0.72)) if shift else size
        for part, cjk in runs(s):
            f = font(FONT_CJK if cjk else FONT_MATH, f_size)
            dy = 0
            if shift == 1:
                dy = size * 0.30
            elif shift == -1:
                dy = -size * 0.34
            pieces.append((part, f, dy, d.textlength(part, font=f)))
    total = sum(p[3] for p in pieces)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for part, f, dy, w in pieces:
        d.text((x, y + dy), part, font=f, fill=fill, anchor='l' + anchor[1])
        x += w
    return total


def arrow_head(d, p_from, p_to, color, head=13):
    (x0, y0), (x1, y1) = p_from, p_to
    dx, dy = x1 - x0, y1 - y0
    n = max(math.hypot(dx, dy), 1e-9)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    d.polygon([(x1, y1),
               (x1 - ux * head * 1.7 + px * head * 0.75,
                y1 - uy * head * 1.7 + py * head * 0.75),
               (x1 - ux * head * 1.7 - px * head * 0.75,
                y1 - uy * head * 1.7 - py * head * 0.75)], fill=color)


def arc_arrow(d, center, r, a0, a1, color, width=4, heads=(60, 88)):
    n = max(int(abs(a1 - a0) / 0.04), 12)
    pts = [(center[0] + r * math.cos(a0 + (a1 - a0) * i / n),
            center[1] - r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=color, width=width)
    for k in heads:
        i = max(1, min(n, int(n * k / 100)))
        arrow_head(d, pts[i - 1], pts[i], color)


def dot(d, p, r=6, color=INK):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

mdraw(d, (W / 2, 34), '收敛圆：圆内绝对收敛，圆外发散，圆上的点单独判', 30, INK, anchor='ma')

# ---------------- 左格：收敛圆 ----------------
BOX = (36, 84, 664, 612)
d.rectangle(BOX, outline=FRAME, width=2)
C0 = (350, 372)
R = 170

d.ellipse([C0[0] - R, C0[1] - R, C0[0] + R, C0[1] + R], fill=FILL_IN)
d.ellipse([C0[0] - R, C0[1] - R, C0[0] + R, C0[1] + R], outline=BLUE, width=4)
arc_arrow(d, C0, R, 0.55, 0.55 + 2 * math.pi, BLUE, width=4, heads=(38, 76))

dot(d, C0, 6, INK)
mdraw(d, (C0[0] - 14, C0[1] + 12), 'z_{0}', 26, INK, anchor='la')

# 半径 R（水平向右）
d.line([(C0[0] + 8, C0[1]), (C0[0] + R, C0[1])], fill=GREY, width=2)
arrow_head(d, (C0[0] + R - 20, C0[1]), (C0[0] + R, C0[1]), GREY, head=11)
mdraw(d, (C0[0] + 70, C0[1] - 40), 'R', 29, GREY, anchor='la')

# 圆内：z1
a1 = 0.88 * math.pi
r1 = 0.58 * R
z1 = (C0[0] + r1 * math.cos(a1), C0[1] - r1 * math.sin(a1))
dot(d, z1, 7, GREEN)
mdraw(d, (z1[0] - 46, z1[1] + 8), 'z_{1}', 26, GREEN, anchor='la')
mdraw(d, (C0[0], C0[1] - 136), '圆内：绝对收敛', 26, GREEN, anchor='ma')

# 圆外：z2
a2 = 0.18 * math.pi
r2 = 1.30 * R
z2 = (C0[0] + r2 * math.cos(a2), C0[1] - r2 * math.sin(a2))
dot(d, z2, 7, RED)
mdraw(d, (z2[0] + 14, z2[1] - 16), 'z_{2} 发散', 25, RED, anchor='la')
mdraw(d, (BOX[0] + 14, BOX[1] + 12), '圆外：发散', 26, RED, anchor='la')

# 圆上的点
for a in (0.45 * math.pi, 0.98 * math.pi, -0.30 * math.pi):
    p = (C0[0] + R * math.cos(a), C0[1] - R * math.sin(a))
    dot(d, p, 6, ORANGE)
mdraw(d, (C0[0] + 96, C0[1] - R - 28), '|z − z_{0}| = R', 26, ORANGE, anchor='la')
mdraw(d, (BOX[0] + 14, BOX[3] - 58), '绿点在圆内、红点在圆外、橙点在圆上；', 22, GREY, anchor='la')
mdraw(d, (BOX[0] + 14, BOX[3] - 30), '圆上的点代进级数，化成数项级数再判。', 22, GREY, anchor='la')

# ---------------- 右格：阿贝尔定理 ----------------
T_BOX = (692, 84, 1204, 612)
d.rectangle(T_BOX, outline=FRAME, width=2)
mdraw(d, (718, 104), '阿贝尔定理（只记结论）', 28, INK, anchor='la')
lines = [
    ('在 z_{1} 收敛 ⟹ |z − z_{0}| < |z_{1}| 的点全绝对收敛', INK),
    ('在 z_{2} 发散 ⟹ |z − z_{0}| > |z_{2}| 的点全发散', INK),
    ('', INK),
    ('收敛圆  |z − z_{0}| < R', BLUE),
    ('R 是收敛半径，0 ≤ R ≤ +∞', BLUE),
    ('', INK),
    ('R = 0 ： 只在 z_{0} 收敛', GREY),
    ('R = +∞ ： 全平面收敛', GREY),
    ('', INK),
    ('圆内  |z − z_{0}| < R   绝对收敛', GREEN),
    ('圆外  |z − z_{0}| > R   发散', RED),
    ('圆上  |z − z_{0}| = R   单独判', ORANGE),
]
y = 152
for text, color in lines:
    if text:
        mdraw(d, (720, y), text, 25, color, anchor='la')
    y += 38

mdraw(d, (W / 2, H - 74),
      '收敛半径一次说清圆内与圆外；圆上的点没有统一结论，代进级数化成数项级数再判。',
      24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
