"""保角映射的网格实验 · 第三块：网格变形 + 直角还在不在。

这是实验三（`exp3-mapping-grid`）要填的文件。按 `lab/README.md` 的任务表从上到下填掉
9 处 `raise NotImplementedError`，**填一个验一个**：

    python test_mapping_grid.py -k step1
    python test_mapping_grid.py            # 全部（含自检）

实验二在复平面上逐点验柯西-黎曼条件；这一课不再问「导数存不存在」，改问
**「导数的几何意义在图上长什么样」**：铺一张方格纸，按 w = f(z) 送过去，看格子有没有弯、
交角还是不是直角。结论是：格子弯是常态，直角由 f'(z) ≠ 0 决定。

**六个样例已经写好、别改**：

- `f_sq` / `f_exp` / `f_inv`：三个要画的映射 w = z^2、e^z、1/z；
- `MAPPINGS`：三个映射各自的参数窗口（z^2 的窗口要把原点框进来，1/z 的窗口要避开原点）；
- `is_conformal`：由你填的 `angle_defect` 推出的判据（偏差 ≤ 容差就算直角还在）。

只用标准库（`cmath` / `csv` / `math`）就能跑完 `test_mapping_grid.py`，不装 numpy、不装
matplotlib 都可以——交付物是 CSV，图只是数据的另一种画法。
"""

import cmath
import csv
import math

# 三张网格的参数窗口 (re_min, re_max, im_min, im_max)
SQ_WINDOW = (-1.0, 1.0, -1.0, 1.0)       # z^2：原点（临界点）正好落在网格交点上
EXP_WINDOW = (-1.0, 2.0, -3.0, 3.0)      # e^z：一条水平带，y 跨度正好是 (-π, π) 左右
INV_WINDOW = (0.1, 2.0, 0.1, 2.0)        # 1/z：网格避开极点，离 0 最近的那条线是 0.1

LINE_COUNT = 9        # 每个方向 9 条线
POINT_COUNT = 25      # 每条线 25 个点
ZOOM_WINDOW = (-0.3, 0.3, -0.3, 0.3)     # z^2 在原点附近的局部放大窗口

DEFAULT_DELTA = 1e-4      # 局部十字的臂长：把交点放大到 δ 尺度去看
DEFAULT_TOL_DEG = 0.5     # 夹角离 90° 差多少度以内算「直角还在」
DEFAULT_TOL_DERIV = 1e-9  # |f'(z)| 不超过它就当临界点
DEFAULT_H = 1e-6          # 数值导数的步长

CURVES_HEADER = ("family", "line", "k", "re", "im")
ANGLES_HEADER = ("map", "z0", "delta", "angle_deg", "defect_deg", "stretch", "verdict")


# ══ 三个映射（给好，不用填）══════════════════════════════════════
def f_sq(z):
    return z * z


def f_exp(z):
    return cmath.exp(z)


def f_inv(z):
    """1/z：z = 0 会抛 ZeroDivisionError——极点本来就不在定义域里。"""
    return 1 / z


# (表里显示的名字, 函数, 参数窗口)
MAPPINGS = [
    ("z^2", f_sq, SQ_WINDOW),
    ("e^z", f_exp, EXP_WINDOW),
    ("1/z", f_inv, INV_WINDOW),
]


