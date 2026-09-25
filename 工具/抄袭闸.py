# -*- coding: utf-8 -*-
"""抄袭闸——**新写的一章，不许拿前面章节的句子凑成。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「千万不要出现写每一个章节去抄袭之前章节的情况，一旦出现，後果不堪设想。
   起草是最重要的阶段——起草时就要想方设法把这一章写到最好，把住质量关；起草都把不住，後面够呛。」
  ★当场之实：367 起草交出时与前三十章逐字重合 17.4%，直到第8轮连读客才看出（其同线对 363 为 43.5%）；
    363 已封版而 20.7%。全书常例 0.5%—9%。**写到第八轮才看出来的抄，是起草那一关没把住。**

【怎么量】本章白文（去亮点段、去空白与＊）里，凡 ≥10 字之串逐字见於前 30 章白文者，其字计为「重」；
  重字 ÷ 本章字 = 重合率。**人名、地名、口头禅偶合，常例在 9% 以内**。
【判】≥12% 红（⛔起草不许交，须重写——不是改几个字躲过去，是换写法、写新的）；9%—12% 黄；并印重合最长的五串与其出处。

用法：python3 工具/抄袭闸.py N      # 查第 N 章
      python3 工具/抄袭闸.py --档 <草稿路径> N   # 查第 N 章之草稿（未入正文者）
      python3 工具/抄袭闸.py --段 A B # 逐章印 A—B 之率
      python3 工具/抄袭闸.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K, 前, 红, 黄 = 10, 30, 12.0, 9.0


def _章号(名):
    _cn = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', 名)
    if not m:
        return 0
    tot = cur = 0
    for ch in m.group(1):
        if ch in _cn:
            cur = _cn[ch]
        elif ch in '十百千':
            tot += (cur or 1) * {'十': 10, '百': 100, '千': 1000}[ch]; cur = 0
    return tot + cur


def 诸章():
    return {_章号(f): f for f in glob.glob(os.path.join(ROOT, '正文', '镇冢秘术_第*章*.md')) if _章号(f)}


def 白文(p):
    t = open(p, encoding='utf-8').read().split('【本章亮点】')[0]
    return re.sub(r'[\s＊#]', '', t)


def 量(本, 旧们):
    """回 (率%, [(串, 出处章)…最长五])"""
    源 = {}
    for n, t in 旧们:
        for i in range(len(t) - K + 1):
            源.setdefault(t[i:i + K], n)
    盖 = [0] * len(本)
    for i in range(len(本) - K + 1):
        if 本[i:i + K] in 源:
            for j in range(i, i + K):
                盖[j] = 1
    串们, i = [], 0
    while i < len(本):
        if 盖[i]:
            j = i
            while j < len(本) and 盖[j]:
                j += 1
            s = 本[i:j]
            串们.append((s, 源.get(s[:K], '?')))
            i = j
        else:
            i += 1
    串们.sort(key=lambda x: -len(x[0]))
    return (100.0 * sum(盖) / max(1, len(本))), 串们[:5]


def 查(N, 印=True, 档=None):
    章 = 诸章()
    if 档 is None and N not in 章:
        print('⛔抄袭闸：第%d章之档不在' % N); return False, 0
    旧们 = [(m, 白文(章[m])) for m in range(max(1, N - 前), N) if m in 章]
    率, 串们 = 量(白文(档 or 章[N]), 旧们)
    if 印:
        print('════ 抄袭闸 ════ 第%d章与前%d章逐字重合（≥%d字之串）：%.1f%%（红线 %.0f%%·常例 0.5—9%%）'
              % (N, len(旧们), K, 率, 红))
        for s, n in 串们:
            print('  · 第%s章已有：「%s」（%d字）' % (n, s[:40] + ('…' if len(s) > 40 else ''), len(s)))
        if 率 >= 红:
            print('  ⛔ 抄袭闸：第%d章重合 %.1f%%——⛔起草不许交；须重写那几段（换写法、写新的），不是改几个字躲过去。' % (N, 率))
        elif 率 >= 黄:
            print('  ⚠ 抄袭闸（黄）：%.1f%%，已近红线——上列诸串逐条看，是不是照抄。' % 率)
        else:
            print('  ✓ 抄袭闸：未见照抄。')
    return 率 < 红, 率


def 自测():
    t = [
        ('①全抄即 100%', abs(量('甲乙丙丁戊己庚辛壬癸子丑', [(1, '甲乙丙丁戊己庚辛壬癸子丑')])[0] - 100) < 0.01),
        ('②全新即 0%', 量('甲乙丙丁戊己庚辛壬癸', [(1, '子丑寅卯辰巳午未申酉')])[0] == 0),
        ('③九字之合不计（人名口头禅之偶合）', 量('甲乙丙丁戊己庚辛壬X', [(1, '甲乙丙丁戊己庚辛壬Y')])[0] == 0),
        ('④亮点段不算白文', '【本章亮点】' in open(__file__, encoding='utf-8').read()),
        ('⑤红线 12%', 红 == 12.0),
    ]
    for n, v in t:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    坏 = [n for n, v in t if not v]
    print('负测·抄袭闸 %d/%d' % (len(t) - len(坏), len(t)))
    return not 坏


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--段' in a:
        i = a.index('--段'); A, B = int(a[i + 1]), int(a[i + 2])
        for n in range(A, B + 1):
            ok, r = 查(n, 印=False)
            print('  %s 第%d章 %.1f%%' % ('⛔' if not ok else ('⚠' if r >= 黄 else '✓'), n, r))
        sys.exit(0)
    if '--档' in a:   # 查草稿：python3 工具/抄袭闸.py --档 <路径> N（起草三稿用）
        i = a.index('--档')
        sys.exit(0 if 查(int(a[i + 2]), 档=a[i + 1])[0] else 1)
    sys.exit(0 if 查(int(a[0]))[0] else 1)
