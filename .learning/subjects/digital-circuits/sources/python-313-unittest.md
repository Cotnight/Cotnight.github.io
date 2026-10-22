# Python 3.13 官方文档 · `unittest` —— 抓取节选

> 原址：https://docs.python.org/3.13/library/unittest.html
> 抓取日期：2026-10-19，页面标题显示版本 **Python 3.13.16**（来源：python.org 官方文档，随 3.13 补丁版更新）。
> 用途：**本科目实验课（Python 仿真）用断言校验波形与真值表时，核对 API 怎么写、哪些行为在某版本改过**。只给讲解与 lab 设计对齐用，不挂科目主页。
> 说明：本文是抓取后的节选（页面后半段被截断，`assert*` 方法全表在原址 `#assert-methods` 一节），**不要把它当完整文档**。

## 1. 基本用法（官方示例，逐字）

```python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```

要点（官方原话归纳）：

- 测试方法名必须以 `test` 开头，运行器靠这个命名约定识别测试。
- 三个核心断言：`assertEqual()` 查结果相等，`assertTrue()` / `assertFalse()` 查条件，`assertRaises()` 查是否抛特定异常。
- **官方明确推荐用这些方法而不是裸 `assert` 语句**：这样运行器能累积全部结果并生成报告（对“一次跑完 20 条待测波形，看哪几条错”正是要的）。
- `setUp()` / `tearDown()` 在每个测试方法前后各跑一次；`setUp()` 抛异常则该测试记为 error 且不执行测试体。
- `unittest.main()` 提供命令行入口；`-v` 提高详细度。

## 2. 分组与子测试（对“真值表逐行比对”最有用）

- `TestCase.subTest(msg=None, **params)`：上下文管理器，把循环里每一次迭代当成独立子测试，**失败时把参数值打在输出里**，且**不会在第一次失败就停**。官方示例：

```python
class NumbersTest(unittest.TestCase):
    def test_even(self):
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
```

输出会把 `FAIL: test_even (...)(i=1)`、`(i=3)`、`(i=5)` 三条分别列出；不用 subTest 的话第一条失败就中止，且看不出是哪个 `i`。

- `setUpClass()` / `tearDownClass()`（3.2 起）：类级夹具，需 `@classmethod` 装饰。
- 跳过与预期失败：`@unittest.skip(reason)`、`@unittest.skipIf(condition, reason)`、`@unittest.skipUnless(condition, reason)`、`@unittest.expectedFailure`、`TestCase.skipTest(reason)`、异常 `unittest.SkipTest`。
- 复用旧测试函数：`unittest.FunctionTestCase(testFunc, setUp=..., tearDown=...)`。

## 3. 命令行（lab 里跑脚本用）

```
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method
python -m unittest tests/test_something.py
python -m unittest -v test_module
python -m unittest            # 等价于 python -m unittest discover
```

选项（含版本标注，**这就是“易变”部分**）：

| 选项 | 作用 | 版本 |
|---|---|---|
| `-b/--buffer` | 通过时丢弃 stdout/stderr | 3.2 |
| `-c/--catch` | Ctrl-C 等当前用例结束并汇报已有结果 | 3.2 |
| `-f/--failfast` | 首次错误/失败即停 | 3.2 |
| `-k` | 按名字/通配符筛选测试（可多次） | 3.7 |
| `--locals` | 回溯里显示局部变量 | 3.5 |
| `--durations N` | 显示最慢的 N 个用例（0 = 全部） | 3.12 |

## 4. 版本变迁（核对点，来自本页 “Changed in version” 标注）

- **3.12**：新增 `--durations`。
- **3.11**：测试方法返回值（非 `None`）的行为**被弃用**——所以 lab 里的 `test_*` 方法不要 `return` 结果，用断言表达结论。
- **3.11**：`unittest` **移除了 namespace package 支持**（测试起始目录及其子目录必须是带 `__init__.py` 的常规包）。这条只在用 `discover` 且按包名指定目录时才会踩到。
- **3.4**：`subTest` 加入；`discover` 支持 namespace package 起始目录（后被 3.11 撤销）。
- **3.2**：`TestCase` 可以不传 `methodName` 实例化；`-b/-c/-f`、`setUpClass/tearDownClass`、`discover` 加入。

## 5. 抓取留白

- `assert*` 方法全表（`assertAlmostEqual`、`assertIn`、`assertCountEqual` 等）与原址后段内容**未抓全**：页面超出抓取上限被截断。需要时直接看原址 `#assert-methods`。
- 本文未包含 `unittest.mock`（另一页 `unittest.mock.html`），本科目不涉及。
