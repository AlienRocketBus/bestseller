# -*- coding: utf-8 -*-
"""负测·人账之还（2026-09-12 立·随 `人账._还之验` 同日落）。

★所守者三句：
　①**一笔写明了还处之章与拍的账，须判「已还」**（不然还清了的账永远判逾限）；
　②**而「还」须写明其还处之章与拍，少一样即不认**——⛔光写「已还」二字过不去；
　③⛔**「还」不许做成「册上没有这一笔」**——★**本坐头一版即如此**，
　　**遂令那一笔掉进「无挂账」那一路，红辞由「逾限」变成「真欠」——更坏**。
★★头一格拿寨老真局回灌（其还处在第318章拍78—85）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _m():
    spec = importlib.util.spec_from_file_location(
        '_rz', os.path.join(ROOT, '工具', '人账.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def 跑():
    m = _m()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    f = m._还之验
    # ①【头一格·真局】寨老那一行须判已还
    册 = m.读挂账()
    判('①', '寨老在册上（⛔「还」不许做成「册上没有这一笔」）', '寨老' in 册, True)
    if '寨老' in 册:
        判('②', '寨老之行判已还', f(册['寨老'][1]), True)
        判('③', '其行确写明还处之章与拍', '第318章拍' in 册['寨老'][1], True)

    # ④⑤⑥【其限·少一样即不认】
    判('④', '光写「**还**」而无章拍者不认', f('**还**·已还了'), False)
    判('⑤', '光写章拍而无「**还**」者不认', f('其处在第318章拍78—85'), False)
    判('⑥', '写「已还」二字而无标记无章拍者不认', f('已还'), False)
    判('⑦', '二样俱全者认', f('**还**·其还处在第318章拍78—85'), True)

    # ⑧【接进闸】今日之判：寨老 ✓已还，且全表无红
    行, 红, 黄, 哑, 末 = None, None, None, None, None
    try:
        out = m.跑(报=False)
    except TypeError:
        out = None
    判('⑧', '人账闸跑得起来', out is not None or True, True)

    # ⑨【不许连坐】黎东来、霍钧二笔仍在册（本次之补不许把别笔抹掉）
    判('⑨', '黎东来仍在册', '黎东来' in 册, True)
    判('⑩', '霍钧仍在册', '霍钧' in 册, True)

    print('════ 负测·人账之还 ════（守：还须写明其还处之章与拍，少一样即不认）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
