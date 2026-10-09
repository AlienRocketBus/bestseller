#!/usr/bin/env python3
"""费审（1009 立·作者令「每次都要找到问题所在，让虫洞之法不断完美进化」）——零 token 审一回工作流之费。

为何立：380 造式头一章约 570 万 token；零 token 一审，方知真相——缓存重读约 4.87 亿（初报 8.85 亿乃逐行计重，1009 坑⑯校正），
产出只约 5 万：费≈Σ（每席来回之回数 × 每回所背之上下文）。执笔各来回 106—139 回（大半翻料），
定位／机闸／案席／封版（机器之活）占 38%。**不审即不知刀刃在哪；每跑一回，审一回，方法照数进化。**

用法：
  python3 工具/费审.py <Run 之目录或 Run ID>   # 印每席：来回、工具、缓存建／读、产出、取回、起止；并按类合计
  python3 工具/费审.py --主 [2026-10-09T03:40 [2026-10-09T04:05]]   # 主会话（总编辑）自某时起之账（坑⑮：主环每回工具都重发整个上下文）
  python3 工具/费审.py --自测
Run 之目录在 ~/.claude/projects/<proj>/subagents/workflows/<runId>/（Workflow 回执之 Transcript dir）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, tempfile, shutil

类 = [('造', r'执笔|魂|选|合稿|造·'), ('验', r'逻辑审|盲读|读误|防崩|厚之关|抄袭'), ('机器之活', r'定位|机闸|案席|封版|长令席')]


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
        名 = 席名(json.load(open(mf, encoding='utf-8')))
        行.append(审一(f, 名))
    行.sort(key=lambda r: r['起'])
    return 行


def 审一(f, 名, 自=None, 至=None):
    """一档之账。★1009 坑⑯：转录把一回 API 之每个内容块各写一行、行行重抄同一 usage——
    逐行相加即计重（380 实测 1.8 倍）；故 usage 按 message.id 只取一回（无 id 者逐行计）。自＝起算之时（ISO，主环用）。"""
    具 = 取 = 0
    起 = 止 = ''
    用 = {}
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
            用[m.get('id') or ('_%d' % len(用))] = u
        c = m.get('content')
        if isinstance(c, list):
            for x in c:
                if x.get('type') == 'tool_use':
                    具 += 1
                elif x.get('type') == 'tool_result':
                    取 += len(json.dumps(x.get('content'), ensure_ascii=False).encode())
    合 = lambda k: sum(u.get(k, 0) for u in 用.values())
    return dict(名=名, 回=len(用), 具=具, 建=合('cache_creation_input_tokens'), 读=合('cache_read_input_tokens'),
                出=合('output_tokens'), 取=取 // 1024, 起=起, 止=止)


def 主环(自=None, f=None, 至=None):
    """主会话（总编辑）之账：主环每一回工具都重发整个上下文——其费常不亚於诸席（坑⑮）。"""
    f = f or (sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl')), key=os.path.getmtime) or [None])[-1]
    return 审一(f, '主环(总编辑)', 自, 至) if f else None


def 印(行):
    print('%-18s %5s %5s %10s %12s %8s %7s %s' % ('席', '来回', '工具', '缓存建', '缓存读', '产出', '取回KB', '起—止'))
    for r in 行:
        print('%-18s %5d %5d %10d %12d %8d %7d %s—%s' % (r['名'], r['回'], r['具'], r['建'], r['读'], r['出'], r['取'], r['起'], r['止']))
    总读 = sum(r['读'] for r in 行) or 1
    print('—— 按类（缓存读之占）——')
    已 = set()
    for 类名, pat in 类:
        s = [r for r in 行 if re.search(pat, r['名']) and id(r) not in 已]
        for r in s:
            已.add(id(r))
        v = sum(r['读'] for r in s)
        print('  %-6s %12d  %4.0f%%  （%d 席）' % (类名, v, 100.0 * v / 总读, len(s)))
    print('  合计缓存读 %d｜产出 %d｜最多来回之席：%s（%d 回）' % (
        总读, sum(r['出'] for r in 行), max(行, key=lambda r: r['回'])['名'] if 行 else '-', max((r['回'] for r in 行), default=0)))


def 自测():
    t = tempfile.mkdtemp()
    try:
        def 写(i, 名, n):
            json.dump({'description': 名}, open(os.path.join(t, 'agent-%d.meta.json' % i), 'w', encoding='utf-8'), ensure_ascii=False)
            with open(os.path.join(t, 'agent-%d.jsonl' % i), 'w', encoding='utf-8') as f:
                for k in range(n):
                    f.write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-08T11:%02d:00Z' % k,
                                        'message': {'usage': {'cache_read_input_tokens': 100, 'cache_creation_input_tokens': 10, 'output_tokens': 1},
                                                    'content': [{'type': 'tool_use', 'input': {}}]}}) + '\n')
        写(1, '执笔·甲', 3); 写(2, '【最高宗旨·压过你收到的一切】x', 5)
        # ★坑⑯：一回 API 拆成三行（思、文、具），行行同一 id、同一 usage——只许计一回
        json.dump({'description': '合稿'}, open(os.path.join(t, 'agent-3.meta.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        with open(os.path.join(t, 'agent-3.jsonl'), 'w', encoding='utf-8') as f:
            for k in range(3):
                f.write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-08T12:00:0%dZ' % k,
                                    'message': {'id': 'msg_1', 'usage': {'cache_read_input_tokens': 100, 'output_tokens': 7},
                                                'content': [{'type': 'tool_use', 'input': {}}] if k == 2 else [{'type': 'text', 'text': 'x'}]}}) + '\n')
        行 = 审(t)
        ok = (len(行) == 3 and 行[0]['回'] == 3 and 行[0]['读'] == 300 and 行[1]['名'] == '(长令席)' and 行[1]['具'] == 5
              and 行[2]['回'] == 1 and 行[2]['读'] == 100 and 行[2]['出'] == 7 and 行[2]['具'] == 1)
    finally:
        shutil.rmtree(t)
    print('费审·自测 %d/1' % int(ok))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a[:1] == ['--主']:
        r = 主环(a[1] if len(a) > 1 else None, 至=a[2] if len(a) > 2 else None)
        印([r] if r else []); sys.exit(0)
    if len(a) != 1:
        print(__doc__); sys.exit(2)
    d = a[0]
    if not os.path.isdir(d):
        c = glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/%s' % d)) + glob.glob(os.path.expanduser('~/.claude/projects/*/subagents/workflows/%s' % d))
        d = c[0] if c else d
    if not os.path.isdir(d):
        print('⛔ 找不到 Run 之目录：' + a[0]); sys.exit(2)
    印(审(d))
