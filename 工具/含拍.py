#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""含拍（2026-09-06 立）——一拍整段被紧挨着的另一拍逐字含住：并段之後旧拍没删。

★立此器之由（拿账说，不拿主意说）：
  · 0906 段五 198 之修席落治时报出一条本坐先前没见过的形：
    「85 之全摸长段已逐字含 87／89／91 三拍，係旧段未删」——并附其败因：
    **「凡以新段替旧段者，旧段若被拆成数段，搜头尾六字只逮得着头一段。」**
    即：`邻拍重出` 那一路比的是两拍**互相**有没有重字，而此形是**一拍整个装进另一拍**，
    长的那一段头尾都不同，短的那几拍就那么留在原地。
  · 本坐上盘全书量了一遍：**含拍二十四处、十一章**。而其中最重的一处不在段五，在 **138**——
    138:87 是一段并好的长段，而 138:89—103 **八拍逐字就是它拆开的样子**：
    **同一段话，这一章前後说了两遍，约二百字。**（v01 无此段，v02 起长短两份一起进来，
    历十六版无一版只有一份——**它不是哪一轮改坏的，是那一轮加进来就没删旧的。**）

★★其判（窄而可算）：同一章正文段内，甲拍（剥去标点後 ≥14 字）**整段**逐字见於乙拍之中，
  且两拍相隔 **≤10 拍**者，红。
  ★★之二（0906 当日补·负测①逼出来的）：头一版取 **≤5**，而祖案 138 治前之诸含拍其隔为 **1—7**——
    **此器对它专为之而造的那一案，只逮得着五分之三。**故改取 ≤10。
    改前改後全书之隔谱皆量过：今版只余 **35／83／86** 三处（皆有意之引），
    **8—34 之间全书一处也无**，故 ≤10 既够得着祖案，又离那三处远得很。
    ★★★记此一笔：**一个器造完，必须拿它专为之而造的那一案回灌；那一案只逮着一半，这个器就还没造成。**

★★★它认哪几样，本书同类共几样（令§六④）：
  · **认**：全书含拍 24 处，其中相隔 ≤5 拍者 **N 处**（见 --跑 之印）——即本器所守。
  · **不认（隔得远的那一路，逐条上盘看过，样样是有意的引）**：
    140 拍227⊂拍144（隔 83·长的那一段作「**今天早上我刚说过一句：**……」）；
    236 拍313⊂拍278（隔 35·作「**我说：**……」）；
    247 拍131⊂拍45（隔 86·作「**那七十四页写的是：**……」）。
    **三处皆以一个冒号把话引起来，是引，不是漏删。**
  · **故此器以「隔几拍」分真假**：并段之伤紧挨着（隔 1—7），引旧话隔得远（隔 35 以上），
    中间那一段（隔 8—34）全书一处也无——**这条缝是量出来的，不是划出来的。**

★★★★它红在哪一行（令§十三）：立此器之日，138 已治（原 87 行·约二百字）；
  余者见 --跑 之印，逐处带章号与拍号。

用法：
    python3 工具/含拍.py            # 全书
    python3 工具/含拍.py N          # 只查一章
    python3 工具/含拍.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 亮点对表 import 诸章  # noqa: E402

标 = re.compile(r'[\s★·【】，。、；：？！…—「」『』（）()／/"\'’‘“”0-9a-zA-Z*]')
最短 = 14
隔 = 10


def 剥(s):
    return 标.sub('', s)


def 诸拍(路):
    body = io.open(路, encoding='utf-8').read().split('【本章亮点】')[0]
    return [x.strip() for x in body.split('\n') if x.strip() and x.strip() != '＊']


def 验一章(路):
    拍 = 诸拍(路)
    骨 = [剥(x) for x in 拍]
    出 = []
    for i, a in enumerate(骨):
        if len(a) < 最短:
            continue
        for j, b in enumerate(骨):
            if i == j or len(b) <= len(a) or a not in b:
                continue
            if abs(i - j) <= 隔:
                出.append((i + 1, j + 1, abs(i - j), 拍[i]))
            break
    return 出


def 跑(只=None, 报=True):
    章 = 诸章()
    红 = 0
    远 = 0
    if 报:
        print('════ 含拍 ════')
    for n, p in sorted(章.items()):
        if 只 and n != 只:
            continue
        拍 = 诸拍(p)
        骨 = [剥(x) for x in 拍]
        for i, a in enumerate(骨):
            if len(a) < 最短:
                continue
            for j, b in enumerate(骨):
                if i == j or len(b) <= len(a) or a not in b:
                    continue
                if abs(i - j) <= 隔:
                    红 += 1
                    if 报:
                        print('  ⛔ 第%d章 拍%d 整段见於拍%d（隔%d拍）：%s'
                              % (n, i + 1, j + 1, abs(i - j), 拍[i][:44]))
                else:
                    远 += 1
                break
    if 报:
        print('  ℹ隔 6 拍以上者 %d 处（判为「引」，不作红·其由见此器上方之注）' % 远)
        if not 红:
            print('  ✓ 全书无「并段之後旧拍没删」。')
    return 红


def 自测():
    R = []
    章 = 诸章()
    # ①造一份含拍之料，须逮得出
    拍 = ['一二三四五六七八九十甲乙丙丁戊己', '一二三四五六七八九十甲乙丙丁']
    骨 = [剥(x) for x in 拍]
    R.append(('①短拍整段见於紧邻长拍者逮得出', 骨[1] in 骨[0] and len(骨[1]) >= 最短))
    # ②不足 14 字者不认（免把短句之偶合收进来）
    R.append(('②剥标点後不足14字者不认', len(剥('就一个字。')) < 最短))
    # ③隔得远的那一路不作红——140／236／247 三处须落在「远」那一栏
    远 = 0
    for n in (140, 236, 247):
        拍 = 诸拍(章[n]); 骨 = [剥(x) for x in 拍]
        for i, a in enumerate(骨):
            if len(a) < 最短:
                continue
            for j, b in enumerate(骨):
                if i != j and len(b) > len(a) and a in b:
                    if abs(i - j) > 隔:
                        远 += 1
                    break
    R.append(('③140／236／247 三处引旧话者皆落在「远」栏（得 %d 处）' % 远, 远 >= 3))
    # ④138 已治（其长段不在）
    t = io.open(章[138], encoding='utf-8').read()
    R.append(('④138 之并段已删（0906 落治）',
              t.count('想这一样的时候我脚底下停了半步。停半步以后') == 0))
    # ⑤今日之树
    红 = 跑(报=False)
    R.append(('⑤今日全书红 %d 处' % 红, True))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    a = [x for x in sys.argv[1:] if x.isdigit()]
    sys.exit(1 if 跑(int(a[0]) if a else None) else 0)
