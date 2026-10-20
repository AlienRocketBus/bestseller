#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""行号随移（★1020·W58 立·方案 W58 环 2②）——D1 换齐之後，在役诸档里凡指向漂区之行号，照映随移。零 token。

★1020·W58 其立之由：裁_1020_D1落式「照裁真另起段，许漂而随移」——103、104、196、313、317 五章变行数，其後之号俱漂；
  在役诸档引到漂区者数百处（W58 映与扫原型），⛔今日无一闸逮得着「号还在、指的已是另一行」（静漂）。
  手改必漏必错（#59 驳席逮插行漂引之致命）；故立本器：只改数字、逐条以内容锚自验、二跑零改。

映：`设定/剧情庭题/D1_行号映.json`（D1 施时所吐；在史档之列）。式 {"章": {"旧行": 新行|null}}（null＝删行）；
  亦认 {"章": {…}}／{"映": {…}} 之包（D1施 所吐即 {"章": {章: {"映": {…}, "旧长": …}}}）、每章 {"段": [[起, 止, 移|null], …]} 之段式。
  ⛔无映即拒；键不连续、值不严增即拒。
旧与新：旧＝`--旧` 所指（默 HEAD：git 之本；或一目录，内有旧之全仓）；新＝`--根` 之工作区（默本仓）。
  ①映两法互证：映（施改所吐）× difflib（旧正文对新正文）逐行比——等块里号不合、删行犹在、映到之行文非原文亦非其改作，
    一条即红、⛔施；正文未施（新旧同而映非恒等）亦⛔施；映外之章变了行数亦红。
  ②候选只取「旧本里就有」之号：旧档之行与新档之行逐行配，号在新行仍＝旧号者方移；已＝映後之号者为「已移」——
    故二跑零改；施後他席新写之号（本已是新号）⛔被当旧号再移一回（只列「新引」待判）。
所认之式（号皆照「旧号→新号」移）：
  · 章:行、章：行（全角）、章:行—行（两端各移；尾後随「：」而非数者亦认）、续引（「、行」「、:行」「「…」、:行」「「…」与 :行」）；
    第X章第N行（汉数之章亦认）；
  · 全书记忆/第N章.md 之「L行」（L5—13、L121、325）与「白文第a—b行」；人物链（全书记忆/人物链/）之条「- 〔N·…〕……（L行）」照其章；
  · 施工表锁定行（| N | 锁定 |）与漂章自身之亮点段：「白文第a—b行」「本章第N行」「第N行」「（行N）」；
  · awk/sed 之 NR==N、NR>=a&&NR<=b、sed -n 'a,bp'（⛔同行须有其章之正文档名）；
  · 章号紧邻之「拍N」（`317` 拍65、317→拍3、拍5）：拍映由新旧正文与行映推出（照 器物点名.分拍：以「＊」分）。
⛔不认：号大於该章旧长者（313:3144、317:1953 係净重）、「−」算式（317:116−6）、时刻（凌晨3:15、0911 05:54、HH:MM:SS）、
  千分（315:2,491）、0 起之号、限N：、COLD-313:…、拍103（拍号）、第104拍。
入待判（⛔改，只印建议）：指删行、区间端落删行（「缩」）、全删、带史标之行（旧号、改前、0929、D1施前……）、
  拍之裂与删、无章号之拍（漂章亮点、锁定行）、工具码里之引、新引（新旧不明）、他改、两可、锚异；
  ★1020·W58 驳席补：漂章亮点里前随汉字之「第N行」（「而第337行」本章、「施工表第273行」他档，字面难分）、
  无档名之 NR 而其前最近之章号係漂章者（施工表:1264「313之末句……`awk 'NR==577'`」）——俱⛔默弃。
