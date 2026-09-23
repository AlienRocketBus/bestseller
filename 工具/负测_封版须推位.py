# -*- coding: utf-8 -*-
"""负测·封版须推位（2026-09-23·限362 立）

⛔**其所由来**：**361 封版席自己交上来的第⑦条红**，逐字：
  「**`open_brief` 第六回靠人记得·盘上四把器无一把写它**（355／357／358／359／360／361）
   ——⛔**须立一把器去写它**」。

★**本坐查过盘上之实，判其所指之处为真，而其所求之治不可取**：
  **`open_brief` 五格之中只有 `for_ch` 是机械的**，
  **`接写自`／`required_state_cards`／`位`／`批次` 四格皆係判**；
  ⛔**若器把 `for_ch` 自己推上去而那四格照旧是上一章的**，**闸当场转绿而料是旧的**
  ——**那比没有这道闸更坏**（`书级体检::check_loss` 之鉴）。

★★**而那道闸其实早已有**（`小说检察官.py:4733`），**其真正的缝在「几时查」**：
  **它只在下一章开跑之时才出声**——**於是这一笔永远落在下一坐头上。**
★★★**故所立者不是一把写它的器，是把那一条已有之令挪到它该咬住的那一刻**：
  **封版之前问一句，推不上去就不许封。**
⛔**此改令闸更硬，不更软**：**它不放过任何一章，而从前它只逮下一章之始。**

跑：python3 工具/负测_封版须推位.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
过 = 败 = 0


def chk(名, 实):
    global 过, 败
    if 实:
        过 += 1
    else:
        败 += 1
        print('  ⛔不过：%s' % 名)


_源 = io.open(os.path.join(ROOT, '工具', '收.py'), encoding='utf-8').read()
_段 = _源.split('⑥之二')[-1][:3000] if '⑥之二' in _源 else ''

chk('①`收.py` 之封版序里已有「⑥之二·open_brief 须已推到下一章」这一步', bool(_段))
chk('②其判係 `for_ch != n + 1` 即停（⛔不是只提醒一句）',
    '_for != n + 1' in _段 and 'return' in _段)
chk('⛔③其停语须说出当下之数与该推到几——⛔不许只说「未推」',
    'for_ch＝%s' in _段 and 'n + 1' in _段)
chk('⛔④其停语须同时说「不是只改那一个数」（四格皆係判，须一并写过）',
    '不是只改那一个数' in _段 and '接写自' in _段)
chk('⛔⑤读不出来者须停，⛔不许当作「已推」', '不许当作「已推」' in _段)
chk('⑥其位在「旗在则拒封」之後、`git commit` 之前（⛔封了版再问即已太迟）',
    _源.index('⑥之二') > _源.index('拦停旗未销')
    and _源.index('⑥之二') < _源.index("'commit', '-q'"))

# ⛔⑦之反面：旧式（封版之序里没有这一问）对同一局面一声不响
_旧 = _源.split('── ⑥ 提交并复验 ──')[-1].split('⑥之二')[0]
chk('⛔⑦而旧式那一段（旗与领轮二问）通篇不提 open_brief——故上六格非陪跑',
    'open_brief' not in _旧)

# ── 真盘之实（⛔读而不改）────────────────────────────
import json
_ob = (json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'),
                         encoding='utf-8')).get('open_brief') or {})
_末 = len([x for x in os.listdir(os.path.join(ROOT, '正文')) if x.endswith('.md')])
chk('⑧真盘此刻 open_brief.for_ch 正指末章之次（%s / 末章 %d）' % (_ob.get('for_ch'), _末),
    int(_ob.get('for_ch') or 0) == _末 + 1)

# ── ⑨·本测之限，写死在码里 ────────────────────────
#   **本测验的是「封版之序里有没有这一问」，⛔不是「那四格之料新不新」。**
#   ★**料新不新，机器判不了**——**只有读它的人判得了**；**本闸只保证没人能绕过去不写。**
chk('⑨本测之限已写死在本测码内（⛔验的是有没有问，不是料新不新）',
    '料新不新，机器判不了' in open(__file__, encoding='utf-8').read())

print('  负测·封版须推位：%d/%d' % (过, 过 + 败))
sys.exit(1 if 败 else 0)
