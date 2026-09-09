# -*- coding: utf-8 -*-
"""比带（2026-09-02·293第8轮立）
所治之伤：**一把带，取错了比的人，就把三处好文判成了伤。**

★本坐之实（非设想）：293第5、7、8三轮，各逮一「逾带」，而三处用的是同一把带——
  **苏衍近五章（282／285／287／289／291）**；★★而那五章之形是做事与问人，
  **293是他近年唯一一篇翻判**；★★★换成形相同之十八章（201—280之翻判诸章），
  三个数一个也不逾带：
      项          同镜之带（他近五章）   同形之带（十八章）    本章
      「因为」/千字   0.0—0.0  ⛔逾带      0.0—3.1 中位1.18    2.3  ✓
      「像…」/千字    0.0—0.2  ⛔逾带      0.0—1.2 中位0.31    0.9  ✓
      段长90分位     31—36    ⛔逾带      30—76   中位34      38   ✓
  ★★★★**三个「逾带」，一个也不成立。**

★而其所以险，不在这三处，在这一类：**「比她自己」这一句，本坐用了整整两章**
  （292之句方差、最长句、「她把」；293之三处）；★★**而它对了几回，是因为292那几章
  凑巧同形（沈鸢诸章多记账），不是因为那把尺挑对了。**
★★★**故此器只办一件事：一个数报三条带**（全书／同镜／同形），**并印出本章落在哪几条里**；
  ★★★★**而它不判**——**它只是不许我再只看一条带就下判。**

用法：
    python3 工具/比带.py 293 因为
    python3 工具/比带.py 293 --项 90分位
    python3 工具/比带.py 293 --全            ← 逐项皆报
"""
import io, os, re, sys, glob, statistics as st
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _iu.spec_from_file_location('_lz6', os.path.join(ROOT, '工具', '开轮六检.py'))
_m6 = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_m6)


def _白(c):
    try:
        return _m6.body(c) or ''
    except Exception:
        return ''


def _净(b):
    return len(re.sub(r'[\s＊*]', '', b))


def _拍(b):
    return [re.sub(r'\s', '', p) for p in b.split('＊') if p.strip()]


# ── 项：每一项给一个「取数之法」。凡加新项，须同日答「它认哪几样」（令§六④）──
def _千字(pat):
    def f(b):
        n = _净(b)
        return (len(re.findall(pat, b)) * 1000.0 / n) if n else 0.0
    return f


def _p90(b):
    L = sorted(len(p) for p in _拍(b))
    return L[int(len(L) * 0.9)] if len(L) >= 10 else 0


def _最长(b):
    L = [len(p) for p in _拍(b)]
    return max(L) if L else 0


def _句方差(b):
    """★与 看官.py::评论员 同源之量法（st.pvariance 於以。！？切出之句长）——
    ★★同一个数只许有一把尺；两处各造一把，日後两处判不同即无从对账。"""
    ss = [y for y in re.split(r'[。！？]', re.sub(r'\s', '', b)) if y]
    return st.pvariance([len(y) for y in ss]) if len(ss) > 1 else 0.0


def _段方差(b):
    L = [len(p) for p in _拍(b)]
    return st.pvariance(L) if len(L) > 1 else 0.0


项表 = {
    '因为': _千字(r'因为'),
    '像': _千字(r'像[^，。；]{2,20}'),
    '而起手': lambda b: (sum(1 for s in re.split(r'(?<=[。！？])', re.sub(r'[\s＊*]', '', b))
                           if s.startswith('而')) * 1000.0 / _净(b)) if _净(b) else 0.0,
    '我把': _千字(r'我把'),
    '她把': _千字(r'她把'),
    '90分位': _p90,
    '最长段': _最长,
    '句方差': _句方差,
    '段方差': _段方差,
    # ★★★★★2026-09-03·295第5轮补四项（其立之由见档尾「四感之补」）
    '嗅': _千字(r'味|气味|鼻|闻'),
    '听': _千字(r'听|响|声|叫|吠'),
    '触': _千字(r'凉|温|烫|硬|软|摸|按|贴'),
    '视': _千字(r'灯|光|看|眼|见'),
}

# ★★★★★四感之补（2026-09-03·295第5轮）
# ★其红在哪一行：295第4轮之一疑问「收尾三拍有没有触」，而留给第5轮之器是 `比带`；
#   ★★而 `比带` 之项表原只九样（因为／像／而起手／我把／她把／90分位／最长段／句方差／段方差），
#   **一项嗅听触视也没有**——**那一疑遂挂在空处**（令§七★：挂之前先问那一轮的器验不验这一样）。
# ★★★而第5轮正是「在场庭」——**一轮之名就是四感，而它那一轮的器一项四感也不量。**
# ★★★★其判据与 `跑轮.py::_soft` 逐字同一处正则（嗅：味|气味|鼻|闻｜听：听|响|声|叫|吠｜
#   触：凉|温|烫|硬|软|摸|按|贴｜视：灯|光|看|眼|见）——**一个数不许有两把尺。**
#   ★而其别只一样：`跑轮` 记的是**处数**，本器记的是**每千字**（带须可比，故须归一）。


