#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测 · `开轮六检::⑲` 之卡口（2026-09-17 立·其裁在 `设定/裁_0917_开轮六检⑲_…md`）

★**本器立於治之前，不立於治之後**——⛔**故它今日是红的，而那正是它要记的那件事。**

★★**其所守者一句**：**⑲ 给开镜卡开的那个口，须读那四个字後头的值，
  且其值须与「近三章同朝之那一个向」不同**；⛔**只问那四个字在不在，不算。**

★★★**其由（0917 磁盘之印·非纸上之议）**：
  **342 之卡明写其向係「往内」，而 340／341／342 三章逐个作往内**——
  **照理当红，而 ⑲ 印出来的是**：
      「★前三章皆朝「往内（查自己）」，而本章之开镜卡**已明写换向 ✓**」
  ⛔**同一行字里前半句说三章皆往内，後半句说已明写换向。**
  ★**其根在 `check19` 之末路只跑一句 `if ('换向' in _k) or ('本章之向' in _k)`**——
  **而那四个字正是开镜卡模子自己印上去的格名**（其模在 `工具/第零轮开镜庭.py`）；
  ★★**故凡有卡之章，这一条逃路一律开着**（0917 亲数：有卡 142 份，含那四个字者 **117 份**）。

⛔**本器今日不接进 `全测.py`**——**一道明知是红的测接进全测，即是拿全测去拦所有人的路**；
  ★**其接进之时，正是 `开轮六检.py` 那一处落码之日**（`开轮六检.py` 係诸席在用之器，律⑮）。

〔1119 死规之审·gates18/docs12〕⑲ 入 `_软报`：三局所验之侦一字不动（check19 本身不动）；
  另添二格（软报之格）：⑲ 侦得之红经 `run()` ⛔计入拦（rc 0）｜⛔守牙：硬检（⑬）一红照旧拦（rc 2）。

用法：
    python3 工具/负测_向之口.py          # 三局逐局跑
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as _iu
import io, os, shutil, sys, tempfile

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _取器():
    sp = _iu.spec_from_file_location('_lz6_负测', os.path.join(根, '工具', '开轮六检.py'))
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _摆一盘(tmp, 卡之文, 向=None):
    """★摆三章同朝之局：N-3／N-2／N-1 三章之卡皆书同一个向，第 N 章之卡由参数给。
    ⛔三章之号当场算出，不写死（免落成一张快照钉进一条常令·㊸）。"""
    向 = 向 or ('往' + '内')
    os.makedirs(os.path.join(tmp, '正文'), exist_ok=True)
    for k in (1, 2, 3):
        d = os.path.join(tmp, '版本', '第%d章' % (900 + k))
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, '_开镜卡.md'), 'w', encoding='utf-8').write(
            '- **本章之向**：**%s**\n' % 向)
    d4 = os.path.join(tmp, '版本', '第904章')
    os.makedirs(d4, exist_ok=True)
    if 卡之文 is not None:
        io.open(os.path.join(d4, '_开镜卡.md'), 'w', encoding='utf-8').write(卡之文)
    return {901: 'x', 902: 'x', 903: 'x'}


def _跑一局(卡之文):
    m = _取器()
    tmp = tempfile.mkdtemp(prefix='负测_向之口_')
    try:
        F = _摆一盘(tmp, 卡之文)
        m.ROOT = tmp
        m.F = F
        out = m.check19(904)
        return out[0][1], out[0][2]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _跑闸(m, 真检, cur, 硬红=False):
    """〔1119 死规之审·gates18〕余检一律换作恒绿之桩，只留「真检」照跑，看 run() 拦不拦。
    硬红=True 另令 ⑬ 亮点段 红（守牙）。返 (rc, --静 之印)。"""
    import contextlib
    诸 = ('check3', 'check5', 'check7', 'check10', 'check11', 'check12', 'check13',
          'check15', 'check16', 'check17', 'check18', 'check19', 'check20')
    旧 = dict((k, getattr(m, k)) for k in 诸)
    try:
        for k in 诸:
            if k != 真检:
                setattr(m, k, lambda *a, _k=k: [('桩·' + _k, True, '桩')])
        if 硬红:
            m.check13 = lambda *a: [('⑬·亮点段', False, '⛔桩：无亮点段')]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.run([cur], True)
        return rc, buf.getvalue()
    finally:
        for k, v in 旧.items():
            setattr(m, k, v)


