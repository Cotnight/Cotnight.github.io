# -*- coding: utf-8 -*-
"""产图脚本：由调和函数求解析函数 f(z) 的四步，也是 10 分大题的给分顺序。

输出：assets/img/pool/可导与解析-解析性判定-求fz四步-本机-02.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '可导与解析-解析性判定-求fz四步-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 880
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
DEEP = (26, 78, 140)
FILL = (245, 249, 254)

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

rich(d, (W / 2, 26), '题给含参数的 u(x,y) 或 v(x,y)：四步求出 f(z)', 28, DEEP, anchor='ma')
rich(d, (W / 2, 70), '2022～2025 各套卷的 10 分题都按这四步给分', 24, GREY, anchor='ma')

BX0, BX1 = 110, 1140
steps = [
    ('1', '验调和、定参数',
     ['∂²u/∂x² + ∂²u/∂y² = 0 对一切 x、y 成立',
      '按 x、y 的系数逐项比较，解出 a（或 a、b）']),
    ('2', '写导数、整理成 z',
     ['u 给出时：f′(z) = ∂u/∂x − i ∂u/∂y    v 给出时：f′(z) = ∂v/∂y + i ∂v/∂x',
      '把 x 与 iy 的系数拼成一个 z = x + iy，这一步是给分点']),
    ('3', '积分、补常数',
     ['f(z) = ∫ f′(z) dz + C',
      'C 取实常数：u、v 都是实值函数，常数里不能带 i']),
    ('4', '定常数、取分量',
     ['代入题给条件（f(0)=0、f(2)=i 之类）定出 C',
      '题问 u 或 v，就取 f 的实部或虚部，并回代核对']),
]
top = 116
box_h = 150
gap = 30
for i, (num, title, lines) in enumerate(steps):
    y0 = top + i * (box_h + gap)
    y1 = y0 + box_h
    d.rounded_rectangle((BX0, y0, BX1, y1), radius=12, fill=FILL, outline=FRAME, width=2)
    d.ellipse([BX0 + 22, y0 + 42, BX0 + 78, y0 + 98], fill=BLUE)
    rich(d, (BX0 + 50, y0 + 55), num, 30, (255, 255, 255), anchor='ma')
    rich(d, (BX0 + 100, y0 + 26), title, 29, DEEP, anchor='la')
    rich(d, (BX0 + 100, y0 + 74), lines[0], 25, INK, anchor='la')
    rich(d, (BX0 + 100, y0 + 110), lines[1], 25, GREY, anchor='la')
    if i < len(steps) - 1:
        ay = y1 + 6
        d.line([(BX0 + 50, ay), (BX0 + 50, ay + gap - 14)], fill=FRAME, width=3)
        d.polygon([(BX0 + 50, ay + gap - 6), (BX0 + 43, ay + gap - 18),
                   (BX0 + 57, ay + gap - 18)], fill=FRAME)

rich(d, (W / 2, H - 46),
     '第 2 步与第 4 步最容易丢分：导数不合并成 z、常数漏掉或取成复数。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
