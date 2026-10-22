"""谓词翻译与换名的断言：辖域、换名、求值、换论域、三处错法。

在 lab/0005-pred-translation 目录里跑：

    python -m unittest -v test_scope

只跑某一步：

    python -m unittest -v test_scope.TestScope
    python -m unittest -v test_scope.TestRename
    python -m unittest -v test_scope.TestEvaluate
    python -m unittest -v test_scope.TestDomains
    python -m unittest -v test_scope.TestTranslations
    python -m unittest -v test_scope.TestBroken

断言失败时会指出是哪个式子、哪个变元、哪一道题、哪一行——
照那一行回去查，别从头读代码。
"""

import unittest

import broken
import cases
import formula
import scope


# ── 任务 1：谁在辖域里 ──────────────────────────────────────────


class TestScope(unittest.TestCase):
    """任务 1：自由变元与约束变元，按出现次数数。"""

    def test_free_variables(self):
        TABLE = (
            (cases.EXAMPLE_1_1, ['y', 'z']),
            (cases.EXAMPLE_1_2, ['x', 'y', 'z']),
            (cases.RENAME_PAIR, ['x', 'y']),
            (('all', 'x', ('atom', 'S', ('x',))), []),
            (('exi', 'x', ('all', 'y', ('atom', 'A', ('x', 'y')))), []),
        )
        for f, expect in TABLE:
            with self.subTest(公式=formula.formula_text(f)):
                self.assertEqual(scope.free_variables(f), expect,
                                 '自由变元数错了：外面没有以它自己为指导变元的量词，才算自由')

    def test_occurrence_counts(self):
        # (公式, 变元, 约束出现次数, 自由出现次数)
        TABLE = (
            (cases.EXAMPLE_1_1, 'y', 2, 1),
            (cases.EXAMPLE_1_1, 'x', 2, 0),
            (cases.EXAMPLE_1_2, 'x', 1, 2),
            (cases.EXAMPLE_1_2, 'y', 1, 1),
            (cases.EXAMPLE_1_2, 'z', 0, 1),
            (cases.EXAMPLE_1_2, 'w', 0, 0),
        )
        for f, name, bound, free in TABLE:
            with self.subTest(公式=formula.formula_text(f), 变元=name):
                self.assertEqual(scope.bound_occurrences(f, name), bound,
                                 '约束出现次数不对：数的是该变元在量词辖域里的出现')
                self.assertEqual(scope.free_occurrences(f, name), free,
                                 '自由出现次数不对：数的是该变元在辖域外的出现')

    def test_same_letter_both_ways(self):
        f = cases.EXAMPLE_1_2
        with self.subTest(task='x 既约束又自由'):
            self.assertIn('x', scope.free_variables(f),
                          '后件里的 x 已经脱离 ∀x 的辖域，是自由变元')
            self.assertEqual(scope.bound_occurrences(f, 'x'), 1,
                             '∀x 的括号在前件就收尾了，它只管到 H(x) 那一处')
        with self.subTest(task='两种次数加起来是总出现数'):
            total = (scope.bound_occurrences(f, 'x')
                     + scope.free_occurrences(f, 'x'))
            self.assertEqual(total, 3, 'x 在这条公式里一共出现 3 处')


# ── 任务 2：换名 ────────────────────────────────────────────────


