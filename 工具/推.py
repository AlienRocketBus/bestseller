#!/usr/bin/env python3
"""推（1007 立）——推送之唯一入口：一把锁、不排队、不空转、推到底。

为何立：1007 我写了「等前一次推送结束再推」之排队脚本，用 `pgrep -f "git push"` 判「有无推送在跑」，
而排队脚本自己的命令行里就含这几个字——它把自己认成「还有推送在跑」，两个脚本互等，空转一个多小时一次没推。
（教训见 `设定/教训_D6_方法之僵.md` 附「推送之锁」。）

本器之法：
  ① **用文件锁（fcntl.flock，`.git/推.lock`）判「有无推送在跑」**——锁随进程生死，进程一死锁即放；
     ⛔再用 pgrep／ps 去猜进程名（会认错自己）。
  ② 锁被占 → **不排队、不等待**：只在 `.git/推.待` 记一笔「又有新提交要推」，立即返回。
  ③ 持锁者推完一次，若见 `.git/推.待` 或本地仍超前远端 → **再推一次**，直到推平（至多 5 回）。
  ④ 推送被全测拦（失败）→ **不重试、不循环**，印出红的那几项，返回非零——治红是人的事，⛔空转。
  ⑥ 主环等推：`python3 工具/推.py --等`（阻塞取一回锁，推毕即返；⛔pgrep／sleep 轮询——坑⑮）。
  ⑤ 每次推前先跳心跳（防「接力」误红）、先存底（1008：存底环受两时之限与容器重启而死，存底枝旧则推闸之活态之检红）；全程记 `.git/推.log`。

用法：
  python3 工具/推.py            # 推（後台跑亦可：run_in_background）
  python3 工具/推.py --状       # 有无推送在跑、本地超前几笔
  python3 工具/推.py --自测
⛔ZM_SKIP_HOOK、⛔--no-verify：本器只调普通 `git push`，闸照拦。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, fcntl, subprocess, time, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
枝 = 'claude/the-novel-review-4dtuit'


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


def 速检(root=ROOT):
    """→ [红之行]。全测之中最常拦推而只须数秒者——先跑；全测仍是终审（⛔以此代之）。"""
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
    return 红


def 推(root=ROOT, 推法=None, 最多=5):
    """→ 0 推平｜1 被拦｜2 已有人在推（已登记待推）。"""
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
            return 推(root, 推法, 最多)


def 状(root=ROOT):
    锁 = 取锁(root)
    在跑 = 锁 is None
    if 锁:
        锁.close()
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
    共 += 1; ok += (a is not None and b is None)
    # ② 锁被占 → 推() 立即返回 2 并登记待推，⛔等待
    t0 = time.time(); rc = 推(t, 推法=lambda: R(0))
    共 += 1; ok += (rc == 2 and os.path.exists(os.path.join(t, '.git', '推.待')) and time.time() - t0 < 2)
    a.close()
    # ③ 锁一放即可取（进程死、锁即放）
    c = 取锁(t); 共 += 1; ok += (c is not None); c.close()
    # ④ 被拦不重试：推法只被调一次
    次 = []
    rc = 推(t, 推法=lambda: (次.append(1), R(1, '  ✗ 某闸\nerror: failed'))[1])
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
        rc = 推(t, 推法=推法2)
    finally:
        超前 = 旧
    共 += 1; ok += (rc == 0 and len(次2) == 2)
    # ⑥ 远端之状取不到（-1）⛔称推平
    超前 = lambda root=ROOT: -1
    try:
        rc = 推(t, 推法=lambda: R(0))
    finally:
        超前 = 旧
    共 += 1; ok += (rc == 0)
    # ⑦ 推送逾时 → 返 1、不重试
    def 卡():
        raise subprocess.TimeoutExpired('git push', 1)
    共 += 1; ok += (推(t, 推法=卡) == 1)
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
    print('推·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--状']:
        状(); sys.exit(0)
    if a == ['--等']:
        sys.exit(0 if 等() else 1)
    rc = 推()
    sys.exit(0 if rc in (0, 2) else 1)
