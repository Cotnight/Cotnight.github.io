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


---

# 实验一 · 复变函数图像画廊（0003-gallery）

上面那一节是第 5 课（可导与解析的判定）的小 lab，磁盘上的目录叫 `0005-cr-check-tool`
（上面目录树里写成了 0002，以磁盘上的为准）。本节是**实验一**的实操任务，两节互不影响：
各用各的目录、各跑各的测试，`gallery.py` 与 `cr_tool.py` 没有依赖关系。

实验一验收的是「复数会算」能不能变成「复数会画」：**做出能画出方根分布与 $z^2+c$ 迭代图的
Notebook**。这套东西是图像画廊的第一块，实验二（解析函数长什么样）会直接复用本节的坐标换算与
读 CSV 的代码，所以这一块要留着。

---

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `gallery.py` 里 8 个留白函数 | `lab/0003-gallery/gallery.py` | `python test_gallery.py` 打出 `OK` |
| `out/roots.csv`、`out/grid.csv` | `lab/0003-gallery/out/` | 第 7 步自检写出；两列点、整数矩阵都能读回 |
| `gallery.ipynb`（画廊第一块） | `lab/0003-gallery/gallery.ipynb` | 从头 Run All 不报错，两张图看得见结构 |

`out/` 里那两份 CSV 就是「图的数据」：`roots.csv` 是方根的坐标，`grid.csv` 是缩略图每个像素的
逃逸步数。没有 matplotlib 也能把它们交出来——图只是数据的另一种画法。

---

## 二、装环境（本机没有，要你自己装）

本机（这台）只有 numpy，**没有 matplotlib、也没有装 Jupyter**。画图与 notebook 这两样请在你自己的
电脑上做，或自己装到本机：

```sh
pip install numpy matplotlib jupyter
```

装完在 `lab/0003-gallery/` 里启动（不要用 `jupyter notebook` 的默认目录，不然 import 不到 `gallery.py`）：

```sh
cd lab/0003-gallery
jupyter notebook
```

**没装也照样能自检**：`test_gallery.py` 只用标准库（`cmath` / `csv` / `math` / `unittest`），
不装 numpy 时第 8 步自动跳过，前面 7 步照跑。所以先把函数填对、把 `out/*.csv` 交出来，
画图留到你装好环境之后——顺序反过来也行，但数值没对上画的图一定是错的。

---

## 三、目录

```
lab/
├── README.md                    ← 本文件（第 5 课的 CR 检查器 + 实验一的画廊）
├── 0005-cr-check-tool/          ← 第 5 课那一节（cr_tool.py + test_cr_tool.py）
├── 0003-gallery/
│   ├── gallery.py               ← 你要填的 8 个函数（留白）
│   ├── test_gallery.py          ← 28 条断言，自动判分
│   └── out/                     ← 第 7 步自检写出 roots.csv 与 grid.csv
└── solutions/
    ├── 0005-cr-check-tool/      ← 第 5 课的参考解
    └── 0003-gallery/
        ├── gallery.py           ← 参考解（做完才看）
        └── README.md            ← 每一步为什么这样写、常见错法
```

---

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0003-gallery
$ python test_gallery.py
```

现在（还没动手）会是这样——28 个 ERROR，**退出码 1**：

```term
$ python test_gallery.py
...
NotImplementedError: 第 1 步还没写：nth_roots —— 见 lab/README.md 任务表第 1 行
...
Ran 28 tests in 0.005s

FAILED (errors=28)
```

八步填完、跑出下面这两行，才算数值这一半做完了（退出码 0）：

```term
$ python test_gallery.py
...
Ran 28 tests in 0.010s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_gallery.py -k step5
```

`-k` 后面**大小写要照写**（`step5` 能选中，`Step5` 也行，但写成 `steps5` 就是 `NO TESTS RAN`、退出码 5）。

两个环境的实测输出（同一份参考解）：

- 有 numpy 的解释器：`Ran 28 tests`、`OK`，退出码 0，第 8 步也跑了；
- 只有标准库的解释器：`Ran 28 tests ... OK (skipped=2)`，退出码 0，第 8 步跳过。

---

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `nth_roots` | $z_0$ 的全部 $n$ 次方根（$k=0..n-1$ 的顺序） | `-k step1` |
| 2 | `arg_degrees` | 辐角主值换成 $[0,360)$ 的度数（着色用） | `-k step2` |
| 3 | `escape_from` | 从 $z_0$ 出发按 $z\mapsto z^2+c$ 迭代的**逃逸步数** | `-k step3` |
| 4 | `mandelbrot_escape`、`escaped` | 从 0 出发的逃逸步数；以及「逃出去没有」 | `-k step4` |
| 5 | `escape_grid` | 把一块矩形窗口铺成 $宽\times高$ 的逃逸步数网格 | `-k step5` |
| 6 | `save_points_csv`、`save_grid_csv` | 点集与网格存成 CSV | `-k step6` |
| 7 | —（不用填） | 把画廊第一块的两份数据跑出来写进 `out/` | `-k step7` |
| 8 | `escape_grid_np` | 第 5 步的 numpy 向量化版（没装 numpy 就跳过） | `-k step8` |

文件里已经写好的两个是 `pixel_to_re`、`pixel_to_im`——它们是样板，照它们的形状往下填，**别改**：
第 5 步的断言按它们的坐标算。

---

## 六、逐步做

### 第 1 步 · 方根的模与角

$z_0$ 的 $n$ 个 $n$ 次方根是

$$ z_k=\sqrt[n]{|z_0|}\;e^{i(\theta+2k\pi)/n},\qquad \theta=\operatorname{Arg} z_0,\ k=0,1,\dots,n-1 . $$

三件事一起做：模统一取 $\sqrt[n]{|z_0|}$（`abs(z0) ** (1/n)`），角从 `cmath.phase(z0)` 出发
**按弧度**加 $2\pi k$ 再除 $n$，用 `cmath.exp(1j * 角)` 转回复数。

**唯一容易错的地方**：`cmath.phase` 给的是弧度，别中途 `math.degrees` 一下再塞回公式——
课程大纲里那条「方根用角度制算辐角，图案整体转错角度」就是这个。$z_0=1+i$（辐角 $45^\circ$）、
$n=3$ 时第一个根的角度必须是 $15^\circ$，断言会直接点名这一条。

写完后 `python test_gallery.py -k step1`，应看到 `OK`（6 个测试）。

### 第 2 步 · 辐角着色

`cmath.phase` 的值落在 $(-\pi,\pi]$，负数直接拿去当色相会绕回去。所以先 `math.degrees(...)`，
再 `% 360` 把它压进 $[0,360)$：$-45^\circ$ 要变成 $315^\circ$。

$z=0$ 处 `cmath.phase` 返回 `0.0`（不报错），照原样返回 0 就行——原点的颜色本来没有意义。

### 第 3 步 · 迭代与逃逸判据

曼德博集的规则只有一行：$z\mapsto z^2+c$，从 $c$ 附近的起点反复迭代。

```text
z = z0
重复 max_iter 次：
    z = z*z + c
    如果 |z| > 2：这一次的步数就是答案
没逃出去：返回 max_iter
```

**三个坑，断言各抓一个**：

1. **先迭代再看模**，不是先看起点的模。$c=1$ 时 $0\to1\to2\to5$，第 3 步才超过 2。
2. **严格大于 2**。$c=-2$ 时 $z_1=-2$、$z_2=2$……模正好等于 2，永远不逃逸，答案是 `max_iter`；
   写成 `>= 2` 会得到 1，图像上曼德博集会在实轴左端被啃掉一块。
3. **没逃逸要返回 `max_iter`**，不是 `None`、也不是 0——颜色表的长度靠这个数对齐。

为什么判据是 2：若某步 $|z|>2$ 且 $|z|\ge|c|$，则
$|z^2+c|\ge|z|^2-|c|\ge|z|(|z|-1)>|z|$，模会一路涨下去。所以「超过 2」就等于「一定飞出去」。

### 第 4 步 · 曼德博集的点

`mandelbrot_escape` 就是一步包装：起点固定成 `0j` 调 `escape_from`。
`escaped` 也只回答一个是非题：**逃逸步数小于 `max_iter`** 就是逃出去了。
别写反成「等于 `max_iter` 才算逃出去」——那正好把集内集外换了个个儿。

### 第 5 步 · 铺成网格（第 0 行在最下面）

两层循环：外层行、内层列，每个格子用样板换算坐标，再喂给 `mandelbrot_escape`。

$$ c_{row,col}=\texttt{pixel\_to\_re}(col)\;+\;i\cdot\texttt{pixel\_to\_im}(row). $$

**这一步唯一的坑是行序**：`grid[0]` 必须是 $y=$ `im_min` 那一行，也就是**数学上的最下面一行**。
如果你按屏幕的习惯从 `im_max` 往下排，整张缩略图会上下颠倒——断言里专门拿左下角
（`re_min, im_min`）和右上角（`re_max, im_max`）这两个角对了一遍，它们不相等，翻过来立刻现形。
（画图时 `imshow` 也要配 `origin="lower"`，第七节会再提一次。）

另外 `escape_grid` 的结果要跟逐点算的**逐格相同**：别在里面偷偷换成 `np.linspace`。

### 第 6 步 · 存成 CSV

用 `csv.writer`，`open(..., "w", encoding="utf-8", newline="")` 三件套一个都不能少：

- 少了 `newline=""`，Windows 上每行会写成 `\r\r\n`，文件里多出一倍空行（断言查的就是这个）；
- `encoding` 不写，中文注释或被别的软件打开时会乱码；
- 别把复数对象直接塞给 writer（`(0.5+0.86j)` 不是数），拆成 `z.real` 与 `z.imag` 两列。

`save_points_csv` 返回写入的**数据行数**（不含表头），`save_grid_csv` 返回 `(行数, 列数)`。

### 第 7 步 · 整块自检（不用填）

这一步不用写代码，它把画廊第一块的两份数据跑出来：

- `nth_roots(1+1j, 5)`：5 个根、模都等于 $|1+i|^{1/5}\approx1.0718$、每隔 $72^\circ$ 一个
  （角度依次是 $9^\circ,81^\circ,153^\circ,225^\circ,297^\circ$）——这就是画出来会看到的正五边形；
- 40×24 窗口、`max_iter=60` 的缩略图：**逃逸步数等于 60 的格子有 224 个**（占 960 格的 23%）。
  这个比例是全图「集占多大」的数值代理，画出来以后曼德博集应当像一团偏左的「心形 + 圆盘」；
- 最后把 `out/roots.csv`、`out/grid.csv` 写出来，这就是你要交的证据。

它全绿，说明你的数和图对得上；跑了却红，多半是第 5 步的行序或第 3 步的判据还没对。

### 第 8 步 · numpy 向量化（可选，有 numpy 才跑）

第 5 步的双层循环在 40×24 上够用（480×320、`max_iter=80` 也只要 0.2 秒），
但实验二要拿这套东西扫整片复平面，那时就该向量化：一次把整块矩形铺成复数数组，用布尔掩码
只推进还活着的点。

```text
c = re[None, :] + 1j * im[:, None]        # 形状 (高, 宽)
z = 全 0，counts 全填 max_iter，active 全 True
第 k 次迭代：
    z[active] = z[active]^2 + c[active]
    gone = active 且 |z| > 2
    counts[gone] = k；active 去掉 gone
```

**两个坑**：形状是 `(高, 宽)`，不是 `(宽, 高)`；坐标要用 `pixel_to_re` / `pixel_to_im` 取，
这样与第 5 步**逐格相同**。用 `np.linspace` 也能跑，但末位可能差一点点，边界上的点会翻格，
跟第 5 步就对不上了（断言会比整张矩阵）。

---

## 七、组装 Notebook（画廊第一块，四个 cell）

函数全绿之后，`gallery.ipynb` 里只放「调用 + 画图」，不要再抄一遍算法。

**Cell 1 · 导入与窗口**

```python
import matplotlib.pyplot as plt
from gallery import nth_roots, arg_degrees, escape_grid_np   # 或 escape_grid

RE_MIN, RE_MAX, IM_MIN, IM_MAX = -2.0, 0.5, -1.25, 1.25
```

**Cell 2 · 方根分布图**

```python
roots = nth_roots(1 + 1j, 5)
xs = [z.real for z in roots]          # 一定先分离实部虚部
ys = [z.imag for z in roots]

fig, ax = plt.subplots(figsize=(4, 4))
ax.scatter(xs, ys, c=[arg_degrees(z) for z in roots], cmap="hsv", vmin=0, vmax=360)
ax.plot(xs + [xs[0]], ys + [ys[0]], lw=0.8)      # 连一圈：正五边形
ax.axhline(0, lw=0.5, color="gray")
ax.axvline(0, lw=0.5, color="gray")
ax.set_aspect("equal")                           # 不设的话圆被画成椭圆
ax.set_title("z = 1+i 的 5 个五次方根")
plt.show()
```

**Cell 3 · $z^2+c$ 迭代缩略图**

```python
grid = escape_grid_np(RE_MIN, RE_MAX, IM_MIN, IM_MAX, 480, 320, 80)

plt.figure(figsize=(6, 4))
plt.imshow(grid, origin="lower", cmap="magma",
           extent=[RE_MIN, RE_MAX, IM_MIN, IM_MAX])
plt.colorbar(label="逃逸步数")
plt.title("曼德博集缩略图")
plt.show()
```

`origin="lower"` 不能省：`grid[0]` 是最低的那一行，而 `imshow` 默认把第 0 行画在**最上面**，
不写这张图就是上下颠倒的（跟第 5 步那个坑是同一个）。

**Cell 4 · 结论（Markdown cell，两句话）**

写这两句就够，别写成小作文：

- $n$ 个方根模相等、相邻夹角都是 $360^\circ/n$，所以画出来是正 $n$ 边形；
- $|z|$ 一旦某步超过 2 就必然飞向无穷，所以「第几步超过 2」可以把平面染成有边界的图——
  边界外面是逃逸步数（亮），里面是迭代预算用完的暗色。

打开 `out/roots.csv` 与 `out/grid.csv` 用 `numpy.loadtxt` 读一遍，数值应当和图上一致。

---

## 八、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`AssertionError: ...` 里通常就带着期望值和实际值。差 $2\pi$、差一个
   $1/n$、差符号，都在那一行看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 角度差 3 倍、图案整体转了个角度 | 辐角用了角度制（`math.degrees` 混进公式） |
   | step1 只有一个根 / 根数对但都重合 | `range(n)` 写成了 `range(1)`，或 $2\pi k$ 漏了 `k` 的循环 |
   | step1 根的和不为 0 | 模算成了 $\|z_0\|^{n}$ 而不是 $\|z_0\|^{1/n}$ |
   | step2 第三、四象限颜色倒着转 | 少了 `% 360`，负角没翻成正角 |
   | step3 `c=-2` 得到 1 | 判据写成了 `>= 2`，应为 `> 2` |
   | step3 没逃逸时得到 `None` 或 0 | 循环外要 `return max_iter` |
   | step4 `escaped` 全反了 | 条件写成了 `== max_iter` |
   | step5 整张矩阵第一行与最后一行互换了 | 行序按 `im_max` 往下排了，应为 `im_min` 在最下面 |
   | step5 每行内容相同 / 列不动 | 内层循环用了 `row`，或者坐标换算没走 `pixel_to_re` |
   | step6 文件里每行之间有空白行 | `open` 少了 `newline=""` |
   | step6 表头被当成数据 | 第一行要写 `header`，数据从第二行开始 |
   | step8 只差几个格子 | 坐标用了 `np.linspace`，改成 `pixel_to_re` / `pixel_to_im` |
   | step8 形状反了 | 数组铺成了 `(宽, 高)`，应为 `(高, 宽)` |

3. **还不对，再看参考解**：`solutions/0003-gallery/gallery.py`，**先只读卡住的那一个函数**，
   对照完立刻回来自己写一遍（第 7 步验的是「你填完以后数据对不对」，整段拷会让你跳过判断过程）。

参考解那一步为什么这样写，`solutions/0003-gallery/README.md` 里有逐条说明与常见错法。

---

## 九、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0003-gallery\gallery.py .    # Windows
$ python test_gallery.py
...
Ran 28 tests in 0.010s

OK
```

