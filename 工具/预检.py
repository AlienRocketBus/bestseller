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
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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


# ★2026-09-05·机制总审·硬闸探伤审第1条（本坐 grep 坐实）：崩坏对照第121条自称「已机化·永禁词表（不知过了多久一类）」，
#   而永禁词表（canon 22 词）里一个时间词也没有；`grep -l` 全书：不知过了多久 7 章／不知多久 7 章／过了很久 5 章（皆第1—107章与200、251）。
#   ★它认哪几样，本书同类共几样：本书同类之词八形——认六形（下表）；**不认「半晌」44章、「良久」6章、「一晃」19章**
#     （三者係句内之顷刻或「一晃七年」之远述，不失日历；认了即喊狼）。★★报而不拦，旧章不追：它是软项，与净重同列。
模糊时距形 = ('不知过了多久', '不知多久', '过了很久', '许多天后', '转眼间', '几天后')


def 模糊时距(文):
    """返回白文里所见之模糊时距词（逐处），供软项印数。"""
    body = 文.split('【本章亮点】')[0]
    out = []
    for w in 模糊时距形:
        out += [w] * body.count(w)
    return out

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
    糊 = 模糊时距(文)
    print('     模糊时距 %d%s' % (len(糊), ('（%s）——★报而不拦：一章之日历在首拍之「第N天」，此词只失一段之内的尺' % '、'.join(sorted(set(糊)))) if 糊 else ''))
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
    # ★★★★★2026-09-02·292第3轮所逮：**这道专为裁棘轮而立的器，其「最优」用的是 min()，不分方向。**
    #   ★而棘轮有三类：`RATCHET_MIN=('四字串三现','顿悟起手')` 愈低愈好；
    #     **`RATCHET_MAX=('嗅','沈鸢')` 与 `RATCHET_V01=('嗅','听','触','视')` 愈高愈好**。
    #   ★★其果：跑 `--棘轮 292 --项 嗅` 得「历史最优 2（出於 v01）」——**而 v01 正是最薄那一版**；
    #     ★★★於是这一行不但没帮上裁，它把裁往反方向推：**照它读，嗅 8 是「高於最优」，本轮反倒该记功。**
    #   ★★★★而它与第二十三犯同族（判据里少了它本该认的那一样：此处少的是「这一项该往哪边走」）；
    #     ★**其群**：本器所裁之项，MIN 二目、MAX 二目、V01 四目——**八目里有六目方向是反的**。
    _MIN = ('四字串三现', '顿悟起手')
    _取 = min if 项 in _MIN else max
    最优 = _取(x[1] for x in 行)
    首, 末 = 行[0], 行[-1]
    print('  ── 裁 ──')
    print('     历史最优 %s（出於 %s，彼时净重 %d）｜此项之向：%s'
          % (最优, [x[0] for x in 行 if x[1] == 最优][0],
             [x[2] for x in 行 if x[1] == 最优][0],
             '愈低愈好（MIN）' if 项 in _MIN else '愈高愈好（MAX／V01）'))
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
    # ★★★★★2026-09-02·292第3轮立·举证块（292第2轮之一疑所索）：
    #   ★其疑：「所删者係抄来的」这个由头，往後每一次删都说得出——**而闸一旦可以由我一句话推翻，它就不是闸了。**
    #   ★★其治不是让器替我推翻（那是挖空闸）：**回灌全书，此判据可免裁者 18/28＝64%，
    #     其中含拆章之版**——**免裁太松。**
    #   ★★★故改作举证：**器只摆凭据，裁仍归人**；**我那一句话由此变成可查之实。**
    #   ★★★★它认哪几样（令§六④）：**末二版之间被删去而不见於新版之句（≥11字），
    #     且逐字见於他章正文者**；★**它认不着的三样**：①改写而非整句删者（刀口劈断之句）；
    #     ②所删见於本章他处者（不算抄他章）；③**「该不该删」本身**——**那一判器不下，人下。**
    _删证 = _棘轮删证(n, 档)
    if _删证:
        print()
        print('  ── 举证·末二版之间所删而逐字见於他章者（器摆凭据，裁仍归人）──')
        for _s, _k in _删证[:6]:
            print('     · 「%s」　见於%s' % (_s[:40], _k))
        if len(_删证) > 6:
            print('     …另 %d 句。' % (len(_删证) - 6))
        print('  ★而此块只答「这一句是不是抄的」，不答「该不该删」——后者仍须人裁。')
    print()
    print('  ★裁毕须写进轮记：认它／驳它／留后轮复核，三者必居其一，并附此表。')
    return 0



def _棘轮删证(n, 档):
    """★末二版之间被删去、且逐字见於他章正文之句（≥11字）。
    ★★292第3轮立：**举证，不免裁**——器摆凭据，裁仍归人（其由见调用处之注）。"""
    import difflib
    import glob as _g
    if len(档) < 2:
        return []
    def _b(fp):
        try:
            return io.open(fp, encoding='utf-8').read().split('【本章亮点')[0]
        except OSError:
            return ''
    o = re.sub(r'[\s＊]', '', _b(档[-2]))
    w = re.sub(r'[\s＊]', '', _b(档[-1]))
    if not o or not w:
        return []
    句 = set()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, o, w, autojunk=False).get_opcodes():
        if tag in ('delete', 'replace'):
            for x in re.split(r'[。！？]', o[max(0, i1 - 30):i2 + 30]):
                if len(x) >= 11 and x in o and x not in w:
                    句.add(x)
    out = []
    for fp in sorted(_g.glob(os.path.join(ROOT, '正文', '*.md'))):
        if ('第%d章' % n) in os.path.basename(fp):
            continue
        t = re.sub(r'\s', '', _b(fp))
        for x in sorted(句):
            if x in t:
                out.append((x, os.path.basename(fp)[5:].split('_')[0]))
                句.discard(x)
    return out


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
