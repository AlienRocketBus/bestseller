# -*- coding: utf-8 -*-
"""存版·阅读器过期即报 负测（2026-09-01 立·随其闸同日）。
★其立之由（287第2轮所逮）：每轮改文之后阅读器即过期，而医生／检察官自测／全书检
  三项俱据之报红，遂使每一轮之推送皆被拦一回；而其治只一条命令，难只在「想不起来」。
★★故此测专问：它该催的时候催不催，不该催的时候闭不闭嘴，器崩的时候会不会静默。
★★★而末一项最要紧：一个「看不懂就当没事」的催，比没有更坏。"""
import sys, os, types, importlib.util

spec = importlib.util.spec_from_file_location('pl', '工具/跑轮.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

案 = []
def chk(名, 实, 期):
    案.append((名, 实 == 期, '实=%r 期=%r' % (实, 期)))

def 假器(out='', 崩=False):
    def _c():
        if 崩:
            raise OSError('器崩了')
        return out
    return _c

if True:
    F = 假器('阅读器同步检查通过：287 章\n')
    chk('①同步之时·不许催', m._reader_stale(F), [])

    F = 假器('阅读器未与正文同步；请运行：python3 工具/同步全本阅读器.py\n')
    行 = m._reader_stale(F)
    chk('②过期之时·须催', len(行) >= 1, True)
    chk('②之b 催语须带处方', any('同步全本阅读器.py' in x for x in 行), True)
    chk('②之c 催语须点明会被拦', any('推送必被拦' in x for x in 行), True)

    F = 假器(崩=True)
    行 = m._reader_stale(F)
    chk('③器崩·不许静默', len(行) >= 1, True)

    F = 假器('')
    chk('④看不懂之时·须催（宁可多催，不可漏催）', len(m._reader_stale(F)) >= 1, True)

    F = 假器('段间漏空行(P14硬检·新章): 某章 —— 补齐空行后重跑\n')
    chk('⑤器只报P14而未言通过·须催', len(m._reader_stale(F)) >= 1, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
