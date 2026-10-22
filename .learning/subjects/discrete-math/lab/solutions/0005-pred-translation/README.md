# 0005 · 谓词翻译与换名 —— 参考解

## 怎么用

两种都行：

1. 只看对应处：`scope.py` 里填好的 7 个函数（`free_variables`、`free_occurrences`、
   `bound_occurrences`、`rename_bound`、`evaluate`、`domain_report`、`audit`），
   另有四个私有辅助函数（`_free_names`、`_count`、`_binds`、`_rename`）。
2. 整份跑起来（自包含）：

```sh
python -m unittest -v test_scope
```

这个目录里的六份文件是齐的：`formula.py`、`cases.py`、`scope.py`、`broken.py`、
`test_scope.py`、本说明。把它们单独拷进一个空目录也照样跑得通，不必回头找任务目录。

## 它做了哪七件事

| 任务 | 落在哪个函数 | 关键点一句话 |
| --- | --- | --- |
| 1 · 自由变元 | `free_variables` | 递归带一层「正被哪几个名字约束」；量词管的是别的字母时，那个变元照样自由 |
| 1 · 出现次数 | `free_occurrences` / `bound_occurrences` | 同一趟递归数两样；同一字母可以既约束又自由，两种次数各数各的 |
| 2 · 换名 | `rename_bound` | 只有「是 `old` 且 `old` 正在被约束」的出现才换——判据少一半就是 `broken.py` 那个错法 |
| 2 · 新名查验 | `rename_bound` 前半 | 与公式里已有的变元撞名报 `ValueError`；没有 `old` 的指导变元也报（那属于代入） |
| 3 · 求值 | `evaluate` | 原子查外延，量词把 `model['domain']` 走一遍；蕴含只有「前真后假」为假 |
| 4 · 换论域 | `domain_report` | 每行拿那一行自己的模型**重算**，不缓存、不抄第一行 |
| 5 · 对账 | `audit` | 一行四格：正确式真值、错式真值、课件真值；`misses` 挑出错式没被抓住的题号 |

## 五道翻译题：正确式都等于课件真值，错式都被模型抓住

`python -m unittest -v test_scope.TestTranslations` 会逐题验这张表：

| 编号 | 中文 | 正确式真值 | 错式真值 | 课件真值 | 错法 |
| --- | --- | --- | --- | --- | --- |
| `T01` | 存在小于 2 的素数 | 假 | 真 | 假 | 存在接蕴含：1 不是素数，前件假、蕴含真 |
| `T02` | 凡正数都大于零 | 真 | 假 | 真 | 全称接合取：−1 不是正数，合取链断在这里 |
| `T03` | 有些运动员不钦佩教练 | 真 | 假 | 真 | 内层全称接合取：甲不是教练 |
| `T04` | 只有有借书证的人才把书借走 | 真 | 假 | 真 | 方向反了：条件该写进后件 |
| `T05` | 除了数学书，桌上的书都是教材 | 真 | 假 | 真 | 例外没排除：数学书也得是教材 |

「正确式真值 = 课件真值」是这一节的要求：模型只是课件那句话的一个有限样本，
样本上判错，说明式子的意思就不对。

## 三处薄弱点各有可断言的反例

`broken.py` 的三处错法不是「待修的 bug」，是标本；`TestBroken` 把每处都钉在一条断言上：

| 薄弱点 | 错法函数 | 断言钉住的东西 |
| --- | --- | --- |
| 换名动到辖域外的自由变元 | `rename_touches_free` | 自由变元集合从 `['y', 'z']` 变成 `['s', 'z']`；`H(x,y)` 里的 `y` 被改成了 `s` |
| 特性谓词接错边（全称） | `wired('all', …)` | 正确式 `∀x(F→M)` 真，错式 `∀x(F∧M)` 被 `-1` 拉成假 |
| 特性谓词接错边（存在） | `wired('exi', …)` | 正确式 `∃x(S∧E)` 假，错式 `∃x(S→E)` 被 `1` 白送成真 |
| 换论域不重判真值 | `sticky_truth` | `D01` 两行都抄成 `[True, True]`，正确答案是 `[True, False]` |

第一条最值得看：它改的不是真值，是**自由变元集合**。换名规则第 1 条写着「公式的其余部分不变」，
辖域外那个 `x` 一动，同一个式子的自变量就换了名字，此后按原式做的代入与求值全部错位；
顺带还造出了「`t` 一处自由一处约束」——正是 2.4.2 想消掉的混淆。

## 自验时要看到的

- `python -m unittest -v test_scope` 共 23 条全过：
  `TestScope` 3 条、`TestRename` 4 条、`TestEvaluate` 5 条、`TestDomains` 2 条、
  `TestTranslations` 4 条、`TestBroken` 5 条。
- 留白态（`scope.py` 未填）应当是 23 条**全红**，消息都是 `NotImplementedError: 任务 …`。
  连几条 `assertRaises(ValueError)` 也红：留白时抛的是 `NotImplementedError`，不是 `ValueError`。
  `TestBroken` 那五条一样红——它们要先借你的 `evaluate` 才验得出错法的真值。
- `cases.py` 与 `broken.py` 在任务目录和解目录里逐字相同；只有 `scope.py` 不同（留白 vs 填好）。
- 想手验一条对账：`audit([cases.by_no('T01')])` 应当打出 `[('T01', False, True, False)]`。

## 一处如实交代

本次交付时这台机器的 shell 不可用（`pwsh` 以 0xC0000142 退出），所以上面这些命令与输出
**没有在本机实际执行过**，期望值是按代码与课件真值逐格手算的。第一次跑以断言为准；
若与本说明里的数不一致，先信断言、再回头查这一份说明（或 `cases.py` 里的模型）。
