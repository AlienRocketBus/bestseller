#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书级体检 —— 补十轮系统之唯一盲区。

【立此工具之由（191章末所立）】
十轮系统之每一闸皆为**章级**：四数、⑤90分位、已逮之根表、必答表、两两比、器物点名。
故凡「一样东西在连续数十章里慢慢漂掉」者，无一闸看得见。
其证：沈鸢末次出现於第115章、苏衍末次出现於第101章——
而这七十六章里，每一轮之补裁皆书「判零处而合，其类为本不在场」。
**该判每一次都是对的，而合起来是错的。**

故立六检：
  ① 人物在场衰减 —— 缺席不是罪，缺席而无账才是罪
  ② 章型连锁     —— 单章指标查不出「九章同一个纹理」
  ③ 账之净额     —— 每清一笔便立一笔者，永不收束
  ④ 日数速率     —— 报而不闸
  ⑤ 距终点与账之余额 —— 未清之账须清得完
  ⑥ 轮记开销比   —— 报而不闸

用法：
  python3 工具/书级体检.py            # 跑六检，报并闸
  python3 工具/书级体检.py --存基线    # 跑毕存入 设定/书级基线.json
  python3 工具/书级体检.py --静        # 只报闸之成败（供全测调用）
"""
import json
import os
import re
import sys
import collections
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT_DIR = os.path.join(ROOT, '正文')
BOOK_JSON = os.path.join(ROOT, '设定', '书级基线.json')
DUE_JSON = os.path.join(ROOT, '设定', '到期账.json')
VER_DIR = os.path.join(ROOT, '版本')

# ── 书之终点（191章末所定）──────────────────────────────
# 立此数之由：账之净额近十章为 +2，即每清一笔便立一笔，永不收束；
# 而无终点则无收束之压。定数以后，账才有理由净减，章型才有理由变。
END_CH = 220

# ── 主线人物之在场限（章）──────────────────────────────
# 缺席不得逾此数；逾之而无账者，闸报。
PRESENCE_LIMIT = {
    '老头': 3,
    '钱满': 5,
    '刘二': 5,
    '东头': 5,
    '沈鸢': 40,
    '苏衍': 60,
}
# 同型连锁之限（章）
TYPE_CHAIN_LIMIT = 12
# 自此章起，近十章之账须净减
NET_DUE_FROM = 192

CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
      '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def cn2int(s):
    t = n = 0
    for c in s:
        if c in CN and c != '十':
            n = CN[c]
        elif c == '十':
            t += (n or 1) * 10
            n = 0
        elif c == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


def chapter_no(path):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(path))
    return cn2int(m.group(1)) if m else None


def load_chapters():
    out = {}
    if not os.path.isdir(TEXT_DIR):
        return out
    for name in os.listdir(TEXT_DIR):
        if not name.endswith('.md'):
            continue
        p = os.path.join(TEXT_DIR, name)
        c = chapter_no(p)
        if c is None:
            continue
        with open(p, encoding='utf-8', errors='replace') as f:
            out[c] = f.read().split('【本章亮点')[0]
    return out


def net_len(t):
    return len(re.sub(r'\s', '', t))


def load_due():
    if not os.path.exists(DUE_JSON):
        return []
    with open(DUE_JSON, encoding='utf-8') as f:
        d = json.load(f)
    if isinstance(d, list):
        return d
    return d.get('items', d.get('账', []))


# ── ① 人物在场衰减 ────────────────────────────────────
def check_presence(chs, due):
    cur = max(chs) if chs else 0
    last = {}
    for c in sorted(chs):
        for who in PRESENCE_LIMIT:
            if who in chs[c]:
                last[who] = c
    # 已挂账者（其事之中含该人之名，且未清）视为「已在盯」
    watched = {}
    for x in due:
        if x.get('状态') != 'open':
            continue
        for who in PRESENCE_LIMIT:
            if who in str(x.get('事', '')):
                watched[who] = x.get('到期章')
    rows, bad = [], []
    for who, lim in PRESENCE_LIMIT.items():
        ln = last.get(who)
        gap = (cur - ln) if ln else cur
        ok = gap <= lim
        note = ''
        if not ok:
            if who in watched:
                note = '已挂账·限%s章' % watched[who]
                ok = True
            else:
                note = '⛔逾限而无账'
                bad.append('%s缺席%d章（限%d）且未挂账' % (who, gap, lim))
        rows.append((who, ln, gap, lim, ok, note))
    return rows, bad, last


# ── ② 章型连锁 ────────────────────────────────────────
def sig_of(body):
    ps = [x.strip() for x in body.split('\n') if x.strip()][2:]
    ps2 = [net_len(x) for x in ps if x != '＊']
    if not ps2:
        return None, 0, 0
    n = len(ps2)
    total = sum(net_len(x) for x in ps)
    avg = total / max(1, len(ps))
    # 章型以均段分档：短（<15）／中（15-21）／长（>21）
    kind = '短' if avg < 15 else ('中' if avg <= 21 else '长')
    return kind, avg, total


def check_type_chain(chs):
    seq = []
    for c in sorted(chs):
        k, avg, tot = sig_of(chs[c])
        if k:
            seq.append((c, k, avg, tot))
    chain, last_kind = 0, None
    start = None
    for c, k, avg, tot in seq:
        if k == last_kind:
            chain += 1
        else:
            chain, last_kind, start = 1, k, c
    bad = []
    if chain > TYPE_CHAIN_LIMIT:
        bad.append('同型「%s」已连锁 %d 章（第%d—%d章，限%d）'
                   % (last_kind, chain, start, seq[-1][0], TYPE_CHAIN_LIMIT))
    return seq[-14:], (last_kind, chain, start), bad


# ── ③ 账之净额 ────────────────────────────────────────
def check_due_net(due, cur):
    made = collections.Counter()
    clr = collections.Counter()
    for x in due:
        if isinstance(x.get('立账章'), int):
            made[x['立账章']] += 1
        if isinstance(x.get('清偿章'), int):
            clr[x['清偿章']] += 1
    lo = max(1, cur - 9)
    rows = [(c, made[c], clr[c], made[c] - clr[c]) for c in range(lo, cur + 1)]
    net = sum(r[3] for r in rows)
    bad = []
    if cur >= NET_DUE_FROM and net > 0:
        bad.append('近十章账之净额 %+d（自第%d章起须 ≤0）' % (net, NET_DUE_FROM))
    return rows, net, bad


# ── ④ 日数速率 ────────────────────────────────────────
def check_pace(chs):
    ds = []
    for c in sorted(chs):
        m = re.search(r'第([零〇一二三四五六七八九十百]+)天', chs[c])
        if m:
            ds.append((c, cn2int(m.group(1))))
    if len(ds) < 2:
        return None
    tail = ds[-25:]
    dc = tail[-1][0] - tail[0][0]
    dd = tail[-1][1] - tail[0][1]
    return (tail[0], tail[-1], dc, dd, (dd / dc) if dc else 0)


# ── ⑤ 距终点与账之余额 ────────────────────────────────
def check_endgame(due, cur):
    op = [x for x in due if x.get('状态') == 'open']
    left = END_CH - cur
    bad = []
    if left <= 0:
        bad.append('已达或逾终点第%d章而未收' % END_CH)
    elif len(op) > left:
        bad.append('未清之账 %d 笔 > 距终点 %d 章（清不完）' % (len(op), left))
    over = [x for x in op if isinstance(x.get('到期章'), int) and x['到期章'] > END_CH]
    if over:
        bad.append('有 %d 笔账之到期章逾终点：%s'
                   % (len(over), '、'.join(x['id'] for x in over[:5])))
    return op, left, bad


# ── ⑥ 轮记开销比 ──────────────────────────────────────
def check_overhead(chs):
    cur = max(chs) if chs else 0
    sz, pr = [], []
    for c in range(max(1, cur - 5), cur + 1):
        f = os.path.join(VER_DIR, '第%d章' % c, '_轮记.md')
        if os.path.exists(f):
            with open(f, encoding='utf-8', errors='replace') as fh:
                sz.append(net_len(fh.read()))
        if c in chs:
            pr.append(net_len(chs[c]))
    if not sz or not pr:
        return None
    a, b = sum(sz) / len(sz), sum(pr) / len(pr)
    return a, b, a / b


def main():
    quiet = '--静' in sys.argv
    save = '--存基线' in sys.argv
    chs = load_chapters()
    if not chs:
        print('⛔ 未见正文')
        return 2
    cur = max(chs)
    due = load_due()
    allbad = []

    rows_p, bad_p, last = check_presence(chs, due)
    allbad += bad_p
    seq, chain, bad_t = check_type_chain(chs)
    allbad += bad_t
    rows_d, net_d, bad_d = check_due_net(due, cur)
    allbad += bad_d
    pace = check_pace(chs)
    op, left, bad_e = check_endgame(due, cur)
    allbad += bad_e
    ovh = check_overhead(chs)

    if not quiet:
        total = sum(net_len(v) for v in chs.values())
        print('════════ 书级体检 · 第%d章 ════════' % cur)
        print('  全书 %d 章｜正文净重 %d 字｜均 %.0f 字/章'
              % (len(chs), total, total / len(chs)))
        print()
        print('① 人物在场衰减（缺席不是罪，缺席而无账才是罪）')
        for who, ln, gap, lim, ok, note in rows_p:
            print('   %-4s 末次第%-4s章｜缺席%3d章（限%2d）%s %s'
                  % (who, ln if ln else '—', gap, lim,
                     '✓' if ok else '⛔', note))
        print()
        print('② 章型连锁（限%d章）' % TYPE_CHAIN_LIMIT)
        print('   近十四章：', ' '.join('%d%s' % (c, k) for c, k, a, t in seq))
        print('   ★当前「%s」型已连 %d 章（自第%s章起）%s'
              % (chain[0], chain[1], chain[2], '⛔' if bad_t else '✓'))
        print()
        print('③ 账之净额（自第%d章起须 ≤0）' % NET_DUE_FROM)
        print('   ' + ' '.join('%d:%+d' % (c, n) for c, m, k, n in rows_d))
        print('   ★近十章净 %+d %s' % (net_d, '⛔' if bad_d else '✓'))
        print()
        if pace:
            (c0, d0), (c1, d1), dc, dd, r = pace
            print('④ 日数速率（报而不闸）')
            print('   第%d章＝入山第%d日 → 第%d章＝入山第%d日｜%.2f 日/章'
                  % (c0, d0, c1, d1, r))
            print()
        print('⑤ 距终点与账之余额（终点第%d章）' % END_CH)
        print('   未清 %d 笔｜距终点 %d 章｜须净减 %.2f 笔/章 %s'
              % (len(op), left, len(op) / max(1, left), '⛔' if bad_e else '✓'))
        for x in sorted(op, key=lambda y: y.get('到期章') or 999):
            print('     %-14s 限%-4s %s' % (x['id'], x.get('到期章'), str(x.get('事'))[:40]))
        print()
        if ovh:
            print('⑥ 轮记开销比（报而不闸）')
            print('   轮记 %.0f 字/章｜正文 %.0f 字/章｜★比 %.1f 倍'
                  % (ovh[0], ovh[1], ovh[2]))
        print()
        print('════════════════════════════════')

    if allbad:
        print('  【书级体检·不过】%d 条：' % len(allbad))
        for b in allbad:
            print('     ⛔ ' + b)
        return 2
    if not quiet:
        print('  【书级体检·通过】六检皆过。')
    else:
        print('  ✓书级体检通过。')

    if save:
        base = {
            '章': cur,
            '时': datetime.datetime.now().strftime('%Y-%m-%d'),
            '终点章': END_CH,
            '正文净重': sum(net_len(v) for v in chs.values()),
            '人物末次': {w: last.get(w) for w in PRESENCE_LIMIT},
            '章型连锁': {'型': chain[0], '连': chain[1], '自': chain[2]},
            '账': {'未清': len(op), '近十章净': net_d, '距终点': left},
            '日数速率': round(pace[4], 3) if pace else None,
            '轮记开销比': round(ovh[2], 2) if ovh else None,
        }
        with open(BOOK_JSON, 'w', encoding='utf-8') as f:
            json.dump(base, f, ensure_ascii=False, indent=1)
        print('  ✓基线已存：设定/书级基线.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
