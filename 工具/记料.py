#!/usr/bin/env python3
"""记料（1015 立·W33）——零 token：把记席九件事要翻的诸账之相关段一次汇成一档，记席一回读毕、⛔逐档翻找。

为何立：W24／W27／W31 三份复盘皆点「记席居诸席之首」（386 $5.26／45 回→387 $5.64／51 回→388 $6.09／63 回）；
  1015 量 388 记席之 63 回：取证与翻账 26、跑器 14、其他 14、写 6、读 3——四成回数花在逐份翻找
  「前章回执之式、施工表 N-1 之锁定行与悬账、全书记忆五档之相关段、轮记与行家评、圣经之锚、检察官之行、下一章之段案与总纲」，
  每翻一回重读整份上下文（坑㉚ 之同类：席以零碎之活办多档）。执笔有章料（一档汇齐），记席无——本器即记席之章料。
⛔限：只汇、⛔判；所汇皆逐字抄自盘上之档（章:行可查）；封版.py N --前 之印⛔汇（其有存版之副作用，记席自跑）。

★1020 W53·X15（记席之费在读：392 记席 $4.73；394 长章之记料 161KB 逾 150KB 拦封版，瘦後余量仅 5KB——料随章长与在场人数而涨）之结构之治：
  ①节之界：十二节各有其界（`界`），逾界即截於行界、印其所略与全文之路；Σ界＋诸题 < 限——记料之长与章长、在场人数脱钩（自测以「八倍之章、全册之人」回灌钉之）。
  ②各节之用（据 397 记席之席记「料缺」与 397 封版对全书记忆四档之 diff）：
     去其不用——用法首六十行（读者调取之法）→§五规矩、§六之式（记席照之写第N章.md，旧反不汇）｜总览首十四行（一页之要、按站，记席不改）→今站一块与锚行｜
       前章创作记录首三十行→每节首二行｜前章席记（令已给其式）｜轮记首十行→轮记、行家评之目（带行号；记席本须全读）、构思之档｜
       悬线钉 N—N+3 之整行（一行一二千字）→钉 N、N+1 之处各摘其旁。
     留而改之——同线前章之白文（冷眼轮所冷读者即此章，392—397 回执俱书「记料十节逐字汇入」）加行号（旧无行号，冷眼轮、承前之判引 章:行 另 grep）。
     补其所缺——前章回执每节首三行（旧只首四十行，§四以下另 sed）｜施工表本章硬门槛整节（旧只其头三行）｜open_brief 全块（旧截四千）｜
       检察官 OPEN_BRIEF_CARD_SCHEMA 之行（旧式「^ N:」认不着四格缩进，向来空）｜在场之人（旧以 str(别称) 拆，list 之称全认不着、暗线之「她」恒零——395、397 五、十一两节空）｜
       全书记忆四档之锚行｜state_canon 一卡之式｜大师进化账末三行。
  ③所引之档之「#」行一律加「〉」——旧式引回执、轮记之「## 八·…」与记料自家之「## 八·…」同形，记席按节找料即撞错节；记料自家之节作「## 【八】…」。
  ④（独立验席所逮·【九】之界与段案之取相撞）段案之取止於任一「## 」（旧连附一、附二取入：399 之【九】16KB 截去总纲、余章 400 之行）；
     多源之节锚行短行在前、式样长档殿後（【四】【八】【九】），逾界之注只列被截诸片之源（旧只一源，注指错档）；【八】锚行⛔重印。

★1020 X36（398 记席 flaws③、399 记席另报：四样料外另 sed／grep）之补——各补入其最近之节之尾，⛔新立节（仍十二节）：
  ①【七】诸构思之「## 满分之问」全段（399 记席：甲、己、庚三份另 sed）——三种写法与其比在前、拍表殿後（截自尾起，先截拍表；带行号）；
  ②【二】同镜前章之「| N | 悬账 |」行（398 记席：上一同镜章之悬账另翻）——镜取施工表锁定行之「镜：」、本章取卡「本章之镜」
     （我＝苏衍、她＝沈鸢；X34：399 黎东来镜之同镜前章係 389，⛔397）；同镜无前者照旧取同线；同镜即 N-1 者其行已在上、⛔重印；
  ③【八】本章卡与下一章卡里「圣经:NNNN」（连「、:NNNN」「—NNNN」）所指之行——锚行、前章之条已印者⛔重印；
  ④【五】【十一】卡·问九之二所列之人（399 记席：管章的人只以纸到场，【五】只认白文、状态册与人物.md 另 grep）——
     收「- **名**」之头与注里之称（「不回」「⛔在场」之句⛔收）与白文出现之人之并；册无其人者列其名。
  界：补殿旧体之後，旧体先截於其旧界——旧节之所收一字不让；补之额取诸节未用之界（池＝Σ界−Σ旧体之实），依 补序 分，各补又有其顶（补界）；
     全档 ≤ Σ界＋头 ＜ 限——头注之总界不动（自测压测量之）。逾额即截、印其所略与其源（「（本节逾界·补额」）。
  驳席所逮（1020）：①构思作「② ## 满分之问」「② 满分之问」者（386—397 十八份，圈号起行）旧认不着、印「无满分之问之节」→ _满分之段 兼认；
     ③「`圣经:7408`／`:8161`」之续引（334、335、353 之卡）旧只认首号→兼认「／」与反引号；自测补「镜：我」之归一（396→394）。

用法：
  python3 工具/记料.py N          # → 版本/第N章/_记料.md
  python3 工具/记料.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
表 = os.path.join('设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
记 = os.path.join('设定', '全书记忆')
册档 = os.path.join('设定', '人物状态册.json')
限 = 150 * 1024
# ★1020 X15·节之界（字节）：Σ 145,500＋诸题与逾界之注（≤ 头之界，自测压测量之）＜ 限 153,600——结构上逾不了
#   验席所逮後调：九 16000→20000（W54 段案一章之节至 15KB：398 之节＋余章 398 之行＝17.7KB）｜
#   十 14000→15000（近百章同线白文带行号之顶 360 之 13038，旧余 7%）｜三 4000→3500（385—399 之顶 2694）
界 = {'一': 13000, '二': 17000, '三': 3500, '四': 18000, '五': 6000, '六': 12000,
      '七': 4000, '八': 14000, '九': 20000, '十': 15000, '十一': 17000, '十二': 6000}
头之界 = 6000
# ★1020 X36·补之顶（字节）：补不入 Σ界——其额取诸节未用之界（池＝Σ界−Σ旧体之实，依 补序 先短後长），故全档仍 ≤ Σ界＋头＜限。
#   顶据其实：七 满分之问 385—399 之顶 399 七份 35.1KB（三种写法 10.0KB＋拍表 25.2KB）｜二 悬账行一行之顶 317 之 9.0KB
#   （385—399 之顶 394 之 5.2KB；363、365 之 7—8KB 行逾 6000 即整行截去——截於行界）｜八 卡引圣经 0—3 行（1722 一行 1.6KB）｜
#   五、十一 卡·问九之二所列而白文未见者 0—2 人
补界 = {'八': 6000, '二': 9500, '五': 3000, '十一': 5000, '七': 45000}
补序 = ('八', '二', '五', '十一', '七')


def 读(p, root=ROOT):
    p = os.path.join(root, p)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def 行们(文, 式, 上=0, 下=0, 最多=None):
    """文里合式之行（连上下文），带行号。"""
    L = 文.split('\n'); 出 = []; 已 = set()
    for i, l in enumerate(L):
        if re.search(式, l):
            for k in range(max(0, i - 上), min(len(L), i + 下 + 1)):
                if k not in 已:
                    已.add(k); 出.append('%d｜%s' % (k + 1, L[k]))
            if 最多 and len(出) >= 最多:
                break
    return '\n'.join(出)


def 引(t):
    """★1020 X15③：所引之档之「#」行加「〉」——⛔与记料自家之节同形。"""
    return '\n'.join(('〉' + l) if l.startswith('#') else l for l in (t or '').split('\n'))


