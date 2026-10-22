# -*- coding: utf-8 -*-
"""产图脚本：柯西-黎曼条件在三个函数上成立的点集。

z² 全平面成立（处处解析）；|z|² 只在原点成立（一点可导，不解析）；
z̄ 任何点都不成立（处处不解析）。三格对照，用来练「常见的处处不解析函数」。

输出：assets/img/pool/可导与解析-柯西黎曼条件-成立点集-本机-03.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '可导与解析-柯西黎曼条件-成立点集-本机-03.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 700
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
AXIS = (80, 80, 80)
GRID = (228, 228, 228)
FRAME = (196, 196, 196)
BLUE = (32, 105, 190)
RED = (192, 66, 40)
TINT_ALL = (226, 238, 250)

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


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

SIZE = 290
TOP = 96
PANELS = [
    (60, BLUE, TINT_ALL, False,
     'f(z) = z²', 'CR 在全平面成立', '图上整块区域都是成立点',
     ['处处可导，处处解析']),
    (475, RED, None, True,
     'f(z) = |z|²', 'CR 只在原点成立', '图上一个点成立',
     ['在 z = 0 可导；', '任何邻域内都有不可导的点，', '所以不解析']),
    (890, GREY, None, False,
     'f(z) = z̄', 'CR 处处不成立', '图上一个成立点也没有',
     ['处处不可导，', '处处不解析']),
]

rich(d, (W / 2, 28), '柯西-黎曼条件成立的点集（黑点为原点）', 28, INK, anchor='ma')

for x0, color, tint, dot, name, tag, tag2, concl in PANELS:
    y0 = TOP
    y1 = y0 + SIZE
    if tint:
        d.rectangle((x0, y0, x0 + SIZE, y1), fill=tint)
    d.rectangle((x0, y0, x0 + SIZE, y1), outline=FRAME, width=2)
    for g in range(1, 8):
        gx = x0 + SIZE * g / 8
        gy = y0 + SIZE * g / 8
        d.line([(gx, y0), (gx, y1)], fill=GRID, width=1)
        d.line([(x0, gy), (x0 + SIZE, gy)], fill=GRID, width=1)
    cx, cy = x0 + SIZE / 2, y0 + SIZE / 2
    d.line([(x0 + 6, cy), (x0 + SIZE - 6, cy)], fill=AXIS, width=2)
    d.line([(cx, y1 - 6), (cx, y0 + 6)], fill=AXIS, width=2)
    if dot:
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
    else:
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=AXIS)
    rich(d, (x0, y1 + 14), name, 30, INK, anchor='la')
    rich(d, (x0, y1 + 56), tag, 26, color, anchor='la')
    rich(d, (x0, y1 + 90), tag2, 24, GREY, anchor='la')
    yy = y1 + 130
    for line in concl:
        rich(d, (x0, yy), line, 25, color, anchor='la')
        yy += 33

rich(d, (W / 2, H - 42),
     '可导看「这一个点」，解析看「一整片邻域」：中间那一格就是两者的分界。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
