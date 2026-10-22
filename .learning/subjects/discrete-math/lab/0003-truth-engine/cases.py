"""题库：课件 1.8 的例题 + 五个经典无效式，共 16 道。只读，不要改。

每道题一个字典：

    no          编号，C01 起
    premises    前提，公式列表（合取关系：全部都要为真）
    conclusion  结论
    book        课件（教材）给的答案：True 有效 / False 无效 —— 这就是标准答案
    source      出处；无效的那几道写清是哪一类错法

公式写法与 0001、0002 相同。变元一律单字母大写，编号时按字母顺序排位。

几道题的用意：

    C01  真值表法的最小样板：前提只有一条合取式
    C02–C10  课件上的十二道，涵盖直接证法、附加前提法、归谬法、分情况证明
    C11  「肯定后件」：P→Q 与 Q 推不出 P，反例 01
    C12  「否定前件」：P→Q 与 ¬P 推不出 ¬Q，反例也是 01
    C13  把充分条件当必要条件：P→Q 推不出 Q→P
    C15  前提只说「至少一支」，推不出另一支为假
    C16  把结论当前件：P∧Q→R 与 R 推不出 P∧Q
    C14  前提自己就矛盾（P 与 ¬P）：一个反例都没有，判定为有效 ——
         有效不等于「结论对」，它是说「前提真而结论假的赋值不存在」，
         前提永远不真时这句话空洞成立（定义 1.8.2 的相容/不相容就在这里）
"""

# ── 常用写法，省得太长 ──────────────────────────────────────────

IMP_PQ = ('imp', 'P', 'Q')
IMP_QR = ('imp', 'Q', 'R')
IMP_PR = ('imp', 'P', 'R')


CASES = [
    {
        'no': 'C01',
        'premises': [('and', ('or', 'P', 'Q'), ('not', 'Q'))],
        'conclusion': 'P',
        'book': True,
        'source': '课件 1.8.2 真值表法例',
    },
    {
        'no': 'C02',
        'premises': [IMP_PQ, IMP_QR, ('not', 'R')],
        'conclusion': ('not', 'P'),
        'book': True,
        'source': '课件 1.8.3 例1（直接证法，五行）',
    },
    {
        'no': 'C03',
        'premises': [('or', 'C', 'D'), ('imp', 'C', 'R'), ('imp', 'D', 'S')],
        'conclusion': ('or', 'R', 'S'),
        'book': True,
        'source': '课件 1.8.3 例2',
    },
    {
        'no': 'C04',
        'premises': [('or', 'P', 'Q'), IMP_QR, ('imp', 'P', 'S'), ('not', 'S')],
        'conclusion': ('and', 'R', ('or', 'Q', 'P')),
        'book': True,
        'source': '课件 1.8.3 例3（结论是合取，末行合成）',
    },
    {
        'no': 'C05',
        'premises': [
            ('imp', 'P', ('or', 'Q', 'R')),
            ('imp', ('not', 'S'), ('not', 'Q')),
            ('and', 'P', ('not', 'S')),
        ],
        'conclusion': 'R',
        'book': True,
        'source': '课件 1.8.3 例4',
    },
    {
        'no': 'C06',
        'premises': [
            ('imp', 'A', ('or', 'B', 'C')),
            ('imp', 'B', ('not', 'A')),
            ('imp', 'D', ('not', 'C')),
        ],
        'conclusion': ('imp', 'A', ('not', 'D')),
        'book': True,
        'source': '课件 1.8.4 附加前提法例1',
    },
    {
        'no': 'C07',
        'premises': [('imp', 'P', ('imp', 'Q', 'R')), ('imp', 'S', 'P'), 'Q'],
        'conclusion': ('imp', 'S', 'R'),
        'book': True,
        'source': '课件 1.8.4 附加前提法例2',
    },
    {
        'no': 'C08',
        'premises': [
            ('imp', 'P', ('not', 'Q')),
            ('or', ('not', 'R'), 'Q'),
            ('and', 'R', ('not', 'S')),
        ],
        'conclusion': ('not', 'P'),
        'book': True,
        'source': '课件 1.8.4 归谬法例1',
    },
    {
        'no': 'C09',
        'premises': [
            ('imp', ('and', 'P', 'Q'), ('and', 'R', 'S')),
            ('and', ('imp', 'T', 'Q'), ('imp', 'S', 'U')),
            ('not', 'R'),
            ('and', ('imp', 'W', 'P'), ('imp', 'T', 'U')),
        ],
        'conclusion': ('imp', 'W', ('not', 'T')),
        'book': True,
        'source': '课件 1.8.4 归谬法例2（七个变元，128 个赋值）',
    },
    {
        'no': 'C10',
        'premises': [
            ('or', ('and', ('imp', 'P', 'Q'), 'P'), ('and', ('or', 'P', 'Q'), ('not', 'P'))),
        ],
        'conclusion': 'Q',
        'book': True,
        'source': '课件第 174 页 分情况证明例',
    },
    {
        'no': 'C11',
        'premises': [IMP_PQ, 'Q'],
        'conclusion': 'P',
        'book': False,
        'source': '肯定后件：无效式的样板',
    },
    {
        'no': 'C12',
        'premises': [IMP_PQ, ('not', 'P')],
        'conclusion': ('not', 'Q'),
        'book': False,
        'source': '否定前件：无效式的样板',
    },
    {
        'no': 'C13',
        'premises': [IMP_PQ],
        'conclusion': ('imp', 'Q', 'P'),
        'book': False,
        'source': '把充分条件当成必要条件',
    },
    {
        'no': 'C14',
        'premises': ['P', ('not', 'P')],
        'conclusion': 'Q',
        'book': True,
        'source': '前提不相容：反例为零，判有效（定义 1.8.2）',
    },
    {
        'no': 'C15',
        'premises': [('or', 'P', 'Q'), 'P'],
        'conclusion': ('not', 'Q'),
        'book': False,
        'source': '前提只说「至少一支」，推不出另一支为假',
    },
    {
        'no': 'C16',
        'premises': [('imp', ('and', 'P', 'Q'), 'R'), 'R'],
        'conclusion': ('and', 'P', 'Q'),
        'book': False,
        'source': '把结论当前件：P∧Q→R 与 R 推不出 P∧Q',
    },
]


def by_no(no):
    """按编号取一道题；编号写错会直接 KeyError，别指望它静默返回 None。"""
    for case in CASES:
        if case['no'] == no:
            return case
    raise KeyError('题库里没有 %s 这道题' % no)
