#!/usr/bin/env python3
"""剧情全图（W907 立·1119 作者令「从第一章到最后一章……一眼就能了解所有从头到尾的剧情……一眼就定位到哪个地方的
剧情有问题，哪个地方的剧情还有可以升级的空间……随着整本书不断进化」·常令 1119·法用#剧情全图）——零 token。

为何立：全书之脊（总览②）、逐章之记（第N章.md）、诸账（到期账、canon FS、大问表、约到期、悬念哨、悬线、大审、
  二稿账、段案、行家评、盲读）散在百余档；二稿与大审之时须一眼见全书之脊、未闭之环、漏与可升之处。本器只并既有之源：
  图首「一眼」（十余行·短而全：书至、脊、今站之弧、未闭之环之数与最急、漏之最热、可升之最要、末章之悬、源之病）｜
  ⓪源之鲜｜①一页之脊（站—段—章段）｜②开环之账｜③漏之位（按章聚热）｜④可升之位｜⑤逐章一行（档末）。
⛔限：只读、只并、只算章之差——⛔改正文、⛔改任何账之判；每条引其源（档:行），错在源则改源（照各源之写者）。
  诸析俱 import 其器（剧情链.站们／节之文、段案验.节们、段料.段首、大问表、约到期.扫、悬念哨.判、FS闸.未销、
  大审.诸册／限於、小说检察官._CLEARED_STATES）——⛔同功两处；一源坏只⓪报其缺，⛔崩。
写者唯一：唯 封版 --後 之「剧情全图」步（剧情链之後）写此档——⛔记席、⛔他器、⛔总编辑之坐重跑提交（两坐各写同一档即并时相冲·
  照进化树之例）。诸源封版之外常改（二稿账、到期账、canon、段案、大审……），图随下一封版而新：其间之旧只 ⚠（全测之格绿而带 ⚠）。
何时读（用法.md §二）：二稿、大审、开段之前先读「一眼」（约二分钟）；一章 `--章 N`、一线 `--线 词`；每条带源（档:行），一跳可核。

用法：
  python3 工具/剧情全图.py             # 重生 → 设定/全书记忆/剧情全图.md（唯封版 --後 之步跑之）
  python3 工具/剧情全图.py --章 N      # 一章之全：其行、悬线之开欠、诸条、诸源之链
  python3 工具/剧情全图.py --线 <词>   # 一线之迹：所现之章（详记之事、要句、一句）、诸账之条
  python3 工具/剧情全图.py --验        # 再算与档比：同 rc 0｜旧 rc 2（⚠·待下一封版随）｜不在或结构坏 rc 1（⛔）
  python3 工具/剧情全图.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, difflib, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
记 = os.path.join('设定', '全书记忆')
图档 = os.path.join(记, '剧情全图.md')
将到 = 3          # 限（或宜於）在末章後 1—3 章（末章已封：限≤末即逾限、宜≤末即过宜）
久默 = 40         # 末见至今逾 40 章（与 大问表.上限 同数）——唯硬源（其末见係实数）；软源之末见只是其行所引，⛔计久默
权 = {'记录者': 1, '待执': 2, '情理之疑': 2, '判不治': 1, '半治': 2, '已挂': 2, '读不懂': 1, '读错': 2, '二稿病': 1,
     '记录者·不改': 0, '读错·有意': 0, '二稿病·似已施': 0}            # 权 0：已裁不改、作者有意之误读、二稿账未划而似已施——只入 --章 之列，⛔计热
旧账家 = ('记录者', '待执', '情理之疑')                                # 漏之二家（起章不同：记录者 11 起、盲读与大审 380 起——⛔混排）
读审家 = ('读不懂', '读错', '判不治', '半治', '已挂', '二稿病')
态序 = {'逾限': 0, '将到': 1, '疑未收': 2, '待裁': 3, '久默': 4, '常': 5}
源序 = {'到期账': 0, 'FS': 1, '大问表': 2, '大审已挂': 3, '约到期': 4, '悬念哨': 5, '末章悬线': 6, '段案·排收': 7, '站之欠': 8,
       '大悬': 9, '段案': 10}
软源 = ('末章悬线', '段案·排收', '站之欠', '大悬', '段案')
升序 = ('重造', '大审已挂', '先审', '行家低', '拍库低', '最记得空', '二稿改法')   # ④与一眼之定序（判者⑤c）


# ════ 器：所 import 之析（同功⛔两处）════
def 默器():
    """→ {名: 函}。import 败者其函一调即抛——由 _取 收入⓪（⛔崩）。"""
    器 = {}

    def _败(e):
        def f(*a, **k):
            raise RuntimeError('import 败：%s' % str(e)[:80])
        return f
    try:
        import 剧情链
        器['站们'], 器['节之文'] = 剧情链.站们, 剧情链.节之文
        器['站之病'] = getattr(剧情链, '站之病', None)      # 环1 所立（界之重漏）；无则只报本器所见之「不认」
    except Exception as e:
        器['站们'] = 器['节之文'] = _败(e)
    try:
        import 段案验
        器['节们'] = 段案验.节们
    except Exception as e:
        器['节们'] = _败(e)
    try:
        import 段料
        器['段首'] = 段料.段首
    except Exception as e:
        器['段首'] = _败(e)
    try:
        import 大问表
        器['大问'] = lambda: {'量': 大问表.量(), '挂': 大问表.挂(), '挂事': 大问表.挂事(), '已还': 大问表.已还(),
                             '判废': 大问表.判废(), '表外': 大问表.表外之挂(), '上限': 大问表.上限,
                             '表': [(n, w) for n, w, _ in 大问表.表]}
    except Exception as e:
        器['大问'] = _败(e)
    try:
        import 约到期
        器['约扫'] = 约到期.扫
    except Exception as e:
        器['约扫'] = _败(e)
    try:
        import 悬念哨
        器['悬念判'] = lambda 末: (悬念哨.判({k: v for k, v in 悬念哨.诸章().items() if k <= 末}), 悬念哨.限)   # ⛔末章後之稿（写中之章）
    except Exception as e:
        器['悬念判'] = _败(e)
    try:
        import FS闸
        器['FS未销'] = FS闸.未销
    except Exception as e:
        器['FS未销'] = _败(e)
    try:
        import 大审
        器['大审已挂'] = lambda: ((大审.诸册() or [(None, None)])[-1][0], 大审.限於(10 ** 6))
        器['大审三'], 器['大审诸挂'], 器['汉'] = 大审.三之行, 大审.诸挂, 大审._汉     # §三之行、诸册之挂（旧笔之隙）、章号之汉（寻正文）
        器['号之名'] = 大审.号之名                                                     # 「大审V #号」／次表之「大审V 前册#N」
    except Exception as e:
        器['大审已挂'] = 器['大审三'] = 器['大审诸挂'] = 器['汉'] = _败(e)
    try:
        import 小说检察官
        器['清态'] = lambda: tuple(小说检察官._CLEARED_STATES)
    except Exception as e:
        器['清态'] = _败(e)
    return 器


def _取(器, 名, 缺, *a):
    try:
        return 器[名](*a)
    except Exception as e:
        缺.append(('器', '%s 败：%s' % (名, ('%s %s' % (type(e).__name__, e))[:100])))
        return None


# ════ 小器 ════
def _读(p):
    try:
        return open(p, encoding='utf-8').read()
    except Exception:
        return None


def _短(s, k=60):
    s = re.sub(r'\s+', ' ', re.sub(r'\*\*|`', '', str(s or ''))).strip().replace('|', '｜')
    return s if len(s) <= k else s[:k - 1] + '…'


def _分(s):
    """以「｜」「；」分条（括、引之内⛔分）。"""
    出, 深, 当 = [], 0, ''
    for ch in s:
        if ch in '（(「『【[〔':
            深 += 1
        elif ch in '）)」』】]〕':
            深 = max(0, 深 - 1)
        if 深 == 0 and ch in '｜；;':
            if 当.strip(' 。'):
                出.append(当.strip().rstrip('。').strip())
            当 = ''
        else:
            当 += ch
    if 当.strip(' 。'):
        出.append(当.strip().rstrip('。').strip())
    return 出


def _合(ns):
    """[1,2,3,5] → 1—3、5"""
    ns = sorted(set(ns))
    出, i = [], 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        出.append(str(ns[i]) if i == j else '%d—%d' % (ns[i], ns[j]))
        i = j + 1
    return '、'.join(出)


def _章引(s, 末, 至多=3):
    """文中之章号（⛔「:L」行号、⛔四位之数）→ 前 至多 个。"""
    出 = []
    for x in re.findall(r'(?<![\dA-Za-z:：.])(\d{1,3})(?![\d])', s or ''):
        n = int(x)
        if 1 <= n <= 末 and n not in 出:
            出.append(n)
        if len(出) >= 至多:
            break
    return 出


# ════ 析：逐章记忆 ════
_止式 = re.compile(r'^\s*(?:[-*·]\s*)?\**\s*(?:记录者读时所见|总览席裁|记席裁)')
_标 = {'开': '开', '本章开': '开', '新开': '开', '埋': '开',
      '接': '接', '本章接': '接', '续': '接', '接回': '接',
      '收': '收', '结': '收', '兑': '收', '本章收': '收', '本章结': '收',
      '欠': '欠', '还欠': '欠', '仍挂': '欠', '仍欠': '欠'}
_点式 = re.compile(r'^(?:[-·]|\*(?!\*)|\d{1,2}[.、)）])\s*')   # 「*」只作点（⛔「**」粗体之首）


def 悬线析(文):
    """一章「## 悬线」之文 → {'开'|'接'|'收'|'欠': [(条, 节内行序)], '未识': [名]}。
    标签宽析（随书漂移）：本章开／本章接（1—10）、接／开／还欠（11—401·粗体）、结／收（342 起）、欠（399 起）、
    「- 结：」无粗体（433 起）、仍挂、续、带「（至本章末）」者俱认；节内非点之粗体签而不识者入「未识」（⓪计之）。
    「记录者读时所见」「总览席裁」「记席裁」以下⛔入悬线。433 起「- 结：」式之节里，行首「- X：」而 X 不识（≤4 字）者係新签
    （447「- 挂：」、448「- 作废：」），入「未识」、⛔并入前签（粗体签下之「- X：」仍是条）。"""
    出 = {'开': [], '接': [], '收': [], '欠': [], '未识': []}
    当, 当式 = None, None
    for i, l in enumerate((文 or '').split('\n')):
        if _止式.match(l):
            break
        s = l.strip()
        if not s:
            continue
        点 = bool(_点式.match(s))
        s2 = _点式.sub('', s)
        m = (re.match(r'^\*\*([^*]{1,14}?)\*\*\s*(?:[（(][^）)]{0,24}[）)])?\s*[：:]\s*(.*)$', s2)
             or re.match(r'^\*\*([^*：:]{1,14}?)[：:]\*\*\s*(.*)$', s2))
        粗 = bool(m)
        if not m:
            m = re.match(r'^([^\s*：:（(「\d\-—→|｜]{1,6}?)\s*(?:[（(][^）)]{0,24}[）)])?\s*[：:]\s*(.*)$', s2)
        名 = m.group(1).strip() if m else None
        if 名 in _标:
            当, 当式 = _标[名], ('粗' if 粗 else '点')
            余 = m.group(2).strip().strip('*').strip()
            if 余 and not re.fullmatch(r'[（(][^）)]*[）)]', 余):
                出[当] += [(x, i) for x in _分(余)]
            continue
        if 粗 and not 点 and l[:1] not in ' \t':
            出['未识'].append(re.sub(r'[（(][^）)]*[）)]', '', 名).strip() or 名)
            当 = None
            continue
        if m and not 粗 and 点 and 当式 == '点' and l[:1] not in ' \t' and len(名) <= 4:
            出['未识'].append(名)
            当 = None
            continue
        if 点 and 当:
            出[当].append((s2, i))
    return 出


_已治式 = re.compile(r'已改|已治|已施|已删|已补')
_不改式 = re.compile(r'不改|判不治|⛔改|不治|不须改|毋改')
_裁首式 = re.compile(r'〔\**\s*裁\**\s*[：:]\s*\**\s*([^〕]{0,30})')
_裁不式 = re.compile(r'^(?:本章)?(?:白文一字)?(?:不改|不补|判不治|不治|毋改|⛔改|不须改)')
_裁改式 = re.compile(r'^(?:「[^」]{0,20}」\s*)?(?:改|删|补)')


def _条之等(x):
    """记录者一条 → '治'（书「已改／已治／已施／已删／已补」）｜'不'（已裁不改·权 0）｜'热'。
    有〔裁：…〕者只看裁首之词（复核·宜修：191②「〔裁：改「我们三个又下去了一趟」〕…读之可通，不改」⛔因句末之「不改」作不改）：
    任一裁首「改／删／补」→ 热；诸裁首俱「不改／不补／判不治」→ 不；无裁或裁首别有其词（「从今实」「亮点照白文」……）→ 照旧搜全条（「不改／判不治」→ 不）。"""
    if _已治式.search(x):
        return '治'
    首们 = [re.sub(r'^[\s*]+', '', h) for h in _裁首式.findall(x)]
    if any(_裁改式.match(h) for h in 首们):                    # 裁首「改／删／补」：计热（⛔因条中别处之「不改」作不改）
        return '热'
    if 首们 and all(_裁不式.match(h) for h in 首们):
        return '不'
    return '不' if _不改式.search(x) else '热'


def _诸条(s):
    """同行之备审 → 诸条：先①②（条之明标·其内之「；」只是分句），次 soft-N，再「｜；」。「无」→ []。
    「soft-2、soft-4 某事——不改」（471）之列举⛔切（标前係「、，」者不分）。"""
    s = (s or '').strip().strip('*').strip()
    if not s or re.fullmatch(r'[无（）()。\s*：:]*', s):
        return []
    for 候 in ([x for x in re.split(r'(?<![、，,])(?=[①-⑳])', s) if re.match(r'[①-⑳]', x)],
               [x for x in re.split(r'(?<![、，,])(?=soft-\d)', s) if 'soft-' in x]):
        if len(候) >= 2:
            return 候
    return _分(s) or [s]


def 记录者析(文):
    """→ (行 1 起 或 None, 未治之条数, 已治之条数, 不改之条数)：「**记录者读时所见（未改正文，备审）**」其行之文与其下诸点；
    条分三等（见 _条之等）：已治、已裁不改——二者⛔计热（只计其数·--章 列之）；余（含裁改而未施）计热。"""
    L = (文 or '').split('\n')
    for i, l in enumerate(L):
        if '记录者读时所见' not in l:
            continue
        m = re.search(r'[：:]\s*\**\s*(.*)$', l.split('记录者读时所见', 1)[1])
        条们 = _诸条(m.group(1) if m else '')
        for l2 in L[i + 1:]:
            s = l2.strip()
            if not s:
                continue
            if s.startswith('#') or not _点式.match(s):
                break
            if l2[:1] not in ' \t':
                条们.append(s)
        等 = [_条之等(x) for x in 条们]
        治, 不 = 等.count('治'), 等.count('不')
        return i + 1, len(条们) - 治 - 不, 治, 不
    return None, 0, 0, 0


def 亮点之分(节):
    """「## 亮点」诸点首括内之分（5—10；⛔「第N拍」「:L」）→ [分]"""
    出 = []
    for l in (节 or '').split('\n'):
        if not _点式.match(l.strip()):
            continue
        m = re.search(r'[（(]([^）)]*)[）)]', l)
        if not m:
            continue
        括 = re.sub(r'(?:大进|稿|拍库第|第)\s*[\d一二三四五六七八九十]+(?:\s*[、，,]\s*[\d一二三四五六七八九十]+)*', '', m.group(1))   # 「嫁大进5、2」之序号⛔作分
        for x in re.findall(r'(?<![第\d:：.\-—L进])(\d{1,2}(?:\.\d)?)(?![\d拍:：.\-—])', 括):
            if 5 <= float(x) <= 10:
                出.append(float(x))
    return 出


def _後(条):
    """「→N 以後／之後」→ N；「→後」（无数）→ 0；无 → None——开放之宜，⛔钉 N（判者③e）。"""
    m = re.search(r'→\s*(?:第\s*)?(\d{1,3})\s*章?\s*(?:以|之)?[後后]', 条 or '')
    if m:
        return int(m.group(1))
    return 0 if re.search(r'→\s*[後后]', 条 or '') else None


def _指(条, 章):
    """悬线一条 → (开於, 宜於 或 None, 自引键 如 '472:69' 或 None)；「→N 以後」「→後」宜作 None（开放·见 _後）。"""
    m = re.search(r'(?<![\d])(\d{1,3}):\d', 条)
    开 = int(m.group(1)) if m else 章
    m = re.search(r'→\s*(?:第\s*)?(\d{1,3})(?![\d:：])', 条)
    宜 = int(m.group(1)) if m else None
    if 宜 is None:
        m = re.search(r'[（(](\d{3})[）)]', 条)
        宜 = int(m.group(1)) if m else None
    if _後(条) is not None:
        宜 = None
    m = re.search(r'(?<![\d])[:：](\d{1,4})', 条)
    键 = '%d:%s' % (章, m.group(1)) if (m and not re.search(r'\d' + re.escape(m.group(0)), 条)) else None
    return 开, 宜, 键


def _引键(条, 章):
    """一条之首引 → 「N:L」（「470:53」照取；「:107」补其章）；无 → None。"""
    m = re.search(r'(?<![\d])(\d{1,3})[:：](\d+)', 条 or '')
    if m:
        return '%s:%s' % (m.group(1), m.group(2))
    m = re.search(r'(?<![\d])[:：](\d+)', 条 or '')
    return ('%d:%s' % (章, m.group(1))) if (m and 章) else None


def _账号(s):
    return re.search(r'(?<![A-Za-z])(?:PLOT|CHAR|SUS|PRES|COLD|FS)[-－]?[0-9A-Z]{1,4}', s or '')


# ════ 态 ════
def 判态(末, 限=None, 宜=None, 末见=None, 软=False, 态=None):
    """→ (态, 注)。末章已封（其限、其宜俱已过其章）：
    限（硬：账之到期章）：限 ≤ 末 → 逾限（限＝末者注「当章已封·待核」）；1 ≤ 限−末 ≤ 3 → 将到。
    宜於（软：记席之估、段案之钉）：⛔逾限；1 ≤ 宜−末 ≤ 3 → 将到；宜 ≤ 末 者注「过宜 N」（宜＝末注「末章当收·待核」）。
    末见至今逾 40 → 久默（唯硬源：软＝其末见只是行所引，⛔计）；余 → 常。态：源自定之态（疑未收、待裁）先之。"""
    注 = ''
    if 限 is not None:
        if 限 <= 末:
            return '逾限', ('逾 %d' % (末 - 限)) if 末 > 限 else '当章已封·待核'
        if 限 - 末 <= 将到:
            return '将到', '余 %d' % (限 - 末)
    elif 宜 is not None:
        if 宜 <= 末:
            注 = ('过宜 %d' % (末 - 宜)) if 末 > 宜 else '末章当收·待核'
        elif 宜 - 末 <= 将到:
            return '将到', '余 %d' % (宜 - 末)
    if 态:
        return 态, 注
    if 末见 is not None and not 软 and 末 - 末见 > 久默:
        return '久默', 注
    return '常', 注


def 环(源类, 源, 开於, 欠何, 末, 限=None, 宜=None, 宜文='', 末见=None, 注='', 态=None):
    软 = 源类 in 软源
    态, 态注 = 判态(末, 限, 宜, 末见, 软, 态)
    return {'类': 源类, '源': 源, '开於': 开於, '欠何': 欠何, '限': 限, '宜': 宜, '宜文': 宜文, '末见': 末见, '软': 软,
            '默': (末 - 末见) if 末见 is not None else None, '态': 态, '注': '·'.join(x for x in (态注, 注) if x)}


def 环序(x):
    态 = 态序[x['态']]
    if x['态'] == '逾限':
        距 = -(x['默'] or 0) if x['限'] is None else x['限']
    elif x['态'] == '将到':
        距 = x['限'] if x['限'] is not None else (x['宜'] or 0)
    elif x['态'] == '久默':
        距 = -(x['默'] or 0)
    else:
        距 = x['限'] if x['限'] is not None else (x['宜'] if x['宜'] is not None else 10 ** 6)
    return (态, 源序.get(x['类'], 9), 距, str(x['开於']), x['源'])


