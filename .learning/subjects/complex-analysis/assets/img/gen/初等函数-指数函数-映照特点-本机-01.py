# -*- coding: utf-8 -*-
"""产图脚本：w = e^z 的映照特点（水平带 → 角域，竖直线 → 圆）。

本机没有 matplotlib，所以用 Pillow 逐点算坐标后连线；中文字体取系统 simhei。
输出：assets/img/pool/初等函数-指数函数-映照特点-本机-01.png
用法：<bundled python> -X utf8 -B 本脚本
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '初等函数-指数函数-映照特点-本机-01.png'))
FONT_PATH = r'C:\Windows\Fonts\simhei.ttf'

W, H = 1260, 1170
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (110, 110, 110)
AXIS = (85, 85, 85)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
BLUE_FILL = (228, 239, 251)
ORANGE = (196, 92, 24)
ORANGE_FILL = (252, 236, 223)

CACHE = {}


def font(size):
    if size not in CACHE:
        CACHE[size] = ImageFont.truetype(FONT_PATH, size)
    return CACHE[size]


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)


class Panel:
    """一个带等比坐标的方框面板。"""

    def __init__(self, box, xr, yr):
        self.x0, self.y0, self.x1, self.y1 = box
        self.xr, self.yr = xr, yr

    def px(self, x):
        return self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.x1 - self.x0)

    def py(self, y):
        return self.y1 - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.y1 - self.y0)

    def pt(self, x, y):
        return (self.px(x), self.py(y))

    def poly(self, pts, fill):
        d.polygon([self.pt(x, y) for x, y in pts], fill=fill)

    def line(self, pts, color=INK, width=3):
        d.line([self.pt(x, y) for x, y in pts], fill=color, width=width, joint='curve')

    def dot(self, x, y, color=INK, r=7):
        cx, cy = self.pt(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    def frame(self):
        d.rectangle([self.x0, self.y0, self.x1, self.y1], outline=FRAME, width=2)

    def axes(self, xlab, ylab):
        self.line([(self.xr[0], 0), (self.xr[1], 0)], color=AXIS, width=2)
        self.line([(0, self.yr[0]), (0, self.yr[1])], color=AXIS, width=2)
        d.text((self.x1 - 6, self.py(0) - 22), xlab, font=font(26), fill=GREY, anchor='rs')
        d.text((self.px(0) + 10, self.y0 + 4), ylab, font=font(26), fill=GREY, anchor='la')


def title(cx, y, s, size=31):
    d.text((cx, y), s, font=font(size), fill=INK, anchor='mm')


def arrow(x0, x1, y, label):
    d.line([(x0, y), (x1 - 16, y)], fill=GREY, width=4)
    d.polygon([(x1, y), (x1 - 22, y - 11), (x1 - 22, y + 11)], fill=GREY)
    d.text(((x0 + x1) / 2, y - 34), label, font=font(28), fill=GREY, anchor='mm')


P1 = Panel((70, 90, 530, 550), (-3.2, 3.2), (-1.0, 5.4))
P2 = Panel((730, 90, 1190, 550), (-3.2, 3.2), (-3.2, 3.2))
P3 = Panel((70, 650, 530, 1110), (-2.7, 2.7), (-2.7, 2.7))
P4 = Panel((730, 650, 1190, 1110), (-2.7, 2.7), (-2.7, 2.7))

for p in (P1, P2, P3, P4):
    p.frame()

# ① z 平面上的水平带 0 < y < π：带内几条水平线
P1.poly([(P1.xr[0], 0), (P1.xr[1], 0), (P1.xr[1], math.pi), (P1.xr[0], math.pi)], BLUE_FILL)
P1.axes('x', 'y')
for k, name in enumerate(['π/4', 'π/2', '3π/4']):
    y0 = (k + 1) * math.pi / 4
    P1.line([(P1.xr[0], y0), (P1.xr[1], y0)], color=BLUE, width=3)
    px, py = P1.pt(P1.xr[0] + 0.25, y0)
    d.text((px, py - 18), 'y = ' + name, font=font(25), fill=BLUE, anchor='la')
for yv, lab in ((0.0, '0'), (math.pi, 'π')):
    px, py = P1.pt(-0.18, yv)
    d.text((px, py), lab, font=font(25), fill=GREY, anchor='rm')
title(300, 58, '①  z 平面：水平带 0 < y < π')

# ② w 平面上的上半平面：带内几条射线
P2.poly([(P2.xr[0], 0), (P2.xr[1], 0), (P2.xr[1], P2.yr[1]), (P2.xr[0], P2.yr[1])], BLUE_FILL)
P2.axes('u', 'v')
for k, name in enumerate(['π/4', 'π/2', '3π/4']):
    th = (k + 1) * math.pi / 4
    P2.line([(0, 0), (3.1 * math.cos(th), 3.1 * math.sin(th))], color=BLUE, width=3)
title(960, 58, '②  w 平面：上半平面')

# ③ z 平面上的竖直线 x = 0.5
P3.axes('x', 'y')
P3.line([(0.5, P3.yr[0]), (0.5, P3.yr[1])], color=ORANGE, width=4)
px, py = P3.pt(0.5, 2.35)
d.text((px + 12, py), 'x = 0.5', font=font(26), fill=ORANGE, anchor='lm')
px, py = P3.pt(-0.14, 0)
d.text((px, py - 20), '0', font=font(25), fill=GREY, anchor='rm')
title(300, 618, '③  z 平面：竖直线 x = 0.5')

# ④ w 平面上的圆 |w| = e^{0.5}
P4.axes('u', 'v')
r = math.exp(0.5)
box = [P4.px(-r), P4.py(r), P4.px(r), P4.py(-r)]
d.ellipse(box, outline=ORANGE, width=4)
P4.dot(r, 0.0, ORANGE)
d.text((P4.px(0), P4.py(-2.35)), '圆 |w| = e^0.5 ≈ 1.65',
       font=font(26), fill=ORANGE, anchor='mm')
title(960, 618, '④  w 平面：圆 |w| = e^0.5')

arrow(553, 706, 320, 'w = e^z')
arrow(553, 706, 880, 'w = e^z')

for cx, y, s in (
        (300, 580, '水平带  →  角域'),
        (960, 580, '水平线  →  射线（辐角 = 虚部 y）'),
        (300, 1140, '竖直线  →  圆'),
        (960, 1140, '半径 = e^c，c 是竖直线到虚轴的距离')):
    d.text((cx, y), s, font=font(24), fill=GREY, anchor='mm')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
