#!/usr/bin/env python3
"""复盘（1009 立·作者令「每一次任务都要复盘：踩的坑、哪里做了无用功、哪里花了大量 token 与时却无实果、
具体之改进方案；每回都要有详细之任务记录与具体耗费——越来越有效、越来越科学之 token 用法」）。

本器零 token 起草一份复盘：任务之记录（取自 `设定/工作流账.json`）＋每个 Run 之费审（`工具/费审.py`）自动填入；
「无用功」一节先列机器之疑点（来回最多之席、机器之活之占、超估之倍），**总编辑须亲写其判与改进方案**。
无复盘不许结案（`工具/工作流账.py --裁 W 取／重造` 先验 `设定/复盘/*W*.md` 三节俱在）。

用法：
  python3 工具/复盘.py W12 380造式 wf_e7912fa3-a0c [其他 Run ID…] [--自 2026-10-08T09:01]
      → 写 设定/复盘/<月日>_W12_380造式.md（已在则⛔覆）；自＝任务起时（缺则取工作流账之「起」）
  python3 工具/复盘.py 主环 二代定稿 --自 2026-10-09T03:05 [--至 2026-10-09T04:05]   # 非工作流之任务（总编辑亲手）亦须复盘
  python3 工具/复盘.py W61 401造式 wf_… --简 --平台 84.97   # --平台＝本会话 get_session 之 cost_usd（X56）； ★1021 章之简式：数归器、判只三问三句（作者令「总结⛔过度消耗」）
  python3 工具/复盘.py W72 题 wf_… --简 --平台 "不可分：<由>"   # 一会话跨数件、get_session 之 cost_usd 係累计而分不出者（由四字以上）
  ★1027（执行之审 #86）：--简 无 --平台 即拒（器计曾低估 2.4 倍·X56）。
  python3 工具/复盘.py --验     # 闸：设定/复盘/ 诸档须有 耗费／无用功／改进方案／坑 四节，坑节须点坑账之号或写「无新坑」
      ★1027 起之档另验二样（执行之审 #5 #58 #81②·「立停」之证）：
        ①逾估：实费（平台之实，无则总费）＞工作流账该件预估×1.5 而档无「逾估：<由>」即红；
        ②机器之活：「机器能办而花token」占实费 >5% 者，其「进化」（简式）或「改进方案」须引瑕疵总账在账之 X 号、或「已行：工具/<器>.py」而其器在盘
  python3 工具/复盘.py --效账   # 诸复盘之「效」汇一表：总费、服务目标之费与其占、浪费、机器能办而花token；按类比上回
  python3 工具/复盘.py --自测

1009 作者令「每次总结方法：具体流程、具体制作过程、所踩之坑——一次又一次之经验让虫洞方法越来越好」：
  自动填：流程（各 Run 之席按时序）｜制作过程（任务起後之提交，git 自动）｜耗费（费审：逐回照官方价目精算美元）｜主环之费（费审 --主）｜资源分配（美元之占）
  并自动入 `设定/费账.json`（随时记）
  总编辑亲填：产出、与上回比之判、无用功之判、刀刃、改进方案、坑（新坑先 `工具/方法坑账.py --立`，旧坑复踩 `--复踩`；坑必入法典）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, io, json, glob, time, contextlib, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import 费审


配额 = [('造', 75, '≥'), ('验', 20, '≤'), ('机器之活', 0, '≤')]


def 分配表(行):
    """资源分配官之表：实占（美元之占，费审精算）对配额（造≥75%、验≤20%、机器之活→0 归脚本、找料→0 归章料）。"""
    import re as _re
    总 = sum(x['金'] for x in 行) or 0
    if not 总:
        return '（无 Run 可审——非工作流之席，照回执手填分配）'
    出 = ['| 类 | 配额 | 实占 | 判 |', '|---|---|---|---|']
    已 = set()
    for 名, 额, 向 in 配额:
        pat = dict(费审.类)[名]
        s = [x for x in 行 if _re.search(pat, x['名']) and id(x) not in 已]
        for x in s:
            已.add(id(x))
        占 = 100.0 * sum(x['金'] for x in s) / 总
        合 = (占 >= 额) if 向 == '≥' else (占 <= 额 + (5 if 额 == 0 else 0))
        出.append('| %s | %s%d%% | %.0f%% | %s |' % (名, 向, 额, 占, '✓' if 合 else '⛔失配'))
    出.append('| 找料 | 0（章料） | 见「无用功」：执笔／魂之工具回数 | — |')
    return '\n'.join(出)


import re, subprocess


def 制作(自, root=ROOT, 至=None):
    """任务起後之提交（git 自动）：时、号、说明之首行。"""
    if not 自:
        return ['（无起时——以 --自 给之）']
    o = subprocess.run(['git', '-c', 'core.quotepath=off', 'log', '--since=%s' % 自.replace('Z', '+00:00'), '--reverse',
                        '--date=format:%m-%d %H:%M', '--format=- %ad｜%h｜%s'] + (['--until=%s' % 至.replace('Z', '+00:00')] if 至 else []), cwd=root, capture_output=True, text=True).stdout
    return [l[:220] for l in o.strip().split('\n') if l] or ['（任务起後无提交）']


def 坑号们(t):
    return set(re.findall(r'[\u2460-\u2473\u3251-\u325F\u32B1-\u32BF]|坑\d+', t))


新律起 = '1027'   # ★1027 执行之审 #5 #58 #81②：逾估之由、机器之活之引——自此日之档起验（旧档⛔追·同 1015／1018／1021 之例）
新律起W = 72      # ★复核所逮：档名之日只有月日（MMDD），跨年（0101 起）「≥1027」即不成立、新律静默失效——另以 W 号接住（W 号只增）


def 新律之档(名):
    """日 ≥ 1027 之档，或 W 号 ≥ 72 之档（跨年之後档名之日回到 01xx，以 W 号接住）。"""
    m = re.match(r'(\d{4})_', 名)
    w = re.match(r'\d{4}_W(\d+)_', 名)
    return bool(m and m.group(1) >= 新律起) or bool(w and int(w.group(1)) >= 新律起W)


def _元(效文, 项):
    m = re.search(r'^- %s：(?:约\s*)?\$\s*(\d+(?:\.\d+)?)' % 项, 效文, re.M)
    return float(m.group(1)) if m else None


def 估之元(W, root=ROOT):
    """工作流账该件之「预估」之 $ 数（首见者）；无件、无 $ → None。"""
    try:
        件 = next((x for x in json.load(open(os.path.join(root, '设定', '工作流账.json'), encoding='utf-8'))['件'] if x.get('id') == W), {})
    except Exception:
        return None
    m = re.search(r'\$\s*(\d+(?:\.\d+)?)', str(件.get('预估', '')))
    return float(m.group(1)) if m else None


def 新律之坏(名, t, root=ROOT):
    """★1027 起之复盘：①逾估无由 ②机器之活逾 5% 而未引账／未行。→ [坏]"""
    坏 = []
    效 = re.search(r'^## 效[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
    if not 效:
        return 坏
    实 = _元(效.group(1), '平台之实') or _元(效.group(1), '总费')
    m = re.match(r'\d{4}_(W\d+)_', 名)
    估 = 估之元(m.group(1), root) if m else None
    if 实 and 估 and 实 > 1.5 * 估 and not re.search(r'逾估[：:]\s*(?:\S\s*){4,}', t):
        坏.append('%s 实费 $%.2f 逾预估 $%.2f 之 1.5 倍，而无「逾估：<由>」（立停之证·1027 执行之审 #81②）' % (名, 实, 估))
    机 = _元(效.group(1), '机器能办而花token')
    if 实 and 机 and 机 / 实 > 0.05:
        问 = re.search(r'^- 进化：(.*)$', t, re.M)
        改 = re.search(r'^## 改进方案[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
        文 = (问.group(1) if 问 else '') + '\n' + (改.group(1) if 改 else '')
        try:
            账 = open(os.path.join(root, '设定', '瑕疵总账.md'), encoding='utf-8').read()
        except OSError:
            账 = ''
        引 = [x for x in re.findall(r'X\d+', 文) if re.search(r'^\|\s*%s\s*\|' % x, 账, re.M)]
        行 = [x for x in re.findall(r'已行[：:][^\n]*?工具/([\w\u4e00-\u9fff]+\.py)', 文) if os.path.exists(os.path.join(root, '工具', x))]
        if not 引 and not 行:
            坏.append('%s 机器能办而花token $%.2f 占实费 %.0f%%（>5%%），而其「进化」／「改进方案」未引瑕疵总账在账之 X 号、亦无「已行：工具/<器>.py」（坑⑫·1027 执行之审 #5 #58）'
                      % (名, 机, 100 * 机 / 实))
    return 坏


def 验(root=ROOT):
    坏 = []
    try:
        import 方法坑账 as 坑账
        有号 = {坑账.圈(k['号']) for k in 坑账.读(root)['坑']}
    except Exception:
        有号 = None
    for f in sorted(glob.glob(os.path.join(root, '设定', '复盘', '*.md'))):
        t = open(f, encoding='utf-8').read()
        名 = os.path.basename(f)
        # ★1021 作者令「总结不要过度消耗……轻轻松松一想能想出来」：1021 起带「## 三问」之简式——数归器、判只三句
        _日 = re.match(r'(\d{4})_', 名)
        简 = bool(_日 and _日.group(1) >= '1021' and '## 三问' in t)
        for 节 in (('## 耗费', '## 三问', '## 坑') if 简 else ('## 耗费', '## 无用功', '## 改进方案', '## 坑')):
            if 节 not in t:
                坏.append('%s 缺「%s」' % (名, 节))
        效 = re.search(r'^## 效[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
        if not 效:
            坏.append('%s 缺「## 效」（总费、服务目标之费、浪费、机器能办而花token——俱须 $ 之数）' % 名)
        else:
            for 项 in ('类', '目标'):
                m = re.search(r'^- %s：(.*)$' % 项, 效.group(1), re.M)
                if not m or not m.group(1).strip() or m.group(1).strip().startswith('（填'):
                    坏.append('%s 之效缺「%s」' % (名, 项))
            for 项 in ('总费', '服务目标之费', '浪费', '机器能办而花token'):
                if not re.search(r'^- %s：(?:约\s*)?\$\d' % 项, 效.group(1), re.M):   # 1024 实踩（410）：「约 $1」亦是 $ 之数（--效账 之读法同）
                    坏.append('%s 之效「%s」须是 $ 之数' % (名, 项))
        m日 = re.match(r'(\d{4})_', 名)
        if 简:
            问 = re.search(r'^## 三问[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
            for 项 in ('法行否', '最贵之席值否', '进化'):
                m = re.search(r'^- %s：(.*)$' % 项, 问.group(1), re.M) if 问 else None
                if not m or not m.group(1).strip() or m.group(1).strip().startswith('（填'):
                    坏.append('%s 之三问缺「%s」' % (名, 项))
                elif 项 == '进化' and not re.search(r'X\d+|Y\d+|已行|无[：:]', m.group(1)):
                    坏.append('%s 之三问「进化」须引瑕疵总账 X 号（带限）、或「已行：…」、或「无：<由>」' % 名)
        elif m日 and m日.group(1) >= '1015':                 # ★1015 起之复盘须答虹吸之问（旧档⛔追）
            虹 = re.search(r'^## 虹吸之问[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
            if not 虹:
                坏.append('%s 缺「## 虹吸之问」（重付、可流、顺势、下一回之法）' % 名)
            else:
                if not re.search(r'^- 重付：\$\d', 虹.group(1), re.M):
                    坏.append('%s 之虹吸之问「重付」须是 $ 之数' % 名)
                for 项 in ('可流', '顺势', '下一回之法'):
                    m = re.search(r'^- %s：(.*)$' % 项, 虹.group(1), re.M)
                    if not m or not m.group(1).strip() or m.group(1).strip().startswith('（填'):
                        坏.append('%s 之虹吸之问缺「%s」' % (名, 项))
                # ★1017 作者铁律·开发不停（朝 B＋C）：1018 起之复盘，虹吸之问须有「B＋C 之候」——一条效↑费↓之候选新法，效与费俱有其计
                if m日.group(1) >= '1018':
                    m = re.search(r'^- B＋C 之候：(.*)$', 虹.group(1), re.M)
                    if not m or m.group(1).strip().startswith('（填') or not ('效' in m.group(1) and '费' in m.group(1)):
                        坏.append('%s 之虹吸之问缺「B＋C 之候」（一条效↑费↓之候选新法，效与费各写其计——1017 作者铁律·开发不停）' % 名)
                    # ★1021 作者问「为什么还是我自己发现」：B＋C 之候写了七回只行二回——1021 起须入瑕疵总账（引 X 号）或写「已行」，账限哨按其限催
                    elif m日.group(1) >= '1021' and not re.search(r'X\d+|Y\d+|已行', m.group(1)):
                        坏.append('%s 之「B＋C 之候」未入账：须引瑕疵总账之 X 号（带限）或写「已行：<提交或器>」——账限哨按限催（1021）' % 名)
        if m日 and m日.group(1) >= '1015' and not 简:     # ★1015 起之复盘须答完美之问（1021 简式免之）
            完 = re.search(r'^## 完美之问[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
            if not 完:
                坏.append('%s 缺「## 完美之问」（残缺、独立之眼、未验之断）' % 名)
            else:
                for 项 in ('残缺', '独立之眼', '未验之断'):
                    m = re.search(r'^- %s：(.*)$' % 项, 完.group(1), re.M)
                    if not m or not m.group(1).strip() or m.group(1).strip().startswith('（填'):
                        坏.append('%s 之完美之问缺「%s」' % (名, 项))
        if 新律之档(名):
            坏 += 新律之坏(名, t, root)
        坑节 = t.split('## 坑', 1)[1] if '## 坑' in t else ''
        号 = 坑号们(坑节)
        if '## 坑' in t and not re.search(r'^\s*[-*]?\s*无新坑', 坑节, re.M) and not 号:
            坏.append('%s 坑节既无坑账之号、又未写「无新坑」' % 名)
        if 有号 is not None and 号 - 有号:
            坏.append('%s 坑节点了坑账里没有之号：%s（先 工具/方法坑账.py --立）' % (名, ''.join(sorted(号 - 有号))))
    return not 坏, 坏


def 效账(root=ROOT):
    """自诸复盘之「## 效」汇一表（唯一之源即复盘档，⛔另存而失同步），按类比上回。"""
    行 = []
    for f in sorted(glob.glob(os.path.join(root, '设定', '复盘', '*.md'))):
        t = open(f, encoding='utf-8').read()
        效 = re.search(r'^## 效[^\n]*\n(.*?)(?=^## |\Z)', t, re.M | re.S)
        if not 效:
            continue
        g = lambda k: (re.search(r'^- %s：(.*)$' % k, 效.group(1), re.M) or [None, ''])[1].strip()
        金 = lambda k: float((re.search(r'\$(\d+(?:\.\d+)?)', g(k)) or [0, '0'])[1])
        行.append(dict(档=os.path.basename(f), 类=g('类').split('（')[0].strip(), 总=金('总费'), 目=金('服务目标之费'), 废=金('浪费'), 机=金('机器能办而花token')))
    print('%-34s %-8s %9s %9s %7s %9s %9s' % ('复盘', '类', '总费', '服务目标', '之占', '浪费', '机器能办'))
    上 = {}
    for r in 行:
        占 = 100.0 * r['目'] / r['总'] if r['总'] else 0
        比 = ''
        if r['类'] in 上:
            p = 上[r['类']]
            比 = '｜比上回同类：总费 %+.2f、浪费 %+.2f、之占 %+.0f%%' % (r['总'] - p['总'], r['废'] - p['废'], 占 - (100.0 * p['目'] / p['总'] if p['总'] else 0))
        print('%-34s %-8s %9.2f %9.2f %6.0f%% %9.2f %9.2f%s%s' % (r['档'][:34], r['类'][:8], r['总'], r['目'], 占, r['废'], r['机'], '  ⛔机器能办而花' if r['机'] > 0 else '', 比))
        上[r['类']] = r
    return 行


