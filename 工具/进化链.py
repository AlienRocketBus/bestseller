# -*- coding: utf-8 -*-
"""进化链 · 犯过的每一个错，今天有没有一道器在守着（2026-09-24 立·作者令）

⛔**作者原令之要**：「**曾经犯过的错误，之後不能再犯，要一个完整的进化链……
  我们的每一个机制，不论是什么样的机制，都要进化得越来越好。**」

★**盘上早记着很多错**——**只是散在四处，没有一条链串起来，也没有一道器问「今天谁在守它」**：
  `设定/机制体检账.md`（诸环·通例一至七〇）｜`设定/病族账.md`。
  ★1027·执行之审 #129：**裁之判唯归 `工具/裁之生效.py`**（同功两处即废劣者——旧「二·裁与册」一路与裁之生效各立一棘轮守同一批裁，判法又不同），本器⛔再收裁、册。
  ★1027·执行之审 #119：**体检账只认其顶节为一环**——题以环号起之节（`##`／`###`·㊀—㊿、数字、汉数、通例、附、第N节）；
    其下「一·其事」「二·其理」之子节与无号之节并入其父再判守（旧以每个 `## ` 为一环，子节虚撑地板 39 环）。
⛔**而令九·③ 早有一句：「写下来的法不生效，只有变成闸才生效。」**
  **一条只写在纸上、没有器守着的教训，下一坐照样会再犯**——**0924 之「待验无人读」即如此。**

★★**故本器做三件，皆判得死**：
  ①**串链**：把四处之教训逐环列成一条链（日期、一句之教、出处、守它的器），**写成 `设定/进化链.md`**；
  ②**问守**：**每一环有没有提到一道盘上真存在的器或负测**——⛔**提到而盘上不在者，不算守**；
  ③**棘轮**：**「无守之环」之数只许往下走，⛔不许往上涨**（其底在 `设定/进化链_棘轮.json`）——
    **新添一条教训而不给它配一道器，棘轮当场红**；**给一条旧教训配上了器，底自动下移**。
    ★1027·执行之审 #56：**每段（十章）须降 ≥ 段降（8）**——段底记於棘轮档之「段底」，入新段之首跑比上段之底，
    未降足（且未归零）即棘轮红（⛔只禁涨不逼降＝被容忍之地板）。
  ④**退役之二式**（⛔借标关闸之防）：〔随汰·<日>：…`工具/<已删器>`…〕（其器须真已不在盘上、且 git 史中真删过——从未有过之名⛔认）｜
    〔史·无须守·<日>：<由 ≥8 字>〕（只认体检账之环：一回之事或判断之训、器判不了者；俱列於链档之「退役」节、⛔隐）。
    ★**这就是「每一个机制都要进化得越来越好」之可数的那一半：它只能变好，不能变坏。**

⛔**本器之限（写死，不许假装做得到）**：**它判得了「有没有器守着」，⛔判不了「那道器守得住守不住」**
  ——**後一件归各器之负测（头一格须旧式回灌）。**

用法：
    python3 工具/进化链.py           # 串链、写 设定/进化链.md、过棘轮（连段降之律）
    python3 工具/进化链.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
链档 = os.path.join(ROOT, '设定', '进化链.md')
棘轮 = os.path.join(ROOT, '设定', '进化链_棘轮.json')
器名 = re.compile(r'([\w一-鿿]+\.(?:py|js))')
段降 = 8                                   # ★1027·#56：每段（十章）无守须降此数（或归零）
# ★1027·#119：环号——㊀—㊿、二三位之数、汉数（十一以上或带百／〇）、通例N、附·、第N节；「一·」「二之一·」等小号係子节
大号 = re.compile(r'^(?:第[一二三四五六七八九十]+节|通例[〇一二三四五六七八九十百]+|附·|[㊀-㊿]|\d{2,3}(?!\d)|'
                 r'(?:[二三四五六七八九]?十[一二三四五六七八九]?|[一二三四五六七八九]?[百〇][〇一二三四五六七八九十]*))')
小号 = re.compile(r'^[一二三四五六七八九十](?:之[一二三四五六七八九十])?·')
史式 = re.compile(r'〔史·无须守·\d{4}：([^〕]{8,})〕')
日式 = re.compile(r'(20\d\d)[-/]?(\d\d)[-/]?(\d\d)|(\d{4})(?=[_·])')


def _诸器():
    有 = set()
    for f in glob.glob(os.path.join(ROOT, '工具', '*.py')) + \
             glob.glob(os.path.join(ROOT, '工具', '席', '*.js')):
        有.add(os.path.basename(f))
    return 有


def _守(体, 有):
    """★其体里提到而盘上真在之器。⛔提到而不在者不算守。"""
    return sorted(set(x for x in 器名.findall(体) if x in 有))


def _日(s):
    m = re.search(r'(20\d\d)-(\d\d)-(\d\d)', s)
    if m:
        return '%s-%s-%s' % m.groups()
    m = re.search(r'_(\d\d)(\d\d)_', s)
    if m:
        return '2026-%s-%s' % m.groups()
    return '—'


def 随汰(s, root=None):
    """★1017 淘汰之律：教训所守之法已彻删者，随之退役——段中写「〔随汰·<日>：所守之法 `工具/<器>` 已彻删……〕」，
    且其所点之器**真已不在盘上、且 git 史中真删过**，方认（器仍在、或从未有过之名，俱⛔认：防借此标关闸）。→ 其器之名，或 ''。"""
    m = re.search(r'〔随汰[^〕]*`工具/([^`]+)`[^〕]*〕', s)
    if not m:
        return ''
    名 = m.group(1)
    if os.path.exists(os.path.join(root or ROOT, '工具', 名)):
        return ''
    # ★1027·线 D 复核：「已彻删」须真删过——盘上无而 git 史中亦从未有之名（如体检账六十九所点之 `工具/章界闸.py`，
    #   其闸实在 `跑轮.py` 之 gates 里、在役）⛔认：不在盘上者不全是已删，一个从未有过之名照样「不在」（防借标关闸）。
    删 = 删过之器(root)
    return 名 if 删 is None or 名 in 删 else ''


_删之器 = {}


def 删过之器(root=None):
    """→ git 史中真删过之器（`工具/` 下之相对名，如 '核轮.py'、'席/一章.js'）之集；一回 git log 取之、缓存。
    浅克隆或非 git 之仓 → None（验不得：照旧只验不在盘上，⛔误拦）。"""
    root = root or ROOT
    if root in _删之器:
        return _删之器[root]
    import subprocess
    出 = None
    try:
        浅 = subprocess.run(['git', 'rev-parse', '--is-shallow-repository'], cwd=root, capture_output=True, text=True)
        if 浅.returncode == 0 and 浅.stdout.strip() == 'false':
            r = subprocess.run(['git', '-c', 'core.quotepath=off', 'log', '--no-renames', '--diff-filter=D',
                                '--name-only', '--format=', '--', '工具/'], cwd=root, capture_output=True, text=True)
            if r.returncode == 0:
                出 = {l.strip()[len('工具/'):] for l in r.stdout.split('\n') if l.strip().startswith('工具/')}
    except Exception:
        出 = None
    _删之器[root] = 出
    return 出


def 史(s):
    """★1027·#29 #90：〔史·无须守·<日>：<由>〕——一回之事、判断之训，器判不了者移出链源（由须 ≥8 字；只认体检账之环）。→ 由，或 ''。"""
    m = 史式.search(s)
    return m.group(1).strip() if m else ''


