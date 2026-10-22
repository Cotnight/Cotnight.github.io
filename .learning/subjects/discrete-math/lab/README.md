# 实验与上手练习

这里是离散数学这门课的所有 lab。一节 lab 一个子目录，参考解放在 `solutions/` 下的同名子目录里。
第 1 课（对偶与范式）落了一节：把公式变成编号表的那台小机器。
第 2 课（推理理论）接着落第二节：把「行号、公式、依据」三列的证明表交给断言逐行核。
实验一再落第三节：把真值表引擎写出来，让整批推理一次判完，并与纸上那几道对账。
第 5 课（谓词公式翻译与换名）落第四节：把辖域、自由／约束变元、换名与三条翻译错法做成可跑的核对。

## 载体与环境

- Python 3.13，只用标准库 `unittest`（实验一另外用到 `itertools`）。
- 不装任何第三方包，不要编译工具链，不联网，没有依赖描述文件要装。
- 断言一律用 `assertEqual` 加 `subTest`：一次报出哪几个编号不对，而不是只报第一条。
  需要比同一组结论的两个写法时，用 `assertIn` 加一组可接受的等价写法（例如 `¬P∧¬Q` 与 `¬Q∧¬P`）。
- 不画图：小项、大项、真值表都用等宽表格写，肉眼能对，断言也能逐条报出来；
  推理证明同理，三列表照答卷写。
- 本机解释器：`D:/Program Files/Python313/python.exe`
  （PowerShell 里 `py -3` 一般也指向它；以能跑起来的那一个为准。）

## 怎么跑

在某一节 lab 的目录里跑它自己的测试文件：

```sh
cd lab/0001-minterm-index
python -m unittest -v test_normal_form
```

```sh
cd lab/0002-proof-check
python -m unittest -v test_proof
```

```sh
cd lab/0003-truth-engine
python -m unittest -v test_engine
```

```sh
cd lab/0005-pred-translation
python -m unittest -v test_scope
```

三节的测试文件名不同（`test_normal_form.py`、`test_proof.py`、`test_engine.py`），所以要看目录里的
实际文件名；`python -m unittest -v` 不带参数时也会自动发现当前目录下的 `test_*.py`。
0005 那节的测试文件叫 `test_scope.py`，规矩一样：先看目录里的实际文件名。

只跑某一步：

```sh
python -m unittest -v test_normal_form.TestTable
python -m unittest -v test_proof.TestStep
python -m unittest -v test_engine.TestValidity
python -m unittest -v test_scope.TestRename
```

`subTest` 会把失败的那一项单独列出来，例如 `formula='(P→Q)∧(Q→R)'`、`term={'Q': 1, 'R': 1}`，
`proof='S2_CP_NOT_RESTORED'`，或 `编号='C11'` —— 那就是这个式子（这一份证明／这道题）没对上。
0005 那节的 `subTest` 标签是 `公式='∀x(H(x,y)→∃y(W(y)∧L(x,y,z)))'`、`变元='y'`、`编号='T01'`、
`中文='……'`：红在哪一行，就回去查那一条公式／那个变元／那道题。

实验一还有两个不用断言的入口，跑完测试可以直接看结果：

```sh
cd lab/0003-truth-engine
python report.py      # 16 行「编号｜判定｜依据｜出处」：每一判都带反例或「反例 0 / 2^n」
python audit.py       # 两轮对账：引擎 vs 课件答案、引擎 vs 你纸上写的
```

0005 没有额外的报告脚本：那张对账表就是 `scope.audit(...)` 的返回值。
想看就手敲一行：

```sh
cd lab/0005-pred-translation
python -c "import cases, scope; [print(row) for row in scope.audit(cases.TRANSLATIONS)]"
```

## 任务表

