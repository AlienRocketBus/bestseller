#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1施（1020 立·W58）——D1 老头之年五审之换齐：核、窗、施（只於副本）、行数守、终验。零 token。

为何立：D1 五审之裁（`设定/剧情庭_D1_老头之年.md`·改单#G0929-01）定「那一趟挪到四十八年前」，其执行之表三张——
  §八 A 特改（主案 133 行，以裁档五审§丙覆十一、增十九 → 执行 152 行）、B 机械换数（白文「二十七年」→「四十八年」）、
  C1 亮点之换数（`设定/剧情庭题/D1_老头之年_五审主案.md` §八）；二稿账:91「一次换齐；⛔分两回落」。
  表係 0929 之章:行与原文子串立锚——**抄错一字、落错一行，比不落还坏**；而 103、104、196、313、317 五章照裁真另起段
  （`设定/裁_1020_D1落式.md` 一、二），行号要漂。故立本器：落盘以前逐条验，验过才施；施则一次写盘、吐映。
  ★还账.py 之「行数不变」之律照守（⛔动其码）；D1 之律另立於此（方案 W58 环 2①⑥）。

式（照裁，⛔改其式）：
  · 换（改）：「原」在该行恰一见，换作「改」；B、C1 之换数：该行「二十七年」全换「四十八年」（一行多处者全换，处数须合表）。
  · 段（后添）：该行照留，其後另起段——空行＋段；以「＊」逐段相隔之章（313、317）作 空行＋＊＋空行＋段；
    196 ⛔加「＊」（裁_1020 二·1）；连书之「〔另起段〕〔另起段〕」只作一次。
  · 改段（改＋后添）：「原」换作改作之首段，余段照「段」之式另起。
  · 删段（删）：整行删，连删其隔空行（其後之空行；无则其前）——103:178 删二行、317:259—266 删八行，⛔留连空。
  · 行差：只五章变——103 +28、104 +2、196 +8、313 +12、317 0；余章 0（不合即红）。

验（红即⛔施）：
  ① A：原文为该行之子串、恰一见 → 合；不在该行而在该章白文恰一见 → 移（重锚，黄）；已在该行者为改作（或所添之段已逐段整行在该章；
     改作含原文者以改作在否先判——★驳席补，⛔二跑判合／移而再施）→ 已施
     （211:89·edb78d69，W52 之还账已落）；余 → 无（红，交总编辑裁）；「删」须整行；照留只核其在。
  ② 字形：改作有「後」而该章白文无「後」、或有「后」而无「后」 → 红。
  ③ B 由今文自算：白文含「二十七年」之行减 A 之行（照今行），须＝主案 B 表减 187:245（出 B 入 A），逐行逐处同。
  ④ C1 由亮点行算：亮点与批注层含「二十七年」之行，减 C2 之送信（111:374、123:398 各三处作「四十五年」），须＝主案 C1。
  ⑤ 盖：白文「二十七年」207 处＝A 之原文所含＋B；A 之改作⛔含「二十七年」。
  ⑥ 定数：A 执行 152、B 167 行 172 处 73 章、C1 62 行 155 处、章 95（白文＋亮点）——数不合即红。
  ⑦ 基线：95 章之 blob 哈希（git hash-object 同算）记於 `设定/_草/W58/基线.json`（只 --写基线 写）；--施 前逐章比，异即红。
⛔限：只验「抄得对不对、落得对不对、行号漂得合不合映」；文气之缝由缝审席看窗（--窗）；在役诸档之引随移归 `工具/行号随移.py`。

用法：
  python3 工具/D1施.py --核 [--根 R] [--写基线]              # 对 R（默本仓）之今文核 A／B／C1／字形／盖／定数，并内存模拟施後之行差、六式、canon 禁式
  python3 工具/D1施.py --窗 [--根 R] [--出 目] [--批 B] [--亮]  # 窗_换.md（行内之改）、窗_段.md（增删段）→ --出（默 scratchpad；⛔写主树）
  python3 工具/D1施.py --施 --根 副本 [--批 一|二|三|全] [--亮] [--同步] [--基线 档] [--落]
        # 只在 --根 所指之副本施（⛔无 --根 即拒；--根 为主树须另加 --落——W58 只干跑，落归 W59；--落 而无基线即红）；一次写盘；吐映 <根>/设定/剧情庭题/D1_行号映.json
        # 批：一＝B 独之 61 章；二＝A 行数不变之 29 章；三＝五章；全＝95 章。--亮：并施 C1（C2 送信两行留待撰）；--同步：施後接 还账.施後同步（补接坐 1027 随接坐记汰）
  python3 工具/D1施.py --行数守 [--根 R] [--旧 HEAD]          # 正文、设定逐档行数比 HEAD（git show）；五章之变须合映（行数、内容锚）
  python3 工具/D1施.py --终验 [--根 R] [--旧 HEAD]            # 六式（二稿账 D1 节）残 0 ＋ canon 禁式（F002、F154、F168）新命中 0 ＋ 护三拍未压
  python3 工具/D1施.py --改单 单.json --根 副本 [--验] [--落]
        # ★1021·W58 环2：4b／4c／4d 之模型之改照单施——单＝JSON 列 [{档, 行（施後之号）, 原（该行里恰一见）, 新, 据（4b|4c|4d）, 由}]
        # 该行恰一见即施；该行无则容 ±3 之移而恰一见；原已不在而新在＝已施（二跑零改）；余即红、全单一字不写
        # ⛔无 --根 即拒；--根 为主树须另加 --落（--验 只核不写，许）；⛔插行、⛔删行；施毕印改数。负测：工具/负测_D1施改单.py
  python3 工具/D1施.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, hashlib, subprocess, tempfile, collections, time, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
主树 = '/home/user/the-novel'                     # ★1020·W58：铁律——W58 ⛔於主树施；W59 之落另加 --落
主案 = os.path.join('设定', '剧情庭题', 'D1_老头之年_五审主案.md')
裁档 = os.path.join('设定', '剧情庭_D1_老头之年.md')
映档 = os.path.join('设定', '剧情庭题', 'D1_行号映.json')   # 在史档之列（设定/剧情庭题/D），免被诸扫误读（方案 W58 定式 3）
基线档 = os.path.join('设定', '_草', 'W58', '基线.json')
canon档 = os.path.join('设定', 'canon事实库.json')
默出 = '/tmp/claude-0/-home-user-the-novel/2f785fc3-f03f-5b56-ad3f-32a68833152c/scratchpad/w58/窗'   # 本席之 scratchpad；不在则落 tmp
旧式, 新式 = '二十七年', '四十八年'
批名 = {'一': '一', '1': '一', '二': '二', '2': '二', '三': '三', '3': '三', '全': '全', 'all': '全'}

# ★1020·W58：诸定数皆照裁（裁_1020_D1落式 一、二；方案 W58 定式 1；二稿账:81）——⛔据今文自改其数
默配 = dict(
    五章=(103, 104, 196, 313, 317),
    星章=(313, 317),                                  # 以「＊」逐段相隔之章；196 ⛔加（裁_1020 二·1）
    定差={103: 28, 104: 2, 196: 8, 313: 12, 317: 0},
    定删={103: [178, 179], 317: list(range(259, 267))},
    定数=dict(A主=133, 覆=11, 增=19, A执=152, B主行=168, B主处=173, B行=167, B处=172, B章=73,
            白处=207, C1行=62, C1处=155, 章=95, 批一=61, 批二=29),
    已知已施={(211, 89): 'edb78d69'},
    出B入A=(187, 245),
    C2送信={(111, 374): 3, (123, 398): 3},           # 主案 C1 首：送信之年三处复述，移入 C2 作「四十五年」（撰）
)


# ───────── 章与文 ─────────
_汉 = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def 汉转数(s):
    n = c = 0
    for ch in s:
        if ch in _汉:
            c = _汉[ch]
        elif ch == '十':
            n += (c or 1) * 10; c = 0
        elif ch == '百':
            n += c * 100; c = 0
        else:
            return None
    return n + c


def 章号(rel):
    m = re.match(r'^(?:正文/)?镇冢秘术_第(.+?)章_.*\.md$', rel)
    return 汉转数(m.group(1)) if m else None


def 章档们(根):
    """→ {章: 'rel'}（只认 正文/镇冢秘术_第N章_*.md）"""
    出 = {}
    d = os.path.join(根, '正文')
    for f in (os.listdir(d) if os.path.isdir(d) else []):
        n = 章号(f)
        if n:
            出[n] = os.path.join('正文', f)
    return 出


def 拆(t):
    有尾 = t.endswith('\n')
    ls = t.split('\n')
    if 有尾:
        ls.pop()
    return ls, 有尾


def 合(ls, 有尾):
    return '\n'.join(ls) + ('\n' if 有尾 else '')


def 白界(ls):
    return next((k for k, l in enumerate(ls) if '【本章亮点】' in l), len(ls))


def 白(l):
    return not re.match(r'^\s*(★|\*\*|⛔|\||#)', l)


def 白文行(ls):
    """→ [(行号, 行)]：「【本章亮点】」以前、而不以 ★／**／⛔／|／# 起首之行（主案 §十一）"""
    return [(k + 1, ls[k]) for k in range(白界(ls)) if 白(ls[k])]


def blob(data):
    return hashlib.sha1(b'blob %d\x00' % len(data) + data).hexdigest()


def _git(根, *a, 入=None):
    # ★1020·W58 驳席：--no-optional-locks——diff／ls-files 之机会式刷 index 要取 index.lock；对主树跑（W59、或与写章之席并行）⛔与人之 commit 撞锁
    return subprocess.run(['git', '--no-optional-locks', '-c', 'core.quotepath=off'] + list(a), cwd=根, input=入, capture_output=True)


def 旧文们(根, rels, rev='HEAD'):
    """git cat-file --batch → {rel: 文 或 None}（rev 中无此档者 None）"""
    rels = list(rels)
    if not rels:
        return {}
    p = _git(根, 'cat-file', '--batch', 入=''.join('%s:%s\n' % (rev, r) for r in rels).encode('utf-8'))
    出, b, i = {}, p.stdout, 0
    for r in rels:
        j = b.index(b'\n', i)
        头 = b[i:j].split()
        i = j + 1
        if len(头) < 3 or 头[1] != b'blob':
            出[r] = None
            continue
        n = int(头[2])
        出[r] = b[i:i + n].decode('utf-8')
        i += n + 1
    return 出


class 书:
    """一个根之正文：工作区（rev=None）或某 rev（git cat-file）。"""

    def __init__(self, 根, rev=None, 文们=None):
        self.根, self.rev = 根, rev
        if 文们 is not None:                         # 自测：{章: 文}
            self.档 = {n: '正文/镇冢秘术_第%d章_测.md' % n for n in 文们}
            self._文 = dict(文们)
            return
        if rev:
            ls = _git(根, 'ls-tree', '-r', '--name-only', rev, '--', '正文').stdout.decode('utf-8').split('\n')
            self.档 = {章号(x): x for x in ls if 章号(x)}
        else:
            self.档 = 章档们(根)
        self._文 = {}

    def 文(self, n):
        if n not in self._文:
            rel = self.档.get(n)
            if rel is None:
                self._文[n] = None
            elif self.rev:
                self._文.update({章号(k): v for k, v in 旧文们(self.根, [rel], self.rev).items()})
            else:
                self._文[n] = open(os.path.join(self.根, rel), encoding='utf-8').read()
        return self._文[n]

    def 预取(self):
        缺 = [n for n in self.档 if n not in self._文]
        if self.rev and 缺:
            for k, v in 旧文们(self.根, [self.档[n] for n in 缺], self.rev).items():
                self._文[章号(k)] = v
        else:
            for n in 缺:
                self.文(n)
        return self

    def 行(self, n):
        t = self.文(n)
        return 拆(t)[0] if t is not None else None


