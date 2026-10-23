#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""residue_lab.py 的测试：跑 python test_residue_lab.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_residue_lab.py -k step9

-k 后面写测试名里的一段：step1 … step12、selfcheck。
留白没填时这些测试会报 NotImplementedError——那不是环境坏了，是那一步还没写。

两档容差是分开的（常数在 residue_lab.py 里）：
  · TOL_EXACT：走围道的那几条。圆周上 dz 取解析式 i·Δθ·(z−a)，梯形法到机器精度，
    误差在 1e-14 附近，收成 1e-9 也安全；
  · TOL_VALUE：走「公式 + 数值求导」的那几条。二阶中心差分留着 1e-8 量级的截断误差
    （实测 (1+z+z²)/z³ 在 0 处差 6.1e-9），只能放到 1e-6。
"""

import cmath
import math
import unittest

import residue_lab as lab

PI = math.pi
TAU = 2j * PI               # 2πi
# 第 12 步那两道题的奇点与留数，几个测试共用
R1_NUM, R1_DEN = [1], [4, 8, 5, 1]          # 1/((z+1)(z+2)^2)，分母 z^3+5z^2+8z+4


def r1(z):
    """f(z) = 1/((z+1)(z+2)^2)：分母展开成多项式 z^3+5z^2+8z+4。"""
    return lab.poly_eval(R1_NUM, z) / lab.poly_eval(R1_DEN, z)


def r2(z):
    """f(z) = e^z/((z−πi)(z−2πi)^2)：2022 年卷那道 |z|=8 的题。"""
    return cmath.exp(z) / ((z - 1j * PI) * (z - 2j * PI) ** 2)


def r3(z):
    """f(z) = cos z/(z^2(z^2−π^2))：2024 年卷「求有限复平面内全部奇点与留数」那题。"""
    return cmath.cos(z) / (z ** 2 * (z ** 2 - PI ** 2))


class Base(unittest.TestCase):
    """共同的比对工具：所有数值比对都走这里，容差分两档。"""

    def assertNear(self, actual, expected, msg='', tol=lab.TOL_VALUE):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}（差 {}）'
                             .format(msg, expected, actual, abs(actual - expected)))

    def assertZero(self, value, msg='', tol=lab.TOL_EXACT):
        self.assertLessEqual(abs(value), tol,
                             '{}：应当≈0，实际 {}（模 {}）'.format(msg, value, abs(value)))


class Step1_围道采样(Base):
    """circle_points：逆时针、n 个点、首点不重复写两遍。"""

    def test_step1_first_point(self):
        pts = lab.circle_points(0j, 1, 8)
        self.assertNear(pts[0], 1 + 0j, '起点应是 center + radius', tol=1e-12)

    def test_step1_count(self):
        self.assertEqual(len(lab.circle_points(0j, 1, 8)), 8,
                         'n=8 就该返回 8 个点（首点别重复写进末尾）')

    def test_step1_radius(self):
        center, radius = 2 + 1j, 0.5
        for z in lab.circle_points(center, radius, 16):
            self.assertLessEqual(abs(abs(z - center) - radius), 1e-12,
                                 '点 {} 到圆心的距离不是 {}'.format(z, radius))

    def test_step1_direction(self):
        # n=4：第二个点必须是 i——写成顺时针这一步会跑到 -i
        pts = lab.circle_points(0j, 1, 4)
        self.assertNear(pts[1], 1j, 'n=4 时第二个点是 i（逆时针）', tol=1e-12)

    def test_step1_default_n(self):
        self.assertEqual(len(lab.circle_points(0j, 1)), lab.DEFAULT_N,
                         '不传 n 时用 DEFAULT_N')


class Step2_数值围道积分(Base):
    """closed_integral：dz 换成 i·Δθ·(z−center)，一整圈加起来。"""

    def test_step2_one_over_z(self):
        self.assertNear(lab.closed_integral(lambda z: 1 / z, 0j, 2), TAU,
                        '1/z 沿 |z|=2 正向')

    def test_step2_analytic_zero(self):
        for f, name in ((cmath.exp, 'e^z'), (lambda z: z ** 2, 'z^2'),
                        (cmath.sin, 'sin z')):
            self.assertZero(lab.closed_integral(f, 0j, 1), name + ' 沿 |z|=1')

    def test_step2_pole_outside(self):
        # 奇点 z=2 在 |z|=1 外面，圈内解析 ⇒ 0
        self.assertZero(lab.closed_integral(lambda z: 1 / (z - 2), 0j, 1),
                        '1/(z−2) 沿 |z|=1：奇点在圈外')

    def test_step2_constant_is_zero(self):
        # 漏掉 (z−center) 会算出 2πi；漏掉 1j 会算出 2π —— 两种都不为 0
        self.assertZero(lab.closed_integral(lambda z: 1 + 0j, 0j, 1),
                        '常数 1 沿 |z|=1 应当为 0')

    def test_step2_uses_center(self):
        # dz 里的 (z−center) 写成 z 时这一条立刻错
        self.assertNear(lab.closed_integral(lambda z: 1 / (z - 3), 3 + 0j, 1), TAU,
                        '1/(z−3) 沿 |z−3|=1 正向')


class Step3_圈内判定(Base):
    """inside：奇点在不在围道里，边界一律不算。"""

    def test_step3_inside(self):
        self.assertTrue(lab.inside(1 + 0j, 0j, 2))
        self.assertTrue(lab.inside(2 + 2j, 1 + 1j, 2), '按到圆心的距离判，不是按 |z0|')

    def test_step3_outside(self):
        self.assertFalse(lab.inside(5 + 0j, 0j, 2))
        # 圆心不在原点：|z0|=0.5 < 1.5，但到圆心的距离是 1.5 → 压在围道上
        self.assertFalse(lab.inside(-0.5 + 0j, 1 + 0j, 1.5),
                         '|z0| 小于半径不代表在圈内——要用 z0 − center')

    def test_step3_on_contour(self):
        # 奇点正好压在围道上：strict 小于才算圈内
        self.assertFalse(lab.inside(2 + 0j, 0j, 2), '围道上的点不算圈内')


class Step4_多项式求值(Base):
    """poly_eval：系数按升幂给，霍纳法往下卷。"""

    def test_step4_ascending(self):
        # z^3+5z^2+8z+4 在 z=2 处：8+20+16+4 = 48
        self.assertNear(lab.poly_eval([4, 8, 5, 1], 2), 48 + 0j,
                        '升幂系数 [4,8,5,1] 在 2 处的值', tol=1e-12)
        self.assertNear(lab.poly_eval([4, 8, 5, 1], -1), 0 + 0j,
                        'z=−1 是它的根', tol=1e-12)

    def test_step4_empty(self):
        self.assertNear(lab.poly_eval([], 5), 0j, '空列表当零多项式', tol=1e-12)

    def test_step4_complex(self):
        # 1 + i z 在 z=i 处 = 1 + i·i = 0
        self.assertNear(lab.poly_eval([1, 1j], 1j), 0j,
                        '1 + i·z 在 z=i 处为 0', tol=1e-12)


class Step5_多项式求导(Base):
    """deriv_poly：z^k 求导得 k·z^(k−1)。"""

    def test_step5_quadratic(self):
        self.assertEqual(lab.deriv_poly([1, 2, 3]), [2, 6],
                         '1+2z+3z^2 的导数是 2+6z')

    def test_step5_constant(self):
        self.assertNear(lab.poly_eval(lab.deriv_poly([5]), 3), 0j,
                        '常数的导数是零多项式（返回 [] 或 [0] 都行）', tol=1e-12)

    def test_step5_quartic(self):
        # z + z^3 的导数是 1 + 3z^2
        self.assertEqual(lab.deriv_poly([0, 1, 0, 1]), [1, 0, 3])


class Step6_综合除法(Base):
    """strip_factor：把 (z−z0)^m 从分母里除干净，剩下的商在 z0 处不为零。"""

    def test_step6_once(self):
        q = lab.strip_factor([4, 8, 5, 1], -2, 1)
        self.assertEqual(q, [2, 3, 1],
                         '(z^3+5z^2+8z+4)/(z+2) = z^2+3z+2，升幂写作 [2,3,1]')

    def test_step6_twice(self):
        self.assertEqual(lab.strip_factor([4, 8, 5, 1], -2, 2), [1, 1],
                         '再除一次 (z+2) 得 z+1')

    def test_step6_other_root(self):
        self.assertEqual(lab.strip_factor([4, 8, 5, 1], -1, 1), [4, 4, 1],
                         '除以 (z+1) 得 z^2+4z+4')

    def test_step6_identity(self):
        # 商乘回 (z−z0)^m 必须还原分母——几个点各验一次
        q = lab.strip_factor([4, 8, 5, 1], -2, 2)
        for z in (0j, 1 + 1j, -3 + 0.5j):
            self.assertLessEqual(abs(lab.poly_eval(R1_DEN, z) - lab.poly_eval(q, z) * (z + 2) ** 2),
                                 1e-9, '在 z={} 处还原失败'.format(z))


class Step7_数值求导(Base):
    """deriv_n：0／1／2 阶，步长与求导阶数要配对。"""

    def test_step7_order0(self):
        self.assertEqual(lab.deriv_n(cmath.exp, 1 + 0j, 0), cmath.exp(1 + 0j),
                         'order=0 直接返回 g(z0)，一点不差')

    def test_step7_order1(self):
        self.assertNear(lab.deriv_n(cmath.exp, 1 + 0j, 1), cmath.exp(1),
                        'e^z 在 1 处的一阶导', tol=1e-8)

    def test_step7_order2(self):
        self.assertNear(lab.deriv_n(cmath.cos, 0j, 2), -1 + 0j,
                        'cos z 在 0 处的二阶导是 −1', tol=1e-7)

    def test_step7_bad_order(self):
        with self.assertRaises(ValueError):
            lab.deriv_n(cmath.exp, 0j, 3)


class Step8_一阶极点公式(Base):
    """residue_simple：Res = P(z0)/Q'(z0)。"""

    def test_step8_r1(self):
        # 1/((z+1)(z+2)^2) 在 −1：P(−1)/Q'(−1) = 1/1
        self.assertNear(lab.residue_simple(R1_NUM, R1_DEN, -1), 1 + 0j,
                        'Res[1/((z+1)(z+2)^2), −1]')

    def test_step8_other_point(self):
        # 1/(z^2(z−3)) 在 3 处：Q = z^3−3z^2，Q'(3) = 9
        self.assertNear(lab.residue_simple([1], [0, 0, -3, 1], 3), 1 / 9,
                        'Res[1/(z^2(z−3)), 3]')

    def test_step8_matches_integral(self):
        # 公式与小圆上的数值围道积分对照
        self.assertNear(lab.residue_simple(R1_NUM, R1_DEN, -1),
                        lab.residue_by_integral(r1, -1, 0.5),
                        '一阶公式 vs 小圆积分')

    def test_step8_double_root_raises(self):
        # 分母是重根时 Q'(z0)=0：一阶公式算不出数，这正是要回去重新定阶的信号
        with self.assertRaises(ZeroDivisionError):
            lab.residue_simple(R1_NUM, R1_DEN, -2)


