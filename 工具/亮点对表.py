# -*- coding: utf-8 -*-
"""亮点对表 · 2026-09-01 立（289第9轮所逮·第10轮当场立器）
　★病：亮点段与正文相犯，而全书无一道闸看得见——
　　　数闸只认「N个字」那一式，硬闸只认十八格，开轮十六检之⑮⑳只看正文。
　　　289一章之内实测五处：前天／昨天三处、「二十来口气」（正文作二十三口气）、
　　　「一百天」（正文作「进山到今天」）；此外第10轮又逮出二处假引（把概括套进「」）。

　★★而立此器之前先数其群（令§六②），三路各得一数：
　　·**①引文路**（亮点段「」内之串回正文查，去他章原场、去带「不许／须／该」之预令）
　　　→ **红 57 章／289（20%）**；逐例看去，其大半是亮点段拿「」作着重号、或概括正文之意，
　　　　**非报错**。⛔ 故此路不作闸，只作报。
　　·**②数路**（亮点段带量词之数回正文查）→ **红 51 章／289（18%）**；
　　　其例如「贴两回」——正文写「贴了一下…又贴了一回」，亮点段数了一遍，**是概括不是相犯**。
　　　⛔ 故此路亦不作闸，只作报。
　　·**③约数路**（亮点段出「N来／N多／N几」而正文无此约数）→ **红 3 章／289（1%）**，
　　　★★★而其判准是硬的：**亮点段不许把正文给准了的数抹成约数**
　　　（289之「二十来口气」正是此形，而正文写的是「二十三口气」）。
　　　✓ 故只此一路作闸。

　用：python3 工具/亮点对表.py N   ｜  --全
　　　rc=0 无相犯（③路）｜rc=1 ③路有红｜rc=2 无此章
"""
import io, os, re, sys, glob

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
# ★「层」不入其列：本书之「层」多是骨之层（其骨五层／第五层），是工序之词不是物之数。
量词 = r'(口气|步|拃|指|掌|天|个字|块|下|回|行|页|寸|尺|碗|遍)'
约 = r'([一二三四五六七八九十百零两]+)([来多余几])' + 量词


def _号(s):
    m = re.search(r'第([零一二三四五六七八九十百]+)章', s)
    if not m:
        return None
    t = m.group(1)
    if t.startswith('十'):
        t = '一' + t
    n = c = 0
    for ch in t:
        if ch == '百':
            n += (c or 1) * 100; c = 0
        elif ch == '十':
            n += (c or 1) * 10; c = 0
        else:
            c = CN[ch]
    return n + c


def 诸章():
    d = {}
    for p in glob.glob(os.path.join(根, '正文', '*.md')):
        n = _号(os.path.basename(p))
        if n:
            d[n] = p
    return d


def 剥(s):
    # ★2026-09-01·289第13轮修：原式不剥标点，遂使「那一堆里头，凭什么有闲的」（正文有逗）
    #   与亮点段所引之无逗本读作相犯 ⛔——★★实测此一形独占十章，引文路由 57 章降为 47 章。
    #   ★★★记：一道比字的闸，头一件事是把不比的东西剥干净。
    return re.sub(r'[\s*★·【】，。、；：？！…—「」『』（）()／/]', '', s)


def 骨层数(txt):
    """★2026-09-02 立（290第6轮所逮）：亮点段自书「其骨N层」，而其下所列之层不足N。
    ★★其形是一次静默的 replace 未命中——**改亮点段之骨而只改了那个数**；
    ★★★而此形本坐已犯二回（289之开镜卡写死 %s／290之骨六层只列五条），依令§十一当机化。
    ★★★★其判极窄：只比「其骨N层」之N与其下 ①②③④⑤⑥⑦⑧⑨⑩ 之个数（含①之二、③之三一类之附层）。
    返回 (报之N, 实数M)；无「其骨N层」者返 (None, None)。"""
    if '【本章亮点】' not in txt:
        return None, None
    hl = txt.split('【本章亮点】', 1)[1]
    m = re.search(r'其骨([一二三四五六七八九十]+)层', hl)
    if not m:
        return None, None
    CNN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
    s = m.group(1)
    N = 10 if s == '十' else (10 + CNN.get(s[1], 0) if s.startswith('十') else CNN.get(s, 0))
    # 层之目：行首之 ①—⑩，或 ①之二／④之三 一类
    层 = set()
    for mm in re.finditer(r'^([①②③④⑤⑥⑦⑧⑨⑩])(之[一二三四五六七八九十])?', hl, re.M):
        层.add(mm.group(0))
    return N, len(层)


