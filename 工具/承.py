#!/usr/bin/env python3
"""承.py——容器重启後，从诸 workflow 之 journal 收第 N 章已成之段，造 造章.js 之 args.承（版本/第N章/_承.json）与包裹（_承.js）。

为何立（1017·397 逮）：容器重启频（397 一章两回：执笔之半、选之半），每回主环手翻 journal、手认 label、
手拼 args.承——393、397、397 三回皆手办，易错（稿与执笔之对、丙稿成而未交者之补）。今一器办毕：
  python3 工具/承.py 397            # 扫诸 journal，收 397 之已成段，写 _承.json 与 _承.js，印续之令
  python3 工具/承.py 397 --印       # 只印所收，⛔写
  python3 工具/承.py 397 --再回写   # 「致命未净」（回写一回後复验仍读误／硬崩）：以 盲读·2、逻辑审·2 之果作 盲、审，⛔承回写——再走一回 回写→盲读→审→记席
  python3 工具/承.py 397 --裁 "总编辑之裁"   # 「致命未净」後总编辑亲治、续记（args.裁 写入 _承.js；旧 _承.json 之裁承之）
  python3 工具/承.py 411 --查 甲 版本/第411章/起草_稿三.md   # 查席之器（N≥411·造章.js 补派整席之前派之）：留前席构思之底、量之入账，验盘稿
  python3 工具/承.py --自测

1023（坑㊻·续跑之守之审所逮）：
  ①补自带：选未成者承.补 为 true——缺席之执笔由 造章.js 自判补否（宽足⛔补）；旧之「手加补」写不进 _承.js（包裹定死 args）、致不足三之环。
     选已成者⛔补（选不读补来之稿，补即白耗一执笔）。
  ②重造之界：续跑之守放行 args.重造 之新派时记其时（git 公目 承_重造.json）；此前之 journal、稿档与旧 _承.json（只留 重、魂路、须厚）⛔收。
  ③盘稿：journal 无果（他机之 journal、执笔交了稿而败於 StructuredOutput）而 版本/第N章/起草_稿*.md 在（≥200 字节、界後、有【本章亮点】——稿半⛔收）者亦收。
  ④盲读之壳（未交、被截）⛔收——承之即令造章.js 当场停於「盲读未交」、续之复停。

所收（label → 承之键）：执笔·*→诸稿（以 file 认，後者覆前者）；选·行家兼两眼／选·补→选；合稿／合稿·补→草；
盲读／盲读·补→盲；逻辑审·1→审；回写→回写（true）。盲读·2、逻辑审·2、记席⛔收（造章.js 之承不认之，照跑）。
稿档已不在者⛔收（稿被覆或挪走）。
1024（省 token 之审·records③／seats①·failures①）：
  ⑤拆键：N≥411 诸席共一通式，交为 {draft|pick|merge|blind|audit|rewrite: 旧式之果, flaws}——收时拆出其键；缺键、或缺其子式之必填者作未交⛔收
    （必填之表＝造章.js 通式诸子式之 required，负测_造章令.py 对之）；旧式之果原样。逻辑审·1·补 亦收作审。
  ⑥--查：缺稿之执笔补派之前，查席一跑——前席之构思逾 200 字节者抄留 起草_X_构思_前.md（⛔承·⛔mv：造式.py 认甲乙丙之构思、宽足⛔补时原档须在），
    零 token 量其魂、拍表（拍数）、满分之问、①—⑤，记入 版本/第N章/_补前稿账.json；盘稿在、有【本章亮点】、界後、净重过铁底、硬项零者印「稿：{…}」交回。args 之 章／重／魂路 取旧 _承.json，无则须 --重 与 --魂路。
⛔本器只读 journal、只写 版本/第N章/_承.json 与 _承.js；⛔git。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
诸journal之式 = os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/*/journal.jsonl')
键表 = [(re.compile(r'^执笔·'), '诸稿'), (re.compile(r'^选·(行家兼两眼|补)$'), '选'), (re.compile(r'^合稿(·补)?$'), '草'),
       (re.compile(r'^盲读(·补)?$'), '盲'), (re.compile(r'^逻辑审·1(·补)?$'), '审'), (re.compile(r'^回写$'), '回写')]
# ★1024 通式（N≥411）：承之键 → 通式之键（ASCII·坑⑩）与其子式之必填（照 造章.js 稿式、选式、合式、盲读式、崩式、写式之 required）
通键 = {'诸稿': 'draft', '选': 'pick', '草': 'merge', '盲': 'blind', '审': 'audit', '回写': 'rewrite'}
通之必 = {'draft': ['file', 'beats', 'words', 'soul'], 'pick': ['ranking', 'why', 'fatal', 'leap', 'common_fatal', 'beat_scores'],
         'merge': ['file', 'beats', 'words', 'base', 'gates', 'gates_green', 'ledger', 'recap'],
         'blind': ['understood', 'confused', 'misread', 'want_next', 'why_next', 'happened', 'remember', 'prior'],
         'audit': ['hard', 'soft', 'gate', 'misread'], 'rewrite': ['done'], 'record': ['done', 'left']}


def 式之键(l, 键们):
    return next((k for 式, k in 键们 if 式.search(l)), '')


def 拆(r, k, 通=True):
    """通（N≥411）：通式之果 → 其键之子（缺键、缺必填、交空者 None：作未交）；N≤410 原样。"""
    if not 通:
        return r
    if not isinstance(r, dict):
        return None
    键 = 通键.get(k, k)
    x = r.get(键)
    if not isinstance(x, dict) or any(x.get(f) is None for f in 通之必.get(键, [])):
        return None
    return x


盲未交 = lambda x: (not x) or bool(re.match(r'\s*(未交|未完成|未作答|未答)', str(x.get('happened', '')))) or bool(
    re.search(r'(安全分类器|分类器截|被截停|被拦下|safeguard)', str(x.get('happened', '')) + str(x.get('confused', '')) + str(x.get('why_next', '')), re.I))
盘稿之下限 = 200   # 字节：空档、半档⛔作稿


def _仓目():
    import subprocess
    try:
        p = subprocess.run(['git', 'rev-parse', '--git-common-dir'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if p:
            return p if os.path.isabs(p) else os.path.join(ROOT, p)
    except Exception:
        pass
    return os.path.join(ROOT, '.git')


def _重造档():
    return os.path.join(_仓目(), '承_重造.json')


def 重造之时(n, 档=None):
    """→ 第 n 章末一回重造之时（秒；无则 0）——此前之 journal 与稿档俱属旧轮。"""
    try:
        return float(json.load(open(档 or _重造档(), encoding='utf-8')).get(str(n), 0))
    except Exception:
        return 0.0


def 记重造(n, 档=None, 时=None):
    import time
    档 = 档 or _重造档()
    try:
        d = json.load(open(档, encoding='utf-8'))
    except Exception:
        d = {}
    d[str(n)] = 时 if 时 is not None else time.time()
    with open(档, 'w', encoding='utf-8') as o:
        json.dump(d, o)


def 读(路):
    行 = []
    try:
        with open(路, encoding='utf-8', errors='replace') as f:   # 截於半字之 journal ⛔崩（一份坏即诸章之承俱死）
            for l in f:
                try:
                    行.append(json.loads(l))
                except ValueError:
                    pass
    except OSError:
        pass
    return 行


def 首令属(路, 诸id, n):
    """承之 run 无执笔之果（选起）——以其席之令首（agent-<id>.jsonl 首行）有「你是第 n 章的**」认之（造章.js 七席之令俱有）。"""
    记 = '你是第 %d 章的**' % n
    for i in 诸id:
        try:
            with open(os.path.join(os.path.dirname(路), 'agent-%s.jsonl' % i), encoding='utf-8', errors='replace') as f:
                if 记 in f.readline():
                    return True
        except OSError:
            continue
    return False


def 收(n, 诸路, root=ROOT, 再=False, 界=None):
    """诸 journal 依 mtime 升序扫；属第 n 章之 run（有执笔之果其 file 在 版本/第n章/）方收；後者覆前者。
    界（重造之时，缺则取 承_重造.json）以前之 journal 与稿档⛔收；盲读之壳⛔收；journal 无果之盘稿亦收。"""
    界 = 重造之时(n) if 界 is None else 界
    章目 = os.path.join(root, '版本', '第%d章' % n) + os.sep
    承 = {}
    稿 = {}
    来 = []
    键们 = 键表 + ([(re.compile(r'^盲读·2$'), '盲'), (re.compile(r'^逻辑审·2(·补)?$'), '审')] if 再 else [])
    for 路 in sorted(诸路, key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0):
        try:
            if os.path.getmtime(路) < 界:
                continue
        except OSError:
            continue
        行 = 读(路)
        标 = {d.get('key'): d.get('label', '') for d in 行 if d.get('type') == 'started'}
        果 = [(标.get(d.get('key'), ''), d.get('result')) for d in 行 if d.get('type') == 'result']
        # 通式（N≥411）拆键；回写之果⛔拆（造章.js 不取其果，交了即算办过——缺 rewrite 键而重跑回写即白耗一席）
        果 = [(l, r if 式之键(l, 键们) in ('回写', '') else 拆(r, 式之键(l, 键们), n >= 411)) for l, r in 果]
        # 查席之稿 file 係相对之路（蒙档）——N≥411 依 root 补成绝对：否则其键与下盘稿之 glob 不同，一稿收两回、诸稿重名（怀疑者逮）
        果 = [(l, dict(r, file=os.path.join(root, r['file'])) if n >= 411 and l.startswith('执笔·') and isinstance(r, dict)
               and isinstance(r.get('file'), str) and r['file'] and not os.path.isabs(r['file']) else r) for l, r in 果]
        属 = any(isinstance(r, dict) and str(r.get('file', '')).startswith(章目) for l, r in 果 if l.startswith('执笔·')) \
            or 首令属(路, [d.get('agentId') for d in 行 if d.get('type') == 'started'], n)
        if not 属:
            continue
        来.append(路)
        for l, r in 果:
            for 式, k in 键们:
                if not 式.search(l) or r is None:
                    continue
                if k == '诸稿':
                    if isinstance(r, dict) and r.get('file') and os.path.exists(r['file']):
                        稿[r['file']] = r
                elif k == '回写':
                    承['回写'] = True
                elif k == '盲' and isinstance(r, dict) and 盲未交(r):
                    continue
                elif isinstance(r, dict):
                    承[k] = r
    for f in sorted(glob.glob(os.path.join(章目, '起草_稿*.md'))):
        try:
            if f in 稿 or os.path.getsize(f) < 盘稿之下限 or os.path.getmtime(f) < 界:
                continue
            if '【本章亮点】' not in open(f, encoding='utf-8', errors='replace').read():
                continue                         # 稿半（397「一席稿半」）⛔作已交——亮点与稿同一回写，无之即未写完，交补
            try:
                import 净重对表
                字 = 净重对表.净重(f)
            except Exception:
                字 = len(re.findall(r'[\u4e00-\u9fff]', open(f, encoding='utf-8', errors='replace').read()))
        except OSError:
            continue
        稿[f] = {'file': f, 'words': 字, 'beats': 0, 'soul': '（盘稿：journal 无其果）', '盘': True}
    if 稿:
        承['诸稿'] = list(稿.values())
    if 再:
        承.pop('回写', None)   # 再回写：回写⛔承——造章.js 见 审 有病即再派回写，以 审（逻辑审·2）之读误与硬崩为令
    return 承, 来


def 量构思(文):
    """前席构思之零 token 之量（failures① safeguard⑤：先三回实证其落全否，再议承前）。"""
    行 = 文.split('\n')
    表 = [l for l in 行 if l.startswith('|')]
    分 = any(re.match(r'^\|\s*-{3}', l) for l in 表)
    魂 = [l for l in 行 if l.startswith('魂')]
    满 = 文.split('满分之问', 1)[1] if '满分之问' in 文 else ''
    return {'字节': len(文.encode('utf-8')), '魂': bool(魂), '进化账所避': '进化账所避' in 文, '满分之问': bool(满),
            '写法数': len(re.findall(r'^\s*[-·]?\s*写法', 满.split('\n## ', 1)[0], re.M)) if 满 else 0,
            '拍表': '拍表' in 文 and 分, '拍数': max(0, len(表) - 2) if 分 else 0,
            '①—⑤': ''.join(c for c in '①②③④⑤' if c in 文)}


def 查(n, 名, 档, root=ROOT, 界=None, 时=None):
    """→ (稿 dict 或 None, 由)。抄留前席之构思、量之入 _补前稿账.json；验盘稿。"""
    import shutil
    import time
    界 = 重造之时(n) if 界 is None else 界
    章目 = os.path.join(root, '版本', '第%d章' % n)
    构 = os.path.join(章目, '起草_%s_构思.md' % 名)
    条 = {'时': 时 if 时 is not None else time.strftime('%m-%d %H:%M:%S'), '名': 名, '稿档': 档}
    魂 = ''
    if os.path.exists(构) and os.path.getsize(构) > 盘稿之下限:
        文 = open(构, encoding='utf-8', errors='replace').read()
        前 = os.path.join(章目, '起草_%s_构思_前.md' % 名)
        k = 2
        while os.path.exists(前):
            前 = os.path.join(章目, '起草_%s_构思_前%d.md' % (名, k))
            k += 1
        shutil.copy2(构, 前)
        条['构思_前'] = os.path.basename(前)
        条['量'] = 量构思(文)
        魂们 = [l for l in 文.split('\n') if l.startswith('魂')]
        魂 = 魂们[-1].split('：', 1)[-1].strip() if 魂们 else ''
    else:
        条['构思_前'] = None
    p = 档 if os.path.isabs(档) else os.path.join(root, 档)
    稿, 由 = None, ''
    if not os.path.exists(p) or os.path.getsize(p) < 盘稿之下限:
        由 = '稿档不在或不足 %d 字节' % 盘稿之下限
    elif os.path.getmtime(p) < 界:
        由 = '稿档在重造之界前（旧轮之稿）'
    elif os.path.exists(os.path.join(章目, '_料.md')) and os.path.getmtime(p) < os.path.getmtime(os.path.join(章目, '_料.md')):
        由 = '稿档早於 _料.md（前轮之稿·料已重出）'   # failures① safeguard①③：只收本轮料出之後之稿（怀疑者补）
    else:
        t = open(p, encoding='utf-8', errors='replace').read()
        if '【本章亮点】' not in t:
            由 = '稿无【本章亮点】（稿半）'
        else:
            try:
                import 净重对表
                字, 红 = 净重对表.稿之量(p)
            except Exception as e:
                字, 红 = 0, {'量不起': str(e)[:60]}
            if 红 or 字 < 2000:
                由 = '净重 %d%s' % (字, ('｜硬项 ' + '、'.join('%s %s' % kv for kv in 红.items())) if 红 else '｜低於铁底 2000')
            else:
                白 = t.split('【本章亮点】')[0].split('\n')
                稿 = {'file': 档, 'beats': sum(1 for l in 白 if l.strip() == '＊') + 1, 'words': 字,
                      'soul': 魂 or '（查席收盘稿：魂见构思）'}
                由 = '盘稿收（净重 %d、硬项零）' % 字
    条['稿'] = '收' if 稿 else '无'
    条['由'] = 由
    账 = os.path.join(章目, '_补前稿账.json')
    try:
        旧 = json.load(open(账, encoding='utf-8'))
    except Exception:
        旧 = []
    旧.append(条)
    os.makedirs(章目, exist_ok=True)
    with open(账, 'w', encoding='utf-8') as o:
        json.dump(旧, o, ensure_ascii=False, indent=1)
    return 稿, 由, 条


def 须厚判(n):
    try:
        import 造式验
        return 造式验.须厚之判(n)[0]
    except Exception:
        return None


def 造(n, 承, 旧=None, 重=None, 魂路=None, 再=False, 裁=None, 补=True, 界=0):
    旧 = 旧 or {}
    a = {'章': n, '重': 重 or 旧.get('重'), '魂路': 魂路 or 旧.get('魂路')}
    # ★1020 X40 驳席逮：重启续跑之 args 须带 须厚（旧 _承.json 有则承之；无则照 造式验.须厚之判 现算——与自走之派令同尺）；⛔丢则执笔令、选令之须厚条随之消失
    if 旧.get('须厚') or (n >= 401 and 须厚判(n) is True):
        a['须厚'] = True
    if not a['重'] or not a['魂路']:
        raise SystemExit('⛔承：无旧 _承.json 可取 重／魂路——须 --重 中 --魂路 物证,回声,不说（照 自走.py 之派令）')
    裁 = 裁 or 旧.get('裁')
    if isinstance(裁, str) and 裁.strip():
        a['裁'] = 裁.strip()                     # 造章.js：致命未净而有裁者越停续记
    旧承 = 旧.get('承') or {}
    合 = dict(旧承)
    合.pop('补', None)
    if 承.get('诸稿') or 旧承.get('诸稿'):
        by = {x['file']: x for x in (旧承.get('诸稿') or []) if os.path.exists(x.get('file', '')) and os.path.getmtime(x['file']) >= 界}
        by.update({x['file']: x for x in 承.get('诸稿', [])})
        合['诸稿'] = list(by.values())
    for k in ('选', '草', '盲', '审', '回写'):
        if k in 承:
            合[k] = 承[k]
    if isinstance(合.get('盲'), dict) and 盲未交(合['盲']):
        合.pop('盲')                             # 旧 _承.json 所带之盲读之壳⛔承（承之即停於盲读未交）
    if 补 and '选' not in 合:
        合['补'] = True                          # 1023：缺席之执笔由 造章.js 自判补否（宽足⛔补）；选已成⛔补（补来之稿选不读）
    if 再:
        合.pop('回写', None)
    a['承'] = 合
    return a


def 旧之滤(旧, 旧路, 界):
    """重造前之 _承.json：旧轮之选、草、盲、审、裁、稿⛔承，只留章之设（重、魂路、须厚）——1023 复核逮：只滤 收 而⛔滤旧档，重造之界形同虚设。"""
    if 旧 and 界 and os.path.getmtime(旧路) < 界:
        return {k: 旧[k] for k in ('重', '魂路', '须厚') if k in 旧}
    return 旧


def 包裹(a):
    已 = [k for k in ('选', '草', '盲', '审', '回写') if k in a['承']]
    return ("export const meta = {\n  name: '造章·%d·承',\n  description: '第%d章承已成之段（诸稿 %d%s）续跑',\n"
            "  phases: [{ title: '造' }, { title: '选' }, { title: '合' }, { title: '验' }, { title: '记' }],\n}\n"
            "return await workflow({ scriptPath: '%s' }, %s)\n"
            % (a['章'], a['章'], len(a['承'].get('诸稿', [])), ('、' + '、'.join(已)) if 已 else '',
               os.path.join(ROOT, '工具', '席', '造章.js'), json.dumps(a, ensure_ascii=False)))


def 自测():
    import tempfile
    R = []
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, '版本', '第9章'))
        for x in ('稿一', '稿二', '稿三'):
            open(os.path.join(t, '版本', '第9章', '起草_%s.md' % x), 'w').close()
        f = lambda x: os.path.join(t, '版本', '第9章', '起草_%s.md' % x)
        j1, j2, j3 = (os.path.join(t, 'j%d.jsonl' % i) for i in (1, 2, 3))
        def 写(p, 行):
            with open(p, 'w', encoding='utf-8') as o:
                o.write('\n'.join(json.dumps(x, ensure_ascii=False) for x in 行))
        写(j1, [{'type': 'started', 'key': 'a', 'label': '执笔·甲·物证'}, {'type': 'result', 'key': 'a', 'result': {'file': f('稿一'), 'words': 1}},
                {'type': 'started', 'key': 'b', 'label': '执笔·乙·回声'}])
        写(j2, [{'type': 'started', 'key': 'c', 'label': '执笔·乙·补'}, {'type': 'result', 'key': 'c', 'result': {'file': f('稿二'), 'words': 2}},
                {'type': 'started', 'key': 'g', 'label': '执笔·丙·补'}, {'type': 'result', 'key': 'g', 'result': {'file': f('稿四'), 'words': 4}},
                {'type': 'started', 'key': 'd', 'label': '选·行家兼两眼'}, {'type': 'result', 'key': 'd', 'result': {'ranking': ['稿二']}},
                {'type': 'started', 'key': 'e', 'label': '盲读·2'}, {'type': 'result', 'key': 'e', 'result': {'x': 1}},
                {'type': 'started', 'key': 'h', 'label': '回写'}, {'type': 'result', 'key': 'h', 'result': 'ok'}])
        写(j3, [{'type': 'started', 'key': 'z', 'label': '执笔·甲·物证'}, {'type': 'result', 'key': 'z', 'result': {'file': '/别处/版本/第8章/起草_稿一.md'}},
                {'type': 'started', 'key': 'y', 'label': '选·行家兼两眼'}, {'type': 'result', 'key': 'y', 'result': {'ranking': ['他章']}}])
        j4 = os.path.join(t, 'r4', 'journal.jsonl'); os.makedirs(os.path.dirname(j4))
        写(j4, [{'type': 'started', 'key': 'm', 'agentId': 'q1', 'label': '合稿'}, {'type': 'result', 'key': 'm', 'result': {'file': '正文'}}])
        写(os.path.join(t, 'r4', 'agent-q1.jsonl'), [{'message': {'content': '你是第 9 章的**合稿席'}}])
        os.utime(j1, (1, 1)); os.utime(j2, (2, 2)); os.utime(j3, (3, 3)); os.utime(j4, (4, 4))
        承, 来 = 收(9, [j1, j2, j3, j4], root=t, 界=0)
        R.append(('①只收属本章之 run（他章之 j3 ⛔收，其选⛔覆）；承之 run 以令首认章（j4 之合稿收）',
                  来 == [j1, j2, j4] and 承.get('选') == {'ranking': ['稿二']} and 承.get('草') == {'file': '正文'}))
        R.append(('②诸稿以 file 认、稿档不在者⛔收', sorted(x['file'] for x in 承['诸稿']) == [f('稿一'), f('稿二')]))
        R.append(('③盲读·2 ⛔收；回写记 true', '盲' not in 承 and 承.get('回写') is True))
        a = 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '承': {'补': True, '诸稿': [{'file': f('稿三'), 'words': 3}]}})
        R.append(('④并旧 _承.json：旧稿留、旧补去（所收有选⛔补·⑬）、重魂路承旧', len(a['承']['诸稿']) == 3 and '补' not in a['承'] and a['重'] == '中'
                  and '补' not in 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '承': {'补': True}}, 补=False)['承']))
        R.append(('⑤包裹调 造章.js 而带 args', '造章.js' in 包裹(a) and '"章": 9' in 包裹(a)))
        R.append(('⑤之二·旧 _承.json 带须厚者承之（X40）', 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '须厚': True, '承': {}}).get('须厚') is True and '须厚' not in 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '承': {}})))
        承2, _ = 收(9, [j1, j2, j3, j4], root=t, 再=True, 界=0)
        a2 = 造(9, 承2, 旧={'重': '中', '魂路': ['物证'], '承': {'回写': True}}, 再=True)
        R.append(('⑦再回写：盲读·2 作盲、回写⛔承（新旧俱去）', 承2.get('盲') == {'x': 1} and '回写' not in a2['承']))
        # 1023 坑㊻之审所逮
        j5 = os.path.join(t, 'j5.jsonl')
        写(j5, [{'type': 'started', 'key': 'p', 'label': '执笔·甲·物证'}, {'type': 'result', 'key': 'p', 'result': {'file': f('稿一'), 'words': 9}},
                {'type': 'started', 'key': 'q', 'label': '盲读'}, {'type': 'result', 'key': 'q', 'result': {'happened': '未交：被安全分类器截停'}}])
        os.utime(j5, (5, 5))
        承5, _ = 收(9, [j1, j2, j3, j4, j5], root=t, 界=0)
        R.append(('⑧盲读之壳（未交、被截）⛔收（承之即令造章停於盲读未交）', '盲' not in 承5))
        承6, 来6 = 收(9, [j1, j2, j3, j4, j5], root=t, 界=4.5)
        R.append(('⑨重造之界：界前之 journal（旧轮之选、草）⛔收', 来6 == [j5] and '选' not in 承6 and '草' not in 承6))
        盘 = f('稿五')
        open(盘, 'w', encoding='utf-8').write('第9章 甲\n' + '她' * 300 + '\n【本章亮点】一')
        半 = f('稿六')
        open(半, 'w', encoding='utf-8').write('她' * 400)
        承7, _ = 收(9, [], root=t, 界=0)
        R.append(('⑩盘稿：journal 无果而稿档在（≥200 字节、有亮点）→ 收、量净重；空档（稿三）、稿半（稿六·无亮点）⛔收',
                  [x['file'] for x in 承7.get('诸稿', [])] == [盘] and 承7['诸稿'][0]['words'] == 300))
        os.utime(盘, (3, 3))
        R.append(('⑩之二 盘稿在界前（旧轮）→ ⛔收', not 收(9, [], root=t, 界=4)[0].get('诸稿')))
        a3 = 造(9, 承, 旧={'重': '中', '魂路': ['物证']}, 裁='已亲治读误')
        R.append(('⑪--裁 入 args（造章.js 越致命未净而续记）；旧 _承.json 之裁承之', a3.get('裁') == '已亲治读误'
                  and 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '裁': '旧裁'}).get('裁') == '旧裁' and '裁' not in 造(9, 承, 旧={'重': '中', '魂路': ['物证']})))
        R.append(('⑬选已成 → ⛔补（补来之稿选不读，白耗一执笔）；选未成 → 补', '补' not in 造(9, {'选': {'ranking': []}}, 旧={'重': '中', '魂路': ['物证']})['承']
                  and 造(9, {}, 旧={'重': '中', '魂路': ['物证']})['承'].get('补') is True))
        旧稿 = f('稿七')
        open(旧稿, 'w').write('x')
        os.utime(旧稿, (3, 3))
        a8 = 造(9, {}, 旧={'重': '中', '魂路': ['物证'], '承': {'诸稿': [{'file': 旧稿}], '盲': {'happened': '未交'}}}, 界=4)
        R.append(('⑭造：界前之旧稿⛔承、旧 _承.json 之盲读之壳⛔承', not a8['承'].get('诸稿') and '盲' not in a8['承']))
        旧路 = os.path.join(t, '_承.json')
        open(旧路, 'w').write('{}')
        os.utime(旧路, (3, 3))
        旧9 = {'重': '中', '魂路': ['物证'], '裁': '旧裁', '承': {'选': {'common_fatal': '旧之共病'}, '诸稿': [{'file': f('稿一')}]}}
        a9 = 造(9, {}, 旧之滤(旧9, 旧路, 4), 界=4)
        R.append(('⑭之二 重造後之全路（旧之滤→造）：旧 _承.json 之共病之选、裁、稿俱⛔承，重魂路留；界前不滤', '选' not in a9['承']
                  and '裁' not in a9 and not a9['承'].get('诸稿') and a9['重'] == '中' and 旧之滤(旧9, 旧路, 2) is 旧9 and 旧之滤(旧9, 旧路, 0) is 旧9))
        坏 = os.path.join(t, 'r4', 'bad.jsonl')
        open(坏, 'wb').write(json.dumps({'type': 'started', 'key': 'k', 'label': '执笔·甲'}, ensure_ascii=False).encode('utf-8') + b'\n\xe5\x9b')
        try:
            收(9, [坏], root=t, 界=0)
            R.append(('⑮截於半字之 journal ⛔崩（一份坏即诸章之承俱死）', True))
        except Exception:
            R.append(('⑮截於半字之 journal ⛔崩（一份坏即诸章之承俱死）', False))
        # ★1024 通式（N≥411）：拆键
        j6 = os.path.join(t, 'j6.jsonl')
        盲全 = {'understood': True, 'confused': '全懂', 'misread': '无', 'want_next': True, 'why_next': '想', 'happened': '事', 'remember': '记', 'prior': '无'}
        写(j6, [{'type': 'started', 'key': 'a', 'label': '执笔·甲·物证'}, {'type': 'result', 'key': 'a', 'result': {'draft': {'file': f('稿一'), 'beats': 5, 'words': 9, 'soul': '魂'}, 'flaws': '无'}},
                {'type': 'started', 'key': 'b', 'label': '执笔·乙·查'}, {'type': 'result', 'key': 'b', 'result': {'flaws': '无稿'}},
                {'type': 'started', 'key': 'c', 'label': '选·行家兼两眼'}, {'type': 'result', 'key': 'c', 'result': {'pick': {'ranking': ['稿一']}, 'flaws': '缺必填'}},
                {'type': 'started', 'key': 'd', 'label': '选·补'}, {'type': 'result', 'key': 'd', 'result': {'pick': {'ranking': ['稿一'], 'why': '由', 'fatal': [], 'leap': [], 'common_fatal': '', 'beat_scores': '分'}}},
                {'type': 'started', 'key': 'e', 'label': '合稿'}, {'type': 'result', 'key': 'e', 'result': {}},
                {'type': 'started', 'key': 'g', 'label': '盲读'}, {'type': 'result', 'key': 'g', 'result': {'blind': 盲全}},
                {'type': 'started', 'key': 'h', 'label': '逻辑审·1'}, {'type': 'result', 'key': 'h', 'result': {'merge': {'file': 'x'}}},
                {'type': 'started', 'key': 'i', 'label': '逻辑审·1·补'}, {'type': 'result', 'key': 'i', 'result': {'audit': {'hard': [], 'soft': '', 'gate': '闸', 'misread': False}}}])
        os.makedirs(os.path.join(t, '版本', '第411章'))
        f11 = os.path.join(t, '版本', '第411章', '起草_稿一.md')
        open(f11, 'w').close()
        j6文 = open(j6, encoding='utf-8').read().replace(f('稿一'), f11)
        open(j6, 'w', encoding='utf-8').write(j6文)
        承8, 来8 = 收(411, [j6], root=t, 界=0)
        R.append(('⑯通式拆键：稿以 draft 认章、选缺必填⛔收而其补收、合交空⛔收、盲收、审错键⛔收而 逻辑审·1·补 收；只 flaws 之查⛔作稿',
                  来8 == [j6] and [x['file'] for x in 承8.get('诸稿', [])] == [f11] and 承8.get('选', {}).get('why') == '由'
                  and '草' not in 承8 and 承8.get('盲') == 盲全 and 承8.get('审', {}).get('gate') == '闸'))
        R.append(('⑯之二 N≤410 之果原样（拆⛔动旧章）；N≥411 只 flaws、交空、非对象俱作未交', 拆({'ranking': ['稿二']}, '选', False) == {'ranking': ['稿二']}
                  and 拆('ok', '回写', False) == 'ok' and 拆({}, '草', False) == {} and 收(9, [j1, j2], root=t, 界=0)[0].get('选') == {'ranking': ['稿二']}
                  and 拆({'flaws': '无'}, '选') is None and 拆({}, '草') is None and 拆('ok', '回写') is None
                  and 拆({'rewrite': {'done': True}}, '回写') == {'done': True}))
        # ★1024 --查：抄留前席之构思、量之入账；盘稿验之
        构 = os.path.join(t, '版本', '第9章', '起草_甲_构思.md')
        open(构, 'w', encoding='utf-8').write('# 执笔·甲之构思\n魂（物证路）：一物作证\n进化账所避：某\n## ① 一拍\n## 满分之问\n- 写法甲\n- 写法乙\n- 写法丙\n拍表：\n| 拍 | 其事 | 其物 | 最要之一句 |\n|---|---|---|---|\n| 一 | 事 | 物 | 句 |\n| 二 | 事 | 物 | 句 |\n③ 平处\n' + '想' * 80)
        稿查 = f('稿四')
        open(稿查, 'w', encoding='utf-8').write('第九章 试\n' + '她走过去，停了一下。' * 220 + '\n＊\n' + '他没说话。' * 10 + '\n【本章亮点】骨\n')
        档相 = '版本/第9章/起草_稿四.md'
        稿9, 由9, 条9 = 查(9, '甲', 档相, root=t, 界=0, 时='T')
        账9 = json.load(open(os.path.join(t, '版本', '第9章', '_补前稿账.json'), encoding='utf-8'))
        R.append(('⑰--查：前席构思抄留 _前（原档仍在·⛔mv）、量其魂拍表满分之问①—⑤ 入账', 条9.get('构思_前') == '起草_甲_构思_前.md'
                  and os.path.exists(构) and os.path.exists(os.path.join(t, '版本', '第9章', '起草_甲_构思_前.md'))
                  and 账9[-1]['量'] == {'字节': 账9[-1]['量']['字节'], '魂': True, '进化账所避': True, '满分之问': True, '写法数': 3, '拍表': True, '拍数': 2, '①—⑤': '①③'}))
        R.append(('⑰之二 盘稿过铁底、有亮点、硬项零 → 稿（file 照参、beats 以「＊」数、魂取构思）', bool(稿9) and 稿9['file'] == 档相 and 稿9['beats'] == 2
                  and 稿9['words'] >= 2000 and 稿9['soul'] == '一物作证' and 账9[-1]['稿'] == '收'))
        open(稿查, 'w', encoding='utf-8').write('第九章 试\n' + '她' * 300 + '\n')
        稿10, 由10, _ = 查(9, '甲', 档相, root=t, 界=0)
        open(稿查, 'w', encoding='utf-8').write('第九章 试\n' + '她' * 300 + '\n【本章亮点】骨\n')
        稿11, 由11, _ = 查(9, '甲', 档相, root=t, 界=0)
        账10 = json.load(open(os.path.join(t, '版本', '第9章', '_补前稿账.json'), encoding='utf-8'))
        R.append(('⑰之三 稿半（无亮点）、低於铁底 → 无稿；再查之前稿另名（_前2·⛔覆前账）', 稿10 is None and '稿半' in 由10 and 稿11 is None and '铁底' in 由11
                  and len(账10) == 3 and 账10[1]['构思_前'] == '起草_甲_构思_前2.md'))
        R.append(('⑰之四 无构思之席：前稿无、照验其稿', 查(9, '乙', 档相, root=t, 界=0)[2]['构思_前'] is None))
        # ★1024 怀疑者补：查席之稿 file 相对 → 依 root 补绝对，⛔与盘稿之 glob 重收；料重出後之旧稿⛔收
        f12 = os.path.join(t, '版本', '第411章', '起草_稿二.md')
        open(f12, 'w', encoding='utf-8').write('第四一一章 试\n' + '她走过去。' * 100 + '\n【本章亮点】骨\n')
        j7 = os.path.join(t, 'j7.jsonl')
        写(j7, [{'type': 'started', 'key': 'a', 'label': '执笔·乙·查'},
                {'type': 'result', 'key': 'a', 'result': {'draft': {'file': '版本/第411章/起草_稿二.md', 'beats': 2, 'words': 2200, 'soul': '魂'}, 'flaws': '无'}},
                {'type': 'started', 'key': 'b', 'label': '执笔·甲·物证'}, {'type': 'result', 'key': 'b', 'result': {'draft': {'file': f11, 'beats': 5, 'words': 9, 'soul': '魂'}}}])
        旧目 = os.getcwd()
        os.chdir(t)                              # 真跑之 cwd 即仓根：相对之路 exists 为真，旧式即重收
        try:
            承9 = 收(411, [j7], root=t, 界=0)[0]
        finally:
            os.chdir(旧目)
        R.append(('⑯之三 查席之稿（相对之路）补成绝对、一稿只收一回（⛔与盘稿重收）', sorted(x['file'] for x in 承9.get('诸稿', [])) == sorted([f11, f12])))
        open(稿查, 'w', encoding='utf-8').write('第九章 试\n' + '她走过去，停了一下。' * 220 + '\n＊\n' + '他没说话。' * 10 + '\n【本章亮点】骨\n')
        料9 = os.path.join(t, '版本', '第9章', '_料.md')
        open(料9, 'w').write('料')
        os.utime(稿查, (100, 100))
        稿12, 由12, _ = 查(9, '甲', 档相, root=t, 界=0)
        os.remove(料9)
        R.append(('⑰之五 稿档早於 _料.md（料已重出·前轮之稿）→ 无稿', 稿12 is None and '早於' in 由12 and bool(查(9, '甲', 档相, root=t, 界=0)[0])))
        档 = os.path.join(t, '承_重造.json')
        记重造(9, 档=档, 时=123.0)
        R.append(('⑫记重造／重造之时 往返；他章 0', 重造之时(9, 档) == 123.0 and 重造之时(8, 档) == 0))
        try:
            造(9, 承)
            R.append(('⑥无 重／魂路 即停', False))
        except SystemExit:
            R.append(('⑥无 重／魂路 即停', True))
    for k, ok in R:
        print('  %s %s' % ('✓' if ok else '✗', k))
    ok = sum(1 for _, o in R if o)
    print('── 负测·承 %d/%d %s ──' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    return all(o for _, o in R)


def main():
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if not a or not a[0].isdigit():
        print(__doc__)
        sys.exit(2)
    n = int(a[0])
    取 = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    if '--查' in a:
        i = a.index('--查')
        名, 档 = (a[i + 1:i + 3] + ['', ''])[:2]
        if 名 not in '甲乙丙丁戊己庚' or len(名) != 1 or not re.fullmatch(r'版本/第%d章/起草_稿[一二三四五六七]\.md' % n, 档):
            print('无稿：--查 之参不合（须 执笔之名一字 与 版本/第%d章/起草_稿X.md）' % n)
            sys.exit(2)
        稿, 由, 条 = 查(n, 名, 档)
        print('查·第%d章·执笔·%s：前席构思 %s%s' % (n, 名, 条.get('构思_前') or '无（或不足 %d 字节）' % 盘稿之下限,
              ('｜量 ' + json.dumps(条['量'], ensure_ascii=False)) if 条.get('量') else ''))
        print('  入账：版本/第%d章/_补前稿账.json' % n)
        print('稿：' + json.dumps(稿, ensure_ascii=False) if 稿 else '无稿：' + 由)
        return
    再 = '--再回写' in a
    承, 来 = 收(n, glob.glob(诸journal之式), 再=再)
    if 再 and not (承.get('审') or {}).get('misread') and not (承.get('审') or {}).get('hard'):
        print('  ⚠ --再回写：所收之审无读误亦无硬崩——再回写无的，照常续（去 --再回写）即可')
    章目 = os.path.join(ROOT, '版本', '第%d章' % n)
    旧路 = os.path.join(章目, '_承.json')
    旧 = json.load(open(旧路, encoding='utf-8')) if os.path.exists(旧路) else None
    界 = 重造之时(n)
    旧 = 旧之滤(旧, 旧路, 界)
    魂路 = 取('--魂路').split(',') if 取('--魂路') else None
    args = 造(n, 承, 旧, 取('--重'), 魂路, 再=再, 裁=取('--裁'), 补='--不补' not in a, 界=界)
    print('承·第%d章：journal %d 份；诸稿 %d（%s）；%s' % (
        n, len(来), len(args['承'].get('诸稿', [])),
        '、'.join('%s·%s字' % (os.path.basename(x['file']), x.get('words')) for x in args['承'].get('诸稿', [])),
        '、'.join(k for k in ('选', '草', '盲', '审', '回写') if k in args['承']) or '其後诸段俱未成'))
    if len(args['承'].get('诸稿', [])) < 3:
        print('  ⚠ 诸稿不足三——包裹已带「补」，造章.js 补派缺席之执笔' if args['承'].get('补') else '  ⛔诸稿不足三而无补——造章.js 必停')
    if (args['承'].get('选') or {}).get('common_fatal'):
        print('  ⛔所承之选有共病（%s）——承之即复停於共病；治料後以 args 重造:true 新派' % str(args['承']['选']['common_fatal'])[:60])
    if '--印' in a:
        return
    with open(旧路, 'w', encoding='utf-8') as o:
        json.dump(args, o, ensure_ascii=False, indent=1)
    with open(os.path.join(章目, '_承.js'), 'w', encoding='utf-8') as o:
        o.write(包裹(args))
    print('  ✓ 写 %s 与 _承.js\n  ── 续之令 ──\n  Workflow({scriptPath:\'%s\'})' % (旧路, os.path.join(章目, '_承.js')))


if __name__ == '__main__':
    main()
