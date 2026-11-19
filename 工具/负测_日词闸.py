# -*- coding: utf-8 -*-
"""①之c·一章一日（章首日词唯一）负测（2026-08-28 立·随「补零〇」同日）。
★其立之由（287第1轮所逮）：其式原作 [一二三四五六七八九十百]，不含零／〇，
  ★★遂使凡带零之日号一律漏认，且报的是「0 处」而非报错——静默之误，闸看着在跑而实已失灵。
★★★令九·③：写下来的法不生效，只有变成闸才生效。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, re, importlib.util

spec = importlib.util.spec_from_file_location('q3', '工具/质量三闸.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

m.lunji = lambda c: '本章之一事：随便一件。'
m.is_dark = lambda c: False
m.net = lambda b: 3000


def 跑(体):
    m.body = lambda c: 体
    for 名, ok, 语 in m.gate1(0):
        if '①之c' in 名:
            return ok, 语
    return None, None


def 造(*日):
    # ★题头之内不许出现任何日词（此测具头一跑即栽在这里：我写的题头里就有一个日号）
    拍 = '\n\n＊\n\n'.join(list(日) + ['随便一句。'])
    return 拍 + '\n'


案 = []


def _数(语):
    """★只取其所报之处数，不锁其措辞。
    ★★其立之由（2026-09-23·限359所逮）：器之语後添了「章首」二字（起手哨同日所改），
      ★★★而此测原以整个 (ok, 语) 对等相比，遂十一项尽坏——坏的是测的措辞，不是闸。
      ⛔而不许改作「语中含『1 处』」了事：那样「11 处」也含「1 处」，闸失灵而测仍绿。
      故取整数相比——措辞可漂，处数不可漂。"""
    m = re.search(r'(\d+)\s*处', 语 or '')
    return int(m.group(1)) if m else None


def chk(名, 实, 期):
    ok, 语 = 实
    期ok, 期数 = 期
    过 = (ok == 期ok) and (_数(语) == 期数)
    案.append((名, 过, '实=%r（处数 %r） 期=(%r, %r 处)' % (实, _数(语), 期ok, 期数)))

for s in ['第一百天。', '第九十九天，天没亮我就醒了。', '第九十四日，她先去灶上。',
          '第一百零一天。', '第一百零九天。', '第二百零五天。', '第一百一十天。']:
    chk('①单日须认得：%s' % s.rstrip('。')[:8], 跑(造(s)), (True, 1))

for a, b in [('第一百天。', '第一百零一天。'), ('第一百零一天。', '第一百零二天。'),
             ('第九十九天。', '第一百天。')]:
    chk('②一章二日须拦：%s＋%s' % (a.rstrip('。'), b.rstrip('。')), 跑(造(a, b)), (False, 2))

# 〔1119 死规之审·gates5〕①之c 章首无日词而全章亦无者只 ⚠ 交判（X115：466:9 为过此闸所插之句·大审470 致命#1）；②一章二日照拦（守牙）
_r3 = 跑(造('天没亮。'))
chk('③无日词只 ⚠ 不拦（其语带「⚠白文无日词」）', (_r3[0] is True and '⚠白文无日词' in (_r3[1] or ''), _r3[1]), (True, 0))

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
