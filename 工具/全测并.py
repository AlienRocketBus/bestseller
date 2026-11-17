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

  ⑤（1027 坑54）GitHub 分片之闸亦取本器：`分片`（LPT·定式）、`择片数`（三或四：多一片所省之关键路须过一片之开销）、
     `并判`（诸片之果并而判：恰一之验、留字、空跑闸、推闸——与本机之并同一 `判果`，⛔另写）；秒表取 报/均秒.json（GitHub 实测、并判每跑更之），
     缺即仓中之种 设定/全测均秒.json（⛔读 _器之账.json：各机不同，诸片之分即不一）。

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
    变, 增, 失 = 全测._留字之差(主前)
    副留 = {os.path.basename(p): 副本之留字(p) for p in 诸片}
    副留 = {k: v for k, v in 副留.items() if v}
    留 = None
    if 变 or 增 or 失 or 副留:
        if _席凭 and not 副留:
            print('  ⚠ %-14s **本次係带席而跑**：主仓库内容有变 %d｜新增 %d｜消失 %d（多半係席所写）' % ('负测留字', len(变), len(增), len(失)))
        else:
            留 = '主仓库：变 %d｜增 %d｜失 %d %s｜副本：%s' % (
                len(变), len(增), len(失), '、'.join((变 + 增 + 失)[:4]),
                '；'.join('%s %s' % (k, '、'.join(v[:4])) for k, v in 副留.items()) or '无')
    else:
        print('  ✓ %-14s 主仓库 设定／版本／正文 跑前跑後 sha256 逐档同；%d 份副本 git status 俱净' % ('负测留字', len(诸片)))
    rc, fails, 语, _ = 判果(名们, 果, 留, quick, 器账=True)
    墙 = time.time() - t0
    print('  · 墙时 %.0f 秒｜诸项之秒合计 %.0f｜并之倍 %.1f' % (墙, sum(r[3] for r in 果.values()), sum(r[3] for r in 果.values()) / max(墙, 1)))
    return rc


def 判果(名们, 果, 留字红, quick, 账=None, 章=None, 器账=False, 印=print):
    """并果之判——本机之并（main）与 GitHub 之并判（并判）同此一函：照原序印、留字、空跑闸、推闸。
    账 None：沙盒之推闸（读写本地并云端之器红账）；给出：GitHub 之判（推闸判，新账交调者落 备份/报）。
    → (rc, fails, 推闸之语, 新账)；rc 0 过｜1 红。"""
    import 全测
    fails, 录 = [], []
    for 名 in 名们:
        r = 果.get(名) or [名, False, '⛔未跑（并行之驱漏之）', 0]
        录.append((名, bool(r[1]), r[3], str(r[2])))
        印('  %s %-14s %s' % ('✓' if r[1] else '✗', 名, r[2]))
        if not r[1]:
            fails.append(名)
    if 器账:
        全测._记器账(录, quick)
    if 留字红:
        印('  ✗ %-14s %s' % ('负测留字', 留字红))
        fails.append('负测留字')
    if len(果) < (全测.最少件数 if not quick else 8):
        印('\n  ⛔空跑闸：本次只跑了 %d 件——并行之驱或项表有病。' % len(果))
        return 1, fails or ['空跑闸'], '', 账
    if not fails:
        印('\n  ✓全测通过%s（并）。' % ('（快测，未含全书检）' if quick else ''))
        if 账 is None:
            全测.推闸([], 名们)                  # 俱绿亦更器红账：所跑之格俱销（⛔留旧首见，复红时误判逾限）
            return 0, [], '', None
        _, 语, 新账 = 全测.推闸判([], 账, 章 if 章 is not None else (全测._末章() or 0), 名们 if quick else None)
        return 0, [], 语, 新账
    印('\n  ⛔全测未过：%s' % '、'.join(fails))
    if 账 is None:
        ok, 语 = 全测.推闸(fails, 名们)
        新账 = None
    else:
        ok, 语, 新账 = 全测.推闸判(fails, 账, 章 if 章 is not None else (全测._末章() or 0), 名们 if quick else None)
    印('  %s' % 语)
    if not ok:
        印('  【批115】不过不许推——pre-push 钩子据此拦停。')
    return 1, fails, 语, 新账