class Step9_m阶极点公式(Base):
    """residue_pole_m：(1/(m−1)!)·g^(m−1)(z0)，g 是除掉 (z−z0)^m 之后那个函数。"""

    def test_step9_second_order(self):
        self.assertNear(lab.residue_pole_m(R1_NUM, R1_DEN, -2, 2), -1 + 0j,
                        'Res[1/((z+1)(z+2)^2), −2]')

    def test_step9_third_order_factorial(self):
        # (1+z+z^2)/z^3：m=3，乘 z^3 后求二阶导得 2，除以 2! 得 1。
        # 漏掉 1/(m−1)! 会算出 2 —— 这一条就是那个丢分点的代码版。
        self.assertNear(lab.residue_pole_m([1, 1, 1], [0, 0, 0, 1], 0, 3), 1 + 0j,
                        'Res[(1+z+z^2)/z^3, 0] 应为 1，写成 2 就是漏了 1/2!')

    def test_step9_residue_not_zero(self):
        # 1/(z^2(z−3)) 在 0 处：m=2，g = 1/(z−3)，g'(0) = −1/9
        self.assertNear(lab.residue_pole_m([1], [0, 0, -3, 1], 0, 2), -1 / 9,
                        'Res[1/(z^2(z−3)), 0]')

    def test_step9_m1_matches_simple(self):
        # m=1 时退化成 limit 式 (z−z0)f(z) 在 z0 的取值，两条公式必须一致
        self.assertNear(lab.residue_pole_m(R1_NUM, R1_DEN, -1, 1),
                        lab.residue_simple(R1_NUM, R1_DEN, -1),
                        'm=1 与一阶公式同一条式子')

    def test_step9_matches_integral(self):
        self.assertNear(lab.residue_pole_m(R1_NUM, R1_DEN, -2, 2),
                        lab.residue_by_integral(r1, -2, 0.5),
                        '二阶公式 vs 小圆积分')


