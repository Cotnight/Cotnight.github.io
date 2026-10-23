"""图像画廊 · 第一块（实验一）的自动判分。

跑法（在 lab/0003-gallery/ 里）：

    python test_gallery.py            # 全跑
    python test_gallery.py -k step3   # 只验第 3 步

还没动手时这里会一片 ERROR（NotImplementedError），那是设计：先红后绿。
只用标准库；装了 numpy 才会多跑第 8 步，没装就跳过，不影响结论。
"""

import cmath
import csv
import math
import os
import tempfile
import unittest

import gallery as ge

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def deg(z):
    """测试自己的角度换算（不依赖第 2 步），用来验第 1、7 步。"""
    return math.degrees(cmath.phase(z)) % 360.0


try:
    import numpy  # noqa: F401

    HAS_NUMPY = True
except Exception:
    HAS_NUMPY = False


# ---------------- 第 1 步 · 方根 ----------------

class Step1_方根与正多边形(unittest.TestCase):

    def test_step1_1_单位根的顺序(self):
        roots = ge.nth_roots(1 + 0j, 4)
        want = [1, 1j, -1, -1j]
        self.assertEqual(len(roots), 4)
        for k in range(4):
            self.assertAlmostEqual(roots[k].real, complex(want[k]).real, places=9,
                                   msg=f"k={k} 的根实部不对")
            self.assertAlmostEqual(roots[k].imag, complex(want[k]).imag, places=9,
                                   msg=f"k={k} 的根虚部不对")

    def test_step1_2_负一的三次方根(self):
        roots = ge.nth_roots(-1 + 0j, 3)
        self.assertEqual(len(roots), 3)
        self.assertAlmostEqual(roots[0].real, 0.5, places=9)
        self.assertAlmostEqual(abs(roots[0].imag), math.sqrt(3) / 2, places=9)
        self.assertAlmostEqual(roots[1].real, -1.0, places=9)
        self.assertAlmostEqual(roots[1].imag, 0.0, places=9)
        self.assertAlmostEqual(abs(deg(roots[0])), 60.0, places=6)
        self.assertAlmostEqual(deg(roots[1]), 180.0, places=6)
        self.assertAlmostEqual(deg(roots[2]), 300.0, places=6)

    def test_step1_3_模相等且相邻夹角相等(self):
        z0, n = 1 + 1j, 3
        roots = ge.nth_roots(z0, n)
        radius = abs(z0) ** (1.0 / n)
        for r in roots:
            self.assertAlmostEqual(abs(r), radius, places=9, msg="n 个根的模必须都等于 |z0|^(1/n)")
        angles = sorted(deg(r) for r in roots)
        gaps = [round(angles[k + 1] - angles[k], 6) for k in range(n - 1)]
        gaps.append(round(angles[0] + 360.0 - angles[-1], 6))
        for g in gaps:
            self.assertAlmostEqual(g, 360.0 / n, places=5,
                                   msg=f"相邻两个根的角度差应为 360/n，实际 {gaps}")
        self.assertAlmostEqual(angles[0], 15.0, places=5,
                               msg="1+i 的辐角是 45°，除 3 得 15°——这里差倍数是用了角度制算")

    def test_step1_4_边长相等即正多边形(self):
        roots = ge.nth_roots(1 + 1j, 3)
        sides = [abs(roots[(k + 1) % 3] - roots[k]) for k in range(3)]
        for s in sides:
            self.assertAlmostEqual(s, sides[0], places=9, msg=f"三条边不等长：{sides}")
        self.assertAlmostEqual(sides[0], 2 * abs(1 + 1j) ** (1 / 3) * math.sin(math.pi / 3),
                               places=9)

    def test_step1_5_全部根的和为零(self):
        total = sum(ge.nth_roots(1 + 1j, 3))
        self.assertAlmostEqual(abs(total), 0.0, places=9,
                               msg="正多边形的重心在原点，n 个根加起来必须是 0")

    def test_step1_6_n等于1与非法n(self):
        self.assertEqual(len(ge.nth_roots(2 + 2j, 1)), 1)
        self.assertAlmostEqual(abs(ge.nth_roots(2 + 2j, 1)[0] - (2 + 2j)), 0.0, places=9)
        with self.assertRaises(ValueError):
            ge.nth_roots(1 + 1j, 0)


# ---------------- 第 2 步 · 辐角着色 ----------------

class Step2_辐角着色(unittest.TestCase):

    def test_step2_1_四个正方向(self):
        self.assertAlmostEqual(ge.arg_degrees(1 + 0j), 0.0, places=9)
        self.assertAlmostEqual(ge.arg_degrees(0 + 1j), 90.0, places=9)
        self.assertAlmostEqual(ge.arg_degrees(-1 + 0j), 180.0, places=9)
        self.assertAlmostEqual(ge.arg_degrees(-1j), 270.0, places=9)

    def test_step2_2_第四象限给正角(self):
        self.assertAlmostEqual(ge.arg_degrees(1 - 1j), 315.0, places=9,
                               msg="着色要的是 [0,360)，-45° 得写成 315°")
        self.assertAlmostEqual(ge.arg_degrees(-1 + 1j), 135.0, places=9)

    def test_step2_3_原点不报错(self):
        self.assertAlmostEqual(ge.arg_degrees(0j), 0.0, places=9)


