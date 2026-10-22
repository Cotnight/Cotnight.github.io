"""推理证明校对机的断言：依据栏、蕴含式、行号引用、CP 与归谬的收尾。

在 lab/0002-proof-check 目录里跑：

    python -m unittest -v test_proof

只跑某一步（比如只跑第 2 步）：

    python -m unittest -v test_proof.TestStep

断言失败时会指出是哪份证明、第几行、依据栏写的是什么 —— 照那个行号回去查。
"""

import unittest

import proof as pr
import proofs
import proof_broken as bad

from proofs import IMP_PQ, IMP_QR


def with_basis(proof, number, basis):
    """复制一份证明，只改第 number 行（行号从 1 数）的依据栏。"""
    lines = list(proof['lines'])
    lines[number - 1] = (lines[number - 1][0], basis)
    return dict(proof, lines=lines)


# ── 第 1 步：依据栏 ────────────────────────────────────────────

BASIS = (
    ('P', ('P', (), '')),
    ('P（附加前提）', ('P+', (), '')),
    ('P(附加前提)', ('P+', (), '')),
    ('T，2，3，拒取式', ('T', (2, 3), '拒取式')),
    ('T，1，4，假言推理', ('T', (1, 4), '假言推理')),
    ('T，2，7，CP', ('CP', (2, 7), 'CP')),
    ('T，拒取式', ('T', (), '拒取式')),
    ('T，CP', ('CP', (), 'CP')),
)


class TestBasis(unittest.TestCase):
    """任务 1：把依据栏拆成「规则、行号、规则名」。"""

    def test_parse(self):
        for text, expect in BASIS:
            with self.subTest(basis=text):
                self.assertEqual(pr.parse_basis(text), expect,
                                 '依据栏 %r 拆错了' % text)

    def test_half_width_comma(self):
        with self.subTest(basis='T,2,4,CP'):
            self.assertEqual(pr.parse_basis('T,2,4,CP'), ('CP', (2, 4), 'CP'),
                             '半角逗号也要认：手写时两种都常见')

    def test_unreadable(self):
        for text in ('前提', '', 'P→Q'):
            with self.subTest(basis=text):
                self.assertIsNone(pr.parse_basis(text),
                                  '%r 不该拆得出来' % text)


# ── 第 2 步：七条蕴含式 ────────────────────────────────────────

# (规则名, 手里有的几行, 这一行想推出的公式, 这条蕴含式支不支持)
STEPS = (
    ('假言推理', [IMP_PQ, 'P'], 'Q', True),
    ('假言推理', [IMP_PQ, 'Q'], 'Q', False),
    ('拒取式', [IMP_PQ, ('not', 'Q')], ('not', 'P'), True),
    ('拒取式', [IMP_PQ, 'Q'], ('not', 'P'), False),
    ('析取三段论', [('or', 'P', 'Q'), ('not', 'P')], 'Q', True),
    ('析取三段论', [('or', 'P', 'Q'), ('not', 'P')], 'P', False),
    ('假言三段论', [IMP_PQ, IMP_QR], ('imp', 'P', 'R'), True),
    ('假言三段论', [IMP_PQ, IMP_QR], ('imp', 'R', 'P'), False),
    ('化简', [('and', 'P', 'Q')], 'P', True),
    ('化简', [('and', 'P', 'Q')], 'R', False),
    ('合成', ['P', 'Q'], ('and', 'P', 'Q'), True),
    ('合成', ['P'], ('and', 'P', 'Q'), False),
    ('附加', ['P'], ('or', 'P', 'Q'), True),
    ('附加', ['P'], ('or', 'Q', 'R'), False),
)


class TestStep(unittest.TestCase):
    """任务 2：规则名与公式形状配不配得上。"""

    def test_rules(self):
        for name, refs, conclusion, expect in STEPS:
            with self.subTest(rule=name, conclusion=pr.formula_text(conclusion)):
                self.assertEqual(pr.is_step(name, refs, conclusion), expect,
                                 '「%s」这一判错了' % name)

    def test_unknown_rule(self):
        with self.subTest(rule='逆否推理'):
            self.assertFalse(pr.is_step('逆否推理', [IMP_PQ, 'P'], 'Q'),
                             '本节只认七条蕴含式，别的名字一律不支持')


