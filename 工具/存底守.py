#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""存底守（1021 立·402 之失）——容器内後台每五分自存底一回（零 token）；⛔靠主环、⛔靠自走、⛔靠记性。

【其由】402 之坐写了五时半，云端存底一回也无（10:55→16:24）：存底只在开章、封版、自走起 L0 时跑；
  而写书之时主环只候工作流之通知、诸席禁 git 写——没有一样东西触发它。机一被收，五时半之稿全没。
【其法】会话开头之钩跑 `--起`：起一个脱离之後台进程（新 session、flock 唯一），每五分（作者 1021 令：零 token 即五分）：
  ① `存底.存(续心跳=False, 跳同=True)`——树未改即不推；推往何处由 `存底.判底` 定（他坐持写书之锁即己之旁枝，⛔顶）；
  ② 本坐持锁、且十五分内有转录在写（主环或诸席）→ 续本坐之锁（⛔续他坐之锁、⛔复活逾期之锁）——
     旧时诸席禁 git 写、⛔报心跳，写书之中锁逾四十五分即「死」，别坐看来无人在跑。
  最坏只失五分之工。进程随机生灭：机在则守在，机收则同收。日志 `.git/存底守.log`。
用法：
  python3 工具/存底守.py --起     # 钩用：未起则起（已起即免），即返；守书之坐（只读之巡）只印盘坏之哨、⛔承账⛔起守（1027 A2）
  python3 工具/存底守.py --一回   # 跑一回（人手或验用）
  python3 工具/存底守.py --状     # 在跑否、末回何时
  python3 工具/存底守.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, time, json, glob, fcntl, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '工具'))
间 = 5 * 60            # 秒：两回之隔（1021 作者令「不费 token 即五分一回」——纯 git、零 token；树未改即不推）
活界 = 15 * 60         # 秒：转录此内有写即「在干活」


def _仓目():
    """git 之公目（工作副本里 .git 係一档，⛔径接 ROOT/.git——全测之副本即如此）。"""
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if p:
            return p if os.path.isabs(p) else os.path.join(ROOT, p)
    except Exception:
        pass
    return os.path.join(ROOT, '.git')


锁档 = os.path.join(_仓目(), '存底守.lock')
日志 = os.path.join(_仓目(), '存底守.log')


def _记(s):
    try:
        with open(日志, 'a', encoding='utf-8') as f:
            f.write('%s %s\n' % (time.strftime('%m-%d %H:%M:%S', time.gmtime()), s))
    except Exception:
        pass


def 在写(今=None, 界=活界, 根=None):
    """主环或诸席之转录 界 秒内有写否（机器之实，⛔本坐自称）。"""
    今 = 今 or time.time()
    根 = 根 or os.path.expanduser('~/.claude/projects')
    for f in glob.glob(os.path.join(根, '**', '*.jsonl'), recursive=True):
        try:
            if 今 - os.path.getmtime(f) < 界:
                return True
        except OSError:
            pass
    return False


def 该续(鲜, 锁坐, 章, 我坐, 写着, 後台=False):
    """⛔纯判：续锁只续本坐所持、尚新鲜、且真在干活者（0924：替死锁续命，自走永判候；1021：⛔夺他坐之锁）。
    1022（403 封後之假停写）：「干活」兼认流程之後台活（接棒守 --候主／封版／推／全测）——持锁者候 GitHub 推主枝时
    无转录之写，锁遂陈，守书判停写而重派一坐；今候时锁亦续，机死则续断、陈之即真停。"""
    return bool(鲜 and 章 is not None and 锁坐 and 锁坐 == 我坐 and (写着 or 後台))


def _後台():
    try:
        import 席在跑吗
        return bool(席在跑吗.後台之活())
    except Exception:
        return False


def _盘坏(档, 语, rc=1):
    """1024：遇盘坏之迹即立 <git 公目>/盘坏.flag（⛔只入日志——06:25 起每回 add 皆败而无人见）。"""
    try:
        import 重取
        return 重取.查迹(rc, 语, 档)
    except Exception:
        return False


def 一回():
    import 存底, 心跳
    try:
        rc, m = 存底.存('存底守·定时', 续心跳=False, 跳同=True)
    except OSError as e:   # EIO 之读档（版本/ 诸档）直抛於此
        _盘坏('存底守·一回', '%s：%s' % (getattr(e, 'filename', '') or '', e))
        _记('⛔ %s' % e)
        return 2
    if rc:
        _盘坏('存底守·一回', m or '')
    续 = ''
    鲜, 锁坐, 章 = 存底._锁()
    if 该续(鲜, 锁坐, 章, 心跳.坐(), 在写(), _後台()):
        rc2, err = 心跳._写({'章': int(章), '时': int(time.time()), '坐': 锁坐})
        续 = '｜续锁第%s章' % 章 if rc2 == 0 else '｜⛔续锁未成：%s' % err
    _记('%s %s%s' % ('✓' if rc == 0 else '⛔', m, 续))
    return rc


