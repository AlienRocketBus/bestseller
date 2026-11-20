#!/usr/bin/env python3
"""裁之生效 —— 做了的决定必须生效（2026-09-24 作者当面令立）。

★作者原话之意：「我们已经做出来的决定一定要去执行，有很多决定没有生效——
  那做这件事的意义是什么？浪费时间和资源吗？」

★本器只问一件，判得死：**`设定/裁_*.md` 每一份裁，须点名至少一样守它的器
  （`工具/xxx.py` 或 `工具/席/xxx.js`），且那一样器须真在盘上、且真接在 `全测.py` 里
  （或它本身是 `全测.py`／`自走.py` 每跑必调之器）。**
  ——只写在纸上、没有一样器在守的裁，就是「做了而没生效」的那一种。

★旧裁以棘轮守：**未生效之裁数只许降、不许升**；
  0924（含）以後所立之裁，一份也不许未生效——立裁之日须同日配器。

★1027·执行之审 #75 #129 #56（总编辑之裁·线 D）：
  ①**裁之判唯归本器**（进化链⛔再收裁，同功两处即废劣者）。
  ②**行之证**：只点器名者，证得了「有器在跑」，证不了「裁之文被施」（裁_1020_D1落式 点 行号随移.py 即算生效，而其裁之实一字未行）。
    故 **1027（含）以後所立之裁，须书行之证之一**——`法用#<id>`（其 id 在法用册之法／待）｜`到期账 <id>`（在账，到限须已结）｜
    `改单#G…`（在改单账且已结）；⛔只点器者判未生效。
    **0924—1026 之裁过渡**：只点器而无行之证者印其数（「只点器之底」·棘轮只许降），⛔拦。
  ③**旧裁未生效之底至第 420 章须 0**（限章），未达即红——⛔只禁涨不逼降。
〔1119 W908 环7〕进化链之器废（裁九·并入进化树）：其所借之 随汰／删过之器（git 史之删）归本器（一处判·自进化环、负测_自进化环 借之），
  末章径借 囤灰闸.末章（旧经 进化链 转借）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
棘轮档 = os.path.join(ROOT, '设定', '裁之生效_棘轮.json')
新令起 = '20260924'   # ★此日（含）以後之裁：一份也不许未生效
行证令起 = '20261027'  # ★1027·#75：此日（含）以後之裁须书行之证之一（法用#／到期账／改单#）
限章 = 420         # ★1027·#56：旧裁未生效之底至此章须 0
_结 = ('done', 'closed', '清', '已清', '废弃', '废', '已废', 'void')


def _src(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''


def _在役():
    """全测／自走／诸席所调之器之名（档名）。"""
    s = _src('工具/全测.py') + _src('工具/自走.py') + ''.join(
        _src(os.path.relpath(f, ROOT)) for f in glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    return s


def 守器(裁文):
    """裁文里点名之器：`工具/xxx.py`、`xxx.py`、`工具/席/xxx.js`。
    〔1119 W908 环7 复核〕〔随汰…〕之标内所点之器⛔算守（借标续命：标书「其守归 X.py」，X 在役即判生效，而 X 未必守其往前之令——
      0919／0922 看官账四裁之标初书「逐字重出之守归 重出趋.py」，重出趋只报逾 10% 之章，⛔守 345至347 §三 之永禁一句）。"""
    裁文 = re.sub(r'〔随汰[^〕]*〕', '', 裁文 or '')
    names = set(re.findall(r'([\w一-鿿]+\.py)', 裁文)) | set(re.findall(r'(席/[\w一-鿿]+\.js)', 裁文))
    return {n for n in names if os.path.exists(os.path.join(ROOT, '工具', n))}


def 随汰(文, root=None):
    """★1017 淘汰之律·1027 裁之退役：文中「〔随汰·<日>：所守之法 `工具/<器>` 已彻删……〕」，
    且其所点之器**真已不在盘上、且 git 史中真删过**，方认 → 其器名（如 '核轮.py'、'席/一章.js'）；否则 ''。
    ⛔器仍在、或从未有过之名（不在盘上≠已删），俱⛔认（防借标关闸）。一处判：自进化环（病族之随汰）借之，⛔两份码。
    〔W908 环7〕旧借 进化链.随汰——进化链之器废，其判移此（判法照旧）。"""
    m = re.search(r'〔随汰[^〕]*`工具/([^`]+)`[^〕]*〕', 文 or '')
    if not m:
        return ''
    名 = m.group(1)
    if os.path.exists(os.path.join(root or ROOT, '工具', 名)):
        return ''
    删 = 删过之器(root)
    return 名 if 删 is None or 名 in 删 else ''


_删之器 = {}


def 删过之器(root=None):
    """→ git 史中真删过之器（`工具/` 下之相对名，如 '核轮.py'、'席/一章.js'）之集；一回 git log 取之、缓存。
    浅克隆或非 git 之仓 → None（验不得：照旧只验不在盘上，⛔误拦）。〔W908 环7〕旧在 进化链.py，移此。"""
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


def _读json(rel):
    try:
        return json.load(io.open(os.path.join(ROOT, rel), encoding='utf-8'))
    except Exception:
        return None


def 诸账():
    """→ {'法': 法用册之法与待之 id 集, '到期': {id: 笔}, '改单': {号: 单}}（读不得者空）。"""
    册 = _读json(os.path.join('设定', '法用册.json')) or {}
    到 = _读json(os.path.join('设定', '到期账.json'))
    笔们 = 到 if isinstance(到, list) else ((到 or {}).get('账') or (到 or {}).get('items') or [])
    改 = _读json(os.path.join('设定', '改单账.json')) or {}
    return {'法': {x.get('id') for x in (册.get('法') or []) + (册.get('待') or []) if x.get('id')},
            '到期': {x['id']: x for x in 笔们 if isinstance(x, dict) and x.get('id')},
            '改单': {x['号']: x for x in 改.get('单') or [] if x.get('号')}}


def 行之证(裁文, 账, 末=0):
    """→ (证们, 坏们)：法用#<id>（在法／待）｜到期账 <id>（在账；其到期章 ≤ 末章者须已结）｜改单#G…（在账且 状=毕）。"""
    证, 坏 = [], []
    for i in re.findall(r'法用#([^\s`，。、；：）)〕\]」｜|*]+)', 裁文):
        (证 if i in 账['法'] else 坏).append('法用#%s%s' % (i, '' if i in 账['法'] else '（册无此法）'))
    for 号 in re.findall(r'改单#\s*(G\d{4}-\d{2})', 裁文):
        x = 账['改单'].get(号)
        if x and x.get('状') == '毕':
            证.append('改单#' + 号)
        else:
            坏.append('改单#%s（%s）' % (号, '未结' if x else '账无此单'))
    for i in re.findall(r'到期账\s*[`「]?([A-Z][A-Z0-9]*-[^\s`」，。、；：）)〕\]｜|*]+)', 裁文):
        x = 账['到期'].get(i)
        if not x:
            坏.append('到期账 %s（账无此笔）' % i); continue
        到 = x.get('到期章')
        if isinstance(到, int) and 末 and 到 <= 末 and str(x.get('状态', '')).strip() not in _结:
            坏.append('到期账 %s（限 %d 已到而未结）' % (i, 到)); continue
        证.append('到期账 ' + i)
    return 证, 坏


