#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回修 · 已封版之章的改动之刀（2026-08-19 立）

★立此刀之由（作者令）：
  「封版之后一样也可以改，只要能够让我们整本书的质量达到最好最高。」
  而此令非今日新立——第六十六批（2026-07-19）早已立「封版≠不可改」；
  ★★而它躺了一个月一次没跑过，因为它只是一段字：无闸、无刀、无入口。
  ★★★而依批100之融入标准：只喷字不设闸者，视同未融入。故今日补其刀与闸。

★★而回修之险不在「改」，在「改了上游，下游哪几章跟着塌，没人看得见」。
  ★十三轮是章级的：它只看这一章。
  ★★而一个改动的代价是书级的：第N章一个数、一件器物、一句判，
     可能被 N+1..末章 引过十几回。
  ★★★故此刀之职只有一样：**把「改这一处，要连着看哪几章」算出来。**

用法：
    python3 工具/回修.py --波及 N            # 查第N章之料被下游哪些章引过
    python3 工具/回修.py --波及 N --词 血图    # 只查某一样东西
    python3 工具/回修.py --开案 N "为何要改"   # 开一份回修案（落盘·须逐项填）
    python3 工具/回修.py --验案 N            # 验回修案是否办毕（封版闸据此放行）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import json
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = os.path.join(ROOT, '正文')
CASE = os.path.join(ROOT, '设定', '回修案')

_CN = '零一二三四五六七八九十百'


def _num(s):
    """自中文章名取章号（★而其须能解二百零三、二百一十八、七十二、九）。"""
    m = re.search(r'第([%s]+)章' % _CN, s)
    if not m:
        return None
    d = {c: i for i, c in enumerate('零一二三四五六七八九')}
    sec, cur = 0, 0
    for c in m.group(1):
        if c in d:
            cur = d[c]
        elif c == '十':
            sec += (cur if cur else 1) * 10
            cur = 0
        elif c == '百':
            sec += (cur if cur else 1) * 100
            cur = 0
    return sec + cur or None


# ★★而波及查之大敌是噪音：「一个人」「一会儿」「三个字」这类通用词
#   在本书里章章都有，牵连九十九章——**它报的不是波及，是这本书的口音**。
#   ★故立「独有度」之尺：一样料若在本章之前就已散见於多章，它就不是本章之料。
#   ★★真正要看的，是**本章头一次出现、而后文接着用**的那些。
def _is_own(word, n, ch, tol=1):
    """此词是不是「本章之料」：其前之章至多 tol 章用过。"""
    used = 0
    for c in sorted(k for k in ch if k < n):
        if word in body(ch[c]):
            used += 1
            if used > tol:
                return False
    return True


def chapters():
    """返回 {章号: 路径}。"""
    out = {}
    for f in glob.glob(os.path.join(TXT, '*.md')):
        n = _num(os.path.basename(f))
        if n:
            out[n] = f
    return out


def body(p):
    return open(p, encoding='utf-8').read().split('【本章亮点】')[0]


# ★что算「一样料」：本书之料多为「数＋量词」「器物名」「引语」「判语」。
#   而其共性：**它是后文可以引的东西**。故取三类。
def haul(text):
    """自一章正文抽出「可被下游引用之料」。"""
    out = {}
    # 一·数与量（本书之锚多在此：两指、一寸、第四十六天、二十七级…）
    for m in re.findall(r'[第]?[零一二三四五六七八九十百千两]{1,4}[尺寸指节步级天日回条道根块页行档]', text):
        out.setdefault('数量', set()).add(m)
    # 二·引语（老头钱满之判，后文常引）
    for m in re.findall(r'[“"]([^”"]{2,20})[”"]', text):
        out.setdefault('引语', set()).add(m)
    # 三·器物与专名（三至五字之名词串，去掉常见虚词开头者）
    for m in re.findall(r'[\u4e00-\u9fa5]{2,5}', text):
        if len(m) >= 3 and not re.match(r'^(而|是|的|了|我|他|这|那|不|没|就|也|又|还|只|把|在|有|说|看|摸)', m):
            out.setdefault('词组', set()).add(m)
    return out


