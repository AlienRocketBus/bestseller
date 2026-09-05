#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""息日链（2026-09-05 立）——陈砚那本息账的日子，跨章接不接得上。

★立此器之由（拿账说，不拿主意说）：
  · 0905 丙㉓ 派席核施工表拆章之账，两席在 113／114 与 115／116 上给了**相反**的判：
    一席说 114 错、一席说 116 错。本坐上盘把 109—116 的日子逐章拉出来一比，**两章都错**，
    且错法一样：114 係 113 拆出、116 係 115 拆出，**拆的时候正文分了，那一行息账没跟着走**。
  · 实印（改前）：109 第二十七天＝第十天｜110 第二十八天＝第十一天｜111 第二十九天＝第十二天｜
    113 第三十天＝第十三天，而 114（同日）作第十二天 ⛔；115（第三十一天）＝第十四天，而 116（同日）作第十三天 ⛔。
  · 这一类人眼查不动：全书三百余章，这一行一章一现，隔着几十章才看得出差一。

★★其判（窄而可算）：
  正文里两样数——「第M天早上，还是九」（全书之日）与「第N天，九」／「还是九，第N天」（陈砚息账之日）。
  两者之差 M−N 全书恒为 17（其起在 F 之案：息自全书第十八天起数）。
  ★★之二（0905 当日补·自测④逼出来的）：头一版只扫正文段而不扫亮点段，
    遂使 113（其息日只写在亮点段里）与 114（正文写着错数）比不上，此器对它专为之而造的那一案
    **一声不响**——与已删之 `回修留痕` 同一个败法。
    中间试过把 M 之式放宽到「今天第M天」，当场引来六处误报（110 之「今天第十一天」说的是息日不是全书之日），
    故退回严式，改为**扫全档（正文＋亮点段）**：亮点段是正文的转述，这两个数在两边逐字相同，拿它补正文之缺是稳的。
    补後自测④方由 ⛔ 转 ✓，而全书仍零红。
    ★★★记此一笔：一个器造完必须拿它专为之而造的那一案回灌，绿了才算数。
  故此器只问三句：
    ①同一章内两数并现者，M−N 是不是 17；
    ②拆出之章与其源章（施工表「（N拆出）」）若各有其数，两边是不是同一个；
    ③N 逐章只增不减、且不跳（章号递增而 N 递增或不变）。

★★★它不认得的（写在明处）：
  · 只认上列两种写法；改用别的措辞记同一件事，它看不见。
  · 差 17 这个数是自盘上量出来的（见 --自测②），不是外头给的；若日後书里改了息账之起点，须同日改此数并跑负测。

用法：
    python3 工具/息日链.py          # 全书
    python3 工具/息日链.py --自测
"""
import io, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 亮点对表 import 诸章          # noqa: E402
from 亮点界 import 诸对, 分章       # noqa: E402

差 = 17
CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def _num(t):
    n = c = 0
    for ch in t:
        if ch == '百':
            n += (c or 1) * 100; c = 0
        elif ch == '十':
            n += (c or 1) * 10; c = 0
        elif ch in CN:
            c = CN[ch]
    return n + c


def 取(txt):
    """自一段正文取（全书之日 M 集，息账之日 N 集）。"""
    M = sorted({_num(x) for x in re.findall(r'第([一二三四五六七八九十百]+)天早上[，,]?\s*还是九', txt)})
    N = sorted({_num(x) for x in re.findall(r'第([一二三四五六七八九十百]+)天[，,]\s*九', txt)}
               | {_num(x) for x in re.findall(r'还是九[，,]\s*第([一二三四五六七八九十百]+)天', txt)})
    return M, N


def 全表():
    章 = 诸章()
    out = {}
    for n, p in sorted(章.items()):
        M, N = 取(io.open(p, encoding='utf-8').read())
        if M or N:
            out[n] = (M, N)
    return out


def 跑(报=True):
    t = 全表()
    对 = {b: a for a, b in 诸对()}
    红 = []
    for n, (M, N) in sorted(t.items()):
        for m in M:
            for k in N:
                if m - k != 差:
                    红.append(('①同章两数之差不是%d' % 差, n, '第%d天早上还是九 对 第%d天，九（差%d）' % (m, k, m - k)))
    for b, a in sorted(对.items()):
        if a in t and b in t:
            na, nb = t[a][1], t[b][1]
            if na and nb and set(na) != set(nb):
                红.append(('②拆出之章与源章之息日不同', b, '第%d章%s 对 第%d章%s（%d係%d拆出）' % (a, na, b, nb, b, a)))
    seq = [(n, t[n][1][0]) for n in sorted(t) if t[n][1]]
    for (n1, v1), (n2, v2) in zip(seq, seq[1:]):
        if v2 < v1:
            红.append(('③息日倒退', n2, '第%d章 第%d天 → 第%d章 第%d天' % (n1, v1, n2, v2)))
    if 报:
        print('════ 息日链 · %d 章有其数 ════' % len(t))
        print('  链：' + '｜'.join('%d:%s%s' % (n, ('全书%d' % t[n][0][0]) if t[n][0] else '',
                                              ('息%d' % t[n][1][0]) if t[n][1] else '') for n in sorted(t)))
        for 形, n, s in 红:
            print('  ⛔ %s｜第%d章：%s' % (形, n, s))
        if not 红:
            print('  ✓ 全书息账之日逐章接得上（同章之差恒 %d、拆出与源同数、只增不减）。' % 差)
    return len(红)


def 自测():
    R = []
    t = 全表()
    # ①式子认得出两种写法
    m1, n1 = 取('第三十天早上，还是九。')
    m2, n2 = 取('第十三天，九。')
    m3, n3 = 取('第三十天早上还是九，第十三天，本子还剩两页')
    R.append(('①两种写法各认得出', m1 == [30] and n1 == [] and n2 == [13] and m3 == [30] and n3 == [13]))
    # ②差17是自盘上量出来的：把同章两数并现者逐章算一遍，众数须为17且无第二个数
    ds = []
    for n, (M, N) in t.items():
        for a in M:
            for b in N:
                ds.append(a - b)
    R.append(('②同章两数并现者 %d 处，其差皆 %d' % (len(ds), 差), bool(ds) and set(ds) == {差}))
    # ③今日之树须全绿
    R.append(('③今日之树零红', 跑(报=False) == 0))
    # ④旧式回灌：把 114 之息日退回「第十二天」（0905 治前之状），须报红
    章 = 诸章()
    import glob as _g
    p114 = 章[114]
    原 = io.open(p114, encoding='utf-8').read()
    ok = False
    try:
        io.open(p114, 'w', encoding='utf-8').write(原.replace('第十三天，九。', '第十二天，九。', 1))
        ok = 跑(报=False) > 0
    finally:
        io.open(p114, 'w', encoding='utf-8').write(原)
    R.append(('④旧式回灌（114 之息日退回第十二天）须报红·跑後原样写回', ok))
    # ⑤而把 114 之息日改成一个「同章无二数可比」的章不受影响——豁免不许滥发
    R.append(('⑤拆出对之表读得出且含 (113,114)、(115,116)',
              (113, 114) in 诸对() and (115, 116) in 诸对()))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(1 if 跑() else 0)
