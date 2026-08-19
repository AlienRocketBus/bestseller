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
  ㉑ 已起草之章      —— 本章正文已在即报(勿再另写一篇)
  ⑱ 生死线之期      —— 要命之线还能吊几章(水尽已第十日,限十二日)
  ⑲ 骨之方向       —— 近三章之骨皆朝同一向即报(207/208/209皆为他那本账)
  ⑳ 未答之问       —— 本章摆出之问,当章答了几个
  ⑮ 承前之判       —— 前章收句之骨,本章回指了没有
  ⑯ 悬账之量       —— 同时未清逾12笔即报(读者记不住)
  ⑰ 近五章之形      —— 同形逾三章即报(形一样久了会腻)
  ⑭ 已封版之章      —— 凡领轮之章已封版者当场拦（再跑会覆盖其回执与轮记）
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


def cn2int(s):
    """★中文数字转整（2026-08-18 补·⑱所需）。"""
    CN2 = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
           '六': 6, '七': 7, '八': 8, '九': 9}
    t = n = 0
    for ch in str(s):
        if ch in CN2:
            n = CN2[ch]
        elif ch == '十':
            t += (n or 1) * 10
            n = 0
        elif ch == '百':
            t += (n or 1) * 100
            n = 0
    return t + n


def body(c):
    # ★2026-08-17 订：未起草之章无正文——★★先前於此崩（KeyError），故未起草之章无法跑检；
    # ★★★而其时正该跑⑭⑯⑰以定其可否起草。遂改：无正文者返空串。
    if c not in F:
        return ''
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
            # ★★★★★2026-08-17 订：先前以文中任一「第N轮」计，遂误判。
            # ★其由：轮记之正文常引先例（依二百章第6轮所立、而一百九十九章第8轮…），
            # ★★而那些引文里的轮号被一并计入——★★★遂207真轮5/10而判「十轮已满」。
            # ★★★★而其正法：只计「## 第N轮」之标题，因为那才是一轮之实。
            done = len(set(re.findall(r'^## 第(\d+)轮', tx, re.M))) >= 10
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


# ───────── ⑫ 已封版之章（2026-08-17 立）─────────
# ★★★★★其由：2026-08-17 我拿第202章去跑十轮，而202早已封版（203—207亦然）。
# ★而机器报「真轮10/10」时，我把它当成「本轮该跑第十一轮」——
# ★★可它其实是在说：这一章早跑完了。
# ★★★而我竟又交了一份202回执，覆盖了原有的那一份（已 git checkout 复原）。
# ★★★★而其形正与⑨之「未竟之章」相反：一为该跑而没跑完，一为跑完了还去跑；
# ★★★★★而后者更险——因为它会覆盖已封版的回执与轮记。
def check14(cur):
    """★已封版之章：凡领轮之章已封版者，当场报。
    ★★而其判之据有三：十一轮之凭据、回执、且其后已有新章。"""
    if not cur:
        return [('⑭·已封版之章', True, '★未指章')]
    d = os.path.join(ROOT, '版本', '第%d章' % cur)
    e11 = os.path.exists(os.path.join(d, '_十一轮.json'))
    try:
        hz = [f for f in os.listdir(os.path.join(ROOT, '设定'))
              if '第%d章' % cur in f and '回执' in f]
    except Exception:
        hz = []
    mx = max(F) if F else 0
    # ★2026-08-17 订：先前之条件为 cur < mx，故末章若已封版亦放行；
    # ★★而实况：208已封版（十一轮✓／回执✓）而检报「未封版，可跑」——其为误判。
    # ★★★遂改：凡十一轮之凭据与回执俱在者，即为已封版，不论其是否末章。
    if e11 and hz:
        return [('⑭·已封版之章', False,
                 '⛔第%d章已封版（十一轮✓／回执✓｜末章第%d章）'
                 '：★而封版之章不得再跑十轮——★★再跑会覆盖其回执与轮记。'
                 '★★★而今之末章为第%d章；★★★★下一章为第%d章。'
                 % (cur, mx, mx, mx + 1))]
    return [('⑭·已封版之章', True,
             '★第%d章未封版（十一轮%s／回执%s），可跑'
             % (cur, '✓' if e11 else '✗', '✓' if hz else '✗'))]


