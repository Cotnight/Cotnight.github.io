"""解析函数画廊 · 第二块（实验二）的自动判分。

跑法（在 lab/0006-analytic-gallery/ 里）：

    python test_analytic_gallery.py             # 全部
    python test_analytic_gallery.py -k step4    # 只验第 4 步
    python test_analytic_gallery.py -k numpy    # 只验向量化那一步（要 numpy）
    python test_analytic_gallery.py -k selfcheck

还没动手时这里会一片 ERROR（NotImplementedError），那是设计：先红后绿。
只用标准库；装了 numpy 才会多跑 numpy 那两条，没装就跳过，不影响结论。
"""

import cmath
import csv
import math
import os
import tempfile
import unittest

import analytic_gallery as ag

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

TOL = 1e-4

try:
    import numpy  # noqa: F401

    HAS_NUMPY = True
except Exception:
    HAS_NUMPY = False


class Base(unittest.TestCase):
    """共同的比对工具：数值差分有误差，一律按容差比。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}'.format(msg, expected, actual))


# ---------------- 第 1 步 · 窗口铺点 ----------------

class Step1_窗口铺点(Base):
    """scan_window：行在外列在内，第 0 行是 im_min、第 0 列是 re_min。"""

    def test_step1_1_顺序与形状(self):
        got = ag.scan_window(-1.0, 1.0, -1.0, 1.0, 3, 2)
        want = [-1 - 1j, 0 - 1j, 1 - 1j, -1 + 1j, 0 + 1j, 1 + 1j]
        self.assertEqual(got, want,
                         '展平顺序要「一行行往下」，且每行从左到右')

    def test_step1_2_两个角(self):
        got = ag.scan_window(-1.5, 0.5, -0.25, 2.0, 5, 3)
        self.assertEqual(len(got), 15, '宽 5 高 3 就该有 15 个点')
        self.assertEqual(got[0], complex(-1.5, -0.25),
                         '第一个点是左下角 (re_min, im_min)')
        self.assertEqual(got[-1], complex(0.5, 2.0),
                         '最后一个点是右上角 (re_max, im_max)')

    def test_step1_3_尺寸太小要报错(self):
        for w, h in ((1, 3), (3, 1), (1, 1)):
            with self.assertRaises(ValueError):
                ag.scan_window(-1.0, 1.0, -1.0, 1.0, w, h)


# ---------------- 第 2 步 · 逐点检验 ----------------

class Step2_逐点检验(Base):
    """cr_scan 返回每个点的标签，不是筛出来的点。"""

    def test_step2_1_解析函数整片成立(self):
        pts = [-2 - 2j, 0j, 1 + 1j, 3 - 1j]
        self.assertEqual(ag.cr_scan(ag.f_sq, pts), [True, True, True, True],
                         'z^2 处处解析，四个点都该成立')

    def test_step2_2_共轭处处不成立(self):
        pts = [-2 - 2j, 0j, 1 + 1j, 3 - 1j]
        self.assertEqual(ag.cr_scan(ag.f_conj, pts), [False, False, False, False],
                         'z̄ 的 r1 恒等于 2，四个点都不该成立')

    def test_step2_3_模方只在原点(self):
        got = ag.cr_scan(ag.f_mod_sq, [0j, 1 + 1j, 2 + 0j])
        self.assertEqual(got, [True, False, False],
                         '|z|^2 只在原点满足 CR，另外两个点不满足')

    def test_step2_4_保持顺序(self):
        # u = x^2、v = 2xy + y^2：CR 只在实轴（y = 0）上成立
        f = lambda z: z.real ** 2 + 1j * (2 * z.real * z.imag + z.imag ** 2)
        got = ag.cr_scan(f, [1 + 0j, 0 + 1j, 3 + 0j])
        self.assertEqual(got, [True, False, True],
                         '标签要一一对应传进去的点，别排序、别去重')


# ---------------- 第 3 步 · 比例 ----------------

class Step3_比例(Base):
    """analytic_fraction：点集大小的量化版。"""

    def test_step3_1_全成立(self):
        self.assertAlmostEqual(ag.analytic_fraction(ag.f_sq, [0j, 1 + 1j, 2 - 3j]), 1.0)

    def test_step3_2_全不成立(self):
        self.assertAlmostEqual(ag.analytic_fraction(ag.f_conj, [0j, 1 + 1j]), 0.0)

    def test_step3_3_空点集不除零(self):
        self.assertAlmostEqual(ag.analytic_fraction(ag.f_sq, []), 0.0,
                               '空点集按 0.0 处理，别让 ZeroDivisionError 冒出来')

    def test_step3_4_五点中一个(self):
        pts = [0j, 1 + 1j, 2 + 0j, 0.5 + 0.5j, 3 - 1j]
        self.assertAlmostEqual(ag.analytic_fraction(ag.f_mod_sq, pts), 0.2,
                               '|z|^2 在这五个点里只有原点一个成立')


# ---------------- 第 4 步 · 残差图 ----------------

class Step4_残差图(Base):
    """residual_map：给上色用的数据，行序与步长都跟第 1 步一致。"""

    WINDOW = (-1.0, 1.0, -1.0, 1.0)

    def test_step4_1_形状(self):
        grid = ag.residual_map(ag.f_exp, *self.WINDOW, 6, 4)
        self.assertEqual(len(grid), 4, '高度 4 就是 4 行')
        self.assertEqual(len(grid[0]), 6, '宽度 6 就是每行 6 列')

    def test_step4_2_解析函数整片接近0(self):
        for row in ag.residual_map(ag.f_exp, *self.WINDOW, 6, 4):
            for v in row:
                self.assertLess(v, 1e-6, 'e^z 解析，残差图该整片接近 0')

    def test_step4_3_共轭整片等于2(self):
        for row in ag.residual_map(ag.f_conj, *self.WINDOW, 6, 4):
            for v in row:
                self.assertAlmostEqual(v, 2.0, places=6,
                                       msg='z̄ 的两条残差是 (2, 0)，图上是满幅的 2')

    def test_step4_4_第0行是最下面那一行(self):
        window = (-1.0, 0.5, -0.25, 2.0)
        grid = ag.residual_map(ag.f_mod_sq, *window, 5, 3)
        r1, r2 = ag.cr_residual(ag.f_mod_sq, complex(-1.0, -0.25))
        r3, r4 = ag.cr_residual(ag.f_mod_sq, complex(0.5, 2.0))
        self.assertAlmostEqual(grid[0][0], max(abs(r1), abs(r2)),
                               msg='左下角对不上：第 0 行必须是 im_min 那一行')
        self.assertAlmostEqual(grid[-1][-1], max(abs(r3), abs(r4)),
                               msg='右上角对不上：最后一行最后一列是 (re_max, im_max)')
        self.assertNotAlmostEqual(grid[0][0], grid[-1][-1],
                                  msg='两个角的值本来就不同，上下翻了会一样')


# ---------------- 第 5 步 · 两个梯度 ----------------

class Step5_两个梯度(Base):

    def test_step5_1_z方在2加i(self):
        # z^2：u = x²-y²、v = 2xy ⇒ ∇u = (2x, -2y)、∇v = (2y, 2x)
        (ux, uy), (vx, vy) = ag.grad_u_v(ag.f_sq, 2 + 1j)
        for got, want, what in ((ux, 4.0, 'u_x'), (uy, -2.0, 'u_y'),
                                (vx, 2.0, 'v_x'), (vy, 4.0, 'v_y')):
            self.assertNear(got, want, 'z^2 在 2+i 处的 ' + what)

    def test_step5_2_指数在原点(self):
        (ux, uy), (vx, vy) = ag.grad_u_v(ag.f_exp, 0j)
        for got, want, what in ((ux, 1.0, 'u_x'), (uy, 0.0, 'u_y'),
                                (vx, 0.0, 'v_x'), (vy, 1.0, 'v_y')):
            self.assertNear(got, want, 'e^z 在 0 处的 ' + what)

    def test_step5_3_共轭(self):
        # z̄：u = x、v = -y ⇒ ∇u = (1, 0)、∇v = (0, -1)
        (ux, uy), (vx, vy) = ag.grad_u_v(ag.f_conj, 0.5 + 0.3j)
        self.assertNear(ux, 1.0, 'z̄ 的 u_x')
        self.assertNear(uy, 0.0, 'z̄ 的 u_y')
        self.assertNear(vx, 0.0, 'z̄ 的 v_x')
        self.assertNear(vy, -1.0, 'z̄ 的 v_y')


# ---------------- 第 6 步 · 正交性 ----------------

class Step6_正交性(Base):
    """orthogonality：解析函数的两组等值线垂直，余弦该是 0。"""

    def test_step6_1_解析函数正交(self):
        for f, z, name in ((ag.f_sq, 2 + 1j, 'z^2'),
                           (ag.f_exp, 0.3 - 0.7j, 'e^z')):
            got = ag.orthogonality(f, z)
            self.assertIsNotNone(got, name + ' 的两个梯度都不为零，不该返回 None')
            self.assertLessEqual(abs(got), 1e-6, name + ' 的两组等值线应当正交')

    def test_step6_2_共轭也正交但不是解析(self):
        got = ag.orthogonality(ag.f_conj, 0.5 + 0.3j)
        self.assertIsNotNone(got)
        self.assertLessEqual(abs(got), 1e-6,
                             'z̄ 的两组线也互相垂直——所以「正交」判不出解析，得看第 7 步')

    def test_step6_3_虚部恒为零时没有夹角(self):
        self.assertIsNone(ag.orthogonality(ag.f_mod_sq, 1 + 1j),
                          '|z|^2 的 v 恒等于 0，辐角等值线根本不存在，夹角无意义')

    def test_step6_4_不垂直的例子(self):
        # u = x、v = x+y：∇u = (1,0)、∇v = (1,1) ⇒ 余弦 1/√2
        f = lambda z: z.real + 1j * (z.real + z.imag)
        got = ag.orthogonality(f, 1 + 1j)
        self.assertNear(got, 1.0 / math.sqrt(2.0),
                        '这个函数两组线成 45°，余弦应为 1/√2')


# ---------------- 第 7 步 · 方向（行列式）----------------

class Step7_方向(Base):

    def test_step7_1_解析函数等于导数的模方(self):
        # z^2 在 2+i 处 |f'|^2 = |2z|^2 = 4·5 = 20
        self.assertNear(ag.jacobian(ag.f_sq, 2 + 1j), 20.0,
                        'z^2 的行列式应等于 |f\u2032|^2')

    def test_step7_2_指数在原点(self):
        self.assertNear(ag.jacobian(ag.f_exp, 0j), 1.0, 'e^z 在 0 处的 |f\u2032|^2 = 1')

    def test_step7_3_共轭为负(self):
        self.assertNear(ag.jacobian(ag.f_conj, 0.5 + 0.3j), -1.0,
                        'z̄ 也正交，但方向反了——行列式是负的')

    def test_step7_4_模方为零(self):
        self.assertNear(ag.jacobian(ag.f_mod_sq, 2 + 1j), 0.0,
                        '|z|^2 把整个平面压成半条实轴，行列式处处为零')


# ---------------- 第 8 步 · 结论表 ----------------

class Step8_结论表(Base):
    """save_summary_csv：一行一个函数，写盘三件套。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="analytic_")

    def _read(self, path):
        with open(path, encoding="utf-8", newline="") as handle:
            return list(csv.reader(handle))

    def test_step8_1_表头与行数(self):
        path = os.path.join(self.tmp, "scan.csv")
        rows = [("e^z", 4, 4, 1.0, 1e-9), ("z̄", 4, 0, 0.0, 2.0)]
        n = ag.save_summary_csv(path, rows)
        self.assertEqual(n, 2, '返回值是数据行数，不含表头')
        got = self._read(path)
        self.assertEqual(got[0], list(ag.SUMMARY_HEADER), '第一行是表头')
        self.assertEqual(len(got), 3, '表头 1 行 + 数据 2 行')

    def test_step8_2_数值能读回(self):
        path = os.path.join(self.tmp, "scan2.csv")
        ag.save_summary_csv(path, [("e^z", 651, 651, 1.0, 1.2e-9),
                                   ("|z|^2", 651, 1, 1 / 651, 3.0)])
        got = self._read(path)
        self.assertEqual(got[1][0], 'e^z')
        self.assertEqual(int(got[1][1]), 651)
        self.assertEqual(int(got[1][2]), 651)
        self.assertAlmostEqual(float(got[1][3]), 1.0, places=4)
        self.assertLess(float(got[1][4]), 1e-6, '1e-9 这样的残差必须写成科学计数法才不丢')
        self.assertAlmostEqual(float(got[2][3]), 1 / 651, places=4)

    def test_step8_3_没有多余空行(self):
        path = os.path.join(self.tmp, "scan3.csv")
        ag.save_summary_csv(path, [("z̄", 2, 0, 0.0, 2.0)])
        with open(path, "rb") as handle:
            raw = handle.read()
        self.assertNotIn(b"\r\r\n", raw, '少了 newline=""，Windows 会把每行写成两行')
        self.assertNotIn("\n\n", raw.decode("utf-8"), '文件里不该有空行')