class Step10_小圆兜底(Base):
    """residue_by_integral：(1/2πi)∮ 小圆，本性奇点只能走这条。"""

    def test_step10_exp_inv_z(self):
        self.assertNear(lab.residue_by_integral(lambda z: cmath.exp(1 / z), 0j, 0.5),
                        1 + 0j, 'Res[e^(1/z), 0]：展开读数 c₋₁ = 1')

    def test_step10_z2_exp_inv_z(self):
        self.assertNear(lab.residue_by_integral(lambda z: z ** 2 * cmath.exp(1 / z), 0j, 0.5),
                        1 / 6, 'Res[z^2 e^(1/z), 0]：c₋₁ 来自 1/3!')

    def test_step10_sin_over_z3(self):
        # 填空 3 分那道：sin z/z^3 = 1/z^2 − 1/6 + …，c₋₁ = 0
        self.assertZero(lab.residue_by_integral(lambda z: cmath.sin(z) / z ** 3, 0j, 0.5),
                        'Res[sin z/z^3, 0]', tol=lab.TOL_VALUE)

    def test_step10_tan(self):
        # 一阶极点也能用兜底复核：tan z 在 π/2 的留数是 −1
        self.assertNear(lab.residue_by_integral(cmath.tan, PI / 2, 1.0), -1 + 0j,
                        'Res[tan z, π/2]')

    def test_step10_removable(self):
        # 可去奇点：sin z/z 的留数必为 0
        self.assertZero(lab.residue_by_integral(lambda z: cmath.sin(z) / z, 0j, 0.5),
                        'Res[sin z/z, 0]（可去奇点）', tol=lab.TOL_VALUE)