def 查(档们=None, 在役=None, 账=None, 末=None, 只点=None):
    """→ [(裁名, 由)]：未生效之裁（随汰而退役者不计）。只点：传一列者，0924—1026 之裁只点器而无行之证者入之（⛔入坏）。"""
    档们 = 档们 if 档们 is not None else sorted(glob.glob(os.path.join(ROOT, '设定', '裁_*.md')))
    在役 = _在役() if 在役 is None else 在役
    账 = 诸账() if 账 is None else 账
    末 = 末章() if 末 is None else 末
    坏 = []
    for f in 档们:
        名 = os.path.basename(f)
        _文 = io.open(f, encoding='utf-8', errors='replace').read()
        if 随汰(_文):
            continue                     # ★1027：所守之法已彻删、裁随之退役（⛔计未生效；其史在档）
        日 = _日(名)
        if 跨年之名(名):
            坏.append((名, '档名书 MMDD 而在跨年之後——改名为 裁_YYYYMMDD_…（只书月日，新旧之律即判错）'))
            continue
        证, 证坏 = 行之证(_文, 账, 末) if 日 >= 新令起 else ([], [])
        if 日 >= 行证令起:              # ★1027·#75：只点器名不再算生效
            if not 证:
                坏.append((名, '无行之证（法用#<id>｜到期账 <id>｜改单#G… 之一）%s' % (('：' + '；'.join(证坏)) if 证坏 else '')))
            continue
        器 = 守器(_文)
        if not 器:
            坏.append((名, '无一样器守它'))
            continue
        活 = [x for x in 器 if x in ('全测.py', '自走.py') or os.path.basename(x) in 在役 or x in 在役]
        if not 活:
            坏.append((名, '所点之器（%s）未接进全测／自走／诸席' % '、'.join(sorted(器))))
        elif 只点 is not None and 日 >= 新令起 and not 证:
            只点.append((名, '只点器（%s）而无行之证' % '、'.join(sorted(活))))
    return 坏


