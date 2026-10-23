#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变函数图像画廊 · 第四块：围道、极点、留数（参考解）

与 `lab/0015-contour-residue/contour_residue.py` 逐格对应：十处留白全填好。
拷进任务目录（覆盖同名文件）后 `python test_contour_residue.py` 应当全绿。

每一格为什么这样写、常见错法、实测值，见同目录的 README.md。
只用标准库（`cmath` / `csv` / `math` / `os`），不装任何包。
"""

import cmath
import csv
import math
import os

CONTOUR_N = 2048        # 数值围道积分的采样点数
ART_N = 180             # 字符画上画圆圈用多少个点（只为看图，不求积）
TOL_AGREE = 1e-6        # 「数值积分 == 2πiΣ留数」的容差
TAU = 2j * math.pi      # 2πi

PANEL1 = (1 + 1j, 5)
ARG_WINDOW = (-1.0, 1.0, -1.0, 1.0)
ARG_STEPS = 5
GRID_LINES = (0.25, 0.5, 0.75, 1.0)
GRID_POINTS = 6

PI = math.pi


# ══ 被积函数与配方（给好，不用填）════════════════════════════════════
def f_cubic(z):
    """f(z) = 1/((z+1)(z+2)^2)。"""
    return 1 / ((z + 1) * (z + 2) ** 2)


def f_double(z):
    """f(z) = e^z/((z−πi)(z−2πi)^2)。"""
    return cmath.exp(z) / ((z - 1j * PI) * (z - 2j * PI) ** 2)


POLES_CUBIC = [(-1 + 0j, 1 + 0j), (-2 + 0j, -1 + 0j)]
POLES_DOUBLE = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - 1j * PI) / PI ** 2)]

SPECIMENS = [
    ('S1 · 1/((z+1)(z+2)²) 沿 |z|=3', f_cubic, POLES_CUBIC, 0j, 3.0),
    ('S2 · e^z/((z−πi)(z−2πi)²) 沿 |z|=8', f_double, POLES_DOUBLE, 0j, 8.0),
    ('S3 · 同 S2 换成 |z|=4：2πi 落在圈外', f_double, POLES_DOUBLE, 0j, 4.0),
    ('S4 · 同 S2 换成 |z|=2：两个都落在圈外', f_double, POLES_DOUBLE, 0j, 2.0),
    ('S5 · S2 只列一个奇点（故意错的那一版）', f_double, POLES_DOUBLE[:1], 0j, 8.0),
]


def arg_degrees(z):
    """（给好）辐角主值换成 [0,360) 的度数。"""
    return math.degrees(cmath.phase(z)) % 360


def write_csv(out_dir, filename, header, rows):
    """（给好）把一份面板数据写成 CSV，返回数据行数（不含表头）。"""
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, filename), 'w',
              encoding='utf-8', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for row in rows:
            writer.writerow(['{:.6g}'.format(v) if isinstance(v, float) else v
                             for v in row])
    return len(rows)


# ══ 第 1 步 ═════════════════════════════════════════════════════
def nth_roots(z0, n):
    """z0 的全部 n 次方根，k = 0, 1, …, n−1 的顺序。"""
    radius = abs(z0) ** (1 / n)
    theta0 = cmath.phase(z0)
    return [radius * cmath.exp(1j * (theta0 + 2 * math.pi * k) / n)
            for k in range(n)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def segment_points(a, b, n):
    """线段 a → b 上等距的 n 个点（含两端）。"""
    if n < 2:
        raise ValueError('一条线段至少要 2 个点，收到的是 n = {}'.format(n))
    return [a + (b - a) * k / (n - 1) for k in range(n)]


# ══ 第 3 步 ═════════════════════════════════════════════════════
def circle_contour(center, radius, n=CONTOUR_N):
    """正向圆周上等距的 n 个点，首点不重复写进末尾。"""
    return [center + radius * cmath.exp(1j * 2 * math.pi * k / n)
            for k in range(n)]


# ══ 第 4 步 ═════════════════════════════════════════════════════
def contour_integral(f, center, radius, n=CONTOUR_N):
    """数值围道积分 ∮ f dz，dz 取 i·Δθ·(z − center)。"""
    dtheta = 2 * math.pi / n
    total = 0j
    for z in circle_contour(center, radius, n):
        total += f(z) * (1j * dtheta * (z - center))
    return total


# ══ 第 5 步 ═════════════════════════════════════════════════════
def inside(z0, center, radius):
    """奇点在围道内部吗（边界不算）。"""
    return abs(z0 - center) < radius


# ══ 第 6 步 ═════════════════════════════════════════════════════
def residue_theorem(poles, center, radius):
    """留数定理右边：2πi 乘圈内留数之和。"""
    total = sum(res for z0, res in poles if inside(z0, center, radius))
    return TAU * total


# ══ 第 7 步 ═════════════════════════════════════════════════════
def ledger_row(name, f, poles, center, radius, n=CONTOUR_N):
    """账本里的一行：数值围道积分与 2πiΣ留数并排。"""
    numeric = contour_integral(f, center, radius, n)
    theorem = residue_theorem(poles, center, radius)
    gap = abs(numeric - theorem)
    return {
        'case': name,
        'enclosed': sum(1 for z0, _ in poles if inside(z0, center, radius)),
        'numeric': numeric,
        'theorem': theorem,
        'gap': gap,
        'verdict': '一致' if gap <= TOL_AGREE else '不一致',
    }


def ledger_rows(n=CONTOUR_N):
    """（给好）五个配方各算一行。"""
    return [ledger_row(name, f, poles, center, radius, n)
            for name, f, poles, center, radius in SPECIMENS]


# ══ 第 8 步 ═════════════════════════════════════════════════════
def save_contour_csv(path, center, radius, poles, n=ART_N):
    """围道点 + 极点标记存成 CSV，返回数据行数。"""
    rows = [['contour', k, z.real, z.imag, '']
            for k, z in enumerate(circle_contour(center, radius, n))]
    rows += [['pole', k, z0.real, z0.imag,
              '圈内' if inside(z0, center, radius) else '圈外']
             for k, (z0, _) in enumerate(poles)]
    out_dir = os.path.dirname(path) or '.'
    return write_csv(out_dir, os.path.basename(path),
                     ('kind', 'index', 're', 'im', 'mark'), rows)


# ══ 第 9 步 ═════════════════════════════════════════════════════
def write_gallery(out_dir):
    """四块面板写进同一份 out/，返回画廊总表的四行。"""
    rows = []

    roots = nth_roots(*PANEL1)
    rows.append(('panel1-roots', 'panel1-roots.csv',
                 write_csv(out_dir, 'panel1-roots.csv', ('k', 're', 'im'),
                           [(k, z.real, z.imag) for k, z in enumerate(roots)]),
                 '五个五次方根落成正五边形'))

    re0, re1, im0, im1 = ARG_WINDOW
    arg_pts = [complex(re0 + (re1 - re0) * i / (ARG_STEPS - 1),
                       im0 + (im1 - im0) * j / (ARG_STEPS - 1))
               for j in range(ARG_STEPS) for i in range(ARG_STEPS)]
    rows.append(('panel2-arg', 'panel2-arg.csv',
                 write_csv(out_dir, 'panel2-arg.csv', ('re', 'im', 'arg_deg'),
                           [(z.real, z.imag, arg_degrees(z)) for z in arg_pts]),
                 '辐角着色：颜色绕原点转一圈'))

    grid = []
    for line, x in enumerate(GRID_LINES):
        for k, z in enumerate(segment_points(complex(x, -1.0),
                                             complex(x, 1.0), GRID_POINTS)):
            w = z * z
            grid.append((line, k, w.real, w.imag))
    rows.append(('panel3-grid', 'panel3-grid.csv',
                 write_csv(out_dir, 'panel3-grid.csv', ('line', 'k', 're', 'im'), grid),
                 'z^2 把四条竖线送成抛物线'))

    n_contour = save_contour_csv(os.path.join(out_dir, 'panel4-contour.csv'),
                                 0j, 8.0, POLES_DOUBLE, ART_N)
    rows.append(('panel4-contour', 'panel4-contour.csv', n_contour,
                 '围道 |z|=8 与两个奇点都在圈内'))

    write_csv(out_dir, 'gallery.csv', ('panel', 'file', 'rows', 'note'), rows)
    return rows


# ══ 第 10 步 ════════════════════════════════════════════════════
def ascii_canvas(center, radius, poles, width=41, height=21):
    """围道与极点的字符画：`.` 围道、`*` 圈内极点、`o` 圈外极点。"""
    pts = circle_contour(center, radius, ART_N)
    xs = [z.real for z in pts] + [z0.real for z0, _ in poles]
    ys = [z.imag for z in pts] + [z0.imag for z0, _ in poles]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)

    def cells(z):
        col = int(round((z.real - x0) / (x1 - x0) * (width - 1)))
        row = height - 1 - int(round((z.imag - y0) / (y1 - y0) * (height - 1)))
        return row, col

    canvas = [[' '] * width for _ in range(height)]
    for z in pts:
        row, col = cells(z)
        canvas[row][col] = '.'
    for z0, _ in poles:
        row, col = cells(z0)
        canvas[row][col] = '*' if inside(z0, center, radius) else 'o'
    return [''.join(line) for line in canvas]