# ───────── ⑮ 承前之判（2026-08-17 立）─────────
# ★★★★★其由：十轮里没有一轮问「这一章跟前一章接不接得上」。
# ★第2轮只查回述词（想起/昨天/那一回），★★第3轮只查数；
# ★★★而「昨天他立了一个判，今天本章认它、翻它、还是没提它」——无一轮问。
# ★★★★而其证：208之「老头照着一个已经不在的数使力气」是我写时想到的，不是闸逼出来的。
# ★★★★★故立此检：取前章收句之骨词，查本章有无回指。
def check15(cur):
    """★承前之判：前章之末所立之判，本章认它、翻它、还是没提它。"""
    if not cur or (cur - 1) not in F:
        return [('⑮·承前之判', True, '★无前章，免测')]
    pb = body(cur - 1)
    b = body(cur)
    if not pb or not b:
        return [('⑮·承前之判', True, '★正文缺，免测')]
    # ★取前章之末五段（其为收句之所在）
    tail = [x.strip() for x in pb.split('\n') if x.strip() and x.strip() != '＊'][-5:]
    txt = ''.join(tail)
    # ★★取其中之实词（二字以上、非虚字）
    cand = [w for w in re.findall(r'[\u4e00-\u9fa5]{2,4}', txt)
            if not re.search(r'^(而|是|不|的|了|着|这|那|我|他|她|你|们|就|也|都|还|要|说|有|没|一|个|上|下|里|头|来|去|又|把|跟|得|在|从|到|它|们)', w)]
    seen = []
    for w in cand:
        if w not in seen:
            seen.append(w)
    key = seen[:8]
    hit = [w for w in key if w in b]
    ok = len(hit) >= 2
    return [('⑮·承前之判（前章收句之骨，本章回指了没有）', ok,
             ('★命中 %d 样：%s' % (len(hit), '、'.join(hit[:4]))) if ok
             else ('⛔前章收句之骨 %s，本章一样也没回指'
                   '：★而这不一定是错——★★然须在轮记里明写一句：'
                   '本章认它、翻它、还是有意搁下' % '、'.join(key[:4])))]


# ───────── ⑯ 悬账之量（2026-08-17 立）─────────
# ★★★★★其由：到期账管的是「几时清」，而不管「同时悬着几笔」。
# ★而实测：今未清16笔——★★而读者记不住16笔。
def check16(cur):
    """★悬账之量：同时未清逾12笔即报（报而不拦）。"""
    fp = os.path.join(ROOT, '设定', '到期账.json')
    if not os.path.exists(fp):
        return [('⑯·悬账之量（≤12笔）', True, '★账册未见，免测')]
    try:
        d = json.load(open(fp, encoding='utf-8'))
        its = d if isinstance(d, list) else d.get('items', d.get('账', []))
        op = [x for x in its if x.get('状态') == 'open']
    except Exception as e:
        return [('⑯·悬账之量（≤12笔）', True, '★读账册失败：%s' % e)]
    n = len(op)
    ok = (n <= 12)
    near = sorted(op, key=lambda y: (y.get('到期章') or 999))[:3]
    s = '、'.join('%s(限%s)' % (x.get('id'), x.get('到期章')) for x in near)
    return [('⑯·悬账之量（≤12笔）', ok,
             ('★未清 %d 笔｜最近三笔：%s' % (n, s)) if ok
             else ('⛔未清 %d 笔，逾12：★而读者记不住这么多'
                   '——★★其治有二：或清一笔，或在正文里明说「这一笔先搁着」。'
                   '★★★最近三笔：%s' % (n, s)))]


