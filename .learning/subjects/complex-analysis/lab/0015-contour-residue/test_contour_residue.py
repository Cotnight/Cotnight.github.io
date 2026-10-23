#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contour_residue.py 的测试：跑 python test_contour_residue.py，全绿才算这一课做完。

只验某一步（填一步验一步）：

    python test_contour_residue.py -k step1_    # 第 1 步要带那个下划线
    python test_contour_residue.py -k step7
    python test_contour_residue.py -k selfcheck # 只跑自检，写出 out/

`-k` 后面是**子串**匹配，所以 `-k step1` 会连 step10 一起选中；第 1 步一律写 `step1_`。
留白没填时这些测试会报 NotImplementedError——那不是环境坏了，是那一步还没写。

两档容差（常数在 contour_residue.py 里）：

  · 走围道的那几条用 1e-9：圆周上 dz 取解析式 i·Δθ·(z−a)，梯形法到机器精度；
  · 「有奇点在圈里、积分结果与 2πiΣ 相等」那几条也用 1e-9，别放到 1e-6 去——
    放到 1e-6 就分不清「算对了」和「漏了一个奇点但恰好只差一点点」。
"""

import cmath
import csv
import math
import os
import shutil
import tempfile
import unittest

import contour_residue as lab

PI = math.pi
TAU = 2j * PI                       # 2πi
TOL = 1e-9                          # 围道这条路的容差
S2_VALUE = 2 + 4j / PI              # ∮_{|z|=8} e^z dz/((z−πi)(z−2πi)²) 的理论值
S3_VALUE = 2j / PI                  # 同一函数换成 |z|=4：只剩 πi 那一项


def r_cubic(z):
    """f(z) = 1/((z+1)(z+2)^2)。"""
    return lab.f_cubic(z)


def r_double(z):
    """f(z) = e^z/((z−πi)(z−2πi)^2)。"""
    return lab.f_double(z)


class Base(unittest.TestCase):
    """共同的比对工具：数值比对都走这里。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}（差 {}）'
                             .format(msg, expected, actual, abs(actual - expected)))

    def assertZero(self, value, msg='', tol=TOL):
        self.assertLessEqual(abs(value), tol,
                             '{}：应当≈0，实际 {}（模 {}）'.format(msg, value, abs(value)))


class Step1_方根面板(Base):
    """nth_roots：实验一那块面板，五个五次方根围成正五边形。"""

    def test_step1_count(self):
        self.assertEqual(len(lab.nth_roots(1 + 1j, 5)), 5, 'n=5 就该返回 5 个根')

    def test_step1_modulus(self):
        for z in lab.nth_roots(1 + 1j, 5):
            self.assertLessEqual(abs(abs(z) - abs(1 + 1j) ** 0.2), 1e-12,
                                 '所有根的模都该是 |z0|^(1/5)')

    def test_step1_first_angle(self):
        # 辐角 45° 除以 5：第一个根的角度必须是 9°（按弧度算，别中途换度数）
        z0 = lab.nth_roots(1 + 1j, 5)[0]
        self.assertLessEqual(abs(cmath.phase(z0) - math.radians(9)), 1e-12,
                             '第一个根的辐角是 Arg(z0)/5')

    def test_step1_spacing(self):
        roots = lab.nth_roots(1 + 1j, 5)
        step = cmath.phase(roots[1]) - cmath.phase(roots[0])
        self.assertLessEqual(abs(step - 2 * PI / 5), 1e-12,
                             '相邻两根的角差是 2π/n = 72°')

    def test_step1_sum_is_zero(self):
        self.assertZero(sum(lab.nth_roots(1 + 1j, 5)), '五个根的和是 0')


class Step2_网格面板(Base):
    """segment_points：实验三那块面板，竖线上一串等距的点。"""

    def test_step2_endpoints(self):
        pts = lab.segment_points(0j, 2 + 2j, 5)
        self.assertNear(pts[0], 0j, '第一个点是 a')
        self.assertNear(pts[-1], 2 + 2j, '最后一个点是 b（参数要写 k/(n−1)）')

    def test_step2_count(self):
        self.assertEqual(len(lab.segment_points(0j, 1 + 0j, 6)), 6)

    def test_step2_even(self):
        pts = lab.segment_points(0j, 1 + 0j, 3)
        self.assertNear(pts[1], 0.5 + 0j, '中间那个点在正中间')

    def test_step2_bad_n(self):
        with self.assertRaises(ValueError):
            lab.segment_points(0j, 1 + 0j, 1)


