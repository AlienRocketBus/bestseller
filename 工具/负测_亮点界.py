# -*- coding: utf-8 -*-
"""负测·亮点界 · 2026-09-05 立（与 工具/亮点界.py 同日·令§六③）
　★要害不在「会不会报红」，在四样：
　　①**以旧式回灌**：拿 fe37e08f 之前的 133／134（治前之原物·133 亮点里 2963 字讲的是 134 的正文）
　　　灌回去，须逮出越界，且越界之句须落在 133 那一头；
　　②**非陪跑**：把八字窗换成「整句逐字相同才算命中」（旧式），同一份原物只逮得出 42 句 1236 字，
　　　而八字窗逮得出 80 句 2365 字——**窗不是装饰，去掉它这一案有一半看不见。**
　　　（记一笔：本席头一版把②写成「旧式当场一句也逮不出」，跑出来是 42 句，**判词错了**；
　　　　这一条不是把测试改成过得去，是把话改成真的。）
　　③**非挖空**：现文 23 对全绿（例外那一条另计，不作红）；
　　④**不吃盘**：此器只读不写，跑完全书之後诸档逐字原样。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, subprocess, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 亮点界 as B                                        # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
提交 = 'fe37e08f^'


def 旧本(n):
    rel = os.path.relpath(章[n], 根)
    return subprocess.run(['git', '-C', 根, 'show', '%s:%s' % (提交, rel)],
                          capture_output=True).stdout.decode('utf-8')


def 验(a, b, 文):
    """与 亮点界.验一对 同法，只是正文自 文{} 取而不自盘取。"""
    体, 亮 = {}, {}
    for n in (a, b):
        x, y = (文[n].split('【本章亮点】', 1) + [''])[:2] if '【本章亮点】' in 文[n] else (文[n], '')
        体[n], 亮[n] = B.剥(x), y
    出 = []
    for 我, 邻 in ((a, b), (b, a)):
        for s in B.切句(亮[我]):
            g = B.剥(s)
            if len(g) < B.最短:
                continue
            if B.命中(g, 体[我]) == 0 and B.命中(g, 体[邻]) > 0:
                出.append((我, s))
    return 出


sha0 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 章.items()}

旧 = {133: 旧本(133), 134: 旧本(134)}
t('①旧本取得着（fe37e08f^ 之 133／134 皆非空）', all(len(v) > 500 for v in 旧.values()), True)
出 = 验(133, 134, 旧)
t('①回灌·治前之 133／134 逮得出越界', len(出) > 0, True)
t('①之二·越界之句落在 133 那一头', sorted({我 for 我, _ in 出}), [133])

# ②非陪跑：旧式（整句逐字相同才算命中）对同一份原物零报
def 旧式(a, b, 文):
    体, 亮 = {}, {}
    for n in (a, b):
        x, y = (文[n].split('【本章亮点】', 1) + [''])[:2] if '【本章亮点】' in 文[n] else (文[n], '')
        体[n], 亮[n] = B.剥(x), y
    出 = []
    for 我, 邻 in ((a, b), (b, a)):
        for s in B.切句(亮[我]):
            g = B.剥(s)
            if len(g) < B.最短:
                continue
            if g not in 体[我] and g in 体[邻]:
                出.append((我, s))
    return 出

旧出 = 旧式(133, 134, 旧)
t('②非陪跑·八字窗比「整句逐字相同」多逮一倍（新 %d 句 %d 字／旧 %d 句 %d 字）'
  % (len(出), sum(len(x[1]) for x in 出), len(旧出), sum(len(x[1]) for x in 旧出)),
  len(出) >= len(旧出) * 1.5, True)

# ③非挖空：现文 23 对全绿（例外不计红）
新红 = 0
for a, b in B.诸对():
    r = B.验一对(a, b, 章)
    新红 += len([x for x in r if not x[5]])
t('③现文 %d 对零越界（已裁之例外不计）' % len(B.诸对()), 新红, 0)

# ④不吃盘
sha1 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 诸章().items()}
t('④跑完全书诸档逐字原样', sha1, sha0)

print('════ 负测·亮点界 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:80], str(期)[:80])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·亮点界 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