def _号之类(题):
    t = re.sub(r'^[⛔★\*\s]+', '', 题)
    if 小号.match(t):
        return '小'
    return '大' if 大号.match(t) else ''


def 顶节(t):
    """★1027·#119：体检账 → 顶节之列。顶节＝题以环号起之 `##`／`###`；小号（一·、二之一·）在头一个大号之前之 `##` 亦为顶（档首之部），
    其後俱係子节；无号之节并入其父。→ [节之全文]"""
    节们, 见大, cur = [], False, None
    for l in t.split('\n'):
        m = re.match(r'^(#{2,3}) (.*)', l)
        if m:
            k = _号之类(m.group(2).strip())
            顶 = k == '大' or (k == '小' and not 见大 and m.group(1) == '##')
            见大 = 见大 or k == '大'
            if 顶:
                cur = [l]
                节们.append(cur)
                continue
        if cur is not None:
            cur.append(l)
    return ['\n'.join(x) for x in 节们]


def 诸环():
    """→ [{源, 名, 日, 守, 汰, 史}]。体检账之顶节＋病族；裁归 裁之生效（1027·#129）。"""
    有 = _诸器()
    环 = []
    # 一·体检账之顶节
    p = os.path.join(ROOT, '设定', '机制体检账.md')
    if os.path.exists(p):
        for s in 顶节(io.open(p, encoding='utf-8').read()):
            题 = s.split('\n', 1)[0].lstrip('#').strip()
            环.append({'源': '体检账', '名': re.sub(r'\*', '', 题)[:70],
                       '日': _日(题 + s[:400]), '守': _守(s, 有), '汰': 随汰(s), '史': 史(s)})
    # 二·病族
    p = os.path.join(ROOT, '设定', '病族账.md')
    if os.path.exists(p):
        for l in io.open(p, encoding='utf-8'):
            m = re.match(r'\|\s*\*\*([^*]+)\*\*[^|]*\|\s*(\d+)\s*\|\s*([^|]+)\|', l)
            if m:
                环.append({'源': '病族账', '名': m.group(1).strip()[:70], '日': '2026-09-24',
                           '守': _守(m.group(3), 有) or (['（书之族·第三回方立）']
                                                        if '书之族' in m.group(3) else []),
                           '汰': 随汰(m.group(3))})   # ★1027：病族之环亦认随汰（其器彻删、其病随之去）
    return 环


