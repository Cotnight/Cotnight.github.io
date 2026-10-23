# -*- coding: utf-8 -*-
"""产图脚本：四种常见区域与它们的不等式写法。

四格依次是圆盘 |z - 1| < 2、圆环 1 < |z| < 3、竖直带 0 < Re z < 1、角域
-π/4 < arg z < π/4。严格不等号画虚线边界（边界不算），每格标题下写出
「有界 / 无界 · 单连通 / 多连通 · 开」。

输出：assets/img/pool/复数运算-区域-不等式对照-本机-03.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '复数运算-区域-不等式对照-本机-03.png'))

CJK_FONT = r'C:\Windows\Fonts\msyh.ttc'
MATH_FONT = r'C:\Windows\Fonts\cambria.ttc'
MATH_CHARS = set('πθφ√²³⁴∈≥≤≠≈−×∠′Δ∂→∫ωΩ')

W, H = 1240, 1092
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (105, 105, 105)
AXIS = (85, 85, 85)
FRAME = (205, 205, 205)
GREEN = (50, 130, 82)
GREEN_FILL = (232, 243, 235)
ORANGE = (196, 92, 24)

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

    def dot(self, x, y, color=INK, r=7):
        cx, cy = self.pt(x, y)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

    def circle(self, r, color=INK, width=3, dash=None, cx=0.0, cy=0.0, fill=None):
        if fill is not None:
            box = [self.px(cx - r), self.py(cy + r), self.px(cx + r), self.py(cy - r)]
            d.ellipse(box, fill=fill)
        n = 180
        pts = [(cx + r * math.cos(2 * math.pi * i / n),
                cy + r * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
        self.line(pts, color=color, width=width, dash=dash)

    def poly(self, pts, fill=None, color=None, width=3, dash=None):
        if fill is not None:
            d.polygon([self.pt(x, y) for x, y in pts], fill=fill)
        if color is not None:
            self.line(pts + [pts[0]], color=color, width=width, dash=dash)

    def arc(self, r, a0, a1, color=INK, width=3):
        n = max(8, int(abs(a1 - a0) / 0.04))
        pts = [(r * math.cos(a0 + (a1 - a0) * i / n),
                r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.line(pts, color=color, width=width)

    def axes(self, xlab='x', ylab='y'):
        self.line([(self.xr[0], 0), (self.xr[1], 0)], color=AXIS, width=2)
        self.line([(0, self.yr[0]), (0, self.yr[1])], color=AXIS, width=2)
        d.text((self.x1 - 5, self.py(0) - 20), xlab, font=font(CJK_FONT, 22),
               fill=GREY, anchor='rs')
        d.text((self.px(0) + 9, self.y0 + 3), ylab, font=font(CJK_FONT, 22),
               fill=GREY, anchor='la')

    def frame(self):
        d.rectangle([self.x0, self.y0, self.x1, self.y1], outline=FRAME, width=2)


def heading(p, s, kind):
    cx = (p.x0 + p.x1) / 2
    text(d, cx, p.y0 - 46, s, 25, INK, anchor='ms')
    text(d, cx, p.y0 - 16, kind, 21, GREY, anchor='ms')


# ---------------- ① |z - 1| < 2 ----------------
P1 = Panel((90, 155, 490, 555), (-1.2, 3.2), (-2.2, 2.2))
P1.circle(2.0, color=GREEN, width=3, dash=9, cx=1.0, fill=GREEN_FILL)
P1.frame()
P1.axes()
P1.dot(1.0, 0.0, GREEN, 6)
P1.line([(1.0, 0.0), (1.0 + 2 * math.cos(math.pi / 4), 2 * math.sin(math.pi / 4))],
        color=GREEN, width=2, dash=7)
text(d, P1.px(1.72), P1.py(1.42), 'r = 2', 22, GREEN, anchor='ms')
text(d, P1.px(1.0) + 10, P1.py(0.0) + 28, '圆心 1', 22, GREEN, anchor='ls')
heading(P1, '|z − 1| < 2：圆盘', '有界 · 单连通 · 开')

# ---------------- ② 1 < |z| < 3 ----------------
P2 = Panel((700, 155, 1100, 555), (-3.2, 3.2), (-3.2, 3.2))
P2.circle(3.0, color=GREEN, width=2, dash=9, fill=GREEN_FILL)
P2.circle(1.0, color=BG, width=1, fill=BG)
P2.circle(1.0, color=GREEN, width=3, dash=9)
P2.frame()
P2.axes()
text(d, P2.px(0.55) - 4, P2.py(0.0) - 12, '1', 23, GREEN, anchor='rs')
text(d, P2.px(2.55) - 4, P2.py(0.0) - 12, '3', 23, GREEN, anchor='rs')
text(d, P2.px(0.0), P2.py(-2.05), '内圆被挖掉，所以是多连通', 21, GREY, anchor='ms')
heading(P2, '1 < |z| < 3：圆环', '有界 · 多连通 · 开')

# ---------------- ③ 0 < Re z < 1 ----------------
P3 = Panel((90, 665, 490, 1065), (-1.6, 2.6), (-2.1, 2.1))
d.rectangle([P3.px(0), P3.y0, P3.px(1), P3.y1], fill=GREEN_FILL)
P3.frame()
P3.axes()
P3.line([(0, P3.yr[0]), (0, P3.yr[1])], color=GREEN, width=3, dash=9)
P3.line([(1, P3.yr[0]), (1, P3.yr[1])], color=GREEN, width=3, dash=9)
text(d, P3.px(1.0) + 10, P3.py(1.55), 'Re z = 1', 21, GREEN, anchor='ls')
text(d, P3.px(0.0) - 10, P3.py(1.55), 'Re z = 0', 21, GREEN, anchor='rs')
heading(P3, '0 < Re z < 1：竖直带', '无界 · 单连通 · 开')

# ---------------- ④ −π/4 < arg z < π/4 ----------------
P4 = Panel((700, 665, 1100, 1065), (-1.6, 3.0), (-2.3, 2.3))
a = math.pi / 4
RR = 3.6
P4.poly([(0, 0),
         (RR * math.cos(-a), RR * math.sin(-a)),
         (RR * math.cos(a), RR * math.sin(a))], fill=GREEN_FILL)
P4.frame()
P4.axes()
P4.line([(0, 0), (RR * math.cos(a), RR * math.sin(a))], color=GREEN, width=3, dash=9)
P4.line([(0, 0), (RR * math.cos(-a), RR * math.sin(-a))], color=GREEN, width=3, dash=9)
P4.arc(0.95, 0, a, color=ORANGE, width=3)
P4.arc(0.95, 0, -a, color=ORANGE, width=3)
text(d, P4.px(1.25), P4.py(0.44), 'π/4', 22, ORANGE, anchor='lm')
text(d, P4.px(1.25), P4.py(-0.44), '−π/4', 22, ORANGE, anchor='lm')
text(d, P4.px(-1.45), P4.py(-2.0), '张角 90 度的角域', 21, GREY, anchor='ls')
heading(P4, '−π/4 < arg z < π/4：角域', '无界 · 单连通 · 开')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')

