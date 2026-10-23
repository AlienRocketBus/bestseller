#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""续跑之守（1023 立·坑㊻：406 容器重启後以 resumeFromRunId 直续，已交之五执笔连选俱重跑，白耗约 $60）——PreToolUse 钩（Workflow）。

【其由】resumeFromRunId 只回放「自首起连续皆有果」之 agent() 调用：一席失败（journal 只有 failed、无 result），
  其後之调用——已交者亦然——俱当场重跑。406：执笔·丙 撞产出之顶而败（另派「丙·补」），选席跑中容器重启；
  会话以 resumeFromRunId 续，甲乙回放，丙丁戊己庚五席重写（$53.8）、选再跑（$6.3）——七稿当时俱在盘上。
  此坑 393、397 已踩，1016 立 args.承、1017 立 `工具/承.py`、自走之派令亦印「先跑承.py」，然俱凭记性：⛔一闸拦之。
【其法】钩自 stdin 取 PreToolUse 之 JSON，tool_name 为 Workflow 者：
  ①带 resumeFromRunId：找其 journal；按调用之序（首 started 之序），首个无果之席其後若有已成之席，
    而此 run 係造章（有「执笔·」之席）→ 拦，印将重跑之席与续之正路（承.py → _承.js）。
    无果之席在末（如选席跑中而断）→ 放（只重跑那一席）；journal 不见 → 放（⛔凭猜拦）。
  ②新派造章——scriptPath 係 造章.js、或係包裹（_承.js 等，其文以 workflow() 调造章、args 定死於文）、或内联 script 调之——
    其 args 之 承 未盖尽 承.收(N) 所得（已交之稿、选、草、盲、审）→ 拦：无承即「新派即重写之」，有承即「承已旧、重跑承.py」。
    确要毁稿重造者，args 加 重造:true（总编辑之裁）：放行，并记重造之时（承.py 自此⛔收旧轮）。
  ①之 journal 不见、非造章、或属他章者，落到②再判（续错 run 号即全重跑）。
  造章之认（1023 审逮）：席名合 造章 之席（执笔·、选·、合稿、盲读、逻辑审·、回写、记席）——承之 run 无执笔之席亦认。
  非造章之 workflow、他器一概放（其无承之路，拦之即停书）。入坏、出错 → 放（本钩只防白耗，⛔挡书）。
用法：钩自 stdin 取 JSON；`python3 工具/续跑之守.py --自测`
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
诸journal之根 = os.environ.get('ZM_JOURNAL_ROOT') or os.path.expanduser('~/.claude/projects')   # 环境之注只供自测之子进程


def journal之路(run, 根=None):
    """→ run 之 journal 之路（无则 None）；run 只认 wf_ 之号（⛔路径之注）。"""
    if not re.fullmatch(r'wf_[A-Za-z0-9-]{4,}', str(run or '')):
        return None
    for p in glob.glob(os.path.join(根 or 诸journal之根, '*', '*', 'subagents', 'workflows', run, 'journal.jsonl')):
        return p
    return None


def 读(路):
    行 = []
    try:
        with open(路, encoding='utf-8', errors='replace') as f:
            for l in f:
                try:
                    行.append(json.loads(l))
                except ValueError:
                    pass
    except OSError:
        pass
    return 行


造章之席 = re.compile(r'^(执笔·|选·(行家兼两眼|补)$|合稿(·补)?$|盲读(·2|·补)?$|逻辑审·[12]$|回写$|记席(·补)?$)')


def 令首之章(路, 行):
    """→ journal 诸席之令首（agent-<id>.jsonl 首行）之「你是第 N 章的**」之 N（无则 None）。"""
    for d in 行:
        if d.get('type') != 'started' or not d.get('agentId'):
            continue
        try:
            with open(os.path.join(os.path.dirname(路), 'agent-%s.jsonl' % d['agentId']), encoding='utf-8', errors='replace') as f:
                m = re.search(r'你是第 (\d+) 章的\*\*', f.readline())
        except OSError:
            continue
        if m:
            return int(m.group(1))
    return None