# ═══ 片（1027 坑54·GitHub 分片之闸：autopush、演练之 shard 之阵）═══
种秒档 = os.path.join(ROOT, '设定', '全测均秒.json')
片开销 = 75          # 一片之起（checkout 全史、装机、取候之包、上果）约秒——多开一片计分多此一份
片数之候 = (3, 4)
默秒 = 30.0


def 秒表(档=None):
    """分片之秒表 {名: 秒}：所给之档（GitHub 之 报/均秒.json，经候之包传诸片——诸片同一档）→ 缺或坏即仓中之种。
    ⛔读 _器之账.json（各机不同，诸片各算之分即不一）。"""
    for p in ([档] if 档 else []) + [种秒档]:
        try:
            d = json.load(open(p, encoding='utf-8'))
            if isinstance(d, dict) and d:
                return {str(k): float(v) for k, v in d.items() if isinstance(v, (int, float))}
        except Exception:
            continue
    return {}


def 分片(名们, 秒, n):
    """LPT：长者先（同秒依原序），逐个入当前最轻之片（同轻取号小者）——定式：同表同秒，诸片各算皆同。→ n 列，每名恰在一列。"""
    序 = sorted(range(len(名们)), key=lambda i: (-float(秒.get(名们[i], 默秒)), i))
    片们, 重 = [[] for _ in range(n)], [0.0] * n
    for i in 序:
        j = min(range(n), key=lambda x: (重[x], x))
        片们[j].append(名们[i])
        重[j] += float(秒.get(名们[i], 默秒))
    return 片们


def 片之秒(片们, 秒):
    return [round(sum(float(秒.get(x, 默秒)) for x in p), 1) for p in 片们]


def 择片数(名们, 秒, 候=片数之候, 开销=片开销):
    """→ (n, {n: 关键路之秒})。自少者起：多一片所省之关键路 ≥ 一片之开销方多开（省墙时而⛔白耗计分）。"""
    诸 = {n: max(片之秒(分片(名们, 秒, n), 秒) or [0]) + 开销 for n in 候}
    n = 候[0]
    for m in 候[1:]:
        if 诸[n] - 诸[m] >= 开销:
            n = m
    return n, 诸


def 表纹(名们):
    import hashlib
    return hashlib.sha1('\n'.join(名们).encode('utf-8')).hexdigest()[:12]


def 读片(目):
    """目下（递归）之诸片档 → [dict]（坏者以 {'坏': 路}）。"""
    出 = []
    for dp, _, fs in os.walk(目):
        for f in sorted(fs):
            if not f.endswith('.json'):
                continue
            p = os.path.join(dp, f)
            try:
                d = json.load(open(p, encoding='utf-8'))
            except Exception:
                出.append({'坏': p})
                continue
            if isinstance(d, dict) and '片' in d and '果' in d:
                出.append(d)
    return 出


