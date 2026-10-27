#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""段序之守（1023 立·作者令「设计剧情十章 → 写完这十章 → 大审这十章；定为绝对完美执行的机制，严格按此执行」）——PreToolUse 钩（Workflow）。

【其律】段＝自 381 起每十章（411—420、421—430……）；自 411 之段起严守三序，跳一步即派不出：
  ①审毕方定：开下一段之剧情庭（剧情庭.js，名／题带「势_第S段」）须上一段已大审（大审之册至第 S-1 章在），
    且其题须引 `设定/大审_至第{S-1}章.md`——审出之孤钩、大进、二稿交设计一次造进去（⛔写完再补）。
  ②定毕方写：派第 N 章之造章（造章.js、其包裹、内联调之）须本段剧情庭之势在（设定/剧情庭_势_第S段.md），
    且本段段案十章俱全（S—S+9 每章有 重、魂路）、上一段已大审。
  ③段末方审：大审.js 之 止 ≥410 者须係段末（410、420……），且 起 ＝上一册之止＋1（⛔重审、⛔漏审）。
  ④停则俱停：作者暂停令在（工具/暂停令.py·含「待」之到点）→ 剧情庭、造章、大审俱拦（args.例外 带作者所许之件者放）。
  ⑤欠则⛔写（1027 执行之审 #20① #8② #6·作者令「已定之决……须全部执行起来」）——派第 N 章之造章（N≥411）另验三样，各零 token：
    甲·账限：`账限哨.印(ROOT, N)` 有到期之条即拦（瑕疵总账之限到即先治·1021 作者问「为什么还是我自己发现」）；
    乙·还账：最新大审之册凡「已挂·限M（还账·器施）」而 M≤N 者未还即拦（⛔新章压在已写章之 fatal 上·410 大审 #1 #3—#11）；
    丙·料全：`造式验.py N --料` 红即拦，_料.md 旧於开镜卡（卡改而料未重出）亦拦（坑⑬：料缺已定之细）。
  410 係过渡：审 408—410（401—407 已於 407 审过，⛔重付），自 411 之段起每段之审恰十章。
【其由】大审旧逢 7 封後开（387、397、407），与段（剧情之造以十章为一段）错开三章：审出之病只能写完再补，
  而下一段之造读不到它。今段与审同界：一段写完即审，审之所得即下一段之料。
  非剧情庭／造章／大审之 workflow、他器一概放；入坏、出错 → 放（本钩守序，⛔挡书於器病）。
用法：钩自 stdin 取 JSON；`python3 工具/段序之守.py --自测`
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起行 = 411                      # 自此段起严守（1023 作者令）；410 及其前之章照旧


def 段首(n):
    return 381 + (n - 381) // 10 * 10


def _上审():
    import 大审
    cs = 大审.诸册()
    return cs[-1][0] if cs else 0


def _势在(S):
    return os.path.exists(os.path.join(ROOT, '设定', '剧情庭_势_第%d段.md' % S))


def _段案缺(S):
    """→ S—S+9 之中段案缺（无 重 或 魂路）之章［］。"""
    import 章料
    缺 = []
    for n in range(S, S + 10):
        t = 章料.段案行(n, ROOT) or ''
        if not (re.search(r'^- 重：(轻|中|重)\s*$', t, re.M) and re.search(r'^- 魂路：\S', t, re.M)):
            缺.append(n)
    return 缺


def _题文(p):
    try:
        p = p if os.path.isabs(p) else os.path.join(ROOT, p)
        return open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return None


def _参(入):
    参 = 入.get('tool_input') or {}
    a = 参.get('args')
    if isinstance(a, str):
        try:
            a = json.loads(a)
        except ValueError:
            a = {}
    return 参, (a if isinstance(a, dict) else {})


