# -*- coding: utf-8 -*-
"""负测·承前闸⑮（2026-09-03·295第1轮立）

★所治之伤：`开轮六检::⑮·承前之判` **其处方与其判据对不上**。
　·★它红时自印：「**★★然须在轮记里明写一句：本章认它、翻它、还是有意搁下**」；
　·★★**而它只读正文，一眼也不看轮记**——**照它的处方办了，它照旧红。**
★★取二组数（令§六①）：**第200章起共测95章，旧式报红40章（42%）**；
　**滤去「只此一处之定宽切片」（全书出现<3回者）之後仍红27章（28%）**——**故非切片之过。**
★★★其治：**加一路②**——**轮记里逐样落判者亦算过**，而②须同时具三样：
　「承前之判」四字｜前章收句之骨中≥2样之名｜认／翻／搁下之一。
★★★★**而本测之要害在④**：**以旧式回灌全书，因新路②而转绿之旧章须为 0**——
　**若旧章成片转绿，那就不是补一路，是挖空**（令§六④）。
"""
import importlib.util as iu, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))


def _六检():
    sp = iu.spec_from_file_location('_k', os.path.join(ROOT, '工具', '开轮六检.py'))
    m = iu.module_from_spec(sp); sp.loader.exec_module(m)
    return m


k = _六检()
SRC = io.open(os.path.join(ROOT, '工具', '开轮六检.py'), encoding='utf-8').read()

# ①二路俱在，且②之三样一样不少
# ★★★★★本测头一版之①与①之d 写死了源码里的一个字符串（"'承前之判' in _t"）——
#   **而我同日就把那一行改成了防抄之循环，二条当场判红**；**这是第二十八犯之形，钉的是码的字面。**
#   ★故删此二条，改以「其行」验之：其守之在，由①之b／①之c／①之d 三条看码上之名；
#   ★★而②之三样之真凭在 ③（抽掉即红）、③之b（不点名即红）、③之e（抄报文即红）、③之c（还原即绿）。
chk('①之b ②须点名≥2样', 'len(_名) >= 2' in SRC, True)
chk('①之c ②须落判（认／翻／搁下）', "('认', '翻', '搁下')" in SRC, True)
chk('①之d 且有防抄之守（抄本检之报文者不算声明）', '而这不一定是错' in SRC, True)


def _key(prev):
    pb = k.body(prev) or ''
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
    """★旧式：只读正文，命中≥2即过。"""
    p = k._prev_same_line(c)
    if p is None:
        return None
    b = k.body(c) or ''
    if not b:
        return None
    return len([w for w in _key(p) if w in b]) >= 2


def _新判(c):
    r = k.check15(c)
    for _nm, ok, msg in r:
        if '免测' in msg:
            return None
        return ok
    return None


# ②本章（295）：正文只命中1样，而轮记已落判 → 新式须过、旧式须不过
chk('②之a 295 旧式不过（正文命中<2）', _旧判(295), False)
chk('②之b 295 新式过（轮记逐样落判）', _新判(295), True)

# ③抽掉轮记里的「承前之判」四字 → 须复红（证②非白给）
_lj = os.path.join(ROOT, '版本', '第295章', '_轮记.md')
_o = io.open(_lj, encoding='utf-8').read()
try:
    io.open(_lj, 'w', encoding='utf-8').write(_o.replace('承前之判', '承前之XX'))
    chk('③抽掉「承前之判」四字即复红', _新判(295), False)
    # ★★而只有四字、不点名者亦须红
    _半 = _o
    for _w in _key(k._prev_same_line(295)):
        _半 = _半.replace(_w, '〓')
    io.open(_lj, 'w', encoding='utf-8').write(_半)
    chk('③之b 有四字而不点名者亦须红', _新判(295), False)
finally:
    io.open(_lj, 'w', encoding='utf-8').write(_o)
# ③之e【防抄之验】把本检自己的报文抄进轮记，而别处不留声明 → 须仍红
try:
    _抄 = _o.replace('承前之判', '承前之XX')
    _抄 += ('\n\n⛔同线前章（第293章）收句之骨 后一回、十层、两天这个、数今天没，'
            '本章一样也没回指：★而这不一定是错——★★然须在轮记里明写一句「承前之判」，'
            '逐样点其名并落判（认／翻／搁下）\n')
    io.open(_lj, 'w', encoding='utf-8').write(_抄)
    chk('③之e 抄本检之报文而别处无声明者，须仍红', _新判(295), False)
finally:
    io.open(_lj, 'w', encoding='utf-8').write(_o)
chk('③之c 还原毕·复绿', _新判(295), True)
chk('③之d 还原毕·轮记与测前逐字相同',
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
chk('④转绿之旧章逐章须有真声明（抄本检之报文者不算）', 无据, [])
仍红 = [c for c in sorted(k.F) if c >= 200 and c != 295
        and _旧判(c) is False and _新判(c) is False]
chk('④之b 而无声明之红章须仍红（本闸剩下的牙）', len(仍红) >= 10, True)

# ⑤而其群之数须与立闸之日所量相符（数一变即须重判）
红 = sum(1 for c in sorted(k.F) if c >= 200 and _旧判(c) is False)
测 = sum(1 for c in sorted(k.F) if c >= 200 and _旧判(c) is not None)
chk('⑤旧式之红率仍在四成上下（立闸之日所量：40/95＝42%%）', 35 <= 红 * 100 // max(1, 测) <= 50, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测·承前闸 %d/%d %s（旧式红 %d/%d 章；因新路转绿之旧章 %d）'
      % (len(案) - len(坏), len(案), '全通' if not 坏 else '⛔未过', 红, 测, len(转绿)))
sys.exit(1 if 坏 else 0)
