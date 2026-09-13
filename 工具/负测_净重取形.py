# -*- coding: utf-8 -*-
"""负测·净重取形（2026-09-13 立·317 之三数一案所逮）。

★所守者一句：**锁定行之净重，凡加重号之形（`净重 **1,953**`），器须取得着。**
★★其实：`净重对表.py` 旧式正则作 `净重\\s*([\\d,]+)`——**星号挡在数前，它一概取不着**；
　**而 313 与 317 两章之锁定行只有这一形**，**於是这两章的净重从来没有被验过。**
★★★⛔**其害不在漏一章，在那句印**：「**42 章逐行相符**」——
　**含的只是它取得着的那 42 章；取不着的两章，它一个字也没说。**
　★**放宽之後即 44 章，当场逮出三章真红**：**317 记1953实2010｜313 记3299实3287｜312 记1960实2012。**
⛔**本册 ㊓ 之第二变种**：**一道只验它取得着的那些的闸，比没有闸更会骗人。**
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
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
表 = os.path.join(ROOT, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')


def _m():
    spec = importlib.util.spec_from_file_location(
        '_jz', os.path.join(ROOT, '工具', '净重对表.py'))
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

    # ①【其正则须认加重号】⛔这是本测之骨
    判('①之一', '今式认裸形', bool(m.数.search('净重 1,953')), True)
    判('①之二', '⛔且认加重号之形（旧式此处取不着）',
       bool(m.数.search('净重 **1,953**')), True)
    判('①之三', '取出之数不含星号（得 %s）' % (m.数.search('净重 **1,953**').group(1),),
       m.数.search('净重 **1,953**').group(1), '1,953')

    # ②【证其群·星形确有其章】⛔否则第①格是空的
    裸, 星 = set(), set()
    for ln in io.open(表, encoding='utf-8', errors='replace').read().split('\n'):
        mm = re.match(r'\| (\d+) \| 锁定', ln)
        if not mm:
            continue
        n = int(mm.group(1))
        if re.search(r'净重\s*[\d,]+', ln):
            裸.add(n)
        if re.search(r'净重\s*\*\*[\d,]+', ln):
            星.add(n)
    判('②之一', '星形之章确在盘上（得 %s）' % sorted(星), bool(星), True)
    判('②之二', '⛔而其中有只星形者（旧式一概看不见·得 %s）' % sorted(星 - 裸),
       bool(星 - 裸), True)

    # ③【证其有牙·拿旧式回灌】⛔收窄或放宽，皆须证它换了之後真不一样
    旧式 = re.compile(r'净重\s*([\d,]+)')
    旧得 = sum(1 for n in 星 - 裸 if 旧式.search('净重 **1,953**'))
    判('③之一', '旧式对加重号之形取不着（证其曾漏）',
       bool(旧式.search('净重 **1,953**')), False)
    判('③之二', '而今式取得着', bool(m.数.search('净重 **1,953**')), True)

    # ④【今日之实】全表逐行相符，且其数须逾旧之 42
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '净重对表.py')],
                       capture_output=True, text=True, cwd=ROOT, timeout=600)
    out = r.stdout or ''
    mm = re.search(r'自书净重者 (\d+) 章', out)
    判('④之一', '其可比之章取得出（得 %s）' % (mm.group(1) if mm else None),
       bool(mm), True)
    判('④之二', '⛔其数须逾旧之 42（今 %s）' % (mm.group(1) if mm else '?'),
       int(mm.group(1)) > 42 if mm else False, True)
    判('④之三', '今日逐行相符', '逐行相符' in out, True)

    print('════ 负测·净重取形 ════（守：加重号之形，器须取得着）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
