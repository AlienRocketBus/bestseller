#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第零轮 · 开镜庭（2026-08-16 立）

★而其立之由：十轮之职是「治这一章」，第十一轮之职是「查十轮跑透没有」——
★★而无一轮问这三件：①这一章该不该是这一章（其位对不对）／
②这一章之前该不该先插一章（暗线／别人之镜头）／③这一章写完下一章该是谁的镜头。
★★★而沈鸢漂八十五章、三十七万八千字，正是从这个缝里漏掉的。

★★★★而其所以立为「第零轮」而非「第十二轮」，其由有二：
  ★一为十轮之职是治这一章，而「该不该插一章」是治章与章之间，混进十轮会走味；
  ★★二为这件事须在起草之前问——★★★写完再问「该不该插一章」，
  那一章已经写了五千八百字；★★★★而那时要么白写，要么将就。

用法：
    python3 工具/第零轮开镜庭.py 202        # 起草前跑，出开镜卡
    python3 工具/第零轮开镜庭.py --静 202   # 只报成败（供全测调用）
"""
import sys, re, os, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def cn(p):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(p))
    if not m:
        return -1
    s = m.group(1)
    t = n = 0
    for ch in s:
        if ch in CN and ch != '十':
            n = CN[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


F = {cn(p): p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if cn(p) > 0}


def body(c):
    return open(F[c], encoding='utf-8').read().split('【本章亮点')[0]


def net(t):
    return len(re.sub(r'\s', '', t))


def is_dark(c):
    """★暗线章之判：「我」之密度<3/千字者，即为第三人称之暗线章。"""
    if c not in F:
        return False
    b = body(c)
    w = net(b)
    return (b.count('我') / w * 1000) < 3 if w else False


DARK_EVERY = 10   # ★闸⑤之配额：每10章至少1篇暗线章
GATE_FROM = 200   # ★闸立於第200章

# ★可切镜者与其令（圣经原文·2026-08-16 逐条取毕）
DARK_WHO = [
    ('沈鸢',   '★无禁令｜CHAR-191A限210｜★★而其线只能待四人出洞方接得上'),
    ('黎东来', '★★★卷四起每卷至少1篇其流程视角（明令）｜★★★★恐怖不在凶相，在流程'),
    ('霍钧',   '★★须分层揭露，不得一篇交尽｜★★★青溪是他27年前之旧伤地（可写其对这地名之反应，不露名）'),
    ('祖先',   '★起源纪可写｜★★而「赵阙」「苏玄微」为正文永禁机制词，须以口语落地'),
    ('老头',   '★★★★未禁，然宜缓——他瞒苏衍二十年，一开即收不回；宜留至出洞后且只开一次'),
    ('钱满',   '未禁'),
    ('刘二',   '未禁'),
    ('赵阙',   '⚠受限：只在已连接者之意识、梦与节点异象中现，不得有全知视角'),
]

# ★一站九步（圣经原文）——★★而暗线在第八步
NINE = ['路途', '到站近核', '本站独有的麻烦', '顶着麻烦做五步',
        '验熄与清账', '★反派侧落一笔（暗线）', '下一向接班收章']


def q1_wei(c):
    """★问一·本章之位：这一章该是主线还是暗线。"""
    out = []
    win = [x for x in range(max(GATE_FROM + 1, c - DARK_EVERY), c) if x in F]
    dk = [x for x in win if is_dark(x)]
    n_since = 0
    for x in range(c - 1, GATE_FROM, -1):
        if x in F:
            if is_dark(x):
                break
            n_since += 1
    if not win:
        out.append(('一之a·近%d章之暗线' % DARK_EVERY, True, '★窗内%d章（立闸未满一窗）' % len(win)))
    else:
        ok = len(dk) >= 1
        out.append(('一之a·近%d章之暗线' % DARK_EVERY, ok,
                    '%d 篇｜距上一篇 %d 章%s' % (len(dk), n_since,
                                          '' if ok else '⛔零篇：本章宜为暗线')))
    # ★★而依「一站九步」：前章若刚走完「验熄与清账」，则本章当为第八步
    hint = '★★而依一站九步：暗线在第八步（验熄与清账之后、下一向接班之前）'
    out.append(('一之b·九步之位', True, hint))
    return out, (n_since >= DARK_EVERY - 1)


def q2_jing(c):
    """★★问二·本章之镜：若为暗线，是谁的镜头。"""
    out = []
    last = {}
    for w, _ in DARK_WHO:
        ln = None
        for x in sorted(F):
            b = body(x)
            if w in b:
                ln = x
        last[w] = ln
    rows = []
    for w, rule in DARK_WHO:
        ln = last.get(w)
        gap = (c - ln) if ln else c
        rows.append((w, ln, gap, rule))
    rows.sort(key=lambda r: -r[2])
    out.append(('二·可切之镜（按其距排）', True, ''))
    for w, ln, gap, rule in rows[:5]:
        out.append(('   · %s' % w, True,
                    '末见第%s章｜距 %d 章｜%s' % (ln if ln else '—', gap, rule[:42])))
    return out


def q3_yishi(c):
    """★★★问三·本章之一事：起草前须写明一句（闸①之前置）。"""
    p = os.path.join(ROOT, '版本', '第%d章' % c, '_开镜卡.md')
    has = os.path.exists(p)
    key = ''
    if has:
        t = open(p, encoding='utf-8').read()
        m = re.search(r'本章之一事[：:]\s*(.+)', t)
        key = m.group(1).strip()[:30] if m else ''
    # ★★★★★2026-08-17 焊：卡在不算数，四问须填毕。
    # ★而其由：207之卡於2026-08-16已立，然四问皆为占位符原样；
    # ★★而机器只测「卡在不在」，遂判过——★★★而这一过，等於没测。
    # ★★★★故加一测：卡内若有占位符「〔」，即报。
    if not has:
        return [('三·本章之一事（起草前写明）', False,
                 '⛔未立：须先出开镜卡（本工具 --立 %d）' % c)]
    ph = t.count('〔')
    if ph:
        return [('三·本章之一事（起草前写明）', False,
                 '⛔卡在而四问未填毕：占位符 %d 处（★而此测2026-08-17焊入）' % ph)]
    return [('三·本章之一事（起草前写明）', True,
             '★已立且填毕：%s' % key if key else '★已立开镜卡且四问填毕')]


def make_card(c):
    """★立开镜卡（起草前之实产物）。"""
    d = os.path.join(ROOT, '版本', '第%d章' % c)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, '_开镜卡.md')
    if os.path.exists(p):
        print('★开镜卡已在：%s' % p)
        return p
    rows, need_dark = q1_wei(c)
    prev = c - 1
    tmpl = '''# 第%d章 · 开镜卡（第零轮·开镜庭 2026-08-16 立）

## ★问一·本章之位
- **本章为**：〔主线／暗线〕 ← **★须先定**
- **★★而其据**：近%d章之暗线篇数、距上一篇几章、一站九步走到第几步。
- **★★★而机器所报**：%s

## ★★问二·本章之镜（若为暗线）
- **本章之镜**：〔沈鸢／黎东来／霍钧／祖先／老头／钱满／刘二〕
- **★而其令**（圣经原文，不可违）：
  - **沈鸢**：无禁令｜其线只能待四人出洞方接得上
  - **黎东来**：卷四起每卷至少1篇其流程视角｜**恐怖不在凶相，在流程**
  - **霍钧**：须分层，不得一篇交尽｜青溪是他27年前之旧伤地（可写其反应，不露名）
  - **祖先**：起源纪可写，然「赵阙」「苏玄微」为正文永禁机制词，须以口语落地
  - **老头**：未禁然宜缓——他瞒苏衍二十年，一开即收不回
  - **赵阙**：⚠只在已连接者之意识、梦与节点异象中现，不得有全知视角

## ★★★问三·本章之一事
- **本章之一事**：〔一句话，写在此处〕
- **★而其测**（闸①）：本章之料须逐件皆自这一事所出；若出二事，即拆章。

## ★★★★问四·下一章该是谁的镜头
- **下一章**：〔主线／暗线·谁〕
- **★而此项为「钩子不许烂尾」之前置**（圣经原文：每章收章之悬账须记入施工表该章行）。

---
**★★★★★而此卡须於起草之前填毕**；**★填毕即抄一行「本章之一事」入轮记之首。**
''' % (c, DARK_EVERY, '；'.join('%s %s' % (n, m) for n, ok, m in rows if m))
    open(p, 'w', encoding='utf-8').write(tmpl)
    print('★开镜卡已立：%s' % p)
    print('★★而其须於起草之前填毕（四问）。')
    return p


# ───────── 〇·本章之正文在不在（2026-08-17 立）─────────
# ★★★★★其由：2026-08-17 起草205时，其正文先前已起草过（且第1轮已跑毕，台账v01—v08）；
# ★而我未察，又写了一篇，遂在其上跑了三版，覆盖了先立者之台账。
# ★★而逮出之处为全测之「章节编号不连续」（其报 …204, 205, 205）。
# ★★★故立此问：起草之前，先查其正文在不在。
def check0(c):
    """★本章之正文在不在（起草之前须为零）。"""
    import glob as _g
    hit = [x for x in _g.glob(os.path.join(ROOT, '正文', '*.md')) if cn(x) == c]
    return [('〇·本章之正文在不在（起草前须为零）', len(hit) <= 1,
             ('★%d 篇' % len(hit)) if len(hit) <= 1
             else '⛔%d 篇同章号：%s（★★★★★须先撤其一，否则台账互相覆盖）'
                  % (len(hit), '、'.join(os.path.basename(x) for x in hit)))]

def run(c, quiet=False):
    rows = []
    rows += check0(c)
    r1, need = q1_wei(c)
    rows += r1
    rows += q2_jing(c)
    rows += q3_yishi(c)
    bad = sum(1 for _, ok, _ in rows if not ok)
    if quiet:
        print('第零轮通过' if bad == 0 else
              '；'.join('%s %s' % (n, m) for n, ok, m in rows if not ok))
        return 0 if bad == 0 else 2
    print('=' * 66)
    print('  第零轮 · 开镜庭 · 第%d章（起草之前跑）' % c)
    print('=' * 66)
    for name, ok, msg in rows:
        if msg:
            print('  %s %-30s %s' % ('✓' if ok else '⛔', name, msg))
        else:
            print('  %s %s' % ('✓' if ok else '⛔', name))
    print('=' * 66)
    if need:
        print('  ★★★★★而机器之荐：本章宜为暗线章（距上一篇已近一窗）。')
    print('  %s' % ('✓ 开镜庭过，可起草。' if bad == 0 else
                    '⛔ 开镜庭报 %d 处——★须先立开镜卡并填毕四问，方可起草。' % bad))
    print('=' * 66)
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if '--立' in sys.argv:
        sys.exit(0 if make_card(int(a[0])) else 2)
    q = '--静' in sys.argv
    c = int(a[0]) if a else (max(F) + 1 if F else 1)
    sys.exit(run(c, q))
