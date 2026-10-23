#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复变函数图像画廊 · 第四块：围道、极点、留数（任务版 / 留白）

这是实验四（`exp4-residue-contour`）要填的文件。按 `lab/README.md` 任务表从上到下填掉
10 处 `raise NotImplementedError`，**填一个验一个**：

    python test_contour_residue.py -k step1_    # 只跑第 1 步（注意那个下划线）
    python test_contour_residue.py              # 全部（含自检）
    python test_contour_residue.py -k selfcheck # 只跑自检，写出 out/

三块面板（实验一的方根、实验二的辐角着色、实验三的网格变形）在这一课被重新铺一遍，
和后叠上去的第四块（围道 + 极点）一起写进同一份 `out/`；这就是「并进同一份画廊」。
第四块的数据是两样：

  · `out/panel4-contour.csv`：一条围道的采样点，加上圈内/圈外几个极点——
    这是「围道—极点」那张图的数字版；
  · `out/ledger.csv`：每条围道一行，**数值围道积分**与 **2πi·Σ圈内留数** 并排放，
    差多少、一致不一致都写在行里。留数定理就是让这两列相等。

**给好、别改的几样**（测试按它们算）：

  · `f_cubic` / `f_double`：两个被积函数，都是卷面上的真题；
  · `POLES_DOUBLE` 与 `SPECIMENS`：五个「围道 + 极点 + 留数」的配方，其中 S5 是
    故意少列一个奇点的对照组；
  · `arg_degrees`（实验二的着色）、`write_csv`（写面板 CSV 的样板）、`ledger_rows`。