def _截(片们, k):
    """★1020 X36（自 节 析出，旧节与补同尺）：片们 [(源, 片)] 依序以空行相接；逾 k 字节截於行界 →
    (留, 略)；略 = None 或 (下略之行数, 下略之字节, [被截诸片之源])。"""
    片们 = [(s, (t or '').strip()) for s, t in 片们 if (t or '').strip()]
    体 = '\n\n'.join(t for _, t in 片们)
    if len(体.encode()) <= k:
        return 体, None
    留 = 体.encode()[:k].decode('utf-8', 'ignore')
    if '\n' in 留:
        留 = 留[:留.rfind('\n')]
    略 = 体[len(留):].strip('\n')
    略源, 止 = [], -2
    for s, t in 片们:
        止 += 2 + len(t)
        if 止 > len(留) and s and s not in 略源:
            略源.append(s)
    return 留, (略.count('\n') + 1, len(略.encode()), 略源)


def _片们(体, 源=''):
    return [(源, 体)] if not isinstance(体, list) else 体


def 节(号, 标, 体, 源='', 补=None, 补额=0):
    """★1020 X15①：一节一界——逾界截於行界，印其所略与所略之源（缺者 sed -n 补）。
    体：str（一源，源即其档）或 [(源, 片)]（多源之节：片依序以空行相接；注只列被截诸片之源——
    X15 验席逮：旧只收一源，【九】截在总纲、余章总案而注写段案，记席照注 sed 找不回）。
    多源之节，式样与长档殿後、锚行与短行在前——截自尾起，先截者须是全文最易补者。
    ★1020 X36：补 [(源, 片)] 殿旧体（与其逾界之注）之後，自截於 补额——旧体之截只看旧界，补⛔挤旧。"""
    k = 界[号]
    体, 略 = _截(_片们(体, 源), k)
    体 = 体 or '（无）'
    if 略:
        体 += '\n（本节逾界 %d 字节：下略 %d 行、%d 字节%s——缺者 sed -n 补）' % (
            k, 略[0], 略[1], ('；所略之源 ' + '、'.join(略[2])) if 略[2] else '')
    if 补:
        补体, 补略 = _截(补, 补额)
        if 补体:
            体 += '\n\n' + 补体
        if 补略:
            体 += '\n（本节逾界·补额 %d 字节：补下略 %d 行、%d 字节%s——缺者 sed -n 补）' % (
                补额, 补略[0], 补略[1], ('；所略之源 ' + '、'.join(补略[2])) if 补略[2] else '')
    return '\n## 【%s】%s\n\n%s\n' % (号, 标, 体)


def _用(号, 体, 源=''):
    """旧体截於其界後之实（字节·不计逾界之注）——补之池 ＝ Σ界 − Σ此。"""
    return len(_截(_片们(体, 源), 界[号])[0].encode())


def 段(文, 头式, 起=0):
    """文里（自第 起 行·0 起）首个合「头式」之「#」行起之一段（至下一个同级以上之「#」行止），带行号。"""
    L = 文.split('\n')
    for i, l in enumerate(L):
        if i >= 起 and l.startswith('#') and re.search(头式, l):
            级 = len(l) - len(l.lstrip('#'))
            j = i + 1
            while j < len(L) and not (L[j].startswith('#') and len(L[j]) - len(L[j].lstrip('#')) <= 级):
                j += 1
            return '\n'.join('%d｜%s' % (k + 1, L[k]) for k in range(i, j)).rstrip()
    return ''


def 块(文, i):
    """文之第 i 行（0 起）起之一块「- **…」（至下一个顶格之「- 」或「#」止），带行号。"""
    L = 文.split('\n')
    j = i + 1
    while j < len(L) and not L[j].startswith(('- ', '#')):
        j += 1
    return '\n'.join('%d｜%s' % (k + 1, L[k]) for k in range(i, j)).rstrip()


def _号段(号们):
    """[9924, 9925, 9926, 9930] → '9924—9926、9930'。"""
    出 = []
    for x in sorted(set(号们)):
        if 出 and x == 出[-1][1] + 1:
            出[-1][1] = x
        else:
            出.append([x, x])
    return '、'.join(('%d' % a) if a == b else '%d—%d' % (a, b) for a, b in 出)


def 截(s, k):
    s = str(s)
    return s if len(s) <= k else s[:k] + '…（下略 %d 字）' % (len(s) - k)


def 行截(t, k=300):
    """式样与锚行之每行截 k 字（记席改其档须先 Read 其行——此只给式与行号，⛔整行抄两回）。"""
    return '\n'.join(截(l, k) for l in (t or '').split('\n'))


def 章白(n, root=ROOT):
    import 章料
    f = 章料.章档(n, root)
    if not f:
        return '', ''
    t = open(f, encoding='utf-8').read()
    return f, t.split('【本章亮点】')[0]


def _白行(n, root=ROOT):
    """(档之相对路, [(行号, 行)])——第 n 章白文（【本章亮点】之前）之非空行，行号即整档之行（与 awk NR 同）。"""
    import 章料
    f = 章料.章档(n, root)
    if not f:
        return '?', []
    L = open(f, encoding='utf-8').read().split('【本章亮点】')[0].split('\n')
    return os.path.relpath(f, root), [(i + 1, l) for i, l in enumerate(L) if l.strip()]


def _节首(t, k):
    """★1016（393 封版逮：记料 156KB 逾 150KB；X15 记席之费在读）：前章之档只作式样——每「## 」节留首 k 行，余印其数。"""
    出, 节行 = [], 0
    for l in t.split('\n'):
        if l.startswith('## '):
            if 节行 > k:
                出.append('（本节下略 %d 行）' % (节行 - k))
            出.append(l); 节行 = 0; continue
        节行 += 1
        if 节行 <= k:
            出.append(l)
    if 节行 > k:
        出.append('（本节下略 %d 行）' % (节行 - k))
    return '\n'.join(出)


# ── 在场之人（★1020 X15：旧以 str(别称) 拆——别称是 list，拆出「['她（…）'」，名表之称全认不着；暗线之「她」恒零）──
_泛 = re.compile(r'^(?:一个|那个|这个|那|这)?(?:人|女人|男人|汉子|孩子|老人|后生|姑娘)$')


def _称们(v):
    """名与别称：去括注、拆「甲/乙」、二字以上。"""
    al = v.get('别称') or []
    if isinstance(al, str):
        al = re.split(r'[、，,]', al)
    出 = []
    for x in [v.get('名') or ''] + list(al):
        x = re.sub(r'（[^）]*）|\([^)]*\)', '', str(x)).strip()
        出 += [y.strip() for y in re.split(r'[／/]', x) if len(y.strip()) >= 2]
    return 出


def _镜(白):
    """三值（与 看官._线 同尺）：主（我≥3/千）｜她｜他。"""
    w = len(re.sub(r'\s', '', 白)) or 1
    if 白.count('我') / w * 1000 >= 3:
        return '主'
    return '她' if 白.count('她') >= 白.count('他') else '他'


