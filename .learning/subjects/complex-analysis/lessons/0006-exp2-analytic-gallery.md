---
title: 实验二：解析函数长什么样
goal: 做出解析与非解析函数的图像对照，并数值验证柯西-黎曼条件——`python test_analytic_gallery.py` 打出 `OK`，`out/` 里留下结论表与两张残差图。
---

这是图像画廊的第二块。第 5 课在纸上判解析：拆出 $u$ 与 $v$、求四个偏导、验柯西-黎曼条件。
实验一把复数画上了复平面。这一课把两件事接起来——**同一套偏导，改用数值差分去算，逐点判，再画成图**。

验收的那句话是：**做出解析与非解析函数的图像对照，并数值验证柯西-黎曼条件。**
图不是装饰，它是判据的样子：解析函数的模与辐角两组等值线处处垂直，$\bar z$ 与 $\lvert z\rvert^2$ 不是。

## 这次要交出什么

三样东西，交到 [`lab/0006-analytic-gallery`](../lab/0006-analytic-gallery/)：

| 交出什么 | 落在哪 | 一句话说明 |
|---|---|---|
| `analytic_gallery.py` 里 9 个函数 | `lab/0006-analytic-gallery/analytic_gallery.py` | 铺窗口、逐点判 CR、残差图、正交性、存表 |
| `out/` 三份 CSV | `lab/0006-analytic-gallery/out/` | `scan.csv` 是结论表，另两张是残差图 |
| 三句结论 | 写进 notebook，或直接回话 | 第 3 步给了该写哪三句 |

六个样板已经写好、**别改**：`pixel_to_re` / `pixel_to_im` 来自实验一的 `gallery.py`，
`d_dx` / `d_dy` / `cr_residual` / `cr_holds` 来自第 5 课的 `cr_tool.py`。你填的是它们上面的 9 处留白。

任务表、装环境、卡壳顺序都在 [`lab/README.md`](../lab/README.md) 里，找标题「实验二 · 解析函数长什么样」。

## 怎么算过

被验收的要求拆成三条，逐条都有可观察的证据：

1. **能跑**：`python test_analytic_gallery.py` 打出 `OK`（38 条断言；没装 numpy 时 `OK (skipped=2)` 也算）。这是「数值验证 CR」的硬证据。
2. **有对照**：`out/scan.csv` 六行分得开——$e^z$、$\sin z$、$z^2$ 三行都是 `1.0000`，$\bar z$ 是 `0.0000`，$\lvert z\rvert^2$ 是 `0.0015`；两张残差图一张整片 $10^{-10}$、一张整片 `2`。
3. **说得出**：三句结论各一句（第 3 步给的），并且能指着代码说出「哪一行算出残差」「$\bar z$ 的两组线也垂直，凭什么说它不解析」。

三档结论：

- **通过**：三条都成立。差一步：结论表对了但说不出 $\bar z$ 那一格的理由。
- **部分通过**：测试 `OK`，但结论表里的点数不对（$\lvert z\rvert^2$ 不是 `1`、$\operatorname{Ln} z$ 不是 `651`）——窗口或行序有问题；或者数据齐了却说不出 $\bar z$ 为什么正交。
- **不通过**：只填了函数、没有 `out/` 三份数据；或表里解析与非解析两行看不出区别（残差都写成 `0.0000` 就是这个症状）。

::: warn 说懂了不算
这一课只认三样：`OK` 的测试输出、`out/` 里那三份数据、三句能对得上数的话。三样到手才算过。
:::

## 三步走

::: practice 上手做 | 第 1 步 · 填 9 个函数

打开 [`analytic_gallery.py`](../lab/0006-analytic-gallery/analytic_gallery.py)，按 [`lab/README.md`](../lab/README.md) 的任务表填，**填一个验一个**：

```term
$ cd lab/0006-analytic-gallery
$ python test_analytic_gallery.py -k step1
```

还没动手时跑全量是 `FAILED (errors=36, skipped=2)`、退出码 1——先红后绿，这是设计。

:::

::: practice 上手做 | 第 2 步 · 跑自检交出 out/

九步填完后跑一次全量，再把自检跑一遍：

```term
$ python test_analytic_gallery.py
$ python test_analytic_gallery.py -k selfcheck
```

第二个命令会写出 `out/scan.csv`、`out/residual-exp.csv`、`out/residual-conj.csv`。
自检全绿才算数据出来了：它同时验了「解析的三个整片成立」和「$\operatorname{Ln} z$ 换窗口后整片成立」。