然后再对照自己写的：**先自己全绿、再对照**。两者的差别如果只在写法（比如用列表推导还是
`for`），不用改；如果差在行序、判据、角度单位，那就是你图像出错的根源。

---

## 十、和实验二的关系

实验二（解析函数长什么样）要画 $e^z$、$\sin z$、$\operatorname{Ln} z$ 与 $\bar z$、$|z|^2$ 的
模—辐角着色图，用的正是本节的 `pixel_to_re` / `pixel_to_im` 与「铺一格窗口、逐点算一个数」的
套路；`save_points_csv` 到那时也照用。所以 `gallery.py` 与 `out/` 别删，下一块图要接着长在它上面。

---

# 实验二 · 解析函数长什么样（0006-analytic-gallery）

上面两节分别是第 5 课的小 lab 与实验一，本节是**实验二**。它验收的那句话是：
**做出解析与非解析函数的图像对照，并数值验证柯西-黎曼条件。**

它接着实验一长，不从零开始：

- 实验一的 `pixel_to_re` / `pixel_to_im`（像素下标 ↔ 复平面坐标）与「铺一格窗口、逐点算一个数」
  的套路照用；
- 第 5 课那套 `d_dx` / `d_dy` / `cr_residual` / `cr_holds` 也照用。

所以 `analytic_gallery.py` 开头就把这六个样板放好了（**别改**），你从第 7 个函数开始填。
三个目录各跑各的测试，互不依赖：`cr_tool.py`、`gallery.py` 都别删，也不要改。

---

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `analytic_gallery.py` 里 9 个留白函数 | `lab/0006-analytic-gallery/analytic_gallery.py` | `python test_analytic_gallery.py` 打出 `OK` |
| `out/scan.csv` | `lab/0006-analytic-gallery/out/` | 六个函数各一行：总点数、成立点数、比例、最大残差 |
| `out/residual-exp.csv`、`out/residual-conj.csv` | 同上 | 21 行 × 31 列的残差矩阵；前者整片 `1e-10` 量级，后者整片 `2` |
| 三句结论（写进 notebook，或直接回话） | — | 见第七节末，三条各一句 |

`out/` 里的三份 CSV 就是「图的数据」：没有 matplotlib 也能把它们交出来，图只是数据的另一种画法
（第七节给了一个只用标准库的字符图）。

---

## 二、环境依赖

**只要 Python 3.8+，只用标准库（`cmath` / `csv` / `math` / `unittest`）**，不装任何第三方包。

- numpy 可选，只用于第 10 步的向量化残差图；没装那两条测试自动跳过，不影响结论；
- matplotlib 与 Jupyter **完全不需要**：交付物是 CSV，画图是可选的第 8 节。

本机实测的两个解释器：`D:/Program Files/Python313/python.exe`（3.13.15，无 numpy）与
bundled runtime（3.12.14 + numpy 2.3.5）。命令里的 `python` 按你自己的环境换。

---

## 三、目录

```
lab/
├── README.md                            ← 本文件（第 5 课 CR 检查器 + 实验一 + 实验二）
├── 0005-cr-check-tool/                  ← 第 5 课那节
├── 0006-analytic-gallery/
│   ├── analytic_gallery.py              ← 你要填的 9 个函数（留白）
│   ├── test_analytic_gallery.py         ← 38 条断言，自动判分
│   └── out/                             ← 自检写出 scan.csv 与两张残差图
├── 0003-gallery/                        ← 实验一那节
└── solutions/
    ├── 0005-cr-check-tool/
    ├── 0006-analytic-gallery/
    │   ├── analytic_gallery.py          ← 参考解（做完才看）
    │   └── README.md                    ← 九个函数为什么这样写、常见错法
    └── 0003-gallery/
```

---

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0006-analytic-gallery
$ python test_analytic_gallery.py
```

现在（还没动手）会是这样——38 条里 36 条 ERROR，**退出码 1**：

```term
$ python test_analytic_gallery.py
...
NotImplementedError: 第 1 步还没写：scan_window —— 见 lab/README.md 任务表第 1 行
...
Ran 38 tests in 0.014s

FAILED (errors=36, skipped=2)
```

九步填完、跑出下面这两行，数值这一半才算做完（退出码 0）：

```term
$ python test_analytic_gallery.py
...
Ran 38 tests in 0.046s

OK (skipped=2)                       ← 只有标准库的解释器：numpy 那两条跳过
```

```term
$ python test_analytic_gallery.py
...
Ran 38 tests in 0.032s

OK                                   ← 有 numpy 的解释器：38 条全跑
```

只验某一步（填一步验一步，别一次填完）：`python test_analytic_gallery.py -k step4`。
`-k` 后面写测试名里的一段：`step1` … `step9`、`numpy`、`selfcheck`。

---

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验（条数） |
|---|---|---|---|
| 1 | `scan_window` | 把一块矩形窗口铺成复数点，一行行往下展平 | `-k step1`（3） |
| 2 | `cr_scan` | 逐点的 CR 标签（保持顺序的 bool 列表） | `-k step2`（4） |
| 3 | `analytic_fraction` | CR 成立的点占多大比例 | `-k step3`（4） |
| 4 | `residual_map` | 残差图数据：每格 $\max(\lvert r_1\rvert,\lvert r_2\rvert)$ | `-k step4`（4） |
| 5 | `grad_u_v` | $u$、$v$ 的两个梯度向量 | `-k step5`（3） |
| 6 | `orthogonality` | 两个梯度夹角的余弦（0 = 正交） | `-k step6`（4） |
| 7 | `jacobian` | $u_xv_y-u_yv_x$：解析为正、反解析为负 | `-k step7`（4） |
| 8 | `save_summary_csv` | 六个函数一张对照结论表 | `-k step8`（3） |
| 9 | `save_grid_csv` | 残差图存成 CSV（小残差不许丢成 0） | `-k step9`（3） |
| 10 | `residual_map_np`（可选） | 第 4 步的 numpy 向量化版 | `-k numpy`（2） |
| — | 不用填 | 整块自检：跑六个函数、写出 `out/` 三份数据 | `-k selfcheck`（4） |

六个样板（`pixel_to_re`、`pixel_to_im`、`d_dx`、`d_dy`、`cr_residual`、`cr_holds`）已经写好，
照它们的形状往下填。

---

## 六、逐步做

### 第 1 步 · 铺一格窗口

```python
def scan_window(re_min, re_max, im_min, im_max, width, height):
    return [complex(pixel_to_re(col, width, re_min, re_max),
                    pixel_to_im(row, height, im_min, im_max))
            for row in range(height)
            for col in range(width)]
```

两个循环的**嵌套顺序**决定展平的顺序：外层行、内层列 → 第 0 行整行在前。第 0 行是 $y$ 最小的
那一行（`im_min`），这也是实验一那个坑的同一个位置。

**唯一容易错的地方**：内层循环写成 `for row in range(...)`（每行内容一样），或者自己再写一遍坐标
公式——自己写的和样板差一个末位，第 4 步的残差图就会跟逐点算的对不上。

写完后 `python test_analytic_gallery.py -k step1`，应看到 `OK`（3 个测试）。

### 第 2 步 · 逐点的标签

```python
return [cr_holds(f, z, tol, h) for z in points]
```

第 5 课的 `cr_points` 返回的是**筛出来的点**，这里要的是**每个点成立不成立**——这批标签后面要拿去
上色，一个点都不能丢。

### 第 3 步 · 比例

先判空（空点集返回 `0.0`，别让 `ZeroDivisionError` 冒出来），再「命中数 / 总数」。

为什么用比例：「CR 成立的点集有多大」才是结论的强弱。参考解在 $31\times21$ 的窗口上量出来是
$e^z$、$\sin z$、$z^2$ 各 `1.0000`，$\bar z$ 是 `0.0000`，$\lvert z\rvert^2$ 是 `0.0015`
（$651$ 个点里只有原点一个，因为原点正好落在格点上）。

### 第 4 步 · 残差图

先 `scan_window` 铺点，再对每个点算 `max(abs(r1), abs(r2))`，最后按 `width` 一段段切开成行。

两个坑：切片写成 `values[row::height]` 会按列切（图转 90°）；行序按 `im_max` 往下排会上下颠倒。
参考解的残差图：$e^z$ 整片 $6.7\times10^{-10}$（解析），$\bar z$ 整片 `2`（$r_1=1-(-1)$，满幅）。

### 第 5 步 · 两个梯度

`d_dx` 给的是 $u_x+i v_x$、`d_dy` 给的是 $u_y+i v_y$，实部虚部各取一次就得到四个偏导：

```python
dx, dy = d_dx(f, z, h), d_dy(f, z, h)
return ((dx.real, dy.real), (dx.imag, dy.imag))
```

这两个向量是**等值线的法向量**：解析函数满足 $\lvert f\rvert=e^u$，所以模的等值线就是 $u$ 的等值线；
而 $\arg f=v$，辐角的等值线就是 $v$ 的等值线。两组线正交 ⟺ 两个法向量垂直。

### 第 6 步 · 正交吗

$$\cos\theta=\frac{\nabla u\cdot\nabla v}{\lvert\nabla u\rvert\,\lvert\nabla v\rvert}$$

模长用 `math.hypot`。任一梯度是零向量时返回 `None`：$\lvert z\rvert^2$ 的 $v\equiv0$，谈不上
「辐角等值线」，夹角没有意义。

### 第 7 步 · 方向（行列式）

$$\det J=u_xv_y-u_yv_x .$$

CR 成立时 $\det J=u_x^2+u_y^2=\lvert f'(z)\rvert^2>0$。$\bar z$ 的 $\det J=-1$——**它的两组线也正交**，
所以「正交」判不出解析，方向（符号）才判得出。这一步是第 5 课「处处不解析函数」那张表的又一个维度。

### 第 8 步 · 结论表

`csv.writer` + `utf-8` + `newline=""` 三件套；比例写四位小数，**残差写 `"{:.6g}"`**。
残差写成四位小数的话，$10^{-10}$ 全变 `0.0000`，表里「解析」和「非解析」两行就看不出差别了。

### 第 9 步 · 残差图存盘

一行一个像素行、不写表头、每格 `"{:.6g}"`，返回 `(行数, 列数)`。和第 8 步一样，格式决定这张图还能
不能读出东西。

### 第 10 步 · 向量化（可选）

```python
c = re[None, :] + 1j * im[:, None]     # 形状 (高, 宽)
dx = (f_np(c + h) - f_np(c - h)) / (2 * h)
dy = (f_np(c + 1j * h) - f_np(c - 1j * h)) / (2 * h)
```

`f_np` 必须能吃数组（`np.exp`、`np.sin`、`np.conj`），`cmath.exp` 不行。形状是 `(高, 宽)` 不是
`(宽, 高)`；坐标仍走 `pixel_to_re` / `pixel_to_im`，这样才和逐点版逐格相同（断言比到 $10^{-12}$）。

### 整块自检（不用填）

`-k selfcheck` 跑六个函数，写出三份交付数据，并验两件事：

| 函数 | 窗口 | 成立点数 | 比例 | 最大残差 |
|---|---|---|---|---|
| $e^z$ | $[-1.5,1.5]^2$ | 651 / 651 | 1.0000 | `6.66134e-10` |
| $\sin z$ | 同上 | 651 / 651 | 1.0000 | `4.44089e-10` |
| $z^2$ | 同上 | 651 / 651 | 1.0000 | `4.44089e-10` |
| $\bar z$ | 同上 | 0 / 651 | 0.0000 | `2` |
| $\lvert z\rvert^2$ | 同上 | 1 / 651 | 0.0015 | `3` |
| $\operatorname{Ln} z$ | $[0.25,1.5]\times[-1.5,1.5]$ | 651 / 651 | 1.0000 | `1.66533e-10` |

**$\operatorname{Ln} z$ 为什么换窗口**：主值 $\operatorname{Ln} z$ 在负实轴上不连续，而那正是差分要跨的
地方。把窗口挪到左半平面（$[-1.5,-0.25]\times[-1.5,1.5]$）再跑，比例掉到 `620 / 651`——失败的正好是
$y=0$ 那一行的 31 个点，残差约 $3.1\times10^{6}$（那是 $\pi/h$）。这不是函数不解析，是**差分跨了割线**：
$2\pi$ 的相位跳变被当成了导数。大纲里那条「$\operatorname{Ln} z$ 的分割线被误判为不解析」，在数值上
就是这个形态——认它的办法是看残差量级：解析函数的残差在 $10^{-10}$，假失败是 $10^{6}$，差十几个数量级。

---

## 七、不装 matplotlib 也能看图

交付物是 CSV，但你还是想「看见」一点东西。把残差图当字符矩阵打出来就行，只要标准库：

```python
import analytic_gallery as ag

def show(grid):
    for line in grid:
        print("".join("#" if v > 1e-6 else "." for v in line))

for name, f in (("|z|^2", ag.f_mod_sq), ("z-bar", ag.f_conj), ("e^z", ag.f_exp)):
    print(name)
    show(ag.residual_map(f, -1.0, 1.0, -1.0, 1.0, 17, 5))
```

实测输出（$-1..1$ 的窗口，第 0 行在最下面）：

```term
|z|^2
#################
#################
########.########
#################
#################
z-bar
#################
#################
#################
#################
#################
e^z
.................
.................
.................
.................
.................
```

`#` = 残差大于 $10^{-6}$（CR 不成立），`.` = 残差在容差内（成立）。$\lvert z\rvert^2$ 只剩正中一个点，
$\bar z$ 整片不成立，$e^z$ 整片成立——这就是「对照」肉眼能看的那一面。

三份数据出来后，**结论段三句话**（写进 notebook，或直接回话）：

1. $e^z$、$\sin z$、$z^2$ 整片成立（651/651），残差在 $10^{-10}$：这三个在窗口内解析。
2. $\bar z$ 一个点都不成立（残差恒为 2），$\lvert z\rvert^2$ 只有原点成立：前者处处不解析，
   后者只在一点可导、不解析——点集的一两个点不等于一整片区域。
3. $\operatorname{Ln} z$ 在右半平面整片成立；跨负实轴那列点的「失败」是差分跨过割线造成的假失败
   （残差 $10^{6}$ 量级），不是函数不解析。

---

## 八、装了 matplotlib 就画出来（可选）