def 在场(白, N, 册):
    """[(名, 所见之称, 册行)]：①别称注「主线第一人称」「暗线章通篇只作『她』」者，其镜之章必在场；
    ②名（去括注、非泛称）见於白文；③别称（三字以上、非泛称）见於白文且末见章在三十章内。
    （1020 量 385—397：以「N态」为真——旧 认中 31／漏 23／误 0，今 认中 44／漏 10／误 1。）"""
    if not 白:
        return []
    镜 = _镜(白)
    出 = []
    for v in (册.get('人物') or [] if isinstance(册, dict) else []):
        if not isinstance(v, dict):
            continue
        注们 = []
        for x in (v.get('别称') if isinstance(v.get('别称'), list) else []):
            m = re.search(r'（([^）]*)）', str(x))
            if m:
                注们.append(m.group(1))
        称们 = _称们(v)
        if any(('第一人称' in z and 镜 == '主') or ('通篇' in z and '她' in z and 镜 == '她') for z in 注们):
            出.append((v.get('名'), ['（%s之镜·通篇）' % 镜], v)); continue
        if 称们 and not _泛.match(称们[0]) and 称们[0] in 白:
            出.append((v.get('名'), [称们[0]], v)); continue
        m = re.match(r'\d+', str(v.get('末见章') or ''))
        近 = bool(m) and int(m.group()) >= N - 30
        中 = [x for x in 称们[1:] if len(x) >= 3 and not _泛.match(x) and x in 白]
        if 近 and 中:
            出.append((v.get('名'), 中, v))
    return 出


def _册之区(名, root=ROOT):
    """人物状态册.json 里此人之行区（起—止，1 起）。"""
    L = 读(册档, root).split('\n')
    头 = [i for i, l in enumerate(L) if re.match(r'^   "名": ', l)]
    for k, i in enumerate(头):
        if L[i].strip().rstrip(',') == '"名": %s' % json.dumps(名, ensure_ascii=False):
            止 = (头[k + 1] - 2) if k + 1 < len(头) else len(L)
            return i, 止
    return None


def _册行(v):
    """去旧态、留末一态（截五百字）；余串截二百字、列只留末二条（前略之数印出）——全行看其区。"""
    态 = sorted([x for x in v if re.match(r'\d+态$', x)], key=lambda x: int(re.match(r'\d+', x).group()))
    出 = {}
    for k, x in v.items():
        if re.match(r'\d+态$', k) and k not in 态[-1:]:
            continue
        if isinstance(x, list):
            出[k] = (['（前 %d 条略）' % (len(x) - 2)] if len(x) > 2 else []) + [截(y, 120) for y in x[-2:]]
        elif isinstance(x, str):
            出[k] = 截(x, 500 if re.match(r'\d+态$', k) else 200)
        else:
            出[k] = x
    出['（旧态）'] = '、'.join(态[:-1][-6:]) + ('等 %d 态' % len(态[:-1]) if len(态) > 7 else '')
    return json.dumps(出, ensure_ascii=False)


def _段案(n, root=ROOT):
    """第 n 章之段案之节 → (档之相对路, 节文, [段头与附录诸节之目 :起—止])——取至任一「## 」止。
    ★1020 X15 验席：旧式止於「## 数」，各段案档末一章连其後「## 附一·落账」「## 附二·…」一并取入（400 之节取成 16KB）。"""
    for p in sorted(glob.glob(os.path.join(root, '设定', '段案', '*.md'))):
        if os.path.basename(p).startswith('_'):
            continue
        L = open(p, encoding='utf-8').read().split('\n')
        末 = len(L) - (1 if L and L[-1] == '' else 0)
        头 = [i for i, l in enumerate(L) if l.startswith('## ')]
        for k, i in enumerate(头):
            if re.match(r'## %d\s*$' % n, L[i]):
                止 = 头 + [末]
                目 = ['段头 :1—%d' % 头[0]] + ['%s :%d—%d' % (L[a][3:].strip(), a + 1, 止[q + 1])
                                               for q, a in enumerate(头) if not re.match(r'## \d+\s*$', L[a])]
                return os.path.relpath(p, root), '\n'.join(L[i:止[k + 1]]).strip(), 目
    return '', '', []


# ── ★1020 X36 之补 ──
def _满分之段(文):
    """一份构思之「满分之问」段（带行号）。★1020 X36 驳席逮：386—397 十八份构思作「② ## 满分之问」「② 满分之问」
    （圈号起行、非「#」行——造章令「② 一节「## 满分之问」」照抄），段 认不着，旧印「无满分之问之节」而实有；
    圈号起者止於下一圈号行或「#」行。"""
    s = 段(文, r'满分之问')
    if s:
        return s
    L = 文.split('\n')
    起 = next((i for i, l in enumerate(L) if re.match(r'^[①-⑳]\s*(?:#+\s*)?满分之问', l)), None)
    if 起 is None:
        return ''
    止 = next((j for j in range(起 + 1, len(L)) if re.match(r'^(?:#|[①-⑳])', L[j])), len(L))
    return '\n'.join('%d｜%s' % (k + 1, L[k]) for k in range(起, 止)).rstrip()


def _满分之问(构思, root=ROOT):
    """诸构思之「满分之问」全段（带行号）→ [(源, 片)]：三种写法与其比在前（每份一片），拍表（「|」起之行）殿後——截自尾起先截拍表。"""
    文们, 表们 = [], []
    干 = '甲乙丙丁戊己庚辛壬癸'
    for p in sorted(构思, key=lambda p: (干.find((re.search(r'起草_(.)_构思', p) or [None, ''])[1]) % 99, p)):
        rp = os.path.relpath(p, root)
        s = _满分之段(open(p, encoding='utf-8', errors='replace').read())
        if not s:
            文们.append((rp, '〔%s：无「满分之问」之节〕' % rp)); continue
        L = s.split('\n')
        表 = [l for l in L if l.split('｜', 1)[-1].startswith('|')]
        文 = [l for l in L if l not in 表]
        头 = '〔%s:%s—%s·满分之问%s〕\n' % (rp, L[0].split('｜')[0], L[-1].split('｜')[0], '（拍表 %d 行殿後）' % len(表) if 表 else '')
        文们.append((rp, 头 + 行截('\n'.join(文), 800)))
        if 表:
            表们.append((rp, '〔%s·满分之问之拍表〕\n' % rp + 行截('\n'.join(表), 800)))
    return 文们 + 表们


def _镜名(x):
    """镜之称归一：锁定行作「我」「她」者即苏衍、沈鸢。"""
    x = re.sub(r'[*`\s]', '', x or '')
    return {'我': '苏衍', '她': '沈鸢'}.get(x, x)


def _镜之表(T):
    """施工表锁定行之「镜：X」→ {章: 镜}（365 起有之）。"""
    出 = {}
    for m in re.finditer(r'^\| (\d+) \| 锁定 \|(.*)$', T, re.M):
        k = re.search(r'镜[：:]\s*\**([^｜|*（(，,、\s]{1,12})', m.group(2))
        if k:
            出[int(m.group(1))] = _镜名(k.group(1))
    return 出


def _卡之镜(卡, 识):
    """卡「本章之镜」一行里最先出现之镜名（识：已知之镜名；「不适用（主线·苏衍第一人称）」亦认作苏衍）。"""
    l = next((l for l in (卡 or '').split('\n') if '本章之镜' in l and not l.startswith('#')), None)   # 题行「问二·本章之镜（若为暗线）」⛔认
    if not l:
        return None
    l = l.split('本章之镜', 1)[1]
    位 = sorted((l.find(x), x) for x in 识 if x in l)
    return 位[0][1] if 位 else None