:::

::: practice 上手做 | 第 3 步 · 写三句结论

只要三句，别写小作文：

1. $e^z$、$\sin z$、$z^2$ 整片成立（651/651），残差在 $10^{-10}$：这三个在窗口内解析。
2. $\bar z$ 一个点都不成立（残差恒为 2），$\lvert z\rvert^2$ 只有原点成立：前者处处不解析，后者只在一点可导、不解析。
3. $\operatorname{Ln} z$ 在右半平面整片成立；跨负实轴那列点的「失败」是假失败。

第 2 句是这一课的重点：**点集的一两个点不等于一整片区域**，这就是第 5 课「可导推不出解析」那句话的数值版。

:::

## 等值线为什么正交

解析函数在图上有一个签名：**模的等值线与辐角的等值线处处垂直**。三行就能推完。

若 $f=u+iv$ 解析，则 $\lvert f\rvert=e^{u}$（因为 $u=\ln\lvert f\rvert$），而 $\arg f=v$。所以
「模的等值线」就是 $u$ 的等值线，「辐角的等值线」就是 $v$ 的等值线。两组线垂直 ⟺ 两个梯度垂直：

$$ \nabla u\cdot\nabla v=u_xv_x+u_yv_y=v_yv_x-v_xv_y=0, $$

最后一步用的正是柯西-黎曼条件 $u_x=v_y$ 与 $u_y=-v_x$。

::: svg
alt: 三圈同心圆与四条从圆心射出的直线，每个交点处圆与射线都成直角
caption: 模的等值线（圆）与辐角的等值线（射线）在每个交点处都垂直；这是解析函数的签名。

<svg viewBox="0 0 120 100" role="img" aria-hidden="true">
<g fill="none" stroke="currentColor" stroke-width="0.7">
<circle cx="60" cy="50" r="14"/>
<circle cx="60" cy="50" r="28"/>
<circle cx="60" cy="50" r="42"/>
<line x1="60" y1="50" x2="106" y2="50"/>
<line x1="60" y1="50" x2="83" y2="10"/>
<line x1="60" y1="50" x2="14" y2="50"/>
<line x1="60" y1="50" x2="37" y2="90"/>
</g>
<circle cx="60" cy="50" r="1.5" fill="currentColor"/>
</svg>
:::

::: tip 用到的偏导只有这一条
$\nabla u=(u_x,u_y)$、$\nabla v=(v_x,v_y)$，点积是 $u_xv_x+u_yv_y$——多元微积分里那点东西，够了。
数值上这四个偏导都由中心差分给：$u_x\approx\frac{u(x+h)-u(x-h)}{2h}$，沿 $y$ 方向换成 $z\pm ih$。
:::

## 正交不等于解析

这一条是这一课最容易想歪的地方。$\bar z$ 的实部是 $x$、虚部是 $-y$，两组等值线是竖线和横线——
**它也处处垂直**。所以「正交」这个现象判不出解析。

分开它们的是方向：解析函数的雅可比行列式 $u_xv_y-u_yv_x=\lvert f'(z)\rvert^2>0$，$\bar z$ 的那个是 $-1$。
数值上量出来：$z^2$ 在 $2+i$ 处是 `20`，$\bar z$ 在 $0.5+0.3i$ 处是 `-1`。
所以判据是「CR 残差为 0 **且** 行列式为正」，只看图上的直角是不够的。

## Ln z 的割线

主值 $\operatorname{Ln} z$ 在负实轴上不连续，而那正是差分要跨过去的地方。第 2 步的自检里：

- 右半平面 $[0.25,1.5]\times[-1.5,1.5]$：`651 / 651` 成立，残差 $1.7\times10^{-10}$；
- 左半平面 $[-1.5,-0.25]\times[-1.5,1.5]$：`620 / 651`，失败的正好是 $y=0$ 那一行的 31 个点，残差约 $3.1\times10^{6}$。

$3.1\times10^{6}$ 就是 $\pi/h$：$h=10^{-6}$，相位在割线两侧差 $2\pi$，被差分当成了导数。
**认假失败的办法是看残差量级**——解析函数的残差在 $10^{-10}$，假失败在 $10^{6}$，差十几个数量级。
这也是大纲第 3 条坑「分割线被误判为不解析」的数值形态。

## 不装包也能自检

