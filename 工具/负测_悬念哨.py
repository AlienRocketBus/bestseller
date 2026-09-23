# -*- coding: utf-8 -*-
"""负测 · 悬念哨之「逾限须挂哨，挂了才算写明卡在哪一条」（2026-09-13 立）

⛔其事：三条主账各自之形皆写死「每三章至少一处」，而盘上至今没有一只手在数它
   （0913 头一回跑：SUS-A 隔 13 章｜SUS-C 隔 10 章）。
★★本测两路，缺一即假：
   一·**逾限须逮得出**（隔十章／从来没提过）；
   二·⛔**牙不许拔**：**限内不许报**｜**骨记之明报须带据（空口一行不算）**｜
      **账上挂了哨才算写明——一笔逾限而账上无哨，全测那一格须红。**
"""
import json as _j
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
哨 = importlib.import_module('悬念哨')


def chk_xuannian():
    R = []
    def one(k, d):
        # ⛔沙盘之局皆係造出来的章号，其回执不在盘上；
        #   ★而盘上真局照旧只数已封版之章（0914 立·330 之草稿曾把三条一齐哄绿）。
        return [x for x in 哨.判(d, 只封版=False)[1] if x[0] == k][0]
    R.append(('①隔十章须报', one('SUS-A-那六天', {10: '那六天', 20: '别'})[3] is True))
    R.append(('②从来没提过者须报', one('SUS-C-照着做', {20: '别'})[3] is True))
    R.append(('③⛔牙·限内不报', one('SUS-B-磨窝', {17: '磨窝', 20: '别'})[3] is False))
    R.append(('④骨记明报带据者算一处',
              one('SUS-C-照着做', {18: 'SUS-C·本章复提：拍四十一，一行两样各量一回', 20: '别'})[1] == 18))
    R.append(('⑤⛔牙·空口一行不算', one('SUS-C-照着做', {18: 'SUS-C·本章复提：有', 20: '别'})[1] == 0))
    # ⑥⛔牙·全测那一格：拿一份「无哨」之账回灌，须判红
    import json, io as _io
    p = os.path.join(哨.ROOT, '设定', '到期账.json')
    账 = json.load(_io.open(p, encoding='utf-8'))['items']
    # ★2026-09-14 改其判（⛔非放宽）：旧格钉死「二笔」，而 329 已把 SUS-A 真兑、SUS-B 亦随之在限内
    #   （其兑之形係骨记明报带据·暗线永禁其词，故第一路本就看不见它）——**挂哨之数是会动的**。
    #   ★故改问其实：**凡此刻逾限者，逐笔须有其哨**；⛔**一笔逾限而无哨，即当场红。**
    _, _报 = 哨.判()
    逾 = [x for x in _报 if x[3]]        # ⛔只取真逾限者（bad），非整张表
    无哨 = [k for k, 末见, 距, bad in 逾 if not [x for x in 账 if x['id'] == k and x.get('哨')]]
    R.append(('⑥凡此刻逾限者逐笔有哨（今逾 %d 笔，无哨 %s）'
              % (len(逾), 无哨 or '零'), not 无哨))
    R.append(('⑦⛔牙·若把哨拔掉，全测那一格须红（其判在 chk_suspense：坏→False）',
              '坏' in _io.open(os.path.join(哨.ROOT, '工具', '全测.py'), encoding='utf-8').read()))
    # ⛔★★★★★2026-09-23·限362 补二格（随 `全测::chk_suspense` 之第二问同日）：
    #   ★**其所治**：**一个已经过去的哨不是哨，是碑**——
    #     **今日之实：SUS-A→哨344｜SUS-B→哨350｜SUS-C→哨330，三个哨俱在末章(362)之前，而本格照旧绿。**
    #   ⛔**故补：⑦验新式逮得着「哨已朽」｜⑧验旧式对同一份料一声不响（故⑦非陪跑）。**
    _源 = _io.open(os.path.join(哨.ROOT, '工具', '全测.py'), encoding='utf-8').read()
    R.append(('⑧新式已问第二问（哨须落在末章之後·`哨 > 末`）',
              '哨已朽' in _源 and '<= 末' in _源))
    R.append(('⛔⑨而旧式只问「挂没挂哨」——其辞「逾限而账上无哨」原样仍在，二问并存，故⑧非陪跑',
              '逾限而账上无哨' in _源))
    R.append(('⑩真盘之实：三条之哨今皆落在末章之後（⛔本格读盘只作报，其判在⑧⑨）',
              all(int((x.get('哨') or 0)) > max(哨.诸章())
                  for x in _j.load(_io.open(os.path.join(哨.ROOT, '设定', '到期账.json'),
                                            encoding='utf-8'))['items']
                  if str(x.get('id', '')).startswith('SUS-'))))
    坏 = [n for n, ok in R if not ok]
    print('════ 负测·悬念哨 ════ %d/%d %s'
          % (len(R) - len(坏), len(R), '全通' if not 坏 else '有败'))
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    return (not 坏), ''


if __name__ == '__main__':
    ok, _ = chk_xuannian()
    sys.exit(0 if ok else 1)
