# -*- coding: utf-8 -*-
"""负测 · 换型令之尺（2026-09-24 立·同日负测·令§一⑤）

⛔**其所验者，正是本坐今日最须被人盯着的那一改**：
  **本坐把 `换型令` 之尺由「绝对四档」换成「相对之型」，而那一换令十五条红当场消失，
  并解开了一道拦了本坐六天的推闸。**
★★**故本测头一件事不是证它绿，是证它「不是一路放绿」**：
  ①**旧尺回灌**：旧尺於真盘上红 15 章（其数逐章列出），新尺不红——**二者判得不一样，本测非陪跑**；
  ②**造一本「真的一成不变」之局**：新尺照旧当场红——⛔**换尺不是把眼睛闭上**；
  ③**限已由 12 收紧到 6**，且**旧尺一个字未删**（係窗不足八章时之退路）。
⛔本负测造局不动真盘一个字；点真盘者只作注。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器(名, 档):
    s = _u.spec_from_file_location(名, os.path.join(ROOT, '工具', 档))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def 跑():
    m = _器('换型令', '换型令.py')
    R = []
    诸均 = m._诸均()
    封 = set(n for n in 诸均 if m.封了版(n))

    # ①⛔旧尺回灌：以绝对四档判型，真盘上当场红 15 章
    旧诸 = dict((n, m.型(v)) for n, v in 诸均.items())
    旧红 = m.查(旧诸, 封版者=封, 认={})
    旧章 = sorted(n for n, _, _ in 旧红)
    R.append(('①⛔旧尺（绝对四档）回灌：真盘上红 %d 章%s'
              % (len(旧红), '（%d—%d）' % (旧章[0], 旧章[-1]) if 旧章 else ''),
              len(旧红) >= 15))
    R.append(('①之二·旧尺之红係 345—359 那十五章（⛔即六天推不上去的那一条）',
              set(旧章) >= set(range(345, 360))))

    # ②新尺於同一份正文上不红（⛔而其所以不红，是那十五章之型本来就在变）
    新诸 = dict((n, m.章型(n)) for n in 诸均)
    新红 = m.查(新诸, 封版者=封, 认={})
    R.append(('②新尺於同一份正文上不红（今 %d 章）' % len(新红), not 新红))
    型们 = [新诸[n] for n in range(345, 360) if n in 新诸]
    R.append(('②之二·⛔其所以不红，是那十五章之型本来就在变：%s（%d 种）'
              % ('／'.join(型们), len(set(型们))), len(set(型们)) >= 3))

    # ③⛔造一本「真的一成不变」之局：新尺照旧当场红
    局 = dict((n, '窄') for n in range(331, 350))
    局红 = m.查(局, 封版者=set(局), 认={})
    R.append(('③⛔造局·连 19 章同型（皆已封版），新尺当场侦得 %d 章——'
              '**换尺⛔不是把眼睛闭上**' % len(局红), len(局红) > 0))
    # ③之三〔1119 死规之审·gates12〕侦得者只印 ⚠、全书 rc 0（⛔再拦推）
    import contextlib
    _buf = io.StringIO()
    with contextlib.redirect_stdout(_buf):
        _rc = m.全书(诸=局, 封版者=set(局))
    R.append(('③之三·〔1119·gates12〕同局全书 rc 0，其 %d 章逐章印 ⚠（只报）' % len(局红),
              _rc == 0 and _buf.getvalue().count('⚠第') == len(局红) and '⛔第' not in _buf.getvalue()))
    局2 = dict((n, '窄' if n % 3 else '宽') for n in range(331, 350))
    R.append(('③之二·同样十九章而型在变者不红（⛔证③非一律判否）',
              not m.查(局2, 封版者=set(局2), 认={})))

    # ④限已收紧，且其据係亲数
    src = io.open(os.path.join(ROOT, '工具', '换型令.py'), encoding='utf-8').read()
    R.append(('④⛔限 == 6（由旧式之 12 收紧一倍）', m.限 == 6))
    R.append(('④之二·码上係常量，⛔不由今日之数算出',
              re.search(r'^限 = 6\b', src, re.M) is not None))
    R.append(('④之三·⛔「严限／严自」那一自相矛盾之层已撤（8 比 6 松）',
              '严限' not in src.split('"""')[0] + src.split('def 查')[1]))
    R.append(('④之四·⛔旧尺一个字未删（`型()` 照旧在役，係窗不足八章之退路）',
              m.型(10) == '短' and m.型(18) == '中' and m.型(30) == '长'))

    # ⑤⛔窗不足八章者退回旧尺（⛔不许拿三五个数去分四档）
    R.append(('⑤窗不足八章者退回旧尺（造局：只六章）',
              _器('书级体检', '书级体检.py').相对之型(
                  dict((n, float(n)) for n in range(1, 7)), 6) is None))

    # ⑥两器今日同尺（⛔0917 那一改漏了本器，正是六天之根）
    体 = _器('书级体检', '书级体检.py')
    同 = [n for n in range(340, 364)
          if n in 诸均 and (体.相对之型(诸均, n) or 体.sig_of('')[0]) == 新诸.get(n)]
    R.append(('⑥340—363 两器逐章同型（⛔0917 那一改只换了一器之尺，正是六天之根）',
              len(同) >= 20))

    # ⑦真盘（只作注）
    R.append(('⑦真盘·今窗（起%d）内最长同型链 4 章（窄·347—350），而限 %d'
              % (m.起, m.限), True))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·换型令之尺 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
