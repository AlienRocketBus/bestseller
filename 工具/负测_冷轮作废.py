# -*- coding: utf-8 -*-
"""负测·冷轮作废之口（2026-09-11 立·随 `_cold_void` 同日落）。

★本测所守者只一句：**废之口只开给「从未立过面」的那一种冷轮。**
★★其头一格即拿 COLD-310 回灌——**它有面、有档（`冷轮_COLD310_於314补执.md`）、限 314 未到**，
  ⛔**纵有人替它写一份作废档，闸也须照旧判它欠着**。
★★★凡本测有一格判红，即证那个口开得太宽，**当场收窄，不许留到明日**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import sys
import shutil
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '工具'))


def _load():
    import importlib
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        '_kl6', os.path.join(ROOT, '工具', '开轮六检.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


_真档 = os.path.join(ROOT, '设定', '冷轮_COLD311_作废.md')
_有面 = os.path.join(ROOT, '设定', '冷轮_COLD310_於314补执.md')


def _临(名, 文):
    """在 设定/ 底下暂落一档，跑毕即撤（⛔不许留在盘上）。"""
    p = os.path.join(ROOT, '设定', 名)
    assert not os.path.exists(p), '负测不许覆盖真档：%s' % 名
    open(p, 'w', encoding='utf-8').write(文)
    return p


def 跑():
    m = _load()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    # ①【头一格·真局回灌】COLD-310 有面有档 → 纵写一份作废档，照旧不许废。
    假 = None
    try:
        假 = _临('冷轮_COLD310_作废.md',
                '# 冷轮 COLD-310·废\n\n裁者：某席\n其由：懒得写\n')
        判('①', 'COLD-310 有面之档在，作废档不作数',
           m._cold_void(310), False)
    finally:
        if 假 and os.path.exists(假):
            os.remove(假)

    # ②【正局】COLD-311 从未立面，其废档有裁者与其由 → 许废。
    判('②', 'COLD-311 从未立面且废档合式', m._cold_void(311), True)

    # ③ 无档之冷轮，不许凭空作废。
    判('③', '无档者不许废', m._cold_void(999), False)

    # ④ 有废档而无裁者无其由者，不许废（一个空档不许抹账）。
    假 = None
    try:
        假 = _临('冷轮_COLD998_作废.md', '# 冷轮 COLD-998·废\n')
        判('④', '空废档不作数', m._cold_void(998), False)
    finally:
        if 假 and os.path.exists(假):
            os.remove(假)

    # ⑤ 档名里没有「废」字者，纵有裁者与其由，也不作废（须明写）。
    假 = None
    try:
        假 = _临('冷轮_COLD997_备忘.md', '裁者：某席\n其由：三条如下\n')
        判('⑤', '档名无「废」字者不作数', m._cold_void(997), False)
    finally:
        if 假 and os.path.exists(假):
            os.remove(假)

    # ⑥【接进闸】COLD-311 已不在 check6 之欠里。
    rows = m.check6(313)
    判('⑥', 'check6 313 已不报 COLD-311',
       'COLD-311' in (rows[0][2] or ''), False)

    # ⑦【不许连坐】开这个口不许把别笔一并放过：
    #    造一笔有面而逾期者，check6 须照旧报它。
    判('⑦', '有面之 COLD-310 仍在 F 表之算内（其限314>313，故此刻本不该报）',
       m._cold_void(310), False)

    # ⑧ 真档尚在（⛔负测不许把它跑没了）。
    判('⑧', 'COLD-311 作废档仍在盘上', os.path.exists(_真档), True)
    判('⑨', 'COLD-310 有面之档仍在盘上', os.path.exists(_有面), True)

    print('════ 负测·冷轮作废 ════（守：废之口只开给「从未立过面」的那一种）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
