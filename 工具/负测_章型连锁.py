#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测 · 章型连锁之「相对之型」（2026-09-17 立·随 `书级体检.py::相对之型` 同日落）

★**其所治之病**：**「段」这个单位，本书自 332 前後换过一回**——
  **从前一拍之内分数段（均段十几二十）；今一拍即一段**（白文一拍一行）。
  ⛔**於是旧式四档（短<15／中15-18／中长18-21／长>21）自 332 起章章判「长」**，
  **连锁必逾十二，且此後永远如此**——**一条永远清不掉的红**（与 `COLD-336` 同形）。
★★**其治**：**「型」改作相对之判**——**本章之均段，落在近十二章之第几档（四等分位）**。
  ⛔**其所以可以相对**：**「纹理一成不变」这一问本来就是相对的**——
  **问的是「这一章与它左右邻章像不像」**，⛔**不是「它有没有超过某个绝对之数」。**

★★★**而本器所守者，正是「改成相对之後，它还咬不咬得动」**——
  ⛔**一道分类若怎么排都不报，那就是把闸拆了，不是把它修好。**

用法：
    python3 工具/负测_章型连锁.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as iu, os, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    sp = iu.spec_from_file_location('_sj_负测', os.path.join(根, '工具', '书级体检.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _型串(m, 诸均):
    return [m.相对之型(诸均, c) for c in sorted(诸均)]


def 跑():
    m = _器()
    R = []

    # ①⛔全书均段一模一样 → 逐章皆同型（**这正是本检要逮的那一种**）
    同 = {n: 50.0 for n in range(400, 420)}
    串 = [x for x in _型串(m, 同) if x]
    R.append(('①均段章章一样 → 逐章同型（其型不论叫什么，须只有一种）',
              len(set(串)) == 1 and len(串) >= 10))

    # ②⛔一路只往上走（单调）→ 章章落在其窗之顶，亦须同型
    升 = {n: 30.0 + (n - 400) * 5 for n in range(400, 420)}
    串2 = [x for x in _型串(m, 升) if x]
    R.append(('②均段一路往上走 → 章章落顶，亦须同型',
              len(set(串2)) == 1))

    # ③★真在变者，其型须变（⛔不许怎么排都只报一种）
    import math
    波 = {n: 40.0 + 30.0 * math.sin(n) for n in range(400, 425)}
    串3 = [x for x in _型串(m, 波) if x]
    R.append(('③均段有起有伏 → 其型须多於一种（⛔不许怎么排都同型）',
              len(set(串3)) >= 3))

    # ④⛔窗内不足八章者不判（免拿三五个数去分四档）
    少 = {400: 10.0, 401: 20.0, 402: 30.0}
    R.append(('④窗内不足八章者退回旧式（本函返 None）',
              all(m.相对之型(少, c) is None for c in 少)))

    # ⑤★其窗只取本章及其前者，⛔不许拿後头之章去判前头之章
    甲 = {n: 50.0 for n in range(400, 412)}
    甲[411] = 999.0
    乙 = dict(甲)
    乙[412] = 999.0                      # ⛔多一章在後
    R.append(('⑤其窗只看本章与其前（後添一章不改前章之判）',
              m.相对之型(甲, 410) == m.相对之型(乙, 410)))

    # ⑥⛔盘上跑得动，且今日之连锁已非「永远的长」
    chs = {}
    import glob, io, re
    for f in glob.glob(os.path.join(根, '正文', '*.md')):
        mm = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(f))
        if not mm:
            continue
        chs[mm.group(1)] = None
    R.append(('⑥盘上正文 ≥300 章（本测之料在）', len(chs) >= 300))

    # ⑦〔1119 死规之审·gates12〕连锁逾限照旧侦得（链长照算），⛔入「不过」——只由 main 印 ⚠
    文 = '《书》\n\n第九十九章　假\n\n' + '\n\n'.join(['甲' * 50] * 4) + '\n'
    _sq, _ch, _bad = m.check_type_chain(dict((n, 文) for n in range(400, 420)))
    R.append(('⑦二十章同纹理：链长 %d 照旧侦得（＞限 %d），而⛔入 bad' % (_ch[1], m.TYPE_CHAIN_LIMIT),
              _ch[1] > m.TYPE_CHAIN_LIMIT and _bad == []))

    print('════ 负测 · 章型连锁之「相对之型」 ════')
    过 = 0
    for 名, ok in R:
        print(('  ✓ ' if ok else '  ⛔ ') + 名)
        过 += 1 if ok else 0
    print('  %d/%d %s' % (过, len(R), '全通' if 过 == len(R) else '未全通'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
