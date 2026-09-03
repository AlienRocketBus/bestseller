# -*- coding: utf-8 -*-
"""负测·空头签（2026-09-03 立·与其闸同日·令§六③）

★逐条回灌，每一条都拿「真犯过此项之原物」去撞它（令§十四③）：
  ①今日之盘须绿（其基线）
  ②把295之回执改回「以本章之号写那六字」即红——**这正是2026-09-03·296起手时逮出的那一笔**
  ③而其红须点得出是哪一份（不许只报个数）
  ④旧式那一代（75—278）不许判红——**头一版不分年代，一扫报195处，皆是假红**
  ⑤旧式回灌：**若判据不分年代**，②③照旧过，**而④必崩**——**故本测证得出「分代」那一刀有用，非陪跑**
  ⑥还原毕之盘须与测前逐字相同（第二十八犯之处方）
"""
import importlib.util as iu, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, '设定', '回执_20260903_第295章作业单.md')


def _mod():
    sp = iu.spec_from_file_location('_kt', os.path.join(ROOT, '工具', '空头签.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def 跑():
    if not os.path.exists(P):
        print('✗ 负测·空头签 ⛔前置不在：%s' % P)
        return 1
    原 = io.open(P, encoding='utf-8').read()
    m = _mod()
    坏 = []
    try:
        fps, 含签, 坏签, 旧, _早 = m.查()
        if 坏签:
            坏.append('★①今日之盘本该绿，而它报 %d 处' % len(坏签))
        if 旧 < 100:
            坏.append('★④之前置·旧式那一代本该有近二百份（今 %d 份），其数一变即知年代之界须重判' % 旧)
        # ②③注入：於295之回执补一行「以本章之号写那六字」
        io.open(P, 'w', encoding='utf-8').write(原 + '\n· 本章须写足之六字：295章冷眼轮——已执。\n')
        fps2, _c2, 坏2, _o2, _早 = m.查()
        if not 坏2:
            坏.append('★②把295改回「以本章之号写六字」而它没红——正是296起手时那一笔')
        elif 坏2[0][0] != 295:
            坏.append('★③其红点错了份：报 %s，而所注入者是295' % (坏2[0],))
        # ④旧式那一代照旧不许红
        if any(c < m.新式之首 for c, _n in 坏2):
            坏.append('★④旧式那一代（<%d）被判红——头一版正是这么报了195处假红' % m.新式之首)
        # ⑤旧式回灌：不分年代之判据
        无代 = []
        for fp in fps2:
            mm = re.search(r'第(\d+)章', os.path.basename(fp))
            if not mm:
                continue
            C = int(mm.group(1))
            tx = io.open(fp, encoding='utf-8', errors='replace').read()
            if C in set(int(x) for x in re.findall(r'(\d+)章冷眼轮', tx)):
                无代.append(C)
        if len([c for c in 无代 if c < m.新式之首]) < 100:
            坏.append('★⑤旧式回灌本该报出近二百处假红（证「分代」那一刀有用），而它报 %d 处'
                      % len([c for c in 无代 if c < m.新式之首]))
        # ★★★★★⑦⑧【2026-09-03·297起手时自撞·同日加】第二路·早签
        #   ★其红在哪一行：296之回执第四节，我以「294章冷眼轮」「295章冷眼轮」六字作两行之标题，
        #     其文写的正是「限298，未到期，本章不执」——**一面说没执，一面把签核落下去**；
        #   ★★而第一路（一章不许签自己）对它一声不吭：**294、295 皆非 296 之号。**
        io.open(P, 'w', encoding='utf-8').write(
            原 + '\n· **294章冷眼轮**：限298，**未到期，本章不执**。\n')
        _f, _h, 坏1, _o, 早1 = m.查()
        if not any(x[1] == 294 and x[4] for x in 早1):
            坏.append('★⑦注入「一面说未到期一面写足六字」之行，而第二路没红')
        if any(x[0] == 296 for x in 坏1):
            坏.append('★⑧此注入不该惊动第一路（其N≠本章之号），而第一路也红了')
    finally:
        io.open(P, 'w', encoding='utf-8').write(原)
    if io.open(P, encoding='utf-8').read() != 原:
        坏.append('★⑥还原毕之档与测前不同——本测改坏了它所读的盘')
    if 坏:
        print('✗ 负测·空头签 %d/8 ⛔未过' % (8 - len(坏)))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·空头签 8/8 全通（②③注入即红且点得出其份；'
          '④旧式那一代不判；⑤不分年代之旧式回灌报出 %d 处假红，故「分代」那一刀非陪跑；'
          '⑦第二路·早签之注入即红；⑧且不惊动第一路——**二路各认各的，非陪跑**）'
          % len([c for c in 无代 if c < m.新式之首]))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
