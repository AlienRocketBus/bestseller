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

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