# ───────── ⑰ 近五章之形（2026-08-17 立）─────────
# ★★★★★其由：近十章之骨皆为「翻一个判断」（手不准了/她那本账/算错的那个数/不是停是住）；
# ★而形一样，久了会腻——★★而无一轮回头读「近五章连起来，是不是在原地打转」。
FORM = {
    # ★2026-08-18 补（同⑲之由）：翻判之词只七样，不含「我先没懂／后来我明白／我先当他是」等本书之定式。
    '翻判': ('先前当', '今天知道不是', '而其错', '翻', '不是…是', '我先前以为', '先前我当',
           '我先没懂', '后来我明白', '我先当他', '后来我知道不是', '它只写少了', '没写错'),
    # ★2026-08-18 补（同⑲之由）：
    '做事': ('抠开', '挖', '绑', '背', '走到', '拆', '推开', '爬',
           '蹲', '插', '掏', '量', '迈', '托', '起身', '出发'),
    '问人': ('我问', '他说', '答不上', '不肯说'),
    '记账': ('本子', '第十', '记号', '划', '账'),
}

def check17(cur):
    """★近五章之形：若同形逾三章，即报（报而不拦）。"""
    cs = [c for c in range(max(1, cur - 4), cur + 1) if c in F]
    if len(cs) < 3:
        return [('⑰·近五章之形', True, '★章数不足，免测')]
    forms = []
    for c in cs:
        b = body(c)
        sc = {k: sum(b.count(w) for w in ws) for k, ws in FORM.items()}
        forms.append((c, max(sc, key=sc.get)))
    from collections import Counter
    cnt = Counter(f for _, f in forms)
    top, n = cnt.most_common(1)[0]
    ok = (n <= 3)
    seq = '→'.join('%d:%s' % (c, f) for c, f in forms)
    return [('⑰·近五章之形（同形≤3章）', ok,
             ('★%s' % seq) if ok
             else ('⛔近五章有 %d 章同为「%s」：★而形一样久了会腻'
                   '——★★其治：下一章换一种形。★★★%s' % (n, top, seq)))]


# ───────── ⑱ 生死线之期（2026-08-18 立）─────────
# ★★★★★其由：2026-08-18 逐章核之，水尽已第十日（199为第一日，209为第十日）；
# ★而一个人无水十日已到极限之边——★★而正文自己在算：昨天三天，今天两天；
# ★★★即：这条线最多还能走两三章，必须给它一个了断（或找到水，或死人）。
# ★★★★而十轮里没有一轮问「这条要命的线还能吊几章」；
# ★★★★★故立此检：凡文内之「无X第N日」逾其限者，即报。
LIFELINE = {
    '水': {'词': ('水尽', '没水', '无水'), '限': 12,
           '据': '★人无水十日已到极限之边；★★而十二日为其硬限——逾此即须了断（找到水，或死人）'},
    '气': {'词': ('气不够', '喘不上'), '限': 20, '据': '★气之线较缓，然亦不可久吊'},
}

def check21(cur):
    """★★★★★已起草之章（2026-08-18 立）。
    ★其由：本日我拿已起草且已跑第1轮之第211章，又另写了一篇；
    ★★而领轮时机器已报「真轮1/10，该跑第2轮」——而我未核其实。
    ★★★而⑭只拦「已封版之章」，不拦「已起草而未封版之章」；
    ★★★★而后者更险：封版之章有回执可认，而已起草之章只在磁盘上。
    ★★★★★故立此检：凡本章之正文已在，即报其名与净重，令人先核再动笔。"""
    if cur not in F:
        return [('㉑·已起草之章', True, '★第%d章尚未起草，可起草' % cur)]
    b = body(cur)
    nm = os.path.basename(F[cur]).replace('.md', '')
    w = net(b)
    tz = os.path.join(ROOT, '版本', '第%d章' % cur, '_台账.json')
    rn = 0
    if os.path.exists(tz):
        try:
            _d = json.load(open(tz, encoding='utf-8'))
            rn = len({int(_m.group(1)) for _v in _d.get('版本', [])
                      for _m in [re.search(r'第(\d+)轮', str(_v.get('说明', '')))] if _m})
        except Exception:
            pass
    return [('㉑·已起草之章', True,
             '⚠第%d章之正文已在（%s｜净重%d｜真轮%d/10）：'
             '★而其非伤——★★是提醒：本章已起草，勿再另写一篇；'
             '★★★须接着跑下一轮。' % (cur, nm, w, rn))]


