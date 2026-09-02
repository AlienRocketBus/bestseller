# -*- coding: utf-8 -*-
"""负测·功力回检第五路（批131·292第12轮·极限轮所立）
所治之伤：丁2·功力回检至今五修，前四修皆是「再加几个词」（08-19／08-21／08-22／08-22再修）。
        而一道靠加词修的闸，每加一个词就多一个「写这个词即可蒙混」的口，
        且它照旧看不见没写那个词的活。
        292第7轮之轮记里有十一版回灌表、一个相关系数、一处「42→27」，是全十轮量得最细的一轮，
        而器判它「五路俱无·走了过场」——器报的不是活没干，是器看不见活。
本测所验者为不变量，非快照：
  ①第五路读的是台账（正文之实动），不是轮记之词——写什么词也蒙混不了；
  ②一轮若正文一字未动且轮记无实，仍须判⚠（不许把闸修成人人皆绿）；
  ③每一轮之绿须印出「凭何而绿」，见得出它是靠轮记之实还是只靠正文动过。
"""
import io, os, re, sys, json, shutil, tempfile, subprocess
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_src = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()
chk('①第五路须读台账，不读轮记之词', "_轮版动否" in _src and "['版本']" in _src, True)
chk('①之b 且其判据係净重之差（正文实动），非任何词表',
    "_cur - _pre" in _src and "_轮版动否[_rr]" in _src, True)
chk('③绿须印出「凭何而绿」', "'｜凭：'" in _src, True)
chk('③之b 而无凭者不许印凭（⚠那一行不许挂一条空的凭）',
    "if _by else ''" in _src, True)
chk('②闸未被改成人人皆绿——⚠之路仍在', "_idle.append(_r)" in _src, True)

