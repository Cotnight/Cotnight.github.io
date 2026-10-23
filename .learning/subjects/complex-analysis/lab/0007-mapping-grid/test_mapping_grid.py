"""保角映射的网格实验（实验三）的自动判分。

跑法（在 lab/0007-mapping-grid/ 里）：

    python test_mapping_grid.py             # 全部
    python test_mapping_grid.py -k step5    # 只验第 5 步（小十字的夹角）
    python test_mapping_grid.py -k selfcheck

还没动手时这里会一片 ERROR（NotImplementedError），那是设计：先红后绿。
只用标准库（`cmath` / `csv` / `math` / `unittest`），不装 numpy、不装 matplotlib 都能跑。
"""

import cmath
import csv
import math
import os
import tempfile
import unittest

import mapping_grid as mg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

TOL = 1e-4      # 数值比对的容差（导数、坐标）
ANG = 0.5       # 角度的容差，单位是度

# 结论表的十个测点：(表里的名字, 函数, 打点位置, 位置怎么写, 局部放大的臂长 δ)
CASES = [
    ("z^2", mg.f_sq, 1 + 1j, "1+1i", 1e-4),
    ("z^2", mg.f_sq, 0j, "0", 1e-4),
    ("z^2", mg.f_sq, 0j, "0", 1e-2),
    ("z^2", mg.f_sq, 0.01 + 0j, "0.01", 1e-2),
    ("z^2", mg.f_sq, 0.01 + 0j, "0.01", 1e-4),
    ("e^z", mg.f_exp, 0j, "0", 1e-4),
    ("e^z", mg.f_exp, 1 + 1j, "1+1i", 1e-4),
    ("1/z", mg.f_inv, 1j, "i", 1e-4),
    ("1/z", mg.f_inv, 0.1 + 0.1j, "0.1+0.1i", 1e-4),
    ("1/z", mg.f_inv, 0.1 + 0.1j, "0.1+0.1i", 1e-2),
]


class Base(unittest.TestCase):
    """共同的比对工具：数值走容差，角度走「度」的容差。"""

    def assertNear(self, actual, expected, msg='', tol=TOL):
        self.assertLessEqual(abs(actual - expected), tol,
                             '{}：期望 {}，实际 {}'.format(msg, expected, actual))

    def assertAngle(self, got, want, msg=''):
        self.assertIsNotNone(got, msg + '：量不出夹角（有一条臂的像是零向量）')
        self.assertLessEqual(abs(got - want), ANG,
                             '{}：期望 {}°，实际 {}°'.format(msg, want, got))


# ---------------- 第 1 步 · 线段铺点 ----------------

class Step1_线段铺点(Base):
    """segment_points：网格的骨架，参数按 k/(n-1)，两端正好落在起点与终点上。"""

    def test_step1_1_端点与个数(self):
        pts = mg.segment_points(-1 + 0j, 1 + 0j, 5)
        self.assertEqual(len(pts), 5, 'n = 5 就该给 5 个点（含两端）')
        self.assertNear(pts[0], -1 + 0j, '第一个点是起点 a')
        self.assertNear(pts[-1], 1 + 0j, '最后一个是终点 b')
        self.assertNear(pts[2], 0j, '5 个点里中间那个应该在中点')

    def test_step1_2_复平面上的斜线段(self):
        got = mg.segment_points(0j, 1 + 1j, 3)
        self.assertEqual(len(got), 3)
        self.assertNear(got[1], 0.5 + 0.5j, '中间点在 a 到 b 的一半处')
        self.assertNear(got[2], 1 + 1j, '终点不能被 (n-1) 截掉')

    def test_step1_3_少于两点要报错(self):
        for n in (0, 1, -3):
            with self.assertRaises(ValueError):
                mg.segment_points(0j, 1 + 0j, n)


# ---------------- 第 2 步 · 参数网格 ----------------

