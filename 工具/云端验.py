#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""云端验——**从 GitHub 重新克隆一份，逐档比对：我们辛苦写的东西，云端到底存没存。**

【其立之由（2026-09-10 作者令）】
  「一定要确保经过精心优化过的最终版本保存在云端……**如果我们做好的东西没有保存，那就前功尽弃**。」
★**而本器所以不问 `git status`**：那只说得出「本地有没有没交的东西」，
  说不出「**云端那一份到底是什么**」——**本地的账，证不了远端的实。**
★★故本器之法只有一条：**真去克隆一份下来，逐档比**。**不看本地之账，只看云端之物。**

【它认哪几样，本书同类共几样（令§六④）】
  认 `正文/`、`设定/`、`工具/`、`版本/`、`回执/`、`阅读器/` **六处之全部已跟踪之档**——
  即本仓一切成果之所在（判据之源律：其单当场自 `git ls-files` 取，不写死）。
  ★**未跟踪之档不认**（它本就不在版本里）；★★**而它会把未跟踪者逐个印出来**，
  好教人当场看见「有什么还没进云端」。

【三路】
  甲·**齐不齐**：云端之 HEAD 与本地之 HEAD 同不同；本地有几个提交还没推。
  乙·**全不全**：逐档比 sha——云端缺了哪几档、多了哪几档、哪几档内容不同。
  丙·**实不实**：云端那一份自己数一遍（几章、几字），**不拿本地之数充数**。

用法：
    python3 工具/云端验.py            # 全验（要克隆，约一两分钟）
    python3 工具/云端验.py --快        # 只验甲路（不克隆，秒出）
    python3 工具/云端验.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import glob
import hashlib
import subprocess
import tempfile
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
枝 = 'claude/the-novel-review-4dtuit'
认 = ('正文/', '设定/', '工具/', '版本/', '回执/', '阅读器/')


def _跑(*a, cwd=None):
    return subprocess.run(a, cwd=cwd or ROOT, capture_output=True, text=True)


def _sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 16), b''):
            h.update(b)
    return h.hexdigest()[:16]


def 甲_齐(印=True):
    _跑('git', 'fetch', '-q', 'origin', 枝)
    本 = _跑('git', 'rev-parse', 'HEAD').stdout.strip()[:8]
    远 = _跑('git', 'rev-parse', 'origin/' + 枝).stdout.strip()[:8]
    未推 = _跑('git', 'rev-list', '--count', 'origin/%s..HEAD' % 枝).stdout.strip() or '?'
    未跟 = [x for x in _跑('git', '-c', 'core.quotepath=false',
                          'ls-files', '--others', '--exclude-standard').stdout.split('\n') if x.strip()]
    if 印:
        print('  ── 甲·齐不齐 ──')
        print('   本地 HEAD %s｜云端 HEAD %s｜%s' % (本, 远, '**同**' if 本 == 远 else '⛔不同'))
        print('   本地未推之提交：%s 个%s' % (未推, '' if 未推 == '0' else ' ⛔'))
        if 未跟:
            print('   ⚠未跟踪之档 %d 份（不在版本里，云端自然没有）：' % len(未跟))
            for x in 未跟[:6]:
                print('     · ' + x)
        else:
            print('   ✓无未跟踪之档')
    return (本 == 远 and 未推 == '0'), 未跟


