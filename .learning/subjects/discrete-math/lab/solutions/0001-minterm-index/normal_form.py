"""范式机·参考解：把公式变成编号表，再读出成真赋值。

本目录是自包含的：把这里的四个文件单独拷进一个空目录，
`python -m unittest -v test_normal_form` 照样能跑通。

本课只用三个变元 P、Q、R，位序固定：P 最高位、R 最低位。
编号 m_i / M_i 里的 i，就是这个赋值按 P、Q、R 顺序拼出的二进制值（真记 1）。
同一行上 m_i 为真、M_i 为假，所以同一个式子的 Σm 与 ΠM 恰好互补。

公式写成嵌套元组，变元直接写字符串：

    'P'                    变元 P
    ('not', 'P')           ¬P
    ('and', 'P', 'Q')      P∧Q
    ('or', 'P', 'Q')       P∨Q
    ('imp', 'P', 'Q')      P→Q
    ('nand', 'P', 'Q')     P↑Q（与非）
    ('nor', 'P', 'Q')      P↓Q（或非）
    ('T',)                 1
    ('F',)                 0

例：(P∧Q)↑R 写作 ('nand', ('and', 'P', 'Q'), 'R')。
"""

VARS = ('P', 'Q', 'R')

SYMBOL = {'and': '∧', 'or': '∨', 'imp': '→', 'nand': '↑', 'nor': '↓'}


# ── 工具 ────────────────────────────────────────────────────────


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
    """按编号顺序列出全部赋值：assignments(2) == [(0,0), (0,1), (1,0), (1,1)]。

    第 i 项就是 bits(i, nvars) 那一位串拆开的元组。
    """
    rows = [()]
    for _ in range(nvars):
        rows = [row + (bit,) for row in rows for bit in (0, 1)]
    return rows


def env_of(row, nvars):
    """取值元组 → 求值用的字典，例如 env_of((1,0,1), 3) == {'P':1,'Q':0,'R':1}。"""
    return {VARS[i]: row[i] for i in range(nvars)}


def evaluate(f, env):
    """在给定赋值下求值，返回 0 或 1。env 是 {'P':1,'Q':0,'R':1} 这样的字典。"""
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
    """公式 → 人读的字符串，(('nand', ('and','P','Q'), 'R')) 写作 '(P∧Q)↑R'。"""
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
    """二元式的操作数：变元、常量与否定号裸露，其余的加括号。"""
    if isinstance(f, str) or f[0] in ('not', 'T', 'F'):
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


# ── 任务 1：编号表 ──────────────────────────────────────────────


def truth_vector(f, nvars):
    """公式的真值列：'0'/'1' 串，第 i 个字符就是编号 i 那一行的真值。"""
    return ''.join(str(evaluate(f, env_of(row, nvars)))
                   for row in assignments(nvars))


def minterms(f, nvars):
    """主析取范式的编号列表（真值为 1 的行），升序。"""
    return [i for i, row in enumerate(assignments(nvars))
            if evaluate(f, env_of(row, nvars)) == 1]


def maxterms(f, nvars):
    """主合取范式的编号列表（真值为 0 的行），升序。"""
    return [i for i, row in enumerate(assignments(nvars))
            if evaluate(f, env_of(row, nvars)) == 0]


# ── 任务 2：缺变元补成小项 ──────────────────────────────────────


def expand_term(term, nvars):
    """把缺变元的项补成小项，返回编号列表。

    做法是枚举：0～2^n-1 全试一遍，满足 term 里每一条约束的就是落点。
    缺 k 个变元自然落 2**k 格，不用去数。
    """
    return [i for i, row in enumerate(assignments(nvars))
            if all(env_of(row, nvars)[var] == value
                   for var, value in term.items())]


# ── 任务 3：对偶式 ──────────────────────────────────────────────


def dual(f):
    """对偶式：∧↔∨、↑↔↓、1↔0 三组一起换；变元、括号、否定号一概不动。"""
    if isinstance(f, str):
        return f
    tag = f[0]
    if tag in ('T', 'F'):
        return ('F',) if tag == 'T' else ('T',)
    if tag == 'not':
        return ('not', dual(f[1]))
    swap = {'and': 'or', 'or': 'and', 'nand': 'nor', 'nor': 'nand'}
    return (swap[tag], dual(f[1]), dual(f[2]))


# ── 任务 4：否号推到底、判等值 ──────────────────────────────────


def to_nnf(f):
    """把否号推到变元前面，只留 ¬、∧、∨（→、↑、↓ 全部消掉）。"""
    return _nnf(f, False)


def _nnf(f, neg):
    """neg 为真表示「正在给 f 求否定」，这一层否定号就不再写进结果。"""
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
        # A→B 换成 ¬A∨B
        return _nnf(('or', ('not', f[1]), f[2]), neg)
    if tag == 'nand':
        # A↑B 换成 ¬(A∧B)
        return _nnf(('not', ('and', f[1], f[2])), neg)
    if tag == 'nor':
        # A↓B 换成 ¬(A∨B)
        return _nnf(('not', ('or', f[1], f[2])), neg)
    if not neg:
        return (tag, _nnf(f[1], False), _nnf(f[2], False))
    # 关键一行：否号穿进括号，∧ 与 ∨ 必须互换
    flip = 'or' if tag == 'and' else 'and'
    return (flip, _nnf(f[1], True), _nnf(f[2], True))


def same_function(f, g):
    """两个公式是否等值：变元取并集，n 取到最靠后的那个变元为止，再逐行比。"""
    used = vars_in(f) + vars_in(g)
    nvars = (max(VARS.index(v) for v in used) + 1) if used else 0
    return truth_vector(f, nvars) == truth_vector(g, nvars)
