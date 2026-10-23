# -*- coding: utf-8 -*-
"""产图脚本：留数的四条算法与适用条件（选型卡）。

输出：assets/img/pool/留数-四种算法-选型-本机-01.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '留数-四种算法-选型-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 990
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


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (60, 22), '留数的四条算法：先定奇点与阶，再选规则', 30, DEEP, anchor='la')
rich(d, (60, 66), '四种算法各有适用条件，选错规则算出来的数不是留数', 23, GREY, anchor='la')

# 第 1 步：定奇点与阶
d.rounded_rectangle((60, 108, 1180, 218), radius=12, fill=FILL,
                    outline=FRAME, width=2)
rich(d, (84, 122), '第 1 步 · 定奇点与阶（上一课已练）', 25, DEEP, anchor='la')
rich(d, (84, 158), '分母为零的有限点：分母零点的阶就是极点的阶，分子先约掉同阶零点',
     23, INK, anchor='la')
rich(d, (84, 190), '分完类，从上到下选一行；四行之间的公式互不通用', 22, GREY, anchor='la')

rows = [
    ('可去奇点', '展开没有负幂项',
     ['留数直接写 0', '不必套公式，也不必求极限'],
     ['sin z / z 在 z₀ = 0', '可去奇点，留数 0']),
    ('一阶极点', '分母的一阶零点',
     ['Res = lim (z − z₀) f(z)（z → z₀）', '分式：P(z₀) / Q′(z₀)'],
     ['tan z 在 π/2 → −1', '(z² − π²)/(z sin z) 在 2π → 3π/2']),
    ('m 阶极点', '分母的 m 重零点',
     ['Res = 1/(m−1)! × 第 (m−1) 阶导', '对 (z − z₀)ᵐf(z) 求导，再代 z₀'],
     ['1/((z+1)(z+2)²) 在 −2 → −1', 'exp(z)/(z−1)³ 在 1 → e/2']),
    ('本性奇点', '负幂项无穷多',
     ['展开成洛朗级数，取 1/(z − z₀) 的系数', '极限式在这里不收敛，用不上'],
     ['exp(1/z) 在 0 → 1', 'z²exp(1/z) 在 0 → 1/6']),
]

top, row_h, gap = 238, 152, 12
COL_TYPE = (60, 296)
COL_RULE = (312, 812)
COL_EX = (828, 1180)

for i, (name, note, rule, ex) in enumerate(rows):
    y0 = top + i * (row_h + gap)
    y1 = y0 + row_h
    d.rounded_rectangle((60, y0, 1180, y1), radius=12, fill=BG,
                        outline=FRAME, width=2)
    d.rounded_rectangle((COL_TYPE[0] + 8, y0 + 10, COL_TYPE[1] - 6, y1 - 10),
                        radius=10, fill=FILL)
    rich(d, (COL_TYPE[0] + 26, y0 + 34), name, 27, DEEP, anchor='la')
    rich(d, (COL_TYPE[0] + 26, y0 + 84), note, 21, GREY, anchor='la')
    rich(d, (COL_TYPE[0] + 26, y0 + 114), '第 %d 条' % (i + 1), 20, BLUE,
         anchor='la')
    rich(d, (COL_RULE[0], y0 + 34), rule[0], 24, INK, anchor='la')
    rich(d, (COL_RULE[0], y0 + 80), rule[1], 22, GREY, anchor='la')
    d.line([(COL_EX[0] - 16, y0 + 16), (COL_EX[0] - 16, y1 - 16)],
           fill=FRAME, width=2)
    rich(d, (COL_EX[0], y0 + 30), '卷面例', 20, WARMINK, anchor='la')
    rich(d, (COL_EX[0], y0 + 66), ex[0], 21, INK, anchor='la')
    rich(d, (COL_EX[0], y0 + 104), ex[1], 21, INK, anchor='la')

rich(d, (60, H - 54),
     '第 2 步在四行里选一行，第 3 步把数算出来，第 4 步求和乘 2πi。',
     23, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
