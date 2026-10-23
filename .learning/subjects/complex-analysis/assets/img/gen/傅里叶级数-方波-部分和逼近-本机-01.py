# -*- coding: utf-8 -*-
"""产图脚本：方波的部分和——奇次谐波按 4/(nπ) 叠加。

主格画周期为 2π 的方波（灰色虚线）与它的三条部分和：只取基波、取到三次谐波、
取到九次谐波。三条曲线在 x = 0 与 x = ±π 的跳变处都经过 0，对应「级数在间断点
取左右极限的平均」。右格把展开式与系数写在图上。

输出：assets/img/pool/傅里叶级数-方波-部分和逼近-本机-01.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '傅里叶级数-方波-部分和逼近-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 780
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (120, 120, 120)
FRAME = (202, 202, 202)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
GREEN = (24, 120, 84)
RED = (176, 42, 42)

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
    segs, buf, i = [], '', 0
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


def mdraw_halo(d, xy, text, size, fill, anchor='la', bg=BG):
    """先画一圈底色再画字，压在曲线上的刻度与轴标签才读得清。"""
    for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        mdraw(d, (xy[0] + ox, xy[1] + oy), text, size, bg, anchor=anchor)
    return mdraw(d, xy, text, size, fill, anchor=anchor)


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


def dash_poly(d, pts, color, width=2, dash=10, gap=8):
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        ux, uy = dx / L, dy / L
        s = 0.0
        while s < L:
            e = min(s + dash, L)
            d.line([(a[0] + ux * s, a[1] + uy * s), (a[0] + ux * e, a[1] + uy * e)],
                   fill=color, width=width)
            s += dash + gap


def square_wave(x):
    """周期 2π 的方波：(-π,0) 上取 -1，(0,π) 上取 +1。"""
    y = math.atan2(math.sin(x), math.cos(x))
    return -1.0 if y < 0 else 1.0


def partial_sum(x, K):
    return (4.0 / math.pi) * sum(math.sin((2 * k - 1) * x) / (2 * k - 1)
                                 for k in range(1, K + 1))


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

mdraw(d, (W / 2, 30), '方波由奇次谐波叠加而成', 31, INK, anchor='ma')

BOX = (40, 92, 858, 700)
d.rectangle(BOX, outline=FRAME, width=2)

XMIN, XMAX = -2 * math.pi - 0.35, 2 * math.pi + 0.35
YMAX = 1.45
CY = (BOX[1] + BOX[3]) / 2 + 6
SCALE = (BOX[3] - BOX[1]) / 2 / YMAX - 12


def px(x):
    return BOX[0] + 26 + (x - XMIN) / (XMAX - XMIN) * (BOX[2] - BOX[0] - 50)


def py(y):
    return CY - y * SCALE


# 坐标轴
axis_y = py(0)
d.line([(px(XMIN), axis_y), (px(XMAX), axis_y)], fill=GREY, width=2)
d.line([(px(0), BOX[1] + 12), (px(0), BOX[3] - 12)], fill=GREY, width=2)
for t in (-2 * math.pi, -math.pi, math.pi, 2 * math.pi):
    d.line([(px(t), axis_y - 7), (px(t), axis_y + 7)], fill=GREY, width=2)

# 理想方波
xs = [XMIN + i * (XMAX - XMIN) / 720 for i in range(721)]
pts = [(px(x), py(square_wave(x))) for x in xs]
dash_poly(d, pts, GREY, width=3)


def curve(fn, color, width):
    ys = [fn(x) for x in xs]
    d.line([(px(x), py(y)) for x, y in zip(xs, ys)], fill=color, width=width)


curve(lambda x: partial_sum(x, 1), BLUE, 3)
curve(lambda x: partial_sum(x, 2), ORANGE, 3)
curve(lambda x: partial_sum(x, 5), GREEN, 3)

# 刻度与轴标签压在曲线之上，加底色保证可读
labels = [(-2 * math.pi, '−2π'), (-math.pi, '−π'), (math.pi, 'π'), (2 * math.pi, '2π')]
for t, s in labels:
    mdraw_halo(d, (px(t), py(0) + 14), s, 25, GREY, anchor='ma')
mdraw_halo(d, (px(XMAX) - 10, py(0) - 40), 'x', 27, GREY, anchor='ra')
mdraw_halo(d, (px(0) - 14, py(1.33)), '1', 25, GREY, anchor='ra')
mdraw_halo(d, (px(0) - 14, py(-1.33)), '−1', 25, GREY, anchor='ra')

# 跳变处的取值
for t in (0.0, math.pi, -math.pi):
    d.ellipse([px(t) - 6, py(0) - 6, px(t) + 6, py(0) + 6], fill=RED)
mdraw_halo(d, (px(0) + 18, py(0) - 44), '级数取值 0', 24, RED, anchor='la')

# 右格：展开式与系数
TBOX = (884, 92, 1204, 700)
d.rectangle(TBOX, outline=FRAME, width=2)
mdraw(d, (906, 110), '方波的展开式', 28, INK, anchor='la')
lines = [
    ('f(x) ~ (4/π)[ sin x', INK),
    ('　　　　 + sin 3x / 3', INK),
    ('　　　　 + sin 5x / 5 + … ]', INK),
    ('', INK),
    ('b_{n} = 4/(nπ)　n 为奇数', BLUE),
    ('b_{n} = 0　　　n 为偶数', BLUE),
    ('a_{n} = 0　（奇函数）', BLUE),
    ('c_{n} = −2i/(nπ)　n 为奇数', GREEN),
]
y = 150
for text, color in lines:
    if text:
        mdraw(d, (906, y), text, 24, color, anchor='la')
    y += 35

# 图例
y += 12
for color, label, dashed in ((GREY, '理想方波', True),
                             (BLUE, '取 1 项：sin x', False),
                             (ORANGE, '取 2 项：到 sin 3x', False),
                             (GREEN, '取 5 项：到 sin 9x', False)):
    if dashed:
        dash_poly(d, [(902, y + 11), (954, y + 11)], color, width=3)
    else:
        d.line([(902, y + 11), (954, y + 11)], fill=color, width=3)
    mdraw(d, (966, y), label, 23, INK, anchor='la')
    y += 32

mdraw(d, (906, y + 12), '项数越多，平顶越平、跳变越陡，', 23, GREY, anchor='la')
mdraw(d, (906, y + 40), '过冲不消失；跳变点始终取 0。', 23, GREY, anchor='la')

mdraw(d, (W / 2, H - 52),
      '跳变处左右极限是 −1 与 1，级数在那里取值 0，也就是两者的平均。',
      24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