def _同镜(N, T, 卡, root=ROOT):
    """(同镜前章, 镜, 由)：本章之镜先取施工表 N 之锁定行（已封），无则取卡；同镜前章取六十章内最近者；
    同镜无前（或镜不明）者照旧取同线（X34）——由 = '同镜'／'同线'。"""
    表 = _镜之表(T)
    镜 = 表.get(N) or _卡之镜(卡, set(表.values()) | {'苏衍', '沈鸢'})
    前 = [k for k, v in 表.items() if N - 60 <= k < N and v == 镜] if 镜 else []
    if 前:
        return max(前), 镜, '同镜'
    import 造式验
    本线 = 造式验.线(N, root)
    同 = next((k for k in range(N - 1, N - 13, -1) if 本线 and 造式验.线(k, root) == 本线), None)
    return 同, 镜, '同线'


def _圣经之引(t):
    """「圣经:1950、:2644」「圣经:12—14」→ [1950, 2644, 12, 13, 14]（去重、依序；一段至多展八行）。
    ★1020 X36 驳席：334、335、353 之卡作「`圣经:7408`／`:8161`」（斜杠、反引号相隔）——旧只认首号；段尾小於段首（「:1950—52」）旧整段丢，今只取段首。"""
    号 = []
    for m in re.finditer(r'圣经[:：](\d+)(?:[—–-](\d+))?((?:`?\s*[、，,／/]\s*`?[:：]\d+(?:[—–-]\d+)?)*)', t or ''):
        for a, b in [(m.group(1), m.group(2))] + re.findall(r'[:：](\d+)(?:[—–-](\d+))?', m.group(3)):
            a = int(a)
            号 += list(range(a, min(int(b) if b and int(b) >= a else a, a + 7) + 1))
    return list(dict.fromkeys(号))


_不收 = re.compile(r'不回|⛔在场|不在场')


def _卡之人(卡, 册, 已):
    """卡·问九之二所列之人 → ([(名, [所见之称], 册之人)], [册无其人之头])：
    「- **名**」之头只认其名；注（他行）以「；。」分句，句含「不回」「⛔在场」者⛔收（399：录入的那个、接线的永不回）；已（白文所认之名）⛔重。"""
    L = (卡 or '').split('\n')
    起 = next((i for i, l in enumerate(L) if l.startswith('#') and '问九之二' in l), None)
    if 起 is None:
        return [], []
    止 = next((j for j in range(起 + 1, len(L)) if L[j].startswith(('#', '---'))), len(L))
    头们, 句们 = [], []
    for l in L[起 + 1:止]:
        m = re.match(r'^- \*\*([^*]+)\*\*', l)
        if m:
            头们.append(re.sub(r'（[^）]*）|\([^)]*\)', '', m.group(1)).strip())
        elif l.strip() and not l.startswith('>'):
            句们 += [s for s in re.split(r'[；;。]', l) if s.strip() and not _不收.search(s)]
    出, 中头 = [], set()
    for v in (册.get('人物') or [] if isinstance(册, dict) else []):
        if not isinstance(v, dict):
            continue
        称们 = [x for x in _称们(v) if not _泛.match(x)]
        中 = [h for h in 头们 if any(x == h or x in h for x in 称们)]
        中头.update(中)
        中 += [x for x in 称们 if any(x in s for s in 句们) and x not in 中]
        if 中 and v.get('名') not in 已:
            出.append((v.get('名'), 中, v))
    return 出, [h for h in 头们 if h not in 中头]