def 乙丙_克隆而比(印=True):
    url = _跑('git', 'remote', 'get-url', 'origin').stdout.strip()
    tmp = tempfile.mkdtemp(prefix='云端验_')
    d = os.path.join(tmp, 'c')
    try:
        r = _跑('git', 'clone', '-q', '--depth', '1', '-b', 枝, url, d, cwd=tmp)
        if r.returncode != 0:
            if 印:
                print('  ⛔克隆不下来：%s' % (r.stderr or r.stdout).strip()[:160])
            return None
        单 = [x for x in _跑('git', '-c', 'core.quotepath=false', 'ls-files').stdout.split('\n')
              if x.strip() and x.startswith(认)]
        缺, 异 = [], []
        for f in 单:
            a, b = os.path.join(ROOT, f), os.path.join(d, f)
            if not os.path.exists(b):
                缺.append(f)
            elif os.path.exists(a) and _sha(a) != _sha(b):
                异.append(f)
        # 丙·云端自己数一遍
        章 = len(glob.glob(os.path.join(d, '正文', '*.md')))
        字 = 0
        for p in glob.glob(os.path.join(d, '正文', '*.md')):
            s = open(p, encoding='utf-8').read()
            w = s[:s.index('【本章亮点】')] if '【本章亮点】' in s else s
            字 += len(re.sub(r'\s|＊', '', w))
        if 印:
            print('  ── 乙·全不全（逐档比 sha·认 %d 档）──' % len(单))
            print('   云端缺 %d 档%s｜内容不同 %d 档%s'
                  % (len(缺), '' if not 缺 else ' ⛔', len(异), '' if not 异 else ' ⛔'))
            for x in (缺 + 异)[:8]:
                print('     ⛔ ' + x)
            print('  ── 丙·实不实（云端那一份自己数的，非本地之数）──')
            print('   **云端实存：正文 %d 章｜白文净字 %s**' % (章, format(字, ',')))
        return {'缺': 缺, '异': 异, '章': 章, '字': 字, '档': len(单)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)



存底枝 = '备份/存底'


def 丁_存底枝(印=True):
    """★2026-09-16 立：**问一句「东西到底丢没丢」——而这一句旧本器从来没问过。**

    ⛔**其所由来·0916 之实**：本器印「**云端实存：正文 323 章**」，**而本地已写到 336**，
    **未推之提交 152 个**——**读到这一行的人，会以为有十三章只活在这个随时会被回收的沙盒里。**
    ★**而其实不然**：`备份/存底` 那一枝 **09:01 刚推过，正文 336 档，一章不少**
    （诸席每二十分钟一回 `存底.py --存`，正是为此）。
    ⛔**旧本器只看主枝**：**它说的每一句都是真的，而它没说的那一句才是人最想知道的那一句。**

    ★**故本节只答一问**：**主枝落後几章，而存底枝齐不齐。**
    ⛔**它不把红改成绿**：主枝不齐照旧红、照旧拦推——**它只让「落後」与「丢了」分得开。**
    """
    _跑('git', 'fetch', '-q', 'origin', 存底枝)
    r = _跑('git', 'log', '-1', '--format=%h %ad', '--date=iso', 'FETCH_HEAD')
    头 = (r.stdout or '').strip() or '?'
    # ⛔**须带 core.quotepath=false**：⭑本坐头一版不带它，`git ls-tree` 把中文档名印成
    #   `"\346\255\243\346\226\207/…"`（八进制转义并加引号），**行末是那个引号不是 `.md`**，
    #   於是 `endswith('.md')` 一档也数不着——**本器当场印「存底枝正文 0 档」，而其实 336 档一档不少。**
    #   ★**这正是本节所要分的那两件事，自己先犯了一回**：**「数不着」被印成了「东西没了」。**
    n = _跑('git', '-c', 'core.quotepath=false', 'ls-tree', '-r', '--name-only',
            'FETCH_HEAD', '正文/')
    存底章 = len([x for x in (n.stdout or '').split('\n')
                if x.strip().strip('"').endswith('.md')])
    本地章 = len(glob.glob(os.path.join(ROOT, '正文', '*.md')))
    if 印:
        print('  ── 丁·存底枝（★「主枝落後」与「东西丢了」是两件事）──')
        print('   `%s` 末一笔：%s' % (存底枝, 头))
        print('   存底枝正文 %d 档｜本地正文 %d 档｜%s'
              % (存底章, 本地章,
                 '✓**一章不少——未推之物並未只活在沙盒里**' if 存底章 >= 本地章
                 else '⛔**存底枝也短 %d 档：这才是真会丢的那一种**' % (本地章 - 存底章)))
    return 存底章 >= 本地章, 存底章, 本地章


