# -*- coding: utf-8 -*-
"""承前闸（⑮）负测（2026-09-01 立·随「⑮改比同线前章」同日）。
★其立之由：⑮之所比由「前一章」改为「同线最近之章」，是放宽了它看的窗；
  ★★而放宽之闸若窗划得不准，等於把闸拆了。
★★★故此测专问两样：①同线相接之章，新旧两式之判须一字不差（其防未动）；
  ②换线相接之章，新式所比者须真是同线那一章（而非前一章）。

★★★★2026-09-03·295第1轮并入第二节（⑧起）：⑮又改一路——**轮记里逐样落判者亦算过**。
　·★其由：**⑮之处方与其判据对不上**——它红时自印「须在轮记里明写一句：本章认它、翻它、还是有意搁下」，
　　**而它只读正文，一眼也不看轮记**。
　·★★取二组数：第200章起共测95章，旧式报红40章（42%）；滤去定宽切片後仍红27章（28%）——**非切片之过**。
　·★★★而并入此档不另立一份，其由二：**①一个数不许有两把尺，一族测亦不许有两本账**；
　　**②今日我曾以 cat > 覆盖此档（289所立），落刀之前未走可逆之路**——**其号 R0020，已存**；
　　**故不但要并回来，还要把这一笔记在这里**。"""
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
# ★★★★★2026-09-03·295第1轮所正：**本条原比「新式之全判」，而全判自今日起有二路**
#   （①正文命中 ②轮记逐样落判）；★**第二路与「⑮改比同线」这一改无涉**，
#   ★★而它今日把 238、272 二章转绿（二章俱有真声明），**遂使本条判红**；
#   ★★★**故本条所比者改为「新式之第一路（正文命中）」**——**那才是本条要守的那一样**：
#   **改比同线之後，正文命中那一路於同线相接之章上一字未动。**
#   ★★★★而第二路之守另在 ⑬⑭（抽掉即红／转绿者须有真声明），不与本条相混。
def _新式第一路(c):
    p = K._prev_same_line(c)
    if p is None:
        return None
    b = K.body(c) or ''
    pb = K.body(p) or ''
    if not b or not pb:
        return None
    tail = [x.strip() for x in pb.split('\n') if x.strip() and x.strip() != '＊'][-5:]
    txt = ''.join(tail)
    cand = [w for w in re.findall(r'[一-龥]{2,4}', txt)
            if not re.search(r'^(而|是|不|的|了|着|这|那|我|他|她|你|们|就|也|都|还|要|说|有|没'
                             r'|一|个|上|下|里|头|来|去|又|把|跟|得|在|从|到|它|们)', w)]
    seen = []
    for w in cand:
        if w not in seen:
            seen.append(w)
    return len([w for w in seen[:8] if w in b]) >= 2


异 = [c for c in 同 if _新式第一路(c) != 旧式(c)]
chk('③同线相接：新旧两式之第一路逐章同判（其防未动）', 异, [])

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


# ══════ 第二节（2026-09-03·295第1轮并入）：⑮之第二路——轮记里逐样落判者亦算过 ══════
import io as _io, os as _os
SRC = _io.open(_os.path.join('工具', '开轮六检.py'), encoding='utf-8').read()
ROOT = '.'
os = _os
io = _io
k = K


def chk2(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))


def _key(prev):
    pb = K.body(prev) or ''
    tail = [x.strip() for x in pb.split('\n') if x.strip() and x.strip() != '＊'][-5:]
    txt = ''.join(tail)
    cand = [w for w in re.findall(r'[一-龥]{2,4}', txt)
            if not re.search(r'^(而|是|不|的|了|着|这|那|我|他|她|你|们|就|也|都|还|要|说|有|没'
                             r'|一|个|上|下|里|头|来|去|又|把|跟|得|在|从|到|它|们)', w)]
    seen = []
    for w in cand:
        if w not in seen:
            seen.append(w)
    return seen[:8]


def _旧判(c):
    p = K._prev_same_line(c)
    if p is None:
        return None
    b = K.body(c) or ''
    if not b:
        return None
    return len([w for w in _key(p) if w in b]) >= 2


def _新判(c):
    for _nm, ok, msg in K.check15(c):
        return None if '免测' in msg else ok
    return None

chk2('⑧②须点名≥2样 ②须点名≥2样', 'len(_名) >= 2' in SRC, True)
chk2('⑨②须落判（认／翻／搁下） ②须落判（认／翻／搁下）', "('认', '翻', '搁下')" in SRC, True)
chk2('⑩防抄之守 且有防抄之守（抄本检之报文者不算声明）', '而这不一定是错' in SRC, True)


