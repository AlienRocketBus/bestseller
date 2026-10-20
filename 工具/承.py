#!/usr/bin/env python3
"""承.py——容器重启後，从诸 workflow 之 journal 收第 N 章已成之段，造 造章.js 之 args.承（版本/第N章/_承.json）与包裹（_承.js）。

为何立（1017·397 逮）：容器重启频（397 一章两回：执笔之半、选之半），每回主环手翻 journal、手认 label、
手拼 args.承——393、397、397 三回皆手办，易错（稿与执笔之对、丙稿成而未交者之补）。今一器办毕：
  python3 工具/承.py 397            # 扫诸 journal，收 397 之已成段，写 _承.json 与 _承.js，印续之令
  python3 工具/承.py 397 --印       # 只印所收，⛔写
  python3 工具/承.py 397 --再回写   # 「致命未净」（回写一回後复验仍读误／硬崩）：以 盲读·2、逻辑审·2 之果作 盲、审，⛔承回写——再走一回 回写→盲读→审→记席
  python3 工具/承.py --自测

所收（label → 承之键）：执笔·*→诸稿（以 file 认，後者覆前者）；选·行家兼两眼／选·补→选；合稿／合稿·补→草；
盲读／盲读·补→盲；逻辑审·1→审；回写→回写（true）。盲读·2、逻辑审·2、记席⛔收（造章.js 之承不认之，照跑）。
稿档已不在者⛔收（稿被覆或挪走）。args 之 章／重／魂路 取旧 _承.json，无则须 --重 与 --魂路。
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
       (re.compile(r'^盲读(·补)?$'), '盲'), (re.compile(r'^逻辑审·1$'), '审'), (re.compile(r'^回写$'), '回写')]


def 读(路):
    行 = []
    try:
        with open(路, encoding='utf-8') as f:
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
            with open(os.path.join(os.path.dirname(路), 'agent-%s.jsonl' % i), encoding='utf-8') as f:
                if 记 in f.readline():
                    return True
        except OSError:
            continue
    return False


def 收(n, 诸路, root=ROOT, 再=False):
    """诸 journal 依 mtime 升序扫；属第 n 章之 run（有执笔之果其 file 在 版本/第n章/）方收；後者覆前者。"""
    章目 = os.path.join(root, '版本', '第%d章' % n) + os.sep
    承 = {}
    稿 = {}
    来 = []
    键们 = 键表 + ([(re.compile(r'^盲读·2$'), '盲'), (re.compile(r'^逻辑审·2$'), '审')] if 再 else [])
    for 路 in sorted(诸路, key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0):
        行 = 读(路)
        标 = {d.get('key'): d.get('label', '') for d in 行 if d.get('type') == 'started'}
        果 = [(标.get(d.get('key'), ''), d.get('result')) for d in 行 if d.get('type') == 'result']
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
                elif isinstance(r, dict):
                    承[k] = r
    if 稿:
        承['诸稿'] = list(稿.values())
    if 再:
        承.pop('回写', None)   # 再回写：回写⛔承——造章.js 见 审 有病即再派回写，以 审（逻辑审·2）之读误与硬崩为令
    return 承, 来


def 须厚判(n):
    try:
        import 造式验
        return 造式验.须厚之判(n)[0]
    except Exception:
        return None


def 造(n, 承, 旧=None, 重=None, 魂路=None, 再=False):
    旧 = 旧 or {}
    a = {'章': n, '重': 重 or 旧.get('重'), '魂路': 魂路 or 旧.get('魂路')}
    # ★1020 X40 驳席逮：重启续跑之 args 须带 须厚（旧 _承.json 有则承之；无则照 造式验.须厚之判 现算——与自走之派令同尺）；⛔丢则执笔令、选令之须厚条随之消失
    if 旧.get('须厚') or (n >= 401 and 须厚判(n) is True):
        a['须厚'] = True
    if not a['重'] or not a['魂路']:
        raise SystemExit('⛔承：无旧 _承.json 可取 重／魂路——须 --重 中 --魂路 物证,回声,不说（照 自走.py 之派令）')
    旧承 = 旧.get('承') or {}
    合 = dict(旧承)
    合.pop('补', None)
    if 承.get('诸稿') or 旧承.get('诸稿'):
        by = {x['file']: x for x in (旧承.get('诸稿') or []) if os.path.exists(x.get('file', ''))}
        by.update({x['file']: x for x in 承.get('诸稿', [])})
        合['诸稿'] = list(by.values())
    for k in ('选', '草', '盲', '审', '回写'):
        if k in 承:
            合[k] = 承[k]
    if 再:
        合.pop('回写', None)
    a['承'] = 合
    return a


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
        承, 来 = 收(9, [j1, j2, j3, j4], root=t)
        R.append(('①只收属本章之 run（他章之 j3 ⛔收，其选⛔覆）；承之 run 以令首认章（j4 之合稿收）',
                  来 == [j1, j2, j4] and 承.get('选') == {'ranking': ['稿二']} and 承.get('草') == {'file': '正文'}))
        R.append(('②诸稿以 file 认、稿档不在者⛔收', sorted(x['file'] for x in 承['诸稿']) == [f('稿一'), f('稿二')]))
        R.append(('③盲读·2 ⛔收；回写记 true', '盲' not in 承 and 承.get('回写') is True))
        a = 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '承': {'补': True, '诸稿': [{'file': f('稿三'), 'words': 3}]}})
        R.append(('④并旧 _承.json：旧稿留、补去、重魂路承旧', len(a['承']['诸稿']) == 3 and '补' not in a['承'] and a['重'] == '中'))
        R.append(('⑤包裹调 造章.js 而带 args', '造章.js' in 包裹(a) and '"章": 9' in 包裹(a)))
        R.append(('⑤之二·旧 _承.json 带须厚者承之（X40）', 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '须厚': True, '承': {}}).get('须厚') is True and '须厚' not in 造(9, 承, 旧={'重': '中', '魂路': ['物证'], '承': {}})))
        承2, _ = 收(9, [j1, j2, j3, j4], root=t, 再=True)
        a2 = 造(9, 承2, 旧={'重': '中', '魂路': ['物证'], '承': {'回写': True}}, 再=True)
        R.append(('⑦再回写：盲读·2 作盲、回写⛔承（新旧俱去）', 承2.get('盲') == {'x': 1} and '回写' not in a2['承']))
        try:
            造(9, 承)
            R.append(('⑥无 重／魂路 即停', False))
        except SystemExit:
            R.append(('⑥无 重／魂路 即停', True))
    for k, ok in R:
        print('  %s %s' % ('✓' if ok else '✗', k))
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
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
    再 = '--再回写' in a
    承, 来 = 收(n, glob.glob(诸journal之式), 再=再)
    if 再 and not (承.get('审') or {}).get('misread') and not (承.get('审') or {}).get('hard'):
        print('  ⚠ --再回写：所收之审无读误亦无硬崩——再回写无的，照常续（去 --再回写）即可')
    章目 = os.path.join(ROOT, '版本', '第%d章' % n)
    旧路 = os.path.join(章目, '_承.json')
    旧 = json.load(open(旧路, encoding='utf-8')) if os.path.exists(旧路) else None
    魂路 = 取('--魂路').split(',') if 取('--魂路') else None
    args = 造(n, 承, 旧, 取('--重'), 魂路, 再=再)
    print('承·第%d章：journal %d 份；诸稿 %d（%s）；%s' % (
        n, len(来), len(args['承'].get('诸稿', [])),
        '、'.join('%s·%s字' % (os.path.basename(x['file']), x.get('words')) for x in args['承'].get('诸稿', [])),
        '、'.join(k for k in ('选', '草', '盲', '审', '回写') if k in args['承']) or '其後诸段俱未成'))
    if len(args['承'].get('诸稿', [])) < 3:
        print('  ⛔诸稿不足三——造章.js 必停；缺者可加「"补": true」於 _承.json 之承（补派缺席之执笔）')
    if '--印' in a:
        return
    with open(旧路, 'w', encoding='utf-8') as o:
        json.dump(args, o, ensure_ascii=False, indent=1)
    with open(os.path.join(章目, '_承.js'), 'w', encoding='utf-8') as o:
        o.write(包裹(args))
    print('  ✓ 写 %s 与 _承.js\n  ── 续之令 ──\n  Workflow({scriptPath:\'%s\'})' % (旧路, os.path.join(章目, '_承.js')))


if __name__ == '__main__':
    main()
