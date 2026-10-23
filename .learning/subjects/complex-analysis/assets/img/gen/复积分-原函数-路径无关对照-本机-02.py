# -*- coding: utf-8 -*-
"""产图脚本：同一对端点，被积函数解析时三条路同一答案；含 z̄ 时换一条路答案就变。

左格：∫(z + 2)dz 从 0 到 3 + i，沿直线、沿实轴折、沿虚轴折，三条路都得 10 + 5i。
右格：∫z̄ dz 从 0 到 1 + i，沿直线段得 1，先到 1 再竖直上去得 1 + i。

输出：assets/img/pool/复积分-原函数-路径无关对照-本机-02.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '复积分-原函数-路径无关对照-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 700
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
AXIS = (80, 80, 80)
GRID = (236, 236, 236)
FRAME = (200, 200, 200)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
GREEN = (24, 120, 84)

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


def arrow(d, p0, p1, color, width=4, head=12):
    d.line([p0, p1], fill=color, width=width)
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    n = max((dx * dx + dy * dy) ** 0.5, 1e-9)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    d.polygon([(x1, y1),
               (x1 - ux * head * 1.6 + px * head * 0.7,
                y1 - uy * head * 1.6 + py * head * 0.7),
               (x1 - ux * head * 1.6 - px * head * 0.7,
                y1 - uy * head * 1.6 - py * head * 0.7)], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)


def panel(box, ox, oy, unit, steps, title, title_color, foot):
    """一格复平面：box 外框、原点 (ox, oy)、每单位 unit 像素；steps 是折线（像素点列表）。"""
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=FRAME, width=2)
    for k in range(1, 6):
        gx = ox + unit * k
        if gx < x1 - 6:
            d.line([(gx, y0 + 6), (gx, y1 - 6)], fill=GRID, width=1)
        gy = oy - unit * k
        if gy > y0 + 6:
            d.line([(x0 + 6, gy), (x1 - 6, gy)], fill=GRID, width=1)
    d.line([(x0 + 10, oy), (x1 - 12, oy)], fill=AXIS, width=2)
    d.line([(ox, y1 - 10), (ox, y0 + 12)], fill=AXIS, width=2)
    rich(d, (x0 + unit + 30, y0 + 10), title, 26, title_color, anchor='la')
    rich(d, (x1 - 26, oy + 8), 'x', 23, AXIS, anchor='la')
    rich(d, (ox + 8, y0 + 40), 'y', 23, AXIS, anchor='la')
    for pts, color in steps:
        for a, b in zip(pts, pts[1:]):
            arrow(d, a, b, color, width=4)
    rich(d, ((x0 + x1) / 2, y1 - 50), foot, 26, INK, anchor='ma')


def dot(p):
    d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=INK)


# ---------- 左格：z + 2 ----------
A_BOX = (40, 86, 606, 594)
AX, AY, AU = 152, 496, 100
a_0 = (AX, AY)
a_3 = (AX + 3 * AU, AY)
a_3i = (AX + 3 * AU, AY - AU)

panel(A_BOX, AX, AY, AU,
      [([(a_0[0] + 2, a_0[1] - 2), (a_3i[0] - 5, a_3i[1] + 5)], BLUE),
       ([a_0, a_3, a_3i], GREEN),
       ([a_0, (AX, a_3i[1]), a_3i], ORANGE)],
      'z + 2 解析：三条路的答案相同', BLUE,
      '∫(z + 2) dz = 10 + 5i')

for p in (a_0, a_3, a_3i):
    dot(p)
rich(d, (a_0[0] + 4, a_0[1] + 10), '0', 24, INK, anchor='la')
rich(d, (a_3[0] - 6, a_3[1] + 12), '3', 24, INK, anchor='la')
rich(d, (AX - 26, a_3i[1] - 10), 'i', 24, INK, anchor='la')
rich(d, (a_3i[0] + 14, a_3i[1] - 8), '3 + i', 24, INK, anchor='la')
rich(d, (a_3i[0] - 152, a_3i[1] - 38), '路①', 24, BLUE, anchor='la')
rich(d, (a_3[0] - 108, a_3[1] - 40), '路②', 24, GREEN, anchor='la')
rich(d, (AX + 18, a_3i[1] - 38), '路③', 24, ORANGE, anchor='la')

# ---------- 右格：z̄ ----------
B_BOX = (636, 86, 1200, 594)
BX, BY, BU = 748, 496, 148
b_0 = (BX, BY)
b_1 = (BX + BU, BY)
b_1i = (BX + BU, BY - BU)

panel(B_BOX, BX, BY, BU,
      [([(b_0[0] + 2, b_0[1] - 2), (b_1i[0] - 5, b_1i[1] + 5)], BLUE),
       ([b_0, b_1, b_1i], ORANGE)],
      'z̄ 不解析：两条路的答案不同', ORANGE,
      '直线段得 1 ，折线得 1 + i')

for p in (b_0, b_1, b_1i):
    dot(p)
rich(d, (b_0[0] + 4, b_0[1] + 10), '0', 24, INK, anchor='la')
rich(d, (b_1[0] - 6, b_1[1] + 12), '1', 24, INK, anchor='la')
rich(d, (b_1i[0] + 14, b_1i[1] - 8), '1 + i', 24, INK, anchor='la')
rich(d, (b_1i[0] - 118, b_1i[1] - 46), '路①', 24, BLUE, anchor='la')
rich(d, (b_1[0] - 118, b_1[1] + 14), '路②', 24, ORANGE, anchor='la')

rich(d, (W / 2, 630),
     '被积函数在区域内解析，结果只由端点定；含 z̄、Re z、Im z 的不解析，换一条路答案就变。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
