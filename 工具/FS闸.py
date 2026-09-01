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
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
清 = ('paid', 'done', 'closed', '已销', '已兑', '废')


def 未销():
    d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
    out = []
    for x in d.get('foreshadows', []):
        if str(x.get('status', '')).lower() in 清:
            continue
        out.append({'id': x.get('id'), 'due': x.get('due'), 'desc': x.get('desc', '')})
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
    return 未答


if __name__ == '__main__':
    sys.exit(1 if 报() else 0)