def 并判(诸片, 候=None, 账=None, 章=None, quick=False, 印=print, 名们=None):
    """GitHub 之并判：诸片之果 → (rc, 判)。rc 0 过｜1 红（推闸同策）｜2 败（片缺、片坏、sha 不一、恰一不成——⛔以残果判）。
    判：{果, fails, 读红, 器红, 逾, 语, 新账, 片秒, 诸秒}"""
    import 全测
    去 = []
    if not 名们:
        # ★1117 片去活态（法用#片去活态）：GitHub 上片闸之表＝全表去活态之格（全测.闸之诸项·与 --片数、--片 同一函）。
        #   降级之容：诸片之表纹若为全表（旧式：开关关、旧器之片）或「全表去活态之格」（沙盒并 GitHub 之片），即以其表判（恰一照验）；⛔认他表。
        全名 = [x for x, _ in 全测.诸项(quick)]
        名们 = [x for x, _ in 全测.闸之诸项(quick)]
        纹们 = {d.get('表') for d in 诸片 if '坏' not in d}
        if len(纹们) == 1 and 表纹(名们) not in 纹们:
            for 候表 in (全名, [x for x in 全名 if x not in 全测.活态之格]):
                if 表纹(候表) in 纹们:
                    名们 = 候表
                    break
        去 = [x for x in 全名 if x not in 名们]
    章 = 章 if 章 is not None else (全测._末章() or 0)
    判 = {'果': '败', 'fails': [], '读红': [], '器红': [], '逾': [], '语': '', '新账': None, '片秒': {}, '诸秒': {}, '免': 去}
    败 = []
    坏 = [d['坏'] for d in 诸片 if '坏' in d]
    诸片 = [d for d in 诸片 if '坏' not in d]
    if 坏:
        败.append('片档坏：%s' % '、'.join(坏[:4]))
    数们 = sorted({d.get('数') for d in 诸片}, key=str)
    号们 = sorted(d.get('片') for d in 诸片 if isinstance(d.get('片'), int))
    if len(数们) != 1 or not isinstance(数们[0], int) or 号们 != list(range(1, 数们[0] + 1)):
        败.append('片缺或重：得 %s（片数 %s）' % (号们, 数们))
    sha们 = {d.get('sha') for d in 诸片}
    if len(sha们) != 1 or (候 and sha们 != {候}):
        败.append('诸片所验之树非候（%s ≠ 候 %s）——⛔以他树之果放行' % ('、'.join(sorted(str(x)[:12] for x in sha们)), (候 or '')[:12]))
    if any(d.get('表') != 表纹(名们) for d in 诸片):
        败.append('片之项表与候之树不一（表纹）')
    if any(bool(d.get('快')) != bool(quick) for d in 诸片):
        败.append('片之快慢与并判不一')
    计 = {}
    for d in 诸片:
        for x in d.get('名们') or []:
            计[x] = 计.get(x, 0) + 1
    重, 漏, 外 = sorted(x for x, c in 计.items() if c > 1), [x for x in 名们 if x not in 计], sorted(x for x in 计 if x not in 名们)
    if 重 or 漏 or 外:
        败.append('分片恰一不成：重 %s｜漏 %s｜外 %s' % (重[:4], 漏[:4], 外[:4]))
    果 = {}
    for d in sorted(诸片, key=lambda x: str(x.get('片'))):
        for r in d.get('果') or []:
            果[r[0]] = r
        判['片秒'][str(d.get('片'))] = d.get('秒')
        未 = [x for x in d.get('名们') or [] if x not in 果]
        if 未 or not d.get('毕'):
            败.append('片 %s 未毕（逾时或崩）：未跑 %d 项 %s' % (d.get('片'), len(未), '、'.join(未[:4])))
    if 败:
        for x in 败:
            印('  ⛔片闸·败：' + x)
        判['语'] = '；'.join(败)
        return 2, 判
    判['诸秒'] = {k: v[3] for k, v in 果.items()}
    留 = []
    for d in sorted(诸片, key=lambda x: x['片']):
        if d.get('留字') and not d.get('席凭'):
            留.append('片%s：%s' % (d['片'], '、'.join(d['留字'][:4])))
        elif d.get('留字'):
            印('  ⚠ %-14s 片%s 带席（%s）：%s' % ('负测留字', d['片'], '、'.join(d['席凭']), '、'.join(d['留字'][:4])))
    印('\n████ 全测·并判 · %d 项 · %d 片 · 候 %s ████' % (len(名们), 数们[0], (候 or next(iter(sha们)) or '')[:12]))
    rc, fails, 语, 新账 = 判果(名们, 果, '；'.join(留) or None, quick, 账=dict(账 or {}), 章=章, 印=印)
    读红, 器红 = 全测.分等(fails)
    if rc != 0 and 语.startswith('✓推闸'):
        rc = 0                                  # 只器之红而未逾限：推闸放行（与 pre-push 认「✓推闸·分等：放行」同）
    判.update(果='过' if rc == 0 else '红', fails=fails, 读红=读红, 器红=器红, 语=语, 新账=新账, 章=章,
             逾=[k for k in 器红 if 新账 and k in 新账 and 章 > 新账[k]['限']])
    印('  · 诸片之秒：%s' % '、'.join('%s→%s' % kv for kv in sorted(判['片秒'].items())))
    if 去:
        印('  · 活态免（GitHub·法用#片去活态）：%s——沙盒之全测与封版之活态之报照跑；复旧：全测.活态免GitHub = False' % '、'.join(去))
    return rc, 判