class Step11_留数定理(Base):
    """contour_by_residues：2πi 乘圈内留数之和。"""

    def test_step11_two_poles(self):
        poles = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - PI * 1j) / PI ** 2)]
        self.assertNear(lab.contour_by_residues(poles, 0j, 8), 2 + 4j / PI,
                        '∮_{|z|=8} e^z dz/((z−πi)(z−2πi)^2) = 2 + 4i/π')

    def test_step11_outside_excluded(self):
        # 同两个奇点，围道换成 |z|=1：都在圈外 ⇒ 0
        poles = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - PI * 1j) / PI ** 2)]
        self.assertZero(lab.contour_by_residues(poles, 0j, 1),
                        '奇点都在圈外，积分为 0')

    def test_step11_cancellation(self):
        # 两个非零留数正好抵消：答案是 0，但不是「圈内没奇点」
        self.assertZero(lab.contour_by_residues([(-1, 1), (-2, -1)], 0j, 3),
                        '∮_{|z|=3} dz/((z+1)(z+2)^2)：1 + (−1) = 0')

    def test_step11_has_factor_tau(self):
        # 只求和忘乘 2πi：结果会和正确值差一个 2πi
        poles = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - PI * 1j) / PI ** 2)]
        got = lab.contour_by_residues(poles, 0j, 8)
        self.assertGreater(abs(got - (poles[0][1] + poles[1][1])), 1.0,
                           '结果里必须带上 2πi 这个因子')

    def test_step11_matches_numeric(self):
        self.assertNear(lab.closed_integral(r2, 0j, 8), 2 + 4j / PI,
                        '数值围道积分 vs 理论值', tol=lab.TOL_EXACT)


class Step12_漏掉奇点的对照(Base):
    """contour_missing_poles 是故意写错的那一版：圈内两个奇点只算一个。"""

    def setUp(self):
        self.poles = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - PI * 1j) / PI ** 2)]

    def test_step12_wrong_value(self):
        self.assertNear(lab.contour_missing_poles(self.poles, 0j, 8), 2j / PI,
                        '只算第一个奇点得到 2i/π')

    def test_step12_differs_from_right(self):
        right = lab.contour_by_residues(self.poles, 0j, 8)
        wrong = lab.contour_missing_poles(self.poles, 0j, 8)
        self.assertGreater(abs(right - wrong), 1.0,
                           '漏掉一个奇点，答案差得远：{} vs {}'.format(right, wrong))

    def test_step12_numeric_sides_with_right(self):
        # 数值围道积分是裁判：它站在「两个都算」那边，而不是「只算一个」
        numeric = lab.closed_integral(r2, 0j, 8)
        right = lab.contour_by_residues(self.poles, 0j, 8)
        wrong = lab.contour_missing_poles(self.poles, 0j, 8)
        self.assertLess(abs(numeric - right), abs(numeric - wrong) / 10,
                        '围道积分应更接近正确值')

    def test_step12_single_pole_same(self):
        # 圈内只有一个奇点时两版必然相同——差异只可能来自「漏点」
        one = [(-1, 1), (-5, -1)]
        self.assertNear(lab.contour_missing_poles(one, 0j, 3),
                        lab.contour_by_residues(one, 0j, 3),
                        '只有一个奇点在圈内时，错版与正版相等')