# ════ 析：行家评、盲读、二稿账、大审、段案 ════
def 行家评析(文):
    """→ {'胜': '稿四', '计': 96.5, '栏': '计／110', '满': 110, '十分': 8.77, '行': 31} 或 None（无十维之表或胜稿不在表）。
    只析表头末栏带「计／合／均／加权」者（其余入⓪）；胜稿取「## 名次」节首见之「稿X」。"""
    L = (文 or '').split('\n')
    胜 = None
    for i, l in enumerate(L):
        if l.startswith('## ') and '名次' in l:
            节 = '\n'.join(L[i:i + 60])
            m = (re.search(r'胜稿[：:]\s*\**\s*(稿[一二三四五六七八九十])', 节)                       # 「胜稿：稿一」
                 or re.search(r'(稿[一二三四五六七八九十])\**\s*[＞>]', 节)                           # 「稿四 ＞ 稿五 ＞ …」
                 or re.search(r'(稿[一二三四五六七八九十])[^稿\n]{0,30}?胜', 节)                       # 「稿五（换账）——胜」「稿四（胜·作底）」
                 or re.search(r'(?m)^\s*(?:1[.、]|一[、·])[^\n]{0,8}?(稿[一二三四五六七八九十])', 节))   # 「1. **稿四**」「一、稿一」
            胜 = m.group(1) if m else None                # ⛔取「先跑之印：稿一净重…」之首见
            break
    for i, l in enumerate(L):
        if not l.startswith('|'):
            continue
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if not (c and re.match(r'^\**稿\**$', c[0]) and re.search(r'计|合|均|加权', c[-1]) and len(c[-1]) <= 10):
            continue
        栏, 头 = c[-1], l
        行们 = []
        for j in range(i + 1, len(L)):
            if not L[j].startswith('|'):
                break
            d = [x.strip() for x in L[j].strip().strip('|').split('|')]
            if re.fullmatch(r'[-:\s]*', d[0]):
                continue
            数 = []
            for x in d[1:]:
                m = re.search(r'\d+(?:\.\d+)?', x)
                数.append(float(m.group(0)) if m else None)
            if 数 and 数[-1] is not None:
                行们.append((d[0], 数, j + 1))
        if not 行们:
            return None
        取 = [r for r in 行们 if 胜 and 胜 in r[0]]
        if not 取:
            return None
        名, 数, 行 = 取[0]
        计, 维 = 数[-1], [x for x in 数[:-1] if x is not None]
        if 计 <= 10.5:
            满 = 10
        elif len(维) >= 10 and 维[9] > 10:                       # ⑩栏已书其倍（「19」）
            满 = 110
        elif len(维) >= 10 and abs(计 - (sum(维[:10]) + 维[9])) <= 0.6:
            满 = 110
        elif len(维) >= 10 and abs(计 - sum(维[:10])) <= 0.6:
            满 = 100
        else:
            满 = 110 if ('110' in 头 or '×2' in 头 or 计 > 100) else 100
        return {'胜': 胜, '计': 计, '栏': 栏, '满': 满, '十分': round(计 / 满 * 10, 2), '行': 行}
    return None


_盲式 = re.compile(r'(?m)(?:^|(?<=[｜·\-*\s」]))\**\s*(读到发生了什么|读不懂处|读错处|最记得|前情之指)\s*\**\s*(?=[：:「])')
# 380—401 之旧式（行首之签：英文之键 understood／confused／misread／remember／happened／prior，或「① 读得懂吗」「② 有没有读错」
#   「④ 这一章发生了什么」「⑤ 最记得哪一拍」之问；⛔want_next）；旧式之节里行首「③」「④」「⑤」而无键者依其序（③想读 ④发生 ⑤最记得），
#   行首「想读／想不想」而无冒号者亦作想读之签（395:65「③ 想读下一章。她揣着…」：签无冒号，旧混入读错处之值，且「③」被算一条）
_旧键 = (r'understood|confused|misread|remember|happened|prior|want_next|why_next|读不读得懂|读得懂|读懂否|有没有读错|有无读错|读错之处'
        r'|读错处|读误|发生了什么|最记得|想不想|想读')
_旧盲式 = re.compile(r'(?m)^[ \t]*(?:[-*·][ \t]*)?\**[ \t]*(?:[①-⑳](?:之二)?[ \t]*)?[^\n：:「]{0,24}?'
                   r'(' + _旧键 + r')[^\n：:「]{0,30}?(?:\**[ \t]*[：:]|$)')
_序盲式 = re.compile(r'(?m)^[ \t]*\**[ \t]*(?:([③④⑤])|(?=想读|想不想))[ \t]*\**[ \t]*')
_序之签 = {'③': '想读', '④': '读到发生了什么', '⑤': '最记得', None: '想读'}
_旧盲 = (('confused', '读不懂处'), ('misread', '读错处'), ('remember', '最记得'), ('happened', '读到发生了什么'), ('prior', '前情之指'),
        ('understood', '读懂'), ('want_next', '想读'), ('why_next', '想读'), ('读不读得懂', '读不懂处'), ('读得懂', '读不懂处'),
        ('读懂否', '读不懂处'), ('读错', '读错处'), ('读误', '读错处'), ('发生了什么', '读到发生了什么'), ('最记得', '最记得'),
        ('想不想', '想读'), ('想读', '想读'))


def _空(v):
    """值空否：去标点後为空、或整值为「无／否／全懂……」；值首「否／无／没有」而随「（」或「。」者亦空（「否（misread=false）。…」）。"""
    if re.match(r'^\s*[*「]*\s*(?:否|无|没有)\s*[（(。]', v or ''):
        return True
    v = re.sub(r'[\s「」：:*｜。，（）()、\-]', '', v or '')
    return (not v) or bool(re.fullmatch(r'(?:是|否)?(?:无|没有|否|全懂|自报全懂|大体全懂|无读错|没有读错|无误读|均无|无不懂|都懂)[^\w]*', v))


def 盲读析(文):
    """→ [(签, 值, 行 1 起)]：_轮记.md「## 造式·盲读」节（多位盲读者俱收）；节在而签俱不识 → []；无节 → None。
    签之漂移：「读不懂处「…」｜读错处「…」」内联、「- 读不懂处：」点式、「**读不懂处**：」粗体、380—401 英文之键俱认。"""
    m = re.search(r'^## 造式·盲读[^\n]*\n(.*?)(?=^## |\Z)', 文 or '', re.M | re.S)
    if not m:
        return None
    节, 起 = m.group(1), (文 or '')[:m.start(1)].count('\n') + 1
    判 = re.search(r'(?m)^#{3,4} [^\n]*(?:本席之判|二、)', 节)          # 380：「### 二、本席之判」以下係核席之判（「读误与否：否」），⛔盲读者之答
    if 判:
        节 = 节[:判.start()]
    ms = [(x.start(), x.end(), x.group(1)) for x in _盲式.finditer(节)]
    旧 = 0
    for x in _旧盲式.finditer(节):
        if any(a <= x.start() < b or x.start() <= a < x.end() for a, b, _ in ms):
            continue
        ms.append((x.start(), x.end(), next(v for k, v in _旧盲 if k in x.group(0))))
        旧 += 1
    if 旧:
        for x in _序盲式.finditer(节):
            行末 = 节.find('\n', x.start()) % (len(节) + 1)
            if not any(a <= x.start() < b or x.start() <= a <= 行末 for a, b, _ in ms):   # 同行已有签者⛔再认
                ms.append((x.start(), x.end(), _序之签[x.group(1)]))
    ms.sort()
    出 = []
    for k, (a, b, 签) in enumerate(ms):
        值 = 节[b: ms[k + 1][0] if k + 1 < len(ms) else len(节)]
        值 = re.split(r'\n#{2,4} ', 值)[0].strip().lstrip('：:*').strip()
        if 值.startswith('「'):
            值 = 值[1:]
        值 = re.sub(r'[」｜\s*]+$', '', 值)
        if 签 not in ('读懂', '想读'):
            出.append((签, 值, 起 + 节[:a].count('\n')))
    return 出


_条首 = r'(?:^|\n|\s|[「；;。]|(?<!\d)[：:])\s*(?:\d{1,2}(?:[.、](?!\d)|[)）])|[（(]\d{1,2}[)）]|[①-⑳]|[一二三四五六七八九十][、.])'   # 「1）380:49」：）後许数


def _读条(v):
    return max(1, len(re.findall(_条首, v or '')) + len(re.findall(r'(?m)^\s*- ', v or '')))


_有意式 = re.compile(r'作者有意|有意让我|错得舒服|读错是舒服|是舒服的|卡之所欲')   # 380:493「这一回读错是舒服的」


