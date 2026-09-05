# -*- coding: utf-8 -*-
"""负测·息日链 · 2026-09-05 立（与 工具/息日链.py 同日·令§六③）
　★要害不在「会不会报红」，在四样：
　　①**以旧式回灌·正文那一路**：把 114 之息日退回「第十二天」（0905 治前之原物），须报红；
　　②**以旧式回灌·施工表那一路**：把施工表 106／107／108／109／110／111／113／115 八行的息日
　　　各退回治前之数（一律少一，差 18），须报红，且**八行一行不漏**；
　　③**非陪跑**：若只问「有没有这两个数」而不问差，同一份原物一处也报不出；
　　④**非挖空**：现文须全绿，且跑完之後两档逐字原样（此器要改档回灌，改完必须写回）。
"""
import io, os, re, sys, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 息日链 as X                                        # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
p114 = 章[114]
表 = X.表

def _sha(p):
    return hashlib.sha256(io.open(p, 'rb').read()).hexdigest()

原114, 原表 = io.open(p114, encoding='utf-8').read(), io.open(表, encoding='utf-8').read()
sha0 = (_sha(p114), _sha(表))

# 治前之施工表八行（皆比正文少一）
旧行 = [('息九第七日', '息九第六日'), ('息九第八日', '息九第七日'), ('息九第九日', '息九第八日'),
        ('息九第十日', '息九第九日'), ('息九第十一日', '息九第十日'), ('息九第十二日', '息九第十一日'),
        ('息九第十三日', '息九第十二日'), ('息第十四日', '息第十三日')]

try:
    # ①正文那一路
    io.open(p114, 'w', encoding='utf-8').write(原114.replace('第十三天，九。', '第十二天，九。', 1))
    t('①旧式回灌·114 息日退回第十二天须报红', X.跑(报=False) > 0, True)
    io.open(p114, 'w', encoding='utf-8').write(原114)

    # ②施工表那一路·八行一并退回
    s = 原表
    for 今, 旧 in 旧行:
        s = s.replace(今, 旧, 1)
    io.open(表, 'w', encoding='utf-8').write(s)
    tb = X.表数()
    坏 = sorted(n for n, (m, k) in tb.items() if m - k != X.差)
    t('②旧式回灌·施工表八行退回治前之数，逐行逮得出', 坏, [106, 107, 108, 109, 110, 111, 113, 115])
    t('②之二·此时全器报红', X.跑(报=False) > 0, True)

    # ③非陪跑：旧式只问「这一行有没有把这两个数写上」，那八行**样样都写着**，故旧式零报
    旧式坏 = [n for n in (106, 107, 108, 109, 110, 111, 113, 115) if n not in tb]
    t('③旧式（只问这一行有没有写这两个数）对同一份原物零报', 旧式坏, [])
    t('③之二·而新式在同一份原物上逮出八行', len(坏), 8)
finally:
    io.open(p114, 'w', encoding='utf-8').write(原114)
    io.open(表, 'w', encoding='utf-8').write(原表)

# ④非挖空：现文全绿，且两档逐字原样
t('④现文零红', X.跑(报=False), 0)
t('④之二·回灌跑完两档逐字原样', (_sha(p114), _sha(表)), sha0)

print('════ 负测·息日链 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (实, 期)))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·息日链 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
