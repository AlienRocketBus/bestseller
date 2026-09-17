# -*- coding: utf-8 -*-
"""逐字重出之趋（2026-09-13 立）——**一章一章看不出来的第二样**。

★**其所以要立**：`看官.py --连读` 逐对报其数，**而它只报眼前这一对**；
⛔**「这一对高不高」与「这一路上它在往哪儿走」是两个问题**，**而後一个从来没有人问过。**

**0913 之实（本器头一回跑·300—327 逐章与其上一同线之章比）**：
　**300—324 二十五章：中位 2.1%，逾 10% 者一章（306·12.7）**
　**→ 325：14.4%｜326：10.0%｜327：24.1%**——**连三章，末一章逾本书中位十倍。**

★★**而这一件事与「日课体」是同一枚硬币的两面**：
**日课原样在役——三章同句正是本书报「这一样没有变」的语法**（327 第8轮十八项逐项裁过，判合十八）；
⛔**而一章之中若四分之一是两章前的原话，读者手上那一本就不是「没有变」，是「没有往下走」。**
★**故本器不判哪一拍该删**（那是逐拍之事，`看官.py --连读` 与轮记已在办）——
**它只答一问：这一路上，那个数在往哪儿走。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
界 = 10.0     # 逾此即报（本书群顶 13.8｜中位 2.1）
最短 = 10     # 逐字重出之最短串（与 看官.py --连读 同）


def _号(f):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', f)
    if not m:
        return None
    d = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
         '六': 6, '七': 7, '八': 8, '九': 9}
    t = n = 0
    for ch in m.group(1):
        if ch in d:
            n = d[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


def 诸章():
    out = {}
    for f in glob.glob(os.path.join(ROOT, '正文', '*第*章_*.md')):
        n = _号(os.path.basename(f))
        if n:
            out[n] = io.open(f, encoding='utf-8', errors='replace').read().split('【本章亮点】')[0]
    return out


def 率(前, 本):
    """★本章之字里，与前一同线之章逐字重出 ≥%d 字者，占几成。""" % 最短
    A = re.sub(r'\s', '', 前)
    拍 = [re.sub(r'\s', '', b) for b in 本.split('＊')]
    tot = rep = 0
    for x in 拍:
        tot += len(x)
        i = 0
        while i < len(x):
            j, best = i + 最短, 0
            while j <= len(x) and x[i:j] in A:
                best = j - i
                j += 1
            if best:
                rep += best
                i += best
            else:
                i += 1
    return 100.0 * rep / tot if tot else 0.0


def 判(d=None, 起=300):
    """返回 (逐章之数, 逾界者)。⛔同线之配对係 n 与 n−2（主暗相间之实）。"""
    d = d or 诸章()
    出 = []
    for n in sorted(d):
        if n >= 起 and (n - 2) in d:
            出.append((n, round(率(d[n - 2], d[n]), 1)))
    return 出, [x for x in 出 if x[1] > 界]


def 印():
    出, 逾 = 判()
    if not 出:
        print('════ 重出之趋 ════ 无可比之章')
        return 0
    v = [x[1] for x in 出]
    # ⛔0917·MECH-341-两把尺 之治：本器之率係**字口径**（分母＝本章之字数），
    #   而 `看官.py::_重出率` 之率係**拍口径**（分母＝本章之拍数）；**两器同名而不同尺**。
    #   ★0917 同一批对上亲量：旧窗（264—296）字 1.69%／拍 2.04%；近段（325—340）字 2.70%／拍 8.47%。
    #   ⛔**故两器之数不可互引、不可共用一条线**——其口径今各自印在头一行上。
    print('════ 重出之趋 ════（逐章与其上一同线之章比·逐字重出 ≥%d 字'
          '〔**字口径·分母＝本章字数**〕·逾 %g%% 即报）'
          % (最短, 界))
    print('  · 可比 %d 章｜中位 %.1f%%｜顶 %.1f%%' % (len(出), statistics.median(v), max(v)))
    print('  · 末十章：%s' % '｜'.join('%d:%.1f' % x for x in 出[-10:]))
    if not 逾:
        print('  ✓ 无一章逾 %g%%。' % 界)
        return 0
    for n, r in 逾:
        print('  ⛔ 第%d章 %.1f%%（中位 %.1f）' % (n, r, statistics.median(v)))
    print('  ★本器不判哪一拍该删（那是逐拍之事，`看官.py --连读` 与轮记已在办）；')
    print('  ⛔它只问一样：**这一章是「没有变」，还是「没有往下走」**——**其裁须落在册上。**')
    return 0


def 自测():
    R = []
    甲 = '＊' + '＊'.join(['她把柴一根一根摆进圈里，掰口朝里' for _ in range(5)])
    乙 = '＊' + '＊'.join(['今天门口空着，她把罐抱到缸边去量了一回' for _ in range(5)])
    R.append(('①全抄者其率近百', 率(甲, 甲) > 90))
    R.append(('②⛔牙·两不相干者近零', 率(甲, 乙) < 5))
    d = {10: 甲, 12: 甲}
    出, 逾 = 判(d, 起=10)
    R.append(('③全抄之章须报', len(逾) == 1 and 逾[0][0] == 12))
    d2 = {10: 甲, 12: 乙}
    R.append(('④⛔牙·不相干者不报', not 判(d2, 起=10)[1]))
    # ⑤⛔牙·只比同线（n−2），不比 n−1
    d3 = {10: 乙, 11: 甲, 12: 甲}
    出3, 逾3 = 判(d3, 起=12)
    R.append(('⑤只比 n−2（今 12 对 10，不对 11）', 出3 and abs(出3[0][1] - 率(乙, 甲)) < 0.05))
    出4, _ = 判()
    R.append(('⑥盘上跑得动（可比 %d 章）' % len(出4), len(出4) > 20))
    坏 = [n for n, ok in R if not ok]
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    print('  自测 %d/%d' % (len(R) - len(坏), len(R)))
    return 0 if not 坏 else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 印())
