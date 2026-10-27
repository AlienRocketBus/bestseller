# -*- coding: utf-8 -*-
"""大审闸（2026-09-02·作者令所立）

★**作者令（逐字）**：「**这个小说应该平均10章就应该从头到尾我们来进行一个剧情和质量
  等等各个方面严格把控，看看有没有达到一个最高等级**……**站在普通读者的视角，站在一个
  最顶尖小说家的视角，站在一个评委的视角，站在一个编辑的视角，站在一个普通小说爱好者
  的这么一个视角**……**不要说只有一个小说家，你可以用好几个小说家。**」

★★**而立此闸之前，先把「为什么现有的看官五席不够」写死在这里**（2026-09-02 九席审读之实）：
  ①**五席之输入是同一样东西**——`白文(n)` 的字符流加一张手写动词表加对它的计数；
    ★**四席吃同一份输入，於是四席是同一次测量的四个样本，不是四只眼**；
    ★★**唯一产出过真发现的是连读客（289/291开篇重出），而它正是唯一输入不同的那一席（多章）**。
  ②**必响之器不携带信息**：小说家（`if len(分)<3` 强制交三拍）与评论员（七项对中位，
    低者即「弱」，54章里52章出得了负）——**一个从不判谁不过的庭不是庭，而一个必然要响的器，
    响的时候不携带任何信息**。
  ③**回路没闭**：账 105 笔、93 笔未清（88.6%），`记账()` 无去重（今已焊），
    **只有产方没有收方**；**往一个消费端已饱和的系统里加生产端，加出来的只有积压**。
★★★**故此闸之律有三，缺一即不许开审**：
  · **甲·一席要占位，须说得出「它看得见而现有各席都看不见的那一样是什么」**
    （连读客说得出：多章；第二个小说家说不出）；
  · **乙·不强制出负，强制留痕**——**一席被逼着说「我在拍47停了一下，因为X」，
    这句话不论是不是伤都是信息；「非删三拍不可」不是**；
  · **丙·每一笔判须落到拍号或逐字引用之原句**，且须逐笔落「治／驳／挂」，不许只挂。

★★★★**而此器不读小说，也不判小说**——**它只管一件事：到十章了没有，上一次大审在不在，
  其席够不够，其判有没有人收。** ★**真读的那一步只有人（或替人真读的第三方）做得了**，
  器不许替它签字（`看官.py` 自陈之限：「这只眼仍是我，故它是半只眼……逮不出心里动不动」）。

用法：
    python3 工具/大审.py            ← 报：距上次大审几章、该不该开、上次之判清了没有
    python3 工具/大审.py --闸        ← 只出判（供全测调用）
    python3 工具/大审.py --立 293    ← 造一份大审之册（其模在下）
    python3 工具/大审.py --包 398 407 ← 瘦式·零 token 先行：诸器之红＋十章白文＋已付之盲读、逻辑审 → 设定/_草/大审407/包.md
    python3 工具/大审.py --录 <runId> ← 瘦式·录册归器（X27）：自 journal 排册之一、二、三节，⛔一席抄档
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
每 = 10                      # ★作者令：平均十章一回
段齐起 = 410                 # ★1023 作者令「设计十章→写十章→审十章」：自 410 起大审与段同界（段＝381 起每十章，段末＝410、420……）


def 到期(末, 上):
    """→ 该审至之章（段末）或 None。410 起：末以前（含）最近之段末未审即到期（审 上+1—段末；⛔段中开审）；
    其前照旧「距上一回满十章」。旧逢 7 而审（387、397、407），与段错开三章——审出之病下一段之造读不到。"""
    if 末 >= 段齐起:
        应 = 380 + (末 - 380) // 10 * 10
        return 应 if 应 >= 段齐起 and 应 > 上 else None
    return 末 if 末 - 上 >= 每 else None
册目 = os.path.join(ROOT, '设定')

# ★席之表：其名·其所独见（甲律：说不出「独见」者不许占位）
# ★1023 瘦式（X51·裁_1021_省律 九）：十二席并作四席一裁——诸旧席之问俱并入其一，⛔丢问：
#   连读客←生客·冷起手、生客·三章空降、连读客、评委、类型读者、弃卷席；小说家←白描、繁复、结构、编辑；
#   逻辑闭环←立得住、主线、悬念账、复述（并孤钩之兑删）；人物←人物之审六席（读人物链＋十章）；裁←录册之判。
#   所废：二十余席各读十章（W50 约 $75）、录册一席抄档（$21）、驳席重读、认声盲测（去名之器 X25 随之去）。
席表 = [
    ('连读客', '十章连读之读者之眼——拖、腻、弃卷、钩；并冷起手、半路进来、评委、类型读者之问：唯一看得见「同一个意思说了几遍」与「读到第几拍合书」'),
    ('小说家', '白描、繁复、结构、编辑四路合一——独见「意思已尽而字还在」「看着克制其实是空」「哪一章是多的」「信息负担」'),
    ('逻辑闭环', '立得住、主线、悬念账、复述——对圣经、canon、全书记忆：独见「凑出来的因」「线丢」「开了几个结了几个」'),
    ('人物', '诸人合一席，读人物链（全程而薄）与十章——独见「人前後不一、智之降、关系之断」'),
    ('裁', '只读四席之报与上册逾限之笔，⛔重读十章——逐笔落裁，出口归造'),
]


def _末章():
    ns = []
    for f in os.listdir(os.path.join(ROOT, '正文')):
        m = re.search(r'第([零〇一二三四五六七八九十百]+)章', f)
        if not m:
            continue
        s, t, n = m.group(1), 0, 0
        d = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
             '六': 6, '七': 7, '八': 8, '九': 9}
        for ch in s:
            if ch in d:
                n = d[ch]
            elif ch == '十':
                t += (n or 1) * 10
                n = 0
            elif ch == '百':
                t += (n or 1) * 100
                n = 0
        ns.append(t + n)
    return max(ns) if ns else 0


def 空模子(路):
    """★2026-09-13 立：一份只造了没填过的册，不算一回大审。

    ⛔其事：`大审_至第313章.md` 与 `大审_至第323章.md` 二档皆 42 行、
    通篇 `第%d—%d章`、裁定表只一行「⛔待裁」——**是 `--立` 造出来的空模子**，
    而 319—327 九章之开镜卡与悬账逐章照抄「**大审停在第313章，已欠十五章**」，
    ★**实则 `大审_至第324章.md` 248 行、裁定表逐行有裁，大审真正停在 324。**
    ⛔**一句错的现况，抄了九章。**（机制体检账 ㊧）

    ★其判只两问，皆字面可数：**模子之记号还在**（`%d` 未被换掉）
    **或 裁定表一笔裁也没有**。
    """
    try:
        t = io.open(路, encoding='utf-8', errors='replace').read()
    except Exception:
        return True
    if '%d' in t:
        return True
    _sec = t.split('## 三·')[-1].split('\n## ')[0] if '## 三·' in t else ''
    for x in _sec.splitlines():
        if x.strip().startswith('|') and ('已治' in x or '判驳' in x
                                          or '判不治' in x or '已挂' in x):
            return False
    return True


def 诸册(含空=False):
    out = []
    for f in sorted(os.listdir(册目)):
        m = re.match(r'大审_至第(\d+)章\.md$', f)
        if m:
            路 = os.path.join(册目, f)
            if not 含空 and 空模子(路):
                continue
            out.append((int(m.group(1)), 路))
    return sorted(out)


def 账():
    末 = _末章()
    cs = 诸册()
    上 = cs[-1][0] if cs else 0
    距 = 末 - 上
    判 = []
    止 = 到期(末, 上)
    if 止:
        判.append('⛔大审到期（审 %d—%d；距上次 %d 章·410 起与段同界）——**该开一回大审**：'
                  '★其席须≥5且各说得出其「独见」；★★其判须逐笔落拍号；'
                  '★★★跑 python3 工具/大审.py --立 %d 造其册。' % (上 + 1, 止, 距, 止))
    # ★上一册之判有没有人收（丙律）
    if cs:
        t = io.open(cs[-1][1], encoding='utf-8', errors='replace').read()
        # ★【立闸当日即修】初版数的是§二里九席之原话（`· ⛔` 起手者，22条），
        #   ★★而§三之职正是把那些原话**并**成可裁之笔（今为9笔）——
        #     **拿并前之数去比并後之数，它永远差着**；
        #   ★★★故改数§三那张裁定表之行：**逐行须有一裁**（已治／判驳／判不治／已挂）。
        #   ★★★★而「已挂」须带其限（限N）方算一裁——**挂而无限，是把账搬个地方放着**。
        _sec = t.split('## 三·')[-1].split('\n## ')[0] if '## 三·' in t else ''
        _rows = [x for x in _sec.splitlines()
                 if x.strip().startswith('|') and x.count('|') >= 5
                 and not re.match(r'^\s*\|[\s\-:|]+\|\s*$', x)
                 and '判（席·题）' not in x]
        挂 = len(_rows)
        # ★★★★★2026-09-23·限359（本坐填「至第357章」一册时所逮）：**补两样真判之名。**
        #   ⛔**旧式只认四样**（已治／判驳／判不治／已挂＋限），**而一庭之上真会出的判不止四样**：
        #     ①**「半治·半驳」**——**一判之中取其半、驳其半**（如编辑席既指对了那一拍係第六次「空着」，
        #       而其「移末拍」之议会断掉四章之倒数）；②**「留痕·不裁」**——**一席自书「无致命之判」**，
        #       **其身无可裁，而⛔它须入册**（坑㉗所要的正是这一样：交白卷而说得出何以白）。
        #   ★**旧式之下，这两样各算一行「没人收」**，**於是本器逼着填册的人把它们改写成假的「已治」或「判驳」**——
        #     ⛔**一道闸若逼着人为过它而改判，那道闸就是在教人说谎**（④之五之律）。
        #   ⛔**而其口开得极窄**：**只认这两个整词，⛔不认单独一个「治」「驳」「挂」字**
        #     （⛔否则「⛔待裁」之模子里那一行也会被「裁」字放过去·同日负测④在守）。
        收 = len([x for x in _rows
                  if ('已治' in x or '判驳' in x or '判不治' in x
                      or '半治' in x or '留痕·不裁' in x
                      or ('已挂' in x and re.search(r'限\s*\d+', x)))])
        if 挂 and 收 < 挂:
            判.append('⛔上一册（至第%d章）裁定表 %d 行，而落了裁者只 %d 行——'
                      '**只有产方没有收方，账一成噪声，真的那几笔就没人看了**；'
                      '★而「已挂」须带其限方算一裁。'
                      % (cs[-1][0], 挂, 收))
        elif not 挂:
            判.append('⛔上一册（至第%d章）无裁定表——**逐席之判须并成可裁之笔**（丙律）。'
                      % cs[-1][0])
        # ★★★★★★2026-09-13 补第三问（本器自己欠的那一样）：
        #   ⛔**册上自书「『挂』不是把裁推开：它带着限，到期不裁即是逾期，器会报」**
        #   ——**而本器从来没有数过那个限到没到**：**它只问「已挂带没带一个数」。**
        #   ★**即一句写在册上的话，盘上没有一只手兑它**（本册 ㊚ 之同骨：**账断了一头**）；
        #   ★★**而这一路比那一路更难见**：**它不是报错了，是它从头到尾没在看。**
        #   ⛔**故补此问：凡「已挂·限N」而末章已过 N 者，当场报逾期。**
        逾 = []
        for x in _rows:
            if '已挂' not in x:
                continue
            # ⛔**立日即自栽一回**：头一版拿整行去找「限N」并取其最小
            #   ——**而一笔之「其由」那一格里常引着别的限**（0913 第11笔引 FS 之旧限 309），
            #   **於是它把别人的旧限当成了这一笔的限，当场报了一个假逾期。**
            #   ★**其治**：**一笔之限只认「已挂」所在那一格**（裁之格），⛔**其由之格一个数也不取**。
            _cells = [c for c in x.split('|') if '已挂' in c]
            ms = re.findall(r'限\s*(\d+)', _cells[0]) if _cells else []
            if not ms:
                continue
            lim = min(int(y) for y in ms)
            if 末 >= lim:
                号 = x.split('|')[1].strip() if x.count('|') > 1 else '?'
                逾.append((号, lim))
        if 逾:
            判.append('⛔上一册（至第%d章）之「已挂」逾限 %d 笔（今为第%d章）：%s'
                      '——**挂带着限，到期不裁即是逾期**；'
                      '★**其裁须当场下或当面改限，⛔不许静静顺延。**'
                      % (cs[-1][0], len(逾), 末,
                         '、'.join('第%s笔(限%d)' % (i, l) for i, l in 逾)))
    return 末, 上, 距, 判


def 限於(n):
    """★1016（394 逮：393 记席照 大问表 之印填 394 卡问七，⛔见大审册「已挂·限394」之 #23——开镜卡漏、封版必逾）：
    上一册§三里「已挂」之格其限（取最小，同上「逾」之读法）≤ n 之笔 → [(号, 限, 其行之要)]。"""
    cs = 诸册()
    if not cs:
        return []
    t = io.open(cs[-1][1], encoding='utf-8', errors='replace').read()
    _sec = t.split('## 三·')[-1].split('\n## ')[0] if '## 三·' in t else ''
    出 = []
    for x in _sec.splitlines():
        if not (x.strip().startswith('|') and x.count('|') >= 5 and '已挂' in x):
            continue
        _cells = [c for c in x.split('|') if '已挂' in c]
        ms = re.findall(r'限\s*(\d+)', _cells[0]) if _cells else []
        if ms and min(int(y) for y in ms) <= n:
            出.append((x.split('|')[1].strip(), min(int(y) for y in ms), re.sub(r'\s+', ' ', _cells[0]).strip()))   # ★1020：⛔截二百字（399 卡问七抄得半句·#47 截於「随改状态册钱满、东」）——卡须逐字抄其全裁
    return 出


def 立(n):
    p = os.path.join(册目, '大审_至第%d章.md' % n)
    if os.path.exists(p):
        print('★已在：%s' % p)
        return p
    lo = max(1, n - 每 + 1)
    io.open(p, 'w', encoding='utf-8').write(
        ('# 大审 · 至第%d章（第%d—%d章）\n\n' % (n, lo, n)) +  # ★0925 逮：此行原无 % 代入，册首印出「%d」字样
        '> **★作者令**：「平均10章就应该从头到尾进行一个剧情和质量各个方面严格把控。」\n'
        '> **★★而此册之律三**（`工具/大审.py` 头所载）：\n'
        '> **甲**·一席要占位，须说得出「它看得见而现有各席都看不见的那一样是什么」；\n'
        '> **乙**·不强制出负，**强制留痕**；\n'
        '> **丙**·每一笔判须落到拍号或逐字引用之原句，且须逐笔落「治／驳／挂」。\n\n'
        '## 一·本回之席（其名｜其独见｜其所读）\n\n'
        '| 席 | 其独见（甲律·说不出者不许占位） | 所读 |\n|---|---|---|\n'
        + ''.join('| %s | %s | 〔第N—N章〕 |\n' % (a, b) for a, b in 席表) +
        '\n## 二·逐席之判（乙律·留痕；丙律·落拍号）\n\n'
        '〔逐席一节，每节：其所答之全文＋其致命之判（题／据／何以要命／拟治）〕\n\n'
        '## 三·逐笔裁定（丙律·不许只挂）\n\n'
        '| # | 判（席·题） | 据（章·拍·原句） | 裁 | 其由 |\n|---|---|---|---|---|\n'
        '| 1 | | | ⛔待裁／已治／判驳／已挂 | |\n\n'
        '## 四·本回之数（器出，非估）\n\n'
        '〔净重之趋／站账／约到期／大问表逾期之样／看官账未清之数〕\n\n'
        '## 五·本回之得（一句话）\n\n'
        '〔**这十章合起来，是「慢而深」还是「原地打转」**〕\n')
    print('★大审之册已立：%s' % p)
    print('★★而它须由真读的席来填——**器不许替它签字**。')
    return p


def 印(只闸=False):
    末, 上, 距, 判 = 账()
    if not 只闸:
        print('\n════ 大审 · 以第%d章计 ════' % 末)
        print('  【其律】平均 %d 章一回，从头到尾，逐席真读。' % 每)
        print('  上次大审：%s｜距今 %d 章' % (('至第%d章' % 上) if 上 else '**从来没有过**', 距))
        print('  ── 席之表（%d 席·各须说得出其独见）──' % len(席表))
        for a, b in 席表:
            print('   · %-14s %s' % (a, b))
        print('  ★而此器不读小说、不判小说——它只管「到十章了没有、席够不够、判有没有人收」。')
    else:
        # ★2026-09-05·机制总审：只闸之式原一字不印即为绿——全测之 hook 索器自印之头（§一⑤），故只闸亦印一行头。
        print('════ 大审 · 以第%d章计（只闸）════ 上次%s｜距今 %d 章' % (末, ('至第%d章' % 上) if 上 else '无', 距))
    for x in 判:
        print('  ' + x)
    if not 判:
        print('  ✓不到期，或上一册之判已逐笔落裁。')
    return 判



def _汉(n):
    d = '零一二三四五六七八九'
    if n < 10:
        return d[n]
    if n < 20:
        return '十' + (d[n % 10] if n % 10 else '')
    if n < 100:
        return d[n // 10] + '十' + (d[n % 10] if n % 10 else '')
    h, r = n // 100, n % 100
    if r == 0:
        return d[h] + '百'
    if r < 10:
        return d[h] + '百零' + d[r]
    return d[h] + '百' + d[r // 10] + '十' + (d[r % 10] if r % 10 else '')


def 章档(n):
    for f in sorted(os.listdir(os.path.join(ROOT, '正文'))):
        if ('_第%s章_' % _汉(n)) in f:
            return os.path.join(ROOT, '正文', f)
    return None


def 白文(n):
    p = 章档(n)
    if not p:
        return None
    out = []
    for i, l in enumerate(io.open(p, encoding='utf-8', errors='replace').read().split('\n'), 1):
        if '【本章亮点】' in l:
            break
        out.append('%d\t%s' % (i, l))
    return '\n'.join(out)


def _节(t, 题, 末=True):
    """轮记中题含 题 之 ## 节（末＝取末一回）。"""
    ps = re.split(r'(?m)^(?=## )', t)
    hs = [x for x in ps if x.startswith('## ') and 题 in x.split('\n', 1)[0]]
    return (hs[-1] if 末 else hs[0]).strip() if hs else ''