class Selfcheck_整表自检(Base):
    """不用填。课件里那几道真题整表跑一遍：数值围道积分与 2πiΣ 留数逐行对照。"""

    def test_selfcheck_residue_table(self):
        # 每个奇点：公式（或小圆积分）算出的留数 vs 小圆围道积分
        rows = [
            ('cos z/(z^2(z^2−π^2)) 在 0（二阶，留数为 0）', r3, 0j, 1.0, 0j),
            ('cos z/(z^2(z^2−π^2)) 在 π（一阶）', r3, PI, 1.0, -1 / (2 * PI ** 3)),
            ('cos z/(z^2(z^2−π^2)) 在 −π（一阶）', r3, -PI, 1.0, 1 / (2 * PI ** 3)),
            ('e^z/(z−1)^3 在 1（三阶）', lambda z: cmath.exp(z) / (z - 1) ** 3,
             1 + 0j, 1.0, cmath.exp(1) / 2),
            ('(z^2−π^2)/(z sin z) 在 2π（一阶）',
             lambda z: (z ** 2 - PI ** 2) / (z * cmath.sin(z)), 2 * PI, 1.0, 3 * PI / 2),
        ]
        for name, f, z0, radius, want in rows:
            self.assertNear(lab.residue_by_integral(f, z0, radius), want,
                            '留数表：' + name)

    def test_selfcheck_contour_table(self):
        # 三道 10 分题：数值围道积分 vs 2πiΣ留数 vs 理论值
        r2a = lab.residue_by_integral(r2, 1j * PI, 1.0)
        r2b = lab.residue_by_integral(r2, 2j * PI, 1.0)
        f5 = lambda z: cmath.exp(1j * z) / (z ** 2 - 3 * PI * z + 2 * PI ** 2)
        rows = [
            ('1/((z+1)(z+2)^2) 沿 |z|=3', r1, 0j, 3,
             [(-1, 1 + 0j), (-2, -1 + 0j)], 0j),
            ('e^z/((z−πi)(z−2πi)^2) 沿 |z|=8', r2, 0j, 8,
             [(1j * PI, r2a), (2j * PI, r2b)], 2 + 4j / PI),
            ('e^(iz)/(z^2−3πz+2π^2) 沿 |z−3|=4', f5, 3 + 0j, 4,
             [(PI, lab.residue_by_integral(f5, PI, 1.0)),
              (2 * PI, lab.residue_by_integral(f5, 2 * PI, 1.0))], 4j),
        ]
        for name, f, center, radius, poles, want in rows:
            self.assertNear(lab.closed_integral(f, center, radius), want,
                            '数值围道积分：' + name, tol=lab.TOL_EXACT)
            self.assertNear(lab.contour_by_residues(poles, center, radius), want,
                            '2πiΣ留数：' + name, tol=lab.TOL_EXACT)

    def test_selfcheck_zero_sum(self):
        # 全平面留数（这里只列有限奇点）之和为零：R1 是 1+(−1)，
        # R3 是 0 + (−1/(2π^3)) + 1/(2π^3)
        total1 = (lab.residue_pole_m(R1_NUM, R1_DEN, -1, 1)
                  + lab.residue_pole_m(R1_NUM, R1_DEN, -2, 2))
        self.assertZero(total1, 'R1 两个留数相加（算完核对那一行）', tol=lab.TOL_VALUE)
        total = (lab.residue_by_integral(r3, 0j, 1.0)
                 + lab.residue_by_integral(r3, PI, 1.0)
                 + lab.residue_by_integral(r3, -PI, 1.0))
        self.assertZero(total, 'R3 三个留数相加', tol=lab.TOL_VALUE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
