#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""会话之守（1021 立·402 之失）——PreToolUse 钩：动别的会话之前，由机器拦，⛔凭本坐记性。

【其由·402 之失】1021 16:24，总编辑凭 10:21 之旧状（「候批」）归档了正在封 402 之会话——归档即收其机，
  其五时半之稿未上云端，全没（约五十元）。病有四：凭旧状、写时无存底、存底互覆、归档无一器拦。
  此器治第一与第四；存底二病由 `工具/存底.py`（防覆）与 `工具/存底守.py`（後台十五分一存）治。

【所拦】（钩之 matcher 只认 mcp__…__ 诸会话之器；名之前缀两写——Claude_Code_Remote 与 claude-code-remote——俱认）
  ① archive_session：**一律拦**。闲会话之机平台自收，归档零益而可杀活；须清理者作者於界面手为。
     settings.json 之 permissions.deny 另禁一道（两锁，一坏一在）。
  ② interrupt_session：本会话之转录须五分钟内对同一会话跑过 get_session（实时之状）方放——⛔凭旧状。
  ③ create_session：云端心跳之锁（`工具/心跳.py`·四十五分）为他坐所持即拦——⛔同时两坐写同一章。
  其余（unarchive、get_session、list 诸器）放。钩自身出错：①照拦（fail closed）；②③亦拦并印由。
用法：钩自 stdin 取 JSON；`python3 工具/会话之守.py --自测`
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, json, re, time, subprocess
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
鲜限 = 300          # 秒：get_session 须在此内
禁 = ('archive_session',)
守书之记 = '【守书·⛔写书】'     # 令中带此记之会话只查不写，他坐持锁亦许开


def 器名(n):
    """mcp__Claude_Code_Remote__archive_session → archive_session；unarchive_session 照原名，⛔误认作 archive。"""
    return (n or '').split('__')[-1]


def _时(s):
    try:
        return datetime.fromisoformat(str(s).replace('Z', '+00:00')).timestamp()
    except Exception:
        return None


def _号(s):
    """session_01AB… 与 cse_01AB… 同一会话：去前缀比。"""
    return re.sub(r'^(session_|cse_)', '', str(s or '').strip())


def 新查(转录, 目标, 今=None, 限=鲜限):
    """转录中 限 秒内有 get_session(session_id=目标) 之调用否。回 (有否, 几秒前)。"""
    今 = 今 or time.time()
    最 = None
    try:
        with open(转录, encoding='utf-8') as f:
            for l in f:
                if 'get_session' not in l:
                    continue
                try:
                    d = json.loads(l)
                except Exception:
                    continue
                for c in ((d.get('message') or {}).get('content') or []):
                    if not isinstance(c, dict) or c.get('type') != 'tool_use':
                        continue
                    if 器名(c.get('name')) != 'get_session':
                        continue
                    if _号((c.get('input') or {}).get('session_id')) != _号(目标):
                        continue
                    t = _时(d.get('timestamp'))
                    if t and (最 is None or t > 最):
                        最 = t
    except Exception:
        return False, None
    if 最 is None:
        return False, None
    差 = 今 - 最
    return (0 <= 差 <= 限), int(差)


def 锁之主():
    """回 (有人持锁?, 坐, 章)。⛔另造尺：取 心跳.py 之 _远 与其限。"""
    sys.path.insert(0, os.path.join(ROOT, '工具'))
    import 心跳
    在, d = 心跳._远()
    if not 在 or not isinstance(d, dict) or d.get('章') is None:
        return False, '', None
    差 = int(time.time()) - int(d.get('时', 0) or 0)
    return (差 <= 心跳.限), str(d.get('坐') or ''), d.get('章')


def 判(入, 转录读=新查, 锁读=锁之主, 我=None):
    """纯判：回 (拦?, 由)。"""
    名 = 器名(入.get('tool_name'))
    参 = 入.get('tool_input') or {}
    if 名 in 禁:
        return True, ('⛔会话之守：归档会话一律禁（1021·402 之失：凭旧状归档正在封版之会话，其机被收，五时半之稿全没）。'
                      '闲会话之机平台自收，归档零益；要它停，先 get_session 看实时之状，再 send 一令请其存底收尾。')
    if 名 == 'interrupt_session':
        有, 秒 = 转录读(入.get('transcript_path') or '', 参.get('session_id'))
        if not 有:
            return True, ('⛔会话之守：打断 %s 前须五分钟内 get_session 看其实时之状（%s）——⛔凭旧状（402 之失）。'
                          % (参.get('session_id'), '末查 %d 秒前' % 秒 if 秒 is not None else '本会话未查过'))
        return False, ''
    if 名 == 'create_session':
        if 守书之记 in str(参.get('prompt') or ''):
            return False, ''          # 守书之会话（只查、⛔写书）⛔与写书之坐争锁（1022）
        try:
            持, 坐, 章 = 锁读()
        except Exception as e:
            return True, '⛔会话之守：心跳读不出（%s），新开会话不放——先 `python3 工具/心跳.py` 看锁' % e
        我 = _号(我 if 我 is not None else 我之坐())
        if 持 and _号(坐) != 我:
            return True, ('⛔会话之守：第%s章之锁为他坐（%s）所持——⛔另开会话同写（402 之失）。'
                          '先 get_session 看那一坐实时之状；其办毕撤锁（`心跳.py --收`）或逾四十五分不报，方可开。' % (章, 坐 or '未名'))
        return False, ''
    return False, ''


