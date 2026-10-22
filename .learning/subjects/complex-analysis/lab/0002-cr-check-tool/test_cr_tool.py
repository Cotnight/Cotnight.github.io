#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cr_tool.py 的测试：跑 python test_cr_tool.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_cr_tool.py -k step3

-k 后面写测试名里的一段：step1 … step9。
留白没填时这些测试会报 NotImplementedError，那不是环境坏了，是那一步还没写。
"""

import cmath
import unittest

import cr_tool as tool

TOL = 1e-4


class Base(unittest.TestCase):
    """共同的比对工具：数值差分有误差，一律按容差比。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}'.format(msg, expected, actual))


class Step1_沿y方向的差分(Base):
    """∂f/∂y。差分的步进方向与分母都跟 d_dx 不同。"""

    def test_step1_z2(self):
        # f(z)=z^2：f'(z)=2z，沿 y 求偏导应得 i*f'(z)=i*2z
        got = tool.d_dy(lambda z: z ** 2, 1 + 2j)
        self.assertNear(got, -4 + 2j, 'z^2 在 1+2j 处对 y 求偏导')

    def test_step1_zbar(self):
        # f(z)=conj(z)：u_y=0、v_y=-1，故 ∂f/∂y = -i
        got = tool.d_dy(lambda z: z.conjugate(), 0.5 + 0.3j)
        self.assertNear(got, -1j, 'z̄ 对 y 求偏导')


class Step2_两条残差(Base):
    """r1 = u_x - v_y，r2 = u_y + v_x。残差写反符号，后面全错。"""

    def test_step2_z2(self):
        # z^2 处处解析，两条残差都该是 0
        r1, r2 = tool.cr_residual(lambda z: z ** 2, 2 - 1j)
        self.assertNear(r1, 0, 'z^2 的 r1 = u_x - v_y')
        self.assertNear(r2, 0, 'z^2 的 r2 = u_y + v_x')

    def test_step2_zbar(self):
        # conj：u=x、v=-y ⇒ u_x=1、v_y=-1 ⇒ r1=2；u_y=0、v_x=0 ⇒ r2=0
        r1, r2 = tool.cr_residual(lambda z: z.conjugate(), 0.5 + 0.3j)
        self.assertNear(r1, 2, 'z̄ 的 r1')
        self.assertNear(r2, 0, 'z̄ 的 r2')

    def test_step2_mod_sq(self):
        # |z|^2：u=x^2+y^2、v=0 ⇒ r1=2x、r2=2y，在 1+1j 处是 (2, 2)
        r1, r2 = tool.cr_residual(lambda z: abs(z) ** 2, 1 + 1j)
        self.assertNear(r1, 2, '|z|^2 的 r1')
        self.assertNear(r2, 2, '|z|^2 的 r2')


class Step3_一点上成不成立(Base):
    """cr_holds：两条残差都在容差内才算成立。"""

    def test_step3_true(self):
        for z in (0j, 1 + 1j, -2 + 0.5j, 3 - 4j):
            self.assertTrue(tool.cr_holds(lambda w: w ** 2, z),
                            'z^2 在 {} 处应满足 CR'.format(z))

    def test_step3_false(self):
        for z in (0j, 1 + 1j, -0.5 + 2j):
            self.assertFalse(tool.cr_holds(lambda w: w.conjugate(), z),
                             'z̄ 在 {} 处不该满足 CR'.format(z))

    def test_step3_mod_sq_origin_only(self):
        self.assertTrue(tool.cr_holds(lambda w: abs(w) ** 2, 0j),
                        '|z|^2 在原点满足 CR')
        self.assertFalse(tool.cr_holds(lambda w: abs(w) ** 2, 1 + 1j),
                         '|z|^2 在 1+1j 不满足 CR')


class Step4_点集(Base):
    """cr_points：CR 成立的点集落在哪里，决定结论怎么说。"""

    GRID = [0j, 1 + 0j, 0 + 1j, 2 + 2j]

    def test_step4_mod_sq(self):
        # 只有原点那个点满足
        got = tool.cr_points(lambda z: abs(z) ** 2, self.GRID)
        self.assertEqual(got, [0j], '|z|^2 的 CR 点集应只有原点')

    def test_step4_all_or_none(self):
        self.assertEqual(len(tool.cr_points(lambda z: z ** 2, self.GRID)),
                         len(self.GRID), 'z^2 在这批点上应处处满足')
        self.assertEqual(tool.cr_points(lambda z: z.conjugate(), self.GRID), [],
                         'z̄ 一个点都不该满足')

    def test_step4_keep_order(self):
        # 只在实轴上满足 CR 的写法：u=x^2、v=2xy+y^2
        f = lambda z: z.real ** 2 + 1j * (2 * z.real * z.imag + z.imag ** 2)
        pts = [1 + 0j, 0 + 1j, 3 + 0j, 2 + 2j]
        got = tool.cr_points(f, pts)
        self.assertEqual(got, [1 + 0j, 3 + 0j],
                         '实轴上的两个点，且要按传入顺序返回')