def _器(参):
    """→ 'pt'（剧情庭）、'zz'（造章）、'ds'（大审）或 ''。scriptPath 之名为准；内联者看其文所调。"""
    sp = os.path.basename(str(参.get('scriptPath') or ''))
    for 名, k in (('剧情庭.js', 'pt'), ('造章.js', 'zz'), ('大审.js', 'ds')):
        if sp == 名:
            return k
    return ''


def _停():
    try:
        import 暂停令
        在, 由 = 暂停令.在(ROOT)
        return (由 if 在 else ''), 暂停令.许跑   # 1027 W75：开件所销之例外，其件进行中仍许（⛔一例外两处消费）
    except Exception:
        return '', (lambda 件: False)


def _账限(n):
    """→ [由]：瑕疵总账之限压在第 n 章头上者（账限哨·一处判）。读崩 → []（本钩守序，⛔挡书於器病）。"""
    try:
        import 账限哨
        拦, L = 账限哨.印(ROOT, n)
    except Exception:
        return []
    if not 拦:
        return []
    号 = [x.strip().split()[1] for x in L[1:] if x.strip().startswith('⛔') and len(x.strip().split()) > 1]
    return ['瑕疵总账到期 %d 条（%s）——先治或「弃：由」移已治（python3 工具/账限哨.py）' % (len(号), '、'.join(号[:8]))]


def _还账(n):
    """→ [由]：最新大审之册「已挂·限M（…）」而 M≤n 未还者（大审.限於·与开镜卡问七同一读；「入段案」者除外）。"""
    try:
        import 大审
        欠 = [(号, 限) for 号, 限, 裁 in 大审.限於(n) if '入段案' not in 裁]   # 1027 合流（线 E 复核所逮）：⛔只认字面「还账」——「已挂·限M（待撰）」漏之；入段案者归段案
    except Exception:
        return []
    if not 欠:
        return []
    return ['大审还账 %d 笔未还（%s）——册已给原句新句者照册三节出单、python3 工具/还账.py --施 <单.json> 器施（零 token·改单 --施单 禁正文）；须撰者本段之坐撰之；施毕其格改「已治·改单#…」'
            % (len(欠), '、'.join('#%s·限%d' % x for x in 欠[:12]))]


def _料验(n):
    """→ [由]：造式验 --料 之红；_料.md 旧於开镜卡逾一秒亦红（卡改而料未重出）。"""
    import subprocess
    d = os.path.join(ROOT, '版本', '第%d章' % n)
    卡, 料 = os.path.join(d, '_开镜卡.md'), os.path.join(d, '_料.md')
    try:
        p = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '造式验.py'), str(n), '--料'], cwd=ROOT,
                           capture_output=True, text=True, timeout=120, env=dict(os.environ, ZM_STREAM='段序之守'))
    except Exception:
        return []
    由 = []
    if p.returncode != 0:
        由.append('料不全（%s）' % ((p.stdout.strip().split('\n') or [''])[-1][:200]))
    try:
        if os.path.exists(卡) and os.path.exists(料) and os.path.getmtime(卡) - os.path.getmtime(料) > 1:
            由.append('_料.md 旧於开镜卡（卡改而料未重出）——python3 工具/章料.py %d' % n)
    except OSError:
        pass
    return 由


