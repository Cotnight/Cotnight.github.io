# -*- coding: utf-8 -*-
"""产图脚本：分母含 (z-z0)^m 的闭路积分怎么套公式——四步流程与两个分支。

输出：assets/img/pool/柯西积分公式-四步套公式-本机-01.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '柯西积分公式-四步套公式-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 930
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
DEEP = (26, 78, 140)
FILL = (245, 249, 254)
WARMFILL = (255, 249, 243)
WARMEDGE = (219, 186, 160)
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


def arrow_right(d, x0, x1, y, color=FRAME, width=3):
    d.line([(x0, y), (x1 - 12, y)], fill=color, width=width)
    d.polygon([(x1, y), (x1 - 14, y - 7), (x1 - 14, y + 7)], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (60, 24), '分母含 (z − z₀) 的闭路积分：四步套公式', 30, DEEP, anchor='la')
rich(d, (60, 68), '每一步只看一件事；四步走完，答案只剩乘 2πi', 24, GREY, anchor='la')

BX0, BX1 = 60, 660
RX0, RX1 = 690, 1180
top, box_h, gap = 116, 142, 34

steps = [
    ('1', '找奇点',
     ['分母 = 0 的根就是奇点，记 z₀',
      '分母因式有几个，奇点就有几个']),
    ('2', '看 z₀ 在围道 C 内还是外',
     ['正向围道逆时针；比较 |z₀ − a| 与 r',
      '在 C 外：这一项直接写 0（见右）']),
    ('3', '凑成标准形式',
     ['写成 g(z) / (z − z₀)^m，g 在 C 内解析',
      '分子含 (z − z₀) 的先约掉，再数 m']),
    ('4', '按幂次 m 套公式',
     ['m = 1：2πi · g(z₀)',
      'm ≥ 2：2πi/(m−1)! · g 的 (m−1) 阶导']),
]

for i, (num, title, lines) in enumerate(steps):
    y0 = top + i * (box_h + gap)
    y1 = y0 + box_h
    d.rounded_rectangle((BX0, y0, BX1, y1), radius=12, fill=FILL,
                        outline=FRAME, width=2)
    d.ellipse([BX0 + 20, y0 + 44, BX0 + 76, y0 + 100], fill=BLUE)
    rich(d, (BX0 + 48, y0 + 57), num, 30, (255, 255, 255), anchor='ma')
    rich(d, (BX0 + 96, y0 + 22), title, 28, DEEP, anchor='la')
    rich(d, (BX0 + 96, y0 + 72), lines[0], 24, INK, anchor='la')
    rich(d, (BX0 + 96, y0 + 108), lines[1], 24, GREY, anchor='la')
    if i < len(steps) - 1:
        ay = y1 + 5
        d.line([(BX0 + 48, ay), (BX0 + 48, ay + gap - 14)], fill=FRAME, width=3)
        d.polygon([(BX0 + 48, ay + gap - 5), (BX0 + 41, ay + gap - 17),
                   (BX0 + 55, ay + gap - 17)], fill=FRAME)

# 分支一：z0 在围道外
y0 = top + 1 * (box_h + gap)
y1 = y0 + box_h
d.rounded_rectangle((RX0, y0, RX1, y1), radius=12, fill=WARMFILL,
                    outline=WARMEDGE, width=2)
rich(d, (RX0 + 26, y0 + 20), '在围道外：整项为 0', 26, WARMINK, anchor='la')
rich(d, (RX0 + 26, y0 + 62), 'z₀ 不在 C 内，柯西公式不适用', 23, INK, anchor='la')
rich(d, (RX0 + 26, y0 + 100), '这一项写成 0，不参与相加', 23, GREY, anchor='la')
arrow_right(d, BX1 + 4, RX0 - 6, (y0 + y1) // 2)

# 分支二：按幂次选公式
y0 = top + 3 * (box_h + gap)
y1 = y0 + box_h
d.rounded_rectangle((RX0, y0, RX1, y1), radius=12, fill=WARMFILL,
                    outline=WARMEDGE, width=2)
rich(d, (RX0 + 26, y0 + 12), '幂次 m 决定求几阶导', 25, WARMINK, anchor='la')
rich(d, (RX0 + 26, y0 + 52), 'm = 1：2πi · g(z₀)', 22, INK, anchor='la')
rich(d, (RX0 + 26, y0 + 82), 'm ≥ 2：2πi/(m−1)! ×', 22, INK, anchor='la')
rich(d, (RX0 + 26, y0 + 112), 'g 在 z₀ 的 (m−1) 阶导数值', 22, INK, anchor='la')
arrow_right(d, BX1 + 4, RX0 - 6, (y0 + y1) // 2)

rich(d, (60, H - 56),
     '围道内有几个奇点，就按四步各走一遍再加起来；圈内一个奇点也没有，积分就是 0。',
     25, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