def _形(c):
    """★卡为先，词频为退（与 开轮六检::check17 同法）。"""
    kj = os.path.join(ROOT, '版本', '第%d章' % c, '_开镜卡.md')
    if os.path.exists(kj):
        m = re.search(r'本章之形[：:）\)\*★]*[^\n]{0,12}?(问人|记账|做事|翻判)',
                      io.open(kj, encoding='utf-8', errors='replace').read())
        if m:
            return m.group(1)
    b = _白(c)
    if not b:
        return None
    sc = {k: sum(b.count(w) for w in ws) for k, ws in _m6.FORM.items()}
    return re.sub(r'（.*', '', max(sc, key=sc.get))


def _镜(c):
    """★暗线之镜以「她」为主，主线以「我」为主；只分二类，不猜其名。"""
    b = _白(c)
    return '暗线' if b.count('她') > b.count('我') else '主线'


# ★★★★★DEBT-297C（297第5轮立·限307·於307封版之序结清）
#   ★其伤逐字（到期账 items::DEBT-297C）：**「带() 之底取 min(xs)，故凡全书有一章此项为零者，
#     其「低於其底」永不报」**——297第5轮实逮：**听项全书94章中5章为0（同形19章中只1章）**，
#     **而297听0.0照旧印「✓在带内」**。
#   ★★即：**一个零章就把整条带的底钉死在零上，此後任何一章的零都合格**——
#     **一把尺被它自己的最差那一个样本废掉了。**
#   ★★★其治（照其档所命）：**底改取分位（10分位）**，不再取 min；顶照旧取 max
#     （★顶不改之由：逾顶者係「多」，多一处从来不会把顶钉死在无穷大上，其病不对称）。
#   ★★★★而其验（照其档所命之头一项断言）：**以297第5轮之前的听0回灌，新式须报红而旧式报绿**
#     ——其测在 `工具/负测_比带.py::八`，且以旧式（min）对同一份数回灌须照旧报绿，故非陪跑。
def 底(xs, q=0.10):
    """取分位之底（默认10分位·线性插值），而非 min——一个零章不许把整条带的底钉死在零上。"""
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    i = q * (len(ys) - 1)
    lo_i = int(i)
    hi_i = min(lo_i + 1, len(ys) - 1)
    return ys[lo_i] + (ys[hi_i] - ys[lo_i]) * (i - lo_i)


def 带(c, 项名, lo=200):
    f = 项表[项名]
    本 = f(_白(c))
    我形, 我镜 = _形(c), _镜(c)
    全, 同镜, 同形 = [], [], []
    for k in range(lo, 294):
        if k == c:
            continue
        b = _白(k)
        if not b or _净(b) < 500:
            continue
        v = f(b)
        全.append(v)
        if _镜(k) == 我镜:
            同镜.append(v)
        if _形(k) == 我形:
            同形.append(v)
    def 说(名, xs):
        if len(xs) < 3:
            return '  %-6s（章数%d，不足三章，不作带）' % (名, len(xs))
        lo_, hi_, md = 底(xs), max(xs), st.median(xs)
        judge = '✓在带内' if lo_ <= 本 <= hi_ else ('⛔逾其顶' if 本 > hi_ else '⛔低於其底')
        return '  %-6s 章数%-4d 带 %.1f—%.1f 中位%.2f ｜ 本章 %.1f  %s' % (名, len(xs), lo_, hi_, md, 本, judge)
    print('\n── 比带 · 第%d章 · 项「%s」──' % (c, 项名))
    print('  本章之镜 %s｜本章之形 %s｜本章之数 %.1f' % (我镜, 我形, 本))
    print(说('全书', 全))
    print(说('同镜', 同镜))
    print(说('同形', 同形))
    print('  ★三条带若不同判，以同形为先——**本坐第5、7、8三轮各栽一回，皆因只看同镜那一条。**')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip())
        raise SystemExit(1)
    n = int(sys.argv[1])
    rest = [x for x in sys.argv[2:] if not x.startswith('--')]
    if '--全' in sys.argv:
        for k in 项表:
            带(n, k)
    else:
        for k in (rest or ['因为']):
            if k not in 项表:
                print('  ✗ 无此项：%s（现有 %s）' % (k, '、'.join(项表)))
                raise SystemExit(2)
            带(n, k)
