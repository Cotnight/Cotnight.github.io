# -*- coding: utf-8 -*-
"""产图脚本：复域内 |sin z| 不再有界。

横轴同一个位置放两个自变量：实轴上的 x 与虚轴上的 y。
蓝线 = |sin x|（始终不超过 1），橙线 = |sin(iy)| = |sinh y|（y = 3 时已超过 10）。

输出：assets/img/pool/初等函数-三角函数-无界性-本机-03.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '初等函数-三角函数-无界性-本机-03.png'))
FONT_PATH = r'C:\Windows\Fonts\simhei.ttf'

W, H = 1200, 780
BG = (255, 255, 255)
INK = (34, 34, 34)
GREY = (110, 110, 110)
AXIS = (85, 85, 85)
GRID = (232, 232, 232)
FRAME = (205, 205, 205)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)

CACHE = {}


def font(size):
    if size not in CACHE:
        CACHE[size] = ImageFont.truetype(FONT_PATH, size)
    return CACHE[size]


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

BOX = (150, 140, 1050, 620)
XR = (-3.2, 3.2)
YR = (-0.6, 10.8)
X0, Y0, X1, Y1 = BOX


def px(x):
    return X0 + (x - XR[0]) / (XR[1] - XR[0]) * (X1 - X0)


def py(y):
    return Y1 - (y - YR[0]) / (YR[1] - YR[0]) * (Y1 - Y0)


d.rectangle(BOX, outline=FRAME, width=2)

# 网格与刻度
for yv in range(0, 11, 2):
    d.line([(px(XR[0]), py(yv)), (px(XR[1]), py(yv))], fill=GRID, width=2)
    d.text((px(XR[0]) - 12, py(yv)), str(yv), font=font(24), fill=GREY, anchor='rm')
for xv in range(-3, 4):
    d.text((px(xv), py(YR[0]) + 12), str(xv), font=font(24), fill=GREY, anchor='mt')

d.line([(px(XR[0]), py(0)), (px(XR[1]), py(0))], fill=AXIS, width=2)
d.line([(px(0), py(YR[0])), (px(0), py(YR[1]))], fill=AXIS, width=2)
d.text((px(0) + 12, Y0 + 8), '|sin z|', font=font(25), fill=GREY, anchor='la')


def plot(fn, color, width=4):
    pts = []
    n = 600
    for i in range(n + 1):
        t = XR[0] + (XR[1] - XR[0]) * i / n
        v = fn(t)
        if v is None:
            continue
        pts.append((px(t), py(min(v, YR[1]))))
    d.line(pts, fill=color, width=width, joint='curve')


plot(lambda t: abs(math.sin(t)), BLUE, 5)
plot(lambda t: abs(math.sinh(t)) if abs(t) <= 3.05 else None, ORANGE, 5)

# |sin x| 的上界线
d.line([(px(XR[0]), py(1.0)), (px(XR[1]), py(1.0))], fill=(150, 150, 150), width=2)
d.text((px(-3.1), py(0.32)), '虚线：实轴上的上界 1',
       font=font(23), fill=(120, 120, 120), anchor='la')

# 虚轴上 y = 2 的点：|sin(2i)| = 3.63
for yv in (2.0,):
    v = abs(math.sinh(yv))
    cx, cy = px(yv), py(v)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=ORANGE)
    d.text((cx - 16, cy - 30), 'y = 2：|sin(2i)| = 3.63',
           font=font(24), fill=ORANGE, anchor='rm')

# 图例
lx, ly = px(-1.15), py(9.3)
d.line([(lx, ly), (lx + 60, ly)], fill=BLUE, width=5)
d.text((lx + 74, ly), '|sin x|，横轴取实部 x', font=font(24), fill=BLUE, anchor='lm')
ly2 = ly + 44
d.line([(lx, ly2), (lx + 60, ly2)], fill=ORANGE, width=5)
d.text((lx + 74, ly2), '|sin(iy)| = |sinh y|，横轴取虚部 y',
       font=font(24), fill=ORANGE, anchor='lm')

d.text((W / 2, H - 34),
       '沿实轴 |sin x| 始终不超过 1，沿虚轴却按双曲正弦指数增长：复域内的 sin z 无界。',
       font=font(25), fill=GREY, anchor='mm')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
