#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""推报（1027 立·坑51；1027 坑54 改·分片之闸）——GitHub autopush 与 演练 之报：机写 `备份/报`，会话 git fetch 读之；并验诸 workflow 与 pre-push 之形、以桩真跑之。

【其由·坑51】404、406—410 之 autopush 俱败、唯 405 成，主枝只由沙盒直推而进：旧 yml 一树二跑闸、无取无重试、无报。
【其由·坑54】坑51 之治後，GitHub 之闸仍一 job 串跑（二核之机 722—1140 秒）：主枝含章-N 方派下一章，闸即在关键路上；
  器红账（设定/器红账.json）在 .gitignore，GitHub 之机每跑皆新、首见恒为本章——X55「器之红限三章治」从未生效；改流程之物无处先演。
【其法·零 token】
  ①写（GitHub 之机）：`--写` 出 报/推/<枝>.json（ref、sha、果、红、main_after、时、run_url，并 因、试、器红、逾、候、片、演）与末八十行之 txt；
    `--写演` 出 报/演/<名>.json（名、ref、sha、果：过｜红、红、时、run_url，并 候、因、片）；`--落 目` 把目下诸档并入 备份/报（取而再推，至多五回）。
  ②读（沙盒）：`读(枝)`、`读演(名)` git show 云端之报——推.py --候、接棒守 --候主 俱经此；`坏(d)` 判坏果（败·重派 係在飞、⛔作坏）；`快进()`。
    `诸报()` 一取而读 报/推、报/演 之全（法用之守：自走之首之 报之读、流程之法之 演录）。
  ③验：`验(诸文, 钩)` 静验二形——乙（分片：autopush 调 gate.yml，备候、N 片、并判、推候、器红账、演章、演练）照乙之律；
    甲（一 job·推时之钩即闸，97286329 之形）照甲之律；旧 yml（540c1c91·一树二跑）回灌须红。`验盘` 另索乙形（坑54）。⛔依 PyYAML（片之机无之）：本器自析其子集。
  ④演：以桩真跑诸 workflow（式之值、job 之序、矩阵、复用之流、上下传之件）於临时之裸库——成、已在、红、器红、逾限、拒、片崩、闸中主进而重派、
    重派之续、重派已尽、闸中已在、章（演章）、演练（派与推二触）。
用法：
  python3 工具/推报.py --读 章-411        # 印云端之报（无即 rc=1；坏果 rc=3）
  python3 工具/推报.py --读演 <名>        # 印演练之报（无 rc=1；红 rc=3）
  python3 工具/推报.py --验               # 静验 .github/workflows/{autopush,gate,演练}.yml 与 工具/githooks/pre-push
  python3 工具/推报.py --写 --ref R --sha S --果 G [--因 Y] [--试 K] --印 档 --主 SHA --跑 URL --出 目 [--候 C --判 档 --演 档]
  python3 工具/推报.py --写演 --名 N --ref R --sha S --果 过|红 [--因 Y] --印 档 --跑 URL --出 目 [--候 C --判 档]
  python3 工具/推报.py --落 目 --信 语      # 目下诸档并入 备份/报（GitHub 之机用）
  python3 工具/推报.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, time, shutil, tempfile, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
主枝 = 'claude/the-novel-review-4dtuit'
报枝 = '备份/报'
诸果 = ('成', '已在', '红', '拒', '败')
坏果 = ('红', '拒', '败')
暂存之前缀 = ('refs/heads/章-*', 'refs/heads/治-*', 'refs/heads/备份/*')
旧yml之笔 = '540c1c91'      # 坑51 之前之 autopush.yml（一闸二跑、无取无重试、无报）——自测回灌须红
单闸yml之笔 = '97286329'    # 坑54 之前之 autopush.yml（一 job、推时之钩即闸）——甲形，静验照判为合；而盘上须乙形
流之档 = ('autopush.yml', 'gate.yml', '演练.yml')
演之前缀 = '备份/演/'


def 报径(枝, 式='json'):
    return '报/推/%s.%s' % (枝, 式)


def 演名(名):
    """演之名：去「备份/演/」之前缀、斜作横（报/演/<名>.json 一层）。"""
    名 = str(名 or '').strip()
    if 名.startswith(演之前缀):
        名 = 名[len(演之前缀):]
    return 名.replace('/', '-').strip() or '无名'


def 演径(名, 式='json'):
    return '报/演/%s.%s' % (演名(名), 式)


# ═══ 一、写（GitHub 之机） ═══
def 红行(印):
    """→ 闸之红行：含 ✗ 之行、「⛔全测未过：」之行、「⛔推闸」「⛔片闸」起首之行（去重、存序、至多六十）。"""
    出 = []
    for l in (印 or '').split('\n'):
        s = l.strip()
        if s and ('✗' in s or '⛔全测未过：' in s or s.startswith('⛔推闸') or s.startswith('⛔片闸')) and s not in 出:
            出.append(s[:300])
    return 出[:60]


def 器红(印):
    """→ 只器之红之名（推闸·分等放行之行）。"""
    m = re.search(r'✓推闸·分等：放行——只器之红 \d+（([^）]*)）', 印 or '')
    return [x for x in m.group(1).split('、') if x] if m else []


def 要行(印):
    """拒、败而无 ✗ 之行者：取其由（⛔、error、fatal、! [ 之行；至多十二）。"""
    出 = []
    for l in (印 or '').split('\n'):
        s = l.strip()
        if s and (s.startswith('⛔') or 'error:' in s or 'fatal:' in s or s.startswith('! [')) and s not in 出:
            出.append(s[:300])
    return 出[-12:]


def _读json(档):
    try:
        d = json.load(open(档, encoding='utf-8'))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _读演之印(档):
    """演章之印（存底.py --演章 之末行）→ {果: 过｜红, 语}；无档即 None。"""
    try:
        行 = [x.strip() for x in open(档, encoding='utf-8', errors='replace').read().split('\n') if x.strip()]
    except Exception:
        return None
    末 = next((x for x in reversed(行) if x[:1] in ('✓', '⛔')), 行[-1] if 行 else '⛔演章无印')
    return {'果': '过' if 末.startswith('✓') else '红', '语': 末[:300]}


def 成报(ref, sha, 果, 印, 主='', 跑='', 因='', 试=0, 时=None, 候='', 判=None, 演=None):
    果 = 果 if 果 in 诸果 else '败'
    红 = 红行(印) if 果 in 坏果 else []
    if 果 in ('拒', '败') and not 红:
        红 = 要行(印)
    判 = 判 or {}
    d = {'ref': ref, 'sha': sha, '果': 果, '红': 红, 'main_after': 主 or '',
         '时': 时 or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'run_url': 跑 or '',
         '因': 因 or '', '试': int(试 or 0), '器红': list(判.get('器红') or 器红(印)), '逾': list(判.get('逾') or []), '候': 候 or ''}
    if 判.get('片秒'):
        d['片'] = {'数': len(判['片秒']), '秒': 判['片秒']}
    if 演 is not None:
        d['演'] = 演
    return d


