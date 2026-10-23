#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cauchy_tool.py 的测试：跑 python test_cauchy_tool.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_cauchy_tool.py -k step3

-k 后面写测试名里的一段：step1 … step9。
留白没填时这些测试会报 NotImplementedError，那不是环境坏了，是那一步还没写。
"""

import cmath
import math
import unittest

import cauchy_tool as tool

TOL = 1e-6          # 公式值（含数值求导）与理论值的容差
TOL_NUM = 1e-9      # 纯数值围道积分与理论值的容差
TOL_LOOSE = 1e-4    # 对「数值围道积分」再求一次导的那种检查
TAU = 2j * math.pi

# 课件里那几道题：(名字, 被积函数, 圆心, 半径, [(g, 奇点, 幂次)], 理论值)
EXAM_CASES = [
    ('西建大四大题①  z/(z-1)', lambda z: z / (z - 1), 0j, 2,
     [(lambda z: z, 1 + 0j, 1)], TAU),
    ('西建大四大题②  cos z/(z-i)³', lambda z: cmath.cos(z) / (z - 1j) ** 3, 1j, 1,
     [(cmath.cos, 1j, 3)], -math.pi * 1j * cmath.cos(1j)),
    ('2022 B 卷填空  (1+z+z²)/z³', lambda z: (1 + z + z * z) / z ** 3, 0j, 1,
     [(lambda z: 1 + z + z * z, 0j, 3)], TAU),
    ('奇点在圈外  e^z/(z-3)', lambda z: cmath.exp(z) / (z - 3), 0j, 1,
     [(cmath.exp, 3 + 0j, 1)], 0),
    ('2024 年 10 分题  cos z/(z²(z+i))',
     lambda z: cmath.cos(z) / (z * z * (z + 1j)), 0j, 2,
     [(lambda z: cmath.cos(z) / (z + 1j), 0j, 2),
      (lambda z: cmath.cos(z) / (z * z), -1j, 1)],
     TAU * (1 - cmath.cos(1j))),
    ('2022 年 10 分题  e^{iz}/(z²-3πz+2π²)',
     lambda z: cmath.exp(1j * z) / (z * z - 3 * math.pi * z + 2 * math.pi ** 2),
     3 + 0j, 4,
     [(lambda z: cmath.exp(1j * z) / (z - 2 * math.pi), math.pi + 0j, 1),
      (lambda z: cmath.exp(1j * z) / (z - math.pi), 2 * math.pi + 0j, 1)],
     4j),
]


class Base(unittest.TestCase):
    """共同的比对工具：数值围道积分有误差，一律按容差比。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}'.format(msg, expected, actual))


class Step1_围道采样(Base):
    """z_k = center + r·e^{i·2πk/n}：从 center+r 出发、逆时针。"""

    def test_step1_n4(self):
        # 半径 2、四个点：2, 2i, -2, -2i
        got = tool.circle_points(0j, 2, 4)
        self.assertEqual(len(got), 4, 'n=4 应该正好 4 个点')
        for k, want in enumerate([2 + 0j, 2j, -2 + 0j, -2j]):
            self.assertNear(got[k], want, '第 {} 个采样点'.format(k), tol=TOL_NUM)

    def test_step1_modulus_and_center(self):
        # 每个点到圆心的距离都等于半径；点的平均落在圆心（单位根之和为零）
        got = tool.circle_points(3 + 0j, 4, 8)
        self.assertEqual(len(got), 8)
        for k, z in enumerate(got):
            self.assertNear(abs(z - 3), 4, '第 {} 个点到圆心的距离'.format(k), tol=TOL_NUM)
        self.assertNear(sum(got) / len(got), 3 + 0j, 'n 个点的平均应落在圆心', tol=TOL_NUM)

    def test_step1_direction(self):
        # 相邻两点的差要转 +2π/n：逆时针才是正向
        n = 6
        got = tool.circle_points(1 + 1j, 2, n)
        self.assertNear(got[0], 1 + 1j + 2, '第一个点必须是 center + radius', tol=TOL_NUM)
        ratio = (got[1] - (1 + 1j)) / (got[0] - (1 + 1j))
        self.assertNear(ratio, cmath.exp(1j * 2 * math.pi / n),
                        '相邻两点的角差（逆时针为正）', tol=TOL_NUM)


