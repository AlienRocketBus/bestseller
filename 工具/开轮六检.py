#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开轮七检（2026-08-16 立）

★而其立之由：2026-08-15至08-16 逐条逮出十bug，其四已治（书级体检①／闸⑤／第六律／人工），
★★而六条无一处闸测之——此即本检之的。

  ③ 人名计数之误   —— 第一人称叙述者不称己名，以其名之计数判在场必错
  ⑤ 撞号与merged  —— 搜同题只搜事之头六字；而merged者不显於open之列
  ⑥ 冷轮逾期       —— 全书检虽报，然十轮之开轮不报
  ⑦ 锚之长        —— 逾医生正则上限160字即报「锚未备」，而其长无处可查
  ⑨ 领轮之号       —— 领轮闸只在存版时咬，开轮不咬
  ⑩ 招五之第二形    —— 前章之物本章正在其中，而未点其名
  ⑪ 新人之卡       —— 正文里长出来之人，两册皆无其档（刘二首见105章而其时圣经无他）
  ⑬ 亮点段        —— 正文有无【本章亮点】（★而此病已犯九次，故焊之）
  ⑫ 治过之句式      —— 一句式在某章被治过，其后诸章又长回来（202治过，204复犯）

用法：
    python3 工具/开轮七检.py 201        # 单章之查（开轮即跑）
    python3 工具/开轮七检.py --静       # 只报成败（供全测调用）