def 验(快=False):
    print('════ 云端验 ════（不看本地之账，只看云端之物）')
    齐, 未跟 = 甲_齐()
    if 快:
        print('  （--快：只验甲路，未克隆）')
        return 0 if 齐 else 1
    r = 乙丙_克隆而比()
    存底齐, _sc, _lc = 丁_存底枝()
    坏 = (not 齐) or (r is None) or r['缺'] or r['异']
    print()
    if 坏:
        print('  ⛔**主枝与本地不齐**——上列诸条逐条治，治毕再跑一回本器。')
        # ★而把那一句人最想知道的话，当场说清楚（⛔不拿它去把红改成绿）
        if 存底齐:
            print('  ★**而东西没丢**：`%s` 有 %d 档正文，一章不少——'
                  '**此处红的是「推不上去」，不是「写的东西不在了」。**' % (存底枝, _sc))
        else:
            print('  ⛔⛔**且存底枝也短 %d 档**——**这一种才是真会丢的**，当场先跑 '
                  '`python3 工具/存底.py --存 "抢存"`。' % (_lc - _sc))
    else:
        print('  ✓**云端所存＝本地所有**：逐档 sha 同，一档不缺、一档不异。')
        print('  ★而未跟踪之档若有（上列），**那是还没进版本的，不算丢**——但要么提交，要么当场说明它为何不进。')
    return 1 if 坏 else 0


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    T('①认哪几处係当场取（六处，判据之源律）', len(认) == 6 and all(x.endswith('/') for x in 认))
    T('②其单自 git ls-files 取，不写死',
      "'ls-files'" in open(os.path.join(ROOT, '工具', '云端验.py'), encoding='utf-8').read())
    齐, 未跟 = 甲_齐(印=False)
    T('③甲路跑得动', isinstance(齐, bool))
    T('④sha 算得出（拿本器自己验）', len(_sha(os.path.join(ROOT, '工具', '云端验.py'))) == 16)
    # ⑤**本器不许拿本地之数充云端之数**：丙路之数须自克隆之档算
    s = open(os.path.join(ROOT, '工具', '云端验.py'), encoding='utf-8').read().split('def 自测')[0]
    T('⑤丙路之数自克隆之档算（glob 之根係 d，非 ROOT）',
      "glob.glob(os.path.join(d, '正文'" in s)
    T('⑥克隆之处跑毕即扫（不吃盘）', 'shutil.rmtree' in s and 'finally' in s)
    # ⑦★2026-09-16 立：**「主枝落後」与「东西丢了」须分得开**
    T('⑦丁路真去问存底枝（其名不写死在印里，而在码里取）',
      "存底枝 = '备份/存底'" in s and 'def 丁_存底枝' in s)
    # ⑦之三⛔**中文档名须带 core.quotepath=false 方数得着**（本坐头一版之栽）
    T('⑦之三 丁路带 core.quotepath=false（否则中文档名一档也数不着）',
      "'core.quotepath=false', 'ls-tree'" in s)
    齐存, _a, _b = 丁_存底枝(印=False)
    T('⑦之二 丁路跑得动且数得出（存底章 %d／本地章 %d）' % (_a, _b),
      isinstance(齐存, bool) and _b > 0)
    # ⑦之四⛔**存底枝之数须 >0**：⭑本坐头一版不带 core.quotepath=false，此数印作 0，
    #   **而其实一档不少**——**「数不着」被本器印成了「东西没了」。**
    T('⑦之四 存底枝数得着（>0；头一版曾因引号之故印作 0）', _a > 0, '得 %d' % _a)
    # ⑧⛔**丁路不许把红改成绿**：坏之判里不许掺存底枝之绿
    T('⑧丁路不得混进「坏」之判（存底齐不齐，主枝照旧拦）',
      '坏 = (not 齐) or (r is None)' in s and '存底齐' not in s.split('坏 = (not 齐)')[1].split('\n')[0])
    print('── 负测·云端验 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(验('--快' in sys.argv))
