# -*- coding: utf-8 -*-
"""预检.py —— 拟改之文，落盘之前先问器。

其立法之由（2026-08-27·第286章第6轮）：
    上一坐拟了四段长气之文令我照落；实测四段全部踩五逗硬闸（逗9／5／7／6）。
    若照落，存版当场转红。
    ★而其病不在那四段，在「拟」与「落」之间没有一道闸。

其判据不自造，直接调 工具/跑轮.py 之 score()——单一真源，它改一处此处即随。

用法：
    # 一·单段预检（把这一段当正文看）
    python3 工具/预检.py --文 "今天再煨一罐，同一只罐，……"
    python3 工具/预检.py --档 /tmp/拟稿.txt

    # 二·模拟代换（最有用：改了之后全章之数会怎样）
    python3 工具/预检.py --代 286 --旧 "原文原样" --新 "拟改之文"
    python3 工具/预检.py --代 286 --旧档 /tmp/旧.txt --新档 /tmp/新.txt

    # 三·棘轮复算（存版报回退时跑它，不许凭印象认或驳）
    python3 工具/预检.py --棘轮 286 --项 四字串三现
"""
import argparse
import io
import os
import re
import sys
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _跑轮():
    sp = _u.spec_from_file_location('_pl', os.path.join(ROOT, '工具', '跑轮.py'))
    m = _u.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _读(路径):
    return io.open(路径, encoding='utf-8').read()


def _印硬(hard, 题='硬项'):
    坏 = [(k, v) for k, v in hard.items() if v]
    print('  ── %s ──' % 题)
    if not 坏:
        print('     ✓ 全零')
        return True
    for k, v in 坏:
        print('     ⛔ %s ×%d' % (k, v))
    return False


def _指五逗(文):
    """五逗踩闸时，指出是哪一句、几个逗，并给治法。"""
    句 = [s for s in re.split(r'(?<=[。！？…])', 文) if s.strip()]
    坏 = [s for s in 句 if s.count('，') >= 5]
    if not 坏:
        return
    print('  ── 五逗之详（器之判据：一句之内全角逗 ≥5；而句只按 。！？… 切，分号不断句）──')
    for s in 坏:
        print('     逗%d ⛔ %s' % (s.count('，'), s.strip()[:56]))
    print('     ★治法：长拍是段长挣来的，不是句长挣来的——**并段不并句**。')
    print('     ★★把分号断成句号，每句逗号压到 ≤4，段仍是一段，最长段不减。')


def 单段(文):
    m = _跑轮()
    # 造一份最小可评之稿：器要「第N章」那一行才切得出 body
    假 = '《镇冢秘术》\n\n第九百九十九章　预检\n\n' + 文 + '\n'
    hard, soft = m.score(假)
    print('══ 单段预检 ══')
    print('  字数 %d' % len(re.sub(r'\s', '', 文)))
    净 = _印硬(hard)
    if hard.get('五逗句') or hard.get('亮点段五逗'):
        _指五逗(文)
    print('  ── 软项 ──')
    for k in ('净重', '段数', '最长段', '长段数'):
        if k in soft:
            print('     %s %s' % (k, soft[k]))
    return 0 if 净 else 1


def 代换(n, 旧, 新):
    m = _跑轮()
    路 = m.find_chapter(n)
    if not 路:
        print('⛔ 第%d章正文不在' % n)
        return 2
    原 = _读(路)
    c = 原.count(旧)
    if c != 1:
        print('⛔ 锚不唯一：旧文在第%d章出现 %d 次（须恰 1 次）' % (n, c))
        if c == 0:
            print('   ★而这正是「凭记忆落刀」之险：所拟之旧文，原场里没有。')
        return 2
    后 = 原.replace(旧, 新)
    h0, s0 = m.score(原)
    h1, s1 = m.score(后)
    print('══ 模拟代换 · 第%d章 ══' % n)
    print('  旧 %d 字 → 新 %d 字（净 %+d）'
          % (len(re.sub(r'\s', '', 旧)), len(re.sub(r'\s', '', 新)),
             len(re.sub(r'\s', '', 新)) - len(re.sub(r'\s', '', 旧))))
    print()
    print('  ── 硬项（改前 → 改后）──')
    坏 = False
    for k in h1:
        a, b = h0.get(k, 0), h1[k]
        if a or b:
            旗 = '⛔新踩' if b > a == 0 else ('⚠升' if b > a else '✓降' if b < a else '＝')
            print('     %-10s %d → %d  %s' % (k, a, b, 旗))
            if b:
                坏 = True
    if not 坏:
        print('     ✓ 改前改后皆全零')
    if h1.get('五逗句', 0) > h0.get('五逗句', 0):
        _指五逗(新)
    print()
    print('  ── 软项（改前 → 改后）──')
    for k in ('净重', '段数', '均段', '最长段', '长段数', '四字串三现'):
        if k in s1:
            a, b = s0.get(k, 0), s1[k]
            print('     %-10s %s → %s  (%+d)' % (k, a, b, b - a))
    print()
    if 坏:
        print('  【定论】⛔ 此改踩硬闸，不许落盘。先改其法，不改其料。')
        return 1
    print('  【定论】✓ 此改硬项全零，可落盘。落毕仍须以 一坐.py 复核。')
    return 0


