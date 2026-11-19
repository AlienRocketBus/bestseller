#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""进化树（1119 立·作者令「进化路线·进化树·俱存 GitHub 主线·⛔倒车」与「GitHub 上诸程序亦不停进化」·法用#进化树）。

作者 1119 原话之要：
  「只要每次我们去给一个方法进行进化和升级……都要严格考虑我们的总目标和我们的6个主义……尽最大可能的能够使用GitHub。
   把所有的这些进化和修改记录……都要认认真真的保存在GitHub的主线……每次进化具体修改了什么地方，具体进化到什么地方……
   我们要有一个进化树，从零到最后完美，我们要知道他是怎么去进化出来的……所有的坑……都要认认真真的去记录……
   为什么这个方法会变得更好……千万不要走倒车路线」；
  「我们在GitHub上面运行的这些所有的程序，也要不断的去进化，变得绝对的完美，趋于完美。朝着完美不断的去进化」。

为何立：一法之进化散在四处——法用册（今之形、所废）、方法账（判、所废、较旧：为何更好）、方法坑账（踩过之坑）、git 之提交
  （每回具体改了何处）——各账各写、⛔一处可读「此法从零到今是怎么长出来的」；GitHub 上之诸程序（.github/workflows 与其所调之器）
  更⛔一处记其进化。旧之 进化链（设定/进化链.md）只问「犯过之错今有无器守」，⛔问「法之线」——同名异功，⛔相代。
