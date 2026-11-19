#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""法用之守（1027 立·作者令「要有一个专门的机制，确保我们制定的这些最好的策略、已经进化的这些方法跑起来、被用上，而不是闲置和囤灰」）。

为何立：囤灰闸问「器接没接上跑口」、跑账问「器跑没跑过」、裁之生效问「裁有没有器守」——⛔一器问「总章已取之法，这一章真用上了没有」。
  其实（1027 查）：§二.7 许「其果由 Action 提交到 备份/报 枝」而云端无此枝；§八.2 推闸交 GitHub，章-406 至 章-410 五回 autopush
  俱败（gh run list），⛔一器报，封版犹令沙盒自推；§八.15 之「未行：缓存分档待解停之首坐探」「待 411 以 费审 核」无限、无人催。
  法立而无证，即囤灰——与器之囤灰同病，只是更难看见。
其法（零 token）：`设定/法用册.json` 一法一条——据（何处所立）、起（自第几章索证）、立（何章起行·回放用）、时（开｜封前｜封後｜段｜十）、
  证（俱须过）。证之式：档（glob＋含／无）、跑（_跑账 与 _器之迹：末跑 ≥ 本章之开＝前章封版之提交）、git（含／改／枝）、
  报（origin/备份/报 之 报/<路>.json 之「果」）、钩（.claude/settings.json）、量（章之数对阈）、限；并 或、若。
  待（缓办之件）带限：N ≥ 限 而无证即红。缓（暂免）至多三章、须写由。
  ★完备之律（立法须同日立证）：总章第八节每一条、方法账 1027 起每一行，须有一条之据点着它——否则「法立无证」红；
    机证不能（纯理）须写由、⛔逾四之一。自此⛔取一法而无用证。
  ★完备之律·扩（1027 执行之核·作者令「已定之决、立之法、作者之令、要避之坑须全部执行起来……一定要核查」）：
    ①作者常令 1021 起每条「- MMDD …令」：行内「法用#<id>」（id 在册），或其「落」所点之器／档在盘且为册（据、证）所引——否则「令立无证」红；
      落所点之档不在盘亦红（令落之档不在）；
    ②总章之五大主义、心诀（「见五大主义」之指⛔计）、§二—§六 每条编号之规（§四 作一条）、§五 每「｜」之守：须为册之法／待／废之
      「据」所点（写作 五大主义·执行、心诀七、§二.3、§五「管档」），或入册「机证不能」（据、由）——⛔逾四之一；
    ③时∈开／封前／封後 之法：至少一条行为之证（跑／git／报／量，或章之迹：档之路带 {N}／{N-1}／{段} 之类），或书「钩自跑」带钩之证；
    ④方法账 1027 起之行、总章§八 ≥23 之条：须书「所废」与「较旧：效…；费…」（真无旧可比写「较旧：无」）——心诀·虫洞。
  ★未行之数（同功两处即废劣者：五本执行之账合印一数）：进化链无守＋裁未生效＋坑已治未守＋令无证＋待逾限＋废而未除＋复核未行——
    --报 印之、只许降（棘轮唯一处：册之「未行」「底」；--未行 --降 降之）；--报 --首 印一行之要（会话开头之钩印之）。