def 续之判(行):
    """→ (将重跑之已成席之名［］, 首个无果之席名, 章号或 None, 係造章否)：照 resumeFromRunId 之回放（首个无果之调用起俱重跑）。"""
    序, 名, 成 = [], {}, set()
    章 = None
    for d in 行:
        t, k = d.get('type'), d.get('key')
        if t == 'started' and k and k not in 名:
            序.append(k)
            名[k] = d.get('label') or k[:12]
        elif t == 'result' and k and d.get('result') is not None:
            成.add(k)
            r = d.get('result')
            m = re.search(r'版本/第(\d+)章/', str(r.get('file', '')) if isinstance(r, dict) else '')
            if m and 章 is None:
                章 = int(m.group(1))
    造章 = any(造章之席.match(str(v)) for v in 名.values())
    for i, k in enumerate(序):
        if k not in 成:
            return [名[x] for x in 序[i + 1:] if x in 成], 名[k], 章, 造章
    return [], None, 章, 造章


def _参(入):
    参 = 入.get('tool_input') or {}
    a = 参.get('args')
    if isinstance(a, str):
        try:
            a = json.loads(a)
        except ValueError:
            a = {}
    return 参, (a if isinstance(a, dict) else {})


包裹之式 = re.compile(r"workflow\(\s*\{\s*scriptPath:\s*['\"][^'\"]*造章\.js['\"]\s*\}\s*,\s*(\{.*\})\s*\)", re.S)
转传之式 = re.compile(r"造章\.js[\x27\x22]\s*\}\s*,\s*args\s*\)")


def 派造章之参(参, a):
    """→ 新派造章之 args（含 章）；非新派造章、或认不出者 None。
    scriptPath 係 造章.js → tool_input.args；係他档而其文以 workflow() 调造章（_承.js 等包裹）→ 其文中定死之 args；
    内联 script 调造章 → 文中之字面 args，或其转传之 tool_input.args。"""
    sp = str(参.get('scriptPath') or '')
    if sp:
        if os.path.basename(sp) == '造章.js':
            return a
        try:
            p = sp if os.path.isabs(sp) else os.path.join(ROOT, sp)
            if os.path.getsize(p) > 512 * 1024:
                return None
            文 = open(p, encoding='utf-8', errors='replace').read()
        except OSError:
            return None
    else:
        文 = str(参.get('script') or '')
    if '造章.js' not in 文:
        return None
    m = 包裹之式.search(文)
    if m:
        try:
            return json.loads(m.group(1))
        except ValueError:
            pass
        if 转传之式.search(文):
            return a
        字 = m.group(1)
        n = re.search(r'["\']?章["\']?\s*:\s*(\d+)', 字)
        if not n:
            return None
        return {'章': int(n.group(1)), '重造': bool(re.search(r'["\']?重造["\']?\s*:\s*true', 字)),
                '承': {'?': 1} if re.search(r'["\']?承["\']?\s*:', 字) else None, '_字面': True}
    if 转传之式.search(文):
        return a
    return None


def _令(n, a, 末=''):
    """承.py 之全令（带 重、魂路、裁——旧只印 `承.py N`，无旧 _承.json 时当场 SystemExit）。"""
    c = 'python3 工具/承.py %s' % n
    if a.get('重'):
        c += ' --重 %s' % a['重']
    if isinstance(a.get('魂路'), list) and a['魂路']:
        c += ' --魂路 %s' % ','.join(str(x) for x in a['魂路'])
    if isinstance(a.get('裁'), str) and a['裁'].strip():
        c += " --裁 '%s'" % a['裁'].strip().replace("'", '’')
    return '`%s`%s' % (c, 末)


