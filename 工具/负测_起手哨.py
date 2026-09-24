# -*- coding: utf-8 -*-
"""负测 · 起手哨（2026-09-24 立·令§一⑤）

⛔**其所以非有此测不可**：`对位闸` 与 `全测` 当面印过一句——
  「**跑得过它自己那十格，不等於它测着了什么——它至今无一份负测**」。
★**自测与负测所问的不是同一件事**：
  **自测问「今日之盘上这几样对不对」**；**负测问「把它弄坏，它红不红」**。
★★**本器之要害有三**：**串怎么数**｜**日词须在句首**｜**其自 352，其门 18**。
  ⛔**三样里但凡有一样悄悄走了形，它照旧印绿，而没有人看得出来。**
⛔本负测一律造局（**自造之库，⛔不读真盘之正文**），末二格方点一回真盘。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    s = _u.spec_from_file_location('起手哨', os.path.join(ROOT, '工具', '起手哨.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _章(日=True, 句中=False):
    头 = '第一百三十三天。他把手收回来。' if 日 else '他把手收回来。'
    if 句中:
        头 = '他把手收回来，到第一百三十三天才又伸出去。'
    return '《书》\n\n第九十九章　假\n\n%s\n' % 头


def 跑():
    m = _器()
    R = []

    # ① 造一串 20 章日起手（皆在 352 之後）——⛔它须数得出这一串
    库 = dict((n, _章(True)) for n in range(352, 372))
    flags, 串 = m.量(库)
    R.append(('①造局·352—371 连 20 章日起手，数得出且恰 20 章',
              any(c == 20 and a == 352 and b == 371 for c, a, b in 串)))
    犯 = [s for s in 串 if s[0] >= m.门 and s[2] >= m.自]
    R.append(('①之二·此串过门（%d）且在自（%d）之後，係当报之串' % (m.门, m.自), len(犯) == 1))

    # ② 同一局只改一章为非日起手，二十章即断作两串，皆不过门
    库2 = dict(库)
    库2[361] = _章(False)
    _, 串2 = m.量(库2)
    R.append(('②中间断一章即分作两串（9＋10），二者皆不过门——⛔证它不是一律判有',
              sorted(c for c, _, _ in 串2) == [9, 10]))

    # ③⛔日词在句中者不算起手（本器自书之界）
    R.append(('③⛔日词在句中者不算起手', m.日起手(_章(句中=True)) is False))
    R.append(('③之二·同一句挪到句首即算', m.日起手(_章(True)) is True))

    # ④⛔首句之认：书名行、章名行、分隔之星皆不算
    脏 = '《镇冢秘术》\n\n＊\n\n第九十九章　假\n\n＊\n\n第一百三十三天。他收回手。\n'
    R.append(('④书名行／章名行／分隔之星皆不算首句', m.日起手(脏) is True))
    脏2 = '《镇冢秘术》\n\n第九十九章　假\n\n他收回手。\n\n第一百三十三天。\n'
    R.append(('④之二·⛔第二句之日词不算起手（⛔不许在全章里搜）', m.日起手(脏2) is False))

    # ⑤⛔其自 352：**其前之串再长也不报**
    库3 = dict((n, _章(True)) for n in range(300, 341))
    _, 串3 = m.量(库3)
    R.append(('⑤造局·300—340 连 41 章日起手，数得出', any(c == 41 for c, _, _ in 串3)))
    R.append(('⑤之二·⛔而其止在 340（＜自%d），本器不追' % m.自,
              [s for s in 串3 if s[0] >= m.门 and s[2] >= m.自] == []))
    库4 = dict(库3)
    库4[352] = _章(True)          # ★一串结在 352 上（⛔跨过那一界）
    _, 串4 = m.量(库4)
    R.append(('⑤之三·一串若结在自之後（352），即当报——⛔证⑤之二不是一路放行',
              any(s[0] >= m.门 and s[2] >= m.自 for s in 串4)))

    # ⑥ 串之算须收末一串（⛔不许把结在末章那一串漏掉）
    R.append(('⑥诸串收得着末一串', m.诸串([(1, True), (2, True)]) == [(2, 1, 2)]))
    R.append(('⑥之二·全非日起手者零串', m.诸串([(1, False), (2, False)]) == []))
    R.append(('⑥之三·首尾各一串', m.诸串([(1, True), (2, False), (3, True)]) == [(1, 1, 1), (1, 3, 3)]))

    # ⑦⛔其门与其自係写死之数，⛔不是随今章往後挪的数
    src = io.open(os.path.join(ROOT, '工具', '起手哨.py'), encoding='utf-8').read()
    R.append(('⑦⛔门 == 18（⛔而史上三串 41／30／25 皆在门上，故此门非凭空）', m.门 == 18))
    R.append(('⑦之二·⛔自 == 352（⛔不随今章往後挪）', m.自 == 352))
    R.append(('⑦之三·码上此二数係常量，⛔不由今章算出',
              re.search(r'^门 = 18$', src, re.M) is not None
              and re.search(r'^自 = 352', src, re.M) is not None))

    # ⑧⛔报之判：有犯即 False（⛔不许只印不判）
    R.append(('⑧⛔其报有犯即判否（码上 `if 犯:` 之下 return False）',
              re.search(r'if 犯:(?:.|\n)*?return False', src) is not None))

    # ⑨真盘（⛔只点二样，不作判）：352／353／354 三章俱非日起手
    库真 = m._库()
    d = dict(m.量(库真)[0])
    R.append(('⑨真盘·352、353、354 三章俱非日起手（0922 之治·至今未回去）',
              all(d.get(n) is False for n in (352, 353, 354))))
    R.append(('⑨之二·真盘·自第%d章起无一串过门 %d（⛔此係今日之实，逐日会变，只作注）'
              % (m.自, m.门),
              m.报() is True))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·起手哨 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
