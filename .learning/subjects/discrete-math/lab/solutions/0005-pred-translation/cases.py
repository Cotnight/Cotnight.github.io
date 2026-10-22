"""本节的数据：四个例题式子、五道翻译题、两道换论域的题。

**一个模型**（有限论域上的一种解释）是一个字典：

    {'domain': [1, 2, 3],
     'pred': {'S': {(2,), (3,)}}}      # S 的外延：满足 S 的客体组成的 1 元组集合

论域里的客体用数字或字符串都行；谓词的外延写成元组集合，
`(2,)` 表示 1 元谓词 S 对客体 2 成立，`('甲', '丙')` 表示 2 元谓词 A 对
甲、丙这一对成立。论域外的客体不能出现在外延里——外延只写论域内的客体。

一道**翻译题**是一个字典，五道都在 `TRANSLATIONS` 里：

    {'no': 'T01', 'chinese': '……',
     'model': 那个模型,
     'expected': False,          # 课件给的真值（真= True，假= False）
     'right': 正确式, 'wrong': 错式,
     'fault': 错在哪一句话'}

一道**换论域的题**在 `DOMAINS` 里，它没有对错式，只有「同一串字在两个论域上」：

    {'no': 'D01', 'chinese': '……', 'formula': 式子,
     'domains': [{'name': '论域 {2, 3}', 'model': ...}, {…}],
     'expected': [True, False]}

本文件是数据，**不用改**。
"""


def model(domain, **preds):
    """搭一个模型：model([1, 2], S={(2,)}) 就是论域 {1,2} 上 S 只对 2 成立。"""
    return {'domain': list(domain),
            'pred': {name: set(ext) for name, ext in preds.items()}}


# ── 课件第 41 页例1 的两个式子：标辖域、数出现次数 ────────────────

# ∀x(H(x,y)→∃y(W(y)∧L(x,y,z)))：y 一处自由（H 里）两处约束（W 与 L 里）
EXAMPLE_1_1 = ('all', 'x',
               ('imp',
                ('atom', 'H', ('x', 'y')),
                ('exi', 'y',
                 ('and', ('atom', 'W', ('y',)),
                         ('atom', 'L', ('x', 'y', 'z'))))))

# ∀x(H(x)→W(y))→∃y(F(x)∧L(x,y,z))：x 前件约束、后件自由
EXAMPLE_1_2 = ('imp',
               ('all', 'x',
                ('imp', ('atom', 'H', ('x',)),
                        ('atom', 'W', ('y',)))),
               ('exi', 'y',
                ('and', ('atom', 'F', ('x',)),
                        ('atom', 'L', ('x', 'y', 'z')))))


# ── 课件第 44 页例1 的两个换名对象 ──────────────────────────────

# 第一个换名：∀x(P(x)→R(x,y))∧L(x,y)，把 ∀x 的 x 换成 t，外层 L(x,y) 不动
RENAME_PAIR = ('and',
               ('all', 'x',
                ('imp', ('atom', 'P', ('x',)),
                        ('atom', 'R', ('x', 'y')))),
               ('atom', 'L', ('x', 'y')))

# 第二个换名：∀x(H(x,y)→∃y(W(y)∧L(x,y,z)))，把内层 ∃y 的 y 换成 s
RENAME_CASE = ('all', 'x',
               ('imp',
                ('atom', 'H', ('x', 'y')),
                ('exi', 'y',
                 ('and', ('atom', 'W', ('y',)),
                         ('atom', 'L', ('x', 'y', 'z'))))))


# ── 五道翻译题：正确式与错式都在同一个模型上判 ──────────────────