def 我之坐():
    sys.path.insert(0, os.path.join(ROOT, '工具'))
    try:
        import 心跳
        return 心跳.坐()
    except Exception:
        return os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID', '')


def 自测():
    import tempfile
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    无锁 = lambda: (False, '', None)
    他锁 = lambda: (True, '01OTHER', 402)
    我锁 = lambda: (True, '016MINE', 402)
    for 前 in ('mcp__Claude_Code_Remote__', 'mcp__claude-code-remote__'):
        T('①归档一律拦（%s）' % 前[:9], 判({'tool_name': 前 + 'archive_session', 'tool_input': {'session_id': 'session_x'}}, 锁读=无锁)[0])
    T('①之二 unarchive ⛔误拦', not 判({'tool_name': 'mcp__claude-code-remote__unarchive_session'}, 锁读=无锁)[0])
    T('①之三 get_session、list_sessions 放', not any(判({'tool_name': 'mcp__X__' + n}, 锁读=无锁)[0] for n in ('get_session', 'list_sessions', 'send_later')))
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 't.jsonl')
        now = time.time()
        def 行(秒前, sid, 名='mcp__Claude_Code_Remote__get_session'):
            ts = datetime.utcfromtimestamp(now - 秒前).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            return json.dumps({'type': 'assistant', 'timestamp': ts, 'message': {'content': [
                {'type': 'tool_use', 'name': 名, 'input': {'session_id': sid}}]}}) + '\n'
        open(p, 'w').write(行(4000, 'session_01AAA') + 行(60, 'session_01BBB'))
        入 = lambda sid: {'tool_name': 'mcp__Claude_Code_Remote__interrupt_session', 'transcript_path': p, 'tool_input': {'session_id': sid}}
        T('②打断：一分钟前查过 → 放', not 判(入('session_01BBB'), 锁读=无锁)[0])
        T('②之二 打断：六十六分前之旧状 → 拦', 判(入('session_01AAA'), 锁读=无锁)[0])
        T('②之三 打断：从未查过 → 拦', 判(入('session_01CCC'), 锁读=无锁)[0])
        T('②之四 cse_ 与 session_ 同号认作一会话', not 判(入('cse_01BBB'), 锁读=无锁)[0])
        open(p, 'w').write(行(30, 'session_01AAA', 'mcp__Claude_Code_Remote__list_sessions'))
        T('②之五 别器之调用⛔充 get_session', 判(入('session_01AAA'), 锁读=无锁)[0])
        T('②之六 转录读不出 → 拦', 判({'tool_name': 'mcp__X__interrupt_session', 'transcript_path': '/无/此档', 'tool_input': {'session_id': 's'}}, 锁读=无锁)[0])
    建 = {'tool_name': 'mcp__Claude_Code_Remote__create_session', 'tool_input': {}}
    T('③新开：无锁 → 放', not 判(建, 锁读=无锁, 我='016MINE')[0])
    T('③之二 新开：他坐持锁 → 拦', 判(建, 锁读=他锁, 我='016MINE')[0])
    T('③之三 新开：本坐持锁 → 放（封毕自开接班）', not 判(建, 锁读=我锁, 我='cse_016MINE')[0])
    T('③之六 守书之会话（令带【守书·⛔写书】）他坐持锁亦许开', not 判({'tool_name': 'mcp__X__create_session', 'tool_input': {'prompt': '你是' + 守书之记 + '……'}}, 锁读=他锁, 我='016MINE')[0])
    def 坏():
        raise RuntimeError('网断')
    T('③之四 心跳读不出 → 拦（fail closed）', 判(建, 锁读=坏, 我='016MINE')[0])
    T('③之五 未名之锁（旧坐）亦拦', 判(建, 锁读=lambda: (True, '未名', 403), 我='016MINE')[0])
    # ④钩之真跑：经 stdin、rc=2、stderr 有由
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], input=json.dumps(
        {'tool_name': 'mcp__claude-code-remote__archive_session', 'tool_input': {'session_id': 's'}}),
        capture_output=True, text=True)
    T('④真跑：归档 rc=2、由印於 stderr', p.returncode == 2 and '归档会话一律禁' in p.stderr)
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], input='不是 JSON', capture_output=True, text=True)
    T('④之二 入坏（非 JSON）→ rc=2（fail closed）', p.returncode == 2)
    # ⑤两锁俱在：settings.json 之 deny 与钩
    try:
        s = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8'))
        deny = (s.get('permissions') or {}).get('deny') or []
        T('⑤settings 之 permissions.deny 禁归档（两写俱在）',
          'mcp__Claude_Code_Remote__archive_session' in deny and 'mcp__claude-code-remote__archive_session' in deny)
        钩 = [h for e in (s.get('hooks') or {}).get('PreToolUse', []) for h in e.get('hooks', [])
             if '会话之守' in h.get('command', '') and re.search(e.get('matcher', '^$'), 'mcp__claude-code-remote__archive_session')
             and re.search(e.get('matcher', '^$'), 'mcp__Claude_Code_Remote__create_session')]
        T('⑤之二 PreToolUse 钩挂本器、matcher 两写俱中', bool(钩))
    except Exception as e:
        T('⑤settings 读不出：%s' % e, False)
    ok = sum(r)
    print('── 负测·会话之守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    if '--自测' in sys.argv[1:]:
        sys.exit(0 if 自测() else 1)
    try:
        入 = json.load(sys.stdin)
        拦, 由 = 判(入)
    except Exception as e:
        拦, 由 = True, '⛔会话之守：钩入读不出（%s）——fail closed' % e
    if 拦:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