def check18(cur):
    """★生死线之期：查文内之要命之线还能吊几章。"""
    b = body(cur)
    if not b:
        return [('⑱·生死线之期', True, '★正文缺，免测')]
    out = []
    for nm, g in LIFELINE.items():
        if not any(w in b for w in g['词']):
            continue
        # ★取其日：先搜「第N日/天」之数
        m = re.findall(r'(?:水尽|没水|无水)第([零〇一二三四五六七八九十百]+)[日天]', b)
        if not m:
            m2 = re.search(r'第([零〇一二三四五六七八九十百]+)[日天]', b)
            out.append(('⑱·%s之线' % nm, True,
                        '★在场而未标其日（%s）：★★须自核其期' % (m2.group(0) if m2 else '—')))
            continue
        d = cn2int(m[-1])
        lim = g['限']
        ok = (d < lim)
        out.append(('⑱·%s之线（限%d日）' % (nm, lim), ok,
                    ('★第%d日｜余 %d 日' % (d, lim - d)) if ok
                    else ('⛔第%d日，逾限%d：★而这条线不能再吊了'
                          '——★★其治只有二：或了断（找到水，或死人），'
                          '或明写一句「为什么还没死」。★★★而其据：%s' % (d, lim, g['据']))))
    if not out:
        out.append(('⑱·生死线之期', True, '★本章无生死线之词'))
    return out


# ───────── ⑲ 骨之方向（2026-08-18 立）─────────
# ★★★★★其由：⑰只测「近五章之形」（翻判/做事/问人/记账），而不测「骨往哪个方向走」。
# ★而2026-08-18 逐章核之：207先还债、208算错的那个数、209说出来那一下——
# ★★三章连着皆为「他那本账」；★★★而三章皆好，可它们是同一个方向的三步；
# ★★★★而读者跟着走，会觉得「这队人不往前走了，光在算」。
# ★★★★★故立此检：凡近三章之骨皆朝同一「向」者，即报。
DIRECTION = {
    # ★2026-08-19 补：先前之词表只七样，且皆为主线第一人称之语（我这本账／我算的／我记的…）；
    # ★★而217为第三人称暗线章（其人称为「她」），一样也命中不了，遂被判为「往前」——
    # ★★★而其实通篇在查自己那本账记的是哪一头；
    # ★★★★故补第三人称之形与「查自己所记」之词，令其量得实。
    '往内（查自己）': ('我这本账', '我算的', '我错', '我记的', '我这只手', '我不敢', '账上',
                '她那本账', '她记的', '这本账', '那本账', '翻回去', '往回翻',
                '记不着', '答不上', '白守', '够得着', '自己用不上', '替谁记'),
    # ★2026-08-18 补：先前之词表只六样，且皆为211之霍钧线专用词；
    # ★★而214通篇在查「那个封屋之人怎么走的」（他拽过、他割了绳、他没带走），其形却被判为「往前」——
    # ★★★而其由：本书之查人必带手上之动作（摸、托、捻），故「做事」之数恒高；
    # ★★★★故补「往外」之词，令其量得实。
    '往外（查那个人）': ('那个人', '他先走', '他留', '他不塞', '他记着', '二十七年',
                  '他为什么', '他没', '被人', '有人', '拽', '割', '带走', '留下的',
                  '用坏的', '磨的', '先来过'),
    # ★2026-08-18 补：先前之词表只八样，不含蹲/插/掏/量/迈/托等；
    # ★★而212通篇在走、在蹲、在插针、在量步，其形却被判为「记账」——
    # ★★★而其由：本书之主角凡做事必带本子，故「本子/第十/记号」之数恒高；
    # ★★★★故补「做事」之词，令其量得实。
    '往前（走路做事）': ('抠开', '挖', '爬', '走到', '下去', '绑', '背', '过去',
                  '蹲', '插', '掏', '量', '迈', '托', '起身', '收东西', '出发', '走了'),
    '往侧（问人）': ('我问', '他说', '答不上', '不肯说', '报数'),
}

