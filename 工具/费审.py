#!/usr/bin/env python3
"""费审（1009 立·作者令「每次都要找到问题所在，让虫洞之法不断完美进化」）——零 token 审一回工作流之费。

为何立：380 造式头一章约 570 万 token；零 token 一审，方知真相——缓存重读约 8.85 亿，
产出只约 5 万：费≈Σ（每席来回之回数 × 每回所背之上下文）。执笔各来回 200—258 回（大半翻料），
定位／机闸／案席／封版（机器之活）占 37%。**不审即不知刀刃在哪；每跑一回，审一回，方法照数进化。**

用法：
  python3 工具/费审.py <Run 之目录或 Run ID>   # 印每席：来回、工具、缓存建／读、产出、取回、起止；并按类合计
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
    return re.sub(r'【最高宗旨.*', '(长令席)', d, flags=re.S)[:18]


def 审(目录):
    行 = []
    for f in glob.glob(os.path.join(目录, 'agent-*.jsonl')):
        mf = f[:-len('.jsonl')] + '.meta.json'
        if not os.path.exists(mf):
            continue
        名 = 席名(json.load(open(mf, encoding='utf-8')))
        回 = 具 = 建 = 读 = 出 = 取 = 0
        起 = 止 = ''
        for l in open(f, encoding='utf-8'):
            try:
                e = json.loads(l)
            except Exception:
                continue
            ts = e.get('timestamp') or ''
            if ts:
                起 = 起 or ts[11:16]; 止 = ts[11:16]
            m = e.get('message') or {}
            u = m.get('usage')
            if u and e.get('type') == 'assistant':
                回 += 1
                建 += u.get('cache_creation_input_tokens', 0); 读 += u.get('cache_read_input_tokens', 0)
                出 += u.get('output_tokens', 0)
            c = m.get('content')
            if isinstance(c, list):
                for x in c:
                    if x.get('type') == 'tool_use':
                        具 += 1
                    elif x.get('type') == 'tool_result':
                        取 += len(json.dumps(x.get('content'), ensure_ascii=False).encode())
        行.append(dict(名=名, 回=回, 具=具, 建=建, 读=读, 出=出, 取=取 // 1024, 起=起, 止=止))
    行.sort(key=lambda r: r['起'])
    return 行


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
        行 = 审(t)
        ok = (len(行) == 2 and 行[0]['回'] == 3 and 行[0]['读'] == 300 and 行[1]['名'] == '(长令席)' and 行[1]['具'] == 5)
    finally:
        shutil.rmtree(t)
    print('费审·自测 %d/1' % int(ok))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) != 1:
        print(__doc__); sys.exit(2)
    d = a[0]
    if not os.path.isdir(d):
        c = glob.glob(os.path.expanduser('~/.claude/projects/*/subagents/workflows/%s' % d))
        d = c[0] if c else d
    if not os.path.isdir(d):
        print('⛔ 找不到 Run 之目录：' + a[0]); sys.exit(2)
    印(审(d))
