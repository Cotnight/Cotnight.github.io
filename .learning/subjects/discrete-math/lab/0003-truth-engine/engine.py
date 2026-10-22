"""真值表引擎：穷举赋值，判「前提合取蕴含结论」是不是重言式，并报出反例。

公式写成嵌套元组（与 0001 的范式机、0002 的证明校对同一套写法）：

    'P'                     变元
    ('not', 'P')            ¬P
    ('and', 'P', 'Q')       P∧Q
    ('or', 'P', 'Q')        P∨Q
    ('imp', 'P', 'Q')       P→Q

本文件 7 个函数留白，分在任务 1～5 里；其余函数都写好了，不用改：

    任务 1  valuations、index_of        穷举赋值；给小项编号
    任务 2  evaluate                    递归求值
    任务 3  minterms                    真值列 → Σm 编号
    任务 4  counterexamples、is_valid   反例与有效性
    任务 5  mismatches                  与纸上答案对账

编号规则与 0001 那台范式机逐字一致：变元按字母顺序排，第一个变元占最高位，
真记 1。所以 ['P','Q','R'] 的 101 号赋值是 P=1、Q=0、R=1，写作 m5 / M5。
"""

import itertools

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
    """H1∧H2∧…∧Hn → C：判定重言式用的那条公式，可以拿去求 Σm。

    有效 ⇔ 它的主析取范式含全部 2^n 个小项（第 1 课的那句判定就在这里落地）。
    """
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
    """穷举全部赋值，按编号从小到大排好。任务 1 留白。

        valuations(['P', 'Q'])
        → [{'P': 0, 'Q': 0}, {'P': 0, 'Q': 1},
           {'P': 1, 'Q': 0}, {'P': 1, 'Q': 1}]

    第一个变元是最高位，所以它变得最慢：返回列表的第 i 项正好是 i 号赋值。
    itertools.product((0, 1), repeat=变元个数) 给的顺序已经是这个顺序，
    只要按 variables 的顺序 zip 回去，别自己反转。
    """
    raise NotImplementedError('任务 1：itertools.product 穷举，再 zip 回变元名')


def index_of(env, variables):
    """一个赋值的小项编号（0 … 2^n-1）。任务 1 留白。

        index_of({'P': 1, 'Q': 0, 'R': 1}, ['P', 'Q', 'R']) → 5   # 101

    第一个变元乘最高的权：从头往下读，读一位就 index = index * 2 + 这一位的值。
    这一步写反了（把第一个变元当最低位），后面整张 Σm 表都会错位，
    而错位后的编号照样「看起来像编号」，是最难自己发现的一处。
    """
    raise NotImplementedError('任务 1：从第一个变元往下读，index = index * 2 + 值')


# ── 任务 2：递归求值 ────────────────────────────────────────────


def evaluate(formula, env):
    """在给定赋值下求公式的真值，返回 0 或 1。任务 2 留白。

    四种联结词各有各的算法，其中只有蕴含不对称：
    P→Q 只在「P 真、Q 假」这一种情形下为 0。写成 min / max 会把它算成
    合取或析取，而真值表看上去仍然「有 0 有 1」，错得不显眼。
    """
    raise NotImplementedError('任务 2：变元查 env；not/and/or/imp 各一段，注意蕴含')


# ── 任务 3：真值列 → Σm 编号 ────────────────────────────────────


def minterms(formula, variables):
    """主析取范式的编号（升序）：真值为 1 的那些赋值。任务 3 留白。

        minterms(('imp', 'P', 'Q'), ['P', 'Q']) → [0, 1, 3]

    真值列的下标就是编号（truth_values 已经按编号排好），所以这一步只是
    「把值为 1 的下标挑出来」，一个变元都不用算。
    读出来的是成真赋值——第 1 课手算的那张表，这里由程序重新长一遍。
    """
    raise NotImplementedError('任务 3：enumerate 真值列，挑出值为 1 的下标')


# ── 任务 4：反例与有效性 ────────────────────────────────────────


def counterexamples(premises, conclusion, variables):
    """反例赋值：**前提全真、结论为假**的那些赋值。任务 4 留白。

    返回 dict 列表，顺序照编号从小到大；一个都没有就是空列表。

    两个条件缺一不可。只判「结论为假」就判无效，会把「前提本身就不成立」
    的赋值也算成反例，于是每题都「无效」；只判「前提全真」又会把
    结论为真的赋值也算进去。第 1 课的那句「推理有效 ⇔ 前提合取蕴含结论是
    重言式」，落到代码上就是这两行 and。
    """
    raise NotImplementedError('任务 4：前提全真 and 结论为假，两个条件都要')


def is_valid(premises, conclusion):
    """这个推理有效吗：反例一个都没有就是有效。任务 4 留白。

    变元取「前提与结论里出现过的全部变元」的并集，不能各按自己出现的算——
    结论里没出现某个变元时，那个变元要在前提的每一行上都穷举到。
    """
    raise NotImplementedError('任务 4：variables_of 求并集，再看反例是不是空')


# ── 任务 5：与纸上答案对账 ──────────────────────────────────────


def mismatches(case_list, answers):
    """把引擎的判定与一份答案表逐题比，返回对不上的那几道。任务 5 留白。

        case_list：题库，每道有 'no' / 'premises' / 'conclusion'
        answers：  {编号: True/False}，True 表示有效

    返回值是三元组列表：(编号, 引擎说, 答案说)，按题库顺序。
    答案表里没有的编号也算「对不上」（答案说那一项是 None），
    否则漏填一题会静默通过。
    """
    raise NotImplementedError('任务 5：逐题算 is_valid，再与 answers.get(编号) 比')