★执行之守·丝滑之守（1027 作者令「执行主义」「丝滑主义」·坑53：沙盒推与 GitHub 推同推主枝、新法立而旧路未除）：
  ①所废除尽：册之「废」一废一条——据、废于、在（废前之笔）、去证（无档｜无文｜无格｜推报验｜无踪｜无渲）；去证有一尚在即「废而未除」红
    （待合＝并行之轨合流方除：限前只报⚠）；每条去证於其「在」之树须红（--自测 验之：式写错即永绿）。
  ②写者唯一：`设定/写者册.json` 一族之枝一写者（推.py --直 係唯一之审计之例外）；静析 工具/*.py、githooks、workflows、席之 js 之
    git push（随简变量、函之返、他模之常量、列之串接、git 之包〔以其体识〕解其靶；push 须係 git 之令；yml 自析、⛔依推报之私函），
    册外之写者即「二写者」红；例外只许於其旗之正支（else、否之判⛔算）。回灌：540c1c91（推.py 默直推主枝、自进化环裸推）须红。
  ③同功之检：每法书 功、处（沙盒｜GitHub）；二活法同功异处即红——除非其一入废、或书互补带由。
  ④演练之证：流程之法（流程:true）须有真料之演（设定/演练账.json｜备份/报 之 报/演/*.json，果 同／过——演练账之「唯後治之异」而诸闸之判过即同，
    早於其起章之封）；
    演练之律前已行者（立 ≤ 412）方许演免。
  ⑤报之读：自走之首一取 备份/报，报/推、报/演 之 红／拒／败 未为後之成所消者印 ⛔（≤三行）。
用法：
  python3 工具/法用之守.py --验 N [--前]     # 封版之验（封版 --前 带 --前：记席之前·阶後之证免）；并验执行之守·丝滑之守；红 rc=1
  python3 工具/法用之守.py --开 N            # 开章：本章须用之法 → 其证（≤10 行；自走於【判】起印之）
  python3 工具/法用之守.py --册              # 印册、量之势、待、废
  python3 工具/法用之守.py --报              # 全测之格（只报）：完备、册之形、逾限之待、废、写者、同功、演之数、未行之数（只许降）
  python3 工具/法用之守.py --报 --首        # 一行之要（会话开头之钩印之·⛔析写者：约一秒）
  python3 工具/法用之守.py --未行 [--降]     # 未行之数之分（--降：今 < 底 即降其底·棘轮唯一处）
  python3 工具/法用之守.py --废              # 每废：今尽否、其「在」之树去证真红否（合流之段校去证用之）
  python3 工具/法用之守.py --写者 [版]       # 诸推之处与其族（带版即以今之写者册回放史之树）
  python3 工具/法用之守.py --报读            # 备份/报 之未消坏报（全；自走之首只印三行）
  python3 工具/法用之守.py --回放 406 410    # 以史回放（立 ≤ N；盘取其章封版之提交、跑取 版本/第N章/_器之迹.md）
  python3 工具/法用之守.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, glob, time, subprocess, calendar, ast, shlex, fnmatch, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
册名 = os.path.join('设定', '法用册.json')
总章名 = '00_总章.md'
法账名 = os.path.join('设定', '方法账.md')
起章 = 411                                   # ★N≤410 ⛔验（法用之守 1027 立，411 起索证）
立日 = '1027'                                # 方法账自此日起之行须有册之据
立时 = 1793059200                           # 2026-10-27 00:00 UTC：回放之时界⛔逾此（其後所补之报⛔改史之判）
时们 = ('开', '封前', '封後', '段', '十')
果默 = ('成', '已在')
机证之顶 = 0.25
常令名 = os.path.join('设定', '00_作者常令_不停之律.md')
令起日 = '1021'                              # 作者常令自此日起之令须有证（1027 执行之核）
行为之键 = ('跑', 'git', '报', '量')
章迹之占 = ('{N}', '{N-1}', '{N+1}', '{N-2}', '{段}', '{段末}', '{段-1}', '{前段}', '{前段末}', '{前段-1}')
try:
    import 存底 as _存底
    主枝 = _存底.主枝                        # ⛔另起尺
except Exception:
    主枝 = 'claude/the-novel-review-4dtuit'
证之键 = ('档', '跑', 'git', '报', '钩', '量', '限', '或', '若')


# ───────── 小件 ─────────
def 段起(n):
    return 381 + (n - 381) // 10 * 10 if n >= 381 else (n - 1) // 10 * 10 + 1


def 填(s, n):
    if not isinstance(s, str):
        return s
    b = 段起(n)
    for k, v in (('{N-1}', n - 1), ('{N-2}', n - 2), ('{N+1}', n + 1), ('{段末}', b + 9), ('{段-1}', b - 1), ('{前段末}', b - 1), ('{前段-1}', b - 11), ('{前段}', b - 10),
                 ('{段}', b), ('{N}', n), ('{主枝}', 主枝)):
        s = s.replace(k, str(v))
    return s


def _git(root, *a, 限=60):
    try:
        r = subprocess.run(['git', '-c', 'core.quotepath=off'] + list(a), cwd=root, capture_output=True, text=True, timeout=限)
        return r.returncode, r.stdout
    except Exception as e:
        return 99, str(e)


def 封时(n, root, 至='HEAD'):
    """第 n 章封版之提交之时（epoch；取其末一回）；无即 None。"""
    rc, o = _git(root, 'log', '-1', '--format=%ct', '-F', '--grep=（造式二代·封版#%d）' % n, 至)
    return int(o.strip()) if rc == 0 and o.strip().isdigit() else None


def 封提交(n, root, 至='HEAD'):
    rc, o = _git(root, 'log', '-1', '--format=%H', '-F', '--grep=（造式二代·封版#%d）' % n, 至)
    return o.strip() if rc == 0 and o.strip() else None


def _iso(t):
    return time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(t))


def 提交之坐(root, 版):
    """提交之说明之「Claude-Session: …session_<号>」（或「坐：<号>」）→ 号（去 session_ 之前缀）；无即 None。"""
    if not 版:
        return None
    rc, o = _git(root, 'log', '-1', '--format=%B', 版)
    m = re.search(r'(?mi)^Claude-Session:\s*\S*?(?:session_|cse_)?([A-Za-z0-9]{8,})\s*$', o or '') or re.search(r'(?m)^坐[：:]\s*(\S{8,})\s*$', o or '')
    return m.group(1)[:32] if rc == 0 and m else None


def 今之坐():
    """本会话之号（同 心跳.坐：去 session_／cse_ 之前缀）；无即 None。"""
    for k in ('CLAUDE_CODE_REMOTE_SESSION_ID', 'CLAUDE_SESSION_ID', 'CLAUDE_CODE_SESSION_ID'):
        v = os.environ.get(k, '').strip()
        if v:
            return re.sub(r'^(session_|cse_)', '', v)[:32]
    return None


def _秒(s):
    """'2026-10-24 06:16:36' 或 '2026-10-24T06:16:36'（UTC）→ epoch；坏即 None。"""
    try:
        return calendar.timegm(time.strptime(str(s)[:19].replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
    except Exception:
        return None


def _式(p):
    """glob → 正则（* 与 ? ⛔跨 /）。"""
    return re.compile('^' + ''.join('[^/]*' if c == '*' else '[^/]' if c == '?' else re.escape(c) for c in p) + '$')


# ───────── 盘：今之盘（root）或史之盘（某提交之树） ─────────
class 盘:
    def __init__(self, root, 版=None):
        self.root, self.版, self._诸 = root, 版, None
        self._缓, self._目 = {}, None

    def 有(self, 式):
        if self.版 is None:
            return sorted(os.path.relpath(p, self.root) for p in glob.glob(os.path.join(self.root, 式)))
        if self._诸 is None:
            rc, o = _git(self.root, 'ls-tree', '-r', '--name-only', self.版)
            self._诸 = [x for x in o.split('\n') if x] if rc == 0 else []
        r = _式(式)
        return [p for p in self._诸 if r.match(p)]

    def 在(self, 式):
        """档或目在否（glob）→ 所中之路们。史之盘：目以其下有档为在。"""
        if self.版 is None:
            return self.有(式)
        诸 = self.有(式)
        if self._目 is None:
            self._目 = sorted({'/'.join(p.split('/')[:k]) for p in self._诸 for k in range(1, p.count('/') + 1)})
        r = _式(式)
        return 诸 + [d for d in self._目 if r.match(d)]

    def 读(self, p):
        if p in self._缓:
            return self._缓[p]
        if self.版 is None:
            try:
                v = open(os.path.join(self.root, p), encoding='utf-8').read()
            except Exception:
                v = None
        else:
            rc, o = _git(self.root, 'show', '%s:%s' % (self.版, p))
            v = o if rc == 0 else None
        self._缓[p] = v
        return v

    def 踪(self, 式):
        """git 所踪之档（glob）→ 路们：今之盘问其索引（ls-files·⛔认 .gitignore 之盘上之档）、史之盘即其树。"""
        if self.版 is not None:
            return self.有(式)
        rc, o = _git(self.root, 'ls-files', '--', 式)
        return [x for x in o.split('\n') if x] if rc == 0 else []

    def 含(self, 词, 式们):
        """式们（glob）之档里含 词 者 → 路们（史之盘以 git grep 一回先滤，⛔逐档 show）。"""
        诸 = sorted({p for 式 in 式们 for p in self.有(式)})
        if self.版 is None:
            return [p for p in 诸 if 词 in (self.读(p) or '')]
        rc, o = _git(self.root, 'grep', '-l', '-F', '-e', 词, self.版, '--', *式们)
        中 = {x.split(':', 1)[1] for x in o.split('\n') if ':' in x} if rc == 0 else set()
        return [p for p in 诸 if p in 中]


# ───────── 迹：器跑没跑（今：_器之迹.jsonl 与 _跑账.json，缺则自云端承；史：版本/第N章/_器之迹.md） ─────────
class 迹:
    def __init__(self, root, 史=None, 承=None):
        self.root, self.史, self._承 = root, 史, 承
        self._账 = self._行 = None
        self._已承 = False

    def _载(self):
        if self._账 is None:
            try:
                self._账 = json.load(open(os.path.join(self.root, '_跑账.json'), encoding='utf-8'))
            except Exception:
                self._账 = {}
        if self._行 is None:
            self._行 = []
            try:
                for l in open(os.path.join(self.root, '_器之迹.jsonl'), encoding='utf-8'):
                    try:
                        self._行.append(json.loads(l))
                    except Exception:
                        pass
            except Exception:
                pass

    def _云(self):
        """一回：跑账.承（合云端诸存底之 _跑账）＋诸存底之 _器之迹.jsonl（一章一会话，前坐之迹在其存底）。承=False 即⛔网。⛔抛。"""
        if self._已承 or self._承 is False:
            return False
        self._已承 = True
        try:
            if self._承:
                self._承()
            else:
                import 跑账
                跑账.承(印=False)
            self._账 = None
            self._载()
            rc, o = _git(self.root, 'ls-remote', 'origin', 'refs/heads/备份/存底*')
            # ★1106（429·法用之守误拦）：他坐之存顶己底时，己底只挂於「存旧」之提交之亲（存底-旧 再被顶即埋二层）——
            #   只读诸枝之梢即失前坐交棒之迹（428 坐之「交棒之迹·--派令 429」埋於 存底-旧~1^2）。故每枝溯其近八笔（诸亲俱走），迹行去重。
            见 = set()
            for l in (o.strip().split('\n') if rc == 0 and o.strip() else []):
                rc1, 诸笔 = _git(self.root, 'rev-list', '--max-count=8', l.split()[0])
                for c in ((诸笔.split() if rc1 == 0 else []) or [l.split()[0]]):
                    rc2, t = _git(self.root, 'show', '%s:_器之迹.jsonl' % c)
                    for x in (t.split('\n') if rc2 == 0 else []):
                        if not x.strip() or x in 见:
                            continue
                        见.add(x)
                        try:
                            self._行.append(json.loads(x))
                        except Exception:
                            pass
            return True
        except Exception:
            return False

    def _判(self, 器, 自, 参, 近, 不, 今):
        """迹有本器开後之行者以迹为准（有参即须其参）；迹无本器之行方退取跑账之末跑（参未核）。
        自测之跑（参首 --自测：全测诸格俱跑之）⛔算用法——迹唯其自测者亦以迹为准（⛔退跑账：其末跑即自测）。"""
        全 = [x for x in self._行 if x.get('器') == 器 and str(x.get('t', '')) >= _iso(自)]
        诸 = [x for x in 全 if str((x.get('参') or [''])[0]) != '--自测']
        中 = [x for x in 诸 if not 参 or ' '.join(str(y) for y in x.get('参') or []).startswith(参)]
        t, 凭 = max([_秒(x.get('t')) or 0 for x in 中] or [0]), '迹'
        末 = _秒((self._账.get(器) or {}).get('末跑'))
        if not t and not 全 and 末 and 末 >= 自 and not (不 and 参):     # 不而有参：账不辨参，⛔凭账诬其跑
            t, 凭 = 末, '账'
        名 = 器 + (' ' + 参 if 参 else '')
        if 不:
            return ('⛔', '%s 於本章之开後跑过（%s）' % (名, _iso(t)[5:16])) if t else ('✓', '%s 本章之开後未跑' % 名)
        if not t:
            return '⛔', '%s 自本章之开（%s）未跑%s' % (名, _iso(自)[5:16], '（迹有其器而无此参）' if 诸 else '（迹唯其自测）' if 全 else '')
        if 近 and (今 or time.time()) - t > 近 * 60:
            return '⛔', '%s 末跑 %s，逾 %d 分' % (名, _iso(t)[5:16], 近)
        return '✓', '%s 跑於 %s%s' % (名, _iso(t)[5:16], ('（凭跑账·迹无其行%s）' % ('·参未核' if 参 else '')) if 凭 == '账' else '')

    def 查(self, 器, 自, 参=None, 近=None, 不=False, 今=None):
        """→ (态, 语)。态 ✓／⛔／？（史料不及）。本机不得即自云端承一回再判（⛔弱化判法）。"""
        if self.史 is not None:
            文 = self.史.读(self.史._迹档) or ''
            if 参 or 近 or 不:
                return '？', '史迹不录其参与时'
            return ('✓', '%s 见於本章之器之迹' % 器) if re.search(r'^\|\s*%s\s*\|' % re.escape(器), 文, re.M) else ('？', '%s 不在本章器之迹之窗（窗始於料成）' % 器)
        self._载()
        r = self._判(器, 自, 参, 近, 不, 今)
        # 凭跑账（本机之迹无其器而账有末跑）亦先承云端之迹：⛔凭跑账一笔放过他参或自测之跑（新机之迹空、跑账已承——验参即成空跑）
        if ((r[0] == '⛔' and not 不) or '凭跑账' in r[1]) and self._云():
            r = self._判(器, 自, 参, 近, 不, 今)
        return r


# ───────── 量：章之数（零 token：费账＋复盘之「按类」） ─────────
def 大审费(n, root=ROOT, 行=None):
    """至第 n 章之大审之费（费账诸行名含「大审…n」者之合·1027 #131：瘦式 ≤$25）；无行即 None。"""
    if 行 is None:
        try:
            行 = json.load(open(os.path.join(root, '设定', '费账.json'), encoding='utf-8')).get('行', [])
        except Exception:
            return None
    式 = re.compile(r'大审\D{0,4}(?:\d+\D{1,3})?%d(?!\d)' % n)
    v = [float(r.get('美元') or 0) for r in 行 if 式.search(str(r.get('名', '')))]
    return round(sum(v), 2) if v else None


def 章量(n, root=ROOT):
    """→ {W, 费, 主环, 主环占, 造占, 验占, 记占, 缓存读占, 大审费}（缺即无其键）。费＝该章 W 之诸行（⛔主会话），
    造／验＝复盘「按类」之造／验，记＝复盘诸 Run 表之「记席」行之美元（1027 #79：总章 §二.3 验≤15%、记≤5%）。"""
    try:
        行 = json.load(open(os.path.join(root, '设定', '费账.json'), encoding='utf-8')).get('行', [])
    except Exception:
        return {}
    审 = 大审费(n, root, 行)
    d, 费, 主, 读, 全 = ({'大审费': 审} if 审 is not None else {}), 0.0, 0.0, 0, 0
    for r in 行:
        m = re.match(r'(W\d+)·第?(\d{3})(?:章|造式)', str(r.get('名', '')))
        k = str(r.get('键', ''))
        if not m or int(m.group(2)) != n or k.startswith('主会话'):
            continue
        d['W'] = m.group(1)
        美 = float(r.get('美元') or 0)
        费 += 美
        if k.startswith('主环'):
            主 += 美
        elif k.startswith('wf_'):
            读 += int(r.get('缓存读') or 0); 全 += int(r.get('全量') or 0)
    if 'W' not in d:
        return d
    d.update(费=round(费, 2), 主环=round(主, 2), 主环占=round(主 / 费, 3) if 费 else None,
             缓存读占=round(读 / 全, 3) if 全 else None)
    造 = 验 = None
    记 = 0.0
    for p in glob.glob(os.path.join(root, '设定', '复盘', '*_%s_*.md' % d['W'])):
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:
            continue
        v = [float(x) for x in re.findall(r'(?m)^\s*造\s+\$\s*([\d.]+)', t)]
        if v:
            造 = (造 or 0) + sum(v)
            验 = (验 or 0) + sum(float(x) for x in re.findall(r'(?m)^\s*验\s+\$\s*([\d.]+)', t))
            记 += sum(float(x) for x in re.findall(r'(?m)^记席\S*(?:\s+\d+){7}\s+([\d.]+)\s', t))   # 来回 工具 新入 缓存建 缓存读 产出 全量 美元
    if 造 is not None and 费:
        d['造占'] = round(造 / 费, 3)
        d['验占'] = round((验 or 0) / 费, 3)
        d['记占'] = round(记 / 费, 3)
    return d


# ───────── 册 ─────────
def 读册(root=ROOT):
    return json.load(open(os.path.join(root, 册名), encoding='utf-8'))


def 当验(x, n):
    """此法於第 n 章当验否：起 ≤ n；十 只验於段首（上段之审）。"""
    if x.get('机证不能') or int(x.get('起', 起章)) > n:
        return False
    return x.get('时') != '十' or n == 段起(n)


def _示证(c):
    if '示' in c:
        return c['示']
    if '或' in c:
        return '或（%s）' % '｜'.join(_示证(y) for y in c['或'])
    if '若' in c:
        return '若 %s 则 %s' % (_示证(c['若']), _示证(c.get('则', {})))
    for k in 证之键:
        if k in c:
            v = c[k]
            if k == '档':
                return '%s%s' % (v, '「%s」' % (c['含'] if isinstance(c.get('含'), str) else '、'.join(c.get('含') or []))[:24] if c.get('含') else '')
            if k == 'git':
                return 'git %s %s' % (v, c.get('甲') or c.get('档') or c.get('枝') or '')
            return '%s %s%s' % (k, v, ' ' + c['参'] if c.get('参') else '')
    return '?'


# ───────── 验一证 ─────────
class 境:
    """一回之验之境：章、盘、迹、前（--前·阶後免）、史（回放：时之界）、取（是否自云端取 git 之引）。"""
    def __init__(self, n, root=ROOT, 前=False, 史版=None, 史至=None, 承=None, 取=True, 今=None):
        self.n, self.root, self.前, self.取 = n, root, 前, 取
        self.盘 = 盘(root, 史版)
        self.迹 = 迹(root, self.盘 if 史版 else None, 承)
        if 史版:
            self.盘._迹档 = os.path.join('版本', '第%d章' % n, '_器之迹.md')
        self.史至 = 史至                     # 回放：报、枝取此时之前者
        self.开 = 封时(n - 1, root, 史版 or 'HEAD')
        if self.开 is None and not 史版 and 取 and _git(root, 'rev-parse', '--is-shallow-repository')[1].strip() == 'true':
            _git(root, 'fetch', '-q', '--unshallow', 'origin', 限=600)   # 云端会话係浅克隆（五十笔）：前章之封或在其外——补全史一回再寻（同 全测.补浅克隆）
            self.开 = 封时(n - 1, root, 'HEAD')
        self.今 = 今
        self.坐 = None                       # 本章之坐（None 即取本会话之号；自测可代）
        self._取过 = set()

    def 取引(self, 枝):
        if not self.取 or 枝 in self._取过:
            return
        self._取过.add(枝)
        _git(self.root, 'fetch', '-q', 'origin', '+refs/heads/%s:refs/remotes/origin/%s' % (枝, 枝))


def 验证(c, e):
    """→ (态, 语)。态：✓ ⛔ ⚠ ？ 免。"""
    n = e.n
    if int(c.get('起', 0)) > n:
        return '免', '自 %s 起' % c['起']
    if c.get('段首') and n != 段起(n):
        return '免', '段首（%d）方验' % 段起(n)
    if c.get('阶') == '後' and e.前:
        return '免', '记席之後验（--後）'
    态, 语 = _验证(c, e)
    if 态 == '⛔' and c.get('轻'):
        态 = '⚠'
    return 态, 语


def _验证(c, e):
    n = e.n
    if '或' in c:
        果 = [验证(y, e) for y in c['或']]
        for 态, 语 in 果:
            if 态 in ('✓', '免'):
                return '✓', 语
        if any(态 == '？' for 态, _ in 果):
            return '？', '；'.join(语 for _, 语 in 果)[:160]
        return '⛔', '俱无：' + '｜'.join(语 for _, 语 in 果)[:200]
    if '若' in c:
        态, 语 = 验证(c['若'], e)
        if 态 != '✓':
            return '免', '若不成（%s）' % 语[:40]
        return 验证(c.get('则') or {}, e)
    if '跑' in c:
        if e.开 is None:
            return '⛔', '第%d章封版之提交寻不着——本章之开无界' % (n - 1)
        return e.迹.查(c['跑'], e.开, 填(c.get('参'), n), c.get('近'), c.get('不'), e.今)
    if '钩' in c:
        t = e.盘.读(os.path.join('.claude', 'settings.json'))
        if t is None:
            return '⛔', '.claude/settings.json 不在'
        于 = c.get('于')
        try:
            d = json.loads(t)
            if 于 == 'permissions':
                域 = '\n'.join((d.get('permissions') or {}).get('allow') or [])
            elif 于:
                域 = '\n'.join(h.get('command', '') for g in (d.get('hooks') or {}).get(于) or [] for h in g.get('hooks') or [])
            else:
                域 = t
        except Exception:
            域 = t
        return ('✓', '%s 之钩含 %s' % (于 or 'settings', c['钩'])) if c['钩'] in 域 else ('⛔', '%s 无 %s' % (于 or 'settings', c['钩']))
    if '报' in c:
        路 = '报/%s.json' % 填(c['报'], n)
        e.取引('备份/报')
        引 = 'refs/remotes/origin/备份/报'
        if e.史至 is not None:
            rc, o = _git(e.root, 'log', '-1', '--format=%H', '--until=@%d' % e.史至, 引)
            引 = o.strip() if rc == 0 and o.strip() else None
        elif _git(e.root, 'rev-parse', '-q', '--verify', 引)[0] != 0:
            引 = None
        if not 引:
            return '⛔', '%s 无凭：备份/报 无此枝%s' % (路, '（彼时）' if e.史至 is not None else '')
        rc, o = _git(e.root, 'show', '%s:%s' % (引, 路))
        if rc != 0:
            return '⛔', '%s 不在（备份/报）' % 路
        try:
            果 = json.loads(o).get('果')
        except Exception:
            return '⛔', '%s 坏' % 路
        return ('✓', '%s 果＝%s' % (路, 果)) if 果 in (c.get('果') or 果默) else ('⛔', '%s 果＝%s' % (路, 果))
    if 'git' in c:
        k = c['git']
        if k == '含':
            甲, 乙 = 填(c['甲'], n), 填(c['乙'], n)
            for x in (甲, 乙):
                e.取引(x)
            a = _git(e.root, 'rev-parse', '-q', '--verify', 'refs/remotes/origin/%s' % 甲)
            if a[0] != 0:
                return '⛔', 'origin 无 %s' % 甲
            rc, _ = _git(e.root, 'merge-base', '--is-ancestor', a[1].strip(), 'refs/remotes/origin/%s' % 乙)
            return ('✓', '%s 已在 %s' % (甲, 乙[:12])) if rc == 0 else ('⛔', '%s 不在 %s' % (甲, 乙[:12]))
        if k == '改' and c.get('自'):     # 自（1027 #100·段末之证）：档於第「自」章封版以来有提交（窗跨一段，⛔只认前章封後）
            m = int(填(str(c['自']), n))
            t0 = 封时(m, e.root, e.盘.版 or 'HEAD')
            if t0 is None:
                return '⛔', '第%d章封版之提交寻不着（自）' % m
            档 = 填(c['档'], n)
            rc, o = _git(e.root, 'log', '--format=%h', '--since=@%d' % (t0 + 1), e.盘.版 or 'HEAD', '--', 档)
            return ('✓', '%s 自第%d章封版以来有提交 %s' % (档, m, o.split()[0])) if rc == 0 and o.strip() else ('⛔', '%s 自第%d章封版（%s）无提交' % (档, m, _iso(t0)[5:16]))
        if k == '坐异':                   # 坐异（1027 #87·换会话之证）：前章封版之坐 ≠ 本章之坐（今：本会话；史：本章封版之提交）
            甲 = 封提交(n - 1, e.root, e.盘.版 or 'HEAD')
            坐甲 = 提交之坐(e.root, 甲) if 甲 else None
            坐乙 = 提交之坐(e.root, e.盘.版) if e.盘.版 else (e.坐 if e.坐 is not None else 今之坐())
            if not 坐甲 or not 坐乙:
                return '？', '坐不可辨（第%d章封版%s；本章%s）' % (n - 1, '之提交寻不着' if not 甲 else '之提交无 Claude-Session',
                                                       '之坐未名' if not 坐乙 else '之坐 %s' % 坐乙[:12])
            return ('✓', '第%d章之坐 %s ≠ 本章之坐 %s' % (n - 1, 坐甲[:12], 坐乙[:12])) if 坐甲 != 坐乙 else \
                ('⛔', '第%d章与第%d章同坐 %s——封一章即换会话（总章 §二.5、§三.5）' % (n - 1, n, 坐甲[:12]))
        if k == '改':
            if e.开 is None:
                return '⛔', '第%d章封版之提交寻不着' % (n - 1)
            档 = 填(c['档'], n)
            if c.get('于封'):      # 于封（1027 A2 验）：档须在前章封版之提交本身——「或其後」之证旧序（封後另提交）亦过，空跑
                h = 封提交(n - 1, e.root, e.盘.版 or 'HEAD')
                rc, o = _git(e.root, 'show', '--name-only', '--format=', h, '--', 档) if h else (1, '')
                return ('✓', '%s 在前章封版之提交 %s' % (档, h[:8])) if rc == 0 and o.strip() else ('⛔', '%s 不在前章封版之提交（%s）' % (档, (h or '寻不着')[:8]))
            # 含封（1027 A2·一章一提交）：交接与复盘入封版#N 之一提交——前章之封版之提交本身亦算（⛔只认其後之笔）
            rc, o = _git(e.root, 'log', '--format=%h', '--since=@%d' % (e.开 + (0 if c.get('含封') else 1)), e.盘.版 or 'HEAD', '--', 档)
            return ('✓', '%s 於前章封後有提交 %s' % (档, o.split()[0])) if rc == 0 and o.strip() else ('⛔', '%s 自前章封版（%s）无提交' % (档, _iso(e.开)[5:16]))
        if k == '枝':
            枝 = 填(c['枝'], n)
            if e.史至 is not None:
                rc, o = _git(e.root, 'log', '-1', '--format=%h', '--until=@%d' % e.史至, 'refs/remotes/origin/%s' % 枝)
                return ('✓', 'origin/%s 彼时在' % 枝) if rc == 0 and o.strip() else ('⛔', 'origin/%s 彼时无' % 枝)
            if e.取:
                rc, o = _git(e.root, 'ls-remote', '--heads', 'origin', 枝)
            else:
                rc, o = _git(e.root, 'rev-parse', '-q', '--verify', 'refs/remotes/origin/%s' % 枝)
            return ('✓', 'origin/%s 在' % 枝) if rc == 0 and o.strip() else ('⛔', 'origin 无 %s 之枝' % 枝)
        return '⛔', 'git 之式不识：%s' % k
    if '档' in c:
        式 = 填(c['档'], n)
        诸 = e.盘.有(式)
        if c.get('不'):
            return ('⛔', '%s 在' % 式) if 诸 else ('✓', '%s 不在' % 式)
        if not 诸:
            return '⛔', '%s 不在' % 式
        含 = c.get('含') or []
        含 = [含] if isinstance(含, str) else 含
        无 = c.get('无')
        缺语 = ''
        for p in 诸:
            文 = e.盘.读(p) or ''
            缺 = [x for x in 含 if not re.search(填(x, n), 文)]
            犯 = re.search(填(无, n), 文) if 无 else None
            if not 缺 and not 犯:
                return '✓', p
            缺语 = '%s %s' % (p, ('缺「%s」' % '」「'.join(填(x, n) for x in 缺)) if 缺 else '犯「%s」' % 犯.group(0)[:30])
        return '⛔', 缺语 if not c.get('示') or len(诸) > 1 else '%s——%s' % (缺语, c['示'])
    if '量' in c:
        m = int(填(str(c.get('章', '{N-1}')), n))
        v = 章量(m, e.root).get(c['量'])
        if v is None:
            return '⛔', '第%d章无「%s」之数（费账／复盘）' % (m, c['量'])
        if '≥' in c and v < c['≥']:
            return '⛔', '第%d章%s %.0f%%（须≥%.0f%%）' % (m, c['量'], v * 100, c['≥'] * 100) if v <= 1 else '第%d章%s %.2f（须≥%s）' % (m, c['量'], v, c['≥'])
        if '≤' in c and v > c['≤']:
            return '⛔', '第%d章%s %.0f%%（须≤%.0f%%）' % (m, c['量'], v * 100, c['≤'] * 100) if v <= 1 else '第%d章%s %.2f（须≤%s）' % (m, c['量'], v, c['≤'])
        return '✓', '第%d章%s %s' % (m, c['量'], v)
    if '限' in c:
        return ('✓', '未到限 %s' % c['限']) if n <= int(c['限']) else ('⛔', '逾限 %s' % c['限'])
    return '⛔', '证之式不识：%s' % '、'.join(c)


def 验法(x, e):
    """→ (态, [(态, 语)])。⛔ 者有一即 ⛔；⚠／？ 者为 ⚠。"""
    果 = [验证(c, e) for c in x.get('证') or []]
    态 = '⛔' if any(a == '⛔' for a, _ in 果) else '⚠' if any(a in ('⚠', '？') for a, _ in 果) else '✓'
    return 态, 果


# ───────── 完备之律（立法须同日立证） ─────────
def _日序(md):
    return (0 if int(md[:2]) >= 7 else 1, md)


def 总章之八(root=ROOT):
    """→ {号: 首句}。"""
    try:
        t = open(os.path.join(root, 总章名), encoding='utf-8').read()
    except Exception:
        return {}
    m = re.search(r'^## 八、[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
    return {int(a): b.strip()[:30] for a, b in re.findall(r'(?m)^(\d+)\.\s*(.*)$', m.group(1))} if m else {}


def 总章之八全(root=ROOT):
    """→ {号: 全文}（§八 ≥23 之条须书所废、较旧·1027 #134）。"""
    t = _读(root, 总章名) or ''
    m = re.search(r'^## 八、[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
    return {int(a): b.strip() for a, b in re.findall(r'(?m)^(\d+)\.\s*(.*)$', m.group(1))} if m else {}


def 法账之新行(root=ROOT, 自=立日):
    """方法账诸表之行，其日 ≥ 自 者 → [(键, 全行)]。日：表头有「日」栏者取其栏；否则取件之「（MMDD」或「MMDD·」。"""
    try:
        t = open(os.path.join(root, 法账名), encoding='utf-8').read()
    except Exception:
        return []
    出, 头 = [], None
    for l in t.split('\n'):
        if not l.startswith('|'):
            头 = None
            continue
        格 = [x.strip() for x in l.strip().strip('|').split('|')]
        if 头 is None:
            头 = 格
            continue
        if all(set(x) <= set('-: ') for x in 格):
            continue
        日 = None
        if '日' in 头 and 头.index('日') < len(格) and re.fullmatch(r'\d{4}', 格[头.index('日')]):
            日 = 格[头.index('日')]
        if not 日:
            m = re.search(r'（(\d{4})|^\**(\d{4})·', 格[0])
            日 = (m.group(1) or m.group(2)) if m else None
        if 日 and not re.fullmatch(r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])', 日):
            日 = None                        # 「（2610字）」之类非日——⛔误作新行
        if 日 and _日序(日) >= _日序(自):
            键 = re.split(r'[（(]', 格[0].replace('*', ''), maxsplit=1)[0].strip()
            出.append((键, l))
    return 出


# ───────── 完备之律·扩（1027 执行之核：作者常令、总章诸条、行为之证、所废较旧） ─────────
_汉 = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
五主 = ('虫洞', '虹吸', '完美', '丝滑', '执行', '进化', 'GitHub')   # 1106：进化主义入总章（六大主义）；1119：GitHub 主义入为第七（七大主义）——七条俱须有据、俱入执行之守
_路式 = re.compile(r'(?:工具|设定|正文|版本)/[^\s`\'"）)，,、；;」〕\]。：:（(·]+|\.claude/settings\.json|00_总章\.md|README\.md')
_较旧式 = re.compile(r'较旧[：:]\s*(?:无|[^|\n]*效[^|\n]*费)')


def _读(root, p):
    try:
        return open(os.path.join(root, p), encoding='utf-8').read()
    except Exception:
        return None


def 总章之条(root=ROOT):
    """总章须有据之条 → [(键, 文)]：五大主义（五大·<名>）、心诀（心诀N；「见五大主义」之指⛔计）、
    §二、§三、§六 之编号之规（§二.N）、§四（一条）、§五 每「｜」之守（§五·k）。§一、§七、§八 不在此（§八 另有其律）。"""
    t = _读(root, 总章名)
    if t is None:
        return []
    出 = []
    头 = re.split(r'(?m)^## ', t, maxsplit=1)[0]
    for m in re.finditer(r'(?m)^\d+\.\s*\*\*(%s)\*\*[：:]\s*(.*)$' % '|'.join(五主), 头):
        出.append(('五大·' + m.group(1), m.group(2)))
    for 节 in re.split(r'(?m)^## ', t)[1:]:
        题, _, 体 = 节.partition('\n')
        if 题.startswith('心诀'):
            for m in re.finditer(r'(?m)^(\d+)\.\s*(.*)$', 体):
                if not re.match(r'\*\*[^*]+\*\*[：:]\s*见[五六七]大主义[^。；;\n]*。?\s*$', m.group(2)):   # 纯指（其後无他规）方⛔计——「见五大主义…。另：新规」照计
                    出.append(('心诀%s' % m.group(1), m.group(2)))
            continue
        k = 题[:1]
        if 题[1:2] != '、':
            continue
        if k in '二三六':
            for m in re.finditer(r'(?m)^(\d+)\.\s*(.*)$', 体):
                出.append(('§%s.%s' % (k, m.group(1)), m.group(2)))
        elif k == '四':
            出.append(('§四', 体.strip()))
        elif k == '五':
            for i, g in enumerate(x.strip() for x in 体.strip().split('｜')):
                if g:
                    出.append(('§五·%d' % (i + 1), g))
    return 出


def 据之引(s):
    """一据之串 → (所点之总章之键们, §五 之词们)。认：§二.3（§三.1—5 之段）、§四、心诀七（心诀七、八）、五大主义·执行（五大主义·执行、丝滑）、
    §五「管档」（§五·鼎心）。"""
    键, 词 = set(), []
    for m in re.finditer(r'§([二三六])\.(\d+)(?:\s*[—\-–~～]\s*(\d+))?', s):
        for i in range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1):
            键.add('§%s.%d' % (m.group(1), i))
    if re.search(r'§四(?![.\d])', s):
        键.add('§四')
    for m in re.finditer(r'心诀((?:[一二三四五六七八1-8][、，,]?)+)', s):
        for ch in re.findall(r'[一二三四五六七八1-8]', m.group(1)):
            键.add('心诀%d' % (_汉.get(ch) or int(ch)))
    for m in re.finditer(r'[五六七]大主义((?:[·・、]?(?:%s))+)' % '|'.join(五主), s):
        for x in re.findall('|'.join(五主), m.group(1)):
            键.add('五大·' + x)
    for m in re.finditer(r'§五((?:「[^」]+」|·[^\s；;，,。）)「·]+)+)', s):
        词 += [a or b for a, b in re.findall(r'「([^」]+)」|·([^·「]+)', m.group(1)) if a or b]
    return 键, 词


def _清(s):
    return re.sub(r'[`*]', '', s or '')


def 总章之盖(册, root=ROOT):
    """→ (红[], 条数)：总章之条无一法／待／废（或「机证不能」）之据点之者；机证不能之条逾四之一亦红。"""
    条 = 总章之条(root)
    机 = 册.get('机证不能') or []
    红 = []
    for x in 机:
        if not isinstance(x, dict) or not x.get('据') or len(str(x.get('由') or '')) < 8:
            红.append('⛔ 册坏：机证不能之条须 据（所点之总章之条）、由（≥八字）：%s' % json.dumps(x, ensure_ascii=False)[:50])
    def 引之(据们):
        键, 词 = set(), []
        for s in 据们:
            a, b = 据之引(s)
            键 |= a
            词 += b
        return 键, 词

    def 中(k, 文, 键词):
        return k in 键词[0] or (k.startswith('§五·') and any(w in _清(文) for w in 键词[1]))
    # 真据：法（机证不能者除）、待、废、册之「机证不能」；机证不能之法之据只算「机证不能」（⛔以纯理之法冒充有证·复核补：其条入四之一之数）
    真 = 引之([str(x.get('据', '')) for k in ('法', '待', '废') for x in 册.get(k) or [] if not (k == '法' and x.get('机证不能'))]
             + [str(x.get('据', '')) for x in 机 if isinstance(x, dict)])
    机法 = 引之([str(x.get('据', '')) for x in 册.get('法') or [] if x.get('机证不能')])
    机外 = []
    for k, 文 in 条:
        if 中(k, 文, 真):
            continue
        if 中(k, 文, 机法):
            机外.append(k)
            continue
        红.append('⛔ 法立无证：总章 %s「%s」——册无一法／待／废之据点之（据写作 §二.3、心诀七、五大主义·执行、§五「<守之词>」；纯理入册「机证不能」带由）'
                 % (k, _清(文)[:24]))
    数 = len(机) + len(机外)
    if 条 and 数 / len(条) > 机证之顶:
        红.append('⛔ 机证不能 %d／%d（总章之条%s）逾四之一——纯理太多，即规多不可验' % (
            数, len(条), '；只为机证不能之法所点者 %s' % '、'.join(机外[:4]) if 机外 else ''))
    return 红, len(条)


def 常令之令(root=ROOT, 自=令起日):
    """作者常令之「- MMDD …」之行（日 ≥ 自）→ [(行号, 日, 行)]。"""
    出 = []
    for i, l in enumerate((_读(root, 常令名) or '').split('\n'), 1):
        m = re.match(r'^-\s*(\d{4})\s', l)
        if m and re.fullmatch(r'(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])', m.group(1)) and _日序(m.group(1)) >= _日序(自):
            出.append((i, m.group(1), l))
    return 出


def 册之引(册):
    """→ (诸据之文, 诸证之档之集, 诸证之跑之集)（递入 或／若／则）。"""
    文们, 档们, 跑们 = [], set(), set()

    def 入(c):
        if not isinstance(c, dict):
            return
        if '档' in c:
            档们.add(str(c['档']))
        if '跑' in c:
            跑们.add(str(c['跑']))
        for y in c.get('或') or []:
            入(y)
        if '若' in c:
            入(c['若'])
            入(c.get('则'))
    for k in ('法', '待', '废'):
        for x in 册.get(k) or []:
            文们.append(str(x.get('据', '')))
            for c in x.get('证') or []:
                入(c)
    return '\n'.join(文们), 档们, 跑们


def 常令之验(册, root=ROOT):
    """作者常令 1021 起每条：行内「法用#<id>」（id 在册），或其「落」所点之器／档在盘且为册（据、证）所引 → (红[], 令数)。
    落所点之档不在盘亦红；引册外之 id 亦红。"""
    ids = {x.get('id') for k in ('法', '待', '废') for x in 册.get(k) or []}
    据文, 档们, 跑们 = 册之引(册)
    红, 令们 = [], 常令之令(root)
    for i, 日, l in 令们:
        首 = re.sub(r'^-\s*\d{4}\s*', '', l)[:20]
        引 = re.findall(r'法用#([^\s，,；;|）)」』〕\]、。：:]+)', l)
        坏 = [x for x in 引 if x not in ids]
        if 坏:
            红.append('⛔ 令引之法不在册：作者常令 L%d（%s）「法用#%s」' % (i, 首, 坏[0]))
        m = re.search(r'——(?:落处?|入)[：:]?(.*)$', l)
        路们 = [p.rstrip('。.') for p in _路式.findall(m.group(1) if m else '')]
        缺 = [p for p in 路们 if not glob.glob(os.path.join(root, p))]
        if 缺:
            红.append('⛔ 令落之档不在：作者常令 L%d（%s）点 %s——器改名、已删：令随之改' % (i, 首, 缺[0]))
        if any(x in ids for x in 引):
            continue
        盖 = [p for p in 路们 if p not in 缺 and (p in 据文 or any(p == d or fnmatch.fnmatchcase(p, d) for d in 档们)
                                                 or (p.startswith('工具/') and os.path.basename(p) in 跑们))]
        if not 盖:
            红.append('⛔ 令立无证：作者常令 L%d（%s）——行内写「法用#<id>」，或其「落」所点之器／档须在盘且为法用册所引' % (i, 首))
    return 红, len(令们)


def _有行(c):
    """一证係行为之证否：跑／git／报／量，或章之迹（档之路或其「含」带 {N} 之类——本章之产物）；或 须诸支俱是、若 看其则。"""
    if not isinstance(c, dict):
        return False
    if '或' in c:
        return bool(c['或']) and all(_有行(y) for y in c['或'])
    if '若' in c:
        return _有行(c.get('则'))
    if any(k in c for k in 行为之键):
        return True
    return '档' in c and not c.get('不') and any(z in json.dumps([c['档'], c.get('含')], ensure_ascii=False) for z in 章迹之占)


def 行为之验(册):
    """时∈开／封前／封後 之法（机证不能者除）须至少一条行为之证，或书「钩自跑」带钩之证（1027 #132 #102）→ 红[]。"""
    红 = []
    for x in 册.get('法') or []:
        if x.get('机证不能') or x.get('时') not in ('开', '封前', '封後'):
            continue
        证们 = [c for c in x.get('证') or [] if isinstance(c, dict)]
        if any(_有行(c) for c in 证们):
            continue
        if len(str(x.get('钩自跑') or '')) >= 2 and any('钩' in c for c in 证们):
            continue
        红.append('⛔ 法证只验码在：%s（时 %s）——须一条行为之证（跑／git／报／量，或章之迹：档之路带 {N} 之类），或书「钩自跑」带钩之证'
                 % (x.get('id', '?'), x.get('时')))
    return 红


def 废旧之验(root=ROOT):
    """方法账 1027 起之行、总章§八 ≥23 之条：须书「所废」与「较旧：效…；费…」（或「较旧：无」）（1027 #134）→ 红[]。"""
    红 = []
    for 键, 行 in 法账之新行(root):
        if '所废' not in 行 or not _较旧式.search(行):
            红.append('⛔ 法缺所废较旧：方法账「%s」——取一法须书「所废：…」与「较旧：效…；费…」（无旧可比写「较旧：无」·五大主义·虫洞）' % 键[:30])
    for k, 文 in sorted(总章之八全(root).items()):
        if k >= 23 and ('所废' not in 文 or not _较旧式.search(文)):
            红.append('⛔ 法缺所废较旧：总章§八.%d「%s」——须书「所废：…」与「较旧：效…；费…」' % (k, 文[:20]))
    return 红


def 暂停之据(root=ROOT):
    """作者之暂停令在（未解、引作者原话）而其据（档:行）之行无「暂停令」→ 红：改常令移其行号，令在而器不认
    （暂停令.在 判否——段序之守、会话之守俱放，作者之停令即被悄悄撤）。1027 施工自逮：常令删一行，据之 L469 移一行即「不认」。"""
    try:
        d = json.load(open(os.path.join(root, '设定', '暂停令.json'), encoding='utf-8'))
    except Exception:
        return []
    if not isinstance(d, dict) or d.get('解') or '作者令' not in str(d.get('令', '')):
        return []
    m = re.match(r'(.+?):(\d+)$', str(d.get('据', '')))
    L = (_读(root, m.group(1)) or '').split('\n') if m else []
    行 = L[int(m.group(2)) - 1] if m and 0 < int(m.group(2)) <= len(L) else ''
    if '暂停令' in 行:
        return []
    今 = [str(i) for i, l in enumerate(L, 1) if '暂停令' in l and '作者令' in l][-1:]
    return ['⛔ 暂停令之据失位：%s 之行无「暂停令」——令在而器不认（段序之守、会话之守俱放）；改其据之行号%s、⛔再移常令之行'
            % (d.get('据', '（无据）'), '（今在 L%s）' % 今[0] if 今 else '')]


def 完备(册, root=ROOT):
    """→ (红[], 黄[])。"""
    红, 黄 = [], []
    法, 待, 废 = 册.get('法') or [], 册.get('待') or [], 册.get('废') or []
    ids = [x.get('id') for x in 法 + 待 + 废]
    for i in set(ids):
        if ids.count(i) > 1:
            红.append('⛔ 册坏：id 重 %s' % i)
    法ids = {x.get('id') for x in 法}
    for x in 法:                       # 执行之守·丝滑之守（1027）：功、处、流程须书；流程之法须演（或演练之律前已行之演免）
        名 = x.get('id', '?')
        if not x.get('功') or x.get('处') not in 诸处 or not isinstance(x.get('流程'), bool):
            红.append('⛔ 册坏：%s 缺 功／处（%s）／流程（true｜false）' % (名, '｜'.join(诸处)))
        if x.get('流程'):
            if x.get('演免'):
                if len(str(x['演免'])) < 8 or int(x.get('立', 999)) > 演律之界:
                    红.append('⛔ 册坏：%s 演免须由（≥八字），且只许立 ≤ %d 之法（演练之律前已行）——其後之流程之法须真料之演' % (名, 演律之界))
            elif not x.get('演') or not all(isinstance(s, dict) and ('账' in s or '报' in s) for s in x['演']):
                红.append('⛔ 册坏：%s 係流程之法而无「演」（账｜报之源）亦无「演免」' % 名)
        for y in x.get('互补') or []:
            if not isinstance(y, dict) or y.get('与') not in 法ids or len(str(y.get('由') or '')) < 4:
                红.append('⛔ 册坏：%s 之互补须 与（法之 id）、由' % 名)
    for x in 废:
        名 = x.get('id', '?')
        if not all(x.get(k) for k in ('id', '名', '据', '去证')) or not re.fullmatch(r'\d{4}', str(x.get('废于', ''))) \
                or not re.fullmatch(r'[0-9a-f]{7,40}', str(x.get('在', ''))):
            红.append('⛔ 册坏：废 %s 缺 id／名／据／废于（MMDD）／在（废前之笔·证去证真验）／去证' % 名)
        if x.get('待合') and not isinstance(x.get('限'), int):
            红.append('⛔ 册坏：废 %s 待合而无限（数·其章封前须尽）' % 名)
        if x.get('处') and x['处'] not in 诸处:
            红.append('⛔ 册坏：废 %s 之处不识 %s' % (名, x['处']))
        for c in x.get('去证') or []:
            if not isinstance(c, dict) or sum(k in c for k in 去证之键) != 1 or ('无文' in c and not c.get('于')):
                红.append('⛔ 册坏：废 %s 之去证不识 %s（%s 择一；无文须于）' % (名, json.dumps(c, ensure_ascii=False)[:50], '｜'.join(去证之键)))
                continue
            for k in ('无文', '推报验'):
                try:
                    re.compile(c[k]) if k in c else None
                except re.error as e:
                    红.append('⛔ 册坏：废 %s 之%s 正则坏：%s' % (名, k, e))

    def 验式(c, 名):
        if not isinstance(c, dict) or not any(k in c for k in 证之键):
            红.append('⛔ 册坏：%s 之证不识 %s' % (名, json.dumps(c, ensure_ascii=False)[:60]))
            return
        for y in c.get('或') or []:
            验式(y, 名)
        if '若' in c:
            验式(c['若'], 名); 验式(c.get('则'), 名)
        if c.get('git') and c['git'] not in ('含', '改', '枝', '坐异'):
            红.append('⛔ 册坏：%s 之 git 式不识 %s' % (名, c['git']))
    据们 = []
    for x in 法:
        名 = x.get('id', '?')
        if not all(x.get(k) for k in ('id', '名', '据')) or not isinstance(x.get('起'), int) or x.get('时') not in 时们:
            红.append('⛔ 册坏：%s 缺 id／名／据／起（数）／时（%s）' % (名, '｜'.join(时们)))
        if x.get('机证不能'):
            if len(str(x.get('由') or '')) < 8:
                红.append('⛔ 机证不能而无由：%s' % 名)
        elif not x.get('证'):
            红.append('⛔ 法立无证：%s（无证、亦未书机证不能）' % 名)
        for c in x.get('证') or []:
            验式(c, 名)
        据们.append(str(x.get('据', '')))
    for x in 待:
        名 = x.get('id', '?')
        if not all(x.get(k) for k in ('id', '名', '据', '证')) or not isinstance(x.get('限'), int):
            红.append('⛔ 册坏：待 %s 缺 id／名／据／限（数）／证' % 名)
        for c in x.get('证') or []:
            验式(c, 名)
        据们.append(str(x.get('据', '')))
    for x in 册.get('缓') or []:
        if x.get('id') not in ids or not isinstance(x.get('立'), int) or not isinstance(x.get('至'), int) \
                or not 0 <= x['至'] - x['立'] <= 3 or len(str(x.get('由') or '')) < 4:
            红.append('⛔ 缓坏：%s（id 须在册、至－立 ≤3、由须写）' % x.get('id'))
    if 法:
        机 = sum(1 for x in 法 if x.get('机证不能'))
        if 机 / len(法) > 机证之顶:
            红.append('⛔ 机证不能 %d／%d 逾四之一——纯理太多，即法多不可验' % (机, len(法)))
    盖 = set(int(k) for s in 据们 for k in re.findall(r'§八\.(\d+)', s))
    八 = 总章之八(root)
    for k, 首 in sorted(八.items()):
        if k not in 盖:
            红.append('⛔ 法立无证：总章§八.%d「%s」——册无一条之据点之（入 %s，带证）' % (k, 首, 册名))
    for k in sorted(盖 - set(八)):
        黄.append('⚠ 据未见：§八.%d 总章尚无（待合流添之）' % k)
    令们 = set(re.findall(r'方法账\.md\s+([^；;，,\s]+)', '\n'.join(据们)))
    for 键, 行 in 法账之新行(root):
        ok = any(键 and 键 in s for s in 据们) or any(键.startswith(t) for t in 令们) \
            or any(i and ('法用#%s' % i) in 行 for i in ids)
        if not ok:
            红.append('⛔ 法立无证：方法账「%s」（%s 起之行）——册无据点之；入册带证，或行内写「法用#<id>」' % (键[:30], 立日))
    # 完备之律·扩（1027 执行之核）：作者常令 1021 起之令、总章诸条、行为之证、所废较旧
    红 += 常令之验(册, root)[0] + 总章之盖(册, root)[0] + 行为之验(册) + 废旧之验(root) + 暂停之据(root)
    底 = 册.get('未行')
    if 底 is not None and not (isinstance(底, dict) and isinstance(底.get('底'), int)):
        红.append('⛔ 册坏：「未行」须 {底: 数, 记: [...]}（未行之数之棘轮·唯一处）')
    return 红, 黄


# ───────── 验 ─────────
def 缓之(册, i, n):
    for x in 册.get('缓') or []:
        if x.get('id') == i and x.get('立', 0) <= n <= x.get('至', -1):
            return x
    return None


def 执之验(册, e, n, root=ROOT, 取=True):
    """执行之守·丝滑之守：废而未除、二写者、同功两处、流程之法之演 → (红, 黄, 演之果 {id: (态, 语)}, 计)。"""
    废红, 废黄 = 验废(册, e.盘, n)
    写红, 诸 = 验写者(e.盘, root=root)
    同红 = 同功(册)
    录 = 演录(e.盘, root, 取=取) if any(x.get('流程') and not x.get('演免') for x in 册.get('法') or []) else []
    演果 = {x['id']: 验演(x, 录, 封时(int(x.get('起', 起章)), root)) for x in 册.get('法') or [] if x.get('流程')}
    计 = {'废': len(册.get('废') or []), '废红': len(废红), '待合': len(废黄), '写': len([w for w in 诸 if w.get('族') != '演']),
          '演': len([w for w in 诸 if w.get('族') == '演']), '二写': len(写红), '同': len(同红),
          '流程': len(演果), '演过': sum(1 for a, _ in 演果.values() if a == '✓'), '演免': sum(1 for a, _ in 演果.values() if a == '免')}
    return 废红 + 写红 + 同红, 废黄, 演果, 计


def 验(n, 前=False, root=ROOT, 册=None, 境_=None, 执=True):
    """→ (ok, 诸行)。执：并验执行之守·丝滑之守（废、写者、同功、演）。"""
    册 = 册 or 读册(root)
    e = 境_ or 境(n, root, 前)
    红, 黄 = 完备(册, root)
    完红数 = len(红)
    演果, 执计 = {}, None
    if 执:
        e.取引('备份/报')
        执红, 执黄, 演果, 执计 = 执之验(册, e, n, root, 取=False)
        红, 黄 = 红 + 执红, 黄 + 执黄
    行, 计 = [], {'✓': 0, '⛔': 0, '⚠': 0}
    应 = [x for x in 册.get('法') or [] if 当验(x, n)]
    for x in 应:
        态, 果 = 验法(x, e)
        if x['id'] in 演果 and 演果[x['id']][0] == '⛔':      # 流程之法未演：即法未行（⛔真料演练方上）——缓可暂免
            态, 果 = '⛔', 果 + [演果[x['id']]]
        if 态 == '⛔' and 缓之(册, x['id'], n):
            态 = '⚠'
            果 = [(a if a != '⛔' else '⚠', 语 + '（缓至 %d：%s）' % (缓之(册, x['id'], n)['至'], 缓之(册, x['id'], n)['由'][:20])) for a, 语 in 果]
        计[态] += 1
        if 态 != '✓':
            语 = '；'.join(语 for a, 语 in 果 if a in ('⛔', '⚠', '？'))
            行.append('%s %s（%s）：%s' % (态, x['id'], _据短(x['据']), 语[:200]))
    待到, 待红 = 0, 0
    for x in 册.get('待') or []:
        if n < x['限']:
            continue
        待到 += 1
        态, 果 = 验法(x, e)
        if 态 == '⛔' and 缓之(册, x['id'], n):
            态 = '⚠'
        if 态 != '✓':
            待红 += 态 == '⛔'
            行.append('%s 待·%s（限 %d）：%s——%s' % (态, x['id'], x['限'], '；'.join(语 for a, 语 in 果 if a != '✓')[:160], x.get('示', '')[:40]))
    ok = not 红 and 计['⛔'] == 0 and not 待红
    头 = '%s 法用之守 --验 %d%s：应验 %d 法（✓%d ⛔%d ⚠%d）｜待到期 %d（⛔%d）｜完备 %s' % (
        '✓' if ok else '⛔', n, '·前' if 前 else '', len(应), 计['✓'], 计['⛔'], 计['⚠'], 待到, 待红, '✓' if not 完红数 else '⛔%d' % 完红数)
    if 执计:
        头 += '｜执：废而未除 %d、写者之红 %d、同功两处 %d、流程未演 %d' % (执计['废红'], 执计['二写'], 执计['同'],
                                                      sum(1 for a, _ in 演果.values() if a == '⛔'))
    return ok, [头] + 红 + 行 + 黄


def _据短(s):
    m = re.search(r'§[一二三四五六七八九十]+[.\d]*', s or '')
    return m.group(0) if m else (s or '')[:12]


def 开(n, root=ROOT, 册=None, 执=True):
    """开章：本章须用之法 → 其证（≤10 行）。开时之证零网先验（档、钩、跑）；余只列。执：并印执行之守之红（本章封前须尽之废、未演之流程之法）。"""
    册 = 册 or 读册(root)
    出 = ['── 法用之守·第%d章须用之法（封版 --前 印、--後 拦；全册 python3 工具/法用之守.py --册）──' % n]
    项 = []
    try:
        e = 境(n, root, True, 取=False, 承=False)          # ⛔网：开章只读本机
    except Exception:
        e = None
    for x in sorted(册.get('待') or [], key=lambda x: x['限']):
        if x['限'] <= n + 1:
            态 = 验法(x, e)[0] if e else '·'
            项.append('%s 待·%s（限%d）→ %s' % ('✓' if 态 == '✓' else '⛔' if x['限'] <= n else '…', x['id'], x['限'], x.get('示', '')[:46]))
    if e and 执:                       # 执行之守·丝滑之守：本章封前须尽之废、须演之流程之法、写者与同功之红——开章即见（⛔候封版方红）
        try:
            执红, 执黄, 演果, _ = 执之验(册, e, n, root, 取=False)        # n：本章封前须尽者（待合之限 ≤ n）即红
            项 += [x[:90] for x in 执红[:2] + 执黄[:1]]
            项 += ['⛔ 演·%s（起 %s）未演 → 真料演练方上（封版 --後 --试／GitHub 之演）' % (x['id'], x.get('起'))
                  for x in 册.get('法') or [] if 演果.get(x['id'], ('',))[0] == '⛔' and int(x.get('起', 起章)) <= n + 1][:2]
        except Exception as ex:
            项.append('⚠ 执行之守印不出：%s' % str(ex)[:60])
    序 = {t: i for i, t in enumerate(时们)}
    for x in sorted((x for x in 册.get('法') or [] if 当验(x, n)), key=lambda x: (-int(x.get('立', 0)), 序.get(x['时'], 9))):
        标 = '·'
        # 开章零网先验：时 开 之证（⛔报、⛔git）；时 十（段首方验·上段之审与随段）之证亦先验（⛔报；git 只许 改＝本机之史）——
        #   复核补·丝滑：拍库随段、诸册随段、大审瘦式於段首之开即见 ⛔，⛔候本章钱花完、封版 --後 方红
        if e and x['时'] in ('开', '十') and not any(('报' in c or ('git' in c and not (x['时'] == '十' and c.get('git') == '改')))
                                                   for c in x.get('证') or []):
            标 = {'✓': '✓', '⛔': '⛔'}.get(验法(x, e)[0], '·')
        坐证 = [c for c in x.get('证') or [] if isinstance(c, dict) and c.get('git') == '坐异']
        if e and 坐证:                   # 1027 复核补·丝滑（问题早见早治）：坐异只读本机，开章即判——同坐者封版 --後 必拦，开章即交新会话、⛔候钱花完方红
            态, 语 = 验证(坐证[0], e)
            if 态 == '⛔':
                项.insert(0, '⛔ %s：%s——本章交新会话写（封版 --後 必拦）' % (x['id'], 语[:60]))
                continue
        项.append('%s %s → %s' % (标, x['id'], 填(x.get('示') or '；'.join(_示证(c) for c in x.get('证') or []), n)[:50]))
    项 = [x for x in 项 if x.startswith('⛔')] + [x for x in 项 if not x.startswith('⛔')]     # ⛔ 者先（截行⛔掩其红）
    if len(项) > 9:
        项 = 项[:8] + ['……另 %d 法（--册）' % (len(项) - 8)]
    return 出 + ['  ' + x for x in 项]


def 势(键, root=ROOT, 末=None, 几=5):
    """量之势：末几章之数。"""
    if 末 is None:
        末 = max([int(m) for m in re.findall(r'·第?(\d{3})(?:章|造式)', open(os.path.join(root, '设定', '费账.json'), encoding='utf-8').read())] or [0])
    v = []
    for k in range(末 - 几 + 1, 末 + 1):
        x = 章量(k, root).get(键)
        if x is not None:
            v.append('%d %s' % (k, ('%.0f%%' % (x * 100)) if 键.endswith('占') else ('$%.2f' % x)))
    return '｜'.join(v) or '（无数）'


def 册印(root=ROOT):
    册 = 读册(root)
    红, 黄 = 完备(册, root)
    出 = ['════ 法用册（%s）：法 %d（机证不能 %d）｜待 %d｜缓 %d ════' % (册名, len(册['法']), sum(1 for x in 册['法'] if x.get('机证不能')),
                                                         len(册.get('待') or []), len(册.get('缓') or []))]
    for x in 册['法']:
        出.append('· %s【%s·起%s·立%s】%s｜据 %s' % (x['id'], x['时'], x['起'], x.get('立', '?'), x['名'][:30], x['据'][:40]))
        if x.get('机证不能'):
            出.append('    机证不能：%s' % x['由'][:80])
        for c in x.get('证') or []:
            出.append('    证：%s' % _示证(c)[:90])
        for k in x.get('量') or []:
            出.append('    量·%s：%s' % (k, 势(k, root)))
    for x in 册.get('待') or []:
        出.append('· 待·%s【限 %d】%s｜据 %s' % (x['id'], x['限'], x['名'][:30], x['据'][:40]))
    for x in 册.get('废') or []:
        出.append('· 废·%s【废於 %s·在 %s%s】%s｜去证 %d 条' % (x['id'], x.get('废于'), str(x.get('在'))[:8],
                                                    '·待合 %s 限 %s' % (x['待合'], x.get('限')) if x.get('待合') else '', x['名'][:30], len(x.get('去证') or [])))
    出 += 红 + 黄
    出.append('%s 完备：总章§八 %d 条、方法账 %s 起 %d 行俱有据' % ('✓' if not 红 else '⛔', len(总章之八(root)), 立日, len(法账之新行(root))) if not 红 else '⛔ 完备未过 %d 处' % len(红))
    return 出


def 末封(root=ROOT):
    rc, o = _git(root, 'log', '-1', '--format=%s', '-E', '--grep=（造式二代·封版#[0-9]+）', 'HEAD')
    m = re.search(r'封版#(\d+)', o or '')
    return int(m.group(1)) if m else 0


def 未行(root=ROOT, 册=None, 完红=None, 逾数=None, 废红数=None):
    """未行之数（1027 #36·同功两处即废劣者：五本「已定之事有无机器守」之账合印一数）→ (数｜None, [(名, 数｜None)])。
    进化链无守（进化链.诸环）＋裁未生效（裁之生效.查）＋坑已治未守（方法坑账）＋令无证（作者常令之完备）＋待逾限＋废而未除
    ＋复核未行（总编辑复核之甲）。一分算不得即数作 None（只报⚠、⛔判棘轮）。"""
    册 = 册 or 读册(root)
    分 = []

    def 取(名, f):
        try:
            分.append((名, int(f())))
        except Exception:
            分.append((名, None))

    def _链():
        import 进化链
        return sum(1 for x in 进化链.诸环() if not x.get('守') and not x.get('汰') and not x.get('史'))   # 史（线 D：史·无须守）⛔计——与 进化链 之「无守」同尺

    def _裁():
        import 裁之生效
        return len(裁之生效.查())

    def _坑():
        import 方法坑账
        return sum(1 for x in 方法坑账.读(root).get('坑') or [] if x.get('状') == '已治未守')

    def _令():
        红 = 完红 if 完红 is not None else 完备(册, root)[0]
        return sum(1 for x in 红 if re.match(r'⛔ (令立无证|令落之档不在|令引之法不在册)', x))

    def _待():
        if 逾数 is not None:
            return 逾数
        末 = 末封(root)
        e = 境(末 or 起章, root, 取=False, 承=False)
        return sum(1 for x in 册.get('待') or [] if 末 and 末 >= x['限'] and 验法(x, e)[0] == '⛔' and not 缓之(册, x['id'], 末))

    def _废():
        return 废红数 if 废红数 is not None else len(验废(册, 盘(root), 末封(root) or None)[0])

    def _复():
        import 总编辑复核
        return sum(1 for x in 总编辑复核.查(印=False)[1] if str(x).startswith('甲'))
    for 名, f in (('进化链无守', _链), ('裁未生效', _裁), ('坑已治未守', _坑), ('令无证', _令), ('待逾限', _待),
                 ('废而未除', _废), ('复核未行', _复)):
        取(名, f)
    数 = None if any(v is None for _, v in 分) else sum(v for _, v in 分)
    return 数, 分


def 未行之判(数, 册):
    """棘轮（唯一处：册之「未行」「底」）：数 ＞ 底 即 ⛔；数 ＜ 底 报可降；算不得即 ⚠。→ (态, 语)。"""
    底 = (册.get('未行') or {}).get('底')
    if 数 is None:
        return '⚠', '未行之数算不得（某分之器读不得）——棘轮⛔判'
    if not isinstance(底, int):
        return '⛔', '册无「未行」之底（棘轮未立）'
    if 数 > 底:
        return '⛔', '未行之数 %d ＞ 底 %d——只许降：新添之决、法、坑须同回配器配证' % (数, 底)
    if 数 < 底:
        return '✓', '未行之数 %d ＜ 底 %d——可降：python3 工具/法用之守.py --未行 --降' % (数, 底)
    return '✓', '未行之数 %d ＝ 底 %d' % (数, 底)


def 未行之印(数, 分, 册):
    态, 语 = 未行之判(数, 册)
    return '%s 未行之数 %s（%s）｜%s' % (态, '?' if 数 is None else 数, '＋'.join('%s %s' % (k, '?' if v is None else v) for k, v in 分), 语)


def 降底(root=ROOT):
    """今之未行之数 ＜ 底 即降其底（册之文就地改一数、⛔重排其式）→ rc。"""
    册 = 读册(root)
    数, 分 = 未行(root, 册)
    态, 语 = 未行之判(数, 册)
    print(未行之印(数, 分, 册))
    底 = (册.get('未行') or {}).get('底')
    if 数 is None or not isinstance(底, int) or 数 >= 底:
        print('· 未降（%s）' % ('算不得' if 数 is None else '无底' if not isinstance(底, int) else '今 %d ≥ 底 %d' % (数, 底)))
        return 0 if 态 != '⛔' else 1
    p = os.path.join(root, 册名)
    s = _改底(open(p, encoding='utf-8').read(), 底, 数, time.strftime('%m%d', time.gmtime()))
    if s is None:
        print('⛔ 册之「未行」之形不识，⛔改')
        return 1
    open(p, 'w', encoding='utf-8').write(s)
    print('✓ 未行之底降：%d → %d' % (底, 数))
    return 0


def _改底(s, 底, 数, 日):
    """册之文 → 改「未行」之底为 数、记首添「日 底→数」之新文（⛔重排其式；只许降）；形不识或 数 ≥ 底 即 None。"""
    m = re.search(r'("未行":\s*\{\s*"底":\s*)(\d+)(,\s*"记":\s*\[)', s)
    if not m or int(m.group(2)) != 底 or 数 >= 底:
        return None
    记 = json.dumps('%s %d→%d' % (日, 底, 数), ensure_ascii=False)
    s = s[:m.start(2)] + str(数) + m.group(3) + 记 + (', ' if not re.match(r'\s*\]', s[m.end():]) else '') + s[m.end():]
    try:
        d = json.loads(s)
    except ValueError:
        return None
    return s if d.get('未行', {}).get('底') == 数 else None


def 报首(root=ROOT):
    """会话开头之钩印之一行（⛔析写者、⛔演：约一秒）：完备、待逾限、废而未除、未行之数（与底）。"""
    try:
        册 = 读册(root)
        红, _ = 完备(册, root)
        末 = 末封(root)
        e = 境(末 or 起章, root, 取=False, 承=False)
        逾 = [x['id'] for x in 册.get('待') or [] if 末 and 末 >= x['限'] and 验法(x, e)[0] == '⛔' and not 缓之(册, x['id'], 末)]
        废红, 废黄 = 验废(册, e.盘, 末 or None)
        数, 分 = 未行(root, 册, 完红=红, 逾数=len(逾), 废红数=len(废红))
        态, 语 = 未行之判(数, 册)
        ok = not 红 and not 逾 and not 废红 and 态 != '⛔'
        return '%s 法用之守（已封至 %d）：法 %d·待 %d｜完备 %s｜待逾限 %d｜废而未除 %d（待合 %d）｜未行之数 %s（底 %s）%s' % (
            '✓' if ok else '⛔', 末, len(册.get('法') or []), len(册.get('待') or []), '✓' if not 红 else '⛔%d' % len(红), len(逾),
            len(废红), len(废黄), '?' if 数 is None else 数, (册.get('未行') or {}).get('底'),
            '' if ok else '——详 python3 工具/法用之守.py --报')
    except Exception as ex:
        return '⚠ 法用之守·首印不出：%s' % str(ex)[:80]


def 报(root=ROOT):
    """全测之格：完备、册之形、逾限之待（末封之章 ≥ 限而无证）；执行之守·丝滑之守之状（废、写者、同功、流程之法之演：
    起 ≤ 末封而未演即红、将起而未演只报⚠）；未行之数（只许降·册「未行」之底）。零网。"""
    册 = 读册(root)
    红, 黄 = 完备(册, root)
    末 = 末封(root)
    逾 = []
    e = 境(末 or 起章, root, 取=False, 承=False)
    if 末:
        for x in 册.get('待') or []:
            if 末 >= x['限'] and 验法(x, e)[0] == '⛔' and not 缓之(册, x['id'], 末):
                逾.append('⛔ 待逾限：%s（限 %d，已封至 %d）' % (x['id'], x['限'], 末))
    执红, 执黄, 演果, 计 = 执之验(册, e, 末 or None, root, 取=False)
    数, 分 = 未行(root, 册, 完红=红, 逾数=len(逾), 废红数=计['废红'])
    行态, _ = 未行之判(数, 册)
    行印 = 未行之印(数, 分, 册)
    演红, 演黄 = [], []
    for x in 册.get('法') or []:
        a, 语 = 演果.get(x['id'], ('免', ''))
        if a == '⛔':
            已 = 末 >= int(x.get('起', 起章))
            (演红 if 已 else 演黄).append('%s 演·%s（起 %s%s）：%s' % ('⛔' if 已 else '⚠', x['id'], x.get('起'), '·已起' if 已 else '·将起', 语[:120]))
    ok = not 红 and not 逾 and not 执红 and not 演红 and 行态 != '⛔'
    令红, 令数 = 常令之验(册, root)
    条数 = len(总章之条(root))
    return ok, 红 + 逾 + 执红 + 演红 + 黄 + 执黄 + 演黄 + [行印] + [
        '%s 法用之守·报：法 %d、待 %d；完备 %s（作者常令 %d 条%s、总章之条 %d 俱有据）；逾限之待 %d｜废 %d（未除 %d·待合 %d）｜写者 推 %d 处·演 %d（写者之红 %d）｜同功两处 %d｜'
        '流程之法 %d（演 %d·演免 %d·未演 %d）｜未行之数 %s（底 %s）（已封至 %d）' % (
            '✓' if ok else '⛔', len(册['法']), len(册.get('待') or []), '✓' if not 红 else '⛔%d' % len(红), 令数,
            '' if not 令红 else '·⛔%d' % len(令红), 条数, len(逾),
            计['废'], 计['废红'], 计['待合'], 计['写'], 计['演'], 计['二写'], 计['同'],
            计['流程'], 计['演过'], 计['演免'], len(演红) + len(演黄), '?' if 数 is None else 数, (册.get('未行') or {}).get('底'), 末)]


# ───────── 回放（以史） ─────────
def 回放(n0, n1, root=ROOT, 册=None):
    """以史回放 n0—n1：盘取第 N 章封版之提交，法取 立 ≤ N 者（⛔看起），跑取其章器之迹，报与枝取第 N+1 章封版之前者。
    并印「推闸交GitHub」之证於章-N（即 --验 N+1 之所验）。→ {N: (诸行, 推之态)}。"""
    册 = 册 or 读册(root)
    出 = {}
    for n in range(n0, n1 + 1):
        版 = 封提交(n, root)
        至 = min(封时(n + 1, root) or 立时, 立时)
        行 = []
        if not 版:
            出[n] = (['？ 第%d章封版之提交寻不着（浅克隆？）' % n], '？')
            continue
        e = 境(n, root, 史版=版, 史至=至, 取=False, 承=False)
        for x in 册['法']:
            if x.get('机证不能') or int(x.get('立', 999)) > n or (x['时'] == '十' and n != 段起(n)):
                continue
            态, 果 = 验法(x, e)
            行.append('%s %s：%s' % (态, x['id'], '；'.join(语 for a, 语 in 果 if a != '✓')[:120] if 态 != '✓' else '✓'))
        推 = next((x for x in 册['法'] if x['id'] == '推闸交GitHub'), None)
        e1 = 境(n + 1, root, 史版=版, 史至=至, 取=False, 承=False)
        推态, 推语 = 验证((推 or {}).get('证', [{}])[0], e1) if 推 else ('？', '册无此法')
        行.append('%s 推闸交GitHub（章-%d·即 --验 %d 之所验）：%s' % (推态, n, n + 1, 推语))
        出[n] = (行, 推态)
    return 出


# ═════════ 执行之守·丝滑之守（1027 作者令：执行主义——定之策须真跑、所废须除尽、同功两处即废劣者；
#           丝滑主义——跑者无错无冲突、问题早见、凡改流程须真料演练方上）═════════
# 其由（坑53）：沙盒推与 GitHub 推同推主枝——封版旧印「下一步 推.py」、推.py 默直推、自进化环 L1 裸推，与 autopush 相撞六章；
#   新法已立而旧路未除（废而未除），一器⛔问「此枝谁写」「此废真除否」「此新流程演过否」。
写者册名 = os.path.join('设定', '写者册.json')
演练账名 = os.path.join('设定', '演练账.json')
去证之键 = ('无档', '无文', '无格', '推报验', '无踪', '无渲')
诸处 = ('沙盒', 'GitHub')
演律之界 = 412          # 立 ≤ 此之流程之法（演练之律 1027 立前已行、或同轮合流将行）方许「演免」；其後者⛔免——须真料之演
演之好 = ('同', '过')
_守之自 = {'工具/法用之守.py', 册名.replace(os.sep, '/'), 写者册名.replace(os.sep, '/')}   # 无文⛔扫守者自身（去证之式即书於此）


# ───────── 一、所废除尽（废而未除即红） ─────────
def 诸格(盘_, 快=False):
    """全测之格表（诸项 之 ('名', chk_x)）→ 名之集；快：去 `if not quick:` 之块（全测 --快 所跑者）。"""
    t = 盘_.读(os.path.join('工具', '全测.py')) or ''
    if 快:
        m = re.search(r'(?ms)^def 诸项\(quick\):\n(.*?)(?=^\S)', t)
        出, 跳 = [], None
        for l in (m.group(1) if m else '').split('\n'):
            缩 = len(l) - len(l.lstrip())
            if 跳 is not None and (not l.strip() or 缩 > 跳):
                continue
            跳 = None
            if re.match(r'\s*if not quick\s*:', l):
                跳 = 缩
                continue
            出.append(l)
        t = '\n'.join(出)
    return set(re.findall(r"\(\s*'([^']+)'\s*,\s*chk_\w+\s*\)", t))


def 读者可见(盘_):
    m = re.search(r'(?ms)^读者可见之闸\s*=\s*\{(.*?)^\}', 盘_.读(os.path.join('工具', '全测.py')) or '')
    return set(re.findall(r"'([^']+)'", re.sub(r'#[^\n]*', '', m.group(1)))) if m else set()


def 验去证(c, 盘_):
    """→ (态, 语)：✓ 已除｜⛔ 尚在（语指其处）。无档：路（glob·目亦算）⛔在｜无文：正则⛔见於 于（glob 们；守者自身免）｜
    无格：全测之格表（于＝快 即只问 --快 之表；于＝读者 即只问读者可见之闸——格可留而⛔入其等）与读者可见之闸⛔列｜
    推报验：推报.验诸（诸 workflow 与 pre-push；盘上须乙形·⑰）之缺⛔有中此正则者｜无踪：git ⛔踪其档（盘上可有·.gitignore）｜
    无渲：造章.js 渲第「章」章（默 411·负测_造章令之桩）之诸令（席：label 之首们；含「果」即并其返值）⛔中此正则。"""
    if '无档' in c:
        诸 = 盘_.在(c['无档'])
        return ('⛔', '%s 尚在%s' % (诸[0], '（等 %d 处）' % len(诸) if len(诸) > 1 else '')) if 诸 else ('✓', '%s 已无' % c['无档'])
    if '无文' in c:
        式, 于 = re.compile(c['无文']), c.get('于') or []
        for p in sorted({p for g in ([于] if isinstance(于, str) else 于) for p in 盘_.有(g)}):
            if p.replace(os.sep, '/') in _守之自:
                continue
            t = 盘_.读(p)
            m = 式.search(t) if t else None
            if m:
                return '⛔', '%s:%d 犯「%s」' % (p, t.count('\n', 0, m.start()) + 1, m.group(0).strip()[:40])
        return '✓', '「%s」已无' % c['无文'][:30]
    if '无踪' in c:
        诸 = 盘_.踪(c['无踪'])
        return ('⛔', '%s 仍为 git 所踪' % 诸[0]) if 诸 else ('✓', '%s 已⛔踪' % c['无踪'])
    if '无渲' in c:
        return _验渲(c, 盘_)
    if '无格' in c and c.get('于') == '读者':
        return ('⛔', '读者可见之闸仍列「%s」' % c['无格']) if c['无格'] in 读者可见(盘_) else ('✓', '「%s」已出读者可见之闸' % c['无格'])
    if '无格' in c:
        快 = c.get('于') == '快'
        if c['无格'] in 诸格(盘_, 快):
            return '⛔', '全测%s之格表仍有「%s」' % ('·快' if 快 else '', c['无格'])
        if not 快 and c['无格'] in 读者可见(盘_):
            return '⛔', '读者可见之闸仍列「%s」' % c['无格']
        return '✓', '格「%s」已无' % c['无格']
    if '推报验' in c:
        yml, 钩 = 盘_.读(os.path.join('.github', 'workflows', 'autopush.yml')), 盘_.读(os.path.join('工具', 'githooks', 'pre-push'))
        if yml is None or 钩 is None:
            return '⛔', 'autopush.yml 或 pre-push 读不得'
        import 推报, inspect
        他 = {os.path.basename(p): 盘_.读(p) or '' for p in 盘_.有('.github/workflows/*.yml')}   # 诸流俱交（闸分於 gate.yml 者⛔只验 autopush 而空绿）
        他['autopush.yml'] = yml
        缺 = [x for x in (推报.验诸(他, 钩) if hasattr(推报, '验诸') else 推报.验(yml, 钩, 他) if len(inspect.signature(推报.验).parameters) > 2
                          else 推报.验(yml, 钩)) if re.match(c['推报验'], x)]
        return ('⛔', '推报.验：' + '；'.join(缺)[:120]) if 缺 else ('✓', '推报.验 无「%s」之缺' % c['推报验'])
    return '⛔', '去证之式不识：%s' % '、'.join(c)


def _验渲(c, 盘_):
    """无渲：盘上之 造章.js 以 负测_造章令 之桩渲第 n 章（诸席之交以假代之、只收令）——⛔读 js 之原文（N≤410 之枝照旧留其字）。"""
    n, 式 = int(c.get('章') or 起章), re.compile(c['无渲'])
    键 = ('渲', n)
    if 键 not in 盘_._缓:
        t = 盘_.读(os.path.join('工具', '席', '造章.js'))
        if t is None:
            return '⛔', '工具/席/造章.js 读不得'
        d = tempfile.mkdtemp(prefix='法用渲_')
        try:
            import 负测_造章令 as Z
            js, 器 = os.path.join(d, '造章.js'), os.path.join(d, '渲.js')
            open(js, 'w', encoding='utf-8').write(t)
            open(器, 'w', encoding='utf-8').write(Z._器)
            盘_._缓[键] = Z.渲(器, n, js=js, 果=True)
        except Exception as e:
            return '⛔', '造章.js 渲 %d 不起：%s' % (n, str(e)[:80])
        finally:
            shutil.rmtree(d, ignore_errors=True)
    收, 果 = 盘_._缓[键]
    席 = c.get('席') or []
    文们 = [(x['label'], x['prompt']) for x in 收 if not 席 or any(x['label'].startswith(s) for s in 席)]
    if not 席 or '果' in 席:
        文们.append(('果', json.dumps(果, ensure_ascii=False)))
    for 名, 文 in 文们:
        m = 式.search(文 or '')
        if m:
            return '⛔', '造章.js 渲 %d 之「%s」犯「%s」' % (n, 名, m.group(0)[:40])
    return '✓', '造章.js 渲 %d 无「%s」' % (n, c['无渲'][:30])


def 验废(册, 盘_, n=None):
    """→ (红, 黄)。凡「废」之去证有一尚在即「废而未除」；其废所退之法（法）仍列於册亦然。
    待合（并行之轨·合流方除）：n < 限 只报 ⚠（合流前之枝）；n ≥ 限、或 n=None 即红。"""
    红, 黄 = [], []
    法们 = {x.get('id') for x in 册.get('法') or []}
    for x in 册.get('废') or []:
        未 = [语 for 态, 语 in (验去证(c, 盘_) for c in x.get('去证') or []) if 态 != '✓']
        if x.get('法') in 法们:
            未.append('法用册之「法」仍列 %s' % x['法'])
        if not 未:
            continue
        if x.get('待合') and n is not None and n < int(x.get('限') or 0):
            黄.append('⚠ 待合·%s（%s 之轨·限 %d 封前尽）尚在 %d 处：%s' % (x['id'], x['待合'], x['限'], len(未), 未[0][:80]))
        else:
            红.append('⛔ 废而未除：%s（废於 %s）%d 处：%s' % (x['id'], x.get('废于'), len(未), '；'.join(未)[:220]))
    return 红, 黄


def _有笔(root, 版):
    if _git(root, 'cat-file', '-e', '%s^{commit}' % 版)[0] == 0:
        return True
    if _git(root, 'rev-parse', '--is-shallow-repository')[1].strip() == 'true':
        _git(root, 'fetch', '-q', '--unshallow', 'origin', 限=600)        # 云端浅克隆：补全史一回（同 境）
    return _git(root, 'cat-file', '-e', '%s^{commit}' % 版)[0] == 0


def 验在(册, root=ROOT):
    """去证真验（⛔空跑）：每废之每条去证，於其「在」之笔（废前之树）须红——式写错即永绿而废若已除，此即其回灌。→ (红, 诸行)"""
    红, 行 = [], []
    for x in 册.get('废') or []:
        版 = str(x.get('在') or '')
        if not 版 or not _有笔(root, 版):
            红.append('⛔ 去证无凭：%s 之「在」%s 寻不着' % (x.get('id'), 版 or '（未书）'))
            continue
        盘h = 盘(root, 版)
        空 = [json.dumps(c, ensure_ascii=False)[:60] for c in x.get('去证') or [] if 验去证(c, 盘h)[0] != '⛔']
        if 空:
            红.append('⛔ 去证空验：%s 之 %s 於 %s（废前之树）不红——其式不中其物' % (x['id'], '、'.join(空), 版[:8]))
        行.append('%s %s：去证 %d 条於 %s 俱红%s' % ('⛔' if 空 else '✓', x['id'], len(x.get('去证') or []), 版[:8], '（空 %d）' % len(空) if 空 else ''))
    return 红, 行


# ───────── 二、写者唯一（一族之枝一写者；推.py --直 係唯一之审计之例外） ─────────
_写之档 = ('工具/*.py', '工具/githooks/*', '.github/workflows/*.yml', '.github/workflows/*.yaml', '工具/席/*.js')
_壳调 = {'run', 'Popen', 'call', 'check_call', 'check_output', 'system', 'popen', 'getoutput', 'getstatusoutput'}
_壳断 = {';', '&&', '||', '|', '&', '>', '>>', '<', '<<', '>&', '<&', '(', ')', ';;', '|&', '&>', 'then', 'do', 'else', 'fi', 'done'}
_格式 = r'%[-#0 +]*\d*(?:\.\d+)?[sdirxXfgeEc%]'
_全旗 = ('-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path', '--config-env')      # git 之全局之旗（带值）
_推值旗 = ('-o', '--push-option', '--receive-pack', '--exec', '--repo')                         # push 之带值之旗


def _令位(常, i):
    """argv（常：其字，不定作 None）自 i 越 git 之全局之旗 → 其令之位（不定者作旗而越）。"""
    while i < len(常):
        v = 常[i]
        if v in _全旗:
            i += 2
        elif v is None or v.startswith('-'):
            i += 1
        else:
            return i
    return i


def _限(s, 顶=24):
    return set(sorted(s)[:顶]) if len(s) > 顶 else s


def _填式(fmt, 参们):
    """'%s:refs/heads/%s' % (…) 之填：每 % 之位取其参之诸值（积而至多二十四）。"""
    出, k = [''], 0
    for p in re.split('(%s)' % _格式, fmt):
        if re.fullmatch(_格式, p):
            if p == '%%':
                出 = [x + '%' for x in 出]
                continue
            alts = 参们[k] if k < len(参们) else {'*'}
            k += 1
            出 = [x + a for x in 出 for a in sorted(alts)][:24]
        else:
            出 = [x + p for x in 出]
    return set(出)


def _refspec(v, 删=False):
    """refspec 之值 → (靶, 作)：去 + 与 refs/heads/；「:靶」与 --delete 即删；解不出之段作 *。"""
    v = v[1:] if v.startswith('+') else v
    if ':' in v:
        src, v = v.split(':', 1)
        删 = 删 or src == ''
    v = re.sub(r'^refs/heads/', '', v)
    return (v or '*'), ('删' if 删 else '写')


class _py析:
    """一 py 档里 git push 之调（argv 之列、或交 shell 之串）→ 其靶。随简变量（函内与模级之赋、lambda 承其函之赋）、本档之函之返、
    他器之模（import 之名）之常量与函而解；解不出之段作 *。"""
    def __init__(self, 文, 档, 盘_, 诸模=None):
        self.档, self.盘 = 档, 盘_
        self.诸模 = {} if 诸模 is None else 诸模
        self.树 = ast.parse(文)
        self.模, self.函, self.别 = {}, {}, {}
        for nd in ast.walk(self.树):
            if isinstance(nd, ast.Import):
                for a in nd.names:
                    self.别[a.asname or a.name] = a.name
        for nd in self.树.body:
            if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.函[nd.name] = nd
            elif not isinstance(nd, ast.ClassDef):
                for x in ast.walk(nd):
                    self._记赋(x, self.模)
        self.包 = set()                       # git 之包：函（或 lambda 所赋之名）之体以 ['git', …] + 其参 调之——其调之首令即 git 之令（⛔只凭名）
        名们 = {id(x.value): t.id for x in ast.walk(self.树) if isinstance(x, ast.Assign) and isinstance(x.value, ast.Lambda)
              for t in x.targets if isinstance(t, ast.Name)}
        for nd in ast.walk(self.树):
            if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                a = nd.args
                参 = {p.arg for p in a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]}
                if any(isinstance(x, ast.BinOp) and isinstance(x.op, ast.Add) and self._常((self._平(x) or [None])[:1]) == ['git']
                       and any(isinstance(n, ast.Name) and n.id in 参 for n in ast.walk(x.right)) for x in ast.walk(nd)):
                    self.包.add(名们.get(id(nd)) if isinstance(nd, ast.Lambda) else nd.name)

    def _平(self, e, 域=None, 深=0):
        """列之串接（['git', …] + 某 + […]；变量之唯一赋係列者随之）→ 其诸元（不定之段作 Starred）；无列即 None。"""
        if isinstance(e, (ast.List, ast.Tuple)):
            return list(e.elts)
        if isinstance(e, ast.Name) and 深:
            vs = 域[e.id] if 域 is not None and e.id in 域 else self.模.get(e.id)
            return list(vs[0].elts) if vs and len(vs) == 1 and isinstance(vs[0], (ast.List, ast.Tuple)) else None
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add) and 深 < 6:
            a, b = self._平(e.left, 域, 深 + 1), self._平(e.right, 域, 深 + 1)
            if a is None and b is None:
                return None
            return (a if a is not None else [ast.Starred(value=e.left, ctx=ast.Load())]) + \
                (b if b is not None else [ast.Starred(value=e.right, ctx=ast.Load())])
        return None

    @staticmethod
    def _记赋(x, d):
        if isinstance(x, ast.Assign):
            for t in x.targets:
                if isinstance(t, ast.Name):
                    d.setdefault(t.id, []).append(x.value)
                else:
                    for n in ast.walk(t):
                        if isinstance(n, ast.Name):
                            d.setdefault(n.id, []).append(None)      # 拆包之赋：值不定
        elif isinstance(x, ast.AnnAssign) and isinstance(x.target, ast.Name) and x.value is not None:
            d.setdefault(x.target.id, []).append(x.value)
        elif isinstance(x, ast.NamedExpr):
            d.setdefault(x.target.id, []).append(x.value)
        elif isinstance(x, (ast.AugAssign, ast.For, ast.AsyncFor, ast.comprehension)):
            for n in ast.walk(x.target):
                if isinstance(n, ast.Name):
                    d.setdefault(n.id, []).append(None)
        elif isinstance(x, ast.withitem) and x.optional_vars is not None:
            for n in ast.walk(x.optional_vars):
                if isinstance(n, ast.Name):
                    d.setdefault(n.id, []).append(None)

    def 域(self, fn):
        a = fn.args
        d = {}
        for p in a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]:
            d.setdefault(p.arg, []).append(None)                       # 参：值不定
        for x in ast.walk(fn):
            self._记赋(x, d)
        return d

    def _他(self, m):
        m = self.别.get(m, m)
        p = '工具/%s.py' % m
        if p == self.档:
            return self
        if p not in self.诸模:
            t = self.盘.读(p)
            try:
                self.诸模[p] = _py析(t, p, self.盘, self.诸模) if t else None
            except (SyntaxError, ValueError):
                self.诸模[p] = None
        return self.诸模[p]

    def 值(self, e, 域=None, 深=0):
        """式 → 其诸可能之串（glob：不定之段作 *）。"""
        if 深 > 8 or e is None:
            return {'*'}
        if isinstance(e, ast.Constant):
            return {e.value} if isinstance(e.value, str) else {'*'}
        if isinstance(e, ast.Name):
            vs, 下 = (域[e.id], 域) if 域 is not None and e.id in 域 else (self.模.get(e.id), None)
            return _限(set().union(*[self.值(v, 下, 深 + 1) for v in vs])) if vs else {'*'}
        if isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name):
            他 = self._他(e.value.id)
            return 他.值(ast.Name(id=e.attr, ctx=ast.Load()), None, 深 + 1) if 他 else {'*'}
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Add):
            return _限({a + b for a in self.值(e.left, 域, 深 + 1) for b in self.值(e.right, 域, 深 + 1)})
        if isinstance(e, ast.BinOp) and isinstance(e.op, ast.Mod):
            诸参 = [self.值(x, 域, 深 + 1) for x in (e.right.elts if isinstance(e.right, ast.Tuple) else [e.right])]
            return _限(set().union(*[_填式(f, 诸参) for f in self.值(e.left, 域, 深 + 1)]))
        if isinstance(e, ast.JoinedStr):
            出 = {''}
            for v in e.values:
                p = self.值(v.value if isinstance(v, ast.FormattedValue) else v, 域, 深 + 1)
                出 = _限({a + b for a in 出 for b in p})
            return 出
        if isinstance(e, ast.IfExp):
            return self.值(e.body, 域, 深 + 1) | self.值(e.orelse, 域, 深 + 1)
        if isinstance(e, ast.BoolOp):
            return set().union(*[self.值(v, 域, 深 + 1) for v in e.values])
        if isinstance(e, ast.Call):
            f, 析, fn = e.func, self, None
            if isinstance(f, ast.Name) and f.id in self.函:
                fn = self.函[f.id]
            elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                析 = self._他(f.value.id)
                fn = 析.函.get(f.attr) if 析 else None
            if fn is not None:
                域2 = 析.域(fn)
                rs = [x.value for x in ast.walk(fn) if isinstance(x, ast.Return) and x.value is not None]
                return _限(set().union(*[析.值(r, 域2, 深 + 1) for r in rs])) if rs else {'*'}
        return {'*'}

    def _argv(self, 余, 域):
        远, 删, 靶们, 跳 = False, False, [], False
        for x in 余:
            vs = {'*'} if isinstance(x, ast.Starred) else self.值(x, 域)
            if 跳:                                                      # 带值之旗（-o ci.skip）之值⛔作远端或靶
                跳 = False
                continue
            if vs and all(v.startswith('-') for v in vs):
                删 = 删 or any(v in ('-d', '--delete') for v in vs)
                远 = 远 or any(v.startswith('--repo') for v in vs)
                跳 = any(v in _推值旗 for v in vs)
                continue
            if not 远:
                远 = True                                               # 首个非旗者係远端
                continue
            靶们.append(vs)
        return [_refspec(v, 删) for vs in (靶们 or [{'*'}]) for v in sorted(vs)]

    @staticmethod
    def _常(诸):
        return [x.value if isinstance(x, ast.Constant) and isinstance(x.value, str) else None for x in 诸]

    def _列(self, 诸, 域, 起=None):
        """argv 之列（何处皆算：调之参、或先存於数据而後以变量交 run 者）：'git' [全局之旗] push … → 其靶（push 须係其令·⛔认他令之参）。
        起：git 之包之参（列不带 'git'·其首令即 git 之令）。"""
        常 = self._常(诸)
        if 起 is None:
            if 'git' not in 常:
                return []
            起 = 常.index('git') + 1
        j = _令位(常, 起)
        return self._argv(诸[j + 1:], 域) if j < len(常) and 常[j] == 'push' else []

    def _调(self, nd, 域):
        f = nd.func
        名 = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ''
        他 = self._他(f.value.id) if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) else self
        壳名 = bool(re.search(r'git|^_?g$', 名)) or 名 in (他.包 if 他 else ())
        for a in nd.args if 壳名 else ():      # git 之包（_g(['push', …])、跑(['push', …] + x)）：列不带 'git'
            诸 = self._平(a, 域)
            r = self._列(诸, 域, 0) if 诸 is not None and 'git' not in self._常(诸) else []
            if r:
                return r
        平 = [a for a in nd.args if not isinstance(a, (ast.List, ast.Tuple))]   # 散参之式：_跑('git', 'push', …)、_git(工, 'push', …)
        r = self._列(平, 域, None if 'git' in self._常(平) or not 壳名 else 0)
        if r:
            return r
        if 名 in _壳调 and nd.args:
            return [y for s in self.值(nd.args[0], 域) if re.search(r'\bgit\b[^;|&\n]*\bpush\b', s) for y in _sh之推(s, {}, '')]
        return []

    def 诸推(self):
        """→ [(者, 行, 靶, 作)]。者：顶级之函名（类之方即 类.方）、模级即 <模>。"""
        出 = []
        for top in self.树.body:
            if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
                单 = [(top.name, top, self.域(top))]
            elif isinstance(top, ast.ClassDef):
                单 = [('%s.%s' % (top.name, f.name), f, self.域(f)) for f in top.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
            else:
                单 = [('<模>', top, None)]
            for 者, nd0, 域 in 单:
                内 = set()                   # 串接之内之列（已随其串接之全列而析）⛔复析
                for nd in ast.walk(nd0):
                    if isinstance(nd, ast.Call):
                        出 += [(者, nd.lineno, 靶, 作) for 靶, 作 in self._调(nd, 域)]
                    elif id(nd) in 内:
                        continue
                    elif isinstance(nd, ast.BinOp) and isinstance(nd.op, ast.Add) and self._平(nd, 域) is not None:
                        内 |= {id(x) for x in ast.walk(nd) if x is not nd and isinstance(x, (ast.List, ast.Tuple, ast.BinOp))}
                        出 += [(者, nd.lineno, 靶, 作) for 靶, 作 in self._列(self._平(nd, 域), 域)]
                    elif isinstance(nd, (ast.List, ast.Tuple)):
                        出 += [(者, nd.lineno, 靶, 作) for 靶, 作 in self._列(nd.elts, 域)]
        return 出


def _sh变(名, env, 体, 深):
    if 名 in env:
        return _sh值(env[名], env, 体, 深 + 1)
    赋 = re.findall(r'(?:^|[\s;(])%s=("[^"]*"|\'[^\']*\'|[^\s;)]*)' % re.escape(名), 体 or '')
    if 赋:
        出 = set()
        for v in 赋:
            v = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'' else v
            出 |= {'*'} if ('$(' in v or '`' in v) else _sh值(v, env, 体, 深 + 1)
        return 出
    if re.search(r'\bread\b[^\n;]*\b%s\b' % re.escape(名), 体 or ''):        # while read -r S N … case "$N" in 式) …
        m = re.search(r'case\s+"?\$\{?%s\}?"?\s+in\b(.*?)\besac\b' % re.escape(名), 体, re.S)
        式 = {p for g in re.findall(r'(?:^|;;)\s*\(?([^\s()|;]+(?:\|[^\s()|;]+)*)\)', m.group(1)) for p in g.split('|')} if m else set()
        if 式:
            return 式
    return {'*'}


def _sh数组(名, env, 体, 深):
    出 = set()
    for b in re.findall(r'(?:^|[\s;(])%s\+?=\(([^)]*)\)' % re.escape(名), 体 or ''):
        try:
            ws = shlex.split(b)
        except ValueError:
            ws = b.split()
        for w in ws:
            出 |= _sh值(w, env, 体, 深 + 1)
    return 出 or {'*'}


def _sh值(tok, env, 体, 深=0):
    """shell 之词 → 其诸可能之串：$V／${V} 随 env、体内之赋、read 而 case 之式；${A[@]} 随 A+=(…)；余作 *。"""
    if 深 > 6:
        return {'*'}
    出, pos = {''}, 0
    for m in re.finditer(r'\$\{(\w+)(\[[@*]\])?\}|\$(\w+)', tok):
        字, pos = tok[pos:m.start()], m.end()
        名 = m.group(1) or m.group(3)
        vs = _sh数组(名, env, 体, 深) if m.group(2) else _sh变(名, env, 体, 深)
        出 = _限({a + 字 + v for a in 出 for v in vs})
    return {a + tok[pos:] for a in 出}


def _sh之推(文, env, 体):
    """shell 之文 → [(靶, 作)]：凡 git [-c …] push 之令（止於 ; && || | 与重定向）；首个非旗者係远端，余係 refspec。"""
    出 = []
    for l in re.sub(r'\\\n', ' ', 文).split('\n'):
        s = l.strip()
        if not s or s.startswith('#') or 'push' not in s or not re.search(r'\bgit\b', s):
            continue
        try:
            lx = shlex.shlex(s, posix=True, punctuation_chars=';&|<>()')
            lx.whitespace_split, lx.commenters = True, ''
            toks = list(lx)
        except ValueError:
            toks = s.split()
        i = 0
        while i < len(toks):
            if toks[i] != 'git':
                i += 1
                continue
            j = i + 1
            while j < len(toks) and toks[j] in ('-c', '-C', '--git-dir', '--work-tree', '--namespace'):
                j += 2
            if j >= len(toks) or toks[j] != 'push':
                i = j
                continue
            k, 段 = j + 1, []
            while k < len(toks) and toks[k] not in _壳断 and not (re.fullmatch(r'\d', toks[k]) and k + 1 < len(toks) and toks[k + 1][:1] in '<>'):
                段.append(toks[k])
                k += 1
            远, 删, 靶们, 跳 = False, False, [], False
            for t in 段:
                vs = _sh值(t, env, 体)
                if 跳:
                    跳 = False
                    continue
                if all(v.startswith('-') for v in vs):
                    删 = 删 or any(v in ('-d', '--delete') for v in vs)
                    远 = 远 or any(v.startswith('--repo') for v in vs)
                    跳 = any(v in _推值旗 for v in vs)
                    continue
                if not 远:
                    远 = True
                    continue
                靶们.append(vs)
            出 += [_refspec(v, 删) for vs in (靶们 or [{'*'}]) for v in sorted(vs)]
            i = k
    return 出


def _yml诸步(文):
    """→ [{行, 键: 值}]：steps 下诸 `- ` 之步（行＝其首行）；run: | 之块去缩进。自析——⛔依 推报 之私函（推报改析而此⛔随崩）、⛔依 PyYAML。"""
    L, 出, i = 文.split('\n'), [], 0
    while i < len(L):
        m = re.match(r'^(\s*)steps:\s*(#.*)?$', L[i])
        i += 1
        if not m:
            continue
        基, 当, 键缩 = None, None, None
        while i < len(L):
            l = L[i]
            if not l.strip() or l.lstrip().startswith('#'):
                i += 1
                continue
            缩, 项 = len(l) - len(l.lstrip()), re.match(r'^(\s*)-\s+(\S.*)$', l)
            if 基 is None:
                if not 项 or 缩 < len(m.group(1)):
                    break
                基 = 缩
            if 缩 < 基 or (缩 == 基 and not 项):
                break
            if 缩 == 基:
                当, 键缩, 体 = {'行': i + 1}, 项.start(2), 项.group(2)
                出.append(当)
            elif 缩 == 键缩:
                体 = l.strip()
            else:
                i += 1
                continue
            i += 1
            k = re.match(r'^([\w-]+):\s*(.*)$', 体)
            if not k:
                continue
            v = k.group(2).strip()
            if re.fullmatch(r'[|>][+-]?\d*', v):
                块 = []
                while i < len(L) and (not L[i].strip() or len(L[i]) - len(L[i].lstrip()) > 键缩):
                    块.append(L[i])
                    i += 1
                c = min((len(x) - len(x.lstrip()) for x in 块 if x.strip()), default=0)
                当[k.group(1)] = '\n'.join(x[c:] for x in 块)
            else:
                当[k.group(1)] = v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in '\'"' else v
    return 出


def _yml之写(文):
    m = re.search(r'(?ms)^env:[ \t]*\n(.*?)(?=^\S|\Z)', 文)
    env = dict(re.findall(r'(?m)^  ([A-Z_][A-Z0-9_]*):\s*(\S+)\s*$', m.group(1))) if m else {}
    出 = []
    for s in _yml诸步(文):
        run = s.get('run') or ''
        if 'push' in run:                                       # ${{ env.X }} 先填（GitHub 先於 shell 代之）；余之 ${{ … }} 不定作 *
            run = re.sub(r'\$\{\{[^}]*\}\}', '*', re.sub(r'\$\{\{\s*env\.(\w+)\s*\}\}', lambda x: env.get(x.group(1), '*'), run))
            出 += [(s.get('id') or s.get('name') or '?', s['行'], 靶, 作) for 靶, 作 in _sh之推(run, env, run)]
    return 出


def _js之写(文):
    """席之令里之 git push（席⛔ git 写）：凡未被⛔／禁／勿／不得之句所领者即一写者（靶不明）。"""
    出 = []
    for m in re.finditer(r'\bgit\s+(?:-c\s+\S+\s+)*push\b', 文):
        句 = re.split(r'[。；;！!\n]', 文[max(0, m.start() - 400):m.start()])[-1]
        if not re.search(r'⛔|禁|勿|不得|不许|不准', 句):
            出.append(('*', 文.count('\n', 0, m.start()) + 1, '*', '写'))
    return 出


def 诸写(盘_):
    """→ [{档, 者, 行, 靶, 作}]：工具/*.py、githooks、workflows、席之 js 里凡 git push 之处（静析·⛔跑）。"""
    出, 诸模 = [], {}
    for p in 盘_.含('push', list(_写之档)):
        t, p = 盘_.读(p) or '', p.replace(os.sep, '/')
        if p.endswith('.py'):
            try:
                诸 = _py析(t, p, 盘_, 诸模).诸推()
            except (SyntaxError, ValueError) as e:
                诸 = [('<析不得>', getattr(e, 'lineno', 0) or 0, '*', '写')]
        elif p.endswith(('.yml', '.yaml')):
            诸 = _yml之写(t)
        elif p.endswith('.js'):
            诸 = _js之写(t)
        else:
            诸 = [('*', 0, 靶, 作) for 靶, 作 in _sh之推(t, {}, t)]
        出 += [{'档': p, '者': a, '行': b, '靶': c, '作': d} for a, b, c, d in 诸]
    return 出


def _者名(y):
    f = y.get('函') or y.get('步')
    return '%s%s' % (y.get('档'), (':' + ('／'.join(f) if isinstance(f, list) else str(f))) if f else '')


def _者合(w, y):
    if not isinstance(y, dict) or w['档'] != y.get('档'):
        return False
    if y.get('函'):
        return w['者'] in (y['函'] if isinstance(y['函'], list) else [y['函']])
    return w['者'] == y['步'] if y.get('步') else True


def _族之(靶, 族们):
    """靶（glob）全落某族之式内 → 其族名；否则 None（* 之段⛔配实字）。"""
    for k, v in 族们.items():
        if any(fnmatch.fnmatchcase(靶.replace('*', '\x00'), s) for s in v.get('式') or []):
            return k
    return None


def _调名(nd):
    f = nd.func
    return f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else ''


def _带祖(nd, 祖):
    """→ (节, [(祖, 其所在之域)])：域即祖之 body／orelse 等（判其在 if 之正支抑 else 之支）。"""
    yield nd, 祖
    for 域, v in ast.iter_fields(nd):
        for c in (v if isinstance(v, list) else [v]):
            if isinstance(c, ast.AST):
                yield from _带祖(c, 祖 + [(nd, 域)])


def _旗之支(祖, 参):
    """在某 if 之正支（body）、其判含 参 而⛔带否（not、!=、not in、is not）——else 之支、否之判俱⛔算（默路之掩）。"""
    return any(isinstance(a, ast.If) and 域 == 'body' and 参 in ast.unparse(a.test)
               and not any(isinstance(n, (ast.Not, ast.NotEq, ast.NotIn, ast.IsNot)) for n in ast.walk(a.test)) for a, 域 in 祖)


def _例外之闸(盘_, x, 演):
    """例外之函（推.py 直推）只许於其器 __main__ 之「参」之支下调（及其自递、演之函）——⛔默路调之、⛔他器调之。→ [犯]"""
    犯, fn = [], x['函']
    for p in 盘_.含(fn, ['工具/*.py']):
        try:
            树 = ast.parse(盘_.读(p) or '')
        except (SyntaxError, ValueError):
            continue
        p = p.replace(os.sep, '/')
        for top in 树.body:
            者 = top.name if isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) else '<模>'
            if (p == x['档'] and 者 == fn) or any(_者合({'档': p, '者': 者}, y) for y in 演 if y.get('函')):
                continue
            for nd, 祖 in _带祖(top, []):
                if isinstance(nd, ast.Call) and _调名(nd) == fn and (p != x['档'] or not _旗之支(祖, x['参'])):
                    犯.append('%s:%d（%s）调 %s 而⛔在 %s 之「%s」支下' % (p, nd.lineno, 者, fn, x['档'], x['参']))
    return 犯


def 读写者册(root=ROOT):
    return json.load(open(os.path.join(root, 写者册名), encoding='utf-8'))


def 写者册之形(册w):
    红, 例 = [], 0
    族们 = 册w.get('族') or {}
    for k, v in 族们.items():
        多 = len(str(v.get('多由') or '')) >= 8          # 多写者须书其由（如 备份/报 诸 workflow 之报步俱取而再推、⛔相覆）——主枝⛔多
        if not v.get('式') or not v.get('写') or (len(v['写']) > 1 and not 多) or len(v.get('删') or []) > 1:
            红.append('⛔ 写者册坏：族「%s」须有式、写者恰一（多者须书多由）、删者至多一——写者唯一' % k)
        for y in (v.get('写') or []) + (v.get('删') or []):
            if not isinstance(y, dict) or not y.get('档'):
                红.append('⛔ 写者册坏：族「%s」之写者须书档（与函／步）' % k)
        x = v.get('例外')
        if x:
            例 += 1
            if not (isinstance(x, dict) and x.get('档') and x.get('函') and x.get('参') and len(str(x.get('由') or '')) >= 8):
                红.append('⛔ 写者册坏：族「%s」之例外须 档、函、参（令之旗）、由（≥八字）' % k)
    if 例 > 1:
        红.append('⛔ 写者册坏：例外 %d 处——唯一（推.py --直·审计之兜底）' % 例)
    for y in 册w.get('演') or []:
        if not (isinstance(y, dict) and y.get('档') and y.get('函') and len(str(y.get('由') or '')) >= 4):
            红.append('⛔ 写者册坏：演 %s 须 档、函、由' % json.dumps(y, ensure_ascii=False)[:40])
    return 红


def 验写者(盘_, 册w=None, root=ROOT):
    """→ (红, 诸写)：凡推者须为其族之唯一写者（或审计之例外），否则「二写者」；靶解不出亦红；
    册之写者寻不着其推（空名）亦红；例外之函越其旗而调亦红。演（推临时之裸库之自测）免。"""
    if 册w is None:
        try:
            册w = 读写者册(root)
        except Exception as e:
            return ['⛔ 写者册读不得（%s）：%s' % (写者册名, str(e)[:60])], []
    红 = 写者册之形(册w)
    族们, 演 = 册w.get('族') or {}, 册w.get('演') or []
    诸 = 诸写(盘_)
    for w in 诸:
        if any(_者合(w, y) for y in 演):
            w['族'] = '演'
            continue
        k = w['族'] = _族之(w['靶'], 族们)
        位 = '%s:%s（%s）' % (w['档'], w['行'], w['者'])
        if not k:
            w['红'] = True
            红.append('⛔ 二写者：%s 推「%s」——写者册无此族%s' % (位, w['靶'], '（靶解不出：写明其枝）' if '*' in w['靶'] else ''))
            continue
        v = 族们[k]
        if any(_者合(w, y) for y in v.get(w['作']) or []):
            continue
        x = v.get('例外')
        if x and w['作'] == '写' and _者合(w, x):
            w['例外'] = True
            continue
        w['红'] = True
        红.append('⛔ 二写者：%s %s「%s」——族「%s」之唯一%s者係 %s' % (位, '推' if w['作'] == '写' else '删', w['靶'], k, w['作'],
                                                         '、'.join(_者名(y) for y in v.get(w['作']) or []) or '（无）'))
    for k, v in 族们.items():
        for 作 in ('写', '删'):
            for y in v.get(作) or []:
                if not any(w.get('族') == k and w['作'] == 作 and _者合(w, y) for w in 诸):
                    红.append('⛔ 写者册空名：族「%s」之%s者 %s 寻不着其推——器改名、已废、或步名已易：册随之改' % (k, 作, _者名(y)))
        x = v.get('例外')
        if x:
            if not any(w.get('例外') and w.get('族') == k for w in 诸):
                红.append('⛔ 写者册空名：族「%s」之例外 %s 寻不着其推' % (k, _者名(x)))
            红 += ['⛔ 例外越界：' + s for s in _例外之闸(盘_, x, 演)]
    for y in 演:
        if not any(w.get('族') == '演' and _者合(w, y) for w in 诸):
            红.append('⛔ 写者册空名：演 %s 已无推——册随之删' % _者名(y))
    for 条, 靶 in 预授之推(盘_):          # 1027 #68：settings 之预授亦一写之路（Bash 直推主枝⛔经 推.py --直 之审计）
        if 靶 == '*' or _族之(靶, 族们) == '主枝' or 靶 == 主枝:
            红.append('⛔ 二写者：.claude/settings.json permissions.allow「%s」预授 git push %s——主枝之唯一写者係 autopush'
                     '（推.py --直 之兜底在 python 内、⛔经此预授）：删此条' % (条[:60], '（靶不定·可及主枝）' if 靶 == '*' else 靶))
    return 红, 诸


def 预授之推(盘_):
    """.claude/settings.json 之 permissions.allow 里之「Bash(git … push …)」→ [(条, 靶)]（靶：枝名；无明靶或靶不定即 *）。"""
    try:
        d = json.loads(盘_.读(os.path.join('.claude', 'settings.json')) or '{}')
        诸 = (d.get('permissions') or {}).get('allow') or []
    except Exception:
        return []
    出 = []
    for 条 in 诸:
        m = re.fullmatch(r'\s*Bash\((.*)\)\s*', str(条), re.S)
        if not m:
            continue
        令 = re.sub(r':\*$|\*$', '', m.group(1).strip())
        try:
            词 = shlex.split(令)
        except ValueError:
            词 = 令.split()
        if len(词) < 2 or 词[0] != 'git':
            continue
        i = _令位(词, 1)
        if i >= len(词) or 词[i] != 'push':
            continue
        余 = [x for x in 词[i + 1:] if not x.startswith('-')]
        if 余 and not re.search(r'[:/]', 余[0]):
            余 = 余[1:]                                   # 首一係远端（origin）
        if not 余:
            出.append((条, '*'))
        for x in 余:
            x = x.split(':', 1)[-1].lstrip('+')
            x = re.sub(r'^refs/heads/', '', x)
            出.append((条, x if x and x not in ('HEAD', '@') and not re.search(r'[*$`]', x) else '*'))
    return 出


# ───────── 三、同功之检（同功两处即废劣者） ─────────
def 同功(册):
    """二活法同「功」而异「处」（沙盒｜GitHub）即红——除非其一已入「废」（废之「法」），或二者书「互补」带由。"""
    红 = []
    废法 = {x.get('法') for x in 册.get('废') or [] if x.get('法')}
    补 = {frozenset((x.get('id'), y.get('与'))) for x in 册.get('法') or [] for y in x.get('互补') or [] if isinstance(y, dict)}
    活 = [x for x in 册.get('法') or [] if x.get('id') not in 废法 and x.get('功')]
    for i, a in enumerate(活):
        for b in 活[i + 1:]:
            if a['功'] == b['功'] and a.get('处') != b.get('处') and frozenset((a['id'], b['id'])) not in 补:
                红.append('⛔ 同功两处：%s（%s）与 %s（%s）同功「%s」——劣者入「废」（带去证）、或书「互补」带由' % (
                    a['id'], a.get('处'), b['id'], b.get('处'), a['功']))
    for x in 册.get('废') or []:                 # 已废之劣者（功、处）⛔以新法之名复立
        for a in 活:
            if x.get('功') and a['功'] == x['功'] and a.get('处') == x.get('处'):
                红.append('⛔ 废而复立：%s（%s·%s）即已废之 %s——⛔复立劣者' % (a['id'], a['功'], a.get('处'), x.get('id')))
    return 红


# ───────── 四、演练之证（凡改流程须真料演练方上） ─────────
def 演录(盘_, root=ROOT, 取=True):
    """→ [{源, id, 何, 果, 时, 文}]：设定/演练账.json（封版之演等·沙盒）与 origin 备份/报 之 报/演/*.json（GitHub 之演）。"""
    录 = []
    try:
        d = json.loads(盘_.读(演练账名) or '[]')
        d = (d.get('录') or d.get('演') or []) if isinstance(d, dict) else d
    except Exception:
        d = []
    for r in d if isinstance(d, list) else []:
        if isinstance(r, dict):
            果 = r.get('果')
            if 果 not in 演之好 and str(r.get('结', '')).startswith('唯後治之异') and (r.get('判') or {}).get('演') == '过':
                果 = '同'           # 唯後治之异（1027 A2）：副本之异尽与封後真仓所落之治逐字同、诸闸之判同（过）——今之序於封时即治其旧红，即同
            录.append({'源': '账', 'id': str(r.get('id', '')), '何': str(r.get('何', '')), '果': 果, '时': _秒(r.get('时')),
                       '文': json.dumps(r, ensure_ascii=False)})
    try:
        import 推报
        for r in 推报.诸报(root, 取=取, 类=('演', '推')):
            # 报/推 亦入（1027 丝滑）：GitHub 真推之闸（与演练同一 gate.yml、同一候之树、过即并）係演之上位——果 成／已在 而带「片」者即真料之演
            录.append({'源': '报', 'id': r.get('路', ''), '何': str(r.get('何', '')), '果': r.get('果'), '时': _秒(r.get('时')),
                       '文': json.dumps(r, ensure_ascii=False), '推': r.get('类') == '推'})
    except Exception:
        pass
    return 录


def 验演(x, 录, 界=None):
    """流程之法（流程:true）须有一演之录：中其「演」之源（账：id／何之正则｜报：报/演/<glob> 或 报/推/<glob>，含：其文之正则），
    果 ∈ 同／过（报/推 之真推：成／已在），
    且时 ≤ 界（其起章封版之时；未封即今有即可）。演免（演练之律前已行·立 ≤ 演律之界）即免。→ (态, 语)"""
    if not x.get('流程'):
        return '免', '非流程之法'
    if x.get('演免'):
        return '免', '演免：%s' % str(x['演免'])[:40]
    见 = []
    for s in x.get('演') or []:
        for r in 录:
            if '账' in s and r['源'] == '账' and re.search(s['账'], r['id'] + '\n' + r['何']):
                pass
            elif '报' in s and r['源'] == '报' and fnmatch.fnmatchcase(r['id'], '报/' + s['报'] + ('' if s['报'].endswith('.json') else '.json')) \
                    and (not s.get('含') or re.search(s['含'], r['文'])):
                pass
            else:
                continue
            if r['果'] in (果默 if r.get('推') else 演之好) and (界 is None or (r['时'] or 0) <= 界):
                return '✓', '演 %s 果「%s」（%s）' % (r['id'][:40], r['果'], _iso(r['时'])[5:16] if r['时'] else '?')
            见.append('%s 果「%s」%s' % (r['id'][:30], r['果'], '·晚於其起（%s）' % _iso(界)[5:16] if 界 and (r['时'] or 0) > 界 else ''))
    return '⛔', '未演（流程之法须真料演练方上）%s' % (('：所见 ' + '；'.join(见[:2])) if 见 else '：演练账与 报/演 俱无其录')


# ───────── 五、报之读（自走之首·问题早见） ─────────
def 未消之坏(诸, 在主=lambda s: False):
    """报/推 之 红／拒／败：同枝後有成、或其 sha 已入主枝、或係治枝而其後有成 → 已消；报/演 之果非 同／过／成 → 坏，
    同所演之枝（ref，无即名）其後有 同／过 之演 → 已消（治而再演，⛔永印旧坏）。新者在前。"""
    推 = [d for d in 诸 if d.get('类') == '推']
    出 = []
    for d in 推:
        if d.get('果') not in ('红', '拒', '败', '坏'):
            continue
        t = str(d.get('时') or '')
        後成 = [y for y in 推 if y is not d and y.get('果') in 果默 and str(y.get('时') or '') > t]
        if any(y.get('ref') == d.get('ref') for y in 後成) or (d.get('sha') and 在主(d['sha'])) \
                or (str(d.get('ref', '')).startswith('治-') and 後成):
            continue
        出.append(d)
    演 = [d for d in 诸 if d.get('类') == '演']
    键 = lambda d: d.get('ref') or d.get('名')
    出 += [d for d in 演 if d.get('果') not in 演之好 + 果默 and not (键(d) and any(
        y is not d and y.get('果') in 演之好 + 果默 and 键(y) == 键(d) and str(y.get('时') or '') > str(d.get('时') or '') for y in 演))]
    return sorted(出, key=lambda d: str(d.get('时') or ''), reverse=True)


def 报之读(root=ROOT, 取=True, 顶=3, 诸=None):
    """自走之首（零 token·一取）：云端 备份/报 之 报/推、报/演 里未消之 红／拒／败（後之成、或其 sha 已入主枝者即消）→ ≤顶 行（行首 ⛔）。"""
    try:
        if 诸 is None:
            import 推报
            诸 = 推报.诸报(root, 取=取, 类=('推', '演'), 并=(主枝,))
    except Exception as e:
        return ['⚠ 报之读不得：%s' % str(e)[:80]]
    if 取 and _git(root, 'rev-parse', '--is-shallow-repository')[1].strip() == 'true':
        _git(root, 'fetch', '-q', '--deepen=300', 'origin', 主枝, 限=120)   # 浅克隆：旧 sha 不可证入主→误印已消之红（1107 查得）
    坏 = 未消之坏(诸, lambda s: bool(re.fullmatch(r'[0-9a-f]{7,40}', str(s)))
                  and _git(root, 'merge-base', '--is-ancestor', s, 'refs/remotes/origin/%s' % 主枝)[0] == 0)
    行 = []
    for d in 坏:
        枝 = d.get('ref') or os.path.basename(str(d.get('路', '')))[:-5]
        红 = str((d.get('红') or [''])[0])
        if d.get('类') == '演':
            行.append('⛔ 报·演 %s 果「%s」（%s）未消：%s' % (枝, d.get('果'), str(d.get('时', ''))[5:16], (红 or d.get('何') or '')[:60]))
            continue
        治 = {'拒': '兜底 python3 工具/推.py --直', '红': '逐红治、提交、python3 工具/推.py（治-*）'}.get(d.get('果'), '看 run_url；GitHub 停摆即 推.py --直')
        行.append('⛔ 报·推 %s 果「%s」（%s）未消%s → %s（详：python3 工具/推报.py --读 %s）' % (
            枝, d.get('果'), str(d.get('时', ''))[5:16], ('：' + 红[:48]) if 红 else '', 治, 枝))
    if len(行) > 顶:
        行 = 行[:顶 - 1] + ['⛔ ……另 %d 坏报未消（全：python3 工具/法用之守.py --报读）' % (len(行) - 顶 + 1)]
    return 行


# ───────── 自测 ─────────
def _写档(根, 档们):
    for p, s in 档们.items():
        f = os.path.join(根, p)
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w', encoding='utf-8').write(s)


def 自测_执(T, 全):
    """执行之守·丝滑之守之自测（⑧废 ⑨写者 ⑩同功 ⑪演 ⑫报之读）：各带真伪两局与回灌——⛔空跑。"""
    import tempfile, shutil
    册 = 读册(ROOT)
    # ⑧所废除尽
    在红, 在行 = 验在(册)
    T('⑧去证真验：册之每废（%d）之每条去证於其「在」之笔（废前之树）俱红——⛔空验%s' % (len(册.get('废') or []), ('：' + 在红[0][:70]) if 在红 else ''),
      册.get('废') and not 在红 and len(在行) == len(册['废']))
    红410, 黄410 = 验废(册, 盘(ROOT), 410)
    红411, _ = 验废(册, 盘(ROOT), 411)
    T('⑧之二 今之树：已行之废（沙盒直推主枝、autopush 二跑闸）俱尽；待合者限前（410）只报⚠、至限（411）即红（⛔悄悄过限）',
      not 红410 and len(红411) == len(黄410) and any(x['id'] == '沙盒直推主枝' and not x.get('待合') for x in 册['废']))
    空 = dict(册, 废=[{'id': '空', '名': '空', '据': 'x', '废于': '1027', '在': '540c1c91', '去证': [{'无文': '永不见之字·甲乙', '于': ['工具/封版.py']}]}])
    T('⑧之三 回灌：去证之式写错（废前之树亦不中）→「去证空验」红', any('去证空验：空' in x for x in 验在(空)[0]))
    t = tempfile.mkdtemp(prefix='法用废_')
    try:
        _写档(t, {'工具/旧.py': 'def 旧之函():\n    pass\n', '工具/法用之守.py': 'def 旧之函(): 守者自身⛔扫\n', '版本/_库/R1/a': 'x',
                  '工具/全测.py': "def 诸项(quick):\n    items = [('甲', chk_a)]\n    if not quick:\n        items.append(('乙', chk_b))\n"
                                "    items.append(('戊', chk_e))\n    return items\n\n\n读者可见之闸 = {\n    '丙',   # 注'丁'\n}\n"})
        p = 盘(t)
        V = lambda c: 验去证(c, p)[0]
        T('⑧之四 无档（档与目）、无文（守者自身免）、无格（全表·快表·读者可见之闸）之真伪', V({'无档': '工具/旧.py'}) == '⛔' and V({'无档': '版本/_库'}) == '⛔'
          and V({'无档': '工具/新.py'}) == '✓' and V({'无文': r'def 旧之函\b', '于': ['工具/*.py']}) == '⛔'
          and V({'无文': r'def 新之函\b', '于': ['工具/*.py']}) == '✓' and 验去证({'无文': r'def 旧之函\b', '于': ['工具/*.py']}, p)[1].startswith('工具/旧.py:1')
          and V({'无格': '甲'}) == '⛔' and V({'无格': '乙'}) == '⛔' and V({'无格': '乙', '于': '快'}) == '✓' and V({'无格': '甲', '于': '快'}) == '⛔'
          and V({'无格': '戊', '于': '快'}) == '⛔' and V({'无格': '丙'}) == '⛔' and V({'无格': '丁'}) == '✓')
        旧yml = subprocess.run(['git', 'show', '540c1c91:.github/workflows/autopush.yml'], cwd=ROOT, capture_output=True, text=True).stdout
        钩 = open(os.path.join(ROOT, '工具', 'githooks', 'pre-push'), encoding='utf-8').read()
        _写档(t, {'.github/workflows/autopush.yml': 旧yml, '工具/githooks/pre-push': 钩})
        旧态 = 验去证({'推报验': '^[③④]'}, 盘(t))[0]
        _写档(t, {'.github/workflows/autopush.yml': open(os.path.join(ROOT, '.github', 'workflows', 'autopush.yml'), encoding='utf-8').read()})
        T('⑧之五 推报验（复用 推报.验）：旧 yml（一树二跑闸）⛔、今 yml ✓', bool(旧yml) and 旧态 == '⛔' and 验去证({'推报验': '^[③④]'}, 盘(t))[0] == '✓')
        import 推报 as _推
        _旧验 = _推.验
        try:   # 闸分於 gate.yml（推报.验 受 他＝诸流）：⛔只交 autopush 而空绿
            _推.验 = lambda yml, 钩, 他=None: ['③一闸：gate 直跑 pre-push'] if 'githooks/pre-push' in (他 or {}).get('gate.yml', '') else []
            _写档(t, {'.github/workflows/gate.yml': 'jobs:\n  g:\n    steps:\n      - run: bash 工具/githooks/pre-push\n'})
            分红 = 验去证({'推报验': '^[③④]'}, 盘(t))[0]
            _写档(t, {'.github/workflows/gate.yml': 'jobs:\n  g:\n    steps:\n      - run: python3 工具/全测.py --片 1/3\n'})
            分绿 = 验去证({'推报验': '^[③④]'}, 盘(t))[0]
        finally:
            _推.验 = _旧验
        T('⑧之八 推报验 诸流俱交（推报.验 受 他 者）：gate.yml 直跑 pre-push → ⛔、无 → ✓（⛔只验 autopush.yml 而空绿）', 分红 == '⛔' and 分绿 == '✓')
        # ⑧之九（1027 合流）：无踪（盘上可有、git ⛔踪）、无格之于读者（格留而⛔入读者可见之闸）、推报验之⑰（甲形静验虽合、盘上⛔许）、无渲（渲而⛔读原文）
        g = os.path.join(t, '踪')
        _写档(g, {'设定/x.log': 'a\n', '工具/全测.py': "def 诸项(quick):\n    items = [('甲', chk_a), ('乙', chk_b)]\n    return items\n\n\n读者可见之闸 = {\n    '甲',\n}\n"})
        _e = dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, GIT_CONFIG_GLOBAL=os.devnull)
        subprocess.run(['git', 'init', '-q', g], capture_output=True, env=_e)
        踪前 = 验去证({'无踪': '设定/x.log'}, 盘(g))[0]
        subprocess.run(['git', 'add', '设定/x.log'], cwd=g, capture_output=True, env=_e)
        踪後 = 验去证({'无踪': '设定/x.log'}, 盘(g))[0]
        读们 = [验去证({'无格': k, '于': '读者'}, 盘(g))[0] for k in ('甲', '乙')]
        七 = [验去证({'推报验': '^⑰'}, 盘(ROOT, v))[0] for v in (_推.单闸yml之笔, None)] if hasattr(_推, '验诸') else []
        渲 = [验去证(dict({'无渲': '冷轮补执', '席': ['记席']}, **k), 盘(ROOT, v))[0] for k, v in (({}, None), ({'章': 410}, None), ({}, '97286329'))]
        T('⑧之九 无踪（未踪 ✓、add 即 ⛔）、无格于读者（列 ⛔、格在而未列 ✓）、推报验⑰（97286329 之甲形 ⛔、今 ✓）、无渲（411 ✓、410 之枝照旧 ⛔、97286329 之 411 ⛔）%s'
          % ('' if 渲 == ['✓', '⛔', '⛔'] else '：渲 %s' % 渲), 踪前 == '✓' and 踪後 == '⛔' and 读们 == ['⛔', '✓'] and 七 == ['⛔', '✓']
          and 渲 == ['✓', '⛔', '⛔'])
        # ⑪之五（1027 合流）：封版之演「唯後治之异」（异尽与封後之治逐字同、诸闸之判同过）即同；未解之异⛔
        _写档(g, {演练账名: json.dumps([{'id': '封版後演·9·甲', '何': 'x', '果': '异', '结': '唯後治之异：a 异於封版之提交而与其後之治逐字同', '判': {'演': '过'}, '时': '2026-10-27T06:58:04Z'},
                                     {'id': '他演·9·乙', '何': 'x', '果': '异', '结': '未解之异：b', '判': {'演': '过'}, '时': '2026-10-27T06:58:04Z'}], ensure_ascii=False)})
        _录 = 演录(盘(g), g, 取=False)
        T('⑪之五 演练账「唯後治之异」（诸闸之判过）即同 → ✓；「未解之异」⛔', 验演({'流程': True, '演': [{'账': '^封版後演·'}]}, _录)[0] == '✓'
          and 验演({'流程': True, '演': [{'账': '^他演·'}]}, _录)[0] == '⛔')
        假 = {'法': [全({'id': '甲', '名': '甲', '据': 'x', '起': 9, '时': '开', '证': [{'档': 'a'}]})], '待': [],
              '废': [{'id': '废甲', '名': 'x', '据': 'x', '废于': '1027', '在': '540c1c91', '法': '甲', '去证': [{'无档': '工具/新.py'}]},
                    {'id': '废乙', '名': 'x', '据': 'x', '废于': '1027', '在': '540c1c91', '待合': 'A1', '限': 11, '去证': [{'无档': '工具/旧.py'}]}]}
        红a, 黄a = 验废(假, p, 10)
        红b, _ = 验废(假, p, 11)
        T('⑧之六 废所退之法仍列於册 → 废而未除；待合限前 ⚠、至限 ⛔', any('废甲' in x and '仍列 甲' in x for x in 红a)
          and any('废乙' in x for x in 黄a) and not any('废乙' in x for x in 红a) and any('废乙' in x for x in 红b))
        坏 = {'法': [], '待': [], '废': [{'id': '坏一', '名': 'x', '据': 'x', '废于': '1027', '去证': [{'无档': 'a'}]},
                                     {'id': '坏二', '名': 'x', '据': 'x', '废于': '1027', '在': 'abcdef1', '去证': [{'无档': 'a', '无格': 'b'}]},
                                     {'id': '坏三', '名': 'x', '据': 'x', '废于': '1027', '在': 'abcdef1', '待合': 'A2', '去证': [{'无文': '('}]}]}
        红c = 完备(坏, t)[0]
        T('⑧之七 册坏：废缺「在」、去证二式并书、待合无限、无文缺于', any('坏一' in x and '在' in x for x in 红c) and any('坏二' in x and '去证不识' in x for x in 红c)
          and any('坏三' in x and '无限' in x for x in 红c) and any('坏三' in x and '去证不识' in x for x in 红c))
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑨写者唯一
    红w, 诸w = 验写者(盘(ROOT))
    T('⑨今之树：诸推之处俱为其族之唯一写者（或审计之例外、或演）%s' % (('：' + 红w[0][:80]) if 红w else ''), not 红w
      and any(w['档'] == '.github/workflows/autopush.yml' and w['族'] == '主枝' for w in 诸w)
      and any(w['档'] == '工具/推.py' and w['者'] == '直推' and w.get('例外') for w in 诸w)
      and any(w['档'] == '工具/存底.py' and w['者'] == '标' and w['族'] == '章标' for w in 诸w))
    红旧, _ = 验写者(盘(ROOT, '540c1c91'), 读写者册())
    T('⑨之二 回灌 540c1c91（推.py 默直推主枝、自进化环 L1 裸推主枝，与 autopush 同推）→ 二写者红',
      any('工具/推.py' in x and '（推）' in x and '二写者' in x and '主枝' in x for x in 红旧)
      and any('工具/自进化环.py' in x and '二写者' in x for x in 红旧))
    t = tempfile.mkdtemp(prefix='法用写_')
    try:
        主 = 'claude/the-novel-review-4dtuit'
        甲 = ("import subprocess\n主 = '%s'\n\n\ndef 名(n):\n    return '章-%%d' %% n\n\n\ndef 推一(n):\n    靶 = 名(n)\n"
             "    subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/' + 靶])\n\n\ndef 推二():\n"
             "    subprocess.Popen('git push -u origin %%s > x 2>&1' %% 主, shell=True)\n\n\ndef 推三(x):\n"
             "    subprocess.run(['git', 'push', 'origin', x])\n\n\ndef 推四(sha):\n"
             "    f = lambda 名: subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/' + 名])\n    名 = '治-' + sha[:12]\n    return f(名)\n\n\n"
             "def 直推():\n    subprocess.run(['git', 'push', 'origin', 主])\n\n\ndef 自测():\n"
             "    for a in ((['git', 'push', 'origin', 'HEAD:refs/heads/' + 主], 1),):\n        subprocess.run(a[0])\n\n\n"
             "if __name__ == '__main__':\n    import sys\n    if sys.argv[1:] == ['--直']:\n        直推()\n    直推()\n") % 主
        yml = ("name: w\non:\n  push:\n    branches: ['章-*']\nenv:\n  MAIN: %s\njobs:\n  a:\n    steps:\n"
               "      - name: 推\n        id: adv\n        run: |\n          git push origin \"HEAD:refs/heads/$MAIN\" > o 2>&1; rc=$?\n"
               "      - name: 删\n        run: |\n          D=()\n          while read -r S N; do\n"
               "            case \"$N\" in refs/heads/治-*) D+=(\":$N\") ;; esac\n          done < <(git ls-remote origin 'refs/heads/治-*')\n"
               "          if [ ${#D[@]} -gt 0 ]; then git -c core.hooksPath=x push -q origin \"${D[@]}\" || echo 败; fi\n") % 主
        js = "const 令 = `⛔ git push（提交归封版）`;\nconst 坏 = `跑 git push origin x`;\n"
        _写档(t, {'工具/甲.py': 甲, '.github/workflows/w.yml': yml, '工具/席/x.js': js})
        册w = {'族': {'主枝': {'式': [主], '写': [{'档': '.github/workflows/w.yml', '步': 'adv'}],
                             '例外': {'档': '工具/甲.py', '函': '直推', '参': '--直', '由': '兜底之审计之例外（试）'}},
                    '章标': {'式': ['章-*'], '写': [{'档': '工具/甲.py', '函': '推一'}]},
                    '治枝': {'式': ['治-*'], '写': [{'档': '工具/甲.py', '函': '推四'}], '删': [{'档': '.github/workflows/w.yml', '步': '删'}]}},
               '演': [{'档': '工具/甲.py', '函': '自测', '由': '临时之库'}]}
        红s, 诸s = 验写者(盘(t), 册w)
        诸k = {(w['者'], w['靶'], w['作']) for w in 诸s}
        T('⑨之三 静析：函之返（章-%d）、shell 之串、lambda 承其函之赋、read 而 case 之数组之删、数据里之 argv（演）俱解其靶',
          {('推一', '章-*', '写'), ('推二', 主, '写'), ('推三', '*', '写'), ('推四', '治-*', '写'), ('直推', 主, '写'), ('自测', 主, '写'),
           ('adv', 主, '写'), ('删', '治-*', '删'), ('*', '*', '写')} <= 诸k)
        T('⑨之四 红：shell 串推主枝（二写者）、靶解不出、席之 js 未⛔之 git push、例外之函越其旗而调；俱合者⛔红',
          any('（推二）' in x and '二写者' in x for x in 红s) and any('（推三）' in x and '靶解不出' in x for x in 红s)
          and any('工具/席/x.js:2' in x for x in 红s) and not any('工具/席/x.js:1' in x for x in 红s)
          and sum('例外越界' in x for x in 红s) == 1 and not any(k in x for x in 红s for k in ('（推一）', '（推四）', '（直推）', '（自测）', '（adv）', '（删）'))
          and len(红s) == 4)
        _写档(t, {'工具/甲.py': 甲.replace("    subprocess.Popen('git push -u origin %s > x 2>&1' % 主, shell=True)\n", '    pass\n')
                   .replace("    subprocess.run(['git', 'push', 'origin', x])\n", '    pass\n').replace('        直推()\n    直推()\n', '        直推()\n'),
                  '工具/席/x.js': "const 令 = `⛔ git push（提交归封版）`;\n"})
        T('⑨之五 治之即绿（同一器、同一册）', 验写者(盘(t), 册w)[0] == [])
        册2 = json.loads(json.dumps(册w))
        册2['族']['主枝']['写'].append({'档': '工具/甲.py', '函': '推二'})
        册2['族']['章标']['例外'] = {'档': '工具/甲.py', '函': '推一', '参': '--甲', '由': '再立一个例外之试'}
        册2['族']['治枝']['删'][0]['步'] = '删已改名'
        红2 = 验写者(盘(t), 册2)[0]
        T('⑨之六 册坏：一族二写者（无多由）、例外逾一；册之写者寻不着其推（步名已易）→ 空名', any('写者恰一' in x and '主枝' in x for x in 红2)
          and any('例外 2 处' in x for x in 红2) and any('空名' in x and '删已改名' in x for x in 红2))
        甲治 = open(os.path.join(t, '工具', '甲.py'), encoding='utf-8').read()
        _写档(t, {'工具/甲.py': 甲治.replace("        直推()\n", "        pass\n    else:\n        直推()\n    if '--直' not in sys.argv:\n        直推()\n")})
        T('⑨之七 例外之函在旗之 else 之支、或否之判（not in）下调 → 例外越界（默路之掩⛔过）',
          sum('例外越界' in x for x in 验写者(盘(t), 册w)[0]) == 2)
        _写档(t, {'工具/甲.py': 甲治,
                  '工具/乙.py': ("import subprocess\nB = ['git']\n\n\ndef 跑(a):\n    return subprocess.run(['git', '-c', 'x=y'] + a)\n\n\n"
                                "def 串(n):\n    subprocess.run(['git'] + ['push', 'origin', 'HEAD:refs/heads/章-%d' % n])\n\n\n"
                                "def 变(n):\n    a = ['push', '-o', 'ci.skip', 'origin', 'HEAD:refs/heads/章-%d' % n]\n    subprocess.run(B + a)\n\n\n"
                                "def 包(n):\n    跑(['push', '--repo=origin', 'HEAD:refs/heads/章-%d' % n])\n\n\n"
                                "def 非推():\n    subprocess.run(['git', 'log', '--grep', 'push'])\n    跑(['fetch', 'origin', 'push'])\n")})
        乙 = sorted((w['者'], w['靶']) for w in 诸写(盘(t)) if w['档'] == '工具/乙.py')
        T('⑨之八 argv 之串接（[\'git\'] + […]、变量之列）、名不带 git 之包（体以 [\'git\', …] + 参 调者）、带值之旗（-o、--repo=）→ 俱解其靶；'
          'push 非其令（git log --grep push、fetch … push）⛔认', 乙 == sorted([('包', '章-*'), ('串', '章-*'), ('变', '章-*')]))
    finally:
        shutil.rmtree(t, ignore_errors=True)
    t = tempfile.mkdtemp(prefix='法用流_')
    try:   # yml 自析：⛔依 推报 之私函（推报改析即随崩）；步之行即其首行；${{ env.X }} 先填
        import 推报 as _推
        _私 = {k: getattr(_推, k) for k in ('_诸步', '_顶块') if hasattr(_推, k)}
        _写档(t, {'.github/workflows/v.yml': ("name: v\nenv:\n  MAIN: %s\njobs:\n  advance:\n    steps:\n      - uses: actions/checkout@v4\n"
                                              "        with:\n          fetch-depth: 0\n      - name: 并\n        id: adv\n        run: |\n"
                                              "          git push origin \"HEAD:refs/heads/${{ env.MAIN }}\"\n      - name: 他\n"
                                              "        run: git push origin \"HEAD:refs/heads/${{ inputs.ref }}\"\n") % 主枝})
        try:
            for k in _私:
                setattr(_推, k, lambda *a, **kw: (_ for _ in ()).throw(AttributeError('推报之私函已改')))
            流 = sorted((w['者'], w['行'], w['靶']) for w in 诸写(盘(t)))
        except Exception as ex:
            流 = [str(ex)]
        finally:
            for k, v in _私.items():
                setattr(_推, k, v)
        T('⑨之九 yml 自析（推报之私函改而⛔崩）：步之行＝其 `- ` 之行、${{ env.MAIN }} 填之、余之 ${{ … }} 不定作 *', 流 == [('adv', 10, 主枝), ('他', 14, '*')])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑩同功之检
    A, B = 全({'id': 'A', '名': 'a', '据': 'x', '起': 9, '时': '开', '证': [{'档': 'a'}]}), 全({'id': 'B', '名': 'b', '据': 'x', '起': 9, '时': '开', '证': [{'档': 'a'}]})
    A['功'] = B['功'] = '主枝之闸'
    B['处'] = 'GitHub'
    同 = {'法': [A, B]}
    补 = {'法': [dict(A, 互补=[{'与': 'B', '由': '相成之由'}]), B]}
    退 = {'法': [A, B], '废': [{'id': '退A', '法': 'A'}]}
    T('⑩同功两处：同功异处 → 红；书互补带由、或其一入废（废之法）→ 免；同处 → 免；真册 → 无', len(同功(同)) == 1 and not 同功(补) and not 同功(退)
      and not 同功({'法': [A, dict(B, 处='沙盒')]}) and not 同功(册))
    T('⑩之二 废而复立：已废之（功、处）（沙盒直推主枝：主枝之闸·沙盒）以新法之名复立 → 红；异处 → 免',
      any('废而复立' in x for x in 同功(dict(册, 法=册['法'] + [A]))) and not any('废而复立' in x for x in 同功(dict(册, 法=册['法'] + [B]))))
    # ⑪演练之证
    流 = 全({'id': '流', '名': '流', '据': 'x', '立': 413, '起': 413, '时': '段', '证': [{'档': 'a'}]})   # 时 段：此格只验演（⛔索行为之证·⑮另验）
    流.update(流程=True, 演=[{'账': '^封版後演'}, {'报': '演/*', '含': 'autopush'}])
    t0 = 1793100000
    录同 = [{'源': '账', 'id': '封版後演·410·x', '何': 'x', '果': '同', '时': t0, '文': '{}'}]
    T('⑪演：流程之法无录 → ⛔；账之录（果 同、早於其起）→ ✓；晚於其起章之封 → ⛔；果「异」→ ⛔；非流程 → 免',
      验演(流, [])[0] == '⛔' and 验演(流, 录同)[0] == '✓' and 验演(流, 录同, t0 - 1)[0] == '⛔' and '晚於其起' in 验演(流, 录同, t0 - 1)[1]
      and 验演(流, [dict(录同[0], 果='异')])[0] == '⛔' and 验演(dict(流, 流程=False), [])[0] == '免')
    T('⑪之二 册坏：流程之法无演无免；演免而立 > %d（演练之律後之法⛔免）；真册之流程之法俱有演或演免' % 演律之界,
      any('流 係流程之法而无「演」' in x for x in 完备({'法': [dict(流, 演=[])]}, ROOT)[0])
      and any('流 演免须由' in x for x in 完备({'法': [dict(流, 演免='旧法已行之由甚长')]}, ROOT)[0])
      and all(x.get('演') or x.get('演免') for x in 册['法'] if x.get('流程')))
    t = tempfile.mkdtemp(prefix='法用演_')
    try:
        源, 工 = os.path.join(t, 'o.git'), os.path.join(t, '工')
        env = dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t', GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')
        g = lambda *a, d=None: subprocess.run(['git'] + list(a), cwd=d or 工, capture_output=True, text=True, env=env)
        g('init', '-q', '--bare', 源, d=t)
        g('init', '-q', '-b', 主枝, 工, d=t)
        g('remote', 'add', 'origin', 源)
        _写档(工, {'a.txt': '甲'})
        g('add', '-A'); g('commit', '-qm', '甲')
        g('push', '-q', 'origin', 'HEAD:refs/heads/' + 主枝)
        甲sha = g('rev-parse', 'HEAD').stdout.strip()
        _写档(工, {'a.txt': '乙'})
        g('commit', '-qam', '乙（未入主）')
        乙sha = g('rev-parse', 'HEAD').stdout.strip()
        g('checkout', '-q', '--orphan', '报')
        g('rm', '-q', '-rf', '.')
        时 = lambda k: '2026-10-27T0%d:00:00Z' % k
        _写档(工, {'报/演/autopush-410.json': json.dumps({'果': '过', '时': 时(1), '何': 'autopush 於真料'}),
                  '报/推/章-8.json': json.dumps({'ref': '章-8', 'sha': 乙sha, '果': '红', '时': 时(2), '红': ['✗ 甲之项坏']}),
                  '报/推/章-7.json': json.dumps({'ref': '章-7', 'sha': 甲sha, '果': '败', '时': 时(1)}),
                  '报/推/治-x.json': json.dumps({'ref': '治-x', 'sha': 'f' * 40, '果': '红', '时': 时(3)}),
                  '报/推/治-y.json': json.dumps({'ref': '治-y', 'sha': 'e' * 40, '果': '成', '时': 时(4)}),
                  '报/推/治-z.json': json.dumps({'ref': '治-z', 'sha': 'd' * 40, '果': '成', '时': 时(5), '片': {'数': 3}})})
        g('add', '-A'); g('commit', '-qm', '报')
        g('push', '-q', 'origin', 'HEAD:refs/heads/备份/报')
        g('checkout', '-q', 主枝)
        录 = 演录(盘(工), 工, 取=True)
        T('⑪之三 报之源：origin 备份/报 之 报/演/*.json（GitHub 之演）一取得之，含之正则合 → ✓；含不合 → ⛔',
          any(r['源'] == '报' and r['果'] == '过' for r in 录) and 验演(流, 录)[0] == '✓'
          and 验演(dict(流, 演=[{'报': '演/*', '含': '封版'}]), 录)[0] == '⛔')
        # ⑪之三b（1027 丝滑）：报/推 之真推（同一 gate.yml、过即并）係演之上位——果 成 而带「片」→ ✓；无片（已在·免闸）、红 → ⛔；
        #   报/演 之式⛔为 报/推 所中；演之录果「成」⛔作好（成只认於真推）
        _推式 = dict(流, 演=[{'报': '推/*', '含': '"片"'}])
        _伪 = lambda 果, 推: [{'源': '报', 'id': '报/推/治-w.json' if 推 else '报/演/w.json', '何': '', '果': 果, '时': 1, '文': '{"片": {"数": 3}}', '推': 推}]
        T('⑪之三b 报/推 真推之闸：成而带片 → ✓；红而带片 → ⛔；推之录⛔中 演/* 之式；演之录果「成」⛔',
          验演(_推式, 录)[0] == '✓' and '治-z' in 验演(_推式, 录)[1]
          and 验演(_推式, [r for r in 录 if 'z.json' not in r['id']])[0] == '⛔'
          and 验演(_推式, _伪('红', True))[0] == '⛔' and 验演(_推式, _伪('成', True))[0] == '✓'
          and 验演(dict(流, 演=[{'报': '演/*', '含': '"片"'}]), 录)[0] == '⛔'
          and 验演(dict(流, 演=[{'报': '演/*', '含': '"片"'}]), _伪('成', False))[0] == '⛔')
        # ⑫报之读（自走之首）
        L = 报之读(工, 取=True)
        T('⑫报之读（真取·临时之裸库）：章-8 红（sha 未入主）未消 → ⛔；章-7 败而 sha 已入主 → 消；治-x 红而其後 治-y 成 → 消；≤三行',
          len(L) == 1 and L[0].startswith('⛔ 报·推 章-8 果「红」') and '甲之项坏' in L[0])
        g('push', '-q', 'origin', 'HEAD:refs/heads/' + 主枝)
        T('⑫之二 章-8 之 sha 入主枝（治而并）→ 消、印空', 报之读(工, 取=True) == [])
        多 = [{'类': '推', 'ref': '章-%d' % k, 'sha': 'a', '果': '红', '时': 时(k)} for k in range(1, 6)] + \
            [{'类': '演', '路': '报/演/封版.json', '果': '异', '时': 时(6)}]
        L多 = 报之读(工, 诸=多)
        T('⑫之三 坏报六（推五、演一）→ 恰三行：新者在前（演·异 首）、末行「另 4」；空诸 → 无行', len(L多) == 3 and L多[0].startswith('⛔ 报·演 封版')
          and '另 4 坏报' in L多[-1] and 报之读(工, 诸=[]) == [])
        T('⑫之五 演之坏：同所演之枝其後 过 → 消；他枝之 过 ⛔消之；无枝之名者以名', [d.get('ref') or d.get('名') for d in 未消之坏([
            {'类': '演', 'ref': '备份/演/甲', '果': '红', '时': 时(1)}, {'类': '演', 'ref': '备份/演/甲', '果': '过', '时': 时(2)},
            {'类': '演', 'ref': '备份/演/乙', '果': '红', '时': 时(1)}, {'类': '演', '名': '丙', '果': '红', '时': 时(3)},
            {'类': '演', '名': '丙', '果': '过', '时': 时(2)}])] == ['丙', '备份/演/乙'])
        T('⑫之四 未消之坏：同枝後成、治枝後有成即消；章标须其 sha 入主方消（⛔一成即消诸章）', [d['ref'] for d in 未消之坏([
            {'类': '推', 'ref': '章-8', 'sha': 'a', '果': '红', '时': 时(1)}, {'类': '推', 'ref': '治-y', 'sha': 'b', '果': '成', '时': 时(2)},
            {'类': '推', 'ref': '治-x', 'sha': 'c', '果': '拒', '时': 时(1)}])] == ['章-8'])
        # ⑪之四 验之合：流程之法未演 → 法 ⛔；缓之 → ⚠
        _写档(工, {'设定/写者册.json': json.dumps({'族': {}, '演': []})})
        流9 = dict(流, 立=9, 起=9, 演=[{'账': '^无此演'}], 证=[{'档': 'a.txt'}])
        e = 境(9, 工, 取=False, 承=False)
        okA, LA = 验(9, root=工, 册={'法': [流9], '待': []}, 境_=e)
        okB, LB = 验(9, root=工, 册={'法': [流9], '待': [], '缓': [{'id': '流', '立': 9, '至': 9, '由': '演待合流之由'}]}, 境_=e)
        T('⑪之四 --验 之合：流程之法未演 → 法 ⛔、rc 红；缓之（≤三章带由）→ ⚠ 过；头行带「执」之数', not okA and any(l.startswith('⛔ 流') and '未演' in l for l in LA)
          and okB and '流程未演 1' in LA[0])
    finally:
        shutil.rmtree(t, ignore_errors=True)


def 自测_核(T, 全):
    """1027 执行之核之自测（⑬常令 ⑭总章之条 ⑮行为之证 ⑯所废较旧 ⑰回灌 db52f247 ⑱预授之推 ⑲未行之数 ⑳坐异与自 ㉑量之增）：
    各带真伪两局（放行之反例）与回灌——⛔空验。"""
    import tempfile, shutil
    旧笔 = 'db52f247'
    t = tempfile.mkdtemp(prefix='法用核_')
    try:
        # ⑬作者常令 1021 起之令
        _写档(t, {'工具/甲器.py': 'x\n', 总章名: '# 总章\n', 常令名: (
            '# 常令\n- 1020 作者令：「旧」——落：`工具/无器.py`（1021 前⛔计）\n'
            '- 1021 作者令：「甲」——落：`工具/甲器.py`（册之证跑之）\n'
            '- 1022 作者令：「乙」——落：总章某节（法用#甲）\n'
            '- 1023 作者令：「丙」——落：`工具/无器.py` 与 法用#甲\n'
            '- 1024 作者令：「丁」——落：总章某节\n'
            '- 1027 作者令：「戊」——落：某（法用#无此法）\n'
            '- 1027 作者令：「己」——落：`工具/乙器.py`（盘上无、册亦无）\n')})
        册 = {'法': [全({'id': '甲', '名': '甲', '据': 'x', '起': 9, '时': '开', '证': [{'跑': '甲器.py'}]})], '待': [], '废': []}
        红, 数 = 常令之验(册, t)
        T('⑬作者常令 1021 起之令（%d）：落之器在盘且册之证跑之 ✓、法用#甲 ✓；落之档不在 → 令落之档不在（虽有法用#）；无据 → 令立无证；'
          '引册外之法 → 令引之法不在册；1020 之令⛔计' % 数, 数 == 6
          and not any('L3（' in x for x in 红) and not any('L4（' in x for x in 红)
          and any('L5（' in x and '令落之档不在' in x for x in 红) and not any('L5（' in x and '令立无证' in x for x in 红)
          and any('L6（' in x and '令立无证' in x for x in 红) and any('L7（' in x and '令引之法不在册' in x for x in 红)
          and any('L8（' in x and '令落之档不在' in x for x in 红) and any('L8（' in x and '令立无证' in x for x in 红)
          and not any('L2（' in x for x in 红) and len(红) == 6)
        # ⑭总章之条：五大主义、心诀（见五大主义之指⛔计）、§二—§六、§四 一条、§五 每「｜」
        _写档(t, {总章名: ('# 总章\n**★五大主义**：\n1. **虫洞**：省\n2. **虹吸**：引\n3. **完美**：满\n4. **丝滑**：顺\n5. **执行**：行\n\n'
                         '## 心诀\n1. **一**：甲\n2. **二**：见五大主义一（虫洞）。\n\n## 一、的\n不计\n## 二、钱\n1. **造**：x\n2. **问**：y\n'
                         '## 四、段\n段之事\n## 五、守\n⛔「鼎心」｜管档之改须 `改单.py`｜席⛔ git 写\n## 六、升\n1. **准**：z\n## 八、例\n1. 甲：q\n')})
        条 = [k for k, _ in 总章之条(t)]
        T('⑭总章之条：五大主义五、心诀一（「见五大主义」之指⛔计）、§二 二、§四 一、§五 三守、§六 一；§一、§八⛔入',
          条 == ['五大·虫洞', '五大·虹吸', '五大·完美', '五大·丝滑', '五大·执行', '心诀1', '§二.1', '§二.2', '§四', '§五·1', '§五·2', '§五·3', '§六.1'])
        键, 词 = 据之引('00_总章.md §二.1—2；§四；心诀一、八；五大主义·虫洞、执行；§五「管档」「鼎心」；§六.1；§八.3')
        T('⑭之二 据之引：§二.1—2 之段、§四、心诀一八、五大主义·虫洞执行、§五 之词、§八⛔入', 键 == {'§二.1', '§二.2', '§四', '心诀1', '心诀8', '五大·虫洞', '五大·执行', '§六.1'}
          and 词 == ['管档', '鼎心'])
        盖册 = {'法': [全({'id': 'A', '名': 'A', '据': '五大主义·虫洞、虹吸、完美、丝滑；心诀一；§二.1；§四；§五「管档」「鼎心」', '起': 9, '时': '段', '证': [{'档': 'x'}]})],
               '待': [{'id': 'B', '名': 'B', '据': '§六.1', '限': 9, '证': [{'档': 'x'}]}], '废': []}
        红a, n条 = 总章之盖(盖册, t)
        T('⑭之三 无据之条即红（五大主义·执行、§二.2、§五「席⛔ git 写」）；据於「待」亦算', n条 == 13 and len(红a) == 3
          and any('五大·执行' in x for x in 红a) and any('§二.2' in x for x in 红a) and any('§五·3' in x for x in 红a))
        盖册['机证不能'] = [{'据': '§二.2「问」', '由': '纯理：开件之前之判、器只见事後之费'}, {'据': '§五「席⛔ git 写」', '由': '短'}]
        红b, _ = 总章之盖(盖册, t)
        T('⑭之四 机证不能（据、由≥八字）即盖；由短 → 册坏', not any('§二.2' in x for x in 红b) and any('机证不能之条须' in x for x in 红b))
        盖册['机证不能'] = [{'据': '§二.%d' % i, '由': '纯理：某某某某某某某'} for i in (1, 2, 3, 4)]
        T('⑭之五 机证不能 4／13 逾四之一 → 红', any('逾四之一' in x for x in 总章之盖(盖册, t)[0]))
        # ⑭之六（复核补）机证不能之法之据⛔冒充有证：其所点之条入四之一之数
        盖册['机证不能'] = [{'据': '§二.%d' % i, '由': '纯理：某某某某某某某'} for i in (2, 3, 4)]
        机法 = 全({'id': 'M', '名': 'M', '据': '五大主义·执行；§五「席⛔ git 写」', '起': 9, '时': '开', '机证不能': True, '由': '纯理纯理纯理纯理'})
        有证 = {k: v for k, v in 机法.items() if k not in ('机证不能', '由')}
        有证['证'] = [{'跑': 'x.py'}]
        红m = 总章之盖(dict(盖册, 法=盖册['法'] + [机法]), t)[0]
        红y = 总章之盖(dict(盖册, 法=盖册['法'] + [有证]), t)[0]
        T('⑭之六 只为机证不能之法所点之条（五大·执行、§五·3）计入机证不能：3＋2／13 逾四之一 → 红；其法有证 → 3／13 放、⛔法立无证',
          any('逾四之一' in x and '五大·执行' in x for x in 红m) and not any('法立无证' in x for x in 红m) and 红y == [])
        # ⑭之七（复核补）心诀之「见五大主义」只纯指⛔计：其後另书新规者照计（⛔借指逃据）
        _写档(t, {总章名: '# 总章\n## 心诀\n1. **一**：见五大主义一（虫洞）。\n2. **二**：见五大主义一（虫洞）。另：每章必配插图。\n3. **三**：见五大主义五\n'})
        T('⑭之七 心诀：「见五大主义一（虫洞）。」与「见五大主义五」⛔计；「见五大主义一。另：每章必配插图。」照计',
          [k for k, _ in 总章之条(t)] == ['心诀2'])
        # ⑮行为之证
        行册 = {'法': [全({'id': 'p档', '名': 'x', '据': 'x', '起': 9, '时': '封後', '证': [{'档': '工具/a.py', '含': 'def a'}]}),
                      全({'id': 'p跑', '名': 'x', '据': 'x', '起': 9, '时': '开', '证': [{'档': 'a'}, {'跑': 'a.py'}]}),
                      全({'id': 'p迹', '名': 'x', '据': 'x', '起': 9, '时': '封前', '证': [{'档': '版本/第{N}章/_轮记.md'}]}),
                      全({'id': 'p含', '名': 'x', '据': 'x', '起': 9, '时': '封後', '证': [{'档': '设定/方法账.md', '含': 'W\\d+·第{N-1}章'}]}),
                      全({'id': 'p钩', '名': 'x', '据': 'x', '起': 9, '时': '开', '钩自跑': 'Stop（每回合）', '证': [{'钩': 'a.py', '于': 'Stop'}]}),
                      全({'id': 'p钩无', '名': 'x', '据': 'x', '起': 9, '时': '开', '钩自跑': 'Stop', '证': [{'档': 'a'}]}),
                      全({'id': 'p或', '名': 'x', '据': 'x', '起': 9, '时': '开', '证': [{'或': [{'跑': 'a.py'}, {'档': 'a'}]}]}),
                      全({'id': 'p段', '名': 'x', '据': 'x', '起': 9, '时': '段', '证': [{'档': 'a'}]}),
                      全({'id': 'p机', '名': 'x', '据': 'x', '起': 9, '时': '开', '机证不能': True, '由': '纯理纯理纯理纯理'})], '待': []}
        红c = 行为之验(行册)
        T('⑮行为之证：只档含 → 红；或之一支只档 → 红；钩自跑而无钩之证 → 红；跑、章之迹（路或含带 {N}）、钩自跑带钩、时 段、机证不能 → 放',
          sorted(x.split('：')[1].split('（')[0] for x in 红c) == ['p或', 'p档', 'p钩无'])
        # ⑯所废较旧
        _写档(t, {法账名: ('# 方法账\n## 升级链\n| 件 | 法 | 费 | 较旧 | 日 | 判 |\n|---|---|---|---|---|---|\n'
                           '| W1·第9章 | 所废：a | $1 | 较旧：效升；费降 | 1027 | 取 |\n| W2·第10章 | 所废：b | $1 | — | 1028 | 取 |\n'
                           '| W3·第11章 | 新法（未书其旧） | $1 | 较旧：无（新增） | 1029 | 取 |\n| W4·第12章 | 所废：无（新增） | $1 | 较旧：无（新增） | 1030 | 取 |\n'
                           '| W0·第8章 | 旧行 | $1 | — | 1020 | 取 |\n'),
                  总章名: '# 总章\n## 八、例\n%s\n' % '\n'.join('%d. 例%d：所废：x；较旧：效升；费降' % (i, i) if i != 22 else '22. 例二十二：旧式无较旧' for i in range(1, 23))
                  + '23. 例二十三：所废：x；较旧：效升；费降\n24. 例二十四：只书其法\n'})
        红d = 废旧之验(t)
        T('⑯所废较旧：方法账 1027 起之行缺「较旧」（W2）、缺「所废」（W3）→ 红；「较旧：无」放；1020 之行⛔计；§八 ≥23 缺之（24）→ 红、≤22（22）⛔计',
          len(红d) == 3 and any('W2' in x for x in 红d) and any('W3' in x for x in 红d) and any('§八.24' in x for x in 红d)
          and not any(k in x for x in 红d for k in ('W1', 'W4', 'W0', '§八.22', '§八.23')))
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑰回灌 db52f247（执行之核前之树：总章、常令、方法账、册）→ 完备之扩俱红；今之树俱绿
    if _有笔(ROOT, 旧笔):
        t = tempfile.mkdtemp(prefix='法用核旧_')
        try:
            for p in (总章名, 常令名, 法账名, 册名):
                r = subprocess.run(['git', 'show', '%s:%s' % (旧笔, p.replace(os.sep, '/'))], cwd=ROOT, capture_output=True, text=True)
                _写档(t, {p: r.stdout})
            for p in ('工具/*.py', '设定/*.md', '设定/*.json', '.claude/settings.json', '00_*.md', 'README.md'):    # 落之档在盘之判用今盘之路名（⛔误报「不在」）
                for f in glob.glob(os.path.join(ROOT, p)):
                    g = os.path.join(t, os.path.relpath(f, ROOT))
                    if not os.path.exists(g):
                        os.makedirs(os.path.dirname(g), exist_ok=True)
                        open(g, 'w').close()
            旧册 = json.load(open(os.path.join(t, 册名), encoding='utf-8'))
            红e = 完备(旧册, t)[0]
            类 = {k: sum(1 for x in 红e if k in x) for k in ('令立无证', '法立无证：总章', '法证只验码在')}
            今红 = [x for x in 完备(读册(ROOT), ROOT)[0] if '方法账「' not in x]      # 方法账之行係逐章之状（同 ①）
            T('⑰回灌 %s（执行之核前）：作者常令之令立无证 %d、总章之条无据 %d、法证只验码在 %d——俱 >0（⛔空验）；今之树（常令、总章、行为之证）俱绿%s' % (
                旧笔, 类['令立无证'], 类['法立无证：总章'], 类['法证只验码在'], ('：' + 今红[0][:60]) if 今红 else ''), all(类.values()) and not 今红)
        finally:
            shutil.rmtree(t, ignore_errors=True)
    else:
        T('⑰回灌之笔 %s 寻不着（浅克隆补史亦不得）' % 旧笔, False)
    # ⑱预授之推（settings 之 permissions.allow·1027 #68）
    红旧 = [x for x in 验写者(盘(ROOT, 旧笔), 读写者册())[0] if '.claude/settings.json' in x]
    t = tempfile.mkdtemp(prefix='法用预_')
    try:
        def 预(诸):
            _写档(t, {'.claude/settings.json': json.dumps({'permissions': {'allow': 诸}}, ensure_ascii=False)})
            return 预授之推(盘(t))
        p1 = 预(['Bash', 'Bash(git push origin 章-411:*)', 'Bash(git push -u origin %s:*)' % 主枝, 'Bash(git push:*)',
                'Bash(git -c x=y push origin HEAD:refs/heads/%s)' % 主枝, 'Bash(git fetch:*)', 'Bash(python3 工具/推.py:*)'])
        T('⑱预授之推：显靶（章-411、主枝、HEAD:refs/heads/主枝）、无靶即 *；非 push 之令⛔计',
          [x[1] for x in p1] == ['章-411', 主枝, '*', 主枝])
        册w = {'族': {'主枝': {'式': [主枝], '写': [{'档': 'x', '函': 'y'}]}, '章标': {'式': ['章-*'], '写': [{'档': 'x', '函': 'z'}]}}}
        预(['Bash(git push origin 章-411:*)', 'Bash(git push origin 备份/存底:*)'])
        放 = [x for x in 验写者(盘(t), 册w)[0] if 'settings' in x]
        预(['Bash(git push origin %s:*)' % 主枝, 'Bash(git push:*)'])
        拦 = [x for x in 验写者(盘(t), 册w)[0] if 'settings' in x]
        T('⑱之二 写者：预授 git push 主枝、无靶之 push → 二写者红；预授推章标、存底之枝 → 放；回灌 %s 之 settings（直推主枝二条）→ 红 %d、今之树 ⛔红'
          % (旧笔, len(红旧)), not 放 and len(拦) == 2 and len(红旧) == 2
          and not [x for x in 验写者(盘(ROOT))[0] if '.claude/settings.json' in x])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑲未行之数：棘轮（只许降）、降底之改文、真算
    判 = [未行之判(n, {'未行': {'底': 5, '记': []}})[0] for n in (6, 5, 4, None)]
    T('⑲未行之判：数 ＞ 底 ⛔、＝ ✓、＜ ✓（印可降）、算不得 ⚠、无底 ⛔', 判 == ['⛔', '✓', '✓', '⚠'] and 未行之判(1, {})[0] == '⛔'
      and '可降' in 未行之判(4, {'未行': {'底': 5}})[1])
    s0 = '{\n "法": [],\n "未行": {"底": 9, "记": ["1027 立"]},\n "废": []\n}\n'
    s1 = _改底(s0, 9, 7, '1028')
    T('⑲之二 降底：就地改其数、记首添「1028 9→7」、余文⛔动；⛔升（7→9）、底不符即⛔改', s1 is not None and json.loads(s1)['未行'] == {'底': 7, '记': ['1028 9→7', '1027 立']}
      and s1.replace('"底": 7, "记": ["1028 9→7", ', '"底": 9, "记": [') == s0 and _改底(s1, 7, 9, '1029') is None and _改底(s0, 8, 7, '1028') is None)
    数, 分 = 未行(ROOT)
    册 = 读册(ROOT)
    首 = 报首(ROOT)
    T('⑲之三 真算：七分（%s；底 %s——棘轮之红归 --报 之格·器红，⛔入此读者可见之负测）；--报 --首 一行（%s）' % (
        '＋'.join('%s %s' % x for x in 分), (册.get('未行') or {}).get('底'), 首[:40]),
      len(分) == 7 and sum(v is not None for _, v in 分) >= 5 and '\n' not in 首 and 首[:1] in '✓⛔⚠' and ('未行之数' in 首 or 首[:1] == '⚠'))
    # ⑳坐异（换会话之证）与 git 改之「自」：假仓
    t = tempfile.mkdtemp(prefix='法用坐_')
    try:
        工 = os.path.join(t, '工')
        _git(t, 'init', '-q', 工)
        for k, v in (('user.name', 't'), ('user.email', 't@t'), ('commit.gpgsign', 'false')):
            _git(工, 'config', k, v)
        t0 = 1790000000

        def 提(档们, msg, 时):
            _写档(工, 档们)
            _git(工, 'add', '-A')
            subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=工, capture_output=True,
                           env=dict(os.environ, GIT_AUTHOR_DATE='@%d +0000' % 时, GIT_COMMITTER_DATE='@%d +0000' % 时))
        提({'a.md': '1'}, '第7章封版（造式二代·封版#7）\n\nClaude-Session: https://claude.ai/code/session_AAAAAAAA1111', t0)
        提({'总站.html': '1'}, '总站随段', t0 + 100)
        提({'a.md': '2'}, '第8章封版（造式二代·封版#8）\n\nClaude-Session: https://claude.ai/code/session_AAAAAAAA1111', t0 + 200)
        提({'a.md': '3'}, '第9章封版（造式二代·封版#9）\n\nClaude-Session: https://claude.ai/code/session_BBBBBBBB2222', t0 + 300)
        def 坐(n, 今=None, 史=None):
            e = 境(n, 工, 史版=史, 取=False, 承=False)
            e.坐 = 今
            return 验证({'git': '坐异'}, e)[0]
        T('⑳坐异：前章之坐（Claude-Session）≠ 本坐 ✓、同 ⛔、本坐未名 ？；史（封版#9 对 #8）✓、（#8 对 #7）⛔',
          坐(9, 'CCCCCCCC3333') == '✓' and 坐(9, 'AAAAAAAA1111') == '⛔' and 坐(9, '') == '？' and 坐(9, 史=封提交(9, 工)) == '✓' and 坐(8, 史=封提交(8, 工)) == '⛔')
        e = 境(10, 工, 取=False, 承=False)
        T('⑳之二 git 改之「自」：总站於第7章封版以来有提交 ✓；自第8章 ⛔（窗跨一段·⛔只认前章封後）', 验证({'git': '改', '档': '总站.html', '自': '7'}, e)[0] == '✓'
          and 验证({'git': '改', '档': '总站.html', '自': '{N-2}'}, e)[0] == '⛔' and 填('{前段-1}{前段}{前段末}', 421) == '410411420')
        # ⑳之三 开章即判坐异（复核补·丝滑：问题早见——同坐者封版 --後 必拦，⛔候钱花完方红）
        坐册 = {'法': [{'id': '换会话', '名': '换会话', '据': 'x', '起': 1, '时': '封後', '证': [{'git': '坐异'}]}], '待': [], '废': []}
        旧环 = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID')
        try:
            os.environ['CLAUDE_CODE_REMOTE_SESSION_ID'] = 'cse_BBBBBBBB2222'
            同 = 开(10, 工, 册=坐册, 执=False)
            os.environ['CLAUDE_CODE_REMOTE_SESSION_ID'] = 'cse_DDDDDDDD4444'
            异 = 开(10, 工, 册=坐册, 执=False)
        finally:
            if 旧环 is None:
                os.environ.pop('CLAUDE_CODE_REMOTE_SESSION_ID', None)
            else:
                os.environ['CLAUDE_CODE_REMOTE_SESSION_ID'] = 旧环
        T('⑳之三 开章即判坐异：本坐即前章（封版#9）之坐 → 开之印首项「⛔ 换会话」；新坐 → 无此⛔（放行）',
          len(同) > 1 and 同[1].strip().startswith('⛔ 换会话') and not any('⛔ 换会话' in x for x in 异))
        # ⑳之五（复核补·丝滑）时 十 之法於段首之开即先验（本机：档、git 改）——⛔候封版 --後 方红；⛔者列首、⛔为截行所掩
        提({'a.md': '4'}, '第10章封版（造式二代·封版#10）\n\nClaude-Session: https://claude.ai/code/session_BBBBBBBB2222', t0 + 400)
        十册 = {'法': [全({'id': '拍随', '名': 'x', '据': 'x', '起': 1, '时': '十', '证': [{'或': [{'档': '拍库.md', '含': '第{前段}段'},
                                                                                          {'git': '改', '档': '总站.html', '自': '{前段-1}'}]}]})]
                       + [全({'id': '杂%d' % i, '名': 'x', '据': 'x', '起': 1, '时': '封前', '证': [{'档': 'a.md'}]}) for i in range(12)], '待': []}
        缺 = 开(11, 工, 册=十册, 执=False)
        _写档(工, {'拍库.md': '## 第1段\n某拍\n'})
        有 = 开(11, 工, 册=十册, 执=False)
        T('⑳之五 时 十 之法段首（11）之开即先验：拍库无「第1段」、总站自第0章封版以来…（寻不着）→ 首项「⛔ 拍随」（法多亦⛔掩）；拍库有之 → 无⛔（放行）',
          缺[1].strip().startswith('⛔ 拍随') and not any('⛔ 拍随' in x for x in 有)
          and 验法(十册['法'][0], 境(11, 工, True, 取=False, 承=False))[0] == '✓')
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑳之四 封版之尾⛔写死一坐（坐异之源·复核补）：旧尾写死 session_016Hgfc2…，坐异读之即恒同（总编辑之坐）或恒异（余坐）＝空验
    尾证 = next((c for x in 读册(ROOT).get('法') or [] if x.get('id') == '换会话' for c in x.get('证') or [] if c.get('档') == '工具/封版.py'), None)
    旧封 = subprocess.run(['git', 'show', '%s:工具/封版.py' % 旧笔], cwd=ROOT, capture_output=True, text=True).stdout
    今封 = _读(ROOT, os.path.join('工具', '封版.py')) or ''
    尾码 = '\n'.join(l for l in 今封.split('\n') if l.startswith(('_坐 = ', '尾 = ')))

    def 尾之(号):
        旧 = os.environ.get('CLAUDE_CODE_REMOTE_SESSION_ID')
        try:
            if 号:
                os.environ['CLAUDE_CODE_REMOTE_SESSION_ID'] = 号
            else:
                os.environ.pop('CLAUDE_CODE_REMOTE_SESSION_ID', None)
            ns = {'os': os, 're': re}
            exec(尾码, ns)
            return ns.get('尾', '')
        except Exception:
            return ''
        finally:
            if 旧 is None:
                os.environ.pop('CLAUDE_CODE_REMOTE_SESSION_ID', None)
            else:
                os.environ['CLAUDE_CODE_REMOTE_SESSION_ID'] = 旧
    甲尾, 乙尾 = 尾之('cse_EEEEEEEE5555'), 尾之('')
    T('⑳之四 封版之尾：回灌 %s 之 封版.py（写死一坐）→ 换会话之「无」中（红）；今之尾取本会话（cse_→session_）、无号即⛔书 Claude-Session（坐异作 ？）' % 旧笔,
      bool(尾证) and bool(旧封) and re.search(尾证['无'], 旧封) is not None and re.search(尾证['无'], 今封) is None
      and 甲尾.endswith('Claude-Session: https://claude.ai/code/session_EEEEEEEE5555') and 'Co-Authored-By' in 乙尾 and 'Claude-Session' not in 乙尾)
    # ⑳之六（复核补）自走所印段之势之令⛔式新（§八.3 剧情庭式段：裁席出单、主环 --施单）：回灌 db52f247 之 自走.py → 剧情庭式段之「无」中（红）；今 → ⛔中
    段证 = next((c for x in 读册(ROOT).get('法') or [] if x.get('id') == '剧情庭式段' for c in x.get('证') or [] if c.get('档') == '工具/自走.py'), None)
    旧走 = subprocess.run(['git', 'show', '%s:工具/自走.py' % 旧笔], cwd=ROOT, capture_output=True, text=True).stdout
    今走 = _读(ROOT, os.path.join('工具', '自走.py')) or ''
    T('⑳之六 自走所印段之势之令：回灌 %s（式新·裁席亲改）→ 剧情庭式段之「无」中（红）；今（式段·W·段料）→ ⛔中' % 旧笔,
      bool(段证) and bool(旧走) and re.search(段证['无'], 旧走) is not None and re.search(段证['无'], 今走) is None
      and "式:\\'段\\'" in 今走)
    # ㉒暂停令之据（改常令移行号即令在而不认）
    t = tempfile.mkdtemp(prefix='法用停_')
    try:
        令 = {'立': 'x', '令': '作者令：暂停', '据': '设定/常.md:3', '解': None}
        _写档(t, {'设定/常.md': '甲\n乙\n- 1027 作者令·暂停令（候令）\n', '设定/暂停令.json': json.dumps(令, ensure_ascii=False)})
        好 = 暂停之据(t)
        _写档(t, {'设定/常.md': '甲\n- 1027 作者令·暂停令（候令）\n丙\n'})        # 删一行：据之行移
        移 = 暂停之据(t)
        _写档(t, {'设定/暂停令.json': json.dumps(dict(令, 解={'时': 'y'}), ensure_ascii=False)})
        解 = 暂停之据(t)
        T('㉒暂停令之据：据之行有「暂停令」✓；常令删一行致据移 → 红（并指今在之行 L2）；令已解 → ⛔验；今之树 ✓',
          好 == [] and len(移) == 1 and 'L2' in 移[0] and 解 == [] and 暂停之据(ROOT) == [])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ㉑量之增（真费账＋复盘）：验占、记占、大审费
    q = 章量(410)
    T('㉑量：410 之验占（复盘按类之验）、记占（记席之行）；大审费（费账名含「大审…387」之合）', 0.05 < (q.get('验占') or 0) < 0.2
      and 0.05 < (q.get('记占') or 0) < 0.2 and 大审费(387) == 85.71 and 大审费(9999) is None)


def 自测():
    import tempfile, shutil
    R = []

    def T(名, 条):
        R.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    全 = lambda x: dict({'功': x['id'], '处': '沙盒', '流程': False}, **x)     # 假法：执行之守之三键（功、处、流程）默填
    # ①册之形与完备（真册）
    册 = 读册(ROOT)
    红 = [x for x in 完备(册, ROOT)[0] if '方法账「' not in x]     # 方法账之行係逐章之状：封版 --验 拦、全测「法用之守」报；此格只守册之形与总章§八
    T('①真册：册之形无坏、总章§八俱有据、机证不能 ≤ 四之一%s' % (('：' + 红[0][:60]) if 红 else ''), not 红)
    八 = 总章之八(ROOT)
    T('①之二 总章§八 读得出 ≥16 条，册之据盖其 1—16', len(八) >= 16 and all(
        any(re.search(r'§八\.%d(?!\d)' % k, x['据']) for x in 册['法'] + 册['待']) for k in range(1, 17)))
    T('①之三 待：缓存分档之探限 411、411 首回缓存读与窄审之核限 412', any(x['限'] == 411 and '缓存分档' in x['名'] for x in 册['待'])
      and any(x['限'] == 412 and '窄审' in x['名'] and '费审' in x['名'] for x in 册['待']))
    T('①之四 autopush 之证起 412（411 之封只验章-410 之主枝）、证取 报/推/章-{N-1}', any(
        x['id'] == '推闸交GitHub' and x['起'] == 412 and x['证'][0].get('报') == '推/章-{N-1}' for x in 册['法']))
    T('①之五 兜底之推只认 推.py --直（G 後 推.py 默交治枝係常路⛔警）；待之证落方法账者其示带「法用#<id>」（照示记之即过完备）',
      any(c.get('跑') == '推.py' and c.get('不') and c.get('参') == '--直' for x in 册['法'] for c in x.get('证') or [])
      and all(('法用#' + x['id']) in x.get('示', '') for x in 册['待'] if '方法账' in json.dumps(x['证'], ensure_ascii=False)))
    # ②完备之律：造一假仓
    t = tempfile.mkdtemp(prefix='法用_')
    try:
        os.makedirs(os.path.join(t, '设定'))
        open(os.path.join(t, 总章名), 'w', encoding='utf-8').write('# 总章\n## 八、升级之例\n1. 甲法：x\n2. 乙法：y\n3. 丙法：z\n## 九\n')
        open(os.path.join(t, 法账名), 'w', encoding='utf-8').write(
            '# 方法账\n| 件 | 法 |\n|---|---|\n| D6 收口（1008） | x |\n| 新法甲（1027） | 所废：y；较旧：效升；费平 |\n| 净重对表（2610字） | 非日之四数⛔认作日 |\n\n'
            '## 升级链\n| 件 | 法 | 费 | 较旧 | 日 | 判 |\n|---|---|---|---|---|---|\n| W1·第9章 | 所废：a | $1 | — | 1024 | 取 |\n'
            '| W2·第10章 | 所废：b | $1 | 较旧：效平；费降 | 1028 | 取 |\n| W3·第11章 | 所废：c 法用#乙 | $1 | 较旧：无（新增） | 0105 | 取 |\n')
        假 = {'法': [全({'id': '甲', '名': '甲', '据': '总章 §八.1', '起': 9, '时': '段', '证': [{'档': 'a.md'}]}),     # 时 段：⛔索行为之证（此格只验§八与方法账）
                    全({'id': '乙', '名': '乙', '据': '总章 §八.2；设定/方法账.md 新法甲', '起': 9, '时': '段', '证': [{'档': 'b.md'}]})], '待': []}
        红2, _ = 完备(假, t)
        T('②完备：§八.3 无据 → 法立无证；方法账 1028 之行（W2）无据 → 红；1024 之行免；「法用#乙」与「方法账.md 新法甲」认；「（2610字）」非日⛔红', any('§八.3' in x for x in 红2)
          and any('W2·第10章' in x for x in 红2) and not any('W1' in x for x in 红2) and not any('W3' in x for x in 红2)
          and not any('新法甲' in x for x in 红2) and len(红2) == 2)
        假['法'].append(全({'id': '丙', '名': '丙', '据': '§八.3；设定/方法账.md W2', '起': 9, '时': '开', '机证不能': True, '由': '短'}))
        红3, _ = 完备(假, t)
        T('②之二 机证不能须写由（⛔短于八字）；W2 由 据「方法账.md W2」认', any('机证不能而无由：丙' in x for x in 红3) and not any('W2' in x for x in 红3))
        假['法'][2]['由'] = '纯理：无章之迹可数，其守在某器'
        假['法'].append(全({'id': '丁', '名': '丁', '据': 'x', '起': 9, '时': '开', '机证不能': True, '由': '纯理：无章之迹可数之由'}))
        红4, _ = 完备(假, t)
        T('②之三 机证不能 2／4 逾四之一 → 红', any('逾四之一' in x for x in 红4))
        假['法'] = 假['法'][:3]
        假['法'].append(全({'id': '戊', '名': '戊', '据': 'x', '起': 9, '时': '午', '证': [{'怪': 1}]}))
        红5, _ = 完备(假, t)
        T('②之四 时不识、证之式不识 → 册坏', sum('册坏' in x for x in 红5) == 2)
        假['法'] = 假['法'][:3]
        假['缓'] = [{'id': '甲', '立': 9, '至': 14, '由': '某由某由'}]
        T('②之五 缓逾三章 → 缓坏', any('缓坏' in x for x in 完备(假, t)[0]))
        假['缓'] = []
        try:   # ②之六 工作流账 --裁 W 取 所登之行：由之末之「法用#乙」⛔随截而失，且其行即认（W2 之红不变）
            import 工作流账 as _工, datetime as _dt
            json.dump({'件': [{'id': 'W9', '名': '第12章'}, {'id': 'W8', '名': '第11章'}]},
                      open(os.path.join(t, '设定', '工作流账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            _日 = _dt.datetime(2026, 10, 28, tzinfo=_dt.timezone.utc)
            _工.登方法账('W9', '所废：' + '旧法' * 60 + '；较旧：效平费降 法用#乙', t, _日)
            _工.登方法账('W8', '所废：旧法；较旧：效平费降', t, _日)
            _行 = [l for l in open(os.path.join(t, 法账名), encoding='utf-8') if l.startswith('| W9·')]
            _红 = 完备(假, t)[0]
            T('②之六 工作流账所登 1028 之行带「法用#乙」（由逾百字亦⛔失）→ 完备认之；无「法用#」之行（W8）→ 法立无证', len(_行) == 1
              and '法用#乙' in _行[0] and not any('W9' in x for x in _红) and any('W8·第11章' in x for x in _红))
        except Exception as ex:
            T('②之六 工作流账之登跑不得：%s' % ex, False)
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ③诸证之真伪两局：假仓（git 与 origin 皆在本机）
    t = tempfile.mkdtemp(prefix='法用_')
    try:
        源, 工 = os.path.join(t, 'origin.git'), os.path.join(t, '工')
        _git(t, 'init', '-q', '--bare', 源)
        _git(t, 'init', '-q', 工)
        for k, v in (('user.name', 't'), ('user.email', 't@t'), ('commit.gpgsign', 'false')):
            _git(工, 'config', k, v)
        _git(工, 'remote', 'add', 'origin', 源)

        def 提(档们, msg, 时):
            for p, s in 档们.items():
                os.makedirs(os.path.dirname(os.path.join(工, p)) or 工, exist_ok=True)
                open(os.path.join(工, p), 'w', encoding='utf-8').write(s)
            _git(工, 'add', '-A')
            env = dict(os.environ, GIT_AUTHOR_DATE='@%d +0000' % 时, GIT_COMMITTER_DATE='@%d +0000' % 时)
            subprocess.run(['git', 'commit', '-q', '-m', msg], cwd=工, env=env, capture_output=True)
        t0 = 1790000000
        提({'设定/a.md': 'x', '.claude/settings.json': json.dumps({'hooks': {'SessionStart': [{'hooks': [{'command': 'python3 工具/存底守.py --起'}]}]},
                                                                  'permissions': {'allow': ['Bash(python3 工具/封版.py:*)']}})}, '第8章《甲》封版（造式二代·封版#8）', t0)
        _git(工, 'push', '-q', 'origin', 'HEAD:refs/heads/章-8', 'HEAD:refs/heads/主')
        提({'设定/交接_续跑.md': '现状'}, '交接现状', t0 + 600)
        提({'版本/第9章/_轮记.md': '## 造式·逻辑审·合後·第1回\n据 正文＝v02\n窄审（稿差：行变 1）'}, '409 草', t0 + 1200)
        _git(工, 'branch', '-q', '报', 'HEAD')
        _git(工, 'checkout', '-q', '--orphan', '报枝')
        _git(工, 'rm', '-q', '-rf', '.')
        提({'报/推/章-8.json': json.dumps({'果': '成'}), '报/推/章-7.json': json.dumps({'果': '败'})}, '报', t0 + 1300)
        _git(工, 'push', '-q', 'origin', 'HEAD:refs/heads/备份/报')
        _git(工, 'checkout', '-q', '--orphan', '存底枝')     # 前坐之存底：其迹（派器 --甲 9）只在云端
        _git(工, 'rm', '-q', '-rf', '.')
        提({'_器之迹.jsonl': json.dumps({'t': _iso(t0 + 700), '器': '派器.py', '参': ['--甲', '9']}) + '\n'}, '存底', t0 + 1310)
        _git(工, 'push', '-q', 'origin', 'HEAD:refs/heads/备份/存底')
        _git(工, 'checkout', '-q', '报')
        _git(工, 'fetch', '-q', 'origin')
        _git(工, 'push', '-q', 'origin', 'HEAD:refs/heads/主2')
        open(os.path.join(工, '_跑账.json'), 'w').write(json.dumps({'稿差.py': {'末跑': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t0 + 1500))},
                                                              '旧器.py': {'末跑': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t0 - 60))},
                                                              '派器.py': {'末跑': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t0 + 1400))},
                                                              '测器.py': {'末跑': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t0 + 800))}}))
        open(os.path.join(工, '_器之迹.jsonl'), 'w').write(json.dumps({'t': _iso(t0 + 900), '器': '接棒守.py', '参': ['--候主', '8']}) + '\n'
                                                       + json.dumps({'t': _iso(t0 + 800), '器': '测器.py', '参': ['--自测']}) + '\n')
        e = 境(9, 工, 承=lambda: None, 今=t0 + 1600)
        V = lambda c: 验证(c, e)[0]
        T('③开＝前章封版之提交之时（git log --grep 封版#N）', e.开 == t0)
        T('③档：在／不在、含之列、无之犯、{N} 之填', V({'档': '版本/第{N}章/_轮记.md', '含': ['据\\s*正文\\s*[＝=]\\s*v\\d+', '窄审']}) == '✓'
          and V({'档': '版本/第{N}章/_无.md'}) == '⛔' and V({'档': '版本/第{N}章/_轮记.md', '含': '全审'}) == '⛔'
          and V({'档': '版本/第{N}章/_轮记.md', '无': '窄审'}) == '⛔' and V({'档': '设定/*.md'}) == '✓' and V({'档': '版本/第{N}章/_无.md', '不': True}) == '✓')
        T('③跑：末跑 ≥ 开 → ✓；末跑早於开 → ⛔；从未 → ⛔；迹之参（--候主 {N-1}）', V({'跑': '稿差.py'}) == '✓' and V({'跑': '旧器.py'}) == '⛔'
          and V({'跑': '无器.py'}) == '⛔' and V({'跑': '接棒守.py', '参': '--候主 {N-1}'}) == '✓' and V({'跑': '接棒守.py', '参': '--派令 {N}'}) == '⛔')
        e2, e3 = 境(9, 工, 承=lambda: None, 今=t0 + 1600), 境(9, 工, 承=False, 今=t0 + 1600)
        T('③跑之参：本机迹无其器而跑账有末跑 → 先承云端之迹再判（云迹 --甲 9：参 --乙 ⛔、--甲 {N} ✓）；⛔网方退「参未核」',
          验证({'跑': '派器.py', '参': '--乙'}, e2)[0] == '⛔' and 验证({'跑': '派器.py', '参': '--甲 {N}'}, e2)[0] == '✓'
          and 验证({'跑': '派器.py', '参': '--乙'}, e3)[0] == '✓' and '参未核' in 验证({'跑': '派器.py', '参': '--乙'}, e3)[1])
        T('③跑之自测：迹唯 --自测 之跑（全测诸格）⛔算用法、⛔退跑账；不而有参：账不辨参 ⛔诬其跑', V({'跑': '测器.py'}) == '⛔'
          and '迹唯其自测' in 验证({'跑': '测器.py'}, e)[1] and 验证({'跑': '派器.py', '参': '--直', '不': True}, e3)[0] == '✓'
          and 验证({'跑': '派器.py', '不': True}, e3)[0] == '⛔')
        浅 = os.path.join(t, '浅')
        subprocess.run(['git', 'clone', '-q', '--depth', '1', '--branch', '主2', 'file://' + 源, 浅], capture_output=True)
        T('③浅克隆（云端会话五十笔）：前章之封在其外 → 补全史一回再寻得开；⛔网（--开）即无界',
          境(9, 浅, 取=False, 承=False).开 is None and 境(9, 浅, 承=False).开 == t0)
        T('③跑之近与不：近 60 分（末跑距今 100 秒）✓、近 1 分 ⛔；不：未跑之器 ✓、已跑之器 ⛔', V({'跑': '稿差.py', '近': 60}) == '✓'
          and V({'跑': '稿差.py', '近': 1}) == '⛔' and V({'跑': '推.py', '不': True}) == '✓' and V({'跑': '稿差.py', '不': True}) == '⛔')
        T('③git：含（章-{N-1} 在 主）✓、改（交接於封後有提交；含封：封版之提交本身亦算）✓、枝（备份/报）✓；无之 ⛔', V({'git': '含', '甲': '章-{N-1}', '乙': '主'}) == '✓'
          and V({'git': '改', '档': '设定/交接_续跑.md'}) == '✓' and V({'git': '改', '档': '设定/a.md'}) == '⛔'
          and V({'git': '改', '档': '设定/a.md', '含封': True}) == '✓' and V({'git': '改', '档': '设定/无.md', '含封': True}) == '⛔'
          # 于封（1027 A2 验）：档在封版之提交本身 ✓；封後另提交者（旧序）⛔——含封则二者俱 ✓（空跑之回灌）
          and V({'git': '改', '档': '设定/a.md', '于封': True}) == '✓' and V({'git': '改', '档': '设定/交接_续跑.md', '于封': True}) == '⛔'
          and V({'git': '改', '档': '设定/交接_续跑.md', '含封': True}) == '✓'
          and V({'git': '枝', '枝': '备份/报'}) == '✓' and V({'git': '枝', '枝': '备份/无'}) == '⛔' and V({'git': '含', '甲': '章-99', '乙': '主'}) == '⛔')
        T('③报：章-8 果＝成 ✓；章-7 果＝败 ⛔；章-6 不在 ⛔', V({'报': '推/章-{N-1}'}) == '✓' and V({'报': '推/章-7'}) == '⛔' and V({'报': '推/章-6'}) == '⛔')
        T('③钩：SessionStart 含存底守 ✓、PreToolUse 无 ⛔、permissions 含封版 ✓', V({'钩': '存底守.py --起', '于': 'SessionStart'}) == '✓'
          and V({'钩': '会话之守.py', '于': 'PreToolUse'}) == '⛔' and V({'钩': 'Bash(python3 工具/封版.py:*)', '于': 'permissions'}) == '✓')
        T('③或、若、限、轻、起、段首、阶後', V({'或': [{'档': '无.md'}, {'档': '设定/a.md'}]}) == '✓' and V({'或': [{'档': '无.md'}, {'档': '无2.md'}]}) == '⛔'
          and V({'档': '无.md', '段首': True}) == '免' and 验证({'档': '无.md', '段首': True}, 境(11, 工, 承=False, 取=False))[0] == '⛔'
          and V({'若': {'档': '无.md'}, '则': {'档': '无2.md'}}) == '免' and V({'若': {'档': '设定/a.md'}, '则': {'档': '无2.md'}}) == '⛔'
          and V({'限': 9}) == '✓' and V({'限': 8}) == '⛔' and V({'档': '无.md', '轻': True}) == '⚠' and V({'档': '无.md', '起': 10}) == '免'
          and 验证({'跑': '无器.py', '阶': '後'}, 境(9, 工, True, 承=lambda: None))[0] == '免')
        # ④验之合：法与待、缓
        假册 = {'法': [全({'id': '甲', '名': '甲', '据': 'x', '起': 9, '时': '封前', '证': [{'档': '版本/第{N}章/_轮记.md'}]}),
                      全({'id': '乙', '名': '乙', '据': 'x', '起': 9, '时': '封後', '证': [{'报': '推/章-7'}]}),
                      全({'id': '丙', '名': '丙', '据': 'x', '起': 10, '时': '段', '证': [{'档': '无.md'}]}),
                      全({'id': '丁', '名': '丁', '据': 'x', '起': 9, '时': '十', '证': [{'档': '无.md'}]})],
                '待': [{'id': '戊', '名': '戊', '据': 'x', '限': 9, '证': [{'档': '无.md'}], '示': '记之'},
                      {'id': '己', '名': '己', '据': 'x', '限': 10, '证': [{'档': '无.md'}]}]}
        ok, L = 验(9, root=工, 册=假册, 境_=e, 执=False)
        T('④验 9：乙（报之果败）⛔、待·戊（限 9）⛔；丙（起 10）、丁（十·非段首）、待·己（限 10）免；rc 红', not ok
          and any(l.startswith('⛔ 乙') for l in L) and any(l.startswith('⛔ 待·戊') for l in L)
          and not any(('丙' in l or '丁' in l or '己' in l) for l in L[1:]) and '应验 2 法（✓1 ⛔1' in L[0])
        假册['缓'] = [{'id': '乙', '立': 9, '至': 10, '由': '某由之详'}, {'id': '戊', '立': 9, '至': 9, '由': '某由之详'}]
        ok2, L2 = 验(9, root=工, 册=假册, 境_=e, 执=False)
        T('④之二 缓（≤三章）之内 → ⚠ 不拦', ok2 and any(l.startswith('⚠ 乙') and '缓至 10' in l for l in L2))
        假册['缓'] = []
        开L = 开(9, 工, 假册, 执=False)
        T('④之三 --开：≤10 行、列待之到期与应验之法（开时之证零网先验）', len(开L) <= 10 and any('待·戊' in l for l in 开L) and any('甲' in l for l in 开L))
        多 = {'法': [全({'id': '法%d' % i, '名': 'x', '据': 'x', '起': 9, '时': '封前', '证': [{'档': 'a'}]}) for i in range(20)], '待': []}
        T('④之四 --开 法多 → 截於十行、末行「另 N 法」', len(开(9, 工, 多, 执=False)) == 10 and '另 12 法' in 开(9, 工, 多, 执=False)[-1])
    finally:
        shutil.rmtree(t, ignore_errors=True)
    # ⑤量：真费账（406—410 有数）
    q = 章量(410)
    T('⑤量：410 之费、主环之占、造之占、缓存读之占俱取得（费账＋复盘按类）', q.get('W') == 'W71' and q.get('费', 0) > 30
      and 0 < (q.get('主环占') or 0) < 0.2 and 0.3 < (q.get('造占') or 0) < 1 and 0.5 < (q.get('缓存读占') or 0) < 1)
    # ⑥接线（⛔悄悄拆）
    try:
        封 = open(os.path.join(ROOT, '工具', '封版.py'), encoding='utf-8').read()
        走 = open(os.path.join(ROOT, '工具', '自走.py'), encoding='utf-8').read()
        测 = open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
        import 封版 as _封
        T('⑥接线：封版 --前 带 --前 跑之（N≥411）、--後 之闸 N≥411 含之而 410 ⛔；自走【判】起 印 --开；全测二格、负测入读者可见之闸',
          "'法用之守.py'), '--验', str(n), '--前'" in 封 and [x[0] for x in _封.後之闸(411)][:2] == ['囤灰闸', '法用之守']
          and '法用之守' not in [x[0] for x in _封.後之闸(410)] and '法用之守.开(下)' in 走
          and "('负测·法用之守', chk_fayong_neg)" in 测 and "('法用之守', chk_fayong)" in 测
          and "'负测·法用之守'" in 测.split('读者可见之闸 = {')[1].split('}')[0])
        T('⑥之二 自走之首（前哨）印 报之读（一取·≤三行）——问题早见', '出 += 法用之守.报之读()' in 走.split('def 前哨():')[1].split('\ndef ')[0])
    except Exception as ex:
        T('⑥接线读不得：%s' % ex, False)
    # ⑦回放（真料·406—410）：autopush 之证五章俱红——真败（gh：章-406—410 autopush 俱 failure），⛔空跑
    放 = 回放(406, 410)
    for n in range(406, 411):
        print('    回放 %d：' % n + '｜'.join(l[:70] for l in 放[n][0]))
    T('⑦回放 406—410：「推闸交GitHub」之证（报/推/章-N.json）五章俱 ⛔；时界＝立时（2026-10-27 00:00 UTC·当场算）',
      all(放[n][1] == '⛔' for n in range(406, 411)) and 立时 == calendar.timegm((2026, 10, 27, 0, 0, 0)))
    T('⑦之二 回放非一刀红：诸章另有 ✓ 之法（复盘简式、每章一进、防失稿三锁 等）', all(
        sum(1 for l in 放[n][0] if l.startswith('✓')) >= 3 for n in range(406, 411)))
    e410 = 境(411, ROOT, 史版=封提交(410, ROOT), 史至=(封时(410, ROOT) or 0) + 86400 * 3, 取=False, 承=False)
    T('⑦之三 而「主枝含章-N」之 git 证於回放俱 ✓——只验主枝即空跑（沙盒兜底推掩了 autopush 之败），故须 报', all(
        验证({'git': '含', '甲': '章-%d' % n, '乙': '{主枝}'}, e410)[0] == '✓' for n in range(406, 411)))
    自测_执(T, 全)
    自测_核(T, 全)
    ok = sum(R)
    print('── 负测·法用之守 %d/%d %s ──' % (ok, len(R), '全通' if ok == len(R) else '未过'))
    return ok == len(R)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--验' in a and a.index('--验') + 1 < len(a) and a[a.index('--验') + 1].isdigit():
        n = int(a[a.index('--验') + 1])
        if n < 起章:
            print('✓ 法用之守 --验 %d：N≤%d ⛔验（%d 起索证）' % (n, 起章 - 1, 起章)); sys.exit(0)
        ok, L = 验(n, '--前' in a)
        print('\n'.join(L[1:] + L[:1]))           # 末行为总（封版取末行）
        sys.exit(0 if ok else 1)
    if '--开' in a and a.index('--开') + 1 < len(a) and a[a.index('--开') + 1].isdigit():
        print('\n'.join(开(int(a[a.index('--开') + 1])))); sys.exit(0)
    if '--册' in a:
        L = 册印()
        print('\n'.join(L)); sys.exit(0 if L[-1].startswith('✓') else 1)
    if '--报' in a and '--首' in a:      # 会话开头之钩印之（一行·⛔崩：印不出即 ⚠ 一行、rc 0）
        print(报首()); sys.exit(0)
    if '--报' in a:
        ok, L = 报()
        print('\n'.join(L)); sys.exit(0 if ok else 1)
    if '--未行' in a:
        if '--降' in a:
            sys.exit(降底())
        册 = 读册()
        数, 分 = 未行(ROOT, 册)
        print(未行之印(数, 分, 册)); sys.exit(1 if 未行之判(数, 册)[0] == '⛔' else 0)
    if '--废' in a:                    # 每废：今之树（尽否）与其「在」之笔（去证真红否）——合流之段校去证用之
        册 = 读册()
        红, 黄 = 验废(册, 盘(ROOT), None)
        在红, 在行 = 验在(册)
        for x in 册.get('废') or []:
            今 = [语 for 态, 语 in (验去证(c, 盘(ROOT)) for c in x.get('去证') or []) if 态 != '✓']
            print('%s %s（%s）：今%s' % ('✓' if not 今 else '⛔', x['id'], '待合 %s' % x['待合'] if x.get('待合') else '已行',
                                    '已除尽' if not 今 else '尚在 %d：%s' % (len(今), '；'.join(今)[:200])))
        print('\n'.join('  ' + l for l in 在行))
        print('%s 废 %d：今未除 %d｜去证空验 %d' % ('✓' if not 红 and not 在红 else '⛔', len(册.get('废') or []), len(红), len(在红)))
        sys.exit(0 if not 红 and not 在红 else 1)
    if '--写者' in a:                  # 诸写（今之树，或 --写者 <版>：以今之写者册回放史之树）
        i = a.index('--写者')
        版 = a[i + 1] if len(a) > i + 1 and not a[i + 1].startswith('-') else None
        红, 诸 = 验写者(盘(ROOT, 版), 读写者册())
        for w in 诸:
            print('  %s %s:%s（%s）%s「%s」%s' % ('·' if w.get('族') == '演' else '⛔' if w.get('红') else '✓', w['档'], w['行'], w['者'],
                                             w['作'], w['靶'], '→ ' + str(w.get('族')) if w.get('族') else ''))
        print('\n'.join(红))
        print('%s 写者唯一%s：推 %d 处、红 %d' % ('✓' if not 红 else '⛔', '（%s 之树）' % 版 if 版 else '', len(诸), len(红)))
        sys.exit(0 if not 红 else 1)
    if '--报读' in a:
        L = 报之读(顶=999)
        print('\n'.join(L) if L else '✓ 备份/报 无未消之坏报')
        sys.exit(1 if any(l.startswith('⛔') for l in L) else 0)
    if '--回放' in a:
        i = a.index('--回放')
        n0 = int(a[i + 1]); n1 = int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else n0
        for n, (L, _) in 回放(n0, n1).items():
            print('── 回放 第%d章 ──' % n)
            print('\n'.join('  ' + l for l in L))
        sys.exit(0)
    print(__doc__); sys.exit(2)
