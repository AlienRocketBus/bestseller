#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自走（2026-09-13 立·作者当面点名：「**设置个机制，跑起来就必须得跑起来，不能再停下了**」）。

★立此器之由，一句话：**链条断在人身上，不是断在器上。**
　**盘上诸器各守一样，而没有一样东西回答那个最要紧的问**：**此刻这一坐该干哪一件。**
　⛔**於是每一回都要一个人把七八样印看一遍、自己拼出下一步**——**而人会停，器不会。**

★★**本器只答一句话**：**下一件是什么，那一条命令逐字怎么写。**
　⛔**它不判小说、不改一个字、不动任何账**——**只读盘，只印一行。**
　★**其序写死（先来后到，头一件成立即印它，不往下看）**：
　　①**有人在跑** → 不许抢锁：印「候」，并印它跑到哪一段。
　　②**末章未封版**（回执不在）→ 印「接着跑那一章」。
　　③**末章封版而其第十一轮未过** → 印「补跑第十一轮」或「派救章席」。
　　④**逾期之欠压在下一章头上** → 印它，并把它写进下一章之卡。
　　⑤**以上皆清** → 印「起下一章」，并把三条前置之命令一并印出。
　★★**其末一行永远是一条可以照抄去跑的命令**——⛔**不许印「你可以考虑」这种话。**

用法：
    python3 工具/自走.py            # 印下一件
    python3 工具/自走.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import glob
import io
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def _num(s):
    tot, cur = 0, 0
    for ch in s:
        if ch in CN:
            cur = CN[ch]
        elif ch == '十':
            tot += (cur or 1) * 10
            cur = 0
        elif ch == '百':
            tot += (cur or 1) * 100
            cur = 0
        elif ch == '千':
            tot += (cur or 1) * 1000
            cur = 0
    return tot + cur


def 末章():
    ns = []
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', os.path.basename(f))
        if m:
            ns.append(_num(m.group(1)))
    return max(ns) if ns else 0


def 有人在跑():
    """返回 (在跑?, 第几章, 停了几分钟)。⛔其限之数自 心跳.py 现取，不写死。"""
    p = os.path.join(ROOT, '_心跳.json')
    if not os.path.exists(p):
        return False, None, None
    try:
        d = json.load(io.open(p, encoding='utf-8'))
    except Exception:
        return True, None, None          # 读不出，作有人论（宁可候，不可抢）
    if d.get('章') is None:
        return False, None, None         # 已撤锁
    s = io.open(os.path.join(ROOT, '工具', '心跳.py'), encoding='utf-8').read()
    m = re.search(r'^限\s*=\s*(\d+)\s*\*\s*60', s, re.M)
    lim = int(m.group(1)) * 60 if m else 45 * 60
    age = int(time.time()) - int(d.get('时', 0))
    return (age <= lim), d.get('章'), age // 60


def 回执在(n):
    return bool(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n)))


def 十一轮过(n):
    return os.path.exists(os.path.join(ROOT, '版本', '第%d章' % n, '_十一轮.json'))


def 卡在(n):
    return os.path.exists(os.path.join(ROOT, '版本', '第%d章' % n, '_开镜卡.md'))


def 逾期之欠(n):
    """到期章 ≤ n 而状态仍 open 者。"""
    p = os.path.join(ROOT, '设定', '到期账.json')
    if not os.path.exists(p):
        return []
    try:
        d = json.load(io.open(p, encoding='utf-8'))
    except Exception:
        return []
    out = []
    for x in d.get('items', []):
        if str(x.get('状态', '')).lower() != 'open':
            continue
        due = x.get('到期章')
        if isinstance(due, int) and due <= n:
            out.append((x.get('id'), due, str(x.get('事', ''))[:46]))
    return sorted(out, key=lambda y: y[1])


