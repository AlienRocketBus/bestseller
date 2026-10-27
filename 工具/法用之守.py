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
用法：
  python3 工具/法用之守.py --验 N [--前]     # 封版之验（封版 --前 带 --前：记席之前·阶後之证免）；红 rc=1
  python3 工具/法用之守.py --开 N            # 开章：本章须用之法 → 其证（≤10 行；自走於【判】起印之）
  python3 工具/法用之守.py --册              # 印册、量之势、待
  python3 工具/法用之守.py --报              # 全测之格（只报）：完备、册之形、逾限之待
  python3 工具/法用之守.py --回放 406 410    # 以史回放（立 ≤ N；盘取其章封版之提交、跑取 版本/第N章/_器之迹.md）
  python3 工具/法用之守.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, glob, time, subprocess, calendar

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
    for k, v in (('{N-1}', n - 1), ('{N+1}', n + 1), ('{段末}', b + 9), ('{段-1}', b - 1), ('{段}', b), ('{N}', n), ('{主枝}', 主枝)):
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

    def 有(self, 式):
        if self.版 is None:
            return sorted(os.path.relpath(p, self.root) for p in glob.glob(os.path.join(self.root, 式)))
        if self._诸 is None:
            rc, o = _git(self.root, 'ls-tree', '-r', '--name-only', self.版)
            self._诸 = o.split('\n') if rc == 0 else []
        r = _式(式)
        return [p for p in self._诸 if r.match(p)]

    def 读(self, p):
        if self.版 is None:
            try:
                return open(os.path.join(self.root, p), encoding='utf-8').read()
            except Exception:
                return None
        rc, o = _git(self.root, 'show', '%s:%s' % (self.版, p))
        return o if rc == 0 else None


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
            for l in (o.strip().split('\n') if rc == 0 and o.strip() else []):
                rc2, t = _git(self.root, 'show', '%s:_器之迹.jsonl' % l.split()[0])
                for x in (t.split('\n') if rc2 == 0 else []):
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
def 章量(n, root=ROOT):
    """→ {W, 费, 主环, 主环占, 造占, 缓存读占}（缺即无其键）。费＝该章 W 之诸行（⛔主会话），造＝复盘「按类」之造。"""
    try:
        行 = json.load(open(os.path.join(root, '设定', '费账.json'), encoding='utf-8')).get('行', [])
    except Exception:
        return {}
    d, 费, 主, 读, 全 = {}, 0.0, 0.0, 0, 0
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
    if not d:
        return {}
    d.update(费=round(费, 2), 主环=round(主, 2), 主环占=round(主 / 费, 3) if 费 else None,
             缓存读占=round(读 / 全, 3) if 全 else None)
    造 = None
    for p in glob.glob(os.path.join(root, '设定', '复盘', '*_%s_*.md' % d['W'])):
        try:
            v = [float(x) for x in re.findall(r'(?m)^\s*造\s+\$\s*([\d.]+)', open(p, encoding='utf-8').read())]
        except Exception:
            v = []
        if v:
            造 = (造 or 0) + sum(v)
    if 造 is not None and 费:
        d['造占'] = round(造 / 费, 3)
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
            键 = re.split(r'[（(]', 格[0].replace('*', ''), 1)[0].strip()
            出.append((键, l))
    return 出


def 完备(册, root=ROOT):
    """→ (红[], 黄[])。"""
    红, 黄 = [], []
    法, 待 = 册.get('法') or [], 册.get('待') or []
    ids = [x.get('id') for x in 法 + 待]
    for i in set(ids):
        if ids.count(i) > 1:
            红.append('⛔ 册坏：id 重 %s' % i)

    def 验式(c, 名):
        if not isinstance(c, dict) or not any(k in c for k in 证之键):
            红.append('⛔ 册坏：%s 之证不识 %s' % (名, json.dumps(c, ensure_ascii=False)[:60]))
            return
        for y in c.get('或') or []:
            验式(y, 名)
        if '若' in c:
            验式(c['若'], 名); 验式(c.get('则'), 名)
        if c.get('git') and c['git'] not in ('含', '改', '枝'):
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
    return 红, 黄


# ───────── 验 ─────────
def 缓之(册, i, n):
    for x in 册.get('缓') or []:
        if x.get('id') == i and x.get('立', 0) <= n <= x.get('至', -1):
            return x
    return None