def 判(入, 上审=None, 势在=None, 段案缺=None, 题文=None, 造章之参=None, 停=None, 账限=None, 还账=None, 料验=None):
    """→ (拦否, 由)。诸参供自测注之。"""
    if (入.get('tool_name') or '') != 'Workflow':
        return False, ''
    参, a = _参(入)
    停由, 许 = (停 or _停)()
    if 停由 and (_器(参) or (造章之参 or _造章之参())(参, a)):
        件 = str(a.get('例外') or '')
        if not (件 and 许(件)):
            return True, ('⛔段序之守·暂停：%s——剧情庭、造章、大审俱⛔开；只许零 token 之活。作者令下方解：'
                          'python3 工具/暂停令.py --解 "作者令：……"（作者亲许一件者：暂停令.py --例外 W? "作者令：…"，args 带 例外:\'W?\'）。' % 停由[:160])
    上审 = 上审 or _上审
    势在 = 势在 or _势在
    段案缺 = 段案缺 or _段案缺
    题文 = 题文 or _题文
    k = _器(参)
    if k == 'pt':
        m = re.search(r'势_第(\d+)段', str(a.get('名') or '') + ' ' + str(a.get('题') or ''))
        if not m:
            return False, ''
        S = int(m.group(1))
        if S < 起行:
            return False, ''
        上 = 上审()
        if 上 < S - 1:
            return True, ('⛔段序之守（作者 1023 令「设计十章→写十章→审十章」）：第%d—%d段之剧情庭须上一段先大审——'
                          '大审之册今至第%d章，缺 %d—%d。先：python3 工具/大审.py --包 %d %d → '
                          "Workflow({scriptPath:'工具/席/大审.js', args:{起:%d, 止:%d, 孤钩:…}})（自走印全令）。"
                          % (S, S + 9, 上, 上 + 1, S - 1, 上 + 1, S - 1, 上 + 1, S - 1))
        t = 题文(str(a.get('题') or ''))
        引 = '大审_至第%d章' % (S - 1)
        if t is None or 引 not in t:
            return True, ('⛔段序之守：第%d—%d段剧情庭之题（%s）须引 `设定/%s.md`——上一段大审所得之孤钩、大进、二稿'
                          '交设计一次造进去（⛔写完再补）。题中写明其诸笔与本段如何收之，再开庭。' % (S, S + 9, a.get('题') or '（无题）', 引))
        return False, ''
    if k == 'ds':
        try:
            起, 止 = int(a.get('起')), int(a.get('止'))
        except (TypeError, ValueError):
            return False, ''
        if 止 < 410:
            return False, ''
        上 = 上审()
        if (止 - 380) % 10 != 0:
            return True, ('⛔段序之守：大审之止（%d）须係段末（410、420……）——一段写完即审其十章，⛔段中开审。' % 止)
        if 起 != 上 + 1:
            return True, ('⛔段序之守：大审之起（%d）须接上一册之止（%d）＋1＝%d——⛔重审已审之章（已付之料⛔重付）、⛔漏审。'
                          % (起, 上, 上 + 1))
        return False, ''
    # 造章：直派、包裹、内联俱认（取 续跑之守 之认法）
    x = a if k == 'zz' else (造章之参 or _造章之参())(参, a)
    if not isinstance(x, dict):
        return False, ''
    try:
        n = int(x.get('章'))
    except (TypeError, ValueError):
        return False, ''
    if n < 起行:
        return False, ''
    S = 段首(n)
    由 = []
    上 = 上审()
    if 上 < S - 1:
        由.append('上一段未大审（册至第%d章，缺 %d—%d）' % (上, 上 + 1, S - 1))
    if not 势在(S):
        由.append('本段剧情庭之势不在（设定/剧情庭_势_第%d段.md）' % S)
    缺 = 段案缺(S)
    if 缺:
        由.append('本段段案未十章俱全（缺 %s 之 重／魂路）' % '、'.join(str(c) for c in 缺))
    if 由:
        return True, ('⛔段序之守（作者 1023 令「设计十章→写十章→审十章」）：第%d章属 %d—%d 段，未可动笔——%s。'
                      '序：上段大审 → 剧情庭（题引大审之册）→ 段料 → 段案十章（立、驳、验）→ 写。跑 `python3 工具/自走.py` 照其印。'
                      % (n, S, S + 9, '；'.join(由)))
    # ⑤欠则⛔写（1027）：账限、还账、料全——序已齐方验（⛔序未齐时多跑一器）
    欠 = (账限 or _账限)(n) + (还账 or _还账)(n) + (料验 or _料验)(n)
    if 欠:
        return True, ('⛔段序之守·欠（1027 作者令「已定之决、作者之令、要避之坑须全部执行起来」）：第%d章未可动笔——%s。'
                      '先清欠，再派（跑 `python3 工具/自走.py` 照其印）。' % (n, '；'.join(欠)))
    return False, ''


