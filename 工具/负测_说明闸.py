# -*- coding: utf-8 -*-
"""负测·说明闸（2026-09-13 立·325 之席三轮连栽，原样报上来的那一条）。

★所守者一句：**存版之说明须是一句人看得懂的话；汉字少於四个即当场拒收。**
★★其实（325 之席自书於台账「重开·记因」，⛔原样报上，本坐今日方治）：
　**v06 之说明误存为占位字「x」**｜**v09 说明误存占位字「x」**｜**v15 之说明存成了空**
　——**三轮连栽**；其自书逐字：「**存版口须把「说明为空／单字」焊成当场拒收**」。
★★★**并及本坐自己犯的同一样**：**0913 拿真器做探针，把「t」「probe」真存进了台账**
　（**v01「test」／v03「probe」／v10「x」之来历，即此**）——⛔**一版未删，只补说明。**
⛔**其害不在难看**：**台账之说明即轮号之源**（`_round_of(说明)`）——
　**说明一空，那一版就没有号；`--写轮记` 遂拒（「不许以第?轮起头」），
　而那一轮的刀已经落在正文里了**：**活干了，账上没有它。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io
import os
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mod():
    spec = importlib.util.spec_from_file_location(
        '_pl', os.path.join(ROOT, '工具', '跑轮.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def 跑():
    m = _mod()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    def L(vs=None):
        return {'章': 1, '版本': vs or []}

    def 拦(note, **kw):
        h, g = m.gates(1, note, L(), 1, [], **kw)
        return bool(h) and any('说明闸' in x for x in g)

    # ①—④【真局回灌】325 三轮连栽之形＋本坐探针之形
    判('①', '⛔空说明拒收（325 v15 真局）', 拦(''), True)
    判('②', '⛔单字「x」拒收（325 v06／v09 真局）', 拦('x'), True)
    判('③', '⛔「probe」拒收（0913 本坐探针之真局）', 拦('probe'), True)
    判('④', '⛔「test」拒收（v01 之来历）', 拦('test'), True)

    # ⑤⑥⑦【真说明照旧放行·⛔不许一立闸就把活人也拦下】
    判('⑤', '第N轮·某某庭 放行', 拦('第3轮·校对'), False)
    判('⑥', '终版回补 放行', 拦('终版回补·器物'), False)
    判('⑦', '回补／定案 放行', 拦('回补·定案'), False)

    # ⑧⛔force 不免此闸（ZM_FORCE 是为「闸判错了」留的口，而空说明无对错可判）
    判('⑧', '⛔force 不免（空说明照旧拦）', 拦('x', force='审毕判不补'), True)

    # ⑨⛔reopen 亦不免
    判('⑨', '⛔reopen 不免（空说明照旧拦）', 拦('', reopen='重开之由'), True)

    # ⑩【证其界在「四个汉字」上，不是在长度上】
    判('⑩之一', '三个汉字仍拦', 拦('校对了'), True)
    判('⑩之二', '四个汉字即放', 拦('本轮校对'), False)

    # ⑪⛔而此闸不许把别的闸挤掉：真说明之版，其余诸闸照旧判
    h, g = m.gates(1, '第1轮·起草', L(), 1,
                   [os.path.join('设定', '回执_x_第1章作业单.md')])
    判('⑪', '真说明之版，回执闸照旧拦（⛔本闸未把别的闸挤掉）',
       bool(h) and any('回执闸' in x for x in g), True)

    print('════ 负测·说明闸 ════（守：说明须成一句话·汉字<4 即拒）')
    for x in 败:
        print('  ⛔ ' + x)
    print(('  ✓ %d/%d 全通' % (过, 过 + len(败))) if not 败
          else '  ⛔ %d/%d 有败' % (过, 过 + len(败)))
    return not 败


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
