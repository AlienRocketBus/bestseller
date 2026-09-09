#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""坑账——**三百章踩过的每一个坑，逐个点名：谁在守它。**

【其立之由（2026-09-09 作者令）】
  「我们读完这三百多章遇上过的所有的问题，**都要防止在后续的写作中再次出现**……
   **这个机制必须要立，而且一定要跑起来。**……当然千万不要阻碍剧情的发展，**只是为了防止犯错**。」

★**而查过账，缺口是大的**：`设定/起草令_每章必发.md` 有 **31 个坑**，
  其中写了「哪个器挡得住」者只 **7 条**；`设定/执笔病历本_模式性错误档案.md` 有 **43 个病号（P01—P43）**，
  而 `小说检察官.py` 逐轮专查者只 **P04／P05／P07 三个**。
★★**其余六十来样，靠的是「席读了起草令、记得住」**——**而记得住正是本仓三百章里最不可靠的那一样**
  （P22 断层续手之所以立，就是因为记不住）。

【它认哪几样，本书同类共几样（令§六④）】
  **认全部**：坑之全集当场自 `设定/起草令_每章必发.md` 抽（今 31 条）；
  病之全集当场自 `设定/执笔病历本_模式性错误档案.md` 抽（今 43 条）。
  ★**判据之源律**：两份名单一样也不写在本器里——**令里加一个坑，本器下一次跑就认得它。**

【三路】
  甲·**有器守者**：其条自书「哪个器挡得住：`工具/X.py`」，或全仓某个 `.py` 的码里提到它的号。
  乙·**无器·人判者**：机器判不死（令§十三②不许做成闸）——
     **这一路才是本器的正事**：`--逐章 N` 把它们印成一张单子，**逼案席逐条当面答一遍**。
  丙·**未表态者**：条里既没写谁守、全仓也没有器提它——**这一样最危险：它连「谁管」都没有人想过。**

【它不做什么·写明其限（§一⑤）】
  ★**本器不拦任何一章**（只报不拦）——**作者令：不许阻碍剧情的发展。**
  ★★**它也不判「这一章有没有踩坑」**——那是席读了文才判得出的；
    **它只保证一件事：每一章封版之前，那张「机器逮不到的坑」的单子，被人当面过了一遍。**

用法：
    python3 工具/坑账.py                # 总账：三路各几样
    python3 工具/坑账.py --逐章 306      # 印那张须人答之单（案席用）
    python3 工具/坑账.py --自测
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
令 = '设定/起草令_每章必发.md'
病 = '设定/执笔病历本_模式性错误档案.md'


