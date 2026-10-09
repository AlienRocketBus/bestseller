#!/usr/bin/env python3
"""复盘（1009 立·作者令「每一次任务都要复盘：踩的坑、哪里做了无用功、哪里花了大量 token 与时却无实果、
具体之改进方案；每回都要有详细之任务记录与具体耗费——越来越有效、越来越科学之 token 用法」）。

本器零 token 起草一份复盘：任务之记录（取自 `设定/工作流账.json`）＋每个 Run 之费审（`工具/费审.py`）自动填入；
「无用功」一节先列机器之疑点（来回最多之席、机器之活之占、超估之倍），**总编辑须亲写其判与改进方案**。
无复盘不许结案（`工具/工作流账.py --裁 W 取／重造` 先验 `设定/复盘/*W*.md` 三节俱在）。

用法：
  python3 工具/复盘.py W12 380造式 wf_e7912fa3-a0c [其他 Run ID…]   → 写 设定/复盘/<月日>_W12_380造式.md（已在则⛔覆）
  python3 工具/复盘.py --自测
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


def 起草(W, 题, runs, root=ROOT, 日=None):
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
    费段, 疑 = [], []
    总读 = 0
    for r in runs:
        d = r if os.path.isdir(r) else (glob.glob(os.path.expanduser('~/.claude/projects/*/*/subagents/workflows/%s' % r)) or [r])[0]
        if not os.path.isdir(d):
            费段.append('- Run %s：找不到其目录（非工作流之席，耗费照其回执手填）' % r); continue
        行 = 费审.审(d)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            费审.印(行)
        费段.append('### Run %s\n\n```\n%s```' % (r, buf.getvalue()))
        读 = sum(x['读'] for x in 行) or 1
        总读 += 读
        for x in sorted(行, key=lambda x: -x['回'])[:3]:
            疑.append('- 来回最多：%s（%d 回、工具 %d、缓存读 %d）——是在造，还是在翻料／办机器之活？' % (x['名'], x['回'], x['具'], x['读']))
        机 = sum(x['读'] for x in 行 if any(k in x['名'] for k in ('定位', '机闸', '案席', '封版', '长令席')))
        if 机:
            疑.append('- 机器之活（定位／机闸／案席／封版／长令席）占缓存读 %d%%——凡机器能办者，下回归脚本' % (100 * 机 // 读))
    文 = ['# 复盘·%s·%s（%s 立）' % (W, 题, 日), '',
         '## 任务', '',
         '- 名：%s' % 件.get('名', ''), '- 目的：%s' % str(件.get('目的', ''))[:400],
         '- 停止线：%s' % 件.get('停止线', ''), '- 预估：%s' % 件.get('预估', ''),
         '- 裁：%s' % '；'.join('%s %s' % (x.get('法'), str(x.get('由', ''))[:160]) for x in 件.get('裁', [])), '',
         '## 产出', '', '（总编辑填：成了什么、质之实据——致命数、行家对拍库之分、盲读）', '',
         '## 耗费', '', '- 合计缓存读：%d（各 Run 详下）；实耗之 token 与时照工作流回执填：' % 总读, ''] + 费段 + ['',
         '## 无用功', '', '机器之疑（总编辑逐条判：真费、或该花）：'] + (疑 or ['- （无 Run 可审）']) + ['', '（总编辑填：哪里花了大量 token 与时而无实果，其根）', '',
         '## 刀刃', '', '（总编辑填：钱花在哪儿真出了果）', '',
         '## 改进方案', '', '（总编辑填：具体到改哪档哪条；下回照办之验——下回之费审拿什么数比）', '',
         '## 坑之账', '', '（新坑一行，入四入口档之坑之账）', '']
    open(出, 'w', encoding='utf-8').write('\n'.join(文))
    print('✓ 起草 %s——「产出」「无用功」之判「刀刃」「改进方案」「坑之账」须总编辑亲填' % os.path.relpath(出, root))
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
        ok = bool(f) and g is None and all(k in s for k in ('## 耗费', '## 无用功', '## 改进方案')) and '机器之活' in s
    finally:
        shutil.rmtree(t)
    print('复盘·自测 %d/1' % int(ok))
    return ok


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) < 2:
        print(__doc__); sys.exit(2)
    起草(a[0], a[1], a[2:])
