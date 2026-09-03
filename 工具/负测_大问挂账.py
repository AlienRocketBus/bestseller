# -*- coding: utf-8 -*-
"""负测·大问挂账（八造·2026-09-03 立）

★所治之伤：大问表自 2026-09-01 立起自印「只报不拦」，
　而以294章计逾四十章者七样（血图缺234章、悬赏223、地窖222、寨里那些人186、
　爷爷184、走路的理由116、听针92）——**二百三十四章之内没有一道闸因此拦过一次**。
★★八造改其律为「可以欠，不可以不认」：逾限者须各有一笔挂账，挂账须带限章；
　挂了账而逾了自己那个限者，拦。
★★★**而本测断的是不变之则，不是今日之天气**（第二十八犯之戒）：
　逐条皆「拿掉那一样 → 须红；放回去 → 须绿」，一处也不写死今日之数。
"""
import io, os, re, sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_p = os.path.join(ROOT, '工具', '大问表.py')
_s = _iu.spec_from_file_location('_dwb', _p)
M = _iu.module_from_spec(_s); _s.loader.exec_module(M)

档 = M.挂账档
原 = io.open(档, encoding='utf-8').read() if os.path.exists(档) else None

ok = bad = 0


def chk(名, 得, 期):
    global ok, bad
    if 得 == 期:
        ok += 1; print('  ✓ %s' % 名)
    else:
        bad += 1; print('  ✗ %s ← 得 %r，期 %r' % (名, 得, 期))


def 跑():
    """静跑一回，返回 (逾, 无挂, 逾限)。"""
    return M.报(quiet=True)


def 写(t):
    io.open(档, 'w', encoding='utf-8').write(t)


try:
    print('════ 负测·大问挂账 ════')

    # ①今日之实：册在，且逐样有挂——须无「无挂」、无「逾限」
    逾0, 无挂0, 逾限0 = 跑()
    chk('①册齐之时，无一样无挂账', 无挂0, [])
    chk('①册齐之时，无一笔逾其自定之限', 逾限0, [])
    chk('①而逾四十章者本身照旧要报（不许因挂了账就不报）', len(逾0) > 0, True)

    # ②抽掉一笔挂账 → 那一样须落进「无挂」；放回 → 须复绿
    某 = 逾0[0]['名']
    行 = [l for l in 原.split('\n') if l.startswith('| ' + 某 + ' ')]
    assert 行, '取不到 %s 之行' % 某
    写(原.replace(行[0] + '\n', ''))
    _, 无挂1, _ = 跑()
    chk('②抽掉「%s」之挂账 → 它须落进无挂' % 某, 某 in 无挂1, True)
    写(原)
    _, 无挂1b, _ = 跑()
    chk('②放回去 → 须复绿', 某 in 无挂1b, False)

    # ③把一笔的限改到今章之前 → 须落进「逾限」；改回 → 须复绿
    # ★不照单元格之貌下手（本测头一版即栽在此：以「**限第N章**」去替，而册里写的是「**N**」，
    #   於是替了个空，测自己绿了。故改为**按栏重建**，不问那一栏长什么样。）
    末, _rows = M.量()

    def 改限(行, 新):
        c = [x.strip() for x in 行.strip().strip('|').split('|')]
        c[3] = '**%d**' % 新
        return '| ' + ' | '.join(c) + ' |'

    改 = 改限(行[0], 末 - 1)
    assert 改 != 行[0], '③之替换须真改了那一栏'
    写(原.replace(行[0], 改))
    _, _, 逾限2 = 跑()
    chk('③「%s」之限改到今章之前 → 须落进逾限' % 某, 某 in [a for a, b in 逾限2], True)
    写(原)
    _, _, 逾限2b = 跑()
    chk('③改回去 → 须复绿', 某 in [a for a, b in 逾限2b], False)

    # ④限正落在今章者，不算逾（限之义是「最晚这一章还」，不是「这一章之前还」）
    改4 = 改限(行[0], 末)
    写(原.replace(行[0], 改4))
    _, _, 逾限3 = 跑()
    chk('④限正落在今章者不算逾（最晚这一章还，仍在期内）', 某 in [a for a, b in 逾限3], False)
    写(原)

    # ⑤状不作「挂」者不算挂账（还过的那几行不许再当欠条使）
    改5 = 行[0].rsplit('|', 2)[0] + '| 还 |'
    写(原.replace(行[0], 改5))
    _, 无挂4, _ = 跑()
    chk('⑤状改作「还」者不再算挂账 → 须落回无挂', 某 in 无挂4, True)
    写(原)

    # ⑥册整个不在 → 逾限者须一样不落地全进「无挂」
    os.rename(档, 档 + '.bak')
    try:
        逾5, 无挂5, _ = 跑()
        chk('⑥册不在 → 逾限者须一样不落地全进无挂', sorted(无挂5), sorted(r['名'] for r in 逾5))
    finally:
        os.rename(档 + '.bak', 档)

    # ⑦其口须真会拿非零退出（一道只会说「零」的闸没有价值·令§六③）
    src = io.open(_p, encoding='utf-8').read()
    chk('⑦其主口拦得动（见 sys.exit(1 ...)）', 'sys.exit(1 if' in src, True)
    chk('⑦旧律「只报不拦」已不在其主口', "sys.exit(0)   # ★只报不拦" in src, False)

finally:
    if 原 is not None:
        写(原)

# ★其末行须依 全测.py::_简测 之式（「N/N 全通」／「N/N ⛔未过」），否则全测报「未见其数」。
print('  ── %d/%d %s ──' % (ok, ok + bad, '全通' if bad == 0 else '⛔未过'))
sys.exit(0 if bad == 0 else 1)