def 写(d, 印, 出目):
    """→ (json 之路, txt 之路)：出目/报/推/<ref>.json 与 .txt（印之末八十行）。"""
    j = os.path.join(出目, 报径(d['ref']))
    x = os.path.join(出目, 报径(d['ref'], 'txt'))
    os.makedirs(os.path.dirname(j), exist_ok=True)
    json.dump(d, open(j, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(x, 'w', encoding='utf-8').write('\n'.join((印 or '').rstrip('\n').split('\n')[-80:]) + '\n')
    return j, x


def 成演报(名, ref, sha, 果, 印, 跑='', 因='', 候='', 判=None, 时=None):
    判 = 判 or {}
    果 = '过' if 果 == '过' else '红'
    红 = 红行(印) if 果 == '红' else []
    if 果 == '红' and not 红:
        红 = 要行(印) or ['⛔%s' % (因 or '未判')]
    d = {'名': 演名(名), 'ref': ref, 'sha': sha, '果': 果, '红': 红,
         '时': 时 or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'run_url': 跑 or '', '候': 候 or '', '因': 因 or ''}
    if 判.get('片秒'):
        d['片'] = {'数': len(判['片秒']), '秒': 判['片秒']}
    return d


def 写演(d, 印, 出目):
    j = os.path.join(出目, 演径(d['名']))
    os.makedirs(os.path.dirname(j), exist_ok=True)
    json.dump(d, open(j, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(os.path.join(出目, 演径(d['名'], 'txt')), 'w', encoding='utf-8').write('\n'.join((印 or '').rstrip('\n').split('\n')[-80:]) + '\n')
    return j


def 落(目, 信, root='.', 次=5, 睡=time.sleep):
    """目下诸档（相对之路即其於 备份/报 之路）并入 备份/报：取、读其树、添、建、推（钩指空目——暂存之枝⛔闸）；被拒即再取（至多五回）。→ (成否, 语)"""
    档们 = []
    for dp, _, fs in os.walk(目):
        for f in fs:
            档们.append(os.path.relpath(os.path.join(dp, f), 目))
    if not 档们:
        return False, '⛔落：目下无档'
    空钩 = tempfile.mkdtemp(prefix='无钩_')
    idx = os.path.join(tempfile.mkdtemp(prefix='报idx_'), 'i')
    try:
        for k in range(1, 次 + 1):
            env = dict(os.environ, GIT_INDEX_FILE=idx)
            g = lambda a, **kw: subprocess.run(['git', '-c', 'core.quotepath=off'] + a, cwd=root, capture_output=True, text=True, **kw)
            远 = 'refs/remotes/origin/' + 报枝
            有 = g(['fetch', '-q', 'origin', '+refs/heads/%s:%s' % (报枝, 远)]).returncode == 0
            if os.path.exists(idx):
                os.remove(idx)
            g(['read-tree', 远] if 有 else ['read-tree', '--empty'], env=env)
            for p in sorted(档们):
                h = g(['hash-object', '-w', os.path.join(os.path.abspath(目), p)]).stdout.strip()
                g(['update-index', '--add', '--cacheinfo', '100644,%s,%s' % (h, p.replace(os.sep, '/'))], env=env)
            树 = g(['write-tree'], env=env).stdout.strip()
            c = g(['commit-tree', 树] + (['-p', 远] if 有 else []) + ['-m', 信]).stdout.strip()
            if c and g(['-c', 'core.hooksPath=' + 空钩, 'push', '-q', 'origin', '%s:refs/heads/%s' % (c, 报枝)]).returncode == 0:
                return True, '✓落 → %s：%s' % (报枝, '、'.join(sorted(档们)[:6]))
            睡(k * 3)
        return False, '⛔落不上 %s（%d 试）' % (报枝, 次)
    finally:
        shutil.rmtree(空钩, ignore_errors=True)
        shutil.rmtree(os.path.dirname(idx), ignore_errors=True)


# ═══ 二、读（沙盒） ═══
_定库之变 = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES')


def _git(a, root=ROOT, 限=120):
    """⛔承外之 GIT_DIR 诸变（钩中、演中）——库只由 root 定。"""
    e = {k: v for k, v in os.environ.items() if k not in _定库之变}
    return subprocess.run(['git', '-c', 'core.quotepath=off'] + a, cwd=root, capture_output=True, text=True, timeout=限, env=e)


def _读报(路, root=ROOT, 取=True):
    远 = 'refs/remotes/origin/' + 报枝
    try:
        if 取:
            _git(['fetch', '-q', 'origin', '+refs/heads/%s:%s' % (报枝, 远)], root)
        r = _git(['show', '%s:%s' % (远, 路)], root)
        if r.returncode != 0 or not r.stdout.strip():
            return None
        d = json.loads(r.stdout)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def 读(枝, root=ROOT, 取=True):
    """→ 云端 备份/报 里 报/推/<枝>.json 之 dict；无、读不出即 None（⛔作绿）。"""
    return _读报(报径(枝), root, 取)


def 读演(名, root=ROOT, 取=True):
    """→ 云端 报/演/<名>.json 之 dict；无即 None。"""
    return _读报(演径(名), root, 取)


def 坏(d):
    """报之果坏否：红／拒／败——唯「败·重派」（被拒而已自重派本枝）係在飞、⛔作坏（候者照候其新跑之报）。"""
    return bool(d) and d.get('果') in 坏果 and not (d.get('果') == '败' and d.get('因') == '重派')


def 诸报(root=ROOT, 取=True, 类=('推', '演'), 并=()):
    """→ 云端 备份/报 里 报/<类>/*.json 之诸 dict（各添「路」「类」）；一取（并之枝同一回 fetch）；无枝、读不出即 []（⛔作绿·⛔抛）。
    法用之守之 报之读（自走之首）与 演录（GitHub 之演）俱经此——⛔另造一把尺。"""
    远 = 'refs/remotes/origin/' + 报枝
    try:
        if 取:
            参 = ['+refs/heads/%s:refs/remotes/origin/%s' % (b, b) for b in (报枝,) + tuple(并)]
            if _git(['fetch', '-q', 'origin'] + 参, root).returncode != 0 and 并:
                _git(['fetch', '-q', 'origin'] + 参[1:], root)      # 云端尚无 备份/报：同取全败——并者单取（同 推._取）
        r = _git(['ls-tree', '-r', '--name-only', 远, '--'] + ['报/%s/' % k for k in 类], root)
        路们 = [p for p in r.stdout.split('\n') if p.endswith('.json')] if r.returncode == 0 else []
        if not 路们:
            return []
        e = {k: v for k, v in os.environ.items() if k not in _定库之变}
        b = subprocess.run(['git', 'cat-file', '--batch'], input=''.join('%s:%s\n' % (远, p) for p in 路们).encode('utf-8'),
                           cwd=root, capture_output=True, timeout=120, env=e).stdout
    except Exception:
        return []
    出, i = [], 0
    for p in 路们:
        j = b.find(b'\n', i)
        if j < 0:
            break
        头 = b[i:j].split()
        if len(头) < 3 or 头[1] != b'blob':
            i = j + 1
            continue
        n = int(头[2])
        体, i = b[j + 1:j + 1 + n], j + 1 + n + 1
        try:
            d = json.loads(体.decode('utf-8'))
        except Exception:
            d = {'果': '坏'}
        if isinstance(d, dict):
            d['路'], d['类'] = p, p.split('/')[1]
            出.append(d)
    return 出


def 报之语(d):
    """→ 印之行：果、因、红行、器红、演、run_url。"""
    L = ['%s 报·%s（%s）：%s%s｜%s' % ('✓' if d.get('果') in ('成', '已在', '过') else ('·' if not 坏(d) else '⛔'), d.get('ref'),
                                     str(d.get('sha', ''))[:12], d.get('果'), ('（因 %s）' % d['因']) if d.get('因') else '', d.get('时', ''))]
    L += ['    ' + x for x in (d.get('红') or [])[:20]]
    if d.get('器红'):
        L.append('    · 器红（只报不拦·限三章治；账在 备份/报 之 报/器红账.json）：' + '、'.join(d['器红']))
    if d.get('逾'):
        L.append('    ⛔ 器红逾限（拦）：' + '、'.join(d['逾']))
    if isinstance(d.get('演'), dict):
        L.append('    · 演章：' + str(d['演'].get('语', '')))
    if d.get('run_url'):
        L.append('    · ' + d['run_url'])
    return L


def 快进(root=ROOT):
    """成而後：本地主枝快进到 origin 主枝（能则进；不在主枝、本地有未入主之提交即⛔动）。→ (进否, 语)
    ⛔抛：主枝已含而取卡（逾时）即崩，候者印「✓已含」而返非零——调者（推.py --候、接棒守 --候主）之 rc 遂误。"""
    try:
        return _快进(root)
    except Exception as e:
        return False, '⛔ 快进不成：%s' % str(e)[:200]


def _快进(root=ROOT):
    远 = 'refs/remotes/origin/' + 主枝
    _git(['fetch', '-q', 'origin', '+refs/heads/%s:%s' % (主枝, 远)], root)
    当 = _git(['symbolic-ref', '-q', '--short', 'HEAD'], root).stdout.strip()
    if 当 != 主枝:
        return False, '· 快进：HEAD 不在 %s（今 %s）——⛔动' % (主枝, 当 or '游离')
    h, o = _git(['rev-parse', 'HEAD'], root).stdout.strip(), _git(['rev-parse', 远], root).stdout.strip()
    if not o:
        return False, '· 快进：取不到 origin 主枝——⛔动'
    if h == o:
        return True, '· 快进：本地已同 origin 主枝（%s）' % h[:12]
    if _git(['merge-base', '--is-ancestor', 'HEAD', 远], root).returncode != 0:
        return False, '· 快进：本地有未入主之提交——⛔快进（照旧）'
    r = _git(['merge', '-q', '--ff-only', 远], root)
    return (r.returncode == 0), ('✓ 快进：%s → %s' % (h[:12], o[:12]) if r.returncode == 0
                                 else '⛔ 快进不成：%s' % (r.stderr or r.stdout).strip()[:200])


# ═══ 三、验（静） ═══
# YAML 之子集（本仓诸 workflow 所用：块之映与列、流之列、引号、| 之块、注）——片之机 setup-python 无 PyYAML，⛔依之；自测以 PyYAML 对之。
_键式 = re.compile(r'''^("[^"]*"|'[^']*'|[^\s'"#\[\]{},&*!|>%@`-][^:]*?|-[^\s:][^:]*?):(?:[ \t]+(.*))?$''')


def _去注(s):
    q = None
    for i, c in enumerate(s):
        if q:
            if c == q:
                q = None
        elif c in '\'"' and (i == 0 or s[i - 1] in ' \t[,{:('):
            q = c
        elif c == '#' and (i == 0 or s[i - 1] in ' \t'):
            return s[:i].rstrip()
    return s


def _分逗(s):
    出, 深, q, 当 = [], 0, None, ''
    for c in s:
        if q:
            q = None if c == q else q
        elif c in '\'"':
            q = c
        elif c in '[{':
            深 += 1
        elif c in ']}':
            深 -= 1
        elif c == ',' and 深 == 0:
            出.append(当)
            当 = ''
            continue
        当 += c
    if 当.strip():
        出.append(当)
    return 出


def _标(s):
    s = (s or '').strip()
    if not s:
        return None
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return s[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    if s[0] == '[' and s[-1] == ']':
        return [_标(x) for x in _分逗(s[1:-1])]
    if s == '{}':
        return {}
    return s


def _yaml(文):
    """本仓 workflow 之 YAML 子集 → dict／list／str（标量俱作字串；null 作 None）。"""
    L = [l.rstrip('\r') for l in (文 or '').split('\n')]
    空 = lambda l: not l.strip() or l.strip().startswith('#')
    缩 = lambda l: len(l) - len(l.lstrip(' '))
    列首 = lambda l: l.lstrip().startswith('- ') or l.strip() == '-'

    def 块(i, 至少):
        while i < len(L) and 空(L[i]):
            i += 1
        if i >= len(L) or 缩(L[i]) < 至少:
            return None, i
        return (列 if 列首(L[i]) else 映)(i, 缩(L[i]))

    def 列(i, n):
        出 = []
        while True:
            while i < len(L) and 空(L[i]):
                i += 1
            if i >= len(L) or 缩(L[i]) != n or not 列首(L[i]):
                return 出, i
            体 = L[i].lstrip()[1:]
            if not 体.strip():
                v, i = 块(i + 1, n + 1)
                出.append(v)
                continue
            k = n + 1 + 缩(体)
            if _键式.match(体.strip()):
                L[i] = ' ' * k + 体.strip()
                v, i = 映(i, k)
            else:
                v, i = _标(_去注(体)), i + 1
            出.append(v)

    def 映(i, n):
        出 = {}
        while True:
            while i < len(L) and 空(L[i]):
                i += 1
            if i >= len(L) or 缩(L[i]) != n or 列首(L[i]):
                return 出, i
            m = _键式.match(L[i][n:])
            if not m:
                raise ValueError('YAML 之行不识（第 %d 行）：%s' % (i + 1, L[i][:80]))
            键, 余 = _标(m.group(1)), _去注(m.group(2) or '').strip()
            i += 1
            if 余[:1] in ('|', '>') and 余.rstrip('+-') in ('|', '>'):
                体 = []
                while i < len(L) and (not L[i].strip() or 缩(L[i]) > n):
                    体.append(L[i])
                    i += 1
                while 体 and not 体[-1].strip():
                    体.pop()
                c = min((缩(x) for x in 体 if x.strip()), default=0)
                v = '\n'.join(x[c:] for x in 体)
                出[键] = (v + ('' if 余.endswith('-') else '\n')) if 余[0] == '|' else ' '.join(x.strip() for x in 体)
            elif 余 == '':
                j = i
                while j < len(L) and 空(L[j]):
                    j += 1
                if j < len(L) and (缩(L[j]) > n or (缩(L[j]) == n and 列首(L[j]))):
                    出[键], i = 块(j, n)
                else:
                    出[键] = None
            else:
                出[键] = _标(余)
    v, i = 块(0, 0)
    while i < len(L) and 空(L[i]):
        i += 1
    if i < len(L):
        raise ValueError('YAML 有余（第 %d 行）：%s' % (i + 1, L[i][:80]))
    return v


def _诸job(w):
    return (w or {}).get('jobs') or {}


def _诸步(w):
    return [s for j in _诸job(w).values() for s in (j.get('steps') or [])]


def _跑文(w):
    return [s.get('run') or '' for s in _诸步(w)]


def _式本(x):
    return re.sub(r'^\$\{\{\s*|\s*\}\}$', '', str(x or '').strip())


def _环(文):
    """→ [(起, 止, 回数)]：`for v in 1 2 3; do … done`（同缩之 done）。"""
    出 = []
    for m in re.finditer(r'(?m)^(\s*)for \w+ in ([\d ]+); do\s*$', 文):
        缩 = m.group(1)
        d = re.compile(r'(?m)^%sdone\b' % re.escape(缩)).search(文, m.end())
        if d:
            出.append((m.start(), d.start(), len(m.group(2).split())))
    return 出


# 推主枝之形：refspec 之的为主枝——带 refs/heads/ 与否、$MAIN／${MAIN}／字面（B-v 驳：旧式只认「refs/heads/$MAIN」而 \b 不认 ${MAIN}，"$CAND:$MAIN" 之短式漏）
_主推式 = re.compile(r'git\s+(?:-c\s+\S+\s+)*push\b[^\n]*?[\s:"\'](?:refs/heads/)?(?:\$MAIN|\$\{MAIN\}|' + re.escape(主枝) + r')(?![\w/-])')
_推式 = re.compile(r'git\s+(?:-c\s+\S+\s+)*push\b[^\n]*')
# 直跑钩之形：行首、;&|!( 之後、then／do／else、bash／sh／source／exec 之後（⛔只认行首——`if ! bash 工具/githooks/pre-push` 亦一树二跑）
_直钩式 = re.compile(r'(?m)(?:^|[;&|!(]|\b(?:then|do|else|bash|sh|source|exec)\b)\s*(?:\./)?["\']?[^\s"\';|&]*(?:工具/githooks|钩)/pre-push\b')
_直闸式 = re.compile(_直钩式.pattern + r'|python3?\s+[^\n]*工具/全测并?\.py')
_绕式 = ('--no-verify', 'ZM_SKIP_HOOK')


def _验钩(钩):
    缺 = []
    if not re.search(r'while read -r \w+ \w+ (\w+) \w+', 钩 or ''):
        缺.append('⑩钩：须读 stdin 之 ref 行（while read -r 本ref 本sha 远ref 远sha）')
    else:
        免 = re.findall(r'(?m)^\s*([^\s()#]+(?:\|[^\s()]+)*)\)\s*N_STAGE=', 钩)
        式 = set(免[0].split('|')) if len(免) == 1 else set()
        if 式 != set(暂存之前缀):
            缺.append('⑩钩：免闸之前缀须恰 章-*、治-*、备份/*（今 %s）' % (sorted(式) or 免))
        if not re.search(r'"\$N_ALL" -eq "\$N_STAGE"', 钩):
            缺.append('⑩钩：须所推俱係暂存方免（N_ALL == N_STAGE）')
    if 'python3 工具/全测并.py' not in (钩 or '') or '推闸之果' not in (钩 or ''):
        缺.append('⑪钩：余者照跑 全测并、落 推闸之果')
    return 缺


def 验甲(yml, 钩):
    """甲形（一 job·推时之 pre-push 即闸·至多三试；97286329 之形）之律 → [缺]。"""
    缺 = []
    try:
        w = _yaml(yml) or {}
    except Exception as e:
        return ['⓪析：%s' % e]
    步 = _诸步(w)
    跑们 = [s.get('run') or '' for s in 步]
    env = (w.get('env') or {})
    on = w.get('on') or {}
    枝 = ((on.get('push') or {}) if isinstance(on.get('push'), dict) else {}).get('branches') or []
    if not ('章-*' in 枝 and '治-*' in 枝 and 'workflow_dispatch' in on):
        缺.append('①触：push 之 branches 须含 章-* 与 治-*、并 workflow_dispatch（今 %s%s）' % (枝, '' if 'workflow_dispatch' in on else '、无 workflow_dispatch'))
    cc = w.get('concurrency') or {}
    if not (isinstance(cc, dict) and cc.get('group') == 'autopush' and str(cc.get('cancel-in-progress')).lower() == 'false'):
        缺.append('②消：concurrency 须 group autopush、cancel-in-progress false')
    直 = [x for r in 跑们 for x in _直闸式.findall(r)]
    if 直:
        缺.append('③一闸：⛔直跑 pre-push／全测（推时之钩即闸；直跑而再推即一树二跑——坑51）：%s' % 直[:3])
    主推 = [(k, m) for k, r in enumerate(跑们) for m in _主推式.finditer(r)]
    if len(主推) != 1:
        缺.append('④一闸：推主枝之 push 须恰一处（今 %d）' % len(主推))
    else:
        k, m = 主推[0]
        r = 跑们[k]
        行 = r[r.rfind('\n', 0, m.start()) + 1: r.find('\n', m.end()) if r.find('\n', m.end()) >= 0 else len(r)]
        环 = [e for e in _环(r) if e[0] < m.start() < e[1]]
        挂 = re.search(r'git config core\.hooksPath 工具/githooks\s*$', r[:m.start()], re.M)
        if not 环 or 环[0][2] > 3:
            缺.append('④一闸：推主枝须在至多三试之环内（for i in 1 2 3）')
        if not 挂:
            缺.append('④一闸：推主枝之前须 git config core.hooksPath 工具/githooks（推时之钩即闸）')
        if any(x in 行 for x in _绕式 + ('core.hooksPath=',)):
            缺.append('④一闸：推主枝⛔绕钩（%s）' % 行.strip()[:120])
        if 环:
            体 = r[环[0][0]:环[0][1]]
            前, 後 = 体[:m.start() - 环[0][0]], 体[m.start() - 环[0][0]:]
            if not (re.search(r'git fetch[^\n]*\$MAIN', 前) and re.search(r'merge-base --is-ancestor "?\$(T|GITHUB_SHA)"?', 前)
                    and '已在' in 前 and re.search(r'git merge\b', 前) and re.search(r'T="?\$GITHUB_SHA"?', r)):
                缺.append('⑤取判再试：环中推前须 fetch 主枝、merge-base --is-ancestor 本 sha（已在即止）、并主枝')
            if not ('continue' in 後 and 'non-fast-forward' in 後 and re.search(r'!=\s*"\$B0"', 後)):
                缺.append('⑤取判再试：被拒（non-fast-forward 等）而主枝已进方 continue 再试（树变方重闸）')
            if not (re.search(r'git diff --name-only[^\n]*-- \.github/workflows', 前) and '拒' in 前 and 'YIN=workflow' in 前):
                缺.append('⑥拒：并後改 .github/workflows 者须先判「拒」（因 workflow；⛔白跑闸）')
            if '推闸之果' not in 体:
                缺.append('⑤取判再试：闸红与被拒须据 推闸之果 分（⛔凭 rc 混判）')
    报 = [s for s in 步 if 'always()' in str(s.get('if', '')) and '推报.py' in (s.get('run') or '')]
    报跑 = (报[0].get('run') or '') if 报 else ''
    报键 = ('--写', '--ref', '--sha', '--果', '--印', '--主', '--跑', '--出')
    if not 报 or not all(k in 报跑 for k in 报键) or re.search(r'success\(\)|env\.GUO', str(报[0].get('if', ''))):
        缺.append('⑦报：须有 if: always()（⛔系於成败）之步以 推报.py --写 出报（%s）' % '、'.join(报键))
    else:
        环 = _环(报跑)
        推报 = re.search(r'git\s+(?:-c\s+\S+\s+)*push\b[^\n]*refs/heads/(\$REPORT|' + re.escape(报枝) + ')', 报跑)
        if not (推报 and 环 and any(a < 推报.start() < b and 'git fetch' in 报跑[a:推报.start()] for a, b, _ in 环)):
            缺.append('⑦报：推 备份/报 须在取而再推之环内')
        if '$REPORT' in 报跑 and env.get('REPORT') != 报枝:
            缺.append('⑦报：env.REPORT 须係 %s（今 %s）' % (报枝, env.get('REPORT')))
        if '报/推/' not in 报跑:
            缺.append('⑦报：报之路须 报/推/<枝>')
    if env.get('MAIN', 主枝) != 主枝:
        缺.append('④一闸：env.MAIN 须係 %s' % 主枝)
    缺 += _验删(步, yml)
    绕 = [x for x in _绕式 if x in yml]
    if 绕:
        缺.append('⑨⛔绕闸之字：%s' % 绕)
    return 缺 + _验钩(钩)


def _验删(步, 全文):
    缺 = []
    删 = [s for s in 步 if re.search(r'--delete|":\$N"|:refs/heads/治-', s.get('run') or '')]
    if not 删 or not any('refs/heads/治-*' in (s.get('run') or '') and '成' in str(s.get('if', '')) for s in 删):
        缺.append('⑧删：治枝成（成／已在）即删')
    elif not all(re.search(r'merge-base --is-ancestor "?\$\w+"? "?origin/\$MAIN"?[^\n]*&& D\+=', s.get('run') or '') for s in 删):
        缺.append('⑧删：只删已为主枝之祖之治枝（⛔连在飞未并之治枝一并删）')
    if re.search(r'(--delete|:refs/heads/)[^\n]*章-', 全文) or any('章-' in (s.get('run') or '') for s in 删):
        缺.append('⑧删：⛔删 章-*（章标恒留）')
    return 缺


def 验乙(诸文, 钩):
    """乙形（坑54·分片）之律 → [缺]。诸文：{autopush.yml, gate.yml, 演练.yml: 文}。"""
    缺 = []
    try:
        A, G, Y = (_yaml(诸文.get(n) or '') or {} for n in 流之档)
    except Exception as e:
        return ['⓪析：%s' % e]
    if not (G and Y):
        return ['⓪档：乙形须 gate.yml 与 演练.yml 俱在（今缺 %s）' % '、'.join(n for n, w in (('gate.yml', G), ('演练.yml', Y)) if not w)]
    全文 = '\n'.join(诸文.get(n) or '' for n in 流之档)
    AJ, GJ, YJ = _诸job(A), _诸job(G), _诸job(Y)
    # ①触 ②消 ⑯常
    on = A.get('on') or {}
    枝 = ((on.get('push') or {}) if isinstance(on.get('push'), dict) else {}).get('branches') or []
    派 = on.get('workflow_dispatch') or {}
    if not ('章-*' in 枝 and '治-*' in 枝 and isinstance(派, dict) and 'tries' in (派.get('inputs') or {})):
        缺.append('①触：autopush 之 push 须含 章-* 与 治-*、并 workflow_dispatch（inputs.tries·重派之次）（今 %s）' % 枝)
    cc = A.get('concurrency') or {}
    if not (isinstance(cc, dict) and cc.get('group') == 'autopush' and str(cc.get('cancel-in-progress')).lower() == 'false'):
        缺.append('②消：concurrency 须 group autopush、cancel-in-progress false')
    for 名, w in zip(流之档, (A, G, Y)):
        e = w.get('env') or {}
        if e.get('MAIN') != 主枝 or e.get('REPORT') != 报枝:
            缺.append('⑯常：%s 之 env.MAIN／REPORT 须係 %s／%s' % (名, 主枝, 报枝))
    # ⑫调：autopush、演练 各恰一 job 用 gate.yml（mode 推／演）；gate 係 workflow_call 而只读
    def 调者(J, 式):
        x = [(k, j) for k, j in J.items() if str(j.get('uses') or '').strip() == './.github/workflows/gate.yml']
        return x[0] if len(x) == 1 and str((x[0][1].get('with') or {}).get('mode')) == 式 else (None, None)
    a调, _ = 调者(AJ, '推')
    y调, _ = 调者(YJ, '演')
    if not a调 or not y调:
        缺.append('⑫调：autopush（mode 推）与 演练（mode 演）须各恰一 job uses ./.github/workflows/gate.yml')
    if 'workflow_call' not in (G.get('on') or {}) or (G.get('permissions') or {}).get('contents') != 'read':
        缺.append('⑫调：gate.yml 须 on.workflow_call、permissions contents read（闸⛔写云端）')
    # ⑫片：备候（--片数）→ 矩阵之片（--片 k/N，候之树）→ 果交件（always）
    备 = [j for j in GJ.values() if any('--片数' in (s.get('run') or '') for s in j.get('steps') or [])]
    片 = [(k, j) for k, j in GJ.items() if ((j.get('strategy') or {}).get('matrix') or {}).get('k')]
    if len(备) != 1:
        缺.append('⑫片：gate.yml 须恰一备候之 job（全测.py --片数 择片数）')
    if len(片) != 1:
        缺.append('⑫片：gate.yml 须恰一矩阵之 job（matrix.k）')
    else:
        k片, j片 = 片[0]
        st = j片.get('strategy') or {}
        片跑 = '\n'.join(s.get('run') or '' for s in j片.get('steps') or [])
        if _式本(st['matrix']['k']) != 'fromJSON(needs.prepare.outputs.ks)' or str(st.get('fail-fast')).lower() != 'false':
            缺.append('⑫片：矩阵须 k: fromJSON(needs.prepare.outputs.ks)、fail-fast false（一片红⛔消他片）')
        if _式本(j片.get('if')) != "needs.prepare.outputs.go == '1'":
            缺.append("⑫片：片之 job 须 if: needs.prepare.outputs.go == '1'（已在／拒⛔白跑闸）")
        if str(j片.get('continue-on-error')).lower() != 'true':
            缺.append('⑫片：片之 job 须 continue-on-error: true（片红即 workflow_call 败而调者之 outputs 或空·actions/runner#2495——判归 --并果）')
        if not (re.search(r'git checkout[^\n]*"\$CAND"', 片跑) and re.search(r'rev-parse HEAD\)"? != "\$CAND"', 片跑)):
            缺.append('⑫片：片须检出候（"$CAND"）并验 HEAD 即候（⛔验他树）')
        if not re.search(r'工具/全测\.py --片 "\$K/\$N"[^\n]*--出 ', 片跑):
            缺.append('⑫片：片须跑 全测.py --片 "$K/$N" … --出')
        上 = [s for s in j片.get('steps') or [] if str(s.get('uses') or '').startswith('actions/upload-artifact')]
        if not 上 or 'always()' not in str(上[0].get('if', '')):
            缺.append('⑫片：片之果须 if: always() 上件（逾时亦交已跑者）')
    # ⑱省取（1117 GitHub 化之审·F·法用#闸取仓之速）：带 filter 之 checkout（partial clone）须 continue-on-error 而有 id，其 job 之跑验检出、
    #   不成即 quan_qu 降级全取（旧式 fetch-depth 0 无 filter）；片须以 GIT_TRACE2_EVENT 计懒取之败（lan_qu）而降级全取重跑——⛔因省取而红
    省步 = [(k, j) for k, j in GJ.items() for s in j.get('steps') or []
            if str(s.get('uses') or '').startswith('actions/checkout') and (s.get('with') or {}).get('filter')]
    QQ = str((G.get('env') or {}).get('QUANQU') or '')
    if 省步 and 'quan_qu()' not in QQ:
        缺.append('⑱省取：gate 之 env 须有 QUANQU（quan_qu：降级全取之函）')
    # ⑱之二 全取之取须再试（审·F 之治：旧 actions/checkout 之 fetch 经 RetryHelper 至多三回、回间随候 10—20 秒；降级之全取⛔劣於旧）——
    #   网取之再试，⛔1027 所废「机内取并再试」（for i in 1 2 3 之并环·法用之守 ⑧ 之去证仍守其字）
    再试 = re.search(r'zai_shi\(\) \{(.*?)\n\}', QQ, re.S)
    if 省步 and not (再试 and re.search(r'for n in 1 2 3; do', 再试.group(1)) and re.search(r'\$\(\(10 \+ RANDOM % 11\)\)', 再试.group(1))
                    and re.search(r'sleep "\$s"', 再试.group(1))
                    and re.search(r"zai_shi git -c protocol\.version=2 fetch [^\n]*'\+refs/heads/\*:refs/remotes/origin/\*'", QQ)
                    and not re.search(r"(?<!zai_shi )git -c protocol\.version=2 fetch", QQ)):
        缺.append('⑱省取：quan_qu 之全取须再试（zai_shi：至多三回、回间随候 10—20 秒——照 actions/checkout 之 RetryHelper）')
    for k, j in dict(省步).items():
        步 = j.get('steps') or []
        跑 = '\n'.join(s.get('run') or '' for s in 步)
        if any(str(s.get('continue-on-error')).lower() != 'true' or not s.get('id') for s in 步
               if str(s.get('uses') or '').startswith('actions/checkout') and (s.get('with') or {}).get('filter')) \
                or not re.search(r'eval "\$QUANQU"', 跑) or not re.search(r'\|\| quan_qu "\$WANT" "检出不成', 跑):
            缺.append('⑱省取：%s 之省取（filter）须 continue-on-error、有 id，其跑验检出而不成即降级全取（quan_qu）' % k)
        if ((j.get('strategy') or {}).get('matrix') or {}).get('k') and not (
                re.search(r'GIT_TRACE2_EVENT', 跑) and re.search(r'lan_qu "\$T2"', 跑) and re.search(r'quan_qu "\$WANT" "片中懒取败', 跑)):
            缺.append('⑱省取：片须计懒取之败（GIT_TRACE2_EVENT·lan_qu）而降级全取重跑')
    # ③一闸：全档之闸恰一处（片）；⛔直跑钩／全测并／全跑全测；GitHub 上诸推俱指空钩
    片令 = re.findall(r'工具/全测\.py --片 ', 全文)
    if len(片令) != 1:
        缺.append('③一闸：全测 --片 须恰一处（今 %d）——一候之树一闸' % len(片令))
    for r in _跑文(A) + _跑文(G) + _跑文(Y):
        if _直钩式.search(r) or re.search(r'工具/全测并\.py', r):
            缺.append('③一闸：⛔直跑 pre-push／全测并（闸已在片；再跑即一树二闸——坑51）')
            break
        if any(not re.match(r'\s*--(片|片数|并果)\b', r[m.end():]) for m in re.finditer(r'工具/全测\.py', r)):
            缺.append('③一闸：全测.py 只许 --片／--片数／--并果（⛔全跑）')
            break
    for r in _跑文(A) + _跑文(G) + _跑文(Y):
        for m in _推式.finditer(r):
            if not re.search(r'-c\s+core\.hooksPath="?\$RUNNER_TEMP/无钩"?', m.group(0)):
                缺.append('③一闸：GitHub 上之推须指空钩（core.hooksPath=$RUNNER_TEMP/无钩；闸已跑於片，⛔再闸）：%s' % m.group(0)[:80])
    if _推式.search('\n'.join(_跑文(G))):
        缺.append('③一闸：gate.yml ⛔推（闸⛔写云端）')
    # ④主推：autopush 之末 job 恰一处推候於主枝——并判过之後、推後验主枝含候；演练、gate ⛔推主枝
    主推 = [(k, s) for k, j in AJ.items() for s in j.get('steps') or [] if _主推式.search(s.get('run') or '')]
    if len(主推) != 1:
        缺.append('④主推：推主枝之 push 须恰一处（今 %d）' % len(主推))
    else:
        k, s = 主推[0]
        j = AJ[k]
        r = s.get('run') or ''
        m = _主推式.search(r)
        前, 後 = r[:m.start()], r[m.end():]
        need = j.get('needs')
        if (need if isinstance(need, list) else [need]) != [a调] or 'always()' not in str(j.get('if', '')):
            缺.append('④主推：推主枝之 job 须 needs 闸（gate）、if: always()（红、败亦报）')
        if '"$CAND:refs/heads/$MAIN' not in m.group(0):
            缺.append('④主推：所推须即候（"$CAND:refs/heads/$MAIN"）——⛔另并另推未闸之树')
        并 = re.search(r'工具/全测\.py --并果 [^\n]*--候 "\$CAND"', 前)
        if not (并 and re.search(r'rc=\$\?', 前[并.end():]) and re.search(r'\$rc -eq 1', 前) and re.search(r'\$rc -ne 0', 前)):
            缺.append('④主推：推前须 全测.py --并果 … --候 "$CAND"，且其 rc 0 方推（1 红、余败）')
        if not (re.search(r'git fetch[^\n]*\$MAIN', 後) and re.search(r'merge-base --is-ancestor "\$CAND" "origin/\$MAIN"', 後) and 'GUO=成' in 後):
            缺.append('④主推：推後须取主枝而验其含候，方报「成」')
        # ⑤已在、重派
        if not (re.search(r'merge-base --is-ancestor "\$T" "origin/\$MAIN"', 後) and 'GUO=已在' in 後):
            缺.append('⑤被拒：主枝已含本枝即「已在」')
        界 = re.search(r'"\$\{?TRIES(?::-0)?\}?" -lt ([0-9])', 後)
        if not ('/actions/workflows/autopush.yml/dispatches' in 後 and 'YIN=重派' in 後 and 界 and int(界.group(1)) <= 3
                and re.search(r'"\$MA" != "\$B0"', 後)):
            缺.append('⑤被拒：主枝已进而未含本枝须 API 重派本枝（至多三回·tries）、报「败·重派」')
        if (A.get('permissions') or {}).get('actions') != 'write':
            缺.append('⑤被拒：重派须 permissions actions: write')
    for 名, w in (('演练.yml', Y), ('gate.yml', G)):
        if any(_主推式.search(r) for r in _跑文(w)) or '"$CAND:refs/heads/$MAIN"' in (诸文.get(名) or ''):
            缺.append('④主推：%s ⛔推主枝' % 名)
    if _推式.search('\n'.join(_跑文(Y))) or re.search(r'git/refs\b', 诸文.get('演练.yml') or ''):
        缺.append('④主推：演练.yml ⛔git push、⛔动 git/refs（演只经 推报.py --落 写 备份/报：⛔推主枝、⛔删枝）')
    # ⑤已在 ⑥拒（备候）
    备跑 = '\n'.join(s.get('run') or '' for j in 备 for s in j.get('steps') or [])
    if not (re.search(r'"\$MODE" = 推[^\n]*merge-base --is-ancestor "\$T" "origin/\$MAIN"', 备跑) and 'GUO=已在' in 备跑):
        缺.append('⑤已在：备候须判本枝已为主枝之祖即「已在」（推之式）而免闸')
    if not (re.search(r'"\$MODE" = 推[^\n]*git diff --name-only "\$B0" HEAD -- \.github/workflows', 备跑) and 'GUO=拒' in 备跑 and 'YIN=workflow' in 备跑):
        缺.append('⑥拒：备候须判所并之树改 .github/workflows 即「拒」（推之式；⛔白跑闸）')
    if not re.search(r'git branch -f 候 "\$C" && git bundle create[^\n]* 候 --not "\$B0" "\$T"', 备跑):
        缺.append('⑫片：候须以 git bundle 交诸片（⛔推临时之枝）')
    # ⑦报
    def 报步(J, 键们):
        for j in J.values():
            for s in j.get('steps') or []:
                r = s.get('run') or ''
                if 'always()' in str(s.get('if', '')) and all(x in r for x in 键们) and '推报.py --落' in r \
                        and not re.search(r'success\(\)|env\.GUO', str(s.get('if', ''))):
                    return r
        return None
    a报 = 报步(AJ, ('推报.py --写 ', '--ref', '--sha', '--果', '--印', '--主', '--跑', '--出', '--候', '--判', '--演'))
    if not a报:
        缺.append('⑦报：autopush 须有 if: always()（⛔系於成败）之步：推报.py --写（键俱）而 --落 备份/报')
    y报 = 报步(YJ, ('推报.py --写演', '--名', '--ref', '--sha', '--果', '--印', '--跑', '--出'))
    if not y报:
        缺.append('⑦报：演练 须有 if: always() 之步：推报.py --写演 而 --落 备份/报')
    # ⑧删
    缺 += _验删(_诸步(A), 诸文.get('autopush.yml') or '')
    for 名 in ('gate.yml', '演练.yml'):
        if re.search(r'--delete|":\$N"|push[^\n]*\s["\x27]?:refs/heads/', 诸文.get(名) or ''):
            缺.append('⑧删：%s ⛔删枝' % 名)
    # ⑨绕
    绕 = [x for x in _绕式 if x in 全文]
    if 绕:
        缺.append('⑨⛔绕闸之字：%s' % 绕)
    # ⑫并判：autopush 与 演练 同一 --并果（候）
    for 名, J in (('autopush.yml', AJ), ('演练.yml', YJ)):
        r = '\n'.join(s.get('run') or '' for j in J.values() for s in j.get('steps') or [])
        if not re.search(r'工具/全测\.py --并果 "\$W" --候 "\$CAND" --账 "\$A"', r):
            缺.append('⑫并判：%s 须 全测.py --并果 "$W" --候 "$CAND" --账 "$A"（推闸同策、读器红账）' % 名)
    # ⑬器红账：autopush 读而写回；演练只读
    a跑 = '\n'.join(_跑文(A))
    if not ('报/器红账.json' in a跑 and re.search(r'--账出 "\$RUNNER_TEMP/器红账\.新\.json"', a跑) and re.search(r'cp "\$RUNNER_TEMP/器红账\.新\.json" "\$D/报/器红账\.json"', a跑)):
        缺.append('⑬器红账：autopush 须读 报/器红账.json 入并判（--账）、判毕之新账（--账出）落 备份/报')
    if '--账出' in (诸文.get('演练.yml') or '') or '均秒.新' in (诸文.get('演练.yml') or ''):
        缺.append('⑬器红账：演练⛔写器红账、均秒（只读之）')
    # ⑭演章
    演步 = [s for s in _诸步(A) if "startsWith(github.ref_name, '章-')" in str(s.get('if', '')) and '存底.py --演章' in (s.get('run') or '')]
    if not 演步 or 'always()' not in str(演步[0].get('if', '')) or not (a报 and '--演 "$RUNNER_TEMP/演"' in a报):
        缺.append('⑭演章：章-* 须真克隆其标（存底.py --演章·always）而其判入报（--演）')
    # ⑮演练之触
    yon = Y.get('on') or {}
    yin = ((yon.get('workflow_dispatch') or {}) if isinstance(yon.get('workflow_dispatch'), dict) else {}).get('inputs') or {}
    yp = ((yon.get('push') or {}) if isinstance(yon.get('push'), dict) else {}).get('branches') or []
    if not ({'ref', 'name'} <= set(yin) and yp == [演之前缀 + '*']):
        缺.append('⑮演练：须 workflow_dispatch（inputs ref、name）与 push 於 %s*（推之触⛔待默认枝）' % 演之前缀)
    return 缺 + _验钩(钩)


def 是乙(yml):
    return bool(re.search(r'(?m)^\s+uses:\s*\./\.github/workflows/gate\.yml\s*$', yml or ''))


def 验(yml, 钩, 他=None):
    """静验 → [缺]（空即绿）。乙形（uses gate.yml）照乙之律（他＝{gate.yml, 演练.yml: 文}）；余照甲之律。"""
    if 是乙(yml):
        return 验乙(dict(他 or {}, **{'autopush.yml': yml}), 钩)
    return 验甲(yml, 钩)


def 读流(root=ROOT):
    诸 = {}
    for n in 流之档:
        try:
            诸[n] = open(os.path.join(root, '.github', 'workflows', n), encoding='utf-8').read()
        except OSError:
            诸[n] = ''
    return 诸


def 验诸(诸, 钩):
    """盘上之验（诸＝{档名: 文}）：静验之缺，并⑰——甲形（一 job 串跑）静验虽合，盘上⛔再许（法用之守 废之去证「推报验」同取此一判）。"""
    缺 = 验(诸.get('autopush.yml') or '', 钩, 诸)
    if not 是乙(诸.get('autopush.yml') or ''):
        缺.append('⑰须分片（坑54）：盘上 autopush.yml 须调 gate.yml（甲形之一 job 串跑，闸十余分卡关键路）')
    return 缺


def 验盘(root=ROOT):
    return 验诸(读流(root), open(os.path.join(root, '工具', 'githooks', 'pre-push'), encoding='utf-8').read())


# ═══ 四、演（自测用·桩真跑诸 workflow 於临时之裸库；⛔碰真仓） ═══
_式词 = re.compile(r"\s*(\|\||&&|==|!=|!|\(|\)|,|'(?:[^']|'')*'|-?\d+(?:\.\d+)?|[A-Za-z_][\w-]*(?:\.[\w*-]+)*)")


def _真(v):
    return v not in (None, False, 0, '', 0.0)


def _串(v):
    if v is None:
        return ''
    if v is True or v is False:
        return 'true' if v else 'false'
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


def _同(a, b):
    a, b = ('' if a is None else a), ('' if b is None else b)
    if isinstance(a, str) and isinstance(b, str):
        return a.lower() == b.lower()
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return a == b


def _函(名, 参, 境):
    if 名 == 'always':
        return True
    if 名 == 'success':
        return bool(境.get('_成'))
    if 名 == 'failure':
        return bool(境.get('_败'))
    if 名 == 'cancelled':
        return False
    if 名 == 'startsWith':
        return _串(参[0]).lower().startswith(_串(参[1]).lower())
    if 名 == 'contains':
        return _串(参[1]).lower() in _串(参[0]).lower()
    if 名 == 'fromJSON':
        return json.loads(_串(参[0]))
    raise ValueError('式之函不识：%s' % 名)


def _式(s, 境):
    """GitHub 之式（本仓所用之子集）：字面、境之路、函、! == != && || ()；||／&& 返其项（同 GitHub）。"""
    词, i, s = [], 0, (s or '').strip()
    while i < len(s):
        m = _式词.match(s, i)
        if not m:
            raise ValueError('式不识：%r @%d' % (s, i))
        词.append(m.group(1))
        i = m.end()
        while i < len(s) and s[i] in ' \t\n':
            i += 1
    p = [0]
    看 = lambda: 词[p[0]] if p[0] < len(词) else None

    def 取():
        p[0] += 1
        return 词[p[0] - 1]

    def 或():
        v = 且()
        while 看() == '||':
            取()
            r = 且()
            v = v if _真(v) else r
        return v

    def 且():
        v = 等()
        while 看() == '&&':
            取()
            r = 等()
            v = r if _真(v) else v
        return v

    def 等():
        v = 一()
        while 看() in ('==', '!='):
            op, r = 取(), 一()
            v = _同(v, r) if op == '==' else not _同(v, r)
        return v

    def 一():
        w = 取()
        if w == '!':
            return not _真(一())
        if w == '(':
            v = 或()
            取()
            return v
        if w.startswith("'"):
            return w[1:-1].replace("''", "'")
        if re.fullmatch(r'-?\d+(?:\.\d+)?', w):
            return float(w) if '.' in w else int(w)
        if w in ('true', 'false', 'null'):
            return {'true': True, 'false': False, 'null': None}[w]
        if 看() == '(':
            取()
            参 = []
            while 看() != ')':
                参.append(或())
                if 看() == ',':
                    取()
            取()
            return _函(w, 参, 境)
        v = 境
        for k in w.split('.'):
            v = v.get(k) if isinstance(v, dict) else None
        return v
    v = 或()
    if p[0] != len(词):
        raise ValueError('式有余：%r' % s)
    return v


def _插(v, 境):
    if not isinstance(v, str):
        return v
    m = re.fullmatch(r'\s*\$\{\{(.*?)\}\}\s*', v, re.S)
    if m:
        return _式(m.group(1), 境)
    return re.sub(r'\$\{\{(.*?)\}\}', lambda m: _串(_式(m.group(1), 境)), v)


def _条(条, 境):
    return _真(_式(_式本(条), 境))


def _用(uses, 与, 工, 世, 境):
    名 = uses.split('@')[0]
    if 名 == 'actions/checkout':
        ref = _串(与.get('ref')) or 境['github']['sha']
        滤 = _串(与.get('filter'))
        if 滤 and 世.get('省败'):           # 景「省败」：省取不成（其步 continue-on-error → 次步降级全取）
            if not os.path.isdir(os.path.join(工, '.git')):
                _g(['init', '-q', 工], 世['目'], env=世['gitenv'])
            return False
        if not os.path.isdir(os.path.join(工, '.git')):
            if 滤:                          # 省取（1117·法用#闸取仓之速）：真 partial clone（file:// 方认 filter；裸库 allowfilter）
                _g(['clone', '-q', '--no-checkout', '--filter=' + 滤, 'file://' + 世['裸'], 工], 世['目'], env=世['gitenv'])
            else:
                _g(['clone', '-q', 世['裸'], 工], 世['目'], env=世['gitenv'])
        if re.fullmatch(r'[0-9a-f]{40}', ref):
            _g(['checkout', '-q', '--detach', ref], 工, env=世['gitenv'])
        else:
            _g(['checkout', '-q', '-B', ref, 'refs/remotes/origin/' + ref], 工, env=世['gitenv'])
        return True
    if 名 in ('actions/setup-python', 'actions/setup-node'):
        return True
    if 名 == 'actions/upload-artifact':
        p = _串(与.get('path'))
        if os.path.isdir(p) and os.listdir(p):
            shutil.copytree(p, os.path.join(世['件'], _串(与.get('name'))), dirs_exist_ok=True)
        return True
    if 名 == 'actions/download-artifact':
        p, n = _串(与.get('path')), _串(与.get('name'))
        if n:
            if not os.path.isdir(os.path.join(世['件'], n)):
                return False
            shutil.copytree(os.path.join(世['件'], n), p, dirs_exist_ok=True)
        else:
            for x in os.listdir(世['件']):
                shutil.copytree(os.path.join(世['件'], x), os.path.join(p, x), dirs_exist_ok=True)
        return True
    raise ValueError('演不识之 uses：%s' % uses)


def _跑一job(jid, j, 境, wenv, 世, k):
    根 = tempfile.mkdtemp(dir=世['目'], prefix='job_')
    工, rt = os.path.join(根, '工'), os.path.join(根, 'rt')
    os.makedirs(工)
    os.makedirs(rt)
    genv = os.path.join(rt, '.genv')
    open(genv, 'w').close()
    境 = dict(境, matrix=({'k': k} if k is not None else {}), runner={'temp': rt})
    env = {a: _串(_插(b, 境)) for a, b in (wenv or {}).items()}
    for a, b in (j.get('env') or {}).items():
        env[a] = _串(_插(b, dict(境, env=dict(env))))
    诸步, 成 = {}, True
    gh = 境['github']
    for i, s in enumerate(j.get('steps') or []):
        for l in open(genv, encoding='utf-8').read().split('\n'):
            if '=' in l:
                a, b = l.split('=', 1)
                env[a] = b
        境s = dict(境, steps=诸步, env=dict(env), _成=成, _败=not 成)
        行 = _条(s['if'], 境s) if s.get('if') else 成
        名 = s.get('name') or s.get('uses') or 'run'
        if not 行:
            世['印'].append('· %s/%s：免' % (jid, 名))
            continue
        if s.get('uses'):
            ok = _用(s['uses'], {a: _插(b, 境s) for a, b in (s.get('with') or {}).items()}, 工, 世, 境s)
            if s.get('id'):
                诸步[s['id']] = {'outputs': {}, 'outcome': 'success' if ok else 'failure'}
            世['印'].append('· %s/%s：%s' % (jid, 名, 'ok' if ok else '败'))
        else:
            out = os.path.join(rt, '.out%d' % i)
            open(out, 'w').close()
            sp = os.path.join(rt, '步%d.sh' % i)
            open(sp, 'w', encoding='utf-8').write(s['run'])
            e = dict(世['基env'])
            e.update(env)
            e.update({a: _串(_插(b, 境s)) for a, b in (s.get('env') or {}).items()})
            e.update(GITHUB_ENV=genv, GITHUB_OUTPUT=out, RUNNER_TEMP=rt, GITHUB_SHA=gh['sha'], GITHUB_REF_NAME=gh['ref_name'],
                     GITHUB_REPOSITORY=gh['repository'], GITHUB_SERVER_URL=gh['server_url'], GITHUB_RUN_ID=gh['run_id'],
                     GITHUB_API_URL=gh['api_url'], GITHUB_WORKSPACE=工, GITHUB_EVENT_NAME=gh['event_name'])
            r = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', sp], cwd=工, env=e, capture_output=True, text=True, timeout=600)
            ok = r.returncode == 0
            outs = {}
            for l in open(out, encoding='utf-8').read().split('\n'):
                if '=' in l:
                    a, b = l.split('=', 1)
                    outs[a] = b
            if s.get('id'):
                诸步[s['id']] = {'outputs': outs, 'outcome': 'success' if ok else 'failure'}
            世['印'].append('· %s/%s：rc=%d\n%s%s' % (jid, 名, r.returncode, r.stdout[-1200:], r.stderr[-800:]))
            世['印'] += ['告 %s/%s：%s' % (jid, 名, l) for l in r.stdout.split('\n') if l.startswith('::warning::')]   # 告（降级之印）⛔被截
        成 = 成 and (ok or str(s.get('continue-on-error')).lower() == 'true')     # 步之 continue-on-error（outcome 败而 job 续）
    outs = {a: _串(_插(b, dict(境, steps=诸步, env=env))) for a, b in (j.get('outputs') or {}).items()}
    return {'result': 'success' if 成 else 'failure', 'outputs': outs}


def _跑诸job(w, 诸文, 境基, 世):
    jobs, 果 = _诸job(w), {}
    余 = list(jobs)
    while 余:
        进 = False
        for jid in list(余):
            j = jobs[jid]
            needs = j.get('needs') or []
            needs = [needs] if isinstance(needs, str) else needs
            if any(n not in 果 for n in needs):
                continue
            余.remove(jid)
            进 = True
            境 = dict(境基, needs={n: 果[n] for n in needs}, _成=all(果[n]['result'] == 'success' for n in needs),
                     _败=any(果[n]['result'] == 'failure' for n in needs))
            if not (_条(j['if'], 境) if j.get('if') else 境['_成']):
                果[jid] = {'result': 'skipped', 'outputs': {}}
                世['印'].append('· job %s：免' % jid)
                continue
            if j.get('uses'):
                子 = _yaml(诸文[os.path.basename(str(j['uses']).strip())])
                wc = (子.get('on') or {}).get('workflow_call') or {}
                子in = {a: (b or {}).get('default', '') for a, b in (wc.get('inputs') or {}).items()}
                子in.update({a: _串(_插(b, 境)) for a, b in (j.get('with') or {}).items()})
                子境 = dict(github=境基['github'], inputs=子in, vars={})
                子果 = _跑诸job(子, 诸文, 子境, dict(世, wenv=子.get('env') or {}))
                果[jid] = {'result': 'failure' if any(x['result'] == 'failure' for x in 子果.values()) else 'success',
                          'outputs': {a: _串(_插((b or {}).get('value', ''), dict(子境, jobs=子果))) for a, b in (wc.get('outputs') or {}).items()}}
                continue
            mk = ((j.get('strategy') or {}).get('matrix') or {}).get('k')
            诸k = [None]
            if mk is not None:
                v = _插(mk, 境)
                诸k = json.loads(v) if isinstance(v, str) else list(v)
            结 = [_跑一job(jid, j, 境, 世['wenv'], 世, k) for k in 诸k]
            果[jid] = {'result': 'failure' if any(x['result'] == 'failure' for x in 结) else 'success', 'outputs': 结[-1]['outputs']}
        if not 进:
            raise RuntimeError('needs 成环或缺：%s' % 余)
    return 果


def 跑流(诸文, 档, 事, 裸, 目, 基env, 省败=False):
    """以桩真跑一 workflow（事：{event_name, ref_name, sha, inputs}）→ (诸 job 之果, 印)。省败：带 filter 之 checkout 俱败（降级之演）。"""
    w = _yaml(诸文[档])
    on = w.get('on') or {}
    inputs = {}
    if 事['event_name'] == 'workflow_dispatch':
        inputs = {a: (b or {}).get('default', '') for a, b in (((on.get('workflow_dispatch') or {}).get('inputs')) or {}).items()}
        inputs.update(事.get('inputs') or {})
    gh = {'ref_name': 事['ref_name'], 'sha': 事['sha'], 'event_name': 事['event_name'], 'token': 'tok', 'run_id': '1',
          'repository': '演/仓', 'server_url': 'file://' + 目, 'api_url': 'http://api.invalid'}
    件 = tempfile.mkdtemp(dir=目, prefix='件_')
    世 = {'目': 目, '裸': 裸, '件': 件, '印': [], '基env': 基env, 'gitenv': _净env(), 'wenv': w.get('env') or {}, '省败': 省败}
    果 = _跑诸job(w, 诸文, {'github': gh, 'inputs': inputs, 'vars': {}}, 世)
    return 果, '\n'.join(世['印'])


_桩全测 = r'''#!/usr/bin/env python3
# 桩之全测（推报·自测）：载真 全测（_真全测.py）而以桩格代其诸项——--片数、--片、--并果 之真码照跑。
#   ZM_STUB：绿｜红（字数闸·读者可见）｜器红（桩器乙）；ZM_STUB_CNT 记每格之跑；ZM_STUB_MOVE=<他之克隆>：首格之中把他之主枝推上（一回）；
#   ZM_STUB_CRASH=k：第 k 片未跑即崩（⛔落果）。ZM_STUB_LAN=k：第 k 片於省取之仓（promisor）懒取一回而败（形同 git 之 promisor fetch），
#   其片诸格随之红（降级全取而重跑即绿——法用#闸取仓之速）。
import os, sys, importlib.util, subprocess
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
sp = importlib.util.spec_from_file_location('全测', os.path.join(H, '_真全测.py'))
m = importlib.util.module_from_spec(sp)
sys.modules['全测'] = m
sp.loader.exec_module(m)
红 = {'红': {'字数闸', '桩器乙'}, '器红': {'桩器乙'}}.get(os.environ.get('ZM_STUB', '绿'), set())
名们 = ['字数闸', '全书检'] + ['桩器' + x for x in '甲乙丙丁戊'] + ['桩格%02d' % i for i in range(40)]


def 格(名):
    def f():
        计 = os.environ.get('ZM_STUB_CNT')
        if 计:
            open(计, 'a', encoding='utf-8').write(名 + '\n')
        他 = os.environ.get('ZM_STUB_MOVE')
        if 他 and 名 == '桩格00' and not os.path.exists(他 + '.已'):
            open(他 + '.已', 'w').close()
            e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_') or k.startswith('GIT_CONFIG')}
            subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:refs/heads/' + os.environ['ZM_STUB_MAIN']], cwd=他, env=e, capture_output=True)
        return (名 not in 红, '桩' + ('坏' if 名 in 红 else 'ok'))
    return f


m.诸项 = lambda quick: [(n, 格(n)) for n in 名们]
m._留字快照 = lambda: {}
崩 = os.environ.get('ZM_STUB_CRASH')
if 崩 and '--片' in sys.argv and sys.argv[sys.argv.index('--片') + 1].startswith(崩 + '/'):
    sys.exit(3)
懒 = os.environ.get('ZM_STUB_LAN')
if 懒 and '--片' in sys.argv and sys.argv[sys.argv.index('--片') + 1].startswith(懒 + '/') \
        and subprocess.run(['git', 'config', '--get', 'remote.origin.promisor'], capture_output=True, text=True).stdout.strip() == 'true':
    subprocess.run(['git', '-c', 'fetch.negotiationAlgorithm=noop', 'fetch', 'origin', '--no-tags', '--no-write-fetch-head',
                    '--recurse-submodules=no', '--filter=blob:none', '--stdin'], input='0' * 40 + '\n', text=True, capture_output=True,
                   env=dict(os.environ, GIT_ALLOW_PROTOCOL='none'))
    红 = set(名们)
sys.exit(m.main())
'''
_桩名数 = 47


def _净env(**加):
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
             GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
    e.update(加)
    return e


def _g(a, cwd, env=None, 必=True):
    r = subprocess.run(['git', '-c', 'core.quotepath=off'] + a, cwd=cwd, capture_output=True, text=True, env=env or _净env(), timeout=120)
    if 必 and r.returncode != 0:
        raise RuntimeError('git %s：%s' % (' '.join(a[:3]), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout.strip()


def 演乙(诸文, 钩, 景, 目):
    """以桩真跑乙形诸 workflow 於 目 下之裸库。景：
    成｜器红｜红｜逾（器红账首见已逾）｜拒（改 workflows）｜片崩｜章（章-9 触·演章）｜主动（闸中他坐推进主枝 → 重派 → 续跑而成）｜
    重派尽（tries 2 而主动）｜中已在（闸中他坐以他并含本枝）｜演（演练·派：改 workflows 之枝照演）｜演红｜演推（演练·推 备份/演/<名>）｜
    省败（带 filter 之省取俱败 → 降级全取）｜懒败（片一於省取之仓懒取而败、其格俱红 → 降级全取重跑）——法用#闸取仓之速。
    → {果, 报, 演报, 器红账, 计, 主, T, R, 枝们, 派, 印, 二, 沙, 他sha}"""
    import importlib
    env0 = _净env()
    裸 = os.path.join(目, '演', '仓.git')
    种, 沙, 他, 桩bin = (os.path.join(目, x) for x in ('种', '沙', '他', 'bin'))
    os.makedirs(os.path.dirname(裸))
    _g(['init', '-q', '--bare', 裸], 目)
    _g(['config', 'uploadpack.allowfilter', 'true'], 裸)          # 省取（partial clone）之演：file:// 之裸库许 filter
    _g(['init', '-q', '-b', 主枝, 种], 目)
    工具 = os.path.dirname(os.path.abspath(__file__))
    档们 = {'工具/githooks/pre-push': 钩, '工具/全测.py': _桩全测, '设定/全测均秒.json': '{}\n',
           '正文/第四百二十章.md': '一\n', 'a.txt': '甲\n', 'b.txt': '乙\n'}
    for n in ('全测并.py', '推报.py', '存底.py'):
        档们['工具/' + n] = open(os.path.join(工具, n), encoding='utf-8').read()
    档们['工具/_真全测.py'] = open(os.path.join(工具, '全测.py'), encoding='utf-8').read()
    for n, t in 诸文.items():
        档们['.github/workflows/' + n] = t
    for p, t in 档们.items():
        f = os.path.join(种, p)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w', encoding='utf-8').write(t)
    os.chmod(os.path.join(种, '工具/githooks/pre-push'), 0o755)
    for d in ('设定', '版本'):
        os.makedirs(os.path.join(种, d), exist_ok=True)
    _g(['add', '-A'], 种)
    _g(['commit', '-q', '-m', '种'], 种)
    _g(['push', '-q', 裸, 'HEAD:refs/heads/' + 主枝], 种)
    _g(['clone', '-q', '-b', 主枝, 裸, 沙], 目)
    if 景 in ('拒', '演'):
        open(os.path.join(沙, '.github', 'workflows', 'autopush.yml'), 'a', encoding='utf-8').write('# 改\n')
    else:
        open(os.path.join(沙, 'a.txt'), 'a', encoding='utf-8').write('甲之治\n')
    _g(['commit', '-qam', '治'], 沙)
    T = _g(['rev-parse', 'HEAD'], 沙)
    R = {'章': '章-9', '演推': 演之前缀 + '试一'}.get(景, '治-' + T[:12])
    _g(['push', '-q', 'origin', 'HEAD:refs/heads/' + R], 沙)
    _g(['clone', '-q', '-b', 主枝, 裸, 他], 目)
    open(os.path.join(他, 'b.txt'), 'a', encoding='utf-8').write('乙之进\n')
    _g(['commit', '-qam', '他坐先进'], 他)
    _g(['push', '-q', 'origin', 'HEAD:refs/heads/' + 主枝], 他)          # 主枝先进一笔：候係真并（⛔快进）
    他sha = ''
    if 景 in ('主动', '重派尽'):
        open(os.path.join(他, 'b.txt'), 'a', encoding='utf-8').write('乙之再进\n')
        _g(['commit', '-qam', '他坐闸中再进'], 他)
        他sha = _g(['rev-parse', 'HEAD'], 他)
    if 景 == '中已在':
        _g(['fetch', '-q', 'origin', R], 他)
        _g(['merge', '-q', '--no-ff', '-m', '他坐直并本枝', 'FETCH_HEAD'], 他)
        他sha = _g(['rev-parse', 'HEAD'], 他)
    if 景 == '逾':
        报 = os.path.join(目, '报种')
        _g(['init', '-q', 报], 目)
        os.makedirs(os.path.join(报, '报'))
        json.dump({'桩器乙': {'首见': 410, '末见': 416, '限': 413}}, open(os.path.join(报, '报', '器红账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        _g(['add', '-A'], 报)
        _g(['commit', '-q', '-m', '报种'], 报)
        _g(['push', '-q', 裸, 'HEAD:refs/heads/' + 报枝], 报)
    os.makedirs(桩bin)
    派档 = os.path.join(目, '派')
    open(os.path.join(桩bin, 'curl'), 'w').write('#!/bin/sh\nprintf "%%s\\n" "$*" >> "%s"\nexit 0\n' % 派档)
    os.chmod(os.path.join(桩bin, 'curl'), 0o755)
    计 = os.path.join(目, '闸计')
    基 = dict(env0, PATH=桩bin + os.pathsep + env0.get('PATH', ''), ZM_STUB_CNT=计, ZM_STUB_MAIN=主枝,
             ZM_STUB={'红': '红', '演红': '红', '器红': '器红', '逾': '器红'}.get(景, '绿'))
    for k in ('GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL'):
        基.pop(k, None)                                  # 机之身由 yml 之 git config 定（⛔借测者之身）
    if 他sha:
        基['ZM_STUB_MOVE'] = 他
    if 景 == '片崩':
        基['ZM_STUB_CRASH'] = '2'
    if 景 == '懒败':
        基['ZM_STUB_LAN'] = '1'
    if 景 in ('演', '演红'):
        事 = {'event_name': 'workflow_dispatch', 'ref_name': 主枝, 'sha': '', 'inputs': {'ref': R, 'name': '试一'}}
        档 = '演练.yml'
    elif 景 == '演推':
        事, 档 = {'event_name': 'push', 'ref_name': R, 'sha': T}, '演练.yml'
    elif 景 == '重派尽':
        事, 档 = {'event_name': 'workflow_dispatch', 'ref_name': R, 'sha': T, 'inputs': {'tries': '2'}}, 'autopush.yml'
    else:
        事, 档 = {'event_name': 'push', 'ref_name': R, 'sha': T}, 'autopush.yml'
    if 档 == '演练.yml' and not 事['sha']:
        事['sha'] = _g(['rev-parse', 'refs/heads/' + 主枝], 裸)
    果, 印 = 跑流(诸文, 档, 事, 裸, 目, 基, 省败=(景 == '省败'))
    二 = None
    if 景 == '主动':
        计一 = open(计, encoding='utf-8').read() if os.path.exists(计) else ''
        os.remove(计)
        二 = {'报一': json.loads(_g(['show', 'refs/heads/%s:%s' % (报枝, 报径(R))], 裸, 必=False) or 'null'), '计一': 计一}
        事 = {'event_name': 'workflow_dispatch', 'ref_name': R, 'sha': T, 'inputs': {'tries': '1'}}
        果2, 印2 = 跑流(诸文, 'autopush.yml', 事, 裸, 目, 基)
        印 += '\n══ 重派之跑 ══\n' + 印2
    主 = _g(['rev-parse', 'refs/heads/' + 主枝], 裸)
    枝们 = [x.split('refs/heads/', 1)[1] for x in _g(['for-each-ref', '--format=%(refname)', 'refs/heads/'], 裸).split('\n') if x]
    读 = lambda p: (json.loads(_g(['show', 'refs/heads/%s:%s' % (报枝, p)], 裸, 必=False) or 'null')
                   if subprocess.run(['git', 'cat-file', '-e', 'refs/heads/%s:%s' % (报枝, p)], cwd=裸, env=env0, capture_output=True).returncode == 0 else None)
    in主 = lambda x: bool(x) and subprocess.run(['git', 'merge-base', '--is-ancestor', x, 主], cwd=裸, env=env0, capture_output=True).returncode == 0
    return {'果': 果, '报': 读(报径(R)), '演报': 读(演径('试一')), '器红账': 读('报/器红账.json'), '均秒': 读('报/均秒.json'),
            '计': open(计, encoding='utf-8').read().split() if os.path.exists(计) else [], '主': 主, 'T': T, 'R': R, '枝们': 枝们,
            'T在主': in主(T), '他在主': in主(他sha), '派': open(派档, encoding='utf-8').read() if os.path.exists(派档) else '',
            '印': 印, '二': 二, '沙': 沙}


def 演钩(钩, 目):
    """钩之 stdin 诸形真跑（桩之全测并计次）。→ {形: (rc, 闸否, 推闸之果)}"""
    _g(['init', '-q', '-b', 主枝, 目], os.path.dirname(目))
    os.makedirs(os.path.join(目, '工具', 'githooks'))
    open(os.path.join(目, '工具', 'githooks', 'pre-push'), 'w', encoding='utf-8').write(钩)
    os.chmod(os.path.join(目, '工具', 'githooks', 'pre-push'), 0o755)
    open(os.path.join(目, '工具', '全测并.py'), 'w', encoding='utf-8').write(_桩并)
    计 = os.path.join(目, '..', '钩计')
    z, s = '0' * 40, 'a' * 40
    形 = {'治': 'HEAD %s refs/heads/治-abc %s\n' % (s, z), '章': 'HEAD %s refs/heads/章-411 %s\n' % (s, z),
         '备份': 'HEAD %s refs/heads/备份/报 %s\n' % (s, z), '演推': 'HEAD %s refs/heads/备份/演/试 %s\n' % (s, z),
         '主': 'HEAD %s refs/heads/%s %s\n' % (s, 主枝, z),
         '主＋治': 'HEAD %s refs/heads/%s %s\nHEAD %s refs/heads/治-abc %s\n' % (s, 主枝, z, s, z),
         '删治': '(delete) %s refs/heads/治-abc %s\n' % (z, s), '删主': '(delete) %s refs/heads/%s %s\n' % (z, 主枝, s),
         '空': '', '章外': 'HEAD %s refs/heads/章外 %s\n' % (s, z)}
    出 = {}
    for 名, 入 in list(形.items()) + [('手跑', None)]:
        if os.path.exists(计):
            os.remove(计)
        果档 = os.path.join(目, '.git', '推闸之果')
        if os.path.exists(果档):
            os.remove(果档)
        a = ['sh', os.path.join('工具', 'githooks', 'pre-push')] + ([] if 名 == '手跑' else ['origin', 'https://x/y.git'])
        r = subprocess.run(a, cwd=目, input=入 or '', capture_output=True, text=True, env=_净env(ZM_STUB_CNT=计, ZM_STUB='绿'), timeout=60)
        出[名] = (r.returncode, os.path.exists(计), open(果档).read().strip() if os.path.exists(果档) else '')
    r = subprocess.run(['sh', os.path.join('工具', 'githooks', 'pre-push'), 'origin', 'u'], cwd=目, input=形['主'], capture_output=True,
                       text=True, env=_净env(ZM_STUB_CNT=计, ZM_STUB='红'), timeout=60)
    果档 = os.path.join(目, '.git', '推闸之果')
    出['主·红'] = (r.returncode, True, open(果档).read().strip() if os.path.exists(果档) else '')
    return 出


_桩并 = r'''#!/usr/bin/env python3
# 桩之全测并（推报·自测·钩之真跑）：计次；ZM_STUB=红 即印 ✗ 而 rc=1
import os, sys
计 = os.environ.get('ZM_STUB_CNT')
if 计:
    open(计, 'a').write('闸\n')
print('  ✓ 桩项甲        ok')
if os.environ.get('ZM_STUB') == '红':
    print('  ✗ 桩项乙        坏了一处'); print('\n  ⛔全测未过：桩项乙'); sys.exit(1)
print('\n  ✓全测通过（并）。')
'''


def _对yaml(a, b):
    """本器之析与 PyYAML 同否（PyYAML 之标量化为字串、on 之键作 True）。"""
    def 平(x):
        if isinstance(x, dict):
            return {('on' if k is True else str(k)): 平(v) for k, v in x.items()}
        if isinstance(x, list):
            return [平(v) for v in x]
        if x is None:
            return None
        return _串(x)
    return 平(a) == 平(b)


def 自测():
    R = []

    def T(名, 条):
        R.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    # ①析与写
    印 = ('── 第 1 试 ──\n  ✓ 甲  ok\n  ✗ 负测·乙   坏\n  ✗ 质量三闸  红一处\n\n  ⛔全测未过：负测·乙、质量三闸\n'
         '  ✓推闸·分等：放行——只器之红 2（负测·丙、跑账），只报不拦\n⛔ 全测未过,推送已拦停。\nerror: failed to push some refs\n'
         '  ⛔推闸·器红逾限：跑账（首见第410章、限第413章）——到期\n  ⛔片闸·败：片缺或重\n')
    T('①析红：✗ 之行、全测总红之行、⛔推闸／⛔片闸 之行（去重存序）', 红行(印) == ['✗ 负测·乙   坏', '✗ 质量三闸  红一处', '⛔全测未过：负测·乙、质量三闸',
                                                         '⛔推闸·器红逾限：跑账（首见第410章、限第413章）——到期', '⛔片闸·败：片缺或重'])
    T('①之二 器红：取推闸·分等之名；判档给出即取判之器红、逾', 器红(印) == ['负测·丙', '跑账']
      and 成报('a', 'b', '成', 印, 判={'器红': ['x'], '逾': ['y'], '片秒': {'1': 9}})['器红'] == ['x']
      and 成报('a', 'b', '红', 印, 判={'逾': ['y'], '片秒': {'1': 9, '2': 8}})['片'] == {'数': 2, '秒': {'1': 9, '2': 8}})
    d = 成报('治-abc', 'f' * 40, '红', 印, 主='e' * 40, 跑='https://x/runs/1', 时='2026-10-27T00:00:00Z', 候='c' * 40, 演={'果': '过', '语': '✓'})
    T('①之三 报之键俱在（ref、sha、果、红、main_after、时、run_url，并 候、演）', all(k in d for k in ('ref', 'sha', '果', '红', 'main_after', '时', 'run_url', '候', '演'))
      and d['果'] == '红' and len(d['红']) == 5)
    T('①之四 成、已在⛔带红；拒败无 ✗ 者取其由；果不在五者即败',
      成报('a', 'b', '成', 印)['红'] == [] and 成报('a', 'b', '拒', '⛔拒：改 workflows\n')['红'] == ['⛔拒：改 workflows']
      and 成报('a', 'b', '怪', '')['果'] == '败')
    with tempfile.TemporaryDirectory() as t:
        j, x = 写(d, '\n'.join('行%d' % i for i in range(200)), t)
        e = 成演报(演之前缀 + '甲/乙', 'zx/B', 'f' * 40, '红', '⛔片闸·败：片缺\n', 跑='u', 因='片')
        jy = 写演(e, '印', t)
        open(os.path.join(t, '演'), 'w', encoding='utf-8').write('· 克隆中\n⛔演不过：章标 章-9 里缺 工具\n')
        T('①之五 写：报/推/<枝>.json 可解回、txt 存末八十行；演报 报/演/<名>.json（名去前缀、斜作横）；演章之印取其末判',
          json.load(open(j, encoding='utf-8')) == d and open(x, encoding='utf-8').read().split('\n')[0] == '行120'
          and j.endswith(os.path.join('报', '推', '治-abc.json')) and jy.endswith(os.path.join('报', '演', '甲-乙.json'))
          and json.load(open(jy, encoding='utf-8'))['果'] == '红' and json.load(open(jy, encoding='utf-8'))['红'] == ['⛔片闸·败：片缺']
          and _读演之印(os.path.join(t, '演')) == {'果': '红', '语': '⛔演不过：章标 章-9 里缺 工具'} and _读演之印(os.path.join(t, '无')) is None)
    T('①之六 坏：红／拒／败坏；败·重派係在飞⛔坏', 坏({'果': '红'}) and 坏({'果': '败', '因': 'non-ff'}) and not 坏({'果': '败', '因': '重派'})
      and not 坏({'果': '成'}) and not 坏(None))
    源们 = {n: open(os.path.join(ROOT, '工具', n), encoding='utf-8').read() for n in ('接棒守.py', '推.py')}
    T('①之七 候者（接棒守 --候主、推.py --候）以 推报.坏 判坏报（败·重派 係在飞、⛔早返）——⛔以 推报.坏果 直判',
      all('推报.坏(' in s and '推报.坏果' not in s for s in 源们.values()))
    # ②验：今盘（乙）绿；PyYAML 与本器之析同；旧 yml 回灌红；甲形（97286329）照甲律为合而盘上须乙；诸改坏各红
    诸 = 读流(ROOT)
    钩 = open(os.path.join(ROOT, '工具', 'githooks', 'pre-push'), encoding='utf-8').read()
    今缺 = 验盘(ROOT)
    T('②今盘 autopush／gate／演练 与 pre-push 之形俱合（乙形）%s' % ('' if not 今缺 else '：' + '；'.join(今缺)), not 今缺)
    try:
        import yaml as _y
        同 = all(_对yaml(_y.safe_load(诸[n]), _yaml(诸[n])) for n in 流之档)
        T('②之二 PyYAML 可解三档，且与本器之析全同（片之机无 PyYAML，本器自析）', 同)
    except ImportError:
        T('②之二 无 PyYAML——本器自析', all(_yaml(诸[n]) for n in 流之档))
    旧 = subprocess.run(['git', 'show', '%s:.github/workflows/autopush.yml' % 旧yml之笔], cwd=ROOT, capture_output=True, text=True).stdout
    旧缺 = 验(旧, 钩) if 旧 else []
    T('②之三 旧 yml（%s·坑51 之形）回灌须红：一闸二跑、无取再试、无报、无治（%d 缺）' % (旧yml之笔, len(旧缺)),
      bool(旧) and any(x.startswith('③') for x in 旧缺) and any(x.startswith('⑦') for x in 旧缺) and any(x.startswith('①') for x in 旧缺)
      and any(x.startswith('④') for x in 旧缺))
    单 = subprocess.run(['git', 'show', '%s:.github/workflows/autopush.yml' % 单闸yml之笔], cwd=ROOT, capture_output=True, text=True).stdout
    T('②之四 甲形（%s·一 job 推时之钩即闸）照甲律判合；而作盘上之档须红（⑰须分片）' % 单闸yml之笔,
      bool(单) and not 是乙(单) and 验(单, 钩) == [] and 验乙(dict(诸, **{'autopush.yml': 单}), 钩) != [])
    a, g, y = 诸['autopush.yml'], 诸['gate.yml'], 诸['演练.yml']
    坏形 = {
        '再添直跑 pre-push 一步': ('autopush.yml', a.replace('      - name: 删已并之治枝', '      - name: 推闸\n        run: bash 工具/githooks/pre-push\n      - name: 删已并之治枝')),
        '片中跑全测并': ('gate.yml', g.replace('python3 工具/全测.py --片 "$K/$N"', 'python3 工具/全测并.py; python3 工具/全测.py --片 "$K/$N"')),
        '末 job 再全跑全测': ('autopush.yml', a.replace('            rc=$?\n', '            rc=$?\n            python3 工具/全测.py >> "$O"\n', 1)),
        '推主枝不指空钩（钩再闸）': ('autopush.yml', a.replace('git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$CAND', 'git push origin "$CAND')),
        '推主枝⛔推候（另并之树）': ('autopush.yml', a.replace('push origin "$CAND:refs/heads/$MAIN"', 'push origin "HEAD:refs/heads/$MAIN"')),
        '推前⛔并判': ('autopush.yml', a.replace('python3 工具/全测.py --并果 "$W" --候 "$CAND"', 'python3 工具/全测.py --并果 "$W" --候 "$X"')),
        '推後⛔验含候': ('autopush.yml', a.replace('git merge-base --is-ancestor "$CAND" "origin/$MAIN"', 'true')),
        '重派无界': ('autopush.yml', a.replace('"${TRIES:-0}" -lt 2', '"${TRIES:-0}" -lt 9')),
        '⛔重派': ('autopush.yml', a.replace('/actions/workflows/autopush.yml/dispatches', '/x')),
        '去 治-* 之触': ('autopush.yml', a.replace("branches: ['章-*', '治-*']", "branches: ['章-*']")),
        '报⛔always': ('autopush.yml', a.replace("      - name: 报（备份/报·报/推/<枝>.json 与 .txt；器红账、均秒）\n        if: always()\n",
                                                "      - name: 报（备份/报·报/推/<枝>.json 与 .txt；器红账、均秒）\n        if: success()\n")),
        '删及章标': ('autopush.yml', a.replace("refs/heads/治-*) git merge-base", "refs/heads/治-*|refs/heads/章-*) git merge-base").replace(
            "'refs/heads/治-*')", "'refs/heads/治-*' 'refs/heads/章-*')")),
        '删治不问已并': ('autopush.yml', a.replace('refs/heads/治-*) git merge-base --is-ancestor "$S" "origin/$MAIN" && D+=(":$N") ;;', 'refs/heads/治-*) D+=(":$N") ;;')),
        '⛔先判拒': ('gate.yml', g.replace('HEAD -- .github/workflows)" ]', 'HEAD -- .github/xx)" ]')),
        '⛔先判已在': ('gate.yml', g.replace('[ "$MODE" = 推 ] && git merge-base --is-ancestor "$T" "origin/$MAIN"', 'false')),
        '片一红消他片': ('gate.yml', g.replace('fail-fast: false', 'fail-fast: true')),
        '片红败及闸': ('gate.yml', g.replace('    continue-on-error: true\n', '')),
        '片⛔验其树即候': ('gate.yml', g.replace('if [ "$(git rev-parse HEAD)" != "$CAND" ]', 'if false')),
        '片果⛔always 上件': ('gate.yml', g.replace("      - uses: actions/upload-artifact@v4\n        if: always()\n        with:\n          name: shard-",
                                                   "      - uses: actions/upload-artifact@v4\n        with:\n          name: shard-")),
        'gate 可写': ('gate.yml', g.replace('permissions:\n  contents: read', 'permissions:\n  contents: write')),
        '二处 --片（一树二闸）': ('gate.yml', g.replace('python3 工具/全测.py --片 "$K/$N"', 'python3 工具/全测.py --片 "$K/$N" --出 x; python3 工具/全测.py --片 "$K/$N"')),
        '器红账⛔落': ('autopush.yml', a.replace('cp "$RUNNER_TEMP/器红账.新.json" "$D/报/器红账.json"', 'true')),
        '⛔演章': ('autopush.yml', a.replace('存底.py --演章', '存底.py --演')),
        '演练推主枝': ('演练.yml', y.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$CAND:refs/heads/$MAIN"\n          python3 工具/推报.py --落 "$D"')),
        '演练写器红账': ('演练.yml', y.replace('--账 "$A" --判', '--账 "$A" --账出 "$A" --判')),
        '演练删枝': ('演练.yml', y.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin ":refs/heads/$REF"\n          python3 工具/推报.py --落 "$D"')),
        '演练⛔推之触': ('演练.yml', y.replace("    branches: ['备份/演/*']\n", "    branches: ['演/*']\n")),
        '绕钩之字': ('gate.yml', g.replace('git config core.hooksPath 工具/githooks', 'export ZM_SKIP_HOOK=1')),
        '省取⛔降级（检出不成即红）': ('gate.yml', g.replace(' || quan_qu "$WANT" "检出不成：$QU"', '')),
        '省取之检出⛔continue-on-error': ('gate.yml', g.replace('        id: qu\n        continue-on-error: true\n', '        id: qu\n')),
        '片⛔计懒取之败': ('gate.yml', g.replace('quan_qu "$WANT" "片中懒取败 $BAI 回"', 'true')),
        '全取⛔再试': ('gate.yml', g.replace("&& zai_shi git -c protocol.version=2 fetch -q --prune", "&& git -c protocol.version=2 fetch -q --prune")),
        '全取再试⛔候': ('gate.yml', g.replace('        sleep "$s"\n', '')),
        '全取再试二回': ('gate.yml', g.replace('for n in 1 2 3; do', 'for n in 1 2; do')),
        '专取 sha ⛔再试': ('gate.yml', g.replace('|| zai_shi git -c protocol.version=2 fetch -q --no-tags', '|| git -c protocol.version=2 fetch -q --no-tags')),
        # B-v 驳：推主枝之短式（"$CAND:$MAIN"、${MAIN}、推本地同名之枝）旧式俱漏
        '演练推主枝·短式': ('演练.yml', y.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$CAND:$MAIN"\n          python3 工具/推报.py --落 "$D"')),
        '演练推主枝·${MAIN}': ('演练.yml', y.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$CAND:refs/heads/${MAIN}"\n          python3 工具/推报.py --落 "$D"')),
        '演练推同名之枝': ('演练.yml', y.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$MAIN"\n          python3 工具/推报.py --落 "$D"')),
        'autopush 二推主枝·短式': ('autopush.yml', a.replace('          python3 工具/推报.py --落 "$D"', '          git -c core.hooksPath="$RUNNER_TEMP/无钩" push origin "$GITHUB_SHA:$MAIN"\n          python3 工具/推报.py --落 "$D"')),
    }
    错 = [k for k, (n, v) in 坏形.items() if v == 诸[n] or not 验乙(dict(诸, **{n: v}), 钩)]
    T('②之五 乙形诸改坏（%d 形）各红%s' % (len(坏形), ('：未红 ' + '、'.join(错)) if 错 else ''), not 错)
    坏钩 = {'免及主枝': 钩.replace('refs/heads/章-*|refs/heads/治-*|refs/heads/备份/*)', 'refs/heads/*)'),
          '旧钩（⛔读 stdin）': subprocess.run(['git', 'show', '%s:工具/githooks/pre-push' % 旧yml之笔], cwd=ROOT, capture_output=True, text=True).stdout,
          '有一即免': 钩.replace('"$N_ALL" -eq "$N_STAGE"', '"$N_STAGE" -ge 1')}
    T('②之六 钩之改坏（免及主枝、旧钩、有一暂存即免）各红', all(验(a, v, 诸) for v in 坏钩.values()))
    # ③钩之 stdin 诸形真跑
    with tempfile.TemporaryDirectory() as t:
        o = 演钩(钩, os.path.join(t, '钩'))
    T('③钩：治／章／备份（含 备份/演/*）only → 免闸 rc=0', all(o[k][:2] == (0, False) for k in ('治', '章', '备份', '演推')))
    T('③之二 主枝 only、主枝＋治、删主、章外（前缀之外）→ 照闸（绿 rc=0、落「绿」）',
      all(o[k] == (0, True, '绿') for k in ('主', '主＋治', '删主', '章外')))
    T('③之三 删治 → 免；git 所喂空 → 免；手跑（无参）→ 照闸', o['删治'][:2] == (0, False) and o['空'][:2] == (0, False)
      and o['手跑'] == (0, True, '绿'))
    T('③之四 主枝而闸红 → rc=1、落「红」', o['主·红'] == (1, True, '红'))
    # ④乙形诸 workflow 之真跑（桩之全测载真 全测、全测并、推报、存底；裸库）
    import concurrent.futures as _cf
    景们 = ('成', '器红', '红', '逾', '拒', '片崩', '章', '主动', '重派尽', '中已在', '演', '演红', '演推', '省败', '懒败')

    def 演一(景):
        t = tempfile.mkdtemp(prefix='推报演_')
        try:
            r = 演乙(诸, 钩, 景, t)
            if 景 in ('成', '演'):           # 沙盒之读（推.py --候、接棒守 --候主、法用之守 之 报之读／演录）：读、诸报（一取）、快进——⛔另造一把尺
                r['诸'] = 诸报(r['沙'], 取=True)
                if 景 == '成':
                    r['读'] = 读(r['R'], r['沙'], 取=False)
                    r['快进'] = 快进(r['沙'])
                    r['沙主'] = _git(['rev-parse', 'HEAD'], r['沙']).stdout.strip()
            return 景, r
        except Exception as e:
            return 景, {'崩': '%s：%s' % (type(e).__name__, e), '印': ''}
        finally:
            shutil.rmtree(t, ignore_errors=True)
    with _cf.ThreadPoolExecutor(max_workers=min(8, len(景们))) as ex:
        演 = dict(ex.map(演一, 景们))

    def 报合(e, 果):
        b = e.get('报') or {}
        return b.get('果') == 果 and b.get('ref') == e.get('R') and b.get('sha') == e.get('T') and b.get('main_after') == e.get('主') \
            and b.get('run_url', '').endswith('/演/仓/actions/runs/1') and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', b.get('时', ''))

    def 恰一(e):
        return sorted(e.get('计') or []) == sorted(set(e.get('计') or [])) and len(e.get('计') or []) == _桩名数

    def 示(e):
        return '' if not e.get('崩') else '：' + e['崩']
    e = 演['成']
    T('④成：闸恰一（每格恰跑一回）、主枝即候且含本枝、治枝已删、报「成」（候、片之数、键俱）、均秒落 备份/报%s' % 示(e),
      恰一(e) and e['T在主'] and e['R'] not in e['枝们'] and 报合(e, '成') and (e['报'].get('片') or {}).get('数') in (3, 4)
      and e['报'].get('候') == e['主'] and isinstance(e.get('均秒'), dict) and len(e['均秒']) == _桩名数)
    e = 演['器红']
    T('④之二 只器之红 → 成、报带器红、器红账落 备份/报（首见 末见 420、限 423）%s' % 示(e), 报合(e, '成') and e['报'].get('器红') == ['桩器乙']
      and (e.get('器红账') or {}).get('桩器乙') == {'首见': 420, '末见': 420, '限': 423})
    e = 演['成']
    T('④之一b 沙盒 读(枝) 得其报、快进到并後之主枝（候≠本枝）%s' % 示(e), (e.get('读') or {}).get('果') == '成' and (e.get('快进') or (False,))[0]
      and e.get('沙主') == e.get('主') != e.get('T'))
    _诸 = e.get('诸') or []
    T('④之一c 诸报（一取·cat-file 一批）：得 报/推/<枝>.json 之全、带路与类；无 报/演 之目即只推%s' % 示(e), len(_诸) == 1
      and _诸[0].get('路') == 报径(e.get('R', '')) and _诸[0].get('类') == '推' and _诸[0].get('果') == '成'
      and not [d for d in _诸 if d.get('类') == '演'])
    _诸 = 演['演'].get('诸') or []
    T('④之一d 诸报 读 报/演：演练之录带路与类（法用之守·演录之源）', [(d.get('路'), d.get('类'), d.get('果')) for d in _诸]
      == [(演径('试一'), '演', '过')])
    e = 演['红']
    T('④之三 读者可见之红 → 主枝不动、治枝留、报「红」带 ✗ 之行与全测总红之行%s' % 示(e), 恰一(e) and not e['T在主'] and e['R'] in e['枝们']
      and 报合(e, '红') and any('✗' in x and '字数闸' in x for x in e['报']['红']) and any(x.startswith('⛔全测未过：') for x in e['报']['红']))
    e = 演['逾']
    T('④之四 器红逾限（云端器红账首见 410、今 420）→ 红、报带「⛔推闸·器红逾限」、主枝不动%s' % 示(e), 报合(e, '红') and not e['T在主']
      and e['报'].get('逾') == ['桩器乙'] and any(x.startswith('⛔推闸·器红逾限') for x in e['报']['红']))
    e = 演['拒']
    T('④之五 拒：改 workflows 者⛔闸、主枝不动、报「拒」因 workflow%s' % 示(e), not e.get('计') and not e['T在主'] and 报合(e, '拒')
      and e['报'].get('因') == 'workflow')
    e = 演['片崩']
    T('④之六 一片崩（⛔落果）→ 败（因 片）、主枝不动——⛔以残果放行%s' % 示(e), 报合(e, '败') and e['报'].get('因') == '片' and not e['T在主']
      and any('⛔片闸·败' in x for x in e['报']['红']))
    e = 演['章']
    T('④之七 以 章-N 触：成、章标恒留、报之「演」係真克隆章标之判（可跑之仓）%s' % 示(e), 报合(e, '成') and '章-9' in e['枝们']
      and (e['报'].get('演') or {}).get('果') == '过')
    e = 演['主动']
    一 = (e.get('二') or {}).get('报一') or {}
    T('④之八 闸中主枝被他坐推进：推被拒 → API 重派本枝（tries 1）、报「败·重派」（候者⛔作坏）；续跑并新主、再闸而成——二笔俱入主%s' % 示(e),
      一.get('果') == '败' and 一.get('因') == '重派' and not 坏(一) and '"tries": "1"' in e.get('派', '') and '/actions/workflows/autopush.yml/dispatches' in e.get('派', '')
      and 报合(e, '成') and e['报'].get('试') == 1 and e['T在主'] and e['他在主'])
    e = 演['重派尽']
    T('④之九 重派已二回（tries 2）而主枝又进 → 败（因 non-ff）、⛔再派%s' % 示(e), 报合(e, '败') and e['报'].get('因') == 'non-ff' and not e.get('派'))
    e = 演['中已在']
    T('④之十 闸中他坐以他并含本枝 → 推被拒而「已在」、治枝删%s' % 示(e), 报合(e, '已在') and e['T在主'] and e['R'] not in e['枝们'])
    e = 演['演']
    主前 = e.get('主')
    T('④之十一 演练（派）：改 workflows 之枝照演（⛔拒）、闸恰一、报/演/试一.json 果「过」；主枝不动、⛔删枝、⛔写器红账%s' % 示(e),
      恰一(e) and (e.get('演报') or {}).get('果') == '过' and e['演报'].get('名') == '试一' and not e['T在主'] and e['R'] in e['枝们']
      and e.get('器红账') is None and e.get('报') is None and e['演报'].get('sha') == e['T'])
    e = 演['演红']
    T('④之十二 演练之红 → 报/演 果「红」带红行%s' % 示(e), (e.get('演报') or {}).get('果') == '红' and any('字数闸' in x for x in e['演报'].get('红') or []))
    e = 演['演推']
    T('④之十三 演练（推 备份/演/<名>）：名去前缀、所演即其树、果「过」%s' % 示(e), (e.get('演报') or {}).get('果') == '过'
      and e['演报'].get('ref') == 演之前缀 + '试一' and not e['T在主'])
    # 1117 GitHub 化之审·F（法用#闸取仓之速）：省取（partial clone）与其降级
    省 = re.search(r'filter: (\S+)', 诸['gate.yml'])
    省 = 省.group(1) if 省 else ''
    e = 演['成']
    T('④之十四 省取之常：备候、诸片俱省取（%s·真 partial clone）、片印懒取之计（败 0）、⛔降级%s' % (省 or '无 filter', 示(e)),
      bool(省) and '｜取 blob:' in e.get('印', '') and len(re.findall(r'省取（blob:[^）]+）：懒取 0 回、败 0、', e['印'])) >= 3
      and '省取降级' not in e['印'])
    e = 演['省败']
    T('④之十五 省取不成（带 filter 之 checkout 俱败·continue-on-error）→ 备候、诸片俱自降级全取：闸恰一、成、主枝即候%s' % 示(e),
      恰一(e) and 报合(e, '成') and e['T在主'] and len(re.findall(r'(?m)^告 .*：::warning::省取降级·全取（检出不成：failure）', e['印'])) >= 4)
    e = 演['懒败']
    计 = e.get('计') or []
    T('④之十六 片一於省取之仓懒取而败（其格俱红）→ 自降级全取、重跑其片而绿：成、⛔器红、诸格俱跑（唯片一二回）%s' % 示(e),
      报合(e, '成') and e['T在主'] and not e['报'].get('器红') and len(set(计)) == _桩名数 and len(计) > _桩名数
      and len(re.findall(r'(?m)^告 .*：::warning::省取降级', e['印'])) == 1 and '：::warning::省取降级·全取（片中懒取败 1 回）' in e['印'])
    ok = sum(R)
    print('── 负测·autopush %d/%d %s ──' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    if ok != len(R):
        for k, v in 演.items():
            if v.get('崩') or os.environ.get('ZM_推报印'):
                print('══ 景 %s ══ %s\n%s' % (k, v.get('崩', ''), str(v.get('印', ''))[-3000:]))
    return ok == len(R)


def _参(a, k, 缺=''):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else 缺


def _读印(p):
    return open(p, encoding='utf-8', errors='replace').read() if p and os.path.exists(p) else ''


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--验' in a:
        缺 = 验盘()
        for x in 缺:
            print('  ✗ ' + x)
        print('✓ autopush／gate／演练 与 pre-push 之形俱合' if not 缺 else '⛔ 推报·验：%d 缺' % len(缺))
        sys.exit(0 if not 缺 else 1)
    if '--写' in a:
        印 = _读印(_参(a, '--印'))
        d = 成报(_参(a, '--ref'), _参(a, '--sha'), _参(a, '--果', '败'), 印, _参(a, '--主'), _参(a, '--跑'), _参(a, '--因'), _参(a, '--试', '0') or 0,
               候=_参(a, '--候'), 判=_读json(_参(a, '--判')) if _参(a, '--判') else None,
               演=_读演之印(_参(a, '--演')) if _参(a, '--演') else None)
        j, x = 写(d, 印, _参(a, '--出', '.'))
        print('✓ 报：%s（%s）' % (j, d['果']))
        sys.exit(0)
    if '--写演' in a:
        印 = _读印(_参(a, '--印'))
        d = 成演报(_参(a, '--名'), _参(a, '--ref'), _参(a, '--sha'), _参(a, '--果', '红'), 印, _参(a, '--跑'), _参(a, '--因'), _参(a, '--候'),
                 _读json(_参(a, '--判')) if _参(a, '--判') else None)
        print('✓ 演报：%s（%s）' % (写演(d, 印, _参(a, '--出', '.')), d['果']))
        sys.exit(0)
    if '--落' in a:
        ok, 语 = 落(_参(a, '--落'), _参(a, '--信', '报'))
        print(语)
        sys.exit(0 if ok else 1)
    if '--读' in a:
        d = 读(_参(a, '--读'))
        if not d:
            print('· 云端 %s 无 %s' % (报枝, 报径(_参(a, '--读'))))
            sys.exit(1)
        print('\n'.join(报之语(d)))
        sys.exit(3 if 坏(d) else 0)
    if '--读演' in a:
        d = 读演(_参(a, '--读演'))
        if not d:
            print('· 云端 %s 无 %s' % (报枝, 演径(_参(a, '--读演'))))
            sys.exit(1)
        print('\n'.join(报之语(d)))
        sys.exit(3 if d.get('果') != '过' else 0)
    print(__doc__)
    sys.exit(0)
