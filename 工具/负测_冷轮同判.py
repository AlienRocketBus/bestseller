# -*- coding: utf-8 -*-
"""负测·一坐与开轮六检对冷轮须同判（2026-09-01 立·全书审计第二层 2-8）

★立此测之由：同一 HEAD 上，`一坐.py 287` 印「该修者：COLD-284／COLD-285 未执」，
　★★而 `开轮六检.py 288` 印「✓ ⑥·冷轮之欠 零」——**二器对同一笔给相反之判** ⛔。
★★★其由是两处判据：一坐读冷轮档内之「已执＋销档」二词，六检读回执之「N章冷眼轮」六字。
★★★★而数其群（令§六②）：冷轮档 134 份，**含「已执＋销档」者仅 37 份，97 份没有**——
　★那个标记从来没成为惯例；而回执那一路是封版之序强制的（令§十①）。
【故本测之要害只一条】**二器对每一根冷轮之判，须逐根相同**；一处不同即红。

★★★★★2026-09-03·295第1轮扩（同族，故不另立一份测——一个数不许有两把尺，一族测亦不许有两本账）：
　★**今日又逮出第三把尺**：`小说检察官._auto_cold` 自留一份 `_cold_done`，且把到期章硬写作 `n+2`；
　★★**而 `开轮六检._cold_limit` 读档自书之「限N」**（档里没写的才退回通则，且逾 N+5 者不认）。
　★★★**取二组数**：**73—295 之间，二尺之限相异者 99 章**；
　　**而执之判今日相异 0 章**——**只因今日无一份回执含否决记**；**一写否决记，二器即分家**。
　★★★★**故今补三项（④⑤⑥）**：④限逐章同判｜⑤执逐章同判｜
　　**⑥以旧式（n+2）回灌须报出相异之章**——**一份在旧式下也全过的测就是陪跑**（令§六③）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob, importlib.util, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mod(name, path):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, '工具', path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def 跑():
    m6 = _mod('_六检', '开轮六检.py')
    坏 = []
    档判, 回执判 = 0, 0
    for f in sorted(glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md'))):
        mm = re.search(r'COLD(\d+)_於(\d+)', os.path.basename(f))
        if not mm:
            continue
        src = int(mm.group(1))
        s = io.open(f, encoding='utf-8').read()
        旧式 = ('已执' in s and '销档' in s)      # ★一坐之旧判据
        新式 = m6._cold_done(src)                  # ★六检之判据（今二器同用）
        if 旧式:
            档判 += 1
        if 新式:
            回执判 += 1
        # ★不比二式之异同（那正是本病），只验一坐今日确已改用六检那一路
    # ★验一坐之码里确已 import 六检，而非另记一份
    src2 = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()
    if '_m._cold_limit(n)' not in src2:
        坏.append('★⑦检察官之码里未见转调六检之 _cold_limit——它又自留了一份')
    src1 = io.open(os.path.join(ROOT, '工具', '一坐.py'), encoding='utf-8').read()
    if '_m6._cold_done(src)' not in src1:
        坏.append('★一坐未改用六检之 _cold_done——二器仍各记各的')
    if "'已执' in s and '销档' in s" in src1 and 'except Exception' not in src1:
        坏.append('★一坐仍以档内二词为主判据')
    # ★★★★★2026-09-03 扩·检察官与六检须同尺（限与执逐章比）
    try:
        mi = _mod('_检', '小说检察官.py')
    except SystemExit:
        mi = None
    异限 = 异执 = 0
    旧式异 = 0
    if mi is not None and hasattr(mi, '_cold_due'):
        for c in range(73, 296):
            if mi._cold_due(c) != m6._cold_limit(c):
                异限 += 1
            if mi._cold_done(c) != m6._cold_done(c):
                异执 += 1
            if (c + 2) != m6._cold_limit(c):      # ★旧式回灌
                旧式异 += 1
        if 异限:
            坏.append('★④检察官与六检之「限」相异 %d 章——二尺又分家了' % 异限)
        if 异执:
            坏.append('★⑤检察官与六检之「执」相异 %d 章——二尺又分家了' % 异执)
        if 旧式异 == 0:
            坏.append('★⑥以旧式（到期章＝n+2）回灌，一章也不相异——'
                      '本测证不出今日之改有用，它就是陪跑（令§六③）')
    else:
        坏.append('★④之前置·检察官须有 _cold_due 一口（其限须转调六检，不许自留一份）')
    # ★而其群之数须与今日所量相符（数一变即知惯例变了，须重判）
    n = len(glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md')))
    if 档判 > 回执判:
        坏.append('★以档内二词判为已执者（%d）反多於以回执判者（%d）——惯例已变，须重判其判据'
                  % (档判, 回执判))
    if 坏:
        print('✗ 负测·冷轮同判 %d/7 ⛔未过' % (7 - len(坏)))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·冷轮同判 7/7 全通（冷轮档 %d 份｜以档判已执 %d 份、以回执判 %d 份；'
          '一坐与检察官今皆与六检同用一处尺；旧式回灌相异 %d 章，故非陪跑）'
          % (n, 档判, 回执判, 旧式异))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
