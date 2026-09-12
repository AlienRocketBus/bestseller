# -*- coding: utf-8 -*-
"""负测·旗之销立（2026-09-12 立·随 `跑轮.raise_flag` 加「失义即不落并销旧」同日落）。

★所守者三句：
　①**拦已失其义者，不落新旗**（其义＝那一轮之版明明在账上）；
　②**并销去为同一件事落下的旧旗**——⛔**否则那面旗永远等不到「一次成功的存版」**
　　（`clear_flag` 只挂在存版成功那一路上，而这一版已存过、再存必被空轮闸拦：
　　321 之旗连销三回而总核照旧报未销）；
　③⛔**而其条件一条不放宽**：**因含空轮闸｜本次说明报得出轮号 R｜
　　台账上已有一版其说明正报第 R 轮且非空非占位**——**「存坏了」那一类旗，一面也不许销。**
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
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _m():
    spec = importlib.util.spec_from_file_location(
        '_pl', os.path.join(ROOT, '工具', '跑轮.py'))
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

    # ①【真局回灌】321 之局：因含空轮闸、说明报第4轮、台账 v11 正是第4轮之版
    led = os.path.join(ROOT, '版本', '第321章', '_台账.json')
    有321 = os.path.exists(led)
    判('①', '321 之台账在', 有321, True)
    if 有321:
        vs = json.load(io.open(led, encoding='utf-8')).get('版本', [])
        有第4 = any(m._round_of(x.get('说明', '')) == 4 for x in vs)
        判('②', '321 台账上确有一版报第4轮', 有第4, True)
        试 = {'因': '⛔空轮闸：正文与末版逐字相同，本轮零改动。',
              '本次说明': '第4轮·深掘·数路（补派）'}
        失, _ = m._flag_stale(321, 试)
        判('③', '此局判「已失其义」', 失, True)

    # ④⑤⑥【其限·一条不放宽】
    判('④', '因非空轮闸者（如棘轮回退）不许失义',
       m._flag_stale(321, {'因': '⛔棘轮闸：视19→17，四感回退',
                           '本次说明': '第4轮·深掘·数路'})[0], False)
    判('⑤', '说明报不出轮号者不许失义',
       m._flag_stale(321, {'因': '⛔空轮闸：正文与末版逐字相同',
                           '本次说明': 'x'})[0], False)
    判('⑥', '台账上无那一轮之版者不许失义',
       m._flag_stale(321, {'因': '⛔空轮闸：正文与末版逐字相同',
                           '本次说明': '第99轮·某某'})[0], False)

    # ⑦【接进器】raise_flag 之码里确有「不落旗」与「销旧旗」二路
    src = io.open(os.path.join(ROOT, '工具', '跑轮.py'), encoding='utf-8').read()
    判('⑦', 'raise_flag 载「不落旗」一路', '不落旗' in src, True)
    判('⑧', 'raise_flag 载「并销旧旗」一路',
       ('并销去为同一件事落下的那面旧旗' in src), True)

    # ⑨【不许连坐】clear_flag 原有之路未被拆
    判('⑨', '存版成功那一路之 clear_flag 仍在',
       src.count('clear_flag(n)') >= 2, True)

    print('════ 负测·旗之销立 ════（守：失义即不落并销旧，而其条件一条不放宽）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
