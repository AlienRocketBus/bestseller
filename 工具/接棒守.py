#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""接棒守（1022 立·402 封後无人接棒、书停五时半）——书不停之零 token 三锁之二。

【其由】402 之坐封版时 `心跳.py --跳 403` 自持其锁，写毕交接即收工；Stop 钩（席在跑吗）见「有人在跑」放行——
  那「人」正是它自己。无人开 403 之会话，书停五时半（23:17→04:50），作者醒来自见。
【三锁】
  ①Stop 钩（`工具/席在跑吗.py`）：本坐持写书之锁而手上无席、无後台之活 → 拦（⛔再认己锁作「他人在跑」）。
  ②本器 `--候 N`：交棒者收锁、开新会话之後，後台跑之（零 token）；每分取云端心跳——见第 N 章之锁为他坐所持且新鲜
    → ✓接棒成（rc=0）；逾限（默三十分）无人接 → rc=2，醒交棒者重开。候时 Stop 钩认之放行。
  ③停书警报（1117 交 GitHub）：云巡之跑停逾九十分即红——GitHub 邮作者（总编辑之坐亦死之兜底）；旧每时新会话之警报汰。`--哨` 留与写书之坐自查。
  ④停书之巡（1116 作者令「一定要有一个机制防止这种事情再次出现」「stops at most 1 hour」——455 之坐容器死，书停三日）：
    1117 作者令「定时检查能不能不花费 token……最大程度的去利用 github」「没有额度限制 可以无限跑」→ 交 GitHub（`.github/workflows/巡.yml`）：
    每五分跑 `--云巡`（＝巡()）：有人在写／交棒中／暂停即「止」——零 token；停写／解停／合入之卡 → 於哨 PR（头枝 备份/巡警）留一言，
    唤总编辑之坐（其订此 PR·唯其能派；同局二十分一唤）；每跑落 备份/巡印。总编辑醒即跑 `--巡`（沙盒并验巡印之鲜·rc 5 即 GitHub 之巡停摆）。
    兜底之巡（三令入总编辑之坐·见 兜底之令；平台定时之令最短一时，故常＝甲:27＋乙:57 每三十分·缓存恒温，降级＝丙:07 启＋乙改:47 每二十分）防 GitHub 之巡自停。
    坐死至新坐开：常 ≤ 50 分（＝旧），GitHub 死 ≤ 60 分、降级後 ≤ 50。
    1117 再治（環）：*/5 之 cron 首一时零跑（GitHub 之定时不可恃）→ 巡.yml 改「環」：workflow_dispatch huan=1 之跑每五分一巡、
    满三百四十分自派後继（concurrency 排候·无缝），schedule 与无 huan 之 dispatch 为再起之器；rc 5 之印即 run_workflow huan=1 起環。
    1117 作者续令「效果至少要和现在一样，最好能超越」→ 不劣之审：闭环（总编辑每 --巡 落 备份/巡应，云巡唤而三十分未应即红邮作者）、
    常对拍（沙盒复云巡之判，异即 rc 6）、护额（仓转私有即云巡自停）——见⑤。
用法：
  python3 工具/接棒守.py --候主 403 [分]   # 封版後候主枝含 403（run_in_background；零 token）：0 已含（已快进）｜3 GitHub 报红／拒／败（印其红）｜2 逾限（印 workflow_dispatch 之兜底·⛔沙盒跑闸）
  python3 工具/接棒守.py --候 404 [分]     # 交棒後以 run_in_background 跑
  python3 工具/接棒守.py --在候            # rc=0 在候
  python3 工具/接棒守.py --立守书          # 守书之会话首回立之（⛔写书之坐立之）
  python3 工具/接棒守.py --哨              # 定时之保用：有人在写或交棒中 rc=0；停写 rc=2 并印开写书会话之令
  python3 工具/接棒守.py --派令 404 [--重]  # 交棒：印 create_trigger 之参（run_once_at 已算）；总编辑醒即以其中之参原样 create_session 一回
                                           #   403 未入主枝而其报红／拒／败（或缺章标而 备份/存底 有其封版之提交）→ 自出【重派】之参：自「章-403」（或其源）起、先治（1027 A2）
  python3 工具/接棒守.py --巡              # 停书之巡（总编辑之坐·醒於哨 PR 之言或兜底之巡）：印「止」或【重派】之参（rc 0 止｜2 派｜3 解停｜4 封而逾三十分未入主·GitHub 停摆｜5 巡印逾三十分·GitHub 之巡停摆→降级｜6 对拍不合｜7 巡印复鲜→复常）；沙盒每跑落 备份/巡应
  python3 工具/接棒守.py --云巡 [--试]      # GitHub（巡.yml·環之跑每五分一巡）：巡()、落巡印、非止即於哨 PR 留言唤总编辑（--试 必留一言，验唤醒之路）
  python3 工具/接棒守.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, re, sys, time, json, fcntl, subprocess

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
总编辑 = 'session_018Kg61wMkRDSZXTWBa5imhH'   # 唯其有 create_session 之器（1106 迁仓：RobotSpa 之迁仓之坐接为总编辑；旧 016Hgfc2）
def _源():
    """自 git remote origin 推 https://github.com/<owner>/<repo>（1106 迁仓·虹吸：换号⛔再改）；推不得则用新址。"""
    import re as _re, subprocess as _sp
    try:
        u = _sp.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True, timeout=5,
                    cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
        m = _re.search(r'github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?$', u) or \
            _re.search(r'/git/([^/\s]+)/([^/\s]+?)(?:\.git)?/?$', u)
        if m:
            return 'https://github.com/%s/%s' % (m.group(1), m.group(2))
    except Exception:
        pass
    return 'https://github.com/AlienRocketBus/ojedmksaemckdsokjmenjncdklerfml'   # 1116 换号（RobotSpa 被标记→复制至 AlienRocketBus）、同日作者改仓名 bestseller→此


源 = _源()


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


# ── ④停书之巡（1116 作者令「stops at most 1 hour」；1117 作者令「定时检查不花 token、最大程度利用 GitHub」→ 交 GitHub：见⑤云巡）──
#   巡()：GitHub 每五分跑之（`--云巡`），止即零 token；非止方唤总编辑之坐（哨 PR 一言）——唯其有 create_session（定时所唤之新会话⛔能派·1116 演练二回）。
#   总编辑醒（哨 PR 之言、或兜底之巡每三十分）跑 `--巡`（沙盒：并验巡印之鲜、常对拍、落巡应）：印「止」即答「止」一字而止。
#   旧三条每时之令（:07 :27 :47·每二十分唤总编辑一回、日七十二唤）1117 汰：日常之巡零 token。
解停之令 = "python3 -c \"import sys;sys.path.insert(0,'工具');import 心跳,自走;print(心跳.解停(自走.末章()+1))\""


def 巡判(d, 今, 限, 停在=True, 末=None):
    """⛔纯判（停书之巡）：云端心跳 d → (形, 号, 由)。形：'止' 有人在写／交棒中／暂停｜'派' 停写→【重派】第 号 章｜'解' 停锁残留而令已解。
    读不出 → 作停写（fail→派，与 哨判 同）；号取心跳之章（或毕），皆无则 末（自走.末章()+1）。"""
    if isinstance(d, dict) and d.get('章') == '暂停':
        if 停在:
            return '止', None, '暂停令在（停锁）'
        return '解', None, '⛔停锁残留而暂停令已解（解停之推未成）——书⛔能续'
    rc, 由 = 哨判(d, 今, 限)
    if rc == 0:
        return '止', None, 由
    号 = None
    if isinstance(d, dict):
        try:
            号 = int(d.get('章') if d.get('章') is not None else d.get('毕'))
        except (TypeError, ValueError):
            号 = None
    return '派', (号 if 号 is not None else 末), 由