TRANSLATIONS = [
    {'no': 'T01',
     'chinese': '存在小于 2 的素数（全总个体域）',
     'model': model([1, 2, 3, 4], S={(2,), (3,)}, E={(1,)}),
     'expected': False,
     'right': ('exi', 'x',
               ('and', ('atom', 'S', ('x',)), ('atom', 'E', ('x',)))),
     'wrong': ('exi', 'x',
               ('imp', ('atom', 'S', ('x',)), ('atom', 'E', ('x',)))),
     'fault': '存在量词后面接了蕴含：1 不是素数，却让整句为真'},

    {'no': 'T02',
     'chinese': '凡正数都大于零',
     'model': model([-1, 0, 1, 2], F={(1,), (2,)}, M={(1,), (2,)}),
     'expected': True,
     'right': ('all', 'x',
               ('imp', ('atom', 'F', ('x',)), ('atom', 'M', ('x',)))),
     'wrong': ('all', 'x',
               ('and', ('atom', 'F', ('x',)), ('atom', 'M', ('x',)))),
     'fault': '全称量词后面接了合取：-1 不是正数，合取链就断在这里'},

    {'no': 'T03',
     'chinese': '有些运动员不钦佩教练（课件 2.3 例2 第 2 题）',
     'model': model(['甲', '乙', '丙'],
                    L={('甲',), ('乙',)},
                    J={('乙',), ('丙',)},
                    A={('甲', '丙')}),
     'expected': True,
     'right': ('exi', 'x',
               ('and', ('atom', 'L', ('x',)),
                       ('all', 'y',
                        ('imp', ('atom', 'J', ('y',)),
                                ('not', ('atom', 'A', ('x', 'y'))))))),
     'wrong': ('exi', 'x',
               ('and', ('atom', 'L', ('x',)),
                       ('all', 'y',
                        ('and', ('atom', 'J', ('y',)),
                                ('not', ('atom', 'A', ('x', 'y'))))))),
     'fault': '内层全称接了合取：甲不是教练，合取链就断在这里'},

    {'no': 'T04',
     'chinese': '只有有借书证的人，才把书借走',
     'model': model(['张三', '李四', '王五'],
                    P={('张三',), ('李四',)},
                    Q={('张三',)}),
     'expected': True,
     'right': ('all', 'x',
               ('imp', ('atom', 'Q', ('x',)), ('atom', 'P', ('x',)))),
     'wrong': ('all', 'x',
               ('imp', ('atom', 'P', ('x',)), ('atom', 'Q', ('x',)))),
     'fault': '只有 P 才 Q 的方向反了：条件该写进后件'},

    {'no': 'T05',
     'chinese': '除了数学书，桌上的书都是教材',
     'model': model(['甲', '乙', '丙'],
                    T={('甲',), ('乙',)},
                    M={('甲',)},
                    J={('乙',)}),
     'expected': True,
     'right': ('all', 'x',
               ('imp',
                ('and', ('atom', 'T', ('x',)),
                        ('not', ('atom', 'M', ('x',)))),
                ('atom', 'J', ('x',)))),
     'wrong': ('all', 'x',
               ('imp', ('atom', 'T', ('x',)), ('atom', 'J', ('x',)))),
     'fault': '例外没排除：数学书也得是教材，这道模型里它不是'},
]


# ── 两道换论域的题：同一串字，两个论域 ──────────────────────────

DOMAINS = [
    {'no': 'D01',
     'chinese': '论域里的数都大于 1',
     'formula': ('all', 'x', ('atom', 'G', ('x',))),
     'domains': [
         {'name': '论域 {2, 3}', 'model': model([2, 3], G={(2,), (3,)})},
         {'name': '论域 {1, 2, 3}', 'model': model([1, 2, 3], G={(2,), (3,)})},
     ],
     'expected': [True, False]},

    {'no': 'D02',
     'chinese': '凡素数都是奇数',
     'formula': ('all', 'x',
                 ('imp', ('atom', 'S', ('x',)), ('atom', 'O', ('x',)))),
     'domains': [
         {'name': '论域 {2, 3, 5, 7}',
          'model': model([2, 3, 5, 7],
                         S={(2,), (3,), (5,), (7,)},
                         O={(3,), (5,), (7,)})},
         {'name': '论域 {3, 5, 7}',
          'model': model([3, 5, 7],
                         S={(3,), (5,), (7,)},
                         O={(3,), (5,), (7,)})},
     ],
     'expected': [False, True]},
]


def by_no(no):
    """按编号取一道翻译题。"""
    for case in TRANSLATIONS:
        if case['no'] == no:
            return case
    raise KeyError(no)


def by_domain(no):
    """按编号取一道换论域的题。"""
    for entry in DOMAINS:
        if entry['no'] == no:
            return entry
    raise KeyError(no)