# ---------------- 第 9 步 · 残差图存盘 ----------------

class Step9_残差图存盘(Base):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="analytic_")

    def _read(self, path):
        with open(path, encoding="utf-8", newline="") as handle:
            return list(csv.reader(handle))

    def test_step9_1_返回行列数(self):
        path = os.path.join(self.tmp, "res.csv")
        self.assertEqual(ag.save_grid_csv(path, [[1, 2, 3], [4, 5, 6]]), (2, 3))

    def test_step9_2_不写表头(self):
        path = os.path.join(self.tmp, "res2.csv")
        ag.save_grid_csv(path, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(self._read(path)[0], ["1", "2", "3"],
                         '残差图是不写表头的整数/浮点矩阵')

    def test_step9_3_小残差不丢成零(self):
        path = os.path.join(self.tmp, "res3.csv")
        ag.save_grid_csv(path, [[1e-10, 2e-10], [2.0, 0.0]])
        got = self._read(path)
        self.assertAlmostEqual(float(got[0][0]) / 1e-10, 1.0, places=3,
                               msg='1e-10 写成四位小数会变成 0.0000，图就成了一片纯色')
        self.assertAlmostEqual(float(got[1][0]), 2.0)


# ---------------- numpy 那一步（没装就跳过）----------------

@unittest.skipUnless(HAS_NUMPY, "没装 numpy，向量化那一步跳过（不影响前面 9 步的结论）")
class StepNp_向量化残差图(Base):

    def test_numpy_1_与逐点版逐格相同(self):
        window = (-1.0, 1.0, -0.5, 1.0)
        slow = ag.residual_map(ag.f_exp, *window, 6, 4)
        fast = ag.residual_map_np(numpy.exp, *window, 6, 4)
        self.assertEqual(len(fast), 4)
        self.assertEqual(len(fast[0]), 6)
        for r in range(4):
            for c in range(6):
                self.assertLessEqual(abs(slow[r][c] - fast[r][c]), 1e-12,
                                     '({},{}) 两版对不上：先查形状是不是 (高, 宽)'.format(r, c))

    def test_numpy_2_非解析函数也一致(self):
        window = (-1.0, 1.0, -1.0, 1.0)
        slow = ag.residual_map(ag.f_conj, *window, 5, 3)
        fast = ag.residual_map_np(numpy.conj, *window, 5, 3)
        for r in range(3):
            for c in range(5):
                self.assertAlmostEqual(slow[r][c], fast[r][c], places=9)


# ---------------- 整块自检（不用填）----------------

class SelfCheck_整块自检(Base):
    """把画廊六个函数跑成一张结论表，并把两张残差图写进 out/。"""

    STANDARD = (-1.5, 1.5, -1.5, 1.5)
    RIGHT_HALF = (0.25, 1.5, -1.5, 1.5)
    LEFT_HALF = (-1.5, -0.25, -1.5, 1.5)

    def _row(self, name, f, window):
        pts = ag.scan_window(*window, *ag.DEFAULT_SIZE)
        hits = sum(1 for ok in ag.cr_scan(f, pts) if ok)
        resid = ag.residual_map(f, *window, *ag.DEFAULT_SIZE)
        return (name, len(pts), hits, hits / len(pts),
                max(max(v for v in line) for line in resid))

    def _rows(self):
        out = []
        for slug, name, f in ag.GALLERY:
            window = self.RIGHT_HALF if slug == "log" else self.STANDARD
            out.append(self._row(name, f, window))
        return out

    def test_selfcheck_1_解析的三个整片成立(self):
        table = {row[0]: row for row in self._rows()}
        for name in ("e^z", "sin z", "z^2"):
            self.assertAlmostEqual(table[name][3], 1.0, places=9,
                                   msg=name + ' 的 CR 应当处处成立')
            self.assertLess(table[name][4], 1e-6, name + ' 的残差该接近 0')

    def test_selfcheck_2_非解析的两个不成立(self):
        table = {row[0]: row for row in self._rows()}
        self.assertAlmostEqual(table["z̄"][3], 0.0, places=9, msg='z̄ 一个点都不成立')
        self.assertAlmostEqual(table["z̄"][4], 2.0, places=6, msg='z̄ 的残差满幅 2')
        self.assertEqual(table["|z|^2"][2], 1,
                         '|z|^2 在 31×21 的窗口里只有原点一个点成立（原点正好是格点）')

    def test_selfcheck_3_割线是假失败(self):
        right = self._row("Ln z", ag.f_log, self.RIGHT_HALF)
        left = self._row("Ln z", ag.f_log, self.LEFT_HALF)
        self.assertAlmostEqual(right[3], 1.0, places=9,
                               msg='右半平面没有割线，Ln z 该整片成立')
        self.assertLess(left[3], 1.0,
                        '左半平面跨了负实轴：割线上那列点会「假失败」，比例不再是 1')
        self.assertGreater(left[3], 0.9,
                           '只该少一列（负实轴上那 13 个点），少得多说明步长或行序也错了')

    def test_selfcheck_4_三份交付写进out(self):
        os.makedirs(OUT, exist_ok=True)
        scan = os.path.join(OUT, "scan.csv")
        self.assertEqual(ag.save_summary_csv(scan, self._rows()), len(ag.GALLERY))
        for slug, name, f in (("exp", "e^z", ag.f_exp), ("conj", "z̄", ag.f_conj)):
            path = os.path.join(OUT, "residual-{}.csv".format(slug))
            rows, cols = ag.save_grid_csv(
                path, ag.residual_map(f, *self.STANDARD, *ag.DEFAULT_SIZE))
            self.assertEqual((rows, cols), (21, 31), '残差图是 21 行 × 31 列')
        for name in ("scan.csv", "residual-exp.csv", "residual-conj.csv"):
            path = os.path.join(OUT, name)
            self.assertTrue(os.path.exists(path), name + ' 没写出来')
            self.assertGreater(os.path.getsize(path), 0, name + ' 是空文件')


if __name__ == "__main__":
    unittest.main(verbosity=2)