合入之界分 = 30   # 封版之章逾此分未入主枝 → 停书（GitHub 停摆·1116 实见：455 封於 10:25，GitHub 一时无报，心跳鲜而巡判止）


def 合入之卡(d, 今=None, 标=None, 含=None, 时=None):
    """心跳之章 N 鲜（封版之坐已跳 N+1、或新坐写 N）而第 N-1 章之封（章-(N-1)）逾 合入之界分 未入主 → 印停书之由；否则 ''。"""
    try:
        n = int(d.get('章')) - 1 if isinstance(d, dict) and d.get('章') not in (None, '暂停') else None
    except (TypeError, ValueError):
        n = None
    if not n:
        return ''
    sha = (标 or 云端章标)(n)
    if not sha or (含 or 主含)(n):
        return ''
    try:
        t = (时 or (lambda s: int(subprocess.run(['git', 'log', '-1', '--format=%ct', s], cwd=ROOT, capture_output=True,
                                                   text=True).stdout.strip() or 0)))(sha)
    except Exception:
        t = 0
    分 = ((今 or int(time.time())) - t) // 60 if t else -1
    if 0 <= 分 < 合入之界分:
        return ''
    return ('⛔ 停书：第%d章已封（章-%d %s）%s未入主枝——GitHub 之闸无果（多半 Actions 额度用光、或账号之 Actions 被停——1116 RobotSpa 即后者）。'
            '即告作者「GitHub 跑不动了，多半是本月额度用光（或账号被停），请换号或等下月」；兜底 `python3 工具/推.py --直`（直推主枝须作者许）'
            % (n, n, sha[:12], ('%d 分' % 分) if 分 >= 0 else '久'))


_巡之心 = None   # 巡() 所读之云端心跳（云巡落巡印之 心时 取此——所判与所记同一心跳，常对拍方准）


def 巡(查印=False):
    global _巡之心
    import 心跳
    在, d = 心跳._远()
    _巡之心 = d if 在 else None
    try:
        import 暂停令
        停在 = bool(暂停令.在()[0])     # 1117 治：旧 bool(元组) 恒真——令解而停锁残留，巡恒判止、⛔察解停
    except Exception:
        停在 = True
    末 = None
    if not (在 and isinstance(d, dict)) or (d.get('章') is None and d.get('毕') is None):
        try:
            import 自走
            末 = 自走.末章() + 1
        except Exception:
            末 = None
    形, 号, 由 = 巡判(d if 在 else None, int(time.time()), 心跳.限, 停在=停在, 末=末)
    if 形 == '止':
        卡 = 合入之卡(d)
        if 卡:
            print(卡)
            return 4
        if 查印:      # 沙盒（总编辑之坐）：验 GitHub 之巡之鲜（rc 5）→ 降级之复（rc 7）→ 常对拍（rc 6）
            印d = _读枝档(巡印枝, 巡印档)
            印由 = 巡印之由(d=印d)
            if 印由:
                print(印由)
                return 5
            if ((_读枝档(巡应枝, 巡应档) or {}).get('rc')) == 5:
                print('GitHub 之巡复鲜——复常（兜底之巡 %s＝每三十分·撤降级之每二十分）：%s' % (兜底之刻(), 兜底之改(False)))
                return 7
            异 = 对拍判(印d, _巡之心, 停在, 心跳.限)
            if 异:
                print(异)
                return 6
        print('止')
        return 0
    print(由)
    if 形 == '解':
        print('  ①重跑解停：' + 解停之令)
        print('  ②再 `python3 工具/接棒守.py --派令 <末章+1>`，以其参 create_session 一回')
        return 3
    if 号 is None:
        print('  ⛔章号读不出——跑 `python3 工具/自走.py` 取下一章，再 `python3 工具/接棒守.py --派令 N --重`、以其参 create_session')
        return 2
    坐 = str(d.get('坐') or '') if isinstance(d, dict) else ''
    if isinstance(d, dict) and d.get('章') is not None and 坐 and 坐 not in ('暂停令', '未名'):
        print('  ①先 get_session session_%s 看实时之状：正跑一回（running）即⛔重派、答「候」而止；其 rate_limit_info.status 非 allowed（周限·坑59：额度未复，派亦即败）即⛔重派、答「候·周限至 resetsAt」而止；否则续②（痛三：动他会话只凭实时之状）' % 坐)
    治 = 派令之治(号)
    print('  ②create_session 参原样（【重派】·会话之守钩拦即照其参／其由办）%s：' % ('（先治第%d章·源「%s」）' % (号 - 1, 治) if 治 else ''))
    print('  ' + json.dumps(派之参(号, True, 治=治), ensure_ascii=False))
    return 2


# ── ⑤云巡（1117 作者令「定时检查能不能不花费 token 而且能够达到最好的效果……最大程度的去利用 github」；同日「没有额度限制 可以无限跑」）──
#   停书之巡交 GitHub（.github/workflows/巡.yml）：每五分跑 `--云巡`＝巡()；「止」即毕——零 token。
#   非止（停写→派｜解停｜合入之卡｜器自败）→ 於哨 PR（头枝 备份/巡警）留一言：总编辑之坐订其动静（subscribe_pr_activity），一言即唤之
#   （候时零 token）；同一停之局 唤之隔 二十分一唤（⛔每五分刷）；停逾 警之界 九十分（或器自败、合入之卡、唤而未应）→ 唤之跑红：GitHub 邮作者
#   （红随唤：二十分一红·⛔每五分一邮）。每跑落 备份/巡印（单提交、force）之 _巡印.json（并记其所判之心跳之时 心时）。
#   1117 作者续令「转移到 GitHub 上……效果至少要和现在一样，最好能超越」→ 不劣之审（法用#云巡）：
#     ①闭环：总编辑每跑沙盒之 --巡 落 备份/巡应；云巡唤後逾 应之候 三十分未应 → 红（总编辑之坐失联／订阅断——旧制无人知）；
#     ②常对拍：沙盒之 --巡 以同一心跳复云巡之判，异即 rc 6（GitHub 之判⛔与沙盒异）；
#     ③护额：仓转私有（Actions 按分计）→ 云巡自停（disable 巡.yml·⛔耗尽 autopush 之额度而书停）、唤总编辑降级（1117 作者令开源·仓公开，此为其变之守）；
#     ④兜底之巡每三十分（甲 :27＋乙 :57 二令——平台定时之令最短一时，一令二刻〔27,57〕1117 平台拒之；缓存一时内恒温，每唤约 $0.1—0.2；
#       每三时则缓存恒冷、每唤约 $1——日耗反不逾每三时，而守倍密·1117 审计实测）：验巡印之鲜（rc 5 即降级：丙 :07 启＋乙改 :47＝每二十分如旧；复鲜 rc 7 即复）。
#   坐死至新坐开：常 ≤ 心跳.限 25 ＋ 云巡之隔 5 ＋ GitHub 定时之迟（留 15）＋ 派之数分 ≤ 50（＝旧）；GitHub 死 ≤ 25 ＋ 兜底之隔 30 ＋ 5 ≤ 60，降级後 ≤ 50（＝旧）。
#   1117 再治（環·GitHub 之 */5 定时首一时零跑、dispatch 之跑俱成）：巡.yml 之五分⛔倚 cron——workflow_dispatch huan=1 起「環」之跑
#     （每 jian 三百秒一巡、每巡先取本 ref 之新；满 fen 三百四十分〔job 之限 355〕即以 GITHUB_TOKEN 自派後继，concurrency 巡环-<枝> 排候·无缝）；
#     schedule（若偶发）与无 huan 之 dispatch 为再起之器（本枝无環即派一環）；巡.yml 被停（私停）→ 環於本巡後即止。rc 5 之印即起環（run_workflow huan=1）。
云巡之隔分 = 5
GitHub之迟分 = 15
唤之隔分 = 20
警之界分 = 90
应之候分 = 30          # 总编辑之坐长回合时唤候至回合末——十五分则忙而误红；三十分合一时之界（坐死 25＋5＋30≈一时即邮作者）
巡警枝 = '备份/巡警'     # 哨 PR 之头枝（⛔并；只为唤总编辑之坐）
巡印枝 = '备份/巡印'     # 单提交（无父）之枝，其上只 _巡印.json——云巡每跑 force 写之
巡印档 = '_巡印.json'
巡印之限分 = 30
巡应枝 = '备份/巡应'     # 单提交（无父）之枝，其上只 _巡应.json——总编辑沙盒之 --巡 每跑 force 写之（云巡验其应）
巡应档 = '_巡应.json'
# 兜底之巡三令（总编辑之坐之定时之令，各跑 `--巡`·验巡印之鲜）：平台定时之令最短一时（1117 拒 '27,57 * * * *' 之一令）→ 每令一时至多一跑。
#   （名, 号, 常之 cron, 降之 cron, 常时开否）——降级三令俱开。常：甲 :27＋乙 :57＝每三十分（缓存一时内恒温）；
#   降级（GitHub 之巡停摆·rc 5）：丙 :07 启＋乙改 :47 → :07 :27 :47＝每二十分＝旧三令之隔；复常（rc 7）反之。印之令俱由 兜底之改 出（⛔手拟）。
兜底之令 = (
    ('甲', 'trig_01Q7EtciYmueJhVgjeNAzrgU', '27 * * * *', '27 * * * *', True),    # 常开；号同 席在跑吗.守书之令（暂停令三令俱停、解停复常——暂停令.守书之诸参 取此表）
    ('乙', 'trig_01TNKutzRmdDGYtauqe2YHx9', '57 * * * *', '47 * * * *', True),    # 常 :57，降级改 :47
    ('丙', 'trig_014QwEoUV4uaYJXmQrUtHSGh', '7 * * * *', '7 * * * *', False),     # 常停；降级启（:07）
)
兜底之隔分 = 30      # 常之隔（降级二十分）