def hit(n, word, ch):
    """某词在 n 之后哪几章出现。"""
    got = []
    for c in sorted(k for k in ch if k > n):
        if word in body(ch[c]):
            got.append(c)
    return got


def wave(n, only=None, top=40):
    """★波及查：改第n章，下游哪些章会被连累。"""
    ch = chapters()
    if n not in ch:
        print('  ⛔无第%d章。' % n)
        return 2
    print('\n████ 回修·下游波及查 · 第%d章 ████' % n)
    print('  【why】十三轮是章级的，只看这一章；而一个改动的代价是书级的。')
    print('  【读法】下表不是「不许改」，是「改这一处，要连着看哪几章」。')
    print('  下游共 %d 章（第%d—%d章）。' % (
        len([k for k in ch if k > n]), n + 1, max(ch)))

    t = body(ch[n])
    if only:
        got = hit(n, only, ch)
        print('\n  ── 指定之词：「%s」──' % only)
        print('     本章出现 %d 次｜下游引用 %d 章：%s'
              % (t.count(only), len(got),
                 '、'.join(str(x) for x in got) if got else '无'))
        if got:
            print('\n  ── 下游原句（逐章首现）──')
            for c in got[:12]:
                for line in body(ch[c]).split('\n'):
                    if only in line:
                        print('   %3d| %s' % (c, line.strip()[:76]))
                        break
        return 0

    h = haul(t)
    rows = []
    for kind in ('数量', '引语', '词组'):
        for w in h.get(kind, ()):
            if len(w) < 2:
                continue
            got = hit(n, w, ch)
            if not got:
                continue
            if not _is_own(w, n, ch):
                continue          # ★前文已散见者，非本章之料，是本书之口音
            rows.append((len(got), kind, w, got))
    rows.sort(reverse=True, key=lambda x: (x[0], x[1]))

    if not rows:
        print('\n  ✓本章之料，下游一处未引——**此章可独立回修，波及为零。**')
        return 0

    print('\n  ── 本章之料·被下游引用者（按牵连章数降序，录前%d条）──' % top)
    print('     %-5s %-12s %-6s %s' % ('类', '料', '牵连', '章号'))
    for cnt, kind, w, got in rows[:top]:
        s = '、'.join(str(x) for x in got[:10])
        if len(got) > 10:
            s += '…等%d章' % len(got)
        print('     %-5s %-12s %-6d %s' % (kind, w[:11], cnt, s))

    heavy = [r for r in rows if r[0] >= 5]
    print('\n  ══ 定论 ══')
    print('   牵连≥5章之料 %d 件。' % len(heavy))
    if heavy:
        print('   ★而改动若碰到下列任一件，须逐章回看，不得只改本章：')
        for cnt, kind, w, got in heavy[:12]:
            print('     · %s（%d章）' % (w, cnt))
    print('   ★★而牵连为零之料，改之无须回看下游。')
    print('   ★★★此刀只算波及，不判该不该改——该不该改，只有一把尺：改了全书是不是更好。')
    return 0