def 汇(N, root=ROOT):
    f, 白 = 章白(N, root)
    出 = ['# 记料·第%d章（零 token 所汇·工具/记料.py）' % N, '',
          '> 记席之九件事所要翻的诸账，於此一档；逐字抄自盘上（章:行可查）。⛔再逐档翻找——缺者方以 `sed -n` 补，并记其缺（交主环补器）。'
          '封版.py %d --前 之印⛔在此（其有存版之副作用），记席自跑。' % N,
          '> 节作「## 【一】」至「## 【十二】」，各有其界（逾界者印其所略与全文之路）；所引之档之「#」行皆加「〉」（原档无此符）。'
          '「〔补·…〕」起者係 X36 之补（殿其节之尾，额取诸节未用之界）。']
    # ★1020 X36：诸节先记其料、末了一并成节——补之额要等诸节旧体之实量毕方知
    诸, 补们 = [], {}
    卡档 = [os.path.join('版本', '第%d章' % n, '_开镜卡.md') for n in (N, N + 1)]
    卡, 下卡 = 读(卡档[0], root), 读(卡档[1], root)
    # 一、前章回执之式
    前回 = sorted(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % (N - 1))))
    if 前回:
        p = os.path.relpath(前回[-1], root)
        诸.append(('一', '前章回执之式（%s：每节首三行；全文照此式写）' % p, 引(行截(_节首(open(前回[-1], encoding='utf-8').read(), 3), 400)), p))
    # 二、施工表
    T = 读(表, root)
    诸.append(('二', '施工表：N-1 之锁定行与悬账（式样）、本章之硬门槛（整节；下一章之节立於其上）',
                行们(T, r'^\| %d \| (锁定|悬账) \|' % (N - 1)) + '\n\n' + 行截(段(T, r'^## 四、续写第 %d 章前的硬门槛' % N), 400), 表))
    # ★1020 X36②：同镜前章之悬账行（同镜即 N-1 者其行已在上）
    镜前, 镜, 镜由 = _同镜(N, T, 卡, root)
    if 镜前 and 镜前 != N - 1:
        悬 = 行们(T, r'^\| %d \| 悬账 \|' % 镜前)
        补们['二'] = ('；补：%s前章（%d）之悬账行' % (镜由, 镜前), [(表, '〔补·%s前章（第%d章%s）之悬账行（%s）〕\n' % (
            镜由, 镜前, ('·镜：%s' if 镜由 == '同镜' else '·本章之镜 %s 无同镜之前') % 镜 if 镜 else '', 表) +   # 驳席：同线者旧注「·镜：霍钧」读如 389 之镜
            (悬 or '（施工表无「| %d | 悬账 |」之行）' % 镜前))])
    # 三、创作记录（式样）
    创 = os.path.join('版本', '第%d章' % (N - 1), '_创作记录.md')
    诸.append(('三', '前章创作记录（%s：每节首二行·式样；席记之式见令）' % 创, 引(_节首(读(创, root), 2)), 创))
    # 四、全书记忆
    用法 = 读(os.path.join(记, '用法.md'), root)
    U = 用法.split('\n')
    起 = next((i for i, l in enumerate(U) if l.startswith('## 五、')), 0)
    止 = next((i for i in range(起 + 1, len(U)) if U[i].startswith('## 七、')), len(U))
    前章记 = 读(os.path.join(记, '第%d章.md' % (N - 1)), root)
    总览 = 读(os.path.join(记, '总览.md'), root)
    V = 总览.split('\n')
    今站 = max([i for i, l in enumerate(V) if re.match(r'^### E\d', l)] or [-1])
    人物 = 读(os.path.join(记, '人物.md'), root)
    # ★1020 X15 验席：锚行在前，§五§六（有行号，截则 sed -n 起,止p）次之，前章之记（式样）殿後——截自尾起只截式样
    诸.append(('四', '全书记忆：总览与人物之锚行、用法 §五规矩与 §六之式、前章之记（每节首二行·式样）', [
        (os.path.join(记, '总览.md'),
         '〔总览·题、「全书今之末」、今站一块（记席改其「线与日」「读者之所欠」、添本章一行）、索引末三行〕\n' +
         行们(总览, r'^# |全书今之末', 0, 0, 3) + '\n' + (引(行截(段(总览, r'^### E\d', 今站), 200)) if 今站 >= 0 else '（总览无站块）') + '\n' +
         '\n'.join('%d｜%s' % (i + 1, l) for i, l in list(enumerate(V))[-3:])),
        (os.path.join(记, '人物.md'),
         '〔人物.md·题与今之行止（全档 %d 行；在场之人之节见【五】）〕\n' % len(人物.split('\n')) + 行截(行们(人物, r'^# |^> 今之行止', 0, 0, 3))),
        (os.path.join(记, '用法.md'), '〔用法.md:%d—%d〕\n' % (起 + 1, 止) + 引('\n'.join(U[起:止]))),
        (os.path.join(记, '第%d章.md' % (N - 1)),
         '〔第%d章.md·式样（每节首二行；式以上之 §六 为准；全文照 `设定/全书记忆/第%d章.md`）〕\n' % (N - 1, N - 1) + 引(行截(_节首(前章记, 2), 200)))]))
    # 五、在场之人：人物.md 之节首与末一「之变」
    册 = {}
    try:
        册 = json.load(open(os.path.join(root, 册档), encoding='utf-8'))
    except Exception:
        pass
    人们 = 在场(白, N, 册)

    def 人节(名, 题):
        名0 = re.sub(r'（[^）]*）', '', 名 or '')
        节体 = 段(人物, r'^### .*%s' % re.escape(名0)) if 名0 else ''
        行 = 节体.split('\n') if 节体 else []
        变 = [l for l in 行 if re.match(r'\d+｜- \*\*\d+', l)]
        return [题, '\n'.join([引(x) for x in 行[:1]] + [截(x, 400) for x in 变[-1:]]) or '（人物.md 无其节）']
    体 = []
    for 名, 中, v in 人们:
        体 += 人节(名, '### %s（白文所见之称：%s｜末见章 %s）' % (名, '、'.join(中), v.get('末见章')))
    诸.append(('五', '本章白文里出现之人（人物.md 之节首与末一「之变」·式样；状态册之行见【十一】）——须添「%d态」者' % N, '\n'.join(体), os.path.join(记, '人物.md')))
    # ★1020 X36④：卡·问九之二所列而白文未见之人（只以纸、以手到场者——399 管章的人）；册无其人者列其名
    卡人, 卡无册 = _卡之人(卡, 册, {x[0] for x in 人们})
    if 卡人 or 卡无册:
        体 = ['〔补·卡·问九之二所列而白文未见之人（%s）〕' % 卡档[0]]
        for 名, 中, v in 卡人:
            体 += 人节(名, '### %s（卡·问九之二所列之称：%s｜末见章 %s）' % (名, '、'.join(中), v.get('末见章')))
        if 卡无册:
            体.append('〔卡·问九之二所列而状态册无其人：%s〕' % '、'.join(卡无册))
        补们['五'] = ('；补：卡·问九之二所列之人', [(卡档[0], '\n'.join(体))])
    # 六、物件、悬线
    物件 = 读(os.path.join(记, '物件.md'), root)
    悬线 = 读(os.path.join(记, '悬线.md'), root)
    W = 物件.split('\n')
    末物 = max([i for i, l in enumerate(W) if re.match(r'^- \*\*\d+ 之物', l)] or [-1])
    S = 悬线.split('\n')
    所结 = max([i for i, l in enumerate(S) if re.match(r'^- \*\*.*所结所开', l)] or [-1])
    号 = re.compile(r'(?<!\d)(%d|%d)(?!\d)' % (N, N + 1))
    条, 摘 = [], []
    for i, l in enumerate(S):
        if i == 所结 or not 号.search(l):
            continue
        if re.match(r'^- \*\*(%d|%d)（' % (N, N + 1), l):
            条.append('%d｜%s' % (i + 1, 截(l, 400)))
            continue
        窗, 末 = [], -1
        for m in 号.finditer(l):
            a, b = max(m.start() - 40, 末 + 1), min(len(l), m.end() + 24)
            if a < b:
                窗.append(l[a:b]); 末 = b
        摘.append('%d｜%s…%s…%s' % (i + 1, l[:24], '…'.join(窗[:2]), '（另 %d 处）' % (len(窗) - 2) if len(窗) > 2 else ''))
    诸.append(('六', '物件之末一块（式样；新块添於档末）、悬线：末一「所结所开」（式样）、钉 %d、%d 之条与其旁' % (N, N + 1),
                '〔物件.md·题与末一块〕\n' + 行们(物件, r'^# ', 0, 0, 1) + '\n' + (行截(块(物件, 末物), 200) if 末物 >= 0 else '（无）') +
                '\n\n〔悬线.md·题与末一「所结所开」〕\n' + 行们(悬线, r'^# ', 0, 0, 1) + '\n' + ('%d｜%s' % (所结 + 1, 截(S[所结], 600)) if 所结 >= 0 else '（无）') +
                '\n\n〔悬线.md·「%d（」「%d（」之条〕\n' % (N, N + 1) + ('\n'.join(条) or '（无）') +
                '\n\n〔悬线.md·提及 %d、%d 之行（摘其旁；全行 sed -n 读）〕\n' % (N, N + 1) + ('\n'.join(摘) or '（无）'), os.path.join(记, '悬线.md')))
    # 七、轮记、行家评、构思之目（记席本须全读——此只给目与行号）
    def 目(p):
        t = 读(p, root)
        if not t:
            return '〔%s：无〕' % p
        return '〔%s·%d 字节·%d 行〕\n' % (p, len(t.encode()), t.count('\n') + 1) + '\n'.join(
            '%d｜〉%s' % (i + 1, 截(l, 80)) for i, l in enumerate(t.split('\n')) if l.startswith('#'))
    章目 = os.path.join('版本', '第%d章' % N)
    构思 = sorted(glob.glob(os.path.join(root, 章目, '起草_*_构思.md')))
    诸.append(('七', '本章轮记、行家评之目（行号）与诸构思之档——创作记录据之（全读）', [
        (os.path.join(章目, '_轮记.md'), 目(os.path.join(章目, '_轮记.md'))),
        (os.path.join(章目, '_行家评.md'), 目(os.path.join(章目, '_行家评.md')) + '\n\n〔行家评·名次〕\n' +
         行们(读(os.path.join(章目, '_行家评.md'), root), r'^#+ *名次|^\d+\. *稿|名次', 0, 2, 20)),
        (os.path.join(章目, '起草_*_构思.md'), '〔构思〕\n' +
         ('\n'.join('%s（%d 字节）' % (os.path.relpath(p, root), os.path.getsize(p)) for p in 构思) or '（无）'))]))
    # ★1020 X36①：诸构思之「满分之问」全段（三种写法与其比在前、拍表殿後）
    if 构思:
        满 = _满分之问(构思, root)
        满[0] = (满[0][0], '〔补·诸构思之「满分之问」全段（%d 份；三种写法与其比在前，拍表殿後——截自尾起先截拍表）〕\n' % len(构思) + 满[0][1])
        补们['七'] = ('；补：诸构思之「满分之问」全段', 满)
    # 八、圣经之锚、检察官之行、open_brief
    圣 = 读(os.path.join('设定', '00_镇冢秘术_唯一总圣经.md'), root)
    检 = 读(os.path.join('工具', '小说检察官.py'), root)
    try:
        canon = json.load(open(os.path.join(root, '设定', 'canon事实库.json'), encoding='utf-8'))
        ob = canon.get('open_brief') if isinstance(canon, dict) else None
    except Exception:
        canon, ob = {}, None
    圣档 = os.path.join('设定', '00_镇冢秘术_唯一总圣经.md')
    锚 = 行们(圣, r'^## 十一、已写 1—|第 (%d|%d) 章必须从' % (N, N + 1), 0, 2, 12)
    # ★1020 X15 验席：前章之条含本章之锚（398 之 9924—9926 印两回·赘 762 字节）——锚行已印者⛔重印、注其号；
    #   open_brief（记席逐栏重写）在前，前章之条（式样）殿後——截自尾起只截式样
    已印 = {l.split('｜', 1)[0] for l in 锚.split('\n') if '｜' in l}
    条 = [l for l in 段(圣, r'^### 第 %d 章《' % (N - 1)).split('\n') if l]
    重 = [int(l.split('｜', 1)[0]) for l in 条 if l.split('｜', 1)[0] in 已印]
    条文 = 截(引(行截('\n'.join(l for l in 条 if l.split('｜', 1)[0] not in 已印), 300)), 1500)
    诸.append(('八', '圣经之锚与事件链之题、检察官 OPEN_BRIEF_CARD_SCHEMA 本章与下一章之行、open_brief（全块）、前章之条（式样）', [
        (圣档, 行截(锚, 400)),
        (os.path.join('工具', '小说检察官.py'), '〔检察官·OPEN_BRIEF_CARD_SCHEMA〕\n' +
         (行截(行们(检, r'^\s+(%d|%d):\s*\(' % (N, N + 1), 1, 0, 6), 600) or '（无本章与下一章之行）')),
        (os.path.join('设定', 'canon事实库.json'), '〔open_brief〕\n' + (json.dumps(ob, ensure_ascii=False, indent=1) if ob else '（open_brief 不在）')),
        (圣档, '〔圣经·第 %d 章之条（式样%s）〕\n' % (N - 1, '；:%s 即上之锚行，⛔重印' % _号段(重) if 重 else '') + 条文)]))
    # ★1020 X36③：本章卡与下一章卡里「圣经:NNNN」所指之行——上已印者（锚行、前章之条）⛔重印、注其号
    已见 = 已印 | set(re.findall(r'^(\d+)｜', 条文, re.M))
    引们 = [(p, _圣经之引(t)) for p, t in zip(卡档, (卡, 下卡)) if t]
    号们 = list(dict.fromkeys(k for _, ks in 引们 for k in ks))[:24]
    if 号们:
        G = 圣.split('\n')
        新 = [k for k in 号们 if str(k) not in 已见 and 0 < k <= len(G)]
        补们['八'] = ('；补：卡所引圣经之行', [(圣档, '〔补·卡所引圣经之行（%s%s）〕\n' % (
            '；'.join('%s 引 :%s' % (p, _号段(ks)) for p, ks in 引们 if ks),
            '；:%s 已见上，⛔重印' % _号段([k for k in 号们 if str(k) in 已见]) if len(新) < len(号们) else '') +
            (行截('\n'.join('%d｜%s' % (k, G[k - 1]) for k in 新), 400) or '（所引之行俱已见上或逾档末）'))])
    # 九、下一章：总纲、余章总案之短行在前，段案之节殿後（★1020 X15 验席：旧段案在前，一逾界先丢的是总纲、余章总案之行）
    段源, 段文, 段目 = _段案(N + 1, root)
    纲档, 案档 = os.path.join('设定', '02_余章之势_总纲.md'), os.path.join('设定', '剧情庭题', '余章总案.md')
    纲, 案 = 读(纲档, root), 读(案档, root)
    A = 案.split('\n')
    二起 = next((i for i, l in enumerate(A) if l.startswith('## 二、')), None)
    二止 = next((i for i in range((二起 or 0) + 1, len(A)) if A[i].startswith('## ')), len(A)) if 二起 is not None else None
    诸.append(('九', '下一章（%d）：总纲之行、余章总案本站之行、段案之节；开镜卡以「python3 工具/第零轮开镜庭.py --立 %d」起' % (N + 1, N + 1), [
        (纲档, '〔总纲·%d、%d 之行〕\n' % (N + 1, N + 2) + (行们(纲, r'\| *(%d|%d) *\|' % (N + 1, N + 2), 0, 0, 6) or '（无）')),
        (案档, '〔余章总案·§四 %d 之行%s〕\n' % (N + 1, '' if 二起 is None else '；§二解歧之裁在 :%d—%d（sed -n 读）' % (二起 + 1, 二止)) +
         (行们(案, r'^- %d ' % (N + 1), 0, 0, 3) or '（无）')),
        (段源, ('〔%s·%d 之节；段头与附录不汇（sed -n 读）：%s〕\n' % (段源, N + 1, '｜'.join(段目)) + 引(段文)) if 段文 else '（段案无其节）')]))
    # 十、同线前章之白文（带行号）——冷眼轮之冷读、承前之判（开轮⑮比其末五段之骨）；极短段之比已归 封版 --前 ⑥
    import 造式验
    本线 = 造式验.线(N, root)
    同 = next((k for k in range(N - 1, N - 13, -1) if 本线 and 造式验.线(k, root) == 本线), None)
    if 同 and 同 != N - 1:
        p同, L同 = _白行(同, root)
        诸.append(('十', '同线前章（第%d章）之白文（行号即整档之行）——冷眼轮之冷读、承前之判（开轮⑮）、收句之骨' % 同,
                    '〔%s〕\n' % p同 + '\n'.join('%d｜%s' % x for x in L同), p同))
    # 十一、人物状态册之行
    def 册之行(人):
        出 = []
        for 名, 中, v in 人:
            区 = _册之区(v.get('名'), root)
            出.append('〔%s%s〕%s' % (v.get('名'), '·%s:%d—%d' % (册档, 区[0] + 1, 区[1]) if 区 else '', _册行(v)))
        return 出
    行 = 册之行(人们)
    if 卡人:    # ★1020 X36④：卡·问九之二所列而白文未见之人之册行
        补们['十一'] = ('；补：卡·问九之二所列之人', [(册档, '〔补·卡·问九之二所列而白文未见之人（%s）〕\n' % 卡档[0] + '\n'.join(册之行(卡人)))])
    if 行 or 卡人:
        诸.append(('十一', '人物状态册之行（在场之人；留末一态、列留末二条——添「%d态」照此式；全行看其区）' % N, '\n'.join(行), 册档))
    # 十二、canon 卡名与一卡之式、大师进化账之末
    try:
        卡们 = [c for c in ((canon or {}).get('state_canon') or []) if isinstance(c, dict)]
    except Exception:
        卡们 = []
    名们 = [x for _, 中, v in 人们 for x in [re.sub(r'（[^）]*）', '', v.get('名') or '')] + 中 if len(x) >= 2 and not x.startswith('（')]
    近 = [c.get('what', '') for c in 卡们 if (isinstance(c.get('from'), int) and c['from'] >= N - 15) or any(x in str(c.get('what', '')) for x in 名们)]
    式卡 = max(卡们, key=lambda c: c.get('from') if isinstance(c.get('from'), int) else -1) if 卡们 else None
    进 = 读(os.path.join('设定', '大师进化账.md'), root).rstrip('\n').split('\n')
    诸.append(('十二', 'canon state_canon 卡名（近十五章所立、或提在场之人者；open_brief 之 required_state_cards 照此择）、一卡之式、大师进化账末三行', [
        (os.path.join('设定', 'canon事实库.json'), '\n'.join('- ' + x for x in 近[-60:]) + '\n\n〔state_canon·末立之一卡（式样）〕\n' +
         (截(json.dumps(式卡, ensure_ascii=False), 500) if 式卡 else '（无）')),
        (os.path.join('设定', '大师进化账.md'), '〔设定/大师进化账.md·末三行（式样；教训追加於档末）〕\n' +
         '\n'.join('%d｜%s' % (len(进) - 2 + k, 截(l, 200)) for k, l in enumerate(进[-3:])))]))
    # ★1020 X36·成节：补之池＝Σ界−Σ旧体之实（截於其旧界後），依 补序 先短後长分之，各⛔逾其补界——全档 ≤ Σ界＋头
    诸 = [x + ('',) * (4 - len(x)) for x in 诸]       # 多源之节无「源」一格
    池 = sum(界.values()) - sum(_用(号, 体, 源) for 号, _, 体, 源 in 诸)
    额 = {}
    for 号 in 补序:
        if 号 in 补们 and any(号 == x[0] for x in 诸):
            额[号] = max(0, min(补界[号], 池))
            池 -= len(_截(补们[号][1], 额[号])[0].encode())
    出 += [节(号, 标 + (补们[号][0] if 号 in 额 else ''), 体, 源, 补们[号][1] if 号 in 额 else None, 额.get(号, 0))
          for 号, 标, 体, 源 in 诸]
    return '\n'.join(出)