| 编号 | 目录 | 这一节要做出什么 | 判它过的东西 |
| --- | --- | --- | --- |
| 0001 | [0001-minterm-index](0001-minterm-index/范式练习.md) | 7 个留白函数写完：真值列、Σm/ΠM、缺变元补小项、对偶式、否号内移、判等值；并认出三处错法 | `test_normal_form.py` 的 26 条测试 |
| 0002 | [0002-proof-check](0002-proof-check/推理证明校对.md) | 6 个留白函数写完：依据栏拆三段、七条蕴含式配形状、逐行体检行号与依据、CP 还原与归谬矛盾；再把课件 1.8.3 例4 的证明录成数据 | `test_proof.py` 的 30 条测试 |
| 0003 | [0003-truth-engine](0003-truth-engine/真值表引擎.md) | **实验一**：7 个留白函数写完，真值表引擎能把题库 16 道推理逐题判出有效/无效并打印依据；再把 16 道在纸上判一遍填进 `MY_ANSWERS`，两轮对账 0 道差异 | `test_engine.py` 的 21 条测试；`python report.py` 与 `python audit.py` 的输出 |
| 0005 | [0005-pred-translation](0005-pred-translation/谓词翻译与换名.md) | 7 个留白函数写完：一条公式报出自由／约束变元与各自出现次数、换名只动辖域里的变元、有限模型上求值、同一式子按两个论域分别重判；再把五道翻译题的正确式与错式逐题对账，三个错法标本各被一个模型钉住 | `test_scope.py` 的 23 条测试（含 `TestBroken` 5 条） |

## 卡壳顺序

0001（范式机）：

1. 先读断言报的那一组：`subTest` 里的式子名或 `term={...}` 就是出错的那个式子和那一支，
   把它的编号按取值重新拼一遍（`bits(i, 3)`），回表里找一眼。
2. 还连不上就查两处：Σm 与 ΠM 是不是互补（合起来 8 个编号）；缺变元的支是不是落满了 2^k 格。

0002（推理证明校对）：

1. 先看报的是第几行、哪一句：`第 4 行：依据栏「…」没写行号` 是**格式**问题，
   `第 4 行：第 2、3 行按「拒取式」推不出 ¬Q` 是**推导**问题，两类修法不同。
2. 格式问题回去数依据栏：引了哪几行、按哪条规则，两样都要写；推导问题回去看那两行的形状，
   本节的七条蕴含式只整行引用，不能改公式内部。

0003（真值表引擎）：

1. 先看红在哪个类：`TestValuations`／`TestEvaluate` 红，说明赋值或求值这一步就没过，
   后面几类会跟着一起红——先把最前面的类修绿，别急着看后面的报错。
2. 再看差的是整组还是几行：`TestBank` 一次报四五道题，通常是 `counterexamples` 漏了
   「前提全真」那个条件（漏了它，每题都「无效」）；只错一两道且都集中在无效式上，
   通常是蕴含算错（用了 `min`／`max`）。
3. `TestMyAnswers` 红而对账只差一两道：先跑 `python report.py` 看那道题的反例是哪个赋值，
   把那个赋值逐行代进前提验一遍——若反例成立，你纸上那份「证明」必定在某一行用了结论。

0005（谓词翻译与换名）：

1. 按类的顺序修，别跳：`TestScope` → `TestRename` → `TestEvaluate` → `TestDomains`
   → `TestTranslations` → `TestBroken`。`TestBroken` 那五条要靠你的 `evaluate` 才验得出来，
   它红的时候先回头确认 `TestEvaluate` 是绿的。
2. `TestScope` 红在 `变元='y'`、而公式里有 `∃y`：先问自己「`H(x,y)` 里那个 `y` 在 `∃y` 的括号里吗」。
   递归时没把「正被哪几个名字约束」带下去，是这一处的唯一根因。
3. `TestRename` 红成 `H(x,s)` 或 `L(t,y)`：你换了辖域外的出现。判据少了一半——
   要同时满足「它是 `old`」与「`old` 正在被约束」两个条件才换。
4. `TestDomains` 红成两行同一个真值：`domain_report` 里把第一行的结果套给后面几行了，
   每一行都该拿那一行自己的 `model` 重算。
5. `TestTranslations` 的 `test_wrong_formula_is_caught` 红：不是错式错了，是你的 `evaluate` 把某条式子
   算成了与课件真值一样——回去看那道题的模型里哪个客体该把错式打掉。

## 文件分工

- 任务目录 `0001-minterm-index/`：
  `normal_form.py`（7 个函数留白，你来填）、
  `normal_form_broken.py`（三处错法的标本，**不要修**）、
  `test_normal_form.py`（断言，别改）、
  `范式练习.md`（分步任务书，末尾留「我的三条」给你写）。
