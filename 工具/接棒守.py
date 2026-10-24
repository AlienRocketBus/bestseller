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
  python3 工具/接棒守.py --候主 403 [分]   # 封版後候主枝含 403（run_in_background；零 token）
  python3 工具/接棒守.py --候 404 [分]     # 交棒後以 run_in_background 跑
  python3 工具/接棒守.py --在候            # rc=0 在候
  python3 工具/接棒守.py --立守书          # 守书之会话首回立之（⛔写书之坐立之）
  python3 工具/接棒守.py --哨              # 定时之保用：有人在写或交棒中 rc=0；停写 rc=2 并印开写书会话之令
  python3 工具/接棒守.py --派令 404 [--重]  # 交棒：印 create_trigger 之参（run_once_at 已算）；总编辑醒即以其中之参原样 create_session 一回
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


def 派之参(n, 重=False):
    """开第 n 章写书会话之 create_session 参——唯此一形（会话之守逐键比之，⛔手拟）。"""
    n = int(n)
    令 = ('写《镇冢秘术》第 %d 章：先 `python3 工具/心跳.py --跳 %d`（被拒即止——他坐已写）、再读总章、跑自走、照办；'
          '末了照总章三之5 接棒；⛔候人' % (n, n))
    return {'title': '镇冢秘术·第%d章' % n, 'model': 'claude-opus-5-5', 'source_url': 源,
            'source_revision': 主枝, 'outcome_branch': 主枝, 'prompt': ('【重派】' if 重 else '') + 令}


def 派令(n, 重=False, 今=time.time):
    """交棒之 create_trigger 参（零 token 算好 run_once_at）——总编辑醒来只以其中之参原样 create_session 一回（1024：
    交棒⛔经总编辑另查——锁、暂停、已封、前章入主、重派、参之形俱由会话之守钩验；醒一回由约 $4 降至一呼）。"""
    参 = json.dumps(派之参(n, 重), ensure_ascii=False)
    return {'persistent_session_id': 总编辑, 'name': '【派】第%d章' % int(n), 'initiation': 'own_followup',
            'run_once_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(int(今()) + 120)),
            'prompt': ('【派】开第 %d 章之写书会话：以下参原样调 create_session 一回即毕（会话之守钩自验锁、暂停、已封、前章入主、'
                       '重派与参之形；拦即照其由办），⛔另查、⛔改参：%s' % (int(n), 参))}


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


def 候主(n, 限分=90, 隔=120, 查=None, 今=time.time, 睡=time.sleep):
    """封版之後、交棒之前：候 GitHub autopush 把第 n 章推进主枝（零 token；Stop 钩认本器之进程放行）。
    rc=0 已含→即交棒（总章三之5）；rc=2 逾限→跑 `python3 工具/推.py` 兜底、逐红治。"""
    查 = 查 or 主含
    始 = 今()
    while True:
        if 查(n):
            print('✓主枝已含第%s章——即照总章三之5 交棒（收锁、开新会话、--候）' % n)
            return 0
        if 今() - 始 >= 限分 * 60:
            print('⛔主枝 %d 分未含第%s章——跑 `python3 工具/推.py` 兜底、推闸之红逐条治；治毕再交棒' % (限分, n))
            return 2
        睡(隔)


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
    钟 = [0.0]
    序 = iter([False, False, True])
    T('⑤候主：第三查含 → rc=0（候了四分）', 候主(404, 隔=120, 查=lambda n: next(序), 今=lambda: 钟[0], 睡=lambda x: 钟.__setitem__(0, 钟[0] + x)) == 0 and 钟[0] == 240)
    钟[0] = 0.0
    T('⑤之二 九十分不含 → rc=2（推.py 兜底）', 候主(404, 隔=120, 查=lambda n: False, 今=lambda: 钟[0], 睡=lambda x: 钟.__setitem__(0, 钟[0] + x)) == 2)
    src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    段主含 = src.split('def 主含(')[1].split('\ndef ')[0]
    段候主 = src.split('def 候主(')[1].split('\ndef ')[0]
    T('⑥候主之默认查係 主含（1022 复核：⛔以注入之假查充其验）', '查 = 查 or 主含' in 段候主)
    T('⑥之二 主含真查云端：章-N 之标为主枝之祖', all(k in 段主含 for k in ("'merge-base', '--is-ancestor'", "'refs/heads/章-%d'", 'ls-remote')))
    参 = 派之参(411)
    T('⑦派之参：题、模、源、枝、令俱定形', 参['title'] == '镇冢秘术·第411章' and 参['model'] == 'claude-opus-5-5'
      and 参['source_revision'] == 参['outcome_branch'] == 主枝 and 'the-novel' in 参['source_url']
      and '第 411 章' in 参['prompt'] and '--跳 411' in 参['prompt'] and not 参['prompt'].startswith('【重派】'))
    T('⑦之二 重派：令首带【重派】、余同', 派之参(411, True)['prompt'] == '【重派】' + 参['prompt'])
    令 = 派令(411, 今=lambda: 0)
    T('⑦之三 派令：入总编辑之会话、二分後、令中之参可原样解回', 令['persistent_session_id'] == 总编辑
      and 令['run_once_at'] == '1970-01-01T00:02:00Z' and 令['prompt'].startswith('【派】开第 411 章')
      and json.loads(令['prompt'][令['prompt'].index('{'):]) == 参)
    T('⑦之四 诸印之令俱指 --派令（⛔手拟【派】）', src.count('--派令 %s') >= 2 and '令「【派】开第' not in src)
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
    if '--派令' in a:
        i = a.index('--派令')
        令 = 派令(int(a[i + 1]), '--重' in a)
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