# ══ 第 1 步 ═════════════════════════════════════════════════════
def segment_points(a, b, n):
    """线段 a → b 上等距的 n 个点（含两端），第 k 个点按参数 k/(n-1) 取。

    提示：参数写成 k / (n - 1)，两端才能正好落在 a 与 b 上；写成 k / n 会让终点永远差一截
    （网格右边少一列，看着只是「图小了点」，第 3 步一比就露）。
    n 小于 2 要抛 ValueError——一个点画不出线。
    """
    raise NotImplementedError('第 1 步还没写：segment_points —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def grid_lines(re_min, re_max, im_min, im_max, n_lines=LINE_COUNT, n_pts=POINT_COUNT):
    """铺一张参数网格，返回 (竖线族, 横线族)，都是 list[list[complex]]。

    竖线族：x 取 n_lines 个等距值，每条线从 (x, im_min) 走到 (x, im_max)；
    横线族：y 取 n_lines 个等距值，每条线从 (re_min, y) 走到 (re_max, y)。
    n_lines 或 n_pts 小于 2 时抛 ValueError。

    提示：两族都拿第 1 步的 segment_points 铺。别各写一遍循环——写两遍必然有一族端点取错。
    坐标用 complex(x, y) 拼，别写 x + y*1j（本机几种写法末位一致，但 complex() 最不容易看错）。
    """
    raise NotImplementedError('第 2 步还没写：grid_lines —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def map_grid(f, grid):
    """把整张网格按 w = f(z) 逐点送过去，返回同样形状的 (竖线族, 横线族)。

    这一步就是「网格变形」本身：直线送过去会变成抛物线、圆、射线。
    点在定义域外（1/z 的原点）时让异常照实抛出去，**别 catch、别填 0**——
    网格踩到极点这件事本身就是要你看见的东西。

    提示：外层遍历线、内层遍历点，两层都写成列表推导，形状自然保住（几条线、每线几点都不变）。
    """
    raise NotImplementedError('第 3 步还没写：map_grid —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def angle_between(v, w):
    """两个向量之间的夹角，单位是**度**，范围 0 到 180；任一个是零向量时返回 None。

    cos θ = (v·w) / (|v|·|w|)，其中 v·w = v_x·w_x + v_y·w_y。

    提示：点积用 v.real*w.real + v.imag*w.imag，模长用 abs()，最后 math.degrees 一次。
    acos 只吃 [-1, 1]：浮点算出来偶尔是 -1.0000000000000002，直接喂进去会 ValueError，
    所以要先把它夹回区间里。
    """
    raise NotImplementedError('第 4 步还没写：angle_between —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def cross_angle(f, z0, delta=DEFAULT_DELTA):
    """z0 处一个「小十字」被映射之后的夹角（度）。

    十字的两条臂是 z0 → z0 + delta 与 z0 → z0 + i·delta（它们本身成 90°）。
    取它们**各自的像**的两条弦 w1 = f(z0+delta) - f(z0)、w2 = f(z0+i·delta) - f(z0)，
    再量这两条弦的夹角——这就是把网格交点局部放大到 δ 尺度以后看到的角度。

    保角的映射量出 90°；z^2 在原点量出 180°（两条臂的像都倒在实轴上）。

    提示：别在这里求导——这一步只用函数值的差，导数是第 7 步的事。delta 是「放大倍数」：
    点离临界点越近，δ 就得取得越小，否则量到的是截断误差（第 5 步的第三条断言专门验这个）。
    """
    raise NotImplementedError('第 5 步还没写：cross_angle —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def angle_defect(f, z0, delta=DEFAULT_DELTA):
    """小十字的夹角离 90° 差多少度（保角的映射给 0 附近，z^2 在原点给 90）。

    量不出夹角（某条臂的像退化成零向量）时返回 90.0——那按「直角没了」算。

    提示：这一格数是 `out/angles.csv` 里 `defect_deg` 那一列，也是 is_conformal 的唯一依据。
    取绝对值：180° 与 0° 都不是直角，别只看一边。
    """
    raise NotImplementedError('第 6 步还没写：angle_defect —— 见 lab/README.md 任务表第 6 行')


def is_conformal(f, z0, delta=DEFAULT_DELTA, tol=DEFAULT_TOL_DEG):
    """（给好，不用填）这一点的直角还在吗：偏差不超过 tol 度。"""
    return angle_defect(f, z0, delta) <= tol


# ══ 第 7 步 ═════════════════════════════════════════════════════
def derivative_at(f, z0, h=DEFAULT_H):
    """数值导数 f'(z0)，用中心差分。

    |f'(z0)| 是映射在该点的**伸缩率**，arg f'(z0) 是**旋转角**（第 5 课 §1.4 那两句）。
    这个数不为零，十字的直角就保得住；它等于零，保角就坏——第 8 步要做的正是找它。

    提示：与第 5 课 lab 的 d_dx 是同一行代码，只改个名字；别忘记分母是 2h。
    """
    raise NotImplementedError('第 7 步还没写：derivative_at —— 见 lab/README.md 任务表第 7 行')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def critical_points(f, points, tol=DEFAULT_TOL_DERIV):
    """这批点里 |f'(z)| 不超过 tol 的那些（**保持传入顺序**）——保角失效的临界点。

    z^2 只有原点一个；e^z 与 1/z 的导数永不为零，所以在定义域里一个都没有。

    提示：列表推导 + abs(derivative_at(...)) <= tol，条件写成「小于等于」。
    别把 1/z 在 0 处算进来——那里根本没有定义，1/z 的临界点问题在复平面上不存在。
    也别用 set：断言比的是列表，顺序变了就对不上。
    """
    raise NotImplementedError('第 8 步还没写：critical_points —— 见 lab/README.md 任务表第 8 行')


# ══ 第 9 步 ═════════════════════════════════════════════════════
def save_curves_csv(path, families, header=CURVES_HEADER):
    """把映射后的网格写成 CSV：一行一个点，列是 family, line, k, re, im。

    families 形如 [("V", 竖线族), ("H", 横线族)]，每个族是 list[list[complex]]。
    返回写入的**数据行数**（不含表头）。这就是「网格变形图」的数据：
    9 条线 × 25 点 × 2 族 = 450 行。

    提示：open 三件套 `"w"` + `encoding="utf-8"` + `newline=""` 一个都不能省；
    复数要拆成 w.real 与 w.imag 两列（csv 不认 complex）；每格用 "{:.6g}"。
    """
    raise NotImplementedError('第 9 步还没写：save_curves_csv —— 见 lab/README.md 任务表第 9 行')


def save_angles_csv(path, rows, header=ANGLES_HEADER):
    """把「直角还在吗」这张结论表写成 CSV，一行一个测点。

    rows 里每项是 (map_name, z0_text, delta, angle_deg, defect_deg, stretch, verdict)。
    angle 写四位小数（90 与 180 要一眼分得开），defect 与 stretch 用 "{:.6g}"——
    保角那几行的偏差是 1e-3 到 1e-5 量级，写成四位小数会全变 0.0000，跟「坏掉了」就分不开了。
    返回写入的**数据行数**（不含表头）。

    提示：与上一格同一个 open 三件套；verdict 是字符串，原样写进去（它是自检算出来的结论）。
    """
    raise NotImplementedError('第 9 步还没写：save_angles_csv —— 见 lab/README.md 任务表第 9 行')
