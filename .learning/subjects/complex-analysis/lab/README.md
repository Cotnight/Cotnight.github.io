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
