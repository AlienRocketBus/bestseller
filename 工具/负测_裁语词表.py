# -*- coding: utf-8 -*-
"""负测·裁语词表（2026-09-11 立·随 `跑轮.VERDICT` 补「删」「刀」二字同日落）。

★本测所守者两句：
　①**「只删不添」那一类裁，器须认得**（补二字之由）；
　②**而补了二字，抄清单仍须不过**（补二字之限）。
★★头一格拿 315 第8轮那一段真局回灌——**旧词表之下它判 0%，新词表之下须判 100%**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load():
    spec = importlib.util.spec_from_file_location(
        '_pl', os.path.join(ROOT, '工具', '跑轮.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


# ★真局·315 第8轮之必答二项（逐字取自 版本/第315章/_轮记.md，非今日所造）
真局 = ('，印「必答 2 项」）\n'
        '1. **刀数**：**一刀**（行305，只删不添）。'
        '⛔**白文别处一字未动；骨记同笔添⑰⑱两条。**\n'
        '2. **减字**：**白文减十一字**（「，擦到手上不滑了才放下」，本庭亲数）。'
        '**净重 2401→2390**')

旧表 = ('✓', '合', '改', '核', '真伤', '判', '未见', '零', '缺', '对', '错', '撞', '补')


def 跑():
    m = _load()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    desc = sorted(['刀数', '减字'], key=len, reverse=True)

    # ①【头一格·真局回灌】新词表之下，这一段须判「裁过」
    判('①', '315第8轮真局·新表须认得',
       m._judged_near(真局, desc), True)

    # ②【其限·抄清单不许过】光抄清单，每行加一个「删」字，须仍不过
    抄 = '1. **刀数**：删\n2. **减字**：删\n'
    判('②', '抄清单加一个「删」字，照旧不过',
       m._judged_near(抄, desc), False)

    # ③ 同上，加「刀」字亦不过
    判('③', '抄清单加一个「刀」字，照旧不过',
       m._judged_near('1. 刀数：刀\n2. 减字：刀\n', desc), False)

    # ④【证其非陪跑】旧词表之下，头一格那一段判不出（若旧表也认得，本次之补即无据）
    _v = m.VERDICT
    try:
        m.VERDICT = 旧表
        判('④', '旧词表之下同一段判不出（故本次之补非无病呻吟）',
           m._judged_near(真局, desc), False)
    finally:
        m.VERDICT = _v

    # ⑤ 二字确在今日之表内
    判('⑤', '「删」在词表内', '删' in m.VERDICT, True)
    判('⑥', '「刀」在词表内', '刀' in m.VERDICT, True)

    # ⑦ 旧表诸词一个未丢（⛔补字不许顺手改别的）
    判('⑦', '旧表十三词一个未丢',
       all(x in m.VERDICT for x in 旧表), True)

    # ⑧【接进闸】315 第8轮今判 100%
    lj = m._lunji_blocks(315)
    if 8 in lj:
        _, jc, _, _, _, naked = m.duty_cover2(315, 8, '\n'.join(lj[8]))
        判('⑧', '315第8轮裁定率 100% 且无只提未裁者',
           (jc, naked), (100, []))
    else:
        败.append('⑧：315 之轮记取不着第8轮之块')

    # ⑨【不许连坐】一段只有项名而无别的字者，照旧不过（余文不足 8 字）
    判('⑨', '只有项名者照旧不过', m._judged_near('刀数 减字', desc), False)

    print('════ 负测·裁语词表 ════（守：「只删不添」那一类裁须认得，而抄清单仍不许过）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
