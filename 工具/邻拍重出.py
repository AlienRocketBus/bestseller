# -*- coding: utf-8 -*-
"""邻拍重出 · 2026-09-04 立（301第13轮·升华定稿轮·甲之逐轮回检所逮）

★其红在哪一行：301第10轮之逐段生死检逐拍问过「它为什么不能删」，而它漏了一处——
  ★★拍31「数第二遍跟数第一遍，用的是同一个指甲。」，其意逐字在下一拍之首句「同一个指甲数两遍」；
  ★★★第11轮之小说家席一提即中，而第10轮那一轮通读过一遍，没看见。
★★★★其由不是读得不细，是**人读邻拍读的是意思，器读邻拍读的是字**——
  **一句话拆开来摆在两拍上，读起来是两步；逐字一比，是一句。**

★其法：逐拍与其後三拍求最长公共子串（先去标点），≥6字即报。
★★它认哪几样：**只认同一章之内、相隔三拍以内、去标点後逐字相同之串**；
  **不认转述，不认形近，不跨章**（跨章之重由看官·连读客问五量之）。
★★★本书同类共几样：**近四十章共 8 处（均每章 0.2 处，顶 2 处）**——
  ★★★★**故其常态是零；一章出三处以上，即是刀没落到底。**

⛔**而此器须当场自陈一限，不许含糊（令§一⑤·绿只及於器自印之项名）**：
  ★**它逮不着立它的那一处。** **301之拍31「用的是同一个指甲」与下一拍「同一个指甲数两遍」，
    去标点後之公共串只 5 字**——**本器之槛是 6，故它一处也不报。**
  ★★**而拟过一式而驳之**（§六第2步·数其群）：**把槛降到 5**，
    **近四十章由 8 处涨到 247 处（均6.17，顶22）**——**噪。**
  ★★★**另拟一式亦驳**：**只认「单句而≤22字之短拍，与下一拍首句共 5 字以上」**，
    **近四十章 61 处（均1.52，顶10）**，**而逐处一看其大半是本书之顶针**
    （第七十五页／床上那个人／没经第二手／跟四天前一样）——**那是本书之礼，不是伤。**
  ★★★★**故本器所守者只一样：邻拍逐字重出六字以上**；
    **而「一句话拆作两拍」那一形，今日无一条低噪之法逮得着它**——
    **其治仍在人：第10轮逐段生死检、第11轮小说家席。**
  ★★★★★**此限须写在这儿，免得下一坐把它的绿读成「邻拍无重」。**

★而其位（令§十一③）：**第10轮·收官轮**（`工具/一坐.py` 之逐轮之器表）——
  **收官轮之逐段生死检，人问其意，此器问其字。**

用：python3 工具/邻拍重出.py N  ｜  --全
"""
import io, os, re, sys, glob

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINLEN = 6
SPAN = 3


def 诸章():
    d = {}
    for p in glob.glob(os.path.join(根, '正文', '*.md')):
        m = re.search(r'第([一二三四五六七八九十百零]+)章', os.path.basename(p))
        if not m:
            continue
        s, v, u = m.group(1), 0, 0
        for c in s:
            i = '零一二三四五六七八九'.find(c)
            if i >= 0:
                u = i
            elif c == '十':
                v += (u or 1) * 10; u = 0
            elif c == '百':
                v += (u or 1) * 100; u = 0
        d[v + u] = p
    return d


def 分拍(txt):
    body = txt.split('【本章亮点】')[0]
    return [re.sub(r'[，、。！？：；「」\s]', '', x) for x in body.split('\n＊\n')]


def 查(n, p, 报=True):
    b = 分拍(io.open(p, encoding='utf-8').read())
    out = []
    for i in range(len(b) - 1):
        for j in range(i + 1, min(i + 1 + SPAN, len(b))):
            a, c = b[i], b[j]
            best = ''
            for x in range(len(a)):
                for y in range(x + MINLEN, min(len(a), x + 40) + 1):
                    if a[x:y] in c and y - x > len(best):
                        best = a[x:y]
            if len(best) >= MINLEN:
                out.append((i + 1, j + 1, best))
    if 报:
        print('████ 邻拍重出 · 第%d章 ████' % n)
        print('  ★其法：逐拍与其後三拍求最长公共子串（先去标点），≥%d字即报。' % MINLEN)
        print('  ★★本书之群：近四十章共 8 处（均每章 0.2 处，顶 2 处）——**其常态是零。**')
        print('  ★★★而器只报，不判：一处逐字之重未必是伤（本书之礼多有复沓）；')
        print('     ★★★★须逐处答一句「这两拍分开摆，是两步，还是一句话」——答不出即删其一。')
        if not out:
            print('  ✓ 全章无邻拍逐字重出（≥%d字·隔%d拍以内）。' % (MINLEN, SPAN))
        else:
            for i, j, s in out:
                print('  ⚠ 拍%-4d↔拍%-4d 共%d字：%s' % (i, j, len(s), s))
            print('  ── 计 %d 处 ──' % len(out))
            if len(out) >= 3:
                print('  ⛔ 三处以上：本书之顶是 2 处——**刀没落到底。**')
    return out


if __name__ == '__main__':
    全 = 诸章()
    if '--全' in sys.argv:
        tot = 0
        for n in sorted(全):
            r = 查(n, 全[n], 报=False)
            tot += len(r)
            if r:
                print('第%d章 %d 处：%s' % (n, len(r), r[:2]))
        print('── 全书共 %d 处 ──' % tot)
        sys.exit(0)
    a = [x for x in sys.argv[1:] if not x.startswith('-')]
    if not a or int(a[0]) not in 全:
        print('⛔ 用：python3 工具/邻拍重出.py N ｜ --全')
        sys.exit(2)
    n = int(a[0])
    r = 查(n, 全[n])
    sys.exit(1 if len(r) >= 3 else 0)
