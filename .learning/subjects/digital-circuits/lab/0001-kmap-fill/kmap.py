"""卡诺图填图：把真值表与表达式搬到方格上。

变量次序固定为 A、B、C、D，n 个变量就取前 n 个，A 是最高位。
轴上的标号是格雷码：相邻两个标号只差一位。

    四变量图：行取 AB，列取 CD  → 4 行 4 列
    三变量图：行取 A， 列取 BC  → 2 行 4 列

图用 grid[行下标][列下标] 存，存 0 或 1，下标从 0 起。
本文件里有 4 个函数留白（任务 1 与任务 2），别的都写好了，不用改。
"""

VARS = 'ABCD'

# 一条轴放几个变量 → 标号序列（从图的左上角起，从左往右 / 从上往下）
GRAY = {
    0: ('',),
    1: ('0', '1'),
    2: ('00', '01', '11', '10'),
}

# 哪个变量放行轴、哪几个放列轴
ROW_VARS = {3: 'A', 4: 'AB'}
COL_VARS = {3: 'BC', 4: 'CD'}


def gray_axis(nbits):
    """返回 nbits 位轴的标号序列。"""
    if nbits not in GRAY:
        raise ValueError('本课只用 0~2 位的轴，收到 %r' % (nbits,))
    return GRAY[nbits]


def bits_of(minterm, nvars):
    """最小项编号 → 取值串，例如 bits_of(5, 3) == '101'。"""
    return format(minterm, '0%db' % nvars)


def cell_of(minterm, nvars):
    """最小项编号 → (行下标, 列下标)。

    任务 1 留白。做法提示：
    把 bits_of 得到的取值串，按 ROW_VARS / COL_VARS 切成两段标号，
    再各到 gray_axis 里查下标。
    """
    raise NotImplementedError('任务 1：编号 → 格，先做这一个')


def empty_grid(nvars):
    """开一张全 0 的图。"""
    rows = len(gray_axis(len(ROW_VARS[nvars])))
    cols = len(gray_axis(len(COL_VARS[nvars])))
    return [[0] * cols for _ in range(rows)]


def put(grid, minterm, nvars, value=1):
    """把一格填成 value。"""
    row, col = cell_of(minterm, nvars)
    grid[row][col] = value


def fill_from_table(nvars, values):
    """真值表 → 图。

    values 的第 i 项，就是取值串 bits_of(i, nvars) 那一行的输出。
    任务 1 留白。
    """
    raise NotImplementedError('任务 1：逐行把 values 搬到格上')


def cells_of_product(term, nvars):
    """一个乘积项落哪几格，返回最小项编号的列表。

    term 写成 {变量名: 0 或 1}，例如 A'B 是 {'A': 0, 'B': 1}。
    项里没提到的变量，取 0 取 1 都算，所以缺 k 个变量就落 2**k 格。
    任务 2 留白。
    """
    raise NotImplementedError("任务 2：A'B 该落几格？")


def fill_from_products(nvars, terms):
    """一串乘积项 → 图。任务 2 留白。"""
    raise NotImplementedError('任务 2：逐项落 1，重叠的格只留一个 1')


def minterms_from_grid(grid, nvars):
    """图 → 升序的最小项编号列表（这是填图的反方向：给图取式）。

    任务 1 的反方向留白：把两条轴的标号拼回取值串，再读成编号。
    """
    raise NotImplementedError('任务 1 的反方向：扫一遍图，报出所有是 1 的格号')