def 判(入, 根=None, root=None, 收=None, 记=None):
    """→ (拦否, 由)。收(n) → 承.收 之果；记(n) → 记重造（自测注之）。"""
    if (入.get('tool_name') or '') != 'Workflow':
        return False, ''
    参, a = _参(入)
    run = 参.get('resumeFromRunId')
    if run:
        p = journal之路(run, 根)
        if p:
            行 = 读(p)
            将重, 首缺, 章, 造章 = 续之判(行)
            if 造章:
                章 = 章 or 令首之章(p, 行) or (a.get('章') if isinstance(a.get('章'), int) else None)
                if 将重:
                    n = str(章) if 章 else 'N'
                    return True, ('⛔续跑之守（坑㊻·406 白耗约 $60）：resumeFromRunId 只回放首个无果之席（%s）以前者——其後已成之 %d 席（%s）将俱重跑。'
                                  '改走承之路：%s（收诸 journal 已成之段与盘稿、写 版本/第%s章/_承.js，补自带）→ '
                                  "Workflow({scriptPath:'%s'})。" % (首缺, len(将重), '、'.join(将重), _令(n, a), n,
                                                                     os.path.join(root or ROOT, '版本', '第%s章' % n, '_承.js')))
                if not (isinstance(a.get('章'), int) and 章 and a['章'] != 章):
                    return False, ''          # 造章之续、无缺：俱自缓存回放
        # journal 不见、非造章、或属他章 → 落到②（续错 run 号即全重跑）
    x = 派造章之参(参, a)
    if not isinstance(x, dict):
        return False, ''
    try:
        n = int(x.get('章'))
    except (TypeError, ValueError):
        return False, ''
    if x.get('重造') is True:
        try:
            (记 or (lambda n: __import__('承').记重造(n)))(n)
        except Exception:
            pass
        return False, ''
    if 收 is None:
        import 承 as _承
        收 = lambda n: _承.收(n, glob.glob(os.path.join(根 or 诸journal之根, '*', '*', 'subagents', 'workflows', '*', 'journal.jsonl')),
                            root=root or ROOT)[0]
    已 = 收(n) or {}
    承 = x.get('承') if isinstance(x.get('承'), dict) else {}
    if x.get('_字面') and 承:
        return False, ''                  # 内联之字面带承：认不出其细，照放
    有 = {os.path.realpath(str(d.get('file', ''))) for d in (承.get('诸稿') or []) if isinstance(d, dict)}
    缺稿 = [d for d in (已.get('诸稿') or []) if os.path.realpath(str(d.get('file', ''))) not in 有]
    缺段 = [k for k in ('选', '草', '盲', '审') if k in 已 and k not in 承]
    if not (缺稿 or 缺段):
        return False, ''
    包 = os.path.join(root or ROOT, '版本', '第%d章' % n, '_承.js')
    缺 = '、'.join([os.path.basename(str(d.get('file', ''))) for d in 缺稿] + 缺段)
    if not 承:
        return True, ('⛔续跑之守（坑㊻）：第%d章已有已成之段（%s）——新派造章即重写之。走承之路：%s → Workflow({scriptPath:\'%s\'})；'
                      '确要毁稿重造，args 加 重造:true（总编辑之裁；承.py 自此⛔收旧轮）。' % (n, 缺, _令(n, x), 包))
    return True, ('⛔续跑之守（坑㊻）：此派所带之承已旧——未盖第%d章已成之 %s（照派即重跑之）。先重跑 %s 更新 _承.js，再 Workflow({scriptPath:\'%s\'})；'
                  '确要毁稿重造，args 加 重造:true。' % (n, 缺, _令(n, x), 包))


