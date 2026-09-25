# -*- coding: utf-8 -*-
"""负测·盲读之关（2026-09-25 立·作者令「每一章须写到最好，读者读了上瘾；不然就没有必要写」）。
★所守者：`工具/席/一章.js` 之盲读之关**在、有牙、牙没被拔**：
  ①盲读席不给任何一席之说，只给正文；②不过则重锻，至多二回、每回换新盲读席；
  ③二回仍不过，**封版席不派**（机制之牙，不靠案席自觉），且案席令里明写不许封版；
  ④结果随工作流交回（盲读·盲读过）。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys
s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '席', '一章.js'), encoding='utf-8').read()
案 = []
def chk(名, 过): 案.append((名, bool(过)))
chk('①盲读之关在', '七之二·盲读之关' in s)
chk('①之b 盲读席不许读任何席之说', '你不许读任何席的轮记' in s)
chk('②不过则重锻·至多二回', "回 <= 2" in s and '重锻席' in s)
chk('②之b 每回换新盲读席', "盲读题(回 + 1)" in s)
chk('③不过则封版席不派', "const 封 = !盲读过 ?" in s)
chk('③之b 案席令明写不许封版', '本章不许封版' in s)
chk('④结果随工作流交回', '盲读: 盲读记, 盲读过' in s)
chk('⑤拿不准即 false（宁严勿松）', '拿不准即 false' in s)
坏 = [x for x in 案 if not x[1]]
print('════ 负测·盲读之关 ════')
for 名, 过 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名)
print('负测·盲读之关 %d/%d' % (len(案) - len(坏), len(案)))
sys.exit(1 if 坏 else 0)
