#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""推报（1027 立·坑51）——GitHub autopush 之报：机写 `备份/报` 之 `报/推/<枝>.json`（与 .txt），会话 git fetch 读之；并验 autopush.yml 与 pre-push 之形。

【其由·坑51】404、406—410 之 autopush 俱败、唯 405 成，主枝只由沙盒直推而进：
  ①旧 yml 先一步跑 pre-push，其中全测之 chk_hookspath 把 core.hooksPath 自愈挂回，「推主枝」之 push 遂把十二至十九分之闸再跑一回；
  ②其间沙盒照 封版.py 旧印之「下一步 推.py」直推主枝（本地 pre-push 又跑全测并），autopush 之 push 遂 non-fast-forward 而败、无 fetch 无重试；
  ——一章之树三跑闸（私库之分钟计费），GitHub 之路恒输；③总章二之7 许「果入 备份/报、会话 fetch 读之」，无一器实之。
【其法·零 token】
  ①写（GitHub 之机·autopush.yml 之报步，if: always()）：`--写` 自推之印析红行（✗ 之行与「⛔全测未过：」之行）与器红，
    出 json（ref、sha、果、红、main_after、时、run_url，并 因、试、器红）与末八十行之 txt；交於 备份/报 由 yml 之 bash 办（取、建、推，败即再取）。
  ②读（沙盒）：`读(枝)` git fetch 备份/报 而 git show 其 json——推.py --候、接棒守 --候主 俱经此（⛔另造一把尺）；`快进()` 成即本地快进主枝。
  ③验：`验(yml, 钩)` 静验——一试一闸、被拒即取而判已在或并而再试（至多三）、改 workflows 先判拒、报写 备份/报（always）、
    只删治枝、触发含 章-* 与 治-*、钩只免三暂存之前缀而主枝照闸。⛔依 PyYAML（GitHub 之机 setup-python 无之）。
    `--自测` 并以旧 yml（540c1c91）回灌须红；以桩闸真跑 yml 之 bash 於临时之裸库（成、闸中主进而再试、已在、红、拒、章标恒留）；钩之 stdin 诸形真跑。
用法：
  python3 工具/推报.py --读 章-411        # 印云端之报（无即 rc=1；坏果 rc=3）
  python3 工具/推报.py --验               # 静验 .github/workflows/autopush.yml 与 工具/githooks/pre-push
  python3 工具/推报.py --写 --ref R --sha S --果 G [--因 Y] [--试 K] --印 档 --主 SHA --跑 URL --出 目   # autopush.yml 之报步用
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


def 报径(枝, 式='json'):
    return '报/推/%s.%s' % (枝, 式)


# ═══ 一、写（GitHub 之机） ═══
def 红行(印):
    """→ 闸之红行：含 ✗ 之行、「⛔全测未过：」之行（去重、存序、至多六十）。"""
    出 = []
    for l in (印 or '').split('\n'):
        s = l.strip()
        if s and ('✗' in s or '⛔全测未过：' in s) and s not in 出:
            出.append(s[:300])
    return 出[:60]


def 器红(印):
    """→ 只器之红之名（推闸·分等放行之行；GitHub 之机之 设定/器红账.json 不回写，故入报）。"""
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


def 成报(ref, sha, 果, 印, 主='', 跑='', 因='', 试=0, 时=None):
    果 = 果 if 果 in 诸果 else '败'
    红 = 红行(印) if 果 in 坏果 else []
    if 果 in ('拒', '败') and not 红:
        红 = 要行(印)
    return {'ref': ref, 'sha': sha, '果': 果, '红': 红, 'main_after': 主 or '',
            '时': 时 or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'run_url': 跑 or '',
            '因': 因 or '', '试': int(试 or 0), '器红': 器红(印)}