```python
import matplotlib.pyplot as plt
import analytic_gallery as ag

grid = ag.residual_map(ag.f_exp, -1.5, 1.5, -1.5, 1.5, 31, 21)
plt.imshow(grid, origin="lower", extent=[-1.5, 1.5, -1.5, 1.5], cmap="magma")
plt.colorbar(label="max(|r1|, |r2|)")
plt.title("e^z 的 CR 残差：整片接近 0")
plt.show()
```

`origin="lower"` 不能省（`grid[0]` 是最下面那一行，而 `imshow` 默认把第 0 行画在最上面）。
把 `ag.f_exp` 换成 `ag.f_conj`，同一张图会整片变亮——两张并排就是「解析与非解析」的对照图。

---

## 九、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`AssertionError` 后面一般带着期望值与实际值。差符号、差一个 `i`、
   差一个行序，都在那一行看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 每行内容都一样 | 内层循环用了 `row` |
   | step1 每行从右往左 | 列下标写成了 `width-1-col` |
   | step2 断言说长度不对 / 点丢了 | 照抄了第 5 课的 `cr_points`（返回筛出来的点） |
   | step3 抛 `ZeroDivisionError` | 漏了空列表的判空 |
   | step4 整张图转了 90° | 切片写成了 `values[row::height]` |
   | step4 整张图上下颠倒 | 行序按 `im_max` 往下排了，应为 `im_min` 在最下面 |
   | step4 残差大得离谱（$10^{6}$） | 点在割线上（`Ln z` 换窗口），不是函数不解析 |
   | step6 抛 `ZeroDivisionError` | 没判零向量（$\lvert z\rvert^2$ 的 $\nabla v\equiv0$） |
   | step6 余弦到处不为 0 | 两个梯度的四个分量错位（$v_x$ 与 $v_y$ 对调了） |
   | step7 $\bar z$ 的行列式是正数 | 取了绝对值，或写成了 $u_xv_y+u_yv_x$ |
   | step8 / step9 文件里每行之间有空白行 | `open` 少了 `newline=""` |
   | step9 CSV 读回来一片 `0` | 每格写成四位小数了，要用 `"{:.6g}"` |
   | numpy 与逐点版差几个格子 | 坐标改用 `np.linspace` 了 |
   | selfcheck 说 $\lvert z\rvert^2$ 的成立点数不是 1 | 窗口不是 $31\times21$，或原点没落在格点上 |

3. **还不对，再看参考解**：`solutions/0006-analytic-gallery/analytic_gallery.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（自检验的是「你填完以后数据对不对」）。

参考解那一步为什么这样写，`solutions/0006-analytic-gallery/README.md` 里有逐条说明。

---

## 十、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0006-analytic-gallery\analytic_gallery.py .    # Windows
$ python test_analytic_gallery.py
...
Ran 38 tests in 0.046s

OK
```

**先自己全绿、再对照**。两者差别如果只在写法（列表推导还是 `for`），不用改；如果差在行序、切片方向、
格式精度，那就是你图和数据出错的根源。

---

## 十一、和实验三的关系

实验三（保角映射的网格实验）会把同一套东西用在 $z^2$、$e^z$、$1/z$ 上：铺网格 → 逐点映射 → 看直角
是否被保持。它要的判据「保角 ⟺ 导数非零」，正是这里的 `jacobian`：$\det J=\lvert f'(z)\rvert^2$，
$\det J=0$ 的点就是保角失效的临界点（$z^2$ 在原点）。所以 `analytic_gallery.py` 与 `out/` 别删。

# 第 9 课 · 柯西积分公式与高阶导数的数值核对（0009-cauchy-formula-tool）

上面两节是第 5 课（CR 检查器，磁盘上叫 `0005`）与实验一（画廊，`0003`）。本节是第 9 课
「柯西积分公式与高阶导数」的小 lab，三节互不影响：各用各的目录、各跑各的测试。

前面那一节验的是「导数存不存在」，这一节验的是**公式算得对不对**：把
$\oint_C\frac{f(z)}{(z-z_0)^m}dz$ 沿圆周真积一遍，再拿纸上的
$\frac{2\pi i}{(m-1)!}f^{(m-1)}(z_0)$ 去对照。数值对上，那道 7～10 分的大题就多一层保险；
第 9 步还会把课件里那几道真题整表跑一遍。

工具的用法一句话：**先把纸上的答案写下来，再让数值围道积分去验它。**

---

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `cauchy_tool.py` 里 8 个留白函数 | `lab/0009-cauchy-formula-tool/cauchy_tool.py` | `python test_cauchy_tool.py` 打出 `OK`（26 条断言） |
| 一张幂次对照卡（纸笔，不用交文件） | 手边 / 纸笔题型整理册 | 第 7 步填完后能十秒内说清 $m=1,2,3,4$ 各求几阶导 |

`out/`、CSV、图都不用交——这一节只产代码。

## 二、环境依赖

**只要 Python 3.8+，只用标准库（`cmath`、`math`、`unittest`），不装任何第三方包。**
没有 `requirements.txt`，也不需要 numpy：

- 复数是内置类型 `complex`，`1j` 就是虚数单位，$e^{i\theta}$ 写 `cmath.exp(1j * theta)`；
- $2\pi i$ 写成 `2j * math.pi`（文件里已经给成 `TAU`）——这样不会把 $i$ 丢掉；
- 测试用内置 `unittest`，`python test_cauchy_tool.py` 直接跑。

本机实测两个解释器都能跑同一份代码：`D:/Program Files/Python313/python.exe`（Python 3.13.15，
只有标准库）与带 numpy 的
`C:\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`，
两边都是 `Ran 26 tests … OK`。命令里的 `python` 换成本机任意一个 3.8+ 都可以。

## 三、目录

```
lab/
├── README.md                          ← 本文件（第 5 课 + 实验一 + 第 9 课三节）
├── 0009-cauchy-formula-tool/
│   ├── cauchy_tool.py                 ← 你要填的 8 个函数（留白）
│   └── test_cauchy_tool.py            ← 26 条断言，自动判分
└── solutions/
    └── 0009-cauchy-formula-tool/
        ├── cauchy_tool.py             ← 参考解（做完才看）
        └── README.md                  ← 每一步为什么这样写、常见错法
```

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0009-cauchy-formula-tool
$ python test_cauchy_tool.py
```

现在（还没动手）会是这样——26 个 ERROR，**退出码 1**：

```term
$ python test_cauchy_tool.py
test_step1_direction (__main__.Step1_围道采样.test_step1_direction) ... ERROR
...
NotImplementedError: 第 1 步还没写：circle_points —— 见 lab/README.md 任务表第 1 行
...
Ran 26 tests in 0.006s

FAILED (errors=26)
```

最后那行 `FAILED (errors=26)` 是重点：**留白态必须是不通过的**，退出码 1
（PowerShell 里紧接着跑 `echo $LASTEXITCODE` 能看到 1）。

八步填完、跑出下面这两行，就算做完（退出码 0）：

```term
$ python test_cauchy_tool.py
...
Ran 26 tests in 0.008s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_cauchy_tool.py -k step3
...
Ran 3 tests in 0.000s

OK
```

`-k` 后面**大小写要照写**（`step3` 能选中，`Step3` 也行，写成 `steps3` 就是 `NO TESTS RAN`、退出码 5）。

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `circle_points` | 围道 $\lvert z-a\rvert=r$ 上等距的 $n$ 个点（逆时针） | `-k step1` |
| 2 | `contour_integral` | 数值围道积分 $\oint_C f\,dz$（$dz$ 换成 $i\Delta\theta\,(z_k-a)$） | `-k step2` |
| 3 | `inside` | 奇点 $z_0$ 在圈内还是圈外 | `-k step3` |
| 4 | `deriv_n` | 0／1／2 阶数值导（$g^{(m-1)}$ 用它） | `-k step4` |
| 5 | `cauchy_value` | 分母一次方那一项 $2\pi i\,g(z_0)$ | `-k step5` |
| 6 | `high_order_value` | 分母 $m$ 次方那一项 $\frac{2\pi i}{(m-1)!}g^{(m-1)}(z_0)$ | `-k step6` |
| 7 | `formula_value` | 幂次决定用哪个公式（对照卡的代码版） | `-k step7` |
| 8 | `contour_total` | 圈内各项相加、圈外的项按 $0$ | `-k step8` |
| 9 | —（不用填） | 课件那几道考试题整表自检 | `-k step9` |

文件里已经写好的常数是 `DEFAULT_N`、`DEFAULT_H`、`DEFAULT_H2`、`TAU`——照它们的用法往下填，**别改**。

## 六、逐步做

### 第 1 步 · 围道采样

$$ z_k=a+r\,e^{i\theta_k},\qquad \theta_k=\frac{2\pi k}{n},\ k=0,1,\dots,n-1 . $$

从 $a+r$ 出发、逆时针走一圈，正好是「正向简单闭曲线」。$n$ 取 2048：梯形法对**周期解析**
被积函数收敛得极快（误差按 $(d/r)^n$ 掉，$d$ 是奇点到圆心的距离），2048 点已经到机器精度。

**坑**：从圆心出发（忘了乘 $r$）会让第 1 步的 3 条断言全红，后面几步也跟着红；角度写
$-2\pi k/n$ 方向就反了，`test_step1_direction` 会点名「相邻两点的角差」。

### 第 2 步 · $dz$ 换成什么（这一步最容易错）

$z=a+r e^{i\theta}$ 求微分：

$$ dz=i\,r\,e^{i\theta}\,d\theta=i\,\Delta\theta\,(z-a),\qquad \Delta\theta=\frac{2\pi}{n}. $$

于是每一项是 `f(z_k) * (1j * dtheta * (z_k - center))`。八步里只有这一步在跟纸上的
「$dz$ 要换元」打交道——上一节课（复积分的直接计算）那条「$dz$ 忘了换」的坑，在这里变成一行代码。

**两个坑**：漏掉 `1j`，$\oint dz/z$ 会算出 $2\pi$（实数，没有 $i$）；漏掉 `(z_k - center)`，
常数被积函数会算出 $2\pi i$ 而不是 $0$。

### 第 3 步 · 奇点在圈内还是圈外

就是「看内外」那一步的代码版：$\lvert z_0-a\rvert<r$ 才算圈内。**用严格小于**：
距离恰好等于半径时奇点压在围道上，两条公式都不适用（分母在围道上为零），
`test_step3_on_contour` 专门验这两点（$z_0=\pm2$ 在 $\lvert z\rvert=2$ 上）。

### 第 4 步 · 数值求导（0 阶那一条别忘）

$$ g'(z)\approx\frac{g(z+h)-g(z-h)}{2h},\qquad
   g''(z)\approx\frac{g(z+h)-2g(z)+g(z-h)}{h^2}. $$

三件事：

1. **`order = 0` 直接返回 `g(z)`**——公式里 $m=1$ 那一行是「不求导、直接代 $z_0$」，
   对应 $0!=1$。这一步写不出来，第 7 步就分不开两条公式。
2. **二阶差分要除以 $h^2$**，所以默认步长是 `DEFAULT_H2 = 1e-4`；用 `DEFAULT_H = 1e-6`
   会被舍入误差放大到 $10^{-3}$ 量级（第 5 课 `laplacian` 踩的是同一个坑）。
3. 这里算出来的导数**不是精确值**：参考解在 `m=3、g=cos z、z0=i` 处差 $2\times10^{-8}$，
   那是截断误差，不是算错。断言的容差是 $10^{-6}$，就是为了容纳它。

### 第 5 步 · 分母一次方那一项

$$\oint_C\frac{g(z)}{z-z_0}dz=2\pi i\,g(z_0).$$

一行就够：`TAU * g(z0)`。**不要**在这里再求导——求导是高阶导数公式那一支的事。

### 第 6 步 · 分母 $m$ 次方那一项

$$\oint_C\frac{g(z)}{(z-z_0)^m}dz=\frac{2\pi i}{(m-1)!}\,g^{(m-1)}(z_0).$$

三处用的是同一个数 $m-1$：**求导阶数、阶乘、以及「$m=1$ 时它退化成柯西公式」**。
写成 `TAU / math.factorial(m - 1) * deriv_n(g, z0, m - 1)` 就不会错位。

断言里那两条真题值得自己对一遍：$(1+z+z^2)/z^3$ 的二阶导是常数 $2$，答案 $2\pi i$；
分子是常数时求任何正阶导都得 $0$（2023 年 B 卷填空就考这个，**不用真去求 2022 阶导**）。

### 第 7 步 · 幂次决定用哪个（对照卡的代码版）

`formula_value` 只做一个判断：`m == 1` 走第 5 步，`m >= 2` 走第 6 步。
这一步同时是你那张幂次对照卡的自动化版本：

| $m$ | 求几阶导 | 系数 |
|---|---|---|
| 1 | 不求导 | $2\pi i$ |
| 2 | 一阶 | $2\pi i$ |
| 3 | 二阶 | $\pi i$ |
| 4 | 三阶 | $\pi i/3$ |

### 第 8 步 · 两个奇点拆开相加

`terms` 里每个元素是**一个奇点的配方** `(它的 g, 它的位置, 它的幂次)`——$g$ 是
「分子 ÷ 分母的其余因子」，每个奇点的 $g$ 都不一样。先用第 3 步筛，圈外的项跳过，
圈内的用第 7 步算出来累加。

**这一条对应的正是「围道内有两个奇点时只算一个」那个失分点**：
`test_step8_two_poles` 除了比总和，还单独比了「合计 == 两项相加」，
少一项在第 8 步就露馅。同一步还验了两种 $0$：换一条圈不进去的围道（$8\pi i\to0$）
与两项恰好抵消（$\pi i+(-\pi i)$）——后者不是「圈内没奇点」，是**加起来是零**。

### 第 9 步 · 整表自检（不用填）

`-k step9` 把课件里那几道题一张表跑完，每道都验两列：**数值围道积分**与**按公式两项相加**，
两列都要落在理论值上。

| 题 | 围道 | 理论值 |
|---|---|---|
| $z/(z-1)$ | $\lvert z\rvert=2$ | $2\pi i$ |
| $\cos z/(z-i)^3$ | $\lvert z-i\rvert=1$ | $-\pi i\cos i\approx-4.8477i$ |
| $(1+z+z^2)/z^3$ | $\lvert z\rvert=1$ | $2\pi i$ |
| $e^z/(z-3)$ | $\lvert z\rvert=1$ | $0$ |
| $\cos z/(z^2(z+i))$ | $\lvert z\rvert=2$ | $2\pi i(1-\cos i)\approx-3.4123i$ |
| $e^{iz}/(z^2-3\pi z+2\pi^2)$ | $\lvert z-3\rvert=4$ | $4i$ |
| 反向读：$f(\pi)$、$f'(\pi)$ | $\lvert\zeta\rvert=4$ | $2\pi i$、$-2\pi i$ |

最后一条是 2023 年那道选择题：$f(z)=\oint_{\lvert\zeta\rvert=4}\frac{\sin\zeta-\cos\zeta}{\zeta-z}d\zeta$，
读成 $f=2\pi i(\sin z-\cos z)$，再对**这个数值定义的函数**求一次差分，验 $f'(\pi)=-2\pi i$。

它全绿，说明你的工具和纸面结论对上了——这就是这一节的交付证据。

## 七、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`期望 X，实际 Y`。两个数一比，差符号、差因子、差一个 $i$ 都看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 所有点都落在圆心上 | 忘了乘 `radius` |
   | step1 相邻角差是负的 / 点顺时针排 | 角度写成 $-2\pi k/n$ |
   | step2 $\oint dz/z$ 得 $2\pi$（实数） | $dz$ 漏了 `1j` |
   | step2 常数被积函数得 $2\pi i$ 而不是 $0$ | $dz$ 漏了 `(z_k - center)` |
   | step3 围道上的点被判成圈内 | 写成了 `<=`，应为 `<` |
   | step4 二阶导数量级离谱（$10^{-3}$ 以上误差） | 用了 `DEFAULT_H`，应换 `DEFAULT_H2` |
   | step5/6 结果差 $2\pi$ 或差一个 $i$ | 用了 `2*math.pi` 而不是 `TAU`（`2j*math.pi`） |
   | step6 $m=3$ 差 2 倍 / 差 6 倍 | 阶乘写了 `m!` 或求导阶数写了 `m`，两处都要换成 `m-1` |
   | step7 $m=1$ 走进高阶那一支 | 判断写成 `m > 1`，第一支必须是 `m == 1` |
   | step8 只算出一个奇点 | 没遍历 `terms`；`g` 里还带着自己的极点（会 `ZeroDivisionError`） |
   | step9 只有「公式」那一列差 $10^{-8}$ | 正常，是 `deriv_n` 的截断误差，不是错 |

3. **还不对，再看参考解**：`solutions/0009-cauchy-formula-tool/cauchy_tool.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（第 9 步验的是整表，整段拷会让你跳过判断过程）。

