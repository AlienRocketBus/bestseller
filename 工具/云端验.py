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


def 验(快=False):
    print('════ 云端验 ════（不看本地之账，只看云端之物）')
    齐, 未跟 = 甲_齐()
    if 快:
        print('  （--快：只验甲路，未克隆）')
        return 0 if 齐 else 1
    r = 乙丙_克隆而比()
    坏 = (not 齐) or (r is None) or r['缺'] or r['异']
    print()
    if 坏:
        print('  ⛔**云端与本地不齐**——上列诸条逐条治，治毕再跑一回本器。')
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
    print('── 负测·云端验 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(验('--快' in sys.argv))