其法（零 token·虹吸：⛔新立手填之账，只串现有之账）：
  ①设定/法用册.json 之「法」「待」「废」——一号一节。所替（已废之枝归哪一今法·1119 复核改）：废条之「替」（显书·覆写）＞据中
    「法用#<号>」与废条之「法」＞裸字之号（後备：⛔为更长之号之一段〔段序 ⊂ 段序之守〕、⛔为审计之名〔前接四位之日「1027 执行之审」、
    後接「 #<数>」「·线」〕）；只归「法」——待未施行，无从替旧。
  ②设定/方法账.md 之行（表行与文行）凡含「法用#<号>」者归其法——判、所废、较旧（＝为何更好）俱摘。
  ③设定/方法坑账.json 之坑：〔以号〕文含「法用#<号>」；〔以名〕法与废之号裸见於文（同①之後备之律）；〔以守器〕坑之「守」与法之
    证器相交——⛔枢纽之器（≥3 法之证直引：封版、自走、全测……；.claude/settings.json 为诸钩之壳，凡带钩之证俱算其引）、
    ⛔只出自权限串之器（钩 Bash(python3 …/X.py:*)·于 permissions）。
    待之坑只认「法用#<号>」（1119 复核：裸字与守器二路之噪，248 归属 218 出自守器、待「执行之审」以审计之名白得 27 替）。
  ④git 之史（HEAD）：提交说明带「法用#<号>」者入其法之「历次之进」（sha12·日·首行·所改之档）；法之证器另列其 git 之笔数、
    首立与末三——其数＝git log -- <档>（默认之 TREESAME 简化於内存再演：并之笔与某亲同即只循其亲，旁枝之笔被剪者⛔算；
    1119 复核：旧数＝非并之全史＋--cc 之并，与所注之令不合）。三回 git log 取全（主史、并之首亲差、并之 -c 差；⛔逐笔起子进程）。
  ⑤.github/workflows/*.yml 每档一节（GitHub 之枝）：其史（笔数、首立、末五）、所调之 工具/*.py、所系之法、所守之坑。
  ⑥进化链只引其档名一行（⛔重抄；其数随 进化链.py 每跑而变，⛔引——免二谱相缠之假红）。
  ⛔谱里⛔带每跑必变之物：除「截至 <sha12>」一行外，同盘同史之再生逐字同。git 所出之行俱带「⎇」，余俱出自三账。
验（--验·零 token·供全测）：①档在；②法用册「法」「待」「废」每号俱有其节；③非 git 之部（不带 ⎇ 之行）与今盘三账再生之果逐字同——
  不同即红「进化树未随：跑 python3 工具/进化树.py --写」；④git 之部：「截至」之笔须为 HEAD 之祖，且以其笔之史再生之 ⎇ 行逐字同（手改、
  器改而未重写即红）；其後之提交带「法用#」者只印 ⚠「待下回 --写 入谱」（⛔红：提交本身不入其自身之谱，免自指之死结）；
  浅克隆（git rev-parse --is-shallow-repository 为 true）则 ④ 跳过并印一句（③ 红时示「先 git fetch --unshallow 再 --写」）。
并（--并·1119 复核：两枝各 --写 → 第 3 行「截至」俱改 → git merge 必冲突，GitHub 之闸「败·merge」）：并中（MERGE_HEAD 在）而冲突之档
  唯 设定/进化树.md 者，以今盘（已并之三账）与 HEAD（并之首亲）之史重写谱并 git add——截至＝首亲，为并後之笔之祖，④ 照成；
  另有冲突之档即 rc 1、⛔动。调者续 git commit --no-edit（gate.yml 之 bei_hou、autopush 之并步宜接之；其段见方法账）。
随（--随·钩与封版之自动用）：谱之账之部旧、缺节、截至非 HEAD 之祖（--验 红）方 --写，⛔则不动——免每回改「截至」行而生并之冲突。
改一法之式（自 1119 起）：提交说明带「法用#<号>」（其差即「具体改了何处」，GitHub 永存）；方法账一行书「所废」与「较旧：效…；费…」
  （为何更好·⛔倒车：新不胜旧⛔取）；坑入方法坑账——谱自聚，跑 --写 即新。
用法：
  python3 工具/进化树.py --写          # 生成 设定/进化树.md（截至 HEAD）
  python3 工具/进化树.py --随          # --验 红方 --写（钩、封版 --後、推.py 之自动用）
  python3 工具/进化树.py --并          # 并中冲突唯谱者：重写谱并 git add（续 git commit --no-edit）
  python3 工具/进化树.py --印          # 印到屏，⛔写（浅克隆：只印账之部，首行 ⚠）
  python3 工具/进化树.py --法 <号>     # 只印一法（法／待／废）之线（浅克隆同上）
  python3 工具/进化树.py --验          # 零 token 之验（全测之格）：rc 0 绿｜1 红
  python3 工具/进化树.py --自测        # tempfile 造小仓自测，印「进化树·自测 N/N」
  （--根 <仓>：换仓之根，自测与演用；默 本仓）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, subprocess, tempfile, shutil, unicodedata, fnmatch, time, io, contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
册名 = os.path.join('设定', '法用册.json')
法账名 = os.path.join('设定', '方法账.md')
坑账名 = os.path.join('设定', '方法坑账.json')
谱名 = os.path.join('设定', '进化树.md')
链名 = '设定/进化链.md'
流目 = '.github/workflows'
标 = '⎇'                     # git 所出之行之记（--验 以之分 git 之部与账之部）
首行 = ('> 本档由 工具/进化树.py --写 生成，⛔手改；改一法之式：提交说明带「法用#<号>」、方法账一行书「所废」与「较旧：效…；费…」、'
      '坑入方法坑账——谱自聚')
截式 = re.compile(r'^截至 `?([0-9a-f]{7,40})`?')
笔之档限 = 12                 # 一笔所改之档逾此即列前若干并书余数
器之末 = 3                    # 证器之史：末三笔
流之末 = 5                    # GitHub 之枝：末五笔
枢限 = 3                      # 枢纽之器：≥ 此数之法（法、待）之证直引者——坑之守器一路⛔认
_定库之变 = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY',
          'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_NAMESPACE', 'GIT_PREFIX', 'GIT_QUARANTINE_PATH')


# ═══ git ═══
def _env(加=None):
    """⛔承外之 GIT_DIR 诸变（pre-push 之钩中跑全测即带之）——库只由 根 定（同 推报._git、封版）。"""
    e = {k: v for k, v in os.environ.items() if k not in _定库之变}
    e.update(加 or {})
    return e


def _git(根, *a, 入=None, 加=None):
    """→ (rc, 出, 误)；utf-8、core.quotepath=off（汉字之路⛔转义）。"""
    try:
        r = subprocess.run(['git', '-C', 根, '-c', 'core.quotepath=off'] + list(a), input=入, capture_output=True,
                           env=_env(加), timeout=120)
    except Exception as ex:
        return 1, '', str(ex)
    return r.returncode, r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace')


def 浅否(根):
    rc, o, _ = _git(根, 'rev-parse', '--is-shallow-repository')
    return rc == 0 and o.strip() == 'true'


def 头(根):
    rc, o, e = _git(根, 'rev-parse', '--verify', 'HEAD^{commit}')
    if rc != 0:
        raise RuntimeError('HEAD 不可解：%s' % e.strip()[:120])
    return o.strip()


def _并差(根, 至, 式):
    """并之笔之差：{sha: set(档)}（式：first-parent＝与首亲之差；combined＝与诸亲俱异之档〔-c〕）。"""
    rc, o, e = _git(根, 'log', '--merges', '--no-renames', '--diff-merges=' + 式, '--name-only', '--format=%x1e%H%x1d', 至)
    if rc != 0:
        raise RuntimeError('git log --merges 败：%s' % e.strip()[:160])
    出 = {}
    for 录 in o.split('\x1e')[1:]:
        h, _, 名 = 录.partition('\x1d')
        出[h.strip()] = set(x for x in 名.split('\n') if x.strip())
    return 出


def 读史(根, 至):
    """三回 git log 取 至 之全史（新→旧）：笔 [(sha, 日, 亲数, 说明, [档])]、亲 [[亲之序]]、并之首亲差与俱异差；
    并取 至 之树之 workflows：[(路, 文)]。
    --cc：并之笔所列之档（谱之「所改之档」）只取与诸亲俱异而非照取一亲者；--no-renames：⛔改名之判（⛔读 blob·省取之仓亦速）。
    首亲差、俱异差（-c）供 _简 再演 git log -- <档> 之 TREESAME 简化（笔数与所注之令相合）。"""
    rc, o, e = _git(根, 'log', '--no-renames', '--cc', '--name-only', '--date=short',
                    '--format=%x1e%H%x1f%ad%x1f%P%x1f%B%x1d', 至)
    if rc != 0:
        raise RuntimeError('git log 败：%s' % e.strip()[:160])
    笔, 亲们 = [], []
    for 录 in o.split('\x1e')[1:]:
        前, _, 名 = 录.rpartition('\x1d')
        h, 日, 亲, 文 = 前.split('\x1f', 3)
        笔.append((h, 日, len(亲.split()), 文.strip('\n'), [x for x in 名.split('\n') if x.strip()]))
        亲们.append(亲.split())
    序 = {c[0]: j for j, c in enumerate(笔)}
    亲 = [[序[p] for p in ps if p in 序] for ps in 亲们]
    首差 = 俱异 = {}
    if any(len(ps) > 1 for ps in 亲们):
        首差, 俱异 = _并差(根, 至, 'first-parent'), _并差(根, 至, 'combined')
    rc, o, e = _git(根, 'ls-tree', '-r', '--name-only', 至, '--', 流目)
    路们 = sorted(x for x in o.split('\n') if x.endswith(('.yml', '.yaml'))) if rc == 0 else []
    流 = []
    if 路们:
        try:
            r = subprocess.run(['git', '-C', 根, 'cat-file', '--batch'], input=''.join('%s:%s\n' % (至, p) for p in 路们).encode('utf-8'),
                               capture_output=True, env=_env(), timeout=60)
            b, i = r.stdout, 0
            for p in 路们:
                j = b.index(b'\n', i)
                hd = b[i:j].split()
                if len(hd) < 3 or hd[1] != b'blob':
                    流.append((p, '')); i = j + 1; continue
                n = int(hd[2])
                流.append((p, b[j + 1:j + 1 + n].decode('utf-8', 'replace')))
                i = j + 1 + n + 1
        except Exception as ex:
            raise RuntimeError('workflows 读败：%s' % ex)
    return {'sha': 至, '笔': 笔, '流': 流, '亲': 亲, '首差': 首差, '俱异': 俱异}


def _简(h, 档们):
    """git log -- <档>（默认之史之简化）於内存再演 → {档: [笔之序（新→旧）]}——⛔逐档起子进程。
    自 至 起行：非并之笔改此档即入、循其亲；并之笔与首亲同（首亲差无此档）→ 只循首亲、⛔入；⛔则与次亲同（俱异差无此档）→
    只循次亲、⛔入；与诸亲俱异 → 入而循诸亲（git 之 TREESAME：取首个同之亲、剪余枝）。此仓无章鱼之并（三亲以上）——若有，
    「与某非首之亲同」只循次亲，近似之。"""
    笔, 亲, 首差, 俱异 = h['笔'], h['亲'], h['首差'], h['俱异']
    n = len(笔)
    要 = set(档们)
    触 = {p: set() for p in 要}
    for j, c in enumerate(笔):
        if len(亲[j]) <= 1:
            for p in c[4]:
                if p in 要:
                    触[p].add(j)
    出 = {}
    for p in 要:
        见 = bytearray(n)
        栈 = [0] if n else []
        入 = []
        t = 触[p]
        while 栈:
            j = 栈.pop()
            if 见[j]:
                continue
            见[j] = 1
            ps = 亲[j]
            if len(ps) <= 1:
                if j in t:
                    入.append(j)
                栈.extend(ps)
                continue
            sha = 笔[j][0]
            if p not in 首差.get(sha, ()):
                栈.append(ps[0])
            elif p not in 俱异.get(sha, ()):
                栈.append(ps[1])
            else:
                入.append(j)
                栈.extend(ps)
        if 入:
            出[p] = sorted(入)
    return 出


# ═══ 账 ═══
def 平(s):
    """一行之文：去换行、并空白；⛔带 git 之记（账之文万一含之即改书）。"""
    if s is None:
        return ''
    if not isinstance(s, str):
        s = json.dumps(s, ensure_ascii=False)
    return re.sub(r'\s+', ' ', s).strip().replace(标, '(git)')


def 截(s, n):
    """⛔无声截断：截即书其余数。"""
    s = 平(s)
    return s if len(s) <= n else s[:n] + '…（余 %d 字）' % (len(s) - n)


def _文(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return '\n'.join(_文(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return '\n'.join(_文(v) for v in x)
    return '' if x is None else str(x)


def 号们(文, 序):
    """文中「法用#<号>」之号（册中之号·取最长者·依首见之序）。"""
    出, i = [], 文.find('法用#')
    while i >= 0:
        后 = 文[i + 3:i + 3 + 80]
        for x in 序:
            if 后.startswith(x):
                if x not in 出:
                    出.append(x)
                break
        i = 文.find('法用#', i + 3)
    return 出


def _器名(x):
    x = x.strip()
    return x if '/' in x else '工具/' + x


def _证之迹(e, 出, 器, 直=None):
    """证 → 述之条（出）与器档（器：工具/、.github/、.claude/ 下⛔带占位与通配之实路）；直：其中非只出自权限串者
    （钩 Bash(python3 …/X.py:*)·于 permissions 只是预授其跑，⛔其法之器——坑之守器一路⛔认之）。"""
    if 直 is None:
        直 = []
    if isinstance(e, list):
        for x in e:
            _证之迹(x, 出, 器, 直)
        return
    if not isinstance(e, dict):
        return

    def 收器(p, 权=False):
        if isinstance(p, str) and p.startswith(('工具/', '.github/', '.claude/')) and not re.search(r'[{}*?\[]', p):
            if p not in 器:
                器.append(p)
            if not 权 and p not in 直:
                直.append(p)
    档 = e.get('档')
    档们 = [档] if isinstance(档, str) else (档 if isinstance(档, list) else [])
    g = e.get('git')
    if g:
        if g == '枝':
            出.append('git 枝 %s' % e.get('枝', ''))
        elif g == '改':
            出.append('git 改 %s' % '、'.join(档们))
        elif g == '含':
            出.append('git 含 %s→%s' % (e.get('甲', ''), e.get('乙', '')))
        else:
            出.append('git %s' % g)
    else:
        for x in 档们:
            出.append('档 %s%s' % (x, '（须不在）' if e.get('不') else ''))
    for x in 档们:
        收器(x)
    if '跑' in e:
        出.append('跑 %s' % _器名(e['跑']))
        收器(_器名(e['跑']))
    if '钩' in e:
        出.append('钩 %s：%s' % (e.get('于', ''), e['钩']))
        权 = e.get('于') == 'permissions' or str(e['钩']).lstrip().startswith('Bash(')
        for m in re.finditer(r'(?:工具/)?([^\s/()\'"`:]+\.py)', str(e['钩'])):
            收器('工具/' + m.group(1), 权)
    if '报' in e:
        出.append('报 %s' % e['报'])
    if '量' in e:
        出.append('量 %s' % e['量'])
    if '账' in e:
        出.append('账 %s' % e['账'])
    if '或' in e:
        支 = []
        for x in (e['或'] if isinstance(e['或'], list) else [e['或']]):
            子 = []
            _证之迹(x, 子, 器, 直)
            支.append('、'.join(子) or '—')
        出.append('或〔%s〕' % '｜'.join(支))
    if '若' in e or '则' in e:
        若, 则 = [], []
        _证之迹(e.get('若'), 若, 器, 直)
        _证之迹(e.get('则'), 则, 器, 直)
        出.append('若〔%s〕则〔%s〕' % ('、'.join(若) or '—', '、'.join(则) or '—'))


def 读账(根):
    """三账（法用册、方法账、方法坑账）→ 谱之账之部所需（零 git）。"""
    册 = json.load(open(os.path.join(根, 册名), encoding='utf-8'))
    p = os.path.join(根, 法账名)
    账文 = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    p = os.path.join(根, 坑账名)
    坑 = (json.load(open(p, encoding='utf-8')).get('坑') or []) if os.path.exists(p) else []
    a = {'法': list(册.get('法') or []), '待': list(册.get('待') or []), '废': list(册.get('废') or []), '坑': 坑}
    a['类'], a['条'] = {}, {}
    for k in ('法', '待', '废'):
        for x in a[k]:
            a['类'][x['id']] = k
            a['条'][x['id']] = x
    a['序'] = sorted(a['条'], key=lambda x: (-len(x), x))
    a['长者'] = {x: [y for y in a['序'] if len(y) > len(x) and x in y] for x in a['条']}
    # 证之述与器（法、待）
    a['证述'], a['器'], 直 = {}, {}, {}
    for k in ('法', '待'):
        for x in a[k]:
            出, 器, 直器 = [], [], []
            _证之迹(x.get('证') or [], 出, 器, 直器)
            去重 = []
            for t in 出:
                if t not in 去重:
                    去重.append(t)
            a['证述'][x['id']], a['器'][x['id']], 直[x['id']] = 去重, 器, 直器
    # 枢纽之器：≥ 枢限 法（法、待）之证直引者——坑之守器一路⛔认（1119 复核：封版.py 一器归坑五十三）
    用 = {}
    for i, xs in 直.items():
        for p in set(xs) | ({'.claude/settings.json'} if any(t.startswith('钩 ') for t in a['证述'][i]) else set()):
            用[p] = 用.get(p, 0) + 1      # 钩之证俱住 .claude/settings.json——诸钩之壳，算其引
    a['枢纽'] = sorted(p for p, n in 用.items() if n >= 枢限)
    a['守器'] = {x['id']: [p for p in 直[x['id']] if 用[p] < 枢限] for x in a['法']}
    # 方法账之行
    a['账行'], 行入, 表头 = {}, set(), None
    行们 = 账文.split('\n')
    for i, 行 in enumerate(行们):
        s = 行.strip()
        if s.startswith('|') and i + 1 < len(行们) and re.match(r'^\|\s*:?-{3,}', 行们[i + 1].strip()):
            表头 = [c.strip() for c in s.strip('|').split('|')]
            continue
        if not s.startswith('|'):
            表头 = None
        for x in 号们(行, a['序']):
            a['账行'].setdefault(x, []).append((i + 1, 行, 表头 if s.startswith('|') else None))
            行入.add(i + 1)
    a['账行数'] = len(行入)
    # 所替：只归「法」（待未施行，无从替旧）。废之「替」（显书）＞据中「法用#号」与废之「法」＞裸字之号（後备·见 裸提及）
    a['所替'], a['替之者'] = {}, {}
    法号 = [y['id'] for y in a['法']]
    for f in a['废']:
        据 = 平(f.get('据'))
        显 = f.get('替')
        if 显 is not None:
            归 = [(x, '显替') for x in ([显] if isinstance(显, str) else list(显)) if a['类'].get(x) == '法']
        else:
            归 = [(x, '法用#') for x in 号们(据, a['序']) if a['类'].get(x) == '法']
            if a['类'].get(f.get('法')) == '法' and f['法'] not in [y for y, _ in 归]:
                归.append((f['法'], '废之法'))
            if not 归:
                归 = [(x, '以字') for x in 法号 if 裸提及(据, x, a['长者'][x])]
        for x, 由 in 归:
            a['所替'].setdefault(x, []).append((f, 由))
        a['替之者'][f['id']] = [x for x, _ in 归]
    # 坑之归：以号（「法用#号」）、以名（法与废之号裸见·同 裸提及 之律）、以守器（法之直器 ∩ 守，⛔枢纽）；待只认以号
    a['坑归'], 坑入 = {}, set()
    for k in a['坑']:
        文 = _文(k)
        显 = set(号们(文, a['序']))
        守 = set(x for x in (k.get('守') or []) if isinstance(x, str))
        for 类 in ('法', '待', '废'):
            for x in a[类]:
                i = x['id']
                由 = None
                if i in 显:
                    由 = '以号'
                elif 类 != '待' and 裸提及(文, i, a['长者'][i]):
                    由 = '以名'
                elif 类 == '法':
                    交 = [p for p in a['守器'][i] if p in 守]
                    if 交:
                        由 = '以守器 ' + '、'.join(交)
                if 由:
                    a['坑归'].setdefault(i, []).append((k, 由))
                    坑入.add(k.get('号'))
    a['坑入谱'] = len(坑入)
    return a


_审前 = re.compile(r'\d{4}\s?$')           # 「1027 执行之审」：前接四位之日＝一回审计之名
_审後 = re.compile(r'\s?#\d|·线')          # 「执行之审 #12」「执行之核·线B」：後接条号／线名＝审计之名


def 裸提及(文, x, 长者=()):
    """号 x 是否以裸字见於文（所替与坑之後备之配·1119 复核改：旧以裸子串配，「1027 执行之审 #1」白归待「执行之审」二十七条）：
    逐处察——⛔为更长之号之一段（「段序」在「段序之守」中）、⛔为审计之名（前接四位之日，或後接「 #<数>」「·线」）；
    「法用#」後之号由 号们 判（此⛔重认）。"""
    i = 文.find(x)
    while i >= 0:
        ok = True
        for y in 长者:
            k = y.find(x)
            while k >= 0:
                if i - k >= 0 and 文[i - k:i - k + len(y)] == y:
                    ok = False
                    break
                k = y.find(x, k + 1)
            if not ok:
                break
        if ok and (_审前.search(文[max(0, i - 6):i]) or _审後.match(文, i + len(x))):
            ok = False
        if ok and 文[max(0, i - 3):i] == '法用#':
            ok = False
        if ok:
            return True
        i = 文.find(x, i + 1)
    return False


# ═══ 谱 ═══
def _题名(名, n=40):
    s = re.sub(r'[`*_\[\]<>|]', '', 平(名))
    return s if len(s) <= n else s[:n] + '…'


def _锚(题, 用):
    """GitHub 之标题锚（小写、去标点、空格→-；重者加 -1、-2）。"""
    s = ''.join(c for c in 题.lower()
                if c in ' -' or unicodedata.category(c)[0] in 'LM' or unicodedata.category(c) in ('Nd', 'Nl', 'Pc'))
    s = s.replace(' ', '-')
    n = 用.get(s, 0)
    用[s] = n + 1
    return s if n == 0 else '%s-%d' % (s, n)


def _史之索(a, h):
    """→ 号笔 {号: [笔之序（新→旧）]}、档笔 {档: [笔之序]}、入谱之笔数。"""
    号笔, 入 = {}, 0
    for j, c in enumerate(h['笔']):
        if '法用#' not in c[3]:
            continue
        xs = 号们(c[3], a['序'])
        if xs:
            入 += 1
        for x in xs:
            号笔.setdefault(x, []).append(j)
    要 = set(p for ps in a['器'].values() for p in ps) | set(p for p, _ in h['流'])
    return 号笔, _简(h, 要), 入


def _笔述(c, 列档=True):
    h, 日, 亲, 文, 档 = c
    s = '`%s` %s %s' % (h[:12], 日, 截(文.split('\n', 1)[0], 100))
    if not 列档:
        return s
    if not 档:
        return s + ('｜并之笔' if 亲 > 1 else '｜无改之档')
    余 = len(档) - 笔之档限
    return s + '｜改 %d 档：%s%s' % (len(档), '、'.join(档[:笔之档限]), '（余 %d 档）' % 余 if 余 > 0 else '')


def _器史述(h, 档笔, p):
    js = 档笔.get(p, [])
    if not js:
        return '0 笔（截至之史未见此档）'
    n = len(js)
    s = '%d 笔' % n
    if n > 器之末:
        s += '；首立 %s' % _笔述(h['笔'][js[-1]], False)
    末 = [h['笔'][j] for j in js[:器之末]][::-1]
    s += '；末%s（旧→新）：%s' % ('三' if 器之末 == 3 else 器之末, '；'.join(_笔述(c, False) for c in 末))
    余 = n - len(末)
    s += '（%s全史见 git log -- %s）' % ('余 %d 笔·' % 余 if 余 > 0 else '', p)
    return s


def _账行述(行号, 行, 头):
    s = 行.strip()
    所废 = re.search(r'所废[：:]\s*(.*?)(?=[；;。]?\s*较旧[：:]|\s\|\s|\s*\|\s*$|$)', s)
    较旧 = re.search(r'较旧[：:]\s*(.*?)(?=\s\|\s|\s*\|\s*$|$)', s)
    if s.startswith('|'):
        格 = [c.strip() for c in s.strip('|').split('|')]

        def 取(名, 默):
            """依表头取格：格数 ≥ 表头（格中或带「|」）即自尾数，⛔则自首数；表头无此名即默。"""
            if not 头 or 名 not in 头:
                return 默
            k = 头.index(名)
            if len(格) >= len(头):
                return 格[len(格) - (len(头) - k)]
            return 格[k] if k < len(格) else ''
        件 = 格[0] if 格 else ''
        判 = 取('判', 格[-1] if len(格) > 1 else '')
        日 = 取('日', '')
        段 = ['L%d「%s」' % (行号, 截(re.sub(r'\*\*', '', 件), 60))]
        if 日:
            段.append('日 %s' % 截(日, 12))
        段.append('判 %s' % (截(re.sub(r'\*\*', '', 判), 60) or '（未书）'))
    else:
        段 = ['L%d %s' % (行号, 截(s, 160))]
    段.append('所废：%s' % (截(所废.group(1), 120) if 所废 and 所废.group(1).strip() else '（未书）'))
    段.append('较旧：%s' % (截(较旧.group(1), 160) if 较旧 and 较旧.group(1).strip() else '（未书）'))
    return '｜'.join(段)


def _坑述(k, 由):
    s = '坑#%s %s｜治：%s｜守：%s｜%s' % (k.get('号'), 截(k.get('名'), 60), 截(k.get('治'), 100),
                                   '、'.join(k.get('守') or []) or '—', 平(k.get('状')) or '—')
    if k.get('复踩'):
        s += '·复踩 %d' % len(k['复踩'])
    return s + '〔%s〕' % 由


def _一节(a, h, 索, x, 类):
    i = x['id']
    L = ['### 法用#%s（%s）' % (i, _题名(x.get('名'))), '']
    if 类 == '法':
        L.append('- 根：据 %s；立第 %s 章；起第 %s 章' % (平(x.get('据')), x.get('立', '—'), x.get('起', '—')))
    elif 类 == '待':
        L.append('- 根：据 %s；限第 %s 章（待行之进化）' % (平(x.get('据')), x.get('限', '—')))
    else:
        L.append('- 根：据 %s' % 平(x.get('据')))
    if 类 == '废':
        替 = a['替之者'].get(i) or []
        L.append('- 废：废于 %s；在 `%s`（废前之提交）；替之者：%s' % (平(x.get('废于')), 平(x.get('在')),
                                                         '、'.join('法用#' + y for y in 替) or '—'))
        L.append('- 旧之形：%s' % 平(x.get('名')))
        去 = []
        for e in x.get('去证') or []:
            for k2, v in e.items():
                if k2 == '于':
                    continue
                去.append('%s %s%s' % (k2, 平(v), ('（于 %s）' % '、'.join(e['于']) if isinstance(e.get('于'), list)
                                                 else ('（于 %s）' % e['于'] if e.get('于') else ''))))
        L.append('- 去证：%s' % ('；'.join(去) or '—'))
        if h is not None:
            在 = 平(x.get('在'))
            c = next((c for c in h['笔'] if 在 and c[0].startswith(在)), None) if re.fullmatch(r'[0-9a-f]{7,40}', 在) else None
            L.append('- %s 在之笔：%s' % (标, _笔述(c, False) if c else '截至之史未见 `%s`' % 在))
    else:
        L.append('- 今之形：%s' % 平(x.get('名')))
        if 类 == '法':
            行 = ['时 %s' % 平(x.get('时')), '功 %s' % 平(x.get('功')), '处 %s' % 平(x.get('处')),
                 '流程 %s' % ('是' if x.get('流程') else '否')]
            if x.get('演免'):
                行.append('演免：%s' % 平(x['演免']))
            if x.get('演'):
                行.append('演：%s' % 平(x['演']))
            if x.get('钩自跑'):
                行.append('钩自跑：%s' % 平(x['钩自跑']))
            if x.get('量'):
                行.append('量：%s' % 平(x['量']))
            L.append('  - ' + '｜'.join(行))
        证 = a['证述'].get(i) or []
        if x.get('机证不能'):
            L.append('  - 证：机证不能——%s' % 平(x.get('由')))
        L.append('  - 证之档：%s' % ('；'.join(平(t) for t in 证) or '—'))
        if x.get('示'):
            L.append('  - 示：%s' % 平(x['示']))
        for y in x.get('互补') or []:
            L.append('  - 互补：与 法用#%s——%s' % (平(y.get('与')), 平(y.get('由'))))
    # git 之部
    if h is not None:
        号笔, 档笔, _ = 索
        js = 号笔.get(i, [])
        if js:
            L.append('- %s 历次之进（%d 笔·旧→新；每笔之全差：git show <sha>）：' % (标, len(js)))
            for j in reversed(js):
                L.append('  - %s %s' % (标, _笔述(h['笔'][j])))
        elif 类 != '废':
            L.append('- %s 历次之进：无（截至之史未见提交说明带「法用#%s」——自 1119 起改此法之提交须带之）' % (标, i))
        if 类 != '废':
            器 = a['器'].get(i) or []
            if 器:
                L.append('- %s 证器之史：' % 标)
                for p in 器:
                    L.append('  - %s %s：%s' % (标, p, _器史述(h, 档笔, p)))
    # 方法账
    rows = a['账行'].get(i, [])
    if rows:
        L.append('- 方法账之录（%d 行·判、所废、较旧＝为何更好）：' % len(rows))
        for 行号, 行, 头_ in rows:
            L.append('  - ' + _账行述(行号, 行, 头_))
    elif 类 != '废':
        L.append('- 方法账之录：无（设定/方法账.md 未见「法用#%s」）' % i)
    # 所替
    if 类 != '废':
        替 = a['所替'].get(i, [])
        if 替:
            L.append('- 所替（%d·已废之旧枝）：' % len(替))
            for f, 由 in 替:
                L.append('  - 法用#%s（废于 %s·在 `%s`）：%s〔%s〕' % (f['id'], 平(f.get('废于')), 平(f.get('在')), 截(f.get('名'), 80), 由))
        elif 类 == '法':
            L.append('- 所替：无')
    # 坑
    ks = a['坑归'].get(i, [])
    if ks:
        L.append('- 踩过之坑（%d）：' % len(ks))
        for k, 由 in ks:
            L.append('  - ' + _坑述(k, 由))
    elif 类 != '废':
        L.append('- 踩过之坑：无')
    L.append('')
    return L


def _流节(a, h, 索, p, 文):
    号笔, 档笔, _ = 索
    js = 档笔.get(p, [])
    L = ['### %s %s' % (标, p), '']
    if js:
        L.append('- %s 史：%d 笔（全史见 git log -- %s）；首立 %s' % (标, len(js), p, _笔述(h['笔'][js[-1]], False)))
        末 = js[:流之末][::-1]
        余 = len(js) - len(末)
        L.append('- %s 末五（旧→新%s）：' % (标, '；余 %d 笔见 git log' % 余 if 余 > 0 else ''))
        for j in 末:
            L.append('  - %s %s' % (标, _笔述(h['笔'][j])))
    else:
        L.append('- %s 史：0 笔（截至之史未见此档）' % 标)
    器 = sorted(set(re.findall(r'python3\s+(?:-[A-Za-z]+\s+)*(工具/[^\s"\'`;|&()<>]+\.py)', 文)))
    L.append('- %s 所调之器（%d）：%s' % (标, len(器), '、'.join(器) or '—'))
    系 = [x['id'] for x in a['法'] + a['待']
         if any(isinstance(t, str) and fnmatch.fnmatch(p, t) for t in _档们(x.get('证')))]
    L.append('- %s 所系之法：%s' % (标, '、'.join('法用#' + y for y in 系) or '—'))
    坑 = [k for k in a['坑'] if p in (k.get('守') or [])]
    L.append('- %s 所守之坑：%s' % (标, '、'.join('坑#%s %s' % (k.get('号'), 截(k.get('名'), 30)) for k in 坑) or '—'))
    L.append('')
    return L


def _档们(e):
    出 = []
    if isinstance(e, list):
        for x in e:
            出 += _档们(x)
    elif isinstance(e, dict):
        v = e.get('档')
        出 += [v] if isinstance(v, str) else (v if isinstance(v, list) else [])
        for k in ('或', '若', '则'):
            if k in e:
                出 += _档们(e[k])
    return 出


def 生(a, h):
    """三账（a）与史（h；None 即只生账之部）→ 谱之行。git 所出之行俱带「⎇」，余⛔带。"""
    索 = _史之索(a, h) if h is not None else None
    体, 用 = [], {}
    _锚('目录', 用)
    段们 = [('一、现行之法（%d）' % len(a['法']), '法'), ('二、待（待行之进化·%d）' % len(a['待']), '待'),
          ('三、已废之枝（%d）' % len(a['废']), '废')]
    录 = []
    for 题, 类 in 段们:
        锚 = _锚(题, 用)
        体 += ['## ' + 题, '']
        if 类 == '废':
            体 += ['> 废之法：其废前之形在「在」之笔（git show <在>），其所替之今法见「替之者」；去证＝废後须已除尽之迹。', '']
        项 = []
        for x in a[类]:
            节 = _一节(a, h, 索, x, 类)
            项.append('[%s](#%s)' % (x['id'], _锚(节[0][4:], 用)))
            体 += 节
        录.append('- [%s](#%s)：%s' % (题, 锚, ' · '.join(项) or '—'))
    if h is not None:
        题 = '四、GitHub 之枝（.github/workflows·%s %d）' % (标, len(h['流']))
        锚 = _锚(题, 用)
        体 += ['## ' + 题, '',
               '> %s GitHub 上之程序与沙盒之法同入进化树、同守「改须更胜从前」（1119 作者令）——每枝之进化即其笔，全差 git show <sha>。' % 标, '']
        项 = []
        for p, 文 in h['流']:
            节 = _流节(a, h, 索, p, 文)
            项.append('[%s](#%s)' % (os.path.basename(p), _锚(节[0][4:], 用)))
            体 += 节
        录.append('- %s [%s](#%s)：%s' % (标, 题, 锚, ' · '.join(项) or '—'))
    头行 = [首行, '']
    if h is not None:
        头行 += ['截至 `%s`（HEAD 之史；带 %s 之行俱出自 git 至此笔，其後之笔待下回 --写）' % (h['sha'][:12], 标), '']
    无进 = None
    if h is not None:
        无进 = sum(1 for x in a['法'] if x['id'] not in 索[0])
    头行 += ['总计：法 %d、待 %d、废 %d（设定/法用册.json）；方法账入谱之行 %d（带「法用#<号>」者）；方法坑账 %d 坑、入谱 %d'
             % (len(a['法']), len(a['待']), len(a['废']), a['账行数'], len(a['坑']), a['坑入谱']), '']
    if h is not None:
        头行 += ['%s 总计（git）：GitHub 之枝 %d、已入谱之进化提交 %d（提交说明带「法用#<号>」而号在册者）；历次之进尚空之法 %d'
                 % (标, len(h['流']), 索[2], 无进), '']
    头行 += ['> 读法：每法一节——**根**（何处立、何章起）→ **今之形** → %s **历次之进**（提交说明带「法用#<号>」之笔，旧→新；所改之档即「具体修改了什么地方」，'
             '全差 `git show <sha>`）→ %s **证器之史** → **方法账之录**（判、所废、较旧＝「为什么会变得更好」）→ **所替**（已废之旧枝）→ **踩过之坑**。' % (标, 标),
             '> 源：设定/法用册.json（法／待／废）、设定/方法账.md、设定/方法坑账.json、git 之史与 .github/workflows（带 %s 之行）。'
             '犯过之错今有无器守，另见 %s（工具/进化链.py 自写·此⛔重抄）。' % (标, 链名),
             '> ⛔倒车：新不胜旧⛔取（总章心诀5）——方法账每行之「较旧」即其凭。', '',
             '## 目录', ''] + 录 + ['']
    return 头行 + 体


def _组(根, 至=None):
    a = 读账(根)
    h = 读史(根, 至 or 头(根))
    return a, h, 生(a, h)


def _谱路(根):
    return os.path.join(根, 谱名)


# ═══ 令 ═══
def 写(根=ROOT, 印=True):
    """生成 设定/进化树.md（截至 HEAD）。浅克隆⛔写（史不全）。→ rc。"""
    t0 = time.time()
    if 浅否(根):
        print('⛔ 进化树·写：浅克隆之史不全，⛔写（git fetch --unshallow 後再写）')
        return 1
    a, h, 行 = _组(根)
    文 = '\n'.join(行).rstrip('\n') + '\n'
    p = _谱路(根)
    旧 = open(p, encoding='utf-8').read() if os.path.exists(p) else None
    if 旧 != 文:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(文)
    if 印:
        索 = _史之索(a, h)
        print('进化树·写 ✓ %s（截至 %s；法 %d、待 %d、废 %d、GitHub 之枝 %d、入谱之进化提交 %d；%d 行、%.0f KB；%s；%.1f 秒）'
              % (谱名, h['sha'][:12], len(a['法']), len(a['待']), len(a['废']), len(h['流']), 索[2], len(行),
                 len(文.encode('utf-8')) / 1024.0, '已改' if 旧 != 文 else '未变', time.time() - t0))
    return 0


def 账之部(行们):
    """谱之账之部：去带 ⎇ 之行与截至之行，连空行并一、去首尾之空行（git 之行之去⛔留空行之差）。"""
    出 = []
    for x in 行们:
        if 标 in x or 截式.match(x):
            continue
        if x == '' and (not 出 or 出[-1] == ''):
            continue
        出.append(x)
    while 出 and 出[-1] == '':
        出.pop()
    return 出


def _首异(甲, 乙):
    for k in range(max(len(甲), len(乙))):
        x = 甲[k] if k < len(甲) else '（无）'
        y = 乙[k] if k < len(乙) else '（无）'
        if x != y:
            return '第 %d 条之异——档：%s｜应：%s' % (k + 1, 截(x, 70), 截(y, 70))
    return ''


def 验(根=ROOT):
    """零 token 之验（全测之格）：→ (ok, [印之行])。"""
    印 = []
    红 = []
    p = _谱路(根)
    if not os.path.exists(p):
        return False, ['  ⛔ ① 档不在：%s——跑 python3 工具/进化树.py --写' % 谱名]
    行 = open(p, encoding='utf-8').read().rstrip('\n').split('\n')
    截行 = [k for k, x in enumerate(行) if 截式.match(x)]
    if not 截行:
        return False, ['  ⛔ ① 档无「截至 <sha>」之行——跑 python3 工具/进化树.py --写']
    sha12 = 截式.match(行[截行[0]]).group(1)
    印.append('  ✓ ① 档在：%s（截至 %s）' % (谱名, sha12))
    try:
        a = 读账(根)
    except Exception as ex:
        return False, 印 + ['  ⛔ 三账读败：%s' % 截(str(ex), 120)]
    # ②
    有 = set(x for x in 行 if x.startswith('### 法用#'))
    缺 = [x['id'] for k in ('法', '待', '废') for x in a[k]
         if not any(y.startswith('### 法用#%s（' % x['id']) for y in 有)]
    if 缺:
        红.append('② 缺节 %d：%s' % (len(缺), '、'.join(缺[:8]) + ('…（余 %d）' % (len(缺) - 8) if len(缺) > 8 else '')))
        印.append('  ⛔ ' + 红[-1])
    else:
        印.append('  ✓ ② 节齐：法 %d、待 %d、废 %d 俱有其节' % (len(a['法']), len(a['待']), len(a['废'])))
    # ③ 账之部
    浅 = 浅否(根)
    档账 = 账之部([x for k, x in enumerate(行) if k not in 截行])
    应账 = 账之部(生(a, None))
    if 档账 != 应账:
        红.append('③ 进化树未随：%s（%s）' % ('浅克隆——先 git fetch --unshallow 再 python3 工具/进化树.py --写（--写 於浅克隆拒写）'
                                         if 浅 else '跑 python3 工具/进化树.py --写', _首异(档账, 应账)))
        印.append('  ⛔ ' + 红[-1])
    else:
        印.append('  ✓ ③ 账之部（法用册、方法账、坑账所出 %d 行）与今盘三账再生逐字同' % len(档账))
    # ④ git 之部
    if 浅:
        印.append('  · ④ 浅克隆（is-shallow-repository=true）：git 之部之验跳过（史不全·⛔判）')
    else:
        rc, o, _ = _git(根, 'rev-parse', '--verify', '%s^{commit}' % sha12)
        全 = o.strip()
        if rc != 0 or not 全:
            红.append('④ 截至之笔 %s 不在史' % sha12)
            印.append('  ⛔ ' + 红[-1])
        else:
            try:
                H = 头(根)
            except Exception as ex:
                H = ''
                红.append('④ %s' % ex)
                印.append('  ⛔ ' + 红[-1])
            if H:
                rc, _, _ = _git(根, 'merge-base', '--is-ancestor', 全, H)
                if rc != 0:
                    红.append('④ 截至之笔 %s 非 HEAD（%s）之祖——史已改写，跑 python3 工具/进化树.py --写' % (sha12, H[:12]))
                    印.append('  ⛔ ' + 红[-1])
                else:
                    try:
                        h = 读史(根, 全)
                        应全 = 生(a, h)
                    except Exception as ex:
                        h, 应全 = None, None
                        红.append('④ 再生败：%s' % 截(str(ex), 100))
                        印.append('  ⛔ ' + 红[-1])
                    if 应全 is not None:
                        while 应全 and not 应全[-1]:
                            应全.pop()
                        档全 = [x for k, x in enumerate(行) if k not in 截行]
                        应全2 = [x for x in 应全 if not 截式.match(x)]
                        if 档全 != 应全2 and 档账 == 应账:
                            红.append('④ git 之部与截至之笔之史再生不同（手改、或器已改而谱未重写）：跑 python3 工具/进化树.py --写（%s）'
                                     % _首异([x for x in 档全 if 标 in x], [x for x in 应全2 if 标 in x]))
                            印.append('  ⛔ ' + 红[-1])
                        elif 档全 == 应全2:
                            印.append('  ✓ ④ 截至之笔为 HEAD 之祖；git 之部（%d 行）与其史再生逐字同' % sum(1 for x in 档全 if 标 in x))
                        else:
                            印.append('  · ④ 截至之笔为 HEAD 之祖；git 之部之逐字对俟 ③ 治（--写）後再判')
                    rc, o, _ = _git(根, 'log', '--no-renames', '--name-only', '--format=%x1e%H%x1f%B%x1d', '%s..%s' % (全, H))
                    後 = []
                    for 录 in o.split('\x1e')[1:]:
                        前, _, 名 = 录.rpartition('\x1d')
                        hh, 文 = 前.split('\x1f', 1)
                        後.append((hh, 文, [x for x in 名.split('\n') if x.strip()]))
                    印.append('  · 截至之後 %d 笔' % len(後))
                    警 = []
                    for hh, 文, 档 in 後:
                        if '法用#' in 文:
                            xs = 号们(文, a['序'])
                            if xs:
                                警.append('  ⚠ `%s` 带 %s——待下回 --写 入谱' % (hh[:12], '、'.join('法用#' + x for x in xs)))
                            未 = [m.group(1) for m in re.finditer(r'法用#([^\s）)、，,；;。·｜|」』】\]：:]*)', 文)
                                 if not any(m.group(1).startswith(x) for x in a['序']) and m.group(1) not in ('', 'id', '<id>', '<号>')]
                            if 未:
                                警.append('  ⚠ `%s` 带号不在册：%s（错字？）' % (hh[:12], '、'.join('法用#' + 截(x, 20) for x in 未[:3])))
                        if any(x.startswith(流目 + '/') for x in 档):
                            警.append('  ⚠ `%s` 改 GitHub 之枝——待下回 --写 入谱' % hh[:12])
                    印 += 警[:8] + (['  ⚠ …余 %d 条（python3 工具/进化树.py --写 即俱入谱）' % (len(警) - 8)] if len(警) > 8 else [])
    return (not 红), 印


浅警 = '⚠ 浅克隆（is-shallow-repository=true）：git 之史不全——%s 之行（历次之进、证器之史、GitHub 之枝）⛔印，只印账之部；git fetch --unshallow 後再看' % 标


def _印组(根):
    """--印、--法 之组：浅克隆⛔以残史生 ⎇ 之行（1119 复核：浅克隆下 --法 印「历次之进：无」而真史有八笔，rc 0 无声）——只生账之部。
    → (a, h|None, 行)。"""
    if 浅否(根):
        a = 读账(根)
        return a, None, 生(a, None)
    return _组(根)


def 一线(根, 号):
    a, h, 行 = _印组(根)
    起 = next((k for k, x in enumerate(行) if x.startswith('### 法用#%s（' % 号)), None)
    if 起 is None:
        近 = [x for x in a['条'] if 号 in x or x in 号][:8]
        print('⛔ 册无号「%s」%s' % (号, ('；近者：' + '、'.join(近)) if 近 else ''))
        return 1
    终 = next((k for k in range(起 + 1, len(行)) if 行[k].startswith(('### ', '## '))), len(行))
    if h is None:
        print(浅警)
    print('（%s 之线·截至 %s）' % (a['类'][号], h['sha'][:12] if h is not None else '—（浅克隆·无 git 之部）'))
    print('\n'.join(行[起:终]).rstrip('\n'))
    return 0


def 随(根=ROOT):
    """钩、封版 --後、推.py 之自动用：--验 红（谱之账之部旧、缺节、截至非 HEAD 之祖、git 之部被手改）方 --写，⛔则不动
    （1119 复核：每回 --写 必改第 3 行「截至」——两枝各写，git merge 即冲突；只在须写时写，冲突之源少之）。→ rc。"""
    ok, 印 = 验(根)
    if ok:
        print('进化树·随 ✓ 未变（--验 绿：谱随三账、截至为 HEAD 之祖；其後之提交待下回须写时入谱）')
        return 0
    print('进化树·随：--验 红 → --写（%s）' % '；'.join(x.strip() for x in 印 if '⛔' in x)[:300])
    return 写(根)


def 并(根=ROOT):
    """并中之冲突唯谱者：以今盘（已并之三账）与 HEAD（并之首亲）之史重写谱、git add 之；调者续 git commit --no-edit。
    截至＝首亲 → 为并後之笔之祖，--验 ④ 照成；他档亦冲突即 rc 1、⛔动（⛔替人解他档之冲突）。"""
    谱 = 谱名.replace(os.sep, '/')
    if 浅否(根):
        print('⛔ 进化树·并：浅克隆之史不全，⛔写（git fetch --unshallow 後再并）')
        return 1
    rc, _, _ = _git(根, 'rev-parse', '-q', '--verify', 'MERGE_HEAD')
    if rc != 0:
        print('⛔ 进化树·并：无并在进行（MERGE_HEAD 不在）——平时用 --写／--随')
        return 1
    rc, o, e = _git(根, 'diff', '--name-only', '--diff-filter=U')
    if rc != 0:
        print('⛔ 进化树·并：git diff 败：%s' % 截(e, 120))
        return 1
    冲 = sorted(set(x for x in o.split('\n') if x.strip()))
    他 = [x for x in 冲 if x != 谱]
    if 他:
        print('⛔ 进化树·并：另有冲突之档 %d（%s）——⛔自解；手治或 git merge --abort'
              % (len(他), '、'.join(他[:5]) + ('…（余 %d）' % (len(他) - 5) if len(他) > 5 else '')))
        return 1
    rc = 写(根)
    if rc != 0:
        return rc
    rc, _, e = _git(根, 'add', '--', 谱)
    if rc != 0:
        print('⛔ 进化树·并：git add 败：%s' % 截(e, 120))
        return 1
    print('进化树·并 ✓ %s（截至 HEAD＝并之首亲·为并後之祖；冲突之档 %d）——续：git commit --no-edit'
          % ('谱之冲突已解' if 冲 else '无冲突·谱已依并後之账重写', len(冲)))
    return 0


# ═══ 自测 ═══
def 自测():
    t0 = time.time()
    果 = []

    def 判(名, ok, 说=''):
        果.append(bool(ok))
        print('  %s %s%s' % ('✓' if ok else '✗', 名, ('｜' + 说) if (说 and not ok) else ''))

    tmp = tempfile.mkdtemp(prefix='jinhuashu_')
    仓 = os.path.join(tmp, 'repo')
    try:
        for d in ('设定', '工具', '.github/workflows'):
            os.makedirs(os.path.join(仓, d))

        def g(*a, 根=仓, 加=None):
            rc, o, e = _git(根, *a, 加=加)
            if rc != 0:
                raise RuntimeError('git %s 败：%s' % (' '.join(a[:2]), e.strip()[:200]))
            return o.strip()

        def 书(路, 文):
            p = os.path.join(仓, 路)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(文)

        def 交(说, 日):
            g('add', '-A')
            g('commit', '-q', '-m', 说, 加={'GIT_AUTHOR_DATE': 日, 'GIT_COMMITTER_DATE': 日})
            return g('rev-parse', 'HEAD')

        g('init', '-q')
        g('config', 'user.name', '自测')
        g('config', 'user.email', 'zice@example.invalid')
        g('config', 'commit.gpgsign', 'false')
        g('config', 'core.hooksPath', os.path.join(tmp, '无钩'))
        册 = {'法': [{'id': '甲', '名': '甲之法：门前一守' + '长' * 50, '据': '据之甲', '立': 1, '起': 2, '时': '开', '功': '守门',
                     '处': '沙盒', '流程': False, '证': [{'档': '工具/门.py', '含': 'def 守'}, {'跑': '巡.py'}, {'档': '工具/枢.py'}]},
                    {'id': '乙', '名': '乙之法', '据': '据之乙', '立': 3, '起': 3, '时': '封後', '功': '记', '处': 'GitHub',
                     '流程': False, '证': [{'档': '.github/workflows/*.yml'}]},
                    {'id': '戊', '名': '戊之法', '据': '据之戊', '立': 4, '起': 4, '时': '开', '功': '枢', '处': '沙盒', '流程': False,
                     '证': [{'档': '工具/枢.py'}, {'钩': 'Bash(python3 ' + '工具/许.py:*)', '于': 'permissions'}]},
                    {'id': '己', '名': '己之法', '据': '据之己', '立': 4, '起': 4, '时': '开', '功': '枢', '处': '沙盒', '流程': False,
                     '证': [{'档': '工具/枢.py'}]}],
              '待': [{'id': '丙', '名': '丙之待', '据': '据之丙', '限': 9, '证': [{'档': '工具/丙器.py', '含': 'def 写'}]},
                    {'id': '甲审', '名': '甲审之待', '据': '据之待', '限': 9, '证': [{'档': '工具/审器.py'}]}],
              '废': [{'id': '丁旧', '名': '丁旧之法', '据': '法用#甲 立而旧法废', '废于': '1119', '在': '0000000', '去证': [{'无档': '工具/丁.py'}]},
                    {'id': '戊旧', '名': '戊旧之法', '据': '1027 甲审 #1 #12（一回审计之名）', '废于': '1027', '在': '0000000', '去证': []},
                    {'id': '己旧', '名': '己旧之法', '据': '1027 乙 #3；乙·线B', '废于': '1027', '在': '0000000', '去证': []},
                    {'id': '庚旧', '名': '庚旧之法', '据': '审·乙（B·新式）', '废于': '1027', '在': '0000000', '去证': []}]}
        书('设定/法用册.json', json.dumps(册, ensure_ascii=False, indent=1))
        书('设定/方法账.md', '# 方法账\n\n| 件 | 法 | 费 | 较旧 | 日 | 判 |\n|---|---|---|---|---|---|\n'
                         '| 甲之一进 | 所废：旧之门（法用#甲） | $0 | 较旧：效——升；费——平 | 1119 | 取 |\n\n'
                         '散行：乙之记（法用#乙）\n')
        书('设定/方法坑账.json', json.dumps({'坑': [
            {'号': 1, '名': '门开而未守（法用#甲 之坑）', '治': '加锁', '守': ['工具/锁.py'], '状': '已守', '复踩': []},
            {'号': 2, '名': '巡而不报', '治': '报之', '守': ['工具/巡.py'], '状': '已守', '复踩': [{'时': 'x'}]},
            {'号': 3, '名': '无关之坑', '治': '无', '守': ['工具/他.py', '.github/workflows/巡.yml'], '状': '已守', '复踩': []},
            {'号': 4, '名': '枢纽之坑', '治': '无', '守': ['工具/枢.py'], '状': '已守', '复踩': []},
            {'号': 5, '名': '预授之坑', '治': '无', '守': ['工具/许.py'], '状': '已守', '复踩': []},
            {'号': 6, '名': '审计之坑（1027 甲审 195 条）', '治': '无', '守': [], '状': '已守', '复踩': []},
            {'号': 7, '名': '待之坑（法用#甲审）', '治': '无', '守': [], '状': '未守', '复踩': []}]},
            ensure_ascii=False))
        书('工具/门.py', 'def 守():\n    pass\n')
        书('工具/巡.py', 'print(1)\n')
        书('.github/workflows/巡.yml', 'jobs:\n  a:\n    steps:\n      - run: python3 ' + '工具/巡.py --云\n      - run: python3 -u 工具/门.py\n')
        c0 = 交('立', '2026-11-01T00:00:00+00:00')
        书('工具/门.py', 'def 守():\n    return 1\n')
        c1 = 交('甲之进一：门守有返（法用#甲）', '2026-11-02T00:00:00+00:00')
        for k in range(14):
            书('工具/杂/%02d.txt' % k, str(k))
        书('工具/门.py', 'def 守():\n    return 2\n')
        c2 = 交('甲之进二·法用#甲·十五档', '2026-11-03T00:00:00+00:00')
        书('工具/门.py', 'def 守():\n    return 3\n')
        c3 = 交('杂改一', '2026-11-04T00:00:00+00:00')
        书('工具/门.py', 'def 守():\n    return 4\n')
        书('.github/workflows/巡.yml', 'jobs:\n  a:\n    steps:\n      - run: python3 ' + '工具/巡.py --云\n')
        c4 = 交('杂改二（巡.yml 亦改）', '2026-11-05T00:00:00+00:00')

        rc = 写(仓, 印=False)
        文 = open(_谱路(仓), encoding='utf-8').read()
        行 = 文.split('\n')

        def 节(号):
            k = next((i for i, x in enumerate(行) if x.startswith('### 法用#%s（' % 号)), None)
            if k is None:
                return ''
            e = next((i for i in range(k + 1, len(行)) if 行[i].startswith(('### ', '## '))), len(行))
            return '\n'.join(行[k:e])
        # ①
        判('① 节齐（法甲乙·待丙·废丁旧·GitHub 之枝巡.yml·首行之注·截至之行）',
           rc == 0 and all(节(x) for x in ('甲', '乙', '丙', '丁旧')) and '### %s .github/workflows/巡.yml' % 标 in 文
           and 行[0] == 首行 and any(截式.match(x) and c4[:12] in x for x in 行))
        甲 = 节('甲')
        # ②
        i1, i2 = 甲.find(c1[:12]), 甲.find(c2[:12])
        判('② 带「法用#甲」之二笔入甲之「历次之进」（旧→新）、⛔入乙；无号之笔⛔入',
           '历次之进（2 笔' in 甲 and 0 <= i1 < i2 and c1[:12] not in 节('乙') and ('`%s`' % c3[:12]) not in 甲.split('证器之史')[0],
           甲[:300])
        # ③
        判('③ 方法账之行归其法（表行带判、所废、较旧；散行归乙）',
           '「甲之一进」' in 甲 and '判 取' in 甲 and '所废：旧之门' in 甲 and '较旧：效——升；费——平' in 甲 and '日 1119' in 甲
           and 'L7 散行：乙之记' in 节('乙'))
        # ④
        判('④ 坑以号（坑#1〔以号〕）与以守器（坑#2〔以守器 工具/巡.py〕）两路俱归甲；无关之坑#3⛔归',
           '坑#1 ' in 甲 and '〔以号〕' in 甲 and '坑#2 ' in 甲 and '〔以守器 工具/巡.py〕' in 甲 and '坑#3 ' not in 甲
           and '所替（1' in 甲 and '法用#丁旧' in 甲)
        # ⑤
        ok0, 印0 = 验(仓)
        书('设定/方法账.md', open(os.path.join(仓, 法账名), encoding='utf-8').read() + '| 乙之一进 | 所废：无；较旧：效——同 法用#乙 | — | — | 1120 | 取 |\n')
        ok1, 印1 = 验(仓)
        写(仓, 印=False)
        ok2, 印2 = 验(仓)
        判('⑤ --验：写後绿；改账而未 --写 即红「进化树未随」；--写 後复绿',
           ok0 and (not ok1) and any('进化树未随' in x for x in 印1) and ok2, ' / '.join(印1[-2:]))
        # ⑥
        甲文 = open(_谱路(仓), encoding='utf-8').read()
        a = 读账(仓)
        h1 = 读史(仓, c4)
        s1 = '\n'.join(生(a, h1))
        os.environ['TZ'] = 'Pacific/Kiritimati'
        try:
            time.tzset()
        except Exception:
            pass
        s2 = '\n'.join(生(读账(仓), 读史(仓, c4)))
        os.environ.pop('TZ', None)
        try:
            time.tzset()
        except Exception:
            pass
        写(仓, 印=False)
        今 = time.strftime('%Y-%m-%d')
        账一 = 账之部(生(a, h1))
        账二 = 账之部(生(a, None))
        判('⑥ 再生逐字同（换时区再生同、再 --写 档不变、无今日之时刻；账之部与史无涉）',
           s1 == s2 and 甲文 == open(_谱路(仓), encoding='utf-8').read() and 今 not in 甲文.replace('2026-11-0', '') and 账一 == 账二)
        # ⑦ 浅克隆（谱入史：其提交带「法用#甲」——⑨ 用之）
        c5 = 交('谱入（法用#甲）', '2026-11-06T00:00:00+00:00')
        浅 = os.path.join(tmp, 'shallow')
        rc, o, e = _git(tmp, 'clone', '-q', '--depth', '1', 'file://' + 仓, 浅)
        okq, 印q = 验(浅) if rc == 0 else (False, [e])
        with open(os.path.join(浅, 法账名), 'a', encoding='utf-8') as f:
            f.write('| 又 | 法用#甲 | — | — | 1121 | 取 |\n')
        okq2, _ = 验(浅)
        判('⑦ 浅克隆：④ 跳过并印一句、⛔红；账之部照验（改账即红）',
           rc == 0 and 浅否(浅) and okq and any('浅克隆' in x for x in 印q) and not okq2, ' / '.join(印q))
        # ⑧
        判('⑧ 截断书余数（一笔逾十二档→「余 3 档」；器史逾三笔→「余 N 笔·全史见 git log -- 工具/门.py」；长名→「余 N 字」）',
           '（余 3 档）' in 甲 and re.search(r'余 \d+ 笔·全史见 git log -- 工具/门\.py', 甲) is not None and '首立 `%s`' % c0[:12] in 甲
           and '…（余 ' in 截('长' * 200, 10))
        # ⑨ 其後之提交带法用# 只⚠
        ok5, 印5 = 验(仓)
        判('⑨ 截至之後之提交带「法用#」只 ⚠「待下回 --写 入谱」、⛔红（免自指之死结）',
           ok5 and any('⚠' in x and c5[:12] in x and '待下回 --写' in x for x in 印5), ' / '.join(印5))
        # ⑩ 截至非 HEAD 之祖 → 红
        树 = g('rev-parse', 'HEAD^{tree}')
        野 = g('commit-tree', 树, '-m', '野笔', 加={'GIT_AUTHOR_DATE': '2026-11-07T00:00:00+00:00',
                                                  'GIT_COMMITTER_DATE': '2026-11-07T00:00:00+00:00'})
        原 = open(_谱路(仓), encoding='utf-8').read()
        with open(_谱路(仓), 'w', encoding='utf-8') as f:
            f.write(re.sub(r'(?m)^截至 `[0-9a-f]+`', '截至 `%s`' % 野[:12], 原))
        ok10, 印10 = 验(仓)
        with open(_谱路(仓), 'w', encoding='utf-8') as f:
            f.write(re.sub(r'(?m)^截至 `[0-9a-f]+`', '截至 `deadbeef0000`', 原))
        ok10b, _ = 验(仓)
        判('⑩ 截至之笔非 HEAD 之祖、或不在史 → 红', (not ok10) and any('非 HEAD' in x for x in 印10) and not ok10b)
        # ⑪ 手改 git 之部 → 红
        with open(_谱路(仓), 'w', encoding='utf-8') as f:
            f.write(原.replace('甲之进一：门守有返', '甲之进一：手改'))
        ok11, 印11 = 验(仓)
        with open(_谱路(仓), 'w', encoding='utf-8') as f:
            f.write(原)
        ok11b, _ = 验(仓)
        判('⑪ 手改 git 之部（⎇ 行）→ 红；复原即绿', (not ok11) and any('git 之部' in x and '⛔' in x for x in 印11) and ok11b)
        # ⑫ CLI：--验 之 rc、--法 只印一线、缺档即红
        跑 = lambda *x: subprocess.run([sys.executable, os.path.abspath(__file__)] + list(x) + ['--根', 仓],
                                       capture_output=True, env=_env(), timeout=120)
        r1 = 跑('--验')
        r2 = 跑('--法', '甲')
        o2 = r2.stdout.decode('utf-8', 'replace')
        os.rename(_谱路(仓), _谱路(仓) + '.藏')
        r3 = 跑('--验')
        os.rename(_谱路(仓) + '.藏', _谱路(仓))
        判('⑫ 令：--验 rc 0；--法 甲 只印甲之线；档缺即 rc 1',
           r1.returncode == 0 and r2.returncode == 0 and '### 法用#甲（' in o2 and '### 法用#乙（' not in o2 and r3.returncode == 1,
           r1.stdout.decode('utf-8', 'replace')[-200:])
        # ⑬ GitHub 之枝：所调之器、所系之法、末五
        流 = 文.split('### %s .github/workflows/巡.yml' % 标)[1] if ('### %s .github/workflows/巡.yml' % 标) in 文 else ''
        判('⑬ GitHub 之枝：史（2 笔·首立）、所调之器（截至之树）、所系之法、所守之坑',
           '史：2 笔' in 流 and '工具/巡.py' in 流.split('所调之器')[1].split('\n')[0]
           and '工具/门.py' not in 流.split('所调之器')[1].split('\n')[0] and '法用#乙' in 流 and '坑#3' in 流
           and '首立 `%s`' % c0[:12] in 流)
        # ⑭ 所替与坑之以号：审计之名⛔归、待⛔算所替、更长之号之一段⛔归（1119 复核：「1027 执行之审 #1」白归待「执行之审」二十七条）
        审 = 节('甲审')
        判('⑭ 废据「1027 甲审 #1 #12」⛔归待甲审、⛔归甲（甲审之一段）；「1027 乙 #3；乙·线B」⛔归乙；「审·乙（B）」归乙〔以字〕；'
           '待之坑只认「法用#甲审」（坑#7 归、坑#6「1027 甲审 195 条」⛔归）',
           '所替' not in 审 and '坑#7 ' in 审 and '坑#6 ' not in 审 and '法用#戊旧' not in 甲 and '坑#6 ' not in 甲
           and '法用#庚旧' in 节('乙') and '〔以字〕' in 节('乙') and '法用#己旧' not in 节('乙')
           and '替之者：—' in 节('戊旧') and '替之者：法用#乙' in 节('庚旧'), 审[:400])
        # ⑮ 守器之律：枢纽之器（≥3 法直引）与只出自权限串之器⛔入守器一路
        判('⑮ 枢纽之器（工具/枢.py·甲戊己三法直引）所守之坑#4 ⛔归三法；只在权限串引之 工具/许.py 所守之坑#5 ⛔归戊；'
           '非枢纽之 工具/巡.py 照归甲（坑#2〔以守器〕）',
           all('坑#4 ' not in 节(x) for x in ('甲', '戊', '己')) and '坑#5 ' not in 节('戊') and '〔以守器 工具/巡.py〕' in 甲)
        # ⑯ 两枝各 --写 → 并 → 谱冲突 → --并 自解 → --验 绿；他档亦冲突即 --并 拒
        仓2 = os.path.join(tmp, 'repo2')
        g('clone', '-q', 'file://' + 仓, 仓2, 根=tmp)
        for k, v in (('user.name', '自测'), ('user.email', 'zice@example.invalid'), ('commit.gpgsign', 'false'),
                     ('core.hooksPath', os.path.join(tmp, '无钩'))):
            g('config', k, v, 根=仓2)

        def 交2(说, 日):
            g('add', '-A', 根=仓2)
            g('commit', '-q', '-m', 说, 根=仓2, 加={'GIT_AUTHOR_DATE': 日, 'GIT_COMMITTER_DATE': 日})
            return g('rev-parse', 'HEAD', 根=仓2)

        def 添(路, 文2, 根2=None):
            with open(os.path.join(根2 or 仓2, 路), 'a', encoding='utf-8') as f:
                f.write(文2)
        底 = g('rev-parse', 'HEAD', 根=仓2)
        g('checkout', '-q', '-b', 'b1', 根=仓2)
        添(法账名, '| 甲之二进 | 法用#甲 | — | 较旧：效——升 | 1122 | 取 |\n')
        写(仓2, 印=False)
        交2('b1：甲之二进（法用#甲）', '2026-11-08T00:00:00+00:00')
        g('checkout', '-q', '-b', 'b2', 底, 根=仓2)
        坑2 = json.load(open(os.path.join(仓2, 坑账名), encoding='utf-8'))
        坑2['坑'].append({'号': 8, '名': '乙之新坑（法用#乙）', '治': '记之', '守': [], '状': '已守', '复踩': []})
        with open(os.path.join(仓2, 坑账名), 'w', encoding='utf-8') as f:
            f.write(json.dumps(坑2, ensure_ascii=False))
        写(仓2, 印=False)
        交2('b2：乙之新坑（法用#乙）', '2026-11-08T01:00:00+00:00')
        g('checkout', '-q', 'b1', 根=仓2)
        rcm, _, _ = _git(仓2, 'merge', '--no-edit', 'b2', 加={'GIT_AUTHOR_DATE': '2026-11-09T00:00:00+00:00',
                                                            'GIT_COMMITTER_DATE': '2026-11-09T00:00:00+00:00'})
        冲 = g('diff', '--name-only', '--diff-filter=U', 根=仓2)
        with contextlib.redirect_stdout(io.StringIO()):
            rcb = 并(仓2)
        g('commit', '-q', '--no-edit', 根=仓2, 加={'GIT_AUTHOR_DATE': '2026-11-09T00:00:00+00:00',
                                                'GIT_COMMITTER_DATE': '2026-11-09T00:00:00+00:00'})
        ok16, 印16 = 验(仓2)
        谱2 = open(_谱路(仓2), encoding='utf-8').read()
        g('checkout', '-q', '-b', 'b3', 底, 根=仓2)
        书3 = open(os.path.join(仓2, 法账名), encoding='utf-8').read().replace('散行：乙之记', '散行：乙之记（b3 改）')
        with open(os.path.join(仓2, 法账名), 'w', encoding='utf-8') as f:
            f.write(书3)
        写(仓2, 印=False)
        交2('b3', '2026-11-09T01:00:00+00:00')
        g('checkout', '-q', 'b1', 根=仓2)
        g('reset', '-q', '--hard', 'HEAD~1', 根=仓2)       # 回 b1 之并前（b1 之笔）；再於 b1 改同一行
        with open(os.path.join(仓2, 法账名), 'w', encoding='utf-8') as f:
            f.write(open(os.path.join(仓2, 法账名), encoding='utf-8').read().replace('散行：乙之记', '散行：乙之记（b1 改）'))
        写(仓2, 印=False)
        交2('b1 又', '2026-11-09T02:00:00+00:00')
        _git(仓2, 'merge', '--no-edit', 'b3')
        with contextlib.redirect_stdout(io.StringIO()):
            rcx = 并(仓2)
        冲x = g('diff', '--name-only', '--diff-filter=U', 根=仓2)
        _git(仓2, 'merge', '--abort')
        判('⑯ 两枝各 --写 → git merge 冲突唯谱 → --并 重写并 add → commit → --验 绿（二枝之账俱入谱）；方法账亦冲突即 --并 rc 1、⛔动',
           rcm != 0 and 冲 == 谱名.replace(os.sep, '/') and rcb == 0 and ok16 and '坑#8 ' in 谱2 and '甲之二进' in 谱2
           and rcx == 1 and 法账名.replace(os.sep, '/') in 冲x, '冲=%r rcb=%s ok=%s %s' % (冲, rcb, ok16, ' / '.join(印16[-3:])))
        # ⑰ 笔数＝git log -- <档>（旁枝被剪之笔⛔算、两侧俱改之并入）
        书门 = lambda 首, 尾: open(os.path.join(仓2, '工具/门.py'), 'w', encoding='utf-8').write(
            'def 守():\n    a = %s\n    b = 0\n    c = 0\n    d = 0\n    e = 0\n    return %s\n' % (首, 尾))
        书门(0, 0)
        交2('门之七行', '2026-11-10T00:00:00+00:00')
        g('checkout', '-q', '-b', 's1', 根=仓2)
        书门(9, 0)
        交2('旁改一（将弃）', '2026-11-10T01:00:00+00:00')
        书门(8, 0)
        交2('旁改二（将弃）', '2026-11-10T01:30:00+00:00')
        g('checkout', '-q', 'b1', 根=仓2)
        g('merge', '-q', '-s', 'ours', '--no-edit', 's1', 根=仓2, 加={'GIT_AUTHOR_DATE': '2026-11-10T02:00:00+00:00',
                                                                    'GIT_COMMITTER_DATE': '2026-11-10T02:00:00+00:00'})
        g('checkout', '-q', '-b', 's2', 根=仓2)
        书门(0, 7)
        交2('旁改尾', '2026-11-10T03:00:00+00:00')
        g('checkout', '-q', 'b1', 根=仓2)
        书门(5, 0)
        交2('主改首', '2026-11-10T04:00:00+00:00')
        g('merge', '-q', '--no-edit', 's2', 根=仓2, 加={'GIT_AUTHOR_DATE': '2026-11-10T05:00:00+00:00',
                                                       'GIT_COMMITTER_DATE': '2026-11-10T05:00:00+00:00'})
        写(仓2, 印=False)
        谱17 = open(_谱路(仓2), encoding='utf-8').read()
        m17 = re.search(r'%s 工具/门\.py：(\d+) 笔' % 标, 谱17)
        默 = len(g('log', '--format=%H', '--', '工具/门.py', 根=仓2).split())
        全 = len(g('log', '--full-history', '--no-merges', '--format=%H', '--', '工具/门.py', 根=仓2).split())
        h2 = 读史(仓2, g('rev-parse', 'HEAD', 根=仓2))
        简2 = _简(h2, ['工具/门.py', '工具/巡.py', '.github/workflows/巡.yml'])
        合 = all([h2['笔'][j][0] for j in 简2.get(p, [])] == g('log', '--format=%H', '--', p, 根=仓2).split()
                for p in ('工具/门.py', '工具/巡.py', '.github/workflows/巡.yml'))
        判('⑰ 证器之笔数＝git log -- <档>（旁枝 -s ours 被剪之笔⛔算、两侧俱改之并入；逐笔逐序与 git 同）',
           m17 is not None and int(m17.group(1)) == 默 and 全 != 默 and 合 and '全史见 git log -- 工具/门.py' in 谱17,
           'm=%s 默=%d 全=%d 合=%s' % (m17 and m17.group(1), 默, 全, 合))
        # ⑱ 浅克隆之 --法、--印：首行 ⚠、⛔印 ⎇ 之行（旧：印残史「历次之进：无」而 rc 0）
        r18 = subprocess.run([sys.executable, os.path.abspath(__file__), '--法', '甲', '--根', 浅], capture_output=True, env=_env(), timeout=120)
        r18b = subprocess.run([sys.executable, os.path.abspath(__file__), '--印', '--根', 浅], capture_output=True, env=_env(), timeout=120)
        o18, o18b = r18.stdout.decode('utf-8', 'replace'), r18b.stdout.decode('utf-8', 'replace')
        判('⑱ 浅克隆：--法、--印 首行「⚠ 浅克隆」、⛔印 ⎇ 之行（账之部照印）；③ 红示「先 git fetch --unshallow」',
           o18.startswith('⚠ 浅克隆') and 标 not in o18.split('\n', 1)[-1] and '### 法用#甲（' in o18 and o18b.startswith('⚠ 浅克隆')
           and ('%s 历次之进' % 标) not in o18b and ('### %s ' % 标) not in o18b and '### 法用#乙（' in o18b
           and any('git fetch --unshallow' in x for x in 验(浅)[1]), o18[:200])
        # ⑲ --随：谱随账时⛔动（截至⛔改）、账变方写
        前19 = open(_谱路(仓2), encoding='utf-8').read()
        交2('谱入（法用#甲）', '2026-11-11T00:00:00+00:00')
        书门(1, 1)
        交2('又一改（法用#甲）', '2026-11-11T01:00:00+00:00')
        with contextlib.redirect_stdout(io.StringIO()):
            rc19 = 随(仓2)
        不动 = open(_谱路(仓2), encoding='utf-8').read() == 前19
        添(坑账名, '')
        添(法账名, '| 甲之三进 | 法用#甲 | — | 较旧：效——升 | 1123 | 取 |\n')
        with contextlib.redirect_stdout(io.StringIO()):
            rc19b = 随(仓2)
        後19 = open(_谱路(仓2), encoding='utf-8').read()
        判('⑲ --随：--验 绿即⛔动（截至⛔改·免并之冲突）；改账而谱旧 → 自 --写 → 复绿',
           rc19 == 0 and 不动 and rc19b == 0 and 後19 != 前19 and '甲之三进' in 後19 and 验(仓2)[0])
    except Exception as ex:
        import traceback
        traceback.print_exc()
        判('自测之仓', False, str(ex))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    n, m = sum(果), len(果)
    print('进化树·自测 %d/%d %s（%.1f 秒）' % (n, m, '全通' if n == m else '未过', time.time() - t0))
    return 0 if n == m else 1


def main(argv):
    根 = ROOT
    if '--根' in argv:
        k = argv.index('--根')
        根 = os.path.abspath(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    try:
        if '--自测' in argv:
            return 自测()
        if '--写' in argv:
            return 写(根)
        if '--随' in argv:
            return 随(根)
        if '--并' in argv:
            return 并(根)
        if '--印' in argv:
            _, h, 行 = _印组(根)
            sys.stdout.write(('' if h is not None else 浅警 + '\n') + '\n'.join(行).rstrip('\n') + '\n')
            return 0
        if '--法' in argv:
            k = argv.index('--法')
            if k + 1 >= len(argv):
                print('⛔ --法 须带号')
                return 1
            return 一线(根, argv[k + 1])
        if '--验' in argv:
            t0 = time.time()
            ok, 印 = 验(根)
            print('进化树·验')
            print('\n'.join(印))
            print('进化树·验 %s（%.1f 秒）' % ('✓ 绿' if ok else '⛔ 红', time.time() - t0))
            return 0 if ok else 1
    except Exception as ex:
        print('⛔ 进化树：%s' % 截(str(ex), 200))
        return 1
    print(__doc__.split('用法：', 1)[-1])
    return 0 if not argv else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
