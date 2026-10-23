# -*- coding: utf-8 -*-
"""产图脚本：收敛半径的两条公式与四个算例（算例都取自公开试卷与 B 集）。

左格：比值法与根值法两条公式，以及「算出来的是相邻系数比的极限，R 取倒数」这句提醒；
      再给出由函数求半径的那条路：展开中心到最近奇点的距离。
右格：四行算例——∑(iz)^n 得 R = 1、∑z^n/(1+i)^n 得 R = √2、∑n! z^n 得 R = 0、
      ∑(n!/n^n) z^n 得 R = e，每行把「相邻系数比的极限」写在中间。

输出：assets/img/pool/幂级数-收敛半径-比值法与算例-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '幂级数-收敛半径-比值法与算例-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 800
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
ROW = (244, 247, 250)
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


def tokens(text):
    """切成 (串, shift)：0 正常，1 下标，-1 上标。写法 _{X} 与 ^{X}。"""
    segs = []
    buf = ''
    i = 0
    while i < len(text):
        if text.startswith('_{', i) or text.startswith('^{', i):
            if buf:
                segs.append((buf, 0))
                buf = ''
            j = text.index('}', i)
            segs.append((text[i + 2:j], 1 if text[i] == '_' else -1))
            i = j + 1
        else:
            buf += text[i]
            i += 1
    if buf:
        segs.append((buf, 0))
    return segs


def mdraw(d, xy, text, size, fill, anchor='la'):
    pieces = []
    for s, shift in tokens(text):
        f_size = int(round(size * 0.72)) if shift else size
        for part, cjk in runs(s):
            f = font(FONT_CJK if cjk else FONT_MATH, f_size)
            dy = 0
            if shift == 1:
                dy = size * 0.30
            elif shift == -1:
                dy = -size * 0.34
            pieces.append((part, f, dy, d.textlength(part, font=f)))
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


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

mdraw(d, (W / 2, 34), '收敛半径：两条公式，四行算例', 30, INK, anchor='ma')

# ---------------- 左格：公式与提醒 ----------------
L = (36, 84, 610, 700)
d.rectangle(L, outline=FRAME, width=2)

mdraw(d, (60, 104), '比值法', 27, BLUE, anchor='la')
mdraw(d, (60, 146), 'R = lim |a_{n} / a_{n+1}|', 27, INK, anchor='la')
mdraw(d, (60, 190), '   = 1 / lim |a_{n+1} / a_{n}|', 27, INK, anchor='la')

mdraw(d, (60, 258), '根值法', 27, BLUE, anchor='la')
mdraw(d, (60, 300), 'R = 1 / lim |a_{n}|^{1/n}', 27, INK, anchor='la')

d.line([(60, 372), (586, 372)], fill=FRAME, width=2)

mdraw(d, (60, 392), '算的是相邻系数比的极限，R 取它的倒数', 23, RED, anchor='la')
mdraw(d, (60, 428), '系数越来越大 ⟹ R 越来越小', 23, GREY, anchor='la')
mdraw(d, (60, 464), '系数带 i 时先算模，模是实数', 23, GREY, anchor='la')

d.line([(60, 512), (586, 512)], fill=FRAME, width=2)

mdraw(d, (60, 532), '由函数求半径（填空 3 分）', 24, ORANGE, anchor='la')
mdraw(d, (60, 572), 'R = 展开中心到最近奇点的距离', 24, INK, anchor='la')
mdraw(d, (60, 612), 'f = 1 / ((z + 5)(z − 3))，z_{0} = 0', 24, INK, anchor='la')
mdraw(d, (60, 652), '到 5 与 3 取小的：R = 3', 24, GREEN, anchor='la')

# ---------------- 右格：四行算例 ----------------
Rb = (626, 84, 1204, 700)
d.rectangle(Rb, outline=FRAME, width=2)
mdraw(d, (650, 104), '试卷与 B 集上的算例', 26, INK, anchor='la')

X_ROW = 650
X_LIM = 886
X_R = 1182
rows = [
    ('∑ (iz)^{n}', '|i| = 1', 'R = 1'),
    ('∑ z^{n} / (1 + i)^{n}', '1/|1+i| = 1/√2', 'R = √2'),
    ('∑ n! z^{n}', 'n + 1 → +∞', 'R = 0'),
    ('∑ (n! / n^{n}) z^{n}', '(n/(n+1))^{n} → 1/e', 'R = e'),
]
y = 168
for i, (ser, lim, rad) in enumerate(rows):
    d.rectangle([640, y - 8, 1190, y + 74], fill=ROW if i % 2 == 0 else BG)
    mdraw(d, (X_ROW, y + 8), ser, 24, BLUE, anchor='la')
    mdraw(d, (X_LIM, y + 10), lim, 21, GREY, anchor='la')
    mdraw(d, (X_R, y + 8), rad, 24, GREEN, anchor='ra')
    y += 88

mdraw(d, (640, y + 8), '相邻系数比的极限写在中间，右边是取倒数后的 R。', 21, GREY, anchor='la')
mdraw(d, (X_LIM, 126), '|a_{n+1}/a_{n}| 的极限', 21, GREY, anchor='la')

mdraw(d, (W / 2, H - 56),
      '四行都是同一个动作：认清 a_{n} → 算 |a_{n+1}/a_{n}| 的极限 → 取倒数。',
      24, GREY, anchor='ma')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
