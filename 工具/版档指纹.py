#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""版档指纹（2026-09-17 立·机制体检账 七十八／到期账 MECH-345-版档指纹）——
**拿尺回去量每一个版档，看它与台账自书之「净重」对不对得上。**

★立此器之由：
  `版本/第N章/_台账.json` 每一条版记里自书一份 `soft.净重`，
  而 `版本/第N章/vNN.md` 就在它旁边躺着——**全书没有一道器把这两样对过一次。**
  与 `工具/净重对表.py` 同族（那一道量的是施工表锁定行，这一道量的是版档自己），
  ★其分在此：**施工表那个数是人手写的，这个数是器当场算的**——
  **器算的数与器存的档对不上，其事更重。**

★★今日之实（0917 亲跑，全书）：
  · 版档 **4,150**｜台账有记而无档者 45｜**净重不符 25**。
  · ⛔**其 4,125 处逐字相符**——★这一条要紧：**它证本器之尺与 `score()` 之尺是同一把。**
    （⛔若尺不同，错的会是四千处，不是二十五处。**先证尺同，再报不符**，否则报的是自己的错。）

★★★⛔**本器只报不拦，其由逐条写明**（`净重对表.py` 之语：**判不死的就别做成闸**）：
  `跑轮.py::save()`（旧副本 十轮精进.py 1027 汰）之形係 `hard, soft = score(txt)` 而後 `open(vNN.md).write(txt)`——
  **两样同出一个 `txt`，故存版当场绝不可能不符。**
  ⛔**那么这二十五处是几时分的家，本器今日答不出**，其所以答不出者有二：
    ① **版档之 git 史看不见**：一章诸版档尽在其封版席那一个提交里头一回落地
       （0917 亲验：第326章 v06 与 v07 同出提交 `32e7f16a`），**提交之前改过几回，史上一个字也没有**；
    ② **不知该信哪一样**：档是回退之所据，数是轮记之所据；**改哪一样都是在改一份据。**
  ★**故本器不判真伪、不代补、不代改**，只把二十五处原样摆出来，交 MECH-345-版档指纹 当面裁。
  ⛔**并及一句写给下一个人**：**不许拿「现存二十五处」写进任何一条常令或一道闸之判据**
  （㊸：**一张快照钉进一条常令**）——**那个数今日是二十五，明日不是。本器每回自己去数。**

用法：
    python3 工具/版档指纹.py          # 全书（只报不拦，rc 恒 0）
    python3 工具/版档指纹.py --章 332  # 只看一章
    python3 工具/版档指纹.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记
except Exception:
    pass
import glob, io, json, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 净重(文):
    """★与旧尺（0924 前 `score()['净重']`，含「＊」行；其器 十轮精进.py 1027 汰）同源，一字不改地照抄其两步：
    ①取【本章亮点】以前；②剥头一行章题；③去尽空白後计长。
    ⛔**此函一改，本器所报即非其所存**——改它之前先去改那一头。"""
    正 = 文.split('【本章亮点】')[0]
    身 = re.sub(r'^.*?第.+?章[^\n]*\n', '', 正, count=1, flags=re.S)
    return len(re.sub(r'\s', '', 身))


def 净重_0924(文):
    """★0924 之後 `跑轮.py::score` 之尺（提交 18456932·2026-09-24 13:22 UTC：换场符「＊」不计字，与检察官／净重对表同源）。
    ⛔其根（0926·376 救章席查）：跑轮改尺之日本器未随之改，366 起凡新存之版其「记」皆不含＊行而本器仍含，
      每版差数恰等於该版之＊行数（376 差 9＝9 个＊、375 差 5）——**是两把尺，不是两个数**；相符率遂由 97% 跌破 95%。
    ⛔其治不是放宽：每一条记只认它存下那一天的那一把尺（见 `_尺之日`），不许两尺任取其合者。"""
    正 = 文.split('【本章亮点】')[0]
    身 = re.sub(r'^.*?第.+?章[^\n]*\n', '', 正, count=1, flags=re.S)
    return sum(len(re.sub(r'\s', '', x)) for x in 身.split('\n') if x.strip() != '＊')


def _尺之日(时):
    """台账版记之「时」（MM-DD HH:MM）→ 其所用之尺：'旧'（含＊）／'新'（不含＊）／'两'（改尺当日，时区不明，两尺皆认）。"""
    m = re.match(r'(\d\d)-(\d\d)', 时 or '')
    if not m:
        return '旧'
    md = m.group(1) + m.group(2)
    if md < '0924':
        return '旧'
    if md > '0924':
        return '新'
    return '两'


def 量(章=None, 根路=None):
    """返回 (不符, 相符, 无档)。不符 = [(章号, 版名, 所记, 实算, 说明), ...]。
    ⛔**台账无记净重者不认**（重开之记其 soft 为空）——**不书就不认，不许替它猜一个**。"""
    R = 根路 or 根
    不符, 相符, 无档 = [], 0, []
    for 台 in sorted(glob.glob(os.path.join(R, '版本', '第*章', '_台账.json'))):
        d = json.load(io.open(台, encoding='utf-8'))
        n = d.get('章')
        if 章 is not None and n != 章:
            continue
        目 = os.path.dirname(台)
        for e in d.get('版本', []):
            记 = (e.get('soft') or {}).get('净重')
            if 记 is None:
                continue
            档 = os.path.join(目, e.get('版', '') + '.md')
            if not os.path.exists(档):
                无档.append((n, e.get('版')))
                continue
            _文 = io.open(档, encoding='utf-8').read()
            _尺 = _尺之日(e.get('时'))
            实 = 净重_0924(_文) if _尺 == '新' else 净重(_文)
            if _尺 == '两' and 记 != 实:
                实 = 净重_0924(_文)
            if 记 == 实:
                相符 += 1
            else:
                不符.append((n, e.get('版'), 记, 实, (e.get('说明') or '')[:34]))
    return 不符, 相符, 无档