参考解那一步为什么这样写，`solutions/0009-cauchy-formula-tool/README.md` 里有逐条说明。

## 八、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0009-cauchy-formula-tool\cauchy_tool.py .    # Windows
$ python test_cauchy_tool.py
...
Ran 26 tests in 0.008s

OK
```

**先自己全绿、再对照**：直接拷参考解会跳过判断过程，第 9 步验的正是「你的公式和数值对不对得上」。

## 九、和后面几课的关系

- **第 10 课（柯西积分定理及其推广）**要用 `contour_total` 的「哪一项算、哪一项不算」去解释复合闭路；
- **第 13 课（留数定理）**会把每一项 $2\pi i\,g(z_0)$ 改叫「$2\pi i$ 乘留数」，
  `cauchy_tool.py` 里这几个函数照用，断言换成留数公式即可；
- **实验四（围道上的留数）**要把这里的 `circle_points` 拿出来画围道、标极点——
  曲线怎么采点、积分怎么求，这一节已经给了。

# 第 10 课 · 柯西积分定理与复合闭路（0010-cauchy-closed-contour）

上面两节各自对应一节课（第 5 课的 CR 检查器、实验一的画廊），本节是**第 10 课（柯西积分定理及其推广）**
的小 lab，还是同一个「复变计算工具」支线：源码 + 测试，你填 7 个函数，30 条断言自动判。

这一课工具做的事只有一句：**把一条围道采样成点列，沿点列把 $f(z)\,dz$ 累加起来，看这个和是 $0$、
是 $2\pi i$、还是别的数。**

为什么值得写一遍：卷面上动笔前那一步「能不能直接写 $0$」，就是这里的三件事——

- 被积函数在**圈内**解析 ⇒ 和式被代码抵成 $0$（柯西积分定理）；
- 奇点在圈里 ⇒ 挖一个洞，**外圈正向 + 内圈反向**合起来的积分也是 $0$，于是外圈那个积分等于内圈那个
  （复合闭路定理）；
- 被积函数含 $\bar z$、$\operatorname{Re} z$ ⇒ 和式抵不掉，结果是 $2\pi i$、$\pi i$ 这种明显的非零值
  （定理失效）。

实验四（围道上的留数）会把这套「围道 + 极点」搬到图上，所以 `cauchy_lab.py` 后面还要用。

---

## 一、目录与依赖

```
lab/
├── README.md                          ← 本文件（三节：CR 检查器 + 画廊 + 本节）
├── 0010-cauchy-closed-contour/
│   ├── cauchy_lab.py                  ← 你要填的 7 个函数（留白）
│   └── test_cauchy_lab.py             ← 30 条断言，自动判分
└── solutions/
    └── 0010-cauchy-closed-contour/
        ├── cauchy_lab.py              ← 参考解（做完才看）
        └── README.md                  ← 每一步为什么这样写、常见错法
```

**环境依赖：只要 Python 3.8+，只用标准库（`cmath` / `math` / `unittest`），不装任何第三方包。**

- 复数用内置类型 `complex`，`1j` 就是虚数单位，$e^{i\theta}$ 写 `cmath.exp(1j * theta)`；
- 测试用内置 `unittest`，`python test_cauchy_lab.py` 直接跑；
- 本机实测环境是 Python 3.13.15（`python --version` 可查）。命令里的 `python` 如果你的机器上没有，
  换成 `py` 或 `python3` 即可。

---

## 二、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0010-cauchy-closed-contour
$ python test_cauchy_lab.py
```

现在（还没动手）会是这样——30 个 ERROR，**退出码 1**：

```term
$ python test_cauchy_lab.py
...
NotImplementedError: 第 1 步还没写：circle_contour —— 见 lab/README.md 任务表第 1 行
...
Ran 30 tests in 0.006s

FAILED (errors=30)
```

最后那行 `FAILED (errors=30)` 是重点：**留白态必须是不通过的**，退出码 1
（PowerShell 里紧接着跑 `echo $LASTEXITCODE` 能看到 1）。

七步填完、跑出下面这两行，就算做完（退出码 0）：

```term
$ python test_cauchy_lab.py
...
Ran 30 tests in 0.013s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_cauchy_lab.py -k step5
```

`-k` 后面**大小写要照写**（`step5` 能选中，`Step5` 也行，写成 `steps5` 就是 `NO TESTS RAN`、退出码 5）。

---

## 三、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `circle_contour` | 正向圆周上的 $n$ 个点（首点不重复） | `-k step1` |
| 2 | `contour_integral` | 沿点列累加 $f(z_k)\Delta z_k$（开路径） | `-k step2` |
| 3 | `closed_integral` | 末点接回首点的闭路积分 | `-k step3` |
| 4 | `nearly_zero` | 按容差判「这个积分算不算 $0$」 | `-k step4` |
| 5 | `composite_integral` | 复合闭路：外圈正向 + 内圈反向 | `-k step5` |
| 6 | `arc_contour` | 圆弧上的 $n+1$ 个点（可反向） | `-k step6` |
| 7 | `arc_integral` | 沿圆弧的积分（第 2 步套第 6 步） | `-k step7` |
| 8 | —（不用填） | 三张表整跑：柯西定理、复合闭路、$\ln z$ 的分支 | `-k step8` |

---

## 四、逐步做

### 第 1 步 · 把圆周采样成点列

数值积分只认「一串点」，不认「$\lvert z\rvert=2$」这种写法。正向圆周的第 $k$ 个点是

$$ z_k=\text{center}+\text{radius}\cdot e^{i\,2\pi k/n},\qquad k=0,1,\dots,n-1 . $$

**坑一：末点不要重复写。** 列表里只放 $n$ 个点，最后一个点与第一个点**差一步**；首尾相接那一段归第 3 步。
断言查 `len(pts) == n`，也查「末点不等于首点」。

**坑二：方向不用加符号。** $k$ 递增时角跟着递增，点自己逆时针转；写成 `-2j*math.pi*k/n` 就是顺时针，
`-k step1` 会当场指出方向反了（判据是第一次迈步的辐角必须为正）。

写完后 `python test_cauchy_lab.py -k step1`，应看到 `OK`（5 个测试）。

### 第 2 步 · 沿点列累加

$$ \int_C f\,dz\approx\sum_{k=0}^{m-2} f(z_k)\,\bigl(z_{k+1}-z_k\bigr). $$

这就是定积分定义那个和式：每小段用**左端点**的函数值乘上这一段的 $\Delta z$。开路径只求和到倒数第二个点为止
——最后一个点没有「下一段」，这一步不管它。

断言用 $f(z)=z$ 在点列 `[0, 1, 2]` 上把这条契约钉死：左端点式得 $0\cdot1+1\cdot1=1$；写成右端点会得 $3$。

### 第 3 步 · 闭合起来（柯西定理的数值版）

与第 2 步只差一段：`points[-1] → points[0]` 也要算进去。

```python
total = 0j
n = len(points)
for k in range(n):
    total += f(points[k]) * (points[(k + 1) % n] - points[k])
```

跑出来的数与纸面结论对得上（参考解，$n=4096$）：

| 被积函数 / 围道 | 数值结果 | 纸面结论 |
|---|---|---|
| $z^2$ 沿 $\lvert z\rvert=1$ | $1.8\times10^{-15}$ | $0$（解析） |
| $e^z$ 沿 $\lvert z-(1+i)\rvert=2$ | $10^{-14}$ 量级 | $0$（解析） |
| $\dfrac{1}{z-2}$ 沿 $\lvert z\rvert=1$ | $3.8\times10^{-15}$ | $0$（奇点在圈外，圈内解析） |
| $\dfrac1z$ 沿 $\lvert z\rvert=2$ | $-0.0048+6.28318i$ | $2\pi i$（奇点在圈内） |

前三行「抵得干净」：解析就有原函数，和式望远镜式抵消，只剩浮点噪声。

第四行抵不干净，但不是错：$2\pi i=6.2831853i$，代码给的是 $6.2831828i$，**实部还留着 $-0.0048$**。
这点残渣是折线代替圆弧的误差（$O(1/n)$，$n=4096$ 时约 $-4.8\times10^{-3}$）——所以判零必须带容差（下一步）。

**还有一条断言值得看**：故意「不闭合」去算 $z^2$（就是 `-k step3` 里的 `missing_wrap`），结果到了
$10^{-2}$ 量级，不再是 $0$。闭合那一步不是装饰。

### 第 4 步 · 判零要带容差

卷面上写「$=0$」，代码里要写 `abs(value) <= tol`。文件顶上有两个容差，分工不同：

- `TOL_ZERO = 1e-6`：判「是 $0$」用。柯西定理那几行的噪声只有 $10^{-15}$～$10^{-14}$，容差收得紧也安全；
- `TOL_VALUE = 2e-2`：判「等于 $2\pi i$ / $\pi i$」用。折线代替圆弧的残渣有 $10^{-3}$ 量级。

容差要写成参数（`tol=...`），别硬编码：第 8 步整表三个档都要用，`-k step4` 的第三条断言查的就是
「`tol` 传大了就该判成 $0$」。

### 第 5 步 · 挖洞：外圈正向 + 内圈反向

圆环 $r_{\text{in}}<\lvert z-\text{center}\rvert<r_{\text{out}}$ 上取复合闭路：
外圈逆时针、内圈**顺时针**。沿这条合成围道走的积分，等于外圈那个积分**减去**内圈（正方向）那个积分：

$$ \oint_{\Gamma} f\,dz=\oint_{\text{外圈}}f\,dz-\oint_{\text{内圈}}f\,dz . $$

参考解在 $n=1024$ 上实测（$f=\dfrac1z$，圆环 $1<\lvert z\rvert<2$，洞把原点让出去）：

```term
外圈 |z|=2 正方向  ->  (-0.0192765+6.2831459j)
内圈 |z|=1 正方向  ->  (-0.0192765+6.2831459j)      ← 两个都约等于 2πi
复合闭路（外 − 内） ->  0j                          ← 抵得干干净净
```

**这一步最常错的就是那一项符号**：写成「外圈 + 内圈」会得到 $-0.0386+12.5663i$，差不多是 $4\pi i$——
一眼就该看出不对（复合闭路围出的圆环里 $f$ 处处解析，答案只能是 $0$）。这正是卷面上「内圈漏反向」丢分的地方。

另外两条断言换了洞：$f=\dfrac{1}{z-0.5}$（奇点 $0.5$ 落在洞里）与 $f=\dfrac{1}{z-2}$、圆心挪到 $2$
（奇点就是圆心自己）——复合闭路都还是 $0$。挖洞要看的只有一件事：**奇点被圈进洞里了吗**。
进了洞，圆环上就处处解析，复合闭路给 $0$；奇点要是掉在圆环上，两圈都不解析，这条等式根本不成立。

### 第 6 步 · 圆弧

$n$ 段弧要有 $n+1$ 个点（首末两端都要），角从 $\theta_0$ 均匀走到 $\theta_1$；$\theta_1<\theta_0$ 就是反着走。

`range(n + 1)` 别写成 `range(n)`：少了末点，弧就断在 $\theta_1$ 前面一小段，第 7 步会差一点点。
反向那条断言把「正向弧倒着读」与「把两个角对调」逐点比了一遍，两者必须一模一样。

### 第 7 步 · 弧上积分（顺带验一次 $\ln z$ 的分支）

套一下就有了。$\dfrac1z$ 沿单位圆从 $1$ 走到 $-1$（参考解，$n=4096$）：

| 走法 | 数值结果 | 纸面结论 |
|---|---|---|
| 上半圈（$\arg z$ 从 $0$ 增到 $\pi$） | $-0.0012+3.14159i$ | $\pi i$ |
| 下半圈（$\arg z$ 从 $0$ 减到 $-\pi$） | $-0.0012-3.14159i$ | $-\pi i$ |

同一对端点、两条路，差 $2\pi i$。这就是课上「同一对端点换一支 $\ln z$，答案差 $2\pi i$」那段的数值版：
不是积分算错了，是 $\arg z$ 走了**另一支**。

### 第 8 步 · 整表自检（不用填）

`-k step8` 把三张表跑一遍：

- **柯西定理表**：$z^2$、$e^z$、$\sin z$、$\dfrac{1}{z-2}$ 沿 $\lvert z\rvert=1$ 都是 $0$；
  $\dfrac1z$ 是 $2\pi i$；$\bar z$ 是 $2\pi i$；$\operatorname{Re} z$ 是 $\pi i$。
- **复合闭路表**：外圈 $2\pi i$、内圈 $2\pi i$、复合闭路 $0$。
- **分支表**：上半圈 $\pi i$、下半圈 $-\pi i$，两者差 $2\pi i$。

三张表全绿，说明你代码里的「$0$ / $2\pi i$ / $\pi i$」与卷面判断是同一套东西——这就是这一步的交付证据。

---

## 五、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`期望 X，实际 Y（差 Z）`。差符号、差一个 $2\pi i$、差 $n$ 倍，都在那一行看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 第二点朝下（`phase` 为负） | 角写成 `-2j*pi*k/n`，采样成顺时针 |
   | step1 `len` 是 $n+1$ / 末点等于首点 | 在圆周上用了 `range(n + 1)`，首点重复了 |
   | step2 得 $3$ 而不是 $1$ | 被积函数值取在了右端点（`points[k+1]`） |
   | step3 $z^2$ 得到 $10^{-2}$ 量级 | 漏了闭合（`(k+1) % n`），末点没接回首点 |
   | step3 $\dfrac1z$ 模对、实部差一点点 | 正常：折线代替圆弧的残渣，约 $-4.8\times10^{-3}$（$n=4096$） |
   | step3 结果差一个负号 | 采样成了顺时针，或 `points[(k+1) % n] - points[k]` 写反 |
   | step4 全是 `False` | 容差写成 `== 0`，或 `tol` 传成了 0 |
   | step5 复合闭路得 $4\pi i$ | 内圈没反向，写成了 `outer + inner` |
   | step5 复合闭路得 $2\pi i$ | 内圈漏算，只返回了外圈那一个 |
   | step7 上半圈得 $-\pi i$ | $\theta$ 走反了：$\theta_1$ 应为 $+\pi$ |
   | step8 $\bar z$ 或 $\operatorname{Re}z$ 也是 $0$ | 被积函数写成了 $z$——不解析的函数不该被抵成 $0$ |