def _读(p):
    try:
        with open(os.path.join(ROOT, p), encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception:
        return ''


def 诸坑():
    """当场自起草令抽：返 [(号, 题, 守)]。守取其条内「哪个器挡得住：…」一行。"""
    t = _读(令)
    出 = []
    ms = list(re.finditer(r'^(坑[①-⑳㉑-㉟])\s*(.+)$', t, re.M))
    for i, m in enumerate(ms):
        尾 = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        条 = t[m.start():尾]
        g = re.search(r'哪个器挡得住：\s*(.+)', 条)
        出.append((m.group(1), m.group(2).strip()[:46], (g.group(1).strip()[:60] if g else '')))
    return 出


def 诸病():
    """当场自病历本抽：返 [(号, 题)]。"""
    t = _读(病)
    出 = {}
    for m in re.finditer(r'(P\d{2})[^\n]{0,60}', t):
        出.setdefault(m.group(1), m.group(0)[:52])
    return sorted(出.items())


def _器文():
    s = []
    for f in glob.glob(os.path.join(ROOT, '工具', '*.py')) + glob.glob(os.path.join(ROOT, '工具', '席', '*.js')):
        s.append((os.path.basename(f), _读(os.path.relpath(f, ROOT))))
    return s


def 分路():
    器 = _器文()
    甲, 乙, 丙 = [], [], []
    for 号, 题, 守 in 诸坑():
        被引 = [n for n, t in 器 if 号 in t and not n.startswith('负测')]
        if 守.startswith('`工具') or 守.startswith('①有器') or (被引 and '无·人判' not in 守):
            甲.append((号, 题, 守 or ('器：' + '、'.join(被引[:3]))))
        elif '无' in 守 or '人判' in 守:
            乙.append((号, 题, 守))
        else:
            丙.append((号, 题, 守))
    for 号, 题 in 诸病():
        被引 = [n for n, t in 器 if 号 in t and not n.startswith('负测')]
        if 被引:
            甲.append((号, 题, '器：' + '、'.join(被引[:3])))
        else:
            丙.append((号, 题, ''))
    return 甲, 乙, 丙


def 逐章(n):
    甲, 乙, 丙 = 分路()
    单 = 乙 + 丙
    print('████ 坑账·第%d章须人答之单 ████' % n)
    print('  【读法】机器逮得到的，器已在守（%d 样，不列此单）；' % len(甲))
    print('  **下面 %d 样机器逮不到**——本章封版之前，案席须逐条答「本章有没有犯／凭什么说没有」。' % len(单))
    print('  ★答法：一句话，**带实据**（行号／原句／数带量词／grep 之数）。「没犯」二字不算答。')
    print('  ★★**答不出的写「答不出」并写明缺哪一样据**——那是有用的答案；跳过去当没看见是唯一不许做的。')
    print()
    for i, (号, 题, 守) in enumerate(单, 1):
        print('  %2d. %-6s %s' % (i, 号, 题))
    print()
    print('  ★★★**本单只报不拦**（作者令：不许阻碍剧情的发展）——它保的不是「这一章没坑」，')
    print('     是「**那张机器逮不到的单子，被人当面过了一遍**」。')
    return 单


def 总账(印=True):
    甲, 乙, 丙 = 分路()
    if 印:
        print('════ 坑账 ════')
        print('  坑 %d 条（自 %s 当场抽）｜病 %d 号（自 %s 当场抽）' % (len(诸坑()), 令, len(诸病()), 病))
        print('  甲·有器守者 %d 样' % len(甲))
        print('  乙·无器·人判者 %d 样（令§十三②：判不死的不许做成闸——故逐章由人答）' % len(乙))
        print('  丙·**未表态者 %d 样**（既没写谁守，全仓也没有器提它）' % len(丙))
        for 号, 题, _ in 丙[:12]:
            print('   · %-6s %s' % (号, 题))
        if len(丙) > 12:
            print('   · …余 %d 样' % (len(丙) - 12))
        print()
        print('  ★丙路那一批最危险：**它连「谁管」都没有人想过。**')
        print('     其治不是把它们全做成闸（判不死的做成闸，闸终被绕），')
        print('     是**逐样表态**：写进令里「哪个器挡得住」一行——有器写器，无器写「无·人判」。')
        print('     **表了态的才算被防住；没表态的，只是被写下来过。**')
    return 甲, 乙, 丙


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    ks, ps = 诸坑(), 诸病()
    T('①坑之全集当场抽得出（今 %d 条）' % len(ks), len(ks) >= 25, '实 %d' % len(ks))
    T('②病之全集当场抽得出（今 %d 号）' % len(ps), len(ps) >= 30, '实 %d' % len(ps))
    T('③认得出真坑号（㉚在内）', any(k[0] == '坑㉚' for k in ks))
    T('④认得出真病号（P22 断层续手）', any(p[0] == 'P22' for p in ps))
    甲, 乙, 丙 = 分路()
    T('⑤三路之和＝坑数＋病数', len(甲) + len(乙) + len(丙) == len(ks) + len(ps),
      '%d+%d+%d vs %d+%d' % (len(甲), len(乙), len(丙), len(ks), len(ps)))
    T('⑥乙路非空（本书确有判不死之坑）', len(乙) >= 2, '实 %d' % len(乙))
    # ⑦判据之源律：名单不许写死——把令改一个字，抽出来的数须跟着变
    t = _读(令)
    T('⑦名单自令而来（令里「坑」字数 %d 与抽得之数相称）' % t.count('\n坑'), t.count('\n坑') >= len(ks) - 2)
    # ⑧逐章之单跑得动且非空
    import io as _io
    import contextlib as _c
    b = _io.StringIO()
    with _c.redirect_stdout(b):
        单 = 逐章(306)
    T('⑧逐章之单跑得动且非空（今 %d 样）' % len(单), len(单) > 0)
    T('⑨本器只报不拦（无 sys.exit(1) 之路）', 'sys.exit(1)' not in _读('工具/坑账.py').split('def 自测')[0])
    print('── 负测·坑账 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    if '--逐章' in sys.argv:
        i = sys.argv.index('--逐章')
        逐章(int(sys.argv[i + 1]))
    else:
        总账()