class Step3_围道采样(Base):
    """circle_contour：一条真正画得出来的圆，也是积分的采样点。"""

    def test_step3_first_point(self):
        self.assertNear(lab.circle_contour(0j, 1, 8)[0], 1 + 0j, '起点是 center + radius')

    def test_step3_count(self):
        self.assertEqual(len(lab.circle_contour(0j, 1, 8)), 8,
                         'n=8 就该返回 8 个点（首点别重复写进末尾）')

    def test_step3_radius(self):
        center, radius = 2 + 1j, 0.5
        for z in lab.circle_contour(center, radius, 16):
            self.assertLessEqual(abs(abs(z - center) - radius), 1e-12,
                                 '点 {} 到圆心的距离不是 {}'.format(z, radius))

    def test_step3_direction(self):
        pts = lab.circle_contour(0j, 1, 4)
        self.assertNear(pts[1], 1j, 'n=4 时第二个点是 i（逆时针）')


class Step4_数值围道积分(Base):
    """contour_integral：dz 换成 i·Δθ·(z−center)，一整圈加起来。"""

    def test_step4_one_over_z(self):
        self.assertNear(lab.contour_integral(lambda z: 1 / z, 0j, 2), TAU,
                        '1/z 沿 |z|=2 正向')

    def test_step4_analytic_zero(self):
        for f, name in ((cmath.exp, 'e^z'), (lambda z: z ** 2, 'z^2')):
            self.assertZero(lab.contour_integral(f, 0j, 1), name + ' 沿 |z|=1')

    def test_step4_pole_outside(self):
        self.assertZero(lab.contour_integral(lambda z: 1 / (z - 2), 0j, 1),
                        '1/(z−2) 沿 |z|=1：奇点在圈外')

    def test_step4_constant_is_zero(self):
        # 漏掉 (z−center) 会算出 2πi；漏掉 1j 会算出 2π —— 两种都不为 0
        self.assertZero(lab.contour_integral(lambda z: 1 + 0j, 0j, 1),
                        '常数 1 沿 |z|=1 应当为 0')

    def test_step4_uses_center(self):
        self.assertNear(lab.contour_integral(lambda z: 1 / (z - 3), 3 + 0j, 1), TAU,
                        '1/(z−3) 沿 |z−3|=1 正向')


class Step5_圈内判定(Base):
    """inside：奇点在不在围道里，边界一律不算。"""

    def test_step5_inside(self):
        self.assertTrue(lab.inside(1 + 0j, 0j, 2))
        self.assertTrue(lab.inside(2 + 2j, 1 + 1j, 2), '按到圆心的距离判，不是按 |z0|')

    def test_step5_outside(self):
        self.assertFalse(lab.inside(5 + 0j, 0j, 2))

    def test_step5_center_not_origin(self):
        # |z0|=0.5 < 1.5，但到圆心 1 的距离正好 1.5 → 压在围道上，不算圈内
        self.assertFalse(lab.inside(-0.5 + 0j, 1 + 0j, 1.5),
                         '|z0| 小于半径不代表在圈内——要用 z0 − center')

    def test_step5_on_contour(self):
        self.assertFalse(lab.inside(2 + 0j, 0j, 2), '围道上的点不算圈内')


class Step6_留数定理(Base):
    """residue_theorem：2πi 乘圈内留数之和。"""

    def test_step6_two_poles(self):
        self.assertNear(lab.residue_theorem(lab.POLES_DOUBLE, 0j, 8), S2_VALUE,
                        '∮_{|z|=8} e^z dz/((z−πi)(z−2πi)²) = 2 + 4i/π')

    def test_step6_one_pole(self):
        self.assertNear(lab.residue_theorem(lab.POLES_DOUBLE, 0j, 4), S3_VALUE,
                        '换成 |z|=4：只有 πi 在圈内')

    def test_step6_outside_excluded(self):
        self.assertZero(lab.residue_theorem(lab.POLES_DOUBLE, 0j, 2),
                        '换成 |z|=2：奇点都在圈外，答案 0')

    def test_step6_cancellation(self):
        # 两个留数 1 与 −1 正好抵消：答案是 0，但不是「圈内没奇点」
        self.assertZero(lab.residue_theorem(lab.POLES_CUBIC, 0j, 3),
                        '∮_{|z|=3} dz/((z+1)(z+2)²)：1 + (−1) = 0')

    def test_step6_has_factor_tau(self):
        got = lab.residue_theorem(lab.POLES_DOUBLE, 0j, 8)
        bare = sum(res for _, res in lab.POLES_DOUBLE)
        self.assertGreater(abs(got - bare), 1.0, '结果里必须带上 2πi 这个因子')


