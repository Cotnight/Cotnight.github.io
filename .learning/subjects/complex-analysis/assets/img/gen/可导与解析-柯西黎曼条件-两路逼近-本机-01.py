# -*- coding: utf-8 -*-
"""产图脚本：沿两条不同方向逼近，导数只能有一个值，由此得到柯西-黎曼条件。

左边是 z 平面上的 z0 与两条逼近方向；右边两个框分别是两条路的差商与算出的导数；
底部横条是合并后得到的两个方程。

输出：assets/img/pool/可导与解析-柯西黎曼条件-两路逼近-本机-01.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '可导与解析-柯西黎曼条件-两路逼近-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 700
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
AXIS = (80, 80, 80)
GRID = (235, 235, 235)
FRAME = (200, 200, 200)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
BAND = (240, 246, 252)
BAND_EDGE = (176, 205, 232)

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
    """中英混排：中文用雅黑、数学符号用 Cambria，按总宽度对齐。"""
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

# ---------- 左：z 平面与两条逼近方向 ----------
X0, Y0, X1, Y1 = 70, 70, 470, 400
d.rectangle((X0, Y0, X1, Y1), outline=FRAME, width=2)
for g in range(1, 10):
    gx = X0 + (X1 - X0) * g / 10
    gy = Y0 + (Y1 - Y0) * g / 10
    d.line([(gx, Y0), (gx, Y1)], fill=GRID, width=1)
    d.line([(X0, gy), (X1, gy)], fill=GRID, width=1)

cx, cy = 270, 245
d.line([(X0 + 8, cy), (X1 - 14, cy)], fill=AXIS, width=2)
d.line([(cx, Y1 - 8), (cx, Y0 + 14)], fill=AXIS, width=2)
rich(d, (X1 - 26, cy + 8), 'x', 24, AXIS, anchor='la')
rich(d, (cx + 8, Y0 + 8), 'y', 24, AXIS, anchor='la')

d.line([(cx - 118, cy), (cx - 12, cy)], fill=BLUE, width=4)
d.polygon([(cx - 10, cy), (cx - 26, cy - 8), (cx - 26, cy + 8)], fill=BLUE)
rich(d, (cx - 122, cy - 40), 'Δz = Δx', 26, BLUE, anchor='la')

d.line([(cx, cy + 118), (cx, cy + 12)], fill=ORANGE, width=4)
d.polygon([(cx, cy + 10), (cx - 8, cy + 26), (cx + 8, cy + 26)], fill=ORANGE)
rich(d, (cx + 18, cy + 100), 'Δz = iΔy', 26, ORANGE, anchor='la')

d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=INK)
rich(d, (cx + 20, cy - 44), 'z₀', 28, INK, anchor='la')

# ---------- 右：两条路的差商与导数 ----------
BX0, BX1 = 540, 1190


def box(y0, y1, title, quotient, formula, color):
    d.rounded_rectangle((BX0, y0, BX1, y1), radius=10, outline=color, width=3)
    rich(d, (BX0 + 24, y0 + 16), title, 26, color, anchor='la')
    rich(d, (BX0 + 24, y0 + 60), quotient, 26, GREY, anchor='la')
    rich(d, (BX0 + 24, y0 + 106), formula, 32, INK, anchor='la')


box(70, 220, '沿水平方向逼近', '[ f(z₀+Δx) − f(z₀) ] / Δx  →',
    'f′(z₀) = ∂u/∂x + i ∂v/∂x', BLUE)
box(250, 400, '沿竖直方向逼近', '[ f(z₀+iΔy) − f(z₀) ] / ( iΔy )  →',
    'f′(z₀) = ∂v/∂y − i ∂u/∂y', ORANGE)

d.line([(865, 400), (865, 432)], fill=GREY, width=3)
d.polygon([(865, 442), (857, 426), (873, 426)], fill=GREY)
rich(d, (880, 406), '两条路必须相等', 25, GREY, anchor='la')

# ---------- 底部：柯西-黎曼条件 ----------
d.rounded_rectangle((70, 452, 1190, 594), radius=12, fill=BAND, outline=BAND_EDGE, width=3)
rich(d, (630, 470), '分离实部与虚部，得到柯西-黎曼条件', 26, GREY, anchor='ma')
rich(d, (630, 518), '∂u/∂x = ∂v/∂y ，   ∂u/∂y = − ∂v/∂x', 40, INK, anchor='ma')

rich(d, (W / 2, 640),
     '同一点上，两条路算出的必须是同一个数：这一条把实部与虚部绑在一起。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
