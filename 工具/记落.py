#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""记落（1024 立·省 token 之审 records 第一条·第一步，N≥411）——零 token：记席所留之纯机械之格，器代填、器代核。

为何立：405—410 记席五章同形（均 $6.66／26—40 回），其产出与回数有一截花在抄器之印——回执 §一之数、sha1、日号、
  圣经事件链之题与旧锚〔已销〕、检察官 schema 行、总览之题与「写至 N」、席记之骨、创作记录 §五之终稿、开镜卡问七之大审诸笔；
  手抄即有误：408 创作记录 §五手书「净重2610」而器印 2629（六数行）；Y54 大审之笔截半句、Y25 漏 #23；404 未书圣经之随。
  审之裁（records 第一条 revise·safeguards ③⑤）：分两步上——第一步只把纯机械之格交器，判断诸格照旧由记席直写；
  411、412 两章开镜庭 --静、回执闸、末章硬闸、执笔 flaws 俱无新红，方议第二步（一事一写、器分发）。

【其法】
  一、代填：记席於诸档以占位「‹器:键›」留格（键见 `--试` 首所印之表），本器以器算之值代之。
     键：白文止 亮点行 星 拍 星行 拍界 净重 六数 sha1 末版 台账版数 诸版 总纲 总纲行 日号 极短段 对白
         回执之数（§一首三条）终稿（创作记录 §五之首条）章料KB 记料KB 大审笔数 大审之笔 大审#号（一笔一键，如「大审#10」）。
  二、器直落（⛔占位）：圣经「已写 1—N 章·事件链」之题、旧锚「第 N 章必须从」行末〔已销（第N章已接写）〕；
     总览之题「至第 N 章」、本站「写至 N」、「读者之所欠（至 N）」；检察官 OPEN_BRIEF_CARD_SCHEMA[N+1]（据 canon open_brief 之
     required_state_cards 照其序代书一行；已在而与 canon 不合即红，⛔覆）；席记之「封版」段（缺则书「待 封版.py」）。
  三、代核（手写之机械格与器算不合即红）：回执 §一与创作记录 §五之 白文止／亮点行／＊与拍／六数／sha1·版；锁定行之 sha1；
     圣经之题与旧锚、N+1 之锚只一；总览三处；schema 与 canon；席记之章与段名；开镜卡问七须逐字含大审 --限 N+1 之每一笔；
     诸档余「‹器:…›」（键不识）。
  ⛔碰判断之格：坑账之答、冷眼轮、本章之失、全书记忆诸节、状态册、open_brief、开镜卡诸判断格、硬门槛、承前之判、教训。
  ⛔核全书记忆/第N章.md 之 sha1：封版 --後 之「全书记忆 --随」器随之（410 实踩：亮点添注而白文未动），记席可写 ‹器:sha1›。
  回放之「记席之时」：封版之提交里台账末尾之「定稿：正文与末版对齐（封版.py --前）」诸版係记席之後主环所存（410 之 v04、v05），
  回放截去之、以其前末一版为正文——405—410 六章之回执 sha1 俱与之合。

用法：
  python3 工具/记落.py N          # 代填、直落、代核；红则逐条「⛔ 节名：语」、退 1；绿则一行 ✓（只理 N≥411）
  python3 工具/记落.py N --试     # 只印诸键之值与 diff，⛔写（N≤410 亦可试：其档已封，只供看）
  python3 工具/记落.py N --重填   # X83：已填之格末版改後重填（以 _记落值.json 之席时之值为旧、现版为新，逐格换；後照常落与核）
  python3 工具/记落.py --自测     # 以 405—410 之真料回放（各取其封版之提交），器格与已封之档逐字比；并验代填、⛔写、负例
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, re, json, glob, time, difflib, subprocess, tempfile, io, tarfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
起 = 411                                   # ★N≤410 之章已封、其令旧式：⛔写
圣经 = os.path.join('设定', '00_镇冢秘术_唯一总圣经.md')
总览 = os.path.join('设定', '全书记忆', '总览.md')
施工表 = os.path.join('设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
总纲 = os.path.join('设定', '02_余章之势_总纲.md')
检察官 = os.path.join('工具', '小说检察官.py')
canon = os.path.join('设定', 'canon事实库.json')
造章 = os.path.join('工具', '席', '造章.js')
定稿之说 = '造式二代·定稿：正文与末版对齐'
占 = re.compile(r'‹器:([^›\n]{1,24})›')
_十 = '零一二三四五六七八九'


def 汉(k):
    """1—999 → 汉字之数（163→一百六十三、110→一百一十、105→一百零五）：日号与拍名之式。"""
    if k < 10:
        return _十[k]
    if k < 20:
        return '十' + (_十[k % 10] if k % 10 else '')
    if k < 100:
        return _十[k // 10] + '十' + (_十[k % 10] if k % 10 else '')
    百, 余 = divmod(k, 100)
    return _十[百] + '百' + ('' if not 余 else ('零' + _十[余]) if 余 < 10 else 汉(余) if 余 >= 20 else '一' + 汉(余))


def 读(p, root=ROOT):
    fp = os.path.join(root, p)
    return open(fp, encoding='utf-8').read() if os.path.exists(fp) else None


def 回执档(n, root=ROOT):
    回 = sorted(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % n)))
    return os.path.relpath(回[-1], root) if 回 else None


def 档们(n, root=ROOT):
    """记席所写、许留占位之诸档 → [(名, 路)]（路相对 root；回执未立者略）。"""
    出 = [('回执', 回执档(n, root)), ('施工表', 施工表), ('创作记录', os.path.join('版本', '第%d章' % n, '_创作记录.md')),
         ('全书记忆', os.path.join('设定', '全书记忆', '第%d章.md' % n)), ('总览', 总览), ('圣经', 圣经),
         ('轮记', os.path.join('版本', '第%d章' % n, '_轮记.md')), ('开镜卡', os.path.join('版本', '第%d章' % (n + 1), '_开镜卡.md')),
         ('席记', os.path.join('版本', '第%d章' % n, '_席记.json'))]
    return [(k, p) for k, p in 出 if p]