def 兜底之分(降=False):
    """→ 兜底之巡所开诸令之分（升序）：常 [27, 57]；降 [7, 27, 47]。"""
    return sorted(int(m) for _, _, 常, 降之, 开 in 兜底之令 if 降 or 开 for m in (降之 if 降 else 常).split()[0].split(','))


def 兜底之刻(降=False):
    """→ 「:27 :57」之类（兜底之巡所跑之刻）。"""
    return ' '.join(':%02d' % m for m in 兜底之分(降))


def 兜底之改(降):
    """→ 降级（降=True·rc 5）或复常（降=False·rc 7）之 update_trigger 诸令：只列所改之令、所改之栏（先 enabled 後 cron_expression），以「；」连。"""
    开停, 改 = [], []
    for 名, 号, 常, 降之, 开 in 兜底之令:
        (旧c, 旧开), (新c, 新开) = ((常, 开), (降之, True)) if 降 else ((降之, True), (常, 开))
        if 旧开 != 新开:
            开停.append('update_trigger %s（%s）之 enabled「%s」' % (号, 名, 'true' if 新开 else 'false'))
        if 旧c != 新c:
            改.append('update_trigger %s（%s）之 cron_expression「%s」' % (号, 名, 新c))
    return '；'.join(开停 + 改)


警记 = '<!-- 巡警:%s -->'


def 云巡判(rc, d, 今, 旧言, 印=''):
    """⛔纯判（云巡）：巡之 rc、云端心跳 d、今、哨 PR 之旧言 [(时, 键)] → (唤?, 键, 红?, 停分)。
    rc 0 → 不唤、不红。键＝同一停之局（rc·章或毕·心跳之时）；同键之末言未逾 唤之隔分 → ⛔再唤。
    红：器自败（rc ∉ 0/2/3/4/5）、合入之卡（rc 4）、或停逾 警之界分。"""
    if rc == 0:
        return False, '', False, 0
    时 = 0
    if isinstance(d, dict):
        try:
            时 = int(d.get('时') or 0)
        except (TypeError, ValueError):
            时 = 0
    停分 = (今 - 时) // 60 if 时 else -1
    m4 = re.search(r'第(\d+)章已封', 印 or '') if rc == 4 else None
    if rc in (2, 3) and isinstance(d, dict):
        键 = 'rc%d·%s·%d' % (rc, d.get('章') if d.get('章') is not None else d.get('毕'), 时)
    elif m4:
        键 = 'rc4·%s' % m4.group(1)        # 合入之卡之印带「N 分」——以章为键（⛔每跑异键而每五分一唤）
    else:
        import hashlib
        键 = 'rc%d·%s' % (rc, hashlib.sha1((印 or '').split('\n')[0].encode('utf-8')).hexdigest()[:10])
    末 = max([t for t, k in 旧言 if k == 键] or [0])
    唤 = not (末 and 今 - 末 < 唤之隔分 * 60)
    红 = rc not in (2, 3, 5) or 停分 >= 警之界分
    return 唤, 键, 红, 停分


def _接口(法, 径, 体=None):
    """GitHub REST（GITHUB_TOKEN；⛔沙盒用——沙盒走 git 与会话之器）。→ 解析之 JSON。"""
    import urllib.request
    api = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
    req = urllib.request.Request(api + 径, method=法, data=json.dumps(体).encode('utf-8') if 体 is not None else None,
                                 headers={'Authorization': 'Bearer ' + os.environ.get('GH_TOKEN', os.environ.get('GITHUB_TOKEN', '')),
                                          'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8') or 'null')


def 哨PR(仓=None):
    """→ 哨 PR 之号（头枝 备份/巡警、开着者）；无即 None。"""
    import urllib.parse
    仓 = 仓 or os.environ.get('GITHUB_REPOSITORY', '')
    诸 = _接口('GET', '/repos/%s/pulls?state=open&per_page=100&head=%s' % (仓, urllib.parse.quote('%s:%s' % (仓.split('/')[0], 巡警枝))))
    return 诸[0]['number'] if 诸 else None


def _旧言(仓, 号, 今):
    """哨 PR 上 github-actions 所留、带 警记 之言（近六时）→ [(时, 键)]。"""
    import calendar, re as _re
    起 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(今 - 6 * 3600))
    言 = _接口('GET', '/repos/%s/issues/%d/comments?per_page=100&since=%s' % (仓, 号, 起)) or []
    出 = []
    for c in 言:
        m = _re.search(r'<!-- 巡警:(.+?) -->', c.get('body') or '')
        if m and (c.get('user') or {}).get('type') == 'Bot':
            出.append((calendar.timegm(time.strptime(c['created_at'], '%Y-%m-%dT%H:%M:%SZ')), m.group(1)))
    return 出


def _刻(t):
    return time.strftime('%m-%d %H:%M', time.gmtime(int(t))) if t else '无'


