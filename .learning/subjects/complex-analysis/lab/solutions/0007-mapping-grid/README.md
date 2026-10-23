# 参考解 · 0007-mapping-grid（实验三：保角映射的网格实验）

**先自己全绿，再看这里。** 这份说明只回答「为什么这样写」和「常见错成什么样」，代码在旁边的
`mapping_grid.py`——把那个文件拷回 `lab/0007-mapping-grid/` 覆盖同名文件，
`python test_mapping_grid.py` 就该打出 `OK`（实测两个解释器都是 38 条全绿，见第四节）。

```text
lab/0007-mapping-grid/mapping_grid.py             ← 你填的（9 处留白）
lab/0007-mapping-grid/test_mapping_grid.py        ← 38 条断言，自动判分（别改）
lab/solutions/0007-mapping-grid/mapping_grid.py   ← 参考解（自包含，拷过去直接能跑）
lab/solutions/0007-mapping-grid/README.md         ← 本文件
```

参考解只 import 标准库（`cmath` / `csv` / `math`），不引用任务目录里的任何东西，所以单独拷一个
文件就够；`test_mapping_grid.py` 始终用任务目录里那一份。

---

## 一、九个函数为什么这样写

| 函数 | 写法要点 | 常见的错法 |
|---|---|---|
| `segment_points` | 参数取 `k / (n - 1)`，两端正好落在 $a$、$b$ 上 | 写成 `k / n`：终点差一截，网格右边少一列（图看着只是「小了点」） |
| `grid_lines` | 两族都调 `segment_points`：竖线 `complex(x, im_min) → complex(x, im_max)`，横线反过来 | 两族各写一遍循环，其中一族的端点取错；或把竖线写成「从左到右」（方向反了，第 5 步的十字就跟着反） |
| `map_grid` | 两层列表推导，外层线、内层点；异常照实抛 | `try/except` 把 `1/z` 在原点处的 `ZeroDivisionError` 吞掉填 0——网格踩到极点这件事本身就是要你看见的东西 |
| `angle_between` | 点积除两个模长，`math.degrees(acos(...))`，先夹回 $[-1,1]$ 再 `acos` | 忘了夹区间：浮点偶尔给 $-1.0000000000000002$，`acos` 直接 `ValueError`；或者返回弧度（断言比的是度） |
| `cross_angle` | 两条臂的**像的弦**：$w_1=f(z_0+\delta)-f(z_0)$、$w_2=f(z_0+i\delta)-f(z_0)$，再量夹角 | 在这里又求一次导（那是第 7 步）；或者把臂的**原像**的夹角拿去量（永远是 90°，等于什么都没测） |
| `angle_defect` | `abs(夹角 - 90)`，量不出夹角时返回 90 | 返回带符号的差（$84.5$ 与 $95.5$ 一个 $-5.5$ 一个 $+5.5$，都该算坏）；不判 `None` → `TypeError` |
| `derivative_at` | 中心差分 `(f(z0+h) - f(z0-h)) / (2h)` | 分母写成 `h`（差 2 倍）；漏了 `1j`（那是 $x$ 方向，不是 $y$ 方向） |
| `critical_points` | 列表推导 `abs(derivative_at(f, z)) <= tol` | 用 `set`（顺序乱、断言比的是列表）；把 `1/z` 在 $0$ 处算进来（那里没有定义） |
| `save_curves_csv` | `csv.writer` + `utf-8` + `newline=""`；复数拆成 `w.real` / `w.imag`；每格 `"{:.6g}"` | 把 complex 直接塞给 `writer`（写成 `(1+2j)` 一列，读回来解析不了）；少了 `newline=""`（Windows 每行变两行） |
| `save_angles_csv` | 角度四位小数、偏差与伸缩率 `"{:.6g}"`、`δ` 用 `"{:.0e}"` | 偏差也写四位小数：$2.9\times10^{-3}$ 变成 `0.0029`、$2.8\times10^{-5}$ 变成 `0.0000`，跟「坏掉了」分不开 |

## 二、三个「数值做法才有的」判断

这三条决定你算出来的数是「直角坏了」还是「你还没放大够」。