class Step2_参数网格(Base):
    """grid_lines：竖线 x 固定、自下而上；横线 y 固定、自左向右。"""

    def test_step2_1_两个族的形状(self):
        v, h = mg.grid_lines(-1.0, 1.0, -1.0, 1.0, 5, 4)
        self.assertEqual(len(v), 5, '竖线族 5 条')
        self.assertEqual(len(h), 5, '横线族也是 5 条')
        self.assertEqual(len(v[0]), 4, '每条线 4 个点')

    def test_step2_2_竖线是x等于常数_自下而上(self):
        v, _ = mg.grid_lines(-1.0, 2.0, -0.5, 1.5, 3, 5)
        self.assertNear(v[0][0], complex(-1.0, -0.5), '第一条竖线从 (re_min, im_min) 出发')
        self.assertNear(v[0][-1], complex(-1.0, 1.5), '竖线从 im_min 走到 im_max')
        self.assertNear(v[-1][0], complex(2.0, -0.5), '最后一条竖线在 re_max')
        for w in v[1]:
            self.assertNear(w.real, 0.5, '同一条竖线上实部不变', tol=1e-12)

    def test_step2_3_横线是y等于常数_自左向右(self):
        _, h = mg.grid_lines(-1.0, 2.0, -0.5, 1.5, 3, 5)
        self.assertNear(h[0][0], complex(-1.0, -0.5), '第一条横线从 (re_min, im_min) 出发')
        self.assertNear(h[0][-1], complex(2.0, -0.5), '横线从 re_min 走到 re_max')
        self.assertNear(h[-1][0], complex(-1.0, 1.5), '最后一条横线在 im_max')
        for w in h[1]:
            self.assertNear(w.imag, 0.5, '同一条横线上虚部不变', tol=1e-12)

    def test_step2_4_参数太少要报错(self):
        for n_lines, n_pts in ((1, 5), (5, 1), (1, 1)):
            with self.assertRaises(ValueError):
                mg.grid_lines(-1.0, 1.0, -1.0, 1.0, n_lines, n_pts)


# ---------------- 第 3 步 · 网格变形 ----------------

class Step3_网格变形(Base):
    """map_grid：形状不变、逐点等于 f(z)、踩到极点照实抛。"""

    def test_step3_1_形状不变(self):
        got_v, got_h = mg.map_grid(mg.f_sq, mg.grid_lines(-1.0, 1.0, -1.0, 1.0, 5, 4))
        self.assertEqual((len(got_v), len(got_h)), (5, 5), '线数不增不减')
        self.assertEqual((len(got_v[0]), len(got_h[0])), (4, 4), '每条线的点数也不变')

    def test_step3_2_逐点等于函数值(self):
        grid = mg.grid_lines(-1.0, 1.0, -1.0, 1.0, 3, 3)
        v, h = mg.map_grid(mg.f_sq, grid)
        for line_in, line_out in list(zip(grid[0], v)) + list(zip(grid[1], h)):
            for z, w in zip(line_in, line_out):
                self.assertNear(w, z * z, '映射就是逐点代入 f，别的什么都不做')

    def test_step3_3_指数的竖线映成圆(self):
        v, _ = mg.map_grid(mg.f_exp, mg.grid_lines(*mg.EXP_WINDOW))
        for w in v[0]:
            self.assertNear(abs(w), math.exp(-1.0),
                            'e^z 把 x = -1 的竖线映成半径 e^-1 的圆', tol=1e-9)

    def test_step3_4_踩到极点就抛(self):
        with self.assertRaises(ZeroDivisionError):
            mg.map_grid(mg.f_inv, ([[0j, 1 + 0j]], [[0j, 1j]]))


# ---------------- 第 4 步 · 夹角 ----------------

