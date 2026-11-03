#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""接棒守（1022 立·402 封後无人接棒、书停五时半）——书不停之零 token 三锁之二。

【其由】402 之坐封版时 `心跳.py --跳 403` 自持其锁，写毕交接即收工；Stop 钩（席在跑吗）见「有人在跑」放行——
  那「人」正是它自己。无人开 403 之会话，书停五时半（23:17→04:50），作者醒来自见。
【三锁】
  ①Stop 钩（`工具/席在跑吗.py`）：本坐持写书之锁而手上无席、无後台之活 → 拦（⛔再认己锁作「他人在跑」）。
  ②本器 `--候 N`：交棒者收锁、开新会话之後，後台跑之（零 token）；每分取云端心跳——见第 N 章之锁为他坐所持且新鲜
    → ✓接棒成（rc=0）；逾限（默三十分）无人接 → rc=2，醒交棒者重开。候时 Stop 钩认之放行。
  ③定时之保：守书之会话（小模型）每时被唤一回，跑 `--哨`：有人在写或交棒中即止；停写即开写书之会话（总章三之5）。
用法：
  python3 工具/接棒守.py --候主 403 [分]   # 封版後候主枝含 403（run_in_background；零 token）：0 已含（已快进）｜3 GitHub 报红／拒／败（印其红）｜2 逾限（印 workflow_dispatch 之兜底·⛔沙盒跑闸）
  python3 工具/接棒守.py --候 404 [分]     # 交棒後以 run_in_background 跑
  python3 工具/接棒守.py --在候            # rc=0 在候
  python3 工具/接棒守.py --立守书          # 守书之会话首回立之（⛔写书之坐立之）
  python3 工具/接棒守.py --哨              # 定时之保用：有人在写或交棒中 rc=0；停写 rc=2 并印开写书会话之令
  python3 工具/接棒守.py --派令 404 [--重]  # 交棒：印 create_trigger 之参（run_once_at 已算）；总编辑醒即以其中之参原样 create_session 一回
                                           #   403 未入主枝而其报红／拒／败（或缺章标而 备份/存底 有其封版之提交）→ 自出【重派】之参：自「章-403」（或其源）起、先治（1027 A2）
  python3 工具/接棒守.py --守书之令        # 印守书定时之令所嵌之判令（一行·机器出判「止」／「派 N」；1024）
  python3 工具/接棒守.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, time, json, fcntl, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '工具'))


def _仓目():
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if p:
            return p if os.path.isabs(p) else os.path.join(ROOT, p)
    except Exception:
        pass
    return os.path.join(ROOT, '.git')


锁档 = os.path.join(_仓目(), '接棒守.lock')


def _读锁():
    import 存底
    return 存底._锁()          # (新鲜?, 坐, 章)——⛔另造一把尺


def _我():
    import 心跳
    return 心跳.坐()


def 接了(新鲜, 坐, 章, n, 我):
    """⛔纯判：第 n 章之锁为他坐所持且新鲜 → 接棒成。"""
    try:
        return bool(新鲜 and 坐 and 坐 != 我 and 坐 != '未名' and 章 is not None and int(章) == int(n))
    except (TypeError, ValueError):
        return False


def 候(n, 限分=30, 隔=60, 读=None, 我=None, 今=time.time, 睡=time.sleep):
    读 = 读 or _读锁
    我 = 我 or _我()
    f = open(锁档, 'a+')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('✓接棒守已在候（他一守）——本守即止')
        return 0
    始 = 今()
    while True:
        新鲜, 坐, 章 = 读()
        if 接了(新鲜, 坐, 章, n, 我):
            print('✓接棒成：第%s章之锁已为坐 %s 所持——交棒者可收工' % (n, 坐))
            return 0
        if 今() - 始 >= 限分 * 60:
            print('⛔接棒未成：第%s章 %d 分无人接锁——再跑 `python3 工具/接棒守.py --派令 %s`、照其所印 create_trigger 一回，'
                  '再 `接棒守.py --候 %s`；⛔本坐自写、⛔候人' % (n, 限分, n, n))
            return 2
        睡(隔)


主枝 = 'claude/the-novel-review-4dtuit'
总编辑 = 'session_016Hgfc2SSNvGktFmk2LX825'   # 唯其有 create_session 之器（子会话、定时之令所开之会话俱无——1024 实验）
源 = 'https://github.com/AlienRocketBus/the-novel'


def 务之名(n, 上审=None, 待至=None):
    """第 n 章之会话开头实将做何——只为题名（零 token），令⛔随之变。1024 立：题恒为「第N章」，
    而 411 之会话实做 408—410 之大审，作者见题即疑「怎么开始写 411 了」。"""
    try:
        import 大审
        上 = 上审 if 上审 is not None else ((大审.诸册() or [[0]])[-1][0])
        止 = 大审.到期(int(n) - 1, 上)
    except Exception:
        止 = None
    if not 止:
        return '第%d章' % int(n)
    if 待至 is None:
        try:
            待至 = (json.load(open(os.path.join(ROOT, '设定', '暂停令.json'), encoding='utf-8')).get('待') or {}).get('大审至')
        except Exception:
            待至 = None
    return '大审第%d—%d章（%s）' % (上 + 1, 止, '审毕暂停' if 待至 and int(待至) == 止 else '後接第%d章' % int(n))


