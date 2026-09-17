#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""硬条哨（2026-09-17 立）——**一条写在纸上的硬条，到期有没有人回话？**

★**立此器之由（⛔本坐今日自己造出来的那个洞）**：
  **本坐 0917 立 `设定/硬条_345_暗线日课之破.md`，其中三条硬条、四条器上之验**，
  **并在档里写了一句「须抄进 `版本/第345章/_开镜卡.md`，⛔不许只挂在本档上」**——
  ⛔**而「须抄进」这四个字，盘上没有一样东西在量它。**
  ★★**即：本坐立的那一条，与本仓记过三回的那一族同病**
  （`体检账 七十二`／`七十三`：**法与码都在，而两者之间没有一条路把法送到干活的人手里**）；
  ⛔**一条没有送到手里的法，与一条不存在的法，在盘上一模一样，分别只在它还会被拿来罚人。**

★★★**其所守者一句**：
  **凡盘上有 `设定/硬条_N_*.md`，而第N章已有正文者，
  其回执或轮记须逐条回话**——**每一条须见其号，且须带「过／未过／驳」三者之一。**

⛔**其所不守者，写明免人误信**：
  · ⛔**本器不判那一条硬条办成没办成**（那要读正文，机器判不了·㊓）；
  · ⛔**本器只判「有没有人回过话」**——**与 `FS沉默闸` 之「不必兑付，只须回话」同法**。
  ★**其由**：**「回话」写得出来才写得出**；**悄悄滑过去的那一条，没有人写过那三个字。**

★★★★**其号之形**：**硬条档里形如「### ⛔**其一·…**」「其二」「其三」者，即一条**；
  **回话之形**：**回执或轮记里须有一行同时带其号（一／二／三…）与「过／未过／驳」之一**，
  ⛔**且须带『硬条』二字**，免把别处一句「其二……未过」误认作回话。

用法：
    python3 工具/硬条哨.py            # 全盘
    python3 工具/硬条哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob, io, os, re, shutil, sys, tempfile

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_号式 = re.compile(r'###[^\n]*?其([一二三四五六七八九十]+)[·、]')
_答式 = ('过', '未过', '驳')


