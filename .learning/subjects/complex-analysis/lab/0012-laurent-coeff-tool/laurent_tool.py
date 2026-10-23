#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 0012：泰勒/洛朗展开系数核对器（任务版 / 留白）

按 lab/README.md 的任务表，从上到下填掉 8 处 `raise NotImplementedError`，
一边填一边跑：

    python test_laurent_tool.py            # 全部 29 条断言
    python test_laurent_tool.py -k step3   # 只跑第 3 步

两个小工具（closed_range / f_lesson）和两个常数已经给好，照着它们的写法往下填。
只用标准库 cmath / math，不需要装任何包。

这一节要做的判断只有一句：**纸面上的系数对不对，让围道积分来说。**
"""

import cmath
import math

TAU_I = 2j * math.pi   # 2πi：系数公式里那个因子，先乘好，省得中途把 i 丢掉
DEFAULT_N = 512        # 围道上取多少点：梯形法对圆周上的解析被积函数收敛极快，512 点已到机器精度


# ══ 两个现成的小工具（不用改）══════════════════════════════════════
def closed_range(lo, hi):
    """闭区间 [lo, hi] 的整数列表，写断言与自检时省事。"""
    return list(range(lo, hi + 1))


def f_lesson(z):
    """课件里的例题：f(z) = 1 / ((z-1)(z-2))。

    奇点是 1 与 2，所以以原点为心能切出 |z|<1、1<|z|<2、|z|>2 三个环域。
    第 9 步的整表自检就用它。
    """
    return 1 / ((z - 1) * (z - 2))


# ══ 第 1 步 ═════════════════════════════════════════════════════
def contour_points(center, radius, n=DEFAULT_N):
    """环域内一条绕 center 一圈的圆周上，等距的 n 个点（逆时针，从 θ=0 出发）。

    提示：参数化 ζ = center + radius·e^{iθ}，θ 取 2πk/n（k=0..n-1）。
    圆要绕在环域里面，这条围道上的点就是第 2 步积分的采样点。
    """
    raise NotImplementedError('第 1 步还没写：contour_points —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def coeff_integral(f, k, center, radius, n=DEFAULT_N):
    """数值算一个系数

        c_k = (1 / 2πi) ∮ f(ζ) / (ζ - center)^(k+1) dζ ,

    沿 |ζ - center| = radius 正向走一圈。k 可以是负数（负幂项），k = -1 时分母是
    (ζ - center)^0 = 1。

    提示：围道换元以后 dz 也变了——ζ = center + radius·e^{iθ} 求微分得
    dz = i·radius·e^{iθ}·dθ，用 ζ - center 写出来就是 i·Δθ·(ζ - center)，
    其中 Δθ = 2π/n。把 n 个采样点的 f(ζ)/... · dz 加起来，再除以 TAU_I。
    """
    raise NotImplementedError('第 2 步还没写：coeff_integral —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def coeffs(f, ks, center, radius, n=DEFAULT_N):
    """一次算出一组系数：返回 {k: c_k}，键就是 ks 里的那些整数。

    提示：这一步只是循环，别在这里改默认的 n，也别丢掉负号。
    """
    raise NotImplementedError('第 3 步还没写：coeffs —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def series_value(coeff_map, center, z):
    """拿一张系数表在 z 处求和：Σ c_k (z - center)^k，正幂负幂一起算。

    提示：负幂就是 (z - center)**k，k 为负时 Python 会照算，不用自己取倒数。
    空表要返回 0（不是 None）。
    """
    raise NotImplementedError('第 4 步还没写：series_value —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def truncation_error(f, coeff_map, center, z):
    """截断误差：用这张（有限的）系数表在 z 处求和，与 f(z) 差多少（取模）。

    提示：系数表越长误差越小；同一张表在环域内成立、出了环域就发散了，
    这也正是"每一条展开只在它自己的环域内成立"的数值形态。
    """
    raise NotImplementedError('第 5 步还没写：truncation_error —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def partial_fractions(a, b):
    """把 1 / ((z-a)(z-b)) 拆成 A/(z-a) + B/(z-b)，返回 (A, B)。

    提示：分子是常数 1、分母是两个一次因式时，A 就是"遮住 z-a 那一项、把 z=a 代进去"的值。
    注意权重跟着 a、b 走：交换 a、b 时两项的权重也跟着换。
    """
    raise NotImplementedError('第 6 步还没写：partial_fractions —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def geom_coeffs(a, inside, n_max):
    """1/(z-a) 的展开系数表 {k: c_k}，展开到 n_max。

    inside=True  →  在 |z| < |a| 里：提常数，得负幂为 0 的整幂级数；
    inside=False →  在 |z| > |a| 里：提 1/z，只剩负幂项。

    提示：两条式子都是几何级数 1/(1-w) = Σw^n 换元来的：
        |z|<|a|:  1/(z-a) = -(1/a)·1/(1-z/a)
        |z|>|a|:  1/(z-a) = (1/z)·1/(1-a/z)
    系数该怎么排（哪个 k 放哪一项、分母是 a 的几次方），自己从这两行推。
    """
    raise NotImplementedError('第 7 步还没写：geom_coeffs —— 见 lab/README.md 任务表第 7 行')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def ring_coeffs(a, b, ring, n_max=8):
    """1/((z-a)(z-b)) 在指定环域里的系数表 {k: c_k}（展开中心是原点）。

    ring 取三个字符串之一，按奇点到原点的距离分级：
        'inner'  →  |z| < |a|          两项都在圆内，都提常数
        'middle' →  |a| < |z| < |b|    近的那项提 1/z，远的那项提常数
        'outer'  →  |z| > |b|          两项都在圆外，都提 1/z
    （a、b 谁近谁远由 |a|、|b| 自己比，函数里先排一下，别假设 a 更近。）

    提示：先第 6 步拆部分分式拿到两个权重，再对每个奇点用第 7 步的系数表，
    乘上权重后按 k 累加进同一张表——同一个 k 的两项要相加，不是覆盖。
    """
    raise NotImplementedError('第 8 步还没写：ring_coeffs —— 见 lab/README.md 任务表第 8 行')
