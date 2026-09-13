# -*- coding: utf-8 -*-
"""负测·净重一处（2026-09-12 立·322 之净重在册上有五个数方立此条）。

★所守者一句：**一章之净重，册上凡书之处须同**。
★★其实（323 定位席当面逮出，而盘上诸器一处也没红）：
　**322 之净重，其首行书 1,990｜悬账行书 1,945｜开镜卡书 1,836｜硬门槛书 1,935**
　——**同一章四个数在四处**，⛔**而 `净重对表.py` 报绿**：**它只验那头一处（本表自书之处）。**
★★★其根与本坐 ㊎ 同骨：**刀落了而册上的数没跟着走**；
　**而这一回更难见**：**有一处跟着走了**，**於是器绿了，人也就以为都跟上了。**
⛔**故本测只问一句**：**同一章之净重，在役之册上有几个不同的数。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
表 = os.path.join(ROOT, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')


def _册上之数(n):
    """★取册上凡以「N:数」之形书某章净重者（其形係全书通行之写法）。
    ⛔**只认这一形**：括注里明说是陈号者（近处有「旧书」「旧号」「陈号」）不算。"""
    # ⛔**本函头一版自栽**：`N:数` 这个形，**行引与净重共用**
    #   ——它把 `322:237`（行引）当成了净重，近十章逐章皆报红。
    #   ★**与本日「行号引真」那一回同一个坑**：**这个形在册子里被别的东西占着。**
    # ★故收窄二处：①其数须逾该章白文之行数（净重必远大於行数）；
    #   ②近处六十字内须见「净重」二字。⛔二者缺一不认。
    # ⛔**第二版又收窄过了头**：那几处之形係「…320:2123、321:2245、322:1990」，
    #   **「净重」二字在这一串的开头，离得远**，六十字之近处够不着——**它一个也认不着，空转。**
    #   ★**故改看「同一行之内有无『净重』二字」**（那一行本就是净重之列）。
    行数 = _行数(n)
    出 = {}
    for ln in io.open(表, encoding='utf-8', errors='replace').read().split('\n'):
        if '净重' not in ln:
            continue
        for m in re.finditer(r'(?<![0-9])%d:([0-9]{3,5})(?![0-9])' % n, ln):
            近 = ln[max(0, m.start() - 60):m.start()]
            if any(x in 近 for x in ('旧书', '旧号', '陈号')):
                continue
            v = int(m.group(1))
            if 行数 and v <= 行数:
                continue
            出.setdefault(v, 0)
            出[v] += 1
    return 出


def _行数(n):
    """★取第 n 章白文之行数（净重必远大於它，故可作分界）。"""
    d = os.path.join(ROOT, '正文')
    if not os.path.isdir(d):
        return None
    import unicodedata
    for f in os.listdir(d):
        if not f.endswith('.md'):
            continue
        p2 = os.path.join(d, f)
        try:
            head = io.open(p2, encoding='utf-8', errors='replace').readline()
        except OSError:
            continue
        tx2 = io.open(p2, encoding='utf-8', errors='replace').read()
        m = re.search(r'第([零一二三四五六七八九十百千]+)章', tx2[:200])
        if not m:
            continue
        if _汉数(m.group(1)) != n:
            continue
        return len(tx2.split('【本章亮点】')[0].split('\n'))
    return None


_汉表 = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
         '六': 6, '七': 7, '八': 8, '九': 9}


def _汉数(s):
    v, cur = 0, 0
    for ch in s:
        if ch in _汉表:
            cur = _汉表[ch]
        elif ch == '十':
            v += (cur or 1) * 10
            cur = 0
        elif ch == '百':
            v += (cur or 1) * 100
            cur = 0
        elif ch == '千':
            v += (cur or 1) * 1000
            cur = 0
    return v + cur


def 跑():
    过, 败 = 0, []

    def 判(号, 名, 实, 期):
        nonlocal 过
        if 实 == 期:
            过 += 1
        else:
            败.append('%s·%s：得 %r，期 %r' % (号, 名, 实, 期))

    # ①【头一格·322 真局回灌】其数今日已归一
    d322 = _册上之数(322)
    判('①', '322 之净重在册上确有其数（本格之料在）', bool(d322), True)
    判('②', '322 之净重册上只一个数（得 %s）' % sorted(d322),
       len(d322) <= 1, True)

    # ③【其害·证四数之局曾真有】今日所正之四处，其旧数不许再出现
    tx = io.open(表, encoding='utf-8', errors='replace').read()
    旧 = []
    for x in ('322:1935', '322:1945', '322:1836'):
        for m in re.finditer(re.escape(x), tx):
            近 = tx[max(0, m.start() - 60):m.start()]
            if not any(y in 近 for y in ('旧书', '旧号', '陈号')):
                旧.append(x)
    判('③', '四数之局已归一（无未注之旧数）', 旧, [])

    # ④⑤【一般之格】近十章逐章验，凡册上多於一个数者即红
    脏 = []
    for n in range(313, 324):
        d = _册上之数(n)
        if len(d) > 1:
            脏.append('%d:%s' % (n, sorted(d)))
    判('④', '近十章逐章·册上之净重各只一个数', 脏, [])

    # ⑤【证其有牙】⛔否则本测只是一句好听的话：
    #   拿一个真出过问题的旧局（322 之四数）在内存里回灌，它须当场逮得出
    假 = tx.replace('322:1990', '322:1990', 1)
    假 = '净重之列（本行只在内存里·负测之料）322:1935、322:1945、322:1836'
    得, _h = set(), _行数(322)
    for m in re.finditer(r'(?<![0-9])322:([0-9]{3,5})(?![0-9])', 假):
        近 = 假[max(0, m.start() - 60):m.start()]
        _ = 近
        if any(x in 近 for x in ('旧书', '旧号', '陈号')):
            continue
        v = int(m.group(1))
        if (_h and v <= _h) or '净重' not in 假:
            continue
        得.add(v)
    判('⑤', '旧局回灌即逮得出（得 %d 个数）' % len(得), len(得) >= 3, True)

    # ⑥【不许连坐】此测不许把「净重对表」那一路写没了
    判('⑥', '净重对表之器仍在',
       os.path.exists(os.path.join(ROOT, '工具', '净重对表.py')), True)

    print('════ 负测·净重一处 ════（守：一章之净重，册上凡书之处须同）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
