#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 002：柯西-黎曼条件检查器（参考解）

把本文件拷进 lab/0002-cr-check-tool/ 覆盖同名文件，再跑
python test_cr_tool.py，九步应当全绿。

每一处实现旁边都写了"为什么这样写"，方便对照你卡住的那一步。
只用标准库 cmath。
"""

import cmath

DEFAULT_H = 1e-6      # 一阶差分的步长
DEFAULT_H2 = 1e-4     # 二阶差分的步长：差分公式里要除以 h*h，h 太小会被舍入误差吃掉
DEFAULT_TOL = 1e-4    # 判"接近 0"的容差


# ══ 三个现成的辅助函数 ══════════════════════════════════════════════
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

    y 方向走一步，在 z 平面上就是加一个纯虚数 i*h；
    差分 f(y+h) - f(y-h) 已经比真实的 Δy = 2h 大了两倍，
    所以分母仍是 2*h——不要再乘一个 i。
    """
    return (f(z + 1j * h) - f(z - 1j * h)) / (2 * h)


# ══ 第 2 步 ═════════════════════════════════════════════════════
def cr_residual(f, z, h=DEFAULT_H):
    """柯西-黎曼条件的两条残差 (r1, r2)：

        r1 = u_x - v_y，r2 = u_y + v_x

    d_dx 给的是 u_x + i v_x，d_dy 给的是 u_y + i v_y，
    所以 u_x = d_dx 的实部、v_x = d_dx 的虚部，
    u_y = d_dy 的实部、v_y = d_dy 的虚部。
    """
    dx = d_dx(f, z, h)          # u_x + i v_x
    dy = d_dy(f, z, h)          # u_y + i v_y
    return dx.real - dy.imag, dy.real + dx.imag


# ══ 第 3 步 ═════════════════════════════════════════════════════
def cr_holds(f, z, tol=DEFAULT_TOL, h=DEFAULT_H):
    """这一点满足柯西-黎曼条件吗？

    数值差分有误差，所以不能用 == 0，要按容差判（这是数值做法与纸上做法的差别）。
    """
    r1, r2 = cr_residual(f, z, h)
    return abs(r1) <= tol and abs(r2) <= tol


# ══ 第 4 步 ═════════════════════════════════════════════════════
def cr_points(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """把一批点里满足 CR 的筛出来，保持传入顺序。

    点集的大小就是结论的强弱：整片区域才谈得上解析，一两个点只能说可导。
    """
    return [z for z in points if cr_holds(f, z, tol, h)]


# ══ 第 5 步 ═════════════════════════════════════════════════════
def verdict(f, points, tol=DEFAULT_TOL, h=DEFAULT_H):
    """判定卡的结论：'all' / 'some' / 'none'。"""
    if not points:
        return 'none'
    hits = cr_points(f, points, tol, h)
    if len(hits) == len(points):
        return 'all'
    return 'some' if hits else 'none'


# ══ 第 6 步 ═════════════════════════════════════════════════════
def laplacian(u, z, h=DEFAULT_H2):
    """Δu = u_xx + u_yy，两个方向的二阶中心差分相加：

        u_xx ≈ (u(z+h) - 2u(z) + u(z-h)) / h^2
        u_yy ≈ (u(z+ih) - 2u(z) + u(z-ih)) / h^2

    注意每一步都可以在 z 平面上"沿实轴走"或"沿虚轴走"，
    二阶差分的分子是 u(+h) - 2u(0) + u(-h)。
    """
    dxx = (u(z + h) - 2 * u(z) + u(z - h)) / (h * h)
    dyy = (u(z + 1j * h) - 2 * u(z) + u(z - 1j * h)) / (h * h)
    return dxx + dyy


# ══ 第 7 步 ═════════════════════════════════════════════════════
def is_harmonic(u, points, tol=DEFAULT_TOL, h=DEFAULT_H2):
    """u 在这批点上调和吗：每一点的 |Δu| 都要不超过容差。"""
    return all(abs(laplacian(u, z, h)) <= tol for z in points)


# ══ 第 8 步 ═════════════════════════════════════════════════════
def polar_cr_residual(f, r, theta, h=DEFAULT_H):
    """极坐标 CR 的两条残差 (s1, s2)：

        s1 = u_r - v_theta / r，s2 = v_r + u_theta / r

    w(r, theta) = f(r e^{i theta}) 是 r、theta 的复值函数，
    对 r 差分得 u_r 与 v_r，对 theta 差分得 u_theta 与 v_theta；
    极坐标那两条式子里的 1/r 不能漏，它是这两种差分之间的关系。
    """
    def w(rr, tt):
        return f(rr * cmath.exp(1j * tt))

    def uu(rr, tt):
        return w(rr, tt).real

    def vv(rr, tt):
        return w(rr, tt).imag

    u_r = (uu(r + h, theta) - uu(r - h, theta)) / (2 * h)
    v_r = (vv(r + h, theta) - vv(r - h, theta)) / (2 * h)
    u_t = (uu(r, theta + h) - uu(r, theta - h)) / (2 * h)
    v_t = (vv(r, theta + h) - vv(r, theta - h)) / (2 * h)
    return u_r - v_t / r, v_r + u_t / r
