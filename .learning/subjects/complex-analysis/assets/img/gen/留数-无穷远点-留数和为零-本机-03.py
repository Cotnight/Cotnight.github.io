# -*- coding: utf-8 -*-
"""产图脚本：无穷远点的留数，以及全平面留数和为零带来的圈内圈外互算。

输出：assets/img/pool/留数-无穷远点-留数和为零-本机-03.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '留数-无穷远点-留数和为零-本机-03.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 720
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (205, 205, 205)
AXIS = (222, 226, 232)
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

rich(d, (60, 20), '无穷远点的留数：把它算进来，全部留数之和就是零', 30, DEEP, anchor='la')
rich(d, (60, 64), '于是圈内的和可以由圈外的和取负号读出；算完的留数表也能用它核对', 22, GREY,
     anchor='la')

# 左：复平面
d.rounded_rectangle((60, 104, 470, 656), radius=14, fill=BG, outline=FRAME, width=2)
cx, cy, scale = 240, 390, 40.0
d.line([(cx - 150, cy), (cx + 190, cy)], fill=AXIS, width=2)
d.line([(cx, cy - 250), (cx, cy + 220)], fill=AXIS, width=2)
R = 2 * scale
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=BLUE, width=3)
rich(d, (cx, cy - R - 34), 'C：|z| = 2', 20, BLUE, anchor='ma')
# 圈内：二阶极点 0
d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=BLUE)
rich(d, (cx, cy + 18), '0（二阶极点）', 20, INK, anchor='ma')
# 圈外：一阶极点 3
px = cx + 3 * scale
d.ellipse([px - 8, cy - 8, px + 8, cy + 8], fill=BLUE)
rich(d, (px, cy - 36), '3（一阶极点）', 20, INK, anchor='ma')
# 圈外：无穷远点
mx, my, mr = cx + 152, cy - 152, 26
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=DEEP, width=3)
rich(d, (mx, my - 16), '∞', 26, DEEP, anchor='ma')
# 从围道到 ∞ 的虚线
x0, y0 = cx + R * 0.707, cy - R * 0.707
x1, y1 = mx - mr * 0.72, my + mr * 0.72
steps = 7
for i in range(steps):
    t0 = i / steps
    t1 = t0 + 0.55 / steps
    d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
            (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)], fill=DEEP, width=2)
rich(d, (mx - mr - 12, my - 16), '圈外只剩 ∞', 20, DEEP, anchor='ra')
rich(d, (cx, 604), '围道把 0 圈在圈内，3 与 ∞ 留在圈外', 21, GREY, anchor='ma')
rich(d, (cx, 632), '圈内那一个留数，也能由圈外的两个留数读出', 21, GREY, anchor='ma')

# 右：三块文字
BX0, BX1 = 500, 1180

d.rounded_rectangle((BX0, 104, BX1, 262), radius=12, fill=FILL,
                    outline=FRAME, width=2)
rich(d, (BX0 + 24, 118), '无穷远点的留数', 24, DEEP, anchor='la')
rich(d, (BX0 + 24, 156), 'Res[f, ∞] = −c₋₁', 26, INK, anchor='la')
rich(d, (BX0 + 24, 200), 'c₋₁ 取自 f 在 |z| > R 内的展开里 1/z 的系数，负号来自绕行方向',
     21, GREY, anchor='la')
rich(d, (BX0 + 24, 230), '有理函数：分母次数比分子次数至少高二次时，Res[f, ∞] = 0',
     21, GREY, anchor='la')

d.rounded_rectangle((BX0, 278, BX1, 448), radius=12, fill=FILL,
                    outline=FRAME, width=2)
rich(d, (BX0 + 24, 292), '全平面留数和为零', 24, DEEP, anchor='la')
rich(d, (BX0 + 24, 330), 'Σ 全部留数（含 ∞ 的）= 0', 26, INK, anchor='la')
rich(d, (BX0 + 24, 374), '圈内之和 = −（圈外之和）', 22, INK, anchor='la')
rich(d, (BX0 + 24, 406), '沿 |z| = R 的正向积分 = −2πi × 圈外留数之和', 22, INK,
     anchor='la')

d.rounded_rectangle((BX0, 464, BX1, 656), radius=12, fill=WARMFILL,
                    outline=WARMEDGE, width=2)
rich(d, (BX0 + 24, 478), '算例　f(z) = 1/(z²(z−3))，C：|z| = 2', 22, WARMINK,
     anchor='la')
rich(d, (BX0 + 24, 514), '圈内：Res[f, 0] = −1/9 → 积分 −2πi/9', 21, INK,
     anchor='la')
rich(d, (BX0 + 24, 548), '圈外：Res[f, 3] = 1/9，Res[f, ∞] = 0', 21, INK,
     anchor='la')
rich(d, (BX0 + 24, 582), '取负号乘 2πi：−2πi × 1/9 = −2πi/9', 21, INK, anchor='la')
rich(d, (BX0 + 24, 616), '两条路给出同一个数，这就是核对的做法', 21, GREY,
     anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
