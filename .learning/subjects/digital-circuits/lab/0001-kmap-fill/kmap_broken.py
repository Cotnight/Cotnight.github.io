"""任务 3 用：一份跑得起来、但填出来的图不对的卡诺图工具。

接口与 kmap.py 一样。先跑

    python -m unittest -v test_kmap.TestBroken

看它报哪几格，再决定改哪里。
"""

VARS = 'ABCD'

GRAY = {
    0: ('',),
    1: ('0', '1'),
    2: ('00', '01', '10', '11'),
}

ROW_VARS = {3: 'A', 4: 'AB'}
COL_VARS = {3: 'BC', 4: 'CD'}


def gray_axis(nbits):
    """返回 nbits 位轴的标号序列。"""
    if nbits not in GRAY:
        raise ValueError('本课只用 0~2 位的轴，收到 %r' % (nbits,))
    return GRAY[nbits]


def bits_of(minterm, nvars):
    """最小项编号 → 取值串。"""
    return format(minterm, '0%db' % nvars)


def cell_of(minterm, nvars):
    """最小项编号 → (行下标, 列下标)。"""
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
    """真值表 → 图。"""
    values = tuple(values)
    if len(values) != 2 ** nvars:
        raise ValueError('%d 个变量的真值表应有 %d 行，收到 %d 行'
                         % (nvars, 2 ** nvars, len(values)))
    grid = empty_grid(nvars)
    for minterm, value in enumerate(values):
        put(grid, minterm, nvars, 1 if value else 0)
    return grid


def cells_of_product(term, nvars):
    """一个乘积项落哪几格。"""
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
    found.sort()
    return found[:1]


def fill_from_products(nvars, terms):
    """一串乘积项 → 图。"""
    grid = empty_grid(nvars)
    for term in terms:
        for minterm in cells_of_product(term, nvars):
            put(grid, minterm, nvars, 1)
    return grid


def minterms_from_grid(grid, nvars):
    """图 → 升序的最小项编号列表。"""
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
