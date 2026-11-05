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
    # 0924：与检察官 _weight_stats 同尺——换场符「＊」不是字（363 两尺差 13 即此）
    return sum(len(re.sub(r'\s', '', x)) for x in b.split('\n') if x.strip() != '＊')



# ★★★★★★2026-09-13 立第二路（其实逼出来的）：
#   ⛔**本器只验「锁定行」那一处；而净重在册上还有第二形**——
#   **「…320:2137、321:2246、322:1990」这样的列**，**同一章在册上出现七八回**。
#   ★0913 之实：**大审第 1 笔落刀，六章净重同日变过**；**锁定行我改齐了，器报绿**——
#   **而那几列里的旧数一处未动，315 一章就有八处**。
#   ★★**与 ㊎ 同骨，而更阴**：**`负测_净重一处` 只问「册上这几个数彼此同不同」**，
#   **它们八处齐齐地错着，故它也报绿**：**两道闸各守一半，中间那一截谁也没管。**
#   ⛔**故立此路：那几列里的数，须与正文实算同。**
列 = re.compile(r'(?<![0-9`])(\d{3}):(\d{3,5})(?![0-9`])')


def 列量(章=None, 表文=None):
    """返回 (红, 群)：验「净重之列」里 `N:数` 之形与实算同。
    ⛔只取同一行内含「净重」二字者（那一行本就是净重之列）——
    否则 `322:237` 这类行引会被当成净重（`负测_净重一处` 头一版即栽在此）。"""
    章 = 章 or 诸章()
    L = (表文 if 表文 is not None else io.open(表, encoding='utf-8').read()).split('\n')
    红, 群 = [], 0
    for i, line in enumerate(L, 1):
        if '净重' not in line or 锁.match(line):
            continue
        for m in 列.finditer(line):
            n, 记 = int(m.group(1)), int(m.group(2))
            if n not in 章:
                continue
            # ⛔括注里明说是陈数者不认（其形同 `负测_净重一处`：近处见「旧书／旧号／陈号／旧作／原书」）
            # ★0913 立日当场自栽一回：**我把「旧书 292:2595」写进回补之注，它又报了一回红**
            #   ——**判据一立，连我自己写的注都得守它**。
            if any(k in line[max(0, m.start() - 14):m.start()]
                   for k in ('旧书', '旧号', '陈号', '旧作', '原书')):
                continue
            实 = 净重(章[n])
            # ⛔行引与净重共用此形，故须再收一格：净重必远大於该章行数
            if 记 <= len(io.open(章[n], encoding='utf-8').read().split('\n')):
                continue
            群 += 1
            if 记 != 实:
                红.append((i, n, 记, 实))
    return 红, 群


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
    # ★1014 W26／W30 两回漏：列内之「N:数」旧须手正——今随锁定行一并照正文实算补（近处注陈数者，列量本不认，⛔动）
    红二, _ = 列量(表文='\n'.join(L))
    for i, n, 记, 实 in 红二:
        L[i - 1] = re.sub(r'(?<![0-9`])%d:%d(?![0-9`])' % (n, 记), '%d:%d' % (n, 实), L[i - 1], count=1)
        print('  改 表%d行 列内第%d章 %d → %d' % (i, n, 记, 实))
    io.open(表, 'w', encoding='utf-8').write('\n'.join(L))
    return len(红) + len(红二)


def 跑(报=True):
    红, 群 = 量()
    红二, 群二 = 列量()
    if 报:
        print('════ 净重对表 · 锁定行自书净重者 %d 章 ════' % 群)
        for i, n, 记, 实 in 红:
            print('  ⛔ 表%d行 第%d章：记 %d，实 %d（差 %+d）' % (i, n, 记, 实, 实 - 记))
        if not 红:
            print('  ✓ %d 章逐行相符（锁定行之净重与正文实算同）。' % 群)
        print('  ── 第二路·净重之列（0913 立）──')
        for i, n, 记, 实 in 红二:
            print('  ⛔ 表%d行 列内第%d章：记 %d，实 %d（差 %+d）' % (i, n, 记, 实, 实 - 记))
        if not 红二:
            print('  ✓ 列内 %d 处逐处相符。' % 群二)
    return len(红) + len(红二), 群