3. **还不对，再看参考解**：`solutions/0010-cauchy-closed-contour/cauchy_lab.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（第 8 步验的是「三张表对不对」，
   整段拷会让你跳过判断过程）。

参考解那一步为什么这样写，`solutions/0010-cauchy-closed-contour/README.md` 里有逐条说明。

---

## 六、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0010-cauchy-closed-contour\cauchy_lab.py .    # Windows
$ python test_cauchy_lab.py
...
Ran 30 tests in 0.013s

OK
```

**先自己全绿、再对照**：直接拷参考解会跳过判断过程，第 8 步验的正是「你能不能说清什么是 $0$、
什么不是 $0$」。

---

## 七、和后面几课的关系

- 实验四（围道上的留数）要画「围道 + 极点」，用的就是本节的 `circle_contour` 与 `composite_integral`；
- 留数定理那一课说 $\oint_C f\,dz=2\pi i\sum\operatorname{Res}$，本节先把求和里只有一项时
  （$\dfrac1z$ 那种）对上；
- 课上那张「三条路怎么选」的选型卡，本节这四个函数正好各管一行：解析 → `closed_integral` 得 $0$；
  圈里有奇点 → `composite_integral` 挖洞；开路径 → `contour_integral`；分支不定 → `arc_integral`
  分两支各算一次。


---

# 第 12 课 · 展开系数核对器（0012-laurent-coeff-tool）

上面几节分别是第 5 课（CR 检查器）、实验一、实验二、第 9 课（柯西积分公式）与第 10 课
（柯西积分定理与复合闭路）。本节是第 12 课「泰勒级数与洛朗级数」的小 lab，跟哪一节都不互相依赖：
各用各的目录、各跑各的测试。

第 9 课验的是「围道积分算出来的值对不对」，这一节验的是**展开系数**：把

$$ c_k=\frac{1}{2\pi i}\oint_C\frac{f(\zeta)}{(\zeta-z_0)^{k+1}}\,d\zeta $$

沿环域里的一条圆周真积一遍，再拿卷面上写出来的 $\sum c_n(z-z_0)^n$ 去对照。
系数对上，那道 10 分大题就多一层保险；抄串环域、漏掉负幂部分，围道积分当场不认。

工具要做的事一句话：**把卷面那四步（定环域 → 拆部分分式 → 凑几何级数 → 合并系数）写成代码，
让围道积分去验它。**

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `laurent_tool.py` 里 8 个留白函数 | `lab/0012-laurent-coeff-tool/laurent_tool.py` | `python test_laurent_tool.py` 打出 `OK`（29 条断言） |
| 一张三条环域的系数对照卡（纸笔，不用交文件） | 手边 / 纸笔题型整理册 | 第 8 步填完后能十秒内说出 $|z|<1$、$1<|z|<2$、$|z|>2$ 三套系数各长什么样 |

`out/`、CSV、图都不用交——这一节只产代码。

## 二、环境依赖

**只要 Python 3.8+，只用标准库（`cmath`、`math`、`unittest`），不装任何第三方包。**

- 复数是内置类型 `complex`，$1j$ 就是虚数单位，$e^{i\theta}$ 写 `cmath.exp(1j * theta)`；
- $2\pi i$ 写成 `2j * math.pi`（文件里已经给成 `TAU_I`）——这样不会把 $i$ 丢掉；
- 测试用内置 `unittest`，`python test_laurent_tool.py` 直接跑。

本机实测两个解释器都能跑同一份代码：`D:/Program Files/Python313/python.exe`（Python 3.13.15，
只有标准库）与带 numpy 的
`C:\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`
（Python 3.12.14 + numpy 2.3.5），两边都是 `Ran 29 tests … OK`。这一节用不到 numpy，
命令里的 `python` 换成本机任意一个 3.8+ 都可以。

## 三、目录

```
lab/
├── README.md                              ← 本文件（第 5 课 + 实验一 + 实验二 + 第 9/10/12 课）
├── 0012-laurent-coeff-tool/
│   ├── laurent_tool.py                    ← 你要填的 8 个函数（留白）
│   └── test_laurent_tool.py               ← 29 条断言，自动判分
└── solutions/
    └── 0012-laurent-coeff-tool/
        ├── laurent_tool.py                ← 参考解（做完才看）
        └── README.md                      ← 每一步为什么这样写、常见错法与实测值
```

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0012-laurent-coeff-tool
$ python test_laurent_tool.py
```

现在（还没动手）会是这样——29 个 ERROR，**退出码 1**：

```term
$ python test_laurent_tool.py
test_step1_count_and_radius (__main__.Step1_围道采样.test_step1_count_and_radius) ... ERROR
test_step1_counterclockwise (__main__.Step1_围道采样.test_step1_counterclockwise) ... ERROR
...
NotImplementedError: 第 1 步还没写：contour_points —— 见 lab/README.md 任务表第 1 行
...
Ran 29 tests in 0.005s

FAILED (errors=29)
```

最后那行 `FAILED (errors=29)` 是重点：**留白态必须是不通过的**，退出码 1
（PowerShell 里紧接着跑 `echo $LASTEXITCODE` 能看到 1）。

八步填完、跑出下面这两行，就算做完（退出码 0）：

```term
$ python test_laurent_tool.py
...
Ran 29 tests in 0.024s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_laurent_tool.py -k step3
...
Ran 3 tests in 0.002s

OK
```

`-k` 后面**大小写要照写**（`step3` 能选中，`Step3` 也行，写成 `steps3` 就是 `NO TESTS RAN`、退出码 5）。

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `contour_points` | 环域内绕 $z_0$ 一圈的圆周上等距的 $n$ 个点（逆时针） | `-k step1` |
| 2 | `coeff_integral` | 单个系数 $c_k=\frac{1}{2\pi i}\oint\frac{f(\zeta)}{(\zeta-z_0)^{k+1}}d\zeta$（$k$ 可为负） | `-k step2` |
| 3 | `coeffs` | 一次算一组 $k$ 的系数，返回 `{k: c_k}` | `-k step3` |
| 4 | `series_value` | 拿系数表在 $z$ 处求和（正幂负幂一起算） | `-k step4` |
| 5 | `truncation_error` | 有限项截断误差 $\lvert S(z)-f(z)\rvert$ | `-k step5` |
| 6 | `partial_fractions` | $\frac{1}{(z-a)(z-b)}=\frac{A}{z-a}+\frac{B}{z-b}$ 的两个权重 | `-k step6` |
| 7 | `geom_coeffs` | $\frac{1}{z-a}$ 的两支系数（$\lvert z\rvert<\lvert a\rvert$ 与 $\lvert z\rvert>\lvert a\rvert$） | `-k step7` |
| 8 | `ring_coeffs` | 环域里 $\frac{1}{(z-a)(z-b)}$ 的整套系数（环域名取 `inner`/`middle`/`outer`） | `-k step8` |
| 9 | —（不用填） | 把课件那三条展开 + 真题两问整表跑一遍 | `-k step9` |

文件里已经写好的两个小工具是 `closed_range` 与 `f_lesson`（例题 $f(z)=\frac{1}{(z-1)(z-2)}$），
常数是 `TAU_I`、`DEFAULT_N`——照它们的用法往下填，**别改**。

## 六、逐步做

### 第 1 步 · 围道采样

$$ \zeta_k=z_0+r\,e^{i\theta_k},\qquad \theta_k=\frac{2\pi k}{n},\ k=0,1,\dots,n-1 . $$

从 $z_0+r$ 出发、逆时针走一圈，就是「正向简单闭曲线」。围道要**绕在环域里面**：第 2 步的系数
就在这条圆上积出来。

$n$ 取 512 不是凑数：梯形法对圆周上的解析被积函数收敛极快，误差按 $(d/r)^n$ 掉（$d$ 是离圆心最近的
奇点距离）。实测中间环域 $1<|z|<2$（$r=1.5$、$d=1$）的 $c_1$：$n=16$ 误差 $4.1\times10^{-3}$、
$n=32$ 是 $2.7\times10^{-5}$、$n=64$ 是 $2.5\times10^{-9}$、$n=128$ 已经到 $10^{-16}$。

**两个坑**：忘了乘 `radius`（点全落在圆心，第 2 步马上 `ZeroDivisionError`）；角度写成
$-2\pi k/n$（整圈顺时针，第 2 步的系数全体变号，$c_0$ 得 $-0.5$ 而不是 $0.5$）。

写完后 `python test_laurent_tool.py -k step1`，应看到 `OK`（3 个测试）。

### 第 2 步 · 系数积分（这一步最容易错）

$$ c_k=\frac{1}{2\pi i}\oint_C\frac{f(\zeta)}{(\zeta-z_0)^{k+1}}\,d\zeta . $$

围道换了参数，$dz$ 也得跟着换：

$$ \zeta=z_0+r e^{i\theta}\ \Longrightarrow\ dz=i\,r\,e^{i\theta}\,d\theta=i\,\Delta\theta\,(\zeta-z_0),
\qquad \Delta\theta=\frac{2\pi}{n}. $$

所以每一项是 `f(z) / (z - center) ** (k + 1) * (1j * dtheta * (z - center))`，$n$ 项加起来再除以 `TAU_I`。

$k$ 可以是负数：$k=-1$ 时分母是 $(\zeta-z_0)^0=1$，这就是后面留数要用的 $c_{-1}$；$k=-2$ 是
$(\zeta-z_0)^{-1}$，负幂项正是这样一项项积出来的。

**三个坑，断言各抓一个**（括号里是实测值）：

1. **$dz$ 只写 $\Delta\theta$**：$c_1$ 得 `0.0`，全套系数都是 0——被积函数对了，微分丢了。
2. **漏掉 $(\zeta-z_0)$**（写成 $i\,\Delta\theta$）：$c_0$ 得 `0.75`、$c_1$ 得 `0.875`，正确是 `0.5`、`0.75`。
   这是第 8 课「$dz$ 忘了换元」那个坑的同一处。
3. **分母用 $2\pi$ 而不是 $2\pi i$**：结果整体转 $90°$，$c_0$ 得 `0.5j`（模对、方向错）。

### 第 3 步 · 一组系数

只是循环：`{k: coeff_integral(f, k, center, radius, n) for k in ks}`。键就是传入的那几个整数
（负号也要带着），**别在这里改默认的 $n$**——半径给错了，负幂项会整个消失。

写下这三个数自己核对：中间环域 $1<|z|<2$ 取 $r=1.5$，得 $c_0=-1/2$、$c_1=-1/4$、$c_{-1}=c_{-2}=-1$。

### 第 4 步 · 级数求和

$$ S(z)=\sum_k c_k\,(z-z_0)^k , $$

正幂负幂一起算——$1<|z|<2$ 那条展开本来就一半正幂一半负幂，只算一半是验不出东西的。
Python 里负幂直接写 `(z - center) ** k`（$k$ 为负时它会照算），不用自己取倒数。空系数表返回
`0`，不是 `None`。

### 第 5 步 · 截断误差

$$ \bigl|S(z)-f(z)\bigr| . $$

这一步把「项数够不够」量出来。实测（$e^z$ 的麦克劳林系数，$z=1$ 处）：

| 取到第几项 | 误差 |
|---|---|
| $n=2$（到 $1/2!$） | $2.2\times10^{-1}$ |
| $n=5$ | $1.6\times10^{-3}$ |
| $n=8$ | $3.1\times10^{-6}$ |
| $n=11$ | $2.3\times10^{-9}$ |

同一个函数，系数表换成 $|z|>2$ 那条负幂展开、在 $z=3$ 处回代：取 40 项时误差 $9.0\times10^{-8}$，
因为负幂那一支的项按 $(2/3)^n$ 掉。**同一张系数表出了自己的环域就发散**，这也是「每一条展开只在
它自己的环域内成立」的数值形态。

### 第 6 步 · 部分分式

$$ \frac{1}{(z-a)(z-b)}=\frac{A}{z-a}+\frac{B}{z-b},\qquad A=\frac{1}{a-b},\ B=\frac{1}{b-a}. $$

做法就是「遮住一个因式、把那个根代进去」：遮住 $z-a$、令 $z=a$，右边只剩 $A$。
**权重跟着 $a$、$b$ 走**：交换 $a$、$b$ 时两个权重跟着换（断言专门传了一次 `(2, 1)`）。
漏掉负号的话，三点恒等式在 $z=0.3$ 处差 `1.68`——正是两倍的 $1/((z-1)(z-2))$。

### 第 7 步 · 几何级数系数（两支）

$$ \frac{1}{z-a}=
\begin{cases}
-\dfrac{1}{a}\cdot\dfrac{1}{1-z/a}=-\displaystyle\sum_{n\ge0}\frac{z^n}{a^{n+1}}, & |z|<|a|,\\[2mm]
\dfrac{1}{z}\cdot\dfrac{1}{1-a/z}=\displaystyle\sum_{n\ge0}\frac{a^n}{z^{n+1}}, & |z|>|a|.
\end{cases} $$

所以系数表只有一支非零：`inside=True` 时 $c_n=-a^{-(n+1)}$（$n\ge0$）；否则 $c_{-n-1}=a^n$（$n\ge0$）。

**判据始终是 $|z|$ 与 $|a|$ 谁大**，写反了第 8 步三个环域全串。$a=2$ 的两支实测：

| 支 | 前四项系数 |
|---|---|
| $\lvert z\rvert<2$（提常数） | $c_0=-\tfrac12$、$c_1=-\tfrac14$、$c_2=-\tfrac18$、$c_3=-\tfrac1{16}$ |
| $\lvert z\rvert>2$（提 $1/z$） | $c_{-1}=1$、$c_{-2}=2$、$c_{-3}=4$、$c_{-4}=8$ |

第 7 步还有一条交叉验证：`geom_coeffs(2, True, 2)` 与围道积分算出来的
$\frac{1}{z-2}$ 的 $c_0,c_1,c_2$ 要逐项对上——纸面与数值互证，是这一节的核心动作。

### 第 8 步 · 环域系数（卷面四步的代码版）

`ring` 三个值，按奇点到原点的距离分级（$a$、$b$ 谁近谁远由 $|a|$、$|b|$ 自己比）：

| `ring` | 环域 | 两项各走哪一支 |
|---|---|---|
| `'inner'` | $\lvert z\rvert<\lvert a\rvert<\lvert b\rvert$ | 都提常数（只有正幂） |
| `'middle'` | $\lvert a\rvert<\lvert z\rvert<\lvert b\rvert$ | 近的那项提 $1/z$，远的那项提常数 |
| `'outer'` | $\lvert z\rvert>\lvert b\rvert$ | 都提 $1/z$（只有负幂） |

先拆部分分式拿两个权重，再对每个奇点取第 7 步的系数表、乘权重、**按 $k$ 累加**进同一张表——
同一个幂次是两项相加，不是覆盖。实测 $f(z)=\frac{1}{(z-1)(z-2)}$ 的三个环域：

| 环域 | 系数（前几项） |
|---|---|
| $\lvert z\rvert<1$ | $c_0=\tfrac12$、$c_1=\tfrac34$、$c_2=\tfrac78$、$c_3=\tfrac{15}{16}$ |
| $1<\lvert z\rvert<2$ | $c_{-1}=c_{-2}=-1$；$c_0=-\tfrac12$、$c_1=-\tfrac14$ |
| $\lvert z\rvert>2$ | $c_{-1}=0$、$c_{-2}=1$、$c_{-3}=3$、$c_{-4}=7$ |

**两个坑**：假设 `a` 更近（写成「`a` 提常数、`b` 提 $1/z$」也能过 `(1, 2)` 那几条，一传 `(2, 1)` 就错）；
同幂次用 `=` 覆盖（`outer` 的 $c_{-3}$ 会得 $-1$ 或 $4$，正确是 $-1+4=3$）。

### 第 9 步 · 整表自检（不用填）

`-k step9` 跑两张表，每张都是「纸面公式 vs 围道积分」：

| 表 | 内容 |
|---|---|
| 课件三条展开 | $\lvert z\rvert<1$：$c_n=1-2^{-(n+1)}$；$1<\lvert z\rvert<2$：$c_0=-\tfrac12$、$c_n=-2^{-(n+1)}$、$c_{-n}=-1$；$\lvert z\rvert>2$：$c_{-n}=2^{n-1}-1$ |
| 合肥工大卷 10 分题 | $f(z)=\frac{z+1}{(z-1)^2}$：$0<\lvert z\rvert<1$ 里 $c_0=1$、$c_n=2n+1$；$\lvert z\rvert>1$ 里 $c_{-1}=1$、$c_{-m}=2m-1$ |

它全绿，说明你的工具和纸面结论对上了——这就是这一节的交付证据。

## 七、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`期望 X，实际 Y`。两个数一比，差符号、差因子、差一个 $i$、差一位幂次，都看得出来。
2. **按症状对表**（右列数值是实测值，不是估计）：

   | 症状 | 大概率是 |
   |---|---|
   | step1 / step2 抛 `ZeroDivisionError` | `contour_points` 忘了乘 `radius`，点全在圆心 |
   | step2 全部系数都是 `0` | $dz$ 只写了 $\Delta\theta$，微分没换元 |
   | step2 $c_0$ 得 `0.75`、正确 `0.5` | $dz$ 漏了 $(\zeta-z_0)$ 那一段 |
   | step2 系数是纯虚数（$c_0$ 得 `0.5j`） | 分母写了 $2\pi$，应为 $2\pi i$（`TAU_I`） |
   | step2 系数全体变号 | 围道顺时针了，角度写成 $-2\pi k/n$ |
   | step3 负幂项全是 `0`、正幂项却对 | 半径取到了奇点外面（比如中间环域用 $r=0.5$） |
   | step3 / step9 差 $10^{-5}$ 量级 | `DEFAULT_N` 被改小了，采样不够（见第 1 步那张表） |
   | step4 抛 `TypeError` | 系数表空时返回了 `None`，应返回 `0` |
   | step6 三点恒等式差一个符号 | 两个权重对调了，或漏了负号 |
   | step7 / step8 三个环域全串 | 第 7 步两支写反了：`|z|<|a|` 才提常数 |
   | step8 `outer` 的 $c_{-3}$ 得 `-1` 或 `4` | 同幂次覆盖了，应相加（正确 `3`） |
   | step8 传 `(2, 1)` 才错 | 没有先按 $\lvert a\rvert$、$\lvert b\rvert$ 排谁近谁远 |

3. **还不对，再看参考解**：`solutions/0012-laurent-coeff-tool/laurent_tool.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（第 9 步验的是整表，整段拷会让你跳过判断过程）。

