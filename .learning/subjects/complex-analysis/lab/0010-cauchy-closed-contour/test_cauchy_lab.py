#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cauchy_lab.py 的测试：跑 python test_cauchy_lab.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_cauchy_lab.py -k step5

-k 后面写测试名里的一段：step1 … step8。
留白没填时这些测试会报 NotImplementedError，那不是环境坏了，是那一步还没写。

两类容差是分开的：
  · 柯西定理那几行（积分为 0）用 1e-6——解析就有原函数，和式会望远镜式抵干净；
  · 等于 2πi / πi 那几行用 2e-2——折线代替圆弧，实部会留下 O(1/n) 的残渣。
"""

import cmath
import math
import unittest

import cauchy_lab as lab

TWO_PI_I = 2j * math.pi     # 2πi：正向绕一圈、圈里有一个一阶奇点
PI_I = 1j * math.pi         # πi：半圈


class Base(unittest.TestCase):
    """共同的比对工具：所有数值比对都走这里，容差分两档。"""

    def assertNear(self, actual, expected, msg='', tol=lab.TOL_VALUE):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}（差 {}）'
                             .format(msg, expected, actual, abs(actual - expected)))

    def assertZero(self, value, msg='', tol=lab.TOL_ZERO):
        self.assertLessEqual(abs(value), tol,
                             '{}：应当≈0，实际 {}（模 {}）'.format(msg, value, abs(value)))


class Step1_圆周采样(Base):
    """circle_contour：逆时针、n 个点、首点不重复写两遍。"""

    def test_step1_first_point(self):
        pts = lab.circle_contour(0j, 1, 8)
        self.assertNear(pts[0], 1 + 0j, '起点应是 center + radius', tol=1e-12)

    def test_step1_count_and_no_repeat(self):
        pts = lab.circle_contour(0j, 1, 8)
        self.assertEqual(len(pts), 8, 'n=8 就该返回 8 个点（首点别重复写进末尾）')
        self.assertGreaterEqual(abs(pts[0] - pts[-1]), 1e-6,
                                '末点与首点不能重合——闭合那一段归第 3 步管')

    def test_step1_radius_and_center(self):
        center, radius = 2 + 1j, 0.5
        for z in lab.circle_contour(center, radius, 16):
            self.assertLessEqual(abs(abs(z - center) - radius), 1e-12,
                                 '点 {} 到圆心的距离不是 {}'.format(z, radius))

    def test_step1_counterclockwise(self):
        # n=4：0°→90°，第一步必须朝「上」走；写成顺时针这一步就朝下
        pts = lab.circle_contour(0j, 1, 4)
        self.assertGreater(cmath.phase(pts[1] - pts[0]), 0, '方向反了：这里要逆时针（正向）')
        self.assertNear(pts[1], 1j, 'n=4 时第二个点是 i', tol=1e-12)

    def test_step1_default_n(self):
        self.assertEqual(len(lab.circle_contour(0j, 1)), lab.DEFAULT_N,
                         '不传 n 时用 DEFAULT_N')


class Step2_开路径积分(Base):
    """contour_integral：每小段用左端点的函数值乘这一段的 Δz，末点没有下一段。"""

    def test_step2_constant(self):
        pts = [0j, 1 + 0j, 2 + 1j]
        self.assertNear(lab.contour_integral(lambda z: 1 + 0j, pts), 2 + 1j,
                        '常数 1 的积分就是「终点 − 起点」', tol=1e-9)

    def test_step2_last_point_has_no_segment(self):
        # 单位圆前三个点 1 → i → -1：f==1 时只加两段，得 -2（不是 0）
        pts = lab.circle_contour(0j, 1, 4)[:3]
        self.assertNear(lab.contour_integral(lambda z: 1 + 0j, pts), -2 + 0j,
                        '开路径只求和到倒数第二个点为止', tol=1e-9)

    def test_step2_left_endpoint_rule(self):
        # f(z)=z 在 [0, 1, 2] 上：左端点式得 0*1 + 1*1 = 1（用右端点会得 3）
        got = lab.contour_integral(lambda z: z, [0j, 1 + 0j, 2 + 0j])
        self.assertNear(got, 1 + 0j, '每段的被积函数值取在左端点', tol=1e-12)

    def test_step2_reverse_sign(self):
        pts = lab.circle_contour(0j, 1, 16)
        f = lambda z: 1 + 0j
        self.assertNear(lab.contour_integral(f, pts[::-1]),
                        -lab.contour_integral(f, pts),
                        '同一条路反着走，积分变号', tol=1e-9)


class Step3_闭路积分(Base):
    """closed_integral：把末点接回首点。柯西定理在这一步变成可跑的数。"""

    def test_step3_analytic_zero(self):
        for f, name in ((lambda z: z ** 2, 'z^2'), (cmath.exp, 'e^z'), (cmath.sin, 'sin z')):
            self.assertZero(lab.closed_integral(f, lab.circle_contour(0j, 1, 512)),
                            name + ' 沿 |z|=1 正向')

    def test_step3_analytic_off_center(self):
        # 围道挪个位置、换个半径：解析就还是 0
        self.assertZero(lab.closed_integral(cmath.exp, lab.circle_contour(1 + 1j, 2, 512)),
                        'e^z 沿 |z-(1+i)|=2')

    def test_step3_pole_outside(self):
        # 1/(z-2) 的奇点在 |z|=1 外面，圈内解析 ⇒ 积分 0
        self.assertZero(lab.closed_integral(lambda z: 1 / (z - 2), lab.circle_contour(0j, 1, 512)),
                        '1/(z-2) 沿 |z|=1：奇点在圈外')

    def test_step3_one_over_z(self):
        value = lab.closed_integral(lambda z: 1 / z, lab.circle_contour(0j, 2, 4096))
        self.assertNear(value, TWO_PI_I, '1/z 沿 |z|=2 正向')
        self.assertLessEqual(abs(value.real), 1e-2,
                             '实部那点残渣是折线代替圆弧的误差（约 −π²/n），'
                             '算不出来说明连 2πi 都没对上')

    def test_step3_missing_wrap(self):
        # 忘了接回首点会怎样：望远镜式抵不干净，z^2 也不再是 0
        broken = lab.contour_integral(lambda z: z ** 2, lab.circle_contour(0j, 1, 128))
        self.assertGreater(abs(broken), 1e-3,
                           '不闭合时 z^2 的积分明显不为 0——首尾相接那一段不能省')


class Step4_判零(Base):
    """nearly_zero：卷面上的「写 0」，代码里必须带容差。"""

    def test_step4_true(self):
        self.assertTrue(lab.nearly_zero(0 + 0j))
        self.assertTrue(lab.nearly_zero(1e-15), '1e-15 在 1e-6 容差内算 0')
        self.assertTrue(lab.nearly_zero(-7e-8))

    def test_step4_false(self):
        self.assertFalse(lab.nearly_zero(0.0096), '折线代替圆弧的残渣不算 0')
        self.assertFalse(lab.nearly_zero(TWO_PI_I), '2πi 当然不是 0')

    def test_step4_tol_is_parameter(self):
        self.assertFalse(lab.nearly_zero(1e-3, tol=1e-6))
        self.assertTrue(lab.nearly_zero(1e-3, tol=1e-2),
                        'tol 传大了就该判成 0——容差要能从外面调')


class Step5_复合闭路(Base):
    """composite_integral：外圈正向、内圈反向，等于「外圈减内圈」。"""

    ANNULUS = dict(center=0j, r_out=2, r_in=1, n=1024)

    def test_step5_annulus_zero(self):
        # 1/z 在圆环 1<|z|<2 里解析（洞把原点让出去了）⇒ 沿复合闭路积分 0
        got = lab.composite_integral(lambda z: 1 / z, **self.ANNULUS)
        self.assertZero(got, '1/z 沿复合闭路（外 |z|=2 正向 + 内 |z|=1 反向）')

    def test_step5_outer_equals_inner(self):
        # 两个圈都取正向时各是 2πi；正因如此，内圈在复合闭路里必须反向才抵得掉
        outer = lab.closed_integral(lambda z: 1 / z, lab.circle_contour(0j, 2, 1024))
        inner = lab.closed_integral(lambda z: 1 / z, lab.circle_contour(0j, 1, 1024))
        self.assertNear(outer, TWO_PI_I, '外圈单独取的积分')
        self.assertNear(inner, TWO_PI_I, '内圈单独取（正方向）也是 2πi')
        self.assertNear(outer - inner, 0 + 0j, '外圈减内圈才抵成 0', tol=lab.TOL_ZERO)

    def test_step5_pole_in_hole(self):
        # 奇点 0.5 落在洞里（|0.5|<1），圆环内照样解析
        got = lab.composite_integral(lambda z: 1 / (z - 0.5), **self.ANNULUS)
        self.assertZero(got, '1/(z-0.5) 沿复合闭路：奇点在洞里')

    def test_step5_off_center(self):
        # 圆心不在原点也一样：奇点就是圆心自己，洞把它让出去
        got = lab.composite_integral(lambda z: 1 / (z - 2), center=2 + 0j,
                                     r_out=1, r_in=0.5, n=1024)
        self.assertZero(got, '1/(z-2) 沿以 2 为心的复合闭路')


class Step6_圆弧采样(Base):
    """arc_contour：n+1 个点，首末点都在；θ 往回走就是反向。"""

    def test_step6_endpoints(self):
        pts = lab.arc_contour(0j, 1, 0, math.pi, 8)
        self.assertEqual(len(pts), 9, 'n 段弧应有 n+1 个点')
        self.assertNear(pts[0], 1 + 0j, '首点是 θ0 那一端', tol=1e-12)
        self.assertNear(pts[-1], -1 + 0j, '末点是 θ1 那一端', tol=1e-12)

    def test_step6_on_circle(self):
        center, radius = 1 + 0j, 2
        pts = lab.arc_contour(center, radius, 0.3, 2.0, 10)
        for z in pts:
            self.assertLessEqual(abs(abs(z - center) - radius), 1e-12,
                                 '点 {} 不在以 {} 为心、{} 为半径的圆上'.format(z, center, radius))
        self.assertGreater(cmath.phase(pts[1] - center), cmath.phase(pts[0] - center),
                           'θ 递增时点的角也跟着递增')

    def test_step6_reverse(self):
        forward = lab.arc_contour(0j, 1, 0, math.pi, 8)
        backward = lab.arc_contour(0j, 1, math.pi, 0, 8)
        for a, b in zip(forward, backward[::-1]):
            self.assertLessEqual(abs(a - b), 1e-12, '反向弧应当就是正向弧倒着读')


class Step7_弧上积分(Base):
    """arc_integral：1/z 沿半圆弧——上半圈得 πi、下半圈得 −πi。"""

    def test_step7_upper_half(self):
        got = lab.arc_integral(lambda z: 1 / z, 0j, 1, 0, math.pi, n=4096)
        self.assertNear(got, PI_I, '1/z 沿 |z|=1 从 1 上半圈走到 -1')

    def test_step7_lower_half(self):
        got = lab.arc_integral(lambda z: 1 / z, 0j, 1, 0, -math.pi, n=4096)
        self.assertNear(got, -PI_I, '1/z 沿 |z|=1 从 1 下半圈走到 -1（arg 走负的那一支）')

    def test_step7_reverse_sign(self):
        f = lambda z: 1 / z
        forward = lab.arc_integral(f, 0j, 1, 0, math.pi, n=2048)
        backward = lab.arc_integral(f, 0j, 1, math.pi, 0, n=2048)
        self.assertNear(backward, -forward, '同一段弧反着走，积分变号', tol=1e-2)


class Step8_整表自检(Base):
    """不用填。把课件那张「圈里有没有奇点」的表跑一遍：三张表都对得上才算真做完。"""

    def test_step8_cauchy_table(self):
        circle = lab.circle_contour(0j, 1, 1024)
        rows = [
            (lambda z: z ** 2, 'zero', 'z^2'),
            (cmath.exp, 'zero', 'e^z'),
            (cmath.sin, 'zero', 'sin z'),
            (lambda z: 1 / (z - 2), 'zero', '1/(z-2)（奇点在圈外）'),
            (lambda z: 1 / z, 'two_pi_i', '1/z（奇点在圈内）'),
            (lambda z: z.conjugate(), 'two_pi_i', 'z̄（处处不解析）'),
            (lambda z: z.real, 'pi_i', 'Re z（不解析）'),
        ]
        for f, want, name in rows:
            got = lab.closed_integral(f, circle)
            if want == 'zero':
                self.assertZero(got, name + ' 沿 |z|=1')
            elif want == 'two_pi_i':
                self.assertNear(got, TWO_PI_I, name + ' 沿 |z|=1')
            else:
                self.assertNear(got, PI_I, name + ' 沿 |z|=1')

    def test_step8_composite_table(self):
        outer = lab.closed_integral(lambda z: 1 / z, lab.circle_contour(0j, 2, 1024))
        inner = lab.closed_integral(lambda z: 1 / z, lab.circle_contour(0j, 1, 1024))
        composite = lab.composite_integral(lambda z: 1 / z, 0j, 2, 1, 1024)
        self.assertNear(outer, TWO_PI_I, '外圈 |z|=2')
        self.assertNear(inner, TWO_PI_I, '内圈 |z|=1（正方向）')
        self.assertZero(composite, '复合闭路')
        self.assertTrue(lab.nearly_zero(outer - inner), '复合闭路定理那一行：外圈 − 内圈 = 0')

    def test_step8_branch_table(self):
        # 同一对端点 1 → -1，走上半圈得 πi、下半圈得 −πi，两者差 2πi
        f = lambda z: 1 / z
        up = lab.arc_integral(f, 0j, 1, 0, math.pi, n=4096)
        down = lab.arc_integral(f, 0j, 1, 0, -math.pi, n=4096)
        self.assertNear(up - down, 2 * PI_I, '上下两支差 2πi（Ln z 的分支差异）')


if __name__ == '__main__':
    unittest.main(verbosity=2)