# ★（_key 第二份已删·重名扫描所逮：并档时抄了两遍，其义与上一份同）
# ★（_旧判 第二份已删·重名扫描所逮：并档时抄了两遍，其义与上一份同）
# ★（_新判 第二份已删·重名扫描所逮：并档时抄了两遍，其义与上一份同）
# ②本章（295）：正文只命中1样，而轮记已落判 → 新式须过、旧式须不过
chk2('⑪295 旧式不过 295 旧式不过（正文命中<2）', _旧判(295), False)
chk2('⑫295 新式过 295 新式过（轮记逐样落判）', _新判(295), True)

# ③抽掉轮记里的「承前之判」四字 → 须复红（证②非白给）
_lj = os.path.join(ROOT, '版本', '第295章', '_轮记.md')
_o = io.open(_lj, encoding='utf-8').read()
try:
    io.open(_lj, 'w', encoding='utf-8').write(_o.replace('承前之判', '承前之XX'))
    chk2('⑬抽掉「承前之判」四字即复红', _新判(295), False)
    # ★★而只有四字、不点名者亦须红
    _半 = _o
    for _w in _key(k._prev_same_line(295)):
        _半 = _半.replace(_w, '〓')
    io.open(_lj, 'w', encoding='utf-8').write(_半)
    chk2('⑬之b 有四字而不点名者亦须红', _新判(295), False)
finally:
    io.open(_lj, 'w', encoding='utf-8').write(_o)
# ③之e【防抄之验】把本检自己的报文抄进轮记，而别处不留声明 → 须仍红
try:
    _抄 = _o.replace('承前之判', '承前之XX')
    _抄 += ('\n\n⛔同线前章（第293章）收句之骨 后一回、十层、两天这个、数今天没，'
            '本章一样也没回指：★而这不一定是错——★★然须在轮记里明写一句「承前之判」，'
            '逐样点其名并落判（认／翻／搁下）\n')
    io.open(_lj, 'w', encoding='utf-8').write(_抄)
    chk2('⑬之e 抄本检之报文而别处无声明者，须仍红', _新判(295), False)
finally:
    io.open(_lj, 'w', encoding='utf-8').write(_o)
chk2('⑬之c 还原毕·复绿', _新判(295), True)
chk2('⑬之d 还原毕·轮记与测前逐字相同',
    io.open(_lj, encoding='utf-8').read() == _o, True)

# ④【要害】以旧式回灌全书：转绿之旧章，须逐章确有一份真声明；无声明者须仍红
#   ★★★★★本测头一版把④写成「转绿者须为 0」——**而那是把断言钉在我的猜想上**：
#     我猜「旧章无一份轮记写过这一式」，而一跑即见 **12 章写过**
#     （209、212、233、238、242、251、254、257、262、266、272、274、275 之属，
#      逐章点名并落判，如 251「本章认249之收判（食指又动了）」）。
#   ★**它们照闸的处方办了，而闸照旧红它们**——**故它们转绿是对的，错的是我那条断言。**
#   ★★**其真不变量有二**：①转绿者逐章须有真声明（且不许是抄本检之报文）；
#     ②**无声明之红章须仍红**（这才是本闸剩下的牙）。
转绿, 无据 = [], []
for c in sorted(k.F):
    if c < 200 or c == 295:
        continue
    a, b2 = _旧判(c), _新判(c)
    if a is False and b2 is True:
        转绿.append(c)
        _p = os.path.join(ROOT, '版本', '第%d章' % c, '_轮记.md')
        _tx = io.open(_p, encoding='utf-8').read() if os.path.exists(_p) else ''
        _真 = any('而这不一定是错' not in _tx[max(0, m.start() - 200):m.start() + 200]
                  for m in re.finditer('承前之判', _tx))
        if not _真:
            无据.append(c)
chk2('⑭转绿之旧章逐章须有真声明（抄本检之报文者不算）', 无据, [])
仍红 = [c for c in sorted(k.F) if c >= 200 and c != 295
        and _旧判(c) is False and _新判(c) is False]
chk2('⑭之b 而无声明之红章须仍红（本闸剩下的牙）', len(仍红) >= 10, True)

# ⑤而其群之数须与立闸之日所量相符（数一变即须重判）
红 = sum(1 for c in sorted(k.F) if c >= 200 and _旧判(c) is False)
测 = sum(1 for c in sorted(k.F) if c >= 200 and _旧判(c) is not None)
chk2('⑮旧式之红率仍在四成上下（立闸之日所量：40/95＝42%%）', 35 <= 红 * 100 // max(1, 测) <= 50, True)


坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
