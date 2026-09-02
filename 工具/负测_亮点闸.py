# -*- coding: utf-8 -*-
"""负测·亮点闸（批131·293第2轮所立·九犯而未机化，今机化）
所治之伤：一坐⑬之法早已写在纸上——「凡起草毕即须落亮点段，不得留到后轮」；
        而它只报不拦。病历本记「亮点段必犯病」8次，一坐今日印「此病已犯九次」，
        而第九次正是我自己：293起草毕未落，留到第2轮才补。
数其群（令§六①②）：有版可查之章 174，亮点段落在 v01 或 v02 者 125 章，
        **落在 v03 之後者 49 章（28%）**——群成，非孤例。
本测所验者为不变量，非快照：
  ①第1轮之存版无亮点段者，当场拦；
  ②有者不因此拦（不许把闸扩成「凡存版皆拦」）；
  ③其位只在第1轮——第2轮以後不问（那时它本就该在，另有一坐⑬报之）；
  ④不报轮号之存版不受此拦（与领轮闸同律：说明一空即不认轮）；
  ⑤其向只朝前：全书106篇无亮点段之旧章不再重存，故零假红。
"""
import io, os, re, sys, glob, importlib.util as iu
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_s = iu.spec_from_file_location('_pl', os.path.join(_D, '跑轮.py'))
_m = iu.module_from_spec(_s)
_s.loader.exec_module(_m)

def L(vs):
    return {'章': 1, '版本': vs}
def v(note):
    return {'版': 'v01', '说明': note, 'hard': {}, 'soft': {'净重': 2000}}
def 出声(g):
    return any('亮点闸' in x for x in g)

_无 = '《镇冢秘术》\n\n第一章　试\n\n甲。\n'
_有 = _无 + '\n【本章亮点】\n\n**★而其骨一层**：\n①甲。\n'

h1, g1 = _m.gates(1, '第1轮·起草（感官庭）', L([]), 1, [], txt=_无)
chk('①第1轮无亮点段·当场拦', h1 and 出声(g1), True)
chk('①之b 且其语给得出处方（补齐亮点段再存）', any('处方：补齐亮点段' in x for x in g1), True)
chk('①之c 并给其尺（破折0／五逗0／半角0／拉丁字母0）',
    any('拉丁字母0' in x for x in g1), True)

h2, g2 = _m.gates(1, '第1轮·起草（感官庭）', L([]), 1, [], txt=_有)
chk('②有亮点段·此闸不出声（不许扩成「凡存版皆拦」）', 出声(g2), False)

h3, g3 = _m.gates(1, '第2轮·四堂会审', L([v('第1轮·起草')]), 1, [], txt=_无)
chk('③其位只在第1轮·第2轮不问', 出声(g3), False)

h4, g4 = _m.gates(1, '（本轮说明未填，须在回执补记开庭与真伤级别）', L([]), 1, [], txt=_无)
chk('④不报轮号者不受此拦（与领轮闸同律）', 出声(g4), False)

h5, g5 = _m.gates(1, '第1轮·起草', L([]), 1, [], force='审毕判不补', txt=_无)
chk('④之b 而 force 之口照旧在（其口係全器共用，非本闸自开）', 出声(g5), False)

# ⑤回灌：其向只朝前——旧章不再重存，故本闸於全书零假红
_旧无 = [f for f in glob.glob(os.path.join(_R, '正文', '*.md'))
         if '【本章亮点' not in io.open(f, encoding='utf-8').read()]
chk('⑤全书确有无亮点段之旧章（其数须≥1，否则本项无从验）', len(_旧无) >= 1, True)
chk('⑤之b 而本闸只在存版之路上，不扫正文目录（故旧章零假红）',
    '_liang = (_round_of(note) == 1)' in io.open(os.path.join(_D, '跑轮.py'),
                                                 encoding='utf-8').read(), True)

# ⑥回灌·旧式：把 _liang 摘掉，第1轮无亮点段者须由拦转过——证非陪跑
_src = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()
_旧 = _src.replace('    if _liang and not force:', '    if False and not force:')
_ns = {'__file__': os.path.join(_D, '跑轮.py'), '__name__': '_pl_old'}
exec(compile(_旧, '跑轮_旧式', 'exec'), _ns)
h6, g6 = _ns['gates'](1, '第1轮·起草（感官庭）', L([]), 1, [], txt=_无)
chk('⑥旧式回灌·第1轮无亮点段者放行（故此闸非陪跑）', h6 or 出声(g6), False)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
