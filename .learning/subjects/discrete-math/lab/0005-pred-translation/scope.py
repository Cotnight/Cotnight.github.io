"""本课要你填的 7 个函数：辖域与变元角色、换名、有限模型求值、换论域重判、翻译对账。

分 5 步，与任务书《谓词翻译与换名.md》对应：

    任务 1  free_variables、free_occurrences、bound_occurrences   谁在辖域里
    任务 2  rename_bound                                          换名只动辖域里的变元
    任务 3  evaluate                                              有限模型上的真值
    任务 4  domain_report                                         论域换了要重判
    任务 5  audit                                                 正确式与错式逐题对账

公式怎么写见 `formula.py`，题库与模型见 `cases.py`。
本文件只填下面 7 个 raise 处，已有的函数签名与说明不要改。
"""

import formula


# ── 任务 1：谁在辖域里 ──────────────────────────────────────────


def free_variables(f):
    """公式的自由变元名，升序列表。任务 1 留白。

        free_variables(cases.EXAMPLE_1_2) → ['x', 'y', 'z']

    判据：一个出现是不是自由的，只看它外面**有没有以它自己为指导变元的量词**。
    有量词、但量词管的是别的字母（例如 ∀x 里的 y），那个 y 照样自由。
    返回的是变元**名**：同一个名字出现几处都只算一个。
    """
    raise NotImplementedError('任务 1：带着「哪几个名字正被约束」这层信息递归')


def free_occurrences(f, name):
    """变元 name 在公式里的**自由出现**次数。任务 1 留白。

        free_occurrences(cases.EXAMPLE_1_2, 'x') → 2      # F(x) 与 L 的第一个位置

    数的是出现次数，不是变元个数：同一个 x 出现两处就记 2。
    """
    raise NotImplementedError('任务 1：与 free_variables 同一趟递归，改成分开数')


def bound_occurrences(f, name):
    """变元 name 在公式里的**约束出现**次数。任务 1 留白。

        bound_occurrences(cases.EXAMPLE_1_2, 'x') → 1      # H(x)，在 ∀x 辖域里
        bound_occurrences(cases.EXAMPLE_1_2, 'y') → 1      # L 的第二个位置，在 ∃y 辖域里

    同一字母可以既约束又自由：两种次数各数各的，加起来才是它出现的总次数。
    """
    raise NotImplementedError('任务 1：与 free_occurrences 一对，判据只差 bound 里有没有它')


# ── 任务 2：换名 ────────────────────────────────────────────────


def rename_bound(f, old, new):
    """把以 old 为**指导变元**的量词及其辖域内的 old 全部换成 new。任务 2 留白。

        rename_bound(cases.RENAME_PAIR, 'x', 't')
        → ('and',
           ('all', 't', ('imp', ('atom','P',('t',)), ('atom','R',('t','y')))),
           ('atom', 'L', ('x', 'y')))
        外层 L(x,y) 里那个 x 在 ∀x 辖域之外，一个字母都不动。

    两条硬要求（课件 2.4.2 的两条）：
    1. 改动范围只有两处：量词的指导变元，以及**该辖域内**该变元的每一处出现，
       公式的其余部分不变；
    2. 新名不许与公式里已有的变元撞名，否则报 ValueError（本节比课件更严：
       整条公式都不许出现，不只辖域内）。

    公式里没有以 old 为指导变元的量词，也报 ValueError——那说明你想改的
    其实是一个自由变元，改它属于代入，不是换名。
    """
    raise NotImplementedError('任务 2：先验新名，再带着「哪些名字正被约束」递归')


# ── 任务 3：有限模型上的真值 ────────────────────────────────────


def evaluate(f, model, assignment=None):
    """在模型上求公式的真值，返回 True / False。任务 3 留白。

        W = cases.model([1, 2], S={(2,)}, E={(1,)})
        evaluate(('exi','x',('and',('atom','S',('x',)),('atom','E',('x',)))), W)
        → False

    递归照结构走：
    - 原子公式：参数先换成论域里的客体（`assignment` 里有就用它，没有就当客体常项），
      再看这个元组在不在 `model['pred'][谓词名]` 里；
    - not / and / or / imp 各一段，蕴含只有「前真后假」为 False；
    - 量词：把 `model['domain']` 逐个代进指导变元——
      全称要**每个**客体都真，存在要**有一个**客体真。

    自由变元靠 `assignment` 给值（`{'x': 2}`）。本节要算的式子都是闭式，
    不传 `assignment` 就行；变元查不到值时会抛 KeyError，
    那说明你拿一条不闭的式子来求值了。
    """
    raise NotImplementedError('任务 3：原子查外延，量词把 model["domain"] 走一遍')


# ── 任务 4：论域换了要重判 ──────────────────────────────────────


def domain_report(entry):
    """一道换论域的题 → [(论域名, 真值), …]，每一行**重新算**。任务 4 留白。

        domain_report(cases.DOMAINS[0])
        → [('论域 {2, 3}', True), ('论域 {1, 2, 3}', False)]

    式子的字一个都没改，论域一换真值就跟着换——所以每一行都要拿它自己的
    模型重算一遍。把第一行的真值抄给后面几行，是这一课最贵的错法。
    """
    raise NotImplementedError('任务 4：逐行 evaluate(entry["formula"], 那一行的 model)')


# ── 任务 5：与课件真值对账 ──────────────────────────────────────


def audit(case_list):
    """逐题核对：返回 (编号, 正确式真值, 错式真值, 课件真值) 四元组列表，按题库顺序。任务 5 留白。

        audit([cases.by_no('T01')]) → [('T01', False, True, False)]

    一行四格：正确式在这个模型上的真值、错式的、课件给的真值。
    正确式该等于课件真值；错式该不等于——不等于就说明这个模型把错法抓住了。
    """
    raise NotImplementedError('任务 5：逐题算 evaluate(right)、evaluate(wrong)，与 expected 排成一行')


def misses(case_list):
    """错式没被抓住的题号：错式真值与课件真值相同的那些。已经写好，不用改。"""
    return [no for no, right, wrong, expected in audit(case_list) if wrong == expected]