参考解那一步为什么这样写，`solutions/0012-laurent-coeff-tool/README.md` 里有逐条说明。

## 八、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0012-laurent-coeff-tool\laurent_tool.py .    # Windows
$ python test_laurent_tool.py
...
Ran 29 tests in 0.024s

OK
```

**先自己全绿、再对照**：直接拷参考解会跳过判断过程，第 9 步验的正是「你的系数和纸面公式对不对得上」。

## 九、和后面几课的关系

- **第 13 课（奇点分类：零点与极点）**要按洛朗展开的负幂项分组判断奇点类型，第 8、9 步的系数表
  就是「负幂部分到第几项」的直接答案；
- **第 14 课（留数与留数定理）**只要一个数：`coeff_integral(f, -1, z0, r)` 就是 $c_{-1}$，
  也是以奇点为心展开时的留数；
- **实验四（围道上的留数）**要把围道画出来、把极点标在图上，`contour_points` 与 `ring_coeffs`
  这两件东西照用。

---

# 实验三 · 保角映射的网格实验（0007-mapping-grid）

上面几节是这门课已经做过的几个小 lab（第 5 课的 CR 检查器、实验一、实验二、第 9 课、第 10 课、
第 12 课），各用各的目录、各跑各的测试。本节是**实验三**，它验收的那句话是：
**做出 $z^2$、$e^z$、$1/z$ 的网格变形图，指出直角是否被保持。**

它接在实验二后面长，不从零开始：

- 实验二问「导数存不存在」，本课问「导数的几何意义长什么样」——同一条导数，换个问法；
- 采点、逐点算一个数、存成 CSV、用字符画看形状，这一整套流程与实验一、实验二完全一致；
- 实验二的 `jacobian` 在这里换成「十字夹角」：$\det J=\lvert f'(z)\rvert^2$ 为零的点，
  就是本课量出 180° 的那个点。

三个目录各跑各的测试，互不依赖：`cr_tool.py`、`gallery.py`、`analytic_gallery.py` 都别删，
也不要改。

---

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `mapping_grid.py` 里 9 个留白函数 | `lab/0007-mapping-grid/mapping_grid.py` | `python test_mapping_grid.py` 打出 `OK`（38 条断言） |
| `out/curves-z2.csv`、`out/curves-exp.csv`、`out/curves-inv.csv` | `lab/0007-mapping-grid/out/` | 每份 450 行（$2$ 族 × $9$ 条 × $25$ 点），列是 `family,line,k,re,im` |
| `out/zoom-z2-origin.csv` | 同上 | $z^2$ 在原点附近的局部放大网格，也是 450 行 |
| `out/angles.csv` | 同上 | 10 行结论表：每行一个测点，含夹角、偏差、伸缩率、判定 |
| 三句结论（写进 notebook，或直接回话） | — | 见第七节末，三条各一句 |

`out/` 里的 CSV 就是「网格变形图」与「结论表」的数据：没有 matplotlib 也能把它们交出来，
图只是数据的另一种画法（第七节给了只用标准库的字符画）。

## 二、环境依赖

**只要 Python 3.8+，只用标准库（`cmath` / `csv` / `math` / `unittest`）**，不装任何第三方包。

- numpy **不需要**（这一课没有需要向量化的步骤：450 个点的双层循环跑完不到 0.1 秒）；
- matplotlib 与 Jupyter **完全不需要**：交付物是 CSV，画图是可选的第八节。

本机实测的两个解释器：`D:/Program Files/Python313/python.exe`（3.13.15，只有标准库）与
bundled runtime（3.12.14 + numpy 2.3.5）。命令里的 `python` 按你自己的环境换。

## 三、目录

```
lab/
├── README.md                            ← 本文件：各节合集（每节末尾都写着「和别节的关系」）
├── 0005-cr-check-tool/                  ← 第 5 课：CR 检查器
├── 0003-gallery/                        ← 实验一：方根与迭代图
├── 0006-analytic-gallery/               ← 实验二：解析性对照
├── 0009-cauchy-formula-tool/            ← 第 9 课：柯西公式核对
├── 0010-cauchy-closed-contour/          ← 第 10 课：复合闭路
├── 0012-laurent-coeff-tool/             ← 第 12 课：展开系数核对
├── 0007-mapping-grid/                   ← 本课（实验三）
│   ├── mapping_grid.py                  ← 你要填的 9 个函数（留白）
│   ├── test_mapping_grid.py             ← 38 条断言，自动判分
│   └── out/                             ← 自检写出五份数据
└── solutions/
    ├── 0005-cr-check-tool/
    ├── 0003-gallery/
    ├── 0006-analytic-gallery/
    ├── 0009-cauchy-formula-tool/
    ├── 0010-cauchy-closed-contour/
    ├── 0012-laurent-coeff-tool/
    └── 0007-mapping-grid/
        ├── mapping_grid.py              ← 参考解（做完才看）
        └── README.md                    ← 九个函数为什么这样写、常见错法、实测数据
```

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0007-mapping-grid
$ python test_mapping_grid.py
```

现在（还没动手）会是这样——38 条全是 ERROR，**退出码 1**：

```term
$ python test_mapping_grid.py
...
NotImplementedError: 第 1 步还没写：segment_points —— 见 lab/README.md 任务表第 1 行
...
Ran 38 tests in 0.008s

FAILED (errors=38)
```

九步填完、跑出下面这两行，数值这一半才算做完（退出码 0）：

```term
$ python test_mapping_grid.py
...
Ran 38 tests in 0.010s

OK
```

只验某一步（填一步验一步，别一次填完）：`python test_mapping_grid.py -k step5`。
`-k` 后面写测试名里的一段：`step1` … `step9`、`selfcheck`。

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验（条数） |
|---|---|---|---|
| 1 | `segment_points` | 线段 $a\to b$ 上等距的 $n$ 个点（含两端） | `-k step1`（3） |
| 2 | `grid_lines` | 铺参数网格：竖线族 $x$ 固定、横线族 $y$ 固定 | `-k step2`（4） |
| 3 | `map_grid` | 整张网格逐点送过去（形状不变） | `-k step3`（4） |
| 4 | `angle_between` | 两个向量的夹角（**度**），零向量给 `None` | `-k step4`（4） |
| 5 | `cross_angle` | 局部十字的像的夹角——直角还在不在的直接测量 | `-k step5`（4） |
| 6 | `angle_defect` | 夹角离 90° 差多少度（`is_conformal` 已经给好） | `-k step6`（4） |
| 7 | `derivative_at` | 数值导数 $f'(z_0)$：模是伸缩率、辐角是旋转角 | `-k step7`（4） |
| 8 | `critical_points` | 网格点里 $\lvert f'(z)\rvert\approx0$ 的那些（临界点） | `-k step8`（3） |
| 9 | `save_curves_csv`、`save_angles_csv` | 网格数据与结论表存成 CSV | `-k step9`（4） |
| — | 不用填 | 整块自检：三张网格 + 十行结论表，写出 `out/` 五份 | `-k selfcheck`（4） |

已经写好的六个样例（`f_sq`、`f_exp`、`f_inv`、`MAPPINGS`、`is_conformal` 与那几个常量）
照它们的用法往下填，**别改**：第 5、7、8 步的断言按它们算。

## 六、逐步做

### 第 1 步 · 线段铺点

$$ z_k=a+(b-a)\frac{k}{n-1},\qquad k=0,1,\dots,n-1 . $$

**唯一容易错的地方**是分母：写 $k/n$ 时最后一个点只走到全程的 $\dfrac{n-1}{n}$，网格右边永远
差一截。图上看不出来（只是「小了点」），第 3 步一逐点比对就露。$n<2$ 要抛 `ValueError`。

写完后 `python test_mapping_grid.py -k step1`，应看到 `OK`（3 个测试）。

### 第 2 步 · 铺参数网格

竖线族：$x=c$ 逐条，每条从 $(c,\ \text{im\_min})$ 走到 $(c,\ \text{im\_max})$；
横线族：$y=d$ 逐条，每条从 $(\text{re\_min},\ d)$ 走到 $(\text{re\_max},\ d)$。
两族都拿第 1 步的 `segment_points` 铺。

**两个坑**：两族各写一遍循环（其中一族的端点必然取错）；竖线方向反了（从 `im_max` 往下走），
第 5 步的十字会跟着反——图看不出问题，角度却从 90° 变成 270° 那一侧。

### 第 3 步 · 把整张网格送过去

这一步就是「网格变形」本身：$w=z^2$ 把直线送成抛物线，$w=e^z$ 送成圆与射线，
$w=1/z$ 送成过原点的圆。**形状不变量是「几条线、每线几点」**，代码里就是两层列表推导。

**唯一要忍住的地方**：不要 `try/except` 把 `1/z` 在原点处的 `ZeroDivisionError` 吞掉。
极点不在定义域里，网格踩上去就该抛——这就是「极点」这两个字的数值形态。

### 第 4 步 · 夹角（单位是度）

$$\cos\theta=\frac{v_xw_x+v_yw_y}{\lvert v\rvert\,\lvert w\rvert},\qquad \theta=\arccos(\cdots)\ \text{再换度}.$$

**两个坑**：忘了把余弦夹回 $[-1,1]$（浮点偶尔给 $-1.0000000000000002$，`acos` 抛
`ValueError`）；返回了弧度。零向量返回 `None`——$\lvert z\rvert^2$ 那种「虚部恒等于 0」的
情形就是靠这条兜住的（实验二的第 6 步踩过同一个坑）。

### 第 5 步 · 小十字：直角还在吗

在 $z_0$ 处取一个十字：两条臂 $z_0\to z_0+\delta$、$z_0\to z_0+i\delta$，它们本身成直角。
把它们**送过去**，量两条像的弦

$$ w_1=f(z_0+\delta)-f(z_0),\qquad w_2=f(z_0+i\delta)-f(z_0), $$

的夹角。保角的映射给 $90°$，$z^2$ 在原点给 $180°$。

**这一格是整节课的关键，也是「局部放大图」的数值版**：$\delta$ 就是放大倍数。
实测同一个 $\delta=10^{-4}$ 下：

| 打点 | 夹角 | 说明 |
|---|---|---|
| $z^2$ 在 $1+i$ | 90.0029° | 保角 |
| $z^2$ 在 $0$ | 180.0000° | 90° 被加倍，直角没了 |
| $e^z$ 在 $0$ 与 $1+i$ | 90.0029° | 保角（$e^z$ 的导数处处非零） |
| $1/z$ 在 $i$ | 89.9943° | 保角 |
| $1/z$ 在 $0.1+0.1i$ | 89.9427° | 极点旁边：伸缩率已到 50 倍，直角**还在** |

**$\delta$ 不能乱取**：它得比「到临界点的距离」小得多。$z^2$ 在 $0.01$ 处，$\delta=10^{-2}$
量出 116.5651°，$\delta=10^{-4}$ 就回到 90.2865°——前者是「放大不够」，不是「直角坏了」。

### 第 6 步 · 偏差与判据

$$\text{defect}=\lvert\theta-90°\rvert .$$

取绝对值（$84.5°$ 与 $95.5°$ 都不是直角），量不出夹角时返回 `90.0`（按「没了」算）。
`is_conformal` 已经给好：`defect <= 0.5` 就算直角还在。容差 0.5° 是有余量的——实测保角点的
偏差在 $3\times10^{-3}$ 到 $0.06$ 度，临界点是 $90$ 度，两边差四个数量级。

