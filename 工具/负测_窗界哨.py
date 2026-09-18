# -*- coding: utf-8 -*-
"""负测 · 窗界哨（2026-09-18 立·随本哨同日落）

⛔**本哨之立，是因为同一个形一日之内咬了四回**；**故本测之要，是压住它别变成一件摆设**：
①**它得真找得着**（造一个缺界之窗，须入其报单）；
②**它不许乱抓**（二界俱全者，⛔不许入报单）；
③**它得数得出「答过几条」**（⛔否则又是一道「报了没人答」之哨·`体检账 九十一`）；
④⛔**它不许把自己漏掉，也不许把自己算进去**（本哨自己那一行窗式，须不入其报单）。
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import 窗界哨 as W

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 跑():
    局, rows = [], W.扫()
    名 = set(r[0] for r in rows)

    # ①真找得着：本坐今日亲改之三处，其一在报单里
    局.append(('①找得着·`开轮六检.py` 之缺界者在报单里', '开轮六检.py' in 名))
    # ②不许乱抓：二界俱全之式不许入单
    _式 = W._窗
    局.append(('②二界俱全者不入单（`[^。\\n]{0,40}` 之形）',
               not [1 for m in _式.finditer("x = r'[^。\\n]{0,40}'") if
                    ('。' not in m.group(1)) or ('\\n' not in m.group(1))]))
    # ②之b 缺句号者须判缺
    m = list(_式.finditer("y = r'[^\\n]{0,40}'"))
    局.append(('②之b 缺句号者须判「缺。」', bool(m) and '。' not in m[0].group(1)))
    # ②之c 缺换行者须判缺
    m2 = list(_式.finditer("z = r'[^。]{0,40}'"))
    局.append(('②之c 缺换行者须判「缺换行」', bool(m2) and '\\n' not in m2[0].group(1)))
    # ③数得出答过几条
    zh = os.path.join(ROOT, '设定', '窗界账.md')
    局.append(('③`设定/窗界账.md` 在（⛔报了没人答等於没报）', os.path.exists(zh)))
    if os.path.exists(zh):
        t = io.open(zh, encoding='utf-8').read()
        局.append(('③之b 账上已答者 ≥3 条（本坐当日先答三条作样，⛔不许立完就空着）',
                   len(re.findall(r'^\|\s*✅', t, re.M)) >= 3))
        局.append(('③之c 账自书其限，且写明到期即升硬项', '其限 358' in t and '升作硬项' in t))
        局.append(('③之d ⛔账须明写「入报单不等於它错了」（免下一坐把 37 处一律改成一个样子）',
                   '不等於' in t and '不挡句号是对的' in t))
    # ④本哨不许把自己算进去
    局.append(('④本哨自己那一行窗式不入报单（⛔否则它每回都报自己一处）',
               '窗界哨.py' not in 名))

    红 = 0
    print('════ 负测 · 窗界哨（%d 局）════' % len(局))
    for n, r in 局:
        print('  %s %s' % ('✓' if r else '⛔', n))
        if not r:
            红 += 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    sys.exit(1 if 跑() else 0)
