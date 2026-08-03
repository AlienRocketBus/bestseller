#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一章到底.py —— 单章十轮驱动器

它做的是【量】，不是【判】。
每轮开头把"该看哪儿"一次性铺出来；落刀之后一条命令走完存版→自测→全书检→双绿推。

用法：
  python3 工具/一章到底.py --诊断 136          # 跑闸+核台账+本轮镜头之全部机械扫描
  python3 工具/一章到底.py --收轮 136 "第N轮·xxx：真伤＝... ；补..."   # 改检+存版+自测+全书检+双绿推
  python3 工具/一章到底.py --账单 137          # 到期账列单+重复立账扫描+已付扫描
  python3 工具/一章到底.py --拆点 136          # 三步法拆点测算
"""
import os, re, sys, json, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.environ.setdefault('ZM_STREAM', 'streamA-cli')

CN = '零一二三四五六七八九十百'
S_XIU_M = r'味|气味|鼻|闻'                      # 机器计
S_XIU_R = r'味|气味|鼻|闻|腥|馊|甜|潮|焦|酸'     # 并具体气味名（人工复核用）
S_TING  = r'听|响|声|叫|吠'
S_CHU_M = r'凉|温|烫|硬|软|摸|按|贴'                    # 机器计
S_CHU_R = r'凉|温|烫|硬|软|摸|按|贴|硌|压|掂|蹭|撑|捏|搓|拽|勒'  # 并具体触觉动词
DUNWU   = r'^(我忽然|我这才|我心里|我明白|我看出|我先以为|我原先|我在心里|后来我|我头一回)'
JINCI   = ['抖', '点亮', '鼎心', '气运', '换锚', '阵眼', '颤']
WU      = ['灯','芯','油','盐','本子','笔','架','绳','刀','鞋','壁','水','石','布','筒']

LENS = {
 1:'⑤感官庭——逐块测三密度，找三感全零之块（八面之教训：算数段／对话段／大事段／对白之章间隙／承约补叙段／招供段／看不清之段／对峙段）',
 2:'四堂会审——逐句通读全章；查序乱（倒插／反思先于其事／人未动而写其动作）、自造重复、数与本文自撞',
 3:'挑刺王终读——逐数对表；每个数回查canon，每个相对日词回查其所指之章与日；并问"这一笔当时把什么当成了不用算的"',
 4:'升华庭——招式库十招比对，补空缺之招（招七世界无动于衷／招十同一动作两代人最常空）',
 5:'⑥在场庭＋⑦内面庭——各人是否只在功能位；双线是否断；内面之句是否系於一物一事',
 6:'十庭①资源庭——器物总账；零字之物逐一判其可否；前章立过之耗今日是否到期',
 7:'⑧时序＋⑨节奏＋⑩留白——相对日词逐处核；最长无人声串≤50；留白是否止於当止',
 8:'跨章复审——拿前三章当尺子；尤查前章所立之律今日是否被校（校出否定者更值）',
 9:'收官减法轮——先试削，再算真中点，再於其近处找界；逾上限则依【十之九】拆章',
 10:'收官轮——器物总账（拆章后必重测·117通例）＋逐段生死检；毕则跑横评',
}


def sh(cmd, timeout=400):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return '（超时）'


def cn2int(s):
    s = s.strip()
    if s.startswith('十'): s = '一' + s
    v, unit, out = 0, 1, 0
    for ch in reversed(s):
        if ch == '十':
            unit = 10; v = 0
        elif ch == '百':
            unit = 100; v = 0
        else:
            d = CN.index(ch)
            out += d * unit
            unit = 1 if unit == 1 else unit
    if '十' in s and s.index('十') == 0:
        out += 10
    # 简易：仅用于 100-199 章名
    m = re.match(r'^一百(.*)$', s)
    if m:
        rest = m.group(1)
        out = 100 + (cn2int(rest) if rest else 0)
    return out


def chap_file(n):
    for f in glob.glob('正文/*.md'):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if m and cn2int(m.group(1)) == n:
            return f
    return None


def body_of(f):
    t = open(f, encoding='utf-8').read()
    b = t.split('【本章亮点】')[0]
    return re.sub(r'^.*?第.+?章[^\n]*\n', '', b, count=1, flags=re.S)


def ledger(n):
    p = '版本/第%d章/_台账.json' % n
    if not os.path.exists(p): return [], set()
    d = json.load(open(p, encoding='utf-8'))['版本']
    rs = set()
    for r in d:
        m = re.match(r'第(\d+)轮', r.get('说明', ''))
        if m: rs.add(int(m.group(1)))
    return d, rs


def dens(body):
    n = len(re.sub(r'\s', '', body)) or 1
    return dict(
        n=n,
        xiu_m=1000*len(re.findall(S_XIU_M, body))/n,
        xiu_r=1000*len(re.findall(S_XIU_R, body))/n,
        ting=1000*len(re.findall(S_TING, body))/n,
        chu_m=1000*len(re.findall(S_CHU_M, body))/n,
        chu_r=1000*len(re.findall(S_CHU_R, body))/n)


def blocks(paras, k=12):
    """把全章按每 k 段切块，返回每块之三密度"""
    out = []
    for i in range(0, len(paras), k):
        seg = ''.join(paras[i:i+k])
        m = len(re.sub(r'\s', '', seg))
        if not m: continue
        out.append((i, min(i+k, len(paras)), m,
                    1000*len(re.findall(S_XIU_R, seg))/m,
                    1000*len(re.findall(S_TING, seg))/m,
                    1000*len(re.findall(S_CHU_R, seg))/m,
                    seg[:26]))
    return out


def diagnose(n):
    f = chap_file(n)
    if not f:
        print('✗ 未找到第%d章正文' % n); return
    t = open(f, encoding='utf-8').read()
    body = body_of(f)
    paras = [p.strip() for p in body.split('\n') if p.strip()]
    d = dens(body)

    print('█' * 30)
    print('  第%d章 · %s' % (n, os.path.basename(f)))
    print('█' * 30)

    # 1 跑闸
    print('\n── 一·并发闸 ──')
    out = sh("python3 -c \"import importlib.util;s=importlib.util.spec_from_file_location('j','工具/十轮精进.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.concurrency_check(quiet=True)[1].split(chr(10))[2])\"")
    print('  ' + out.strip()[:120])

    # 2 台账 → 本轮
    rows, done = ledger(n)
    todo = [i for i in range(1, 11) if i not in done]
    cur = todo[0] if todo else None
    print('\n── 二·台账 ──')
    print('  版本%d ｜真轮已跑 %s' % (len(rows), sorted(done) or '无'))
    if cur is None:
        print('  ✓ 十轮已满，请跑 --横评 %d' % n)
    else:
        print('  ▶ 本轮＝第%d轮：%s' % (cur, LENS[cur]))

    # 3 硬项
    print('\n── 三·硬项 ──')
    hard = []
    for w in JINCI:
        c = t.count(w)
        if c: hard.append('禁词%s×%d' % (w, c))
    if t.count('—'): hard.append('破折×%d' % t.count('—'))
    if t.count('"'): hard.append('半角×%d' % t.count('"'))
    wu5 = [s for s in re.split(r'(?<=[。！？…])', t) if s.count('，') >= 5]
    if wu5: hard.append('五逗×%d' % len(wu5))
    if re.findall(r'[零一二三四五六七八九十百]+章', body): hard.append('章号泄漏')
    if sum(1 for p in paras if '主角' in p): hard.append('第三人称窜入')
    h = t[t.find('【本章亮点】'):] if '【本章亮点】' in t else ''
    if h.count('—'): hard.append('亮点破折')
    if len(re.findall(r'。\n(?!\n)[^\n]', h)): hard.append('亮点空行病')
    print('  ' + ('✓全清' if not hard else '⛔ ' + '｜'.join(hard)))
    for s in wu5[:3]:
        print('     五逗: %s' % s.strip()[:60])

    # 4 软项
    dw = sum(1 for p in paras if re.match(DUNWU, p))
    say = sum(1 for p in paras if '“' in p)
    run = best = 0
    for p in paras:
        if '“' in p: run = 0
        else:
            run += 1; best = max(best, run)
    longp = sum(1 for p in paras if len(re.sub(r'\s', '', p)) >= 90)
    print('\n── 四·软项 ──')
    print('  净重%d 段%d ｜嗅%.1f(实%.1f) 听%.1f 触%.1f(实%.1f) ｜自定标 嗅≥3 听≥4 触≥7'
          % (d['n'], len(paras), d['xiu_m'], d['xiu_r'], d['ting'], d['chu_m'], d['chu_r']))
    print('  ← 嗅／触之机器计只认少数词；实计并具体名与动词。依133与本轮之律：以实计判达标，不得强灌"味"字')
    print('  长段%d ｜顿悟%d ｜人声%d/%d ｜最长无人声串%d段%s'
          % (longp, dw, say, len(paras), best, '  ⚠逾50' if best > 50 else ''))

    # 5 空块（第1／5／6轮之眼）
    print('\n── 五·逐块三密度（三感全零者即真伤之候选） ──')
    for a, b_, m, x, ti, ch in [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in blocks(paras)]:
        flag = ''
        if x == 0 and ti == 0 and ch == 0: flag = '  ⛔三感全零'
        elif (x == 0) + (ti == 0) + (ch == 0) >= 2: flag = '  ⚠二感零'
        print('  ¶%03d-%03d %4d字 | 嗅%5.1f 听%5.1f 触%5.1f%s' % (a, b_, m, x, ti, ch, flag))

    # 6 器物总账（第6／10轮之眼）
    print('\n── 六·器物总账 ──')
    zero = []
    line = []
    for k in WU:
        c = body.count(k)
        line.append('%s:%d' % (k, c))
        if c == 0: zero.append(k)
    print('  ' + '  '.join(line))
    if zero:
        print('  ⛔零字：%s ← 逐一判其可否（其料是否已归他篇／今日是否无其事）' % '、'.join(zero))

    # 7 相对日词（第3／7轮之眼）
    print('\n── 七·相对日词（逐处回查其所指之章与日） ──')
    hits = list(re.finditer(r'(?<!大)(前天|昨天|三天前|前几天|大前天)', body))
    if not hits: print('  （无）')
    for m in hits[:14]:
        i = m.start()
        print('  [%s] %s' % (m.group(1), body[max(0, i-30):i+22].replace('\n', ' ')))
    if len(hits) > 14: print('  …共%d处' % len(hits))
    if len(hits) > 3:
        print('  ⚠引前章逾三处 → 依135之律须列表逐处核，不得逐句零核')

    # 8 自造重复（第9轮之眼）
    print('\n── 八·四字串六现以上 ──')
    seen = {}
    for i in range(len(body)-3):
        k = body[i:i+4]
        if re.match(r'^[\u4e00-\u9fa5]{4}$', k): seen[k] = seen.get(k, 0) + 1
    rep = sorted([(k, v) for k, v in seen.items() if v >= 6], key=lambda x: -x[1])
    print('  ' + ('（无）' if not rep else '  '.join('%s×%d' % (k, v) for k, v in rep[:12])))
    print('  ← 人名／固定说法判活；其余判死')

    # 9 拆点（第9轮之眼）
    if d['n'] > 3300:
        print('\n── 九·净重逾上限%d%%，拆点三步法预测 ──' % int(d['n']/3300*100-100))
        tot = sum(len(re.sub(r'\s', '', p)) for p in paras)
        c = 0
        for i, p in enumerate(paras):
            c += len(re.sub(r'\s', '', p))
            if abs(c - tot/2) < 110:
                print('  ¶%03d [上%4d 下%4d 差%3d] %s' % (i+1, c, tot-c, abs(2*c-tot), p[:38]))

    print('\n' + '─' * 30)
    print('◆ 机器已把"该看哪儿"铺完。以下须人判：真伤是哪一根、刀怎么落、判活判死。')
    print('◆ 落刀毕，跑：python3 工具/一章到底.py --收轮 %d "第%s轮·…"' % (n, cur or 'N'))


def close_round(n, note):
    f = chap_file(n)
    print('── 改检 ──')
    o = sh('python3 工具/小说检察官.py --改检 %d' % n)
    for ln in o.splitlines():
        if '机械层' in ln or '✓' in ln or '⚠' in ln or '⛔' in ln:
            print('  ' + ln.strip())
    print('\n── 同步全本 ──')
    sh('python3 工具/同步全本阅读器.py')
    print('  ✓')
    print('\n── 存版（新律：先于push） ──')
    o = sh('python3 工具/十轮精进.py --存版 %d "%s"' % (n, note))
    for ln in o.splitlines()[-4:]:
        print('  ' + ln.strip())
    print('\n── 自测 ──')
    st = sh('python3 工具/小说检察官.py --selftest', 200)
    stl = st.strip().splitlines()[-1] if st.strip() else ''
    print('  ' + stl)
    print('\n── 全书 ──')
    fb = sh('python3 工具/小说检察官.py')
    for ln in fb.splitlines():
        if '全书仪表盘' in ln or ln.strip().startswith('✗'):
            print('  ' + ln.strip())
    ok = ('ERROR=0(须0)' in fb
          and re.search(r'规则回归:(\d+)/\1', stl)
          and '契约负测:3/3' in stl)
    if ok:
        sh('git add 正文/ 设定/ 工具/ README.md 阅读器/ 版本/')
        sh('git -c user.name=Claude -c user.email=c@a.com commit -qm "%s"' % note.replace('"', ''))
        p = sh('git push -q')
        print('\n✅ 双绿已推')
    else:
        print('\n⛔ 未过双绿闸，不推。先清上列硬错。')


def bills(n):
    d = json.load(open('设定/到期账.json', encoding='utf-8'))
    items = d['items']
    due = [x for x in items if x.get('状态') == 'open' and int(x.get('到期章', 999)) <= n]
    print('── 到期账（限%d及以前） ──' % n)
    for it in sorted(due, key=lambda x: int(x['到期章'])):
        od = '  ⚠逾期%d章' % (n - int(it['到期章'])) if int(it['到期章']) < n else ''
        print('  %-14s 限%-4s %s%s' % (it['id'], it['到期章'], str(it.get('事'))[:30], od))
    print('\n── 重复立账扫描（依135之律：扫"事"栏＋"人"栏） ──')
    opens = [x for x in items if x.get('状态') == 'open']
    NAMES = ['东头', '钱满', '刘二', '老头', '陈砚', '沈鸢']
    flagged = False
    for i in range(len(opens)):
        for j in range(i+1, len(opens)):
            a, b = str(opens[i].get('事', '')), str(opens[j].get('事', ''))
            same_person = any(p in a and p in b for p in NAMES)
            share = len(set(a) & set(b)) / max(len(set(a) | set(b)), 1)
            if same_person or share > 0.5:
                print('  ⚠ %s「%s」 ／ %s「%s」' % (opens[i]['id'], a[:20], opens[j]['id'], b[:20]))
                flagged = True
    if not flagged: print('  （未见可疑）')
    print('\n── 已付扫描（依131之律：先查其是否已付） ──')
    print('  ← 机器不能判。逐笔取其"事"之关键词，於后三章正文grep，见即判已清（漏销）')
    for it in sorted(due, key=lambda x: int(x['到期章']))[:8]:
        kw = re.sub(r'[何时谁什么怎么为的是了在上下]', '', str(it.get('事', '')))[:6]
        if not kw: continue
        found = []
        for k in range(int(it['到期章'])-2, n+1):
            ff = chap_file(k)
            if ff and kw and kw in open(ff, encoding='utf-8').read():
                found.append(k)
        if found:
            print('  ⚠ %s 之关键词「%s」见於第%s章 → 查是否已实付' % (it['id'], kw, '、'.join(map(str, found))))


def split_point(n):
    f = chap_file(n)
    body = body_of(f)
    paras = [p.strip() for p in body.split('\n') if p.strip()]
    tot = sum(len(re.sub(r'\s', '', p)) for p in paras)
    print('── 三步法·第一步：净重%d（上限3300，逾%d%%） ──' % (tot, int(tot/3300*100-100)))
    print('── 第二步：真中点 ──')
    c = 0
    cands = []
    for i, p in enumerate(paras):
        c += len(re.sub(r'\s', '', p))
        if abs(c - tot/2) < 200:
            cands.append((i+1, c, tot-c, abs(2*c-tot), p))
    for i, up, dn, diff, p in cands:
        mark = ''
        if p.startswith('“'): mark = '  ← 对话首，不宜拆'
        elif len(re.sub(r'\s', '', p)) <= 10: mark = '  ← 短句，界清'
        print('  ¶%03d [上%4d 下%4d 差%3d] %s%s' % (i, up, dn, diff, p[:40], mark))
    print('── 第三步：於其近处取界最清者（其前为一记之收、其后自起新记） ──')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(0)
    cmd, ch = sys.argv[1], int(sys.argv[2])
    if cmd == '--诊断': diagnose(ch)
    elif cmd == '--收轮': close_round(ch, sys.argv[3] if len(sys.argv) > 3 else '第N轮')
    elif cmd == '--账单': bills(ch)
    elif cmd == '--拆点': split_point(ch)
    else: print(__doc__)