def 派之参(n, 重=False, 名=None, 治=None):
    """开第 n 章之会话之 create_session 参——唯此一形（会话之守逐键比之，⛔手拟）。
    治（1027 A2·死锁之治）：前章（n-1）已封而未入主枝、且其报红／拒／败（或缺章标而 备份/存底 有其封版之提交）——
      【重派】之会话自 治（「章-(n-1)」或其治枝、封版之提交之 sha）起（⛔自主枝：主枝无其章），首务治其红；令之首个章号仍係 n（会话之守认之）。"""
    n = int(n)
    if 治:
        令 = ('接《镇冢秘术》第 %d 章之棒（先治第 %d 章：其封版已交而未入主枝——GitHub 之报红／拒／败或缺章标；本会话自「%s」起）：'
              '先 `python3 工具/心跳.py --跳 %d`（被拒即止——他坐已写）、再读总章、跑自走——照其【判】治 治第 %d 章'
              '（红者逐条治、提交、`python3 工具/推.py` 交治枝、`python3 工具/接棒守.py --候主 %d`；⛔绕、⛔弱化），'
              '主枝含第 %d 章後照自走所判续办；末了照总章三之5 接棒；⛔候人' % (n, n - 1, 治, n, n - 1, n - 1, n - 1))
        return {'title': '镇冢秘术·治第%d章（後接第%d章）' % (n - 1, n), 'model': 'claude-opus-5-5', 'source_url': 源,
                'source_revision': 治, 'outcome_branch': 主枝, 'prompt': '【重派】' + 令}
    令 = ('接《镇冢秘术》第 %d 章之棒：先 `python3 工具/心跳.py --跳 %d`（被拒即止——他坐已写）、再读总章、跑自走、'
          '照其所判办（写此章、先大审、或照暂停令停）；末了照总章三之5 接棒；⛔候人' % (n, n))
    return {'title': '镇冢秘术·' + (名 or 务之名(n)), 'model': 'claude-opus-5-5', 'source_url': 源,
            'source_revision': 主枝, 'outcome_branch': 主枝, 'prompt': ('【重派】' if 重 else '') + 令}


def 派令(n, 重=False, 今=time.time, 治=None):
    """交棒之 create_trigger 参（零 token 算好 run_once_at）——总编辑醒来只以其中之参原样 create_session 一回（1024：
    交棒⛔经总编辑另查——锁、暂停、已封、前章入主、重派、参之形俱由会话之守钩验；醒一回由约 $4 降至一呼）。
    治（1027 A2）：前章须治之源（`派令之治` 所判）——即出【重派】自其源起之参。"""
    参 = json.dumps(派之参(n, 重 or bool(治), 治=治), ensure_ascii=False)
    return {'persistent_session_id': 总编辑, 'name': '【派】第%d章%s' % (int(n), '（先治第%d章）' % (int(n) - 1) if 治 else ''),
            'initiation': 'own_followup',
            'run_once_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(int(今()) + 120)),
            'prompt': ('【派】开第 %d 章之写书会话%s：以下参原样调 create_session 一回即毕（会话之守钩自验锁、暂停、已封、前章入主、'
                       '重派与参之形；拦即照其由办），⛔另查、⛔改参：%s' % (int(n), '（重派·自「%s」起、先治第 %d 章）' % (治, int(n) - 1) if 治 else '', 参))}


def 派令之治(n, 主=None, 治=None):
    """`--派令 n` 之判（1027 A2）：前章（n-1）已在主枝 → None（常形）；否则 治之源(n-1)（报坏或缺章标而存底有其封）。读不出 → None（常形·会话之守照拦）。"""
    try:
        if (主 or 主含)(int(n) - 1):
            return None
        return (治 or 治之源)(int(n) - 1)
    except Exception:
        return None


def 主含(n):
    """云端主枝已含第 n 章之封版否（章-n 之标係其封版之提交，为主枝之祖即含）。"""
    def 跑(*a):
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    r = 跑('git', 'ls-remote', 'origin', 'refs/heads/章-%d' % int(n))
    sha = r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else ''
    if not sha:
        return False
    跑('git', 'fetch', '-q', 'origin', 'refs/heads/章-%d' % int(n), 'refs/heads/' + 主枝)
    f = 跑('git', 'ls-remote', 'origin', 'refs/heads/' + 主枝)
    主 = f.stdout.split()[0] if f.returncode == 0 and f.stdout.strip() else ''
    return bool(主) and 跑('git', 'merge-base', '--is-ancestor', sha, 主).returncode == 0