class Step4_夹角(Base):
    """angle_between：单位是度，零向量返回 None。"""

    def test_step4_1_直角(self):
        self.assertNear(mg.angle_between(1 + 0j, 1j), 90.0, '实轴与虚轴成 90°', tol=1e-9)

    def test_step4_2_反向(self):
        self.assertNear(mg.angle_between(1 + 0j, -2 + 0j), 180.0, '反向的两个向量成 180°', tol=1e-9)

    def test_step4_3_四十五度(self):
        self.assertNear(mg.angle_between(1 + 0j, 1 + 1j), 45.0, '45° 不能被夹到别的值上', tol=1e-9)

    def test_step4_4_零向量给None(self):
        self.assertIsNone(mg.angle_between(0j, 1 + 1j))
        self.assertIsNone(mg.angle_between(1 + 0j, 0j))


# ---------------- 第 5 步 · 小十字的夹角 ----------------

class Step5_小十字(Base):
    """cross_angle：把交点放大到 δ 尺度，看那两条臂的像还成不成直角。"""

    def test_step5_1_z方在非临界点(self):
        self.assertAngle(mg.cross_angle(mg.f_sq, 1 + 1j), 90.0, 'z^2 在 1+i 处直角还在')

    def test_step5_2_z方在原点加倍(self):
        for delta in (1e-2, 1e-6):
            self.assertNear(mg.cross_angle(mg.f_sq, 0j, delta), 180.0,
                            'z^2 在原点把 90° 变成 180°，δ={} 也一样'.format(delta), tol=1e-6)

    def test_step5_3_缩小δ才回到直角(self):
        coarse = mg.cross_angle(mg.f_sq, 0.01 + 0j, 1e-2)
        fine = mg.cross_angle(mg.f_sq, 0.01 + 0j, 1e-4)
        self.assertGreater(coarse, 100.0, 'δ=1e-2 比到临界点的距离还大，量出来在 116° 上下')
        self.assertAngle(fine, 90.0, '同一点把 δ 缩到 1e-4 就回到 90°')

    def test_step5_4_极点旁边仍是直角(self):
        self.assertAngle(mg.cross_angle(mg.f_inv, 0.1 + 0.1j), 90.0,
                         '1/z 的导数不为零，极点旁边量出来仍是 90°')


# ---------------- 第 6 步 · 角度偏差与判据 ----------------

class Step6_角度偏差(Base):
    """angle_defect：把「还在不在」变成一个可比的数。"""

    def test_step6_1_保角点接近零(self):
        self.assertLess(mg.angle_defect(mg.f_sq, 1 + 1j), 0.5, 'z^2 在 1+i 的偏差应当很小')
        self.assertLess(mg.angle_defect(mg.f_exp, 1 + 1j), 0.5, 'e^z 处处保角，偏差应当很小')

    def test_step6_2_原点足足九十度(self):
        self.assertNear(mg.angle_defect(mg.f_sq, 0j), 90.0,
                        '量出来 180°，离 90° 差 90°', tol=1e-6)

    def test_step6_3_极点旁边不到半度(self):
        self.assertLess(mg.angle_defect(mg.f_inv, 0.1 + 0.1j), 0.5,
                        '极点旁边偏差只有 0.06° 上下')

    def test_step6_4_判据与偏差一致(self):
        self.assertFalse(mg.is_conformal(mg.f_sq, 0j), '偏差 90° 远超容差，判不保角')
        self.assertTrue(mg.is_conformal(mg.f_exp, 0j))
        self.assertTrue(mg.is_conformal(mg.f_inv, 1j))


# ---------------- 第 7 步 · 数值导数 ----------------

class Step7_数值导数(Base):
    """derivative_at：模是伸缩率，辐角是旋转角。"""

    def test_step7_1_z方(self):
        self.assertNear(mg.derivative_at(mg.f_sq, 2 + 1j), 4 + 2j, "z^2 的导数是 2z")

    def test_step7_2_指数(self):
        self.assertNear(mg.derivative_at(mg.f_exp, 0j), 1 + 0j, "e^z 在 0 处导数是 1")

    def test_step7_3_倒数(self):
        self.assertNear(mg.derivative_at(mg.f_inv, 1j), 1 + 0j, "1/z 在 i 处导数是 1")

    def test_step7_4_伸缩率与旋转角(self):
        dp = mg.derivative_at(mg.f_inv, 0.1 + 0.1j)
        self.assertNear(abs(dp), 50.0, "极点旁边的伸缩率 |f'| = 1/|z|^2 = 50", tol=1e-6)
        self.assertNear(math.degrees(cmath.phase(dp)), 90.0, '同一个点的旋转角是 90°', tol=1e-6)


