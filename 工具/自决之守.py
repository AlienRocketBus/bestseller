#!/usr/bin/env python3
"""自决之守（1027 立·坑55·作者屡令「你是最高决策人……以后不要问我」）——总编辑⛔问作者、⛔列选项请作者择、⛔候作者之许。

【其由·坑55】作者 1021 两令「这种事还用得着你来问我吗」「你去做所有的决定，以后不要问我」，落总章心诀一与一节「遇事自决」；
  1027 本坐推「备份/演/首演」被平台之权限之检拒，即照平台之惯例列二选项请作者择——作者答「这种事情我之前不是跟你说过好多次了吗？
  为什么你现在还是又问我呢」。根：「⛔问作者」只是总章里一句字，⛔一器拦之；遇平台之拒、遇两可，旧习即复（问而候、工作停滞）。
【其法·零 token】
  ①Stop 钩：取本回合总编辑所书之文（transcript 末一真人之言以後之诸 text），去作者原话（「」『』之内）、代码与引文之行，
    中「请作者择／请作者许／问作者可否」之式即拦（exit 2）——令其自决、自办，再答。stop_hook_active 即放（⛔环）。
  ②PreToolUse 钩（AskUserQuestion）：恒拒——总编辑⛔以问卷候作者。
  ③作者亲令之停（如「411 等我指示」）係作者之令、非问——「等你下令」之报⛔中此守。
  ⑥〔1119 执行之审·治9〕问式添候许二式（「要你点头」「等你…告诉我／跟我说／回我」）——11-16 11:31—12:58 钩活之时漏约十处；
    ⛔添「需要你看｜截图发我」之泛式（唯作者能办之事被顶回只改措辞，徒添误拦）。
    〔1119 执行之审·复核〕施工另添之第三式「(工具|我这边|我这里)…看不到…日志」越出设计、实测误红（「我这边看不到运行日志；已改取 备份/报 之红行」
    「存底守之工具读不到日志时即印缺」「我这里拿不到日志全文，先用 get_job_logs 取其尾」俱中），删——12:57「需要你看…截图发我」係已知之漏：
    欲逮其形，先携误红之语料回设计裁（负测⑩之三守其误红之句⛔再中）。
    钩不载之坐（总编辑之坐 cwd＝/home/user）由 `接棒守.py --巡` 以本器之 中问() 扫其转录代守（治1·c）。
【1027 执行之核·线B】Stop 钩并办二事：
  ④（#24 #128·作者 1024 令）上下文逾三十万：取末一回 assistant 之 usage（input＋cache_read＋cache_creation），>300000 即
    stdout 印 {"systemMessage": "上下文约 N 万，逾三十万：请按 /compact"} 直示作者——⛔顶回（顶回即令模型在三十余万之上再付一整回缓存读·违虹吸）。
    〔1119 执行之审·复核〕治1(d) 曾删此示（谓推键於作者违第一律），然作者常令 1024 令（压缩对话·「压缩对话…会非常主动的去压缩」）之落②
    明令「上下文逾三十万，即於答末一行请作者按 `/compact`」——器⛔与常令分歧：此示复留，删否待总编辑以作者令之位阶另裁（改常令②在先、删示在後）。
    其量（一回之上下文、末回之上下文）兼供 `接棒守.py --巡`（钩不载之坐每日首逾三十万之巡印「减本坐之活」·stderr）。
  ⑤（#88）作者之令先落盘：本回首真人之言逾百字、含令词（以后｜一定要｜必须｜不要再｜要求），而其时以来
    `设定/00_作者常令_不停之律.md` 未改（git log --since 其时、工作区与暂存之 diff 俱空）→ 拦「作者之令先落盘」。
    放行之反例：短问、闲谈（无令词）、已落盘、系统之注（<…>）、【派】之唤。
用法：钩自 stdin 取 JSON（`--停` Stop 之钩｜`--问` AskUserQuestion 之钩）；`python3 工具/自决之守.py --自测`
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

问式 = [
    r'需要?你(来)?(决定|定夺|拍板|选择?|批准|同意|确认|点头)', r'请你(决定|定夺|拍板|选择?|批准|同意|确认)',
    r'由你(来)?(决定|定|选)', r'你来(决定|定|选)', r'你(看|觉得)(怎么样|如何|行不行|可不可以|要不要)',
    r'任选其一', r'二选一', r'(选|挑)哪(一)?(个|种|条)', r'要不要我', r'是否(需要|要)我', r'需要我[^。！\n]{0,12}吗',
    r'可不可以', r'(可以|行|好)吗[？?]', r'等你(的)?(批准|同意|确认|许可|回复|决定)', r'(请|待)作者(决定|择|选|批准|同意|确认|许)',
    r'你同意吗', r'是否同意', r'请(你)?确认', r'(请|须|需)你(授权|许可)',
    # 〔1119 执行之审·治9〕11-16 11:31—12:58 钩活之时漏约十处候许（「这一步要你点头」「等你开好两步验证跟我说一声」）：旧式只认「需要?你…点头」「等你(的)?(批准…)」。
    #   添候许二式（唯设计所许之二）。⛔添「需要你看｜截图发我」之泛式：唯作者能办之事（账单、付款之页）被顶回只改措辞、⛔改行为，徒添误拦（负测⑩之二守之）。
    #   〔1119 执行之审·复核〕施工另添之「(工具|我这边|我这里)…看不到…日志」一式删：实测误中不候许之述（负测⑩之三）；12:57 之形係已知之漏，先携误红语料回设计裁。
    r'要你点头', r'等你[^。\n]{0,20}(告诉我|跟我说|回我)',
]
引 = re.compile(r'「[^」]*」|『[^』]*』|`[^`\n]*`')


def 去引(文):
    """去作者原话（「」『』）、行内代码、代码块与引文之行（> 起）——只判总编辑自己之问。"""
    文 = re.sub(r'```.*?```', '', 文, flags=re.S)
    文 = '\n'.join(l for l in 文.split('\n') if not l.lstrip().startswith('>'))
    return 引.sub('', 文)


否 = re.compile(r'(不|⛔|别|勿|无须|毋|免|没有|未)[再必用需须要]{0,3}[问给让请等候向]?[你作者]{0,2}$')


def 中问(文):
    """→ 所中之片（无即空）。否定之述（「不再等你批准」「⛔问作者」「不用你确认」）⛔算问——1027 首跑即误拦此句。"""
    文 = 去引(文 or '')
    for 式 in 问式:
        for m in re.finditer(式, 文):
            i = m.start()
            if 否.search(文[max(0, i - 6):i]):
                continue
            return 文[max(0, i - 24):i + 24].replace('\n', ' ')
    return ''


def 本回之文(路):
    """transcript（jsonl）：末一真人之言（非 tool_result）以後，诸 assistant 之 text 相接。"""
    诸 = []
    try:
        for 行 in open(路, encoding='utf-8'):
            try:
                d = json.loads(行)
            except Exception:
                continue
            t, m = d.get('type'), d.get('message') or {}
            c = m.get('content')
            if t == 'user':
                if isinstance(c, str) or (isinstance(c, list) and any(isinstance(x, dict) and x.get('type') == 'text' for x in c)):
                    诸 = []
            elif t == 'assistant' and isinstance(c, list):
                诸 += [x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text']
    except Exception:
        return ''
    return '\n'.join(诸)


压之界 = 300000        # 上下文之界（Stop 钩之示；〔1119 执行之审·治1(d)〕接棒守 --巡 亦用之：钩不载之坐逾即印「减本坐之活」）
令词 = re.compile(r'以后|以後|一定要|必须|不要再|要求')
常令档 = os.path.join('设定', '00_作者常令_不停之律.md')
机之首 = ('<', '[', '【派】', '【重派】', '【守书', '【巡】', '【试】', 'Caveat:')   # 1116：【巡】停书之巡、【试】演练俱定时之令     # 系统之注、编排与定时之令（[…] 起）⛔作作者之言


def _诸行(路):
    try:
        with open(路, encoding='utf-8') as f:
            for 行 in f:
                try:
                    yield json.loads(行)
                except Exception:
                    continue
    except Exception:
        return


def 一回之上下文(d):
    """转录之一行 → 其 assistant 之 usage 之 input＋cache_read＋cache_creation（非 assistant 或无 usage 即 0）。
    〔1119 执行之审·治1(d)〕接棒守 --巡 逐增量量本坐之上下文亦用此（同一把尺）。"""
    if not isinstance(d, dict) or d.get('type') != 'assistant':
        return 0
    u = (d.get('message') or {}).get('usage') or {}
    return sum(int(u.get(k) or 0) for k in ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens'))


def 末回之上下文(路):
    """→ 末一回 assistant 之 usage 之 input＋cache_read＋cache_creation（无则 0）。"""
    末 = 0
    for d in _诸行(路):
        n = 一回之上下文(d)
        if n:
            末 = n
    return 末


def 压之示(入):
    """→ 印於 stdout 之 JSON 串（无事 ''）。〔1119 执行之审·复核〕复留（常令 1024 令（压缩对话）②：逾三十万即请作者按 /compact）——删否待总编辑另裁。"""
    n = 末回之上下文(入.get('transcript_path') or '')
    if n > 压之界:
        return json.dumps({'systemMessage': '上下文约 %d 万，逾三十万：请按 /compact' % round(n / 10000)}, ensure_ascii=False)
    return ''


def 本回首言(路):
    """→ (本回首真人之言之文, 其时 ISO)：末一真人之言（非 tool_result、非 isMeta）。"""
    言, 时 = '', ''
    for d in _诸行(路):
        if d.get('type') != 'user' or d.get('isMeta'):
            continue
        c = (d.get('message') or {}).get('content')
        if isinstance(c, list):
            if any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in c):
                continue
            c = '\n'.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
        if isinstance(c, str) and c.strip():
            言, 时 = c, str(d.get('timestamp') or '')
    return 言, 时


def 常令已改(时, root=ROOT):
    """其时以来常令改过否：git log --since 其时 有其提交，或工作区／暂存有其 diff。读不出即作已改（⛔挡）。"""
    import subprocess
    from datetime import datetime, timezone
    try:
        t = datetime.fromisoformat(str(时).replace('Z', '+00:00')) if 时 else datetime(1970, 1, 2, tzinfo=timezone.utc)
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        自 = t.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S +0000')      # ⛔径传 ISO（毫秒与 Z 之式 git 或误析）
        r = subprocess.run(['git', 'log', '--since=%s' % 自, '--format=%h', '--', 常令档], cwd=root,
                           capture_output=True, text=True, timeout=10)
        if r.returncode != 0 or r.stdout.strip():
            return True
        for a in (['git', 'diff', '--quiet', '--', 常令档], ['git', 'diff', '--cached', '--quiet', '--', 常令档]):
            if subprocess.run(a, cwd=root, capture_output=True, timeout=10).returncode != 0:
                return True
        return False
    except Exception:
        return True


def 令落之判(入, 改=None):
    """→ 拦之由（无事 ''）。"""
    言, 时 = 本回首言(入.get('transcript_path') or '')
    s = 言.strip()
    if len(s) <= 100 or s.startswith(机之首):
        return ''
    m = 令词.search(s)
    if not m:
        return ''
    if (改 or 常令已改)(时):
        return ''
    return ('⛔自决之守（作者之令先落盘·1027）：本回作者之言含令（「%s」）而 %s 自其时以来未改——'
            '先把此令落进常令（一行「- MMDD 作者令：「原话」——落：<器／档>」），再办再答。' % (s[max(0, m.start() - 12):m.end() + 12].replace('\n', ' '), 常令档))


由停 = ('⛔自决之守（坑55·作者屡令「你是最高决策人……以后不要问我」）：本回之答请作者择、请作者许或问作者可否——「%s」。'
       '总编辑自决：照最好之法当场办（平台之检拒者⛔绕、另择合规之路自通），办毕再报所为；⛔列选项、⛔候作者之许。')
由问 = '⛔自决之守（坑55）：总编辑⛔以 AskUserQuestion 问作者——照最好之法自决自办（总章一「遇事自决」·作者 1021、1027 屡令）。'


def 判停(入, 改=None):
    if 入.get('stop_hook_active'):
        return ''
    片 = 中问(本回之文(入.get('transcript_path') or ''))
    return 由停 % 片 if 片 else 令落之判(入, 改)


def 判问(入):
    return 由问 if 入.get('tool_name') == 'AskUserQuestion' else ''


def 自测():
    import tempfile
    共 = 过 = 0

    def T(名, ok):
        nonlocal 共, 过
        共 += 1; 过 += bool(ok)
        print('  %s %s' % ('✓' if ok else '✗', 名))

    def 迹(诸):
        f = tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False, encoding='utf-8')
        for 类, c in 诸:
            f.write(json.dumps({'type': 类, 'message': {'role': 类, 'content': c}}, ensure_ascii=False) + '\n')
        f.close()
        return f.name
    答 = lambda s: ('assistant', [{'type': 'text', 'text': s}])
    人 = lambda s: ('user', s)
    果 = ('user', [{'type': 'tool_result', 'content': 'x'}])
    # 1027 之真句：列二选项请作者择 → 拦
    p = 迹([人('做完'), 答('**需要你决定：GitHub 演练流程还没跑过**\n两个办法，任选其一：'), 果, 答('411 照你的指示锁着。')])
    T('①真句（1027：「需要你决定」「任选其一」）→ 拦', '需要你决定' in 判停({'transcript_path': p}))
    for s in ('要不要我先推一回？', '你看怎么样？', '可以吗？', '请你批准这一推。', '是否需要我重跑？', '等你确认後再推。'):
        T('①之二 问式「%s」→ 拦' % s, 判停({'transcript_path': 迹([人('x'), 答(s)])}) != '')
    # 作者原话、报作者之停、代码、引文 → 放
    p = 迹([人('x'), 答('作者令「你不需要问我，可不可以都自己决定」已落总章。411 照你上一条指示锁着，等你下令再开。\n'
                     '```\n需要你决定\n```\n> 任选其一（旧句·引）\n已推 `可以吗？` 之例。')])
    T('②作者原话（「」）、等你下令（作者之停）、代码块、引文行、行内代码 → 放', 判停({'transcript_path': p}) == '')
    # 否定之述（1027 首跑误拦之真句）→ 放；否定之後又真问 → 仍拦
    p = 迹([人('x'), 答('以后所有事我自己定、自己办，办完告诉你结果，不再问你、不再给你选项、也不再等你批准。⛔请你确认之习已废，不用你决定。')])
    T('②之二 否定之述（「也不再等你批准」「不用你决定」·1027 真句）→ 放', 判停({'transcript_path': p}) == '')
    p = 迹([人('x'), 答('也不再等你批准。但这回要不要我先推？')])
    T('②之三 否定之後又真问（「要不要我」）→ 仍拦', '要不要我' in 判停({'transcript_path': p}))
    # 只判本回：前回之问⛔牵连
    p = 迹([人('甲'), 答('需要你决定。'), 人('乙'), 答('已办毕：推送成、主枝已含。')])
    T('③只判本回（末一真人之言以後）：前回之问⛔牵连', 判停({'transcript_path': p}) == '')
    T('④stop_hook_active → 放（⛔环）', 判停({'transcript_path': 迹([人('x'), 答('需要你决定')]), 'stop_hook_active': True}) == '')
    T('⑤迹缺、坏 → 放（⛔挡书）', 判停({'transcript_path': '/nonexistent'}) == '' and 判停({}) == '')
    T('⑥AskUserQuestion → 拒；他器 → 放', 判问({'tool_name': 'AskUserQuestion'}) != '' and 判问({'tool_name': 'Bash'}) == '')
    # ★1027（#24 #128）上下文逾三十万：stdout 之 systemMessage 直示作者、⛔顶回；未逾 → 无（〔1119 执行之审·复核〕复留：常令 1024 令（压缩对话）②）
    def 用(n):
        return ('assistant', [{'type': 'text', 'text': 'x'}]), n
    def 迹u(诸):
        f = tempfile.NamedTemporaryFile('w', suffix='.jsonl', delete=False, encoding='utf-8')
        for 类, c, u in 诸:
            d = {'type': 类, 'message': {'role': 类, 'content': c}}
            if u:
                d['message']['usage'] = {'input_tokens': 2, 'cache_read_input_tokens': u - 1002, 'cache_creation_input_tokens': 1000, 'output_tokens': 50}
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
        f.close()
        return f.name
    大 = 迹u([('user', '甲', 0), ('assistant', [{'type': 'text', 'text': 'x'}], 120000), ('assistant', [{'type': 'text', 'text': 'y'}], 334567)])
    小 = 迹u([('user', '甲', 0), ('assistant', [{'type': 'text', 'text': 'x'}], 450000), ('assistant', [{'type': 'text', 'text': 'y'}], 280000)])
    T('⑧末回上下文 33 万（逾三十万）→ systemMessage「上下文约 33 万…/compact」；末回 28 万（前回虽逾）→ 无；'
      '末回之上下文（接棒守 --巡 同用）：33 万 → 334567、28 万 → 280000（只认末回）；一回之上下文 非 assistant → 0',
      json.loads(压之示({'transcript_path': 大}) or '{}').get('systemMessage', '').startswith('上下文约 33 万') and 压之示({'transcript_path': 小}) == ''
      and 末回之上下文(大) == 334567 > 压之界 and 末回之上下文(小) == 280000 < 压之界
      and 一回之上下文({'type': 'user', 'message': {'usage': {'input_tokens': 9}}}) == 0)
    import subprocess
    p = subprocess.run([sys.executable, os.path.abspath(__file__), '--停'], input=json.dumps({'transcript_path': 大}), capture_output=True, text=True)
    T('⑧之二 真跑：逾界 → rc=0（⛔顶回）、stdout 为 systemMessage 之 JSON（〔1119 执行之审·复核〕复留：器⛔与常令 1024 令（压缩对话）② 分歧）',
      p.returncode == 0 and '/compact' in json.loads(p.stdout or '{}').get('systemMessage', ''))
    # 〔1119 执行之审·治9〕真句回放（11-16 钩活之时漏逮之候许）：红例二；绿例（作者之停、唯作者能办、否定之述）⛔误拦
    #   已知之漏（〔1119 执行之审·复核〕）：12:57「**我需要你看一下失败原因**（我这边的工具看不到运行日志）…把那一段**截图**发我」——
    #   设计只许二式；施工所添「工具看不到日志」一式误中不候许之述（⑩之三），删。欲逮其形，先携⑩之三之误红语料回设计裁，再添。
    红例 = ('我去跑时，被平台的安全检查拦下了，理由是直接推主线属于危险操作。这一步要你点头，我不绕过。',              # 11:31
           '2 笔本地提交（停书巡查和它的补丁）都还在本机，另有一份在备份分支。\n\n等你开好两步验证跟我说一声，我马上重新跑一遍检查，然后推送。')   # 11:40
    T('⑩〔治9〕真句红例：「这一步要你点头」（11:31）、「等你开好两步验证跟我说一声」（11:40）→ 俱拦',
      all(判停({'transcript_path': 迹([人('x'), 答(s)])}) != '' for s in 红例)
      and '要你点头' in 中问(红例[0]) and '跟我说' in 中问(红例[1]))
    绿例 = ('411 照你上一条指示锁着，等你下令（暂停令）再开。',
           '唯作者能办：GitHub 付款之页唯作者登录可见——需要你看一下顶上之红条、截图发我（书照写）。',
           '不用等你回我，我先办；办完再报。')
    T('⑩之二〔治9〕绿例：「等你下令（暂停令）」、「唯作者能办：…需要你看…截图发我（书照写）」（⛔泛式）、「不用等你回我」（否定）→ 俱放',
      all(判停({'transcript_path': 迹([人('x'), 答(s)])}) == '' for s in 绿例))
    误红 = ('GitHub 之器今连不上，我这边看不到运行日志；已改取 备份/报 之红行，照其治。',
           '存底守之工具读不到日志时即印缺，⛔印 0。',
           '我这里拿不到日志全文，先用 get_job_logs 取其尾。')
    T('⑩之三〔1119 执行之审·复核〕守牙：不候许之述（「我这边看不到运行日志；已改取 备份/报」「工具读不到日志时即印缺」「拿不到日志全文，先用 get_job_logs」）→ 俱放'
      '（施工另添之「工具看不到日志」一式曾俱误中·Stop 钩每误中一回即顶回一整回）',
      all(中问(s) == '' and 判停({'transcript_path': 迹([人('x'), 答(s)])}) == '' for s in 误红))
    # ★1027（#88）作者之令先落盘：逾百字、含令词、常令未改 → 拦；短问、闲谈、已落盘、系统之注、【派】→ 放
    长令 = '以后每一章封版之前，你一定要先把开镜卡与章料对一遍，凡是开镜卡里点了名的旧章之句都要整段展开放进料里，' * 2
    长谈 = '今天这一章读下来很顺，沈鸢那一段我很喜欢，钱满盯章的那个眼神写得好，街口空着那一句也好，' * 3
    未改, 已改 = (lambda t: False), (lambda t: True)
    T('⑨长令（含「以后」「一定要」）而常令未改 → 拦「作者之令先落盘」', '先落盘' in 判停({'transcript_path': 迹([人(长令), 答('已办。')])}, 改=未改))
    T('⑨之二 已落盘（常令已改）→ 放', 判停({'transcript_path': 迹([人(长令), 答('已办。')])}, 改=已改) == '')
    T('⑨之三 短问（含令词而不逾百字）、长之闲谈（无令词）→ 放',
      判停({'transcript_path': 迹([人('以后还要等多久？'), 答('约一时。')])}, 改=未改) == ''
      and 判停({'transcript_path': 迹([人(长谈), 答('多谢。')])}, 改=未改) == '')
    T('⑨之四 系统之注（<task-notification>）、【派】之唤 → 放；本回之首以末一真人之言计（其後之 tool_result ⛔算）',
      判停({'transcript_path': 迹([人('<task-notification>' + 长令 + '</task-notification>'), 答('x')])}, 改=未改) == ''
      and 判停({'transcript_path': 迹([人('【派】' + 长令), 答('x')])}, 改=未改) == ''
      and '先落盘' in 判停({'transcript_path': 迹([人(长令), 答('x'), 果, 答('y')])}, 改=未改))
    import shutil as _sh
    g = tempfile.mkdtemp(prefix='自决_')
    try:
        os.makedirs(os.path.join(g, '设定'))
        e = dict({k: v for k, v in os.environ.items() if not k.startswith('GIT_')}, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
                 GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t', GIT_CONFIG_GLOBAL=os.devnull)
        跑 = lambda *a: subprocess.run(list(a), cwd=g, capture_output=True, env=e)
        open(os.path.join(g, 常令档), 'w', encoding='utf-8').write('一\n')
        跑('git', 'init', '-q'); 跑('git', 'add', '-A'); 跑('git', 'commit', '-q', '-m', 'a')
        import time as _t
        未来 = _t.strftime('%Y-%m-%dT%H:%M:%S.000Z', _t.gmtime(_t.time() + 3600))      # 转录之时之式（毫秒、Z）
        前 = 常令已改('2000-01-01T00:00:00.000Z', g)
        後 = 常令已改(未来, g)
        open(os.path.join(g, 常令档), 'a', encoding='utf-8').write('- 1027 作者令：……\n')
        改後 = 常令已改(未来, g)
        T('⑨之五 真判（临时之库）：其时以来有提交 → 已改；无提交无 diff → 未改；工作区改之 → 已改', 前 and not 後 and 改後)
    finally:
        _sh.rmtree(g, ignore_errors=True)
    # 接线：settings 之 Stop 与 PreToolUse(AskUserQuestion) 俱挂本守
    try:
        h = json.load(open(os.path.join(ROOT, '.claude', 'settings.json'), encoding='utf-8')).get('hooks', {})
        停接 = any('自决之守.py --停' in x.get('command', '') for m in h.get('Stop', []) for x in m.get('hooks', []))
        问接 = any('自决之守.py --问' in x.get('command', '') and re.search(m.get('matcher') or '', 'AskUserQuestion')
                 for m in h.get('PreToolUse', []) for x in m.get('hooks', []))
    except Exception:
        停接 = 问接 = False
    T('⑦接线：.claude/settings.json 之 Stop 挂 --停、PreToolUse（AskUserQuestion）挂 --问', 停接 and 问接)
    print('── 自决之守·自测 %d/%d %s ──' % (过, 共, '全通' if 过 == 共 else '未过'))
    return 过 == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    try:
        入 = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                      # 入坏⛔拦（本钩只防问作者，⛔挡书）
    由 = 判问(入) if '--问' in a else 判停(入)
    if 由:
        print(由, file=sys.stderr)
        sys.exit(2)
    if '--问' not in a:
        try:
            示 = 压之示(入)          # 上下文逾三十万：直示作者一行（⛔顶回）——〔1119 执行之审·复核〕复留：常令 1024 令（压缩对话）②，删否待总编辑另裁
        except Exception:
            示 = ''
        if 示:
            print(示)
    sys.exit(0)
