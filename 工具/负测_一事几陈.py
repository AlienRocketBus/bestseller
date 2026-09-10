# -*- coding: utf-8 -*-
"""负测·一事几陈（2026-09-02·293第12轮立）

★所验之器：`工具/一事几陈.py::陈`——**把一命题之数陈摆在一起。**
★★其要害在③与④：**以293改前之正文（版本/第293章/v22.md）回灌，拍36须中四词**；
   **以改後（v23／今正文）回灌，拍36须只中二词**——
   ★★★**一份在改前改後都印同一个数的测，就是陪跑（令§六③）。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, rel):
    sp = _iu.spec_from_file_location(name, os.path.join(ROOT, '工具', rel))
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


_m = _load('_ysjc', '一事几陈.py')
_mb = _load('_bd2', '比带.py')
WS = ['浅', '轻', '停', '手', '记号', '事']
案 = []


def _t(名, 得, 期):
    案.append((名, 得 == 期, 得, 期))


def _拍中词(txt, want_sub):
    """★於一段白文里，找含 want_sub 之拍，返其命中之词数（无则 None）。"""
    for p in _mb._拍(txt):
        if want_sub in p:
            return sum(1 for w in WS if w in p)
    return None


def _v(k):
    p = os.path.join(ROOT, '版本', '第293章', 'v%02d.md' % k)
    return io.open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def 跑():
    今 = _mb._白(293)

    # ①器出得来，且不判（返回码0）
    _t('①器可跑', _m.陈(293, WS), 0)

    # ②改後·拍27仍中四词（此拍是第二陈，留着）
    _t('②改後拍27中四词', _拍中词(今, '浅不是那天有什么事'), 4)

    # ③★★★改前（v22）·拍36须中四词以上——**旧式下须显形**
    v22 = _v(22)
    if v22:
        _t('③改前拍36中≥4词', (_拍中词(v22, '停手那一下是我手上出的') or 0) >= 4, True)
    else:
        _t('③改前拍36中≥4词', 'SKIP·v22不在', True)

    # ④★★★改後·同一处只中二词（改前改後须印不同的数）
    _t('④改後拍36中二词', _拍中词(今, '我拿它当记号'), 2)

    # ⑤改前之三陈俱在候选之列
    if v22:
        ps = _mb._拍(v22)
        hit = [i for i, p in enumerate(ps, 1) if sum(1 for w in WS if w in p) >= 2]
        _t('⑤改前三陈俱在候选', all(x in hit for x in (17, 27, 36)), True)
    else:
        _t('⑤改前三陈俱在候选', 'SKIP·v22不在', True)

    # ⑥改後拍36仍在候选（它没被删，只削了首句）——★候选不等於该删
    ps = _mb._拍(今)
    hit = [i for i, p in enumerate(ps, 1) if sum(1 for w in WS if w in p) >= 2]
    _t('⑥改後拍36仍在候选', 36 in hit, True)

    # ⑦候选之数：改前须多於改後（一命题三陈减为二陈）
    if v22:
        h0 = sum(1 for p in _mb._拍(v22) if sum(1 for w in WS if w in p) >= 2)
        _t('⑦改前候选多於改後', h0 > len(hit), True)
    else:
        _t('⑦改前候选多於改後', 'SKIP·v22不在', True)

    # ⑧只中一词者不入候选（否则一部书全是候选，器即废）
    _t('⑧中一词不入候选',
       any(sum(1 for w in WS if w in p) == 1 for p in ps) and
       all(sum(1 for w in WS if w in p) >= 2 for i, p in enumerate(ps, 1) if i in hit), True)

    # ⑨--词 明给者，不去读开镜卡（章无卡亦须跑得动）
    _t('⑨明给词可跑', _m.陈(293, ['点', '本子']), 0)

    # ⑩★而其限须写在册上：它认不着换一整套词者。
    #   「浅」与「轻」係同义而异字——器只因二者俱在 WS 里才连得上；
    #   若只给「浅」，拍17（只说轻，不说浅）即漏。**此漏须验得出。**
    只浅 = [i for i, p in enumerate(ps, 1)
           if sum(1 for w in ['浅', '记号', '事'] if w in p) >= 2]
    _t('⑩只给浅则拍17漏', 17 not in 只浅, True)

    print('\n════ 负测·一事几陈 ════')
    过 = 0
    for 名, ok, 得, 期 in 案:
        print('  %s %s' % ('✓' if ok else '⛔', 名), '' if ok else '  得%r 期%r' % (得, 期))
        过 += ok
    print('  %d/%d %s' % (过, len(案), '全通' if 过 == len(案) else '⛔未过'))
    return 0 if 过 == len(案) else 1


if __name__ == '__main__':
    sys.exit(跑())