def 候时之活():
    """★2026-09-13 立：印「候」之时，顺手把盘上现成的真活点出来。

    ⛔**其由**：律⑪写着「候不是停，手上须同时办另一件真活」，
    **而它从来没说是哪一件**——**於是每一回候，都要现想一件**；
    ★**现想出来的那一件，十有八九是「我看了什么」而不是「我改了什么」**（律⑫：报告不是交付）。
    ★★**故本器不再只印那一句令，改印盘上此刻真红的那几样**——**逐条带其命令。**
    ⛔**本器只印，不办；一个字也不写盘。**
    """
    out = ['  ── 候时可办之真活（盘上现成，⛔挑一件真办掉，不是看一眼）──']
    n = 0
    # 一·到期账：限已到或将到而未清者（⛔数「不在已清词表之内者」，非只数 open·体检账 ㊨）
    try:
        import json as _j
        清 = ('done', 'closed', 'half', '废弃', 'cold', '冷藏', '已清', '清')
        d = _j.load(io.open(os.path.join(ROOT, '设定', '到期账.json'),
                            encoding='utf-8'))
        末 = 末章()
        欠 = [x for x in d.get('items', [])
              if x.get('状态') not in 清
              and isinstance(x.get('到期章'), int)
              and x['到期章'] <= 末 + 2]
        for x in 欠[:4]:
            n += 1
            out.append('  %d. 到期账 %s（限%s）：%s'
                       % (n, x.get('id'), x.get('到期章'), (x.get('事') or '')[:46]))
    except Exception:
        pass
    # 二·诸器之红（只点其名与其命令，⛔本器不代跑——跑起来动辄十分钟）
    for 名, 令 in (('书级体检', 'python3 工具/书级体检.py'),
                   ('跑账', 'python3 工具/跑账.py'),
                   ('净重对表', 'python3 工具/净重对表.py'),
                   ('FS闸', 'python3 工具/FS闸.py')):
        n += 1
        out.append('  %d. 跑一回 %s 看它红没红：%s' % (n, 名, 令))
    out.append('  ★办毕须落到盘上（`git log` 多一笔），⛔否则这一回合等於没有（律⑫）。')
    return out


def 锁滞(ch):
    """★2026-09-16 立：**席已办毕而锁未撤**——问 `_任务流.json` 之末笔，不问心跳。

    ⛔**其所由来·0916 之实**：335 之席十一段全走完（工作流回了结果，`封版席毕` 一笔已落
    `_任务流.json`），⛔**而 `心跳.py --收 335` 那一步不在 `一章.js` 的收口段里**——
    **於是锁原样挂着，`自走.py` 照旧印「候」，而其实那一席早就没了。**
    ★**其价**：本坐候了七分钟才自己想起去看 `续跑`；**若无人看，它要挂满 45 分钟才自动过期**——
    **一章之间白丢三刻钟，而律⑰正是为「席一收，头一件事是派下一席」而立的。**
    ⛔**本器不改 `一章.js`**（那是收口段之事，交工具席）——**它只保证这三刻钟不再白丢。**
    """
    try:
        d = json.load(io.open(os.path.join(ROOT, '_任务流.json'), encoding='utf-8'))
    except Exception:
        return False                 # 读不出即作「席还在」论（宁可候，不可抢）
    return 判锁滞(d.get('步') or [], ch)


def 判锁滞(步, ch):
    """⛔纯判·不碰盘——**自测拿它跑假料，不拿今日之实去钉**（㊸：一张快照钉进一条常令）。"""
    for 笔 in reversed(步):
        事 = str(笔.get('事') or '')
        if 事.startswith('存底'):     # 存底流水不算段
            continue
        return 事.startswith('%s·封版席毕' % ch)
    return False


