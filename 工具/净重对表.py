#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""净重对表（2026-09-08 立·令§六③④、§十三）——**施工表锁定行自书之「净重N」，拿尺回去量一遍**。

★立此器之由（280 之席所报，本坐上盘复量）：
  `设定/01_…施工与伏笔回收表.md` 每一行 `| N | 锁定 |` 里自书一个「净重N」，
  而**全书没有一道器拿它回正文复量过**。280 之席以本书净重式逐章比对，得可比 26 章、红 7 章；
  本坐 0908 复量，红 **17 章**——多出来的十处，正是这一程回修改过正文而锁定行没跟着改。
  **账上写着一个数，而没有一把尺回去量它。** 这与「骨记在不在」同族：不是判错，是根本没在量。

★★这个数为什么要紧（不是好看，是有用）：
  本书以净重定章之带——**常章 2,500—3,500｜爆章 ≥6,000**。
  283 之锁定行自书「净重3,499」，**正压在常章带上限之下一字**，而实数 3,481——
  **一章在不在带内，判据眼下靠的是一个漂掉的数。**

★★★它认哪几样，本书同类共几样（令§六④）：
  · **认**：施工表内 `| N | 锁定 |` 之行，行内含「净重<数>」且第 N 章之正文档在者。
    今可比 **26 章**（余诸章之锁定行不书净重，本器不认——**不书就不认，不许替它猜一个**）。
  · **不认**：回执、圣经、canon、版本台账里的净重——那几本各有其口径（含题／不含题／含骨记），
    口径不一而强行对表，即是造假红。**判不死的就别做成闸。**
  · **净重之式**（与 `工具/跑轮.py` body_of／净重 同源）：取【本章亮点】以前之正文，
    剥去头一行章题（含《镇冢秘术》与「第N章　题」那一段），去尽空白後计长。

★★★★它红在哪一行（令§十三）：立此器之日，红 17 章——
  256／269／282／283／284／285／287／288／290／292／293／296／301／303／304／305／289
  （差自 −68 至 +65）。**同日逐行改齐，改的是锁定行，不是正文**——
  正文係回修所改，改得对；漂的是那个没人回去量的数。

用法：
    python3 工具/净重对表.py            # 全书
    python3 工具/净重对表.py --补        # 把锁定行之数改成实数（逐行印其改）
    python3 工具/净重对表.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 亮点对表 import 诸章  # noqa: E402

表 = os.path.join(根, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
锁 = re.compile(r'^\|\s*(\d+)\s*\|\s*锁定\s*\|')
# ★★★★★2026-09-13 放宽（324 收口之余、317 之三数一案所逮）：
#   ⛔**旧式 `净重\s*([\d,]+)` 取不着加重号之形**（`净重 **1,953**`）——
#   **而 313 与 317 两章之锁定行只有这一形**，**於是这两章的净重从来没有被验过**；
#   ★**其害在那句印**：「42 章逐行相符」——**含的只是它取得着的那 42 章，
#   取不着的两章它一个字也没说**（本册 ㊓：**一道只验一处的闸，比没有闸更会骗人**）。
#   ★★今认 `**` 与全角空格；**其数之形一字未改**，只放宽它前头那几个符号。
数 = re.compile(r'净重[\s\*　]*([\d,]+)')


def 净重(路):
    t = io.open(路, encoding='utf-8').read().split('【本章亮点】')[0]
    b = re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return len(re.sub(r'\s', '', b))


def 量(章=None, 表文=None):
    """返回 (红, 群)：红 = [(表之行号, 章号, 所记, 实数), ...]。"""
    章 = 章 or 诸章()
    L = (表文 if 表文 is not None else io.open(表, encoding='utf-8').read()).split('\n')
    红, 群 = [], 0
    for i, line in enumerate(L, 1):
        m = 锁.match(line)
        if not m:
            continue
        n = int(m.group(1))
        q = 数.search(line)
        if not q or n not in 章:
            continue
        群 += 1
        记 = int(q.group(1).replace(',', ''))
        实 = 净重(章[n])
        if 记 != 实:
            红.append((i, n, 记, 实))
    return 红, 群


def 补():
    L = io.open(表, encoding='utf-8').read().split('\n')
    红, _ = 量()
    for i, n, 记, 实 in 红:
        old = 数.search(L[i - 1]).group(0)
        new = old.replace(数.search(L[i - 1]).group(1), '{:,}'.format(实))
        L[i - 1] = L[i - 1].replace(old, new, 1)
        print('  改 表%d行 第%d章 %d → %d' % (i, n, 记, 实))
    io.open(表, 'w', encoding='utf-8').write('\n'.join(L))
    return len(红)


def 跑(报=True):
    红, 群 = 量()
    if 报:
        print('════ 净重对表 · 锁定行自书净重者 %d 章 ════' % 群)
        for i, n, 记, 实 in 红:
            print('  ⛔ 表%d行 第%d章：记 %d，实 %d（差 %+d）' % (i, n, 记, 实, 实 - 记))
        if not 红:
            print('  ✓ %d 章逐行相符（锁定行之净重与正文实算同）。' % 群)
    return len(红), 群


def 自测():
    R = []
    红, 群 = 量()
    R.append(('①认得出锁定行之净重（其群 ≥25 章）', 群 >= 25))
    R.append(('②今日零处不符', 红 == []))
    # ③净重之式与跑轮同源：拿一章手算复核
    章 = 诸章()
    n = 305
    t = io.open(章[n], encoding='utf-8').read().split('【本章亮点】')[0]
    手 = len(re.sub(r'\s', '', re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)))
    R.append(('③净重之式手算复核（305 章）', 净重(章[n]) == 手))
    # ④假盘：把一行之数改坏，须逮出
    文 = io.open(表, encoding='utf-8').read()
    坏 = None
    for line in 文.split('\n'):
        m = 锁.match(line)
        if m and 数.search(line) and int(m.group(1)) in 章:
            坏 = line
            break
    假 = 文.replace(坏, 数.sub('净重1', 坏, count=1), 1)
    r4, _ = 量(表文=假)
    R.append(('④把一行之数改作 1，逮得出', len(r4) == 1 and r4[0][2] == 1))
    # ⑤不书净重之锁定行不认（不许替它猜一个）
    假2 = 文.replace(坏, 数.sub('', 坏, count=1), 1)
    _, 群2 = 量(表文=假2)
    R.append(('⑤不书净重之行不认（其群随之减一）', 群2 == 群 - 1))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    if '--补' in sys.argv:
        print('════ 净重对表 · 补 ════')
        n = 补()
        print('  共改 %d 行。' % n)
        sys.exit(0)
    红, _ = 跑()
    sys.exit(1 if 红 else 0)
