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
    全 = _器('全测', '全测.py')
    哨 = _器('十一轮哨', '十一轮哨.py')

    # ①⛔真盘之实：363 只有案席，无封版席、无十一轮之凭
    R.append(('①真盘·363 有案席而无封版席（⛔其席断在第 10 段）',
              _有(363, '案席') and not _有(363, '封版席')))
    R.append(('①之二·363 无 `_十一轮.json`',
              not os.path.exists(os.path.join(ROOT, '版本', '第363章', '_十一轮.json'))))
    R.append(('①之三·355—362 章章有封版席（⛔证 363 非常例）',
              all(_有(n, '封版席') for n in range(355, 363))))

    # ②新式：363 ⛔不作已封版
    R.append(('②新式·363 ⛔不作已封版', 全._已封版(363) is False))
    # ⛔旧式回灌：认案席者，363 当场作「已封版」
    旧 = any(glob.glob(os.path.join(ROOT, '设定', '回执_*_第363章%s.md' % k))
             for k in ('作业单', '案席', '封版席'))
    R.append(('②之二·⛔旧式回灌（认案席）：363 当场作「已封版」——**二判确实不同**', 旧 is True))

    # ③已真封版者照旧认（⛔证本改不是一律判否）
    R.append(('③355—362 逐章照旧作已封版', all(全._已封版(n) for n in range(355, 363))))
    R.append(('③之二·⛔358 只有案席＋封版席而无作业单，照旧认得（其封版席在）',
              (not _有(358, '作业单')) and 全._已封版(358)))

    # ④十一轮哨：363 不再被记作「已封版而无凭」
    R.append(('④十一轮哨·363 不在「已交回执之章」之列', 363 not in 哨.已交回执之章()))
    R.append(('④之二·362 照旧在其列（⛔证④非一路放行）', 362 in 哨.已交回执之章()))

    # ⑤码上：三器皆已收回「案席」
    for 名, 档 in (('全测', '全测.py'), ('接力', '接力.py'), ('十一轮哨', '十一轮哨.py')):
        src = io.open(os.path.join(ROOT, '工具', 档), encoding='utf-8').read()
        # ⛔**须先褪去行尾之注再看**——**那一行的注正写着「收回『案席』」**；
        #   ★今日本坐在 `负测_核轮` 已栽过同一处：**一个格问得太宽，
        #     逼出来的不是治，是把对的东西改掉**。
        码 = [l.split('#')[0] for l in src.split('\n')
              if "'作业单'" in l and not l.lstrip().startswith('#')]
        R.append(('⑤%s 之码（褪去行尾之注）里无「案席」（⛔注里那几句係碑，该留）' % 名,
                  bool(码) and all('案席' not in l for l in 码)))

    # ⑥⛔而「案席」二字不许从注里抹掉（那是这一回的记因）
    src = io.open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    R.append(('⑥⛔其记因仍在注里（「363 冒充了封版」那一句）', '冒充了封版' in src))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·封版之凭 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
