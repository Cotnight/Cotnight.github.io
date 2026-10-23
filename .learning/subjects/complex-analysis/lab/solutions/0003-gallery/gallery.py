"""图像画廊 · 第一块：方根分布图 + z^2+c 迭代缩略图（参考解）。

只用标准库（cmath / csv / math）就能跑完 test_gallery.py；numpy 只给第 8 步加急用，
没装 numpy 时第 8 步会自动跳过。画图（matplotlib）不在本文件里，见 lab/README.md。
"""

import cmath
import csv
import math

# 曼德博集的经典观察窗口（复平面上的矩形）
RE_MIN, RE_MAX = -2.0, 0.5
IM_MIN, IM_MAX = -1.25, 1.25

DEFAULT_SIZE = (120, 80)      # (宽, 高)：缩略图，先看清结构再谈分辨率
DEFAULT_MAX_ITER = 60         # 迭代预算


# ---------- 样板：像素下标 <-> 复平面坐标（已经写好，别改） ----------

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


# ---------- 第 1 步 ----------

def nth_roots(z0, n):
    """z0 的全部 n 次方根，按 k = 0, 1, ..., n-1 的顺序返回。

    第 k 个根 = r * e^{i(theta + 2*pi*k)/n}，其中 r = |z0| ** (1/n)，
    theta = cmath.phase(z0)（主值，弧度，落在 (-pi, pi]）。n < 1 时抛 ValueError。
    """
    if n < 1:
        raise ValueError("n 必须是正整数")
    r = abs(z0) ** (1.0 / n)
    theta = cmath.phase(z0)
    return [r * cmath.exp(1j * (theta + 2 * math.pi * k) / n) for k in range(n)]


# ---------- 第 2 步 ----------

def arg_degrees(z):
    """辐角着色用：主值辐角换成 [0, 360) 的度数。

    cmath.phase(0) 是 0.0，所以 z = 0 得 0.0（这个点的颜色其实没有意义）。
    """
    return math.degrees(cmath.phase(z)) % 360.0


# ---------- 第 3 步 ----------

def escape_from(z0, c, max_iter):
    """从 z0 出发按 z <- z*z + c 迭代，返回逃逸步数 k。

    先把 z 迭代一次，再看模：|z_k| > 2 的第一个 k 就是返回值（k 从 1 起算）。
    判据是**严格大于 2**；max_iter 步内没逃出去，返回 max_iter。
    """
    z = z0
    for k in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > 2.0:
            return k
    return max_iter


# ---------- 第 4 步 ----------

def mandelbrot_escape(c, max_iter):
    """曼德博集：一律从 z0 = 0 出发。"""
    return escape_from(0j, c, max_iter)


def escaped(c, max_iter):
    """这个 c 在预算内逃出去了吗（True = 逃逸，不属于曼德博集）。"""
    return mandelbrot_escape(c, max_iter) < max_iter


# ---------- 第 5 步 ----------

def escape_grid(re_min, re_max, im_min, im_max, width, height, max_iter):
    """把矩形窗口铺成 width * height 个 c，逐点算逃逸步数。

    返回 grid[row][col]：row = 0 是 im_min 那一行（数学上的最下面一行），
    col = 0 是 re_min 那一列。每个格子都是整数。
    """
    grid = []
    for row in range(height):
        im = pixel_to_im(row, height, im_min, im_max)
        line = []
        for col in range(width):
            re = pixel_to_re(col, width, re_min, re_max)
            line.append(mandelbrot_escape(complex(re, im), max_iter))
        grid.append(line)
    return grid


# ---------- 第 6 步 ----------

def save_points_csv(path, points, header=("re", "im")):
    """把一串复数写成 CSV：第一行表头，之后每点一行 re,im。

    用 utf-8、newline="" 打开（不然 Windows 会多出空行）。返回写入的数据行数。
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(list(header))
        count = 0
        for z in points:
            w.writerow([repr(float(z.real)), repr(float(z.imag))])
            count += 1
    return count


def save_grid_csv(path, grid):
    """把逃逸步数网格写成 CSV：一行一个像素行，单元格是整数，不写表头。

    返回 (行数, 列数)。
    """
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for line in grid:
            w.writerow([int(v) for v in line])
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return rows, cols


# ---------- 第 8 步（有 numpy 才跑） ----------

def escape_grid_np(re_min, re_max, im_min, im_max, width, height, max_iter):
    """和 escape_grid 逐格相同的结果，只是用 numpy 复数数组向量化算。

    第 0 行同样是 im_min（最下面一行）——修坐标的时候别把上下翻过来。
    坐标直接取 pixel_to_re / pixel_to_im，和第 5 步逐格相同：改成 np.linspace 也能跑，
    但末位可能差一点点，边界上的点会翻格，跟第 5 步就对不上了。
    """
    import numpy as np

    re = np.array([pixel_to_re(col, width, re_min, re_max) for col in range(width)])
    im = np.array([pixel_to_im(row, height, im_min, im_max) for row in range(height)])
    c = re[None, :] + 1j * im[:, None]
    z = np.zeros_like(c)
    counts = np.full(c.shape, max_iter, dtype=int)
    active = np.ones(c.shape, dtype=bool)
    for k in range(1, max_iter + 1):
        z[active] = z[active] ** 2 + c[active]
        gone = active & (np.abs(z) > 2.0)
        counts[gone] = k
        active &= ~gone
        if not active.any():
            break
    return counts.tolist()
