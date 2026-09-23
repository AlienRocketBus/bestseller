# -*- coding: utf-8 -*-
"""负测·对位之三路（2026-09-23·限362 立）

⛔**其所治者**：**`对位.py` 是数「谁没有负测」的那一把尺，而它自己没有负测。**
★**一把量别人有没有防线的尺，自己没有防线**——**这是本坐今日所荐三项之第三项**
  （`册_0923_赤手无负测之拆数.md` §五）。

★★**本测所问只三句**（照其自书之三路）：
  ①**孤器**：一件器无一条路够得着，它认不认得出；
  ②**负测覆盖**：一格之码里指得出 `负测_*.py` 者算「有撑」，指不出者算「赤手」；
  ③**其数与其单相符**：它印的那个数，与它自己列出来的那一单，须一样长。
⛔**本测不判那三路该不该**（那是令§一⑤之事），**只判「它数得对不对」。**

跑：python3 工具/负测_对位之三路.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as iu, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
过 = 败 = 0


def chk(名, 实):
    global 过, 败
    if 实:
        过 += 1
    else:
        败 += 1
        print('  ⛔不过：%s' % 名)


sp = iu.spec_from_file_location('_dw', os.path.join(ROOT, '工具', '对位.py'))
_dw = iu.module_from_spec(sp)
sp.loader.exec_module(_dw)

# ── 一·负测覆盖之判（⛔纯函数，不碰盘）────────────────────
funcs, withneg, bare = _dw.负测覆盖()
chk('①其三堆相加须等於总数（⛔一项不许漏、不许重）',
    len(withneg) + len(bare) == len(funcs))
chk('②「有撑」者之码里逐格皆真指得出一份 `负测_*.py`',
    all(re.search(r'负测_\w+\.py', funcs[n]) for n in withneg))
chk('⛔③而「赤手」者之码里逐格皆真指不出——故②非陪跑',
    all(not re.search(r'负测_\w+\.py', funcs[n]) for n in bare))
chk('④其单无重（⛔同一格不许既算有撑又算赤手）',
    not (set(withneg) & set(bare)))

# ── 二·孤器之判（⛔沙盘之表，不取盘上之实）────────────────
#   `_reach(name, tools)`：自诸器之码里找「谁调它」，回其所及之集。
_诸 = _dw._tools()
chk('⑤其器单非空（⛔取不着即本测无料）', len(_诸) > 50)
_有主 = [f for f in _诸 if f not in _dw.入口 and _dw._reach(f, _诸)]
chk('⑥凡被别器点过名者，`_reach` 须回得出至少一条路', len(_有主) > 20)
chk('⛔⑦而一个盘上根本没有的器名，`_reach` 须回空——故⑥非陪跑',
    not _dw._reach('这一样器盘上没有.py', _诸))

# ── 三·其数与其单相符（⛔本测之要害：它印的数不许与它自己的单不一样）──
import io as _io, contextlib as _ct
_buf = _io.StringIO()
with _ct.redirect_stdout(_buf):
    try:
        _dw.main()
    except SystemExit:
        pass
_out = _buf.getvalue()
_m = re.search(r'全测检项 (\d+)｜有负测撑者 (\d+)｜\*\*赤手无负测者 (\d+)', _out)
chk('⑧其印之三数取得出来', _m is not None)
if _m:
    chk('⑨其印之「检项」与纯函数所数相符（%s / %d）' % (_m.group(1), len(funcs)),
        int(_m.group(1)) == len(funcs))
    chk('⑩其印之「有撑」与纯函数所数相符（%s / %d）' % (_m.group(2), len(withneg)),
        int(_m.group(2)) == len(withneg))
    chk('⑪其印之「赤手」与纯函数所数相符（%s / %d）' % (_m.group(3), len(bare)),
        int(_m.group(3)) == len(bare))
    _列 = re.findall(r'chk_\w+|chk_[一-龥]+', _out.split('一律记「未验」')[-1])
    chk('⛔⑫而它印出来的那一单，长短须与它印的那个数一样（单 %d／数 %s）'
        % (len(set(_列)), _m.group(3)),
        len(set(_列)) == int(_m.group(3)))

# ── 四·本测之限，写死在码里 ──────────────────────────
#   **本测只判「它数得对不对」**，⛔**不判「那三路该不该」**——
#   **一格有没有负测，它数得出；那一份负测硬不硬，它数不出**（丙堆三十八项之限，
#   其详在 `设定/册_0923_赤手无负测之拆数.md` §二）。
chk('⑬本测之限已写死在本测码内（⛔它数得出有没有，数不出硬不硬）',
    '那一份负测硬不硬，它数不出' in open(__file__, encoding='utf-8').read())

print('  负测·对位之三路：%d/%d' % (过, 过 + 败))
sys.exit(1 if 败 else 0)
