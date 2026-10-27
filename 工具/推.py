#!/usr/bin/env python3
"""推（1007 立；1027 坑51 改·默交 GitHub）——推送之唯一入口：一把锁、不排队、不空转、推到底。

为何立：1007 我写了「等前一次推送结束再推」之排队脚本，用 `pgrep -f "git push"` 判「有无推送在跑」，
而排队脚本自己的命令行里就含这几个字——它把自己认成「还有推送在跑」，两个脚本互等，空转一个多小时一次没推。
（教训见 `设定/教训_D6_方法之僵.md` 附「推送之锁」。）

1027 之改（坑51·404—410 一章之树三跑闸、autopush 恒输於 non-fast-forward）：旧默直推主枝，本地 pre-push 跑全测并（四百至一千二百秒），
  GitHub autopush 於同一树又跑二回——沙盒先推进主枝，GitHub 之推遂被拒。今**默交 GitHub**：推 HEAD 於 `治-<sha12>`（暂存之枝，pre-push 免闸），
  GitHub 之机分片而闸（gate.yml·一候之树一闸，1027 坑54）、过即并入主枝、果入 `备份/报`（工具/推报.py）；会话 `--候 <sha>` 零 token 候（每分至多一取、限九十分；
  红／拒／败即早返其红）；成即本地快进。`--直` 係旧法（直推主枝、本地全闸），只作兜底：报「拒」（改 .github/workflows，
  GITHUB_TOKEN 推不得）或 GitHub 停摆。

本器之法：
  ① **用文件锁（fcntl.flock，`.git/推.lock`）判「有无推送在跑」**——锁随进程生死，进程一死锁即放；
     ⛔再用 pgrep／ps 去猜进程名（会认错自己）。
  ② 锁被占 → **不排队、不等待**：只在 `.git/推.待` 记一笔「又有新提交要推」，立即返回。
  ③ 持锁者推完一次，若见 `.git/推.待`（直推：或本地仍超前远端）→ **再交／再推一次**（至多 5 回）。
  ④ 推送被全测拦（失败）→ **不重试、不循环**，印出红的那几项，返回非零——治红是人的事，⛔空转。
  ⑥ 主环等推：`python3 工具/推.py --等`（阻塞取一回锁，推毕即返；⛔pgrep／sleep 轮询——坑⑮）。
  ⑤ 每次推前先跳心跳（防「接力」误红）、枝正、速检、先存底（1008：存底环受两时之限与容器重启而死，存底枝旧则推闸之活态之检红）；全程记 `.git/推.log`。
  ⑦ `--候 <sha>`：⛔pgrep、⛔sleep 环之手候——一进程阻塞：每回一取（主枝与 备份/报 同取，至多每分一回），主枝含 sha 即快进返 0；
     报（同 sha）为红／拒／败即印其红返 3；逾限返 2（GitHub 或停摆 → `--直`）。

用法：
  python3 工具/推.py                  # 交 GitHub：推 治-<sha12>（後台跑亦可）→ 印候之令
  python3 工具/推.py --候 <sha> [分]  # 零 token 候（run_in_background）：0 主枝已含（已快进）｜3 报红／拒／败｜2 逾限（默九十分）
  python3 工具/推.py --直             # 兜底：直推主枝（本地 pre-push 全闸）——只於报「拒」或 GitHub 停摆
  python3 工具/推.py --状             # 有无推送在跑、本地超前几笔
  python3 工具/推.py --等             # 阻塞取一回锁（推者一放即返）
  python3 工具/推.py --自测
⛔ZM_SKIP_HOOK、⛔--no-verify：本器只调普通 `git push`；治枝之免闸係钩自判（工具/githooks/pre-push），主枝照闸。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, fcntl, subprocess, time, tempfile, glob, json, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
枝 = 'claude/the-novel-review-4dtuit'
re_号 = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _git目录(root):
    return os.path.join(root, '.git')


def _跑(args, root=ROOT, **kw):
    return subprocess.run(args, cwd=root, capture_output=True, text=True, **kw)


def 超前(root=ROOT):
    _跑(['git', 'fetch', '-q', 'origin', 枝], root)
    r = _跑(['git', 'rev-list', '--count', 'origin/%s..HEAD' % 枝], root)
    try:
        return int(r.stdout.strip())
    except ValueError:
        return -1


def 心跳章(root=ROOT):
    """心跳照现挂之章重跳（⛔写死章号：写到 380 以後仍跳 379 即错）。读不到则不跳之章以 0 记。"""
    try:
        import json
        return int(json.load(open(os.path.join(root, '_心跳.json'), encoding='utf-8'))['章'])
    except Exception:
        return 0     # ★1013：旧回 379（与头注「以 0 记」相违）——封版撤锁後每推一回即凭空跳一个「379 之席在跑」，自走判候、派章之链断四十五分


def 取锁(root=ROOT):
    """→ 文件对象（持锁）或 None（已有人持锁）。"""
    f = open(os.path.join(_git目录(root), '推.lock'), 'w')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return f
    except BlockingIOError:
        f.close()
        return None


def 等(root=ROOT, 限=3600):
    """★1009 坑⑮：主环等推送，⛔以 pgrep／sleep 环轮询（汉字名认不着、每回重发整个上下文）——
    只阻塞取一回锁：推者一放即返，印 `.git/推.log` 末数行与未推之数。"""
    import signal
    f = open(os.path.join(_git目录(root), '推.lock'), 'w')
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(限)
    try:
        fcntl.flock(f, fcntl.LOCK_EX)
    except TimeoutError:
        print('⛔ 等了 %d 秒推者仍持锁' % 限); return False
    finally:
        signal.alarm(0)
    fcntl.flock(f, fcntl.LOCK_UN); f.close()
    lp = os.path.join(_git目录(root), '推.log')
    if os.path.exists(lp):
        print(''.join(open(lp, encoding='utf-8').readlines()[-4:]).rstrip())
    return True


def _记(root, s):
    with open(os.path.join(_git目录(root), '推.log'), 'a', encoding='utf-8') as f:
        f.write(time.strftime('%m-%d %H:%M:%S ') + s + '\n')


速检之器 = [('改单', ['改单.py', '--查']), ('工作流账', ['工作流账.py', '--查']), ('复盘', ['复盘.py', '--验']),
          ('方法坑账', ['方法坑账.py', '--验']), ('剧情庭之关', ['剧情庭之关.py'])]


覆写之界 = 0.8          # 坑⑱：已入 git 之档一推删其八成以上之行而换新者
覆写之小 = 30           # 原档不足三十行者⛔判（小档之整改常事·⛔误拦）
覆写之域 = ('工具/', '设定/', '.claude/', '.github/')
覆写之免 = ('设定/全书记忆/', '设定/进化链.md', '阅读器/')     # 器生之档（同步、重生）⛔判


def 覆写之检(root=ROOT, 基=None):
    """★1027 坑⑱（#41·旧计「pre-commit 添整份覆写之检」——今 pre-push 免暂存之推，并入速检）：
    自 origin/<主枝> 与 HEAD 之分叉点以来，已入 git 之档（工具、设定、.claude、.github、仓根之 .md）删行 ≥ 八成、增行 ≥ 删行之半，
    而其间诸提交之说明无「覆写：」→ 红（立新器不先查同名、整份覆了旧器）。取不到基（新机未取）⛔判。→ [红之行]"""
    基 = 基 or 'refs/remotes/origin/' + 枝
    mb = _跑(['git', 'merge-base', 基, 'HEAD'], root).stdout.strip()
    if not mb:
        return []
    说 = _跑(['git', 'log', '--format=%B', mb + '..HEAD'], root).stdout
    if '覆写：' in 说 or '覆写:' in 说:
        return []
    出 = []
    for l in _跑(['git', '-c', 'core.quotepath=off', 'diff', '--numstat', mb, 'HEAD'], root).stdout.split('\n'):
        p = l.split('\t')
        if len(p) != 3 or not p[0].isdigit() or not p[1].isdigit():
            continue
        增, 删, 路 = int(p[0]), int(p[1]), p[2]
        if not (路.startswith(覆写之域) or ('/' not in 路 and 路.endswith('.md'))) or 路.startswith(覆写之免):
            continue
        r = _跑(['git', 'cat-file', '-p', '%s:%s' % (mb, 路)], root)
        if r.returncode != 0:
            continue                                   # 新档（基无之）⛔判
        原 = r.stdout.count('\n')
        if 原 >= 覆写之小 and 删 >= 覆写之界 * 原 and 增 >= 删 / 2:
            出.append('%s（原 %d 行，删 %d、增 %d）' % (路, 原, 删, 增))
    if 出:
        return ['  ✗ 覆写之检（坑⑱）：%s——整份覆了旧档？先 git ls-files 查同名、复原後改名；确要覆写者，提交说明写「覆写：<由>」' % '；'.join(出)[:300]]
    return []


def _会话之流目():
    sid = os.environ.get('CLAUDE_CODE_SESSION_ID') or ''
    if not re_号.fullmatch(sid):
        return None
    for d in glob.glob(os.path.join(os.path.expanduser('~/.claude/projects'), '*', sid, 'subagents', 'workflows')):
        return d
    return None


def 费账之检(root=ROOT, 流目=None, 今=None):
    """★1027（#40② #47·坑⑮复踩）：本会话已毕之 Run（journal 有 result；诸席俱收而其目二分无写，或三十分无写）不在 设定/费账.json → 红，
    印 `费审.py --记 <Run>`（容器一换，journal 即没，费账永缺）。无费账（非本仓）、无本会话之流目（GitHub 之机）⛔判。→ [红之行]"""
    p = os.path.join(root, '设定', '费账.json')
    流目 = 流目 if 流目 is not None else _会话之流目()
    if not 流目 or not os.path.exists(p):
        return []
    try:
        键们 = {x.get('键') for x in json.load(open(p, encoding='utf-8')).get('行') or []}
    except Exception:
        return ['  ✗ 费账之检：设定/费账.json 读不出']
    今 = 今 or time.time()
    缺 = []
    for jf in sorted(glob.glob(os.path.join(流目, 'wf_*', 'journal.jsonl'))):
        rid = os.path.basename(os.path.dirname(jf))
        起 = 果 = 败 = 0
        try:
            for l in open(jf, encoding='utf-8', errors='replace'):
                t = (json.loads(l) or {}).get('type') if l.strip().startswith('{') else None
                起 += t == 'started'; 果 += t == 'result'; 败 += t == 'failed'
            新 = max(os.path.getmtime(os.path.join(os.path.dirname(jf), x)) for x in os.listdir(os.path.dirname(jf)))
        except (OSError, ValueError):
            continue
        已毕 = 果 > 0 and ((起 <= 果 + 败 and 今 - 新 >= 120) or 今 - 新 > 1800)
        if 已毕 and rid not in 键们:
            缺.append(rid)
    if 缺:
        return ['  ✗ 费账之检（坑⑮）：本会话已毕之 Run 未入费账 %d：%s——逐个跑 %s' % (
            len(缺), '、'.join(缺), '；'.join('python3 工具/费审.py --记 %s' % r for r in 缺[:4]))]
    return []


def 速检(root=ROOT):
    """→ [红之行]。全测之中最常拦推而只须数秒者——先跑；全测仍是终审（⛔以此代之）。
    ★1027：并验 覆写之检（坑⑱）、费账之检（坑⑮：本会话已毕之 Run 俱入费账）。"""
    红 = []
    for 名, a in 速检之器:
        f = os.path.join(root, '工具', a[0])
        if not os.path.exists(f):
            continue
        try:
            r = subprocess.run([sys.executable, f] + a[1:], cwd=root, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode != 0:
            末 = [l for l in ((r.stdout or '') + (r.stderr or '')).split('\n') if l.strip()][-1:] or ['']
            红.append('  ✗ %s：%s' % (名, 末[0].strip()[:200]))
    for 检 in (覆写之检, 费账之检):
        try:
            红 += 检(root)
        except Exception as e:
            红.append('  ✗ %s 判不出：%s' % (检.__name__, str(e)[:120]))
    return 红


def 枝正(root=ROOT):
    """★1022（405 之推三回 non-fast-forward）：会话起於游离之 HEAD，本地之枝停在旧提交——`git push origin 枝` 推的是那旧枝而非 HEAD。
    → 红之行或 None：游离而枝为 HEAD 之祖即把枝挪到 HEAD 并检出（零 token）；枝不在 HEAD 之祖上即红（⛔盲挪）。"""
    当 = _跑(['git', 'symbolic-ref', '-q', '--short', 'HEAD'], root).stdout.strip()
    if 当 == 枝:
        return None
    if _跑(['git', 'merge-base', '--is-ancestor', 'refs/heads/' + 枝, 'HEAD'], root).returncode not in (0, 128):
        return '  ✗ 枝正：HEAD 不在 %s 上（今 %s），且枝不是 HEAD 之祖——先并而後推' % (枝, 当 or '游离')
    _跑(['git', 'checkout', '-q', '-B', 枝, 'HEAD'], root)
    print('· 枝正：HEAD 原%s，已把 %s 挪到 HEAD 并检出' % ('游离' if not 当 else '在 ' + 当, 枝))
    return None


def 直推(root=ROOT, 推法=None, 最多=5):
    """兜底（--直·旧法）：直推主枝、本地 pre-push 全闸。→ 0 推平｜1 被拦｜2 已有人在推（已登记待推）。"""
    待 = os.path.join(_git目录(root), '推.待')
    锁 = 取锁(root)
    if 锁 is None:
        open(待, 'w').close()
        print('· 已有一次推送在跑——已登记「跑完再推一次」，本次不排队、不等待。')
        _记(root, '登记待推')
        return 2
    try:
        for 回 in range(1, 最多 + 1):
            if os.path.exists(待):
                os.remove(待)
            if 心跳章(root):   # 无挂着之章（已撤锁）⛔跳——跳了即凭空造一个在跑之席
                _跑([sys.executable, os.path.join(ROOT, '工具', '心跳.py'), '--跳', str(心跳章(root))], root)
            if 推法 is None:
                _歪 = 枝正(root)
                if _歪:
                    print('⛔ ' + _歪.strip()); _记(root, _歪.strip()); return 1
            if 推法 is None:   # ★1016 先行之速检（392 後二回推被拦於全测第六分钟——改单之缺、工作流账逾时）：数秒之闸先跑，红即止
                速红 = 速检(root)
                if 速红:
                    print('⛔ 速检红（未起全测）——先治：\n%s' % '\n'.join(速红))
                    _记(root, '速检红：' + '｜'.join(速红)[:500])
                    return 1
            if 推法 is None:   # ★1008：先存底——存底枝新、章数齐，推闸之活态之检（负测·自进化环①之二、②）方不因存底环死而红
                _跑([sys.executable, os.path.join(ROOT, '工具', '存底.py'), '--存'], root, timeout=280)
            try:
                r = (推法 or (lambda: _跑(['git', 'push', '-u', 'origin', 枝], root, timeout=5400)))()
            except subprocess.TimeoutExpired:
                print('⛔ 推送逾九十分钟未完（网络或全测卡死）——已停，不重试')
                _记(root, '逾时')
                return 1
            输出 = (r.stdout or '') + (r.stderr or '')
            if r.returncode != 0:
                红 = [l for l in 输出.split('\n') if '✗' in l or 'error' in l or '⛔' in l][:12]
                print('⛔ 推送被拦（第 %d 回）——不重试，先治红：\n%s' % (回, '\n'.join(红)))
                _记(root, '被拦：' + '｜'.join(x.strip() for x in 红)[:500])
                return 1
            _记(root, '推成（第 %d 回）' % 回)
            前 = 超前(root)
            if 前 < 0:
                print('⚠ 推成，但取不到远端之状（fetch 失败）——不敢称推平，请跑 --状 再看')
                return 0
            if not os.path.exists(待) and 前 == 0:
                print('✓ 已推平（%d 回）' % 回)
                return 0
        print('⚠ 推了 %d 回仍未推平（提交来得太快）——下回再跑本器' % 最多)
        return 0
    finally:
        锁.close()
        # ★放锁与「他人登记待推」之间有一线之隙：放锁後再看一眼，有待推即自己再取锁推（⛔丢单）
        if os.path.exists(待) and 推法 is None:
            return 直推(root, 推法, 最多)


def 治名(sha):
    """暂存之枝名：治-<sha 前十二>（与 autopush.yml 之触、pre-push 之免、推报之 报/推/<枝> 同名）。"""
    return '治-' + sha[:12]


def _取(root=ROOT):
    """一取：主枝与 备份/报 同取（候中每回只此一调）。
    云端尚无 备份/报（首报未推、或报推不上）则同取全败、主枝亦不进——⛔候满九十分：败即单取主枝。网络卡（逾时）⛔崩候。"""
    import 推报
    主 = '+refs/heads/%s:refs/remotes/origin/%s' % (枝, 枝)
    for 参 in ([主, '+refs/heads/%s:refs/remotes/origin/%s' % (推报.报枝, 推报.报枝)], [主]):
        try:
            if _跑(['git', 'fetch', '-q', 'origin'] + 参, root, timeout=120).returncode == 0:
                return True
        except subprocess.TimeoutExpired:
            pass
    return False


def 在主(sha, root=ROOT, 取=True):
    if 取:
        _跑(['git', 'fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/origin/%s' % (枝, 枝)], root, timeout=120)
    return bool(sha) and _跑(['git', 'merge-base', '--is-ancestor', sha, 'refs/remotes/origin/' + 枝], root).returncode == 0


def 已交之枝(sha, root=ROOT):
    """→ 云端已指 sha 之暂存枝（章-*／治-*）之名们：同一树⛔再交（私库 Actions 计分；一树一闸——坑51）。"""
    r = _跑(['git', '-c', 'core.quotepath=off', 'ls-remote', 'origin', 'refs/heads/章-*', 'refs/heads/治-*'], root, timeout=60)
    return [x.split('refs/heads/', 1)[1] for x in r.stdout.split('\n') if x.startswith(sha + '\t') and 'refs/heads/' in x]


def 候之令(sha, 枝们=()):
    """已交之 sha 当以何令候：章-N 者 接棒守 --候主 N；余 推.py --候 sha12。"""
    章 = [x[2:] for x in 枝们 if x.startswith('章-') and x[2:].isdigit()]
    if 章:
        return 'python3 工具/接棒守.py --候主 %s' % 章[0]
    return 'python3 工具/推.py --候 %s' % sha[:12]


def 交(root=ROOT, 交法=None, 最多=5):
    """默（1027 坑51）：推 HEAD 於 治-<sha12>（暂存之枝：pre-push 免闸），GitHub autopush 分片而闸、过即并入主枝（1027 坑54）。
    → 0 已交（或 HEAD 已在主枝）｜1 被拦（枝歪、速检红、推不上）｜2 已有人在推（已登记待推）。⛔本地全测。"""
    待 = os.path.join(_git目录(root), '推.待')
    锁 = 取锁(root)
    if 锁 is None:
        open(待, 'w').close()
        print('· 已有一次推送在跑——已登记「跑完再推一次」，本次不排队、不等待。')
        _记(root, '登记待推')
        return 2
    try:
        for 回 in range(1, 最多 + 1):
            if os.path.exists(待):
                os.remove(待)
            if 交法 is None:
                if 心跳章(root):
                    _跑([sys.executable, os.path.join(ROOT, '工具', '心跳.py'), '--跳', str(心跳章(root))], root)
                _歪 = 枝正(root)
                if _歪:
                    print('⛔ ' + _歪.strip()); _记(root, _歪.strip()); return 1
                速红 = 速检(root)      # 数秒之闸先跑：红即⛔交（省 GitHub 一回十余分之闸）
                if 速红:
                    print('⛔ 速检红（未交 GitHub）——先治：\n%s' % '\n'.join(速红))
                    _记(root, '速检红：' + '｜'.join(速红)[:500])
                    return 1
                _跑([sys.executable, os.path.join(ROOT, '工具', '存底.py'), '--存'], root, timeout=280)
            sha = _跑(['git', 'rev-parse', 'HEAD'], root).stdout.strip()
            if not sha:
                print('⛔ 取不到 HEAD'); return 1
            if 交法 is None and 在主(sha, root):
                print('✓ HEAD（%s）已在主枝——⛔交' % sha[:12]); _记(root, '已在主枝'); return 0
            已 = 已交之枝(sha, root) if 交法 is None else []
            if 已:
                print('✓ HEAD（%s）已交 GitHub（%s）——⛔再交同树（一树一闸）；候：%s（run_in_background）'
                      % (sha[:12], '、'.join(已), 候之令(sha, 已)))
                _记(root, '已交：' + '、'.join(已)); return 0
            名 = 治名(sha)
            try:
                r = (交法 or (lambda 名: _跑(['git', 'push', 'origin', 'HEAD:refs/heads/' + 名], root, timeout=600)))(名)
            except subprocess.TimeoutExpired:
                print('⛔ 交 %s 逾十分钟未完（网络）——已停，不重试' % 名); _记(root, '交逾时'); return 1
            if r.returncode != 0:
                红 = [l for l in ((r.stdout or '') + (r.stderr or '')).split('\n') if '✗' in l or 'error' in l or '⛔' in l][:12]
                print('⛔ 交 %s 不成（第 %d 回）——不重试：\n%s' % (名, 回, '\n'.join(红)))
                _记(root, '交不成：' + '｜'.join(x.strip() for x in 红)[:500])
                return 1
            _记(root, '交 %s（第 %d 回）' % (名, 回))
            print('✓ 已交 GitHub：%s（autopush 分片而闸、过即并入主枝；果入 备份/报 之 报/推/%s.json）' % (名, 名))
            print('  → 零 token 候：python3 工具/推.py --候 %s（run_in_background；红／拒／败即早返）' % sha[:12])
            if not os.path.exists(待):
                return 0
        print('⚠ 交了 %d 回仍有待推（提交来得太快）——下回再跑本器' % 最多)
        return 0
    finally:
        锁.close()
        if os.path.exists(待) and 交法 is None:
            return 交(root, 交法, 最多)


def 候(sha, 限分=90, 隔=60, 查=None, 读=None, 进=None, 取=None, 今=time.time, 睡=time.sleep, root=ROOT):
    """零 token 候 GitHub autopush 把 sha 并入主枝。→ 0 主枝已含（已快进）｜3 报红／拒／败（印其红）｜2 逾限。
    ⛔每分逾一取（隔 <60 即作 60）；⛔pgrep／sleep 环之手候（坑⑮）。"""
    import 推报
    全 = _跑(['git', 'rev-parse', '--verify', '-q', sha + '^{commit}'], root).stdout.strip() or sha
    名 = 治名(全)
    隔 = max(60, 隔)
    取 = 取 or (lambda: _取(root))
    查 = 查 or (lambda: 在主(全, root, 取=False))
    读 = 读 or (lambda: 推报.读(名, root, 取=False))
    进 = 进 or (lambda: 推报.快进(root))
    始 = 今()
    while True:
        取()
        if 查():
            ok, 语 = 进()
            print('✓ 主枝已含 %s（%s）' % (全[:12], 名))
            print(语)
            return 0
        d = 读()
        if d and str(d.get('sha') or '').startswith(全[:12]) and 推报.坏(d):        # 1027 坑54：败·重派係在飞——候
            print('\n'.join(推报.报之语(d)))
            if d.get('果') == '拒':
                print('  → 兜底：python3 工具/推.py --直（GITHUB_TOKEN 推不得改 .github/workflows 之提交；本地全闸）')
            elif d.get('果') == '红':
                print('  → 逐红治、提交，再 python3 工具/推.py（⛔绕、⛔弱化）')
            else:
                print('  → 看 run_url；GitHub 停摆即 python3 工具/推.py --直')
            return 3
        if 今() - 始 >= 限分 * 60:
            print('⛔ 候 %d 分主枝未含 %s、亦无其坏报——GitHub 或停摆：python3 工具/推.py --直 兜底' % (限分, 全[:12]))
            return 2
        睡(隔)


def 在推(root=ROOT):
    """有无推送在跑——即本器之锁被占否（⛔pgrep 猜进程名·1027 A2：自进化环 L1 之守取此，旧 pgrep 'git push -u origin' 已认不着本器所起之推）。"""
    try:
        锁 = 取锁(root)
    except OSError:
        return False                               # 锁档开不得（.git 非目录之副本）：本器亦推不得，⛔作在推
    if 锁 is None:
        return True
    锁.close()
    return False


def 状(root=ROOT):
    在跑 = 在推(root)
    print('推送在跑：%s｜本地超前 %d 笔｜待推之记：%s' % (
        '是' if 在跑 else '否', 超前(root), '有' if os.path.exists(os.path.join(_git目录(root), '推.待')) else '无'))


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    os.makedirs(os.path.join(t, '.git'))
    class R:
        def __init__(s, c, o=''): s.returncode, s.stdout, s.stderr = c, o, ''
    # ① 持锁时，第二个取锁者拿不到（⛔靠进程名猜）
    a = 取锁(t); b = 取锁(t)
    共 += 1; ok += (a is not None and b is None and 在推(t) is True)       # ★1027 A2：在推 即锁之态（自进化环 L1 取之）
    # ② 锁被占 → 直推() 立即返回 2 并登记待推，⛔等待
    t0 = time.time(); rc = 直推(t, 推法=lambda: R(0))
    共 += 1; ok += (rc == 2 and os.path.exists(os.path.join(t, '.git', '推.待')) and time.time() - t0 < 2)
    a.close()
    # ③ 锁一放即可取（进程死、锁即放）
    c = 取锁(t); _c在 = c is not None; c.close(); 共 += 1; ok += (_c在 and 在推(t) is False)
    # ④ 被拦不重试：推法只被调一次
    次 = []
    rc = 直推(t, 推法=lambda: (次.append(1), R(1, '  ✗ 某闸\nerror: failed'))[1])
    共 += 1; ok += (rc == 1 and len(次) == 1)
    # ⑤ 推时又有新提交（待推之记）→ 再推一回
    次2 = []
    def 推法2():
        次2.append(1)
        if len(次2) == 1:
            open(os.path.join(t, '.git', '推.待'), 'w').close()
        return R(0)
    global 超前
    旧 = 超前; 超前 = lambda root=ROOT: 0
    try:
        rc = 直推(t, 推法=推法2)
    finally:
        超前 = 旧
    共 += 1; ok += (rc == 0 and len(次2) == 2)
    # ⑥ 远端之状取不到（-1）⛔称推平
    超前 = lambda root=ROOT: -1
    try:
        rc = 直推(t, 推法=lambda: R(0))
    finally:
        超前 = 旧
    共 += 1; ok += (rc == 0)
    # ⑦ 推送逾时 → 返 1、不重试
    def 卡():
        raise subprocess.TimeoutExpired('git push', 1)
    共 += 1; ok += (直推(t, 推法=卡) == 1)
    # ⑧ 心跳章读现挂之章，⛔写死
    import json
    json.dump({'章': 401}, open(os.path.join(t, '_心跳.json'), 'w'))
    共 += 1; ok += (心跳章(t) == 401)
    os.remove(os.path.join(t, '_心跳.json'))
    共 += 1; ok += (心跳章(t) == 0)        # ★1013：撤锁之後读不到 → 0（⛔回 379 凭空造席）
    _u = tempfile.mkdtemp(); os.makedirs(os.path.join(_u, '工具'))
    open(os.path.join(_u, '工具', '改单.py'), 'w').write("print('甲 改了 正文 而无改单'); raise SystemExit(1)")
    open(os.path.join(_u, '工具', '复盘.py'), 'w').write("print('ok')")
    _r = 速检(_u)
    共 += 1; ok += (len(_r) == 1 and '改单' in _r[0] and '而无改单' in _r[0])   # ★1016 速检：红者印其末行，绿者⛔报，缺器⛔跑
    _g = tempfile.mkdtemp()                                                  # ★1022 枝正：游离之 HEAD、枝在其祖 → 挪枝检出
    for _c in (['git', 'init', '-q', '-b', 枝], ['git', 'commit', '-q', '--allow-empty', '-m', 'a'], ['git', 'checkout', '-q', '--detach'],
               ['git', 'commit', '-q', '--allow-empty', '-m', 'b']):
        subprocess.run(_c, cwd=_g, capture_output=True, env=dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t'))
    import io as _io, contextlib as _cl
    with _cl.redirect_stdout(_io.StringIO()):
        _e = 枝正(_g)
    共 += 1; ok += (_e is None and _跑(['git', 'symbolic-ref', '--short', 'HEAD'], _g).stdout.strip() == 枝
                    and _跑(['git', 'log', '-1', '--format=%s', 枝], _g).stdout.strip() == 'b')
    # ★1027 坑51：默交 GitHub（治-<sha12>，pre-push 免闸）、零 token 之候、--直 兜底
    _h = tempfile.mkdtemp()
    for _c in (['git', 'init', '-q', '-b', 枝], ['git', 'commit', '-q', '--allow-empty', '-m', 'a']):
        subprocess.run(_c, cwd=_h, capture_output=True, env=dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t'))
    _sha = _跑(['git', 'rev-parse', 'HEAD'], _h).stdout.strip()
    _名们 = []
    with _cl.redirect_stdout(_io.StringIO()) as _o:
        _rc = 交(_h, 交法=lambda 名: (_名们.append(名), R(0))[1])
    共 += 1; ok += (_rc == 0 and _名们 == ['治-' + _sha[:12]] and 治名(_sha) == _名们[0]
                    and ('python3 工具/推.py --候 %s' % _sha[:12]) in _o.getvalue())       # ⑨交：推 治-<sha12>、印零 token 候之令
    import 推报 as _报
    _免 = _报.暂存之前缀
    共 += 1; ok += ('refs/heads/治-*' in _免 and 'refs/heads/%s' % 枝 not in _免)          # ⑨之二 治枝在钩之免、主枝⛔在（钩之真跑见 推报 --自测）
    _锁 = 取锁(_h)
    with _cl.redirect_stdout(_io.StringIO()):
        _rc = 交(_h, 交法=lambda 名: R(0))
    _锁.close()
    共 += 1; ok += (_rc == 2 and os.path.exists(os.path.join(_h, '.git', '推.待')))           # ⑩交亦守一锁：被占即登记待推、返 2
    os.remove(os.path.join(_h, '.git', '推.待'))
    _次 = []
    with _cl.redirect_stdout(_io.StringIO()):
        _rc = 交(_h, 交法=lambda 名: (_次.append(1), R(1, 'error: 推不上'))[1])
    共 += 1; ok += (_rc == 1 and len(_次) == 1)                                              # ⑪交不成 → 返 1、不重试
    _次 = []
    def _交法2(名):
        _次.append(名)
        if len(_次) == 1:
            open(os.path.join(_h, '.git', '推.待'), 'w').close()
        return R(0)
    with _cl.redirect_stdout(_io.StringIO()):
        _rc = 交(_h, 交法=_交法2)
    共 += 1; ok += (_rc == 0 and len(_次) == 2)                                              # ⑫交时又有新提交 → 再交一回
    # ⑬候：每回一取、第三取主枝含 → 快进、返 0；隔 <60 作 60
    _钟, _取次, _进 = [0.0], [], []
    _序 = iter([False, False, True])
    with _cl.redirect_stdout(_io.StringIO()):
        _rc = 候(_sha, 隔=5, 查=lambda: next(_序), 读=lambda: None, 进=lambda: (_进.append(1), (True, '快进'))[1],
                取=lambda: _取次.append(1), 今=lambda: _钟[0], 睡=lambda x: _钟.__setitem__(0, _钟[0] + x), root=_h)
    共 += 1; ok += (_rc == 0 and _钟[0] == 120 and len(_取次) == 3 and _进 == [1])
    # ⑭候：报红（同 sha）→ 返 3、印其红行；他 sha 之报⛔认；⑮报拒 → 印 --直；⑯逾限 → 返 2、印 --直
    _红 = {'ref': 治名(_sha), 'sha': _sha, '果': '红', '红': ['✗ 质量三闸  红一处', '⛔全测未过：质量三闸'], 'run_url': 'u'}
    _钟[0] = 0.0
    with _cl.redirect_stdout(_io.StringIO()) as _o:
        _rc = 候(_sha, 查=lambda: False, 读=lambda: _红, 进=lambda: (True, ''), 取=lambda: None, 今=lambda: _钟[0],
                睡=lambda x: _钟.__setitem__(0, _钟[0] + x), root=_h)
    共 += 1; ok += (_rc == 3 and _钟[0] == 0 and '✗ 质量三闸  红一处' in _o.getvalue())
    _钟[0] = 0.0
    with _cl.redirect_stdout(_io.StringIO()) as _o:
        _rc = 候(_sha, 限分=3, 查=lambda: False, 读=lambda: dict(_红, sha='0' * 40), 进=lambda: (True, ''), 取=lambda: None,
                今=lambda: _钟[0], 睡=lambda x: _钟.__setitem__(0, _钟[0] + x), root=_h)
    共 += 1; ok += (_rc == 2 and _钟[0] == 180 and '推.py --直' in _o.getvalue())
    with _cl.redirect_stdout(_io.StringIO()) as _o:
        _rc = 候(_sha, 查=lambda: False, 读=lambda: dict(_红, 果='拒', 因='workflow', 红=['⛔拒：改 .github/workflows']), 进=lambda: (True, ''),
                取=lambda: None, 今=lambda: 0, 睡=lambda x: None, root=_h)
    共 += 1; ok += (_rc == 3 and '推.py --直' in _o.getvalue() and 'workflow' in _o.getvalue())
    共 += 1; ok += (候之令(_sha, ['治-x', '章-411']) == 'python3 工具/接棒守.py --候主 411'
                    and 候之令(_sha, ['治-' + _sha[:12]]) == 'python3 工具/推.py --候 ' + _sha[:12]
                    and "if 交法 is None and 在主(sha, root)" in open(os.path.abspath(__file__), encoding='utf-8').read()
                    and "已 = 已交之枝(sha, root) if 交法 is None else []" in open(os.path.abspath(__file__), encoding='utf-8').read())  # ⑯之二 同树已交（章标或治枝）⛔再交、印其候之令
    # ⑰默路交（⛔直推）、--直 方直推、--候 方候；直推仍走闸（⛔--no-verify）
    _主 = open(os.path.abspath(__file__), encoding='utf-8').read().rsplit("if __name__ == '__main__':", 1)[1]
    共 += 1; ok += (_主.rstrip().endswith('rc = 交()\n    sys.exit(0 if rc in (0, 2) else 1)')
                    and "if a == ['--直']:\n        rc = 直推()" in _主 and "if a[:1] == ['--候']" in _主)
    # ⑱候之真取（临时裸库）：云端无 备份/报（首报未推）而主枝已含 → 默之 取／查 照见主枝、返 0（⛔同取全败而候满九十分）
    _r, _c = tempfile.mkdtemp(), tempfile.mkdtemp()
    _e = dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, GIT_CONFIG_GLOBAL=os.devnull,
              GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    for _a, _d in ((['git', 'init', '-q', '--bare', _r], _r), (['git', 'init', '-q', '-b', 枝, _c], _c),
                   (['git', 'commit', '-q', '--allow-empty', '-m', 'a'], _c), (['git', 'remote', 'add', 'origin', _r], _c),
                   (['git', 'push', '-q', 'origin', 'HEAD:refs/heads/' + 枝], _c)):
        subprocess.run(_a, cwd=_d, capture_output=True, env=_e)
    _t = _跑(['git', 'rev-parse', 'HEAD'], _c).stdout.strip()
    _钟[0] = 0.0
    with _cl.redirect_stdout(_io.StringIO()):
        _rc = 候(_t, 限分=3, 读=lambda: None, 进=lambda: (True, ''), 今=lambda: _钟[0],
                睡=lambda x: _钟.__setitem__(0, _钟[0] + x), root=_c)
    共 += 1; ok += (bool(_t) and _rc == 0 and _钟[0] == 0 and _取(_c) is True)
    import shutil as _sh
    _sh.rmtree(_r, ignore_errors=True); _sh.rmtree(_c, ignore_errors=True)
    # ⑲（1027 坑⑱·#41）覆写之检：已入 git 之档一推删八成而换新、说明无「覆写：」→ 红；小改、新档、说明带「覆写：」、器生之档 → 放
    _w = tempfile.mkdtemp()
    _g2 = lambda *a: subprocess.run(['git'] + list(a), cwd=_w, capture_output=True, text=True, env=_e)
    os.makedirs(os.path.join(_w, '工具')); os.makedirs(os.path.join(_w, '设定', '全书记忆'))
    _旧 = ''.join('旧行 %d\n' % i for i in range(60))
    open(os.path.join(_w, '工具', '坑账.py'), 'w', encoding='utf-8').write(_旧)
    open(os.path.join(_w, '工具', '乙.py'), 'w', encoding='utf-8').write(_旧)
    open(os.path.join(_w, '设定', '全书记忆', '剧情链.md'), 'w', encoding='utf-8').write(_旧)
    _g2('init', '-q', '-b', 枝); _g2('add', '-A'); _g2('commit', '-q', '-m', '基')
    _g2('update-ref', 'refs/remotes/origin/' + 枝, 'HEAD')
    open(os.path.join(_w, '工具', '乙.py'), 'w', encoding='utf-8').write(_旧.replace('旧行 3\n', '改行\n'))
    open(os.path.join(_w, '工具', '丙.py'), 'w', encoding='utf-8').write(''.join('新 %d\n' % i for i in range(80)))
    open(os.path.join(_w, '设定', '全书记忆', '剧情链.md'), 'w', encoding='utf-8').write(''.join('重生 %d\n' % i for i in range(60)))
    _g2('add', '-A'); _g2('commit', '-q', '-m', '小改、新档、器生之档')
    _放 = 覆写之检(_w)
    open(os.path.join(_w, '工具', '坑账.py'), 'w', encoding='utf-8').write(''.join('方法坑账 %d\n' % i for i in range(70)))
    _g2('add', '-A'); _g2('commit', '-q', '-m', '立方法坑账')
    _红 = 覆写之检(_w)
    _g2('commit', '-q', '--allow-empty', '-m', '覆写：坑账.py 旧器已改名 写作坑账.py，此处係有意重立')
    _有由 = 覆写之检(_w)
    _sh.rmtree(_w, ignore_errors=True)
    共 += 1; ok += (_放 == [] and len(_红) == 1 and '工具/坑账.py' in _红[0] and '覆写：' in _红[0] and _有由 == [] and 覆写之检(_u) == [])
    # ⑳（1027 #40② #47·坑⑮）费账之检：本会话已毕之 Run 未入费账 → 红、印 费审 --记；在跑之 Run、已记者、无流目 → 放
    _f = tempfile.mkdtemp()
    os.makedirs(os.path.join(_f, '设定'))
    json.dump({'行': [{'键': 'wf_aaaaaaaa-001'}]}, open(os.path.join(_f, '设定', '费账.json'), 'w', encoding='utf-8'))
    _流 = os.path.join(_f, 'wf')
    def _j(rid, 行, 旧=True):
        d = os.path.join(_流, rid); os.makedirs(d)
        open(os.path.join(d, 'journal.jsonl'), 'w').write(''.join(json.dumps({'type': t}) + '\n' for t in 行))
        if 旧:
            os.utime(os.path.join(d, 'journal.jsonl'), (time.time() - 600, time.time() - 600))
    _j('wf_aaaaaaaa-001', ['launched', 'started', 'result'])                 # 已记
    _j('wf_bbbbbbbb-002', ['launched', 'started', 'started', 'result', 'failed'])   # 已毕而未记 → 红
    _j('wf_cccccccc-003', ['launched', 'started', 'started', 'result'], 旧=False)    # 在跑 → 放
    _j('wf_dddddddd-004', ['launched', 'started'])                           # 无果 → 放
    _费 = 费账之检(_f, 流目=_流)
    共 += 1; ok += (len(_费) == 1 and 'wf_bbbbbbbb-002' in _费[0] and 'wf_cccccccc-003' not in _费[0] and 'wf_aaaaaaaa-001' not in _费[0]
                    and 'python3 工具/费审.py --记 wf_bbbbbbbb-002' in _费[0] and 费账之检(_f, 流目='') == [] and 费账之检(_u) == [])
    _sh.rmtree(_f, ignore_errors=True)
    print('推·自测 %d/%d%s' % (ok, 共, ' 全通' if ok == 共 else ' ⛔未过'))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--状']:
        状(); sys.exit(0)
    if a == ['--等']:
        sys.exit(0 if 等() else 1)
    if a[:1] == ['--候'] and len(a) >= 2:
        sys.exit(候(a[1], int(a[2]) if len(a) > 2 and a[2].isdigit() else 90))
    if a == ['--直']:
        rc = 直推()
        sys.exit(0 if rc in (0, 2) else 1)
    if a:
        print(__doc__); sys.exit(2)
    rc = 交()
    sys.exit(0 if rc in (0, 2) else 1)