CASE_TPL = '''# 回修案 · 第{n}章（{date}）

> **★立案之由（作者令·第六十六批）**：封版≠不可改；**凡能令整本书更好之改动，正文完全可改。**
> **★★而其唯一之尺**：不问「这一处能不能过闸」，问「改了之后，整本书是不是更好」。

## 一·为何要改（须写实，不得写「可以更好」这类空话）

{why}

**★而三问逐条答（答不出即不立案）**：
- **①这一处不改，读者会在哪一段掉下去？**（★须指名段落；指不出，就不是质量问题，是手痒）
  · 答：
- **②改了之后，它服务的是这一章，还是全书？**（★只服务这一章的，等下一轮；服务全书的，现在改）
  · 答：
- **③它牵动几章？**（★跑 `--波及 {n}`，把数贴在这儿）
  · 答：

## 二·改什么（逐处列，改前改后并录）

| # | 段/处 | 原文 | 改后 | 何以更好 |
|---|---|---|---|---|
| 1 |  |  |  |  |

## 三·下游波及（`--波及 {n}` 之结果，逐件裁）

| 料 | 牵连章 | 裁（不动／同改／须回看） | 记因 |
|---|---|---|---|
|  |  |  |  |

## 四·连带须同步者（逐项打钩，缺一不放行）

- [ ] **本章亮点段**（改正文必重写亮点段）
- [ ] **圣经入册条**（第{n}章「已接写」那一条是本章之摘要）
- [ ] **下一章之锚**（第{m}章「必须从…接写」照的是本章末状态）
- [ ] **canon 状态卡**（若改动涉及状态卡所记之物）
- [ ] **施工表本章行**
- [ ] **到期账**（若改动清了或翻了某笔）
- [ ] **阅读器同步**

## 五·改后复验（须逐项跑，贴实数）

- [ ] `python3 工具/小说检察官.py --改检 {n}`（机械层须干净）
- [ ] `python3 工具/跑轮.py --补存 {n} "回修·…"`（硬项须0）
- [ ] `python3 工具/小说检察官.py --十一轮 {n}`（两眼齐审须过）
- [ ] `python3 工具/全测.py`（除「回修案」一项自指外须全绿·0924 改：本格若连自己也要绿即永不可勾）

## 六·定论（一句话，须敢说）

**★改完之后，这一章比原来强在哪一处？**
· 答：

**★★而全书因这一改，强在哪一处？**（★答不出这一句，此案不成立——因为回修之令，为的是整本书）
· 答：
'''


def open_case(n, why):
    os.makedirs(CASE, exist_ok=True)
    p = os.path.join(CASE, '回修案_第%d章_%s.md'
                     % (n, datetime.datetime.now().strftime('%Y%m%d')))
    if os.path.exists(p):
        print('  ⚠本章今日已有案：%s' % os.path.relpath(p, ROOT))
        return 0
    open(p, 'w', encoding='utf-8').write(CASE_TPL.format(
        n=n, m=n + 1, date=datetime.datetime.now().strftime('%Y-%m-%d'), why=why))
    print('  ✓回修案已立：%s' % os.path.relpath(p, ROOT))
    print('  ★而立案不等于可改——须先跑 `--波及 %d`，把第三节填实，再动刀。' % n)
    return 0


def check_case(n):
    """★验案：回修案是否办毕。封版闸据此放行。"""
    os.makedirs(CASE, exist_ok=True)
    fs = sorted(glob.glob(os.path.join(CASE, '回修案_第%d章_*.md' % n)))
    print('\n████ 回修案·验 · 第%d章 ████' % n)
    if not fs:
        print('  ✓本章无回修案（未开案即未回修）。')
        return 0
    bad = 0
    for f in fs:
        t = open(f, encoding='utf-8').read()
        boxes = re.findall(r'- \[( |x|X)\]', t)
        done = sum(1 for b in boxes if b.lower() == 'x')
        empty = len(re.findall(r'· 答：\s*\n', t))
        print('  %s' % os.path.relpath(f, ROOT))
        print('     打钩 %d/%d｜未答之问 %d' % (done, len(boxes), empty))
        if done < len(boxes):
            print('     ⛔连带同步与复验未办毕，禁封版。')
            bad += 1
        if empty:
            print('     ⛔尚有 %d 问未答（其中「全书因这一改强在哪一处」不答即案不成立）。' % empty)
            bad += 1
    if bad:
        print('\n  ⛔回修案未办毕：%d 项。' % bad)
        return 2
    print('\n  ✓回修案俱办毕，可封版。')
    return 0


def main(a):
    if not a:
        print(__doc__)
        return 0
    if a[0] == '--波及':
        w = None
        if '--词' in a:
            w = a[a.index('--词') + 1]
        return wave(int(a[1]), only=w)
    if a[0] == '--开案':
        return open_case(int(a[1]), a[2] if len(a) > 2 else '（未填）')
    if a[0] == '--验案':
        return check_case(int(a[1]))
    print(__doc__)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
