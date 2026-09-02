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


项表 = {
    '因为': _千字(r'因为'),
    '像': _千字(r'像[^，。；]{2,20}'),
    '而起手': lambda b: (sum(1 for s in re.split(r'(?<=[。！？])', re.sub(r'[\s＊*]', '', b))
                           if s.startswith('而')) * 1000.0 / _净(b)) if _净(b) else 0.0,
    '我把': _千字(r'我把'),
    '她把': _千字(r'她把'),
    '90分位': _p90,
    '最长段': _最长,
}


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
        lo_, hi_, md = min(xs), max(xs), st.median(xs)
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
