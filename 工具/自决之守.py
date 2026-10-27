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
]
引 = re.compile(r'「[^」]*」|『[^』]*』|`[^`\n]*`')


def 去引(文):
    """去作者原话（「」『』）、行内代码、代码块与引文之行（> 起）——只判总编辑自己之问。"""
    文 = re.sub(r'```.*?```', '', 文, flags=re.S)
    文 = '\n'.join(l for l in 文.split('\n') if not l.lstrip().startswith('>'))
    return 引.sub('', 文)


def 中问(文):
    文 = 去引(文 or '')
    for 式 in 问式:
        m = re.search(式, 文)
        if m:
            i = m.start()
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


由停 = ('⛔自决之守（坑55·作者屡令「你是最高决策人……以后不要问我」）：本回之答请作者择、请作者许或问作者可否——「%s」。'
       '总编辑自决：照最好之法当场办（平台之检拒者⛔绕、另择合规之路自通），办毕再报所为；⛔列选项、⛔候作者之许。')
由问 = '⛔自决之守（坑55）：总编辑⛔以 AskUserQuestion 问作者——照最好之法自决自办（总章一「遇事自决」·作者 1021、1027 屡令）。'


def 判停(入):
    if 入.get('stop_hook_active'):
        return ''
    片 = 中问(本回之文(入.get('transcript_path') or ''))
    return 由停 % 片 if 片 else ''


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
    # 只判本回：前回之问⛔牵连
    p = 迹([人('甲'), 答('需要你决定。'), 人('乙'), 答('已办毕：推送成、主枝已含。')])
    T('③只判本回（末一真人之言以後）：前回之问⛔牵连', 判停({'transcript_path': p}) == '')
    T('④stop_hook_active → 放（⛔环）', 判停({'transcript_path': 迹([人('x'), 答('需要你决定')]), 'stop_hook_active': True}) == '')
    T('⑤迹缺、坏 → 放（⛔挡书）', 判停({'transcript_path': '/nonexistent'}) == '' and 判停({}) == '')
    T('⑥AskUserQuestion → 拒；他器 → 放', 判问({'tool_name': 'AskUserQuestion'}) != '' and 判问({'tool_name': 'Bash'}) == '')
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
    sys.exit(0)