class Step2_数值围道积分(Base):
    """∮_C f dz 用梯形求和：每一项都乘 i·Δθ·(z_k - center)。"""

    def test_step2_unit_pole(self):
        self.assertNear(tool.contour_integral(lambda z: 1 / z, 0j, 2), TAU,
                        '∮_{|z|=2} dz/z', tol=TOL_NUM)

    def test_step2_analytic_is_zero(self):
        self.assertNear(tool.contour_integral(lambda z: z ** 2, 0j, 2), 0,
                        '∮_{|z|=2} z² dz', tol=TOL_NUM)
        self.assertNear(tool.contour_integral(lambda z: 3 + 0j, 0j, 2), 0,
                        '∮_{|z|=2} 3 dz（dz 那一项不能漏）', tol=TOL_NUM)

    def test_step2_shifted_circle(self):
        self.assertNear(tool.contour_integral(lambda z: 1 / (z - 3), 3 + 0j, 1), TAU,
                        '∮_{|z-3|=1} dz/(z-3)', tol=TOL_NUM)

    def test_step2_pole_outside(self):
        self.assertNear(tool.contour_integral(lambda z: cmath.exp(z) / (z - 3), 0j, 2), 0,
                        '奇点在圈外：∮_{|z|=2} e^z/(z-3) dz', tol=TOL_NUM)


class Step3_奇点内外(Base):
    """|z0 - center| < radius 才算圈内；压在围道上的点不算。"""

    def test_step3_inside(self):
        for z0, center, radius in ((1 + 0j, 0j, 2), (-1 + 0j, 0j, 2), (1j, 0j, 2),
                                   (math.pi + 0j, 3 + 0j, 4), (2 * math.pi + 0j, 3 + 0j, 4)):
            self.assertTrue(tool.inside(z0, center, radius),
                            '{} 应在 |z-{}|={} 的圈内'.format(z0, center, radius))

    def test_step3_outside(self):
        for z0, center, radius in ((3 + 0j, 0j, 2), (3 + 4j, 0j, 4)):
            self.assertFalse(tool.inside(z0, center, radius),
                             '{} 应在 |z-{}|={} 的圈外'.format(z0, center, radius))

    def test_step3_on_contour(self):
        # 距离恰好等于半径：落在围道上，两条公式都不适用
        self.assertFalse(tool.inside(2 + 0j, 0j, 2), 'z0=2 在 |z|=2 上，不算圈内')
        self.assertFalse(tool.inside(-2 + 0j, 0j, 2), 'z0=-2 在 |z|=2 上，不算圈内')


class Step4_数值求导(Base):
    """g^{(m-1)} 用中心差分求；二阶差分要除以 h*h。"""

    def test_step4_order1(self):
        self.assertNear(tool.deriv_n(lambda z: z ** 2, 1 + 2j, 1), 2 + 4j,
                        "(z²)' 在 1+2j 处")

    def test_step4_order2(self):
        # (cos z)'' = -cos z
        self.assertNear(tool.deriv_n(cmath.cos, 1j, 2), -cmath.cos(1j),
                        "(cos z)'' 在 z=i 处")
        self.assertNear(tool.deriv_n(cmath.exp, 0j, 2), 1, "(e^z)'' 在 z=0 处")
        self.assertNear(tool.deriv_n(cmath.sin, 0j, 2), 0, "(sin z)'' 在 z=0 处")

    def test_step4_order0(self):
        # 0! = 1：零阶导就是取值本身
        self.assertNear(tool.deriv_n(cmath.exp, 1 + 1j, 0), cmath.exp(1 + 1j),
                        '(e^z) 在 1+i 处的零阶导', tol=TOL_NUM)


class Step5_柯西公式那一项(Base):
    """分母一次方：2πi·g(z0)。"""

    def test_step5_direct(self):
        self.assertNear(tool.cauchy_value(lambda z: z, 1 + 0j), TAU, 'g(z)=z 在 z0=1')
        self.assertNear(tool.cauchy_value(cmath.cos, 1j), TAU * cmath.cos(1j),
                        'g(z)=cos z 在 z0=i')
        self.assertNear(tool.cauchy_value(lambda z: z * z + 1, 0j), TAU,
                        'g(z)=z²+1 在 z0=0')


class Step6_高阶导数那一项(Base):
    """分母 m 次方：2πi/(m-1)! · g^{(m-1)}(z0)，三处都用 m-1。"""

    def test_step6_m3(self):
        # m=3：二阶导、系数 2πi/2!
        self.assertNear(tool.high_order_value(cmath.cos, 1j, 3), -math.pi * 1j * cmath.cos(1j),
                        'm=3、g=cos z、z0=i')

    def test_step6_m2(self):
        # m=2：一阶导、系数 2πi/1!
        self.assertNear(tool.high_order_value(lambda z: z ** 3, 1 + 0j, 2), 6 * math.pi * 1j,
                        'm=2、g=z³、z0=1')

    def test_step6_polynomial_m3(self):
        # 2022 B 卷填空：(1+z+z²)/z³，二阶导是常数 2
        self.assertNear(tool.high_order_value(lambda z: 1 + z + z * z, 0j, 3), TAU,
                        'm=3、g=1+z+z²、z0=0')

    def test_step6_constant_is_zero(self):
        # 2023 B 卷填空：分子是常数，求任何正阶导都得 0，答案就是 0
        self.assertNear(tool.high_order_value(lambda z: 1 + 0j, -1j, 3), 0,
                        'm=3、g≡1、z0=-i')


