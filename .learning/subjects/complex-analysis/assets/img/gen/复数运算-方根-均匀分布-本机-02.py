# -*- coding: utf-8 -*-
"""产图脚本：n 次方根的 n 个值在圆上均匀分布。

左栏 ³√(-8) 的三个根（半径 2 的圆上，相邻差 2π/3），右栏 ⁴√1 的四个根
（单位圆上，相邻差 π/2）。两栏都用 k = 0,1,2,(3) 标出对应的那个值。

输出：assets/img/pool/复数运算-方根-均匀分布-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '复数运算-方根-均匀分布-本机-02.png'))

CJK_FONT = r'C:\Windows\Fonts\msyh.ttc'
MATH_FONT = r'C:\Windows\Fonts\cambria.ttc'
MATH_CHARS = set('πθφ√²³⁴∈≥≤≠≈−×∠′Δ∂→∫ωΩ')

W, H = 1240, 700
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (105, 105, 105)
AXIS = (85, 85, 85)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
GREEN = (50, 130, 82)
GREEN_FILL = (234, 245, 236)
ORANGE = (196, 92, 24)
CREAM = (252, 244, 228)

CACHE = {}


def font(path, size):
    key = (path, size)
    if key not in CACHE:
        CACHE[key] = ImageFont.truetype(path, size)
    return CACHE[key]


def runs_of(s, size):
    runs = []
    for ch in s:
        path = MATH_FONT if ch in MATH_CHARS else CJK_FONT
        if runs and runs[-1][0] == path:
            runs[-1][1] += ch
        else:
            runs.append([path, ch])
    return [(p, t, font(p, size).getlength(t)) for p, t in runs]


def text(d, x, y, s, size=24, fill=INK, anchor='ls'):
    runs = runs_of(s, size)
    total = sum(r[2] for r in runs)
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    if anchor[1] == 'm':
        y += 0.36 * size
    for p, t, w in runs:
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

    def circle(self, r, color=INK, width=3, dash=None, cx=0.0, cy=0.0):
        n = 180
        pts = [(cx + r * math.cos(2 * math.pi * i / n),
                cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
        self.line(pts, color=color, width=width, dash=dash)

    def arc(self, r, a0, a1, color=INK, width=3):
        n = max(8, int(abs(a1 - a0) / 0.04))
        pts = [(r * math.cos(a0 + (a1 - a0) * i / n),
                r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.line(pts, color=color, width=width)

    def axes(self, xlab, ylab):
        self.line([(self.xr[0], 0), (self.xr[1], 0)], color=AXIS, width=2)
        self.line([(0, self.yr[0]), (0, self.yr[1])], color=AXIS, width=2)
        d.text((self.x1 - 6, self.py(0) - 22), xlab, font=font(CJK_FONT, 23),
               fill=GREY, anchor='rs')
        d.text((self.px(0) + 10, self.y0 + 4), ylab, font=font(CJK_FONT, 23),
               fill=GREY, anchor='la')

    def frame(self):
        d.rectangle([self.x0, self.y0, self.x1, self.y1], outline=FRAME, width=2)


# ---------------- 左栏：³√(-8) ----------------
PL = Panel((100, 130, 540, 570), (-2.5, 2.5), (-2.5, 2.5))
PL.circle(2.0, color=GREEN, width=2, dash=9)
PL.axes('x', 'y')

r3 = [math.pi / 3, math.pi, 5 * math.pi / 3]
for a in r3:
    x, y = 2 * math.cos(a), 2 * math.sin(a)
    PL.line([(0, 0), (x, y)], color=BLUE, width=2)
    PL.dot(x, y, BLUE, 9)
PL.arc(0.62, math.pi / 3, math.pi, color=ORANGE, width=3)
PL.arc(0.62, math.pi / 3, 0, color=ORANGE, width=3)
text(d, PL.px(-0.62), PL.py(0.62), '2π/3', 23, ORANGE, anchor='mm')
text(d, PL.px(0.72), PL.py(-0.42), '2π/3', 23, ORANGE, anchor='lm')
text(d, PL.px(1.62), PL.py(0.52), '半径 2', 22, GREY, anchor='rs')

text(d, PL.px(1.0) + 16, PL.py(1.73) + 8, 'k = 0', 23, BLUE, anchor='ls')
text(d, PL.px(-2.0) + 16, PL.py(0.0) - 14, 'k = 1', 23, BLUE, anchor='ls')
text(d, PL.px(1.0) + 16, PL.py(-1.73) + 10, 'k = 2', 23, BLUE, anchor='ls')
PL.frame()
text(d, (PL.x0 + PL.x1) / 2, PL.y0 - 22, '①  ³√(−8)：三个根，k = 0, 1, 2',
     26, INK, anchor='ms')
text(d, (PL.x0 + PL.x1) / 2, 604,
     'k = 0：1 + √3i　　k = 1：−2　　k = 2：1 − √3i', 22, INK, anchor='ms')

# ---------------- 右栏：⁴√1 ----------------
PR = Panel((700, 130, 1140, 570), (-1.9, 1.9), (-1.9, 1.9))
PR.circle(1.0, color=GREEN, width=2)
PR.axes('x', 'y')

r4 = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2]
for a in r4:
    x, y = math.cos(a), math.sin(a)
    PR.line([(0, 0), (x, y)], color=BLUE, width=2)
    PR.dot(x, y, BLUE, 9)
PR.arc(0.42, 0, math.pi / 2, color=ORANGE, width=3)
text(d, PR.px(0.58), PR.py(0.34), 'π/2', 23, ORANGE, anchor='lm')
text(d, PR.px(1.55), PR.py(1.42), '半径 1', 22, GREY, anchor='rm')
text(d, PR.px(1.0) + 15, PR.py(0.0) + 30, 'k = 0', 23, BLUE, anchor='ls')
text(d, PR.px(0.0) + 14, PR.py(1.0) - 10, 'k = 1', 23, BLUE, anchor='ls')
text(d, PR.px(-1.0) + 15, PR.py(0.0) - 13, 'k = 2', 23, BLUE, anchor='ls')
text(d, PR.px(0.0) + 14, PR.py(-1.0) + 30, 'k = 3', 23, BLUE, anchor='ls')
PR.frame()
text(d, (PR.x0 + PR.x1) / 2, PR.y0 - 22, '②  ⁴√1：四个根，k = 0, 1, 2, 3',
     26, INK, anchor='ms')
text(d, (PR.x0 + PR.x1) / 2, 604,
     'k = 0：1　　k = 1：i　　k = 2：−1　　k = 3：−i', 22, INK, anchor='ms')

d.rectangle([60, 632, W - 60, 682], fill=CREAM)
text(d, W / 2, 666,
     'n 个根都落在以原点为心、半径 √|z| 的圆上，相邻两个相差 2π/n；k 只取 0 到 n − 1。',
     24, INK, anchor='ms')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