# ── 第 3 步：行号、引用与依据 ──────────────────────────────────


class TestLines(unittest.TestCase):
    """任务 3：逐行体检。"""

    def test_good_proofs(self):
        for name in ('PROOF_A', 'PROOF_B', 'PROOF_C', 'PROOF_D'):
            with self.subTest(proof=name):
                self.assertEqual(pr.line_issues(getattr(proofs, name)['lines']),
                                 [], '%s 的逐行检查不该报问题' % name)

    def test_missing_numbers(self):
        with self.subTest(proof='S1_NO_NUMBERS'):
            self.assertEqual(
                pr.line_issues(bad.S1_NO_NUMBERS['lines']),
                ['第 4 行：依据栏「T，拒取式」没写行号——T 行要写清引了哪几行'])

    def test_future_line(self):
        broken = with_basis(proofs.PROOF_A, 3, 'T，4，化简')
        with self.subTest(proof='PROOF_A 第 3 行引第 4 行'):
            self.assertEqual(pr.line_issues(broken['lines']),
                             ['第 3 行：引用了第 4 行，那一行还没出现'])

    def test_unknown_rule(self):
        broken = with_basis(proofs.PROOF_A, 5, 'T，1，4，逆否推理')
        with self.subTest(proof='PROOF_A 第 5 行规则名'):
            self.assertEqual(pr.line_issues(broken['lines']),
                             ['第 5 行：规则名「逆否推理」不在本节这七条里'])

    def test_unreadable_basis(self):
        broken = with_basis(proofs.PROOF_A, 2, '前提')
        with self.subTest(proof='PROOF_A 第 2 行依据栏'):
            self.assertEqual(
                pr.line_issues(broken['lines']),
                ['第 2 行：依据栏「前提」认不出——写成 P、'
                 'P（附加前提）或 T，行号，规则名'])

    def test_wrong_rule(self):
        broken = with_basis(proofs.PROOF_A, 4, 'T，2，3，假言推理')
        with self.subTest(proof='PROOF_A 第 4 行规则与公式不配'):
            self.assertEqual(pr.line_issues(broken['lines']),
                             ['第 4 行：第 2、3 行按「假言推理」推不出 ¬Q'])

    def test_cp_needs_two_numbers(self):
        broken = with_basis(proofs.PROOF_D, 5, 'T，CP')
        with self.subTest(proof='PROOF_D 第 5 行只写了 CP'):
            self.assertEqual(
                pr.line_issues(broken['lines']),
                ['第 5 行：CP 的依据要写两个行号——附加前提行号与末行前一行的行号'])


# ── 第 4 步：CP 还原与归谬矛盾 ─────────────────────────────────

CONTRA = (
    (('and', 'R', ('not', 'R')), True),
    (('and', ('not', 'P'), 'P'), True),
    (('and', 'P', 'Q'), False),
    (('not', 'P'), False),
    (('or', 'R', ('not', 'R')), False),
    ('P', False),
)


class TestEnding(unittest.TestCase):
    """任务 4：首行与末行。"""

    def test_contradiction(self):
        for formula, expect in CONTRA:
            with self.subTest(formula=pr.formula_text(formula)):
                self.assertEqual(pr.is_contradiction(formula), expect,
                                 '%s 判错了' % pr.formula_text(formula))

    def test_cp_and_direct_pass(self):
        for name in ('PROOF_A', 'PROOF_B', 'PROOF_D'):
            with self.subTest(proof=name):
                self.assertEqual(
                    pr.ending_issues(getattr(proofs, name)),
                    [], '%s 的收尾不该报问题' % name)

    def test_refutation_pass(self):
        with self.subTest(proof='PROOF_C'):
            self.assertEqual(pr.ending_issues(proofs.PROOF_C), [])

    def test_cp_not_restored(self):
        with self.subTest(proof='S2_CP_NOT_RESTORED'):
            self.assertEqual(
                pr.ending_issues(bad.S2_CP_NOT_RESTORED),
                ['第 2 行引入了附加前提 S，末行却停在 R——'
                 'CP 证完要把末行写成 S→… 并标 CP'])

    def test_wrong_assumption(self):
        with self.subTest(proof='S3_WRONG_ASSUMPTION'):
            self.assertEqual(
                pr.ending_issues(bad.S3_WRONG_ASSUMPTION),
                ['第 1 行：附加前提应当是结论的否定，即 P，现在写的是 ¬P'])

    def test_no_closing(self):
        with self.subTest(proof='S4_NO_CLOSING'):
            self.assertEqual(pr.ending_issues(bad.S4_NO_CLOSING),
                             ['末行写的是矛盾，但缺一句「按归谬法」的结论句'])

    def test_goal_as_premise(self):
        with self.subTest(proof='S5_GOAL_AS_PREMISE'):
            self.assertEqual(
                pr.ending_issues(bad.S5_GOAL_AS_PREMISE),
                ['第 4 行：把结论整行当成了前提——这一行一写就是循环论证'])

    def test_incomplete(self):
        with self.subTest(proof='S6_INCOMPLETE'):
            self.assertEqual(pr.ending_issues(bad.S6_INCOMPLETE),
                             ['末行是 ¬Q，不是结论 ¬P'])

    def test_cp_numbers(self):
        broken = with_basis(proofs.PROOF_D, 5, 'T，3，4，CP')
        with self.subTest(proof='PROOF_D 第 5 行引错了行号'):
            self.assertEqual(
                pr.ending_issues(broken),
                ['第 5 行：CP 的依据要写「T，2，4，CP」，附加前提行号在前'])