def 棘轮(n, 项):
    """存版报某软项回退时，逐版复算，以数裁之。

    ★其立法之由（286第6轮）：存版报「四字串三现 15→23（升）」。
      直接认则改回，直接驳则是自我安慰。
      逐版复算方知：它随净重长，而本轮净重+90 而零增。
    """
    import glob
    m = _跑轮()
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    档 = sorted(glob.glob(os.path.join(d, 'v*.md')))
    if not 档:
        print('⛔ 第%d章无版本档' % n)
        return 2
    print('══ 棘轮复算 · 第%d章 · 「%s」══' % (n, 项))
    print()
    print('  %-6s %10s %10s %8s' % ('版', 项, '净重', '每千字'))
    行 = []
    for f in 档:
        h, s = m.score(_读(f))
        v = s.get(项, h.get(项))
        净 = s.get('净重', 0)
        if v is None:
            print('⛔ 无此项：%s。可选：%s' % (项, '／'.join(list(s) + list(h))))
            return 2
        行.append((os.path.basename(f)[:-3], v, 净))
        print('  %-6s %10s %10s %8.1f'
              % (行[-1][0], v, 净, (v * 1000.0 / 净) if 净 else 0))
    print()
    最优 = min(x[1] for x in 行)
    首, 末 = 行[0], 行[-1]
    print('  ── 裁 ──')
    print('     历史最优 %s（出於 %s，彼时净重 %d）'
          % (最优, [x[0] for x in 行 if x[1] == 最优][0],
             [x[2] for x in 行 if x[1] == 最优][0]))
    print('     末版 %s（净重 %d）' % (末[1], 末[2]))
    if len(行) >= 2:
        前 = 行[-2]
        d项, d净 = 末[1] - 前[1], 末[2] - 前[2]
        print('     本轮 %s%d ｜ 净重 %s%d' % ('+' if d项 >= 0 else '', d项,
                                              '+' if d净 >= 0 else '', d净))
        if d项 <= 0 < d净:
            print('     ✓ 本轮净重涨而此项未涨——判「长而不复」，回退非本轮所致。')
        elif d项 > 0 and d净 > 0 and (d项 * 1000.0 / d净) < (末[1] * 1000.0 / 末[2]):
            print('     ⚠ 本轮此项涨得比全章密度慢——多半随净重长，须看其条目再裁。')
        elif d项 > 0:
            print('     ⛔ 本轮此项涨而净重未涨（或涨得更快）——回退恐为本轮所致，须逐条查。')
    print()
    print('  ★裁毕须写进轮记：认它／驳它／留后轮复核，三者必居其一，并附此表。')
    return 0


def main():
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument('--文')
    p.add_argument('--档')
    p.add_argument('--代', type=int)
    p.add_argument('--旧')
    p.add_argument('--新')
    p.add_argument('--旧档')
    p.add_argument('--新档')
    p.add_argument('--棘轮', type=int)
    p.add_argument('--项', default='四字串三现')
    a = p.parse_args()
    if a.棘轮:
        return 棘轮(a.棘轮, a.项)
    if a.代:
        旧 = a.旧 if a.旧 is not None else (_读(a.旧档) if a.旧档 else None)
        新 = a.新 if a.新 is not None else (_读(a.新档) if a.新档 else None)
        if 旧 is None or 新 is None:
            print('⛔ --代 须同时给 --旧/--旧档 与 --新/--新档')
            return 2
        return 代换(a.代, 旧, 新)
    文 = a.文 if a.文 else (_读(a.档) if a.档 else sys.stdin.read())
    if not 文.strip():
        print('⛔ 无文可检')
        return 2
    return 单段(文)


if __name__ == '__main__':
    sys.exit(main())
