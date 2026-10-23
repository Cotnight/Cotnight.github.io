# -*- coding: utf-8 -*-
"""产图脚本：复合闭路（挖洞）——大圈换成内圈，内圈取顺时针。

左格：外圈 C 逆时针（区域在左手边），洞里的两个奇点各用小圈 C₁、C₂ 圈住，小圈取顺时针
      （沿复合闭路 Γ = C + C₁ + C₂ 走一圈时，环形区域同样始终在左手边）。
右格：把等式写成可算的形式：∮_C f dz = ∮_C₁ f dz + ∮_C₂ f dz，小圈上按上一课的公式算。

输出：assets/img/pool/柯西定理-复合闭路-挖洞方向-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '柯西定理-复合闭路-挖洞方向-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 700
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
FILL = (238, 245, 252)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
RED = (176, 42, 42)
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
    return total


def arrow_head(d, p_from, p_to, color, head=14):
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


def texdraw(d, xy, text, size, fill, anchor='la'):
    """比 rich 多一件事：把 _{X} 画成下标，用来写 ∮_{C} 这类记号。"""
    segs = []
    i = 0
    while i < len(text):
        if text.startswith('_{', i):
            j = text.index('}', i)
            segs.append((text[i + 2:j], True))
            i = j + 1
        else:
            j = text.find('_{', i)
            j = len(text) if j < 0 else j
            segs.append((text[i:j], False))
            i = j
    sub_size = int(round(size * 0.74))
    widths = []
    for s, z in segs:
        for part, is_cjk_part in runs(s):
            f = font(FONT_CJK if is_cjk_part else FONT_MATH,
                     sub_size if z else size)
            widths.append(d.textlength(part, font=f))
    total = sum(widths)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    k = 0
    for s, z in segs:
        for part, is_cjk_part in runs(s):
            f = font(FONT_CJK if is_cjk_part else FONT_MATH,
                     sub_size if z else size)
            dy = size * 0.30 if z else 0
            d.text((x, y + dy), part, font=f, fill=fill, anchor='l' + anchor[1])
            x += widths[k]
            k += 1

def arc_arrow(d, center, r, a0, a1, color, width=4, heads=(30, 65, 92)):
    n = max(int(abs(a1 - a0) / 0.04), 12)
    pts = [(center[0] + r * math.cos(a0 + (a1 - a0) * i / n),
            center[1] - r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=color, width=width)
    for k in heads:
        i = max(1, min(n, int(n * k / 100)))
        arrow_head(d, pts[i - 1], pts[i], color)


def dot(p, r=6, color=INK):
    d.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=color)


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- 左格：复合闭路 ----------
BOX = (40, 84, 650, 600)
d.rectangle(BOX, outline=FRAME, width=2)
C0 = (345, 340)
R_OUT, R_IN = 170, 46

d.ellipse([C0[0] - R_OUT, C0[1] - R_OUT, C0[0] + R_OUT, C0[1] + R_OUT], fill=FILL)
d.ellipse([C0[0] - R_OUT, C0[1] - R_OUT, C0[0] + R_OUT, C0[1] + R_OUT],
          outline=BLUE, width=4)
# 大圈 C：逆时针
arc_arrow(d, C0, R_OUT, 0.25, 2 * math.pi + 0.25, BLUE, width=4, heads=(18, 52, 86))
rich(d, (C0[0] - 22, C0[1] - R_OUT - 34), 'C', 28, BLUE, anchor='la')

# 两个洞与内圈
holes = [(-92, 'C₁'), (92, 'C₂')]
for dx, name in holes:
    hc = (C0[0] + dx, C0[1] + 26)
    d.ellipse([hc[0] - R_IN, hc[1] - R_IN, hc[0] + R_IN, hc[1] + R_IN], fill=BG)
    d.ellipse([hc[0] - R_IN, hc[1] - R_IN, hc[0] + R_IN, hc[1] + R_IN],
              outline=RED, width=2)
    # 小圈取顺时针：角度递减
    arc_arrow(d, hc, R_IN, 0.25, 0.25 - 2 * math.pi, ORANGE, width=4,
              heads=(30, 72))
    dot(hc, 5, RED)
    rich(d, (hc[0] - 24, hc[1] + R_IN + 10), name, 26, ORANGE, anchor='la')

rich(d, (C0[0] - 46, C0[1] - 116), '环形区域', 24, GREEN, anchor='la')
rich(d, ((BOX[0] + BOX[2]) / 2, BOX[1] + 14), '挖洞：大圈换成内圈，内圈取顺时针',
     25, INK, anchor='ma')

# ---------- 右格：等式与算例 ----------
T_BOX = (680, 84, 1200, 600)
d.rectangle(T_BOX, outline=FRAME, width=2)
lines = [
    ('红色小圈里各藏一个奇点', RED),
    ('C₁ 圈住 z = 1，C₂ 圈住 z = −1', RED),
    ('', INK),
    ('沿 Γ = C + C₁ + C₂ 走一圈', INK),
    ('环形区域始终在左手边', GREY),
    ('所以 ∮_{Γ} f dz = 0', INK),
    ('', INK),
    ('∮_{C} f dz = ∮_{C₁} f dz + ∮_{C₂} f dz', BLUE),
    ('', INK),
    ('f = z/(z² − 1)：', INK),
    ('大圈 2πi，两个小圈各 πi', ORANGE),
]
y = 130
for text, color in lines:
    if text:
        texdraw(d, (706, y), text, 27, color, anchor='la')
    y += 42

rich(d, (W / 2, 640),
     '内圈方向与大小圈之间的等式是同一件事：复合闭路上积分为零，移项即得大圈等于小圈之和。',
     24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
