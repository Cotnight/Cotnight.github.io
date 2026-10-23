#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 010：柯西积分定理与复合闭路（任务版 / 留白）

按 lab/README.md 的任务表，从上到下填掉 7 处 `raise NotImplementedError`，
一边填一边跑：

    python test_cauchy_lab.py            # 全部 29 条断言
    python test_cauchy_lab.py -k step5   # 只跑第 5 步

这个工具做的事只有一句：把一条围道采样成点列，沿点列把 f(z)dz 累加起来，
看这个和是 0、是 2πi、还是别的数——也就是卷面上动笔前那一步「能不能直接写 0」。

两个约定先记住：
  · 比例尺是「点列」而不是「参数式」：曲线一律先变成一串复数点，
    积分只在点列上做。这样圆、圆环、圆弧、以后的折线都用同一套代码。
  · 折线代替光滑曲线总是差一点点，所以代码里写 0 必须写成 nearly_zero。

只用标准库 cmath / math，不需要装任何包。
"""

import cmath
import math

DEFAULT_N = 4096      # 一条圆周上采多少个点
TOL_ZERO = 1e-6       # 判「积分约为 0」的容差
TOL_VALUE = 2e-2      # 判「等于某个非零值」的容差：折线代替圆弧有 O(1/n) 的误差


# ══ 第 1 步 ═════════════════════════════════════════════════════
def circle_contour(center, radius, n=DEFAULT_N):
    """正向（逆时针）圆周上的 n 个点。

    返回一个长度 n 的列表：从 center + radius 出发逆时针走一圈，
    最后一个点与第一个点**差一步**（首点不要重复写进列表末尾）。

    提示：第 k 个点是 center + radius * e^(i*2πk/n)，k = 0, 1, …, n-1。
    Python 里写 cmath.exp(1j * 角)，角一律按弧度算。
    方向不用你另加符号：k 递增时角跟着递增，点自己就逆时针转。
    """
    raise NotImplementedError('第 1 步还没写：circle_contour —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def contour_integral(f, points):
    """沿点列把 f(z)dz 加起来（**开路径**：末点不接回首点）。

    返回 sum(f(points[k]) * (points[k+1] - points[k]))，
    k 从 0 到 len(points) - 2。也就是说：最后一个点没有「下一段」，这里不管它。

    提示：这就是定积分定义那个和式——每小段用左端点的函数值乘上这一段的 Δz。
    """
    raise NotImplementedError('第 2 步还没写：contour_integral —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def closed_integral(f, points):
    """闭路积分：最后一个点要接回第一个点。

    与第 2 步只差一段：points[-1] → points[0] 也算进去，其余段一模一样。
    提示：把下一个点写成 points[(k+1) % len(points)]，一遍循环就闭合了。
    """
    raise NotImplementedError('第 3 步还没写：closed_integral —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def nearly_zero(value, tol=TOL_ZERO):
    """这个积分值的模算不算「0」（按容差判），返回 True / False。

    折线代替圆弧，结果总留着一点残渣（第 5 步会看到 1/z 的残渣有多大），
    所以代码里判零不能写 value == 0。
    """
    raise NotImplementedError('第 4 步还没写：nearly_zero —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def composite_integral(f, center, r_out, r_in, n=DEFAULT_N):
    """复合闭路（挖洞）的积分：区域是圆环 r_in < |z - center| < r_out。

    外圈取正向、内圈取**反向**（沿合成围道走的时候内圈是顺时针）。
    按复合闭路定理，沿合成围道的积分 = 沿外圈的积分 + 沿内圈反走的积分
    = 外圈那个积分 **减去** 内圈（正方向）那个积分。

    返回 closed_integral(f, 外圈点列) - closed_integral(f, 内圈点列)。
    那个减号就是「内圈取顺时针」在代码里的样子，别丢掉。
    """
    raise NotImplementedError('第 5 步还没写：composite_integral —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def arc_contour(center, radius, theta0, theta1, n=DEFAULT_N):
    """圆弧上的 n + 1 个点（开路径，首末两个点都要）。

    从 θ0 按弧度均匀走到 θ1：首点是 center + radius*e^(i*θ0)，
    末点是 center + radius*e^(i*θ1)。θ1 < θ0 就是反着走。
    提示：第 k 个点的角是 theta0 + (theta1 - theta0) * k / n，k 从 0 到 n。
    """
    raise NotImplementedError('第 6 步还没写：arc_contour —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def arc_integral(f, center, radius, theta0, theta1, n=DEFAULT_N):
    """沿圆弧的积分 = 第 2 步套第 6 步：contour_integral(f, arc_contour(...))。

    与第 2 步一样是**开路径**：从 θ0 那个点到 θ1 那个点，不闭合。
    """
    raise NotImplementedError('第 7 步还没写：arc_integral —— 见 lab/README.md 任务表第 7 行')