def 读底():
    try:
        return json.load(io.open(棘轮, encoding='utf-8'))
    except Exception:
        return None


def _计(环):
    """→ (活环, 有守, 无守, 汰, 史)：汰、史俱退役⛔计。"""
    汰 = [x for x in 环 if x.get('汰')]
    史们 = [x for x in 环 if not x.get('汰') and x.get('史')]
    活 = [x for x in 环 if not x.get('汰') and not x.get('史')]
    return 活, [x for x in 活 if x['守']], [x for x in 活 if not x['守']], 汰, 史们


def 写链(环):
    环, _, _, 汰, 史们 = _计(环)
    有守 = [x for x in 环 if x['守']]
    无守 = [x for x in 环 if not x['守']]
    L = ['# 进化链（由 `工具/进化链.py` 自盘上四处之教训串成·⛔勿手改·每回自动重写）', '',
         '> ⛔**犯过的每一个错，今天有没有一道器在守着。**',
         '> **「写下来的法不生效，只有变成闸才生效」**（令九·③）。', '',
         '## 〇·总数', '',
         '| 环 | 有守 | 无守（只写在纸上） |', '|---|---|---|',
         '| %d | %d | **%d** |' % (len(环), len(有守), len(无守)), '',
         '⛔**「无守」之数只许往下走（棘轮·`设定/进化链_棘轮.json`）**——'
         '**新添一条教训而不配一道器，当场红。**', '',
         '★随汰（1017 淘汰之律：所守之法已彻删，教训随之退役、⛔计入上表）：%d 条%s' % (len(汰), ('——' + '；'.join('%s（%s）' % (x['名'][:30], x['汰']) for x in 汰)) if 汰 else ''), '',
         '★史·无须守（1027·执行之审 #29 #90：一回之事、判断之训，器判不了——移出链源、⛔计入上表；逐条列其由，⛔隐）：%d 条' % len(史们), '']
    L += ['- %s ｜%s' % (x['名'][:50].replace('|', '／'), x['史'][:90]) for x in 史们]
    L += ['', 
         '## 一·无守之环（⛔下一个该配器的，就在这里挑）', '',
         '| 日 | 出处 | 一句之教 |', '|---|---|---|']
    for x in sorted(无守, key=lambda y: y['日'], reverse=True):
        L.append('| %s | %s | %s |' % (x['日'], x['源'], x['名'].replace('|', '／')))
    L += ['', '## 二·有守之环（其器在盘上）', '', '| 日 | 出处 | 一句之教 | 守它的器 |',
          '|---|---|---|---|']
    for x in sorted(有守, key=lambda y: y['日'], reverse=True):
        L.append('| %s | %s | %s | %s |' % (x['日'], x['源'], x['名'].replace('|', '／'),
                                          '、'.join(x['守'][:4])))
    io.open(链档, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    return len(有守), len(无守)


def 末章():
    """盘上正文之末章（借 囤灰闸.末章：档名之汉数）；读不出 → 0（段降之律⛔判）。"""
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_tg_jhl', os.path.join(ROOT, '工具', '囤灰闸.py'))
        _m = _u.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        _m.ROOT = ROOT
        return _m.末章()
    except Exception:
        return 0


def 段之判(底, 无, 末):
    """★1027·#56：段＝(末章+9)//10（401—410 为 41）。→ (红语或 '', 段, 新段否)。入新段之首跑：上段之底在而今无守 > max(0, 上段之底 − 段降) 即红。"""
    if not 末:
        return '', None, False
    段 = (末 + 9) // 10
    段底 = 底.get('段底') or {}
    新 = str(段) not in 段底
    前 = 段底.get(str(段 - 1))
    if 前 is not None and 无 > max(0, 前 - 段降):
        return ('⛔**棘轮红·段降之律**：第%d段（%d—%d 章）之无守 %d，较上段之底 %d 未降足 %d（须 ≤ %d）——'
                '**只禁涨不逼降，即被容忍之地板**（执行之审 #56）。' % (段, 段 * 10 - 9, 段 * 10, 无, 前, 段降, max(0, 前 - 段降))), 段, 新
    return '', 段, 新


def 跑(写=True):
    环 = 诸环()
    活, 有们, 无们, 汰, 史们 = _计(环)
    if 写:
        写链(环)
    有, 无 = len(有们), len(无们)
    底 = 读底()
    print('════ 进化链 · 犯过的每一个错，今天有没有一道器在守着 ════')
    print('  共 %d 环｜有守 %d｜⛔无守（只写在纸上）%d' % (len(活), 有, 无))
    print('  ★退役：随汰 %d｜史·无须守 %d（链档之「退役」节逐条列其由）｜裁归 裁之生效（#129）' % (len(汰), len(史们)))
    if 底 is None:
        if 写:
            io.open(棘轮, 'w', encoding='utf-8').write(
                json.dumps({'无守之底': 无, '立於': '2026-09-24'}, ensure_ascii=False))
        print('  ★棘轮初立：无守之底 = %d（⛔此後只许往下走）' % 无)
        return True
    b = 底['无守之底']
    史顶 = 底.get('史之顶')
    if 史顶 is not None and len(史们) > 史顶:
        print('  ⛔**棘轮红·史之门**：「史·无须守」%d 条 ＞ 其顶 %d——**史之门只开於 1027 之链裁（一回之事、判断之训）**；'
              '此後之教训须配器（或随汰），⛔借「史」之标关闸。' % (len(史们), 史顶))
        return False
    if 写 and 史顶 is None:
        底['史之顶'] = len(史们)
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps(底, ensure_ascii=False))
    段红, 段, 新段 = 段之判(底, 无, 末章())
    if 段红:
        print('  ' + 段红)
        print('     ★其治：本段之内逐环配器（节末写守器之名·器须在役），或随汰、或判「史·无须守」并书其由。')
        return False
    if 写 and 段 is not None and 新段:
        底.setdefault('段底', {})[str(段)] = min(无, b)
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps(底, ensure_ascii=False))
        print('  ★段底：第%d段 = %d（下段之首须 ≤ %d）' % (段, min(无, b), max(0, min(无, b) - 段降)))
    if 无 > b:
        print('  ⛔**棘轮红：无守 %d ＞ 底 %d**——**新添了 %d 条教训而没配器**；'
              '⛔**一条只写在纸上的教训，下一坐照样会再犯。**' % (无, b, 无 - b))
        print('     ★其治：给那几条配一道器（或负测），**在其教训之文里写明器名**。')
        return False
    if 无 < b and 写:
        底['无守之底'] = 无
        底.setdefault('下移之记', []).append('%d→%d' % (b, 无))
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps(底, ensure_ascii=False))
        print('  ★**棘轮下移：%d → %d**（又有 %d 条教训配上了器——**这就是进化**）' % (b, 无, b - 无))
    else:
        print('  ✓棘轮：无守 %d ≤ 底 %d' % (无, b))
    print('  ★其链已写：设定/进化链.md')
    return True