# ───────── 表 ─────────
def _段(行们, 起, 止):
    i = next((k for k, l in enumerate(行们) if l.startswith(起)), None)
    if i is None:
        return []
    j = next((k for k in range(i + 1, len(行们)) if 行们[k].startswith(止)), len(行们))
    return 行们[i:j]


def _格(l):
    return [x.strip() for x in l.strip().strip('|').split('|')]


式们 = ('改', '改＋后添', '后添', '删', '照留')


def _式(s):
    return s.replace('後', '后').replace('+', '＋').strip()


def 段们(改):
    """改作 → 诸段（〔另起段〕连书只作一次；⛔生空段）"""
    return [x for x in re.split(r'(?:〔另起段〕)+', 改) if x != '']


def 读表(主文, 裁文, 配=默配):
    """→ dict(A主, 丙, A执, B主, C1, 红)。A执＝主案 A 覆以裁丙「覆」、增以「新」。"""
    红 = []
    主 = 主文.split('\n')
    裁 = 裁文.split('\n')
    A主 = []
    for l in _段(主, '### A　', '### B　'):
        m = re.match(r'^\|\s*(\d{1,3}):(\d+)\s*\|', l)
        if m:
            c = _格(l)
            A主.append(dict(章=int(m.group(1)), 行=int(m.group(2)), 式=_式(c[1]), 原=c[2], 改=c[3], 出='主案'))
    丙 = []
    for l in _段(裁, '## 丙、', '## 丁、'):
        m = re.match(r'^\|\s*(\d{1,3}):(\d+)\s*\|', l)
        if m:
            c = _格(l)
            丙.append(dict(章=int(m.group(1)), 行=int(m.group(2)), 式=_式(c[1]), 类=c[2], 原=c[3], 改=c[4], 出='裁丙'))
    for o in A主 + 丙:
        if o['式'] not in 式们:
            红.append('%s %d:%d 式「%s」不认' % (o['出'], o['章'], o['行'], o['式']))
    键主 = collections.Counter((o['章'], o['行']) for o in A主)
    for k, v in 键主.items():
        if v > 1:
            红.append('主案 A 表 %d:%d 两见' % k)
    覆 = {(o['章'], o['行']) for o in 丙 if o.get('类') == '覆'}
    for o in 丙:
        k = (o['章'], o['行'])
        if o.get('类') == '覆' and k not in 键主:
            红.append('裁丙 %d:%d 类「覆」而主案无此行' % k)
        if o.get('类') == '新' and k in 键主:
            红.append('裁丙 %d:%d 类「新」而主案已有此行' % k)
        if o.get('类') not in ('覆', '新'):
            红.append('裁丙 %d:%d 类「%s」不认' % (k[0], k[1], o.get('类')))
    A执 = sorted([o for o in A主 if (o['章'], o['行']) not in 覆] + 丙, key=lambda o: (o['章'], o['行']))
    B主 = []
    for l in _段(主, '### B　', '### C　'):
        m = re.match(r'^\|\s*(\d+)\s*\|\s*([\d、×]+)\s*\|', l)
        if m:
            for x in m.group(2).split('、'):
                mm = re.match(r'(\d+)(?:×(\d+))?$', x.strip())
                B主.append(dict(章=int(m.group(1)), 行=int(mm.group(1)), 处=int(mm.group(2) or 1)))
    C1 = []
    C1文 = next((l for l in _段(主, '### C　', '### D　') if l.startswith('**C1')), '')
    if not C1文:
        红.append('主案 §八 C 无「**C1」之行')
    for x in (C1文.split('**：', 1)[1] if '**：' in C1文 else '').rstrip('。').split('；'):
        m = re.match(r'(\d+):(\d+)(?:×(\d+))?', x.strip())
        if m:
            C1.append(dict(章=int(m.group(1)), 行=int(m.group(2)), 处=int(m.group(3) or 1)))
    数 = 配.get('定数')
    if 数:
        for 名, 实 in (('A主', len(A主)), ('覆', len(覆)), ('增', sum(1 for o in 丙 if o.get('类') == '新')), ('A执', len(A执)),
                       ('B主行', len(B主)), ('B主处', sum(o['处'] for o in B主))):
            if 实 != 数[名]:
                红.append('定数 %s：表得 %d，裁 %d' % (名, 实, 数[名]))
    return dict(A主=A主, 丙=丙, A执=A执, B主=B主, C1=C1, 红=红)


def 读表根(根, 配=默配):
    return 读表(open(os.path.join(根, 主案), encoding='utf-8').read(), open(os.path.join(根, 裁档), encoding='utf-8').read(), 配)


# ───────── 核 ─────────
def 已添(o, ls, 界):
    """★1020·W58 驳席：后添、改段之二跑——锚文施後照留（後添）或被挪到所添之末段（317:133 之改段，末段即原文），
    旧式遂判「合」或「移」而再添一回，只靠同批别处之红挡住。今：所添诸段（⛔原文本身）已逐段整行在该章 → 已施。
    改段无原文以外之余段者（317:133），以其首段（换原文之段）整行在否判之。→ 首段所在之行 或 None"""
    段 = 段们(o['改'])
    if o['式'] == '后添':
        新 = [s for s in 段 if s != o['原']]
    elif o['式'] == '改＋后添':
        新 = [s for s in 段[1:] if s != o['原']] or 段[:1]
    else:
        return None
    if not 新:
        return None
    行 = {}
    for k in range(界):
        if 白(ls[k]):
            行.setdefault(ls[k].strip(), k + 1)
    return 行[新[0].strip()] if all(s.strip() in 行 for s in 新) else None


def 核一(o, ls):
    """→ (状, 今行, 注)。状 ∈ 合、移、已施、照留、无、多见、章不在、删非整行"""
    if ls is None:
        return ('章不在', None, '')
    n, 原 = o['行'], o['原']
    界 = 白界(ls)
    at = ls[n - 1] if 1 <= n <= len(ls) else None
    def 数(l):
        return (1 if l.strip() == '＊' else 0) if 原 == '＊' else l.count(原)
    if o['式'] == '照留':
        return ('照留', n, '') if at is not None and 数(at) == 1 else ('无', None, '照留之原文不在该行')
    # ★1020·W58 驳席：改作含原文者（111:273「那个人也到过老头家。」＋原文）施後原文仍在该行恰一见——⛔判「合」再换一回
    if o['式'] == '改' and at is not None and 原 in o['改'] and o['改'] in at:
        return ('已施', n, '改作含原文，而该行已是改作')
    添 = 已添(o, ls, 界)
    if 添:
        return ('已施', 添, '所添之段已逐段在该章（首段於 %d 行）' % 添)
    if at is not None and 数(at) == 1:
        if o['式'] == '删' and at.strip() != 原:
            return ('删非整行', n, '「删」＝整行删，而该行另有他字')
        return ('合', n, '')
    if at is not None and 数(at) > 1:
        return ('多见', n, '原文在该行 %d 见' % 数(at))
    改 = o['改'] if o['式'] == '改' else ''
    if 改 and at is not None and 改 in at:
        return ('已施', n, '')
    if 原 != '＊':
        诸 = [k + 1 for k in range(界) if 原 in ls[k] and 白(ls[k])]      # ★驳席：「在该章白文恰一见」——⛔移到 ★／** 批注之行
        if len(诸) == 1 and ls[诸[0] - 1].count(原) == 1:
            return ('移', 诸[0], '%+d' % (诸[0] - n))
        if len(诸) > 1:
            return ('无', None, '原文在该章白文 %d 行见（%s），⛔猜' % (len(诸), '、'.join(map(str, 诸[:6]))))
    if 改:
        诸 = [k + 1 for k in range(界) if 改 in ls[k] and 白(ls[k])]
        if len(诸) == 1:
            return ('已施', 诸[0], '於 %d 行' % 诸[0])
    return ('无', None, '原文不在该章白文')


def 字形(o, ls):
    """→ 不合之由 或 ''（主案 §十一 3）"""
    if o['式'] in ('删', '照留') or ls is None:
        return ''
    字 = ''.join(l for _, l in 白文行(ls))
    改 = ''.join(段们(o['改']))
    出 = []
    for c in ('後', '后'):
        if c in 改 and c not in 字:
            出.append('改作有「%s」而该章白文无「%s」' % (c, c))
    return '；'.join(出)


def 核(书们, 表, 配=默配, 章限=None):
    """书们：书（今文）。章限：只核此诸章（--施 分批）。→ dict(红, 黄, A果, B今, B表, C1今, 亮, 盖, 批, 章)"""
    红, 黄 = list(表['红']), []
    限 = (lambda n: True) if 章限 is None else (lambda n: n in 章限)
    A果 = []
    for o in 表['A执']:
        if not 限(o['章']):
            continue
        ls = 书们.行(o['章'])
        状, 今, 注 = 核一(o, ls)
        形 = 字形(o, ls)
        r = dict(o, 状=状, 今行=今, 注=注, 形=形)
        A果.append(r)
        标 = '%s %d:%d［%s］' % (o['出'], o['章'], o['行'], o['式'])
        if 状 in ('无', '多见', '章不在', '删非整行'):
            红.append('%s %s：%s' % (标, 状, 注))
        elif 状 == '移':
            黄.append('%s 移 → %d:%d（%s；原文在该章白文恰一见，重锚）' % (标, o['章'], 今, 注))
        elif 状 == '已施':
            知 = 配['已知已施'].get((o['章'], o['行']))
            (黄 if 知 else 红).append('%s 已施%s' % (标, ('（%s）' % 知) if 知 else '——⛔不在已知已施之列，先查其由'))
        if 形:
            红.append('%s 字形：%s' % (标, 形))
        if o['式'] not in ('照留', '删') and 旧式 in o['改']:
            红.append('%s 改作含「%s」' % (标, 旧式))
    A今 = {}
    for r in A果:
        if r['状'] in ('合', '移', '已施') and r['今行']:
            A今.setdefault((r['章'], r['今行']), []).append(r)
    # B：今文自算
    白二十七, 亮 = {}, {}
    for n in sorted(书们.档):
        if not 限(n):
            continue
        ls = 书们.行(n)
        if ls is None:
            continue
        界 = 白界(ls)
        for k, l in enumerate(ls):
            c = l.count(旧式)
            if not c:
                continue
            if k < 界 and 白(l):
                白二十七[(n, k + 1)] = c
            else:
                亮[(n, k + 1)] = c
    B今 = {k: v for k, v in 白二十七.items() if k not in A今}
    B表 = {(o['章'], o['行']): o['处'] for o in 表['B主'] if (o['章'], o['行']) != 配['出B入A'] and 限(o['章'])}
    if 配['出B入A'] not in {(o['章'], o['行']) for o in 表['B主']} and 章限 is None:
        黄.append('主案 B 表无 %d:%d（出 B 入 A 之行）' % 配['出B入A'])
    for k in sorted(set(B今) | set(B表)):
        if B今.get(k) != B表.get(k):
            红.append('B %d:%d 今算 %s 处，表（减 %d:%d）%s 处' % (k[0], k[1], B今.get(k, 0), 配['出B入A'][0], 配['出B入A'][1], B表.get(k, 0)))
    # 盖：白文「二十七年」＝A 原文所含＋B
    盖A = 0
    for k, c in 白二十七.items():
        if k in A今:
            a = sum(r['原'].count(旧式) for r in A今[k] if r['状'] != '已施')
            盖A += a
            if a != c:
                红.append('盖 %d:%d 白文「%s」%d 处，A 之原文只含 %d 处——余者无表盖之' % (k[0], k[1], 旧式, c, a))
    盖 = dict(白处=sum(白二十七.values()), A=盖A, B=sum(B今.values()))
    # C1：亮点行算
    C1表 = {(o['章'], o['行']): o['处'] for o in 表['C1'] if 限(o['章'])}
    C1今 = {}
    for k, c in 亮.items():
        v = c - 配['C2送信'].get(k, 0)
        if v > 0:
            C1今[k] = v
    for k in sorted(set(C1今) | set(C1表)):
        if C1今.get(k) != C1表.get(k):
            红.append('C1 %d:%d 亮点今算 %s 处（减 C2 送信），表 %s 处' % (k[0], k[1], C1今.get(k, 0), C1表.get(k, 0)))
    # 章与批
    A章 = {r['章'] for r in A果 if r['式'] != '照留'}
    结构章 = {r['章'] for r in A果 if r['式'] in ('后添', '改＋后添', '删')}
    B章 = {k[0] for k in B表}
    C章 = {k[0] for k in C1表}
    五 = set(c for c in 配['五章'] if 限(c))
    if 结构章 != 五:
        红.append('增删段之章 %s ≠ 裁之五章 %s' % (sorted(结构章), sorted(五)))
    批 = {'三': sorted(五), '二': sorted(A章 - 五), '一': sorted((B章 | C章) - A章)}
    批['全'] = sorted(set(批['一']) | set(批['二']) | set(批['三']))
    数 = 配.get('定数')
    if 数 and 章限 is None:
        for 名, 实 in (('B行', len(B今)), ('B处', sum(B今.values())), ('B章', len({k[0] for k in B今})),
                       ('白处', 盖['白处']), ('C1行', len(C1今)), ('C1处', sum(C1今.values())),
                       ('章', len(批['全'])), ('批一', len(批['一'])), ('批二', len(批['二'])), ('A执', len(A果))):
            if 实 != 数[名]:
                红.append('定数 %s：今算 %d，裁 %d' % (名, 实, 数[名]))
        if 盖['A'] + 盖['B'] != 盖['白处']:
            红.append('盖：A %d＋B %d ≠ 白文 %d' % (盖['A'], 盖['B'], 盖['白处']))
    return dict(红=红, 黄=黄, A果=A果, A今=A今, B今=B今, B表=B表, C1今=C1今, C1表=C1表, 亮=亮, 盖=盖, 批=批)


