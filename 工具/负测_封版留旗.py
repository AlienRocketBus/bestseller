# -*- coding: utf-8 -*-
"""负测·封版留旗（2026-09-23·限361 立）

⛔**其所治者**：**一面留在已封版之章上的拦停旗，是一道没人认领的红。**
★**旗之义係「那一轮的版没存上」**；**封了版还留着旗，旗就成了谎**——
  **读它的人不知道该信哪一样：信旗则这一章没写完，信回执则它已经封版。**

★★**其所由来**：`册_0923_赤手无负测之拆数.md` 把 `对位.py` 那个「赤手 66」拆开数，
  **得「甲·真赤手」二十项**，并荐先补者三，**`chk_sealed_flags` 係其首**——
  **其由逐字：「它绿着，别处就没人再看那一件事。」**

⛔★★★**并及本测之限，先写在头上**：
  **`chk_sealed_flags` 之判係「有回执且有 `_拦停.json`」**——
  **它认不得「旗之因」**：**一面旗是真拦停，还是一串占位（220 之实：空轮闸所留之占位串，
  `_flag_stale` 永不自销），本器一概当作旗。** ★**本测不改它**
  （⛔0923 本坐之界：此非「读错」，係「治法之择」——**宁可多报一面旗，不可漏一面**），
  **只把这一句钉在⑨格里，叫後坐读得见。**

跑：python3 工具/负测_封版留旗.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as iu, os, re, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
过 = 败 = 0


def chk(名, 实):
    global 过, 败
    if 实:
        过 += 1
    else:
        败 += 1
        print('  ⛔不过：%s' % 名)


def _载():
    sp = iu.spec_from_file_location('_qc', os.path.join(ROOT, '工具', '全测.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


m = _载()
_旧式 = lambda 目, 有回执: [n for n, d in 目 if 有回执(n)]   # ⛔旧式：只问「封没封版」，不问旗

# ── 一·沙盘（⛔不动真盘）──────────────────────────────
_沙 = tempfile.mkdtemp(prefix='负测_封版留旗_')


def _造(n, 有旗):
    d = os.path.join(_沙, '第%d章' % n)
    os.makedirs(d, exist_ok=True)
    if 有旗:
        open(os.path.join(d, '_拦停.json'), 'w').write('{"由":"沙盘"}')
    return (n, d)


_目 = [_造(1, True), _造(2, False), _造(3, True), _造(4, False)]
_封 = {1, 2}                       # 1、2 已封版；3、4 未封版（3 正在跑，旗是真的）
_有 = lambda n: n in _封

_得 = m._留旗之章(_目, _有)
chk('①已封版而留旗者须报（第1章）', 1 in _得)
chk('②已封版而无旗者不报（第2章）', 2 not in _得)
chk('⛔③未封版而留旗者不报（第3章正在跑，那面旗是真的·⛔报它即是逼人把真旗销掉）',
    3 not in _得)
chk('④未封版亦无旗者不报（第4章）', 4 not in _得)
chk('⑤其单恰係一章', sorted(_得) == [1])
chk('⛔⑥而旧式（只问封没封版，不问旗）对同一份沙盘报两章——故上五格非陪跑',
    sorted(_旧式(_目, _有)) == [1, 2])

# ── 二·回执之名认不认得三种（承限360·回执三名之治）────────────
_型 = re.compile(r'回执_\d+_第(\d+)章')
for _k in ('作业单', '案席', '封版席'):
    chk('⑦认得回执之名·%s（限360 之治不许在此处漏掉）' % _k,
        _型.search('回执_20260923_第358章%s.md' % _k) is not None)
chk('⛔⑧而别章之回执不算本章（型须咬住章号）',
    int(_型.search('回执_20260923_第358章封版席.md').group(1)) == 358)

# ── 三·本测之限，写死在码里（⛔留给後坐）──────────────────
chk('⑨本项认不得「旗之因」一句已写死在本测码内（⛔宁可多报一面旗，不可漏一面）',
    '宁可多报一面旗，不可漏一面' in open(__file__, encoding='utf-8').read())
shutil.rmtree(_沙)

# ── 四·真盘之实（⛔读而不改）──────────────────────────
_ok, _语 = m.chk_sealed_flags()
chk('⑩真盘此刻无一章封了版还留着旗', _ok is True)
print('  ── 真盘之实：%s ──' % _语)
print('  负测·封版留旗：%d/%d' % (过, 过 + 败))
sys.exit(1 if 败 else 0)
