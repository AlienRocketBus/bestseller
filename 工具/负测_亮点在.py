# -*- coding: utf-8 -*-
"""负测·亮点在 · 2026-09-06 立（与 工具/亮点在.py 同日·令§六③）
　★要害不在「会不会报红」，在四样：
　　①**以旧式回灌**：拿 6d8dee47（此器立成之前）之 280 原物——那时它一段骨记也没有——
　　　新器须当场判红；
　　②**非陪跑**：**旧式对同一份原物报的是绿**。`工具/亮点对表.py` 三路皆以
　　　`if '【本章亮点】' not in txt: return` 开头，无段即空过；
　　　`工具/起草闸.py` 甲层照抄其判，於是「整段不在」这一样，全书的器**一个也逮不着**。
　　　此条即「绿而不实」之第五种：不是没位、不是看不见、不是没接进那一句，
　　　是**遇上「整样东西不在」的时候，它是空过，不是判红**。
　　③**非挖空**：今版须全绿，且其群不得塌（109 以後 ≥197 章）；
　　　并须证「恰一段者绿」——不是一律判红换来的绿。
　　④**不吃盘**：此器只读不写，跑完诸档逐字原样。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys, subprocess, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 亮点在 as L                                        # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
锚 = '6d8dee47'          # 此器立成之前——280—283 四章皆无骨记
sha0 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 章.items()}
tmp = os.path.join(根, '工具', '_负测亮点在_tmp.md')

# ①旧物回灌：280 之旧本，新器须判红
r = subprocess.run(['git', '-C', 根, 'show', '%s:%s' % (锚, os.path.relpath(章[280], 根))],
                   capture_output=True)
旧280 = r.stdout.decode('utf-8')
io.open(tmp, 'w', encoding='utf-8').write(旧280)
红, 群 = L.量({280: tmp})
t('①回灌 %s 之 280（其时无骨记），新器判红' % 锚, [(n, c) for n, c, _ in 红], [(280, 0)])
t('①之二·而那一档确是本书正文（不是空档）', len(旧280) > 3000, True)

# ②非陪跑：旧式（亮点对表之三路）对同一份原物一处也报不出
r2 = subprocess.run([sys.executable, '工具/亮点对表.py', '280'], capture_output=True, cwd=根)
out2 = (r2.stdout + r2.stderr).decode('utf-8', 'replace')
t('②旧式之判据即「有没有这一段」，无段即 return——故 280 之旧本在旧式底下零报红',
  '⛔' in out2, False)
t('②之二·旧式之空过是写在码里的（三路皆以此句起手）',
  io.open(os.path.join(根, '工具', '亮点对表.py'), encoding='utf-8').read()
  .count("if '【本章亮点】' not in") >= 3, True)

# ③非挖空
红今, 群今 = L.量()
t('③今版 109 以後零章缺骨记', [(n, c) for n, c, _ in 红今], [])
# ★2026-09-08·案席：旧式把群写死作 197，於是每写一章新章此负测即败一回——
#   而其所守者是「群不得塌」，不是「群不许长」。故改为下限。
t('③之二·其群不得塌（109 以後 ≥197 章）', 群今 >= 197, True)
io.open(tmp, 'w', encoding='utf-8').write('正文\n【本章亮点】\n①一层\n')
t('③之三·恰一段者绿（这个绿不是一律判红换来的）', L.量({306: tmp}), ([], 1))
os.remove(tmp)

# ④不吃盘
sha1 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 诸章().items()}
t('④跑完诸档逐字原样', sha1, sha0)

print('════ 负测·亮点在 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:70], str(期)[:70])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·亮点在 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