# ───────── 施（内存） ─────────
def 施章(ls, 诸op, 星):
    """ls：旧行（无尾之空）；诸op：[dict(行, 式, 原, 改, 处)]，行＝今行；式 ∈ 换数、改、改＋后添、后添、删。
    → (新行们, 映（旧行 i → 新行 或 None，list 下标 i-1）, 红, 黄, 记)"""
    红, 黄 = [], []
    改 = {}
    添 = collections.defaultdict(list)
    删 = set()
    动 = set()
    随 = {}                                           # ★1021·W58 环2：旧行 → 其原文所落之添段（添[i] 之下标）——映随原文
    for o in sorted(诸op, key=lambda o: (o['行'], o['式'] == '删')):
        i, 式 = o['行'], o['式']
        标 = '%d［%s］' % (i, 式)
        if not 1 <= i <= len(ls):
            红.append('%s 行不在（章 %d 行）' % (标, len(ls))); continue
        if i in 删:
            红.append('%s 该行已删' % 标); continue
        l = 改.get(i, ls[i - 1])
        原 = o.get('原', '')
        if 式 == '换数':
            c = l.count(旧式)
            if c != o['处']:
                红.append('%s「%s」%d 处，表 %d 处' % (标, 旧式, c, o['处'])); continue
            l = l.replace(旧式, 新式)
        elif 式 == '改':
            if l.count(原) != 1:
                红.append('%s 原文在该行 %d 见' % (标, l.count(原))); continue
            l = l.replace(原, o['改'], 1)
        elif 式 == '改＋后添':
            段 = 段们(o['改'])
            if l.count(原) != 1 or not 段:
                红.append('%s 原文在该行 %d 见' % (标, l.count(原))); continue
            前, 後 = l.split(原, 1)
            if 前 or 後:
                黄.append('%s 改段而该行另有余字（前 %d、後 %d 字）——余字随首末段' % (标, len(前), len(後)))
            l = 前 + 段[0] + (後 if len(段) == 1 else '')
            余 = 段[1:]
            if 余:
                余[-1] += 後
            # ★1021·W58 环2（干跑所逮·317:133）：改作之後段即原文（「钱满……走到水边。〔另起段〕纸角翘起来。没有人去压它。」）
            #   ——原文实落於所添之段，旧行之映须随原文（133→137），⛔留在首段（行号随移之互证以 difflib 等块判之）
            k原 = next((k for k, s in enumerate(余) if s.strip() == 原.strip()), None)
            if k原 is not None and 段[0].strip() != 原.strip():
                随[i] = len(添[i]) + k原
            添[i] += 余
        elif 式 == '后添':
            if (原 == '＊' and l.strip() != '＊') or (原 != '＊' and l.count(原) != 1):
                红.append('%s 锚文不在该行或多见' % 标); continue
            添[i] += 段们(o['改'])
        elif 式 == '删':
            if (原 == '＊' and l.strip() != '＊') or (原 != '＊' and l.strip() != 原):
                红.append('%s「删」须整行（该行：%s）' % (标, l[:20])); continue
            if i in 改 or 添.get(i):
                红.append('%s 该行另有改／添' % 标); continue
            删.add(i)
            if i < len(ls) and not ls[i].strip():       # ★裁_1020 二·2：删段连其隔空行——其後之空行；无则其前
                删.add(i + 1)
            elif i >= 2 and not ls[i - 2].strip():
                删.add(i - 1)
            continue
        else:
            红.append('%s 式不认' % 标); continue
        改[i] = l
        动.add(i)
    新, 映 = [], []
    for i in range(1, len(ls) + 1):
        if i in 删:
            映.append(None)
            continue
        新.append(改.get(i, ls[i - 1]))
        映.append(len(新))
        for k, p in enumerate(添.get(i, [])):
            新 += (['', '＊', '', p] if 星 else ['', p])
            if 随.get(i) == k:
                映[-1] = len(新)                     # 旧行随原文落於此段
    for i, j in enumerate(映, 1):                    # 随原文者：新行与旧行同文即非「行内改」（余字随段者仍记动）
        if i in 随 and j is not None:
            if 新[j - 1] == ls[i - 1]:
                动.discard(i)
            else:
                动.add(i)
    def 连空(xs):
        return sum(1 for k in range(1, len(xs)) if not xs[k].strip() and not xs[k - 1].strip())
    def 连星(xs):
        ys = [x.strip() for x in xs if x.strip()]
        return sum(1 for k in range(1, len(ys)) if ys[k] == '＊' and ys[k - 1] == '＊')
    if 连空(新) > 连空(ls):
        红.append('施後连空 %d 处（施前 %d）——⛔留连空' % (连空(新), 连空(ls)))
    if 连星(新) > 连星(ls):
        红.append('施後「＊」相连 %d 处（施前 %d）' % (连星(新), 连星(ls)))
    记 = dict(旧长=len(ls), 新长=len(新), 删=sorted(删), 动=sorted(动), 添={str(i): len(v) * (4 if 星 else 2) for i, v in sorted(添.items()) if v})
    return 新, 映, 红, 黄, 记


def 诸op(果, 章, 亮=False, 配=默配):
    """核之果 → 一章之 op（A 之合／移；B；C1 若 --亮）。→ (ops, 待撰)"""
    ops, 待 = [], []
    for r in 果['A果']:
        if r['章'] != 章 or r['状'] not in ('合', '移'):
            continue
        ops.append(dict(行=r['今行'], 式=r['式'], 原=r['原'], 改=r['改'], 源='A'))
    for (c, i), n in sorted(果['B今'].items()):
        if c == 章:
            ops.append(dict(行=i, 式='换数', 处=n, 源='B'))
    if 亮:
        for (c, i), n in sorted(果['C1表'].items()):
            if c != 章:
                continue
            全 = 果['亮'].get((c, i), 0)
            if 全 == n:
                ops.append(dict(行=i, 式='换数', 处=n, 源='C1'))
            else:
                待.append('%d:%d（亮点「%s」%d 处，C1 %d、C2 送信 %d——留待撰）' % (c, i, 旧式, 全, n, 全 - n))
    return ops, 待


def 模拟(书们, 果, 章们, 亮=False, 配=默配):
    """→ (新文{章: 新行们}, 映{章: list}, 记{章: dict}, 红, 黄, 待)"""
    新文, 映, 记, 红, 黄, 待 = {}, {}, {}, [], [], []
    for 章 in sorted(章们):
        ls = 书们.行(章)
        if ls is None:
            红.append('第%d章 不在' % 章); continue
        ops, d = 诸op(果, 章, 亮, 配)
        待 += d
        新, m, r, y, k = 施章(ls, ops, 章 in 配['星章'])
        红 += ['第%d章 %s' % (章, x) for x in r]
        黄 += ['第%d章 %s' % (章, x) for x in y]
        差 = len(新) - len(ls)
        if 差 != 配['定差'].get(章, 0):
            红.append('第%d章 行差 %+d，裁 %+d' % (章, 差, 配['定差'].get(章, 0)))
        if 章 in 配['定删'] and k['删'] != 配['定删'][章]:
            红.append('第%d章 删行 %s，裁 %s' % (章, k['删'], 配['定删'][章]))
        残 = sum(l.count(旧式) for _, l in 白文行(新))
        if 残:
            红.append('第%d章 施後白文「%s」残 %d 处' % (章, 旧式, 残))
        新文[章], 映[章], 记[章] = 新, m, k
    return 新文, 映, 记, 红, 黄, 待


def 映区(m):
    """映 list → [[旧起, 旧止, 移]]（只列移者；删行另列）"""
    段, 前 = [], object()
    for i, j in enumerate(m, 1):
        δ = None if j is None else j - i
        if 段 and δ == 前 and 段[-1][1] == i - 1:
            段[-1][1] = i
        else:
            段.append([i, i, δ])
        前 = δ
    return [x for x in 段 if x[2]]


# ───────── 六式与 canon ─────────
# ★1020·W58：二稿账 D1 节（:82 末）「落後以正则验白文」之六式；范围 None＝全书
六式 = [
    ('「二十七年」作年义', None, r'二十七年'),
    ('「四十一」作年岁', None, r'(?:今年|时候|那年|他)[^。，；！？\n]{0,2}四十一(?![天日步个处行章号印回趟])|四十一岁'),
    ('313／317 东头下水', (313, 317), r'东头(?:第[一二三四两]趟)?(?:上来|下去|下水|扎下去|潜下去)|上来的(?:先)?是东头|(?:的手[，、]|写：)东头的手'
                                    r'|东头把绳(?:的那一)?头在(?:自己)?手腕上绕了一圈|东头把两根针擦干'),
    ('「他还来过四回」', None, r'他还来过四回'),
    ('211「级别」', (211,), r'级别'),
    ('268「这三年」', (268,), r'这三年'),
]
# ★护句三拍（裁_1020 二·8；二稿账:92 末）：⛔压——须各自成段
护三拍 = [
    ('「为什么是我们家」之挡', 103, lambda l: l.strip() == '“为什么是我们家。”'),
    ('「叫他先别跟你说」', 103, lambda l: '叫他先别跟你说。”' in l),
    ('「东头，我没有递」', 313, lambda l: l.strip() == '东头，我没有递。'),
]
canon之号 = ('F002', 'F154', 'F168')


def 六式之命(书们, 新文=None):
    """→ {式名: [(章, 行, 片)]}；新文{章: 行们} 覆书们之同章（模拟）"""
    出 = {名: [] for 名, _, _ in 六式}
    for n in sorted(书们.档):
        ls = 新文[n] if 新文 and n in 新文 else 书们.行(n)
        if ls is None:
            continue
        for 名, 域, p in 六式:
            if 域 and n not in 域:
                continue
            for i, l in 白文行(ls):
                for m in re.finditer(p, l):
                    出[名].append((n, i, l[max(0, m.start() - 8):m.end() + 8]))
    return 出


