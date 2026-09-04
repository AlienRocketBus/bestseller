# -*- coding: utf-8 -*-
"""负测·回修案档名 · 2026-09-04 立（301第12轮·极限轮自逮·令§六④同日立负测）

★其红在哪一行：本坐当日立「回修案_第288至299章_20260904_骨记残引.md」，
  而全测之回修案检以 `第(\\d+)章` 取其章号——**288之後是「至」，不是「章」，一处也匹配不着**；
  ★★而其果不是报错，是 `continue`：**这一件案从此不在册上，而末行照旧印「N件俱办毕」。**
  ★★★即令§一④之形：**闸绿，而那一件根本不在它的判据里。**

★★★★它认哪几样，本书同类共几样（令§六④）：
  **只认 `设定/回修案/回修案_第*章_*.md` 之档名读不读得出章号这一样**；
  **本书同类**：`设定/回修案/` 今存 8 件，**8 件之档名逐件读得出**（故今日之绿是真绿）；
  ★而其反面之群：**本坐当日一件即犯**——**一件足以证其形，因其害不在多，在无声。**

★旧式回灌之验（③）：**旧式（continue）对同一份档名吐绿，且总数照旧**——故本测非陪跑。
"""
import io, os, re, sys, tempfile, shutil

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(根, '设定', '回修案')

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))


def 新式(fs):
    """今日之判据：档名读不出章号者入 bad。"""
    bad = []
    for f in fs:
        if not re.search(r'第(\d+)章', os.path.basename(f)):
            bad.append(os.path.basename(f))
    return bad


def 旧式(fs):
    """旧判据：读不出即 continue（一句不说）。"""
    bad = []
    for f in fs:
        n = re.search(r'第(\d+)章', os.path.basename(f))
        if not n:
            continue
    return bad


真 = sorted(os.path.basename(x) for x in os.listdir(D)) if os.path.isdir(D) else []
坏名 = '回修案_第288至299章_20260904_骨记残引.md'

# ①今日之册须真绿（8件档名逐件读得出）
t('①今存之案逐件读得出章号', 新式(真), [])
# ②灌回那一份读不懂的档名，新式须报红
t('②读不出章号之档名，新式当场报出其名', 新式(真 + [坏名]), [坏名])
# ③旧式对同一入参吐绿——故此测非陪跑
t('③旧式（continue）对同一份档名一句不说，故非陪跑', 旧式(真 + [坏名]), [])
# ④不误伤：合式之档名不许被报
t('④合式之档名不报（回修案_第290章_20260902b.md）',
  新式(['回修案_第290章_20260902b.md']), [])
# ⑤而「第N至M章」这一式亦须报——其形正是本坐所犯
t('⑤「第N至M章」之式亦读不出章号', bool(新式([坏名])), True)
# ⑥全测之码里那一段须真在（不许本测过而器里没有）
_QC = io.open(os.path.join(根, '工具', '全测.py'), encoding='utf-8').read()
t('⑥全测之回修案检里已无赤裸之 continue（其位已写报红）',
  '档名里读不出章号' in _QC, True)

print('════ 负测·回修案档名 ════')
for 名, ok, 实, 期 in 过:
    print('  %s %s' % ('✓' if ok else '✗', 名), '' if ok else '（实 %r 期 %r）' % (实, 期))
n = sum(1 for _, ok, _, _ in 过 if ok)
print('  %d/%d %s' % (n, len(过), '全通' if n == len(过) else '⛔有败'))
sys.exit(0 if n == len(过) else 1)