def 三路(txt, n=None, 全书=None):
    """返回 (约数红, 引文报, 数报)；★只有头一样作闸。"""
    if '【本章亮点】' not in txt:
        return [], [], []
    body, hl = txt.split('【本章亮点】', 1)
    B = 剥(body)
    约红 = [m.group(0) for m in re.finditer(约, hl) if m.group(0) not in B]
    引报 = []
    for q in dict.fromkeys(re.findall(r'「([^」]{4,})」', hl)):
        if 剥(q) in B or re.search(r'(不许|须|该|凡|即须)', q):
            continue
        他 = False
        if 全书:
            for m, p2 in 全书.items():
                if m != n and 剥(q) in 剥(io.open(p2, encoding='utf-8').read()):
                    他 = True; break
        if not 他:
            引报.append(q)
    数报 = [a + b + c for a, b, c in
            dict.fromkeys(re.findall(r'([一二三四五六七八九十百零两]+)([来多余几]?)' + 量词, hl))
            if a + b + c not in B]
    return 约红, 引报, 数报


def 查(n, 路, 全书=None, 报=True, 详=False):
    txt = io.open(路, encoding='utf-8').read()
    约红, 引报, 数报 = 三路(txt, n, 全书 if 详 else None)
    N, M = 骨层数(txt)
    骨红 = (N is not None and M is not None and N != M)
    if 报:
        if 骨红:
            print('  ⛔ 第%d章 亮点段自书「其骨%d层」，而其下所列之层只有 %d 条。' % (n, N, M))
            print('     ★改亮点段之骨而只改了那个数——多半是一次静默的 replace 未命中。')
        if 约红:
            print('  ⛔ 第%d章 约数相犯 %d 处：%s' % (n, len(约红), '、'.join(约红)))
            print('     ★亮点段不许把正文给准了的数抹成约数。')
        else:
            print('  ✓ 第%d章 亮点段·约数零相犯' % n)
        if 详:
            if 引报:
                print('     ℹ引文可疑 %d 处（报而不拦·此路全书红20%%，多为着重号与概括）：' % len(引报))
                for q in 引报[:6]:
                    print('        「%s」' % q)
            if 数报:
                print('     ℹ数可疑 %d 处（报而不拦·此路全书红18%%，多为概括之数）：%s'
                      % (len(数报), '、'.join(数报[:8])))
    return 1 if (约红 or 骨红) else 0


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('-')]
    全 = 诸章()
    print('════ 亮点对表 ════')
    if '--全' in sys.argv:
        def _红(n):
            _t = io.open(全[n], encoding='utf-8').read()
            _N, _M = 骨层数(_t)
            return bool(三路(_t)[0]) or (_N is not None and _M is not None and _N != _M)
        bad = [n for n in sorted(全) if _红(n)]
        for n in bad:
            查(n, 全[n])
        print('  约数相犯之章 %d／%d' % (len(bad), len(全)))
        sys.exit(1 if bad else 0)
    if not a:
        print('用法：python3 工具/亮点对表.py N ｜ --全'); sys.exit(2)
    n = int(a[0])
    if n not in 全:
        print('⛔ 第%d章之正文不在' % n); sys.exit(2)
    sys.exit(查(n, 全[n], 全, 详=True))
