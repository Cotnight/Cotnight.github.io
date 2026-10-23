# -*- coding: utf-8 -*-
"""产图脚本：模、辐角主值与共轭。

左栏复平面上画出 z = -1 + √3 i 与它的共轭 z̄：两条斜边等长（模都是 2），
一段圆弧标出逆时针的 θ = 2π/3、另一段标出顺时针的 -2π/3，直角的两个投影标出
实部 x = -1 与虚部 y = √3。右栏是卷面上要写的那几行字。

输出：assets/img/pool/复数运算-模与辐角-主值与共轭-本机-01.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '复数运算-模与辐角-主值与共轭-本机-01.png'))

CJK_FONT = r'C:\Windows\Fonts\msyh.ttc'
MATH_FONT = r'C:\Windows\Fonts\cambria.ttc'
# 微软雅黑缺这些符号（或字形难看），交给 Cambria
MATH_CHARS = set('πθφ√²³⁴∈≥≤≠≈−×∠′Δ∂→∫ωΩ')

W, H = 1240, 760
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (105, 105, 105)
AXIS = (85, 85, 85)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
GREEN = (50, 130, 82)
ORANGE = (196, 92, 24)
PURPLE = (120, 70, 160)

CACHE = {}


def font(path, size):
    key = (path, size)
    if key not in CACHE:
        CACHE[key] = ImageFont.truetype(path, size)
    return CACHE[key]


BAR = '\x01'   # 占位符：画一个带横线的 z（雅黑没有组合上划线 U+0304）


def runs_of(s, size):
    runs = []
    for ch in s:
        path = None if ch == BAR else (MATH_FONT if ch in MATH_CHARS else CJK_FONT)
        if runs and runs[-1][0] == path:
            runs[-1][1] += ch
        else:
            runs.append([path, ch])
    out = []
    for p, t in runs:
        w = font(CJK_FONT, size).getlength('z') if p is None else font(p, size).getlength(t)
        out.append((p, t, w))
    return out


def text(d, x, y, s, size=24, fill=INK, anchor='ls'):
    """混合字体绘制：汉字走雅黑、数学符号走 Cambria；anchor 只支持 l/m/r + s/m。"""
    runs = runs_of(s, size)
    total = sum(r[2] for r in runs)
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    if anchor[1] == 'm':
        y += 0.36 * size
    for p, t, w in runs:
        if p is None:
            d.text((x, y), 'z', font=font(CJK_FONT, size), fill=fill, anchor='ls')
            d.line([(x + 1, y - size * 0.70), (x + w - 1, y - size * 0.70)],
                   fill=fill, width=2)
        else:
            d.text((x, y), t, font=font(p, size), fill=fill, anchor='ls')
        x += w


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)


class Panel:
    def __init__(self, box, xr, yr):
        self.x0, self.y0, self.x1, self.y1 = box
        self.xr, self.yr = xr, yr

    def px(self, x):
        return self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.x1 - self.x0)

    def py(self, y):
        return self.y1 - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.y1 - self.y0)

    def pt(self, x, y):
        return (self.px(x), self.py(y))

    def line(self, pts, color=INK, width=3, dash=None):
        seg = [self.pt(x, y) for x, y in pts]
        if dash is None:
            d.line(seg, fill=color, width=width, joint='curve')
            return
        for (ax, ay), (bx, by) in zip(seg, seg[1:]):
            total = math.hypot(bx - ax, by - ay)
            if total == 0:
                continue
            pos = 0.0
            while pos < total:
                s1 = min(pos + dash, total)
                d.line([(ax + (bx - ax) * pos / total, ay + (by - ay) * pos / total),
                        (ax + (bx - ax) * s1 / total, ay + (by - ay) * s1 / total)],
                       fill=color, width=width)
                pos += dash * 2

    def dot(self, x, y, color=INK, r=8):
        cx, cy = self.pt(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    def arc(self, r, a0, a1, color=INK, width=3, dash=None):
        n = max(8, int(abs(a1 - a0) / 0.04))
        pts = [(r * math.cos(a0 + (a1 - a0) * i / n),
                r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.line(pts, color=color, width=width, dash=dash)

    def axes(self, xlab, ylab):
        self.line([(self.xr[0], 0), (self.xr[1], 0)], color=AXIS, width=2)
        self.line([(0, self.yr[0]), (0, self.yr[1])], color=AXIS, width=2)
        d.text((self.x1 - 6, self.py(0) - 24), xlab, font=font(CJK_FONT, 24),
               fill=GREY, anchor='rs')
        d.text((self.px(0) + 12, self.y0 + 6), ylab, font=font(CJK_FONT, 24),
               fill=GREY, anchor='la')

    def frame(self):
        d.rectangle([self.x0, self.y0, self.x1, self.y1], outline=FRAME, width=2)


P = Panel((96, 120, 700, 660), (-2.7, 2.5), (-2.4, 2.4))
P.frame()
P.axes('x（实轴）', 'y（虚轴）')

r = 2.0
th = 2 * math.pi / 3
zx, zy = r * math.cos(th), r * math.sin(th)          # -1, √3
cmx, cmy = zx, -zy                                   # 共轭 -1, -√3

# 两条斜边
P.line([(0, 0), (zx, zy)], color=BLUE, width=4)
P.line([(0, 0), (cmx, cmy)], color=GREEN, width=4)

# 投影：实部与虚部
P.line([(zx, zy), (zx, 0)], color=GREY, width=2, dash=10)
P.line([(zx, zy), (0, zy)], color=GREY, width=2, dash=10)
text(d, P.px(zx) - 6, P.py(0) + 34, 'x = −1', 24, GREY, anchor='ms')
text(d, P.px(0) - 8, P.py(zy) - 12, 'y = √3', 24, GREY, anchor='rs')

# 两段圆弧
P.arc(0.72, 0, th, color=ORANGE, width=3)
P.arc(0.52, 0, -th, color=GREEN, width=3)
text(d, P.px(1.12 * math.cos(th / 2)), P.py(0.92 * math.sin(th / 2)) - 8,
     'θ = 2π/3', 25, ORANGE, anchor='ms')
text(d, P.px(0.92 * math.cos(-th / 3)), P.py(0.80 * math.sin(-th / 3)) + 30,
     '−2π/3', 25, GREEN, anchor='ms')

# 模的标注
text(d, P.px(-0.62) - 30, P.py(1.02), '|z| = 2', 25, BLUE, anchor='rm')
text(d, P.px(-0.55) - 34, P.py(-0.95), '|' + BAR + '| = 2', 25, GREEN, anchor='rm')

# 两个点
P.dot(zx, zy, BLUE, 9)
P.dot(cmx, cmy, GREEN, 9)
text(d, P.px(zx) - 10, P.py(zy) - 22, 'z = −1 + √3i', 26, BLUE, anchor='rs')
text(d, P.px(cmx) - 10, P.py(cmy) + 42, BAR + ' = −1 − √3i', 26, GREEN, anchor='rs')

# 右栏：卷面上要写的那几行
RX = 748
text(d, RX, 150, '卷面上逐行写出', 27, INK, anchor='ls')
rows = [
    ('实部与虚部', 'x = −1，y = √3'),
    ('模', '|z| = √(x² + y²) = 2'),
    ('辐角主值', 'Arg z = 2π/3'),
    ('全部辐角', 'arg z = 2π/3 + 2kπ'),
    ('共轭', BAR + ' = −1 − √3i'),
    ('共轭的辐角', 'Arg ' + BAR + ' = −2π/3'),
]
y = 196
for label, val in rows:
    text(d, RX, y, label, 23, GREY, anchor='ls')
    text(d, RX + 132, y, val, 24, INK, anchor='ls')
    y += 48

d.rectangle([RX - 16, y + 6, W - 40, y + 150], outline=ORANGE, width=2)
text(d, RX, y + 44, '主值取在 (−π, π] 里：', 23, ORANGE, anchor='ls')
text(d, RX, y + 84, '−1 + √3i 落在第二象限 → 2π/3', 23, INK, anchor='ls')
text(d, RX, y + 122, '它的共轭落在第三象限 → −2π/3', 23, INK, anchor='ls')

text(d, W / 2, H - 30,
     '同一个数的辐角写成一条射线上的两个点：模相同，辐角差一个符号（差 2π 的整数倍）。',
     24, GREY, anchor='ms')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