# ── 第 5 步：整份证明与你自己那份 ──────────────────────────────


class TestBroken(unittest.TestCase):
    """六份标本各报一句，不多不少。"""

    def test_s1_no_numbers(self):
        with self.subTest(specimen='S1'):
            self.assertEqual(
                pr.check_proof(bad.S1_NO_NUMBERS),
                ['第 4 行：依据栏「T，拒取式」没写行号——T 行要写清引了哪几行'])

    def test_s2_cp_not_restored(self):
        with self.subTest(specimen='S2'):
            self.assertEqual(
                pr.check_proof(bad.S2_CP_NOT_RESTORED),
                ['第 2 行引入了附加前提 S，末行却停在 R——'
                 'CP 证完要把末行写成 S→… 并标 CP'])

    def test_s3_wrong_assumption(self):
        with self.subTest(specimen='S3'):
            self.assertEqual(
                pr.check_proof(bad.S3_WRONG_ASSUMPTION),
                ['第 3 行：第 1、2 行按「假言推理」推不出 ¬Q',
                 '第 1 行：附加前提应当是结论的否定，即 P，现在写的是 ¬P'])

    def test_s4_no_closing(self):
        with self.subTest(specimen='S4'):
            self.assertEqual(pr.check_proof(bad.S4_NO_CLOSING),
                             ['末行写的是矛盾，但缺一句「按归谬法」的结论句'])

    def test_s5_goal_as_premise(self):
        with self.subTest(specimen='S5'):
            self.assertEqual(
                pr.check_proof(bad.S5_GOAL_AS_PREMISE),
                ['第 4 行：把结论整行当成了前提——这一行一写就是循环论证'])

    def test_s6_incomplete(self):
        with self.subTest(specimen='S6'):
            self.assertEqual(pr.check_proof(bad.S6_INCOMPLETE),
                             ['末行是 ¬Q，不是结论 ¬P'])


class TestWholeProof(unittest.TestCase):
    """四份示范证明与我录的那份都要全绿。"""

    def test_four_proofs(self):
        for name in ('PROOF_A', 'PROOF_B', 'PROOF_C', 'PROOF_D'):
            with self.subTest(proof=name):
                self.assertEqual(pr.check_proof(getattr(proofs, name)), [],
                                 '%s 应当一句问题都没有' % name)

    def test_my_proof(self):
        report = pr.check_proof(pr.MY_PROOF)
        with self.subTest(proof='MY_PROOF'):
            self.assertEqual(pr.MY_PROOF['goal'], 'R',
                             '这份证明的结论是 R，别改')
        with self.subTest(proof='MY_PROOF 体检'):
            self.assertEqual(report, [],
                             '你录的那份还有问题，逐条读：%s' % report)

    def test_empty(self):
        with self.subTest(proof='空证明'):
            self.assertEqual(pr.check_proof({'goal': 'R', 'lines': [],
                                             'closing': ''}),
                             ['一行都没有：先把前提逐条写成 P 行'])


if __name__ == '__main__':
    unittest.main()
