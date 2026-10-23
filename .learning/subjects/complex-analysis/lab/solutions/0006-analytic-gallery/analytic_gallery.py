"""解析函数画廊 · 第二块（参考解）：模—辐角对照 + 柯西-黎曼条件的数值检验。

把本文件拷进 `lab/0006-analytic-gallery/` 覆盖同名文件，
`python test_analytic_gallery.py` 就是全绿。只 import 标准库（numpy 只在第 10 步里临时 import），
所以单独拷这一个文件就够，不依赖任务目录里的任何东西。
"""

import cmath
import csv
import math

# 扫描窗口与分辨率：默认这块正方形，31 × 21 个格点（含边界）
RE_MIN, RE_MAX = -1.5, 1.5
IM_MIN, IM_MAX = -1.5, 1.5
DEFAULT_SIZE = (31, 21)

DEFAULT_H = 1e-6      # 一阶中心差分的步长（与第 5 课同一个值）
DEFAULT_TOL = 1e-4    # 判「残差约等于 0」的容差

SUMMARY_HEADER = ("func", "n_total", "n_cr", "fraction", "max_resid")


# ══ 样板一：像素下标 <-> 复平面坐标（与实验一 gallery.py 逐字相同）══
def pixel_to_re(col, width, re_min=RE_MIN, re_max=RE_MAX):
    """第 col 列（0 .. width-1，从左到右）对应的实部。"""
    if width < 2:
        raise ValueError("width 至少为 2，否则公式里除的是 0")
    return re_min + (re_max - re_min) * col / (width - 1)


def pixel_to_im(row, height, im_min=IM_MIN, im_max=IM_MAX):
    """第 row 行（0 .. height-1，**第 0 行是最下面那一行**）对应的虚部。"""
    if height < 2:
        raise ValueError("height 至少为 2，否则公式里除的是 0")
    return im_min + (im_max - im_min) * row / (height - 1)


# ══ 样板二：数值偏导与 CR 残差（第 5 课 cr_tool.py 里那几个）════════
def d_dx(f, z, h=DEFAULT_H):
    """沿 x 方向的一阶偏导 ∂f/∂x（中心差分），返回复数 u_x + i v_x。"""
    return (f(z + h) - f(z - h)) / (2 * h)


def d_dy(f, z, h=DEFAULT_H):
    """沿 y 方向的一阶偏导 ∂f/∂y（中心差分），返回复数 u_y + i v_y。"""
    return (f(z + 1j * h) - f(z - 1j * h)) / (2 * h)


def cr_residual(f, z, h=DEFAULT_H):
    """柯西-黎曼条件的两条残差 (r1, r2)：r1 = u_x - v_y，r2 = u_y + v_x。"""
    dx, dy = d_dx(f, z, h), d_dy(f, z, h)
    return (dx.real - dy.imag, dy.real + dx.imag)


def cr_holds(f, z, tol=DEFAULT_TOL, h=DEFAULT_H):
    """这一点满足柯西-黎曼条件吗（两条残差都在容差内才算）。"""
    r1, r2 = cr_residual(f, z, h)
    return abs(r1) <= tol and abs(r2) <= tol


# ══ 画廊里的六个函数 ════════════════════════════════════════════
def f_exp(z):
    return cmath.exp(z)


def f_sin(z):
    return cmath.sin(z)


def f_sq(z):
    return z * z


def f_conj(z):
    return z.conjugate()


def f_mod_sq(z):
    return abs(z) ** 2


def f_log(z):
    """主值 Ln z：cmath.log 就是它。z = 0 会抛 ValueError，负实轴就是割线。"""
    return cmath.log(z)


# (文件名里的 slug, 图上/表里显示的名字, 函数)
GALLERY = [
    ("exp", "e^z", f_exp),
    ("sin", "sin z", f_sin),
    ("sq", "z^2", f_sq),
    ("conj", "z̄", f_conj),
    ("modsq", "|z|^2", f_mod_sq),
    ("log", "Ln z", f_log),
]