def 拍之界(文, 白止):
    """→ (「＊」之行们, [(起, 止)])：白文以「＊」切段，每段去首尾空行；首段起於题行（「第…章」）後首个非空行。"""
    L = 文.split('\n')
    题 = next((i for i, l in enumerate(L[:8]) if re.search(r'第.+?章', l)), -1)
    星 = [i + 1 for i, l in enumerate(L[:白止]) if l.strip() == '＊']
    界 = []
    for a, b in zip([题 + 2] + [s + 1 for s in 星], [s - 1 for s in 星] + [白止]):
        while a <= b and not L[a - 1].strip():
            a += 1
        while b >= a and not L[b - 1].strip():
            b -= 1
        界.append((a, b))
    return 星, 界


def 大审之笔(n, root=ROOT):
    """大审.py --限 n 之诸笔 → [(号, 限, 裁格)]——同一函（大审.限於），册目随 root（回放用旧册）。"""
    import 大审
    旧 = 大审.册目
    try:
        大审.册目 = os.path.join(root, '设定')
        return 大审.限於(n)
    finally:
        大审.册目 = 旧


def 值们(n, root=ROOT):
    """器格诸键 → 值（俱取器之印：封版.数、拍之界、封版.极短段、封版.对白之行、大审.限於、总纲之行、canon）。"""
    import 封版
    d = 封版.数(n, root)
    if d.get('坏'):
        raise ValueError(d['坏'])
    文 = open(os.path.join(root, d['正文']), encoding='utf-8').read()
    白止 = int(re.match(r'1 至 (\d+) 行', d['白文']).group(1))
    星, 界 = 拍之界(文, 白止)
    短, 共 = 封版.极短段(文)
    对 = 封版.对白之行(文.split('【本章亮点】')[0].split('\n'))
    v = {'白文止': str(白止), '亮点行': str(d['亮点行']), '星': str(d['＊']), '拍': str(d['拍']),
         '星行': '、'.join(':%d' % s for s in 星), '拍界': '｜'.join('拍%s :%d—%d' % (汉(i + 1), a, b) for i, (a, b) in enumerate(界)),
         '净重': str(d['净重']), '六数': d.get('六数', ''), 'sha1': d['sha1'], '末版': d.get('末版') or '',
         '诸版': '｜'.join(d.get('诸版', [])), '台账版数': 汉(len(d.get('诸版', []))),
         '极短段': '%d／%d＝%.1f%%' % (短, 共, 100.0 * 短 / 共 if 共 else 0.0),
         '对白': '③对白之行 %d' % len(对) + ('：' + '、'.join(':%d' % k for k, _ in 对[:40]) if 对 else '')}
    v['总纲'] = d.get('总纲') or ''
    纲 = (读(总纲, root) or '').split('\n')
    v['总纲行'] = str(next((i + 1 for i, l in enumerate(纲) if v['总纲'] and v['总纲'] in l), ''))
    m = re.match(r'\| \d+ \| ([主暗])·(\d+) \|', v['总纲'])
    v['日号'] = ('第%s%s' % (汉(int(m.group(2))), '天' if m.group(1) == '主' else '日')) if m else ''
    台 = json.load(open(os.path.join(root, '版本', '第%d章' % n, '_台账.json'), encoding='utf-8')).get('版本', []) \
        if os.path.exists(os.path.join(root, '版本', '第%d章' % n, '_台账.json')) else []
    v['回执之数'] = '\n'.join([
        '- 白文 **1—%s** 行，`【本章亮点】` 在第 **%s** 行；`封版.py --前` 印「＊：%s」「拍：%s」——「＊」在 %s，器以「＊」切%s段：%s。'
        % (v['白文止'], v['亮点行'], v['星'], v['拍'], v['星行'] or '（无）', 汉(len(界)), v['拍界']),
        '- **%s**（`封版.py %d --前`「六数」行）。' % (v['六数'], n),
        '- 正文 sha1 前十二 `%s`（%s）；台账%s版：%s。' % (v['sha1'], v['末版'], v['台账版数'],
                                              '｜'.join('%s「%s」' % (x.get('版'), x.get('说明', '')) for x in 台))])
    v['终稿'] = '- **终稿**：%s，sha1 `%s`；**%s**；白文 1—%s，亮点 %s；「＊」%s、器拍 %s；' % (
        v['末版'], v['sha1'], v['六数'], v['白文止'], v['亮点行'], v['星'], v['拍'])
    for 键, 档 in (('章料KB', '_料.md'), ('记料KB', '_记料.md')):
        p = os.path.join(root, '版本', '第%d章' % n, 档)
        v[键] = str(os.path.getsize(p) // 1024) if os.path.exists(p) else ''      # 与 记料.py 自印之「（%d KB）」同一把尺
    笔 = 大审之笔(n + 1, root)
    v['大审笔数'] = str(len(笔))
    v['大审之笔'] = '\n'.join('  - #%s 限%d｜%s' % x for x in 笔) or '  - （零笔）'
    for 号, 限, 裁 in 笔:
        v['大审#%s' % 号] = '#%s 限%d｜%s' % (号, 限, 裁)
    return v, 笔


def 段之文(t, 头):
    """md 之一节（「## 头…」起至下一「## 」止）；无则 ''。"""
    m = re.search(r'(?m)^## %s[^\n]*\n' % re.escape(头), t or '')
    if not m:
        return ''
    e = re.search(r'(?m)^## ', t[m.end():])
    return t[m.start(): m.end() + (e.start() if e else len(t) - m.end())]


def 问七(卡):
    """开镜卡之问七一节（「## …问七…」起至下一「## 」止）；无则全卡。"""
    m = re.search(r'(?m)^## [^\n]*问七[^\n]*\n', 卡 or '')
    if not m:
        return 卡 or ''
    e = re.search(r'(?m)^## ', 卡[m.end():])
    return 卡[m.start(): m.end() + (e.start() if e else len(卡) - m.end())]


def 号之覆(t):
    """问七所点之大审笔号（「#12」与「#1—#9」之段）→ {号}。回放之尺：410 前之卡逐号点、其裁之文多略（「……」）而⛔逐字——
    N≥411 之核则逐字（器代填 ‹器:大审#号›）。"""
    出 = set(re.findall(r'#(\d+)(?!\d)', t))
    for a, b in re.findall(r'#(\d+)\s*[—–\-~～至]\s*#?(\d+)', t):
        出 |= {str(k) for k in range(int(a), int(b) + 1)}
    return 出


# ── 器直落 ──
def 圣经之落(t, n):
    t = re.sub(r'(?m)^(## 十一、已写 1—)%d( 章·事件链)' % (n - 1), r'\g<1>%d\2' % n, t, count=1)
    return re.sub(r'(?m)^(\*\*第 %d 章必须从\*\*[^\n]*?接写)[ \t]*$' % n, r'\1〔已销（第%d章已接写）〕' % n, t)


def 总览之落(t, n):
    t = re.sub(r'(?m)^# 全书记忆·总览（至第 %d 章）' % (n - 1), '# 全书记忆·总览（至第 %d 章）' % n, t, count=1)
    # ★1109（434 记席逮）：旧取首个「写至 N-1」——E7 起而 E6 之题仍被逐章推（E6 写至 433、E7 停在 429）；
    #   今只推档中末一站（末一「### …写至 K）」与末一「- **…读者之所欠（至 K）**」），K<n 方推
    def _末推(式, t):
        ms = list(re.finditer(式, t))
        if not ms or int(ms[-1].group(2)) >= n:
            return t
        m = ms[-1]
        return t[:m.start(2)] + str(n) + t[m.end(2):]
    t = _末推(r'(?m)^(### [^\n]*写至 )(\d+)）', t)
    return _末推(r'(?m)^(- \*\*(?:E\d+ )?读者之所欠（至 )(\d+)）', t)


def schema之行(n, root=ROOT):
    """canon open_brief → 检察官 OPEN_BRIEF_CARD_SCHEMA[n+1] 之一行（照 required_state_cards 之序）；for_ch 不为 n+1 → None。"""
    ob = json.load(open(os.path.join(root, canon), encoding='utf-8')).get('open_brief') or {}
    if ob.get('for_ch') != n + 1 or not ob.get('required_state_cards'):
        return None
    return '    %d: (%s),' % (n + 1, ', '.join(repr(x) for x in ob['required_state_cards']))


def schema之落(t, n, root=ROOT):
    行 = schema之行(n, root)
    if not 行 or re.search(r'(?m)^    %d: \(' % (n + 1), t):
        return t
    m = re.search(r'(?m)^    %d: \([^\n]*\n' % n, t)
    if not m:
        return t
    注 = '    # ★%s·第%d章记席（造式二代）插：记落.py 据 canon open_brief.required_state_cards 代书（%d 判之由见施工表 `| %d | 锁定 |` 与圣经 %d 之锚）\n' % (
        time.strftime('%Y-%m-%d', time.gmtime()), n, n + 1, n, n + 1)
    return t[:m.end()] + 注 + 行 + '\n' + t[m.end():]


def 席记之落(t, n):
    try:
        j = json.loads(t)
    except Exception:
        return t
    if isinstance(j.get('段'), dict) and not j['段'].get('封版'):
        j['段']['封版'] = '待 封版.py'
        return json.dumps(j, ensure_ascii=False, indent=1)
    return t


def 代填(t, v, js=False):
    """‹器:键› → 值；键不识者留原样（核时报红）。→ (新文, 填数)。"""
    数 = [0]
    def _换(m):
        k = m.group(1)
        if k not in v:
            return m.group(0)
        数[0] += 1
        return json.dumps(v[k], ensure_ascii=False)[1:-1] if js else v[k]
    return 占.sub(_换, t), 数[0]


# ── 代核 ──
def 核(n, 文们, v, 笔, root=ROOT, 回放=False):
    """文们：{名: 文}（已填已落者）→ 诸红 [(节名, 语)]。回放：⛔核席记之「封版」（--後 已覆）。"""
    红 = []
    def 同(节, 名, 手, 器):
        if 手 is not None and str(手) != str(器):
            红.append((节, '%s 手书「%s」与器「%s」不合' % (名, 手, 器)))
    def 格(节, t, 必=True):
        if not t:
            return
        m = re.search(r'白文 \*\*1—(\d+)\*\* 行', t) or re.search(r'白文 1—(\d+)[，,]', t)
        同(节, '白文止', m and m.group(1), v['白文止'])
        m = re.search(r'`【本章亮点】` 在第 \*\*(\d+)\*\* 行', t) or re.search(r'白文 1—\d+[，,]亮点 (\d+)', t)
        同(节, '亮点行', m and m.group(1), v['亮点行'])
        m = re.search(r'「＊：(\d+)」「拍：(\d+)」', t) or re.search(r'「＊」(\d+)、器拍 (\d+)', t)
        if m:
            同(节, '＊', m.group(1), v['星']); 同(节, '拍', m.group(2), v['拍'])
        m = re.search(r'\*\*(净重\d+｜段数[^*\n]+)\*\*', t)
        同(节, '六数', m and m.group(1), v['六数'])
        m = re.search(r'sha1 (?:前十二 )?`([0-9a-f]{12})`', t)
        同(节, 'sha1', m and m.group(1), v['sha1'])
        m = re.search(r'sha1 前十二 `[0-9a-f]{12}`（(v\d+)）', t) or re.search(r'\*\*终稿\*\*：(v\d+)', t)
        同(节, '末版', m and m.group(1), v['末版'])
        m = re.search(r'台账([一二三四五六七八九十]+)版', t)
        同(节, '台账版数', m and m.group(1), v['台账版数'])
        if 必 and not re.search(r'sha1 (?:前十二 )?`[0-9a-f]{12}`', t):
            红.append((节, '缺 sha1 之格（写 ‹器:sha1› 或 ‹器:%s›）' % ('回执之数' if 节.startswith('回执') else '终稿')))
    格('回执§一', 段之文(文们.get('回执'), '一'))
    格('创作记录§五', 段之文(文们.get('创作记录'), '五'))
    锁 = next((l for l in (文们.get('施工表') or '').split('\n') if l.startswith('| %d | 锁定 |' % n)), None)
    if 锁:
        m = re.search(r'sha1 `([0-9a-f]{12})`', 锁)
        同('锁定行', 'sha1', m and m.group(1), v['sha1'])
    经 = 文们.get('圣经')
    if 经 is not None:
        if not re.search(r'(?m)^## 十一、已写 1—%d 章·事件链' % n, 经):
            红.append(('圣经', '事件链之题不为「已写 1—%d 章」' % n))
        旧 = re.findall(r'(?m)^\*\*第 %d 章必须从\*\*[^\n]*$' % n, 经)
        if any('〔已销' not in x for x in 旧):
            红.append(('圣经', '旧锚「第 %d 章必须从」未加〔已销（第%d章已接写）〕' % (n, n)))
        锚 = [x for x in re.findall(r'(?m)^\*\*第 %d 章必须从\*\*[^\n]*$' % (n + 1), 经) if '〔已销' not in x]
        if len(锚) != 1:
            红.append(('圣经', '第 %d 章之锚 %d 个（须只一个，记席立）' % (n + 1, len(锚))))
    览 = 文们.get('总览')
    if 览 is not None:
        for 式, 语 in ((r'(?m)^# 全书记忆·总览（至第 %d 章）' % n, '题不为「至第 %d 章」' % n),
                       (r'(?m)^### [^\n]*写至 %d）' % n, '本站之「写至 %d」不在' % n),
                       (r'(?m)^- \*\*(?:E\d+ )?读者之所欠（至 %d）' % n, '「读者之所欠（至 %d）」不在' % n)):
            if not re.search(式, 览):
                红.append(('总览', 语))
    检 = 文们.get('检察官')
    if 检 is not None:
        行 = schema之行(n, root)
        有 = re.search(r'(?m)^    %d: \([^\n]*$' % (n + 1), 检)
        if not 行:
            红.append(('检察官schema', 'canon open_brief.for_ch 不为 %d 或 required_state_cards 空' % (n + 1)))
        elif not 有:
            红.append(('检察官schema', 'OPEN_BRIEF_CARD_SCHEMA 缺 %d 之行' % (n + 1)))
        elif 有.group(0) != 行:
            红.append(('检察官schema', '%d 之行与 canon required_state_cards 不合（器：%s）' % (n + 1, 行.strip()[:200])))
    席 = 文们.get('席记')
    if 席 is not None:
        try:
            j = json.loads(席)
            段名 = re.findall(r"'([^']+)'", re.search(r'const 造式之段 = \[([^\]]*)\]', 读(造章, ROOT)).group(1))
            if j.get('章') != n:
                红.append(('席记', '「章」为 %r，不为 %d' % (j.get('章'), n)))
            if list((j.get('段') or {}).keys()) != 段名:
                红.append(('席记', '段名 %s 与 造章.js 造式之段 %s 不合' % ('、'.join(j.get('段') or {}), '、'.join(段名))))
            if not 回放 and not (j.get('段') or {}).get('封版'):
                红.append(('席记', '「封版」段空'))
        except Exception as e:
            红.append(('席记', 'JSON 坏（%s）' % e))
    卡 = 文们.get('开镜卡')
    if 卡 is not None:
        七 = 问七(卡)
        缺 = [x for x in 笔 if x[0] not in 号之覆(七)] if 回放 else [x for x in 笔 if ('#%s 限%d｜%s' % x) not in 七]
        if 缺:
            红.append(('开镜卡问七', '大审 --限 %d 之笔未%s者 %d：%s（写 ‹器:大审#号› 代之）' % (
                n + 1, '点其号' if 回放 else '逐字抄', len(缺), '、'.join('#%s' % x[0] for x in 缺))))
    for 名, t in 文们.items():
        余 = sorted(set(占.findall(t or '')))
        if 余:
            红.append((名, '占位之键不识：%s' % '、'.join(余)))
        判 = 判占.findall(t or '')
        if 判:
            红.append((名, '回执之骨之判未填 %d 处（X109·‹判›）：%s' % (len(判), '、'.join(sorted(set(判)))[:120])))
    return 红


def 落(n, root=ROOT, 试=False, 印=print):
    """代填、直落、代核 → 诸红；试：只印值与 diff、⛔写。"""
    v, 笔 = 值们(n, root)
    if 试:
        印('· 器格（‹器:键›）：')
        for k in sorted(v, key=lambda x: (x.startswith('大审#'), x)):
            印('    %s＝%s' % (k, v[k].replace('\n', '⏎')[:160]))
    文们, 改, 填 = {}, [], 0
    for 名, p in 档们(n, root) + [('检察官', 检察官)]:
        t = 读(p, root)
        if t is None:
            continue
        新, k = 代填(t, v, js=p.endswith('.json'))
        填 += k
        if 名 == '圣经':
            新 = 圣经之落(新, n)
        elif 名 == '总览':
            新 = 总览之落(新, n)
        elif 名 == '检察官':
            新 = schema之落(新, n, root)
        elif 名 == '席记':
            新 = 席记之落(新, n)
        文们[名] = 新
        if 新 != t:
            改.append((名, p, t, 新))
    红 = 核(n, 文们, v, 笔, root)
    for 名, p, t, 新 in 改:
        if 试:
            差 = list(difflib.unified_diff(t.split('\n'), 新.split('\n'), p, p + '（记落）', n=0, lineterm=''))
            印('\n'.join(l[:300] for l in 差[:60]) + ('\n    ……（diff 余 %d 行）' % (len(差) - 60) if len(差) > 60 else ''))
        else:
            open(os.path.join(root, p), 'w', encoding='utf-8').write(新)
    if not 试:                                   # ★X83：席时之值留档——末版改後 --重填 以之为旧
        json.dump(v, open(os.path.join(root, 值档 % n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
    for 节, 语 in 红:
        印('⛔ %s：%s' % (节, 语))
    if not 红:
        印('✓ 记落 %d%s：代填 %d 格、落 %d 档（%s），核俱合' % (n, '·试（⛔写）' if 试 else '', 填, len(改), '、'.join(x[0] for x in 改) or '无改'))
    return 红


# ── X109（1117·460 起）：回执之骨——记席 455—459 回执一 Write 通篇自拟（$2.9—3.1、12 回、逾配额 5%），器先立骨、记席只填判 ──
骨起 = 460
判占 = re.compile(r'‹判[^›\n]{0,24}›')


def 骨(n, root=ROOT, 日=None):
    """立「设定/回执_<日>_第n章封版席.md」之骨（已有回执即⛔覆、返 None）：节目照前章回执（章号随移）；§一 写器格占位；
    余节之「- **键**」「N. **题**」「> **式…**」留其键与题、判写 ‹判›；无键之节留 ‹判·节›；归封版之节（§十六）照抄。返其路。"""
    if 回执档(n, root):
        return None
    前 = 回执档(n - 1, root)
    if not 前:
        return None
    t = 读(前, root)
    日 = 日 or time.strftime('%Y%m%d')
    号 = lambda s: re.sub(r'(?<!\d)(%d|%d)(?!\d)' % (n, n - 1), lambda m: str(int(m.group(1)) + 1), s)
    出 = ['# 回执 · 第%d章《‹判·题›》封版席（记席·造式二代·%s-%s-%s）' % (n, 日[:4], 日[4:6], 日[6:]), '']
    节, 有 = None, 0
    def 收():
        if 节 is not None and not 有:
            出.append('‹判·%s›' % re.sub(r'^## ([^·]+)·.*$', r'\1', 节))
            出.append('')
    for l in t.split('\n')[1:]:
        if l.startswith('## '):
            收()
            if 出[-1] != '':
                出.append('')
            节, 有 = l, 0
            出.extend([号(l), ''])
            if l.startswith('## 一·'):
                出.extend(['‹器:回执之数›', '- **品**：‹判›；**层**：‹判›', '- **极短段**：‹器:极短段›；‹判·极短段›',
                          '- **对白**：‹器:对白›；‹判·对白›', '']); 有 = 1
            elif l.startswith('## 八·'):
                出.extend(['器拍：‹器:拍界›（「＊」在 ‹器:星行›）', '‹判·八›', '']); 有 = 1
            elif l.startswith('## 九·'):
                出.extend(['- 总纲：‹器:总纲›；日号：‹器:日号›（‹判·日号›）', '‹判·九›', '']); 有 = 1
            continue
        if 节 is None:
            m = re.match(r'^> (\*\*[^*]+\*\*)', l)
            if m:
                出.extend(['> %s：‹判›' % m.group(1), ''])
            continue
        if 节.startswith(('## 一·', '## 八·', '## 九·')) or '本章之失' in 节 or '交总编辑' in 节:     # 本章特有之节⛔袭前章之条
            continue
        if '归 `封版.py`' in 节:
            if l.strip():
                出.append(号(l)); 有 = 1
            continue
        m = re.match(r'^(- \*\*[^*]+\*\*|\d+\. \*\*[^*]+\*\*)', l)
        if m:
            出.append(号(m.group(1)) + ('——' if m.group(1)[0].isdigit() else '：') + '‹判›'); 有 = 1
        elif not l.strip() and 有 and 出[-1] != '':
            出.append('')
    收()
    p = os.path.join('设定', '回执_%s_第%d章封版席.md' % (日, n))
    open(os.path.join(root, p), 'w', encoding='utf-8').write('\n'.join(出).rstrip() + '\n')
    return p


值档 = os.path.join('版本', '第%d章', '_记落值.json')


def 换值(t, 对, js=False):
    """→ (新文, 换数)：对＝[(旧, 新)]，长者先换（复合之格含短者）；js 则换其 JSON 转义之形。"""
    k = 0
    for 旧, 新 in sorted(对, key=lambda x: -len(x[0])):
        a, b = (json.dumps(旧, ensure_ascii=False)[1:-1], json.dumps(新, ensure_ascii=False)[1:-1]) if js else (旧, 新)
        k += t.count(a); t = t.replace(a, b)
    return t, k


def 可换(旧):
    """旧值须独有方许逐字换：长 ≥6 且非纯数（sha1、六数、回执之数、终稿、星行、拍界、对白、诸版……）。
    纯数之短格（白文止、亮点行、净重……）⛔单换（「107」处处有）——其值俱在复合之格内随之换；余者 代核 照红。"""
    return len(旧) >= 6 and not re.fullmatch(r'[\d,，.]+', 旧)


def 重填(n, root=ROOT, 印=print):
    """X83（418 记席六回手改）：已填之格末版改後重填——以 _记落值.json（席时之值）为旧、现版之值为新，诸档逐格换；後照常 落（代填、直落、代核）。"""
    p = os.path.join(root, 值档 % n)
    if not os.path.exists(p):
        印('⛔ 重填：无席时之值（%s）——记落未曾真落；照常 `记落.py %d`' % (值档 % n, n)); return [('重填', '无席时之值')]
    旧 = json.load(open(p, encoding='utf-8'))
    新, _ = 值们(n, root)
    对 = [(旧[k], 新[k]) for k in 新 if k in 旧 and 旧[k] != 新[k] and 可换(旧[k])]
    共 = 0
    for 名, q in 档们(n, root):
        t = 读(q, root)
        if t is None:
            continue
        x, k = 换值(t, 对, js=q.endswith('.json'))
        if k:
            open(os.path.join(root, q), 'w', encoding='utf-8').write(x); 共 += k
            印('  · %s：换 %d 处' % (名, k))
    印('· 重填 %d：变之格 %d（%s）、换 %d 处' % (n, len(对), '、'.join(k for k in 新 if k in 旧 and 旧[k] != 新[k]) or '无', 共))
    return 落(n, root, 印=印)


# ── 回放（--自测）──
def 封之提交(n, root=ROOT):
    return subprocess.run(['git', 'log', '--all', '--format=%H', '-1', '--grep', '^第%d章.*（造式二代·封版#%d）' % (n, n)], cwd=root,   # 锚题首：後之提交引其号⛔误取
                          capture_output=True, text=True).stdout.strip()


def 取(提交, 路们, 目, root=ROOT):
    a = subprocess.run(['git', 'archive', 提交] + 路们, cwd=root, capture_output=True)
    if a.returncode:
        raise RuntimeError(a.stderr.decode('utf-8', 'replace')[:200])
    tarfile.open(fileobj=io.BytesIO(a.stdout)).extractall(目)


def 席时之态(n, 目):
    """记席跑 封版 --前 时之态：台账截至「席时之版」，正文复为其版。席时之版＝诸版中正文 sha1 与回执所书合者
    （回执所书之 sha 即记席所见之正文：408 之 v03 係记席自跑 --前 所存）；无合者，截去末尾诸「定稿对齐」版
    （410 之 v04、v05 係记席之後主环添注所存）。其余诸格（白文止、六数、＊、拍界、大审）俱据此版逐字比。"""
    import 封版
    p = os.path.join(目, '版本', '第%d章' % n, '_台账.json')
    j = json.load(open(p, encoding='utf-8'))
    vs = j.get('版本', [])
    回 = 回执档(n, 目)
    m = re.search(r'sha1 前十二 `([0-9a-f]{12})`', 段之文(读(回, 目), '一')) if 回 else None
    import hashlib
    合 = [i for i, x in enumerate(vs) if m and os.path.exists(os.path.join(目, '版本', '第%d章' % n, '%s.md' % x.get('版'))) and
          hashlib.sha1(open(os.path.join(目, '版本', '第%d章' % n, '%s.md' % x.get('版')), 'rb').read()).hexdigest()[:12] == m.group(1)]
    if 合:
        del vs[合[-1] + 1:]
    while not 合 and len(vs) > 1 and str(vs[-1].get('说明', '')).startswith(定稿之说):
        vs.pop()
    json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    shutil.copyfile(os.path.join(目, '版本', '第%d章' % n, '%s.md' % vs[-1]['版']), 封版.正文档(n, 目))


def 回放(n, root=ROOT):
    """→ (诸比 [(名, ok, 语)], 核之红)。器格与第 n 章封版之提交之档逐字比；圣经／总览之直落施於其父提交之档。"""
    C = 封之提交(n, root)
    if not C:
        return [('封版之提交', False, '第%d章无「封版#%d）」之提交' % (n, n))], []
    目, 父 = tempfile.mkdtemp(prefix='记落_'), tempfile.mkdtemp(prefix='记落父_')
    try:
        取(C, ['正文', '版本/第%d章' % n, '版本/第%d章/_开镜卡.md' % (n + 1), 总纲, 圣经, 总览, 施工表, canon, 检察官,
               '设定/全书记忆/第%d章.md' % n], 目, root)
        大审们 = [l for l in subprocess.run(['git', 'ls-tree', '--name-only', C, '设定/'], cwd=root, capture_output=True,
                                            text=True).stdout.split('\n') if re.search(r'设定/(大审_至第\d+章\.md|回执_\d+_第%d章封版席\.md)$' % n, l)]
        取(C, 大审们, 目, root)
        取(C + '^', [圣经, 总览], 父, root)
        席时之态(n, 目)
        v, 笔 = 值们(n, 目)
        文们 = {名: 读(p, 目) for 名, p in 档们(n, 目) + [('检察官', 检察官)]}
        比 = []
        一 = 段之文(文们['回执'], '一')
        for 片 in ('白文 **1—%s** 行' % v['白文止'], '`【本章亮点】` 在第 **%s** 行' % v['亮点行'],
                   '「＊：%s」「拍：%s」' % (v['星'], v['拍']), '「＊」在 %s' % v['星行'], '器以「＊」切%s段：%s' % (汉(int(v['拍'])), v['拍界']),
                   '**%s**（`封版.py %d --前`「六数」行）' % (v['六数'], n), '正文 sha1 前十二 `%s`' % v['sha1'],
                   '**%s**' % v['极短段'], '器印「%s' % v['对白']):
            比.append(('回执§一 %s' % 片[:40], 片 in 一, ''))
        比.append(('回执 日号', v['日号'] in 文们['回执'] and v['总纲'] in 文们['回执'], v['日号'] + ' ' + v['总纲']))
        比.append(('锁定行 sha1', ('sha1 `%s`' % v['sha1']) in next((l for l in 文们['施工表'].split('\n') if l.startswith('| %d | 锁定 |' % n)), ''), ''))
        for 名, 落之, 式们 in (('圣经', 圣经之落, [r'## 十一、已写 1—%d 章·事件链' % n, r'\*\*第 %d 章必须从\*\*' % n]),
                              ('总览', 总览之落, [r'# 全书记忆·总览（至第 %d 章）' % n, r'### [^\n]*写至 %d）' % n])):
            器文 = 落之(读(圣经 if 名 == '圣经' else 总览, 父), n)
            for 式 in 式们:
                器行 = re.search('(?m)^' + 式 + '[^\n]*$', 器文)
                比.append(('%s 「%s」之行' % (名, 式[:24].replace('\\', '')), bool(器行) and (器行.group(0) + '\n') in (文们[名] + '\n'),
                           (器行.group(0)[:80] if 器行 else '器落不出')))
        _欠 = re.compile(r'(?m)^- \*\*(?:E\d+ )?读者之所欠（至 %d）\*\*' % n)
        比.append(('总览「读者之所欠（至 %d）」' % n, bool(_欠.search(总览之落(读(总览, 父), n))) and bool(_欠.search(文们['总览'])), ''))
        行 = schema之行(n, 目)
        比.append(('检察官 schema %d 之行' % (n + 1), bool(行) and ('\n' + 行 + '\n') in 文们['检察官'], (行 or '')[:80]))
        j = json.loads(文们['席记'])
        比.append(('席记之章与段名', j.get('章') == n and list(j['段']) == ['料', '造', '选', '合', '验', '记', '封版'], ''))
        七 = 问七(文们['开镜卡'])
        比.append(('开镜卡问七 大审 %d 笔之号' % len(笔), all(x[0] in 号之覆(七) for x in 笔),
                   '、'.join('#%s' % x[0] for x in 笔 if x[0] not in 号之覆(七))))
        比.append(('回执之数 首三条俱含其器片', all(x in v['回执之数'] for x in ('**%s**' % v['六数'], '`%s`（%s）' % (v['sha1'], v['末版']))), ''))
        return 比, 核(n, 文们, v, 笔, 目, 回放=True)
    finally:
        shutil.rmtree(目, ignore_errors=True); shutil.rmtree(父, ignore_errors=True)


# 回放之真红（已封之档之手写之误，器逮之——以之为「不合即红」之真例；⛔为之改器格）
#   408：记席首跑 --前 时正文已异於 v02（其 --前 当场存 v03）；回执书 v03 之 sha 而标「v02」「台账二版」，创作记录书 v02 之六数与版。
回放之真红 = {408: [('回执§一', '末版 手书「v02」与器「v03」不合'), ('回执§一', '台账版数 手书「二」与器「三」不合'),
                    ('创作记录§五', '六数 手书「净重2610｜段数47｜长段数7｜嗅0｜触21｜四字串三现2」与器「净重2629｜段数47｜长段数7｜嗅0｜触21｜四字串三现2」不合'),
                    ('创作记录§五', '末版 手书「v02」与器「v03」不合')]}


def 自测():
    共 = ok = 0
    def 验(名, 真, 语=''):
        nonlocal 共, ok
        共 += 1; ok += bool(真)
        if not 真:
            print('  ✗ %s %s' % (名, 语))
    # ①汉数与拍界
    验('汉数', [汉(k) for k in (5, 10, 13, 20, 105, 110, 156, 163)] == ['五', '十', '十三', '二十', '一百零五', '一百一十', '一百五十六', '一百六十三'])
    验('拍界', 拍之界('《书》\n\n第一章　甲\n\n一\n\n二\n\n＊\n\n三\n\n＊\n\n四\n', 16) == ([9, 13], [(5, 7), (11, 11), (15, 15)]))
    # ②回放 405—410：器格与已封之档逐字比；核之红只许为已录之真红
    for n in range(405, 411):
        try:
            比, 红 = 回放(n)
        except Exception as e:
            验('回放 %d' % n, False, '崩：%s' % e); continue
        for 名, 真, 语 in 比:
            验('回放 %d·%s' % (n, 名), 真, 语)
        验('回放 %d·核之红＝已录之真红' % n, 红 == 回放之真红.get(n, []), '；'.join('%s：%s' % x for x in 红)[:400])
    # ③代填、直落、⛔写、负例——於 410 之席时之态之副本
    C = 封之提交(410)
    目, 父 = tempfile.mkdtemp(prefix='记落测_'), tempfile.mkdtemp(prefix='记落测父_')
    try:
        取(C, ['正文', '版本/第410章', '版本/第411章/_开镜卡.md', 总纲, 施工表, canon, 检察官, '设定/全书记忆/第410章.md'], 目)
        取(C, [l for l in subprocess.run(['git', 'ls-tree', '--name-only', C, '设定/'], cwd=ROOT, capture_output=True, text=True).stdout.split('\n')
               if re.search(r'设定/(大审_至第\d+章\.md|回执_\d+_第410章封版席\.md)$', l)], 目)
        取(C + '^', [圣经, 总览, 检察官], 父)
        席时之态(410, 目)
        for p in (圣经, 总览):
            shutil.copyfile(os.path.join(父, p), os.path.join(目, p))           # 记席之前之圣经、总览：器直落其题与旧锚
        v, 笔 = 值们(410, 目)
        回 = 回执档(410, 目)
        原回 = 读(回, 目)
        一 = 段之文(原回, '一')
        新一 = '## 一·本章之数（器出）\n\n‹器:回执之数›\n- 日号：‹器:日号›（`总纲:‹器:总纲行›`「‹器:总纲›」）\n\n'
        open(os.path.join(目, 回), 'w', encoding='utf-8').write(原回.replace(一, 新一))
        open(os.path.join(目, 圣经), 'a', encoding='utf-8').write('\n**第 411 章必须从**405 之末那一句（**甲**）接写\n')
        卡 = os.path.join(目, '版本', '第411章', '_开镜卡.md')
        原卡 = 读(卡, 目)
        open(卡, 'w', encoding='utf-8').write(原卡.replace(问七(原卡), '## ★★★★★问七·器格之测\n' + ''.join('  - ‹器:大审#%s›——判\n' % x[0] for x in 笔) + '‹器:乱键›\n\n'))
        前 = {p: 读(p, 目) for p in (回, 圣经, 总览)}
        印们 = []
        红 = 落(410, 目, 试=True, 印=印们.append)
        验('试·⛔写', all(读(p, 目) == t for p, t in 前.items()))
        验('试·印 diff 与器格', any(l.startswith('· 器格') for l in 印们) and any('〔已销（第410章已接写）〕' in l for l in 印们))
        验('核·不识之键报红', ('开镜卡', '占位之键不识：乱键') in 红, str(红)[:300])
        验('核·schema 缺 411 报红（父之检察官）', any(x[0] == '检察官schema' for x in 核(410, {'检察官': 读(检察官, 父)}, v, 笔, 目)))
        验('schema之落·代书一行', (schema之行(410, 目) + '\n') in schema之落(读(检察官, 父), 410, 目))
        t = 读(卡, 目)                                                   # 先读後写（open(…,'w') 先截档）
        open(卡, 'w', encoding='utf-8').write(t.replace('‹器:乱键›', ''))
        红 = 落(410, 目, 印=印们.append)
        新回 = 读(回, 目)
        验('真落·回执之数代填', v['回执之数'] in 新回 and '‹器:' not in 新回 and v['日号'] in 新回, str(红)[:300])
        验('真落·圣经之题与旧锚', re.search(r'(?m)^## 十一、已写 1—410 章·事件链', 读(圣经, 目)) and '接写〔已销（第410章已接写）〕' in 读(圣经, 目))
        _两站 = ('# 全书记忆·总览（至第 433 章）\n### E6 某（约 396—425；写至 433）\n- **读者之所欠（至 433）**：甲\n'
                 '### E7 某（约 426—450；写至 429）\n- **E7 读者之所欠（至 428）**：乙\n')
        _落 = 总览之落(_两站, 434)
        验('总览只推末一站（434 逮：E6 之题被推、E7 停）', 'E6 某（约 396—425；写至 433）' in _落 and '读者之所欠（至 433）**：甲' in _落
            and 'E7 某（约 426—450；写至 434）' in _落 and 'E7 读者之所欠（至 434）**：乙' in _落 and 总览之落(_落, 434) == _落)
        验('真落·总览三处', '# 全书记忆·总览（至第 410 章）' in 读(总览, 目) and '写至 410）' in 读(总览, 目) and '读者之所欠（至 410）' in 读(总览, 目))
        验('真落·大审诸笔', all(('#%s 限%d｜%s——判' % x) in 读(卡, 目) for x in 笔))
        验('真落·绿', 红 == [], str(红)[:300])
        验('幂等·重落无改', 落(410, 目, 印=lambda s: None) == [] and 读(回, 目) == 新回)
        # 负例：手书之机械格与器不合即红
        open(os.path.join(目, 回), 'w', encoding='utf-8').write(新回.replace('`%s`' % v['sha1'], '`0123456789ab`', 1))
        验('负例·回执 sha1 不合', any(x[0] == '回执§一' and 'sha1' in x[1] for x in 落(410, 目, 试=True, 印=lambda s: None)))
        open(os.path.join(目, 回), 'w', encoding='utf-8').write(新回.replace('白文 **1—67** 行', '白文 **1—66** 行'))
        验('负例·白文止不合', any(x[0] == '回执§一' and '白文止' in x[1] for x in 落(410, 目, 试=True, 印=lambda s: None)))
        open(os.path.join(目, 回), 'w', encoding='utf-8').write(新回)
        t = 读(卡, 目)
        open(卡, 'w', encoding='utf-8').write(t.replace('#%s 限%d｜%s' % 笔[0], '#%s 限%d｜%s' % (笔[0][0], 笔[0][1], 笔[0][2][:20])) if 笔 else t)
        验('负例·大审之笔截半句', (not 笔) or any(x[0] == '开镜卡问七' for x in 落(410, 目, 试=True, 印=lambda s: None)))
        open(os.path.join(目, 圣经), 'a', encoding='utf-8').write('\n**第 411 章必须从**乙之末那一句（**乙**）接写\n')
        验('负例·411 之锚两个', any(x[0] == '圣经' and '锚 2 个' in x[1] for x in 落(410, 目, 试=True, 印=lambda s: None)))
        # ★X83：末版改後 --重填——白文改一字（正文与末版同改）→ 试即红（sha1 不合）→ 重填 → 绿、回执载新 sha1、⛔留旧
        _圣 = 读(圣经, 目).replace('\n**第 411 章必须从**乙之末那一句（**乙**）接写\n', '')     # 先读後写
        open(os.path.join(目, 圣经), 'w', encoding='utf-8').write(_圣)
        open(卡, 'w', encoding='utf-8').write(t)
        落(410, 目, 印=lambda s: None)
        旧v = json.load(open(os.path.join(目, 值档 % 410), encoding='utf-8'))
        import 封版 as _封
        _d = _封.数(410, 目)
        for q in {_d['正文'], os.path.join('版本', '第410章', '%s.md' % _d['末版'])}:
            _t = 读(q, 目); _i = _t.index('。', 200)
            open(os.path.join(目, q), 'w', encoding='utf-8').write(_t[:_i] + '，' + _t[_i + 1:])
        验('重填·改後未重填即红', any('sha1' in x[1] for x in 落(410, 目, 试=True, 印=lambda s: None)))
        _红 = 重填(410, 目, 印=lambda s: None)
        _新v = json.load(open(os.path.join(目, 值档 % 410), encoding='utf-8'))
        验('重填·绿而回执载新 sha1、⛔留旧', _红 == [] and _新v['sha1'] != 旧v['sha1'] and _新v['sha1'] in 读(回, 目) and 旧v['sha1'] not in 读(回, 目), str(_红)[:300])
        验('重填·纯数短格⛔单换', not 可换('107') and not 可换('2,629') and 可换(旧v['sha1']) and 换值('a107b', [('107', '9')]) == ('a9b', 1))
        os.remove(os.path.join(目, 值档 % 410))
        验('重填·无席时之值即红', 重填(410, 目, 印=lambda s: None) == [('重填', '无席时之值')])
        # ★X109：回执之骨——节目随前章、§一器格、判占未填即红、已有回执⛔覆
        _骨目 = tempfile.mkdtemp(); os.makedirs(os.path.join(_骨目, '设定'))
        open(os.path.join(_骨目, '设定', '回执_20261101_第409章封版席.md'), 'w', encoding='utf-8').write(
            '# 回执 · 第409章《甲》封版席\n\n> **式：虫洞**：乙\n\n## 一·本章之数（器出）\n\n- 白文 **1—9** 行\n\n## 二·检察官回执诸项\n\n- **章魂**：丙\n'
            '- **五钩**：丁\n\n## 四·本章之失\n\n1. **读误**——戊\n\n## 八·锁定行逐拍之落处\n\n器拍：己\n\n## 十三·410 开镜卡\n\n- **锚之取**：庚\n\n'
            '## 十六·归 `封版.py` 之事（本坐⛔办）\n\n- 俱归 `python3 工具/封版.py 409 --後`。\n')
        _p = 骨(410, _骨目, '20261102'); _t = 读(_p, _骨目)
        验('骨·立', _p and '‹器:回执之数›' in _t and '- **章魂**：‹判›' in _t and '## 十三·411 开镜卡' in _t and '封版.py 410 --後' in _t
            and '读误' not in _t and '丙' not in _t and '‹器:拍界›' in _t and 骨(410, _骨目) is None, _t[:300])
        验('骨·判未填即红', any('‹判›' in x[1] for x in 核(410, {'回执': _t}, v, [], _骨目)))
        shutil.rmtree(_骨目, ignore_errors=True)
        验('N≤410 ⛔写', subprocess.run([sys.executable, os.path.abspath(__file__), '410'], capture_output=True, text=True).returncode == 2)
    finally:
        shutil.rmtree(目, ignore_errors=True); shutil.rmtree(父, ignore_errors=True)
    print('%s 记落·自测 %d/%d' % ('✓' if ok == 共 else '⛔', ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a and a[0].isdigit() and a[1:] == ['--重填']:
        if int(a[0]) < 起:
            print('⛔ 记落：只理 N≥%d' % 起); sys.exit(2)
        try:
            sys.exit(1 if 重填(int(a[0])) else 0)
        except Exception as e:
            print('⛔ 记落·重填：器格算不出（%s）' % e); sys.exit(1)
    if a and a[0].isdigit() and a[1:] == ['--骨']:
        p = 骨(int(a[0]))
        print('✓ 回执之骨：%s（只以 Edit 填 ‹判›·X109）' % p if p else '· 回执之骨：已有回执或无前章回执，⛔立')
        sys.exit(0)
    if a and a[0].isdigit() and set(a[1:]) <= {'--试'}:
        N, 试 = int(a[0]), '--试' in a
        if N < 起 and not 试:
            print('⛔ 记落：只理 N≥%d（≤%d 之章已封、其令旧式）；看可 --试' % (起, 起 - 1)); sys.exit(2)
        try:
            红 = 落(N, 试=试)
        except Exception as e:
            print('⛔ 记落：器格算不出（%s）' % e); sys.exit(1)
        sys.exit(1 if 红 else 0)
    print(__doc__); sys.exit(2)
