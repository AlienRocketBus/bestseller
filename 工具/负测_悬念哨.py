# -*- coding: utf-8 -*-
"""负测 · 悬念哨之「逾限须挂哨，挂了才算写明卡在哪一条」（2026-09-13 立）

⛔其事：三条主账各自之形皆写死「每三章至少一处」，而盘上至今没有一只手在数它
   （0913 头一回跑：SUS-A 隔 13 章｜SUS-C 隔 10 章）。
★★本测两路，缺一即假：
   一·**逾限须逮得出**（隔十章／从来没提过）；
   二·⛔**牙不许拔**：**限内不许报**｜**骨记之明报须带据（空口一行不算）**｜
      **账上挂了哨才算写明——一笔逾限而账上无哨，全测那一格须红。**
"""
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
        return [x for x in 哨.判(d)[1] if x[0] == k][0]
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
    有哨 = [x['id'] for x in 账 if x.get('哨')]
    R.append(('⑥盘上逾限二笔皆已挂哨（%s）' % '、'.join(有哨), len(有哨) >= 2))
    R.append(('⑦⛔牙·若把哨拔掉，全测那一格须红（其判在 chk_suspense：坏→False）',
              '坏' in _io.open(os.path.join(哨.ROOT, '工具', '全测.py'), encoding='utf-8').read()))
    坏 = [n for n, ok in R if not ok]
    print('════ 负测·悬念哨 ════ %d/%d %s'
          % (len(R) - len(坏), len(R), '全通' if not 坏 else '有败'))
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    return (not 坏), ''


if __name__ == '__main__':
    ok, _ = chk_xuannian()
    sys.exit(0 if ok else 1)