包目 = lambda b: os.path.join(ROOT, '设定', '_草', '大审%d' % b)
零先之器 = [('抄袭闸', ['抄袭闸.py', '--段']), ('刻意之疲', ['刻意之疲.py']), ('悬念哨', ['悬念哨.py']),
          ('线限哨', ['线限哨.py']), ('清偿章哨', ['清偿章哨.py'])]


def 包(a, b):
    """★1023 X51·瘦式之一「零 token 先行」与之三「虹吸」：诸器先跑、其红汇一页；十章白文（带行号）与各章已付之盲读、
    逻辑审之读误之判同入一包——诸席一读即得，⛔各自重找。→ 设定/_草/大审B/包.md"""
    import subprocess
    os.makedirs(包目(b), exist_ok=True)
    L = ['# 大审之包 · 第%d—%d章（零 token 所汇·诸席同读此一档）\n' % (a, b),
         '## 甲·器之红（零 token 先行：机械之病已由器逮，⛔再劳你找；你只判其中读者可见者）\n']
    for 名, 令 in 零先之器:
        a_ = ['python3', os.path.join(ROOT, '工具', 令[0])] + 令[1:] + ([str(a), str(b)] if 令[-1] == '--段' else [])
        try:
            r = subprocess.run(a_, cwd=ROOT, capture_output=True, text=True, timeout=300)
            o = (r.stdout or '') + (r.stderr or '')
        except Exception as e:
            o = '（跑不成：%s）' % e
        红 = [x for x in o.splitlines() if re.search(r'⛔|⚠|✗|红', x) and '只报不拦' not in x[:6]]
        L.append('- **%s**：%s' % (名, ('红 %d 行' % len(红)) if 红 else '✓'))
        L += ['    ' + x.strip()[:240] for x in 红[:12]]
    for n in range(a, b + 1):
        try:
            r = subprocess.run(['python3', os.path.join(ROOT, '工具', '整句复述哨.py'), str(n)], cwd=ROOT,
                               capture_output=True, text=True, timeout=120)
            o = r.stdout or ''
        except Exception:
            o = ''
        if '本章无一句' not in o and o.strip():
            L.append('- **整句复述哨·%d**：' % n)
            L += ['    ' + x.strip()[:240] for x in o.splitlines()[2:10] if x.strip()]
    L.append('\n## 乙·十章白文（带原行号；引句一律「章:行」）与各章已付之盲读、逻辑审之末判\n')
    缺 = []
    for n in range(a, b + 1):
        t = 白文(n)
        if t is None:
            缺.append(n)
            continue
        L.append('### 第%d章 · %s\n' % (n, os.path.basename(章档(n))))
        L.append(t)
        rp = os.path.join(ROOT, '版本', '第%d章' % n, '_轮记.md')
        if os.path.exists(rp):
            rt = io.open(rp, encoding='utf-8', errors='replace').read()
            盲 = _节(rt, '盲读')
            审 = _节(rt, '逻辑审')
            误 = ''
            if 审:
                m = re.search(r'(?ms)^### 读误之判.*', 审)
                误 = m.group(0) if m else ''
            if 盲:
                L.append('\n#### 第%d章·已付之盲读（末回）\n%s' % (n, 盲[:3000]))
            if 误:
                L.append('\n#### 第%d章·已付之逻辑审·读误之判（末回）\n%s' % (n, 误[:1500]))
        L.append('')
    if 缺:
        raise SystemExit('⛔包缺章：%s' % 缺)
    p = os.path.join(包目(b), '包.md')
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    # 上册「已挂」限 ≤b 之笔（逐字·裁席当面裁之，⛔静静顺延）
    旧 = 限於(b)
    io.open(os.path.join(包目(b), '旧笔.md'), 'w', encoding='utf-8').write(
        '# 上册「已挂」限 ≤%d 之笔（%d 笔·逐字自上册三节）\n\n' % (b, len(旧)) + '\n\n'.join(
            '- 前册#%s 限%d｜%s' % (号, l, c) for 号, l, c in 旧) + '\n')
    print('★上册逾限之笔：%d 笔 → %s' % (len(旧), os.path.relpath(os.path.join(包目(b), '旧笔.md'), ROOT)))
    print('★大审之包：%s（%d 字）' % (os.path.relpath(p, ROOT), sum(len(x) for x in L)))
    return p


