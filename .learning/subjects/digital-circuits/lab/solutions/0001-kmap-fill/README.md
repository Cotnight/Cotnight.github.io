# 0001 · 卡诺图填图 —— 参考解

## 怎么用

两种都行：

1. 只看对应处：`kmap.py` 对照你自己的 4 个函数；`kmap_broken.py` 对照你改的那两行。
2. 整份跑起来（自包含）：

```sh
python -m unittest -v test_kmap
```

三个文件都在这一个目录里，直接跑就是绿的全绿 —— 不需要回头找任务目录。

## 它做了哪三件事

| 任务 | 落在哪个函数 | 关键点一句话 |
| --- | --- | --- |
| 1 · 真值表填三变量图 | `cell_of`、`fill_from_table`、`minterms_from_grid` | 编号写成取值串，按行轴、列轴切两段标号，下标到 `gray_axis` 里查 |
| 2 · 缺变量的项落多格 | `cells_of_product`、`fill_from_products` | 缺 k 个变量就落 $2^k$ 格；枚举全部编号、满足 term 的都算，重叠只留一个 1 |
| 3 · 坏图修回来 | `kmap_broken.py` | 两处：轴的标号 `'00','01','10','11'` 改回 `'00','01','11','10'`；`return found[:1]` 改成 `return found` |

## 任务 3 的两处错，为什么只改一处不够

- 只改标号：`cell_of` 对了，但缺变量的项还只落一格，`test_no_missing_cells` 照旧红。
- 只改 `[:1]`：缺变量的项落满 4 格，但落的是二进制序图上的格，`test_cells_match_good` 在
  m2、m3、m6、m7、m10、m11、m14、m15 这些编号上照旧红 ——
  这些编号的列标是 `10` 或 `11`，而格雷序与二进制序正好在这两格上换了位置。

两条各自独立，断言也各管一条，红的那条直接指出是哪种错。

## 自验时要看到的

- `python -m unittest -v test_kmap` 共 9 条测试全过（`TestCellOf` 2 条、`TestFillFromTable` 2 条、
  `TestProductTerms` 2 条、`TestBroken` 3 条）。
- 想在终端里直接看一张图，可以临时加三行：

```python
import kmap
for line in kmap.fill_from_table(3, (0, 0, 0, 0, 0, 0, 1, 1)):
    print(line)
```

应当打出 `[0, 0, 0, 0]` 与 `[0, 0, 1, 1]`：1 在 m7、m6 两格，也就是第 2 行最后两列。

> 本次交付时本机 shell 不可用，上面这些命令与输出**没有实际执行过**（按代码推得）。
> 第一次跑以断言为准；若与这里写的数不一致，先信断言、再回头查这一份说明。
