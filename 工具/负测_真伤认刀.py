#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测·真伤认刀（2026-09-17 立·MECH-343-真伤之词 之治·其裁见 机制体检账 八十二）——
**守：`跑轮::总核` 之「无真伤之轮」须认那一刀落过没有，⛔不认「真伤」那两个字。**

★其立之由：旧判据係「文里有没有『真伤』二字」。
  **0917 亲跑 325—341 四百七十轮**：**照批134写那一行者 26 轮（5.5%）**，
  **而其文里看得出落过刀者 431 轮（91.7%）**——**它数的是那两个字出现过没有，不是那一刀落过没有。**
⛔**故本测之头一条，正是这道闸的本分**：**抄了那两个字而无一处可指之刀者，须判其无刀。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 取其式():
    """⛔自 `跑轮.py` 之码里把那一条正则原样取回来——
    ★**不许在本测里另抄一份**：抄一份即成两把尺，改了一头另一头照旧（本仓㊎之族）。"""
    s = io.open(os.path.join(根, '工具', '跑轮.py'), encoding='utf-8').read()
    m = re.search(r'_刀式 = re\.compile\((.*?)\)\n', s, re.S)
    if not m:
        return None
    return eval('re.compile(' + m.group(1) + ')', {'re': re})


def 自测():
    式 = 取其式()
    R = [('①自 跑轮.py 取得着那一条判据（⛔不另抄一份）', 式 is not None)]
    if 式 is None:
        print('  ⛔ ①自 跑轮.py 取不着 _刀式——其治已被人改掉或改名')
        print('  自测 0/1')
        return False
    案 = [
        ('②⛔抄了那两个字而无一处可指之刀 → 须判无刀',
         '本轮真伤两根。逐条核过皆合。', False),
        ('③⛔只说有伤而不说落在哪儿 → 须判无刀',
         '本轮有真伤，判合。', False),
        ('④真落过刀而不写那两个字 → 须判有刀',
         '拍十二删去叙者自报之判一句，净减十一字。', True),
        ('⑤补N字之形（含廿卅两之数）→ 须判有刀',
         '拍三十五补廿四字：这一根的眼我也数了一遍。', True),
        ('⑥净增之形 → 须判有刀', '本路净增三十字。', True),
        ('⑦改作之形 → 须判有刀', '旧句改作「他两只手都不在包上」。', True),
        ('⑧⛔判不补而无刀 → 须判无刀',
         '第13轮·判不补·记因：四处判合逐处回原文重判，零翻案。', False),
    ]
    for 名, 文, 期 in 案:
        R.append((名, bool(式.search(文)) == 期))
    # ⑨⛔那两个字本身不许算一刀（与②③同骨，另立一条免人删了②③）
    R.append(('⑨⛔「真伤」二字本身不算一刀', not 式.search('真伤')))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    好 = sum(1 for _, o in R if o)
    print('  负测·真伤认刀 %d/%d%s' % (好, len(R), ' 全通' if 好 == len(R) else ' ⛔有败'))
    return 好 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 自测() else 1)
