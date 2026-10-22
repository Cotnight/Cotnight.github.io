# 0002 · 推理证明校对 —— 参考解

## 怎么用

两种都行：

1. 只看对应处：`proof.py` 对照你自己填的那 6 个函数（`parse_basis`、`is_step`、`line_issues`、
   `is_contradiction`、`ending_issues`、`check_proof`），以及末尾那份 `MY_PROOF`。
2. 整份跑起来（自包含）：

```sh
python -m unittest -v test_proof
```

四个文件都在这一个目录里，直接跑就全绿 —— 不需要回头找任务目录。

## 它做了哪四件事

| 任务 | 落在哪个函数 | 关键点一句话 |
| --- | --- | --- |
| 1 · 依据栏 | `parse_basis` | 先切逗号，再看第一段是 `P` 还是 `T`；数字进行号，`CP` 单独成类；认不出返回 `None` |
| 2 · 七条蕴含式 | `is_step` | 只判形状、不看行号；`refs` 顺序无关，按「在不在里面」判 |
| 3 · 逐行体检 | `line_issues` | 每行只报一条，顺序是「形状 → 行号 → 规则」；查表时行号减一 |
| 4 · 收口 | `is_contradiction`、`ending_issues`、`check_proof` | 先扫「结论当前提」，再按直接证法 / CP / 归谬四条路分头核末行 |
| 5 · 自己那份 | `MY_PROOF` | 课件 1.8.3 例4 的八行，`check_proof` 交回空清单 |

`MY_PROOF` 用的是「先拆合取、再假言推理、最后析取三段论」这条链：

```text
1  (P∧¬S)            P
2  P                 T，1，化简
3  ¬S                T，1，化简
4  P→(Q∨R)           P
5  Q∨R               T，2，4，假言推理
6  ¬S→¬Q             P
7  ¬Q                T，3，6，假言推理
8  R                 T，5，7，析取三段论
```

## 六处错法：标本给什么、断言报什么

`proof_broken.py` 是错法标本，**不要修**（`TestBroken` 断言的正是它的错处）。

| 标本 | 标本那一处 | 断言报的那一句 |
| --- | --- | --- |
| `S1_NO_NUMBERS` | 第 4 行依据栏 `T，拒取式` | `第 4 行：依据栏「T，拒取式」没写行号——T 行要写清引了哪几行` |
| `S2_CP_NOT_RESTORED` | 末行停在 `R` | `第 2 行引入了附加前提 S，末行却停在 R——CP 证完要把末行写成 S→… 并标 CP` |
| `S3_WRONG_ASSUMPTION` | 第 1 行写 `¬P` | 两句：第 3 行推不出 `¬Q`；第 1 行假设应当是 `P` |
| `S4_NO_CLOSING` | `closing` 是空串 | `末行写的是矛盾，但缺一句「按归谬法」的结论句` |
| `S5_GOAL_AS_PREMISE` | 第 4 行把结论当 `P` 行 | `第 4 行：把结论整行当成了前提——这一行一写就是循环论证` |
| `S6_INCOMPLETE` | 末行停在 `¬Q` | `末行是 ¬Q，不是结论 ¬P` |

`S3` 报两句不是副作用：附加前提写错之后，第 3 行的假言推理就没了前件，
于是一路塌下去。答卷上的样子正是「假设错，整串错」。

## 自验时要看到的

- `python -m unittest -v test_proof` 共 30 条测试全过：
  `TestBasis` 3 条、`TestStep` 2 条、`TestLines` 7 条、`TestEnding` 9 条、
  `TestBroken` 6 条、`TestWholeProof` 3 条。
- 想在终端里直接看一份报告，可以临时加两行：

```python
import proofs, proof as pr
print(pr.check_proof(proofs.PROOF_B))
```

应当打出 `[]`：`PROOF_B` 是 CP 那份，八行、末行还原；把 `lines` 的最后一项去掉再看，
才会打出 S2 那一句。

> 本次交付时本机 shell 不可用（`pwsh` 以 0xC0000142 退出），
> 上面这些命令与输出**没有实际执行过**，期望值按代码与课件答案手算。
> 第一次跑以断言为准；若与这里写的数不一致，先信断言、再回头查这一份说明。