class Step5_判定卡结论(Base):
    """verdict：点集是整片、几个点、还是一个都没有。"""

    def test_step5_all(self):
        self.assertEqual(tool.verdict(lambda z: z ** 2, [0j, 1 + 1j, 2 + 0j]), 'all')

    def test_step5_some(self):
        self.assertEqual(tool.verdict(lambda z: abs(z) ** 2, [0j, 1 + 1j, 2 + 0j]),
                         'some')

    def test_step5_none(self):
        self.assertEqual(tool.verdict(lambda z: z.conjugate(), [0j, 1 + 1j]), 'none')
        self.assertEqual(tool.verdict(lambda z: z ** 2, []), 'none',
                         '空列表按 none 处理')


class Step6_拉普拉斯(Base):
    """Δu = u_xx + u_yy。二阶差分是 (u(z+h) - 2u(z) + u(z-h)) / h^2。"""

    def test_step6_harmonic_ones(self):
        self.assertNear(tool.laplacian(lambda z: z.real ** 2 - z.imag ** 2, 1 + 2j),
                        0, 'x^2-y^2 的 Δu')
        self.assertNear(tool.laplacian(lambda z: 2 * z.real * z.imag + 3 * z.imag,
                                       3 + 2j), 0, '2xy+3y 的 Δu')

    def test_step6_not_harmonic(self):
        self.assertNear(tool.laplacian(lambda z: 3 * z.real ** 2 + z.imag ** 2, 1 + 1j),
                        8, '3x^2+y^2 的 Δu 应为 8')
        self.assertNear(tool.laplacian(lambda z: z.real ** 2 * z.imag, 3 + 2j),
                        4, 'x^2 y 的 Δu 应为 2y = 4')


class Step7_调和判定(Base):
    """is_harmonic：每个点的 |Δu| 都不超过容差才算。"""

    def test_step7_harmonic(self):
        pts = [1 + 1j, -2 + 0.5j, 3 - 1j]
        self.assertTrue(tool.is_harmonic(lambda z: z.real ** 2 - z.imag ** 2, pts),
                        'x^2-y^2 是调和函数')

    def test_step7_not_harmonic(self):
        pts = [1 + 1j, 2 - 1j]
        self.assertFalse(tool.is_harmonic(lambda z: 3 * z.real ** 2 + z.imag ** 2, pts),
                         '3x^2+y^2 不是调和函数')


class Step8_极坐标(Base):
    """s1 = u_r - v_θ/r，s2 = v_r + u_θ/r。少一个 1/r 通不过。"""

    def test_step8_analytic(self):
        for f, r, t in ((lambda z: z ** 2, 2.0, 0.4),
                        (lambda z: 1 / z, 1.5, 0.7)):
            s1, s2 = tool.polar_cr_residual(f, r, t)
            self.assertNear(s1, 0, '解析函数在 r={} θ={} 的 s1'.format(r, t))
            self.assertNear(s2, 0, '解析函数在 r={} θ={} 的 s2'.format(r, t))

    def test_step8_mod_sq(self):
        # |z|^2：u=r^2、v=0 ⇒ s1=2r、s2=0
        s1, s2 = tool.polar_cr_residual(lambda z: abs(z) ** 2, 2.0, 0.4)
        self.assertNear(s1, 4, '|z|^2 的 s1 = u_r')
        self.assertNear(s2, 0, '|z|^2 的 s2')

    def test_step8_zbar(self):
        # conj：u=r cosθ、v=-r sinθ ⇒ s1=2cosθ、s2=-2sinθ
        s1, s2 = tool.polar_cr_residual(lambda z: z.conjugate(), 2.0, 0.4)
        self.assertNear(s1, 2 * cmath.cos(0.4), 'z̄ 的 s1')
        self.assertNear(s2, -2 * cmath.sin(0.4), 'z̄ 的 s2')


class Step9_整表自检(Base):
    """把课件那张"处处不解析函数"表跑一遍：工具对得上纸面结论，才算真做完。"""

    def test_step9_table(self):
        grid = [0j, 1 + 0j, 1j, 1 + 1j, -2 - 2j, 3 - 1j]
        cases = [
            (lambda z: z ** 2, 'all', 'z^2'),
            (lambda z: z.conjugate(), 'none', 'z̄'),
            (lambda z: abs(z) ** 2, 'some', '|z|^2'),
            (lambda z: z.real, 'none', 'Re z'),
            (lambda z: 1j * z.imag, 'none', 'i·Im z'),
        ]
        for f, want, name in cases:
            self.assertEqual(tool.verdict(f, grid), want,
                             '{} 在这批网格点上的结论'.format(name))


if __name__ == '__main__':
    unittest.main(verbosity=2)
