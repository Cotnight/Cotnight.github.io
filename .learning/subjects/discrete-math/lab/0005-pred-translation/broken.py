"""三处错法的标本：本课真正要你认出来的三种错。

**不要修**这些函数。它们是断言要打的对象（`test_scope.py` 的 `TestBroken`）：
断言会证明这三处错在一个具体模型上都与正确答案分得开——
分不开，学生就永远看不出自己错在哪一处。

    错法 1  rename_touches_free   换名时把辖域外的同名自由变元一起改了
    错法 2  wired                 特性谓词接错边：全称接合取、存在接蕴含
    错法 3  sticky_truth          论域换了不重判，把第一行的真值抄给每一行

错法 2、3 靠 `scope.evaluate` 才验得出对错，所以先把任务 3 弄绿，再看这几条。
"""

import scope


def _blind(f, old, new):
    """把公式里**所有** old 换成 new，不管它在不在辖域里。"""
    if isinstance(f, str):
        return new if f == old else f
    tag = f[0]
    if tag == 'atom':
        return ('atom', f[1], tuple(_blind(arg, old, new) for arg in f[2]))
    if tag == 'not':
        return ('not', _blind(f[1], old, new))
    if tag in ('all', 'exi'):
        return (tag, new if f[1] == old else f[1], _blind(f[2], old, new))
    return (tag, _blind(f[1], old, new), _blind(f[2], old, new))


def rename_touches_free(f, old, new):
    """错法 1：按字面换名。

    换名规则只改「指导变元 + 该辖域内该变元的出现」，这个函数把辖域外的
    同名变元也一起改了。后果不是「真值变了」，而是**自由变元集合变了**：
    原本的自由变元 x 变成 t，此后按原式约定的代入与求值全部错位。
    """
    return _blind(f, old, new)


def wired(kind, prop, claim):
    """错法 2：两边接反。'all' 接合取、'exi' 接蕴含。

    kind 取 'all' 或 'exi'，prop 是特性谓词名，claim 是那句结论的谓词名。
    接反之后，一块「不是 prop」的石头就能把这句判反——
    `test_scope.py` 的 `TestBroken` 拿 -1 与 1 各试一次。
    """
    op = 'and' if kind == 'all' else 'imp'
    return (kind, 'x', (op, ('atom', prop, ('x',)), ('atom', claim, ('x',))))


def sticky_truth(entry):
    """错法 3：只算第一行，把那个真值抄给每一行。

    entry 是 `cases.DOMAINS` 里的一道题。式子的字一个字没改，
    论域一换真值就可能翻——抄第一行等于根本没按新论域重判。
    """
    first = scope.evaluate(entry['formula'], entry['domains'][0]['model'])
    return [(row['name'], first) for row in entry['domains']]
