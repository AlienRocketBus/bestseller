# -*- coding: utf-8 -*-
"""负测·亮点残引（2026-09-13 立·随 `亮点对表.旧版残引` 之收窄同日落）。

★所守者一句：**亮点段引了一句而那一句是本章自己删掉的，即红。**
★★而 0913 收窄一处：**骨记里明写「原作 X →改後 Y」的改动记录，其「原作」那一句不算残引**
　——**那正是改动之实**；⛔**照旧判据，凡诚实记录自己那一刀的轮记，都会被判成残引**
　（324 之骨记⑳逐字「⛔**原作**：……→**删後半**」即当日之红）。
★★★⛔**而收窄最怕把牙一并磨掉**，故本测之骨在第③格：
　**拿 301 立闸当日之原物回灌**（其三处残引正是立此闸之由），**它须当场逮得出**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io
import os
import re
import sys
import subprocess
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _m():
    spec = importlib.util.spec_from_file_location(
        '_lb', os.path.join(ROOT, '工具', '亮点对表.py'))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
    except SystemExit:
        pass
    return m


def 跑():
    m = _m()
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    # ①【今日之实】324 之骨记⑳係改动记录，不算残引
    p324 = None
    for f in os.listdir(os.path.join(ROOT, '正文')):
        if '第三百二十四章' in f:
            p324 = os.path.join(ROOT, '正文', f)
    判('①之一', '324 之正文在', bool(p324), True)
    t324 = io.open(p324, encoding='utf-8').read() if p324 else ''
    判('①之二', '324 之骨记确带「原作」之注（本格之料在）',
       '⛔**原作**' in t324, True)
    判('①之三', '⛔而其不算残引（改动记录非残引）',
       m.旧版残引(324, t324), [])

    # ②【证「原作」那一句确係今版所无而旧版有】⛔否则第①格是空的
    q = '压住的地方那一股绳比别处扁，扁的那一段是旧的，不是今天压的。'
    body = re.sub(r'\s', '', t324.split('【本章亮点】')[0])
    判('②之一', '其串今版正文确无', q in body, False)
    import glob
    旧 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '版本', '第324章', 'v*.md'))):
        s = io.open(f, encoding='utf-8', errors='replace').read()
        旧.append(re.sub(r'\s', '', s.split('【本章亮点】')[0]))
    判('②之二', '而某一旧版逐字有（故旧判据必报之）',
       any(q in o for o in 旧), True)

    # ③【证其有牙·拿 301 立闸当日之原物回灌】⛔收窄不许把牙磨掉
    # ③【证其有牙·剥注即红】⛔收窄不许把牙磨掉。
    #   ★**本格原拟拿 301 立闸当日之原物回灌，而那条路走不通**：
    #     `旧版残引` 只认「旧版 v*.md 里逐字有」之串，而 301 那三处 0904 治时
    #     **连正文里的引一并改了**（十二版逐版回灌皆得 0，本测第三跑亲印）。
    #   ⛔**故改拿本章之真局**：**把 324 骨记⑳里「原作」二字剥掉，它须当场逮得出**
    #     ——**与本日「站账逐章行」第③格同法：剥掉那一处注，闸即回到收窄之前。**
    剥 = t324.replace('⛔**原作**', '⛔**其句**')
    得 = m.旧版残引(324, 剥)
    判('③之一', '剥去「原作」二字，其残引当场逮得出（得 %d 处）' % len(得),
       len(得) >= 1, True)
    判('③之二', '而所逮者正是那一句（非别处）',
       any('扁的那一段是旧的' in x for x in 得), True)
    判('③之三', '⛔注不剥则放过（白名之界未被扫没）',
       m.旧版残引(324, t324), [])

    # ④【不许连坐】今版 301 照旧零红
    p301 = os.path.join(ROOT, '正文', '镇冢秘术_第三百零一章_一二三四五六七.md')
    if os.path.exists(p301):
        判('④', '今版 301 零红（其三处早已治毕）',
           m.旧版残引(301, io.open(p301, encoding='utf-8').read()), [])

    # ⑤【白名单只认那四个词，不许再宽】
    src = io.open(os.path.join(ROOT, '工具', '亮点对表.py'), encoding='utf-8').read()
    判('⑤', "其白名单逐字只四样（原作／改前／改後／旧作）",
       "_注 = ('原作', '改前', '改後', '改后', '旧作')" in src, True)

    print('════ 负测·亮点残引 ════（守：引了自己删掉的话即红；而改动记录不算）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
