"""范式机的断言：编号表、补变元、对偶式、否号内移、判等值。

在 lab/0001-minterm-index 目录里跑：

    python -m unittest -v test_normal_form

只跑某一步（比如只跑第 1 步）：

    python -m unittest -v test_normal_form.TestTable

断言失败时会指出是哪个式子、哪个编号 —— 照着那个编号回去查。
"""

import unittest

import normal_form as nf
import normal_form_broken as bad


# 五个式子：名字、公式、真值列（按编号 0→7，变元 P、Q、R）、Σm、ΠM。
# 真值列的写法是 bits(0) 到 bits(7) 的顺序：第一位是 000、最后一位是 111。
TABLE = (
    ('(P→Q)∧(Q→R)',
     ('and', ('imp', 'P', 'Q'), ('imp', 'Q', 'R')),
     '11010001', [0, 1, 3, 7], [2, 4, 5, 6]),
    ('P→Q',
     ('imp', 'P', 'Q'),
     '11110011', [0, 1, 2, 3, 6, 7], [4, 5]),
    ('((P∨Q)→R)→P',
     ('imp', ('imp', ('or', 'P', 'Q'), 'R'), 'P'),
     '00101111', [2, 4, 5, 6, 7], [0, 1, 3]),
    ('(P→Q)∧(P→R)',
     ('and', ('imp', 'P', 'Q'), ('imp', 'P', 'R')),
     '11110001', [0, 1, 2, 3, 7], [4, 5, 6]),
    ('P∨(Q→R)',
     ('or', 'P', ('imp', 'Q', 'R')),
     '11011111', [0, 1, 3, 4, 5, 6, 7], [2]),
)

# (P→Q)∧(Q→R) 代数展开后的三支：各自是部分赋值
THREE_BRANCHES = ({'P': 0, 'Q': 0}, {'P': 0, 'R': 1}, {'Q': 1, 'R': 1})


def neg_only_on_vars(f):
    """否定号都直接贴在变元上，且只剩 ¬、∧、∨ 这三种写法。"""
    if isinstance(f, str):
        return True
    tag = f[0]
    if tag in ('T', 'F'):
        return True
    if tag == 'not':
        return isinstance(f[1], str)
    if tag in ('and', 'or'):
        return neg_only_on_vars(f[1]) and neg_only_on_vars(f[2])
    return False


class TestTable(unittest.TestCase):
    """任务 1：真值列与两组编号。"""

    def test_truth_vector(self):
        for name, formula, vec, _sigma, _pi in TABLE:
            with self.subTest(formula=name):
                self.assertEqual(nf.truth_vector(formula, 3), vec,
                                 '%s 的真值列对不上' % name)

    def test_sigma(self):
        for name, formula, _vec, sigma, _pi in TABLE:
            with self.subTest(formula=name):
                self.assertEqual(nf.minterms(formula, 3), sigma,
                                 '%s 的 Σm 应当写 %s'
                                 % (name, nf.sigma_text(sigma)))

    def test_pi(self):
        for name, formula, _vec, _sigma, pi in TABLE:
            with self.subTest(formula=name):
                self.assertEqual(nf.maxterms(formula, 3), pi,
                                 '%s 的 ΠM 应当写 %s'
                                 % (name, nf.pi_text(pi)))

    def test_sigma_pi_complement(self):
        for name, formula, vec, sigma, pi in TABLE:
            with self.subTest(formula=name):
                self.assertEqual(sorted(sigma + pi), list(range(8)),
                                 '%s 的 Σm 与 ΠM 合起来要正好占满 0～7' % name)
                self.assertEqual(len(sigma), vec.count('1'),
                                 '%s 的成真赋值个数应当等于真值列里 1 的个数' % name)


