"""推理证明校对：把一张「行号、公式、依据」三列的证明表交给断言，逐行核依据。

公式写成嵌套元组（与 0001 那台范式机同一套写法）：

    'P'                     变元
    ('not', 'P')            ¬P
    ('and', 'P', 'Q')       P∧Q
    ('or', 'P', 'Q')        P∨Q
    ('imp', 'P', 'Q')       P→Q

依据栏照考试原样写成字符串，逗号用全角：

    'P'                     前提
    'P（附加前提）'          附加前提（CP 与归谬的起点）
    'T，2，3，拒取式'        由第 2、3 行按拒取式推得
    'T，2，7，CP'            CP 收尾

一份证明写成字典：

    {'goal': 结论公式, 'lines': [(公式, 依据), …], 'closing': '…'}

行号不存进数据：它就是列表下标加一，所以「行号连续」这条自带。
closing 只有归谬法要写（「由第 8 行得矛盾，按归谬法，原推理有效。」），
直接证法与 CP 留空字符串。

（参考解：6 个留白函数都填好了，其余部分与任务目录那份逐字相同。）
"""

RULES = ('假言推理', '拒取式', '析取三段论', '假言三段论', '化简', '合成', '附加')

SYMBOL = {'and': '∧', 'or': '∨', 'imp': '→'}


# ── 现成的工具（不用改）──────────────────────────────────────────


def formula_text(f):
    """公式 → 人读的字符串：('and', 'P', ('not', 'Q')) 写作 'P∧¬Q'。"""
    if isinstance(f, str):
        return f
    if f[0] == 'not':
        return '¬' + _operand_text(f[1])
    return _operand_text(f[1]) + SYMBOL[f[0]] + _operand_text(f[2])


def _operand_text(f):
    """二元式的操作数：变元与否定号裸露，其余加括号。"""
    if isinstance(f, str):
        return f
    if f[0] == 'not':
        return formula_text(f)
    return '(' + formula_text(f) + ')'


def negate(f):
    """结论的否定：¬P 的否定是 P，其余的在前面加一个 ¬。"""
    if isinstance(f, tuple) and f[0] == 'not':
        return f[1]
    return ('not', f)


# ── 任务 1：解析依据栏 ──────────────────────────────────────────


def parse_basis(basis):
    """依据栏 → (规则, 行号元组, 规则名)。

    'P'              → ('P', (), '')
    'P（附加前提）'   → ('P+', (), '')
    'T，2，3，拒取式' → ('T', (2, 3), '拒取式')
    'T，2，7，CP'    → ('CP', (2, 7), 'CP')
    认不出就返回 None —— 让调用方报出「第几行的依据栏认不出」。
    """
    text = basis.replace(' ', '').replace(',', '，')
    if text == 'P':
        return ('P', (), '')
    if text in ('P（附加前提）', 'P(附加前提)'):
        return ('P+', (), '')
    parts = [p for p in text.split('，') if p != '']
    if not parts or parts[0] != 'T':
        return None
    numbers = []
    name = ''
    for part in parts[1:]:
        if part.isdigit():
            numbers.append(int(part))
        else:
            name = part
    if name == 'CP':
        return ('CP', tuple(numbers), 'CP')
    return ('T', tuple(numbers), name)


# ── 任务 2：蕴含式对不对 ────────────────────────────────────────