def 验(n, 前=False, root=ROOT, 册=None, 境_=None):
    """→ (ok, 诸行)。"""
    册 = 册 or 读册(root)
    e = 境_ or 境(n, root, 前)
    红, 黄 = 完备(册, root)
    行, 计 = [], {'✓': 0, '⛔': 0, '⚠': 0}
    应 = [x for x in 册.get('法') or [] if 当验(x, n)]
    for x in 应:
        态, 果 = 验法(x, e)
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
        '✓' if ok else '⛔', n, '·前' if 前 else '', len(应), 计['✓'], 计['⛔'], 计['⚠'], 待到, 待红, '✓' if not 红 else '⛔%d' % len(红))
    return ok, [头] + 红 + 行 + 黄


def _据短(s):
    m = re.search(r'§[一二三四五六七八九十]+[.\d]*', s or '')
    return m.group(0) if m else (s or '')[:12]


def 开(n, root=ROOT, 册=None):
    """开章：本章须用之法 → 其证（≤10 行）。开时之证零网先验（档、钩、跑）；余只列。"""
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
    序 = {t: i for i, t in enumerate(时们)}
    for x in sorted((x for x in 册.get('法') or [] if 当验(x, n)), key=lambda x: (-int(x.get('立', 0)), 序.get(x['时'], 9))):
        标 = '·'
        if e and x['时'] == '开' and not any(('报' in c or 'git' in c) for c in x.get('证') or []):
            标 = {'✓': '✓', '⛔': '⛔'}.get(验法(x, e)[0], '·')
        项.append('%s %s → %s' % (标, x['id'], 填(x.get('示') or '；'.join(_示证(c) for c in x.get('证') or []), n)[:50]))
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
    出 += 红 + 黄
    出.append('%s 完备：总章§八 %d 条、方法账 %s 起 %d 行俱有据' % ('✓' if not 红 else '⛔', len(总章之八(root)), 立日, len(法账之新行(root))) if not 红 else '⛔ 完备未过 %d 处' % len(红))
    return 出


def 末封(root=ROOT):
    rc, o = _git(root, 'log', '-1', '--format=%s', '-E', '--grep=（造式二代·封版#[0-9]+）', 'HEAD')
    m = re.search(r'封版#(\d+)', o or '')
    return int(m.group(1)) if m else 0


def 报(root=ROOT):
    """全测之格：完备、册之形、逾限之待（末封之章 ≥ 限而无证）。零网。"""
    册 = 读册(root)
    红, 黄 = 完备(册, root)
    末 = 末封(root)
    逾 = []
    if 末:
        e = 境(末, root, 取=False, 承=False)
        for x in 册.get('待') or []:
            if 末 >= x['限'] and 验法(x, e)[0] == '⛔' and not 缓之(册, x['id'], 末):
                逾.append('⛔ 待逾限：%s（限 %d，已封至 %d）' % (x['id'], x['限'], 末))
    ok = not 红 and not 逾
    return ok, 红 + 逾 + 黄 + ['%s 法用之守·报：法 %d、待 %d；完备 %s；逾限之待 %d（已封至 %d）' % (
        '✓' if ok else '⛔', len(册['法']), len(册.get('待') or []), '✓' if not 红 else '⛔%d' % len(红), len(逾), 末)]


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


