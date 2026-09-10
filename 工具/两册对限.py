# -*- coding: utf-8 -*-
"""两册对限（2026-09-04·300第7轮立）

★所治之伤：**一笔改了限，而另一册没跟着改。**
　★2026-09-04 本坐把 PRES-297B刘二 之限由300改作301，
　　同笔改了 `设定/大问挂账.md`、圣经300锚、施工表、300之开镜卡四处；
　★★**而 `设定/到期账.json` 照旧写着 300，三坐无人看见**——
　　直到第7轮 `小说检察官.py --五钩 300` 之到期账那一节把它印出来。
★★此即 欠-297A 之形（**令与闸各读一册**）：
　`大问表.py` 只读大问挂账，`检察官/书级体检` 只读到期账，二册之间无一道桥。

【它认哪几样，本书同类共几样（令§六④）】
· **它认**：**两册俱有之笔**——以「其形／事」之白文长串相认（去★与标点後取前16字）；
　　**其判只一样**：**同一笔之「限第N章」与「到期章」须相等。**
· **本书同类共几样**：`大问挂账.md` 挂着者 10 笔｜`到期账.json` open 且带到期章者 6 笔｜
　　**而两册俱有、认得上的只有 2 对**（PRES-297A东头｜PRES-297B刘二）。
　★**故此器只看得见十分之二**——**其余八笔只在一册上，本器一个字也不说**；
　★★**记此一行是为免把它的绿读成「两册全对上了」**（§一⑤）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
挂账 = os.path.join(ROOT, '设定', '大问挂账.md')
到期 = os.path.join(ROOT, '设定', '到期账.json')


def _净(s):
    return re.sub(r'[★\*（）()「」，。；、：\s]', '', s or '')


def 读挂():
    out = []
    if not os.path.exists(挂账):
        return out
    for ln in io.open(挂账, encoding='utf-8'):
        if not ln.startswith('|'):
            continue
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) < 7 or c[-1] != '挂':
            continue
        m = re.search(r'(\d+)', c[3])
        if m:
            out.append((c[0].strip('*'), int(m.group(1)), c[5]))
    return out


def 读期():
    if not os.path.exists(到期):
        return []
    d = json.load(io.open(到期, encoding='utf-8'))
    return [it for it in d.get('items', [])
            if it.get('状态') == 'open' and isinstance(it.get('到期章'), int)]


def 对():
    """返回 (对得上者, 不合者)。"""
    挂, 期 = 读挂(), 读期()
    pair, bad = [], []
    for 名, 限, 形 in 挂:
        k = _净(形)[:16]
        if not k:
            continue
        for it in 期:
            if k in _净(it.get('事', '')):
                pair.append((名, 限, it['id'], it['到期章']))
                if 限 != it['到期章']:
                    bad.append((名, 限, it['id'], it['到期章']))
                break
    return pair, bad


def 报(quiet=False):
    挂, 期 = 读挂(), 读期()
    pair, bad = 对()
    if not quiet:
        print('════ 两册对限 · 大问挂账 对 到期账 ════')
        print('  挂账挂着者 %d 笔｜到期账 open 且带到期章者 %d 笔｜两册认得上者 %d 对'
              % (len(挂), len(期), len(pair)))
        for 名, 限, i, n in pair:
            print('   %-6s 挂账限%-4d 到期账限%-4d %s' % (名, 限, n, '⛔不合' if 限 != n else '✓'))
        if bad:
            print('  ⛔ 两册不合 %d 笔——★一笔改了限而另一册没跟着改（欠-297A之形）。' % len(bad))
            print('     ★★其治不是挑一册为准，是二册同笔改，且各写一行改期记因。')
        else:
            print('  ✓ 两册认得上的逐笔同限。')
        print('  ★而其余 %d 笔只在一册上，本器一个字也不说（§一⑤：绿只及於器自印之项名）。'
              % (len(挂) + len(期) - 2 * len(pair)))
    return pair, bad


if __name__ == '__main__':
    _p, _b = 报()
    sys.exit(1 if _b else 0)
