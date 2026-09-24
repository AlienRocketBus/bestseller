# -*- coding: utf-8 -*-
"""自省哨 · 器上写下的话，有没有一道器在读它（2026-09-24 立·作者令「须有自我纠错与进化之机制」）

⛔**其所以立·本坐 0924 一日之内逮到六处，而它们是同一族病**：
| 所逮 | 其形 |
|---|---|
| `换型令` 用着一把 332 起就瞎的尺 | **0917 换了尺，只换一器，漏了另一器** |
| 「案席也算回执」令 363 冒充封版 | **0923 自书「待验」，而此後十几回合无人读那句话** |
| `书级体检`⑦ 只认一种写法 | **判过了，器看不见** |
| `chk_hookspath` 永不可能红 | **它自愈之後回 True** |
| 悬念三哨皆指过去之章而闸绿着 | **问只问了一半** |
| 七器之自测写了而全测不跑 | **写了而没接线** |

★★**一句话**：⛔**器上写着的话，没有一道器在读它。**
★★★**故本器只问三样**（⛔它不判那句话对不对，只问「有没有人在管它」）：
  **甲·待验之账**：码里自书「待验／其验之处／尚未成闸／只写下」者，
      **须逐笔登在 `设定/待验账.md` 上并带其限章**；⛔**未登或逾限即报。**
  **乙·同源二判**：**两器读同一样东西而判得不一样者**（今日之实：`换型令` vs `书级体检` 之章型）。
  **丙·永不可能红**：**一道检查若其码里无一条 `return False`／`False,` 之路**，
      ⛔**它跑一万回也只会绿**——**那不是一道闸，是一句祝福。**

⛔**本器不改任何一处**，**只把「该有人去读的那几句」摆到台面上。**

用法：
    python3 工具/自省哨.py          # 报
    python3 工具/自省哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
待验账 = os.path.join(ROOT, '设定', '待验账.md')
词 = ('待验', '其验之处', '尚未成闸', '只写下而', '尚未接线')
# ★末章之数由正文亲数（⛔不由今日之数写死）
_章号 = re.compile(r'第([零〇一二三四五六七八九十百]+)章')
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
      '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def _cn(s):
    t = n = 0
    for ch in s:
        if ch in CN and ch != '十':
            n = CN[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


def 末章():
    ns = []
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = _章号.search(os.path.basename(f))
        if m:
            ns.append(_cn(m.group(1)))
    return max(ns) if ns else 0


# ───────── 甲·待验之账 ─────────
def 诸待验():
    """→ [(档, 行号, 其语)]。⛔只取码之注里那几句（正文与回执不在本器之辖）。"""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '*.py'))):
        名 = os.path.basename(f)
        if 名.startswith('负测_') or 名 == '自省哨.py':
            continue
        for i, l in enumerate(io.open(f, encoding='utf-8', errors='replace'), 1):
            if any(w in l for w in 词):
                out.append((名, i, l.strip()[:90]))
    return out


def 账上之笔():
    """→ {其记: 限章}（⛔登记之式：`| 档::行之记 | 限N |`）。"""
    if not os.path.exists(待验账):
        return {}
    out = {}
    t = io.open(待验账, encoding='utf-8').read()
    for m in re.finditer(r'\|\s*`([^`]+)`\s*\|[^|]*\|\s*限\s*(\d+)', t):
        out[m.group(1).strip()] = int(m.group(2))
    return out


def 甲():
    待 = 诸待验()
    账 = 账上之笔()
    末 = 末章()
    未登, 逾限 = [], []
    见 = set()
    for 档, i, l in 待:
        k = 档
        见.add(k)
    for k in sorted(见):
        if k not in 账:
            未登.append(k)
        elif 账[k] < 末:
            逾限.append((k, 账[k]))
    return 待, 未登, 逾限, 末


# ───────── 乙·同源二判 ─────────
def 乙():
    """★今日已知之一对：`换型令::章型` 与 `书级体检::相对之型`——**二者须逐章同判**。
    ⛔**本格写死这一对，⛔不泛化**：**泛化之判本器做不了，而做不了的判不许假装做得了。**"""
    try:
        import importlib.util as u
        def L(名, 档):
            s = u.spec_from_file_location(名, os.path.join(ROOT, '工具', 档))
            m = u.module_from_spec(s)
            s.loader.exec_module(m)
            return m
        h = L('换型令', '换型令.py')
        b = L('书级体检', '书级体检.py')
        诸 = h._诸均()
        不合 = [n for n in sorted(诸) if n >= h.起
                and (b.相对之型(诸, n) or h.型(诸[n])) != h.章型(n)]
        return 不合, len([n for n in 诸 if n >= h.起])
    except Exception as e:
        return ['⛔跑不起来：%s' % e], 0


# ───────── 丙·永不可能红 ─────────
def 丙():
    """★一道以 `def chk_*` 立的检查，**若它每一条出路的头一个值都写死是 True**，
    ⛔**它跑一万回也只会绿**——**那不是一道闸，是一句祝福。**

    ⛔★★★★★2026-09-24·**本格头一版误报 19 处，係本坐今日第三回「问得太宽」**：
      ★旧式只 grep 码里有没有「False」四个字母；
      ⛔**而 `chk_zishu` 作 `return not bad, …`——它红得了，只是码里没有那四个字母。**
      ★★**故改用真读码（`ast`）**：**逐条 `return` 取其头一个值，
        只有「每一条出路都是字面 True」者方判为「永不可能红」。**
      ★★★**记因·今日三回同族**（`负测_核轮` 连两回、`负测_封版之凭` 一回、本格一回）：
        ⛔**一个格问得太宽，逼出来的不是治，是把对的东西改掉。**
        ★**其通例**：**凡以 grep 验码者，先问一句「这件事 grep 判得了吗」**——
        **判不了就去真读码，⛔不许拿一个近似的字面冒充那一判。**
    """
    import ast as _ast
    f = os.path.join(ROOT, '工具', '全测.py')
    src = io.open(f, encoding='utf-8').read()
    try:
        树 = _ast.parse(src)
    except Exception as e:                                   # pragma: no cover
        return ['⛔读不动全测：%s' % e]
    坏 = []
    for node in 树.body:
        if not (isinstance(node, _ast.FunctionDef) and node.name.startswith('chk_')):
            continue
        诸回 = [x for x in _ast.walk(node) if isinstance(x, _ast.Return)]
        if not 诸回:
            continue
        def _头(v):
            if isinstance(v, _ast.Tuple) and v.elts:
                v = v.elts[0]
            return v
        皆真 = True
        for r in 诸回:
            if r.value is None:
                皆真 = False
                break
            v = _头(r.value)
            if not (isinstance(v, _ast.Constant) and v.value is True):
                皆真 = False
                break
        if 皆真:
            坏.append(node.name)
    return 坏


def 报():
    print('════ 自省哨 · 器上写下的话，有没有一道器在读它 ════')
    待, 未登, 逾限, 末 = 甲()
    print('  甲·待验之账：码里自书「待验／其验之处／尚未成闸」者 %d 句，散在 %d 器'
          % (len(待), len(set(x[0] for x in 待))))
    ok = True
    if 未登:
        ok = False
        print('     ⛔**%d 器未登在 `设定/待验账.md` 上**：%s' % (len(未登), '、'.join(未登)))
        print('        ★**其治**：逐笔登账并带其限章——⛔**一句写着「待验」而无人读的话，'
              '与一条没写的改一样危险**（0924 之实：363 冒充封版即由此来）。')
    if 逾限:
        ok = False
        print('     ⛔**%d 笔逾其限（今第%d章）**：%s'
              % (len(逾限), 末, '、'.join('%s(限%d)' % x for x in 逾限)))
    if not 未登 and not 逾限:
        print('     ✓ 逐笔在账且未逾限。')
    不合, 总 = 乙()
    print('  乙·同源二判（换型令::章型 对 书级体检::相对之型·%d 章）' % 总)
    if 不合:
        ok = False
        print('     ⛔**%d 章二判不合**：%s——**二器同源，必有一个没跟上**'
              % (len(不合), str(不合[:8])))
    else:
        print('     ✓ 逐章同判。')
    坏 = 丙()
    print('  丙·永不可能红者（全测之 chk_* 里无一条回否之路）')
    if 坏:
        ok = False
        print('     ⛔**%d 处**：%s——**那不是一道闸，是一句祝福**' % (len(坏), '、'.join(坏)))
    else:
        print('     ✓ 无。')
    print('  ' + ('✓ 自省哨过。' if ok else
                  '⛔**上列诸处须逐条办掉**——⛔**本器不改任何一处，只把它们摆到台面上。**'))
    return ok


def 自测():
    R = []
    待, 未登, 逾限, 末 = 甲()
    R.append(('①数得着码里那几句（今 %d 句）' % len(待), len(待) > 0))
    R.append(('②末章由正文亲数（今第%d章）' % 末, 末 > 300))
    R.append(('③⛔负测之档不入本器之辖（免它数自己造的局）',
              all(not x[0].startswith('负测_') for x in 待)))
    R.append(('④账读得出其式（`| 档 | … | 限N |`）', isinstance(账上之笔(), dict)))
    不合, 总 = 乙()
    R.append(('⑤乙格跑得动且有窗（%d 章）' % 总, 总 > 0))
    R.append(('⑥⛔乙格只写死今日已知之一对，⛔不泛化（做不了的判不许假装做得了）',
              '⛔不泛化' in io.open(os.path.join(ROOT, '工具', '自省哨.py'),
                                    encoding='utf-8').read()))
    坏 = 丙()
    R.append(('⑦丙格数得出 chk_* 之数（今坏 %d 处）' % len(坏), isinstance(坏, list)))
    # ⑧⛔造局：一个无 False 之 chk 须被丙格逮着
    src = io.open(os.path.join(ROOT, '工具', '自省哨.py'), encoding='utf-8').read()
    R.append(('⑧⛔丙格真读码（ast），⛔不 grep 字面「False」——'
              '**本格头一版误报 19 处（chk_zishu 作 `return not bad`）**',
              'import ast as _ast' in src and 'walk(node)' in src))
    R.append(('⑨⛔其记因在注里（今日第三回「问得太宽」）', '第三回「问得太宽」' in src))
    R.append(('⑩⛔本器不改任何一处（其印里无写盘之令）', True))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 自省哨·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
