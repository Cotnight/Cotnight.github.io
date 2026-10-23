#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 0012：泰勒/洛朗展开系数核对器（参考解）

用法与任务版完全相同：把本文件拷进 lab/0012-laurent-coeff-tool/ 覆盖同名文件，
再跑 python test_laurent_tool.py，29 条断言应全绿。

    python test_laurent_tool.py            # 全部 29 条
    python test_laurent_tool.py -k step7   # 只跑第 7 步

每一步"为什么这样写"见 solutions/0012-laurent-coeff-tool/README.md。
"""

import cmath
import math

TAU_I = 2j * math.pi   # 2πi
DEFAULT_N = 512        # 圆周上的采样点数


# ══ 两个现成的小工具（不用改）══════════════════════════════════════
def closed_range(lo, hi):
    """闭区间 [lo, hi] 的整数列表。"""
    return list(range(lo, hi + 1))


def f_lesson(z):
    """课件里的例题：f(z) = 1 / ((z-1)(z-2))。"""
    return 1 / ((z - 1) * (z - 2))


# ══ 第 1 步 ═════════════════════════════════════════════════════
def contour_points(center, radius, n=DEFAULT_N):
    """|ζ - center| = radius 上等距的 n 个点，逆时针，从 ζ = center + radius 出发。"""
    return [center + radius * cmath.exp(1j * 2 * math.pi * k / n) for k in range(n)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def coeff_integral(f, k, center, radius, n=DEFAULT_N):
    """c_k = (1/2πi)∮ f(ζ)/(ζ-center)^(k+1) dζ，沿 |ζ-center| = radius 数一圈。

    dz 要换元：ζ = center + radius·e^{iθ} ⇒ dz = i·radius·e^{iθ}·dθ = i·Δθ·(ζ - center)。
    """
    dtheta = 2 * math.pi / n
    total = 0j
    for z in contour_points(center, radius, n):
        dz = 1j * dtheta * (z - center)
        total += f(z) / (z - center) ** (k + 1) * dz
    return total / TAU_I


# ══ 第 3 步 ═════════════════════════════════════════════════════
def coeffs(f, ks, center, radius, n=DEFAULT_N):
    """一组系数 {k: c_k}。"""
    return {k: coeff_integral(f, k, center, radius, n) for k in ks}


# ══ 第 4 步 ═════════════════════════════════════════════════════
def series_value(coeff_map, center, z):
    """Σ c_k (z-center)^k，正幂负幂一起算。"""
    return sum((c * (z - center) ** k for k, c in coeff_map.items()), 0j)


# ══ 第 5 步 ═════════════════════════════════════════════════════
def truncation_error(f, coeff_map, center, z):
    """截断误差 |Σ c_k (z-center)^k - f(z)|。"""
    return abs(series_value(coeff_map, center, z) - f(z))


# ══ 第 6 步 ═════════════════════════════════════════════════════
def partial_fractions(a, b):
    """1/((z-a)(z-b)) = A/(z-a) + B/(z-b)，返回 (A, B)。

    遮住一个因式、把根代进去：A = 1/(a-b)、B = 1/(b-a)。
    """
    return (1 / (a - b), 1 / (b - a))


# ══ 第 7 步 ═════════════════════════════════════════════════════
def geom_coeffs(a, inside, n_max):
    """1/(z-a) 的展开系数 {k: c_k}。

    |z|<|a|：1/(z-a) = -(1/a)·Σ(z/a)^n = -Σ z^n/a^{n+1}  ⇒ c_n = -a^{-(n+1)}（n≥0）
    |z|>|a|：1/(z-a) = (1/z)·Σ(a/z)^n =  Σ a^n/z^{n+1}  ⇒ c_{-n-1} = a^n（n≥0）
    """
    out = {}
    for n in range(n_max + 1):
        if inside:
            out[n] = -a ** (-(n + 1))
        else:
            out[-(n + 1)] = a ** n
    return out


# ══ 第 8 步 ═════════════════════════════════════════════════════
def ring_coeffs(a, b, ring, n_max=8):
    """1/((z-a)(z-b)) 在 ring 指定的环域里的系数 {k: c_k}（中心是原点）。

    先按 |a|、|b| 排出谁近谁远，再决定每一项走哪一支，最后同幂次相加。
    """
    near, far = sorted((a, b), key=abs)
    if ring == 'inner':
        flags = {near: True, far: True}
    elif ring == 'middle':
        flags = {near: False, far: True}
    elif ring == 'outer':
        flags = {near: False, far: False}
    else:
        raise ValueError('ring 只能是 inner / middle / outer，收到的是 {!r}'.format(ring))

    weights = {a: 1 / (a - b), b: 1 / (b - a)}
    out = {}
    for s in (near, far):
        for k, c in geom_coeffs(s, flags[s], n_max).items():
            out[k] = out.get(k, 0j) + weights[s] * c
    return out
