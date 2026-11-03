# -*- coding: utf-8 -*-
"""自进化环 · 查 → 自修 → 验自修 → 修不了才报，报了就挂账（2026-09-24 立·作者令）

════════════════════════════════════════════════════════════════════
⛔**其所以立·0924 之实（作者当面三令）**：
  「**要有自我纠错与自我进化之机制**」｜「**东西一定要随时保存在 GitHub**」｜
  「**不能故步自封，一直按老的问题去执行**」。

★**本坐当日自认之病，是这一环要治的全部**：
  ①**只会报，不会修**：推闸红了六天，回执里逐章记过，**没有一道器去修它**；
  ②**报了而无人读**：「待验」写在注里，十几个回合没人回头；
  ③**哨自己也会量错**：本坐当日立的 `未上库哨` 只量主枝、看不见存底枝，
    **报了一个「198 笔没上库」的假警**——⛔**而云端存底枝一直都有全部 363 章**；
  ④**同一族病反复发**：当日「问得太宽」一日三回。

★★**故本环四层，每层皆作「查 → 自修 → 验自修 → 修不了才报 → 报了就挂账」**：
  **L0 保命**（云端有没有这本书）——**会自己存、自己打标、自己验**；
  **L1 发布**（主枝落後多少）——**会自己推；同一原因连两回不变即判「卡死」——换法自通（另一合规之路）、记由入裁档、办毕报所为**（1027 第一律·自决：⛔停工候作者）；
  **L2 自纠**（尺之校＋自省哨）——**把「该疑那把尺」「写了没人读」摆出来**；
  **L3 自进化**（病族账）——**一族病逮到第二回而无器管它，即红**；
    **每一个器立起来，都要登是为哪一族病立的**——⛔**不许只治这一回，要治这一族。**
★★★**并有一层管这一环自己**：**每跑一回落一行 `设定/自进化环.log`**；
  **逾两个钟头没跑过，即是这一环自己停了**——⛔**一个会停而没人知道的环，就是又一道祝福。**
  ★1027 A2：其日志入 .gitignore（旧随踪：自走每跑一行、树恒脏、自 10-13 起三十一提交），存底强塞之（存底.强塞之档）；
    挂账照随踪（跨坐之卡死之计係其职），而文同即⛔写（回至卡死之回即止、末见只记日）。
    L0 缺碑推封版#N 之提交（⛔HEAD）；L1「已有推在跑」取 推.py 之锁（推.在推·⛔pgrep）。
════════════════════════════════════════════════════════════════════

用法：
    python3 工具/自进化环.py            # 跑一整环（查＋自修＋验＋挂账），自走每回合头一件
    python3 工具/自进化环.py --只查      # 不自修，只报（给负测与人眼用）
    python3 工具/自进化环.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, glob, json, time, subprocess
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
日志 = os.path.join(ROOT, '设定', '自进化环.log')
病族账 = os.path.join(ROOT, '设定', '病族账.md')
挂账 = os.path.join(ROOT, '设定', '自进化环_挂账.json')
主枝 = 'claude/the-novel-review-4dtuit'
# ⛔诸限写死，⛔不随今日之数挪（今日之教：一个会随今日之数挪的限，等於没有限）
存底之限分 = 30        # 存底枝逾此分钟未更新 → 自修（存一回）
主枝之限笔 = 3         # 主枝落後逾此笔 → 自修（推一回）
卡死之回 = 2           # 同一原因连此回不变 → 判卡死：换法自通、记由入裁档、办毕报所为（⛔停工候作者）
陈之日 = 7             # ★1027 执行之审 #117：首见逾此日而只见一回（回=1）之挂 → 自销（其因一去不返，⛔永挂）
环停之限时 = 2         # 本环逾此钟头没跑过 → 本环自己停了
推之间隔分 = 50        # L1 两回发起推之最短间隔（⛔每回推跑一整套全测约二十分钟）


def _器(名):
    s = _u.spec_from_file_location(名, os.path.join(ROOT, '工具', 名 + '.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _跑(*a, timeout=120):
    try:
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        class R:
            returncode = 99
            stdout = ''
            stderr = str(e)
        return R()


def _本地章数():
    return len(glob.glob(os.path.join(ROOT, '正文', '*.md')))


# ═══════════ 挂账（修不了的，逐笔挂上，⛔不许再沉默）═══════════
def _读挂():
    try:
        return json.load(io.open(挂账, encoding='utf-8'))
    except Exception:
        return {}


def _写挂(d):
    """★1027 A2：文同即⛔写——挂账随踪（跨坐之卡死之计係其职，⛔入 .gitignore），旧每跑必写（回与末见之分秒），树恒脏、提交恒多。"""
    新 = json.dumps(d, ensure_ascii=False, indent=1)
    try:
        if io.open(挂账, encoding='utf-8').read() == 新:
            return
    except Exception:
        pass
    io.open(挂账, 'w', encoding='utf-8').write(新)


本回所报之层 = set()
本回所见 = set()   # ★0924：本回报过挂之层；其旧因本回未再见者即销（因之文一变，旧笔永挂不销——卡死 6 处五处是陈账）
                    # ★1027 A2：以本回所见之键判陈（⛔以末见之时比：末见今只记日）


def 挂(层, 因, 修得了):
    """★同一「层＋因」连着出现几回？——**连 `卡死之回` 回不变，即判卡死**。
    ★1027 A2：回至卡死之回即止（其後不增：卡死之判已成，再数只令挂账每跑一变）；末见只记日——同日同态之跑⛔改其档。"""
    d = _读挂()
    k = '%s｜%s' % (层, 因[:60])
    if 修得了:
        d.pop(k, None)
        _写挂(d)
        return 0
    本回所报之层.add(层)
    本回所见.add(k)
    x = dict(d.get(k) or {'首见': time.strftime('%Y-%m-%d %H:%M'), '回': 0})
    x['回'] = min(x['回'] + 1, 卡死之回)
    x['末见'] = time.strftime('%Y-%m-%d')
    d[k] = x
    _写挂(d)
    return x['回']


def _封之章(回执们, 已录):
    """回执之档 → 已封版之章号。★1015（391 封版逮）：回执由记席写於封版之前，碑由封版提交之後立——
    旧以「回执在」即算已封，则每章封版中之全测必红其自身「缺碑」（序之缺）；今以「回执已提交」为已封。"""
    封 = set()
    for f in 回执们:
        m = re.search(r'第(\d+)章', os.path.basename(f))
        if m and f in 已录:
            封.add(int(m.group(1)))
    return 封


def _缺碑():
    """→ [已封版（309 起）而云端无 `章-N` 碑之章]。⛔**309 係章标之制立起之章，其前不追。**"""
    r = _跑('git', 'ls-remote', '--heads', 'origin', timeout=60)
    有 = set(int(x) for x in re.findall(r'refs/heads/章-(\d+)', r.stdout or ''))
    回执们 = [os.path.relpath(f, ROOT) for f in (glob.glob(os.path.join(ROOT, '设定', '回执_*第*章封版席*.md'))
                                              + glob.glob(os.path.join(ROOT, '设定', '回执_*第*章作业单*.md')))]
    录 = _跑('git', '-c', 'core.quotepath=off', 'ls-files', '--', *回执们, timeout=60) if 回执们 else None
    已录 = set((录.stdout or '').split('\n')) if (录 and 录.returncode == 0) else set(回执们)   # ⛔git 失灵即照旧式全算（⛔静默放过）
    封 = _封之章(回执们, 已录)
    return sorted(n for n in 封 if n >= 309 and n not in 有)


# ═══════════ L0 保命：云端有没有这本书 ═══════════
def L0(自修=True):
    """→ (安否, 诸语)。★**先量存底枝（保命那一层），不是主枝**——
    ⛔**0924 本坐立的未上库哨只量主枝，报了一个假警；本层即治它。**"""
    语 = []
    底 = _器('存底')
    v = 底.验(印=False)
    本 = _本地章数()
    旧分 = None
    if v:
        r = _跑('git', 'log', '-1', '--format=%ct', 'origin/备份/存底')
        if r.stdout.strip().isdigit():
            旧分 = (time.time() - int(r.stdout.strip())) / 60.0
    缺 = (v is None) or (v['章'] < 本) or (旧分 is None) or (旧分 > 存底之限分)
    # ★★★★★2026-09-24 补·**缺碑之查与自补**（作者查问「是不是都保存了」之日逐块核出）：
    #   ⛔**七章封了版而没立碑**（324／325／330／348／350／351／361）——
    #     **书本身不缺（存底枝里全有），而「一章一块覆不掉的碑」这一层有洞**；
    #   ★**其族係「封版之序有一步没人管」**——故 L0 自己查、自己补，⛔不再靠有人想起来。
    缺碑 = _缺碑()
    if 缺碑 and 自修:
        # ★1027 A2：补碑推「封版#N」之提交（⛔HEAD——HEAD 或已远在其後：以任意之树触 autopush 而充 章-N）；寻不着即只报
        封 = _器('封版')
        补, 无封 = [], []
        for n in 缺碑:
            sha = 封.封之笔(n, ROOT)
            if not sha:
                无封.append(n)
                continue
            rc, msg = 底.标(n, sha)
            if rc == 0:
                补.append(n)
        语.append('  ★已自修：补碑 %d 块（%s）——各推其封版#N 之提交' % (len(补), '、'.join(str(x) for x in 补)))
        if 无封:
            语.append('  ⚠ 寻不着封版#N 之提交（%s）——⛔以 HEAD 充碑；查其封版之笔、人手 `python3 工具/存底.py --标 N`（HEAD 须即其封版之提交）'
                     % '、'.join(str(x) for x in 无封))
        缺碑 = [n for n in 缺碑 if n not in 补]
    if 缺碑:
        语.append('⚠L0 保命：已封版而无碑 %d 章：%s' % (len(缺碑), 缺碑[:10]))
    if not 缺 and not 缺碑:
        语.append('✓L0 保命：云端存底枝 %d 章（本地 %d）｜%.0f 分钟前存过｜章标 %d 个｜封版之章无一缺碑'
                 % (v['章'], 本, 旧分, v['标']))
        挂('L0', '存底', True)
        挂('L0', '缺碑', True)   # ★0924：碑补齐了而旧挂不销，卡死里挂了十回「缺碑」陈账
        return True, 语
    if not 缺:
        回 = 挂('L0', '缺碑', False)
        return False, 语
    因 = ('存底枝不在云端' if v is None else
          ('云端 %d 章 < 本地 %d 章' % (v['章'], 本) if v['章'] < 本 else
           '存底枝 %.0f 分钟未更新（限 %d）' % (旧分 or -1, 存底之限分)))
    语.append('⚠L0 保命：%s' % 因)
    if not 自修:
        return False, 语
    # ★自修：存一回
    # ⛔**续心跳=False**：L0 不是一个在跑的席，⛔不许替任何一把锁续命（0924·本环曾令 363 之死锁永活）
    rc, msg = 底.存('自进化环·L0 自修：%s' % 因, 续心跳=False)
    v2 = 底.验(印=False)
    好 = (rc == 0 and v2 is not None and v2['章'] >= 本)
    语.append(('  ★已自修：存底一回（%s）→ 云端今 %d 章' % (msg, v2['章'] if v2 else -1))
             if 好 else ('  ⛔自修不成：%s' % msg))
    回 = 挂('L0', 因, 好)
    if not 好 and 回 >= 卡死之回:
        语.append('  ⛔⛔**L0 卡死（连 %d 回）——**总编辑当场治（律⑳）**：书之云端存底连着存不上去，查其根、治之，⛔不许停下等作者**' % 回)
    return 好, 语


# ═══════════ L1 发布：主枝落後多少 ═══════════
def L1(自修=True):
    """→ (安否, 诸语)。⛔**主枝落後不是「丢了」，是「成果未发布」——二者不许混说**（0924 之教）。"""
    语 = []
    _跑('git', 'fetch', '-q', 'origin', 主枝, timeout=60)
    r = _跑('git', 'rev-list', '--count', 'origin/%s..HEAD' % 主枝)
    n = int(r.stdout.strip()) if r.stdout.strip().isdigit() else None
    if n is None:
        语.append('⛔L1 发布：数不出主枝落後几笔——⛔**读不着不是绿**')
        return False, 语
    if n < 主枝之限笔:
        语.append('✓L1 发布：主枝落後 %d 笔' % n)
        挂('L1', '主枝落後', True)
        return True, 语
    语.append('⚠L1 发布：主枝落後 %d 笔（⛔此係「成果未发布」，不是「丢了」——书在 L0 里）' % n)
    if not 自修:
        return False, 语
    # ★自修：推一回（⛔走闸，不绕；推闸之判即其判）——放在後台，免本环被卡二十分钟
    # ⛔★★★★★2026-09-24 补·**本层头一版每跑一回就发起一回推**（本坐当日逐层计时所逮）：
    #   **每回推跑一整套全测（约二十分钟）**，而 `自走` 每小时一回、手动又可随时跑——
    #   ⛔**几回全测叠在一起抢机器，并互相撞「负测留字」**（通例六九）。
    #   ★**故加二闸**：①**已有一回推在跑，不再起**；②**距上一回发起不足 `推之间隔分` 分钟，不再起**。
    记 = os.path.join(ROOT, '设定', '_自进化环_推.out')
    # ★1027 A2：「已有推在跑」取 推.py 自己之锁之态（推.在推）——旧以进程名猜（'git push -u origin'）认不着本层今所起之 推.py（交治枝）
    try:
        在跑 = _器('推').在推(ROOT)
    except Exception:
        在跑 = False
    try:
        上回分 = (time.time() - os.path.getmtime(记)) / 60.0
    except Exception:
        上回分 = 1e9
    if 在跑:
        语.append('  ★已有一回推在跑（⛔不再起第二回·免全测叠跑）')
    elif 上回分 < 推之间隔分:
        语.append('  ★上一回推发起於 %.0f 分钟前（限 %d）——⛔不再起' % (上回分, 推之间隔分))
    else:
        # ★1027 坑51：自修之推交 GitHub——`推.py` 默推「治-<sha>」，GitHub 分片而闸（坑54）、绿即并入主枝（果入 备份/报）；
        #   ⛔沙盒直推主枝（本地再跑十余分之全测，且与 autopush 抢主枝、令其 non-fast-forward 而败）。
        try:
            subprocess.Popen('"%s" "%s" > "%s" 2>&1' % (sys.executable, os.path.join(ROOT, '工具', '推.py'), 记),
                             cwd=ROOT, shell=True, start_new_session=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             stdin=subprocess.DEVNULL)
            语.append('  ★已自修：交 GitHub 一回（後台·推.py 默推治枝、GitHub 闸而并·其印落 设定/_自进化环_推.out）')
        except Exception as e:
            语.append('  ⛔发起推不成：%s' % e)
    # ★上一回推之果：若仍被拦，读出其「点名之红」作因
    因 = '主枝落後'
    try:
        上 = io.open(记, encoding='utf-8', errors='replace').read()
        m = re.search(r'推闸：([^\n]+)', 上)
        if m:
            因 = m.group(1).strip()[:60]
    except Exception:
        pass
    回 = 挂('L1', 因, False)
    if 回 >= 卡死之回:
        语.append('  ⛔⛔**L1 卡死（同一因连 %d 回：%s）——**总编辑当场治其根（律⑳）**；治不动者写明卡在哪一条、落裁，**书照写（令：书往前走，账在後头跟）**，⛔不许停下等作者**'
                 % (回, 因))
    return False, 语


# ═══════════ L2 自纠：尺之校＋自省哨 ═══════════
def L2():
    语, 好 = [], True
    for 名 in ('尺之校', '自省哨'):
        try:
            m = _器(名)
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ok = m.报()
            if ok:
                语.append('✓L2 %s：过' % 名)
            else:
                好 = False
                坏 = [l.strip() for l in buf.getvalue().split('\n') if '⛔' in l][:2]
                语.append('⛔L2 %s：%s' % (名, '｜'.join(坏)[:140]))
            挂('L2', 名, ok)
        except Exception as e:
            好 = False
            语.append('⛔L2 %s 跑不起来：%s' % (名, e))
    return 好, 语


# ═══════════ L3 自进化：病族账 ═══════════
def 读病族():
    """→ [{名, 例, 器}]。⛔其式：`| 族名 | 例数 | 器 |`（器写「无」者即无器管它）。"""
    if not os.path.exists(病族账):
        return []
    # ⛔★★★★★2026-09-24 治·**本函头一版看不见四族**（本坐添了两族而 L3 仍印「12 族」，当场逮出）：
    #   **旧正则要求族名之後紧跟「|」**——⛔**凡族名後带括注者**（「**拿快照当判**（写死今日之数……）」）**一概读不出**；
    #   ★**其漏者四族，而其中一族正是「读者之判没走到落笔之前」**——**L3 自己犯了病族账第六族「判过了而器看不见」**。
    #   ★**故改：族名取第一栏里第一对 `**…**` 之内，其後之括注一概不管；例数取第二栏；器取第三栏。**
    out = []
    for l in io.open(病族账, encoding='utf-8'):
        栏 = [x.strip() for x in l.strip().strip('|').split('|')]
        if len(栏) < 3 or not 栏[1].isdigit():
            continue
        m = re.search(r'\*\*([^*]+)\*\*', 栏[0])
        名 = (m.group(1) if m else 栏[0]).strip()
        if 名 in ('族', '族名'):
            continue
        out.append({'名': 名, '例': int(栏[1]), '器': 栏[2]})
    return out


def L3():
    语 = []
    族 = 读病族()
    if not 族:
        return False, ['⛔L3 自进化：病族账读不出——⛔**读不着不是绿**']
    # ⛔「书之族」之限是 3 不是 2（第三回方判它是病还是这个人的样子·病族账§三）
    def _无器(x):
        # ⛔「⛔**无器守它**」之式亦是无器（旧式只认以「无」开头者，漏之）
        k = re.sub(r'[⛔*\s]', '', x['器'])
        return k.startswith('无') or k in ('', '—', '-')
    def _限(x):
        return 3 if '书之族' in x['器'] else 2
    无器 = [x for x in 族 if _无器(x) and x['例'] >= _限(x)]
    器不在 = []
    # ★1027：随汰之族（「〔随汰·…`工具/<器>` 已彻删〕」而其器真不在）退役——⛔作「器不在」；判借 进化链.随汰（一处判，⛔两份码；器仍在即⛔认）
    _汰 = _器('进化链').随汰
    for x in 族:
        if _汰(x['器'], ROOT):
            continue
        for f in re.findall(r'`([^`]+\.py)`', x['器']):
            if not os.path.exists(os.path.join(ROOT, '工具', os.path.basename(f))):
                器不在.append('%s→%s' % (x['名'], f))
    if 无器 or 器不在:
        if 无器:
            语.append('⛔L3 自进化：%d 族病已逮到第二回而无器管它：%s'
                     % (len(无器), '、'.join(x['名'] for x in 无器)))
        if 器不在:
            语.append('⛔L3 自进化：%d 族所登之器盘上不在：%s' % (len(器不在), '、'.join(器不在)))
        return False, 语
    语.append('✓L3 自进化：病族 %d 族，逮到二回以上者皆有器管它' % len(族))
    # ★★★★★2026-09-24 补·**进化链之棘轮**（作者令「要一个完整的进化链，犯过的错不能再犯」）：
    #   **犯过的每一个错，今天有没有一道器在守着；「无守」之数只许往下走。**
    try:
        import contextlib
        链 = _器('进化链')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ok = 链.跑()
        行 = [l.strip() for l in buf.getvalue().split('\n') if '共 ' in l or '棘轮' in l]
        语.append(('✓' if ok else '⛔') + 'L3 进化链：' + '｜'.join(行)[:150])
        if not ok:
            return False, 语
    except Exception as e:
        语.append('⛔L3 进化链跑不起来：%s' % e)
        return False, 语
    return True, 语


# ═══════════ L4 书之进化：读者之判有没有流进落笔之前 ═══════════
书之账 = os.path.join(ROOT, '设定', '书之进化账.md')
书棘轮 = os.path.join(ROOT, '设定', '书之进化_棘轮.json')


def L4():
    """⭐**最高优先之层**（作者令「小说之质是最高优先，⛔不能有任何妥协」）。
    ★**读者席（大审）判出的每一处「让人放下书」，须流进落笔之前的开镜卡**；
    ⛔**所登之问须在开镜卡模子里逐字在**（登了而模子里没有，等於没落）；
    ★**「未落卡」之数只许往下走（棘轮）。**"""
    语 = []
    if not os.path.exists(书之账):
        return False, ['⛔L4 书之进化：书之进化账不在——⛔**读不着不是绿**']
    模 = io.open(os.path.join(ROOT, '工具', '第零轮开镜庭.py'), encoding='utf-8').read()
    模 = 模.split('def make_card')[1].split('def check0')[0]
    行们 = []
    for l in io.open(书之账, encoding='utf-8'):
        m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$', l)
        if m and m.group(1) not in ('读者席',) and not m.group(1).startswith('---'):
            行们.append((m.group(1), m.group(2), m.group(3)))
    未落 = [x for x in 行们 if '未落卡' in x[2]]
    假落 = []
    for 席, 判, 问 in 行们:
        for q in re.findall(r'`([^`]+)`', 问):
            if q not in 模:
                假落.append('%s→%s' % (席, q))
    if 假落:
        语.append('⛔L4 书之进化：%d 席所登之问，开镜卡模子里并没有：%s——**登了而模子里没有，等於没落**'
                 % (len(假落), '、'.join(假落[:4])))
        return False, 语
    try:
        底 = json.load(io.open(书棘轮, encoding='utf-8'))['未落卡之底']
    except Exception:
        底 = len(未落)
        io.open(书棘轮, 'w', encoding='utf-8').write(
            json.dumps({'未落卡之底': 底, '立於': '2026-09-24'}, ensure_ascii=False))
    if len(未落) > 底:
        语.append('⛔L4 书之进化：读者之判未落卡 %d ＞ 底 %d——**新的读者之判没流进落笔之前**'
                 % (len(未落), 底))
        return False, 语
    if len(未落) < 底:
        io.open(书棘轮, 'w', encoding='utf-8').write(
            json.dumps({'未落卡之底': len(未落), '下移': '%d→%d' % (底, len(未落))}, ensure_ascii=False))
        语.append('★L4 书之进化：棘轮下移 %d → %d（又有读者之判流进了落笔之前——**这就是书在进化**）'
                 % (底, len(未落)))
    语.append('✓L4 书之进化：读者之判 %d 席｜已落卡 %d｜未落卡 %d（底 %d）'
             % (len(行们), sum(1 for x in 行们 if '`' in x[2]), len(未落), min(底, len(未落))))
    return True, 语


# ═══════════ 本环自己：它停没停 ═══════════
def 环之脉():
    try:
        末 = io.open(日志, encoding='utf-8').read().strip().split('\n')[-1]
        t = time.mktime(time.strptime(末[:16], '%Y-%m-%d %H:%M'))
        return (time.time() - t) / 3600.0
    except Exception:
        return None


def 记脉(标):
    """本环之日志只由本环写（0927：自走.py 自诩不动盘，其头之一行脉改由此落）。"""
    try:
        with io.open(日志, 'a', encoding='utf-8') as fh:
            fh.write('%s｜%s\n' % (time.strftime('%Y-%m-%d %H:%M'), 标))
    except Exception:
        pass


def 陈账(d, 跑过, 所见, 今=None):
    """→ (陈, 旧)：陈＝其层本回跑过而其因本回未见；旧＝首见逾 陈之日 而回=1（只见一回）、本回未见者（#117）。"""
    import datetime as _dt
    今 = 今 or _dt.datetime.now()
    陈 = [k for k in d if k.split('｜')[0] in 跑过 and k not in 所见]
    旧 = []
    for k, v in d.items():
        if k in 陈 or k in 所见 or v.get('回', 0) != 1:
            continue
        try:
            首 = _dt.datetime.strptime(str(v.get('首见', ''))[:16], '%Y-%m-%d %H:%M')
        except ValueError:
            continue
        if (今 - 首).days >= 陈之日:
            旧.append(k)
    return 陈, 旧


