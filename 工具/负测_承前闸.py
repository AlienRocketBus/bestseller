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
　　**故不但要并回来，还要把这一笔记在这里**。

〔1119 死规之审·gates20〕⑮ 入 `_软报`：上列侦之格一字不动（「红」即侦得）；另添 ⑰：
　⑮ 於真盘仍红之章侦得而 `run()` ⛔计入拦（rc 0）｜⛔守牙：硬检（⑬）一红照旧拦（rc 2），--静 败单⛔混进 ⑮。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
    # ★1016·X01：分群之线与 ⑮ 同尺（K._线／K._同线：总纲有行者照总纲，无者照 _line_of 三值）
    l0, l1 = K._线(c - 1), K._线(c)
    if (None, None) in (l0, l1):
        continue
    (同 if K._同线(l0, l1) else 换).append(c)
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

# ── 丁·线之三值（2026-09-05·机制总审）：霍钧章268、黎东来章277（通篇「他」）不许当作沈鸢之同线前章 ──
chk('④之a 268／277 判为「他」，270／279 判为「她」', (K._line_of(268), K._line_of(277), K._line_of(270), K._line_of(279)), ('他', '他', '她', '她'))
chk('④之b 270 之同线前章不是 268；279 之不是 277', (K._prev_same_line(270) != 268, K._prev_same_line(279) != 277), (True, True))
# ★旧式回灌：旧式二值下 270 之前章即 268（他/她皆「我」<3/千）——故此格非陪跑
def _旧线(c):
    bb = K.body(c); w = len(re.sub(r'\s', '', bb)) or 1
    return '暗' if bb.count('我') / w * 1000 < 3 else '主'
chk('④之c 旧式二值把 268 与 270 判作同线（证此改非陪跑）', _旧线(268) == _旧线(270), True)

# ── 丙·换线相接之章，新式所比者须是同线那一章，不是前一章 ──
错 = []
for c in 换:
    p = K._prev_same_line(c)
    if p is None:
        continue
    if p == c - 1 or not K._同线(K._线(p), K._线(c)):
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

# ── 己·线照总纲两栏认（1016·X01·391 之⑮报「本线之前无章」而 389 係同线前章）──
# ★造局（临时总纲＋假细线，⛔不钉盘上之数）：总纲左右两栏混排；细线（我/她/他之密度）故意判错——
#   3 纲暗而细判「主」（如 389 对白多「我」）；5、7 纲暗而细判「他」（如 391、393 霍钧镜）；1 无纲行、细判「她」（旧章）。
import tempfile as _tf, shutil as _sh
_tmp = _tf.mkdtemp()
try:
    _o.makedirs(_o.path.join(_tmp, '设定'))
    open(_o.path.join(_tmp, '设定', '02_余章之势_总纲.md'), 'w', encoding='utf-8').write(
        '| 章 | 线 | 事 |\n|---|---|---|\n'
        '| 2 | 主·1 | 甲 | | 4 | 主·2 | 丙 |\n'
        '| 3 | 暗·1 | 乙 | | 5 | 暗·2 | 丁 |\n'
        '| 9 | 主·9 | 庚 | | 6 | 主·3 | 戊 |\n'
        '| 10 | 暗·9 | 辛 | | 7 | 暗·3 | 己 |\n')
    _细 = {1: '她', 2: '主', 3: '主', 4: '主', 5: '他', 6: '主', 7: '他'}.get
    _有 = set(range(1, 8))
    _得 = tuple(K._prev_same_line(c, root=_tmp, 有=_有, 细=_细) for c in (3, 4, 5, 6, 7))
    chk('⑦之b 总纲两栏：3→1（一有纲一无纲以粗值比）4→2 5→3（右栏）6→4 7→5', _得, (1, 2, 3, 4, 5))
    # ★非陪跑之凭：旧式（只认细线）下 5 无同线前章（3 被判「主」·即 391 之「免测」），3 误比主线之 2（即 390 误比 389）
    _旧 = lambda cur: next((c for c in range(cur - 1, max(0, cur - 13), -1)
                            if c in _有 and _细(c) == _细(cur)), None)
    chk('⑦之c 旧式（只认细线）於 5 报无前章、3 误比主线之 2（证此格非陪跑）', (_旧(5), _旧(3)), (None, 2))
finally:
    _sh.rmtree(_tmp, ignore_errors=True)


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