def 自测():
    R = []
    红, 群 = 量()
    R.append(('①认得出锁定行之净重（其群 ≥25 章）', 群 >= 25))
    R.append(('②今日零处不符', 红 == []))
    # ③净重之式与跑轮同源：拿一章手算复核
    章 = 诸章()
    n = 305
    t = io.open(章[n], encoding='utf-8').read().split('【本章亮点】')[0]
    # ★0924 改：手算之式旧含「＊」（净重同尺之後即成两尺）——今直取铁底闸所用之尺（检察官 _weight_stats）逐章比，
    #   ⛔并验 363（13 个＊·两尺曾差 13 之章）：二尺之差若复现即红
    import importlib.util as _u
    _s = _u.spec_from_file_location('_检', os.path.join(os.path.dirname(os.path.abspath(__file__)), '小说检察官.py'))
    _检 = _u.module_from_spec(_s); _s.loader.exec_module(_检)
    _差 = [k for k in (305, 363) if k in 章 and 净重(章[k]) != _检._weight_stats(io.open(章[k], encoding='utf-8').read())[0]]
    R.append(('③净重与铁底闸同尺（305、363 逐章比·今相差：%s）' % (_差 or '无'), not _差))
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
    # ⑥⑦⑧【第二路·0913 立·须当场证它有牙，且不误伤行引】
    红二, 群二 = 列量()
    R.append(('⑥净重之列认得出（其处 ≥20）', 群二 >= 20))
    R.append(('⑦今日列内零处不符', 红二 == []))
    行 = [l for l in 文.split('\n') if '净重' in l and not 锁.match(l) and 列.search(l)]
    假3 = 文.replace(行[0], 列.sub(lambda m: '%s:%s' % (m.group(1), '9' * len(m.group(2))),
                                  行[0], count=1), 1)
    r6, _ = 列量(表文=假3)
    R.append(('⑧把列内一个数改坏，逮得出', len(r6) == 1))
    # ⑨⛔行引之形（同行无「净重」二字）不许被当成净重
    r7, g7 = 列量(表文='- 其凭 `322:237`／`324:17` 两处亲印。')
    R.append(('⑨无「净重」二字之行引不认', r7 == [] and g7 == 0))
    # ⑩⛔并证「旧书」之免不是一个洞：同一个错数，带注即放、不带注即红
    n0 = sorted(章)[len(章) // 2]
    坏数 = 净重(章[n0]) + 7
    带注 = '- 净重之列：（旧书 %d:%d）' % (n0, 坏数)
    裸 = '- 净重之列：%d:%d' % (n0, 坏数)
    r8, _ = 列量(表文=带注)
    r9, _ = 列量(表文=裸)
    R.append(('⑩「旧书」之免只免带注者（裸者照旧红）', r8 == [] and len(r9) == 1))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


def 稿之量(路):
    """★1016（393 逮：执笔令「落笔前照此估、⛔跑器」，诸席在思考里数字——一席单回逾 128k 输出而死，三席各 25 万上下，章费倍）：
    一档之净重与硬项（非零者），供执笔写毕之同一条命令末尾一跑。"""
    from 硬闸 import 硬项
    t = io.open(路, encoding='utf-8').read()
    红 = {k: v for k, v in 硬项(t).items() if v and k not in ('段间空行病', '章号入正文')}   # 此二格係合稿入正文之式，稿⛔计
    return 净重(路), 红


if __name__ == '__main__':
    if '--量' in sys.argv:
        路 = sys.argv[sys.argv.index('--量') + 1]
        n, 红 = 稿之量(路)
        print('净重 %d｜硬项 %s' % (n, '零' if not 红 else '、'.join('%s %d' % kv for kv in 红.items())))
        sys.exit(0)
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    if '--补' in sys.argv:
        print('════ 净重对表 · 补 ════')
        n = 补()
        print('  共改 %d 行。' % n)
        sys.exit(0)
    红, _ = 跑()
    sys.exit(1 if 红 else 0)