1. **$\delta$ 是放大倍数，不是随便一个小数。** 十字的臂长 $\delta$ 与「到临界点的距离」之比
   决定量出来的角度：$\delta$ 比距离还大，量到的是曲线在那一段的**平均**弯曲，不是交点处的角。
   实测（同一个 $z_0$，只换 $\delta$）：

   | 打点位置 | $\delta=10^{-2}$ | $10^{-3}$ | $10^{-4}$ | $10^{-6}$ |
   |---|---|---|---|---|
   | $z^2$ 在 $0.01$ | 116.5651° | 92.8624° | 90.2865° | 90.0029° |
   | $1/z$ 在 $0.1+0.1i$ | 84.5474° | 89.4299° | 89.9427° | 89.9994° |
   | $z^2$ 在 $1+i$ | 90.2858° | 90.0286° | 90.0029° | 90.00003° |
   | $z^2$ 在 $0$ | 180.0000° | 180.0000° | 180.0000° | 180.0000° |

   前三行的偏差随 $\delta$ 缩小而**收敛到 0**（截断误差），最后一行钉在 180° 不动——
   这才是「角度被改了」。判据不是「偏差大不大」，而是「缩小 $\delta$ 以后还大不大」。
2. **容差 0.5° 是给「已经足够小」留的余量。** 默认 $\delta=10^{-4}$ 时，所有保角点量出来的
   偏差都在 $3\times10^{-3}$ 到 $0.06$ 度之间（远小于 0.5），临界点是 90 度（远大于 0.5）。
   两边差四个数量级，所以这个数不敏感——换成 0.1 或 5 都得出同一批结论。
3. **结论表的三档是按「导数」分的，不是按「角度」分的。** 自检里那三行判断是：

   ```text
   |f'(z0)| ≤ 1e-9        → 临界点：角度加倍
   is_conformal(z0, δ)    → 保角
   否则                    → 偏差待核对：缩小 δ
   ```

   第三档故意不写「不保角」：它只说明「在这个 $\delta$ 下量出来不像 90°」，要按第 1 条
   缩小 $\delta$ 再量一次才下结论。

## 三、参考解的实测数据

### 三张网格各是什么形状

| 映射 | 窗口 | 竖线（$x=c$）映成 | 横线（$y=d$）映成 | 实测 |
|---|---|---|---|---|
| $w=z^2$ | $[-1,1]^2$ | 抛物线 $u=c^2-\dfrac{v^2}{4c^2}$ | 抛物线 $u=\dfrac{v^2}{4d^2}-d^2$ | 代入残差 `0.0`；$\lvert w\rvert$ 落在 $[0,2]$ |
| $w=e^z$ | $[-1,2]\times[-3,3]$ | 圆 $\lvert w\rvert=e^c$ | 射线 $\arg w=d$ | 竖线 $x=-1$ 上 $\lvert w\rvert$ 全等于 $0.367879441171$（$=e^{-1}$）；$x=2$ 那条是 $7.389056099$（$=e^2$）；横线 $y=-3$ 的辐角全是 $-171.887338539°$（$=-3$ 弧度） |
| $w=1/z$ | $[0.1,2]^2$ | 过原点的圆：圆心 $\left(\frac{1}{2c},0\right)$、半径 $\frac{1}{2c}$ | 过原点的圆：圆心 $\left(0,-\frac{1}{2d}\right)$、半径 $\frac{1}{2\lvert d\rvert}$ | 竖线 $x=0.1$ 上每点到 $(5,0)$ 的距离都是 `5.0`；$y=0.1$ 那条到 $(0,-5)$ 也是 `5.0`；$\lvert w\rvert$ 落在 $[0.3536,7.0711]$ |

**这三行就是「网格变形」的全部内容**：格子会弯、会被拉长压扁，$1/z$ 甚至把最近的线拉到
$7.07$ 倍远（原窗口最远的点才 $2.83$）。

### out/angles.csv（参考解原样，10 行）

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

`stretch` 那一列是 $\lvert f'(z_0)\rvert$：$z^2$ 在 $1+i$ 处是 $\lvert 2z\rvert=2\sqrt2=2.82843$，
$e^z$ 在 $1+i$ 处是 $e=2.71828$，$1/z$ 在 $0.1+0.1i$ 处是 $1/\lvert z\rvert^2=50$。
**最后一个数就是「极点旁边」的真相**：尺度炸到 50 倍，角度仍是 90°。
旋转角（$\arg f'$，本表没列）同样由 `derivative_at` 给：$z^2$ 在 $1+i$ 处 $45°$、
$e^z$ 在 $1+i$ 处 $57.2958°$（$=1$ 弧度）、$1/z$ 在 $0.1+0.1i$ 处 $90°$。