def _造章之参():
    try:
        import 续跑之守
        return 续跑之守.派造章之参
    except Exception:
        return lambda 参, a: None


def 自测():
    import tempfile
    import subprocess
    r = []

    def T(名, 条):
        r.append(bool(条))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)

    W = lambda sp, **a: {'tool_name': 'Workflow', 'tool_input': {'scriptPath': sp, 'args': a}}
    无停 = lambda: ('', lambda 件: False)
    _判 = globals()['判']

    无欠 = lambda n: []

    def 判(入, **k):                                # 诸测默认「无暂停」「无欠」（⛔读真仓之暂停令、瑕疵总账、大审之册、料）
        k.setdefault('停', 无停)
        for 键 in ('账限', '还账', '料验'):
            k.setdefault(键, 无欠)
        return _判(入, **k)
    题有 = lambda p: '…收 设定/大审_至第410章.md 之孤钩三笔…'
    题无 = lambda p: '只写势'
    全 = lambda S: []
    缺三 = lambda S: [418, 419, 420]
    在 = lambda S: True
    不在 = lambda S: False
    审至 = lambda n: (lambda: n)
    # ①审毕方定
    PT = W('工具/席/剧情庭.js', 题='设定/剧情庭题/势_第411段.md', 名='势_第411段', 式='新')
    T('①上段未审（册至407）而开 411 段剧情庭 → 拦，印大审 408—410', 判(PT, 上审=审至(407), 题文=题有)[0]
      and '起:408, 止:410' in 判(PT, 上审=审至(407), 题文=题有)[1])
    T('①之二 已审至410、题引 大审_至第410章 → 放', not 判(PT, 上审=审至(410), 题文=题有)[0])
    T('①之三 已审而题未引大审之册 → 拦（审之所得须交设计）', 判(PT, 上审=审至(410), 题文=题无)[0])
    T('①之四 401 段（起行之前）之剧情庭 → 放（照旧）', not 判(W('工具/席/剧情庭.js', 名='势_第401段', 题='x'), 上审=审至(397), 题文=题无)[0])
    T('①之五 非势之剧情庭（名题无「势_第S段」）→ 放', not 判(W('工具/席/剧情庭.js', 名='某裁', 题='设定/剧情庭题/某.md'), 上审=审至(0), 题文=题无)[0])
    # ②定毕方写
    ZZ = lambda n: W('工具/席/造章.js', 章=n, 重='重', 魂路=['换账'])
    T('②411：审至410、势在、段案十章全 → 放', not 判(ZZ(411), 上审=审至(410), 势在=在, 段案缺=全)[0])
    拦, 由 = 判(ZZ(411), 上审=审至(407), 势在=不在, 段案缺=缺三)
    T('②之二 未审、势不在、段案缺三章 → 拦，三由俱印', 拦 and '未大审' in 由 and '势不在' in 由 and '418、419、420' in 由)
    T('②之三 段案只缺末章（十章未全）→ 拦（先定十章再写）', 判(ZZ(415), 上审=审至(410), 势在=在, 段案缺=lambda S: [420])[0])
    T('②之四 410 及其前之章 → 放（照旧）', not 判(ZZ(410), 上审=审至(397), 势在=不在, 段案缺=缺三)[0])
    T('②之五 包裹（_承.js）、内联调造章 → 照其 args 之章判', 判(W('版本/第411章/_承.js'), 上审=审至(407), 势在=在, 段案缺=全,
                                                    造章之参=lambda 参, a: {'章': 411})[0]
      and not 判({'tool_name': 'Workflow', 'tool_input': {'script': 'return 1'}}, 上审=审至(407), 势在=在, 段案缺=全, 造章之参=lambda 参, a: None)[0])
    # ⑤欠则⛔写（1027 执行之审 #20① #8② #6）：账限、还账、料全——各一欠即拦；俱无即放；序未齐时⛔验欠（先印序之由）
    齐 = dict(上审=审至(410), 势在=在, 段案缺=全)
    拦账, 由账 = 判(ZZ(411), 账限=lambda n: ['瑕疵总账到期 1 条（X52）'], **齐)
    拦还, 由还 = 判(ZZ(411), 还账=lambda n: ['大审还账 10 笔未还（#1·限411）'], **齐)
    拦料, 由料 = 判(ZZ(411), 料验=lambda n: ['料不全（⛔ 第411章之料不全：无章料）'], **齐)
    T('⑤甲乙丙 账限之欠、大审还账之欠、料不全 → 各拦，印其由与「段序之守·欠」', 拦账 and 'X52' in 由账 and 拦还 and '#1·限411' in 由还
      and 拦料 and '料不全' in 由料 and all('段序之守·欠' in x for x in (由账, 由还, 由料)))
    T('⑤之二 三样俱无欠 → 放（放行之反例）', not 判(ZZ(411), **齐)[0])
    _叫 = []
    判(ZZ(411), 上审=审至(407), 势在=不在, 段案缺=缺三, 账限=lambda n: _叫.append(n) or ['x'])
    T('⑤之三 序未齐 → 先印序之由（⛔验欠、⛔多跑一器）', _叫 == [])
    T('⑤之四 410 及其前之章 → ⛔验欠（照旧）', not 判(ZZ(410), 上审=审至(397), 账限=lambda n: ['x'], 还账=lambda n: ['x'], 料验=lambda n: ['x'])[0])
    try:   # ⑤之五 回灌旧树：db52f247 之 大审_至第410章.md（#1 #3—#11「已挂·限411（还账·器施）」）→ 派 411 欠 10 笔；派 410 → 无（限未到·放行之反例）
        import 大审 as _大5
        _旧5 = subprocess.run(['git', 'show', 'db52f247:设定/大审_至第410章.md'], cwd=ROOT, capture_output=True, text=True)
        if _旧5.returncode == 0:
            _目5 = _大5.册目
            with tempfile.TemporaryDirectory() as _d5:
                open(os.path.join(_d5, '大审_至第410章.md'), 'w', encoding='utf-8').write(_旧5.stdout)
                _大5.册目 = _d5
                try:
                    _欠411, _欠410 = _还账(411), _还账(410)
                finally:
                    _大5.册目 = _目5
            T('⑤之五 回灌旧树（db52f247 之 410 大审之册）：派 411 → 还账之欠 10 笔（#1、#3—#11）；派 410 → 无',
              len(_欠411) == 1 and '10 笔' in _欠411[0] and '#1·限411' in _欠411[0] and '#2·' not in _欠411[0] and _欠410 == [])
        else:
            print('  · ⑤之五 旧树不在（浅克隆）——略')
        T('⑤之六 真读：账限、还账、料验之读不崩（今之欠由真仓定，⛔钉其数）', all(isinstance(f(411), list) for f in (_账限, _还账, _料验)))
    except Exception as e:
        T('⑤之五 真读崩：%s' % e, False)
    # ③段末方审
    DS = lambda a, b: W('工具/席/大审.js', 起=a, 止=b, 孤钩=[])
    T('③审 408—410（过渡）→ 放；审 411—420 → 放', not 判(DS(408, 410), 上审=审至(407))[0] and not 判(DS(411, 420), 上审=审至(410))[0])
    T('③之二 止非段末（417）→ 拦（⛔段中开审）', 判(DS(408, 417), 上审=审至(407))[0])
    T('③之三 起不接上一册（重审 401—410、漏审 412—420）→ 拦', 判(DS(401, 410), 上审=审至(407))[0] and 判(DS(412, 420), 上审=审至(410))[0])
    T('③之四 止 <410 之旧审 → 放', not 判(DS(398, 407), 上审=审至(397))[0])
    T('④他器、非 Workflow → 放', not 判({'tool_name': 'Bash', 'tool_input': {'command': 'ls'}})[0]
      and not 判(W('工具/席/大升级.js', 起=1), 上审=审至(0))[0])
    # ④停则俱停
    有停 = lambda: ('暂停令在（作者令：审完即停）', lambda 件: 件 == 'W70')
    T('④之二 暂停令在：剧情庭、造章、大审俱拦（齐备亦拦）', all(_判(x, 停=有停, 上审=审至(410), 势在=在, 段案缺=全, 题文=题有)[0]
                                                  for x in (PT, ZZ(411), DS(411, 420))))
    T('④之三 暂停之中作者所许之件（args.例外）→ 放；非其件 → 拦', not _判(W('工具/席/剧情庭.js', 题='设定/剧情庭题/势_第411段.md', 名='势_第411段', 例外='W70'),
                                                                停=有停, 上审=审至(410), 题文=题有)[0]
      and _判(W('工具/席/剧情庭.js', 题='设定/剧情庭题/势_第411段.md', 名='势_第411段', 例外='W69'), 停=有停, 上审=审至(410), 题文=题有)[0])
    T('④之四 暂停之中他器（非庭非章非审）→ 放', not _判(W('工具/席/大升级.js', 起=1), 停=有停)[0])
    T('④之五 暂停之许用 暂停令.许跑（1027 W75 实踩：工作流账 --开 销例外，其件进行中之 Workflow 仍许；⛔一例外两处消费）',
      '暂停令.许跑' in open(os.path.abspath(__file__), encoding='utf-8').read().split('def 自测')[0])
    # ⑤真接得上：段案、势、大审之册之读
    try:
        T('⑤真读：401 段段案十章俱全、势在；大审之册读得出', _段案缺(401) == [] and _势在(401) and _上审() >= 407)
    except Exception as e:
        T('⑤真读崩：%s' % e, False)
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], input='{坏', capture_output=True, text=True,
                       env=dict(os.environ, ZM_STREAM='自测'))
    T('⑥入坏 → rc=0', p.returncode == 0)
    p = subprocess.run([sys.executable, os.path.abspath(__file__)], input=json.dumps(DS(408, 417)), capture_output=True, text=True,
                       env=dict(os.environ, ZM_STREAM='自测'))
    T('⑥之二 真跑：段中开审 → rc=2、stderr 印段序之守', p.returncode == 2 and '段序之守' in p.stderr)
    try:
        import 大审 as _大
        T('⑧大审.到期：410（上407）→410；409、417 → 无；420、421（上410）→420；397（上387）→397',
          (_大.到期(410, 407), _大.到期(409, 407), _大.到期(417, 410), _大.到期(420, 410), _大.到期(421, 410), _大.到期(397, 387))
          == (410, None, None, 420, 420, 397))
    except Exception as e:
        T('⑧大审.到期 崩：%s' % e, False)
    try:
        st = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8'))
        钩 = [e for e in (st.get('hooks') or {}).get('PreToolUse', []) for h in e.get('hooks', []) if '段序之守' in h.get('command', '')]
        T('⑦settings 之 PreToolUse 挂本器，matcher 认 Workflow', bool(钩) and re.fullmatch(钩[0]['matcher'], 'Workflow') is not None)
    except Exception as e:
        T('⑦settings 读不出：%s' % e, False)
    ok = sum(r)
    print('── 负测·段序之守 %d/%d %s ──' % (ok, len(r), '全通' if ok == len(r) else '未过'))
    return ok == len(r)


if __name__ == '__main__':
    if '--自测' in sys.argv[1:]:
        sys.exit(0 if 自测() else 1)
    try:
        入 = json.load(sys.stdin)
        拦, 由 = 判(入)
    except Exception:
        sys.exit(0)
    if 拦:
        print(由, file=sys.stderr)
        sys.exit(2)
    sys.exit(0)