def _软报之局(卡之文, 硬红=False):
    m = _取器()
    tmp = tempfile.mkdtemp(prefix='负测_向之口_')
    try:
        m.ROOT = tmp
        m.F = _摆一盘(tmp, 卡之文)
        侦 = m.check19(904)[0]
        rc, 印 = _跑闸(m, 'check19', 904, 硬红)
        return 侦, rc, 印
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def 跑():
    格 = '本章' + '之向'          # ⛔当场拼出，不写死（免本档自己被别的哨当成真处方／真格名）
    内 = '往' + '内'
    外 = '往' + '外'
    局 = []

    # ①⛔卡上之值正是三章同朝之那一个 → 须判红（旧式於此判绿，故非陪跑）
    绿1, 语1 = _跑一局('- **%s**：**%s**\n' % (格, 内))
    局.append(('①卡之值＝近三章同朝之向（%s）须判红' % 内, 绿1 is False, 语1))

    # ②⛔卡上只有格名而无值 → 须判红（此正是那条逃路之本形）
    绿2, 语2 = _跑一局('## ★★★之二·%s（模子自印之格名，其後无值）\n' % 格)
    局.append(('②卡上只有格名而无值，须判红', 绿2 is False, 语2))

    # ③★卡之值与三章同朝之向不同 → 须判绿（证没把它改瞎）
    绿3, 语3 = _跑一局('- **%s**：**%s**\n' % (格, 外))
    局.append(('③卡之值≠近三章同朝之向（%s）须判绿' % 外, 绿3 is True, 语3))

    print('════ 负测 · ⑲之卡口 ════（守：那个口须读值，不只读格名）')
    过 = 0
    for 名, ok, 语 in 局:
        print(('  ✓ ' if ok else '  ⛔ ') + 名)
        print('     其印：%s' % str(语)[:110])
        过 += 1 if ok else 0
    print('  三局 %d/3' % 过)

    # ── 〔1119 死规之审·gates18/docs12〕软报之格：⑲ 侦得照旧，⛔计入拦；硬检照旧拦 ──
    软 = []
    侦, rc, 印 = _软报之局('- **%s**：**%s**\n' % (格, 内))
    软.append(('④⑲侦得（ok=False）而 run() ⛔计入拦：rc 0、--静 印「通过」',
               侦[1] is False and rc == 0 and '开轮十六检通过' in 印, 印.strip()))
    侦2, rc2, 印2 = _软报之局('- **%s**：**%s**\n' % (格, 内), 硬红=True)
    软.append(('⑤⛔守牙：同局而硬检（⑬）一红 → rc 2，且 --静 之败单只列 ⑬、⛔混进 ⑲',
               rc2 == 2 and '⑬' in 印2 and '⑲' not in 印2, 印2.strip()))
    软过 = 0
    for 名, ok, 语 in 软:
        print(('  ✓ ' if ok else '  ⛔ ') + 名)
        print('     其印：%s' % str(语)[:110])
        软过 += 1 if ok else 0
    print('  软报 %d/%d' % (软过, len(软)))
    if 过 < 3:
        print('  ⛔**并及③今日这一个绿，係陪跑之绿，不算数**：'
              '**那条逃路此刻对三局一律放行**——'
              '**③之绿不是它判对了，是它恰好落在本局所要的那一边**；'
              '★**故此绿之值，要到治落之後方才有**。')
        print('  ⛔**今日之红係已知之红**：其治之形已写死在'
              '`设定/裁_0917_开轮六检⑲_卡之口只验有没有那四个字.md` 第三节；')
        print('  ⛔**其码待无席之窗**（`开轮六检.py` 係诸席在用之器，律⑮）。')
    return 过 == 3 and 软过 == len(软)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