### 另外几个可以直接对表的值

| 算什么 | 结果 |
|---|---|
| `critical_points(z^2, 9×25 网格)` | `[0j]`——原点正好是格点 |
| `critical_points(e^z, …)`、`critical_points(1/z, …)` | 都是 `[]` |
| `cross_angle(z^2, 0, δ)` | 无论 $\delta$ 取 $10^{-2}$ 还是 $10^{-6}$，都是 `180.0` |
| 局部放大窗口 $[-0.3,0.3]^2$ 的像 | 实部范围 $-0.090..0.090$、虚部 $-0.180..0.180$，正好是整张图按 $0.3^2=0.09$ 缩小——$z^2$ 在原点附近是二次的，所以放大图与整图**同形** |
| 每张网格的数据量 | $2\times9\times25=450$ 行 |

## 四、实测的运行输出

```text
$ python test_mapping_grid.py                 （Python 3.13.15，只有标准库）
Ran 38 tests in 0.010s
OK                                            ← 退出码 0

$ python test_mapping_grid.py                 （bundled runtime，Python 3.12.14 + numpy 2.3.5）
Ran 38 tests in 0.011s
OK                                            ← 退出码 0，两个解释器都全绿
```

留白态（还没动手、任务文件原样）实测两个解释器都是：

```text
Ran 38 tests in 0.008s
FAILED (errors=38)                            ← 退出码 1，38 条全是 NotImplementedError
```

分步过滤也实测过（`-k stepN` 各自只跑那一步）：

```text
$ python test_mapping_grid.py -k step1     → Ran 3 tests … OK
$ python test_mapping_grid.py -k step2     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step3     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step4     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step5     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step6     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step7     → Ran 4 tests … OK
$ python test_mapping_grid.py -k step8     → Ran 3 tests … OK
$ python test_mapping_grid.py -k step9     → Ran 4 tests … OK
$ python test_mapping_grid.py -k selfcheck → Ran 4 tests … OK     ← 写出 out/ 五份数据
```

`selfcheck` 跑完，`out/` 里是这五份：

```text
out/curves-z2.csv          450 行   w = z^2 的变形网格
out/curves-exp.csv         450 行   w = e^z 的变形网格
out/curves-inv.csv         450 行   w = 1/z 的变形网格
out/zoom-z2-origin.csv     450 行   原点附近的局部放大网格
out/angles.csv              10 行   「直角还在吗」的结论表
```

## 五、做完以后

- **三句结论**（写进 notebook，或直接回话）：见 `lab/README.md` 第七节末，每条都要能指到
  `out/angles.csv` 的一行。
- **和实验二的关系**：实验二的 `jacobian` 是 $u_xv_y-u_yv_x=\lvert f'(z)\rvert^2$，
  它等于零 ⟺ 本课的 `critical_points` 找到 $z=0$ ⟺ 十字夹角 180°。三条路说的是同一件事：
  **保角 ⟺ 导数非零**。实验二那张「$\bar z$ 也正交」的坑在这里有个对照版：
  $\bar z$ 的十字夹角**也是 90°**（它只把方位翻了过来），所以「夹角没变」同样判不出解析——
  要判方向，还得回到实验二的 `jacobian` 符号。
- **和实验四的关系**：那里的围道也是按参数采点（`0009-cauchy-formula-tool` 的
  `circle_points`），把极点画在图上、把围道叠上去，用的就是本课 `map_grid` 的同一套「采点 → 送过去
  → 存 CSV」流程。

## 六、不装 matplotlib 时怎么「看」这三张图

交付物是 CSV，但你可以把它当字符画打印出来（只用标准库）：

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


show(mg.f_sq, mg.SQ_WINDOW)
```

实测输出（$w=z^2$，窗口 $[-1,1]^2$；实部 $-1..1$、虚部 $-2..2$）：

```text
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

两族抛物线正交地铺开——**这就是「方格纸被 $z^2$ 揉过之后」的样子**。
把窗口换成本课的 `ZOOM_WINDOW`（$[-0.3,0.3]^2$）再画，形状一模一样，只小了一圈（$0.09$ 倍）：
$z^2$ 在临界点附近是二次的，越放大越像自己。真正的异常是「压缩」而不是「形状」：
原点附近两条坐标线的像都倒在实轴上，夹角从 90° 变成 180°。