# ══ 第 1 步 ═════════════════════════════════════════════════════
def scan_window(re_min, re_max, im_min, im_max, width, height):
    """把一块矩形窗口铺成 width * height 个复数点，按「一行行往下」展平。"""
    return [complex(pixel_to_re(col, width, re_min, re_max),
                    pixel_to_im(row, height, im_min, im_max))
            for row in range(height)
            for col in range(width)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def cr_scan(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """逐点检验 CR，返回与 points 等长的 bool 列表（保持传入顺序）。"""
    return [cr_holds(f, z, tol, h) for z in points]


# ══ 第 3 步 ═════════════════════════════════════════════════════
def analytic_fraction(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """CR 成立的点占多大比例（0.0 ~ 1.0）；空点集返回 0.0。"""
    if not points:
        return 0.0
    hits = sum(1 for ok in cr_scan(f, points, tol, h) if ok)
    return hits / len(points)


# ══ 第 4 步 ═════════════════════════════════════════════════════
def residual_map(f, re_min, re_max, im_min, im_max, width, height, h=DEFAULT_H):
    """残差图：每格一个数 max(|r1|, |r2|)，形状 height 行 × width 列，第 0 行是 im_min。"""
    points = scan_window(re_min, re_max, im_min, im_max, width, height)
    values = [max(abs(r1), abs(r2)) for r1, r2 in
              (cr_residual(f, z, h) for z in points)]
    return [values[row * width:(row + 1) * width] for row in range(height)]


# ══ 第 5 步 ═════════════════════════════════════════════════════
def grad_u_v(f, z, h=DEFAULT_H):
    """u 与 v 的梯度：返回 ((u_x, u_y), (v_x, v_y))。"""
    dx, dy = d_dx(f, z, h), d_dy(f, z, h)
    return ((dx.real, dy.real), (dx.imag, dy.imag))


# ══ 第 6 步 ═════════════════════════════════════════════════════
def orthogonality(f, z, h=DEFAULT_H):
    """两个法向量夹角的余弦：0 就是 90°（两组等值线正交）。零向量时返回 None。"""
    (ux, uy), (vx, vy) = grad_u_v(f, z, h)
    nu, nv = math.hypot(ux, uy), math.hypot(vx, vy)
    if nu == 0.0 or nv == 0.0:
        return None
    return (ux * vx + uy * vy) / (nu * nv)


# ══ 第 7 步 ═════════════════════════════════════════════════════
def jacobian(f, z, h=DEFAULT_H):
    """u_x·v_y - u_y·v_x：解析函数为正，反解析函数为负。"""
    (ux, uy), (vx, vy) = grad_u_v(f, z, h)
    return ux * vy - uy * vx


# ══ 第 8 步 ═════════════════════════════════════════════════════
def save_summary_csv(path, rows, header=SUMMARY_HEADER):
    """把六个函数的对照结论写成一张表：一行一个函数，第一行是表头。返回数据行数。"""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for name, n_total, n_cr, fraction, max_resid in rows:
            writer.writerow([name, int(n_total), int(n_cr),
                             "{:.4f}".format(float(fraction)),
                             "{:.6g}".format(float(max_resid))])
    return len(rows)


# ══ 第 9 步 ═════════════════════════════════════════════════════
def save_grid_csv(path, grid):
    """把残差图写成 CSV：一行一个像素行，不写表头，每格用 "{:.6g}" 写。返回 (行数, 列数)。"""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        for line in grid:
            writer.writerow(["{:.6g}".format(float(v)) for v in line])
    return (rows, cols)


# ══ 第 10 步（可选，有 numpy 才跑）════════════════════════════════
def residual_map_np(f_np, re_min, re_max, im_min, im_max, width, height, h=DEFAULT_H):
    """第 4 步的向量化版，与 residual_map 逐格相同。"""
    import numpy as np

    re = np.array([pixel_to_re(col, width, re_min, re_max) for col in range(width)])
    im = np.array([pixel_to_im(row, height, im_min, im_max) for row in range(height)])
    c = re[None, :] + 1j * im[:, None]              # 形状 (高, 宽)
    dx = (f_np(c + h) - f_np(c - h)) / (2 * h)
    dy = (f_np(c + 1j * h) - f_np(c - 1j * h)) / (2 * h)
    r1 = dx.real - dy.imag
    r2 = dy.real + dx.imag
    return np.maximum(np.abs(r1), np.abs(r2)).tolist()