`test_analytic_gallery.py` 只用标准库（`cmath` / `csv` / `math` / `unittest`），不装 numpy、matplotlib、Jupyter 都能跑。
本机两个解释器的实测输出：

```term
$ python test_analytic_gallery.py            # Python 3.13.15，只有标准库
Ran 38 tests in 0.046s

OK (skipped=2)
```

```term
$ python test_analytic_gallery.py            # bundled runtime，Python 3.12.14 + numpy 2.3.5
Ran 38 tests in 0.032s

OK
```

留白态是 `FAILED (errors=36, skipped=2)`、退出码 1——先红也量过。

想看「图」但没有 matplotlib：把残差图当字符矩阵打出来，只用标准库，`1e-6` 以上画 `#`、以下画 `.`。
$\lvert z\rvert^2$ 会只剩正中一个点，$\bar z$ 整片 `#`，$e^z$ 整片 `.`——同一份数据，另一种画法。
代码在 [`lab/README.md`](../lab/README.md) 第七节，字符图与 CSV 是同一批数字。

## 最可能卡在哪

| 症状或报错 | 原因 | 去哪一步 |
|---|---|---|
| `NotImplementedError: 第 N 步还没写` | 那一步还没填，不是环境坏了 | 任务表第 N 行 |
| `ZeroDivisionError` | 空点集没判空，或梯度是零向量（$\lvert z\rvert^2$ 的 $\nabla v\equiv0$） | 第 3、6 步 |
| 残差图整片 $10^{6}$ | 点在 $\operatorname{Ln} z$ 的割线上，差分跨了割线 | 换窗口，别把割线框进来 |
| 残差图上下颠倒 / 转了 90° | 第 0 行不是 `im_min`，或切片按列切了 | 第 4 步 |
| 结论表里两行都是 `0.0000` | 残差写成四位小数，$10^{-10}$ 被抹平了 | 第 8 步 |
| CSV 每行之间有空白行 | `open` 少了 `newline=""` | 第 8、9 步 |
| 余弦到处不为 0 | 四个偏导错位（$v_x$ 与 $v_y$ 对调） | 第 5、6 步 |
| $\bar z$ 的行列式是正的 | 取了绝对值，或写成了 $u_xv_y+u_yv_x$ | 第 7 步 |

## 自查清单

1. `python test_analytic_gallery.py` 打出 `OK`（没 numpy 时 `OK (skipped=2)` 也算）。
2. `out/scan.csv` 七行（表头 + 六个函数），三行 `1.0000`、一行 `0.0000`、`|z|^2` 那行 `1`。
3. `out/residual-exp.csv` 是 21 行、每行 31 个数，最大不超过 $10^{-8}$。
4. `out/residual-conj.csv` 也是 21 × 31，每个数都是 `2`。
5. 能说出 $\bar z$ 的两组等值线为什么也垂直，以及凭什么判它不解析（行列式 $-1$）。
6. 第 3 步那三句是你自己写的，不是抄课件的整段。

## 卡壳了怎么走

1. 先读断言最后一行：`AssertionError` 后面通常带着期望值与实际值，差符号、差行序、差点数都在那里。
2. 对不上就查 [`lab/README.md`](../lab/README.md) 第九节的症状对表，按症状定位到哪一步。
3. 还不对，只打开参考解里**卡住的那一个函数**（[`solutions/0006-analytic-gallery/analytic_gallery.py`](../lab/solutions/0006-analytic-gallery/analytic_gallery.py)），看完立刻自己重写一遍。

## 下一步

实验三「保角映射的网格实验」会把同一套东西用到 $z^2$、$e^z$、$1/z$ 上：铺网格、逐点映射、看直角有没有被保持。
它要的判据「保角 ⟺ 导数非零」，正是这一课的 `jacobian`：$\det J=\lvert f'(z)\rvert^2$，为零的点就是保角失效的临界点。
所以 `analytic_gallery.py` 与 `out/` 别删。

::: resources
- 李君、于非非《复变函数与积分变换》§1.4 可导与解析、§1.3 初等函数 | 书 · 柯西-黎曼条件与解析的定义以它为准
- [第 5 课：可导与解析的判定](0005-ch1-analytic.html) | 课件 · 纸面那套四步判定，本课是它的数值版
- [实验一：把复数画上复平面](0003-exp1-complex-gallery.html) | 课件 · 坐标换算与铺网格的出处
:::
