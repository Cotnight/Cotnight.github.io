# -*- coding: utf-8 -*-
"""产图脚本：卷面 100 分的分布——填空 15、选择 15、解答题 70 分逐题拆开。

输出：assets/img/pool/绪论-卷面分值分布-解答题九道-本机-01.png
分值取自 sources/hfut-complex-exam-with-answers-文本.md（合肥工大 2022 A 卷）。
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '绪论-卷面分值分布-解答题九道-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 900
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
DEEP = (26, 78, 140)
LIGHT = (219, 232, 246)
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
    return total


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 24), '卷面 100 分：填空 15 分、选择 15 分、解答题 70 分', 29, DEEP, anchor='ma')
rich(d, (W / 2, 66), '逐题分值取自合肥工大 2022 A 卷原文，四套卷的题号与分值基本不变', 23, GREY, anchor='ma')

# ---- 上半：100 分的三段 ----
BAR_X0, BAR_X1 = 100, 1140
BAR_Y0, BAR_Y1 = 118, 182
span = BAR_X1 - BAR_X0
parts = [
    ('填空 3 分 × 5', 15, LIGHT, DEEP),
    ('选择 3 分 × 5', 15, LIGHT, DEEP),
    ('解答题 9 题', 70, BLUE, (255, 255, 255)),
]
x = BAR_X0
for name, val, fill, ink in parts:
    w = span * val / 100.0
    d.rectangle((x, BAR_Y0, x + w, BAR_Y1), fill=fill, outline=(255, 255, 255), width=3)
    rich(d, (x + w / 2, BAR_Y0 + 18), str(val), 30, ink, anchor='ma')
    rich(d, (x + w / 2, BAR_Y1 + 10), name, 22, GREY, anchor='ma')
    x += w

# ---- 下半：解答题九道 ----
rows = [
    ('1', '求 z 的模与辐角', 6, '第 1 章'),
    ('2', '解方程、求方根与 Ln 的值', 6, '第 1 章'),
    ('3', '沿折线或参数曲线积分', 6, '第 2 章'),
    ('4', '沿正向圆周的闭路积分', 10, '第 2 章 / 第 3 章'),
    ('5', '由调和函数求 f(z)', 10, '第 1 章'),
    ('6', '圆环域上的洛朗展开', 10, '第 3 章'),
    ('7', '奇点与相应的留数', 10, '第 3 章'),
    ('8', '用拉氏变换解微分方程', 9, '第 5 章'),
    ('9', '概念简答', 3, '跨章'),
]
top = 236
row_h = 66
NAME_X = 132
BAR_X = 660
BAR_MAX = 300  # 10 分对应的长度
TAG_X = 1078
for i, (num, name, score, chap) in enumerate(rows):
    y = top + i * row_h
    if i % 2 == 0:
        d.rectangle((88, y - 6, 1152, y + row_h - 14), fill=FILL)
    rich(d, (100, y + 8), num, 24, BLUE, anchor='la')
    rich(d, (NAME_X, y + 6), name, 25, INK, anchor='la')
    bw = BAR_MAX * score / 10.0
    d.rounded_rectangle((BAR_X, y + 12, BAR_X + bw, y + 34), radius=5,
                        fill=BLUE if score >= 9 else LIGHT,
                        outline=None if score >= 9 else FRAME, width=1)
    rich(d, (BAR_X + bw + 12, y + 8), str(score) + ' 分',
         24, DEEP if score >= 9 else GREY, anchor='la')
    rich(d, (TAG_X, y + 10), chap, 21, GREY, anchor='la')

rich(d, (W / 2, H - 42),
     '第 4～7 题四道各 10 分，合计 40 分；第 8 题 9 分是同一类套路题，简答只值 3 分但不能空着。',
     24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