def 自测():
    global 棘轮, 诸环
    R = []
    有 = _诸器()
    R.append(('①盘上之器数得着（今 %d）' % len(有), len(有) > 100))
    R.append(('②⛔提到而盘上不在之器不算守',
              _守('见 `工具/并不存在的器.py`', 有) == []))
    R.append(('②之二·提到而在者算守', _守('见 `工具/存底.py`', 有) == ['存底.py']))
    R.append(('②之三·随汰：所点之器已彻删（git 史中删过）方认（1017 淘汰之律）', 随汰('〔随汰·1027：所守之法 `工具/核轮.py` 已彻删〕') == '核轮.py'
              and 随汰('〔随汰·1027：所守之法 `工具/席/一章.js` 已彻删〕') == '席/一章.js'))
    R.append(('②之四·随汰：所点之器仍在即⛔认（防借标关闸）', 随汰('〔随汰·1017：所守之法 `工具/存底.py` 已彻删〕') == ''))
    # ②之五 回灌 a0c6cc98 之体检账六十九：所点 `工具/章界闸.py` 从未有过（其闸在 跑轮.py 之 gates·在役）→ ⛔认；git 史验不得（浅克隆）时照旧只验不在盘
    _删 = 删过之器()
    R.append(('②之五·随汰：从未有过之名（六十九之 `工具/章界闸.py`）⛔认——不在盘上≠已删（防借标关闸）',
              (_删 is None) or (随汰('〔随汰·1027：所守之法 `工具/章界闸.py` 已彻删——十三轮之章界闸随轮务 1027 汰（#119）〕') == ''
                                and 随汰('〔随汰·1027：所守之法 `工具/并不存在的器.py` 已彻删〕') == '')))
    环 = 诸环()
    R.append(('③串得出链（今 %d 环·体检账之顶节＋病族）' % len(环), len(环) > 120))
    R.append(('④二处皆入链、裁⛔入（#129：裁之判唯归 裁之生效）', {'体检账', '病族账'} <= set(x['源'] for x in 环)
              and not any(x['源'].startswith(('裁_', '册_')) for x in 环)))
    R.append(('④之二·病族亦认随汰（今病族 %d 环已汰）' % sum(1 for x in 环 if x['源'] == '病族账' and x.get('汰')),
              any(x['源'] == '病族账' and x.get('汰') for x in 环)))
    # ★1027·#119：顶节——子节（一·其事）与无号之节并入其父；### 之环号亦为顶；档首之「一·」（未见大号前）为顶
    样 = ('# 账\n## 一·档首之部\n甲\n## 七十一 **大号之环**\n乙\n## 一·其事\n见 `工具/存底.py`\n## ⛔**其所以要记**\n丙\n'
          '### 七十二 **三级之环**\n丁\n## 二·其理\n戊\n## 52 0922·**数字之环**\n己\n')
    节 = 顶节(样)
    题们 = [s.split('\n', 1)[0] for s in 节]
    R.append(('⑦顶节：子节与无号之节并入其父（七十一 收「一·其事」之 存底.py）、### 之环号亦为顶',
              题们 == ['## 一·档首之部', '## 七十一 **大号之环**', '### 七十二 **三级之环**', '## 52 0922·**数字之环**']
              and _守(节[1], 有) == ['存底.py'] and _守(节[2], 有) == []))
    # ⑦之二 回灌旧树：旧式（每个 `## ` 一环）於真体检账虚撑之环 > 新式之顶节——子节确被并入（#119 之病）
    try:
        _t = io.open(os.path.join(ROOT, '设定', '机制体检账.md'), encoding='utf-8').read()
        旧数 = sum(1 for s in re.split(r'\n(?=## )', _t) if s.startswith('## '))
        新顶 = 顶节(_t)
        子 = sum(1 for s in re.split(r'\n(?=## )', _t) if s.startswith('## ') and 小号.match(re.sub(r'^[⛔★\*\s]+', '', s[3:])))
        R.append(('⑦之二·回灌真体检账：旧式 %d 节里小号子节 %d，新式顶节 %d 无一以小号子节起（档首之部除外）' % (旧数, 子, len(新顶)),
                  子 > 20 and not any(小号.match(re.sub(r'^[⛔★\*\s]+', '', s.split('\n', 1)[0].lstrip('#').strip()))
                                     for s in 新顶[10:])))
    except Exception as e:
        R.append(('⑦之二·回灌真体检账读不得：%s' % e, False))
    # ⑧史·无须守：由 ≥8 字方认；短由、缺日⛔认（防借标关闸）
    R.append(('⑧史·无须守：「〔史·无须守·1027：一回之事其器判不了之训〕」认；由短於八字、缺日俱⛔认',
              bool(史('〔史·无须守·1027：一回之事其器判不了之训〕')) and not 史('〔史·无须守·1027：短由〕')
              and not 史('〔史·无须守：一回之事其器判不了之训〕')))
    # ⑨段降之律（#56）：上段之底在而本段未降足 → 红；降足、归零 → 放行；无末章 → ⛔判
    R.append(('⑨段降：上段底 78 而今 78（410→411 入新段）→ 红', bool(段之判({'段底': {'41': 78}}, 78, 411)[0])))
    R.append(('⑨之二 放行：降足（78→70）、归零（5→0）、首段无上段之底、末章读不出', not 段之判({'段底': {'41': 78}}, 70, 411)[0]
              and not 段之判({'段底': {'41': 5}}, 0, 415)[0] and not 段之判({}, 78, 411)[0] and not 段之判({'段底': {'41': 78}}, 78, 0)[0]))
    R.append(('⑨之三 同段之内⛔比（41 段之内 78 不红）', not 段之判({'段底': {'41': 78}}, 78, 410)[0]))
    # ⑩史之门（防借史之标关闸）：史之数逾其顶即红；不逾放行
    import tempfile as _tf, contextlib as _cl
    _老, _老环 = 棘轮, 诸环
    _d = _tf.mkdtemp(prefix='棘轮史_')
    try:
        棘轮 = os.path.join(_d, 'r.json')
        _假史 = {'源': '体检账', '名': '假·新添之教训标作史', '日': '—', '守': [], '汰': '', '史': '一回之事其器判不了之训'}
        _今史 = len(_计(_老环())[4])
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps({'无守之底': 99999, '史之顶': _今史}))
        诸环 = lambda: _老环() + [_假史]
        with _cl.redirect_stdout(io.StringIO()):
            _红 = 跑(写=False)
        诸环 = _老环
        with _cl.redirect_stdout(io.StringIO()):
            _放 = 跑(写=False)
        R.append(('⑩史之门：今史 %d 而注一新史 → 棘轮红；不添 → 放行' % _今史, _红 is False and _放 is True))
    finally:
        棘轮, 诸环 = _老, _老环
    # ⑤⛔棘轮之牙：无守之数比底大即红——★1027：今链无守或已归零，⛔借今之数（为零即空验）：注一假无守之环
    import tempfile
    老, 老环 = 棘轮, 诸环
    d = tempfile.mkdtemp(prefix='棘轮_')
    棘轮 = os.path.join(d, 'r.json')
    try:
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps({'无守之底': 0}))
        import contextlib
        诸环 = lambda: 老环() + [{'源': '体检账', '名': '假·新添而未配器之教训', '日': '—', '守': [], '汰': '', '史': ''}]
        with contextlib.redirect_stdout(io.StringIO()):
            ok = 跑(写=False)
        诸环 = 老环
        R.append(('⑤⛔棘轮之牙：底设 0 而注一无守之环 → 当场红', ok is False))
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps({'无守之底': 99999}))
        with contextlib.redirect_stdout(io.StringIO()):
            ok2 = 跑(写=False)
        R.append(('⑤之二·底比今大者不红（⛔证⑤非一律判否）', ok2 is True))
    finally:
        棘轮, 诸环 = 老, 老环
    R.append(('⑥⛔本器之限写明：判得了「有没有器守」，判不了「守不守得住」',
              '判不了「那道器守得住守不住」' in io.open(__file__, encoding='utf-8').read()))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 进化链·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 跑() else 1)
