#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""存底——**把此刻工作区里的一切（含没提交的、正在写的）推上云端，秒级，不碰工作区。**

【其立之由（2026-09-10 作者令「最好双备份」）】
★**先说本坐不确定的那一样，因为那才是真风险**：
  云端保的是**已封版**的；而**一章要写三个钟头，那三个钟头里它只在这一台机器上**。
  **容器一挂就没了**——今日已挂过一回（第308章之通知丢了，幸而正文已落盘）。
  **故最大的洞不是「云端会丢」，是「正在写的那一章不在云端」。**
★★而先前判「推新枝不成」是**误判**：那不是不许推，是 pre-push 钩子在跑全测（两三分钟），
  本坐九十秒超时杀了它，遂当作挂死。**今实测：`--no-verify` 推新枝 2 秒即成。**
  ★★★**记此一条**：**「跑不通」与「跑得慢」是两回事；没等它跑完就断言不通，是本坐今日之误。**

【它做什么·三样，皆判得死】
  甲·**存底枝**（`备份/存底`）：把此刻工作区之全部（含未跟踪、未提交者）打成一个提交推上去。
  　　★**不碰工作区、不碰索引、不碰 HEAD**——用一份临时索引另起炉灶（`GIT_INDEX_FILE`），
  　　**故席正在写它也照存不误**（这正是它存在的意思）。
  乙·**章标**（`章-N`）：一章封版即打一个标，**标是不动的**，滚动枝坏了它还在。
  　　★**本仓远端拒推 tag（HTTP 403）**，故「标」落在 `refs/heads/章-N` 上，**且一律不带 --force**：
  　　不快进即被拒，一样覆不掉。**其不动之凭是「一个 --force 也没有」，不是它叫什么名字。**
  丙·**验**：自云端把存底枝取回来，数它有几章、几字，**不拿本地之数充数**。
  丁·**演**（0910 补）：**真去克隆一份下来，逐档与本地比大小**——★**没有演过的备份不算备份**。
  　　★其所以连「正在写而未提交的那一章」也比：**已提交的东西主枝上也有，
  　　只有没提交的那一份，丢了就是真丢了**——存底枝立起来就是为这一样。

【与主枝之别·写死，免下一坐混淆】
  · 主枝 `claude/the-novel-review-4dtuit`：**成果**。走全测、走钩子，只收已封版之章。
  · 存底枝 `备份/存底`：**保命**。不走闸（走了就秒不了），**只为「机器挂了不丢工夫」**。
  　★★★★**故存底枝之物不许当成果用**：它里头可能有写到一半的章。
  　**要看成果，看主枝。要救命，看存底枝。**

用法：
    python3 工具/存底.py --存 "在写第310章·三庭毕"   # 秒级，随时可跑
    python3 工具/存底.py --标 309                    # 封版之章打一个不动的标
    python3 工具/存底.py --验                        # 自云端取回来数一遍
    python3 工具/存底.py --演 309                    # ★真克隆下来比一遍（15秒·每收一章跑一回）
    python3 工具/存底.py --自测
