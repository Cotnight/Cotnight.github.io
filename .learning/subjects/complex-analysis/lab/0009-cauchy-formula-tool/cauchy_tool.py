#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 003：柯西积分公式与高阶导数的数值核对（任务版 / 留白）

按 lab/README.md 的任务表，从上到下填掉 8 处 `raise NotImplementedError`，
一边填一边跑：

    python test_cauchy_tool.py            # 全部断言
    python test_cauchy_tool.py -k step3   # 只跑第 3 步

工具的用法一句话：**先把纸上的答案写下来，再让数值围道积分去验它。**
第 9 步把课件里那几道考试题整表跑一遍，跑绿了才算真会。

只用标准库 cmath / math，不需要装任何包。
"""

import cmath
import math

DEFAULT_N = 2048      # 围道上的采样点数（梯形法：周期解析函数收敛得极快，2048 绰绰有余）
DEFAULT_H = 1e-6      # 一阶差分的步长
DEFAULT_H2 = 1e-4     # 二阶差分的步长：差分公式里要除以 h*h，h 太小会被舍入误差吃掉
TAU = 2j * math.pi    # 2πi：两条公式里都有它，写成 2j*math.pi 就不会把 i 丢掉


# ══ 第 1 步 ═════════════════════════════════════════════════════
def circle_points(center, radius, n=DEFAULT_N):
    """围道 C: |z - center| = radius 上等距的 n 个采样点。

    从 center + radius 出发、按逆时针走一圈（正向）。
    提示：第 k 个点的角是 theta_k = 2*pi*k/n，
    z_k = center + radius * cmath.exp(1j * theta_k)。
    """
    raise NotImplementedError('第 1 步还没写：circle_points —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def contour_integral(f, center, radius, n=DEFAULT_N):
    """数值围道积分 ∮_C f(z) dz（沿第 1 步的采样点做梯形求和）。

    提示：dz 不是常数。z = center + r·e^{iθ} 时
    dz = i·r·e^{iθ}·dθ = i·dθ·(z - center)，dθ = 2*pi/n。
    所以每一项是 f(z_k) 乘 (1j * dtheta * (z_k - center))。
    """
    raise NotImplementedError('第 2 步还没写：contour_integral —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def inside(z0, center, radius):
    """奇点 z0 是否严格落在围道内部：|z0 - center| < radius。

    提示：围道上的点（距离恰好等于半径）不算圈内——
    公式要求被积函数在 C 及其内部解析，压在 C 上的点是两条公式都不适用的情形。
    """
    raise NotImplementedError('第 3 步还没写：inside —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def deriv_n(g, z, order, h=DEFAULT_H2):
    """g 在 z 处的第 order 阶导，order 只要求支持 0、1、2。

    提示：order = 0 时公式里是 0! = 1、不求导，直接返回 g(z)。
    order = 1 用中心差分 (g(z+h) - g(z-h)) / (2h)；
    order = 2 用 (g(z+h) - 2g(z) + g(z-h)) / (h*h)。
    二阶差分要除以 h 的平方，所以默认步长给的是 DEFAULT_H2 而不是 DEFAULT_H。
    """
    raise NotImplementedError('第 4 步还没写：deriv_n —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def cauchy_value(g, z0):
    """分母是一次方的那一项：∮_C g(z)/(z - z0) dz 的公式值 = 2πi·g(z0)。"""
    raise NotImplementedError('第 5 步还没写：cauchy_value —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def high_order_value(g, z0, m, h=DEFAULT_H2):
    """分母是 (z - z0)**m 的那一项（m >= 2）：

        2πi / (m-1)! · g^{(m-1)}(z0)

    提示：幂次是 m，求的导数是 m-1 阶，阶乘也是 (m-1)!，三处用的是同一个数 m-1。
    """
    raise NotImplementedError('第 6 步还没写：high_order_value —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def formula_value(g, z0, m, h=DEFAULT_H2):
    """统一入口：m = 1 走第 5 步，m >= 2 走第 6 步。

    这一步就是课件那张「分母幂次决定用哪个公式」的对照卡。
    """
    raise NotImplementedError('第 7 步还没写：formula_value —— 见 lab/README.md 任务表第 7 行')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def contour_total(terms, center, radius):
    """围道内所有奇点的项相加。

    terms 是 [(g, z0, m), ...]：每个奇点给一个 (它的 g、它的位置、它的幂次)。
    提示：先用第 3 步筛，圈外的项直接跳过（它的值是 0），
    圈内的项用第 7 步算出来加到总和里。
    """
    raise NotImplementedError('第 8 步还没写：contour_total —— 见 lab/README.md 任务表第 8 行')