def 跑(自修=True):
    print('════ 自进化环 · 查 → 自修 → 验自修 → 修不了才报，报了就挂账 ════')
    本回所见.clear()
    本回所报之层.clear()
    时 = 环之脉()
    if 时 is not None and 时 > 环停之限时:
        print('  ⛔**本环上一回跑在 %.1f 钟头前（限 %d）——这一环自己停过**；'
              '⛔**一个会停而没人知道的环，就是又一道祝福**' % (时, 环停之限时))
    诸 = []
    # ⭐L4 列在最前——**它是最高优先**（作者令）；L0 保命係其前提，其次
    for 名, f in (('L4', L4), ('L0', lambda: L0(自修)), ('L1', lambda: L1(自修)),
                  ('L2', L2), ('L3', L3)):
        try:
            ok, 语 = f()
        except Exception as e:
            ok, 语 = False, ['⛔%s 跑不起来：%s' % (名, e)]
        诸.append((名, ok))
        for l in 语:
            print('  ' + l)
    # ★0924·销陈账：本回报过之层，其挂账里本回未再见之因即销（⛔只销报过之层，免一层跳过而误清）
    # ★1027 执行之审 #98：旧只销「本回报过之层」——一层全好、本回不报，其陈账永不销（L0、L1 四笔陈账挂至 1027）；
    #   今以「本回跑过之层」判：报过之层，或跑毕而全好（ok）之层；跑不起来（崩）之层⛔销（免一层跳过而误清）
    _跑过 = 本回所报之层 | {名 for 名, ok in 诸 if ok}
    _d = _读挂()
    _陈, _旧 = 陈账(_d, _跑过, 本回所见)
    for k in _陈 + _旧:
        _d.pop(k, None)
    if _陈 or _旧:
        _写挂(_d)
    if _陈:
        print('  ✓销陈账 %d 笔（其层本回跑过而其因已不见）：%s' % (len(_陈), '；'.join(x[:40] for x in _陈)))
    if _旧:
        print('  ✓自销旧挂 %d 笔（首见逾 %d 日而只见一回）：%s' % (len(_旧), 陈之日, '；'.join(x[:40] for x in _旧)))
    卡 = [(k, v) for k, v in _读挂().items() if v.get('回', 0) >= 卡死之回]
    if 卡:
        print('  ' + '═' * 60)
        print('  ⛔⛔⛔ **卡死 %d 处——总编辑当场逐条治其根（律⑳·⛔不许停下等作者；⛔亦不许默默不治）** ⛔⛔⛔' % len(卡))
        for k, v in 卡:
            print('     · %s（首见 %s·连 %d 回）' % (k, v.get('首见'), v['回']))
    行 = '%s｜%s｜卡死%d' % (time.strftime('%Y-%m-%d %H:%M'),
                            ' '.join('%s%s' % (n, '✓' if o else '⛔') for n, o in 诸), len(卡))
    try:
        with io.open(日志, 'a', encoding='utf-8') as fh:
            fh.write(行 + '\n')
    except Exception:
        pass
    print('  ── 本环落一行 设定/自进化环.log：%s' % 行)
    return all(o for _, o in 诸) and not 卡