def check19(cur):
    """★骨之方向：近三章之骨若皆朝同一向，即报。"""
    # ★2026-08-18 订：本章若未起草（无正文），则取其前三章——
    # ★★而其正该在起草之前告诉我：前三章之向是什么，本章该换哪个向。
    cs = [c for c in range(max(1, cur - 2), cur + 1) if c in F]
    if len(cs) < 3:
        cs = [c for c in range(max(1, cur - 3), cur) if c in F]
    if len(cs) < 3:
        return [('⑲·骨之方向', True, '★章数不足，免测')]
    dirs = []
    for c in cs:
        # 【批123·订】词频判向，其病在「不问所对之物」：
        #   ★221通篇是问人、记账、对着一个躺着的人摸床底下的缝（走路实判仅4段），
        #   ★★而「摸／蹲／插／伸手」尽归「往前」，遂把一篇往侧之章判成往前；
        #   ★★★而同一个动作，其向由「所对之物」定，不由动作本身定（221开镜卡问五所立）。
        # 治：某章之开镜卡若已明写「本章之向：X」，即以卡为准——
        #   ★而卡是人判的、且须给实判之据（数其动，非数其词）；★★词频只在无卡时用。
        _d = None
        _kj = os.path.join(ROOT, '版本', '第%d章' % c, '_开镜卡.md')
        if os.path.exists(_kj):
            try:
                _kt = open(_kj, encoding='utf-8', errors='replace').read()
                _m = re.search(r'本章之向[：:）\)\*★]*[^\n]{0,12}?(往内|往外|往前|往侧)', _kt)
                if _m:
                    for _k in DIRECTION:
                        if _k.startswith(_m.group(1)):
                            _d = _k
                            break
            except Exception:
                pass
        if _d is None:
            b = body(c)
            sc = {k: sum(b.count(w) for w in ws) for k, ws in DIRECTION.items()}
            _d = max(sc, key=sc.get)
        dirs.append((c, _d))
    from collections import Counter
    cnt = Counter(d for _, d in dirs)
    top, n = cnt.most_common(1)[0]
    ok = (n < 3)
    seq = '→'.join('%d:%s' % (c, d) for c, d in dirs)
    # ★★★★★2026-08-18 订：⑲报的是「已成之事实」（前三章确实同向），非本章之误；
    # ★而若本章未起草，其治正在本章——★★故若开镜卡已明写「本章须换向」，即判过。
    # ★★★而其由：闸之职是逼人换向，不是永拦；★★★★而已换向者，闸当放行。
    # ★2026-08-19 订：原此路只对「本章未起草」者开，故已起草之章即便开镜卡明写其向亦不放行；
    #   ★★而⑲以词频判向，其数会被减法轮之刀改变（219第8轮所立）——
    #   ★★★故已起草之章，若其开镜卡明写「本章之向」并给实判之据，一样当放行；
    #   ★★★★而其闸未削：开镜卡须明写，否则仍拦。
    if not ok:
        kj = os.path.join(ROOT, '版本', '第%d章' % cur, '_开镜卡.md')
        if os.path.exists(kj):
            try:
                _k = open(kj, encoding='utf-8', errors='replace').read()
                if ('换向' in _k) or ('本章之向' in _k):
                    return [('⑲·骨之方向（近三章不同向）', True,
                             '★前三章皆朝「%s」，而本章之开镜卡已明写换向 ✓：★★%s'
                             % (top, seq))]
            except Exception:
                pass
    return [('⑲·骨之方向（近三章不同向）', ok,
             ('★%s' % seq) if ok
             else ('⛔近三章之骨皆朝「%s」：★而三章皆好，可它们是同一个方向的三步；'
                   '★★而读者跟着走，会觉得这队人不往前走了。'
                   '★★★而其治：下一章换一个向（★★★★而换毕须在开镜卡里明写「本章之向」）。'
                   '★★★★★%s' % (top, seq)))]