def 写(d, 印, 出目):
    """→ (json 之路, txt 之路)：出目/报/推/<ref>.json 与 .txt（印之末八十行）。"""
    j = os.path.join(出目, 报径(d['ref']))
    x = os.path.join(出目, 报径(d['ref'], 'txt'))
    os.makedirs(os.path.dirname(j), exist_ok=True)
    json.dump(d, open(j, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(x, 'w', encoding='utf-8').write('\n'.join((印 or '').rstrip('\n').split('\n')[-80:]) + '\n')
    return j, x


# ═══ 二、读（沙盒） ═══
_定库之变 = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES')


def _git(a, root=ROOT, 限=120):
    """⛔承外之 GIT_DIR 诸变（钩中、演中）——库只由 root 定。"""
    e = {k: v for k, v in os.environ.items() if k not in _定库之变}
    return subprocess.run(['git', '-c', 'core.quotepath=off'] + a, cwd=root, capture_output=True, text=True, timeout=限, env=e)


def 读(枝, root=ROOT, 取=True):
    """→ 云端 备份/报 里 报/推/<枝>.json 之 dict；无、读不出即 None（⛔作绿）。"""
    远 = 'refs/remotes/origin/' + 报枝
    try:
        if 取:
            _git(['fetch', '-q', 'origin', '+refs/heads/%s:%s' % (报枝, 远)], root)
        r = _git(['show', '%s:%s' % (远, 报径(枝))], root)
        if r.returncode != 0 or not r.stdout.strip():
            return None
        d = json.loads(r.stdout)
        return d if isinstance(d, dict) else None
    except Exception:
        return None


def 报之语(d):
    """→ 印之行：果、因、红行、run_url。"""
    L = ['%s 报·%s（%s）：%s%s｜%s' % ('✓' if d.get('果') in ('成', '已在') else '⛔', d.get('ref'), str(d.get('sha', ''))[:12],
                                     d.get('果'), ('（因 %s）' % d['因']) if d.get('因') else '', d.get('时', ''))]
    L += ['    ' + x for x in (d.get('红') or [])[:20]]
    if d.get('器红'):
        L.append('    · 器红（只报不拦·GitHub 之机⛔回写 器红账）：' + '、'.join(d['器红']))
    if d.get('run_url'):
        L.append('    · ' + d['run_url'])
    return L


def 快进(root=ROOT):
    """成而後：本地主枝快进到 origin 主枝（能则进；不在主枝、本地有未入主之提交即⛔动）。→ (进否, 语)"""
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
def _诸步(文):
    """→ [{键: 值}]：steps 下诸 `- 键:` 之步；run: | 之块去缩进而存。只认本 yml 之形（⛔依 PyYAML）。"""
    行 = 文.split('\n')
    步, 当, 基, 键缩, 在 = [], None, None, None, False
    i = 0
    while i < len(行):
        l = 行[i]
        if re.match(r'^\s*steps:\s*$', l):
            在, 基, 当 = True, None, None
            i += 1
            continue
        if not 在:
            i += 1
            continue
        m = re.match(r'^(\s*)- ([\w-]+):\s*(.*)$', l)
        if m and (基 is None or len(m.group(1)) == 基):
            基, 当 = len(m.group(1)), {}
            步.append(当)
            键缩 = 基 + 2
            键, 值 = m.group(2), m.group(3)
        else:
            m = re.match(r'^(\s*)([\w-]+):\s*(.*)$', l)
            if not (当 is not None and m and len(m.group(1)) == 键缩):
                if l.strip() and 基 is not None and len(l) - len(l.lstrip()) < 基:
                    在 = False
                i += 1
                continue
            键, 值 = m.group(2), m.group(3)
        i += 1
        if 值.strip() in ('|', '|-', '>', '>-', ''):
            块 = []
            while i < len(行) and (not 行[i].strip() or len(行[i]) - len(行[i].lstrip()) > 键缩):
                块.append(行[i])
                i += 1
            缩 = min((len(x) - len(x.lstrip()) for x in 块 if x.strip()), default=0)
            当[键] = '\n'.join(x[缩:] for x in 块).strip('\n') + ('\n' if 值.strip().startswith('|') else '')
        else:
            v = 值.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in '\'"':
                v = v[1:-1]
            当[键] = v
    return 步


def _顶块(文, 键):
    m = re.search(r'(?ms)^%s:\s*\n(.*?)(?=^\S|\Z)' % re.escape(键), 文)
    return m.group(1) if m else ''


def _触(文):
    """→ (push 之 branches, 有 workflow_dispatch 否)。"""
    块 = _顶块(文, 'on')
    m = re.search(r'branches:\s*\[([^\]]*)\]', 块)
    if m:
        枝 = [x.strip().strip('\'"') for x in m.group(1).split(',') if x.strip()]
    else:
        m = re.search(r'(?ms)branches:\s*\n((?:\s+-\s*\S.*\n?)+)', 块)
        枝 = [x.strip()[1:].strip().strip('\'"') for x in m.group(1).split('\n') if x.strip()] if m else []
    return 枝, bool(re.search(r'(?m)^\s+workflow_dispatch:', 块))


def _环(文):
    """→ [(起, 止, 回数)]：`for v in 1 2 3; do … done`（同缩之 done）。"""
    出 = []
    for m in re.finditer(r'(?m)^(\s*)for \w+ in ([\d ]+); do\s*$', 文):
        缩 = m.group(1)
        d = re.compile(r'(?m)^%sdone\b' % re.escape(缩)).search(文, m.end())
        if d:
            出.append((m.start(), d.start(), len(m.group(2).split())))
    return 出


_主推式 = re.compile(r'git\s+(?:-c\s+\S+\s+)*push\b[^\n]*refs/heads/(?:\$MAIN|\$\{MAIN\}|' + re.escape(主枝) + r')\b')
_直闸式 = re.compile(r'(?m)^\s*(?:bash\s+|sh\s+|\./)?工具/githooks/pre-push\b|python3?\s+[^\n]*工具/全测并?\.py')
_绕式 = ('--no-verify', 'ZM_SKIP_HOOK')


def 验(yml, 钩):
    """静验 autopush.yml 与 pre-push 之文 → [缺]（空即绿）。"""
    缺 = []
    步 = _诸步(yml)
    跑们 = [s.get('run', '') for s in 步]
    env = dict(re.findall(r'(?m)^  ([A-Z_]+):\s*(\S+)\s*$', _顶块(yml, 'env')))
    枝, 手 = _触(yml)
    if not ('章-*' in 枝 and '治-*' in 枝 and 手):
        缺.append('①触：push 之 branches 须含 章-* 与 治-*、并 workflow_dispatch（今 %s%s）' % (枝, '' if 手 else '、无 workflow_dispatch'))
    if not (re.search(r'(?m)^\s+group:\s*autopush\s*$', yml) and re.search(r'(?m)^\s+cancel-in-progress:\s*false\s*$', yml)):
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
        if any(w in 行 for w in _绕式 + ('core.hooksPath=',)):
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
    报 = [s for s in 步 if 'always()' in str(s.get('if', '')) and '推报.py' in s.get('run', '')]
    报跑 = 报[0].get('run', '') if 报 else ''
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
    删 = [s for s in 步 if re.search(r'--delete|":\$N"|:refs/heads/治-', s.get('run', ''))]
    if not 删 or not any('refs/heads/治-*' in s.get('run', '') and '成' in str(s.get('if', '')) for s in 删):
        缺.append('⑧删：治枝成（成／已在）即删')
    if re.search(r'(--delete|:refs/heads/)[^\n]*章-', yml) or any('章-' in s.get('run', '') for s in 删):
        缺.append('⑧删：⛔删 章-*（章标恒留）')
    绕 = [w for w in _绕式 if w in yml]
    if 绕:
        缺.append('⑨⛔绕闸之字：%s' % 绕)
    # 钩
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


def 验盘(root=ROOT):
    yml = open(os.path.join(root, '.github', 'workflows', 'autopush.yml'), encoding='utf-8').read()
    钩 = open(os.path.join(root, '工具', 'githooks', 'pre-push'), encoding='utf-8').read()
    return 验(yml, 钩)


# ═══ 四、演（自测用·临时之裸库；⛔碰真仓） ═══
_桩闸 = r'''#!/usr/bin/env python3
# 桩之全测并（推报·自测）：计次；ZM_STUB=红 即印 ✗ 而 rc=1；ZM_STUB_MOVE=<他之克隆> 则首闸之中把主枝推进一笔
import os, sys, subprocess
计 = os.environ.get('ZM_STUB_CNT')
n = 0
if 计:
    open(计, 'a').write('闸\n'); n = len(open(计).read().split())
他 = os.environ.get('ZM_STUB_MOVE')
if 他 and n == 1:
    e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_') or k.startswith('GIT_CONFIG')}
    subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:refs/heads/' + os.environ['ZM_STUB_MAIN']], cwd=他, env=e, capture_output=True)
print('  ✓ 桩项甲        ok')
if os.environ.get('ZM_STUB') == '红':
    print('  ✗ 桩项乙        坏了一处'); print('  ✗ 桩项丙        又坏一处'); print('\n  ⛔全测未过：桩项乙、桩项丙'); sys.exit(1)
print('\n  ✓全测通过（并）。')
'''


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


def _式值(式, env, 前成):
    """GitHub 之式（只本 yml 所用：always()、success()、env.X、github.ref_name、startsWith、==、!=、&&、||）。"""
    if not 式:
        return 前成
    s = 式.replace('${{', '').replace('}}', '')
    s = re.sub(r'env\.(\w+)', lambda m: repr(env.get(m.group(1), '')), s)
    s = s.replace('github.ref_name', repr(env.get('GITHUB_REF_NAME', '')))
    s = s.replace('always()', 'True').replace('success()', repr(前成)).replace('failure()', repr(not 前成))
    s = s.replace('&&', ' and ').replace('||', ' or ').replace('startsWith(', '_sw(')
    return bool(eval(s, {'__builtins__': {}, '_sw': lambda a, b: str(a).startswith(str(b)), 'True': True, 'False': False}))


def 演yml(yml, 钩, 推报文, 景, 目):
    """以桩闸真跑 yml 诸步之 bash（一如 GitHub：bash --noprofile --norc -eo pipefail）於 目 下之裸库。
    景：成｜主动（闸中主枝被推进一笔）｜已在（沙盒已直推主枝）｜红｜拒（改 workflows）｜章（以 章-N 触、成）。
    → {果, 闸次, 主, T在主, 他在主, 枝们, 报, 印}"""
    env0 = _净env()
    裸, 种, 沙, 机, 他, rt = (os.path.join(目, x) for x in ('o.git', '种', '沙', '机', '他', 'rt'))
    os.makedirs(rt)
    _g(['init', '-q', '--bare', 裸], 目)
    _g(['init', '-q', '-b', 主枝, 种], 目)
    for p, t, x in (('工具/githooks/pre-push', 钩, True), ('工具/全测并.py', _桩闸, False), ('工具/推报.py', 推报文, False),
                    ('.github/workflows/autopush.yml', yml, False), ('a.txt', '甲\n', False), ('b.txt', '乙\n', False)):
        f = os.path.join(种, p)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w', encoding='utf-8').write(t)
        if x:
            os.chmod(f, 0o755)
    _g(['add', '-A'], 种)
    _g(['commit', '-q', '-m', '种'], 种)
    _g(['push', '-q', 裸, 'HEAD:refs/heads/' + 主枝], 种)
    _g(['clone', '-q', '-b', 主枝, 裸, 沙], 目)
    if 景 == '拒':
        open(os.path.join(沙, '.github', 'workflows', 'autopush.yml'), 'a', encoding='utf-8').write('# 改\n')
    else:
        open(os.path.join(沙, 'a.txt'), 'a', encoding='utf-8').write('甲之治\n')
    _g(['commit', '-qam', '治'], 沙)
    T = _g(['rev-parse', 'HEAD'], 沙)
    R = ('章-9' if 景 == '章' else '治-' + T[:12])
    _g(['push', '-q', 'origin', 'HEAD:refs/heads/' + R], 沙)
    if 景 == '已在':
        _g(['push', '-q', 'origin', 'HEAD:refs/heads/' + 主枝], 沙)
    _g(['clone', '-q', '-b', 主枝, 裸, 他], 目)
    open(os.path.join(他, 'b.txt'), 'a', encoding='utf-8').write('乙之进\n')
    _g(['commit', '-qam', '他坐直推'], 他)
    他sha = _g(['rev-parse', 'HEAD'], 他)
    _g(['clone', '-q', '-b', 主枝, 裸, 机], 目)          # actions/checkout（ref 主枝、fetch-depth 0）
    计 = os.path.join(目, '闸计')
    genv = os.path.join(rt, 'GITHUB_ENV')
    open(genv, 'w').close()
    顶env = dict(re.findall(r'(?m)^  ([A-Z_]+):\s*(\S+)\s*$', _顶块(yml, 'env')))
    env = dict(env0, **顶env)
    env.update(GITHUB_SHA=T, GITHUB_REF_NAME=R, GITHUB_ENV=genv, RUNNER_TEMP=rt, GITHUB_SERVER_URL='https://github.com',
               GITHUB_REPOSITORY='演/仓', GITHUB_RUN_ID='1', ZM_STUB_CNT=计, ZM_STUB_MAIN=主枝,
               ZM_STUB='红' if 景 == '红' else '绿')
    for k in ('GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL'):
        env.pop(k, None)                                  # 机之身由 yml 之 git config 定（⛔借测者之身）
    if 景 == '主动':
        env['ZM_STUB_MOVE'] = 他
    前成, 印 = True, []
    for k, s in enumerate(_诸步(yml)):
        if 'run' not in s:
            continue
        for l in open(genv, encoding='utf-8').read().split('\n'):
            if '=' in l:
                a, b = l.split('=', 1)
                env[a] = b
        if not _式值(s.get('if', ''), env, 前成):
            印.append('· 步 %s：免（if 不合）' % s.get('name', k))
            continue
        sp = os.path.join(rt, '步%d.sh' % k)
        open(sp, 'w', encoding='utf-8').write(s['run'])
        r = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', sp], cwd=机, env=env,
                           capture_output=True, text=True, timeout=300)
        印.append('· 步 %s：rc=%d\n%s%s' % (s.get('name', k), r.returncode, r.stdout[-1500:], r.stderr[-1500:]))
        前成 = 前成 and r.returncode == 0
    主 = _g(['rev-parse', 'refs/heads/' + 主枝], 裸)
    枝们 = [x.split('refs/heads/', 1)[1] for x in _g(['for-each-ref', '--format=%(refname)', 'refs/heads/'], 裸).split('\n') if x]
    报 = None
    r = subprocess.run(['git', 'show', 'refs/heads/%s:%s' % (报枝, 报径(R))], cwd=裸, capture_output=True, text=True, env=env0)
    if r.returncode == 0:
        报 = json.loads(r.stdout)
    in主 = lambda x: subprocess.run(['git', 'merge-base', '--is-ancestor', x, 主], cwd=裸, env=env0, capture_output=True).returncode == 0
    return {'果': env.get('GUO'), '闸次': len(open(计).read().split()) if os.path.exists(计) else 0, '主': 主, 'T': T, 'R': R,
            'T在主': in主(T), '他在主': in主(他sha), '枝们': 枝们, '报': 报, '印': '\n'.join(印), '沙': 沙}


def 演钩(钩, 目):
    """钩之 stdin 诸形真跑（桩之全测并计次）。→ {形: (rc, 闸否, 推闸之果)}"""
    _g(['init', '-q', '-b', 主枝, 目], os.path.dirname(目))
    os.makedirs(os.path.join(目, '工具', 'githooks'))
    open(os.path.join(目, '工具', 'githooks', 'pre-push'), 'w', encoding='utf-8').write(钩)
    os.chmod(os.path.join(目, '工具', 'githooks', 'pre-push'), 0o755)
    open(os.path.join(目, '工具', '全测并.py'), 'w', encoding='utf-8').write(_桩闸)
    计 = os.path.join(目, '..', '钩计')
    z, s = '0' * 40, 'a' * 40
    形 = {'治': 'HEAD %s refs/heads/治-abc %s\n' % (s, z), '章': 'HEAD %s refs/heads/章-411 %s\n' % (s, z),
         '备份': 'HEAD %s refs/heads/备份/报 %s\n' % (s, z), '主': 'HEAD %s refs/heads/%s %s\n' % (s, 主枝, z),
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


def 自测():
    R = []

    def T(名, 条):
        R.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    # ①析
    印 = ('── 第 1 试 ──\n  ✓ 甲  ok\n  ✗ 负测·乙   坏\n  ✗ 质量三闸  红一处\n\n  ⛔全测未过：负测·乙、质量三闸\n'
         '  ✓推闸·分等：放行——只器之红 2（负测·丙、跑账），只报不拦\n⛔ 全测未过,推送已拦停。\nerror: failed to push some refs\n')
    T('①析红：✗ 之行与全测总红之行（去重存序）', 红行(印) == ['✗ 负测·乙   坏', '✗ 质量三闸  红一处', '⛔全测未过：负测·乙、质量三闸'])
    T('①之二 器红：取推闸·分等之名', 器红(印) == ['负测·丙', '跑账'])
    d = 成报('治-abc', 'f' * 40, '红', 印, 主='e' * 40, 跑='https://x/runs/1', 时='2026-10-27T00:00:00Z')
    T('①之三 报之键俱在（ref、sha、果、红、main_after、时、run_url）', all(k in d for k in ('ref', 'sha', '果', '红', 'main_after', '时', 'run_url'))
      and d['果'] == '红' and len(d['红']) == 3)
    T('①之四 成、已在⛔带红；拒败无 ✗ 者取其由；果不在五者即败',
      成报('a', 'b', '成', 印)['红'] == [] and 成报('a', 'b', '拒', '⛔拒：改 workflows\n')['红'] == ['⛔拒：改 workflows']
      and 成报('a', 'b', '怪', '')['果'] == '败')
    with tempfile.TemporaryDirectory() as t:
        j, x = 写(d, '\n'.join('行%d' % i for i in range(200)), t)
        T('①之五 写：报/推/<枝>.json 可解回、txt 存末八十行', json.load(open(j, encoding='utf-8')) == d
          and open(x, encoding='utf-8').read().split('\n')[0] == '行120' and j.endswith(os.path.join('报', '推', '治-abc.json')))
    # ②验：今盘绿；旧 yml 回灌红；诸改坏各红
    yml = open(os.path.join(ROOT, '.github', 'workflows', 'autopush.yml'), encoding='utf-8').read()
    钩 = open(os.path.join(ROOT, '工具', 'githooks', 'pre-push'), encoding='utf-8').read()
    今缺 = 验(yml, 钩)
    T('②今盘 autopush.yml 与 pre-push 之形俱合%s' % ('' if not 今缺 else '：' + '；'.join(今缺)), not 今缺)
    try:
        import yaml as _y
        _d = _y.safe_load(yml)
        _on = _d.get('on', _d.get(True)) or {}
        _yr = [s.get('run', '') for s in _d['jobs']['advance']['steps']]
        T('②之二 PyYAML 可解，且与本器之析同（触、诸步之 run）', _on['push']['branches'] == _触(yml)[0]
          and [x for x in _yr if x] == [s['run'] for s in _诸步(yml) if 'run' in s])
    except ImportError:
        T('②之二 无 PyYAML（GitHub 之机 setup-python 无之）——本器自析', bool(_诸步(yml)))
    旧 = subprocess.run(['git', 'show', '%s:.github/workflows/autopush.yml' % 旧yml之笔], cwd=ROOT, capture_output=True, text=True).stdout
    旧缺 = 验(旧, 钩) if 旧 else []
    T('②之三 旧 yml（%s·坑51 之形）回灌须红：一闸二跑、无取再试、无报、无治（%d 缺）' % (旧yml之笔, len(旧缺)),
      bool(旧) and any(x.startswith('③') for x in 旧缺) and any(x.startswith('⑦') for x in 旧缺) and any(x.startswith('①') for x in 旧缺)
      and any(x.startswith('④') for x in 旧缺))
    坏 = {
        '再添直跑 pre-push 一步': yml.replace('      - name: 删已并之治枝', '      - name: 推闸\n        run: bash 工具/githooks/pre-push\n      - name: 删已并之治枝'),
        '去 治-* 之触': yml.replace("branches: ['章-*', '治-*']", "branches: ['章-*']"),
        '去重试': yml.replace('; continue\n', '; break\n'),
        '重试⛔问主进否': yml.replace('!= "$B0"', '!= "x"'),
        '报⛔always': yml.replace("        if: always()\n        shell: bash\n        run: |\n          set +e\n          R=", "        shell: bash\n        run: |\n          set +e\n          R="),
        '推主枝绕钩': yml.replace('git push origin "HEAD:refs/heads/$MAIN"', 'git push --no-verify origin "HEAD:refs/heads/$MAIN"'),
        '删及章标': yml.replace("refs/heads/治-*) git merge-base", "refs/heads/治-*|refs/heads/章-*) git merge-base").replace(
            "'refs/heads/治-*')", "'refs/heads/治-*' 'refs/heads/章-*')"),
        '⛔先判拒': yml.replace('.github/workflows)" ]', '.github/xx)" ]'),
        '五试': yml.replace('for i in 1 2 3; do', 'for i in 1 2 3 4 5; do'),
    }
    T('②之四 诸改坏（%d 形）各红' % len(坏), all(验(v, 钩) and v != yml for v in 坏.values()))
    坏钩 = {'免及主枝': 钩.replace('refs/heads/章-*|refs/heads/治-*|refs/heads/备份/*)', 'refs/heads/*)'),
          '旧钩（⛔读 stdin）': subprocess.run(['git', 'show', '%s:工具/githooks/pre-push' % 旧yml之笔], cwd=ROOT, capture_output=True, text=True).stdout,
          '有一即免': 钩.replace('"$N_ALL" -eq "$N_STAGE"', '"$N_STAGE" -ge 1')}
    T('②之五 钩之改坏（免及主枝、旧钩、有一暂存即免）各红', all(验(yml, v) for v in 坏钩.values()))
    # ③钩之 stdin 诸形真跑
    with tempfile.TemporaryDirectory() as t:
        o = 演钩(钩, os.path.join(t, '钩'))
    T('③钩：治／章／备份 only → 免闸 rc=0', all(o[k][:2] == (0, False) for k in ('治', '章', '备份')))
    T('③之二 主枝 only、主枝＋治、删主、章外（前缀之外）→ 照闸（绿 rc=0、落「绿」）',
      all(o[k] == (0, True, '绿') for k in ('主', '主＋治', '删主', '章外')))
    T('③之三 删治 → 免；git 所喂空（俱已同或被拒）→ 免；手跑（无参）→ 照闸', o['删治'][:2] == (0, False) and o['空'][:2] == (0, False)
      and o['手跑'] == (0, True, '绿'))
    T('③之四 主枝而闸红 → rc=1、落「红」', o['主·红'] == (1, True, '红'))
    o2 = {}
    with tempfile.TemporaryDirectory() as t:
        o2 = 演钩(坏钩['免及主枝'], os.path.join(t, '钩'))
    T('③之五 回灌：免及主枝之钩 → 主枝竟免闸（此即其病，静验亦红）', o2['主'][:2] == (0, False))
    # ④yml 之 bash 真跑（桩闸·临时之裸库）
    推报文 = open(os.path.abspath(__file__), encoding='utf-8').read()
    演 = {}
    for 景 in ('成', '主动', '已在', '红', '拒', '章'):
        with tempfile.TemporaryDirectory() as t:
            try:
                演[景] = 演yml(yml, 钩, 推报文, 景, t)
                if 景 == '主动':
                    _r = 读(演[景]['R'], 演[景]['沙'])
                    演[景]['读'] = _r
                    演[景]['快进'] = 快进(演[景]['沙'])
                    演[景]['沙主'] = _git(['rev-parse', 'HEAD'], 演[景]['沙']).stdout.strip()
            except Exception as e:
                演[景] = {'果': '⛔演崩：%s' % e, '报': None, '印': ''}
    def 报合(e, 果):
        b = e.get('报') or {}
        return b.get('果') == 果 and b.get('ref') == e.get('R') and b.get('sha') == e.get('T') and b.get('main_after') == e.get('主') \
            and b.get('run_url', '').endswith('/演/仓/actions/runs/1') and re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ', b.get('时', ''))
    e = 演['成']
    T('④成：一闸、主枝含本 sha、治枝已删、报「成」（键俱）%s' % ('' if e.get('果') == '成' else '：' + str(e.get('果')) + e.get('印', '')[-600:]),
      e.get('果') == '成' and e.get('闸次') == 1 and e.get('T在主') and e.get('R') not in e.get('枝们', []) and 报合(e, '成'))
    e = 演['主动']
    T('④之二 闸中主枝被推进：取、并、再试——二闸（树变方重闸）、二笔俱入主、报「成」试 2%s' % ('' if e.get('果') == '成' else '：' + str(e.get('果')) + e.get('印', '')[-600:]),
      e.get('果') == '成' and e.get('闸次') == 2 and e.get('T在主') and e.get('他在主') and 报合(e, '成') and e['报'].get('试') == 2)
    T('④之三 沙盒 读(枝) 得其报、快进到并後之主枝', (e.get('读') or {}).get('果') == '成' and (e.get('快进') or (False,))[0]
      and e.get('沙主') == e.get('主') != e.get('T'))
    e = 演['已在']
    T('④之四 已在：⛔闸、报「已在」、治枝删', e.get('果') == '已在' and e.get('闸次') == 0 and 报合(e, '已在') and e.get('R') not in e.get('枝们', []))
    e = 演['红']
    T('④之五 红：一闸、主枝不动、治枝留、报「红」带 ✗ 之行与全测总红之行', e.get('果') == '红' and e.get('闸次') == 1 and not e.get('T在主')
      and e.get('R') in e.get('枝们', []) and 报合(e, '红') and '✗ 桩项乙        坏了一处' in e['报']['红'] and '⛔全测未过：桩项乙、桩项丙' in e['报']['红'])
    e = 演['拒']
    T('④之六 拒：改 workflows 者⛔闸、主枝不动、报「拒」因 workflow', e.get('果') == '拒' and e.get('闸次') == 0 and not e.get('T在主')
      and 报合(e, '拒') and e['报'].get('因') == 'workflow')
    e = 演['章']
    T('④之七 以 章-N 触：成而章标恒留', e.get('果') == '成' and e.get('闸次') == 1 and '章-9' in e.get('枝们', []) and 报合(e, '成'))
    ok = sum(R)
    print('── 负测·autopush %d/%d %s ──' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    return ok == len(R)


def _参(a, k, 缺=''):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else 缺


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--验' in a:
        缺 = 验盘()
        for x in 缺:
            print('  ✗ ' + x)
        print('✓ autopush.yml 与 pre-push 之形俱合' if not 缺 else '⛔ 推报·验：%d 缺' % len(缺))
        sys.exit(0 if not 缺 else 1)
    if '--写' in a:
        印 = open(_参(a, '--印'), encoding='utf-8', errors='replace').read() if os.path.exists(_参(a, '--印')) else ''
        d = 成报(_参(a, '--ref'), _参(a, '--sha'), _参(a, '--果', '败'), 印, _参(a, '--主'), _参(a, '--跑'), _参(a, '--因'), _参(a, '--试', '0') or 0)
        j, x = 写(d, 印, _参(a, '--出', '.'))
        print('✓ 报：%s（%s）' % (j, d['果']))
        sys.exit(0)
    if '--读' in a:
        d = 读(_参(a, '--读'))
        if not d:
            print('· 云端 %s 无 %s' % (报枝, 报径(_参(a, '--读'))))
            sys.exit(1)
        print('\n'.join(报之语(d)))
        sys.exit(3 if d.get('果') in 坏果 else 0)
    print(__doc__)
    sys.exit(0)
