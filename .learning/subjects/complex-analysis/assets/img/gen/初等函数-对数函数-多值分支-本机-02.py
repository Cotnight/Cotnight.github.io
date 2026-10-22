# -*- coding: utf-8 -*-
"""产图脚本：Ln z 的多值性与主值。

左栏 z 平面上取一个点 z0，右栏 w 平面上把它全部的对数值竖着排出来（相邻两个相差 2πi），
并用浅色带圈出主值所在的那一支（-π < Im w < π）。

输出：assets/img/pool/初等函数-对数函数-多值分支-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '初等函数-对数函数-多值分支-本机-02.png'))
FONT_PATH = r'C:\Windows\Fonts\simhei.ttf'

W, H = 1200, 800
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (105, 105, 105)
AXIS = (85, 85, 85)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
GREEN = (50, 130, 82)
GREEN_FILL = (234, 245, 236)
ORANGE = (196, 92, 24)
BROWN = (170, 70, 70)

CACHE = {}


def font(size):
    if size not in CACHE:
        CACHE[size] = ImageFont.truetype(FONT_PATH, size)
    return CACHE[size]


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
            steps = max(1, int(total // (dash * 2)))
            for i in range(steps + 1):
                s0 = i * 2 * dash
                s1 = min(s0 + dash, total)
                if s0 >= total:
                    break
                d.line([(ax + (bx - ax) * s0 / total, ay + (by - ay) * s0 / total),
                        (ax + (bx - ax) * s1 / total, ay + (by - ay) * s1 / total)],
                       fill=color, width=width)

    def dot(self, x, y, color=INK, r=8):
        cx, cy = self.pt(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    def axes(self, xlab, ylab):
        self.line([(self.xr[0], 0), (self.xr[1], 0)], color=AXIS, width=2)
        self.line([(0, self.yr[0]), (0, self.yr[1])], color=AXIS, width=2)
        d.text((self.x1 - 8, self.py(0) - 26), xlab, font=font(24), fill=GREY, anchor='rs')
        d.text((self.px(0) + 10, self.y0 + 4), ylab, font=font(24), fill=GREY, anchor='la')

    def frame(self):
        d.rectangle([self.x0, self.y0, self.x1, self.y1], outline=FRAME, width=2)


def title(cx, y, s):
    d.text((cx, y), s, font=font(30), fill=INK, anchor='mm')


# ---- 左栏：z 平面上的一个点 ----
PZ = Panel((70, 110, 470, 510), (-2.2, 2.2), (-2.2, 2.2))
PZ.frame()
PZ.axes('x', 'y')
PZ.line([(-2.2, 0), (0, 0)], color=BROWN, width=4, dash=13)
d.text((PZ.px(-2.1), PZ.py(-0.48)), '负实轴 = 分支切割', font=font(24), fill=BROWN, anchor='la')

z0 = 2.0
th0 = math.pi / 4
zx, zy = z0 * math.cos(th0), z0 * math.sin(th0)
PZ.line([(0, 0), (zx, zy)], color=BLUE, width=3)
PZ.dot(zx, zy, BLUE)
d.text((PZ.px(-2.05), PZ.py(-1.02)), 'z0 = 2e^{iπ/4}', font=font(24), fill=BLUE, anchor='la')
d.text((PZ.px(-2.05), PZ.py(-1.55)), '|z0| = 2, arg z0 = π/4',
       font=font(23), fill=BLUE, anchor='la')
title(270, 72, '①  z 平面：取一个点 z0')

# ---- 右栏：w 平面上的全部对数值 ----
PR = Panel((660, 100, 1026, 720), (-1.7, 5.5), (-3.6, 8.6))
PR.frame()
ln2 = math.log(2.0)

# 主值分支带 -π < Im w < π
d.rectangle([PR.px(-1.7), PR.py(math.pi), PR.px(5.5), PR.py(-math.pi)], fill=GREEN_FILL)
PR.frame()
PR.axes('u', 'v')
d.text((PR.px(-1.55), PR.py(2.45)), '主值分支 -π < Im w < π',
       font=font(23), fill=GREEN, anchor='lm')

for k in (0, 1):
    wy = th0 + 2 * k * math.pi
    color = ORANGE if k == 0 else GREY
    PR.dot(ln2, wy, color)
    if k == 0:
        d.text((PR.px(ln2) + 18, PR.py(wy) - 17), 'k = 0：主值',
               font=font(24), fill=ORANGE, anchor='lm')
        d.text((PR.px(ln2) + 18, PR.py(wy) + 15), 'ln 2 + iπ/4',
               font=font(24), fill=ORANGE, anchor='lm')
    else:
        d.text((PR.px(ln2) + 18, PR.py(wy)), 'k = 1：再加 2πi',
               font=font(24), fill=GREY, anchor='lm')

# 两点之间的 2πi 双向箭头
ax = PR.px(0.2)
y_lo, y_hi = PR.py(th0), PR.py(th0 + 2 * math.pi)
d.line([(ax, y_lo), (ax, y_hi)], fill=GREY, width=3)
for yy, sign in ((y_lo, 1), (y_hi, -1)):
    d.polygon([(ax, yy), (ax - 9, yy + 15 * sign), (ax + 9, yy + 15 * sign)], fill=GREY)
d.text((ax + 14, (y_lo + y_hi) / 2), '2πi', font=font(25), fill=GREY, anchor='lm')

d.text((PR.px(-1.5), PR.py(-2.7)), '无穷多支，每支相差 2πi',
       font=font(23), fill=GREY, anchor='lm')
title(843, 72, '②  w 平面：它的全部 Ln 值')

# ---- 中间箭头 ----
d.line([(500, 330), (636, 330)], fill=GREY, width=4)
d.polygon([(656, 330), (632, 318), (632, 342)], fill=GREY)
d.text((578, 296), '取 Ln', font=font(25), fill=GREY, anchor='mm')

d.text((W / 2, H - 28),
       '同一个 z 有无穷多个对数值，两两相差 2πi 的整数倍；写「全部值」时这一段不能省。',
       font=font(24), fill=GREY, anchor='mm')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
