"""真值表引擎的断言（参考解副本，与任务目录里的 `test_engine.py` 逐字相同）。

在本目录里跑：

    python -m unittest -v test_engine

只跑某一步（比如只跑到第 3 步）：

    python -m unittest -v test_engine.TestMinterms

断言失败时会指出是哪道题、哪个赋值——照那一行回去查。
"""

import unittest

import audit
import cases
import engine
import report

from cases import IMP_PQ, IMP_QR


# ── 任务 1：穷举赋值与编号 ──────────────────────────────────────


class TestValuations(unittest.TestCase):
    """任务 1：valuations 的顺序就是编号，index_of 是那张对照表。"""

    def test_two_vars(self):
        with self.subTest(task='valuations'):
            self.assertEqual(
                engine.valuations(['P', 'Q']),
                [{'P': 0, 'Q': 0}, {'P': 0, 'Q': 1},
                 {'P': 1, 'Q': 0}, {'P': 1, 'Q': 1}],
                '第一个变元要变得最慢，否则返回列表的下标就不是编号了')

    def test_three_vars_order(self):
        envs = engine.valuations(['P', 'Q', 'R'])
        with self.subTest(task='个数'):
            self.assertEqual(len(envs), 8, '三个变元应当有 2^3 = 8 个赋值')
        with self.subTest(task='首位'):
            self.assertEqual(envs[0], {'P': 0, 'Q': 0, 'R': 0}, '第 0 项应当是 000')
        with self.subTest(task='中间'):
            self.assertEqual(envs[5], {'P': 1, 'Q': 0, 'R': 1}, '第 5 项应当是 101')
        with self.subTest(task='末位'):
            self.assertEqual(envs[-1], {'P': 1, 'Q': 1, 'R': 1}, '最后一项应当是 111')

    def test_index_of(self):
        TABLE = (
            ({'P': 0, 'Q': 0}, ['P', 'Q'], 0),
            ({'P': 0, 'Q': 1}, ['P', 'Q'], 1),
            ({'P': 1, 'Q': 0}, ['P', 'Q'], 2),
            ({'P': 1, 'Q': 0, 'R': 1}, ['P', 'Q', 'R'], 5),
            ({'A': 0, 'B': 0, 'C': 1, 'D': 1}, ['A', 'B', 'C', 'D'], 3),
        )
        for env, variables, expect in TABLE:
            with self.subTest(赋值=engine.format_env(env, variables)):
                self.assertEqual(engine.index_of(env, variables), expect,
                                 '编号算错了：第一个变元占最高位')

    def test_index_matches_order(self):
        with self.subTest(task='下标即编号'):
            variables = ['P', 'Q', 'R']
            got = [engine.index_of(env, variables) for env in engine.valuations(variables)]
            self.assertEqual(got, [0, 1, 2, 3, 4, 5, 6, 7],
                             'valuations 的第 i 项，index_of 必须给出 i')


# ── 任务 2：递归求值 ────────────────────────────────────────────

# (公式, 赋值, 应当算出的真值)
EVAL = (
    ('P', {'P': 1}, 1),
    (('not', 'P'), {'P': 0}, 1),
    (('not', 'P'), {'P': 1}, 0),
    (('and', 'P', ('not', 'Q')), {'P': 1, 'Q': 0}, 1),
    (('and', 'P', 'Q'), {'P': 1, 'Q': 0}, 0),
    (('or', 'P', 'Q'), {'P': 0, 'Q': 0}, 0),
    (('imp', 'P', 'Q'), {'P': 1, 'Q': 0}, 0),
    (('imp', 'P', 'Q'), {'P': 0, 'Q': 0}, 1),
    (('imp', 'P', 'Q'), {'P': 1, 'Q': 1}, 1),
    (('imp', ('imp', 'P', 'Q'), 'R'), {'P': 1, 'Q': 1, 'R': 0}, 0),
    (('imp', ('and', 'P', 'Q'), ('or', 'R', 'S')),
     {'P': 1, 'Q': 1, 'R': 0, 'S': 0}, 0),
    (('or', ('and', 'P', ('not', 'Q')), ('and', ('not', 'P'), 'Q')),
     {'P': 1, 'Q': 0}, 1),
    (('or', ('and', 'P', ('not', 'Q')), ('and', ('not', 'P'), 'Q')),
     {'P': 1, 'Q': 1}, 0),
)