def 自测():
    R = []
    R.append(('①诸限写死（30分／3笔／2回／2时／推间50分）',
              (存底之限分, 主枝之限笔, 卡死之回, 环停之限时, 推之间隔分) == (30, 3, 2, 2, 50)))
    _L1码 = io.open(__file__, encoding='utf-8').read().split('def L1')[1].split('def L2')[0]
    R.append(('①之二·⛔L1 已有推在跑即不再起（免全测叠跑·0924 逐层计时所逮）——其判取 推.py 之锁之态（1027 A2：⛔pgrep 猜进程名）',
              "_器('推').在推(ROOT)" in _L1码 and "'pgrep'" not in _L1码 and hasattr(_器('推'), '在推')))
    # ②⛔挂账：同一因连两回即卡死，修好即销（★1027 A2：於临时之档验——⛔动盘上之挂账）
    global 挂账
    import tempfile as _tf
    _真挂 = 挂账
    _目 = _tf.mkdtemp(prefix='自进化环挂_')
    try:
        挂账 = os.path.join(_目, '挂.json')
        _写挂({})
        a = 挂('测', '造局之因', False)
        b = 挂('测', '造局之因', False)
        R.append(('②⛔同一因连两回即计 2（≥卡死之回）', (a, b) == (1, 2)))
        _文 = io.open(挂账, encoding='utf-8').read()
        os.utime(挂账, (1, 1))
        c = 挂('测', '造局之因', False)
        R.append(('②之三·回至卡死之回即止、末见只记日——同日同态再跑⛔改其档（1027 A2：旧每跑必写、树恒脏）',
                  c == 2 and io.open(挂账, encoding='utf-8').read() == _文 and os.path.getmtime(挂账) == 1
                  and re.fullmatch(r'\d{4}-\d\d-\d\d', _读挂()['测｜造局之因']['末见']) is not None))
        挂('测', '造局之因', True)
        R.append(('②之二·修好即销（⛔不许留一笔已好了的卡死）', '测｜造局之因' not in _读挂()))
    finally:
        挂账 = _真挂
        import shutil as _sh
        _sh.rmtree(_目, ignore_errors=True)
    _L0码 = io.open(__file__, encoding='utf-8').read().split('def L0')[1].split('def L1')[0]
    R.append(('⑨L0 缺碑之补推封版#N 之提交（封版.封之笔·同一把尺），⛔HEAD；寻不着即只报（1027 A2）',
              "封.封之笔(n, ROOT)" in _L0码 and '底.标(n, sha)' in _L0码 and '底2.标(n)' not in _L0码 and '底.标(n)' not in _L0码))
    R.append(('⑩销陈账以本回所见之键（⛔以末见之时比：末见今只记日）', 'k not in 所见' in io.open(__file__, encoding='utf-8').read()))
    # ⑪⑫1027 执行之审 #98 #117：层全好（本回跑过而未报）时旧挂即销；跑不起来之层⛔销；首见逾七日而回=1 自销、回=2（卡死）⛔自销
    import datetime as _dt
    _今 = _dt.datetime(2026, 10, 27, 12, 0)
    _d = {'L0｜存底枝 85 分钟未更新（限 30）': {'首见': '2026-10-26 15:45', '回': 1},
          'L1｜某因': {'首见': '2026-10-27 08:00', '回': 1},
          'L2｜本回又见': {'首见': '2026-09-01 08:00', '回': 1},
          'L3｜崩层之挂': {'首见': '2026-10-27 08:00', '回': 2},
          'L3｜卡死久矣': {'首见': '2026-09-01 08:00', '回': 2},
          'L2｜旧而只一回': {'首见': '2026-10-10 08:00', '回': 1}}
    _陈, _旧 = 陈账(_d, {'L0', 'L1', 'L2'}, {'L2｜本回又见'}, _今)
    R.append(('⑪层全好（L0、L1 本回跑过而未报）→ 其旧挂即销；本回又见者、崩层（L3）之挂⛔销（#98）',
              sorted(_陈) == ['L0｜存底枝 85 分钟未更新（限 30）', 'L1｜某因', 'L2｜旧而只一回'] and 'L3｜崩层之挂' not in _陈))
    _陈2, _旧2 = 陈账(_d, set(), {'L2｜本回又见'}, _今)
    R.append(('⑫首见逾七日而回=1、本回未见 → 自销；回=2（卡死）、本回又见、未逾七日者⛔自销（#117）',
              sorted(_旧2) == ['L2｜旧而只一回'] and _陈2 == []))
    R.append(('⑬卡死之印⛔含「报作者」（1027 第一律·自决：换法自通、办毕报所为）', '报作者' not in io.open(__file__, encoding='utf-8').read().split('def 自测')[0]))
    # ③病族账读得出，且其式认「无」为无器
    族 = 读病族()
    R.append(('③病族账读得出（今 %d 族）' % len(族), len(族) >= 5))
    R.append(('④⛔L1 之语明写「成果未发布，不是丢了」（⛔0924 本坐混说二者，致作者惊慌）',
              '不是「丢了」' in io.open(__file__, encoding='utf-8').read()))
    R.append(('⑤⛔L0 先量存底枝，⛔不量主枝（0924 未上库哨之假警即由此来）',
              "'origin/备份/存底'" in io.open(__file__, encoding='utf-8').read()))
    R.append(('⑥⛔L1 之推走闸不绕（码里无 --no-verify／ZM_SKIP_HOOK）',
              all(w not in io.open(__file__, encoding='utf-8').read().split('def L1')[1]
                  .split('def L2')[0] for w in ('--no-verify', 'ZM_SKIP_HOOK'))))
    _L1 = io.open(__file__, encoding='utf-8').read().split('def L1')[1].split('def L2')[0]
    R.append(('⑥之二·L1 之自修交 GitHub（推.py 默推治枝），⛔沙盒直推主枝（坑51）',
              "'工具', '推.py'" in _L1 and 'git push -u origin %s' not in _L1))
    R.append(('⑦本环每跑一回落一行日志（本环之脉）', '日志' in io.open(__file__, encoding='utf-8').read()))
    R.append(('⑧封版中之章（回执在而未提交）⛔算已封——⛔自红其缺碑；已提交者照算',
              _封之章(['设定/回执_1_第390章封版席.md', '设定/回执_1_第391章封版席.md'], {'设定/回执_1_第390章封版席.md'}) == {390}))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 自进化环·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 跑(自修='--只查' not in sys.argv) else 1)
