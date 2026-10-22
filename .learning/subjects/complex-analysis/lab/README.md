# lab · 复变计算工具（0002 CR 检查器）

这是「可导与解析的判定」这一课的小 lab。载体是**源码 + 测试**：你手写实现几个
复变计算函数，用断言把结果和纸面上算出来的值对照。

工具要做的事只有一句：**给一个函数 $f$，在复平面上取几个点，用数值差分检验柯西-黎曼条件。**

课上那张「条件成立的点集决定结论」的表格（$z^2$ 处处成立、$|z|^2$ 只有原点、$\bar z$ 一个也没有）
在这个 lab 里会变成一段能跑的程序——判完一批点，它自己说出 `all` / `some` / `none`。
实验二（解析函数长什么样）会把这套逐点检验搬到图上，所以这一课的代码后面还要用。

---

## 目录与依赖

```
lab/
├── README.md                       ← 本文件：任务表 + 卡壳顺序
├── 0002-cr-check-tool/
│   ├── cr_tool.py                  ← 你要填的 8 个函数（留白）
│   └── test_cr_tool.py             ← 断言，自动判分
└── solutions/
    └── 0002-cr-check-tool/
        ├── cr_tool.py              ← 参考解（做完才看）
        └── README.md               ← 参考解的九步要点与常见错法
```

**环境依赖：只要 Python 3.8+，只用标准库（`cmath`、`unittest`），不装任何第三方包。**
没有 `requirements.txt`，也不需要 numpy：

- 复数用内置类型 `complex`，`1j` 就是虚数单位；
- 极坐标用 `cmath.exp(1j*theta)`，不需要 `math` 以外的库；
- 测试用内置 `unittest`，`python test_cr_tool.py` 直接跑。

本机实测环境是 Python 3.13.15（`python --version` 可查）。命令里的 `python`
如果你的机器上没有，换成 `py` 或 `python3` 即可。

---

## 怎么算做完

进到任务目录，跑：

```term
$ cd lab/0002-cr-check-tool
$ python test_cr_tool.py
```

现在（还没动手）会是这样——22 个 ERROR，**退出码 1**：

```term
$ python test_cr_tool.py
test_step1_z2 (__main__.Step1_沿y方向的差分.test_step1_z2) ... ERROR
...
NotImplementedError: 第 1 步还没写：d_dy —— 见 lab/README.md 任务表第 1 行
...
Ran 22 tests in 0.004s

FAILED (errors=22)
```

最后那行 `FAILED (errors=22)` 是重点：**留白态必须是不通过的**，退出码 1
（PowerShell 里紧接着跑 `echo $LASTEXITCODE` 能看到 1）。

八步填完、跑出下面这两行，就算做完（退出码 0）：

```term
$ python test_cr_tool.py
...
Ran 22 tests in 0.001s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_cr_tool.py -k step3
```

---

## 任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `d_dy` | 沿 $y$ 方向的一阶偏导 $\partial f/\partial y$ | `-k step1` |
| 2 | `cr_residual` | 两条 CR 残差 $r_1=u_x-v_y$、$r_2=u_y+v_x$ | `-k step2` |
| 3 | `cr_holds` | 一点上 CR 成立吗（按容差判） | `-k step3` |
| 4 | `cr_points` | 一批点里满足 CR 的那些（保持顺序） | `-k step4` |
| 5 | `verdict` | 判定卡结论：`all` / `some` / `none` | `-k step5` |
| 6 | `laplacian` | $\Delta u=u_{xx}+u_{yy}$ | `-k step6` |
| 7 | `is_harmonic` | $u$ 在这批点上调和吗 | `-k step7` |
| 8 | `polar_cr_residual` | 极坐标 CR 的残差（带 $1/r$） | `-k step8` |
| 9 | —（不用填） | 把课件那张「处处不解析函数」表跑一遍 | `-k step9` |

已经在文件里写好的三个是 `u_of`、`v_of`、`d_dx`——它们是样板，照它们的形状往下填。

---

## 逐步做

### 第 1 步 · 沿 y 方向的差分

$x$ 方向的一阶偏导是

$$\frac{\partial f}{\partial x}\approx\frac{f(x+h,\,y)-f(x-h,\,y)}{2h},$$

`d_dx` 已经写好了。$y$ 方向把「$y$ 增加 $h$」翻成复数，就是 $z$ 加上 $ih$：

$$\frac{\partial f}{\partial y}\approx\frac{f(z+ih)-f(z-ih)}{2h}.$$

**唯一容易错的地方**：分子没有除以 $i$，所以分母还是 $2h$，不是 $2hi$。
（若写成 $2hi$，对 $z^2$ 算出来正好是 $f'(z)$ 而不是 $i f'(z)$——第 1 步的断言能立刻抓出来。）

写完后 `python test_cr_tool.py -k step1`，应看到 `OK`（2 个测试）。

### 第 2 步 · 两条残差

`d_dx` 返回的是**复数** $u_x+i v_x$（实部、虚部各是一个偏导），`d_dy` 返回 $u_y+i v_y$。所以

$$r_1=u_x-v_y,\qquad r_2=u_y+v_x,$$

