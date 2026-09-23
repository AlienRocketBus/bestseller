# -*- coding: utf-8 -*-
"""负测·钩路（2026-09-23·限361 立）——**守那道守着所有闸的闸**

⛔**其所以要立**：`对位.py` 今印「**赤手无负测者 67（38%）**」，`chk_hookspath` 在其列。
★**而这一项不是寻常一项**：**`core.hooksPath` 指不对，`pre-push` 就不跑**；
  **`pre-push` 不跑，全测不跑，於是本仓所有的闸一齐失效而无人知道**——
  **它是守着所有闸的那一道闸，⛔而它自己一条负测也没有。**

★★**并当面报本坐读它之所得（⛔一处真弱，不是挑刺）**：
  **`chk_hookspath` 在 `cur != want` 之时会 `git config` 自己挂回去，然後 `return True`**——
  ⛔**即：这一项永远红不了。** **它自愈，而自愈之後它说「已挂」。**
  ★**自愈本身是对的**（其注自书其由：「容器每次重建后 .git 皆新」）；
  ⛔**而「自愈过」与「本来就挂着」在报文里须分得开**——**否则一份全绿的报，说不出钩子在那一跑之前是不是空的。**
  ★★**本测不去改它**（⛔0923 本坐之界：一条令严到什么地步不改；而此处非「读错」，係「治法之择」）；
  **本测只把它做得到与做不到的事逐格钉死**，**并留一格在那儿，指着那一处分不开的地方。**

跑：python3 工具/负测_钩路.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as iu, os, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
过 = 败 = 0


def chk(名, 实):
    global 过, 败
    if 实:
        过 += 1
    else:
        败 += 1
        print('  ⛔不过：%s' % 名)


def _载(root):
    """★载一份 `全测.py`，把其 ROOT 指进沙盘（⛔本测一个字不写真盘）。"""
    sp = iu.spec_from_file_location('_qc', os.path.join(ROOT, '工具', '全测.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.ROOT = root
    return m


def _造沙(带钩=True, 可执行=True):
    d = tempfile.mkdtemp(prefix='负测_钩路_')
    subprocess.run(['git', 'init', '-q', d], capture_output=True)
    g = os.path.join(d, '工具', 'githooks')
    os.makedirs(g, exist_ok=True)
    if 带钩:
        p = os.path.join(g, 'pre-push')
        open(p, 'w').write('#!/bin/sh\nexit 0\n')
        os.chmod(p, 0o755 if 可执行 else 0o644)
    return d


def _读钩路(d):
    r = subprocess.run(['git', 'config', '--get', 'core.hooksPath'],
                       cwd=d, capture_output=True, text=True)
    return r.stdout.strip()


# ── ①②·钩不在＝红（⛔此係本项唯一红得起来的一路，须钉死）──────────
_d = _造沙(带钩=False)
_m = _载(_d)
_ok, _语 = _m.chk_hookspath()
chk('①⛔`工具/githooks/pre-push` 不在盘上者，本项须红', _ok is False)
chk('②其红辞须指得出缺的是哪一档（非只说「不过」）', 'pre-push' in (_语 or ''))
shutil.rmtree(_d)

# ── ③④⑤·钩在而 hooksPath 未设：自愈，且自愈须是真的 ────────────
_d = _造沙()
chk('③前置·沙盘之 hooksPath 本是空的', _读钩路(_d) == '')
_m = _载(_d)
_ok, _语 = _m.chk_hookspath()
chk('④钩在而路未设者，本项放行（其注自书其由：容器每次重建后 .git 皆新）', _ok is True)
chk('⛔⑤而其自愈须是真的——跑毕再问 git，须真读回 工具/githooks',
    _读钩路(_d) == '工具/githooks')
chk('⑥其语须说出「自动挂回」，不许只说「已挂」（否则一份全绿的报，'
    '说不出钩子在那一跑之前是不是空的）', '自动挂回' in (_语 or ''))
shutil.rmtree(_d)

# ── ⑦⑧·路指错了地方：亦须自愈到对的那一处 ─────────────────
_d = _造沙()
subprocess.run(['git', 'config', 'core.hooksPath', '别处/钩'], cwd=_d, capture_output=True)
_m = _载(_d)
_ok, _语 = _m.chk_hookspath()
chk('⑦路指着别处者亦放行（同④之由）', _ok is True)
chk('⛔⑧而跑毕须真指回 工具/githooks（⛔不许只在报文里说挂回了）',
    _读钩路(_d) == '工具/githooks')
shutil.rmtree(_d)

# ── ⑨⑩·钩在、路对，而钩没有执行位 ──────────────────────
_d = _造沙(可执行=False)
subprocess.run(['git', 'config', 'core.hooksPath', '工具/githooks'], cwd=_d, capture_output=True)
_m = _载(_d)
_ok, _语 = _m.chk_hookspath()
chk('⑨钩无执行位者放行（本项自补其位）', _ok is True)
chk('⛔⑩而跑毕那一档须真可执行——⛔一个不可执行的 pre-push 等於没有钩子',
    os.access(os.path.join(_d, '工具', 'githooks', 'pre-push'), os.X_OK))
shutil.rmtree(_d)

# ── ⑪·真盘之实（⛔报而不改，本测一个字不写真盘）────────────────
_真路 = _读钩路(ROOT)
chk('⑪真盘此刻之 core.hooksPath 正指 工具/githooks', _真路 == '工具/githooks')
chk('⑫真盘之 工具/githooks/pre-push 在且可执行',
    os.access(os.path.join(ROOT, '工具', 'githooks', 'pre-push'), os.X_OK))

# ── ⑬·⛔本项之限，写死在码里（留给後坐）──────────────────
#   **本项永不因「钩子先前是空的」而红**——它自愈而後报「已挂」。
#   ⛔**故一份全绿的全测，⛔不能拿来证明「这一跑之前钩子一直挂着」**；
#   ★**它只证得了「这一跑跑完之後钩子是挂着的」。**
#   ★★**本坐不改它**（自愈是对的治法，改它要动的是「治法之择」，非「读错」）；
#   **本格只把这一句钉在码里，⛔叫後坐读得见。**
chk('⑬本项之限已写死在本测码内（⛔全绿证不了「跑之前钩子一直挂着」）',
    '这一跑跑完之後钩子是挂着的' in open(__file__, encoding='utf-8').read())

print('  负测·钩路：%d/%d' % (过, 过 + 败))
sys.exit(1 if 败 else 0)
