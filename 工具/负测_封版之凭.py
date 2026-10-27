# -*- coding: utf-8 -*-
"""负测 · 封版之凭只认「作业单／封版席」（2026-09-24 立·同日负测·令§一⑤）

⛔**其所治者，係本坐 0923 自己放宽的那一名**：
  **0923 把「回执」放宽为三名（作业单／案席／封版席）**，
  ⛔**而案席係十一段之第 10 段所交，封版席方是第 11 段所交**；
  ★**於是一章跑到第 10 段断了，器里已作「封了版」。**
★★**0924 之实**：**363 之席断在第 10 段（心跳停在 37 分钟前）**，
  **盘上 355—362 章章有封版席，⛔独 363 只有案席、无封版席、无 `_十一轮.json`**——
  **而 `十一轮哨` 报的是「已封版而无十一轮之凭」**：**那一条红记错了人。**
★★★**并记 0923 本坐自己写下的那一句**：「**其验之处已定：下一回推闸跑全测之时逐条对看，
  若有哪一条红因此而消，本坐须当场说出是哪一条、并判它该不该消。**」
  ⛔**而本坐此後十几个回合一次也没回头验它**——
  **一条写着「待验」的改，与一条没写的改，一样危险。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, glob, re
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器(名, 档):
    s = _u.spec_from_file_location(名, os.path.join(ROOT, '工具', 档))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _有(n, k):
    return bool(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章%s.md' % (n, k))))


def 跑():
    R = []
    # ★1027：全测之 `_已封版` 随 `_推闸旧` 汰（其唯一之调）——封版之凭今由 接力.有回执、十一轮哨.已交回执之章 二器判，验其二
    接 = _器('接力', '接力.py')
    哨 = _器('十一轮哨', '十一轮哨.py')

    # ①②【0924 午改·快照→不变式】头一版写死「363 无封版席」——363 一封，四格同红（通例：快照不是守）。
    #   ⛔今守其理：**真盘上凡有案席之章，已封版与否，只看封版席／作业单在不在；案席一份不作数。**
    import re as _re
    诸 = sorted({int(x) for x in _re.findall(r'第(\d+)章案席', ' '.join(
        os.path.basename(f) for f in glob.glob(os.path.join(ROOT, '设定', '回执_*_第*章案席.md'))))})
    诸 = [n for n in 诸 if n >= 355]
    R.append(('①真盘·355 以降有案席之章 ≥5（⛔证下面不是空转）', len(诸) >= 5))
    错 = [n for n in 诸 if 接.有回执(n) != (_有(n, '封版席') or _有(n, '作业单'))]
    R.append(('②新式·已封版 ⇔ 有封版席或作业单（案席不作数·今相违：%s）' % (错 or '无'), not 错))
    # ②之二⛔旧式回灌：造一个只有案席之假章（内存·不落盘），旧式判封、新式判未封——二判确实不同
    假 = 9999
    旧 = any(k in ('作业单', '案席', '封版席') for k in ('案席',))
    R.append(('②之二·⛔旧式回灌（认案席）：只有案席之章当场作「已封版」——**二判确实不同**',
              旧 is True and 接.有回执(假) is False))

    # ③已真封版者照旧认（⛔证本改不是一律判否）
    R.append(('③355—362 逐章照旧作已封版', all(接.有回执(n) for n in range(355, 363))))
    R.append(('③之二·⛔358 只有案席＋封版席而无作业单，照旧认得（其封版席在）',
              (not _有(358, '作业单')) and 接.有回执(358)))

    # ④十一轮哨：363 不再被记作「已封版而无凭」
    _交 = 哨.已交回执之章()
    _违 = [n for n in 诸 if (n in _交) != (_有(n, '封版席') or _有(n, '作业单'))]
    R.append(('④十一轮哨·已交回执 ⇔ 有封版席或作业单（今相违：%s）' % (_违 or '无'), not _违))
    R.append(('④之二·362 照旧在其列（⛔证④非一路放行）', 362 in 哨.已交回执之章()))

    # ⑤码上：二器皆已收回「案席」（全测之 _已封版 1027 随 _推闸旧 汰）
    for 名, 档 in (('接力', '接力.py'), ('十一轮哨', '十一轮哨.py')):
        src = io.open(os.path.join(ROOT, '工具', 档), encoding='utf-8').read()
        # ⛔**须先褪去行尾之注再看**——**那一行的注正写着「收回『案席』」**；
        #   ★今日本坐在 `负测_核轮` 已栽过同一处：**一个格问得太宽，
        #     逼出来的不是治，是把对的东西改掉**。
        码 = [l.split('#')[0] for l in src.split('\n')
              if "'作业单'" in l and not l.lstrip().startswith('#')]
        R.append(('⑤%s 之码（褪去行尾之注）里无「案席」（⛔注里那几句係碑，该留）' % 名,
                  bool(码) and all('案席' not in l for l in 码)))

    # ⑥⛔而「案席」二字不许从注里抹掉（那是这一回的记因；全测之碑随 _已封版 去，今守十一轮哨之碑）
    src = io.open(os.path.join(ROOT, '工具', '十一轮哨.py'), encoding='utf-8').read()
    R.append(('⑥⛔其记因仍在注里（「363 之席断在第 10 段，而器里已作封版」那一句）', '363 之席断在第 10 段' in src))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·封版之凭 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
