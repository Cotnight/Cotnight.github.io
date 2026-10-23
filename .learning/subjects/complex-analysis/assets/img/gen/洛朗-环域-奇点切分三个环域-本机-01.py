# -*- coding: utf-8 -*-
"""产图脚本：奇点把平面切成三个环域，同一个函数在每个环域里各有一套写法。

左格：f(z) = 1/((z-1)(z-2)) 的两个奇点 1 与 2 落在以原点为心、半径 1 与 2 的圆上。
      这两条圆把复平面切成三块：|z|<1 的圆盘、1<|z|<2 的圆环、|z|>2 的外部，
      每一块内部都没有奇点，所以每一块都能作洛朗展开。
右格：同一块区域里 1/(z-1) 与 1/(z-2) 各写成首项加省略号的形式——
      半径内的那个提 1/(1-w)，半径外的那个提 1/z。

输出：assets/img/pool/洛朗-环域-奇点切分三个环域-本机-01.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '洛朗-环域-奇点切分三个环域-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 780
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
RED = (176, 42, 42)
GREEN = (24, 120, 84)
R1_FILL = (228, 240, 252)
R2_FILL = (253, 242, 228)
R3_FILL = (232, 246, 236)

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


def split_markup(text):
    """把 _{X} 拆成下标、^{X} 拆成上标。"""
    segs = []
    i = 0
    while i < len(text):
        if text.startswith('_{', i) or text.startswith('^{', i):
            j = text.index('}', i)
            segs.append((text[i + 2:j], text[i]))
            i = j + 1
        else:
            nxt = [k for k in (text.find('_{', i), text.find('^{', i)) if k >= 0]
            j = min(nxt) if nxt else len(text)
            segs.append((text[i:j], None))
            i = j
    return segs


def mtext(d, xy, text, size, fill, anchor='la'):
    segs = split_markup(text)
    sub_size = int(round(size * 0.72))
    widths = []
    for s, mark in segs:
        f = font(FONT_MATH, sub_size if mark else size)
        for part, _ in runs(s):
            widths.append(d.textlength(part, font=f))
        if not s:
            widths.append(0.0)
    total = sum(widths)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    k = 0
    for s, mark in segs:
        f = font(FONT_MATH, sub_size if mark else size)
        dy = 0
        if mark == '_':
            dy = size * 0.28
        elif mark == '^':
            dy = -size * 0.30
        first = True
        for part, _ in runs(s):
            d.text((x, y + dy), part, font=f, fill=fill, anchor='l' + anchor[1])
            x += widths[k]
            k += 1
            first = False
        if not s:
            k += 0
    return total


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


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 30), '奇点 1、2 落在两条过原点的圆上，把平面切成三个环域', 30, INK,
     anchor='ma')

# ---------------- 左格：三个环域 ----------------
BOX = (56, 104, 700, 700)
d.rectangle(BOX, outline=FRAME, width=2)
C0 = (378, 408)
U = 105  # 一个单位 = 105 像素
R_A, R_B = U, 2 * U

d.rectangle([BOX[0] + 1, BOX[1] + 1, BOX[2] - 1, BOX[3] - 1], fill=R3_FILL)
d.ellipse([C0[0] - R_B, C0[1] - R_B, C0[0] + R_B, C0[1] + R_B], fill=R2_FILL)
d.ellipse([C0[0] - R_A, C0[1] - R_A, C0[0] + R_A, C0[1] + R_A], fill=R1_FILL)

# 坐标轴
d.line([(BOX[0] + 18, C0[1]), (BOX[2] - 26, C0[1])], fill=GREY, width=2)
arrow_head(d, (BOX[2] - 40, C0[1]), (BOX[2] - 22, C0[1]), GREY)
d.line([(C0[0], BOX[3] - 18), (C0[0], BOX[1] + 26)], fill=GREY, width=2)
arrow_head(d, (C0[0], BOX[1] + 40), (C0[0], BOX[1] + 22), GREY)
rich(d, (BOX[2] - 30, C0[1] + 10), 'x', 25, GREY, anchor='la')
rich(d, (C0[0] + 10, BOX[1] + 30), 'y', 25, GREY, anchor='la')

# 两条分界圆
d.ellipse([C0[0] - R_A, C0[1] - R_A, C0[0] + R_A, C0[1] + R_A],
          outline=BLUE, width=3)
d.ellipse([C0[0] - R_B, C0[1] - R_B, C0[0] + R_B, C0[1] + R_B],
          outline=ORANGE, width=3)

# 区域标号
rich(d, (322, 470), '① |z| < 1', 27, BLUE, anchor='ma')
rich(d, (300, 290), '② 1 < |z| < 2', 27, ORANGE, anchor='ma')
rich(d, (300, 175), '③ |z| > 2', 27, GREEN, anchor='ma')

# 奇点
for k, name in ((1, 'z = 1'), (2, 'z = 2')):
    p = (C0[0] + k * U, C0[1])
    d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=RED)
    rich(d, (p[0], p[1] + 20), name, 25, RED, anchor='ma')

rich(d, ((BOX[0] + BOX[2]) / 2, 660),
     '两条分界圆过奇点：每块区域内部没有奇点，才能展开', 25, GREY, anchor='ma')

# ---------------- 右格：三套写法 ----------------
TB = (730, 104, 1200, 700)
d.rectangle(TB, outline=FRAME, width=2)
rich(d, (TB[0] + 16, TB[1] + 14), 'f = 1/((z − 1)(z − 2))', 26, INK, anchor='la')

blocks = [
    ('① |z| < 1', BLUE, [
        '1/(z − 1) = − (1 + z + z² + …)',
        '1/(z − 2) = − (1/2)(1 + z/2 + z²/4 + …)',
    ], '圆盘里只有非负幂次，是泰勒级数'),
    ('② 1 < |z| < 2', ORANGE, [
        '1/(z − 1) = 1/z + 1/z² + 1/z³ + …',
        '1/(z − 2) = − (1/2)(1 + z/2 + z²/4 + …)',
    ], '靠里的项提 1/z，靠外的项提 1/2'),
    ('③ |z| > 2', GREEN, [
        '1/(z − 1) = 1/z + 1/z² + 1/z³ + …',
        '1/(z − 2) = 1/z + 2/z² + 4/z³ + …',
    ], '两项都提 1/z，只剩负幂次'),
]
y = 168
for title, color, lines, note in blocks:
    rich(d, (TB[0] + 16, y), title, 27, color, anchor='la')
    yy = y + 34
    for ln in lines:
        mtext(d, (TB[0] + 30, yy), ln, 25, INK, anchor='la')
        yy += 30
    rich(d, (TB[0] + 30, yy + 2), note, 25, GREY, anchor='la')
    y = yy + 48

rich(d, (TB[0] + 16, 636),
     '两项相加：负幂还是正幂，由环域定。', 25, INK, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
