# -*- coding: utf-8 -*-
"""产图脚本：洛朗级数的两半——负幂项（主要部分）与非负幂项（解析部分）。

上半：把项按指数排开。n < 0 的项是洛朗级数独有的部分（主要部分），n ≥ 0 的项就是泰勒级数那一半。
下半：c_{-1} 单独提出来——系数公式里 n = -1 时分母正好是 1，于是
      ∮_C f dz = 2πi·c_{-1}；在 0 < |z - z0| < R 这样的环域里它就是留数。

输出：assets/img/pool/洛朗-级数-负幂项与主要部分-本机-02.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(
    HERE, '..', 'pool', '洛朗-级数-负幂项与主要部分-本机-02.png'))
FONT_CJK = r'C:\Windows\Fonts\msyh.ttc'
FONT_MATH = r'C:\Windows\Fonts\cambria.ttc'

W, H = 1240, 760
BG = (255, 255, 255)
INK = (32, 32, 32)
GREY = (110, 110, 110)
FRAME = (200, 200, 200)
BLUE = (32, 105, 190)
ORANGE = (196, 92, 24)
RED = (176, 42, 42)
GREEN = (24, 120, 84)
FILL_NEG = (253, 242, 228)
FILL_POS = (232, 243, 253)

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


def split_markup(text):
    segs = []
    i = 0
    while i < len(text):
        if text.startswith('_{', i) or text.startswith('^{', i):
            j = text.index('}', i)
            segs.append((text[i + 2:j], text[i]))
            i = j + 1
        else:
            nxt = [k for k in (text.find('_{', i), text.find('^{', i)) if k >= 0]
            j = min(nxt) if nxt else len(text)
            segs.append((text[i:j], None))
            i = j
    return segs


def seg_font(mark, size):
    sub = int(round(size * 0.72))
    return font(FONT_MATH, sub if mark else size)


def math(d, xy, text, size, fill, anchor='la'):
    """画一段混排：中文走 msyh，其余走 cambria；_{}/^{} 分别画成下／上标。"""
    segs = split_markup(text)
    widths = []
    for s, mark in segs:
        f = seg_font(mark, size)
        for part, is_cjk_part in runs(s):
            if is_cjk_part:
                f = font(FONT_CJK, int(round(size * 0.72)) if mark else size)
            else:
                f = seg_font(mark, size)
            widths.append(d.textlength(part, font=f))
        if not s:
            widths.append(0.0)
    total = sum(widths)
    x, y = xy
    if anchor[0] == 'm':
        x -= total / 2
    elif anchor[0] == 'r':
        x -= total
    k = 0
    for s, mark in segs:
        dy = size * 0.28 if mark == '_' else (-size * 0.30 if mark == '^' else 0)
        for part, is_cjk_part in runs(s):
            f = font(FONT_CJK, int(round(size * 0.72)) if mark else size) \
                if is_cjk_part else seg_font(mark, size)
            d.text((x, y + dy), part, font=f, fill=fill, anchor='l' + anchor[1])
            x += widths[k]
            k += 1
    return total


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


def term_box(d, box, text, size, border, fill, hi=False):
    d.rounded_rectangle(box, radius=8, fill=fill,
                        outline=RED if hi else border,
                        width=4 if hi else 2)
    math(d, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 - size * 0.62),
         text, size, RED if hi else INK, anchor='ma')


img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

rich(d, (W / 2, 26), '洛朗级数把项按指数排开：负幂那一半是新的', 30, INK, anchor='ma')

# ---------------- 主要部分 ----------------
rich(d, (60, 92), '主要部分：n < 0 的项（负幂项）', 27, ORANGE, anchor='la')
term_box(d, (60, 128, 168, 200), '…', 26, ORANGE, FILL_NEG)
term_box(d, (186, 128, 452, 200), 'c_{−2}/(z − z_{0})²', 26, ORANGE, FILL_NEG)
term_box(d, (470, 128, 736, 200), 'c_{−1}/(z − z_{0})', 26, ORANGE, FILL_NEG, hi=True)
rich(d, (60, 212),
     '环域里有奇点，才长出这一半；这一半有几项，决定奇点属哪一类。',
     25, GREY, anchor='la')

# ---------------- 解析部分 ----------------
rich(d, (60, 268), '解析部分：n ≥ 0 的项', 27, BLUE, anchor='la')
term_box(d, (60, 304, 200, 376), 'c_{0}', 26, BLUE, FILL_POS)
term_box(d, (218, 304, 452, 376), 'c_{1}(z − z_{0})', 26, BLUE, FILL_POS)
term_box(d, (470, 304, 736, 376), 'c_{2}(z − z_{0})²', 26, BLUE, FILL_POS)
term_box(d, (754, 304, 862, 376), '…', 26, BLUE, FILL_POS)
math(d, (60, 388),
     '这一半在整块圆盘 |z − z_{0}| < R 里收敛；只留下它，洛朗级数就退成泰勒级数。',
     25, GREY, anchor='la')

d.line([(60, 442), (1180, 442)], fill=FRAME, width=2)

# ---------------- c_{-1} 的两个说法 ----------------
d.rounded_rectangle((60, 470, 606, 706), radius=10, outline=RED, width=3)
math(d, (82, 486), 'c_{−1} 这一项单独能用', 27, RED, anchor='la')
math(d, (82, 528), '绕 z_{0} 一圈的积分 = 2πi · c_{−1}', 27, INK, anchor='la')
math(d, (82, 574), 'C 取环域内绕 z_{0} 一圈的正向闭曲线。', 25, GREY, anchor='la')
rich(d, (82, 610), '把 n = −1 代进系数公式，分母正好是 1，', 25, GREY, anchor='la')
rich(d, (82, 640), '于是这一项就是整条闭曲线上的积分。', 25, GREY, anchor='la')

d.rounded_rectangle((634, 470, 1180, 706), radius=10, outline=GREEN, width=3)
rich(d, (656, 486), '它就是留数', 27, GREEN, anchor='la')
math(d, (656, 528), '以奇点为心的环域 0 < |z − z_{0}| < R 里，', 25, INK, anchor='la')
math(d, (656, 562), 'c_{−1} = Res[f, z_{0}]', 27, INK, anchor='la')
rich(d, (656, 606), '下一章求闭路积分，整章都在用这一个系数。', 25, GREY, anchor='la')
rich(d, (656, 640), '环域不是以奇点为心时，它等于环内各奇点之和，', 25, GREY, anchor='la')
rich(d, (656, 670), '别把两种情形混成一句话。', 25, GREY, anchor='la')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, optimize=True)
print('written', OUT, os.path.getsize(OUT), 'bytes')