def 连带(引):
    """★1023 X46：改一处先知其伤谁——引中「N:L」之原句取其≥6字之段，grep 全书正文他处同段 → 连带之单（零 token）。"""
    out = []
    for n, l in re.findall(r'(\d{1,3})[:：](\d+)', 引 or ''):
        p = 章档(int(n))
        if not p:
            continue
        ls = io.open(p, encoding='utf-8', errors='replace').read().split('\n')
        if not (0 < int(l) <= len(ls)):
            continue
        句 = ls[int(l) - 1]
        段 = [x for x in re.split(r'[，。；：？！、“”「」\s]+', 句) if len(x) >= 6][:3]
        for x in 段:
            hit = []
            for f in sorted(os.listdir(os.path.join(ROOT, '正文'))):
                fp = os.path.join(ROOT, '正文', f)
                for i, y in enumerate(io.open(fp, encoding='utf-8', errors='replace').read().split('\n'), 1):
                    if x in y and not (fp == p and i == int(l)):
                        m = re.search(r'第([零一二三四五六七八九十百]+)章', f)
                        hit.append('%s:%d' % (m.group(1) if m else f, i))
            if hit:
                out.append('%s:%s「%s」亦见 %s' % (n, l, x, '、'.join(hit[:8]) + ('…' if len(hit) > 8 else '')))
    return out


