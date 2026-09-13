# -*- coding: utf-8 -*-
"""悬念哨（2026-09-13 立）——**三条主账有没有按其自定之限复提**。

★**其所以要立**：`设定/到期账.json` 之 `SUS-A`／`SUS-B`／`SUS-C` 三笔，
**其形各自写死「每三章至少一处」**——⛔**而盘上没有一只手在数它。**

**0913 之实（本器头一回跑）**：
　**SUS-A·那六天** 末见 **324**（325／326／327 皆零）｜
　**SUS-B·磨窝** 末见 **325**｜
　**SUS-C·照着做** 末见 **318**——**九章无一处字面之迹。**

★★**而 SUS-C 之难正在这里**：**其形自书「须由格式与工夫排出，⛔不许把『给谁』答死」**
——**即它本来就不该有一个固定的词**；**於是任何数词之器都数不着它，它遂成了三条里唯一没人看得见的那一条。**
⛔**故本器为它开第二路**：**一章之骨记里若明写一行 `SUS-C·本章复提：…` 并带其据（拍号或逐字），即算一处。**
★**这不是放宽，是换一把尺**：**数不着的东西，要由写它的人当场报出来，且报得出其据。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
限 = 3   # 每几章至少一处

账 = {
    'SUS-A-那六天': ['那六天', '背的人', '六天就不是六天'],
    'SUS-B-磨窝': ['磨窝'],
    'SUS-C-照着做': ['照着做', '给人照'],
}


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


def 诸章(路=None):
    out = {}
    for f in glob.glob(os.path.join(路 or os.path.join(ROOT, '正文'), '*第*章_*.md')):
        n = _号(os.path.basename(f))
        if n:
            out[n] = io.open(f, encoding='utf-8', errors='replace').read()
    return out


def 复提之章(账号, d):
    """★返回本笔复提过的诸章之号。两路皆算：
    一·白文或骨记里见其记号；
    二·骨记里明写一行「<账号>·本章复提：…」并带其据（⛔空口一行不算：其後须有 ≥8 字）。"""
    出 = []
    pat = re.compile(re.escape(账号.split('-')[0] + '-' + 账号.split('-')[1])
                     + r'[·:：].{0,6}复提[：: ]\s*(\S.{7,})')
    for n in sorted(d):
        t = d[n]
        if any(k in t for k in 账[账号]) or pat.search(t):
            出.append(n)
    return 出


def 判(d=None):
    d = d or 诸章()
    末 = max(d) if d else 0
    报 = []
    for k in 账:
        ch = 复提之章(k, d)
        末见 = max(ch) if ch else 0
        距 = 末 - 末见 if 末见 else 末
        报.append((k, 末见, 距, 距 > 限))
    return 末, 报


def 印():
    末, 报 = 判()
    print('════ 悬念哨 ════（三条主账·各自之形皆写死「每 %d 章至少一处」·以第%d章计）' % (限, 末))
    红 = 0
    for k, 末见, 距, bad in 报:
        if bad:
            红 += 1
            print('  ⛔ %-14s 末见第%s章｜已隔 %d 章（限 %d）' % (k, 末见 or '—', 距, 限))
        else:
            print('  ✓ %-14s 末见第%s章｜隔 %d 章' % (k, 末见 or '—', 距))
    if 红:
        print('  ★**其复提之形，逐笔写死在 `设定/到期账.json` 其条之「其形」里**——')
        print('  ⛔**不许专开一拍去提、不许把它答死、不许用同一句式**；')
        print('  ⛔**而「这一章没位子」不是由**：没位子即改挂到走得到的那一章，当场写明。')
    return 0


def 自测():
    R = []
    造 = lambda **kw: dict(kw)
    # ①造局：某笔末见第10章而今第20章 → 须报
    d = {10: '那六天是照着有人背算的', 20: '别的话'}
    _, r = 判(d)
    a = [x for x in r if x[0] == 'SUS-A-那六天'][0]
    R.append(('①隔十章须报', a[3] is True and a[1] == 10))
    # ②⛔牙·隔三章不报（限内）
    d2 = {17: '磨窝', 20: '别的'}
    b = [x for x in 判(d2)[1] if x[0] == 'SUS-B-磨窝'][0]
    R.append(('②隔三章（限内）不报', b[3] is False))
    # ③⛔牙·从来没提过者，其距＝末章之号，照旧报
    d3 = {20: '别的话'}
    c = [x for x in 判(d3)[1] if x[0] == 'SUS-C-照着做'][0]
    R.append(('③从来没提过者照旧报', c[3] is True and c[1] == 0))
    # ④第二路·骨记之明报算一处（⛔而须带其据）
    d4 = {18: 'SUS-C·本章复提：拍四十一，一行两样各量一回，页数与日数之比', 20: '别的'}
    e = [x for x in 判(d4)[1] if x[0] == 'SUS-C-照着做'][0]
    R.append(('④骨记明报带据者算一处', e[1] == 18))
    # ⑤⛔牙·空口一行不算（其後无据）
    d5 = {18: 'SUS-C·本章复提：有', 20: '别的'}
    f = [x for x in 判(d5)[1] if x[0] == 'SUS-C-照着做'][0]
    R.append(('⑤空口一行不算（无据者不认）', f[1] == 0))
    # ⑥盘上真局：跑得动
    末, r = 判()
    R.append(('⑥盘上跑得动（末章 %d）' % 末, 末 > 300))
    坏 = [n for n, ok in R if not ok]
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    print('  自测 %d/%d' % (len(R) - len(坏), len(R)))
    return 0 if not 坏 else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 印())