def canon禁(根, 书们, 新文=None, 事实=None):
    """照 小说检察官.priority_one 之界：forbid 只跑白文（「【本章亮点】」以前之全文），from_ch／except_ch／only_ch 照守。
    → [(号, 章, 片)]"""
    if 事实 is None:
        try:
            事实 = json.load(open(os.path.join(根, canon档), encoding='utf-8'))['facts']
        except Exception:
            return None
    fs = [f for f in 事实 if str(f.get('id', '')).startswith(canon之号)]
    出 = []
    for n in sorted(书们.档):
        ls = 新文[n] if 新文 and n in 新文 else 书们.行(n)
        if ls is None:
            continue
        t = '\n'.join(ls).split('【本章亮点】')[0]
        for f in fs:
            if n in set(f.get('except_ch', [])) or n < f.get('from_ch', 1) or (f.get('only_ch') and n not in set(f['only_ch'])):
                continue
            for p in f.get('forbid', []):
                for m in re.finditer(p, t):
                    出.append((f['id'], n, m.group(0)))
    return 出


默配['护'] = 护三拍


def 护之缺(书们, 新文=None, 配=默配):
    缺 = []
    for 名, 章, 判 in 配['护']:
        ls = 新文[章] if 新文 and 章 in 新文 else 书们.行(章)
        if ls is None or not any(判(l) for _, l in 白文行(ls)):
            缺.append('%s（第%d章）' % (名, 章))
    return 缺


# ───────── 窗 ─────────
def 窗(旧, 新, m, 诸op, 章, 宽=2):
    """→ (换之窗[str], 段之窗[str])：每处改前改後；●＝变（含新添、删去之行）"""
    结构 = {o['行'] for o in 诸op if o['式'] in ('后添', '改＋后添', '删')}
    点 = sorted({o['行'] for o in 诸op})
    删 = {i for i, j in enumerate(m, 1) if j is None}
    点 = sorted(set(点) | 删)
    像 = {}
    for i, j in enumerate(m, 1):
        if j is not None and 旧[i - 1] == 新[j - 1]:
            像[j] = i
    块 = []
    for i in 点:
        if 块 and i - 块[-1][1] <= 2 * 宽 + 1:
            块[-1][1] = i
        else:
            块.append([i, i])
    换, 段 = [], []
    for a, b in 块:
        lo, hi = max(1, a - 宽), min(len(旧), b + 宽)
        s = next((m[i - 1] for i in range(lo, hi + 1) if m[i - 1] is not None), None)
        e = next((m[i - 1] - 1 for i in range(hi + 1, len(旧) + 1) if m[i - 1] is not None), len(新))
        if s is None:
            s = next((m[i - 1] for i in range(hi + 1, len(旧) + 1) if m[i - 1] is not None), len(新) + 1)
        是段 = any(lo <= i <= hi for i in 结构 | 删)
        出 = ['', '### %d:%d—%d → %d:%d—%d' % (章, lo, hi, 章, s, e), '〔前〕']
        for i in range(lo, hi + 1):
            变 = m[i - 1] is None or 旧[i - 1] != 新[m[i - 1] - 1]
            if 旧[i - 1].strip() or 变 or 是段:
                出.append('%s %d｜%s%s' % ('●' if 变 else ' ', i, 旧[i - 1] if 旧[i - 1].strip() else '（空）', '　〔删〕' if m[i - 1] is None else ''))
        出.append('〔後〕')
        for j in range(s, e + 1):
            变 = j not in 像
            if 新[j - 1].strip() or 变 or 是段:
                出.append('%s %d｜%s' % ('●' if 变 else ' ', j, 新[j - 1] if 新[j - 1].strip() else '（空）'))
        (段 if 是段 else 换).extend(出)
    return 换, 段


# ───────── 行数守 ─────────
免守 = ('设定/_草/', '设定/改单备份/', 映档.replace(os.sep, '/'))


def 行数守(根, rev='HEAD', 配=默配, 取旧=None, 列变=None, 映=None):
    """正文、设定之档逐档行数比 rev；五章之变须合映。→ (红, 黄, 计)
    取旧(rels) → {rel: 文}；列变() → [(rel, 在)]——自测注入，默用 git。"""
    红, 黄 = [], []
    if 列变 is None:
        p = _git(根, 'diff', '--numstat', '--no-renames', rev, '--', '正文', '设定')
        变 = [l.split('\t', 2)[2] for l in p.stdout.decode('utf-8').split('\n') if l.count('\t') >= 2]
        新档 = [x for x in _git(根, 'ls-files', '--others', '--exclude-standard', '--', '正文', '设定').stdout.decode('utf-8').split('\n') if x]
    else:
        变, 新档 = 列变()
    取旧 = 取旧 or (lambda rels: 旧文们(根, rels, rev))
    旧 = 取旧(变)
    if 映 is None:
        try:
            映 = json.load(open(os.path.join(根, 映档), encoding='utf-8')).get('章', {})
        except Exception:
            映 = {}
    计 = dict(变档=len(变), 新档=len(新档), 五章合=0)
    for rel in 变:
        if rel.startswith(免守):
            continue
        p = os.path.join(根, rel)
        if not os.path.exists(p):
            红.append('%s 删档（rev 有、今无）' % rel); continue
        o = 旧.get(rel)
        if o is None:
            continue
        t = open(p, encoding='utf-8').read()
        a, b = 拆(o)[0], 拆(t)[0]
        n = 章号(rel) if rel.startswith('正文/') else None
        if n in 配['五章']:
            e = 映.get(str(n))
            if not e:
                红.append('%s 第%d章 有变而映档无其章' % (rel, n)); continue
            if len(a) != e['旧长'] or len(b) != e['新长']:
                红.append('%s 第%d章 行数 %d→%d，映 %d→%d' % (rel, n, len(a), len(b), e['旧长'], e['新长'])); continue
            动 = set(e.get('动', []))
            界 = 白界(a)
            坏 = []
            for i in range(1, len(a) + 1):
                j = e['映'].get(str(i))
                if j is None or a[i - 1] == b[j - 1] or i in 动:
                    continue
                坏.append((i, j))
            白坏 = [x for x in 坏 if x[0] <= 界]
            if 白坏:
                红.append('%s 第%d章 内容锚不合 %d 行（白文；静漂或误改）：%s' % (rel, n, len(白坏), '、'.join('%d→%d' % x for x in 白坏[:8])))
            elif 坏:
                黄.append('%s 第%d章 亮点层 %d 行与旧异（C2 撰之改？）：%s' % (rel, n, len(坏), '、'.join('%d→%d' % x for x in 坏[:8])))
            if not 白坏:
                计['五章合'] += 1
        elif len(a) != len(b):
            红.append('%s 行数 %d→%d（⛔非五章之档变行数）' % (rel, len(a), len(b)))
    for rel in 新档:
        if not rel.startswith(免守):
            黄.append('%s 新档（rev 无）' % rel)
    return 红, 黄, 计


# ───────── 基线 ─────────
def 基线(根, 书们, 章们):
    return {str(n): dict(档=书们.档[n], blob=blob(书们.文(n).encode('utf-8'))) for n in sorted(章们) if 书们.档.get(n)}


def 基线比(根, 书们, 章们, 路=None):
    """→ (红, 黄)"""
    for p in [路 or os.path.join(根, 基线档)]:          # ⛔退而取本器之仓之基线（副本与主树之基线各立；要比主树之基线，--基线 明给其路）
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8')).get('章', {})
            今 = 基线(根, 书们, 章们)
            异 = [n for n in sorted(章们) if str(n) in d and 今.get(str(n), {}).get('blob') != d[str(n)]['blob']]
            缺 = [n for n in sorted(章们) if str(n) not in d]
            红 = ['基线（%s）：第 %s 章之 blob 与基线异——立单以後正文动过，⛔施' % (p, '、'.join(map(str, 异[:12])))] if 异 else []
            return 红 + (['基线无第 %s 章' % '、'.join(map(str, 缺[:12]))] if 缺 else []), []
    return [], ['无基线（%s）——先 --核 --写基线，或 --基线 明给其路' % (路 or 基线档)]


# ───────── 拒 ─────────
def 拒根(根, 落=False):
    """→ 拒之由 或 ''"""
    if not 根:
        return '⛔无 --根 即拒：--施 只在 --根 所指之副本施（git clone --local 主树 副本）'
    if not os.path.isdir(os.path.join(根, '正文')) or not os.path.isdir(os.path.join(根, '设定')):
        return '⛔--根 %s 不是本书之仓（无 正文/、设定/）' % 根
    if os.path.realpath(根) == os.path.realpath(主树) and not 落:
        return '⛔--根 为主树（%s）：W58 只干跑於副本；落归 W59，另加 --落' % 主树
    return ''


# ───────── 改单（★1021·W58 环2：4b 亮点撰、4c 设定层义判、4d 待判单与器物册——模型之改以单记之，器照单施） ─────────
# 单：JSON 列 [{"档": 相对路径, "行": 施後之行号, "原": 该行里之原片（恰一见）, "新": 新片, "据": "4b|4c|4d", "由": "…"}]
# 施：逐条於「档」之「行」找「原」→「新」；该行恰一见即施（合），该行无则容 ±3 之移而窗内恰一见（移·黄）；
#   「原已不在而新在」＝已施（二跑零改；新含原者——史料行照留加行内注——以「新」所盖之原⛔算）；余即红、全单一字不写。
#   ⛔插行、⛔删行：原、新俱⛔含换行，施後逐档行数比施前；施毕在内存再判一回（二跑之模拟），条条须已施，否则红。
改单据 = ('4b', '4c', '4d')
改单容 = 3


def _见(l, s):
    """s 在 l 之诸起位（含叠见）"""
    出, i = [], l.find(s)
    while i >= 0:
        出.append(i)
        i = l.find(s, i + 1)
    return 出


def _原见(l, 原, 新):
    """该行里「原」之起位，减去落在「新」之内者（新含原：史料行加注之後，原在新中⛔再算一见）"""
    盖 = [(q, q + len(新)) for q in _见(l, 新)] if 原 in 新 else []
    return [p for p in _见(l, 原) if not any(a <= p and p + len(原) <= b for a, b in 盖)]


def 读单(条们):
    """→ (条们, 红)：逐条核其式（键、类、据、换行、重条、出根）"""
    红 = []
    if not isinstance(条们, list):
        return [], ['单须为 JSON 列（[{档, 行, 原, 新, 据, 由}, …]）']
    见 = set()
    for k, o in enumerate(条们, 1):
        标 = '#%d' % k
        if not isinstance(o, dict):
            红.append('%s 非 {…}' % 标); continue
        缺 = [x for x in ('档', '行', '原', '新', '据', '由') if x not in o]
        if 缺:
            红.append('%s 缺键 %s' % (标, '、'.join(缺))); continue
        档, 行, 原, 新 = o['档'], o['行'], o['原'], o['新']
        if not isinstance(档, str) or not 档 or os.path.isabs(档) or '\\' in 档 or \
                any(x in ('..', '.git') for x in 档.split('/')) or 档 != os.path.normpath(档).replace(os.sep, '/'):
            红.append('%s 档「%s」须为根下之相对路径（⛔绝对、⛔..、⛔.git）' % (标, 档)); continue
        if not isinstance(行, int) or isinstance(行, bool) or 行 < 1:
            红.append('%s %s 行「%s」须为正整数' % (标, 档, 行)); continue
        标 = '#%d %s:%d' % (k, 档, 行)
        if not isinstance(原, str) or not isinstance(新, str) or not 原:
            红.append('%s 原、新须为字串，原⛔空' % 标); continue
        if any(c in 原 + 新 for c in '\n\r\u2028\u2029'):
            红.append('%s 原或新含换行——⛔插行、⛔删行（行数守）' % 标); continue
        if not 新:
            红.append('%s 新为空——删片须连其邻字作原、新（否则二跑判不出已施）' % 标); continue
        if 新 == 原:
            红.append('%s 新＝原（空改）' % 标); continue
        if o['据'] not in 改单据:
            红.append('%s 据「%s」不认（只认 %s）' % (标, o['据'], '、'.join(改单据))); continue
        if not isinstance(o['由'], str) or not o['由'].strip():
            红.append('%s 由⛔空' % 标); continue
        键 = (档, 行, 原)
        if 键 in 见:
            红.append('%s 重条（同档、同行、同原）' % 标); continue
        见.add(键)
    return 条们, 红


