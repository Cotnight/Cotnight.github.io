#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""laurent_tool.py 的测试：跑 python test_laurent_tool.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_laurent_tool.py -k step3

-k 后面写测试名里的一段：step1 … step9。
留白没填时这些测试会报 NotImplementedError，那不是环境坏了，是那一步还没写。

数都不是随手写的：每一条期望值都能在纸上算出来（课件里那三条环域展开，
或者哈密工大卷那道圆环域洛朗展开的 10 分题）。
"""

import cmath
import math
import unittest

import laurent_tool as tool

TOL = 1e-8


class Base(unittest.TestCase):
    """共同的比对工具：数值积分有误差，一律按容差比。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}'.format(msg, expected, actual))


class Step1_围道采样(Base):
    """|z - center| = radius 上等距、逆时针的一圈点。"""

    def test_step1_count_and_radius(self):
        pts = tool.contour_points(1 + 2j, 0.5, 64)
        self.assertEqual(len(pts), 64, '取点个数应等于传入的 n')
        for p in pts:
            self.assertNear(abs(p - (1 + 2j)), 0.5, '每个点到圆心的距离应等于 radius')

    def test_step1_start_point(self):
        pts = tool.contour_points(2 - 1j, 1.5, 8)
        self.assertNear(pts[0], 3.5 - 1j, 'θ=0 处应当是 center + radius（不是圆心）')

    def test_step1_counterclockwise(self):
        pts = tool.contour_points(0j, 2.0, 16)
        turn = (pts[1] - 0j) / (pts[0] - 0j)
        self.assertNear(cmath.phase(turn), 2 * math.pi / 16,
                        '相邻两点转过的角应等于 +2π/n（负号就是顺时针了）')


class Step2_系数积分(Base):
    """c_k = (1/2πi)∮ f(ζ)/(ζ-center)^(k+1) dζ。dz 换元那一步最容易错。"""

    def test_step2_inner_c0(self):
        # |z|<1 里 f 展开成 Σ(1 - 1/2^{n+1}) z^n，c_0 = 1 - 1/2
        got = tool.coeff_integral(tool.f_lesson, 0, 0j, 0.5)
        self.assertNear(got, 0.5, 'c_0 = 1 - 1/2')

    def test_step2_inner_c1(self):
        # c_1 = 1 - 1/4
        got = tool.coeff_integral(tool.f_lesson, 1, 0j, 0.5)
        self.assertNear(got, 0.75, 'c_1 = 1 - 1/4')

    def test_step2_no_negative_power(self):
        # |z|<1 这一支是泰勒级数，c_{-1} 必须是 0（漏了 dz 换元会给错数）
        got = tool.coeff_integral(tool.f_lesson, -1, 0j, 0.5)
        self.assertNear(got, 0, '|z|<1 那条展开里没有负幂项')

    def test_step2_exp_factorial(self):
        # e^z 在 0 处：c_k = 1/k!，取 k=3 时是 1/6
        got = tool.coeff_integral(cmath.exp, 3, 0j, 1.0)
        self.assertNear(got, 1 / math.factorial(3), 'e^z 的 c_3 应等于 1/3!')


class Step3_一组系数(Base):
    """coeffs 只是循环：键要对，别把负号或半径写错。"""

    def test_step3_keys(self):
        got = tool.coeffs(tool.f_lesson, [0, 1, -2], 0j, 0.5)
        self.assertEqual(sorted(got), [-2, 0, 1], '键应正好是传入的那几个 k')

    def test_step3_middle_ring(self):
        # 1<|z|<2：c_0 = -1/2、c_1 = -1/4、c_{-1} = c_{-2} = -1
        got = tool.coeffs(tool.f_lesson, [0, 1, -1, -2], 0j, 1.5)
        self.assertNear(got[0], -0.5, '中间环域的 c_0')
        self.assertNear(got[1], -0.25, '中间环域的 c_1')
        self.assertNear(got[-1], -1, '中间环域的 c_{-1}')
        self.assertNear(got[-2], -1, '中间环域的 c_{-2}')

    def test_step3_outer_ring(self):
        # |z|>2：c_{-n} = 2^{n-1} - 1，所以 c_{-1}=0、c_{-2}=1、c_{-3}=3
        got = tool.coeffs(tool.f_lesson, [-1, -2, -3], 0j, 3.0)
        self.assertNear(got[-1], 0, '外环域的 c_{-1}')
        self.assertNear(got[-2], 1, '外环域的 c_{-2}')
        self.assertNear(got[-3], 3, '外环域的 c_{-3}')


