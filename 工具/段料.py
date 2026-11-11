#!/usr/bin/env python3
"""段料（1013 立·造式二代 §四：段案之料，零 token）——每十章一份段案之前，机器先把料汇齐，设计席只读此档。

汇：余章总案 §二之裁｜§四 本段诸章之行｜§五 收线表涉本段之行｜§七 之种（若涉）｜悬线钉在本段之行｜
    canon 有界之卡（only_ch／from_ch 落本段）｜全员之账（章料.全员，坑⑬）｜总纲本段逐章之日｜前两章白文｜叫绝之拍库全文｜段案之格｜
    ★1027 X47：剧情庭之守令（本段之势「守令」一节全文·置料首）——段案 398—400 立席未逮守令首条「⛔回信」、驳席方逮（复盘 1020_W54），
    立令未把守令逐条摆出；今料首即列，立席首回即守。
限：≤150KB（坑③：档要短）。

用法：
  python3 工具/段料.py 390 399 [出档]   → 写 设定/段案/_料_390-399.md（或出档）
  python3 工具/段料.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import 章料
限 = 150 * 1024
格 = """## 〔段案之格〕（工具/段案验.py 据此验；每章一节，八项俱全）

## <章号>
- 重：轻｜中｜重（重＝爆章、叫绝之拍所在、全书之钉）
- 魂路：两三条，取 翻个儿／不说／速度／换账／物证／咬合／回声，以「｜」相隔
- 叫绝之拍：一句（对标拍库第N拍）
- 种：埋「…」→收 NNN；收「…」（埋於 NNN）——无则写「无」
- 知之变：谁、知何事
- 物之动：何物由谁到谁、在哪
- 日：照总纲（如 暗·142）
- 钩：章尾之钩一句"""


def 行於(文, a, b):
    pat = re.compile(r'(?<!\d)(%s)(?!\d)' % '|'.join(str(k) for k in range(a, b + 1)))
    return [l for l in 文.split('\n') if pat.search(l)]


def 总纲之日(纲, a, b):
    """→ {章: '主·153'}。总纲两栏排（左 381、右 404），整行逐栏认。"""
    return {int(m.group(1)): m.group(2) for m in re.finditer(r'\|\s*(\d{3})\s*\|\s*([主暗]·\d+)\s*\|', 纲) if a <= int(m.group(1)) <= b}


def 段首(n):
    return 381 + (n - 381) // 10 * 10


def 守令(a, root=ROOT):
    """★1027 X47：本段剧情庭之势（设定/剧情庭_势_第S段.md）之「守令」一节（###…守令… 至下一 ### 或 ##）→ (档, 文)；无势或无其节 → (档, '')。"""
    档 = os.path.join('设定', '剧情庭_势_第%d段.md' % 段首(a))
    p = os.path.join(root, 档)
    t = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
    m = re.search(r'^(###[^\n]*守令[^\n]*\n.*?)(?=^##[# ]|\Z)', t, re.M | re.S)
    return 档, (m.group(1).strip() if m else '')


