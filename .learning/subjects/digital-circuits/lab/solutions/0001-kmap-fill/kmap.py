"""卡诺图填图（参考解）。

变量次序固定为 A、B、C、D，n 个变量就取前 n 个，A 是最高位。
轴上的标号是格雷码：相邻两个标号只差一位。

    四变量图：行取 AB，列取 CD  → 4 行 4 列
    三变量图：行取 A， 列取 BC  → 2 行 4 列

图用 grid[行下标][列下标] 存，存 0 或 1，下标从 0 起。
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

    取值串按变量次序排，两段标号按行轴、列轴各取走自己那几个变量；
    下标就是那两段标号在各自 gray_axis 里排第几。
    """
    row_vars = ROW_VARS[nvars]
    col_vars = COL_VARS[nvars]
    bits = bits_of(minterm, nvars)
    row_bits = ''.join(bits[VARS.index(name)] for name in row_vars)
    col_bits = ''.join(bits[VARS.index(name)] for name in col_vars)
    row = gray_axis(len(row_vars)).index(row_bits)
    col = gray_axis(len(col_vars)).index(col_bits)
    return row, col


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
    """
    values = tuple(values)
    if len(values) != 2 ** nvars:
        raise ValueError('%d 个变量的真值表应有 %d 行，收到 %d 行'
                         % (nvars, 2 ** nvars, len(values)))
    grid = empty_grid(nvars)
    for minterm, value in enumerate(values):
        put(grid, minterm, nvars, 1 if value else 0)
    return grid


def cells_of_product(term, nvars):
    """一个乘积项落哪几格，返回最小项编号的列表（升序）。

    term 写成 {变量名: 0 或 1}，例如 A'B 是 {'A': 0, 'B': 1}。
    项里没提到的变量，取 0 取 1 都算 —— 逐个枚举全部 2**n 个取值，
    满足 term 里每一条的那些编号就是落点。
    """
    names = VARS[:nvars]
    for name in term:
        if name not in names:
            raise ValueError('%d 个变量里没有 %s' % (nvars, name))
    found = []
    for minterm in range(2 ** nvars):
        bits = bits_of(minterm, nvars)
        if all(int(bits[names.index(name)]) == value
               for name, value in term.items()):
            found.append(minterm)
    return found


def fill_from_products(nvars, terms):
    """一串乘积项 → 图。重叠的格重复填 1，仍是 1。"""
    grid = empty_grid(nvars)
    for term in terms:
        for minterm in cells_of_product(term, nvars):
            put(grid, minterm, nvars, 1)
    return grid


def minterms_from_grid(grid, nvars):
    """图 → 升序的最小项编号列表（给图取式：扫一遍图，报出是 1 的格号）。"""
    row_vars = ROW_VARS[nvars]
    col_vars = COL_VARS[nvars]
    row_axis = gray_axis(len(row_vars))
    col_axis = gray_axis(len(col_vars))
    found = []
    for row, row_label in enumerate(row_axis):
        for col, col_label in enumerate(col_axis):
            if grid[row][col]:
                bits = ['0'] * nvars
                for name, value in zip(row_vars, row_label):
                    bits[VARS.index(name)] = value
                for name, value in zip(col_vars, col_label):
                    bits[VARS.index(name)] = value
                found.append(int(''.join(bits), 2))
    found.sort()
    return found