class Step4_级数求和(Base):
    """series_value：正幂负幂一起算，空表返回 0。"""

    def test_step4_finite_table(self):
        # 0.5 - 1/z 在 z=2 处刚好是 0；空表就是 0
        self.assertNear(tool.series_value({0: 0.5, -1: -1.0}, 0j, 2 + 0j), 0,
                        '0.5 - 1/2 应等于 0')
        self.assertNear(tool.series_value({}, 0j, 1 + 1j), 0, '空表应返回 0，不是 None')

    def test_step4_negative_power(self):
        center = 1 + 0j
        z = 1 + 2j
        want = 3 * (z - center) ** 2 + 4 * (z - center) ** -2
        got = tool.series_value({2: 3, -2: 4}, center, z)
        self.assertNear(got, want, '中心不在原点时，负幂项也要按 z-center 算')

    def test_step4_taylor_sum(self):
        center = 0j
        z = 0.5 + 0j
        coeff_map = {k: tool.coeff_integral(cmath.exp, k, center, 1.0) for k in range(0, 4)}
        want = sum(z ** k / math.factorial(k) for k in range(0, 4))
        self.assertNear(tool.series_value(coeff_map, center, z), want,
                        'e^z 的前四项在 z=0.5 处的和')


class Step5_截断误差(Base):
    """项数够了误差就掉到机器精度，项数不够就是看得见的差。"""

    def test_step5_more_terms(self):
        cmap = {k: tool.coeff_integral(cmath.exp, k, 0j, 1.0) for k in range(0, 12)}
        got = tool.truncation_error(cmath.exp, cmap, 0j, 1 + 0j)
        self.assertLess(got, 1e-8, '取到 1/11! 那一项，误差应小于 1e-8')

    def test_step5_few_terms(self):
        cmap = {k: tool.coeff_integral(cmath.exp, k, 0j, 1.0) for k in range(0, 3)}
        got = tool.truncation_error(cmath.exp, cmap, 0j, 1 + 0j)
        self.assertGreater(got, 0.1, '只取到 1/2! 那一项，误差应在 10^-1 量级')

    def test_step5_outer_ring(self):
        # |z|>2 的负幂系数，取到 c_{-40}，在 z=3 处回代
        cmap = {k: tool.coeff_integral(tool.f_lesson, k, 0j, 3.0)
                for k in range(-40, 0)}
        got = tool.truncation_error(tool.f_lesson, cmap, 0j, 3 + 0j)
        self.assertLess(got, 1e-6, '外环域取 40 个负幂项后误差应小于 1e-6')


class Step6_部分分式(Base):
    """1/((z-a)(z-b)) = A/(z-a) + B/(z-b)：权重跟着 a、b 走。"""

    def test_step6_ab(self):
        a_weight, b_weight = tool.partial_fractions(1, 2)
        self.assertNear(a_weight, -1, '1/(z-1) 的权重')
        self.assertNear(b_weight, 1, '1/(z-2) 的权重')

    def test_step6_swapped(self):
        a_weight, b_weight = tool.partial_fractions(2, 1)
        self.assertNear(a_weight, 1, '交换 a、b 后 1/(z-2) 的权重')
        self.assertNear(b_weight, -1, '交换 a、b 后 1/(z-1) 的权重')

    def test_step6_identity(self):
        a_weight, b_weight = tool.partial_fractions(1, 2)
        for z in (0.3 + 0j, 1.5 + 0j, 5 + 0j):
            want = 1 / ((z - 1) * (z - 2))
            got = a_weight / (z - 1) + b_weight / (z - 2)
            self.assertNear(got, want, '在 z={} 处拆开前后应相等'.format(z))


class Step7_几何级数系数(Base):
    """1/(z-a) 两支：|z|<|a| 提常数（只有正幂），|z|>|a| 提 1/z（只有负幂）。"""

    def test_step7_inside(self):
        got = tool.geom_coeffs(2, True, 3)
        for k, want in ((0, -0.5), (1, -0.25), (2, -0.125), (3, -0.0625)):
            self.assertNear(got[k], want, '|z|<2 里 c_{}'.format(k))
        self.assertTrue(all(k >= 0 for k in got), '|z|<2 这一支不该有负幂项')

    def test_step7_outside(self):
        got = tool.geom_coeffs(2, False, 3)
        for k, want in ((-1, 1), (-2, 2), (-3, 4), (-4, 8)):
            self.assertNear(got[k], want, '|z|>2 里 c_{}'.format(k))
        self.assertTrue(all(k < 0 for k in got), '|z|>2 这一支不该有正幂项')

    def test_step7_sum_back(self):
        inside = tool.series_value(tool.geom_coeffs(2, True, 40), 0j, 0.5 + 0j)
        self.assertNear(inside, 1 / (0.5 - 2), '提常数那一支回代应等于 1/(z-2)')
        outside = tool.series_value(tool.geom_coeffs(2, False, 40), 0j, 5 + 0j)
        self.assertNear(outside, 1 / (5 - 2), '提 1/z 那一支回代应等于 1/(z-2)')

    def test_step7_against_contour(self):
        paper = tool.geom_coeffs(2, True, 2)
        numeric = tool.coeffs(lambda z: 1 / (z - 2), [0, 1, 2], 0j, 1.0)
        for k in (0, 1, 2):
            self.assertNear(numeric[k], paper[k],
                            '围道积分算的 c_{} 应与纸面系数一致'.format(k))


