# -*- coding: utf-8 -*-
"""起手哨 · **连着几章拿日号起手**（2026-09-22 立）

★**其所以立**：`起手账` 自 0919 起逐章转交，其文作「**327—351 连 25 章以日号／天号起手，
  其限 352**」——⛔**而盘上没有一道器在数这个数**：**它是人一章一章抄下来的**，
  **抄错了没有人知道，抄漏了也没有人知道**（`体检账 ㊮`：一条账连着三章靠人手转交，它迟早断）。

★★**立器之日先数，後立限**（⛔不许先定一个好听的数再去找据）：
  **196—354 共 159 章，日起手 143 章（89.9%）**——**这是本书的常式，不是病**；
  **其最长四串：41 章（278—318）｜30 章（218—247）｜25 章（327—351）｜16 章（252—267）。**
★★★**故本器不拦，只报**：**连 18 章以上者当面报出**——
  ⛔**而其价写明**：**照此阈，史上三串皆会报**（41／30／25）；**本器不追旧账，只自 352 起看。**
  **352／353／354 三章已连着三章不以日号起手**（0922 本坐亲跑）——**即那一笔治已落地，本器是替它看着别再回去。**

⛔**本器之「起手」只认白文头一句之句首**：**日词须在句首**（`第一百三十三天。…`），
  **句中之日词不算起手**——**那是别的账（`质量三闸①之c`）在管的事。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
门 = 18
自 = 352                                   # ★只自此章起看（其前係史，不追）
日词 = re.compile(r'^第[一二三四五六七八九十百零]+[天日]')


def _库():
    import importlib.util as u
    s = u.spec_from_file_location('日差哨', os.path.join(ROOT, '工具', '日差哨.py'))
    m = u.module_from_spec(s)
    s.loader.exec_module(m)
    return {r[0]: r[1] for r in m.读库()}   # 读库 之行 (章, 文, …)——420 起添第三格（骨日），只取前二


def 首句(t):
    """★白文头一句——⛔书名行、章名行、分隔之星皆不算。"""
    for l in t.split('\n'):
        l = l.strip()
        if not l or l.startswith('《') or l.startswith('＊') or l.startswith('#'):
            continue
        if re.match(r'^第[一二三四五六七八九十百零]+章', l):
            continue
        return l
    return ''


def 日起手(t):
    return bool(日词.match(首句(t)))


def 诸串(flags):
    """[(长, 起, 止)]——flags 係 [(章, 是不是日起手)]。"""
    out, cur, st, 末 = [], 0, None, None
    for n, b in flags:
        if b:
            cur += 1
            st = st if st is not None else n
            末 = n
        else:
            if cur:
                out.append((cur, st, 末))
            cur, st, 末 = 0, None, None
    if cur:
        out.append((cur, st, 末))
    return out


def 量(库=None):
    库 = _库() if 库 is None else 库
    flags = [(n, 日起手(t)) for n, t in sorted(库.items())]
    return flags, 诸串(flags)


def 报():
    flags, 串 = 量()
    if not flags:
        print('⛔读不着正文')
        return False
    末 = flags[-1][0]
    尾 = [s for s in 串 if s[2] == 末]
    今 = 尾[0][0] if 尾 else 0
    日数 = sum(1 for _, b in flags if b)
    print('════ 起手哨 · 连着几章拿日号起手 ════')
    print('  逐章亲数 %d 章｜日起手 %d 章（%.1f%%）｜**此係本书常式，非病**'
          % (len(flags), 日数, 100.0 * 日数 / len(flags)))
    print('  今之串：**%d 章**（末章第%d章%s）' % (今, 末, '·日起手' if 今 else '·非日起手'))
    犯 = [s for s in 串 if s[0] >= 门 and s[2] >= 自]
    if 犯:
        print('  ⛔ 自第%d章起，连 %d 章以上者 %d 串：%s'
              % (自, 门, len(犯), '、'.join('%d—%d（%d章）' % (a, b, c) for c, a, b in 犯)))
        print('     ★**其治不是硬换一个开头**——**换开头是笔，不是事**；'
              '**须换的是「这一章头一件事是什么」**（0922 之裁：352 之治即如此）。')
        return False
    print('  ✓ 自第%d章起无一串连 %d 章以上。' % (自, 门))
    print('  ℹ其前之史（⛔本器不追）：%s'
          % '、'.join('%d—%d（%d章）' % (a, b, c)
                       for c, a, b in sorted(串, reverse=True)[:3]))
    return True


def 自测():
    R = []
    库 = _库()
    flags, 串 = 量(库)
    d = dict(flags)
    R.append(('①352／353／354 三章俱非日起手（0922 之治·亲跑）',
              all(d.get(n) is False for n in (352, 353, 354) if n in d)))
    R.append(('②351 係日起手（⛔证本器不是一律判否）', d.get(351) is True))
    R.append(('③327—351 那一串数得出，且恰 25 章',
              any(c == 25 and a == 327 and b == 351 for c, a, b in 串)))
    # ④⛔严式之验：**日词须在句首**。
    #   ★先认一件今日之实：**真盘上宽式与严式同数（各 %d 章）**——
    #     **即本书里没有一章之头一句把日词摆在句中**；⛔**故此格不拿真盘作局（拿它等於陪跑）**，
    #     **改造一份局来验那一道界。**
    宽 = re.compile(r'第[一二三四五六七八九十百零]+[天日]')
    严数 = sum(1 for _, b in flags if b)
    宽数 = sum(1 for n, t in 库.items() if 宽.search(首句(t)))
    句中 = '《书》\n\n第九十九章　假\n\n他把手收回来，到第一百三十三天才又伸出去。\n'
    句首 = '《书》\n\n第九十九章　假\n\n第一百三十三天。他把手收回来。\n'
    R.append(('④⛔日词在句中者不算起手（造局·⛔真盘上宽严同数 %d，拿它作局即陪跑）' % 严数,
              日起手(句中) is False and 宽.search(首句(句中)) is not None))
    R.append(('④之二·同一句把日词挪到句首即算起手', 日起手(句首) is True))
    R.append(('④之三·真盘宽严同数一事，逐日会变——故只作注，不作判（宽%d／严%d）'
              % (宽数, 严数), True))
    # ⑤串之算须收末一串（⛔不许漏尾）
    R.append(('⑤诸串之算收得着末一串（⛔不许把结在末章那一串漏掉）',
              诸串([(1, True), (2, True)]) == [(2, 1, 2)]))
    R.append(('⑤之二·中断者分作两串', 诸串([(1, True), (2, False), (3, True)]) == [(1, 1, 1), (1, 3, 3)]))
    R.append(('⑥门之数非凭空：史上三串（41／30／25）皆在门上，今之门 %d' % 门,
              门 < 25))
    R.append(('⑦⛔本器只自第%d章起看（其前係史，不追旧账）' % 自, 自 == 352))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 起手哨·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