# ⑤而其群须够大，且新旧两式之分须真分得开
# ★★★★★2026-09-10 改（312 收尾席·令§六③：改闸必同日立负测，且以旧局回灌验）·
#   **此条今日报红，而它守的那一样一分也没有坏**——**其历与其数逐条写实，一条也不含混**：
#   ★**其旧式**：`chk2('⑮旧式之红率仍在四成上下（立闸之日所量：40/95＝42%）', 35 <= 红*100//测 <= 50, True)`
#     ——**它把一条断言钉在 2026-09-03 那一天磁盘上的一个比值上。**
#   ★★**今日之实（本席当场跑，非凭记忆）**：**旧式 38/109＝34%**（**低於其下限 35 一点**）；
#     **而 200—295 那一段单独算为 35/92＝38%**（**立闸之日同一段记的是 40/95＝42%**）。
#   ★★★**其何以今日方红，三条，逐条可查**：
#     ①**2026-09-05 `d8bbfc07`「线之尺三值（主／她／他）」改了 `_prev_same_line`**——
#       **霍钧章268／黎东来章277 不再算作沈鸢之同线前章**；**故其分母由 95 落到 92，且若干章之所比者换了一章。**
#     ②**2026-09-06 `28385c5c` 与 2026-09-08 `71c3781a` 两回回修**，**改了 240—287 之内二十余章之末几行**——
#       **而旧式所读者正是前章末五行之词**；**故那些章之判随之动。**
#     ③⛔**而最要紧的是第三条，且它是好事不是坏事**：**新章 296—312 十七章之内，旧式只报红 3 章（18%）**
#       ——**近十七章「承前」这一样，是真的写好了**；**於是全群之率被它拖到 34%，掉出那个带。**
#   ★★★★**即：这条断言的红，不是闸坏了，是书变好了**；**一条「书一变好就红」的断言，守的不是不变量，是那一天的磁盘**
#     （**其判语照录本族 `负测_销立门.py` ④之d 之判：一条要靠改断言才活得下去的断言，它守的不是那个不变量，是那一天的磁盘**）。
#   ★★★★★**故照其本意重述，不钉比值**：**⑮本是为「⑤⑥那一比不是在量噪音」作底的**——
#     **其所守者只两样**：①**其群够大**（**样本不足则⑤⑥之比无意义**）；
#     ②**新旧两式之分真分得开**（**新式之红须显著少於旧式，否则那一次放宽等於没做**）。
#   ⛔**而其牙不许因此变钝**：**下之⑮之c 以两组回灌当场验之**——
#     **旧局之数（40/95＝42%，且新式少於旧式）须照旧过；而一组「新旧同判」之退化数须当场红。**
_旧红 = set(c for c in sorted(k.F) if c >= 200 and _旧判(c) is False)
_测群 = set(c for c in sorted(k.F) if c >= 200 and _旧判(c) is not None)
_新红 = set(c for c in _测群 if _新判(c) is False)


def _十五之判(旧红, 新红, 测):
    """★⑮之判，抽成一函，为的是能拿旧局与退化局回灌它（否则它验不出自己是不是陪跑）。
    ★★其三条，一个比值也没有——**比值会随书之好坏走，而这三样不会**：
      ①**其群够大**（≥90章）：**样本不足则⑤⑥那一比是在量噪音。**
      ②**新式只放宽，不收紧**：**凡新式判红者，旧式须亦判红**（**新红 ⊆ 旧红**）——
        ★**这是「⑮改比同线前章」那一改之本义**：**它是把窗放宽，不是换一把尺**；
        **若有一章新式红而旧式绿，那就不是放宽，是它悄悄咬上了旧式咬不着的东西**，**须当场重审。**
      ③**而那一次放宽真的做了事**：**旧红转新绿者须 ≥1**（**否则那一改等於没做**）。
    ★★★**其今日之实（本席当场跑）**：**测109章｜旧红38｜新红22｜新红⊆旧红（违者0章）｜旧红转新绿16章**。"""
    if 测 < 90:
        return False
    if not 旧红:
        return False
    if not 新红 <= 旧红:
        return False
    return len(旧红 - 新红) >= 1


chk2('⑮之a 其群够大（≥90章·样本不足则⑤⑥之比无意义）　今测%d章' % len(_测群),
     len(_测群) >= 90, True)
chk2('⑮之b 新式只放宽不收紧（新红⊆旧红）　今违者%s' % (sorted(_新红 - _旧红) or '零'),
     sorted(_新红 - _旧红), [])
chk2('⑮之c 而那一次放宽真的做了事（旧红转新绿≥1）　今%d章' % len(_旧红 - _新红),
     _十五之判(_旧红, _新红, len(_测群)), True)
# ⑮之d【回灌·非陪跑之凭】★立闸之日那一局须照旧过；★★而四组退化之局须逐组当场红。
chk2('⑮之d 回灌·旧局（立闸之日所量 旧红40／新红22／测95）照旧判过',
     _十五之判(set(range(40)), set(range(22)), 95), True)
