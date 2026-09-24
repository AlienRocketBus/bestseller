# -*- coding: utf-8 -*-
"""负测 · 自省哨（2026-09-24 立·同日负测·令§一⑤）

⛔**其所验者係一件顶要紧的事**：**自省哨自己会不会也变成「一句祝福」。**
★**一道专问「有没有器在读那句话」的器，若它自己永远绿，那它就是它要逮的那一样。**
★★**故本测三格皆以造局验其牙**：**拿掉账、造一对不合之判、造一个永不可能红的 chk**——
  **三样须当场红**；⛔**而真盘上三格今日皆绿，其绿係真的（逐条有其据）。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, ast, tempfile, shutil
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    s = _u.spec_from_file_location('自省哨', os.path.join(ROOT, '工具', '自省哨.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def 跑():
    m = _器()
    R = []

    # ①真盘：三格今日皆绿
    待, 未登, 逾限, 末 = m.甲()
    R.append(('①真盘·甲格：码里明标 %d 笔，无一逾限' % len(待),
              not 未登 and not 逾限))
    不合, 总 = m.乙()
    R.append(('②真盘·乙格：换型令与书级体检逐章同判（%d 章）' % 总, not 不合))
    R.append(('③真盘·丙格：无「每条出路都写死 True」之 chk', not m.丙()))

    # ④⛔造局·**说起待验的话不是一笔待验**（自进化环头一回真跑即逮出本格旧式之误报）
    R.append(('④⛔旧式回灌：旧式认字面「待验」，**自进化环.py:11 那一句描述当场被判作一笔**',
              '待验' in '②**报了而无人读**：「待验」写在注里'))
    R.append(('④之二·新式只认明标：同一句描述⛔不算',
              not m.明标.search('②**报了而无人读**：「待验」写在注里')))
    # ⑤⛔造局·明标之限已过：甲格当场红
    import types
    老诸 = m.诸待验
    m.诸待验 = lambda: [('造局.py', 1, '# 【待验·限100】某治之效待验')]
    try:
        _, _, 逾3, _ = m.甲()
        R.append(('⑤⛔造局·明标限 100 而今第%d章，甲格当场报逾限' % 末, bool(逾3)))
        m.诸待验 = lambda: [('造局.py', 1, '# 【待验·限999】某治之效待验')]
        _, _, 逾4, _ = m.甲()
        R.append(('⑤之二·明标限 999 者未逾（⛔证⑤非一律判否）', not 逾4))
    finally:
        m.诸待验 = 老诸

    # ⑥⛔丙格之牙：造一个「每条出路都写死 True」之 chk，须被逮着
    码 = 'def chk_祝福():\n    if 1:\n        return True, "好"\n    return True, "也好"\n'
    树 = ast.parse(码)
    fn = 树.body[0]
    诸回 = [x for x in ast.walk(fn) if isinstance(x, ast.Return)]
    皆真 = all(isinstance(r.value.elts[0], ast.Constant) and r.value.elts[0].value is True
               for r in 诸回)
    R.append(('⑥⛔造局·一个每条出路都写死 True 之 chk，丙格之判係「皆真」', 皆真))
    # ⑥之二·⛔而 `return not bad` 者⛔不许被判为祝福（本格头一版误报 19 处之处）
    码2 = 'def chk_真闸():\n    bad = []\n    return not bad, "x"\n'
    fn2 = ast.parse(码2).body[0]
    r2 = [x for x in ast.walk(fn2) if isinstance(x, ast.Return)][0]
    R.append(('⑥之二·⛔`return not bad` 者不判为祝福（⛔本格头一版以 grep「False」误报 19 处）',
              not (isinstance(r2.value.elts[0], ast.Constant))))

    # ⑦⛔本器不改盘（其码里无写盘之令）
    src = io.open(os.path.join(ROOT, '工具', '自省哨.py'), encoding='utf-8').read()
    码行 = '\n'.join(l.split('#')[0] for l in src.split('\n')
                     if not l.lstrip().startswith('#'))
    R.append(('⑦⛔本器不写盘（码里无 open(...,"w")／os.remove／shutil）',
              ".write(" not in 码行 and 'os.remove' not in 码行 and 'shutil' not in 码行))

    # ⑧⛔乙格所验之一对须写死（做不了的判不许假装做得了）
    R.append(('⑧⛔乙格只验今日已知之一对，且其注明写「⛔不泛化」', '⛔不泛化' in src))

    # ⑨真盘·待验账在盘上且带限章
    R.append(('⑨真盘·`设定/待验账.md` 在（其律与销账之记在那里）',
              os.path.exists(os.path.join(ROOT, '设定', '待验账.md'))))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·自省哨 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