def _有意数(v):
    """读错之值里自注「作者有意让我先错」之条数：其注带「这两处／这N处」者计其前 N 条，否则计其所在之一条。"""
    if not _有意式.search(v or ''):
        return 0
    首们 = [x.start() for x in re.finditer(_条首, v)] or [0]
    条们 = [v[a:b] for a, b in zip(首们, 首们[1:] + [len(v)])]
    计 = set()
    for i, x in enumerate(条们):
        if _有意式.search(x):
            m = re.search(r'这([一二两三四五六七八九\d])处', x)
            k = ({'一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}.get(m.group(1)) or int(m.group(1))) if m else 1
            计 |= set(range(max(0, i - k + 1), i + 1))
    return min(len(计), _读条(v))


_他令式 = re.compile(r'拆|另起|增|补|移|并')


def _似已施(改, 白):
    """二稿账一条之改法与其章之白文 → True（似已施）｜'半'（半施·待核）｜False：
    其中「改「新句」」之新句俱已在白文、「删「旧句」」之旧句俱已不在（句≥4 字）→ 似已施；无此二式 → False。
    而改法於引号之改、删以外另有指令（引号外书「拆／另起／增／补／移／并」）者 → '半'——其余令器⛔可核，⛔判已施、留其权
    （复核·宜修：二稿账:132 [406] 换句已施而「第三行写完，」起另起一段未施，旧判似已施而⓪令划之，误）。"""
    if not 白:
        return False
    新 = [x.strip('，。；、 ') for x in re.findall(r'改(?:作|为|成)?「([^」]{4,})」', 改 or '')]
    旧 = [x.strip('，。；、 ') for x in re.findall(r'删「([^」]{4,})」', 改 or '')]
    新, 旧 = [x for x in 新 if len(x) >= 4], [x for x in 旧 if len(x) >= 4]
    if not (bool(新 or 旧) and all(x in 白 for x in 新) and all(x not in 白 for x in 旧)):
        return False
    return '半' if _他令式.search(re.sub(r'「[^」]*」', '', 改 or '')) else True


def 二稿账析(文, 末, 白=None):
    """→ (病们 [(章, 段, 病, 改, 行, 似已施)], 先审 ([章], 行), 况)：「## 病」以下未划之条（「- ~~」者已改）；先审之章取「执笔席失败之章」之行。
    章：其段之首章；段逾 40 章（久默之数）者与无章号之条（「[全书]」「[现文自有之缝…]」）作 0——⛔计入一章之热，亦⛔丢（附③列之）。
    似已施：白(n)→第 n 章白文；单章之条其改法已见於白文者 True（未划而已施·⛔计热；由二稿账之写者划之）；
    引号之改已见而另有拆段、另起诸令者 '半'（半施·待核：照计热，⛔令划）。
    况：{'节': 「## 病」之节在否, '条行': 全档「- [」之行数, '全书': 无章之条数, '重造': [(a, b)], '重造行': 行}——
    「## 病」之节不得或解出 0 条而档有「- [」之行者，⓪报（⛔静读 0）；重造取「局烂即造（…）」之章段（二稿之法·判者⑤a）。"""
    L = (文 or '').split('\n')
    病们, 先 = [], ([], None)
    况 = {'节': False, '条行': len([l for l in L if re.match(r'^\s*- (?:~~)?\[', l)]), '全书': 0, '重造': [], '重造行': None}
    在 = False
    for i, l in enumerate(L):
        if '执笔席失败之章' in l and '之章：' in l and 先[1] is None:
            段 = l.split('之章：', 1)[1].split('。', 1)[0]
            先 = ([int(x) for x in re.findall(r'(?<![\d—])(\d{3})(?![\d—])', 段)], i + 1)
        m = re.search(r'局烂即造（([^）]*)）', l)
        if m and 况['重造行'] is None:
            况['重造行'] = i + 1
            for a, b in re.findall(r'(?<!\d)(\d{1,3})(?:\s*—\s*(\d{1,3}))?(?!\d)', m.group(1).replace('／', '、')):
                况['重造'].append((int(a), int(b or a)))
        if l.startswith('## '):
            在 = l.startswith('## 病')
            况['节'] = 况['节'] or 在
            continue
        if not 在:
            continue
        m = re.match(r'^\s*- \[([^\]]+)\]\s*(.*)$', l)
        if not m:
            continue
        c = _章引(m.group(1), 末, 1)
        r = re.search(r'(?<![\dA-Za-z])(\d{1,3})\s*—\s*(\d{1,3})(?!\d)', m.group(1))
        宽 = (int(r.group(2)) - int(r.group(1))) if r else 0
        段 = [x.strip() for x in m.group(2).split('｜')]
        if not c:
            况['全书'] += 1
        n = 0 if (not c or 宽 > 久默) else c[0]
        改 = 段[2] if len(段) > 2 else ''
        单 = bool(re.fullmatch(r'\s*\d{1,3}(?:[:：][\d、，,—\s]+)?\s*', m.group(1)))      # 唯单章之条（「[407]」「[56:131]」）核其施；多章者⛔
        施 = _似已施(改, 白(n)) if (n and 单 and 白) else False
        病们.append((n, _短(m.group(1), 16), 段[0], 改, i + 1, 施))
    return 病们, 先, 况


def 大审析(文, 至, 三之行=None):
    """§三裁定表 → [(章, 裁类, 判之要, 限 或 None, 行, 号)]——逐行之析 import 大审.三之行（⛔同功两处·细④），本器只认其章：
    判栏「N:L」→ 据栏「N:L」→ 判栏首个章号（⛔「拍N」「第N拍」「#N」之数）→ 至。"""
    出 = []
    for r in (三之行 or _大审三)(文):
        m = re.search(r'(?<![\d])(\d{3})[:：]\d', r['判']) or re.search(r'(?<![\d])(\d{3})[:：]\d', r['据'])
        if m:
            章 = int(m.group(1))
        else:
            净 = re.sub(r'(?:拍|第|#|＃)\s*\d+(?:\s*[—\-–~～]\s*\d+)?', '', r['判'])
            章 = (_章引(净, 至, 1) or [至])[0]
        出.append((章, r['类'], _短(r['判'], 50), r['限'], r['行'], r['号']))
    return 出


def _审号(器, 至, 号):
    """「大审V #号」（次表之「前册#N」书「大审V 前册#N」）——import 大审.号之名；不得则旧式。"""
    f = (器 or {}).get('号之名')
    return f(至, 号) if callable(f) else '大审%d #%s' % (至, 号)


def _大审三(文):
    import 大审
    return 大审.三之行(文)


def _名(s):
    return re.sub(r'[\s「」『』“”"\'·，,。]', '', s or '')


def _似(a, b):
    a, b = _名(a), _名(b)
    if not a or not b:
        return False
    if a == b or (min(len(a), len(b)) >= 2 and (a in b or b in a)):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.6


_收式 = re.compile(r'收「([^」]+)」(?:（埋於\s*(\d{1,3})）)?(?:——([^；]*))?')


def 段案之收(种):
    """一章段案之「种」→ [(X, 埋於 或 None, 如何)]（「——」後之法；埋於可二位：「（埋於 41）」）。"""
    return [(x, int(k) if k else None, (w or '').strip()) for x, k, w in _收式.findall(种 or '')]


_否引式 = re.compile(r'零碰|零书|未收|未兑|未接|未落|仍挂|改钉|⛔接')


def 段案种析(段们, 末, 记=None):
    """段们：[(a, b, 档, {章: 节}, {章: 种行})] → 跨段之埋（埋於 ≤末，收章在其段外；段内由 段案验.验 管，此⛔重）
    → [(埋章, X, 收章, 宜於, 档:行, 况, 据)]。况（判者③d·须修①）：
      已收——段案有其收（收於 ≤末）：名似者（收「X'」·埋於 n 或未注）、或旁名而同章（收章 k 之段案有「收「…」（埋於 n）」·名不须似）；
      记忆已引——段案未记其收，而 前一指 後 ≤末 之详记「## 悬线」收／接之条含其名（或在收章 k 引「n:」且与其名有二字之交；条书「零碰／未收／仍挂」者⛔认）；
      排收——收在末章之後，段案已排（宜於其排之章）；未排——收在末章之後，段案未排（收段之案未立或无其收）；
      疑未收——收章 ≤末 而二者俱无（待核·⛔混作过宜）。据：已收、记忆已引者其章。
    一埋多指（复核·须修①：463「链、锁、手绳」→469／471／495、464「他知其处」→473／485、467「她的结」→470／476）：
      同 (n, X) 之诸指（段内之指在内）与诸收照章序一一相配——先配同章之收（c＝k），余指依序取未用之名似之收 c（c > 前一指）；
      一收只闭一指（⛔以 469 之收闭 495 之指）；未配之指照常判排收、未排、记忆已引、疑未收。
    记：{章: {'悬': 悬线析之果}}（无则⛔副证）。"""
    埋, 收 = {}, []
    for a, b, 档, 节, 行 in 段们:
        for n, d in 节.items():
            for x, k in re.findall(r'埋「([^」]+)」\s*→\s*收\s*(\d{3})', d.get('种', '')):
                v = 埋.setdefault((n, x), [])
                if all(k2 != int(k) for k2, *_ in v):
                    v.append((int(k), a, b, '%s:%s' % (档, 行.get(n, '?'))))
            for x, k, _ in 段案之收(d.get('种', '')):
                收.append((n, x, k))
    出 = []
    for (n, x), 指们 in 埋.items():
        if n > 末:
            continue
        指们.sort()
        似 = sorted({c[0] for c in 收 if c[0] > n and c[2] in (None, n) and _似(c[1], x)})
        旁 = {c[0] for c in 收 if c[2] == n}
        配, 用 = {}, set()
        for k, *_ in 指们:                                    # 先配同章之收
            if k in 似 or k in 旁:
                配[k], _ = k, 用.add(k)
        前 = n
        for k, *_ in 指们:                                    # 余指依序取未用之名似之收（c > 前一指）
            if k not in 配:
                c = next((c for c in 似 if c > 前 and c not in 用), None)
                if c is not None:
                    配[k], _ = c, 用.add(c)
            前 = k
        前 = n
        for k, a, b, 源 in 指们:
            前一, 前 = 前, k
            if a <= k <= b:
                continue                                      # 段内之指：只作配之序（段案验 管）
            c = 配.get(k)
            if c is not None:
                出.append((n, x, k, k, 源, '已收', c) if c <= 末 else (n, x, k, c, 源, '排收', None))
                continue
            if k > 末:
                立 = any(p <= k <= q for p, q, *_ in 段们)
                出.append((n, x, k, k, 源, '未排' + ('（段案无其收）' if 立 else '（收段之案未立）'), None))
                continue
            名 = _名(x)
            据 = None
            for c in range(max(n, 前一) + 1, 末 + 1):
                for t, _ in ((记 or {}).get(c, {}).get('悬', {}).get('收', []) + (记 or {}).get(c, {}).get('悬', {}).get('接', [])):
                    if _否引式.search(t):
                        continue
                    交 = any(名[i:i + 2] in _名(t) for i in range(len(名) - 1))
                    if (len(名) >= 2 and 名 in _名(t)) or (c == k and 交 and re.search(r'(?<!\d)%d[:：]\d' % n, t)):
                        据 = c
                        break
                if 据:
                    break
            出.append((n, x, k, k, 源, '记忆已引' if 据 else '疑未收', 据))
    return 出


def 用法之块(文):
    """用法.md §四站表之「块」栏 → [(a, b, 名)]（顶层之块；括内之细块⛔取）。"""
    出 = []
    for l in (文 or '').split('\n'):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(c) < 3 or not re.match(r'^E\d', c[0]):
            continue
        for 片 in _分(c[2]):
            片 = re.sub(r'[（(][^）)]*[）)]', '', 片).strip()
            片 = re.sub(r'^本站[：:]\s*', '', 片)
            m = re.match(r'^(.*?)\s*(\d+)—(\d+)\s*$', 片) or re.match(r'^(.*?)\s*(\d+)\s*$', 片)
            if m:
                a = int(m.group(2))
                b = int(m.group(3)) if m.lastindex >= 3 else a
                出.append((a, b, m.group(1).strip() or '（块）'))
    return 出


def 一句(文):
    """总览③之一句：去其首之「第N天（…）：」「暗177 天亮以前（…（…）…）：」之冠（括可嵌）。"""
    s = re.sub(r'\*\*|`', '', 文 or '')
    i = s.find('（')
    if 0 <= i <= 30 and '：' not in s[:i]:
        深 = 0
        for j in range(i, len(s)):
            深 += {'（': 1, '）': -1}.get(s[j], 0)
            if 深 == 0:
                if s[j + 1: j + 2] in ('：', ':'):
                    return s[j + 2:].strip()
                break
    return s


# ════ 并 ════
def 料(root=ROOT, 器=None):
    """诸源 → ctx（每源坏入 ctx['缺']，⛔抛）。"""
    器 = 器 or 默器()
    缺, 鲜 = [], []
    ctx = {'root': root, '缺': 缺, '鲜': 鲜, '器': 器}
    节之文 = 器.get('节之文')
    if not callable(节之文):
        节之文 = lambda t, 名: ''
    # ── 逐章记忆
    档们 = {}
    for f in glob.glob(os.path.join(root, 记, '第*章.md')):
        m = re.search(r'第(\d+)章\.md$', f)
        if m:
            档们[int(m.group(1))] = f
    末 = max(档们) if 档们 else 0
    ctx['末'] = 末
    章 = {}
    未识, 无节 = {}, {'悬线': [], '一句之要': []}
    无记录, 记录总, 已治总, 不改总 = [], 0, 0, 0
    for n in sorted(档们):
        t = _读(档们[n]) or ''
        try:
            悬 = 节之文(t, '悬线')
        except Exception:
            悬 = ''
        try:
            要 = 节之文(t, '一句之要')
            亮 = 节之文(t, '亮点')
        except Exception:
            要, 亮 = '', ''
        if not 悬:
            无节['悬线'].append(n)
        if not 要:
            无节['一句之要'].append(n)
        析 = 悬线析(悬)
        for x in 析['未识']:
            未识.setdefault(x, []).append(n)
        悬起 = next((i + 1 for i, l in enumerate(t.split('\n')) if l.startswith('## 悬线')), 0)
        行, 条, 治, 不 = 记录者析(t)
        if 行 is None:
            无记录.append(n)
        记录总 += 条
        已治总 += 治
        不改总 += 不
        章[n] = {'档': os.path.relpath(档们[n], root), '文': t, '悬': 析, '悬起': 悬起, '要': 要,
                 '亮': 亮点之分(亮), '记录者': (行, 条, 不)}
    ctx['章'] = 章
    缺号 = [n for n in range(1, 末 + 1) if n not in 章]
    鲜.append(('逐章记忆 `%s/第N章.md`' % 记, '1—%d' % 末 if 末 else '—', '%d 档' % len(章),
               '；'.join(x for x in (
                   ('缺档 %s' % _合(缺号)) if 缺号 else '',
                   ('无「## 悬线」%s' % _合(无节['悬线'])) if 无节['悬线'] else '',
                   ('无「## 一句之要」%s' % _合(无节['一句之要'])) if 无节['一句之要'] else '',
                   ('悬线之签不识 %d 处（%s）' % (sum(len(v) for v in 未识.values()),
                                          '、'.join('%s×%d·首 %d' % (k, len(v), v[0]) for k, v in sorted(未识.items(), key=lambda kv: -len(kv[1]))[:6])))
                   if 未识 else '',
                   ('记录者读时所见 %d 章有、未治 %d 条（已改 %d、已裁不改 %d ⛔计热）；无此行者 %s' % (len(章) - len(无记录), 记录总, 已治总, 不改总, _合(无记录))) if 章 else '')
                   if x) or '✓'))
    if not 章:
        缺.append(('逐章记忆', '无一档——诸析俱空'))
    # ── 总览
    总 = _读(os.path.join(root, 记, '总览.md'))
    索, 站文, 分段 = {}, {}, {}
    if 总 is None:
        缺.append(('总览.md', '不在'))
    else:
        m = re.search(r'^# .*?至第\s*(\d+)\s*章', 总, re.M)
        题 = int(m.group(1)) if m else None
        在三, 当站 = False, None
        for i, l in enumerate(总.split('\n')):
            if l.startswith('## '):
                在三 = l.startswith('## ③')
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if 在三 and len(c) >= 4 and c[0].isdigit():
                索[int(c[0])] = (c[1], c[2], c[3], i + 1)
            m2 = re.match(r'^### (E\d+)', l)
            if m2:
                站文[m2.group(1)] = {'行': i + 1, '题': l[4:].strip()}
                当站 = m2.group(1)
            elif l.startswith('### '):
                当站 = None
            elif l.startswith('- **此站之事**') and 站文 and 当站:
                站文[当站]['事'] = l.split('：', 1)[-1]
            elif re.match(r'^- \*\*(?:E\d+ )?读者之所欠', l) and 当站:
                站文[当站]['欠'] = (i + 1, re.sub(r'^\s*(?:〔(?!\d+〕)[^〕]*〕)?\s*[：:]?\s*', '', l.split('**', 2)[-1]))   # 「〔473〕」係分组之章⛔去
            elif l.startswith('- **分段**') and 当站:
                for 片 in _分(l.split('：', 1)[-1].rstrip('。')):
                    m3 = re.search(r'(?<![A-Za-z\d])(\d+)(?:—(\d+))?', 片)   # 「B1 柏冢初入 6—10」⛔取 B1 之 1
                    if m3:
                        名 = re.sub(r'\s*（', '（', re.sub(r'\s+', ' ', 片[:m3.start()] + 片[m3.end():])).strip(' ——')
                        分段[(int(m3.group(1)), int(m3.group(2) or m3.group(1)))] = 名
        缺行 = [n for n in range(1, 末 + 1) if n not in 索]
        无事 = [k for k in sorted(站文, key=lambda x: int(x[1:])) if not 站文[k].get('事')]
        鲜.append(('总览.md', '题「至第 %s 章」；③ %d 行' % (题, len(索)), '② %d 站' % len(站文),
                   '；'.join(x for x in (('③缺行 %s' % _合(缺行)) if 缺行 else '',
                                         ('题旧（末章 %d）' % 末) if 题 is not None and 题 < 末 else '',
                                         ('② %s 无「此站之事」（①之站事取段案之骨代之·其写者补）' % '、'.join(无事)) if 无事 else '') if x) or '✓'))
    ctx['索'], ctx['站文'], ctx['分段'] = 索, 站文, 分段
    # ── 站界（import 剧情链.站们；⛔另写站界之析——其病⓪报）
    站 = _取(器, '站们', 缺, root) or []
    站 = [(a, min(b, max(末, a)), t) for a, b, t in 站]
    认 = set(re.match(r'(E\d+)', t).group(1) for _, _, t in 站 if re.match(r'E\d+', t))
    漏站 = [k for k in sorted(站文, key=lambda x: int(x[1:])) if k not in 认]
    盖 = set(n for a, b, _ in 站 for n in range(a, b + 1))
    外 = [n for n in 章 if n not in 盖]
    界病 = []
    if callable(器.get('站之病')) and 站:
        try:
            界病 = list(器['站之病'](站))
        except Exception as e:
            界病 = ['站之病 败：%s' % str(e)[:60]]
    鲜.append(('站界（`剧情链.站们`）', '、'.join('%s %d—%d' % (t.split()[0], a, b) for a, b, t in 站) or '—', '%d 站' % len(站),
               '；'.join(x for x in (('⛔不认总览②之 %s（其章俱落前一站）' % '、'.join(漏站)) if 漏站 else '',
                                     ('站外之章 %s' % _合(外)) if 外 else '',
                                     ('界之病（`剧情链.站之病`）：%s' % '；'.join(界病)) if 界病 else '') if x) or '✓'))
    if not 站:
        站 = [(1, max(末, 1), '（站界不得）')]
    ctx['站'] = 站
    # ── 块（用法.md §四）与段（段料.段首）
    用 = _读(os.path.join(root, 记, '用法.md'))
    ctx['块'] = 用法之块(用) if 用 else []
    if 用 is None:
        缺.append(('用法.md', '不在——381 以前之章段不得'))
    段首 = 器.get('段首')
    try:
        段首(381)
    except Exception as e:                                # ⛔另写段界（同功两处）：段不得则 381 起之章段只照块、余标「未分块」
        缺.append(('器', '段料.段首 败：%s——381 起之段不得' % str(e)[:60]))
        段首 = None
    ctx['段首'] = 段首
    # ── 段案
    段们 = []
    for f in sorted(glob.glob(os.path.join(root, '设定', '段案', '*.md'))):
        m = re.search(r'(?:^|/)(\d+)-(\d+)\.md$', f)
        if not m:
            continue
        t = _读(f) or ''
        节 = _取(器, '节们', 缺, t) or {}
        L = t.split('\n')
        种行, 当 = {}, None
        for i, l in enumerate(L):
            m2 = re.match(r'^## (\d{3})\s*$', l)
            if m2:
                当 = int(m2.group(1))
            elif 当 and l.startswith('- 种：'):
                种行.setdefault(当, i + 1)
        m3 = re.match(r'^# [^（(\n]*[（(]([^\n]*)', t)
        题 = re.split(r'[：:；;]|——', m3.group(1))[0] if m3 else ''

        def 引行(k):          # 段之势：「> - **弧**（…）：…」「> - **骨**（…）：…」（判者①a：真者据此）
            x = re.search(r'(?m)^>?\s*- \*\*%s\*\*[^：:\n]*[：:]\s*(.*)$' % k, t)
            return re.sub(r'\*\*', '', x.group(1)).strip() if x else ''
        禁 = re.search(r'(?m)^.*\*\*本段之禁字\*\*.*$', t)
        段们.append({'a': int(m.group(1)), 'b': int(m.group(2)), '档': os.path.relpath(f, root), '节': 节, '种行': 种行, '题': 题,
                    '弧': 引行('弧'), '骨': 引行('骨'), '禁': re.findall(r'⛔「([^」]{1,6})」字', 禁.group(0)) if 禁 else [],
                    '日': {n: d.get('日', '') for n, d in 节.items()}})
    ctx['段案'] = 段们
    if not 段们:
        缺.append(('段案', '设定/段案/ 无一档'))
    return ctx


def _源行(text, 式):
    for i, l in enumerate((text or '').split('\n')):
        if re.search(式, l):
            return i + 1
    return None


def _字对(s):
    s = re.sub(r'[\s★·「」『』“”（）()、，,。；;：:\-—|｜/／]', '', s or '')
    return {s[i:i + 2] for i in range(len(s) - 1)}


def 收线表(文):
    """余章总案 §五 收线表 → [(悬, 收, 行)]（「余四十行」之总行⛔取）。"""
    m = re.search(r'(?ms)^## 五、收线表.*?(?=^## |\Z)', 文 or '')
    if not m:
        return []
    起 = (文 or '')[:m.start()].count('\n')
    出 = []
    for i, l in enumerate(m.group(0).split('\n')):
        c = [x.strip() for x in l.strip().strip('|').split('|')]
        if l.startswith('|') and len(c) >= 2 and c[0] != '悬' and not re.fullmatch(r'[-:\s]*', c[0]) and not c[0].startswith('余'):
            出.append((c[0], c[1], 起 + i + 1))
    return 出


def 配收线(欠, 表):
    """大悬之「欠何物」→ 收线表最似之行（二字之交为主、首词相同者先；无交 → None）。"""
    q = re.sub(r'[\s★「」]', '', 欠 or '')
    候 = []
    for 悬, 收, 行 in 表:
        首 = re.sub(r'[\s★「」]', '', 悬)[:2]
        交 = len(_字对(悬) & _字对(欠))
        if 交:
            候.append((q.startswith(首), 交, len(_字对(悬) & _字对(q[:12])), -行, (悬, 收, 行)))
    return max(候)[-1] if 候 else None


def _链章(收):
    """收线之链 → 章号（⛔「N:L」之行、⛔「第N段」、⛔四位与一位之数、⛔字母後之数）。"""
    return sorted(set(int(x) for x in re.findall(r'(?<![\d:：.§第拍#＃A-Za-z_])(\d{2,3})(?!\d|段)', 收 or '') if 10 <= int(x) <= 999))


def 线之键(线):
    """总览③之线·日 → 线之镜：「主」｜「暗·她」「暗·霍钧」「暗·黎东来」（「暗·黎东来镜（…）」去其「镜」）；无 → None。"""
    if (线 or '').startswith('主'):
        return '主'
    m = re.match(r'^暗·([^·（(\d日]+)', 线 or '')
    if m:
        return '暗·' + re.sub(r'镜$', '', m.group(1).strip())
    return '暗' if (线 or '').startswith('暗') else None


def 诸环(ctx):
    root, 末, 器, 缺, 鲜 = ctx['root'], ctx['末'], ctx['器'], ctx['缺'], ctx['鲜']
    出 = []
    记文 = {n: c['文'] for n, c in ctx['章'].items()}
    计 = ctx.setdefault('计', {})

    def 末提(号):
        ns = [n for n, t in 记文.items() if 号 in t]
        return max(ns) if ns else None
    # ── 大问表（先取：其词之末见并入 FS、大悬之末见·判者⑥b）
    q = _取(器, '大问', 缺)
    问见 = {}
    if q is not None:
        问见 = {r['名']: r['末见'] for r in q['量'][1] if r.get('末见')}
        问词 = {n: ws for n, ws in q['表']}

    def 并问见(文, 见):
        候 = [问见[n] for n, ws in (问词.items() if q is not None else []) if n in 问见 and any(w in (文 or '') for w in [n] + list(ws))]
        候 = [v for v in 候 + [见] if v]
        return max(候) if 候 else None
    # ── 到期账
    清态 = _取(器, '清态', 缺)                          # 已清之态 import 小说检察官._CLEARED_STATES（⛔另抄一份）
    p = os.path.join('设定', '到期账.json')
    t = _读(os.path.join(root, p))
    try:
        if 清态 is None:
            raise RuntimeError('已清之态不得（小说检察官）——⛔自判 open')
        d = json.loads(t)
        开们 = [x for x in d.get('items', []) if x.get('状态') not in 清态]
        坏 = []
        for x in 开们:
            号 = str(x.get('id'))
            try:
                ns = [int(m.group(0)) for k, v in x.items() if k.endswith('章') and k != '到期章' for m in [re.search(r'\d+', str(v))] if m]
                見 = max([n for n in ns + [末提(号) or 0] if n <= 末] or [None]) if ns else 末提(号)
                立 = re.search(r'\d+', str(x.get('立账章') or ''))
                限 = re.search(r'^\s*(\d+)', str(x.get('到期章') or ''))
                出.append(环('到期账', '`%s:%s`' % (p, _源行(t, r'"id":\s*"%s"' % re.escape(号))), int(立.group(0)) if 立 else '—',
                            '%s %s' % (号, _短(x.get('事'), 50)), 末, 限=int(限.group(1)) if 限 else None, 末见=見))
            except Exception as e:                       # 一条坏只弃其一（⛔弃整账）
                坏.append('%s（%s）' % (号, str(e)[:30]))
        if 坏:
            缺.append(('到期账', '%d 条析不得而弃：%s' % (len(坏), '、'.join(坏[:5]))))
        计['到期已清'] = len(d.get('items', [])) - len(开们)
        鲜.append(('到期账 `%s`' % p, '%d 条' % len(d.get('items', [])), 'open %d' % len(开们), '✓' if not 坏 else '⚠ 弃 %d 条' % len(坏)))
    except Exception as e:
        缺.append(('到期账', '%s 析不得：%s' % (p, str(e)[:60])))
    # ── canon FS（未销之判 import FS闸.未销）
    p = os.path.join('设定', 'canon事实库.json')
    t = _读(os.path.join(root, p)) or ''
    try:
        诸FS = {str(x.get('id')): x for x in json.loads(t).get('foreshadows', [])}
    except Exception:
        诸FS = {}
    植 = {k: x.get('plant') for k, x in 诸FS.items()}
    fs = _取(器, 'FS未销', 缺)
    if fs is not None:
        for x in fs:
            号 = str(x.get('id'))
            开 = int(植.get(号)) if str(植.get(号, '')).isdigit() else '—'
            見 = max([v for v in (末提(号), 开 if isinstance(开, int) else None) if v] or [None])
            見2 = 并问见(x.get('desc'), 見)
            出.append(环('FS', '`%s:%s`' % (p, _源行(t, r'"id":\s*"%s"' % re.escape(号))), 开, '%s %s' % (号, _短(x.get('desc'), 50)), 末,
                        限=int(x['due']) if str(x.get('due', '')).isdigit() else None, 末见=見2,
                        注='·'.join(z for z in (('改期 %s 回' % x.get('改期')) if x.get('改期') else '',
                                                ('末见取大问表同词') if 見2 != 見 else '') if z)))
        计['FS已销'] = len(诸FS) - len(fs)
        鲜.append(('canon FS（`FS闸.未销`）', '', '未销 %d' % len(fs), '✓'))
    # ── 大问表（import 量／挂／挂事／已还／判废／表外之挂）
    if q is not None:
        (末q, rows), G, 事, R, W, 外, 上 = q['量'], q['挂'], q['挂事'], q['已还'], q['判废'], q['表外'], q['上限']
        挂档 = os.path.join('设定', '大问挂账.md')
        挂文 = _读(os.path.join(root, 挂档)) or ''

        def _行(名):
            """其样於挂账册之行：状「挂」者取其末一行（同 大问表.挂 之读：後行覆前行），无则「还／废」之末行，再无则首行。"""
            候 = []
            for i, l in enumerate(挂文.split('\n')):
                c = [x.strip() for x in l.strip().strip('|').split('|')]
                if l.startswith('|') and len(c) >= 6 and re.sub(r'[*\s]', '', c[0]) == 名:
                    候.append((0 if c[-1] == '挂' else (1 if re.search(r'还|废', c[-1]) else 2), -i, i + 1))
            return '`%s:%d`' % (挂档, min(候)[2]) if 候 else '`工具/大问表.py`'
        for r in rows:
            名 = r['名']
            if 名 in R:
                continue
            if 名 in W:
                出.append(环('大问表', _行(名), r['末见'] or '—', '%s：%s' % (名, r['问']), 末, 宜文='判死於 %d' % W[名], 末见=r['末见'] or None,
                            注='判死不是清账'))
                continue
            限 = G.get(名, (r['末见'] + 上) if r['末见'] else 0)
            出.append(环('大问表', _行(名), r['末见'] or '—', '%s：%s' % (名, r['问']), 末, 限=限, 末见=r['末见'] or None,
                        注='' if 名 in G else '⛔逾四十而无挂账'))
        for 名, v in sorted(事.items()):
            # 挂事（判者②c）：其文首个「E\d」之站已在末章之前走完 → 逾限（事之站已过）；余作「待裁」——⛔一律判常
            站码 = re.search(r'E(\d+)', re.sub(r'\*\*', '', v))
            界 = next(((a, b) for a, b, tt in ctx['站'] if 站码 and tt.split()[0] == 'E' + 站码.group(1)), None)
            过 = bool(界 and 界[1] < 末)
            出.append(环('大问表', _行(名), '—', '%s（挂事）' % 名, 末, 宜文=_短(v, 40),
                        注=('事之站已过（%s 止 %d）·须当面裁其存废' % ('E' + 站码.group(1), 界[1])) if 过 else '挂事：须人答其事到没到',
                        态='逾限' if 过 else '待裁'))
        for 名, v in sorted(外.items()):
            出.append(环('大问表', _行(名), '—', '%s（表外之挂·器未量）' % 名, 末, 限=v))
        计['大问已还'] = sorted(R.items(), key=lambda kv: kv[1])
        鲜.append(('大问表（import）', '以第 %d 章计' % 末q, '九样；已还 %d、判死 %d、挂 %d、挂事 %d' % (len(R), len(W), len(G), len(事)),
                   ('⚠ 正文末章 %d ≠ 记忆末章 %d' % (末q, 末)) if 末q != 末 else '✓'))
    # ── 约到期（import 扫）
    ys = _取(器, '约扫', 缺, 200, 末)               # 只扫至记忆之末章（⛔写中之章之稿）
    if ys is not None:
        for x in [y for y in ys if y.get('欠')]:
            出.append(环('约到期', '正文 第%d章拍%d（`工具/约到期.py`）' % (x['立'], x['拍']), x['立'], '%s「%s」' % (x['号'], _短(x['文'], 40)),
                        末, 限=x['到期'], 末见=x['立']))
        鲜.append(('约到期（import 扫）', '200—%d' % 末, '立约 %d、欠 %d' % (len(ys), len([y for y in ys if y.get('欠')])), '✓'))
    # ── 悬念哨（import 判）
    sp = _取(器, '悬念判', 缺, 末)
    if sp is not None:
        (末s, 报), 限s = sp
        dt = _读(os.path.join(root, '设定', '到期账.json')) or ''
        for k, 見, 距, bad in 报:
            号 = '-'.join(k.split('-')[:2])
            行 = _源行(dt, r'"id":\s*"%s' % re.escape(号))
            出.append(环('悬念哨', '`设定/到期账.json:%s`' % 行 if 行 else '`工具/悬念哨.py`', 見 or '—', '%s（长悬之母题·距逾 %d 即报·只报）' % (k, 限s),
                        末, 宜=(見 + 限s) if 見 else None, 末见=見 or None))
        鲜.append(('悬念哨（import 判）', '以第 %d 章计' % 末s, '三账；逾 %d 者 %d' % (限s, len([1 for x in 报 if x[3]])), '✓'))
    # ── 悬线.md：一之大悬（宜於并余章总案 §五 收线表·判者⑥a⑩a）、诸节之鲜
    p = os.path.join(记, '悬线.md')
    t = _读(os.path.join(root, p))
    ctx['悬线文'] = t
    总案档 = os.path.join('设定', '剧情庭题', '余章总案.md')
    表 = 收线表(_读(os.path.join(root, 总案档)))
    if t is None:
        缺.append(('悬线.md', '不在'))
    else:
        m = re.search(r'^# .*?至第\s*(\d+)\s*章', t, re.M)
        题 = int(m.group(1)) if m else None
        节们 = {k: v for k, v in re.findall(r'(?ms)^## ([一二三四五六七八九十])、[^\n]*\n(.*?)(?=^## |\Z)', t)}
        节至 = {k: max(_章引(节们[k], 末, 10 ** 4) or [0]) for k in ('一', '六', '八', '十') if k in 节们}
        旧节 = ['%s（所引至 %d）' % (k, v) for k, v in 节至.items() if 末 - v > 10]
        无节 = [k for k in ('一', '六', '八', '十') if k not in 节们]
        在, 数, 旧宜, FS不合 = False, 0, [], []
        for i, l in enumerate(t.split('\n')):
            if l.startswith('## '):
                在 = l.startswith('## 一')
                continue
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if not (在 and l.startswith('|') and len(c) >= 3) or c[0] == '开' or re.fullmatch(r'[-:\s]*', c[0]):
                continue
            数 += 1
            开 = _章引(c[0], 末, 9)
            宜 = [n for n in _章引(c[2], 10 ** 4, 9) if n > 末]
            见 = max(_章引(' '.join(c[:3]), 末, 30) or [None])        # 表行三栏所引之章之末
            配 = 配收线(c[1], 表)
            链 = _链章(配[1]) if 配 else []
            注们 = []
            宜於, 宜文 = (min(宜) if 宜 else None), c[2]
            if 链:
                已, 未 = [n for n in 链 if n <= 末], [n for n in 链 if n > 末]
                见 = max([v for v in [见] + 已 if v] or [None])
                if (min(未) if 未 else None) != 宜於:
                    旧宜.append('%d' % (i + 1))
                宜於, 宜文 = (min(未) if 未 else None), '%s〔余章总案:%d〕' % (配[1], 配[2])
                注们.append('宜取余章总案（软）' if 未 else '余章总案之链俱 ≤%d（已写·待核其收；悬线.md 一宜随之）' % 末)
            见2 = 并问见(c[1], 见)
            if 见2 != 见:
                注们.append('末见并大问表同词')
            for fsid, 限n in sorted(set(re.findall(r'(FS\d+)[^|｜]{0,6}?限\s*(\d{3})', l))):
                due = (诸FS.get(fsid) or {}).get('due')
                if due is not None and str(due) != 限n:
                    FS不合.append('%s:%d 书 %s 限 %s·canon due %s' % (p, i + 1, fsid, 限n, due))
                    注们.append('%s 限与 canon 不合' % fsid)
            出.append(环('大悬', '`%s:%d`' % (p, i + 1), _合(开) or c[0], _短(c[1], 50), 末, 宜=宜於,
                        宜文=宜文, 末见=见2, 注='·'.join(注们)))
        if not 数:
            缺.append(('悬线.md', '一之大悬表解出 0 行（节题或表式改？）——⛔静读 0'))
        计['大悬旧宜'] = len(旧宜)
        十数 = len(re.findall(r'(?m)^- \*\*\d{3}（', 节们.get('十', '')))
        鲜.append(('悬线.md', '题「至第 %s 章」；诸节所引之末：%s' % (题, '、'.join('%s %d' % kv for kv in 节至.items())),
                   '一 %d 行；十 %d 条（⛔并入②：其条即诸章详记悬线之接写之锚，末章悬线已取）' % (数, 十数),
                   '；'.join(x for x in (
                       ('⚠ 节旧（距末章逾一段）：%s——交其写者随书' % '、'.join(旧节)) if 旧节 else '',
                       ('⚠ 节不得：%s' % '、'.join(无节)) if 无节 else '',
                       ('一之宜於与余章总案 §五 不合 %d 行（:%s；图取余章总案之链）' % (len(旧宜), '、:'.join(旧宜[:8]))) if 旧宜 else '',
                       ('⚠ FS 限与 canon 不合：%s' % '；'.join(FS不合)) if FS不合 else '',
                       ('题旧（末章 %d）' % 末) if 题 and 题 < 末 else '') if x) or '✓'))
    if not 表:
        缺.append(('余章总案', '%s §五 收线表不得——大悬之宜於只取悬线.md' % 总案档))
    # ── 末章之「## 悬线」：每线每镜各取其末章（主｜暗·她｜暗·霍钧｜暗·黎东来——判者·须修③）；末一段（10 章）以前止笔之镜⛔取
    线末 = {}
    for n, (名, 线, _, _) in ctx['索'].items():
        k = 线之键(线)
        if k and n in ctx['章']:
            线末[k] = max(线末.get(k, 0), n)
    线末 = {k: v for k, v in 线末.items() if 末 - v < 10}
    if not 线末 and ctx['章']:
        线末 = {'?': 末}
    ctx['线末'] = 线末
    後引 = {}
    for n, c in ctx['章'].items():
        後引[n] = ' '.join(x for x, _ in c['悬']['接'] + c['悬']['收'])
    见过 = {}
    for 线, n in sorted(线末.items(), key=lambda kv: -kv[1]):
        c = ctx['章'][n]
        for 类 in ('欠', '开'):
            for 条, i in c['悬'][类]:
                if _账号(条):
                    continue                                      # 已在其账（到期账／FS／悬念哨）
                开, 宜, 键 = _指(条, n)
                後 = _後(条)
                if 类 == '开' and 宜 is None and 後 is None:
                    continue
                if 类 == '开' and 键 and any(键 in 後引.get(k, '') for k in range(n + 1, 末 + 1)):
                    continue
                名 = re.split(r'[（(]', 条)[0].strip() or 条
                同 = next((y for y in 见过.values() if y['宜'] == 宜 and _似(y['名'], 名)), None)
                if 同:                                             # 诸镜同一条（「那一卷在苏衍怀」「那一卷」）：并入先见者，注其亦见
                    同['x']['注'] = '·'.join(z for z in (同['x']['注'], '亦见%s %d' % (线, n)) if z)
                    continue
                x = 环('末章悬线', '`%s:%d`' % (c['档'], c['悬起'] + 1 + i), 开, '〔%s〕%s' % (类, _短(条, 50)), 末,
                      宜=宜, 宜文=('%d 以後（开放）' % 後 if 後 else '其後（开放）') if 後 is not None else '', 末见=n,
                      注='' if 线 == '?' else 线)
                x['引'] = _引键(条, n)
                见过[len(见过)] = {'宜': 宜, '名': 名, 'x': x}
                出.append(x)
    末悬 = [x for x in 出 if x['类'] == '末章悬线']

    def _名之(x):
        return re.split(r'[（(]', re.sub(r'^〔[^〕]*〕', '', x['欠何']))[0]

    def 并入(宜, 名, 注, 引=None, 法=''):
        """与末章悬线同一环（同宜而名似、或同引「章:行」、或段案之法与其名似）：并入其行、注其亦见，⛔两列。"""
        同 = next((y for y in 末悬 if y['宜'] == 宜 and (_似(_名之(y), 名) or (引 and y.get('引') == 引)
                                                     or (法 and _似(_名之(y), re.split(r'[，、（(]', 法)[0])))), None)
        if 同:
            同['注'] = '·'.join(z for z in (同['注'], 注) if z)
        return 同
    # ── 大审：诸册之「已挂」（import 大审.诸挂——末册照常，前诸册旧笔不及／限非数者亦出·判者②）
    ctx['大审'] = []
    册们 = sorted((int(m.group(1)), f) for f in glob.glob(os.path.join(root, '设定', '大审_至第*章.md'))
                for m in [re.search(r'至第(\d+)章\.md$', f)] if m)
    三 = 器.get('大审三')
    for 至, f in 册们:
        try:
            行们 = 大审析(_读(f), 至, 三)
        except Exception as e:
            缺.append(('大审', '§三之析败（大审.三之行）：%s' % str(e)[:60]))
            break
        if 行们:
            ctx['大审'].append((至, os.path.relpath(f, root), 行们))
    for i, (至, 档, 行们) in enumerate(ctx['大审']):          # 次表之「前册#N」：其章取前诸册 #N 之章（407 前册#11 → 397 #11 → 391·⛔一律作 407）
        for j, x in enumerate(行们):
            m = re.match(r'^前册\s*#\s*(\d+)$', re.sub(r'[*\s]', '', x[5]))
            if m:
                前章 = next((y[0] for _, _, 前们 in reversed(ctx['大审'][:i]) for y in 前们
                            if re.sub(r'[*\s]', '', y[5]) == m.group(1)), None)
                if 前章:
                    行们[j] = (前章,) + tuple(x[1:])
    挂 = _取(器, '大审已挂', 缺)
    诸挂 = _取(器, '大审诸挂', 缺)
    ctx['诸挂'] = []
    if 诸挂 is not None and ctx['大审']:
        末册 = ctx['大审'][-1][0]
        if 挂 is not None and 挂[0] is not None and 挂[0] != 末册:
            缺.append(('大审', '大审.诸册 之末册（至 %s）≠ 本器所析之末册（至 %d）' % (挂[0], 末册)))
        章之 = {(至, x[5]): x[0] for 至, _, 行们 in ctx['大审'] for x in 行们}
        for x in 诸挂:
            章 = 章之.get((x['至'], x['号']), x['至'])
            旧 = x['至'] != 末册
            注 = ((('旧笔不及（限 %d > 下一册之至 %d）·待核' % (x['限'], x['下册'])) if x['限'] > x['下册'] else
                   '旧读不见（三栏之表／改挂·下一册之包⛔及）·待核') if (旧 and x['限'] is not None) else ('限非数·待裁' if x['限'] is None else ''))
            y = 环('大审已挂', '`%s:%d`' % (x['档'], x['行']), 章, '%s %s' % (_审号(器, x['至'], x['号']), _短(x['判'], 44)), 末, 限=x['限'],
                  注=注, 态='待裁' if x['限'] is None else None)
            出.append(y)
            ctx['诸挂'].append((章, x['至'], x['号'], x['限'], '`%s:%d`' % (x['档'], x['行']), y))
        隙 = [x for x in 诸挂 if x['至'] != 末册 and x['限'] is not None]
        计['旧笔之隙'] = len(隙)
        鲜.append(('大审 `设定/大审_至第N章.md`', '末册至第 %d 章' % 末册, '%d 册有表；已挂未收 %d' % (len(ctx['大审']), len(诸挂)),
                   '；'.join(z for z in (
                       ('⚠ 旧笔之隙 %d 笔（前诸册「已挂」限 > 其下一册之至而後无人收：%s——`大审.包` 之旧笔已补入）' % (
                           len(隙), '、'.join(_审号(器, x['至'], x['号'])[2:] for x in 隙[:8]) + ('…' if len(隙) > 8 else ''))) if 隙 else '',
                       ('限非数 %d 笔（待裁）' % len([1 for x in 诸挂 if x['限'] is None])) if any(x['限'] is None for x in 诸挂) else '',
                       ('⚠ 距末章 %d 章' % (末 - 末册)) if 末 - 末册 > 10 else '') if z) or '✓'))
    elif not ctx['大审']:
        缺.append(('大审', '无一册有 §三之表'))
    # ── 段案：跨段之埋（已收／记忆已引⛔入；排收、未排、疑未收入）＋下三章段案所排之收（段案·排收·判者③a）
    段们 = [(d['a'], d['b'], d['档'], d['节'], d['种行']) for d in ctx['段案']]
    孤 = 段案种析(段们, 末, ctx['章'])
    排 = []
    for d in ctx['段案']:
        for c, 节 in sorted(d['节'].items()):
            if 末 < c <= 末 + 将到:
                for X, k, 法 in 段案之收(节.get('种', '')):
                    排.append((c, X, k, 法, '%s:%s' % (d['档'], d['种行'].get(c, '?'))))
    已排 = set((k, c) for c, X, k, 法, _ in 排)
    for n, x, k, 宜, 源, 况, 据 in 孤:
        if 况 in ('已收', '记忆已引'):
            continue
        if 况 == '排收' and (n, 宜) in 已排:
            continue                                      # 下三章之排收另列（带其法）
        if 并入(宜, x, '亦见段案 %s' % 源.split('/')[-1]):
            continue
        出.append(环('段案', '`%s`' % 源, n, '埋「%s」→收 %d%s' % (_短(x, 30), k, '' if 况 in ('排收', '疑未收') else 况[2:]),
                    末, 宜=宜, 末见=n, 态='疑未收' if 况 == '疑未收' else None,
                    注='段案与记忆俱无其收' if 况 == '疑未收' else ''))
    for c, X, k, 法, 源 in 排:
        if 并入(c, X, '段案 %d 排收：%s' % (c, _短(法, 30)), 法=法):
            continue
        出.append(环('段案·排收', '`%s`' % 源, k or '—', '收「%s」%s——%s' % (_短(X, 24), ('（埋於 %d）' % k) if k else '', _短(法, 40) or '（法未书）'),
                    末, 宜=c))
    if ctx['段案']:
        from collections import Counter
        数 = Counter(x[5][:2] if x[5].startswith('未排') else x[5] for x in 孤)
        计['段案记忆已引'] = 数.get('记忆已引', 0)
        计['段案疑未收'] = 数.get('疑未收', 0)
        鲜.append(('段案 `设定/段案/a-b.md`', '%d—%d' % (ctx['段案'][0]['a'], ctx['段案'][-1]['b']), '%d 段' % len(ctx['段案']),
                   '；'.join(z for z in (
                       ('疑未收 %d（收章已写而段案与记忆俱无其收·待核）' % 数['疑未收']) if 数.get('疑未收') else '',
                       ('段案未记其收而记忆已引 %d（⛔入②·由段案之写者补其收）' % 数['记忆已引']) if 数.get('记忆已引') else '',
                       '跨段之埋（埋於 ≤%d）%d：段案已收 %d、排於末章後 %d、未排 %d；下三章段案所排之收 %d' % (
                           末, len(孤), 数.get('已收', 0), 数.get('排收', 0), 数.get('未排', 0), len(排))) if z)))
    # ── 总览② 诸站「读者之所欠」：带「→N」「（N）」而 N > 末者入（站之欠·软）；N ≤ 末者⛔并（E1 之「→」係已付之注）
    站欠, 弃欠 = 0, 0
    for 码, v in sorted(ctx['站文'].items(), key=lambda kv: int(kv[0][1:])):
        if not v.get('欠'):
            continue
        行, 文 = v['欠']
        组 = None                                          # E8 之欠以「〔473〕」分组：其下「（:107→474）」即 473:107
        for 条 in _分(文):
            条 = 条.lstrip('：: ')
            m = re.match(r'^〔(\d+)〕\s*', 条)
            if m:
                组, 条 = int(m.group(1)), 条[m.end():]
            指 = [int(a or b) for a, b in re.findall(r'→\s*(\d{3})|[（(](\d{3})[）)·、]', 条)]
            if not 指:
                continue
            未 = [x for x in 指 if x > 末]
            if 指[0] <= 末:                                 # 首指 ≤ 末（已付之注、或已过之宜）⛔并
                弃欠 += 1
                continue
            名 = re.split(r'[（(]', 条)[0].strip()
            if 并入(min(未), 名, '亦见总览② %s' % 码, _引键(条, 组) if 组 else None):
                continue
            站欠 += 1
            出.append(环('站之欠', '`%s/总览.md:%d`' % (记, 行), 码, _短(条, 60), 末, 宜=min(未)))
    计['站欠弃'] = 弃欠
    # ── 将到之撞（判者③b）：限／宜落之章，其段案之禁字见於欠何、或硬限落暗线之章
    for x in 出:
        if x['态'] != '将到':
            continue
        c = x['限'] if x['限'] is not None else x['宜']
        d = next((d for d in ctx['段案'] if d['a'] <= c <= d['b']), None)
        if not d:
            continue
        禁 = [w for w in d['禁'] if w in x['欠何']]
        注们 = ['⚠撞段案禁「%s」' % w for w in 禁[:2]]
        if x['限'] is not None and d['日'].get(c, '').startswith('暗'):
            注们.append('限落暗线章（%d %s）' % (c, d['日'][c]))
        if 注们:
            x['注'] = '·'.join(z for z in [x['注']] + 注们 if z)
    出.sort(key=环序)
    return 出


def 白文之(root, 器, n):
    """第 n 章正文之白文（【本章亮点】以前）；章号之汉 import 大审._汉（⛔另写）；不得 → None。"""
    try:
        汉 = 器['汉'](n)
    except Exception:
        return None
    fs = glob.glob(os.path.join(root, '正文', '*_第%s章_*' % 汉))
    t = _读(fs[0]) if fs else None
    return t.split('【本章亮点】')[0] if t else None


def 诸漏诸升(ctx):
    """→ (漏们 [(章, 类, 文, 源)], 升们 [(章, 类, 文, 源, 分)], 行家 {章: 析})"""
    root, 末, 缺, 鲜 = ctx['root'], ctx['末'], ctx['缺'], ctx['鲜']
    漏, 升 = [], []
    for n, c in ctx['章'].items():
        行, 条, 不 = c['记录者']
        if 条:
            漏.append((n, '记录者', '记录者读时所见 %d 条' % 条, '`%s:%d`' % (c['档'], 行), 条))
        if 不:
            漏.append((n, '记录者·不改', '记录者读时所见 已裁不改 %d 条（⛔计热）' % 不, '`%s:%d`' % (c['档'], 行), 不))
    t = ctx.get('悬线文')
    p = os.path.join(记, '悬线.md')
    if t:
        在, 六, 八, 有 = None, 0, 0, set()
        for i, l in enumerate(t.split('\n')):
            if l.startswith('## '):
                在 = '六' if l.startswith('## 六') else ('八' if l.startswith('## 八') else None)
                有.add(在)
                continue
            if 在 == '六' and l.startswith('|'):
                c = [x.strip() for x in l.strip().strip('|').split('|')]
                if len(c) >= 4 and '待执' in c[3]:
                    六 += 1
                    for n in _章引(c[1] + ' ' + c[2], 末, 2) or [0]:
                        漏.append((n, '待执', '悬线六#%s %s' % (c[0], _短(c[1], 40)), '`%s:%d`' % (p, i + 1), 1))
            elif 在 == '八' and re.match(r'^\d+\.\s', l):
                八 += 1
                文 = re.sub(r'^\d+\.\s*', '', l)                     # 序号「1.」—「8.」⛔作章号；「**水**：141」之签冒号後之数是章
                for n in _章引(re.sub(r'^\*\*[^*]{1,12}\*\*\s*[：:]\s*', '', 文), 末, 2) or [0]:
                    漏.append((n, '情理之疑', '悬线八 %s' % _短(文, 40), '`%s:%d`' % (p, i + 1), 1))
        坏 = [k for k, v in (('六', 六), ('八', 八)) if k not in 有 or not v]
        鲜.append(('悬线.md 六／八', '', '六待执 %d、八之疑 %d' % (六, 八),
                   ('⚠ %s 节不得或解出 0（⛔静读 0）' % '、'.join(坏)) if 坏 else '✓'))
    for 至, 档, 行们 in ctx.get('大审', []):
        for 章, 类, 判, 限, 行, 号 in 行们:
            if 类 in ('判不治', '半治'):
                漏.append((章, 类, '%s %s' % (_审号(ctx['器'], 至, 号), 判), '`%s:%d`' % (档, 行), 1))
    for 章, 至, 号, 限, 源, y in ctx.get('诸挂', []):          # 已挂：取 ②同一之诸挂（末册＋旧笔之隙＋限非数·判者⑤b）
        漏.append((章, '已挂', '%s %s〔%s〕' % (_审号(ctx['器'], 至, 号), y['欠何'].split(' ', 2)[-1], y['态']), 源, 1))
        升.append((章, '大审已挂', '%s 限%s〔%s%s〕%s' % (_审号(ctx['器'], 至, 号), 限 if 限 is not None else '—', y['态'], ('·' + y['注']) if y['注'] else '',
                                                         y['欠何'].split(' ', 2)[-1]), 源, 态序.get(y['态'], 9)))
    # ── 盲读（版本/第N章/_轮记.md「## 造式·盲读」）
    无盲, 有盲, 空记, 不识盲, 无忆 = [], 0, [], [], []
    行家 = {}
    无表 = []
    诸版 = {}
    for d in glob.glob(os.path.join(root, '版本', '第*章')):
        m = re.search(r'第(\d+)章$', d)
        if m:
            诸版[int(m.group(1))] = d
    for n, d in sorted(诸版.items()):
        if n > 末:
            continue
        f = os.path.join(d, '_轮记.md')
        if os.path.exists(f):
            ms = 盲读析(_读(f))
            rel = os.path.relpath(f, root)
            if ms is None:
                if n >= 380:
                    无盲.append(n)
            elif not ms:
                不识盲.append(n)
            else:
                有盲 += 1
                for 签, 值, 行 in ms:
                    if 签 in ('读不懂处', '读错处') and not _空(值):
                        k = _读条(值)
                        意 = _有意数(值) if 签 == '读错处' else 0
                        if k - 意:
                            漏.append((n, '读不懂' if 签 == '读不懂处' else '读错', '盲读%s %d 条：%s' % (签, k - 意, _短(值, 36)), '`%s:%d`' % (rel, 行), k - 意))
                        if 意:
                            漏.append((n, '读错·有意', '盲读读错处之 %d 条自注作者有意（⛔计热）' % 意, '`%s:%d`' % (rel, 行), 意))
                忆 = [(值, 行) for 签, 值, 行 in ms if 签 == '最记得']
                if not 忆:
                    无忆.append(n)
                elif any(_空(v) for v, _ in 忆):
                    空记.append(n)
                    升.append((n, '最记得空', '盲读「最记得」空', '`%s:%d`' % (rel, next(r for v, r in 忆 if _空(v))), None))
        elif n >= 380:
            无盲.append(n)
        f = os.path.join(d, '_行家评.md')
        if os.path.exists(f):
            r = 行家评析(_读(f))
            if r:
                r['档'] = os.path.relpath(f, root)
                行家[n] = r
            else:
                无表.append(n)
    鲜.append(('盲读 `版本/第N章/_轮记.md`「## 造式·盲读」', '%d 章可析' % 有盲, '「最记得」空 %d 章' % len(空记),
               '；'.join(x for x in (('380 起无此节者 %s' % _合(无盲)) if 无盲 else '',
                                     ('节在而签俱不识者 %s' % _合(不识盲)) if 不识盲 else '',
                                     ('无「最记得」之签者 %s' % _合(无忆)) if 无忆 else '') if x) or '✓'))
    鲜.append(('行家评 `版本/第N章/_行家评.md`', '%d 份' % (len(行家) + len(无表)), '十维之表可析 %d' % len(行家),
               ('无表（或末栏非计／合／均／加权、或胜稿不在表）者 %d 份：%s——⛔猜分' % (len(无表), _合(无表))) if 无表 else '✓'))
    # 行家胜稿之分低：可析者之末四分之一
    序 = sorted(行家.items(), key=lambda kv: (kv[1]['十分'], kv[0]))
    低 = 序[:(len(序) + 3) // 4]
    for n, r in 低:
        升.append((n, '行家低', '胜稿%s %s %s（折 %.2f／10）' % (r['胜'], r['栏'], ('%g' % r['计']), r['十分']), '`%s:%d`' % (r['档'], r['行']), r['十分']))
    # 拍库低分：诸拍之均在有分之章之末四分之一
    均 = sorted(((round(sum(c['亮']) / len(c['亮']), 2), n) for n, c in ctx['章'].items() if c['亮']))
    for v, n in 均[:(len(均) + 3) // 4]:
        c = ctx['章'][n]
        行 = next((i + 1 for i, l in enumerate(c['文'].split('\n')) if l.startswith('## 亮点')), 0)
        升.append((n, '拍库低', '亮点诸拍之均 %.2f（%d 拍）' % (v, len(c['亮'])), '`%s:%d`' % (c['档'], 行), v))
    # 二稿账
    p = os.path.join('设定', '二稿账.md')
    t = _读(os.path.join(root, p))
    if t is None:
        缺.append(('二稿账', '不在'))
    else:
        病们, (先, 先行), 况 = 二稿账析(t, 末, lambda n: 白文之(root, ctx['器'], n))
        for n, 段, 病, 改, 行, 施 in 病们:
            if 施 is True:
                漏.append((n, '二稿病·似已施', '二稿账 [%s] %s（改法已见於白文·未划·⛔计热）' % (段, _短(病, 30)), '`%s:%d`' % (p, 行), 1))
                continue
            漏.append((n, '二稿病', '二稿账 [%s] %s%s' % (段, _短(病, 40), '（半施·待核：引号之改已见於白文，拆段／另起诸令未见·⛔划）' if 施 == '半' else ''),
                      '`%s:%d`' % (p, 行), 1))
            if 改:
                升.append((n, '二稿改法', '[%s] %s → %s' % (段, _短(病, 24), _短(改, 40)), '`%s:%d`' % (p, 行), None))
        for n in 先:
            升.append((n, '先审', '二稿先审之章（执笔席失败·稿数不足）', '`%s:%s`' % (p, 先行), None))
        for a, b in 况['重造']:                              # 二稿之法「局烂即造」：章段之升（⛔计入一章·判者⑤a）
            升.append((0, '重造', '重造 %s（二稿之法·局烂即造）' % ('%d—%d' % (a, b) if a != b else a), '`%s:%s`' % (p, 况['重造行']), -(b - a + 1)))
        施数 = len([1 for x in 病们 if x[5] is True])
        半们 = [x for x in 病们 if x[5] == '半']
        ctx.setdefault('计', {})['二稿似已施'] = 施数
        鲜.append(('二稿账 `%s`' % p, '', '未划之病 %d（无章之条 %d、似已施 %d）；先审 %d 章（:%s）；重造 %s' % (
            len(病们), 况['全书'], 施数, len(先), 先行, _合(sum([list(range(a, b + 1)) for a, b in 况['重造']], [])) or '—'),
                   '；'.join(z for z in (
                       ('⚠「## 病」之节不得（档有「- [」之行 %d）——⛔静读 0' % 况['条行']) if not 况['节'] and 况['条行'] else '',
                       ('⚠ 解出 0 条而档有「- [」之行 %d' % 况['条行']) if 况['节'] and not 病们 and 况['条行'] else '',
                       ('⚠ 似已施而未划 %d 条（%s）——由二稿账之写者核而划之' % (施数, '、'.join(':%d' % x[4] for x in 病们 if x[5] is True))) if 施数 else '',
                       ('半施 %d 条（%s：引号之改已见，拆段／另起诸令待施——照计热，⛔划）' % (len(半们), '、'.join(':%d' % x[4] for x in 半们))) if 半们 else '',
                       '' if 先行 else '⚠ 先审之行不得') if z) or '✓'))
    ctx['行家'] = 行家
    return 漏, 升


def 热(漏, 家=None):
    """→ {章: 热}（权 0 之条⛔入；家：只计其类，如 旧账家／读审家）。"""
    出 = {}
    for n, 类, _, _, k in 漏:
        if 权[类] and (家 is None or 类 in 家):
            出[n] = 出.get(n, 0) + 权[类] * (k or 1)
    return 出


# ════ 表 ════
def _表(头, 行们):
    return ['| ' + ' | '.join(头) + ' |', '|' + '---|' * len(头)] + ['| ' + ' | '.join(str(x) for x in r) + ' |' for r in 行们]


def _环行(x, 全=False):
    """②表与附②之行；全＝附②：欠何、宜文⛔截（判者⑩c）。软源之末见只是其行所引（书「引」），⛔计久默。"""
    限宜 = ('限 %d' % x['限']) if x['限'] is not None else (('宜於 %d' % x['宜']) if x['宜'] is not None else ('宜於 %s' % (x['宜文'] or '未钉')))
    if x['宜文'] and x['宜'] is not None:
        限宜 += '（%s）' % (_短(x['宜文'], 10 ** 4) if 全 else _短(x['宜文'], 40))
    见 = '—' if x['末见'] is None else (('引 %s' % x['末见']) if x.get('软') else x['末见'])
    return [x['态'] + ('·' + x['注'] if x['注'] else ''), x['类'], x['开於'], _短(x['欠何'], 10 ** 4 if 全 else 60), 限宜,
            见, x['默'] if x['默'] is not None else '—', x['源']]


# ════ 生 ════
读法 = {
    '态': '> 态：**逾限**＝末章已封而限 ≤ 末章（限＝末章者注「当章已封·待核」）｜**将到**＝限或宜於在末章後 1—%d 章｜'
          '**疑未收**＝段案跨段之埋，其收章已写而段案与详记俱无其收（待核）｜**待裁**＝挂事未到其站、大审「已挂」限非数｜'
          '**久默**＝硬源之末见至今逾 %d 章｜**常**。「限」＝账之到期章（硬）；「宜於」＝记席之估、段案之钉、余章总案之链、表行之引'
          '（软，⛔逾限：过者注「过宜 N」、宜＝末章注「末章当收·待核」；「→N 以後」作开放之宜，⛔钉 N）。'
          '末见：到期账取其诸章之栏与记忆提其号之末、FS 取记忆提其号之末（并大问表同词之末见）、大问表·悬念哨取其器之实数；'
          '软源（末章悬线、段案、站之欠、大悬）之末见书「引 N」＝其行所引之章，⛔计久默。'
          '大审已挂：诸册之「已挂」而无人收（`大审.诸挂`）——末册照常，前诸册「旧笔不及」者（限 > 其下一册之至：下一册之旧笔未到限、再下一册只读上一册）亦出。'
          '末章悬线：每线每镜各取其末章（主｜暗·她｜暗·霍钧｜暗·黎东来；末一段以前止笔之镜⛔取）。' % (将到, 久默),
    '热': '> 漏之热＝记录者读时所见×%d／条（书「已改」「不改／判不治」者⛔计）＋悬线六待执×%d＋悬线八之疑×%d＋大审判不治×%d、半治×%d、已挂（诸挂）×%d'
          '＋盲读读不懂×%d／条、读错×%d／条（自注「作者有意让我先错」者⛔计；计於其轮记之章）＋二稿账未划之病×%d（段者计於其首章；改法已见於白文者⛔计·⓪报）。'
          '二家：旧账家（记录者、待执、疑·11 章起）与读审家（盲读、大审、二稿·380 章起）起章不同，各列其最热，⛔混排。'
          % (权['记录者'], 权['待执'], 权['情理之疑'], 权['判不治'], 权['半治'], 权['已挂'], 权['读不懂'], 权['读错'], 权['二稿病']),
    '升': '> 升之计（定序：重造＞大审已挂＞先审＞行家低＞拍库低＞最记得空＞二稿改法）：二稿之法「局烂即造」之章段（⛔计入一章）、'
          '大审「已挂」而未收（逾限者先）、二稿先审之章、行家胜稿之分（十维之合折作十分）在可析者之末四分之一、'
          '亮点诸拍之均在有分者之末四分之一（「大进N」之序号⛔作分）、盲读「最记得」空、二稿账有其改法（似已施者⛔列）——各计一。'}


def _计环(环们):
    """→ (计态 {态: 数}, 计源 {源类: 数})——②与一眼同用（⛔两算）。"""
    计态 = {k: len([x for x in 环们 if x['态'] == k]) for k in 态序}
    计源 = {}
    for x in 环们:
        计源[x['类']] = 计源.get(x['类'], 0) + 1
    return 计态, 计源


def _源计文(计源):
    return '、'.join('%s %d' % (k, 计源[k]) for k in sorted(计源, key=lambda k: 源序.get(k, 9)))


def _热序(热们):
    """→ [(章, 热)]：热降、章升；全书或跨站之条（章 0）⛔入。"""
    return sorted(((n, h) for n, h in 热们.items() if n), key=lambda kv: (-kv[1], kv[0]))


def _由(漏, n, 家=None):
    """一章之热由 → [(类, 条)]，按其所贡之热降（权 0 之类⛔入）。"""
    由 = {}
    for m, 类, _, _, k in 漏:
        if m == n and 权[类] and (家 is None or 类 in 家):
            由[类] = 由.get(类, 0) + (k or 1)
    return sorted(由.items(), key=lambda kv: -权[kv[0]] * kv[1])


def _升低(升, 类):
    return sorted([x for x in 升 if x[1] == 类], key=lambda x: (x[4] if x[4] is not None else 0, x[0]))


def _首句(s, k=60):
    return _短(re.split(r'[。；]', re.sub(r'\*\*', '', s or ''))[0], k)


def 脊之片(ctx):
    """→ [(a, b, 站题, 站事, 事源, [(x, y, 弧, 详)])]——①之表、图首「一眼」、--章 同用（⛔另算）。站取 剧情链.站们；
    站事取总览②「此站之事」，缺者（E6—E8）合其诸段段案之「骨」（无骨取段案之题）代之，事源书「段案之骨」；
    章段：381 以前取 用法.md §四之块（其弧：总览②「分段」同起止之片先，无则块名），381 起取 段料.段首（弧取段案之题与「重」之数；
    详＝{'骨','弧','重':[(章, 一句)], '档'}：段之势之「骨」「弧」两行全文、重章之一句——判者①a⑦）；未盖之章标〔未分块〕。"""
    末, 段首, 出 = ctx['末'], ctx['段首'], []
    for a, b, 题 in ctx['站']:
        站码 = re.match(r'(E\d+)', 题)
        站事 = ctx['站文'].get(站码.group(1), {}).get('事', '') if 站码 else ''
        事源 = '总览②' if 站事 else ''
        片 = []
        for x, y, 名 in ctx['块']:
            x2, y2 = max(x, a), min(y, b, 380)
            if x2 <= y2 and (x2, y2) not in [(p, q) for p, q, *_ in 片]:
                片.append((x2, y2, ctx['分段'].get((x, y)) or 名, {}))
        n = a
        while n <= b and n <= 末:
            if n >= 381 and 段首:
                s = max(段首(n), a)
                e = max(min(段首(n) + 9, b, 末), n)          # ⛔死循环：段首之义若变，e 至少为 n（细⑨）
                诸 = [d for d in ctx['段案'] if d['a'] <= e and d['b'] >= s]
                弧 = '／'.join(_短(d['题'], 30) for d in 诸 if d['题'])
                重 = {}
                for d in 诸:
                    for 章n, v in d['节'].items():
                        if s <= 章n <= e and d['a'] <= 章n <= d['b'] and v.get('重'):
                            重[章n] = v['重']
                详 = {'骨': '／'.join(d['骨'] for d in 诸 if d['骨']), '弧': '／'.join(d['弧'] for d in 诸 if d['弧']),
                      '题': [d['题'] for d in 诸 if d['题'] and d['a'] >= a and d['b'] <= b],
                      '重': [(k, 一句(ctx['索'].get(k, ('', '', '', 0))[2]) or ctx['章'].get(k, {}).get('要', ''))
                             for k in sorted(重) if 重[k] == '重' and k <= 末],
                      '档': '、'.join(d['档'] for d in 诸)}
                片.append((s, e, ('段 ' + (弧 or '（无段案）')) + (('｜重%d·中%d·轻%d' % tuple(list(重.values()).count(w) for w in '重中轻')) if 重 else ''), 详))
                n = e + 1
            else:
                n += 1
        去重, 片2 = set(), []
        for x in sorted(片, key=lambda z: (z[0], z[1], z[2])):
            if (x[0], x[1], x[2]) not in 去重:
                去重.add((x[0], x[1], x[2]))
                片2.append(x)
        片 = 片2
        盖 = set(k for x, y, *_ in 片 for k in range(x, y + 1))
        未 = [k for k in range(a, min(b, 末) + 1) if k not in 盖]
        for 段文 in _合(未).split('、') if 未 else []:
            x, _, y = 段文.partition('—')
            片.append((int(x), int(y or x), '〔未分块〕', {}))
        片.sort(key=lambda z: (z[0], z[1]))
        if not 站事:                                       # 站事缺（E6—E8）：诸段之骨（首句）先，无骨取其站内整段之题（去「E7 」「造式二代」）
            骨们 = [_首句(z[3]['骨'], 30) for z in 片 if z[3].get('骨')]
            题们 = [_短(re.sub(r'^E\d+\s*|[·、；]?造式二代.*$', '', w), 24) for z in 片 if z[3] for w in z[3].get('题', [])]
            站事 = '／'.join(dict.fromkeys(x for x in (骨们 or 题们) if x))
            事源 = ('段案之骨' if 骨们 else '段案之题') if 站事 else ''
        出.append((a, b, 题, 站事, 事源, 片))
    return 出


一眼之限 = (20, 4200)   # 图首「一眼」之行数（题、空行在内）与字数之上限——短而全：逾则自测红（判者议：宽至约二十行）
一眼之列 = 6            # 逾限、硬限将到、久默之硬限：每行至多列几条（余书其数、指②）


def _态计文(计态):
    return '｜'.join('%s %d' % (k, 计态[k]) for k in 态序 if 计态.get(k) or k in ('逾限', '将到', '久默', '常'))


def _病序(ctx):
    """⓪之病 → [(伤判否, 源名, 首句)]：伤判断者先（大审旧笔之隙、悬线 宜於旧／节旧、二稿账似已施、总览站事缺、段案疑未收、FS 不合）。"""
    伤式 = re.compile(r'旧笔之隙|宜於与余章总案|节旧|似已施|无「此站之事」|FS 限|疑未收|节不得|解出 0')
    出 = []
    for 源, _, _, d in ctx['鲜']:
        if d == '✓':
            continue
        名 = re.split(r'[\s`（(]', 源)[0]
        for 片 in re.split(r'[；;]', d):
            片 = 片.strip()
            if not 片 or re.match(r'^(?:记录者读时所见|无此行者)', 片):      # 记录者之计係数、非病
                continue
            出.append((not 伤式.search(片), 名, _短(re.sub(r'[（(][^（）()]*[）)]', '', 片), 34)))
    出.sort(key=lambda x: x[0])
    return 出


def 一眼(ctx, 片们):
    """图首（1119 作者令「一眼就能了解所有从头到尾的剧情……一眼就定位到哪个地方的剧情有问题……还有可以升级的空间」）：
    短而全——书至何处、全书之脊（每站一句）、今站之弧、未闭之环（逾限俱列、将到之硬限俱列而软者计其章、待核者计之、久默之硬限俱列）、
    漏之最热（旧账家、读审家分列）、可升之最要（照定序：重造＞大审已挂＞先审＞行家低＞拍库低＞二稿改法）、末章之悬（诸镜）、源之病（伤判者先）
    ——每行指其详节。其数俱取①—⑤同一之算（_计环／_热序／_由／_升低／脊之片），⛔另算。"""
    末, 环们, 漏, 升 = ctx['末'], ctx['环们'], ctx['漏'], ctx['升']
    名, 线, 句, _ = ctx['索'].get(末, ('', '', '', 0))
    句 = 一句(句) if 句 else ctx['章'].get(末, {}).get('要', '')
    出 = ['## 一眼', '']
    出.append('- **书至**：第 %d 章《%s》（%s）——%s' % (末, 名 or '？', _短(线, 26), _短(句, 60) or '（无一句）'))
    出.append('- **脊**（①·每站一句）：' + '｜'.join('%s %d—%d〔%s〕' % (_短(题, 14), a, b, _首句(事, 22) or '—')
                                               for a, b, 题, 事, _, _ in 片们))
    今 = next(((a, b, 题, 片) for a, b, 题, _, _, 片 in 片们 if a <= 末 <= b), None)
    if 今:
        a, b, 题, 片 = 今
        码 = 题.split()[0]
        弧们 = []
        for x, y, w, 详 in 片:
            题弧 = re.sub(r'^段 (?:%s\s+(?!之))?' % re.escape(码), '', re.sub(r'｜重\d+·中\d+·轻\d+$', '', w))
            弧们.append(('%d—%d' % (x, y) if x != y else str(x), _首句(详.get('骨'), 30) if 详.get('骨') else _短(题弧, 30)))
        出.append('- **今站 %s**（%d—%d）之弧：%s' % (码, a, b, '｜'.join('%s %s' % kv for kv in 弧们)))
    计态, 计源 = _计环(环们)
    出.append('- **未闭之环 %d**（②）：%s——按源 %s' % (len(环们), _态计文(计态), _源计文(计源)))

    def 条(x, k=22):
        return '%s〔%s·%s%s〕' % (_短(x['欠何'], k), ('限 %d' % x['限']) if x['限'] is not None else
                                 (('宜於 %d' % x['宜']) if x['宜'] is not None else '未钉'), x['类'],
                                 ('·' + _短(x['注'], 18)) if x['注'] else '')

    def 列(xs, f):
        return '；'.join(f(x) for x in xs[:一眼之列]) + (('；余 %d 见②' % (len(xs) - 一眼之列)) if len(xs) > 一眼之列 else '')
    逾 = [x for x in 环们 if x['态'] == '逾限']
    if 逾:
        出.append('- **逾限 %d**（末章已封·限 ≤%d）：%s' % (len(逾), 末, 列(逾, 条)))
    到 = [x for x in 环们 if x['态'] == '将到']
    if 到:
        硬 = sorted([x for x in 到 if x['限'] is not None], key=lambda x: (x['限'], 源序.get(x['类'], 9)))
        软 = {}
        for x in 到:
            if x['限'] is None:
                软[x['宜']] = 软.get(x['宜'], 0) + 1
        出.append('- **将到 %d**（%d—%d 章）：硬限 %d%s｜宜於（软）%d%s' % (
            len(到), 末 + 1, 末 + 将到, len(硬), ('——' + 列(硬, 条)) if 硬 else '', sum(软.values()),
            ('——' + '、'.join('%d 章 %d' % kv for kv in sorted(软.items()))) if 软 else ''))
    当收 = [x for x in 环们 if x['限'] is None and x['宜'] == 末]
    疑 = [x for x in 环们 if x['态'] == '疑未收']
    裁 = [x for x in 环们 if x['态'] == '待裁']
    if 当收 or 疑 or 裁:
        裁计 = {}
        for x in 裁:
            k = re.match(r'(大审\d+|\S+?)(?:\s|（|：|$)', x['欠何'])
            裁计[k.group(1) if k else x['类']] = 裁计.get(k.group(1) if k else x['类'], 0) + 1
        出.append('- **待核**：末章当收 %d（宜於 %d 之软环·%d 已封：已收否待核）｜疑未收 %d（段案·收章已写而段案与记忆俱无其收）｜待裁 %d（%s）' % (
            len(当收), 末, 末, len(疑), len(裁), '、'.join('%s %d' % kv for kv in sorted(裁计.items())) or '—'))
    默 = sorted([x for x in 环们 if x['态'] == '久默'], key=lambda x: -(x['默'] or 0))
    if 默:
        出.append('- **久默 %d**（硬源·末见至今逾 %d 章；软源⛔计）：%s' % (len(默), 久默, 列(默, lambda x: '%s〔默 %s·%s%s〕' % (
            _短(x['欠何'], 18), x['默'], ('限 %d' % x['限']) if x['限'] is not None else '无限', ('·' + _短(x['注'], 12)) if x['注'] else ''))))
    家们 = []
    for 名_, 家 in (('旧账家', 旧账家), ('读审家', 读审家)):
        序 = _热序(热(漏, 家))[:5]
        if 序:
            家们.append('%s %s' % (名_, '、'.join('%d《%s》%d（%s）' % (n, _短(ctx['索'].get(n, ('',))[0], 6), h,
                                                                   '、'.join('%s×%d' % kv for kv in _由(漏, n, 家)[:2])) for n, h in 序)))
    if 家们:
        出.append('- **漏之最热五章**（③·二家分列：旧账家＝记录者、待执、疑〔11 起〕；读审家＝盲读、大审、二稿〔380 起〕）：' + '｜'.join(家们))
    片升 = []
    for 类 in 升序:
        xs = _升低(升, 类)
        if not xs:
            continue
        if 类 == '重造':
            片升.append('重造 ' + '、'.join(re.sub(r'^重造 |（.*$', '', x[2]) for x in xs[:3]))
        elif 类 == '先审':
            片升.append('先审 ' + _合(sorted(set(x[0] for x in xs))))
        elif 类 == '大审已挂':
            片升.append('大审已挂 %d（%s）' % (len(xs), '、'.join(' '.join(x[2].split(' ')[:2]) for x in xs[:3])))
        elif 类 in ('行家低', '拍库低'):
            片升.append('%s %s' % ({'行家低': '行家胜稿最低', '拍库低': '拍库最低'}[类], '、'.join('%d（%.2f）' % (x[0], x[4]) for x in xs[:3])))
        else:
            片升.append('%s %d' % (类, len(xs)))
    出.append('- **可升之最要**（④·定序·各列其首三；共 %d 条）：%s' % (len(升), '｜'.join(片升)))
    计 = ctx.get('计', {})
    if 计.get('大问已还') or 计.get('到期已清') or 计.get('FS已销'):
        出.append('- **已结之大环**：大问表已还 %s｜到期账已清 %s 条｜canon FS 已销 %s（未闭者见②）' % (
            '、'.join('%s %d' % kv for kv in 计.get('大问已还', [])) or '—', 计.get('到期已清', '—'), 计.get('FS已销', '—')))
    末悬 = [x for x in 环们 if x['类'] == '末章悬线']
    线末 = ctx.get('线末') or {}
    出.append('- **末章之悬**：%s 之「## 悬线」入账 %d（欠 %d、开 %d；将到 %d）｜大悬（悬线.md 一）%d 行｜全书未闭 %d 环' % (
        '、'.join('%s %d' % (k, v) for k, v in sorted(线末.items(), key=lambda kv: kv[1])) or '末章',
        len(末悬), len([x for x in 末悬 if x['欠何'].startswith('〔欠〕')]), len([x for x in 末悬 if x['欠何'].startswith('〔开〕')]),
        len([x for x in 末悬 if x['态'] == '将到']), 计源.get('大悬', 0), len(环们)))
    病 = _病序(ctx)
    出.append('- **源之病**（⓪·伤判者先）：%s；缺／败 %d' % ('｜'.join('%s：%s' % (名_, d) for _, 名_, d in 病[:6]) + (('｜余 %d 见⓪' % (len(病) - 6)) if len(病) > 6 else '')
                                                     if 病 else '无', len(ctx['缺'])))
    出.append('')
    return 出


def 生(root=ROOT, 器=None):
    t0 = time.time()
    ctx = 料(root, 器)
    末 = ctx['末']
    环们 = 诸环(ctx)
    漏, 升 = 诸漏诸升(ctx)
    热们 = 热(漏)
    升数 = {}
    for n, *_ in 升:
        if n:
            升数[n] = 升数.get(n, 0) + 1
    开数 = {}
    for x in 环们:
        k = x['开於'] if isinstance(x['开於'], int) else (int(re.match(r'\d+', x['开於']).group(0)) if re.match(r'\d+', str(x['开於'])) else None)
        if k:
            开数[k] = 开数.get(k, 0) + 1
    ctx.update({'环们': 环们, '漏': 漏, '升': 升, '热': 热们, '升数': 升数})
    片们 = 脊之片(ctx)
    出 = ['# 剧情全图（至第 %d 章）' % 末, '',
         '> 零 token 所并（`工具/剧情全图.py`；封版 --後 於「剧情链」之後重生·写者唯一：唯封版之步——总编辑之坐⛔重跑提交，'
         '诸源封版之外改者下一封版随）。只并既有之源、只算章之差——⛔改正文、⛔改账之判；每条带源（档:行），错在源则改源。'
         '何时读：二稿、大审、开段之前先读「一眼」；一章之全：`--章 N`；一线之迹：`--线 <词>`；旧否：`--验`。'
         '诸数之读法（态、热、升之计）各书於其节之首。', '']
    出 += 一眼(ctx, 片们)                                 # 图首：短而全（其数俱取下诸节同一之算，⛔另算）
    # ⓪
    出 += ['## ⓪ 源之鲜', '']
    出 += _表(['源', '所至', '数', '鲜否·病'], [[a, b, c, d] for a, b, c, d in ctx['鲜']])
    if ctx['缺']:
        出 += ['', '**缺／败（%d）**：' % len(ctx['缺'])] + ['- %s：%s' % (a, b) for a, b in ctx['缺']]
    出.append('')
    # ①
    出 += ['## ① 一页之脊（站—段—章段）', '',
           '> 站取 `剧情链.站们`（总览②；站事取「此站之事」，缺者合段案之骨代之而注「段案之骨」）；章段：381 以前取 `用法.md` §四之块，'
           '381 起取段（`段料.段首`·十章一段，弧取段案之题；其下二行：段之势之「弧」（≤120 字）、「重」章之一句（≤40 字）——全文 `--章 N`）。'
           '环＝②开环之开於其中者；漏＝③热之和；升＝④条数。', '']
    脊 = []
    for a, b, 题, 站事, 事源, 片 in 片们:
        首 = True
        for x, y, 名, 详 in 片:
            环n = sum(v for k, v in 开数.items() if x <= k <= y)
            热n = sum(v for k, v in 热们.items() if x <= k <= y)
            升n = sum(v for k, v in 升数.items() if x <= k <= y)
            脊.append(['**%s**（%d—%d）%s' % (题, a, b, ('：' + _短(站事, 40) + ('〔%s〕' % 事源 if 事源 != '总览②' else '')) if 站事 else '') if 首 else '',
                       '%d—%d' % (x, y) if x != y else str(x), _短(名, 56), 环n or '', 热n or '', 升n or ''])
            首 = False
            if 详.get('弧') or 详.get('骨'):
                脊.append(['', '', '弧：' + _短(详.get('弧') or 详.get('骨'), 120), '', '', ''])
            if 详.get('重'):
                脊.append(['', '', '重：' + '；'.join('%d %s' % (k, _短(w, 40)) for k, w in 详['重']), '', '', ''])
    出 += _表(['站', '章段', '弧', '环', '漏', '升'], 脊) + ['']
    # ②
    计态, 计源 = _计环(环们)
    出 += ['## ② 开环之账（未闭之环）', '', 读法['态'], '',
           '**数**：共 %d 环——%s。按源：%s。' % (len(环们), _态计文(计态), _源计文(计源)), '']
    要 = [x for x in 环们 if x['态'] == '逾限'][:30] + [x for x in 环们 if x['态'] == '将到'][:24]
    要 += [x for x in 环们 if x['态'] in ('疑未收', '待裁')][:12]
    要 += [x for x in 环们 if x['态'] == '久默'][:8]
    出 += _表(['态', '源类', '开於', '欠何', '限／宜於', '末见', '默', '源'], [_环行(x) for x in 要])
    出 += ['', '余 %d 环见档末「附② 开环全账」。' % (len(环们) - len(要)), '']
    # ③
    计类 = {}
    for n, 类, _, _, k in 漏:
        计类[类] = 计类.get(类, 0) + (k or 1)
    热序 = _热序(热们)
    出 += ['## ③ 漏之位（按章聚热）', '', 读法['热'], '',
           '**数**：%d 条源、%d 章有热（热和 %d）。按类：%s。' % (len(漏), len([k for k in 热们 if k]), sum(热们.values()),
                                                     '、'.join('%s %d' % (k, 计类[k]) for k in 权 if k in 计类)), '']
    for 名_, 家 in (('旧账家（记录者、待执、情理之疑·11 章起）', 旧账家), ('读审家（盲读、大审、二稿账·380 章起）', 读审家)):
        rows = []
        for n, h in _热序(热(漏, 家))[:10]:
            首源 = next(源 for m, 类, _, 源, _ in 漏 if m == n and 类 in 家)
            rows.append([n, _短(ctx['索'].get(n, ('',))[0], 10), h, '、'.join('%s×%d' % kv for kv in _由(漏, n, 家)), 首源])
        出 += ['**%s之最热**（⛔与他家混排）：' % 名_, ''] + _表(['章', '名', '热', '其由（类×条）', '首源'], rows) + ['']
    出 += ['', '热之前 40 章之诸条见档末「附③」；他章之条：`--章 N`。', '']
    # ④
    计升 = {}
    for _, 类, *_ in 升:
        计升[类] = 计升.get(类, 0) + 1
    出 += ['## ④ 可升之位', '', 读法['升'], '',
           '**数**（定序）：%s。' % '、'.join('%s %d' % (k, 计升.get(k, 0)) for k in 升序), '']
    造 = _升低(升, '重造')
    if 造:
        出.append('- **重造**（%s）：%s' % (造[0][3], '、'.join(re.sub(r'^重造 |（.*$', '', x[2]) for x in 造)))
    挂们 = _升低(升, '大审已挂')
    if 挂们:
        出.append('- **大审已挂而未收**（%d；逾限者先）：' % len(挂们) + '；'.join('%s〔%s〕' % (_短(x[2], 70), x[3]) for x in 挂们[:6])
                  + ('；余 %d 见附④' % (len(挂们) - 6) if len(挂们) > 6 else ''))
    先 = sorted(set(n for n, 类, *_ in 升 if 类 == '先审'))
    if 先:
        出.append('- **二稿先审之章**（%s）：%s' % (next(s for n, 类, _, s, _ in 升 if 类 == '先审'), '、'.join(map(str, 先))))
    低 = _升低(升, '行家低')[:8]
    if 低:
        出.append('- **行家胜稿之分最低**：' + '；'.join('%d（%.2f·%s）' % (n, v, 源) for n, _, _, 源, v in 低))
    拍 = _升低(升, '拍库低')[:8]
    if 拍:
        出.append('- **亮点诸拍之均最低**：' + '；'.join('%d（%.2f）' % (n, v) for n, _, _, _, v in 拍))
    空 = sorted(n for n, 类, *_ in 升 if 类 == '最记得空')
    出.append('- **盲读「最记得」空**：%s' % (_合(空) if 空 else '无（可析之盲读俱有其所记）'))
    改 = [x for x in 升 if x[1] == '二稿改法']
    if 改:
        出.append('- **二稿账之改法**（%d 条；前五）：' % len(改) + '；'.join('%s（%s）' % (文, 源) for n, _, 文, 源, _ in 改[:5]))
    出 += ['', '全条见档末「附④」。', '']
    # ⑤
    出 += ['## ⑤ 逐章一行', '', '> 名、线·日、一句取总览③（一句去其冠、截六十字；无行者取详记「一句之要」）；开＝本章悬线之开条；'
           '收＝结／收／兑之条（旧式之章只记「接」者书「接N」）；漏＝③之热；升＝④之条。', '']
    rows = []
    for n in sorted(ctx['章']):
        c = ctx['章'][n]
        名, 线, 句, _ = ctx['索'].get(n, ('', '', '', 0))
        句 = 一句(句) if 句 else c['要']
        收n = len(c['悬']['收'])
        rows.append([n, _短(名, 12), _短(线, 22), _短(句, 60), len(c['悬']['开']) or '',
                     收n if 收n else (('接%d' % len(c['悬']['接'])) if c['悬']['接'] else ''), 热们.get(n, '') or '', 升数.get(n, '') or ''])
    出 += _表(['N', '名', '线·日', '一句', '开', '收', '漏', '升'], rows) + ['']
    # 附
    出 += ['## 附② 开环全账（%d）' % len(环们), '']
    出 += _表(['态', '源类', '开於', '欠何', '限／宜於', '末见', '默', '源'], [_环行(x) for x in 环们]) + ['']
    出 += ['## 附③ 漏之诸条（热之前 40 章）', '']
    for n, h in 热序[:40]:
        出.append('- **%d**（热 %d）：%s' % (n, h, '；'.join('%s〔%s〕%s' % (类, 源, 文 if 类 != '记录者' else ('%d 条' % k))
                                                         for m, 类, 文, 源, k in 漏 if m == n)))
    零 = [x for x in 漏 if not x[0]]
    if 零:
        出.append('- **（全书或跨站之条·⛔计入章热）**：' + '；'.join('%s〔%s〕%s' % (类, 源, 文) for _, 类, 文, 源, _ in 零))
    出 += ['', '## 附④ 可升之诸条（定序）', '']
    for 类 in 升序:
        xs = _升低(升, 类)
        if xs:
            出.append('- **%s**（%d）：%s' % (类, len(xs), '；'.join('%s%s〔%s〕' % (('%d ' % n) if n else '', 文 if 类 not in ('先审', '最记得空') else '', 源)
                                                                  for n, _, 文, 源, _ in xs)))
    出.append('')
    统 = {'末': 末, '环': len(环们), '态': 计态, '漏': len(漏), '升': len(升), '缺': len(ctx['缺']), '秒': round(time.time() - t0, 2)}
    ctx.update({'环们': 环们, '漏': 漏, '升': 升, '热': 热们, '升数': 升数})
    return '\n'.join(出), 统, ctx


# ════ 令：--章 --线 --验 ════
def 一章(n, root=ROOT):
    _, _, ctx = 生(root)
    if n not in ctx['章']:
        print('⛔ 第 %d 章无详记（末章 %d）' % (n, ctx['末']))
        return 1
    c = ctx['章'][n]
    名, 线, 句, 行 = ctx['索'].get(n, ('', '', '', 0))
    站 = next((t for a, b, t in ctx['站'] if a <= n <= b), '—')
    片 = next((z for a, b, _, _, _, 片们 in 脊之片(ctx) if a <= n <= b for z in 片们 if z[0] <= n <= z[1]), None)   # ⛔另算：取①同一之片（判者①c）
    段 = ('%d—%d %s' % (片[0], 片[1], re.sub(r'^段 ', '', 片[2]))) if 片 else '—'
    print('════ 剧情全图·第 %d 章《%s》════' % (n, 名))
    print('  站：%s｜段：%s｜线·日：%s' % (站, 段, 线))
    if 片 and 片[3]:
        for k in ('骨', '弧'):
            if 片[3].get(k):
                print('  段之%s：%s' % (k, 片[3][k]))
    print('  一句之要：%s' % _短(c['要'], 400))
    print('  悬线：开 %d｜接 %d｜收 %d｜欠 %d；漏之热 %s；升 %s' % (len(c['悬']['开']), len(c['悬']['接']), len(c['悬']['收']), len(c['悬']['欠']),
                                                        ctx['热'].get(n, 0), ctx['升数'].get(n, 0)))
    for 类 in ('开', '欠'):                               # 逐条印本章之开与欠（判者⑧：⛔只印数）
        for 条, _ in c['悬'][类]:
            print('    %s：%s' % (类, _短(条, 60)))
    xs = [x for x in ctx['环们'] if n in (x['开於'], x['末见'], x['限'], x['宜'])]
    print('  ── 开环（开於／末见／限／宜於 落本章）%d ──' % len(xs))
    for x in xs:
        print('   ', '｜'.join(str(v) for v in _环行(x)))
    print('  ── 漏（权 0 者：已裁不改、作者有意、似已施——⛔计热）──')
    for m, 类, 文, 源, k in ctx['漏']:
        if m == n:
            print('    %s×%d %s〔%s〕' % (类, k or 1, 文, 源))
    print('  ── 升 ──')
    for m, 类, 文, 源, _ in ctx['升']:
        if m == n:
            print('    %s %s〔%s〕' % (类, 文, 源))
    print('  ── 诸源 ──')
    链 = [c['档'], '%s/总览.md:%s' % (记, 行) if 行 else '', '%s/剧情链.md（### %d）' % (记, n)]
    for f in ('_行家评.md', '_轮记.md', '_开镜卡.md'):
        p = os.path.join('版本', '第%d章' % n, f)
        if os.path.exists(os.path.join(root, p)):
            链.append(p)
    for d in ctx['段案']:
        if d['a'] <= n <= d['b']:
            链.append('%s:%s' % (d['档'], d['种行'].get(n, '')))
    print('    ' + '\n    '.join(x for x in 链 if x))
    return 0


_线之节 = ('发生了什么', '要句', '一句之要')


def 一线(词, root=ROOT):
    """一线之迹：只搜详记之「## 发生了什么」「## 要句」「## 一句之要」三节（⛔所携、物、悬线诸列——判者⑥c），另印全文所提之章数以对。"""
    _, _, ctx = 生(root)
    节之文 = ctx['器'].get('节之文')
    章们 = []
    for n, c in ctx['章'].items():
        try:
            if any(词 in (节之文(c['文'], k) or '') for k in _线之节):
                章们.append(n)
        except Exception:
            pass
    章们.sort()
    全 = sorted(n for n, c in ctx['章'].items() if 词 in c['文'])
    print('════ 剧情全图·一线之迹「%s」════' % 词)
    if not 章们:
        print('  详记三节（%s）无一章提「%s」' % ('、'.join(_线之节), 词))
    else:
        隙 = max(((b - a, a, b) for a, b in zip(章们, 章们[1:])), default=(0, 章们[0], 章们[0]))
        print('  所现之章 %d（详记三节：%s）：%s' % (len(章们), '、'.join(_线之节), _合(章们)))
        print('  首见 %d｜末见 %d（至今默 %d 章）｜最长之默 %d 章（%d→%d）' % (章们[0], 章们[-1], ctx['末'] - 章们[-1], 隙[0], 隙[1], 隙[2]))
        for a, b, t in ctx['站']:
            k = [n for n in 章们 if a <= n <= b]
            if k:
                print('    %s：%d 章' % (t, len(k)))
    print('  （详记全文提之者 %d 章——含所携、物、悬线诸列，⛔作其现）' % len(全))
    xs = [x for x in ctx['环们'] if 词 in x['欠何'] or 词 in str(x['宜文'])]
    print('  ── 开环之条 %d ──' % len(xs))
    for x in xs:
        print('   ', '｜'.join(str(v) for v in _环行(x, 全=True)))
    ys = [x for x in ctx['漏'] if 词 in x[2]] + [x for x in ctx['升'] if 词 in x[2]]
    print('  ── 漏／升之条 %d ──' % len(ys))
    for x in ys[:30]:
        print('    %d %s %s〔%s〕' % (x[0], x[1], x[2], x[3]))
    return 0


_要节 = ('## 一眼', '## ⓪', '## ①', '## ②', '## ③', '## ④', '## ⑤')


def 验(root=ROOT):
    """→ 0 同｜2 图旧（⚠：诸源封版之外常改，待下一封版随——写者唯一，⛔总编辑之坐重跑提交）｜1 不在或结构坏（⛔）。"""
    t, 统, _ = 生(root)
    p = os.path.join(root, 图档)
    旧 = _读(p)
    if 旧 == t:
        print('剧情全图·验：✓ 与诸源同（%d 环·%d 漏条·%d 升条·%.1f 秒）' % (统['环'], 统['漏'], 统['升'], 统['秒']))
        return 0
    if 旧 is None:
        print('剧情全图·验：⛔ %s 不在——封版 --後 之步重生之' % 图档)
        return 1
    缺节 = [k for k in _要节 if ('\n%s' % k) not in '\n' + 旧]
    if 缺节:
        print('剧情全图·验：⛔ 图之结构坏（缺 %s）——封版 --後 之步重生之' % '、'.join(缺节))
        return 1
    差 = [l for l in difflib.unified_diff(旧.split('\n'), t.split('\n'), lineterm='', n=0) if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    print('剧情全图·验：⚠ 图旧（差 %d 行）——诸源封版之外有改，待下一封版 --後 随（写者唯一：唯封版之步重写；总编辑之坐⛔重跑提交）' % len(差))
    for l in 差[:8]:
        print('   ' + l[:150])
    return 2


# ════ 自测（以小样之料钉诸析：标签漂移、源缺、限算……）════
def _一眼块(文):
    """图中「## 一眼」一节（至下一「## 」前，去尾之空行）。"""
    m = re.search(r'(?m)^## 一眼\n.*?(?=^## |\Z)', 文 or '', re.S)
    return m.group(0).rstrip('\n') if m else ''


def 自测():
    import tempfile, shutil
    R = []

    def 钉(名, ok):
        R.append((名, bool(ok)))
    钉('①分条：｜；分、括内⛔分', _分('甲（1｜2）｜乙；丙') == ['甲（1｜2）', '乙', '丙'])
    x = 悬线析('- **本章开**：\n  - 老头是谁（→ 5）\n  - 爷爷来历\n- **本章接**：\n  - 第2章之灯\n')
    钉('②标签漂移·1—10「本章开／本章接」＋下点', len(x['开']) == 2 and len(x['接']) == 1 and not x['未识'])
    x = 悬线析('**接**：\n- 349:5 甲→L5\n- 340:1 乙\n\n**开**：\n- **四页**→354:323\n- **甲印**：一线毛\n\n**还欠**（至本章末）：那四页；第八行\n')
    钉('③粗体「接／开／还欠（至本章末）」·点内粗体之条⛔作签', len(x['接']) == 2 and len(x['开']) == 2 and len(x['欠']) == 2 and not x['未识'])
    x = 悬线析('- 结：两张（438:39→:49）｜回水（436:81→:21）\n- 开：「这是头一个」（:115→446）｜少一个人（:133→後）\n- 欠：主者是谁；三点亮（442）\n')
    钉('④433 起无粗体「- 结：／- 开：／- 欠：」', len(x['收']) == 2 and len(x['开']) == 2 and len(x['欠']) == 2)
    x = 悬线析('- **欠**：那一卷（470:53→474）｜那一封（:125→485）\n- 仍挂：车之去（471:119）；PLOT-447（→485）\n- 续：一张嘴（→478）\n')
    钉('⑤欠／仍挂／续俱认', len(x['欠']) == 4 and len(x['接']) == 1)
    x = 悬线析('**接**：\n- a\n**怪签**：b\n\n**记录者读时所见（未改正文，备审）**：\n- **方位相犯**：c\n')
    钉('⑥不识之签入「未识」·记录者以下⛔入悬线', x['未识'] == ['怪签'] and len(x['接']) == 1)
    x = 悬线析('- 开：甲（:5→480）\n- 改挂：乙（→490）\n- 兑现：丙\n- 欠：丁\n')
    y = 悬线析('**接**：\n- 未钉：甲\n- 四页：乙\n')
    钉('⑥之二 433 起「- X：」式之节里不识之签（改挂、兑现）入「未识」⛔并入前签；粗体签下之「- X：」仍是条（判者·宜修⑨）',
       [t for t, _ in x['开']] == ['甲（:5→480）'] and x['未识'] == ['改挂', '兑现'] and [t for t, _ in x['欠']] == ['丁']
       and len(y['接']) == 2 and not y['未识'])
    钉('⑦记录者条数：soft-N／①②／无／下点',
       记录者析('x\n**记录者读时所见（未改正文，备审）**：soft-1 甲（:15）；soft-2 乙（:57）；soft-4 丙\n**总览席裁**：无')[1] == 3
       and 记录者析('**记录者读时所见（未改正文，备审）**：①甲；②乙\n')[1] == 2
       and 记录者析('**记录者读时所见（未改正文，备审）**：无\n')[1] == 0
       and 记录者析('**记录者读时所见（未改正文，备审）**：\n- 甲\n- 乙\n  - 乙之细\n\n**总览席裁**：无')[1] == 2
       and 记录者析('无此行')[0] is None)
    钉('⑦之二 记录者三等：已改、已裁不改⛔计热；①②为条之明标（其内之「；」⛔再分）',
       记录者析('**记录者读时所见（未改正文，备审）**：①甲——不改；後章须回治。②乙（已改）③丙：裁：改「六行」\n')[1:] == (1, 1, 1))
    钉('⑧指：开於／宜於／自引键', _指('那一卷（470:53→474）', 472)[:2] == (470, 474) and _指('那一封（:125→485）', 472) == (472, 485, '472:125')
       and _指('钱满之账（→478）', 472)[:2] == (472, 478) and _指('她找得着那一卷否（425）', 417)[1] == 425)
    钉('⑧之二「→N 以後」「→後」作开放之宜（⛔钉 N）', _指('认不认我（:95→473 以後）', 473)[1] is None and _後('认不认我（:95→473 以後）') == 473
       and _後('少一个人（:133→後）') == 0 and _後('那一卷（470:53→474）') is None and _引键('那一卷（470:53→474）', 473) == '470:53'
       and _引键('卡口之放（:107→474）', 473) == '473:107')
    钉('⑨态·限：末章已封——限≤末 逾限（限＝末「当章已封·待核」）／将到（1—3）／久默（>40）／常', 判态(473, 限=470)[0] == '逾限'
       and 判态(473, 限=476)[0] == '将到' and 判态(473, 限=477, 末见=430)[0] == '久默' and 判态(473, 限=477, 末见=440)[0] == '常'
       and 判态(473, 限=473) == ('逾限', '当章已封·待核'))
    钉('⑩态·宜於：⛔逾限、过者注「过宜」、宜＝末「末章当收·待核」⛔将到；软源⛔久默', 判态(473, 宜=460) == ('常', '过宜 13')
       and 判态(473, 宜=474)[0] == '将到' and 判态(473, 宜=473) == ('常', '末章当收·待核')
       and 判态(473, 宜=400, 末见=400)[0] == '久默' and 判态(473, 宜=400, 末见=400, 软=True)[0] == '常'
       and 环('大悬', 's', 1, 'x', 473, 末见=1)['态'] == '常' and 环('段案', 's', 1, 'x', 473, 宜=440, 末见=400, 态='疑未收')['态'] == '疑未收')
    xs = [环('段案', 's', 1, 'a', 473, 宜=500, 末见=470), 环('FS', 's', 1, 'b', 473, 限=470), 环('到期账', 's', 1, 'c', 473, 末见=1),
          环('到期账', 's', 1, 'd', 473, 限=475), 环('段案', 's', 1, 'e', 473, 宜=440, 态='疑未收'), 环('大问表', 's', 1, 'f', 473, 态='待裁')]
    钉('⑪排：逾限→将到→疑未收→待裁→久默→常', [x['态'] for x in sorted(xs, key=环序)] == ['逾限', '将到', '疑未收', '待裁', '久默', '常'])
    钉('⑪之二 亮点之分：「大进N」「大进1、2、6」之序号⛔作分（394、462 实行）', 亮点之分('- 拍5 L95—119（叫绝·行家 9／嫁大进5 後）\n'
       '- 拍6（嫁大进1、2、6）\n- 拍二（嫁·大进5、2）\n- 拍一（行家 9、9）\n') == [9.0, 9.0, 9.0])
    评 = ('## 名次\n\n**稿四 ＞ 稿五 ＞ 稿一**\n\n## 小说家之眼\n\n| 稿 | ①白描 | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | ⑩剧情（×2） | 计／110 |\n'
         '|---|---|---|---|---|---|---|---|---|---|---|---|\n| 稿五 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 99 |\n'
         '| 稿四 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 88 |\n')
    r = 行家评析(评)
    钉('⑫行家评：胜稿取名次首见、计／110 折十分', r and r['胜'] == '稿四' and r['满'] == 110 and r['十分'] == 8.0)
    r2 = 行家评析('## 名次\n一、稿一胜\n| 稿 | ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | ⑩ | 均 |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n'
                 '| 稿一 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 8.95 |\n')
    钉('⑬行家评：均（十分制）照取；无表者 None（入⓪·⛔猜分）', r2 and r2['满'] == 10 and r2['十分'] == 8.95
       and 行家评析('## 名次\n稿一胜\n\n| 稿 | 落於 | 其句 | 分 |\n|---|---|---|---|\n| 稿一 | 拍四 | 甲 | 9 |\n') is None)
    m = 盲读析('## 造式·盲读\n\n读到发生了什么「甲」｜读不懂处「1) 乙「丙」 2) 丁」｜读错处「」｜最记得「戊」｜前情之指「己」\n\n## 他\n')
    d = {k: v for k, v, _ in m}
    钉('⑭盲读·内联「」式（嵌引号）：读不懂 2 条、读错空、最记得非空', _读条(d['读不懂处']) == 2 and _空(d['读错处']) and not _空(d['最记得']))
    m = 盲读析('## 造式·盲读\n- 读不懂处：全懂\n- 读错处：1. 甲\n2. 乙\n- 最记得：\n- 前情之指：丙\n\n- **读不懂处**：全懂\n- **最记得**：丁\n')
    钉('⑮盲读·多位、点式：全懂为空、最记得空者认', [k for k, v, _ in m if not _空(v)] == ['读错处', '前情之指', '最记得']
       and _读条([v for k, v, _ in m if k == '读错处'][0]) == 2)
    m = 盲读析('## 造式·盲读\n### 一、盲读者之四答\n· 读不懂处：（自报全懂）大体读懂。\n\n1）380:49『甲』\n2）380:101『乙』\n\n'
              '· 读错处：1）读错了：380:85『丙』\n\n2）一霎读歪\n\n· 想不想立刻读下一章：想\n### 二、本席之判\n'
              '**读误与否：否（misread=false）。** 四答无一处……\n- 读不懂1（甲）\n- 读错1（丙）\n- 读错2\n')
    钉('⑮之二 盲读（380 实样）：「### 二、本席之判」以下⛔入签（核席之「读误与否：否」）；「1）380:49」之条认（读不懂 2、读错 2）；值首「否（」者空',
       [(k, _读条(v)) for k, v, _ in m if not _空(v)] == [('读不懂处', 2), ('读错处', 2)] and _空('否（misread=false）。** 四答无一处')
       and _有意数('一、甲\n二、乙。（这两处是作者有意让我先错，错得舒服。）\n三、丙') == 2 and _有意数('一、甲') == 0)
    _p = os.path.join(ROOT, '版本', '第380章', '_轮记.md')
    if os.path.exists(_p):
        钉('⑮之三 真料 380：读错 4、读不懂 4（旧误读核席之判作读错 15）', sorted((k, _读条(v)) for k, v, _ in 盲读析(_读(_p)) if k in ('读不懂处', '读错处') and not _空(v))
           == [('读不懂处', 4), ('读错处', 4)])
    m395 = 盲读析('## 造式·盲读\n\n① 读懂否：大体懂，有几处卡住。\n- 开头「框外最底下一行，是第一百四十八日。」这一句，开头读不出来。\n'
                  '- 「她轻了。」谁说的、说给谁？读完仍不明白。\n\n② misread：\n'
                  '- 「床跟前地上，他还在。……他背靠着床，头歪在床沿上睡着。」我先以为「他」是那孩子，到「他爹醒了」才知是孩子他爹。\n'
                  '- 「床上那个人」我一直当作不知男女的病人，读到「那孩子的娘平躺在自家床上了」才知是孩子的娘。\n'
                  '- 「灶沿上那把勺不在了」：至今拿不准是那家人拿去喂饭了，还是别的。\n\n'
                  '③ 想读下一章。她揣着三折的纸、斜挎布包，把册子藏进床脚板底下，写完第一百四十九日就「出了寨」：人走了，光木头还剩着。\n\n'
                  '④ 她给那孩子的娘点脊背，第九处不暗了。\n\n⑤ 「柱子上那一竖还没有到底，她的拇指已经到了底，弯过来了。」\n')
    钉('⑮之四 盲读旧式（395:53—69 真行·复核须修②）：行首「③ 想读下一章。」无冒号亦作想读之签（⛔混入读错处、⛔「③」算一条）→ 读错 3、读不懂 2；'
       '「这一回读错是舒服的」（380:493）作有意',
       [(k, _读条(v)) for k, v, _ in m395 if k in ('读不懂处', '读错处')] == [('读不懂处', 2), ('读错处', 3)]
       and not any('想读' in v or '揣着' in v for k, v, _ in m395 if k == '读错处') and [k for k, _, _ in m395][-2:] == ['读到发生了什么', '最记得']
       and _有意数('1）读错了，後来才改过来：380:85『刘二从杠上直起身子』……才知道不是。这一回读错是舒服的。') == 1)
    病们, 先, 况 = 二稿账析('x\n> 局烂即造（约 22—55、269／272、273—350）；骨好则改\n> 455—473 稿数不足之章：459（三稿）、468（三稿）；458、461（四稿）。今⛔回改，执笔席失败之章\n'
                       '## 病\n- ~~[25—33] 绕｜盲读｜压~~〔已了〕\n- [340—378] 玉零现｜盲读C｜补回扣\n- [370] 未问｜审｜看\n- [1—379 之预示] 甲｜乙｜丙\n'
                       '- [全书] 星注｜裁｜剥净\n- [407] 视角翻向｜§三#3｜改「条案靠门那一头，那只碗还满着。」\n'
                       '- [404] 纯复｜§三#6｜删「，柄上那个窝冲着门」\n', 473,
                       lambda n: {407: '甲\n条案靠门那一头，那只碗还满着。\n', 404: '柄上那个窝冲着门'}.get(n))
    钉('⑯二稿账：划者⛔计、段计其首章、逾四十章之段与无章之条作 0（⛔丢·⛔计章热）、先审取「之章：」後、似已施（改句已在／删句仍在）、重造之章段',
       [(n, 改[:4], 施) for n, _, _, 改, _, 施 in 病们] == [(340, '补回扣', False), (370, '看', False), (0, '丙', False), (0, '剥净', False),
                                                           (407, '改「条案', True), (404, '删「，柄', False)]
       and 先[0] == [459, 468, 458, 461] and 先[1] == 3 and 况['全书'] == 1 and 况['节'] and 况['重造'] == [(22, 55), (269, 269), (272, 272), (273, 350)])
    _, _, 况2 = 二稿账析('## 第二稿之病\n- [370] 未问｜审｜看\n', 473)
    行132 = ('- [406] 「照着」与「另一边」打架、一段负六样｜§三#7；406:29｜改「他落过的那两处在街口那一边，我往另一边写」；路条与她到场拆段'
             '〔1103 X65 判：未施——器施：单_406（其一·换句）；其二拆段（大审册 §三#7：「第三行写完，」起另起一段至「……不到一拃。」止，「第四行」再另起）'
             '係增行，`还账.py` 行数不变⛔施——交主环以行变之器施〕')        # 二稿账:132 真行（换句已施、拆段未施）
    白406 = '他落过的那两处在街口那一边，我往另一边写。第三行写完，……不到一拃。'
    病3, _, _ = 二稿账析('## 病\n' + 行132 + '\n- [406] 老头左手｜§三#8；406:7｜删「老头那只左手一夜搁在膝盖上，指头弯着，没有伸开过。」\n', 473,
                     lambda n: 白406 if n == 406 else None)
    钉('⑯之三 二稿账半施（复核·宜修①）：引号之改已见而另有「拆段／另起」之令者作「半」（⛔似已施、⛔令划·留其权）；单删已施者仍似已施',
       [x[5] for x in 病3] == ['半', True] and _似已施('改「条案靠门那一头，那只碗还满着。」', '条案靠门那一头，那只碗还满着。') is True)
    x191 = ('- ②**L157「筒传完一圈以后，四个人又下去了一趟。」（数；相犯·章内）**：L167「刘二没进来。他在口子外头守着人」、L637「今天进去的三个把里头摸过一趟」'
            '——进者三人。〔**裁**：改「我们三个又下去了一趟」。〕另：L339—343「我出来的时候，三个人都在口子外头。钱满蹲在口子边上……」係倒述头一趟出口子'
            '（L127 之前后），非再下一趟之后（再下一趟钱满在里头）——读之可通，不改。')    # 第191章.md:105 真行
    钉('⑦之二 记录者有〔裁〕者只看裁首（复核·宜修②）：191②「〔裁：改…〕…读之可通，不改」计热；「〔裁：不改——…〕」「〔裁：不补於本章…〕」权 0；'
       '471「soft-2、soft-4 …——不改」⛔切作二条（不改 3、热 0）',
       [_条之等(x191), _条之等('- ⑧**L37**：甲〔**裁**：不改——自第四十三天水尽至今满十天〕'), _条之等('- ⑥**饮否**：乙〔**裁**：不补於本章——读作量完报完才分着喝〕')]
       == ['热', '不', '不']
       and 记录者析('**记录者读时所见（未改正文，备审）**：soft-1 灯之灭无交（:41 灯亮）——不改（读者自补）；soft-3 摊位雪上无印（:83、:113）——不改；'
                 'soft-2、soft-4 骨中一句之机与时——不改，476 前後合账。\n**总览席裁（0929）**：无。\n')[1:] == (0, 0, 3))
    钉('⑯之二 二稿账「## 病」改名 → 况报节不得（⓪⚠·⛔静读 0）', not 况2['节'] and 况2['条行'] == 1)
    审 = ('## 三·逐笔裁定\n\n| # | 判（席·题） | 据（章·拍·原句） | 裁 | 其由 |\n|---|---|---|---|---|\n'
         '| 1 | 468:69 甲 | 乙 | 已治·改单#1 | 由 |\n| 2 | 丙 | 466:11 丁 | 判不治 | 由 |\n| 3 | 戊 470 | 己 | **半治**——删 | 由 |\n'
         '| 4 | 庚 | 辛 | 已挂·限480（入段案） | 由 |\n\n## 四\n| a | b |\n')
    钉('⑰大审§三：裁之类与章之认（判栏「N:L」→据栏→首章号）', [(x[0], x[1], x[3]) for x in 大审析(审, 470)]
       == [(468, '已治', None), (466, '判不治', None), (470, '半治', None), (470, '已挂', 480)])
    审2 = ('## 三·逐笔裁定\n\n| # | 判（席·题） | 据 | 裁 | 其由 |\n|---|---|---|---|---|\n'
          '| 1 | 拍33—35 甲 | 乙 | **已治**（405 白文）〔原：已挂限四〇五〕 | 由 |\n| 2 | 丙 | 丁 | 同框之落处：已挂·限415（总编辑裁） | 由 |\n'
          '| 3 | | | ⛔待裁／已治／判驳／已挂 | |\n| 4 | 戊 | 己 | **已挂** | 其限 380 |\n')
    钉('⑰之二 大审§三（import 大审.三之行·⛔同功两处）：裁之类取首见之词、「拍33」⛔作章、模子作他、限只取裁格（限非数 None）',
       [(x[0], x[1], x[3]) for x in 大审析(审2, 470)] == [(470, '已治', None), (470, '已挂', 415), (470, '他', None), (470, '已挂', None)])
    try:                                   # ⑰之三 真册之行（W907 复核·另核同功两处）：每表重取其头、无裁栏之表跳过、改挂、〔原〕外之挂
        import 大审 as _审3
        真 = {n: {r['号']: (r['类'], r['限']) for r in _审3.三之行(_读(os.path.join(ROOT, '设定', '大审_至第%d章.md' % n)))}
             for n in (337, 397, 407, 410)}
        挂3 = {(x['至'], x['号']) for x in _审3.诸挂(473)}
        限3 = [r for r in _审3.三之行('## 三·逐笔裁定\n\n| 合 | 撞上它的席 | 其事 |\n|---|---|---|\n| 甲 | 乙 | 丙 |\n\n'
                                      '| # | 判（席·题） | 据 | 裁 | 其由 |\n|---|---|---|---|---|\n| 1 | a | b | **判驳** | c |\n\n> 注\n'
                                      '| 2 | d | e | **已挂·限 346** | f |\n\n### 上册逾限之笔·当面裁\n\n| 旧号 | 裁 | 其由 |\n|---|---|---|\n'
                                      '| 前册#16 | 改挂·限414 | 没有兑 |\n| 前册#10 | 已兑·409:63 | g |\n')]
    except Exception as e:
        真, 挂3, 限3 = {}, set(), [('败', str(e)[:60])]
    钉('⑰之三 大审§三真册（复核·同功两处）：337 首表「合」无裁栏⛔析、「>」注後之行续用前头（#2 判不治、#4—12 已挂限346）；'
       '397 #11「半治…已挂·限407」、#72 作已挂；407／410 次表「旧号｜裁｜其由」重取其头（前册#11 已挂限417、前册#17 判不治、410 前册#16 改挂限414、前册#10 他）；'
       '诸挂：407 前册#11 出（旧笔不及）、410 前册#16 本册 #18 已治之⛔出；号之名「大审407 前册#11」',
       真 and not any(k.startswith('**甲') for k in 真[337]) and 真[337]['2'] == ('判不治', None)
       and all(真[337][str(k)] == ('已挂', 346) for k in range(4, 13))
       and 真[397]['11'] == ('已挂', 407) and 真[397]['72'][0] == '已挂'
       and 真[407]['前册#11'] == ('已挂', 417) and 真[407]['前册#17'] == ('判不治', None) and 真[407]['13'] == ('已挂', 418)
       and 真[410]['前册#16'] == ('已挂', 414) and 真[410]['前册#10'] == ('他', None)
       and (407, '前册#11') in 挂3 and (410, '前册#16') not in 挂3 and (397, '11') not in 挂3
       and [(r['号'], r['类'], r['限']) for r in 限3] == [('1', '判驳', None), ('2', '已挂', 346), ('前册#16', '已挂', 414), ('前册#10', '他', None)]
       and _审3.号之名(407, '前册#11') == '大审407 前册#11' and _审3.号之名(440, '1') == '大审440 #1')
    段 = [(461, 470, 'a.md', {463: {'种': '埋「剪不动」→收 495；埋「链头」→收 469'}, 469: {'种': '收「链头」（埋於 463）'}}, {463: 9}),
         (471, 480, 'b.md', {471: {'种': '收「人写回」（埋於 465）'}, 465: {}}, {}),
         (461, 470, 'c.md', {465: {'种': '埋「人字写回」→收 471；埋「哎」→收 509'}, 470: {'种': '埋「那一卷」→收 474'}}, {}),
         (471, 480, 'd.md', {474: {'种': '收「那一卷」（埋於 470）'}, 473: {'种': '收「短一线」（埋於 424）'}}, {}),
         (401, 410, 'e.md', {410: {'种': '埋「结构校准两套」→收 412'}}, {}), (411, 420, 'f.md', {412: {'种': '收「两个包」（埋於 410）——两套原件'},
                                                                         415: {'种': '埋「协助」→收 447'}}, {}),
         (421, 430, 'g.md', {423: {'种': '埋「扬那一头，开」→收 473'}, 424: {'种': '埋「照本」→收 473'}}, {})]
    记样 = {473: {'悬': {'收': [], '接': [('423:79 扬那一头，开→:29 断', 0)]}}, 447: {'悬': {'收': [], '接': [('协助（415:23 钉 447·本章零碰）', 0)]}}}
    孤 = {(n, x): (宜, 况, 据) for n, x, _, 宜, _, 况, 据 in 段案种析(段, 473, 记样)}
    钉('⑱段案跨段（须修①）：段内⛔管；名似之收、旁名而同章之收（埋於 n·名不须似）俱认已收；段案无而详记悬线引其名者「记忆已引」；'
       '书「零碰」者⛔认；收在末章後：排收（宜於其排）、未排；收章已写而俱无：疑未收',
       孤 == {(463, '剪不动'): (495, '未排（收段之案未立）', None), (465, '人字写回'): (471, '已收', 471), (465, '哎'): (509, '未排（收段之案未立）', None),
             (470, '那一卷'): (474, '排收', None), (410, '结构校准两套'): (412, '已收', 412), (424, '照本'): (473, '已收', 473),
             (423, '扬那一头，开'): (473, '记忆已引', 473), (415, '协助'): (447, '疑未收', None)}
       and 段案之收('收「八枝」（埋於 41）——八枝俱清；收「她的结」（埋於 467）——解而重缠') == [('八枝', 41, '八枝俱清'), ('她的结', 467, '解而重缠')])
    # ⑱之三 一埋多指（复核·须修①之伪绿）：段案/461-470.md:64、:75、:108、:130、:141 与 471-480.md:41、:63、:96 之真行（摘其种）
    段3 = [(461, 470, '设定/段案/461-470.md', {
        463: {'种': 'SUS-C 复提：掀凳面那一方衣裳，手掌一抹，那一沓的厚没了（461 她揣走）；埋「链、锁、手绳」→收 469；埋「链、锁、手绳」→收 471；'
                    '埋「链、锁、手绳」→收 495；埋「剪不动」→收 495'},
        464: {'种': '收「柜上那张号码条」（埋於 461）——他知其处（读者自合）；埋「信封留桌」→收 470；埋「剩一站」→收 468；埋「他知其处」→收 473；埋「他知其处」→收 485'},
        467: {'种': '收「判纸新位、诸纸新位」（埋於 455）——判词在怀，那一沓贴其外（SUS-C）；埋「她的结」→收 470；埋「她的结」→收 476；埋「185 日末见东头」→收 481'},
        469: {'种': '收「链、锁、手绳」（埋於 463）——床板底下露一截链头，她没看'},
        470: {'种': '收「她的结」（埋於 467）——结还在她拇指那地方，⛔解；收「信封留桌」（埋於 464）——仍在原处（续 485）'}}, {463: 64, 464: 75, 467: 108}),
          (471, 480, '设定/段案/471-480.md', {471: {'种': '收「链、锁、手绳」（埋於 463）——床板底下抽出，束；收「链头」（埋於 469）'},
                                              473: {'种': '收「他知其处」（埋於 464）——「那一家」'},
                                              476: {'种': '收「三处一结」（埋於 471）——我重打；收「她的结」（埋於 467）——解而重缠'}}, {})]
    孤3 = {(n, x, k): (宜, 况, 据) for n, x, k, 宜, _, 况, 据 in 段案种析(段3, 473)}
    钉('⑱之三 一埋多指（复核·须修①）：同 (n, X) 之收与指照章序一一相配——463 链锁绳 469 段内、471 已收、495 未排（⛔被 469 之收闭）；'
       '464 他知其处 473 已收、485 未排（⛔被 473 之收闭）；467 她的结 476 排收（470 之收⛔闭之）',
       {k: v for k, v in 孤3.items() if k[1] in ('链、锁、手绳', '他知其处', '她的结')} == {
           (463, '链、锁、手绳', 471): (471, '已收', 471), (463, '链、锁、手绳', 495): (495, '未排（收段之案未立）', None),
           (464, '他知其处', 473): (473, '已收', 473), (464, '他知其处', 485): (485, '未排（收段之案未立）', None),
           (467, '她的结', 476): (476, '排收', None)})
    钉('⑱之二 线之镜（须修③）：主｜暗·她｜暗·霍钧｜暗·黎东来（「镜」去之）', [线之键(x) for x in ('主·入山194（＝暗188）', '暗·她·日186', '暗·霍钧·日186—187',
                                                               '暗·黎东来镜（第134日；＝主364同日）', '暗·黎东来·日188', '暗176')]
       == ['主', '暗·她', '暗·霍钧', '暗·黎东来', '暗·黎东来', '暗'])
    表 = [('地窖古尸', '418 启阵之废→440 青页→446 装匣→502 两指合目', 3), ('★血图原件', '446 连先人右手→500 九点一点一点暗', 4), ('霍钧', '391→393→471', 5)]
    钉('⑱之三 大悬配余章总案收线表（二字之交·首词同者先）、收链之章（⛔「N:L」之行、「第N段」、FS18、§二之9）',
       配收线('血图原件仍在地窖古尸手里（6:39；360 悬）', 表)[0] == '★血图原件' and 配收线('地窖古尸是谁、为何在苏家地底', 表)[0] == '地窖古尸'
       and 配收线('楼兰真相', 表) is None
       and _链章('418 启阵之废→440 青页（376:77 落指）→490；据 剧情庭_势_第411段；交预筛对 FS18；§二之9；1106 据') == [376, 418, 440, 490])
    钉('⑲用法之块：括内细块⛔取、「本站：」去冠', 用法之块('| E5 贺兰 | 331—约 395 | 起身之程 331—360（起 331—332｜离站 333—338）｜本站：到站 361—370｜人祸 383—389 |')
       == [(331, 360, '起身之程'), (361, 370, '到站'), (383, 389, '人祸')])
    钉('⑳一句去冠（括可嵌）', 一句('第178天（一月二十三日；E7 主线第八章）：老头下坡') == '老头下坡' and 一句('东头说「不」：走') == '东头说「不」：走'
       and 一句('暗186 天亮以前（E8 暗线第十五章·常；v01 合稿嫁大进三（窗亮人咳）、折缝）：鞋尖没了') == '鞋尖没了')
    r3 = 行家评析('## 名次\n\n先跑之印：净重 稿一 2325／稿二 2364\n\n稿二 ＞ 稿三 ＞ 稿一。胜稿：稿二\n\n'
                 '| 稿 | ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | ⑩×2 | 合 |\n|---|---|---|---|---|---|---|---|---|---|---|---|\n'
                 '| 稿二 | 9.5 | 9 | 9.5 | 9.5 | 9 | 9 | 9 | 9.5 | 9 | 19 | 102 |\n| 稿一 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 9 | 18 | 99 |\n')
    钉('㉗行家评：「胜稿：」先於「稿三。胜稿」之误读、⛔取「先跑之印」之首见；⑩栏已书其倍者折 110',
       r3 and r3['胜'] == '稿二' and r3['满'] == 110 and r3['十分'] == 9.27)
    m = 盲读析('## 造式·盲读\n**① 读不读得懂（understood／confused）**\nunderstood：大体读懂。\nconfused：\n- 甲\n- 乙\n\n'
              '**② 有无读错（misread）**\n- 丙\n③ want_next：想\n④ 她进城。\n⑤ 「柱子上那一竖。」\n')
    钉('㉘盲读·380—401 旧式（英文之键、行首④⑤依序）', [(k, _读条(v)) for k, v, _ in m if k in ('读不懂处', '读错处') and not _空(v)] == [('读不懂处', 2), ('读错处', 1)]
       and [k for k, v, _ in m][-2:] == ['读到发生了什么', '最记得'] and not _空(m[-1][1]))
    # ㉑—㉕ 小样之仓：源缺、器败、站界之病、标签漂移入⓪、--验 之比
    t = tempfile.mkdtemp(prefix='剧情全图_')
    try:
        os.makedirs(os.path.join(t, 记))
        for n, 悬 in ((1, '- **本章开**：\n  - 老头是谁（→ 3）\n'), (2, '**接**：\n- 1:3 甲\n**开**：\n- 乙（:7→9）\n**怪签**：丙\n'),
                      (3, '- 接：2:7 乙→:5\n- 开：丁（:9→5）\n- 欠：戊（→4）｜PLOT-1（→9）\n\n**记录者读时所见（未改正文，备审）**：soft-1 甲；soft-2 乙\n')):
            open(os.path.join(t, 记, '第%d章.md' % n), 'w', encoding='utf-8').write(
                '# 第%d章《名%d》\n\n## 悬线\n\n%s\n## 一句之要\n\n第%d章之要\n' % (n, n, 悬, n))
        open(os.path.join(t, 记, '总览.md'), 'w', encoding='utf-8').write(
            '# 全书记忆·总览（至第 2 章）\n\n## ② 按站\n\n### E1 甲（第 1—2 章）\n- **此站之事**：甲事\n\n### E2 乙（第 3 章起：写至 3）\n\n'
            '## ③ 逐章索引\n\n| 章 | 章名 | 线·日 | 一句之要 |\n|---|---|---|---|\n| 1 | 名1 | 主·入山1 | 第1天（甲）：一之事 |\n| 3 | 名3 | 主·入山3 | 三之事 |\n')
        def 坏(*a, **k):
            raise RuntimeError('造之败')
        器 = dict(默器())
        器.update({'站们': lambda root: [(1, 2, 'E1 甲')], 'FS未销': 坏, '大问': 坏, '约扫': lambda *a: [], '悬念判': 坏, '大审已挂': 坏,
                  '大审诸挂': 坏, '清态': lambda: ('done',)})
        文, 统, ctx = 生(t, 器)
        钉('㉑源缺·器败⛔崩：⓪俱报（到期账、悬线.md、用法.md、FS未销、大问……）', all(k in 文 for k in ('## ⓪', '## ⑤', '到期账', '悬线.md', '用法.md', 'FS未销 败', '大问 败'))
           and 统['缺'] >= 6)
        钉('㉒站界之病：总览②有 E2 而站们不认 → ⓪报其病', '⛔不认总览②之 E2' in 文 and '站外之章 3' in 文)
        钉('㉓⓪：总览题旧、③缺行、悬线之签不识计数', '题旧（末章 3）' in 文 and '③缺行 2' in 文 and '悬线之签不识 1 处（怪签×1·首 2）' in 文)
        钉('㉔末章悬线：欠俱入（⛔账号者）、开以後章之接所引者为已收', [x['欠何'] for x in ctx['环们'] if x['类'] == '末章悬线'] == ['〔欠〕戊（→4）', '〔开〕丁（:9→5）']
           and next(x for x in ctx['环们'] if x['欠何'].startswith('〔欠〕'))['态'] == '将到')
        open(os.path.join(t, 图档), 'w', encoding='utf-8').write(文)
        import io as _io, contextlib as _cl
        _生 = globals()['生']
        globals()['生'] = lambda root=ROOT, 器_=None: _生(root, 器)
        try:
            with _cl.redirect_stdout(_io.StringIO()):
                同 = globals()['验'](t)
            open(os.path.join(t, 图档), 'a', encoding='utf-8').write('旧\n')
            印 = _io.StringIO()
            with _cl.redirect_stdout(印):
                旧 = globals()['验'](t)
            open(os.path.join(t, 图档), 'w', encoding='utf-8').write(文.replace('\n## ③', '\n## 叁'))
            with _cl.redirect_stdout(_io.StringIO()):
                坏构 = globals()['验'](t)
            os.remove(os.path.join(t, 图档))
            with _cl.redirect_stdout(_io.StringIO()):
                不在 = globals()['验'](t)
        finally:
            globals()['生'] = _生
        钉('㉕--验（须修④·照进化树之例）：同即 0；图旧只 ⚠ rc 2（诸源封版之外常改·待下一封版随）并印其差；结构坏、不在 ⛔ rc 1',
           同 == 0 and 旧 == 2 and '⚠ 图旧' in 印.getvalue() and '-旧' in 印.getvalue() and 坏构 == 1 and 不在 == 1)
        块 = _一眼块(文)
        钉('㉙一眼·小样：题後首节（先於⓪）、书至末章、源之病照⓪（伤判者先：总览站事缺；总览③缺行、站界不认）与缺／败之数',
           文.split('\n## ')[1].startswith('一眼') and '**书至**：第 3 章《名3》' in 块 and '总览.md：③缺行 2' in 块
           and '站界：⛔不认总览②之 E2' in 块 and ('缺／败 %d' % 统['缺']) in 块 and '今站' not in 块
           and 块.index('总览.md：② E2 无「此站之事」') < 块.index('总览.md：③缺行 2'))
        # 悬线八之序号⛔作章号（宜修②）：小样之 ctx 直调 诸漏诸升
        小 = {'root': t, '末': 473, '缺': [], '鲜': [], '章': {}, '器': 器, '大审': [], '诸挂': [],
              '悬线文': '## 六、差\n| # | 事 | 裁 | 状 |\n|---|---|---|---|\n| 3 | 甲（200:5） | 改 | 待执 |\n'
                       '## 八、情理之疑\n1. **水**：141……至 191\n3. 两桶零半桶（271）→274\n'}
        漏_, _ = 诸漏诸升(小)
        钉('㉙之二 悬线八之序号「1.」「3.」⛔作章号（取 141、191、271、274）；六之待执取其事栏之章',
           sorted(n for n, 类, *_ in 漏_ if 类 == '情理之疑') == [141, 191, 271, 274] and [n for n, 类, *_ in 漏_ if 类 == '待执'] == [200])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ㉚ 一眼·造料：逾限多则列前 一眼之列 条、余书其数；将到分硬限（俱名）与宜於（只计其章）；久默只列其硬限者
    假 = [环('到期账', 's', 1, '逾%d' % i, 480, 限=470 + i) for i in range(8)]
    假 += [环('大问表', 's', 1, '甲问', 480, 限=482), 环('段案', 's', 1, '乙', 480, 宜=481), 环('段案', 's', 1, '丙', 480, 宜=481),
           环('FS', 's', 1, '丁', 480, 限=520, 末见=400), 环('大悬', 's', 1, '戊', 480, 末见=300)]
    假.sort(key=环序)
    块 = '\n'.join(一眼({'末': 480, '环们': 假, '漏': [], '升': [], '热': {}, '索': {}, '章': {}, '鲜': [('总览.md', '', '', '✓')], '缺': []}, []))
    钉('㉚一眼·造料：逾限列 6 余 2、将到（481—483）硬 1 软 2（481 章 2）、久默唯硬源（大悬之末见⛔计）、源无病',
       '**逾限 8**' in 块 and '余 2 见②' in 块 and '逾7' not in 块 and '**将到 3**（481—483 章）：硬限 1——甲问〔限 482·大问表·余 2〕' in 块
       and '宜於（软）2——481 章 2' in 块 and '**久默 1**' in 块 and '丁〔默 80·限 520〕' in 块 and '戊' not in 块
       and '**源之病**（⓪·伤判者先）：无；缺／败 0' in 块 and '**未闭之环 13**' in 块)
    # ㉖ 真仓：跑得动、⓪—⑤俱在、末章之行在、<30 秒（细⑦：二核之片并跑亦宽；速度之守交囤灰闸之「慢」）
    t0 = time.time()
    文, 统, ctx = 生(ROOT)
    秒 = time.time() - t0
    末 = 统['末']
    钉('㉖真仓：⓪—⑤俱在、⑤至末章（%d）、%.1f 秒 <30' % (末, 秒),
       all(('## %s' % k) in 文 for k in '⓪①②③④⑤') and ('| %d |' % 末) in 文 and 秒 < 30 and 末 > 400)
    块 = _一眼块(文)
    行们 = 块.split('\n')
    数 = re.search(r'\*\*数\*\*：共 (\d+) 环——([^。]*)。按源', 文)
    审首 = re.search(r'(?m)^\*\*读审家[^\n]*\n\n\| 章 \|[^\n]*\n\|[-|]+\n\| (\d+) \|', 文)
    先 = re.search(r'二稿先审之章\*\*（[^）]*）：([\d、]+)', 文)
    钉('㉛一眼·真仓：题後首节、≤%d 行／≤%d 字、诸行俱在（全）；其数与②③④同（环之态、读审家最热之首章、先审之章）、今站之弧在' % 一眼之限,
       文.split('\n## ')[1].startswith('一眼') and len(行们) <= 一眼之限[0] and len(块) <= 一眼之限[1]
       and 数 and ('**未闭之环 %s**（②）：%s——' % 数.groups()) in 块
       and 审首 and ('读审家 %s《' % 审首.group(1)) in 块
       and 先 and ('先审 ' + _合(int(x) for x in 先.group(1).split('、'))) in 块
       and '**今站 E' in 块 and '**脊**（①·每站一句）：E1 ' in 块
       and all(k in 块 for k in ('**书至**', '**未闭之环', '**漏之最热五章**', '**可升之最要**', '**末章之悬**', '**源之病**')))
    # ㉜—㊲ 真仓之钉（复核之须修与判者之错俱以真料钉之；以源之器自比，⛔钉会随书而变之数）
    环们 = ctx['环们']
    钉('㉜末章已封（宜修①）：⛔有将到之限／宜 ≤ 末章；将到之距俱 1—%d' % 将到,
       all(末 < (x['限'] if x['限'] is not None else x['宜']) <= 末 + 将到 for x in 环们 if x['态'] == '将到'))
    try:
        import 大审 as _审
        应 = [(x['至'], x['号']) for x in _审.诸挂(末) if x['限'] is not None]
    except Exception:
        应 = None
    钉('㉝大审诸挂（判者②）：大审.诸挂 限≤末者俱在②作逾限（旧笔之隙在内）、其数与⓪同',
       应 is not None and all(any(x['类'] == '大审已挂' and x['欠何'].startswith(_审.号之名(*kk) + ' ') and x['态'] == '逾限' for x in 环们) for kk in 应))
    线末 = ctx['线末']
    钉('㉞末章悬线每镜各取其末章（须修③）：诸镜俱在末一段之内、主与暗之镜俱有、主之末章即③主线之末',
       '主' in 线末 and any(k.startswith('暗·') for k in 线末) and all(末 - v < 10 for v in 线末.values())
       and 线末['主'] == max(n for n, v in ctx['索'].items() if v[1].startswith('主')))
    from collections import Counter as _C
    真孤 = 段案种析([(d['a'], d['b'], d['档'], d['节'], d['种行']) for d in ctx['段案']], 末, ctx['章'])
    钉('㉟段案（须修①）：段案环⛔有「已收」「记忆已引」者；疑未收者其收章 ≤ 末、俱⛔将到；一收只闭一指（同 (n, X) 之已收、排收⛔共一收章）',
       all(x['态'] == '疑未收' or (x['宜'] or 0) > 末 for x in 环们 if x['类'] == '段案')
       and all(v == 1 for v in _C((n, x, 据 if 况 == '已收' else 宜) for n, x, _, 宜, _, 况, 据 in 真孤 if 况 in ('已收', '排收')).values()))
    钉('㊱漏热之权 0 者（宜修③）⛔入章热：已裁不改、作者有意、似已施', all(权[类] == 0 for 类 in ('记录者·不改', '读错·有意', '二稿病·似已施'))
       and all(热(漏_x) == {} for 漏_x in ([(1, '记录者·不改', '', '', 3)], [(1, '读错·有意', '', '', 2)])))
    钉('㊲④定序（判者⑤c）：升序首为重造、次大审已挂；附④ 照其序', 升序[:3] == ('重造', '大审已挂', '先审')
       and 文.index('- **重造**') < 文.index('- **大审已挂而未收**') < 文.index('- **二稿先审之章**') if '- **重造**' in 文 else True)
    坏 = [n for n, ok in R if not ok]
    for n, ok in R:
        print('  %s %s' % ('✓' if ok else '⛔', n))
    print('剧情全图·自测 %d/%d' % (len(R) - len(坏), len(R)))
    return not 坏


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--验']:
        sys.exit(验())
    if len(a) == 2 and a[0] == '--章' and a[1].isdigit():
        sys.exit(一章(int(a[1])))
    if len(a) == 2 and a[0] == '--线':
        sys.exit(一线(a[1]))
    if a:
        print(__doc__)
        sys.exit(2)
    t, 统, ctx = 生()
    open(os.path.join(ROOT, 图档), 'w', encoding='utf-8').write(t)
    for 源, _, _, 病 in ctx['鲜']:                     # ⓪每次重生必印（源之病⛔静默）
        if 病 != '✓':
            print('  ⓪ %s：%s' % (源, _短(病, 150)))
    for 源, 病 in ctx['缺']:
        print('  ⓪ ⛔%s：%s' % (源, 病))
    病源 = len([1 for x in ctx['鲜'] if x[3] != '✓'])
    print('✓ 写 %s（至第 %d 章；%d 环：%s；漏 %d 条、升 %d 条；⓪病 %d 源、缺 %d；%d KB·%.1f 秒）'     # 末行带⓪病之数：封版只印末行（细⑥·⛔静默）
          % (图档, 统['末'], 统['环'], '、'.join('%s %d' % (k, v) for k, v in 统['态'].items() if v), 统['漏'], 统['升'], 病源, 统['缺'],
             len(t.encode()) // 1024, 统['秒']))
