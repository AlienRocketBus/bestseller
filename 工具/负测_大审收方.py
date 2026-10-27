# -*- coding: utf-8 -*-
"""负测·大审收方（2026-09-23·限359 立·随 `大审.py::收` 之补两名同日）。
★所守者：**一册之裁定表，几行算「有人收」。**
★★其立之由：本坐填「至第357章」一册时，落了两样旧式不认的真判——
  **「半治·半驳」**（取其半、驳其半）与**「留痕·不裁」**（一席自书无致命之判·坑㉗）——
  ⛔**旧式各算一行「没人收」**，**於是本器逼着填册的人把它们改写成假的「已治」或「判驳」**。
  ★★★**一道闸若逼着人为过它而改判，那道闸就是在教人说谎**（④之五之律）。
⛔**而本测之重不在「新名认不认得」，在「口开宽了之後，空模子还拦不拦得住」**——
  **④以旧式回灌验其非陪跑，⑤⑥守其窄。**"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys, importlib.util

_D = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location('dz', os.path.join(_D, '大审.py'))
_m = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_m)

案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得 %r 期 %r' % (得, 期)))


def 收数(行们):
    """★照 `大审.py` 本身那一式复算（⛔不另写一式，否则测的是我自己写的那一个）。"""
    src = io.open(os.path.join(_D, '大审.py'), encoding='utf-8').read()
    新 = ("'已治' in x or '判驳' in x or '判不治' in x\n"
          "                      or '半治' in x or '留痕·不裁' in x")
    assert 新 in src, '⛔器之式已改，本测须同日随之改'
    n = 0
    for x in 行们:
        if ('已治' in x or '判驳' in x or '判不治' in x
                or '半治' in x or '留痕·不裁' in x
                or ('已挂' in x and re.search(r'限\s*\d+', x))):
            n += 1
    return n


_旧式 = lambda 行们: len([x for x in 行们
                        if ('已治' in x or '判驳' in x or '判不治' in x
                            or ('已挂' in x and re.search(r'限\s*\d+', x)))])

# ① 四样旧名照旧认得
chk('①已治', 收数(['| 1 | a | b | **已治** | c |']), 1)
chk('①之b 判驳', 收数(['| 1 | a | b | **判驳** | c |']), 1)
chk('①之c 已挂带限', 收数(['| 1 | a | b | **已挂·限 362** | c |']), 1)
# ② 新补两名
chk('②半治·半驳', 收数(['| 1 | a | b | **半治·半驳** | c |']), 1)
chk('②之b 留痕·不裁', 收数(['| 1 | a | b | **留痕·不裁** | c |']), 1)
# ③ ⛔空模子照旧拦得住（口开宽了而这一样一格没放松）
chk('③⛔「⛔待裁」之模子仍算没人收', 收数(['| 1 | | | ⛔待裁／已治／判驳／已挂 | |']), 1)
#   ★★★上一行之期是 1 而非 0，其由：**模子那一行里字面就含「已治」「判驳」**——
#     ⛔**故空模子之防不在本判，在 `空模子()`**；本测④正为着把这一层写明，免後坐误以为本判在守它。
chk('③之b ⛔而空模子之真防在 `空模子()`，它照旧逮得出',
    _m.空模子.__doc__ is not None and '模子之记号还在' in _m.空模子.__doc__, True)
chk('③之c ⛔一行全空者，新旧二式皆算没人收',
    (收数(['| 1 | | | | |']), _旧式(['| 1 | | | | |'])), (0, 0))
# ④ ⛔旧式回灌：本坐今日那两行，旧式之下皆算「没人收」（证本改治的是真伤）
_两行 = ['| 6 | 编辑席 | 357:53 | **半治·半驳** | 取其半，驳其移末拍之议 |',
         '| 12 | 冷起手席·无致命之判 | — | **留痕·不裁** | 交白卷而说得出何以白 |']
chk('④旧式回灌·那两行旧式之下算 0 行有人收', _旧式(_两行), 0)
chk('④之b 而新式之下算 2 行', 收数(_两行), 2)
# ⑤ ⛔其口极窄：单一个「治」「驳」「挂」字不算
chk('⑤单一个「治」字不算', 收数(['| 1 | a | b | 治 | c |']), 0)
chk('⑤之b 单一个「驳」字不算', 收数(['| 1 | a | b | 驳 | c |']), 0)
chk('⑤之c 「半驳」独一个亦不算（须「半治」或「留痕·不裁」整词）',
    收数(['| 1 | a | b | 半驳 | c |']), 0)
chk('⑤之d ⛔「已挂」无限者照旧不算', 收数(['| 1 | a | b | **已挂** | c |']), 0)
# ⑥ ★真册回灌：今日所填之册，十二行须行行有收
_p = os.path.join(os.path.dirname(_D), '设定', '大审_至第357章.md')
if os.path.exists(_p):
    _t = io.open(_p, encoding='utf-8').read()
    _sec = _t.split('## 三·逐笔裁定')[1].split('## 四·')[0]
    _rows = [x for x in _sec.splitlines()
             if x.strip().startswith('|') and x.count('|') >= 5
             and not re.match(r'^\s*\|[\s\-:|]+\|\s*$', x)
             and '判（席·题）' not in x]
    chk('⑥真册回灌·至第357章一册十二行', len(_rows), 12)
    chk('⑥之b 且行行有收（⛔一行没收即此册不算一回大审）', 收数(_rows), len(_rows))

坏 = [x for x in 案 if not x[1]]
print('════ 负测·大审收方 ════（守：一册之裁定表几行算「有人收」）')
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
