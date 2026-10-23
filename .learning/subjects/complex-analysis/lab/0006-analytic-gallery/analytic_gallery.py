"""解析函数画廊 · 第二块：模—辐角对照 + 柯西-黎曼条件的数值检验。

这是你要填的文件（实验二）。按 lab/README.md 的任务表从上到下填掉 9 处
`raise NotImplementedError`，**填一个验一个**：

    python test_analytic_gallery.py -k step1
    python test_analytic_gallery.py            # 全部（含自检）

**六个样板已经写好、别改**：

- `pixel_to_re` / `pixel_to_im`：实验一 `gallery.py` 里那两行，逐字搬来
  （跨目录 import 会让参考解不自包含，所以这里放一份自己的）；
- `d_dx` / `d_dy` / `cr_residual` / `cr_holds`：第 5 课 lab `cr_tool.py` 里你已经写过的四个。

只用标准库（`cmath` / `csv` / `math`）就能跑完 `test_analytic_gallery.py`；
numpy 只在向量化残差图那一步用，没装就跳过。
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


# ══ 样板一：像素下标 <-> 复平面坐标（与实验一 gallery.py 逐字相同，别改）══
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


# ══ 样板二：数值偏导与 CR 残差（第 5 课 cr_tool.py 里那几个，别改）════
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


# ══ 画廊里的六个函数（给好，不用填）══════════════════════════════
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
    """把一块矩形窗口铺成 width * height 个复数点，按「一行行往下」展平。

    返回 list[complex]：第 0 行是 im_min（数学上的最下面一行）、第 0 列是 re_min；
    width 或 height 小于 2 要抛 ValueError。

    提示：坐标换算走上面两个样板（pixel_to_re / pixel_to_im），别自己再写一遍公式——
    自己写的版本和它们差一个末位，第 4 步的残差图就会跟逐点算的对不上。
    """
    raise NotImplementedError('第 1 步还没写：scan_window —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def cr_scan(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """逐点检验 CR，返回与 points 等长的 bool 列表（**保持传入顺序**）。

    提示：第 5 课的 cr_points 返回的是「筛出来的点」，这里要的是「每个点成立不成立」——
    这批标签后面要拿去上色，一个点都不能丢。
    """
    raise NotImplementedError('第 2 步还没写：cr_scan —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def analytic_fraction(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """CR 成立的点占多大比例（0.0 ~ 1.0）；空点集返回 0.0。

    这个数是「点集大小」的量化版：约等于 1 才谈得上在这块区域解析，
    只有很小一点（甚至等于 0）就只是个别点可导、或者处处不解析。
    """
    raise NotImplementedError('第 3 步还没写：analytic_fraction —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def residual_map(f, re_min, re_max, im_min, im_max, width, height, h=DEFAULT_H):
    """残差图：每格一个数 max(|r1|, |r2|)，形状 height 行 × width 列。

    第 0 行同样是 im_min（最下面那一行）。这张图就是「解析性」的着色数据：
    解析的函数整片接近 0，非解析的整片是同一个非零值。

    提示：先 scan_window 铺点，再按 width 一段段切开成行——切的时候别把行序弄反。
    """
    raise NotImplementedError('第 4 步还没写：residual_map —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def grad_u_v(f, z, h=DEFAULT_H):
    """u 与 v 的梯度：返回 ((u_x, u_y), (v_x, v_y))，都是 (实部方向, 虚部方向) 的二元组。

    提示：d_dx 给的是 u_x + i·v_x，d_dy 给的是 u_y + i·v_y——实部虚部各取一次，
    四个偏导就齐了。这两个向量是模的等值线与辐角的等值线的**法向量**。
    """
    raise NotImplementedError('第 5 步还没写：grad_u_v —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def orthogonality(f, z, h=DEFAULT_H):
    """两个法向量夹角的余弦：0 就是 90°（两组等值线正交）。任一梯度是零向量时返回 None。

    提示：余弦 = 点积 / (模长 × 模长)；模长用 math.hypot。
    零向量没法归一化——那正是 |z|^2 这种「虚部恒等于 0、谈不上辐角」的情形。
    """
    raise NotImplementedError('第 6 步还没写：orthogonality —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def jacobian(f, z, h=DEFAULT_H):
    """u_x·v_y - u_y·v_x：解析函数为正（= |f'(z)|^2），反解析函数为负。

    提示：正交只说明「两组线互相垂直」，说明不了方向。z̄ 的两组线也垂直，
    但它的行列式是负的——符号才是解析与反解析的分界。
    """
    raise NotImplementedError('第 7 步还没写：jacobian —— 见 lab/README.md 任务表第 7 行')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def save_summary_csv(path, rows, header=SUMMARY_HEADER):
    """把六个函数的对照结论写成一张表：一行一个函数，第一行是表头。

    rows 里每项是 (name, n_total, n_cr, fraction, max_resid)。
    fraction 写成四位小数，max_resid 写成 "{:.6g}"。返回写入的**数据行数**（不含表头）。

    提示：open 三件套 `"w"` + `encoding="utf-8"` + `newline=""` 一个都不能省。
    """
    raise NotImplementedError('第 8 步还没写：save_summary_csv —— 见 lab/README.md 任务表第 8 行')


# ══ 第 9 步 ═════════════════════════════════════════════════════
def save_grid_csv(path, grid):
    """把残差图写成 CSV：一行一个像素行，**不写表头**，每格用 "{:.6g}" 写。

    返回 (行数, 列数)。残差量级从 1e-10 到 10 都有，所以要用科学计数法的格式，
    写死成四位小数会把 1e-10 全写成 0.0000（图就成了一片纯色）。
    """
    raise NotImplementedError('第 9 步还没写：save_grid_csv —— 见 lab/README.md 任务表第 9 行')


# ══ 第 10 步（可选，有 numpy 才跑）════════════════════════════════
def residual_map_np(f_np, re_min, re_max, im_min, im_max, width, height, h=DEFAULT_H):
    """第 4 步的向量化版：f_np 必须能吃 numpy 复数数组（np.exp / np.sin 这类）。

    与 residual_map 逐格相同（同一个窗口、同一个步长、同一套坐标换算），
    返回 list[list[float]]（形状 height 行 × width 列，第 0 行是 im_min）。

    提示：整块矩形一次铺成复数数组，形状是 (高, 宽)：
        c = re[None, :] + 1j * im[:, None]
    然后用一次数组运算算出 dx、dy，再取实部虚部凑 r1、r2。
    """
    raise NotImplementedError('第 10 步还没写：residual_map_np —— 见 lab/README.md 任务表第 10 行')
