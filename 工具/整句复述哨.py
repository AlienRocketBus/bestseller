# -*- coding: utf-8 -*-
"""整句复述哨 —— 本章哪几句是从前章逐字搬来的（2026-09-05·机制总审·八路之覆盖之缺审第9条：P21 整句复述复发7而器只管章内四字串与 N-2）

★其红在哪一行（上磁盘核）：病历本 P21「81开篇比喻、87认脸段、89三问、91老头清点原话、93复述77火塘原场」——
  ★而本书之器：四字串三现只看章内；连读客问五只比 N-2（同线前一章）；**跨任意前章之照抄，无一器读。**
★★它认哪几样，本书同类共几样（`python3 工具/整句复述哨.py --自测` 之①逐年重数）：
  · 认：**本章白文里 ≥10 汉字之整句（以 。！？；断，去标点），与第1至N-1任一章之整句逐字同者**，并印其首见之章。
  · 本书今 357 处／165 章（近三十章每章 0—8 处；304 章 8 处为顶）。
  · 不认：<10 字之句（口头禅与短令，如「跟昨天一样。」）；亮点段；章题。
★★★其判：**不判红，只上桌**——本书有意之回响不少（「怀里那本子，湿了就没有了」301承299；「跟昨天一样，跟前天一样」），
  故此哨只把每一句摆上桌（今由 大审.py --包 逐章跑之），逼人答「有意的回响，还是懒的搬」。

用法：
    python3 工具/整句复述哨.py 305        # 印第305章之复述句与其源章
    python3 工具/整句复述哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
最短 = 10
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn2i(t):
    v = 0
    m = re.match(r'([一二三四五六七八九])?百(.*)', t)
    if m:
        v = CN.get(m.group(1), 1) * 100
        t = m.group(2)
    m = re.match(r'([一二三四五六七八九])?十(.*)', t)
    if m:
        v += CN.get(m.group(1), 1) * 10
        t = m.group(2)
    for c in t:
        if c in CN:
            v += CN[c]
    return v


def 章号(p):
    m = re.search(r'第(.+?)章', os.path.basename(p))
    return cn2i(m.group(1)) if m else -1


def 白文(t):
    t = t.split('【本章亮点')[0]
    return re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)


def 整句(body):
    """返回 [(净句, 原句)]，净句去标点、≥最短 字。"""
    out = []
    for s in re.split(r'[。！？；\n]', body):
        净 = re.sub(r'[^一-龥]', '', s)
        if len(净) >= 最短:
            out.append((净, s.strip()))
    return out


def 库(至, 窗=None):
    """第1至 至-1 章之净句 → 首见之章。窗=k 则只看 至-k…至-1（旧式连读客之窗，供回灌）。"""
    首见 = {}
    for p in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md')), key=章号):
        n = 章号(p)
        if n <= 0 or n >= 至 or (窗 and n < 至 - 窗):
            continue
        for 净, _ in 整句(白文(io.open(p, encoding='utf-8').read())):
            首见.setdefault(净, n)
    return 首见


def 查(n, body=None, 窗=None):
    """返回 [(原句, 源章)]——本章与前章逐字同之整句。body 可给（测试用）；窗=k 只看前 k 章（旧式回灌用）。"""
    if body is None:
        fs = [p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if 章号(p) == n]
        if not fs:
            return None
        body = 白文(io.open(fs[0], encoding='utf-8').read())
    首见 = 库(n, 窗)
    seen = set()
    out = []
    for 净, 原 in 整句(body):
        if 净 in 首见 and 净 not in seen:
            seen.add(净)
            out.append((原, 首见[净]))
    return out


def 报(n):
    r = 查(n)
    print('════ 整句复述哨 · 第%d章 ════' % n)
    print('  【其律】≥%d 字之整句与任一前章逐字同者上桌；不判红——判「有意的回响」还是「懒的搬」，归大审。' % 最短)
    if r is None:
        print('  ⛔无第%d章正文' % n)
        return 2
    if not r:
        print('  ✓ 本章无一句与前章逐字同。')
        return 0
    for 原, m in r:
        print('  ⚠ 「%s」 ← 第%d章' % (原[:40], m))
    print('  共 %d 句；逐句须判（合／删）。' % len(r))
    return 0


def 自测():
    R = []
    # ①磁盘之群：全书 ≥ 300 处、≥ 150 章（证其非孤例，§十三）
    tot = 0
    章 = 0
    fs = sorted(glob.glob(os.path.join(ROOT, '正文', '*.md')), key=章号)
    首见 = {}
    for p in fs:
        n = 章号(p)
        hits = 0
        for 净, _ in set(整句(白文(io.open(p, encoding='utf-8').read()))):
            if 净 in 首见 and 首见[净] < n:
                hits += 1
            else:
                首见.setdefault(净, n)
        if hits:
            章 += 1
            tot += hits
    R.append(('①其群·全书 %d 处／%d 章（须≥300／≥150）' % (tot, 章), tot >= 300 and 章 >= 150))
    # ②真红：第93章须有一句源自第77章（病历本 P21 所记之「93复述77火塘原场」）
    r93 = 查(93) or []
    R.append(('②真红·第93章有句源自第77章（P21 原案）', any(m == 77 for _, m in r93)))
    # ③不喊狼：<10 字不认
    r = 查(305, body='跟昨天一样。\n跟前天一样。\n')
    R.append(('③短句不认（<%d 字）' % 最短, r == []))
    # ④认十字以上之逐字同（以 301 之一句造文喂 305 之位，须报其源为 301 或更早）
    r = 查(305, body='怀里那本子，湿了就没有了。\n今天先量钥匙。\n')
    R.append(('④十字以上之逐字同必报，并给首见之章（%s）' % (r[0][1] if r else '无'), bool(r) and r[0][1] <= 301))
    # ⑤旧式回灌：连读客问五只比 N-2（同线前一章）——以窗=2 回灌第93章，77之句须不在其内；全窗则在
    r_old = 查(93, 窗=2) or []
    R.append(('⑤旧式回灌·窗=2（连读客之窗）看不见 93←77，全窗看得见（旧 %d 条／新 %d 条）' % (len(r_old), len(r93)),
              not any(m == 77 for _, m in r_old) and any(m == 77 for _, m in r93)))
    # ⑥自陈在册（旧⑥必答项之式随十三轮之必答表 1027 汰）
    src = io.open(__file__, encoding='utf-8').read()
    R.append(('⑥自陈在册·它认哪几样／不判红只上桌', '它认哪几样' in src and '不判红' in src))
    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·整句复述哨 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '有败'))
    return 0 if not bad else 1


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(自测())
    a = [x for x in sys.argv[1:] if x.isdigit()]
    sys.exit(报(int(a[0])) if a else 2)
