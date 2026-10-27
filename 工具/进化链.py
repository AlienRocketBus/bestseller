# -*- coding: utf-8 -*-
"""进化链 · 犯过的每一个错，今天有没有一道器在守着（2026-09-24 立·作者令）

⛔**作者原令之要**：「**曾经犯过的错误，之後不能再犯，要一个完整的进化链……
  我们的每一个机制，不论是什么样的机制，都要进化得越来越好。**」

★**盘上早记着很多错**——**只是散在四处，没有一条链串起来，也没有一道器问「今天谁在守它」**：
  `设定/机制体检账.md`（177 大节·通例一至七〇）｜`设定/裁_*.md`（60 份）｜`设定/册_*.md`｜`设定/病族账.md`。
⛔**而令九·③ 早有一句：「写下来的法不生效，只有变成闸才生效。」**
  **一条只写在纸上、没有器守着的教训，下一坐照样会再犯**——**0924 之「待验无人读」即如此。**

★★**故本器做三件，皆判得死**：
  ①**串链**：把四处之教训逐环列成一条链（日期、一句之教、出处、守它的器），**写成 `设定/进化链.md`**；
  ②**问守**：**每一环有没有提到一道盘上真存在的器或负测**——⛔**提到而盘上不在者，不算守**；
  ③**棘轮**：**「无守之环」之数只许往下走，⛔不许往上涨**（其底在 `设定/进化链_棘轮.json`）——
    **新添一条教训而不给它配一道器，棘轮当场红**；**给一条旧教训配上了器，底自动下移**。
    ★**这就是「每一个机制都要进化得越来越好」之可数的那一半：它只能变好，不能变坏。**

⛔**本器之限（写死，不许假装做得到）**：**它判得了「有没有器守着」，⛔判不了「那道器守得住守不住」**
  ——**後一件归各器之负测（头一格须旧式回灌）。**

用法：
    python3 工具/进化链.py           # 串链、写 设定/进化链.md、过棘轮
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
    且其所点之器**真已不在盘上**，方认（器仍在即⛔认：防借此标关闸）。→ 其器之名，或 ''。"""
    m = re.search(r'〔随汰[^〕]*`工具/([^`]+)`[^〕]*〕', s)
    if not m:
        return ''
    return m.group(1) if not os.path.exists(os.path.join(root or ROOT, '工具', m.group(1))) else ''


def 诸环():
    """→ [{源, 名, 日, 守}]。"""
    有 = _诸器()
    环 = []
    # 一·体检账之大节
    p = os.path.join(ROOT, '设定', '机制体检账.md')
    if os.path.exists(p):
        t = io.open(p, encoding='utf-8').read()
        节 = re.split(r'\n(?=## )', t)
        for s in 节:
            if not s.startswith('## '):
                continue
            题 = s.split('\n', 1)[0][3:].strip()
            环.append({'源': '体检账', '名': re.sub(r'\*', '', 题)[:70],
                       '日': _日(题 + s[:400]), '守': _守(s, 有), '汰': 随汰(s)})
    # 二·裁与册
    for f in sorted(glob.glob(os.path.join(ROOT, '设定', '裁_*.md'))
                    + glob.glob(os.path.join(ROOT, '设定', '册_*.md'))):
        t = io.open(f, encoding='utf-8', errors='replace').read()
        题 = (t.split('\n', 1)[0].lstrip('# ').strip() or os.path.basename(f))
        环.append({'源': os.path.basename(f)[:40], '名': re.sub(r'\*', '', 题)[:70],
                   '日': _日(os.path.basename(f) + t[:300]), '守': _守(t, 有), '汰': 随汰(t)})   # ★1027：裁／册亦认随汰
    # 三·病族
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


def 写链(环):
    汰 = [x for x in 环 if x.get('汰')]
    环 = [x for x in 环 if not x.get('汰')]
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


def 跑(写=True):
    环 = 诸环()
    有, 无 = (写链(环) if 写 else (sum(1 for x in 环 if x['守'] and not x.get('汰')),
                                   sum(1 for x in 环 if not x['守'] and not x.get('汰'))))   # ★1027：dry 与写同计（汰者俱不计）
    底 = 读底()
    print('════ 进化链 · 犯过的每一个错，今天有没有一道器在守着 ════')
    print('  共 %d 环｜有守 %d｜⛔无守（只写在纸上）%d' % (len(环), 有, 无))
    if 底 is None:
        if 写:
            io.open(棘轮, 'w', encoding='utf-8').write(
                json.dumps({'无守之底': 无, '立於': '2026-09-24'}, ensure_ascii=False))
        print('  ★棘轮初立：无守之底 = %d（⛔此後只许往下走）' % 无)
        return True
    b = 底['无守之底']
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
    R = []
    有 = _诸器()
    R.append(('①盘上之器数得着（今 %d）' % len(有), len(有) > 100))
    R.append(('②⛔提到而盘上不在之器不算守',
              _守('见 `工具/并不存在的器.py`', 有) == []))
    R.append(('②之二·提到而在者算守', _守('见 `工具/存底.py`', 有) == ['存底.py']))
    R.append(('②之三·随汰：所点之器已不在方认（1017 淘汰之律）', 随汰('〔随汰·1017：所守之法 `工具/并不存在的器.py` 已彻删〕') == '并不存在的器.py'))
    R.append(('②之四·随汰：所点之器仍在即⛔认（防借标关闸）', 随汰('〔随汰·1017：所守之法 `工具/存底.py` 已彻删〕') == ''))
    环 = 诸环()
    R.append(('③串得出链（今 %d 环·体检账＋裁＋册＋病族）' % len(环), len(环) > 200))
    R.append(('④四处皆入链', {'体检账', '病族账'} <= set(x['源'] for x in 环)
              and any(x['源'].startswith('裁_') for x in 环)))
    # ★1027：裁、病族之环亦认随汰（旧只体检账认之——裁之所守彻删，其环只得作无守而涨棘轮）
    R.append(('④之二·裁与病族亦认随汰（今 裁 %d 环、病族 %d 环已汰）' % (
        sum(1 for x in 环 if x['源'].startswith('裁_') and x.get('汰')), sum(1 for x in 环 if x['源'] == '病族账' and x.get('汰'))),
              any(x['源'].startswith('裁_') and x.get('汰') for x in 环) and any(x['源'] == '病族账' and x.get('汰') for x in 环)))
    # ⑤⛔棘轮之牙：无守之数比底大即红
    import tempfile
    global 棘轮
    老 = 棘轮
    d = tempfile.mkdtemp(prefix='棘轮_')
    棘轮 = os.path.join(d, 'r.json')
    try:
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps({'无守之底': 0}))
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            ok = 跑(写=False)
        无 = sum(1 for x in 环 if not x['守'])
        R.append(('⑤⛔棘轮之牙：底设 0 而今无守 %d → 当场红' % 无, (ok is False) if 无 > 0 else True))
        io.open(棘轮, 'w', encoding='utf-8').write(json.dumps({'无守之底': 99999}))
        with contextlib.redirect_stdout(io.StringIO()):
            ok2 = 跑(写=False)
        R.append(('⑤之二·底比今大者不红（⛔证⑤非一律判否）', ok2 is True))
    finally:
        棘轮 = 老
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