def 诸硬条(盘=None):
    """返回 {章号: (档名, [条之号, ...])}。⛔只认档名形如 `硬条_<数>_*.md` 者。"""
    R = 盘 or 根
    出 = {}
    for f in sorted(glob.glob(os.path.join(R, '设定', '硬条_*.md'))):
        m = re.match(r'硬条_(\d+)_', os.path.basename(f))
        if not m:
            continue
        try:
            s = io.open(f, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        条 = _号式.findall(s)
        if 条:
            出[int(m.group(1))] = (os.path.basename(f), 条)
    return 出


def _有正文(n, 盘=None):
    R = 盘 or 根
    for f in glob.glob(os.path.join(R, '正文', '*.md')):
        if re.search(r'第[零〇一二三四五六七八九十百]+章', os.path.basename(f)):
            pass
    # ★章号之形係中文，故另取一路：拿 `版本/第N章/_台账.json` 在不在判其已起草
    return bool(glob.glob(os.path.join(R, '版本', '第%d章' % n, '_台账.json')))


def _回话之文(n, 盘=None):
    R = 盘 or 根
    出 = []
    for p in (glob.glob(os.path.join(R, '设定', '回执_*第%d章*.md' % n))
              + glob.glob(os.path.join(R, '版本', '第%d章' % n, '_轮记.md'))):
        try:
            出.append(io.open(p, encoding='utf-8', errors='replace').read())
        except OSError:
            pass
    return 出


def 量(盘=None):
    """返回 [(章, 档, 未回话之条), ...]，⛔只取已起草之章。"""
    红 = []
    for n, (档, 条) in sorted(诸硬条(盘).items()):
        if not _有正文(n, 盘):
            continue
        文 = _回话之文(n, 盘)
        缺 = []
        for c in 条:
            答 = False
            for t in 文:
                for ln in t.split('\n'):
                    if '硬条' in ln and ('其' + c) in ln and any(a in ln for a in _答式):
                        答 = True
                        break
                if 答:
                    break
            if not 答:
                缺.append(c)
        if 缺:
            红.append((n, 档, 缺))
    return 红


def 跑(报=True):
    条 = 诸硬条()
    红 = 量()
    if 报:
        print('════ 硬条哨 ════（守：一条写在纸上的硬条，到期须有人回话）')
        print('  盘上硬条档 %d 份｜其条共 %d 条｜已起草之章里未回话者 %d 章'
              % (len(条), sum(len(x[1]) for x in 条.values()), len(红)))
        for n, 档, 缺 in 红:
            print('  ⛔ 第%d章：`%s` 之「其%s」未见回话'
                  % (n, 档, '／其'.join(缺)))
        for n, (档, c) in sorted(条.items()):
            if not _有正文(n):
                print('  · 第%d章未起草，`%s` 之 %d 条候其章（⛔不催）' % (n, 档, len(c)))
        if not 红:
            print('  ✓ 已起草之章里，硬条逐条有人回过话。')
        print('  ⛔**本器只判「回没回话」，不判那一条办成没办成**——'
              '**後者要读正文，机器判不了（㊓）。**')
    return 红


def 自测():
    R = []
    tmp = tempfile.mkdtemp(prefix='硬条哨_')
    try:
        os.makedirs(os.path.join(tmp, '设定'))
        d9 = os.path.join(tmp, '版本', '第900章')
        os.makedirs(d9)
        名 = '硬条_900_' + '试' + '.md'
        io.open(os.path.join(tmp, '设定', 名), 'w', encoding='utf-8').write(
            '### ⛔**其一·甲**\n文\n### ⛔**其二·乙**\n文\n### ⛔**其三·丙**\n文\n')
        # ①⛔章未起草者不催
        R.append(('①章未起草者不催（候其章）', 量(tmp) == []))
        io.open(os.path.join(d9, '_台账.json'), 'w', encoding='utf-8').write('{}')
        # ②⛔已起草而一条也没回话者，三条俱红
        r = 量(tmp)
        R.append(('②已起草而无一条回话者，三条俱红',
                  len(r) == 1 and r[0][2] == ['一', '二', '三']))
        # ③★回执里回一条，即只余二条
        io.open(os.path.join(tmp, '设定', '回执_x_第900章y.md'), 'w',
                encoding='utf-8').write('· 硬条其一：过（其据…）\n')
        r = 量(tmp)
        R.append(('③回一条即只余二条', r and r[0][2] == ['二', '三']))
        # ④★轮记亦算回话之处（不只回执）
        io.open(os.path.join(d9, '_轮记.md'), 'w', encoding='utf-8').write(
            '· 硬条其二：未过（其由…）\n')
        r = 量(tmp)
        R.append(('④轮记亦算回话之处', r and r[0][2] == ['三']))
        # ⑤⛔「过／未过／驳」三者之外不算回话
        io.open(os.path.join(d9, '_轮记.md'), 'a', encoding='utf-8').write(
            '· 硬条其三：容後再看\n')
        r = 量(tmp)
        R.append(('⑤⛔「容後再看」不算回话', r and r[0][2] == ['三']))
        # ⑥★落「驳」亦算回话（⛔本器不要求它必须过）
        io.open(os.path.join(d9, '_轮记.md'), 'a', encoding='utf-8').write(
            '· 硬条其三：驳（其由…）\n')
        R.append(('⑥落「驳」亦算回话（不强求其过）', 量(tmp) == []))
        # ⑦⛔不带「硬条」二字者不算（免把别处一句误认作回话）
        io.open(os.path.join(d9, '_轮记.md'), 'w', encoding='utf-8').write(
            '· 其一：过\n· 其二：过\n· 其三：过\n')
        os.remove(os.path.join(tmp, '设定', '回执_x_第900章y.md'))
        r = 量(tmp)
        R.append(('⑦⛔不带「硬条」二字者不算回话',
                  len(r) == 1 and r[0][2] == ['一', '二', '三']))
        # ⑧⛔档名不合其形者不认
        io.open(os.path.join(tmp, '设定', '硬条_无号.md'), 'w',
                encoding='utf-8').write('### ⛔**其一·甲**\n')
        R.append(('⑧⛔档名无章号者不认', 900 in 诸硬条(tmp) and len(诸硬条(tmp)) == 1))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ⑨★盘上跑得动
    R.append(('⑨盘上跑得动（硬条档 ≥1 份）', len(诸硬条()) >= 1))
    for 名, ok in R:
        print(('  ✓ ' if ok else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    跑()
    sys.exit(0)   # ⛔只报不拦（其拦待接进全测之日再议）
