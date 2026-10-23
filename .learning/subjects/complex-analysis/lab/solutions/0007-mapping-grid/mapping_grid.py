"""保角映射的网格实验 · 第三块：网格变形 + 直角还在不在（参考解）。

把上一个文件（`lab/0007-mapping-grid/mapping_grid.py`）覆盖掉同名文件就能直接跑；
本文件只 import 标准库（`cmath` / `csv` / `math`），不引用任务目录里的任何东西。
"""

import cmath
import csv
import math

# 三张网格的参数窗口 (re_min, re_max, im_min, im_max)
SQ_WINDOW = (-1.0, 1.0, -1.0, 1.0)
EXP_WINDOW = (-1.0, 2.0, -3.0, 3.0)
INV_WINDOW = (0.1, 2.0, 0.1, 2.0)

LINE_COUNT = 9
POINT_COUNT = 25
ZOOM_WINDOW = (-0.3, 0.3, -0.3, 0.3)

DEFAULT_DELTA = 1e-4
DEFAULT_TOL_DEG = 0.5
DEFAULT_TOL_DERIV = 1e-9
DEFAULT_H = 1e-6

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
    """线段 a → b 上等距的 n 个点（含两端），第 k 个点按参数 k/(n-1) 取。"""
    if n < 2:
        raise ValueError("n 至少为 2：一个点画不出线")
    return [a + (b - a) * k / (n - 1) for k in range(n)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def grid_lines(re_min, re_max, im_min, im_max, n_lines=LINE_COUNT, n_pts=POINT_COUNT):
    """铺参数网格，返回 (竖线族, 横线族)：竖线 x 固定自下而上，横线 y 固定自左向右。"""
    if n_lines < 2 or n_pts < 2:
        raise ValueError("n_lines 与 n_pts 都至少为 2")
    vertical = [segment_points(complex(re_min + (re_max - re_min) * k / (n_lines - 1), im_min),
                               complex(re_min + (re_max - re_min) * k / (n_lines - 1), im_max),
                               n_pts)
                for k in range(n_lines)]
    horizontal = [segment_points(complex(re_min, im_min + (im_max - im_min) * k / (n_lines - 1)),
                                 complex(re_max, im_min + (im_max - im_min) * k / (n_lines - 1)),
                                 n_pts)
                  for k in range(n_lines)]
    return (vertical, horizontal)


# ══ 第 3 步 ═════════════════════════════════════════════════════
def map_grid(f, grid):
    """把整张网格逐点送过去，形状不变；定义域外的点让异常照实抛。"""
    vertical, horizontal = grid
    return ([[f(z) for z in line] for line in vertical],
            [[f(z) for z in line] for line in horizontal])


# ══ 第 4 步 ═════════════════════════════════════════════════════
def angle_between(v, w):
    """两个向量的夹角（度，0 到 180）；任一为零向量返回 None。"""
    nv, nw = abs(v), abs(w)
    if nv == 0.0 or nw == 0.0:
        return None
    cos = (v.real * w.real + v.imag * w.imag) / (nv * nw)
    return math.degrees(math.acos(max(-1.0, min(1.0, cos))))


# ══ 第 5 步 ═════════════════════════════════════════════════════
def cross_angle(f, z0, delta=DEFAULT_DELTA):
    """z0 处小十字（两条坐标方向的臂）被映射后的夹角（度）。"""
    w1 = f(z0 + delta) - f(z0)
    w2 = f(z0 + 1j * delta) - f(z0)
    return angle_between(w1, w2)


# ══ 第 6 步 ═════════════════════════════════════════════════════
def angle_defect(f, z0, delta=DEFAULT_DELTA):
    """小十字的夹角离 90° 差多少度；量不出夹角时按 90 算。"""
    got = cross_angle(f, z0, delta)
    if got is None:
        return 90.0
    return abs(got - 90.0)


def is_conformal(f, z0, delta=DEFAULT_DELTA, tol=DEFAULT_TOL_DEG):
    """（给好，不用填）这一点的直角还在吗：误差不超过 tol 度。"""
    return angle_defect(f, z0, delta) <= tol


# ══ 第 7 步 ═════════════════════════════════════════════════════
def derivative_at(f, z0, h=DEFAULT_H):
    """数值导数 f'(z0)（中心差分）：模是伸缩率，辐角是旋转角。"""
    return (f(z0 + h) - f(z0 - h)) / (2 * h)


# ══ 第 8 步 ═════════════════════════════════════════════════════
def critical_points(f, points, tol=DEFAULT_TOL_DERIV):
    """这批点里 |f'(z)| 不超过 tol 的那些（保持顺序）——保角失效的临界点。"""
    return [z for z in points if abs(derivative_at(f, z)) <= tol]


# ══ 第 9 步 ═════════════════════════════════════════════════════
def save_curves_csv(path, families, header=CURVES_HEADER):
    """网格数据写成 CSV：一行一个点，列 family,line,k,re,im。返回数据行数。"""
    rows = 0
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for family, curves in families:
            for i, curve in enumerate(curves):
                for k, w in enumerate(curve):
                    writer.writerow([family, i, k,
                                     "{:.6g}".format(w.real),
                                     "{:.6g}".format(w.imag)])
                    rows += 1
    return rows


def save_angles_csv(path, rows, header=ANGLES_HEADER):
    """结论表写成 CSV：一行一个测点。返回数据行数。"""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for name, z0_text, delta, angle, defect, stretch, verdict in rows:
            writer.writerow([name, z0_text, "{:.0e}".format(float(delta)),
                             "{:.4f}".format(float(angle)),
                             "{:.6g}".format(float(defect)),
                             "{:.6g}".format(float(stretch)),
                             verdict])
    return len(rows)