只用标准库（`cmath` / `csv` / `math` / `os`），不用 numpy、不用 matplotlib、不用 Jupyter。
"""

import cmath
import csv
import math
import os

CONTOUR_N = 2048        # 数值围道积分的采样点数
ART_N = 180             # 字符画上画圆圈用多少个点（只为看图，不求积）
TOL_AGREE = 1e-6        # 「数值积分 == 2πiΣ留数」的容差
TAU = 2j * math.pi      # 2πi：留数定理里那个乘法因子

# 三块旧面板用的窗口，与实验一～三同一批数字
PANEL1 = (1 + 1j, 5)              # 实验一：z = 1+i 的 5 个五次方根
ARG_WINDOW = (-1.0, 1.0, -1.0, 1.0)   # 实验二：辐角着色的窗口
ARG_STEPS = 5                     # 每边 5 个点 → 25 个点
GRID_LINES = (0.25, 0.5, 0.75, 1.0)   # 实验三：z^2 面板的四条竖线 x = 常数
GRID_POINTS = 6                   # 每条线上 6 个点

PI = math.pi


# ══ 被积函数与配方（给好，不用填）════════════════════════════════════
def f_cubic(z):
    """f(z) = 1/((z+1)(z+2)^2)：奇点 −1（一阶）与 −2（二阶）。"""
    return 1 / ((z + 1) * (z + 2) ** 2)


def f_double(z):
    """f(z) = e^z/((z−πi)(z−2πi)^2)：2022 年卷那道 |z|=8 的题。"""
    return cmath.exp(z) / ((z - 1j * PI) * (z - 2j * PI) ** 2)


# 奇点与它们的留数（第 14 课算过）：(位置, 留数)
POLES_CUBIC = [(-1 + 0j, 1 + 0j), (-2 + 0j, -1 + 0j)]
POLES_DOUBLE = [(1j * PI, 1 / PI ** 2), (2j * PI, (1 - 1j * PI) / PI ** 2)]

# (案名, 被积函数, 奇点表, 圆心, 半径)
SPECIMENS = [
    ('S1 · 1/((z+1)(z+2)²) 沿 |z|=3', f_cubic, POLES_CUBIC, 0j, 3.0),
    ('S2 · e^z/((z−πi)(z−2πi)²) 沿 |z|=8', f_double, POLES_DOUBLE, 0j, 8.0),
    ('S3 · 同 S2 换成 |z|=4：2πi 落在圈外', f_double, POLES_DOUBLE, 0j, 4.0),
    ('S4 · 同 S2 换成 |z|=2：两个都落在圈外', f_double, POLES_DOUBLE, 0j, 2.0),
    ('S5 · S2 只列一个奇点（故意错的那一版）', f_double, POLES_DOUBLE[:1], 0j, 8.0),
]


def arg_degrees(z):
    """（给好）辐角主值换成 [0,360) 的度数——实验二那张着色图用的就是它。"""
    return math.degrees(cmath.phase(z)) % 360


def write_csv(out_dir, filename, header, rows):
    """（给好）把一份面板数据写成 CSV，返回数据行数（不含表头）。

    样板就是这一段：`open` 三件套（`"w"` + `encoding` + `newline=""`）一个都不能省，
    复数要拆成 real / imag 两列，每格用 "{:.6g}"。
    """
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(os.path.join(out_dir, filename), 'w',
              encoding='utf-8', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for row in rows:
            writer.writerow(['{:.6g}'.format(v) if isinstance(v, float) else v
                             for v in row])
    return len(rows)


# ══ 第 1 步 ═════════════════════════════════════════════════════
def nth_roots(z0, n):
    """实验一那块面板：z0 的全部 n 次方根，按 k = 0, 1, …, n−1 的顺序。

        z_k = |z0|^(1/n) · e^(i(Arg z0 + 2πk)/n)

    提示：模统一 `abs(z0) ** (1 / n)`；角从 `cmath.phase(z0)` 出发、**按弧度**加
    2πk 再除以 n，最后 `cmath.exp(1j * 角)`。中途别 `math.degrees` 一下再塞回公式
    ——实验一那条「方根用角度制」的坑就是这个。
    """
    raise NotImplementedError('第 1 步还没写：nth_roots —— 见 lab/README.md 任务表第 1 行')


# ══ 第 2 步 ═════════════════════════════════════════════════════
def segment_points(a, b, n):
    """实验三那块面板：线段 a → b 上等距的 n 个点（含两端）。

    参数取 k / (n − 1)，两端才能正好落在 a 与 b 上；写成 k / n 时终点永远差一截
    （网格右边少一列，看着只是「图小了点」）。n 小于 2 抛 ValueError。

    提示：`a + (b - a) * k / (n - 1)`，k 从 0 到 n−1。
    """
    raise NotImplementedError('第 2 步还没写：segment_points —— 见 lab/README.md 任务表第 2 行')


# ══ 第 3 步 ═════════════════════════════════════════════════════
def circle_contour(center, radius, n=CONTOUR_N):
    """第四块面板：正向（逆时针）圆周 |z − center| = radius 上等距的 n 个点。

        z_k = center + radius · e^(i·2πk/n),  k = 0, 1, …, n−1

    返回长度 n 的列表，**首点不要重复写进末尾**：圆周是闭合的，闭合那一段由第 4 步
    的 dz 公式负责。这个点列同时是「图上那条围道」——第 8 步与第 10 步都拿它画。

    提示：忘了乘 radius，点全落在圆心，第 4 步马上 ZeroDivisionError。
    """
    raise NotImplementedError('第 3 步还没写：circle_contour —— 见 lab/README.md 任务表第 3 行')


# ══ 第 4 步 ═════════════════════════════════════════════════════
def contour_integral(f, center, radius, n=CONTOUR_N):
    """数值围道积分 ∮_{|z−center|=radius} f(z) dz（正向一整圈）。

    z = a + r e^(iθ) 求微分得

        dz = i·r·e^(iθ) dθ = i·Δθ·(z − a),   Δθ = 2π/n,

    于是和式里每一项是 `f(z_k) * (1j * dtheta * (z_k - center))`。

    提示：漏掉 1j，∮dz/z 会算出 2π（实数）；漏掉 `(z_k − center)`，常数被积函数
    会算出 2πi 而不是 0；漏了 center 只减 `z_k`，圆心一离开原点就全错。
    """
    raise NotImplementedError('第 4 步还没写：contour_integral —— 见 lab/README.md 任务表第 4 行')


# ══ 第 5 步 ═════════════════════════════════════════════════════
def inside(z0, center, radius):
    """奇点 z0 在围道 |z − center| = radius 的**内部**吗？

    严格小于：距离恰好等于半径时奇点压在围道上，留数定理的两条前提都不满足，
    这一步必须把它判成「不算圈内」。

    提示：判的是 |z0 − center|，不是 |z0|——圆心一挪开原点，用 |z0| 就会数错奇点。
    """
    raise NotImplementedError('第 5 步还没写：inside —— 见 lab/README.md 任务表第 5 行')


# ══ 第 6 步 ═════════════════════════════════════════════════════
def residue_theorem(poles, center, radius):
    """留数定理的右边：2πi ·（圈内各奇点的留数之和）。

    poles 是 (奇点位置, 该点的留数) 的列表，留数已经算好（第 14 课的活）。
    只把第 5 步判成圈内的那些加起来，再乘 TAU；圈外的一项都不算。

    提示：漏乘 TAU 得到的是留数之和（差一个 2πi）；把圈外的也加进来，就是卷面上
    「围道内有两个奇点却只算一个 / 把圈外的也算进去」那一类失分。
    """
    raise NotImplementedError('第 6 步还没写：residue_theorem —— 见 lab/README.md 任务表第 6 行')


# ══ 第 7 步 ═════════════════════════════════════════════════════
def ledger_row(name, f, poles, center, radius, n=CONTOUR_N):
    """账本里的一行：同一条围道，数值积分的值与 2πiΣ留数的值并排。

    返回一个字典，键固定（测试按这几个键读）：

        'case'      案名，原样带回
        'enclosed'  圈内的奇点个数（整数）
        'numeric'   第 4 步算出来的数值围道积分
        'theorem'   第 6 步算出来的 2πiΣ留数
        'gap'       abs(numeric − theorem)
        'verdict'   '一致' 当 gap <= TOL_AGREE，否则 '不一致'

    提示：'enclosed' 用第 5 步数一遍（`sum(1 for z0, _ in poles if inside(...))`），
    别写成 `len(poles)`——S3、S4 就是靠这个数区分的。
    """
    raise NotImplementedError('第 7 步还没写：ledger_row —— 见 lab/README.md 任务表第 7 行')


def ledger_rows(n=CONTOUR_N):
    """（给好）五个配方各算一行，凑成整本账本。"""
    return [ledger_row(name, f, poles, center, radius, n)
            for name, f, poles, center, radius in SPECIMENS]


# ══ 第 8 步 ═════════════════════════════════════════════════════
def save_contour_csv(path, center, radius, poles, n=ART_N):
    """把「围道 + 极点」那张图存成 CSV，返回数据行数（不含表头）。

    列是 `kind,index,re,im,mark`：先写 n 个围道点（kind 写 `contour`），
    再写每个奇点（kind 写 `pole`，mark 按第 5 步写 `圈内` 或 `圈外`）。
    所以一共 n + len(poles) 行。

    提示：这份 CSV 就是图上那条圆与那几个点的坐标；第 10 步的字符画读的是同一批数。
    别用 `{:.6g}` 之外的四位小数——半径 8 的圆周上，四位小数会把相邻两点写成同一个数。
    """
    raise NotImplementedError('第 8 步还没写：save_contour_csv —— 见 lab/README.md 任务表第 8 行')


# ══ 第 9 步 ═════════════════════════════════════════════════════
def write_gallery(out_dir):
    """把四块面板写进同一份 `out/`，并返回画廊总表的四行。

    每行是 `(面板名, 文件名, 数据行数, 一句话结论)`，都用 `write_csv` 写盘：

      | 面板 | 文件 | 行数 | 数据从哪来 |
      |---|---|---|---|
      | panel1-roots | panel1-roots.csv | 5 | `nth_roots(*PANEL1)`，列 `k,re,im` |
      | panel2-arg | panel2-arg.csv | 25 | ARG_WINDOW 里 5×5 个点的 `arg_degrees`，列 `re,im,arg_deg` |
      | panel3-grid | panel3-grid.csv | 24 | GRID_LINES 四条竖线各 6 点、过一遍 z²，列 `line,k,re,im` |
      | panel4-contour | panel4-contour.csv | 182 | 第 8 步，取 S2 那条围道与它的两个奇点 |

    最后再写一份 `gallery.csv`（列 `panel,file,rows,note`，四行），返回那四行。

    提示：四行的形状一样，照第一行抄，只换数据来源；行数由 `write_csv` 返回，别手写死。
    """
    raise NotImplementedError('第 9 步还没写：write_gallery —— 见 lab/README.md 任务表第 9 行')


# ══ 第 10 步 ════════════════════════════════════════════════════
def ascii_canvas(center, radius, poles, width=41, height=21):
    """不装 matplotlib 也能看的那张图：围道与极点画成字符画，返回 height 行字符串。

    约定：`.` 是围道上的点，`*` 是圈内的极点，`o` 是圈外的极点，其余是空格。

    做法：用第 3 步采 ART_N 个点；把所有点（围道 + 极点）的实部虚部各取最小最大值
    当包围盒；每个点按比例落成一格，行号要**上下翻过来**（第 0 行是最上面那行，
    而虚部大的在下面）。

    提示：列下标 `int(round((x - x0) / (x1 - x0) * (width - 1)))`、
    行下标 `height - 1 - int(round((y - y0) / (y1 - y0) * (height - 1)))`。
    先画围道的点，再画极点——极点压在上面才看得见。
    """
    raise NotImplementedError('第 10 步还没写：ascii_canvas —— 见 lab/README.md 任务表第 10 行')
