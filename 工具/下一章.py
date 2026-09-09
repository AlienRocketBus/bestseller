#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""下一章——**任何一次新开的会话，跑这一条就知道该干什么。**

【其立之由（2026-09-08·作者问「完全不需要我操作，可以吗」）】
  可以，但有一个前提：**这本书的进度不许只活在某一次会话的脑子里。**
  会话会被压缩、会断、会重开；**凡只记在上下文里的，断一次就没了**（P22 断层续手）。
  ★故立此器：它只读盘上的东西，印出三样——
    ①下一章是第几章；②它起草之前必须先办的是哪几件；③上一章有没有留下未了之事。
  **一个新会话读完它的印，就能接着写，不必问任何人。**

用法：
    python3 工具/下一章.py          # 印下一章之号与其前置
    python3 工具/下一章.py --自测
"""
import os
import re
import sys
import glob
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_汉 = '零一二三四五六七八九'


def _汉数(n):
    """章号转汉字，与本书档名逐字同。
    ★两处坑，皆立器之日踩过：
      ①**百位之後的十位不许省「一」**：110 是「一百一十」，不是「一百十」——
        本书档名 `第一百一十章_一个记号.md` 为凭；而十位以下（10—19）单独用时才是「十」「十九」。
      ②**四位以上不许硬转**：原式 `_汉[n // 100]` 遇 9999 当场 IndexError。
        本书章数不会过千，故 ≥1000 一律返空串，令 glob 找不着而返 None（明摆着的假章号，不许假装认得）。"""
    if n < 0 or n >= 1000:
        return ''
    if n < 10:
        return _汉[n]
    if n < 20:
        return '十' + (_汉[n % 10] if n % 10 else '')
    if n < 100:
        return _汉[n // 10] + '十' + (_汉[n % 10] if n % 10 else '')
    s = _汉[n // 100] + '百'
    r = n % 100
    if r == 0:
        return s
    if r < 10:
        return s + '零' + _汉[r]
    return s + _汉[r // 10] + '十' + (_汉[r % 10] if r % 10 else '')


def 正文档(n):
    g = glob.glob(os.path.join(ROOT, '正文', '*第%s章_*.md' % _汉数(n)))
    return g[0] if g else None


def 末章():
    """自正文逐章上数，返最末一章之号。"""
    n = 0
    while 正文档(n + 1):
        n += 1
    return n


def 席记全(n):
    p = os.path.join(ROOT, '版本', '第%d章' % n, '_席记.json')
    if not os.path.isfile(p):
        return False, '无 _席记.json'
    try:
        j = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        return False, '读不动：%s' % e
    八段 = ['定位', '三魂', '起草', '机闸', '读席', '修席', '极限', '案席']
    缺 = [x for x in 八段 if x not in (j.get('段') or {})]
    return (not 缺), ('缺段：' + '／'.join(缺) if 缺 else '八段俱全')


def 门槛(n):
    """自 02_余章之势_总纲 与 01_施工表 取本章之硬门槛（逐行原文，不转述）。"""
    出 = []
    for 档, 头 in (('设定/02_余章之势_总纲.md', '总纲'),
                   ('设定/01_镇冢秘术_逐章施工与伏笔回收表.md', '施工表')):
        p = os.path.join(ROOT, 档)
        if not os.path.isfile(p):
            continue
        for i, line in enumerate(open(p, encoding='utf-8'), 1):
            if re.search(r'(?<!\d)%d(?!\d)' % n, line) and ('⛔' in line or '锁定' in line or '限%d' % n in line):
                出.append('%s:%d %s' % (头, i, line.strip()[:180]))
    return 出


def main():
    末 = 末章()
    下 = 末 + 1
    print('════ 下一章 ════')
    print('  已写到：第 %d 章（%s）' % (末, os.path.basename(正文档(末) or '')))
    ok, 语 = 席记全(末)
    print('  末章席记：%s %s' % ('✓' if ok else '⚠', 语))
    print('  ★下一章：**第 %d 章**' % 下)
    print()
    print('  【起草之前必办·照次序】')
    print('   1. python3 工具/起草庭.py %d      —— 四层俱过方许起草' % 下)
    print('   2. python3 工具/囤灰闸.py           —— 该跑的器跑没跑')
    print('   3. Workflow({scriptPath:\'工具/席/一章.js\', args:{章:%d}})' % 下)
    print('      —— 八段八席自走；每一席都会自己去读 设定/起草令_每章必发.md 与 设定/自判之尺.md')
    print()
    ms = 门槛(下)
    if ms:
        print('  【第 %d 章之硬门槛·逐行原文（%d 条）】' % (下, len(ms)))
        for m in ms[:12]:
            print('   · ' + m)
        if len(ms) > 12:
            print('   · …余 %d 条，见 设定/02_余章之势_总纲.md 与施工表' % (len(ms) - 12))
    else:
        print('  ⚠第 %d 章在总纲与施工表里查不着硬门槛——**先把它的位定下来再动笔**。' % 下)
    print()
    print('  ★★凡为了让一个数好看而落的笔，一笔也不许落。交白卷比交一刀假的强。')
    print()
    print('  ════ 常令（2026-09-09 作者令·见 设定/自判之尺.md §〇之前之前）════')
    print('   一·**不停**：一章写完接着下一章，中途撞见的问题就地修，**不为请示而停**。')
    print('   二·遇问题即修，按「让书更好」那一头修；先干活再看闸——')
    print('       活干完闸还红→闸错了，改它并**同日立负测**；活没干就改闸→那是把欠条撕了。')
    print('   三·只有两件事许停下来说：①须作者本人之权限；②本坐判不了而判错会伤书的事')
    print('       （且须先把不依赖它的活全干完再说）。除此一律自己决断、自己落字、自己往下走。')
    return 0


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    T('①汉数转得对 306→三百零六', _汉数(306) == '三百零六', _汉数(306))
    # ★②这一格逐个咬真档名（本书正文档确有这几章），尤其 110＝「一百一十」不是「一百十」
    据 = (('二百七十三', 273), ('三百零五', 305), ('一', 1), ('十', 10), ('二十', 20),
          ('一百一十', 110), ('一百', 100), ('二百', 200))
    错 = [(a, _汉数(b)) for a, b in 据 if _汉数(b) != a]
    T('②汉数逐个咬真章号（含 110＝一百一十）', not 错, str(错))
    T('②之二 千以上返空串而不崩', _汉数(9999) == '' and _汉数(1000) == '')
    T('③正文档()找得着 273 与 1', bool(正文档(273)) and bool(正文档(1)))
    T('④末章 ≥305（活数）', 末章() >= 305, '实为 %d' % 末章())
    T('⑤正文档()对不存在之章返 None', 正文档(9999) is None)
    T('⑥门槛()对 306 取得着（总纲写过它）', len(门槛(306)) > 0, '实取 %d 条' % len(门槛(306)))
    T('⑦门槛()不拿章号当子串（306 不许被 3060 骗）',
      not any('3060' in x and '306' not in x.replace('3060', '') for x in 门槛(306)))
    print('── 负测·下一章 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    sys.exit((0 if 自测() else 1) if '--自测' in sys.argv else main())