def is_step(name, refs, conclusion):
    """refs（几行已推出来的公式，顺序无关）按 name 能不能得出 conclusion。

    七条蕴含式：假言推理、拒取式、析取三段论、假言三段论、化简、合成、附加。
    认不出的 name 一律返回 False。
    """
    if name == '假言推理':
        for f in refs:
            if isinstance(f, tuple) and f[0] == 'imp':
                if f[1] in refs and conclusion == f[2]:
                    return True
        return False
    if name == '拒取式':
        for f in refs:
            if isinstance(f, tuple) and f[0] == 'imp':
                if ('not', f[2]) in refs and conclusion == ('not', f[1]):
                    return True
        return False
    if name == '析取三段论':
        for f in refs:
            if isinstance(f, tuple) and f[0] == 'or':
                if ('not', f[1]) in refs and conclusion == f[2]:
                    return True
                if ('not', f[2]) in refs and conclusion == f[1]:
                    return True
        return False
    if name == '假言三段论':
        for f in refs:
            if isinstance(f, tuple) and f[0] == 'imp':
                for g in refs:
                    if isinstance(g, tuple) and g[0] == 'imp' and g[1] == f[2]:
                        if conclusion == ('imp', f[1], g[2]):
                            return True
        return False
    if name == '化简':
        for f in refs:
            if isinstance(f, tuple) and f[0] == 'and':
                if conclusion in (f[1], f[2]):
                    return True
        return False
    if name == '合成':
        if isinstance(conclusion, tuple) and conclusion[0] == 'and':
            return conclusion[1] in refs and conclusion[2] in refs
        return False
    if name == '附加':
        if isinstance(conclusion, tuple) and conclusion[0] == 'or':
            return conclusion[1] in refs or conclusion[2] in refs
        return False
    return False


# ── 任务 3：行号、引用与依据 ────────────────────────────────────


def line_issues(lines):
    """逐行核三件事：依据栏认不认得出、引的行存不存在、这一行推不推得出。

    返回问题清单（字符串列表）；一行问题都没有就是空列表。
    """
    issues = []
    formulas = [line[0] for line in lines]
    for index, (formula, basis) in enumerate(lines):
        number = index + 1
        parsed = parse_basis(basis)
        if parsed is None:
            issues.append('第 %d 行：依据栏「%s」认不出——写成 P、'
                          'P（附加前提）或 T，行号，规则名' % (number, basis))
            continue
        kind, refs, name = parsed
        if kind in ('P', 'P+'):
            continue
        if kind == 'CP':
            if len(refs) < 2:
                issues.append('第 %d 行：CP 的依据要写两个行号——'
                              '附加前提行号与末行前一行的行号' % number)
            continue
        if not refs:
            issues.append('第 %d 行：依据栏「%s」没写行号——'
                          'T 行要写清引了哪几行' % (number, basis))
            continue
        later = [r for r in refs if r < 1 or r > index]
        if later:
            issues.append('第 %d 行：引用了第 %s 行，那一行还没出现'
                          % (number, '、'.join(str(r) for r in later)))
            continue
        if name not in RULES:
            issues.append('第 %d 行：规则名「%s」不在本节这七条里'
                          % (number, name))
            continue
        cited = [formulas[r - 1] for r in refs]
        if not is_step(name, cited, formula):
            issues.append('第 %d 行：第 %s 行按「%s」推不出 %s'
                          % (number, '、'.join(str(r) for r in refs),
                             name, formula_text(formula)))
    return issues


# ── 任务 4：首行与末行（CP 还原、归谬矛盾）──────────────────────


def is_contradiction(f):
    """是不是一对矛盾：A∧¬A 这种形状，左右顺序不限。"""
    if not isinstance(f, tuple) or f[0] != 'and':
        return False
    left, right = f[1], f[2]
    return right == negate(left) or left == negate(right)


