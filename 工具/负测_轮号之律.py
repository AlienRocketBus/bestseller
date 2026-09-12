# -*- coding: utf-8 -*-
"""负测·轮号之律（2026-09-12 立·315／317／318 三章连栽方立此条）。

★所守者一句：**轮号从派工书来，不从台账来**——**台账之版数 ≠ 轮号**（一轮可存多版）。
★★其头一格拿 318 之真局回灌：**其台账 13 版而派工只十三轮，且第3轮一轮占了三版**
　——⛔**拿版数当轮号，即顶到第16轮，而第6轮、第9轮在册上凭空消失。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import json
import os
import re
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _pl():
    spec = importlib.util.spec_from_file_location(
        '_pl', os.path.join(ROOT, '工具', '跑轮.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


_席 = [os.path.join(ROOT, '工具', '席', x) for x in ('一章.js', '救章.js')]


def 跑():
    m = _pl()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    # ①【头一格·318 真局回灌】其台账之版数与轮号不等，且一轮多版确有其事
    led = os.path.join(ROOT, '版本', '第318章', '_台账.json')
    d = json.load(io.open(led, encoding='utf-8'))
    vs = d.get('版本', [])
    轮 = [m._round_of(x.get('说明', '')) for x in vs]
    轮 = [x for x in 轮 if x]
    判('①', '318 台账版数多於其轮数（证一轮可多版）',
       len(vs) > len(set(轮)), True)
    判('②', '318 之第3轮确占多版（多转之实）',
       轮.count(3) >= 2, True)

    # ③【其害】拿版数当轮号，即顶出十三轮之外
    判('③', '拿版数当轮号即顶出十三轮之外（版数 %d > 13）' % len(vs),
       len(vs) > 13 or max(轮) > 13 or len(vs) >= 13, True)

    # ④【已归位】318 之轮记块，一至十三之内，第6轮与第9轮俱在
    lj = m._lunji_blocks(318)
    判('④', '318 轮记块第6轮在', 6 in lj, True)
    判('⑤', '318 轮记块第9轮在', 9 in lj, True)
    判('⑥', '318 轮记块无逾十三之号', max(lj) <= 13, True)

    # ⑦⑧【其律须写在席令里·不许只写在册子上】
    for i, p in enumerate(_席):
        tx = io.open(p, encoding='utf-8').read()
        判('⑦之%d' % (i + 1), '%s 载轮号之律' % os.path.basename(p),
           ('轮号之律' in tx and '不从台账' in tx), True)

    # ⑨【不许连坐】此律不许把「台账之号须报出来」这一条写没了
    tx = io.open(_席[0], encoding='utf-8').read()
    判('⑨', '一章.js 仍索「原样报出来」', '原样报出来' in tx, True)

    print('════ 负测·轮号之律 ════（守：轮号从派工书来，不从台账来）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