class Step7_账本一行(Base):
    """ledger_row：数值积分与 2πiΣ 并排，差多少、一致不一致。"""

    def test_step7_keys(self):
        row = lab.ledger_row(*lab.SPECIMENS[1])
        self.assertEqual(sorted(row), sorted(['case', 'enclosed', 'numeric',
                                              'theorem', 'gap', 'verdict']),
                         '账本一行的键是固定的六个')

    def test_step7_two_poles_agree(self):
        row = lab.ledger_row(*lab.SPECIMENS[1])
        self.assertEqual(row['enclosed'], 2, 'S2 圈内有两个奇点')
        self.assertNear(row['numeric'], S2_VALUE, 'S2 的数值积分')
        self.assertLessEqual(row['gap'], 1e-6, 'S2 数值与定理值应当一致')
        self.assertEqual(row['verdict'], '一致')

    def test_step7_contour_shrinks(self):
        # 换一条把 2πi 漏在外面的围道：两边一起变成 2i/π，仍然一致
        row = lab.ledger_row(*lab.SPECIMENS[2])
        self.assertEqual(row['enclosed'], 1, 'S3 圈内只剩 πi 一个')
        self.assertNear(row['numeric'], S3_VALUE, 'S3 的数值积分')
        self.assertEqual(row['verdict'], '一致')

    def test_step7_all_outside(self):
        row = lab.ledger_row(*lab.SPECIMENS[3])
        self.assertEqual(row['enclosed'], 0, 'S4 圈内一个奇点都没有')
        self.assertZero(row['numeric'], 'S4 的数值积分', tol=1e-9)
        self.assertEqual(row['verdict'], '一致')

    def test_step7_missing_pole_disagrees(self):
        # S5 故意只列一个奇点：账本当场判「不一致」，数值站到正确值那边
        row = lab.ledger_row(*lab.SPECIMENS[4])
        self.assertEqual(row['enclosed'], 1)
        self.assertEqual(row['verdict'], '不一致', '少列一个奇点，两列不该相等')
        self.assertGreater(row['gap'], 1.0, '差得不是一点点，是一整个留数项')
        self.assertNear(row['numeric'], S2_VALUE, '数值积分仍然是对的')


class Step8_围道图存盘(Base):
    """save_contour_csv：围道点 + 极点标记，图的数据版。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='contour-')
        self.path = os.path.join(self.tmp, 'panel4-contour.csv')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def rows(self):
        with open(self.path, encoding='utf-8', newline='') as fh:
            return list(csv.reader(fh))

    def test_step8_row_count(self):
        n = lab.save_contour_csv(self.path, 0j, 8.0, lab.POLES_DOUBLE)
        self.assertEqual(n, lab.ART_N + 2, 'ART_N 个围道点 + 2 个奇点')

    def test_step8_header(self):
        lab.save_contour_csv(self.path, 0j, 8.0, lab.POLES_DOUBLE)
        self.assertEqual(self.rows()[0], ['kind', 'index', 're', 'im', 'mark'],
                         '表头是 kind,index,re,im,mark')

    def test_step8_marks(self):
        lab.save_contour_csv(self.path, 0j, 4.0, lab.POLES_DOUBLE)
        marks = [r[4] for r in self.rows()[1:] if r[0] == 'pole']
        self.assertEqual(marks, ['圈内', '圈外'],
                         '半径 4 时 πi 在圈内、2πi 在圈外')

    def test_step8_no_blank_lines(self):
        lab.save_contour_csv(self.path, 0j, 8.0, lab.POLES_DOUBLE)
        with open(self.path, encoding='utf-8', newline='') as fh:
            text = fh.read()
        self.assertNotIn('\r\r', text, 'open 少了 newline="" 时 Windows 会多出空行')
        self.assertEqual(len(self.rows()), lab.ART_N + 2 + 1, '表头 + 数据行')


class Step9_画廊合并(Base):
    """write_gallery：四块面板并进同一份 out/，总表四行。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix='gallery-')

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_step9_four_rows(self):
        rows = lab.write_gallery(self.tmp)
        self.assertEqual(len(rows), 4, '四块面板四行')
        self.assertEqual([r[0] for r in rows],
                         ['panel1-roots', 'panel2-arg', 'panel3-grid', 'panel4-contour'],
                         '面板名与顺序')

    def test_step9_row_counts(self):
        rows = lab.write_gallery(self.tmp)
        self.assertEqual([r[2] for r in rows],
                         [5, 25, 24, lab.ART_N + 2], '四块面板的数据行数')

    def test_step9_files_exist(self):
        lab.write_gallery(self.tmp)
        for name in ('gallery.csv', 'panel1-roots.csv', 'panel2-arg.csv',
                     'panel3-grid.csv', 'panel4-contour.csv'):
            self.assertTrue(os.path.isfile(os.path.join(self.tmp, name)),
                            '缺少 {}'.format(name))

    def test_step9_gallery_index(self):
        lab.write_gallery(self.tmp)
        with open(os.path.join(self.tmp, 'gallery.csv'),
                  encoding='utf-8', newline='') as fh:
            table = list(csv.reader(fh))
        self.assertEqual(table[0], ['panel', 'file', 'rows', 'note'])
        self.assertEqual(len(table), 5, '总表是表头 + 四行')

    def test_step9_arg_column(self):
        lab.write_gallery(self.tmp)
        with open(os.path.join(self.tmp, 'panel2-arg.csv'),
                  encoding='utf-8', newline='') as fh:
            table = list(csv.reader(fh))
        angles = [float(r[2]) for r in table[1:]]
        self.assertTrue(all(0.0 <= a < 360.0 for a in angles),
                        '辐角着色的度数要压在 [0,360)')


