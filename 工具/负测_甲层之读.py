# -*- coding: utf-8 -*-
"""负测·甲层之读（2026-09-23·限359 立·随 `书级体检::check_loss` 正其缩排同日）。
★所守者：**一章有两三份回执之时，「本章之失」那一行找不找得着。**
★★其立之由（本坐照 `自走` 之【候】跑 `书级体检` 时所逮）：
  ⛔**旧式那一个 `break` 缩排错了一级**——**在 `for f` 之内、`if m` 之外**，
    **於是它只看 `glob` 回来的头一份回执，看完即走。**
  ★**而一章之回执常有两三份**（作业单／封版席／冷轮明裁），**`本章之失` 只写在作业单上**；
    **351 头一份是「冷轮明裁」、352 头一份是「封版席」，二者皆无那一行，遂皆判「未记」。**
  ★★**其实两份作业单上那一行逐字都在。**
  ★★★**故本器那一句红说反了**：**它印「没有人判过一章」，而实情是「判过了，本器没看见」**——
    ⛔**一个看不见的器，比一个不存在的器更坏：它每跑一回都在替一件办过的事作证说没办。**
⛔**而本测之重不在「找得着」，在「①之序不许再作数」**：**④以乱序回灌，⑤守其仍答得出「真未记」。**"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys, glob, tempfile, shutil

案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得 %r 期 %r' % (得, 期)))


def _旧式(fs):
    """★旧式：`break` 在 `if m` 之外——只看头一份。"""
    rec = '未记'
    for f in fs:
        m = re.search(r'\*\*本章之失\*\*[：:]\s*(.+)',
                      io.open(f, encoding='utf-8', errors='replace').read())
        if m:
            rec = m.group(1).strip().strip('*').strip()
        break
    return rec


def _新式(fs):
    """★新式：找着了才走。"""
    rec = '未记'
    for f in sorted(fs):
        m = re.search(r'\*\*本章之失\*\*[：:]\s*(.+)',
                      io.open(f, encoding='utf-8', errors='replace').read())
        if m:
            rec = m.group(1).strip().strip('*').strip()
            break
    return rec


_T = tempfile.mkdtemp(prefix='jiaceng')
try:
    _甲 = os.path.join(_T, '回执_20260922_第900章封版席.md')     # 无那一行·序在前
    _乙 = os.path.join(_T, '回执_20260919_第900章作业单.md')     # 有那一行·序在後
    io.open(_甲, 'w', encoding='utf-8').write('# 封版席\n本章无冷轮可补执。\n')
    io.open(_乙, 'w', encoding='utf-8').write('# 作业单\n**本章之失**：一处——某某。\n')
    _两 = [_甲, _乙]

    # ① ⛔旧式：头一份无那一行者，当场判「未记」（本改所治之伤）
    chk('①旧式·头一份无其行者即判「未记」（⛔而那一行就在第二份上）', _旧式(_两), '未记')
    chk('①之b 新式找得着', _新式(_两).startswith('一处'), True)
    # ② 只一份而有其行者，新旧二式皆找得着（⛔证本改非把旧式整个推翻）
    chk('②只一份而有其行者·旧式亦找得着', _旧式([_乙]).startswith('一处'), True)
    chk('②之b 新式同', _新式([_乙]).startswith('一处'), True)
    # ③ ⛔真未记者，新式照旧答「未记」（⛔不许为了不报红而乱认一行）
    chk('③⛔真未记者新式照旧答「未记」', _新式([_甲]), '未记')
    chk('③之b 一份也没有者亦然', _新式([]), '未记')
    # ④ ⛔乱序回灌：两份之序颠倒，新式之答不变（⛔其答不许再由 `glob` 之序决定）
    chk('④乱序回灌·序颠倒而新式之答不变', _新式(_两) == _新式(list(reversed(_两))), True)
    chk('④之b ⛔而旧式之答随其序而变（此即其病之形）',
        _旧式(_两) != _旧式(list(reversed(_两))), True)
    # ⑤ ★真盘回灌：351／352 二章之实（其行逐字在作业单上）
    _R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for _c in (351, 352):
        _fs = glob.glob(os.path.join(_R, '设定', '回执_*第%d章*' % _c))
        if len(_fs) >= 2:
            chk('⑤真盘回灌·第%d章新式找得着其行' % _c, _新式(_fs) != '未记', True)
    # ⑥ ⛔且器里那一格缩排确已改（⛔免测改了而器没改）
    _src = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '书级体检.py'),
                   encoding='utf-8').read()
    chk('⑥⛔器里 `break` 已在 `if m` 之内',
        "                rec = m.group(1).strip().strip('*').strip()\n                break" in _src,
        True)
finally:
    shutil.rmtree(_T, ignore_errors=True)

坏 = [x for x in 案 if not x[1]]
print('════ 负测·甲层之读 ════（守：一章两三份回执之时，「本章之失」找不找得着）')
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
