#!/usr/bin/env python3
"""还账（1014 立·W26）——D6 六审 G 号落正文之执行器：料之汇、译单之验、窗、施。零 token。

为何立：欠账闸实清——D6 六审之裁（改单#G1008-01）定 G1—G72 为执行之令，七十号落了两号（G50、G52）；
  381—385 照 D6 之骨写成，与未改之前文当面相抵（383 粮房戏 × 261／263「她在粮房押了两年」等，W25 全段逻辑评逮）。
  G 号之文多已逐字裁定，执行是抄、不是写——抄错一字、抄错一行，比不抄还坏；故席只「译」（把一号译成结构化之单），
  落盘由本器：每一条单先逐字验过，验过才施。
单之式（JSON：{"组":…, "ops":[…], "缓":[…], "疑":[…]}；ops 依序施，同一行之後条见前条之果）：
  {"G":"G44", "据":"G44"|"S10"|"补表"|"六之四", "章":263, "行":189, "止":189, "式":"换"|"插"|"添"|"清",
   "原":"…", "新":"…", "撰":""}
  · 换：「原」在该行恰一见，换作「新」（新可空＝删片）。原、新取最短而在该行唯一之片。
  · 插：「原」为锚（恰一见、照留），「新」接其後。
  · 添：「新」接该行之末（「後添」：该行照留、其文接上——行号不移，照 G1014-01 之例）。
  · 清：行至止整行清空（行留、字去——行号不移）；「原」＝首行之头六字以上。
  · 撰：裁文只给「意」、未给字者，「新」由席照意撰，「撰」栏抄其意之原文；⛔撰而不标。
验（红即⛔施）：
  ① 章在、行在；式合；② 只动裁文点名之行：行⊆（G 号之行文 ∪ 据之行文）所引之行（「NNN:」立章、其後之数与 a—b 俱属之）；
     据「补表／六之四」者须有该 章:行 之行；六之四 之 263 行⛔承（G56）；
  ③ 原：换、插恰一见；清：首行以原起头；④ 新：非撰者须逐字在 G 号或据之行文里；
  ⑤ 护句（§四之四「⛔动之句」）：换、清 → 红，唯括注所许之行 → 黄；插、添 → 可（护句只添）；
  ⑥ 字顶：G 号之式「⛔多於N字」——所添之汉字逾 N → 红；连标点逾 N → 黄；⑦ 行数不变（由式所保）。
⛔限：只验「抄得对不对、动没动不该动的」；改得顺不顺、缝合不合，由缝审席看窗（--窗）。

用法：
  python3 工具/还账.py --料 丁                 # 汇一组之料 → 设定/_草/W26/料_丁.md（G 号、S 号、补表与六之四、护句、所引之行）
  python3 工具/还账.py --验 单1.json [单2…]    # 依序模拟；印红黄；有红 rc=1
  python3 工具/还账.py --窗 单1.json [单2…]    # 验之上，印每处改前改後之窗 → 设定/_草/W26/窗_<首单名>.md
  python3 工具/还账.py --施 单1.json [单2…]    # 无红方写盘；印每章几处；行数不变
  python3 工具/还账.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
主案 = os.path.join('设定', '剧情庭题', 'D6_床上那人_六审主案.md')
五审 = os.path.join('设定', '剧情庭题', 'D6_床上那人_五审主案.md')
草 = os.path.join('设定', '_草', 'W26')
组们 = {'甲': [88, 109, 115, 126, 161, 195, 199, 201],
        '乙': [217, 221, 232],
        '丙': [235, 239, 241, 244, 247, 249, 253, 255, 257, 259],
        '丁': [261, 263, 265, 267, 270],
        '戊': [272, 273, 275, 279, 281, 283, 286, 288, 290, 292, 296, 298, 300, 316, 318, 325, 329, 335]}
式们 = ('换', '插', '添', '清')


# ───────── 裁文 ─────────
def _段(行们, 起, 止):
    """行们 里自「起」字头之行至「止」字头之行（不含）。"""
    i = next((k for k, l in enumerate(行们) if l.startswith(起)), None)
    if i is None:
        return []
    j = next((k for k in range(i + 1, len(行们)) if 行们[k].startswith(止)), len(行们))
    return 行们[i:j]


def 读规(root=ROOT):
    """→ {'G': {号: 行文}, 'S': {号: 行文}, '表': {(章, 行): [(出处, 行文)]}, '六之四首': 文, '护': 文}"""
    六 = open(os.path.join(root, 主案), encoding='utf-8').read().split('\n')
    五 = open(os.path.join(root, 五审), encoding='utf-8').read().split('\n')
    规 = {'G': {}, 'S': {}, '表': {}, '六之四首': '', '护': ''}
    四 = _段(六, '## 四、', '## 五、')
    for l in 四:
        m = re.match(r'\|\s*(G\d+)\s*\|', l)
        if m:
            规['G'][m.group(1)] = l
        if l.startswith('- **⛔动之句**'):
            规['护'] = l
    for l in _段(四, '#### G56 补表', '### 四之三'):
        m = re.match(r'\|\s*(\d{2,3}):(\d+)\s*\|', l)
        if m:
            规['表'].setdefault((int(m.group(1)), int(m.group(2))), []).append(('补表', l))
    for l in _段(五, '### 六之一', '### 六之三'):
        m = re.match(r'\|\s*(S\d+[a-z]?)\s*\|', l)
        if m:
            规['S'][m.group(1)] = l
    六四 = _段(五, '### 六之四', '### 六之五')
    规['六之四首'] = '\n'.join(l for l in 六四 if not l.startswith('|'))
    for l in 六四:
        m = re.match(r'\|\s*(\d{2,3}):(\d+)\s*\|', l)
        if m:
            规['表'].setdefault((int(m.group(1)), int(m.group(2))), []).append(('六之四', l))
    return 规


def 令文(行文):
    """表行 → 只取「处、式、原、改」（G 号）或「章:行、式、改前、改後」（S 号）之栏；「由」栏（理由里引的他处）⛔作可改之行。"""
    c = [x.strip() for x in (行文 or '').strip().strip('|').split('|')]
    if len(c) > 2:                                    # 式栏之括注是由、是「照留」之注（G29「381—401 照留」、G68「抵 201:579」）——⛔作可改
        c[2] = re.sub(r'（[^（）]*）|\([^()]*\)', '', c[2])
    if len(c) == 4:                                   # G65—G72 三栏之式：号｜处｜式｜原→改（其後「｜删此号」係由）
        c[3] = re.split(r'｜\s*删此号', c[3])[0]
        return ' | '.join(c[1:])
    return ' | '.join(c[1:5])


def 首章(文):
    m = re.search(r'(?<![\dA-Za-z])(\d{2,3})(?=[:：（(]|\s|$)', 文 or '')
    return int(m.group(1)) if m else None


def 引(文, 默章=None):
    """行文 → {章: {行}}：剥「」中之字；「NNN:」立章，其後之数（a、a—b）俱属之；未立章之数属默章。"""
    s = re.sub(r'「[^」]*」', '', 文 or '')
    出, 今 = {}, 默章
    for m in re.finditer(r'(?<![\dA-Za-z§])(\d{1,4})(?:\s*[—–\-~～]\s*(\d{1,4}))?(\s*[:：])?', s):
        a, b, 冒 = m.group(1), m.group(2), m.group(3)
        if 冒 and not b:
            今 = int(a)
            continue
        if 今 is None:
            continue
        a = int(a); b = int(b) if b else a
        if b < a or b - a > 400:
            continue
        出.setdefault(今, set()).update(range(a, b + 1))
    return 出


def 护们(护文):
    """§四之四「⛔动之句」→ ({章: {行}} 护, {章: {行}} 括注所许, {章} 全章护)"""
    护, 许, 全 = {}, {}, set()
    文 = 护文.split('**⛔动之句**', 1)[-1]
    尾 = re.search(r'（(\d{2,3}:\d+[^）]*)）\s*$', 文.strip())      # 末之括注：「（201:13 照二审⑤……；270:357 照 S39……）」→ 所许
    if 尾:
        for 章, 行们 in 引(尾.group(1)).items():
            许.setdefault(章, set()).update(行们)
        文 = 文[:尾.start()]
    for 段 in re.split(r'[；;]', 文):
        m = re.search(r'(\d{2,3})\s*全章', 段)
        if m:
            全.add(int(m.group(1)))
            continue
        m = re.search(r'(\d{2,3})\s*[:：]', 段)
        if not m:
            continue
        章 = int(m.group(1))
        for 括 in re.findall(r'（([^）]*)）', 段):
            for n in re.findall(r'(?<![\dA-Za-z])(\d{1,4})(?![\d—–\-])', 括):
                许.setdefault(章, set()).add(int(n))
        净 = re.sub(r'（[^）]*）', '', 段)
        for 章2, 行们 in 引(净).items():
            护.setdefault(章2, set()).update(行们)
    return 护, 许, 全


def 字顶(式文):
    m = re.search(r'⛔(?:合)?多於([〇零一二两三四五六七八九十百]+)字', 式文 or '')
    if not m:
        return None
    s, 数 = m.group(1), {'〇': 0, '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    总 = 节 = 0
    for ch in s:
        if ch == '百':
            总 += (节 or 1) * 100; 节 = 0
        elif ch == '十':
            总 += (节 or 1) * 10; 节 = 0
        else:
            节 = 数[ch]
    return 总 + 节


def 汉(s):
    return len(re.findall(r'[一-鿿]', s or ''))


# ───────── 正文 ─────────
def 读章(n, root=ROOT):
    import 章料
    f = 章料.章档(n, root)
    return (f, open(f, encoding='utf-8').read().split('\n')) if f else (None, None)


# ───────── 验 ─────────
def 验(ops们, 规, 取章=读章):
    """ops们：[(单名, op)…] 依序 → (红[], 黄[], 文{章: (档, 旧行们, 新行们)}, 计{})"""
    护, 许, 全护 = 护们(规['护'])
    红, 黄, 文, 计, 添字 = [], [], {}, {}, {}
    for 单名, o in ops们:
        标 = '%s·%s %s:%s' % (单名, o.get('G', '?'), o.get('章'), o.get('行'))
        def R(x): 红.append('%s｜%s' % (标, x))
        def Y(x): 黄.append('%s｜%s' % (标, x))
        G, 据, 式 = o.get('G') or '', o.get('据') or o.get('G') or '', o.get('式')
        原, 新, 撰 = o.get('原') or '', o.get('新') or '', (o.get('撰') or '').strip()
        try:
            章, 行 = int(o.get('章')), int(o.get('行'))
            止 = int(o.get('止') or 行)
        except Exception:
            R('章、行非数'); continue
        if 式 not in 式们:
            R('式「%s」不在 换／插／添／清' % 式); continue
        if G not in 规['G']:
            R('G 号「%s」不在主案 §四' % G); continue
        if 章 not in 文:
            f, ls = 取章(章)
            if not ls:
                R('第%d章正文不在' % 章); continue
            文[章] = (f, list(ls), list(ls))
        f, 旧, 今 = 文[章]
        if not (1 <= 行 <= 止 <= len(今)):
            R('行越界（全章 %d 行）' % len(今)); continue
        # ② 只动裁文点名之行
        G文 = 规['G'][G]
        处 = G文.split('|')[2] if G文.count('|') > 2 else ''
        准 = 引(令文(G文), 首章(处)).get(章, set())
        if 据 in ('补表', '六之四'):
            行文们 = [文2 for 出, 文2 in 规['表'].get((章, 行), []) if 出 == 据]
            if not 行文们:
                R('据「%s」而该表无 %d:%d 之行' % (据, 章, 行)); continue
            if 据 == '六之四' and 章 == 263:
                R('六之四之 263 行⛔承（G56：263 照 G44）'); continue
            据文 = '\n'.join(行文们)
            准 = 准 | {行}
        elif 据 == G:
            据文 = G文
        elif 据 == '缝':                     # 缝审之修：G 号之改留下之缝（悬指、断句）——可动邻行，一律黄、须有由；护句照守
            if not (o.get('由') or '').strip():
                R('据「缝」须有由'); continue
            据文 = ''
            准 = 准 | set(range(行, 止 + 1))
            Y('缝（%s）：%s' % ((o.get('由') or '')[:40], 新[:40] or '删「%s」' % 原[:20]))
        elif 据 in 规['S']:
            据文 = 规['S'][据]
            if 据 not in G文 and G != 'G56':
                Y('据 %s 而 %s 之行文未提此号' % (据, G))
            准 = 准 | 引(令文(据文), 首章(据文.split('|')[2] if 据文.count('|') > 2 else '')).get(章, set())
        else:
            R('据「%s」不认（G 号、S 号、补表、六之四）' % 据); continue
        外 = sorted(set(range(行, 止 + 1)) - 准)
        if 外:
            R('动了裁文未点名之行 %s' % (外[:6],)); continue
        # ⑤ 护句
        if 式 in ('换', '清'):
            护中 = [k for k in range(行, 止 + 1) if 章 in 全护 or k in 护.get(章, set())]
            if 护中:
                if all(k in 许.get(章, set()) for k in 护中):
                    Y('护句 %s 括注所许，改之' % 护中[:6])
                else:
                    R('护句 %s ⛔换、⛔清（护句只添）' % 护中[:6]); continue
        # ③ 原
        l = 今[行 - 1]
        if 式 in ('换', '插'):
            if not 原:
                R('%s 无原' % 式); continue
            n = l.count(原)
            if n != 1:
                R('原「%s」在该行 %d 见（须恰一）' % (原[:24], n)); continue
        if 式 == '清':
            if len(原) < 6 and l.strip():
                R('清之原须首行之头六字以上'); continue
            if l.strip() and not l.startswith(原):
                R('清之原「%s」非首行之头' % 原[:16]); continue
            if 止 - 行 > 200:
                R('一条清逾二百行'); continue
        if 式 == '添' and not l.strip():
            R('添於空行（後添须接在有字之行末）'); continue
        if 式 in ('插', '添') and not 新:
            R('%s 无新' % 式); continue
        # ④ 新之出处
        if 新:
            if 撰:
                Y('撰（照意「%s」）：「%s」' % (撰[:30], 新[:40]))
            elif 据 == '缝':
                R('缝之新字须标「撰」'); continue
            elif 新 not in 据文 and 新 not in G文:
                R('新「%s」不在 %s 或 %s 之行文（照意撰者须标「撰」）' % (新[:30], 据, G)); continue
        # 施於模拟
        if 式 == '换':
            今[行 - 1] = l.replace(原, 新, 1); 增 = 汉(新) - 汉(原); 增全 = len(新) - len(原)
        elif 式 == '插':
            今[行 - 1] = l.replace(原, 原 + 新, 1); 增 = 汉(新); 增全 = len(新)
        elif 式 == '添':
            今[行 - 1] = l + 新; 增 = 汉(新); 增全 = len(新)
        else:
            for k in range(行, 止 + 1):
                今[k - 1] = ''
            增 = 增全 = 0
        a = 添字.setdefault(G, [0, 0]); a[0] += max(增, 0); a[1] += max(增全, 0)
        计[式] = 计.get(式, 0) + 1
        if 撰:
            计['撰'] = 计.get('撰', 0) + 1
    # ⑥ 字顶
    for G, (h, t) in 添字.items():
        顶 = 字顶(规['G'][G].split('|')[3] if 规['G'][G].count('|') > 3 else '')
        if 顶 is None:
            continue
        if h > 顶:
            红.append('%s｜所添汉字 %d 逾顶 %d' % (G, h, 顶))
        elif t > 顶:
            黄.append('%s｜所添连标点 %d 逾顶 %d（汉字 %d 未逾）' % (G, t, 顶, h))
    for 章, (f, 旧, 今) in 文.items():
        if len(旧) != len(今):
            红.append('第%d章行数变了（%d→%d）' % (章, len(旧), len(今)))
    return 红, 黄, 文, 计


def 读单们(路们):
    出 = []
    for p in 路们:
        d = json.load(open(p, encoding='utf-8'))
        名 = os.path.splitext(os.path.basename(p))[0]
        出 += [(名, o) for o in (d.get('ops') if isinstance(d, dict) else d)]
    return 出


def 窗(文, 宽=2):
    """→ markdown：每章每处改前改後之窗（清之长段只印首末）。"""
    出 = []
    for 章 in sorted(文):
        f, 旧, 今 = 文[章]
        变 = [k for k in range(len(旧)) if 旧[k] != 今[k]]
        if not 变:
            continue
        出.append('## 第%d章（%s）' % (章, os.path.basename(f)))
        块, 起 = [], 变[0]
        前 = 变[0]
        for k in 变[1:] + [None]:
            if k is not None and k - 前 <= 2 * 宽 + 1:
                前 = k; continue
            块.append((起, 前)); 起 = 前 = k
        for a, b in 块:
            lo, hi = max(0, a - 宽), min(len(旧), b + 宽 + 1)
            出.append('\n### %d:%d—%d' % (章, a + 1, b + 1))
            for 名, 版 in (('前', 旧), ('後', 今)):
                出.append('〔%s〕' % 名)
                清段 = [k for k in range(lo, hi) if 旧[k].strip() and not 今[k].strip()]
                for k in range(lo, hi):
                    if 名 == '後' and k in 清段 and len(清段) > 6 and k not in (清段[0], 清段[-1]):
                        if k == 清段[1]:
                            出.append('    …（清 %d 行）…' % (len(清段) - 2))
                        continue
                    if 名 == '前' and len(清段) > 6 and k in 清段 and k not in 清段[:2] + 清段[-2:]:
                        if k == 清段[2]:
                            出.append('    …（中 %d 行将清）…' % (len(清段) - 4))
                        continue
                    if 版[k].strip() or 旧[k] != 今[k]:
                        出.append('%s %d｜%s' % ('●' if 旧[k] != 今[k] else ' ', k + 1, 版[k] if 版[k].strip() else '（空）'))
    return '\n'.join(出)


# ───────── 料 ─────────
def 料(组, root=ROOT, 规=None):
    规 = 规 or 读规(root)
    章们 = set(组们[组])
    主 = [(g, l) for g, l in 规['G'].items() if g != 'G56' and 首章(l.split('|')[2]) in 章们]
    主.sort(key=lambda x: int(x[0][1:]))
    S号 = sorted({s for _, l in 主 for s in re.findall(r'(?<![A-Za-z])S\d+[a-z]?', l) if s in 规['S']}, key=lambda s: int(re.sub(r'\D', '', s)))
    表 = sorted((k, 出, l) for k, v in 规['表'].items() if k[0] in 章们 for 出, l in v)
    引行 = {}
    for g, l in 主:
        for 章, 行们 in 引(令文(l), 首章(l.split('|')[2])).items():
            引行.setdefault(章, set()).update(行们)
    for s in S号:
        l = 规['S'][s]
        for 章, 行们 in 引(令文(l), 首章(l.split('|')[2])).items():
            引行.setdefault(章, set()).update(行们)
    for (章, 行), _, _ in 表:
        引行.setdefault(章, set()).add(行)
    护, 许, 全 = 护们(规['护'])
    出 = ['# 还账之料·%s 组（第 %s 章）' % (组, '、'.join(map(str, sorted(章们)))),
          '', '> 零 token 所汇（工具/还账.py --料）。裁文逐字抄自 %s（G 号、补表）与 %s（S 号、六之四）；正文之行照 `正文/` 物理行亲印。' % (主案, 五审),
          '', '## 一、本组之 G 号（主案 §四；G56 另见第三节）', '']
    出 += [l for _, l in 主] or ['（无）']
    出 += ['', '## 二、所照之 S 号（五审 §六之一、之二；「改後之意」只给意者，照意撰、单里标「撰」）', '']
    出 += [规['S'][s] for s in S号] or ['（无）']
    出 += ['', '## 三、G56 数之正（本组诸章之行；凡与 G 号同行者以 G 号为准；263 之六之四行⛔承）', '', 规['G']['G56'], '', '〔六之四之首〕', 规['六之四首'][:3000], '']
    出 += ['%s｜%s' % (出处, l) for _, 出处, l in 表] or ['（无）']
    出 += ['', '## 四、护句（换、清⛔；添、插可）', '']
    for 章 in sorted(set(引行) | 章们):
        if 章 in 全:
            出.append('- %d：全章' % 章)
        elif 护.get(章):
            出.append('- %d：%s%s' % (章, _区(sorted(护[章])), ('（括注许：%s）' % _区(sorted(许[章]))) if 许.get(章) else ''))
    出 += ['', '## 五、所引之行（物理行；前後各一行；长段只印首末）', '']
    for 章 in sorted(引行):
        f, ls = 读章(章, root)
        if not ls:
            出.append('### 第%d章：正文不在' % 章); continue
        出.append('### 第%d章（%s，共 %d 行）' % (章, os.path.basename(f), len(ls)))
        要 = sorted(k for k in 引行[章] if 1 <= k <= len(ls))
        印 = set()
        for k in 要:
            印.update(range(max(1, k - 1), min(len(ls), k + 1) + 1))
        前 = None
        for k in sorted(印):
            if not ls[k - 1].strip():
                continue
            if 前 is not None and k - 前 > 2:
                出.append('…')
            出.append('%d｜%s' % (k, ls[k - 1]))
            前 = k
        出.append('')
    return '\n'.join(出)


def _区(xs):
    出, i = [], 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[j + 1] == xs[j] + 1:
            j += 1
        出.append(str(xs[i]) if i == j else '%d—%d' % (xs[i], xs[j])); i = j + 1
    return '、'.join(出)


# ───────── 自测 ─────────
def 自测():
    ok = 共 = 0
    规 = {'G': {'G1': '| G1 | 88:3 後 | 後添（⛔多於十字） | 88:3「甲乙。」 | 「丙丁戊。」 | 由 |',
                'G2': '| G2 | 89（漂） | 此段改为 | 5「旧旧旧旧旧旧。」；7—9 删 | 5「新新。」 | 由 |',
                'G3': '| G3 | 90:2 | 照五审 S9 | 90:2「原句。」 | 照 S9 | 由 |',
                'G4': '| G4 | 91:1 | 後添（⛔多於二字） | 91:1「一。」 | 「多多多。」 | 由 |',
                'G56': '| G56 | 数之正 | 照表 | 见补表 | 由 |'},
          'S': {'S9': '| S9 | 90:2 | 改 | 「原句」 | 「意：改作新意」 | 由 |'},
          '表': {(89, 5): [('补表', '| 89:5 | 「旧旧」 | 甲 | 「新」 |')]},
          '六之四首': '', '护': '- **⛔动之句**（本案）：88:1—2；89:9（只正其数：9 乙）；90 全章。'}
    假 = {88: ['护护', '', '甲乙。', ''], 89: ['a', '', '', '', '旧旧旧旧旧旧。', '', 'x', 'y', 'z'], 90: ['', '原句。'], 91: ['一。']}
    取 = lambda n: ('假%d.md' % n, 假[n]) if n in 假 else (None, None)
    def T(ops, 应红):
        nonlocal ok, 共
        红, 黄, 文, 计 = 验([('单', o) for o in ops], 规, 取)
        共 += 1; ok += (bool(红) == 应红)
        return 红, 黄, 文
    _, _, 文 = T([{'G': 'G1', '章': 88, '行': 3, '式': '添', '新': '丙丁戊。'}], False)
    共 += 1; ok += 文[88][2][2] == '甲乙。丙丁戊。' and len(文[88][2]) == 4                 # 添：行末接上，行数不变
    T([{'G': 'G1', '章': 88, '行': 3, '式': '添', '新': '编的。'}], True)                 # 新不在裁文 → 红
    T([{'G': 'G1', '章': 88, '行': 3, '式': '添', '新': '编的。', '撰': '意'}], False)    # 标撰 → 黄、不红
    T([{'G': 'G1', '章': 88, '行': 2, '式': '换', '原': 'x', '新': '丙丁戊。'}], True)    # 动了裁文未点名之行（88:2）
    T([{'G': 'G2', '章': 89, '行': 7, '止': 9, '式': '清', '原': 'x'}], True)             # 原不足六字 → 红
    _, 黄, 文 = T([{'G': 'G2', '章': 89, '行': 5, '式': '换', '原': '旧旧旧旧旧旧。', '新': '新新。'}], False)
    T([{'G': 'G2', '章': 89, '行': 5, '式': '换', '原': '旧旧', '新': '新新。'}], True)     # 原在该行三见 → 红
    T([{'G': 'G2', '章': 89, '行': 9, '式': '换', '原': 'z', '新': '新新。'}], False)       # 89:9 护而括注许 → 黄
    T([{'G': 'G3', '据': 'S9', '章': 90, '行': 2, '式': '换', '原': '原句。', '新': '改作新意'}], True)   # 90 全章护 → 红
    T([{'G': 'G3', '据': 'S9', '章': 90, '行': 2, '式': '插', '原': '原句。', '新': '改作新意'}], False)  # 护句只添 → 可
    T([{'G': 'G4', '章': 91, '行': 1, '式': '添', '新': '多多多。'}], True)               # 汉字 3 逾顶 2 → 红
    T([{'G': 'G56', '据': '补表', '章': 89, '行': 5, '式': '换', '原': '旧旧旧旧旧旧', '新': '新'}], False)
    T([{'G': 'G56', '据': '补表', '章': 89, '行': 6, '式': '换', '原': 'x', '新': '新'}], True)   # 补表无 89:6 → 红
    T([{'G': 'G1', '据': '缝', '章': 88, '行': 1, '式': '换', '原': '护护', '新': '甲', '撰': '缝', '由': '悬指'}], True)   # 缝亦守护句
    T([{'G': 'G2', '据': '缝', '章': 89, '行': 1, '式': '换', '原': 'a', '新': '乙', '撰': '缝', '由': '悬指'}], False)  # 缝可动邻行
    T([{'G': 'G2', '据': '缝', '章': 89, '行': 1, '式': '换', '原': 'a', '新': '乙', '由': '悬指'}], True)               # 缝之新字须标撰
    共 += 1; ok += 引(令文('| G9 | 88:3 | 改 | 「甲」 | 「乙」 | 与 201:29 相抵 |'), 88) == {88: {3}}   # 由栏之 201:29 ⛔作可改
    共 += 1; ok += 引(令文('| G29 | 235:325—329 | 此段改为（照留 381—401） | 「甲」 | 「乙」 | 由 |'), 235) == {235: {325, 326, 327, 328, 329}}
    共 += 1; ok += 令文('| G65 | 261:509 | 改 | 509「甲」→「乙」｜删此号，书少：77:1 |') == '261:509 | 改 | 509「甲」→「乙」'
    共 += 1; ok += 引('| G7 | 195:715；199:175、347—349 | 改 | 「12:3」 |') == {195: {715}, 199: {175, 347, 348, 349}}
    共 += 1; ok += 字顶('後添（⛔多於一百三十五字）') == 135 and 字顶('改（⛔合多於一百字）') == 100 and 字顶('改') is None
    护, 许, 全 = 护们('- **⛔动之句**（本案之所以立）：201:17、155；263:77—141（护句）、457—473；272 全章；283:5—37（只正其数：13 乙、33 照 S38）。（201:13 照二审⑤只添半句，G62。）')
    共 += 1; ok += 护[201] == {17, 155} and 140 in 护[263] and 460 in 护[263] and 272 in 全 and 许[283] == {13, 33} and 13 in 许[201]
    print('还账·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a[:1] == ['--料'] and len(a) == 2:
        os.makedirs(os.path.join(ROOT, 草), exist_ok=True)
        p = os.path.join(ROOT, 草, '料_%s.md' % a[1])
        t = 料(a[1])
        open(p, 'w', encoding='utf-8').write(t)
        print('还账·料 %s → %s（%d 字）' % (a[1], os.path.relpath(p, ROOT), len(t)))
        sys.exit(0)
    if a[:1] in (['--验'], ['--窗'], ['--施']) and len(a) >= 2:
        规 = 读规()
        红, 黄, 文, 计 = 验(读单们(a[1:]), 规)
        for x in 红:
            print('  ⛔', x)
        for x in 黄:
            print('  ⚠', x)
        动 = {章: sum(1 for i in range(len(v[1])) if v[1][i] != v[2][i]) for 章, v in 文.items()}
        import 欠账闸
        def 模白(n):
            if n in 文:
                t2 = '\n'.join(文[n][2]); i = t2.find('【本章亮点】')
                return t2[:i] if i >= 0 else t2
            return 欠账闸.白文(n)
        所涉 = sorted({o.get('G') for _, o in 读单们(a[1:]) if o.get('G') and o.get('G') != 'G56'}, key=lambda g: int(g[1:]))
        判们 = {}
        for 号, 处, 式, 原, 改, 由 in 欠账闸.行们(open(os.path.join(ROOT, 主案), encoding='utf-8').read()):
            if 号 in 所涉:
                判们.setdefault(欠账闸.判一(处, 式, 原, 改, 模白)[0], []).append(号)
        print('欠账闸（模拟施後·单所涉之号）：%s' % '｜'.join('%s %d%s' % (k, len(v), '' if k == '已执行' else '（%s）' % '、'.join(v)) for k, v in 判们.items()))
        print('还账·验：%s｜动 %d 章 %d 行｜红 %d｜黄 %d' % ('、'.join('%s %d' % kv for kv in 计.items()) or '无单', sum(1 for v in 动.values() if v), sum(动.values()), len(红), len(黄)))
        if a[0] == '--窗':
            os.makedirs(os.path.join(ROOT, 草), exist_ok=True)
            p = os.path.join(ROOT, 草, '窗_%s.md' % os.path.splitext(os.path.basename(a[1]))[0])
            open(p, 'w', encoding='utf-8').write('# 还账之窗（改前／改後；●＝变）\n\n' + 窗(文))
            print('还账·窗 → %s' % os.path.relpath(p, ROOT))
        if a[0] == '--施':
            if 红:
                print('还账·施：有红，⛔施'); sys.exit(1)
            for 章, (f, 旧, 今) in sorted(文.items()):
                if 旧 != 今:
                    open(f, 'w', encoding='utf-8').write('\n'.join(今))
                    print('  施 第%d章 %d 行' % (章, 动[章]))
        sys.exit(1 if 红 else 0)
    print(__doc__)
    sys.exit(2)