class Step7_幂次决定用哪个(Base):
    """m=1 走柯西积分公式，m≥2 走高阶导数公式。"""

    def test_step7_m1_same_as_cauchy(self):
        self.assertNear(tool.formula_value(cmath.exp, 1 + 0j, 1), TAU * math.e,
                        'm=1：∮ e^z/(z-1) dz')
        self.assertNear(tool.formula_value(cmath.exp, 1 + 0j, 1),
                        tool.cauchy_value(cmath.exp, 1 + 0j),
                        'm=1 必须走柯西积分公式那一路', tol=TOL_NUM)

    def test_step7_m3_same_as_high_order(self):
        self.assertNear(tool.formula_value(cmath.cos, 1j, 3),
                        tool.high_order_value(cmath.cos, 1j, 3),
                        'm=3 必须走高阶导数公式那一路', tol=TOL_NUM)

    def test_step7_m2(self):
        self.assertNear(tool.formula_value(lambda z: z * z, 1 + 1j, 2),
                        TAU * 2 * (1 + 1j), 'm=2：∮ z²/(z-(1+i))² dz')
        self.assertNear(tool.formula_value(lambda z: z * z, 1 + 1j, 1),
                        TAU * (1 + 1j) ** 2, 'm=1：∮ z²/(z-(1+i)) dz')


class Step8_两项相加(Base):
    """圈内每个奇点各一项，全部相加；圈外的项就是 0。"""

    def test_step8_two_poles(self):
        # 课件那道 10 分题：∮_{|z|=3} (2z+1)/(z²+z-2) dz = 4πi
        terms = [(lambda z: (2 * z + 1) / (z + 2), 1 + 0j, 1),
                 (lambda z: (2 * z + 1) / (z - 1), -2 + 0j, 1)]
        self.assertNear(tool.contour_total(terms, 0j, 3), 4 * math.pi * 1j,
                        '两个奇点都圈住时的合计')
        self.assertNear(tool.contour_total(terms, 0j, 3),
                        tool.formula_value(terms[0][0], 1 + 0j, 1)
                        + tool.formula_value(terms[1][0], -2 + 0j, 1),
                        '合计必须等于两项相加（少算一项就在这里露出来）', tol=TOL_NUM)

    def test_step8_outside_is_zero(self):
        # 换一条圈不进去的围道：答案从 8πi 变 0
        terms = [(lambda z: z + 1, 3 + 0j, 1)]
        self.assertNear(tool.contour_total(terms, 0j, 5), 8 * math.pi * 1j, '|z|=5 圈住 3')
        self.assertNear(tool.contour_total(terms, 0j, 1), 0, '|z|=1 圈不住 3')

    def test_step8_cancel(self):
        # ∮_{|z|=2} dz/(z²-1)：两项 πi 与 -πi，和是 0
        terms = [(lambda z: 1 / (z + 1), 1 + 0j, 1),
                 (lambda z: 1 / (z - 1), -1 + 0j, 1)]
        self.assertNear(tool.contour_total(terms, 0j, 2), 0, '两项抵消的合计')
        self.assertNear(tool.contour_total(terms, 0j, 2),
                        math.pi * 1j + (-math.pi * 1j), '两项相加，不是相减', tol=TOL_NUM)


class Step9_整表自检(Base):
    """把课件里那几道考试题跑一遍：数值围道积分与公式值互相对上。"""

    def test_step9_exam_table(self):
        for name, f, center, radius, terms, want in EXAM_CASES:
            self.assertNear(tool.contour_integral(f, center, radius), want,
                            '{}：数值围道积分'.format(name), tol=TOL)
            self.assertNear(tool.contour_total(terms, center, radius), want,
                            '{}：按公式两项相加'.format(name), tol=TOL)

    def test_step9_reverse_formula(self):
        # 2023 年选择题：f(z)=∮_{|ζ|=4}(sinζ-cosζ)/(ζ-z)dζ = 2πi(sin z - cos z)
        g = lambda w: cmath.sin(w) - cmath.cos(w)
        f = lambda z: tool.contour_integral(lambda w: g(w) / (w - z), 0j, 4)
        self.assertNear(f(math.pi + 0j), TAU * g(math.pi), 'f(π) = 2πi·g(π)', tol=TOL)
        h = 1e-3
        self.assertNear((f(math.pi + h) - f(math.pi - h)) / (2 * h), -TAU,
                        "f'(π) = 2πi·g'(π)", tol=TOL_LOOSE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