# ---------------- 第 3 步 · 迭代与逃逸 ----------------

class Step3_逃逸迭代(unittest.TestCase):

    def test_step3_1_步数就是第一次超过2的那次(self):
        # c = 1：z1=1, z2=2, z3=5 > 2，所以是第 3 步
        self.assertEqual(ge.escape_from(0j, 1 + 0j, 100), 3)

    def test_step3_2_判据是严格大于2(self):
        # c = -2：z1=-2（模正好 2，不算逃逸）、z2=2、z3=2……永远不逃逸
        self.assertEqual(ge.escape_from(0j, -2 + 0j, 100), 100,
                         msg="|z| = 2 不算逃逸，判据是严格大于 2")

    def test_step3_3_预算用完返回预算(self):
        self.assertEqual(ge.escape_from(0j, 0 + 0j, 5), 5,
                         msg="没逃逸时要返回 max_iter，不是 None 也不是 0")

    def test_step3_4_起点不是原点时结果会变(self):
        self.assertEqual(ge.escape_from(1 + 1j, 0j, 100), 2,
                         msg="同样 c=0，从 1+i 出发两步就飞出去了")
        self.assertEqual(ge.escape_from(0.5 + 0j, -0.5 + 0.5j, 100), 100)


# ---------------- 第 4 步 · 曼德博集的点 ----------------

class Step4_曼德博集的点(unittest.TestCase):

    def test_step4_1_集内的点(self):
        self.assertEqual(ge.mandelbrot_escape(0j, 100), 100)
        self.assertEqual(ge.mandelbrot_escape(-1 + 0j, 100), 100)
        self.assertEqual(ge.mandelbrot_escape(-0.75 + 0j, 200), 200)
        self.assertEqual(ge.mandelbrot_escape(0.3 + 0.5j, 100), 100)

    def test_step4_2_集外的点(self):
        self.assertEqual(ge.mandelbrot_escape(1 + 0j, 100), 3)
        self.assertEqual(ge.mandelbrot_escape(2 + 0j, 100), 2)
        self.assertEqual(ge.mandelbrot_escape(1 + 1j, 100), 2)

    def test_step4_3_逃出去没有(self):
        self.assertFalse(ge.escaped(0j, 100))
        self.assertFalse(ge.escaped(0.3 + 0.5j, 100))
        self.assertTrue(ge.escaped(1 + 0j, 100))
        self.assertTrue(ge.escaped(2 + 0j, 100))


# ---------------- 第 5 步 · 缩略图网格 ----------------

class Step5_缩略图网格(unittest.TestCase):

    def test_step5_1_形状与整数(self):
        grid = ge.escape_grid(-2.0, 0.5, -1.25, 1.25, 5, 3, 40)
        self.assertEqual(len(grid), 3, msg="高度 3 就是 3 行")
        self.assertEqual(len(grid[0]), 5, msg="宽度 5 就是每行 5 列")
        for line in grid:
            for v in line:
                self.assertIsInstance(v, int, msg="格子必须是整数（逃逸步数），不能是复数或浮点")
                self.assertTrue(1 <= v <= 40)

    def test_step5_2_整张矩阵(self):
        grid = ge.escape_grid(-2.0, 0.5, -0.25, 1.0, 5, 3, 40)
        want = [[1, 6, 13, 40, 5],
                [1, 5, 8, 40, 5],
                [1, 3, 3, 13, 2]]
        self.assertEqual(grid, want,
                         msg="整张矩阵对不上：先查第 0 行是不是最下面那行（im_min），再查列的方向")

    def test_step5_3_第0行是最下面那一行(self):
        re_min, re_max, im_min, im_max = -2.0, 0.5, -0.25, 1.0
        grid = ge.escape_grid(re_min, re_max, im_min, im_max, 5, 3, 40)
        self.assertEqual(grid[0][0], ge.mandelbrot_escape(complex(re_min, im_min), 40),
                         msg="左下角对不上：第 0 行必须是 im_min")
        self.assertEqual(grid[-1][-1], ge.mandelbrot_escape(complex(re_max, im_max), 40),
                         msg="右上角对不上：最后一行的最后一列是 (re_max, im_max)")

    def test_step5_4_每格都等于逐点算的结果(self):
        re_min, re_max, im_min, im_max, w, h, it = -2.0, 0.5, -0.25, 1.0, 5, 3, 40
        grid = ge.escape_grid(re_min, re_max, im_min, im_max, w, h, it)
        for row in range(h):
            for col in range(w):
                re = ge.pixel_to_re(col, w, re_min, re_max)
                im = ge.pixel_to_im(row, h, im_min, im_max)
                self.assertEqual(grid[row][col], ge.mandelbrot_escape(complex(re, im), it),
                                 msg=f"({row},{col}) 与逐点算的不一致")


