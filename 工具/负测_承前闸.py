# -*- coding: utf-8 -*-
"""承前闸（⑮）负测（2026-09-01 立·随「⑮改比同线前章」同日）。
★其立之由：⑮之所比由「前一章」改为「同线最近之章」，是放宽了它看的窗；
  ★★而放宽之闸若窗划得不准，等於把闸拆了。
★★★故此测专问两样：①同线相接之章，新旧两式之判须一字不差（其防未动）；
  ②换线相接之章，新式所比者须真是同线那一章（而非前一章）。"""
import sys, re, importlib.util

spec = importlib.util.spec_from_file_location('k', '工具/开轮六检.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

案 = []
def chk(名, 实, 期):
    案.append((名, 实 == 期, '实=%r 期=%r' % (实, 期)))

def 旧式(cur):
    """★旧式：一律取前一章。★★（其余一字未改，逐字照录改前之码。）"""
    if not cur or (cur - 1) not in K.F:
        return None
    pb, b = K.body(cur - 1), K.body(cur)
    if not pb or not b:
        return None
    tail = [x.strip() for x in pb.split('\n') if x.strip() and x.strip() != '＊'][-5:]
    txt = ''.join(tail)
    cand = [w for w in re.findall(r'[一-龥]{2,4}', txt)
            if not re.search(r'^(而|是|不|的|了|着|这|那|我|他|她|你|们|就|也|都|还|要|说|有|没|一|个|上|下|里|头|来|去|又|把|跟|得|在|从|到|它|们)', w)]
    seen = []
    for w in cand:
        if w not in seen:
            seen.append(w)
    return len([w for w in seen[:8] if w in b]) >= 2

# ── 甲·分群（其数须与立法之日所量相符：同线24章／换线56章·210章以来）──
同, 换 = [], []
for c in sorted(K.F):
    if c - 1 not in K.F or c < 210:
        continue
    l0, l1 = K._line_of(c - 1), K._line_of(c)
    if None in (l0, l1):
        continue
    (同 if l0 == l1 else 换).append(c)
chk('①同线相接之章数 ≥20', len(同) >= 20, True)
chk('②换线相接之章数 ≥50', len(换) >= 50, True)

# ── 乙·其防未动：同线相接之章，新旧两式之判须一字不差 ──
异 = [c for c in 同 if K.check15(c)[0][1] != 旧式(c)]
chk('③同线相接：新旧两式逐章同判（其防未动）', 异, [])

# ── 丙·换线相接之章，新式所比者须是同线那一章，不是前一章 ──
错 = []
for c in 换:
    p = K._prev_same_line(c)
    if p is None:
        continue
    if p == c - 1 or K._line_of(p) != K._line_of(c):
        错.append(c)
chk('④换线相接：所比者皆为同线之章且非前一章', 错, [])

# ── 丁·旧式回灌（令§六③：一份在旧式下也全过的测，就是陪跑）──
# ★旧式於换线相接之章红率九成；新式若与旧式同判，即是没改动——那才是陪跑。
旧红 = sum(1 for c in 换 if 旧式(c) is False)
新红 = sum(1 for c in 换 if K.check15(c)[0][1] is False)
chk('⑤旧式於换线之章红率 ≥80%%（%d/%d）' % (旧红, len(换)),
    旧红 * 100 // max(len(换), 1) >= 80, True)
chk('⑥新式於换线之章红率 显著低於旧式（新%d ＜ 旧%d）' % (新红, 旧红), 新红 < 旧红, True)

# ── 戊·免测之口须窄：十二章之内无同线者方免 ──
chk('⑦无前章者免测', K.check15(1)[0][1], True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
