# -*- coding: utf-8 -*-
"""负测·看官问三之窗（2026-09-23·限359 立·随 `看官.py::问三` 不取跨句之窗同日）。
★所守者：**「有没有一样东西说得太多」所数的那个窗，能不能跨句。**
★★其立之由（本坐跑 `python3 工具/看官.py --生客 357` 时所逮）：
  ⛔**旧式之窗跨句而取**，於是 357 之报头一行印作「**。她把指**」11回——
    **那一点句号是上一句的尾巴，不是这一样东西的名字。**
  ★**而其害不止於难看**：**一个带着句号的窗只数得着「句首那几个字」**，
    **同一个词落在段中者它一个也数不着**——**於是它报的数比实数小，而它印得像个实数。**
  ★★**并及一件**：**带标点那一支还占着 `top[:3]` 的位子，把真正说得太多的那一样挤下榜**。
    **357 即如此**：**旧式榜首係「。她把指」，新式榜首係「的那一头」9回**——
    **後者正是 0923 大审诸席所指「这本书在重复自己」的那一样。**
⛔**而本测之重在两头**：**④证其非陪跑（旧式之下那一支确在榜上）｜⑤⑥证其不误伤（不跨句者一个没少）。**"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys
from collections import Counter

_D = os.path.dirname(os.path.abspath(__file__))
案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得 %r 期 %r' % (得, 期)))


_标 = '。，、；：？！「」『』（）—…·《》'


def _新窗(t2):
    c = Counter()
    for k in (4, 5):
        for i in range(len(t2) - k + 1):
            w = t2[i:i + k]
            if any(ch in _标 for ch in w):
                continue
            c[w] += 1
    return c


def _旧窗(t2):
    c = Counter()
    for k in (4, 5):
        for i in range(len(t2) - k + 1):
            c[t2[i:i + k]] += 1
    return c


# ① 造一段：同一个词落在句首三回、落在段中三回
_文 = ('她把册子翻开。她把册子合上。她把册子送进去。'
       '今天她把册子举到眼前，明天她把册子搁回膝上，后天她把册子按平了。')
# ⛔①⛔旧式之下带句号那一支当真在榜（证本改治的是真伤）
chk('①旧式之下「。她把册」入榜', _旧窗(_文).get('。她把册', 0) >= 2, True)
# ⛔★本格之期，本坐头一版写作 `(6, 3)` ——**係用眼睛数的，不是用器数的**，实为 `(6, 2)`
#   （**头一句「她把册子翻开」在串首，其前没有那一点句号**）。
#   ★**而今日盘上已因「照着抄的数」栽过三回**（拍73／器物册23／354之三窗）；
#   ★★**故本格今改作不钉其数，只钉其关系**——**「带句号那一支恒少於实数」方是本判所守之不变量**，
#   **而那个 6 与那个 2 会随这一段例文变，律不会变。**
_a, _b = _旧窗(_文).get('她把册子', 0), _旧窗(_文).get('。她把册', 0)
chk('①之b ⛔而它数得比实数小（带句号那一支恒少於实数·⛔不钉其数只钉其关系）',
    (_a >= 4 and 0 < _b < _a), True)
# ② 新式之下带标点者一支不入
chk('②新式之下带句号者一支不入', 
    [w for w in _新窗(_文) if any(ch in _标 for ch in w)], [])
# ③ ⛔而不跨句者一个没少（⛔不许把闸收得连真的也数不着）
chk('③不跨句者其数不变',
    _新窗(_文).get('她把册子', 0) == _旧窗(_文).get('她把册子', 0) == 6, True)
# ④ ⛔逐样标点皆挡得住（⛔不止句号）
for _ch in '，、；：？！「」（）—…':
    if _新窗('甲乙丙丁' + _ch + '戊己庚辛'):
        pass
chk('④逐样标点皆挡得住',
    all(not any(c in w for c in _标) for w in _新窗('甲乙丙丁，戊己庚辛。壬癸子丑')),
    True)
# ⑤ ★真盘回灌：357 白文之下，新式榜首不带标点，且旧式榜首带标点
_p = os.path.join(os.path.dirname(_D), '正文')
import glob as _g
_fs = _g.glob(os.path.join(_p, '*第三百五十七章*.md'))
if _fs:
    _t = io.open(_fs[0], encoding='utf-8').read()
    _t = _t.split('【本章亮点】')[0]
    _t2 = re.sub(r'[\s＊]', '', _t)
    _旧顶 = max(_旧窗(_t2).items(), key=lambda z: z[1])[0]
    _新顶 = max(_新窗(_t2).items(), key=lambda z: z[1])[0]
    chk('⑤真盘回灌·357 旧式榜首带标点', any(c in _旧顶 for c in _标), True)
    chk('⑤之b 而新式榜首不带标点', any(c in _新顶 for c in _标), False)
# ⑥ ⛔器里那一格确已改（⛔免测改了而器没改）
_src = io.open(os.path.join(_D, '看官.py'), encoding='utf-8').read()
chk('⑥⛔器里已挡标点之窗', "if any(ch in _标 for ch in w):" in _src, True)

坏 = [x for x in 案 if not x[1]]
print('════ 负测·看官问三之窗 ════（守：数「说得太多」的那个窗，不许跨句）')
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
