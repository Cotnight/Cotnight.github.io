#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变计算工具 · 0014：留数与留数定理（参考解）

把它拷进 ``lab/0014-residue-contour/`` 覆盖同名的留白文件，再跑
``python test_residue_lab.py``，就是全绿。

这个工具做的事只有一句：**把留数公式算出来的数，拿去和小圆上的数值围道积分对照。**
两种算法对得上，卷面上那一步才叫真的会。

两个约定先记住：
  · 围道一律先采样成点列，积分只在点列上做；圆周上 ``dz`` 用解析式
    ``i·Δθ·(z−a)``（而不是折线的 ``Δz``），这样梯形法能到机器精度。
  · 纸面上的 0 与精确值在代码里都是近似，所以判等一律带容差；
    两档容差的意义见 ``TOL_EXACT`` / ``TOL_VALUE`` 的注释。

只用标准库 ``cmath`` / ``math``，不需要装任何包。
"""

import cmath
import math

DEFAULT_N = 2048        # 一条圆周上采多少个点
DEFAULT_H = 1e-6        # 一阶数值导的步长
DEFAULT_H2 = 1e-4       # 二阶数值导的步长（除以 h^2，步长必须放大）
TOL_EXACT = 1e-9        # 围道积分这条路的容差：圆周上 dz 取解析式，误差到机器精度
TOL_VALUE = 1e-6        # 公式 + 数值求导这条路的容差：二阶中心差分留着 1e-8 量级的截断误差
TWO_PI = 2 * math.pi
TAU = 2j * math.pi      # 2πi：留数定理里那个乘法因子


# ══ 第 1 步 ═════════════════════════════════════════════════════
def circle_points(center, radius, n=DEFAULT_N):
    """正向（逆时针）圆周 |z − center| = radius 上等距的 n 个点。

    返回长度 n 的列表：第 k 个点是 center + radius * e^(i·2πk/n)，k = 0, 1, …, n−1。
    最后一个点与第一个点**差一步**（首点不要重复写进列表末尾），闭合那一段由积分里
    的 dz 公式负责——圆周是闭合的，dz 本身就是按整圈算的。

    提示：cmath.exp(1j * 角)，角一律按弧度。
    """
    return [center + radius * cmath.exp(1j * TWO_PI * k / n) for k in range(n)]


# ══ 第 2 步 ═════════════════════════════════════════════════════
def closed_integral(f, center, radius, n=DEFAULT_N):
    """数值围道积分 ∮_{|z−a|=r} f(z) dz（正向一整圈）。

    z = a + r e^(iθ) 求微分得 dz = i·r·e^(iθ) dθ = i·Δθ·(z − a)，Δθ = 2π/n。
    于是每一项是 f(z_k) * (1j * dtheta * (z_k - center))，n 项相加就是梯形法的和式。

    提示：漏掉 1j，∮dz/z 会算出 2π（实数）；漏掉 (z_k − center)，常数被积函数会
    算出 2πi 而不是 0。
    """
    points = circle_points(center, radius, n)
    dtheta = TWO_PI / n
    return sum(f(z) * (1j * dtheta * (z - center)) for z in points)


# ══ 第 3 步 ═════════════════════════════════════════════════════
def inside(z0, center, radius):
    """奇点 z0 在围道 |z − center| = radius 的内部吗？

    **用严格小于**：距离恰好等于半径时奇点压在围道上，留数定理的两条前提
    （奇点不在 C 上、在 C 内）都不满足，这一步必须把那种点判成「不算圈内」。

    这一行就是卷面上「圈内的奇点数一数」那个动作的代码版；写成点与圆心的距离
    而不是 |z0|，圆心不在原点时才不会数错。
    """
    return abs(z0 - center) < radius


# ══ 第 4 步 ═════════════════════════════════════════════════════
def poly_eval(coeffs, z):
    """多项式求值。coeffs 按**升幂**给：coeffs[k] 是 z^k 的系数。

    例：z^3 + 5z^2 + 8z + 4 写成 [4, 8, 5, 1]。
    用霍纳法从最高次系数往下卷：total 每次「乘 z 再加下一个系数」。

    提示：空列表当零多项式，返回 0。
    """
    total = 0j
    for c in reversed(coeffs):
        total = total * z + c
    return total


# ══ 第 5 步 ═════════════════════════════════════════════════════
def deriv_poly(coeffs):
    """多项式求导，结果仍按升幂给。

    z^k 求导得 k·z^(k−1)，所以新系数列表的第 k−1 项是 k * coeffs[k]，
    从 k = 1 起取到末尾。常数（只有 coeffs[0]）导成空列表，poly_eval 对它给 0。

    这一条只为一阶极点那条分式公式服务：Res = P(z0) / Q'(z0)。
    """
    return [k * coeffs[k] for k in range(1, len(coeffs))]


# ══ 第 6 步 ═════════════════════════════════════════════════════
def strip_factor(coeffs, z0, m):
    """把 (z − z0)^m 从多项式里除干净，返回剩下的商（升幂）。

    用综合除法（霍纳）反复除 m 次：除一次 (z − z0) 时，按降幂
    b[0] = d[0]、b[i] = d[i] + z0·b[i−1]，最后那一位 b[n] 是余数，
    前面 n 位就是商的系数。

    m 阶极点的公式要的就是这个商：分母 Q 除掉 (z−z0)^m 之后剩下的 Q̃ 在 z0
    处不为零，于是 (z−z0)^m·f = P/Q̃ 在 z0 解析——公式里的那个「括号内」。
    """
    q = list(coeffs)
    for _ in range(m):
        d = list(reversed(q))
        n = len(d) - 1
        if n <= 0:
            q = []
            break
        b = [d[0]]
        for i in range(1, n + 1):
            b.append(d[i] + z0 * b[i - 1])
        q = list(reversed(b[:n]))
    return q


# ══ 第 7 步 ═════════════════════════════════════════════════════
def deriv_n(g, z0, order):
    """g 在 z0 处的 0／1／2 阶数值导数。

    order = 0 直接返回 g(z0)——公式里 m = 1 那一行是「零阶导、直接代 z0」，
    对应 0! = 1，这一条写不出来分不开两条极点公式。

    一阶用中心差分 (g(z0+h) − g(z0−h)) / 2h，步长 DEFAULT_H；
    二阶用 (g(z0+h) − 2g(z0) + g(z0−h)) / h²，步长必须换成 DEFAULT_H2——
    除以 h² 会把舍入误差放大，10^-6 的步长误差会涨到 10^-3 量级。

    提示：数值导不是精确值，二阶差分的截断误差在 1e-8 量级，容差就是为它留的。
    """
    if order == 0:
        return g(z0)
    if order == 1:
        return (g(z0 + DEFAULT_H) - g(z0 - DEFAULT_H)) / (2 * DEFAULT_H)
    if order == 2:
        return (g(z0 + DEFAULT_H2) - 2 * g(z0) + g(z0 - DEFAULT_H2)) / DEFAULT_H2 ** 2
    raise ValueError('本工具只做到二阶导：order 只接受 0／1／2')


# ══ 第 8 步 ═════════════════════════════════════════════════════
def residue_simple(num, den, z0):
    """一阶极点处的留数，分式版本：f = P/Q，P(z0) ≠ 0，Q(z0) = 0、Q'(z0) ≠ 0。

        Res = P(z0) / Q'(z0)

    num 是分子 P 的系数（升幂），den 是分母 Q 的系数（升幂）。
    一行：poly_eval(num, z0) / poly_eval(deriv_poly(den), z0)。

    这一条就是填空那 3 分（tan z 在 π/2、sin z / z^3 那类）的算法；
    Q'(z0) = 0 说明 z0 是分母的重根，一阶公式不适用，该回去重新定阶。
    """
    return poly_eval(num, z0) / poly_eval(deriv_poly(den), z0)


# ══ 第 9 步 ═════════════════════════════════════════════════════
def residue_pole_m(num, den, z0, m):
    """m 阶极点处的留数。

        Res = (1/(m−1)!) · lim_{z→z0} d^{m−1}/dz^{m−1} [ (z−z0)^m f(z) ]

    三件事按顺序做，对应公式的三格：
      1. strip_factor(den, z0, m) 得到 Q̃，括号内那个函数 g = P/Q̃ 在 z0 解析；
      2. deriv_n(g, z0, m−1) 求 m−1 阶导；
      3. 除以 math.factorial(m − 1)。

    m = 1 时它退化成 limit_mul(f, z0) = g(z0)，与一阶公式是同一条式子
    （0! = 1，零阶导就是函数本身）。
    """
    q_reduced = strip_factor(den, z0, m)

    def g(z):
        return poly_eval(num, z) / poly_eval(q_reduced, z)

    return deriv_n(g, z0, m - 1) / math.factorial(m - 1)


# ══ 第 10 步 ════════════════════════════════════════════════════
def residue_by_integral(f, z0, radius=0.5, n=DEFAULT_N):
    """兜底算法：留数就是洛朗展开的 c₋₁，所以

        Res = (1/2πi) ∮_{|z−z0|=ρ} f(z) dz

    在小圆上积一圈除以 2πi 就得到它。本性奇点只有这一条路（没有极限式可套），
    其他类型的奇点也都能用它复核——这就是「展开读 c₋₁」的数值版本。

    radius 要小到圈内只剩 z0 这一个奇点；n 取 DEFAULT_N 时，
    被积函数在环域里解析的话误差到机器精度。
    """
    return closed_integral(f, z0, radius, n) / TAU


# ══ 第 11 步 ════════════════════════════════════════════════════
def contour_by_residues(poles, center, radius):
    """留数定理：∮_C f dz = 2πi ·（圈内各奇点的留数之和）。

    poles 是一串配方 (奇点位置, 该点的留数)，已经算好的。
    只把 inside(z0, center, radius) 为真的那些加起来，再乘 TAU。
    圈外的项一律不算——这是「围道圈住几个奇点」那一步。

    提示：漏乘 TAU 会得到留数之和（差 2πi）；把圈外的也算进来是最常见的失分。
    """
    total = sum(res for z0, res in poles if inside(z0, center, radius))
    return TAU * total


# ══ 第 12 步 ════════════════════════════════════════════════════
def contour_missing_poles(poles, center, radius):
    """**故意写错的那一版**：圈内有几个奇点，它只算第一个就返回。

    这不是要你用的函数，是要你拿它当对照组：它对应卷面上「围道内有两个奇点
    只算一个」那个失分点。第 12 步的断言要求它算出来的数**和正确值不同**，
    并且要求数值围道积分站在正确值那边。

    实现：遍历 poles，遇到第一个 inside 为真的就返回 TAU * 它的留数；
    一个都没有时返回 0j。
    """
    for z0, res in poles:
        if inside(z0, center, radius):
            return TAU * res
    return 0j
