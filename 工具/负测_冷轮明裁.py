#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测 · 冷轮之令改式（2026-09-22 立）：**无档者不凭空记一笔欠，⛔而其回执须有一句立／不立之明裁。**

★其所守者三样，逐样有旧式回灌：
  ①**有明裁者不入欠**（⛔此係本改之口）；
  ②⛔**无明裁者照旧入欠**（⛔此係本改之价——**不是把这一格废掉，是把它换了一个问法**）；
  ③⛔**有档者一律照旧走老路**（签核／废档），**本改一个字也没有碰它们**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys
import glob
import importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location('k', os.path.join(ROOT, '工具', '开轮六检.py'))
K = importlib.util.module_from_spec(_s)
_s.loader.exec_module(K)

ok = bad = 0


def chk(名, 得, 期):
    global ok, bad
    if 得 == 期:
        ok += 1
        print('  ✓ %s' % 名)
    else:
        bad += 1
        print('  ⛔ %s：得 %r，期 %r' % (名, 得, 期))


print('════ 负测·冷轮明裁 ════（守：无档者不凭空记一笔欠，而其回执须有立／不立之明裁）')

# ①★盘上真局：350 与 352 之回执各有一句明裁，且二章皆无冷轮档
chk('①350 无档而其回执有明裁（不立新冷轮）',
    (K._cold_有档(350), K._cold_明裁(350)), (False, '不立新冷轮'))
chk('①之二·352 无档而其回执有明裁（无从执）',
    (K._cold_有档(352), K._cold_明裁(352)), (False, '无从执'))

# ②⛔本改之价：无档**且**无明裁者，照旧判欠。
#   ★2026-09-22 当日改过一回：**本格原拿 351 作局，而 353 封版席之回执落盘後，
#   351 当日即有了明裁**——⛔**其前提数小时内就过期了**（`体检账 51／55` 之型）。
#   ★★**故改拿 317 作局**：**317 无档、无明裁、其章已封版且其限早过**，
#   **它不会因为下一章写了什么而变**。
chk('②317 无档且无明裁（⛔照旧入欠）',
    (K._cold_有档(317), K._cold_明裁(317)), (False, None))
#   ★★★**并当面认一件**：**317 之冷轮已执**（`_cold_done(317)` → True），
#   **故它不会真落进今日之欠**——⛔**本格所验者只是「本改那一项不替它开门」**，
#   **⛔不许拿它冒充「今日盘上还有一笔真欠」**。
chk('②之二·本改那一项对 317 不放行（⛔它落不落欠，由 done／void 定，不由本改定）',
    (not (not K._cold_有档(317) and K._cold_明裁(317))), True)
#   ②之三·⛔把本改那一项单独拿出来验其式：**无档且无明裁者，此项必不放行**
_项 = lambda 有档, 明裁: not (not 有档 and 明裁)
chk('②之三·式验：无档且无明裁→不放行（照旧入欠）', _项(False, None), True)
chk('②之四·式验：无档而有明裁→放行（本改之全部所为，只此一格）', _项(False, '明裁'), False)
chk('②之五·式验：有档者一律不走本项（其销在 done／void）', _项(True, None), True)

# ③⛔有档者一律照旧：349 有废档（本日所立），其路仍走 _cold_void，非本改之路
chk('③349 有档（0922 废档），故走老路', K._cold_有档(349), True)
chk('③之二·349 由 _cold_void 销，⛔非由明裁销', K._cold_void(349), True)

# ④⛔旧式回灌：把明裁之记表清空，350 与 352 须当场落回欠
_记 = K._明裁之记
try:
    K._明裁之记 = ()
    _late = [n for n in sorted(K.F) if n >= 73 and K._cold_limit(n) <= 352
             and not K._cold_done(n) and not K._cold_void(n)
             and not (not K._cold_有档(n) and K._cold_明裁(n))]
    chk('④旧式回灌·无明裁之路时 350 落回欠', 350 in _late, True)
finally:
    K._明裁之记 = _记

# ⑤★而今式之下，以第352章计，⑥须为零
_今 = [n for n in sorted(K.F) if n >= 73 and K._cold_limit(n) <= 352
       and not K._cold_done(n) and not K._cold_void(n)
       and not (not K._cold_有档(n) and K._cold_明裁(n))]
chk('⑤今式·以第352章计，冷轮之欠为零', _今, [])

print('  ── %d/%d %s ──' % (ok, ok + bad, '全通' if bad == 0 else '⛔未过'))
sys.exit(0 if bad == 0 else 1)