# ───────── 自测 ─────────
def 自测():
    import tempfile, shutil
    R = []

    def T(名, 条):
        R.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

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
            '# 方法账\n| 件 | 法 |\n|---|---|\n| D6 收口（1008） | x |\n| 新法甲（1027） | y |\n| 净重对表（2610字） | 非日之四数⛔认作日 |\n\n'
            '## 升级链\n| 件 | 法 | 费 | 较旧 | 日 | 判 |\n|---|---|---|---|---|---|\n| W1·第9章 | 所废：a | $1 | — | 1024 | 取 |\n'
            '| W2·第10章 | 所废：b | $1 | — | 1028 | 取 |\n| W3·第11章 | 所废：c 法用#乙 | $1 | — | 0105 | 取 |\n')
        假 = {'法': [{'id': '甲', '名': '甲', '据': '总章 §八.1', '起': 9, '时': '开', '证': [{'档': 'a.md'}]},
                    {'id': '乙', '名': '乙', '据': '总章 §八.2；设定/方法账.md 新法甲', '起': 9, '时': '开', '证': [{'档': 'b.md'}]}], '待': []}
        红2, _ = 完备(假, t)
        T('②完备：§八.3 无据 → 法立无证；方法账 1028 之行（W2）无据 → 红；1024 之行免；「法用#乙」与「方法账.md 新法甲」认；「（2610字）」非日⛔红', any('§八.3' in x for x in 红2)
          and any('W2·第10章' in x for x in 红2) and not any('W1' in x for x in 红2) and not any('W3' in x for x in 红2)
          and not any('新法甲' in x for x in 红2) and len(红2) == 2)
        假['法'].append({'id': '丙', '名': '丙', '据': '§八.3；设定/方法账.md W2', '起': 9, '时': '开', '机证不能': True, '由': '短'})
        红3, _ = 完备(假, t)
        T('②之二 机证不能须写由（⛔短于八字）；W2 由 据「方法账.md W2」认', any('机证不能而无由：丙' in x for x in 红3) and not any('W2' in x for x in 红3))
        假['法'][2]['由'] = '纯理：无章之迹可数，其守在某器'
        假['法'].append({'id': '丁', '名': '丁', '据': 'x', '起': 9, '时': '开', '机证不能': True, '由': '纯理：无章之迹可数之由'})
        红4, _ = 完备(假, t)
        T('②之三 机证不能 2／4 逾四之一 → 红', any('逾四之一' in x for x in 红4))
        假['法'] = 假['法'][:3]
        假['法'].append({'id': '戊', '名': '戊', '据': 'x', '起': 9, '时': '午', '证': [{'怪': 1}]})
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
        假册 = {'法': [{'id': '甲', '名': '甲', '据': 'x', '起': 9, '时': '封前', '证': [{'档': '版本/第{N}章/_轮记.md'}]},
                      {'id': '乙', '名': '乙', '据': 'x', '起': 9, '时': '封後', '证': [{'报': '推/章-7'}]},
                      {'id': '丙', '名': '丙', '据': 'x', '起': 10, '时': '开', '证': [{'档': '无.md'}]},
                      {'id': '丁', '名': '丁', '据': 'x', '起': 9, '时': '十', '证': [{'档': '无.md'}]}],
                '待': [{'id': '戊', '名': '戊', '据': 'x', '限': 9, '证': [{'档': '无.md'}], '示': '记之'},
                      {'id': '己', '名': '己', '据': 'x', '限': 10, '证': [{'档': '无.md'}]}]}
        ok, L = 验(9, root=工, 册=假册, 境_=e)
        T('④验 9：乙（报之果败）⛔、待·戊（限 9）⛔；丙（起 10）、丁（十·非段首）、待·己（限 10）免；rc 红', not ok
          and any(l.startswith('⛔ 乙') for l in L) and any(l.startswith('⛔ 待·戊') for l in L)
          and not any(('丙' in l or '丁' in l or '己' in l) for l in L[1:]) and '应验 2 法（✓1 ⛔1' in L[0])
        假册['缓'] = [{'id': '乙', '立': 9, '至': 10, '由': '某由之详'}, {'id': '戊', '立': 9, '至': 9, '由': '某由之详'}]
        ok2, L2 = 验(9, root=工, 册=假册, 境_=e)
        T('④之二 缓（≤三章）之内 → ⚠ 不拦', ok2 and any(l.startswith('⚠ 乙') and '缓至 10' in l for l in L2))
        假册['缓'] = []
        开L = 开(9, 工, 假册)
        T('④之三 --开：≤10 行、列待之到期与应验之法（开时之证零网先验）', len(开L) <= 10 and any('待·戊' in l for l in 开L) and any('甲' in l for l in 开L))
        多 = {'法': [{'id': '法%d' % i, '名': 'x', '据': 'x', '起': 9, '时': '封前', '证': [{'档': 'a'}]} for i in range(20)], '待': []}
        T('④之四 --开 法多 → 截於十行、末行「另 N 法」', len(开(9, 工, 多)) == 10 and '另 12 法' in 开(9, 工, 多)[-1])
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
    if '--报' in a:
        ok, L = 报()
        print('\n'.join(L)); sys.exit(0 if ok else 1)
    if '--回放' in a:
        i = a.index('--回放')
        n0 = int(a[i + 1]); n1 = int(a[i + 2]) if len(a) > i + 2 and a[i + 2].isdigit() else n0
        for n, (L, _) in 回放(n0, n1).items():
            print('── 回放 第%d章 ──' % n)
            print('\n'.join('  ' + l for l in L))
        sys.exit(0)
    print(__doc__); sys.exit(2)
