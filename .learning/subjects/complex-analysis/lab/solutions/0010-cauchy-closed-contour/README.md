# 参考解 · 0010-cauchy-closed-contour

`cauchy_lab.py` 是第 10 课（柯西积分定理及其推广）lab 的参考解：把它拷进
`lab/0010-cauchy-closed-contour/` 覆盖同名文件，`python test_cauchy_lab.py` 就是 30 个测试全绿
（实测 `Ran 30 tests in 0.013s … OK`，退出码 0）。

**先自己做到全绿，再对照这里。** 下面按步写「参考解为什么这样写」和「最常见的错法」。

## 七步要点

| 步 | 参考解的做法 | 最常见的错法 |
|---|---|---|
| 1 `circle_contour` | 列表推导 `center + radius*cmath.exp(2j*pi*k/n)`，`range(n)` | 用 `range(n + 1)` 把首点又写了一遍；角前面加个负号变成顺时针 |
| 2 `contour_integral` | 循环到 `len(points) - 1`，每段取**左端点**的函数值 | 取右端点 `points[k+1]`；顺手把末点也接回首点（那是第 3 步的事） |
| 3 `closed_integral` | 下一段用 `points[(k + 1) % n]`，`%` 就是「闭合」 | 忘了 `% n`，末点那段漏掉——$z^2$ 从此不再是 $0$ |
| 4 `nearly_zero` | `abs(value) <= tol` | 写 `value == 0`；或者把 `tol` 写死，参数传不进来 |
| 5 `composite_integral` | 外圈正向那个**减去**内圈（正方向）那个 | 写成 `outer + inner`，得 $4\pi i$；只返回 `outer`，得 $2\pi i$ |
| 6 `arc_contour` | `theta0 + (theta1 - theta0)*k/n`，`range(n + 1)` | `range(n)`——末点缺失，弧短一小段 |
| 7 `arc_integral` | 一行：`contour_integral(f, arc_contour(...))` | 又写一遍积分循环；或误以为弧是闭路 |
| 8 整表自检 | 不用写，跑 `-k step8` | — |

## 两个「数值做法才有的」判断

- **为什么要两档容差**：纸面上的 $0$ 与 $2\pi i$ 是精确值，代码里都是近似。区别在误差量级不一样——
  - 解析函数 / 奇点在圈外：和式望远镜式抵消，误差只剩浮点噪声（$10^{-15}$～$10^{-14}$），所以 `TOL_ZERO = 1e-6`
    收得再紧也安全；
  - 有奇点在圈里（$\frac1z$ 那种）：结果本身不是 $0$，而且折线代替圆弧会留 $O(1/n)$ 的残渣。
    $n=4096$ 时 $\frac1z$ 沿 $\lvert z\rvert=2$ 得 $-0.0048+6.28318i$——模对了，实部还差 $4.8\times10^{-3}$。
    所以判「等于 $2\pi i$」只能放到 `TOL_VALUE = 2e-2`。
- **为什么挖洞那一步抵得这么干净**：外圈与内圈用的是同一套点、同一个 $n$，$\frac1z$ 在两圈上的
  和式误差几乎一样大，相减就抵掉了（实测复合闭路得 `0j`）。所以第 5 步的容差用 `TOL_ZERO` 就够——
  这也是「复合闭路定理」在代码里的样子：等式两边不是近似相等，是同一个和式的搬项。

## 做完能拿走什么

- 一套「围道 → 点列 → 积分」的工具：圆周、圆环（复合闭路）、圆弧三种围道，以后加折线也不用改积分函数；
- `closed_integral` 加 `nearly_zero` 就是卷面上「能不能直接写 $0$」那一行的可执行版；
- `composite_integral` 里那个减号，对应卷面上「内圈取顺时针」——符号写错丢的分，这里一次就记住；
- 实验四（围道上的留数）会把 `circle_contour` 的点直接画到图上，再叠极点，所以这一份别删。

## 参考解实测输出

```term
$ python test_cauchy_lab.py
test_step1_count_and_no_repeat (__main__.Step1_圆周采样...) ... ok
...
Ran 30 tests in 0.013s

OK
```

留白态（任务文件原样）是 `Ran 30 tests in 0.006s` / `FAILED (errors=30)`，退出码 1：
30 条断言在留白时全部报 `NotImplementedError`，所以「先红后绿」是这支工具自带的证据。