# ---------------- 第 8 步 · 临界点 ----------------

class Step8_临界点(Base):
    """critical_points：|f'(z)| ≈ 0 的点，保角在这类点上失效。"""

    def test_step8_1_z方只有原点(self):
        pts = [z for line in mg.grid_lines(*mg.SQ_WINDOW)[0] for z in line]
        got = mg.critical_points(mg.f_sq, pts)
        self.assertEqual(len(got), 1, 'z^2 在这张网格上只有一个临界点')
        self.assertNear(got[0], 0j, '那个点就是原点', tol=1e-12)

    def test_step8_2_指数没有临界点(self):
        pts = [z for line in mg.grid_lines(*mg.EXP_WINDOW)[0] for z in line]
        self.assertEqual(mg.critical_points(mg.f_exp, pts), [], 'e^z 的导数处处非零')

    def test_step8_3_倒数没有临界点(self):
        pts = [z for line in mg.grid_lines(*mg.INV_WINDOW)[0] for z in line]
        self.assertEqual(mg.critical_points(mg.f_inv, pts), [],
                         '1/z 的导数 -1/z^2 在本窗口内没有零点')


# ---------------- 第 9 步 · 两张表存盘 ----------------

class Step9_两张表(Base):
    """save_curves_csv / save_angles_csv：写盘三件套与格式精度。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="mapping_")

    def _read(self, path):
        with open(path, encoding="utf-8", newline="") as handle:
            return list(csv.reader(handle))

    def test_step9_1_网格表的行列与行数(self):
        path = os.path.join(self.tmp, "curves.csv")
        n = mg.save_curves_csv(path, [("V", [[1 + 0j, 2 + 0j]]), ("H", [[0 + 1j]])])
        self.assertEqual(n, 3, '返回的是数据行数：2 + 1')
        got = self._read(path)
        self.assertEqual(got[0], list(mg.CURVES_HEADER), '第一行是表头')
        self.assertEqual(got[1], ["V", "0", "0", "1", "0"], '复数要拆成实部与虚部两列')

    def test_step9_2_网格表小值不丢(self):
        path = os.path.join(self.tmp, "curves2.csv")
        mg.save_curves_csv(path, [("V", [[1e-9 + 3j]])])
        got = self._read(path)
        self.assertAlmostEqual(float(got[1][3]) / 1e-9, 1.0, places=3,
                               msg='1e-9 这样的实部不能写成四位小数，会被抹成 0')
        self.assertAlmostEqual(float(got[1][4]), 3.0)

    def test_step9_3_角度表的格式(self):
        path = os.path.join(self.tmp, "angles.csv")
        rows = [("z^2", "0", 1e-4, 180.0, 90.0, 0.0, "临界点"),
                ("e^z", "0", 1e-4, 90.0, 2.8e-05, 1.0, "保角")]
        self.assertEqual(mg.save_angles_csv(path, rows), 2, '返回数据行数')
        got = self._read(path)
        self.assertEqual(got[0], list(mg.ANGLES_HEADER))
        self.assertEqual(got[1][2], "1e-04", 'δ 写成科学计数法，一看就知道放大到哪个尺度')
        self.assertEqual(got[1][3], "180.0000", '角度写四位小数，90 与 180 要一眼分得开')
        self.assertEqual(got[1][4], "90", '偏差 90 度就写 90')
        self.assertEqual(got[1][5], "0", '伸缩率为 0 就写 0')
        self.assertLess(float(got[2][4]), 1e-4, '2.8e-05 这样的偏差要用科学计数法，不能抹成 0')

    def test_step9_4_没有多余空行(self):
        path = os.path.join(self.tmp, "curves3.csv")
        mg.save_curves_csv(path, [("V", [[1 + 2j]])])
        with open(path, "rb") as handle:
            raw = handle.read()
        self.assertNotIn(b"\r\r\n", raw, '少了 newline=""，Windows 会把每行写成两行')
        self.assertNotIn("\n\n", raw.decode("utf-8"), '文件里不该有空行')


# ---------------- 整块自检（不用填）----------------

class SelfCheck_整块自检(Base):
    """三张网格 + 一张结论表，并把五份数据写进 out/。"""

    FILES = [
        ("curves-z2.csv", mg.f_sq, mg.SQ_WINDOW),
        ("curves-exp.csv", mg.f_exp, mg.EXP_WINDOW),
        ("curves-inv.csv", mg.f_inv, mg.INV_WINDOW),
        ("zoom-z2-origin.csv", mg.f_sq, mg.ZOOM_WINDOW),
    ]

    def _mapped(self, f, window):
        return mg.map_grid(f, mg.grid_lines(*window))

    def _angle_rows(self):
        rows = []
        for name, f, z0, text, delta in CASES:
            if abs(mg.derivative_at(f, z0)) <= mg.DEFAULT_TOL_DERIV:
                verdict = '临界点：角度加倍'
            elif mg.is_conformal(f, z0, delta):
                verdict = '保角'
            else:
                verdict = '偏差待核对：缩小 δ'
            rows.append((name, text, delta, mg.cross_angle(f, z0, delta),
                         mg.angle_defect(f, z0, delta), abs(mg.derivative_at(f, z0)),
                         verdict))
        return rows

    def test_selfcheck_1_三张网格的形状(self):
        for name, f, window in mg.MAPPINGS:
            v, h = self._mapped(f, window)
            self.assertEqual(len(v), mg.LINE_COUNT, name + ' 的竖线族条数')
            self.assertEqual(len(h), mg.LINE_COUNT, name + ' 的横线族条数')
            self.assertEqual(len(v[0]), mg.POINT_COUNT, name + ' 每条线的点数')

    def test_selfcheck_2_原点角度加倍(self):
        self.assertNear(mg.cross_angle(mg.f_sq, 0j), 180.0, 'z^2 在原点：90° 变 180°', tol=1e-6)
        self.assertFalse(mg.is_conformal(mg.f_sq, 0j), '这个点判不保角')
        self.assertTrue(mg.is_conformal(mg.f_sq, 1 + 1j), '离开原点就保角')

    def test_selfcheck_3_极点旁边尺度炸了直角还在(self):
        dp = mg.derivative_at(mg.f_inv, 0.1 + 0.1j)
        self.assertNear(abs(dp), 50.0, "极点旁边的伸缩率 |f'| = 50", tol=1e-6)
        self.assertTrue(mg.is_conformal(mg.f_inv, 0.1 + 0.1j), '缩放 50 倍，直角还在')
        pts = [z for line in mg.grid_lines(*mg.INV_WINDOW)[0] for z in line]
        self.assertEqual(mg.critical_points(mg.f_inv, pts), [], '1/z 没有临界点')

    def test_selfcheck_4_五份数据写进out(self):
        os.makedirs(OUT, exist_ok=True)
        for name, f, window in self.FILES:
            v, h = self._mapped(f, window)
            got = mg.save_curves_csv(os.path.join(OUT, name), [("V", v), ("H", h)])
            self.assertEqual(got, 2 * mg.LINE_COUNT * mg.POINT_COUNT, name + ' 的数据行数')
        rows = self._angle_rows()
        self.assertEqual(len(rows), 10, '结论表 10 个测点')
        self.assertEqual(mg.save_angles_csv(os.path.join(OUT, "angles.csv"), rows), 10)
        for name in [item[0] for item in self.FILES] + ["angles.csv"]:
            path = os.path.join(OUT, name)
            self.assertTrue(os.path.exists(path), name + ' 没写出来')
            self.assertGreater(os.path.getsize(path), 0, name + ' 是空文件')


if __name__ == "__main__":
    unittest.main(verbosity=2)
