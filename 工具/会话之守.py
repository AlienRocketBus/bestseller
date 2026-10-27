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
     1024 起交棒⛔经总编辑另查——令含「第N章」之写书会话，本钩一并验：参须与 `接棒守.派之参` 逐键同（⛔手拟）、
     第N章云端已封即拦、第N-1章未入主枝即拦（新会话自主枝起，见不到前章）；总编辑醒来只照【派】所带之参调一回。
  ③之守书（1024）：暂停令已解而「守书已停」之记仍在 → 拦开写书之会话，印复开守书之巡之原样参（⛔守书停而书续，断流无人兜）。
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


def 章号(令):
    m = re.search(r'第\s*(\d+)\s*章', 令 or '')
    return int(m.group(1)) if m else None


def 前派(转录, 章, 今=None, 限=3600, 排=None, 近=20):
    """转录中 限 秒内有无 create_session 之令含同章号者。回其几分前（无则 None）。
    1022 治：⛔认此回之调用自身（钩跑时其 tool_use 已落转录）——排其 id；无 id 者，近 20 秒内者不认。"""
    今 = 今 or time.time()
    最 = None
    败 = set()                      # 被拦或出错之调用（tool_result is_error）⛔算已派
    try:
        with open(转录, encoding='utf-8') as f:
            for l in f:
                if '"is_error": true' in l or '"is_error":true' in l:
                    try:
                        for c in ((json.loads(l).get('message') or {}).get('content') or []):
                            if isinstance(c, dict) and c.get('type') == 'tool_result' and c.get('is_error'):
                                败.add(c.get('tool_use_id'))
                    except Exception:
                        pass
    except Exception:
        return None
    try:
        with open(转录, encoding='utf-8') as f:
            for l in f:
                if 'create_session' not in l:
                    continue
                try:
                    d = json.loads(l)
                except Exception:
                    continue
                for c in ((d.get('message') or {}).get('content') or []):
                    if isinstance(c, dict) and c.get('type') == 'tool_use' and 器名(c.get('name')) == 'create_session' \
                            and 章号(str((c.get('input') or {}).get('prompt') or '')) == 章:
                        if (排 and c.get('id') == 排) or c.get('id') in 败:
                            continue
                        t = _时(d.get('timestamp'))
                        if t and (排 or 今 - t > 近) and 0 <= 今 - t <= 限 and (最 is None or t > 最):
                            最 = t
    except Exception:
        return None
    return None if 最 is None else int((今 - 最) // 60)


def 停读():
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 暂停令
        return bool(暂停令.在(ROOT)[0])
    except Exception:
        return False


def 守书停读():
    """→ 红由（''＝无事）：令已解而「守书已停」之记仍在（暂停令.守书之哨）。读不出⛔拦（此守係兜底，非主闸）。"""
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 暂停令
        return '；'.join(暂停令.守书之哨(ROOT))
    except Exception:
        return ''


def 守书停参():
    try:
        import 暂停令
        if 暂停令.守书停记():
            return ''
        return '；守书之巡未记停者照此调：%s，调毕 `暂停令.py --守书已停`' % 暂停令.守书之参(False)
    except Exception:
        return ''


def 立停读():
    try:
        sys.path.insert(0, os.path.join(ROOT, '工具'))
        import 心跳
        心跳.立停()
    except Exception:
        pass


def 派查(章, 参, 封=None, 主=None):
    """1024：写书之会话之参⛔手拟——逐键比 `接棒守.派之参`；第章已封、前章未入主枝俱拦。回 (拦?, 由)。⛔另造尺：封与主含取 自走、接棒守 之器。"""
    sys.path.insert(0, os.path.join(ROOT, '工具'))
    import 接棒守
    正 = 接棒守.派之参(章, '【重派】' in str(参.get('prompt') or ''))
    差 = [k for k in 正 if 参.get(k) != 正[k]]
    if 差:
        return True, ('⛔会话之守：开写书会话之参⛔手拟（%s 不合）——原样用此参再调一回：%s'
                      % ('、'.join(差), json.dumps(正, ensure_ascii=False)))
    if 封 is None:
        import 自走
        封 = 自走.云端已封
    if 封(章):
        return True, ('⛔会话之守：第%d章云端已封（有「章-%d」之标）——⛔重写；该开第%d章（`python3 工具/接棒守.py --派令 %d`）'
                      % (章, 章, 章 + 1, 章 + 1))
    if not (主 or 接棒守.主含)(章 - 1):
        return True, ('⛔会话之守：第%d章未入主枝——新会话自主枝起、见不到前章；先 `python3 工具/接棒守.py --候主 %d`，'
                      '其报红即照其红治（`python3 工具/推.py` 交 GitHub）、拒或逾时即 `python3 工具/推.py --直`，再派' % (章 - 1, 章 - 1))
    return False, ''


def 判(入, 转录读=新查, 锁读=锁之主, 我=None, 查=None):
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
        令 = str(参.get('prompt') or '')
        if 守书之记 in 令:
            return False, ''          # 守书之会话（只查、⛔写书）⛔与写书之坐争锁（1022）
        # 1022 复核：①作者暂停令在 → ⛔开写书之会话，并立停锁令守书⛔每时空派；②一时内已派同章之会话 → ⛔再派（一派数令之重）
        if 停读():
            立停读()
            return True, '⛔会话之守：作者暂停令在——⛔开写书之会话（已立停锁，守书⛔再派；解令 `暂停令.py --解` 即续）' + 守书停参()
        守 = 守书停读()
        if 守:
            return True, '⛔会话之守：先复开守书之巡再开写书之会话——' + 守.lstrip('⛔ ')
        章 = 章号(令)
        if 章 is not None:
            try:
                拦, 由 = (查 or 派查)(章, 参)
            except Exception as e:
                拦, 由 = True, '⛔会话之守：派查出错（%s）——fail closed；先 `python3 工具/接棒守.py --派令 %d` 取参、查网' % (e, 章)
            if 拦:
                return True, 由
        if 章 is not None and '【重派】' not in 令:
            前 = 前派(入.get('transcript_path') or '', 章, 排=入.get('tool_use_id'))
            if 前 is not None:
                return True, ('⛔会话之守：%d 分前已派第%d章之会话——⛔再派（数令同至）。先 get_session 看其状；'
                              '确已死或被拦方於令中加「【重派】」再开' % (前, 章))
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

    _判 = globals()['判']
    判 = lambda *a, **k: _判(*a, **dict({'查': lambda 章, 参: (False, '')}, **k))   # 旧格只验锁、重派、暂停；派查另验（⑧）
    # 1024 实踩：盘上暂停令真在时，③诸格读真令而误拦、且真调了 心跳.立停——自测⛔读盘上之令、⛔动真锁（⑦另以桩验暂停）
    _真停, _真立 = globals()['停读'], globals()['立停读']
    globals()['停读'], globals()['立停读'] = (lambda: False), (lambda: None)
    _真守 = globals()['守书停读']; globals()['守书停读'] = lambda: ''   # 1024：⛔读盘上「守书已停」之记
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
    with tempfile.TemporaryDirectory() as d2:
        p2 = os.path.join(d2, 't.jsonl')
        now2 = time.time()
        def 派行(秒前, 令, id_='old'):
            ts = datetime.utcfromtimestamp(now2 - 秒前).strftime('%Y-%m-%dT%H:%M:%S.000Z')
            return json.dumps({'type': 'assistant', 'timestamp': ts, 'message': {'content': [
                {'type': 'tool_use', 'id': id_, 'name': 'mcp__Claude_Code_Remote__create_session', 'input': {'prompt': 令}}]}}) + '\n'
        open(p2, 'w').write(派行(1200, '写《镇冢秘术》第 404 章：先……'))
        g = globals()
        旧停 = g['停读']; g['停读'] = lambda: False
        try:
            建2 = lambda 令: {'tool_name': 'mcp__X__create_session', 'transcript_path': p2, 'tool_input': {'prompt': 令}}
            T('⑥二十分前已派第404章 → 再派第404章拦（数令同至之重）', 判(建2('写第404章'), 锁读=无锁, 我='M')[0])
            T('⑥之二 令带【重派】 → 放（确已死方用）', not 判(建2('【重派】写第404章'), 锁读=无锁, 我='M')[0])
            T('⑥之三 他章（第405章）→ 放', not 判(建2('写第 405 章'), 锁读=无锁, 我='M')[0])
            open(p2, 'w').write(派行(4000, '写第 404 章'))
            T('⑥之四 逾一时之前派 → 放', not 判(建2('写第404章'), 锁读=无锁, 我='M')[0])
            open(p2, 'w').write(派行(1, '写第405章', 'cur'))
            T('⑥之五 转录中只此回之调用自身（同 id）→ 放（1022 实踩：自拦自）',
              not 判(dict(建2('写第405章'), tool_use_id='cur'), 锁读=无锁, 我='M')[0])
            T('⑥之六 无 id 而只二十秒内之一笔（此回自身）→ 放', not 判(建2('写第405章'), 锁读=无锁, 我='M')[0])
            open(p2, 'w').write(派行(120, '写第405章', 'blk') + json.dumps({'type': 'user', 'message': {'content': [
                {'type': 'tool_result', 'tool_use_id': 'blk', 'is_error': True, 'content': 'hook error'}]}}) + '\n')
            T('⑥之七 前派被拦（tool_result is_error）⛔算已派 → 放', not 判(建2('写第405章'), 锁读=无锁, 我='M')[0])
            g['停读'] = lambda: True
            立了 = []
            旧立 = g['立停读']; g['立停读'] = lambda: 立了.append(1)
            T('⑦作者暂停令在 → 拦写书之会话，并立停锁', 判(建2('写第406章'), 锁读=无锁, 我='M')[0] and 立了)
            T('⑦之二 暂停中守书之会话照开', not 判(建2(守书之记 + '巡'), 锁读=无锁, 我='M')[0])
            g['停读'] = lambda: False
            g['守书停读'] = lambda: '⛔ 守书之巡仍停：…照此调一回：update_trigger {"trigger_id": "trig_x", "enabled": true}'
            拦守 = 判(建2('写第406章'), 锁读=无锁, 我='M')
            T('⑦之三 令已解而守书已停之记仍在 → 拦写书之会话、由带 enabled=true 之参；守书之会话照开（1024）',
              拦守[0] and '"enabled": true' in 拦守[1] and not 判(建2(守书之记 + '巡'), 锁读=无锁, 我='M')[0])
            g['守书停读'] = lambda: ''
            g['立停读'] = 旧立
        finally:
            g['停读'] = 旧停
    sys.path.insert(0, os.path.join(ROOT, '工具'))
    import 接棒守
    正 = 接棒守.派之参(411)
    真 = lambda **k: _判({'tool_name': 'mcp__X__create_session', 'tool_input': dict(正, **k)}, 锁读=无锁, 我='M',
                         查=lambda 章, 参: 派查(章, 参, 封=lambda n: False, 主=lambda n: True))
    旧停2 = globals()['停读']; globals()['停读'] = lambda: False
    try:
        T('⑧参原样（接棒守.派之参）→ 放', not 真()[0])
        T('⑧之二 模手拟（sonnet）→ 拦、由中带原样之参', 真(model='claude-sonnet-5-5')[0] and '"model": "claude-opus-5-5"' in 真(model='x')[1])
        T('⑧之三 枝手拟 → 拦', 真(source_revision='main')[0] and 真(outcome_branch='')[0])
        T('⑧之四 令手改一字 → 拦（⛔转令被改）', 真(prompt=正['prompt'] + '。')[0])
        T('⑧之五 重派之形（令首【重派】）→ 放', not _判({'tool_name': 'mcp__X__create_session', 'tool_input': 接棒守.派之参(411, True)},
            锁读=无锁, 我='M', 查=lambda 章, 参: 派查(章, 参, 封=lambda n: False, 主=lambda n: True))[0])
        T('⑧之六 第章云端已封 → 拦（⛔重写已封之章）', _判({'tool_name': 'mcp__X__create_session', 'tool_input': 正}, 锁读=无锁, 我='M',
            查=lambda 章, 参: 派查(章, 参, 封=lambda n: n == 411, 主=lambda n: True))[0])
        T('⑧之七 前章未入主枝 → 拦', _判({'tool_name': 'mcp__X__create_session', 'tool_input': 正}, 锁读=无锁, 我='M',
            查=lambda 章, 参: 派查(章, 参, 封=lambda n: False, 主=lambda n: n != 410))[0])
        def 崩(章, 参):
            raise RuntimeError('网断')
        T('⑧之八 派查崩 → 拦（fail closed）', _判({'tool_name': 'mcp__X__create_session', 'tool_input': 正}, 锁读=无锁, 我='M', 查=崩)[0])
        T('⑧之九 令无章号（试验之会话）⛔派查', not _判({'tool_name': 'mcp__X__create_session', 'tool_input': {'prompt': '【试】只读'}},
            锁读=无锁, 我='M', 查=崩)[0])
        T('⑧之十 守书之会话⛔派查', not _判({'tool_name': 'mcp__X__create_session', 'tool_input': {'prompt': 守书之记 + '第411章'}},
            锁读=无锁, 我='M', 查=崩)[0])
    finally:
        globals()['停读'] = 旧停2
    src = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    T('⑧之十一 默查係 派查、派查默取 自走.云端已封 与 接棒守.主含（⛔以注入之假充其验）',
      '(查 or 派查)(章, 参)' in src and '封 = 自走.云端已封' in src and '(主 or 接棒守.主含)(章 - 1)' in src)
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
    globals()['停读'], globals()['立停读'] = _真停, _真立
    globals()['守书停读'] = _真守
    自 = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[1]
    T('③之七 自测桩掉暂停之读与立停（盘上令在时③亦通、⛔动真锁）',
      "globals()['停读'], globals()['立停读'] = (lambda: False), (lambda: None)" in 自 and 自.index('_真停') < 自.index("T('③新开"))
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
