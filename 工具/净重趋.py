# -*- coding: utf-8 -*-
"""净重之趋（2026-09-13 立）——**一章一章看不出来的那一样**。

★**其所以要立**：盘上诸闸皆逐章而问（章型带问「这一章落在哪一带」、
`棘轮预检` 问「这一版比上一版长没长」、`字数闸` 问「N个字数得上数不上」）
——⛔**而它们合起来，看不见「全书在慢慢变薄」这一件事**：
**每一章都只比上一章少一点点，十五章之後就是三成。**

**0913 之实（本器头一回跑，逐段中位，器算非估）**：
　**280—299 中位 2,616** → **300—314 中位 2,289** → **315—327 中位 1,869**。
　**四十七章之间，中位跌了 28.5%。**⛔**而这一路上，没有一章报过红。**

★★**本器只答一问**：**近一段之中位，比上一段跌了几成。**
⛔**它不判该不该**——**一站之末在原地量，本来就该薄**（321—327 七章皆如此，此係段之形不是病）；
**故其报只作 ⚠，并写明「其判须由人当场落，且须落在册上」。**
★★★**而「不判该不该」不等於「随它去」**：**其限一到，须有一行裁**（留·其由／治·其法），
**⛔写不出其由的，就是那一段真的薄了。**
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
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
段长 = 15          # 一段几章
界 = 0.15          # 跌逾几成即报


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


def 净重(路):
    """⛔与 `净重对表.py` 同一式，一字不改（两器之数须对得上）。"""
    t = io.open(路, encoding='utf-8').read().split('【本章亮点】')[0]
    b = re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return len(re.sub(r'\s', '', b))


def 诸章():
    out = {}
    for f in glob.glob(os.path.join(ROOT, '正文', '*第*章_*.md')):
        n = _号(os.path.basename(f))
        if n:
            out[n] = 净重(f)
    return out


def _中(v):
    v = sorted(v)
    return v[len(v) // 2] if v else 0


def 段之中位(d=None, 段长=段长):
    d = d or 诸章()
    ks = sorted(d)
    out = []
    for i in range(len(ks) - 1, -1, -段长):
        块 = ks[max(0, i - 段长 + 1):i + 1]
        if len(块) < 段长 // 2:
            break
        out.append((块[0], 块[-1], _中([d[k] for k in 块])))
    return list(reversed(out))


def 判(d=None):
    """返回诸报。⛔只报「跌逾其界」，不报涨。"""
    段 = 段之中位(d)
    报 = []
    for i in range(1, len(段)):
        a, b = 段[i - 1], 段[i]
        if a[2] and b[2] < a[2] * (1 - 界):
            报.append((a, b, (a[2] - b[2]) / float(a[2])))
    return 段, 报


def 印():
    段, 报 = 判()
    print('════ 净重之趋 ════（每 %d 章一段·跌逾 %d%% 即报）' % (段长, int(界 * 100)))
    for a, b, m in 段:
        print('  · 第%d—%d章　中位 %s' % (a, b, '{:,}'.format(m)))
    if not 报:
        print('  ✓ 无一段比上一段跌逾 %d%%。' % int(界 * 100))
        return 0
    for a, b, r in 报:
        print('  ⚠ 第%d—%d章（中位 %s）比 第%d—%d章（中位 %s）跌 %.1f%%'
              % (b[0], b[1], '{:,}'.format(b[2]), a[0], a[1],
                 '{:,}'.format(a[2]), r * 100))
    print('  ★本器不判该不该——**一站之末在原地量，本来就该薄**；')
    print('  ⛔而其判须由人当场落，且须落在册上（留·其由／治·其法）；')
    print('  ⛔**写不出其由的，就是那一段真的薄了。**')
    return 0


def 自测():
    R = []
    # ①造局：一段 2000、下一段 1000 → 须报，且其数係五成
    d = dict([(i, 2000) for i in range(1, 16)] + [(i, 1000) for i in range(16, 31)])
    段, 报 = 判(d)
    R.append(('①跌五成须报', len(报) == 1 and abs(报[0][2] - 0.5) < 0.01))
    # ②⛔牙·平者不报
    d2 = dict((i, 2000) for i in range(1, 31))
    R.append(('②平者不报', not 判(d2)[1]))
    # ③⛔牙·涨者不报（本器只问薄，不问厚）
    d3 = dict([(i, 1000) for i in range(1, 16)] + [(i, 2000) for i in range(16, 31)])
    R.append(('③涨者不报', not 判(d3)[1]))
    # ④⛔牙·跌一成（未逾界）不报
    d4 = dict([(i, 2000) for i in range(1, 16)] + [(i, 1800) for i in range(16, 31)])
    R.append(('④跌一成未逾界不报', not 判(d4)[1]))
    # ⑤其式须与 净重对表 同（同一章两器同数）
    try:
        import importlib
        对 = importlib.import_module('净重对表')
        f = sorted(glob.glob(os.path.join(ROOT, '正文', '*第*章_*.md')))[0]
        R.append(('⑤与净重对表同式（同章同数）', 净重(f) == 对.净重(f)))
    except Exception as e:
        R.append(('⑤与净重对表同式（%s）' % e, False))
    # ⑥盘上真局：跑得动且段数 ≥3
    段, _ = 判()
    R.append(('⑥盘上跑得动（今 %d 段）' % len(段), len(段) >= 3))
    坏 = [n for n, ok in R if not ok]
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    print('  自测 %d/%d' % (len(R) - len(坏), len(R)))
    return 0 if not 坏 else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 印())