class TestExpand(unittest.TestCase):
    """任务 2：缺变元补成小项。"""

    def test_one_var_missing(self):
        cases = (
            ({'P': 0, 'Q': 0}, [0, 1]),
            ({'P': 0, 'R': 1}, [1, 3]),
            ({'Q': 1, 'R': 1}, [3, 7]),
            ({'P': 1}, [4, 5, 6, 7]),
            ({'R': 1}, [1, 3, 5, 7]),
        )
        for term, expect in cases:
            with self.subTest(term=str(term)):
                self.assertEqual(nf.expand_term(term, 3), expect,
                                 '缺一个变元要落 2 格：%s' % nf.sigma_text(expect))

    def test_no_var_missing(self):
        self.assertEqual(nf.expand_term({'P': 1, 'Q': 1, 'R': 0}, 3), [6], '不缺变元只落 1 格')
        self.assertEqual(nf.expand_term({'P': 0, 'Q': 0, 'R': 0}, 3), [0])

    def test_all_free(self):
        self.assertEqual(nf.expand_term({}, 3), list(range(8)), '三个变元都不定，八格全落')

    def test_three_branches(self):
        got = [nf.expand_term(term, 3) for term in THREE_BRANCHES]
        self.assertEqual(got, [[0, 1], [1, 3], [3, 7]],
                         '三支各补成两个小项')
        union = sorted({n for part in got for n in part})
        self.assertEqual(union, [0, 1, 3, 7],
                         '三支并起来应当是 Σm(0,1,3,7)')
        self.assertEqual(sum(len(part) for part in got), 6,
                         '三支一共写出 6 个编号，并起来只剩 4 个：m1 与 m3 各出现两次')
        self.assertIn(1, got[0], 'm1 既在 ¬P∧¬Q 里')
        self.assertIn(1, got[1], 'm1 也在 ¬P∧R 里')
        self.assertIn(3, got[1], 'm3 既在 ¬P∧R 里')
        self.assertIn(3, got[2], 'm3 也在 Q∧R 里')


class TestDual(unittest.TestCase):
    """任务 3：对偶式。"""

    def test_nand_swaps_to_nor(self):
        f = ('nand', ('and', 'P', 'Q'), 'R')
        self.assertEqual(nf.to_text(nf.dual(f)), '(P∨Q)↓R',
                         '(P∧Q)↑R 的对偶是 (P∨Q)↓R：↑ 与 ↓ 也要换')

    def test_three_groups(self):
        cases = (
            (('or', ('not', 'P'), ('and', 'Q', 'R')), '¬P∧(Q∨R)'),
            (('and', ('and', 'P', 'Q'), ('T',)), '(P∨Q)∨0'),
            (('nor', 'P', 'Q'), 'P↑Q'),  # ↓ 的对偶是 ↑：否定号不动，只换联结词
        )
        for formula, expect in cases:
            with self.subTest(expect=expect):
                self.assertEqual(nf.to_text(nf.dual(formula)), expect,
                                 '对偶要换 ∧↔∨、↑↔↓、1↔0 三组')

    def test_double_dual(self):
        cases = (
            ('nand', ('and', 'P', 'Q'), 'R'),
            ('or', ('not', 'P'), ('and', 'Q', 'R')),
            ('and', ('and', 'P', 'Q'), ('T',)),
        )
        for formula in cases:
            with self.subTest(formula=nf.to_text(formula)):
                self.assertEqual(nf.to_text(nf.dual(nf.dual(formula))),
                                 nf.to_text(formula), '取两次对偶回到原式')

    def test_dual_principle(self):
        left = ('and', 'P', ('or', 'Q', 'R'))
        right = ('or', ('and', 'P', 'Q'), ('and', 'P', 'R'))
        self.assertEqual(nf.truth_vector(left, 3), nf.truth_vector(right, 3),
                         '分配律本来该成立')
        self.assertEqual(nf.truth_vector(nf.dual(left), 3),
                         nf.truth_vector(nf.dual(right), 3),
                         '成对的式子取对偶后也成对：一条主干配一次对偶')

    def test_fold_path(self):
        f = ('nand', ('and', 'P', 'Q'), 'R')
        folded = ('not', ('or', ('or', 'P', 'Q'), 'R'))
        self.assertEqual(nf.truth_vector(nf.dual(f), 3),
                         nf.truth_vector(folded, 3),
                         '折成 ¬∧∨ 再取对偶，与按定义换 ↑↔↓ 的结果必须一致')
        self.assertEqual(nf.to_text(nf.dual(f)), '(P∨Q)↓R')


class TestNNF(unittest.TestCase):
    """任务 4 的前一半：否号推到底。"""

    CASES = (
        ('not', ('or', 'P', 'Q')),
        ('not', ('and', 'P', 'Q')),
        ('imp', 'P', 'Q'),
        ('nand', 'P', 'Q'),
        ('nor', 'P', 'Q'),
        ('not', ('not', 'P')),
        ('not', ('imp', 'P', ('and', 'Q', 'R'))),
        ('and', ('imp', 'P', 'Q'), ('imp', 'Q', 'R')),
    )

    def test_equal_on_all_rows(self):
        for formula in self.CASES:
            with self.subTest(formula=nf.to_text(formula)):
                got = nf.to_nnf(formula)
                self.assertEqual(nf.truth_vector(got, 3), nf.truth_vector(formula, 3),
                                 '化成 %s 之后与原式不等值了' % nf.to_text(got))
                self.assertTrue(neg_only_on_vars(got),
                                '%s 里还有否定号压在括号上，或者还留着 → ↑ ↓'
                                % nf.to_text(got))

    def test_demorgan_or(self):
        got = nf.to_nnf(('not', ('or', 'P', 'Q')))
        self.assertIn(nf.to_text(got), ('¬P∧¬Q', '¬Q∧¬P'),
                      '¬(P∨Q) 该化成 ¬P∧¬Q，不是 ¬P∨¬Q')

    def test_demorgan_and(self):
        got = nf.to_nnf(('not', ('and', 'P', 'Q')))
        self.assertIn(nf.to_text(got), ('¬P∨¬Q', '¬Q∨¬P'),
                      '¬(P∧Q) 该化成 ¬P∨¬Q')

    def test_neg_of_imp(self):
        got = nf.to_nnf(('not', ('imp', 'P', ('and', 'Q', 'R'))))
        self.assertIn(nf.to_text(got), ('P∧(¬Q∨¬R)', 'P∧(¬R∨¬Q)'),
                      '¬(P→(Q∧R)) 先消箭头，再让否号穿进括号')