class Step8_环域系数(Base):
    """ring_coeffs：拆开、按环域选分支、同幂次相加。"""

    def test_step8_inner(self):
        got = tool.ring_coeffs(1, 2, 'inner', 5)
        self.assertNear(got[0], 0.5, '|z|<1 里 c_0 = 1 - 1/2')
        self.assertNear(got[1], 0.75, '|z|<1 里 c_1 = 1 - 1/4')
        self.assertTrue(all(k >= 0 for k in got), '|z|<1 这一支是泰勒级数，没有负幂项')

    def test_step8_middle(self):
        got = tool.ring_coeffs(1, 2, 'middle', 5)
        self.assertNear(got[-1], -1, '1<|z|<2 里 c_{-1} = -1')
        self.assertNear(got[0], -0.5, '1<|z|<2 里 c_0 = -1/2')
        self.assertNear(got[1], -0.25, '1<|z|<2 里 c_1 = -1/4')
        swapped = tool.ring_coeffs(2, 1, 'middle', 5)
        for k in got:
            self.assertNear(swapped[k], got[k], 'a、b 传反了，c_{} 不该变'.format(k))

    def test_step8_outer(self):
        got = tool.ring_coeffs(1, 2, 'outer', 4)
        for k, want in ((-1, 0), (-2, 1), (-3, 3), (-4, 7)):
            self.assertNear(got[k], want, '|z|>2 里 c_{}'.format(k))
        self.assertTrue(all(k < 0 for k in got), '|z|>2 这一支只剩负幂项')

    def test_step8_against_contour(self):
        radii = {'inner': 0.5, 'middle': 1.5, 'outer': 3.0}
        for ring, radius in radii.items():
            paper = tool.ring_coeffs(1, 2, ring, 4)
            ks = sorted(paper)
            numeric = tool.coeffs(tool.f_lesson, ks, 0j, radius)
            for k in ks:
                self.assertNear(numeric[k], paper[k],
                                '环域 {} 的 c_{} 应与围道积分一致'.format(ring, k))


class Step9_整表自检(Base):
    """把课件那三条展开与真题的两问整表跑一遍：工具对得上纸面结论，才算真做完。"""

    def test_step9_lesson_three_rings(self):
        # 课件那三条展开，系数按纸面公式现写（不经过你第 8 步的函数），拿去与围道积分对
        cases = []
        cases.append(('|z|<1', 0.5, {k: 1 - 2.0 ** (-(k + 1)) for k in range(0, 5)}))
        middle = {0: -0.5}
        middle.update({k: -2.0 ** (-(k + 1)) for k in range(1, 5)})
        middle.update({-m: -1.0 for m in range(1, 5)})
        cases.append(('1<|z|<2', 1.5, middle))
        cases.append(('|z|>2', 3.0, {-m: 2.0 ** (m - 1) - 1 for m in range(1, 7)}))
        for label, radius, paper in cases:
            for k in sorted(paper):
                self.assertNear(tool.coeff_integral(tool.f_lesson, k, 0j, radius), paper[k],
                                '{} 里 f 的 c_{}'.format(label, k))

    def test_step9_exam_question(self):
        # 合肥工大卷那道 10 分题：f(z) = (z+1)/(z-1)^2
        #   (1) 0<|z|<1：c_0 = 1，c_n = 2n+1（n≥1）
        #   (2) |z|>1 ：c_{-1} = 1，c_{-m} = 2m-1（m≥2）
        f = lambda z: (z + 1) / (z - 1) ** 2
        for k in range(0, 4):
            want = 1 if k == 0 else 2 * k + 1
            self.assertNear(tool.coeff_integral(f, k, 0j, 0.5), want,
                            '(1) 里 c_{} 应等于 {}'.format(k, want))
        for m in range(1, 5):
            want = 2 * m - 1
            self.assertNear(tool.coeff_integral(f, -m, 0j, 3.0), want,
                            '(2) 里 c_-{} 应等于 {}'.format(m, want))


if __name__ == '__main__':
    unittest.main(verbosity=2)