def _砌(档, 体, 信):
    """单档、单提交（无父）之 commit（hash-object＋mktree＋commit-tree：⛔经索引、⛔碰 HEAD 与工作区）→ sha 或 ''。"""
    def 跑令(*a, **k):
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, **k)
    b = 跑令('git', 'hash-object', '-w', '--stdin', input=体).stdout.strip()
    t = 跑令('git', 'mktree', input='100644 blob %s\t%s\n' % (b, 档)).stdout.strip()
    env = dict(os.environ, GIT_AUTHOR_NAME='xun', GIT_AUTHOR_EMAIL='xun@users.noreply.github.com',
               GIT_COMMITTER_NAME='xun', GIT_COMMITTER_EMAIL='xun@users.noreply.github.com')
    return subprocess.run(['git', 'commit-tree', t or '-', '-m', 信], cwd=ROOT, capture_output=True, text=True, env=env).stdout.strip()   # 树空即败而返空


def _读枝档(枝, 档):
    """云端单档之枝（巡印、巡应）→ dict｜None（读不出）。先 fetch。"""
    subprocess.run(['git', 'fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/origin/%s' % (枝, 枝)], cwd=ROOT, capture_output=True)
    r = subprocess.run(['git', 'show', 'origin/%s:%s' % (枝, 档)], cwd=ROOT, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout) if r.returncode == 0 else None
    except Exception:
        d = None
    return d if isinstance(d, dict) else None


def 落巡印(rc, 印, 今, 跑='', 心=None, 私=False):
    """→ 落 备份/巡印（单提交、force）之 _巡印.json（rc、印之首行、所判之心跳之时 心时〔常对拍〕、仓私否）；成否。"""
    try:
        心时 = int((心 or {}).get('时') or 0) if isinstance(心, dict) else 0
    except (TypeError, ValueError):
        心时 = 0
    体 = json.dumps({'时': 今, '刻': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(今)), 'rc': rc,
                    '印': (印 or '').strip().split('\n')[0][:200], '心时': 心时, '私': bool(私), '跑': 跑}, ensure_ascii=False)
    c = _砌(巡印档, 体, '巡印 rc=%s' % rc)
    if not c:
        return False
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', 'push', '-q', '-f', 'origin', '%s:refs/heads/%s' % (c, 巡印枝)],
                          cwd=ROOT, capture_output=True, text=True).returncode == 0


def 落巡应(rc, 今=None):
    """沙盒（总编辑之坐）每跑 --巡 → 落 备份/巡应（单提交、force）：云巡验总编辑之应（唤而未应即红）；成否。"""
    今 = 今 or int(time.time())
    体 = json.dumps({'时': 今, '刻': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(今)), 'rc': rc,
                    '坐': os.environ.get('CLAUDE_CODE_SESSION_ID', '')}, ensure_ascii=False)
    c = _砌(巡应档, 体, '巡应 rc=%s' % rc)
    if not c:
        return False
    return subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', 'push', '-q', '-f', 'origin', '%s:refs/heads/%s' % (c, 巡应枝)],
                          cwd=ROOT, capture_output=True, text=True).returncode == 0


def 巡印判(d, 今):
    """⛔纯判：巡印 d（dict 或 None）→ ''（鲜）或停摆之由（附降级之令）。"""
    降级 = '降级（兜底之巡 %s＝每二十分·如旧之三令）：%s' % (兜底之刻(True), 兜底之改(True))
    降 = ('——①先再起：actions_run_trigger run_workflow 巡.yml ref 主枝 inputs {"huan":"1"}（起環：每五分一巡、满三百四十分自派後继；環已在则排候、⛔重環）；②%s'
          '——巡印复鲜，--巡 即印 rc 7 而复常（%s＝每三十分）' % (降级, 兜底之刻()))
    if isinstance(d, dict) and d.get('私'):
        return ('⛔ GitHub 之巡自停：仓已转私有（Actions 按分计——云巡之環终日在跑将耗尽 autopush 之额度而书停，故自 disable 巡.yml·環即止）'
                '——%s；仓复公开即 enable 巡.yml（Actions 页「巡」之 Enable workflow），再 run_workflow 巡.yml ref 主枝 inputs {"huan":"1"} 起環' % 降级)
    try:
        时 = int((d or {}).get('时') or 0)
    except (TypeError, ValueError):
        时 = 0
    if not 时:
        return '⛔ GitHub 之巡停摆：备份/巡印 读不出——巡.yml 未跑或被停' + 降
    分 = (今 - 时) // 60
    if 分 > 巡印之限分:
        return '⛔ GitHub 之巡停摆：巡印 %d 分未更（限 %d 分）——查 Actions「巡」之跑（被停／定时失灵／cron 坏）' % (分, 巡印之限分) + 降
    return ''


def 巡印之由(今=None, d=None):
    """沙盒（总编辑之兜底之巡）：取云端巡印验其鲜 → ''｜停摆之由。"""
    return 巡印判(d if d is not None else _读枝档(巡印枝, 巡印档), 今 or int(time.time()))


