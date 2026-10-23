# -*- coding: utf-8 -*-
"""产图脚本：单连通区域与多连通区域的区别，以及定理在有洞时为什么用不上。

左格：圆盘区域里任意一条闭曲线都能在区域内收缩成一点，柯西积分定理成立，闭路积分为 0。
右格：挖去原点附近的洞，绕洞的闭曲线收缩不下来；被积函数 1/z 在去原点的区域内解析，
      绕洞一圈的积分仍是 2πi。

输出：assets/img/pool/柯西定理-单连通与多连通-对照-本机-01.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '柯西定理-单连通与多连通-对照-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 660
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
FILL = (238, 245, 252)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
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


def arc_arrow(d, center, r, a0, a1, color, width=4, heads=6):
    """沿圆弧画带箭头的曲线：角度用弧度，a0 -> a1 为行进方向。"""
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

# ---------- 左格：单连通 ----------
L_BOX = (40, 84, 606, 552)
d.rectangle(L_BOX, outline=FRAME, width=2)
LC = ((L_BOX[0] + L_BOX[2]) // 2, 320)
R_OUT = 172

d.ellipse([LC[0] - R_OUT, LC[1] - R_OUT, LC[0] + R_OUT, LC[1] + R_OUT], fill=FILL)
d.ellipse([LC[0] - R_OUT, LC[1] - R_OUT, LC[0] + R_OUT, LC[1] + R_OUT],
          outline=BLUE, width=3)
rich(d, (LC[0] - 148, LC[1] - 152), '区域 D', 24, BLUE, anchor='la')

# 区域内一条闭曲线 + 收缩箭头
R_IN = 112
arc_arrow(d, LC, R_IN, 0.4, 2 * math.pi + 0.4, ORANGE, width=4, heads=(20, 55, 90))
rich(d, (LC[0] - 34, LC[1] - R_IN - 34), 'C', 26, ORANGE, anchor='la')

for k in range(3):
    a = math.radians(150 + 120 * k)
    p0 = (LC[0] + R_IN * 0.92 * math.cos(a), LC[1] - R_IN * 0.92 * math.sin(a))
    p1 = (LC[0] + 34 * math.cos(a), LC[1] - 34 * math.sin(a))
    d.line([p0, p1], fill=GREY, width=2)
    arrow_head(d, p0, p1, GREY, head=10)
dot(LC, 6)
rich(d, (LC[0] + 10, LC[1] + 6), '收缩成一点', 22, GREY, anchor='la')

rich(d, ((L_BOX[0] + L_BOX[2]) / 2, L_BOX[1] + 14), '单连通区域：整体没有洞',
     26, INK, anchor='ma')
rich(d, ((L_BOX[0] + L_BOX[2]) / 2, L_BOX[3] - 54),
     'f 在 D 内解析，则沿 C 一圈 ∮ f dz = 0', 26, BLUE, anchor='ma')

# ---------- 右格：多连通 ----------
R_BOX = (636, 84, 1200, 552)
d.rectangle(R_BOX, outline=FRAME, width=2)
RC = ((R_BOX[0] + R_BOX[2]) // 2, 320)
R_HOLE = 66

d.ellipse([RC[0] - R_OUT, RC[1] - R_OUT, RC[0] + R_OUT, RC[1] + R_OUT], fill=FILL)
d.ellipse([RC[0] - R_OUT, RC[1] - R_OUT, RC[0] + R_OUT, RC[1] + R_OUT],
          outline=BLUE, width=3)
d.ellipse([RC[0] - R_HOLE, RC[1] - R_HOLE, RC[0] + R_HOLE, RC[1] + R_HOLE], fill=BG)
d.ellipse([RC[0] - R_HOLE, RC[1] - R_HOLE, RC[0] + R_HOLE, RC[1] + R_HOLE],
          outline=RED, width=3)
dot(RC, 5, RED)
rich(d, (RC[0] + 12, RC[1] + 8), '洞', 24, RED, anchor='la')
rich(d, (RC[0] - 148, RC[1] - 152), '区域 D', 24, BLUE, anchor='la')

# 绕洞的闭曲线（顺时针方向无关紧要，只表示收缩不下来）
R_MID = 118
arc_arrow(d, RC, R_MID, 0.35, 2 * math.pi + 0.35, ORANGE, width=4, heads=(25, 60, 92))
rich(d, (RC[0] - 40, RC[1] - R_MID - 36), 'C', 26, ORANGE, anchor='la')

# 收缩箭头在洞口停住：绕不过去
for k in range(3):
    a = math.radians(150 + 120 * k)
    p0 = (RC[0] + R_MID * 0.93 * math.cos(a), RC[1] - R_MID * 0.93 * math.sin(a))
    p1 = (RC[0] + (R_HOLE + 8) * math.cos(a), RC[1] - (R_HOLE + 8) * math.sin(a))
    d.line([p0, p1], fill=GREY, width=2)
    arrow_head(d, p0, p1, GREY, head=10)

rich(d, ((R_BOX[0] + R_BOX[2]) / 2, R_BOX[1] + 14), '多连通区域：中间被挖掉一块',
     26, INK, anchor='ma')
rich(d, ((R_BOX[0] + R_BOX[2]) / 2, R_BOX[3] - 54),
     'f = 1/z 在 D 内解析，绕洞一圈 ∮ dz/z = 2πi', 25, ORANGE, anchor='ma')
rich(d, (W / 2, 596),
     '定理要的是整块区域单连通；有洞时，绕洞一圈的闭路积分可以不为零。',
     25, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