def 汇(a, b, root=ROOT, 出=None, 顶=限):
    读 = lambda p: open(os.path.join(root, p), encoding='utf-8').read() if os.path.exists(os.path.join(root, p)) else ''
    案 = 读('设定/剧情庭题/余章总案.md')
    纲 = 读('设定/02_余章之势_总纲.md')
    段 = []
    令档, 令 = 守令(a, root)
    段.append(('剧情庭之守令（%s·立席首回逐条守之；段案诸⛔之上加之）' % 令档,
              令 or '（本段之势未立或无「守令」一节——先开剧情庭（段序之守：上段大审 → 剧情庭 → 段料）；⛔无守令而立段案）'))
    段.append(('气鼎之律（本书之科学·凡事须指律；指不出即洞·1107 作者令）', 读('设定/气鼎之律.md')))
    段.append(('余章总案·解歧之裁', 章料.节(案, '## 二、')))
    段.append(('余章总案·§四 本段诸章之行（%d—%d）' % (a, b), '\n'.join(行於(章料.节(案, '## 四、'), a, b))))
    段.append(('余章总案·§五 收线表涉本段之行', '\n'.join(行於(章料.节(案, '## 五、'), a, b))))
    七 = 章料.节(案, '## 七、')
    if 行於(七, a, b):
        段.append(('余章总案·§七 本段之种', 七))
    # ★1013：380—389 之拍定在 D6／D3 之主案（余章总案 §七「只在 D6／D3 之拍旁添」）——汇诸题现行主案涉本段之行（⛔已被後审所代之三审／四审／五审）
    import glob as _g
    for f in sorted(_g.glob(os.path.join(root, '设定', '剧情庭题', '*主案.md'))):
        if re.search(r'[三四五]审主案', os.path.basename(f)):
            continue
        行们 = 行於(open(f, encoding='utf-8').read(), a, b)
        if 行们:
            段.append(('主案·%s 涉本段之行' % os.path.basename(f)[:-3], '\n'.join(行们)))
    段.append(('悬线·钉在本段之行', '\n'.join(行於(读('设定/全书记忆/悬线.md'), a, b))))
    库 = json.loads(读('设定/canon事实库.json') or '{}')
    卡 = []
    for f in 库.get('facts', []):
        o, fr = f.get('only_ch') or [], f.get('from_ch')
        if any(a <= k <= b for k in o) or (fr and a <= fr <= b):
            卡.append('- **%s**（%s）：%s' % (f.get('id'), f.get('level'), str(f.get('note', ''))[:900]))
    if 卡:
        段.append(('canon 有界之卡（落本段）', '\n'.join(卡)))
    册 = json.loads(读('设定/人物状态册.json') or '{}')
    段.append(('全员之账（生死、末见、线、最新之态）', '\n'.join(章料.全员(册))))
    日 = 总纲之日(纲, a, b)
    段.append(('总纲·本段逐章之日', '\n'.join('| %d | %s |' % (k, 日[k]) for k in sorted(日))))
    for k in (a - 1, a - 2):
        f = 章料.章档(k, root)
        if f:
            段.append(('前文·第%d章白文（全）' % k, open(f, encoding='utf-8').read()))
    段.append(('叫绝之拍库（全）', 读('设定/叫绝之拍库.md')))
    段.append(('段案之格', 格))
    # ★1111（W111·441 段料 159KB）：逾顶先舍 a-2 章之白文（a-1 章仍全；a-2 章由立席 sed -n 另读其所须之行）——⛔舍诸账
    if 顶 and sum(len((t or '').encode()) for _, t in 段) > 顶 - 2048:
        舍名 = '前文·第%d章白文（全）' % (a - 2)
        段 = [(n, t) if n != 舍名 else ('前文·第%d章白文（逾顶舍之）' % (a - 2), '（段料逾 %d KB·坑③：本章白文舍去；须者 sed -n 另读 %s）' % (顶 // 1024, os.path.relpath(章料.章档(a - 2, root) or '', root))) for n, t in 段]
    文 = ['# 第%d—%d章·段料（工具/段料.py 零 token 汇；设计席只读此档，料外只许 grep 核一处、上下三行）\n' % (a, b)]
    for 名, t in 段:
        文.append('## 〔%s〕\n\n%s\n' % (名, (t or '（无）').strip()))
    出 = 出 or os.path.join(root, '设定', '段案', '_料_%d-%d.md' % (a, b))
    os.makedirs(os.path.dirname(出), exist_ok=True)
    open(出, 'w', encoding='utf-8').write('\n'.join(文))
    大 = os.path.getsize(出)
    for 名, t in 段:
        print('  %-30s %7d 字节' % (名, len((t or '').encode())))
    print('✓ 写 %s（%d KB）' % (os.path.relpath(出, root), 大 // 1024))
    if 顶 and 大 > 顶:
        print('⛔ 段料 %d KB 逾 %d KB（坑③）' % (大 // 1024, 顶 // 1024)); return None
    return 出


def 自测():
    ok = 共 = 0
    共 += 1; ok += (行於('a 390 b\nc 3901\nd 399 e\nf 400', 390, 399) == ['a 390 b', 'd 399 e'])
    import tempfile, shutil, io, contextlib
    t = tempfile.mkdtemp()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            p = 汇(381, 389, ROOT, os.path.join(t, 'x.md'), 顶=None)   # ★1014：381—389 已写成之段，其悬线随记席一章章长（151KB）——验诸节在不在⛔受顶（第二十八犯之族：⛔钉快照）
            q = 汇(381, 389, ROOT, os.path.join(t, 'y.md'), 顶=1024)       # 顶照拦（真用照守 150KB）
        s = open(p, encoding='utf-8').read() if p else ''
        共 += 1; ok += (q is None)
        共 += 1; ok += bool(p) and all(k in s for k in ('〔气鼎之律', '## 母律', '〔余章总案·解歧之裁〕', '〔全员之账', '〔总纲·本段逐章之日〕', '| 381 | 暗·142 |', '〔段案之格〕', '四十拍'))
        纲 = open(os.path.join(ROOT, '设定', '02_余章之势_总纲.md'), encoding='utf-8').read()
        日 = 总纲之日(纲, 381, 405)
        共 += 1; ok += (日.get(381) == '暗·142' and 日.get(404) == '主·160' and 日.get(405) == '暗·154' and len(日) == 25)   # 右栏之章亦认
        # ★1027 X47：守令置料首——398—400（391 段）之料首节即「⛔「回信」」之守令（W54 立席所漏）；401 段之守令取其段之势；无势之段印「先开剧情庭」
        _档, _令 = 守令(398)
        _档2, _令2 = 守令(405)
        with contextlib.redirect_stdout(io.StringIO()):
            r = 汇(398, 400, ROOT, os.path.join(t, 'z.md'), 顶=None)
        z = open(r, encoding='utf-8').read() if r else ''
        共 += 1; ok += (_档.endswith('剧情庭_势_第391段.md') and '⛔「回信」' in _令 and '## 二、' not in _令
                       and '二线律' in _令2 and z.split('\n## 〔')[1].startswith('剧情庭之守令') and '⛔「回信」' in z.split('〔余章总案·解歧之裁〕')[0]
                       and 守令(9991)[1] == '' and 段首(411) == 411 and 段首(420) == 411)
    finally:
        shutil.rmtree(t)
    print('段料·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) in (2, 3) and a[0].isdigit() and a[1].isdigit():
        sys.exit(0 if 汇(int(a[0]), int(a[1]), 出=a[2] if len(a) == 3 else None) else 1)
    print(__doc__); sys.exit(2)
