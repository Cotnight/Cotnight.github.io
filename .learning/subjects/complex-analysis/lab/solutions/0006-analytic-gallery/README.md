# 参考解 · 0006-analytic-gallery（实验二：解析函数长什么样）

**先自己全绿，再看这里。** 这份说明只回答「为什么这样写」和「常见错成什么样」，
代码在旁边的 `analytic_gallery.py`——把那个文件拷回 `lab/0006-analytic-gallery/` 覆盖同名文件，
`python test_analytic_gallery.py` 就该打出 `OK`（实测两次，见下面第四节）。

```text
lab/0006-analytic-gallery/analytic_gallery.py             ← 你填的
lab/solutions/0006-analytic-gallery/analytic_gallery.py   ← 参考解（自包含，拷过去直接能跑）
lab/solutions/0006-analytic-gallery/README.md             ← 本文件
```

参考解只 import 标准库（`cmath` / `csv` / `math`，numpy 只在向量化那一步里临时 import），
不引用任务目录里的任何东西，所以单独拷一个文件就够；`test_analytic_gallery.py` 始终用任务目录里那一份。

---

## 一、九个函数为什么这样写

| 函数 | 写法要点 | 常见的错法 |
|---|---|---|
| `scan_window` | 两个 for 嵌套：**外层行、内层列**，坐标全走 `pixel_to_re` / `pixel_to_im` | 内层循环用了 `row`（每行都一样）；自己重写坐标公式（与样板差末位，第 4 步对不上） |
| `cr_scan` | `[cr_holds(f, z, tol, h) for z in points]`，返回标签不是筛出来的点 | 照抄第 5 课的 `cr_points`（返回的是点），上色时点就丢了 |
| `analytic_fraction` | 先判空返回 `0.0`，再 `命中数 / 总数` | 忘了空列表 → `ZeroDivisionError`；用 `all(mask)` 判（只能回答「全成立吗」，答不了「多大比例」） |
| `residual_map` | 先 `scan_window` 铺点，再按 `width` 切片成行 | 切片写成 `values[row::height]`（那是按列切，图转 90°）；行序按 `im_max` 往下排（上下颠倒） |
| `grad_u_v` | `dx.real` 是 $u_x$、`dx.imag` 是 $v_x$；`dy.real` 是 $u_y$、`dy.imag` 是 $v_y$ | 把 `d_dx` 与 `d_dy` 的实部配成一对（$(u_x,u_y)$ 拿对了、$(v_x,v_y)$ 却错位成 $(v_y,v_x)$） |
| `orthogonality` | 点积除两个模长，`math.hypot` 算模长；任一为零返回 `None` | 忘了判零 → `ZeroDivisionError`（`\|z\|^2` 的 $\nabla v$ 恒等于零向量）；返回反余弦的角度而不是余弦（断言对不上） |
| `jacobian` | $u_xv_y-u_yv_x$ 照定义写 | 写成 $u_xv_y+u_yv_x$（那是 $r_1,r_2$ 的组合，解析与非解析都非零）；或漏了乘积顺序的符号 |
| `save_summary_csv` | `csv.writer` + `utf-8` + `newline=""`；fraction 四位小数、残差 `"{:.6g}"` | 残差写成四位小数 → $10^{-10}$ 全变 `0.0000`，对照表里「解析」和「非解析」两行看不出差别 |
| `save_grid_csv` | 一行一个像素行、不写表头、每格 `"{:.6g}"` | 写了表头（读回来第一行是 `func,...`）；用 `str(v)` 写出 `6.6e-10` 之外的长尾（能跑，但文件大、对表麻烦） |
| `residual_map_np` | `c = re[None, :] + 1j * im[:, None]` 一次铺整块，形状 `(高, 宽)` | 形状铺成 `(宽, 高)`；坐标改用 `np.linspace`（末位不一样，边界格子会和逐点版差一点点） |

## 二、三个「数值做法才有的」判断

1. **步长**：一阶差分 $h=10^{-6}$。取大了截断误差 $O(h^2)$ 显出来，取小了舍入误差 $O(\varepsilon/h)$
   显出来。第 5 课那个 `DEFAULT_H = 1e-6` 在这里原样沿用——**割线上那个假失败**（见下）反而说明
   步长够小：跨过割线时相位跳了 $2\pi$，残差约等于 $\pi/h\approx3.1\times10^{6}$，一眼就知道不是
   「函数不解析」，而是「差分跨了割线」。