chk2('⑮之d2 回灌·退化局（新旧同判：那一次放宽等於没做）当场判红',
     _十五之判(set(range(38)), set(range(38)), 109), False)
chk2('⑮之d3 回灌·退化局（新式咬上了旧式咬不着的一章：非放宽，是换尺）当场判红',
     _十五之判(set(range(38)), set(range(20)) | {999}, 109), False)
chk2('⑮之d4 回灌·退化局（群不足90章）当场判红',
     _十五之判(set(range(30)), set(range(5)), 40), False)
chk2('⑮之d5 回灌·退化局（旧式一章不红，则那一次放宽本无可放）当场判红',
     _十五之判(set(), set(), 109), False)

# ⑯【X19·W53·1020】新尺（X01·线照总纲）之下，旧判失据之二章须照新尺补点名：
#   389（旧尺误作主线、所比 388）→同线前章 387；391（旧尺报「本线之前无章，免测」）→同线前章 389。
#   今二章之轮记已逐样点新尺之名 → ⑮须绿；回灌旧病（抽去新尺所点之名＝补判前之轮记）→ 须复红。
#   ⛔不写盘上之轮记（389、391 之轮记他席或正在改）：以临时 ROOT 只换 ⑮所读之轮记一档，正文与总纲仍读盘上。
_根 = K.ROOT
for _c, _p in ((389, 387), (391, 389)):
    chk2('⑯X19 第%d章之同线前章照新尺为第%d章' % (_c, _p), K._prev_same_line(_c), _p)
    chk2('⑯X19 第%d章轮记已补点新尺之名·⑮绿' % _c, _新判(_c), True)
    _lj3 = os.path.join(_根, '版本', '第%d章' % _c, '_轮记.md')
    _o3 = io.open(_lj3, encoding='utf-8').read()
    _半3 = _o3
    for _w in _key(_p):
        _半3 = _半3.replace(_w, '〓')
    _tmp3 = _tf.mkdtemp()
    try:
        _os.makedirs(os.path.join(_tmp3, '版本', '第%d章' % _c))
        io.open(os.path.join(_tmp3, '版本', '第%d章' % _c, '_轮记.md'), 'w', encoding='utf-8').write(_半3)
        K.ROOT = _tmp3
        chk2('⑯X19 第%d章回灌旧病（抽去新尺所点之名）须复红' % _c, _新判(_c), False)
    finally:
        K.ROOT = _根
        _sh.rmtree(_tmp3, ignore_errors=True)
    chk2('⑯X19 第%d章还原毕·⑮复绿、盘上轮记未动' % _c,
         (_新判(_c), io.open(_lj3, encoding='utf-8').read() == _o3), (True, True))


# ⑰〔1119 死规之审·gates20〕⑮ 只报：取真盘仍红之一章（⑭之b 之群），真跑 check15，余检换桩，看 run() 拦不拦
import contextlib as _cl
def _跑闸(真检, cur, 硬红=False):
    """余检一律换作恒绿之桩，只留「真检」照跑；硬红=True 另令 ⑬ 红（守牙）。返 (rc, --静 之印)。"""
    诸 = ('check3', 'check5', 'check7', 'check10', 'check11', 'check12', 'check13',
          'check15', 'check16', 'check17', 'check18', 'check19', 'check20')
    旧 = dict((kk, getattr(K, kk)) for kk in 诸)
    try:
        for kk in 诸:
            if kk != 真检:
                setattr(K, kk, lambda *a, _k=kk: [('桩·' + _k, True, '桩')])
        if 硬红:
            K.check13 = lambda *a: [('⑬·亮点段', False, '⛔桩：无亮点段')]
        _buf = io.StringIO()
        with _cl.redirect_stdout(_buf):
            rc = K.run([cur], True)
        return rc, _buf.getvalue()
    finally:
        for kk, v in 旧.items():
            setattr(K, kk, v)
if 仍红:
    _c17 = 仍红[0]
    _rc17, _印17 = _跑闸('check15', _c17)
    chk2('⑰第%d章 ⑮侦得（ok=False）而 run() ⛔计入拦：rc 0、印「通过」' % _c17,
         (K.check15(_c17)[0][1], _rc17, '开轮十六检通过' in _印17), (False, 0, True))
    _rc17b, _印17b = _跑闸('check15', _c17, 硬红=True)
    chk2('⑰之b ⛔守牙：同章而硬检（⑬）一红 → rc 2，--静 败单只列 ⑬、⛔混进 ⑮',
         (_rc17b, '⑬' in _印17b, '⑮' in _印17b), (2, True, False))
else:
    chk2('⑰真盘有仍红之章可取', False, True)

坏 = [x for x in 案 if not x[1]]

for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