def 在跑():
    try:
        f = open(锁档, 'a+')
    except Exception:
        return False
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(f, fcntl.LOCK_UN)
        return False
    except BlockingIOError:
        return True
    finally:
        f.close()


def 跑():
    f = open(锁档, 'a+')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        return 0                                   # 已有一守在跑
    _记('起 pid %d（每 %d 分一回）' % (os.getpid(), 间 // 60))
    while True:
        time.sleep(间)
        try:
            # 每回另起一进程跑：器一改即下一回生效（⛔守里缓存旧码）；一回崩⛔拖垮守
            p = subprocess.run([sys.executable, os.path.abspath(__file__), '--一回'], cwd=ROOT, timeout=间,
                               stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if p.returncode in (-7, 135):   # 1024：一回之进程死於 SIGBUS——盘坏
                _盘坏('存底守 --一回', 'signal 7', p.returncode)
        except Exception as e:
            _记('⛔一回崩：%s' % e)


def 起(开=subprocess.Popen, 盘=None, 守书=None):
    # 1024 盘坏之哨：SessionStart 之钩跑本器——旗在即首印（零 token；守书之坐亦见）
    try:
        import 重取
        l = (盘 or 重取.印)()
        if l:
            print(l)
    except Exception:
        pass
    # 1027 A2：守书之坐（只读之巡、⛔写书）⛔承账、⛔起守——旧其钩照起，跑账 --承 写 _跑账.json、五分一存推「备份/存底-<守书之坐>」
    try:
        if 守书 is None:
            import 席在跑吗
            守书 = 席在跑吗.守书之坐()
    except Exception:
        守书 = False
    if 守书:
        print('· 守书之坐（只读之巡）：⛔承账、⛔起存底守')
        return 0
    # 1022：会话开头先承云端诸存底之跑账（新机之账空，封版之跑账闸判「从没跑过」而停——404 实踩）；後台、⛔候
    try:
        with open(日志, 'a') as lf:
            开([sys.executable, os.path.join(ROOT, '工具', '跑账.py'), '--承'], cwd=ROOT, stdin=subprocess.DEVNULL,
               stdout=lf, stderr=subprocess.STDOUT, start_new_session=True, close_fds=True)
    except Exception:
        pass
    if 在跑():
        print('✓存底守在跑（每五分自存底·.git/存底守.log）')
        return 0
    with open(日志, 'a') as lf:
        开([sys.executable, os.path.abspath(__file__), '--跑'], cwd=ROOT, stdin=subprocess.DEVNULL,
           stdout=lf, stderr=subprocess.STDOUT, start_new_session=True, close_fds=True)
    print('✓存底守已起（每五分自存底；写书之中本坐之锁自续·.git/存底守.log）')
    return 0


def 状():
    末 = ''
    try:
        末 = open(日志, encoding='utf-8').read().strip().split('\n')[-1]
    except Exception:
        pass
    print('%s 存底守%s｜末行：%s' % ('✓' if 在跑() else '⛔', '在跑' if 在跑() else '未跑', 末 or '（无）'))
    return 0 if 在跑() else 1


def 自测():
    import tempfile
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'p', 's', 'subagents', 'wf_1', 'agent-a.jsonl')
        os.makedirs(os.path.dirname(p))
        open(p, 'w').write('{}')
        今 = time.time()
        os.utime(p, (今 - 60, 今 - 60))
        T('①诸席之转录一分钟前有写 → 在写', 在写(今, 根=d))
        os.utime(p, (今 - 3600, 今 - 3600))
        T('①之二 一时前之转录 → ⛔在写', not 在写(今, 根=d))
    T('②本坐持鲜锁且在写 → 续', 该续(True, 'A', 402, 'A', True))
    T('②之二 他坐之锁 → ⛔续（⛔夺锁）', not 该续(True, 'B', 402, 'A', True))
    T('②之三 逾期之锁 → ⛔续（⛔复活）', not 该续(False, 'A', 402, 'A', True))
    T('②之四 无人在写 → ⛔续（0924：替死锁续命）', not 该续(True, 'A', 402, 'A', False))
    T('②之五 撤过之锁（章空）、未名之坐 → ⛔续', not 该续(True, 'A', None, 'A', True) and not 该续(True, '', 402, '', True))
    T('②之六 本坐持鲜锁、无转录而接棒守／封版在後台 → 续（403 封後候推之假停写）', 该续(True, 'A', 404, 'A', False, True))
    T('②之七 後台在而锁属他坐 → ⛔续', not 该续(True, 'B', 404, 'A', False, True))
    global 锁档, 日志
    旧锁, 旧志 = 锁档, 日志
    with tempfile.TemporaryDirectory() as d:
        锁档, 日志 = os.path.join(d, 'l'), os.path.join(d, 'log')
        起们 = []
        f = open(锁档, 'a+')
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        起(开=lambda *a, **k: 起们.append(a), 守书=False)
        T('③已有一守在跑 → ⛔再起守（唯承账一回）', len(起们) == 1 and '--承' in 起们[0][0] and 在跑())
        起们.clear()
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        起(开=lambda *a, **k: 起们.append(k), 守书=False)
        T('③之二 无守 → 承账一回＋起一守，俱脱离（新 session）、⛔占钩之管', len(起们) == 2 and 起们[-1].get('start_new_session')
          and 起们[-1].get('stdin') == subprocess.DEVNULL and 起们[-1].get('stdout') not in (None, subprocess.PIPE))
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()) as 印:
            起(开=lambda *a, **k: None, 盘=lambda: '⛔ 盘坏：试', 守书=False)
        T('⑦盘坏之旗在 → 会话开头之钩首印其 ⛔ 行（1024）', 印.getvalue().startswith('⛔ 盘坏：试'))
        with contextlib.redirect_stdout(io.StringIO()) as 印:
            起(开=lambda *a, **k: None, 盘=lambda: '', 守书=False)
        T('⑦之二 无旗 ⛔印', '盘坏' not in 印.getvalue())
        起们.clear()
        with contextlib.redirect_stdout(io.StringIO()) as 印:
            _rc = 起(开=lambda *a, **k: 起们.append(a), 盘=lambda: '⛔ 盘坏：试', 守书=True)
        T('⑧守书之坐（只读之巡）→ 盘坏之哨照印，而⛔承账、⛔起守（1027 A2）', _rc == 0 and not 起们
          and 印.getvalue().startswith('⛔ 盘坏：试') and '守书之坐' in 印.getvalue())
    锁档, 日志 = 旧锁, 旧志
    T('⑥锁与日志落 git 之公目（全测之工作副本里 .git 係一档亦通）', 锁档.startswith(_仓目()) and os.path.isdir(_仓目()))
    s = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    T('④一回之存：⛔续心跳（续锁归 该续）、树未改即不推', "存('存底守·定时', 续心跳=False, 跳同=True)" in s)
    T('④之三 每回另起一进程跑（器改即生效、一回崩⛔拖垮守）', "'--一回'], cwd=ROOT, timeout=间" in s)
    段一回 = s.split('def 一回')[1].split('\ndef ')[0]
    T('⑦之三 一回之败（rc≠0、OSError）与子进程死於 SIGBUS 俱问盘坏之迹', "_盘坏('存底守·一回', m or '')" in 段一回
      and 'except OSError' in 段一回 and "_盘坏('存底守 --一回', 'signal 7', p.returncode)" in s)
    T('④之四 一回把後台之活交给该续（1022 复核：删之即复 403 封後之假停写，而旧自测照绿）', '在写(), _後台())' in 段一回)
    try:
        import 席在跑吗
        T('④之五 _後台 真调得着 席在跑吗.後台之活（⛔吞了导入之错而永判无後台）', isinstance(席在跑吗.後台之活('/无此目'), list) and 'import 席在跑吗' in s)
    except Exception as e:
        T('④之五 席在跑吗导入不得：%s' % e, False)
    T('④之二 间係五分（作者 1021 令·零 token）', 间 == 5 * 60)
    try:
        st = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8'))
        cmds = [h.get('command', '') for e in (st.get('hooks') or {}).get('SessionStart', []) for h in e.get('hooks', [])]
        T('⑤会话开头之钩起存底守（每会话即时生效）', any('存底守.py --起' in c for c in cmds))
    except Exception as e:
        T('⑤settings 读不出：%s' % e, False)
    ok = sum(r)
    print('── 负测·存底守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--起' in a:
        sys.exit(起())
    if '--跑' in a:
        sys.exit(跑())
    if '--一回' in a:
        sys.exit(一回())
    sys.exit(状())