- 任务目录 `0002-proof-check/`：
  `proof.py`（6 个函数留白 + 末尾 `MY_PROOF` 等你填）、
  `proofs.py`（四份正确的示范证明，只读）、
  `proof_broken.py`（六份错法标本，**不要修**）、
  `test_proof.py`（断言，别改）、
  `推理证明校对.md`（分步任务书，末尾留「我的三条」给你写）。
- 任务目录 `0003-truth-engine/`：
  `engine.py`（7 个函数留白，你来填；`formula_text`、`variables_of`、`truth_values`、`maxterms`、
  `entailment_formula`、`format_env` 已经写好，不用改）、
  `cases.py`（题库 16 道 + 课件答案，只读）、
  `audit.py`（末尾 `MY_ANSWERS` 等你填，填完跑它看对账）、
  `report.py`（整批报告，已写好，不用改）、
  `test_engine.py`（断言，别改）、
  `真值表引擎.md`（分步任务书，末尾留「我的三条」给你写）。
- 任务目录 `0005-pred-translation/`：
  `scope.py`（7 个函数留白，你来填；`misses` 已写好，不用改）、
  `formula.py`（公式的打印工具 `formula_text`、`variables`，已写好，不用改）、
  `cases.py`（四个例题式子 + 五道翻译题 + 两道换论域的题 + `model`／`by_no`／`by_domain`，只读）、
  `broken.py`（三处错法标本：换名动到自由变元、特性谓词接错边、换论域不重判，**不要修**）、
  `test_scope.py`（断言，别改）、
  `谓词翻译与换名.md`（分步任务书，末尾留「我的三条」给你写）。
- `solutions/0001-minterm-index/`：同一套文件的成品 + 一份说明。**做完再看**。
- `solutions/0002-proof-check/`：同一套文件的成品 + 一份说明。**做完再看**。
- `solutions/0003-truth-engine/`：同一套文件的成品（含填满的 `MY_ANSWERS`）+ 一份说明。**做完再看**。
- `solutions/0005-pred-translation/`：同一套文件的成品（`scope.py` 填好，其余五份与任务目录逐字相同）+ 一份说明。**做完再看**。
- 参考解是自包含的：把 `solutions/0001-minterm-index/`、`solutions/0002-proof-check/` 或
  `solutions/0003-truth-engine/` 里那几个文件单独放进一个空目录，也能直接
  `python -m unittest -v <测试文件名>` 跑通，不必回头找任务目录。
- 0005 同理：`solutions/0005-pred-translation/` 的六份文件单独放进一个空目录，
  `python -m unittest -v test_scope` 照样跑通；它不依赖前几节的任何文件。
- 三节共用一套公式写法（`'P'`、`('not','P')`、`('and','P','Q')`、`('or','P','Q')`、`('imp','P','Q')`）：
  0001 把公式变成编号表，0002 把公式排成证明的行，0003 拿同一套写法穷举赋值判有效性。
  0001 与 0003 的编号规则是同一个：变元按字母顺序排，第一个变元占最高位，真记 1。
- 0005 还是同一族嵌套元组，只多了量词与谓词两项：`('atom','S',('x',))`、`('all','x',body)`、
  `('exi','x',body)`。公式没有「辖域」字段——辖域是读出来的，量词后面那一对括号里的整段就是它管的地方。

## 后面的实验

`0003` 这套「编号 → 断言 → 对账表」的写法不是用完就算：实验二的关系矩阵、实验三的等价类与拓扑序、
实验四的最短路手算表、实验五的最小生成树，输入校验与对账表都照它写。
同一套三段式（`cases.py` 放题／`xxx.py` 留白／`test_xxx.py` 断言）会在后面四节里反复出现。

`0005` 补的是这套写法的另一半：**模型**（论域 + 各谓词的外延）。实验二写关系矩阵时要判自反、对称，
判据就是一句带量词的公式——把公式喂给 0005 的 `evaluate`，在有限论域上就能一眼判出它成不成立。

## 一处如实交代

这三节 lab 交付时这台机器的 shell 不可用（`pwsh` 直接以 0xC0000142 退出），
所以这些断言**没有在本机实际跑过**，任务书与说明里的期望值是按代码手算的。
你第一次跑出来的红/绿以断言本身为准；若与任务书里写的数不一致，先信断言。

0005 这一节同样是手算的期望值（五道翻译题的真值逐格对过课件 2.3 的答案），
本机没有跑过 `test_scope.py`；留白态应当 23 条全红，参考解应当 23 条全绿。
