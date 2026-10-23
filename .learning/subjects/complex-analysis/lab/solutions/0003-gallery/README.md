# 参考解 · 0003-gallery（实验一：把复数画上复平面）

**先自己全绿，再看这里。** 这份说明只回答「为什么这样写」和「常见错成什么样」，
代码在旁边的 `gallery.py`——把那个文件拷回 `lab/0003-gallery/` 覆盖同名文件，
`python test_gallery.py` 就该打出 `OK`。

```text
lab/0003-gallery/gallery.py                     ← 你填的
lab/solutions/0003-gallery/gallery.py           ← 参考解（自包含，拷过去直接能跑）
lab/solutions/0003-gallery/README.md            ← 本文件
```

参考解不引用任务目录里的任何东西（只 import 标准库，第 8 步 import numpy），
所以单独拷一个文件就够；`test_gallery.py` 始终用任务目录里那一份。

---

## 每个函数为什么这样写

| 函数 | 写法要点 | 为什么不能换个写法 |
|---|---|---|
| `nth_roots` | `r = abs(z0) ** (1/n)`；角度用 `cmath.phase`（弧度）+ `2πk`，整体除 `n` | 模要开 `n` 次方；中途转成角度制会把 $360^\circ$ 当 $2\pi$ 用，图案整体转错 |
| `arg_degrees` | `math.degrees(cmath.phase(z)) % 360` | 不 `% 360` 就有负数色相，第四象限绕回去 |
| `escape_from` | 先迭代、后判模；`abs(z) > 2.0`（严格）；循环外 `return max_iter` | `>= 2` 会让 $c=-2$ 在第 1 步「逃逸」；返回 `None` 会让颜色表对不齐 |
| `mandelbrot_escape` | `escape_from(0j, c, max_iter)` 一行 | 曼德博集的定义里起点就是 0；自己再写一遍循环容易和 `escape_from` 走偏 |
| `escaped` | `mandelbrot_escape(...) < max_iter` | 「逃出去」是步数没用完，不是用完 |
| `escape_grid` | 外层行、内层列，坐标走 `pixel_to_re/pixel_to_im` | 行序反了图上下颠倒；坐标自己重算（比如 `np.linspace`）会和逐点版差末位 |
| `save_points_csv` | `csv.writer` + `utf-8` + `newline=""`，写 `z.real` / `z.imag` | 少 `newline=""` 每行变 `\r\r\n`；直接写复数对象不是数 |
| `save_grid_csv` | 一行一个像素行，不写表头，单元格 `int(v)` | 写了表头，读回来第一行就是 `re,im` 之类的字符串，`int()` 直接崩 |
| `escape_grid_np` | `c = re[None, :] + 1j * im[:, None]`；掩码只推进活着的点 | 形状要 `(高, 宽)`；用 `np.linspace` 会让边界格子翻格 |

---

## 三个「几乎人人会错」的点

1. **角度单位**。`cmath.phase` 是弧度，`cmath.exp` 吃的也是弧度。只有「画图时的色相」和
   「给人看的标题」才需要度数——那是 `arg_degrees` 的活儿，别把它塞回方根公式里。
2. **行序**。`grid[0]` 是 $y$ 最小那行。屏幕上你我都是从上看下来，但复平面的 $y$ 轴朝上，
   第 0 行在下。`imshow` 那边对应的是 `origin="lower"`。
3. **`newline=""`**。Windows 的文本模式会把 `\n` 翻成 `\r\n`，再碰上 csv 自己写的 `\r\n`，
   文件里就多出一倍空行。三件套（`"w"`、`encoding="utf-8"`、`newline=""`）一个都不能省。

---

## 实测数据（本机 bundled runtime，numpy 2.3.5 / Python 3.12.14）

参考解的运行结果，拿来核对自己那几行数：

```text
$ python test_gallery.py
Ran 28 tests in 0.010s
OK                                     ← 退出码 0，第 8 步也跑了

$ python test_gallery.py            （同一份代码，装在只有标准库的 Python 3.13.15）
Ran 28 tests in 0.008s
OK (skipped=2)                         ← 第 8 步需要 numpy，跳过不算失败

$ python test_gallery.py -k step5
Ran 4 tests in 0.000s
OK
```

留白态（还没动手）是 `FAILED (errors=28)`、退出码 1——这个「先红」也是验过的。

几个可以直接对表的值：

| 算什么 | 结果 |
|---|---|
| `nth_roots(1+1j, 5)` 的模 | 都等于 $2^{1/10}\approx1.071773$ |
| 同样五个根的角度 | $9^\circ,\ 81^\circ,\ 153^\circ,\ 225^\circ,\ 297^\circ$（每隔 $72^\circ$） |
| `nth_roots(-1, 3)` | $\tfrac12\pm\tfrac{\sqrt3}{2}i$ 与 $-1$，边长 $\sqrt3\approx1.732$ |
| `escape_from(0, 1, 100)` | `3`（$0\to1\to2\to5$） |
| `escape_from(0, -2, 100)` | `100`（模正好等于 2，不算逃逸） |
| `mandelbrot_escape(0.5, 40)` | `5` |
| 40×24 窗口、`max_iter=60` | 逃逸步数 $=60$ 的格子 224 个 / 960 格（23%） |
| `escape_grid(-2, 0.5, -0.25, 1.0, 5, 3, 40)` | `[[1,6,13,40,5],[1,5,8,40,5],[1,3,3,13,2]]` |
| `escape_grid_np` 与逐点版 | 40×24 上逐格相同（`True`） |

耗时（bundled runtime，只供参考）：逐点版 480×320、`max_iter=80` 约 0.2 秒，
numpy 版同尺寸约 0.07 秒。所以第 8 步不是「不写就跑不动」，而是**实验二要扫整片复平面时的底子**。

---

## 做完以后

- `out/roots.csv` 与 `out/grid.csv` 是画廊第一块的证据，实验二还会读它们；
- 两张图（方根分布、缩略图）在 notebook 里怎么看对不对：
  方根应当在以原点为心的圆上等距排开、连起来是正 $n$ 边形；缩略图应当是一团偏左的
  「心形 + 圆盘」亮边暗心，边界附近颜色变化最剧烈；
- 图上下颠倒、方根挤成一团、整张全黑或全白，三种症状都对应本文第二节那三个坑。
