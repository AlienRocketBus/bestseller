# -*- coding: utf-8 -*-
"""负测·段间空行闸（批131）
所治之伤：段间空行之检原查全文，而【本章亮点】係markdown列行，行行紧挨本就无空行；
        故全书292章中55章长红，而其白文内命中皆为0——一个只会假红的闸。
        阅读器那一头更进一步：为堵这噪，加了「七十／八十」一条赦令，只对两批章号硬拦，余者一概「不拦」。
本测所验者为不变量，非快照：
  ①亮点段之列行不许再算漏空行（不论其形如何）；
  ②白文内真漏空行必被逮（新旧两器皆然）；
  ③阅读器不许再按章号赦免——白文漏空行，哪一章都拦。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

尾 = '\n\n【本章亮点】\n\n**★★本章之一事**：她今天要写第十八行。\n①**★第十八行没有**。★昨天推不动。\n**★★★★★而某章之位**：暗线｜常章｜向＝往内｜形＝记账。\n**二线之距：主线第一百零三天／暗线第九十七日，今差六日。**\n'
白 = '《镇冢秘术》\n\n第九百九十九章　试\n\n第一日。天没亮。\n\n＊\n\n她把册子抽出来。\n'
白漏 = '《镇冢秘术》\n\n第九百九十九章　试\n\n第一日。天没亮。\n她把册子抽出来。\n\n＊\n\n剩一个。\n'

# ── 一·检察官改动闸 ──
spec = importlib.util.spec_from_file_location('_jc', os.path.join(os.path.dirname(os.path.abspath(__file__)), '小说检察官.py'))
_src = io.open(spec.origin, encoding='utf-8').read()
新式 = '_bw = new.split' in _src
# ★2026-09-05·机制总审：式由 [。！？”] 扩为 [。！？”＊]（与 硬闸.py 同式；245 章「＊\n正文」一处实有），此处随之。
chk('①检察官已改为只查白文（不是把闸删了）', 新式 and "re.search(r'[。！？”＊]" in _src, True)
chk('①之b 且白文漏空行仍计入 bad（不是降成只报不拦）', 新式 and 'if _lk: bad += 1' in _src, True)

def 判(txt):
    _bw = txt.split('【本章亮点')[0]
    return bool(re.search(r'[。！？”＊]\n(?!\n)(?=[^\n])', _bw))
def 旧判(txt):
    return bool(re.search(r'。\n(?!\n)(?=[^\n])', txt))

chk('②亮点段之列行·新式不报', 判(白 + 尾), False)
chk('②之b 而旧式在此正是长红者（本测若在旧器上跑必坏）', 旧判(白 + 尾), True)
chk('③白文真漏空行·新式必逮', 判(白漏 + 尾), True)
chk('③之b 带亮点段亦逮（不许因尾巴一红就把白文那一红盖过去）', 判(白漏 + 尾) and not 判(白 + 尾), True)
chk('④问号叹号引号收尾亦逮（非只逮句号）', 判('甲。\n\n＊\n\n他问了一句？\n答了。\n' ), True)

# ── 二·阅读器P14 ──
_rd = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '同步全本阅读器.py'), encoding='utf-8').read()
chk('⑤阅读器已撤「七十／八十」之赦', ('"七十"' in _rd or '「七十」' in _rd.replace('批131','')) and 'if _new:' in _rd, False)
# 注：此项查的是「出路」——即那一条 print 而不 raise 的路，非查字面。
# 头一版写成 '存量待补' in _rd，被我自己注释里那四个字判坏；字面之查逮的是话，不是路。
chk('⑤之b 且不再有「存量待补(不拦)」这一条出路',
    any(l.lstrip().startswith('print(') and '存量待补' in l for l in _rd.split('\n')), False)
chk('⑤之c 而其检未被删——白文漏空行仍 SystemExit', '_P14.append(path.name)' in _rd and 'raise SystemExit("段间漏空行' in _rd, True)
chk('⑥阅读器之检须落在亮点段切开之後（否则改的只是话，不是位）',
    _rd.find('hl_part.strip().split()') < _rd.find('_P14.append(path.name)'), True)

# ── 三·全书实测（不变量：白文内无一章漏空行；若日後有，本测即当场坏，这正是要的） ──
根 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '正文')
坏章 = []
for f in sorted(os.listdir(根)):
    if not f.endswith('.md'): continue
    if 判(io.open(os.path.join(根, f), encoding='utf-8').read()): 坏章.append(f)
chk('⑦全书白文内漏空行为0（撤赦之凭据）', 坏章, [])
假红 = sum(1 for f in sorted(os.listdir(根)) if f.endswith('.md')
           and 旧判(io.open(os.path.join(根, f), encoding='utf-8').read()))
chk('⑧而旧式在全书上假红须≥20章（凭据：这是「只会假红」之实测，非本席之说）', 假红 >= 20, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