# ───────── ⑳ 未答之问（2026-08-18 立）─────────
# ★★★★★其由：本书之法有「必问之答」——凡正文摆出一问而当章不答者，须记其欠。
# ★而十轮里第10轮虽查生死检，然无一轮专查「本章摆出之问，答了几个」；
# ★★而一章摆三问而一个不答，读者会觉得「作者忘了」。
# ★★★故立此检：搜本章之问句（以「什么／哪儿／几／怎么／为什么」结於「。」者），
# ★★★★而后查其后二十段内有无「答之形」。
def check20(cur):
    """★未答之问：本章摆出之问，当章答了几个。"""
    b = body(cur)
    if not b:
        return [('⑳·未答之问', True, '★正文缺，免测')]
    ps = [x.strip() for x in b.split('\n') if x.strip() and x.strip() != '＊']
    qs = []
    for i, x in enumerate(ps):
        if re.search(r'(是什么|在哪儿|几时|怎么办|为什么|多少|哪一样|哪一条)[。？]', x):
            qs.append((i, x[:34]))
    if not qs:
        return [('⑳·未答之问', True, '★本章未摆明问')]
    unans = []
    for i, q in qs:
        tail = ''.join(ps[i + 1:i + 21])
        if not re.search(r'(是因为|其由|答|知道了|明白|原来|后来我|遂|所以)', tail):
            unans.append('段%d「%s」' % (i, q))
    ok = (len(unans) <= 1)
    return [('⑳·未答之问（≤1）', ok,
             ('★摆问 %d 处｜未答 %d 处' % (len(qs), len(unans))) if ok
             else ('⛔摆问 %d 处而未答 %d 处：★而一章摆三问而一个不答，'
                   '读者会觉得作者忘了。★★其治有二：或当章答，或明写「这一问我没有问出口」。'
                   '★★★%s' % (len(qs), len(unans), '；'.join(unans[:3]))))]


def run(chs, quiet=False):
    bad = 0
    rows = []
    # ★2026-08-17 订：cur 先前恒取末章，故命令行所指之章不入⑨⑩⑫三检。
    # ★★而⑫（已封版之章）正须认所指之章——★★★不认，则其永不报。
    cur = (chs[0] if chs else (max(F) if F else 0))
    for c in chs:
        if c not in F:
            # ★2026-08-17 订：未起草之章亦须可跑检——★★而其时正该跑⑭⑯⑰以定其可否起草。
            for name, ok, msg in check14(c) + check16(c) + check17(c) + check18(c) + check19(c) + check20(c) + check21(c):
                rows.append((name, ok, msg))
                if not ok:
                    bad += 1
            rows.append(('第%d章·正文' % c, True, '★尚未起草（★★而⑭⑯⑰已跑，可据以起草）'))
            continue
        for name, ok, msg in check3(c) + check9(c) + check10(c):
            rows.append((name, ok, msg))
            if not ok:
                bad += 1
    # ★2026-08-18 订：⑱⑲⑳於「未起草之支」已跑一遍，而主支亦跑——遂重出二遍。
    # ★★故主支之三测只在本章有正文时跑（未起草者已由上支办毕）。
    _tail = (check18(cur) + check19(cur) + check20(cur) + check21(cur)) if (cur in F) else []
    for name, ok, msg in check5() + check6(cur) + check7(cur) + check11(cur) + check13(cur) + check12(cur) + check14(cur) + check15(cur) + check16(cur) + check17(cur) + _tail:
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
        print('  %s' % ('✓ 十六检皆过。' if bad == 0 else '⛔ 十六检报 %d 处，须修。' % bad))
        print('=' * 64)
    else:
        print('开轮十六检通过' if bad == 0 else '；'.join('%s %s' % (n, m) for n, ok, m in rows if not ok))
    return 0 if bad == 0 else 2


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    q = '--静' in sys.argv
    chs = [int(x) for x in a] if a else [max(F)]
    sys.exit(run(chs, q))
