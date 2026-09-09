#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""席法——**诸席之 .js 写法闸**：专防本坐在写席时反复踩的那几样。

【其立之由（2026-09-09）】本坐一日之内在同一形上犯了**四回**：
  ①`一章.js` 之 schema 键写成中文 → API 400，**六个席一个也没起来，一个字都没写**；
  ②五庭之提示里把命令用反引号括起来 → 工作流解析当场拒；
  ③第12/13轮必答表之提示，同形；④封版席里 `mk695e@gmail.com` 之反引号，同形。
★**而四回都被拦住了，一次也没混过去**——拦它的是工作流之解析与 API，**不是本仓的任何一道闸**。
★★**其病之形**：提示自己活在反引号里，而写提示的人习惯拿反引号括命令——
  **两层反引号撞在一处，外层当场断掉。**
★★★**而 `node --check` 量不出它**：断掉之後那一段仍是合法的 JS（只是意思全变了）——
  **一把量不出这个病的尺，用了四回还在用，这本身才是要治的那一样。**

【它认哪几样，本书同类共几样（令§六④）】
  认 `工具/席/*.js` **全部**（今 6 样，判据之源律：当场 glob，不写死）。两路：
  甲·**schema 键须 ASCII**：API 之 `input_schema.properties` 只收 `^[a-zA-Z0-9_.-]{1,64}$`。
  乙·**模板串内之反引号须转义**：凡在 `agent(\\`…\\`)` 之模板串里出现未转义之 `` ` ``，即红。

【其限（§一⑤）】本闸只认这两样；**它不保证一份席跑得起来**，只保证不因这两样跑不起来。

用法：
    python3 工具/席法.py
    python3 工具/席法.py --自测
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _读(p):
    with open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def 查一(t):
    """返 (schema键之红, 反引号之红)。"""
    键红 = [k for k in re.findall(r'([^\s:,{}\'"`]+)\s*:\s*\{\s*type:', t)
            if not re.fullmatch(r'[A-Za-z0-9_.\-]{1,64}', k)]
    # ★立器当日砍掉一路·记此**免下一坐再造它**：初版另有一路「数反引号之奇偶，未闭合即红」，
    #   而它把 `//` 注释里的反引号也数了进去，当场对 `一章.js` 报假红——
    #   **一个会喊狼的核对器比没有更糟**（本仓旧律），故砍。
    # ★★**其限须直说**（§一⑤）：本器只逮「模板串里拿反引号括命令」这一形，
    #   逮不出别的形之反引号相撞；**逮不出的那些，靠工作流解析当场拒**——
    #   而那一道是有效的：本坐今日四回同形，四回皆被它拦下，一次也没混过去。
    引红 = []
    # ★★★2026-09-09 补一形·**它刚让本坐跑废一次，而本器当时印「诸席俱合」——那是一次假绿**：
    #   heredoc 里写 `\\\\``（双转义）落到档上即成「反斜杠＋反引号」，
    #   **JS 读作「一个字面反斜杠」＋「模板串就此结束」**——外层当场断掉，而 node --check 照旧过。
    #   ★其判得死：模板串里出现 `\\\\`` 者，一律红（真要写一个字面反斜杠加反引号，本仓无此需）。
    for m in re.finditer(r'\\\\`', t):
        引红.append('第%d行附近：双转义之 \\\\`（heredoc 写多了一层）——'
                    'JS 读作「字面反斜杠」＋「模板串结束」，外层当场断掉，而 node --check 照旧过'
                    % (t[:m.start()].count('\n') + 1))
    # 另一路·更实：模板串内出现「`cmd`」之形（一对反引号夹着 python3/grep/awk/ls/git）
    for m in re.finditer(r'(?<!\\)`\s*(python3|grep|awk|sed|ls|git|node)\b', t):
        引红.append('第%d行附近：未转义之 `%s …（提示里的命令须写作 \\\\`）'
                    % (t[:m.start()].count('\n') + 1, m.group(1)))
    return 键红, sorted(set(引红))


def 查(印=True):
    fs = sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    红 = []
    for f in fs:
        k, b = 查一(_读(f))
        rp = os.path.relpath(f, ROOT)
        for x in k:
            红.append('甲·%s：schema 键非 ASCII「%s」——API 只收 ^[a-zA-Z0-9_.-]{1,64}$，'
                      '写中文则 400，**诸席一个也起不来**。' % (rp, x))
        for x in b:
            红.append('乙·%s：%s' % (rp, x))
    if 印:
        print('════ 席法 ════（认 %d 份席·两路：schema键须ASCII／模板串内反引号须转义）' % len(fs))
        for x in 红:
            print('  ⛔ ' + x)
        print('  ✓ 诸席俱合。' if not 红 else '  ⛔ %d 处。' % len(红))
    return 红


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    T('①今局诸席俱合', not 查(印=False), '；'.join(查(印=False))[:120])
    # ②旧局回灌·甲：中文 schema 键须当场逮出（此係 0909 之真局）
    k, _ = 查一("schema: { properties: { 锁定行: { type: 'string' } } }")
    T('②中文 schema 键照旧判红', k == ['锁定行'], str(k))
    T('②之二 ASCII 键不误伤', 查一("{ lock_row: { type: 'string' } }")[0] == [])
    # ③旧局回灌·乙：提示里未转义之命令反引号须逮出（0909 之真局·四回同形）
    _, b = 查一("const p = `跑一下 `python3 工具/全测.py` 看看`")
    T('③未转义之 `python3 照旧判红', any('python3' in x for x in b), str(b))
    # ★2026-09-09 改此格之样本·记其由：**这个样本自己就是双转义的**（写的是 \\\\`，不是 \\`）——
    #   它本想演示「写对的样子」，写出来的却正是本日新逮的那个病。**改样本，不改判据。**
    T('③之二 已转义者不误伤（单转义 \\`）', 查一("const p = `跑一下 \\`python3 x.py\\` 看看`")[1] == [],
      str(查一("const p = `跑一下 \\`python3 x.py\\` 看看`")[1]))
    # ③之三·**双转义须判红**（0909 新形：它让本坐跑废一次，而本器当时印「诸席俱合」）
    T('③之三 双转义 \\\\` 照旧判红',
      any('双转义' in x for x in 查一("const p = `读 \\\\`档名\\\\` 一遍`")[1]))
    # ④席之全集当场 glob（判据之源律）
    T('④席之全集当场读出（今 %d 份）' % len(glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))),
      len(glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))) >= 4)
    # ⑤本闸逮得出 node --check 逮不出的那一样（其立之由）
    T('⑤本闸之乙路非空判据（认命令词 7 样）', len(re.findall(r'python3\|grep', _读(os.path.join(ROOT, '工具', '席法.py')))) >= 1)
    print('── 负测·席法 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(1 if 查() else 0)