def 应判(旧言, 应时, 今):
    """⛔纯判（闭环·1117 不劣之审）：哨 PR 之真唤（⛔试、⛔私）之末者逾 应之候分 而 巡应 未更於其後 → 唤而未应之由；否则 ''。"""
    真 = [t for t, k in 旧言 if not str(k).startswith(('试', '私'))]
    if not 真:
        return ''
    t = max(真)
    try:
        应时 = int(应时 or 0)
    except (TypeError, ValueError):
        应时 = 0
    if 今 - t < 应之候分 * 60 or 应时 >= t:
        return ''
    return ('⛔ 唤而未应：前唤（%s UTC）逾 %d 分而 备份/巡应 未更（末应 %s）——总编辑之坐或已失联、或其订此 PR 之路已断：'
            '作者知悉（开总编辑之会话，令其 subscribe_pr_activity 哨 PR #1、跑 `python3 工具/接棒守.py --巡`）' % (_刻(t), (今 - t) // 60, _刻(应时)))


def 对拍判(印d, 心d, 停在, 限):
    """⛔纯判（常对拍·1117 不劣之审）：云巡所判之心跳（巡印之 心时）与沙盒所读者同一 → 沙盒以 巡判 复其时之判；rc 异 → 不合之由；否则 ''。
    只对 rc 0/2/3（4 关云端之标、1 器败、5 不出於云）。"""
    try:
        印时, 云rc, 心时 = int(印d['时']), int(印d['rc']), int(印d.get('心时') or 0)
        我心时 = int((心d or {}).get('时') or 0)
    except Exception:
        return ''
    if 云rc not in (0, 2, 3) or not 心时 or 我心时 != 心时:
        return ''
    当 = {'止': 0, '派': 2, '解': 3}[巡判(心d, 印时, 限, 停在=停在)[0]]
    if 当 == 云rc:
        return ''
    return ('⚠ 对拍不合：云巡（%s）判 rc=%d，沙盒以同一心跳（时 %d）复其时之判当 rc=%d——GitHub 之判与沙盒异：'
            '查云巡之境（暂停令、心跳之读、主枝之旧）而治之（法用#云巡·常对拍）；本回照沙盒之判' % (印d.get('刻', ''), 云rc, 心时, 当))


def 仓私(仓):
    """→ True 私有｜False 公开｜None 读不出（⛔因读不出而自停）。"""
    try:
        return bool((_接口('GET', '/repos/%s' % 仓) or {}).get('private'))
    except Exception:
        return None


def 私停(仓, 今):
    """仓转私有（Actions 按分计）：云巡之環终日在跑（≈月四万三千分）将耗尽 autopush 之额度而书停 → 自 disable 巡.yml（環於本巡後见之即止）、唤总编辑降级。→ 1（红）。"""
    import urllib.parse
    由 = '⛔ 仓已转私有（Actions 按分计：云巡之環终日在跑≈月四万三千分，将耗尽 autopush 之额度而书停）——云巡自停（disable 巡.yml·環即止）'
    try:
        _接口('PUT', '/repos/%s/actions/workflows/%s/disable' % (仓, urllib.parse.quote('巡.yml')))
    except Exception as e:
        由 += '——而 disable 不成（%s）：作者於 Actions 页停之' % e
    print(由)
    try:
        号 = 哨PR(仓)
        if 号:
            _接口('POST', '/repos/%s/issues/%d/comments' % (仓, 号), {'body': '【巡警】%s\n\n总编辑：沙盒跑 `python3 工具/接棒守.py --巡`，照其 rc 5 之印降级（兜底之巡每二十分如旧）。\n\n%s'
                                                                         % (由, 警记 % ('私·%d' % 今))})
    except Exception as e:
        print('⛔ 唤不成：%s' % e)
    return 1


def 再闸(仓, n):
    """合入之卡（rc 4）之首唤：workflow_dispatch autopush.yml（ref 章-n·tries 0）令 GitHub 再跑其闸——旧须总编辑醒而手派（1117 GitHub 化之审·D）。→ 印之语。"""
    import urllib.parse
    try:
        _接口('POST', '/repos/%s/actions/workflows/%s/dispatches' % (仓, urllib.parse.quote('autopush.yml')), {'ref': '章-%s' % n, 'inputs': {'tries': '0'}})
        return '· 已自 workflow_dispatch autopush.yml（ref 章-%s）——GitHub 再跑其闸（零 token）；总编辑候其果，二十分後仍卡即再唤' % n
    except Exception as e:
        return '⚠ 再闸不成（workflow_dispatch autopush.yml·章-%s：%s）——总编辑照印手派' % (n, str(e)[:120])


def 云巡(试=False):
    """GitHub（巡.yml）之跑：巡() → 落巡印 → 仓私即自停 → 非止即唤（哨 PR 留一言；唤而未应即红）。→ 0 绿｜1 红（随唤：停逾九十分、器败、合入之卡、唤而未应；唤不成；私停）。"""
    import io, contextlib, traceback
    global _巡之心
    今 = int(time.time())
    _巡之心 = None
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = 巡()
    except Exception:
        rc = 1
        buf.write('⛔ 云巡自败：\n' + traceback.format_exc()[-1500:])
    印 = buf.getvalue()
    print(印.rstrip())
    d = _巡之心
    仓 = os.environ.get('GITHUB_REPOSITORY', '')
    跑 = '%s/%s/actions/runs/%s' % (os.environ.get('GITHUB_SERVER_URL', 'https://github.com'), 仓, os.environ.get('GITHUB_RUN_ID', ''))
    私 = 仓私(仓) is True
    if not 落巡印(rc, 印, 今, 跑, 心=d, 私=私):
        print('⚠ 巡印落不成（备份/巡印）')
    if 私 and not 试:
        return 私停(仓, 今)
    if rc == 0 and not 试:
        return 0
    try:
        号 = 哨PR(仓)
        if not 号:
            print('⛔ 哨 PR（头枝 %s）不在——唤不得：总编辑立之、订之' % 巡警枝)
            return 1
        try:
            旧 = _旧言(仓, 号, 今)
        except Exception as e:      # 读旧言败 → 宁多唤一回、⛔因去重之败而不唤
            print('⚠ 旧言读不出（%s）——作无旧言论' % e)
            旧 = []
        print('· 哨 PR #%d：近六时旧唤 %d（%s）' % (号, len(旧), '、'.join(k for _, k in 旧[-3:]) or '无'))
        唤, 键, 红, 停分 = 云巡判(rc, d, 今, 旧, 印)
        应由 = '' if 试 else 应判(旧, (_读枝档(巡应枝, 巡应档) or {}).get('时'), 今)
        if 应由:
            print(应由)
            红 = True
        闸由 = ''
        if rc == 4 and not 试 and not any(k == 键 for _, k in 旧):      # 合入之卡之首唤：先令 GitHub 再跑其闸（零 token·旧须总编辑手派）
            闸由 = 再闸(仓, 键.split('·', 1)[1])
            print(闸由)
        if 试:
            唤, 键 = True, '试·%d' % 今
        if not 唤:
            print('· 同局（%s）%d 分内已唤——⛔再唤（红随唤：二十分一红，⛔每五分一邮）' % (键, 唤之隔分))
            return 0
        体 = ('【巡警】%s\n\n```\n%s\n```\n\n总编辑：醒即照总章三之5「醒於【巡】」办——沙盒跑 `python3 工具/接棒守.py --巡` 自验（⛔凭此言径派）。'
              '%s%s\n\n%s' % ('试唤（验唤醒之路·无须派）' if 试 else ('停书 %s 分' % 停分 if 停分 >= 0 else '器之报'),
                              印.strip()[:3000], ''.join('\n\n' + x for x in (闸由, 应由) if x),
                              '\n\n⚠ 本跑红——GitHub 邮作者知悉。' if (红 and not 试) else '', 警记 % 键))
        _接口('POST', '/repos/%s/issues/%d/comments' % (仓, 号), {'body': 体})
        print('✓ 已唤（哨 PR #%d·%s）' % (号, 键))
        return 1 if (红 and not 试) else 0
    except Exception as e:
        print('⛔ 唤不成：%s' % e)
        return 1


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
            print('⛔⛔ 报作者（1108 作者令）：GitHub Actions 跑不动了——多半是本月额度（分钟）用光；即告作者「GitHub 跑不动了，多半是本月额度用光，请换号或等下月」。总编辑之坐当场告作者（对话＋推送通知）；写书之坐 create_trigger 入总编辑之会话（接棒守.总编辑）、令以「【报】GitHub 跑不动」起')
            print(存底包之语(n))
            return 2
        睡(隔)


def 存底包之语(n):
    """候主非成之返（1027 A2）：主枝未含本章，阅读器即无之——存底包打全本单档、SendUserFile 交作者（0924 作者令「推被拦下，存底包照送」）。"""
    return ('· 作者手上之书⛔由那道闸说了算（0924 令）：主枝未含第%s章、阅读器无之——`python3 工具/存底包.py`（全本单档 .txt、正文 .tar.gz、全仓 .bundle），'
            '其印之路以 SendUserFile 交作者（打了⛔送等於没打）；主枝含之後⛔再打' % n)


交棒之宽分 = 20     # 撤锁後此内无人接，作「交棒中」（⛔误判停写而另开一坐）；1116 一时之令 30→20（与 席在跑吗.交棒之宽 同）


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
      and json.JSONDecoder().raw_decode(派令(411, 今=lambda: 0, 治='章-410')['prompt'].split('⛔改参：', 1)[1])[0] == 治参
      and '先治第410章' in 派令(411, 今=lambda: 0, 治='章-410')['name'] and '先治' not in 派令(411, 今=lambda: 0)['name'])
    T('⑨之四 --派令 之判：前章已在主 → 常形（⛔查治）；未在主 → 治之源；读崩 → 常形',
      派令之治(411, 主=lambda n: True, 治=lambda n: 1 / 0) is None and 派令之治(411, 主=lambda n: False, 治=lambda n: '章-%d' % n) == '章-410'
      and 派令之治(411, 主=lambda n: 1 / 0) is None and '治 = 派令之治(int(a[i + 1]))' in open(os.path.abspath(__file__), encoding='utf-8').read())
    T('⑥之二 主含真查云端：章-N 之标为主枝之祖', all(k in 段主含 for k in ("'merge-base', '--is-ancestor'", "'refs/heads/章-%d'", 'ls-remote')))
    参 = 派之参(411, 名='第411章')
    T('⑦派之参：题、模、源、枝、令俱定形', 参['title'] == '镇冢秘术·第411章' and 参['model'] == 'claude-opus-5-5'
      and 参['source_revision'] == 参['outcome_branch'] == 主枝 and 参['source_url'] == 源 and __import__('re').match(r'^https://github\.com/[^/]+/[^/]+$', 源)
      and '第 411 章' in 参['prompt'] and '--跳 411' in 参['prompt'] and not 参['prompt'].startswith('【重派】'))
    T('⑦之二 重派：令首带【重派】、余同', 派之参(411, True, '第411章')['prompt'] == '【重派】' + 参['prompt'])
    T('⑦之五 题名实务：大审到期即名其段（1024 作者疑「怎么开始写 411」）',
      务之名(411, 上审=407, 待至=410) == '大审第408—410章（审毕暂停）' and 务之名(421, 上审=410, 待至=410) == '大审第411—420章（後接第421章）'
      and 务之名(412, 上审=410) == '第412章' and 务之名(411, 上审=410) == '第411章')
    T('⑦之六 令⛔言「写」第 N 章（实务由自走判）', '照其所判办' in 参['prompt'] and not 参['prompt'].startswith('写'))
    令 = 派令(411, 今=lambda: 0)
    T('⑦之三 派令：入总编辑之会话、二分後、令中之参可原样解回', 令['persistent_session_id'] == 总编辑
      and 令['run_once_at'] == '1970-01-01T00:02:00Z' and 令['prompt'].startswith('【派】开第 411 章')
      and json.JSONDecoder().raw_decode(令['prompt'][令['prompt'].index('{'):])[0] == 派之参(411))
    # ⑩1116 停书之巡（作者令「stops at most 1 hour」）：巡判逐形；一时之界：限＋云巡之隔＋GitHub 之迟＋派 ＜ 六十分（1117 交 GitHub）
    import 心跳 as _心
    _今 = 10 ** 9
    _限 = _心.限
    import 席在跑吗 as _席
    def _分(c):      # cron 之分栏（'27 * * * *'）→ [27]
        return [int(x) for x in c.split()[0].split(',')]
    def _隔(ms):     # 所开诸令之分之并 → 相邻之隔之最大者（环一时）
        m = sorted(set(ms))
        return max((m[(i + 1) % len(m)] - m[i]) % 60 or 60 for i in range(len(m)))
    _常分 = [x for _, _, c, _, 开 in 兜底之令 if 开 for x in _分(c)]
    _降分 = [x for _, _, _, c, _ in 兜底之令 for x in _分(c)]     # 降级三令俱开
    T('⑩一时之界（1117 云巡·不劣之审）：常 心跳.限 25＋云巡之隔 5＋GitHub 定时之迟 15＋派 5 ≤ 50（＝旧三令之界）；'
      'GitHub 死 25＋兜底之隔 30＋5 ≤ 60、降级後 25＋20＋5 ≤ 50（＝旧）——隔取所开诸令之分之并（常 甲乙、降 甲乙丙）；交棒之宽 ≤ 心跳.限；甲之号 即 席在跑吗.守书之令',
      _限 == 25 * 60 and 云巡之隔分 == 5 and _限 // 60 + 云巡之隔分 + GitHub之迟分 + 5 <= 50 and 交棒之宽分 * 60 <= _限
      and _隔(_常分) == 兜底之隔分 == 30 and _限 // 60 + 兜底之隔分 + 5 <= 60 and _隔(_降分) == 20 and _限 // 60 + _隔(_降分) + 5 <= 50
      and 兜底之分() == sorted(_常分) and 兜底之分(True) == sorted(_降分) and 兜底之刻() == ':27 :57' and 兜底之刻(True) == ':07 :27 :47'
      and [x[0] for x in 兜底之令] == ['甲', '乙', '丙'] and len({x[1] for x in 兜底之令}) == 3 and all(str(x[1]).startswith('trig_') for x in 兜底之令)
      and 兜底之令[0][1] == _席.守书之令 and 兜底之令[0][4] is True)   # 旧三令之号之去：法用册「废·停书之巡三令与每时之警报」之去证守之
    T('⑩之六 兜底之巡每令一时至多一跑（平台定时之令最短一时·1117 拒「27,57 * * * *」之一令）：常、降之 cron 俱五栏、分栏只一数（0—59）、余栏俱「*」',
      all(len(c.split()) == 5 and re.fullmatch(r'[0-9]{1,2}', c.split()[0]) and int(c.split()[0]) < 60 and c.split()[1:] == ['*'] * 4
          for _, _, 常, 降之, _ in 兜底之令 for c in (常, 降之)))
    T('⑩之二 巡判逐形：在写／交棒中→止；停写→派（号取章或毕；皆无取末）；读不出→派末；暂停→止；停锁残而令解→解',
      巡判({'章': 455, '时': _今 - 600, '坐': 'A'}, _今, _限)[0] == '止'
      and 巡判({'章': None, '毕': 456, '时': _今 - 600}, _今, _限)[0] == '止'
      and 巡判({'章': 455, '时': _今 - _限 - 60, '坐': 'A'}, _今, _限)[:2] == ('派', 455)
      and 巡判({'章': None, '毕': 456, '时': _今 - 交棒之宽分 * 60 - 60}, _今, _限)[:2] == ('派', 456)
      and 巡判(None, _今, _限, 末=457)[:2] == ('派', 457)
      and 巡判({'时': 'x'}, _今, _限, 末=458)[:2] == ('派', 458)
      and 巡判({'章': '暂停', '时': 4102444800, '坐': '暂停令'}, _今, _限)[0] == '止'
      and 巡判({'章': '暂停', '时': 4102444800, '坐': '暂停令'}, _今, _限, 停在=False)[0] == '解')
    import io as _io, contextlib as _cl, 暂停令 as _停令
    _旧远, _旧在 = _心._远, _停令.在
    try:   # 1117 治：巡之 停在 取 暂停令.在()[0]——旧 bool(元组) 恒真，令解而停锁残留则巡（云巡亦然）恒判止、⛔察解停
        _心._远 = lambda: (True, {'章': '暂停', '时': 4102444800, '坐': '暂停令'})
        with _cl.redirect_stdout(_io.StringIO()):
            _停令.在 = lambda root=None: (False, '已解（试）'); _rc解 = 巡()
            _停令.在 = lambda root=None: (True, '暂停令在（试）'); _rc止 = 巡()
    finally:
        _心._远, _停令.在 = _旧远, _旧在
    T('⑩之七 巡之停在取 暂停令.在()[0]：停锁在而令已解 → rc 3（解）、令在 → rc 0（止）——暂停中兜底三令俱停，解停唯 GitHub 云巡察之',
      _rc解 == 3 and _rc止 == 0)
    _段巡 = src.split('def 巡(查印=False):')[1].split('\ndef ')[0] if 'def 巡(查印=False):' in src else ''
    T('⑩之四 合入之卡：封逾三十分未入主→停书之报；未封／已入主／未逾→空',
      '停书' in 合入之卡({'章': 456, '时': 1}, 今=10000, 标=lambda n: 'a' * 40, 含=lambda n: False, 时=lambda s: 10000 - 31 * 60)
      and 合入之卡({'章': 456, '时': 1}, 今=10000, 标=lambda n: '', 含=lambda n: False, 时=lambda s: 0) == ''
      and 合入之卡({'章': 456, '时': 1}, 今=10000, 标=lambda n: 'a' * 40, 含=lambda n: True, 时=lambda s: 0) == ''
      and 合入之卡({'章': 456, '时': 1}, 今=10000, 标=lambda n: 'a' * 40, 含=lambda n: False, 时=lambda s: 10000 - 600) == ''
      and 合入之卡({'章': None, '毕': 456}, 今=10000) == '' and 合入之卡({'章': '暂停'}, 今=10000) == '')
    T('⑩之三 巡之派参俱【重派】（越会话之守「一时内同章已派」之拦）、先 get_session 其坐、印「止」即止',
      '派之参(号, True, 治=治)' in _段巡 and 'get_session' in _段巡 and "print('止')" in _段巡
      and 派之参(455, True)['prompt'].startswith('【重派】'))
    T('⑩之五 巡之重派先核周限（坑59·1117：周限尽则写书之坐与诸巡俱停十一时；额度未复⛔派）',
      'rate_limit_info' in _段巡 and '周限' in _段巡)
    _旧 = [(_今 - 600, 'rc2·455·%d' % (_今 - _限 - 60))]
    _d = {'章': 455, '时': _今 - _限 - 60, '坐': 'A'}
    T('⑪云巡判（1117）：止→⛔唤⛔红；停写→唤（键＝rc·章·心跳之时）；同键二十分内⛔再唤、逾即再唤；停逾九十分或器败或合入之卡→红',
      云巡判(0, _d, _今, [])[:3] == (False, '', False)
      and 云巡判(2, _d, _今, [])[:3] == (True, 'rc2·455·%d' % (_今 - _限 - 60), False)
      and 云巡判(2, _d, _今, _旧)[0] is False
      and 云巡判(2, _d, _今 + 唤之隔分 * 60, _旧)[0] is True
      and 云巡判(2, {'章': 455, '时': _今 - 警之界分 * 60, '坐': 'A'}, _今, [])[2] is True
      and 云巡判(1, None, _今, [], '⛔ 云巡自败')[2] is True and 云巡判(4, _d, _今, [], '⛔ 停书')[2] is True
      and 云巡判(3, {'章': '暂停', '时': _今 - 60}, _今, [])[2] is False)
    T('⑪之二 巡印判：鲜→空；逾三十分或读不出→停摆之由',
      巡印判({'时': _今 - 600}, _今) == '' and '停摆' in 巡印判({'时': _今 - 巡印之限分 * 60 - 120}, _今)
      and '停摆' in 巡印判(None, _今) and '停摆' in 巡印判({'时': 'x'}, _今))
    _流 = open(os.path.join(ROOT, '.github', 'workflows', '巡.yml'), encoding='utf-8').read() if os.path.exists(
        os.path.join(ROOT, '.github', 'workflows', '巡.yml')) else ''
    _段云 = src.split('def 云巡(')[1].split('\ndef ')[0]
    T('⑪之四 云巡：读旧言败即作无旧言（宁多唤⛔不唤）；哨 PR 不在即红（GitHub 邮作者）；巡印每跑俱落（止亦落）',
      "旧 = []" in _段云 and '哨 PR' in _段云 and 'return 1' in _段云
      and _段云.index('落巡印(') < _段云.index('if rc == 0 and not 试'))
    T('⑪之三 巡.yml：每五分之 cron、跑 --云巡、可写言（issues／pull-requests）、可推巡印（contents）；沙盒之 --巡 验巡印（rc 5）、GitHub 之 --巡⛔验；'
      '環（1117·cron 首一时零跑）：huan 之入、每巡取本 ref 之新、满分自派後继（dispatches 之 POST）、concurrency 巡环 排候、job 之限 355、'
      '再起之器认 run-name「巡环」、巡.yml 被停即止；rc 5 之印起環（"huan":"1"）',
      "cron: '*/5 * * * *'" in _流 and '接棒守.py --云巡' in _流 and 'issues: write' in _流 and 'pull-requests: write' in _流
      and 'contents: write' in _流 and 'actions: write' in _流 and '巡印之由(d=印d)' in _段巡
      and all(k in _流 for k in ('      huan:\n', "inputs.huan == '1'", 'timeout-minutes: 355', 'group: 巡环-${{ github.ref_name }}',
                                  'cancel-in-progress: false', 'fetch -q origin "$GITHUB_REF_NAME"', 'reset -q --hard FETCH_HEAD',
                                  '-X POST', '/actions/workflows/%E5%B7%A1.yml/dispatches', '"huan":"1"', "format('巡环", 'startswith("巡环")',
                                  '!= active', 'until curl'))
      and '"huan":"1"' in 巡印判({'时': _今 - 巡印之限分 * 60 - 120}, _今) and '"huan":"1"' in 巡印判(None, _今)
      and all(k in open(os.path.abspath(__file__), encoding='utf-8').read().split("\nif __name__ == '__main__':")[1] for k in ("_rc = 巡(查印=True)", '落巡应(_rc)', 'sys.exit(巡())')))
    T('⑪之九 合入之卡：键以章（印之分数异而键同·⛔每五分一唤）；首唤先 workflow_dispatch autopush（ref 章-N）、再唤⛔复派',
      云巡判(4, _d, _今, [], '⛔ 停书：第456章已封（章-456 abc）31 分未入主枝')[1] == 云巡判(4, _d, _今, [], '⛔ 停书：第456章已封（章-456 abc）36 分未入主枝')[1] == 'rc4·456'
      and 云巡判(4, _d, _今, [(_今 - 300, 'rc4·456')], '⛔ 停书：第456章已封（章-456 abc）36 分未入主枝')[0] is False
      and '再闸(仓' in _段云 and 'not any(k == 键 for _, k in 旧)' in _段云
      and "'ref': '章-%s' % n" in src.split('def 再闸(')[1].split('\ndef ')[0])
    _w = [(_今 - (应之候分 + 5) * 60, 'rc2·455·1'), (_今 - 3 * 60, '试·9'), (_今 - 2 * 60, '私·9')]
    T('⑪之五 应判（闭环）：真唤逾应之候（三十分）而巡应未更於其後→未应；应新於唤、未逾应之候、无真唤（试／私不计）→空',
      应之候分 == 30 and '未应' in 应判(_w, _今 - (应之候分 + 10) * 60, _今) and 应判(_w, _今 - (应之候分 + 4) * 60, _今) == ''
      and 应判(_w, 0, _今 - 6 * 60) == ''
      and 应判([(_今 - 3600, '试·1'), (_今 - 3600, '私·1')], 0, _今) == '' and '未应' in 应判(_w, None, _今) and 应判([], 0, _今) == '')
    _hd = {'章': 455, '时': _今 - 600, '坐': 'A'}
    T('⑪之六 对拍判（常对拍）：同一心跳而云判异→不合；判同、心跳异、rc 4／1／5、心时缺→空',
      '对拍不合' in 对拍判({'时': _今, 'rc': 2, '心时': _今 - 600}, _hd, False, _限)
      and 对拍判({'时': _今, 'rc': 0, '心时': _今 - 600}, _hd, False, _限) == ''
      and 对拍判({'时': _今 + _限, 'rc': 2, '心时': _今 - 600}, _hd, False, _限) == ''
      and '对拍不合' in 对拍判({'时': _今 + _限, 'rc': 0, '心时': _今 - 600}, _hd, False, _限)
      and 对拍判({'时': _今, 'rc': 2, '心时': _今 - 601}, _hd, False, _限) == ''
      and 对拍判({'时': _今, 'rc': 4, '心时': _今 - 600}, _hd, False, _限) == '' and 对拍判({'时': _今, 'rc': 2}, _hd, False, _限) == ''
      and 对拍判(None, _hd, False, _限) == '')
    _号 = {x[0]: x[1] for x in 兜底之令}
    _降印, _私印 = 巡印判(None, _今), 巡印判({'时': _今, '私': True}, _今)
    T('⑪之七 巡印判之降级：停摆→附 run_workflow 与降级之令（丙 enabled true、乙 cron :47·各名其号；甲⛔动）；私→自停之由并降级；'
      'rc 5→7 复常之印在沙盒之巡（丙 enabled false、乙 cron :57）',
      兜底之改(True) == 'update_trigger %s（丙）之 enabled「true」；update_trigger %s（乙）之 cron_expression「47 * * * *」' % (_号['丙'], _号['乙'])
      and 兜底之改(False) == 'update_trigger %s（丙）之 enabled「false」；update_trigger %s（乙）之 cron_expression「57 * * * *」' % (_号['丙'], _号['乙'])
      and 兜底之改(True) in _降印 and ':07 :27 :47' in _降印 and _号['甲'] not in _降印 and 'cron「' not in _降印
      and 'run_workflow' in 巡印判({'时': _今 - 巡印之限分 * 60 - 120}, _今) and 兜底之改(True) in 巡印判({'时': _今 - 巡印之限分 * 60 - 120}, _今)
      and '私有' in _私印 and 兜底之改(True) in _私印 and 巡印判({'时': _今, '私': False}, _今) == ''
      and 'return 7' in _段巡 and '兜底之改(False)' in _段巡 and 'return 6' in _段巡
      and _段巡.index('return 5') < _段巡.index('return 7') < _段巡.index('return 6') < _段巡.index("print('止')"))
    T('⑪之八 云巡：仓私即自停（disable·在唤之前）、唤而未应即红；红随唤（不唤之跑⛔红）；落巡印记所判之心跳',
      '私停(仓, 今)' in _段云 and _段云.index('私停(仓, 今)') < _段云.index('哨PR(仓)') and '应判(' in _段云
      and "return 0\n" in _段云.split('if not 唤:')[1].split('体 =')[0] and '心=d' in _段云 and '_巡之心' in _段云
      and '/disable' in src.split('def 私停(')[1].split('\ndef ')[0])
    T('⑦之四 诸印之令俱指 --派令（⛔手拟【派】）', src.count('--派令 %s') >= 2 and '令「【派】开第' not in src)
    _起们 = []
    _原迹存 = os.environ.pop('ZM_TRACE_SAVE', None)
    try:
        迹存('t', 起=lambda a, **k: _起们.append((a, k)))
    finally:
        if _原迹存 is not None:
            os.environ['ZM_TRACE_SAVE'] = _原迹存
    _段主 = open(os.path.abspath(__file__), encoding='utf-8').read().split("\nif __name__ == '__main__':")[1]
    T('X86 --候主／--派令 之末起後台之存（脱离、候三秒、⛔续心跳），迹先落而後存',
               len(_起们) == 1 and _起们[0][1].get('start_new_session') is True and 'sleep 3;' in _起们[0][0][2]
               and '--不续心跳 --存' in _起们[0][0][2] and '存底.py' in _起们[0][0][2]
               and _段主.split("'--派令' in a")[1].split('sys.exit')[0].count('迹存(') == 1
               and _段主.split("'--候主' in a")[1].split('sys.exit')[0].count('迹存(') == 1)
    _段巡沙 = _段主.split("if '--巡' in a:")[1].split('sys.exit(_rc)')[0] if "if '--巡' in a:" in _段主 else ''
    T('1119 沙盒之巡每跑验存底守在跑、不在即起（印归 stderr、⛔扰「止」）；GitHub 之巡⛔起',
      '_守.在跑()' in _段巡沙 and '_守.起()' in _段巡沙 and 'redirect_stdout(sys.stderr)' in _段巡沙
      and _段巡沙.index('_守.起()') > _段巡沙.index("GITHUB_ACTIONS") and _段巡沙.index('_守.起()') < _段巡沙.index('巡(查印=True)'))
    ok = sum(r)
    print('── 负测·接棒守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


def 迹存(说, 起=None):
    """X86（1105·425 还账）：--候主／--派令 之迹於本器退出时方由 _账 追入 _器之迹.jsonl，而其时锁已收、存底守已停——新坐承云端之迹即缺。
    故於二令之末起一後台之存（脱离本器、候三秒令本器先退而迹先落），零 token；⛔续心跳（锁已收：⛔复活）。ZM_TRACE_SAVE=0 即免（自测）。"""
    if os.environ.get('ZM_TRACE_SAVE') == '0':
        return None
    令 = 'sleep 3; %s %s --不续心跳 --存 %s >/dev/null 2>&1' % (
        sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), '存底.py'), json.dumps('交棒之迹·' + 说, ensure_ascii=False))
    try:
        return (起 or subprocess.Popen)(['sh', '-c', 令], cwd=_仓目(), start_new_session=True,
                                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return None


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
        治 = 派令之治(int(a[i + 1]))        # 1027 A2：前章未入主而报坏（或缺章标而存底有其封）→【重派】自其源起、先治
        令 = 派令(int(a[i + 1]), '--重' in a, 治=治)
        if 治:
            print('⛔ 第%d章未入主枝而须治（源「%s」）——派【重派】之会话自其源起、先治之（会话之守认此形）' % (int(a[i + 1]) - 1, 治))
        print('照下参调 create_trigger 一回（⛔改）：')
        print(json.dumps(令, ensure_ascii=False, indent=1))
        迹存('--派令 %s' % a[i + 1])
        sys.exit(0)
    if '--候主' in a:
        i = a.index('--候主')
        _rc = 候主(int(a[i + 1]), int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else 90)
        迹存('--候主 %s rc=%s' % (a[i + 1], _rc))
        sys.exit(_rc)
    if '--哨' in a:
        sys.exit(哨())
    if '--云巡' in a:
        sys.exit(云巡('--试' in a))
    if '--巡' in a:
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            sys.exit(巡())
        try:                         # 1119 作者令「及时备份……防沙盒突然重启」（法用#防失稿三锁）：每巡验本坐之存底守在跑、不在即起——
            import contextlib as _cl, 存底守 as _守   # 机换而开头之钩未跑之隙（1119 实踩：本坐 11-16 後三日无守、五十一档未存底）；零 token
            if not _守.在跑():
                with _cl.redirect_stdout(sys.stderr):
                    _守.起()
        except Exception as _e:
            sys.stderr.write('⚠ 存底守之验起不成：%s\n' % _e)
        _rc = 巡(查印=True)          # 沙盒（总编辑之坐）：验巡印、常对拍；每跑俱落巡应（云巡验其应）
        if not 落巡应(_rc):
            sys.stderr.write('⚠ 巡应落不成（备份/巡应·先 git remote set-url origin 正址）——云巡将以「唤而未应」红\n')
        sys.exit(_rc)
    if '--在候' in a:
        sys.exit(0 if 在候() else 1)
    if '--候' in a:
        i = a.index('--候')
        n = int(a[i + 1])
        分 = int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else 30
        sys.exit(候(n, 分))
    print(__doc__)
    sys.exit(0)
