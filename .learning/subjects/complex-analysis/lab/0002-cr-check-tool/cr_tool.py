#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 002：柯西-黎曼条件检查器（任务版 / 留白）

按 lab/README.md 的任务表，从上到下填掉 8 处 `raise NotImplementedError`，
一边填一边跑：

    python test_cr_tool.py            # 全部 22 条断言
    python test_cr_tool.py -k step3   # 只跑第 3 步

三个辅助函数（u_of / v_of / d_dx）已经给好，照着它们的写法往下填。
只用标准库 cmath，不需要装任何包。
"""

import cmath

DEFAULT_H = 1e-6      # 一阶差分的步长
DEFAULT_H2 = 1e-4     # 二阶差分的步长：差分公式里要除以 h*h，h 太小会被舍入误差吃掉
DEFAULT_TOL = 1e-4    # 判"接近 0"的容差


# ══ 三个现成的辅助函数（不用改）══════════════════════════════════════
def u_of(f, z):
    """f 在 z 处的实部 u。"""
    return f(z).real


def v_of(f, z):
    """f 在 z 处的虚部 v。"""
    return f(z).imag


def d_dx(f, z, h=DEFAULT_H):
    """沿 x 方向的一阶偏导 ∂f/∂x（中心差分），返回复数 u_x + i v_x。"""
    return (f(z + h) - f(z - h)) / (2 * h)


# ══ 第 1 步 ═════════════════════════════════════════════════════
def d_dy(f, z, h=DEFAULT_H):
    """沿 y 方向的一阶偏导 ∂f/∂y（中心差分），返回复数 u_y + i v_y。

    提示：y 方向走一步，在 z 平面上是加一个纯虚数 i*h。
    想一想差分 f(y+h) - f(y-h) 对应真实的 Δy 是多少，分母该写什么。
    """
    raise NotImplementedError('第 1 步还没写：d_dy —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def cr_residual(f, z, h=DEFAULT_H):
    """柯西-黎曼条件的两条残差 (r1, r2)：

        r1 = u_x - v_y，r2 = u_y + v_x

    提示：d_dx 给的是 u_x + i v_x，d_dy 给的是 u_y + i v_y，
    所以 u_x = d_dx 的实部、v_x = d_dx 的虚部，另外两个同理。
    """
    raise NotImplementedError('第 2 步还没写：cr_residual —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def cr_holds(f, z, tol=DEFAULT_TOL, h=DEFAULT_H):
    """这一点满足柯西-黎曼条件吗？

    提示：数值差分有误差，所以不能用 == 0 判，要按容差判。
    """
    raise NotImplementedError('第 3 步还没写：cr_holds —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def cr_points(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """把一批点里满足 CR 的筛出来，保持传入顺序。

    提示：点集的大小就是结论的强弱——整片区域才谈得上解析，一两个点只能说可导。
    """
    raise NotImplementedError('第 4 步还没写：cr_points —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def verdict(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """判定卡的结论：'all' / 'some' / 'none'。

    提示：注意空点集这个边界——all([]) 在 Python 里是 True，别让它骗过去。
    """
    raise NotImplementedError('第 5 步还没写：verdict —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def laplacian(u, z, h=DEFAULT_H2):
    """Δu = u_xx + u_yy，两个方向的二阶中心差分相加。

    提示：二阶差分的分子是 u(+h) - 2u(0) + u(-h)，分母是 h*h；
    "沿实轴走"和"沿虚轴走"各算一项，再加起来。
    """
    raise NotImplementedError('第 6 步还没写：laplacian —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def is_harmonic(u, points, tol=DEFAULT_TOL, h=DEFAULT_H2):
    """u 在这批点上调和吗：每一点的 |Δu| 都要不超过容差。"""
    raise NotImplementedError('第 7 步还没写：is_harmonic —— 见 lab/README.md 任务表第 7 行')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def polar_cr_residual(f, r, theta, h=DEFAULT_H):
    """极坐标 CR 的两条残差 (s1, s2)：

        s1 = u_r - v_theta / r，s2 = v_r + u_theta / r

    提示：w(r, theta) = f(r e^{i theta}) 是 r、theta 的复值函数，
    对 r 和 theta 各做一次中心差分，得到 u_r、v_r、u_theta、v_theta，
    再注意极坐标那两条式子里的 1/r 不能漏。
    """
    raise NotImplementedError('第 8 步还没写：polar_cr_residual —— 见 lab/README.md 任务表第 8 行')
