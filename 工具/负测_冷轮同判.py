# -*- coding: utf-8 -*-
"""负测·一坐与开轮六检对冷轮须同判（2026-09-01 立·全书审计第二层 2-8）

★立此测之由：同一 HEAD 上，`一坐.py 287` 印「该修者：COLD-284／COLD-285 未执」，
　★★而 `开轮六检.py 288` 印「✓ ⑥·冷轮之欠 零」——**二器对同一笔给相反之判** ⛔。
★★★其由是两处判据：一坐读冷轮档内之「已执＋销档」二词，六检读回执之「N章冷眼轮」六字。
★★★★而数其群（令§六②）：冷轮档 134 份，**含「已执＋销档」者仅 37 份，97 份没有**——
　★那个标记从来没成为惯例；而回执那一路是封版之序强制的（令§十①）。
【故本测之要害只一条】**二器对每一根冷轮之判，须逐根相同**；一处不同即红。
"""
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
    src1 = io.open(os.path.join(ROOT, '工具', '一坐.py'), encoding='utf-8').read()
    if '_m6._cold_done(src)' not in src1:
        坏.append('★一坐未改用六检之 _cold_done——二器仍各记各的')
    if "'已执' in s and '销档' in s" in src1 and 'except Exception' not in src1:
        坏.append('★一坐仍以档内二词为主判据')
    # ★而其群之数须与今日所量相符（数一变即知惯例变了，须重判）
    n = len(glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md')))
    if 档判 > 回执判:
        坏.append('★以档内二词判为已执者（%d）反多於以回执判者（%d）——惯例已变，须重判其判据'
                  % (档判, 回执判))
    if 坏:
        print('✗ 负测·冷轮同判 %d/3' % (3 - len(坏)))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·冷轮同判 3/3 全通（冷轮档 %d 份｜以档判已执 %d 份、以回执判 %d 份；'
          '一坐今与六检同用一处 _cold_done）' % (n, 档判, 回执判))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
