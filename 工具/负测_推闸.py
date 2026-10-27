# -*- coding: utf-8 -*-
"""推闸负测（2026-08-28 立·随「改钩子之策」同日；X55·1021 分等；1027 汰跑轮档／封版档）。
★所测者一句：**读者可见之闸红即拦；只器之红放行而入账（器红账限三章治）。**
⛔1027：旧推闸之跑轮档（回执未交而放⑥·冷轮之欠、第零轮、FS沉默闸之认账）与封版档（放⑭）随十三轮、冷眼轮汰——
  X55 以来读者可见之红必先至「分等」而拦，旧口不可达、只余死码；其旧测（①—⑪）随之去。
★★非陪跑（令§六③）：以改前之全测（97286329）回灌——FS沉默闸 独红而逾期之根俱已「认账」，旧式经跑轮档放行；新式恒拦。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, importlib.util, tempfile, os, io, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('qc', os.path.join(ROOT, '工具', '全测.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

案 = []

# ⑫ X55 分等：读者可见之红必拦；只器之红放行（只测 分等，⛔写器红账）
for 名, f, 期读, 期器 in [
    ('⑫之a 只器红', ['负测·含拍', '跑账', '囤灰闸'], [], ['负测·含拍', '跑账', '囤灰闸']),
    ('⑫之b 器红＋字数闸', ['跑账', '字数闸'], ['字数闸'], ['跑账']),
    ('⑫之c 负测留字必拦', ['负测留字'], ['负测留字'], []),
    ('⑫之d 全书检必拦', ['全书检', '负测·推闸'], ['全书检'], ['负测·推闸']),
]:
    读, 器 = m.分等(f)
    案.append((名, 读 == 期读 and 器 == 期器, '读=%r 器=%r' % (读, 器)))

# ⑬ 推闸之判（器红账以桩代之，⛔写真账）
_入 = []
m._器红入账 = lambda 器红, 章: (_入.append((list(器红), 章)), [])[1]
m._末章 = lambda: 411
ok, 语 = m.推闸(['改单', '跑账'])
案.append(('⑬之a 读红（改单）＋器红 → 拦，语点读红之名、⛔入器红账', ok is False and '改单' in 语 and '读者可见' in 语 and _入 == [],
           '实=%r %s' % (ok, 语[:60])))
ok, 语 = m.推闸(['FS沉默闸'])
案.append(('⑬之b FS沉默闸 独红（旧跑轮档认账即放）→ 拦', ok is False and 'FS沉默闸' in 语, '实=%r' % ok))
ok, 语 = m.推闸(['跑账', '囤灰闸'])
案.append(('⑬之c 只器之红 → 放行、入器红账（第411章）', ok is True and '分等：放行' in 语 and _入 == [(['跑账', '囤灰闸'], 411)],
           '实=%r 入=%r' % (ok, _入)))
案.append(('⑬之d 旧口俱去：⛔_推闸旧／_RAW／跑轮档之放行标', not any(hasattr(m, x) for x in ('_推闸旧', '_RAW', '_放行标', '_逾期伏笔俱已认账'))
           and '跑轮档：放行' not in io.open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read(), ''))

# ⑭ 旧式回灌（令§六③）：改前之全测（97286329·_推闸旧 在）对 ⑬之b 同局放行——故⑬之b 非陪跑
旧源 = subprocess.run(['git', 'show', '97286329:工具/全测.py'], cwd=ROOT, capture_output=True, text=True).stdout
if 旧源:
    sys.dont_write_bytecode = True          # 临时之旧档⛔留 __pycache__
    fd, tmp = tempfile.mkstemp(prefix='quance_tz_', suffix='.py', dir=os.path.join(ROOT, '工具'))
    os.close(fd)
    io.open(tmp, 'w', encoding='utf-8').write(旧源)
    try:
        sp = importlib.util.spec_from_file_location('quance_tz', tmp)
        旧 = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(旧)
    finally:
        os.remove(tmp)
    旧._末章 = lambda: 411
    旧._已封版 = lambda n: False                 # 回执未交（跑轮档）
    旧._逾期伏笔俱已认账 = lambda raw: True        # 逾期之根俱写「FSxx·本章未兑」
    旧._器红入账 = lambda 器红, 章: []
    旧放 = 旧.推闸(['FS沉默闸'])[0]
    案.append(('⑭旧式回灌（97286329）：同局（FS沉默闸 独红而已认账）旧式放行 → 新式拦，判得不同', 旧放 is True, '旧=%r' % 旧放))
else:
    案.append(('⑭旧式回灌：取不着 97286329 之全测（浅克隆？）', False, ''))

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
