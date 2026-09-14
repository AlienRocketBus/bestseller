# -*- coding: utf-8 -*-
"""咬合哨（2026-09-14 立）——**331 起，每五章之内须有一章其事係「两件事咬在一起」。**

★**其所由来**：0913 三把尺，三个方向，指的是同一处——
　`净重趋`（**顶在 223—237 之 7,076，今 313—327 之 2,216**）｜
　`重出趋`（**325:14.4｜326:10.0｜327:24.1**）｜
　`书级体检`②（**同型「长」连锁 13 章**）——**这一段书太匀了。**
★★**其裁已落**（`设定/裁_0913_净重之趋_全书在慢慢变薄.md`）：**治在事之择，不在字数**——
　**331 起每五章之内须有一章其事係「两件事咬在一起」**：**一件办到一半被另一件打断，两件都得办，而手只有一双。**
⛔**而那一条裁立了一日，盘上没有一只手在数它**（**㊛ 之骨：册上写着而器没在看**）——**故立本器。**

★★★**其认之法（与 `悬念哨` 之第二路同式）**：**数不着的东西，由写它的人当场报出来，且报得出其据。**
**一章之骨记里明写一行 `咬合：…` 并带其据（≥8 字，须指得出拍号或逐字）**，即算一章。
⛔**空口一行不算**；⛔**而器不判「咬得好不好」**——**那只有读的人判得了**；**它只数「有没有一章报过」。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起 = 331     # 自此章起在役
窗 = 5       # 每几章须有一章


def _号(f):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', f)
    if not m:
        return None
    d = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
         '六': 6, '七': 7, '八': 8, '九': 9}
    t = n = 0
    for ch in m.group(1):
        if ch in d:
            n = d[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


_报 = re.compile(r'咬合[：:]\s*(\S.{7,})')


def 诸章(d=None):
    if d is not None:
        return d
    out = {}
    for f in glob.glob(os.path.join(ROOT, '正文', '*第*章_*.md')):
        n = _号(os.path.basename(f))
        if n:
            out[n] = io.open(f, encoding='utf-8', errors='replace').read()
    return out


def 报过(t):
    """★一章有没有当场报过它咬合了（⛔须带其据，空口一行不算）。"""
    return bool(_报.search(t or ''))


def 判(d=None, 起=起, 窗=窗):
    """返回 (诸章之报, 诸红)。★红＝一个满窗之内一章也没有报过。"""
    d = 诸章(d)
    ns = sorted(n for n in d if n >= 起)
    报 = [(n, 报过(d[n])) for n in ns]
    红 = []
    for i in range(len(ns)):
        块 = ns[i:i + 窗]
        if len(块) < 窗:           # ⛔窗未满即不判（其章还没写到）
            break
        if not any(报过(d[n]) for n in 块):
            红.append((块[0], 块[-1]))
    return 报, 红


def 印():
    报, 红 = 判()
    print('════ 咬合哨 ════（自第%d章起·每 %d 章之内须有一章报「两件事咬在一起」）' % (起, 窗))
    if not 报:
        print('  ✓ 尚未写到第%d章，本哨未起役。' % 起)
        return 0
    print('  · 已写之章：%s' % '｜'.join('%d:%s' % (n, '报' if ok else '—') for n, ok in 报))
    if not 红:
        print('  ✓ 无一个满窗空着。')
        return 0
    for a, b in 红:
        print('  ⛔ 第%d—%d章五章之内一章也没有报过' % (a, b))
    print('  ★其报之法：**骨记里明写一行「咬合：…」并带其据（拍号或逐字·≥8字）**；')
    print('  ⛔空口一行不算；⛔而器不判咬得好不好——那只有读的人判得了。')
    print('  ★★其裁之出处：`设定/裁_0913_净重之趋_全书在慢慢变薄.md`。')
    return 0


def 自测():
    R = []
    好 = '咬合：拍四十一办到一半，绳那一头掉下去，两件都得办而手只有一双'
    空 = '咬合：有'
    无 = '今天她把柴摆进圈里'
    R.append(('①带据之报认得出', 报过(好) is True))
    R.append(('②⛔牙·空口一行不算', 报过(空) is False))
    R.append(('③⛔牙·没报过者不认', 报过(无) is False))
    d = dict((n, 无) for n in range(331, 336))
    R.append(('④满窗皆无须报红', 判(d)[1] == [(331, 335)]))
    d2 = dict(d); d2[333] = 好
    R.append(('⑤⛔牙·窗内有一章报过即不红', not 判(d2)[1]))
    d3 = dict((n, 无) for n in range(331, 335))
    R.append(('⑥⛔牙·窗未满不判（其章还没写到）', not 判(d3)[1]))
    d4 = dict((n, 无) for n in range(325, 331))
    R.append(('⑦⛔牙·331 之前不在役', not 判(d4)[1]))
    坏 = [n for n, ok in R if not ok]
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    print('  自测 %d/%d' % (len(R) - len(坏), len(R)))
    return 0 if not 坏 else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 印())