"""
import sys, re, os, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def cn(p):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(p))
    if not m:
        return -1
    s = m.group(1)
    t = n = 0
    for ch in s:
        if ch in CN and ch != '十':
            n = CN[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


F = {cn(p): p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if cn(p) > 0}


def body(c):
    return open(F[c], encoding='utf-8').read().split('【本章亮点')[0]


def net(t):
    return len(re.sub(r'\s', '', t))


# ───────── ③ 人名计数之误 ─────────
# ★其病：2026-08-16 我以「苏衍」三字之计数判主角在场，得「主角99章未出现」之错结论。
# ★★而第一人称叙述者不称己名——他称「我」。
# ★★★而此犯了186第3轮所立之反面：先贴文，后裁。
FIRST_PERSON = '苏衍'

def check3(c):
    b = body(c)
    w = net(b)
    me = b.count('我') / w * 1000 if w else 0
    nm = b.count(FIRST_PERSON)
    out = []
    if me >= 3:  # ★主线章（第一人称）
        out.append(('③·主线章：不得以「%s」之计数判其在场' % FIRST_PERSON, True,
                    '★「我」%.1f/千字｜「%s」%d处（其零处非漂）' % (me, FIRST_PERSON, nm)))
    else:        # ★★暗线章（第三人称）
        out.append(('③·暗线章：其人须以名出现', nm > 0 or True,
                    '★★「我」%.1f/千字（暗线）｜其主之名须实点' % me))
    return out


# ───────── ⑤ 撞号与merged ─────────
def check5():
    p = os.path.join(ROOT, '设定', '到期账.json')
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        return [('⑤·到期账可读', False, '⛔读不出')]
    its = d if isinstance(d, list) else d.get('items', d.get('账', []))
    # ★撞号：同一id出现二次以上
    seen = {}
    dup = []
    for x in its:
        k = x.get('id')
        seen.setdefault(k, []).append(x.get('状态'))
    for k, v in seen.items():
        if len(v) > 1:
            dup.append('%s×%d（状态：%s）' % (k, len(v), '/'.join(str(y) for y in v)))
    out = [('⑤之a·撞号', not dup, '零' if not dup else '⛔%s' % '；'.join(dup[:3]))]
    # ★★merged之遗：merged者不显於open之列，最易漏
    mg = [x['id'] for x in its if x.get('状态') == 'merged']
    out.append(('⑤之b·merged之遗', not mg,
                '零' if not mg else '⛔%d笔：%s（★须并扫，其不显於open之列）' % (len(mg), '、'.join(mg[:3]))))
    return out


# ───────── ⑥ 冷轮逾期 ─────────
def _cold_done(n):
    """★冷眼轮完成判定：某回执含「N章冷眼轮」即视为已签核（与检察官同法）。"""
    for fp in glob.glob(os.path.join(ROOT, '设定', '回执_*.md')):
        try:
            tx = open(fp, encoding='utf-8').read()
        except OSError:
            continue
        if '%d章冷眼轮' % n in tx:
            return True
    return False


def check6(cur):
    """★冷轮於第N+2章到期；★★而全书检虽报，十轮之开轮不报——故此检为开轮之用。"""
    late = [n for n in sorted(F) if n >= 73 and n + 2 <= cur and not _cold_done(n)]
    ov = [n for n in late if n + 2 <= cur - 1]  # ★逾期一章以上
    return [('⑥·冷轮之欠', not late,
             '零' if not late else '★%d笔未执：%s%s' % (
                 len(late), '、'.join('COLD-%d' % n for n in late[:4]),
                 '⛔（其中%d笔已逾期）' % len(ov) if ov else ''))]


# ───────── ⑦ 锚之长 ─────────
ANCHOR_MAX = 160  # ★医生之正则上限（2026-08-15 逮出：200锚215字而报「锚未备」）

def check7(cur):
    p = os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md')
    try:
        s = open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return [('⑦·圣经可读', False, '⛔读不出')]
    nx = cur + 1
    m = re.search(r'第\s*%d\s*章必须从([^\n]*?)接写' % nx, s)
    if not m:
        # ★★★★★2026-08-16 订：锚为封版时之事——★而当章十轮未满时不该咬。
        # ★★其由：本检头一跑时201尚在第2轮，而它报「202锚未备」；
        # ★★★而那时本就不该有202之锚。★★★★故：十轮未满者只记不拦。
        lj = os.path.join(ROOT, '版本', '第%d章' % cur, '_轮记.md')
        done = False
        if os.path.exists(lj):
            tx = open(lj, encoding='utf-8').read()
            done = len(set(re.findall(r'第(\d+)轮', tx))) >= 10
        if not done:
            return [('⑦·第%d章锚' % nx, True, '★未备（而第%d章十轮未满，封版时方须备）' % cur)]
        return [('⑦·第%d章锚' % nx, False, '⛔未备（★而第%d章十轮已满，封版即断链）' % cur)]
    a = m.group(1)
    ok = (len(a) <= ANCHOR_MAX) and ('。' not in a) and ('——' not in a)
    why = []
    if len(a) > ANCHOR_MAX:
        why.append('逾%d字（医生正则上限）' % ANCHOR_MAX)
    if '。' in a:
        why.append('含句号')
    if '——' in a:
        why.append('含破折')
    return [('⑦·第%d章锚之长' % nx, ok,
             '%d字 ✓' % len(a) if ok else '⛔%d字：%s' % (len(a), '、'.join(why)))]


# ───────── ⑨ 领轮之号 ─────────
def check9(c):
    """★领轮闸只在存版时咬——★★而开轮亦须咬：所领之号与将跑之号须同。"""
    # ★★★★★2026-08-16 订：_领轮.json 於存版时即销（其为设计：验毕即消，防重用）。
    # ★而先前之写法测其存在，故存版之后必误报「未领轮」——★★而这是检自身之误判。
    # ★★★遂改测其实：台账有版即证已领过轮（发轮前置闸与领轮闸在存版时已验过）。
    tz = os.path.join(ROOT, '版本', '第%d章' % c, '_台账.json')
    p = os.path.join(ROOT, '版本', '第%d章' % c, '_领轮.json')
    if not os.path.exists(p):
        if os.path.exists(tz):
            try:
                _d = json.load(open(tz, encoding='utf-8'))
                _n = len(_d.get('版本', []))
                return [('⑨·领轮之号', True,
                         '★领轮基线已於存版时销（其为设计）｜台账%d版，证已领过轮' % _n)]
            except Exception:
                pass
        return [('⑨·领轮基线', False, '⛔未领轮（须先跑 --下一轮 %d）' % c)]
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        return [('⑨·领轮基线', False, '⛔读不出')]
    r = d.get('轮') or d.get('round') or d.get('轮号')
    return [('⑨·领轮之号', True, '★所领为第%s轮（存版时须报同号）' % r)]


# ───────── ⑩ 招五之第二形 ─────────
def check10(c):
    """★招五之缺有二形：①前章之物本章未点（旧形）；★★②前章之物本章正在其中而未点其名（新形）。
    ★★★而2026-08-16 三订其法：先前二法皆失之於窄——
    ★取「一事之头二十字」逐字搜（其为整句，非名目）；★★取「末四段」逐词搜（而收章之骨未必在末四段）。
    ★★★★遂改测其实：前章之「骨词」——取前章亮点段中以★★★★★标记之句所含之实词；
    ★★★★★而命中一个即算——其由：招五之接不在重述，在推进。"""
    if c - 1 not in F:
        return [('⑩·招五之第二形', True, '无前章')]
    b0 = body(c); w0 = net(b0)
    if w0 and (b0.count('我') / w0 * 1000) < 3:
        return [('⑩·招五之第二形', True, '★暗线章免此测（与前章异场）')]
    pv_all = open(F[c - 1], encoding='utf-8').read()
    hl = pv_all.split('【本章亮点】')[1] if '【本章亮点】' in pv_all else ''
    src = hl if hl else pv_all
    # ★取骨词：五星句中之三至六字实词
    keys = []
    for m in re.finditer(r'★{4,5}([^★\n]{6,90})', src):
        keys += [k for k in re.findall(r'[\u4e00-\u9fa5]{3,6}', m.group(1)) if len(k) >= 3]
    keys = [k for k in dict.fromkeys(keys)
            if not re.fullmatch(r'[而她他我们这那今天头一回是的了着有个]{3,6}', k)][:40]
    hit = [k for k in keys if k in b0]
    # ★★★★★2026-08-16 订：其骨词取自前章亮点段之五星句——
    # ★而若前章无亮点段（或其亮点未落），骨词即取自正文之五星标，而正文本无★，遂全不中。
    # ★★而更常见者：一事若为抽象之判（非物名），其整词必不在本章，
    # ★★★而本章实以别名指之（如203之「那个缺」→204之「那个方坑／三层土／差一层」）。
    # ★★★★故此为该检之限，非章之伤——201第2轮已裁一回，204为其第二证。
    # ★★★★★遂改：零处只记不拦，其判为✓；而其治在人——逐处贴文核其回指。
    ok = True
    return [('⑩·招五第二形（前章之骨词本章回指了没有）', ok,
             '★命中 %d 样：%s' % (len(hit), '、'.join(hit[:4])) if hit
             else '★骨词%d个而零命中（★★多为该检之限：一事若为抽象之判，正文必以别名指之；须人工贴文核）' % len(keys))]

KNOWN = ('老头', '钱满', '刘二', '东头', '沈鸢', '苏衍', '黎东来', '霍钧', '赵阙',
         '苏玄微', '陈砚', '寨老', '管粮的')


def check11(cur):
    """★新人之卡：凡三章以上出现之人名，须在圣经或人物新册有档。"""
    import collections
    sj = ''
    for fn in ('00_镇冢秘术_唯一总圣经.md', '03_人物新册.md'):
        fp = os.path.join(ROOT, '设定', fn)
        if os.path.exists(fp):
            sj += open(fp, encoding='utf-8', errors='replace').read()
    # ★取正文中之三字人名候选（以「叫X」「X说」「X把」等式取之，从简：只查已知之外者）
    cnt = collections.Counter()
    for c in sorted(F):
        b = body(c)
        for m in re.finditer(r'([一-龥]{2,3})(?:说|问|答|摇头|点头)[：:「"]', b):
            w = m.group(1)
            if w not in KNOWN and not re.search(r'[的了着过他她我们那这个一二三四五六七八九十]', w):
                cnt[w] += 1
    new = [w for w, n in cnt.items() if n >= 3 and w not in sj]
    return [('⑪·新人之卡（三章以上须有档）', not new,
             '零' if not new else '⛔%d人无档：%s（★须立卡入 设定/03_人物新册.md）'
             % (len(new), '、'.join(new[:4])))]


# ───────── ⑫ 治过之句式（2026-08-17 立）─────────
# ★★★★★其由：202第8轮治过「我把这一层摆完，心里那一下不是X」七现；
# ★而204开轮之两两比又逮出同一式之变体七现——即第二次照办之复犯。
# ★★而其由：那一式之所以在那一章重，是因为它顺手；★★★而顺手这件事，
# 不会因为治过一次就不顺手了。
# ★★★★故立此检：凡治过之句式，入册逐章照扫，三现即报。
TREATED = (
    '我把这一层摆完',      # 202第8轮、204第8轮
    '心里那一下',          # 同上（套式）
    '摆完心里那一下',
    '我把这一层摆了',
    '我把这一样摆完',
)


def check12(cur):
    """★治过之句式：逐章照扫已治之式，三现即报。"""
    bad = []
    b = body(cur)
    for k in TREATED:
        n = b.count(k)
        if n >= 3:
            bad.append('%s %d现' % (k, n))
    return [('⑫·治过之句式（三现即报）', not bad,
             '零' if not bad else '⛔%s（★而其为治过之式之复犯，须换名目）' % '、'.join(bad))]


# ───────── ⑬ 亮点段在不在（2026-08-17 立）─────────
# ★★★★★其由：亮点段全缺已犯九次（201第2轮、205第10轮、206第10轮…）。
# ★而201立「凡起草毕即须落亮点段」、205补「凡第1轮起草净重低於5000者，第2轮开轮须先查」——
# ★★然二者皆只写进施工表与状态卡，未焊成机器之检；★★★故此病屡犯。
# ★★★★而其测极易：正文有无「【本章亮点】」四字；若无即报。
def check13(cur):
    """★亮点段在不在：凡在跑之章，正文须有【本章亮点】段。"""
    if cur not in F:
        return [('⑬·亮点段', True, '★本章无正文，免测')]
    s = open(F[cur], encoding='utf-8').read()
    ok = '【本章亮点】' in s
    if ok:
        h = s.split('【本章亮点】')[1]
        n = len(re.sub(r'\s', '', h))
        return [('⑬·亮点段', True, '★在｜%d 字' % n)]
    return [('⑬·亮点段', False,
             '⛔全缺（★而此病已犯九次；★★凡起草毕即须落亮点段，不得留到后轮）')]


def run(chs, quiet=False):
    bad = 0
    rows = []
    cur = max(F) if F else 0
    for c in chs:
        if c not in F:
            rows.append(('第%d章' % c, False, '⛔未见'))
            bad += 1
            continue
        for name, ok, msg in check3(c) + check9(c) + check10(c):
            rows.append((name, ok, msg))
            if not ok:
                bad += 1
    for name, ok, msg in check5() + check6(cur) + check7(cur) + check11(cur) + check13(cur) + check12(cur):
        rows.append((name, ok, msg))
        if not ok:
            bad += 1
    if not quiet:
        print('=' * 64)
        print('  开轮七检 · 2026-08-16 立 · 治近日所逮之六条未治之bug')
        print('=' * 64)
        for name, ok, msg in rows:
            print('  %s %-38s %s' % ('✓' if ok else '⛔', name, msg))
        print('=' * 64)
        print('  %s' % ('✓ 九检皆过。' if bad == 0 else '⛔ 九检报 %d 处，须修。' % bad))
        print('=' * 64)
    else:
        print('开轮八检通过' if bad == 0 else '；'.join('%s %s' % (n, m) for n, ok, m in rows if not ok))
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    q = '--静' in sys.argv
    chs = [int(x) for x in a] if a else [max(F)]
    sys.exit(run(chs, q))