def 判条(ls, o, 容=改单容):
    """→ (状, 行, 位, 注)。状 ∈ 合、移、已施、多见、两可、不见。行：施於／已施於之行号；位：原在该行之起位"""
    n, 原, 新 = o['行'], o['原'], o['新']
    if 1 <= n <= len(ls):
        l = ls[n - 1]
        u = _原见(l, 原, 新)
        if len(u) == 1:
            return ('合', n, u[0], '')
        if len(u) > 1:
            return ('多见', n, None, '原在该行 %d 见' % len(u))
        if 新 in l:
            return ('已施', n, None, '')
    窗 = [i for i in range(max(1, n - 容), min(len(ls), n + 容) + 1) if i != n]
    原们 = [(i, p) for i in 窗 for p in _原见(ls[i - 1], 原, 新)]
    新们 = [i for i in 窗 if 新 in ls[i - 1]]
    if len(原们) == 1 and not 新们:
        i, p = 原们[0]
        return ('移', i, p, '%+d' % (i - n))
    if len(原们) == 1:
        return ('两可', None, None, '该行无原；±%d 内原一见（%d 行）而新亦在（%s 行）——已施与否⛔猜' % (容, 原们[0][0], '、'.join(map(str, 新们))))
    if len(原们) > 1:
        return ('多见', None, None, '该行无原；±%d 内原 %d 见（%s 行）——⛔猜' % (容, len(原们), '、'.join(str(i) for i, _ in 原们[:6])))
    if 新们:
        return ('已施', 新们[0], None, '於 %s 行' % '、'.join(map(str, 新们)))
    return ('不见', None, None, '该行与 ±%d 内俱无原、亦无新' % 容)


def 施改单(根, 条们, 容=改单容):
    """内存施之、内存二跑验之。→ (红, 黄, 计, 写们[(绝对路, 新文)])——一字不写，写由跑改单"""
    红, 黄 = [], []
    根r = os.path.realpath(根)
    文, 旧, 尾, 败 = {}, {}, {}, set()
    for o in 条们:
        档 = o['档']
        if 档 in 文 or 档 in 败:
            continue
        p = os.path.realpath(os.path.join(根r, 档))
        if not (p + os.sep).startswith(根r + os.sep) or not os.path.isfile(p):
            红.append('%s 不在根下（或非档）' % 档); 败.add(档); continue
        try:
            t = open(p, encoding='utf-8', newline='').read()
        except Exception as e:
            红.append('%s 读不出（%s）' % (档, repr(e)[:60])); 败.add(档); continue
        旧[档] = t
        文[档], 尾[档] = 拆(t)
        文[档] = list(文[档])
    计 = collections.Counter()
    施们 = []
    for k, o in enumerate(条们, 1):
        if o['档'] in 败:
            continue
        ls = 文[o['档']]
        状, i, p, 注 = 判条(ls, o, 容)
        标 = '#%d %s:%d［%s］' % (k, o['档'], o['行'], o['据'])
        计[状] += 1
        if 状 in ('合', '移'):
            l = ls[i - 1]
            ls[i - 1] = l[:p] + o['新'] + l[p + len(o['原']):]
            施们.append((k, o, i))
            if 状 == '移':
                黄.append('%s 移 → %d 行（%s；±%d 内恰一见）' % (标, i, 注, 容))
            n = 章号(o['档']) if o['档'].startswith('正文/') else None
            if n and i <= 白界(ls) and 白(ls[i - 1]):
                黄.append('%s 改在第%d章白文（白文归 D1施 之 A／B；改单只该动亮点层、设定——查其由）' % (标, n))
        elif 状 != '已施':
            红.append('%s %s：%s' % (标, 状, 注))
    for 档, ls in 文.items():                          # 行数守：⛔插行、⛔删行（合而再拆——行内夹换行者，list 之长不变而档之行数变）
        前n, 后n = len(拆(旧[档])[0]), len(拆(合(ls, 尾[档]))[0])
        if 前n != 后n:
            红.append('%s 行数 %d→%d（⛔变）' % (档, 前n, 后n))
    for k, o in enumerate(条们, 1):                    # 二跑之模拟：施後条条须判「已施」，否则二跑必再改（叠改、互吞）
        if o['档'] in 文:
            状 = 判条(文[o['档']], o, 容)[0]
            if 状 != '已施' and not 红:
                红.append('#%d %s:%d 施後再判作「%s」——⛔二跑零改不成（与同单他条相叠？）' % (k, o['档'], o['行'], 状))
    写们 = [(os.path.join(根r, 档), 合(ls, 尾[档])) for 档, ls in sorted(文.items()) if 合(ls, 尾[档]) != 旧[档]]
    计['档'] = len(写们)
    计['施'] = len(施们)
    return 红, 黄, 计, 写们


def 跑改单(根, a, 配=默配, 主=主树):
    """--改单 <单.json> --根 <根> [--验] [--落]"""
    单 = _参(a, '--改单')
    if not 单 or 单.startswith('--'):
        单 = next((x for x in a if x.endswith('.json') and x != _参(a, '--根')), None)
    验 = '--验' in a
    if not 根:
        print('⛔--改单 无 --根 即拒：改单只在 --根 所指之副本施（主树另加 --落）'); return 2
    if not os.path.isdir(os.path.join(根, '正文')) or not os.path.isdir(os.path.join(根, '设定')):
        print('⛔--根 %s 不是本书之仓（无 正文/、设定/）' % 根); return 2
    if os.path.realpath(根) == os.path.realpath(主) and not 验 and '--落' not in a:
        print('⛔--根 为主树（%s）：改单之施只在副本；落主树另加 --落（--验 只核不写，许）' % 主); return 2
    if not 单 or not os.path.isfile(单):
        print('⛔--改单 须给单之 JSON 档（%s 不在）' % 单); return 2
    try:
        条们 = json.load(open(单, encoding='utf-8'))
    except Exception as e:
        print('⛔单 %s 读不出（%s）' % (单, repr(e)[:80])); return 1
    print('════ D1施 --改单%s · %s · 单 %s ════' % (' --验' if 验 else '', _头(根), 单))
    条们, 红 = 读单(条们)
    if 红:
        _印(红, [], 200)
        print('D1施·改单：单之式有红 %d，⛔施（一字未写）' % len(红)); return 1
    红, 黄, 计, 写们 = 施改单(根, 条们)
    _印(红, 黄, 200)
    据计 = collections.Counter(o['据'] for o in 条们)
    摘 = '条 %d（%s）：合 %d、移 %d、已施 %d' % (len(条们), '、'.join('%s %d' % kv for kv in sorted(据计.items())),
                                         计['合'], 计['移'], 计['已施'])
    if 红:
        print('D1施·改单：%s｜有红 %d，⛔施（一字未写）' % (摘, len(红))); return 1
    if 验:
        print('D1施·改单 --验：%s｜将改 %d 条、%d 档；只核不写 ✓' % (摘, 计['施'], 计['档'])); return 0
    for p, t in 写们:
        open(p + '.d1tmp', 'w', encoding='utf-8', newline='').write(t)
    for p, t in 写们:
        os.replace(p + '.d1tmp', p)
    print('D1施·改单：%s｜✓ 改 %d 条、写 %d 档（行数俱不变）' % (摘, 计['施'], 计['档']))
    return 0


# ───────── 入口 ─────────
def _参(a, k, 默=None):
    return a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else 默


def _印(红, 黄, 限=40):
    for x in 黄[:限]:
        print('  ⚠ ' + x)
    if len(黄) > 限:
        print('  ⚠ …余 %d 条' % (len(黄) - 限))
    for x in 红[:限]:
        print('  ⛔ ' + x)
    if len(红) > 限:
        print('  ⛔ …余 %d 条' % (len(红) - 限))


def _头(根):
    h = _git(根, 'rev-parse', '--short=8', 'HEAD').stdout.decode().strip() if os.path.isdir(os.path.join(根, '.git')) else '—'
    return '根 %s（HEAD %s）' % (根, h)


