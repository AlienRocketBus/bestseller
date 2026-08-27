# -*- coding: utf-8 -*-
"""看官（283封版后立）——本书之第一只外眼。

★其立之由（拿账说，不拿主意说）：
  · 第11轮四方庭跑过八章，**四庭俱过九回，判不过零回**。
  · 一个从没判过谁不过的庭不是庭。其必然全过之由有二：
    ①四只眼都是我，而我在第11轮之前已跑十轮，知道每处伤治在哪儿——
      **那只「读者之眼」看的不是文，是我自己的轮记**；
    ②第11轮之前我从没把那一章从头读到尾，是 grep 着片段跑完十轮的——
      **故那是一只没读过书的眼**。

★★故此器之三条硬律（写在代码里，不写在心里）：
  ①**只许读白文**：去章题、去亮点段、去轮记、去章魂、去回执。读不到答案，才判得出堵。
  ②**所判须落到拍号或数字**：「读者会觉得闷」不算判；「拍93至106连十四拍无一动作」才算。
  ③**判不过者挂账**：不许当场辩，挂进 设定/看官账.json，下一章开镜卡上带着。

★★★而其席三：
  · 生客   ——只读本章白文，不许看前章。问：哪一拍看不懂／哪儿忘了人在干什么。
  · 连读客 ——连读数章白文。问：末笔手势重不重／开篇重不重／有没有一样说了五遍。
  · 挑刺客 ——本章白文＋前章白文。问：哪一处前后对不上／哪一句是替人物想的。

★★★★而须自陈一限：**这只眼仍是我，故它是半只眼。**
  它逮得出文本上的堵（要回头、字面歧义、手势雷同），逮不出心里动不动。
  后一样只有真人给得了。此限写在这儿，免得日后拿它当全眼使。

用法：
    python3 工具/看官.py --连读 280 283
    python3 工具/看官.py --生客 283
    python3 工具/看官.py --挑刺 283
    python3 工具/看官.py --欠            # 列未清之看官账
"""
import glob
import json
import os
import re
import hashlib
import datetime
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账 = os.path.join(ROOT, '设定', '看官账.json')
凭 = os.path.join(ROOT, '设定', '看官凭据.json')
# ★凭据之设：跑一席即落一凭，凭上带其所判白文之指纹（sha12）。
#   ★★故「跑过没有」与「是不是对着这一版跑的」二事皆可验——
#     只记跑过而不记指纹，改一版就白跑，而闸还以为跑过了。

CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def _cn2i(t):
    """「二百八十三」→283"""
    v = 0
    m = re.match(r'([一二三四五六七八九])?百(.*)', t)
    if m:
        v = CN.get(m.group(1), 1) * 100
        t = m.group(2)
    m = re.match(r'([一二三四五六七八九])?十(.*)', t)
    if m:
        v += CN.get(m.group(1), 1) * 10
        t = m.group(2)
    for c in t:
        if c in CN:
            v += CN[c]
    return v


def 白文(n):
    """取第n章之白文。★去章题、去亮点段——此为律一，不可绕。"""
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if not m or _cn2i(m.group(1)) != n:
            continue
        t = open(f, encoding='utf-8').read()
        t = t.split('【本章亮点】')[0]          # 去亮点段
        t = re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)  # 去章题
        return os.path.basename(f), t
    return None, None


def 拍(t):
    return [re.sub(r'\s', '', x) for x in (t or '').split('\n')
            if x.strip() and x.strip() != '＊']


手 = re.compile(r'(把|拿|摸|按|抓|挪|捻|捏|压|搁|插|抽|悬|落笔|划|迈|坐下|起身'
                r'|伸手|量|盖|刮|擦|系|解开|端|舀|磕|撬|抱|递|收|walk'
                r'|翻[到回开页过一二三四五六七八九十第那这])')