class TestEvaluate(unittest.TestCase):
    """任务 2：四种联结词各算对，蕴含只有一种情形为 0。"""

    def test_values(self):
        for formula, env, expect in EVAL:
            with self.subTest(公式=engine.formula_text(formula),
                              赋值=engine.format_env(env, sorted(env))):
                self.assertEqual(engine.evaluate(formula, env), expect,
                                 '%s 在这一行算错了' % engine.formula_text(formula))


# ── 任务 3：Σm 编号 ────────────────────────────────────────────


class TestMinterms(unittest.TestCase):
    """任务 3：真值列与编号，主析取范式的那组编号。"""

    def test_truth_column(self):
        with self.subTest(formula='P→Q'):
            self.assertEqual(engine.truth_values(('imp', 'P', 'Q'), ['P', 'Q']),
                             [1, 1, 0, 1],
                             '真值列按编号排：00、01、10、11')

    def test_minterms(self):
        TABLE = (
            (('imp', 'P', 'Q'), ['P', 'Q'], [0, 1, 3]),
            (('and', 'P', 'Q'), ['P', 'Q', 'R'], [6, 7]),
            (('or', 'P', ('not', 'P')), ['P'], [0, 1]),
            (('and', 'P', ('not', 'P')), ['P', 'Q'], []),
        )
        for formula, variables, expect in TABLE:
            with self.subTest(公式=engine.formula_text(formula)):
                self.assertEqual(engine.minterms(formula, variables), expect,
                                 'Σm 编号不对（重言式要占满全部编号，矛盾式是空表）')

    def test_maxterms_complement(self):
        with self.subTest(formula='P∧Q'):
            self.assertEqual(engine.maxterms(('and', 'P', 'Q'), ['P', 'Q', 'R']),
                             [0, 1, 2, 3, 4, 5],
                             'ΠM 是小项编号的补集')
        with self.subTest(task='互补'):
            variables = ['P', 'Q', 'R']
            sigma = engine.minterms(('imp', 'P', 'Q'), variables)
            pi = engine.maxterms(('imp', 'P', 'Q'), variables)
            self.assertEqual(sorted(sigma + pi), engine.all_indices(variables),
                             'Σm 与 ΠM 合起来必须正好占满 0…7')


# ── 任务 4：反例与有效性 ───────────────────────────────────────


