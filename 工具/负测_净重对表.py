# -*- coding: utf-8 -*-
"""负测·净重对表 · 2026-09-08 立（与 工具/净重对表.py 同日·令§六③）
　★要害在四样：
　　①**以旧式回灌**：拿 `db520882`（此器立成之前）之施工表灌回去，须逐行逮出那 17 处；
　　②**非陪跑**：**旧式对同一份原物零报**——立此器之前，全书没有一道器拿锁定行之净重回正文量过
　　　（`grep -rn 净重 工具/*.py` 之下，只有 书级体检 与 全测 在自己算自己的，无一处回表复量）；
　　③**非挖空**：今版须全绿，且其群不得塌（26 章），并须证「把一行改坏立刻逮得出」；
　　④**不吃盘**：此器只读不写（`--补` 例外，本负测不跑它），跑完诸档逐字原样。
"""
import io, os, sys, subprocess, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 净重对表 as J                                      # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
锚 = 'db520882'      # 此器立成之前——那 17 行尚未补
守 = [os.path.join(根, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')] + list(章.values())
sha0 = {p: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for p in 守}

# ①旧物回灌：拿立器之前的施工表，须逮出 17 处
r = subprocess.run(['git', '-C', 根, 'show', '%s:设定/01_镇冢秘术_逐章施工与伏笔回收表.md' % 锚],
                   capture_output=True)
旧表 = r.stdout.decode('utf-8')
红旧, 群旧 = J.量(表文=旧表)
t('①回灌 %s 之施工表，逐行逮出 17 处不符' % 锚, len(红旧), 17)
t('①之二·其群不变（26 章自书净重）', 群旧, 26)
t('①之三·逐处之差与立器之日所印同（283 记3499 实3481）',
  [(n, a, b) for _, n, a, b in 红旧 if n == 283], [(283, 3499, 3481)])

# ②非陪跑：立此器以前，无一道器拿锁定行之净重回正文量过。
#   ★怎么算「拿它量过」：一道器要量它，非得在同一处**既认锁定行、又取净重**不可。
#   故逐档逐行看：别器里有没有一行同时含「锁定」与「净重」。
#   ★★而 全测.py 里也有这样的行——那是**本器自己的接线与器注**，不算别器；
#     故它们必须**全落在 chk_net_weight_table 那一函数之内**。落在函数外，即是别处也在读它，此格该红。
全码 = io.open(os.path.join(根, '工具', '全测.py'), encoding='utf-8').read().split('\n')
起 = next(i for i, l in enumerate(全码) if l.startswith('def chk_net_weight_table'))
止 = next(i for i in range(起 + 1, len(全码)) if 全码[i].startswith('def '))
犯 = []
for f in sorted(os.listdir(os.path.join(根, '工具'))):
    if not f.endswith('.py') or f in ('净重对表.py', '负测_净重对表.py'):
        continue
    for i, ln in enumerate(io.open(os.path.join(根, '工具', f), encoding='utf-8'), 1):
        if '锁定' in ln and '净重' in ln:
            if f == '全测.py' and 起 < i <= 止:
                continue        # 本器之接线，不算别器
            犯.append('%s:%d' % (f, i))
t('②非陪跑：除本器之接线外，别处无一行同时读「锁定」与「净重」（故那 17 处一器也报不出）', 犯, [])
t('②之三·而本器之接线确在（不是靠删干净换来的绿）',
  any('锁定' in l and '净重' in l for l in 全码[起:止]), True)
# ②之二·而 全测.py 确实提过「净重」——提的是别的账（回执对台账、全书净重中位、台账之版比），
#   非施工表之锁定行；此格证「提过」不等于「量过」。
全 = io.open(os.path.join(根, '工具', '全测.py'), encoding='utf-8').read()
t('②之二·全测提过净重（故此非「谁都没提过」，是「提过而没回表量过」）', '净重' in 全, True)

# ③非挖空
红今, 群今 = J.量()
t('③今版零处不符', [(n, a, b) for _, n, a, b in 红今], [])
t('③之二·其群不得塌（26 章）', 群今, 26)
文 = io.open(守[0], encoding='utf-8').read()
坏 = None
for line in 文.split('\n'):
    m = J.锁.match(line)
    if m and J.数.search(line) and int(m.group(1)) in 章:
        坏 = line
        break
假 = 文.replace(坏, J.数.sub('净重1', 坏, count=1), 1)
r4, _ = J.量(表文=假)
t('③之三·把一行之数改作 1，当场逮出（这个绿不是一律放行换来的）',
  len(r4) == 1 and r4[0][2] == 1, True)

# ④不吃盘
sha1 = {p: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for p in 守}
t('④跑完施工表与诸章逐字原样', sha1, sha0)

print('════ 负测·净重对表 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:70], str(期)[:70])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·净重对表 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