def _日(名):
    """裁_YYYYMMDD_… → 'YYYYMMDD'；裁_MMDD_…（旧式，俱 2026：裁档始於 0913）→ '2026MMDD'；他 → '00000000'。
    ★1027 治跨年：只比 MMDD，0105 之裁即落「旧裁」而免行之证——新裁书 YYYYMMDD，旧式而 MMDD < 0913 者即红（跨年之後）。"""
    m = re.match(r'裁_(\d{8}|\d{4})(?!\d)', 名)
    if not m:
        return '00000000'
    return m.group(1) if len(m.group(1)) == 8 else '2026' + m.group(1)


def 跨年之名(名):
    """旧式 MMDD 之名而 MMDD < 0913（即跨年之後所立）→ True：须书 裁_YYYYMMDD_。"""
    m = re.match(r'裁_(\d{4})(?!\d)', 名)
    return bool(m and m.group(1) < '0913')


def 末章():
    """盘上正文之末章（借 囤灰闸.末章：档名之汉数）；读不出 → 0（限章⛔判）。〔W908 环7〕旧经 进化链 转借，进化链之器废即径借。"""
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_tg_cszx', os.path.join(ROOT, '工具', '囤灰闸.py'))
        _m = _u.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        _m.ROOT = ROOT
        return _m.末章()
    except Exception:
        return 0


def 判(坏, 只点, 底, 末):
    """纯判 → (ok, 行们, 新底)。底：{'旧裁未生效之底', '只点器之底'}（缺者初立）。"""
    新坏 = [x for x in 坏 if _日(x[0]) >= 新令起]
    旧坏 = [x for x in 坏 if _日(x[0]) < 新令起]
    底 = dict(底 or {})
    ok, L = True, []
    if 新坏:
        ok = False
        L.append('  ⛔0924 以後之裁未生效 %d 份（⛔立裁同日须配器；1027 起须书行之证）：' % len(新坏))
        L += ['     · %s：%s' % (n, why) for n, why in 新坏]
    b = 底.get('旧裁未生效之底')
    if b is None:
        底['旧裁未生效之底'] = b = len(旧坏)
        L.append('  ℹ棘轮初立：旧裁未生效 %d 份（此後只许降）' % b)
    elif len(旧坏) > b:
        ok = False
        L.append('  ⛔棘轮红：旧裁未生效 %d 份 ＞ 其底 %d' % (len(旧坏), b))
    else:
        底['旧裁未生效之底'] = min(b, len(旧坏))
        L.append('  ✓旧裁未生效 %d 份（其底 %d·只许降）' % (len(旧坏), b))
    if 旧坏 and 末 and 末 >= 限章:
        ok = False
        L.append('  ⛔限章红：第 %d 章已到限（%d）而旧裁未生效仍 %d 份——须 0（执行之审 #56）' % (末, 限章, len(旧坏)))
    if 旧坏:
        L += ['     · %s：%s' % (n, why) for n, why in 旧坏]
    c = 底.get('只点器之底')
    if c is None:
        底['只点器之底'] = c = len(只点)
    if len(只点) > c:
        ok = False
        L.append('  ⛔棘轮红：0924—1026 之裁只点器而无行之证 %d 份 ＞ 其底 %d（过渡之数只许降）' % (len(只点), c))
    else:
        底['只点器之底'] = min(c, len(只点))
        L.append('  ℹ过渡：0924—1026 之裁只点器而无行之证 %d 份（其底 %d·只许降；补「法用#／到期账／改单#」之一即出此数）' % (len(只点), c))
    if ok and not 新坏:
        L.append('  ✓0924 以後之裁，份份有器在守；1027 起之裁份份有行之证。')
    return ok, L, 底


