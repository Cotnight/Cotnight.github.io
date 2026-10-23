# -*- coding: utf-8 -*-
"""产图脚本：五章主线与各章主考的题型、分值量级。

输出：assets/img/pool/绪论-五章主线-题型地图-本机-02.png
分值量级按 sources/ 下四套合肥工大卷的逐题分值估。
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '绪论-五章主线-题型地图-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 920
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
    return total


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 22), '五章主线：各章在卷面上主考哪些题', 29, DEEP, anchor='ma')
rich(d, (W / 2, 64), '教材按李君版五章排；分值量级按四套公开卷的逐题分值估', 23, GREY, anchor='ma')

chapters = [
    ('第 1 章', '复变函数与解析函数',
     '四则与初等函数、判解析、由调和函数求 f(z)',
     '解答 1、2、5；填空与选择各 2～3 处',
     '约 38 分'),
    ('第 2 章', '复变函数的积分',
     '参数化算积分、柯西定理、柯西公式与高阶导数',
     '解答 3、4；填空与选择各一处',
     '约 20 分'),
    ('第 3 章', '级数与留数',
     '收敛半径、洛朗展开、奇点分类、留数定理',
     '解答 6、7；第 4 题也可走留数',
     '约 26 分'),
    ('第 4 章', '傅里叶变换',
     '傅里叶级数与频谱、变换的定义与性质、查附录 B',
     '填空与选择各一处，不出大题',
     '3～9 分'),
    ('第 5 章', '拉普拉斯变换',
     '查表求正变换、部分分式求逆变换、解微分方程',
     '解答 8 与填空一处',
     '9～13 分'),
]

BOX_X0, BOX_X1 = 76, 1164
BOX_H = 122
GAP = 36
TOP = 116
links = [
    '解析是积分公式的成立条件',
    '会算积分才轮得到展开与留数',
    '级数取极限得到频谱与变换',
    '乘上衰减因子成为拉氏变换',
]
for i, (num, name, what, where, score) in enumerate(chapters):
    y0 = TOP + i * (BOX_H + GAP)
    y1 = y0 + BOX_H
    d.rounded_rectangle((BOX_X0, y0, BOX_X1, y1), radius=12, fill=FILL, outline=FRAME, width=2)
    d.rounded_rectangle((BOX_X0 + 18, y0 + 22, BOX_X0 + 118, y0 + 62), radius=8, fill=BLUE)
    rich(d, (BOX_X0 + 68, y0 + 30), num, 22, (255, 255, 255), anchor='ma')
    rich(d, (BOX_X0 + 140, y0 + 16), name, 27, DEEP, anchor='la')
    rich(d, (BOX_X0 + 140, y0 + 58), what, 22, INK, anchor='la')
    rich(d, (BOX_X0 + 140, y0 + 88), '卷面：' + where, 21, GREY, anchor='la')
    rich(d, (BOX_X1 - 26, y0 + 26), score, 28, BLUE, anchor='ra')
    rich(d, (BOX_X1 - 26, y0 + 72), '合计分值', 19, GREY, anchor='ra')
    if i < len(chapters) - 1:
        ay = y1 + 4
        d.line([(BOX_X0 + 68, ay), (BOX_X0 + 68, ay + GAP - 12)], fill=FRAME, width=3)
        d.polygon([(BOX_X0 + 68, ay + GAP - 4), (BOX_X0 + 61, ay + GAP - 16),
                   (BOX_X0 + 75, ay + GAP - 16)], fill=FRAME)
        rich(d, (BOX_X0 + 92, ay + 6), links[i], 20, GREY, anchor='la')

rich(d, (W / 2, H - 40),
     '五章的顺序就是解题顺序：先判解析，再算积分，最后展开与变换。',
     24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