def 新秒表(旧, 诸秒, 名们):
    """GitHub 实测之秒入表（指数平滑 0.7 旧＋0.3 新；只留今表之格）。"""
    出 = {}
    for x in 名们:
        if x in 诸秒:
            出[x] = round(0.7 * float(旧[x]) + 0.3 * float(诸秒[x]), 2) if x in 旧 else round(float(诸秒[x]), 2)
        elif x in 旧:
            出[x] = 旧[x]
    return 出


def 并判口(a, quick):
    """`全测.py --并果 目 --候 sha [--账 档 --账出 档 --判 档 --秒表 档 --秒出 档]` → rc 0 过｜1 红｜2 败。"""
    import 全测
    def 参(k):
        return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    账 = {}
    if 参('--账'):
        try:
            账 = json.load(open(参('--账'), encoding='utf-8'))
        except Exception:
            账 = {}
    rc, 判 = 并判(读片(参('--并果') or '.'), 参('--候'), 全测.并账(账 if isinstance(账, dict) else {}), quick=quick)
    if 参('--账出') and 判.get('新账') is not None:
        json.dump(判['新账'], open(参('--账出'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    if 参('--秒出') and 判.get('诸秒') and rc in (0, 1):
        名们 = [x for x, _ in 全测.诸项(quick)]
        json.dump(新秒表(秒表(参('--秒表')), 判['诸秒'], 名们), open(参('--秒出'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    if 参('--判'):
        json.dump({k: v for k, v in 判.items() if k != '新账'}, open(参('--判'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return rc

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
    R += 片之自测(名们)
    R += 片去活态之自测(名们)
    for k, ok in R:
        print('  %s %s' % ('✓' if ok else '✗', k))
    ok = sum(1 for _, o in R if o)
    print('  全测并·自测 %d/%d %s' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    return 0 if ok == len(R) else 1


def 片之自测(名们):
    """1027 坑54：GitHub 分片之闸——分片恰一（N＝1..4）、择片数、并判之四形（俱绿／只器红／读者红／器红逾限）与败形、器红账、片跑往返。"""
    import 全测
    R = []
    秒 = 秒表()
    恰 = True
    for n in (1, 2, 3, 4):
        p = 分片(名们, 秒, n)
        恰 = 恰 and len(p) == n and sorted(sum(p, [])) == sorted(名们) and len(sum(p, [])) == len(名们) and p == 分片(list(名们), dict(秒), n)
    R.append(('⑦分片恰一：N＝1..4 诸片之并恰为全表、各格恰一、定式（再算全同）', 恰))
    重 = 片之秒(分片(名们, 秒, 4), 秒)
    R.append(('⑦之二 LPT 之均：最重与最轻之差 ≤ 最长一格（今 %s）' % 重, max(重) - min(重) <= max(float(秒.get(x, 默秒)) for x in 名们)))
    R.append(('⑦之三 种表（设定/全测均秒.json）可读、所给之档坏即退种', bool(秒) and 秒表('/无此档.json') == 秒))
    n, 诸 = 择片数(名们, 秒)
    小 = {'甲': 100.0, '乙': 10.0, '丙': 10.0, '丁': 10.0, '戊': 10.0}
    R.append(('⑧择片数：三或四；多一片所省 ≥ 一片之开销方取四（大格独占即取三）',
              n in 片数之候 and (n == 4) == (诸[3] - 诸[4] >= 片开销) and 择片数(list(小), 小)[0] == 3))
    # ⑨并判：以真表造片之果（俱绿而改其一二）
    sha = 'c' * 40

    def 造(n=3, 红=(), 留=None, 改=None):
        诸 = []
        for k, 我 in enumerate(分片(名们, 秒, n), 1):
            诸.append({'片': k, '数': n, 'sha': sha, '表': 表纹(名们), '快': False, '名们': list(我),
                       '果': [[x, x not in 红, 'ok' if x not in 红 else '坏', 1.0] for x in 我],
                       '留字': (留 if k == 1 and 留 else []), '席凭': [], '秒': len(我), '毕': True})
        if 改:
            改(诸)
        return 诸
    读 = sorted(全测.读者可见之闸 & set(名们))[0]
    器 = next(x for x in 名们 if x not in 全测.读者可见之闸)
    静 = lambda *a, **k: None

    def 判(诸, 账=None, 章=420):
        return 并判(诸, sha, 账 if 账 is not None else {}, 章, 印=静, 名们=名们)
    rc, d = 判(造())
    R.append(('⑨并判·俱绿 → 过（rc 0）、新账空', rc == 0 and d['果'] == '过' and d['新账'] == {}))
    rc, d = 判(造(红=(器,)), {'旧已绿之格': {'首见': 400, '末见': 401, '限': 403}})
    R.append(('⑨之二 只器之红 → 过、入账（首见 末见 420、限 423）、已绿者销',
              rc == 0 and d['果'] == '过' and d['器红'] == [器] and d['新账'] == {器: {'首见': 420, '末见': 420, '限': 423}}))
    rc, d = 判(造(红=(读, 器)))
    R.append(('⑨之三 读者可见之红 → 红（rc 1）', rc == 1 and d['果'] == '红' and d['读红'] == [读]))
    rc, d = 判(造(红=(器,)), {器: {'首见': 416, '末见': 419, '限': 419}})
    R.append(('⑨之四 器红逾限（首见 416、今 420）→ 红、逾、语「⛔推闸·器红逾限」、首见留旧',
              rc == 1 and d['果'] == '红' and d['逾'] == [器] and d['语'].startswith('⛔推闸·器红逾限') and d['新账'][器]['首见'] == 416))
    rc, d = 判(造(红=(器,)), {器: {'首见': 417}})
    R.append(('⑨之五 器红恰在限之章（首见 417、今 420）→ 过而预警', rc == 0 and '本章即限' in d['语']))
    rc, d = 判(造(留=['设定/x.md']))
    R.append(('⑨之六 片之留字（无席）→ 负测留字红（读者可见）', rc == 1 and '负测留字' in d['读红']))
    败形 = {
        '片缺': 造(改=lambda 诸: 诸.pop()),
        '片之树非候': 造(改=lambda 诸: 诸[1].update(sha='d' * 40)),
        '一格二片': 造(改=lambda 诸: 诸[0]['名们'].append(诸[1]['名们'][0])),
        '片未毕（逾时）': 造(改=lambda 诸: (诸[2].update(毕=False), 诸[2]['果'].pop())),
        '表纹不一': 造(改=lambda 诸: 诸[0].update(表='x')),
        '片档坏': 造(改=lambda 诸: 诸.append({'坏': '/x.json'})),
    }
    R.append(('⑩并判之败（%s）→ rc 2、⛔以残果判' % '、'.join(败形), all(判(v)[0] == 2 for v in 败形.values())))
    # ⑪器红账：并账首见取早、纯判⛔写盘、快测⛔销未跑之格
    合 = 全测.并账({'a': {'首见': 412, '限': 415}}, {'a': {'首见': 410, '末见': 411, '限': 413}, 'b': {'首见': 'x'}})
    新, 逾 = 全测.器红之判(['a'], 414, 合, 跑过=['a', 'c'])
    R.append(('⑪器红账：本地并云端首见取早（410）、坏笔弃；只跑数格⛔销未跑之格', 合 == {'a': {'首见': 410, '末见': 412, '限': 413}}
              and 逾 == ['a'] and 全测.器红之判([], 414, {'b': {'首见': 1}}, 跑过=['a'])[0] == {'b': {'首见': 1}}))
    R.append(('⑪之二 新秒表：平滑、只留今表之格', 新秒表({'a': 10, 'z': 5}, {'a': 20, 'b': 3}, ['a', 'b']) == {'a': 13.0, 'b': 3.0}))
    # ⑫片跑往返：真 全测.片跑 跑假格三片，--并果 之口并之（账出、判、秒出）
    原诸项, 原照 = 全测.诸项, 全测._留字快照
    假 = [('假%d' % i, (lambda i=i: (i != 5, '第%d' % i))) for i in range(45)]
    try:
        全测.诸项 = lambda quick: list(假)
        全测._留字快照 = lambda: {}
        with tempfile.TemporaryDirectory() as t:
            import contextlib
            import io
            片目_ = os.path.join(t, '片')
            with contextlib.redirect_stdout(io.StringIO()):
                rcs = [全测.片跑(k, 3, os.path.join(片目_, '%d.json' % k), False, '/无此档.json') for k in (1, 2, 3)]
                json.dump({'假5': {'首见': 1}}, open(os.path.join(t, '账.json'), 'w'))
                候 = json.load(open(os.path.join(片目_, '1.json'), encoding='utf-8'))['sha']
                rc = 并判口(['--并果', 片目_, '--候', 候, '--账', os.path.join(t, '账.json'), '--账出', os.path.join(t, '新账.json'),
                           '--判', os.path.join(t, '判.json'), '--秒出', os.path.join(t, '秒.json'), '--秒表', '/无此档.json'], False)
            j = json.load(open(os.path.join(t, '判.json'), encoding='utf-8'))
            新 = json.load(open(os.path.join(t, '新账.json'), encoding='utf-8'))
            R.append(('⑫片跑往返：三片各落其档、并判恰一而判（假5 器红首见 1 → 逾限 → 红）、账出与秒出俱落',
                      sorted(rcs) == [0, 0, 1] and rc == 1 and j['果'] == '红' and j['逾'] == ['假5'] and 新['假5']['首见'] == 1
                      and sorted(json.load(open(os.path.join(t, '秒.json'), encoding='utf-8'))) == sorted(n for n, _ in 假)))
    finally:
        全测.诸项, 全测._留字快照 = 原诸项, 原照
    return R


def _封版之活态之格():
    """封版.py 之 `活态之格 = (...)`（封版 --後 之活态之报於沙盒所跑）——ast 取之（⛔import 封版：其载重）。"""
    import ast
    try:
        for n in ast.parse(open(os.path.join(ROOT, '工具', '封版.py'), encoding='utf-8').read()).body:
            if isinstance(n, ast.Assign) and any(getattr(t, 'id', '') == '活态之格' for t in n.targets):
                return tuple(ast.literal_eval(n.value))
    except Exception:
        pass
    return ()


def 片去活态之自测(名们):
    """1117 GitHub 化之审·H（法用#片去活态）：GitHub 片闸免活态之格——名单之据、沙盒照跑、免之形、降级（开关、名单不合、表纹之容）、片跑往返。"""
    import 全测
    import contextlib
    import io
    R = []
    格 = tuple(全测.活态之格)
    快 = [n for n, _ in 全测.诸项(True)]
    R.append(('⑬片去活态·名单：活态之格 ⊆ 全测并.活态（W51 串并对表所定·⛔凭猜添）；沙盒照跑——俱在全测之全表与快表、俱在 封版.活态之格（--後 之活态之报）',
              bool(格) and set(格) <= set(活态) and set(格) <= set(名们) and set(格) <= set(快) and set(格) <= set(_封版之活态之格())))
    R.append(('⑬之二 ⛔免判树之活态：跑账（乙路·注没注上）、钩子挂载（pre-push 在盘·读者可见）、负测·自进化环（自测）——GitHub 上红得起',
              not ({'跑账', '钩子挂载', '负测·自进化环'} & set(格)) and not (set(格) & 全测.读者可见之闸)))
    # ⛔诸格不随开关之位：开之诸验当场置开（finally 复原）——开关关（降级）时本测照绿，⛔令降级反红闸
    原境, 原关, 原格 = os.environ.get('GITHUB_ACTIONS'), 全测.活态免GitHub, 全测.活态之格

    def 境(v):
        if v is None:
            os.environ.pop('GITHUB_ACTIONS', None)
        else:
            os.environ['GITHUB_ACTIONS'] = v
    try:
        全测.活态免GitHub = True
        境(None)
        沙 = [n for n, _ in 全测.闸之诸项(False)]
        境('true')
        云 = [n for n, _ in 全测.闸之诸项(False)]
        云语 = 全测.活态之语(名们)
        全测.活态免GitHub = False
        复 = [n for n, _ in 全测.闸之诸项(False)]
        复语 = 全测.活态之语(名们)
        全测.活态免GitHub = True
        全测.活态之格 = 格 + ('无此格',)
        缺去, 缺 = 全测.活态之免(名们)
        缺语 = 全测.活态之语(名们)
        缺表 = [n for n, _ in 全测.闸之诸项(False)]
    finally:
        全测.活态免GitHub, 全测.活态之格 = 原关, 原格
        境(原境)
    R.append(('⑬之三 沙盒（非 GitHub）片闸之表＝全表；GitHub 上恰去活态之格（余序不变）而印其免；开关关（活态免GitHub = False）即复全表',
              沙 == 名们 and 云 == [n for n in 名们 if n not in 格] and 格[0] in 云语 and '活态免' in 云语 and 复 == 名们 and 复语 == ''))
    R.append(('⑬之四 降级：名单之名有不在表者（改名、删格）→ ⛔免、全跑（旧式）而语带⚠',
              缺去 == () and 缺 == ['无此格'] and 缺语.startswith('⚠') and 缺表 == 名们))
    # ⑬之五 并判之表纹之容：默表（闸之诸项）与诸片之表不一时，诸片之表为全表或「全表去活态」方认；他表照败
    秒 = 秒表()
    sha = 'e' * 40

    def 造(表名):
        return [{'片': k, '数': 3, 'sha': sha, '表': 表纹(表名), '快': False, '名们': list(我),
                 '果': [[x, True, 'ok', 1.0] for x in 我], '留字': [], '席凭': [], '秒': len(我), '毕': True}
                for k, 我 in enumerate(分片(表名, 秒, 3), 1)]
    静 = lambda *a, **k: None
    去表 = [n for n in 名们 if n not in 格]
    try:
        全测.活态免GitHub = True
        境('true')
        rc云全, d云全 = 并判(造(名们), sha, {}, 420, 印=静)
        rc云去, d云去 = 并判(造(去表), sha, {}, 420, 印=静)
        境(None)
        rc沙去, d沙去 = 并判(造(去表), sha, {}, 420, 印=静)
        rc沙全, d沙全 = 并判(造(名们), sha, {}, 420, 印=静)
        rc他, _ = 并判(造(名们[:-1] + ['外格']), sha, {}, 420, 印=静)
    finally:
        全测.活态免GitHub = 原关
        境(原境)
    R.append(('⑬之五 并判：GitHub 之去表 → 过而判记其免；诸片跑全表（旧式）→ 以全表判、⛔免；沙盒判 GitHub 之去表 → 认；他表 → rc 2',
              rc云去 == 0 and d云去['免'] == list(格) and rc云全 == 0 and d云全['免'] == [] and rc沙去 == 0 and d沙去['免'] == list(格)
              and rc沙全 == 0 and d沙全['免'] == [] and rc他 == 2))
    # ⑬之六 片跑往返（GitHub 之境）：假表含「接力」——诸片⛔跑之（其函一跑即记）、片档记其免、--并果 恰一而过、--秒出 留其旧秒
    原诸项, 原照 = 全测.诸项, 全测._留字快照
    跑了 = []
    假 = [('假%d' % i, (lambda i=i: (True, '第%d' % i))) for i in range(44)] + [('接力', lambda: (跑了.append(1), (True, '活'))[1])]
    try:
        全测.诸项 = lambda quick: list(假)
        全测._留字快照 = lambda: {}
        全测.活态免GitHub = True
        境('true')
        with tempfile.TemporaryDirectory() as t:
            片目_ = os.path.join(t, '片')
            json.dump({'接力': 0.42, '假0': 9.0}, open(os.path.join(t, '秒.json'), 'w'))
            with contextlib.redirect_stdout(io.StringIO()) as 印:
                rcs = [全测.片跑(k, 3, os.path.join(片目_, '%d.json' % k), False, os.path.join(t, '秒.json')) for k in (1, 2, 3)]
                候 = json.load(open(os.path.join(片目_, '1.json'), encoding='utf-8'))['sha']
                rc = 并判口(['--并果', 片目_, '--候', 候, '--判', os.path.join(t, '判.json'), '--秒出', os.path.join(t, '秒出.json'),
                           '--秒表', os.path.join(t, '秒.json')], False)
            诸档 = [json.load(open(os.path.join(片目_, '%d.json' % k), encoding='utf-8')) for k in (1, 2, 3)]
            j = json.load(open(os.path.join(t, '判.json'), encoding='utf-8'))
            秒出 = json.load(open(os.path.join(t, '秒出.json'), encoding='utf-8'))
        印文 = 印.getvalue()
    finally:
        全测.诸项, 全测._留字快照 = 原诸项, 原照
        全测.活态免GitHub = 原关
        境(原境)
    R.append(('⑬之六 片跑往返（GitHub 之境）：接力⛔跑、三片之名们之并＝去表、片档记免、并判过而印「活态免」、秒出留接力之旧秒（复旧时分片⛔失其秒）',
              not 跑了 and rcs == [0, 0, 0] and rc == 0 and sorted(sum((d['名们'] for d in 诸档), [])) == sorted('假%d' % i for i in range(44))
              and all(d['免'] == ['接力'] for d in 诸档) and j['免'] == ['接力'] and '活态免' in 印文 and 秒出.get('接力') == 0.42))
    # ⑬之七 --片数 之 stdout 唯片数（备候以 $(…) 取之）：GitHub 之境亦然（免之语入 stderr）
    e = dict(os.environ, GITHUB_ACTIONS='true')
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '全测.py'), '--片数'], cwd=ROOT, env=e, capture_output=True, text=True, timeout=120)
    R.append(('⑬之七 --片数（GitHub 之境）：stdout 唯一整数；免之语在 stderr（开关开即有、关即无——降级⛔红）', r.returncode == 0 and r.stdout.strip().isdigit()
              and len(r.stdout.strip().split('\n')) == 1 and ('活态免' in r.stderr) == bool(原关)))
    try:
        import 推报
        报 = 推报.成报('章-1', 'a' * 40, '成', '', 判={'免': ['接力'], '片秒': {'1': 1.0}})
        演报 = 推报.成演报('试', 'x', 'a' * 40, '过', '', 判={'免': ['接力']})
        无免 = 推报.成报('章-1', 'a' * 40, '成', '', 判={'片秒': {'1': 1.0}})
        报之免 = 报.get('免') == ['接力'] and 演报.get('免') == ['接力'] and '免' not in 无免
    except Exception:
        报之免 = False
    R.append(('⑬之八 报/推、报/演 之 json 记其免（并判之判.免·可观）；不免者⛔此键', 报之免))
    return R


if __name__ == '__main__':
    sys.exit(main())
