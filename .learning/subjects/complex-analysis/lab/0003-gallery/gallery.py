"""图像画廊 · 第一块：方根分布图 + z^2+c 迭代缩略图。

这里是你要填的文件。样板（pixel_to_re / pixel_to_im）已经写好、别改；
留白的 8 个函数按 lab/README.md 的任务表一步步填，填一个就跑一次：

    python test_gallery.py -k step1

全部只用标准库（cmath / csv / math），不装任何第三方包也能跑完 test_gallery.py。
numpy 只在第 8 步加速时用，没装就跳过；matplotlib 与 Jupyter 只给 notebook 画图用，
装不装都不影响 test_gallery.py 的结论（见 lab/README.md）。
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
    raise NotImplementedError("第 1 步还没写：nth_roots —— 见 lab/README.md 任务表第 1 行")


# ---------- 第 2 步 ----------

def arg_degrees(z):
    """辐角着色用：主值辐角换成 [0, 360) 的度数。

    cmath.phase(0) 是 0.0，所以 z = 0 得 0.0（这个点的颜色其实没有意义）。
    """
    raise NotImplementedError("第 2 步还没写：arg_degrees —— 见 lab/README.md 任务表第 2 行")


# ---------- 第 3 步 ----------

def escape_from(z0, c, max_iter):
    """从 z0 出发按 z <- z*z + c 迭代，返回逃逸步数 k。

    先把 z 迭代一次，再看模：|z_k| > 2 的第一个 k 就是返回值（k 从 1 起算）。
    判据是**严格大于 2**；max_iter 步内没逃出去，返回 max_iter。
    """
    raise NotImplementedError("第 3 步还没写：escape_from —— 见 lab/README.md 任务表第 3 行")


# ---------- 第 4 步 ----------

def mandelbrot_escape(c, max_iter):
    """曼德博集：一律从 z0 = 0 出发。"""
    raise NotImplementedError("第 4 步还没写：mandelbrot_escape —— 见 lab/README.md 任务表第 4 行")


def escaped(c, max_iter):
    """这个 c 在预算内逃出去了吗（True = 逃逸，不属于曼德博集）。"""
    raise NotImplementedError("第 4 步还没写：escaped —— 见 lab/README.md 任务表第 4 行")


# ---------- 第 5 步 ----------

def escape_grid(re_min, re_max, im_min, im_max, width, height, max_iter):
    """把矩形窗口铺成 width * height 个 c，逐点算逃逸步数。

    返回 grid[row][col]：row = 0 是 im_min 那一行（数学上的最下面一行），
    col = 0 是 re_min 那一列。每个格子都是整数。
    """
    raise NotImplementedError("第 5 步还没写：escape_grid —— 见 lab/README.md 任务表第 5 行")


# ---------- 第 6 步 ----------

def save_points_csv(path, points, header=("re", "im")):
    """把一串复数写成 CSV：第一行表头，之后每点一行 re,im。

    用 utf-8、newline="" 打开（不然 Windows 会多出空行）。返回写入的数据行数。
    """
    raise NotImplementedError("第 6 步还没写：save_points_csv —— 见 lab/README.md 任务表第 6 行")


def save_grid_csv(path, grid):
    """把逃逸步数网格写成 CSV：一行一个像素行，单元格是整数，不写表头。

    返回 (行数, 列数)。
    """
    raise NotImplementedError("第 6 步还没写：save_grid_csv —— 见 lab/README.md 任务表第 6 行")


# ---------- 第 8 步（有 numpy 才跑） ----------

def escape_grid_np(re_min, re_max, im_min, im_max, width, height, max_iter):
    """和 escape_grid 逐格相同的结果，只是用 numpy 复数数组向量化算。

    第 0 行同样是 im_min（最下面一行）——修坐标的时候别把上下翻过来。
    坐标直接取 pixel_to_re / pixel_to_im，和第 5 步逐格相同：改成 np.linspace 也能跑，
    但末位可能差一点点，边界上的点会翻格，跟第 5 步就对不上了。
    """
    raise NotImplementedError("第 8 步还没写：escape_grid_np —— 见 lab/README.md 任务表第 8 行")