def 断(印=True):
    """返回 (判, 诸行)。判 ∈ 候／跑／补／救／欠／起。"""
    L, 末 = [], 末章()
    跑, ch, 分 = 有人在跑()
    if 跑 and 锁滞(ch):
        L.append('  【判】起。第%s章之席**已办毕而锁未撤**（`_任务流.json` 末笔＝%s·封版席毕）。' % (ch, ch))
        L.append('  ★**这不是抢锁**：那一席十一段全走完了，只是收口段里没有撤锁那一步。')
        L.append('  ⛔**而先验一遍再撤**：封版五件须俱在（回执／锁定行／下一章开镜卡／封版之锚／正文）。')
        L.append('  ── 下一条命令 ──')
        L.append('  python3 工具/心跳.py --收 %s        # 撤毕再跑一回本器，它会印「起」' % ch)
        return '起', L

    if 跑:
        L.append('  【判】候。第%s章之席在跑（%s 分钟前报到）。' % (ch, 分))
        L.append('  ⛔不许抢锁、不许动盘。★而候不是停：手上须同时有另一件真活')
        L.append('     （治闸／补账／清欠／写下一段之势），办完再跑一回本器。')
        L.append('  ⛔⛔而席在跑之时，一切动整个工作区的命令一律不许（律⑮）：')
        L.append('     git stash／git checkout .／git reset --hard／git clean／git add -A')
        L.append('     ——只许动我自己手上那几条明路径。要比改前改後：git show HEAD:<路径> > /tmp/旧.md')
        for x in 候时之活():
            L.append(x)
        L.append('  ── 下一条命令 ──')
        L.append('  python3 工具/续跑.py        # 看它跑到哪一段了')
        return '候', L

    if not 回执在(末):
        L.append('  【判】跑。第%d章正文在盘而回执不在——那一章没走完。' % 末)
        L.append('  ── 下一条命令 ──')
        L.append('  python3 工具/心跳.py --跳 %d' % 末)
        L.append('  Workflow({scriptPath:\'工具/席/一章.js\', args:{章:%d}})' % 末)
        return '跑', L

    if not 十一轮过(末):
        L.append('  【判】补。第%d章回执已交，而第十一轮未跑或未过。' % 末)
        L.append('  ⛔批123／126：十轮跑完须跑，不过不许封版。')
        L.append('  ── 下一条命令 ──')
        L.append('  python3 工具/小说检察官.py --十一轮 %d' % 末)
        L.append('  ★若其左眼报「无真伤之轮≥5／层薄／对数不足」三条之一：')
        L.append('     Workflow({scriptPath:\'工具/席/救章.js\', args:{章:%d}})' % 末)
        return '补', L

    欠 = 逾期之欠(末 + 1)
    下 = 末 + 1
    if 欠:
        L.append('  【判】欠。有 %d 笔到期之账压在第%d章头上，须写进其卡再起笔：' % (len(欠), 下))
        for i, d, s in 欠:
            L.append('     · %-12s 限%-4s %s' % (i, d, s))
        L.append('  ⛔不许只挂不办；办不成即照实写明卡在哪一条，当场裁，不许无声顺延。')
        # ★★★★★★2026-09-13 补（体检账 ㊥·本坐当日两栽）：
        #   ⛔**我把两笔账的限都写成「下一章」，而没有先问一句「下一章是哪一条线」**——
        #   **327 是暗线，而那两笔皆係主线之物**：**那个限从写下来那一刻起就是空的。**
        #   ★故本器印「欠」时，必连这一问一并印出来，⛔不许下一坐再栽同一处。
        L.append('  ★★⛔而落笔之前先答这一问（体检账 ㊥·0913 本坐当日两栽）：')
        L.append('     **这一笔是谁的物、谁的线？第%d章是哪一条线？**' % 下)
        L.append('     ⛔两条对不上，即当场把它改挂到那条线走得到的头一章——')
        L.append('     **非顺延，是改挂**；★而一个挂在它走不到的章上的限，到期只会逼出')
        L.append('     破线硬插或再改一次期，两样都是账烂掉的样子。')

    # ★★★★★2026-09-14 立·大审之口（⛔其所以要补：`大审.py` 之律自书「平均十章一回」，
    #   而**盘上没有一只手在那一日把它派出去**——`一章.js` 之十一段里没有它，
    #   於是它只在 `大审.py --账` 里报一句「该开一回大审」，而没有人在读那一句
    #   （**㊛ 之骨：册上写着「器会报」而器报了没人接**；
    #    ★其实：`大审_至第313章.md` 与 `_至第323章.md` 二册皆空模子，正是没人接的那两回）。
    #   ★故本器在「起」之前先问一句：这一章封了版，大审到期没有？到了就先印它。
    try:
        _大 = __import__('大审')
        _上 = (_大.诸册() or [(0, None)])[-1][0]
        if 末 - _上 >= getattr(_大, '每', 10):
            L.append('  【判】庭。第%d章已封版，而大审距上一回已 %d 章（限 %d）——**先开庭，再起下一章。**'
                     % (末, 末 - _上, getattr(_大, '每', 10)))
            L.append('  ⛔**一庭两用者尤不许拖**：收站之章之欠，正要这一庭当面裁。')
            L.append('  ── 下一条命令 ──')
            L.append("  Workflow({scriptPath:'工具/席/大审.js', args:{起:%d, 止:%d}})"
                     % (_上 + 1, 末))
            L.append('  ★其後再跑 python3 工具/大审.py --立 %d 造其册并当场填判；' % 末)
            L.append('  ⛔**只造册不填判者，`大审.py::空模子()` 当场滤掉它，不算一回大审**（㊧）。')
            L.append('  ★★办毕再跑一回本器，它自会印「起第%d章」。' % 下)
            return '庭', L
    except Exception:
        pass

    L.append('  【判】起。第%d章已封版且十一轮过——当起第%d章。' % (末, 下))
    L.append('  ── 下一条命令（⛔逐条照抄，序不许换）──')
    L.append('  python3 工具/心跳.py --跳 %d' % 下)
    if not 卡在(下):
        L.append('  python3 工具/第零轮开镜卡.py --立 %d   # 卡不在，先立卡（器名以磁盘为准）' % 下)
    L.append('  python3 工具/席法.py                      # 钥匙不绿，一个席也不许派')
    L.append('  python3 工具/起草庭.py %d' % 下)
    L.append('  Workflow({scriptPath:\'工具/席/一章.js\', args:{章:%d}})' % 下)
    return ('欠' if 欠 else '起'), L


