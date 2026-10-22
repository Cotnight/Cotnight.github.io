"""真值表引擎（参考解）：穷举赋值，判「前提合取蕴含结论」是不是重言式，并报出反例。

七个留白函数都已填好；其余部分与任务目录里的 `engine.py` 逐字相同，
所以把本目录整套拷进一个空目录也能直接跑 `python -m unittest -v test_engine`。
"""

import itertools

SYMBOL = {'and': '∧', 'or': '∨', 'imp': '→'}


# ── 工具 ────────────────────────────────────────────────────────


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


def variables_of(forms):
    """几道公式里出现过的变元，按字母顺序排——这就是编号时的位序。"""
    names = set()
    for f in forms:
        _collect_vars(f, names)
    return sorted(names)


def _collect_vars(f, names):
    if isinstance(f, str):
        names.add(f)
        return
    for part in f[1:]:
        _collect_vars(part, names)


def all_indices(variables):
    """全部编号：0 … 2^n - 1。"""
    return list(range(2 ** len(variables)))


def format_env(env, variables):
    """{'P': 0, 'Q': 1} → '01（P=0，Q=1）'：前一段是编号的二进制写法。"""
    bits = ''.join(str(env[v]) for v in variables)
    pairs = '，'.join('%s=%d' % (v, env[v]) for v in variables)
    return '%s（%s）' % (bits, pairs)


def entailment_formula(premises, conclusion):
    """H1∧H2∧…∧Hn → C：判定重言式用的那条公式，可以拿去求 Σm。"""
    head = premises[0]
    for nxt in premises[1:]:
        head = ('and', head, nxt)
    return ('imp', head, conclusion)


def truth_values(formula, variables):
    """公式在全部赋值上的真值，列表下标就是编号：第 i 项对应 i 号赋值。"""
    return [evaluate(formula, env) for env in valuations(variables)]


def maxterms(formula, variables):
    """ΠM 的编号：小项编号的补集，升序。Σm 与 ΠM 合起来正好占满 0 … 2^n-1。"""
    chosen = set(minterms(formula, variables))
    return [i for i in all_indices(variables) if i not in chosen]


# ── 任务 1：穷举赋值与编号 ──────────────────────────────────────


def valuations(variables):
    """穷举全部赋值，按编号从小到大排好。

    itertools.product 让最后一个变元变得最快，正好就是「第一个变元占最高位」，
    所以返回列表的第 i 项就是 i 号赋值，不必再排一遍。
    """
    bits_list = itertools.product((0, 1), repeat=len(variables))
    return [dict(zip(variables, bits)) for bits in bits_list]


def index_of(env, variables):
    """一个赋值的小项编号：从头往下读，读一位就 index = index * 2 + 这一位的值。"""
    index = 0
    for v in variables:
        index = index * 2 + env[v]
    return index


# ── 任务 2：递归求值 ────────────────────────────────────────────


def evaluate(formula, env):
    """在给定赋值下求公式的真值，返回 0 或 1。"""
    if isinstance(formula, str):
        return env[formula]
    head = formula[0]
    if head == 'not':
        return 1 - evaluate(formula[1], env)
    left = evaluate(formula[1], env)
    right = evaluate(formula[2], env)
    if head == 'and':
        return min(left, right)
    if head == 'or':
        return max(left, right)
    if head == 'imp':
        return 1 if (left == 0 or right == 1) else 0
    raise ValueError('认不出的联结词：%r' % (head,))


# ── 任务 3：真值列 → Σm 编号 ────────────────────────────────────


def minterms(formula, variables):
    """主析取范式的编号（升序）：真值为 1 的那些赋值。"""
    values = truth_values(formula, variables)
    return [i for i, value in enumerate(values) if value == 1]


# ── 任务 4：反例与有效性 ────────────────────────────────────────


def counterexamples(premises, conclusion, variables):
    """反例赋值：前提全真、结论为假。两个条件缺一不可。"""
    found = []
    for env in valuations(variables):
        premises_true = all(evaluate(p, env) == 1 for p in premises)
        if premises_true and evaluate(conclusion, env) == 0:
            found.append(env)
    return found


def is_valid(premises, conclusion):
    """反例一个都没有就是有效；变元取前提与结论的并集。"""
    variables = variables_of(list(premises) + [conclusion])
    return counterexamples(premises, conclusion, variables) == []


# ── 任务 5：与纸上答案对账 ──────────────────────────────────────


def mismatches(case_list, answers):
    """逐题比：返回 (编号, 引擎说, 答案说) 三元组；答案表里漏掉的也算对不上。"""
    found = []
    for case in case_list:
        engine_says = is_valid(case['premises'], case['conclusion'])
        says = answers.get(case['no'])
        if says != engine_says:
            found.append((case['no'], engine_says, says))
    return found
