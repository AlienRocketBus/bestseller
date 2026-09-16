# -*- coding: utf-8 -*-
"""负测·末行之判（2026-09-16 立·治 `chk_wuzha` 之假红）

⛔**其所治之局**：`全测.py::chk_wuzha` 旧判作 `if '⛔' in out2`，
　**而 `无闸之卡.py` 自己的栏目之标里就带着那一个字**——
　`ERROR 卡 176 张：有正则 156｜无正则而有验码 1｜⛔无正则亦无验码 19`；
　**其末行实印 `✓ 无闸之卡：无闸者 19 张，账上逐张有名且其数相符`（rc=0、自测 12/12）。**
★★**更坏的一层**：旧式红了之後去捡「以⛔起头之行」，**一行也捡不着**（那个字在行中不在行首），
　**遂回一句「账与今数不符」——一句它根本没有验过的话。**

★**本负测之骨**（承 `负测_全测崩绿.py` 之式）：**旧式须在此局上照旧判错，新式须判对。**
⛔**若旧式也过，那本负测就是陪跑**——**故每一格都同笔跑一遍旧式并验它确实错。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, io, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 旧式(out, 项名=None):
    """⛔旧判之原样复刻：印里有⛔即红，再去捡以⛔起头之行。"""
    if '⛔' in out:
        bad = [l.strip() for l in out.splitlines() if l.strip().startswith('⛔')]
        return False, (bad[0][:90] if bad else '账与今数不符')
    return True, '绿'


def 取新式():
    spec = importlib.util.spec_from_file_location('_qc', os.path.join(ROOT, '工具', '全测.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.判末行


# ★真局逐字（2026-09-16 `python3 工具/无闸之卡.py` 之印，逐行照抄）
真局 = (u'════ 无闸之卡 ════\n'
        u'  ERROR 卡 176 张：有正则 156｜无正则而有验码 1｜⛔无正则亦无验码 19\n'
        u'✓ 无闸之卡：无闸者 19 张，账上逐张有名且其数相符\n')
# ⛔真红之局（其数与账不符时之印）
真红 = (u'════ 无闸之卡 ════\n'
        u'  ERROR 卡 177 张：有正则 156｜无正则而有验码 1｜⛔无正则亦无验码 20\n'
        u'⛔ 无闸之卡：无闸者 20 张，而账上只 19 张——新添一张而未记账\n')


def 自测():
    判末行 = 取新式()
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))

    # ①★真局·新式判绿
    报('①真局新式绿', 判末行(真局, '无闸之卡')[0], True)
    # ②⛔同一真局·旧式判红（⛔若此格为 True，本负测即陪跑）
    报('②真局旧式红·非陪跑', 旧式(真局)[0], False)
    # ③⛔旧式红了还捡不着行，回一句没验过的话
    报('③旧式回一句没验过的话', 旧式(真局)[1], '账与今数不符')
    # ④★真红·新式judgment仍红（⛔不许把闸放松到连真红也过）
    报('④真红新式仍红', 判末行(真红, '无闸之卡')[0], False)
    # ⑤★真红之由取自末行本身，非造语
    报('⑤真红之由取自末行', 判末行(真红, '无闸之卡')[1].startswith('⛔ 无闸之卡'), True)
    # ⑥⛔项名对不上者判红（不许拿别家的✓冒充）
    报('⑥项名对不上即红', 判末行(真局, '档肿哨')[0], False)
    # ⑦⛔空印判红（器崩而印空）
    报('⑦空印即红', 判末行('', '无闸之卡'), (False, '无印'))
    # ⑧★末行之後有空行者不误判
    报('⑧末尾空行不误判', 判末行(真局 + '\n\n  \n', '无闸之卡')[0], True)
    # ⑨★「✓ 项名」带一格空白者亦认
    报('⑨带空白之式亦认', 判末行('✓ 档肿哨：无肿到推不上去之档\n', '档肿哨')[0], True)

    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 负测·末行之判 %d/%d 全通' % ('✓' if 过 == len(格) else '⛔', 过, len(格)))
    return 0 if 过 == len(格) else 1


if __name__ == '__main__':
    sys.exit(自测())