def 治之在飞(标):
    """→ 云端治枝之含 标（章-n 之封版之笔）者 [(枝, sha)]：章红而治推已交、GitHub 未毕——其果当读治枝之报。"""
    r = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-remote', 'origin', 'refs/heads/治-*'], cwd=ROOT, capture_output=True, text=True)
    诸 = [(x.split('refs/heads/', 1)[1], x.split()[0]) for x in r.stdout.split('\n') if 'refs/heads/治-' in x]
    if 诸:
        subprocess.run(['git', 'fetch', '-q', 'origin'] + ['refs/heads/' + 枝 for 枝, _ in 诸], cwd=ROOT, capture_output=True)
    return [(枝, s) for 枝, s in 诸 if subprocess.run(['git', 'merge-base', '--is-ancestor', 标, s], cwd=ROOT,
                                                     capture_output=True).returncode == 0]


def 云端章标(n):
    """→ 云端「章-n」之 sha；无或读不出即 ''。"""
    r = subprocess.run(['git', 'ls-remote', 'origin', 'refs/heads/章-%d' % int(n)], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.split()[0] if r.returncode == 0 and r.stdout.strip() else ''


def 坏报之源(n, 读=None, 标=None, 飞=None):
    """→ (枝, 报) 或 None：GitHub autopush 於 备份/报 之 报/推/章-n.json 之果为红／拒／败、且其 sha 即云端 章-n 之标者。
    章红而含此章之治枝已交（治在飞）：⛔以章之旧红早返——诸治俱有坏报方返其最晚者（枝＝其治枝），有未毕（或已成待并）即 None（候）。"""
    import 推报
    读 = 读 or (lambda 枝: 推报.读(枝, ROOT))
    d = 读('章-%d' % int(n))
    if not 推报.坏(d):                  # 1027 坑54：败·重派係在飞（autopush 已自重派本枝）——候其新跑之报
        return None
    if 标 is None:
        标 = 云端章标(n)
    if 标 and d.get('sha') != 标:
        return None                    # 旧标之报（⛔认他笔之果）
    在飞 = (飞 or 治之在飞)(标 or d.get('sha', ''))
    if 在飞:
        # 治枝红者不删（autopush 只删已并者）：旧治红而新治已交未毕，⛔以旧治之红早返——诸治俱有坏报方返，取其最晚者
        配 = [(枝, x) for x, (枝, s) in zip([读(枝) for 枝, _ in 在飞], 在飞) if x and x.get('sha') == s]
        if len(配) < len(在飞) or any(not 推报.坏(x) for _, x in 配):
            return None                # 治在飞而有未毕者（或已成待并）——候
        return max(配, key=lambda t: str(t[1].get('时') or ''))
    return '章-%d' % int(n), d


def 存底之封(n):
    """→ 云端 备份/存底（及诸坐之旁枝 备份/存底-*）之史里第 n 章封版之提交（「（造式二代·封版#n）」）之 sha；无即 ''。
    （封版之提交已成、「章-n」未推而坐死：存底守五分一存，其存以 HEAD 为父，故封版之提交在存底之史里）"""
    r = subprocess.run(['git', 'ls-remote', 'origin', 'refs/heads/备份/存底*'], cwd=ROOT, capture_output=True, text=True)
    诸 = [x.split()[1] for x in r.stdout.split('\n') if x.strip() and 'refs/heads/备份/存底' in x and '-旧' not in x]
    if not 诸:
        return ''
    subprocess.run(['git', 'fetch', '-q', 'origin'] + ['+%s:refs/remotes/origin/%s' % (x, x[len('refs/heads/'):]) for x in 诸],
                   cwd=ROOT, capture_output=True)
    import 封版                                   # 封版之提交之认：同一把尺（⛔另写）
    return 封版.封之笔(n, ROOT, ['refs/remotes/origin/' + x[len('refs/heads/'):] for x in 诸]) or ''


def 治之源(n, 坏=None, 标=None, 存=None):
    """第 n 章已封而未入主枝、须治（1027 A2·死锁之治：封版之坐死於 GitHub 报红之後，守书【派】n+1 而会话之守拦「第n章未入主枝」，
    无人治 n、书停）——→ 重派之会话之起（source_revision）：①其报红／拒／败 → 「章-n」（或其最晚之坏治枝）；
    ②云端无「章-n」而 备份/存底 之史有其封版之提交 → 其 sha（L0 缺碑自补之、治同上）；余 → ''（候主、⛔重派）。"""
    源 = (坏 or 坏报之源)(n)
    if 源:
        return 源[0]
    if 标 is None:
        标 = 云端章标(n)
    return '' if 标 else ((存 or 存底之封)(n) or '')


def 章之坏报(n, 读=None, 标=None, 飞=None):
    """→ 印之行：GitHub autopush 於 备份/报 之 报/推/章-n.json 之果为红／拒／败、且其 sha 即云端 章-n 之标者；否则 []。
    （1027 坑51：旧候主只问主枝含否，autopush 红了亦白候九十分。读与 推.py --候 同一把尺：推报.读）
    章红而含此章之治枝已交（治在飞）：⛔以章之旧红早返——读治枝之报，坏即返其红、未毕即候（判归 坏报之源）。"""
    import 推报
    源 = 坏报之源(n, 读, 标, 飞)
    if not 源:
        return []
    d = 源[1]
    L = 推报.报之语(d)
    if d.get('果') == '拒':
        L.append('  → 兜底：python3 工具/推.py --直（GITHUB_TOKEN 推不得改 .github/workflows 之提交；本地全闸直推主枝）')
    elif d.get('果') == '红':
        L.append('  → 推闸之红逐条治（⛔绕、⛔弱化）、提交，再 python3 工具/推.py（交 GitHub）→ 其所印 --候；治毕再交棒')
    else:
        L.append('  → 看 run_url；GitHub 停摆即 python3 工具/推.py --直')
    return L


def 候主(n, 限分=90, 隔=120, 查=None, 报=None, 进=None, 今=time.time, 睡=time.sleep):
    """封版之後、交棒之前：候 GitHub autopush 把第 n 章推进主枝（零 token；Stop 钩认本器之进程放行）。
    rc=0 已含→本地快进主枝、即交棒（总章三之5）；rc=3 备份/报 报章-n 红／拒／败→即返其红（⛔白候）；
    rc=2 逾限→印 workflow_dispatch 之兜底（GitHub 再跑 章-n 之闸·零 token）；⛔沙盒跑闸（1027 A2）——其仍无果（GitHub 停摆）方 `推.py --直`（审计·本地全闸）。
    非成之返（3、2）并印 存底包 之令：主枝（阅读器）未含本章，作者手上之书⛔由那道闸说了算（0924 作者令）。主含先问：章已由治推入主即⛔认旧坏报。"""
    查 = 查 or 主含
    报 = 报 or 章之坏报
    if 进 is None:
        import 推报
        进 = lambda: 推报.快进(ROOT)
    始 = 今()
    while True:
        if 查(n):
            print('✓主枝已含第%s章——即照总章三之5 交棒（收锁、开新会话、--候）' % n)
            print(进()[1])
            return 0
        坏 = 报(n)
        if 坏:
            print('\n'.join(坏))
            print('⛔GitHub autopush 未并第%s章（见上）——照其末行办；主枝含之後再交棒' % n)
            print(存底包之语(n))
            return 3
        if 今() - 始 >= 限分 * 60:
            print('⛔主枝 %d 分未含第%s章、亦无其坏报——⛔沙盒跑闸；先 workflow_dispatch 令 GitHub 再跑「章-%s」之闸（零 token）：'
                  '`gh workflow run autopush.yml --ref 章-%s`（或 GitHub 之器 actions_run_trigger：workflow autopush.yml、ref 章-%s），'
                  '再 `python3 工具/接棒守.py --候主 %s`；仍无果（GitHub 停摆）方 `python3 工具/推.py --直`（审计之兜底·本地全闸）；治毕再交棒'
                  % (限分, n, n, n, n, n))
            print(存底包之语(n))
            return 2
        睡(隔)


def 存底包之语(n):
    """候主非成之返（1027 A2）：主枝未含本章，阅读器即无之——存底包打全本单档、SendUserFile 交作者（0924 作者令「推被拦下，存底包照送」）。"""
    return ('· 作者手上之书⛔由那道闸说了算（0924 令）：主枝未含第%s章、阅读器无之——`python3 工具/存底包.py`（全本单档 .txt、正文 .tar.gz、全仓 .bundle），'
            '其印之路以 SendUserFile 交作者（打了⛔送等於没打）；主枝含之後⛔再打' % n)


交棒之宽分 = 30     # 撤锁後此内无人接，作「交棒中」（⛔误判停写而另开一坐）


def 哨判(d, 今, 限):
    """⛔纯判（定时之保用）：云端心跳 d（dict 或 None）→ (rc, 由)。rc=0 有人在写或交棒中｜2 停写。"""
    if not isinstance(d, dict):
        return 2, '⛔停写：心跳读不出或不在'
    try:
        时 = int(d.get('时') or 0)
    except (TypeError, ValueError):
        时 = 0
    分 = (今 - 时) // 60
    if d.get('章') is not None:
        if 今 - 时 <= 限:
            return 0, '✓有人在写：第%s章（坐 %s，%d 分前报到）' % (d.get('章'), str(d.get('坐') or '')[:12], 分)
        return 2, '⛔停写：第%s章之锁 %d 分未续（逾 %d 分）' % (d.get('章'), 分, 限 // 60)
    if 今 - 时 < 交棒之宽分 * 60:
        return 0, '✓交棒中：交第%s章之棒、撤锁 %d 分（宽 %d 分）' % (d.get('毕'), 分, 交棒之宽分)
    return 2, '⛔停写：交第%s章之棒、撤锁已 %d 分无人接' % (d.get('毕'), 分)


# 1024·省审 sessions 二：守书（Haiku）旧自读 JSON、自算 T−J.时、自比 2700／1800——每唤约五调；今由机器一令出判，每唤二调。
#   守书⛔跑仓中脚本（只读之巡），故判式嵌於定时之令之文；其真本在此一处，自测拿 哨判 逐形对之（阈同一把尺：心跳.限、交棒之宽分）。
#   ⛔try（单引号里之 \n 係字面之反斜杠——1024 审实测 SyntaxError、rc=1，二字俱不印）；读坏即 || echo '派 ?'。
#   令文须写明：印出之字不是「止」即作停写（与 哨判 之 fail→2 同）。
守书之判式 = ('''python3 -c "import sys,json,time;j=json.load(sys.stdin);c=j.get('章');d=time.time()-int(j.get('时') or 0);'''
            '''print('止' if (d<=2700 if c is not None else d<1800) else '派 %s'%(c if c is not None else j.get('毕')))"'''
            " || echo '派 ?'")
守书之判令 = 'cd /home/user/the-novel && git fetch -q origin 备份/心跳 && git show origin/备份/心跳:_心跳.json | ' + 守书之判式


def 哨():
    import 心跳
    在, d = 心跳._远()
    rc, 由 = 哨判(d if 在 else None, int(time.time()), 心跳.限)
    print(由)
    if rc:
        N = (d or {}).get('章') or (d or {}).get('毕') if (在 and isinstance(d, dict)) else None
        if not N:
            try:
                import 自走
                N = 自走.末章() + 1
            except Exception:
                N = '?'
        print('  下一章 N=%s' % N)
        print('  → 子会话无开会话之器：`python3 工具/接棒守.py --派令 %s`、照其所印 create_trigger 一回（入总编辑之会话）'
              '→ `python3 工具/接棒守.py --候 %s`（run_in_background）' % (N, N))
    return rc


def 在候():
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


def 自测():
    import tempfile
    global 锁档
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    T('①他坐持第 404 章之鲜锁 → 接了', 接了(True, 'B', 404, 404, 'A'))
    T('①之二 己锁 → ⛔接了（402 之病：己锁当作他人在跑）', not 接了(True, 'A', 404, 404, 'A'))
    T('①之三 锁已陈 → ⛔接了', not 接了(False, 'B', 404, 404, 'A'))
    T('①之四 他坐持前章之锁 → ⛔接了', not 接了(True, 'B', 403, 404, 'A'))
    T('①之五 锁空（章空）、未名之坐 → ⛔接了', not 接了(True, 'B', None, 404, 'A') and not 接了(True, '未名', 404, 404, 'A'))
    旧 = 锁档
    with tempfile.TemporaryDirectory() as d:
        锁档 = os.path.join(d, 'l')
        钟 = [0.0]
        序 = iter([(False, '', None), (True, 'A', 404), (True, 'B', 404)])
        rc = 候(404, 限分=30, 隔=60, 读=lambda: next(序), 我='A', 今=lambda: 钟[0], 睡=lambda s: 钟.__setitem__(0, 钟[0] + s))
        T('②候：锁空 → 己锁 → 他坐接 → rc=0（候了两分）', rc == 0 and 钟[0] == 120)
        钟[0] = 0.0
        rc = 候(404, 限分=30, 隔=60, 读=lambda: (False, '', None), 我='A', 今=lambda: 钟[0], 睡=lambda s: 钟.__setitem__(0, 钟[0] + s))
        T('②之二 三十分无人接 → rc=2（醒交棒者重开）', rc == 2 and 钟[0] == 30 * 60)
        f = open(锁档, 'a+')
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        T('③候时 在候() 为真（Stop 钩认之放行）', 在候())
        T('③之二 已有一守在候 → 再起之守即止（⛔两守）', 候(404, 读=lambda: (False, '', None), 我='A') == 0)
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()
        T('③之三 守毕锁释 → 在候() 为假', not 在候())
    锁档 = 旧
    今, 限 = 100000, 45 * 60
    T('④哨：锁新鲜 → rc=0 有人在写', 哨判({'章': 403, '时': 今 - 600, '坐': 'B'}, 今, 限)[0] == 0)
    T('④之二 锁逾四十五分未续 → rc=2 停写', 哨判({'章': 403, '时': 今 - 46 * 60, '坐': 'B'}, 今, 限)[0] == 2)
    T('④之三 撤锁十分（交棒中）→ rc=0（⛔另开一坐）', 哨判({'章': None, '毕': 403, '时': 今 - 600}, 今, 限)[0] == 0)
    T('④之四 撤锁逾三十分无人接 → rc=2 停写（402 封後书停之形）', 哨判({'章': None, '毕': 402, '时': 今 - 31 * 60}, 今, 限)[0] == 2)
    T('④之五 心跳读不出 → rc=2', 哨判(None, 今, 限)[0] == 2)
    import io, contextlib
    钟 = [0.0]
    序 = iter([False, False, True])
    进了 = []
    无报 = lambda n: []
    with contextlib.redirect_stdout(io.StringIO()):
        rc = 候主(404, 隔=120, 查=lambda n: next(序), 报=无报, 进=lambda: (进了.append(1), (True, '快进'))[1],
                 今=lambda: 钟[0], 睡=lambda x: 钟.__setitem__(0, 钟[0] + x))
    T('⑤候主：第三查含 → rc=0（候了四分）、本地快进一回', rc == 0 and 钟[0] == 240 and 进了 == [1])
    钟[0] = 0.0
    with contextlib.redirect_stdout(io.StringIO()) as o:
        rc = 候主(404, 隔=120, 查=lambda n: False, 报=无报, 进=lambda: (True, ''), 今=lambda: 钟[0], 睡=lambda x: 钟.__setitem__(0, 钟[0] + x))
    T('⑤之二 九十分不含、亦无坏报 → rc=2：先印 workflow_dispatch（⛔沙盒跑闸），GitHub 停摆方 推.py --直；并印存底包（1027 A2）',
      rc == 2 and '推.py --直' in o.getvalue() and 'gh workflow run autopush.yml --ref 章-404' in o.getvalue()
      and o.getvalue().index('workflow run') < o.getvalue().index('推.py --直') and '存底包.py' in o.getvalue())
    # ⑤之三—六 1027 坑51：备份/报 之坏报即早返（⛔白候九十分）；主含先问；旧标之报⛔认
    红报 = {'ref': '章-404', 'sha': 'a' * 40, '果': '红', '红': ['✗ 质量三闸  一章一日', '⛔全测未过：质量三闸'], 'run_url': 'u', '时': 't'}
    钟[0] = 0.0
    with contextlib.redirect_stdout(io.StringIO()) as o:
        rc = 候主(404, 查=lambda n: False, 报=lambda n: 章之坏报(n, 读=lambda 枝: dict(红报), 标='a' * 40, 飞=lambda 标: []), 进=lambda: (True, ''),
                 今=lambda: 钟[0], 睡=lambda x: 钟.__setitem__(0, 钟[0] + x))
    T('⑤之三 报/推/章-N.json 红 → 即 rc=3、印其红行（⛔候）、并印存底包', rc == 3 and 钟[0] == 0 and '✗ 质量三闸  一章一日' in o.getvalue()
      and '存底包.py' in o.getvalue())
    with contextlib.redirect_stdout(io.StringIO()):
        rc = 候主(404, 查=lambda n: True, 报=lambda n: ['⛔红'], 进=lambda: (True, ''), 今=lambda: 0, 睡=lambda x: None)
    T('⑤之四 主枝已含（治推已并）→ rc=0，⛔认旧坏报', rc == 0)
    T('⑤之五 旧标之报（sha 非今之章标）、成报 → ⛔坏', 章之坏报(404, 读=lambda 枝: dict(红报), 标='b' * 40, 飞=lambda 标: []) == []
      and 章之坏报(404, 读=lambda 枝: dict(红报, 果='成', 红=[]), 标='a' * 40) == [] and 章之坏报(404, 读=lambda 枝: None, 标='') == [])
    无飞 = lambda 标: []
    拒 = 章之坏报(404, 读=lambda 枝: dict(红报, 果='拒', 因='workflow', 红=['⛔拒：改 .github/workflows']), 标='a' * 40, 飞=无飞)
    T('⑤之六 拒 → 印 --直 兜底与其由', any('推.py --直' in x for x in 拒) and any('workflow' in x for x in 拒))
    T('⑤之六b 败·重派（1027 坑54：autopush 被拒而已自重派本枝）係在飞 → ⛔坏、照候；败·他因 → 坏',
      章之坏报(404, 读=lambda 枝: dict(红报, 果='败', 因='重派', 红=[]), 标='a' * 40, 飞=无飞) == []
      and bool(章之坏报(404, 读=lambda 枝: dict(红报, 果='败', 因='non-ff', 红=[]), 标='a' * 40, 飞=无飞)))
    诸报 = {'章-404': dict(红报), '治-bbbbbbbbbbbb': None}
    飞 = lambda 标: [('治-bbbbbbbbbbbb', 'b' * 40)] if 标 == 'a' * 40 else []
    候中 = 章之坏报(404, 读=lambda 枝: 诸报.get(枝), 标='a' * 40, 飞=飞)
    诸报['治-bbbbbbbbbbbb'] = dict(红报, ref='治-bbbbbbbbbbbb', sha='b' * 40, 红=['✗ 改单  治推又红'])
    治红 = 章之坏报(404, 读=lambda 枝: 诸报.get(枝), 标='a' * 40, 飞=飞)
    T('⑤之七 章红而含此章之治枝在飞：未毕 → 候（⛔以章之旧红早返）；治报红 → 返治之红', 候中 == [] and any('治推又红' in x for x in 治红)
      and not any('一章一日' in x for x in 治红))
    # ⑤之八 旧治红（其枝不删）而新治已交未毕 → 候（⛔以旧治之红早返）；二治俱红 → 返最晚者之红
    诸报['治-cccccccccccc'] = None
    飞2 = lambda 标: [('治-bbbbbbbbbbbb', 'b' * 40), ('治-cccccccccccc', 'c' * 40)]
    旧红新候 = 章之坏报(404, 读=lambda 枝: 诸报.get(枝), 标='a' * 40, 飞=飞2)
    诸报['治-bbbbbbbbbbbb']['时'] = '2026-10-27T01:00:00Z'
    诸报['治-cccccccccccc'] = dict(红报, ref='治-cccccccccccc', sha='c' * 40, 红=['✗ 新治之红'], 时='2026-10-27T02:00:00Z')
    俱红 = 章之坏报(404, 读=lambda 枝: 诸报.get(枝), 标='a' * 40, 飞=飞2)
    T('⑤之八 旧治红而新治未毕 → 候（⛔以旧治之红早返）；二治俱红 → 返最晚者之红', 旧红新候 == []
      and any('新治之红' in x for x in 俱红) and not any('治推又红' in x for x in 俱红))
    src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    段主含 = src.split('def 主含(')[1].split('\ndef ')[0]
    段候主 = src.split('def 候主(')[1].split('\ndef ')[0]
    T('⑥候主之默认查係 主含、默认报係 章之坏报、默认进係 推报.快进（1022 复核：⛔以注入之假查充其验）',
      '查 = 查 or 主含' in 段候主 and '报 = 报 or 章之坏报' in 段候主 and '推报.快进(ROOT)' in 段候主
      and "推报.读(枝, ROOT)" in src.split('def 坏报之源(')[1].split('\ndef ')[0]
      and '源 = 坏报之源(n, 读, 标, 飞)' in src.split('def 章之坏报(')[1].split('\ndef ')[0])
    # ⑨1027 A2·死锁之治：封版之坐死於 GitHub 报红之後，守书【派】N+1 而会话之守拦「第N章未入主枝」——无人治 N、书停。
    #   治之源：报坏 → 「章-N」（或其最晚之坏治枝）；缺章标而存底有其封 → 其 sha；报未毕／成、或章标在而无坏报 → ''（候主、⛔重派）
    _坏 = lambda 枝: (lambda n: (枝, {'果': '红'}))
    T('⑨治之源：报红 → 章-N；坏在治枝 → 其治枝；缺章标而存底有封 → 其 sha；章标在而报未坏 → 空；俱无 → 空',
      治之源(410, 坏=_坏('章-410')) == '章-410' and 治之源(410, 坏=_坏('治-bbbbbbbbbbbb')) == '治-bbbbbbbbbbbb'
      and 治之源(410, 坏=lambda n: None, 标='', 存=lambda n: 'f' * 40) == 'f' * 40
      and 治之源(410, 坏=lambda n: None, 标='a' * 40, 存=lambda n: 'f' * 40) == ''
      and 治之源(410, 坏=lambda n: None, 标='', 存=lambda n: '') == '')
    _源 = 坏报之源(404, 读=lambda 枝: dict(红报), 标='a' * 40, 飞=lambda 标: [])
    _源治 = 坏报之源(404, 读=lambda 枝: 诸报.get(枝), 标='a' * 40, 飞=飞2)
    T('⑨之二 坏报之源：章红 → (章-N, 报)；二治俱红 → 最晚之治枝；章之坏报只经之（同一把尺）',
      _源 == ('章-404', 红报) and _源治 and _源治[0] == '治-cccccccccccc')
    治参 = 派之参(411, True, 治='章-410')
    T('⑨之三 治之参：自「章-410」起（⛔主枝）、【重派】、令之首个章号仍 411、题名「治第410章」；派令同形且名带「先治」',
      治参['source_revision'] == '章-410' and 治参['outcome_branch'] == 主枝 and 治参['prompt'].startswith('【重派】接《镇冢秘术》第 411 章之棒')
      and 治参['title'] == '镇冢秘术·治第410章（後接第411章）' and '【判】治' in 治参['prompt'] and 'python3 工具/推.py' in 治参['prompt']
      and 派之参(411, False, 治='章-410') == 治参
      and json.loads(派令(411, 今=lambda: 0, 治='章-410')['prompt'].split('⛔改参：', 1)[1]) == 治参
      and '先治第410章' in 派令(411, 今=lambda: 0, 治='章-410')['name'] and '先治' not in 派令(411, 今=lambda: 0)['name'])
    T('⑨之四 --派令 之判：前章已在主 → 常形（⛔查治）；未在主 → 治之源；读崩 → 常形',
      派令之治(411, 主=lambda n: True, 治=lambda n: 1 / 0) is None and 派令之治(411, 主=lambda n: False, 治=lambda n: '章-%d' % n) == '章-410'
      and 派令之治(411, 主=lambda n: 1 / 0) is None and '治 = 派令之治(int(a[i + 1]))' in open(os.path.abspath(__file__), encoding='utf-8').read())
    T('⑥之二 主含真查云端：章-N 之标为主枝之祖', all(k in 段主含 for k in ("'merge-base', '--is-ancestor'", "'refs/heads/章-%d'", 'ls-remote')))
    参 = 派之参(411, 名='第411章')
    T('⑦派之参：题、模、源、枝、令俱定形', 参['title'] == '镇冢秘术·第411章' and 参['model'] == 'claude-opus-5-5'
      and 参['source_revision'] == 参['outcome_branch'] == 主枝 and 'the-novel' in 参['source_url']
      and '第 411 章' in 参['prompt'] and '--跳 411' in 参['prompt'] and not 参['prompt'].startswith('【重派】'))
    T('⑦之二 重派：令首带【重派】、余同', 派之参(411, True, '第411章')['prompt'] == '【重派】' + 参['prompt'])
    T('⑦之五 题名实务：大审到期即名其段（1024 作者疑「怎么开始写 411」）',
      务之名(411, 上审=407, 待至=410) == '大审第408—410章（审毕暂停）' and 务之名(421, 上审=410, 待至=410) == '大审第411—420章（後接第421章）'
      and 务之名(412, 上审=410) == '第412章' and 务之名(411, 上审=410) == '第411章')
    T('⑦之六 令⛔言「写」第 N 章（实务由自走判）', '照其所判办' in 参['prompt'] and not 参['prompt'].startswith('写'))
    令 = 派令(411, 今=lambda: 0)
    T('⑦之三 派令：入总编辑之会话、二分後、令中之参可原样解回', 令['persistent_session_id'] == 总编辑
      and 令['run_once_at'] == '1970-01-01T00:02:00Z' and 令['prompt'].startswith('【派】开第 411 章')
      and json.loads(令['prompt'][令['prompt'].index('{'):]) == 派之参(411))
    T('⑦之四 诸印之令俱指 --派令（⛔手拟【派】）', src.count('--派令 %s') >= 2 and '令「【派】开第' not in src)
    # ⑧1024 守书之判式：真跑於 bash，逐形与 哨判 同判（止＝rc0；派 N＝rc2）；读坏、空入俱「派 ?」；阈与 心跳.限、交棒之宽分 同
    import 心跳
    现 = int(time.time())
    形 = [({'章': '暂停', '时': 4102444800, '坐': '暂停令'}, '止'),
         ({'章': 411, '时': 现 - 600, '坐': 'B'}, '止'), ({'章': 411, '时': 现 - 2800, '坐': 'B'}, '派 411'),
         ({'章': None, '毕': 412, '时': 现 - 600}, '止'), ({'章': None, '毕': 412, '时': 现 - 1900}, '派 412')]
    跑式 = lambda 入: subprocess.run(['bash', '-c', 守书之判式], input=入, capture_output=True, text=True, timeout=30)
    出 = [(跑式(json.dumps(d, ensure_ascii=False)).stdout.strip(), 期, 哨判(d, 现, 心跳.限)[0]) for d, 期 in 形]
    坏 = [跑式(x) for x in ('', '不是 JSON', '{"章": 411, "时": "x"}')]
    T('⑧守书之判式：五形之印与 哨判 同判（止↔rc0、派 N↔rc2；停锁判止）', all(o == 期 and (rc == 0) == (o == '止') for o, 期, rc in 出))
    T('⑧之二 读坏、空入、时坏 → 印「派 ?」且 rc=0（⛔报错无字）', all(p.stdout.strip() == '派 ?' and p.returncode == 0 for p in 坏))
    T('⑧之三 阈同一把尺（2700＝心跳.限、1800＝交棒之宽分）、⛔try、令自云端心跳枝取',
      'd<=2700' in 守书之判式 and 心跳.限 == 2700 and 'd<1800' in 守书之判式 and 交棒之宽分 * 60 == 1800
      and 'try' not in 守书之判式 and '\\n' not in 守书之判式 and 守书之判令.endswith('| ' + 守书之判式)
      and 'git show origin/%s:_心跳.json' % 心跳.枝 in 守书之判令)
    ok = sum(r)
    print('── 负测·接棒守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--立守书' in a:
        # 守书之会话立之（只查、⛔写书）：Stop 钩见之⛔令此坐写书。⛔写书之坐立之——其 Stop 钩之守即失。
        open(os.path.join(_仓目(), '守书.flag'), 'w').write('守书之会话（定时之保）\n')
        print('✓本机立为守书之坐（%s）' % os.path.join(_仓目(), '守书.flag'))
        sys.exit(0)
    if '--守书之令' in a:
        print(守书之判令)
        sys.exit(0)
    if '--派令' in a:
        i = a.index('--派令')
        治 = 派令之治(int(a[i + 1]))        # 1027 A2：前章未入主而报坏（或缺章标而存底有其封）→【重派】自其源起、先治
        令 = 派令(int(a[i + 1]), '--重' in a, 治=治)
        if 治:
            print('⛔ 第%d章未入主枝而须治（源「%s」）——派【重派】之会话自其源起、先治之（会话之守认此形）' % (int(a[i + 1]) - 1, 治))
        print('照下参调 create_trigger 一回（⛔改）：')
        print(json.dumps(令, ensure_ascii=False, indent=1))
        sys.exit(0)
    if '--候主' in a:
        i = a.index('--候主')
        sys.exit(候主(int(a[i + 1]), int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else 90))
    if '--哨' in a:
        sys.exit(哨())
    if '--在候' in a:
        sys.exit(0 if 在候() else 1)
    if '--候' in a:
        i = a.index('--候')
        n = int(a[i + 1])
        分 = int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else 30
        sys.exit(候(n, 分))
    print(__doc__)
    sys.exit(0)