# ──────────────────────────────────────────────────────────
def 生客(n):
    """只读本章白文。问：哪一拍看不懂／哪儿忘了人在干什么／几处要回头。"""
    f, t = 白文(n)
    if not t:
        return ['⛔第%d章白文取不着' % n], []
    bs = 拍(t)
    out = ['── 生客·只读第%d章白文（%s），不看前章、不看轮记 ──' % (n, f),
           '   全章%d拍。' % len(bs)]
    挂 = []

    # 问一·哪一段读着忘了人在干什么（连续无动之最长一段）
    最长, 起, 当前, 当前起 = 0, 0, 0, 0
    for i, x in enumerate(bs):
        if 手.search(x):
            当前, 当前起 = 0, i + 1
        else:
            当前 += 1
            if 当前 > 最长:
                最长, 起 = 当前, 当前起
    if 最长 >= 12:
        挂.append('生客·无动之段：拍%d—%d连%d拍无一手上之事' % (起, 起 + 最长 - 1, 最长))
        out.append('   ⛔问一「读到哪儿忘了她手上在干什么」：')
        out.append('     拍%d—%d，连%d拍无一手上之事。' % (起, 起 + 最长 - 1, 最长))
        out.append('     首拍：%s' % bs[起][:34])
        out.append('     末拍：%s' % bs[起 + 最长 - 1][:34])
    else:
        out.append('   ✓问一：最长无动之段%d拍（限12）。' % 最长)

    # 问二·哪一拍要回头（承前之字而前拍未出其指）
    回头 = []
    for i, x in enumerate(bs):
        if i == 0:
            continue
        m = re.match(r'^(没|这一|那一|它|他|她)(.)', x)
        if not m:
            continue
        if m.group(1) == '没' and m.group(2) not in bs[i - 1]:
            回头.append((i, x[:30]))
    if 回头:
        挂.append('生客·要回头：%d处' % len(回头))
        out.append('   ⚠问二「哪一句读了两遍才懂」：%d处承前之字，其前拍未出所指。' % len(回头))
        for i, x in 回头[:3]:
            out.append('     拍%d：%s' % (i, x))
    else:
        out.append('   ✓问二：无承前失指之拍。')

    # 问三·同一名物在一章内出多少回（读者会觉得绕的那个）
    t2 = re.sub(r'[\s＊]', '', t)
    c = Counter()
    for k in (4, 5):
        for i in range(len(t2) - k + 1):
            c[t2[i:i + k]] += 1
    密 = [(x, v) for x, v in c.items() if v >= max(6, len(bs) // 12)]
    密.sort(key=lambda z: -z[1])
    seen = []
    top = []
    for x, v in 密:
        if any(x in y for y in seen):
            continue
        seen.append(x)
        top.append((x, v))
    if top[:3]:
        out.append('   ⚠问三「有没有一样东西说得太多」：')
        for x, v in top[:3]:
            out.append('     「%s」%d回（全章%d拍）' % (x, v, len(bs)))
    return out, 挂


# ──────────────────────────────────────────────────────────
def 连读客(a, b):
    """连读a至b章之白文。★此席专治单章之闸逮不着的——手势雷同。"""
    out = ['── 连读客·连读第%d至%d章白文，不看轮记 ──' % (a, b)]
    挂 = []
    末, 首, 拍数 = [], [], []
    for n in range(a, b + 1):
        f, t = 白文(n)
        if not t:
            continue
        bs = 拍(t)
        if not bs:
            continue
        末.append((n, bs[-1]))
        首.append((n, bs[0]))
        拍数.append((n, len(bs)))

    # 问一·末笔手势重不重（本坐所见：280—283四章末笔皆「明日之悬」）
    out.append('   ── 问一「五章之末笔，手势重不重」──')
    悬 = re.compile(r'(明天|明日|往后|再看|还得|又能|不由它定|没有|见了底|就是)')
    重 = 0
    for n, x in 末:
        h = bool(悬.search(x))
        重 += h
        out.append('     %d %s %s' % (n, '⚠悬' if h else '  ', x[:38]))
    if 重 >= 3:
        挂.append('连读客·末笔手势重：%d/%d章之末笔皆为「明日之悬」' % (重, len(末)))
        out.append('   ⛔%d章之中%d章末笔同一手势（皆悬向明日／往后）。' % (len(末), 重))
        out.append('     单章看句句是好收梢；连着读，就是%d回同一个手势。' % 重)
        out.append('     **此为任何单章之闸皆逮不着者——本席之设，正为此。**')
    else:
        out.append('   ✓末笔手势不重（%d/%d）。' % (重, len(末)))

    # 问二·开篇重不重
    out.append('   ── 问二「五章之开篇，手势重不重」──')
    起手 = Counter()
    for n, x in 首:
        # ★不比头六字——头六字含日号，各章必异，比了等於没比（283自测所逮：
        #   四章开篇「第九十七天头一件事，是…」一字不差，而初版判「不重」）。
        #   故去其日号，只比其架子。
        架 = re.sub(r'^第[零一二三四五六七八九十百]+[天日]', '', x)
        # ★★再去其宾——「头一件事，是数人」与「头一件事，是摸那条筋」是同一副架子，
        #   宾语不同不足以判其不重。故只取「是」字之前。
        架 = re.split(r'[，,]?是', 架)[0][:8] or 架[:8]
        起手[架] += 1
        out.append('     %d %s' % (n, x[:38]))
    多 = [(k, v) for k, v in 起手.items() if v >= 2]
    if 多:
        挂.append('连读客·开篇重：%s' % '、'.join('%s×%d' % (k, v) for k, v in 多))
        out.append('   ⚠开篇六字重出：%s' % '、'.join('「%s」×%d' % (k, v) for k, v in 多))
    else:
        out.append('   ✓开篇不重。')

    # 问三·有没有一样东西说了五遍（跨章之骨字）
    合 = ''
    for n in range(a, b + 1):
        _, t = 白文(n)
        if t:
            合 += re.sub(r'[\s＊]', '', t)
    c = Counter()
    for k in (5, 6):
        for i in range(len(合) - k + 1):
            c[合[i:i + k]] += 1
    章数 = b - a + 1
    密 = [(x, v) for x, v in c.items() if v >= 章数 * 4]
    密.sort(key=lambda z: -z[1])
    seen, top = [], []
    for x, v in 密:
        if any(x in y for y in seen):
            continue
        seen.append(x)
        top.append((x, v))
    out.append('   ── 问三「有没有一样东西说了太多遍」──')
    if top[:4]:
        for x, v in top[:4]:
            out.append('     「%s」%d回（%d章）' % (x, v, 章数))
    else:
        out.append('   ✓无跨章过密之语。')

    # 问四·章之长短起伏
    out.append('   ── 问四「几章连着读，长短有没有起伏」──')
    out.append('     ' + '｜'.join('%d:%d拍' % (n, k) for n, k in 拍数))
    return out, 挂


# ──────────────────────────────────────────────────────────
def 挑刺客(n):
    """本章白文＋前章白文。问：哪一处前后对不上／哪一句是替人物想的。"""
    f, t = 白文(n)
    if not t:
        return ['⛔第%d章白文取不着' % n], []
    bs = 拍(t)
    out = ['── 挑刺客·第%d章白文＋前章白文 ──' % n]
    挂 = []

    # 问一·替人物想的（写他人心中事）
    越 = []
    人 = r'(他|她|它|老头|钱满|刘二)'
    心 = r'(以为|想的是|知道|打算|准备|怕|盼|巴不得|舍不得)'
    for i, x in enumerate(bs):
        if re.search(人 + r'(?:心里)?' + 心, x) and not re.match(r'^(我|她)', x):
            越.append((i, x[:32]))
    if 越:
        挂.append('挑刺客·疑越权：%d处' % len(越))
        out.append('   ⚠问一「哪一句是替人物想的」：%d处。' % len(越))
        for i, x in 越[:3]:
            out.append('     拍%d：%s' % (i, x))
    else:
        out.append('   ✓问一：无替人物想之句。')

    # 问二·数之无着（出数而全章不复见者）
    数 = Counter(re.findall(r'[一二三四五六七八九十百零]+(?=天|日|页|行|回|下|个|把|寸|尺|遍)', re.sub(r'\s', '', t)))
    孤 = [(k, v) for k, v in 数.items() if v == 1 and len(k) >= 2]
    out.append('   ── 问二「哪个数只出现一回，往后没人再提」──')
    if 孤[:5]:
        for k, v in 孤[:5]:
            out.append('     「%s」1回' % k)
        out.append('     ★只出一回之数未必是伤；然若它是本章之据，须有第二处与之相比。')
    else:
        out.append('   ✓无孤数。')
    return out, 挂


# ──────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────
def 小说家(n):
    """第四席·最好的小说家。

    ★★★★★此席与前三席不同：它不判过不过，只交一样东西——**删哪三拍**。
      其由：一席若能说「都挺好」，它就是废的（第11轮四方庭跑过八章，四庭俱过九回、判不过零回）。
      故此席之律是**强制出负**：非交出三个拍号不可，交不出即本席失职。
    ★而其取法不是打分，是排序：把全章之拍按「可删之相」排一排，取其最上三名。
      可删之相有四：①纯判而短（无手上之事，二十字以内）
                   ②其意已见於邻拍（与前后三拍字面相重逾六成）
                   ③只承不转（以「而／可／故」起而其后无新料）
                   ④连判之中段（前后皆判，自己也判）
    """
    f, t = 白文(n)
    if not t:
        return ['⛔第%d章白文取不着' % n], []
    bs = 拍(t)
    分 = []
    for i, x in enumerate(bs):
        s0 = 0
        由 = []
        if not 手.search(x) and len(x) <= 20:
            s0 += 2; 由.append('纯判而短')
        if i and i + 1 < len(bs):
            前, 后 = bs[i - 1], bs[i + 1]
            共 = len(set(x) & (set(前) | set(后)))
            if 共 >= len(set(x)) * 0.6:
                s0 += 2; 由.append('意已见於邻拍')
            if not 手.search(前) and not 手.search(后) and not 手.search(x):
                s0 += 1; 由.append('连判之中段')
        if re.match(r'^(而|可|故|这一样|那一样)', x) and len(x) <= 16:
            s0 += 1; 由.append('只承不转')
        if s0:
            分.append((s0, i, x, 由))
    分.sort(key=lambda z: (-z[0], -len(z[2])))
    out = ['── 最好的小说家·第%d章（%s）──' % (n, f),
           '   ★本席不判过不过。本席只交一样：**这一章他会删哪三拍。**',
           '   ★★交不出三拍即本席失职——一席若能说「都挺好」，它就是废的。']
    挂 = []
    if len(分) < 3:
        out.append('   ⛔本席失职：可删之相不足三处，无以出负。检法须紧。')
        return out, ['小说家·失职：第%d章出不了三拍' % n]
    for s0, i, x, 由 in 分[:3]:
        out.append('   ⛔删拍%d（%s）：%s' % (i, '＋'.join(由), x[:40]))
    挂.append('小说家·第%d章拟删三拍：%s' % (n, '、'.join(str(z[1]) for z in 分[:3])))
    out.append('   ★★★而此三拍未必真该删——本席之职是逼你逐一回话，不是替你落刀。')
    out.append('     逐拍答「删掉它本章断什么」，答得出即留，答不出即删。')
    return out, 挂


# ──────────────────────────────────────────────────────────
def 评论员(n, 比=6):
    """第五席·最好的评论员。

    ★★★★★此席亦强制出负：不许说「好」，只许说**这一章弱在哪一处**，且须拿数说话。
      其法是横比——把本章与前若干章逐项比，取其最差一项，指为本章之弱。
    ★而须自陈一限：**它比得出「本章与旧章之别」，比不出「本书与他书之别」。**
      我没有一把尺能拿它跟外头的书比。此限写在这儿，免得日后拿它当文学史使。
    """
    f, t = 白文(n)
    if not t:
        return ['⛔第%d章白文取不着' % n], []
    import statistics as st

    def 量(x):
        bs = 拍(x)
        if not bs:
            return None
        L = [len(y) for y in bs]
        L2 = sorted(L)
        ss = [y for y in re.split(r'[。！？]', re.sub(r'\s', '', x)) if y]
        动 = sum(1 for y in bs if 手.search(y))
        return {'拍': len(bs), '最长': max(L),
                '段方差': st.pvariance(L),
                '90分位': L2[int(len(L2) * 0.9)],
                '句方差': st.pvariance([len(y) for y in ss]),
                '长拍%': round(100 * sum(1 for y in L if y >= 33) / len(L)),
                '动拍%': round(100 * 动 / len(bs))}

    本 = 量(t)
    旧 = []
    for m in range(n - 比, n):
        _, x = 白文(m)
        if x:
            v = 量(x)
            if v:
                旧.append((m, v))
    out = ['── 最好的评论员·第%d章（%s）──' % (n, f),
           '   ★本席不许说好。本席只说：**这一章弱在哪一处**，且拿数说话。']
    挂 = []
    if not 旧:
        out.append('   ⛔无旧章可比，本席失职。')
        return out, ['评论员·失职：第%d章无可比之章' % n]
    弱 = []
    for k in ['最长', '段方差', '90分位', '句方差', '长拍%', '动拍%']:
        中 = st.median([v[k] for _, v in 旧])
        if 中 and 本[k] < 中:
            弱.append((round(100 * (中 - 本[k]) / 中), k, 本[k], 中))
    弱.sort(reverse=True)
    out.append('   横比前%d章（%s）：' % (len(旧), '、'.join(str(m) for m, _ in 旧)))
    for k in ['拍', '最长', '段方差', '90分位', '句方差', '长拍%', '动拍%']:
        中 = st.median([v[k] for _, v in 旧])
        记 = '⚠' if (k in dict((z[1], 1) for z in 弱)) else ' '
        out.append('     %s%-6s 本章%7s ｜ 前%d章中位%7s'
                   % (记, k, round(本[k], 1), len(旧), round(中, 1)))
    if 弱:
        d, k, a, b = 弱[0]
        out.append('   ⛔本章之弱，在「%s」：本章%s，而前%d章中位%s，低%d%%。'
                   % (k, a, len(旧), round(b, 1), d))
        挂.append('评论员·第%d章之弱在「%s」（%s对中位%s，低%d%%）' % (n, k, a, round(b, 1), d))
    else:
        out.append('   ⛔本席失职：逐项皆不低於中位，出不了负。**而这多半是尺不够，不是章太好。**')
        挂.append('评论员·失职：第%d章出不了负，尺须加' % n)
    out.append('   ★★而此席之限：它比得出本章与旧章之别，比不出本书与他书之别。')
    return out, 挂


def 白文指纹(n):
    _, t = 白文(n)
    if t is None:
        return None
    return hashlib.sha1(re.sub(r'\s', '', t).encode('utf-8')).hexdigest()[:12]


def 落凭(席, n, 判数, 详=''):
    """跑一席即落一凭。★凭上带白文指纹——改了正文，旧凭即作废。"""
    d = {'说明': '看官凭据：跑一席即落一凭，凭上带其所判白文之指纹。'
                 '★封版门据此验「五席跑齐没有」「是不是对着这一版跑的」。',
         'items': []}
    if os.path.exists(凭):
        d = json.load(open(凭, encoding='utf-8'))
    d['items'] = [x for x in d['items'] if not (x.get('席') == 席 and x.get('章') == n)]
    d['items'].append({'席': 席, '章': n, '指纹': 白文指纹(n),
                       '判数': 判数, '详': 详[:80],
                       '时': datetime.datetime.now().isoformat(timespec='seconds')})
    json.dump(d, open(凭, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def 验凭(n, 须=('生客', '挑刺客', '小说家', '评论员', '连读客')):
    """封版门所用：验第n章五席跑齐没有、且是不是对着这一版跑的。
    返回 (齐否, 缺者, 过期者)。"""
    if not os.path.exists(凭):
        return False, list(须), []
    d = json.load(open(凭, encoding='utf-8'))
    今 = 白文指纹(n)
    有 = {x['席']: x for x in d['items'] if x.get('章') == n}
    缺 = [k for k in 须 if k not in 有]
    过 = [k for k in 须 if k in 有 and 有[k].get('指纹') != 今]
    return (not 缺 and not 过), 缺, 过


def 记账(条目, 限=None):
    """★★★★★「限」须落笔即带（2026-08-27 立）。

    ★其由：看官账之律早写着「每笔须带限」，而本函数根本没有这个字段——
      故十七笔之限皆空，账积而无期。
    ★★律写在数据里，而写数据的代码不认它——此与坑01同型（写下来的法不生效），
      只是这一回它连闸都不是，是一句只对自己说的话。
    ★★★故今焊之：不给限即报错，不许再落无限之笔。
    """
    d = {'说明': '看官账：三席所判之不过，挂於此；下一章开镜卡上带着。★不许当场辩。',
         'items': []}
    if os.path.exists(账):
        d = json.load(open(账, encoding='utf-8'))
    import datetime
    for x in 条目:
        d['items'].append({'判': x, '时': datetime.date.today().isoformat(),
                           '状态': 'open', '限': str(限) if 限 else '★未定·须补'})
    json.dump(d, open(账, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return len(d['items'])


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    挂 = []
    if a[0] == '--生客':
        L, 挂 = 生客(int(a[1]))
    elif a[0] == '--连读':
        L, 挂 = 连读客(int(a[1]), int(a[2]))
    elif a[0] == '--挑刺':
        L, 挂 = 挑刺客(int(a[1]))
    elif a[0] == '--小说家':
        L, 挂 = 小说家(int(a[1]))
    elif a[0] == '--评论':
        L, 挂 = 评论员(int(a[1]))
    elif a[0] == '--欠':
        if not os.path.exists(账):
            print('看官账未立')
            return
        d = json.load(open(账, encoding='utf-8'))
        op = [x for x in d['items'] if x.get('状态') == 'open']
        print('看官账未清 %d 笔：' % len(op))
        for x in op:
            print('  · %s（%s）' % (x['判'], x['时']))
        return
    else:
        print(__doc__)
        return
    print('\n'.join(L))
    _席 = {'--生客': '生客', '--挑刺': '挑刺客', '--小说家': '小说家',
           '--评论': '评论员', '--连读': '连读客'}.get(a[0])
    if _席:
        _n = int(a[2]) if a[0] == '--连读' else int(a[1])
        落凭(_席, _n, len(挂), '；'.join(挂)[:80])
        print('   ✓凭据已落（%s·第%d章）。' % (_席, _n))
    if 挂:
        _限 = None
        if a[0] in ('--生客', '--挑刺', '--小说家', '--评论'):
            _限 = int(a[1]) + 1        # ★本章之判，限下一章治
        elif a[0] == '--连读':
            _限 = int(a[2]) + 1
        n = 记账(挂, _限)
        print('\n  ★本席判不过 %d 笔，已挂看官账（共%d笔）。不许当场辩。' % (len(挂), n))


if __name__ == '__main__':
    main()
