#!/usr/bin/env python3
"""封版（1013 立·造式二代·设定/方法升级_造式二代.md §五之五）——封版诸件之跑器、核数、提交、备份，归脚本。

为何立：一代之案席与封版席两席（380：$19.65＋$31.88，来回 414 回）大半在跑器、核数、提交、备份——机器之活。
二代拆开（零 token 之检）：
  · 读懂了才写得出之档（回执之文、锁定行逐拍、创作记录、全书记忆、状态册、open_brief、下一章开镜卡）——记席（造章.js 之末席）；
  · 其余——存版对表、造式之实、锁定行之数、坑账之单、诸闸、第十一轮、全测、提交、双备份、存底包、撤锁——本器。

用法：
  python3 工具/封版.py N --前        # 记席先跑：对表（正文≠末版即存一版）、造式之实、锁定行之数、坑账之单、前章回执与锁定行之样
  python3 工具/封版.py N --前 --红   # 复跑只印红：⛔ 项（新红／变）、较上回之变、上回红今已绿，末行「✓ 余 N 项俱绿」（上回之印存 .cache/封版前/；首跑全印）
  python3 工具/封版.py N --後        # 记席毕、主环跑：验记席之档俱在 → 诸闸 → 第十一轮 → 全测 → 提交 → 存底与存底包 → 撤锁（红即停、⛔提交）
  python3 工具/封版.py N --後 --试   # 只跑诸闸与第十一轮之验，⛔写、⛔提交、⛔存底（演练用）
  python3 工具/封版.py --自测         # 以已封版之 380 之真料核诸数（与其锁定行亲核之数逐个同）
次序之据：开轮六检於第十一轮之前跑（旧⑭「封版之章不得再跑十轮」1027 汰——其防移 续跑之守：已封之 N ⛔再派造章）。
推送：本器⛔推主枝；其末 `存底 --标` 推「章-N」即触 GitHub autopush（推时即闸、绿即并入主枝、果入 备份/报）——
  跑毕主环 `python3 工具/接棒守.py --候主 N`（run_in_background、零 token：主枝含即快进返 0、坏报即返其红）；
  ⛔即跑 推.py（1027 坑51：旧印「下一步 推.py」，沙盒直推抢先、GitHub 之推恒 non-fast-forward 而败，一章之树三跑闸）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, time, hashlib, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
施工表 = os.path.join('设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
总纲 = os.path.join('设定', '02_余章之势_总纲.md')
尾 = 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825'


def 正文档(n, root=ROOT):
    from 对账预筛 import 章号
    for f in glob.glob(os.path.join(root, '正文', '*.md')):
        if 章号(f) == n:
            return f
    return None


def 跑(a, root=ROOT, 限=900):
    t = time.time()
    try:
        r = subprocess.run([sys.executable] + a if a[0].endswith('.py') else a, cwd=root, capture_output=True, text=True, timeout=限)
        return r.returncode, r.stdout + r.stderr, time.time() - t
    except subprocess.TimeoutExpired:
        return 124, '（逾 %d 秒未毕）' % 限, time.time() - t


def 器(名):
    return os.path.join(ROOT, '工具', 名)


def 数(n, root=ROOT):
    """锁定行之机器之数（⛔凭空写一个数即是造数）。"""
    f = 正文档(n, root)
    if not f:
        return {'坏': '第%d章之正文不在' % n}
    文 = open(f, encoding='utf-8').read()
    L = 文.split('\n')
    亮 = next((i + 1 for i, l in enumerate(L) if '【本章亮点】' in l), None)
    白止 = (亮 - 1) if 亮 else len(L)
    while 白止 > 1 and not L[白止 - 1].strip():
        白止 -= 1
    星 = sum(1 for l in L[:白止] if l.strip() == '＊')
    import 净重对表
    d = {'正文': os.path.relpath(f, root), '白文': '1 至 %d 行' % 白止, '亮点行': 亮, '净重': 净重对表.净重(f),
         '＊': 星, '拍': 星 + 1, 'sha1': hashlib.sha1(文.encode('utf-8')).hexdigest()[:12]}
    台 = os.path.join(root, '版本', '第%d章' % n, '_台账.json')
    if os.path.exists(台):
        版们 = json.load(open(台, encoding='utf-8')).get('版本', [])
        if 版们:
            末 = 版们[-1]
            d['末版'] = 末.get('版')
            s = 末.get('soft')
            s = eval(s, {}) if isinstance(s, str) else (s or {})      # 台账之 soft 以 Python 字面存（跑轮所写）
            d['六数'] = '净重%s｜段数%s｜长段数%s｜嗅%s｜触%s｜四字串三现%s' % tuple(s.get(k, '?') for k in ('净重', '段数', '长段数', '嗅', '触', '四字串三现'))
            d['诸版'] = ['%s %s「%s」' % (v.get('版'), v.get('时', ''), str(v.get('说明', ''))[:40]) for v in 版们]
            末档 = os.path.join(root, '版本', '第%d章' % n, '%s.md' % 末.get('版'))
            d['与末版同'] = os.path.exists(末档) and open(末档, encoding='utf-8').read() == 文
    m = re.search(r'\|\s*%d\s*\|\s*([主暗]·\d+)\s*\|' % n, open(os.path.join(root, 总纲), encoding='utf-8').read())   # 两栏排，整行逐栏认
    d['总纲'] = '| %d | %s |' % (n, m.group(1)) if m else None
    return d


_引式 = re.compile(            # ★W60 X37：骨记之「章:行」——全角半角冒号、区间（至／—／-，後端可复书其章）、本章（：行）、续前一引之章（、：行）
    r'(?<![\dA-Za-zＡ-Ｚａ-ｚ０-９_#/.\-])(\d{1,3})[:：](\d{1,4})(?:\s*(?:至|—|–|-|～|~)\s*(?:(\d{1,3})[:：])?(\d{1,4}))?'
    r'|(?<=[（(])[:：](\d{1,4})(?:\s*(?:至|—|–|-|～|~)\s*(\d{1,4}))?(?=\s*[）)、，,])'
    r'|(?<=、)[:：](\d{1,4})(?:\s*(?:至|—|–|-|～|~)\s*(\d{1,4}))?')
_原句式 = re.compile(r'[ \t]*[）)]?[ \t]*「([^」\n]+)」')       # 紧随其引之「原句」（「（：23）「……」」之式容一「）」）
_略 = re.compile(r'……|…|⋯+|\.\.\.|／')                        # 原句内之略与分行：逐段各核
_标 = '，。！？、；：,.!?;:…—「」『』“”‘’"\'（）()·｜|\\s'


def _净(s):
    """⛔比标点之引号与空白：骨记以「」引，白文之对白是“”，引中之引是『』。"""
    return re.sub(r'[\s「」『』“”‘’"\']', '', s)


def 骨引(骨, n):
    """骨记之诸引 → [{章, 起, 止, 句, 前文, 後文, 原}]。句＝紧随之「原句」（无则 None＝远引）；前文／後文＝其引所在小句之文（供远引之核）。
    ⛔认：字母之後之号（Ｄ6：164、W33:）、跨章之区间；「总纲：325」之类（冒号前无章号、亦非「（：」）非章之引。"""
    出 = []; 前章 = None
    for m in _引式.finditer(骨):
        if m.group(1):
            c, a = int(m.group(1)), int(m.group(2))
            if m.group(3) and int(m.group(3)) != c:
                前章 = None; continue
            b = int(m.group(4)) if m.group(4) else a
        elif m.group(5):
            c, a = n, int(m.group(5)); b = int(m.group(6)) if m.group(6) else a
        else:
            if 前章 is None:
                continue
            c, a = 前章, int(m.group(7)); b = int(m.group(8)) if m.group(8) else a
        前章 = c
        q = _原句式.match(骨, m.end())
        i = max(骨.rfind(x, 0, m.start()) for x in '｜|；;。\n')
        j = [k for k in (骨.find(x, m.end()) for x in '）)｜|；;。\n') if k >= 0]
        出.append({'章': c, '起': a, '止': max(a, b), '句': q.group(1) if q else None, '原': m.group(0),
                   '前文': 骨[i + 1:m.start()].rstrip(' \t（(')[-40:], '後文': 骨[m.end():min(j) if j else len(骨)][:40]})
    return 出


def 共串(甲, 乙, 下=4):
    """甲之一串（⛔跨标点）逐字在乙者，取其最长；短於「下」字者 ''。"""
    乙 = _净(乙); 最 = ''
    for 段 in re.split('[%s]+' % _标, 甲):
        for i in range(len(段)):
            j = i + max(下, len(最) + 1)
            while j <= len(段) and 段[i:j] in 乙:
                最 = 段[i:j]; j += 1
    return 最 if len(最) >= 下 else ''


def 核引(引, 白们):
    """一引 → (类, 合否, 注)。类：原句／远引／短（原句不足四字·不核）。白们：章 → 白文之行（行号与档同）。
    原句：全句逐段核（⛔旧式只核句首二十四字）——以略号与「／」切段，凡四字以上之段俱须逐字在所引之行·±1（区间则其起－1 至止＋1）；
    远引：骨记其小句之文与所引之行·±1 之最长逐字共串（四字以上方算），注即其串；无者注空，由印者印所引之行。"""
    L = 白们.get(引['章'])
    类 = '远引' if 引['句'] is None else '原句'
    if L is None:
        return 类, False, '所引之章不在'
    if 引['起'] > len(L):
        return 类, False, '行逾其白文（%d 行）' % len(L)
    lo, hi = max(1, 引['起'] - 1), min(len(L), 引['止'] + 1)
    窗 = '\n'.join(L[lo - 1:hi])
    if 类 == '远引':
        s = 共串(引['前文'] + '｜' + 引['後文'], 窗)
        return 类, bool(s), s
    段们 = [s for s in (_净(x) for x in _略.split(引['句'])) if len(re.sub('[%s]' % _标, '', s)) >= 4]
    if not 段们:
        return '短', True, ''
    缺 = [s for s in 段们 if s not in _净(窗)]
    if not 缺:
        return 类, True, ''
    实 = [k for k, l in enumerate(L, 1) if 缺[0] in _净(l)]
    return 类, False, ('实在 :%s' % '、:'.join(map(str, 实[:3]))) if 实 else '所引之章无此句'


def 骨引之核(骨, n, root=ROOT, 白们=None):
    """→ [(引, 类, 合, 注, 所引之章之白文行)]。白们缺省则只载所引诸章之白文（⛔全书）。"""
    引们 = 骨引(骨, n)
    if 白们 is None:
        import 章料
        白们 = {}
        for c in sorted({x['章'] for x in 引们}):
            f = 章料.章档(c, root)
            if f:
                t = open(f, encoding='utf-8').read(); i = t.find('【本章亮点】')
                白们[c] = (t[:i] if i >= 0 else t).split('\n')
    出 = []
    for x in 引们:
        类, 合, 注 = 核引(x, 白们)
        出.append((x, 类, 合, 注, 白们.get(x['章'])))
    return 出


def 骨引之印(核):
    """骨引之核 → 机械之证之①（一项；远引诸行以换行续之）。"""
    def 号(x):
        return '%d:%d' % (x['章'], x['起']) + ('—%d' % x['止'] if x['止'] > x['起'] else '')
    原 = [k for k in 核 if k[1] == '原句']; 短 = [k for k in 核 if k[1] == '短']; 远 = [k for k in 核 if k[1] == '远引']
    坏 = ['%s「%s」%s' % (号(x), x['句'][:20], 注) for x, _, 合, 注, _L in 原 if not 合]
    s = '①骨记引句（章:行「原句」·含区间、全角冒号、本章（：行））%d/%d 合｜不合 %d%s%s' % (
        len(原) - len(坏), len(原), len(坏), ('：' + '；'.join(坏[:30])) if 坏 else '（俱四字以上逐字在所引之章之行·±1）',
        '｜不足四字不核 %d' % len(短) if 短 else '')
    if 远:
        共 = [k for k in 远 if k[2]]; 余 = [k for k in 远 if not k[2]]
        s += '\n      ①之二·骨记远引（章:行 而无「原句」）%d 处：骨记之文四字以上逐字在所引之行·±1 者 %d/%d%s' % (
            len(远), len(共), len(远), ('（' + '、'.join('%s「%s」' % (号(x), 注) for x, _, _, 注, _L in 共[:40]) + '）') if 共 else '')
        if 余:
            s += '；余 %d 处印所引之行（记席照此判、⛔再 awk）：' % len(余)
            for x, _, _, 注, L in 余[:40]:
                if 注:
                    行 = '（%s）' % 注
                else:                    # 所引之行（区间则连其诸行）；骨记之文有三字以上落在其行·±1 者，截其近处，否则截行首
                    窗 = _净(''.join(L[max(1, x['起'] - 1) - 1:min(len(L), x['止'] + 1)]))
                    本 = _净(''.join(L[x['起'] - 1:x['止']]))
                    近 = 共串(x['前文'] + '｜' + x['後文'], 窗, 3)
                    p = max(0, 窗.find(近) - 20) if 近 else -1
                    行 = '「%s」' % (('…' if p > 0 else '') + 窗[p:p + 100] if p >= 0 else 本[:100])
                s += '\n        %s%s ← 骨「%s‖%s」' % (号(x), 行, x['前文'][-16:], x['後文'][:16])
    return s


def 对白之行(L):
    """白文之行们 → [(行号, 行)]：对白之行（坑⑩·机械之证③）；记落.py 之「‹器:对白›」同此一把尺。"""
    return [(k + 1, l) for k, l in enumerate(L) if '“' in l or re.search(r'「[^」]{1,40}」[，。！？]?(?:他|她|我|钱满|刘二|东头|老头)?说', l)]


def 机械之证(n, root=ROOT):
    """★1015 W33 之改（390 之试：记席 58 工具里翻查 32——坑账之答所须之据由模型逐条 grep）：
    据之可机算者器先算——①骨记引句逐条核於所引之章（坑㉕；★W60 X37：含区间、本章、远引——远引无原句者印所引之行）②卡之⛔字在白文之数（坑⑱）③对白之行（坑⑩）④日词（坑⑫）⑤数词之行（坑㉘）
    ⑥极短段之比：本章与同线前三章（坑账 P39；★1016 X06 之补——旧缺此项，391、393 记席每章自算）。
    ⛔判：只交据；犯没犯仍由记席判。"""
    import 章料
    f = 章料.章档(n, root)
    t = open(f, encoding='utf-8').read()
    i = t.find('【本章亮点】')
    白, 骨 = (t[:i], t[i:]) if i >= 0 else (t, '')
    L = 白.split('\n'); 出 = []
    # ①骨记之引（★W60 X37：逐条机核——旧式只认「章:行「≤40 字」」一式、只核句首 24 字，398 记席仍亲 awk 远引六处）
    出.append(骨引之印(骨引之核(骨, n, root)))
    # ②卡之⛔字
    卡 = os.path.join(root, '版本', '第%d章' % n, '_开镜卡.md')
    禁 = []
    if os.path.exists(卡):
        kt = open(卡, encoding='utf-8').read()
        禁 = sorted(set(re.findall(r'⛔\s*「([^」]{1,8})」', kt) + re.findall(r'「([^」]{1,8})」\s*⛔', kt)))
    出.append('②卡之⛔字在白文之数：' + ('｜'.join('「%s」%d' % (w, 白.count(w)) for w in 禁[:30]) or '（卡无⛔「字」之式）'))
    # ③对白之行
    对 = 对白之行(L)
    出.append('③对白之行 %d：%s' % (len(对), '、'.join(':%d' % k for k, _ in 对[:40])))
    # ④日词
    日 = [(k + 1, m) for k, l in enumerate(L) for m in re.findall(r'第[零〇一二三四五六七八九十百]+[天日]|昨天|前天|今天|明天|後半夜|天亮|天黑|晌午|後晌|日落', l)]
    出.append('④日词：%s' % ('、'.join(':%d%s' % (k, m) for k, m in 日[:40]) or '无'))
    # ⑤数词之行
    数 = [(k + 1, m) for k, l in enumerate(L) for m in re.findall(r'[零〇一二两三四五六七八九十百千]+(?:个|道|处|回|天|步|指|尺|丈|口|块|张|行|格|刻|时辰|下)', l) if not re.match(r'一[^十百千]', m)]   # 「一个」「一下」之类⛔列（噪）
    出.append('⑤数词 %d 处（先说後数之核）：%s' % (len(数), '、'.join(':%d%s' % (k, m) for k, m in 数[:40])))
    # ⑥极短段之比（P39）：本章与同线前三章，同一把尺（极短段()），旧→新排
    import 造式验
    前三 = 同线前三(n, lambda k: 造式验.线(k, root), lambda k: 章料.章档(k, root) is not None)
    def _比(k):
        短, 共 = 极短段(open(章料.章档(k, root), encoding='utf-8').read())
        return 短, 共, (100.0 * 短 / 共 if 共 else 0.0)
    列 = [(k,) + _比(k) for k in 前三 + [n]]
    率 = [r for *_, r in 列]
    出.append('⑥极短段（≤%d 字）之比｜同线(%s)前三章与本章：%s｜连四章上行：%s' % (
        极短段之限, 造式验.线(n, root) or '?', '→'.join('%d %d／%d＝%.1f%%' % x for x in 列),
        ('是' if all(a < b for a, b in zip(率, 率[1:])) else '否') if len(列) == 4 else '（同线前章不足三，判不出）'))
    return 出


极短段之限 = 15        # ★P39 之尺（382—393 记席同法：≤15 字为极短段）


def 极短段(文, 限=极短段之限):
    """(极短段数, 段数)。段之尺与 跑轮.score 之「段数」同（白文去题行、去空行、去「＊」、去空白）——⛔另造一把尺。"""
    import 跑轮
    段 = [re.sub(r'\s', '', x) for x in 跑轮.body_of(文).split('\n') if x.strip() and x.strip() != '＊']
    return sum(1 for x in 段 if len(x) <= 限), len(段)


def 同线前三(n, 线之, 在=lambda k: True, 远=24):
    """n 之同线（造式验.线）前三章，旧→新；线认不出则 []。"""
    l0 = 线之(n)
    if not l0:
        return []
    得 = []
    for k in range(n - 1, max(n - 远, 0), -1):
        if len(得) == 3:
            break
        if 线之(k) == l0 and 在(k):
            得.append(k)
    return 得[::-1]


def 慢检并起(n, root=ROOT, 隔=0.5):
    """★W60 X39（399 记席 flaws②：--前 逾 120 秒，记席之 Bash 转後台、候二回）——400 於副本实测改前 121.5 秒：
    检察官 --末章 79.9 秒、开轮六检 --静 39.0 秒（二者相继），余检合计约 2 秒。今此二检先并起於後台，余检照序跑；
    印之序照旧（至其位方 result()）。⛔删一检、⛔减其所查：命令一字不改，只改其起之时。
    隔：诸器一载 `_账` 即读改写 `_跑账.json` 一笔（无锁），同刻起则丢一笔——错开半秒起。
    → {'检察官': future→CompletedProcess（与旧之 subprocess.run 同）, '开轮六检': future→(rc, 印, 秒)（与旧之 跑() 同）}"""
    from concurrent.futures import ThreadPoolExecutor
    池 = ThreadPoolExecutor(max_workers=2)
    慢 = {'检察官': 池.submit(subprocess.run, [sys.executable, 器('小说检察官.py'), '--末章', str(n)], cwd=root, capture_output=True, text=True)}
    time.sleep(隔)
    慢['开轮六检'] = 池.submit(跑, [器('开轮六检.py'), str(n), '--静'], root)
    time.sleep(隔)
    池.shutdown(wait=False)          # 不候：二检照跑，至其位 result() 方候
    return 慢


def 前(n, root=ROOT):
    print('════ 封版·前（第%d章）════' % n)
    d = 数(n, root)
    if d.get('坏'):
        print('⛔ ' + d['坏']); return False
    if d.get('与末版同') is False:
        rc, out, _ = 跑([器('跑轮.py'), '--存', str(n), '造式二代·定稿：正文与末版对齐（封版.py --前）'], root)
        print('· 正文与末版不一：已存一版（rc=%d）' % rc)
        d = 数(n, root)
    慢 = 慢检并起(n, root)                                   # ★W60 X39：二慢检先并起於後台（存版之後：其读版本）；余检照序跑、照序印
    rc, out, _ = 跑([器('造式.py'), str(n)], root)
    print('· 造式之实：%s' % (out.strip().split('\n')[-1] if out.strip() else rc))
    print('· 锁定行之数（取此，⛔凭空写）：')
    for k in ('正文', '总纲', '白文', '亮点行', '净重', '六数', '＊', '拍', '末版', '与末版同', 'sha1'):
        print('    %s：%s' % (k, d.get(k)))
    for v in d.get('诸版', []):
        print('    版：' + v)
    rc, out, _ = 跑([器('层census.py'), str(n)], root)
    print('· 层（层census.py %d）：\n%s' % (n, '\n'.join('    ' + l for l in out.strip().split('\n')[-8:])))
    rc, out, _ = 跑([器('坑账.py'), '--逐章', str(n)], root)
    print('· 坑账之单（逐条答进回执「坑账之答」）：\n' + '\n'.join('    ' + l for l in out.strip().split('\n')))
    try:
        print('· 坑账之机械之证（器先算·记席照此答、⛔再逐条 grep——W33 之治：390 记席翻查 32 回多在此）：\n' + '\n'.join('    ' + l for l in 机械之证(n, root)))
    except Exception as _e:
        print('· 坑账之机械之证：⛔算不出（%s）——记席照旧手查' % _e)
    try:                                                     # ★1013：开轮十六检——384 记席未写「承前之判」（⑮），封版·後 方红；今於 --前 即印其红
        rc6, out6, _ = 慢['开轮六检'].result()
        import 全测 as _全测
        余6 = _全测._六检之败(out6)
        print('· 开轮十六检：%s' % ('✓ 俱过' if not 余6 else '⛔ ' + '；'.join(余6)[:600] + '——记席须治（承前之判写进轮记，逐样点名落判：认／翻／搁下）'))
    except Exception as _e:
        print('· 开轮十六检：⛔判不出（%s）' % _e)
    try:                                                     # ★1017：回执闸（小说检察官._receipt_ok）——397 记席之回执缺「到期账」一词，封版·後之全测·快（检察官自测·末章硬闸）方红；今於 --前 即印所缺之键
        import 小说检察官 as _检
        _文 = ''.join(open(_f, encoding='utf-8').read() for _f in _检._receipt_files(n))
        _缺 = [k for k in ('五钩', '伏笔', '新锚', '病历', '清单', '原场', '到期账', '章魂', '生死检', '改动闸', '本章之失') if k not in _文]
        print('· 回执闸：%s' % ('✓ 键俱在' if _检._receipt_ok(n) else '⛔ 回执（设定/回执_*第%d章*.md）缺键：%s——记席照 396 回执之式补其节（到期账：本章动没动 设定/到期账.json、哨与限）' % (n, '、'.join(_缺) or '（档名不认本章）')))
    except Exception as _e:
        print('· 回执闸：⛔判不出（%s）' % _e)
    if os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_器物.md')):     # ★1020：398 治 soft-1 删「本子」於拍5，器物册之「出=5」遂错——全测·快不含逐章回灌，推闸方红；左移於此
        r = subprocess.run([sys.executable, 器('器物点名.py'), str(n)], cwd=root, capture_output=True, text=True)
        _红 = [l.strip() for l in r.stdout.split('\n') if '⛔ ★' in l]
        print('· 器物册（器物点名 %d）：%s' % (n, ('⛔ ' + '｜'.join(_红[:3]) + '——改册之拍号照白文亲数') if (_红 or '⛔' in r.stdout) else '✓ 拍号俱对'))
    主环 = []                                               # ★1024 省 token 之审 records 二·④：N≥411 越职三闸（囤灰闸、跑账、席令之禁）入「主环之职」一栏；质量三闸（含①之e 六问）留记席之栏
    for _名, _令 in (('囤灰闸', ['囤灰闸.py']), ('跑账', ['跑账.py']), ('圣经随裁', ['圣经随裁.py']),
                     ('质量三闸', ['质量三闸.py']), ('席令之禁', ['席令之禁.py'])):   # ★1023 坑㉟复踩：408 新立大审.js 缺律⑮⑳，至 --後 之全测·快（六分）方红——一秒之器左移於此   # ★1022 坑㊹：404 封毕而推闸之质量三闸①之c（一章一日）方红——与推闸同一器左移於 --前   # ★1020 坑㉟：400 封版三回——新器未接未跑、新裁未书圣经之随，至 --後 之全测·快（十分钟後）方红；此三闸各一秒，左移於此
        _r = subprocess.run([sys.executable, 器(_令[0])] + _令[1:], cwd=root, capture_output=True, text=True)
        _红 = [l.strip() for l in _r.stdout.split('\n') if l.strip().startswith('⛔')][:3]   # ⛔取行中之「⛔」：挂账之由文里亦有⛔字
        _行 = '· %s：%s' % (_名, '✓' if _r.returncode == 0 else '⛔ ' + ('；'.join(_红) or 'rc=%d' % _r.returncode)[:400] + '——治後再跑 --前')
        if n >= 分栏之始 and _名 in 主环之闸:
            主环.append('    ' + _行.replace('——治後再跑 --前', '——主环治'))
        else:
            print(_行)
    if n >= 分栏之始:          # ★1027 法用之守：已取之法本章真用上了没有（--前：记席之後方有之证免）——主环之职，--後 照拦
        _r = subprocess.run([sys.executable, 器('法用之守.py'), '--验', str(n), '--前'], cwd=root, capture_output=True, text=True)
        _红 = [l.strip() for l in _r.stdout.split('\n') if l.strip().startswith('⛔')][:3]
        主环.append('    · 法用之守：%s' % ('✓' if _r.returncode == 0 else '⛔ ' + ('；'.join(_红) or 'rc=%d' % _r.returncode)[:400] + '——主环治'))
    r = 慢['检察官'].result()   # ★1020：398 亮点 5+逗 至封版·後之全测·快（十一分钟後）方红——检察官之末章硬闸单跑左移於此（W60 X39：已於上并起）
    _病 = 末章之病(r.stdout) if r.returncode else []
    print('· 末章硬闸（检察官）：%s' % ('✓ 通过' + ('（第十一轮归 --後）' if r.returncode else '') if not _病 else '⛔ ' + '；'.join(_病)[:600] + '——治後再跑 --前'))
    try:                                                     # ★1013：六问（质量三闸①之e）——381 记席未答，封版之全测方红；今於 --前 即印
        import 质量三闸
        _名, _过, _语 = 质量三闸.gate1e(n)[0]
        print('· 六问：%s %s%s' % ('✓' if _过 else '⛔', _语, '' if _过 else '——记席须於轮记之首答六条（造章.js 记令 2之二）'))
    except Exception as _e:
        print('· 六问：⛔判不出（%s）' % _e)
    回 = sorted(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % (n - 1))))
    print('· 前章回执之样：%s' % (os.path.relpath(回[-1], root) if 回 else '（无）'))
    t = open(os.path.join(root, 施工表), encoding='utf-8').read()
    样 = [l[:120] + '…' for l in t.split('\n') if l.startswith('| %d | 锁定 |' % (n - 1)) or l.startswith('| %d | 悬账 |' % (n - 1))]
    print('· 前章锁定行与悬账行之样（施工表）：\n' + '\n'.join('    ' + x for x in 样))
    if 主环:
        print('· 主环之职（记席⛔治；封版 --後 照拦）：\n' + '\n'.join(主环))
    return True


分栏之始 = 411                                   # ★N≤410 之 --前 之印一字不变
主环之闸 = ('囤灰闸', '跑账', '席令之禁')        # 越记席之职（409 回执 §十四·3 自注）；--後 之囤灰闸、全测·快照拦
_项式 = re.compile(r'^(    )?· ([^：]+)：[ \t]*(✓|⛔)')


def 前之项(印):
    """--前 之印 → {名: [栏, 态, 文]}：栏 席／主环；态 ✓／⛔／·（无态之印，文＝其块之全文，供较上回之变）。"""
    项, 块 = {}, None
    for l in 印.split('\n'):
        m = _项式.match(l)
        if m:
            项[m.group(2).strip()] = ['主环' if m.group(1) else '席', m.group(3), l.strip()]; 块 = None
        elif l.startswith('· '):
            块 = re.split('[：（]', l[2:], 1)[0].strip(); 项[块] = ['席', '·', l]
        elif l.startswith('⛔ '):
            项[l[:24]] = ['席', '⛔', l.strip()]; 块 = None
        elif 块 and l.startswith(' '):
            项[块][2] += '\n' + l
    return 项


def _锁之数(文):
    return dict(re.findall(r'(?m)^    ([^：\n]+)：(.*)$', 文))


def 红印(n, 今, 上, 时=''):
    """--前 --红 之印：席栏之 ⛔（新红／变）、较上回之变、上回红今已绿、主环之职之红；末行「✓ 余 N 项俱绿」。"""
    出, 绿 = ['════ 封版·前·红（第%d章；较上回 %s）════' % (n, 时 or '?')], 0
    for 名, (栏, 态, 文) in 今.items():
        旧 = 上.get(名)
        if 态 == '✓':
            绿 += 1
        elif 态 == '⛔' and 栏 == '席':
            出.append(文 + ('' if 旧 and 旧[1] == '⛔' and 旧[2] == 文 else '（变）' if 旧 and 旧[1] == '⛔' else '（新红）'))
        elif 态 == '·' and 旧 and 旧[2] != 文:
            if 名 == '锁定行之数':
                a, b = _锁之数(旧[2]), _锁之数(文)
                出.append('· 变·锁定行之数：' + '；'.join('%s %s→%s' % (k, a.get(k, '（无）'), b.get(k, '（无）')) for k in b if a.get(k) != b.get(k)))
            else:
                出.append('· 变·%s（其印已异於上回；全印：python3 工具/封版.py %d --前）' % (名, n))
    已 = [名 for 名, x in 上.items() if x[1] == '⛔' and (今.get(名) or [0, '✓'])[1] != '⛔']
    if 已:
        出.append('· 上回红今已绿：' + '、'.join(已))
    环 = [x[2] for x in 今.values() if x[0] == '主环' and x[1] == '⛔']
    if 环:
        出.append('· 主环之职（记席⛔治；封版 --後 照拦）：\n' + '\n'.join('    ' + x for x in 环))
    出.append('✓ 余 %d 项俱绿' % 绿)
    return '\n'.join(出)


def 上回之档(n, root=ROOT):
    return os.path.join(root, '.cache', '封版前', '第%d章.json' % n)     # ⛔存 版本/（免 --後 提交、惹囤灰闸、档肿哨）


class _分流:
    """印之二路：存其文、且（显）照印於终端——--前 跑约二分，⛔候毕方印。"""
    def __init__(self, 显, 原):
        self.显, self.原, self.文 = 显, 原, []

    def write(self, x):
        self.文.append(x)
        if self.显:
            self.原.write(x)
        return len(x)

    def flush(self):
        self.原.flush()


def 前印(n, 红=False, root=ROOT):
    """--前（与 --前 --红）之跑口：印之同时存其项於 .cache；红且有上回者只印 红印()，无上回者全印（首跑）。"""
    档 = 上回之档(n, root)
    try:
        上 = json.load(open(档, encoding='utf-8'))
    except Exception:
        上 = None
    原 = sys.stdout
    流 = _分流(not (红 and 上), 原)
    sys.stdout = 流
    try:
        ok = 前(n, root)
    finally:
        sys.stdout = 原
    今 = 前之项(''.join(流.文))
    if 红 and 上:
        print(红印(n, 今, 上.get('项', {}), 上.get('时', '')))
    try:
        os.makedirs(os.path.dirname(档), exist_ok=True)
        json.dump({'时': time.strftime('%m-%d %H:%M:%S'), '项': 今}, open(档, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    except Exception as e:
        print('· 上回之印存不得（%s）——下回 --红 照全印' % e)
    return ok


def 记之缺(n, root=ROOT):
    t = open(os.path.join(root, 施工表), encoding='utf-8').read()
    项 = [('回执', bool(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % n)))),
         ('锁定行', ('| %d | 锁定 |' % n) in t), ('悬账行', ('| %d | 悬账 |' % n) in t),
         ('创作记录', os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_创作记录.md'))),
         ('全书记忆·章详记', os.path.exists(os.path.join(root, '设定', '全书记忆', '第%d章.md' % n))),
         ('下一章开镜卡', os.path.exists(os.path.join(root, '版本', '第%d章' % (n + 1), '_开镜卡.md'))),
         ('席记', os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_席记.json')))]
    if n >= 分栏之始:          # ★1024 验席：记席留「‹器:键›」而未跑 记落.py 即交，器格成空壳入封——--後 拦之（N≤410 无此项）
        import 记落
        项 += [('占位未填·%s（跑 python3 工具/记落.py %d）' % (名, n), False) for 名, p in 记落.档们(n, root) + [('检察官', 记落.检察官)]
               if '‹器:' in (记落.读(p, root) or '')]
    return [k for k, ok in 项 if not ok]


def 可提交(n, 路们):
    """只收本章所及之处（⛔git add -A）：正文／本章与下一章之版本目录／设定／根之 .md 与 .html。"""
    # ★1013：记席按令改 工具/小说检察官.py 之 OPEN_BRIEF_CARD_SCHEMA[N+1]——旧只收 设定/ 等，此档永留未提交（381 实逮）
    #   ⛔1027：提示词系统之「--开拍 N+1」随十三轮之旧令汰（阶段之数⛔再改之），其档⛔收
    前缀 = ('正文/', '版本/第%d章/' % n, '版本/第%d章/' % (n + 1), '设定/', '工具/小说检察官.py',
          '阅读器/镇冢秘术_全本阅读器.html')        # ★1013：阅读器由本器同步，旧不收——381 实逮「不在本章所及之处」
    收 = [p for p in 路们 if p.startswith(前缀) or ('/' not in p and p.endswith(('.md', '.html')))]
    return 收, [p for p in 路们 if p not in 收]


def 末章之病(out):
    """检察官 --末章 之印 → 诸病（✗ 行之下诸条）；⛔「第十一轮未过」——其归 --後（399 --前 之假红）。"""
    L = out.split('\n')
    i = next((k for k, l in enumerate(L) if '✗' in l), None)
    if i is None:
        return ['（判不出：无 ✗ 行）']
    return [l.strip() for l in L[i + 1:] if l.strip() and not l.strip().startswith('第十一轮未过') and not l.strip().startswith('末章硬闸·')]


def 红行(out, 顶=15):
    """器之印中之红项（「✗」行、行首「⛔」而非 D6 之训者）——封版红时当面印，⛔只印末一行。"""
    出 = [l.strip() for l in out.split('\n') if l.strip() and ('✗' in l or l.strip().startswith('⛔')) and '永远的痛' not in l]
    return 出[:顶]


def 後之闸(n):
    """席记写毕之後、提交之前之序：→ [(名, 命令)]（红即停）。
    ★1020 X21：⛔於此跳心跳 N+1——N+1 无席而锁在（空锁：自走判候、席在跑吗放行、全测之留字降黄；W53 验席所逮）。
      封版之全测撞断流之治在接力：其静自交棒之刻（本表第十一轮所产之 `_十一轮.json`）起算。
    ★1027 法用之守（N≥411）：已取之法本章无证即红、⛔提交（其验之末行入席记「法用」，下一章以之为前章已验之凭）。"""
    if n >= 分栏之始:
        return [('囤灰闸', [器('囤灰闸.py')]), ('法用之守', [器('法用之守.py'), '--验', str(n)]),
                ('第十一轮', [器('小说检察官.py'), '--十一轮', str(n)]), ('全测·快', [器('全测.py'), '--快'])]
    return [('囤灰闸', [器('囤灰闸.py')]), ('第十一轮', [器('小说检察官.py'), '--十一轮', str(n)]), ('全测·快', [器('全测.py'), '--快'])]


def 後之存(n):
    """提交之後之序：→ [(名, 命令)]（红只报⚠）。末步撤锁（心跳.可收 守：心跳已属 N+1 者⛔清）。"""
    return [('存底 --存', [器('存底.py'), '--存', '第%d章封版' % n]), ('存底 --标', [器('存底.py'), '--标', str(n)]),
            ('存底 --演', [器('存底.py'), '--演', str(n)]), ('云端验', [器('云端验.py')]), ('跑账', [器('跑账.py')]),
            ('存底包', [器('存底包.py')]), ('撤锁', [器('心跳.py'), '--收', str(n)])]


def 封毕之语(n):
    """封毕之下一步（1027 坑51）：章-N 已触 GitHub autopush——主环只候（零 token），⛔直推主枝。"""
    return ('✓ 封版毕。下一步（主环）：python3 工具/接棒守.py --候主 %d（run_in_background；零 token——「章-%d」已触 GitHub autopush，'
            '推时即闸、绿即并入主枝；坏报即早返其红，逾限方 推.py --直）' % (n, n))


def 阶段之数(n, root=ROOT):
    """★X53·1021：README 阶段句随封版自改（零 token；旧由记席／主环手改，401 漏之即红於全测·快）。
    ⛔1027：提示词系统（十三轮之旧令，无一席读之）之「--开拍 N+1」⛔再改——其检（检察官医生之提示词系统一支）同日汰。"""
    改 = []
    for 档, 式, 新 in (('README.md', r'第 1—\d+ 章已经同步封版；第 \d+ 章开写前', '第 1—%d 章已经同步封版；第 %d 章开写前' % (n, n + 1)),):
        fp = os.path.join(root, 档)
        t = open(fp, encoding='utf-8').read()
        t2 = re.sub(式, 新, t, count=1)
        if t2 != t:
            open(fp, 'w', encoding='utf-8').write(t2); 改.append(档)
    return 改


def 後(n, 试=False, root=ROOT):
    print('════ 封版·後（第%d章）%s════' % (n, '·试（⛔写、⛔提交）' if 试 else ''))
    缺 = 记之缺(n, root)
    if 缺 and not 试:
        print('⛔ 记席之档未齐：%s——回记席补（⛔本器代写）' % '、'.join(缺)); return False
    步 = []
    if not 试:
        print('  ✓ 阶段之数    %s' % ('、'.join(阶段之数(n, root)) or '已是 %d／%d' % (n, n + 1)))
        步 += [('净重对表 --补', [器('净重对表.py'), '--补'], False), ('同步全本阅读器', [器('同步全本阅读器.py')], False),
              ('全书记忆随', [器('全书记忆.py'), '--随'], False),   # ★1024 实踩（410）：亮点添注而白文未动，详记之 sha 器随（零 token）
              ('剧情链', [器('剧情链.py')], False),          # ★1015 作者令：每章精读之详记串成从头到尾之链，封版即重生、随提交上 GitHub
              ('人物链', [器('人物链.py'), '--并记'], False),   # ★1015 作者议：每人从头到尾之链与每两人之关系——自记席之「在场之人」零 token 重并（虹吸）
              ('器之迹', [器('囤灰闸.py'), '--迹', str(n), '--写'], False)]   # ★1015 作者议：每章从头到尾用了哪些器、每器之表现（败、慢、重跑）——自 _器之迹.jsonl 零 token
    步 += [('回执对账', [器('回执对账.py')], True), ('开轮六检', [器('开轮六检.py'), str(n)], True),
          ('第零轮开镜庭', [器('第零轮开镜庭.py')], True), ('造式之实', [器('造式.py'), str(n)], True)]
    for 名, a, 必 in 步:
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        print('  %s %-10s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⛔', 名, rc, 秒, 末[0].strip()[:150]))
        if 必 and rc != 0:
            print('⛔ 停：%s 红——⛔提交；照其印治（记席之档或交总编辑）' % 名); return False
    if not 试:
        p = os.path.join(root, '版本', '第%d章' % n, '_席记.json')
        j = json.load(open(p, encoding='utf-8'))
        j.setdefault('段', {})['封版'] = '封版.py：净重对表补、阅读器同步、回执对账、开轮六检、开镜庭、造式之实、囤灰闸、第十一轮、全测俱过；提交、存底、撤锁（%s）' % time.strftime('%Y-%m-%d', time.gmtime())
        json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for 名, a in 後之闸(n):
        if 试 and 名 == '第十一轮' and os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_十一轮.json')):
            print('  · 第十一轮：试·已有凭据（⛔重写）——其 mtime 即接力之交棒之刻，试不新之：全测·快之接力若报断流，真跑重写凭据即新（演练与真跑唯此一异）'); continue
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        print('  %s %-10s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⛔', 名, rc, 秒, 末[0].strip()[:150]))
        if rc != 0:
            for l in 红行(out):      # ★1020 398 封版：全测·快红而只印末一行，须另跑十一分钟方知何项——红则当面印其诸红项
                print('      ' + l)
            print('⛔ 停：%s 红——⛔提交' % 名); return False
        if 名 == '法用之守' and not 试:      # ★1027：其验入席记（随本章之提交上云；下一章之法用之守以此为前章已验之凭）
            _p = os.path.join(root, '版本', '第%d章' % n, '_席记.json')
            _j = json.load(open(_p, encoding='utf-8'))
            _j['法用'] = 末[0].strip()[:200]
            json.dump(_j, open(_p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    if 试:
        print('✓ 试毕：诸闸俱过（⛔提交、⛔存底）'); return True
    st = subprocess.run(['git', '-c', 'core.quotepath=off', 'status', '--porcelain', '-uall'], cwd=root, capture_output=True, text=True).stdout
    路们 = [l[3:].strip().strip('"') for l in st.split('\n') if l.strip()]
    收, 弃 = 可提交(n, 路们)
    if 弃:
        print('  · 不在本章所及之处、⛔提交：%s' % '、'.join(弃))
    名 = re.sub(r'^.*?第.+?章_?', '', os.path.basename(正文档(n, root) or ''))[:-3]
    subprocess.run(['git', 'add', '--'] + 收, cwd=root, check=True)
    # ★1013：说明须标「封版#N」——改单闸认之为「新章封版之追记（係添不係改）」；缺之则推时改单红（381 实逮）
    msg = '第%d章《%s》封版（造式二代·封版#%d）：诸闸、第十一轮、全测俱过——记席之档（回执、锁定行、创作记录、全书记忆、状态册、open_brief、第%d章开镜卡）\n\n%s' % (n, 名, n, n + 1, 尾)
    r = subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=root, capture_output=True, text=True)
    print('  %s 提交 %s' % ('✓' if r.returncode == 0 else '⛔', subprocess.run(['git', 'log', '--oneline', '-1'], cwd=root, capture_output=True, text=True).stdout.strip()[:100]))
    if r.returncode != 0:
        print(r.stdout + r.stderr); return False
    for 名, a in 後之存(n):
        rc, out, 秒 = 跑(a, root)
        末 = [l for l in out.split('\n') if l.strip()][-1:] or ['']
        print('  %s %-8s rc=%d %5.0fs  %s' % ('✓' if rc == 0 else '⚠', 名, rc, 秒, 末[0].strip()[:150]))
    print(封毕之语(n))
    return True


def 自测():
    ok = 共 = 0
    d = 数(380)
    # 据 380 锁定行亲核之数（施工表 | 380 | 锁定 |）：白文 1 至 107 行、亮点 109、净重与六数（照锁定行现取）、末版、「＊」4 处（五拍）、与末版逐字同
    共 += 1; ok += (d.get('白文') == '1 至 107 行' and d.get('亮点行') == 109)
    # ★1020：净重与六数⛔钉快照（2572）——还账施改白文（380·v05，1020）後锁定行由 净重对表 --补 重量为 2,559，旧格遂红於快测；
    #   今照其注之本义「与其锁定行亲核之数逐个同」：取施工表 380 锁定行之六数比之（正文改而锁定行未补 → 仍红）
    _锁 = re.search(r'净重([\d,]+)｜段数\d+｜长段数\d+｜嗅\d+｜触\d+｜四字串三现\d+',
                   next((l for l in open(os.path.join(ROOT, 施工表), encoding='utf-8') if l.startswith('| 380 | 锁定 |')), ''))
    共 += 1; ok += (_锁 is not None and d.get('净重') == int(_锁.group(1).replace(',', '')) and re.fullmatch(r'v\d\d', d.get('末版') or '') is not None
                   and d.get('六数') == _锁.group(0).replace(',', ''))   # ★1015：末版⛔钉 v03（还账施改骨记即存新版——坑二十八之家）
    共 += 1; ok += (d.get('＊') == 4 and d.get('拍') == 5 and re.fullmatch(r'[0-9a-f]{12}', d.get('sha1', '')) is not None and d.get('与末版同') is True)   # ★sha1 ⛔钉快照：白文之数（行、净重、拍）不随骨记之改而变，sha1 随之变
    共 += 1; ok += (d.get('总纲') == '| 380 | 主·148 |')
    _证 = 机械之证(390)                       # ★1015 W33 之改：据 390 记席手查之果（回执 §六：骨记引句俱合、对白 8 行皆钱满 :15…:125）
    共 += 1; ok += (len(_证) == 6 and '不合 0' in _证[0] and _证[2].startswith('③对白之行 8：:15、:99'))
    # ★W60 X37：骨记之引逐条机核——造局於字串（⛔钉盘上会长之数）：全角冒号、区间（至／略号分段）、逾四十字之原句、
    #   本章（：行）、续引（、：行）、Ｄ6／总纲之号⛔认、跨章区间⛔认、不足四字不核、±1 之界、章不在、行逾白文、远引四字之共与印行
    _长 = '天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往秋收冬藏闰余成岁律吕调阳云腾致雨露结为霜金生丽水玉出昆冈'
    _错 = _长[:24] + '错字错字'                 # 句首二十四字俱对、其尾错
    _白们 = {12: ['子丑寅卯辰', '甲乙丙丁戊', '“一二三四五，”他说。', '己庚辛壬癸', '', _长],
            13: ['戌亥甲子乙丑丙寅', '问话，尾巴没有往上走。', '上头一张是复印的悬赏。'], 900: ['# 第九百章', '本章之一句话在此。']}
    _骨 = ('【本章亮点】\na（12：3「一二三四五，」）。b 12:1「己庚辛壬癸」。c 12：2至4「甲乙丙丁戊……己庚辛壬癸」。d 12:6「%s」。e 12:6「%s」。'
          'f 拍一（：2）「本章之一句话在此。」。g Ｄ6：2「本章之一句话在此」、总纲：2「本章之一句话在此」。h 13:1「子丑」。'
          'i （13：2 尾巴没有往上走之翻）。j 背冲街坐（13：3 悬赏在身）。k 12：2至13：3。l 12：1、：4「己庚辛壬癸」。'
          'm 14:1「此章不在其书」。n 12:99「甲乙丙丁戊」。') % (_长, _错)
    _核 = 骨引之核(_骨, 900, 白们=_白们)
    _印 = 骨引之印(_核)
    共 += 1; ok += ([(x['章'], x['起'], x['止'], 类, 合) for x, 类, 合, _, _ in _核] == [
        (12, 3, 3, '原句', True), (12, 1, 1, '原句', False), (12, 2, 4, '原句', True), (12, 6, 6, '原句', True), (12, 6, 6, '原句', False),
        (900, 2, 2, '原句', True), (13, 1, 1, '短', True), (13, 2, 2, '远引', True), (13, 3, 3, '远引', False), (12, 1, 1, '远引', False),
        (12, 4, 4, '原句', True), (14, 1, 1, '原句', False), (12, 99, 99, '原句', False)]
        and _印.startswith('①骨记引句（章:行「原句」·含区间、全角冒号、本章（：行））5/9 合｜不合 4：12:1「己庚辛壬癸」实在 :4；')
        and '12:6「天地玄黄宇宙洪荒日月盈昃辰宿列张寒来暑往」所引之章无此句' in _印 and '14:1「此章不在其书」所引之章不在' in _印
        and '12:99「甲乙丙丁戊」行逾其白文（6 行）' in _印 and '｜不足四字不核 1' in _印
        and '①之二·骨记远引（章:行 而无「原句」）3 处：骨记之文四字以上逐字在所引之行·±1 者 1/3（13:2「尾巴没有往上走」）；余 2 处' in _印
        and '\n        13:3「上头一张是复印的悬赏。」 ← 骨「j 背冲街坐‖ 悬赏在身」' in _印)
    # 回灌：旧式（一式之正则＋人物链.核句 只核句首 24 字）——认Ｄ6 为章、漏区间／逾四十字／本章／续引，且放过 e 之错尾
    import 人物链
    _旧 = [(a, b) for a, b, _ in re.findall(r'(\d{1,3})[:：](\d{1,4})(?:[—–-]\d+)?\s*「([^」]{4,40})」', _骨)]
    共 += 1; ok += (_旧 == [('12', '3'), ('12', '1'), ('12', '6'), ('6', '2'), ('14', '1'), ('12', '99')]
                   and 人物链.核句(12, _错, '6', 文='\n'.join(_白们[12])) == (True, 6))
    # 真局（瑕疵总账 X37 所举：398 记席亲 awk 之远引 272:509、388:49）——器今自核、自印其行
    _证398 = 机械之证(398)[0]
    共 += 1; ok += ('272:509「尾巴没有往上走」' in _证398 and re.search(r'\n        388:49「[^」]*悬赏[^」]*」 ← 骨「', _证398) is not None
                   and '不合 0' in _证398 and '不合 0' in 机械之证(400)[0])
    # ★1016 X06：⑥极短段之比——造局於字串（⛔钉盘上会长之数）：≤15 字为极短，「＊」与题行不算段、空白不算字
    _文 = '# 第九百章 某\n\n短。\n\n＊\n\n' + '长' * 16 + '\n\n' + '一二三四五六七 八九十一二三四五\n\n【本章亮点】\n短\n'
    _线 = lambda k: '主' if k % 2 == 0 else '暗'
    共 += 1; ok += (极短段(_文) == (2, 3) and 极短段('') == (0, 0)
                   and 同线前三(391, _线) == [385, 387, 389] and 同线前三(391, _线, lambda k: k != 387) == [383, 385, 389]
                   and 同线前三(391, lambda k: None) == [] and 同线前三(3, _线) == [1]
                   and _证[5].startswith('⑥极短段（≤15 字）之比｜同线(主)前三章与本章：') and _证[5].count('→') == 3
                   and re.search(r'→390 \d+／\d+＝\d+\.\d%｜连四章上行：[是否]$', _证[5]) is not None)
    收, 弃 = 可提交(381, ['正文/a.md', '版本/第381章/x', '版本/第382章/_开镜卡.md', '设定/y.json', 'README.md', '工具/z.py', '版本/第379章/v.md'])
    共 += 1; ok += (弃 == ['工具/z.py', '版本/第379章/v.md'] and len(收) == 5)
    共 += 1; ok += (记之缺(380) == [] and '下一章开镜卡' not in 记之缺(380))
    # ★1024 验席：N≥411 之占位未填 --後 拦（施工表留 ‹器:sha1›）；N≤410 照旧不认
    import tempfile as _tf0, shutil as _sh0
    _目0 = _tf0.mkdtemp(prefix='封版占_')
    try:
        os.makedirs(os.path.join(_目0, os.path.dirname(施工表)))
        open(os.path.join(_目0, 施工表), 'w', encoding='utf-8').write('| 410 | 锁定 | ‹器:sha1› |\n| 411 | 锁定 | ‹器:sha1› |\n')
        共 += 1; ok += (any(x.startswith('占位未填·施工表') for x in 记之缺(411, _目0)) and not any(x.startswith('占位未填') for x in 记之缺(410, _目0)))
    finally:
        _sh0.rmtree(_目0, ignore_errors=True)
    # ★1020 X21（W53 验席之治法 a）：①⛔跳 N+1（空锁）、撤锁为提交後之末步；後() 真走此两表（⛔内联另一份——验席之七）；
    #   ②封版之全测⛔撞断流：接力之静自交棒（_十一轮.json）起算；③撤 N 之锁⛔清 N+1 之心跳（取本地与远端之新者——验席之十）。
    #   回灌：旧表（心跳 N+1 於全测前、⛔撤锁）、後() 内联旧表、接力只看下一章之新动、可收不比新旧——各即红。
    #   （接力、心跳二器之自测不在全测，借此格入快测）
    _体 = open(__file__, encoding='utf-8').read().split('\ndef 後(')[1].split('\ndef ')[0]
    共 += 1; ok += ([x[0] for x in 後之闸(400)] == ['囤灰闸', '第十一轮', '全测·快']
                   and not any('心跳.py' in x for _, a in 後之闸(400) for x in a)
                   and 後之存(400)[-1] == ('撤锁', [器('心跳.py'), '--收', '400'])
                   and 'in 後之闸(n):' in _体 and 'in 後之存(n):' in _体)
    try:
        import 接力 as _接, 心跳 as _跳
        _t = 1e9
        _封 = dict(印=False, now=_t, 末=400, 回执=True, 动=_t - 68 * 60, 跳=(False, None, None), 停=(False, ''))
        共 += 1; ok += (_接.查(交=_t - 120, **_封)[0] == [] and _接.查(交=_t - 68 * 60, **_封)[0] != []
                       and _跳.可收(400, [{'章': 401, '时': 2}, {'章': None, '时': 1}])[0] is False
                       and _跳.可收(400, [{'章': 401, '时': 1}, {'章': None, '毕': 400, '时': 2}])[0] is True)
    except Exception:
        共 += 1
    # ★1027 坑51：封毕之下一步係 接棒守 --候主 N（後台·零 token），⛔推.py（沙盒直推抢先、GitHub 之推恒败）；後() 只经 封毕之语 印之
    _毕 = 封毕之语(411)
    共 += 1; ok += ('python3 工具/接棒守.py --候主 411' in _毕 and '推.py（' not in _毕 and 'print(封毕之语(n))' in _体
                   and 'python3 工具/推.py（後台）' not in open(__file__, encoding='utf-8').read().split('def 自测')[0])
    共 += 1; ok += 红行('x\n  ✗ 负测·甲  坏\n⛔⛔ 永远的痛·D6\n  ✓ 乙\n⛔ 停') == ['✗ 负测·甲  坏', '⛔ 停']   # ★1020：红则印诸红项、⛔D6 之训
    _印 = '  ✗第9章《甲》:\n      第十一轮未过:未见 x\n  末章硬闸·第9章：失败'
    共 += 1; ok += 末章之病(_印) == [] and 末章之病(_印.replace('      第十一轮', '      5+逗:甲\n      第十一轮')) == ['5+逗:甲']   # ★1020：--前 免第十一轮（其归 --後）、余病照报
    # ★W60 X39：--前 之二慢检并起——①二检之命令与旧一字不差（检察官 --末章 N 以 subprocess.run、开轮六检 N --静 以 跑）；
    #   ②并起：二检各耗 0.4 秒，候齐二果之时 < 相继之时（0.9 秒）；③前() 只经 慢检并起 起此二检（⛔另跑一回、⛔删一检）
    import subprocess as _sp
    _记 = []
    _原run, _原跑 = _sp.run, globals()['跑']

    def _假run(a, **k):
        _记.append(('run', a[1:], k.get('cwd'))); time.sleep(0.4); return _sp.CompletedProcess(a, 0, '', '')

    def _假跑(a, root=ROOT, 限=900):
        _记.append(('跑', a, root)); time.sleep(0.4); return 0, '', 0.4
    try:
        _sp.run = _假run; globals()['跑'] = _假跑
        _t = time.time(); _慢 = 慢检并起(400, ROOT, 隔=0.05)
        _r1, _r2 = _慢['检察官'].result(), _慢['开轮六检'].result(); _秒 = time.time() - _t
    finally:
        _sp.run = _原run; globals()['跑'] = _原跑
    _前体 = open(__file__, encoding='utf-8').read().split('\ndef 前(')[1].split('\ndef ')[0]
    共 += 1; ok += (sorted(_记) == sorted([('run', [器('小说检察官.py'), '--末章', '400'], ROOT), ('跑', [器('开轮六检.py'), '400', '--静'], ROOT)])
                   and _秒 < 0.75 and _r1.returncode == 0 and _r2[0] == 0
                   and "慢['开轮六检'].result()" in _前体 and "慢['检察官'].result()" in _前体 and _前体.count('慢检并起(') == 1
                   and '开轮六检.py' not in _前体 and '小说检察官.py' not in _前体)
    _前 = open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0]
    共 += 1; ok += ("('质量三闸', ['质量三闸.py'])" in _前)        # ★1022 坑㊹：--前 跑与推闸同一之质量三闸（一章一日等）
    共 += 1; ok += ("('席令之禁', ['席令之禁.py'])" in _前)        # ★1023 坑㉟复踩：--前 跑席令之禁（新席缺律⑮⑳）
    共 += 1; ok += ("('全书记忆随', [器('全书记忆.py'), '--随']" in _前 and _前.index('全书记忆随') < _前.index("('剧情链', [器('剧情链.py')]"))   # ★1024 坑㊾：--後 先随详记之 sha、後生剧情链
    # ★1024 省 token 之审 records 二：--前 --红 与「主环之职」之栏
    #   ①分栏只走 N≥411、只移三闸（质量三闸＝六问之所出，留记席栏）；N≤410 之印照旧（print(_行) 一路）；--後 之囤灰闸照拦
    共 += 1; ok += (分栏之始 == 411 and 主环之闸 == ('囤灰闸', '跑账', '席令之禁') and 'if n >= 分栏之始 and _名 in 主环之闸' in _前体
                   and "return [('囤灰闸', [器('囤灰闸.py')])" in _前)
    # ★1027 法用之守：--前 於 N≥411 带 --前 跑之、入主环之职栏；--後 之闸 N≥411 含之（红即停、⛔提交）而 N≤410 一字不变；其验之末行入席记「法用」
    共 += 1; ok += ([x[0] for x in 後之闸(411)] == ['囤灰闸', '法用之守', '第十一轮', '全测·快'] and 後之闸(411)[1][1][1:] == ['--验', '411']
                   and [x[0] for x in 後之闸(410)] == ['囤灰闸', '第十一轮', '全测·快']
                   and "if n >= 分栏之始:          # ★1027 法用之守" in _前体 and "'法用之守.py'), '--验', str(n), '--前']" in _前体
                   and "主环.append('    · 法用之守：" in _前体 and "_j['法用'] = 末[0]" in _体
                   and 前之项('· 主环之职（记席⛔治；封版 --後 照拦）：\n    · 法用之守：⛔ 甲——主环治\n')['法用之守'][:2] == ['主环', '⛔'])
    _上 = ('· 造式之实：✓ 二代\n· 锁定行之数（取此，⛔凭空写）：\n    净重：3004\n    sha1：aaaaaaaaaaaa\n'
          '· 坑账之机械之证（器先算·记席照此答、⛔再逐条 grep）：\n    ①甲\n· 开轮十六检：⛔ ⑮未答——记席须治\n'
          '· 回执闸：⛔ 回执缺键：到期账——记席照式补\n· 六问：✓ 已答\n· 器物册（器物点名 411）：✓ 拍号俱对\n'
          '· 主环之职（记席⛔治；封版 --後 照拦）：\n    · 囤灰闸：✓\n    · 跑账：⛔ 甲器从没跑过——主环治\n    · 席令之禁：✓\n')
    _今 = (_上.replace('⛔ ⑮未答——记席须治', '✓ 俱过').replace('回执缺键：到期账', '回执缺键：病历').replace('aaaaaaaaaaaa', 'bbbbbbbbbbbb')
           .replace('    ①甲\n', '    ①乙\n') + '· 末章硬闸（检察官）：⛔ 5+逗:甲——治後再跑 --前\n')
    _项上, _项今 = 前之项(_上), 前之项(_今)
    _印 = 红印(411, _项今, _项上, '10-24 00:00:00')
    _L = _印.split('\n')
    共 += 1; ok += (_项上['跑账'][:2] == ['主环', '⛔'] and _项上['开轮十六检'][:2] == ['席', '⛔'] and _项上['锁定行之数'][1] == '·'
                   and '· 回执闸：⛔ 回执缺键：病历——记席照式补（变）' in _L and '· 末章硬闸（检察官）：⛔ 5+逗:甲——治後再跑 --前（新红）' in _L
                   and '· 上回红今已绿：开轮十六检' in _L and '· 变·锁定行之数：sha1 aaaaaaaaaaaa→bbbbbbbbbbbb' in _L
                   and any(l.startswith('· 变·坑账之机械之证') for l in _L) and '    · 跑账：⛔ 甲器从没跑过——主环治' in _L
                   and _L[-1] == '✓ 余 6 项俱绿' and not any('造式之实' in l or '六问' in l or '器物册' in l for l in _L))
    # ②前印：上回之印存 .cache（⛔版本/）；首跑全印、其後 --红 只印红；同印再跑 → 只余末行与题
    import tempfile as _tf, io as _io
    _目 = _tf.mkdtemp(prefix='封版红_')
    _原前 = globals()['前']
    try:
        globals()['前'] = lambda n, root=ROOT: (print(_上, end=''), True)[1]
        _o1 = _io.StringIO(); _s.stdout, _原 = _o1, _s.stdout
        try:
            _r1 = 前印(411, True, _目); _r2 = 前印(411, True, _目)
        finally:
            _s.stdout = _原
        _存 = 上回之档(411, _目)
        共 += 1; ok += (_r1 and _r2 and _o1.getvalue().startswith(_上) and _o1.getvalue().count('════ 封版·前·红') == 1
                       and _o1.getvalue().rstrip().endswith('✓ 余 5 项俱绿') and os.path.exists(_存)
                       and '/.cache/封版前/' in _存.replace(os.sep, '/') and '版本' not in os.path.relpath(_存, _目))
    finally:
        globals()['前'] = _原前
        import shutil as _sh; _sh.rmtree(_目, ignore_errors=True)
    print('封版·自测 %d/%d%s' % (ok, 共, ' 全通' if ok == 共 else ' 未过'))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) >= 2 and a[0].isdigit() and a[1] in ('--前', '--後'):
        n = int(a[0])
        sys.exit(0 if (前印(n, '--红' in a) if a[1] == '--前' else 後(n, '--试' in a)) else 1)
    print(__doc__); sys.exit(2)