class TestSame(unittest.TestCase):
    """任务 4 的后一半：判等值。"""

    def test_equivalent_pair(self):
        self.assertTrue(nf.same_function(
            ('and', ('imp', 'P', 'Q'), ('imp', 'P', 'R')),
            ('imp', 'P', ('and', 'Q', 'R'))),
            '(P→Q)∧(P→R) 与 P→(Q∧R) 等值')

    def test_different_pair(self):
        self.assertFalse(nf.same_function(
            ('imp', 'P', ('and', 'Q', 'R')),
            ('or', 'P', ('imp', 'Q', 'R'))),
            'P→(Q∧R) 与 P∨(Q→R) 的编号不同，不能判等价')

    def test_union_of_vars(self):
        self.assertTrue(nf.same_function(
            'P',
            ('and', 'P', ('or', 'Q', ('not', 'Q')))),
            '两边变元数不同也要取并集再比：各按自己的变元算 n，编号会错位')

    def test_imp_vs_or_not(self):
        self.assertTrue(nf.same_function(
            ('imp', 'P', 'Q'),
            ('or', ('not', 'P'), 'Q')))

    def test_conjunction_is_not_its_conclusion(self):
        self.assertFalse(nf.same_function(
            ('and', ('imp', 'P', 'Q'), ('imp', 'Q', 'R')),
            ('imp', 'P', 'R')),
            '合取的两支只是蕴含 P→R，不是与它等值：P→R 的编号更多')


class TestBroken(unittest.TestCase):
    """把三处错法各自顶出来：它们错成什么，这里逐条钉死。"""

    def test_expand_misses_branch(self):
        term = {'Q': 1, 'R': 1}
        self.assertEqual(bad.expand_term(term, 3), [3],
                         '错法：缺的变元按 0 补齐，Q∧R 只落 m3')
        self.assertEqual(nf.expand_term(term, 3), [3, 7],
                         '正确：Q∧R 缺 P，要落 m3 与 m7 两格')
        got = sorted({n for t in THREE_BRANCHES
                      for n in bad.expand_term(t, 3)})
        self.assertEqual(got, [0, 1, 3],
                         '错法把三支并成 Σm(0,1,3)，比正确的 Σm(0,1,3,7) 少 m7')

    def test_demorgan_swaps_wrong(self):
        formula = ('not', ('or', 'P', 'Q'))
        got = bad.to_nnf(formula)
        self.assertIn(bad.to_text(got), ('¬P∨¬Q', '¬Q∨¬P'),
                      '错法：否号进括号时没换运算')
        self.assertEqual(bad.evaluate(got, {'P': 1, 'Q': 0, 'R': 0}), 1,
                         '错法在 P=1、Q=0 这一行露出来：它算出 1')
        self.assertEqual(nf.evaluate(nf.to_nnf(formula), {'P': 1, 'Q': 0, 'R': 0}), 0,
                         '正确结果在同一行是 0：P=1、Q=0 一行就能推翻那种写法')

    def test_dual_swaps_half(self):
        f = ('nand', ('and', 'P', 'Q'), 'R')
        self.assertEqual(bad.to_text(bad.dual(f)), '(P∨Q)↑R',
                         '错法：只换 ∧↔∨，↑ 与 ↓ 没换')
        self.assertEqual(nf.to_text(nf.dual(f)), '(P∨Q)↓R',
                         '正确：(P∨Q)↓R')

    def test_double_dual_hides_error(self):
        f = ('nand', ('and', 'P', 'Q'), 'R')
        self.assertEqual(bad.to_text(bad.dual(bad.dual(f))), bad.to_text(f),
                         '取两次对偶回到原式 —— 这条自查对「只换一半」不设防，'
                         '所以对偶要用折成 ¬∧∨ 的路子再验一遍')


if __name__ == '__main__':
    unittest.main()
