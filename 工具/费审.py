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
  python3 工具/费审.py <Run 之目录或 Run ID>   # 每席：来回、工具、四项、全量、美元、末回；按类合计（美元之占）；与通知核
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


def 审一(f, 名, 自=None, 至=None, root=ROOT):
    """一档之账。usage 按 message.id 只取一回（无 id 者逐行计）；自／至＝起止之时（ISO，主环用）；美元逐回照价目算。"""
    具 = 取 = 0
    起 = 止 = ''
    用, 序, 模 = {}, [], {}
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
        m = e.get('message') or {}
        u = m.get('usage')
        if u and e.get('type') == 'assistant':
            k = m.get('id') or ('_%d' % len(用))
            if k not in 用:
                序.append(k)
            用[k] = u
            模[k] = m.get('model') or ''
        c = m.get('content')
        if isinstance(c, list):
            for x in c:
                if x.get('type') == 'tool_use':
                    具 += 1
                elif x.get('type') == 'tool_result':
                    取 += len(json.dumps(x.get('content'), ensure_ascii=False).encode())
    r = dict(名=名, 回=len(用), 具=具, 取=取 // 1024, 起=起, 止=止)
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
    s = {k: sum(r[k] for r in 行) for k in ('回', '具', '新', '建', '读', '出', '全', '金', '末')}
    s['疑'] = sum(len(r['疑']) for r in 行)
    return s


def 印(行, rid=None, 档们=None):
    print('%-16s %4s %4s %7s %9s %11s %7s %11s %9s %9s %s' % ('席', '来回', '工具', '新入', '缓存建', '缓存读', '产出', '全量', '美元', '末回', '起—止'))
    for r in 行:
        print('%-16s %4d %4d %7d %9d %11d %7d %11d %9.2f %9d %s—%s' % (
            r['名'], r['回'], r['具'], r['新'], r['建'], r['读'], r['出'], r['全'], r['金'], r['末'], r['起'], r['止']))
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
        os.makedirs(os.path.join(t, '设定'))
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            记('wf_x', '测', 行, s['末'], t); 记('wf_x', '测', 行, s['末'] + 1, t)
        账 = json.load(open(os.path.join(t, 账档), encoding='utf-8'))['行']
        共 += 1; ok += (len(账) == 1 and 账[0]['核'] == '不符' and 账[0]['全量'] == s['全'])   # 同键更新、不符即记
    finally:
        shutil.rmtree(t)
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
