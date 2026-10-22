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


def _free_names(f, bound, names):
    """把自由变元名收进 names。bound 是「当前正被哪几个名字约束」。"""
    if isinstance(f, str):
        if f not in bound:
            names.add(f)
        return
    tag = f[0]
    if tag in ('all', 'exi'):
        _free_names(f[2], bound | {f[1]}, names)
        return
    if tag == 'atom':
        for arg in f[2]:
            _free_names(arg, bound, names)
        return
    if tag == 'not':
        _free_names(f[1], bound, names)
        return
    _free_names(f[1], bound, names)
    _free_names(f[2], bound, names)


def _count(f, name, bound):
    """(约束出现次数, 自由出现次数) 一对。"""
    if isinstance(f, str):
        if f != name:
            return (0, 0)
        return (1, 0) if name in bound else (0, 1)
    tag = f[0]
    if tag in ('all', 'exi'):
        return _count(f[2], name, bound | {f[1]})
    if tag == 'atom':
        total = (0, 0)
        for arg in f[2]:
            part = _count(arg, name, bound)
            total = (total[0] + part[0], total[1] + part[1])
        return total
    if tag == 'not':
        return _count(f[1], name, bound)
    left = _count(f[1], name, bound)
    right = _count(f[2], name, bound)
    return (left[0] + right[0], left[1] + right[1])


def free_variables(f):
    """公式的自由变元名，升序列表。"""
    names = set()
    _free_names(f, frozenset(), names)
    return sorted(names)


def free_occurrences(f, name):
    """变元 name 在公式里的自由出现次数。"""
    return _count(f, name, frozenset())[1]


def bound_occurrences(f, name):
    """变元 name 在公式里的约束出现次数。"""
    return _count(f, name, frozenset())[0]


# ── 任务 2：换名 ────────────────────────────────────────────────


def _binds(f, name):
    """公式里有没有以 name 为指导变元的量词。"""
    if isinstance(f, str):
        return False
    tag = f[0]
    if tag in ('all', 'exi'):
        return f[1] == name or _binds(f[2], name)
    if tag == 'atom':
        return False
    if tag == 'not':
        return _binds(f[1], name)
    return _binds(f[1], name) or _binds(f[2], name)


def _rename(f, old, new, bound):
    """只换「old 正被约束」的那些出现；bound 里没有 old 的，一律原样。"""
    if isinstance(f, str):
        return new if (f == old and old in bound) else f
    tag = f[0]
    if tag in ('all', 'exi'):
        guide = new if f[1] == old else f[1]
        return (tag, guide, _rename(f[2], old, new, bound | {f[1]}))
    if tag == 'atom':
        return ('atom', f[1], tuple(_rename(arg, old, new, bound) for arg in f[2]))
    if tag == 'not':
        return ('not', _rename(f[1], old, new, bound))
    return (tag, _rename(f[1], old, new, bound), _rename(f[2], old, new, bound))


def rename_bound(f, old, new):
    """把以 old 为指导变元的量词及其辖域内的 old 全部换成 new。"""
    if old == new:
        raise ValueError('新旧变元名相同：%s' % old)
    used = formula.variables(f)
    if new in used:
        raise ValueError('新名 %s 在公式里已经出现过（已有的变元：%s）'
                         % (new, '、'.join(used)))
    if not _binds(f, old):
        raise ValueError('公式里没有以 %s 为指导变元的量词；'
                         '改自由变元属于代入，不是换名' % old)
    return _rename(f, old, new, frozenset())


# ── 任务 3：有限模型上的真值 ────────────────────────────────────


def evaluate(f, model, assignment=None):
    """在模型上求公式的真值，返回 True / False。"""
    env = {} if assignment is None else assignment
    if isinstance(f, str):
        return env[f]
    tag = f[0]
    if tag == 'atom':
        name, args = f[1], f[2]
        key = tuple(env[arg] if arg in env else arg for arg in args)
        return key in model['pred'][name]
    if tag == 'not':
        return not evaluate(f[1], model, env)
    if tag == 'and':
        return evaluate(f[1], model, env) and evaluate(f[2], model, env)
    if tag == 'or':
        return evaluate(f[1], model, env) or evaluate(f[2], model, env)
    if tag == 'imp':
        return (not evaluate(f[1], model, env)) or evaluate(f[2], model, env)
    if tag in ('all', 'exi'):
        guide = f[1]
        truths = []
        for item in model['domain']:
            inner = dict(env)
            inner[guide] = item
            truths.append(evaluate(f[2], model, inner))
        return all(truths) if tag == 'all' else any(truths)
    raise ValueError('认不出这个公式：%r' % (f,))


# ── 任务 4：论域换了要重判 ──────────────────────────────────────


def domain_report(entry):
    """一道换论域的题 → [(论域名, 真值), …]，每一行重新算。"""
    return [(row['name'], evaluate(entry['formula'], row['model']))
            for row in entry['domains']]


# ── 任务 5：与课件真值对账 ──────────────────────────────────────


def audit(case_list):
    """逐题核对：(编号, 正确式真值, 错式真值, 课件真值)，按题库顺序。"""
    return [(case['no'],
             evaluate(case['right'], case['model']),
             evaluate(case['wrong'], case['model']),
             case['expected'])
            for case in case_list]


def misses(case_list):
    """错式没被抓住的题号：错式真值与课件真值相同的那些。"""
    return [no for no, right, wrong, expected in audit(case_list) if wrong == expected]
