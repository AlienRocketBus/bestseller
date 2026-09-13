# -*- coding: utf-8 -*-
"""FS 沉默闸（2026-09-01 立·全书审计第二层 2-3／制度补法 M9）

★立此闸之由（今日器印）：
　·canon事实库.foreshadows 共 18 根，未销 13 根；其限最迟 150、最早 75——
　　★★以第 287 章计，**逾期 137 至 212 章**；
　·而小说检察官每章跑一次 foreshadow_report，把它们逐根印出来；
　·★★★**含 FS 编号之回执共 32 份，最末一份是第 99 章**——
　　★★★★**188 章问了 188 遍，一次没人答。**
★一道天天在印而从来没人回话的报，等於不存在。

【其律】凡本章之回执全文不含某根逾期之 FS 编号者，判红。
【怎么销红】**不必兑付，只须回话**——在回执里写一句即可：
　　「FS08：判改期至E5」／「FS03：已於第110章兑（其身在…），今补销」／「FS13：判废，其由…」
　★**它逼的是回话，不是逼数相等**（三本账粒度不同：到期账数十几章之微钩、canon 数十八根中账、
　　圣经十五笔数全书大账；「三账同屏、任二数不合即⛔」那种闸开机即死，故不立）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
清 = ('paid', 'done', 'closed', '已销', '已兑', '废')


def 未销():
    d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
    out = []
    for x in d.get('foreshadows', []):
        if str(x.get('status', '')).lower() in 清:
            continue
        # ★★★★★2026-09-01 补·并记「改过几回期」。
        #   ★其由：今日十三根裁毕，六根判已兑补销、七根判改期——**而闸随即转绿，是靠改期绿的**；
        #   ★★一根钩子若靠反复改期永不兑现，这道闸就成了一张会自己签字的欠条 ⛔；
        #   ★★★故凡改期者其 reschedule_note 逐次累加，此处数之并印：
        #     ★★★★**改期逾二回者，无论逾没逾期，一律入报**——由人当场裁它还算不算一根活钩子。
        # ★数其回数只认一个记号「（原限」——立此闸之日以二词并数，一回改期数成了二回 ⛔
        _rn = str(x.get('reschedule_note', ''))
        # ★2026-09-05·机制总审（八路·跨章连贯审第6条）：只数「（原限」一个记号——FS03 实改五回印 2 回；今取「（原限」「改期」「改至」三记号之最大者。
        n = max(_rn.count('（原限'), _rn.count('改期'), _rn.count('改至'))
        out.append({'id': x.get('id'), 'due': x.get('due'),
                    'desc': x.get('desc', ''), '改期': max(n, 1 if x.get('reschedule_note') else 0)})
    return out


def _末章():
    ns = []
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', os.path.basename(f))
        if not m:
            continue
        CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
              '六': 6, '七': 7, '八': 8, '九': 9}
        s, tot, cur = m.group(1), 0, 0
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
        ns.append(tot + cur)
    return max(ns) if ns else 0


def 回执之答(n):
    """★取第 n 章之回执全文；返回其中出现之 FS 编号集。"""
    for p in sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*第%d章*.md' % n))):
        t = io.open(p, encoding='utf-8').read()
        return os.path.basename(p), set(re.findall(r'FS\d{2}', t))
    return None, set()


def 查(n=None):
    n = n or _末章()
    欠 = [x for x in 未销() if x['due'] and x['due'] < n]
    f, 答 = 回执之答(n)
    未答 = [x for x in 欠 if x['id'] not in 答]
    return n, f, 欠, 未答, 答



# ★★★★★★2026-09-13 立第二路（FS18 一案逼出来的）：
#   ⛔**本闸只问「逾期之根，本章回执回没回话」**——**它从来没问过「回执说已经付了的，账上销没销」。**
#   ★0913 之实：**FS18 係第313章当章付毕**（`回执_20260911_第313章作业单.md:121` 自书「本章付毕（拍101—110）」，
#   同档第48行逐格记其三段拍号），⛔**而 canon 之 status 自那日起一直留着 open**；
#   **於是本闸连报十二章「逾期」，而它报的是一笔已经付过的钱。**
#   ★★**这与本册 ㊗ 同骨**：**一个产方（回执自书付毕）而无收方（账上无人去销）**；
#   **而更坏的一层是：它报的红看上去像真的，於是每一章都有人把它当噪声跳过去。**
#   ⛔**故立此路：凡回执自书「FSxx…付毕」者，canon 之 status 不许再是 open。**
_付 = re.compile(r'(FS\d{2})[^。\n]{0,80}?本章付毕')


def 已付而未销():
    """返回 [(FS编号, 回执档名)]：回执自书付毕，而 canon 上仍 open 者。"""
    d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
    开 = {x.get('id') for x in d.get('foreshadows', [])
          if str(x.get('status', '')).lower() not in 清}
    出 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*.md'))):
        s = io.open(f, encoding='utf-8', errors='replace').read()
        for m in _付.finditer(s):
            if m.group(1) in 开:
                出.append((m.group(1), os.path.basename(f)))
    return sorted(set(出))


def 报(quiet=False):
    n, f, 欠, 未答, 答 = 查()
    if not quiet:
        print('════ FS 沉默闸 · 以第%d章计 ════' % n)
        print('  【其律】逾期之伏笔，本章回执须逐根回话——不必兑付，只须回话。')
        print('  逾期 %d 根｜本章回执%s｜已答 %d 根｜**未答 %d 根**'
              % (len(欠), ('＝' + f) if f else '未交', len(答 & {x['id'] for x in 欠}), len(未答)))
        for x in 未答:
            print('  ⛔ %-6s 限%-4s 逾 %3d 章 ｜%s' % (x['id'], x['due'], n - x['due'], x['desc'][:52]))
        if not 未答:
            print('  ✓ 逐根俱已回话。')
        # ★并印改期之数——一根钩子若靠反复改期永不兑现，那笔账在这儿看得见
        多 = [x for x in 未销() if x.get('改期', 0) >= 2]
        改 = [x for x in 未销() if x.get('改期', 0) >= 1]
        if 改:
            print('  ── 改期之账 ──')
            print('     改过期者 %d 根：%s' % (len(改), '、'.join('%s(限%s·%d回)' % (x['id'], x['due'], x['改期']) for x in 改)))
        if 多:
            print('  ⚠ 改期逾二回者 %d 根——须由人当场裁它还算不算一根活钩子：%s'
                  % (len(多), '、'.join(x['id'] for x in 多)))
        漏 = 已付而未销()
        print('  ── 第二路·回执自书付毕而账上未销（0913 立）──')
        for i, f in 漏:
            print('  ⛔ %s：回执自书「本章付毕」而 canon 仍 open（%s）' % (i, f))
        if not 漏:
            print('  ✓ 零处（凡回执自书付毕者，账上皆已销）。')
    return list(未答) + 已付而未销()


def 自测():
    R = []
    R.append(('①今日零处「已付而未销」', 已付而未销() == []))
    # ②【证其有牙】拿 FS18 之真局回灌：把它当作仍 open，须逮得出
    d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
    有 = any(x.get('id') == 'FS18' and str(x.get('status', '')).lower() in 清
             for x in d.get('foreshadows', []))
    R.append(('②FS18 今已销（其付在313·拍101—110）', 有))
    R.append(('③回执里确有「FS18…本章付毕」之句（⛔证②不是空销）',
              any(i == 'FS18' for i, _ in _扫回执())))
    # ④⛔「付毕」二字不在同一句者不认（不许拿一句不相干的话当付讫）
    R.append(('④隔句者不认', _付.search('FS18 之限在313。另有一根本章付毕。') is None))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


def _扫回执():
    出 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*.md'))):
        s = io.open(f, encoding='utf-8', errors='replace').read()
        for m in _付.finditer(s):
            出.append((m.group(1), os.path.basename(f)))
    return 出


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(1 if 报() else 0)
