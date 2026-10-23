#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 010：柯西积分定理与复合闭路（参考解）

把这份文件拷进 `lab/0010-cauchy-closed-contour/` 覆盖同名文件，
`python test_cauchy_lab.py` 就是 30 条断言全绿（实测 `Ran 30 tests … OK`）。

每一步为什么这样写，见 `solutions/0010-cauchy-closed-contour/README.md`。
只用标准库 cmath / math。
"""

import cmath
import math

DEFAULT_N = 4096      # 一条圆周上采多少个点
TOL_ZERO = 1e-6       # 判「积分约为 0」的容差
TOL_VALUE = 2e-2      # 判「等于某个非零值」的容差：折线代替圆弧有 O(1/n) 的误差


# ══ 第 1 步 ═════════════════════════════════════════════════════
def circle_contour(center, radius, n=DEFAULT_N):
    """正向圆周上的 n 个点；第 k 个是 center + radius*e^(i*2πk/n)，首点不重复。"""
    return [center + radius * cmath.exp(2j * math.pi * k / n) for k in range(n)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def contour_integral(f, points):
    """开路径积分：Σ f(z_k)(z_{k+1} − z_k)，k 到 len(points)−2 为止。"""
    total = 0j
    for k in range(len(points) - 1):
        total += f(points[k]) * (points[k + 1] - points[k])
    return total


# ══ 第 3 步 ═════════════════════════════════════════════════════
def closed_integral(f, points):
    """闭路积分：下一个点取 points[(k+1) % n]，末点自动接回首点。"""
    total = 0j
    n = len(points)
    for k in range(n):
        total += f(points[k]) * (points[(k + 1) % n] - points[k])
    return total


# ══ 第 4 步 ═════════════════════════════════════════════════════
def nearly_zero(value, tol=TOL_ZERO):
    """模不超过容差就算 0。"""
    return abs(value) <= tol


# ══ 第 5 步 ═════════════════════════════════════════════════════
def composite_integral(f, center, r_out, r_in, n=DEFAULT_N):
    """复合闭路：外圈正向 + 内圈反向 = 外圈那个积分减去内圈（正方向）那个积分。"""
    outer = closed_integral(f, circle_contour(center, r_out, n))
    inner = closed_integral(f, circle_contour(center, r_in, n))
    return outer - inner


# ══ 第 6 步 ═════════════════════════════════════════════════════
def arc_contour(center, radius, theta0, theta1, n=DEFAULT_N):
    """圆弧上的 n+1 个点，角从 theta0 均匀走到 theta1（可按弧度反向）。"""
    return [center + radius * cmath.exp(1j * (theta0 + (theta1 - theta0) * k / n))
            for k in range(n + 1)]


# ══ 第 7 步 ═════════════════════════════════════════════════════
def arc_integral(f, center, radius, theta0, theta1, n=DEFAULT_N):
    """沿圆弧的积分：第 2 步套第 6 步，仍是开路径。"""
    return contour_integral(f, arc_contour(center, radius, theta0, theta1, n))