def 跑核(根, a, 配=默配):
    print('════ D1施 --核 · %s ════' % _头(根))
    表 = 读表根(根, 配)
    书们 = 书(根).预取()
    果 = 核(书们, 表, 配)
    计 = collections.Counter(r['状'] for r in 果['A果'])
    已 = ['%d:%d·%s' % (r['章'], r['今行'], 配['已知已施'].get((r['章'], r['行']), '?')) for r in 果['A果'] if r['状'] == '已施']
    覆 = sum(1 for o in 表['丙'] if o.get('类') == '覆')
    print('  A：主案 %d 行（裁丙覆 %d、增 %d）→ 执行 %d 行：%s%s' % (
        len(表['A主']), 覆, len(表['丙']) - 覆, len(表['A执']),
        '、'.join('%s %d' % (k, 计.get(k, 0)) for k in ('合', '移', '无', '已施', '照留')), ('（已施 %s）' % '、'.join(已)) if 已 else ''))
    for r in 果['A果']:
        if r['状'] not in ('合', '照留'):
            print('     %s %d:%d［%s］%s%s' % (r['状'], r['章'], r['行'], r['式'], ('→%d ' % r['今行']) if r['今行'] and r['今行'] != r['行'] else '', r['注']))
    形 = [r for r in 果['A果'] if r['形']]
    print('  字形：%d 不合%s' % (len(形), ' ✓' if not 形 else ''))
    B今, B表 = 果['B今'], 果['B表']
    print('  B：今算 %d 行 %d 处 %d 章（白文含「%s」之行减 A 之今行）；主案 B %d 行 %d 处减 %d:%d → %d 行 %d 处 %s' % (
        len(B今), sum(B今.values()), len({k[0] for k in B今}), 旧式, len(表['B主']), sum(o['处'] for o in 表['B主']),
        配['出B入A'][0], 配['出B入A'][1], len(B表), sum(B表.values()), '逐行逐处同 ✓' if B今 == B表 else '⛔不同'))
    C1今, C1表 = 果['C1今'], 果['C1表']
    print('  C1：亮点与批注层「%s」%d 行 %d 处，减 C2 送信 %d 处 → %d 行 %d 处；主案 C1 %d 行 %d 处 %s' % (
        旧式, len(果['亮']), sum(果['亮'].values()), sum(配['C2送信'].values()), len(C1今), sum(C1今.values()),
        len(C1表), sum(C1表.values()), '逐行逐处同 ✓' if C1今 == C1表 else '⛔不同'))
    盖 = 果['盖']
    print('  盖：白文「%s」%d 处＝A 原文所含 %d＋B %d %s' % (旧式, 盖['白处'], 盖['A'], 盖['B'], '✓' if 盖['A'] + 盖['B'] == 盖['白处'] else '⛔'))
    批 = 果['批']
    print('  章：%d（批一 B 独 %d、批二 A 行数不变 %d、批三 五章 %s）' % (len(批['全']), len(批['一']), len(批['二']), '、'.join(map(str, 批['三']))))
    新文, 映, 记, 红s, 黄s, 待 = 模拟(书们, 果, 批['全'], '--亮' in a, 配)
    差 = {n: 记[n]['新长'] - 记[n]['旧长'] for n in 记 if 记[n]['新长'] != 记[n]['旧长'] or n in 配['五章']}
    余 = sum(1 for n in 记 if n not in 配['五章'] and 记[n]['新长'] == 记[n]['旧长'])
    删 = ['%d:%s' % (n, '、'.join(str(x) for x in 记[n]['删'])) for n in sorted(记) if 记[n]['删']]
    print('  模拟（内存）：五章行差 %s；余 %d 章行差 0；删行 %s' % ('、'.join('%d %+d' % kv for kv in sorted(差.items())), 余, '；'.join(删) or '无'))
    命 = 六式之命(书们, 新文)
    前 = 六式之命(书们)
    print('  模拟六式（施前→施後）：%s' % '；'.join('%s %d→%d' % (名, len(前[名]), len(命[名])) for 名, _, _ in 六式))
    cn = canon禁(根, 书们, 新文)
    cn0 = canon禁(根, 书们)
    print('  模拟 canon 禁式（%s）：施前 %s、施後 %s' % ('、'.join(canon之号), '?' if cn0 is None else len(cn0), '?' if cn is None else len(cn)))
    缺 = 护之缺(书们, 新文, 配)
    print('  模拟护三拍：%s' % ('俱成段 ✓' if not 缺 else '⛔缺 ' + '、'.join(缺)))
    if 待:
        print('  待撰（--亮）：' + '；'.join(待))
    红 = 果['红'] + 红s + ['模拟施後 %s 残 %d' % (名, len(v)) for 名, v in 命.items() if v] + (['模拟施後护三拍缺 ' + '、'.join(缺)] if 缺 else [])
    黄 = 果['黄'] + 黄s
    br, by = 基线比(根, 书们, 批['全'])
    if '--写基线' in a:
        p = os.path.join(根, 基线档)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        d = dict(_说明='D1施 --核 --写基线（★1020·W58 keep-lines 之嫁接）：95 章（白文＋亮点）之 blob 哈希（git hash-object 同算）；--施 前逐章比，异即⛔施',
                 HEAD=_git(根, 'rev-parse', 'HEAD').stdout.decode().strip(), 时=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                 章=基线(根, 书们, 批['全']))
        tmp = p + '.tmp%d' % os.getpid()
        open(tmp, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
        os.replace(tmp, p)
        print('  基线：%d 章 blob → %s' % (len(d['章']), os.path.relpath(p, 根)))
    else:
        print('  基线：%s' % ('与 %s 同 ✓' % 基线档 if not br and not by else (by[0] if by else br[0])))
        红 += br
    _印(红, 黄)
    print('D1施·核：%s（红 %d、黄 %d）' % ('✓ 核过' if not 红 else '⛔有红', len(红), len(黄)))
    return 1 if 红 else 0


def 跑窗(根, a, 配=默配):
    出目 = _参(a, '--出') or (默出 if os.path.isdir(os.path.dirname(默出)) else os.path.join(tempfile.gettempdir(), 'D1施_窗'))
    # ★1020·W58 驳席：旧式只在「未给 --出」时查，而默出本不在主树——那一查是死的；令明「⛔写主树」，--出 指进主树一样拒（W59 另加 --落）
    if (os.path.realpath(出目) + os.sep).startswith(os.path.realpath(主树) + os.sep) and '--落' not in a:
        print('⛔--窗 ⛔写主树（--出 %s 在主树 %s 之内）：W58 之窗出到 scratchpad；W59 另加 --落' % (出目, 主树)); return 2
    表 = 读表根(根, 配)
    书们 = 书(根).预取()
    果 = 核(书们, 表, 配)
    批 = 批名.get(_参(a, '--批', '全'), '全')
    章们 = 果['批'][批]
    新文, 映, 记, 红, 黄, 待 = 模拟(书们, 果, 章们, '--亮' in a, 配)
    换, 段 = ['# D1施之窗·行内之改（批%s；改前／改後；●＝变）' % 批, '', '> %s；零 token 所出（工具/D1施.py --窗）。' % _头(根)], \
             ['# D1施之窗·增删段（批%s；改前／改後；●＝变，含新添之空行、「＊」与删去之行）' % 批, '', '> %s；五章之行号漂——〔後〕之号係施後之号。' % _头(根)]
    for 章 in sorted(新文):
        ops, _ = 诸op(果, 章, '--亮' in a, 配)
        h, s = 窗(书们.行(章), 新文[章], 映[章], ops, 章)
        if h:
            换 += ['', '## 第%d章（%s）' % (章, os.path.basename(书们.档[章]))] + h
        if s:
            段 += ['', '## 第%d章（%s；%d→%d 行）' % (章, os.path.basename(书们.档[章]), 记[章]['旧长'], 记[章]['新长'])] + s
    os.makedirs(出目, exist_ok=True)
    后 = '' if 批 == '全' else '_批' + 批
    p1, p2 = os.path.join(出目, '窗_换%s.md' % 后), os.path.join(出目, '窗_段%s.md' % 后)
    open(p1, 'w', encoding='utf-8').write('\n'.join(换) + '\n')
    open(p2, 'w', encoding='utf-8').write('\n'.join(段) + '\n')
    _印(果['红'] + 红, 果['黄'] + 黄)
    print('D1施·窗：%d 章 → %s（%d 行）、%s（%d 行）' % (len(新文), p1, len(换), p2, len(段)))
    return 1 if 果['红'] or 红 else 0


def 跑施(根, a, 配=默配):
    由 = 拒根(根, '--落' in a)
    if 由:
        print(由); return 2
    根 = os.path.realpath(根)
    批 = 批名.get(_参(a, '--批', '全'))
    if not 批:
        print('⛔--批 只认 一、二、三、全'); return 2
    print('════ D1施 --施 · 批%s · %s ════' % (批, _头(根)))
    表 = 读表根(根, 配)
    书们 = 书(根).预取()
    全果 = 核(书们, 表, 配)                        # 批之分须全书之果（批一＝B 独之章）
    章们 = 全果['批'][批]
    果 = 核(书们, 表, 配, 章限=set(章们))          # ★分批：只核本批之章（前批已施之章⛔再判）
    亮 = '--亮' in a
    新文, 映, 记, 红s, 黄s, 待 = 模拟(书们, 果, 章们, 亮, 配)
    br, by = 基线比(根, 书们, 章们, _参(a, '--基线'))
    if '--落' in a and by:                          # ★1020·W58 驳席：落（W59）⛔无基线——keep-lines「施前逐章比 blob」⛔静悄悄跳过
        br, by = br + ['--落 而' + x for x in by], []
    红 = 果['红'] + 红s + br
    黄 = 果['黄'] + 黄s + by
    if 批 == '全':
        命 = 六式之命(书们, 新文)
        红 += ['施後 %s 残 %d：%s' % (名, len(v), '；'.join('%d:%d「%s」' % x for x in v[:4])) for 名, v in 命.items() if v]
        缺 = 护之缺(书们, 新文, 配)
        红 += ['施後护三拍缺 ' + '、'.join(缺)] if 缺 else []
    _印(红, 黄)
    if 待:
        print('  待撰：' + '；'.join(待))
    if 红:
        print('D1施·施：有红 %d，⛔施（一字未写）' % len(红)); return 1
    # ★一次写盘：诸章新文俱已在内存且俱过验，始写；每档 tmp＋os.replace
    写 = []
    for 章 in sorted(新文):
        旧t = 书们.文(章)
        _, 有尾 = 拆(旧t)
        t = 合(新文[章], 有尾)
        if t != 旧t:
            写.append((os.path.join(根, 书们.档[章]), t, 章))
    for p, t, _ in 写:
        tmp = p + '.d1tmp'
        open(tmp, 'w', encoding='utf-8').write(t)
    for p, t, _ in 写:
        os.replace(p + '.d1tmp', p)
    p = os.path.join(根, 映档)
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        d = {}
    d['_说明'] = ('D1 老头之年五审之换齐（工具/D1施.py --施）之行号映：章 → 旧行（施前今文之号；--核 无「移」时即 0929 表之号）→ 新行；删行映 null。'
                '「动」＝行内改之旧行，「添」＝其後所添之行数，「区」＝[旧起, 旧止, 移]。本档在史档之列（⛔诸扫认作在役之引）。')
    d.setdefault('章', {})
    for 章 in sorted(新文):
        if 记[章]['新长'] != 记[章]['旧长'] or 记[章]['删'] or 记[章]['添']:
            d['章'][str(章)] = dict(档=书们.档[章], 旧长=记[章]['旧长'], 新长=记[章]['新长'], 删=记[章]['删'], 动=记[章]['动'], 添=记[章]['添'],
                                  区=映区(映[章]), 映={str(i): j for i, j in enumerate(映[章], 1)})
    d.setdefault('施', []).append(dict(批=批, 亮=亮, 时=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 章=sorted(新文),
                                     HEAD=_git(根, 'rev-parse', '--short=8', 'HEAD').stdout.decode().strip()))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p + '.tmp', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')
    os.replace(p + '.tmp', p)
    动 = sum(len(记[n]['动']) for n in 记)
    print('  施 %d 章（动行 %d；A %d 条、B %d 行 %d 处%s）；行差 %s' % (
        len(写), 动, sum(1 for r in 果['A果'] if r['状'] in ('合', '移') and r['式'] != '照留'), len(果['B今']), sum(果['B今'].values()),
        ('、C1 %d 行' % sum(1 for k in 果['C1表'] if 果['亮'].get(k) == 果['C1表'][k])) if 亮 else '',
        '、'.join('%d %+d' % (n, 记[n]['新长'] - 记[n]['旧长']) for n in sorted(记) if n in 配['五章']) or '无'))
    print('  映 → %s（%d 章）' % (映档, len(d['章'])))
    if '--同步' in a:
        sys.path.insert(0, os.path.join(根, '工具'))
        import importlib.util as _u
        sp = _u.spec_from_file_location('_还账_d1', os.path.join(根, '工具', '还账.py'))
        还账 = _u.module_from_spec(sp)
        sp.loader.exec_module(还账)
        还账.施後同步([c for _, _, c in 写], root=根, 单名='D1施·批' + 批)
    print('D1施·施：✓ 批%s 一次写盘 %d 档' % (批, len(写)))
    return 0


def 跑行数守(根, a, 配=默配):
    rev = _参(a, '--旧', 'HEAD')
    print('════ D1施 --行数守 · %s · 比 %s ════' % (_头(根), rev))
    红, 黄, 计 = 行数守(根, rev, 配)
    _印(红, 黄)
    print('D1施·行数守：变档 %d、新档 %d、五章合映 %d｜%s（红 %d）' % (计['变档'], 计['新档'], 计['五章合'], '✓' if not 红 else '⛔', len(红)))
    return 1 if 红 else 0


def 跑终验(根, a, 配=默配):
    rev = _参(a, '--旧', 'HEAD')
    print('════ D1施 --终验 · %s ════' % _头(根))
    书们 = 书(根).预取()
    命 = 六式之命(书们)
    红 = []
    for 名, _, _ in 六式:
        v = 命[名]
        print('  %s %s：%d%s' % ('✓' if not v else '⛔', 名, len(v), ('　' + '；'.join('%d:%d「%s」' % x for x in v[:6])) if v else ''))
        if v:
            红.append('%s 残 %d' % (名, len(v)))
    cn = canon禁(根, 书们)
    if cn is None:
        红.append('canon 事实库读不出')
    else:
        旧书 = 书(根, rev) if os.path.isdir(os.path.join(根, '.git')) else None
        cn旧 = collections.Counter((x[0], x[1], x[2]) for x in (canon禁(根, 旧书.预取()) or [])) if 旧书 else collections.Counter()
        新 = [x for x in cn if not cn旧[(x[0], x[1], x[2])]]
        旧 = [x for x in cn if cn旧[(x[0], x[1], x[2])]]
        print('  %s canon 禁式（%s）：新命中 %d、旧有 %d%s' % ('✓' if not 新 else '⛔', '、'.join(canon之号), len(新), len(旧),
                                                     ('　' + '；'.join('%s 第%d章「%s」' % x for x in 新[:6])) if 新 else ''))
        if 新:
            红.append('canon 禁式新命中 %d' % len(新))
    缺 = 护之缺(书们, 配=配)
    print('  %s 护三拍：%s' % ('✓' if not 缺 else '⛔', '俱成段' if not 缺 else '缺 ' + '、'.join(缺)))
    if 缺:
        红.append('护三拍缺 %d' % len(缺))
    print('D1施·终验：%s' % ('✓ 六式残 0、canon 禁式新命中 0、护三拍俱在' if not 红 else '⛔ ' + '；'.join(红)))
    return 1 if 红 else 0


# ───────── 自测 ─────────
def 自测():
    import io, contextlib
    ok = 共 = 0
    def 静(f, *x):                                   # 内层之印收起（自测只印其格）
        with contextlib.redirect_stdout(io.StringIO()):
            return f(*x)
    def T(名, 真, 注=''):
        nonlocal ok, 共
        共 += 1
        ok += bool(真)
        print('  %s %s%s' % ('✓' if 真 else '✗', 名, '' if 真 else ('　' + str(注)[:200])))
    配 = dict(默配, 五章=(103, 313), 星章=(313,), 定差={103: 0, 313: 4}, 定删={103: [5, 6]}, 定数=None,
             已知已施={(211, 9): 'x'}, 出B入A=(187, 2), C2送信={(120, 9): 1}, 护=[护三拍[2]])
    def 主案文(A行, B行, C1):
        return '\n'.join(['# 主案', '### A　特改', '| 章:行 | 式 | 原文 | 改作 | 由 |', '|---|---|---|---|---|'] + A行 +
                         ['', '### B　机械换数', '| 章 | 行 |', '|---|---|'] + B行 + ['', '### C　亮点', '**C1「二十七年」→「四十八年」（测）**：' + C1, '', '### D　照留'])
    def 裁文(丙行):
        return '\n'.join(['# 裁', '## 丙、裁定之正', '| 章:行 | 式 | 类 | 原文 | 改作 | 由 |', '|---|---|---|---|---|---|'] + 丙行 + ['', '## 丁、诸刺'])
    书文 = {
        103: '\n'.join(['第一百零三章　测', '', '他二十七年前来过。', '', '我一直以为他有七八十。', '', '“我背包袱。”', '', '后来他走了。', '',
                        '【本章亮点】', '亮：二十七年前。']) + '\n',
        313: '\n'.join(['第三百一十三章　测', '', '针我也给了他们。一人一根。', '', '＊', '', '东头第二趟上来。', '']) + '\n',
        120: '\n'.join(['第一百二十章　测', '', '那是二十七年前，二十七年前的事。', '', '【本章亮点】', '', '', '', '亮：二十七年前；二十七年后。']) + '\n',
        187: '\n'.join(['第一百八十七章　测', '而这二十七年里只有一个。', '', '二十七年。']) + '\n',
        211: '\n'.join(['第二百一十一章　测'] + [''] * 7 + ['守了七天。缠完了。']) + '\n',
    }
    A行 = ['| 103:3 | 改 | 他二十七年前来过。 | 他四十八年前来过。 | 数 |',
           '| 103:5 | 删 | 我一直以为他有七八十。 | （整行删） | 由 |',
           '| 103:7 | 改 | “我背包袱。” | “我背包袱，主案。” | 由 |',
           '| 211:9 | 改 | 守了三个月。 | 守了七天。缠完了。 | 由 |',
           '| 313:3 | 改＋后添 | 针我也给了他们。一人一根。 | 针我也给了。〔另起段〕〔另起段〕东头，我没有递。 | 由 |']
    丙行 = ['| 103:7 | 改 | 覆 | “我背包袱。” | “我背包袱，裁之。” | 由 |',
           '| 187:2 | 改 | 新 | 而这二十七年里只有一个。 | 而这四十八年里数得出两个。 | 由 |',
           '| 313:7 | 改 | 新 | 东头第二趟上来。 | 钱满第二趟上来。 | 由 |']
    B行 = ['| 120 | 3×2 |', '| 187 | 2、4 |']
    C1 = '103:12；120:9'
    表 = 读表(主案文(A行, B行, C1), 裁文(丙行), 配)
    # ① 覆增
    行7 = [o for o in 表['A执'] if (o['章'], o['行']) == (103, 7)]
    T('①表之覆增：主案 5 行、裁覆 1 增 2 → 执行 7 行，覆者取裁文', len(表['A执']) == 7 and len(行7) == 1 and '裁之' in 行7[0]['改'] and not 表['红'], 表['红'])
    书们 = 书(None, 文们=书文)
    果 = 核(书们, 表, 配)
    状 = {(r['章'], r['行']): r['状'] for r in 果['A果']}
    # ② 合
    T('②原文为该行之子串、恰一见 → 合', 状[(103, 3)] == '合' and 状[(313, 3)] == '合', 状)
    # ③ 已施
    T('③改作已在该行 → 已施（在已知之列则黄）', 状[(211, 9)] == '已施' and not any('211:9' in x for x in 果['红']), 果['红'])
    # ④ 多见
    o = dict(章=120, 行=3, 式='改', 原='二十七年前', 改='四十八年前', 出='测')
    T('④原文在该行两见 → 多见（红）', 核一(o, 书们.行(120))[0] == '多见')
    # ⑤ 移
    o = dict(章=103, 行=9, 式='改', 原='他二十七年前来过。', 改='x', 出='测')
    s = 核一(o, 书们.行(103))
    T('⑤原文不在该行而在该章白文恰一见 → 移，重锚其行', s[0] == '移' and s[1] == 3, s)
    # ⑥ 无
    ls2 = ['甲乙。', '', '甲乙。', '']
    T('⑥原文全章两见而不在该行 → 无（⛔猜）', 核一(dict(章=1, 行=2, 式='改', 原='甲乙。', 改='丙', 出='测'), ls2)[0] == '无')
    # ⑦ 字形
    o = dict(章=103, 行=3, 式='改', 原='他二十七年前来过。', 改='他四十八年後来过。', 出='测')
    o2 = dict(o, 改='他四十八年后来过。')
    T('⑦字形不合即红：该章白文只用「后」而改作有「後」；用「后」则合', 字形(o, 书们.行(103)) and not 字形(o2, 书们.行(103)))
    # ⑧ B 今算＝表、表多一行即红
    T('⑧B 由今文自算（减 A 之行、减出 B 入 A）＝表 → 无 B 红', 果['B今'] == {(120, 3): 2, (187, 4): 1} and not any(x.startswith('B ') for x in 果['红']), (果['B今'], 果['红']))
    表2 = 读表(主案文(A行, B行 + ['| 120 | 1 |'], C1), 裁文(丙行), 配)
    T('⑨B 表有而今文无（或数异）→ 红', any(x.startswith('B 120:1') for x in 核(书们, 表2, 配)['红']))
    # ⑩ 盖
    书文2 = dict(书文)
    书文2[103] = 书文[103].replace('“我背包袱。”', '“我背包袱。”二十七年。')
    果2 = 核(书(None, 文们=书文2), 表, 配)
    T('⑩盖：A 之行另有「二十七年」在原文之外 → 红（无表盖之）', any(x.startswith('盖 103:7') for x in 果2['红']), 果2['红'])
    # ⑪ C1
    T('⑪C1 由亮点行算（减 C2 送信）＝表', 果['C1今'] == {(103, 12): 1, (120, 9): 1} and not any(x.startswith('C1') for x in 果['红']), (果['C1今'], 果['红']))
    # ⑫ 一行多处
    新, m, r, y, k = 施章(['那是二十七年前，二十七年前的事。'], [dict(行=1, 式='换数', 处=2)], False)
    T('⑫一行多处：B 之行「二十七年」全换', 新 == ['那是四十八年前，四十八年前的事。'] and not r, (新, r))
    新, m, r, y, k = 施章(['那是二十七年前，二十七年前的事。'], [dict(行=1, 式='换数', 处=1)], False)
    T('⑬处数不合表 → 红（⛔只换其一）', r and 新 == ['那是二十七年前，二十七年前的事。'])
    # ⑭ 段（非星章）与连书
    新, m, r, y, k = 施章(['甲。', '', '乙。'], [dict(行=1, 式='后添', 原='甲。', 改='丙。〔另起段〕〔另起段〕丁。')], False)
    T('⑭段：後添＝空行＋段；连书〔另起段〕只作一次（不生空段）', 新 == ['甲。', '', '丙。', '', '丁。', '', '乙。'] and m == [1, 6, 7] and not r, (新, m, r))
    # ⑮ ＊之式
    新, m, r, y, k = 施章(['甲。', '', '＊', '', '乙。'], [dict(行=1, 式='后添', 原='甲。', 改='丙。〔另起段〕丁。')], True)
    T('⑮＊之式：星章後添＝空行＋＊＋空行＋段（逐段）', 新 == ['甲。', '', '＊', '', '丙。', '', '＊', '', '丁。', '', '＊', '', '乙。'] and m == [1, 10, 11, 12, 13], (新, m))
    # ⑯ 改段
    新, m, r, y, k = 施章(['针我也给了他们。一人一根。', '', '乙。'], [dict(行=1, 式='改＋后添', 原='针我也给了他们。一人一根。', 改='针我也给了。〔另起段〕东头，我没有递。')], True)
    T('⑯改段：首段改於本行、余段照星章之式另起', 新 == ['针我也给了。', '', '＊', '', '东头，我没有递。', '', '乙。'] and m == [1, 6, 7], (新, m))
    # ⑰ 删段连空
    旧 = ['甲。', '', '删我。', '', '乙。']
    新, m, r, y, k = 施章(旧, [dict(行=3, 式='删', 原='删我。')], False)
    T('⑰删段连其隔空行（其後之空行）：⛔留连空；删行映 None', 新 == ['甲。', '', '乙。'] and m == [1, 2, None, None, 3] and k['删'] == [3, 4] and not r, (新, m, r))
    # ⑱ 317 式：删「＊」与段，八行
    旧 = ['钱满走过来。', '', '＊', '', '他回到纸边上。', '', '＊', '', '他没有看图。', '', '＊', '', '刘二。']
    ops = [dict(行=3, 式='删', 原='＊'), dict(行=5, 式='删', 原='他回到纸边上。'), dict(行=7, 式='删', 原='＊'), dict(行=9, 式='删', 原='他没有看图。')]
    新, m, r, y, k = 施章(旧, ops, True)
    T('⑱星章删四行连其隔空行＝删八行，前後无连空、无「＊」相连', 新 == ['钱满走过来。', '', '＊', '', '刘二。'] and k['删'] == list(range(3, 11)) and not r, (新, k['删'], r))
    # ⑲ 删非整行
    新, m, r, y, k = 施章(['甲乙丙。'], [dict(行=1, 式='删', 原='甲乙')], False)
    T('⑲「删」而该行另有他字 → 红（⛔删整行吞字）', bool(r) and 新 == ['甲乙丙。'])
    # ⑳ 映之正（模拟 103：删二行；313：改段 +4）
    新文, 映, 记, 红s, 黄s, 待 = 模拟(书们, 果, [103, 313, 120, 187], False, 配)
    ok映 = (映[103][:7] == [1, 2, 3, 4, None, None, 5] and 记[103]['新长'] == 记[103]['旧长'] - 2 and
           映[313] == [1, 2, 3, 8, 9, 10, 11, 12] and all(映[120][i] == i + 1 for i in range(len(映[120]))))
    锚 = all(书们.行(103)[i - 1] == 新文[103][j - 1] for i, j in enumerate(映[103], 1) if j and i not in 记[103]['动'])
    T('⑳映之正：删行 None、其後前移、改段之後移 +4、未动之行内容锚同', ok映 and 锚, (映[103], 映[313]))
    T('㉑行差不合裁之定差 → 红（103 删二行而裁 0）', any('第103章 行差 -2' in x for x in 红s), 红s)
    # ㉒ 拒根
    T('㉒无 --根 即拒；--根 为主树（无 --落）即拒', 拒根(None).startswith('⛔无 --根') and (拒根(主树).startswith('⛔--根 为主树') or not os.path.isdir(主树)))
    rc = 静(main, ['--施'])
    T('㉓main --施 无 --根 → rc 2（一字未写）', rc == 2)
    # ㉔ 一次写盘 与 二跑即拒（真档：临时之根）
    tmp = tempfile.mkdtemp(prefix='D1施自测_')
    try:
        os.makedirs(os.path.join(tmp, '正文')); os.makedirs(os.path.join(tmp, '设定', '剧情庭题'))
        open(os.path.join(tmp, 主案), 'w', encoding='utf-8').write(主案文(A行, B行, C1))
        open(os.path.join(tmp, 裁档), 'w', encoding='utf-8').write(裁文(丙行))
        名 = {103: '一百零三', 313: '三百一十三', 120: '一百二十', 187: '一百八十七', 211: '二百一十一'}
        for n, t in 书文.items():
            open(os.path.join(tmp, '正文', '镇冢秘术_第%s章_测.md' % 名[n]), 'w', encoding='utf-8').write(t)
        前 = {f: open(os.path.join(tmp, '正文', f), encoding='utf-8').read() for f in os.listdir(os.path.join(tmp, '正文'))}
        配2 = dict(配, 定差={103: -2, 313: 4})
        rc坏 = 静(跑施, tmp, ['--施', '--根', tmp, '--批', '全'], 配)        # 103 行差 -2 ≠ 定差 0 → 红 → 一字不写
        后 = {f: open(os.path.join(tmp, '正文', f), encoding='utf-8').read() for f in os.listdir(os.path.join(tmp, '正文'))}
        T('㉔一次写盘：一章有红（行差）→ 诸章皆不写、映不吐', rc坏 == 1 and 前 == 后 and not os.path.exists(os.path.join(tmp, 映档)))
        rc落 = 静(跑施, tmp, ['--施', '--根', tmp, '--批', '全', '--落'], 配2)          # ★驳席：配2 本可施，只缺基线
        后2 = {f: open(os.path.join(tmp, '正文', f), encoding='utf-8').read() for f in os.listdir(os.path.join(tmp, '正文'))}
        T('㉔之二 --落 而无基线 → 红、一字不写（keep-lines 施前之比⛔静悄悄跳过）', rc落 == 1 and 前 == 后2 and not os.path.exists(os.path.join(tmp, 映档)))
        rc好 = 静(跑施, tmp, ['--施', '--根', tmp, '--批', '全'], 配2)
        d = json.load(open(os.path.join(tmp, 映档), encoding='utf-8')) if os.path.exists(os.path.join(tmp, 映档)) else {}
        t103 = open(os.path.join(tmp, '正文', '镇冢秘术_第一百零三章_测.md'), encoding='utf-8').read()
        T('㉕施：写盘、吐映（删行 null、五章之映）', rc好 == 0 and d.get('章', {}).get('103', {}).get('映', {}).get('5', 1) is None
          and '四十八年前来过' in t103 and '七八十' not in t103 and '313' in d.get('章', {}), (rc好, list(d.get('章', {}))))
        rc二 = 静(跑施, tmp, ['--施', '--根', tmp, '--批', '全'], 配2)
        T('㉖二跑即拒（原文已不在、B 行已无「二十七年」→ 红）', rc二 == 1)
        # ㉗ 行数守（注入 rev 之文）
        旧档 = {('正文/镇冢秘术_第%s章_测.md' % 名[n]): t for n, t in 书文.items()}
        open(os.path.join(tmp, '设定', '某档.md'), 'w', encoding='utf-8').write('一\n二\n三\n')
        旧档['设定/某档.md'] = '一\n二\n'
        列 = lambda: (sorted(旧档), [映档.replace(os.sep, '/')])
        红g, 黄g, 计g = 行数守(tmp, 'HEAD', 配2, 取旧=lambda rels: {r: 旧档.get(r) for r in rels}, 列变=列)
        T('㉗行数守：非五章之档（设定）多一行 → 红；五章合映 → 不红', any('设定/某档.md 行数 2→3' in x for x in 红g) and 计g['五章合'] == 2
          and not any('第103章' in x or '第313章' in x for x in 红g), 红g)
        p103 = os.path.join(tmp, '正文', '镇冢秘术_第一百零三章_测.md')
        open(p103, 'w', encoding='utf-8').write(t103.replace('后来他走了。', '后来他走了，静漂。'))
        红h, _, _ = 行数守(tmp, 'HEAD', 配2, 取旧=lambda rels: {r: 旧档.get(r) for r in rels}, 列变=列)
        open(p103, 'w', encoding='utf-8').write(t103 + '多一行\n')
        红i, _, _ = 行数守(tmp, 'HEAD', 配2, 取旧=lambda rels: {r: 旧档.get(r) for r in rels}, 列变=列)
        T('㉘行数守：五章未动之行变（静漂）→ 红；五章行数与映不合 → 红', any('内容锚不合' in x for x in 红h) and any('映 ' in x and '第103章 行数' in x for x in 红i), (红h, 红i))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ㉙ 六式与 canon
    书3 = 书(None, 文们={313: '第三百一十三章\n东头第二趟上来。\n底下写：东头的手。\n东头把地上那一卷绳的头拎起来，在自己手腕上绕了一圈。\n',
                         268: '第二百六十八章\n他这三年学会的。\n', 104: '第一百零四章\n今天他四十一。第四十一天。\n'})
    命 = 六式之命(书3)
    T('㉙终验六式：东头下水 2（拎绳之句⛔认）、这三年 1、四十一作年岁 1（第四十一天⛔认）', len(命['313／317 东头下水']) == 2 and len(命['268「这三年」']) == 1
      and len(命['「四十一」作年岁']) == 1, {k: len(v) for k, v in 命.items()})
    事实 = [dict(id='F002_年龄', forbid=[r'我[^。\n]{0,2}二十[一二四五六七八九]岁'], from_ch=1), dict(id='F168_x', forbid=['四十一'], from_ch=200)]
    cn = canon禁(None, 书(None, 文们={104: '我二十四岁。\n【本章亮点】\n我二十四岁。\n', 313: '四十一。\n'}), 事实=事实)
    T('㉚canon 禁式：只跑白文、from_ch 照守', sorted((x[0], x[1]) for x in cn) == [('F002_年龄', 104), ('F168_x', 313)], cn)
    书4 = 书(None, 文们={103: '“为什么是我们家。”\n“那个娃娃，是我。叫他先别跟你说。”\n', 313: '东头，我没有递。\n'})
    书5 = 书(None, 文们={103: '“为什么是我们家。”路上……\n', 313: '针我也给了。东头，我没有递。\n'})
    T('㉛护三拍：各自成段则无缺；并段（压拍）即缺', not 护之缺(书4) and len(护之缺(书5)) == 3, 护之缺(书5))
    # ★1020·W58 驳席所补四格
    o后 = dict(章=1, 行=1, 式='后添', 原='甲。', 改='丙。〔另起段〕丁。', 出='测')
    o段 = dict(章=1, 行=1, 式='改＋后添', 原='乙。', 改='甲。〔另起段〕乙。', 出='测')     # 317:133 之形：末段即原文
    o含 = dict(章=1, 行=1, 式='改', 原='他不说。', 改='他来过。他不说。', 出='测')         # 111:273 之形：改作含原文
    T('㉜二跑：後添之段已在、改段（末段即原文）已施、改作含原文已施 → 已施（⛔判合／移而再施）；施前照判合',
      核一(o后, ['甲。', '', '丙。', '', '丁。'])[0] == '已施' and 核一(o后, ['甲。', '', '乙。'])[0] == '合'
      and 核一(o段, ['甲。', '', '乙。'])[0] == '已施' and 核一(o段, ['乙。'])[0] == '合'
      and 核一(o含, ['他来过。他不说。'])[0] == '已施' and 核一(o含, ['他不说。'])[0] == '合',
      (核一(o后, ['甲。', '', '丙。', '', '丁。']), 核一(o段, ['甲。', '', '乙。']), 核一(o含, ['他来过。他不说。'])))
    出p = os.path.join(主树, '设定', '_草', 'W58', '窗_驳测_不该在')
    空 = tempfile.mkdtemp(prefix='D1施自测窗_')
    try:
        try:
            rc窗 = 静(跑窗, 空, ['--窗', '--出', 出p])      # 空根：守若失，读表即崩於建目之前——本格⛔真写主树
        except Exception as e:
            rc窗 = repr(e)[:80]
    finally:
        shutil.rmtree(空, ignore_errors=True)
    T('㉝--窗 之 --出 指进主树（无 --落）→ rc 2、⛔建目', rc窗 == 2 and not os.path.exists(出p), rc窗)
    T('㉞映区：只列移者、删行另列（null 不入区）', 映区([1, 2, None, None, 3, 4, 9, 10, 11]) == [[5, 6, -2], [7, 9, 2]], 映区([1, 2, None, None, 3, 4, 9, 10, 11]))
    o移 = dict(章=1, 行=4, 式='改', 原='甲乙。', 改='丙丁。', 出='测')
    s1, s2 = 核一(o移, ['甲。', '★批注：甲乙。', '', '丙。', '甲乙。']), 核一(o移, ['甲。', '★批注：甲乙。', '', '丙。'])
    T('㉟移只认白文：★ 批注之行另见原文⛔算一见、⛔移去批注', s1[:2] == ('移', 5) and s2[0] == '无', (s1, s2))
    # ★1021·W58 环2：改段而改作之後段即原文（317:133 之形）→ 旧行之映随原文（133→137），与 difflib 之等块（行号随移之互证）相合
    import difflib
    旧 = ['甲。', '', '纸角翘起来。没有人去压它。', '', '乙。']
    o317 = dict(行=3, 式='改＋后添', 原='纸角翘起来。没有人去压它。', 改='钱满走到水边。〔另起段〕〔另起段〕纸角翘起来。没有人去压它。')
    新, m, r, y, k = 施章(旧, [o317], True)
    等 = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, 旧, 新, autojunk=False).get_opcodes():
        if tag == 'equal':
            等.update({i1 + q + 1: j1 + q + 1 for q in range(i2 - i1)})
    证 = all(等[i] == j for i, j in enumerate(m, 1) if i in 等 and 旧[i - 1].strip())
    新b, mb, rb, yb, kb = 施章(['纸角。'], [dict(行=1, 式='改＋后添', 原='纸角。', 改='钱满。〔另起段〕纸角。')], False)
    新c, mc, rc_, yc, kc = 施章(['他说：纸角。'], [dict(行=1, 式='改＋后添', 原='纸角。', 改='钱满。〔另起段〕纸角。')], False)
    T('㊱改段而改作之後段即原文（三一七章一三三行之形）：旧行映随原文（星章 3→7、非星 1→3）、与 difflib 等块相合；原文落处同文则⛔记动、带余字则记动',
      新 == ['甲。', '', '钱满走到水边。', '', '＊', '', '纸角翘起来。没有人去压它。', '', '乙。'] and m == [1, 2, 7, 8, 9] and 证
      and k['动'] == [] and not r and 新b == ['钱满。', '', '纸角。'] and mb == [3] and kb['动'] == []
      and 新c == ['他说：钱满。', '', '纸角。'] and mc == [3] and kc['动'] == [1], (新, m, 证, k['动'], mb, mc, kc['动']))
    print('D1施·自测 %d/%d' % (ok, 共))
    print('自测 %d/%d' % (ok, 共))
    return 0 if ok == 共 else 1


def main(a):
    根 = _参(a, '--根')
    if a and a[0] == '--自测':
        return 自测()
    if '--改单' in a:
        return 跑改单(根, a)
    if a and a[0] == '--施':
        return 跑施(根, a)
    根 = os.path.realpath(根) if 根 else ROOT
    if a and a[0] == '--核':
        return 跑核(根, a)
    if a and a[0] == '--窗':
        return 跑窗(根, a)
    if a and a[0] == '--行数守':
        return 跑行数守(根, a)
    if a and a[0] == '--终验':
        return 跑终验(根, a)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
