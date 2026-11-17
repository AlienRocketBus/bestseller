#!/usr/bin/env python3
"""机械账（1013 立·作者令「所有的非工作性任务都要全面采用虫洞效应、全面进化：不仅要省 token，还要效果更好——是所有的」）
——零 token：把主会话（总编辑）每一回 API 按其所发之工具归类，算出每一类非写作之活花了几回、几美元。

为何立：非写作之活（推、存底、全测、封版、记账、等、看状态、读料……）多由主环发命令去跑，
**命令本身零 token，而主环每发一回都重读整份上下文**——花的是「回数 × 上下文」。不先量出哪类回数多、哪类贵，
就无从判哪类该并成一条命令、哪类该交给钩子或事件、哪类根本不该醒模型。

量法（与 工具/费审.py 同一把尺，⛔另造）：
  · 每回按 message.id 去重，usage 取其末行（流式之末值）；美元照 费审.一回之金（设定/价目.json）。
  · 主会话读其同名诸档（费审.主档们·坑62：会话换目录而续，旧段只在旧档）。
  · 一回发数个工具者，其费按工具数均分到各类；无工具之回（答话）入「答话」。
  · 闲逾一时之首回另记其缓存重写之费（费审.主环之重载，坑㉓）——它是「停」之价，⛔是那一回之活之价。
  · 归类只看命令之字（先剔 heredoc 之体与引号中之字，同 费审.是等——坑㉑），先中先得，序即下表之序。

用法：
  python3 工具/机械账.py [起 ISO [止 ISO]]     # 主会话一段之账，按类印 回／美元／占
  python3 工具/机械账.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob

import 费审

# 先中先得。（类名, 是否写作之活, 认法）——认法对 Bash 之命令（已剔 heredoc／引号）或工具名
类 = [
    ('等待·轮询', False, lambda n, c: n == 'Bash' and (费审.是等({'type': 'tool_use', 'name': 'Bash', 'input': {'command': c}}) or re.search(r'(^|[;&|]\s*)ps\s', c))),
    ('通知·任务之管', False, lambda n, c: n in ('ReadNotifications', 'TaskStop', 'TaskOutput', 'TaskGet', 'TaskList', 'TaskCreate', 'TaskUpdate', 'Monitor') or re.search(r'\.claude/projects|/tasks/', c or '')),   # 翻席之转录看进度亦是看任务
    ('定时·接力', False, lambda n, c: 'trigger' in n or 'send_later' in n or re.search(r'自走|接力|心跳', c or '')),
    ('推送·存底', False, lambda n, c: re.search(r'推\.py|存底|git\s+(push|fetch|pull)', c or '')),
    ('提交', False, lambda n, c: re.search(r'git\s+(commit|add)\b', c or '')),
    ('封版·回执', False, lambda n, c: re.search(r'封版\.py|回执对账|同步全本阅读器|净重对表', c or '')),
    ('全测·诸闸', False, lambda n, c: re.search(r'全测|囤灰闸|对位|小说检察官|起草闸|硬闸|开轮六检|负测_|--自测|造式验|段案验', c or '')),
    ('记账·复盘', False, lambda n, c: re.search(r'费审|复盘|费账|对拍|工作流账|方案\.py|方法坑账|总编辑复核|暂停令|机械账', c or '')),
    ('看状态', False, lambda n, c: re.search(r'git\s+(status|log|diff|show|rev-parse|branch)', c or '')),
    ('工作流·派席', True, lambda n, c: n in ('Workflow', 'Agent', 'SendMessage')),
    ('写器·写档', True, lambda n, c: n in ('Write', 'Edit', 'NotebookEdit') or re.search(r"open\([^)]*['\"]w['\"]|\.write\(|sed\s+-i", c or '')),
    ('读料', False, lambda n, c: n in ('Read', 'Grep', 'Glob') or re.search(r'^\s*(cd [^&]*&&\s*)?(cat|sed -n|grep|head|tail|ls|find|wc|python3 -c|python3 - )', c or '')),
]


def _剔(c):
    c = re.sub(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", '', c, flags=re.S)
    c = re.sub(r'"(?:[^"\\]|\\.)*"', '""', c)
    return re.sub(r"'[^']*'", "''", c)


def 归(x):
    n = x.get('name') or ''
    c = _剔((x.get('input') or {}).get('command') or '') if n == 'Bash' else ''
    if n == 'Bash' and not c.strip():
        c = (x.get('input') or {}).get('command') or ''
    for 名, _, 认 in 类:
        try:
            if 认(n, c):
                return 名
        except Exception:
            pass
    return '其他'


def 账(f=None, 自=None, 至=None):
    """→ {类: [回, 美元]}（另「答话」「闲置重载」二行）。
    ★1117（坑62）：f 可为诸档；不给即 费审.主档们（最新之主会话档与其同名之旧档／续档）——按 message.id 合，续档所抄之回与原回同 id 同 usage，合之即一回。"""
    fs = [f] if isinstance(f, str) else (list(f) if f else 费审.主档们())
    用, 模, 时, 具 = {}, {}, {}, {}
    for l in (l for ff in fs for l in open(ff, encoding='utf-8')):
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
            if isinstance(x, dict) and x.get('type') == 'tool_use' and x.get('id'):
                具.setdefault(k, {})[x['id']] = x
    目 = 费审.价目()
    出 = {}
    for k in 用:
        if (自 and 时[k] < 自) or (至 and 时[k] >= 至):
            continue
        金 = 费审.一回之金(模[k], 用[k], 目)[0]
        xs = list((具.get(k) or {}).values())
        名们 = [归(x) for x in xs] or ['答话']
        for 名 in 名们:
            r = 出.setdefault(名, [0.0, 0.0])
            r[0] += 1 / len(名们); r[1] += 金 / len(名们)
    回, 金 = 费审.主环之重载(自, 至, fs)
    出['（内含）闲置重载'] = [回, 金]
    return 出


def 印(出):
    总 = sum(v[1] for k, v in 出.items() if not k.startswith('（'))
    写 = {名 for 名, 是, _ in 类 if 是}
    print('  %-14s %8s %10s %6s' % ('类', '回', '美元', '占'))
    for k, v in sorted(出.items(), key=lambda kv: -kv[1][1]):
        if k.startswith('（'):
            continue
        print('  %-14s %8.1f %10.2f %5.1f%%%s' % (k, v[0], v[1], 100 * v[1] / 总 if 总 else 0, '' if k in 写 or k == '答话' else '  ·非写作'))
    非 = sum(v[1] for k, v in 出.items() if not k.startswith('（') and k not in 写 and k != '答话')
    print('  合计 $%.2f｜非写作之活 $%.2f（%.0f%%）｜%s $%.2f（%d 回）' % (总, 非, 100 * 非 / 总 if 总 else 0, '闲置重载（已摊入各类）', 出['（内含）闲置重载'][1], 出['（内含）闲置重载'][0]))


def 自测():
    ok = 共 = 0
    def b(c): return {'type': 'tool_use', 'name': 'Bash', 'input': {'command': c}}
    共 += 1; ok += (归(b('python3 工具/推.py')) == '推送·存底')
    共 += 1; ok += (归(b('sleep 30')) == '等待·轮询' and 归(b('python3 工具/推.py --等')) == '等待·轮询')
    共 += 1; ok += (归(b("cd x && python3 - <<'EOF'\nprint('git push sleep 9')\nEOF")) != '推送·存底')   # heredoc 之体⛔认（坑㉑）
    共 += 1; ok += (归(b('git commit -m "推.py 存底"')) == '提交')                                          # 引号中之字⛔认
    共 += 1; ok += (归({'type': 'tool_use', 'name': 'ReadNotifications', 'input': {}}) == '通知·任务之管' and 归({'type': 'tool_use', 'name': 'Workflow', 'input': {}}) == '工作流·派席')
    共 += 1; ok += (归(b('cd /x && sed -n 1,9p a.py')) == '读料' and 归(b('python3 工具/全测.py --快')) == '全测·诸闸')
    共 += 1; ok += (归(b('ps aux | grep 全测')) == '等待·轮询' and 归(b('D=/root/.claude/projects/x; ls $D')) == '通知·任务之管')
    print('机械账·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    印(账(自=a[0] if a else None, 至=a[1] if len(a) > 1 else None))
