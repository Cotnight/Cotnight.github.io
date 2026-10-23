# -*- coding: utf-8 -*-
"""产图脚本：曼德博集——迭代 z -> z^2 + c 时留在有界区域内的那些 c。

输出：assets/img/pool/绪论-分形-曼德博集迭代-本机-03.png
纯 numpy 迭代 + Pillow 绘制；图上标出当例子的两个 c：c = -1 留在集内、c = 1 逃逸。
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '绪论-分形-曼德博集迭代-本机-03.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, FH = 1000, 640          # 分形区
BAND = 62                  # 底部说明带
H = FH + BAND
CACHE = {}

# 视窗（宽高比与分形区一致）
X0, X1 = -2.2, 1.3
Y1 = 1.12
Y0 = -1.12
MAXIT = 100
BAIL = 4.0


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


def to_px(zx, zy):
    return ((zx - X0) / (X1 - X0) * W, (Y1 - zy) / (Y1 - Y0) * FH)


xs = np.linspace(X0, X1, W)
ys = np.linspace(Y1, Y0, FH)
cx, cy = np.meshgrid(xs, ys)
c = cx + 1j * cy
z = np.zeros_like(c)
alive = np.ones(c.shape, dtype=bool)
count = np.zeros(c.shape, dtype=np.int32)
for _ in range(MAXIT):
    z[alive] = z[alive] * z[alive] + c[alive]
    escaped = alive & (np.abs(z) > BAIL)
    count[escaped] = _
    alive &= ~escaped
count[alive] = MAXIT

# 配色：逃逸越快越浅，贴近边界越深，集内最深
t = np.clip(np.sqrt(count.astype(np.float64) / MAXIT), 0.0, 1.0)
lo = np.array([240.0, 246.0, 252.0])
hi = np.array([88.0, 148.0, 208.0])
rgb = lo[None, None, :] + (hi - lo)[None, None, :] * t[:, :, None]
rgb[count >= MAXIT] = np.array([26.0, 60.0, 112.0])

img = Image.new('RGB', (W, H), (255, 255, 255))
img.paste(Image.fromarray(rgb.astype(np.uint8), 'RGB'), (0, 0))
d = ImageDraw.Draw(img)

# 标出两个例子
for zx, zy, label, ink in [(-1.0, 0.0, 'c = -1', (255, 255, 255)),
                           (1.0, 0.0, 'c = 1', (26, 60, 112))]:
    px, py = to_px(zx, zy)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], outline=ink, width=3)
    rich(d, (px + 16, py - 12), label, 26, ink, anchor='la')

rich(d, (W / 2, FH + 18),
     '图上每一点是一个 c；深色区域里的 c 让 0, c, c² + c, … 不逃向无穷。',
     23, (110, 110, 110), anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
