"""范式机·坏的那一份：能跑，但三处结果不对。

接口与 normal_form.py 一样，公式写法也一样（见那一份开头的说明）。
下面这段代码是照着真实作业里的三处错法写的，每一处都写得像模像样、
跑起来也不报错，只是答案不对：

    1. expand_term：缺的变元一律按 0 补齐，不再展开 → 该落 2 格的项只落 1 格
    2. to_nnf    ：否号进括号时没有把 ∧ 与 ∨ 互换 → ¬(P∨Q) 被写成 ¬P∨¬Q
    3. dual       ：只换了 ∧ 与 ∨，没换 ↑↔↓ 与 1↔0 → (P∧Q)↑R 的对偶写成 (P∨Q)↑R

其余函数（truth_vector、minterms、maxterms、same_function）是对的。

这一份是「错法标本」：test_normal_form 里的 TestBroken 断言的正是它错成什么样，
所以它**不应该被修好** —— 修好之后那四条断言就会红。你要做的是认出这三处、
说出改哪个字就对了（改法就在你自己写的 normal_form.py 里）。
"""

VARS = ('P', 'Q', 'R')

SYMBOL = {'and': '∧', 'or': '∨', 'imp': '→', 'nand': '↑', 'nor': '↓'}


def bits(index, nvars):
    """编号 → 取值串，例如 bits(5, 3) == '101'。"""
    return format(index, '0%db' % nvars)


def index_of(row):
    """取值元组 → 编号，例如 index_of((1, 0, 1)) == 5。"""
    value = 0
    for bit in row:
        value = value * 2 + bit
    return value


def assignments(nvars):
    """按编号顺序列出全部赋值。"""
    rows = [()]
    for _ in range(nvars):
        rows = [row + (bit,) for row in rows for bit in (0, 1)]
    return rows


def env_of(row, nvars):
    """取值元组 → 求值用的字典。"""
    return {VARS[i]: row[i] for i in range(nvars)}


def evaluate(f, env):
    """在给定赋值下求值，返回 0 或 1。"""
    if isinstance(f, str):
        return env[f]
    tag = f[0]
    if tag == 'T':
        return 1
    if tag == 'F':
        return 0
    if tag == 'not':
        return 1 - evaluate(f[1], env)
    left = evaluate(f[1], env)
    right = evaluate(f[2], env)
    if tag == 'and':
        return int(left == 1 and right == 1)
    if tag == 'or':
        return int(left == 1 or right == 1)
    if tag == 'imp':
        return int(left == 0 or right == 1)
    if tag == 'nand':
        return int(not (left == 1 and right == 1))
    if tag == 'nor':
        return int(not (left == 1 or right == 1))
    raise ValueError('认不出的联结词：%r' % (tag,))


def to_text(f):
    """公式 → 人读的字符串。"""
    if isinstance(f, str):
        return f
    tag = f[0]
    if tag == 'T':
        return '1'
    if tag == 'F':
        return '0'
    if tag == 'not':
        inner = f[1]
        if isinstance(inner, str) or inner[0] == 'not':
            return '¬' + to_text(inner)
        return '¬(' + to_text(inner) + ')'
    return _operand_text(f[1]) + SYMBOL[tag] + _operand_text(f[2])


def _operand_text(f):
    """二元式的操作数：变元与否定号裸露，其余的加括号。"""
    if isinstance(f, str) or f[0] == 'not':
        return to_text(f)
    return '(' + to_text(f) + ')'


def vars_in(f):
    """公式里出现的变元，按 VARS 的位序返回元组。"""
    if isinstance(f, str):
        return (f,)
    if f[0] in ('T', 'F'):
        return ()
    if f[0] == 'not':
        return vars_in(f[1])
    left = vars_in(f[1])
    right = vars_in(f[2])
    return tuple(v for v in VARS if v in left or v in right)


def sigma_text(numbers):
    """编号列表 → 'Σm(0,1,3,7)'。"""
    return 'Σm(%s)' % ','.join(str(n) for n in numbers)


def pi_text(numbers):
    """编号列表 → 'ΠM(2,4,5,6)'。"""
    return 'ΠM(%s)' % ','.join(str(n) for n in numbers)


def truth_vector(f, nvars):
    """公式的真值列：'0'/'1' 串，第 i 个字符是编号 i 那一行的真值。"""
    return ''.join(str(evaluate(f, env_of(row, nvars)))
                   for row in assignments(nvars))


def minterms(f, nvars):
    """主析取范式的编号列表，升序。"""
    return [i for i, row in enumerate(assignments(nvars))
            if evaluate(f, env_of(row, nvars)) == 1]


def maxterms(f, nvars):
    """主合取范式的编号列表，升序。"""
    return [i for i, row in enumerate(assignments(nvars))
            if evaluate(f, env_of(row, nvars)) == 0]


def expand_term(term, nvars):
    """把缺变元的项补成小项（这一处有错：缺的变元按 0 补齐了）。"""
    full = {v: term.get(v, 0) for v in VARS[:nvars]}
    return [index_of(tuple(full[v] for v in VARS[:nvars]))]


def dual(f):
    """对偶式（这一处有错：只换了 ∧ 与 ∨）。"""
    if isinstance(f, str):
        return f
    tag = f[0]
    if tag in ('T', 'F'):
        return f
    if tag == 'not':
        return ('not', dual(f[1]))
    left = dual(f[1])
    right = dual(f[2])
    if tag == 'and':
        return ('or', left, right)
    if tag == 'or':
        return ('and', left, right)
    return (tag, left, right)


def to_nnf(f):
    """否号推到底（这一处有错：进括号时没换运算）。"""
    return _nnf(f, False)


def _nnf(f, neg):
    """neg 为真表示「正在给 f 求否定」。"""
    if isinstance(f, str):
        return ('not', f) if neg else f
    tag = f[0]
    if tag == 'T':
        return ('F',) if neg else ('T',)
    if tag == 'F':
        return ('T',) if neg else ('F',)
    if tag == 'not':
        return _nnf(f[1], not neg)
    if tag == 'imp':
        return _nnf(('or', ('not', f[1]), f[2]), neg)
    if tag == 'nand':
        return _nnf(('not', ('and', f[1], f[2])), neg)
    if tag == 'nor':
        return _nnf(('not', ('or', f[1], f[2])), neg)
    if not neg:
        return (tag, _nnf(f[1], False), _nnf(f[2], False))
    return (tag, _nnf(f[1], True), _nnf(f[2], True))


def same_function(f, g):
    """两个公式是否等值。"""
    used = vars_in(f) + vars_in(g)
    nvars = (max(VARS.index(v) for v in used) + 1) if used else 0
    return truth_vector(f, nvars) == truth_vector(g, nvars)
