"""谓词公式怎么写、怎么打印（本节的公共格式，任务与答案都用它）。

    'x'                          变元，写成字符串
    ('atom', 'S', ('x',))        S(x)；一元谓词
    ('atom', 'A', ('x', 'y'))    A(x, y)；n 元谓词，参数一律当变元写
    ('not', f)                   ¬f
    ('and', a, b)                a∧b
    ('or',  a, b)                a∨b
    ('imp', a, b)                a→b
    ('all', 'x', f)              ∀x f
    ('exi', 'x', f)              ∃x f

与 0001 的范式机、0002 的证明校对、0003 的真值表引擎是同一族写法，
只多了量词与谓词两项。

本文件是现成的工具，**不用改**。公式本身没有「辖域」这个字段：
辖域是读出来的——量词后面紧跟的那一对括号里的整段就是它的辖域，
所以 ('all', 'x', body) 的 body 整段都在 ∀x 底下，body 之外一律不在。
"""

SYMBOL = {'and': '∧', 'or': '∨', 'imp': '→'}
QUANT = {'all': '∀', 'exi': '∃'}


def formula_text(f):
    """公式 → 人读的字符串：('all','x',('atom','S',('x',))) 写作 '∀x(S(x))'。"""
    if isinstance(f, str):
        return f
    tag = f[0]
    if tag == 'atom':
        return '%s(%s)' % (f[1], ','.join(f[2]))
    if tag == 'not':
        return '¬' + _operand(f[1])
    if tag in QUANT:
        return QUANT[tag] + f[1] + '(' + formula_text(f[2]) + ')'
    return _operand(f[1]) + SYMBOL[tag] + _operand(f[2])


def _operand(f):
    """二元式的操作数：变元、原子公式、否定号裸露，其余加一层括号。"""
    if isinstance(f, str) or f[0] in ('atom', 'not'):
        return formula_text(f)
    return '(' + formula_text(f) + ')'


def variables(f, found=None):
    """公式里出现过的变元名（连当指导变元的也算），升序列表。"""
    names = set() if found is None else found
    if isinstance(f, str):
        names.add(f)
        return sorted(names)
    tag = f[0]
    if tag == 'atom':
        for arg in f[2]:
            variables(arg, names)
    elif tag == 'not':
        variables(f[1], names)
    elif tag in QUANT:
        names.add(f[1])
        variables(f[2], names)
    else:
        variables(f[1], names)
        variables(f[2], names)
    return sorted(names)
