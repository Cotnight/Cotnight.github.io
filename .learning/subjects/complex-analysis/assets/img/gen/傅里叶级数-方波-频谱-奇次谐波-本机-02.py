# -*- coding: utf-8 -*-
"""产图脚本：方波的频谱——只有奇次谐波，幅度按 1/n 衰减。

主格是幅度谱：横轴是谐波次数 n，每根竖线的高度是 |c_n| = 2/(nπ)（n 为奇数），
偶次与 n = 0 处在轴上是 0。虚线是包络 2/(nπ)，说明幅度按 1/n 衰减。
右格写系数、幅度、相位的数值与三句结论。

输出：assets/img/pool/傅里叶级数-方波-频谱-奇次谐波-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '傅里叶级数-方波-频谱-奇次谐波-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 760
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (120, 120, 120)
LIGHT = (170, 170, 170)
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
    for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        mdraw(d, (xy[0] + ox, xy[1] + oy), text, size, bg, anchor=anchor)
    return mdraw(d, xy, text, size, fill, anchor=anchor)


def dash_poly(d, pts, color, width=2, dash=9, gap=7):
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


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

mdraw(d, (W / 2, 28), '频谱：只有奇次谐波，幅度按 1/n 衰减', 31, INK, anchor='ma')

BOX = (40, 92, 856, 700)
d.rectangle(BOX, outline=FRAME, width=2)

NM = 10.5
YTOP = 0.72


def px(n):
    return BOX[0] + 40 + (n + NM) / (2 * NM) * (BOX[2] - BOX[0] - 76)


def py(v):
    return BOX[3] - 66 - v / YTOP * (BOX[3] - BOX[1] - 150)


# 轴
d.line([(px(-NM), py(0)), (px(NM), py(0))], fill=GREY, width=2)
d.line([(px(0), py(0)), (px(0), py(YTOP) + 10)], fill=LIGHT, width=2)
mdraw(d, (px(NM) - 4, py(0) + 20), 'n', 27, GREY, anchor='ra')
mdraw(d, (px(NM) - 10, py(YTOP) + 6), '|c_{n}|', 26, GREY, anchor='ra')

for n in range(-10, 11):
    if n % 2 == 0 and n != 0:
        d.ellipse([px(n) - 4, py(0) - 4, px(n) + 4, py(0) + 4], fill=LIGHT)
        continue
    if n == 0:
        d.ellipse([px(0) - 5, py(0) - 5, px(0) + 5, py(0) + 5], fill=RED)
        continue
    h = 2.0 / (abs(n) * math.pi)
    d.line([(px(n), py(0)), (px(n), py(h))], fill=BLUE, width=4)
    d.ellipse([px(n) - 6, py(h) - 6, px(n) + 6, py(h) + 6], fill=BLUE)
    if abs(n) <= 9:
        mdraw_halo(d, (px(n), py(h) - 34), f'{h:.3f}', 23, BLUE, anchor='ma')

# 包络 2/(nπ)，两侧对称
env_x = [1 + 0.02 * i for i in range(0, 476)]
dash_poly(d, [(px(x), py(2 / (x * math.pi))) for x in env_x], ORANGE, width=2)
dash_poly(d, [(px(-x), py(2 / (x * math.pi))) for x in env_x], ORANGE, width=2)

for t in range(-10, 11, 2):
    mdraw_halo(d, (px(t), py(0) + 22), str(t), 24, GREY, anchor='ma')

mdraw_halo(d, (px(-10.2), py(0.26)), '灰点：偶次项为 0', 24, GREY, anchor='la')
mdraw_halo(d, (px(4.1), py(0.44)), '包络 2/(nπ)', 24, ORANGE, anchor='la')

# 右格
TBOX = (884, 92, 1204, 700)
d.rectangle(TBOX, outline=FRAME, width=2)
mdraw(d, (906, 110), '系数与幅度', 28, INK, anchor='la')
lines = [
    ('c_{n} = −2i/(nπ)　n 为奇数', BLUE),
    ('c_{n} = 0　　　　 n 为偶数', BLUE),
    ('c_{0} = 0', RED),
    ('', INK),
    ('|c_{n}| = 2/(nπ)', GREEN),
    ('n = 1　0.637　基波', INK),
    ('n = 3　0.212', INK),
    ('n = 5　0.127', INK),
    ('n = 7　0.091', INK),
    ('', INK),
    ('c_{−n} 与 c_{n} 共轭：', INK),
    ('幅度相同、相位相反。', INK),
]
y = 150
for text, color in lines:
    if text:
        mdraw(d, (906, y), text, 24, color, anchor='la')
    y += 34

mdraw(d, (906, y + 16), '次数越高幅度越小，', 23, GREY, anchor='la')
mdraw(d, (906, y + 44), '但永远不为零；跳变', 23, GREY, anchor='la')
mdraw(d, (906, y + 72), '越陡，需要的高频越多。', 23, GREY, anchor='la')

mdraw(d, (W / 2, H - 42),
      '频谱就是把这些柱子的高低按 n 排开：偶次没有，奇次按 1/n 递减。',
      24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
