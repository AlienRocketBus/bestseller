# -*- coding: utf-8 -*-
"""死处方哨（2026-09-16 立·体检账 七十二之器化）。

★**所守之一句**：⛔**一道闸的处方里点名的器，盘上须有那个器。**

★★**其所以要机化**：**本日一日之内逮着同族五例**——
　`章界闸`／`漂移哨`／`销立门`／`书级体检::在场之衰` 四处係「律与码不符」，
　★而第五例是这一器要逮的那一种：**`自走.py` 印的那一条，其器名末字作「卡」，
　  而盘上之器名末字係「庭」**——**照它跑，当场 can't open file**。
　⛔**并及一件当场自栽**：**本器初版把那两个器名逐字写进了这段注里**，
　**於是它头一回跑就把自己逮了出来**——**样本之名不许照写，今日第三度同栽**
　（囤灰闸之样本档名一度、338 回执之签核六字一度、本器一度）。
　⛔**并及一件当面记下**：**那一行自己的注写着「器名以磁盘为准」**——
　**写注的人知道这一条要对盘，而他没有对**；**故此事不能靠人记，只能靠器扫。**

★★★**其判之形（⛔窄，只逮一样，不扩）**：
　**凡 `.py`／`.js` 之内出现 `python3 工具/X.py` 者，`工具/X.py` 须在盘上。**
　⛔**不判其参数对不对**（那要真跑一回，不在本器之职）；
　⛔**不判 `设定/*.md` 里的引**（文书之引另有其哨）。

跑法：
    python3 工具/死处方哨.py          # 正路
    python3 工具/死处方哨.py --自测    # 负测（⛔每一格皆验其反面）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PAT = re.compile(r'python3\s+(工具/[^\s\'"`)\]]+?\.py)')


def 扫(root=None):
    """返回 [(所点之器, 点名之档)]，逐条皆「盘上没有」者。"""
    root = root or ROOT
    坏 = []
    档 = sorted(glob.glob(os.path.join(root, '工具', '*.py')) +
                glob.glob(os.path.join(root, '工具', '席', '*.js')))
    _本器 = os.path.abspath(__file__)
    for f in 档:
        # ⛔本器之档不入其扫：**它的注与沙盘里必有那些名字**，
        #   ★否则它头一回跑就逮住自己（本器初版之实）。
        if os.path.abspath(f) == _本器:
            continue
        try:
            t = open(f, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        for m in _PAT.finditer(t):
            器 = m.group(1)
            if not os.path.exists(os.path.join(root, 器)):
                坏.append((器, os.path.relpath(f, root)))
    return sorted(set(坏))


def 跑():
    坏 = 扫()
    print('════ 死处方哨 ════（守：处方里点名的器，盘上须有那个器）')
    if not 坏:
        print('  ✓死处方哨：零处（处方里点名的器，样样在盘上）。')
        return 0
    for 器, src in 坏:
        print('     ⛔ %s  ← 点名於 %s' % (器, src))
    print('  ★其治：**要么把器名改对，要么把那个器补上**；'
          '⛔**不许把那一行删掉了事**——**删了，那条处方就成了一句没人办的话。**')
    # ⛔其判须落在末一行（`全测::判末行` 只读末一行）——
    #   ★本日五十二之教训：**处方印在判之後，那把尺就取错了行。**
    print('  ⛔死处方哨：%d 处——**照它跑，当场取不着那个器**。' % len(坏))
    return 2


def 自测():
    import shutil
    import tempfile
    过, 败 = 0, []

    def chk(名, 得, 期):
        nonlocal 过
        if 得 == 期:
            过 += 1
        else:
            败.append('%s：得 %r，期 %r' % (名, 得, 期))

    tmp = tempfile.mkdtemp(prefix='zm_sfp_')
    try:
        os.makedirs(os.path.join(tmp, '工具', '席'))
        # ① 点名一个不在的器 → 须逮着
        _无 = '没有' + '这个器'
        with open(os.path.join(tmp, '工具', '甲.py'), 'w', encoding='utf-8') as f:
            f.write('# 处方：python3 工具/%s.py --立 5\n' % _无)
        chk('①点名而盘上没有者须逮着', 扫(tmp), [('工具/%s.py' % _无, '工具/甲.py')])
        # ② 其反面·把那个器补上 → 当场零（⛔证其可解，非死结；并证①非陪跑）
        with open(os.path.join(tmp, '工具', _无 + '.py'), 'w', encoding='utf-8') as f:
            f.write('#\n')
        chk('②补上那个器即零（⛔证①非陪跑，且其停可解）', 扫(tmp), [])
        # ③ 点名一个在的器 → 不许报
        with open(os.path.join(tmp, '工具', '乙.py'), 'w', encoding='utf-8') as f:
            f.write('# 处方：python3 工具/甲.py\n')
        chk('③点名而盘上有者不许报', 扫(tmp), [])
        # ④ 席之 js 亦在其扫内
        _无2 = '也没' + '有'
        with open(os.path.join(tmp, '工具', '席', '丙.js'), 'w', encoding='utf-8') as f:
            f.write('// python3 工具/%s.py\n' % _无2)
        chk('④席之 js 亦在其扫内', 扫(tmp), [('工具/%s.py' % _无2, '工具/席/丙.js')])
        # ⑤ ⛔不许把 设定/*.md 之引也扫进来（本器之职只及於器）
        os.makedirs(os.path.join(tmp, '设定'))
        _无3 = '文书里' + '点的器'
        with open(os.path.join(tmp, '设定', '丁.md'), 'w', encoding='utf-8') as f:
            f.write('python3 工具/%s.py\n' % _无3)
        chk('⑤⛔设定之 md 不在其职内（不扩其口）',
            [x for x in 扫(tmp) if _无3 in x[0]], [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ⑥ 真盘之实：今日二处已正，故正路须零
    chk('⑥真盘今日零处（自走与开轮六检那二处死处方皆已正）', 扫(), [])
    print('════ 负测·死处方哨 ════（守：处方里点名的器，盘上须有那个器）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 跑())
