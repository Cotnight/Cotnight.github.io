# 参考解 · 0014-residue-contour

`residue_lab.py` 是第 14 课（留数与留数定理）lab 的参考解：把它拷进
`lab/0014-residue-contour/` 覆盖同名文件，`python test_residue_lab.py` 就是 53 个测试全绿
（实测 `Ran 53 tests in 0.026s … OK`，退出码 0）。

**先自己做到全绿，再对照这里。** 下面按步写「参考解为什么这样写」和「最常见的错法」。

## 十二步要点

| 步 | 参考解的做法 | 最常见的错法 |
|---|---|---|
| 1 `circle_points` | 列表推导 `center + radius*cmath.exp(1j*2πk/n)`，`range(n)` | 忘了乘 `radius`；角写成负的（变顺时针）；`range(n+1)` 把首点又写一遍 |
| 2 `closed_integral` | 每项 `f(z) * (1j*dtheta*(z - center))`，`dtheta = 2π/n` | 漏 `1j`（得 $2\pi$）；漏 `(z - center)`（常数积出 $2\pi i$） |
| 3 `inside` | `abs(z0 - center) < radius` | 写 `abs(z0) < radius`；写 `<=` 把围道上的点算进来 |
| 4 `poly_eval` | 霍纳：`total = total*z + c` 遍历 `reversed(coeffs)` | 按降幂读系数；空列表抛 `IndexError` |
| 5 `deriv_poly` | `[k*coeffs[k] for k in range(1, len(coeffs))]` | 从 `k=0` 起（常数位留着）；导数位整体错一位 |
| 6 `strip_factor` | 降幂霍纳，`b[n]` 是余数、前 $n$ 位是商；循环 `m` 次 | 把余数也算进商；只除一次就返回 |
| 7 `deriv_n` | `order` 分三支：0 直接取值、1 用 `DEFAULT_H`、2 用 `DEFAULT_H2` | 二阶用 `DEFAULT_H`（误差 $10^{-3}$）；漏了 `order=0` 那一支 |
| 8 `residue_simple` | `poly_eval(num,z0) / poly_eval(deriv_poly(den),z0)` | 分母写了 $Q(z_0)$（恒为 0）；重根处不报错而是硬算出数 |
| 9 `residue_pole_m` | `strip_factor` → `g = P/Q̃` → `deriv_n(g,z0,m-1)` → 除 `factorial(m-1)` | 求导阶数写 `m`；阶乘写 `m!`；漏 `1/(m-1)!`（$m=3$ 时答案正好差一倍） |
| 10 `residue_by_integral` | `closed_integral(f, z0, radius) / TAU` | 乘 `TAU` 而不是除；`radius` 太大，圈里混进第二个奇点 |
| 11 `contour_by_residues` | 先按 `inside` 筛，再 `TAU * sum(...)` | 漏乘 `TAU`；圈外的也算进来 |
| 12 `contour_missing_poles` | 遍历，遇到第一个圈内的就 `return TAU * 留数` | 写成和正版一样（那就没有对照组了）；忘了 `0` 个奇点时返回 `0j` |

## 三个「数值做法才有的」判断

- **为什么 $dz$ 取解析式而不是折线的 $\Delta z$**：第 10 课那条 lab 用的是 `points[k+1]-points[k]`，
  折线代替圆弧会留 $O(1/n)$ 的残渣（实部差 $4.8\times10^{-3}$），判零只能放到 $2\times10^{-2}$。
  这一节要和留数、和 $2\pi i\sum$ 逐位对，所以 `dz` 直接用 $i\Delta\theta(z_k-a)$——
  梯形法对周期解析被积函数的误差按 $(d/r)^n$ 掉，$n=2048$ 时实测 $10^{-14}$ 量级，
  `TOL_EXACT = 1e-9` 收得再紧也安全。这一节因此**只有两档容差**：围道一档、公式一档。
- **为什么公式那一路只能到 $10^{-6}$**：$m$ 阶公式要数值求 $m-1$ 阶导。二阶中心差分除以 $h^2$，
  步长取 $10^{-6}$ 时舍入误差被放大到 $10^{-3}$，取 $10^{-4}$ 时截断误差在 $10^{-8}$ 量级
  （实测 $(1+z+z^2)/z^3$ 在 $0$ 处得 $0.9999999939$，差 $6.1\times10^{-9}$）。
  所以 `DEFAULT_H2 = 1e-4`、`TOL_VALUE = 1e-6`：紧到能抓住「漏 $1/2!$」这种差一倍的错，
  又松到不会把截断误差当错。
- **为什么第 12 步要留一个「故意写错」的函数**：卷面上「圈内两个奇点只算一个」这类错，
  在纸上是看不出来的——两个答案都长得像个积分值。有了数值围道积分当裁判，
  $\lvert z\rvert=8$ 那道题：正版 `2.0000000000000018+1.2732395447351612j`、
  错版 `0+0.6366197723675809j`、围道积分 `2.0000000000000204+1.2732395447351617j`，
  对错一眼分开。断言里还留了反向对照（只有一个奇点时两版相等），证明差异只可能来自漏点。

## 做完能拿走什么

- 一套「公式 ↔ 围道积分」互相校验的工具，四种留数算法各有一个函数，
  卷面上算完可以自己验一遍；
- `strip_factor` + `deriv_n` + `factorial(m-1)` 这三行就是把 $m$ 阶极点公式默写出来的样子，
  「求几阶导、乘几的阶乘」不再是背的；
- `inside` 那一行的 `abs(z0 - center)`：围道不圆心在原点时数错奇点，是这一章最贵的错；
- 实验四（围道上的留数）会直接把 `circle_points` 的点列画成围道、把 `contour_by_residues`
  的结果叠上去，所以这一份别删。

## 参考解实测输出

```term
$ python test_residue_lab.py
test_selfcheck_contour_table (__main__.Selfcheck_整表自检...) ... ok
...
Ran 53 tests in 0.026s

OK
```

留白态（任务文件原样）是 `Ran 53 tests in 0.008s` / `FAILED (errors=53)`，退出码 1：
53 条断言在留白时全部报 `NotImplementedError`，所以「先红后绿」是这支工具自带的证据。
