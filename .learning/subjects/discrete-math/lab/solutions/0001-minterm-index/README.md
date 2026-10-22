# 0001 · 范式机 —— 参考解

## 怎么用

两种都行：

1. 只看对应处：`normal_form.py` 对照你自己填的 7 个函数（`truth_vector`、`minterms`、
   `maxterms`、`expand_term`、`dual`、`to_nnf`、`same_function`）。
2. 整份跑起来（自包含）：

```sh
python -m unittest -v test_normal_form
```

四个文件都在这一个目录里，直接跑就全绿 —— 不需要回头找任务目录。

## 它做了哪四件事

| 任务 | 落在哪个函数 | 关键点一句话 |
| --- | --- | --- |
| 1 · 真值列与两组编号 | `truth_vector`、`minterms`、`maxterms` | 第 i 行就是 `assignments` 的第 i 项；1 的行写 m、0 的行写 M，两组合起来正好占满 0～7 |
| 2 · 缺变元补成小项 | `expand_term` | 枚举 0～2^n-1，满足 term 里每条约束的都算；缺 k 个变元自然落 2^k 格 |
| 3 · 对偶式 | `dual` | ∧↔∨、↑↔↓、1↔0 三组一起换，变元与否定号不动 |
| 4 · 否号内移与判等值 | `to_nnf`、`same_function` | 否号穿进括号时 ∧ 与 ∨ 互换；判等值先定同一个 n，再逐行比 |

## 三处错法：标本给什么、正确给什么

`normal_form_broken.py` 是错法标本，**不要修**（`TestBroken` 断言的正是它的错值）。

| 错法 | 标本那一行 | 它给出的结果 | 正确结果 |
| --- | --- | --- | --- |
| 缺变元按 0 补齐 | `expand_term` 里 `term.get(v, 0)` | `Q∧R` 只落 m3；三支并起来 Σm(0,1,3) | 落 m3、m7；Σm(0,1,3,7) |
| 否号进括号没换运算 | `_nnf` 末尾 `return (tag, …)` | ¬(P∨Q) 化成 ¬P∨¬Q，P=1、Q=0 上算出 1 | ¬P∧¬Q，同一行算出 0 |
| 只换 ∧↔∨ | `dual` 只处理 `and`/`or` | `(P∧Q)↑R` 的对偶写成 (P∨Q)↑R | (P∨Q)↓R |

第三条还有一层：错的这一份**能通过**「取两次对偶回到原式」这条自查（`test_double_dual_hides_error`
钉的就是这件事）。所以对偶的可靠验法是折成 ¬、∧、∨ 再取对偶，两条路结果必须一致。

修正记录：`test_three_groups` 原来的用例把 ↓ 的对偶写成了 `P∧Q`（输入 `('nor','P','Q')`），
这是错的 —— ↓ 是 ¬(P∨Q)、↑ 是 ¬(P∧Q)，对偶只换联结词、否定号不动，所以 P↓Q 的对偶是 **`P↑Q`**；
该用例的 `expect` 已改成 `'P↑Q'`。另外常量 `('T',)`/`('F',)` 以前会被 `_operand_text` 套上括号
（`(P∨Q)∨(0)`），现在和变元、`¬` 一样裸露（`(P∨Q)∨0`）。

## 自验时要看到的

- `python -m unittest -v test_normal_form` 共 26 条测试全过：
  `TestTable` 4 条、`TestExpand` 4 条、`TestDual` 5 条、`TestNNF` 4 条、`TestSame` 5 条、
  `TestBroken` 4 条。
- 想在终端里直接看一组编号，可以临时加三行：

```python
import normal_form as nf
f = ('and', ('imp', 'P', 'Q'), ('imp', 'Q', 'R'))
print(nf.truth_vector(f, 3), nf.sigma_text(nf.minterms(f, 3)), nf.pi_text(nf.maxterms(f, 3)))
```

应当打出 `11010001 Σm(0,1,3,7) ΠM(2,4,5,6)`：八行里四个 1，编号 0、1、3、7。

> 本次交付时本机 shell 不可用，上面这些命令与输出**没有实际执行过**（按代码推得）。
> 第一次跑以断言为准；若与这里写的数不一致，先信断言、再回头查这一份说明。