def 裁之文(x, b):
    """裁席之一行 → 册三节「裁」格之文。★1024 实踩（408—410 册）：裁席把还账之限写成 408（包之首章），录成「已挂·限408」，
    册一成即逾限、推闸全红——限⛔早於本册之下一章：≤b 者一律正为 b+1（还账本义即限下一章）。"""
    裁 = str(x.get('ruling', ''))
    限 = x.get('limit')
    try:
        限 = max(int(限), b + 1) if 限 not in (None, '') else None
    except (TypeError, ValueError):
        pass
    if 裁 == '已挂' and 限:
        裁 = '已挂·限%s' % 限
    elif 裁 == '还账':   # 已写章之读者可见致命：一单器施（还账.py），限下一章
        裁 = '已挂·限%s（还账·器施）' % (限 or b + 1)
    return 裁


def 录(run, a=None, b=None):
    """★1023 X27：自 workflow 之 journal 排册之一、二节（逐席之判）与三节（裁席之裁）——⛔一席抄档（W50 录册一席 $20.96）。"""
    import glob
    import json
    js = glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/%s/journal.jsonl' % run))
    if not js:
        raise SystemExit('⛔无此 run 之 journal：%s' % run)
    行 = []
    for l in io.open(js[0], encoding='utf-8', errors='replace'):
        try:
            行.append(json.loads(l))
        except ValueError:
            pass
    标 = {d.get('key'): d.get('label', '') for d in 行 if d.get('type') == 'started'}
    果 = {}
    for d in 行:
        if d.get('type') == 'result':
            r = d.get('result')
            if isinstance(r, str):
                try:
                    r = json.loads(r)
                except ValueError:
                    pass
            果[标.get(d.get('key'), '')] = r
    席果 = {k.split('·', 1)[1]: v for k, v in 果.items() if k.startswith('大审·')}
    裁果 = 果.get('裁') or {}
    if not b:
        b = int(裁果.get('to') or 0) or _末章()
    a = a or b - 每 + 1
    p = os.path.join(册目, '大审_至第%d章.md' % b)
    L = ['# 大审 · 至第%d章（第%d—%d章）\n' % (b, a, b),
         '> 瘦式（X51·裁_1021_省律 九）：零 token 先行（`设定/_草/大审%d/包.md` 甲）＋四席一裁；本册一、二、三节由 `大审.py --录 %s` 自 journal 排出，⛔一席抄档。\n' % (b, run),
         '> 律三：甲·独见｜乙·不强制出负，强制留痕｜丙·每笔落拍号或原句、逐笔落裁。\n',
         '## 一·本回之席（其名｜其独见｜其所读）\n', '| 席 | 其独见 | 所读 |', '|---|---|---|']
    for 名, 独 in 席表:
        r = 席果.get(名) if 名 != '裁' else 裁果
        读 = (r or {}).get('read', '未交') if isinstance(r, dict) else '未交'
        L.append('| %s | %s | %s |' % (名, 独, str(读).replace('|', '／').replace('\n', ' ')))
    L.append('\n## 二·逐席之判（乙律·留痕；丙律·落拍号）\n')
    for 名, _ in 席表[:-1]:
        r = 席果.get(名)
        L.append('### %s\n' % 名)
        if not isinstance(r, dict):
            L.append('未交。\n')
            continue
        fs = r.get('findings') or []
        if not fs:
            L.append('本席无致命之判：%s\n' % r.get('no_fatal_note', ''))
        for i, f in enumerate(fs, 1):
            L.append('%d. 〔%s〕%s:%s「%s」——%s｜拟治：%s' % (i, f.get('severity', ''), f.get('ch', ''), f.get('beat', ''),
                                                       str(f.get('quote', '')).replace('\n', ' '), f.get('issue', ''), f.get('fix', '')))
        if r.get('summary'):
            L.append('\n总：%s' % r['summary'])
        if r.get('hooks'):
            L.append('\n孤钩：' + '；'.join('%s→%s %s %s' % (h.get('id'), h.get('verdict'), h.get('chapter', ''), h.get('form', '')) for h in r['hooks']))
        L.append('')
    L += ['## 三·逐笔裁定（丙律·不许只挂）\n', '| # | 判（席·题） | 据（章·拍·原句） | 裁 | 其由 | 连带（器·X46） |', '|---|---|---|---|---|---|']
    for i, x in enumerate(裁果.get('rows') or [], 1):
        裁 = 裁之文(x, b)
        if x.get('to_segment'):
            裁 += '（入段案·%s）' % x['to_segment']
        带 = '；'.join(连带(x.get('evidence', ''))[:4]) if x.get('repay') else ''
        L.append('| %d | %s | %s | %s | %s | %s |' % (i, *(str(v).replace('|', '／').replace('\n', ' ') for v in (
            x.get('judgment', ''), x.get('evidence', ''), 裁, x.get('reason', ''), 带))))
    cs = 裁果.get('carried') or []
    if cs:
        L += ['\n### 上册逾限之笔·当面裁\n', '| 旧号 | 裁 | 其由 |', '|---|---|---|']
        for x in cs:
            裁 = str(x.get('ruling', ''))
            if '已挂' in 裁 and x.get('limit') and '限' not in 裁:
                裁 += '·限%s' % x['limit']
            L.append('| 前册#%s | %s | %s |' % (str(x.get('old_no', '')).replace('前册#', ''), 裁, str(x.get('reason', '')).replace('|', '／').replace('\n', ' ')))
    L += ['\n## 四·本回之数（器出，非估）\n', '见 `设定/_草/大审%d/包.md` 甲节（零 token 先行诸器之红）。\n' % b,
          '## 五·本回之得（一句话）\n', str(裁果.get('verdict_line', '〔裁席未交〕')) + '\n',
          '## 六·出口归造（入下一段之剧情庭题与段案）\n'] + ['- %s' % x for x in (裁果.get('to_next_segment') or [])]
    io.open(p, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('★大审之册已录：%s（席 %d、裁 %d 行、旧笔 %d）' % (os.path.relpath(p, ROOT), len(席果), len(裁果.get('rows') or []), len(cs)))
    return p

if __name__ == '__main__':
    if '--限' in sys.argv:                 # 开镜卡问七：python3 工具/大审.py --限 N → 上一册「已挂」限 ≤N 之笔
        n = int(sys.argv[sys.argv.index('--限') + 1])
        r = 限於(n)
        print('── 大审「已挂」限 ≤%d 之笔（开镜卡问七须逐笔抄上；到其限须裁：已治／改限带由）──' % n)
        for 号, l, c in r:
            print('  #%s 限%d｜%s' % (号, l, c))
        print('  （零笔）' if not r else '  共 %d 笔' % len(r))
        raise SystemExit(0)
    if '--包' in sys.argv:
        i = sys.argv.index('--包')
        包(int(sys.argv[i + 1]), int(sys.argv[i + 2]))
        raise SystemExit(0)
    if '--录' in sys.argv:
        录(sys.argv[sys.argv.index('--录') + 1])
        raise SystemExit(0)
    if '--立' in sys.argv:
        raise SystemExit(0 if 立(int(sys.argv[sys.argv.index('--立') + 1])) else 2)
    raise SystemExit(1 if 印('--闸' in sys.argv) else 0)