def 起草(W, 题, runs, root=ROOT, 日=None, 自=None, 至=None, 简=False, 平台=None):
    日 = 日 or time.strftime('%m%d', time.gmtime())
    出 = os.path.join(root, '设定', '复盘', '%s_%s_%s.md' % (日, W, 题))
    if os.path.exists(出):
        print('⛔ 已在：%s（⛔覆——要补就直接改它）' % os.path.relpath(出, root)); return None
    os.makedirs(os.path.dirname(出), exist_ok=True)
    件 = {}
    try:
        账 = json.load(open(os.path.join(root, '设定', '工作流账.json'), encoding='utf-8'))
        件 = next((x for x in 账['件'] if x['id'] == W), {})
    except Exception:
        pass
    自 = 自 or 件.get('起')
    费段, 疑 = [], []
    费审之行 = []
    流程 = []
    总金 = 0.0
    机总 = 0.0          # ★1027 复核所逮：诸 Run 之机器之活之席（费审.类）——简式之「机器能办而花token」照填（旧恒填 $0，#5 #58 之验遂空）
    for r in runs:
        d = r if os.path.isdir(r) else (glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/%s' % r)) or [r])[0]
        if not os.path.isdir(d):
            费段.append('- Run %s：找不到其目录（非工作流之席，耗费照其回执手填）' % r); continue
        行 = 费审.审(d)
        费审之行 += 行
        rid = os.path.basename(d.rstrip('/'))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            费审.印(行, rid=rid)
            费审.记(rid, '%s·%s' % (W, 题), 行, 费审.通知之数(rid), root)   # ★随时记：复盘起草即补记其 Run（⛔漏记）
        费段.append('### Run %s\n\n```\n%s```' % (r, buf.getvalue()))
        流程.append('- Run %s：%s' % (r, ' → '.join('%s(%s)' % (x['名'], x['起']) for x in 行)))
        金 = sum(x['金'] for x in 行) or 1e-9
        总金 += 金
        for x in sorted(行, key=lambda x: -x['金'])[:3]:
            疑.append('- 花费最多：%s（$%.2f；%d 回、工具 %d）——是在造，还是在翻料／办机器之活？' % (x['名'], x['金'], x['回'], x['具']))
        import re as _re
        机 = sum(x['金'] for x in 行 if _re.search(dict(费审.类)['机器之活'], x['名']))
        机总 += 机
        if 机:
            疑.append('- 机器之活（定位／机闸／案席／封版）占美元 %d%%——凡机器能办者，下回归脚本' % (100 * 机 / 金))
    主 = None
    if 自:
        try:
            主 = 费审.主环(自.replace('Z', ''), 至=至.replace('Z', '') if 至 else None)
        except Exception:
            主 = None
    载 = 费审.主环之重载(自.replace('Z', '') if 自 else None, 至.replace('Z', '') if 至 else None) if 自 else (0, 0.0)
    等 = 费审.主环之等(自.replace('Z', '') if 自 else None, 至.replace('Z', '') if 至 else None) if 自 else (0, 0.0)
    机段 = '- 主环非写作之活：（无起时）'
    if 自:
        try:
            import 机械账
            m = 机械账.账(自=自.replace('Z', ''), 至=至.replace('Z', '') if 至 else None)
            写 = {名 for 名, 是, _ in 机械账.类 if 是} | {'答话'}
            非 = sorted([(k, v) for k, v in m.items() if not k.startswith('（') and k not in 写], key=lambda kv: -kv[1][1])
            总 = sum(v[1] for k, v in m.items() if not k.startswith('（'))
            机段 = '- 主环非写作之活：机器自认 $%.2f（占主环 %d%%）——前三：%s（坑㉔：一件机械之活一条命令；候即止）' % (
                sum(v[1] for _, v in 非), 100 * sum(v[1] for _, v in 非) / 总 if 总 else 0,
                '；'.join('%s %.0f 回 $%.2f' % (k, v[0], v[1]) for k, v in 非[:3]))
        except Exception as e:
            机段 = '- 主环非写作之活：（机械账读不出：%s）' % e
    if 主:
        with contextlib.redirect_stdout(io.StringIO()):
            费审.记('主环:%s' % 自.replace('Z', ''), '%s·%s' % (W, 题), [主], None, root, 时=自)   # ★随时记
    主段 = ['- 主环（总编辑）自 %s 至 %s：美元 $%.2f｜来回 %d｜全量 %d｜缓存读 %d｜产出 %d（主环每回工具都重发整个上下文——坑⑮）' % (自, 至 or '今', 主['金'], 主['回'], 主['全'], 主['读'], 主['出'])] if 主 else ['- 主环之费：（无起时或读不出主会话之记）']
    文 = ['# 复盘·%s·%s（%s 立）' % (W, 题, 日), '',
         '## 任务', '',
         '- 名：%s' % 件.get('名', ''), '- 目的：%s' % str(件.get('目的', ''))[:400],
         '- 停止线：%s' % 件.get('停止线', ''), '- 预估：%s' % 件.get('预估', ''),
         '- 裁：%s' % '；'.join('%s %s' % (x.get('法'), str(x.get('由', ''))[:160]) for x in 件.get('裁', [])), '',
         '## 流程（实走·自动）', ''] + (流程 or ['- （无 Run——总编辑亲手之任务，照「制作过程」）']) + ['',
         '## 制作过程（任务起後之提交·git 自动）', ''] + 制作(自, root, 至) + ['',
         '## 产出', '', '（总编辑填：成了什么、质之实据——致命数、行家对拍库之分、盲读）', '',
         '## 耗费', '', '- 合计美元（诸席）：$%.2f（各 Run 详下；逐回照 设定/价目.json 精算，已入 设定/费账.json）' % 总金] + 主段 + [''] + 费段 + ['',
         '## 资源分配（资源分配官·1009）', '', 分配表(费审之行), '',
         '## 效（每任务必记·1009 作者令「token 有没有浪费、有没有服务於最该服务之目标」）', '',
         '- 类：（填：一章／造剧情／核验／治器设计……——效账按类比上回）',
         '- 目标：（填：此件最该服务之目标一句）',
         '- 总费：$%.2f（自动：诸席 $%.2f＋主环 $%.2f）' % (总金 + (主['金'] if 主 else 0), 总金, 主['金'] if 主 else 0),
         ] + (['- 平台之实：$%.2f（本会话 get_session 之 cost_usd·X56：以此为准；器计 $%.2f，差 %.1f 倍）' % (平台, 总金 + (主['金'] if 主 else 0), 平台 / max(总金 + (主['金'] if 主 else 0), 0.01))]
              if isinstance(平台, (int, float)) else ['- 平台之实：%s（以器计之总费为准）' % 平台] if 平台 else []) + [
         '- 服务目标之费：$（填：直接产出目标之席与来回之费，引费审之类或费账）',
         '- 浪费：$（填：无用功逐条之 $ 合计）',
         '- 机器能办而花token：$（填：须 $0；非零即入坑账。主环等待／轮询之回，机器自认：%d 回 $%.2f）' % 等,
         '- 闲置重载：机器自认 %d 回 $%.2f（会话闲逾一时、缓存过期而整份上下文重写——坑㉓；长停宜开新会话接交接档）' % 载,
         机段, '',
         '## 与上回比（一次比一次好·1009）', '', '| 项 | 上回同类（填其复盘档名与数） | 本回 | 判 |', '|---|---|---|---|', '| 造之占 | | | 须↑ |', '| 总费（美元，费审精算） | | | 须↓ |', '| 质（致命数、拍库之分、盲读） | | | 须不劣 |', '', '（三样俱合方算进化；不合即写其因、其改）', '',
         '## 无用功', '', '机器之疑（总编辑逐条判：真费、或该花）：'] + (疑 or ['- （无 Run 可审）']) + ['', '（总编辑填：哪里花了大量 token 与时而无实果，其根）', '',
         '## 刀刃', '', '（总编辑填：钱花在哪儿真出了果）', '',
         '## 改进方案', '', '（总编辑填：具体到改哪档哪条；下回照办之验——下回之费审拿什么数比）', '',
         '## 虹吸之问（1015 作者令「方法照虹吸、虫洞不停进化，服务於中国最好看之小说」·法典一「虹吸之律」）', '',
         '- 重付：$（填：本件所付而早已付过之料——章记、病册、诸席之交、费账；须 $0，非零即入坑账）',
         '- 可流：（填：本件之活有无会重复者；已做成流水线之一环否——封版／记席／全测；未做者写其计）',
         '- 顺势：（填：本件有无另起一席专办、本可由已在做之事顺带产出者）',
         '- 下一回之法：（填：照上三问，此类之活下回之法比本回好在哪——具体到改哪档）',
         '- B＋C 之候：（填：一条效更好且费更省之候选新法——效之计、费之计、凭什么；下一件照上线之律试之）', '',
         '## 完美之问（1015 作者令「所有的一切都必须达到绝对的完美」·法典一「完美之律」）', '',
         '- 残缺：（填：本件交出後仍知之缺，逐条带限；无则写「无」）',
         '- 独立之眼：（填：谁验——驳席、盲读、负测、对照之试；逮了什么、治了没有）',
         '- 未验之断：（填：未经跑或测之断语；无则写「无」，有则逐条写其验之计）', '',
         '## 坑', '', '（每条点坑账之号：新坑先 `python3 工具/方法坑账.py --立 名 根 治 计`；旧坑复踩 `--复踩 号 "……；治：……"`；并入法典。无则写「无新坑」）', '']
    if 简:   # ★1021 简式：任务、流程、制作、耗费、效（数俱器填）＋三问三句＋坑；长节俱去（作者令「总结不要过度消耗」）
        止 = 文.index('## 与上回比（一次比一次好·1009）')
        文 = [x for x in 文[:止] if not x.startswith('## 产出') and not x.startswith('（总编辑填：成了什么')]
        _名 = str(件.get('名', '')) + ' ' + 题      # ★1027：类照件名（旧恒填「一章」——W72、W73 之治器与审入写书之占，费哨失真）
        _类 = ('一章' if re.search(r'第\d+章|\d{3}造式|造式二代', _名) else '造剧情' if '剧情庭' in _名
              else '核验' if re.search(r'审', _名) else '治器设计')
        文 = [('- 类：%s' % _类 if x.startswith('- 类：（填') else
              ('- 目标：写%s，以最少之钱写到最好' % 题 if _类 == '一章' else '- 目标：办%s，以最少之钱办到最好' % 题) if x.startswith('- 目标：（填') else
              '- 服务目标之费：$%.2f（自动：诸席）' % 总金 if x.startswith('- 服务目标之费：') else
              '- 机器能办而花token：$%.2f（自动：机器之活之席 $%.2f＋主环等待 %d 回 $%.2f）' % (机总 + 等[1], 机总, 等[0], 等[1])
              if x.startswith('- 机器能办而花token：') else x) for x in 文]
        文 += ['## 三问（1021 作者令：每章之始与末一想即得，⛔长文）', '',
              '- 法行否：（填一句：原法还靠谱否——费比上章、致命、盲读）',
              '- 最贵之席值否：（填一句：最贵之席值不值，可省之数）',
              '- 进化：（填一句：一条更省更好之改——入瑕疵总账 X 号带限，或「已行：…」，或「无：<由>」）', '',
              '## 坑', '', '- 无新坑']
    open(出, 'w', encoding='utf-8').write('\n'.join(文))
    print('✓ 起草 %s——%s' % (os.path.relpath(出, root), '三问三句与「浪费」之数须总编辑亲填（简式）' if 简 else '「产出」「与上回比」「无用功」之判「刀刃」「改进方案」「坑」须总编辑亲填'))
    return 出


def 自测():
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定'))
        json.dump({'件': [{'id': 'W9', '名': '测', '目的': '测', '裁': [{'法': '取', '由': '达'}]}]},
                  open(os.path.join(t, '设定', '工作流账.json'), 'w'), ensure_ascii=False)
        rd = os.path.join(t, 'run'); os.makedirs(rd)
        json.dump({'description': '封版'}, open(os.path.join(rd, 'agent-1.meta.json'), 'w'), ensure_ascii=False)
        open(os.path.join(rd, 'agent-1.jsonl'), 'w').write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-09T01:00:00Z', 'message': {'usage': {'cache_read_input_tokens': 50}, 'content': []}}) + '\n')
        with contextlib.redirect_stdout(io.StringIO()):
            f = 起草('W9', '测', [rd], t, '1009')
            g = 起草('W9', '测', [rd], t, '1009')
        s = open(f, encoding='utf-8').read() if f else ''
        ok = bool(f) and g is None and all(k in s for k in ('## 耗费', '## 无用功', '## 改进方案', '## 坑', '## 流程', '## 制作过程')) and '机器之活' in s and '主环非写作之活' in s and '## 虹吸之问' in s and '## 完美之问' in s
        ok = ok and 验(t)[0] is False                                   # 草稿之坑节、效节未填 → 闸红
        s2 = open(f, encoding='utf-8').read()
        s2 = re.sub(r'- 类：.*', '- 类：核验', s2); s2 = re.sub(r'- 目标：.*', '- 目标：测', s2)
        s2 = re.sub(r'- 服务目标之费：.*', '- 服务目标之费：$0', s2); s2 = re.sub(r'- 浪费：.*', '- 浪费：$0', s2)
        s2 = re.sub(r'- 机器能办而花token：.*', '- 机器能办而花token：$0', s2)
        open(f, 'w', encoding='utf-8').write(s2 + '无新坑\n')
        ok = ok and 验(t)[0] is True
        open(f, 'w', encoding='utf-8').write(re.sub(r'- 浪费：.*', '- 浪费：约 $1（估）', s2) + '无新坑\n')
        ok = ok and 验(t)[0] is True                                    # 「约 $N」亦过
        open(f, 'w', encoding='utf-8').write(re.sub(r'- 浪费：.*', '- 浪费：约一块', s2) + '无新坑\n')
        ok = ok and 验(t)[0] is False                                   # 无 $ 之数仍红
        os.remove(f)
        # ★1027 执行之审 #5 #58 #81②：1027 起之档——逾估无由即红、写「逾估：」即过；机器之活逾 5% 未引账即红、引在账之 X 或已行之器即过；旧档（1026）⛔追
        json.dump({'件': [{'id': 'W9', '名': '测', '目的': '测', '预估': '约 2 时、$10', '裁': []}]},
                  open(os.path.join(t, '设定', '工作流账.json'), 'w'), ensure_ascii=False)
        open(os.path.join(t, '设定', '瑕疵总账.md'), 'w', encoding='utf-8').write('## 未治\n| X7 | 机器之活 | s | t | 420 段前 |\n')
        os.makedirs(os.path.join(t, '工具'), exist_ok=True)
        open(os.path.join(t, '工具', '某器.py'), 'w').write('#')
        模 = ('# 复盘\n## 耗费\n- x\n## 效\n- 类：一章\n- 目标：测\n- 总费：$%s\n- 服务目标之费：$1\n- 浪费：$0\n- 机器能办而花token：$%s\n'
             '## 三问\n- 法行否：行\n- 最贵之席值否：值\n- 进化：%s\n%s## 坑\n- 无新坑\n')
        def 局(日, 总, 机, 进, 尾=''):
            for x in glob.glob(os.path.join(t, '设定', '复盘', '*.md')):
                os.remove(x)
            open(os.path.join(t, '设定', '复盘', '%s_W9_测.md' % 日), 'w', encoding='utf-8').write(模 % (总, 机, 进, 尾))
            return 验(t)
        r1 = 局('1027', 20, 0, '无：测')                                   # 20 > 10×1.5 而无由 → 红
        r2 = 局('1027', 20, 0, '无：测', '- 逾估：执笔撞顶重派三席，估未计重派\n')
        r3 = 局('1026', 20, 0, '无：测')                                   # 旧档⛔追
        r4 = 局('1027', 12, 1, '无：测')                                   # 机 1/12 > 5% 而未引 → 红
        r5 = 局('1027', 12, 1, '入账 X7（限 420 段前）')
        r6 = 局('1027', 12, 1, '已行：工具/某器.py 归脚本')
        r7 = 局('1027', 12, 1, '入账 X99（账上无此号）')
        r8 = 局('1027', 12, 0.5, '无：测')                                 # 0.5/12 ≈ 4% → 不红
        ok = ok and (r1[0] is False and '逾估' in r1[1][0] and r2[0] and r3[0] and r4[0] is False and '机器能办' in r4[1][0]
                     and r5[0] and r6[0] and r7[0] is False and r8[0])
        # 跨年：「0105_W90_」仍验（W≥72）；「1026_W71_」、「1009_主环_」⛔追；「1027_主环_」验
        ok = ok and 新律之档('0105_W90_第450章.md') and 新律之档('1027_W72_执行.md') and not 新律之档('1026_W71_第410章.md') \
            and not 新律之档('1009_主环_坑账.md') and 新律之档('1027_主环_x.md')
        # --简 无 --平台 → 拒（rc=2）；--平台 不可分：由 → 起草（档记其由）
        p0 = subprocess.run([sys.executable, os.path.abspath(__file__), 'W9', '测', '--简'], capture_output=True, text=True, cwd=t)
        if p0.returncode != 2:                                          # 守未拦即会起草入真仓——当场清之（⛔留字）
            for x in glob.glob(os.path.join(ROOT, '设定', '复盘', '*_W9_测.md')):
                os.remove(x)
        ok = ok and p0.returncode == 2 and '--平台' in p0.stdout
        with contextlib.redirect_stdout(io.StringIO()):
            f2 = 起草('W9', '测二', [rd], t, '1027', 简=True, 平台='不可分：一会话跨三件')
        ok = ok and bool(f2) and '- 平台之实：不可分：一会话跨三件' in open(f2, encoding='utf-8').read()
        # ★1027 复核所逮（#5 #58 之验旧为空验）：简式之「机器能办而花token」旧恒填 $0——机器之活之席（封版）占满亦过；今照费审之类自填，
        #   1027 起之档其占逾 5% 而「进化」未引账即红；引在账之 X 号即过（放行之反例）
        rd2 = os.path.join(t, 'run2'); os.makedirs(rd2)
        json.dump({'description': '封版'}, open(os.path.join(rd2, 'agent-1.meta.json'), 'w'), ensure_ascii=False)
        open(os.path.join(rd2, 'agent-1.jsonl'), 'w').write(json.dumps({'type': 'assistant', 'timestamp': '2026-10-27T01:00:00Z', 'message': {
            'id': 'm1', 'model': 'claude-opus-5-5', 'usage': {'input_tokens': 10, 'cache_read_input_tokens': 4000000, 'output_tokens': 20000}, 'content': []}}) + '\n')
        for x in glob.glob(os.path.join(t, '设定', '复盘', '*.md')):
            os.remove(x)
        with contextlib.redirect_stdout(io.StringIO()):
            f3 = 起草('W9', '测三', [rd2], t, '1027', 简=True, 平台='不可分：一会话跨三件')
        s3 = open(f3, encoding='utf-8').read() if f3 else ''
        m3 = re.search(r'^- 机器能办而花token：\$(\d+\.\d+)（自动：机器之活之席 \$(\d+\.\d+)', s3, re.M)
        s3 = re.sub(r'- 法行否：.*', '- 法行否：行', s3); s3 = re.sub(r'- 最贵之席值否：.*', '- 最贵之席值否：值', s3)
        s3 = re.sub(r'- 浪费：.*', '- 浪费：$0', s3)
        s3 = re.sub(r'- 进化：.*', '- 进化：无：测', s3) + '\n无新坑\n'
        open(f3, 'w', encoding='utf-8').write(s3)
        r9 = 验(t)
        open(f3, 'w', encoding='utf-8').write(s3.replace('- 进化：无：测', '- 进化：入账 X7（限 420 段前）'))
        r10 = 验(t)
        ok = ok and bool(m3) and float(m3.group(1)) > 0 and m3.group(1) == m3.group(2) \
            and r9[0] is False and any('机器能办' in x for x in r9[1]) and r10[0] is True
    finally:
        shutil.rmtree(t)
    print('复盘·自测 %d/1' % int(ok))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--效账']:
        效账(); sys.exit(0)
    if a == ['--验']:
        o, 坏 = 验()
        print('✓ 复盘：诸档四节俱在、坑节俱点坑账之号' if o else '⛔ 复盘：\n  ' + '\n  '.join(坏))
        sys.exit(0 if o else 1)
    自 = 至 = None
    简 = '--简' in a
    a = [x for x in a if x != '--简']
    if '--自' in a:
        i = a.index('--自'); 自 = a[i + 1]; a = a[:i] + a[i + 2:]
    if '--至' in a:
        i = a.index('--至'); 至 = a[i + 1]; a = a[:i] + a[i + 2:]
    平台 = None
    if '--平台' in a:   # ★X56：本会话 get_session 之 cost_usd（器计曾低估 2.4 倍）
        i = a.index('--平台'); v = a[i + 1] if i + 1 < len(a) else ''; a = a[:i] + a[i + 2:]
        if re.match(r'不可分[：:]\s*(?:\S\s*){4,}', v):
            平台 = v
        else:
            try:
                平台 = float(v.lstrip('$'))
            except ValueError:
                print('⛔ --平台 须是 $ 之数（get_session 之 cost_usd），或「不可分：<由>」（由四字以上）'); sys.exit(2)
    if 简 and 平台 is None:   # ★1027 执行之审 #86：简式之费以平台之实为准——⛔无之即拒
        print('⛔ --简 须带 --平台 $X（本会话 get_session 之 cost_usd·X56：器计曾低估 2.4 倍）；一会话跨数件而分不出者写 --平台 "不可分：<由>"'); sys.exit(2)
    if len(a) < 2:
        print(__doc__); sys.exit(2)
    起草(a[0], a[1], a[2:], 自=自, 至=至, 简=简, 平台=平台)