免：二稿账「剧情庭 D1」节（0929 之锚·⛔随移，裁§二4 只行内注）。
不扫：史档（还账.史档）、案卷（版本/已写章）、版本/第400章 与第 400 章之正文、正文白文、工具/*.py 之注、负测之档、本器。

用法：
  python3 工具/行号随移.py --扫 [--根 副本] [--映 档] [--旧 HEAD] [--出 档.json] [--全]
  python3 工具/行号随移.py --施 --根 副本 [--映 档] [--旧 HEAD]    # ⛔无 --根 即拒；只改数字、行数不变；施毕自跑二跑
  python3 工具/行号随移.py --验 [--根 副本] [--映 档] [--旧 HEAD]    # 互证、已移之锚、二跑零改、史档未动
负测：python3 工具/负测_行号随移.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import collections
import difflib
import glob
import json
import os
import re
import subprocess
import sys

from 还账 import 史档          # ★史档之规只一处（还账.史档）；⛔另抄一份

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
映档 = os.path.join('设定', '剧情庭题', 'D1_行号映.json')
禁章 = (400,)                  # ★1020·W58：第 400 章之席正在跑——其案卷与正文⛔碰（裁§一：案卷含 400 一字不动）
二稿账 = '设定/二稿账.md'
_免节 = re.compile(r'^#{2,4}\s*剧情庭\s*D1（')   # 二稿账 D1 节：0929 之锚（裁§二4：⛔随移）

# ───────── 汉数 ─────────
_汉 = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def 汉转数(s):
    if s and s.isdigit():
        return int(s)
    n = c = 0
    for ch in s or '':
        if ch in _汉:
            c = _汉[ch]
        elif ch in '十百千':
            n += (c or 1) * {'十': 10, '百': 100, '千': 1000}[ch]
            c = 0
        else:
            return None
    return (n + c) or None


def 数转汉(n):
    数 = '零一二三四五六七八九'
    if n < 10:
        return 数[n]
    if n < 20:
        return '十' + (数[n % 10] if n % 10 else '')
    if n < 100:
        return 数[n // 10] + '十' + (数[n % 10] if n % 10 else '')
    百, 余 = divmod(n, 100)
    s = 数[百] + '百'
    if not 余:
        return s
    if 余 < 10:
        return s + '零' + 数[余]
    return s + 数[余 // 10] + '十' + (数[余 % 10] if 余 % 10 else '')


def _读(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


# ───────── 映 ─────────
def 读映(p):
    """→ {章: {旧行: 新行|None}}；不整即 ValueError。"""
    d = json.load(open(p, encoding='utf-8'))
    for 包 in ('章', '映'):                          # D1施 所吐係 {"章": {章: {"映": {…}, "旧长": …}}, "_说明": …}
        if isinstance(d, dict) and isinstance(d.get(包), dict):
            d = d[包]
            break
    if not isinstance(d, dict):
        raise ValueError('映非 {章: …} 之式')
    出 = {}
    for k, v in d.items():
        if not re.fullmatch(r'\d{1,3}', str(k)):
            continue                                  # 元数据之键（注、式、源……）
        c = int(k)
        if isinstance(v, dict) and isinstance(v.get('映'), dict):
            v = v['映']
        if isinstance(v, dict) and isinstance(v.get('段'), list):
            v = v['段']
        m = {}
        if isinstance(v, dict):
            for a, b in v.items():
                if not re.fullmatch(r'\d{1,5}', str(a)):
                    raise ValueError('第%d章之映键 %r 非行号' % (c, a))
                m[int(a)] = None if b is None else int(b)
        elif isinstance(v, list):
            for seg in v:
                起, 止, 移 = seg
                for i in range(int(起), int(止) + 1):
                    m[i] = None if 移 is None else i + int(移)
        else:
            raise ValueError('第%d章之映非 dict／段' % c)
        ks = sorted(m)
        if ks != list(range(1, len(ks) + 1)):
            raise ValueError('第%d章之映键不连续（应自 1 至 %d）' % (c, len(ks)))
        vs = [m[i] for i in ks if m[i] is not None]
        if any(x < 1 for x in vs) or any(b <= a for a, b in zip(vs, vs[1:])):
            raise ValueError('第%d章之映值不严增' % c)
        出[c] = m
    if not 出:
        raise ValueError('映里无一章')
    return 出


# ───────── 旧本 ─────────
class 旧本:
    """旧之全仓：git 之号（默 HEAD），或一目录。只读：git 俱以 --no-optional-locks。"""

    def __init__(s, root, ref='HEAD'):
        s.root, s.ref = root, ref
        s.目 = os.path.abspath(ref) if os.path.isdir(ref) else None
        s.改 = s.有 = None
        if s.目:
            return
        g = ['git', '--no-optional-locks', '-C', root, '-c', 'core.quotepath=off']
        r = subprocess.run(g + ['rev-parse', '--verify', '-q', ref + '^{commit}'], capture_output=True, text=True)
        if r.returncode:
            raise ValueError('旧本 %r 取不着（非目录、亦非 git 之号）' % ref)
        s.sha = r.stdout.strip()
        s._g = g
        s.有 = s._z(['ls-tree', '-r', '--name-only', '-z', s.sha])
        s.刷()

    def _z(s, a):
        return set(x for x in subprocess.run(s._g + a, capture_output=True).stdout.decode('utf-8', 'replace').split('\0') if x)

    def 刷(s):
        """工作区与旧本相异之档（施後须重取：否则施过之档被当作未改，二跑即把新号当旧号再移一回）。"""
        if not s.目:
            s.改 = s._z(['diff', '--name-only', '-z', s.sha, '--'])

    def 读(s, rel, 今=None):
        """→ 旧文（str），旧本无此档 → None。今：工作区之文（git 之本里未改者即返之，免逐档 show）。"""
        if s.目:
            p = os.path.join(s.目, rel)
            return _读(p) if os.path.isfile(p) else None
        if rel not in s.有:
            return None
        if rel not in s.改 and 今 is not None:
            return 今
        r = subprocess.run(s._g + ['show', '%s:%s' % (s.sha, rel)], capture_output=True)
        return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None

    def 改了的(s, 诸):
        """诸档里与旧本不同者（目录式逐档比）。"""
        if not s.目:
            return [x for x in 诸 if x in s.改]
        出 = []
        for rel in 诸:
            p = os.path.join(s.目, rel)
            if os.path.isfile(p) and os.path.isfile(os.path.join(s.root, rel)) and _读(p) != _读(os.path.join(s.root, rel)):
                出.append(rel)
        return 出


# ───────── 诸档与其类 ─────────
def 章档(root):
    出 = {}
    for f in glob.glob(os.path.join(root, '正文', '*.md')):
        m = re.search(r'第([零〇一二两三四五六七八九十百千]+)章', os.path.basename(f))
        n = 汉转数(m.group(1)) if m else None
        if n:
            出[n] = os.path.relpath(f, root)
    return 出


def 诸档(root):
    出 = set()
    for dp, dn, fn in os.walk(os.path.join(root, '设定')):
        for f in fn:
            if f.endswith(('.md', '.json')):
                出.add(os.path.relpath(os.path.join(dp, f), root))
    for pat in ('正文/*.md', '*.md', '工具/*.md', '工具/*.py', '工具/席/*.js', '版本/第*章/*.md', '版本/第*章/*.json'):
        出.update(os.path.relpath(f, root) for f in glob.glob(os.path.join(root, pat)))
    return sorted(出)


def 类(rel, 已写):
    """→ 役（在役·随移）｜文（正文·只扫亮点）｜码（工具之码·只待判）｜史｜卷｜禁｜免扫"""
    名 = os.path.basename(rel)
    if rel.startswith('版本/'):
        m = re.match(r'版本/第(\d+)章/', rel)
        n = int(m.group(1)) if m else None
        if n in 禁章:
            return '禁'
        return '卷' if (n is None or n in 已写) else '役'      # 未写章之卡在役；已写章之卷一字不动
    if rel.startswith('正文/'):
        m = re.search(r'第([零〇一二两三四五六七八九十百千]+)章', 名)
        return '禁' if (m and 汉转数(m.group(1)) in 禁章) else '文'
    if rel.startswith('设定/'):
        return '史' if (rel.startswith(史档) or 名.startswith('回执_')) else '役'
    if rel.startswith('工具/') and rel.endswith(('.py', '.js')):
        return '免扫' if (名.startswith(('负测_', '_')) or 名 == '行号随移.py') else '码'
    return '役'


def _码之行(文, 名):
    """工具码 → {行号: 该行之码（去注；py 之 docstring 亦去）}。只供待判，故粗取即可。"""
    行们 = 文.split('\n')
    出 = {}
    if 名.endswith('.py'):
        import io as _io
        import tokenize
        try:
            ds = set()
            import ast
            for node in ast.walk(ast.parse(文)):
                if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
                    b = node.body[0]
                    if isinstance(b, ast.Expr) and isinstance(getattr(b, 'value', None), ast.Constant) and isinstance(b.value.value, str):
                        ds.update(range(b.lineno, (b.end_lineno or b.lineno) + 1))
            for t in tokenize.generate_tokens(_io.StringIO(文).readline):
                if t.type == tokenize.STRING and t.start[0] not in ds:
                    for q, k in enumerate(range(t.start[0], t.end[0] + 1)):    # 只取串之字（注⛔扫）
                        出[k] = (出.get(k, '') + ' ' + t.string.split('\n')[q]).strip()
        except Exception:
            pass
        return 出
    for k, l in enumerate(行们, 1):
        s = l.strip()
        if s.startswith(('//', '/*', '*')):
            continue
        出[k] = l.split(' //')[0]
    return 出


# ───────── 引之认 ─────────
_D = r'[—–~～\-](?![—–~～\-])'
_尾 = r'(?!\d|\s?[:：]\s?\d)'     # ★1020·W58 驳席：区间之尾後随「：合到一半」者照认（旧作 (?![\d:：]) 致「313:477—537：」只移其头）；尾後「:数」係他章之头
_头 = re.compile(r'(?<![\dA-Za-z_\-.§#/@:Ｌ])(\d{1,3})([:：])(\d{1,4})(?!\d)')
_区 = re.compile(r'\s?' + _D + r'\s?(\d{1,4})' + _尾)
_续 = re.compile(r'(「[^」]*」|（[^（）]*）)?\s?([、，,／/]|与|和|及)\s?([:：])?(\d{1,4})(?:\s?' + _D + r'\s?(\d{1,4}))?(?!\d)')
_单位 = set('字处回次年天人个条章段页岁拍行号%％')
_章章行 = re.compile(r'第([零〇一二两三四五六七八九十百千]+|\d{1,3})章第(\d{1,4})(?:\s?' + _D + r'\s?(\d{1,4}))?行')
_L = re.compile(r'(?<![A-Za-z0-9_])L(\d{1,4})(?:\s?' + _D + r'\s?L?(\d{1,4}))?' + _尾)
_L续 = re.compile(r'\s?([、，,／])\s?L?(\d{1,4})(?:\s?' + _D + r'\s?L?(\d{1,4}))?' + _尾)
_白文 = re.compile(r'白文\s?第(\d{1,4})(?:\s?' + _D + r'\s?(\d{1,4}))?行')
_自行 = re.compile(r'(本章)?第(\d{1,4})(?:\s?' + _D + r'\s?(\d{1,4}))?行')
_行N = re.compile(r'(?<=[（(·｜|\s])行(\d{1,4})(?:\s?' + _D + r'\s?(\d{1,4}))?(?!\d)')
_NR = re.compile(r'NR\s*==\s*(\d{1,4})(?!\d)|NR\s*>=?\s*(\d{1,4})\s*&&\s*NR\s*<=?\s*(\d{1,4})(?!\d)'
                 r'|sed\s+-n\s+[\'"]?(\d{1,4})(?:\s*,\s*(\d{1,4}))?p')
_档名 = re.compile(r'第([零〇一二两三四五六七八九十百千]+)章[_…*][^\s`\'"）)|｜]*?\.md')   # 亦认「正文/…第三百一十三章….md」「正文/*第三百一十七章*.md」之略（案卷里已见）
_前章 = re.compile(r'(?<![\d:：.,\-=<>＝])(\d{2,3})(?![\d:：,])|第([零〇一二两三四五六七八九十百千]+)章')
_拍 = re.compile(r'(?<![\d拍第A-Za-z_\-.:：])(\d{1,3})(?![\d:：])[\s`*·→]{0,4}(?:章)?[\s·的之]{0,2}拍(\d{1,3})'
                r'(?:\s?[—–~～\-至](?![—–~～\-])\s?拍?(\d{1,3}))?(?!\d)')
_拍续 = re.compile(r'\s?\**\s?([、，／])\s?\**拍(\d{1,3})(?:\s?[—–~～\-至](?![—–~～\-])\s?拍?(\d{1,3}))?(?!\d)')
_自拍 = re.compile(r'(?<![\d第])拍(\d{1,3})(?:\s?[—–~～\-至](?![—–~～\-])\s?拍?(\d{1,3}))?(?!\d)')
_史标 = re.compile(r'旧号|改前|0929|D1\s*施前|施前|旧作|原作|已删|已治|旧书|陈号')
_时词 = re.compile(r'(凌晨|清晨|早上|早晨|上午|中午|正午|午后|下午|傍晚|黄昏|晚上|夜里|夜间|深夜|半夜|时刻|几点|钟点)\s?$')
_日前 = re.compile(r'(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}[ T]?|\d{1,2}月\d{1,2}[日号]\s?|(?<!\d)\d{4}\s)$')
_汉字 = re.compile(r'[一-鿿]')
_全角许 = set('见即照同承与及和於于在係系对比自')


def _端(m, *gs):
    return [(int(m.group(g)), m.start(g), m.end(g)) for g in gs if m.group(g)]


def 提(l, 境):
    """一行 → (诸引, 不认之计)。引＝{'式': '行'|'拍'|'自拍', '章', '端': [(值, 起, 止)…], '形'}；
    境：{'漂': {章: 旧长}, '默': 章|None, 'L': bool, '自': bool}——只认漂章（映非恒等者）。"""
    漂, 默 = 境['漂'], 境.get('默')
    引们, 占, 弃 = [], set(), collections.Counter()

    def 收(式, 章, 端, 形):
        if not 端 or any(s in 占 for _, s, _e in 端):
            return
        长 = 漂.get(章)
        if 长 is None:
            return
        if 式 == '行' and any(v < 1 or v > 长 for v, _s, _e in 端):
            弃['越界'] += 1
            return
        if len(端) == 2 and 端[1][0] < 端[0][0]:
            端 = 端[:1]                                   # 「a—b」而 b<a：不成区间，只认其头
        占.update(s for _, s, _e in 端)
        引们.append({'式': 式, '章': 章, '端': 端, '形': 形})

    # ①第X章第N行
    for m in _章章行.finditer(l):
        c = 汉转数(m.group(1))
        if c in 漂:
            收('行', c, _端(m, 2, 3), '第章第行')
    # ②章:行（续、区间）
    for m in _头.finditer(l):
        cs, ns = m.group(1), m.group(3)
        c = int(cs)
        if c not in 漂:
            continue
        前 = l[max(0, m.start() - 1):m.start()]
        后 = l[m.end():]
        if cs.startswith('0') or ns.startswith('0') or 前 in ('限', '拍', '第'):
            弃['非号'] += 1
            continue
        if m.group(2) == '：' and 前 and _汉字.match(前) and 前 not in _全角许:
            弃['非号'] += 1
            continue
        if re.match(r'[:：]\d', 后) or (c <= 24 and len(ns) == 2 and int(ns) <= 59 and (
                _时词.search(l[:m.start()]) or _日前.search(l[:m.start()]) or re.match(r'\s?(时|分|点钟|UTC|GMT|左右)', 后))):
            弃['时刻'] += 1
            continue
        if re.match(r',\d{3}(?!\d)', 后):
            弃['千分'] += 1
            continue
        if re.match(r'\s?−', 后) or re.search(r'−\s?$', l[:m.start()]):
            弃['算式'] += 1
            continue
        if int(ns) > 漂[c] or int(ns) == 0:
            弃['越界'] += 1
            continue
        端 = [(int(ns), m.start(3), m.end(3))]
        p = m.end()
        r = _区.match(l, p)
        if r:
            端.append((int(r.group(1)), r.start(1), r.end(1)))
            p = r.end()
        收('行', c, 端, '章:行')
        while True:
            q = _续.match(l, p)
            if not q:
                break
            后2 = l[q.end():]
            if re.match(r'[:：]\d', 后2):
                break                                       # 「、315:73」係新章之头
            if (q.group(1) or q.group(2) in ('，', '/', '与', '和', '及')) and not q.group(3):
                break                                       # 跨引文、逗号、「与／和／及」者须带「:」方认作续（「317:77「十九」与 :197」）
            if not q.group(3) and (re.match(r'\s?([' + ''.join(_单位) + '])', 后2) or (q.group(2) == ',' and len(q.group(4)) == 3)):
                break
            e = [(int(q.group(4)), q.start(4), q.end(4))] + ([(int(q.group(5)), q.start(5), q.end(5))] if q.group(5) else [])
            if any(v < 1 or v > 漂[c] for v, _s, _e in e):
                break
            收('行', c, e, '续')
            p = q.end()
    # ③awk/sed NR（⛔同行须有其章之正文档名）
    名们 = [(n.start(), 汉转数(n.group(1))) for n in _档名.finditer(l)]
    诸NR = list(_NR.finditer(l))
    for k, m in enumerate(诸NR):
        界 = 诸NR[k + 1].start() if k + 1 < len(诸NR) else len(l)
        c = next((cc for s, cc in 名们 if m.end() <= s < min(界, m.end() + 200)), None)
        if c is None and len(诸NR) == 1 and len({cc for _, cc in 名们}) == 1:
            c = 名们[0][1]                                  # 一行一 NR、一档名：档名在前亦认
        if c is None:
            if 名们 == [] and 漂:
                # ★1020·W58 驳席：无档名之 NR，其前最近之章号係漂章者入待判（⛔改：令「须同行有其章之档名」）——
                #   施工表:1264「313之末句……`awk 'NR==577'` 亲印」与 :1282 同句，一移一不移而⛔声即静漂
                前 = [x for x in _前章.finditer(l[:m.start()])]
                cc = (int(前[-1].group(1)) if 前[-1].group(1) else 汉转数(前[-1].group(2))) if 前 else None
                if re.search(r'\.(md|json|txt|py)\b', l[m.end():m.end() + 60].split('`')[0]):
                    cc = None                               # 「`awk 'NR==178' 设定/02_余章之势_总纲.md`」：NR 属他档
                if cc in 漂:
                    gs = [g for g in (1, 2, 3, 4, 5) if m.group(g)]
                    收('行', cc, _端(m, *gs), 'NR·疑')
                else:
                    弃['NR·无档名'] += 1
            continue
        if c in 漂:
            gs = [g for g in (1, 2, 3, 4, 5) if m.group(g)]
            收('行', c, _端(m, *gs), 'NR')
    # ④全书记忆 L 与白文第（默章）
    if 默 in 漂 and 境.get('L'):
        for m in _L.finditer(l):
            收('行', 默, _端(m, 1, 2), 'L')
            p = m.end()
            while True:
                q = _L续.match(l, p)
                if not q or re.match(r'\s?([' + ''.join(_单位) + '])', l[q.end():]):
                    break
                收('行', 默, _端(q, 2, 3), 'L续')
                p = q.end()
    if 默 in 漂 and (境.get('L') or 境.get('自')):
        for m in _白文.finditer(l):
            收('行', 默, _端(m, 1, 2), '白文第')
    if 默 in 漂 and 境.get('自'):
        for m in _自行.finditer(l):
            形 = '第N行'
            if not m.group(1):
                前 = l[:m.start()].rstrip('*`')
                if 前 and _汉字.match(前[-1]) and not 前.endswith(('白文', '本章')):
                    if 前.endswith('章') and not 前.endswith(('同章', '该章')):
                        continue                            # 「第七十三章第149行」：他章
                    形 = '第N行·疑'                         # ★1020·W58 驳席：「而第337行」（本章）与「施工表第273行」（他档）字面难分 → 入待判，⛔默弃
            收('行', 默, _端(m, 2, 3), 形)
        for m in _行N.finditer(l):
            收('行', 默, _端(m, 1, 2), '行N')
    # ⑤章号紧邻之拍
    for m in _拍.finditer(l):
        c = int(m.group(1))
        if c not in 漂:
            continue
        收('拍', c, _端(m, 2, 3), '拍')
        p = m.end()
        while True:
            q = _拍续.match(l, p)
            if not q:
                break
            收('拍', c, _端(q, 2, 3), '拍续')
            p = q.end()
    if 默 in 漂 and 境.get('自'):
        for m in _自拍.finditer(l):
            收('自拍', 默, _端(m, 1, 2), '拍·无章号')
    return 引们, 弃


# ───────── 局：映、旧正文、新正文、互证、拍映 ─────────
def _凡(l):
    return l.strip() in ('', '＊')


def 改作(a, b):
    if a == b:
        return True
    if not a.strip() or not b.strip():
        return False
    if a in b or b in a:
        return True
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() >= 0.5


def 拍号(行们):
    """照 器物点名.分拍（以「＊」分，章题行与亮点不入）→ ({行号: 拍号}, 拍数, 内联＊否)"""
    界 = next((k for k, l in enumerate(行们) if '【本章亮点】' in l), len(行们))
    题 = next((k for k, l in enumerate(行们[:8]) if re.search(r'第.+?章', l)), -1)
    号 = 0
    在 = 坏 = False
    出 = {}
    for k in range(题 + 1, 界):
        s = 行们[k].strip()
        if s == '＊':
            在 = False
            continue
        if '＊' in s:
            坏 = True
        if s:
            if not 在:
                号 += 1
                在 = True
            出[k + 1] = 号
    return 出, 号, 坏


class 局:
    def __init__(s, root, 映, ref='HEAD'):
        s.root, s.映 = root, 映
        s.旧 = 旧本(root, ref)
        s.章档 = 章档(root)
        s.红, s.注 = [], []
        s.旧文, s.新文, s.未施, s.拍映, s.旧拍, s.新拍, s.替 = {}, {}, {}, {}, {}, {}, {}
        s.漂 = {}
        s.互证计 = collections.Counter()
        for c, m in sorted(映.items()):
            rel = s.章档.get(c)
            if not rel:
                s.红.append('第%d章之正文不在 %s' % (c, root))
                continue
            W = _读(os.path.join(root, rel))
            O = s.旧.读(rel, W)
            if O is None:
                s.红.append('第%d章之正文旧本无之（%s）' % (c, rel))
                continue
            Ol, Wl = O.split('\n'), W.split('\n')
            s.旧文[c], s.新文[c] = Ol, Wl
            恒 = all(v == k for k, v in m.items())
            if 恒:
                if len(Ol) != len(Wl):
                    s.红.append('第%d章映为恒等而行数变了（%d→%d）' % (c, len(Ol), len(Wl)))
                continue
            s.漂[c] = len(Ol)
            if O == W:
                s.未施[c] = True
                continue
            s.未施[c] = False
            if max(m) not in (len(Ol), len(Ol) - (1 if Ol and Ol[-1] == '' else 0)):
                s.红.append('第%d章映之旧长 %d ≠ 旧正文 %d 行' % (c, max(m), len(Ol)))
                continue
            if max(v for v in m.values() if v is not None) > len(Wl):
                s.红.append('第%d章映之新号越出新正文（%d 行）' % (c, len(Wl)))
                continue
            等, 替 = {}, {}
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, Ol, Wl, autojunk=False).get_opcodes():
                if tag == 'equal':
                    for k in range(i2 - i1):
                        等[i1 + k + 1] = j1 + k + 1
                elif tag == 'replace':
                    for k in range(i2 - i1):
                        替[i1 + k + 1] = (j1 + 1, j2)          # 替块：旧行落在新块之内即两法相合（改、改＋后添之行）
            不合 = []
            for i, v in sorted(m.items()):
                if i > len(Ol) or _凡(Ol[i - 1]):
                    continue
                if v is None:
                    if i in 等:
                        不合.append('%d 映作删而新文犹在（新 %d）' % (i, 等[i]))
                    continue
                if i in 等 and 等[i] != v:
                    不合.append('%d→%d 而 difflib 作 %d（原文「%s」落於新 %d：改＋后添而原文在後段者，映须随原文）' % (
                        i, v, 等[i], Ol[i - 1].strip()[:12], 等[i]))
                elif not 改作(Ol[i - 1], Wl[v - 1]) and not (i in 替 and 替[i][0] <= v <= 替[i][1]):
                    不合.append('%d→%d 新行非旧文亦非其改作' % (i, v))
                else:
                    s.互证计['同' if Ol[i - 1] == Wl[v - 1] else '改作'] += 1
            s.替[c] = 替
            if 不合:
                s.红.append('第%d章映两法不合 %d 处：%s' % (c, len(不合), '；'.join(不合[:4])))
            o, on, ob = 拍号(Ol)
            n, nn, nb = 拍号(Wl)
            if on > 1 and not ob and not nb:
                bm = collections.defaultdict(set)
                for i, b in o.items():
                    v = m.get(i)
                    if v is not None and v in n:
                        bm[b].add(n[v])
                s.拍映[c] = {b: sorted(v) for b, v in bm.items()}
                s.旧拍[c] = o
                s.新拍[c] = n
        # 映外之章变行数（⛔只许映内之章变）
        诸正 = [r for c, r in s.章档.items() if c not in s.漂 and c not in 禁章]
        for rel in s.旧.改了的(诸正):
            W = _读(os.path.join(root, rel))
            O = s.旧.读(rel, W)
            if O is not None and len(O.split('\n')) != len(W.split('\n')):
                s.红.append('映外之章变了行数：%s（%d→%d）' % (rel, len(O.split('\n')), len(W.split('\n'))))
        s.已写 = set(s.章档)
        s.预 = re.compile('|'.join([r'(?<!\d)%d(?!\d)' % c for c in s.漂] + ['第%s章' % 数转汉(c) for c in s.漂])) if s.漂 else None

    # 号之移
    def 移(s, t):
        c, vs = t['章'], [v for v, _a, _b in t['端']]
        if t['式'] == '行':
            m = s.映[c]
            if len(vs) == 1:
                v = m.get(vs[0])
                return ([v], None) if v is not None else (None, '指删行')
            a, b = vs
            if m.get(a) is not None and m.get(b) is not None:
                return [m[a], m[b]], None
            活 = [m[i] for i in range(a, b + 1) if m.get(i) is not None]
            return ([活[0], 活[-1]], '缩') if 活 else (None, '全删')
        pm = s.拍映.get(c)
        if pm is None:
            return None, ('拍·未施' if s.未施.get(c) else '拍不可算')
        S = [pm.get(v) for v in vs]
        if any(not x for x in S):
            return None, '拍删'
        if len(vs) == 1:
            return ([S[0][0]], None) if len(S[0]) == 1 else ([S[0][0], S[0][-1]], '拍裂')
        return [S[0][0], S[1][-1]], None

    def 锚(s, t, 新):
        c = t['章']
        if s.未施.get(c):
            return '未施'
        O, W = s.旧文[c], s.新文[c]
        结 = []
        if t['式'] == '行':
            for (v, _a, _b), x in zip(t['端'], 新):
                a = O[v - 1] if 0 < v <= len(O) else None
                b = W[x - 1] if 0 < x <= len(W) else None
                if a is None or b is None:
                    结.append('异')
                elif a == b:
                    结.append('同' if a.strip() else '同·空')
                elif 改作(a, b):
                    结.append('改作')
                else:
                    块 = s.替.get(c, {}).get(v)
                    结.append('改作·块' if (块 and 块[0] <= x <= 块[1]) else '异')
        else:
            o, n = s.旧拍.get(c, {}), s.新拍.get(c, {})
            for (v, _a, _b), x in zip(t['端'], 新):
                a = ''.join(O[i - 1] for i, b in sorted(o.items()) if b == v)
                b = ''.join(W[i - 1] for i, bb in sorted(n.items()) if bb == x)
                结.append('同' if a == b else ('改作' if 改作(a, b) else '异'))
        for k in ('异', '改作·块', '改作', '同·空'):
            if k in 结:
                return k
        return '同'

    def 锚文(s, t, 新):
        c = t['章']
        if t['式'] != '行' or s.未施.get(c) or not 新:
            return ''
        W = s.新文[c]
        x = 新[0]
        return (W[x - 1].strip()[:16] if 0 < x <= len(W) else '')


# ───────── 扫 ─────────
def _骨(l):
    return re.sub(r'\d+', '#', l)


def _配(O, W):
    if O is None:
        return [None] * len(W)
    if O == W or len(O) == len(W):
        return list(range(len(W)))
    p = [None] * len(W)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, O, W, autojunk=False).get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(j2 - j1):
                p[j1 + k] = i1 + k
    return p


def _示(c, t, vs):
    if t['式'] == '行':
        if t['形'] in ('L', 'L续'):
            pre = 'L'
        elif t['形'].startswith('NR'):
            pre = '%d·NR' % c
        else:
            pre = '%d:' % c
    else:
        pre = '%d·拍' % c
    return pre + '—'.join(str(v) for v in vs)


def 扫(局_, 印弃=None):
    """→ (诸项, 计)。项：{'档', '行', '类', '旧', '新', '由', '锚', '文', '改': [(起, 止, 新数)]}"""
    s = 局_
    项们, 计 = [], collections.Counter()
    if not s.漂:
        return 项们, 计
    for rel in 诸档(s.root):
        k = 类(rel, s.已写)
        if k in ('史', '卷', '禁', '免扫'):
            continue
        p = os.path.join(s.root, rel)
        try:
            W文 = _读(p)
        except Exception:
            continue
        O文 = s.旧.读(rel, W文)
        W = W文.split('\n')
        O = O文.split('\n') if O文 is not None else None
        名 = os.path.basename(rel)
        默, L = None, False
        mm = re.match(r'设定/全书记忆/第(\d+)章\.md$', rel)
        if mm and int(mm.group(1)) in s.漂:
            默, L = int(mm.group(1)), True
        区 = None                                            # 只扫之行（None＝全档）
        if k == '文':
            m2 = re.search(r'第([零〇一二两三四五六七八九十百千]+)章', 名)
            c2 = 汉转数(m2.group(1)) if m2 else None
            wj = next((j for j, l in enumerate(W) if '【本章亮点】' in l), None)
            oj = next((i for i, l in enumerate(O) if '【本章亮点】' in l), None) if O else None
            if wj is None:
                计['正文无亮点标'] += 1
                continue
            区 = (wj, oj)
            if c2 in s.漂:
                默 = c2
        码行 = _码之行(W文, 名) if k == '码' else None
        施工 = 名.startswith('01_') and '施工' in 名 and rel.startswith('设定/')
        链 = rel.startswith('设定/全书记忆/人物链/')       # 人物链.py --并记 自章记并来；其 L 照章记同移（重并亦得同号）
        免 = set()
        if rel == 二稿账:
            j0 = next((j for j, l in enumerate(W) if _免节.match(l)), None)
            if j0 is not None:
                j1 = next((j for j in range(j0 + 1, len(W)) if re.match(r'^#{2,3}\s', W[j])), len(W))
                免 = set(range(j0, j1))
        配 = _配(O, W)
        for j, w in enumerate(W):
            if 区 and (j < 区[0]):
                continue
            if 码行 is not None:
                if (j + 1) not in 码行:
                    continue
                w = 码行[j + 1]
            i = 配[j]
            if 区 and i is not None and (区[1] is None or i < 区[1]):
                i = None
            o = O[i] if i is not None else None
            if 码行 is not None and o is not None:
                o = w if o == W[j] else _码之行(O文, 名).get(i + 1, '')
            境 = {'漂': s.漂, '默': 默, 'L': L, '自': False}
            if k == '文' and 默:
                境['自'] = True
            if 施工:
                r = re.match(r'^\|\s*(\d{1,3})\s*\|\s*锁定\s*\|', w)
                if r and int(r.group(1)) in s.漂:
                    境['默'], 境['自'] = int(r.group(1)), True
            if 链:
                r = re.match(r'^\s*[-*]?\s*〔(\d{1,3})·', w)          # ★1020·W58 驳席：人物链之条「- 〔313·主〕……（L161）」——L 係其章之行
                if r and int(r.group(1)) in s.漂:
                    境['默'], 境['L'] = int(r.group(1)), True
            if not 境['默'] and not re.search(r'\d', w):
                continue
            if not 境['默'] and not s.预.search(w) and not (o and s.预.search(o)):
                continue
            史 = bool(_史标.search(w))

            def 出(t, 新, 由, 类名, 改=None, 锚='', 旧vs=None):
                vs = 旧vs or [v for v, _a, _b in t['端']]
                项们.append({'档': rel, '行': j + 1, '类': 类名, '旧': _示(t['章'], t, vs),
                             '新': _示(t['章'], t, 新) if 新 else '', '由': 由 or '', '锚': 锚,
                             '文': s.锚文(t, 新) if 新 else '', '改': 改 or [], '式': t['形']})

            def 判(t, w端):
                """t：旧号之引（其端在 w 之 w端 处）→ 一项"""
                新, 由 = s.移(t)
                vs = [v for v, _a, _b in t['端']]
                if 新 == vs and not 由:
                    return
                if j in 免:
                    出(t, 新, '0929锚节·⛔移', '免')
                elif 史:
                    出(t, 新, '史标', '待判')
                elif k == '码':
                    出(t, 新, '器码', '待判')
                elif t['形'].endswith('·疑'):
                    出(t, 新, {'NR·疑': 'NR·无档名（据其前之章号）'}.get(t['形'], '本章抑他档不明') + ('·' + 由 if 由 else ''), '待判')
                elif 由:
                    出(t, 新, 由, '待判')
                elif t['式'] == '自拍':
                    出(t, 新, '拍·无章号', '待判')
                else:
                    a = s.锚(t, 新)
                    if a == '异':
                        出(t, 新, '锚异', '待判', 锚=a)
                    else:
                        改 = [(b0, b1, str(x)) for (_v, b0, b1), x in zip(w端, 新) if _v != x]
                        出(t, 新, '', '移', 改=改, 锚=a)

            if o is not None and o == w:
                ts, 弃 = 提(o, 境)
                计.update(弃)
                for t in ts:
                    判(t, t['端'])
            elif o is not None and _骨(o) == _骨(w):
                ts, 弃 = 提(o, 境)
                计.update(弃)
                ro = [x.span() for x in re.finditer(r'\d+', o)]
                rw = list(re.finditer(r'\d+', w))
                for t in ts:
                    idx = [ro.index((a, b)) if (a, b) in ro else None for _v, a, b in t['端']]
                    if None in idx:
                        continue
                    w端 = [(int(rw[x].group()), rw[x].start(), rw[x].end()) for x in idx]
                    wv = [v for v, _a, _b in w端]
                    vs = [v for v, _a, _b in t['端']]
                    if wv == vs:
                        判(t, w端)
                        continue
                    新, 由 = s.移(t)
                    if 新 and wv == 新 and not 由:
                        a = s.锚(t, 新) if t['式'] != '自拍' else '同'
                        出(t, 新, '' if a != '异' else '锚异', '已移', 锚=a, 旧vs=vs)
                    else:
                        出(dict(t, 端=w端), None, '他改（旧 %s）' % _示(t['章'], t, vs), '待判')
            else:
                ts_o, 弃 = (提(o, 境) if o is not None else ([], {}))
                ts_w, 弃w = 提(w, 境)
                计.update(弃w)
                旧键, 新键 = {}, {}
                for t in ts_o:
                    新, 由 = s.移(t)
                    vs = [v for v, _a, _b in t['端']]
                    if 新 == vs and not 由:
                        continue
                    旧键[(t['式'], t['章'], tuple(vs))] = t
                    if 新:
                        新键[(t['式'], t['章'], tuple(新))] = (t, 新, 由)
                for t in ts_w:
                    key = (t['式'], t['章'], tuple(v for v, _a, _b in t['端']))
                    if key in 新键 and key not in 旧键:
                        t0, 新, 由 = 新键[key]
                        a = s.锚(t0, 新) if t0['式'] != '自拍' else '同'
                        出(t0, 新, 由 or ('' if a != '异' else '锚异'), '已移', 锚=a, 旧vs=list(key[2]))
                    elif key in 旧键 and key in 新键:
                        新, 由 = s.移(t)
                        出(t, 新, '两可（旧新同号）', '待判')
                    elif key in 旧键:
                        判(t, t['端'])
                    else:
                        新, 由 = s.移(t)
                        vs = list(key[2])
                        if 新 != vs or 由:
                            出(t, 新, '新引（新旧不明）' + ('·' + 由 if 由 else ''), '待判')
    return 项们, 计


def 史档未动(局_):
    """史、卷、禁之档：与旧本比，凡「只改了数字」之行即红（随移⛔碰史档）。"""
    s = 局_
    诸 = [r for r in 诸档(s.root) if 类(r, s.已写) in ('史', '卷', '禁')]
    坏 = []
    for rel in s.旧.改了的(诸):
        W = _读(os.path.join(s.root, rel)).split('\n')
        O = (s.旧.读(rel) or '').split('\n')
        配 = _配(O, W)
        for j, w in enumerate(W):
            i = 配[j]
            if i is not None and O[i] != w and _骨(O[i]) == _骨(w):
                坏.append('%s:%d' % (rel, j + 1))
    return 坏


# ───────── 施 ─────────
def 施(局_, 项们):
    """只改数字：逐档逐行由右而左换；行数、骨（去数字之形）逐行验；json 之档施後须仍可读。→ (改处, 改档, 红)"""
    按档 = collections.defaultdict(lambda: collections.defaultdict(list))
    for x in 项们:
        if x['类'] == '移':
            for a, b, n in x['改']:
                按档[x['档']][x['行']].append((a, b, n))
    改处 = 0
    红 = []
    for rel, 行改 in sorted(按档.items()):
        p = os.path.join(局_.root, rel)
        原 = _读(p)
        行们 = 原.split('\n')
        for j, 改们 in 行改.items():
            l = 行们[j - 1]
            新 = l
            for a, b, n in sorted(set(改们), reverse=True):
                if not 新[a:b].isdigit():
                    红.append('%s:%d 之 %d—%d 非数字' % (rel, j, a, b))
                    break
                新 = 新[:a] + n + 新[b:]
                改处 += 1
            if _骨(新) != _骨(l):
                红.append('%s:%d 施後之骨变了' % (rel, j))
            行们[j - 1] = 新
        出 = '\n'.join(行们)
        if len(出.split('\n')) != len(原.split('\n')):
            红.append('%s 行数变了' % rel)
        if rel.endswith('.json'):
            try:
                json.loads(出)
            except Exception as e:
                红.append('%s 施後非合式 JSON：%s' % (rel, e))
        if 红:
            break
        tmp = p + '.随移tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(出)
        os.replace(tmp, p)
    return 改处, len(按档), 红


# ───────── 印 ─────────
def _计类(项们):
    return collections.Counter(x['类'] for x in 项们)


def 印(局_, 项们, 计, 全=False, 头=''):
    s = 局_
    print('════ 行号随移%s（根：%s；旧：%s）════' % (头, s.root, s.旧.目 or s.旧.ref))
    for c in sorted(s.映):
        m = s.映[c]
        if c not in s.漂:
            continue
        删 = sum(1 for v in m.values() if v is None)
        移 = sum(1 for k, v in m.items() if v is not None and v != k)
        print('  映·%d：旧 %d 行（移 %d、删 %d）%s' % (c, len(m), 移, 删, '·正文未施' if s.未施.get(c) else '·新 %d 行' % len(s.新文[c])))
    print('  两法互证：%s（同 %d、改作 %d）' % ('⛔' if s.红 else '✓', s.互证计['同'], s.互证计['改作']))
    for x in s.红:
        print('     ⛔ ' + x)
    cc = _计类(项们)
    for 名 in ('移', '待判', '免', '已移'):
        xs = [x for x in 项们 if x['类'] == 名]
        if not xs:
            continue
        档数 = len({x['档'] for x in xs})
        print('  ── %s %d 处（%d 档）' % (名, len(xs), 档数))
        if 名 == '已移' and not 全:
            异 = [x for x in xs if x['锚'] == '异']
            print('     锚：%s' % '、'.join('%s %d' % (k, v) for k, v in collections.Counter(x['锚'] for x in xs).most_common()))
            for x in 异:
                print('     ⛔ %s:%d｜%s→%s｜锚异' % (x['档'], x['行'], x['旧'], x['新']))
            continue
        for x in xs:
            if 名 == '移':
                print('     %s:%d｜%s→%s｜锚：%s「%s」' % (x['档'], x['行'], x['旧'], x['新'], x['锚'], x['文']))
            else:
                print('     %s:%d｜%s→%s｜由：%s' % (x['档'], x['行'], x['旧'], x['新'] or '？', x['由']))
    无标 = 计.pop('正文无亮点标', 0)
    if 计:
        print('  不认：%s' % '、'.join('%s %d' % (k, v) for k, v in sorted(计.items())))
    if 无标:
        print('  注：正文无「【本章亮点】」之标者 %d 档（无亮点段可扫）' % 无标)
    return cc


def _参(argv, 名):
    if 名 in argv:
        k = argv.index(名)
        return argv[k + 1] if k + 1 < len(argv) else None
    return None


def 主(argv):
    式 = next((a for a in argv if a in ('--扫', '--施', '--验')), None)
    if not 式:
        print(__doc__)
        return 2
    根 = _参(argv, '--根')
    if 式 == '--施' and not 根:
        print('⛔行号随移 --施：须明给 --根（副本或落盘之仓之路）——⛔无 --根 即拒（不默写本仓）')
        return 2
    root = os.path.abspath(根) if 根 else ROOT
    映p = _参(argv, '--映') or 映档
    if not os.path.isabs(映p):
        映p = os.path.join(root, 映p)
    if not os.path.isfile(映p):
        print('⛔行号随移：无映（%s）——⛔无映即拒' % 映p)
        return 2
    try:
        映 = 读映(映p)
        局_ = 局(root, 映, _参(argv, '--旧') or 'HEAD')
    except ValueError as e:
        print('⛔行号随移：%s——拒' % e)
        return 2
    项们, 计 = 扫(局_)
    cc = 印(局_, 项们, 计, 全=('--全' in argv), 头={'--扫': '·扫', '--施': '·施', '--验': '·验'}[式])
    出p = _参(argv, '--出')
    if 出p:
        json.dump({'项': 项们, '不认': dict(计), '红': 局_.红}, open(出p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    异 = sum(1 for x in 项们 if x['由'] == '锚异')
    if 式 == '--扫':
        末 = '移 %d、待判 %d、免 %d、已移 %d、不认 %d' % (cc['移'], cc['待判'], cc['免'], cc['已移'], sum(计.values()))
        if 局_.红 or 异:
            print('⛔行号随移·扫：互证 %d 红、锚异 %d——%s' % (len(局_.红), 异, 末))
            return 1
        print('✓行号随移·扫：%s%s' % (末, '（正文未施：锚未验）' if any(局_.未施.values()) else ''))
        return 0
    if 式 == '--施':
        if 局_.红 or 异 or any(局_.未施.values()):
            print('⛔行号随移·施：拒——互证 %d 红、锚异 %d、正文未施 %d 章' % (len(局_.红), 异, sum(局_.未施.values())))
            return 1
        改处, 改档, 红 = 施(局_, 项们)
        if 红:
            for x in 红:
                print('     ⛔ ' + x)
            print('⛔行号随移·施：%d 红，止於首红之档' % len(红))
            return 1
        局_.旧.刷()
        二, _计 = 扫(局_)
        c2 = _计类(二)
        print('  二跑：移 %d、已移 %d、待判 %d' % (c2['移'], c2['已移'], c2['待判']))
        if c2['移']:
            print('⛔行号随移·施：改 %d 处（%d 档），而二跑仍有 %d 处——⛔零改不成' % (改处, 改档, c2['移']))
            return 1
        print('✓行号随移·施：改 %d 处（%d 档·只改数字·行数不变）；二跑零改；待判 %d 处另交' % (改处, 改档, c2['待判']))
        return 0
    坏 = 史档未动(局_)
    for x in 坏[:20]:
        print('     ⛔ 史档只改了数字：' + x)
    已异 = sum(1 for x in 项们 if x['类'] == '已移' and x['锚'] == '异')
    if 局_.红 or 异 or 已异 or cc['移'] or 坏 or any(局_.未施.values()):
        print('⛔行号随移·验：互证 %d 红、未施 %d 章、未移 %d 处、已移锚异 %d、史档只改数字 %d 行' % (
            len(局_.红), sum(局_.未施.values()), cc['移'], 已异 + 异, len(坏)))
        return 1
    锚计 = collections.Counter(x['锚'] for x in 项们 if x['类'] == '已移')
    print('✓行号随移·验：已移 %d 处锚俱合（%s）；二跑零改；史档未动；互证 ✓（待判 %d、免 %d 另交）' % (
        cc['已移'], '、'.join('%s %d' % kv for kv in 锚计.most_common()) or '无', cc['待判'], cc['免']))
    return 0


if __name__ == '__main__':
    sys.exit(主(sys.argv[1:]))