def 跑(章=None, 报=True):
    不符, 相符, 无档 = 量(章)
    if 报:
        总 = 相符 + len(不符)
        print('════ 版档指纹 · 台账自书之净重 对 版档实算 ════')
        # ⛔0917 当场自正其名：本器只认「书净重」者，故此数非「无档」之全数——
        #   盘上无档者今共 45，其中 42 条根本不书净重（重开之记其 soft 为空），本器不认。
        #   ★两个数不是一件事，名混作一个，即是拿一把尺去量另一样。
        print('  可比版档 %d｜相符 %d｜⛔不符 %d｜书有净重而无其档者 %d'
              % (总, 相符, len(不符), len(无档)))
        if 总:
            print('  ★相符 %d 处係本器之尺与 score() 同之凭——先证尺同，再看不符。'
                  % 相符)
        for n, v, 记, 实, 说 in 不符:
            print('  ⛔ 第%d章 %s：记 %d，实 %d（差 %+d）｜%s'
                  % (n, v, 记, 实, 实 - 记, 说))
        if not 不符:
            print('  ✓ 逐档相符。')
        print('  ── ⛔本器只报不拦（其由见档首）：交 MECH-345-版档指纹 当面裁 ──')
    return 不符


def 自测():
    import shutil, tempfile
    R = []
    不符, 相符, _ = 量()
    # ①②先证尺同——⛔这一条不过，底下所报者一概不算数
    R.append(('①可比版档成千（≥3000）', 相符 + len(不符) >= 3000))
    R.append(('②相符者压倒多数（≥95%）＝本器之尺与 score() 同',
              相符 >= 0.95 * (相符 + len(不符))))
    # ③净重之式与旧尺（0924 前之 score，含「＊」行）之定数逐档对——⛔不许只凭眼看两段码像
    #   ★1027：旧尺之器（十轮精进.py，跑轮之旧副本）汰；其十二档之数於汰前以 十轮精进.score 亲跑而钉於此（与本器之数逐档同）
    样 = {'版本/第300章/v01.md': 2273, '版本/第300章/v02.md': 2263, '版本/第300章/v03.md': 2422,
         '版本/第300章/v04.md': 2414, '版本/第300章/v05.md': 2483, '版本/第300章/v06.md': 2487,
         '版本/第300章/v07.md': 2484, '版本/第300章/v08.md': 2481, '版本/第300章/v09.md': 2481,
         '版本/第301章/v01.md': 2516, '版本/第301章/v02.md': 2516, '版本/第301章/v03.md': 2520}
    同 = all(os.path.exists(os.path.join(根, x)) and 净重(io.open(os.path.join(根, x), encoding='utf-8').read()) == v
             for x, v in 样.items())
    R.append(('③与旧尺之定数同（十二档逐档对；其数钉於 十轮精进 汰前）', 同 and len(样) == 12))
    # ④⑤⑥假盘：自造一仓，证它有牙、且不误伤
    tmp = tempfile.mkdtemp(prefix='版档指纹_')
    try:
        d = os.path.join(tmp, '版本', '第7章')
        os.makedirs(d)
        身 = '《镇冢秘术》第七章　假\n' + '一二三四五六七八九十\n' * 3 + '\n【本章亮点】\n①不计\n'
        真 = 净重(身)
        io.open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(身)
        io.open(os.path.join(d, 'v02.md'), 'w', encoding='utf-8').write(身)
        io.open(os.path.join(d, 'v03.md'), 'w', encoding='utf-8').write(身)
        json.dump({'章': 7, '版本': [
            {'版': 'v01', '说明': '合', 'soft': {'净重': 真}},
            {'版': 'v02', '说明': '坏', 'soft': {'净重': 真 + 9}},
            {'版': 'v03', '说明': '重开·无记', 'soft': {}},
            {'版': 'v09', '说明': '无档', 'soft': {'净重': 真}},
        ]}, io.open(os.path.join(tmp, '版本', '第7章', '_台账.json'), 'w', encoding='utf-8'),
            ensure_ascii=False)
        f, g, h = 量(根路=tmp)
        R.append(('④把一版之数改坏，逮得出（且只逮那一版）',
                  len(f) == 1 and f[0][1] == 'v02' and f[0][2] == 真 + 9))
        R.append(('⑤数对者不误伤（v01 判合）', g == 1))
        R.append(('⑥无记净重之重开记不认／有记而无档者另计',
                  h == [(7, 'v09')] and all(x[1] != 'v03' for x in f)))
        # ⑦⛔【本器之要害】亮点段之字不许算进净重——否则它量的是另一样
        胖 = 身 + '②' + '甲乙丙丁' * 50 + '\n'
        io.open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(胖)
        f2, _, _ = 量(根路=tmp)
        R.append(('⑦亮点段加二百字，净重不动（v01 仍判合）',
                  all(x[1] != 'v01' for x in f2)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ⑧⛔㊸之守：本器不许把「今日之数」写死在自己身上
    码 = io.open(os.path.abspath(__file__), encoding='utf-8').read()
    尾 = 码.split('def 自测', 1)[0]
    R.append(('⑧⛔本器之判据里没有一个写死的章号／版名（㊸）',
              not re.search(r"[（('\"]第?3[0-9]{2}章?['\")）]", 尾.split('"""', 3)[-1])))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    ch = None
    if '--章' in sys.argv:
        ch = int(sys.argv[sys.argv.index('--章') + 1])
    跑(ch)
    sys.exit(0)   # ⛔只报不拦
