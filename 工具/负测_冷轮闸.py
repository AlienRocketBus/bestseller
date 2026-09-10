# -*- coding: utf-8 -*-
"""⑥·冷轮之欠 负测（2026-08-28 立·随「改⑥之闸」同日）。
★一个只会说「零」的闸没有价值；故此测专问：它还逮不逮得住真欠。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, io, sys, glob, tempfile, importlib.util

spec = importlib.util.spec_from_file_location('k6', '工具/开轮六检.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def 造(tmp, 正文章, 冷轮档, 回执文=''):
    os.makedirs(os.path.join(tmp, '正文'), exist_ok=True)
    os.makedirs(os.path.join(tmp, '设定'), exist_ok=True)
    F = {}
    for n in 正文章:
        p = os.path.join(tmp, '正文', 'ch%d.md' % n)
        io.open(p, 'w', encoding='utf8').write('x')
        F[n] = p
    for n, lim in 冷轮档.items():
        io.open(os.path.join(tmp, '设定', '冷轮_COLD%d_於%d补执.md' % (n, lim)),
                'w', encoding='utf8').write('# 冷轮 COLD-%d（第%d章立·限%d·於%d补执）\n' % (n, n, lim, lim))
    io.open(os.path.join(tmp, '设定', '回执_x_第1章作业单.md'), 'w', encoding='utf8').write(回执文)
    m.ROOT, m.F = tmp, F

def 跑(cur):
    (名, ok, 语), = m.check6(cur)
    return ok, 语

案 = []
def chk(名, 实, 期):
    案.append((名, 实 == 期, '实=%r 期=%r' % (实, 期)))

# ① 真欠须逮住：COLD-73 限75，已写到75，回执无其签核
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {73: 75})
    ok, 语 = 跑(75)
    chk('①真欠须逮住（限75·已到75·未签核）', (ok, 'COLD-73' in 语), (False, True))

# ② 已签核者不许报
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {73: 75}, '并及：73章冷眼轮已销档。')
    chk('②已签核者不许报', 跑(75)[0], True)

# ③ 未到其限者不许报：限75，而今方76-1=75？取cur=74
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {73: 75})
    chk('③未到其限者不许报（限75·cur=74）', 跑(74)[0], True)

# ④ 档自书之限压倒通则：73+2=75为通则，而档书限76 → cur=75时不许报
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 77), {73: 76})
    chk('④档限压倒通则（限76·cur=75）', 跑(75)[0], True)
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 77), {73: 76})
    ok, 语 = 跑(76)
    chk('④之反·到其限即报（限76·cur=76）', (ok, 'COLD-73' in 语), (False, True))

# ⑤ 逃逸之防：限999 不认，退回通则 73+2=75
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {73: 999})
    ok, 语 = 跑(75)
    chk('⑤限999不认·退回通则须仍逮住', (ok, 'COLD-73' in 语), (False, True))

# ⑥ 无档者用通则：73无档，cur=75 → 须报
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {})
    ok, 语 = 跑(75)
    chk('⑥无档者用通则N+2', (ok, 'COLD-73' in 语), (False, True))

# ⑦ cur 收到末一有正文之章：正文只到75，而以77为cur → 不得把限77者算进来
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 76), {73: 75, 74: 77}, '并及：73章冷眼轮已销档。')
    chk('⑦cur须收到末一有正文之章（正文止75·cur=77）', 跑(77)[0], True)
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 78), {73: 75, 74: 77}, '并及：73章冷眼轮已销档。')
    ok, 语 = 跑(77)
    chk('⑦之反·正文真到77即报', (ok, 'COLD-74' in 语), (False, True))

# ⑧ 逾期之标须仍在
with tempfile.TemporaryDirectory() as t:
    造(t, range(73, 78), {73: 75})
    ok, 语 = 跑(77)
    chk('⑧逾期一章以上须标⛔', (ok, '逾期' in 语), (False, True))

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
