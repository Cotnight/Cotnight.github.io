"""整批报告：一行一道题，先给判定，再给依据（反例 / 反例为零），最后是出处。

    python report.py

依据那一栏就是这次实验要交的东西：判「有效」要说得出「全部 2^n 个赋值里
没有一个让前提全真而结论为假」；判「无效」要说得出「是哪一个赋值」。

这个文件已经写好了，不用改——它只调用 engine.py 里你填的那几个函数。
你填得对不对，看这里打出来的东西对不对。
"""

import cases
import engine


def counterexample_text(case):
    """依据那一栏：'反例 0 / 16'，或 '反例 01（P=0，Q=1）'。"""
    variables = engine.variables_of(list(case['premises']) + [case['conclusion']])
    found = engine.counterexamples(case['premises'], case['conclusion'], variables)
    if not found:
        return '反例 0 / %d' % len(engine.valuations(variables))
    return '反例 ' + '、'.join(engine.format_env(env, variables) for env in found)


def report_line(case):
    """一道题一行：编号｜判定｜依据｜出处。"""
    verdict = '有效' if engine.is_valid(case['premises'], case['conclusion']) else '无效'
    return '%s｜%s｜%s｜%s' % (case['no'], verdict, counterexample_text(case), case['source'])


def main():
    print('编号｜判定｜依据｜出处')
    for case in cases.CASES:
        print(report_line(case))


if __name__ == '__main__':
    main()
