# -*- coding: utf-8 -*-
"""产图脚本：三格围道对照——奇点在圈内、圈内且幂次高、奇点在圈外。

输出：assets/img/pool/柯西积分公式-围道内外-奇点位置-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '柯西积分公式-围道内外-奇点位置-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 830
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (130, 130, 130)
LIGHT = (205, 205, 205)
BLUE = (32, 105, 190)
DEEP = (26, 78, 140)
RED = (198, 60, 48)
PANEL = (247, 249, 252)
FRAME = (219, 224, 230)

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

rich(d, (W / 2, 22), '围道把哪些奇点圈在里面，决定用哪条公式', 30, DEEP, anchor='ma')
rich(d, (W / 2, 66), '正向圆周 C 上的闭路积分：三种典型情形', 24, GREY, anchor='ma')

PX = [40, 440, 840]
PW = 360
PY0, PY1 = 108, 560

panels = [
    dict(cx=PX[0] + PW // 2, cy=(PY0 + PY1) // 2 + 10, u=56,
         cir=(0.0, 0.0, 2.0), poles=[(1.0, 0.0, 'z₀ = 1', 'in')],
         title='m = 1，z₀ 在 C 内',
         formula='= 2πi · 1 = 2πi',
         note=['g(z) = z，在 C 内解析', '代 z₀ = 1 直接乘 2πi']),
    dict(cx=PX[1] + PW // 2, cy=(PY0 + PY1) // 2 + 40, u=62,
         cir=(0.0, 1.0, 1.0), poles=[(0.0, 1.0, 'i', 'in')],
         title='m = 3，z₀ 在 C 内',
         formula='= (2πi / 2!) · (−cos i)',
         note=['g 求两阶导再代 z₀', '分母幂次 3 → 求 3 − 1 阶']),
    dict(cx=PX[2] + PW // 2, cy=(PY0 + PY1) // 2 + 10, u=46,
         cir=(0.0, 0.0, 1.0), poles=[(3.0, 0.0, '3', 'out')],
         title='z₀ 在 C 外',
         formula='= 0',
         note=['圈内没有奇点', '公式不适用，整项为 0']),
]

for p in panels:
    d.rounded_rectangle((p['cx'] - PW // 2, PY0, p['cx'] + PW // 2, PY1),
                        radius=14, fill=PANEL, outline=FRAME, width=2)
    cx, cy, u = p['cx'], p['cy'], p['u']
    # 坐标轴
    d.line([(cx - PW // 2 + 18, cy), (cx + PW // 2 - 18, cy)], fill=LIGHT, width=2)
    d.line([(cx, PY0 + 18), (cx, PY1 - 18)], fill=LIGHT, width=2)
    d.polygon([(cx + PW // 2 - 12, cy), (cx + PW // 2 - 24, cy - 5),
               (cx + PW // 2 - 24, cy + 5)], fill=LIGHT)
    d.polygon([(cx, PY0 + 12), (cx - 5, PY0 + 24), (cx + 5, PY0 + 24)], fill=LIGHT)
    # 围道 C
    a, b, r = p['cir']
    ox, oy = cx + a * u, cy - b * u
    rr = r * u
    d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], outline=BLUE, width=3)
    ang = math.radians(-38)
    d.text((ox + rr * math.cos(ang) - 14, oy + rr * math.sin(ang) - 30), 'C',
           font=font(FONT_MATH, 26), fill=BLUE)
    # 奇点
    for x, y, label, where in p['poles']:
        px, py = cx + x * u, cy - y * u
        col = RED if where == 'in' else (150, 150, 150)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=col)
        rich(d, (px, py - 40), label, 24, col, anchor='ma')

for i, p in enumerate(panels):
    x0 = PX[i] + 8
    rich(d, (x0, PY1 + 18), p['title'], 25, DEEP, anchor='la')
    rich(d, (x0, PY1 + 54), p['formula'], 24, INK, anchor='la')
    for j, line in enumerate(p['note']):
        rich(d, (x0, PY1 + 92 + j * 30), line, 22, GREY, anchor='la')

rich(d, (40, PY1 + 178),
     '红点是奇点：落在蓝圈里才算这一项，落在圈外那一项写 0。',
     24, GREY, anchor='la')
rich(d, (40, PY1 + 214),
     '同一个被积函数，换一条围道，圈进去的奇点变了，答案就变了。',
     24, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