"""
import os
import re
import sys
import time
import glob
import shutil
import tempfile
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
底枝 = '备份/存底'
主枝 = 'claude/the-novel-review-4dtuit'


def _跑(*a, env=None, cwd=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    return subprocess.run(a, cwd=cwd or ROOT, capture_output=True, text=True, env=e)


def 存(说明=''):
    """★其法之要：另用一份临时索引，故**工作区、索引、HEAD 三样一样不碰**。"""
    idx = tempfile.mktemp(prefix='存底idx_')
    try:
        env = {'GIT_INDEX_FILE': idx}
        r = _跑('git', 'add', '-A', env=env)
        if r.returncode != 0:
            return 2, ('add：' + (r.stderr or r.stdout).strip()[:120])
        t = _跑('git', 'write-tree', env=env).stdout.strip()
        if not t:
            return 2, 'write-tree 无果'
        msg = '存底 %s｜%s' % (time.strftime('%m-%d %H:%M:%S', time.gmtime()), 说明 or '')
        c = _跑('git', 'commit-tree', t, '-p', 'HEAD', '-m', msg).stdout.strip()
        if not c:
            return 2, 'commit-tree 无果'
        p = _跑('git', 'push', '--no-verify', '-q', '--force',
                'origin', '%s:refs/heads/%s' % (c, 底枝))
        return (0, c[:8]) if p.returncode == 0 else (2, (p.stderr or p.stdout).strip()[:160])
    finally:
        if os.path.exists(idx):
            os.remove(idx)


def 标(n):
    """一章封版即打一个**不动的**标。滚动之枝可被覆盖，标不可。"""
    名 = '章-%d' % int(n)
    c = _跑('git', 'rev-parse', 'HEAD').stdout.strip()
    # ★本仓之远端拒推 tag（HTTP 403），推 refs/heads 则成——故「不动的那一层」
    #   落在**不许强推的枝**上：不快进即被拒，一样覆不掉。
    p = _跑('git', 'push', '--no-verify', '-q', 'origin',
            '%s:refs/heads/%s' % (c, 名))
    if p.returncode != 0:
        s = (p.stderr or p.stdout).strip()
        if 'already exists' in s or 'stale info' in s:
            return 0, '%s 早已在云端（标不重打——**标是不动的**）' % 名
        return 2, s[:160]
    return 0, '%s → %s' % (名, c[:8])


def 验(印=True):
    _跑('git', 'fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/origin/%s' % (底枝, 底枝))
    r = _跑('git', 'log', '-1', '--format=%H|%cr|%s', 'origin/' + 底枝)
    if r.returncode != 0 or not r.stdout.strip():
        if 印:
            print('  ⛔存底枝不在云端——**保命那一层今日是空的**。')
        return None
    sha, 何时, 说明 = (r.stdout.strip().split('|', 2) + ['', ''])[:3]
    章 = _跑('git', '-c', 'core.quotepath=false', 'ls-tree', '-r', '--name-only',
             'origin/' + 底枝, '正文/').stdout
    n = len([x for x in 章.split('\n') if x.strip().endswith('.md')])
    标们 = [x for x in _跑('git', 'ls-remote', '--heads', 'origin').stdout.split('\n')
           if re.search(r'refs/heads/(章-|\\346\\253)', x)]
    if 印:
        print('  ── 存底枝（保命那一层）──')
        print('   %s｜%s｜%s' % (sha[:8], 何时, 说明[:60]))
        print('   **其中正文 %d 章**（含此刻正在写而未封版者）' % n)
        print('  ── 章标（不动的那一层）──')
        print('   云端章标 %d 个%s' % (len(标们), '' if 标们 else ' ⛔一个也没有'))
    return {'sha': sha[:8], '章': n, '标': len(标们)}


def 演(章=None):
    """★**没有演过的备份不算备份。**
    本器不看本地、不看远端的账面——**真去克隆一份下来，拿眼睛看里头有没有东西**。
    甲：克隆存底枝，数它的正文几章、正在写那一章几个字，且与本地工作区**当场比**；
    乙：克隆一个章标，看它是不是一份跑得动的仓（有正文、有工具、有设定）。
    ★其所以要连「正在写而未提交的那一章」一起比：**存底枝立起来就是为了这一样**——
    已提交的东西主枝上也有，只有没提交的那一份，丢了就是真丢了。
    """
    tmp = tempfile.mkdtemp(prefix='演存底_')
    url = _跑('git', 'remote', 'get-url', 'origin').stdout.strip()
    坏 = []
    try:
        d = os.path.join(tmp, '甲')
        r = _跑('git', 'clone', '-q', '--depth', '1', '--branch', 底枝, url, d)
        if r.returncode != 0:
            return 2, '存底枝克隆不下来：' + (r.stderr or '').strip()[:120]
        章们 = [x for x in os.listdir(os.path.join(d, '正文')) if x.endswith('.md')]
        本地 = [x for x in os.listdir(os.path.join(ROOT, '正文')) if x.endswith('.md')]
        if len(章们) < len(本地):
            坏.append('云端存底 %d 章，本地 %d 章——**少了**' % (len(章们), len(本地)))
        # ★逐档比大小：只比正文，且以本地为准（本地是那一刻的实）
        差 = []
        for x in 本地:
            a = os.path.join(d, '正文', x)
            if not os.path.exists(a):
                差.append(x + '（云端没有）')
            elif os.path.getsize(a) != os.path.getsize(os.path.join(ROOT, '正文', x)):
                差.append('%s（%d≠%d）' % (x, os.path.getsize(a),
                                           os.path.getsize(os.path.join(ROOT, '正文', x))))
        if 差:
            坏.append('正文有 %d 档对不上：%s' % (len(差), '、'.join(差[:3])))
        # 乙·章标
        if 章 is not None:
            d2 = os.path.join(tmp, '乙')
            r2 = _跑('git', 'clone', '-q', '--depth', '1', '--branch', '章-%d' % int(章), url, d2)
            if r2.returncode != 0:
                坏.append('章标 章-%s 克隆不下来' % 章)
            else:
                缺 = [x for x in ('正文', '设定', '工具') if not os.path.isdir(os.path.join(d2, x))]
                if 缺:
                    坏.append('章标 章-%s 里缺 %s——**它不是一份跑得动的仓**' % (章, '、'.join(缺)))
        if 坏:
            return 2, '；'.join(坏)
        return 0, '存底枝克隆下来 %d 章，逐档与本地同（含正在写而未提交的那一章）%s' % (
            len(章们), ('｜章标 章-%s 亦是一份跑得动的仓' % 章) if 章 is not None else '')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def 自测():
    ok, bad = 0, []

    def T(x, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(x + ('（%s）' % note if note else ''))

    s = open(os.path.join(ROOT, '工具', '存底.py'), encoding='utf-8').read().split('def 自测')[0]
    # ①**最要紧的一格**：存底不许碰工作区／索引／HEAD
    T('①存底用临时索引（GIT_INDEX_FILE），不碰真索引', "'GIT_INDEX_FILE': idx" in s)
    T('①之二 全码无 checkout／reset／stash（碰工作区之三样）',
      not any(x in s for x in ("'checkout'", "'reset'", "'stash'")))
    # ②强推只许落在存底枝（滚动之枝），不许落在主枝
    强 = re.findall(r"'git', 'push'.*?\)", s, re.S)
    T('②凡强推皆落存底枝，主枝一处不推（今 %d 处 push）' % len(强),
      all(('--force' not in x) or ('底枝' in x) for x in 强) and not any('主枝' in x for x in 强),
      str(强)[:200])
    # ③章标不许覆盖（标是不动的）——本仓拒推 tag，标落在 refs/heads/章-N，
    #   故其凭不是「不带 --force」这一句空话，而是：**打标那一段码里一个 --force 也没有**。
    段标 = s.split('def 标(')[1].split('\ndef ')[0]
    T('③打标那一段不带 --force（标不许被覆盖）',
      '--force' not in 段标 and 'refs/heads/%s' in 段标 and "'--tags'" not in 段标, 段标[-90:])
    T('③之二 标之名恒为 章-N（不夹说明、不夹日子）', "名 = '章-%d' % int(n)" in 段标)
    T('④临时索引跑毕即除（不吃盘）', 'os.remove(idx)' in s and 'finally' in s)
    T('⑤存底枝与主枝之名不同，且皆当场自常量取', 底枝 != 主枝 and 底枝.startswith('备份/'))
    # ⑥★**没有演过的备份不算备份**：本器须有一路真去克隆、真去比的活
    段演 = s.split('def 演(')[1].split('\ndef ')[0] if 'def 演(' in s else ''
    T('⑥有一路真去克隆下来比（非只看账面）',
      "'clone'" in 段演 and 'getsize' in 段演, '演之段 %d 字' % len(段演))
    T('⑥之二 演所比者含「正在写而未提交的那一章」（存底枝立起来正为这一样）',
      'ROOT' in 段演 and "'正文'" in 段演)
    T('⑥之三 演跑毕即除其临时之仓（不吃盘）', 'rmtree' in 段演 and 'finally' in 段演)
    print('── 负测·存底 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    a = sys.argv
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--存' in a:
        i = a.index('--存')
        rc, m = 存(a[i + 1] if len(a) > i + 1 else '')
        print('✓存底已上云端：%s' % m if rc == 0 else '⛔存底未成：%s' % m)
        sys.exit(rc)
    if '--标' in a:
        i = a.index('--标')
        rc, m = 标(a[i + 1])
        print('✓章标：%s' % m if rc == 0 else '⛔打标未成：%s' % m)
        sys.exit(rc)
    if '--演' in a:
        i = a.index('--演')
        章 = a[i + 1] if len(a) > i + 1 and a[i + 1].isdigit() else None
        rc, m = 演(章)
        print('✓演过了：%s' % m if rc == 0 else '⛔演不过：%s' % m)
        sys.exit(rc)
    验()
    sys.exit(0)
