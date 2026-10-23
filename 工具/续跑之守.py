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
  ②新派 造章.js（scriptPath 或内联之 script 点到它）而 args 无 承、无 重造：第 N 章诸 journal 已有已交之稿（承.收）→ 拦。
    确要毁稿重造者，args 加 重造:true（总编辑之裁）。
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
诸journal之根 = os.path.expanduser('~/.claude/projects')


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
    造章 = any(str(v).startswith('执笔·') for v in 名.values())
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


def 派造章之章(参, a):
    """→ 新派造章之章号（非新派造章者 None）：scriptPath 点到 造章.js、或内联 script 以 workflow() 调之。"""
    sp = str(参.get('scriptPath') or '')
    if os.path.basename(sp) == '造章.js':
        try:
            return int(a.get('章'))
        except (TypeError, ValueError):
            return None
    sc = str(参.get('script') or '')
    if '造章.js' in sc and not sp:
        if re.search(r'["\']?承["\']?\s*:', sc) or re.search(r'["\']?重造["\']?\s*:\s*true', sc):
            return None
        m = re.search(r'["\']?章["\']?\s*:\s*(\d+)', sc)
        return int(m.group(1)) if m else None
    return None


def 判(入, 根=None, root=None, 收=None):
    """→ (拦否, 由)。"""
    if (入.get('tool_name') or '') != 'Workflow':
        return False, ''
    参, a = _参(入)
    run = 参.get('resumeFromRunId')
    if run:
        p = journal之路(run, 根)
        if not p:
            return False, ''
        将重, 首缺, 章, 造章 = 续之判(读(p))
        if not (造章 and 将重):
            return False, ''
        n = str(章) if 章 else 'N'
        return True, ('⛔续跑之守（坑㊻·406 白耗约 $60）：resumeFromRunId 只回放首个无果之席（%s）以前者——其後已成之 %d 席（%s）将俱重跑。'
                      '改走承之路：`python3 工具/承.py %s`（收诸 journal 已成之段、写 版本/第%s章/_承.js；诸稿不足三者照其印加「补」）→ '
                      "Workflow({scriptPath:'%s'})。" % (首缺, len(将重), '、'.join(将重), n, n,
                                                         os.path.join(root or ROOT, '版本', '第%s章' % n, '_承.js')))
    n = 派造章之章(参, a)
    if n is None or a.get('承') or a.get('重造') is True:
        return False, ''
    if 收 is None:
        import 承 as _承
        收 = lambda n: _承.收(n, glob.glob(os.path.join(根 or 诸journal之根, '*', '*', 'subagents', 'workflows', '*', 'journal.jsonl')),
                            root=root or ROOT)[0]
    已 = 收(n).get('诸稿') or []
    if not 已:
        return False, ''
    return True, ('⛔续跑之守（坑㊻）：第%d章诸 journal 已有已交之稿 %d 份（%s）——新派造章即重写之。'
                  '走承之路：`python3 工具/承.py %d` → Workflow({scriptPath:\'%s\'})；'
                  '确要毁稿重造，args 加 重造:true（总编辑之裁，记其由）。' % (
                      n, len(已), '、'.join(os.path.basename(str(x.get('file', ''))) for x in 已), n,
                      os.path.join(root or ROOT, '版本', '第%d章' % n, '_承.js')))


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
        F = lambda **a: {'tool_name': 'Workflow', 'tool_input': {'scriptPath': '工具/席/造章.js', 'args': dict({'章': 407}, **a)}}
        有 = lambda n: {'诸稿': [{'file': '/x/版本/第407章/起草_稿甲.md'}]} if n == 407 else {}
        T('⑦新派造章·第407章已有已交之稿·无承 → 拦', 判(F(), 收=有)[0])
        T('⑦之二 args 带 承、或 重造:true → 放；他章无稿 → 放', not 判(F(承={'诸稿': []}), 收=有)[0]
          and not 判(F(重造=True), 收=有)[0] and not 判(F(章=408), 收=有)[0])
        T('⑦之三 args 以 JSON 之串传 → 照认而拦', 判({'tool_name': 'Workflow', 'tool_input': {
            'scriptPath': '/home/user/the-novel/工具/席/造章.js', 'args': '{"章": 407, "重": "重"}'}}, 收=有)[0])
        T('⑦之四 _承.js 之包裹（scriptPath 非造章）→ 放', not 判({'tool_name': 'Workflow', 'tool_input': {
            'scriptPath': '版本/第407章/_承.js'}}, 收=有)[0])
        T('⑦之五 内联 script 以 workflow() 调造章、无承 → 拦；带承 → 放',
          判({'tool_name': 'Workflow', 'tool_input': {'script': "return await workflow({scriptPath:'工具/席/造章.js'}, {章: 407})"}}, 收=有)[0]
          and not 判({'tool_name': 'Workflow', 'tool_input': {'script': "return await workflow({scriptPath:'工具/席/造章.js'}, {章: 407, 承: {}})"}}, 收=有)[0])
        T('⑧他器（Bash 等）→ 放', not 判({'tool_name': 'Bash', 'tool_input': {'command': 'ls'}}, 根=d)[0])
        # ⑨承.收 真接得上：已交之稿其档在 → 认；档已不在 → ⛔认（稿被覆或挪走）
        ch = os.path.join(d, 'repo', '版本', '第407章')
        os.makedirs(ch)
        稿档 = os.path.join(ch, '起草_稿甲.md')
        open(稿档, 'w').write('x')
        行 = []
        席(行, '1', '执笔·甲·换账', '成', 稿档)
        写j('wf_real-407', 行)
        T('⑨真收（承.收）：第407章已交之稿档在 → 新派造章拦', 判(F(), 根=d, root=os.path.join(d, 'repo'))[0])
        os.remove(稿档)
        T('⑨之二 稿档已不在 → 放', not 判(F(), 根=d, root=os.path.join(d, 'repo'))[0])
        p = subprocess.run([sys.executable, os.path.abspath(__file__)], input='{坏', capture_output=True, text=True)
        T('⑩入坏 → rc=0（⛔挡书）', p.returncode == 0)
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
