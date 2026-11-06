# -*- coding: utf-8 -*-
"""席在跑吗（2026-09-15 立·**律⑰之机化**）——**本坐想收回合的那一刻，由机器拦一次。**

★**其所由来·说实话**：**「不许停」这一条，作者当面说过不止一次；本坐也把它写成了律⑮⑯⑰**，
　**而 0915 当日仍旧停了一回**（333 之席跑完→去补机制→收回合，手上一样在跑的席也没有）。
⛔**故：再写第四条律没有用。**
　**律是本坐自己读、自己守的，而失手的正是本坐**——**一样只靠「我记得」的东西，迟早有一回我不记得。**

★★**其治：把它挪到「我记不记得」之外去。**
　**本器挂作 Stop 钩**（`.claude/settings.json`）：**每一回本坐想收回合，它先跑一遍。**
　**没有席在跑，它就把回合顶回去，并把该跑的那一行命令印在脸上。**
⛔**本器不讲道理、不听解释、不认「我这一回合办了别的正事」**——**律⑰已写死：机制之活排在派席之後。**

★★★**何谓「有席在跑」**：⛔**不自己去读心跳档**——**直接问 `工具/心跳.py`**：
　　**rc=1（「⛔有人在跑」）＝有席**｜**rc=0（「✓无人在跑」）＝没席**。
　**其所以如此**（⛔**本器头一版自破此条，当场记下**）：**心跳不落在工作区，它落在一枝专用之枝 `备份/心跳` 上**；
　**本器头一版去读 `工具/席/_心跳.json`，读不着，於是把「有席在跑」误判成「没席」。**
　★**而器头本已写着「与心跳同一把尺，⛔不另造一把」——头一版写的正是第二把。**
　**故今改为：跑它、认它的 rc，一个数也不自己算。**

**其放行之三种情形**（⛔逐条写明，不许含糊）：
　①**有席在跑**（心跳新鲜）——放行。
　②**全书已完本**（`自走.py` 印得出「完本」之判）——放行。
　③⛔**作者当面叫停**（盘上有 `设定/_作者叫停.flag`）——放行，**而此档只许作者立，本坐不许自立。**

⛔⛔**本器头一回真拦人之实（0916 01:14）与其当场露出的一个洞——一并记在此处，不许只记它成了那一半**：

★**成的那一半**：334 之席回执已交、跑到 v15 而心跳停在 55 分钟前（逾 45 分之限）；
　**本坐本已要收回合，本器把回合顶了回去**，遂接手跑十一轮、裁 `SUS-B`、指 335 开镜卡。
　**那一章若照旧例收了，就烂在那儿。**

⛔**而洞在这里**：**那一席其实没死**——它正在封版／交提那一段长活里，**只是没有再报心跳**；
　**本器据 45 分之限判其死，本坐遂接锁、又派了救章席**——**两席一度并坐。**
　★**此回验过无伤**（白文一字未冲，只有轮记在改），⛔**而「这一回没伤」不等於「安全」。**

★★**其根**：**心跳是「席记得报」才有的东西**；**而封版／交提那一段最长、最不报**——
　**故 45 分之限在那一段上最容易把活人判死。**
⛔**本器不因此放宽那个限**（放宽即回到「停了也没人管」那一边，而那是它要治的病）；
　**其真治在源头：席在封版／交提那一段亦须续报心跳**——**那一改在 `工具/席/一章.js` 之收口段，不在本器。**
　⛔**未办，挂在此处，留与另一轮。**
★★★**在那之前，本器之判须这样读**：**它说「没席在跑」＝「45 分钟没人报到」**，
　**⛔不等於「那一席已经死透」**；**接手之前，先看一眼 `ls -t 版本/第N章/` 之末改时刻——若仍在动，那就是活的。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, json, io, re, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
叫停 = os.path.join(ROOT, '设定', '_作者叫停.flag')


def 问心跳():
    """⛔不另造一把尺：跑 `工具/心跳.py`，认它的 rc 与它印的那一行。
    回 (有没有席, 它印的末一行)。**rc=1 ＝有人在跑｜rc=0 ＝无人在跑。**"""
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '心跳.py')],
                           capture_output=True, text=True, timeout=180)
    except Exception as e:
        return None, '⛔心跳器跑不起来：%s' % e
    行 = [l for l in (r.stdout or '').strip().splitlines() if l.strip()]
    return (r.returncode == 1), (行[-1] if 行 else '')


活之界 = 900   # 秒


def 席之转录在写(界=活之界, 今=None):
    """1013：工作流之席十五分钟内写过其转录 → 有席在跑。回 (有否, 末改之档)。
    ⛔其由：二代（造章.js）之席不报心跳（报心跳要写 git 之枝，席禁 git 写——律⑮），381 跑时心跳逾 45 分即「死」，
    本钩遂把回合一回回顶回去，每回白花一回主环（坑㉔）。转录之末改时刻是机器之实，⛔本坐自称。"""
    import glob as _g
    今 = 今 or time.time()
    fs = _g.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/wf_*/agent-*.jsonl'))
    新 = [f for f in fs if 今 - os.path.getmtime(f) < 界]
    return (bool(新), max(新, key=os.path.getmtime) if 新 else '')


def 暂停令在():
    """盘上之暂停令（工具/暂停令.py·坑⑭）在否——与 自走.py、接力同认一处。读不出即作「不在」（照旧拦）。"""
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 暂停令
        return 暂停令.在(ROOT)
    except Exception:
        return False, ''


def 完本了吗():
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '自走.py')],
                             capture_output=True, text=True, timeout=120).stdout
        return ('完本' in out), out
    except Exception:
        return False, ''


def 锁之档():
    """→ 云端心跳之 dict（读不出作 None）。"""
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 心跳
        在, d = 心跳._远()
        if 在 and isinstance(d, dict):
            return d
    except Exception:
        pass
    return None


def 锁之主(d=None):
    """→ (锁坐, 锁章)：云端心跳之锁为谁所持。读不出作 ('', None)。"""
    d = d if d is not None else 锁之档()
    if isinstance(d, dict):
        return str(d.get('坐') or ''), d.get('章')
    return '', None


交棒之宽 = 30 * 60    # 秒：撤锁後此内作「交棒中」（与 接棒守.交棒之宽分 同）


def 交棒之状(d, 今=None):
    """→ (交棒中?, 撤锁者, 毕章)：锁空而撤锁未满三十分。"""
    今 = 今 or time.time()
    if isinstance(d, dict) and d.get('章') is None:
        try:
            if 今 - int(d.get('时') or 0) < 交棒之宽:
                return True, str(d.get('坐') or ''), d.get('毕')
        except (TypeError, ValueError):
            pass
    return False, '', None


def 我之坐():
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 心跳
        return 心跳.坐()
    except Exception:
        return '未名'


後台之器 = ('工具/封版.py', '工具/推.py', '工具/全测.py', '工具/全测并.py', '工具/接棒守.py')   # 1022：⛔认裸 git push（存底守五分一推）


def 流在跑(根=None, 今=None, 界=30 * 60):
    """1022：本机有无「真在跑」之工作流——journal 之 started 多於 result，且其目三十分内有写（长思逾十分亦认；
    崩而留半之 journal 三十分後即不认）。⛔以「十五分内有转录写过」充之：流毕之後十五分，持锁者遂得闲收（复核所逮）。"""
    import glob as _g, json as _j
    今 = 今 or time.time()
    根 = 根 or os.path.expanduser('~/.claude/projects')
    for jf in _g.glob(os.path.join(根, '*', '*', 'subagents', 'workflows', 'wf_*', 'journal.jsonl')):
        d = os.path.dirname(jf)
        try:
            新 = max(os.path.getmtime(os.path.join(d, x)) for x in os.listdir(d))
        except (OSError, ValueError):
            continue
        if 今 - 新 > 界:
            continue
        起 = 果 = 0
        try:
            for l in open(jf, encoding='utf-8'):
                t = (_j.loads(l) or {}).get('type')
                起 += t == 'started'
                果 += t == 'result'
        except Exception:
            continue
        if 起 > 果:
            return True
    return False


守书之号 = ('01HCXDm7LtSf4nECX75WCL3D', '01BFuD1GJM5avGrcaUg1REwV')   # 守书之会话（定时之保·小模型·只查⛔写）；换坐即改此行
守书之令 = 'trig_01Y4mtqtyshYjTb6wkDGdnzP'   # 唤守书之定时之令（每时 :42）——暂停令·守书之参 取此，⛔另硬写；换令即改此行


def 守书开头之判(坐, 守):
    """⛔纯判（SessionStart 之钩用）：守书之坐方⛔灌总章。1024 实见：总编辑之机之公目里有 10-22 05:32 之 守书.flag
    （立守书时误立於总编辑之机），单认旗即令总编辑每回开头失其总章——故总编辑之坐（接棒守.总编辑）一律作非守书。"""
    try:
        import 接棒守
        总 = 接棒守.总编辑
    except Exception:
        总 = 'session_016Hgfc2SSNvGktFmk2LX825'
    号 = lambda s: str(s or '').replace('session_', '').replace('cse_', '')
    return bool(守) and 号(坐) != 号(总)


def 守书之坐():
    """守书之会话（定时之保·只查与派、⛔写书）——本钩⛔令其写书。认其坐号（守书之号），或其机之 <git 公目>/守书.flag。"""
    if 我之坐() in 守书之号:
        return True
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        gd = p if os.path.isabs(p) else os.path.join(ROOT, p or '.git')
        return os.path.exists(os.path.join(gd, '守书.flag'))
    except Exception:
        return False


def 後台之活(根='/proc'):
    """本机有无流程之後台活（封版 --後、推、全测、git push、接棒守 --候）——候其通知係正当之候，⛔拦。"""
    在 = []
    try:
        for pid in os.listdir(根):
            if not pid.isdigit() or int(pid) == os.getpid():
                continue
            try:
                c = open(os.path.join(根, pid, 'cmdline'), 'rb').read().replace(b'\0', b' ').decode('utf-8', 'ignore')
            except Exception:
                continue
            for k in 後台之器:
                if k in c and '--自测' not in c:
                    在.append(k)
    except Exception:
        pass
    return sorted(set(在))


def 判路(叫停=False, 暂停=False, 有席=False, 锁坐='', 我坐='', 转录活=False, 後台活=False, 完本=False,
        交棒中=False, 撤锁者='', 流活=False, 守书=False):
    """⛔纯判（main 只走此一条路）：回 (rc, 由)。rc=0 放行｜2 拦（无席）｜3 拦（己持锁而闲）｜4 拦（己撤锁而未候接棒）。"""
    if 叫停:
        return 0, '叫停'
    if 暂停:
        return 0, '暂停令'
    if 守书:
        return 0, '守书之坐（只查、⛔写书）'
    己 = bool(我坐) and 我坐 != '未名'
    if 有席 and 己 and 锁坐 == 我坐:
        # ★1022（402 封後书停五时半）：锁为本坐所持——唯真在跑之工作流或流程之後台活方许收；
        #   ⛔以「十五分内有转录写过」充之（复核所逮：流毕之後十五分，持锁者得闲收，书停至定时之保）。
        if 流活 or 後台活:
            return 0, '己锁·流或後台在跑'
        return 3, '己持锁而闲'
    if 转录活:
        return 0, '转录在写'
    if 後台活:
        return 0, '後台之活'
    if 有席:
        return 0, '他坐在跑'
    if 己 and 撤锁者 == 我坐:
        # ★1022：锁空而撤者係本坐——交了棒须候人接住（接棒守 --候 在跑即上一条放行）；⛔限三十分（复核所逮：候逾时醒来即被令自写）
        return 4, '己撤锁而未候接棒'
    if 交棒中:
        return 0, '交棒中'
    if 完本:
        return 0, '完本'
    return 2, '无席'


def main():
    if os.path.exists(叫停):
        print('✓席在跑吗：作者已叫停（设定/_作者叫停.flag 在盘上）——放行。')
        return 0
    # ★1017（坑⑭复踩：作者令「大审毕即暂停」已立於盘上之暂停令，自走.py 判「停」，而本钩不认，逼派 398）：暂停令在即放行
    在停, 停由 = 暂停令在()
    if 在停:
        print('✓席在跑吗：%s——放行（⛔派席；作者令下方 `python3 工具/暂停令.py --解`）。' % 停由[:120])
        return 0
    有席, 行 = 问心跳()
    锁 = 锁之档()
    锁坐, 锁章 = 锁之主(锁) if 有席 else ('', None)
    交, _, 毕章 = (False, '', None) if 有席 else 交棒之状(锁)
    撤者 = str(锁.get('坐') or '') if (not 有席 and isinstance(锁, dict) and 锁.get('章') is None) else ''
    毕章 = 毕章 if 毕章 is not None else (锁.get('毕') if isinstance(锁, dict) else None)
    转, 档 = 席之转录在写()
    後 = 後台之活()
    流 = 流在跑()
    rc, 由 = 判路(有席=有席, 锁坐=锁坐, 我坐=我之坐(), 转录活=转, 後台活=bool(後), 交棒中=交, 撤锁者=撤者,
                流活=流, 守书=守书之坐(),
                完本=(False if (有席 or 转 or 後 or 交) else 完本了吗()[0]))
    if rc == 0:
        print('✓席在跑吗：%s——放行。%s' % (由, ('（%s）' % '、'.join(後)) if 後 else ''))
        if 行:
            print('   心跳印：%s' % 行)
        return 0
    if rc == 4:
        print('⛔⛔⛔ 席在跑吗：**本坐已撤锁、交第%s章之棒，而无人接住、本坐亦未候——⛔交了棒不看就收工**（1022）。' % 毕章, file=sys.stderr)
        print('   跑 `python3 工具/接棒守.py --候 %s`（run_in_background）；候逾时则再跑 `python3 工具/接棒守.py --派令 %s`、'
              '照其所印 create_trigger 一回，再候。⛔本坐自写（防两坐同写）。' % (毕章, 毕章), file=sys.stderr)
        return 2
    if rc == 3:
        _o = sys.stdout
        sys.stdout = sys.stderr
        try:
            print('⛔⛔⛔ 席在跑吗：**本坐持第%s章之锁，而手上无席、无後台之活——收了，书就停**（1022·402 封後书停五时半之形）。' % 锁章)
            print('   ①第%s章未写：跑 `cd /home/user/the-novel && python3 工具/自走.py`，照其令派席。' % 锁章)
            print('   ②上一章已封、第%s章该由新会话写（总章三之5 接棒）：' % 锁章)
            print('      `python3 工具/接棒守.py --候主 %s`（run_in_background；报主枝已含方续）→ `python3 工具/心跳.py --收 %s` → '
                  '`python3 工具/接棒守.py --派令 %s`、照其所印 create_trigger 一回 → `python3 工具/接棒守.py --候 %s`（run_in_background）。⛔候人。'
                  % ((锁章 or 1) - 1 if str(锁章).isdigit() else 锁章, 锁章, 锁章, 锁章))
        finally:
            sys.stdout = _o
        return 2
    # ⛔拦（★印到 stderr：Stop 钩只把 stderr 给模型——1013 实踩，印在 stdout 则模型只见「No stderr output」）
    _o = sys.stdout
    sys.stdout = sys.stderr
    try:
        print('⛔⛔⛔ 席在跑吗：**手上没有一样在跑的席——这一回合还没完，不许收。**')
        print('   心跳印：%s' % (行 or '（心跳器无话）'))
        print('')
        print('★**律⑰**：席一收，头一件事只有一件——**跑 `自走.py`，照它印的那一行派下一席**。')
        print('　**机制之活、补账之活、治闸之活，一律排在「席已起、Run ID 已回」之後。**')
        print('')
        print('── 现在就跑这一条 ──')
        print('   cd /home/user/the-novel && python3 工具/自走.py')
        print('　★它印「起」→ 逐条照抄跑完，末一条 `Workflow(...)`（造章.js——照自走所印；一代 一章.js 已淘汰）')
        print('　★它印「候」→ 说明另有席在跑；若心跳已死而它仍印「候」，跑 `python3 工具/心跳.py --跳 N` 接手')
        print('⛔**「我现在开它」这六个字不算派席——须回了 Run ID 才算。**')

    finally:
        sys.stdout = _o
    return 2


def 自测():
    """⛔本器之自测不碰真心跳（那会扰正在跑的席）——只钉死「三条放行之路」与「一条拦」。"""
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))

    def 判(有席, 有叫停, 完本, 转录活=False, 暂停=False):
        """⛔不另写一份：直调 main 所走之 判路（他坐之锁）。"""
        return 判路(叫停=有叫停, 暂停=暂停, 有席=有席, 锁坐='B', 我坐='A', 转录活=转录活, 完本=完本)[0]

    报('①有席即放行', 判(True, False, False), 0)
    报('②⛔无席即拦', 判(False, False, False), 2)
    报('③完本即放行', 判(False, False, True), 0)
    报('④作者叫停即放行', 判(False, True, False), 0)
    # ⑤★叫停之权在作者，不在本坐：本器只认那一档在不在，⛔不自立
    报('⑤叫停压过无席', 判(False, True, False), 0)
    # ⑥⛔「有席」不许由本坐自称：其据只认 心跳.py 之 rc
    import inspect
    src = inspect.getsource(问心跳)
    报('⑥其据只认心跳之rc', ('心跳.py' in src) and ('returncode == 1' in src), True)
    # ⑦⛔不许自己去读心跳档（头一版之病：心跳不在工作区，读不着即误判无席）
    报('⑦不自读心跳档', '_心跳.json' not in src, True)

    报('⑧二代之席不报心跳而转录在写即放行', 判(False, False, False, True), 0)
    import tempfile as _t
    _d = _t.mkdtemp(); _f = os.path.join(_d, 'a.jsonl'); open(_f, 'w').write('x')
    报('⑨转录之活以末改时刻判（十五分钟之界）', (time.time() - os.path.getmtime(_f) < 活之界, time.time() + 2 * 活之界 - os.path.getmtime(_f) < 活之界), (True, False))
    import shutil as _sh; _sh.rmtree(_d)
    src2 = inspect.getsource(main)
    报('⑩拦时印到 stderr', 'sys.stdout = sys.stderr' in src2, True)
    报('⑪盘上暂停令在即放行（坑⑭：与自走、接力同认）', 判(False, False, False, False, True), 0)
    报('⑪之二·main 真调暂停令之判', '暂停令在()' in src2 and 'import 暂停令' in inspect.getsource(暂停令在), True)
    # ⑫—⑮·1022（402 封後书停五时半）：己持锁而闲即拦；後台之活、他坐之锁放行
    报('⑫己持锁、无席无後台 → 拦（rc=3）', 判路(有席=True, 锁坐='A', 我坐='A')[0], 3)
    报('⑫之二 他坐持锁 → 放行', 判路(有席=True, 锁坐='B', 我坐='A')[0], 0)
    报('⑫之三 己持锁而工作流真在跑 → 放行', 判路(有席=True, 锁坐='A', 我坐='A', 流活=True)[0], 0)
    报('⑫之四 己持锁、只十五分内有转录（流已毕）→ 拦（复核所逮）', 判路(有席=True, 锁坐='A', 我坐='A', 转录活=True)[0], 3)
    报('⑬己持锁而封版／推／接棒守在後台 → 放行', 判路(有席=True, 锁坐='A', 我坐='A', 後台活=True)[0], 0)
    报('⑬之二 已收锁而接棒守在候 → 放行', 判路(有席=False, 後台活=True)[0], 0)
    报('⑭未名之坐（旧锁）⛔认作己锁', 判路(有席=True, 锁坐='未名', 我坐='未名')[0], 0)
    报('⑮main 只走 判路、真认後台与锁主', '判路(' in src2 and '後台之活()' in src2 and '锁之主(' in src2 and '交棒之状(' in src2, True)
    报('⑰他坐撤锁未满三十分（交棒中）→ 放行（守书之会话⛔误起一坐）', 判路(交棒中=True, 撤锁者='B', 我坐='A')[0], 0)
    报('⑰之二 己撤锁而未候接棒 → 拦（rc=4）', 判路(交棒中=True, 撤锁者='A', 我坐='A')[0], 4)
    报('⑰之三 己撤锁而接棒守在候 → 放行', 判路(交棒中=True, 撤锁者='A', 我坐='A', 後台活=True)[0], 0)
    报('⑰之四 己撤锁逾三十分（候已逾时）→ 仍 rc=4（⛔令其自写）', 判路(交棒中=False, 撤锁者='A', 我坐='A')[0], 4)
    报('⑲守书之坐 → 放行（⛔令其写书）', 判路(守书=True)[0], 0)
    报('⑲之二 开头之判：守书之坐 → 是；总编辑之坐虽有旗 → 否（1024）；非守书 → 否',
       (守书开头之判('01HCXDm7LtSf4nECX75WCL3D', True), 守书开头之判('016Hgfc2SSNvGktFmk2LX825', True),
        守书开头之判('cse_016Hgfc2SSNvGktFmk2LX825', True), 守书开头之判('X', False)), (True, False, False, False))
    try:   # 1024·省审 sessions 二②：SessionStart 印总章之钩加括号之判（A || B && C 实为 (A||B)&&C，⛔裸加）；坐号⛔硬写进 settings
        _st = open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8').read()
        _c = [h.get('command', '') for e in (json.loads(_st).get('hooks') or {}).get('SessionStart', [])
              for h in e.get('hooks', []) if '00_总章.md' in h.get('command', '')]
        报('⑲之三 开头之钩：{ 守书之判 ; } || { …cat 总章… ; }、坐号⛔入 settings',
           (len(_c) == 1 and _c[0].startswith('{ python3 /home/user/the-novel/工具/席在跑吗.py --守书之坐') and ' ; } || { ' in _c[0]
            and _c[0].rstrip().endswith('; }'), any(x in _st for x in 守书之号)), (True, False))
        # 1106·坑57：钩之输出逾限即被截、醒来只见前二千字——钩只印总章首段（至「## 一、」），首段须含痛之录且 ≤五千字
        _t = open(os.path.join(ROOT, '00_总章.md'), encoding='utf-8').read()
        _h = re.split(r'(?m)^## 一、', _t, maxsplit=1)[0]
        报('⑲之四 开头之钩只印总章首段（awk 至「## 一、」）、首段含痛之录且 ≤5000 字（今 %d）' % len(_h),
           (len(_c) == 1 and "awk '/^## 一、/{exit}1' 00_总章.md" in _c[0] and 'cat 00_总章.md' not in _c[0],
            '**痛之录' in _h, len(_h) <= 5000), (True, True, True))
        # 1106 作者令「每次在开写的时候你也要读到，并且要严格执行起来」：开写三纲（唯一之的→第一律·自决→六大主义）俱在首段、依此序，自决以二者为裁之尺
        _i = [_h.find(k) for k in ('**开写三纲', '**★唯一之的**', '**★第一律·自决', '**★六大主义')]
        _z = _h[_i[2]:_i[3]] if -1 not in _i else ''
        报('⑲之五 首段带开写三纲：唯一之的→第一律·自决→六大主义依序；自决除作者之令外一切自决、以唯一之的与六大主义为裁之尺',
           (-1 not in _i and _i == sorted(_i), '除作者亲下之令' in _z and '唯一之的' in _z and '六大主义' in _z), (True, True))
    except Exception as e:
        报('⑲之三 settings 读不出：%s' % e, False, True)
    import json as _jj
    _w = __import__('tempfile').mkdtemp(); _d = os.path.join(_w, 'p', 's', 'subagents', 'workflows', 'wf_1'); os.makedirs(_d)
    open(os.path.join(_d, 'journal.jsonl'), 'w').write(_jj.dumps({'type': 'started'}) + '\n')
    报('⑳流在跑：started 多於 result、目新 → 是', 流在跑(_w), True)
    open(os.path.join(_d, 'journal.jsonl'), 'a').write(_jj.dumps({'type': 'result'}) + '\n')
    报('⑳之二 started＝result（流毕）→ 否', 流在跑(_w), False)
    open(os.path.join(_d, 'journal.jsonl'), 'a').write(_jj.dumps({'type': 'started'}) + '\n')
    报('⑳之三 半崩之 journal 逾三十分无写 → 否', 流在跑(_w, 今=time.time() + 31 * 60), False)
    _sh.rmtree(_w)
    报('㉑後台之器⛔认裸 git push（存底守五分一推）', 'git push' in 後台之器, False)
    _今 = 100000
    报('⑱交棒之状：撤锁十分 → 交棒中', 交棒之状({'章': None, '毕': 403, '时': _今 - 600, '坐': 'A'}, _今)[0], True)
    报('⑱之二 撤锁逾三十分 → ⛔交棒中（停写，归定时之保）', 交棒之状({'章': None, '毕': 403, '时': _今 - 1900}, _今)[0], False)
    报('⑱之三 锁在（章非空）→ ⛔交棒中', 交棒之状({'章': 404, '时': _今}, _今)[0], False)
    import tempfile as _t2
    _p = _t2.mkdtemp()
    for _pid, _c in (('11', b'python3\0/x/\xe5\xb7\xa5\xe5\x85\xb7/\xe5\xb0\x81\xe7\x89\x88.py\0601\0--\xe5\xbe\x8c'), ('12', b'sleep\0' + b'9')):
        os.makedirs(os.path.join(_p, _pid)); open(os.path.join(_p, _pid, 'cmdline'), 'wb').write(_c)
    报('⑯後台之活：/proc 之 cmdline 认得 封版.py', 後台之活(_p), ['工具/封版.py'])
    _sh.rmtree(_p)
    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 席在跑吗·自测 %d/%d%s' % ('✓' if 过 == len(格) else '⛔', 过, len(格), ' 全通' if 过 == len(格) else ' 未过'))
    return 0 if 过 == len(格) else 1


if __name__ == '__main__':
    if '--守书之坐' in sys.argv:   # 1024：SessionStart 之钩用——守书之坐 rc=0（其钩⛔灌总章约 8K 之字）；余 rc=1。⛔把坐号硬写进 settings
        sys.exit(0 if 守书开头之判(我之坐(), 守书之坐()) else 1)
    sys.exit(自测() if '--自测' in sys.argv else main())
