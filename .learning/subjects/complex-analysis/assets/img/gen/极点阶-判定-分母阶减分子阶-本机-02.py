# -*- coding: utf-8 -*-
"""产图脚本：极点阶的判定——数分母与分子的零点阶，再用极限核对。

输出：assets/img/pool/极点阶-分母阶减分子阶-本机-02.png
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '极点阶-分母阶减分子阶-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 1004
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (120, 120, 120)
DEEP = (26, 78, 140)
BLUE = (32, 105, 190)
RED = (190, 55, 45)
AMBER = (163, 112, 18)
GREEN = (28, 120, 96)
PANEL = (247, 249, 252)
FRAME = (219, 224, 230)
LINE = (226, 231, 237)
WHITE = (255, 255, 255)

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


def draw_text(d, x, y, text, size, fill):
    """中英数混排：中文走 msyh，其余走 cambria；返回右端 x。"""
    for s, c in runs(text):
        f = font(FONT_CJK if c else FONT_MATH, size)
        d.text((x, y), s, font=f, fill=fill, anchor='la')
        x += d.textlength(s, font=f)
    return x


def measure_text(d, text, size):
    total = 0.0
    for s, c in runs(text):
        f = font(FONT_CJK if c else FONT_MATH, size)
        total += d.textlength(s, font=f)
    return total


def rich(d, xy, text, size, fill, anchor='la'):
    x, y = xy
    total = measure_text(d, text, size)
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    draw_text(d, x, y, text, size, fill)


def seq(d, xy, parts, size, anchor='la'):
    """parts: [(kind, text, color)]，kind 取 b（正文，中英混排）/ s（下标）/ p（上标）。"""
    x, y = xy
    widths = []
    for kind, text, _col in parts:
        if kind in ('s', 'p'):
            widths.append(d.textlength(text, font=font(FONT_MATH, int(size * 0.60))))
        else:
            widths.append(measure_text(d, text, size))
    total = sum(widths)
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    for (kind, text, col), w in zip(parts, widths):
        if kind in ('s', 'p'):
            f = font(FONT_MATH, int(size * 0.60))
            dy = size * 0.30 if kind == 's' else -size * 0.36
            d.text((x, y + dy), text, font=f, fill=col, anchor='la')
        else:
            draw_text(d, x, y, text, size, col)
        x += w
    return x


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 20), '极点的阶：分母的零点阶减去分子的零点阶', 32, DEEP, anchor='ma')
rich(d, (W / 2, 68),
     '卷面上那句「求出极点的阶」，落到纸上就是数两个阶、再用一条极限核对',
     23, GREY, anchor='ma')

# ── 左栏：四步 ───────────────────────────────────────────────
LX0, LX1 = 40, 600
BX0, BX1 = 58, LX1 - 18
steps = [
    ('①  找奇点',
     [('b', '分母 = 0 的根 z₀ 就是奇点', INK)]),
    ('②  数分母的零点阶 n',
     [('b', '分母 = (z − z₀)', INK), ('p', 'n', INK),
      ('b', '·φ(z)，且 φ(z₀) ≠ 0', INK)]),
    ('③  数分子的零点阶 k',
     [('b', '分子在同一个 z₀ 也有零点阶 k，可能是 0', INK)]),
    ('④  相减得阶数',
     [('b', 'n − k 是几，z₀ 就是几阶极点', INK)]),
]

STEP_Y0, STEP_H, STEP_GAP = 116, 112, 22
for i, (title, body) in enumerate(steps):
    y0 = STEP_Y0 + i * (STEP_H + STEP_GAP)
    d.rounded_rectangle((BX0, y0, BX1, y0 + STEP_H), radius=12,
                        fill=PANEL, outline=FRAME, width=2)
    d.rounded_rectangle((BX0, y0 + 10, BX0 + 6, y0 + STEP_H - 10), radius=3, fill=BLUE)
    rich(d, (BX0 + 22, y0 + 16), title, 25, DEEP)
    seq(d, (BX0 + 22, y0 + 58), body, 21)
    if i < len(steps) - 1:
        cx = (BX0 + BX1) // 2
        ay = y0 + STEP_H + 4
        d.line([(cx, ay), (cx, ay + 16)], fill=LINE, width=3)
        d.polygon([(cx - 6, ay + 16), (cx + 6, ay + 16), (cx, ay + 25)], fill=LINE)

# ── 右栏上：n − k 的三种正负 ────────────────────────────────
RX0, RX1 = 620, 1200
d.rounded_rectangle((RX0, 116, RX1, 368), radius=12, fill=PANEL, outline=FRAME, width=2)
rich(d, (RX0 + 22, 132), 'n − k 的正负决定结论', 25, DEEP)

branches = [
    ('n − k > 0', 'z₀ 是 n − k 阶极点', AMBER),
    ('n − k = 0', 'z₀ 是可去奇点，留数 0', BLUE),
    ('n − k < 0', 'z₀ 是零点，本来就不是奇点', GREEN),
]
for i, (cond, concl, col) in enumerate(branches):
    y = 184 + i * 58
    d.rounded_rectangle((RX0 + 22, y, RX1 - 22, y + 46), radius=8,
                        fill=WHITE, outline=FRAME, width=1)
    seq(d, (RX0 + 38, y + 10), [('b', cond, col)], 23)
    rich(d, (RX0 + 178, y + 11), concl, 21, INK)

# ── 右栏下：极限判别 ────────────────────────────────────────
d.rounded_rectangle((RX0, 388, RX1, 620), radius=12, fill=PANEL, outline=FRAME, width=2)
rich(d, (RX0 + 22, 404), '极限判别：用一条极限核对阶数', 25, DEEP)
rich(d, (RX0 + 24, 452), 'lim', 23, INK)
rich(d, (RX0 + 24, 474), 'z → z₀', 15, GREY)
seq(d, (RX0 + 108, 452), [('b', '(z − z₀)', INK), ('p', 'm', INK),
                          ('b', ' f(z) = c', INK)], 23)

lim_rows = [
    ('c 是有限非零常数', 'z₀ 就是 m 阶极点', AMBER),
    ('c = 0', '真实阶数比 m 低', BLUE),
    ('c 是无穷大', '真实阶数比 m 高', GREY),
]
for i, (cond, concl, col) in enumerate(lim_rows):
    y = 498 + i * 40
    rich(d, (RX0 + 46, y), cond, 21, col)
    rich(d, (RX0 + 248, y), '→ ' + concl, 21, INK)

# ── 底部：例子表 ─────────────────────────────────────────────
COLS = [58, 330, 440, 610, 780]
HEAD = ['f(z)', '奇点 z₀', '分母阶 n', '分子阶 k', '结论']
ROWS = [
    ['sin z / z³', '0', '3', '1', '2 阶极点'],
    ['sin z / (z − π)²', 'π', '2', '1', '1 阶极点'],
    ['(z² − π²)/(z sin z)', '0', '2', '0', '2 阶极点'],
    ['(z² − π²)/(z sin z)', 'π', '1', '1', '可去奇点'],
]
FUNCS = [
    [('b', 'sin z / z', INK), ('p', '3', INK)],
    [('b', 'sin z / (z − π)', INK), ('p', '2', INK)],
    [('b', '(z', INK), ('p', '2', INK), ('b', ' − π', INK), ('p', '2', INK),
     ('b', ') / (z sin z)', INK)],
    [('b', '(z', INK), ('p', '2', INK), ('b', ' − π', INK), ('p', '2', INK),
     ('b', ') / (z sin z)', INK)],
]
TY = 656
d.rounded_rectangle((40, TY - 14, W - 40, TY + 226), radius=12,
                    fill=WHITE, outline=FRAME, width=2)
for j, h in enumerate(HEAD):
    rich(d, (COLS[j], TY), h, 21, GREY)
d.line([(58, TY + 34), (W - 58, TY + 34)], fill=LINE, width=2)
for i, row in enumerate(ROWS):
    y = TY + 46 + i * 44
    if i:
        d.line([(58, y - 10), (W - 58, y - 10)], fill=LINE, width=1)
    seq(d, (COLS[0], y), FUNCS[i], 22)
    for j in range(1, 4):
        rich(d, (COLS[j], y), row[j], 22, INK)
    rich(d, (COLS[4], y), row[4], 22, AMBER if '极点' in row[4] else BLUE)

rich(d, (58, TY + 246),
     '抵消掉的那些点：分子分母各数一遍阶再相减，减出 0 时卷面上写可去奇点，别写 0 阶极点。',
     22, DEEP)
rich(d, (58, TY + 288),
     '同一个函数在 0 处是二阶极点、在 ±π 处是可去奇点，两处要分开写。',
     22, GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