def 自测():
    import tempfile
    import subprocess
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    def 席(行, k, 名, 果='成', 档=None):
        行.append({'type': 'started', 'key': k, 'agentId': 'a' + k, 'label': 名, 'phase': '造'})
        if 果 == '成':
            行.append({'type': 'result', 'key': k, 'agentId': 'a' + k, 'result': {'file': 档 or '/x/版本/第406章/起草_稿%s.md' % k}})
        elif 果 == '败':
            行.append({'type': 'failed', 'key': k, 'agentId': 'a' + k})

    with tempfile.TemporaryDirectory() as d:
        def 写j(run, 行):
            p = os.path.join(d, 'p', 's', 'subagents', 'workflows', run, 'journal.jsonl')
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                f.write('{"type":"launched"}\n' + ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in 行))
        R = lambda run: {'tool_name': 'Workflow', 'tool_input': {'scriptPath': '工具/席/造章.js', 'resumeFromRunId': run}}
        行 = []
        for k, 名, 果 in [('1', '执笔·甲·换账', '成'), ('2', '执笔·乙·翻个儿', '成'), ('3', '执笔·丙·不说', '败'),
                         ('4', '执笔·丁·速度', '成'), ('5', '执笔·戊·物证', '成'), ('6', '执笔·己·咬合', '成'),
                         ('7', '执笔·庚·回声', '成'), ('8', '执笔·丙·补', '成'), ('9', '选·行家兼两眼', '断')]:
            席(行, k, 名, 果)
        写j('wf_406a-001', 行)
        拦, 由 = 判(R('wf_406a-001'), 根=d)
        T('①406 之实：丙败、丁至补已成、选断 → 拦，点名将重跑之五席与补、印承.py 406',
          拦 and '执笔·丁·速度' in 由 and '执笔·丙·补' in 由 and '承.py 406' in 由 and '执笔·甲' not in 由)
        行 = []
        for k, 名 in [('1', '执笔·甲'), ('2', '执笔·乙'), ('3', '执笔·丙')]:
            席(行, k, 名)
        席(行, '4', '选·行家兼两眼', '断')
        写j('wf_tail-001', 行)
        T('②唯末一席（选）断、其前俱成 → 放（只重跑那一席）', not 判(R('wf_tail-001'), 根=d)[0])
        行 = []
        for k, 名 in [('1', '执笔·甲'), ('2', '执笔·乙'), ('3', '选·行家兼两眼')]:
            席(行, k, 名)
        写j('wf_done-001', 行)
        T('③俱成 → 放', not 判(R('wf_done-001'), 根=d)[0])
        行 = []
        席(行, '1', '攻·一', '败')
        席(行, '2', '攻·二')
        写j('wf_other-01', 行)
        T('④非造章之 workflow（无执笔）同式 → 放（其无承之路，⛔停书）', not 判(R('wf_other-01'), 根=d)[0])
        T('⑤journal 不见、run 号不合式（路径之注）→ 放', not 判(R('wf_none-001'), 根=d)[0] and not 判(R('../../etc'), 根=d)[0])
        行 = []
        席(行, '1', '执笔·甲', '败')
        席(行, '1', '执笔·甲')
        席(行, '2', '执笔·乙', '断')
        席(行, '3', '执笔·丙')
        写j('wf_twice-01', 行)
        拦, 由 = 判(R('wf_twice-01'), 根=d)
        T('⑥同键前败後成（续过一回）以成计、序以首起 → 首缺乙、拦丙', 拦 and '执笔·丙' in 由 and '（执笔·乙）' in 由)
        # ⛔自测一律用假章（9），并注 记（⛔写真仓之 承_重造.json——写了即令真章之承.py ⛔收其旧 journal）
        记们 = []
        记 = 记们.append
        F = lambda **a: {'tool_name': 'Workflow', 'tool_input': {'scriptPath': '工具/席/造章.js', 'args': dict({'章': 9, '重': '重', '魂路': ['换账', '不说']}, **a)}}
        有 = lambda n: {'诸稿': [{'file': '/x/版本/第9章/起草_稿甲.md'}], '选': {'ranking': []}} if n == 9 else {}
        拦, 由 = 判(F(), 收=有, 记=记)
        T('⑦新派造章·本章已有已交之稿·无承 → 拦，印全令（带 --重 --魂路）', 拦 and '承.py 9 --重 重 --魂路 换账,不说' in 由)
        T('⑦之二 承盖尽已成（诸稿与选）→ 放；他章无稿 → 放', not 判(F(承={'诸稿': [{'file': '/x/版本/第9章/起草_稿甲.md'}], '选': {}}), 收=有, 记=记)[0]
          and not 判(F(章=8), 收=有, 记=记)[0])
        T('⑦之三 承未盖尽（缺稿、或缺选、或 承:{诸稿:[]}）→ 拦「承已旧」', all(判(F(承=c), 收=有, 记=记)[0] for c in (
            {'诸稿': []}, {'诸稿': [{'file': '/x/版本/第9章/起草_稿甲.md'}]}, {'选': {}})) and '承已旧' in 判(F(承={'诸稿': []}), 收=有, 记=记)[1])
        T('⑦之四 重造:true → 放，且记重造之时（承.py 自此⛔收旧轮）', not 判(F(重造=True), 收=有, 记=记)[0] and 记们 == [9])
        T('⑦之五 args 以 JSON 之串传 → 照认而拦', 判({'tool_name': 'Workflow', 'tool_input': {
            'scriptPath': '/home/user/the-novel/工具/席/造章.js', 'args': '{"章": 9, "重": "重"}'}}, 收=有, 记=记)[0])
        包档 = os.path.join(d, '_承.js')
        def 包(承):
            open(包档, 'w', encoding='utf-8').write("export const meta = {name: 'x'}\nreturn await workflow({ scriptPath: '/r/工具/席/造章.js' }, %s)\n"
                                                    % json.dumps({'章': 9, '重': '重', '魂路': ['换账'], '承': 承}, ensure_ascii=False))
            return {'tool_name': 'Workflow', 'tool_input': {'scriptPath': 包档}}
        T('⑦之六 包裹（_承.js）其承已旧（後又成选）→ 拦；新者 → 放（审逮：旧只认 造章.js 之名，包裹俱放）',
          判(包({'诸稿': [{'file': '/x/版本/第9章/起草_稿甲.md'}], '补': True}), 收=有, 记=记)[0]
          and not 判(包({'诸稿': [{'file': '/x/版本/第9章/起草_稿甲.md'}], '选': {}, '补': True}), 收=有, 记=记)[0])
        内 = lambda sc, a=None: {'tool_name': 'Workflow', 'tool_input': dict({'script': sc}, **({'args': a} if a else {}))}
        T('⑦之七 内联 script 以 workflow() 调造章：字面无承 → 拦；字面带承 → 放（认不出其细）；转传 args → 照 args 判',
          判(内("return await workflow({scriptPath:'工具/席/造章.js'}, {章: 9})"), 收=有, 记=记)[0]
          and not 判(内("return await workflow({scriptPath:'工具/席/造章.js'}, {章: 9, 承: {}})"), 收=有, 记=记)[0]
          and 判(内("return await workflow({scriptPath:'工具/席/造章.js'}, args)", {'章': 9}), 收=有, 记=记)[0])
        T('⑧他器（Bash 等）、非造章之 scriptPath → 放', not 判({'tool_name': 'Bash', 'tool_input': {'command': 'ls'}}, 根=d)[0]
          and not 判({'tool_name': 'Workflow', 'tool_input': {'scriptPath': '工具/席/大审.js', 'args': {'起': 1}}}, 收=有, 记=记)[0])
        # ⑨承.收 真接得上：已交之稿其档在 → 认；档已不在 → ⛔认（稿被覆或挪走）
        ch = os.path.join(d, 'repo', '版本', '第9章')
        os.makedirs(ch)
        稿档 = os.path.join(ch, '起草_稿甲.md')
        open(稿档, 'w').write('x')
        行 = []
        席(行, '1', '执笔·甲·换账', '成', 稿档)
        写j('wf_real-409', 行)
        import 承 as _承
        原时 = _承.重造之时
        _承.重造之时 = lambda n, 档=None: 0.0          # ⛔读真仓之重造档
        try:
            T('⑨真收（承.收）：本章已交之稿档在 → 新派造章拦', 判(F(), 根=d, root=os.path.join(d, 'repo'), 记=记)[0])
            os.remove(稿档)
            T('⑨之二 稿档已不在 → 放', not 判(F(), 根=d, root=os.path.join(d, 'repo'), 记=记)[0])
        finally:
            _承.重造之时 = 原时
        # ⑫承之 run（无执笔之席）：选败、选·补与合稿已成、盲读断 → 续之即重跑选·补、合稿 → 拦（审逮：旧只认执笔·）
        行 = []
        席(行, '1', '选·行家兼两眼', '败')
        席(行, '2', '选·补', '成', '/x/选')
        席(行, '3', '合稿', '成', '/x/正文/第9章.md')
        席(行, '4', '盲读', '断')
        写j('wf_cheng-409', 行)
        a0 = os.path.join(d, 'p', 's', 'subagents', 'workflows', 'wf_cheng-409', 'agent-a1.jsonl')
        open(a0, 'w', encoding='utf-8').write(json.dumps({'message': {'content': '你是第 9 章的**选席**'}}, ensure_ascii=False) + '\n')
        拦, 由 = 判(R('wf_cheng-409'), 根=d)
        T('⑫承之 run 之续（无执笔之席）有缺 → 拦，章取令首（第 9 章）', 拦 and '选·补' in 由 and '合稿' in 由 and '承.py 9' in 由)
        # ⑬续错 run 号：journal 不见、非造章、或属他章 → 落到② 照新派判
        Rr = lambda run, n=9: {'tool_name': 'Workflow', 'tool_input': {'scriptPath': '工具/席/造章.js', 'resumeFromRunId': run, 'args': {'章': n}}}
        T('⑬续错 run 号（不见／非造章／他章之 run）而本章已有已成 → 落②而拦；本章之 run 无缺 → 放', 判(Rr('wf_none-001'), 根=d, 收=有, 记=记)[0]
          and 判(Rr('wf_other-01'), 根=d, 收=有, 记=记)[0] and 判(Rr('wf_done-001'), 根=d, 收=有, 记=记)[0]
          and not 判(Rr('wf_done-001', 406), 根=d, 收=有, 记=记)[0])
        T('⑭续之令带 --裁（致命未净之後总编辑之续：承之路接得住裁）', '--裁' in 判({'tool_name': 'Workflow', 'tool_input': {
            'scriptPath': '工具/席/造章.js', 'resumeFromRunId': 'wf_406a-001', 'args': {'章': 406, '重': '重', '魂路': ['换账'], '裁': '已亲治'}}}, 根=d)[1])
        env = dict(os.environ, ZM_STREAM='自测', ZM_JOURNAL_ROOT=d)
        p = subprocess.run([sys.executable, os.path.abspath(__file__)], input='{坏', capture_output=True, text=True, env=env)
        T('⑩入坏 → rc=0（⛔挡书）', p.returncode == 0)
        p = subprocess.run([sys.executable, os.path.abspath(__file__)], input=json.dumps(R('wf_406a-001')), capture_output=True, text=True, env=env)
        T('⑩之二 真跑：406 之续 → rc=2、stderr 印续跑之守', p.returncode == 2 and '续跑之守' in p.stderr)
    try:
        st = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8'))
        钩 = [e for e in (st.get('hooks') or {}).get('PreToolUse', []) for h in e.get('hooks', []) if '续跑之守' in h.get('command', '')]
        T('⑪settings 之 PreToolUse 挂本器，matcher 认 Workflow', bool(钩) and re.fullmatch(钩[0]['matcher'], 'Workflow') is not None)
        许 = (st.get('permissions') or {}).get('allow') or []
        T('⑪之二 承.py 已预授（拦後之正路⛔再被权限所卡）', any('工具/承.py' in x for x in 许))
    except Exception as e:
        T('⑪settings 读不出：%s' % e, False)
    ok = sum(r)
    print('── 负测·续跑之守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    if '--自测' in sys.argv[1:]:
        sys.exit(0 if 自测() else 1)
    try:
        入 = json.load(sys.stdin)
        拦, 由 = 判(入)
    except Exception:
        sys.exit(0)                      # 入坏、出错⛔拦（本钩只防白耗，⛔挡书）
    if 拦:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