def ending_issues(proof):
    """核首行与末行：结论有没有被当前提、CP 有没有还原、归谬有没有推成矛盾。"""
    issues = []
    lines = proof['lines']
    goal = proof['goal']
    closing = proof.get('closing', '')
    formulas = [line[0] for line in lines]
    parsed = [parse_basis(line[1]) for line in lines]

    for index, (formula, basis) in enumerate(lines):
        if parsed[index] is not None and parsed[index][0] == 'P':
            if formula == goal:
                issues.append('第 %d 行：把结论整行当成了前提——'
                              '这一行一写就是循环论证' % (index + 1))

    plus_numbers = [i + 1 for i, p in enumerate(parsed)
                    if p is not None and p[0] == 'P+']
    cp_numbers = [i + 1 for i, p in enumerate(parsed)
                  if p is not None and p[0] == 'CP']

    if cp_numbers and not plus_numbers:
        issues.append('标了 CP，却没有任何一行写 P（附加前提）')
        return issues

    if not plus_numbers:
        if formulas[-1] != goal:
            issues.append('末行是 %s，不是结论 %s'
                          % (formula_text(formulas[-1]), formula_text(goal)))
        return issues

    plus_no = plus_numbers[0]
    plus_formula = formulas[plus_no - 1]

    if not cp_numbers:
        if is_contradiction(formulas[-1]) or '归谬' in closing:
            if plus_formula != negate(goal):
                issues.append('第 %d 行：附加前提应当是结论的否定，即 %s，'
                              '现在写的是 %s'
                              % (plus_no, formula_text(negate(goal)),
                                 formula_text(plus_formula)))
            if not is_contradiction(formulas[-1]):
                issues.append('末行是 %s，不是一对矛盾——'
                              '归谬法要推到 R∧¬R' % formula_text(formulas[-1]))
            if '归谬' not in closing:
                issues.append('末行写的是矛盾，但缺一句「按归谬法」的结论句')
        else:
            issues.append('第 %d 行引入了附加前提 %s，末行却停在 %s——'
                          'CP 证完要把末行写成 %s→… 并标 CP'
                          % (plus_no, formula_text(plus_formula),
                             formula_text(formulas[-1]),
                             formula_text(plus_formula)))
        return issues

    cp_no = cp_numbers[-1]
    if cp_no != len(lines):
        issues.append('第 %d 行：CP 收尾必须是最后一行' % cp_no)
    if cp_no < 2:
        issues.append('第 %d 行：CP 收尾之前至少要有一行被合成的公式' % cp_no)
        return issues
    expected = ('imp', plus_formula, formulas[cp_no - 2])
    if formulas[cp_no - 1] != expected:
        issues.append('第 %d 行：CP 收尾要把附加前提 %s 与前一行的 %s 合成 %s'
                      % (cp_no, formula_text(plus_formula),
                         formula_text(formulas[cp_no - 2]),
                         formula_text(expected)))
    refs = parsed[cp_no - 1][1]
    if refs != (plus_no, cp_no - 1):
        issues.append('第 %d 行：CP 的依据要写「T，%d，%d，CP」，'
                      '附加前提行号在前' % (cp_no, plus_no, cp_no - 1))
    if formulas[-1] != goal:
        issues.append('末行是 %s，不是结论 %s——CP 写完末行必须等于结论'
                      % (formula_text(formulas[-1]), formula_text(goal)))
    return issues


def check_proof(proof):
    """整份证明的体检报告：先逐行核（任务 3），再核首行与末行（任务 4）。"""
    if not proof.get('lines'):
        return ['一行都没有：先把前提逐条写成 P 行']
    return line_issues(proof['lines']) + ending_issues(proof)


# ── 任务 5：自己录一份证明 ──────────────────────────────────────

# 课件 1.8.3 例4：前提 (P→(Q∨R))∧(¬S→¬Q)∧(P∧¬S)，结论 R。
# 行号、公式、依据照你的答卷录进来；check_proof(MY_PROOF) 要交回空清单。
MY_PROOF = {
    'goal': 'R',
    'lines': [
        (('and', 'P', ('not', 'S')), 'P'),
        ('P', 'T，1，化简'),
        (('not', 'S'), 'T，1，化简'),
        (('imp', 'P', ('or', 'Q', 'R')), 'P'),
        (('or', 'Q', 'R'), 'T，2，4，假言推理'),
        (('imp', ('not', 'S'), ('not', 'Q')), 'P'),
        (('not', 'Q'), 'T，3，6，假言推理'),
        ('R', 'T，5，7，析取三段论'),
    ],
    'closing': '',
}