### 第 7 步 · 数值导数（伸缩率与旋转角）

$$ f'(z_0)\approx\frac{f(z_0+h)-f(z_0-h)}{2h},\qquad h=10^{-6}. $$

$|f'(z_0)|$ 是**伸缩率**，$\arg f'(z_0)$ 是**旋转角**——第 5 课 §1.4 那两句原话。
实测：$z^2$ 在 $2+i$ 处是 $4+2i$（伸缩率 $4.47$、旋转 $26.57°$）、$e^z$ 在 $0$ 处是 $1$、
$1/z$ 在 $i$ 处是 $1$、$1/z$ 在 $0.1+0.1i$ 处是 $50i$（伸缩率 $50$、旋转 $90°$）。
和 `cr_tool.py` 的 `d_dx` 是同一行代码，只是换了个名字。

### 第 8 步 · 临界点

就是「网格点里 $\lvert f'(z)\rvert\le10^{-9}$ 的那些」。实测：

| 映射 | 临界点 |
|---|---|
| $z^2$ | `[0j]`（原点正好是格点：第 5 条竖线 × 第 5 条横线） |
| $e^z$ | `[]`（导数处处非零） |
| $1/z$ | `[]`（导数 $-1/z^2$ 在窗口内没有零点） |

**这个列表与「量出 180° 的那些点」是同一批**：保角失效的点只有临界点。

### 第 9 步 · 两张表存盘

`save_curves_csv`：一行一个点，列 `family,line,k,re,im`，返回数据行数（$450$）。
`save_angles_csv`：一行一个测点，列 `map,z0,delta,angle_deg,defect_deg,stretch,verdict`。

**两个坑**：`open` 少了 `newline=""`（Windows 每行变两行）；偏差用四位小数（$2.9\times10^{-3}$
变 `0.0029`、$2.8\times10^{-5}$ 变 `0.0000`，跟「坏掉了」分不开，所以用 `"{:.6g}"`）。

### 整块自检（不用填）

`-k selfcheck` 跑三个映射、量十个测点，写出五份数据：

| 文件 | 内容 |
|---|---|
| `out/curves-z2.csv` | $z^2$ 的变形网格：两族抛物线 |
| `out/curves-exp.csv` | $e^z$ 的变形网格：同心圆 + 射线 |
| `out/curves-inv.csv` | $1/z$ 的变形网格：过原点的圆 |
| `out/zoom-z2-origin.csv` | 原点附近 $[-0.3,0.3]^2$ 的放大网格（像正好是整图的 $0.09$ 倍） |
| `out/angles.csv` | 十行结论表（下表） |

`out/angles.csv` 实测原样：

```text
map,z0,delta,angle_deg,defect_deg,stretch,verdict
z^2,1+1i,1e-04,90.0029,0.00286472,2.82843,保角
z^2,0,1e-04,180.0000,90,0,临界点：角度加倍
z^2,0,1e-02,180.0000,90,0,临界点：角度加倍
z^2,0.01,1e-02,116.5651,26.5651,0.02,偏差待核对：缩小 δ
z^2,0.01,1e-04,90.2865,0.286477,0.02,保角
e^z,0,1e-04,90.0029,0.00286479,1,保角
e^z,1+1i,1e-04,90.0029,0.00286479,2.71828,保角
1/z,i,1e-04,89.9943,0.00572958,1,保角
1/z,0.1+0.1i,1e-04,89.9427,0.0572671,50,保角
1/z,0.1+0.1i,1e-02,84.5474,5.45262,50,偏差待核对：缩小 δ
```

它全绿 + 这张表对得上，就是这一节的交付证据。

---

## 七、不装 matplotlib 也能看图

交付物是 CSV，但你还是想「看见」形状。把映射后的网格当字符画打出来就行，只要标准库：

```python
import mapping_grid as mg


def show(f, window, width=45, height=17, lines=13, points=120):
    v, h = mg.map_grid(f, mg.grid_lines(*window, lines, points))
    pts = [(w.real, w.imag) for fam in (v, h) for line in fam for w in line]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    canvas = [[" "] * width for _ in range(height)]
    for x, y in pts:
        col = int((x - x0) / (x1 - x0) * (width - 1))
        row = height - 1 - int((y - y0) / (y1 - y0) * (height - 1))
        canvas[row][col] = "#"
    print("\n".join("".join(line) for line in canvas))


for name, f, window in mg.MAPPINGS:
    print(name)
    show(f, window)
```

实测输出（$w=z^2$ 那一张，实部 $-1..1$、虚部 $-2..2$）：

```term
w = z^2
                      #
                 ##########
            #######      #######
        #####      ######      #####
     ####   ########    ########   ####
   ############    ######    ############
 ###########   ##############   ###########
##########  ####################  ##########
#############################################
#     ##  ########################  ##     #
##########  ####################  ##########
 ###########   ##############   ###########
   ############    ######    ############
     ####   ########    ########   ####
        #####      ######      #####
            #######      #######
                 ##########
                      #
```

两族抛物线：竖线 $x=c$ 送成 $u=c^2-\dfrac{v^2}{4c^2}$，横线 $y=d$ 送成 $u=\dfrac{v^2}{4d^2}-d^2$。
**格子全弯了，交点却仍是直角**——这就是「保角」和「变形」互不矛盾的样子。

把窗口换成 `ZOOM_WINDOW`（$[-0.3,0.3]^2$）再画，形状一模一样、只小一圈：$z^2$ 在原点附近是
二次的，像正好是整图的 $0.3^2=0.09$ 倍（实测实部 $-0.090..0.090$、虚部 $-0.180..0.180$）。
真正不正常的是原点那一处——两条坐标线的像都倒在实轴上。

五份数据出来后，**结论段三句话**（写进 notebook，或直接回话）：

1. $z^2$ 的网格是两族抛物线，$e^z$ 是同心圆加射线，$1/z$ 是过原点的圆——格子全被弯过，
   但弯不影响直角：这三张图的交点都还是 90°（`out/angles.csv` 里 `angle_deg` 全是 90 上下）。
2. 唯一量出 180° 的是 $z^2$ 的原点，而它正是唯一满足 $f'(z)=0$ 的点（`stretch` 那一列是 0）：
   **直角被保持 ⟺ 导数非零**；$1/z$ 在极点旁边伸缩率已到 50 倍，角度仍是 90°。
3. 「角度不对」有两种来源：缩小 $\delta$ 后收敛到 90° 的是放大不够（$z^2$ 在 0.01 处
   从 116.6° 收到 90.3°），钉在 180° 不动的是临界点——判据是「还收不收」，不是「差多少」。

---

## 八、装了 matplotlib 就画出来（可选）

```python
import matplotlib.pyplot as plt
import mapping_grid as mg

v, h = mg.map_grid(mg.f_sq, mg.grid_lines(*mg.SQ_WINDOW))
for line in v + h:
    plt.plot([w.real for w in line], [w.imag for w in line], lw=0.6, color="steelblue")
plt.gca().set_aspect("equal")
plt.title("w = z^2 把方格纸揉成两族抛物线")
plt.show()
```

把 `mg.f_sq` 换成 `mg.f_exp`（窗口换 `mg.EXP_WINDOW`）或 `mg.f_inv`（窗口换 `mg.INV_WINDOW`），
就是另外两张。`set_aspect("equal")` 不能省：不然直角会被画布比例压成别的角度——
那就成了「画图制造出来的不保角」，与函数无关。

## 九、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`AssertionError` 后面一般带着期望值与实际值。差 90°、差一个符号、
   差一个端点，都在那一行看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 最后一条线不在 `re_max` 上 | 参数用了 `k / n`，应写 `k / (n - 1)` |
   | step1 报 `ZeroDivisionError` | `n = 1` 时除的是 0，先抛 `ValueError` |
   | step2 竖线从 `im_max` 往下走 / 十字翻了个面 | 竖线方向反了，应自下而上 |
   | step2 同一族的点实部不相等 | 内层用了另一个下标，`x` 没固定住 |
   | step3 形状变成一维 / 少了一层 | 两层列表推导只写了一层 |
   | step3 得不到 `ZeroDivisionError` | 用 `try/except` 吞掉了（或把 0 换成了别的数） |
   | step4 抛 `ValueError: math domain error` | 余弦没夹回 $[-1,1]$ |
   | step4 直角量出 1.5708 | 返回的是弧度，没 `math.degrees` |
   | step5 $z^2$ 在原点量出 90° | 量的是**原像**的夹角（永远是 90°），要量像的弦 |
   | step5 保角点量出 116° 上下 | $\delta$ 比到临界点的距离还大，换小一号 |
   | step6 偏差是负的 | 忘了取绝对值 |
   | step6 `TypeError: NoneType` | 没处理「量不出夹角」的那条分支 |
   | step7 导数差 2 倍 | 分母写成 `h`，应为 `2 * h` |
   | step7 导数是个纯虚数 | 漏了 `2h` 里的实数性，或把 `1j` 加到了错的地方 |
   | step8 `1/z` 抛 `ZeroDivisionError` | 把原点放进了待查点集 |
   | step8 结果顺序乱 / 有重复 | 用了 `set` |
   | step9 文件里每行之间有空白行 | `open` 少了 `newline=""` |
   | step9 复数列写成 `(1+2j)` | 没拆成 `w.real` 与 `w.imag` |
   | step9 偏差列全是 `0.0000` | 用了四位小数，应换 `"{:.6g}"` |

3. **还不对，再看参考解**：`solutions/0007-mapping-grid/mapping_grid.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（自检验的是「你填完以后数据对不对」）。

参考解那一步为什么这样写、常见错法逐条列，`solutions/0007-mapping-grid/README.md` 里有。

## 十、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0007-mapping-grid\mapping_grid.py .    # Windows
$ python test_mapping_grid.py
...
Ran 38 tests in 0.010s

OK
```

**先自己全绿、再对照**。两者差别如果只在写法（列表推导还是 `for`），不用改；
如果差在端点、方向、$\delta$ 或格式精度，那就是你图和数据出错的根源。

## 十一、和前后几节的关系

- **实验二（解析函数长什么样）**：那里逐点验 CR 条件，`jacobian` 等于
  $u_xv_y-u_yv_x=\lvert f'(z)\rvert^2$。本课的「十字夹角 180°」与「`critical_points` 找到
  $z=0$」与「`jacobian` 等于零」是同一件事的三种量法。
  顺带一条对照：$\bar z$ 的十字夹角**也是 90°**（它只把方位翻了过来），所以「夹角没变」同样
  判不出解析——要判方向还得看 `jacobian` 的符号，这就是实验二那条「正交不等于解析」的几何版。
- **实验四（围道上的留数）**：那里的围道也是按参数采点（`circle_points`），把极点画在图上、
  把围道叠上去，用的就是本课「采点 → 送过去 → 存 CSV」这同一套流程。所以
  `mapping_grid.py` 与 `out/` 别删。

# 第 14 课 · 留数与留数定理的数值核对（0014-residue-contour）

上面几节分别是第 5 课（CR 检查器）、实验一、实验二、第 9 课与第 10 课。本节是第 14 课
「留数与留数定理」的小 lab，各节互不影响：各用各的目录、各跑各的测试。

前面第 9 课验的是**柯西公式**（分母幂次 → 求几阶导），这一节验的是**留数**：
把四条留数算法各写成函数，再拿 $\dfrac{1}{2\pi i}\oint_{|z-z_0|=\rho}f\,dz$
这个小圆上的数值围道积分当裁判。两种算法对得上，卷面上「算留数」那一步才叫真的会。

工具的用法一句话：**先按公式算出留数，再让数值围道积分去验它。**

---

## 一、要交出什么

| 交付物 | 落在哪 | 怎么算合格 |
|---|---|---|
| `residue_lab.py` 里 12 个留白函数 | `lab/0014-residue-contour/residue_lab.py` | `python test_residue_lab.py` 打出 `OK`（53 条断言） |
| 一张默写卡（纸笔，不用交文件） | 纸笔题型整理册 | 四种算法三十秒默完，见课件「上手做」第 1 条 |

`out/`、CSV、图都不用交——这一节只产代码。

## 二、环境依赖

**只要 Python 3.8+，只用标准库（`cmath`、`math`、`unittest`），不装任何第三方包。**

- 复数是内置类型 `complex`，`1j` 就是虚数单位，$e^{i\theta}$ 写 `cmath.exp(1j * theta)`；
- $2\pi i$ 写成 `2j * math.pi`（文件里已经给成 `TAU`）——这样不会把 $i$ 丢掉；
- 测试用内置 `unittest`，`python test_residue_lab.py` 直接跑。

本机实测两个解释器都能跑同一份代码：`D:/Program Files/Python313/python.exe`
（Python 3.13.15，只有标准库）与带 numpy 的
`C:\Users\Administrator\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe`
（Python 3.12.14），两边都是 `Ran 53 tests … OK`。命令里的 `python` 换成本机任意一个 3.8+ 都可以。

## 三、目录

```
lab/
├── README.md                              ← 本文件（各课各一节）
├── 0014-residue-contour/
│   ├── residue_lab.py                     ← 你要填的 12 个函数（留白）
│   └── test_residue_lab.py                ← 53 条断言，自动判分
└── solutions/
    └── 0014-residue-contour/
        ├── residue_lab.py                 ← 参考解（做完才看）
        └── README.md                      ← 每一步为什么这样写、常见错法
```

## 四、怎么算做完

进到任务目录，跑：

```term
$ cd lab/0014-residue-contour
$ python test_residue_lab.py
```

现在（还没动手）会是这样——53 个 ERROR，**退出码 1**：

```term
$ python test_residue_lab.py
test_selfcheck_contour_table (__main__.Selfcheck_整表自检...) ... ERROR
...
NotImplementedError: 第 9 步还没写：residue_pole_m —— 见 lab/README.md 任务表第 9 行
...
Ran 53 tests in 0.008s

FAILED (errors=53)
```

最后那行 `FAILED (errors=53)` 是重点：**留白态必须是不通过的**，退出码 1
（PowerShell 里紧接着跑 `echo $LASTEXITCODE` 能看到 1）。

十二步填完、跑出下面这两行，就算做完（退出码 0）：

```term
$ python test_residue_lab.py
...
Ran 53 tests in 0.026s

OK
```

只验某一步（填一步验一步，别一次填完）：

```term
$ python test_residue_lab.py -k step9
...
Ran 5 tests in 0.002s

OK
```

`-k` 后面是**子串**匹配，所以第 1 步要写成 `-k step1_`（带下划线）：
`-k step1` 会连 `step10`、`step11`、`step12` 一起选中，跑出 19 条（不是环境坏了）。

## 五、任务表

