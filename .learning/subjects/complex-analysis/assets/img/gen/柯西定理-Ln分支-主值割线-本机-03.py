# -*- coding: utf-8 -*-
"""产图脚本：Ln z 要先定分支——从 1 到 −1 的两条半圆弧，积分值差一个 2πi。

上路（z = e^{iθ}, θ: 0 → π）arg 连续增到 π，与主值一致，代端点得 πi。
下路（θ: 0 → −π）arg 连续减到 −π，终点 −1 落在主值的割线上，主值只能给 π，
照主值代端点仍然得 πi，实际是 −πi；两支差 2πi。

输出：assets/img/pool/柯西定理-Ln分支-主值割线-本机-03.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '柯西定理-Ln分支-主值割线-本机-03.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 700
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
AXIS = (80, 80, 80)
FRAME = (200, 200, 200)
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


def rich(d, xy, text, size, fill, anchor='la'):
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


def arrow_head(d, p_from, p_to, color, head=14):
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


def arc_arrow(d, center, r, a0, a1, color, width=4, heads=(30, 65, 92)):
    n = max(int(abs(a1 - a0) / 0.03), 12)
    pts = [(center[0] + r * math.cos(a0 + (a1 - a0) * i / n),
            center[1] - r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=color, width=width)
    for k in heads:
        i = max(1, min(n, int(n * k / 100)))
        arrow_head(d, pts[i - 1], pts[i], color)


def dashed(d, p0, p1, color, width=3, dash=14, gap=10):
    (x0, y0), (x1, y1) = p0, p1
    n = max(math.hypot(x1 - x0, y1 - y0), 1e-9)
    ux, uy = (x1 - x0) / n, (y1 - y0) / n
    t = 0.0
    while t < n:
        a = (x0 + ux * t, y0 + uy * t)
        t2 = min(t + dash, n)
        b = (x0 + ux * t2, y0 + uy * t2)
        d.line([a, b], fill=color, width=width)
        t += dash + gap


def dot(p, r=6, color=INK):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- 左格：复平面 ----------
BOX = (40, 84, 600, 640)
d.rectangle(BOX, outline=FRAME, width=2)
O = (330, 372)
R = 152

d.line([(BOX[0] + 24, O[1]), (BOX[2] - 24, O[1])], fill=AXIS, width=2)
d.line([(O[0], BOX[3] - 24), (O[0], BOX[1] + 24)], fill=AXIS, width=2)
rich(d, (BOX[2] - 44, O[1] + 8), 'x', 23, AXIS, anchor='la')
rich(d, (O[0] + 10, BOX[1] + 56), 'y', 23, AXIS, anchor='la')

# 割线：负实轴
dashed(d, (O[0], O[1]), (BOX[0] + 30, O[1]), RED, width=3)
rich(d, (BOX[0] + 34, O[1] + 12), '割线：负实轴', 24, RED, anchor='la')

# 单位圆（浅色参考）
d.ellipse([O[0] - R, O[1] - R, O[0] + R, O[1] + R], outline=(226, 226, 226), width=2)

# 上路：1 → −1，逆时针
arc_arrow(d, O, R, 0.0, math.pi, BLUE, width=4, heads=(28, 62, 90))
rich(d, (O[0] - 30, O[1] - R - 46), '上路：得 πi', 25, BLUE, anchor='la')

# 下路：1 → −1，顺时针
arc_arrow(d, O, R, 0.0, -math.pi, ORANGE, width=4, heads=(28, 62, 90))
rich(d, (O[0] - 40, O[1] + R + 22), '下路：得 −πi', 25, ORANGE, anchor='la')

# 点与标注
dot((O[0] + R, O[1]), 6)
rich(d, (O[0] + R + 10, O[1] + 8), '1', 24, INK, anchor='la')
dot((O[0] - R, O[1]), 6, RED)
rich(d, (O[0] - R - 30, O[1] + 8), '−1', 24, RED, anchor='la')

d.ellipse([O[0] - 9, O[1] - 9, O[0] + 9, O[1] + 9], outline=RED, width=2)
rich(d, (O[0] + 16, O[1] + 16), '原点', 23, GREY, anchor='la')

rich(d, ((BOX[0] + BOX[2]) / 2, BOX[1] + 14),
     '同一对端点，两条路，两个答案', 25, INK, anchor='ma')

# ---------- 右格：分支与判据 ----------
T_BOX = (630, 84, 1200, 640)
d.rectangle(T_BOX, outline=FRAME, width=2)
lines = [
    ('主值 ln z = ln|z| + i Arg z', INK),
    ('Arg z 落在 (−π, π] 内', GREY),
    ('', INK),
    ('去掉原点与负实轴的区域内解析', GREEN),
    ('导数就是 1/z', GREEN),
    ('', INK),
    ('上路：ln(−1) − ln 1 = πi，与实算一致', BLUE),
    ('', INK),
    ('下路：终点 −1 落在割线上', ORANGE),
    ('主值只能给 πi，实算 −πi，差 2πi', ORANGE),
    ('', INK),
    ('判据：路径不跨割线、终点不在割线上', INK),
]
y = 116
for text, color in lines:
    if text:
        rich(d, (660, y), text, 25, color, anchor='la')
    y += 40

rich(d, (W / 2, 668),
     'ln 是 1/z 的原函数，只在某一块单连通区域里单值解析；路径换到另一块，就得换一支。',
     24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