def 报():
    判, L = 断()
    print('════ 自走 · 此刻该干哪一件 ════')
    for x in L:
        print(x)
    print('  ⛔本器只印一行命令。★照它跑，跑完再跑一回本器——**中间不许停下来问。**')
    return 判


def 自测():
    R = []
    判, L = 断(印=False)
    R.append(('①判得出一个字（候／跑／补／救／欠／起／庭）',
               判 in ('候', '跑', '补', '救', '欠', '起', '庭')))
    R.append(('②末一行是一条可照抄之命令', any(
        x.strip().startswith(('python3', 'Workflow')) for x in L)))
    R.append(('③末章取自正文档名，非版本目录（版本底下有第999章之试样）',
              末章() == max([_num(re.search(
                  r'第([零〇一二三四五六七八九十百千]+)章',
                  os.path.basename(f)).group(1))
                  for f in glob.glob(os.path.join(ROOT, '正文', '*.md'))
                  if re.search(r'第([零〇一二三四五六七八九十百千]+)章',
                               os.path.basename(f))])))
    # ④⛔心跳之限不写死在本器里（体检账 ㊖：判据里不许有「今天才成立」的数）
    src = io.open(os.path.abspath(__file__), encoding='utf-8').read()
    码 = src.split('def 自测')[0]          # ★只数自测以上之码，否则测在数它自己
    # ⑨★2026-09-14 补：大审之口须真在码里，且其判之名在①之表内
    #   ⛔其所以要验：`大审.py` 之律自书「平均十章一回」，而盘上从来没有一只手在那一日把它派出去
    #   （㊛ 之骨：册上写着「器会报」而器报了没人接；313／323 二册之空模子即其实）。
    R.append(('⑨大审之口在码里（其判作「庭」，并印席之命令）',
               '工具/席/大审.js' in 码 and "'庭', L" in 码))
    # ⑩★2026-09-16 立：**锁滞之判须真跑得出，且宁可候不可抢**
    #   ⛔其所以要验：335 之席办毕而锁未撤，本器照旧印「候」，白丢七分钟（若无人看要挂满 45 分钟）。
    #   ★其判之据係 `_任务流.json` 之末笔（略过存底流水），⛔**读不出即作「席还在」论**。
    R.append(('⑩锁滞·读不出即作席还在论（宁可候不可抢）',
               'def 锁滞' in 码 and 'return False                 # 读不出' in 码))
    R.append(('⑩之二·锁滞之判略过存底流水（存底不算一段）',
               "事.startswith('存底')" in 码 and "continue" in 码))
    _步 = [{'事': '9·案席毕'}, {'事': '9·封版席毕'}, {'事': '存底·第9章封版'}]
    R.append(('⑩之三·锁滞之判拿假料跑得出（封版席毕＝True，别章＝False，空表＝False）',
               判锁滞(_步, '9') is True and 判锁滞(_步, '8') is False
               and 判锁滞([], '9') is False
               and 判锁滞([{'事': '9·案席毕'}], '9') is False))
    R.append(('④心跳之限自 心跳.py 现取（本器内只余一处兜底）',
              "re.search(r'^限" in 码 and 码.count('45 * 60') == 1))
    # ⑤⛔读不出心跳者作「有人在跑」论（宁可候，不可抢）
    R.append(('⑤心跳读不出即作有人论（宁可候不可抢）', '作有人论' in 码))
    # ⑥⛔本器一个字也不写盘：无写口、无删口、无外跑
    R.append(('⑥本器不动盘（无写口 open(...,\'w\')／无 remove／无 shutil）',
              ".write(" not in 码 and "os.remove" not in 码
              and 'shutil' not in 码 and "', 'w'" not in 码))
    # ⑦⛔并证它真读得着盘：末章须 >0，且其回执之查真跑过一回
    R.append(('⑦真读得着盘（末章 >0 且回执之查跑得动）',
              末章() > 0 and isinstance(回执在(末章()), bool)))
    # ⑧⛔印「欠」时必带「谁的线／哪一章是哪一条线」那一问（体检账 ㊥）
    R.append(('⑧印「欠」时必带线之问（㊥·0913 两栽之治）', '谁的物、谁的线' in 码))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    报()
    sys.exit(0)
