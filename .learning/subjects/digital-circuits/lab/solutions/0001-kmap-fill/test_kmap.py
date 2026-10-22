"""卡诺图填图的逐格断言（任务目录那一份的自包含副本）。

与 lab/0001-kmap-fill/test_kmap.py 的代码逐字相同，只换了这段文件头说明；
放在这里是为了让参考解自带夹具，拷到空目录就能跑。

    python -m unittest -v test_kmap
"""

import unittest

import kmap
import kmap_broken


# 数字钟的分频级：三位二进制计数器，计数值到 6、7 时测试点 T=1。
# 行按 Q2Q1Q0 递增列（000、001、……、111），T 依次是：
DECODE_TABLE = (0, 0, 0, 0, 0, 0, 1, 1)


class TestCellOf(unittest.TestCase):
    """任务 1 的前一半：编号 → 格。"""

    def test_three_vars(self):
        expect = {
            0: (0, 0), 1: (0, 1), 2: (0, 3), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 3), 7: (1, 2),
        }
        for minterm, cell in expect.items():
            with self.subTest(m='m%d' % minterm):
                self.assertEqual(kmap.cell_of(minterm, 3), cell)

    def test_four_vars(self):
        expect = {
            0: (0, 0), 1: (0, 1), 2: (0, 3), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 3), 7: (1, 2),
            8: (3, 0), 9: (3, 1), 10: (3, 3), 11: (3, 2),
            12: (2, 0), 13: (2, 1), 14: (2, 3), 15: (2, 2),
        }
        for minterm, cell in expect.items():
            with self.subTest(m='m%d' % minterm):
                self.assertEqual(kmap.cell_of(minterm, 4), cell)


class TestFillFromTable(unittest.TestCase):
    """任务 1：真值表逐行搬进方格，再搬回来。"""

    def test_row_by_row(self):
        grid = kmap.fill_from_table(3, DECODE_TABLE)
        for minterm, value in enumerate(DECODE_TABLE):
            bits = kmap.bits_of(minterm, 3)
            row, col = kmap.cell_of(minterm, 3)
            with self.subTest(取值=bits, m='m%d' % minterm):
                self.assertEqual(
                    grid[row][col], value,
                    '%s（m%d）在第 %d 行第 %d 列，应填 %d'
                    % (bits, minterm, row + 1, col + 1, value))
        self.assertEqual(grid, [[0, 0, 0, 0], [0, 0, 1, 1]])
        self.assertEqual(sum(sum(line) for line in grid), sum(DECODE_TABLE),
                         '图上的 1 数应当等于真值表里输出为 1 的行数')

    def test_back_to_minterms(self):
        grid = [[0, 1, 0, 1], [1, 0, 0, 0]]
        self.assertEqual(kmap.minterms_from_grid(grid, 3), [1, 2, 4])


class TestProductTerms(unittest.TestCase):
    """任务 2：缺变量的项落多格。"""

    def test_missing_vars_spread(self):
        cases = (
            ({'A': 0, 'B': 1}, 3, [2, 3]),
            ({'A': 1}, 3, [4, 5, 6, 7]),
            ({'C': 1}, 3, [1, 3, 5, 7]),
            ({'A': 0, 'B': 1}, 4, [4, 5, 6, 7]),
            ({'C': 1, 'D': 1}, 4, [3, 7, 11, 15]),
            ({'B': 1, 'D': 1}, 4, [5, 7, 13, 15]),
        )
        for term, nvars, expect in cases:
            with self.subTest(nvars=nvars, term=str(sorted(term.items()))):
                got = sorted(kmap.cells_of_product(term, nvars))
                self.assertEqual(got, expect)

    def test_overlap_counts_once(self):
        grid = kmap.fill_from_products(4, [{'A': 0, 'B': 1}, {'C': 1, 'D': 1}])
        self.assertEqual(kmap.minterms_from_grid(grid, 4),
                         [3, 4, 5, 6, 7, 11, 15])
        self.assertEqual(sum(sum(line) for line in grid), 7,
                         '两项各 4 格、m7 重叠，图上一共 7 格 1')


class TestBroken(unittest.TestCase):
    """任务 3：把 kmap_broken.py 修到与 kmap.py 一致，这三条才会过。"""

    def test_axis_labels(self):
        self.assertEqual(kmap_broken.gray_axis(2), kmap.gray_axis(2))

    def test_cells_match_good(self):
        for minterm in range(16):
            with self.subTest(m='m%d' % minterm):
                self.assertEqual(kmap_broken.cell_of(minterm, 4),
                                 kmap.cell_of(minterm, 4),
                                 'm%d 在坏图上落错了格' % minterm)

    def test_no_missing_cells(self):
        got = sorted(kmap_broken.cells_of_product({'B': 1, 'D': 1}, 4))
        self.assertEqual(got, [5, 7, 13, 15],
                         '缺变量的项落成 %d 格了，应当 4 格' % len(got))


if __name__ == '__main__':
    unittest.main()
