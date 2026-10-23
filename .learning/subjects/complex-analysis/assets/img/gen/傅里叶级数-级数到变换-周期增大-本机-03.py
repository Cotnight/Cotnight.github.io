# -*- coding: utf-8 -*-
"""产图脚本：从傅里叶级数到傅里叶变换——周期变大时谱线怎么变。

上排三格是同一个矩形脉冲（|t| < 1 上取 1，按周期 T 重复）的频谱，T 依次为 4、8、16：
相邻谱线的间距 Δω = 2π/T 减半，每根谱线的高度按 1/T 变矮，虚线包络原地不动。
下排写出这一步跨过去之后的两个式子。

输出：assets/img/pool/傅里叶级数-级数到变换-周期增大-本机-03.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '傅里叶级数-级数到变换-周期增大-本机-03.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 880
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (120, 120, 120)
FRAME = (202, 202, 202)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
GREEN = (24, 120, 84)
RED = (176, 42, 42)

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


def layout(text, size, depth=0):
    """把一串文字切成 (串, 字号, 上移量)，支持嵌套的 _{...} 与 ^{...}。"""
    pieces = []
    buf = ''
    i = 0

    def flush():
        nonlocal buf
        if buf:
            for part, cjk in runs(buf):
                f = font(FONT_CJK if cjk else FONT_MATH, size)
                pieces.append((part, f, 0.0))
            buf = ''

    while i < len(text):
        if (text.startswith('_{', i) or text.startswith('^{', i)) and depth < 3:
            flush()
            open_at = i
            depth_n = 0
            j = i + 1
            while j < len(text):
                if text[j] == '{':
                    depth_n += 1
                elif text[j] == '}':
                    depth_n -= 1
                    if depth_n == 0:
                        break
                j += 1
            inner = text[open_at + 2:j]
            inner_size = int(round(size * 0.72))
            dy = size * 0.30 if text[open_at] == '_' else -size * 0.34
            for part, f, d2 in layout(inner, inner_size, depth + 1):
                pieces.append((part, f, dy + d2))
            i = j + 1
        else:
            buf += text[i]
            i += 1
    flush()
    return pieces


def mdraw(d, xy, text, size, fill, anchor='la'):
    pieces = [(part, f, dy, d.textlength(part, font=f))
              for part, f, dy in layout(text, size)]
    total = sum(p[3] for p in pieces)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for part, f, dy, w in pieces:
        d.text((x, y + dy), part, font=f, fill=fill, anchor='l' + anchor[1])
        x += w
    return total


def mdraw_halo(d, xy, text, size, fill, anchor='la', bg=BG):
    for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)):
        mdraw(d, (xy[0] + ox, xy[1] + oy), text, size, bg, anchor=anchor)
    return mdraw(d, xy, text, size, fill, anchor=anchor)


def arrow_head(d, p_from, p_to, color, head=13):
    (x0, y0), (x1, y1) = p_from, p_to
    dx, dy = x1 - x0, y1 - y0
    n = max(math.hypot(dx, dy), 1e-9)
    ux, uy = dx / n, dy / n
    px, py = -uy, ux
    d.polygon([(x1, y1),
               (x1 - ux * head * 1.7 + px * head * 0.75,
                y1 - uy * head * 1.7 + py * head * 0.75),
               (x1 - ux * head * 1.7 - px * head * 0.75,
                y1 - uy * head * 1.7 - py * head * 0.75)], fill=color)


def dash_poly(d, pts, color, width=2, dash=9, gap=7):
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        ux, uy = dx / L, dy / L
        s = 0.0
        while s < L:
            e = min(s + dash, L)
            d.line([(a[0] + ux * s, a[1] + uy * s), (a[0] + ux * e, a[1] + uy * e)],
                   fill=color, width=width)
            s += dash + gap


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

mdraw(d, (W / 2, 26), '周期变大：谱线变密、每根变矮，极限是连续谱', 31, INK, anchor='ma')

OM = 3.4
VMAX = 0.56
PANELS = [(40, 400), (435, 795), (830, 1190)]
TOP, BOT = 96, 430


def draw_panel(x0, x1, T):
    d.rectangle((x0, TOP, x1, BOT), outline=FRAME, width=2)
    axis_y = BOT - 56

    def px(w):
        return x0 + 22 + (w + OM) / (2 * OM) * (x1 - x0 - 44)

    def py(v):
        return axis_y - v / VMAX * (axis_y - TOP - 62)

    w0 = 2 * math.pi / T
    d.line([(px(-OM), axis_y), (px(OM), axis_y)], fill=GREY, width=2)
    d.line([(px(0), axis_y), (px(0), axis_y - (axis_y - TOP - 56))], fill=(224, 224, 224), width=2)

    n = 0
    while n * w0 <= OM:
        for sgn in ((0,) if n == 0 else (1, -1)):
            w = sgn * n * w0
            c = (2 / T) * (1.0 if n == 0 else math.sin(n * w0) / (n * w0))
            if abs(c) > 1e-9:
                d.line([(px(w), axis_y), (px(w), py(c))], fill=BLUE, width=3)
                d.ellipse([px(w) - 5, py(c) - 5, px(w) + 5, py(c) + 5], fill=BLUE)
        n += 1

    # 包络：T 倍的谱线高度，随 T 增大不动
    env_x = [-OM + 0.02 * i for i in range(0, int(2 * OM / 0.02) + 1)]
    env_pts = [(px(w), py((2 / T) * abs(math.sin(w) / w) if abs(w) > 1e-6 else 2 / T))
               for w in env_x]
    dash_poly(d, env_pts, ORANGE, width=2)

    for t in (-2, 0, 2):
        d.line([(px(t), axis_y - 5), (px(t), axis_y + 5)], fill=GREY, width=2)
        mdraw_halo(d, (px(t), axis_y + 12), str(t), 23, GREY, anchor='ma')
    mdraw_halo(d, (px(OM) - 4, axis_y - 34), 'ω', 25, GREY, anchor='ra')

    mdraw(d, (x0 + 18, TOP + 14), f'周期 T = {T}', 25, INK, anchor='la')
    mdraw(d, (x0 + 18, TOP + 46), f'c₀ = {2 / T:.3f}', 23, BLUE, anchor='la')
    mdraw(d, (x1 - 14, TOP + 16), f'Δω = 2π/T ≈ {w0:.2f}', 22, GREY, anchor='ra')


for (x0, x1), T in zip(PANELS, (4, 8, 16)):
    draw_panel(x0, x1, T)

mdraw(d, (W / 2, BOT + 14),
      '同一个矩形脉冲：周期翻倍，谱线间距减半、每根高度减半，包络不动。',
      24, GREY, anchor='ma')

# 下排：跨过去的那一步
INFO = (40, 486, 1200, 848)
d.rectangle(INFO, outline=FRAME, width=2)

ax0, ax1, ay = INFO[0] + 60, INFO[2] - 60, INFO[1] + 40
d.line([(ax0, ay), (ax1 - 10, ay)], fill=BLUE, width=3)
arrow_head(d, (ax1 - 30, ay), (ax1, ay), BLUE, head=13)
mdraw(d, (W / 2, ay - 40), 'T → ∞', 26, BLUE, anchor='ma')

lines = [
    ('谱线间距 Δω = 2π/T → 0：一根根离散的谱线连成一条曲线。', INK),
    ('每根的高度 c_{n} → 0，但 T c_{n} 趋于有限值 F(ω_{n})，', INK),
    ('所以把求和写成步长为 Δω 的求和，再取极限：', INK),
]
y = ay + 30
for text, color in lines:
    mdraw(d, (INFO[0] + 30, y), text, 24, color, anchor='la')
    y += 38

y += 10
mdraw(d, (INFO[0] + 30, y), '周期函数　　　f(t) = (1/2π) Σ F(ω_{n}) e^{iω_{n}t} Δω', 25, GREEN, anchor='la')
y += 44
mdraw(d, (INFO[0] + 30, y), '周期趋于无穷　f(t) = (1/2π) ∫ F(ω) e^{iωt} dω', 25, GREEN, anchor='la')
y += 44
mdraw(d, (INFO[0] + 30, y), '其中　　　　　F(ω) = ∫ f(t) e^{−iωt} dt', 25, GREEN, anchor='la')

mdraw(d, (INFO[0] + 30, INFO[3] - 44),
      '下一课以这两个式子为定义；本课只要求知道级数是怎么过去的。',
      23, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