# ---------------- 第 6 步 · 存盘 ----------------

class Step6_存盘(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gallery_")

    def test_step6_1_方根存成两列(self):
        path = os.path.join(self.tmp, "roots.csv")
        roots = ge.nth_roots(-1 + 0j, 3)
        n = ge.save_points_csv(path, roots)
        self.assertEqual(n, 3, msg="返回值是写入的数据行数，不含表头")
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["re", "im"], msg="第一行是表头 re,im")
        self.assertEqual(len(rows), 4, msg="表头 1 行 + 数据 3 行")
        for k in range(3):
            self.assertEqual(len(rows[k + 1]), 2, msg="每行两列")
            self.assertAlmostEqual(float(rows[k + 1][0]), roots[k].real, places=9)
            self.assertAlmostEqual(float(rows[k + 1][1]), roots[k].imag, places=9)

    def test_step6_2_网格存成整数矩阵(self):
        path = os.path.join(self.tmp, "grid.csv")
        info = ge.save_grid_csv(path, [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(tuple(info), (2, 3), msg="返回值是 (行数, 列数)")
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual([[int(v) for v in line] for line in rows], [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(rows[0], ["1", "2", "3"], msg="不写表头")

    def test_step6_3_没有多余空行(self):
        path = os.path.join(self.tmp, "blank.csv")
        ge.save_points_csv(path, [1 + 1j, -1 + 0j])
        with open(path, "rb") as f:
            raw = f.read()
        self.assertNotIn(b"\r\r\n", raw,
                         msg="open 时少了 newline=\"\"，Windows 会把每行写成两行")
        text = raw.decode("utf-8")
        self.assertNotIn("\n\n", text, msg="文件里不该有空行")
        self.assertNotIn("j", text, msg="只写数字，别把 Python 的复数写法 (1+1j) 写进 CSV")


# ---------------- 第 7 步 · 整块自检（不用填） ----------------

class Step7_整块自检(unittest.TestCase):

    def test_step7_1_第一块数据_方根(self):
        roots = ge.nth_roots(1 + 1j, 5)
        self.assertEqual(len(roots), 5)
        for r in roots:
            self.assertAlmostEqual(abs(r), abs(1 + 1j) ** 0.2, places=9)
        angles = sorted(deg(r) for r in roots)
        gaps = [angles[k + 1] - angles[k] for k in range(4)]
        for g in gaps:
            self.assertAlmostEqual(g, 72.0, places=5, msg="五个根应每隔 72° 一个")

    def test_step7_2_第二块数据_曼德博缩略图(self):
        grid = ge.escape_grid(-2.0, 0.5, -1.25, 1.25, 40, 24, 60)
        flat = [v for line in grid for v in line]
        self.assertEqual(len(flat), 40 * 24)
        held = [v for v in flat if v == 60]
        self.assertTrue(180 <= len(held) <= 280,
                        msg=f"集内（60 步没逃出去）的格子有 {len(held)} 个，"
                            f"正常应在 180~280 之间；太少或太多说明窗口或判据错了")
        self.assertLess(min(flat), 10, msg="贴着窗口边缘的格子应该一两步就飞出去")
        self.assertEqual(max(flat), 60)

    def test_step7_3_交付证据写进out(self):
        os.makedirs(OUT, exist_ok=True)
        roots_path = os.path.join(OUT, "roots.csv")
        grid_path = os.path.join(OUT, "grid.csv")
        self.assertEqual(ge.save_points_csv(roots_path, ge.nth_roots(1 + 1j, 5)), 5)
        rows, cols = ge.save_grid_csv(grid_path, ge.escape_grid(-2.0, 0.5, -1.25, 1.25, 40, 24, 60))
        self.assertEqual((rows, cols), (24, 40))
        for path in (roots_path, grid_path):
            self.assertTrue(os.path.exists(path), msg=f"{path} 没写出来")
            self.assertGreater(os.path.getsize(path), 0)


# ---------------- 第 8 步 · numpy 加速（没装就跳过） ----------------

@unittest.skipUnless(HAS_NUMPY, "没装 numpy，第 8 步跳过（不影响前面 7 步的结论）")
class Step8_numpy加速(unittest.TestCase):

    def test_step8_1_和逐点版逐格相同(self):
        slow = ge.escape_grid(-2.0, 0.5, -1.25, 1.25, 40, 24, 60)
        fast = ge.escape_grid_np(-2.0, 0.5, -1.25, 1.25, 40, 24, 60)
        self.assertEqual(len(fast), 24)
        self.assertEqual(fast, slow, msg="向量化版必须和逐点版一模一样；差在边界上多半是坐标取了 linspace")

    def test_step8_2_形状是行在前列在后(self):
        grid = ge.escape_grid_np(-1.0, 1.0, -1.0, 1.0, 7, 4, 20)
        self.assertEqual(len(grid), 4, msg="高度 4 就是 4 行")
        self.assertEqual(len(grid[0]), 7, msg="宽度 7 就是每行 7 列")


if __name__ == "__main__":
    unittest.main(verbosity=2)


