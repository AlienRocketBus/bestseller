# -*- coding: utf-8 -*-
"""无闸之卡（2026-09-15 立）——**ERROR 之卡，须有一样东西在看着它。**

★**其所由来**：诸席封版之日皆印一句「**ERROR 卡 forbid 正则 430 条跑本章白文 → 命中 0**」，
　**而那一句听起来像「canon 全绿」。**⛔**它不是。**
　0915 逐张亲数（`level=='ERROR'` 递归全档）：
　　**ERROR 卡共 176 张**｜**其中有 `forbid` 正则者 156 张**（那 430 条正则即出於此）｜
　　⛔**其余 20 张，一条正则也没有**；**而那 20 张里，只有 1 张（`F026`）有 `checker`**——
　　⛔⛔**余 19 张：既无正则，也无验码，盘上没有任何一样东西在看着它们。**
★**而它们不是小卡**：`F089_起源定版_两人一机`｜`F090_血契独承与座心玉`｜`F091_玉之本相`｜
　`F095_沈鸢终局锁定`｜`F097_九鼎名录`｜`F098_亡秦账`｜`F099_大禹立鼎`……**皆作者亲笔定版之条。**

★★**本器不冒充能查它们**：**那 19 张之所禁多係「事理」而非「字样」**
　（如「沈鸢终局人质局中自尽＝照旧锁死」），⛔**拿正则去查它，查出来的是假绿，比不查更坏。**
★★★**故本器只办一件事**：**把「没有闸的那一批」数出来，并钉死其数**——
　**新添一张无闸之 ERROR 卡而不记账，即红。**
　⛔**其治不是给它编一条正则**，**是在 `设定/无闸之卡账.md` 上写明「留·其由」或「治·其法」。**
⛔**并禁一句话**：**自本器立日起，封版之印不许再只写「正则 430 条命中 0」**——
　**须同写「另有 N 张无闸之卡未验」**；**一个数报出来而不报它没盖住的那一半，就是拿半个数当全绿。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, json, io, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
库 = os.path.join(ROOT, '设定', 'canon事实库.json')
账 = os.path.join(ROOT, '设定', '无闸之卡账.md')


def 走(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from 走(v)
    elif isinstance(o, list):
        for v in o:
            yield from 走(v)


def 数(d):
    """回 (ERROR总数, 有正则者, 无正则无验码者之 id 表, 无正则而有验码者之 id 表)。"""
    err = [c for c in 走(d) if c.get('level') == 'ERROR']
    有则 = [c for c in err if c.get('forbid') and any(p for p in c['forbid'])]
    无则 = [c for c in err if not (c.get('forbid') and any(p for p in c['forbid']))]
    无闸 = sorted(str(c.get('id')) for c in 无则 if not c.get('checker'))
    有码 = sorted(str(c.get('id')) for c in 无则 if c.get('checker'))
    return len(err), len(有则), 无闸, 有码


def 账上之数():
    """账上钉死的那个数（`钉：N 张`）。⛔账不在即回 None。"""
    if not os.path.exists(账):
        return None, set()
    t = io.open(账, encoding='utf-8').read()
    m = re.search(r'钉：(\d+)\s*张', t)
    ids = set(re.findall(r'`(F\d+_[^`]+)`', t))
    return (int(m.group(1)) if m else None), ids


def 自测():
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))
    D = lambda *cs: {'x': list(cs)}
    E = lambda i, **k: dict(id=i, level='ERROR', **k)

    # ①有正则者不入无闸
    报('①有正则不报', 数(D(E('A', forbid=['x'])))[2], [])
    # ②⛔无正则亦无验码者·入无闸
    报('②无正则无码者报', 数(D(E('B')))[2], ['B'])
    # ③无正则而有验码者·不入无闸（另立一格）
    n, y, w, c = 数(D(E('C', checker='f')))
    报('③有验码不入无闸', w, []); 报('③有验码另计', c, ['C'])
    # ④⛔forbid 係空表者＝无正则（⛔不许当作「有闸」）
    报('④空表算无正则', 数(D(E('D', forbid=[])))[2], ['D'])
    报('④空串亦算无', 数(D(E('E2', forbid=['']))) [2], ['E2'])
    # ⑤非 ERROR 之卡不辖
    报('⑤非ERROR不辖', 数({'x': [dict(id='F', level='WARN')]})[2], [])
    # ⑥⛔递归须及於嵌套（卡藏在 foreshadows/state_canon 之类的深处）
    报('⑥深处亦数得着', 数({'a': {'b': [{'c': E('G')}]}})[2], ['G'])
    # ⑦总数之分：176＝156＋20 之式（有正则＋无正则）
    n2, y2, w2, c2 = 数(D(E('H', forbid=['p']), E('I'), E('J', checker='k')))
    报('⑦总数', n2, 3); 报('⑦有正则', y2, 1); 报('⑦无闸', w2, ['I']); 报('⑦有码', c2, ['J'])

    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 无闸之卡·自测 %d/%d' % ('✓' if 过 == len(格) else '⛔', 过, len(格)))
    return 0 if 过 == len(格) else 1


def 全书():
    d = json.load(io.open(库, encoding='utf-8'))
    总, 有则, 无闸, 有码 = 数(d)
    print('  ERROR 卡 %d 张：有正则 %d｜无正则而有验码 %d｜⛔无正则亦无验码 %d'
          % (总, 有则, len(有码), len(无闸)))
    钉, 账内 = 账上之数()
    if 钉 is None:
        print('⛔ 无闸之卡：账不在（设定/无闸之卡账.md）——**须立账并钉其数**')
        return 1
    新 = [i for i in 无闸 if i not in 账内]
    if len(无闸) != 钉 or 新:
        if 新:
            print('  ⛔账上无名者 %d 张：%s' % (len(新), '、'.join(新)))
        if len(无闸) != 钉:
            print('  ⛔今数 %d 张，而账上钉 %d 张' % (len(无闸), 钉))
        print('⛔ 无闸之卡：有一张 ERROR 卡没有闸而账上未记')
        print('  ★其治⛔不是给它编一条正则（那是假绿）——**是在账上写明「留·其由」或「治·其法」。**')
        return 1
    print('✓ 无闸之卡：无闸者 %d 张，账上逐张有名且其数相符' % len(无闸))
    return 0


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 全书())
