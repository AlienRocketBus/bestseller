#!/usr/bin/env python3
"""费审（1009 立·作者令「每次都要找到问题所在，让虫洞之法不断完美进化」；同日作者令「计算方式要认认真真弄，⛔再犯错——每次计算都要精准」）
——零 token 审一回工作流（或主会话）之费。

【量法（1009 定·精准之律）】一回 API 之 usage 有四项，逐回取、按 message.id 去重（坑⑯）：
  新入 input_tokens｜缓存建 cache_creation_input_tokens｜缓存读 cache_read_input_tokens｜产出 output_tokens
  · **全量** ＝ 四项之和，逐回相加——模型真读真写之 token 总数。
  · **美元** ＝ 逐回照 `设定/价目.json`（官方价目页，注其源与抓取之日）精算：按该回之模型取价；缓存写分 5m／1h 两档
    （usage.cache_creation 之 ephemeral_5m／ephemeral_1h）；缓存读按该模型之倍数（Opus 5.5 为 0.05×，非 0.1×）；产出含思考；
    inference_geo=us ×1.1；speed=fast 用快速之价；web_search 每次 0.01。**比费以美元为准**（与上回比、资源分配之占）。
    价目里没有之模型、或缓存写两档之和对不上总数者，即报「未价」「不符」，⛔当零、⛔隐。
    此为「API 标价」之美元——走订阅者实付按订阅计，本数是用量之标价折算。
    （1009 淘汰：①逐行相加〔计重〕②通知之数当实耗③「等效」以 0.1× 计缓存读、1.25× 计一切缓存写——Opus 5.5 之缓存读实 0.05×、本会话之缓存写多是 1h 档 2×。）
  · **末回** ＝ 各席最後一回之（四项之和），Σ 之即工作流通知里之 `subagent_tokens`——
    **它量的是「各席最後背了多大」，⛔是实耗**（不计来回）。380 通知报 570 万，全量约 4.9 亿。坑⑲。
  · **核**：Σ末回 与通知之 subagent_tokens 逐 Run 比，相符方证本器读对了转录（1009 核全：15 个 Run 分毫不差、13 个不符）；
    不符即报，⛔隐。不符之因未尽明：已知续跑之 Run（如 380）通知只计其一段；另有微差（W17 差 0.2%）待查。
【随时记（1009 作者令「任务一完就记，记了就不会算错」）】每个 Run 一完、每件主环之活一完，即 `--记`：
  界面所示之数（通知之 subagent_tokens）与精算之数（美元、四项、全量、末回）同记一行入 `设定/费账.json`，当场核；
  复盘起草时自动补记其 Run。⛔事後凭记忆追算。
【前车】坑⑯：旧审逐行相加，一回 API 拆数行、行行重抄 usage，计重 1.8 倍。坑⑲：方法账之「实耗」取自通知之数，非实耗。

用法：
  python3 工具/费审.py <Run 之目录或 Run ID>   # 每席：来回、工具、四项、全量、美元、末回、构思（首落−席起之分）、构思隔（诸写之最长隔）、撞顶而截之回（max_tokens·1020 X26）；按类合计（美元之占）；与通知核
  python3 工具/费审.py --主 [起 ISO [止 ISO]]     # 主会话（总编辑）一段时间之账（坑⑮：主环每回工具都重发整个上下文）
  python3 工具/费审.py --核全                     # 凡通知有数之 Run，逐一核 Σ末回＝subagent_tokens
  python3 工具/费审.py --记 <Run ID> [名]          # 随时记：一 Run 一行入 设定/费账.json（已记则更新）
  python3 工具/费审.py --记主 <名> <起 ISO> [止 ISO]  # 随时记：一件主环之活一行
  python3 工具/费审.py --记全                     # 费账覆全会话：工作流 Run、非工作流子席、主会话全程
  （精准之证：`python3 工具/费审对拍.py`——结构全异之 SQLite 算器逐单位对拍，并核记录之义）
  python3 工具/费审.py --自测
Run 之目录在 ~/.claude/projects/<proj>/<session>/subagents/workflows/<runId>/。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
类 = [('造', r'执笔|魂|选|合稿|造·'), ('验', r'逻辑审|盲读|读误|防崩|厚之关|抄袭'), ('机器之活', r'定位|机闸|案席|封版|长令席')]
项 = (('新', 'input_tokens'), ('建', 'cache_creation_input_tokens'), ('读', 'cache_read_input_tokens'), ('出', 'output_tokens'))
_价目 = {}


def 价目(root=ROOT):
    if root not in _价目:
        _价目[root] = json.load(open(os.path.join(root, '设定', '价目.json'), encoding='utf-8'))
    return _价目[root]


def 一回之金(model, u, 目):
    """→ (美元, 疑)。疑：None 或一句（未价之模型／缓存写两档对不上）。"""
    新, 建, 读, 出 = (u.get(k, 0) or 0 for _, k in 项)
    if not (新 or 建 or 读 or 出):
        return 0.0, None
    cc = u.get('cache_creation') or {}
    w5, w1 = cc.get('ephemeral_5m_input_tokens'), cc.get('ephemeral_1h_input_tokens')
    疑 = None
    if w5 is None and w1 is None:
        w5, w1 = 建, 0
        if 建:
            疑 = '缓存写无两档之分（按 5m 计）'
    elif (w5 or 0) + (w1 or 0) != 建:
        疑 = '缓存写两档之和 %d ≠ 总 %d' % ((w5 or 0) + (w1 or 0), 建)
    键 = model
    if model == 'claude-haiku-5-5' and 新 + 建 + 读 > 目.get('海酷长档之界', 100000):
        键 = 'claude-haiku-5-5>100k'
    p = 目['模型'].get(键)
    if not p:
        return 0.0, '未价之模型：%s' % model
    p = dict(p)
    if u.get('speed') == 'fast' and model in 目.get('快速', {}):
        f = 目['快速'][model]
        倍读 = 目['缓存倍数']['缓存读'].get(model, 目['缓存倍数']['缓存读']['余'])
        p = {'新入': f['新入'], '产出': f['产出'], '缓存写5m': f['新入'] * 目['缓存倍数']['缓存写5m'],
             '缓存写1h': f['新入'] * 目['缓存倍数']['缓存写1h'], '缓存读': f['新入'] * 倍读}
    金 = (新 * p['新入'] + (w5 or 0) * p['缓存写5m'] + (w1 or 0) * p['缓存写1h'] + 读 * p['缓存读'] + 出 * p['产出']) / 1e6
    金 *= 目.get('地域', {}).get(u.get('inference_geo'), 1.0)
    金 += ((u.get('server_tool_use') or {}).get('web_search_requests', 0) or 0) * 目.get('网搜每次', 0.01)
    return 金, 疑


def 席名(meta):
    d = meta.get('description') or meta.get('label') or ''
    if d.startswith('【最高宗旨'):
        # ★1009：长令诸席之 description 皆是同一段宗旨——取其相位名之，⛔一概算机器之活（380 之定魂属造而被误归）
        相 = meta.get('workflowPhase') or ''
        return ('%s(长令)' % 相) if 相 else '(长令席)'
    return d[:18]


def 审(目录):
    行 = []
    for f in glob.glob(os.path.join(目录, 'agent-*.jsonl')):
        mf = f[:-len('.jsonl')] + '.meta.json'
        if not os.path.exists(mf):
            continue
        行.append(审一(f, 席名(json.load(open(mf, encoding='utf-8')))))
    行.sort(key=lambda r: r['起'])
    return 行


_构思档 = r'起草_[^\s/"\'<>|;&]+_构思\.md'
构思之界 = 5     # 分：首条消息即建构思档（与 Read 料同发）——首落逾此即未守
构思隔之界 = 10  # 分：构思诸写之最长隔（席起至首写、写与写之间）——逾此即在思考里排全章：392—397 二十一回撞 128k 回回在构思首落之前、一回约二十二分

# ★W60·X33⑤（W53 验席所逮）：旧剔 heredoc 之式 `<<…(\w+)….*?\n\1\b`（re.S）连开头那一行之余一并吃掉，
#   故「heredoc 在前、导向在後」之形认不着——真例 391 庚（wf_bc5f1caf-503·10-15 15:03）：
#   `python3 -I - "$S/draft6.md" <<'PYEND' && cp … && cat > 版本/第391章/起草_庚_构思.md <<'ZZEND' && …`。
#   今只剔其体（自下一行至收尾之行），开头那一行之余留下；一行数 heredoc 依次剔（体依次相接）。
_体式 = re.compile(r"(?<!<)<<-?[ \t]*(['\"]?)([A-Za-z_]\w*)\1([^\n]*)\n(?:[^\n]*\n)*?[ \t]*\2\b")


def _剔体(c):
    while True:
        m = _体式.search(c)
        if not m:
            return c
        c = c[:m.start()] + ' ' + m.group(3) + c[m.end():]


def _换变(c):
    """`F=版本/…/起草_戊_构思.md && cat > $F <<'EOF'` 之形（真例 383 戊·wf_db24c946-4a1·10-13 14:24）：简单之赋值代入 $F／${F}。"""
    变 = {m.group(1): m.group(3) for m in
         re.finditer(r'(?:^|[;&|\n(])\s*([A-Za-z_]\w*)=(["\']?)([^\s"\';&|()]+)\2(?=\s|$|[;&|)])', c)}
    return re.sub(r'\$\{?([A-Za-z_]\w*)\}?', lambda m: 变.get(m.group(1), m.group(0)), c) if 变 else c


def 是建构思(x):
    """★1020 W53·X26：一个 tool_use 是否写构思档（起草_<名>_构思.md）。
    认：Write／Edit／MultiEdit 之 file_path；Bash 之 >／>>／tee（先剔 heredoc 之体：体里之字⛔误认；heredoc 在前、导向在後亦认）、
    cp／mv／install 之末参（目的）、sed -i 之末参（W60·X33⑤）。⛔认：读档（cat／head／grep／Read）、cp 之源、体里之字。"""
    if not isinstance(x, dict) or x.get('type') != 'tool_use':
        return False
    i = x.get('input') or {}
    if x.get('name') in ('Write', 'Edit', 'MultiEdit'):
        return bool(re.search(_构思档 + r'$', i.get('file_path') or ''))
    if x.get('name') != 'Bash':
        return False
    c = _换变(_剔体(i.get('command') or ''))
    if re.search(r'(?:>>?|\btee\b(?:\s+-a)?)\s*["\']?[^\s"\'<>|;&]*' + _构思档, c):
        return True
    import shlex
    for 段 in re.split(r'&&|\|\||[;&|\n()]', c):
        try:
            a = shlex.split(段)
        except ValueError:
            a = 段.split()
        while a and re.match(r'[A-Za-z_]\w*=', a[0]):
            a = a[1:]
        if len(a) < 3:
            continue
        if a[0] in ('cp', 'mv', 'install') or (a[0] == 'sed' and any(y == '-i' or y.startswith(('-i', '--in-place')) for y in a[1:-1])):
            if re.search(_构思档 + r'$', a[-1]):
                return True
    return False


def _分(a, b):
    from datetime import datetime
    P = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    return round((P(b) - P(a)).total_seconds() / 60, 1)


def 审一(f, 名, 自=None, 至=None, root=ROOT):
    """一档之账。usage 按 message.id 只取一回（无 id 者逐行计）；自／至＝起止之时（ISO，主环用）；美元逐回照价目算。
    ★1020 W53·X26：构思＝「构思首落−席起」之分（席之首行之时至首回写构思档之时）；构思隔＝构思诸写之最长隔
    （席起、诸写之时依次相减取最大——首回只建档首而後一气写毕者，首落虽小而此隔必大）；无构思档者俱 None。"""
    具 = 取 = 可见 = 0
    起 = 止 = ''
    起全 = None
    构思时们 = []
    用, 序, 模, 终, 截 = {}, [], {}, {}, set()
    for l in open(f, encoding='utf-8'):
        try:
            e = json.loads(l)
        except Exception:
            continue
        ts = e.get('timestamp') or ''
        if (自 and ts and ts < 自) or (至 and ts and ts >= 至):
            continue
        if ts:
            起 = 起 or ts[11:16]; 止 = ts[11:16]
            起全 = 起全 or ts
        m = e.get('message') or {}
        u = m.get('usage')
        if u and e.get('type') == 'assistant':
            k = m.get('id') or ('_%d' % len(用))
            if k not in 用:
                序.append(k)
            用[k] = u
            模[k] = m.get('model') or ''
            终[k] = bool(m.get('stop_reason'))          # ★坑㉗：席之转录多只记流首之 usage（stop_reason 空、产出为占位之数）
            if m.get('stop_reason') == 'max_tokens':   # ★1020 W53·X26：撞产出之顶（128k）而截之回——X26 实证之主量
                截.add(k)
        c = m.get('content')
        if isinstance(c, list):
            for x in c:
                if x.get('type') == 'tool_use':
                    具 += 1
                    if e.get('type') == 'assistant':
                        可见 += len(json.dumps(x.get('input'), ensure_ascii=False))
                        if ts and 是建构思(x):
                            构思时们.append(ts)
                elif x.get('type') == 'text' and e.get('type') == 'assistant':
                    可见 += len(x.get('text') or '')
                elif x.get('type') == 'tool_result':
                    取 += len(json.dumps(x.get('content'), ensure_ascii=False).encode())
    r = dict(名=名, 回=len(用), 具=具, 取=取 // 1024, 起=起, 止=止, 未终=sum(1 for k in 用 if not 终.get(k)), 可见=可见, 截=len(截),
             写1h=sum((u.get('cache_creation') or {}).get('ephemeral_1h_input_tokens', 0) for u in 用.values()),
             写5m=sum((u.get('cache_creation') or {}).get('ephemeral_5m_input_tokens', 0) for u in 用.values()),
             构思=_分(起全, 构思时们[0]) if (起全 and 构思时们) else None,
             构思隔=max(_分(a, b) for a, b in zip([起全] + 构思时们, 构思时们)) if (起全 and 构思时们) else None)
    for k, key in 项:
        r[k] = sum(u.get(key, 0) for u in 用.values())
    r['全'] = r['新'] + r['建'] + r['读'] + r['出']
    r['末'] = sum(用[序[-1]].get(key, 0) for _, key in 项) if 序 else 0
    目 = 价目(root)
    r['金'], r['疑'] = 0.0, []
    for k in 序:
        金, 疑 = 一回之金(模[k], 用[k], 目)
        r['金'] += 金
        if 疑:
            r['疑'].append(疑)
    return r


def 主环(自=None, f=None, 至=None):
    """主会话（总编辑）之账：主环每一回工具都重发整个上下文——其费常不亚於诸席（坑⑮）。"""
    f = f or (sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime) or [None])[-1]
    return 审一(f, '主环(总编辑)', 自, 至) if f else None


等之式 = re.compile(r'(?<![\w.])sleep\s+\d|\bpgrep\b|\bkill\s+-0\b|推\.py\s+--等')


def 是等(x):
    """一个 tool_use 是否等待／轮询：只认 Bash 之命令，且先剔去 heredoc 之体（写码时码里有这些字样，⛔误认——1009 实踩）。"""
    if not isinstance(x, dict) or x.get('type') != 'tool_use' or x.get('name') != 'Bash':
        return False
    c = (x.get('input') or {}).get('command') or ''
    c = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c, flags=re.S)
    c = re.sub(r'"(?:[^"\\]|\\.)*"', '""', c)          # 引号中之字是参数、⛔命令（1009 再踩：坑之描述里之「kill -0」被认作等待）
    c = re.sub(r"'[^']*'", "''", c)
    return bool(等之式.search(c))


def 主环之等(自=None, 至=None, f=None):
    """→ (回, 美元)：主环於 [自, 至) 内发出等待／轮询类工具调用（sleep、pgrep、kill -0、推.py --等）之那几回 API 之费——机器能办而花 token 之一类（坑⑮）。"""
    f = f or (sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime) or [None])[-1]
    if not f:
        return 0, 0.0
    用, 模, 时, 等 = {}, {}, {}, set()
    for l in open(f, encoding='utf-8'):
        try:
            e = json.loads(l)
        except Exception:
            continue
        if e.get('type') != 'assistant':
            continue
        m = e.get('message') or {}
        k = m.get('id')
        if not k:
            continue
        if m.get('usage'):
            用[k] = m['usage']; 模[k] = m.get('model') or ''; 时.setdefault(k, e.get('timestamp') or '')
        for x in (m.get('content') or []):
            if 是等(x):
                等.add(k)
    ids = [k for k in 等 if k in 用 and (not 自 or 时[k] >= 自) and (not 至 or 时[k] < 至)]
    目 = 价目()
    return len(ids), sum(一回之金(模[k], 用[k], 目)[0] for k in ids)


def 主环之重载(自=None, 至=None, f=None, 闲=3600):
    """→ (回, 美元)：主环於 [自, 至) 内「闲逾一时之後之首回」重写缓存之费（缓存 1h 档过期，整份上下文重写；坑㉓）。
    只计缓存写之费（照该回之 5m／1h 两档），⛔计其读与产出——那是这一回本来就要花的。"""
    from datetime import datetime
    f = f or (sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime) or [None])[-1]
    if not f:
        return 0, 0.0
    用, 时, 模 = {}, {}, {}
    for l in open(f, encoding='utf-8'):
        try:
            e = json.loads(l)
        except Exception:
            continue
        m = e.get('message') or {}
        if e.get('type') == 'assistant' and m.get('usage') and m.get('id'):
            用[m['id']] = m['usage']; 模[m['id']] = m.get('model') or ''; 时.setdefault(m['id'], e.get('timestamp') or '')
    P = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
    目 = 价目(); 回 = 0; 金 = 0.0; 前 = None
    for k in sorted(用, key=lambda k: 时[k]):
        if 前 and 时[k] and 时[前] and (P(时[k]) - P(时[前])).total_seconds() > 闲 and (not 自 or 时[k] >= 自) and (not 至 or 时[k] < 至):
            p = 目['模型'].get(模[k])
            if p:
                cc = 用[k].get('cache_creation') or {}
                回 += 1
                金 += ((cc.get('ephemeral_5m_input_tokens') or 0) * p['缓存写5m'] + (cc.get('ephemeral_1h_input_tokens') or 0) * p['缓存写1h']) / 1e6
        前 = k
    return 回, 金


def 通知之数(rid, 档们=None):
    """主会话转录里，该 Run 之通知所报之 subagent_tokens（取末一回）；无则 None。"""
    档们 = 档们 if 档们 is not None else glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
    数 = None
    for f in 档们:
        for l in open(f, encoding='utf-8', errors='ignore'):
            if rid not in l or 'subagent_tokens' not in l:
                continue
            for blk in re.findall(r'<task-notification>.*?</task-notification>', l, re.S):
                if rid in blk:
                    m = re.search(r'<subagent_tokens>(\d+)</subagent_tokens>', blk)
                    if m:
                        数 = int(m.group(1))
    return 数


def 合(行):
    s = {k: sum(r.get(k, 0) for r in 行) for k in ('回', '具', '新', '建', '读', '出', '全', '金', '末', '未终', '可见', '写1h', '写5m', '截')}
    s['疑'] = sum(len(r['疑']) for r in 行)
    return s


def 印(行, rid=None, 档们=None):
    分 = lambda v: '—' if v is None else '%.1f' % v
    print('%-16s %4s %4s %7s %9s %11s %7s %11s %9s %9s %6s %6s %s' % ('席', '来回', '工具', '新入', '缓存建', '缓存读', '产出', '全量', '美元', '末回', '构思', '构思隔', '起—止'))
    for r in 行:
        print('%-16s %4d %4d %7d %9d %11d %7d %11d %9.2f %9d %6s %6s %s—%s' % (
            r['名'], r['回'], r['具'], r['新'], r['建'], r['读'], r['出'], r['全'], r['金'], r['末'],
            分(r.get('构思')), 分(r.get('构思隔')), r['起'], r['止']))
    s = 合(行)
    目 = 价目()
    print('—— 按类（美元之占；价目源 %s，抓於 %s）——' % (目.get('源', ''), 目.get('抓', '')))
    已 = set()
    for 类名, pat in 类:
        g = [r for r in 行 if re.search(pat, r['名']) and id(r) not in 已]
        for r in g:
            已.add(id(r))
        v = sum(r['金'] for r in g)
        print('  %-6s $%10.2f  %4.0f%%  （%d 席）' % (类名, v, 100.0 * v / (s['金'] or 1), len(g)))
    余 = [r for r in 行 if id(r) not in 已]
    if 余:
        v = sum(r['金'] for r in 余)
        print('  %-6s $%10.2f  %4.0f%%  （%d 席：%s）' % ('未归', v, 100.0 * v / (s['金'] or 1), len(余), '、'.join(r['名'] for r in 余)[:60]))
    print('  合计：美元 $%.2f｜来回 %d｜全量 %d｜缓存读 %d｜产出 %d｜Σ末回 %d' % (s['金'], s['回'], s['全'], s['读'], s['出'], s['末']))
    # ★1020 W53·X26：执笔令 N≥398「首条消息即建构思档、想定一样追记一样」——首落逾五分、诸写最长隔逾十分即未守
    #   （392—397：首落中位 37.9 分；二十一回撞 128k 回回在首落之前。只量首落者，首回建档首、再想四十分一气写出，仍报✓——故并量最长隔）
    for 键, 题, 界, 由 in (('构思', '构思首落−席起', 构思之界, '首条消息即建之令未守'),
                         ('构思隔', '构思诸写之最长隔', 构思隔之界, '在思考里排全章——想定一样追记一样之令未守')):
        构 = sorted((r[键], r['名']) for r in 行 if r.get(键) is not None)
        if not 构:
            continue
        逾 = [(v, n) for v, n in 构 if v > 界]
        print('  %s（分）：%d 席｜中位 %.1f｜最长 %.1f（%s）%s' % (
            题, len(构), 构[len(构) // 2][0] if len(构) % 2 else (构[len(构) // 2 - 1][0] + 构[len(构) // 2][0]) / 2, 构[-1][0], 构[-1][1],
            ('｜⛔逾 %d 分 %d 席：%s（%s）' % (界, len(逾), '、'.join('%s %.1f' % (n, v) for v, n in 逾), 由)) if 逾 else '｜✓俱在 %d 分内' % 界))
    if s['截']:   # ★1020 W53·X26：撞 128k 而截（stop_reason=max_tokens）——392—397 三十四席 21 回、15 席；截下之思即废（每回 128k 产出约 $2.6）
        print('  ⛔撞产出之顶而截（max_tokens）：%d 回／%d 席：%s' % (s['截'], sum(1 for r in 行 if r.get('截')),
              '、'.join('%s %d' % (r['名'], r['截']) for r in 行 if r.get('截'))))
    if s['写1h'] or s['写5m']:   # ★1014·坑㉘：席之缓存档（subagentPromptCacheTtl=1h 後须俱一时档）
        print('  缓存写之档：一时 %d（%.0f%%）｜五分 %d' % (s['写1h'], 100.0 * s['写1h'] / (s['写1h'] + s['写5m']), s['写5m']))
    if s['未终']:
        print('  ⚠ 产出未全（坑㉗）：%d/%d 回之 usage 非终值（stop_reason 空——席之转录只记流首，产出为占位之数）；'
              '新入、缓存建、缓存读开流即定，是准的；**产出之 token 与其美元本地不可量，上之美元是下限**。'
              '可见之产出（工具之参＋文字）%d 字；思考之字转录不存，不可量。' % (s['未终'], s['回'], s['可见']))
    if s['疑']:
        print('  ⚠ 未能精算之回 %d：%s' % (s['疑'], '；'.join(sorted({x for r in 行 for x in r['疑']}))[:200]))
    if rid:
        n = 通知之数(rid, 档们)
        if n is None:
            print('  核：通知之数不在（非後台工作流、或转录已不在）——无从核')
        elif n == s['末']:
            print('  核：✓ Σ末回 %d ＝ 通知之 subagent_tokens %d（本器读对了转录）' % (s['末'], n))
        else:
            print('  核：⚠ Σ末回 %d ≠ 通知之 %d（差 %+.1f%%）——不符之因未尽明（已知：续跑之 Run 通知只计其一段）；美元照转录精算，不受此影响' % (s['末'], n, 100.0 * (s['末'] - n) / (n or 1)))


def 找目录(x):
    if os.path.isdir(x):
        return x
    c = glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/%s' % x)) + glob.glob(os.path.expanduser('~/.claude/projects/*/subagents/workflows/%s' % x))
    return c[0] if c else None


def 核全():
    档们 = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
    ids = set()
    for f in 档们:
        for l in open(f, encoding='utf-8', errors='ignore'):
            if 'subagent_tokens' in l:
                ids.update(re.findall(r'wf_[0-9a-f]{8}-[0-9a-f]{3}', l))
    符 = 不符 = 无 = 0
    for rid in sorted(ids):
        d = 找目录(rid)
        n = 通知之数(rid, 档们)
        if not d or n is None:
            无 += 1; continue
        m = 合(审(d))['末']
        if m == n:
            符 += 1
        else:
            不符 += 1; print('  ⚠ %s：Σ末回 %d ≠ 通知 %d' % (rid, m, n))
    print('核全：相符 %d｜不符 %d（续跑／中断之 Run）｜无从核 %d' % (符, 不符, 无))
    return 符, 不符


账档 = os.path.join('设定', '费账.json')


def 记(键, 名, 行, 示=None, root=ROOT, 时=None):
    """一行入费账：界面所示之数（示）与精算之数同记，当场核。"""
    p = os.path.join(root, 账档)
    try:
        账 = json.load(open(p, encoding='utf-8'))
    except Exception:
        账 = {'说明': '费账（1009 立·作者令「任务一完就记」「要非常精准地算出货币量」）：一 Run 或一件主环之活一行。美元＝逐回照 设定/价目.json 精算（比费以此为准）；全量＝四项逐回之和；示＝界面所示（通知之 subagent_tokens，量各席末回之上下文，⛔实耗）；疑＝未能精算之回数（须为 0）。由 工具/费审.py --记／--记主 写，⛔手改。', '行': []}
    s = 合(行)
    row = {'键': 键, '名': 名, '时': 时 or (min((r['起'] for r in 行 if r['起']), default='')), '席': len(行),
           '来回': s['回'], '新入': s['新'], '缓存建': s['建'], '缓存读': s['读'], '产出': s['出'],
           '全量': s['全'], '美元': round(s['金'], 4), '末回': s['末'], '示': 示, '疑': s['疑'],
           '核': (None if 示 is None else ('符' if 示 == s['末'] else '不符'))}
    旧 = next((x for x in 账['行'] if x['键'] == 键), None)
    if 旧 and not 名:
        row['名'] = 旧.get('名', '')          # --记全 补记时⛔冲掉旧之名
    账['行'] = [x for x in 账['行'] if x['键'] != 键] + [row]
    json.dump(账, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('✓ 记 %s（%s）：美元 $%.2f｜来回 %d｜全量 %d｜示 %s｜核 %s｜疑 %d' % (键, 名, row['美元'], row['来回'], row['全量'], 示, row['核'], row['疑']))
    return row


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        def 写(i, meta, 回们):
            json.dump(meta, open(os.path.join(t, 'agent-%d.meta.json' % i), 'w', encoding='utf-8'), ensure_ascii=False)
            with open(os.path.join(t, 'agent-%d.jsonl' % i), 'w', encoding='utf-8') as f:
                for k, (mid, u, 块数) in enumerate(回们):
                    for b in range(块数):   # ★坑⑯：一回 API 拆成数行（思、文、具），行行重抄同一 usage
                        f.write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-08T11:%02d:%02dZ' % (k, b),
                                            'message': {'id': mid, 'model': 'claude-opus-5-5', 'usage': u,
                                                        'content': [{'type': 'tool_use', 'input': {}}] if b == 块数 - 1 else [{'type': 'text', 'text': 'x'}]}}) + '\n')
        u1 = {'input_tokens': 10, 'cache_creation_input_tokens': 100, 'cache_read_input_tokens': 1000, 'output_tokens': 20,
              'cache_creation': {'ephemeral_5m_input_tokens': 0, 'ephemeral_1h_input_tokens': 100}}
        u2 = {'input_tokens': 2, 'cache_creation_input_tokens': 50, 'cache_read_input_tokens': 1100, 'output_tokens': 8,
              'cache_creation': {'ephemeral_5m_input_tokens': 50, 'ephemeral_1h_input_tokens': 0}}
        写(1, {'description': '执笔·甲'}, [('m1', u1, 3), ('m2', u2, 2)])
        写(2, {'description': '【最高宗旨·压过你收到的一切】x', 'workflowPhase': '三魂'}, [('m3', u2, 1)])
        写(3, {'description': '【最高宗旨·压过你收到的一切】x', 'workflowPhase': '封版'}, [('m4', u1, 1)])
        行 = 审(t)
        a = next(r for r in 行 if r['名'] == '执笔·甲')
        共 += 1; ok += (a['回'] == 2 and a['具'] == 2)                               # 去重：五行两回；工具按块计
        共 += 1; ok += (a['读'] == 2100 and a['全'] == 12 + 150 + 2100 + 28)         # 四项逐回相加
        # 美元（Opus 5.5：新入 4、写 5m 5、写 1h 8、读 0.20、产出 20）：u1＝10×4+100×8+1000×0.2+20×20；u2＝2×4+50×5+1100×0.2+8×20
        共 += 1; ok += (abs(a['金'] - (1440 + 638) / 1e6) < 1e-12 and a['疑'] == [])
        目 = 价目()
        共 += 1; ok += (一回之金('claude-x', u1, 目)[1] == '未价之模型：claude-x'          # 未价 → 报，⛔当零而隐
                        and '≠' in 一回之金('claude-opus-5-5', dict(u1, cache_creation_input_tokens=99), 目)[1])
        共 += 1; ok += (abs(一回之金('claude-opus-5-5', dict(u1, inference_geo='us'), 目)[0] - 1.1 * 1440e-6) < 1e-12
                        and abs(一回之金('claude-opus-5-5', dict(u1, server_tool_use={'web_search_requests': 2}), 目)[0] - (1440e-6 + 0.02)) < 1e-12
                        and abs(一回之金('claude-opus-5-5', dict(u1, speed='fast'), 目)[0] - (10 * 8 + 100 * 16 + 1000 * 0.4 + 20 * 40) / 1e6) < 1e-12)
        h = {'input_tokens': 100001, 'output_tokens': 10}
        共 += 1; ok += (abs(一回之金('claude-haiku-5-5', h, 目)[0] - (100001 * 0.5 + 10 * 2.5) / 1e6) < 1e-12)   # 海酷逾十万用长档
        共 += 1; ok += (a['末'] == 2 + 50 + 1100 + 8)                                # 末回＝最後一回之四项
        共 += 1; ok += ({r['名'] for r in 行} == {'执笔·甲', '三魂(长令)', '封版(长令)'})   # 长令席按相位名
        s = 合(行)
        mf = os.path.join(t, 'main.jsonl')
        blk = '<task-notification>wf_aaaaaaaa-bbb done<subagent_tokens>%d</subagent_tokens></task-notification>' % s['末']
        open(mf, 'w', encoding='utf-8').write(json.dumps({'type': 'user', 'message': {'content': blk}}, ensure_ascii=False) + '\n')
        共 += 1; ok += (通知之数('wf_aaaaaaaa-bbb', [mf]) == s['末'] and 通知之数('wf_cccccccc-ddd', [mf]) is None)
        r = 审一(os.path.join(t, 'agent-1.jsonl'), '主', 自='2026-10-08T11:01')
        共 += 1; ok += (r['回'] == 1 and r['读'] == 1100)                            # 主环之窗
        # 重载：两回相隔逾一时，後一回之缓存写计（m1 在 11:00、m2 在 11:01——不逾；另造一档相隔两时）
        g = os.path.join(t, 'gap.jsonl')
        with open(g, 'w', encoding='utf-8') as fh:
            for mid, ts in (('g1', '2026-10-08T10:00:00Z'), ('g2', '2026-10-08T12:30:00Z')):
                fh.write(json.dumps({'type': 'assistant', 'timestamp': ts, 'message': {'id': mid, 'model': 'claude-opus-5-5', 'usage': u1}}) + '\n')
        n重, 金重 = 主环之重载(f=g)
        共 += 1; ok += (n重 == 1 and abs(金重 - 100 * 8 / 1e6) < 1e-12)          # u1 之缓存写 100 皆 1h 档 → $8/M
        B = lambda c, n='Bash': {'type': 'tool_use', 'name': n, 'input': {'command': c}}
        共 += 1; ok += (是等(B('sleep 5; tail x')) and 是等(B('timeout 590 python3 工具/推.py --等')) and 是等(B('while kill -0 123; do :; done'))
                        and not 是等(B("python3 - <<'EOF'\nr = 'sleep 5|pgrep|kill -0'\nEOF\necho ok"))   # 码里之字样⛔误认
                        and not 是等(B('sleep 5', 'Write')) and not 是等(B('grep -n sleepy x'))
                        and not 是等(B('python3 x.py --立 "把码里之 sleep 5／kill -0 认作等待"')) and not 是等(B("echo 'pgrep x'")))
        os.makedirs(os.path.join(t, '设定'))
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            记('wf_x', '测', 行, s['末'], t); 记('wf_x', '测', 行, s['末'] + 1, t)
        账 = json.load(open(os.path.join(t, 账档), encoding='utf-8'))['行']
        共 += 1; ok += (len(账) == 1 and 账[0]['核'] == '不符' and 账[0]['全量'] == s['全'])   # 同键更新、不符即记
    finally:
        shutil.rmtree(t)
    # ★坑㉗：stop_reason 空之回作「未终」（产出为流首之占位）；有 stop_reason 者作终
    t2 = tempfile.mkdtemp()
    try:
        g = os.path.join(t2, 'a.jsonl')
        u = {'input_tokens': 1, 'output_tokens': 8}
        with open(g, 'w', encoding='utf-8') as f:
            f.write(json.dumps({'type': 'assistant', 'message': {'id': 'p', 'model': 'claude-opus-5-5', 'usage': u, 'content': [{'type': 'tool_use', 'input': {'a': '一二三'}}]}}) + '\n')
            f.write(json.dumps({'type': 'assistant', 'message': {'id': 'q', 'model': 'claude-opus-5-5', 'usage': u, 'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': '四五'}]}}) + '\n')
        r = 审一(g, 'x')
        共 += 1; ok += (r['未终'] == 1 and r['可见'] == len(json.dumps({'a': '一二三'}, ensure_ascii=False)) + 2)
        # ★1020 W53·X26：「构思首落−席起」与「构思隔」（诸写之最长隔）——席首行 11:00：
        #   甲＝照令：首条消息 Read 料与 Bash cat > 构思同发（0.2 分），其後 4.0、9.0 分各追记 → 首落 0.2、隔 5.0；
        #   乙＝旧病：heredoc 体里写着「> 起草_乙_构思.md」之字⛔认、读档⛔认，36 分方以 Write 落 → 36.0／36.0；
        #   丁＝验席所逮之空子：首条消息只建档首，再想四十分一气写出 → 首落 0.2（✓）而隔 40.0（⛔）；丙＝无构思档 → None／None
        u0 = {'input_tokens': 1, 'output_tokens': 1}
        def 席(名, 回们):
            p = os.path.join(t2, 名 + '.jsonl')
            with open(p, 'w', encoding='utf-8') as f:
                f.write(json.dumps({'type': 'user', 'timestamp': '2026-10-20T11:00:00Z', 'message': {'content': '令'}}, ensure_ascii=False) + '\n')
                for k, (ts, 具) in enumerate(回们):
                    f.write(json.dumps({'type': 'assistant', 'timestamp': ts, 'message': {'id': 名 + str(k), 'model': 'claude-opus-5-5', 'usage': u0, 'stop_reason': 'tool_use',
                                                                                         'content': 具 if isinstance(具, list) else [具]}}, ensure_ascii=False) + '\n')
            return 审一(p, 名)
        B = lambda c: {'type': 'tool_use', 'name': 'Bash', 'input': {'command': c}}
        读料 = {'type': 'tool_use', 'name': 'Read', 'input': {'file_path': '/x/版本/第398章/_料.md', 'allow_large': True}}
        首 = [读料, B("cat > 版本/第398章/起草_甲_构思.md <<'EOF'\n# 执笔·甲之构思（翻个儿路）\nEOF")]
        追 = lambda 名, 行: B("cat >> 版本/第398章/起草_%s_构思.md <<'EOF'\n%s\nEOF" % (名, 行))
        甲 = 席('甲', [('2026-10-20T11:00:12Z', 首), ('2026-10-20T11:04:00Z', 追('甲', '魂（翻个儿路）：…')), ('2026-10-20T11:09:00Z', 追('甲', '| 一 | 到 | 纸 | 句 |'))])
        共 += 1; ok += (甲['构思'] == 0.2 and 甲['构思隔'] == 5.0)                  # 照令：首落 0.2、隔 5.0（读料之 Read ⛔认作构思）
        乙 = 席('乙', [('2026-10-20T11:01:00Z', B("cat > 版本/第398章/说明.md <<'EOF'\n先 cat > 版本/第398章/起草_乙_构思.md\nEOF")),
                       ('2026-10-20T11:01:30Z', B('cat 版本/第398章/起草_乙_构思.md')),
                       ('2026-10-20T11:36:00Z', {'type': 'tool_use', 'name': 'Write', 'input': {'file_path': '/x/版本/第398章/起草_乙_构思.md', 'content': '魂'}})])
        共 += 1; ok += (乙['构思'] == 36.0 and 乙['构思隔'] == 36.0 and 乙['截'] == 0)   # ⛔heredoc 之体、⛔读档；Write 认
        丁 = 席('丁', [('2026-10-20T11:00:12Z', [读料, B("cat > 版本/第398章/起草_丁_构思.md <<'EOF'\n# 执笔·丁之构思\nEOF")]),
                       ('2026-10-20T11:40:12Z', 追('丁', '魂：…\n## 满分之问\n…\n| 一 | 到 | 纸 | 句 |'))])
        共 += 1; ok += (丁['构思'] == 0.2 and 丁['构思隔'] == 40.0)               # 验席所逮：首落⛔量得出、隔量得出
        丙 = 席('丙', [('2026-10-20T11:03:00Z', 读料)])
        # 撞顶（max_tokens）之回：同一 id 拆数行只计一回；stop_reason 他值⛔计
        截档 = os.path.join(t2, '截.jsonl')
        with open(截档, 'w', encoding='utf-8') as f:
            for mid, sr in (('x1', 'max_tokens'), ('x1', 'max_tokens'), ('x2', 'tool_use'), ('x3', 'max_tokens'), ('x4', None)):
                f.write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-20T11:30:00Z', 'message': {'id': mid, 'model': 'claude-opus-5-5', 'usage': u0, 'stop_reason': sr, 'content': []}}) + '\n')
        截 = 审一(截档, '戊')
        共 += 1; ok += (截['截'] == 2 and 丙['截'] == 0)
        共 += 1; ok += (丙['构思'] is None and 丙['构思隔'] is None)
        # 令与量同一式：造章.js N≥398 之执笔令所定之建档之式（首条消息里与 Read 料同发之那一条 Bash），本器须认得（令改其式而量不跟，即红）
        try:
            js = open(os.path.join(ROOT, '工具', '席', '造章.js'), encoding='utf-8').read()
        except Exception:
            js = ''
        m = re.search(r"cat > \$\{章目\}/起草_\$\{x\.名\}_构思\.md <<'EOF'", js[js.index('首回即落】'):] if '首回即落】' in js else '')
        式 = m.group(0).replace('${章目}', '版本/第398章').replace('${x.名}', '甲') + "\n# x\nEOF" if m else ''
        共 += 1; ok += bool(式 and 是建构思(B(式)) and not 是建构思(读料))
        # ★W60·X33⑤（W53 验席所逮：heredoc 在前之形与 cp／Edit 认不着）——以真转录片段为样（体有删节，形一字未改）：
        #   ①391 庚（wf_bc5f1caf-503·10-15 15:03）：一行两 heredoc，构思之导向在第一个 heredoc 之後
        庚 = ('S=/tmp/claude-0/x/scratchpad && python3 -I - "$S/draft6.md" <<\'PYEND\' && cp "$S/draft6.md" 版本/第391章/起草_稿六.md'
              ' && cat > 版本/第391章/起草_庚_构思.md <<\'ZZEND\' && wc -c 版本/第391章/起草_庚_构思.md\n'
              'import sys\np=sys.argv[1]\nt=open(p,encoding=\'utf-8\').read()\nPYEND\n'
              '魂（回声路）：旧伤不提一字，从离他最近的那只拇指上回来——\nZZEND')
        共 += 1; ok += 是建构思(B(庚))
        #   ②验席之形：`cat <<'EOF' >> 构思`／`cat <<'EOF' > 构思`（导向写在 heredoc 开头之後）
        共 += 1; ok += (是建构思(B("cat <<'EOF' >> 版本/第398章/起草_甲_构思.md\n魂\nEOF"))
                        and 是建构思(B("cat <<'EOF' > 版本/第398章/起草_甲_构思.md\n魂\nEOF")))
        #   ③387 己（wf_9adebaa9-58b·10-14 12:25）：cp 至构思档
        共 += 1; ok += 是建构思(B('cd /home/user/the-novel; S=/tmp/claude-0/x/scratchpad; cp "$S/goushi.md" 版本/第387章/起草_己_构思.md'
                                 ' && cp "$S/gao.md" 版本/第387章/起草_稿一.md && head -1 版本/第387章/起草_己_构思.md'))
        #   ④377 甲（wf_feab0f2b-cad·09-26 23:26）：Edit 构思档
        共 += 1; ok += 是建构思({'type': 'tool_use', 'name': 'Edit', 'input': {
            'replace_all': False, 'file_path': '/home/user/the-novel/版本/第377章/起草_甲_构思.md',
            'old_string': '- **咬合**：本章不担。', 'new_string': '- **咬合**：本章不担。\n\n## 动笔中所改'}})
        #   ⑤383 戊（wf_db24c946-4a1·10-13 14:24）：`F=…构思.md && cat > $F <<'EOF'`；⑥382 丙（wf_24925875-da8·10-13 08:58）：sed -i 构思档
        共 += 1; ok += 是建构思(B("F=版本/第383章/起草_戊_构思.md && cat > $F <<'EOF'\n魂（速度路）：寨里的账划掉一个人有它的快慢\nEOF"))
        共 += 1; ok += 是建构思(B('N=$(grep -n x "$F380" | cut -d: -f1); sed -i "s/风哨 380:9 之三处/风哨 380:${N} 之三处/" 版本/第382章/起草_丙_构思.md;'
                                 ' grep -c "380:${N} 之三处" 版本/第382章/起草_丙_构思.md'))
        #   ⑦⛔误认（不放松）：cp 之源、读档（399 庚·wf_73644685-437 之 sed -n）、体里之字（heredoc 在前亦然）、
        #     记席 `_创作记录` 体里列构思档（400·wf_0f2390c8-4d7）、Edit 他档而其文提构思档
        共 += 1; ok += not any(是建构思(y) for y in (
            B('cp 版本/第391章/起草_庚_构思.md /tmp/bak.md'),
            B("sed -n 11,24p 版本/第399章/起草_庚_构思.md; python3 - <<'EOF'\nfor f in sorted(glob.glob('版本/第%d章/起草_*_构思.md'%n)):\nEOF"),
            B("cat <<'EOF' > 版本/第398章/说明.md\n先 cp x 版本/第398章/起草_乙_构思.md\n再 cat >> 版本/第398章/起草_乙_构思.md\nEOF"),
            B("cat > 版本/第400章/_创作记录.md <<'EOF'\n> 记席据本章各档逐字写成：`起草_甲／乙／丙／丁／戊_构思.md`、`_行家评.md`\nEOF"),
            {'type': 'tool_use', 'name': 'Edit', 'input': {'file_path': '/x/工具/费审.py', 'old_string': '起草_甲_构思.md', 'new_string': 'y'}}))
        #   ⑧量之假绿（验席所述之害）：首回照令 cat > 构思建档首（0.2 分），其後之追记以 heredoc 在前（25 分）与 cp（30 分）落——
        #     旧式认不着後二者，隔＝0.2 而报✓；今须量出隔 24.8
        己 = 席('己', [('2026-10-20T11:00:12Z', [读料, B("cat > 版本/第398章/起草_己_构思.md <<'EOF'\n# 执笔·己之构思\nEOF")]),
                       ('2026-10-20T11:25:00Z', B("cat <<'EOF' >> 版本/第398章/起草_己_构思.md\n魂：…\n| 一 | 到 | 纸 | 句 |\nEOF")),
                       ('2026-10-20T11:30:00Z', B('cp /tmp/x/己.md 版本/第398章/起草_己_构思.md'))])
        共 += 1; ok += (己['构思'] == 0.2 and 己['构思隔'] == 24.8)
        # 印：逐行之「构思」「构思隔」两列印其值（⛔只验表头——验席突变：值印作空串，旧格仍过）；汇总两行各逮其逾
        import io as _io, contextlib as _cl
        buf = _io.StringIO()
        with _cl.redirect_stdout(buf):
            印([甲, 乙, 丁, 丙, 截])
        o = buf.getvalue().split('\n')
        头 = o[0].split()
        列 = {l.split()[0]: l.split() for l in o[1:5] if l.split()}
        值 = lambda 名: tuple(列.get(名, [])[头.index('构思'):头.index('构思隔') + 1]) if '构思' in 头 and '构思隔' in 头 else ()
        共 += 1; ok += (值('甲') == ('0.2', '5.0') and 值('乙') == ('36.0', '36.0') and 值('丁') == ('0.2', '40.0') and 值('丙') == ('—', '—'))
        汇 = '\n'.join(o)
        共 += 1; ok += ('构思首落−席起（分）：3 席' in 汇 and '⛔逾 5 分 1 席：乙 36.0' in 汇
                        and '构思诸写之最长隔（分）：3 席' in 汇 and '⛔逾 10 分 2 席：乙 36.0、丁 40.0' in 汇
                        and '⛔撞产出之顶而截（max_tokens）：2 回／1 席：戊 2' in 汇)
    finally:
        shutil.rmtree(t2)
    print('费审·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--核全']:
        核全(); sys.exit(0)
    if a[:1] == ['--记'] and len(a) in (2, 3):
        d = 找目录(a[1])
        if not d:
            print('⛔ 找不到 Run 之目录：' + a[1]); sys.exit(2)
        rid = os.path.basename(d.rstrip('/'))
        记(rid, a[2] if len(a) == 3 else '', 审(d), 通知之数(rid)); sys.exit(0)
    if a == ['--记全']:
        # ★1009：费账覆全会话——工作流 Run、非工作流子席、主会话全程（单位之定与 费审对拍 同源）
        import 费审对拍
        for 名, fs in 费审对拍.单位们():
            if 名.startswith('run:'):
                rid = 名[4:]
                记(rid, '', 审(os.path.dirname(fs[0])), 通知之数(rid))
            elif 名.startswith('子席:'):
                mf = fs[0][:-len('.jsonl')] + '.meta.json'
                nm = 席名(json.load(open(mf, encoding='utf-8'))) if os.path.exists(mf) else ''
                记(名, '非工作流子席·' + nm, [审一(fs[0], nm)], None)
            else:
                记(名, '主会话全程', [审一(fs[0], '主会话')], None)
        sys.exit(0)
    if a[:1] == ['--记主'] and len(a) in (3, 4):
        r = 主环(a[2], 至=a[3] if len(a) == 4 else None)
        记('主环:%s' % a[2], a[1], [r], None, 时=a[2]); sys.exit(0)
    if a[:1] == ['--主']:
        r = 主环(a[1] if len(a) > 1 else None, 至=a[2] if len(a) > 2 else None)
        印([r] if r else []); sys.exit(0)
    if len(a) != 1:
        print(__doc__); sys.exit(2)
    d = 找目录(a[0])
    if not d:
        print('⛔ 找不到 Run 之目录：' + a[0]); sys.exit(2)
    印(审(d), rid=os.path.basename(d.rstrip('/')))
