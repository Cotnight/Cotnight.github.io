#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 003：柯西积分公式与高阶导数的数值核对（参考解）

八步都填好了。把它拷进 lab/0009-cauchy-formula-tool/ 覆盖同名留白文件，
`python test_cauchy_tool.py` 就是全绿。

逐条为什么这样写、每步最常见的错法，见同目录的 README.md。
只用标准库 cmath / math。
"""

import cmath
import math

DEFAULT_N = 2048      # 围道上的采样点数（梯形法对周期解析函数几乎精确）
DEFAULT_H = 1e-6      # 一阶差分的步长
DEFAULT_H2 = 1e-4     # 二阶差分的步长
TAU = 2j * math.pi    # 2πi


def circle_points(center, radius, n=DEFAULT_N):
    """从 center + radius 出发、逆时针等距取 n 个点。"""
    dtheta = 2 * math.pi / n
    return [center + radius * cmath.exp(1j * dtheta * k) for k in range(n)]


def contour_integral(f, center, radius, n=DEFAULT_N):
    """∮_C f dz ≈ Σ f(z_k)·i·Δθ·(z_k - center)。"""
    dtheta = 2 * math.pi / n
    total = 0j
    for z in circle_points(center, radius, n):
        total += f(z) * (1j * dtheta * (z - center))
    return total


def inside(z0, center, radius):
    """严格在圆内；压在围道上的点不算。"""
    return abs(z0 - center) < radius


def deriv_n(g, z, order, h=DEFAULT_H2):
    """0/1/2 阶中心差分。"""
    if order == 0:
        return g(z)
    if order == 1:
        return (g(z + h) - g(z - h)) / (2 * h)
    if order == 2:
        return (g(z + h) - 2 * g(z) + g(z - h)) / (h * h)
    raise ValueError('deriv_n 只支持 0/1/2 阶，收到 {}'.format(order))


def cauchy_value(g, z0):
    """分母一次方那一项：2πi·g(z0)。"""
    return TAU * g(z0)


def high_order_value(g, z0, m, h=DEFAULT_H2):
    """分母 (z-z0)^m 那一项：2πi/(m-1)! · g^{(m-1)}(z0)，m >= 2。"""
    if m < 2:
        raise ValueError('high_order_value 只接 m >= 2，m = 1 请用 cauchy_value')
    order = m - 1
    return TAU / math.factorial(order) * deriv_n(g, z0, order, h)


def formula_value(g, z0, m, h=DEFAULT_H2):
    """幂次决定用哪个公式：m = 1 走柯西积分公式，m >= 2 走高阶导数公式。"""
    if m == 1:
        return cauchy_value(g, z0)
    return high_order_value(g, z0, m, h)


def contour_total(terms, center, radius):
    """圈内的项相加；圈外的项按 0 处理。"""
    total = 0j
    for g, z0, m in terms:
        if not inside(z0, center, radius):
            continue
        total += formula_value(g, z0, m)
    return total
