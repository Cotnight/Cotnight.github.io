# -*- coding: utf-8 -*-
"""产图脚本：沿折线求积分，每一段各写一个参数式、各算一个定积分，最后相加。

左边是 z 平面上的折线 C: 1 → 1+i → i（两段带方向箭头）；
右边三格依次是 C₁、C₂ 两段的参数式、dz、被积函数与定积分结果，以及相加后的总数。

输出：assets/img/pool/复积分-参数化计算-折线分段-本机-01.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '复积分-参数化计算-折线分段-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 720
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
AXIS = (80, 80, 80)
GRID = (236, 236, 236)
FRAME = (200, 200, 200)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
GREEN = (24, 120, 84)
BAND = (240, 246, 252)
BAND_EDGE = (176, 205, 232)

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


def rich(d, xy, text, size, fill, anchor='la'):
    """中英混排：中文用雅黑、数学符号用 Cambria，按总宽度对齐。"""
    segs = runs(text)
    total = 0.0
    for s, c in segs:
        f = font(FONT_CJK if c else FONT_MATH, size)
        total += d.textlength(s, font=f)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for s, c in segs:
        f = font(FONT_CJK if c else FONT_MATH, size)
        d.text((x, y), s, font=f, fill=fill, anchor='l' + anchor[1])
        x += d.textlength(s, font=f)


def arrow(d, p0, p1, color, width=4, head=13):
    d.line([p0, p1], fill=color, width=width)
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = max((dx * dx + dy * dy) ** 0.5, 1e-9)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    d.polygon([(x1, y1),
               (x1 - ux * head * 1.6 + px * head * 0.7,
                y1 - uy * head * 1.6 + py * head * 0.7),
               (x1 - ux * head * 1.6 - px * head * 0.7,
                y1 - uy * head * 1.6 - py * head * 0.7)], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- 左：z 平面上的折线 ----------
X0, Y0, X1, Y1 = 46, 86, 520, 606
d.rectangle((X0, Y0, X1, Y1), outline=FRAME, width=2)
OX, OY, UNIT = 196, 486, 132          # 原点像素位置与每单位长度

for k in range(1, 5):
    d.line([(OX + UNIT * k, Y0 + 6), (OX + UNIT * k, Y1 - 6)], fill=GRID, width=1)
    d.line([(OX - UNIT * k, Y0 + 6), (OX - UNIT * k, Y1 - 6)], fill=GRID, width=1)
    d.line([(X0 + 6, OY - UNIT * k), (X1 - 6, OY - UNIT * k)], fill=GRID, width=1)
d.line([(X0 + 10, OY), (X1 - 12, OY)], fill=AXIS, width=2)
d.line([(OX, Y1 - 10), (OX, Y0 + 12)], fill=AXIS, width=2)
rich(d, (X1 - 24, OY + 8), 'x', 24, AXIS, anchor='la')
rich(d, (OX + 8, Y0 + 8), 'y', 24, AXIS, anchor='la')

p_1 = (OX + UNIT, OY)
p_1i = (OX + UNIT, OY - UNIT)
p_i = (OX, OY - UNIT)

arrow(d, (p_1[0], p_1[1] - 14), (p_1i[0], p_1i[1] + 16), BLUE)
arrow(d, (p_1i[0] - 14, p_1i[1]), (p_i[0] + 16, p_i[1]), ORANGE)

for p in (p_1, p_1i, p_i):
    d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=INK)
rich(d, (p_1[0] + 12, p_1[1] + 10), '1', 26, INK, anchor='la')
rich(d, (p_i[0] - 26, p_i[1] - 10), 'i', 26, INK, anchor='la')
rich(d, (p_1i[0] + 12, p_1i[1] - 12), '1 + i', 26, INK, anchor='la')
rich(d, (p_1[0] + 16, p_1[1] - 96), 'C₁', 28, BLUE, anchor='la')
rich(d, (p_i[0] + 74, p_1i[1] + 16), 'C₂', 28, ORANGE, anchor='la')
rich(d, (OX, OY + 22), 'O', 24, AXIS, anchor='la')

# ---------- 右：两段各自的参数式与结果 ----------
BX0, BX1 = 566, 1194


def box(y0, y1, title, lines, color):
    d.rounded_rectangle((BX0, y0, BX1, y1), radius=10, outline=color, width=3)
    rich(d, (BX0 + 22, y0 + 12), title, 27, color, anchor='la')
    y = y0 + 56
    for text, size, fill in lines:
        rich(d, (BX0 + 22, y), text, size, fill, anchor='la')
        y += size + 16


box(86, 264, '第一段 C₁：从 1 到 1 + i', [
    ('z = 1 + it ，  0 ≤ t ≤ 1 ，  dz = i dt', 23, GREY),
    ('Re z + Im z = 1 + t', 23, GREY),
    ('∫₀¹ (1 + t) i dt = (3/2) i', 30, INK),
], BLUE)

box(280, 458, '第二段 C₂：从 1 + i 到 i', [
    ('z = 1 + i − t ，  0 ≤ t ≤ 1 ，  dz = − dt', 23, GREY),
    ('Re z + Im z = 2 − t', 23, GREY),
    ('∫₀¹ − (2 − t) dt = − 3/2', 30, INK),
], ORANGE)

d.rounded_rectangle((BX0, 474, BX1, 588), radius=12, fill=BAND, outline=BAND_EDGE, width=3)
rich(d, (BX0 + 22, 488), '两段相加', 27, GREY, anchor='la')
rich(d, ((BX0 + BX1) / 2, 530), '∫C (Re z + Im z) dz = − 3/2 + (3/2) i', 33, INK, anchor='ma')

rich(d, (W / 2, 636),
     '每一段各从 t = 0 起算；竖直段的 dz 是 − dt 还是 i dt，由 t 增大的方向与题目给的方向定。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
