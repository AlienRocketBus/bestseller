# -*- coding: utf-8 -*-
"""负测·字数闸 · 2026-09-06 立（与 工具/字数闸.py 同日·令§六③）
　★要害不在「会不会报红」，在四样：
　　①**以旧式回灌**：拿 832499ed（立此器之日、六处未治之时）的 198／200／203 三档灌回去，
　　　须逐处报红，且**六处一处不漏**；
　　②**非陪跑**：旧式若只问「有没有『N个字』这一式」，同一份原物**一处也报不出**——
　　　那六处样样都写着「N个字」，写着而数错，旧式看不见；
　　③**非挖空**：今版须全绿（治毕之後），且其群不得塌（紧邻式仍 ≥130 处）；
　　④**不吃盘**：此器只读不写，跑完诸档逐字原样。
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
import 字数闸 as Z                                        # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
锚 = '832499ed'          # 立此器之日之 HEAD——其时六处未治


def 旧本(n):
    rel = os.path.relpath(章[n], 根)
    r = subprocess.run(['git', '-C', 根, 'show', '%s:%s' % (锚, rel)], capture_output=True)
    return r.stdout.decode('utf-8')


sha0 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 章.items()}

# ①旧式回灌·三档六处
红 = []
for n in (198, 200, 203):
    s = 旧本(n)
    if not s:
        continue
    for q, cnt, real, _尾 in Z.取(s.split('【本章亮点】')[0]):
        if cnt != real:
            红.append((n, q, cnt, real))
t('①回灌 %s 之 198／200／203，逐处逮出六处' % 锚, len(红), 6)
t('①之二·三章各逮两处', sorted({n for n, *_ in 红}), [198, 200, 203])

# ②非陪跑：旧式只问「有没有 N个字 这一式」，同一份原物零报
旧式 = re.compile(r'([一二三四五六七八九十两]+)个字')
漏 = 0
for n, q, cnt, real in 红:
    s = 旧本(n)
    if 旧式.search(s):      # 式子在，故旧式判「有，合格」——一处也报不出
        漏 += 1
t('②旧式（只问这一式在不在）对同一份原物零报（六处样样写着，写着而数错）', 漏, 6)

# ⑤路二·拿 6d8dee47（路二立成之前、242 未治之时）之 242 原物回灌，须逮出「称七实八」
锚二 = '6d8dee47'
r = subprocess.run(['git', '-C', 根, 'show', '%s:%s' % (锚二, os.path.relpath(章[242], 根))],
                   capture_output=True)
旧242 = r.stdout.decode('utf-8').split('【本章亮点】')[0]
二 = [x for x in Z.取二(旧242) if x[3] != x[4]]
t('⑤回灌 %s 之 242，路二逮出「从今天起，我先动手」称七实八' % 锚二,
  [(x[2], x[3], x[4]) for x in 二], [('从今天起，我先动手', 7, 8)])

# ⑥非陪跑：**紧邻式对同一份原物一处也报不出**——那八个字与其数隔着一个＊拍
t('⑥旧式（只认紧邻式）对同一份原物零报（立言与报数隔着一个＊拍，紧邻式看不见）',
  [1 for q, cnt, real, _ in Z.取(旧242) if cnt != real], [])
t('⑥之二·而那一处确实写着「个字」（不是没写，是写着而数错）', '七个字占了一行' in 旧242, True)

# ③非挖空：今版之群不得塌
今红, 今群 = Z.跑(报=False)
t('③今版其群仍在（紧邻式＋冒号立言式 ≥130 处）', 今群 >= 130, True)
t('③之二·路二之群今皆合（本书同类共 5 处，逐处对得上）',
  [x for n, p in sorted(章.items())
   for x in Z.取二(io.open(p, encoding='utf-8').read().split('【本章亮点】')[0]) if x[3] != x[4]], [])

# ④不吃盘
sha1 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 诸章().items()}
t('④跑完诸档逐字原样', sha1, sha0)

print('════ 负测·字数闸 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:70], str(期)[:70])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·字数闸 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
print('  ℹ今版余红 %d 处（治毕之後此数须为 0，方可把本闸接进全测）' % 今红)
sys.exit(0 if 好 == len(过) else 1)