class Step10_字符画(Base):
    """ascii_canvas：不装 matplotlib 也能看见围道与极点。"""

    def setUp(self):
        self.lines = lab.ascii_canvas(0j, 4.0, lab.POLES_DOUBLE)

    def test_step10_shape(self):
        self.assertEqual(len(self.lines), 21, '默认 21 行')
        self.assertEqual({len(line) for line in self.lines}, {41}, '每行 41 个字符')

    def test_step10_contour_drawn(self):
        self.assertIn('.', ''.join(self.lines), '围道的点画成 .')

    def test_step10_marks_inside_and_outside(self):
        art = ''.join(self.lines)
        self.assertIn('*', art, 'πi 在圈内，要画成 *')
        self.assertIn('o', art, '2πi 在圈外，要画成 o')

    def test_step10_all_inside(self):
        art = ''.join(lab.ascii_canvas(0j, 8.0, lab.POLES_DOUBLE))
        self.assertIn('*', art)
        self.assertNotIn('o', art, '半径 8 时两个奇点都在圈内，不该出现 o')


class Selfcheck_整块自检(Base):
    """不用填。把四块面板与账本真跑一遍，写出 out/，并把字符画打出来。"""

    def test_selfcheck_write_out(self):
        rows = lab.write_gallery('out')
        self.assertEqual([r[2] for r in rows], [5, 25, 24, lab.ART_N + 2])
        for name, lines in (('gallery.csv', 5), ('panel1-roots.csv', 6),
                            ('panel2-arg.csv', 26), ('panel3-grid.csv', 25),
                            ('panel4-contour.csv', lab.ART_N + 3)):
            path = os.path.join('out', name)
            self.assertTrue(os.path.isfile(path), '自检没写出 {}'.format(name))
            with open(path, encoding='utf-8', newline='') as fh:
                self.assertEqual(len(list(csv.reader(fh))), lines,
                                 '{} 的行数不对'.format(name))

    def test_selfcheck_ledger(self):
        rows = lab.ledger_rows()
        ledger = []
        for row in rows:
            ledger.append([row['case'], row['enclosed'],
                           row['numeric'].real, row['numeric'].imag,
                           row['theorem'].real, row['theorem'].imag,
                           row['gap'], row['verdict']])
        lab.write_csv('out', 'ledger.csv',
                      ('case', 'enclosed', 'numeric_re', 'numeric_im',
                       'theorem_re', 'theorem_im', 'gap', 'verdict'), ledger)
        verdicts = [row['verdict'] for row in rows]
        self.assertEqual(verdicts, ['一致', '一致', '一致', '一致', '不一致'],
                         '只有少列奇点的 S5 该被账本抓出来')
        self.assertEqual([row['enclosed'] for row in rows], [2, 2, 1, 0, 1],
                         '圈内奇点个数：S3 漏掉 2πi、S4 一个不剩')

    def test_selfcheck_art(self):
        for name, center, radius, poles in (
                ('S2 · |z|=8', 0j, 8.0, lab.POLES_DOUBLE),
                ('S3 · |z|=4', 0j, 4.0, lab.POLES_DOUBLE)):
            print('\n' + name)
            for line in lab.ascii_canvas(center, radius, poles):
                print(line)


if __name__ == '__main__':
    unittest.main(verbosity=2)
