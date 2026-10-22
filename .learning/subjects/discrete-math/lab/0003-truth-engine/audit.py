"""第 5 步的对账：先在纸上判一遍，再让引擎判一遍，两边逐题比。

    python audit.py

两轮：

    第一轮  引擎 vs 课件     engine.mismatches(cases.CASES, book_answers())
    第二轮  引擎 vs 你纸上    engine.mismatches(cases.CASES, MY_ANSWERS)

两轮都「对不上 0 道」，这一节的第 5 步才算过。第二轮报出来的那几道，
先跑 `python report.py` 找出那道题的反例，把那个赋值逐行代进前提验一遍：
反例确实成立的话，你纸上那份「证明」一定在某一行偷偷用了结论——
1.8 里最隐蔽的一处错法就在这里。

一份答案表写成 {编号: True/False}，True 表示「有效」（与 cases.py 的 'book' 字段同一个意思）。
对账不是「让程序替我判」，是先判再对：顺序倒过来，对的只是格式，
你哪一题判反了反而看不出来。
"""

import cases
import engine


def book_answers():
    """课件给的答案：{编号: True/False}。每次现取一份，改它不会污染题库。"""
    return {case['no']: case['book'] for case in cases.CASES}


# ── 我的答案（第 5 步：这 16 道先在纸上判一遍）─────────────────
#
# 纸上有过的照纸上抄，没写过的当场判；判的时候只问一句：
# 有没有一个赋值让「前提全真」而「结论为假」？
# 有，写 False，并把那个赋值（如 '01'）记在行末注释里；一个都没有，写 True。
# 16 道都要填：漏填的那几道在第二轮的表里显示「（没填）」，
# TestMyAnswers.test_all_filled 也会直接红。

MY_ANSWERS = {
    # 'C01': True,    # 一行一道：True 有效 / False 无效
}


def verdict_text(answer):
    """True → '有效'，False → '无效'，None（答案表里没有这一题）→ '（没填）'。"""
    if answer is None:
        return '（没填）'
    return '有效' if answer else '无效'


def audit_round(answers):
    """对一轮账：返回对不上的那些行，一道一行，按题库顺序。

    行长这样：'C11｜引擎 无效｜答案 有效｜肯定后件：无效式的样板'。
    全对上是空列表——空表就是这一轮的成绩。
    """
    lines = []
    for no, engine_says, answer_says in engine.mismatches(cases.CASES, answers):
        lines.append('%s｜引擎 %s｜答案 %s｜%s' % (
            no,
            verdict_text(engine_says),
            verdict_text(answer_says),
            cases.by_no(no)['source'],
        ))
    return lines


def print_lines(lines):
    """一道一行，缩进两格打在标题下面；没有对不上的就什么也不打。"""
    for line in lines:
        print('  ' + line)


def main():
    book = book_answers()
    first = audit_round(book)
    second = audit_round(MY_ANSWERS)

    print('第一轮 引擎 vs 课件：对不上 %d 道' % len(first))
    print_lines(first)
    print()
    print('第二轮 引擎 vs 你纸上：你填了 %d 道，对不上 %d 道'
          % (len(MY_ANSWERS), len(second)))
    print_lines(second)
    print()

    if not first and not second:
        print('全部对上。')
    else:
        print('还有 %d 道对不上：先跑 python report.py 看那几道的反例，'
              '再把赋值逐行代进前提验一遍。' % (len(first) + len(second)))


if __name__ == '__main__':
    main()
