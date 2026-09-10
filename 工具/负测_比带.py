# -*- coding: utf-8 -*-
"""负测·比带（批131·293第8轮所立）
所治之伤：**一把带，取错了比的人，就把三处好文判成了伤。**
        本坐293第5、7、8三轮各逮一「逾带」，而三处用的是同一把手挑之带
        （苏衍近五章 282／285／287／289／291）；而那五章之形是做事与问人，
        **293是他近年唯一一篇翻判**。换成形相同之十八章，三个数一个也不逾带：
            「因为」2.3（同形带0.0—3.1）｜「像」0.9（同形带0.0—1.2）｜90分位38（同形带30—76）。
        三个「逾带」，一个也不成立。
本测所验者为不变量，非快照：
  ①一个数须报三条带（全书／同镜／同形），一条也不许少；
  ②三条带确会判得不一样——全书回灌须得≥10处相犯（若为0，此器即无用，当日撤）；
  ③其判据係「本章之形」，而形之取法须与 开轮六检::check17 同源（卡为先，词频为退）；
  ④而它不判——只报三条带与本章之落处，不出「须改」二字。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, contextlib
import importlib.util as iu
_D = os.path.dirname(os.path.abspath(__file__))
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_s = iu.spec_from_file_location('_bd', os.path.join(_D, '比带.py'))
_bd = iu.module_from_spec(_s)
with contextlib.redirect_stdout(io.StringIO()):
    _s.loader.exec_module(_bd)

_src = io.open(os.path.join(_D, '比带.py'), encoding='utf-8').read()
chk('①三条带俱在（全书／同镜／同形）',
    all(("说('%s'" % x) in _src for x in ('全书', '同镜', '同形')), True)
chk('④其语不出「须改」二字（它只报，不判）', '须改' in _src, False)
chk('④之b 而它明写「以同形为先」（三条不同判时之序）', '以同形为先' in _src, True)
chk('③形之取法与 check17 同源（卡为先，词频为退）',
    '本章之形[：:）' in _src and 'FORM' in _src, True)
chk('③之b 且其不称职之凭据与器同存（本坐三轮之实写在器上）',
    '293是他近年唯一一篇翻判' in _src or '第5、7、8三轮' in _src, True)

# ②回灌全书：三条带确会判得不一样
cache_all = {}
found = []
for 项 in _bd.项表:
    f = _bd.项表[项]
    cache = {}
    for k in range(200, 294):
        b = _bd._白(k)
        if b and _bd._净(b) >= 500:
            cache[k] = (f(b), _bd._镜(k), _bd._形(k))
    for c, (v, mj, xg) in cache.items():
        同镜 = [x[0] for k, x in cache.items() if k != c and x[1] == mj]
        同形 = [x[0] for k, x in cache.items() if k != c and x[2] == xg]
        if len(同镜) < 3 or len(同形) < 3:
            continue
        if (min(同镜) <= v <= max(同镜)) != (min(同形) <= v <= max(同形)):
            found.append((项, c))
chk('②回灌全书·三条带判得不一样者须≥10处（若为0，此器无用，当日撤）', len(found) >= 10, True)
chk('②之b 且其相犯不只出於一项（只一项者，是那一项之偏，不是带之理）',
    len({x[0] for x in found}) >= 2, True)

# ⑤本章之实：三项俱须报得出三条带且不崩
for 项 in ('因为', '像', '90分位'):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        _bd.带(293, 项)
    o = buf.getvalue()
    chk('⑤第293章项「%s」三条带俱报得出' % 项,
        all(x in o for x in ('全书', '同镜', '同形', '本章之形')), True)

# ★★★★★⑧·DEBT-297C 之验（297第5轮立·限307·於307封版之序结清）
#   ★其档所命之头一项断言逐字：**「以297第5轮之前的听0回灌，新式须报红而旧式报绿」**。
#   ★★故此处取全书「听」之实群，把一个 0.0 之章当作本章回灌，两式各判一回：
#     旧式（底＝min）须判「在带内」（因群中已有零章，底被钉在0）；新式（底＝10分位）须判「低於其底」。
_听 = _bd.项表['听']
_群 = []
for k in range(200, 294):
    b = _bd._白(k)
    if b and _bd._净(b) >= 500:
        _群.append(_听(b))
_零章 = [v for v in _群 if v == 0.0]
chk('⑧群中确有零章（此伤之所以成立·若无零章则本测係陪跑）', len(_零章) >= 1, True)
_旧底 = min(_群)
_新底 = _bd.底(_群)
chk('⑧之b 旧式之底被零章钉死在 0', _旧底 == 0.0, True)
chk('⑧之c 新式之底高於 0（一个零章不许把整条带的底钉死）', _新底 > 0.0, True)
_本 = 0.0
chk('⑧之d 以听0回灌·旧式报「在带内」（此即297第5轮所逮之假绿）',
    _旧底 <= _本 <= max(_群), True)
chk('⑧之e 以听0回灌·新式报「低於其底」（红）', _本 < _新底, True)
#   ★★★而其不许挖空闸：新式之底不得高於中位（高过中位即是把半本书判成伤）。
import statistics as _st
chk('⑧之f 新式之底不得高於群之中位（防挖空闸／防误判半本书）', _新底 <= _st.median(_群), True)
#   ★★★★并验一样：本器所改者只有底，顶照旧取 max（逾顶之病不对称，见 比带.py::底 之注）。
chk('⑧之g 顶照旧取 max（只改底，不改顶）', 'hi_, md = 底(xs), max(xs)' in
    open(os.path.join(_D, '比带.py'), encoding='utf-8').read().replace('lo_, ', ''), True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
