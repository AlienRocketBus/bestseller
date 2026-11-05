# -*- coding: utf-8 -*-
"""负测·站账逐章行（2026-09-12 立·「E4收後·过渡」那一栏走满八章才被逮着，方立此条）。

★所守者一句：**凡一栏之对站记里已有逐章之表，其栏内每一已封版之章须有其行，缺一即红。**
★★其根不在漏记，在**记那一行的时辰没人管**：
　那八行是我回头照着 `git log` 数出来的，**不是当天记的**——⛔**补得上不是本事，是运气。**
★★★**而本闸落下去当日自栽两回，两格皆在下头钉着**：
　①不认表头地扫，把 E4 那份记里「| 段 | 均净重 |」那张**别的表**认成逐章表，报「缺42行」；
　②以正文在不在为准，**起草一落盘就催**——而那时诸轮没跑，那一句「它干了什么」还没定。
⛔**故收窄二处：只认表头次格作「章」者｜只数已封版（回执在）之章。**
★★★★**而收窄之後须当场证它还有牙**（本册通例·同日立）：第③④格即此。
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
        '_zz', os.path.join(ROOT, '工具', '站账.py'))
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

    过渡 = os.path.join(ROOT, '设定', '站账_E4收後·过渡_对站.md')
    E4 = os.path.join(ROOT, '设定', '站账_E4巴蜀水下_对站.md')

    # ①【逐章表认得出】314—321 八章逐章之行俱在
    逐 = m._逐章之行(过渡)
    判('①', '过渡栏之逐章表认得出，且 314—321 八行俱在',
       逐 is not None and set(range(314, 322)) <= 逐, True)

    # ②【假红之一·当日自栽】E4 那份记里那张「段／均净重」之表，⛔不许被认作逐章表
    e = m._逐章之行(E4)
    判('②', 'E4 那份记之别表不被认作逐章表（⛔不许再报「缺42行」）',
       e is None or not (set(range(272, 314)) & e), True)

    # ③【证其有牙·剥一行即红】⛔否则收窄之後它就只是一句好听的话
    tx = io.open(过渡, encoding='utf-8').read()
    剥 = '\n'.join(ln for ln in tx.split('\n')
                   if not ln.strip().startswith('| 321 |'))
    判('③之一', '剥 321 那一行，其文确变短', len(剥) < len(tx), True)
    import tempfile
    fd, tp = tempfile.mkstemp(suffix='.md')
    os.close(fd)
    io.open(tp, 'w', encoding='utf-8').write(剥)
    try:
        剥逐 = m._逐章之行(tp)
        判('③之二', '剥一行，第判三当场逮得出（321 不在其内）',
           剥逐 is not None and 321 not in 剥逐, True)
        判('③之三', '而余下七行照旧认得出（⛔不许一剥就整张表作废）',
           剥逐 is not None and set(range(314, 321)) <= 剥逐, True)
    finally:
        os.unlink(tp)

    # ④【假红之二·当日自栽】起草而未封版者不催；已封版者才催
    # ⛔**本格原钉死在「322 未封版」这一实况上，而 322 当日即封了版，格遂自己过期**
    #   （0912 当天下午自栽·全测逮出）——★**这是本坐立过那条总纲的又一个变种：
    #   **快照不是律**：**当时的实况写进判据，它就只对那一天成立。**
    #   ★★故改为验「那条律本身」：**取一个必然未封版之章（末章之後一章）**。
    _末 = m._末章()
    判('④之一', '末章之正文在盘（%d）' % _末, m._净(_末) > 0, True)
    判('④之二', '⛔而末章之後那一章必未封版（其回执不在），故不催其行',
       m._已封版(_末 + 1), False)
    # ⛔**0913 第三回自栽**：本格原写作「末章已封版」——**而末章正在写的时候它必未封版**
    #   （0913 第325章之席在跑，全测当场逮出）。★**又一个「快照不是律」的变种**：
    #   **前两回钉的是章号，这一回钉的是「末章此刻的状态」**——⛔**状态也是快照。**
    #   ★★故改验那条律本身：**取盘上最末那一个「已封版」之章**（必有，起用章＝306 以来章章有回执），
    #   **该催即催**；⛔**而末章封没封版，本格一个字也不问。**
    _末封 = _末
    while _末封 > 300 and not m._已封版(_末封):
        _末封 -= 1
    判('④之三', '盘上最末之已封版章（%d）该催即催' % _末封,
       m._已封版(_末封) and _末封 > 300, True)
    判('④之四', '⛔而其行确在表内（证④之三不是空转）',
       逐 is not None and (_末封 in 逐 or _末封 > max(逐)), True)

    # ⑤【表未立者不在此判之内】
    判('⑤', '无此档者返 None（表未立即跳过）',
       m._逐章之行(os.path.join(ROOT, '设定', '站账_没有这一份_对站.md')), None)

    # ⑥【不许连坐】判一（对站之记不在即红）须仍在
    src = io.open(os.path.join(ROOT, '工具', '站账.py'), encoding='utf-8').read()
    判('⑥', '判一仍在（对站之记不在即红）', '而对站之记不在' in src, True)

    # ⑦【今日之实】盘上此刻一处不缺
    rows, 判语 = m.账()
    判('⑦', '今日站账无逐章行之红',
       [x for x in 判语 if '逐章之表' in x], [])

    print('════ 负测·站账逐章行 ════（守：一栏之逐章表，每封一章即加一行）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