def 报():
    只点 = []
    坏 = 查(只点=只点)
    底 = _读json(os.path.relpath(棘轮档, ROOT)) if os.path.exists(棘轮档) else None
    ok, L, 新底 = 判(坏, 只点, 底, 末章())
    print('════ 裁之生效 ════（做了的决定须有器守、且那器真在跑；1027 起须有行之证）')
    print('\n'.join(L))
    if 新底 != (底 or {}):
        json.dump(新底, io.open(棘轮档, 'w', encoding='utf-8'), ensure_ascii=False)
    return ok


def 自测():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    R = []
    try:
        a = os.path.join(d, '裁_0999_空.md'); io.open(a, 'w', encoding='utf-8').write('只写了一句话。')
        b = os.path.join(d, '裁_0999_有器不在役.md'); io.open(b, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。')
        c = os.path.join(d, '裁_0999_有器在役.md'); io.open(c, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。法用#假法')
        账 = {'法': {'假法'}, '到期': {'ARC-999-甲': {'id': 'ARC-999-甲', '到期章': 400, '状态': 'done'},
                                       'ARC-999-乙': {'id': 'ARC-999-乙', '到期章': 400, '状态': 'open'},
                                       'ARC-999-丙': {'id': 'ARC-999-丙', '到期章': 999, '状态': 'open'}},
              '改单': {'G9999-01': {'号': 'G9999-01', '状': '毕'}, 'G9999-02': {'号': 'G9999-02', '状': '开'}}}
        K = dict(账=账, 末=410)
        R.append(('①无器之裁判未生效', 查([a], 在役='', **K)[0][1] == '无一样器守它'))
        R.append(('②有器而未接进全测者判未生效', bool(查([b], 在役='', **K))))
        R.append(('③有器且在役者过', 查([c], 在役='工具/分量闸.py', **K) == []))
        e = os.path.join(d, '裁_0999_假名.md'); io.open(e, 'w', encoding='utf-8').write('由 `工具/并不存在之器.py` 守。')
        R.append(('④点名不存在之器不算（⛔不许写个假名混过）',
                  查([e], 在役='并不存在之器.py', **K) == [('裁_0999_假名.md', '无一样器守它')]))
        g = os.path.join(d, '裁_0999_随汰.md'); io.open(g, 'w', encoding='utf-8').write('〔随汰·1027：所守之法 `工具/接坐记.py` 已彻删〕')
        h = os.path.join(d, '裁_0999_借标.md'); io.open(h, 'w', encoding='utf-8').write('〔随汰·1027：所守之法 `工具/分量闸.py` 已彻删〕')
        h2 = os.path.join(d, '裁_0999_借名.md'); io.open(h2, 'w', encoding='utf-8').write('〔随汰·1027：所守之法 `工具/并不存在之器.py` 已彻删〕')
        R.append(('⑤随汰（所守之器 git 史中真已彻删·接坐记）之裁退役、⛔计未生效', 查([g], 在役='', **K) == []))
        R.append(('⑥⛔借标：随汰所点之器仍在者照旧判', 查([h], 在役='', **K) != []))
        _删 = 删过之器(ROOT)
        R.append(('⑥之二⛔借名：随汰所点之名从未有过（不在盘上≠已删）者照旧判（git 史验不得时略）',
                  _删 is None or 查([h2], 在役='', **K) != []))
        # ⑥之三〔W908 环7 复核〕借标续命：随汰之标内所点之在役之器⛔算守；标外者照算
        _标 = '〔随汰·1119：所守之法 `工具/并不存在之器.py` 已彻删——其守归 重出趋.py〕'
        R.append(('⑥之三⛔借标续命：〔随汰〕标内所点之器（重出趋.py）⛔算守；标外所点者（分量闸.py）照算',
                  守器(_标) == set() and 守器(_标 + '由 `工具/分量闸.py` 守。') == {'分量闸.py'}))
        # ⑦ 1027·#75 行之证：1027 起之裁只点器（在役）即判未生效；书真行之证即过；伪证俱⛔
        def 新(名, 文):
            p = os.path.join(d, '裁_1028_%s.md' % 名); io.open(p, 'w', encoding='utf-8').write(文); return p
        R.append(('⑦1027 起之裁只点在役之器而无行之证 → 未生效（裁_1020_D1落式 之形：点器而其实未行）',
                  bool(查([新('只点', '由 `工具/分量闸.py` 守。')], 在役='工具/分量闸.py', **K))))
        R.append(('⑦之二 放行：法用#<册中之法>、改单#<已结>、到期账 <已结或未到限> 俱算行之证',
                  查([新('法', '其证：法用#假法')], 在役='', **K) == [] and 查([新('改', '改单#G9999-01 施之')], 在役='', **K) == []
                  and 查([新('结', '到期账 ARC-999-甲 已结')], 在役='', **K) == [] and 查([新('待', '到期账 ARC-999-丙 限 999')], 在役='', **K) == []))
        R.append(('⑦之三 伪证俱⛔：册无之法、未结之改单、到限未结之到期账、账无之笔',
                  all(bool(查([新(n, 文)], 在役='', **K)) for n, 文 in (('伪法', '法用#无此法'), ('开单', '改单#G9999-02'),
                                                                     ('欠', '到期账 ARC-999-乙'), ('无笔', '到期账 ARC-999-丁')))))
        def 跨(名, 文):
            p = os.path.join(d, 名); io.open(p, 'w', encoding='utf-8').write(文); return p
        R.append(('⑦之四 跨年（1027 治）：旧式「裁_0105_」即红（须书 YYYYMMDD）；「裁_20270105_」照 1027 之律判（只点器 → 未生效、书行之证 → 过）',
                  any('YYYYMMDD' in x[1] for x in 查([跨('裁_0105_跨.md', '其证：法用#假法')], 在役='', **K))
                  and bool(查([跨('裁_20270105_只点.md', '由 `工具/分量闸.py` 守。')], 在役='工具/分量闸.py', **K))
                  and 查([跨('裁_20270105_有证.md', '其证：法用#假法')], 在役='', **K) == []))
        # ⑧ 0924—1026 过渡：只点器而无行之证入「只点」（⛔入坏）；书行之证即出
        只 = []
        p8 = os.path.join(d, '裁_0930_过渡.md'); io.open(p8, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。')
        p9 = os.path.join(d, '裁_0930_有证.md'); io.open(p9, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。改单#G9999-01')
        R.append(('⑧0924—1026 之裁只点器：入「只点」之数、⛔入未生效；带行之证者⛔入',
                  查([p8, p9], 在役='工具/分量闸.py', 只点=只, **K) == [] and [x[0] for x in 只] == ['裁_0930_过渡.md']))
        # ⑨ 判：只点器之底只许降；旧裁未生效至限章须 0
        ok1, _, 底1 = 判([], [('裁_0930_甲.md', 'x'), ('裁_0930_乙.md', 'x')], {'旧裁未生效之底': 0, '只点器之底': 1}, 410)
        ok2, _, 底2 = 判([], [('裁_0930_甲.md', 'x')], {'旧裁未生效之底': 0, '只点器之底': 2}, 410)
        R.append(('⑨只点器之数逾其底即红；降则底随降', ok1 is False and ok2 is True and 底2['只点器之底'] == 1))
        ok3, _, _ = 判([('裁_0916_旧.md', '无一样器守它')], [], {'旧裁未生效之底': 1, '只点器之底': 0}, 420)
        ok4, _, _ = 判([('裁_0916_旧.md', '无一样器守它')], [], {'旧裁未生效之底': 1, '只点器之底': 0}, 419)
        R.append(('⑨之二 限章：旧裁未生效 1 份於第 420 章即红、419 照棘轮不红（#56）', ok3 is False and ok4 is True))
        ok5, _, _ = 判([('裁_1028_新.md', '无行之证')], [], {'旧裁未生效之底': 0, '只点器之底': 0}, 410)
        R.append(('⑨之三 1027 起之裁未生效即红（⛔借棘轮）', ok5 is False))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # ⑩ 回灌真仓：裁_1020_D1落式（只点 行号随移.py 等）若照 1027 之律判，即未生效——证此律真红（⛔空验）
    #   〔W908 环7〕其裁已〔随汰〕（行号随移.py 彻删）：回灌之本并去其随汰之标（⛔借退役而空验）；⑩之二 验真档随汰即退役
    p = os.path.join(ROOT, '设定', '裁_1020_D1落式.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8').read()
        t1 = re.sub(r'〔随汰[^〕]*〕', '', re.sub(r'改单#\s*G\d{4}-\d{2}', '', t))
        _删10 = 删过之器(ROOT)
        _汰10 = 随汰(t)
        R.append(('⑩之二 裁_1020_D1落式带〔随汰〕：其器（%s）git 史中已删即退役、⛔计未生效（史验不得或未提交其删者略）' % (_汰10 or '—'),
                  ('〔随汰' in t) and (_删10 is None or '行号随移.py' not in _删10 or (_汰10 == '行号随移.py' and 查([p], 末=410) == []))))
        q = tempfile.mkdtemp()
        try:
            f = os.path.join(q, '裁_1028_D1落式之回灌.md'); io.open(f, 'w', encoding='utf-8').write(t1)
            R.append(('⑩回灌真仓：裁_1020_D1落式去其改单之引、照 1027 之律判 → 未生效（只点器不算）', bool(查([f], 末=410))))
        finally:
            shutil.rmtree(q, ignore_errors=True)
    else:
        R.append(('⑩回灌真仓：裁_1020_D1落式不在', False))
    # ⑩之三〔W908 环7 复核〕0919／0922 看官账四裁：带〔随汰〕点 看官欠哨.py；其删入 git 史即退役（未提交其删、或史验不得者略）
    _看 = [os.path.join(ROOT, '设定', n) for n in ('裁_0919_看官账263_342至344之重出.md', '裁_0919_看官账_345至347之重出.md',
                                                  '裁_0922_看官账_逾353三笔_按串长分判.md', '裁_0922_看官账_限354八笔_按串长分判.md')]
    _看在 = [x for x in _看 if os.path.exists(x)]
    _删看 = 删过之器(ROOT)
    R.append(('⑩之三 看官账四裁（在 %d）带〔随汰〕点 `工具/看官欠哨.py`；其删入 git 史即退役、⛔计未生效（未提交其删者略）' % len(_看在),
              len(_看在) == 4 and all('〔随汰' in io.open(x, encoding='utf-8').read() and '`工具/看官欠哨.py`' in io.open(x, encoding='utf-8').read() for x in _看在)
              and (_删看 is None or '看官欠哨.py' not in _删看 or 查(_看在, 末=410) == [])))
    for n, o in R:
        print('  %s %s' % ('✓' if o else '⛔', n))
    k = sum(1 for _, o in R if o)
    print('  ── 裁之生效·自测 %d/%d %s ──' % (k, len(R), '全通' if k == len(R) else '⛔未过'))
    return k == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
