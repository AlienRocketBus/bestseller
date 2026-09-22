#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测 · 冷轮之令改式（2026-09-22 立）：**无档者不凭空记一笔欠，⛔而其回执须有一句立／不立之明裁。**

★其所守者三样，逐样有旧式回灌：
  ①**有明裁者不入欠**（⛔此係本改之口）；
  ②⛔**无明裁者照旧入欠**（⛔此係本改之价——**不是把这一格废掉，是把它换了一个问法**）；
  ③⛔**有档者一律照旧走老路**（签核／废档），**本改一个字也没有碰它们**。
"""
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

# ②⛔本改之价：无档**且**无明裁者，照旧判欠——351 正是那一种（其限 353，届时当场咬）
chk('②351 无档且无明裁（⛔其限353，届时照旧入欠）',
    (K._cold_有档(351), K._cold_明裁(351)), (False, None))
_late353 = [n for n in sorted(K.F) if n >= 73 and K._cold_limit(n) <= 353
            and not K._cold_done(n) and not K._cold_void(n)
            and not (not K._cold_有档(n) and K._cold_明裁(n))]
chk('②之二·以第353章计，351 当场入欠（⛔证本改不是把这一格废掉）', 351 in _late353, True)

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