class TestRename(unittest.TestCase):
    """任务 2：换名只动指导变元与辖域里的那些出现。"""

    def test_inner_binder(self):
        expect = ('all', 'x',
                  ('imp',
                   ('atom', 'H', ('x', 'y')),
                   ('exi', 's',
                    ('and', ('atom', 'W', ('s',)),
                            ('atom', 'L', ('x', 's', 'z'))))))
        got = scope.rename_bound(cases.RENAME_CASE, 'y', 's')
        with self.subTest(task='内层 ∃y 换成 ∃s'):
            self.assertEqual(got, expect,
                             '课件第 44 页例1 的第二个换名：H(x,y) 里的 y 在辖域外，要原样留着')
        with self.subTest(task='自由变元集合不变'):
            self.assertEqual(scope.free_variables(got), ['y', 'z'],
                             '换名不改变自由变元：改完还是 y 与 z')

    def test_free_variable_outside_scope_untouched(self):
        expect = ('and',
                  ('all', 't',
                   ('imp', ('atom', 'P', ('t',)),
                           ('atom', 'R', ('t', 'y')))),
                  ('atom', 'L', ('x', 'y')))
        got = scope.rename_bound(cases.RENAME_PAIR, 'x', 't')
        with self.subTest(task='外层 L(x,y) 的 x 不动'):
            self.assertEqual(got, expect,
                             '∀x 的辖域只到 P(x)→R(x,y)，L(x,y) 里那个 x 是自由变元')
        with self.subTest(task='自由变元集合不变'):
            self.assertEqual(scope.free_variables(got), ['x', 'y'])

    def test_new_name_must_be_fresh(self):
        with self.subTest(task='撞上指导变元 x'):
            with self.assertRaises(ValueError):
                scope.rename_bound(cases.RENAME_CASE, 'y', 'x')
        with self.subTest(task='撞上自由变元 z'):
            with self.assertRaises(ValueError):
                scope.rename_bound(cases.RENAME_CASE, 'y', 'z')

    def test_no_binder_to_rename(self):
        with self.subTest(task='没有以 w 为指导变元的量词'):
            with self.assertRaises(ValueError):
                scope.rename_bound(cases.RENAME_CASE, 'w', 's')


# ── 任务 3：有限模型上的真值 ────────────────────────────────────


class TestEvaluate(unittest.TestCase):
    """任务 3：原子查外延，量词把论域走一遍。"""

    def test_atoms(self):
        m = cases.model([1, 2], S={(2,)})
        with self.subTest(task='1 不满足 S'):
            self.assertFalse(scope.evaluate(('atom', 'S', ('x',)), m, {'x': 1}))
        with self.subTest(task='2 满足 S'):
            self.assertTrue(scope.evaluate(('atom', 'S', ('x',)), m, {'x': 2}))

    def test_not(self):
        m = cases.model([1], S=set())
        with self.subTest(task='¬S(1)'):
            self.assertTrue(scope.evaluate(('not', ('atom', 'S', ('x',))), m, {'x': 1}))

    def test_quantifiers(self):
        m = cases.model([1, 2, 3], S={(2,), (3,)})
        with self.subTest(task='全称：1 不是素数'):
            self.assertFalse(scope.evaluate(('all', 'x', ('atom', 'S', ('x',))), m))
        with self.subTest(task='存在：2 是素数'):
            self.assertTrue(scope.evaluate(('exi', 'x', ('atom', 'S', ('x',))), m))

    def test_imp_inside_scope(self):
        m = cases.model([1, 2], S={(2,)}, E={(1,)})
        f = ('all', 'x', ('imp', ('atom', 'S', ('x',)), ('atom', 'E', ('x',))))
        with self.subTest(task='2 让蕴含为假，全称跟着假'):
            self.assertFalse(scope.evaluate(f, m),
                             'S→E 对 2 为假（2 是素数但不小于 2），全称因此为假')

    def test_closed_without_assignment(self):
        m = cases.model(['a'], S={('a',)})
        with self.subTest(task='闭式不传 assignment 也能算'):
            self.assertTrue(scope.evaluate(('all', 'x', ('atom', 'S', ('x',))), m))


# ── 任务 4：论域换了要重判 ──────────────────────────────────────


class TestDomains(unittest.TestCase):
    """任务 4：同一串字，两个论域，两行真值各算各的。"""

    def test_domain_flips_truth(self):
        for entry in cases.DOMAINS:
            with self.subTest(编号=entry['no'], 中文=entry['chinese']):
                got = [truth for _, truth in scope.domain_report(entry)]
                self.assertEqual(got, entry['expected'],
                                 '式子的字没变，论域变了真值就跟着变：每一行都要重算')

    def test_rows_carry_domain_name(self):
        entry = cases.by_domain('D01')
        with self.subTest(task='每行带论域名'):
            self.assertEqual([name for name, _ in scope.domain_report(entry)],
                             ['论域 {2, 3}', '论域 {1, 2, 3}'])


# ── 任务 5：与课件真值对账 ──────────────────────────────────────


