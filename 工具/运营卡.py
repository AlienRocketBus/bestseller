#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""运营卡（W908 环5·1119 作者令「GitHub 之运营……跑到绝对的100分」「拖累了这个目标，那就不要去使用」）——
GitHub 四流（autopush、gate、巡、演练）每流×八维之分，零 token 机算；每扣带 类、据、治。尺即 设定/方案/W908.md「满分之尺」。

【读】①Actions（GITHUB_TOKEN；增量：卡记已取之跑，键 (run_id, attempt)⛔以 ref——坑62；只取新毕者之 jobs；每算 ≤20 回请求；
       沙盒无令亦试公仓之读，读不得即只读报与静析）；環之毕跑取其志末「環毕：N 巡（rc：…）」之行。
     ②备份/报 之 报/推、报/演 之史：推报.诸报之史（git log＋一批 cat-file·报每 ref 覆写，旧果取其旧版·⛔另立 jsonl）；
       本跑之报（--出 目下·尚未 --落）经 推报.目之报；旧卡经 推报._读报——报之读俱在 推报（坑53·⛔另造报之读写）。
     ③哨 PR 之言（唤之史）。④静：.github/workflows/*.yml（借 推报._yaml 之子集·⛔另写析器；探唯其码——推报._去注 去其注，
       注中之字⛔充其实）、钉之律（推报.钉式之缺·唯一处，本器只加 Node24 之版）与诸器之源之探（接棒守、封版、全测、法用之守）。
【算】每流×八维照尺逐类扣（下限 0）；扣之键＝流·维·类——首见即记，治即销而移「史」，销後复见标「复发」（运营之进化账）。
【写】报/卡.json（机读：算於、流、扣、史、迹之存）、报/卡.md（人读·近十卡之分趋）；--摘 印 summary。
     写者唯一：autopush 报步（推报 --写 之後、--落 之前），随本跑之报同一 --落 入 备份/报——写者册「报」族之写者不增；巡、演练⛔写卡。
【限】卡只读只算：⛔拦推、⛔入器红账、⛔开 Issue（裁三）；算败或逾时（autopush.yml timeout 60 与 || 守之）报照落、卡留旧。
用法：
  python3 工具/运营卡.py --算 --出 目 [--摘]      # GitHub autopush 报步：写 目/报/卡.json、目/报/卡.md；--摘 印 summary 之 md
  python3 工具/运营卡.py --读                      # 沙盒：印云端卡之一行（最低之流、新扣；卡旧 24 时 ⚠）
  python3 工具/运营卡.py --取样 [--至 a,x,y]       # 取今之迹为回放之样（工具/_负测料/运营卡/样.json·总编辑手跑）
  python3 工具/运营卡.py --自测                    # 以样回放：须得方案「今之分」或书其差之由；变异二；进化账；写之形
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, ast, json, math, time, calendar, statistics, subprocess, tempfile, shutil
import urllib.request, urllib.parse, urllib.error
import 推报                                       # 报之读写、YAML 子集、钉律、去注俱借之（坑53·⛔另造）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
主枝, 报枝, 坏果 = 推报.主枝, 推报.报枝, 推报.坏果
卡径, 卡md径 = '报/卡.json', '报/卡.md'
样档 = os.path.join(ROOT, '工具', '_负测料', '运营卡', '样.json')
诸流 = ('autopush', 'gate', '巡', '演练')
有跑之流 = ('autopush', '巡', '演练')            # gate 係 workflow_call：其跑即 autopush、演练 之 gate / * 之 job
流档 = {'autopush': 'autopush.yml', 'gate': 'gate.yml', '巡': '巡.yml', '演练': '演练.yml'}
尺 = (('稳', 25), ('准', 20), ('服', 15), ('观', 10), ('愈', 10), ('安', 10), ('速', 5), ('进', 5))
权 = dict(尺)
窗数 = 100                                       # 窗：末号−100 至末号（「近百跑」）
非意之因 = ('merge', 'fetch', 'bundle', '片数', 'push', 'non-ff', '逾时')   # 尺·稳：报因∈此、或败而无报
沙盒之runtime = {'python': '3.13', 'node': '22'}   # 方案 W908 环4 之试：python3 --version → 3.13.18、node --version → v22.23.4
Node24之始 = {'actions/checkout': 5, 'actions/setup-python': 6, 'actions/setup-node': 5,       # 各家 action.yml 之 runs.using 始为 node24 之大版
            'actions/upload-artifact': 6, 'actions/download-artifact': 7}                   # （1119 git ls-remote 并取其 action.yml 验之）
误告之语 = ('请换号',)                            # 公仓 Actions 不计分：「额度用光·请换号」係误告作者（W908 环2(b)）
请求之顶 = 20
请求之时顶 = 30                                   # 秒：Actions 之取逾此即止（余者下回）——卡之算守 autopush 报步 timeout 60 之内
新跑之顶 = 12                                     # 每算至多取新毕之跑之 jobs 数（余者下回）
步挂之倍, 步挂之底 = 10, 300                      # 步挂：逾同步之中位十倍且逾五分（免秒级之步偶慢误计）——底係本器所加、尺无之：
                                                 #   逾十倍而 <5 分者略之、⛔掩——其数与逾一分者列於卡之「限」（如 #116 片 download-artifact 3 分），
                                                 #   计否由总编辑裁（降底为 60 即 gate −1）
静之档 = ('.github/workflows/autopush.yml', '.github/workflows/gate.yml', '.github/workflows/巡.yml', '.github/workflows/演练.yml',
         '工具/接棒守.py', '工具/封版.py', '工具/全测.py', '工具/法用之守.py', '.gitattributes', '设定/方法账.md', '工具/运营卡.py')
治之表 = {
    '非意之败·merge': '治6 账并（gate.yml 备候 git merge 前 --装·总编辑并）', '被顶未吸': '环2(b) 云巡再闸即补', '步挂': '环4 checkout 步限 4 分（省取降级全取）',
    '封前⊉GitHub': '环9 封前之闸与 GitHub 同表', '果因误记': '环4 autopush 已在之支 YIN=', '跑绿果红': '环4 演练「期」：果≠期方 exit 1',
    '取消落红报': '环4 演练 report if: !cancelled()', '对照无期': '环4 演练入参「期」（治17）', 'runtime异': '裁六：唯演练对拍逐项同方切（3.13／22）',
    '入主迟': '治6 账并＋环2(b)', '手治': '治6 账并＋环2(b)(c)', '活守空唤': '环2(a) 态变方唤', '假⛔': '环6 报之读去对照、果＝期即消',
    '无summary': '环4 推报 --摘 入 summary', '环末方现': '環之跑六时一步，summary 唯步末现——留（環之制）', '红行无注': '环4 ::error 注实因',
    '信不书因': '环4 --信 带因', '无run-name': '环4 演练 run-name', '注非实因': '环4 ::error 取印之首⛔行', '片红而跑绿': '环4 片之器红 ::warning 而 rc 0',
    '败不书细因': '环4 冲突之档出 output', '去重rc0': '环4 summary 汇非止之巡', '题误': '环2(e) rc4 之题', '频因无自治': '治6 账并',
    '一类无自治': '环2(b)／环4', '误降级': '环4 真冲突⛔降级', '自愈实死': '环2(d) 同局首唤之时', 'tag或Node20': '环4 钉 40 位 sha 之 Node24 原生之版',
    '冗权': '环4 permissions 移 job 级', '平台之规未裁': '环11（书裁於 设定/方法账.md「环11…裁」即销）', '关键路': '环4 advance 省取（可缓）',
    '定候过长': '环2(b) API 判被顶', '无计无读者': '计：环5 运营卡（autopush 报步调之）；读者：环6 法用之守.报之读 添卡之一行（运营卡.一行）',
    '再起漏判': '环4 再起之察去 status 之滤', '误告': '环2(b) 删额度之断',
    '派必败': '环2(c) 再闸辨 merge', '红之色迟': '環之制（環末方红）——留；::error 当巡即注', '卡·算败': '查 autopush 报步之「卡·算败」',
}


def _秒(s):
    if isinstance(s, (int, float)):
        return int(s)
    try:
        return calendar.timegm(time.strptime(str(s)[:19], '%Y-%m-%dT%H:%M:%S'))
    except Exception:
        return None


def _iso(t):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))


def _git(a, root=ROOT, 入=None, 限=60):
    """⛔承外之 GIT_DIR 诸变（钩中、演中）——库只由 root 定。→ CompletedProcess（bytes）。"""
    e = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR',
                                                           'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES')}
    return subprocess.run(['git', '-c', 'core.quotepath=off'] + a, cwd=root, input=入, capture_output=True, timeout=限, env=e)


# ═══ 一、祖之问（记其答：取样存之，回放唯读所记·⛔动 git） ═══
class 祖器:
    def __init__(s, root=None, 记=None):
        s.root = root
        s.祖记 = dict((记 or {}).get('祖') or {})
        s.亲记 = dict((记 or {}).get('亲') or {})
        s.缺 = set()

    def 祖(s, a, b):
        """a 为 b 之祖（或即 b）否；物不在（git 128）或回放无记 → False 而记「缺」（⛔猜）。记之键取 sha 之首十二。"""
        if not (a and b):
            return False
        k = '%s..%s' % (a[:12], b[:12])
        if k not in s.祖记:
            if s.root is None:
                s.缺.add(k)
                return False
            r = _git(['merge-base', '--is-ancestor', a, b], s.root)
            if r.returncode not in (0, 1):
                s.缺.add(k)
                return False
            s.祖记[k] = int(r.returncode == 0)
        return bool(s.祖记[k])

    def 亲(s, h):
        k = (h or '')[:12]
        if k not in s.亲记:
            if s.root is None:
                s.缺.add('亲:' + k)
                return []
            r = _git(['rev-list', '--parents', '-n1', h], s.root)
            if r.returncode != 0:
                s.缺.add('亲:' + k)
                return []
            s.亲记[k] = [x[:12] for x in r.stdout.decode().split()[1:]]
        return s.亲记[k]

    def 记(s):
        return {'祖': s.祖记, '亲': s.亲记}


# ═══ 二、读 ═══
def _跑(x):
    """Actions 之跑 → 卡之形（时俱作秒）。"""
    return {'id': x['id'], 'n': x['run_number'], '试': x.get('run_attempt') or 1, '事': x.get('event'), '态': x.get('status'),
            '果': x.get('conclusion'), '枝': x.get('head_branch') or '', '头': x.get('head_sha') or '', '题': (x.get('display_title') or '')[:20],
            '起': _秒(x.get('created_at')), '始': _秒(x.get('run_started_at')), '毕': _秒(x.get('updated_at')),
            '者': (x.get('triggering_actor') or x.get('actor') or {}).get('login', '')}


def _步名(n):
    return re.sub(r'@\S+', '@', str(n or ''))


def _job(j):
    步 = []
    for s in j.get('steps') or []:
        a, b = _秒(s.get('started_at')), _秒(s.get('completed_at'))
        步.append([_步名(s.get('name')), s.get('conclusion'), (b - a) if (a is not None and b is not None) else None])
    return [j.get('name') or '', j.get('conclusion'), _秒(j.get('started_at')), _秒(j.get('completed_at')), 步, j.get('id')]


def _版(d, 路, 笔时):
    m = re.search(r'/runs/(\d+)', str(d.get('run_url') or ''))
    return {'路': 路, '类': 路.split('/')[1], '笔时': 笔时, 'ref': d.get('ref') or d.get('名') or '', 'sha': d.get('sha') or '',
            '果': d.get('果'), '因': d.get('因') or '', '时': _秒(d.get('时')), '主': d.get('main_after') or '',
            '跑': m.group(1) if m else '', '期': d.get('期'), '冲突': list(d.get('冲突') or [])[:8]}


def 读报史(root=ROOT, 引='refs/remotes/origin/' + 报枝, 至=None):
    """备份/报 之史 → 报/推、报/演 之诸版（每笔所改之档取其当笔之版·笔之时升序）；读不出即 []（⛔抛）。
    经 推报.诸报之史（一回 git log＋一批 cat-file：百余版一取；推报.诸报(引=笔) 一笔一读则百余回）——⛔另造报之读。"""
    return [_版(d, d['路'], d['笔时']) for d in 推报.诸报之史(root, 引, 至=至)]


def 读本报(出目, 今):
    """本跑之报（--出 目下 报/推、报/演 之 json·尚未 --落）→ [版]。经 推报.目之报（--摘、--注 同源）。"""
    return [_版(d, d['路'], 今) for d in 推报.目之报(出目 or '')]


def 读文(root=ROOT, 笔=None):
    """静析之源：笔给出即取其树（git show·史一字不移），否则读盘。→ {路: 文|None}"""
    文 = {}
    for p in 静之档:
        if 笔:
            r = _git(['show', '%s:%s' % (笔, p)], root)
            文[p] = r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None
        else:
            f = os.path.join(root, p)
            文[p] = open(f, encoding='utf-8', errors='replace').read() if os.path.exists(f) else None
    return 文


class _不随(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def _请(径, 计, 令=None, 文本=False):
    """GitHub REST（零 token：GITHUB_TOKEN 或公仓之读）；计[0] 为本算之请求数（≤ 请求之顶）。志之取：先取其 302 之址、去令而取（令⛔随至存储之址）。"""
    if 计[0] >= 请求之顶:
        raise RuntimeError('请求逾顶 %d' % 请求之顶)
    if len(计) > 1 and time.time() - 计[1] > 请求之时顶:
        raise RuntimeError('请求逾顶（%d 秒）' % 请求之时顶)
    计[0] += 1
    api = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
    头 = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'yunying-ka'}
    if 令:
        头['Authorization'] = 'Bearer ' + 令
    req = urllib.request.Request(api + 径, headers=头)
    if not 文本:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode('utf-8') or 'null')
    try:
        with urllib.request.build_opener(_不随).open(req, timeout=10) as r:
            return r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        址 = e.headers.get('Location') if e.code in (301, 302, 303, 307) else None
        if not 址:
            raise
        with urllib.request.urlopen(urllib.request.Request(址, headers={'User-Agent': 'yunying-ka'}), timeout=15) as r:
            return r.read().decode('utf-8', 'replace')


def 取迹(旧迹, 令, 仓, 计, 至=None, 新顶=新跑之顶, 页顶=1):
    """Actions 之迹（增量）：三流之跑列（各一请）、新毕之跑之 jobs（键 id:attempt，至多 新顶）、新毕之環之「環毕」、哨 PR 之言。
    → (迹, 限)；一请败即留旧迹之同项、记其限（⛔抛）。"""
    迹 = {'跑': dict((旧迹 or {}).get('跑') or {}), 'job': dict((旧迹 or {}).get('job') or {}), '環毕': dict((旧迹 or {}).get('環毕') or {}),
         '唤': list((旧迹 or {}).get('唤') or [])}
    限 = []
    for 流 in 有跑之流:
        try:
            新 = []
            for 页 in range(1, 页顶 + 1):          # 取样（至）须窗之全：翻页至窗首（常算一页·旧迹存其余）
                d = _请('/repos/%s/actions/workflows/%s/runs?per_page=100&page=%d' % (仓, urllib.parse.quote(流档[流]), 页), 计, 令)
                新 += [_跑(x) for x in d.get('workflow_runs') or []]
                if len(d.get('workflow_runs') or []) < 100 or not 至 or min(r['n'] for r in 新) <= (至.get(流) or 0) - 窗数 - 10:
                    break
            if 至 and 至.get(流):
                新 = [r for r in 新 if r['n'] <= 至[流]]
            旧 = {r['id']: r for r in 迹['跑'].get(流) or []}
            旧.update({r['id']: r for r in 新})
            迹['跑'][流] = sorted(旧.values(), key=lambda r: r['n'])
        except Exception as e:
            限.append('Actions 之跑列（%s）读不得：%s——用旧迹' % (流, str(e)[:80]))
    缺 = []
    for 流 in 有跑之流:
        rs = 迹['跑'].get(流) or []
        末 = max([r['n'] for r in rs] or [0])
        for r in rs:
            if r['态'] == 'completed' and r['n'] >= 末 - 窗数 and '%s:%s' % (r['id'], r['试']) not in 迹['job']:
                缺.append(r)
    缺.sort(key=lambda r: -(r['毕'] or 0))
    for r in 缺[:新顶]:
        try:
            d = _请('/repos/%s/actions/runs/%s/attempts/%s/jobs?per_page=100' % (仓, r['id'], r['试']), 计, 令)
            迹['job']['%s:%s' % (r['id'], r['试'])] = [_job(j) for j in d.get('jobs') or []]
        except Exception as e:
            限.append('jobs（#%s）读不得：%s' % (r['n'], str(e)[:60]))
            break                                  # 一败即止（逾顶、断网）：余者下回
    if len(缺) > 新顶:
        限.append('迹未全：%d 跑之 jobs 待後算取（每算至多 %d）' % (len(缺) - 新顶, 新顶))
    for r in 迹['跑'].get('巡') or []:
        k = '%s:%s' % (r['id'], r['试'])
        if r['态'] == 'completed' and r['果'] in ('success', 'failure') and r['题'].startswith('巡环') and str(r['id']) not in 迹['環毕'] and k in 迹['job']:
            hid = next((j[5] for j in 迹['job'][k] if j[0] == 'huan' and len(j) > 5), None)
            if not hid:
                continue
            try:
                文 = _请('/repos/%s/actions/jobs/%s/logs' % (仓, hid), 计, 令, 文本=True)
                行 = [re.sub(r'^\S+Z ', '', l) for l in 文.split('\n') if '環毕：' in l and 'echo' not in l]
                迹['環毕'][str(r['id'])] = 行[-1][:400] if 行 else ''
            except Exception as e:
                限.append('環毕（#%s）读不得：%s' % (r['n'], str(e)[:60]))
                if '逾顶' in str(e):
                    break
                迹['環毕'][str(r['id'])] = ''          # 志已失（blob 404）：记空、⛔每算再请
    try:
        prs = _请('/repos/%s/pulls?state=open&per_page=10&head=%s' % (仓, urllib.parse.quote('%s:备份/巡警' % 仓.split('/')[0])), 计, 令)
        if prs:
            言 = _请('/repos/%s/issues/%d/comments?per_page=100' % (仓, prs[0]['number']), 计, 令) or []
            迹['唤'] = [{'id': c['id'], '时': _秒(c.get('created_at')), '键': ((re.findall(r'<!--(.*?)-->', c.get('body') or '') or [''])[-1]).strip()[:80],
                        '体': (c.get('body') or '')[:600]} for c in 言 if (c.get('user') or {}).get('login') == 'github-actions[bot]']
    except Exception as e:
        限.append('哨 PR 之言读不得：%s' % str(e)[:60])
    return 迹, 限


def _剪迹(迹):
    """存於卡之迹：唯窗内（并其前十号之余）之跑与其 jobs——卡⛔无限而长。"""
    出 = {'跑': {}, 'job': {}, '環毕': dict(迹.get('環毕') or {}), '唤': list(迹.get('唤') or [])[-30:]}
    for 流, rs in (迹.get('跑') or {}).items():
        末 = max([r['n'] for r in rs] or [0])
        出['跑'][流] = [r for r in rs if r['n'] >= 末 - 窗数 - 10]
    留 = {'%s:%s' % (r['id'], r['试']) for rs in 出['跑'].values() for r in rs}
    出['job'] = {k: v for k, v in (迹.get('job') or {}).items() if k in 留}
    出['環毕'] = {k: v for k, v in 出['環毕'].items() if any(str(r['id']) == k for r in 出['跑'].get('巡') or [])}
    return 出


# ═══ 三、静之探 ═══
def _yaml(t):
    try:
        return 推报._yaml(t or '') or {}
    except Exception:
        return {}


def _码(t):
    """yml 之码（逐行去注·行号不移）：注中之字⛔充其实（如 autopush.yml 头注之「::error」）——去注借 推报._去注（引号内之 # 不去）。"""
    return '\n'.join(推报._去注(l) for l in (t or '').split('\n'))


def _行(t, 式):
    m = re.search(式, t or '', re.M)
    return (t[:m.start()].count('\n') + 1) if m else 0


def 钉之缺(t):
    """安·钉：钉之律（40 位 sha 而注其版）唯 推报.钉式之缺 一处（推闸 ⑲ 同之）；本器只加「版为 Node24 原生」→ [缺]（行序；空即合）。"""
    坏 = 推报.钉式之缺(t)
    缺 = [(i, ':%d %s（%s）' % (i, u, 由)) for i, u, 由 in 坏]
    坏行 = {i for i, _, _ in 坏}
    for i, u, 注 in 推报.诸uses(t):
        名 = u.partition('@')[0]
        m = re.match(r'v(\d+)', 注)
        if i not in 坏行 and m and 名 in Node24之始 and int(m.group(1)) < Node24之始[名]:
            缺.append((i, ':%d %s %s（Node20 之版）' % (i, 名, 注)))
    return [x for _, x in sorted(缺)]


def _字面(t, 名):
    m = re.search(r'(?ms)^%s = (\{.*?\n\}|\(.*?\)|\[.*?\])' % re.escape(名), t or '')
    if not m:
        return None
    try:
        return ast.literal_eval(m.group(1))
    except Exception:
        return None


def 封前之缺(文):
    """封前之闸 ⊇ GitHub 读者可见之非负测、非活态之格（外声闸恒 exit 0·免）否 → (缺, 据)；不可考 → (None, 由)。"""
    封, 全 = 文.get('工具/封版.py'), 文.get('工具/全测.py')
    读 = _字面(全, '读者可见之闸')
    if not (封 and 读):
        return None, '封版／全测之表读不出'
    活 = set(_字面(全, '活态之格') or ())
    要 = {x for x in 读 if not str(x).startswith('负测·')} - 活 - {'外声闸'}
    m = re.search(r'(?m)^读者之慢 = (.+)$', 封)
    if not m:
        return None, '封版.py 无「读者之慢」'
    try:
        封前 = set(ast.literal_eval(m.group(1).split('#')[0].strip()))
    except Exception:
        return (set(), '读者之慢 由 全测.读者可见之闸 算（同表）') if '读者可见之闸' in m.group(1) else (None, '读者之慢 非字面')
    return 要 - 封前, '封版.py:%d 读者之慢 %d 格；全测.读者可见之闸 之非负测非活态 %d 格' % (_行(封, r'^读者之慢 = '), len(封前), len(要))


def _函体(t, 名):
    m = re.search(r'(?ms)^def %s\(.*?(?=^def |\Z)' % re.escape(名), t or '')
    return m.group(0) if m else ''


def _读卡否(源):
    """一函之码读卡否（ast·函之文档与注⛔算）：调 运营卡.一行（或 from 运营卡 import 一行）、或码中之串含「报/卡.json」。析不出 → False（⛔猜）。"""
    try:
        f = ast.parse(源).body[0]
    except Exception:
        return False
    if not isinstance(f, ast.FunctionDef):
        return False
    体 = f.body[1:] if f.body and isinstance(f.body[0], ast.Expr) and isinstance(getattr(f.body[0], 'value', None), ast.Constant) else f.body
    for n in ast.walk(ast.Module(body=体, type_ignores=[])):
        if isinstance(n, ast.Attribute) and n.attr == '一行' and isinstance(n.value, ast.Name) and n.value.id == '运营卡':
            return True
        if isinstance(n, ast.ImportFrom) and n.module == '运营卡' and any(a.name == '一行' for a in n.names):
            return True
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and '报/卡.json' in n.value:
            return True
    return False


# ═══ 四、算 ═══
def _p90(xs):
    xs = sorted(xs)
    return xs[max(0, math.ceil(0.9 * len(xs)) - 1)] if xs else None


def _分秒(s):
    s = int(s or 0)
    return ('%d 时 %d 分' % (s // 3600, s % 3600 // 60)) if s >= 3600 else ('%d 分 %d 秒' % (s // 60, s % 60) if s >= 60 else '%d 秒' % s)


def 算(迹, 文, 算於, 祖, 报史=(), 窗=窗数, 旧卡=None, 本跑=''):
    """纯算（⛔读写盘、⛔请求；祖之问经 祖器）→ 卡（dict）。"""
    扣们 = []

    def 扣(流, 维, 类, 分, 据, 次=1):
        扣们.append({'键': '%s·%s·%s' % (流, 维, 类), '流': 流, '维': 维, '类': 类, '分': round(分, 1), '次': 次,
                    '据': [str(x) for x in 据][:12], '治': 治之表.get(类.split('·')[0] if 类.split('·')[0] in 治之表 else 类, 治之表.get(类, ''))})
    限 = []
    跑 = {}
    for 流 in 有跑之流:
        rs = [r for r in (迹.get('跑') or {}).get(流) or [] if r.get('态') == 'completed' and (r.get('毕') or 0) <= 算於]
        跑[流] = sorted(rs, key=lambda r: r['n'])
    末号 = {流: max([r['n'] for r in 跑[流]] or [0]) for 流 in 有跑之流}
    窗跑 = {流: [r for r in 跑[流] if r['n'] >= 末号[流] - 窗] for 流 in 有跑之流}
    jobs = 迹.get('job') or {}
    jk = lambda r: '%s:%s' % (r['id'], r['试'])
    无job = [r for 流 in 有跑之流 for r in 窗跑[流] if jk(r) not in jobs]
    if 无job:
        限.append('窗内 %d 跑无 jobs 之迹（步挂、片红之判略之）' % len(无job))
    版们 = sorted([v for v in 报史 if (v.get('笔时') or 0) <= 算於], key=lambda v: (v['笔时'], v['路']))
    跑之报 = {}
    for v in 版们:
        if v['跑']:
            跑之报.setdefault(v['跑'], []).append(v)
    号 = lambda r: '#%d %s' % (r['n'], r['id'])
    原 = {流: 文.get('.github/workflows/' + 流档[流]) or '' for 流 in 诸流}
    y = {流: _码(原[流]) for 流 in 诸流}             # 静之探唯其码（逐行去注·行号不移）：注中之字⛔充其实
    Y = {流: _yaml(原[流]) for 流 in 诸流}
    接 = (文.get('工具/接棒守.py') or '').split('\ndef 自测(')[0]       # 探唯其码（自测之断言或含所探之语·⛔计）

    # ── 稳 ──
    因计 = {}
    for 流 in ('autopush', '演练'):
        for r in 窗跑[流]:
            if r['果'] != 'failure':
                continue
            vs = 跑之报.get(str(r['id']))
            因 = None if vs else '无报'
            if vs and vs[-1]['果'] == '败' and vs[-1]['因'] in 非意之因:
                因 = vs[-1]['因']
            if 因:
                因计.setdefault((流, 因), []).append(号(r))
    for 流 in ('巡',):
        for r in 窗跑[流]:
            if r['果'] == 'failure' and any(s[0].startswith('续') and s[1] == 'failure' for j in jobs.get(jk(r)) or [] for s in j[4]):
                因计.setdefault((流, '续'), []).append(号(r))
    for (流, 因), 据 in sorted(因计.items()):
        扣(流, '稳', '非意之败·' + 因, 2 * len(据), 据, len(据))
    # 手并（服·手治与稳·被顶共用）：治-* 之推其头为并之提交，某章之头为其一亲之祖而非另一亲之祖（并章入主之手并）——一章一计
    章头 = {}
    for r in 跑['autopush']:
        if r['枝'].startswith('章-') and r['枝'] not in 章头:
            章头[r['枝']] = r['头']
    未成之章 = {b: h for b, h in 章头.items() if any(x['枝'] == b and x['果'] in ('failure', 'cancelled') for x in 跑['autopush'])}
    手并 = {}
    for r in 窗跑['autopush']:
        if not (r['枝'].startswith('治-') and r['事'] == 'push'):
            continue
        ps = 祖.亲(r['头'])
        if len(ps) < 2:
            continue
        for b, h in sorted(未成之章.items()):
            if b in 手并:
                continue
            ins = [祖.祖(h, p) for p in ps]
            if any(ins) and not all(ins):
                手并[b] = r
    手并之头 = {r['头'] for r in 手并.values()}
    成跑 = [r for r in 跑['autopush'] if r['果'] == 'success']
    未吸 = []
    for r in 窗跑['autopush']:
        if r['果'] != 'cancelled':
            continue
        吸 = next((x for x in 成跑 if x['起'] > r['起'] and 祖.祖(r['头'], x['头'])), None)
        if 吸 is None:
            if 算於 - (r['毕'] or 算於) >= 1800:
                未吸.append('%s（%s·其後无含之成跑）' % (号(r), r['枝']))
        elif 吸['头'] in 手并之头:
            未吸.append('%s（%s·至 #%d 手并方入）' % (号(r), r['枝'], 吸['n']))
    if 未吸:
        扣('autopush', '稳', '被顶未吸', 2 * len(未吸), 未吸, len(未吸))
    步 = {}
    for 流 in ('autopush', '演练', '巡'):
        for r in 窗跑[流]:
            for j in jobs.get(jk(r)) or []:
                名 = j[0]
                属 = 'gate' if 名.startswith('gate / ') else 流
                jn = re.sub(r'^gate / ', '', 名)
                jn = '片' if jn.startswith('片 ') else jn
                for s in j[4]:
                    if s[2] is not None:
                        步.setdefault((属, jn, s[0]), []).append((s[2], r))
    挂, 略 = {}, []
    for (属, jn, sn), xs in 步.items():
        中 = statistics.median([x for x, _ in xs])
        for x, r in xs:
            if x > 步挂之倍 * max(中, 1):
                语 = '%s %s「%s」%s（中位 %s）' % (号(r), jn, sn, _分秒(x), _分秒(中))
                if x >= 步挂之底:
                    挂.setdefault(属, []).append((语, jn, sn))
                else:
                    略.append((x, '%s·%s' % (属, 语)))
    for 属, xs in sorted(挂.items()):
        扣(属, '稳', '步挂', len(xs), [x[0] for x in xs], len(xs))
    if 略:                                          # 底係本器所加（尺唯「逾常值十倍」）：所略者列其数、逾一分者列其据——⛔掩，计否总编辑裁
        略.sort(key=lambda z: -z[0])
        分 = [z[1] for z in 略 if z[0] >= 60]
        限.append('步挂之底 %d 秒（尺无之·本器所加）：逾十倍而 <5 分者略之 %d%s' % (
            步挂之底, len(略), ('；其逾一分者 %d：%s' % (len(分), '；'.join(分[:4]))) if 分 else ''))
    环跑 = [r for r in 跑['巡'] if r['题'].startswith('巡环') and r['枝'] == 主枝]
    叠 = []
    for x in [r for r in 窗跑['巡'] if r in 环跑]:
        y0 = next((w for w in 环跑 if w is not x and w['始'] and w['毕'] and w['始'] + 60 < x['起'] < w['毕'] - 120), None)
        if y0:
            察 = [w for w in 跑['巡'] if not w['题'].startswith('巡环') and 0 <= x['起'] - w['起'] <= 180]
            叠.append('%s 起於 #%d 之環在跑时%s' % (号(x), y0['n'], ('（派者 %s）' % 号(察[-1])) if 察 else ''))
    if 叠:
        扣('巡', '稳', '再起漏判', len(叠), 叠, len(叠))

    # ── 准 ──
    if any(w in 接 for w in 误告之语):
        据 = ['工具/接棒守.py:%d' % _行(接, '|'.join(map(re.escape, 误告之语)))]
        据 += ['唤 %s' % c['id'] for c in 迹.get('唤') or [] if c.get('时', 0) <= 算於 and ('额度用光' in c.get('体', '') or '换号' in c.get('体', ''))]
        扣('巡', '准', '误告', 5, 据)
    缺, 由 = 封前之缺(文)
    if 缺 is None:
        限.append('封前⊉GitHub 不可考：' + 由)
    elif 缺:
        扣('autopush', '准', '封前⊉GitHub', 3, [由, '缺 %d：%s' % (len(缺), '、'.join(sorted(缺)[:8]))])
    for 流 in ('autopush', '演练'):
        误记, 绿红, 消红 = [], [], []
        for r in 窗跑[流]:
            vs = 跑之报.get(str(r['id'])) or []
            for v in vs:
                if v['果'] in ('成', '已在', '过') and v['因']:
                    误记.append('%s %s 果「%s」因「%s」' % (号(r), v['路'], v['果'], v['因']))
            末 = vs[-1] if vs else None
            if 末 and r['果'] == 'success' and 末['果'] in 坏果 and not (末.get('期') and 末['果'] == 末['期']):
                绿红.append('%s %s 果「%s」' % (号(r), 末['路'], 末['果']))
            if 末 and r['果'] == 'cancelled' and 末['果'] in 坏果:
                消红.append('%s %s 果「%s」' % (号(r), 末['路'], 末['果']))
        if 误记:
            扣(流, '准', '果因误记', 2, 误记, len(误记))
        if 绿红:
            扣(流, '准', '跑绿果红', 2, 绿红, len(绿红))
        if 消红:
            扣(流, '准', '取消落红报', 2, 消红, len(消红))
    if y['演练'] and '--期' not in y['演练']:
        红演 = sorted({v['路'] for v in 版们 if v['类'] == '演' and v['果'] == '红' and not v.get('期')})
        扣('演练', '准', '对照无期', 2, ['演练.yml 无「期」之入'] + 红演[:4])
    派败 = []
    for r in 窗跑['autopush']:
        if r['事'] != 'workflow_dispatch' or r['者'] != 'github-actions[bot]':
            continue
        vs = 跑之报.get(str(r['id'])) or []
        if not vs or vs[-1]['因'] != 'merge':
            continue
        前 = [v for v in 版们 if v['路'] == vs[-1]['路'] and v['笔时'] < vs[-1]['笔时']]
        if 前 and 前[-1]['因'] == '重派':
            continue                    # autopush 自重派（tries）⛔计
        派败.append('%s %s 再闸之派而败·merge' % (号(r), r['枝']))
    if 派败:
        扣('巡', '准', '派必败', 2, 派败, len(派败))
    g = Y['gate']
    版 = {}
    for j in (g.get('jobs') or {}).values():
        for s in j.get('steps') or []:
            u = str(s.get('uses') or '')
            w = s.get('with') or {}
            if u.startswith('actions/setup-python'):
                版['python'] = str(w.get('python-version') or '')
            if u.startswith('actions/setup-node'):
                版['node'] = str(w.get('node-version') or '')
    异 = ['%s %s（沙盒 %s）' % (k, v, 沙盒之runtime[k]) for k, v in sorted(版.items()) if v != 沙盒之runtime[k]]
    if 异:
        扣('gate', '准', 'runtime异', 2, ['gate.yml:%d' % _行(y['gate'], r'python-version')] + 异)
    迟 = []
    for r in 窗跑['巡']:
        if r['果'] != 'failure' or not r['题'].startswith('巡环'):
            continue
        m = re.search(r'rc：([\d ]+)）', 迹.get('環毕', {}).get(str(r['id'])) or '')
        jm = re.search(r'隔(\d+)秒', r['题'])
        if m and jm:
            rc = m.group(1).split()
            if '1' in rc and rc.index('1') < len(rc) - 1:
                迟.append('%s 第 %d 巡 rc 1 而跑红迟 %s（環末方红）' % (号(r), rc.index('1') + 1, _分秒((len(rc) - 1 - rc.index('1')) * int(jm.group(1)))))
    if 迟:
        扣('巡', '准', '红之色迟', 1, 迟, len(迟))

    # ── 服 ──
    推版 = sorted([v for v in 版们 if v['类'] == '推' and v['主'] and v['时']], key=lambda v: v['时'])
    迟们 = []
    for b in sorted(章头):
        首 = min((r for r in 跑['autopush'] if r['枝'] == b), key=lambda r: r['n'])
        if 首['n'] < 末号['autopush'] - 窗:
            continue
        t0, h = 首['起'], 章头[b]
        候 = [v for v in 推版 if v['时'] >= t0]
        lo, hi = 0, len(候)
        while lo < hi:
            mid = (lo + hi) // 2
            if 祖.祖(h, 候[mid]['主']):
                hi = mid
            else:
                lo = mid + 1
        if lo < len(候):
            迟们.append((候[lo]['时'] - t0, b, 候[lo]['ref']))
        elif 算於 - t0 > 600:
            迟们.append((算於 - t0, b, '未入'))
    p = _p90([x for x, _, _ in 迟们])
    if p is not None and p > 600:
        分 = 1 if p <= 1800 else (3 if p <= 3600 else 5)
        扣('autopush', '服', '入主迟', 分, ['章推至入主 p90 %s（%d 章）' % (_分秒(p), len(迟们))]
          + ['%s %s（%s）' % (b, _分秒(x), w) for x, b, w in sorted(迟们, reverse=True)[:4]])
    手派 = [号(r) for r in 窗跑['autopush'] if r['事'] == 'workflow_dispatch' and r['者'] and r['者'] != 'github-actions[bot]']
    if 手派 or 手并:
        扣('autopush', '服', '手治', min(5, 0.5 * (len(手派) + len(手并))),
          ['手派 %d：%s' % (len(手派), ' '.join(x.split()[0] for x in 手派))]
          + ['手并 %d：%s' % (len(手并), ' '.join('%s←#%d %s' % (b, r['n'], r['头'][:9]) for b, r in sorted(手并.items())))], len(手派) + len(手并))
    if re.search(r"键 = '活守·' \+ time\.strftime\('%Y-%m-%d'", 接):
        扣('巡', '服', '活守空唤', 3, ['工具/接棒守.py:%d 活守之键带日：钩死不复则每日一空唤' % _行(接, r"键 = '活守·' \+ time\.strftime")])
    法 = _函体(文.get('工具/法用之守.py'), '报之读')
    今演 = {}
    for v in 版们:
        if v['类'] == '演':
            今演[v['路']] = v
    红演 = [v for v in 今演.values() if v['果'] == '红' and not (v.get('期') and v['果'] == v['期'])]
    if 法 and '期' not in 法 and 红演:
        扣('演练', '服', '假⛔', 3, ['工具/法用之守.py 报之读 不辨对照与「期」'] + [v['路'] for v in 红演[:4]])

    # ── 观 ──
    for 流 in ('autopush', '巡', '演练'):
        t, w = y[流], Y[流]
        if not t:
            continue
        if 'GITHUB_STEP_SUMMARY' not in t:
            扣(流, '观', '无summary', 2, ['%s 无 GITHUB_STEP_SUMMARY' % 流档[流]])
        else:
            诸 = [(s, j) for j in (w.get('jobs') or {}).values() for s in j.get('steps') or [] if 'GITHUB_STEP_SUMMARY' in _码(str(s.get('run') or ''))]
            if 诸 and all(int(str(s.get('timeout-minutes') or j.get('timeout-minutes') or 360)) >= 60 for s, j in 诸):
                扣(流, '观', '环末方现', 2, ['%s:%d summary 唯写於长步（步末方现）' % (流档[流], _行(t, r'GITHUB_STEP_SUMMARY'))])
        败 = [号(r) for r in 窗跑[流] if r['果'] == 'failure']
        if 败 and '::error' not in t and '推报.py --注' not in t:      # 码中之 ::error 或 推报 --注 之调（同 推报 ⑳）；注中之字⛔算
            扣(流, '观', '红行无注', 1, ['%s 之码无 ::error、无 推报 --注；红跑 %d：%s' % (流档[流], len(败), ' '.join(x.split()[0] for x in 败[:6]))])
        信 = re.findall(r'--信 "([^"]*)"', t)
        if 信 and not any('YIN' in x for x in 信):
            扣(流, '观', '信不书因', 1, ['%s:%d --信 只书果' % (流档[流], _行(t, r'--信 "'))])
        if 'run-name' not in w and 窗跑[流]:
            无名 = [r for r in 窗跑[流] if r['题'] == 流]
            if len(无名) * 2 >= len(窗跑[流]):
                扣(流, '观', '无run-name', 1, ['%s 无 run-name：窗内 %d／%d 跑之题即流名' % (流档[流], len(无名), len(窗跑[流]))])
        for i, l in enumerate(t.split('\n'), 1):
            m = re.search(r'::error[^:]*::([^"]*)', l)
            if m and '$' not in m.group(1) and m.group(1).count('／') >= 3:
                扣(流, '观', '注非实因', 2, ['%s:%d ::error 列诸可能之因（%s）' % (流档[流], i, m.group(1)[:40])])
                break
    红绿 = []
    for 流 in ('autopush', '演练'):
        for r in 窗跑[流]:
            if r['果'] == 'success' and any(j[0].startswith('gate / 片') and j[1] == 'failure' for j in jobs.get(jk(r)) or []):
                红绿.append(号(r))
    if 红绿:
        扣('gate', '观', '片红而跑绿', 2, ['片之 job 红（器红）而跑绿 %d 跑' % len(红绿)] + 红绿[-4:], len(红绿))
    if 'git merge' in y['gate'] and '--diff-filter=U' not in y['gate']:
        扣('gate', '观', '败不书细因', 2, ['gate.yml:%d 并败而⛔出冲突之档' % _行(y['gate'], r'git merge --no-edit')])
    if y['巡'] and '非止' not in y['巡']:
        扣('巡', '观', '去重rc0', 1, ['巡.yml summary 唯 rc（去重之巡 rc 0 而态非止）'])
    if 'rc == 4' in 接 and '卡之题(' not in 接:
        据 = ['工具/接棒守.py:%d rc4 之题用停书之龄' % _行(接, r"'停书 %s 分'")]
        据 += ['唤 %s「%s」' % (c['id'], c['体'].split('\n')[0][:16]) for c in 迹.get('唤') or [] if c.get('时', 0) <= 算於 and str(c.get('键', '')).startswith('巡警:rc4')]
        扣('巡', '观', '题误', 1, 据)

    # ── 愈 ──
    自治 = {
        'merge': bool(文.get('.gitattributes') and 'merge=' in 文['.gitattributes'] and '账并' in y['gate']),
        'fetch': 'sheng_cang; then quan_qu' in y['gate'], 'bundle': 'sheng_cang; then quan_qu' in y['gate'],
        '片数': 'sheng_cang; then quan_qu' in y['gate'], 'non-ff': '/actions/workflows/autopush.yml/dispatches' in y['autopush'],
        '被顶': "'cancelled'" in 接, '续': 'until curl' in y['巡'],
    }
    类计 = {}
    for (流, 因), 据 in 因计.items():
        类计[(流, 因)] = 据
    if 未吸:
        类计[('autopush', '被顶')] = 未吸
    for (流, 因), 据 in sorted(类计.items()):
        if 自治.get(因):
            continue
        if len(据) >= 5:
            扣(流, '愈', '频因无自治·' + 因, 3, ['%s %d 回而无自治' % (因, len(据))])
        else:
            扣(流, '愈', '一类无自治·' + 因, 2, ['%s %d 回而无自治' % (因, len(据))])
    for 属, xs in sorted(挂.items()):
        if 属 != 'gate':
            continue
        无限 = set()
        for _, jn, sn in xs:
            for k, j in (g.get('jobs') or {}).items():
                if not (k == jn or (jn == '片' and (j.get('strategy') or {}).get('matrix'))):
                    continue
                for s in j.get('steps') or []:
                    u = str(s.get('uses') or '')
                    if (u and sn.startswith('Run ' + u.split('@')[0])) or s.get('name') == sn:
                        if not s.get('timeout-minutes'):
                            无限.add('%s「%s」' % (jn, sn))
        if 无限:
            扣('gate', '愈', '一类无自治·步挂', 2, ['步挂之步无步限：' + '、'.join(sorted(无限))])
    l = next((x for x in y['gate'].split('\n') if 'sheng_cang; then quan_qu' in x and '败' in x), '')
    if l and 'merge' not in l and 'CHONG' not in l:
        扣('gate', '愈', '误降级', 1, ['gate.yml:%d 真冲突亦降级全取' % _行(y['gate'], re.escape(l.strip()))])
    隔, 候 = re.search(r'(?m)^唤之隔分 = (\d+)', 接), re.search(r'(?m)^应之候分 = (\d+)', 接)
    if 隔 and 候 and int(隔.group(1)) < int(候.group(1)) and 'max(真)' in _函体(接, '应判'):
        扣('巡', '愈', '自愈实死', 4, ['工具/接棒守.py:%d 唤隔 %s ＜ 应候 %s 而应判取末唤（max）' % (_行(接, r'^def 应判'), 隔.group(1), 候.group(1))])

    # ── 安 ──
    for 流 in 诸流:
        缺钉 = 钉之缺(原[流])                        # 版之注即行末之注：取原文
        if 缺钉:
            扣(流, '安', 'tag或Node20', 2, 缺钉[:6], len(缺钉))
    # 〔1120〕旧「冗权」之扣（巡之 pull-requests: write 冗）係误判：PR 之 issue 评论须 pull-requests 之写——备份/巡演 --试（run 44655946521）只读即 403，故去其扣
    # 裁之行须其式「环11·環之占机·裁：留｜事驱…」（旧探「环11…裁」连「未裁」亦销·自欺）
    if re.search(r'timeout-minutes: (3\d\d)', y['巡']) and not re.search(r'环11·[環环]之占机·裁：\s*(留|改?事驱)', 文.get('设定/方法账.md') or ''):
        扣('巡', '安', '平台之规未裁', 2, ['巡.yml:%d 環之 24/7 占机未裁（设定/方法账.md 无「环11·環之占机·裁：留｜事驱…」）' % _行(y['巡'], r'timeout-minutes: 3\d\d')])

    # ── 速 ──
    for 流 in ('autopush', '演练'):
        for k, j in (Y[流].get('jobs') or {}).items():
            for s in j.get('steps') or []:
                w = s.get('with') or {}
                if str(s.get('uses') or '').startswith('actions/checkout') and str(w.get('fetch-depth')) == '0' and not w.get('filter'):
                    扣(流, '速', '关键路', 1, ['%s:%d %s 之 checkout 全取（史与档俱取）' % (流档[流], _行(y[流], r'fetch-depth: 0'), k)])
                    break
            else:
                continue
            break
    m = re.search(r'(?m)^合入之界分 = (\d+)', 接)
    if m and int(m.group(1)) > 5:
        扣('巡', '速', '定候过长', 2, ['工具/接棒守.py:%d 合入之界 %s 分定候（卡之觉之标 ≤5 分）' % (_行(接, r'^合入之界分 = '), m.group(1))])

    # ── 进 ──
    # 进·有史无计无读者：计＝运营卡在而 autopush 之码调其 --算；读者＝法用之守.报之读（自走之首、会话首）之码读卡——
    #   卡在而无读者照扣（坑6「可达≠用」：旧探只问 运营卡.py 在否，读者未接而先销）
    计 = bool(文.get('工具/运营卡.py')) and '运营卡.py --算' in y['autopush']
    读者 = _读卡否(_函体(文.get('工具/法用之守.py'), '报之读'))
    if not (计 and 读者):
        缺 = '无运营卡' if not 计 else '运营卡在而 法用之守.报之读 未读卡（运营卡.一行／报/卡.json）'
        扣('autopush', '进', '无计无读者', 2, ['败因之史在 备份/报 之 git log 而%s：%s' % ('无计无读者' if not 计 else '有计无读者', 缺)])
        扣('巡', '进', '无计无读者', 2, ['巡印 force 无史、rc 之布%s：%s' % ('无账' if not 计 else '有账无读者', 缺)])
    if 旧卡 and 旧卡.get('本跑') and 本跑:
        # 卡·算败（运营之机·降级）：旧卡之後，报照落（果 成／红：其报步之树即候、含主枝之卡器）而卡未新之跑——
        #   已在、拒、备候之败之报步之树係本枝之笔（或先於卡器）⛔计
        卡跑 = set(旧卡.get('卡跑') or []) | {str(旧卡.get('本跑'))}
        漏 = [号(r) for r in 窗跑['autopush'] if (r['始'] or 0) > _秒(旧卡.get('算於') or 0) and str(r['id']) not in 卡跑
              and (跑之报.get(str(r['id'])) or [{}])[-1].get('果') in ('成', '红')]
        if 漏:
            扣('autopush', '稳', '卡·算败', len(漏), ['报照落而卡未新：' + ' '.join(漏[:6])], len(漏))

    # ── 分 ──
    流分 = {}
    for 流 in 诸流:
        维 = {}
        for k, w in 尺:
            维[k] = max(0, round(w - sum(x['分'] for x in 扣们 if x['流'] == 流 and x['维'] == k), 1))
            if float(维[k]).is_integer():
                维[k] = int(维[k])
        流分[流] = {'分': round(sum(维.values()), 1) if not all(isinstance(v, int) for v in 维.values()) else sum(维.values()), '维': 维}
    # 进化之账：首见即记；治即销（移史）；同键销後复见即「复发」
    旧扣 = {x['键']: x for x in (旧卡 or {}).get('扣') or []}
    旧史 = {x['键']: x for x in (旧卡 or {}).get('史') or []}
    for x in 扣们:
        o = 旧扣.get(x['键'])
        x['首见'] = (o or {}).get('首见') or _iso(算於)
        x['末见'] = _iso(算於)
        if x['键'] in 旧史 and not o:
            x['复发'] = True
            x['首见'] = _iso(算於)
        elif o and o.get('复发'):
            x['复发'] = True
    史 = [dict(o, 销=_iso(算於)) for k, o in 旧扣.items() if k not in {x['键'] for x in 扣们}]
    史 += [o for k, o in 旧史.items() if k not in {x['键'] for x in 扣们} and k not in {h['键'] for h in 史}]
    复 = sorted({x['键'] for x in 扣们 if x.get('复发')})
    同类 = sorted({x['类'] for x in 扣们 if len({y_['流'] for y_ in 扣们 if y_['类'] == x['类']}) >= 2})
    卡 = {'说明': '运营卡（W908 环5·工具/运营卡.py）：四流×八维（尺：设定/方案/W908.md「满分之尺」）；扣即运营之进化账（治即销入史、复见即复发）',
         '算於': _iso(算於), '窗': {流: [min([r['n'] for r in 窗跑[流]] or [0]), 末号[流]] for 流 in 有跑之流},
         '末跑': {流: (窗跑[流][-1]['id'] if 窗跑[流] else None) for 流 in 有跑之流}, '本跑': str(本跑 or ''),
         '卡跑': ([str(本跑)] if 本跑 else []) + [x for x in ((旧卡 or {}).get('卡跑') or [])][:40],
         '流': 流分, '扣': sorted(扣们, key=lambda x: (诸流.index(x['流']), [k for k, _ in 尺].index(x['维']), -x['分'])),
         '史': 史[-60:], '复发': 复, '同类及二流': 同类, '限': sorted(set(限)) + (['祖之问不可考 %d' % len(祖.缺)] if 祖.缺 else [])}
    return 卡


# ═══ 五、写 ═══
def _表(卡, 旧卡=None):
    L = ['| 流 | ' + ' | '.join(k for k, _ in 尺) + ' | 分 | 增减 |', '|---|' + '---|' * (len(尺) + 2)]
    for 流 in 诸流:
        f = (卡.get('流') or {}).get(流) or {}
        o = ((旧卡 or {}).get('流') or {}).get(流) or {}
        增 = (f.get('分', 0) - o['分']) if o.get('分') is not None else None
        L.append('| %s | %s | **%s** | %s |' % (流, ' | '.join(str((f.get('维') or {}).get(k, '—')) for k, _ in 尺), f.get('分', '—'),
                                              ('%+g' % 增) if 增 else '—'))
    return L


def 摘(卡, 旧卡=None):
    """→ summary 之 md（卡之表、本跑之增减、新扣、扣之要每流至多三）。"""
    L = ['### 运营卡（算於 %s·窗 %s）' % (卡['算於'][5:16].replace('T', ' '), '、'.join('%s #%s—#%s' % (k, v[0], v[1]) for k, v in 卡['窗'].items())), '']
    L += _表(卡, 旧卡)
    旧键 = {x['键'] for x in (旧卡 or {}).get('扣') or []}
    新 = [x for x in 卡['扣'] if 旧卡 and x['键'] not in 旧键]
    销 = [x for x in (旧卡 or {}).get('扣') or [] if x['键'] not in {y['键'] for y in 卡['扣']}]
    if 新 or 销:
        L += ['', '本跑之增减：' + '；'.join(['新扣 %s −%g' % (x['键'], x['分']) for x in 新] + ['销 %s +%g' % (x['键'], x['分']) for x in 销])]
    if 卡.get('复发') or 卡.get('同类及二流'):
        L += ['', '⚠ 运营之扣复发（%s）或同类及二流（%s）——总编辑立坑於 设定/方法坑账.json' % ('、'.join(卡.get('复发') or []) or '无',
                                                                        '、'.join(卡.get('同类及二流') or []) or '无')]
    L += ['', '扣之要（每流至多三）：']
    for 流 in 诸流:
        xs = sorted([x for x in 卡['扣'] if x['流'] == 流], key=lambda x: -x['分'])[:3]
        if xs:
            L.append('- **%s**：' % 流 + '；'.join('%s·%s −%g（%s）' % (x['维'], x['类'], x['分'], x['据'][0][:60] if x['据'] else '') for x in xs))
    if 卡.get('限'):
        L += ['', '限：' + '；'.join(卡['限'][:4])]
    return '\n'.join(L) + '\n'


def 成md(卡, 趋=()):
    L = ['# 运营卡', '', '> 工具/运营卡.py 机算（W908 环5）：GitHub 四流×八维；尺见 设定/方案/W908.md「满分之尺」。算於 %s。' % 卡['算於'], '']
    L += _表(卡)
    if 趋:
        L += ['', '## 近十卡之分趋', '', '| 算於 | ' + ' | '.join(诸流) + ' |', '|---|' + '---|' * len(诸流)]
        for t, d in 趋:
            L.append('| %s | %s |' % (t[5:16].replace('T', ' '), ' | '.join(str(((d.get(流) or {}).get('分', '—'))) for 流 in 诸流)))
    L += ['', '## 扣（类·分·据·治）', '']
    for x in 卡['扣']:
        L.append('- %s·%s·%s −%g%s：%s（治：%s）' % (x['流'], x['维'], x['类'], x['分'], '·复发' if x.get('复发') else '',
                                              '；'.join(x['据'][:4]), x.get('治') or '—'))
    if 卡.get('史'):
        L += ['', '## 史（已销）', ''] + ['- %s −%g（首见 %s、销 %s）' % (x['键'], x['分'], str(x.get('首见', ''))[5:16], str(x.get('销', ''))[5:16])
                                       for x in 卡['史'][-20:]]
    if 卡.get('限'):
        L += ['', '## 限', ''] + ['- ' + x for x in 卡['限']]
    return '\n'.join(L) + '\n'


def 写卡(卡, 出目, 迹=None, 趋=()):
    os.makedirs(os.path.join(出目, '报'), exist_ok=True)
    d = dict(卡)
    if 迹 is not None:                                # 迹之存（增量之据）：窗内之跑与 jobs，步名入表（卡⛔肥）
        d['迹'] = _剪迹(迹)
        d['迹']['job'], d['迹']['名表'] = _压(d['迹']['job'])
    # 先写於 出目 之旁、後 os.replace（同盘·原子）：逾时被杀⛔留半截之卡入 --落
    旁 = os.path.dirname(os.path.abspath(出目))
    for 径, 文 in ((卡径, json.dumps(d, ensure_ascii=False, separators=(',', ':'))), (卡md径, 成md(卡, 趋))):
        t = os.path.join(旁, '.卡_%d_%s' % (os.getpid(), os.path.basename(径)))
        open(t, 'w', encoding='utf-8').write(文)
        os.replace(t, os.path.join(出目, 径))
    return os.path.join(出目, 卡径)


def _读旧卡(root):
    """云端之卡（备份/报 之 报/卡.json）→ dict｜None。经 推报._读报（⛔另造报之读）。"""
    return 推报._读报(卡径, root, 取=False)


def _趋(root, 引='refs/remotes/origin/' + 报枝, 顶=9):
    """近 顶 卡之 (算於, 流)（新者先）。经 推报.诸报之史（⛔另造报之读）。"""
    return [(d.get('算於', ''), d.get('流') or {}) for d in reversed(推报.诸报之史(root, 引, 路们=(卡径,), 顶=顶))]


def 算口(出目, 印摘=False, root=ROOT):
    """GitHub autopush 报步：取 备份/报（旧卡、报史）、取主枝（祖之问）、Actions 之迹（增量）→ 算 → 写 出目/报/卡.json、卡.md。→ rc"""
    今 = int(time.time())
    for b in (报枝, 主枝):
        _git(['fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/origin/%s' % (b, b)], root, 限=40)
    旧卡 = _读旧卡(root)
    旧迹 = 样之迹(旧卡['迹']) if isinstance((旧卡 or {}).get('迹'), dict) and (旧卡['迹'].get('跑') is not None) else None
    if not 旧迹 and os.path.exists(样档):             # 首算：以样之迹为种（窗内之 jobs 免百回之请）
        try:
            样 = json.load(open(样档, encoding='utf-8'))
            旧迹 = 样之迹(样)
        except Exception:
            旧迹 = None
    令 = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN') or ''
    仓 = os.environ.get('GITHUB_REPOSITORY') or ''
    限 = []
    计 = [0, time.time()]
    if 仓:
        迹, 限 = 取迹(旧迹, 令, 仓, 计)
    else:
        迹, 限 = (旧迹 or {'跑': {}, 'job': {}}), ['无 GITHUB_REPOSITORY——Actions 之迹不取（只读报与静析）']
    报史 = 读报史(root) + 读本报(出目, 今)
    祖 = 祖器(root)
    卡 = 算(迹, 读文(root), 今, 祖, 报史, 旧卡=旧卡, 本跑=os.environ.get('GITHUB_RUN_ID', ''))
    卡['限'] = sorted(set(卡['限'] + 限)) + ['请求 %d 回' % 计[0]]
    写卡(卡, 出目, 迹, 趋=_趋(root))
    if 印摘:
        print(摘(卡, 旧卡))
    return 0


def 一行(root=ROOT, 取=True, 今=None):
    """沙盒（法用之守 --报读 之接口）：云端卡之一行——最低之流分、新扣数；卡旧 24 时 ⚠；复发或同类及二流 ⚠。无卡 → ''。"""
    卡 = 推报._读报(卡径, root, 取=取)
    if not 卡:
        return ''
    今 = 今 or int(time.time())
    流 = 卡.get('流') or {}
    低 = min(流.items(), key=lambda kv: kv[1].get('分', 100)) if 流 else ('—', {})
    t = _秒(卡.get('算於'))
    旧 = t is None or 今 - t > 24 * 3600
    新 = [x for x in 卡.get('扣') or [] if x.get('首见') == 卡.get('算於')]
    复 = bool(卡.get('复发') or 卡.get('同类及二流'))
    return '%s 运营卡（算於 %s）：最低 %s %s；新扣 %d%s%s' % (
        '⚠' if 旧 or 复 else '·', str(卡.get('算於', ''))[5:16].replace('T', ' '), 低[0], 低[1].get('分', '—'), len(新),
        ('（%s）' % '、'.join(x['键'] for x in 新[:2])) if 新 else '', '；卡旧逾 24 时' if 旧 else ('；⚠ 运营之扣复发' if 复 else ''))


def _压(job):
    """样之 jobs：步名入表、以号代之（样⛔肥）。→ (压之 jobs, 名表)"""
    表, 号 = [], {}
    def n(x):
        if x not in 号:
            号[x] = len(表)
            表.append(x)
        return 号[x]
    return {k: [[n(j[0]), j[1], j[2], j[3], [[n(s[0]), s[1], s[2]] for s in j[4]]] + j[5:] for j in v] for k, v in job.items()}, 表


def _解(job, 表):
    if not 表:
        return job
    return {k: [[表[j[0]], j[1], j[2], j[3], [[表[s[0]], s[1], s[2]] for s in j[4]]] + j[5:] for j in v] for k, v in job.items()}


def 样之迹(样):
    """样或卡之迹之存 → 迹（步名之表还原）。"""
    return {'跑': 样.get('跑') or {}, 'job': _解(样.get('job') or {}, 样.get('名表')), '環毕': 样.get('環毕') or {}, '唤': 样.get('唤') or []}


# ═══ 六、取样（总编辑手跑·沙盒：公仓之读）═══
def 取样(至, 出=样档, root=ROOT, 笔=None, 报引=None):
    """今之迹 → 回放之样：三流之跑（至 至[流]）、其 jobs、環毕、哨 PR 之言、备份/报 之史（至 报引之时）、祖之问之记；静之源取 笔 之树（自测 git show 之）。"""
    计 = [-10 ** 6]                                     # 取样⛔受每算 ≤20 之限（一回之手跑）
    令 = os.environ.get('GH_TOKEN_取样') or ''
    仓 = os.environ.get('GITHUB_REPOSITORY') or 'AlienRocketBus/ojedmksaemckdsokjmenjncdklerfml'
    迹, 限 = 取迹({}, 令, 仓, 计, 至=至, 新顶=10 ** 6, 页顶=5)
    报引 = 报引 or 'refs/remotes/origin/' + 报枝
    t至 = int(_git(['log', '-1', '--format=%ct', 报引], root).stdout.decode().strip())
    if 至 and 至.get('autopush'):                     # 算於：报引之时与 autopush 末跑（至）之毕取晚者（报先落、跑後毕）
        t至 = max([t至] + [r['毕'] for r in 迹['跑'].get('autopush') or [] if r['n'] == 至['autopush'] and r['毕']])
    报史 = 读报史(root, 报引)
    祖 = 祖器(root)
    文 = 读文(root, 笔)
    卡 = 算(迹, 文, t至, 祖, 报史)
    样 = {'说明': '运营卡之回放之样（W908 环5）：Actions 之迹（三流之跑、jobs、環毕、哨 PR 之言）经 REST 取（与 GitHub MCP actions_list／actions_get 同源）；'
                 '报史取 备份/报 之 git log；静之源取「笔」之树（自测 git show·史一字不移）；祖、亲 係取样时 git 之答（回放唯读之）。',
          '取於': _iso(int(time.time())), '算於': t至, '笔': 笔 or '', '报引': _git(['rev-parse', 报引], root).stdout.decode().strip(), '至': 至,
          '跑': _剪迹(迹)['跑'], '環毕': 迹['環毕'], '唤': 迹['唤'], '报史': 报史}
    样['job'], 样['名表'] = _压(_剪迹(迹)['job'])
    样.update(祖.记())
    样['限'] = 限 + ['#1—#53 之志已 404：不可考（坑27）——窗（末号−100）外，⛔计']
    os.makedirs(os.path.dirname(出), exist_ok=True)
    json.dump(样, open(出, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    return 样, 卡


# ═══ 七、自测 ═══
今之分 = {'autopush': (7, 15, 7, 6, 5, 8, 4, 3, 55), 'gate': (24, 18, 15, 6, 7, 8, 5, 5, 88),
         '巡': (24, 12, 12, 4, 6, 5, 3, 3, 69), '演练': (25, 14, 12, 7, 10, 8, 4, 5, 85)}
差之由 = {('巡', '安'): '方案计「冗权 −1」（巡之 pull-requests: write）係误判——PR 之 issue 评论须 pull-requests 之写：1120 备份/巡演 --试（run 44655946521）只读即 403，故去其扣（+1）', ('演练', '观'): '方案漏计 演练.yml --信 亦只书果（「演：$NAME（$REF …）→ ${GUO:-红}」⛔带因）——机算照尺同扣 −1（信不书因）'}


def 自测():
    R = []

    def T(名, 条):
        R.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)
    if not os.path.exists(样档):
        T('样在（工具/_负测料/运营卡/样.json）', False)
        print('── 负测·运营卡 0/1 未过 ──')
        return False
    样 = json.load(open(样档, encoding='utf-8'))
    文 = 读文(ROOT, 样['笔'])
    T('①样之静源可取（笔 %s 之树·git show）' % 样['笔'][:12], all(文.get('.github/workflows/' + 流档[f]) for f in 诸流) and 文.get('工具/接棒守.py'))
    迹 = 样之迹(样)
    祖 = 祖器(None, 样)
    卡 = 算(迹, 文, 样['算於'], 祖, 样['报史'])
    差, 印 = [], []
    for 流 in 诸流:
        f = 卡['流'][流]
        得 = tuple(f['维'][k] for k, _ in 尺) + (f['分'],)
        印.append('%s %s' % (流, 得[-1]))
        for i, (k, _) in enumerate(尺):
            if 得[i] != 今之分[流][i]:
                差.append((流, k, 得[i], 今之分[流][i]))
    未由 = [x for x in 差 if (x[0], x[1]) not in 差之由]
    T('②回放之分（%s）与方案「今之分」（autopush 55、gate 88、巡 69、演练 85）逐维对拍：%s' % (
        '、'.join(印), '全同' if not 差 else '差 %d 维（%s）俱书其由' % (len(差), '；'.join('%s·%s %s→%s：%s' % (a, b, d, c, 差之由.get((a, b), '⛔未由'))
                                                                          for a, b, c, d in 差))), not 未由)
    T('③每扣带 类、据、治；祖之问俱有记（回放⛔动 git）%s' % (('：缺 %d' % len(祖.缺)) if 祖.缺 else ''),
      卡['扣'] and all(x['类'] and x['据'] and x['治'] for x in 卡['扣']) and not 祖.缺)
    键 = {x['键'] for x in 卡['扣']}
    要 = {'autopush·稳·非意之败·merge', 'autopush·稳·被顶未吸', 'gate·稳·步挂', 'autopush·服·入主迟', 'autopush·服·手治', '巡·准·误告',
         '巡·稳·再起漏判', '巡·准·派必败', '巡·准·红之色迟', '演练·准·跑绿果红', '演练·准·取消落红报', 'gate·观·片红而跑绿', 'autopush·准·封前⊉GitHub'}
    T('④方案之扣之要俱机算而得（merge 八败、#149 被顶未吸、#68 步挂、入主 p90、手治、误告、#20 叠派、派必败、#31 红迟、演练二准、片红跑绿、封前）%s'
      % ('' if 要 <= 键 else '：缺 ' + '、'.join(sorted(要 - 键))), 要 <= 键)
    m = next((x for x in 卡['扣'] if x['键'] == 'autopush·稳·非意之败·merge'), {})
    T('④之二 merge 之败恰八（#81 #88 #92 #99 #105 #120 #124 #160）；被顶未吸唯 #149（#121 #127 #154 同坐後推自吸⛔扣）',
      m.get('次') == 8 and [x.split()[0] for x in m.get('据', [])] == ['#81', '#88', '#92', '#99', '#105', '#120', '#124', '#160']
      and [x.split()[0] for x in next((x for x in 卡['扣'] if x['键'] == 'autopush·稳·被顶未吸'), {}).get('据', [])] == ['#149'])
    # 变异一：去一非意之败（#81）→ 稳 +2
    样1 = json.loads(json.dumps(样))
    for r in 样1['跑']['autopush']:
        if r['n'] == 81:
            r['果'] = 'success'
    样1['报史'] = [v for v in 样1['报史'] if v['跑'] != '44267608150']
    卡1 = 算(样之迹(样1), 文, 样['算於'], 祖器(None, 样), 样1['报史'])
    T('⑤变异一：去一非意之败（#81）→ autopush 稳 +2（%s→%s）' % (卡['流']['autopush']['维']['稳'], 卡1['流']['autopush']['维']['稳']),
      卡1['流']['autopush']['维']['稳'] == 卡['流']['autopush']['维']['稳'] + 2)
    # 变异二：今树之 autopush.yml（钉 sha·Node24）→ 安满；加一 tag 之 uses → 安 −2
    今文 = dict(文, **{'.github/workflows/autopush.yml': open(os.path.join(ROOT, '.github', 'workflows', 'autopush.yml'), encoding='utf-8').read()})
    卡2 = 算(迹, 今文, 样['算於'], 祖器(None, 样), 样['报史'])
    变 = 今文['.github/workflows/autopush.yml'].replace('      - name: 演章', '      - uses: actions/checkout@v5\n      - name: 演章', 1)
    卡3 = 算(迹, dict(今文, **{'.github/workflows/autopush.yml': 变}), 样['算於'], 祖器(None, 样), 样['报史'])
    T('⑤之二 变异二：今树 autopush.yml（钉 40 位 sha·Node24）安 %s；加一 tag 之 uses → 安 −2（%s）' % (卡2['流']['autopush']['维']['安'], 卡3['流']['autopush']['维']['安']),
      卡2['流']['autopush']['维']['安'] == 10 and 卡3['流']['autopush']['维']['安'] == 8 and 变 != 今文['.github/workflows/autopush.yml'])
    T('⑤之三 钉之律：tag／未注版／Node20 之版俱缺；钉 sha 注 v5 之 checkout 合', 钉之缺('      - uses: actions/checkout@v4\n') and
      钉之缺('      - uses: actions/checkout@%s\n' % ('a' * 40)) and 钉之缺('      - uses: actions/upload-artifact@%s # v4.6.2\n' % ('a' * 40))
      and not 钉之缺('      - uses: actions/checkout@%s # v5.1.0\n      - uses: ./.github/workflows/gate.yml\n' % ('a' * 40)))
    # 进化之账：再算（旧卡）首见留；销者入史；复见即复发
    t2 = 样['算於'] + 3600
    卡4 = 算(迹, 今文, t2, 祖器(None, 样), 样['报史'], 旧卡=卡)
    销 = {x['键'] for x in 卡['扣']} - {x['键'] for x in 卡4['扣']}
    卡5 = 算(迹, 文, t2 + 3600, 祖器(None, 样), 样['报史'], 旧卡=卡4)
    同 = next((x for x in 卡4['扣'] if x['键'] == 'autopush·稳·非意之败·merge'), {})
    T('⑥进化之账：同键再见首见留（%s）；治而销者入史（%d：%s）；销後复见标复发；同类及二流者列' % (str(同.get('首见'))[5:16], len(销), '、'.join(sorted(销))[:60]),
      同.get('首见') == _iso(样['算於']) and 'autopush·安·tag或Node20' in 销 and any(h['键'] == 'autopush·安·tag或Node20' for h in 卡4['史'])
      and 'autopush·安·tag或Node20' in 卡5['复发'] and 'tag或Node20' in 卡['同类及二流'])
    with tempfile.TemporaryDirectory() as t:
        p = 写卡(卡, t, 迹, 趋=[(卡['算於'], 卡['流'])])
        d = json.load(open(p, encoding='utf-8'))
        md = open(os.path.join(t, 卡md径), encoding='utf-8').read()
        s = 摘(卡4, 卡)
        T('⑦写：报/卡.json（算於 ISO·流·扣·迹之存；⛔顶层「果」——法用之守 {报: 卡, 新: 24} 只验鲜）、报/卡.md（表、趋、扣）；摘（表、增减）',
          re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', d['算於']) and set(诸流) <= set(d['流']) and d['扣'] and '果' not in d
          and d['迹']['job'] and '| autopush |' in md and '近十卡之分趋' in md and '| 流 |' in s and '本跑之增减' in s
          and os.path.getsize(p) < 600 * 1024)
    # 降级：Actions 之迹全无（沙盒无令·读不得）→ 只报与静析，⛔抛
    卡6 = 算({'跑': {}, 'job': {}}, 文, 样['算於'], 祖器(None, 样), 样['报史'])
    T('⑧降级：无 Actions 之迹 → 只报与静析而成卡（⛔抛）；静之扣照在（安·tag、观·无summary）',
      卡6['流'] and any(x['键'] == 'gate·安·tag或Node20' for x in 卡6['扣']) and any(x['键'] == 'autopush·观·无summary' for x in 卡6['扣']))
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, '报'))
        json.dump(dict(卡, 算於=_iso(int(time.time()) - 25 * 3600)), open(os.path.join(t, 卡径), 'w', encoding='utf-8'), ensure_ascii=False)
        _git(['init', '-q', t], t)
        for k, v in (('user.name', 't'), ('user.email', 't@t')):
            _git(['config', k, v], t)
        _git(['add', '-A'], t)
        _git(['commit', '-qm', '卡'], t)
        _git(['update-ref', 'refs/remotes/origin/' + 报枝, 'HEAD'], t)
        行 = 一行(t, 取=False)
    T('⑨读（法用之守 --报读 之接口）：一行、卡旧逾 24 时 ⚠、最低之流（%s）' % 行[:50], 行.startswith('⚠') and '卡旧逾 24 时' in 行 and '最低 autopush 55' in 行)
    # ⑩—⑭ 复核之钉（W908 环5·静探之实、步挂之底、坑53）
    今源 = 读文(ROOT)
    今A = 今源['.github/workflows/autopush.yml']
    去注 = re.sub(r'(?m)^(\s*)python3 工具/推报\.py --注 "\$D"(\s+#)', r'\1true\2', 今A, count=1)
    键 = lambda 卡_: {x['键'] for x in 卡_['扣']}
    卡10, 卡10b = (算(迹, dict(今源, **{'.github/workflows/autopush.yml': t}), 样['算於'], 祖器(None, 样), 样['报史']) for t in (今A, 去注))
    T('⑩观·红行无注之探唯其码：今树 autopush.yml（推报 --注 之调）⛔扣；去其调而留头注之「::error」字 → 扣（注中之字⛔充其实·同 推报 ⑳）',
      去注 != 今A and '::error' in 去注 and 'autopush·观·红行无注' not in 键(卡10) and 'autopush·观·红行无注' in 键(卡10b))
    法源 = 今源.get('工具/法用之守.py') or ''
    尾 = re.search(r'(?m)^    return 行\n(?=\n\n# ─+ 自测)', 法源)
    接法 = (法源[:尾.start()] + '    行.append(运营卡.一行(root, 取=False))\n' + 法源[尾.start():]) if 尾 else ''
    假法 = 法源.replace('    """自走之首（零 token·一取）', '    # 运营卡.一行 报/卡.json（注而⛔调）\n    """自走之首（零 token·一取）报/卡.json 运营卡.一行（文档⛔算）', 1)
    卡11 = [算(迹, dict(今源, **{'工具/法用之守.py': t}), 样['算於'], 祖器(None, 样), 样['报史']) for t in (法源, 接法, 假法)]
    进键 = {'autopush·进·无计无读者', '巡·进·无计无读者'}
    T('⑪进·无计无读者：卡在（autopush 调 --算）而 法用之守.报之读 未读卡 → 照扣；报之读之码调 运营卡.一行 → 销；只注与文档言之 → 照扣（坑6 可达≠用）',
      bool(尾) and 进键 <= 键(卡11[0]) and not (进键 & 键(卡11[1])) and 进键 <= 键(卡11[2]) and 假法 != 法源
      and '有计无读者' in next(x for x in 卡11[0]['扣'] if x['键'] == 'autopush·进·无计无读者')['据'][0]
      and 进键 <= 键(卡))
    略 = next((x for x in 卡['限'] if x.startswith('步挂之底 %d 秒' % 步挂之底)), '')
    T('⑫步挂之底 %d 秒（尺无之）：逾十倍而 <5 分者略而⛔掩——卡之「限」列其数与逾一分者（#116 片 download-artifact 3 分·计否总编辑裁）' % 步挂之底,
      bool(re.search(r'略之 \d+', 略)) and '#116 44546510426' in 略 and 'download-artifact' in 略)
    账 = re.sub(r'(?m)^.*环11·[環环]之占机·裁：.*\n?', '', 今源.get('设定/方法账.md') or '')   # 〔1120〕真账已有裁行：先剔之，方测其判式（⛔为真账所染）
    卡13 = [算(迹, dict(今源, **{'设定/方法账.md': 账 + x}), 样['算於'], 祖器(None, 样), 样['报史'])
           for x in ('\n- 环11 之果：未裁·取不得（旧语）\n', '\n- 环11·環之占机·裁：留（据：GitHub 附加条款 Actions 一节）\n')]
    T('⑬平台之规未裁之探须裁之式「环11·環之占机·裁：留｜事驱…」：「环11…未裁」⛔销（旧探连「未裁」亦销）；裁之行在 → 销',
      '巡·安·平台之规未裁' in 键(卡13[0]) and '巡·安·平台之规未裁' not in 键(卡13[1]))
    with tempfile.TemporaryDirectory() as t:
        推报.写(推报.成报('章-9', 'a' * 40, '败', '⛔备候不成（因 merge）\n', 因='merge', 跑='https://x/actions/runs/7'), '', t)
        推报.写演(推报.成演报('试', 'x', 'b' * 40, '红', '✗ 字数闸  坏\n', 期='红', 跑='https://x/actions/runs/8'), '', t)
        本 = 读本报(t, 100)
    源 = open(os.path.abspath(__file__), encoding='utf-8').read().split('\ndef 自测(')[0]
    T('⑭坑53 同功唯一处：本跑之报经 推报.目之报（路、类、跑号俱得）、报史与卡之趋经 推报.诸报之史、旧卡经 推报._读报、钉律经 推报.钉式之缺；本器⛔自 cat-file',
      sorted((v['路'], v['类'], v['跑'], v['果'], v['期']) for v in 本) == [('报/推/章-9.json', '推', '7', '败', None), ('报/演/试.json', '演', '8', '红', '红')]
      and all(k in 源 for k in ('推报.目之报(', '推报.诸报之史(', '推报._读报(', '推报.钉式之缺(', '推报.诸uses('))
      and "'cat-file'" not in 源 and '坏果 = (' not in 源)
    今卡 = 算(迹, 今源, 样['算於'], 祖器(None, 样), 样['报史'])
    print('  · 今树之静（样之迹·今之源）：%s' % '、'.join('%s %s' % (f, 今卡['流'][f]['分']) for f in 诸流))
    ok = sum(R)
    print('── 负测·运营卡 %d/%d %s ──' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    return ok == len(R)


def _参(a, k, 缺=''):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else 缺


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--算' in a:
        try:
            sys.exit(算口(_参(a, '--出', '.'), '--摘' in a))
        except Exception as e:
            print('卡·算败：%s' % str(e)[:200])
            sys.exit(1)
    if '--读' in a:
        print(一行() or '· 云端无卡（报/卡.json）')
        sys.exit(0)
    if '--取样' in a:
        z = [int(x) for x in _参(a, '--至', '').split(',') if x.strip()] if _参(a, '--至') else []
        至 = dict(zip(有跑之流, z)) if z else None
        样, 卡 = 取样(至, 笔=_参(a, '--笔') or None, 报引=_参(a, '--报引') or None)
        print('✓ 样：%s（跑 %s；报史 %d；祖记 %d）' % (样档, '、'.join('%s %d' % (k, len(v)) for k, v in 样['跑'].items()), len(样['报史']), len(样['祖'])))
        print('  分：' + '、'.join('%s %s' % (f, 卡['流'][f]['分']) for f in 诸流))
        sys.exit(0)
    print(__doc__)
    sys.exit(0)