2. **容差**：纸上写 $u_x=v_y$ 是恒等式，代码里永远差一点点。判断一律走 `tol=1e-4`，
   所以「CR 成立的点集」是「残差落在容差内」的点集——`out/scan.csv` 里的 `n_cr` 就是这么数的。
3. **比例而不是结论**：`fraction`（或 `n_cr`）才是可比的数。$651$ 个点里 $651$ 个成立、$0$ 个成立、
   $1$ 个成立，三种情形对应「解析」「处处不解析」「只在一点可导」——这就是第 5 课那张表的量化版。

## 三、参考解的实测数据

`out/scan.csv`（31×21 的窗口；`Ln z` 用右半平面 $(0.25,1.5)\times(-1.5,1.5)$ 避开割线）：

```text
func,n_total,n_cr,fraction,max_resid
e^z,651,651,1.0000,6.66134e-10
sin z,651,651,1.0000,4.44089e-10
z^2,651,651,1.0000,4.44089e-10
z̄,651,0,0.0000,2
|z|^2,651,1,0.0015,3
Ln z,651,651,1.0000,1.66533e-10
```

几个可以直接对表的值：

| 算什么 | 结果 |
|---|---|
| `|z|^2` 在 $31\times21$ 窗口里的成立点数 | `1`（原点正好是格点：第 15 列、第 10 行） |
| `z̄` 的残差最大值 | `2.0`（$r_1=u_x-v_y=1-(-1)$，满幅） |
| `e^z` / `sin z` / `z^2` 的残差最大值 | $6.7\times10^{-10}$ / $4.4\times10^{-10}$ / $4.4\times10^{-10}$ |
| `Ln z` 右半平面 | `273 / 273` 成立（换 31×21 窗口是 `651 / 651`） |
| `Ln z` 左半平面（跨负实轴） | `620 / 651`，失败的正好是 $y=0$ 那一行 31 个点，残差约 $3.1\times10^{6}$ |
| `orthogonality(z^2, 2+i)` | $2.2\times10^{-11}$（正交） |
| `orthogonality(z̄, 0.5+0.3i)` | `0.0`（**也正交**——所以正交判不出解析） |
| `orthogonality(\|z\|^2, 1+i)` | `None`（$\nabla v$ 是零向量，谈不了夹角） |
| `jacobian(z^2, 2+i)` | `20.0`（$=\lvert f'(z)\rvert^2=\lvert2z\rvert^2$） |
| `jacobian(z̄, 0.5+0.3i)` | `-1.0`（方向反了） |

## 四、实测的运行输出

```text
$ python test_analytic_gallery.py            （Python 3.13.15，只有标准库）
Ran 38 tests in 0.046s
OK (skipped=2)                               ← 退出码 0，numpy 那两条跳过

$ python test_analytic_gallery.py            （bundled runtime，Python 3.12.14 + numpy 2.3.5）
Ran 38 tests in 0.032s
OK                                           ← 退出码 0，38 条全跑

$ python test_analytic_gallery.py -k step4
Ran 4 tests in 0.000s
OK

$ python test_analytic_gallery.py -k selfcheck
Ran 4 tests in 0.022s
OK
```

留白态（还没动手）是 `FAILED (errors=36, skipped=2)`、退出码 1——这个「先红」也实测过：
38 条里 36 条报 `NotImplementedError`，另外 2 条是 numpy 那一步（没装就被跳过）。

## 五、做完以后

- `out/scan.csv` 是「解析与非解析的对照」这张表；`out/residual-exp.csv` 与 `out/residual-conj.csv`
  是同一张对照的两张残差图数据（前者整片 $10^{-10}$，后者整片 `2`）；
- 没装 matplotlib 也能看图：把残差图当字符矩阵打出来，`1e-6` 以上画 `#`、以下画 `.`，
  `|z|^2` 会只剩正中一个点；装了 matplotlib 就 `imshow(..., origin="lower")`，行序与 CSV 一致；
- 实验三（保角映射的网格实验）要接着用这里的 `jacobian` 与「导数非零」这条判据——`jacobian`
  等于零的点正是保角失效的临界点，所以这一块别删。
