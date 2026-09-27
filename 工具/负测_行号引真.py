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
import json
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

    # ⑧【圣经之 318 锚·真处 7406 → 0925 起真处 7409 → 0927 起真处 7496 → 0927 设定评审之裁起真处 7530】
    #    ★0927·改单#G0927-13（二、4 立律·死地抽寿元＋二、5 裁D1—D9 之表、人物档床上那人等，共 +34 行），
    #    318／317 两锚随之下移；awk NR==7530／NR==7529 亲印过。
    #    ★0927·圣经大修（改单#G0927-08／-10／-11）於其前插十一之补章数实图、二、4 有编号之律、事件链各卷一行、
    #    人物档案刘二东头等（共 +87 行），318／317 两锚随之下移；awk NR==7496／NR==7495 亲印过。
    #    ★0925·改单#G0925-02 往本圣经 ~619、~1702 两处各插注（共 +3 行），
    #    318／317 两锚随之下移三行；awk NR==7409／NR==7408 亲印过。锚是活号，改之非弱化。
    圣 = io.open(_在役[0], encoding='utf-8').read().split('\n')
    判('⑧', '圣经 7530 係 318 之定位行',
       '第 318 章必须从' in 圣[7529], True)
    判('⑨', '圣经 7529 係 317 之定位行（CHAR-317A 之锚）',
       '第 317 章必须从' in 圣[7528], True)

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


    # ⑬【缺口一·指着骨记行冒充白文行】⛔本形非空行，故第⑪格对它全盲。
    #    ★其实（0912·322 定位席当面逮出，而本闸一笔没逮着）：
    #      开镜卡与 320 骨记皆书那把铜「三寸」之原场係 `305:552`，
    #      **而 305 之 `【本章亮点】` 在第 542 行——552 落在它后头，是骨记，不是白文。**
    #    ★★故立此判：**凡近处称「白文」或「原场」而其行号越过该章亮点线者，即红。**
    def _亮点线(ch):
        w = _白文(ch)
        if not w:
            return None
        for i, l in enumerate(w, 1):
            if '【本章亮点】' in l:
                return i
        return None

    _lx = {}
    越 = []
    for p2 in _在役:
        if p2.endswith('.json'):
            continue
        for i, ln in enumerate(io.open(p2, encoding='utf-8').read().split('\n'), 1):
            for mm in re.finditer(r'`(\d{1,3}):(\d{1,4})`', ln):
                ch, no = int(mm.group(1)), int(mm.group(2))
                if ch not in _lx:
                    _lx[ch] = _亮点线(ch)
                L = _lx[ch]
                if not L or no <= L:
                    continue
                近 = ln[max(0, mm.start() - 40):mm.end() + 40]
                if ('白文' in 近 or '原场' in 近) and \
                        not any(x in 近 for x in ('旧号', '旧书', '陈号', '错引', '不实')):
                    越.append('%s:%d→%d:%d（亮点线在%d）'
                              % (os.path.basename(p2)[:8], i, ch, no, L))
    判('⑬', '在役档无「称白文而指到亮点线之后」之引', 越, [])

    # ⑭【缺口二·汉字形「白文第N行逐字『X』」】⛔第⑪格只认反引号之 `N:M`，看不见这一形。
    #    ★其实：`圣经:8011` 书「第 322 章必须从321之末那一拍（白文第381行…）」，
    #      **而 321 之真末句在第 389 行**（381 行实印的是另一句）——差八行，
    #      **而三章之席照着这个号往下接**。
    #    ★★本格之利在：这一形自带逐字原文，故不必只验空行，**可当场比对那一句在不在那一行**。
    #    ⛔**只验那一章已封版者**（其回执在）：**未封版之章行号还在动，验它是在跟自己较劲。**
    import glob as _g
    汉 = []
    _验数, _验章 = 0, set()
    # ⛔**心跳正指着的那一章不验**：**回执在 ≠ 已定稿**——
    #   322 之席已交回执，而救章席随即又把它掀开重掘，行号当场就动了。
    #   ★这与站账判三那一回同形：**「走完了没有」这件事，得问最新的那个凭据。**
    try:
        _跑中 = int(json.load(io.open(os.path.join(ROOT, '_心跳.json'),
                                      encoding='utf-8')).get('章') or 0)
    except Exception:
        _跑中 = 0
    # ⛔**章号取「从N之末」那一个，不取句首那一个**：
    #   `圣经:8011` 之形係「第 322 章必须从321之末那一拍（白文第381行…「…」）」
    #   ——**那个行号属 321，不属 322**；头一版正则抓走 322（未封版）遂整条跳过，
    #   **看着绿，其实一个字也没验着**（本日反复栽的那一样，第⑮格即为此立）。
    _pat = re.compile(
        r'第\s*(\d{1,4})\s*章[^\n]{0,40}?从\s*(\d{1,4})\s*之末'
        r'[^\n]{0,40}?白文第\s*(\d{1,4})\s*行[^「]{0,60}「([^」]{4,40})」')
    for p2 in _在役:
        if p2.endswith('.json'):
            continue
        for ln in io.open(p2, encoding='utf-8').read().split('\n'):
            for mm in _pat.finditer(ln):
                ch, no, 句 = (int(mm.group(2)), int(mm.group(3)), mm.group(4))
                if ch == _跑中:
                    continue
                if not _g.glob(os.path.join(ROOT, '设定',
                                            '回执_*_第%d章作业单.md' % ch)):
                    continue
                w = _白文(ch)
                if not w or no > len(w):
                    continue
                _验数 += 1
                _验章.add(ch)
                核 = 句.replace('*', '').strip()[:12]
                if 核 and 核 not in w[no - 1]:
                    汉.append('%d:%d 所称「%s…」不在其行'
                              % (ch, no, 核[:10]))
    判('⑭', '在役档「白文第N行逐字X」之引，逐处对得上', 汉, [])


    # ⑮【证第⑭格没有空转·⛔本日之骨】**一道看着绿的闸，先问它验着了几处。**
    #    ★其由：⑭之头一版正则抓错章号，**扫遍全仓验了零处而报绿**——
    #      ⛔**零处之绿与全对之绿，在印出来的字面上一模一样。**
    #    ★★故本格只问一句：**它到底验着了几处**；验着零处即判空转。
    判('⑮之一', '第⑭格确验着了处（非空转·验着 %d 处）' % _验数, _验数 >= 1, True)
    判('⑮之二', '其中确含 321 那一笔（圣经:8011 之接写锚）', 321 in _验章, True)

    print('════ 负测·行号引真 ════（守：所引之号与所书之句须对得上；案卷不验）')
    for x in 败:
        print('  ⛔ ' + x)
    print('  %s %d/%d %s' % ('✓' if not 败 else '⛔', 过, 过 + len(败),
                             '全通' if not 败 else '有败'))
    return 0 if not 败 else 2


if __name__ == '__main__':
    sys.exit(跑())
