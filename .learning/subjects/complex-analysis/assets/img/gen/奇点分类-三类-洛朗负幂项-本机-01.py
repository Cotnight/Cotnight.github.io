# -*- coding: utf-8 -*-
"""产图脚本：可去奇点、m 阶极点、本性奇点三分对照，按洛朗展开的负幂项判定。

输出：assets/img/pool/奇点分类-三类-洛朗负幂项-本机-01.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '奇点分类-三类-洛朗负幂项-本机-01.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 866
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (120, 120, 120)
DEEP = (26, 78, 140)
BLUE = (32, 105, 190)
RED = (190, 55, 45)
AMBER = (163, 112, 18)
PANEL = (247, 249, 252)
FRAME = (219, 224, 230)

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


def measure(d, text, size):
    total = 0.0
    for s, c in runs(text):
        f = font(FONT_CJK if c else FONT_MATH, size)
        total += d.textlength(s, font=f)
    return total


def rich(d, xy, text, size, fill, anchor='la'):
    segs = runs(text)
    total = measure(d, text, size)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for s, c in segs:
        f = font(FONT_CJK if c else FONT_MATH, size)
        d.text((x, y), s, font=f, fill=fill, anchor='l' + anchor[1])
        x += d.textlength(s, font=f)


def ser(d, xy, parts, size, anchor='la'):
    """parts: [(kind, text, color)]，kind 取 b（正体）/ s（下标）/ p（上标）。"""
    x, y = xy
    widths = []
    for kind, text, _col in parts:
        if kind in ('s', 'p'):
            f = font(FONT_MATH, int(size * 0.60))
        else:
            f = font(FONT_MATH, size)
        widths.append((f, d.textlength(text, font=f)))
    total = sum(w for _f, w in widths)
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for (kind, text, col), (f, w) in zip(parts, widths):
        dy = 0
        if kind == 's':
            dy = size * 0.30
        elif kind == 'p':
            dy = -size * 0.36
        d.text((x, y + dy), text, font=f, fill=col, anchor='l' + anchor[1])
        x += w
    return x


def term(col, coef, sb, power=None):
    """c₋₃(z − z0)⁻³ 或 c₀ 这种一项。"""
    parts = [('b', coef, col)]
    if sb is not None:
        parts.append(('s', sb, col))
    if power is not None:
        parts += [('b', '(z − z', col), ('s', '0', col), ('b', ')', col),
                  ('p', power, col)]
    return parts


def row_series(d, x, y, chunks, size):
    """chunks: [(parts)]，用 ' + ' 连接，末尾补 ⋯（末尾已在 chunks 里给出时不补）。"""
    for i, parts in enumerate(chunks):
        if i:
            x = ser(d, (x, y), [('b', ' + ', INK)], size)
        x = ser(d, (x, y), parts, size)
    return x


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 20), '负幂项有几个，奇点就是哪一类', 32, DEEP, anchor='ma')
rich(d, (W / 2, 68),
     'f 在 0 < |z − z₀| < R 内的洛朗展开，只看 (z − z₀) 的负幂项',
     23, GREY, anchor='ma')

TOP, ROW_H, GAP = 116, 196, 14
Z0 = ('0',)

rows = [
    dict(name='可去奇点', badge='负幂项：0 个', color=BLUE,
         eg=['例 sin z / z', '在 z = 0 处'],
         note='主部是空的：级数里没有负幂项，最“坏”的一项就是常数 c₀。',
         verdict=['lim f(z) 存在且有限，等于 c₀；补上 f(z₀) 之后在 z₀ 解析；',
                  '留数恒为 0，阶数按 0 阶看。']),
    dict(name='m 阶极点', badge='负幂项：到 (z − z₀) 的 −m 次为止', color=AMBER,
         eg=['例 1/(z + 2)²', '在 z = −2 处，2 阶'],
         note='这里画的是 m = 3：负幂项到 (z − z₀) 的 −3 次就断了，再往上是正幂次。',
         verdict=['f(z) 的模无限增大；最高的那一次负幂决定阶数 m；',
                  '留数取 c₋₁ 这一项，m ≥ 2 时还要求 m − 1 阶导。']),
    dict(name='本性奇点', badge='负幂项：无限多个', color=RED,
         eg=['例 sin(1/z)', '在 z = 0 处'],
         note='负幂项永远列不完，幂次一次比一次低，阶数无从谈起。',
         verdict=['lim f(z) 不存在，沿不同路径可以差得任意远；',
                  '极点那套留数公式在这里不能用。']),
]

series_chunks = [
    [term(INK, 'c', '0', None),
     term(INK, 'c', '1', '1'),
     term(INK, 'c', '2', '2'),
     [('b', '⋯', GREY)]],
    [term(RED, 'c', '−3', '−3'),
     term(RED, 'c', '−2', '−2'),
     term(RED, 'c', '−1', '−1'),
     term(INK, 'c', '0', None),
     term(INK, 'c', '1', '1'),
     [('b', '⋯', GREY)]],
    [[('b', '⋯', GREY)],
     term(RED, 'c', '−3', '−3'),
     term(RED, 'c', '−2', '−2'),
     term(RED, 'c', '−1', '−1'),
     term(INK, 'c', '0', None),
     [('b', '⋯', GREY)]],
]

for i, r in enumerate(rows):
    y0 = TOP + i * (ROW_H + GAP)
    d.rounded_rectangle((40, y0, W - 40, y0 + ROW_H), radius=14,
                        fill=PANEL, outline=FRAME, width=2)
    d.rounded_rectangle((40, y0 + 12, 48, y0 + ROW_H - 12), radius=4,
                        fill=r['color'])
    rich(d, (74, y0 + 24), r['name'], 30, r['color'])
    rich(d, (74, y0 + 76), r['badge'], 20, GREY)
    for j, line in enumerate(r['eg']):
        rich(d, (74, y0 + 118 + j * 30), line, 21, (88, 88, 88))

    sx, sy = 400, y0 + 30
    x = ser(d, (sx, sy), [('b', 'f(z) = ', INK)], 27)
    row_series(d, x, sy, series_chunks[i], 27)
    rich(d, (sx, sy + 66), r['note'], 22, GREY)
    for j, line in enumerate(r['verdict']):
        rich(d, (sx, sy + 108 + j * 32), line, 22, INK if j == 0 else (86, 86, 86))

rich(d, (40, TOP + 3 * (ROW_H + GAP) + 6),
     '数负幂项：一个都没有是可去奇点，有限多个、最高的到 −m 次是 m 阶极点，无限多个是本性奇点。',
     23, DEEP)
rich(d, (40, TOP + 3 * (ROW_H + GAP) + 44),
     '三类各有各的极限行为：可去奇点极限有限，极点极限是无穷，本性奇点的极限不存在。',
     23, GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
