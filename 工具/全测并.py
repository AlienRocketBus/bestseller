#!/usr/bin/env python3
"""全测并.py——全测之分片并行（W51·1017 立）：同一表、同一判，墙时约串行之三分之一，负测只改副本。

为何立：作者 1017 转来他件之法（GitHub 多机并行、逐屏比对、无人值守），令「一切皆可进化」。
  本仓私有（Actions 非免费）、费在 token、章不可并行——故只取其核：**并行、隔离、无人值守之验**，於本机行之。
  推前全测 185 项串行约 19 分（`_器之账.json` 均秒合计 1463）；十余份负测在真仓库上改档再复原，
  故推时主环⛔改档。今：
  ① `.git/全测片/片k` 若干份工作副本（detach 到 HEAD；`git clean -fdx` 後拷入主仓库之忽略之状态档）；
  ② 诸项按均秒长者先，入一个动态之队，诸片各取各跑（`python3 工具/全测.py --只 名 --出 档`，跑的是副本里之器）；
  ③ 「活态」之项（读主仓库之现场：心跳、存底枝、推之日志……）留主仓库与诸片同时跑；
  ④ 并果照原序印、留字（副本以 git status、主仓库以 _留字快照）、空跑闸、推闸——俱取 全测.py 之原函，⛔另写一份。
  验之所验係 HEAD（已提交者）；工作区若有未提交之改，印其警。

用法：
  python3 工具/全测并.py [--快] [--片 N]      # 默 N＝核数−1（至少 1）
  python3 工具/全测并.py --自测
上线之律（设定/方案/W51.md）：同一 HEAD 串并逐项过否全同、墙时 ≤ 串行 2/5、主仓库 sha256 跑前跑後同；不胜即退（钩照旧串行）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
片目 = os.path.join(ROOT, '.git', '全测片')
# 活态之项：读主仓库之现场（忽略之状态档、.git 内之日志、心跳、存底枝、钩之挂载），副本里读不着或读到旧的——留主仓库跑。
#   ★其名单由一处试定（W51 环3：串并逐项对表，凡不同者归此），⛔凭猜添。
活态 = {'接力', '跑账', '负测·自进化环', '钩子挂载'}


def _git(args, cwd=ROOT, check=True):
    r = subprocess.run(['git', '-c', 'core.quotepath=off'] + args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError('git %s：%s' % (' '.join(args[:3]), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout


def 忽略之状态档(root=ROOT):
    """主仓库里被 .gitignore 而诸器要读之小档（_心跳.json、_跑账.json、_器之账.json……）——拷进副本，副本方同主仓库之现场。"""
    out = _git(['ls-files', '-o', '-i', '--exclude-standard'], cwd=root, check=False)
    诸 = []
    for p in out.split('\n'):
        p = p.strip().strip('"')
        if not p or '__pycache__' in p or p.startswith('.git'):
            continue
        q = os.path.join(root, p)
        if os.path.isfile(q) and os.path.getsize(q) <= 5 * 1024 * 1024:
            诸.append(p)
    return 诸


def 备片(n, sha, root=ROOT):
    """→ 诸片之路。在则 checkout 到 sha 并 clean，⛔在则 worktree add；俱拷入忽略之状态档。"""
    os.makedirs(片目, exist_ok=True)
    _git(['worktree', 'prune'], cwd=root, check=False)
    状态 = 忽略之状态档(root)
    诸 = []
    for k in range(n):
        p = os.path.join(片目, '片%d' % k)
        if os.path.isdir(os.path.join(p, '工具')):
            _git(['checkout', '-q', '-f', '--detach', sha], cwd=p)
            _git(['clean', '-q', '-f', '-d', '-x'], cwd=p)
        else:
            if os.path.exists(p):
                shutil.rmtree(p)
            _git(['worktree', 'add', '-q', '--detach', p, sha], cwd=root)
        for f in 状态:
            d = os.path.join(p, f)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            shutil.copy2(os.path.join(root, f), d)
        诸.append(p)
    return 诸


def 排(名们, 均秒):
    """长者先（LPT）——动态之队取之，诸片之末几乎齐收。均秒不知者作 30。"""
    return sorted(名们, key=lambda n: -(均秒.get(n, 30.0)))


def 均秒之表(root=ROOT):
    try:
        d = json.load(open(os.path.join(root, '_器之账.json'), encoding='utf-8'))
        return {k: float(v.get('秒均', 0) or 0) for k, v in d.items()}
    except Exception:
        return {}


def 跑一项(名, 片, quick, 出档):
    a = [sys.executable, os.path.join(片, '工具', '全测.py'), '--只', 名, '--出', 出档] + (['--快'] if quick else [])
    t0 = time.time()
    r = subprocess.run(a, cwd=片, capture_output=True, text=True)
    try:
        d = json.load(open(出档, encoding='utf-8'))
        if d.get('未认'):
            return [名, False, '⛔副本之全测不认此项（%s）' % 名, round(time.time() - t0, 2)]
        return d['果'][0]
    except Exception:
        return [名, False, '⛔并行之跑崩（rc=%s）：%s' % (r.returncode, (r.stderr or r.stdout).strip()[-300:]), round(time.time() - t0, 2)]


def 并跑(诸片, 队, 主队, quick, root=ROOT):
    """诸片各一线、取共队；主仓库一线跑主队（活态）。→ {名: [名, 过, 语, 秒]}"""
    果, 锁, 余 = {}, threading.Lock(), list(队)
    tmp = tempfile.mkdtemp(prefix='全测并_')

    def 工(片, 号):
        while True:
            with 锁:
                if not 余:
                    return
                名 = 余.pop(0)
            r = 跑一项(名, 片, quick, os.path.join(tmp, '%s_%d.json' % (号, len(果) + id(名) % 100000)))
            with 锁:
                果[名] = r

    def 主工():
        for 名 in 主队:
            r = 跑一项(名, root, quick, os.path.join(tmp, '主_%d.json' % (id(名) % 100000)))
            with 锁:
                果[名] = r

    线 = [threading.Thread(target=工, args=(p, k)) for k, p in enumerate(诸片)] + [threading.Thread(target=主工)]
    for t in 线:
        t.start()
    for t in 线:
        t.join()
    shutil.rmtree(tmp, ignore_errors=True)
    return 果


def 副本之留字(片):
    """副本係 sha 之净检出（加拷入之忽略档）——跑後 git status 有一行即负测留字（⛔含忽略档之变）。"""
    out = _git(['status', '--porcelain', '--', '设定', '版本', '正文'], cwd=片, check=False)
    免 = ('设定/自进化环.log', '设定/自进化环_挂账.json', '设定/_自进化环_推.out')
    return [l[3:].strip().strip('"') for l in out.split('\n') if l.strip() and not any(x in l for x in 免)]


def main():
    a = sys.argv[1:]
    if '--自测' in a:
        return 自测()
    quick = '--快' in a
    片数 = int(a[a.index('--片') + 1]) if '--片' in a else max(1, (os.cpu_count() or 2) - 1)
    import 全测
    t0 = time.time()
    项 = 全测.诸项(quick)
    名们 = [n for n, _ in 项]
    print('\n████ 全测·并 · %d 项 · %d 片＋主仓库 ████' % (len(名们), 片数))
    _席凭 = 全测._有席在跑()
    if _席凭:
        print('  ⚠ **本次係带席而跑**（%s）——下列诸红须逐条分辨真假（时序不是病）；待席收毕再跑一回，那一回才算数。' % '、'.join(_席凭))
    sha = _git(['rev-parse', 'HEAD']).strip()
    if _git(['status', '--porcelain', '--untracked-files=no'], check=False).strip():
        print('  ⚠ 工作区有未提交之改：并行所验係 HEAD（%s）之已提交者，⛔含未提交之改——要验之须先提交，或跑串行 全测.py' % sha[:8])
    try:
        诸片 = 备片(片数, sha)
    except Exception as e:
        print('  ⚠ 副本建不成（%s）——退回串行' % e)
        return 全测.main()
    print('  · 副本 %d 份就绪（HEAD %s；拷入忽略之状态档 %d 份）：%.0f 秒' % (len(诸片), sha[:8], len(忽略之状态档()), time.time() - t0))
    主队 = [n for n in 名们 if n in 活态]
    队 = 排([n for n in 名们 if n not in 活态], 均秒之表())
    主前 = 全测._留字快照()
    果 = 并跑(诸片, 队, 主队, quick)
    fails = []
    _器录 = []
    for 名 in 名们:
        r = 果.get(名) or [名, False, '⛔未跑（并行之驱漏之）', 0]
        _器录.append((名, bool(r[1]), r[3], str(r[2])))
        print('  %s %-14s %s' % ('✓' if r[1] else '✗', 名, r[2]))
        if not r[1]:
            fails.append(名)
    全测._记器账(_器录, quick)
    变, 增, 失 = 全测._留字之差(主前)
    副留 = {os.path.basename(p): 副本之留字(p) for p in 诸片}
    副留 = {k: v for k, v in 副留.items() if v}
    if 变 or 增 or 失 or 副留:
        if _席凭 and not 副留:
            print('  ⚠ %-14s **本次係带席而跑**：主仓库内容有变 %d｜新增 %d｜消失 %d（多半係席所写）' % ('负测留字', len(变), len(增), len(失)))
        else:
            print('  ✗ %-14s 主仓库：变 %d｜增 %d｜失 %d %s｜副本：%s' % (
                '负测留字', len(变), len(增), len(失), '、'.join((变 + 增 + 失)[:4]),
                '；'.join('%s %s' % (k, '、'.join(v[:4])) for k, v in 副留.items()) or '无'))
            fails.append('负测留字')
    else:
        print('  ✓ %-14s 主仓库 设定／版本／正文 跑前跑後 sha256 逐档同；%d 份副本 git status 俱净' % ('负测留字', len(诸片)))
    墙 = time.time() - t0
    print('  · 墙时 %.0f 秒｜诸项之秒合计 %.0f｜并之倍 %.1f' % (墙, sum(x[2] for x in _器录), sum(x[2] for x in _器录) / max(墙, 1)))
    if len(果) < (全测.最少件数 if not quick else 8):
        print('\n  ⛔空跑闸：本次只跑了 %d 件——并行之驱或项表有病。' % len(果))
        return 1
    if fails:
        print('\n  ⛔全测未过：%s' % '、'.join(fails))
        ok, 语 = 全测.推闸(fails)
        print('  %s' % 语)
        if not ok:
            print('  【批115】不过不许推——pre-push 钩子据此拦停。')
        return 1
    print('\n  ✓全测通过%s（并）。' % ('（快测，未含全书检）' if quick else ''))
    return 0


def 自测():
    R = []
    R.append(('①长者先：均秒大者排前、不知者作 30', 排(['a', 'b', 'c'], {'a': 5, 'b': 100}) == ['b', 'c', 'a']))
    import 全测
    名们 = [n for n, _ in 全测.诸项(False)]
    R.append(('②项表取自 全测.诸项（⛔另写）且活态俱在表中', set(活态) <= set(名们) and len(名们) == len(set(名们))))
    with tempfile.TemporaryDirectory() as t:
        subprocess.run(['git', 'init', '-q', t], check=True)
        os.makedirs(os.path.join(t, '设定'))
        open(os.path.join(t, '设定', 'x.md'), 'w').write('1')
        open(os.path.join(t, '.gitignore'), 'w').write('_*.json\n')
        open(os.path.join(t, '_状态.json'), 'w').write('{}')
        subprocess.run(['git', '-C', t, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', t, '-c', 'user.email=a@b', '-c', 'user.name=a', 'commit', '-qm', 'x'], check=True)
        R.append(('③忽略之状态档认得出（拷入副本之源）', 忽略之状态档(t) == ['_状态.json']))
        open(os.path.join(t, '设定', 'x.md'), 'w').write('22')
        open(os.path.join(t, '设定', '新.md'), 'w').write('n')
        R.append(('④副本之留字：改与增俱认', sorted(副本之留字(t)) == sorted(['设定/新.md', '设定/x.md'])))
    # ⑤并跑：以假之「片」验动态之队——每项俱跑一回、⛔漏⛔重
    global 跑一项
    原 = 跑一项
    次 = []
    跑一项 = lambda 名, 片, q, 出: (次.append(名), [名, True, 'ok', 0.0])[1]
    try:
        果 = 并跑(['甲', '乙', '丙'], ['a', 'b', 'c', 'd', 'e'], ['主1'], False)
    finally:
        跑一项 = 原
    R.append(('⑤动态之队：诸项各跑一回（⛔漏⛔重）、主队在主仓库', sorted(次) == ['a', 'b', 'c', 'd', 'e', '主1'] and set(果) == {'a', 'b', 'c', 'd', 'e', '主1'}))
    src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    R.append(('⑥推闸、空跑闸、留字、器账俱取 全测 之原函（⛔另写）', all(x in src for x in ('全测.推闸(', '全测.最少件数', '全测._留字之差(', '全测._记器账('))))
    for k, ok in R:
        print('  %s %s' % ('✓' if ok else '✗', k))
    print('  全测并·自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return 0 if all(o for _, o in R) else 1


if __name__ == '__main__':
    sys.exit(main())