class TestTranslations(unittest.TestCase):
    """任务 5：正确式等于课件真值，错式被同一个模型抓住。"""

    def test_right_formula_matches_book(self):
        for case in cases.TRANSLATIONS:
            with self.subTest(编号=case['no'], 中文=case['chinese']):
                self.assertEqual(
                    scope.evaluate(case['right'], case['model']), case['expected'],
                    '正确式在这个模型上与课件真值对不上')

    def test_wrong_formula_is_caught(self):
        for case in cases.TRANSLATIONS:
            with self.subTest(编号=case['no'], 错法=case['fault']):
                self.assertNotEqual(
                    scope.evaluate(case['wrong'], case['model']), case['expected'],
                    '这个模型没把错式抓住：错式的真值竟然与课件真值相同')

    def test_audit_rows(self):
        rows = scope.audit(cases.TRANSLATIONS)
        with self.subTest(task='行数与顺序'):
            self.assertEqual([row[0] for row in rows],
                             [case['no'] for case in cases.TRANSLATIONS])
        with self.subTest(编号='T01'):
            self.assertEqual(rows[0], ('T01', False, True, False),
                             'T01 正确式假、错式真、课件真值假')

    def test_misses(self):
        with self.subTest(task='五道错式都抓住'):
            self.assertEqual(scope.misses(cases.TRANSLATIONS), [],
                             '有错式没被抓住，回去看那一题的模型')
        case = cases.by_no('T02')
        swapped = dict(case, right=case['wrong'], wrong=case['right'])
        with self.subTest(task='正确式与错式对调，misses 要报出来'):
            self.assertEqual(scope.misses([swapped]), ['T02'])


# ── 三处错法：每处都要有一个模型把它与正确答案分开 ──────────────


class TestBroken(unittest.TestCase):
    """`broken.py` 的三处错法，各有一条断言钉住——这就是本课的三条反例。"""

    def test_rename_touches_free(self):
        right = scope.rename_bound(cases.RENAME_CASE, 'y', 's')
        wrong = broken.rename_touches_free(cases.RENAME_CASE, 'y', 's')
        with self.subTest(task='公式文本不一样'):
            self.assertNotEqual(formula.formula_text(wrong), formula.formula_text(right),
                                '错法把 H(x,y) 里的 y 也改了，正确解留着它')
        with self.subTest(task='自由变元集合被改掉'):
            self.assertEqual(scope.free_variables(right), ['y', 'z'])
            self.assertEqual(scope.free_variables(wrong), ['s', 'z'],
                             '错法把自由变元 y 变成了 s：换名动到了辖域外的东西')

    def test_wired_all_takes_and(self):
        m = cases.model([-1, 0, 1, 2], F={(1,), (2,)}, M={(1,), (2,)})
        right = ('all', 'x', ('imp', ('atom', 'F', ('x',)), ('atom', 'M', ('x',))))
        wrong = broken.wired('all', 'F', 'M')
        with self.subTest(task='正确式为真'):
            self.assertTrue(scope.evaluate(right, m))
        with self.subTest(task='错法被 -1 拉成假'):
            self.assertFalse(scope.evaluate(wrong, m),
                             '全称接了合取：-1 不是正数，合取链就断在这里')

    def test_wired_exi_takes_imp(self):
        m = cases.model([1, 2, 3, 4], S={(2,), (3,)}, E={(1,)})
        right = ('exi', 'x', ('and', ('atom', 'S', ('x',)), ('atom', 'E', ('x',))))
        wrong = broken.wired('exi', 'S', 'E')
        with self.subTest(task='正确式为假'):
            self.assertFalse(scope.evaluate(right, m))
        with self.subTest(task='错法被 1 白送成真'):
            self.assertTrue(scope.evaluate(wrong, m),
                            '存在接了蕴含：1 不是素数，前件假、蕴含真，整句就真了')

    def test_sticky_truth_keeps_first_row(self):
        entry = cases.by_domain('D01')
        got = [truth for _, truth in broken.sticky_truth(entry)]
        with self.subTest(task='两行都是第一行的真值'):
            self.assertEqual(got, [True, True])
        with self.subTest(task='与逐行重算的答案不同'):
            self.assertNotEqual(got, entry['expected'],
                                '论域换了不重判，正是这一课的第一处薄弱点')

    def test_sticky_truth_breaks_second_case(self):
        entry = cases.by_domain('D02')
        got = [truth for _, truth in broken.sticky_truth(entry)]
        with self.subTest(task='错法抄成 [False, False]'):
            self.assertEqual(got, [False, False])
        with self.subTest(task='正确答案是 [False, True]'):
            self.assertNotEqual(got, entry['expected'])


if __name__ == '__main__':
    unittest.main()
