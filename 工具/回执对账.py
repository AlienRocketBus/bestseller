# -*- coding: utf-8 -*-
"""回执对账闸（2026-09-01 立·全书审计第二层 2-4）

★立此闸之由：287回执自书「净重2,951（起草）→2,796…十三轮共减155字」，
　★★而台账逐版明印 v01=2,529 → 峰 v08=2,951 → v15=2,796，**是净增 267**——
　★★★把第6轮那个峰当成了起草，方向整个反了 ⛔。
★★★★而令§十一曰：**留底之档里的错因，会被下一坐当成场**。
　★一份把自己的产出记反了的回执，比一处错字活得久得多。

【其式】自回执首节取「净重 A（起草…）→ … → B（末版…）」之二数，
　　与 版本/第N章/_台账.json 之 版本[0] / 版本[-1] 逐个比；不等即红。
【不认者】旧制之章其回执无此式者——报「无此式」，不判红（不许拿今日之尺去量昨日封的章）。
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _净(v):
    return (v.get('soft') or {}).get('净重') or (v.get('量') or {}).get('净重')


def 台账(n):
    p = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    if not os.path.exists(p):
        return None
    vs = json.load(io.open(p, encoding='utf-8')).get('版本') or []
    vs = [v for v in vs if _净(v) is not None]
    if not vs:
        return None
    return {'起': _净(vs[0]), '峰': max(_净(v) for v in vs), '终': _净(vs[-1]),
            '首版': vs[0].get('版'), '末版': vs[-1].get('版'), '版数': len(vs)}


def 回执之数(n):
    """★★2026-09-01 再收窄（首二版皆开得太宽，其伤在闸不在文）：
      ①首版把「回执未报起草／末版之数」判红 → 全书一开报约150章 ⛔（旧回执格式不同，不是错）；
      ②二版判「峰在 nums 而起不在」→ 报8章，逐份读过全是误报：
        ★253之回执写「**定本**：v22…净重2998」——那是末版，而其峰恰好等於终 ✓；
        ★★269之回执甚至把整条曲线印了出来「4495→…→7004，峰在末轮 ✓」。
      ★★★故真正那一形只有一个，且须逐字咬定：**回执明写「起草」二字，而它旁边那个数不是台账的 v01**。
      ★★★★此形今日全书只 287 一章犯过（已正），而它正是令§十一所指之病：
        ★留底之档里的错因，会被下一坐当成场。
    """
    for p in sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*第%d章*.md' % n))):
        t = io.open(p, encoding='utf-8').read()
        头 = t.split('## 二')[0]
        # ★★★2026-09-01 三收窄（前式仍有二噪，皆是闸自己的）：
        #   ①向後看那一支会咬到「（起草）→3,330」里的 3,330——那是末版，不是起草 ⛔
        #     （286之回执作「净重2,506（起草）→3,330」，2,506 正对台账 v01，本无错）；
        #   ②回执里凡自陈其错者（「此处先前写作『2,951（起草）→…』」），
        #     ★★那一行是**改正**，不是错——闸把人认错的那句话又判了一遍 ⛔。
        #   ★★★故：只认「数＋（起草」这一形（数在前，紧贴），且跳过含「先前写作」之行。
        起 = []
        for l in 头.split('\n'):
            if '先前写作' in l or '先前作' in l:
                continue
            for x in re.findall(r'([\d,]{3,7})\s*[（(]\s*起草', l):
                起.append(int(x.replace(',', '')))
        return os.path.basename(p), 起
    return None, []


def 查(n):
    t = 台账(n)
    if not t:
        return None
    f, 起数 = 回执之数(n)
    if not f:
        return ('无回执', n, t, [])
    if not 起数:
        return ('无此式', n, t, [])       # ★回执未用「起草」二字者不判——不许拿今日之尺量昨日之章
    # ★★★★2026-09-01 四收窄（末二噪，逐份读过方见）：
    #   ①第276章：回执作「2589（起草）」而台账 v01＝2813——而 v01 之说明是「**第1轮**」，
    #     ★即 276 之第0轮根本没存版；2589 是真的起草之数，缺的是台账那一版 ⛔ → 不判回执，另报「台账缺起草版」。
    #   ②第275章：回执与 v01 之说明皆作 3498，而器量得 3499——差一字。
    #     ★★令§一④曰凭据须由器自己落；然差一字者判红即天天喊，故只软报。
    # ★★★故其律：**唯 v01 确为起草之版，且其差 ≥50 者，方判红**。
    #   ★★★★今日全书只 287 一章曾犯（差 422，已正）——**一道只在真出事时才响的闸。**
    首说 = ''
    tp = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    if os.path.exists(tp):
        _vs = json.load(io.open(tp, encoding='utf-8')).get('版本') or []
        if _vs:
            首说 = str(_vs[0].get('说明', ''))
    if not re.search(r'起草|第0轮', 首说):
        return ('缺起草版', n, t, ['台账 %s 之说明为「%s…」，非起草之版——其差不判回执，判台账缺一版'
                                   % (t['首版'], 首说[:12])])
    坏, 软 = [], []
    for x in 起数:
        d = abs(x - t['起'])
        if d >= 50:
            坏.append('★回执称 %d 为起草，而台账之 %s＝%d，差 %d%s ⛔'
                      % (x, t['首版'], t['起'], d,
                         '（%d 是峰，不是起草）' % x if x == t['峰'] else ''))
        elif d:
            软.append('回执 %d 与器印 %d 差 %d（软报）' % (x, t['起'], d))
    return ('红' if 坏 else '过', n, t, 坏 or 软)


def 全书(quiet=False):
    out = []
    for d in sorted(glob.glob(os.path.join(ROOT, '版本', '第*章'))):
        m = re.search(r'第(\d+)章', d)
        if not m:
            continue
        r = 查(int(m.group(1)))
        if r and r[0] == '红':
            out.append(r)
    if not quiet:
        print('════ 回执对账 ════')
        print('  【其式】回执首节之净重诸数 vs 台账 版本[0]／版本[-1]。')
        if not out:
            print('  ✓ 零章不符。')
        for st, n, t, 坏 in out:
            print('  ⛔ 第%d章：台账 起%d 峰%d 终%d（%d版）' % (n, t['起'], t['峰'], t['终'], t['版数']))
            for x in 坏:
                print('       · ' + x)
    return out


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--章':
        print(查(int(sys.argv[2])))
        sys.exit(0)
    sys.exit(1 if 全书() else 0)