def 自测():
    ok = 共 = 0
    共 += 1; ok += 行们('a\nb 12\nc', r'12', 1, 1) == '1｜a\n2｜b 12\n3｜c'
    共 += 1; ok += 节('三', '', '') == '\n## 【三】\n\n（无）\n'
    t = 汇(388)
    共 += 1; ok += all(k in t for k in ('【一】前章回执之式', '| 387 | 锁定 |', '【四】全书记忆', '【五】本章白文里出现之人', '【九】下一章（389）'))
    共 += 1; ok += ('### 刘二' in t or '### 钱满' in t)                  # 在场之人认得出（册之式 1015 自测逮：旧当作 dict）
    # ★1016（393 封版逮）：量限不钉 388——其料取自日增之账（总览、物件、状态册），钉旧章则账一长即红（二十八之家）；量今之末章
    末 = max([int(m.group(1)) for f in glob.glob(os.path.join(ROOT, '版本', '第*章')) for m in [re.search(r'第(\d+)章$', f)] if m and 章白(int(m.group(1)))[0]] or [388])
    t末 = 汇(末)
    共 += 1; ok += len(t末.encode()) <= 限
    # ── ★1020 W53·X15 之格 ──
    # ⑥节之界：逾界即截、印其略；Σ界＋诸题之界 < 限（结构上逾不了——旧无界，394 161KB）
    大 = 节('一', '甲', '\n'.join('行%05d' % i for i in range(5000)), 'x.md')
    共 += 1; ok += (len(大.encode()) <= 界['一'] + 300 and '逾界' in 大 and 'x.md' in 大 and sum(界.values()) + 头之界 < 限)
    # ⑦回灌旧病（料随章长与在场人数而涨）：八倍之章、全册之人俱在场——记料仍 ≤ 限（旧式量之 ≫150KB）
    _册 = json.load(open(os.path.join(ROOT, 册档), encoding='utf-8'))
    _诸名 = '、'.join(re.sub(r'（[^）]*）', '', v.get('名') or '') for v in _册.get('人物') or [])
    _f, _白 = 章白(末)
    _旧章白, _旧白行 = globals()['章白'], globals()['_白行']
    _p, _L = _白行(末)
    try:
        globals()['章白'] = lambda n, root=ROOT: (_f, (_白 + _诸名 + '\n') * 8)
        globals()['_白行'] = lambda n, root=ROOT: (_p, _L * 8)
        胀文 = 汇(末)
        胀 = len(胀文.encode())
    finally:
        globals()['章白'], globals()['_白行'] = _旧章白, _旧白行

    def _头(t):
        """诸节之体以外之字节：档头、节题、逾界之注（结构之界里「头之界」所管者）。"""
        n, 入 = 0, False
        for l in t.split('\n'):
            入 = 入 or l.startswith('## 【')
            if not 入 or l.startswith(('## 【', '（本节逾界')):
                n += len(l.encode()) + 1
        return n
    # ★1020 X15 验席（头之界只是自测里一个常数，码里不强制）：压测之档头、节题、逾界之注实量 ≤ 头之界，则 Σ界＋头之界 < 限 方成其证
    共 += 1; ok += 胀 <= 限 and _头(胀文) <= 头之界 and 胀 <= sum(界.values()) + 头之界
    # ⑧回灌旧病（暗线·她之镜之章无一人在场）：397 之「她」须认作沈鸢（旧以 str(别称) 拆，395、397 五、十一两节空）
    _, 白397 = 章白(397)
    共 += 1; ok += ('沈鸢' in [x[0] for x in 在场(白397, 397, _册)] and '霍钧' not in [x[0] for x in 在场(白397, 397, _册)])
    # ⑨回灌旧病（引档之节撞记料之节）：记料里「## 」起之行唯自家之「## 【」
    共 += 1; ok += all(l.startswith('## 【') for l in t末.split('\n') if l.startswith('## '))
    # ⑩回灌旧病（检察官之行恒空：旧式「^ N:」认不着四格缩进）：末章之记料须带 OPEN_BRIEF_CARD_SCHEMA 本章之行
    共 += 1; ok += bool(re.search(r'\d+｜\s+%d:\s*\(' % 末, t末))
    # ── ★1020 X15·独立验席所逮（【九】之界与段案之取相撞、逾界之注指错档、【八】锚行印两回）之格 ──
    # ⑪回灌旧病（段案之取连附录）：段案档末一章之後之「## 附一·落账」⛔取入（旧式止於「## 数」，400 之节取成 16KB）；附录入目、带行号
    import tempfile, shutil
    _d = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(_d, '设定', '段案'))
        open(os.path.join(_d, '设定', '段案', '1-2.md'), 'w', encoding='utf-8').write(
            '# 段案·1—2\n> 律\n## 1\n- 一\n## 2\n- 二\n## 附一·落账\n| 甲 |\n')
        _源, _文, _目 = _段案(2, _d)
    finally:
        shutil.rmtree(_d, ignore_errors=True)
    共 += 1; ok += (_源 == os.path.join('设定', '段案', '1-2.md') and _文 == '## 2\n- 二' and _目 == ['段头 :1—2', '附一·落账 :7—8']
                    and all(not re.search(r'^## (?!%d\s*$)' % n, _段案(n)[1], re.M) for n in range(末 - 15, 末 + 4)))
    # ⑫回灌旧病（逾界之注指错档）：多源之节，注只列被截诸片之源——截在尾片者⛔列前片；截入前片者两源俱列
    _短, _长 = '322｜| 398 | 主·157 |', '\n'.join('段%05d' % i for i in range(4000))
    _甲 = 节('九', '', [('纲.md', _短), ('段.md', _长)])
    _乙 = 节('九', '', [('段.md', _长), ('纲.md', _短)])
    共 += 1; ok += (_短 in _甲 and '所略之源 段.md——' in _甲 and '纲.md' not in _甲.split('（本节逾界')[1]
                    and '所略之源 段.md、纲.md' in _乙)
    # ⑬回灌旧病（总纲、余章总案之行被段案挤掉）：【九】总纲、余章总案在前，段案之节殿後；段案之节⛔带附录
    _九 = t末.split('## 【九】')[1].split('\n## 【')[0] if '## 【九】' in t末 else ''
    _位 = [_九.find(x) for x in ('〔总纲·', '〔余章总案·', '之节；段头与附录不汇')]
    共 += 1; ok += (0 <= _位[0] < _位[1] and (_位[2] < 0 or _位[1] < _位[2]) and '〉## 附' not in _九
                    and (('（本节逾界' not in _九) or re.search(r'所略之源 设定/段案/[^、—]+——', _九) is not None))
    # ⑭回灌旧病（【八】锚行印两回：398 前章之条含 9924—9926）：圣经之行号於【八】只现一回
    def _八号(t):
        八 = t.split('## 【八】')[1].split('\n## 【')[0]
        锚, 条 = 八.split('〔检察官')[0], (八.split('〔圣经·第')[1] if '〔圣经·第' in 八 else '')
        return re.findall(r'^(\d+)｜', 锚, re.M), re.findall(r'^(\d+)｜', 条, re.M)
    t398 = 汇(398)
    _锚号, _条号 = _八号(t398)
    共 += 1; ok += bool(_锚号) and not set(_锚号) & set(_条号) and len(_锚号) == len(set(_锚号))
    # ── ★1020 X36 之格（四样各一格，并补之池一格）；钉已封之 399（七份构思、黎东来镜、卡引圣经:1950、:2644、管章的人只以纸到场）──
    t399 = t末 if 末 == 399 else 汇(399)

    def _节(t, k):
        return t.split('## 【%s】' % k)[1].split('\n## 【')[0] if '## 【%s】' % k in t else ''
    _T = 读(表)
    _卡399 = 读(os.path.join('版本', '第399章', '_开镜卡.md'))
    # ⑮回灌旧病（满分之问只列档名，399 记席甲、己、庚另 sed）：七份之「## 满分之问」头行带其行号俱在【七】之补；三种写法俱在拍表之前；
    #   拍表或全在、或其略注明其源（池不足时先截拍表）
    _七 = _节(t399, '七')
    _构 = sorted(glob.glob(os.path.join(ROOT, '版本', '第399章', '起草_*_构思.md')))
    _头行 = []
    for p in _构:
        L = open(p, encoding='utf-8').read().split('\n')
        i = next((i for i, l in enumerate(L) if l.startswith('#') and '满分之问' in l), None)
        _头行.append('%d｜%s' % (i + 1, L[i]) if i is not None else None)
    _补位 = _七.find('〔补·诸构思')
    _表位 = [_七.find('·满分之问之拍表〕')] + [_七.find(h) for h in _头行 if h]
    #   ★1020 X36 驳席：圈号起之「② ## 满分之问」「② 满分之问」（386—397 十八份；397 甲、戊）须认得、止於「③」行之前
    _圈 = [_满分之段(open(os.path.join(ROOT, '版本', '第397章', '起草_%s_构思.md' % g), encoding='utf-8').read()) for g in '甲戊']
    共 += 1; ok += (len(_构) == 7 and all(_头行) and 0 <= _补位 < min(_表位[1:])
                    and (max(_表位[1:]) < _表位[0] or (_表位[0] < 0 and '（本节逾界·补额' in _七))   # 驳席：拍表全截（账长池瘦）亦合其注，⛔红
                    and ('（本节逾界·补额' not in _七 or re.search(r'补额.*所略之源 版本/第399章/起草_._构思\.md', _七) is not None)
                    and _满分之段('# 题\n① 甲\n② 满分之问\n- 写法甲\n③ 乙') == '3｜② 满分之问\n4｜- 写法甲'
                    and _圈[0].startswith('7｜② ## 满分之问') and _圈[1].startswith('4｜② 满分之问')
                    and not any(re.search(r'^\d+｜③', x, re.M) for x in _圈))
    # ⑯回灌旧病（同镜前章之悬账另翻）：399 黎东来镜之同镜前章係 389（⛔同线 397）、395 她之镜越 389 黎东来、391／393 霍钧取 387；
    #   本章锁定行未立（记席跑记料之时）则取卡之「本章之镜」；同镜无前（391 霍钧首见）照旧取同线；【二】之补带 389 之悬账行
    _T去 = re.sub(r'^\| 399 \| 锁定 \|.*\n', '', _T, flags=re.M)
    共 += 1; ok += (_同镜(399, _T, _卡399) == (389, '黎东来', '同镜') and _同镜(399, _T去, _卡399) == (389, '黎东来', '同镜')
                    and _同镜(395, _T, '')[0] == 387 and _同镜(391, _T, '')[2] == '同线'
                    and _同镜(396, _T, '')[0] == 394       # 驳席：锁定行「镜：我」须归一作苏衍（⛔跳去 374 之「我」）
                    and _卡之镜('- **本章之镜**：黎东来（第三人称；⛔沈鸢、苏衍）', {'苏衍', '沈鸢', '黎东来'}) == '黎东来'
                    and re.search(r'^\d+｜\| 389 \| 悬账 \|', _节(t399, '二'), re.M) is not None
                    and re.search(r'^\d+｜\| 396 \| 悬账 \|', _节(t398, '二'), re.M) is not None)
    # ⑰回灌旧病（卡所引圣经行料外另查）：「圣经:1950、:2644」「圣经:12—14」之认；399 之【八】印 1950、2644 各一回，【八】之行号⛔重
    _八 = _节(t399, '八')
    _八号们 = re.findall(r'^(\d+)｜', _八.split('〔检察官')[0] + '\n' + _八.split('〔圣经·第')[-1], re.M)
    共 += 1; ok += (_圣经之引('圣经:1950、:2644；`圣经：12—14`，圣经七·9') == [1950, 2644, 12, 13, 14]
                    and _圣经之引('`圣经:7408`／`:8161`；`圣经:8496`／`施工表:305`；圣经:1950—52') == [7408, 8161, 8496, 1950]
                    and '\n1950｜' in _八 and '\n2644｜' in _八 and len(_八号们) == len(set(_八号们)))
    # ⑱回灌旧病（只以纸到场之人不在【五】）：管章的人（399 卡·问九之二之注）入【五】【十一】之补；「永不回」之句⛔收（录入的那个）；白文之人仍在补前
    _五, _十一 = _节(t399, '五'), _节(t399, '十一')
    _卡人, _无册 = _卡之人('## 问九之二\n- **甲某**｜在场\n- **乙某**（不出场）｜x\n  - 注：丙某只以纸到场；丁某永不回\n---\n- **戊某**',
                         {'人物': [{'名': n} for n in ('甲某', '乙某', '丙某', '丁某', '戊某')]}, {'甲某'})
    共 += 1; ok += ('### 管章的人（卡·问九之二所列' in _五 and '录入的那个' not in _五 and '〔管章的人·' in _十一
                    and -1 < _五.find('### 黎东来') < _五.find('〔补·卡') and [x[0] for x in _卡人] == ['乙某', '丙某'] and _无册 == [])
    # ⑲补之池：旧体先截於其旧界、一字不让补；补殿其後、截於补额而注其源；399、398 之记料 ≤ Σ界＋头之界
    _旧 = 节('九', '', [('纲.md', _短), ('段.md', _长)])
    _新 = 节('九', '', [('纲.md', _短), ('段.md', _长)], 补=[('补.md', '\n'.join('补%04d' % i for i in range(900)))], 补额=2000)
    共 += 1; ok += (_新.startswith(_旧.rstrip('\n')) and '补0000' in _新 and '补0899' not in _新
                    and re.search(r'（本节逾界·补额 2000 字节：补下略 \d+ 行.*所略之源 补\.md——', _新) is not None
                    and max(len(t399.encode()), len(t398.encode())) <= sum(界.values()) + 头之界)
    print('记料·自测 %d/%d（%d 之记料 %d 字节；八倍之章、全册在场 %d 字节·头 %d；399 %d 字节；限 %d）' % (
        ok, 共, 末, len(t末.encode()), 胀, _头(胀文), len(t399.encode()), 限))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) == 1 and a[0].isdigit():
        N = int(a[0]); t = 汇(N)
        p = os.path.join(ROOT, '版本', '第%d章' % N, '_记料.md')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(t)
        b = len(t.encode())
        print('✓ 写 %s（%d KB）%s' % (os.path.relpath(p, ROOT), b // 1024, '' if b <= 限 else '　⛔逾 150KB（坑③）'))
        sys.exit(0 if b <= 限 else 1)
    print(__doc__); sys.exit(2)
