# -*- coding: utf-8 -*-
"""负测·含拍 · 2026-09-06 立（与 工具/含拍.py 同日·令§六③）
　★要害不在「会不会报红」，在四样：
　　①**以旧式回灌·祖案**：拿 832499ed^（治 138 之前）的第 138 章灌回去，须报红——
　　　那一章 87 行是并好的长段，89—103 八拍逐字就是它拆开的样子，约二百字说了两遍；
　　②**以旧式回灌·今日所治**：拿 af907d08（治六章之前）的 196／197／201／206／207／270 灌回去，
　　　须逐章报红，六章一章不漏；
　　③**非陪跑（其说 0906 当日改过一次·照实记）**：
　　　立此器之日，`邻拍重出` 对同一份 138 原物**一处也报不出**——其时它按「＊」分拍，
　　　而 138 通篇以空行分拍，於是它见 138 为 **1 拍**（`含拍` 见 223 拍），整章无从比起。
　　　**而这个洞正是本负测逼出来的**：同日已把 `邻拍重出` 之分拍改为按行，改後它见 8 处、过线报红。
　　　**故此条今日之说不再是「旧器看不见」，而是「两器所判不同」**——
　　　`邻拍重出` 报两拍互有重字（只报不拦），`含拍` 判一拍整个装进另一拍（红即拦）。
　　　★留此一笔，是因为「旧器一处也报不出」这句话曾经为真、今日已假；
　　　**一个负测若把已经不真的话留着当凭据，它自己就成了下一个坑。**
　　④**非挖空**：今版全书零红，而「隔得远的那一路」（有意之引）仍在，不曾被一并扫掉。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, subprocess, sys, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 含拍 as H                                          # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
祖锚 = '832499ed^'      # 治 138 之前
今锚 = 'af907d08'       # 治六章之前


def 旧本(n, 锚):
    rel = os.path.relpath(章[n], 根)
    return subprocess.run(['git', '-C', 根, 'show', '%s:%s' % (锚, rel)],
                          capture_output=True).stdout.decode('utf-8')


def 验(txt):
    """与 含拍.验一章 同法，只是正文自串取而不自盘取。返回 [(短拍, 长拍, 隔), ...]"""
    body = txt.split('【本章亮点】')[0]
    拍 = [x.strip() for x in body.split('\n') if x.strip() and x.strip() != '＊']
    骨 = [H.剥(x) for x in 拍]
    出 = []
    for i, a in enumerate(骨):
        if len(a) < H.最短:
            continue
        for j, b in enumerate(骨):
            if i != j and len(b) > len(a) and a in b and abs(i - j) <= H.隔:
                出.append((i + 1, j + 1, abs(i - j)))
                break
    return 出


sha0 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 章.items()}

# ①祖案回灌
祖 = 验(旧本(138, 祖锚))
t('①回灌 %s 之第138章（治前）须报红（其诸含拍之隔为 1—7，故隔窗须 ≥7）' % 祖锚, len(祖) >= 7, True)

# ②今日所治六章回灌
坏 = [n for n in (196, 197, 201, 206, 207, 270) if 验(旧本(n, 今锚))]
t('②回灌 %s 之六章（治前）逐章报红' % 今锚, 坏, [196, 197, 201, 206, 207, 270])

# ③非陪跑：立器之日 `邻拍重出` 按「＊」分拍，见 138 为 1 拍，故整章比不着
def 按星分拍(txt):
    import re as _re
    body = txt.split('【本章亮点】')[0]
    return [_re.sub(r'[，、。！？：；「」\s]', '', x) for x in body.split('\n＊\n')]
t('③非陪跑·立器之日 `邻拍重出` 按「＊」分拍，见138治前为 1 拍（含拍见 223 拍），整章比不着',
  len(按星分拍(旧本(138, 祖锚))), 1)

# ④非挖空：今版零红，而「隔得远的有意之引」仍在
t('④今版全书零红', H.跑(报=False), 0)
远 = 0
for n, p in 章.items():
    拍 = H.诸拍(p); 骨 = [H.剥(x) for x in 拍]
    for i, a in enumerate(骨):
        if len(a) < H.最短:
            continue
        for j, b in enumerate(骨):
            if i != j and len(b) > len(a) and a in b:
                if abs(i - j) > H.隔:
                    远 += 1
                break
t('④之二·隔得远的那一路（有意之引）仍在，未被一并扫掉', 远 >= 3, True)

sha1 = {n: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for n, p in 诸章().items()}
t('④之三·跑完诸档逐字原样', sha1, sha0)

print('════ 负测·含拍 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:70], str(期)[:70])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·含拍 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
