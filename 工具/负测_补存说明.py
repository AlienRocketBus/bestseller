# -*- coding: utf-8 -*-
"""负测 · 补存说明短於八字者拒存（2026-09-24 立·同日负测）

⛔**其所治**：体检账通例一〇二「拿一件会写盘的器去『看一眼』，往台账上落了一行『x』」——
  **0924 本坐一字不差地复犯**（`--补存 363 "x"` 存成了，落一版说明作「x」）。
★**头一格係旧式回灌**：旧式之 `--补存` 分支直接 `return buccun(n, _记(sys.argv))`，**不问说明长短**。
⛔本负测不真跑存版（⛔那正是本器要禁的「拿会写盘的器去看一眼」），只读其码与其拒之判。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 跑():
    src = io.open(os.path.join(ROOT, '工具', '跑轮.py'), encoding='utf-8').read()
    段 = src.split("if cmd == '--补存':")[1].split("if cmd == '--还原':")[0]
    R = []
    R.append(('①⛔旧式回灌：旧式分支一行直存、不问说明（今之码已不是那一行）',
              "return buccun(n, _记(sys.argv))" not in 段))
    R.append(('②新式：说明短於八字即 return 2（拒存）',
              '< 8' in 段 and 'return 2' in 段))
    R.append(('③⛔拒之语指明其由（通例一〇二）与其正路（--对表）',
              '通例一〇二' in 段 and '--对表' in 段))
    # ④真跑一回「x」，⛔证它真的不写盘（台账前後逐字同）
    台 = os.path.join(ROOT, '版本', '第363章', '_台账.json')
    前 = io.open(台, 'rb').read() if os.path.exists(台) else b''
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '跑轮.py'), '--补存', '363', 'x'],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    後 = io.open(台, 'rb').read() if os.path.exists(台) else b''
    R.append(('④真跑「x」：rc=2 且台账前後逐字同（⛔证它真的只看了一眼）',
              r.returncode == 2 and 前 == 後))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·补存说明 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
