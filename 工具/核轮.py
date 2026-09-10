#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核轮（2026-08-16 立）

★而其立之由：作者令「我会连发好几条『跑』，怕漏跑」——
★★而漏跑之实已见二回：200跑到第5轮停（章界闸偶然逮住），201跑到第1轮停（无一闸响）。
★★★故立此工具：一句话逐章点名，一眼看出哪一章跑到一半停了。

用法：
    python3 工具/核轮.py           # 逐章报（末十章）
    python3 工具/核轮.py --全       # 全书逐章报
    python3 工具/核轮.py --静       # 只报未竟之章（供全测调用）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, re, os, glob

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
SET_DIR = os.path.join(ROOT, '设定')
_SET = os.listdir(SET_DIR) if os.path.isdir(SET_DIR) else []


def row(c):
    d = os.path.join(ROOT, '版本', '第%d章' % c)
    rs = set()
    lj = os.path.join(d, '_轮记.md')
    if os.path.exists(lj):
        rs = set(int(x) for x in re.findall(
            r'## 第(\d+)轮', open(lj, encoding='utf-8', errors='replace').read()))
    e11 = os.path.exists(os.path.join(d, '_十一轮.json'))
    hz = [f for f in _SET if '第%d章' % c in f and '回执' in f]
    kj = os.path.exists(os.path.join(d, '_开镜卡.md'))
    b = open(F[c], encoding='utf-8').read().split('【本章亮点')[0]
    return {'章': c, '轮': sorted(rs), '十一轮': e11, '回执': bool(hz),
            '开镜卡': kj, '净重': len(re.sub(r'\s', '', b))}


def judge(r, is_last):
    """★判其状：封版／在跑／★★未竟（跑到一半停了）。"""
    n = len(r['轮'])
    if r['十一轮'] and r['回执']:
        return '✓封版', True
    if n == 0:
        return '—未起轮', True
    if n >= 10:
        # 【第102批·修】原作 `not is_last`，其义反了：
        #   ★核轮立法之由是「防跑到一半跳去写下一章」——而跳去写下一章之凭据，
        #     正是「它已不是末章而余轮未跑」；★★故末章十轮满乃正常在跑，不该拦。
        #   ★★★而原式令末章一到十轮满即判未竟，遂在十三轮制下每章必红三轮
        #     （第11、12、13轮期间）。★★★★负测：219末章十轮满须过、218非末章十轮满须拦。
        return '⚠十轮满·待十一轮', is_last
    if not is_last:
        return '⛔未竟（跑到一半停了）', False
    return '·在跑（第%d轮）' % max(r['轮']), True


def run(chs, quiet=False):
    mx = max(F) if F else 0
    bad, rows = [], []
    for c in chs:
        if c not in F:
            continue
        r = row(c)
        st, ok = judge(r, c == mx)
        rows.append((r, st))
        if not ok:
            bad.append('第%d章 %s（有记之轮 %s）' % (c, st, r['轮']))
    if quiet:
        print('核轮通过' if not bad else '；'.join(bad))
        return 0 if not bad else 2
    print('=' * 74)
    print('  核轮 · 逐章点名（★而其立之由：防连发多条时漏跑）')
    print('=' * 74)
    for r, st in rows:
        print('  %3d 轮%2d %-16s｜十一轮 %s｜回执 %s｜开镜卡 %s｜净重 %d  %s'
              % (r['章'], len(r['轮']), str(r['轮'])[:16],
                 '✓' if r['十一轮'] else '⛔',
                 '✓' if r['回执'] else '⛔',
                 '✓' if r['开镜卡'] else '—',
                 r['净重'], st))
    print('=' * 74)
    if bad:
        print('  ⛔ 未竟之章 %d 处：' % len(bad))
        for x in bad:
            print('     %s' % x)
        print('  ★而其治：回头把那一章之余轮跑完，再往下写。')
    else:
        print('  ✓ 无未竟之章。')
    print('=' * 74)
    return 0 if not bad else 2


if __name__ == '__main__':
    q = '--静' in sys.argv
    cs = sorted(F)
    if '--全' not in sys.argv:
        cs = cs[-10:]
    sys.exit(run(cs, q))
