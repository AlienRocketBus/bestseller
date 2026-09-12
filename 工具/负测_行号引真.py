# -*- coding: utf-8 -*-
"""负测·行号引真（2026-09-12 立·四笔行号错引压了三章方立此条）。

★所守者一句：**在役之指路档里所引的白文行号，须与其所书之句相符**。
★★其头一格拿 316 之真局回灌：**盘上曾以 `316:438` 指「门槛上那只勺」（真处 420）、
　以 `316:356` 指「八十四页写满了」（真处 332）**——⛔**两号皆错，而三章之席照着往下传。**
★★★其根不是手滑：**引号之人当时没有 `awk` 亲印一遍**；
　**故本测所验者即「亲印」这一件事本身**——号与句对得上，才算引过。
⛔**本测只验在役之指路档**（圣经·施工表·到期账·开镜卡）；
　**轮记与回执係案卷，存其当时所见之原样，一字不验、一字不改。**
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
正文 = os.path.join(ROOT, '正文')

_在役 = [
    os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'),
    os.path.join(ROOT, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md'),
    os.path.join(ROOT, '设定', '到期账.json'),
]

# 本次四笔之旧号：⛔在役之档里一处也不许再有（括注里那一份除外，其形作「旧书N」）
_旧 = [('316', '438'), ('316', '356')]


def _白文(n):
    """取第 n 章之正文档，逐行。"""
    for f in os.listdir(正文):
        if not f.endswith('.md'):
            continue
        p = os.path.join(正文, f)
        head = io.open(p, encoding='utf-8').readline()
        if re.search(r'第\s*%d\s*章' % n, head) or _号(f) == n:
            return io.open(p, encoding='utf-8').read().split('\n')
    return None


_汉 = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
       '六': 6, '七': 7, '八': 8, '九': 9}


def _号(名):
    m = re.search(r'第([零一二三四五六七八九十百千]+)章', 名)
    if not m:
        return None
    s, v, cur = m.group(1), 0, 0
    for ch in s:
        if ch in _汉:
            cur = _汉[ch]
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

    白316 = _白文(316)
    判('①', '316 之白文取得着', bool(白316), True)

    # ②③【头一格·真局回灌】真处之句，逐字对得上
    判('②', "316:420 係「门槛上那只勺…」",
       白316 and '门槛上那只勺' in 白316[419], True)
    判('③', "316:332 係「八十四页写满了…」",
       白316 and '八十四页写满了' in 白316[331], True)

    # ④⑤【其害】旧号所指者，与所称之句全不相干
    判('④', "旧号 316:438 不是那只勺（证其错）",
       白316 and '门槛上那只勺' not in 白316[437], True)
    判('⑤', "旧号 316:356 不是那一页（证其错）",
       白316 and '八十四页写满了' not in 白316[355], True)

    # ⑥⑦【在役之档不许再带旧号】括注之「旧书N」不算，其形已明说是陈号
    for p in _在役:
        tx = io.open(p, encoding='utf-8').read()
        脏 = []
        for ch, ln in _旧:
            for m in re.finditer(r'%s[:：]%s' % (ch, ln), tx):
                前 = tx[max(0, m.start() - 12):m.start()]
                if '旧书' in 前 or '旧号' in 前 or '陈号' in 前:
                    continue
                脏.append('%s:%s' % (ch, ln))
        判('⑥·%s' % os.path.basename(p)[:8], '在役之档无未注之旧号',
           脏, [])

    # ⑧【圣经之 318 锚·真处 7406】
    圣 = io.open(_在役[0], encoding='utf-8').read().split('\n')
    判('⑧', '圣经 7406 係 318 之定位行',
       '第 318 章必须从' in 圣[7405], True)
    判('⑨', '圣经 7405 係 317 之定位行（CHAR-317A 之锚）',
       '第 317 章必须从' in 圣[7404], True)

    # ⑩【不许连坐】此律不许把「案卷存原样」这一条写没了：
    #    318 之轮记仍须留着它当时所见的那四个错号，一个不许抹
    lj = os.path.join(ROOT, '版本', '第318章', '_轮记.md')
    tx = io.open(lj, encoding='utf-8').read() if os.path.exists(lj) else ''
    判('⑩', '318 轮记仍存其当时所见之旧号（案卷不改）',
       ('7372' in tx and '316:356' in tx), True)


    # ⑪【一般之格·在役档全扫】凡引白文行而指着空行者，近处须有一句明说它是陈号
    #    ⛔本格之界：**只认空行**（空行必非其所称之句），不认「句对不对」
    #      ——那一样要逐句比，据不够，不在本格之内。
    #    ⛔**只认反引号包着的 `N:M`**——那是全仓引白文行的通行写法。
    #      **其由是本格头一跑自栽**：不带反引号地扫，逮出五处假红，
    #      **一处不是行引**——`0911 05:54` 是时刻｜`COLD-240:232` 是冷轮号｜
    #      `限287：285与286连着两章` 是全角冒号把「限287」与「285与286」切开了｜
    #      `315:2,491` 是净重。⛔**「章:行」这个形，在册子里被别的东西占着。**
    白名 = ('旧号', '旧书', '陈号', '空拍', '真处', '错引', '不实', '偏五')
    虚 = []
    _w = {}
    for p2 in _在役:
        if p2.endswith('.json'):
            continue
        for i, ln in enumerate(io.open(p2, encoding='utf-8').read().split('\n'), 1):
            for mm in re.finditer(r'`(\d{1,3}):(\d{1,4})`', ln):
                ch, no = int(mm.group(1)), int(mm.group(2))
                if not (1 <= ch <= 400):
                    continue
                if ch not in _w:
                    _w[ch] = _白文(ch)
                w = _w[ch]
                if not w or no > len(w) or w[no - 1].strip():
                    continue
                近 = ln[max(0, mm.start() - 60):mm.end() + 60]
                if any(x in 近 for x in 白名):
                    continue
                虚.append('%s:%d→%d:%d' % (os.path.basename(p2)[:8], i, ch, no))
    判('⑪', '在役档无「指着空行而未注其為陈号」之引', 虚, [])


    # ⑫【证其有牙·⛔否则收窄之後它就只是一句好听的话】
    #    取施工表里那一行真文（其内确有 `315:309` 之陈号），**把白名之注剥掉**，
    #    ⛔**它须当场逮得出**——逮不出，即是第⑪格被我收成了一句空话。
    st = io.open(_在役[1], encoding='utf-8').read().split('\n')
    真行 = [x for x in st if '`315:309`' in x]
    判('⑫之一', '施工表里确有 `315:309` 之陈号（本格之料在）', bool(真行), True)
    if 真行:
        剥 = 真行[0]
        for x in 白名:
            剥 = 剥.replace(x, '　')
        w315 = _w.get(315) or _白文(315)
        中 = [m2.group(0) for m2 in re.finditer(r'`(\d{1,3}):(\d{1,4})`', 剥)
              if int(m2.group(1)) == 315 and int(m2.group(2)) <= len(w315)
              and not w315[int(m2.group(2)) - 1].strip()]
        判('⑫之二', '注一剥，第⑪格当场逮得出（得 %d 处）' % len(中),
           len(中) >= 1, True)
        判('⑫之三', '注不剥则放过（白名之界未被扫没）',
           any(x in 真行[0] for x in 白名), True)

    print('════ 负测·行号引真 ════（守：所引之号与所书之句须对得上；案卷不验）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