# ── 实跑：造一本假账，第A轮正文动过而轮记无一词，第B轮两皆无 ──
tmp = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp, '工具'))
    shutil.copy(os.path.join(_D, '跑轮.py'), os.path.join(tmp, '工具', '跑轮.py'))
    vd = os.path.join(tmp, '版本', '第999章'); os.makedirs(vd)
    io.open(os.path.join(vd, '_台账.json'), 'w', encoding='utf-8').write(json.dumps({'章': 999, '版本': [
        {'版': 'v01', '说明': '第1轮·起草', 'hard': {}, 'soft': {'净重': 2000}},
        {'版': 'v02', '说明': '第2轮·四堂会审', 'hard': {}, 'soft': {'净重': 2140}},
        {'版': 'v03', '说明': '第3轮·挑刺王', 'hard': {}, 'soft': {'净重': 2140}},
    ]}, ensure_ascii=False, indent=1))
    io.open(os.path.join(vd, '_轮记.md'), 'w', encoding='utf-8').write(
        '# 第999章 · 轮记\n\n'
        '## 第1轮·起草\n本轮判合，无可再说。\n\n'
        '## 第2轮·四堂会审\n本轮四堂逐一读过，判合。\n\n'   # 一个动手之词也没有，而正文动了140字
        '## 第3轮·挑刺王\n本轮读毕，判合。\n')             # 词无、正文亦未动
    os.makedirs(os.path.join(tmp, '正文'))
    io.open(os.path.join(tmp, '正文', '镇冢秘术_第九百九十九章_试.md'), 'w', encoding='utf-8').write(
        '《镇冢秘术》\n\n第九百九十九章　试\n\n第一日。\n\n＊\n\n她把册子抽出来。\n')
    p = subprocess.run([sys.executable, os.path.join(tmp, '工具', '跑轮.py'), '--尽力', '999'],
                       cwd=tmp, capture_output=True, text=True)
    out = (p.stdout or '') + (p.stderr or '')
    行 = {int(m.group(1)): m.group(0) for m in re.finditer(r'第(\d+) ?轮 真伤.*', out)}
    chk('④第2轮·轮记无一动手之词而正文动了140字·须绿',
        2 in 行 and '✓' in 行[2], True)
    chk('④之b 且其凭须明写「正文实动」（而非假托一个词）',
        2 in 行 and '正文实动+140字' in 行[2], True)
    chk('⑤第3轮·词无、正文亦未动·仍须⚠（证非人人皆绿）',
        3 in 行 and '⚠' in 行[3], True)
    chk('⑤之b 且⚠那一行不许挂凭', 3 in 行 and '凭：' not in 行[3], True)
    # 末了那一行係「第A、B轮无动手之痕」之合并式；查的是「3 在其名单里」，不是那一行长什么样。
    import re as _re
    _mm = _re.search(r'第([\d、]+)轮无动手之痕', out)
    chk('⑤之c 并须在末了点名那一轮', bool(_mm) and '3' in _mm.group(1).split('、'), True)

    # 旧式回灌：把第五路摘掉，第2轮须由绿转⚠——证此路非陪跑
    _old = io.open(os.path.join(tmp, '工具', '跑轮.py'), encoding='utf-8').read()
    _old = _old.replace("        if _tz: _by.append('正文实动%+d字' % _tz)\n", "")
    io.open(os.path.join(tmp, '工具', '跑轮.py'), 'w', encoding='utf-8').write(_old)
    p2 = subprocess.run([sys.executable, os.path.join(tmp, '工具', '跑轮.py'), '--尽力', '999'],
                        cwd=tmp, capture_output=True, text=True)
    out2 = (p2.stdout or '') + (p2.stderr or '')
    行2 = {int(m.group(1)): m.group(0) for m in re.finditer(r'第(\d+) ?轮 真伤.*', out2)}
    chk('⑥旧式回灌·第2轮须由绿转⚠（一份在旧式下也全过的测就是陪跑）',
        2 in 行2 and '⚠' in 行2[2], True)
    chk('⑥之b 而第3轮两式同判⚠（证新路只补它看不见的那一样，不放走真过场）',
        3 in 行2 and '⚠' in 行2[3], True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ── 三·轮记切块：一、二级标题皆须认（292第13轮甲实见） ──
# 其形：切块只认「\n## 」，而第11、12轮之标题写作「\n# 」；
#      其果不是漏掉那两轮，**是把那两轮的活并进了第10轮**——记错头比漏记更险：
#      漏记看得出少了一行，记错看着一切正常。
tmp2 = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp2, '工具')); os.makedirs(os.path.join(tmp2, '正文'))
    shutil.copy(os.path.join(_D, '跑轮.py'), os.path.join(tmp2, '工具', '跑轮.py'))
    vd2 = os.path.join(tmp2, '版本', '第998章'); os.makedirs(vd2)
    io.open(os.path.join(vd2, '_台账.json'), 'w', encoding='utf-8').write(json.dumps({'章': 998, '版本': [
        {'版': 'v01', '说明': '第1轮·起草', 'hard': {}, 'soft': {'净重': 2000}},
        {'版': 'v02', '说明': '第2轮·四堂会审', 'hard': {}, 'soft': {'净重': 2100}},
    ]}, ensure_ascii=False, indent=1))
    io.open(os.path.join(vd2, '_轮记.md'), 'w', encoding='utf-8').write(
        '# 第998章 · 轮记\n\n'
        '## 第1轮·起草\n本轮真伤1根，其治已落。\n\n'
        '# 第2轮·四堂会审\n本轮真伤2根，其治二处，复量复量。\n')   # 一级标题
    io.open(os.path.join(tmp2, '正文', '镇冢秘术_第九百九十八章_试.md'), 'w', encoding='utf-8').write(
        '《镇冢秘术》\n\n第九百九十八章　试\n\n第一日。\n\n＊\n\n她把册子抽出来。\n')
    p3 = subprocess.run([sys.executable, os.path.join(tmp2, '工具', '跑轮.py'), '--尽力', '998'],
                        cwd=tmp2, capture_output=True, text=True)
    o3 = (p3.stdout or '') + (p3.stderr or '')
    chk('⑦一级标题之轮须认得出（不许并进前一轮）',
        bool(re.search(r'第2 ?轮 真伤', o3)), True)
    chk('⑦之b 而前一轮不许因此长出别人的数（第1轮真伤须仍为1）',
        bool(re.search(r'第1 ?轮 真伤1 ', o3)), True)
    chk('⑧须并印「轮记见N轮｜台账见M轮」两数', '轮记见' in o3 and '台账见' in o3, True)
    # 轮记有而台账无：加第3轮之话而不加其版
    io.open(os.path.join(vd2, '_轮记.md'), 'a', encoding='utf-8').write(
        '\n## 第3轮·挑刺王\n本轮真伤1根，其治已落。\n')
    p4 = subprocess.run([sys.executable, os.path.join(tmp2, '工具', '跑轮.py'), '--尽力', '998'],
                        cwd=tmp2, capture_output=True, text=True)
    o4 = (p4.stdout or '') + (p4.stderr or '')
    chk('⑧之b 轮记有而台账无者·须出声', '轮记有而台账无' in o4, True)
finally:
    shutil.rmtree(tmp2, ignore_errors=True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