其中 $u_x$、$v_x$ 取自 `d_dx` 的实部与虚部，$u_y$、$v_y$ 取自 `d_dy` 的实部与虚部。

纸上算过的两个数可以拿来对：$\bar z$ 的两条残差是 $(2,0)$（$u_x=1$、$v_y=-1$），
$|z|^2$ 在 $1+i$ 处是 $(2,2)$（$u_x=2x$、$u_y=2y$）。测试里用的就是这两组。

### 第 3 步 · 一点上成不成立

数值差分只能是**近似**，所以判「等于 0」要写容差：$|r_1|\le \text{tol}$ 且 $|r_2|\le\text{tol}$，
`tol` 默认 `1e-4`。这一步就是纸上「验 CR」那行的代码版。

### 第 4 步 · 点集

把一批点里满足 CR 的筛出来，**按传入顺序**返回（用列表推导就对了；用 `set` 顺序会乱）。
点集的大小就是结论的强弱，这一步的返回值和课件那张表的第三列是同一件事。

### 第 5 步 · 判定卡结论

`verdict` 只返回三个字符串：都满足 `'all'`、部分满足 `'some'`、一个都不满足 `'none'`。
两个坑：空列表要按 `'none'`（`all([])` 在 Python 里是 `True`，别被它骗）；
部分满足时不能返回 `'none'`。

### 第 6 步 · 拉普拉斯

二阶中心差分：$\;u_{xx}\approx\dfrac{u(z+h)-2u(z)+u(z-h)}{h^2}$，
$u_{yy}$ 同理但把 $h$ 换成 $ih$；两者相加就是 $\Delta u$。

**这一步的坑是步长**：要除以 $h^2$，$h=10^{-6}$ 时舍入误差会被放大到 $10^{-3}$ 量级，
结果看着像"不调和"或者大得离谱。实测（参考解，$u=x^2-y^2$ 在 $1+2i$ 处）：
$h=10^{-6}$ 得 $-1.3\times10^{-3}$，$h=10^{-4}$ 得 $-8.9\times10^{-8}$。
所以文件里另给了 `DEFAULT_H2 = 1e-4`，二阶差分用它
（函数签名里已经默认好了，你别改成 `DEFAULT_H`）。

### 第 7 步 · 调和判定

`is_harmonic` 就是「每个点都 $|\Delta u|\le\text{tol}$」。这一步是选择题里
「哪个不能作解析函数的实部或虚部」的代码版：$\Delta u\ne0$ 就不是调和函数，直接排除。

### 第 8 步 · 极坐标

把 $w(r,\theta)=f(r e^{i\theta})$ 看成 $r$、$\theta$ 的复值函数，分别对 $r$、$\theta$ 差分：

$$s_1=u_r-\frac{v_\theta}{r},\qquad s_2=v_r+\frac{u_\theta}{r}.$$

$1/r$ **不能漏**——漏了以后常数倍全错（第 8 步的断言会给出差了多少倍）。
这条式子就是课件里验证 $1/z$ 的那两条，测试里也把 $1/z$ 放进去了。

### 第 9 步 · 整表自检（不用填）

`-k step9` 把课件那张「处处不解析函数」的表格跑一遍：$z^2$ 应 `all`、$\bar z$ 应 `none`、
$|z|^2$ 应 `some`、$\operatorname{Re}z$ 与 $i\operatorname{Im}z$ 应 `none`。
它全绿，说明你的工具和纸面结论对得上——这就是这一步的交付证据。

---

## 卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`期望 X，实际 Y`。两个数一比，差符号、差因子、差一个 $i$ 都看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 期望 `(-4+2j)`，实际 `(2+4j)` | 分母多除了一个 `1j` |
   | step1 期望 `-1j`，实际 `1` | 忘了步进 `1j*h`，差分退化成对 $x$ 求导 |
   | step2 的 $r_2$ 与期望差一个负号 | 写成了 `u_y - v_x` 或 `v_x - u_y` |
   | step3 全是 `False` | 容差写死成 `== 0`，或者 `tol` 传成了 0 |
   | step4 顺序乱 / 少了点 | 用了 `set`，或者筛选条件写成了 `cr_holds` 的否定 |
   | step5 空列表返回 `'all'` | `all([])` 是 `True`，要先判空 |
   | step6 结果第三位小数就歪（$\Delta u$ 误差约 $10^{-3}$） | 二阶差分用了 `DEFAULT_H`，没换 `DEFAULT_H2` |
   | step8 差常数倍 | 少了 `1/r`，或者对 $\theta$ 差分时把 $r$ 也动了 |

3. **还不对，再看参考解**：`solutions/0002-cr-check-tool/cr_tool.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（别整段拷，第 9 步会验你懂不懂）。

参考解那一步为什么这样写，`solutions/0002-cr-check-tool/README.md` 里有逐条说明。

---

## 做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0002-cr-check-tool\cr_tool.py .    # Windows
$ python test_cr_tool.py
...
Ran 22 tests in 0.001s

OK
```

**先自己全绿、再对照**：直接拷参考解会跳过判断过程，第 9 步验的正是「你能不能从点集说出结论」。
