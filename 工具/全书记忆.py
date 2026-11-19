#!/usr/bin/env python3
"""全书记忆之闸（0927·作者令「通读一回就要全书记住，以後直接调取，不必每回再读」）：
自 设定/全书记忆/总览.md 立起之後启用：每一正文章须有 设定/全书记忆/第N章.md，且其所记 sha1（前十二位）与现正文相符；
正文改了而详记未随即红——记忆不许过期。
★1119 总编辑复核「全书记忆」→改（0b78fa725）：旧判只认 sha 子串——还账、记落盲换 sha 则恒绿（W26 後 24 章残留原片 123 处；
  今 458／428／448／430／410／407 正文已删而详记照记，本器 ✓）。今：
  ① sha 只认其格「- 正文档：…｜sha1：<十二位小写十六进>」（24 位、缺格俱红；⛔子串）；
  ② 所记 sha ≠ 现正文：取所记 sha 之稿（版本/第N章/*.md，否则 git 史中本章正文之 blob，俱以 sha1 前十二位认），比白文
     （【本章亮点】以前）：旧稿之片（以标点分、≥8 汉字）现白文已无、而仍见於详记正记（在场之人、物二头行及其下缩进之子行；发生了什么、
     要句、本章之新知三节；备审之注行、行首「**…备审…**」「**…席裁…**」之注块⛔算）者＝残片 → 红并列「第N章 详记:行 ← 原片」；无残片 → 器随 sha（零 token·吞 --随）；
     所记之稿无处可取 → 红（比不得，⛔放）；
  ③ --拦章 N（封版 --後 之闸）：缺详记、sha 格坏、稿无处可取，凡章俱拦；残片唯本章 N 拦，他章之残片只印（入全测 → 器红账·三章治），
     ⛔以他章之残片拦本章之封；
  ④ 还账.施後同步、记落 --重填 ⛔盲换 sha，改调本器（器换·随章）。
用法：python3 工具/全书记忆.py               # 全书：残片、缺、格坏即红；可随者器随 sha
      python3 工具/全书记忆.py --随          # 同上（旧名，封版 --後「全书记忆随」之步）
      python3 工具/全书记忆.py --拦章 N      # 封版 --後 之闸：他章之残片只印⛔拦
      python3 工具/全书记忆.py --只查        # ⛔写（全测）：可随者亦红
      python3 工具/全书记忆.py --通扫        # 一回之清：以本章正文 git 史诸稿与 版本 诸稿比今白文，列详记正记中之残片（⛔写）
      python3 工具/全书记忆.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, glob, hashlib, tempfile, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
数 = {c: i for i, c in enumerate('零一二三四五六七八九')}
片限 = 8                                             # 残片之最短（汉字）：短片太泛（「他没有动」撞满书）
正节 = ('发生了什么', '要句', '本章之新知')            # 详记正记之节（⛔悬线、亮点、读之得、一句之要：彼多引史）
正头式 = re.compile(r'^- (?:在场之人|物)[（：]')          # 首节之正记二头（「- 在场之人：」「- 在场之人（行次…）：」）；其下缩进之子行（「  - **我**：…」）同係正记
注式 = re.compile(r'备审|已改|已删|[vV]\d+\s*(?:作|删)|〔[^〕]*裁')   # 备审之注、改史之注（「v0N 作」「〔裁」）：引旧文係史，⛔算
注段式 = re.compile(r'（[^（）]*）|〔[^〔〕]*〕|\([^()]*\)')       # 括注：含注之记者（「（见备审③）」「（v02 作「…」）」「〔裁：…〕」）去之，余文照判
注头式 = re.compile(r'^\s*\*\*[^*\n]*(?:备审|席裁|〔[^〕\n]*裁)[^*\n]*\*\*')   # 「**记录者读时所见（未改正文，备审）**」「**总览席裁（…）**」：其下至节末俱注。
#   ★只认行首「**」之头：「- **米账一页…她裁去宽的那一头…**」「- **…（见备审③）**」係正记之条（「裁」係书中裁纸之字）——⛔当注头吞其下至节末
标点式 = re.compile(r'[\s，。；：！？、「」『』“”‘’（）《》〈〉【】\[\]…—－·,.;:!?()<>"\'*`~/|｜]+')
格式 = re.compile(r'(?m)^- 正文档：[^\n]*?｜sha1：([0-9A-Za-z]*)')


def 汉转(s):
    n = 0; 段 = 0
    for c in s:
        if c in 数:
            段 = 数[c]
        elif c == '十':
            n += (段 or 1) * 10; 段 = 0
        elif c == '百':
            n += 段 * 100; 段 = 0
    return n + 段


def 诸章(root):
    r = {}
    for p in glob.glob(os.path.join(root, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(p))
        if m:
            r[汉转(m.group(1))] = p
    return r


def 白文(t):
    """【本章亮点】以前之文——详记所记者只此；亮点之注改而白文未动，记忆不算过期。"""
    i = t.find('\n【本章亮点】')
    return t if i < 0 else t[:i]


def 汉(s):
    return len(re.findall(r'[一-鿿]', s or ''))


def 去标(t):
    """去标点与空白：片之在否以此比（逗号之添删⛔算删句）。"""
    return 标点式.sub('', t or '')


def 片们(t):
    """白文 → 片（以标点分、≥片限汉字），去重存序。"""
    return [x for x in dict.fromkeys(标点式.split(t or '')) if 汉(x) >= 片限]


def 所记(记):
    """→ (sha, 坏)：sha 只认其格「- 正文档：…｜sha1：<十二位小写十六进>」；格缺或位数不合 → (None, 坏之语)。"""
    m = 格式.search(记 or '')
    if not m:
        return None, '无「- 正文档：…｜sha1：<十二位>」之格'
    if not re.fullmatch(r'[0-9a-f]{12}', m.group(1)):
        return None, 'sha1 之格坏（「%s」%d 位·须恰十二位小写十六进）' % (m.group(1)[:30], len(m.group(1)))
    return m.group(1), None


def 去注(l):
    """行 → 去其注段之余文；整行係注（去括注後仍带注之记：备审、已改、v0N 作、〔裁）→ None。
    按拍之行带「（见备审③）」者仍係正记（只去其括注）——⛔整行放过。"""
    s = l
    for _ in range(3):
        s2 = 注段式.sub(lambda m: '' if 注式.search(m.group(0)) else m.group(0), s)
        if s2 == s:
            break
        s = s2
    return None if 注式.search(s) else s


def 注行(l):
    return 去注(l) is None


def _诸行(记):
    """→ [(行号, 行, 节)]：去注块（「**…备审…**」「**…裁…**」之头至节末）。节 None ＝首节。"""
    出, 节, 块 = [], None, False
    for i, l in enumerate((记 or '').split('\n'), 1):
        if l.startswith('## '):
            节, 块 = l[3:].strip(), False; continue
        if 注头式.match(l):
            块 = True
        if not 块:
            出.append((i, l, 节))
    return 出


def 正记行(记):
    """→ [(行号, 余文)]：详记正记之行（首节 在场之人、物二头及其下缩进之子行；发生了什么、要句、本章之新知三节），去备审之注块、注行与行中之注段。"""
    出, 头 = [], False
    for i, l, 节 in _诸行(记):
        if 节 is None:
            if 正头式.match(l):
                头 = True
            elif l.strip() and not l[:1].isspace():
                头 = False                                   # 首节他头（正文档、线与日…）
            是 = 头 and bool(l.strip())
        else:
            是 = 节.startswith(正节)
        if 是:
            s = 去注(l)
            if s:
                出.append((i, s))
    return 出


def _外换(l, x, y):
    """行中注段（含注之记之括注）以外之 x → y。"""
    出, k = [], 0
    for m in 注段式.finditer(l):
        if 注式.search(m.group(0)):
            出 += [l[k:m.start()].replace(x, y), m.group(0)]; k = m.end()
    return ''.join(出) + l[k:].replace(x, y)


_git缓 = {}


def _仓(r):
    p = subprocess.run(['git', '-C', r, 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def _git诸稿(root, 档):
    """本章正文於 git 史之诸 blob（凡分支、凡名：以档名「_第X章_」认，改题亦得）→ [bytes]。
    一仓只跑一回 git log（正文/ 全史之 raw，按章段分）；root 非 git 之树则借本器之仓（以 sha1 认内容，⛔误）。"""
    m = re.search(r'_第[零一二三四五六七八九十百千]+章_', os.path.basename(档 or ''))
    树 = m and (_仓(root) or _仓(ROOT))
    if not 树:
        return []
    if 树 not in _git缓:
        out = subprocess.run(['git', '-c', 'core.quotepath=off', '-C', 树, 'log', '--all', '--format=', '--raw', '--no-abbrev', '--', '正文/'],
                             capture_output=True, text=True).stdout
        索 = {}
        for l in out.split('\n'):
            if not l.startswith(':') or '\t' not in l:
                continue
            f, 径 = l.split('\t')[0].split(), l.split('\t')[-1]
            k = re.search(r'_第[零一二三四五六七八九十百千]+章_', os.path.basename(径))
            if not k:
                continue
            for x in f[2:4]:
                if re.fullmatch(r'[0-9a-f]{40}', x) and set(x) != {'0'}:
                    索.setdefault(k.group(0), {})[x] = None
        _git缓[树] = {'索': 索, '稿': {}}
    缓 = _git缓[树]
    if m.group(0) not in 缓['稿']:
        号们 = list(缓['索'].get(m.group(0), {}))
        诸 = []
        if 号们:
            p = subprocess.run(['git', '-C', 树, 'cat-file', '--batch'], input=('\n'.join(号们) + '\n').encode(), capture_output=True)
            b, i = p.stdout, 0
            while i < len(b):
                j = b.index(b'\n', i)
                头 = b[i:j].split()
                if len(头) < 3 or 头[1] != b'blob':
                    i = j + 1; continue
                k = int(头[2])
                诸.append(b[j + 1:j + 1 + k]); i = j + 1 + k + 1
        缓['稿'][m.group(0)] = 诸
    return 缓['稿'][m.group(0)]


def 旧稿(n, sha, root=ROOT, 档=None):
    """所记 sha 之稿：先 版本/第N章/*.md，次 git 史之 blob（俱以 sha1 前十二位认）→ (文, 出处) 或 (None, None)。"""
    for v in sorted(glob.glob(os.path.join(root, '版本', '第%d章' % n, '*.md'))):
        b = open(v, 'rb').read()
        if hashlib.sha1(b).hexdigest()[:12] == sha:
            return b.decode('utf-8', 'replace'), os.path.relpath(v, root)
    for b in _git诸稿(root, 档 or 诸章(root).get(n, '')):
        if hashlib.sha1(b).hexdigest()[:12] == sha:
            return b.decode('utf-8', 'replace'), 'git'
    return None, None


def 残(旧, 新, 记):
    """旧稿、现正文、详记 → [(详记行号, 片)]：旧白文之片现白文已无、而仍见於详记正记者。"""
    新白 = 去标(白文(新))
    去 = [x for x in 片们(白文(旧)) if x not in 新白]
    行们 = 正记行(记)
    return [(i, x) for x in 去 for i, l in 行们 if x in l]


def 随章(n, root=ROOT, 写=True):
    """一章之判 → (状, 红们)。状：合｜随（无残片，已器随 sha）｜可随（同上而⛔写）｜无记｜格坏｜无稿｜残。"""
    p = 诸章(root).get(n)
    f = os.path.join(root, '设定', '全书记忆', '第%d章.md' % n)
    if not p:
        return '合', []
    if not os.path.exists(f):
        return '无记', ['第%d章无详记' % n]
    记 = open(f, encoding='utf-8', errors='replace').read()
    sha, 坏 = 所记(记)
    if 坏:
        return '格坏', ['第%d章详记 %s' % (n, 坏)]
    现 = open(p, 'rb').read()
    h = hashlib.sha1(现).hexdigest()[:12]
    if sha == h:
        return '合', []
    旧, 处 = 旧稿(n, sha, root, p)
    if 旧 is None:
        return '无稿', ['第%d章详记过期（正文 sha1 %s；所记 %s 之稿 版本/第%d章 与 git 史俱无——比不得，须记席照现正文重核重记）' % (n, h, sha, n)]
    r = 残(旧, 现.decode('utf-8', 'replace'), 记)
    if r:
        return '残', ['第%d章 详记:%d ← 「%s」（正文已无·所记 %s 之稿 %s）' % (n, i, x, sha, 处) for i, x in r]
    if not 写:
        return '可随', ['第%d章详记 sha1 未随（正文 %s≠所记 %s；白文之变无残片——器可随：python3 工具/全书记忆.py --随）' % (n, h, sha)]
    open(f, 'w', encoding='utf-8').write(记.replace('｜sha1：' + sha, '｜sha1：' + h, 1))
    return '随', []


def 器换(n, 旧, 新, root=ROOT):
    """还账「换」类：旧正文 → 新正文（同行之改），一字不差之同片（≥片限汉字、旧白文恰一见、新片见於新白文）於详记（备审之注行⛔动）器换
    → [(行号, 旧片, 新片)]。零 token；换不得者（删而无新片、详记之引跨片）留与 随章 判残片。"""
    import difflib
    f = os.path.join(root, '设定', '全书记忆', '第%d章.md' % n)
    if not os.path.exists(f):
        return []
    旧白, 新白 = 白文(旧), 白文(新)
    if 旧白.count('\n') != 新白.count('\n'):
        return []                                            # 行数不齐（非 --施 之「换」）：⛔逐行配对（恐配错片而误改引文）——留与 随章 判残片
    对 = []
    for 旧行, 新行 in zip(旧白.split('\n'), 新白.split('\n')):
        if 旧行 == 新行:
            continue
        a, b = 标点式.split(旧行), 标点式.split(新行)
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag != 'replace' or i2 - i1 != j2 - j1:
                continue
            for x, y in zip(a[i1:i2], b[j1:j2]):
                if 汉(x) >= 片限 and y and 旧白.count(x) == 1 and x not in 去标(新白) and y in 新白:
                    对.append((x, y))
    if not 对:
        return []
    文 = open(f, encoding='utf-8').read()
    行们 = 文.split('\n')
    换了 = []
    for i, l, _ in _诸行(文):
        if l.startswith('- 正文档：') or 注行(l):
            continue
        for x, y in 对:
            l2 = _外换(l, x, y)
            if l2 != l:
                l = l2; 换了.append((i, x, y))
        行们[i - 1] = l
    if 换了:
        open(f, 'w', encoding='utf-8').write('\n'.join(行们))
    return 换了


def 查(root=ROOT, 拦章=None, 写=True, 只报=None, 随了=None):
    """→ 红（拦）之列；总览未立 → None。写：可随者器随 sha（否则亦红；所随之章入 随了）。拦章 N：他章之残片入 只报（⛔拦），余照拦。"""
    d = os.path.join(root, '设定', '全书记忆')
    if not os.path.exists(os.path.join(d, '总览.md')):
        return None
    红 = []
    for n in sorted(诸章(root)):
        状, r = 随章(n, root, 写)
        if 状 == '随' and 随了 is not None:
            随了.append(n)
        if 状 == '残' and 拦章 is not None and n != 拦章:
            if 只报 is not None:
                只报.extend(r)
            continue
        红.extend(r)
    return 红


def 随(root=ROOT):
    """1024 实踩（410）之器随，今吞入 随章：凡所记 sha 不合而所记之稿可取、白文之变无残片者，器改 sha（零 token）。回所随之章。"""
    if not os.path.exists(os.path.join(root, '设定', '全书记忆', '总览.md')):
        return []
    return [n for n in sorted(诸章(root)) if 随章(n, root, True)[0] == '随']


def 通扫(root=ROOT):
    """一回之清（1119）：详记史上所记之诸 sha（git 史中 设定/全书记忆/第N章.md 之「正文档」行，一回 git log 取尽）各取其稿，
    与今白文比——旧稿之片今已无而仍见於今详记正记者 → [(章, 行号, 片)]（⛔写）。sha 已被盲换之章（还账、记落之旧器）以此方见其残。"""
    树 = _仓(root)
    out = subprocess.run(['git', '-c', 'core.quotepath=off', '-C', 树, 'log', '--all', '-p', '--format=', '--', '设定/全书记忆/'],
                         capture_output=True, text=True).stdout if 树 else ''
    史 = {}
    档 = None
    for l in out.split('\n'):
        if l.startswith('+++ ') or l.startswith('--- '):
            m = re.search(r'设定/全书记忆/第(\d+)章\.md', l)
            档 = int(m.group(1)) if m else (档 if l.startswith('+++ /dev/null') else None)
        elif 档 and l[:1] in '+-' and l[1:].startswith('- 正文档：'):
            m = re.search(r'sha1：([0-9a-f]{12})', l)
            if m:
                史.setdefault(档, {})[m.group(1)] = None
    出 = []
    for n, p in sorted(诸章(root).items()):
        f = os.path.join(root, '设定', '全书记忆', '第%d章.md' % n)
        if not os.path.exists(f):
            continue
        记 = open(f, encoding='utf-8', errors='replace').read()
        现 = open(p, encoding='utf-8', errors='replace').read()
        sha, _ = 所记(记)
        诸 = dict(史.get(n, {}))
        if sha:
            诸[sha] = None
        见 = set()
        for s in 诸:
            旧, _ = 旧稿(n, s, root, p)
            if 旧 is None:
                continue
            for i, x in 残(旧, 现, 记):
                if (i, x) not in 见:
                    见.add((i, x)); 出.append((n, i, x))
    return 出


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '正文')); os.makedirs(os.path.join(t, '设定', '全书记忆'))
        p = os.path.join(t, '正文', '镇冢秘术_第一百零七章_某.md'); open(p, 'w').write('正文甲')
        记档 = os.path.join(t, '设定', '全书记忆', '第107章.md')
        def 记(sha, 余=''):
            open(记档, 'w', encoding='utf-8').write('# 第107章\n- 正文档：正文/镇冢秘术_第一百零七章_某.md｜sha1：%s｜字数约 9\n%s' % (sha, 余))
        共 += 1; ok += (查(t) is None)                      # 总览未立，不启
        open(os.path.join(t, '设定', '全书记忆', '总览.md'), 'w').write('览')
        共 += 1; ok += (查(t) == ['第107章无详记'])
        h = hashlib.sha1(b'\xe6\xad\xa3\xe6\x96\x87\xe7\x94\xb2').hexdigest()[:12]
        记(h)
        共 += 1; ok += (查(t) == [])
        open(p, 'w').write('正文乙')
        共 += 1; ok += (len(查(t)) == 1 and '过期' in 查(t)[0])   # 正文改而记未随（所记之稿无处可取）→ 红
        # 随：白文改了（正文甲→乙）而稿中无其 sha → ⛔随、仍红
        共 += 1; ok += (随(t) == [] and len(查(t)) == 1)
        # 随：记照 v03（白文＋亮点甲），正文只改亮点 → 器随 sha、转绿
        v = os.path.join(t, '版本', '第107章'); os.makedirs(v)
        稿 = '白文一行\n【本章亮点】\n甲'.encode('utf-8'); open(os.path.join(v, 'v03.md'), 'wb').write(稿)
        记(hashlib.sha1(稿).hexdigest()[:12])
        open(p, 'w', encoding='utf-8').write('白文一行\n【本章亮点】\n甲；总编辑之注')
        共 += 1; ok += (随(t) == [107] and 查(t) == [])
        # 随：白文亦改、所删之句仍在详记 → ⛔随（真过期）
        稿 = '他把那一截线头攥在了手心里。\n【本章亮点】\n甲'.encode('utf-8'); open(os.path.join(v, 'v03.md'), 'wb').write(稿)
        记(hashlib.sha1(稿).hexdigest()[:12], '## 要句\n- :1「他把那一截线头攥在了手心里。」\n')
        open(p, 'w', encoding='utf-8').write('白文改了\n【本章亮点】\n甲')
        共 += 1; ok += (随(t) == [] and len(查(t)) == 1)
        共 += 1; ok += (汉转('三百七十九') == 379 and 汉转('十一') == 11 and 汉转('一百一十七') == 117)
        # ★1119 负例：白文之句删而详记按拍仍记 → 红并列 详记:行 ← 原片
        旧 = '他把那一截线头攥在了手心里。\n门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        新 = '门缝底下那一点鞋尖没有了。\n\n【本章亮点】\n甲'
        open(os.path.join(v, 'v03.md'), 'w', encoding='utf-8').write(旧)
        s旧 = hashlib.sha1(旧.encode('utf-8')).hexdigest()[:12]
        记(s旧, '- 在场之人：他\n## 发生了什么（按拍）\n1. 他把那一截线头攥在了手心里（:1）；门缝底下那一点鞋尖没有了（:2）。\n## 要句（原句照录）\n- :2「门缝底下那一点鞋尖没有了。」\n')
        open(p, 'w', encoding='utf-8').write(新)
        _r = 查(t)
        共 += 1; ok += (_r == ['第107章 详记:5 ← 「他把那一截线头攥在了手心里」（正文已无·所记 %s 之稿 版本/第107章/v03.md）' % s旧] and s旧 in open(记档, encoding='utf-8').read())
        # 负例：原片只在备审之注（及悬线之节）→ ⛔算、器随 sha 转绿
        记(s旧, '## 发生了什么（按拍）\n1. 门缝底下那一点鞋尖没有了（:2）。\n**记录者读时所见（未改正文，备审）**：v01 作「他把那一截线头攥在了手心里」\n'
              '## 悬线\n- 作废：他把那一截线头攥在了手心里（v03 删）\n')
        共 += 1; ok += (查(t) == [] and hashlib.sha1(新.encode('utf-8')).hexdigest()[:12] in open(记档, encoding='utf-8').read())
        # 负例：按拍之行只带「（见备审①）」之括注 → 仍係正记，照红（⛔整行放过）
        记(s旧, '## 发生了什么（按拍）\n1. 他把那一截线头攥在了手心里（:1·见备审①）。\n')
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '详记:4 ← 「他把那一截线头攥在了手心里」' in _r[0])
        # 负例：sha 之格 24 位（前十二位与现正文合亦红·⛔子串）；无格亦红
        h新 = hashlib.sha1(新.encode('utf-8')).hexdigest()[:12]
        记(h新 + '069a087f0eea')
        共 += 1; ok += (len(查(t)) == 1 and '格坏' in 查(t)[0] and '24 位' in 查(t)[0])
        open(记档, 'w', encoding='utf-8').write('# 第107章\n备审：sha1：%s\n' % h新)
        共 += 1; ok += (len(查(t)) == 1 and '无「- 正文档' in 查(t)[0])
        # 拦章（封版 --後）：他章之残片只报⛔拦；本章之残片、他章之缺与格坏照拦；全书（全测）照红
        记(s旧, '## 要句\n- :1「他把那一截线头攥在了手心里。」\n')
        _报 = []
        共 += 1; ok += (查(t, 拦章=108, 只报=_报) == [] and len(_报) == 1 and '详记:4' in _报[0] and len(查(t, 拦章=107)) == 1 and len(查(t)) == 1)
        open(os.path.join(t, '正文', '镇冢秘术_第一百零八章_某.md'), 'w').write('又一章')
        共 += 1; ok += (查(t, 拦章=108, 只报=[]) == ['第108章无详记'])
        os.remove(os.path.join(t, '正文', '镇冢秘术_第一百零八章_某.md'))
        # 只查（全测）：可随者⛔写而红
        记(s旧, '## 要句\n- :2「门缝底下那一点鞋尖没有了。」\n')
        _前 = open(记档, encoding='utf-8').read()
        共 += 1; ok += (len(查(t, 写=False)) == 1 and '可随' in 查(t, 写=False)[0] and open(记档, encoding='utf-8').read() == _前)
        # 器换（还账「换」）：要句之旧句一字不差 → 器换新句；备审之注⛔动；後随章 → 随（零残）
        旧 = '他把那一截线头攥在了手心里，没有松。\n【本章亮点】\n甲'
        新 = '他把那一截线头攥进了袖口的那一圈里，没有松。\n【本章亮点】\n甲'
        open(os.path.join(v, 'v03.md'), 'w', encoding='utf-8').write(旧)
        记(hashlib.sha1(旧.encode('utf-8')).hexdigest()[:12], '## 要句\n- :1「他把那一截线头攥在了手心里，没有松。」（v01 作「他把那一截线头攥在了手心里」）\n备审：v01 作「他把那一截线头攥在了手心里」\n')
        open(p, 'w', encoding='utf-8').write(新)
        _换 = 器换(107, 旧, 新, t)
        _文 = open(记档, encoding='utf-8').read()
        共 += 1; ok += (_换 == [(4, '他把那一截线头攥在了手心里', '他把那一截线头攥进了袖口的那一圈里')] and '- :1「他把那一截线头攥进了袖口的那一圈里，没有松。」（v01 作「他把那一截线头攥在了手心里」）' in _文
                       and 'v01 作「他把那一截线头攥在了手心里」' in _文 and 随章(107, t) == ('随', []) and 查(t) == [])
        # ★1119 复审：「- **…裁…**」係正记之条（裁纸之「裁」）——⛔当注头吞其下；其下新知之行引所删之句 → 红
        旧 = '她拿小指比了比页边，页边宽得下小指一半写得下两个字。\n门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        新 = '\n门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        open(os.path.join(v, 'v03.md'), 'w', encoding='utf-8').write(旧)
        s旧 = hashlib.sha1(旧.encode('utf-8')).hexdigest()[:12]
        open(p, 'w', encoding='utf-8').write(新)
        记(s旧, '## 本章之新知\n- **米账一页记两样，她裁去宽的那一头（其比之方向见备审③）**（:1）。\n- 页边宽得下小指一半写得下两个字（:1）。\n')
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '详记:5 ← 「页边宽得下小指一半写得下两个字」' in _r[0])
        # 行首「**总览席裁（…）**」「**记录者读时所见（…备审）**」之真注块：其下引所删之句⛔算 → 器随
        记(s旧, '## 本章之新知\n- 门缝底下那一点鞋尖没有了（:2）。\n**总览席裁（0929）**：\n- 原文「页边宽得下小指一半写得下两个字」今不见\n'
              '## 要句\n- :2「门缝底下那一点鞋尖没有了。」\n**记录者读时所见（未改正文，备审）**\n- 页边宽得下小指一半写得下两个字\n')
        共 += 1; ok += (查(t) == [] and hashlib.sha1(新.encode('utf-8')).hexdigest()[:12] in open(记档, encoding='utf-8').read())
        # 首节「- 在场之人（行次…）：」之头与其下缩进之子行同係正记
        记(s旧, '- 在场之人（行次：她在前）：她\n  - **她**：她拿小指比了比页边（:1）\n- 物：页边\n')
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '详记:4 ← 「她拿小指比了比页边」' in _r[0])
        记(s旧, '- 在场之人（行次：她拿小指比了比页边）：她\n- 线与日：暗\n  - 页边宽得下小指一半写得下两个字\n')
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '详记:3 ← 「她拿小指比了比页边」' in _r[0])     # 他头（线与日）之子行⛔算
        # 器换：行数不齐（非 --施 之「换」）→ ⛔逐行配对（零换），留与 随章 判残片
        #   （删首行而後行上移：逐行配对则「他把那一截线头攥在了手心里」→「门缝底下那一点鞋尖没有了」之误换）
        旧 = '他把那一截线头攥在了手心里。\n门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        新 = '门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        open(os.path.join(v, 'v03.md'), 'w', encoding='utf-8').write(旧)
        open(p, 'w', encoding='utf-8').write(新)
        记(hashlib.sha1(旧.encode('utf-8')).hexdigest()[:12], '## 要句\n- :1「他把那一截线头攥在了手心里。」\n')
        _前 = open(记档, encoding='utf-8').read()
        共 += 1; ok += (器换(107, 旧, 新, t) == [] and open(记档, encoding='utf-8').read() == _前 and len(查(t, 写=False)) == 1)
    finally:
        shutil.rmtree(t)
    # git 史之稿（版本/第N章 无所记 sha 之稿）：以本章正文 git 史之 blob 认 → 照判残片；史亦无 → 无稿红
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '正文')); os.makedirs(os.path.join(t, '设定', '全书记忆'))
        open(os.path.join(t, '设定', '全书记忆', '总览.md'), 'w').write('览')
        p = os.path.join(t, '正文', '镇冢秘术_第一百零七章_某.md')
        旧 = '他把那一截线头攥在了手心里。\n门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲'
        open(p, 'w', encoding='utf-8').write(旧)
        _g = lambda *x: subprocess.run(['git', '-C', t, '-c', 'user.name=t', '-c', 'user.email=t@t', '-c', 'commit.gpgsign=false'] + list(x), capture_output=True)
        _g('init', '-q'); _g('add', '-A'); _g('commit', '-qm', '旧')
        open(p, 'w', encoding='utf-8').write('门缝底下那一点鞋尖没有了。\n【本章亮点】\n甲')
        _g('commit', '-qam', '新')
        s旧 = hashlib.sha1(旧.encode('utf-8')).hexdigest()[:12]
        记档 = os.path.join(t, '设定', '全书记忆', '第107章.md')
        open(记档, 'w', encoding='utf-8').write('# 第107章\n- 正文档：正文/镇冢秘术_第一百零七章_某.md｜sha1：%s\n## 要句\n- :1「他把那一截线头攥在了手心里。」\n' % s旧)
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '详记:4 ← 「他把那一截线头攥在了手心里」' in _r[0] and '之稿 git' in _r[0])
        open(记档, 'w', encoding='utf-8').write('# 第107章\n- 正文档：正文/镇冢秘术_第一百零七章_某.md｜sha1：%s\n## 要句\n- :1「他把那一截线头攥在了手心里。」\n' % ('0' * 12))
        _r = 查(t, 写=False)
        共 += 1; ok += (len(_r) == 1 and '过期' in _r[0] and 'git 史俱无' in _r[0])
    finally:
        shutil.rmtree(t)
    print('全书记忆·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--通扫']:
        r = 通扫()
        for n, i, x in r:
            print('  第%d章 详记:%d ← 「%s」' % (n, i, x))
        print('%s 全书记忆·通扫：详记正记中之残片 %d 处（%d 章）' % ('⛔' if r else '✓', len(r), len({x[0] for x in r})))
        sys.exit(1 if r else 0)
    拦章 = int(a[a.index('--拦章') + 1]) if '--拦章' in a else None
    写 = '--只查' not in a
    报, 随了 = [], []
    红 = 查(拦章=拦章, 写=写, 只报=报, 随了=随了)
    if 红 is None:
        print('ℹ 全书记忆：总览未立，闸未启')
        sys.exit(0)
    if 随了:
        print('✓ 全书记忆·随：%s 之 sha 随正文（所记之稿与现白文比，无残片）' % '、'.join('第%d章' % n for n in 随了))
    if 报:
        print('⚠ 全书记忆·他章之残片 %d 处（只报⛔拦第%d章之封·入全测 → 器红账三章治；治＝照现正文改详记、python3 工具/全书记忆.py）：' % (len(报), 拦章))
        for l in 报[:30]:
            print('  ' + l)
    if 红:
        print('⛔ 全书记忆：%d 处（详记缺、sha 格坏、或正文改了而详记未随——记忆不许过期）：' % len(红))
        for l in 红[:30]:
            print('  ' + l)
        print('⛔ 全书记忆：%d 处——%s' % (len(红), '｜'.join(红[:6])[:600]))
        sys.exit(1)
    if 报:
        print('✓ 全书记忆（--拦章 %d）：诸章详记齐全、sha1 之格俱合、所记之稿俱可取，第%d章无残片；他章之残片 %d 处只报（⛔拦本章之封）' % (拦章, 拦章, len(报)))
    else:
        print('✓ 全书记忆：诸章详记齐全、sha1 之格俱合且与正文相符（不符者白文之变无残片则器随）')
