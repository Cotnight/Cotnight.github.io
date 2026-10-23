# -*- coding: utf-8 -*-
"""产图脚本：同一类被积函数换一条围道，圈内奇点的个数就变。

输出：assets/img/pool/留数-围道与奇点-计数-本机-02.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '留数-围道与奇点-计数-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 770
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (205, 205, 205)
AXIS = (222, 226, 232)
BLUE = (32, 105, 190)
DEEP = (26, 78, 140)
WARMINK = (150, 84, 30)

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

rich(d, (60, 20), '同一个函数换一条围道，圈进来的奇点就变了', 30, DEEP, anchor='la')
rich(d, (60, 64), '留数定理的求和项数等于围道内的奇点数；圈外的点既不参与相加，也不影响 2πi',
     22, GREY, anchor='la')

PANELS = [
    dict(x0=60, head=['1/((z+1)(z+2)²)', 'C：|z| = 3'],
         scale=38.0, r=3.0,
         poles=[(-1.0, 0.0, '−1', -22, 'R'),
                (-2.0, 0.0, '−2（二阶）', 6, 'R')],
         out=[],
         res=['圈内：−1（一阶）、−2（二阶）', '2πi(1 − 1) = 0']),
    dict(x0=455, head=['tan z', 'C：|z| = 2'],
         scale=34.0, r=2.0,
         poles=[(0.0, 1.5708, 'π/2', -34, 'C'),
                (0.0, -1.5708, '−π/2', 18, 'C')],
         out=[(0.0, 4.7124, '3π/2'), (0.0, -4.7124, '−3π/2')],
         res=['圈内：±π/2 两点，留数各 −1', '2πi(−1 − 1) = −4πi']),
    dict(x0=850, head=['exp(z)/((z−πi)(z−2πi)²)', 'C：|z| = 8'],
         scale=18.0, r=8.0,
         poles=[(0.0, 3.1416, 'πi', -22, 'R'),
                (0.0, 6.2832, '2πi（二阶）', 6, 'R')],
         out=[],
         res=['圈内：πi（一阶）、2πi（二阶）', '2πi(1/π² + (1−πi)/π²)', '= 2 + (4/π)i']),
]

PW = 350
PY = 330

for P in PANELS:
    x0 = P['x0']
    x1 = x0 + PW
    cx = (x0 + x1) // 2
    d.rounded_rectangle((x0, 96, x1, 700), radius=14, fill=BG,
                        outline=FRAME, width=2)
    for i, line in enumerate(P['head']):
        rich(d, (cx, 110 + i * 26), line, 21, DEEP, anchor='ma')
    d.line([(x0 + 16, PY), (x1 - 16, PY)], fill=AXIS, width=2)
    d.line([(cx, 172), (cx, PY + 128)], fill=AXIS, width=2)
    R = P['scale'] * P['r']
    d.ellipse([cx - R, PY - R, cx + R, PY + R], outline=BLUE, width=3)
    rich(d, (cx + R + 10, PY - 10), 'C', 22, BLUE, anchor='la')
    for (u, v, lab) in P['out']:
        px = cx + P['scale'] * u
        yy = PY - P['scale'] * v
        d.ellipse([px - 7, yy - 7, px + 7, yy + 7], outline=GREY, width=2)
        rich(d, (px + 16, yy - 13), lab, 19, GREY, anchor='la')
    for (u, v, lab, dy, side) in P['poles']:
        px = cx + P['scale'] * u
        yy = PY - P['scale'] * v
        d.ellipse([px - 8, yy - 8, px + 8, yy + 8], fill=BLUE)
        if side == 'R':
            rich(d, (px + 16, yy + dy), lab, 20, INK, anchor='la')
        elif side == 'L':
            rich(d, (px - 16, yy + dy), lab, 20, INK, anchor='ra')
        else:
            rich(d, (px, yy + dy), lab, 20, INK, anchor='ma')
    rich(d, (x0 + 18, 500), '结果', 20, WARMINK, anchor='la')
    for i, line in enumerate(P['res']):
        rich(d, (x0 + 18, 530 + i * 27), line, 21, INK, anchor='la')

rich(d, (60, H - 34),
     '灰圈是圈外的点：它们不参与求和；圈内漏数一个，答案就差出整项。',
     21, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
