# -*- coding: utf-8 -*-
"""负测 · 到期账之「一样东西只许一个键名」（2026-09-13 立）

⛔其事：一笔账销了，其章写在哪个键上，盘上有两种写法——
   **`清偿章` 133 笔｜`结账章` 11 笔**；**而 `书级体检.py::check_due_net` 只读 `清偿章`**。
★**故那十一笔在账上看着已销，在闸眼里从来没有销过**（296／298／301／307／328 五处皆有）。
⛔**其害不在某一笔**：**净额那一条闸，量的是「开的线与收的线之差」**——
   **收的那一头漏掉十一笔，它报出来的红就不是书的红，是键名的红。**

★★本测两路，缺一即假：
   一·**盘上不许再有第二个键名**（`结账章`／`结帐章`／`销账章` 之类一个不许有）；
   二·⛔**牙不许拔**：**`书级体检` 之算须真读得着 `清偿章`**——
      **拿一笔造出来的销回灌，其净额须跟着落一格**；**读不着即是这一条白改。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, json, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
体检 = importlib.import_module('书级体检')

别名 = ('结账章', '结帐章', '销账章', '清账章', '了账章')


def chk_zhangjian():
    R = []
    p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     '设定', '到期账.json')
    it = json.load(io.open(p, encoding='utf-8'))['items']
    坏 = [(x['id'], k) for x in it for k in 别名 if k in x]
    R.append(('①盘上无第二个销之键名（今 %s）' % (坏 or '零'), not 坏))
    n清 = sum(1 for x in it if isinstance(x.get('清偿章'), int))
    R.append(('②`清偿章` 仍在且不空（今 %d 笔）' % n清, n清 > 100))
    # ③⛔牙·体检之算须真读得着 `清偿章`：造二局相减
    cur = 328
    基 = [{'id': 'a', '立账章': cur, '状态': 'open'}]
    销 = [{'id': 'a', '立账章': cur, '状态': 'done', '清偿章': cur}]
    try:
        r1 = 体检.check_due_net(基, cur)
        r2 = 体检.check_due_net(销, cur)
        def 取(r):
            for v in (r if isinstance(r, (list, tuple)) else [r]):
                if isinstance(v, (int, float)):
                    return v
            return None
        a, b = 取(r1), 取(r2)
        R.append(('③⛔牙·一笔销落进去，净额须落一格（%s→%s）' % (a, b),
                  a is not None and b is not None and b == a - 1))
    except Exception as e:
        R.append(('③体检之算跑得动（%s）' % e, False))
    # ④⛔牙·别名之局回灌：写作 `结账章` 者，体检须**不**认（证其只读一个键）
    别 = [{'id': 'a', '立账章': cur, '状态': 'done', '结账章': cur}]
    try:
        r3 = 体检.check_due_net(别, cur)
        def 取(r):
            for v in (r if isinstance(r, (list, tuple)) else [r]):
                if isinstance(v, (int, float)):
                    return v
        R.append(('④⛔牙·别名写法体检不认（故盘上不许有它）', 取(r3) == 取(体检.check_due_net(基, cur))))
    except Exception as e:
        R.append(('④别名之局跑得动（%s）' % e, False))
    坏项 = [n for n, ok in R if not ok]
    print('════ 负测·账键一名 ════ %d/%d %s'
          % (len(R) - len(坏项), len(R), '全通' if not 坏项 else '有败'))
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    return (not 坏项), ''


if __name__ == '__main__':
    ok, _ = chk_zhangjian()
    sys.exit(0 if ok else 1)