| 步 | 填哪个函数 | 要算出什么 | 立刻验 |
|---|---|---|---|
| 1 | `circle_points` | 围道 $\lvert z-a\rvert=r$ 上等距的 $n$ 个点（逆时针） | `-k step1_` |
| 2 | `closed_integral` | 数值围道积分 $\oint_C f\,dz$（$dz=i\Delta\theta\,(z-a)$） | `-k step2` |
| 3 | `inside` | 奇点 $z_0$ 在圈内还是圈外（边界不算） | `-k step3` |
| 4 | `poly_eval` | 升幂系数多项式的值（霍纳） | `-k step4` |
| 5 | `deriv_poly` | 多项式的一阶导（给 $Q'(z_0)$ 用） | `-k step5` |
| 6 | `strip_factor` | 把 $(z-z_0)^m$ 从分母里除干净（综合除法） | `-k step6` |
| 7 | `deriv_n` | $0$／$1$／$2$ 阶数值导（$g^{(m-1)}$ 用它） | `-k step7` |
| 8 | `residue_simple` | 一阶极点：$P(z_0)/Q'(z_0)$ | `-k step8` |
| 9 | `residue_pole_m` | $m$ 阶极点：$\frac{1}{(m-1)!}g^{(m-1)}(z_0)$ | `-k step9` |
| 10 | `residue_by_integral` | 兜底：$\frac{1}{2\pi i}\oint_{|z-z_0|=\rho}f\,dz$（本性奇点走这条） | `-k step10` |
| 11 | `contour_by_residues` | 留数定理：$2\pi i$ 乘圈内留数之和 | `-k step11` |
| 12 | `contour_missing_poles` | **故意写错的那一版**：圈内只算第一个奇点 | `-k step12` |
| — | 不用填 | 课件那几道真题整表自检 | `-k selfcheck` |

文件里已经写好的常数是 `DEFAULT_N`、`DEFAULT_H`、`DEFAULT_H2`、`TOL_EXACT`、
`TOL_VALUE`、`TWO_PI`、`TAU`——照它们的用法往下填，**别改**。

## 六、逐步做

### 第 1 步 · 围道采样

$$ z_k=a+r\,e^{i\theta_k},\qquad \theta_k=\frac{2\pi k}{n},\ k=0,1,\dots,n-1 . $$

从 $a+r$ 出发、逆时针走一圈，正好是「正向简单闭曲线」。$n$ 取 2048 就够：
梯形法对周期解析被积函数的误差按 $(d/r)^n$ 掉（$d$ 是奇点到圆心的距离），2048 点已经到机器精度。

**坑**：忘了乘 `radius`，点全落在圆心上；角度写成 $-2\pi k/n$ 方向就反了。

### 第 2 步 · $dz$ 换成什么（这一步最容易错）

$z=a+r e^{i\theta}$ 求微分：

$$ dz=i\,r\,e^{i\theta}\,d\theta=i\,\Delta\theta\,(z-a),\qquad \Delta\theta=\frac{2\pi}{n}. $$

于是每一项是 `f(z_k) * (1j * dtheta * (z_k - center))`。

**两个坑**：漏掉 `1j`，$\oint dz/z$ 会算出 $2\pi$（实数，没有 $i$）；漏掉 `(z_k - center)`，
常数被积函数会算出 $2\pi i$ 而不是 $0$。`test_step2_constant_is_zero` 与
`test_step2_uses_center` 各抓一个。

### 第 3 步 · 奇点在圈内还是圈外

$\lvert z_0-\text{center}\rvert<\text{radius}$ 才算圈内，**严格小于**：距离恰好等于半径时
奇点压在围道上，两条前提都不满足。写成 $\lvert z_0\rvert$ 是最常见的错法——
圆心一离开原点就数错，`test_step3_outside` 里那个点 $z_0=-0.5$ 就专门验这件事：
它的 $\lvert z_0\rvert=0.5<1.5$，但离圆心 $1$ 的距离正好 $1.5$，**不在**圈内。

### 第 4 步 · 多项式求值

系数按**升幂**给：$z^3+5z^2+8z+4$ 写成 `[4, 8, 5, 1]`。霍纳法从最高次系数往下卷，
`total = total * z + c` 循环一遍。空列表当零多项式，返回 `0`。

### 第 5 步 · 多项式求导

$z^k$ 求导得 $k\,z^{k-1}$，所以新列表第 $k-1$ 项是 `k * coeffs[k]`，从 $k=1$ 取到末尾。
常数导成空列表（`poly_eval` 对它给 $0$，写成 `[0]` 也行）。

这一条只为一阶极点那条分式公式服务：$\operatorname{Res}=\dfrac{P(z_0)}{Q'(z_0)}$。

### 第 6 步 · 综合除法（把 $(z-z_0)^m$ 除干净）

按降幂做霍纳：$b_0=d_0$、$b_i=d_i+z_0b_{i-1}$，最后一位 $b_n$ 是余数，前面 $n$ 位就是商。
除 $m$ 次就是 $m$ 阶极点要的那个 $\tilde Q$。

为什么需要它：$m$ 阶极点公式里的括号是 $(z-z_0)^m f(z)=\dfrac{P}{\tilde Q}$，
$\tilde Q$ 在 $z_0$ 处不为零，这个商才在 $z_0$ 解析、才谈得上求导。

$z^3+5z^2+8z+4=(z+1)(z+2)^2$：除 $(z+2)$ 一次得 $z^2+3z+2$，除两次得 $z+1$。

### 第 7 步 · 数值求导

$$ g'(z_0)\approx\frac{g(z_0+h)-g(z_0-h)}{2h},\qquad
   g''(z_0)\approx\frac{g(z_0+h)-2g(z_0)+g(z_0-h)}{h^2}. $$

三件事：

1. **`order = 0` 直接返回 `g(z0)`**——$m=1$ 那一行是「零阶导、直接代 $z_0$」，对应 $0!=1$。
   这一条写不出来，两条极点公式就分不开。
2. **二阶差分要除以 $h^2$**，所以步长换 `DEFAULT_H2 = 1e-4`；用 `1e-6` 会被舍入误差抬到
   $10^{-3}$ 量级（第 5 课的 `laplacian` 踩的是同一个坑）。
3. 这里算出来的导**不是精确值**：实测 `m=3`、$g=\cos z$ 那一类差 $2\times10^{-8}$ 量级，
   是截断误差不是算错——`TOL_VALUE = 1e-6` 就是为它留的。

### 第 8 步 · 一阶极点

$$\operatorname{Res}=\frac{P(z_0)}{Q'(z_0)}. $$

一行：`poly_eval(num, z0) / poly_eval(deriv_poly(den), z0)`。

$Q'(z_0)=0$ 说明 $z_0$ 是分母的重根，**一阶公式算不出数**——`test_step8_double_root_raises`
要求这里直接抛 `ZeroDivisionError`。这不是 bug，是信号：回去重新定阶，换第 9 步的公式。
课件那个 warn 块讲的正是这件事。

### 第 9 步 · $m$ 阶极点

$$\operatorname{Res}=\frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{\,m-1}}{dz^{\,m-1}}\Big[(z-z_0)^mf(z)\Big]. $$

三格对应三行：

```text
q = strip_factor(den, z0, m)                    # 括号内那个函数的分母
g = lambda z: poly_eval(num, z) / poly_eval(q, z)
return deriv_n(g, z0, m - 1) / math.factorial(m - 1)
```

求导阶数与阶乘**用的是同一个数 $m-1$**，写成 `m - 1` 就不会错位。
断言里 $(1+z+z^2)/z^3$ 在 $0$ 处必须得 $1$：乘 $z^3$ 后求二阶导得 $2$，再除 $2!$——
**忘了那个 $2!$ 就会写 $2$**，这正是课件点出的「$m\ge3$ 最常见的丢分处」。

### 第 10 步 · 兜底：小圆上的围道积分

$$\operatorname{Res}=\frac{1}{2\pi i}\oint_{|z-z_0|=\rho}f(z)\,dz . $$

本性奇点**只有这一条**：$\lim(z-z_0)^mf$ 对任何 $m$ 都不收敛，代 $z_0$ 无处可代，
只能展开读 $c_{-1}$——而「展开读 $c_{-1}$」的数值版本就是这个小圆积分。

$\rho$ 要小到圈内只剩 $z_0$ 一个奇点。三个实测值：$\operatorname{Res}[e^{1/z},0]=1$、
$\operatorname{Res}[z^2e^{1/z},0]=1/6$、$\operatorname{Res}[\sin z/z^3,0]=0$
（最后这个是填空 3 分那道，展开一步读出 $c_{-1}=0$）。

它也是**所有**奇点的复核手段：第 8、9 步的两个公式，断言都拿它对照过一遍。

### 第 11 步 · 留数定理

$$\oint_C f\,dz=2\pi i\sum_{|z_k-a|<r}\operatorname{Res}[f,z_k]. $$

`poles` 是一串配方 `(奇点位置, 该点的留数)`，先按第 3 步筛，再把圈内的加起来乘 `TAU`。

**两个坑**：漏乘 `TAU` 得到的是留数之和（差一个 $2\pi i$）；把圈外的也加进来是最常见的失分。
`test_step11_outside_excluded` 用同两个奇点换一条 $|z|=1$ 的围道验后者：答案必须是 $0$。
`test_step11_cancellation` 验的是另一种 $0$——$1+(-1)=0$，两个非零留数抵消，
**不是**「圈内没奇点」，这两种 $0$ 卷面上不能混。

### 第 12 步 · 漏掉奇点的对照（这一步是排错，不是新公式）

`contour_missing_poles` 是**故意写错**的那一版：圈内有两个奇点，它只算第一个。
它对应卷面上「围道内有两个奇点只算一个」那个失分点。

拿题目 $\oint_{|z|=8}\dfrac{e^z\,dz}{(z-\pi i)(z-2\pi i)^2}$ 对照，三个数实测：

| 算法 | 结果 |
|---|---|
| 数值围道积分（裁判） | `2.0000000000000204+1.2732395447351617j` |
| 正确：两个留数都算 | `2.0000000000000018+1.2732395447351612j` |
| 错版：只算 $\pi i$ | `0+0.6366197723675809j` |

理论值是 $2+\frac{4}{\pi}i$。数值积分与正版对到 $10^{-15}$，与错版差一个多单位——
**围道积分站哪边，哪边就是对的**，这就是这一节的核验方式。
换 $1/((z+1)(z+2)^2)$ 沿 $|z|=3$ 更狠：正解是 $0$，只算 $-1$ 会得到 $6.283185307179586i$。

`test_step12_single_pole_same` 是反向的对照：圈内只有一个奇点时两版必然相等——
所以两者的差异**只可能**来自漏点，不是别的地方写错了。

### 整表自检（不用填）

`-k selfcheck` 把课件那几道真题一张表跑完：

| 题 | 围道/奇点 | 理论值 |
|---|---|---|
| $\cos z/(z^2(z^2-\pi^2))$ | 奇点 $0$（二阶） | $0$ |
| 同上 | 奇点 $\pi$（一阶） | $-\frac{1}{2\pi^3}$ |
| 同上 | 奇点 $-\pi$（一阶） | $\frac{1}{2\pi^3}$ |
| $e^z/(z-1)^3$ | 奇点 $1$（三阶） | $\frac{e}{2}$ |
| $(z^2-\pi^2)/(z\sin z)$ | 奇点 $2\pi$（一阶） | $\frac{3\pi}{2}$ |
| $1/((z+1)(z+2)^2)$ | $\lvert z\rvert=3$ | $0$ |
| $e^z/((z-\pi i)(z-2\pi i)^2)$ | $\lvert z\rvert=8$ | $2+\frac{4}{\pi}i$ |
| $e^{iz}/(z^2-3\pi z+2\pi^2)$ | $\lvert z-3\rvert=4$ | $4i$ |

每一行都验两列：**数值围道积分**与**按公式算的 $2\pi i\sum$ 留数**，两列都要落在理论值上；
最后一条 `test_selfcheck_zero_sum` 验「算完核对」那一行：全部有限留数之和为零
（$1+(-1)=0$；$0-\frac{1}{2\pi^3}+\frac{1}{2\pi^3}=0$）。

它全绿，说明你的工具和纸面结论对上了——这就是这一节的交付证据。

## 七、卡壳的时候，按这个顺序走

1. **先读断言最后一行**：`期望 X，实际 Y`。两个数一比，差符号、差因子、差一个 $i$ 都看得出来。
2. **按症状对表**：

   | 症状 | 大概率是 |
   |---|---|
   | step1 所有点都落在圆心上 | 忘了乘 `radius` |
   | step1 相邻角差是负的 / 点顺时针排 | 角度写成 $-2\pi k/n$ |
   | step2 $\oint dz/z$ 得 $2\pi$（实数） | $dz$ 漏了 `1j` |
   | step2 常数被积函数得 $2\pi i$ 而不是 $0$ | $dz$ 漏了 `(z_k - center)` |
   | step2 圆心不在原点时全错 | $dz$ 里的 `(z_k - center)` 写成了 `z_k` |
   | step3 围道上的点被判成圈内 | 写成了 `<=`，应为 `<` |
   | step3 圆心一挪就数错奇点 | 用了 `abs(z0)`，应为 `abs(z0 - center)` |
   | step4 多项式值全带小尾巴 / 差得离谱 | 系数当降幂读了，应按升幂 |
   | step6 除完商还是零 / 余数没丢 | 综合除法把最后那一位余数也算进商了 |
   | step7 二阶导数量级离谱（$10^{-3}$ 以上误差） | 用了 `DEFAULT_H`，应换 `DEFAULT_H2` |
   | step7 `order=0` 报错或返回奇怪的值 | 漏了「零阶导直接代 $z_0$」这一支 |
   | step9 $m=3$ 差 2 倍 / 差 6 倍 | 阶乘写了 `m!`，或求导阶数写了 `m`——两处都要 `m - 1` |
   | step9 正确值是 $1$ 而得到 $2$ | 漏了 $\frac{1}{(m-1)!}$（这一条就是那个丢分点的代码版） |
   | step11 结果是留数之和，少了 $i$ | 漏乘 `TAU`（`2j * math.pi`） |
   | step11 换小围道还有非零值 | 圈外的奇点也加进来了 |
   | step10 小圆积分算出的留数不对 | `radius` 太大，圈里混进了第二个奇点 |
   | selfcheck 只有「公式」那一列差 $10^{-8}$ | 正常，是 `deriv_n` 的截断误差，不是错 |

3. **还不对，再看参考解**：`solutions/0014-residue-contour/residue_lab.py`，
   **先只读卡住的那一个函数**，对照完立刻回来自己写一遍（整块自检验的是整表，整段拷会让你跳过判断过程）。

参考解那一步为什么这样写，`solutions/0014-residue-contour/README.md` 里有逐条说明。

## 八、做完之后的对照方式

把参考解拷进任务目录、覆盖同名文件，再跑一次：

```term
$ copy ..\solutions\0014-residue-contour\residue_lab.py .    # Windows
$ python test_residue_lab.py
...
Ran 53 tests in 0.026s

OK
```

**先自己全绿、再对照**。两者的差别如果只在写法（列表推导还是 `for`），不用改；
如果差在求导阶数、阶乘位置、`TAU`、圈内判定，那就是卷面上丢分的根源。

## 九、和实验四的关系

实验四（围道上的留数）要把极点、围道与数值积分画在同一张图上，并在 notebook 里核验
$\oint_C f\,dz=2\pi i\sum$ 留数。它要的两个零件都是这一节产出的：
`contour_by_residues`（右边那一半）和 `closed_integral`（左边那一半），
`circle_points` 采出来的点列直接就是图上那条围道。所以 `residue_lab.py` 别删。