class TestValidity(unittest.TestCase):
    """任务 4：反例 = 前提全真 且 结论为假。"""

    def test_modus_ponens(self):
        with self.subTest(rule='假言推理'):
            self.assertTrue(engine.is_valid([IMP_PQ, 'P'], 'Q'))
        with self.subTest(rule='假言三段论'):
            self.assertTrue(engine.is_valid([IMP_PQ, IMP_QR], ('imp', 'P', 'R')))
        with self.subTest(rule='化简'):
            self.assertTrue(engine.is_valid([('and', 'P', 'Q')], 'P'))

    def test_affirming_consequent(self):
        premises = [IMP_PQ, 'Q']
        with self.subTest(task='肯定后件是无效式'):
            self.assertFalse(engine.is_valid(premises, 'P'),
                             'P→Q 与 Q 推不出 P，反例是 P=0、Q=1')
        with self.subTest(task='反例就那一个'):
            self.assertEqual(engine.counterexamples(premises, 'P', ['P', 'Q']),
                             [{'P': 0, 'Q': 1}],
                             '反例要按「前提全真、结论为假」两个条件一起筛')

    def test_denying_antecedent(self):
        premises = [IMP_PQ, ('not', 'P')]
        with self.subTest(task='否定前件是无效式'):
            self.assertFalse(engine.is_valid(premises, ('not', 'Q')),
                             'P→Q 与 ¬P 推不出 ¬Q，反例也是 P=0、Q=1')
        with self.subTest(task='反例'):
            self.assertEqual(engine.counterexamples(premises, ('not', 'Q'), ['P', 'Q']),
                             [{'P': 0, 'Q': 1}])

    def test_counterexample_order(self):
        with self.subTest(task='两个反例按编号排'):
            self.assertEqual(
                engine.counterexamples([('or', 'P', 'Q')], ('and', 'P', 'Q'), ['P', 'Q']),
                [{'P': 0, 'Q': 1}, {'P': 1, 'Q': 0}],
                '01 在 10 前面：反例也要按编号从小到大报')

    def test_inconsistent_premises(self):
        with self.subTest(task='前提自己矛盾'):
            self.assertTrue(engine.is_valid(['P', ('not', 'P')], 'Q'),
                            '前提不相容时，任意结论都是有效结论（定义 1.8.2）')
        with self.subTest(task='但没有反例'):
            self.assertEqual(engine.counterexamples(['P', ('not', 'P')], 'Q', ['P', 'Q']),
                             [],
                             '前提永远不真，就不存在「前提真而结论假」的赋值')

    def test_entailment_formula(self):
        with self.subTest(task='有效 ⇔ 前提合取蕴含结论是重言式'):
            formula = engine.entailment_formula([IMP_PQ, 'Q'], 'P')
            self.assertEqual(engine.minterms(formula, ['P', 'Q']), [0, 2, 3],
                             '缺的那一号 1 正是反例；有效时要占满全部编号')


# ── 任务 5：对账 ───────────────────────────────────────────────


class TestBank(unittest.TestCase):
    """题库 16 道：引擎的判定必须等于课件给的答案。"""

    def test_every_case(self):
        for case in cases.CASES:
            with self.subTest(编号=case['no'], 出处=case['source']):
                self.assertEqual(engine.is_valid(case['premises'], case['conclusion']),
                                 case['book'],
                                 '%s 判反了：%s' % (case['no'], case['source']))

    def test_no_mismatch(self):
        with self.subTest(task='引擎 vs 课件'):
            self.assertEqual(engine.mismatches(cases.CASES, audit.book_answers()), [])


class TestMyAnswers(unittest.TestCase):
    """纸上那 16 道：填全，而且与引擎全部对上。"""

    def test_all_filled(self):
        with self.subTest(task='填全'):
            self.assertEqual(sorted(audit.MY_ANSWERS),
                             sorted(case['no'] for case in cases.CASES),
                             '16 道都要填：漏填的那几道在对账表里会显示「（没填）」')

    def test_no_mismatch(self):
        with self.subTest(task='引擎 vs 你纸上'):
            self.assertEqual(engine.mismatches(cases.CASES, audit.MY_ANSWERS), [],
                             '对不上的那几道，回去先复算反例')


class TestMismatch(unittest.TestCase):
    """对账函数自己也要经得起一份错答案。"""

    def test_wrong_answer_reported(self):
        answers = dict(audit.book_answers())
        answers['C11'] = True
        with self.subTest(task='改错一道'):
            self.assertEqual(engine.mismatches(cases.CASES, answers),
                             [('C11', False, True)],
                             '答案表写错一道，对账就要报出那一行')


# ── 打印依据：报告那一行 ───────────────────────────────────────


class TestReport(unittest.TestCase):
    """report.py 用的是引擎的结果，所以这两条也在验引擎。"""

    def test_valid_line(self):
        with self.subTest(编号='C01'):
            self.assertEqual(report.report_line(cases.CASES[0]),
                             'C01｜有效｜反例 0 / 4｜课件 1.8.2 真值表法例',
                             '有效的依据是「反例 0 / 4」，不是光写一个「有效」')

    def test_invalid_line(self):
        with self.subTest(编号='C11'):
            self.assertEqual(report.report_line(cases.by_no('C11')),
                             'C11｜无效｜反例 01（P=0，Q=1）｜肯定后件：无效式的样板',
                             '无效的依据是那个反例赋值：01，即 P=0、Q=1')


if __name__ == '__main__':
    unittest.main()
